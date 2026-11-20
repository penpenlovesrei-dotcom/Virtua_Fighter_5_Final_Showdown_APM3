#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Envoie une touche a la fenetre de la borne, SANS toucher au premier plan.

POURQUOI CE SCRIPT EXISTE. Le reflexe -- AppActivate puis SendKeys -- envoie la
touche a la fenetre ACTIVE, et met une autre fenetre au premier plan au
passage. La capture qui suit photographie alors le bureau de l'utilisateur et
non la borne. C'est arrive.

Ici on retrouve la fenetre par sa CLASSE (`BorneAPM3`, unique) et on lui poste
directement WM_KEYDOWN puis WM_KEYUP. Rien ne bouge a l'ecran.

    py -3 tools/borne_touche.py P
    py -3 tools/borne_touche.py DROITE GAUCHE ENTREE
"""
import ctypes
import sys
import time

u32 = ctypes.windll.user32

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

TOUCHES = {
    'GAUCHE': 0x25, 'HAUT': 0x26, 'DROITE': 0x27, 'BAS': 0x28,
    'ENTREE': 0x0D, 'ESPACE': 0x20, 'ECHAP': 0x1B,
    'F5': 0x74, 'F11': 0x7A,
}


def fenetre():
    h = u32.FindWindowW('BorneAPM3', None)
    return h if h else 0


def envoyer(h, code):
    u32.PostMessageW(h, WM_KEYDOWN, code, 0)
    time.sleep(0.05)
    u32.PostMessageW(h, WM_KEYUP, code, 0)


def main():
    noms = [a.upper() for a in sys.argv[1:]]
    if not noms:
        print(__doc__)
        return 1
    h = fenetre()
    if not h:
        print('La borne n est pas ouverte (aucune fenetre de classe BorneAPM3).')
        return 1
    for n in noms:
        code = TOUCHES.get(n)
        if code is None:
            if len(n) == 1:
                code = ord(n)
            else:
                print('touche inconnue : %s' % n)
                return 1
        envoyer(h, code)
        print('  envoye : %s' % n)
        time.sleep(0.25)
    return 0


if __name__ == '__main__':
    sys.exit(main())
