#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VGA ou WXGA : quelle variante d'affichage le selecteur charge-t-il ?

La planche `aet_s_selcha` porte deux scenes (tools/aet.py) :

    VGA_MAIN    113 compositions  --  Dural : ZERO calque
    WXGA_MAIN   174 compositions  --  Dural : trois calques

et le choix tient a l'octet `[0x1806490D0 + 0x20]`, lu a 54 endroits de
l'interface. En `0x1801700B0` il devient un identifiant de scene :

    0x1801703F7  cmp   byte [0x1806490D0 + 0x20], bl
    0x1801703FA  setne r13b                            ; 0 = VGA, 1 = WXGA
    0x1801704FE  lea   r8d, [r13 + 0x149]              ; 0x149 ou 0x14A

Ce script releve `r13` et `r8` a ce site : c'est la reponse directe, sans avoir
a juger a l'ecran si l'interface « a l'air » differente.

    py -3 tools/pister_vga.py
"""
import collections
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
SITE = 0x1704FE               # RVA : lea r8d, [r13 + 0x149]
SITE_GRILLE = 0x170D86        # RVA : r14d porte l identifiant de scene choisi
SCENES = {0x149: 'VGA_MAIN', 0x14A: 'WXGA_MAIN', 0x14B: '0x14B', 0x14C: '0x14C'}
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')


def main():
    argv = sys.argv[1:]
    secondes, pose_a = 90, 8.0
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'rester_grille.txt')
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 100000
    journal = os.path.join(RACINE, 'analysis', 'pister_vga.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'vus': collections.Counter(),
          'grille': collections.Counter()}

    def sur_bp(d, bp, ctx, tid):
        if bp.nom == 'Grille':
            et['grille'][ctx.R14 & 0xFFFFFFFF] += 1
            return
        et['vus'][(ctx.R13 & 0xFF, (ctx.R13 + 0x149) & 0xFFFFFFFF)] += 1

    def tic(d, t):
        if et['pose'] or t < pose_a:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        for n_, rva_ in (('VariantAffichage', SITE), ('Grille', SITE_GRILLE)):
            bp = instrument.PointArret(n_, b + rva_, max_coups=100000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  point d\'arret sur le choix de variante, a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic
    if scenario and os.path.exists(scenario):
        with open(scenario, 'rb') as fp:
            data = fp.read()
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(data)
    print('journal : %s' % journal)
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    print()
    if not et['vus']:
        print('--- AUCUN passage : le site n a pas ete atteint ---')
        return 0
    if et['grille']:
        print('--- scene choisie AU SITE DE LA GRILLE (0x180170D86) ---')
        for ident, n in et['grille'].most_common():
            print('   r14 = 0x%X  (%s)   %d passage(s)'
                  % (ident, SCENES.get(ident, '?'), n))
        print()
    print('--- variante d affichage choisie par le selecteur ---')
    for (r13, ident), n in et['vus'].most_common():
        print('   r13 = %d  ->  scene 0x%X  (%s)   %d passage(s)'
              % (r13, ident, 'WXGA' if r13 else 'VGA', n))
    return 0


if __name__ == '__main__':
    sys.exit(main())
