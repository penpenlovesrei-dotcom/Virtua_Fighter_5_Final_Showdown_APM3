#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Trace la machine a etats de vfes.exe, et sait la devier.

Le moteur tient une machine a etats nommee. `0x1800DA800` en est le changement
d'etat : elle recoit le nouvel etat en `ecx`, garde le courant dans le global
`0x18070C4F0`, et journalise « [ancien]->[nouveau] » avec la table de noms
`0x1803A0C80` -- 67 noms, de `STARTUP` a `APM3_TESTMODE_MAIN`.

Ce que ce script en fait :

  * `--tracer`    pose un point d'arret sur le changement d'etat et imprime
                  chaque transition en clair. C'est la carte du parcours reel,
                  de l'ecran-titre au combat.
  * `--devier A B` quand le jeu demande l'etat A, ecrit B dans `ecx` a la place.
                  Le jeu emprunte alors sa propre machinerie de transition, ce
                  qui est bien plus sur que d'ecrire l'etat en memoire.

Les etats interessants : 60 APM3_ENTRY, 61 APM3_SELECTOR, 62 APM3_GAME_VS,
63 APM3_GAMEOVER, **64 APM3_TRAINING**, 65 APM3_ONLINE_VS.

Usage :
    py -3 tools/tracer_etats.py --tracer --secondes 90
    py -3 tools/tracer_etats.py --devier 62 64 --secondes 120
"""
import os
import re
import time
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402
from pe_disasm import Image                                # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
DLL = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', MOTEUR)
IMAGE_BASE = 0x180000000
SET_STATE = 0x0DA800          # RVA du changement d'etat
NOMS_TBL = 0x3A0C80           # RVA de la table des noms de tete (11 entrees)
SOUS_TBL = 0x3A0CE0           # RVA de la table des sous-etats (56 entrees)
ETAT_COURANT = 0x70C4F0       # RVA du global de l'etat courant
SOUS_COURANT = 0x70C50C       # RVA du global du sous-etat courant
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')


def _table(img, rva, n):
    out = []
    for i in range(n):
        p = struct.unpack('<Q', img.read(IMAGE_BASE + rva + 8 * i, 8))[0]
        if not p:
            out.append(None)
            continue
        d = img.read(p, 48)
        m = re.match(rb'[\x20-\x7e]{1,46}', d)
        out.append(m.group().decode('latin-1') if m else None)
    return out


def lire_noms():
    """Les DEUX tables : les etats de tete (11) et les sous-etats (56).

    Le sentinelle 0x37 = 55 que SetState ecrit est le MAX de la seconde, ce qui
    confirme le decoupage."""
    img = Image(DLL)
    return _table(img, NOMS_TBL, 11), _table(img, SOUS_TBL, 56)


def main():
    argv = sys.argv[1:]
    secondes = 120
    pose_a = 12.0
    devier = None
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'combat_martelage.txt')
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--a' in argv:
        pose_a = float(argv[argv.index('--a') + 1])
    if '--devier' in argv:
        i = argv.index('--devier')
        devier = (int(argv[i + 1]), int(argv[i + 2]))
    # Certains sous-etats n'appartiennent pas a l'etat de tete courant :
    # les DATA_TEST_* sont sous l'etat 3 (DATA_TEST), pas sous APM3. Il faut
    # alors devier AUSSI ecx, sinon on demande un sous-etat etranger a la tete.
    tete_forcee = None
    if '--tete' in argv:
        tete_forcee = int(argv[argv.index('--tete') + 1])
    # --sauter-entry : au moment ou le jeu entre dans l'etat de tete APM3 (8)
    # sans changer de sous-etat (MAX = 55), demander directement
    # APM3_SELECTOR (49). Cela court-circuite APM3_ENTRY, l'attente de la borne
    # qui n'affiche rien chez nous et qui repart au titre au bout de 60 s.
    sauter_entry = '--sauter-entry' in argv
    # --passer-entry : la bonne facon de se debarrasser de l'ecran noir.
    # Sauter l'etat le fait planter (violation d'acces a moteur+0xB1D33 : il
    # prepare quelque chose dont la selection a besoin). On le TRAVERSE donc,
    # en simulant un appui sur START des que le jeu y entre. Le stub accepte
    # une directive " impulsion = start " declenchee par la date du fichier,
    # ce qui evite d'avoir a connaitre son horloge interne.
    passer_entry = '--passer-entry' in argv
    base_scenario = None
    if passer_entry:
        with open(scenario, encoding='utf-8', errors='replace') as fp:
            base_scenario = [l for l in fp.read().splitlines()
                             if not l.strip().lower().startswith('impulsion')]
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]
    captures = []
    if '--captures' in argv:
        for spec in argv[argv.index('--captures') + 1].split(','):
            t, chemin = spec.split(':', 1)
            captures.append((os.path.join(RACINE, 'analysis', chemin),
                             float(t), 'Virtua Fighter'))
    journal = os.path.join(RACINE, 'analysis', 'trace_etats.txt')

    tete, sous = lire_noms()

    def nom(n, t):
        return t[n] if 0 <= n < len(t) and t[n] else '?%d' % n

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 10000
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'base': 0, 'n': 0, 't0': time.time()}

    def sur_bp(d, bp, ctx, tid):
        etat = ctx.Rcx & 0xFFFFFFFF
        ss = ctx.Rdx & 0xFFFFFFFF
        courant = d.u32(et['base'] + ETAT_COURANT)
        sc = d.u32(et['base'] + SOUS_COURANT)
        marque = ''
        if passer_entry and etat == 8 and ss == 55:
            try:
                saut = chr(10)
                contenu = (saut.join(base_scenario) + saut + saut
                           + 'impulsion = start' + saut + 'duree = 150' + saut)
                with open(SCENARIO_ACTIF, 'w', encoding='ascii',
                          newline=saut) as fp:
                    fp.write(contenu)
                marque = '   <<< impulsion START envoyee pour traverser APM3_ENTRY'
            except Exception as exc:
                marque = '   <<< impulsion IMPOSSIBLE : %s' % exc
        if sauter_entry and etat == 8 and ss == 55:
            ctx.Rdx = 49
            ctx.ContextFlags = instrument.CONTEXT_FULL | instrument.CONTEXT_DEBUG_REGISTERS
            d.poser_contexte(tid, ctx)
            marque = '   <<< APM3_ENTRY COURT-CIRCUITE -> APM3_SELECTOR'
        if devier and ss == devier[0]:
            ctx.Rdx = devier[1]
            if tete_forcee is not None:
                ctx.Rcx = tete_forcee
            ctx.ContextFlags = instrument.CONTEXT_FULL | instrument.CONTEXT_DEBUG_REGISTERS
            d.poser_contexte(tid, ctx)
            marque = '   <<< DEVIE vers %s%s' % (
                nom(devier[1], sous),
                (' sous la tete %s' % nom(tete_forcee, tete))
                if tete_forcee is not None else '')
        et['n'] += 1
        d.dire('  %3d  [t=%5.1f s]  etat [%s] -> [%s]   sous-etat [%s] -> [%s]%s'
               % (et['n'], time.time() - et['t0'],
                  nom(courant if courant is not None else -1, tete),
                  nom(etat, tete),
                  nom(sc if sc is not None else -1, sous), nom(ss, sous), marque))

    def tic(d, t):
        if et['pose'] or t < pose_a:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        et['base'] = b
        bp = instrument.PointArret('SetState', b + SET_STATE, max_coups=10000)
        bp.silencieux = True
        d.bps.append(bp)
        d.armer_logiciel(bp)
        d.dire('  point d\'arret sur le changement d\'etat, a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    if scenario and os.path.exists(scenario):
        with open(scenario, 'rb') as fp:
            data = fp.read()
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(data)
    print('journal : %s' % journal)
    if devier:
        print('deviation du sous-etat : %s -> %s'
              % (nom(devier[0], sous), nom(devier[1], sous)))
    dbg.run(EXE, os.path.dirname(EXE), secondes, tuple(captures))
    fichier.close()
    with open(journal, encoding='utf-8') as fp:
        for ligne in fp:
            if ligne.startswith('  ') and ('->' in ligne or 'arret' in ligne):
                sys.stdout.write(ligne)
    return 0


if __name__ == '__main__':
    sys.exit(main())
