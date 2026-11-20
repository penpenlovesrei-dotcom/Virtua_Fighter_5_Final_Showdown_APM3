#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE MENU PRINCIPAL EST-IL ENCORE LA PENDANT LE `CHARACTER SELECT` ?

POURQUOI (2026-10-12). Le decor du TERMINAL a ete deplace a l etat 40 du
sequenceur 0x1801C3D60 : mesure, il s y charge bien, APRES les deux ecrans de
selection. Et l ecran est PIRE -- le `Character Select` flotte sur un fond
vide. La capture console, elle, le montre PAR-DESSUS LE MENU PRINCIPAL, dont
le sous-menu TERMINAL est encore ouvert.

Il ne s agit donc pas de l instant du decor mais de LA SURVIE DU MENU. Avant
d y toucher, on mesure : pendant l etat 10 du sequenceur -- les deux ecrans de
selection -- la page du menu principal est-elle encore MISE A JOUR, encore
DESSINEE, ou plus rien ?

  . 0x1801DC620  creneau 2 de la page du menu principal -- sa mise a jour
                 (un seul pointeur dans tout le binaire, 0x180532AF8)
  . 0x1801E0C80  creneau 4 -- son dessin
  . 0x1801C3D60  le sequenceur des ecrans, pour situer l etat

On compte les passages par seconde, et on les met en regard de l etat.

    py -3 tools/sonde_menu_vivant.py [--secondes N]

Journal : analysis/sonde_menu_vivant.txt
"""
import os
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                              # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
EXE = os.path.join(JEU, 'vfes.exe')
SCENARIO_ACTIF = os.path.join(JEU, 'apm_entrees.txt')
REF = os.path.join(ICI, 'apm_entrees.txt')

POINTS = (('MAJ', 0x1DC620), ('DESS', 0x1E0C80), ('SEQ', 0x1C3D60))

# QUATRE HAUT, ET NON TROIS BAS -- correction du 2026-10-12, sur
# remarque de Frederic : « quand tu navigues tu ne prends pas en compte
# que la manette n est pas connectee ». Sans manette, --versus-manette
# grise OFFLINE VERSUS et le curseur la saute : le nombre de crans
# jusqu a VF.TERMINAL change. En remontant, non -- les entrees 9, 8 et 7
# ne grisent JAMAIS et l entree 6 grise TOUJOURS, donc quatre HAUT
# depuis SINGLE PLAYER tombent sur VF.TERMINAL dans les deux cas.
APPUIS = [(18000, 'start', 'titre'), (24000, 'start', 'titre'),
          (30000, '2', 'haut'), (31500, '2', 'haut'),
          (33000, '2', 'haut'), (34500, '2', 'haut'),
          (36000, 'start', 'ENTRER DANS VF.TERMINAL'),
          (43000, 'start', 'VALIDER 1'),
          (51000, 'start', 'VALIDER 2')]


def scenario():
    seq = ['0       rien']
    for ms, code, _ in APPUIS:
        seq += ['%d   %s' % (ms, code), '%d   rien' % (ms + 400)]
    return '\n'.join(seq) + '\n'


def main():
    argv = sys.argv[1:]
    secondes = 64
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    ref = open(REF, encoding='latin-1', newline='').read()
    assert '0       rien\n' in ref, 'apm_entrees.txt sans sa ligne « 0 rien »'
    with open(SCENARIO_ACTIF, 'w', encoding='latin-1', newline='\n') as fp:
        fp.write(ref.replace('0       rien\n', scenario(), 1))

    journal = os.path.join(RACINE, 'analysis', 'sonde_menu_vivant.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = True
    dbg.bp_max = 40000000
    dbg.sortie = fichier
    et = {'poses': False, 'etat': None, 'n': {}, 'ligne': [], 'seconde': -1}

    def sur_bp(d, bp, ctx, tid):
        et['n'][bp.nom] = et['n'].get(bp.nom, 0) + 1
        if bp.nom != 'SEQ':
            return
        try:
            et['etat'] = d.u32(ctx.Rcx + 0x7C)
        except Exception:
            pass

    def tic(d, t):
        if not et['poses']:
            b = d.base_de(MOTEUR)
            if not b:
                return
            et['poses'] = True
            for nom, rva in POINTS:
                bp = instrument.PointArret(nom, b + rva, max_coups=40000000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)
            return
        s = int(t)
        if s == et['seconde']:
            return
        et['seconde'] = s
        n = et['n']
        et['ligne'].append((s, n.get('MAJ', 0), n.get('DESS', 0),
                            n.get('SEQ', 0), et['etat']))
        et['n'] = {}

    dbg.on_bp = sur_bp
    dbg.tic = tic

    print('SONDE : le menu principal survit-il au Character Select ?')
    print('  Le scenario conduit seul. Ne touchez a rien.')
    print()
    try:
        dbg.run(EXE, JEU, secondes, ())
    finally:
        fichier.close()
        import shutil
        shutil.copyfile(REF, SCENARIO_ACTIF)

    print('=' * 68)
    print(' seconde   menu:maj   menu:dessin   sequenceur   etat')
    for s, a, b, c, e in et['ligne']:
        if a == b == c == 0:
            continue
        print('   %4d     %6d       %6d       %6d     %s'
              % (s, a, b, c, '-' if e is None else e))
    print('=' * 68)
    print('LES APPUIS : ' + ', '.join('%.1f s %s' % (m / 1000.0, q)
                                      for m, _, q in APPUIS))
    return 0


if __name__ == '__main__':
    sys.exit(main())
