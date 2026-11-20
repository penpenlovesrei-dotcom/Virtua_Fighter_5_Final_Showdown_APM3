#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prend le repartiteur de la liste 2 de mothead sur le fait, dans un combat.

La liste 2 a bien un repartiteur : `MothRunList2` (APM3 **0x180152CE0**). Il ne
cherche aucun code -- il s'en sert comme d'un INDICE dans une table de 55 entrees
de 32 octets en 0x180648840, remplie a l'execution par l'initialiseur
0x180003D30. C'est pourquoi aucune recherche de « cmp code, K » ne pouvait le
trouver.

Le curseur de parcours est `etat+0x498`, remis a la base `etat+0x4A0` par
0x180152DE0 a chaque installation d'enregistrement : la liste 2 est une FRISE
CHRONOLOGIQUE consommee une fois, dans l'ordre des trames, et non un dictionnaire.

Cet outil lance le jeu, le mene au combat, puis pose des points d'arret logiciels
sur le repartiteur et sur les gestionnaires demandes. A chaque passage il decode
l'entree (code, trame, offset de charge) et la charge utile.

Convention des gestionnaires, lue dans le repartiteur :
    gestionnaire(rcx = &ctx, rdx = charge utile, r8 = entree de 12 octets)
    ctx = [ROB, ROB+0x440, [ROB+0x20]+0x30C0, ROB, ROB+0x440, ROB+0x8A0]

Usage :
    py -3 tools/pister_liste2.py                    repartiteur + codes 0 et 9
    py -3 tools/pister_liste2.py --codes 0,9,26     d'autres gestionnaires
    py -3 tools/pister_liste2.py --secondes 120 --a 55
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
IMAGE_BASE = 0x180000000
RUN_LIST2 = 0x152CE0                  # RVA de MothRunList2
TABLE = 0x648840                      # RVA de la table des 55 gestionnaires
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')


def main():
    argv = sys.argv[1:]
    secondes = 120
    pose_a = 55.0
    codes = [0, 9]
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'combat_martelage.txt')
    journal = os.path.join(RACINE, 'analysis', 'pistage_liste2.txt')
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--a' in argv:
        pose_a = float(argv[argv.index('--a') + 1])
    if '--codes' in argv:
        codes = [int(x, 0) for x in argv[argv.index('--codes') + 1].split(',')]
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]
    if '--journal' in argv:
        journal = argv[argv.index('--journal') + 1]
    bp_max = int(argv[argv.index('--bp-max') + 1]) if '--bp-max' in argv else 6

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv     # sourdine par defaut
    dbg.bp_max = bp_max
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    etat = {'pose': False}

    def sur_bp(d, bp, ctx, tid):
        if bp.nom == 'MothRunList2':
            # A l'entree, ebx ne porte pas encore la trame : elle arrive en xmm2 et
            # n'est convertie qu'a 0x180152D4A. On ne l'affiche donc pas ici.
            cur = d.u64(ctx.Rcx + 0x498)
            d.dire('        etat=0x%X  ROB=0x%X  ecart=0x%X  curseur=0x%X'
                   % (ctx.Rcx, ctx.Rdx, ctx.Rcx - ctx.Rdx, cur or 0))
            if cur:
                brut = d.read(cur, 12 * 6)
                for k in range(len(brut) // 12):
                    c, tr, off = struct.unpack_from('<iii', brut, 12 * k)
                    if c < 0:
                        d.dire('          [%d] fin de liste' % k)
                        break
                    d.dire('          [%d] code=%-3d trame=%-4d charge=+%d' % (k, c, tr, off))
            return
        # gestionnaire : rdx = charge utile, r8 = entree
        ent = d.read(ctx.R8, 12)
        if len(ent) == 12:
            c, tr, off = struct.unpack('<iii', ent)
            charge = d.read(ctx.Rdx, 8) if ctx.Rdx else b''
            d.dire('        entree : code=%d trame=%d ; charge en 0x%X = %s'
                   % (c, tr, ctx.Rdx, charge.hex() if charge else '(aucune)'))

    def tic(d, t):
        if etat['pose'] or t < pose_a:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        etat['pose'] = True
        bp = instrument.PointArret('MothRunList2', b + RUN_LIST2)
        d.bps.append(bp)
        d.armer_logiciel(bp)
        for c in codes:
            h = d.u64(b + TABLE + 32 * c)
            if not h:
                d.dire('  code %d : aucun gestionnaire installe' % c)
                continue
            bp = instrument.PointArret('gestionnaire liste2 code %d' % c, h)
            d.bps.append(bp)
            d.dire('  code %d -> gestionnaire 0x%X (RVA 0x%X)' % (c, h, h - b + IMAGE_BASE))
            d.armer_logiciel(bp)
        d.dire('  t=%.0f s : points d\'arret poses' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    if scenario and os.path.exists(scenario):
        with open(scenario, 'rb') as fp:
            data = fp.read()
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(data)
        print('scenario : %s installe' % scenario)
    print('journal : %s' % journal)
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()
    with open(journal, encoding='utf-8') as fp:
        for ligne in fp:
            if ligne.startswith(('  BP', '  code', '  t=', '        ', '          ')):
                sys.stdout.write(ligne)
    print('journal complet : %s' % journal)
    return 0


if __name__ == '__main__':
    sys.exit(main())
