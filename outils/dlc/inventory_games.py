#!/usr/bin/env python3
"""Fingerprint every item of VF5 (2007), FS base game and FS DLC for cross-game matching.

usage: inventory_games.py OUT.json [--games vf5,fs,dlc]

Per item: object/mesh/material names, vertex counts, a hash of each mesh's vertex
positions, and a hash of each texture's full-resolution image data (all faces).
"""
import argparse
import hashlib
import json
import math
import re
import struct
import time

from sources import GAMES, archives
from vf5fs import CHARACTERS, TEX_FORMATS, iter_farc_bytes, parse_objset, parse_txp

ITEM_RE = re.compile(r"(\w{3})itm(\d+)_(obj|tex)\.bin")


def position_hash(d, obj_off, mesh_off, nvert):
    """Hash the position stream of a mesh (first attribute offset); None if not plausible."""
    (pos,) = struct.unpack_from("<I", d, mesh_off + 0x28)
    for start in (pos, obj_off + pos):
        end = start + 12 * nvert
        if not pos or nvert == 0 or end > len(d):
            continue
        floats = struct.unpack_from("<%df" % (3 * nvert), d, start)
        if all(math.isfinite(f) and abs(f) < 100 for f in floats) and any(floats):
            return hashlib.sha1(d[start:end]).hexdigest()[:16]
    return None


def fingerprint_obj(d):
    info = parse_objset(d)
    ver, nobj, _, objs_off = struct.unpack_from("<4I", d, 0)
    obj_offs = struct.unpack_from("<%dI" % nobj, d, objs_off)
    objects = []
    for o, op in zip(info["objects"], obj_offs):
        (nmesh, meshes_off) = struct.unpack_from("<II", d, op + 0x18)
        meshes = []
        for i, m in enumerate(o["meshes"]):
            mp = op + meshes_off + i * 0xD8
            meshes.append([m["name"], m["vertices"], m["submeshes"], position_hash(d, op, mp, m["vertices"])])
        objects.append(dict(name=o["name"], skinned=o["skinned"], meshes=meshes,
                            materials=[[mt["shader"], mt["name"]] for mt in o["materials"]]))
    return dict(objects=objects, texture_ids=info["texture_ids"])


def fingerprint_tex(t):
    out = []
    for tex in parse_txp(t):
        h = hashlib.sha1()
        for a in range(tex["array"]):
            sub = tex["subs"][a * tex["mips"]]
            h.update(t[sub["data"]:sub["data"] + sub["size"]])
        s0 = tex["subs"][0]
        out.append([s0["width"], s0["height"], TEX_FORMATS.get(s0["format"], str(s0["format"])),
                    tex["array"], h.hexdigest()[:16]])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--games", default="vf5,fs,dlc")
    args = ap.parse_args()

    items, errors = [], []
    t0 = time.time()
    for game in args.games.split(","):
        for code, name, loader in archives(game):
            if code == "cmn":
                continue
            per_item = {}
            for ent, data in iter_farc_bytes(loader()):
                m = ITEM_RE.fullmatch(ent["name"])
                if not m:
                    errors.append([game, name, ent["name"], "unexpected entry"])
                    continue
                key = "%sitm%s" % (m.group(1), m.group(2))
                rec = per_item.setdefault(key, dict(
                    game=game, code=code, character=CHARACTERS.get(code, code), item=key,
                    number=int(m.group(2))))
                kind = m.group(3)
                rec[kind + "_size"] = len(data)
                rec[kind + "_sha1"] = hashlib.sha1(data).hexdigest()[:16]
                try:
                    if kind == "obj":
                        rec.update(fingerprint_obj(data))
                    else:
                        rec["textures"] = fingerprint_tex(data)
                except Exception as ex:
                    errors.append([game, name, ent["name"], repr(ex)])
            items += sorted(per_item.values(), key=lambda r: r["number"])
            print("%-4s %-20s %4d items  [%.0fs]" % (game, name, len(per_item), time.time() - t0), flush=True)

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(dict(items=items, errors=errors), fh, ensure_ascii=False)
    no_pos = sum(1 for it in items for o in it.get("objects", []) for m in o["meshes"] if m[3] is None)
    all_mesh = sum(1 for it in items for o in it.get("objects", []) for m in o["meshes"])
    print("items:", len(items), "errors:", len(errors), "meshes without position hash: %d/%d" % (no_pos, all_mesh))
    for e in errors[:20]:
        print("  ERR", e)


if __name__ == "__main__":
    main()
