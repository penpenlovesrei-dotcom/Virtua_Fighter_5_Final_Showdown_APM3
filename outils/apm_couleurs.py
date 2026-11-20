#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""LES COULEURS DE L'INTERFACE APM3 -- mesurees dans les materiaux.

POURQUOI ON NE PEUT PAS LES PRENDRE SUR LES IMAGES. Les panneaux de l'ecran
(`GameSelect.Design`) sont des **Material**, pas des dessins : leurs textures
sont des masques BLANCS, teintes a l'execution. Preleve sur le PNG, on ne
recolte donc que du #FFFFFF. Seules les fleches et le bouton de lecture ont
leur rose cuit dans l'image (#EB407B).

OU SONT-ELLES ALORS. Dans le bloc `m_SavedProperties` de chaque Material, qui
garde une table `m_Colors` : le NOM de la propriete y est ecrit en clair --
`_Color`, `_EmissionColor` -- meme dans un build de sortie sans arbre de
types. C'est la seule chose nommee du fichier, et elle suffit.

LE FORMAT, pour qui reprendra. Une chaine Unity est un entier 32 bits de
longueur suivi des octets, le tout aligne sur 4. Une couleur est quatre
flottants r, v, b, a. Une entree de la table vaut donc :

    [longueur][nom][bourrage jusqu'a 4][r][v][b][a]

    py -3 tools/apm_couleurs.py
"""
import os
import struct
import sys

BASE = os.path.join('C:' + os.sep, 'Users', 'frede', 'Desktop',
                    'VF5 FS DECOMP', 'APM_V1.04_internal_0')
FICHIERS = ['Apmv3System_Data/sharedassets0.assets',
            'Apmv3System_Data/globalgamemanagers.assets',
            'Apmv3System_Data/resources.assets']
NOMS = [b'_Color', b'_EmissionColor', b'_TintColor', b'_SpecColor']


def plausible(v):
    """Un composant de couleur Unity vit entre 0 et 1 (HDR : jusqu'a 8)."""
    return -0.001 <= v <= 8.0


def couleurs(donnees):
    """Rend (nom, r, v, b, a, offset) pour chaque entree lisible."""
    sortie = []
    for nom in NOMS:
        i = 0
        while True:
            j = donnees.find(nom, i)
            if j < 0:
                break
            i = j + 1
            # La longueur precede le nom.
            if j < 4:
                continue
            lg = struct.unpack('<i', donnees[j - 4:j])[0]
            if lg != len(nom):
                continue
            fin = j + len(nom)
            fin += (-fin) % 4                       # alignement sur 4
            if fin + 16 > len(donnees):
                continue
            r, v, b, a = struct.unpack('<ffff', donnees[fin:fin + 16])
            if not all(plausible(x) for x in (r, v, b, a)):
                continue
            sortie.append((nom.decode(), r, v, b, a, j))
    return sortie


def hexa(r, v, b):
    q = lambda x: max(0, min(255, int(round(x * 255.0))))
    return '#%02X%02X%02X' % (q(r), q(v), q(b))


def main():
    total = 0
    vues = {}
    for rel in FICHIERS:
        p = os.path.join(BASE, rel.replace('/', os.sep))
        if not os.path.exists(p):
            continue
        d = open(p, 'rb').read()
        trouvees = couleurs(d)
        if not trouvees:
            continue
        print('=' * 68)
        print(os.path.basename(p))
        print('=' * 68)
        for nom, r, v, b, a, off in trouvees:
            total += 1
            cle = (hexa(r, v, b), round(a, 3))
            vues[cle] = vues.get(cle, 0) + 1
            print('  0x%08X  %-14s %s  alpha %.3f   (%.3f %.3f %.3f)'
                  % (off, nom, hexa(r, v, b), a, r, v, b))
        print()

    if not total:
        print('Aucune couleur lisible.')
        return 1
    print('-' * 68)
    print('  %d entree(s), %d couleur(s) distincte(s) :' % (total, len(vues)))
    for (h, a), n in sorted(vues.items(), key=lambda kv: -kv[1]):
        print('     %s  alpha %-6s  vue %d fois' % (h, a, n))
    print('-' * 68)
    return 0


if __name__ == '__main__':
    sys.exit(main())
