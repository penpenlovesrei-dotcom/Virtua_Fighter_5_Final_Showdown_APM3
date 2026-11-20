#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ALLER TOUT SEUL JUSQU'A L'ECRAN DU QUEST, ET LE PHOTOGRAPHIER.

POURQUOI (2026-10-19, demande de Frederic). Verifier un seul sprite a coute
huit allers-retours « relance, regarde, dis-moi ». La sequence est toujours la
meme : elle s'automatise.

ON ECRIT UN SCENARIO HORODATE, ON NE BASCULE PAS LE FICHIER.
Premiere version : on ecrivait le code, on dormait, on ecrivait « rien ».
L'appui durait alors RELECTURE + duree, soit **650 ms** -- et la repetition
automatique du menu faisait descendre le curseur de sept lignes d'un coup
(constat de Frederic : « tu as fait un appui bas trop long »). On a atterri
sur OPTIONS au lieu de QUEST MODE.

Le format de `apm_entrees.txt` est pourtant une LIGNE DE TEMPS :

    <t_ms> <codes>    a partir de t_ms, compte du premier appel d'entree,
                      les codes cites sont tenus ; « rien » relache tout.

On ecrit donc le scenario ENTIER avant de lancer, et le stub le joue a la
milliseconde. Un appui de 60 ms, soit quatre trames : bien au-dessus du seuil
de detection, bien en dessous de la repetition.

ET ON RESTAURE LE FICHIER EN PARTANT. La premiere version ecrasait les
reglages `clavier`, `manette` et `manette_joueur` -- on les perdait a chaque
essai. Le maitre est `tools/apm_entrees.txt` ; on le recopie a la fin.

LES CODES, lus dans `tools/quest_runtime.c` :
    2 HAUT   3 BAS   4 GAUCHE   5 DROITE   7 START/valider   8 annuler

LA SEQUENCE PAR DEFAUT : 10 s d'attente, START pour entrer dans le menu,
six HAUT pour epingler le curseur en haut (SINGLE PLAYER), un BAS -- qui
tombe sur QUEST MODE, les lignes 1 et 2 etant grisees et sautees -- puis
START, et la capture.

    py -3 tools/quest_auto.py
    py -3 tools/quest_auto.py --sortie analysis/x.png
    py -3 tools/quest_auto.py --capture 22        capturer a 22 s
    py -3 tools/quest_auto.py --montrer           ecrire le scenario et sortir
"""
import os
import shutil
import subprocess
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
MAITRE = os.path.join(ICI, 'apm_entrees.txt')
ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')
SORTIE = os.path.join(RACINE, 'analysis', '_quest_auto.png')

APPUI = 60                      # ms : quatre trames, sous la repetition
#  : la fenetre pendant laquelle Input_isOnNow reste vrai apres un
# appui. Le maitre la met a 10 ms parce que le CLAVIER la pilote en continu ;
# pour un scenario ECRIT c est trop court -- le moteur scrute toutes les
# 16,7 ms et manque la fenetre. Le commentaire du maitre le dit : 150 ms est
# la valeur sure quand on ecrit le fichier. Mesure du 2026-10-19 : a 10 ms le
# START de l ecran-titre n etait jamais vu, la capture restait sur
# PRESS START BUTTON.
FRONT = 150
CAPTURE = 19.0                  # s apres le premier appel d'entree

# (instant en ms, code) ; « rien » est pose APPUI ms plus tard.
SEQUENCE = [
    (10000, 7),                 # entrer dans le menu
    (11600, 2), (11900, 2), (12200, 2),   # epingler le curseur en haut
    (12500, 2), (12800, 2), (13100, 2),
    (14000, 3),                 # un cran : QUEST MODE (1 et 2 sont grisees)
    (15200, 7),                 # valider
]


def scenario():
    """Le fichier complet : les reglages du maitre, puis la ligne de temps."""
    garde = []
    with open(MAITRE, encoding='latin-1') as fp:
        for l in fp:
            t = l.strip()
            t = t.split('#')[0].strip()          # sans le commentaire de fin
            if (t.startswith(('clavier', 'manette', 'nom ', 'test'))
                    and '=' in t):
                garde.append(t)
    lignes = ['# ecrit par tools/quest_auto.py -- scenario horodate',
              'front = 150', 'journal = 0'] + garde + ['0 rien']
    for t, code in SEQUENCE:
        lignes.append('%d %d' % (t, code))
        lignes.append('%d rien' % (t + APPUI))
    return '\n'.join(lignes) + '\n'


def tourne():
    r = subprocess.run(['tasklist', '/fi', 'IMAGENAME eq vfes.exe'],
                       capture_output=True, text=True)
    return 'vfes.exe' in (r.stdout or '')


def main():
    argv = sys.argv[1:]
    sortie = SORTIE
    capture = CAPTURE
    if '--sortie' in argv:
        sortie = argv[argv.index('--sortie') + 1]
    if '--capture' in argv:
        capture = float(argv[argv.index('--capture') + 1])

    txt = scenario()
    if '--montrer' in argv:
        sys.stdout.write(txt)
        return 0

    if tourne():
        print('REFUS : vfes.exe tourne deja. Le scenario doit etre en place '
              'AVANT le demarrage du moteur, ses instants comptant du premier '
              'appel d entree.')
        return 2

    with open(ACTIF + '.neuf', 'w', encoding='ascii', newline='\n') as fp:
        fp.write(txt)
    os.replace(ACTIF + '.neuf', ACTIF)
    print('scenario pose (%d appuis, capture a %.0f s)'
          % (len(SEQUENCE), capture))

    try:
        t0 = time.time()
        while not tourne():
            if time.time() - t0 > 180:
                print('vfes.exe ne demarre pas.')
                return 1
            time.sleep(0.5)
        depart = time.time()
        print('vfes.exe est la ; capture dans %.0f s...' % capture)
        time.sleep(max(0.0, capture - (time.time() - depart)))
        os.makedirs(os.path.dirname(sortie), exist_ok=True)
        r = subprocess.run([sys.executable,
                            os.path.join(ICI, 'capture_fenetre.py'), sortie],
                           capture_output=True, text=True)
        sys.stdout.write(r.stdout or '')
        sys.stderr.write(r.stderr or '')
    finally:
        # LE MAITRE EST RENDU : sans cela on perd clavier/manette a chaque essai.
        shutil.copyfile(MAITRE, ACTIF + '.neuf')
        os.replace(ACTIF + '.neuf', ACTIF)
        print('apm_entrees.txt rendu depuis tools/')

    if os.path.exists(sortie):
        print('capture : %s (%d octets)'
              % (os.path.relpath(sortie, RACINE), os.path.getsize(sortie)))
        return 0
    print('AUCUNE CAPTURE ecrite.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
