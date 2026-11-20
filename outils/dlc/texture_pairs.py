"""Pair the textures of matched VF5 / Final Showdown items by appearance (8x8 thumbnails)."""
from match_items import TEX_DIFF_MAX, _const, _flat, _pixels, tex_distance

NORMAL_MAP_FORMAT = "3552088"   # VF5 'X36' uncompressed 16-bit normal maps (see vf5fs.TEX_FORMATS)


def texture_pairs(matches, items, thumbs, statuses=("Identique", "Modifié")):
    """Yield, for each VF5 texture, the same-looking texture of the matched FS item."""
    inv = {(it["game"], it["item"]): it for it in items}
    for r in matches["vf5"]:
        b = r["best"]
        if not b or r["status"] not in statuses:
            continue
        fs_px = {j: _pixels(x) for j, x in enumerate(thumbs[b["game"]].get(b["item"]) or []) if x}
        fs_px = {j: p for j, p in fs_px.items() if not _flat(p)}
        if not fs_px:
            continue
        vf5_tex = inv[("vf5", r["item"])].get("textures", [])
        fs_tex = inv[(b["game"], b["item"])].get("textures", [])
        for i, x in enumerate(thumbs["vf5"].get(r["item"]) or []):
            if not x:
                continue
            pa = _pixels(x)
            if _flat(pa):
                continue
            dist, j = min((tex_distance(pa, p), j) for j, p in fs_px.items())
            if dist <= TEX_DIFF_MAX:
                yield dict(vf5=r, fs=b, i=i, j=j, vf5_tex=vf5_tex[i], fs_tex=fs_tex[j], distance=dist,
                           normal_map=vf5_tex[i][2] == NORMAL_MAP_FORMAT or (_const(pa, 0) and _const(pa, 2)))


def higher_res_textures(matches, items, thumbs):
    """Texture pairs where the VF5 image has more pixels than its FS counterpart."""
    return [p for p in texture_pairs(matches, items, thumbs)
            if p["vf5_tex"][0] * p["vf5_tex"][1] > p["fs_tex"][0] * p["fs_tex"][1]]
