#!/usr/bin/env python3
"""Depaquete un PKG PS3 retail (chiffrement AES-128-CTR, cle gpkg publique).

Ne dechiffre PAS les SELF/EBOOT qu'il contient : ceux-ci restent chiffres SCE.

Usage:
    py -3 tools/unpack_ps3_pkg.py <pkg> --list
    py -3 tools/unpack_ps3_pkg.py <pkg> --out <dir> [--only SUBSTR]
"""
import os
import struct
import sys

from Crypto.Cipher import AES

# Cle publique utilisee par tous les PKG PS3 retail (gpkg_key).
GPKG_KEY = bytes.fromhex("2E7B71D7C9C9A14EA3221F188828B8F8")
CHUNK_BLOCKS = 4096          # 64 Kio de keystream par tour


class PkgCtr:
    """Keystream AES-128-CTR : bloc n = AES_ECB(gpkg_key, riv + n)."""

    def __init__(self, riv):
        self.riv = int.from_bytes(riv, "big")
        self.ecb = AES.new(GPKG_KEY, AES.MODE_ECB)

    def keystream(self, first_block, nblocks):
        buf = bytearray()
        v = self.riv + first_block
        for i in range(nblocks):
            buf += ((v + i) & ((1 << 128) - 1)).to_bytes(16, "big")
        return self.ecb.encrypt(bytes(buf))

    def decrypt_at(self, fp, data_offset, rel_off, size):
        """Dechiffre `size` octets a l'offset relatif `rel_off` dans la zone data."""
        first = rel_off // 16
        pad = rel_off % 16
        total = pad + size
        nblocks = (total + 15) // 16
        fp.seek(data_offset + first * 16)
        out = bytearray()
        done = 0
        while done < nblocks:
            n = min(CHUNK_BLOCKS, nblocks - done)
            ct = fp.read(n * 16)
            if not ct:
                break
            ks = self.keystream(first + done, n)
            out += bytes(a ^ b for a, b in zip(ct, ks[:len(ct)]))
            done += n
        return bytes(out[pad:pad + size])


def read_header(fp):
    fp.seek(0)
    h = fp.read(0x100)
    if h[:4] != b"\x7fPKG":
        raise SystemExit("magic PKG absent")
    rev, ptype = struct.unpack(">HH", h[4:8])
    item_count = struct.unpack(">I", h[0x14:0x18])[0]
    total_size, data_offset, data_size = struct.unpack(">QQQ", h[0x18:0x30])
    content_id = h[0x30:0x60].split(b"\0")[0].decode("latin-1")
    riv = h[0x70:0x80]
    return dict(rev=rev, type=ptype, item_count=item_count, total_size=total_size,
                data_offset=data_offset, data_size=data_size,
                content_id=content_id, riv=riv)


def read_items(fp, hdr, ctr):
    n = hdr["item_count"]
    table = ctr.decrypt_at(fp, hdr["data_offset"], 0, n * 0x20)
    items = []
    for i in range(n):
        rec = table[i * 0x20:(i + 1) * 0x20]
        (name_off, name_size) = struct.unpack(">II", rec[0:8])
        (doff, dsize) = struct.unpack(">QQ", rec[8:0x18])
        flags = struct.unpack(">I", rec[0x18:0x1C])[0]
        items.append(dict(name_off=name_off, name_size=name_size,
                          off=doff, size=dsize, flags=flags))
    for it in items:
        raw = ctr.decrypt_at(fp, hdr["data_offset"], it["name_off"], it["name_size"])
        it["name"] = raw.split(b"\0")[0].decode("latin-1")
    return items


def main():
    path = sys.argv[1]
    with open(path, "rb") as fp:
        hdr = read_header(fp)
        ctr = PkgCtr(hdr["riv"])
        print("content id  : %s" % hdr["content_id"])
        print("revision    : 0x%04X (%s)" % (
            hdr["rev"], "retail" if hdr["rev"] == 0x8000 else "debug/autre"))
        print("type        : 0x%04X (%s)" % (
            hdr["type"], "PS3" if hdr["type"] == 1 else "PSP/autre"))
        print("elements    : %d" % hdr["item_count"])
        print("data        : off=0x%X size=0x%X" % (hdr["data_offset"], hdr["data_size"]))
        print()
        items = read_items(fp, hdr, ctr)

        if "--list" in sys.argv:
            for it in items:
                kind = "DIR " if (it["flags"] & 0xFF) == 4 else "FILE"
                print("%s %12d  flags=0x%08X  %s"
                      % (kind, it["size"], it["flags"], it["name"]))
            return

        outdir = sys.argv[sys.argv.index("--out") + 1]
        only = None
        if "--only" in sys.argv:
            only = sys.argv[sys.argv.index("--only") + 1]
        for it in items:
            if only and only not in it["name"]:
                continue
            dest = os.path.join(outdir, it["name"].replace("/", os.sep))
            if (it["flags"] & 0xFF) == 4:
                os.makedirs(dest, exist_ok=True)
                continue
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            data = ctr.decrypt_at(fp, hdr["data_offset"], it["off"], it["size"])
            with open(dest, "wb") as out:
                out.write(data)
            print("%12d  %s" % (it["size"], it["name"]), flush=True)


if __name__ == "__main__":
    main()
