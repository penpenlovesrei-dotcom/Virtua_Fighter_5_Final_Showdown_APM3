#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La legende du bas : qui la porte, et notre greffe tourne-t-elle ?

Deux questions, une seule passe :

  1. La caverne de `--legende-sousmenu` (`0x1801A7CCA`) est-elle ATTEINTE
     quand un sous-menu est ouvert ? Si elle ne l'est pas, la mise a jour du
     menu principal n'est plus appelee du tout, et le geste est au mauvais
     endroit.

  2. La passe de resolution (`0x1801BBD01`) lit `[rbx+0x21C]`. En relevant
     `rbx` et l'identifiant a chaque passage, on voit COMBIEN d'objets
     portent une legende et lesquels -- c'est ce qui dira si le menu
     principal en a bien une a cet offset.

Releve au fil de l'eau : analysis\\pister_legende.txt
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
    ('caverne legende', 0x1A7CCA),   # notre greffe
    ('garde sousmenu',  0x1DC649),   # le site qui y mene
    ('maj menu',        0x1DC620),   # la mise a jour du menu principal
    ('resolution',      0x1BBD01),   # mov ecx, [rbx+0x21C]
]


def main():
    argv = sys.argv[1:]
    secondes = 60
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 400
    journal = os.path.join(RACINE, 'analysis', 'pister_legende.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'compte': collections.Counter(), 'porteurs': {},
          't0': None, 'base': None}

    def note(txt):
        fichier.write(txt + os.linesep)
        fichier.flush()

    def sur_bp(d, bp, ctx, tid):
        et['compte'][bp.nom] += 1
        if et['t0'] is None:
            et['t0'] = time.time()
        ms = (time.time() - et['t0']) * 1000.0

        if bp.nom == 'resolution':
            rbx = ctx.Rbx & 0xFFFFFFFFFFFFFFFF
            brut = d.read(rbx + 0x21C, 8) or b''
            if len(brut) == 8:
                l1 = int.from_bytes(brut[0:4], 'little')
                l2 = int.from_bytes(brut[4:8], 'little')
                vu = et['porteurs'].setdefault(rbx, [0, l1, l2])
                vu[0] += 1
                vu[1], vu[2] = l1, l2
            return

        if bp.nom == 'caverne legende' and et['compte'][bp.nom] <= 5:
            rdi = ctx.Rdi & 0xFFFFFFFFFFFFFFFF
            brut = d.read(rdi + 0x21C, 8) or b''
            l1 = int.from_bytes(brut[0:4], 'little') if len(brut) == 8 else -1
            note('%9.1f ms  CAVERNE atteinte : page=0x%X  [+0x21C]=0x%X '
                 '(avant notre ecriture)' % (ms, rdi, l1))
            return

        if et['compte'][bp.nom] <= 2:
            note('%9.1f ms  PREMIERE FOIS : %s' % (ms, bp.nom))

    def tic(d, t):
        if et['pose']:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        et['base'] = b
        for nom_, rva in POINTS:
            bp = instrument.PointArret(nom_, b + rva, max_coups=2000000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  points d\'arret poses a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    print('MESURE : la legende du bas.')
    print()
    print('  Deux fois Entree pour le menu, puis Entree sur SINGLE PLAYER,')
    print('  et LAISSEZ le sous-menu ouvert quelques secondes avant de fermer.')
    print()
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    lignes = []

    def dit(txt=''):
        lignes.append(txt)

    dit()
    dit('=' * 72)
    dit('COMPTES :')
    for nom_, _ in POINTS:
        dit('   %-18s %d' % (nom_, et['compte'][nom_]))
    dit()
    dit('PORTEURS DE LEGENDE (objets vus dans la resolution) :')
    for adr, (n, l1, l2) in sorted(et['porteurs'].items(),
                                   key=lambda kv: -kv[1][0])[:12]:
        dit('   objet 0x%-14X  %6d passages   ligne1=0x%-6X ligne2=0x%X'
            % (adr, n, l1, l2))
    dit()
    dit('LECTURE :')
    dit('   caverne a 0  -> la mise a jour du menu principal n est plus')
    dit('                   appelee quand un sous-menu est ouvert : le geste')
    dit('                   est au mauvais endroit.')
    dit('   caverne > 0 et superposition persistante -> l offset +0x21C n est')
    dit('                   pas celui que porte le menu principal.')
    bilan = os.path.join(RACINE, 'analysis', 'pister_legende_bilan.txt')
    with open(bilan, 'w', encoding='utf-8') as fp:
        fp.write(os.linesep.join(lignes) + os.linesep)
    for t in lignes:
        try:
            print(t)
        except UnicodeEncodeError:
            print(t.encode('ascii', 'replace').decode('ascii'))
    print()
    print('bilan ecrit dans %s' % bilan)
    return 0


if __name__ == '__main__':
    sys.exit(main())
