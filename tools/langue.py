#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bascule le drapeau de region du moteur : Japon <-> export.

Trouve en remontant le choix `logo_jpn` / `logo_usu`. Le selecteur tient en
cinq instructions et ne depend que d'UN octet :

    0x1802447C0  movzx eax, byte ptr [0x18064D956]
    0x1802447C7  neg   al
    0x1802447C9  sbb   eax, eax
    0x1802447CB  and   eax, 2          ; rend 0 (Japon) ou 2 (export)
    0x1802447CE  ret

Quatre appelants, et ils ne choisissent pas que le logo :

    0x18006BBD1   logo_jpn  /  logo_usu
    0x1801AAF4F   ecrit [rdi+0x240] = 0 ou 2, puis appelle avec edx = 0x19
    0x1801BB077   les libelles de resultat : " W " et leur equivalent
    0x1801BB090   idem pour " L "

Usage :
    py -3 tools/langue.py --export      met l'octet a 1
    py -3 tools/langue.py --japon       le remet a 0
    py -3 tools/langue.py --export --captures 66:langue.png
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
DRAPEAU = 0x64D956            # l'octet de region, dans .data
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')


def main():
    argv = sys.argv[1:]
    val = 1 if '--export' in argv else (0 if '--japon' in argv else None)
    secondes = 100
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'select_a.txt')
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]
    captures = []
    if '--captures' in argv:
        for spec in argv[argv.index('--captures') + 1].split(','):
            t, chemin = spec.split(':', 1)
            captures.append((os.path.join(RACINE, 'analysis', chemin),
                             float(t), 'Virtua Fighter'))

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    journal = os.path.join(RACINE, 'analysis', 'langue.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'lu': False, 'n': 0}

    def tic(d, t):
        b = d.base_de(MOTEUR)
        if not b:
            return
        a = b + DRAPEAU
        cur = d.read(a, 1)
        if not cur:
            return
        if not et['lu']:
            et['lu'] = True
            d.dire('  drapeau de region a 0x%X : %d  (%s)'
                   % (a, cur[0], 'Japon' if cur[0] == 0 else 'export'))
        # on le remet a chaque tour : le moteur peut l'ecrire a son
        # initialisation, apres notre premier passage.
        if val is not None and cur[0] != val:
            d.write(a, bytes([val]))
            et['n'] += 1
            if et['n'] <= 3:
                d.dire('  [t=%.0f s] drapeau %d -> %d' % (t, cur[0], val))

    dbg.tic = tic
    if scenario and os.path.exists(scenario):
        with open(scenario, 'rb') as fp:
            data = fp.read()
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(data)
    print('drapeau vise : %s' % ('inchange' if val is None
                                 else ('export (1)' if val else 'Japon (0)')))
    dbg.run(EXE, os.path.dirname(EXE), secondes, tuple(captures))
    fichier.close()
    print('ecritures : %d   (journal : %s)' % (et['n'], journal))
    return 0


if __name__ == '__main__':
    sys.exit(main())
