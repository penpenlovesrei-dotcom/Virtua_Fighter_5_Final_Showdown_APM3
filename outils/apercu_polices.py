#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES POLICES DU MOTEUR, LISTEES ET DESSINEES.

MESURE DU 2026-10-12. Le moteur n'a pas « des polices » quelque part : il en a
EXACTEMENT TROIS, et le selecteur le dit en quatre instructions
(`0x180199FB0`) :

    xor eax, eax
    cmp ecx, 3          <- l identifiant est borne a TROIS
    cmovb eax, ecx      <- tout ce qui depasse retombe sur 0
    lea rcx, [rax+rax*2] ; mov rax, [0x180750FF8] ; lea rax, [rax+rcx*8]
    add rax, 0x98       <- enregistrements de 24 octets, a partir de +0x98

Et c'est `0x180199B70`, l'initialiseur du gestionnaire, qui les construit : il
fabrique TROIS objets de 0x40 octets (`0x1802FE160(ptr, 0x40, 3, ...)`) et
appelle `0x18019A740` sur chacun. Les champs se lisent dans cette fonction :

    [+0x00] identifiant   [+0x04] [+0x05] la CASE, en pixels
    [+0x06] [+0x07] la CHASSE                   [+0x0C] la TEXTURE (-1 = aucune)

d'ou le tableau, releve sur les trois appels :

    id 0   0x18F  (399)      case 10 x 16   chasse 10 x 16   texture -1
    id 1   0xD30D (54 029)   case 32 x 32   chasse 33 x 33   texture  0
    id 2   0xD3DB (54 235)   case 48 x 48   chasse 48 x 48   texture  1

Les deux dernieres sont EXACTEMENT les deux polices que `fontmap.bin` decrit
(`tools/echappements.py --fontmap`) : 32/33 avec 62 colonnes et 3669 glyphes,
48/48 avec 21 colonnes et 127 glyphes. Les textures 0 et 1 sont celles de
`spr_n_fnt32`.

COMMENT ON EN CHOISIT UNE. `0x18019B6F0(style, id)` n'est pas « le mode »,
comme le disait le dossier : c'est LE SELECTEUR DE POLICE. Il appelle
`0x180199FB0(id)`, ecrit l'identifiant en `style+0x00`, et en tire les
metriques et les echelles. Le constructeur de style `0x18019A9D0` l'appelle
avec zero : **la police par defaut est la 0**.

    py -3 tools/apercu_polices.py                 le tableau
    py -3 tools/apercu_polices.py <mot>           et le mot dessine dans
                                                  chacune des deux planches
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import echappements                                          # noqa: E402

PLANCHES = os.path.join(RACINE, 'HD_TEXTURES', 'EXTRACTED', '2D')
SORTIE = os.path.join(RACINE, 'analysis', '_apercu_polices.png')

# Les trois enregistrements, releves dans `0x180199B70`. L'ordre est celui des
# identifiants que `0x18019B6F0` accepte.
POLICES = [
    dict(id=0, ident=0x18F, case=(10, 16), chasse=(10, 16), texture=-1,
         note='la petite police interne : aucune texture de planche'),
    dict(id=1, ident=0xD30D, case=(32, 32), chasse=(33, 33), texture=0,
         note='3669 glyphes, pictos de manette compris (rangees 56 et 57)'),
    dict(id=2, ident=0xD3DB, case=(48, 48), chasse=(48, 48), texture=1,
         note='127 glyphes : ASCII seul, AUCUN picto -- celle du texte des '
              'variantes'),
]


def fontmap_polices():
    """Rend [(case, chasse, colonnes, {codepoint: (rangee, colonne)})]."""
    fm = echappements.fontmap()
    n, = struct.unpack_from('<I', fm, 8)
    liste, = struct.unpack_from('<I', fm, 0x0C)
    out = []
    for i in range(n):
        p, = struct.unpack_from('<I', fm, liste + 4 * i)
        cw, ch, aw, ah = fm[p + 4], fm[p + 5], fm[p + 6], fm[p + 7]
        cols, = struct.unpack_from('<I', fm, p + 0x10)
        nglyphes, = struct.unpack_from('<I', fm, p + 0x14)
        table, = struct.unpack_from('<I', fm, p + 0x18)
        g = {}
        for k in range(nglyphes):
            o = table + 8 * k
            cp, _tex, idx = struct.unpack_from('<HHH', fm, o)
            g[cp] = (idx >> 8, idx & 0xFF)
        out.append(((cw, ch), (aw, ah), cols, g))
    return out


def dessiner(mot):
    from PIL import Image
    polices = fontmap_polices()
    lignes = []
    for rang, ((cw, ch), (aw, ah), cols, g) in enumerate(polices):
        # fontmap 0 -> texture 0 (police id 1) ; fontmap 1 -> texture 1 (id 2)
        f = os.path.join(PLANCHES, 'spr_n_fnt32__tex%02d.png' % rang)
        if not os.path.exists(f):
            print('   %s manque -- py -3 tools/textures_hd.py --sortir' % f)
            continue
        planche = Image.open(f).convert('RGBA')
        im = Image.new('RGBA', (aw * len(mot), ch), (0, 0, 0, 0))
        x = 0
        for ch_ in mot:
            cp = ord(ch_)
            if cp not in g:
                x += aw
                continue
            r, c = g[cp]
            boite = (c * aw, r * ah, c * aw + cw, r * ah + ch)
            im.paste(planche.crop(boite), (x, 0))
            x += aw
        lignes.append((rang, im))
    if not lignes:
        return
    # Fond sombre, et chaque mot a sa taille NATIVE puis ramene a la meme
    # hauteur, pour qu'on compare le dessin et non la taille.
    h_cible = max(im.height for _, im in lignes)
    larg = max(im.width for _, im in lignes)
    for _, im in lignes:
        larg = max(larg, int(im.width * h_cible / float(im.height)))
    out = Image.new('RGB', (larg + 20, (h_cible * 2 + 30) * len(lignes)),
                    (24, 24, 24))
    y = 10
    for rang, im in lignes:
        out.paste(im, (10, y), im)
        y += h_cible + 10
        f = h_cible / float(im.height)
        g2 = im.resize((int(im.width * f), h_cible), Image.LANCZOS)
        out.paste(g2, (10, y), g2)
        y += h_cible + 20
    out.save(SORTIE)
    print('ecrit : %s' % SORTIE)
    print('  (pour chaque planche : taille native, puis ramenee a la meme '
          'hauteur)')


def main(argv):
    print('LES TROIS POLICES DU MOTEUR')
    print('%-4s %-10s %-12s %-12s %-9s %s'
          % ('id', 'identifiant', 'case', 'chasse', 'texture', 'ce que c est'))
    for p in POLICES:
        print('%-4d 0x%-8X %-12s %-12s %-9s %s'
              % (p['id'], p['ident'],
                 '%d x %d' % p['case'], '%d x %d' % p['chasse'],
                 'aucune' if p['texture'] < 0 else str(p['texture']),
                 p['note']))
    print()
    for (cw, ch), (aw, ah), cols, g in fontmap_polices():
        print('fontmap : case %dx%d, chasse %dx%d, %d colonnes, %d glyphes'
              % (cw, ch, aw, ah, cols, len(g)))
    if argv:
        print()
        dessiner(argv[0])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
