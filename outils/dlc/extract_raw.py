#!/usr/bin/env python3
"""Extract the raw item files (_obj.bin / _tex.bin) of one game, then verify them.

usage: extract_raw.py vf5|fs|dlc [--workers N]
Layout: <game EXTRACTION dir>/<Character>/<item>/<item>_obj.bin, <item>_tex.bin
        shared itmcmn archive -> <EXTRACTION>/_Commun/itmcmn/
Files already present with the right size are not rewritten.
"""
import argparse
import os
import re
import sys
import time
from multiprocessing import Pool

from sources import GAMES, archives
from vf5fs import CHARACTERS, farc_entries, iter_farc_bytes

ITEM_RE = re.compile(r"(\w{3}itm\d+)_(?:obj|tex)\.bin")


def target(outdir, code, entry_name):
    m = ITEM_RE.fullmatch(entry_name)
    item = m.group(1) if m else entry_name.rsplit("_", 1)[0]
    char = "_Commun" if code == "cmn" else CHARACTERS.get(code, code)
    return os.path.join(outdir, char, item, entry_name)


def extract_one(job):
    game, archive_name = job
    outdir = GAMES[game]["extract_dir"]
    code, _, loader = next(a for a in archives(game) if a[1] == archive_name)
    written = kept = 0
    total = 0
    for ent, data in iter_farc_bytes(loader()):
        dst = target(outdir, code, ent["name"])
        total += len(data)
        if os.path.exists(dst) and os.path.getsize(dst) == len(data):
            kept += 1
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as fh:
            fh.write(data)
        written += 1
    return archive_name, written, kept, total


def verify(game):
    """Every archive entry must exist on disk with its unpacked size."""
    outdir = GAMES[game]["extract_dir"]
    expected, bad = 0, []
    for code, name, loader in archives(game):
        for ent in farc_entries(loader()):
            expected += 1
            dst = target(outdir, code, ent["name"])
            if not os.path.exists(dst) or os.path.getsize(dst) != ent["usize"]:
                bad.append(dst)
    return expected, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("game", choices=sorted(GAMES))
    ap.add_argument("--workers", type=int, default=min(os.cpu_count() or 1, 2))
    args = ap.parse_args()

    jobs = [(args.game, name) for _, name, _ in archives(args.game)]
    print("%s -> %s (%d archives)" % (GAMES[args.game]["label"], GAMES[args.game]["extract_dir"], len(jobs)), flush=True)
    t0 = time.time()
    files = size = 0
    with Pool(args.workers) as pool:
        for name, written, kept, total in pool.imap_unordered(extract_one, jobs):
            files += written + kept
            size += total
            print("  %-20s written=%4d kept=%4d  [%.0fs]" % (name, written, kept, time.time() - t0), flush=True)
    print("extracted files=%d bytes=%d in %.0fs" % (files, size, time.time() - t0), flush=True)

    expected, bad = verify(args.game)
    print("verification: expected=%d missing_or_wrong_size=%d" % (expected, len(bad)))
    for b in bad[:20]:
        print("  BAD", b)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
