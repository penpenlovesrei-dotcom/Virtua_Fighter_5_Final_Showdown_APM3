#!/usr/bin/env python3
"""Desassemblage cible d'un PE x64 : recherche de xrefs et rendu de fonctions.

S'appuie sur pefile pour la structure et capstone pour le desassemblage.
Concu pour vf5fs-pxd-w64-*.dll, mais generique.

Usage:
    py -3 tools/pe_disasm.py <pe> info
    py -3 tools/pe_disasm.py <pe> str <motif>            chaines + leur VA
    py -3 tools/pe_disasm.py <pe> xref <va>              qui reference cette VA
    py -3 tools/pe_disasm.py <pe> func <va> [--max N]    desassemble a partir de VA
    py -3 tools/pe_disasm.py <pe> back <va> [--win N]    remonte au debut de fonction
"""
import re
import struct
import sys

import capstone
import pefile


class Image:
    def __init__(self, path):
        self.pe = pefile.PE(path, fast_load=True)
        self.base = self.pe.OPTIONAL_HEADER.ImageBase
        self.secs = []
        for s in self.pe.sections:
            name = s.Name.rstrip(b"\0").decode("latin-1")
            self.secs.append(dict(
                name=name,
                va=self.base + s.VirtualAddress,
                vsize=s.Misc_VirtualSize,
                off=s.PointerToRawData,
                rsize=s.SizeOfRawData,
                exec=bool(s.Characteristics & 0x20000000),
            ))
        with open(path, "rb") as fp:
            self.data = fp.read()
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.md.detail = True
        self._funcs = None

    def off2va(self, off):
        for s in self.secs:
            if s["off"] <= off < s["off"] + s["rsize"]:
                return s["va"] + (off - s["off"])
        return None

    def va2off(self, va):
        for s in self.secs:
            if s["va"] <= va < s["va"] + s["vsize"]:
                d = va - s["va"]
                if d < s["rsize"]:
                    return s["off"] + d
        return None

    def sec_of(self, va):
        for s in self.secs:
            if s["va"] <= va < s["va"] + s["vsize"]:
                return s
        return None

    def text_sections(self):
        return [s for s in self.secs if s["exec"]]

    def read(self, va, n):
        off = self.va2off(va)
        return self.data[off:off + n] if off is not None else b""


def cmd_info(img):
    print("base   : 0x%X" % img.base)
    print("%-10s %-18s %-10s %-10s %s" % ("section", "va", "vsize", "raw off", "exec"))
    for s in img.secs:
        print("%-10s 0x%016X 0x%08X 0x%08X %s"
              % (s["name"], s["va"], s["vsize"], s["off"], "X" if s["exec"] else ""))


def cmd_str(img, pattern):
    pat = re.compile(pattern.encode(), re.I)
    seen = 0
    for m in re.finditer(rb"[\x20-\x7e]{4,200}", img.data):
        if not pat.search(m.group()):
            continue
        va = img.off2va(m.start())
        print("off=0x%08X  va=%s  %s"
              % (m.start(), ("0x%016X" % va) if va else "-" * 18,
                 m.group().decode("latin-1")))
        seen += 1
        if seen > 200:
            print("... (tronque)")
            break


def runtime_functions(img):
    """Bornes exactes des fonctions, lues dans .pdata (RUNTIME_FUNCTION x64).

    Chaque entree fait 12 octets : BeginAddress, EndAddress, UnwindInfoAddress,
    tous en RVA.
    """
    if img._funcs is not None:
        return img._funcs
    sec = None
    for s in img.secs:
        if s["name"] == ".pdata":
            sec = s
            break
    if sec is None:
        img._funcs = []
        return img._funcs
    blob = img.data[sec["off"]:sec["off"] + sec["rsize"]]
    out = []
    for i in range(0, len(blob) - 11, 12):
        beg, end, _unw = struct.unpack("<III", blob[i:i + 12])
        if beg == 0 and end == 0:
            continue
        if end <= beg:
            continue
        out.append((img.base + beg, img.base + end))
    out.sort()
    img._funcs = out
    return out


def func_bounds(img, va):
    """Fonction contenant `va`, d'apres .pdata."""
    funcs = runtime_functions(img)
    lo, hi = 0, len(funcs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        b, e = funcs[mid]
        if va < b:
            hi = mid - 1
        elif va >= e:
            lo = mid + 1
        else:
            return b, e
    return None


def iter_code(img):
    """Desassemble fonction par fonction d'apres .pdata ; a defaut, balayage
    lineaire robuste qui reprend apres chaque octet invalide."""
    funcs = runtime_functions(img)
    if funcs:
        for beg, end in funcs:
            off = img.va2off(beg)
            if off is None:
                continue
            yield beg, img.data[off:off + (end - beg)]
        return
    for s in img.text_sections():
        blob = img.data[s["off"]:s["off"] + s["rsize"]]
        pos = 0
        while pos < len(blob):
            last = pos
            for ins in img.md.disasm(blob[pos:], s["va"] + pos):
                last = ins.address - s["va"] + ins.size
            if last <= pos:
                pos += 1
            else:
                yield s["va"] + pos, blob[pos:last]
                pos = last


def cmd_xref(img, target, quiet=False):
    """Instructions dont un operande memoire RIP-relatif vise `target`,
    plus les immediats egaux a `target`."""
    hits = []
    for va, blob in iter_code(img):
        for ins in img.md.disasm(blob, va):
            for op in ins.operands:
                if op.type == capstone.x86.X86_OP_MEM and op.mem.base == capstone.x86.X86_REG_RIP:
                    if ins.address + ins.size + op.mem.disp == target:
                        hits.append((ins.address, ins.mnemonic, ins.op_str))
                elif op.type == capstone.x86.X86_OP_IMM and op.imm == target:
                    hits.append((ins.address, ins.mnemonic, ins.op_str))
    if not quiet:
        for a, m, o in hits:
            fb = func_bounds(img, a)
            print("0x%016X  %-8s %-34s  [fonction 0x%X]"
                  % (a, m, o, fb[0] if fb else 0))
        print("%d reference(s)" % len(hits))
    return [h[0] for h in hits]


PROLOGUES = (b"\x48\x89\x5c\x24", b"\x48\x89\x54\x24", b"\x48\x89\x4c\x24",
             b"\x40\x53", b"\x40\x55", b"\x40\x56", b"\x40\x57",
             b"\x48\x83\xec", b"\x48\x81\xec", b"\x55\x48\x8b\xec")


def find_start(img, va, window=0x800):
    """Remonte jusqu'a un int3/ret suivi d'un prologue plausible."""
    off = img.va2off(va)
    lo = max(0, off - window)
    blob = img.data[lo:off]
    # Dernier alignement int3 (0xCC) suivi d'octets non-0xCC
    best = None
    for i in range(len(blob) - 1, 0, -1):
        if blob[i - 1] == 0xCC and blob[i] != 0xCC:
            cand = lo + i
            if any(img.data[cand:cand + len(p)] == p for p in PROLOGUES):
                best = cand
                break
            if best is None:
                best = cand
    return img.off2va(best) if best is not None else None


def cmd_func(img, va, maxins=200, stop_at_ret=True):
    s = img.sec_of(va)
    off = img.va2off(va)
    end = s["off"] + s["rsize"]
    blob = img.data[off:min(end, off + maxins * 15)]
    n = 0
    for ins in img.md.disasm(blob, va):
        note = ""
        for op in ins.operands:
            if op.type == capstone.x86.X86_OP_MEM and op.mem.base == capstone.x86.X86_REG_RIP:
                tgt = ins.address + ins.size + op.mem.disp
                note = "  ; -> 0x%X" % tgt
                raw = img.read(tgt, 64)
                if raw:
                    m = re.match(rb"[\x20-\x7e]{3,60}", raw)
                    if m:
                        note += '  "%s"' % m.group().decode("latin-1")
        print("0x%016X  %-24s %-40s%s"
              % (ins.address, ins.bytes.hex(), "%s %s" % (ins.mnemonic, ins.op_str), note))
        n += 1
        if n >= maxins:
            break
        if stop_at_ret and ins.mnemonic == "ret":
            break


def main():
    img = Image(sys.argv[1])
    cmd = sys.argv[2]
    if cmd == "info":
        cmd_info(img)
    elif cmd == "str":
        cmd_str(img, sys.argv[3])
    elif cmd == "xref":
        cmd_xref(img, int(sys.argv[3], 0))
    elif cmd == "func":
        n = 200
        if "--max" in sys.argv:
            n = int(sys.argv[sys.argv.index("--max") + 1])
        cmd_func(img, int(sys.argv[3], 0), n)
    elif cmd == "back":
        va = int(sys.argv[3], 0)
        st = find_start(img, va)
        print("debut probable : 0x%X" % st if st else "non trouve")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
