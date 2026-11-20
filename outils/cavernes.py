#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Les bourrages `int3` libres de `.text`, PROUVES libres.

MSVC aligne ses fonctions a 16 octets et remplit l'ecart avec 0xCC. Une plage
n'est utilisable que si l'on peut demontrer qu'elle n'appartient a aucune
fonction. Trois conditions, toutes verifiees ici :

  1. la plage n'est que des 0xCC ;
  2. elle ne tombe dans AUCUNE des entrees de `.pdata` ;
  3. elle finit sur une frontiere de 16 octets (c'est bien du bourrage
     d'alignement, pas le ventre d'une fonction feuille absente de `.pdata`).

La condition 3 est la plus importante : les FEUILLES ne sont pas dans `.pdata`
(piege paye plusieurs fois sur ce chantier), donc « absent de .pdata » ne suffit
pas. Une plage de 0xCC qui se termine pile sur un multiple de 16 et qui est
suivie d'un octet non-0xCC est du bourrage.

    py -3 tools/cavernes.py --min 20
    py -3 tools/cavernes.py --min 20 --autour 0x1800B8AFA --portee 0x40000
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                          # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')

# Cavernes deja prises par patch_moteur.py -- ne pas les proposer.
PRISES = [
    (0x18034575C, 0x180345800), (0x1801A7C89, 0x1801A7CDB),
    (0x1801A703D, 0x1801A707D), (0x1801A71D8, 0x1801A71FC),
    (0x1802786EB, 0x180278720), (0x18027718B, 0x1802771C0),
    (0x1802758DB, 0x180275910),
]


def dans_pdata(fs, a, b):
    for x, y in fs:
        if a < y and x < b:
            return True
    return False


def main():
    mini = 20
    if '--min' in sys.argv:
        mini = int(sys.argv[sys.argv.index('--min') + 1], 0)
    autour = portee = None
    if '--autour' in sys.argv:
        autour = int(sys.argv[sys.argv.index('--autour') + 1], 0)
        portee = 0x40000
        if '--portee' in sys.argv:
            portee = int(sys.argv[sys.argv.index('--portee') + 1], 0)
    img = P.Image(MOTEUR + '.origine')
    fs = P.runtime_functions(img)
    n = 0
    for s in img.secs:
        if not s['exec']:
            continue
        blob = img.data[s['off']:s['off'] + s['rsize']]
        i = 0
        L = len(blob)
        while i < L:
            if blob[i] != 0xCC:
                i += 1
                continue
            j = i
            while j < L and blob[j] == 0xCC:
                j += 1
            a, b = s['va'] + i, s['va'] + j
            i = j
            if b - a < mini:
                continue
            if b % 16 != 0:
                continue
            if dans_pdata(fs, a, b):
                continue
            if any(a < y and x < b for x, y in PRISES):
                continue
            if autour is not None and abs(a - autour) > portee:
                continue
            print('0x%X - 0x%X   %d octets' % (a, b, b - a))
            n += 1
    print('== %d caverne(s) >= %d octets' % (n, mini))
    return 0


if __name__ == '__main__':
    sys.exit(main())
