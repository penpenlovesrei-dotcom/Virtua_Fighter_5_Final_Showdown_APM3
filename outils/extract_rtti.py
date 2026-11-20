#!/usr/bin/env python3
"""Extrait les noms de types Itanium C++ ABI (typeinfo name) d'un ELF.

Un typeinfo name est une chaine mangled : 12TaskSelChara, N3prj3anyE, P4Task...
On ne garde que ce qui se demangle en un nom de type plausible.

Usage:
    py -3 tools/extract_rtti.py <elf> [--out F]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_elf import Elf  # noqa: E402

# Une composante <length><identifier>, eventuellement enchainee dans N...E
COMP = r"(?:[0-9]+[A-Za-z_][A-Za-z0-9_]*)"
TOKEN = re.compile(
    (r"(?:N(?:%s)+E|%s)" % (COMP, COMP)).encode()
)


def demangle_name(tok):
    """Demangle sommaire d'un nom de type (pas d'une fonction)."""
    s = tok
    nested = s.startswith("N") and s.endswith("E")
    if nested:
        s = s[1:-1]
    parts = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j].isdigit():
            j += 1
        if j == i:
            return None
        n = int(s[i:j])
        if n == 0 or j + n > len(s):
            return None
        parts.append(s[j:j + n])
        i = j + n
    if not parts:
        return None
    if not nested and len(parts) != 1:
        return None
    return "::".join(parts)


def main():
    path = sys.argv[1]
    ef = Elf(path)
    seen = {}
    for sname in (".rodata", ".data", "PSFD00"):
        sec = ef.sec(sname)
        if not sec or sec["type"] == 8:
            continue
        base_off, base_va = sec["off"], sec["addr"]
        blob = ef.data[base_off:base_off + sec["size"]]
        # Un typeinfo name est une chaine C terminee par NUL et precedee d'un NUL.
        for m in re.finditer(rb"\x00([0-9N][\x21-\x7e]{2,200})\x00", blob):
            tok = m.group(1).decode("latin-1")
            if not TOKEN.fullmatch(tok.encode()):
                continue
            name = demangle_name(tok)
            if not name or len(name) < 4:
                continue
            va = base_va + m.start(1)
            seen.setdefault(name, (va, tok, sname))
    out = sys.stdout
    if "--out" in sys.argv:
        out = open(sys.argv[sys.argv.index("--out") + 1], "w", encoding="utf-8")
    out.write("# %d types RTTI dans %s\n" % (len(seen), os.path.basename(path)))
    out.write("# vaddr_nom  mangled  section  nom\n")
    for name in sorted(seen):
        va, tok, sname = seen[name]
        out.write("0x%08X  %-40s %-10s %s\n" % (va, tok, sname, name))
    if out is not sys.stdout:
        out.close()
        print("%d types -> %s" % (len(seen), sys.argv[sys.argv.index("--out") + 1]))


if __name__ == "__main__":
    main()
