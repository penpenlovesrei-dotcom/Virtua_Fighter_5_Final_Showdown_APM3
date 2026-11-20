#!/usr/bin/env python3
"""8x8 RGBA thumbnail of every texture (first face) of the extracted items of all games.

usage: thumbs_games.py OUT.json
Thumbnails survive re-encoding: the same image compressed twice gives nearly the same
thumbnail, while hashes of the compressed data differ.
"""
import json
import os
import sys
import time
from multiprocessing import Pool

from PIL import Image

from sources import GAMES
from vf5fs import decode_mip, parse_txp


def thumbs_for_dir(job):
    game, char_dir = job
    out = {}
    for item in sorted(os.listdir(char_dir)):
        path = os.path.join(char_dir, item, item + "_tex.bin")
        if not os.path.exists(path):
            continue
        t = open(path, "rb").read()
        row = []
        try:
            textures = parse_txp(t)
        except Exception:
            out[item] = None
            continue
        for tex in textures:
            mips = tex["subs"][:tex["mips"]]
            sub = next((s for s in mips if max(s["width"], s["height"]) <= 32), mips[-1])
            try:
                im = decode_mip(t, sub, upright=False).convert("RGBA").resize((8, 8), Image.BOX)
                row.append(im.tobytes().hex())
            except Exception:
                row.append(None)
        out[item] = row
    return game, out


def main():
    out_path = sys.argv[1]
    games = sys.argv[2].split(",") if len(sys.argv) > 2 else list(GAMES)
    jobs = []
    for game in games:
        root = GAMES[game]["extract_dir"]
        for name in sorted(os.listdir(root)):
            if not name.startswith("_") and os.path.isdir(os.path.join(root, name)):
                jobs.append((game, os.path.join(root, name)))
    # recompute only the requested games, keep the others from a previous run
    result = json.load(open(out_path, encoding="utf-8")) if os.path.exists(out_path) else {}
    for g in GAMES:
        result.setdefault(g, {})
    for g in games:
        result[g] = {}
    t0 = time.time()
    with Pool(2) as pool:
        for game, out in pool.imap_unordered(thumbs_for_dir, jobs):
            result[game].update(out)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh)
    for g in GAMES:
        n = sum(len(v) for v in result[g].values() if v)
        bad = sum(1 for v in result[g].values() if v for x in v if x is None)
        print("%-4s items=%5d textures=%6d undecodable=%d" % (g, len(result[g]), n, bad))
    print("%.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
