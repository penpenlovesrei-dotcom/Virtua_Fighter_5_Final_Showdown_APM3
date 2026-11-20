#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES ANCRES DES ÉCRANS DU QUEST, SUR TOUTES LES PLANCHES DE FS.

POURQUOI (2026-10-19). Le §17.17 a relevé les ancres des tournois en
balayant six planches (`ancres_tnt.py`). Les écrans du §18 — le menu de la
maison, `Quest settings`, la boutique, les deux listes de nouveautés et les
emblèmes — demandent le même relevé, mais la question est l'autre : **ce qui
MANQUE à Final Showdown.** Un motif introuvable est un résultat, pas une
erreur, et il faut donc balayer les **quinze** `aet_*.bin`, pas six, pour
pouvoir l'affirmer.

LA LECTURE DE LA TRANSFORME. Le u32 en `calque + 0x28` **est** le bloc de 48
octets (`Position.X` en `+0x14`, `Position.Y` en `+0x1C`). Mesuré le
2026-10-19 contre le cas dont la réponse est connue : la racine de la scène
`MAIN` de `aet_n_adv` (1280x768) rend (640, 384) pour ses deux calques, le
centre exact. La double indirection que portait `ancres_que.py` rendait
(None, None) sur ce même cas ; elle est corrigée.

    py -3 tools/ancres_ecrans.py --motif p_home_menu
    py -3 tools/ancres_ecrans.py --motif p_q_opt --motif p_item
    py -3 tools/ancres_ecrans.py --ecrans          les cinq écrans du §18
    py -3 tools/ancres_ecrans.py --motif xxx --planche aet_n_qwin.bin
    py -3 tools/ancres_ecrans.py --scenes          le nom des scènes, par planche
    py -3 tools/ancres_ecrans.py --2007 --ecrans  dans le media de 2007
    py -3 tools/ancres_ecrans.py --dossier <d>    dans un autre dossier

LE MEDIA 2D DE 2007 EST DEJA EXTRAIT (il l etait avant la seance du
2026-10-19) : `C:/Users/frede/Desktop/VF5 FS DECOMP/X360_VF5/media/
rom/2d`, 265 fichiers dont vingt-sept `aet_*.bin`. Il porte deux
planches que Final Showdown n a pas du tout : `aet_n_qcmn.bin` et
`aet_t_item.bin`.
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aet import Aet, TAILLE_CALQUE, TYPES          # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D2 = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media',
                  'rom', '2d')
# Le media 2D de VF5 Xbox 360 de 2007, deja extrait.
D2007 = os.path.join('C:' + os.sep, 'Users', 'frede', 'Desktop',
                     'VF5 FS DECOMP', 'X360_VF5', 'media', 'rom', '2d')

# Les cinq écrans que le §18 dit écrits mais non câblés.
ECRANS = ['p_home_menu', 'p_q_opt', 'p_item', 'p_embsel', 'p_newitem']


def planches(d=None):
    return [n for n in sorted(os.listdir(d or D2))
            if n.startswith('aet_') and n.endswith('.bin')]


def val(pr):
    """La valeur d'une propriété : constante, ou ('anime', n clés)."""
    if pr is None:
        return None
    if pr['valeur'] is not None:
        return pr['valeur']
    if pr['cles']:
        return ('anime', len(pr['cles']))
    return None


def fmt(v):
    if v is None:
        return '-'
    if isinstance(v, tuple):
        return 'anime(%d)' % v[1]
    if abs(v - round(v)) < 1e-4:
        return '%d' % round(v)
    return '%.2f' % v


def transforme(a, calque):
    """UNE indirection : le u32 en `+0x28` est le bloc de 48 octets."""
    t = a.transforme(a.u32(calque + 0x28))
    if t is None:
        return None
    return (val(t['Position.X']), val(t['Position.Y']),
            val(t['Origine.X']), val(t['Origine.Y']),
            val(t['Echelle.X']), val(t['Echelle.Y']))


def balayer(a, motifs, tout):
    """Les calques retenus, avec la scène et la composition où ils vivent."""
    out = []
    for p in a.scenes():
        sc = a.scene(p)
        compos = a.compositions(sc)
        for i, (n, ptr) in enumerate(compos):
            racine = (i == len(compos) - 1)
            for k in range(n):
                o = ptr + TAILLE_CALQUE * k
                nom = a.chaine(a.u32(o)) or ''
                if not tout:
                    bas = nom.lower()
                    if not any(m.lower() in bas for m in motifs):
                        continue
                out.append((sc['nom'], i, racine, nom,
                            TYPES.get(a.d[o + 0x17], '?'), transforme(a, o)))
    return out


def main():
    args = sys.argv[1:]
    global D2
    if '--2007' in args:
        D2 = D2007
    if '--dossier' in args:
        D2 = args[args.index('--dossier') + 1]
    if not os.path.isdir(D2):
        print('dossier introuvable : %s' % D2)
        return 2
    print('# dossier : %s' % D2)
    motifs = [args[i + 1] for i, x in enumerate(args) if x == '--motif']
    if '--ecrans' in args:
        motifs = motifs + ECRANS
    tout = '--tout' in args
    liste_scenes = '--scenes' in args
    voulues = [args[i + 1] for i, x in enumerate(args) if x == '--planche']
    if not motifs and not tout and not liste_scenes:
        print(__doc__)
        return 2

    noms = voulues or planches()
    trouve_par_motif = dict((m, []) for m in motifs)

    for nomf in noms:
        chemin = os.path.join(D2, nomf)
        if not os.path.exists(chemin):
            print('%-20s : ABSENT' % nomf)
            continue
        try:
            a = Aet(chemin)
        except Exception as exc:                  # noqa: BLE001
            print('%-20s : illisible (%s)' % (nomf, exc))
            continue

        if liste_scenes:
            sc = [a.scene(p)['nom'] for p in a.scenes()]
            print('%-20s %2d scene(s) : %s' % (nomf, len(sc), ', '.join(sc)))
            continue

        res = balayer(a, motifs, tout)
        for m in motifs:
            for r in res:
                if m.lower() in r[3].lower():
                    trouve_par_motif[m].append(nomf)
                    break
        if not res:
            continue
        print()
        print('=== %s : %d calque(s) ===' % (nomf, len(res)))
        scene_vue = None
        for scene, i, racine, nom, t, pos in res:
            if scene != scene_vue:
                print('  -- scene %s' % scene)
                scene_vue = scene
            marque = 'RACINE' if racine else 'c%d' % i
            if pos is None:
                print('     %-8s %-34s %-11s pas de transforme'
                      % (marque, nom, t))
            else:
                print('     %-8s %-34s %-11s pos (%s, %s)  org (%s, %s)  ech (%s, %s)'
                      % (marque, nom, t, fmt(pos[0]), fmt(pos[1]),
                         fmt(pos[2]), fmt(pos[3]), fmt(pos[4]), fmt(pos[5])))

    if motifs:
        print()
        print('=== CE QUE FINAL SHOWDOWN A, ET CE QU IL N A PAS ===')
        for m in motifs:
            ou = sorted(set(trouve_par_motif[m]))
            if ou:
                print('  %-16s present dans : %s' % (m, ', '.join(ou)))
            else:
                print('  %-16s INTROUVABLE dans les %d planches'
                      % (m, len(noms)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
