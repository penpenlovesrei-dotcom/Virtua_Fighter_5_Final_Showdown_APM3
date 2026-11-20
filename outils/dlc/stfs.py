#!/usr/bin/env python3
"""Read-only inspector for Xbox 360 STFS packages (CON / LIVE / PIRS).

usage: stfs.py PACKAGE OUTDIR [--verify] [--extract]
Addressing follows Velocity's StfsPackage (female / read-only layout).
"""
import hashlib
import os
import struct
import sys

BLOCK = 0x1000


def u24le(b):
    return b[0] | (b[1] << 8) | (b[2] << 16)


def u24be(b):
    return (b[0] << 16) | (b[1] << 8) | b[2]


def wstr(b):
    return b.decode("utf-16-be", errors="replace").split("\x00", 1)[0]


def fat_time(v):
    if not v:
        return ""
    d, t = v >> 16, v & 0xFFFF
    return "%04d-%02d-%02d %02d:%02d:%02d" % (
        (d >> 9) + 1980, (d >> 5) & 0xF, d & 0x1F, t >> 11, (t >> 5) & 0x3F, (t & 0x1F) * 2)


class Stfs:
    def __init__(self, path):
        self.f = open(path, "rb")
        h = self.read(0, 0xB000)
        self.magic = h[:4].decode("ascii", "replace")
        self.content_id = h[0x32C:0x340].hex().upper()
        self.header_size, self.content_type, self.meta_version = struct.unpack(">III", h[0x340:0x34C])
        (self.content_size,) = struct.unpack(">Q", h[0x34C:0x354])
        self.media_id, self.version, self.base_version, self.title_id = struct.unpack(">IIII", h[0x354:0x364])
        vd = h[0x379:0x379 + 0x24]
        self.block_sep = vd[2]
        (self.ft_count,) = struct.unpack("<H", vd[3:5])
        self.ft_start = u24le(vd[5:8])
        self.top_hash = vd[8:28]
        self.alloc, self.unalloc = struct.unpack(">II", vd[28:36])
        (self.descriptor_type,) = struct.unpack(">I", h[0x3A9:0x3AD])
        self.names = [wstr(h[0x411 + i * 0x100:0x511 + i * 0x100]) for i in range(9)]
        self.descs = [wstr(h[0xD11 + i * 0x100:0xE11 + i * 0x100]) for i in range(9)]
        self.publisher = wstr(h[0x1611:0x1691])
        self.title_name = wstr(h[0x1691:0x1711])
        self.transfer_flags = h[0x1711]
        tsz, ttsz = struct.unpack(">II", h[0x1712:0x171A])
        self.thumb = h[0x171A:0x171A + tsz]
        self.title_thumb = h[0x571A:0x571A + ttsz]
        if self.meta_version >= 2:
            self.names += [wstr(h[0x541A + i * 0x100:0x551A + i * 0x100]) for i in range(3)]
            self.descs += [wstr(h[0x941A + i * 0x100:0x951A + i * 0x100]) for i in range(3)]

        self.sex = (~self.block_sep) & 1  # 0 = female (read-only, single hash tables)
        if self.sex != 0:
            raise NotImplementedError("male (writable) STFS layout not supported")
        self.step0, self.step1 = 0xAB, 0x718F
        self.first_hash = (self.header_size + 0xFFF) & ~0xFFF
        if self.alloc <= 0xAA:
            self.top_level = 0
        elif self.alloc <= 0x70E4:
            self.top_level = 1
        else:
            self.top_level = 2
        self._l0_cache = {}

    def read(self, off, n):
        self.f.seek(off)
        return self.f.read(n)

    # --- block addressing -------------------------------------------------
    def data_block(self, b):
        r = ((b + 0xAA) // 0xAA) + b
        if b < 0xAA:
            return r
        if b < 0x70E4:
            return r + ((b + 0x70E4) // 0x70E4)
        return 1 + r + ((b + 0x70E4) // 0x70E4)

    def l0_block(self, b):
        if b < 0xAA:
            return 0
        n = (b // 0xAA) * self.step0 + ((b // 0x70E4) + 1)
        return n if b // 0x70E4 == 0 else n + 1

    def l1_block(self, b):
        return self.step0 if b < 0x70E4 else 1 + (b // 0x70E4) * self.step1

    def l2_block(self, b):
        return self.step1

    def addr(self, phys_block):
        return (phys_block << 12) + self.first_hash

    def top_table_addr(self):
        blk = {0: 0, 1: self.step0, 2: self.step1}[self.top_level]
        return self.addr(blk)

    def l0_entry(self, b):
        tb = self.l0_block(b)
        tab = self._l0_cache.get(tb)
        if tab is None:
            tab = self.read(self.addr(tb), BLOCK)
            if len(self._l0_cache) > 64:
                self._l0_cache.clear()
            self._l0_cache[tb] = tab
        i = (b % 0xAA) * 0x18
        e = tab[i:i + 0x18]
        return e[:20], e[20], u24be(e[21:24])

    def read_block(self, b):
        return self.read(self.addr(self.data_block(b)), BLOCK)

    # --- file table -------------------------------------------------------
    def file_table(self):
        entries = []
        b = self.ft_start
        for _ in range(self.ft_count):
            data = self.read_block(b)
            for j in range(0, BLOCK, 0x40):
                e = data[j:j + 0x40]
                flags = e[0x28]
                nlen = flags & 0x3F
                if nlen == 0:
                    entries.append(None)
                    continue
                (path,) = struct.unpack(">h", e[0x32:0x34])
                size, ctime, atime = struct.unpack(">III", e[0x34:0x40])
                entries.append(dict(
                    name=e[:nlen].decode("ascii", "replace"),
                    is_dir=bool(flags & 0x80),
                    contiguous=bool(flags & 0x40),
                    blocks=u24le(e[0x29:0x2C]),
                    start=u24le(e[0x2F:0x32]),
                    parent=path,
                    size=size,
                    ctime=fat_time(ctime),
                    atime=fat_time(atime),
                ))
            b = self.l0_entry(b)[2]
        for e in entries:
            if e is None:
                continue
            parts, p, guard = [e["name"]], e["parent"], 0
            while p != -1 and guard < 64:
                parent = entries[p]
                parts.append(parent["name"])
                p, guard = parent["parent"], guard + 1
            e["path"] = "/".join(reversed(parts))
        return [e for e in entries if e is not None]

    def file_blocks(self, e):
        b = e["start"]
        for i in range(e["blocks"]):
            yield b
            b = b + 1 if e["contiguous"] else self.l0_entry(b)[2]

    def iter_file(self, e):
        left = e["size"]
        for b in self.file_blocks(e):
            if left <= 0:
                break
            chunk = self.read_block(b)[:min(BLOCK, left)]
            left -= len(chunk)
            yield chunk


def main():
    pkg, out = sys.argv[1], sys.argv[2]
    verify = "--verify" in sys.argv
    extract = "--extract" in sys.argv
    os.makedirs(out, exist_ok=True)
    s = Stfs(pkg)

    print("magic            :", s.magic)
    print("content id       :", s.content_id)
    print("title id         : %08X" % s.title_id)
    print("title name       :", s.title_name)
    print("publisher        :", s.publisher)
    print("content type     : %08X" % s.content_type)
    print("metadata version :", s.meta_version)
    print("content size     :", s.content_size)
    print("version/base     :", s.version, s.base_version)
    print("media id         : %08X" % s.media_id)
    print("transfer flags   : %02X" % s.transfer_flags)
    print("descriptor type  :", s.descriptor_type, "(0=STFS,1=SVOD)")
    print("block separation :", s.block_sep, "sex:", "female" if s.sex == 0 else "male")
    print("header size      : %X  first hash table @ %X" % (s.header_size, s.first_hash))
    print("alloc/unalloc    :", s.alloc, s.unalloc, "top level:", s.top_level)
    print("file table       : start", s.ft_start, "count", s.ft_count)
    for i, n in enumerate(s.names):
        if n:
            print("name[%d]          : %s" % (i, n))
    for i, d in enumerate(s.descs):
        if d:
            print("desc[%d]          : %s" % (i, d))

    top = s.read(s.top_table_addr(), BLOCK)
    print("top hash valid   :", hashlib.sha1(top).digest() == s.top_hash)

    for name, data in (("thumbnail.png", s.thumb), ("title_thumbnail.png", s.title_thumb)):
        if data:
            with open(os.path.join(out, name), "wb") as fh:
                fh.write(data)

    files = s.file_table()
    total = 0
    print("\n%-60s %12s %6s %s" % ("path", "size", "contig", "head"))
    for e in files:
        if e["is_dir"]:
            print("%-60s %12s" % (e["path"] + "/", "<dir>"))
            continue
        head = s.read_block(e["start"])[:16] if e["size"] else b""
        total += e["size"]
        print("%-60s %12d %6s %s %r" % (e["path"], e["size"], e["contiguous"], head.hex(), head[:8]))
    print("\nfiles:", sum(not e["is_dir"] for e in files), "dirs:", sum(e["is_dir"] for e in files), "bytes:", total)

    if verify:
        bad = checked = 0
        for e in files:
            if e["is_dir"]:
                continue
            for b in s.file_blocks(e):
                h, _, _ = s.l0_entry(b)
                if hashlib.sha1(s.read_block(b)).digest() != h:
                    bad += 1
                    if bad <= 10:
                        print("BAD block", b, "in", e["path"])
                checked += 1
        print("verified data blocks:", checked, "bad:", bad)

    if extract:
        root = os.path.join(out, "files")
        for e in files:
            dst = os.path.join(root, *e["path"].split("/"))
            if e["is_dir"]:
                os.makedirs(dst, exist_ok=True)
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "wb") as fh:
                for chunk in s.iter_file(e):
                    fh.write(chunk)
        print("extracted to", root)


if __name__ == "__main__":
    main()
