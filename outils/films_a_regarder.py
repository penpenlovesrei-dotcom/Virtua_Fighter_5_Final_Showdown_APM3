#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rendre les films regardables dans VLC, sans copier un octet.

POURQUOI CA MARCHE, et c est mesure : un `.sfd` Sofdec1 EST un flux de
programme MPEG-1. Ses deux premiers en-tetes le disent --

    00 00 01 BA   pack header
    00 00 01 BB   system header

VLC le lit donc tel quel ; il ne bute que sur l EXTENSION. On pose a cote un
**lien dur** en `.mpg` : le meme fichier sous deux noms, zero octet de plus.

CE QU ON ENTENDRA : rien. Le son d un `.sfd` est de l **ADX** de CRI, range
dans un flux prive que VLC ne decode pas. L image suffit a reconnaitre un film
et a le nommer -- c est tout ce qu on demande ici.

Les liens vont dans `MOVIES/A_REGARDER/`. Les refaire est sans effet : un lien
deja pose est laisse tel quel.

    py -3 tools/films_a_regarder.py              les films de /tv/ de VF5 R
    py -3 tools/films_a_regarder.py --tous       tous les .sfd de l atelier
    py -3 tools/films_a_regarder.py --retirer
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
SOURCES = (os.path.join(RACINE, 'extracted', 'VF5R_movies'),
           os.path.join(RACINE, 'MOVIES'))
SORTIE = os.path.join(RACINE, 'MOVIES', 'A_REGARDER')

# Ce que chaque film dure, pour s y retrouver dans l explorateur. Mesure par
# `tools/sfd_inventaire.py`, pas estime.
DUREES = {
    'vd_RikoReis_00': '3 min 39', 'vd_VF5RReis_00': '2 min 59',
    'vd_RikoDesi_00': '2 min 29', 'vd_RikoVFNT_00': '2 min 07',
    'vd_RikoTmnl_00': '1 min 58', 'vd_RikoVSmv_00': '1 min 58',
    'cm_VER_R_00': '53 s', 'bngf_hp_01': '19 s',
    'ec_00000000_00': '4 s', 'ec_00000000_01': '4 s',
    'ec_00000000_02': '4 s',
}


def main(argv):
    if '--retirer' in argv:
        if not os.path.isdir(SORTIE):
            print('rien a retirer')
            return 0
        for n in os.listdir(SORTIE):
            os.remove(os.path.join(SORTIE, n))
        os.rmdir(SORTIE)
        print('%s retire -- aucun film n a ete touche, ce n etaient que des '
              'liens.' % SORTIE)
        return 0

    tous = '--tous' in argv
    os.makedirs(SORTIE, exist_ok=True)
    n = 0
    for dossier in SOURCES:
        if not os.path.isdir(dossier):
            continue
        for nom in sorted(os.listdir(dossier)):
            if not nom.lower().endswith('.sfd'):
                continue
            base = nom[:-4]
            if not tous and base not in DUREES:
                continue
            cible = os.path.join(SORTIE, base + '.mpg')
            if os.path.exists(cible):
                print('   deja la : %s' % os.path.basename(cible))
                n += 1
                continue
            source = os.path.join(dossier, nom)
            try:
                os.link(source, cible)
            except OSError as ex:
                # un lien dur demande le MEME volume ; sinon on le dit, on ne
                # copie pas 850 Mo dans le dos de personne.
                print('   LIEN IMPOSSIBLE pour %s : %s' % (nom, ex))
                continue
            n += 1
            print('   %-22s %s' % (base + '.mpg', DUREES.get(base, '')))
    print()
    print('%d film(s) dans %s' % (n, SORTIE))
    print('Ouvrez-les dans VLC. L image seule : le son est de l ADX, que VLC')
    print('ne decode pas -- c est sans importance pour les reconnaitre.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
