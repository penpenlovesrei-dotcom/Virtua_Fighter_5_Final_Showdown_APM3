#!/usr/bin/env python3
"""Extract every VF5FS DLC item: raw obj/tex .bin files plus one PNG per texture.

usage: extract.py PACKAGE OUTDIR [--only aki,aoi] [--limit N] [--workers N]
Layout: OUTDIR/<Character>/<item>/<item>_obj.bin, <item>_tex.bin, <item>_texNN.png
Re-running skips PNGs that already exist.
"""
import argparse
import os
import re
import sys
import time
from multiprocessing import Pool

from stfs import Stfs
from vf5fs import CHARACTERS, decode_mip, iter_farc, parse_txp

ITEM_RE = re.compile(r"(\w{3}itm\d+)_(obj|tex)\.bin")


def extract_farc(job):
    pkg, outdir, farc_name, limit, png_enabled = job
    s = Stfs(pkg)
    fe = next(e for e in s.file_table() if e["name"] == farc_name)
    code = farc_name[:3]
    char_dir = os.path.join(outdir, CHARACTERS.get(code, code))
    stats = dict(farc=farc_name, bins=0, pngs=0, skipped=0, bytes=0, errors=[])
    seen = set()
    for ent, data in iter_farc(s, fe):
        m = ITEM_RE.fullmatch(ent["name"])
        item = m.group(1) if m else os.path.splitext(ent["name"])[0]
        if limit and item not in seen and len(seen) >= limit:
            break
        seen.add(item)
        item_dir = os.path.join(char_dir, item)
        os.makedirs(item_dir, exist_ok=True)
        dst = os.path.join(item_dir, ent["name"])
        if not (os.path.exists(dst) and os.path.getsize(dst) == len(data)):
            with open(dst, "wb") as fh:
                fh.write(data)
        stats["bins"] += 1
        stats["bytes"] += len(data)
        if not png_enabled or not (m and m.group(2) == "tex"):
            continue
        try:
            textures = parse_txp(data)
        except Exception as ex:
            stats["errors"].append((ent["name"], repr(ex)))
            continue
        for i, tex in enumerate(textures):
            for a in range(tex["array"]):
                suffix = "_face%d" % a if tex["array"] > 1 else ""
                png = os.path.join(item_dir, "%s_tex%02d%s.png" % (item, i, suffix))
                if os.path.exists(png):
                    stats["skipped"] += 1
                    continue
                try:
                    decode_mip(data, tex["subs"][a * tex["mips"]]).save(png, compress_level=4)
                    stats["pngs"] += 1
                except Exception as ex:
                    stats["errors"].append(("%s tex%02d%s" % (item, i, suffix), repr(ex)))
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("package")
    ap.add_argument("outdir")
    ap.add_argument("--only", default="")
    ap.add_argument("--limit", type=int, default=0, help="max items per character (test runs)")
    ap.add_argument("--workers", type=int, default=min(os.cpu_count() or 1, 6))
    ap.add_argument("--no-png", action="store_true", help="raw .bin files only")
    args = ap.parse_args()

    only = {c for c in args.only.split(",") if c}
    farcs = [e["name"] for e in Stfs(args.package).file_table()
             if not e["is_dir"] and e["name"].endswith(".farc") and (not only or e["name"][:3] in only)]
    # biggest archives first so the pool stays busy
    jobs = [(args.package, args.outdir, f, args.limit, not args.no_png) for f in farcs]
    t0 = time.time()
    totals = dict(bins=0, pngs=0, skipped=0, bytes=0)
    errors = []
    with Pool(args.workers) as pool:
        for st in pool.imap_unordered(extract_farc, jobs):
            for k in totals:
                totals[k] += st[k]
            errors += st["errors"]
            print("%-22s bins=%4d pngs=%5d skipped=%5d errors=%d  [%.0fs]" % (
                st["farc"], st["bins"], st["pngs"], st["skipped"], len(st["errors"]), time.time() - t0), flush=True)
    print("TOTAL bins=%(bins)d pngs=%(pngs)d skipped=%(skipped)d raw_bytes=%(bytes)d" % totals,
          "errors=%d time=%.0fs" % (len(errors), time.time() - t0))
    for e in errors[:30]:
        print("  ERR", e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
