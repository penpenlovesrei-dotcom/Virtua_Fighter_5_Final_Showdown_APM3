#!/usr/bin/env python3
"""Chaines d'un binaire, avec offset fichier et adresse virtuelle si ELF.

Usage:
    py -3 tools/extract_strings.py <fichier> [--min N] [--grep REGEX] [--out F]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def load_map(path):
    """Renvoie une liste (off, size, vaddr) pour convertir offset -> vaddr."""
    try:
        from scan_elf import Elf
        ef = Elf(path)
        return [(p["off"], p["filesz"], p["vaddr"]) for p in ef.segments
                if p["type"] == "LOAD"], ef.data
    except Exception:
        with open(path, "rb") as fp:
            return [], fp.read()


def to_vaddr(mapping, off):
    for o, sz, va in mapping:
        if o <= off < o + sz:
            return va + (off - o)
    return None


def main():
    path = sys.argv[1]
    minlen = 5
    if "--min" in sys.argv:
        minlen = int(sys.argv[sys.argv.index("--min") + 1])
    pat = None
    if "--grep" in sys.argv:
        pat = re.compile(sys.argv[sys.argv.index("--grep") + 1], re.I)
    out = sys.stdout
    if "--out" in sys.argv:
        out = open(sys.argv[sys.argv.index("--out") + 1], "w", encoding="utf-8")

    mapping, data = load_map(path)
    for m in re.finditer(rb"[\x20-\x7e\t]{%d,}" % minlen, data):
        text = m.group().decode("latin-1")
        if pat and not pat.search(text):
            continue
        va = to_vaddr(mapping, m.start())
        addr = "0x%08X" % va if va is not None else "-" * 10
        out.write("%s  off=0x%08X  %s\n" % (addr, m.start(), text))
    if out is not sys.stdout:
        out.close()


if __name__ == "__main__":
    main()
