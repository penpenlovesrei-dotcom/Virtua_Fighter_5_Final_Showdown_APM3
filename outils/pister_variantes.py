#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Pourquoi la barre espace ne fait pas defiler les variantes.

Le detour de `--variantes` peut echouer a quatre endroits, et ils ne se
ressemblent pas :

  1. le detour n'est jamais joue           -> 0x180174710 n'est pas atteint ;
  2. il est joue, mais la requete d'entree rend toujours faux
     -> la barre espace n'arrive pas sur le code 6, ou `[rax+0x160]` n'est pas
        « ce bouton est-il presse » ;
  3. l'etat n'est pas 2                    -> la garde `cmp [rbx+0x58], 2`
        ferme la porte ;
  4. l'index est bien change, puis QUELQU'UN LE REECRIT avant le chargement.

On pose donc trois points d'arret dans la greffe elle-meme, et on releve
`[rbx+0x5C]` en continu :

    0x180EA1000   entree du detour              (compte)
    0x180EA1015   apres l'appel d'entree        (on lit al)
    0x180EA1036   l'ecriture de l'index         (on lit eax)

    py -3 tools/pister_variantes.py
    py -3 tools/pister_variantes.py --secondes 300
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
SCENARIO = """# ecrit par tools/pister_variantes.py -- le clavier mene.
front   = 10
journal = 0
clavier = 1
manette = 1
0       rien
"""

SELECTOR_RVA = 0x714928
SELSTAGE_OFF = 0x3B0
GREFFE = 0xEA1000
POINTS = [('entree', GREFFE + 0x0000), ('entree_lue', GREFFE + 0x0015),
          ('ecriture', GREFFE + 0x0036)]
NOMS = ['tst', 'ts2', 'ts3', 'wht', 'ban', 'ter', 'nyc', 'cas', 'riv', 'jin',
        'sin', 'djo', 'umi', 'hai', 'are', 'slk', 'yuk', 'tak', 'aur', 'bar',
        'tan', 'du1', 'du2', 'du3', 'du4', 'du5', 'trm', 'cid', 'trs']


def nom(i):
    return NOMS[i] if 0 <= i < len(NOMS) else ('ALEA' if i == 41 else str(i))


def main():
    argv = sys.argv[1:]
    secondes = 300
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    journal = os.path.join(os.path.dirname(ICI), 'analysis',
                           'pister_variantes.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = True
    dbg.bp_max = 2000000
    dbg.sortie = fichier
    et = {'poses': False, 'compte': {}, 'al': {}, 'ecrits': [],
          'etat': None, 'decor': None, 'base': 0}

    def sur_bp(d, bp, ctx, tid):
        et['compte'][bp.nom] = et['compte'].get(bp.nom, 0) + 1
        if bp.nom == 'entree_lue':
            al = ctx.Rax & 0xFF
            et['al'][al] = et['al'].get(al, 0) + 1
            if al:
                d.dire('  ENTREE ACTIVE : al = %d' % al)
        elif bp.nom == 'ecriture':
            eax = ctx.Rax & 0xFFFFFFFF
            et['ecrits'].append(eax)
            d.dire('  ECRITURE de l index : %d (%s)' % (eax, nom(eax)))

    def tic(d, t):
        b = d.base_de(MOTEUR)
        if not b:
            return
        if not et['poses']:
            et['poses'] = True
            for n, rva in POINTS:
                # `entree` ne sert qu'a prouver que le detour est joue : 300
                # passages suffisent, et le desarmer allege le jeu.
                bp = instrument.PointArret(
                    n, b + rva, max_coups=300 if n == 'entree' else 2000000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)
            d.dire('  points poses dans la greffe (t=%.1f s)' % t)
        selector = d.u64(b + SELECTOR_RVA)
        if not selector:
            return
        tache = selector + SELSTAGE_OFF
        etat = d.u32(tache + 0x58)
        decor = d.u32(tache + 0x5C)
        if etat is None or decor is None:
            return
        if (etat, decor) != (et['etat'], et['decor']):
            et['etat'], et['decor'] = etat, decor
            d.dire('  t=%6.1f s  etat %s  decor %s'
                   % (t, etat, nom(decor) if decor < 0x80000000 else '-1'))

    dbg.on_bp = sur_bp
    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)

    print('MESURE : pourquoi la barre espace ne fait rien.')
    print()
    print('  Allez a STAGE SELECT, curseur sur la case de DURAL,')
    print('  puis pressez la BARRE ESPACE plusieurs fois, lentement.')
    print('  journal : %s' % journal)
    print()
    dbg.run(EXE, JEU, secondes, ())
    fichier.close()

    print()
    print('=' * 70)
    e = et['compte'].get('entree', 0)
    lu = et['compte'].get('entree_lue', 0)
    ec = et['compte'].get('ecriture', 0)
    print('detour joue          : %d fois' % e)
    print('requete d entree     : %d fois' % lu)
    print('index reecrit        : %d fois' % ec)
    if et['al']:
        print('valeurs de al        : %s'
              % ', '.join('%d -> %d fois' % (k, v)
                          for k, v in sorted(et['al'].items())))
    if et['ecrits']:
        print('index ecrits         : %s'
              % ', '.join('%d (%s)' % (x, nom(x)) for x in et['ecrits'][:20]))
    print()
    if e == 0:
        print('VERDICT : le detour n est JAMAIS joue. 0x180174710 n est pas')
        print('  atteint sur cet ecran -- le point d accroche est mauvais.')
    elif lu and not any(et['al'].get(k) for k in et['al'] if k):
        print('VERDICT : le detour tourne, mais la requete d entree rend')
        print('  TOUJOURS 0. La barre espace n arrive pas sur le code 6, ou')
        print('  [rax+0x160] n est pas « ce bouton est-il presse ».')
        print('  A verifier : le stub met bien VK_SPACE sur g_touche[6], et')
        print('  le moteur n interroge peut-etre ce creneau que pour 0,7,8,15.')
    elif ec == 0:
        print('VERDICT : l entree repond, mais l index n est jamais reecrit :')
        print('  c est une garde qui ferme -- l etat n est pas 2, ou l index')
        print('  courant est hors de l anneau 21..25.')
    else:
        print('VERDICT : l index EST reecrit. Le probleme est en aval :')
        print('  quelqu un le remet a du1 avant le chargement. Regardez la')
        print('  suite des « etat / decor » dans le journal.')
    print('=' * 70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
