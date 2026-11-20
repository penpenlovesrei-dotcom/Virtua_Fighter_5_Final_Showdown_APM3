#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Toutes les references a une PLAGE d'adresses, en un seul balayage.

`refs_lineaires.py` cherche UNE adresse. Une table, elle, ne se reference pas
qu'a son premier octet : le moteur y entre par `table + index*pas`, par
`table + 0x10`, par la fin pour un balayage inverse. Chercher les 41 adresses
une par une couterait 41 balayages, et surtout ne dirait pas quelles entrees
sont visees.

Ici, un seul passage sur les sections, et on retient tout deplacement
RIP-relatif dont la cible tombe DANS la plage -- plus les pointeurs absolus sur
huit octets, ou qu'ils soient.

C'est l'outil a passer AVANT de deplacer une table : deplacer ce qu'on n'a pas
enumere, c'est la faute des tables indexees par l'etage du chantier 3SX,
transposee ici.

    py -3 tools/refs_plage.py 0x180403430 0x180405AA0
    py -3 tools/refs_plage.py 0x18039F7A0 0x18039F8E8 --pas 8
    py -3 tools/refs_plage.py <debut> <fin> --data      aussi hors `.text`
    py -3 tools/refs_plage.py <debut> <fin> --patche    sur la DLL patchee
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import pe_disasm as P                                          # noqa: E402
import refs_lineaires as RL                                    # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')


def chercher_plage(img, debut, fin, avec_data=False):
    """Rend [(va_site, genre, texte, cible), ...] trie par site."""
    hits = []
    secs = img.secs if avec_data else [s for s in img.secs if s['exec']]
    for s in secs:
        blob = img.data[s['off']:s['off'] + s['rsize']]
        base = s['va']
        n = len(blob)
        if s['exec']:
            for i in range(n - 4):
                disp = struct.unpack_from('<i', blob, i)[0]
                if disp == 0:
                    continue
                for queue in (0, 1, 2, 4):
                    cible = base + i + 4 + queue + disp
                    if not (debut <= cible < fin):
                        continue
                    ins = RL.decoder_autour(img, base + i, cible)
                    if ins is None:
                        continue
                    hits.append((ins.address, 'rip',
                                 '%s %s' % (ins.mnemonic, ins.op_str), cible,
                                 base + i))
                    break
        for i in range(0, max(0, n - 8), 4):
            v = struct.unpack_from('<Q', blob, i)[0]
            if debut <= v < fin:
                hits.append((base + i, 'ptr64[%s]' % s['name'], None, v,
                             base + i))
    vus, out = set(), []
    for va, genre, txt, cible, champ in sorted(hits):
        if (champ, genre) in vus:
            continue
        vus.add((champ, genre))
        out.append((va, genre, txt, cible, champ))
    return out


def main():
    argv = sys.argv[1:]
    if len(argv) < 2:
        print(__doc__)
        return 1
    debut, fin = int(argv[0], 0), int(argv[1], 0)
    pas = 0
    if '--pas' in argv:
        pas = int(argv[argv.index('--pas') + 1], 0)
    chemin = MOTEUR + ('' if '--patche' in argv else '.origine')
    img = P.Image(chemin)
    fs = P.runtime_functions(img)
    hits = chercher_plage(img, debut, fin, '--data' in argv)

    print('plage 0x%X..0x%X (%d octets) : %d reference(s)'
          % (debut, fin, fin - debut, len(hits)))
    print()
    for va, genre, txt, cible, champ in hits:
        d = cible - debut
        rang = ('  [entree %d, +0x%X]' % (d // pas, d % pas)) if pas else ''
        f = RL.contenant(fs, va)
        print('  0x%-12X %-14s -> 0x%X (+0x%X)%s' % (va, genre, cible, d, rang))
        if txt:
            # Le CHAMP est ce qu'un patcheur reecrit : le disp32 pour une
            # reference RIP-relative, le qword pour un pointeur absolu. Sa
            # position ne depend pas du prefixe REX que capstone rate quand il
            # part mal aligne -- l'adresse d'instruction ci-dessus, elle, peut
            # etre decalee d'un octet pour cette raison.
            print('       %-46s champ disp32 en 0x%X   %s'
                  % (txt, champ, ('dans 0x%X' % f) if f else '(hors .pdata)'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
