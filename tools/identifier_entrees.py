#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Identifie les codes d'entree d'apm.dll a l'ecran de selection de personnage.

Le sens des codes 2 a 14 n'est pas etabli. Les chercher pendant un combat ne
donne rien : l'adversaire gere par la machine bouge en meme temps, et une capture
ne permet pas d'attribuer un mouvement au bouton plutot qu'a lui.

L'ecran de selection, lui, est sans ambiguite : seul le curseur du joueur bouge.
Ce script y presse chaque code a tour de role et compare la bande du roster entre
avant et apres. Un code qui deplace le curseur se voit immediatement, chiffre a
l'appui, sans avoir a regarder treize captures.

Le jeu doit tourner (tools/lancer_vfes_combat.cmd, ou ce script le lance).

Usage :
    py -3 tools/identifier_entrees.py               lance le jeu et fait la passe
    py -3 tools/identifier_entrees.py --deja-lance  le jeu tourne deja
    py -3 tools/identifier_entrees.py --codes 2,3,4,5
"""
import os
import subprocess
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
SCENARIO = os.path.join(JEU, 'apm_entrees.txt')
SORTIE = os.path.join(RACINE, 'analysis', 'identification_entrees')

import capture_fenetre as cap                               # noqa: E402


def ecrire(codes):
    with open(SCENARIO, 'w', encoding='ascii', newline='\n') as fp:
        fp.write('# ecrit par tools/identifier_entrees.py\nfront = 150\njournal = 0\n'
                 '0 %s\n' % (codes or 'rien'))


def prendre(chemin):
    """Capture la fenetre du jeu -- SEULEMENT si elle est au premier plan.

    capture_fenetre photographie la ZONE D'ECRAN occupee par la fenetre : si une
    autre fenetre la recouvre, c'est cette autre fenetre qu'on enregistre. Ce
    piege a produit une passe entiere de captures inutilisables, et pire, il
    photographie ce que l'utilisateur a sous les yeux. On refuse donc de capturer
    a l'aveugle, plutot que de ramener une image fausse."""
    import ctypes
    import ctypes.wintypes as w
    cap.dpi_aware()
    hwnd, nom, rect = cap.trouver('Virtua Fighter')
    if not hwnd:
        return None
    if cap.user32.GetForegroundWindow() != hwnd:
        return 'ARRIERE_PLAN'
    r = w.RECT()
    cap.user32.GetWindowRect(hwnd, ctypes.byref(r))
    cap.capturer((r.left, r.top, r.right, r.bottom), chemin)
    return chemin


def bande(chemin):
    """La bande du roster, en bas de l'ecran : c'est la que le curseur bouge."""
    from PIL import Image
    im = Image.open(chemin).convert('RGB')
    l, h = im.size
    return im.crop((0, int(h * 0.66), l, h))


def difference(a, b):
    from PIL import ImageChops
    d = ImageChops.difference(bande(a), bande(b))
    hist = d.convert('L').histogram()
    total = sum(hist)
    # part des pixels dont l'ecart depasse 24 niveaux
    forts = sum(hist[24:])
    return 100.0 * forts / total if total else 0.0


def main():
    argv = sys.argv[1:]
    codes = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14]
    if '--codes' in argv:
        codes = [int(x, 0) for x in argv[argv.index('--codes') + 1].split(',')]
    os.makedirs(SORTIE, exist_ok=True)

    if '--deja-lance' not in argv:
        ecrire('rien')
        subprocess.Popen([os.path.join(JEU, 'vfes.exe')], cwd=JEU)
        print('jeu lance, on attend l ecran-titre...')
        time.sleep(16)
        try:
            subprocess.run([sys.executable, os.path.join(ICI, 'muet.py'),
                            '--surveiller', '5'], capture_output=True, timeout=30)
        except Exception:
            pass
        ecrire('7')
        time.sleep(0.6)
        ecrire('rien')
        print('START presse ; on attend la selection de personnage...')
        time.sleep(4)

    avant = prendre(os.path.join(SORTIE, 'depart.png'))
    if avant == 'ARRIERE_PLAN':
        print("la fenetre du jeu n'est pas au premier plan : la capture ramenerait")
        print("l'ecran de quelqu'un d'autre. Mettez la fenetre devant, ou passez par")
        print("tools/carte_entrees.py, qui mesure en memoire et ne capture rien.")
        return 1
    if not avant:
        print('fenetre du jeu introuvable')
        return 1
    print('\n%-6s %-10s %s' % ('code', 'ecart %', 'verdict'))
    resultats = []
    for c in codes:
        ecrire('rien')
        time.sleep(0.30)
        a = prendre(os.path.join(SORTIE, 'avant_%02d.png' % c))
        ecrire(str(c))
        time.sleep(0.45)
        b = prendre(os.path.join(SORTIE, 'code_%02d.png' % c))
        ecrire('rien')
        time.sleep(0.25)
        if a == 'ARRIERE_PLAN' or b == 'ARRIERE_PLAN':
            print('%-6d --         fenetre passee en arriere-plan, on arrete' % c)
            break
        d = difference(a, b) if (a and b) else -1.0
        v = 'DEPLACE LE CURSEUR' if d > 1.5 else ('leger' if d > 0.3 else '')
        print('%-6d %-10.2f %s' % (c, d, v))
        resultats.append((c, d))
    ecrire('rien')
    print('\ncaptures dans %s' % SORTIE)
    bouge = [c for c, d in resultats if d > 1.5]
    print('codes qui deplacent le curseur : %s' % (bouge or 'aucun'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
