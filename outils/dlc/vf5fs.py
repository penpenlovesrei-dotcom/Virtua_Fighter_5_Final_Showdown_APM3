"""VF5 Final Showdown DLC helpers: FArC archives, obj sets and TXP texture sets."""
import gzip
import struct

# Internal 3-letter codes -> display names. krt/mon/msk are deduced from the
# fighting style (karate / monkey kung-fu / masked luchador).
CHARACTERS = {
    "aki": "Akira", "aoi": "Aoi", "bra": "Brad", "dur": "Dural", "goh": "Goh", "jak": "Jacky",
    "jef": "Jeffry", "kag": "Kage", "krt": "Jean", "lau": "Lau", "lei": "Lei-Fei",
    "lio": "Lion", "mon": "Eileen", "msk": "El Blaze", "pai": "Pai", "sar": "Sarah",
    "shu": "Shun", "tak": "Taka-Arashi", "van": "Vanessa", "wol": "Wolf",
}

TEX_FORMATS = {
    0: "A8", 1: "RGB8", 2: "RGBA8", 3: "RGB5", 4: "RGB5A1", 5: "RGBA4",
    6: "DXT1", 7: "DXT1a", 8: "DXT3", 9: "DXT5", 10: "ATI1", 11: "ATI2",
    12: "L8", 13: "L8A8", 15: "BC7", 16: "BC6H",
    0x363358: "RG88",  # 'X36' in VF5 2007: uncompressed 2x8-bit normal maps
}

OBJSET_MAGIC = 0x05062500
TXP_SET, TXP_TEX, TXP_CUBE, TXP_MIP = 0x03505854, 0x04505854, 0x05505854, 0x02505854


def cstr(b, off, maxlen=None):
    end = b.find(b"\0", off, None if maxlen is None else off + maxlen)
    if end < 0:
        end = off + maxlen
    return b[off:end].decode("ascii", "replace")


def u32s(b, off, n):
    return list(struct.unpack_from("<%dI" % n, b, off))


# --- FArC -------------------------------------------------------------------
def farc_entries(data):
    magic = data[:4]
    (hsize,) = struct.unpack_from(">I", data, 4)
    pos, end, out = (12 if magic in (b"FArC", b"FArc") else 8), 8 + hsize, []
    while pos < end:
        z = data.index(b"\0", pos)
        name = data[pos:z].decode("ascii", "replace")
        pos = z + 1
        if magic == b"FArC":
            off, csize, usize = struct.unpack_from(">III", data, pos)
            pos += 12
        else:
            off, usize = struct.unpack_from(">II", data, pos)
            csize = usize
            pos += 8
        out.append(dict(name=name, offset=off, csize=csize, usize=usize))
    return out


def iter_farc(stfs, file_entry):
    """Yield (entry, unpacked bytes) for every file of a FArC stored in the package."""
    return iter_farc_bytes(b"".join(stfs.iter_file(file_entry)))


def iter_farc_bytes(data):
    """Yield (entry, unpacked bytes) for every file of a FArC held in memory."""
    for ent in farc_entries(data):
        raw = data[ent["offset"]:ent["offset"] + ent["csize"]]
        payload = gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw
        if len(payload) != ent["usize"]:
            raise ValueError("%s: size %d != %d" % (ent["name"], len(payload), ent["usize"]))
        yield ent, payload


# --- obj set ------------------------------------------------------------------
def parse_objset(d):
    ver, nobj, _, objs_off, skins_off, names_off, ids_off, texids_off, ntex = u32s(d, 0, 9)
    if ver & 0xFFFFFF00 != OBJSET_MAGIC:
        raise ValueError("not an obj set (magic %08X)" % ver)
    names = [cstr(d, p) for p in u32s(d, names_off, nobj)]
    ids = u32s(d, ids_off, nobj)
    skins = u32s(d, skins_off, nobj) if skins_off else [0] * nobj
    objects = []
    for i, op in enumerate(u32s(d, objs_off, nobj)):
        nmesh, meshes_off, nmat, mats_off = struct.unpack_from("<4I", d, op + 0x18)
        meshes = []
        for m in range(nmesh):
            mp = op + meshes_off + m * 0xD8
            meshes.append(dict(
                name=cstr(d, mp + 0x98, 64),
                submeshes=struct.unpack_from("<I", d, mp + 0x14)[0],
                vertices=struct.unpack_from("<I", d, mp + 0x24)[0],
            ))
        materials = []
        for k in range(nmat):
            mp = op + mats_off + k * 0x4B0
            materials.append(dict(shader=cstr(d, mp + 8, 8), name=cstr(d, mp + 0x430, 64)))
        objects.append(dict(name=names[i], id=ids[i], skinned=bool(skins[i]),
                            meshes=meshes, materials=materials))
    return dict(objects=objects, texture_ids=u32s(d, texids_off, ntex))


# --- TXP texture set ------------------------------------------------------------
def parse_txp(t):
    sig, count, _ = u32s(t, 0, 3)
    if sig != TXP_SET:
        raise ValueError("not a TXP set (magic %08X)" % sig)
    textures = []
    for o in u32s(t, 12, count):
        tsig, nsub, info = u32s(t, o, 3)
        mips, array = info & 0xFF, (info >> 8) & 0xFF
        if mips * array != nsub:
            mips, array = nsub, 1
        subs = []
        for so in u32s(t, o + 12, nsub):
            msig, w, h, fmt, idx, size = u32s(t, o + so, 6)
            if msig != TXP_MIP:
                raise ValueError("bad mip header")
            subs.append(dict(width=w, height=h, format=fmt, index=idx, size=size, data=o + so + 24))
        textures.append(dict(cube=tsig == TXP_CUBE, mips=mips, array=array, subs=subs))
    return textures


BCN = {"DXT1": (1, "RGBA"), "DXT1a": (1, "RGBA"), "DXT3": (2, "RGBA"), "DXT5": (3, "RGBA"),
       "ATI1": (4, "L"), "ATI2": (5, "RGB"), "BC7": (7, "RGBA")}
RAW = {"RGB8": ("RGB", "RGB"), "RGBA8": ("RGBA", "RGBA"), "A8": ("L", "L"), "L8": ("L", "L"),
       "L8A8": ("LA", "LA"),
       # 16-bit 5:6:5, red in the low bits (checked against the item's DXT textures)
       "RGB5": ("RGB", "RGB;16")}


def decode_mip(t, sub, upright=True):
    """Decode one mip to a PIL image. Textures are stored bottom-up; upright flips them."""
    from PIL import Image
    fmt = TEX_FORMATS.get(sub["format"], str(sub["format"]))
    size = (sub["width"], sub["height"])
    data = t[sub["data"]:sub["data"] + sub["size"]]
    if fmt in BCN:
        n, mode = BCN[fmt]
        im = Image.frombytes(mode, size, data, "bcn", (n, fmt))
    elif fmt == "RG88":
        # laid out like the DXT5 normal maps of Final Showdown: x in green, y in alpha
        lum, alpha = Image.frombytes("LA", size, data, "raw", "LA").split()
        im = Image.merge("RGBA", (Image.new("L", size, 0), lum, Image.new("L", size, 0), alpha))
    elif fmt in RAW:
        mode, rawmode = RAW[fmt]
        im = Image.frombytes(mode, size, data, "raw", rawmode)
    else:
        raise ValueError("unsupported texture format " + fmt)
    return im.transpose(Image.FLIP_TOP_BOTTOM) if upright else im
