#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Sort les textures d'un decor en PNG, et en fait une PLANCHE CONTACT.

Un decor ne s'identifie ni a sa couleur de brouillard ni a un mot-cle : deux
erreurs deja payees. Quand les noms d'objets ne disent rien -- le `stgdur` de
VF5 ver.B n'a qu'un seul objet, `stgdur_gnd` -- il reste l'image.

    py -3 tools/textures_decor.py extracted/du_obj/stgdur/stgdur_tex.bin
    py -3 tools/textures_decor.py <tex.bin> --planche analysis/dur_verb.png
    py -3 tools/textures_decor.py <tex.bin> --min 512     grandes seulement

Le conteneur est le meme TXP que les planches 2D ; on reutilise `txp.py`.
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import txp                                                     # noqa: E402


def charger(chemin):
    d = open(chemin, 'rb').read()
    if d[:4] == b'FArC':
        morceaux = txp.defarc(chemin)
        d = b''.join(morceaux.values())
    return txp.textures(d)


def planche(images, chemin, colonnes=6, cote=256):
    from PIL import Image, ImageDraw
    if not images:
        print('aucune image a poser')
        return
    lignes = (len(images) + colonnes - 1) // colonnes
    marge = 18
    grande = Image.new('RGB', (colonnes * cote, lignes * (cote + marge)),
                       (24, 24, 24))
    dess = ImageDraw.Draw(grande)
    for k, (etiquette, im) in enumerate(images):
        c, li = k % colonnes, k // colonnes
        vignette = im.copy()
        vignette.thumbnail((cote, cote))
        x = c * cote + (cote - vignette.size[0]) // 2
        y = li * (cote + marge) + (cote - vignette.size[1]) // 2
        grande.paste(vignette, (x, y))
        dess.text((c * cote + 4, li * (cote + marge) + cote + 3), etiquette,
                  fill=(210, 210, 210))
    grande.save(chemin)
    print('planche : %s  (%d images, %dx%d)'
          % (chemin, len(images), grande.size[0], grande.size[1]))


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    mini = 0
    if '--min' in a:
        i = a.index('--min')
        mini = int(a[i + 1])
        del a[i:i + 2]
    sortie = None
    if '--planche' in a:
        i = a.index('--planche')
        sortie = a[i + 1]
        del a[i:i + 2]
    dossier = None
    if '--dossier' in a:
        i = a.index('--dossier')
        dossier = a[i + 1]
        del a[i:i + 2]
    chemin = a[0]
    ts = charger(chemin)
    print('%s : %d textures' % (os.path.basename(chemin), len(ts)))
    images = []
    for t in ts:
        nom = 'tex%03d %s %dx%d' % (
            t['i'], txp.FORMATS.get(t['format'], '?%d' % t['format']),
            t['larg'], t['haut'])
        if max(t['larg'], t['haut']) < mini:
            continue
        try:
            im = txp.image(t)
        except Exception as ex:                                # noqa: BLE001
            print('  %s -> ECHEC %s' % (nom, ex))
            continue
        images.append((nom, im))
        if dossier:
            os.makedirs(dossier, exist_ok=True)
            im.convert('RGB').save(
                os.path.join(dossier, 'tex%03d.png' % t['i']))
    print('  %d retenues (min %d)' % (len(images), mini))
    if sortie:
        planche(images, sortie)
    return 0


if __name__ == '__main__':
    sys.exit(main())
