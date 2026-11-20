#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Toutes les adresses de code citees par la documentation et les outils.

Sert de DENOMINATEUR honnete : au lieu de dire « on a bien avance », on
compte combien de fonctions du binaire sont touchees par au moins une
adresse citee quelque part. Le fichier produit se donne ensuite a
`CouvVF5.java`, qui resout chaque adresse en fonction et somme les tailles.

    py -3 mesures/extraire_adresses.py adresses.txt            le moteur
    py -3 mesures/extraire_adresses.py adresses.txt --exe       vfes.exe
    py -3 mesures/extraire_adresses.py adresses.txt --x360      PowerPC

Deux groupes sont ecrits : TOUT (toute citation, dans n'importe quel
fichier) puis DOCS (uniquement les .md -- le savoir redige). L'ecart
entre les deux mesure ce qui a ete regarde sans etre explique.
"""
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)

# (motif d'adresse, borne basse, borne haute) -- les bornes sont celles de
# la section .text, relevees dans l'en-tete PE de chaque binaire.
PLAGES = {
    'moteur': (r'0x(18[0-9A-Fa-f]{7})', 0x180001000, 0x180346000),
    'exe': (r'0x(140[0-9A-Fa-f]{5,6})', 0x140001000, 0x140134000),
    'x360': (r'0x(82[0-9A-Fa-f]{6})', 0x82000000, 0x83000000),
}
EXTS = ('.md', '.c', '.h', '.py', '.java', '.txt', '.json', '.csv')


def main():
    av = sys.argv[1:]
    if not av or av[0].startswith('--'):
        print(__doc__)
        return 1
    sortie = av[0]
    quoi = 'exe' if '--exe' in av else ('x360' if '--x360' in av else 'moteur')
    motif, bas, haut = PLAGES[quoi]
    pat = re.compile(motif)

    tout, docs = {}, {}
    for r, ds, fs in os.walk(RACINE):
        ds[:] = [d for d in ds if d not in ('projet', 'binaires')]
        for fn in fs:
            if not fn.lower().endswith(EXTS):
                continue
            p = os.path.join(r, fn)
            try:
                t = open(p, encoding='utf-8', errors='replace').read()
            except Exception:
                continue
            for m in pat.finditer(t):
                a = int(m.group(1), 16)
                if not (bas <= a < haut):
                    continue
                tout[a] = 1
                if fn.lower().endswith('.md'):
                    docs[a] = 1
    with open(sortie, 'w') as f:
        f.write('TOUT\n')
        for a in sorted(tout):
            f.write('%x\n' % a)
        f.write('DOCS\n')
        for a in sorted(docs):
            f.write('%x\n' % a)
    print('%s : %d adresses dans .text, dont %d citees par un .md'
          % (quoi, len(tout), len(docs)))
    print('ecrit dans %s' % sortie)
    return 0


if __name__ == '__main__':
    sys.exit(main())
