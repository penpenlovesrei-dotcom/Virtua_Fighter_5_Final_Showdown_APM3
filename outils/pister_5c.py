#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""QUI ecrit `TaskSelStage+0x5C` -- l'index du decor sous le curseur.

La mesure du 2026-09-08 a montre que le detour de `--variantes` fait tout ce
qu'il doit : il est joue, la barre espace repond (`al = 1`), et l'index EST
ecrit a 22 (du2). Puis quelque chose le remet a du1 dans la foulee.

Le balayage des ecritures vers `+0x5C` en donne huit candidats dans la seule
zone `0x180170000`-`0x180180000`. Plutot que de les departager par la lecture,
on pose un point d'arret MATERIEL en ecriture sur le champ : le processeur
nomme lui-meme l'instruction fautive.

`TaskSelStage` est un membre de `TaskSelector` : `[0x180714928] + 0x3B0`.

    py -3 tools/pister_5c.py
    py -3 tools/pister_5c.py --secondes 300
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import instrument                                              # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
JEU = os.path.join(os.path.dirname(ICI), 'runtime', 'media', 'vf5fs')
EXE = os.path.join(JEU, 'vfes.exe')
SCENARIO_ACTIF = os.path.join(JEU, 'apm_entrees.txt')
SCENARIO = """# ecrit par tools/pister_5c.py -- le clavier mene.
front   = 10
journal = 0
clavier = 1
manette = 1
0       rien
"""

SELECTOR_RVA = 0x714928
SELSTAGE_OFF = 0x3B0
CHAMP = 0x5C
NOMS = ['tst', 'ts2', 'ts3', 'wht', 'ban', 'ter', 'nyc', 'cas', 'riv', 'jin',
        'sin', 'djo', 'umi', 'hai', 'are', 'slk', 'yuk', 'tak', 'aur', 'bar',
        'tan', 'du1', 'du2', 'du3', 'du4', 'du5', 'trm', 'cid', 'trs']


def nom(i):
    if i is None:
        return '?'
    if i == 0xFFFFFFFF:
        return '-1'
    return NOMS[i] if 0 <= i < len(NOMS) else ('ALEA' if i == 41 else str(i))


def main():
    argv = sys.argv[1:]
    secondes = 300
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    journal = os.path.join(os.path.dirname(ICI), 'analysis',
                           'pister_5c.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = True
    dbg.sortie = fichier
    # Le registre ne doit PAS se desarmer tout seul : on veut compter TOUTES
    # les ecritures, pas seulement les quarante premieres. Passe ce seuil,
    # `instrument` cesse de detailler mais continue d'appeler `on_dr`.
    dbg.dr_max = 40
    dbg.dr_auto_desarmer = False
    et = {'arme': None, 'base': 0, 'ecrivains': {}, 'adresse': 0}

    def sur_dr(d, m, ctx, tid):
        """Le DR se declenche APRES l'ecriture : rip pointe la suivante."""
        rip = ctx.Rip
        b = et['base']
        rel = rip - b if b else 0
        valeur = d.u32(et['adresse'])
        cle = rip
        e = et['ecrivains'].setdefault(cle, {'n': 0, 'valeurs': {}})
        e['n'] += 1
        e['valeurs'][valeur] = e['valeurs'].get(valeur, 0) + 1
        if e['n'] <= 3:
            d.dire('  ecriture depuis 0x%X (rva 0x%X) -> %s'
                   % (rip, rel, nom(valeur)))

    def tic(d, t):
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['base'] = b
        if et['arme'] is not None:
            return
        selector = d.u64(b + SELECTOR_RVA)
        if not selector:
            return
        adresse = selector + SELSTAGE_OFF + CHAMP
        et['adresse'] = adresse
        et['arme'] = d.armer_materiel(adresse, 4, 'w', nom='TaskSelStage+0x5C')
        if et['arme'] is None:
            et['arme'] = False
            return
        d.dire('  DR arme sur 0x%X (t=%.1f s) -- valeur actuelle %s'
               % (adresse, t, nom(d.u32(adresse))))

    dbg.on_dr = sur_dr
    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)

    print('MESURE : qui ecrit TaskSelStage+0x5C.')
    print()
    print('  Allez a STAGE SELECT, curseur sur la case de DURAL,')
    print('  pressez la BARRE ESPACE deux ou trois fois, puis quittez.')
    print('  journal : %s' % journal)
    print()
    dbg.run(EXE, JEU, secondes, ())
    fichier.close()

    print()
    print('=' * 70)
    if not et['ecrivains']:
        print('AUCUNE ecriture relevee. Soit l ecran n a pas ete atteint,')
        print('soit le registre de debogage n a pas pu etre arme (le journal')
        print('le dit).')
    else:
        print('%-14s %-12s %8s  %s' % ('adresse', 'rva', 'fois', 'valeurs'))
        for rip, e in sorted(et['ecrivains'].items(), key=lambda x: -x[1]['n']):
            vals = ', '.join('%s x%d' % (nom(v), n)
                             for v, n in sorted(e['valeurs'].items(),
                                                key=lambda x: -x[1])[:5])
            print('0x%012X 0x%08X %8d  %s'
                  % (rip, rip - et['base'], e['n'], vals))
        print()
        print('  Le DR se declenche APRES l ecriture : l adresse montree est')
        print('  l instruction SUIVANTE. L ecrivain est juste avant.')
    print('=' * 70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
