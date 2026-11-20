#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Comme `refs_lineaires.py`, mais pour PLUSIEURS cibles en UN seul balayage.

Le balayage lineaire de `.text` coute une trentaine de secondes ; le refaire
par cible rend impraticable l'etude d'un module entier. Ici on balaye une fois
et on teste toutes les cibles a chaque position.

    py -3 tools/refs_multi.py 0x180099340 0x180099390 0x1800993D0
    py -3 tools/refs_multi.py --plage 0x180098AF0 0x18009C500   toutes les
        fonctions .pdata de la plage, chacune avec ses appelants
    py -3 tools/refs_multi.py 0x1806F9418 --data     inclut les sections
        non executables (pointeurs, vtables)

Meme mise en garde que `refs_lineaires` : on ne se fie pas a `.pdata` pour
trouver les references, seulement pour NOMMER la fonction contenante.
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import pe_disasm as P                                          # noqa: E402
import refs_lineaires as R                                     # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')


def balayer(img, cibles, avec_data=False):
    """{cible: [(va, genre, texte), ...]} en un seul passage."""
    res = {c: [] for c in cibles}
    ens = set(cibles)
    secs = img.secs if avec_data else [s for s in img.secs if s['exec']]
    for s in secs:
        blob = img.data[s['off']:s['off'] + s['rsize']]
        base = s['va']
        n = len(blob)
        if s['exec']:
            for i in range(n - 4):
                b = blob[i]
                if b in (0xE8, 0xE9):
                    rel = struct.unpack_from('<i', blob, i + 1)[0]
                    t = base + i + 5 + rel
                    if t in ens:
                        res[t].append((base + i,
                                       'appel' if b == 0xE8 else 'saut', None))
                disp = struct.unpack_from('<i', blob, i)[0]
                if disp == 0:
                    continue
                for queue in (0, 1, 2, 4):
                    t = base + i + 4 + queue + disp
                    if t not in ens:
                        continue
                    ins = R.decoder_autour(img, base + i, t)
                    if ins is None:
                        continue
                    res[t].append((ins.address, 'rip',
                                   '%s %s' % (ins.mnemonic, ins.op_str)))
                    break
        for i in range(0, n - 8, 4):
            v = struct.unpack_from('<Q', blob, i)[0]
            if v in ens:
                res[v].append((base + i, 'ptr64[%s]' % s['name'], None))
    return res


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    chemin = MOTEUR + ('' if '--patche' in sys.argv else '.origine')
    img = P.Image(chemin)
    fs = P.runtime_functions(img)
    if '--plage' in sys.argv:
        lo, hi = int(args[0], 0), int(args[1], 0)
        cibles = [a for a, b in fs if lo <= a < hi]
    else:
        cibles = [int(a, 0) for a in args]
    if not cibles:
        print(__doc__)
        return 1
    res = balayer(img, cibles, avec_data='--data' in sys.argv)
    for c in cibles:
        hits = res[c]
        vus = set()
        propres = []
        for va, genre, txt in hits:
            if (va, genre) in vus:
                continue
            vus.add((va, genre))
            propres.append((va, genre, txt))
        propres.sort()
        print('== 0x%X : %d reference(s)' % (c, len(propres)))
        for va, genre, txt in propres:
            f = R.contenant(fs, va)
            print('   0x%-12X %-14s %-40s %s'
                  % (va, genre, txt or '',
                     ('dans 0x%X' % f) if f else '(hors .pdata)'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
