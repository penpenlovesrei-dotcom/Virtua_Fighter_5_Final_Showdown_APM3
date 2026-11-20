#!/usr/bin/env python3
"""Match VF5 (2007) items against Final Showdown items (base game + DLC), per character.

usage: match_items.py games_inventory.json thumbs.json vf5_item_names_en.json OUT.json

Identity evidence
  same number      item numbers were largely kept between the games
  same stem        internal label stem, e.g. joha_outer_02 (object main names)
Content evidence (what changed)
  geo   share of the VF5 item's significant meshes whose vertex positions are byte-identical
  mesh  share of the VF5 item's significant meshes found with the same name and vertex count
  tex   share of the VF5 item's textures that look the same (8x8 thumbnail difference)
"""
import collections
import json
import re
import sys

MIN_MESH_VERTICES = 32      # smaller meshes (eye planes, quads) are shared by many items
TEX_DIFF_MAX = 8.0          # mean abs RGBA difference (0-255) for "same looking" textures
STEM_RE = re.compile(r"(atam|face|joha|kaha)_([a-z]+)_(\d+)")

STATUSES = ["Identique", "Modifié", "Refait", "Incertain", "Absent du FS"]


def object_labels(item):
    objs = item.get("objects", [])
    prefix = item["item"] + "_"
    primary = [o["name"] for o in objs if "__" in o["name"]] or [o["name"] for o in objs]
    return [(n[len(prefix):] if n.lower().startswith(prefix) else n).split("__", 1)[0] for n in primary]


def stems(labels):
    found = {m.group(0) for lab in labels for m in [STEM_RE.match(lab)] if m}
    return found or set(labels)


def significant_meshes(item):
    meshes = [m for o in item.get("objects", []) for m in o["meshes"]]
    big = [m for m in meshes if m[1] >= MIN_MESH_VERTICES]
    return big or meshes


def _pixels(hexstr):
    b = bytes.fromhex(hexstr)
    return [tuple(b[i:i + 4]) for i in range(0, len(b), 4)]


def _const(px, c):
    return all(p[c] == px[0][c] for p in px)


def _flat(px):
    return all(p[:3] == px[0][:3] for p in px)


def tex_distance(pa, pb):
    """Mean abs difference over the channels both encodings actually use."""
    if all(_const(px, c) for px in (pa, pb) for c in (0, 2)):
        # 2-channel normal maps: x/y live in green/alpha, red/blue are filler (0 or 255)
        pairs = [(a[1], b[1]) for a, b in zip(pa, pb)] + [(a[3], b[3]) for a, b in zip(pa, pb)]
    elif _const(pa, 3) or _const(pb, 3):
        # alpha unused by at least one encoding: compare colour only
        pairs = [(a[c], b[c]) for a, b in zip(pa, pb) for c in range(3)]
    else:
        # alpha used by both: colour premultiplied by alpha (colour under transparent pixels is noise)
        pairs = [(a[c] * a[3] // 255, b[c] * b[3] // 255) for a, b in zip(pa, pb) for c in range(3)]
        pairs += [(a[3], b[3]) for a, b in zip(pa, pb)]
    return sum(abs(x - y) for x, y in pairs) / len(pairs)


def tex_similarity(pa_list, pb_list):
    """Share of A's textures that have a same-looking texture in B (None if A has none)."""
    if not pa_list:
        return None
    if not pb_list:
        return 0.0
    same = sum(min(tex_distance(pa, pb) for pb in pb_list) <= TEX_DIFF_MAX for pa in pa_list)
    return same / len(pa_list)


class Fingerprint:
    def __init__(self, item, thumbs):
        self.item = item
        self.labels = object_labels(item)
        self.stems = stems(self.labels)
        sig = significant_meshes(item)
        # items made only of small meshes (decals, eye planes) share geometry with many others
        self.small_only = not any(m[1] >= MIN_MESH_VERTICES for m in sig)
        self.geo = {m[3] for m in sig if m[3]}
        self.mesh = collections.Counter((m[0], m[1]) for m in sig)
        # flat thumbnails (placeholders, plain colours) are not evidence
        self.tex_px = [p for p in (_pixels(x) for x in (thumbs or []) if x) if not _flat(p)]


def compare(a, b):
    geo = len(a.geo & b.geo) / len(a.geo) if a.geo else 0.0
    mesh = sum((a.mesh & b.mesh).values()) / sum(a.mesh.values()) if a.mesh else 0.0
    tex = tex_similarity(a.tex_px, b.tex_px)
    same_num = a.item["number"] == b.item["number"]
    same_stem = bool(a.stems & b.stems)
    if a.small_only:
        content = (tex or 0) >= 0.5
        exact = geo >= 0.999 and tex is not None and tex >= 0.999
    else:
        content = geo > 0 or mesh >= 0.5 or (tex or 0) >= 0.5
        exact = geo >= 0.999 and (tex is None or tex >= 0.999)
    if same_num and same_stem:
        identity = 3
    elif (same_stem or same_num) and content:
        identity = 2
    elif exact:
        identity = 2
    elif same_stem or content:
        identity = 1
    else:
        identity = 0
    return dict(identity=identity, geo=geo, mesh=mesh, tex=tex, same_num=same_num, same_stem=same_stem)


def describe(c):
    if c["geo"] >= 0.999:
        model = "Identique"
    elif c["mesh"] >= 0.999:
        model = "Mêmes maillages, géométrie retouchée"
    elif c["geo"] > 0 or c["mesh"] > 0:
        model = "Partiellement modifié"
    else:
        model = "Refait"
    if c["tex"] is None:
        textures = "Aucune"
    elif c["tex"] >= 0.999:
        textures = "Identiques"
    elif c["tex"] > 0:
        textures = "En partie identiques"
    else:
        textures = "Différentes"
    if c["identity"] <= 1:
        status = "Incertain"
    elif model == "Identique" and textures in ("Identiques", "Aucune"):
        status = "Identique"
    elif model == "Refait" and textures in ("Différentes", "Aucune"):
        status = "Refait"
    else:
        status = "Modifié"
    return model, textures, status


def main():
    inv_path, thumbs_path, names_path, out_path = sys.argv[1:5]
    items = json.load(open(inv_path, encoding="utf-8"))["items"]
    thumbs = json.load(open(thumbs_path, encoding="utf-8"))
    names = json.load(open(names_path, encoding="utf-8"))

    fp = {(it["game"], it["item"]): Fingerprint(it, thumbs[it["game"]].get(it["item"])) for it in items}
    fs_by_code = collections.defaultdict(list)
    for key, f in fp.items():
        if key[0] != "vf5":
            fs_by_code[f.item["code"]].append(f)
    index = collections.defaultdict(lambda: collections.defaultdict(list))
    for code, fs in fs_by_code.items():
        for f in fs:
            index[code]["n%d" % f.item["number"]].append(f)
            for s in f.stems:
                index[code]["s" + s].append(f)
            for g in f.geo:
                index[code]["g" + g].append(f)
            for mname, verts in f.mesh:
                index[code]["m%s|%d" % (mname, verts)].append(f)

    variants = collections.defaultdict(list)
    for code, recs in names.items():
        for r in sorted(recs, key=lambda r: (r["model"], r["variant"], r["index"])):
            if r["name"] and r["name"] not in ("UNKNOWN", "NO NAME", "NO_NAME") and r.get("type") != 3:
                variants[(code, r["model"])].append(r["name"])

    results, used_fs = [], collections.defaultdict(list)
    for key, a in fp.items():
        if key[0] != "vf5":
            continue
        it, code = a.item, a.item["code"]
        pool = {}
        keys = ["n%d" % it["number"]] + ["s" + s for s in a.stems] + ["g" + g for g in a.geo] + \
               ["m%s|%d" % mv for mv in a.mesh]
        for k in keys:
            for f in index[code].get(k, []):
                pool[(f.item["game"], f.item["item"])] = f
        cands = []
        for fkey, f in pool.items():
            c = compare(a, f)
            if c["identity"] == 0:
                continue
            c.update(game=fkey[0], item=fkey[1], number=f.item["number"], label=", ".join(f.labels))
            c["model"], c["textures"], c["status"] = describe(c)
            cands.append(c)
        cands.sort(key=lambda c: (-c["identity"], -(c["geo"] + c["mesh"] + (c["tex"] or 0)),
                                  not c["same_num"], c["game"] != "fs", c["item"]))
        best = cands[0] if cands else None
        names_list = list(dict.fromkeys(variants.get((code, it["number"]), [])))
        results.append(dict(
            code=code, character=it["character"], item=it["item"], number=it["number"],
            name=names_list[0] if names_list else "", variants=names_list[1:],
            label=", ".join(a.labels), status=best["status"] if best else "Absent du FS",
            best=best, others=[c for c in cands[1:6] if c["identity"] >= 2],
            weak=[c for c in cands[1:6] if c["identity"] == 1],
        ))
        if best and best["identity"] >= 2:
            used_fs[(best["game"], best["item"])].append(it["item"])
            for c in cands[1:]:
                if c["identity"] >= 2 and c["status"] in ("Identique", "Modifié"):
                    used_fs[(c["game"], c["item"])].append(it["item"])

    fs_items = []
    for (game, item), f in sorted(fp.items()):
        if game == "vf5":
            continue
        fs_items.append(dict(game=game, code=f.item["code"], character=f.item["character"], item=item,
                             number=f.item["number"], label=", ".join(f.labels),
                             vf5=sorted(set(used_fs.get((game, item), [])))))

    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(dict(vf5=results, fs=fs_items), fh, ensure_ascii=False, indent=1)

    st = collections.Counter(r["status"] for r in results)
    print("VF5 items:", len(results), {s: st[s] for s in STATUSES})
    print("  named:", sum(bool(r["name"]) for r in results),
          " named & absent:", sum(bool(r["name"]) and r["status"] == "Absent du FS" for r in results))
    print("  best in:", collections.Counter(r["best"]["game"] for r in results if r["best"]),
          " different number:", sum(1 for r in results if r["best"] and not r["best"]["same_num"]))
    print("  model:", collections.Counter(r["best"]["model"] for r in results if r["best"]))
    print("  textures:", collections.Counter(r["best"]["textures"] for r in results if r["best"]))
    print("FS items with a VF5 counterpart:", sum(bool(f["vf5"]) for f in fs_items), "/", len(fs_items))
    for s in STATUSES:
        print("\n--", s)
        for r in [r for r in results if r["status"] == s][:6]:
            b = r["best"]
            print("   %s %-26s %-24s -> %s" % (r["item"], r["label"][:26], r["name"][:24],
                  "%s:%s %s geo=%.2f mesh=%.2f tex=%s id=%d" % (b["game"], b["item"], b["label"][:22], b["geo"], b["mesh"],
                  None if b["tex"] is None else round(b["tex"], 2), b["identity"]) if b else "-"))


if __name__ == "__main__":
    main()
