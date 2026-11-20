#!/usr/bin/env python3
"""Convertit en UTF-8 les CSV japonais du jeu (Shift-JIS / CP932).

Les tables d'origine sont des exports de tableur en CP932. On les recopie en
UTF-8 sans rien changer d'autre, pour qu'elles soient lisibles et grepables.

Usage:
    py -3 tools/convert_csv.py <racine> <destination>
"""
import os
import sys

ENCODINGS = ("cp932", "utf-8-sig", "utf-8", "latin-1")


def decode(raw):
    for enc in ENCODINGS:
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", "replace"), "latin-1(replace)"


def main():
    root, dest = sys.argv[1], sys.argv[2]
    stats = {}
    n = 0
    for dp, _dn, fns in os.walk(root):
        for fn in fns:
            if not fn.lower().endswith((".csv", ".txt")):
                continue
            src = os.path.join(dp, fn)
            with open(src, "rb") as fp:
                raw = fp.read()
            text, enc = decode(raw)
            stats[enc] = stats.get(enc, 0) + 1
            out = os.path.join(dest, os.path.relpath(src, root))
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8", newline="") as fp:
                fp.write(text)
            n += 1
    print("%d fichiers -> %s" % (n, dest))
    for enc, c in sorted(stats.items(), key=lambda kv: -kv[1]):
        print("  %-18s %d" % (enc, c))


if __name__ == "__main__":
    main()
