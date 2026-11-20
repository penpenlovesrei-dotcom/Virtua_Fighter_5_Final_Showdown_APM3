#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le tampon de l'attract suit-il la geometrie du film, ou est-il fige ?

C'est la question qui decide s'il suffit de REMULTIPLEXER un film console
(`.sfd`, 1280x720) dans un conteneur USM, ou s'il faut aussi le REENCODER en
1920x1088.

Le plantage du 2026-09-06 est un `rep movsb` (`vfes.exe+0x111E3E`) qui recopie
une ligne de 1920 octets et sort du tampon des le premier octet. La pile
designe le demandeur cote moteur : `0x18026A1D7`, c'est-a-dire le retour de

    0x18026A1D2  call 0x18026A320      ; le televersement vers la texture

appele depuis l'enrobage `0x18026A180`. On se pose a l'entree de cet enrobage
et on lit ce qu'il recoit : si les dimensions sont celles du fichier, le tampon
SUIT la geometrie ; si elles sont figees, il faudra reencoder.

Convention Windows x64 : rcx, rdx, r8, r9 puis la pile a partir de rsp+0x28.
L'enrobage relit explicitement `[rsp+0x80]`, `[rsp+0x88]`, `[rsp+0x90]` et
`[rsp+0x98]` -- ce sont ses arguments empiles, qu'on releve aussi.

    py -3 tools/pister_tampon.py --secondes 90
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
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')

POINTS = [
    ('televersement', 0x26A180),
]


def main():
    argv = sys.argv[1:]
    secondes = 90
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 400
    journal = os.path.join(RACINE, 'analysis', 'pister_tampon.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'compte': collections.Counter(), 't0': None,
          'vus': set()}

    def note(t):
        fichier.write(t + os.linesep)
        fichier.flush()

    def sur_bp(d, bp, ctx, tid):
        et['compte'][bp.nom] += 1
        n = et['compte'][bp.nom]
        if et['t0'] is None:
            et['t0'] = time.time()
        ms = (time.time() - et['t0']) * 1000.0
        # Le televersement sert TOUTES les textures du jeu (256x256, 1024...).
        # Seules les grandes nous interessent : une image de film fait au
        # moins 1280 de large.
        if (ctx.R8 & 0xFFFFFFFF) < 1200:
            return
        et['compte']['grandes'] += 1
        if et['compte']['grandes'] > 8:
            return
        rsp = ctx.Rsp & 0xFFFFFFFFFFFFFFFF
        pile = d.read(rsp, 0xB0) or b''

        def mot(o):
            return (int.from_bytes(pile[o:o+4], 'little')
                    if len(pile) >= o + 4 else -1)
        note('%9.1f ms  televersement #%d' % (ms, n))
        note('              rcx=0x%X  rdx=0x%X  r8d=%d  r9d=%d'
             % (ctx.Rcx & 0xFFFFFFFFFFFFFFFF, ctx.Rdx & 0xFFFFFFFFFFFFFFFF,
                ctx.R8 & 0xFFFFFFFF, ctx.R9 & 0xFFFFFFFF))
        note('              [rsp+0x80]=%d  [rsp+0x88]=%d  [rsp+0x90]=0x%X  '
             '[rsp+0x98]=0x%X'
             % (mot(0x80), mot(0x88), mot(0x90), mot(0x98)))

    def tic(d, t):
        if et['pose']:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        for nom_, rva in POINTS:
            bp = instrument.PointArret(nom_, b + rva, max_coups=100000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  point pose sur le televersement, a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    print('MESURE : le tampon suit-il la geometrie du film ?')
    print('  Laissez tourner. Aucune touche.')
    print()
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    lignes = ['', '=' * 72,
              'COMPTE televersement : %d' % et['compte']['televersement'], '',
              'RELEVE :']
    with open(journal, encoding='utf-8') as fp:
        for l in fp:
            if 'televersement #' in l or 'rcx=' in l or '[rsp+' in l:
                lignes.append('   ' + l.rstrip())
    lignes += ['', 'LECTURE :',
               '   des dimensions egales a celles du FICHIER -> le tampon suit,',
               '     un remultiplexage suffit.',
               '   des dimensions FIGEES -> il faudra reencoder a cette taille.']
    bilan = os.path.join(RACINE, 'analysis', 'pister_tampon_bilan.txt')
    with open(bilan, 'w', encoding='utf-8') as fp:
        fp.write(os.linesep.join(lignes) + os.linesep)
    for t in lignes:
        try:
            print(t)
        except UnicodeEncodeError:
            print(t.encode('ascii', 'replace').decode('ascii'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
