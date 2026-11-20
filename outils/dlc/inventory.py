#!/usr/bin/env python3
"""Scan every item of the VF5FS DLC package and dump its metadata to JSON.

usage: inventory.py PACKAGE OUT.json
"""
import collections
import json
import re
import sys
import time

from stfs import Stfs
from vf5fs import CHARACTERS, TEX_FORMATS, iter_farc, parse_objset, parse_txp

ITEM_RE = re.compile(r"(\w{3})itm(\d+)_(obj|tex)\.bin")


def split_object_name(item, name):
    """'akiitm041_atam_atama_05__divskn' -> ('atam', 'atama_05')."""
    rest = name[len(item) + 1:] if name.lower().startswith(item + "_") else name
    rest = rest.split("__", 1)[0]
    slot, _, label = rest.partition("_")
    return slot, label


def main():
    pkg, out = sys.argv[1], sys.argv[2]
    s = Stfs(pkg)
    items, textures, errors = [], [], []
    t0 = time.time()
    for fe in s.file_table():
        if fe["is_dir"] or not fe["name"].endswith(".farc"):
            continue
        code = fe["name"][:3]
        per_item = collections.defaultdict(dict)
        for ent, data in iter_farc(s, fe):
            m = ITEM_RE.fullmatch(ent["name"])
            if not m:
                errors.append((fe["name"], ent["name"], "unexpected name"))
                continue
            item, kind = "%sitm%s" % (m.group(1), m.group(2)), m.group(3)
            rec = per_item[item]
            rec["number"] = int(m.group(2))
            rec[kind + "_csize"], rec[kind + "_usize"] = ent["csize"], ent["usize"]
            try:
                if kind == "obj":
                    rec["objset"] = parse_objset(data)
                else:
                    rec["txp"] = [
                        dict(cube=t["cube"], mips=t["mips"], array=t["array"],
                             width=t["subs"][0]["width"], height=t["subs"][0]["height"],
                             format=TEX_FORMATS.get(t["subs"][0]["format"], str(t["subs"][0]["format"])))
                        for t in parse_txp(data)
                    ]
            except Exception as ex:  # keep going, report at the end
                errors.append((fe["name"], ent["name"], repr(ex)))
        for item, rec in sorted(per_item.items(), key=lambda kv: kv[1]["number"]):
            objset = rec.get("objset", {"objects": [], "texture_ids": []})
            txp = rec.get("txp", [])
            objs = objset["objects"]
            slots = [split_object_name(item, o["name"]) for o in objs]
            items.append(dict(
                character=CHARACTERS.get(code, code), code=code, item=item, number=rec["number"],
                objects=[o["name"] for o in objs],
                slot=", ".join(dict.fromkeys(sl for sl, _ in slots)),
                label=", ".join(lb for _, lb in slots),
                meshes=[mm["name"] for o in objs for mm in o["meshes"]],
                submeshes=sum(mm["submeshes"] for o in objs for mm in o["meshes"]),
                vertices=sum(mm["vertices"] for o in objs for mm in o["meshes"]),
                materials=[mt["name"] for o in objs for mt in o["materials"]],
                shaders=sorted({mt["shader"] for o in objs for mt in o["materials"]}),
                skinned=any(o["skinned"] for o in objs),
                texture_ids=objset["texture_ids"],
                texture_count=len(txp),
                max_width=max((t["width"] for t in txp), default=0),
                max_height=max((t["height"] for t in txp), default=0),
                formats=sorted({t["format"] for t in txp}),
                obj_csize=rec.get("obj_csize", 0), obj_usize=rec.get("obj_usize", 0),
                tex_csize=rec.get("tex_csize", 0), tex_usize=rec.get("tex_usize", 0),
            ))
            for i, t in enumerate(txp):
                tid = objset["texture_ids"][i] if i < len(objset["texture_ids"]) else None
                textures.append(dict(character=CHARACTERS.get(code, code), item=item, index=i,
                                     texture_id=tid, **t))
        print("%-20s %4d items  %.1fs" % (fe["name"], len(per_item), time.time() - t0), flush=True)

    with open(out, "w", encoding="utf-8") as fh:
        json.dump(dict(items=items, textures=textures, errors=errors), fh, ensure_ascii=False)

    print("items:", len(items), "textures:", len(textures), "errors:", len(errors))
    for e in errors[:20]:
        print("  ERR", e)
    slots = collections.Counter(i["slot"] for i in items)
    examples = collections.defaultdict(list)
    for i in items:
        if len(examples[i["slot"]]) < 4:
            examples[i["slot"]].append(i["label"])
    print("\nslots:")
    for sl, n in slots.most_common():
        print("  %-12s %5d  e.g. %s" % (sl, n, examples[sl]))
    print("formats:", collections.Counter(t["format"] for t in textures))
    print("cube maps:", sum(t["cube"] for t in textures), "arrays>1:", sum(t["array"] > 1 for t in textures))
    print("shaders:", collections.Counter(sh for i in items for sh in i["shaders"]))
    print("multi-object items:", sum(len(i["objects"]) > 1 for i in items),
          "no-texture items:", sum(i["texture_count"] == 0 for i in items))


if __name__ == "__main__":
    main()
