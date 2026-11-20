#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Coupe le son d'un seul processus, sans toucher au volume general de Windows.

Les campagnes de pistage font tourner vfes.exe plusieurs minutes d'affilee, en
arriere-plan : autant qu'il se taise. Windows tient un volume par session audio ;
on retrouve la session dont l'identifiant de processus est celui du jeu et on la
met en sourdine. Rien d'autre sur la machine n'est modifie.

Le processus doit avoir ouvert sa sortie audio pour que sa session existe : il
faut donc l'appeler APRES le lancement. Le mode --surveiller attend l'apparition
du processus, puis le met en sourdine des que sa session apparait, et reessaie
tant qu'elle n'est pas la (le moteur ouvre le son quelques secondes apres le
demarrage).

Usage :
    py -3 tools/muet.py                        met vfes.exe en sourdine
    py -3 tools/muet.py --rendre               lui rend le son
    py -3 tools/muet.py --surveiller 180       attend et coupe, pendant 180 s
    py -3 tools/muet.py --lister               les sessions audio en cours
"""
import os
import sys
import time

from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

DEFAUT = 'vfes.exe'


def sessions():
    out = []
    for s in AudioUtilities.GetAllSessions():
        nom = ''
        try:
            if s.Process:
                nom = s.Process.name()
        except Exception:
            pass
        out.append((s, nom))
    return out


def agir(cible, muet):
    n = 0
    for s, nom in sessions():
        if nom.lower() == cible.lower():
            vol = s._ctl.QueryInterface(ISimpleAudioVolume)
            vol.SetMute(1 if muet else 0, None)
            n += 1
    return n


def main():
    argv = sys.argv[1:]
    cible = DEFAUT
    for a in argv:
        if a.lower().endswith('.exe'):
            cible = a

    if '--lister' in argv:
        for s, nom in sessions():
            pid = ''
            try:
                pid = s.ProcessId
            except Exception:
                pass
            print('%-24s pid=%s' % (nom or '(systeme)', pid))
        return 0

    if '--surveiller' in argv:
        i = argv.index('--surveiller')
        duree = float(argv[i + 1]) if len(argv) > i + 1 and not argv[i + 1].startswith('-') \
            else 120.0
        t0 = time.time()
        fait = 0
        while time.time() - t0 < duree:
            n = agir(cible, True)
            if n and not fait:
                print('%s en sourdine (%d session(s)) apres %.0f s'
                      % (cible, n, time.time() - t0))
                fait = n
            time.sleep(1.0)
        if not fait:
            print('aucune session audio pour %s pendant %.0f s' % (cible, duree))
        return 0

    rendre = '--rendre' in argv
    n = agir(cible, not rendre)
    if n:
        print('%s : %d session(s) %s' % (cible, n, 'rendue(s)' if rendre else 'en sourdine'))
    else:
        print('aucune session audio pour %s (le processus tourne-t-il, et a-t-il '
              'ouvert le son ?)' % cible)
    return 0 if n else 1


if __name__ == '__main__':
    sys.exit(main())
