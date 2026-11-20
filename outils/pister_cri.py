#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fait parler CRI : on lit ses messages d'erreur au lieu de les deviner.

`vfes.exe` embarque CRI Mana 2.18.00 (lecteur Sofdec2, les `.usm`) et CRI Atom
2.20.83. L'attract demarre -- la scene est vivante, mesure de
`tools/pister_attract.py` -- puis meurt au bout d'une poignee de trames.

CRI est bavard : 703 messages numerotes sont dans `vfes.exe`, entre
`0x14017ECE8` et `0x1401AEDA8`, et 4019 sites les passent a un notificateur
commun. Deux enveloppes dominent (`0x1400B4134`, 460 sites ; `0x1400B4150`,
151) et **toutes deux se deversent dans `0x1400B427C`**, qui est aussi appele
directement 53 fois.

On se pose donc la, une seule fois, et `rcx` porte le message.

    py -3 tools/pister_cri.py --secondes 60
"""
import collections
import os
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                            # noqa: E402

HOTE = 'vfes.exe'
MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')

# RVA dans vfes.exe (base 0x140000000)
CRI_ERREUR = 0x0B427C
# et les deux bornes du sous-etat, pour situer les messages dans le temps
CS_DEMO_ENTREE = 0x0DDC40
CS_DEMO_SORTIE = 0x0DD558


def main():
    argv = sys.argv[1:]
    secondes = 60
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 400
    journal = os.path.join(RACINE, 'analysis', 'pister_cri.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'hote': False, 'moteur': False, 'compte': collections.Counter(),
          't0': None, 'messages': []}

    def note(txt):
        fichier.write(txt + os.linesep)
        fichier.flush()

    def sur_bp(d, bp, ctx, tid):
        et['compte'][bp.nom] += 1
        if et['t0'] is None:
            et['t0'] = time.time()
        ms = (time.time() - et['t0']) * 1000.0

        if bp.nom == 'erreur CRI':
            # `0x1400B41A0` fait `mov rdi, rdx` et `mov esi, ecx` : le message
            # est en rdx, rcx porte un code. On lit les trois premiers
            # registres et on garde ce qui ressemble a du texte -- c'est plus
            # sur que de parier sur une convention.
            morceaux = []
            for nom_r, val in (('rcx', ctx.Rcx), ('rdx', ctx.Rdx),
                               ('r8', ctx.R8), ('r9', ctx.R9)):
                v = val & 0xFFFFFFFFFFFFFFFF
                brut = d.read(v, 160) if v > 0x10000 else None
                if brut:
                    fin = brut.find(b'\x00')
                    t = brut[:fin if fin >= 0 else 120]
                    if len(t) >= 4 and all(0x20 <= c < 0x7f for c in t):
                        morceaux.append('%s=%r' % (nom_r,
                                                   t.decode('latin-1')[:110]))
                        continue
                morceaux.append('%s=0x%X' % (nom_r, v))
            txt = '  '.join(morceaux)
            if txt not in [m for _, m in et['messages']]:
                et['messages'].append((ms, txt))
                note('%9.1f ms  CRI : %s' % (ms, txt))
            return

        note('%9.1f ms  %s' % (ms, bp.nom))

    def tic(d, t):
        if not et['hote']:
            b = d.base_de(HOTE)
            if b:
                et['hote'] = True
                bp = instrument.PointArret('erreur CRI', b + CRI_ERREUR,
                                           max_coups=200000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)
                d.dire('  point sur le notificateur CRI, base %s = 0x%X'
                       % (HOTE, b))
        if not et['moteur']:
            b = d.base_de(MOTEUR)
            if b:
                et['moteur'] = True
                for nom_, rva in (('--> entree CS_DEMO', CS_DEMO_ENTREE),
                                  ('<-- sortie CS_DEMO', CS_DEMO_SORTIE)):
                    bp = instrument.PointArret(nom_, b + rva, max_coups=1000)
                    bp.silencieux = True
                    d.bps.append(bp)
                    d.armer_logiciel(bp)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    print('MESURE : les messages de CRI pendant l attract.')
    print('  Laissez tourner. Aucune touche.')
    print()
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    lignes = []

    def dit(t=''):
        lignes.append(t)

    dit()
    dit('=' * 72)
    dit('COMPTES : %s' % ', '.join('%s=%d' % (n, c)
                                   for n, c in sorted(et['compte'].items())))
    dit()
    dit('MESSAGES CRI, dans l ordre :')
    if not et['messages']:
        dit('   AUCUN. CRI ne se plaint de rien -- la mort de la scene vient')
        dit('   d ailleurs que du lecteur video.')
    for ms, m in et['messages']:
        dit('   %9.1f ms  %s' % (ms, m))
    bilan = os.path.join(RACINE, 'analysis', 'pister_cri_bilan.txt')
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
