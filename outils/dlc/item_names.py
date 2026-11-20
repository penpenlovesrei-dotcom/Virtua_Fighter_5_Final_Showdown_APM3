#!/usr/bin/env python3
"""Read the VF5 (2007) item tables (chritm_tbl.farc -> <code>itm_tbl.bin).

Record layout (0x50 bytes, little-endian), table header: magic, record count, records offset.
  +0x04 name ptr        ("UNKNOWN" = unused slot)
  +0x10 type            (3 = removal entry such as "Bare Chest": no object of its own)
  +0x28 label ptr       ("007 BELT_01", "NO_NAME" for skin tones)
  +0x44 sprite ptr      ("SPR_T_ITMAKI_AKI_P_0101")
  +0x48 code (decimal)  K MMM V III : K=1 object item (99 = skin tone), MMM=objset item
                                     number, V=colour variant, III=record index
usage: item_names.py OUT.json [--lang en]
"""
import argparse
import json
import os
import re
import struct

from sources import VF5_MEDIA
from vf5fs import CHARACTERS, farc_entries, iter_farc_bytes


def cstr(d, off):
    if not 0 < off < len(d):
        return None
    return d[off:d.find(b"\0", off)].decode("utf-8", "replace")


def parse_item_table(d):
    _, count, start = struct.unpack_from("<3I", d, 0)
    records = []
    for k in range(count):
        o = start + k * 0x50
        name = cstr(d, struct.unpack_from("<I", d, o + 4)[0])
        (code,) = struct.unpack_from("<I", d, o + 0x48)
        if code == 0:
            continue
        records.append(dict(
            index=k, name=name, type=struct.unpack_from("<I", d, o + 0x10)[0],
            label=cstr(d, struct.unpack_from("<I", d, o + 0x28)[0]),
            sprite=cstr(d, struct.unpack_from("<I", d, o + 0x44)[0]),
            kind=code // 10000000, model=(code // 10000) % 1000,
            variant=(code // 1000) % 10, id=code % 1000,
        ))
    return records


def table_path(lang):
    if lang == "jp":
        return os.path.join(VF5_MEDIA, "rom", "chritm_tbl.farc")
    return os.path.join(VF5_MEDIA, "lang", lang, "rom", "chritm_tbl.farc")


def load_names(lang="en"):
    """{code: [record, ...]} for every character table."""
    out = {}
    with open(table_path(lang), "rb") as fh:
        data = fh.read()
    for ent, payload in iter_farc_bytes(data):
        m = re.fullmatch(r"(\w{3})itm_tbl\.bin", ent["name"])
        if m:
            out[m.group(1)] = parse_item_table(payload)
    return out


def objset_numbers():
    """{code: set(item numbers)} straight from the VF5 archive headers."""
    folder = os.path.join(VF5_MEDIA, "objset_x36")
    out = {}
    for name in os.listdir(folder):
        m = re.fullmatch(r"(\w{3})itm\.farc", name)
        if not m:
            continue
        with open(os.path.join(folder, name), "rb") as fh:
            head = fh.read(8)
            (hsize,) = struct.unpack(">I", head[4:8])
            fh.seek(0)
            ents = farc_entries(fh.read(8 + hsize))
        out[m.group(1)] = {int(x.group(1)) for e in ents for x in [re.search(r"itm(\d+)_", e["name"])] if x}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--lang", default="en")
    args = ap.parse_args()
    names = load_names(args.lang)
    objsets = objset_numbers()
    bad_index = 0
    print("%-9s %5s %6s %6s %8s %8s" % ("char", "recs", "kind1", "models", "no_obj", "unnamed"))
    for code in sorted(names):
        recs = names[code]
        bad_index += sum(r["id"] != r["index"] for r in recs)
        obj_recs = [r for r in recs if r["kind"] == 1]
        models = {r["model"] for r in obj_recs}
        nums = objsets.get(code, set())
        print("%-9s %5d %6d %6d %8d %8d   kinds=%s" % (
            CHARACTERS.get(code, code), len(recs), len(obj_recs), len(models),
            len(models - nums), len(nums - models), sorted({r["kind"] for r in recs})))
    print("records whose id != index:", bad_index)
    sample = [r for r in names["aki"] if r["kind"] == 1][:12]
    print("aki sample:", [(r["model"], r["variant"], r["name"], r["label"]) for r in sample])
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(names, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
