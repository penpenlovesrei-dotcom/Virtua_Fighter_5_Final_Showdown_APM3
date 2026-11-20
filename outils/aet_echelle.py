#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REMETTRE A L ECHELLE LES CALQUES D UNE PLANCHE AGRANDIE.

CE QUE L ESSAI DU 2026-10-12 A MONTRE, et c est une mesure, pas un calcul.
`spr_n_adv__tex01` et `tex03` ont ete posees en 4x. Sans rien toucher d autre,
le logo AM2 s affiche **quatre fois trop grand ET decale** : son coin
haut-gauche n a pas bouge, sa taille a quadruple. Les deux consequences se
lisent dans la formule de placement, mesuree dans `tools/aet.py` :

    ecran = position + (pixel - origine) x echelle

  . la taille du quad vient du RECTANGLE EN PIXELS DU SPRITE, pas du champ
    `largeur/hauteur` de la surface AET -- qui, lui, n a pas bouge et n a rien
    change ;
  . `origine` est en pixels de la surface : restee a (240, 176) devant une
    image qui en fait maintenant 1920 x 1408, elle ancre l image a son
    HUITIEME, d ou le decalage.

D OU LE CORRECTIF, et il tient en deux reglages par calque :

    echelle  /= F        rend la taille d affichage
    origine  *= F        remet l ancre au meme point de l image
    position    inchangee

LE PARTAGE DES VALEURS EST VERIFIE AVANT D ECRIRE. L ecrivain AET met en
commun les flottants identiques -- la rotation de dix calques peut tenir en
UNE adresse. Ecrire sans regarder changerait des calques qu on ne vise pas.
L outil refuse si une adresse qu il s apprete a toucher sert aussi a un calque
hors de la selection.

LA CORRESPONDANCE SURFACE -> TEXTURE passe par la TAILLE : une surface AET de
480 x 352 est le sprite de 480 x 352 du jeu de sprites, dont l enregistrement
porte l indice de texture. On lit donc le `.farc` **D ORIGINE** (celui que
`textures_hd.py --poser` a mis de cote), puisque dans le posé les rectangles
ont deja ete multiplies. Toute taille ambigue -- deux sprites de meme taille
sur DEUX textures differentes -- fait refuser.

    py -3 tools/aet_echelle.py <aet.bin> --spr <spr.farc> --texture 1 3
                               --facteur 4 [--essai]
    py -3 tools/aet_echelle.py <aet.bin> --rendre
"""
import os
import shutil
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import aet as mod_aet                                        # noqa: E402
import farc as mfarc                                         # noqa: E402

SPR_NSPR, SPR_OFS, SPR_PAS = 0x0C, 0x10, 0x28


def tailles_par_texture(chemin_spr):
    """{(largeur, hauteur): {indices de texture}} depuis le jeu de sprites."""
    origine = chemin_spr + '.origine'
    source = origine if os.path.exists(origine) else chemin_spr
    f = mfarc.Farc(source)
    membre = None
    for e in f.entries:
        if e['name'].endswith('.bin'):
            membre = e
            break
    if membre is None:
        raise SystemExit('%s : aucun membre .bin' % source)
    d = f.read(membre)
    n, = struct.unpack_from('<I', d, SPR_NSPR)
    ofs, = struct.unpack_from('<I', d, SPR_OFS)
    out = {}
    for i in range(n):
        o = ofs + SPR_PAS * i
        tex, = struct.unpack_from('<i', d, o)
        w, h = struct.unpack_from('<2f', d, o + 0x20)
        out.setdefault((int(round(w)), int(round(h))), set()).add(tex)
    return out, os.path.basename(source)


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    chemin = argv[0]
    origine = chemin + '.origine'

    if '--rendre' in argv:
        if not os.path.exists(origine):
            print('%s : pas d origine gardee, rien a rendre'
                  % os.path.basename(chemin))
            return 1
        os.remove(chemin)
        os.rename(origine, chemin)
        print('rendu : %s' % os.path.basename(chemin))
        return 0

    if '--spr' not in argv or '--facteur' not in argv:
        print(__doc__)
        return 1
    chemin_spr = argv[argv.index('--spr') + 1]
    facteur = float(argv[argv.index('--facteur') + 1])
    textures = set()
    if '--texture' in argv:
        for a in argv[argv.index('--texture') + 1:]:
            if not a.lstrip('-').isdigit():
                break
            textures.add(int(a))
    if not textures:
        print('--texture attend au moins un indice')
        return 1
    essai = '--essai' in argv

    par_taille, nom_spr = tailles_par_texture(chemin_spr)
    print('jeu de sprites lu : %s' % nom_spr)

    # On lit TOUJOURS l etat d origine : relancer l outil ne doit pas
    # multiplier deux fois.
    source = origine if os.path.exists(origine) else chemin
    a = mod_aet.Aet(source)

    vises, autres = [], []
    for p in a.scenes():
        if not a.tient(p, 0x38):
            continue
        sc = a.scene(p)
        surf = {s['offset']: s for s in a.surfaces(sc)}
        for i, (n, ptr) in enumerate(a.compositions(sc)):
            for c in a.calques(n, ptr):
                t = a.transforme(c['video'])
                if t is None:
                    continue
                s = surf.get(c['element']) if c['type'] == 1 else None
                tex = (par_taille.get((s['largeur'], s['hauteur']))
                       if s else None)
                if s and tex and len(tex) > 1 and (tex & textures):
                    print('REFUS : la taille %dx%d existe sur les textures %s '
                          '-- impossible de dire laquelle porte le calque %r.'
                          % (s['largeur'], s['hauteur'], sorted(tex), c['nom']))
                    return 2
                if s and tex and (tex & textures):
                    vises.append((sc['nom'], i, c, s, t))
                else:
                    autres.append(t)

    if not vises:
        print('aucun calque ne dessine les textures %s' % sorted(textures))
        return 1

    # --- LE PARTAGE : on ne touche rien qui serve ailleurs ----------------
    a_ecrire = set()
    for _, _, _, _, t in vises:
        for nom in ('Echelle.X', 'Echelle.Y', 'Origine.X', 'Origine.Y'):
            a_ecrire.add(t[nom]['ptr'])
    partagees = set()
    for t in autres:
        for nom in ('Echelle.X', 'Echelle.Y', 'Origine.X', 'Origine.Y',
                    'Position.X', 'Position.Y', 'Rotation', 'Opacite'):
            if t[nom]['ptr'] in a_ecrire:
                partagees.add(t[nom]['ptr'])
    if partagees:
        print('REFUS : %d valeur(s) sont PARTAGEES avec des calques hors de la '
              'selection : %s. L ecrivain AET met les flottants identiques en '
              'commun ; les ecrire ici changerait ces calques-la aussi.'
              % (len(partagees), ' '.join('0x%X' % x for x in
                                          sorted(partagees))))
        return 2

    d = bytearray(a.d)
    print('%d calque(s) vise(s), facteur %g :' % (len(vises), facteur))
    for nom_sc, i, c, s, t in vises:
        ech = (t['Echelle.X'], t['Echelle.Y'])
        org = (t['Origine.X'], t['Origine.Y'])
        if any(p['nombre'] != 1 for p in ech + org):
            print('   %-28s ANIMEE -- non traitee (echelle ou origine a '
                  'plusieurs cles)' % c['nom'])
            continue
        print('   %-28s %4dx%-5d  echelle %g -> %g   origine (%g, %g) -> '
              '(%g, %g)'
              % (c['nom'], s['largeur'], s['hauteur'],
                 ech[0]['valeur'], ech[0]['valeur'] / facteur,
                 org[0]['valeur'], org[1]['valeur'],
                 org[0]['valeur'] * facteur, org[1]['valeur'] * facteur))
        if essai:
            continue
        for p in ech:
            struct.pack_into('<f', d, p['ptr'], p['valeur'] / facteur)
        for p in org:
            struct.pack_into('<f', d, p['ptr'], p['valeur'] * facteur)

    if essai:
        print('(--essai : rien n a ete ecrit)')
        return 0
    if not os.path.exists(origine):
        shutil.copyfile(chemin, origine)
    tmp = chemin + '.neuf'
    with open(tmp, 'wb') as fp:
        fp.write(bytes(d))
    os.replace(tmp, chemin)
    print('%s reecrit (%d octets). L original est en %s'
          % (os.path.basename(chemin), len(d), os.path.basename(origine)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
