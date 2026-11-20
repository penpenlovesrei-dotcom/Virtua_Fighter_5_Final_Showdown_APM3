#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lit une vtable MSVC : ses creneaux, et ce que chaque creneau vise.

Le releve `rtti.py` ne montre que quatre creneaux et ne dit pas ou la table
s'arrete. Or les vtables voisines se touchent : lire quatre qwords a partir
d'une adresse donne parfois la fin de la table PRECEDENTE (piege paye le
2026-09-05 sur `LinkMainStateStartup`, dont le creneau [1] semblait etre une
autre fonction que celui de ses freres).

Cet outil rend, pour une plage de donnees :

  * chaque qword, avec la fonction visee et sa taille `.pdata` ;
  * les deux premiers octets de la cible, ce qui suffit a reconnaitre un
    `mov eax, N ; ret` (un identifiant d'etat) d'un vrai corps de fonction ;
  * la FRONTIERE des vtables : un qword qui pointe sur un
    CompleteObjectLocator ouvre une nouvelle table, et on la nomme.

Usage :
    py -3 tools/vtable.py 0x1805C6CF0 0x1805C7060
    py -3 tools/vtable.py 0x1805C6CF0 0x1805C7060 --patche
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import pe_disasm as P                                          # noqa: E402
import rtti                                                    # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')


def charger(chemin):
    img = P.Image(chemin)
    tds, cols, vtables = rtti.collecter(img)
    noms_col = {va: rtti.joli(tds[td]) for va, td in cols.items()}
    return img, noms_col


def resume_cible(img, va):
    """Premiere instruction de la cible, en clair, si c'est du code court."""
    o = img.va2off(va)
    if o is None:
        return None
    blob = img.data[o:o + 16]
    try:
        ins = list(img.md.disasm(blob, va))
    except Exception:
        return None
    txt = []
    for x in ins[:3]:
        txt.append('%s %s' % (x.mnemonic, x.op_str))
        if x.mnemonic == 'ret':
            break
    return ' ; '.join(txt)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    lo, hi = int(sys.argv[1], 0), int(sys.argv[2], 0)
    chemin = MOTEUR + ('' if '--patche' in sys.argv else '.origine')
    img, noms_col = charger(chemin)
    fs = P.runtime_functions(img)
    debuts = {a: b for a, b in fs}

    texte = img.sec_of(lo)
    creneau = 0
    for va in range(lo, hi, 8):
        q = img.read(va, 8)
        if len(q) < 8:
            break
        v = struct.unpack('<Q', q)[0]
        if v in noms_col:
            print()
            print('=== vtable 0x%X : %s' % (va + 8, noms_col[v]))
            creneau = 0
            print('  (COL 0x%X)' % v)
            continue
        s = img.sec_of(v) if v else None
        etiq = ''
        if s is not None and s['exec']:
            fin = debuts.get(v)
            taille = ('%d o' % (fin - v)) if fin else 'feuille'
            etiq = '  %-9s  %s' % (taille, resume_cible(img, v) or '')
        elif s is not None:
            etiq = '  [%s]' % s['name']
        print('  [%2d] 0x%X -> 0x%X%s' % (creneau, va, v, etiq))
        creneau += 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
