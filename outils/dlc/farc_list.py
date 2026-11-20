#!/usr/bin/env python3
"""List the table of contents of every FArC archive inside an STFS package."""
import json
import struct
import sys

from stfs import Stfs


def read_prefix(s, e, n):
    buf = bytearray()
    for chunk in s.iter_file(e):
        buf += chunk
        if len(buf) >= n:
            break
    return bytes(buf[:n])


def parse_farc(head):
    magic = head[:4]
    (hsize,) = struct.unpack(">I", head[4:8])
    end = 8 + hsize
    pos = 12 if magic in (b"FArC", b"FArc") else 8
    out = []
    while pos < end:
        z = head.index(b"\x00", pos)
        name = head[pos:z].decode("ascii", "replace")
        pos = z + 1
        if magic == b"FArC":
            off, csize, usize = struct.unpack(">III", head[pos:pos + 12])
            pos += 12
        else:
            off, usize = struct.unpack(">II", head[pos:pos + 8])
            csize = usize
            pos += 8
        out.append(dict(name=name, offset=off, csize=csize, usize=usize))
    return magic.decode(), out


def main():
    s = Stfs(sys.argv[1])
    result = {}
    for e in s.file_table():
        if e["is_dir"] or not e["name"].endswith(".farc"):
            continue
        head = read_prefix(s, e, 8)
        (hsize,) = struct.unpack(">I", head[4:8])
        head = read_prefix(s, e, 8 + hsize)
        magic, entries = parse_farc(head)
        result[e["name"]] = entries
        usz = sum(x["usize"] for x in entries)
        print("== %s  (%s, %d entries, %.1f MB unpacked)" % (e["name"], magic, len(entries), usz / 1e6))
        for x in entries[:6]:
            print("   %-50s %10d -> %10d" % (x["name"], x["csize"], x["usize"]))
        if len(entries) > 6:
            print("   ... last:", entries[-1]["name"])
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)


if __name__ == "__main__":
    main()
