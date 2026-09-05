#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Piste -- et force -- l'indice de personnage, a l'entonnoir.

Deux tentatives ont echoue avant celle-ci, et il faut savoir pourquoi :

  * point d'arret MATERIEL en ecriture sur `ROB+0x10` : **zero acces en 245 s**.
    Le champ est ecrit a la construction du ROB, donc avant que son adresse
    existe. On ne peut pas armer une surveillance sur une adresse qu'on n'a pas.
  * point d'arret sur `0x180151F5E`, le site qui lit `[joueur+0x10]` pour batir
    `mot_%s.bin` : **zero passage**. Ce site est dans une branche d'un automate
    a saut par table, et notre parcours ne l'emprunte pas.

D'ou ce troisieme angle : **`CodeDuPersonnage` (`0x18012CA90`)**, la fonction qui
traduit un indice en code a trois lettres. Tout nom de fichier de personnage
passe par elle, quelle que soit la branche. Elle borne son argument par
`cmp ecx, 0x15` -- donc 0 a 20 -- et sa table porte en 20 le code `DUR`.

    py -3 tools/pister_perso.py                   observe : qui demande quoi
    py -3 tools/pister_perso.py --forcer 20       repond DUR a la place
    py -3 tools/pister_perso.py --forcer 20 --joueur 1
"""
import collections
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
CODE_PERSO = 0x12CA90         # CodeDuPersonnage(ecx) ; borne cmp ecx,0x15
CODE_PERSO_B = 0x12CAB0       # la jumelle
CODE_PERSO_C = 0x12CAE0       # celle du nom localise
MOTH_APPLY_RECORD = 0x158B40
GET_MOTION_FOR_ROLE = 0x15B310   # equivalent APM3, verifie par oracle
# Champs du ROB (voir analysis/liste2_repartiteur.md) : personnage +0x10,
# posture +0x65C, etat de mouvement +0x8A0.
ROB_PERSO, ROB_POSTURE, ROB_ETAT = 0x10, 0x65C, 0x8A0
# Site 1 lit l'indice dans [rbx-0x10c] et saute l'appel si l'indice vaut 0x15
# (21) -- hors borne, donc "pas de personnage". C'est la source, pas le code.
SOURCE_INDICE = 0x14F5B3      # mov ecx, dword ptr [rbx-0x10c]
DECALAGE_SOURCE = -0x10C
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')
PERSOS = ['AKI', 'SAR', 'LAU', 'SHU', 'JEF', 'PAI', 'JAK', 'KAG', 'LIO', 'WOL',
          'AOI', 'LEI', 'VAN', 'BRA', 'GOH', 'MON', 'MSK', 'KRT', 'TAK', 'TE2', 'DUR']


def nom(c):
    return PERSOS[c] if c is not None and 0 <= c < len(PERSOS) else '?%s' % c


def main():
    argv = sys.argv[1:]
    secondes, pose_a = 120, 6.0
    if '--a' in argv:
        pose_a = float(argv[argv.index('--a') + 1])
    forcer = None
    depuis = None
    surveiller = '--surveiller' in argv
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'select_a.txt')
    if '--forcer' in argv:
        forcer = int(argv[argv.index('--forcer') + 1], 0)
    if '--depuis' in argv:
        depuis = int(argv[argv.index('--depuis') + 1], 0)
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]
    captures = []
    if '--captures' in argv:
        for spec in argv[argv.index('--captures') + 1].split(','):
            t, chemin = spec.split(':', 1)
            captures.append((os.path.join(RACINE, 'analysis', chemin),
                             float(t), 'Virtua Fighter'))

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 200000
    journal = os.path.join(RACINE, 'analysis', 'pister_perso.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'sites': collections.Counter(), 'forces': 0,
          'robs': [], 'rob': '--rob' in argv, 'etat': '--etat' in argv,
          'moth': collections.Counter(),
          'ecrivains': collections.Counter()}

    def sur_bp(d, bp, ctx, tid):
        # Ces deux-la se comptent seulement. Surtout PAS de passage par la
        # branche generique en fin de fonction : elle ecrirait l'indice force
        # dans `rcx`, qui ne porte pas un indice de personnage ici.
        if bp.nom == 'GetMotionForRole':
            et['moth'][(ctx.Rcx & 0xFFFFFFFF, ctx.Rdx & 0xFFFFFFFF,
                        ctx.R8 & 0xFFFFFFFF)] += 1
            return
        if bp.nom == 'MothApplyRecord':
            rob = ctx.Rdx
            if rob and rob not in et['robs']:
                et['robs'].append(rob)
                d.dire('  en combat : ROB %d = 0x%X   personnage %s'
                       % (len(et['robs']), rob, nom(d.u32(rob + 0x10))))
            # --etat : suivre personnage/posture/etat du ROB 1, et n'imprimer
            # que les CHANGEMENTS. Une posture qui n'evolue plus, c'est un
            # combattant qui reste au sol.
            if et.get('etat') and et['robs'] and rob == et['robs'][0]:
                trio = (d.u32(rob + ROB_PERSO), d.u32(rob + ROB_POSTURE),
                        d.u32(rob + ROB_ETAT))
                if trio != et.get('dernier_trio'):
                    et['dernier_trio'] = trio
                    et['trios'] = et.get('trios', 0) + 1
                    if et['trios'] <= 40:
                        d.dire('    ROB1  perso %-4s  posture %-6s  etat 0x%X'
                               % (nom(trio[0]),
                                  trio[1] if trio[1] is not None else '?',
                                  trio[2] or 0))
            # --surveiller : qui ECRIT l'etat de mouvement du ROB 1 ?
            # C'est la question qui separe TAK de Dural : les deux resolvent
            # leurs roles a la meme cadence, mais un seul change d'etat. Un
            # point d'arret materiel en ecriture sur ROB+0x8A0 nomme le site
            # qui installe l'animation -- et dit s'il tourne pour Dural.
            if surveiller and et['robs'] and not et.get('dr_arme'):
                et['dr_arme'] = True
                d.dr_max = 100000
                d.dr_auto_desarmer = False
                d.armer_materiel(et['robs'][0] + ROB_ETAT, 4, 'w',
                                 'ROB1+0x8A0')
            # --rob : rendre le ROB coherent avec la selection. Sans cela le
            # modele est celui de Dural mais les mouvements restent ceux du
            # personnage d'origine -- d'ou une silhouette qui clignote.
            if rob and et.get('rob') and forcer is not None:
                v = d.u32(rob + 0x10)
                if v is not None and (depuis is None or v == depuis):
                    d.write(rob + 0x10, int(forcer).to_bytes(4, 'little'))
                    et['robs_forces'] = et.get('robs_forces', 0) + 1
                    if et['robs_forces'] == 1:
                        d.dire('      >>> ROB 0x%X +0x10 : %s -> %s'
                               % (rob, nom(v), nom(forcer)))
            return
        if bp.nom == 'SourceIndice':
            a = (ctx.Rbx + DECALAGE_SOURCE) & 0xFFFFFFFFFFFFFFFF
            v = d.u32(a)
            proche = ''
            for k, rob in enumerate(et['robs']):
                if abs(a - rob) < 0x8000:
                    proche = '   ROB%d%+d' % (k + 1, a - rob)
            cle = ('SourceIndice', v, '0x%X' % a)
            premier = cle not in et['sites']
            et['sites'][cle] += 1
            if premier:
                d.dire('  SourceIndice : rbx=0x%X  [rbx-0x10C]=0x%X vaut %s (%s)%s'
                       % (ctx.Rbx, a, v, nom(v), proche))
            if forcer is not None and (depuis is None or v == depuis):
                d.write(a, int(forcer).to_bytes(4, 'little'))
                et['forces'] += 1
                if premier:
                    d.dire('      >>> ecrit %d (%s) a 0x%X'
                           % (forcer, nom(forcer), a))
            return
        c = ctx.Rcx & 0xFFFFFFFF
        ret = d.u64(ctx.Rsp)
        nm, dp = d.module_of(ret) if ret else ('?', 0)
        cle = (bp.nom, c, '%s+0x%X' % (nm, dp))
        premier = cle not in et['sites']
        et['sites'][cle] += 1
        if premier:
            d.dire('  %s(%d = %s)   depuis %s+0x%X'
                   % (bp.nom, c, nom(c), nm, dp))
        if forcer is not None and (depuis is None or c == depuis):
            ctx.Rcx = forcer
            ctx.ContextFlags = (instrument.CONTEXT_FULL
                                | instrument.CONTEXT_DEBUG_REGISTERS)
            d.poser_contexte(tid, ctx)
            et['forces'] += 1
            if premier:
                d.dire('      >>> force a %d (%s)' % (forcer, nom(forcer)))

    def tic(d, t):
        if et['pose'] or t < pose_a:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        liste = [('MothApplyRecord', MOTH_APPLY_RECORD),
                 ('SourceIndice', SOURCE_INDICE)]
        if '--code' in argv:
            liste.append(('CodeDuPersonnage', CODE_PERSO))
        if '--jumelles' in argv:
            liste += [('CodeDuPersonnage_B', CODE_PERSO_B),
                      ('NomLocalise', CODE_PERSO_C)]
        if '--seul' in argv:
            liste = [('MothApplyRecord', MOTH_APPLY_RECORD)]
        # --moth : la resolution des animations. Dural reste sur son repos
        # (0x510B = DUR_L_IDLE_TA, role 0) alors que TAK force par la meme
        # methode enchaine. La question est : quels ROLES le moteur demande-t-il
        # dans chaque cas, et rendent-ils quelque chose ?
        #
        # ATTENTION : `MothOnMotionEnd` 0x180133010 et `RoleToMotionId`
        # 0x180147680 d'`analysis/functions.csv` sont les adresses du build
        # **Steam**, pas d'APM3 -- s'en servir ici donne zero passage, erreur
        # commise le 2026-09-04. L'equivalent APM3 verifie dynamiquement
        # (14157/14157 contre motdb.py) est `GetMotionForRole` = 0x18015B310.
        # Signature : rcx = indice de personnage, rdx = posture, r8 = role.
        if '--moth' in argv:
            liste += [('GetMotionForRole', GET_MOTION_FOR_ROLE)]
        for n, rva in liste:
            bp = instrument.PointArret(n, b + rva, max_coups=200000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  points d\'arret poses a t=%.0f s' % t)

    def sur_dr(d, m, ctx, tid):
        nm, dp = d.module_of(ctx.Rip)
        val = d.u32(m.adresse)
        et['ecrivains'][('%s+0x%X' % (nm, dp), val)] += 1

    dbg.on_bp = sur_bp
    dbg.on_dr = sur_dr
    dbg.tic = tic

    with open(scenario, 'rb') as fp:
        data = fp.read()
    with open(SCENARIO_ACTIF, 'wb') as fp:
        fp.write(data)
    print('journal : %s%s' % (journal,
                              ('   forcage -> %d' % forcer) if forcer is not None else ''))
    dbg.run(EXE, os.path.dirname(EXE), secondes, tuple(captures))
    fichier.close()

    print('\n--- demandes, par site et par indice ---')
    for (fn, c, site), n in et['sites'].most_common(40):
        print('  %6d x  %-20s (%2d = %-4s)  depuis %s' % (n, fn, c, nom(c), site))
    if et['ecrivains']:
        print()
        print('--- qui ecrit ROB1+0x8A0 (l etat de mouvement) ---')
        par_site = collections.Counter()
        for (site, val), n in et['ecrivains'].items():
            par_site[site] += n
        for site, n in par_site.most_common(12):
            paires = [(v, c) for (s2, v), c in et['ecrivains'].items()
                      if s2 == site]
            paires.sort(key=lambda t: -t[1])
            print('  %7d ecriture(s)  %-34s %d valeur(s) distincte(s)'
                  % (n, site, len(paires)))
            # Les plus FREQUENTES, pas les plus petites : trier par valeur
            # cachait les identifiants propres au personnage, qui sont hauts.
            print('        %s'
                  % '  '.join('0x%X x%d' % (v, c) for v, c in paires[:10]))
    elif surveiller:
        print()
        print('--- ROB1+0x8A0 : AUCUNE ecriture relevee ---')
    if et['moth']:
        print('\n--- machinerie d enchainement ---')
        for n, v in sorted(et['moth'].items()):
            print('  %-18s %8d passage(s)' % (n, v))
    if forcer is not None:
        print('\nsubstitutions : %d' % et['forces'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
