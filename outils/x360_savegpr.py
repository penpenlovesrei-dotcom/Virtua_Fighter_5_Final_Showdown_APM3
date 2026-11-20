#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Les routines `__savegprlr_N` / `__restgprlr_N` d'une image Xbox 360.

POURQUOI (2026-10-05). Pour importer une image PowerPC dans Ghidra, il faut
neutraliser ces deux routines par un « call fixup » (`SauvegardesX360.java`),
sinon le decompilateur coupe chaque fonction apres son prologue : Ghidra en
fait des fonctions qui ne reviennent pas, et tout ce qui suit l'appel est
perdu.

Les adresses de la console de 2007 sont consignees (0x825FFA10..0x825FFA4C et
0x825FFA60..0x825FFA9C) ; celles de la Final Showdown console ne l'etaient
pas, et on ne les recopie pas d'une image a l'autre -- chaque build a les
siennes.

COMMENT ON LES TROUVE, sans rien supposer. Ces routines sont UNE SUITE de
`std rN, -M(r1)` (resp. `ld rN, -M(r1)`) ou l'appelant entre a la ligne du
premier registre a sauver. On cherche donc la plus longue suite
d'instructions consecutives de cette forme. Encodage, gros-boutien :

    std rS, D(rA)   opcode 62, forme DS : 111110 SSSSS AAAAA DD..DD 00
    ld  rT, D(rA)   opcode 58, meme forme

On n'accepte qu'un `rA = 1` (la pile) et un deplacement NEGATIF, et on exige
une suite d'au moins huit : aucune fonction ordinaire n'empile huit registres
d'affilee par cette forme sans rien faire entre.

Usage :
    py -3 tools/x360_savegpr.py
    py -3 tools/x360_savegpr.py --image <autre.img>
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import x360_ppc as X                                         # noqa: E402

MINI = 8          # longueur minimale d'une suite retenue


def suites(img, opcode):
    """[(debut, fin, nombre)] des suites de `std`/`ld` sur r1, deplacement < 0."""
    out = []
    for s in img.secs:
        if not s.get('exec'):
            continue
        va0, n = s['va'], s['vsize']
        o0 = va0 - img.base
        debut, compte = None, 0
        for k in range(0, n - 3, 4):
            mot, = struct.unpack_from('>I', img.d, o0 + k)
            ok = False
            if (mot >> 26) == opcode:
                ra = (mot >> 16) & 0x1F
                d = mot & 0xFFFC
                if ra == 1 and (d & 0x8000):        # r1 et deplacement negatif
                    ok = True
            if ok:
                if debut is None:
                    debut, compte = va0 + k, 0
                compte += 1
            else:
                if debut is not None and compte >= MINI:
                    out.append((debut, va0 + k, compte))
                debut, compte = None, 0
        if debut is not None and compte >= MINI:
            out.append((debut, va0 + n, compte))
    return out


def main():
    a = sys.argv[1:]
    chemin = a[a.index('--image') + 1] if '--image' in a else X.IMAGE
    img = X.Image(chemin)
    print('image : %s  (base 0x%X)' % (os.path.basename(chemin), img.base))
    for opcode, nom in ((62, '__savegprlr (std)'), (58, '__restgprlr (ld)')):
        s = suites(img, opcode)
        s.sort(key=lambda t: -t[2])
        print()
        print('%s : %d suite(s) de %d instructions ou plus' % (nom, len(s), MINI))
        for debut, fin, compte in s[:4]:
            print('   0x%08X .. 0x%08X   %d instructions' % (debut, fin, compte))
            # les quatre instructions qui SUIVENT la suite : c'est la queue de
            # la routine (`stw r12,-8(r1) ; blr` ou `mtlr r12 ; blr`)
            for k in range(4):
                mot, = struct.unpack_from('>I', img.d, fin - img.base + 4 * k)
                print('        0x%08X  %08X' % (fin + 4 * k, mot))
    print()
    print('A passer a SauvegardesX360.java : <debut sauve> <fin sauve> '
          '<debut rest> <fin rest>')
    return 0


if __name__ == '__main__':
    sys.exit(main())
