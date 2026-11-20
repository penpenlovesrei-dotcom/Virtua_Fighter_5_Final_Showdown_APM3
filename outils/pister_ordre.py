#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""QUI dessine APRES nous ? L'ordre reel d'une trame, releve, pas deduit.

Le texte des variantes s'affiche mais passe SOUS les couches AET. Trois essais
de placement ont echoue, tous fondes sur un raisonnement :

  . creneau 4 de TaskSelStage      -> dessine, mais dessous ;
  . creneau 6 de TaskSelStage      -> jamais appele ;
  . detour du creneau 4 de TaskSelector (qui dessine le panneau) -> dessous.

Ce dernier point est le plus instructif : si dessiner apres le parent ne suffit
pas, l'AET n'est pas rendu par une tache. Il reste a savoir PAR QUOI.

On enregistre donc la suite des appels entre DEUX passages de notre dessin,
c'est-a-dire une trame exactement. Ce qui apparait dedans, apres nous, est ce
qui nous recouvre.

Sont instrumentes : notre dessin, et les sept creneaux d'`AetMgr`
(vtable 0x1803487A8), la classe nommee par le RTTI.

    py -3 tools/pister_ordre.py
    py -3 tools/pister_ordre.py --secondes 300
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
SCENARIO = """# ecrit par tools/pister_ordre.py -- le clavier mene.
front   = 10
journal = 0
clavier = 1
manette = 1
0       rien
"""

# (rva, nom). Les creneaux d'AetMgr sont ceux de sa vtable 0x1803487A8.
CIBLES = [
    (0xEA1300, 'NOTRE DESSIN'),
    (0x021980, 'AetMgr creneau 0'),
    (0x024A00, 'AetMgr creneau 1'),
    (0x023150, 'AetMgr creneau 2'),
    (0x0235A0, 'AetMgr creneau 3'),
    (0x0235C0, 'AetMgr creneau 4'),
    (0x0251A0, 'AetMgr creneau 6'),
]
MAX_EVENEMENTS = 120


def main():
    argv = sys.argv[1:]
    secondes = 300
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    journal = os.path.join(RACINE, 'analysis', 'pister_ordre.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = True
    dbg.bp_max = 2000000
    dbg.sortie = fichier
    et = {'poses': False, 'suite': [], 'depart': False, 'fini': False,
          'compte': {}}

    def sur_bp(d, bp, ctx, tid):
        et['compte'][bp.nom] = et['compte'].get(bp.nom, 0) + 1
        if et['fini']:
            return
        # Premiere version : on s'arretait au DEUXIEME passage de notre dessin,
        # en croyant tenir une trame. Mesure du 2026-09-08 : notre dessin est
        # appele DEUX FOIS D AFFILEE, et la fenetre se refermait entre les
        # deux, vide. On enregistre donc une longue suite, sur plusieurs
        # trames, et on la lit telle quelle.
        if bp.nom == 'NOTRE DESSIN' and not et['depart']:
            et['depart'] = True
            d.dire('  --- debut du releve ---')
        if et['depart']:
            et['suite'].append(bp.nom)
            # DANS LE JOURNAL, pas seulement a l'ecran : la suite est tout
            # l'interet de la mesure, et la premiere version l'a perdue en ne
            # l'imprimant que sur la sortie standard.
            d.dire('    %3d  %s' % (len(et['suite']), bp.nom))
            if len(et['suite']) >= MAX_EVENEMENTS:
                et['fini'] = True
                d.dire('  --- arret : %d evenements releves ---'
                       % MAX_EVENEMENTS)

    def tic(d, t):
        if et['poses']:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['poses'] = True
        for rva, nom in CIBLES:
            bp = instrument.PointArret(nom, b + rva, max_coups=2000000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  %d points poses (t=%.1f s)' % (len(CIBLES), t))

    dbg.on_bp = sur_bp
    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)

    print('MESURE : qui dessine APRES nous.')
    print()
    print('  Allez a STAGE SELECT, curseur sur la case de DURAL, et laissez')
    print('  l ecran tranquille deux secondes -- le releve se fait tout seul.')
    print('  journal : %s' % journal)
    print()
    dbg.run(EXE, JEU, secondes, ())
    fichier.close()

    print()
    print('=' * 70)
    if not et['suite']:
        print('AUCUN releve : notre dessin n a pas tourne. Le curseur n a pas')
        print('atteint la case de Dural.')
    else:
        print('LA TRAME, DANS L ORDRE (entre deux passages de notre dessin) :')
        precedent, n = None, 0
        for nom in et['suite']:
            if nom == precedent:
                n += 1
                continue
            if precedent is not None:
                print('   %-24s %s' % (precedent, ('x%d' % n) if n > 1 else ''))
            precedent, n = nom, 1
        print('   %-24s %s' % (precedent, ('x%d' % n) if n > 1 else ''))
        print()
        apres = [x for x in et['suite'][1:] if x != 'NOTRE DESSIN']
        if not apres:
            print('VERDICT : RIEN d instrumente ne passe apres nous. Ce qui')
            print('  nous recouvre n est donc pas AetMgr -- il faut elargir')
            print('  le filet.')
        else:
            print('VERDICT : ce qui passe APRES notre dessin, et donc nous')
            print('  recouvre, est dans la liste ci-dessus. Detourner CE')
            print('  creneau-la (original d abord, notre texte ensuite) met')
            print('  le texte au premier plan.')
    print()
    print('TOTAL DES PASSAGES (sur toute la mesure) :')
    for nom, n in sorted(et['compte'].items(), key=lambda x: -x[1]):
        print('   %-24s %d' % (nom, n))
    print('=' * 70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
