#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pourquoi un appui sur Entree valide-t-il DEUX fois ?

Constat de Frederic, tenace : « la double validation est toujours presente »,
y compris apres avoir ramene la fenetre de `Input_isOnNow` de 150 ms a 20 ms.
Ma premiere cause etait donc fausse, ou incomplete.

Deux explications restent, et une seule mesure les separe :

  A. LE PREDICAT rend « presse » plusieurs fois pour un seul appui.
     `0x1801A2BC0` lit `Input_isOnNow(7)` et rend 0 si presse, -1 sinon. Si le
     stub garde la fenetre ouverte plus d'une trame, le curseur partage voit
     deux fronts.

  B. LE CURSEUR TOURNE DEUX FOIS PAR TRAME. Le meme `0x1801BBBE0` est appele
     par la mise a jour de la page ET par autre chose ; un seul front suffit
     alors a valider deux fois.

Points d'arret :

    0x1801BBBE0  chaque tour du curseur partage
    0x1801BBCE4  le resultat du predicat de validation (eax >= 0 = presse)
    0x1801A8090  le gestionnaire de validation de la liste d'options

Chaque evenement est horodate : deux validations dans la meme milliseconde
designent B, deux validations espacees d'une trame designent A.

    py -3 tools/pister_validation.py
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
POINTS = [
    ('Curseur', 0x1BBBE0),
    ('Predicat', 0x1BBCE4),
    ('Valider', 0x1A8090),
]
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')


def main():
    argv = sys.argv[1:]
    secondes = 300
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 200
    journal = os.path.join(RACINE, 'analysis', 'pister_validation.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'compte': collections.Counter(), 'recit': [],
          'presse': 0, 't0': None}

    def sur_bp(d, bp, ctx, tid):
        et['compte'][bp.nom] += 1
        if et['t0'] is None:
            et['t0'] = time.time()
        ms = (time.time() - et['t0']) * 1000.0
        if bp.nom == 'Predicat':
            if (ctx.Rax & 0x80000000) == 0:          # eax >= 0 : presse
                et['presse'] += 1
                if len(et['recit']) < 120:
                    et['recit'].append('%9.1f ms  PREDICAT : presse' % ms)
        elif bp.nom == 'Valider':
            if len(et['recit']) < 120:
                et['recit'].append('%9.1f ms  VALIDER (0x1801A8090)' % ms)

    def tic(d, t):
        if et['pose'] or t < 8.0:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        for nom_, rva in POINTS:
            bp = instrument.PointArret(nom_, b + rva, max_coups=400000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  points d\'arret poses a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    print('MESURE : d\'ou vient la double validation.')
    print()
    print('  Le jeu va se lancer. Faites CECI, et rien d\'autre :')
    print('     deux fois Entree            -> menu console')
    print('     descendez sur OPTIONS, validez UNE SEULE FOIS')
    print('     puis fermez le jeu tout de suite.')
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
    dit('=' * 70)
    dit('COMPTES :')
    for nom_, _ in POINTS:
        dit('   %-12s %d' % (nom_, et['compte'][nom_]))
    dit('   dont « presse » : %d' % et['presse'])
    dit()
    if et['compte']['Curseur'] and et['compte']['Predicat']:
        r = float(et['compte']['Predicat']) / et['compte']['Curseur']
        dit('Predicat par tour de curseur : %.2f   (1.00 attendu)' % r)
    dit()
    dit('RECIT HORODATE :')
    for t in et['recit']:
        dit('   ' + t)
    dit()
    dit('LECTURE :')
    dit('   deux PREDICAT presses a une trame d ecart (~17 ms) -> la FENETRE')
    dit('        du stub reste ouverte trop longtemps : baisser `front`.')
    dit('   un seul PREDICAT mais deux VALIDER -> le curseur partage tourne')
    dit('        DEUX FOIS par trame : c est un site d appel a fermer.')
    bilan = os.path.join(RACINE, 'analysis', 'pister_validation_bilan.txt')
    with open(bilan, 'w', encoding='utf-8') as fp:
        fp.write(os.linesep.join(lignes) + os.linesep)
    print()
    print('bilan ecrit dans %s' % bilan)
    return 0


if __name__ == '__main__':
    sys.exit(main())
