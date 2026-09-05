#!/usr/bin/env python3
"""Extrait une section ELF vers un fichier, ou en liste les chaines.

Usage:
    py -3 tools/dump_section.py <elf> <section> --out <fichier>
    py -3 tools/dump_section.py <elf> <section> --strings [minlen]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_elf import Elf  # noqa: E402


def main():
    elf, name = sys.argv[1], sys.argv[2]
    ef = Elf(elf)
    s = ef.sec(name)
    if not s:
        sys.exit("section %s absente" % name)
    blob = ef.data[s["off"]:s["off"] + s["size"]]
    if "--out" in sys.argv:
        dest = sys.argv[sys.argv.index("--out") + 1]
        with open(dest, "wb") as fp:
            fp.write(blob)
        print("%s : 0x%X octets -> %s" % (name, len(blob), dest))
        return
    minlen = 4
    if "--strings" in sys.argv:
        i = sys.argv.index("--strings")
        if i + 1 < len(sys.argv) and sys.argv[i + 1].isdigit():
            minlen = int(sys.argv[i + 1])
    seen = set()
    for m in re.finditer(rb"[\x20-\x7e]{%d,}" % minlen, blob):
        t = m.group().decode("latin-1")
        if t not in seen:
            seen.add(t)
            print(t)


if __name__ == "__main__":
    main()
