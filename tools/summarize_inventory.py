#!/usr/bin/env python3
"""Resume un CSV d'inventaire : par extension et par type detecte.

Usage:
    py -3 tools/summarize_inventory.py <ID> [--dirs] [--type T]
"""
import csv
import os
import sys
from collections import Counter, defaultdict

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = os.path.join(WORK, "analysis", "inventory")


def load(sid):
    with open(os.path.join(INV, sid + ".csv"), encoding="utf-8") as fp:
        return list(csv.DictReader(fp))


def main():
    sid = sys.argv[1]
    rows = load(sid)
    if "--type" in sys.argv:
        want = sys.argv[sys.argv.index("--type") + 1].lower()
        for r in rows:
            if want in r["type"].lower():
                print("%-12s %-60s %s" % (
                    "%.2f Mo" % (int(r["size"]) / 1048576.0), r["path"], r["type"]))
        return

    if "--dirs" in sys.argv:
        agg = defaultdict(lambda: [0, 0])
        for r in rows:
            top = r["path"].split("/")
            key = "/".join(top[:2]) if len(top) > 1 else "(racine)"
            agg[key][0] += 1
            agg[key][1] += int(r["size"])
        print("%-40s %8s %12s" % ("dossier", "fich.", "taille"))
        for k, (n, sz) in sorted(agg.items(), key=lambda kv: -kv[1][1]):
            print("%-40s %8d %9.1f Mo" % (k, n, sz / 1048576.0))
        return

    ext = Counter()
    esz = Counter()
    for r in rows:
        e = os.path.splitext(r["path"])[1].lower() or "(sans ext)"
        ext[e] += 1
        esz[e] += int(r["size"])
    print("=== %s : %d fichiers" % (sid, len(rows)))
    print("%-16s %8s %12s" % ("extension", "nombre", "taille"))
    for e, n in ext.most_common(40):
        print("%-16s %8d %9.1f Mo" % (e, n, esz[e] / 1048576.0))
    print()
    typ = Counter(r["type"] for r in rows if r["type"])
    print("--- types detectes par signature")
    for t, n in typ.most_common(40):
        print("%-40s %6d" % (t, n))


if __name__ == "__main__":
    main()
