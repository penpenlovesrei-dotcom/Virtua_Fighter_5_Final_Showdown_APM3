#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""LA TABLE D ECHAPPEMENTS DU MOTEUR, et la resolution des glyphes.

C est elle qui decide quel picto de bouton s affiche dans les menus -- pas la
table de textes, pas la planche. Des paires {glyphe UTF-8, nom} en 0x18053428E,
que le moteur substitue dans les libelles.

SEGA EN A MIS DEUX JEUX, et c est tout le sujet :

    ESC_BTN_CIRCLE       -> U+E000   le B   (Xbox 360)
    ESC_BTN_CIRCLE_PS3   -> U+E015   le rond (PlayStation)

`patch_moteur.py --boutons-xbox` fait rendre aux quatre `_PS3` les memes
glyphes que leurs homologues sans suffixe. Quatre octets.

    py -3 tools/echappements.py              la table, et ou chaque glyphe va
    py -3 tools/echappements.py --fontmap    le FMH3 en entier
    py -3 tools/echappements.py --patche     lit le binaire PATCHE, pas l origine
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
sys.path.insert(0, ICI)

import par_inventaire                                       # noqa: E402
import sllz                                                 # noqa: E402

DLL = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                   'vf5fs-pxd-w64-Retail_APM3.dll')
PAR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_data.par')

# La zone des paires, mesuree le 2026-10-09. Elle commence au premier glyphe
# (U+E000) et finit apres ESC_STK_2486.
ZONE = (0x532E80, 0x533200)


def fontmap():
    """Le fontmap.bin du .par, decompresse. Il n existe QUE la-dedans."""
    _, fichiers = par_inventaire.lire(PAR)
    for nom, taille, comp, offset, comprime in fichiers:
        if nom != 'fontmap.bin':
            continue
        with open(PAR, 'rb') as f:
            f.seek(offset)
            brut = f.read(comp if comprime else taille)
        return sllz.decompresser(brut) if comprime else brut
    raise SystemExit('fontmap.bin introuvable dans le .par')


def polices(d):
    """Les polices du FMH3 : (base, case, chasse, colonnes, n, table)."""
    assert d[:4] == b'FMH3', d[:4]
    n = struct.unpack_from('<I', d, 8)[0]
    ptr = struct.unpack_from('<I', d, 12)[0]
    out = []
    for i in range(n):
        b = struct.unpack_from('<I', d, ptr + i * 4)[0]
        lg, hg, ax, ay = d[b + 4], d[b + 5], d[b + 6], d[b + 7]
        col = struct.unpack_from('<I', d, b + 0x10)[0]
        ng = struct.unpack_from('<I', d, b + 0x14)[0]
        tab = struct.unpack_from('<I', d, b + 0x18)[0]
        out.append((b, (lg, hg), (ax, ay), col, ng, tab))
    return out


def cases(d):
    """{codepoint: (rangee, colonne, police)} pour toutes les polices."""
    m = {}
    for k, (b, case, pas, col, ng, tab) in enumerate(polices(d)):
        for i in range(ng):
            cp, _f, idx, _b6, _b7 = struct.unpack_from('<HHHBB', d, tab + i * 8)
            m.setdefault(cp, (idx >> 8, idx & 0xFF, k))
    return m


def table(brut, base_va=0x180000000):
    """Les paires {glyphe, nom} de la zone, dans l ordre du binaire."""
    lo, hi = ZONE
    o = lo
    sorties = []
    courant = None
    while o < hi:
        fin = brut.find(b'\x00', o)
        if fin < 0 or fin > hi:
            break
        s = brut[o:fin]
        if s:
            try:
                u = s.decode('utf-8')
            except UnicodeDecodeError:
                u = None
            # LE RUN PEUT PORTER DES OCTETS PARASITES DEVANT : la premiere
            # paire, ESC_BTN_CIRCLE, est precedee de deux octets de bourrage
            # dans le meme intervalle entre deux NUL. On ne garde donc que le
            # SUFFIXE en zone privee, et on rectifie l offset.
            k = len(u) if u else 0
            while u and k and 0xE000 <= ord(u[k - 1]) <= 0xF8FF:
                k -= 1
            if u and k < len(u):
                cps = [ord(c) for c in u[k:]]
                courant = (fin - 3 * len(cps), cps)
            elif u and u.startswith('ESC_') and courant:
                sorties.append((courant[0], courant[1], u, o))
                courant = None
        o = fin + 1
    return sorties


def main():
    import pe_disasm as P
    chemin = DLL if '--patche' in sys.argv else DLL + '.origine'
    img = P.Image(chemin)
    brut = img.data
    fm = fontmap()
    if '--fontmap' in sys.argv:
        print('fontmap.bin : %d octets' % len(fm))
        for b, case, pas, col, ng, tab in polices(fm):
            print('  police a 0x%X : case %dx%d, chasse %dx%d, %d colonnes, '
                  '%d glyphes, table 0x%X'
                  % (b, case[0], case[1], pas[0], pas[1], col, ng, tab))
        return 0
    ou = cases(fm)
    print('%s' % os.path.basename(chemin))
    print()
    print('%-24s %-10s %-14s %s' % ('nom', 'VA', 'glyphe(s)', 'case(s) de la planche'))
    for off, cps, nom, offnom in table(brut):
        va = img.off2va(off)
        g = ' '.join('U+%04X' % c for c in cps)
        c = ' '.join(('r%d c%d' % ou[c][:2]) if c in ou else '?' for c in cps)
        print('%-24s 0x%X  %-14s %s' % (nom, va, g, c))
    return 0


if __name__ == '__main__':
    sys.exit(main())
