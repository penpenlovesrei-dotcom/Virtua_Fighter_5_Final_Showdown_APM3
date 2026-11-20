#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Bornes de fonctions (.pdata) dans une plage de VA.

    py -3 tools/bornes.py 0x180099000 0x1800A2000
    py -3 tools/bornes.py 0x180099426          (fonction contenant cette VA)

Rappel du chantier : une fonction reelle couvre souvent PLUSIEURS entrees
.pdata chainees. Les entrees adjacentes sont donc signalees par `+` quand
elles se touchent (fin de l'une == debut de la suivante).
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                          # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')


def main():
    chemin = MOTEUR + ('' if '--patche' in sys.argv else '.origine')
    img = P.Image(chemin)
    fs = P.runtime_functions(img)
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) == 1:
        va = int(args[0], 0)
        lo, hi = va - 0x40, va + 0x40
    else:
        lo, hi = int(args[0], 0), int(args[1], 0)
    prec_fin = None
    for a, b in fs:
        if b <= lo or a >= hi:
            continue
        colle = '+' if prec_fin == a else ' '
        print('%s 0x%X - 0x%X   (%d o)' % (colle, a, b, b - a))
        prec_fin = b
    return 0


if __name__ == '__main__':
    sys.exit(main())
