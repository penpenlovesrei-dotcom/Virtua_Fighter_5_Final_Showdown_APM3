#!/usr/bin/env python3
"""Inventaire + typage + hash des sources VF5.

Lecture seule sur les dumps. Produit un CSV par source dans analysis/inventory/.

Usage:
    python tools/inventory_sources.py [ID ...]
"""
import csv
import hashlib
import os
import struct
import sys

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(WORK, "analysis", "inventory")

DESK = r"C:\Users\frede\Desktop\VF5 FS DECOMP"
SOURCES = {
    "LIND_FS": os.path.join(DESK, "LIND_FS"),
    "APM3_FS": os.path.join(DESK, "APM3_FS"),
    "PS3_FS": os.path.join(DESK, "PS3_FS"),
    "X360_FS": os.path.join(DESK, "X360_FS"),
    "APM3_US": os.path.join(DESK, "APM3_US"),
    "PC_REVO": r"C:\Program Files (x86)\Steam\steamapps\common\VFREVO",
}

# Hash integral en dessous de ce seuil ; au-dela, hash de tete+queue (marque HEADTAIL).
FULL_HASH_LIMIT = 64 * 1024 * 1024
CHUNK = 1 << 20

EM = {
    0x03: "x86",
    0x3E: "x86-64",
    0x14: "PowerPC",
    0x15: "PowerPC64",
    0x28: "ARM",
    0xB7: "AArch64",
    0x08: "MIPS",
    0x2A: "SuperH",
}
ET = {1: "REL", 2: "EXEC", 3: "DYN", 4: "CORE"}


def elf_info(fp):
    """Renvoie une description ELF a partir d'un fichier ouvert positionne a 0."""
    hdr = fp.read(64)
    if len(hdr) < 20:
        return None
    cls = hdr[4]
    end = "<" if hdr[5] == 1 else ">"
    etype, machine = struct.unpack(end + "HH", hdr[16:20])
    return "ELF%s %s %s %s" % (
        "32" if cls == 1 else "64",
        "LE" if hdr[5] == 1 else "BE",
        ET.get(etype, "T%d" % etype),
        EM.get(machine, "machine=0x%X" % machine),
    )


def sniff(path):
    """Type sommaire d'apres la signature (jamais d'apres l'extension seule)."""
    try:
        with open(path, "rb") as fp:
            magic = fp.read(16)
            if magic[:4] == b"\x7fELF":
                fp.seek(0)
                return elf_info(fp) or "ELF"
            if magic[:4] == b"XEX2":
                return "Xbox360 XEX2"
            if magic[:4] == b"XEX1":
                return "Xbox360 XEX1"
            if magic[:4] == b"\x53\x43\x45\x00" or magic[:4] == b"SCE\x00":
                return "PS3 SELF/SPRX (SCE)"
            if magic[:4] == b"\x7fPKG" or magic[:4] == b"\x7FPKG":
                return "PS3 PKG"
            if magic[:4] == b"FArc":
                return "FARC (non compresse)"
            if magic[:4] == b"FArC":
                return "FARC (compresse)"
            if magic[:4] == b"FARC":
                return "FARC (chiffre/FT)"
            if magic[:2] == b"MZ":
                return "PE/DOS"
            if magic[:6] == b"7z\xbc\xaf\x27\x1c":
                return "7z"
            if magic[:4] == b"Rar!":
                return "RAR"
            if magic[:4] == b"PK\x03\x04":
                return "ZIP"
            if magic[:4] == b"RIFF":
                return "RIFF"
            if magic[:3] == b"DDS":
                return "DDS"
            if magic[:4] == b"OggS":
                return "Ogg"
            if magic[:2] == b"#!":
                return "script shell"
            if magic[:4] == b"\x1f\x8b\x08\x00" or magic[:2] == b"\x1f\x8b":
                return "gzip"
            return None
    except OSError:
        return None


def hash_file(path, size):
    h = hashlib.sha256()
    tag = "FULL"
    try:
        with open(path, "rb") as fp:
            if size <= FULL_HASH_LIMIT:
                while True:
                    blk = fp.read(CHUNK)
                    if not blk:
                        break
                    h.update(blk)
            else:
                tag = "HEADTAIL"
                h.update(struct.pack("<Q", size))
                h.update(fp.read(CHUNK))
                fp.seek(-CHUNK, os.SEEK_END)
                h.update(fp.read(CHUNK))
    except OSError as exc:
        return "ERREUR", str(exc)
    return tag, h.hexdigest()


def walk(sid, root, writer):
    n = 0
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            try:
                size = os.path.getsize(full)
            except OSError:
                continue
            tag, digest = hash_file(full, size)
            writer.writerow([
                sid,
                os.path.relpath(full, root).replace("\\", "/"),
                size,
                sniff(full) or "",
                tag,
                digest,
            ])
            n += 1
            if n % 500 == 0:
                print("  %s : %d fichiers" % (sid, n), flush=True)
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    wanted = sys.argv[1:] or list(SOURCES)
    for sid in wanted:
        root = SOURCES[sid]
        if not os.path.isdir(root):
            print("ABSENT %s -> %s" % (sid, root))
            continue
        dest = os.path.join(OUT, sid + ".csv")
        with open(dest, "w", newline="", encoding="utf-8") as fp:
            w = csv.writer(fp)
            w.writerow(["source", "path", "size", "type", "hash_mode", "sha256"])
            n = walk(sid, root, w)
        print("%s : %d fichiers -> %s" % (sid, n, dest), flush=True)


if __name__ == "__main__":
    main()
