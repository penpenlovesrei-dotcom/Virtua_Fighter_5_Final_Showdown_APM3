#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bornes reelles de 0x180227790 : entrees .pdata, chainage, voisinage."""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                          # noqa: E402
import graphe_appels as G                                      # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')

img = P.Image(MOTEUR)
ent = G.entrees_pdata(img)

CIBLE = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0x180227790

print('--- entrees .pdata brutes autour de 0x%X ---' % CIBLE)
for i, (deb, fin, unw) in enumerate(ent):
    if not (CIBLE - 0x400 <= deb <= CIBLE + 0x2400):
        continue
    o = img.va2off(img.base + unw)
    ver_flags, prol, n_codes, fr = img.data[o:o + 4]
    chain = bool((ver_flags >> 3) & 0x04)
    extra = ''
    if chain:
        saut = 4 + 2 * ((n_codes + 1) & ~1)
        pb, pe, pu = struct.unpack_from('<III', img.data, o + saut)
        extra = '  -> mere 0x%X..0x%X' % (img.base + pb, img.base + pe)
    print('  0x%X .. 0x%X  (%5d o)  unw=0x%X ver=%d flags=%d ncodes=%d%s%s'
          % (deb, fin, fin - deb, img.base + unw, ver_flags & 7,
             ver_flags >> 3, n_codes, '  CHAINE' if chain else '', extra))

print()
print('--- fonctions reelles (fragments rattaches) ---')
debuts, fins = G.fonctions_reelles(img)
for d in debuts:
    if CIBLE - 0x400 <= d <= CIBLE + 0x2400:
        print('  0x%X .. 0x%X  (%d o)' % (d, fins[d], fins[d] - d))
