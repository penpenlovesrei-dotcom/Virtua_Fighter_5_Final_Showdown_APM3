#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pourquoi SINGLE PLAYER ne lance-t-il rien ?

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
    ('ModeChoisi', 0x1DDD1D),      # la page des modes : quel mode est valide
    ('SceneMode', 0x1DDDC5),       # le demarrage de la scene du mode a-t-il pris
    ('SousPage', 0x1DBED4),        # la mise a jour voit-elle une sous-page
    ('Relais', 0x1A7046),          # notre relais : le predicat a-t-il dit OUI
    ('Caverne', 0x34579C),         # la caverne de transition est-elle appelee
    ('DemandeMode', 0x0DA9A0),     # une demande de MODE
    ('DemandeSousEtat', 0x0DA9C0), # une demande de SOUS-ETAT
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
    journal = os.path.join(RACINE, 'analysis', 'pister_sp.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'compte': collections.Counter(), 'recit': [],
          'presse': 0, 't0': None}

    et['vu'] = None

    def note(txt):
        # Ecrit IMMEDIATEMENT dans le journal : la mesure du 2026-09-05 s'est
        # bloquee (defaut connu du debogueur, voir reference_debogueur_win32_pieges)
        # et le bilan, ecrit seulement a la fin, a tout perdu.
        et['recit'].append(txt)
        fichier.write(txt + os.linesep)
        fichier.flush()

    def sur_bp(d, bp, ctx, tid):
        et['compte'][bp.nom] += 1
        if et['t0'] is None:
            et['t0'] = time.time()
        ms = (time.time() - et['t0']) * 1000.0
        if len(et['recit']) >= 120:
            return
        if bp.nom == 'ModeChoisi':
            n = int.from_bytes(
                d.read((ctx.Rcx & 0xFFFFFFFFFFFFFFFF) + 0x58, 4) or bytes(4),
                'little')
            noms = ['Arcade', 'Score Attack', 'License Challenge',
                    'Special Sparring']
            note('%9.1f ms  MODE CHOISI : %d (%s)'
                 % (ms, n, noms[n] if n < 4 else '?'))
        elif bp.nom == 'SceneMode':
            note('%9.1f ms  SCENE DU MODE demarree : %s'
                 % (ms, 'OUI' if ctx.Rax & 0xFF else 'ECHEC'))
        elif bp.nom == 'SousPage':
            v = ctx.Rcx & 0xFFFFFFFFFFFFFFFF
            if v != et['vu']:                 # on ne note que les CHANGEMENTS
                et['vu'] = v
                note('%9.1f ms  la mise a jour voit sous-page = 0x%X' % (ms, v))
        elif bp.nom == 'Relais':
            note('%9.1f ms  RELAIS : le predicat rend %s'
                 % (ms, 'OUI' if ctx.Rax & 0xFF else 'non'))
        elif bp.nom == 'Caverne':
            note('%9.1f ms  CAVERNE DE TRANSITION appelee' % ms)
        elif bp.nom == 'DemandeMode':
            note('%9.1f ms  demande de MODE %d'
                 % (ms, ctx.Rcx & 0xFFFFFFFF))
        elif bp.nom == 'DemandeSousEtat':
            note('%9.1f ms  demande de SOUS-ETAT %d'
                 % (ms, ctx.Rcx & 0xFFFFFFFF))

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
    print('     SINGLE PLAYER, validez')
    print('     choisissez Arcade, validez')
    print('     dans la page de reglages, validez')
    print('     puis fermez le jeu.')
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
    dit()
    dit('RECIT HORODATE :')
    for t in et['recit']:
        dit('   ' + t)
    dit()
    dit('LECTURE :')
    dit('   pas de RELAIS      -> le site 0x1801DBEF2 n est jamais atteint :')
    dit('                         la page des modes n arrive pas jusque-la.')
    dit('   RELAIS toujours non -> le predicat ne dit jamais OUI : ce n est pas')
    dit('                         le bon signal de validation.')
    dit('   CAVERNE mais pas de demande de MODE -> la caverne echoue en amont')
    dit('                         (la session ne se cree pas).')
    bilan = os.path.join(RACINE, 'analysis', 'pister_sp_bilan.txt')
    with open(bilan, 'w', encoding='utf-8') as fp:
        fp.write(os.linesep.join(lignes) + os.linesep)
    print()
    print('bilan ecrit dans %s' % bilan)
    return 0


if __name__ == '__main__':
    sys.exit(main())
