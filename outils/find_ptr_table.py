#!/usr/bin/env python3
"""Retrouve les tables de pointeurs vers chaines dans un ELF 32 bits.

Sert a remettre en ordre un pool de litteraux que le compilateur a deduplique
et reordonne : la table de pointeurs, elle, garde l'ordre d'origine.

Usage:
    py -3 tools/find_ptr_table.py <elf> --near 0x08A3A612 [--min 4]
    py -3 tools/find_ptr_table.py <elf> --at 0x08BA1234 --count 32
"""
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_elf import Elf  # noqa: E402


def build_strings(ef):
    """Index vaddr -> chaine, pour toutes les chaines imprimables des sections."""
    out = {}
    for sec in ef.sections:
        if sec["type"] == 8 or not sec["addr"]:      # NOBITS ou pas mappee
            continue
        blob = ef.data[sec["off"]:sec["off"] + sec["size"]]
        for m in re.finditer(rb"[\x20-\x7e]{2,200}\x00", blob):
            out[sec["addr"] + m.start()] = m.group()[:-1].decode("latin-1")
    return out


def vaddr_to_off(ef, va):
    for p in ef.segments:
        if p["type"] == "LOAD" and p["vaddr"] <= va < p["vaddr"] + p["filesz"]:
            return p["off"] + (va - p["vaddr"])
    return None


def scan_tables(ef, strings, targets, minlen):
    """Cherche les suites de >= minlen dwords pointant tous vers des chaines."""
    found = []
    for p in ef.segments:
        if p["type"] != "LOAD":
            continue
        base_off, base_va, size = p["off"], p["vaddr"], p["filesz"]
        data = ef.data[base_off:base_off + size]
        run_start = None
        run = []
        for i in range(0, len(data) - 4, 4):
            val = struct.unpack("<I", data[i:i + 4])[0]
            if val in strings:
                if run_start is None:
                    run_start = i
                run.append(val)
            else:
                if run_start is not None and len(run) >= minlen:
                    found.append((base_va + run_start, list(run)))
                run_start, run = None, []
        if run_start is not None and len(run) >= minlen:
            found.append((base_va + run_start, list(run)))
    if targets:
        found = [f for f in found if any(t in f[1] for t in targets)]
    return found


def main():
    ef = Elf(sys.argv[1])
    strings = build_strings(ef)
    minlen = 4
    if "--min" in sys.argv:
        minlen = int(sys.argv[sys.argv.index("--min") + 1])

    if "--at" in sys.argv:
        va = int(sys.argv[sys.argv.index("--at") + 1], 0)
        n = int(sys.argv[sys.argv.index("--count") + 1])
        off = vaddr_to_off(ef, va)
        for i in range(n):
            val = struct.unpack("<I", ef.data[off + 4 * i:off + 4 * i + 4])[0]
            print("[%3d] 0x%08X  %s" % (i, val, strings.get(val, "")))
        return

    targets = []
    if "--near" in sys.argv:
        i = sys.argv.index("--near")
        for a in sys.argv[i + 1:]:
            if a.startswith("--"):
                break
            targets.append(int(a, 0))

    for va, run in scan_tables(ef, strings, targets, minlen):
        print("=== table a 0x%08X, %d entrees" % (va, len(run)))
        for i, val in enumerate(run):
            print("  [%3d] 0x%08X  %s" % (i, val, strings.get(val, "")))
        print()


if __name__ == "__main__":
    main()
