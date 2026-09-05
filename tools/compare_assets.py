#!/usr/bin/env python3
"""Compare deux inventaires par nom de fichier (basename) : identique / different / absent.

Usage:
    py -3 tools/compare_assets.py <IDa> <IDb> [--filter SUBSTR] [--only-common]
"""
import csv
import os
import sys
from collections import defaultdict

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = os.path.join(WORK, "analysis", "inventory")


def load(sid, filt):
    idx = defaultdict(list)
    with open(os.path.join(INV, sid + ".csv"), encoding="utf-8") as fp:
        for r in csv.DictReader(fp):
            if filt and filt not in r["path"]:
                continue
            idx[os.path.basename(r["path"])].append(r)
    return idx


def main():
    a, b = sys.argv[1], sys.argv[2]
    filt = None
    if "--filter" in sys.argv:
        filt = sys.argv[sys.argv.index("--filter") + 1]
    ia, ib = load(a, filt), load(b, filt)
    same = diff = 0
    names = sorted(set(ia) | set(ib))
    print("%-30s %-12s %-12s %s" % ("fichier", a, b, "verdict"))
    for n in names:
        ra, rb = ia.get(n), ib.get(n)
        if not ra or not rb:
            if "--only-common" in sys.argv:
                continue
            print("%-30s %-12s %-12s ABSENT" % (
                n, len(ra or []), len(rb or [])))
            continue
        # On compare le premier exemplaire de chaque cote.
        va, vb = ra[0], rb[0]
        if va["hash_mode"] == vb["hash_mode"] == "FULL" and va["sha256"] == vb["sha256"]:
            same += 1
            verdict = "IDENTIQUE"
        else:
            diff += 1
            verdict = "DIFFERENT (%s o vs %s o)" % (va["size"], vb["size"])
        print("%-30s %-12s %-12s %s" % (n, va["size"], vb["size"], verdict))
    print()
    print("identiques=%d differents=%d" % (same, diff))


if __name__ == "__main__":
    main()
