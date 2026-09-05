#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quel decor l'ecran TERMINAL charge-t-il vraiment, et par quel chemin ?

Pourquoi cette mesure. Changer l'index code en dur dans la tache de decor de
l'ecran de personnalisation (`0x1801C4DD0`) n'a produit **aucune difference a
l'ecran** entre `ts2` (505 Ko), `trm` (1,3 Mo) et `ter` (16,7 Mo). Trois
archives de tailles aussi differentes ne peuvent pas donner la meme image :
le decor demande n'arrive donc pas a l'ecran, et l'index n'est pas la variable.

Or `0x1800D7130(index)` -- l'unique chargeur de decor -- a **deux** appelants :

    0x1801C4DD0   dans la tache de l'ecran de personnalisation, index EN DUR
    0x18018F8A3   dans le chargeur general, index lu dans `[rsi+0x5C]`

Un seul point d'arret, pose sur `0x1800D7130` lui-meme, repond a tout : on lit
`ecx` (l'index demande) et l'adresse de retour au sommet de la pile (donc
l'appelant). Si seul `0x18018F8A3` passe, patcher l'autre ne pouvait rien
changer -- et on saura quoi patcher.

Deux points d'arret secondaires disent si la tache avance :

    0x1801C4DBE   etape 1 : elle va demander le decor
    0x1801C4DE3   etape 2 : elle attend que le chargement finisse

Le clavier reste actif : c'est vous qui menez le jeu jusqu'a TERMINAL.

    py -3 tools/pister_decor.py
    py -3 tools/pister_decor.py --secondes 240
"""
import collections
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
CHARGEUR = 0x0D7130            # RVA de 0x1800D7130
ETAPE1 = 0x1C4DBE              # RVA : la tache va demander
ETAPE2 = 0x1C4DE3              # RVA : la tache attend le chargement
APPELANTS = {0x1801C4DD5: 'ECRAN DE PERSONNALISATION (index en dur)',
             0x18018F8A8: 'CHARGEUR GENERAL (index variable)'}
NOM = ['tst', 'ts2', 'ts3', 'wht', 'ban', 'ter', 'nyc', 'cas', 'riv', 'jin',
       'sin', 'djo', 'umi', 'hai', 'are', 'slk', 'yuk', 'tak', 'aur', 'bar',
       'tan', 'du1', 'du2', 'du3', 'du4', 'du5', 'trm', 'cid', 'trs', 'evo00',
       'evo01', 'evo02', 'evo03', 'evo04', 'evo05', 'evo06', 'evo07', 'evo08',
       'evo09', 'gym', 'smo']
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                              'apm_entrees.txt')
SCENARIO = """# ecrit par tools/pister_decor.py -- le clavier mene, on ne force rien.
front   = 200
journal = 0
clavier = 1
manette = 1
0       rien
"""


def main():
    argv = sys.argv[1:]
    secondes = 240
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 200
    journal = os.path.join(RACINE, 'analysis', 'pister_decor.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'charges': [], 'etapes': collections.Counter()}

    def sur_bp(d, bp, ctx, tid):
        if bp.nom == 'Chargeur':
            index = ctx.Rcx & 0xFFFFFFFF
            retour = d.u64(ctx.Rsp) or 0
            qui = APPELANTS.get(retour, 'appelant inconnu 0x%X' % retour)
            nom = NOM[index] if index < len(NOM) else '?%d' % index
            et['charges'].append((index, nom, qui))
            d.dire('  CHARGEMENT : index %d (%s)  <- %s' % (index, nom, qui))
        else:
            et['etapes'][bp.nom] += 1

    def tic(d, t):
        if et['pose'] or t < 8.0:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        for nom_, rva in (('Chargeur', CHARGEUR), ('Etape1', ETAPE1),
                          ('Etape2', ETAPE2)):
            bp = instrument.PointArret(nom_, b + rva, max_coups=5000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  points d\'arret poses a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)

    print('MESURE : quel decor est charge, et par quel chemin.')
    print()
    print('  Le jeu va se lancer. Allez jusqu\'a TERMINAL :')
    print('     deux fois Entree  ->  menu console')
    print('     descendre sur TERMINAL, valider')
    print('  Puis laissez tourner quelques secondes. Echap quitte un mode.')
    print()
    print('  journal : %s' % journal)
    print()
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    print()
    print('=' * 66)
    if not et['charges']:
        print('AUCUN chargement de decor pendant la mesure.')
        print('  -> la tache ne demande jamais de decor : ce n est pas l index.')
    else:
        print('CHARGEMENTS OBSERVES :')
        vus = collections.Counter(et['charges'])
        for (i, nom, qui), n in vus.most_common():
            print('   index %-3d %-6s  x%-4d  <- %s' % (i, nom, n, qui))
    print()
    print('ETAPES DE LA TACHE DE DECOR :')
    for nom_ in ('Etape1', 'Etape2'):
        n = et['etapes'][nom_]
        print('   %-8s %d passage(s)%s'
              % (nom_, n, '   <-- jamais atteinte' if n == 0 else ''))
    if et['etapes']['Etape2'] and not et['charges']:
        print()
        print('  L etape 2 tourne mais rien n est charge : le chargement est')
        print('  refuse en amont (l etape 1 attend que le chargeur soit libre).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
