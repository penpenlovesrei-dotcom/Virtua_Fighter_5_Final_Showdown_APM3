#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Vidage d'une plage de VA en qwords, avec resolution des pointeurs.

Chaque qword est affiche brut ; s'il tombe dans une section du module, on
indique la section, et s'il pointe sur du texte imprimable on le cite. C'est
l'outil qui manquait pour lire une TABLE DE DESCRIPTEURS (le piege maison :
prendre une suite reguliere pour une table identifiee -- ici on voit les
chaines, donc on peut nommer les champs).

    py -3 tools/hexva.py 0x1804056C0 0x180405900
    py -3 tools/hexva.py 0x1804056C0 --n 56          56 qwords
    py -3 tools/hexva.py 0x1804056C0 0x180405900 --pas 0x1C0   une ligne par
        enregistrement de 0x1C0 octets (affiche seulement le premier qword)
"""
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                          # noqa: E402
import struct                                                  # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')


def texte(img, va, n=80):
    raw = img.read(va, n)
    if not raw:
        return None
    m = re.match(rb'[\x20-\x7e]{2,%d}' % n, raw)
    return m.group().decode('latin1') if m else None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__)
        return 1
    chemin = MOTEUR + ('' if '--patche' in sys.argv else '.origine')
    img = P.Image(chemin)
    lo = int(args[0], 0)
    if '--n' in sys.argv:
        hi = lo + 8 * int(sys.argv[sys.argv.index('--n') + 1], 0)
    else:
        hi = int(args[1], 0)
    for va in range(lo, hi, 8):
        off = img.va2off(va)
        if off is None:
            print('0x%X  (hors sections)' % va)
            continue
        q = struct.unpack_from('<Q', img.data, off)[0]
        d0, d1 = q & 0xFFFFFFFF, q >> 32
        note = ''
        s = img.sec_of(q) if q else None
        if s:
            t = texte(img, q)
            note = '-> [%s]' % s['name'] + ('  "%s"' % t if t else '')
        print('0x%X  %016X   %10d %10d  %s'
              % (va, q, d0 if d0 < 2**31 else d0 - 2**32,
                 d1 if d1 < 2**31 else d1 - 2**32, note))
    return 0


if __name__ == '__main__':
    sys.exit(main())
