#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pilote le MENU OPERATEUR de vfes.exe, une impulsion a la fois.

Le stub `apm.dll` rend `Sequence_isTest` vrai quand le scenario porte
`test = 1` : le jeu demarre alors dans le menu de test de la borne, dont
l'ecran de test d'entrees NOMME chaque signal. C'est la voie propre pour
identifier les codes 2 a 14 : ecran fixe, pas d'adversaire, pas d'animation.

Les deux boutons du menu, releves a l'execution :

    code 1 = SERVICE  (deplace le curseur)
    code 0 = TEST     (valide)

**Une impulsion doit etre BREVE.** Les menus appliquent une auto-repetition :
un appui de 350 ms balaie toute la liste et ramene le curseur a son point de
depart, ce qui donne l'illusion que rien n'a bouge. Le stub relit son scenario
toutes les 30 ms, ce qui permet des appuis de l'ordre de 80 ms -- environ cinq
trames, sous le seuil de repetition.

Usage :
    py -3 tools/menu_test.py --lancer              lance le jeu en mode test
    py -3 tools/menu_test.py service               une impulsion SERVICE
    py -3 tools/menu_test.py service x3            trois impulsions
    py -3 tools/menu_test.py test                  valide
    py -3 tools/menu_test.py --capture nom.png     capture l'ecran
"""
import os
import subprocess
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
SCENARIO = os.path.join(JEU, 'apm_entrees.txt')

SERVICE, TEST = 1, 0
IMPULSION = 0.02          # duree d'un appui, en secondes ; --duree la change
# Mesure : a 0.08 s le curseur avance de TROIS lignes et a 0.04 s de DEUX,
# l'auto-repetition mordant deja. 20 ms -- une trame a 60 images par seconde --
# donne un pas et un seul. C'est pour cela que le stub relit son scenario toutes
# les 30 ms : a 250 ms, aucune impulsion assez breve n'etait possible.
REPOS = 0.35              # temps de repos entre deux appuis


def ecrire(codes):
    with open(SCENARIO, 'w', encoding='ascii', newline='\n') as fp:
        fp.write('# ecrit par tools/menu_test.py\nfront = 60\njournal = 0\ntest = 1\n'
                 '0 %s\n' % (codes or 'rien'))


def impulsion(code, n=1):
    for _ in range(n):
        ecrire('rien')
        time.sleep(0.12)
        ecrire(str(code))
        time.sleep(IMPULSION)
        ecrire('rien')
        time.sleep(REPOS)


# Les six lignes du GAME TEST MODE, a leur ordonnee dans la capture 1920x1080.
LIGNES = [('BOOKKEEPING', 200), ('GAME ASSIGNMENTS', 237), ('SOUND SETTING', 273),
          ('BACKUP DATA CLEAR', 309), ('SUB SYSTEM TEST MODE', 345), ('EXIT', 381)]


def ou_est_le_curseur(chemin):
    """Lit la position du chevron dans une capture. Evite de compter les pas :
    l'auto-repetition rend le nombre de lignes parcourues imprevisible."""
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        return None
    a = np.asarray(Image.open(chemin).convert('L'))
    if a.shape[0] < 400:
        return None
    colonne = a[:, 350:375]
    for nom, y in LIGNES:
        if colonne[y - 12:y + 12, :].max() > 120:
            return nom
    return None


def aller_a(cible, maxi=12):
    """Pousse SERVICE jusqu'a ce que le curseur soit sur la ligne voulue."""
    tmp = os.path.join(RACINE, 'analysis', '_curseur.png')
    for k in range(maxi):
        capturer(tmp)
        ou = ou_est_le_curseur(tmp)
        print('   curseur : %s' % ou)
        if ou is None:
            return False
        if ou.upper().startswith(cible.upper()):
            return True
        impulsion(SERVICE, 1)
    return False


def capturer(nom):
    chemin = nom if os.path.isabs(nom) else os.path.join(RACINE, 'analysis', nom)
    r = subprocess.run([sys.executable, os.path.join(ICI, 'capture_fenetre.py'), chemin],
                       capture_output=True, text=True)
    sortie = (r.stdout or '').strip().splitlines()
    return sortie[0] if sortie else 'capture impossible'


def lancer():
    ecrire('rien')
    subprocess.Popen([os.path.join(JEU, 'vfes.exe')], cwd=JEU)
    print('jeu lance en mode test, on attend le menu...')
    time.sleep(15)
    try:
        subprocess.run([sys.executable, os.path.join(ICI, 'muet.py'), '--surveiller', '3'],
                       capture_output=True, timeout=20)
    except Exception:
        pass


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    global IMPULSION
    if '--duree' in argv:
        IMPULSION = float(argv[argv.index('--duree') + 1])
    if '--lancer' in argv:
        lancer()
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ('service', 'test'):
            n = 1
            if i + 1 < len(argv) and argv[i + 1].startswith('x'):
                n = int(argv[i + 1][1:])
                i += 1
            impulsion(SERVICE if a == 'service' else TEST, n)
            print('%s x%d' % (a, n))
        elif a == '--aller':
            i += 1
            ok = aller_a(argv[i])
            print('aller a %s : %s' % (argv[i], 'atteint' if ok else 'ECHEC'))
            if not ok:
                return 1
        elif a == '--capture':
            i += 1
            print(capturer(argv[i]))
        elif a == '--duree':
            i += 1
        elif a == '--attendre':
            i += 1
            time.sleep(float(argv[i]))
        i += 1
    ecrire('rien')
    return 0


if __name__ == '__main__':
    sys.exit(main())
