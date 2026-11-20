#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA SUITE DES ÉTATS DU VRAI SÉQUENCEUR DU TERMINAL, relevée et non déduite.

POURQUOI (2026-10-12). Le correctif `--terminal-ordre` a rendu le chargement du
décor aux étapes 1, 2 et 3 de `CUST_MAIN` (`0x1801C2EC0`, sur `[objet+0x58]`).
C'était exact et insuffisant : ces étapes précèdent l'étape 10, et l'étape 10
n'est qu'un `call 0x1801C3D60` -- un SECOND séquenceur, sur `[objet+0x7C]`,
soixante-et-onze états, et c'est LUI qui tient le `Character Select` et le menu
`Customize`. Le décor se charge donc toujours avant les deux écrans.

Avant de déplacer quoi que ce soit, il faut savoir QUEL état ferme quel écran.
Cette sonde pose un point d'arrêt en tête de `0x1801C3D60` et note CHAQUE
CHANGEMENT de `[rcx+0x7C]`, avec l'instant. Le scénario d'entrées conduit seul
jusqu'au TERMINAL puis valide trois fois : les instants des appuis sont connus,
donc chaque transition se rattache à l'écran qui la provoque.

    py -3 tools/sonde_terminal.py [--secondes N]

Journal : analysis/sonde_terminal.txt
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

RVA_SEQ = 0x1C3D60          # customize : le sequenceur sur [objet+0x7C]
RVA_CUST = 0x1C2EC0         # CUST_MAIN : le sequenceur sur [objet+0x58]

# Les appuis, et ce qu'ils valent -- trois BAS sautent les lignes grisees et
# amenent sur VF.TERMINAL (0 -> 1 -> 4 -> 5), puis on valide quatre fois.
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
          (51000, 'start', 'VALIDER 2'),
          (59000, 'start', 'VALIDER 3')]


def scenario():
    seq = ['0       rien']
    for ms, code, _ in APPUIS:
        seq += ['%d   %s' % (ms, code), '%d   rien' % (ms + 400)]
    return '\n'.join(seq) + '\n'


def main():
    argv = sys.argv[1:]
    secondes = 72
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    ref = open(REF, encoding='latin-1', newline='').read()
    assert '0       rien\n' in ref, 'apm_entrees.txt sans sa ligne « 0 rien »'
    with open(SCENARIO_ACTIF, 'w', encoding='latin-1', newline='\n') as fp:
        fp.write(ref.replace('0       rien\n', scenario(), 1))

    journal = os.path.join(RACINE, 'analysis', 'sonde_terminal.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = True
    dbg.bp_max = 4000000
    dbg.sortie = fichier
    et = {'poses': False, 'seq': None, 'cust': None, 'suite': [], 't0': None}

    def sur_bp(d, bp, ctx, tid):
        if et['t0'] is None:
            et['t0'] = time.time()
        champ = 0x7C if bp.nom == 'SEQ' else 0x58
        try:
            v = d.u32(ctx.Rcx + champ)
        except Exception:
            return
        clef = (bp.nom, v)
        if et[bp.nom.lower()] == clef:
            return
        et[bp.nom.lower()] = clef
        t = time.time() - et['t0']
        et['suite'].append((t, bp.nom, v))
        d.dire('  %6.1f s   %-4s  etat = %d' % (t, bp.nom, v))

    def tic(d, t):
        if et['poses']:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['poses'] = True
        for rva, nom in ((RVA_SEQ, 'SEQ'), (RVA_CUST, 'CUST')):
            bp = instrument.PointArret(nom, b + rva, max_coups=4000000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  2 points poses (t=%.1f s)' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    print('SONDE : les etats du sequenceur de personnalisation.')
    print('  Le scenario conduit seul. Ne touchez a rien.')
    print('  journal : %s' % journal)
    print()
    try:
        dbg.run(EXE, JEU, secondes, ())
    finally:
        fichier.close()
        import shutil
        shutil.copyfile(REF, SCENARIO_ACTIF)
        print('  scenario retire : le clavier est rendu.')

    print()
    print('=' * 72)
    print('LES APPUIS DU SCENARIO :')
    for ms, code, quoi in APPUIS:
        print('   %5.1f s   %-6s  %s' % (ms / 1000.0, code, quoi))
    print()
    print('LES TRANSITIONS RELEVEES :')
    if not et['suite']:
        print('   AUCUNE -- le sequenceur n a pas tourne.')
    for t, nom, v in et['suite']:
        print('   %6.1f s   %-4s  etat = %d' % (t, nom, v))
    print('=' * 72)
    return 0


if __name__ == '__main__':
    sys.exit(main())
