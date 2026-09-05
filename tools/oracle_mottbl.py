#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fait arbitrer le decodage de rob_cmn_mottbl.bin par le moteur lui-meme.

La DLL du build APM3 (vf5fs-pxd-w64-Retail_APM3.dll) n'a que des imports systeme :
elle se charge dans un processus Python ordinaire. On y installe un tampon
rob_cmn_mottbl relocalise, puis on appelle GetMotionForRole(perso, posture, role)
pour toutes les combinaisons et on compare a ce que tools/motdb.py rend.

Relocation : dans le fichier, chaque offset est absolu depuis le debut du fichier ;
le chargeur le reecrit sur place en offset RELATIF AU CHAMP qui le porte. Le code
du moteur le montre :
    lea r11,[rax+8] ; movsxd r10,[r11] ; add r10,r11      -> table des entrees
    lea rdx,[r10+chr*8] ; movsxd rax,[rdx] ; lea rcx,[rdx+rax]   -> table des postures
    movsxd rax,[rcx+posture*4] ; lea rdx,[rcx+posture*4] ; lea r9,[rdx+rax]  -> bloc

Usage :
    py -3 tools/oracle_mottbl.py
"""
import ctypes
import os
import struct
import sys

DLL = 'runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll'
TBL = 'extracted/APM3_FS_farc/rob/rob_mot_tbl/rob_cmn_mottbl.bin'
MOTDB = 'extracted/APM3_FS_farc/rob/mot_db/mot_db.bin'
VA_GETMOTION = 0x18015B310          # GetMotionForRole, trouve par motif d'octets
VA_GLOBAL = 0x180713F20             # le global qu'ecrit ParseRobCmnMotTbl


def relocate(raw):
    """Reecrit chaque offset en relatif au champ qui le porte."""
    d = bytearray(raw)

    def u32(o):
        return struct.unpack_from('<I', d, o)[0]

    def put(o, v):
        struct.pack_into('<i', d, o, v)

    count, nslot, tbl = u32(0), u32(4), u32(8)
    # Deux entrees peuvent partager la meme table de postures : on releve d'abord
    # toutes les positions a relocaliser, chacune une seule fois, puis on ecrit.
    champs = {8: tbl}
    for i in range(count):
        p = tbl + 8 * i
        off, npos = u32(p), u32(p + 4)
        champs[p] = off
        for k in range(npos):
            q = off + 4 * k
            champs.setdefault(q, u32(q))
    for pos, val in champs.items():
        put(pos, val - pos)
    return bytes(d), count, nslot


def main():
    raw = open(TBL, 'rb').read()
    buf, count, nslot = relocate(raw)
    print('rob_cmn_mottbl.bin : %d octets, %d entrees, borne de role %d'
          % (len(raw), count, nslot))

    dll = ctypes.WinDLL(os.path.abspath(DLL))
    base = dll._handle
    print('DLL chargee a 0x%X' % base)
    fn = base + (VA_GETMOTION - 0x180000000)
    glob = base + (VA_GLOBAL - 0x180000000)

    mem = ctypes.create_string_buffer(buf, len(buf))
    ctypes.memmove(glob, ctypes.byref(ctypes.c_void_p(ctypes.addressof(mem))), 8)
    print('tampon installe a 0x%X, global ecrit en 0x%X'
          % (ctypes.addressof(mem), glob))

    F = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)(fn)

    sys.path.insert(0, 'tools')
    from motdb import RobMotTbl
    ref = RobMotTbl(TBL)

    ok = diff = 0
    exemples = []
    for chr_ in range(count):
        e = ref.entries[chr_]
        for posture in range(e['nposture']):
            mine = ref.slots(chr_, posture)
            for role in range(nslot):
                got = F(chr_, posture, role) & 0xFFFFFFFF
                exp = mine[role] if role < len(mine) else None
                if exp is None:
                    continue
                if got == exp:
                    ok += 1
                else:
                    diff += 1
                    if len(exemples) < 8:
                        exemples.append((chr_, posture, role, got, exp))
    print()
    print('%d valeurs comparees : %d identiques, %d differentes' % (ok + diff, ok, diff))
    for c, p, r, g, e in exemples:
        print('   perso %2d posture %d role %3d : moteur %6d, motdb.py %6d' % (c, p, r, g, e))
    if diff == 0:
        print('Le moteur rend exactement ce que tools/motdb.py rend, sur toute la table.')
    return 0 if diff == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
