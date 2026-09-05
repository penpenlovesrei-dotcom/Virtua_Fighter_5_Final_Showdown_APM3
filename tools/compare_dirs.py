#!/usr/bin/env python3
"""Compare N repertoires par nom de fichier, avec SHA-256 complet.

Usage:
    py -3 tools/compare_dirs.py ETIQ=CHEMIN [ETIQ=CHEMIN ...] [--only-diff] [--csv F]
"""
import csv
import hashlib
import os
import sys


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for blk in iter(lambda: fp.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def index(root):
    out = {}
    for dp, _dn, fns in os.walk(root):
        for fn in fns:
            full = os.path.join(dp, fn)
            out[fn] = (os.path.getsize(full), sha(full))
    return out


def main():
    labels, idx = [], {}
    csv_out = None
    args = sys.argv[1:]
    for a in args:
        if "=" in a and not a.startswith("--"):
            lab, path = a.split("=", 1)
            labels.append(lab)
            idx[lab] = index(path)
    if "--csv" in args:
        csv_out = args[args.index("--csv") + 1]

    names = sorted(set().union(*[set(idx[l]) for l in labels]))
    rows = []
    width = max(len(n) for n in names) + 2
    head = "%-*s %s" % (width, "fichier", "  ".join("%-10s" % l for l in labels))
    print(head)
    print("-" * len(head))
    for n in names:
        digests = []
        cells = []
        for l in labels:
            e = idx[l].get(n)
            if not e:
                cells.append("-")
                digests.append(None)
            else:
                digests.append(e[1])
                cells.append("")
        # Groupe les digests identiques sous une lettre A, B, C...
        seen, letter = {}, ord("A")
        for i, d in enumerate(digests):
            if d is None:
                continue
            if d not in seen:
                seen[d] = chr(letter)
                letter += 1
            cells[i] = seen[d]
        uniq = len(seen)
        if "--only-diff" in args and uniq <= 1:
            continue
        print("%-*s %s" % (width, n, "  ".join("%-10s" % c for c in cells)))
        rows.append([n] + cells + [uniq])
    if csv_out:
        with open(csv_out, "w", newline="", encoding="utf-8") as fp:
            w = csv.writer(fp)
            w.writerow(["file"] + labels + ["variants"])
            w.writerows(rows)
        print("\n-> %s" % csv_out)
    print("\nMeme lettre = octets identiques. '-' = absent.")


if __name__ == "__main__":
    main()
