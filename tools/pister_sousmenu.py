#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pourquoi le menu principal bouge-t-il encore quand un sous-menu est ouvert ?

Constat de Frederic : « quand je me deplace dans un sous menu, les directions
agissent aussi sur le menu principal situe en arriere plan ».

Le mecanisme voulu est pourtant ECRIT, et il est correct. Ouvrir un sous-menu
demarre sa scene et range la sous-page dans `[menu + 0x650]` :

    0x1801DE06F  call 0x180245830          ; demarrer la scene du sous-menu
    0x1801DE074  test al, al
    0x1801DE076  je   sortie               ; ECHEC -> [menu+0x650] reste vide
    ...          mov  [rdi+0x650], rbx     ; SUCCES -> la sous-page est rangee

et la mise a jour du menu principal (`0x1801DC620`) se coupe des sa premiere
instruction quand cette case est remplie :

    0x1801DC63D  mov  rcx, [rdi+0x650]
    0x1801DC644  test rcx, rcx
    0x1801DC647  je   suite                ; vide -> le menu principal continue
    0x1801DC649  call 0x180244EA0          ; la sous-page est-elle vivante ?
    0x1801DC650  jne  0x1801DCE33          ; OUI -> on rend la main sans rien lire

Le curseur du menu principal n'est touche qu'apres, en fin de fonction :

    0x1801DD118  lea  rcx, [rdi+0x348]     ; un dialogue est-il ouvert ?
    0x1801DD126  jne  sortie
    0x1801DD12B  call 0x1801BBBE0          ; <- le curseur partage

Deux causes possibles, et une seule mesure les separe :

  A. `[menu+0x650]` est VIDE  -> l'ouverture n'a pas ete enregistree
     (`0x180245830` a rendu faux : la scene du sous-menu ne demarre pas).
  B. `[menu+0x650]` est REMPLI mais `0x180244EA0` rend faux
     -> la sous-page est jugee morte alors qu'elle est a l'ecran.

Trois points d'arret repondent :

    0x1801DC64E   apres le test de vivacite : on lit [rdi+0x650] et al
    0x1801DD12B   le curseur du menu principal bouge
    0x1801DE074   une ouverture de sous-menu : a-t-elle reussi ?

Le clavier reste actif : c'est vous qui menez le jeu.

    py -3 tools/pister_sousmenu.py
    py -3 tools/pister_sousmenu.py --secondes 300
"""
import collections
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                            # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
GARDE = 0x1DC64E               # RVA : apres le test de vivacite
OUBLI = 0x1DC656               # RVA : on EFFACE la sous-page (jugee morte)
CURSEUR = 0x1DD12B             # RVA : le menu principal bouge son curseur
OUV_VERSUS = 0x1DDFCF          # RVA : OFFLINE VERSUS -- la scene a-t-elle pris ?
OUV_AUTRES = 0x1DE074          # RVA : DOJO / TERMINAL -- idem
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                              'apm_entrees.txt')
SCENARIO = """# ecrit par tools/pister_sousmenu.py -- le clavier mene.
front   = 200
journal = 0
clavier = 1
manette = 1
0       rien
"""


def main():
    argv = sys.argv[1:]
    secondes = 300
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 200
    journal = os.path.join(RACINE, 'analysis', 'pister_sousmenu.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'garde': collections.Counter(),
          'curseur': 0, 'ouvertures': collections.Counter(),
          'oubli': 0, 'recit': []}

    def note(txt):
        if len(et['recit']) < 60:
            et['recit'].append(txt)

    def sur_bp(d, bp, ctx, tid):
        if bp.nom == 'Garde':
            page = d.u64((ctx.Rdi & 0xFFFFFFFFFFFFFFFF) + 0x650) or 0
            vivante = ctx.Rax & 0xFF
            if vivante:
                et['garde']['sous-page rangee ET vivante'] += 1
            else:
                et['garde']['sous-page rangee mais JUGEE MORTE'] += 1
            note('GARDE  sous-page=0x%X  vivante=%d  (curseur deja bouge %d x)'
                 % (page, vivante, et['curseur']))
        elif bp.nom == 'Oubli':
            et['oubli'] += 1
            note('OUBLI  la sous-page est effacee de [menu+0x650]')
        elif bp.nom == 'Curseur':
            et['curseur'] += 1
        else:
            ok = ctx.Rax & 0xFF
            quoi = 'OFFLINE VERSUS' if bp.nom == 'OuvVersus' else 'DOJO/TERMINAL'
            et['ouvertures']['%s : %s' % (quoi, 'reussie' if ok else 'ECHOUEE')] += 1
            note('OUVRE  %s -> %s' % (quoi, 'reussie' if ok else 'ECHOUEE'))

    def tic(d, t):
        if et['pose'] or t < 8.0:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        for nom_, rva in (('Garde', GARDE), ('Oubli', OUBLI),
                          ('Curseur', CURSEUR),
                          ('OuvVersus', OUV_VERSUS),
                          ('OuvAutres', OUV_AUTRES)):
            bp = instrument.PointArret(nom_, b + rva, max_coups=200000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  points d\'arret poses a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)

    print('MESURE : pourquoi le menu principal lit-il encore les directions.')
    print()
    print('  Le jeu va se lancer. Faites CECI, et rien d\'autre :')
    print('     deux fois Entree           -> menu console')
    print('     descendez sur OFFLINE VERSUS, validez')
    print('     dans le sous-menu, appuyez HAUT et BAS plusieurs fois')
    print('     Echap pour revenir')
    print()
    print('  journal : %s' % journal)
    print()
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    lignes = []
    def dit(txt=''):
        lignes.append(txt)
        print(txt)

    dit()
    dit('=' * 68)
    dit('OUVERTURES DE SOUS-MENU :')
    if not et['ouvertures']:
        dit('   aucune -- aucun sous-menu ouvert par ces deux sites.')
    for k, n in et['ouvertures'].most_common():
        dit('   %-34s x%d' % (k, n))
    dit()
    dit('GARDE DU MENU PRINCIPAL (0x1801DC64E, atteinte seulement quand')
    dit('[menu+0x650] n est PAS vide) :')
    total = sum(et['garde'].values())
    if not total:
        dit('   JAMAIS atteinte -> [menu+0x650] est reste vide tout du long :')
        dit('   la sous-page n a jamais ete enregistree (cause A).')
    for k, n in et['garde'].most_common():
        dit('   %-34s %6d  (%4.1f %%)' % (k, n, 100.0 * n / total))
    dit()
    dit('SOUS-PAGE EFFACEE (0x1801DC656) : %d fois' % et['oubli'])
    dit('CURSEUR DU MENU PRINCIPAL DEPLACE (0x1801DD12B) : %d fois'
        % et['curseur'])
    dit()
    dit('RECIT (les 60 premiers evenements, dans l ordre) :')
    for t in et['recit']:
        dit('   ' + t)
    bilan = os.path.join(RACINE, 'analysis', 'pister_sousmenu_bilan.txt')
    with open(bilan, 'w', encoding='utf-8') as fp:
        fp.write(os.linesep.join(lignes) + os.linesep)
    print()
    print('bilan ecrit dans %s' % bilan)
    return 0


if __name__ == '__main__':
    sys.exit(main())
