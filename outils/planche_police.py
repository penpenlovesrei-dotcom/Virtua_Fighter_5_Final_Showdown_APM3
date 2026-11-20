#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rendre la planche de police, et retrouver un glyphe par son caractere.

Disposition MESUREE (mesurer_atlas.py, autocorrelation) :
  . 8 bits par pixel (247 valeurs distinctes dans le fichier -- ce n'est pas
    du 4 bits, contrairement a ce que je croyais)
  . pas de ligne 32 octets, pic net a 0.7358 avec ses multiples 64/96/128
  . donc une case = 32 octets x 32 lignes = 1024 octets, cases bout a bout
  . 7 766 016 / 1024 = 7584 cases

Carte fontmap.bin (FMH3), en-tete de police a l'offset donne par la table de
tetes ; chaque police porte :
    +0x04 u8 x4   largeur/hauteur du glyphe, puis du pas (chasse)
    +0x10 u32     nombre de colonnes
    +0x14 u32     nombre de glyphes
    +0x18 u32     pointeur vers la table des glyphes
Un enregistrement de glyphe fait 8 octets :
    u16 codepoint | u16 page | u16 indice de case | u8 marge | u8 largeur

    py -3 tools/planche_police.py --page 0 --cases 0 128
    py -3 tools/planche_police.py --texte "ABC 0123"
    py -3 tools/planche_police.py --plage E000 E040
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
ATLAS = os.path.join(RACINE, 'extracted', 'font_gothic.bin')
CARTE = os.path.join(RACINE, 'extracted', 'fontmap.bin')
CASE = 32                       # 32 x 32 pixels, 1 octet par pixel
OCTETS_CASE = CASE * CASE


def lire_carte():
    d = open(CARTE, 'rb').read()
    assert d[:4] == b'FMH3', d[:4]
    nb = struct.unpack_from('<I', d, 8)[0]
    polices = []
    for i in range(nb):
        tete = struct.unpack_from('<I', d, 0x10 + 4 * i)[0]
        gl_l, gl_h, pas_l, pas_h = d[tete + 4:tete + 8]
        cols = struct.unpack_from('<I', d, tete + 0x10)[0]
        n = struct.unpack_from('<I', d, tete + 0x14)[0]
        tbl = struct.unpack_from('<I', d, tete + 0x18)[0]
        glyphes = {}
        for k in range(n):
            o = tbl + 8 * k
            cp, page, idx = struct.unpack_from('<HHH', d, o)
            marge, larg = d[o + 6], d[o + 7]
            glyphes[cp] = (page, idx, marge, larg)
        polices.append({'i': i, 'glyphe': (gl_l, gl_h), 'pas': (pas_l, pas_h),
                        'cols': cols, 'n': n, 'table': tbl, 'g': glyphes})
    return polices


def case(data, idx):
    o = idx * OCTETS_CASE
    return data[o:o + OCTETS_CASE]


def bmp_gris(chemin, larg, haut, pixels):
    """BMP 24 bits, sans dependance externe. pixels = bytes de larg*haut."""
    pad = (-larg * 3) % 4
    corps = bytearray()
    for y in range(haut - 1, -1, -1):
        ligne = pixels[y * larg:(y + 1) * larg]
        for v in ligne:
            corps += bytes((v, v, v))
        corps += b'\0' * pad
    taille = 54 + len(corps)
    ent = b'BM' + struct.pack('<IHHI', taille, 0, 0, 54)
    ent += struct.pack('<IiiHHIIiiII', 40, larg, haut, 1, 24, 0,
                       len(corps), 2835, 2835, 0, 0)
    open(chemin, 'wb').write(ent + bytes(corps))


def grille(data, indices, cols, chemin, etiquettes=None):
    lignes = (len(indices) + cols - 1) // cols
    L, H = cols * CASE, lignes * CASE
    px = bytearray(L * H)
    for k, idx in enumerate(indices):
        cx, cy = (k % cols) * CASE, (k // cols) * CASE
        c = case(data, idx)
        if len(c) < OCTETS_CASE:
            continue
        for y in range(CASE):
            deb = (cy + y) * L + cx
            px[deb:deb + CASE] = c[y * CASE:(y + 1) * CASE]
    bmp_gris(chemin, L, H, bytes(px))
    return L, H


def main():
    a = sys.argv[1:]
    data = open(ATLAS, 'rb').read()
    polices = lire_carte()
    print('planche : %d octets -> %d cases de %dx%d'
          % (len(data), len(data) // OCTETS_CASE, CASE, CASE))
    for p in polices:
        print('  police %d : glyphe %dx%d  pas %dx%d  %d colonnes  '
              '%d glyphes  table 0x%X'
              % (p['i'], p['glyphe'][0], p['glyphe'][1], p['pas'][0],
                 p['pas'][1], p['cols'], p['n'], p['table']))
        cps = sorted(p['g'])
        print('       codepoints 0x%04X..0x%04X ; indices %d..%d'
              % (cps[0], cps[-1], min(v[1] for v in p['g'].values()),
                 max(v[1] for v in p['g'].values())))
    print()

    sortie = os.environ.get('SORTIE') or os.path.join(RACINE, 'analysis')
    g0 = polices[0]['g']

    if '--texte' in a:
        txt = a[a.index('--texte') + 1]
        idx = []
        for ch in txt:
            e = g0.get(ord(ch))
            print('  %r U+%04X -> %s' % (ch, ord(ch), e))
            if e:
                idx.append(e[1])
        f = os.path.join(sortie, 'police_texte.bmp')
        print(grille(data, idx, min(len(idx), 16), f), f)
        return 0

    if '--plage' in a:
        i = a.index('--plage')
        d0, d1 = int(a[i + 1], 16), int(a[i + 2], 16)
        idx, vus = [], []
        for cp in range(d0, d1 + 1):
            e = g0.get(cp)
            if e:
                idx.append(e[1])
                vus.append(cp)
        print('  %d glyphes dans U+%04X..U+%04X : %s'
              % (len(idx), d0, d1,
                 ' '.join('U+%04X->%d' % (c, i2) for c, i2 in
                          zip(vus, idx))[:400]))
        if idx:
            f = os.path.join(sortie, 'police_plage.bmp')
            print(grille(data, idx, min(len(idx), 16), f), f)
        return 0

    i = a.index('--cases') if '--cases' in a else -1
    d0 = int(a[i + 1]) if i >= 0 else 0
    d1 = int(a[i + 2]) if i >= 0 else 128
    f = os.path.join(sortie, 'police_cases.bmp')
    print(grille(data, list(range(d0, d1)), 16, f), f)
    return 0


if __name__ == '__main__':
    sys.exit(main())
