#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES ANCRES DE LA CARTE DU QUEST (`AET_N_QUE`, scene MAIN).

Meme lecture que `analysis/quest/ancres_qwin.txt`, mais pour la planche de la
CARTE : c'est la qu'on trouve le cadre de la fiche du joueur (`waku_1p`), les
portraits (`face_<perso>`), les BATIMENTS des salles (`bg_01_<lieu>`) et les
ancres de la fiche -- `p_name_lt` le nom, `p_dan_c` le grade, `p_gen_c`
l'argent, `p_txt_01_lt` et `p_txt_02_lt` les deux lignes.

La position d'un calque se lit dans le bloc de 48 octets que DESIGNE le u32
en `+0x28` du calque -- une seule indirection, mesuree le 2026-10-19 contre
`aet.py`. Huit proprietes `{nombre, pointeur}` de 8 octets a partir de
`+0x04` : origine, position, rotation, echelle, opacite. Une propriete a une
seule cle est une constante ; le pointeur mene alors au flottant.

    py -3 tools/ancres_que.py              les calques de la racine
    py -3 tools/ancres_que.py --tout       toutes les compositions
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aet import Aet, TAILLE_CALQUE, TYPES          # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANCHE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media',
                       'rom', '2d', 'aet_n_que.bin')


def propriete(a, p):
    n, ptr = a.u32(p), a.u32(p + 4)
    if n == 0:
        return 0.0
    if n == 1 and 0 < ptr < len(a.d):
        return struct.unpack_from('<f', a.d, ptr)[0]
    return None


def position(a, calque):
    """Position.X / Position.Y du calque.

    MESURE le 2026-10-19 : le u32 en `calque + 0x28` EST le bloc de 48
    octets de la transforme, pas un pointeur vers un pointeur. Sur la
    racine de `MAIN` de `aet_n_adv` (1280x768) ce chemin rend
    (640, 384) pour les deux calques -- le centre exact de la scene --
    la ou la double indirection d'avant rendait (None, None). Les
    proprietes sont des couples {nombre de cles, pointeur} tous les 8
    octets a partir de +0x04 : Origine.X +0x04, Origine.Y +0x0C,
    Position.X +0x14, Position.Y +0x1C.
    """
    v = a.u32(calque + 0x28)
    if not 0 < v < len(a.d):
        return None
    return (propriete(a, v + 0x14), propriete(a, v + 0x1C))


def main():
    tout = '--tout' in sys.argv
    a = Aet(PLANCHE)
    for p in a.scenes():
        sc = a.scene(p)
        if sc['nom'] != 'MAIN':
            continue
        compos = a.compositions(sc)
        for i, (n, ptr) in enumerate(compos):
            racine = (i == len(compos) - 1)
            if not tout and not racine:
                continue
            print('composition %d%s : %d calques'
                  % (i, ' (RACINE)' if racine else '', n))
            for k in range(n):
                o = ptr + TAILLE_CALQUE * k
                pos = position(a, o)
                nom = a.chaine(a.u32(o))
                t = TYPES.get(a.d[o + 0x17], '?')
                if pos and pos[0] is not None and pos[1] is not None:
                    print('  %-26s %-12s x %7.1f  y %7.1f'
                          % (nom, t, pos[0], pos[1]))
                else:
                    print('  %-26s %-12s (anime ou sans transformation)'
                          % (nom, t))
    return 0


if __name__ == '__main__':
    sys.exit(main())
