#!/usr/bin/env python3
"""Construit la matrice imports du jeu -> bibliotheque fournisseur.

Lit les symboles indefinis de l'executable et les symboles definis de chaque .so
donne, puis attribue chaque import a la premiere bibliotheque qui l'exporte.

Usage:
    py -3 tools/api_matrix.py <exe> <lib.so> [lib.so ...] [--out F]
"""
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_elf import Elf  # noqa: E402

STT = {0: "NOTYPE", 1: "OBJECT", 2: "FUNC", 3: "SECTION", 4: "FILE"}


def dynsyms(path):
    ef = Elf(path)
    undef, defined = [], {}
    for s in ef.symbols(".dynsym"):
        if not s["name"]:
            continue
        typ = STT.get(s["info"] & 0xF, "?")
        if s["shndx"] == 0:
            undef.append((s["name"], typ))
        else:
            defined[s["name"]] = typ
    return undef, defined, ef


def main():
    exe = sys.argv[1]
    rest = sys.argv[2:]
    if "--out" in rest:
        i = rest.index("--out")
        rest = rest[:i] + rest[i + 2:]
    libs = [a for a in rest if not a.startswith("--")]
    undef, _d, ef = dynsyms(exe)
    needed = [t for tag, _v, t in ef.dynamic() if tag == "NEEDED"]

    provider = {}
    for lib in libs:
        try:
            _u, defined, _e = dynsyms(lib)
        except Exception as exc:
            print("!! %s : %s" % (lib, exc), file=sys.stderr)
            continue
        base = os.path.basename(lib)
        for name in defined:
            provider.setdefault(name, base)

    groups = defaultdict(list)
    for name, typ in undef:
        groups[provider.get(name, "(non resolu localement)")].append((name, typ))

    out = sys.stdout
    if "--out" in sys.argv:
        out = open(sys.argv[sys.argv.index("--out") + 1], "w", encoding="utf-8")

    out.write("# Matrice API : %s\n\n" % os.path.basename(exe))
    out.write("DT_NEEDED declares (%d) :\n" % len(needed))
    for n in needed:
        out.write("  - %s\n" % n)
    out.write("\nImports indefinis : %d\n\n" % len(undef))
    for lib in sorted(groups, key=lambda k: (k.startswith("("), k)):
        syms = sorted(groups[lib])
        out.write("## %s  (%d symboles)\n" % (lib, len(syms)))
        for name, typ in syms:
            out.write("  %-6s %s\n" % (typ, name))
        out.write("\n")
    if out is not sys.stdout:
        out.close()
        print("-> %s" % sys.argv[sys.argv.index("--out") + 1])


if __name__ == "__main__":
    main()
