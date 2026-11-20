#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES MUSIQUES DU MODE QUEST, posées dans le média de Final Showdown.

CE N'EST PAS UN CHOIX, C'EST UNE LECTURE. Chaque morceau est nommé dans le
code de 2007, et on sait QUI le demande (relevé par
`tools/quest_x360.py --chaine "vf5ps3_b"`, puis lu au décompilateur ; §20.2
de `analysis/mode_quest.md`).

LES QUINZE FICHIERS, ET LEUR DEMANDEUR

    vf5ps3_b03map   la CARTE, la MAISON et les SALLES
                    TaskQuestMap (0x8230CBC0), TaskQuestHomeMenu (0x8230B7D0,
                    0x8230B8E0), TaskQuestTenpo (0x82312E58, 0x82315500)

    vf5ps3_j26      jingle d'ouverture du tournoi, niveau 0 -- la SALLE
    vf5ps3_j25      jingle d'ouverture, niveau 1 -- OFFICIEL ordinaire
    vf5ps3_j24      jingle d'ouverture, niveau 2 -- la FINALE
                    TASK_TOURNAMENT_OPENING (0x8231E538), indexes par
                    [obj+0x58] ; chacun va avec une VOIX, `tnm_taikai_tenpo`
                    / `_normal` / `_final`, jouee par nom (non posee ici)

    vf5ps3_b04tn1   niveau 0, AVANT les demi-finales
    vf5ps3_b05tn2   niveau 0, A PARTIR des demi-finales
    vf5ps3_b06tn1   niveau 1, avant   /  b07tn2  niveau 1, apres
    vf5ps3_b08tn1   evenement 14, avant / b09tn2  evenement 14, apres
                    0x8231F1D8, le niveau 2 du sequenceur. Le basculement
                    tn1 -> tn2 se fait sur `desc[6] == 3`, le type de tour
                    `Semifinals` (§17.15).

    vf5ps3_b10ke1   la FINALE (desc[6] == 4), cas ordinaire
    vf5ps3_b11ke2   la FINALE, quand FUN_82315BE8(evenement) est vrai
    vf5ps3_b12ke3   la FINALE de l evenement 14
                    0x8231F1D8, cas 8

    vf5ps3_b16tse   l ecran CUSTOMIZE, [obj+0x58] == 1
    vf5ps3_b17tco   l ecran CUSTOMIZE, sinon
                    0x822F4F98

Final Showdown n'en a AUCUNE -- la musique est partie avec le mode. On les
copie depuis le média de 2007, exactement comme `tools/rivaux.py` copie la
table des mille rivaux : des fichiers NEUFS dans
`vf5fs_media/rom/sound/bgm/`, rien n'est masqué, rien n'est écrasé.

Le moteur les joue par `0x180185DA0(voie, chemin, 0)` -- la fonction que FS
emploie lui-même pour `rom/sound/bgm/vf5fs_bgm_sel.adx` (`0x18016D180`) --, et
`0x180186D40(voie)` les arrête. `b03map` est la seule dont on ait la preuve
d'EXECUTION : `runtime/media/vf5fs/quest_journal.txt` du 2026-10-18 porte
sept « musique du Quest lancee ».

    py -3 tools/musique_quest.py --ajouter    les poser toutes
    py -3 tools/musique_quest.py --controle   lesquelles sont la ?
    py -3 tools/musique_quest.py --retirer    les reprendre
    py -3 tools/musique_quest.py --ajouter --seule vf5ps3_b03map
"""
import argparse
import hashlib
import os
import shutil
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BGM = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media',
                   'rom', 'sound', 'bgm')
# Les dossiers ou l on cherche, dans l ordre.
DOSSIERS = [
    os.path.join(r'C:\Users\frede\Desktop\VF5 FS DECOMP\X360_VF5\media',
                 'sound', 'bgm'),
    os.path.join(RACINE, 'extracted', 'quest'),
]

# nom -> a quoi il sert. L ordre est celui du §20.2.
MORCEAUX = [
    ('vf5ps3_b03map', 'la carte, la maison et les salles'),
    ('vf5ps3_j26', 'ouverture du tournoi, niveau 0 (la salle)'),
    ('vf5ps3_j25', 'ouverture du tournoi, niveau 1 (officiel)'),
    ('vf5ps3_j24', 'ouverture du tournoi, niveau 2 (la finale)'),
    ('vf5ps3_b04tn1', 'niveau 0, avant les demi-finales'),
    ('vf5ps3_b05tn2', 'niveau 0, a partir des demi-finales'),
    ('vf5ps3_b06tn1', 'niveau 1, avant les demi-finales'),
    ('vf5ps3_b07tn2', 'niveau 1, a partir des demi-finales'),
    ('vf5ps3_b08tn1', 'evenement 14, avant les demi-finales'),
    ('vf5ps3_b09tn2', 'evenement 14, a partir des demi-finales'),
    ('vf5ps3_b10ke1', 'la finale, cas ordinaire'),
    ('vf5ps3_b11ke2', 'la finale, FUN_82315BE8 vrai'),
    ('vf5ps3_b12ke3', 'la finale de l evenement 14'),
    ('vf5ps3_b16tse', 'l ecran Customize, [obj+0x58] == 1'),
    ('vf5ps3_b17tco', 'l ecran Customize, sinon'),
]


def source(nom):
    for d in DOSSIERS:
        c = os.path.join(d, nom + '.adx')
        if os.path.exists(c):
            return c
    return None


def cible(nom):
    return os.path.join(BGM, nom + '.adx')


def sha(chemin):
    h = hashlib.sha256()
    with open(chemin, 'rb') as fh:
        for bloc in iter(lambda: fh.read(1 << 20), b''):
            h.update(bloc)
    return h.hexdigest()


def choisis(seules):
    if not seules:
        return MORCEAUX
    inconnus = [s for s in seules if s not in dict(MORCEAUX)]
    if inconnus:
        raise SystemExit('inconnu(s) : %s' % ' '.join(inconnus))
    return [(n, r) for n, r in MORCEAUX if n in seules]


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--ajouter', action='store_true')
    ap.add_argument('--controle', action='store_true')
    ap.add_argument('--retirer', action='store_true')
    ap.add_argument('--seule', nargs='+', default=None,
                    help='n agir que sur ces morceaux')
    a = ap.parse_args()
    lot = choisis(a.seule)

    if a.retirer:
        n = 0
        for nom, _ in lot:
            c = cible(nom)
            if os.path.exists(c):
                os.remove(c)
                n += 1
        print('  %d morceau(x) retire(s) sur %d.' % (n, len(lot)))
        return 0

    if a.controle:
        manque = []
        for nom, role in lot:
            c = cible(nom)
            if os.path.exists(c):
                print('  presente  %-16s %9d o   %s'
                      % (nom, os.path.getsize(c), role))
            else:
                s = source(nom)
                print('  ABSENTE   %-16s %9s     %s%s'
                      % (nom, '-' if not s else '%d o' % os.path.getsize(s),
                         role, '' if s else '   (ET SANS SOURCE)'))
                manque.append(nom)
        print('  %d presente(s), %d absente(s) sur %d.'
              % (len(lot) - len(manque), len(manque), len(lot)))
        return 1 if manque else 0

    if not a.ajouter:
        print(__doc__)
        return 2

    # LES SOURCES D ABORD, TOUTES : on ne pose rien si l une manque.
    sources = {}
    perdues = []
    for nom, _ in lot:
        s = source(nom)
        if s:
            sources[nom] = s
        else:
            perdues.append(nom)
    if perdues:
        print('  REFUS : source introuvable pour %s' % ' '.join(perdues))
        print('  Cherchee dans :')
        for d in DOSSIERS:
            print('    %s' % d)
        return 1

    os.makedirs(BGM, exist_ok=True)
    poses, deja = 0, 0
    for nom, role in lot:
        c = cible(nom)
        s = sources[nom]
        if os.path.exists(c) and os.path.getsize(c) == os.path.getsize(s) \
                and sha(c) == sha(s):
            print('  deja la   %-16s %9d o   %s'
                  % (nom, os.path.getsize(c), role))
            deja += 1
            continue
        # a cote, puis on remplace : la regle du depot.
        tmp = c + '.neuf'
        shutil.copy2(s, tmp)
        os.replace(tmp, c)
        print('  posee     %-16s %9d o   %s  sha %s'
              % (nom, os.path.getsize(c), role, sha(c)[:16]))
        poses += 1
    print('  %d posee(s), %d deja la, dans %s'
          % (poses, deja, os.path.relpath(BGM, RACINE)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
