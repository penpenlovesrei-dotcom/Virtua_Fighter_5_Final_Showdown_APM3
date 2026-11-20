#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Presse des boutons dans vfes.exe DEJA LANCE, et capture le resultat.

Le apm.dll de substitution relit apm_entrees.txt toutes les 250 ms : reecrire ce
fichier revient donc a appuyer sur un bouton, sans recompiler ni relancer le jeu.
C'est l'outil de reconnaissance des codes d'entree : on presse un code, on
regarde ce que l'ecran devient.

Usage :
    py -3 tools/presser.py 7                        presse le code 7
    py -3 tools/presser.py 7,8 --duree 500          deux codes, 500 ms
    py -3 tools/presser.py 7 --apres analysis/x.png --attendre 2
    py -3 tools/presser.py --relacher                tout relacher
"""
import os
import subprocess
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
SCENARIO = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')
DELAI_RELECTURE = 0.35          # le stub controle la date du fichier toutes les 250 ms


def ecrire(codes):
    txt = ('# ecrit par tools/presser.py -- passe de reconnaissance\n'
           'front = 150\n'
           'journal = 0\n'
           '0 %s\n' % (codes or 'rien'))
    with open(SCENARIO, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(txt)


def capturer(chemin):
    r = subprocess.run([sys.executable, os.path.join(ICI, 'capture_fenetre.py'), chemin],
                       capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    duree = 0.30
    attendre = 1.5
    avant = apres = None
    if '--duree' in argv:
        duree = int(argv[argv.index('--duree') + 1]) / 1000.0
    if '--attendre' in argv:
        attendre = float(argv[argv.index('--attendre') + 1])
    if '--avant' in argv:
        avant = argv[argv.index('--avant') + 1]
    if '--apres' in argv:
        apres = argv[argv.index('--apres') + 1]

    if '--relacher' in argv:
        ecrire('rien')
        print('tout relache')
        return 0

    codes = argv[0]
    if avant:
        capturer(avant)
    ecrire('rien')                    # etat connu avant l'appui
    time.sleep(DELAI_RELECTURE)
    ecrire(codes)
    print('appui   : %s' % codes)
    time.sleep(DELAI_RELECTURE + duree)
    ecrire('rien')
    print('relache : apres %.0f ms' % (duree * 1000))
    time.sleep(attendre)
    if apres:
        capturer(apres)
    return 0


if __name__ == '__main__':
    sys.exit(main())
