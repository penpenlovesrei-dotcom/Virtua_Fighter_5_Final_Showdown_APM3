#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES ANCRES DES PLANCHES DE TOURNOI (`aet_n_tnt` et `aet_n_tnto`).

POURQUOI (2026-10-18). Le 17.13 a relevé quelle fenêtre porte quel libellé
dans les six écrans de tournoi, mais **les positions ne sont pas dans le
code** : `FUN_822E39C0` les prend dans l'ancre de la planche AET, à partir du
nom. C'est la règle du 9.17 -- le Quest ne place pas son texte, il le POSE.
Ce relevé est donc l'autre moitié de la mise en page.

Même lecture que `tools/ancres_que.py`, deux planches de plus, et on cherche
par NOM : les fenêtres des six écrans, les trois tableaux, les places
`p_name_NN_lt` et les calques de déplacement `idoNN`.

    py -3 tools/ancres_tnt.py              les noms cités par le code
    py -3 tools/ancres_tnt.py --tout       tous les calques de toutes les scènes
    py -3 tools/ancres_tnt.py --motif xxx  ceux dont le nom contient xxx
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aet import Aet, TAILLE_CALQUE, TYPES          # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D2 = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media',
                  'rom', '2d')
PLANCHES = ['aet_n_tnt.bin', 'aet_n_tnto.bin', 'aet_n_que.bin',
            'aet_n_qwin.bin', 'aet_n_cmn.bin', 'aet_n_info.bin']

# Ce que le code cite (17.12, 17.13, 17.8, 16.3).
CITES = [
    'p_que_info_win', 'p_rule_win', 'p_tnt_info_win', 'p_tnt_vs_win',
    'p_compe_list', 'p_tnt_rslt_win', 'p_cmn_win_l',
    'tnt_hyou', 'p_name_', 'ido', 'tnt_move', 'dan_icon',
]


def val(pr):
    """La valeur d'une propriete : constante, ou ('anime', n cles)."""
    if pr is None:
        return None
    if pr['valeur'] is not None:
        return pr['valeur']
    if pr['cles']:
        return ('anime', len(pr['cles']))
    return None


def position(a, calque):
    """La position du calque. LE BLOC DE 48 OCTETS EST EN `calque + 0x28`,
    directement -- c'est ce que documente `aet.py`, mesure a l'appui (les
    640/384 de `aet_n_adv`). Passer par une seconde indirection
    (`u32(v + 0x08)`, comme le fait `ancres_que.py`) ne rend que des
    proprietes illisibles : voir la reserve du 17.17."""
    t = a.transforme(a.u32(calque + 0x28))
    if t is None:
        return None
    return (val(t['Position.X']), val(t['Position.Y']),
            val(t['Origine.X']), val(t['Origine.Y']))


def main():
    tout = '--tout' in sys.argv
    motif = None
    if '--motif' in sys.argv:
        motif = sys.argv[sys.argv.index('--motif') + 1]

    for nomf in PLANCHES:
        chemin = os.path.join(D2, nomf)
        if not os.path.exists(chemin):
            print('%s : absent' % nomf)
            continue
        a = Aet(chemin)
        trouves = []
        for p in a.scenes():
            sc = a.scene(p)
            compos = a.compositions(sc)
            for i, (n, ptr) in enumerate(compos):
                for k in range(n):
                    o = ptr + TAILLE_CALQUE * k
                    nom = a.chaine(a.u32(o)) or ''
                    if not tout:
                        if motif:
                            if motif.lower() not in nom.lower():
                                continue
                        elif not any(nom.startswith(c) for c in CITES):
                            continue
                    pos = position(a, o)
                    t = TYPES.get(a.d[o + 0x17], '?')
                    trouves.append((sc['nom'], i, nom, t, pos))
        print()
        print('=== %s : %d calque(s) retenu(s) ===' % (nomf, len(trouves)))
        for scene, i, nom, t, pos in trouves:
            if pos is None:
                print('  %-10s c%-3d %-30s %-11s pas de transforme'
                      % (scene, i, nom, t))
            else:
                print('  %-10s c%-3d %-30s %-11s pos (%s, %s)  origine (%s, %s)'
                      % (scene, i, nom, t, pos[0], pos[1], pos[2], pos[3]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
