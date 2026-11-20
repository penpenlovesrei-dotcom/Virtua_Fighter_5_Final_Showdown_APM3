#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Decouper les PICTOS DE BOUTON de `spr_n_fnt32` et en faire une planche.

POURQUOI CET OUTIL EXISTE. Le 2026-10-09 le chantier a conclu, par elimination,
que les pictos PlayStation d'OPTIONS > Controls venaient de la table
d'echappements du moteur, et `--boutons-xbox` a fait rendre aux quatre
echappements `ESC_BTN_*_PS3` les glyphes `U+E000`..`U+E003` au lieu de
`U+E015`..`U+E018`. Frederic a essaye : LES PICTOS SONT TOUJOURS PLAYSTATION.

Or ce que `U+E000`..`U+E003` DESSINENT n'a jamais ete regarde : la ligne
« U+E000-E003 = B, A, Y, X -- le jeu Xbox 360 » de `analysis/polices_et_pictos.md`
vient de la doc du depot, pas d'une image. C'est exactement la faute de (168),
une case plus loin. Cet outil rend la case, et l'image tranche.

La chaine, et chaque maillon est mesure ailleurs :

    spr_n_fnt32.farc -> spr_n_fnt32.bin -> TXP tex0, DXT5 2048x2048
                        (tools/txp.py, deja ecrit)
    fontmap.bin (FMH3) : codepoint -> indice empaquete `(rangee << 8) | colonne`
    la case : 32 x 32 pixels, PAS de 33 x 33, 62 colonnes

    py -3 tools/pictos_planche.py                 U+E000..U+E018, etiquetes
    py -3 tools/pictos_planche.py --plage E000 E033
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
CARTE = os.path.join(RACINE, 'extracted', 'fontmap.bin')
PLANCHE = os.path.join(RACINE, 'extracted', '2d', 'spr_n_fnt32_tex00.png')
SORTIE = os.path.join(RACINE, 'analysis', 'pictos_fnt32.png')

CASE = 32                       # le glyphe
PAS = 33                        # le pas entre deux cases

# Les noms que la table d'echappements du moteur (0x18053428E) donne a chaque
# glyphe. Releves dans le binaire, pas devines.
NOMS = {
    0xE000: 'ESC_BTN_CIRCLE', 0xE001: 'ESC_BTN_CROSS',
    0xE002: 'ESC_BTN_TRIANGLE', 0xE003: 'ESC_BTN_SQUARE',
    0xE004: 'ESC_BTN_START', 0xE006: 'ESC_BTN_SELECT',
    0xE008: 'ESC_BTN_L1', 0xE00A: 'ESC_BTN_L2',
    0xE00C: 'ESC_BTN_R1', 0xE00E: 'ESC_BTN_R2',
    0xE010: 'ESC_BTN_L3', 0xE012: 'ESC_BTN_R3',
    0xE014: '(croix directionnelle ?)',
    0xE015: 'ESC_BTN_CIRCLE_PS3', 0xE016: 'ESC_BTN_CROSS_PS3',
    0xE017: 'ESC_BTN_TRIANGLE_PS3', 0xE018: 'ESC_BTN_SQUARE_PS3',
}


def lire_carte():
    """La police 0 de `fontmap.bin` : codepoint -> (page, indice)."""
    d = open(CARTE, 'rb').read()
    if d[:4] != b'FMH3':
        raise SystemExit('%s n est pas un FMH3' % CARTE)
    tete = struct.unpack_from('<I', d, 0x10)[0]
    cols = struct.unpack_from('<I', d, tete + 0x10)[0]
    n = struct.unpack_from('<I', d, tete + 0x14)[0]
    tbl = struct.unpack_from('<I', d, tete + 0x18)[0]
    g = {}
    for k in range(n):
        o = tbl + 8 * k
        cp, page, idx = struct.unpack_from('<HHH', d, o)
        g[cp] = (page, idx)
    return cols, g


def main(argv):
    d, f = 0xE000, 0xE018
    if '--plage' in argv:
        i = argv.index('--plage')
        d, f = int(argv[i + 1], 16), int(argv[i + 2], 16)
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        raise SystemExit('Pillow manque : py -3 -m pip install pillow')
    if not os.path.exists(PLANCHE):
        raise SystemExit('%s manque -- lancer d abord '
                         'py -3 tools/txp.py --sortir spr_n_fnt32' % PLANCHE)
    cols, g = lire_carte()
    src = Image.open(PLANCHE).convert('RGBA')

    liste = [cp for cp in range(d, f + 1) if cp in g]
    manquants = [cp for cp in range(d, f + 1) if cp not in g]
    if manquants:
        print('absents de fontmap : ' + ' '.join('U+%04X' % c
                                                 for c in manquants))

    # UNE GRILLE, pas une bande : les cinquante et un pictos tiennent sur
    # quatre rangees de treize, chacun etiquete de son codepoint et de la case
    # que `fontmap` lui donne. C est l inventaire, pas une selection -- c est a
    # Frederic de nommer ce qu il voit.
    ech, pas_x, pas_y, par_rang = 4, 150, CASE * 4 + 46, 13
    rangs = (len(liste) + par_rang - 1) // par_rang
    out = Image.new('RGBA', (pas_x * min(par_rang, len(liste)), pas_y * rangs),
                    (24, 24, 32, 255))
    dr = ImageDraw.Draw(out)
    for k, cp in enumerate(liste):
        page, idx = g[cp]
        rang, col = idx >> 8, idx & 0xFF
        x, y = col * PAS, rang * PAS
        case = src.crop((x, y, x + CASE, y + CASE))
        case = case.resize((CASE * ech, CASE * ech), Image.NEAREST)
        cx = (k % par_rang) * pas_x
        cy = (k // par_rang) * pas_y
        ox = cx + (pas_x - CASE * ech) // 2
        for yy in range(0, CASE * ech, 16):
            for xx in range(0, CASE * ech, 16):
                t = 90 if ((xx // 16 + yy // 16) % 2) else 60
                dr.rectangle([ox + xx, cy + 8 + yy, ox + xx + 15,
                              cy + 8 + yy + 15], fill=(t, t, t, 255))
        out.alpha_composite(case, (ox, cy + 8))
        dr.text((cx + 8, cy + CASE * ech + 12), 'U+%04X' % cp,
                fill=(255, 255, 255, 255))
        dr.text((cx + 8, cy + CASE * ech + 24), 'r%d c%d' % (rang, col),
                fill=(150, 150, 160, 255))
        nom = NOMS.get(cp, '')
        dr.text((cx + 8, cy + CASE * ech + 36), nom[:22],
                fill=(170, 200, 255, 255))
        print('U+%04X  rangee %2d colonne %2d  %s' % (cp, rang, col, nom))
    out.save(SORTIE)
    print('%s  (%d x %d)' % (SORTIE, out.width, out.height))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
