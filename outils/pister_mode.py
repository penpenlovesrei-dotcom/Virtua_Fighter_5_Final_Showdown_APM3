#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QUI pose le mode de jeu, quand, et avec quelle valeur.

Frederic, apres l'essai de `--sp-mode` : « je pense que c'est le mode arcade
qui est lance ». C'est une observation, donc un point de depart d'analyse. Trois
explications la produisent toutes les trois, et une seule mesure les separe :

  A. LA GREFFE N'EST PAS ATTEINTE. Les deux gardes d'animation de la mise a
     jour (`0x1801BD9D0`, puis `0x1801BD9C0` sur `[page+0x240]`) ne retombent
     pas dans ce build : le site `0x1801DD73E` n'est jamais execute, le mode
     reste a 0, et 0 est Arcade.

  B. LA GREFFE EST ATTEINTE MAIS TROP TARD. Elle pose bien 1, mais apres que le
     combat a lu le mode -- l'ordre des evenements le dira.

  C. QUELQU'UN REPOSE 0 PAR-DESSUS. `TaskMenuMain::update` pose le mode 0 en
     `0x1801DCC63` (`xor ecx,ecx ; call 0x18019C420`), et le menu console tourne
     encore sous le combat. Un seul passage apres le notre suffit a tout
     ramener en Arcade.

La mesure les distingue sans ambiguite : chaque ecriture du mode est notee avec
sa VALEUR et l'ADRESSE DE RETOUR de son appelant -- donc le site exact qui l'a
posee. Et a chaque evenement on relit le bloc de seize octets `0x180751010`,
qui porte le mode, la sante, le temps, les rounds et le niveau CPU.

Les cinq setters sont couverts : le balayage lineaire de `mode_de_jeu.md` §3 en
denombre CINQ, et pas un de plus, pour huit references en tout dans `.text`.

    tools/pister_mode.cmd          (applique le build d'essai, puis mesure)
"""
import collections
import os
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                            # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
MODE_GLOBAL = 0x751010                                       # RVA du bloc

# Les CINQ setters du mode (mode_de_jeu.md §3), plus nos deux cavernes, plus le
# consommateur qui lit le mode au demarrage du combat.
POINTS = [
    ('SetterBloc',   0x19C4A0),   # (type, reglages, annexe, echanger) mode 1
    ('SetterSolo',   0x19C420),   # (type, reglages, niveau, echanger) modes 0/2/3
    ('SetterVersus', 0x19C520),   # (type, reglages, annexe)           mode 4
    ('SetterTrain',  0x19C3D0),   # (type, annexe, demander_mode)      modes 6-8
    ('SetterSeul',   0x19C490),   # (type) -- le mode SEUL, plus utilise
    ('CaverneSA',    0x1A7058),   # notre greffe Score Attack
    ('CaverneLC',    0x1A71D8),   # notre greffe License Challenge
    ('ModeLu',       0x0B8BA4),   # juste apres `call 0x18019C090` : eax = mode
    ('DemandeMode',  0x0DA9A0),
    ('DemandeSsEtat', 0x0DA9C0),
]
SETTERS = {'SetterBloc', 'SetterSolo', 'SetterVersus', 'SetterTrain',
           'SetterSeul'}
NOMS = ['Arcade', 'Score Attack', 'License Challenge', 'Special Sparring',
        'Versus', '(5, jamais ecrit)', 'Free Training', 'Command Training',
        '(8, 3e ligne du Dojo)', '(9, jamais ecrit)']
# Les sites d'ecriture connus, indexes par l'ADRESSE DE RETOUR (le site + 5),
# pour nommer l'appelant sans avoir a le chercher.
SITES = {
    0x1801DC3AB: 'TaskMenuArcadeNormal::update (mode 0)',
    0x1801DCC68: 'TaskMenuMain::update (mode 0)',
    0x1801DD743: 'TaskMenuScoreAttack::update (mode 1)',
    0x1801DC17E: 'TaskMenuArcadeLicenceChallenge::update (mode 2)',
    0x1801A4257: 'TaskMenuTeam::update (mode 3)',
    0x1801DDC48: 'TaskMenuVersus::update (mode 4)',
    0x1801DCB70: 'TaskMenuMain::update (mode 4)',
    0x1801DDAB3: 'TaskMenuTraining::update (mode 6)',
    0x1801DDA66: 'TaskMenuTraining::update (modes 6/7/8)',
    0x1801A7061: 'NOTRE caverne Score Attack',
    0x1801A71E1: 'NOTRE caverne License Challenge',
    0x18023A42C: 'chemin APM3 (mode 0)',
    0x18023C72C: 'chemin APM3 (mode 0)',
    0x1800DE00B: 'gestionnaire de mode (mode 4)',
    0x1801BB666: 'fin de boucle (mode 4)',
}
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')


def main():
    argv = sys.argv[1:]
    secondes = 300
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 400
    journal = os.path.join(RACINE, 'analysis', 'pister_mode.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'compte': collections.Counter(), 'recit': [],
          't0': None, 'base': None, 'dernier_lu': None}

    def note(txt):
        # Au fil de l'eau : le debogueur se bloque parfois en fin de session
        # (piege connu), et un bilan ecrit seulement a la fin serait perdu.
        et['recit'].append(txt)
        fichier.write(txt + os.linesep)
        fichier.flush()

    def bloc(d):
        """Les seize octets du bloc de reglages, en clair."""
        b = d.read(et['base'] + MODE_GLOBAL, 16) or bytes(16)
        mode = int.from_bytes(b[0:4], 'little')
        return ('mode=%d %-18s sante=%d/%d temps=%d rounds=%d cpu=%d'
                % (mode, NOMS[mode] if mode < 10 else '?',
                   int.from_bytes(b[4:6], 'little'),
                   int.from_bytes(b[6:8], 'little'), b[8], b[9], b[10]))

    def sur_bp(d, bp, ctx, tid):
        et['compte'][bp.nom] += 1
        if et['t0'] is None:
            et['t0'] = time.time()
        ms = (time.time() - et['t0']) * 1000.0
        if len(et['recit']) >= 250:
            return
        if bp.nom in SETTERS:
            mode = ctx.Rcx & 0xFFFFFFFF
            ret = d.u64(ctx.Rsp) or 0
            # La DLL n'est PAS chargee a sa base preferee : l'adresse de retour
            # est relogee (0x7FFB.... au lieu de 0x1801.....). Il faut la
            # ramener a la VA statique pour la nommer, sinon `SITES` ne trouve
            # jamais rien -- defaut vu sur le releve du 2026-09-05, ou notre
            # propre caverne n'a pas ete reconnue.
            stat = ret - et['base'] + 0x180000000 if et['base'] else ret
            note('%9.1f ms  ECRITURE mode=%d (%s)  par 0x%X  %s'
                 % (ms, mode, NOMS[mode] if mode < 10 else '?', stat,
                    SITES.get(stat, '(site inconnu)')))
        elif bp.nom in ('CaverneSA', 'CaverneLC'):
            note('%9.1f ms  >>> NOTRE CAVERNE %s ATTEINTE  (%s)'
                 % (ms, bp.nom[-2:], bloc(d)))
        elif bp.nom == 'ModeLu':
            v = ctx.Rax & 0xFFFFFFFF
            if v != et['dernier_lu']:          # on ne note que les CHANGEMENTS
                et['dernier_lu'] = v
                note('%9.1f ms  LE COMBAT LIT le mode %d (%s)   %s'
                     % (ms, v, NOMS[v] if v < 10 else '?', bloc(d)))
        elif bp.nom == 'DemandeMode':
            note('%9.1f ms  demande de MODE %d' % (ms, ctx.Rcx & 0xFFFFFFFF))
        elif bp.nom == 'DemandeSsEtat':
            note('%9.1f ms  demande de SOUS-ETAT %d'
                 % (ms, ctx.Rcx & 0xFFFFFFFF))

    def tic(d, t):
        if et['pose'] or t < 8.0:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        et['base'] = b
        for nom_, rva in POINTS:
            bp = instrument.PointArret(nom_, b + rva, max_coups=400000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  points d\'arret poses a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    print('MESURE : qui pose le mode de jeu, et qui le repose.')
    print()
    print('  Le jeu va se lancer. Faites CECI, et rien d\'autre :')
    print('     deux fois Entree               -> menu console')
    print('     SINGLE PLAYER, validez')
    print('     SCORE ATTACK, validez')
    print('     dans la page de reglages, validez')
    print('     laissez le combat demarrer, puis fermez le jeu.')
    print()
    print('  Moins vous appuyez, plus le releve est lisible.')
    print()
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    lignes = []

    def dit(txt=''):
        lignes.append(txt)
        print(txt)

    dit()
    dit('=' * 72)
    dit('COMPTES :')
    for nom_, _ in POINTS:
        dit('   %-14s %d' % (nom_, et['compte'][nom_]))
    dit()
    dit('RECIT HORODATE :')
    for t in et['recit']:
        dit('   ' + t)
    dit()
    dit('LECTURE :')
    dit('   CaverneSA a 0 coup            -> cause A : la mise a jour n atteint')
    dit('                                    jamais le site. Les gardes')
    dit('                                    d animation ne retombent pas.')
    dit('   CaverneSA atteinte, puis une ECRITURE mode=0 apres elle')
    dit('                                 -> cause C : quelqu un repose 0.')
    dit('                                    L adresse de retour le nomme.')
    dit('   CaverneSA atteinte, aucune ecriture apres, mais LE COMBAT LIT 0')
    dit('                                 -> cause B : trop tard, ou le combat')
    dit('                                    lit autre chose que ce bloc.')
    bilan = os.path.join(RACINE, 'analysis', 'pister_mode_bilan.txt')
    with open(bilan, 'w', encoding='utf-8') as fp:
        fp.write(os.linesep.join(lignes) + os.linesep)
    print()
    print('bilan ecrit dans %s' % bilan)
    return 0


if __name__ == '__main__':
    sys.exit(main())
