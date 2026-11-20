#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La grille de selection de la borne, lue en memoire.

Etabli statiquement (analysis/dural.md section 13) : `0x1801700B0` monte un
tableau LOCAL de 21 cases de 0x18 octets, a `rbp-0x70`. Chaque case porte

    +0x00   l'indice de personnage du ROB
    +0x08   un nom d'animation      ("aki", "dur", "rnd", ...)
    +0x10   un nom d'animation de sortie  ("aki_end", ...)

et la case **19 recoit l'indice 20, c'est-a-dire DURAL** (ecrit en clair a
`0x1801703CB`). La question que ce script tranche : dans le jeu qui tourne,
cette case est-elle peuplee comme les autres, et qu'est-ce qui la distingue ?

Le tableau etant local, on ne peut pas le lire depuis un global : il faut un
point d'arret DANS la fonction, une fois le montage fini. `0x1801703E9` est le
premier appel apres la derniere ecriture d'indice (`0x1801703DF`), donc rbp est
valide et le tableau complet.

    py -3 tools/pister_grille.py                 mode borne, scenario select_a
    py -3 tools/pister_grille.py --secondes 150
"""
import collections
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
MONTAGE_FIN = 0x1703E9        # RVA : dans 0x1801700B0, tableau complet
CASES = 21
PAS = 0x18
DEBUT = -0x70                 # le tableau commence a rbp-0x70
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')
PERSOS = ['AKI', 'SAR', 'LAU', 'SHU', 'JEF', 'PAI', 'JAK', 'KAG', 'LIO', 'WOL',
          'AOI', 'LEI', 'VAN', 'BRA', 'GOH', 'MON', 'MSK', 'KRT', 'TAK', 'TE2',
          'DUR']


def nom(c):
    if c is None:
        return 'illisible'
    if c == 21:
        return '(aucun)'
    return PERSOS[c] if 0 <= c < len(PERSOS) else '?%d' % c


def main():
    argv = sys.argv[1:]
    secondes, pose_a = 130, 8.0
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'select_a.txt')
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--a' in argv:
        pose_a = float(argv[argv.index('--a') + 1])
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 50000
    journal = os.path.join(RACINE, 'analysis', 'pister_grille.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'n': 0, 'vues': collections.OrderedDict()}

    def chaine(d, adr):
        if not adr:
            return ''
        b = d.read(adr, 24)
        if not b:
            return ''
        b = b.split(bytes([0]), 1)[0]
        if 1 <= len(b) <= 20 and all(32 <= c < 127 for c in b):
            return b.decode('latin-1')
        return ''

    def sur_bp(d, bp, ctx, tid):
        if bp.nom in ('CasesA', 'CasesB'):
            sur_bp_cases(d, bp, ctx, tid)
            return
        et['n'] += 1
        if et['n'] > 3:            # trois releves suffisent
            return
        rbp = ctx.Rbp
        lignes = []
        for k in range(CASES):
            a = rbp + DEBUT + PAS * k
            idx = d.u32(a)
            p1 = d.u64(a + 8)
            p2 = d.u64(a + 0x10)
            lignes.append((k, idx, chaine(d, p1), chaine(d, p2)))
        cle = tuple((l[1], l[2]) for l in lignes)
        if cle in et['vues']:
            return
        et['vues'][cle] = lignes
        d.dire('  --- releve %d, rbp = 0x%X ---' % (len(et['vues']), rbp))
        for k, idx, n1, n2 in lignes:
            marque = '   <<<< DURAL' if idx == 20 else ''
            d.dire('    case %2d  indice %-4s %-8s %-12s %-12s%s'
                   % (k, idx if idx is not None else '?', nom(idx), n1, n2,
                      marque))

    def sur_bp_cases(d, bp, ctx, tid):
        """Dumper le tableau de cases de 0x298 octets, et diffuser 18 vs 19.

        Les cases du selecteur font 0x298 octets (`imul .., 0x298` a
        0x18016EEC4 et 0x180237DC9). Si Dural n'apparait pas alors que sa case
        du tableau d'animations est peuplee, la difference est dans CETTE
        structure-la. On la lit plutot que de la deduire.
        """
        base = ctx.Rdx if bp.nom == 'CasesA' else ctx.R15
        if not base or et.get('cases'):
            return
        brut = d.read(base, 0x298 * 21)
        if not brut or len(brut) < 0x298 * 21:
            return
        et['cases'] = True
        d.dire('  --- tableau de cases, base 0x%X (via %s) ---' % (base, bp.nom))
        ref = None
        for k in range(21):
            c = brut[0x298 * k: 0x298 * (k + 1)]
            tete = ' '.join('%02X' % b for b in c[:0x18])
            d.dire('    case %2d : %s' % (k, tete))
        a, b = brut[0x298 * 18:0x298 * 19], brut[0x298 * 19:0x298 * 20]
        diff = [i for i in range(0x298) if a[i] != b[i]]
        d.dire('  --- case 18 (TAK) contre case 19 (DUR) : %d octet(s) different(s) ---'
               % len(diff))
        for i in diff[:40]:
            d.dire('    +0x%03X : TAK %02X   DUR %02X' % (i, a[i], b[i]))

    def tic(d, t):
        if et['pose'] or t < pose_a:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        for n_, rva_ in (('MontageGrille', MONTAGE_FIN),
                         ('CasesA', 0x16EEBA), ('CasesB', 0x237DC9)):
            bp = instrument.PointArret(n_, b + rva_, max_coups=50000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  point d\'arret sur le montage de la grille, a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    if scenario and os.path.exists(scenario):
        with open(scenario, 'rb') as fp:
            data = fp.read()
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(data)
    print('journal : %s' % journal)
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    print()
    if not et['vues']:
        print('--- AUCUN passage sur le montage de la grille ---')
        print('  0x1801700B0 n a pas ete appele : ce n est pas cette fonction')
        print('  qui monte la grille dans le parcours emprunte.')
    else:
        print('--- %d passage(s), %d disposition(s) distincte(s) ---'
              % (et['n'], len(et['vues'])))
        with open(journal, encoding='utf-8') as fp:
            for l in fp:
                if l.startswith('    ') or l.startswith('  ---'):
                    sys.stdout.write(l)
    return 0


if __name__ == '__main__':
    sys.exit(main())
