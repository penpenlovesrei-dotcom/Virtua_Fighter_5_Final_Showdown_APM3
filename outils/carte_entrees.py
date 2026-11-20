#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cartographie les codes d'entree d'apm.dll vers les bits du masque du combattant.

Le sens des codes 2 a 14 n'etait pas etabli. Les chercher a l'ecran ne marche
pas : l'ecran de combat est anime et l'adversaire bouge, l'ecran de selection est
anime lui aussi, et une capture ne photographie que la ZONE D'ECRAN de la fenetre
-- donc n'importe quelle fenetre posee dessus. Ici on ne capture rien : on LIT LA
MEMOIRE.

Le moteur range l'etat des boutons dans `ROB+0x508` (masque courant) et
`ROB+0x510` (masque tamponne) -- les champs que consultent les gestionnaires 20 a
24 et 51 de la liste 2. Il suffit donc de tenir un code a la fois et de regarder
quels bits s'allument.

Deux precautions, apprises a la premiere passe :

 * on ne sait pas d'avance quel ROB est celui du JOUEUR. On en releve donc DEUX
   (les deux premiers combattants vus passer) et on mesure sur les deux : celui
   qui reagit a nos appuis est le bon, et il se designe tout seul.
 * l'adversaire gere par la machine bouge pendant la mesure. Un seul passage ne
   prouve rien : on repete la sequence et on ne retient que les bits qui
   reapparaissent.

Usage :
    py -3 tools/carte_entrees.py
    py -3 tools/carte_entrees.py --codes 2,3,4,5 --passes 4
"""
import collections
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
MOTH_APPLY_RECORD = 0x158B40
SET_STATE = 0x0DA800          # SetState(ecx = etat, edx = sous-etat)
APM3_GAME_VS = 50             # sous-etats : voir tools/tracer_etats.py
APM3_TRAINING = 52
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')
DEPART = os.path.join(RACINE, 'tools', 'scenarios', 'combat_martelage.txt')
CHAMPS = [0x508, 0x510]


def ecrire(codes):
    with open(SCENARIO, 'w', encoding='ascii', newline='\n') as fp:
        fp.write('# ecrit par tools/carte_entrees.py\nfront = 400\njournal = 0\n'
                 '0 %s\n' % (codes or 'rien'))


def main():
    argv = sys.argv[1:]
    codes = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14]
    secondes, pose_a, pause, passes = 400, 55.0, 0.9, 3
    if '--codes' in argv:
        codes = [int(x, 0) for x in argv[argv.index('--codes') + 1].split(',')]
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--a' in argv:
        pose_a = float(argv[argv.index('--a') + 1])
    if '--pause' in argv:
        pause = float(argv[argv.index('--pause') + 1])
    if '--passes' in argv:
        passes = int(argv[argv.index('--passes') + 1])
    journal = os.path.join(RACINE, 'analysis', 'carte_entrees.txt')

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 8
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier

    # --dojo : devier le sous-etat APM3_GAME_VS vers APM3_TRAINING au moment ou
    # le jeu le demande. Le partenaire d'entrainement ne bouge pas : c'est la
    # seule facon d'obtenir une mesure propre, l'adversaire gere par la machine
    # ayant fait echouer toutes les passes precedentes.
    dojo = '--dojo' in argv
    et = {'pose': False, 'robs': [], 'phase': 0, 'quand': 0.0, 'i': 0,
          'passe': 0, 'repos': None, 'fini': False, 'devie': False}
    # (code, index de ROB) -> Counter des masques XOR observes
    releve = collections.defaultdict(collections.Counter)

    def sur_bp(d, bp, ctx, tid):
        if bp.nom == 'SetState':
            if dojo and (ctx.Rdx & 0xFFFFFFFF) == APM3_GAME_VS:
                ctx.Rdx = APM3_TRAINING
                ctx.ContextFlags = (instrument.CONTEXT_FULL
                                    | instrument.CONTEXT_DEBUG_REGISTERS)
                d.poser_contexte(tid, ctx)
                et['devie'] = True
                d.dire('  sous-etat devie : APM3_GAME_VS -> APM3_TRAINING')
            return
        if ctx.Rdx and ctx.Rdx not in et['robs']:
            et['robs'].append(ctx.Rdx)
            d.dire('  ROB %d = 0x%X' % (len(et['robs']), ctx.Rdx))
        if len(et['robs']) >= 2:
            d.desarmer_logiciel(bp)

    def lire(d):
        return [tuple(d.u32(r + o) or 0 for o in CHAMPS) for r in et['robs']]

    def tic(d, t):
        if et['fini']:
            return
        # la deviation doit etre en place AVANT que le jeu demande APM3_GAME_VS,
        # c'est-a-dire des le chargement du moteur -- pas au moment de la mesure
        if dojo and not et.get('sb') and t >= 10:
            b = d.base_de(MOTEUR)
            if b:
                sb = instrument.PointArret('SetState', b + SET_STATE, max_coups=10000)
                sb.silencieux = True
                d.bps.append(sb)
                d.armer_logiciel(sb)
                et['sb'] = True
        if not et['pose']:
            if t < pose_a:
                return
            b = d.base_de(MOTEUR)
            if not b:
                return
            et['pose'] = True
            bp = instrument.PointArret('MothApplyRecord', b + MOTH_APPLY_RECORD,
                                       max_coups=8)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
            return
        if not et['robs'] or t < et['quand']:
            return
        if et['phase'] == 0:
            ecrire('rien')
            et['phase'] = 1
            et['quand'] = t + pause
            return
        if et['phase'] == 1:
            et['repos'] = lire(d)
            ecrire(str(codes[et['i']]))
            et['phase'] = 2
            et['quand'] = t + pause
            return
        c = codes[et['i']]
        tenu = lire(d)
        for k in range(len(tenu)):
            x = tuple(a ^ b for a, b in zip(et['repos'][k], tenu[k]))
            releve[(c, k)][x] += 1
            if any(x):
                d.dire('  passe %d code %-3d ROB%d : %s -> %s  xor %s'
                       % (et['passe'], c, k + 1,
                          ' '.join('%08X' % v for v in et['repos'][k]),
                          ' '.join('%08X' % v for v in tenu[k]),
                          ' '.join('%08X' % v for v in x)))
        et['i'] += 1
        et['phase'] = 0
        et['quand'] = t + 0.05
        if et['i'] >= len(codes):
            et['i'] = 0
            et['passe'] += 1
            d.dire('  --- passe %d terminee ---' % et['passe'])
            if et['passe'] >= passes:
                et['fini'] = True

    dbg.on_bp = sur_bp
    dbg.tic = tic

    if os.path.exists(DEPART):
        with open(DEPART, 'rb') as fp:
            data = fp.read()
        with open(SCENARIO, 'wb') as fp:
            fp.write(data)
    print('journal : %s ; %d passes sur %d codes' % (journal, passes, len(codes)))
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()
    ecrire('rien')

    print('\n--- carte des entrees (bits reapparaissant sur plusieurs passes) ---')
    print('%-6s %-38s %s' % ('code', 'ROB 1', 'ROB 2'))
    for c in codes:
        cols = []
        for k in (0, 1):
            cpt = releve.get((c, k), collections.Counter())
            stables = [x for x, n in cpt.items() if any(x) and n >= 2]
            if stables:
                cols.append(' '.join('+0x%X^%08X' % (CHAMPS[j], x[j])
                                     for x in stables for j in range(len(CHAMPS))
                                     if x[j]))
            else:
                bruit = sum(n for x, n in cpt.items() if any(x))
                cols.append('-' if not bruit else '(%d changement(s) non repete(s))' % bruit)
        print('%-6d %-38s %s' % (c, cols[0][:38], cols[1][:38]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
