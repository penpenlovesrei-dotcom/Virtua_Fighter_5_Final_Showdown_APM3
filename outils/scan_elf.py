#!/usr/bin/env python3
"""Lecteur ELF minimal (32/64, LE/BE) : en-tete, sections, segments, dynamique.

Usage:
    py -3 tools/scan_elf.py <fichier> [--sections] [--dyn] [--syms N]
"""
import struct
import sys

EM = {
    0x03: "EM_386", 0x3E: "EM_X86_64", 0x14: "EM_PPC", 0x15: "EM_PPC64",
    0x28: "EM_ARM", 0xB7: "EM_AARCH64", 0x08: "EM_MIPS", 0x2A: "EM_SH",
}
ET = {0: "NONE", 1: "REL", 2: "EXEC", 3: "DYN", 4: "CORE"}
PT = {
    0: "NULL", 1: "LOAD", 2: "DYNAMIC", 3: "INTERP", 4: "NOTE", 5: "SHLIB",
    6: "PHDR", 7: "TLS", 0x6474E550: "GNU_EH_FRAME", 0x6474E551: "GNU_STACK",
    0x6474E552: "GNU_RELRO",
}
SHT = {
    0: "NULL", 1: "PROGBITS", 2: "SYMTAB", 3: "STRTAB", 4: "RELA", 5: "HASH",
    6: "DYNAMIC", 7: "NOTE", 8: "NOBITS", 9: "REL", 11: "DYNSYM",
    14: "INIT_ARRAY", 15: "FINI_ARRAY", 16: "PREINIT_ARRAY",
}
DT = {
    1: "NEEDED", 2: "PLTRELSZ", 3: "PLTGOT", 4: "HASH", 5: "STRTAB", 6: "SYMTAB",
    12: "INIT", 13: "FINI", 14: "SONAME", 15: "RPATH", 16: "SYMBOLIC",
    0x1D: "RUNPATH",
}


class Elf:
    def __init__(self, path):
        with open(path, "rb") as fp:
            self.data = fp.read()
        d = self.data
        if d[:4] != b"\x7fELF":
            raise ValueError("pas un ELF")
        self.cls = d[4]           # 1=32, 2=64
        self.end = "<" if d[5] == 1 else ">"
        self.is64 = self.cls == 2
        e = self.end
        self.etype, self.machine = struct.unpack(e + "HH", d[16:20])
        if self.is64:
            (self.entry, self.phoff, self.shoff) = struct.unpack(e + "QQQ", d[24:48])
            (self.phentsize, self.phnum, self.shentsize, self.shnum,
             self.shstrndx) = struct.unpack(e + "HHHHH", d[54:64])
        else:
            (self.entry, self.phoff, self.shoff) = struct.unpack(e + "III", d[24:36])
            (self.phentsize, self.phnum, self.shentsize, self.shnum,
             self.shstrndx) = struct.unpack(e + "HHHHH", d[42:52])
        self.sections = self._sections()
        self.segments = self._segments()

    def _segments(self):
        e, d, out = self.end, self.data, []
        for i in range(self.phnum):
            o = self.phoff + i * self.phentsize
            if self.is64:
                p_type, p_flags = struct.unpack(e + "II", d[o:o + 8])
                p_off, p_vaddr, _pa, p_filesz, p_memsz = struct.unpack(
                    e + "QQQQQ", d[o + 8:o + 48])
            else:
                p_type, p_off, p_vaddr, _pa, p_filesz, p_memsz, p_flags = \
                    struct.unpack(e + "IIIIIII", d[o:o + 28])
            out.append(dict(type=PT.get(p_type, hex(p_type)), off=p_off,
                            vaddr=p_vaddr, filesz=p_filesz, memsz=p_memsz,
                            flags=p_flags))
        return out

    def _sections(self):
        if not self.shoff or not self.shnum:
            return []
        e, d, raw = self.end, self.data, []
        for i in range(self.shnum):
            o = self.shoff + i * self.shentsize
            if self.is64:
                nm, typ, _fl, addr, off, size, link, info, _al, entsz = \
                    struct.unpack(e + "IIQQQQIIQQ", d[o:o + 64])
            else:
                nm, typ, _fl, addr, off, size, link, info, _al, entsz = \
                    struct.unpack(e + "IIIIIIIIII", d[o:o + 40])
            raw.append(dict(nameoff=nm, type=typ, addr=addr, off=off, size=size,
                            link=link, info=info, entsize=entsz))
        if self.shstrndx < len(raw):
            strtab = raw[self.shstrndx]
            blob = d[strtab["off"]:strtab["off"] + strtab["size"]]
            for s in raw:
                end = blob.find(b"\0", s["nameoff"])
                s["name"] = blob[s["nameoff"]:end].decode("latin-1")
        return raw

    def sec(self, name):
        for s in self.sections:
            if s.get("name") == name:
                return s
        return None

    def dynamic(self):
        s = self.sec(".dynamic")
        if not s:
            for p in self.segments:
                if p["type"] == "DYNAMIC":
                    s = dict(off=p["off"], size=p["filesz"], link=None)
                    break
        if not s:
            return []
        e, d = self.end, self.data
        step = 16 if self.is64 else 8
        fmt = e + ("QQ" if self.is64 else "II")
        strtab = self.sec(".dynstr")
        blob = d[strtab["off"]:strtab["off"] + strtab["size"]] if strtab else b""
        out = []
        for o in range(s["off"], s["off"] + s["size"], step):
            tag, val = struct.unpack(fmt, d[o:o + step])
            if tag == 0:
                break
            txt = ""
            if tag in (1, 14, 15, 0x1D) and blob:
                end = blob.find(b"\0", val)
                txt = blob[val:end].decode("latin-1")
            out.append((DT.get(tag, hex(tag)), val, txt))
        return out

    def symbols(self, section=".symtab"):
        s = self.sec(section)
        if not s:
            return []
        strs = self.sections[s["link"]] if s["link"] < len(self.sections) else None
        blob = self.data[strs["off"]:strs["off"] + strs["size"]] if strs else b""
        e, d, out = self.end, self.data, []
        step = 24 if self.is64 else 16
        for o in range(s["off"], s["off"] + s["size"], step):
            if self.is64:
                nm, info, _o, shndx, val, size = struct.unpack(e + "IBBHQQ", d[o:o + 24])
            else:
                nm, val, size, info, _o, shndx = struct.unpack(e + "IIIBBH", d[o:o + 16])
            end = blob.find(b"\0", nm)
            out.append(dict(name=blob[nm:end].decode("latin-1"), value=val,
                            size=size, info=info, shndx=shndx))
        return out


def main():
    path = sys.argv[1]
    ef = Elf(path)
    print("fichier      : %s" % path)
    print("classe       : ELF%d %s" % (32 if not ef.is64 else 64,
                                       "LE" if ef.end == "<" else "BE"))
    print("type         : %s" % ET.get(ef.etype, ef.etype))
    print("machine      : %s" % EM.get(ef.machine, hex(ef.machine)))
    print("entry        : 0x%08X" % ef.entry)
    print("segments     : %d   sections : %d" % (ef.phnum, ef.shnum))
    print()
    print("--- segments")
    for p in ef.segments:
        print("  %-14s off=0x%08X vaddr=0x%08X filesz=0x%08X memsz=0x%08X f=%d"
              % (p["type"], p["off"], p["vaddr"], p["filesz"], p["memsz"], p["flags"]))
    if "--sections" in sys.argv:
        print()
        print("--- sections")
        for s in ef.sections:
            print("  %-22s %-10s addr=0x%08X off=0x%08X size=0x%08X"
                  % (s.get("name", "?"), SHT.get(s["type"], hex(s["type"])),
                     s["addr"], s["off"], s["size"]))
    print()
    print("--- dynamique")
    for tag, val, txt in ef.dynamic():
        print("  %-10s 0x%08X %s" % (tag, val, txt))
    syms = ef.symbols(".symtab")
    dyns = ef.symbols(".dynsym")
    print()
    print("symboles: .symtab=%d  .dynsym=%d" % (len(syms), len(dyns)))


if __name__ == "__main__":
    main()
