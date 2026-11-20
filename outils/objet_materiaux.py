#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Les MATERIAUX d'un objet de decor : drapeaux, shader, emplacements de
texture -- et de quoi comparer deux generations cote a cote.

Pourquoi : « l'eau d'Eileen » ne se tranche pas a l'oeil. Le grand plan
`stgslk_eff_water` existe chez ver.B comme chez FS ; ce qui change est le
MATERIAU (shader, cube d'environnement, drapeaux). Il fallait un outil qui les
rende, et il n'y en avait pas.

La forme, deja etablie par `variantes_vf5.py` et verifiee sur quatre archives :

    objet   +0x20  u32 nombre de materiaux
            +0x24  u32 deplacement des materiaux (depuis le debut de l objet)
    materiau            0x4B0 octets
            +0x00  u32 nombre d emplacements utilises
            +0x04  u32 DRAPEAUX (0x101 sur l eau de ver.B)
            +0x08  char[8] le nom du SHADER ("WATER01", "ITEM01"...)
            +0x14 + t*0x78   emplacement de texture t (huit)
                   +0x00 u32 drapeaux de l emplacement
                   +0x04 u32 IDENTIFIANT de texture (0xFFFFFFFF = vide)
    py -3 tools/objet_materiaux.py <objset.bin> <motif de nom>
    py -3 tools/objet_materiaux.py <objset.bin> eff_water --brut
"""
import argparse
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import objset as O                                             # noqa: E402

MATERIAU_PAS = 0x4B0
TEXTURE_PAS = 0x78
TEXTURES_PAR_MATERIAU = 8


def ascii_de(b):
    s = ''
    for c in b:
        s += chr(c) if 32 <= c < 127 else '.'
    return s


def materiaux(ob, k):
    """[(deplacement, octets)] des materiaux de l objet de rang `k`."""
    b = ob.brut
    po, = struct.unpack_from('<I', b, ob.off_objets + k * 4)
    nmat, offm = struct.unpack_from('<2I', b, po + 0x20)
    out = []
    for j in range(nmat):
        m = po + offm + j * MATERIAU_PAS
        out.append((m, bytes(b[m:m + MATERIAU_PAS])))
    return out


def shader(m):
    """Le nom du shader : huit octets en +0x08, termines par zero."""
    return m[8:0x10].split(bytes([0]))[0].decode('latin-1')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('objset')
    ap.add_argument('motif')
    ap.add_argument('--brut', action='store_true')
    a = ap.parse_args()
    ob = O.Objset(a.objset)
    noms = ob.noms()
    vus = 0
    for k, n in enumerate(noms):
        if a.motif.lower() not in n.lower():
            continue
        vus += 1
        mats = materiaux(ob, k)
        print('== %s   (rang %d, %d materiau(x))' % (n, k, len(mats)))
        for j, (dep, m) in enumerate(mats):
            nb_e, drapeaux = struct.unpack_from('<2I', m, 0)
            print('   materiau %-2d  0x%06X  shader %-10r drapeaux %08X  '
                  'emplacements %d'
                  % (j, dep, shader(m), drapeaux, nb_e))
            for t in range(TEXTURES_PAR_MATERIAU):
                o = 0x14 + t * TEXTURE_PAS
                dr, ident = struct.unpack_from('<2I', m, o)
                if ident == 0xFFFFFFFF and dr == 0:
                    continue
                print('        emplacement %d  drapeaux %08X  texture %s'
                      % (t, dr,
                         'vide' if ident == 0xFFFFFFFF else '%d' % ident))
            if a.brut:
                for o in range(0, MATERIAU_PAS, 16):
                    print('        +0x%03X  %s  %s'
                          % (o, m[o:o + 16].hex(' '), ascii_de(m[o:o + 16])))
    if not vus:
        print('(aucun objet ne porte %r)' % a.motif)


if __name__ == '__main__':
    main()
