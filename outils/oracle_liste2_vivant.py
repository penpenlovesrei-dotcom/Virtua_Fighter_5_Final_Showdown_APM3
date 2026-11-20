#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fait arbitrer les gestionnaires de la liste 2 par le jeu en marche.

tools/oracle_handlers.py fait deja cela hors du jeu, sur un faux combattant. Mais
un faux ROB a tous ses drapeaux a zero : les gestionnaires gardes ne font rien, et
ceux qui derefencent un global plantent. Ici, c'est le vrai combattant du vrai
combat qui sert de sujet.

Methode, pour chaque gestionnaire surveille :

 1. point d'arret logiciel sur son entree ; a l'entree on connait
    ctx (rcx), la charge utile (rdx) et l'entree de liste 2 (r8) ;
 2. on lit ROB[0 .. TAILLE] -- l'instantane AVANT -- et l'adresse de retour
    empilee en [rsp] ;
 3. on pose un point d'arret a cette adresse de retour ;
 4. quand il tombe, on relit ROB et on DIFFE : les mots changes sont exactement
    ce que le gestionnaire a ecrit, dans les conditions reelles du combat.

Le releve est ensuite compare a la prediction tiree du desassemblage. Un accord
fait passer le code de LIKELY a SUPPORTED ; un desaccord est signale comme tel.

Usage :
    py -3 tools/oracle_liste2_vivant.py --codes 12,17,19,27
    py -3 tools/oracle_liste2_vivant.py --codes 20,21,22 --secondes 150 --a 55
    py -3 tools/oracle_liste2_vivant.py --codes 1,7 --coups 3
"""
import csv
import io
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
IMAGE_BASE = 0x180000000
TABLE = 0x648840                      # RVA de la table des 55 gestionnaires (liste 2)
TABLE1 = 0x3F95B0                     # RVA de la table des 84 gestionnaires (liste 1)
ETAT = 0x8A0                          # l'etat de mouvement dans le ROB (build APM3)
TAILLE = 0x3000                       # fenetre de ROB observee

# ROB+0x10 est l'indice du personnage : l'entree dans rob_cmn_mottbl. La table
# ci-dessous vient de RobMotTbl.label(), qui identifie chaque entree par son jeu
# d'animations dominant. Noter que 19 est un doublon d'AKI -- les deux entrees
# partagent la meme table de postures.
PERSOS = ['AKI', 'SAR', 'LAU', 'SHU', 'JEF', 'PAI', 'JAK', 'KAG', 'LIO', 'WOL',
          'AOI', 'LEI', 'VAN', 'BRA', 'GOH', 'MON', 'MSK', 'KRT', 'TAK', 'AKI', 'DUR']
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')

# Ce que la lecture du desassemblage predit, code par code : les champs ecrits,
# en offsets de ROB. Vide = aucune ecriture directe predite (le gestionnaire
# delegue ou se contente d'appeler).
PREDIT = {
    1:  [],
    7:  [],
    10: [0x66C],
    12: [ETAT + 0x4AC],
    13: [],
    17: [ETAT + 0x4B0, ETAT + 0x4B4, ETAT + 0x4B8, ETAT + 0x4BC,
         0x11CC, 0x11D0, 0x11D4],
    18: [],
    19: [],
    20: [0x668], 21: [0x668], 22: [0x668], 23: [0x668], 24: [0x668],
    25: [],
    27: [],
    29: [],
    31: [],
    32: [ETAT + 0x4C6],
    33: [ETAT + 0x78C],
    50: [0x864, 0x898],
    51: [0x668],
    52: [],
    53: [ETAT + 0x888, ETAT + 0x88C],
    54: [],
    # codes deja etablis, gardes ici pour pouvoir les revoir
    9:  [ETAT + 0x4A8],
    26: [0x65C, 0x660],
    28: [ETAT + 0x4B0, ETAT + 0x4B4, ETAT + 0x4BC],
    30: [ETAT + 0x92C, ETAT + 0x934],
    3:  [ETAT + 0x1C], 4: [ETAT + 0x1C], 5: [0x6C0], 6: [0x66C, ETAT + 0x1C],
    14: [0x690], 15: [0x690], 16: [0x690],
    11: [], 2: [ETAT + 0x1C, ETAT + 0x35C], 8: [], 0: [], 34: [ETAT + 0x7AC],
    35: [ETAT + 0x7B4],
}


def libelle(off):
    if off >= ETAT:
        return 'etat+0x%03X' % (off - ETAT)
    return 'ROB+0x%03X' % off


def main():
    argv = sys.argv[1:]
    secondes, pose_a, coups = 140, 55.0, 2
    codes = [12, 17, 19, 27]
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'combat_martelage.txt')
    journal = os.path.join(RACINE, 'analysis', 'oracle_liste2_vivant.txt')
    if '--codes' in argv:
        codes = [int(x, 0) for x in argv[argv.index('--codes') + 1].split(',')]
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--a' in argv:
        pose_a = float(argv[argv.index('--a') + 1])
    if '--coups' in argv:
        coups = int(argv[argv.index('--coups') + 1])
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]
    if '--journal' in argv:
        journal = argv[argv.index('--journal') + 1]
    # champs de ROB a relever a l'entree, pour verifier les gardes
    champs = []
    if '--champs' in argv:
        champs = [int(x, 0) for x in argv[argv.index('--champs') + 1].split(',')]
    # --liste 1 : surveiller les gestionnaires de la LISTE 1 au lieu de la liste 2.
    # L'oracle hors du jeu (tools/oracle_handlers.py) les fait tourner sur un faux
    # combattant a zero : quatre plantent sur un global nul et quatre ne font rien,
    # gardes par un drapeau eteint. Sur le vrai combattant, ces huit-la repondent.
    liste = 1 if ('--liste' in argv and argv[argv.index('--liste') + 1] == '1') else 2
    table = TABLE1 if liste == 1 else TABLE
    pas = 8 if liste == 1 else 32

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv     # sourdine par defaut
    dbg.bp_max = coups
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier

    etat = {'pose': False}
    attente = {}          # adresse de retour -> (code, rob, avant, charge, entree)
    vus = {}              # code -> nombre de releves complets
    resultats = []        # (code, [offsets changes], charge)
    vus_rob = set()       # pour annoncer chaque combattant une seule fois

    def sur_bp(d, bp, ctx, tid):
        if bp.nom.startswith('retour '):
            cle = bp.adresse
            info = attente.pop(cle, None)
            if info is None:
                return
            code, rob, avant, charge, ent = info
            apres = d.read(rob, TAILLE)
            if len(apres) != len(avant):
                return
            mots = sorted({(i // 4) * 4 for i in range(len(avant))
                           if avant[i] != apres[i]})
            d.dire('  == code %d : %d mot(s) change(s) ==' % (code, len(mots)))
            d.dire('     charge = %s   entree = %s'
                   % (charge.hex() if charge else '(aucune)', ent.hex()))
            for m in mots[:24]:
                d.dire('     %-14s %s -> %s'
                       % (libelle(m), avant[m:m + 4].hex(), apres[m:m + 4].hex()))
            if len(mots) > 24:
                d.dire('     ... %d de plus' % (len(mots) - 24))
            resultats.append((code, mots, charge.hex() if charge else ''))
            vus[code] = vus.get(code, 0) + 1
            d.desarmer_logiciel(bp)
            return

        # entree d'un gestionnaire
        code = int(bp.nom.rsplit(' ', 1)[1])
        rob = d.u64(ctx.Rcx)
        if not rob:
            return
        avant = d.read(rob, TAILLE)
        if len(avant) != TAILLE:
            return
        charge = d.read(ctx.Rdx, 16) if ctx.Rdx else b''
        ent = d.read(ctx.R8, 12 if liste == 2 else 8)
        if rob not in vus_rob:
            vus_rob.add(rob)
            n = d.u32(rob + 0x10) or 0
            d.dire('  combattant : ROB=0x%X  personnage %d = %s'
                   % (rob, n, PERSOS[n] if 0 <= n < len(PERSOS) else '?'))
        if champs:
            d.dire('  -- code %d, gardes a l entree : %s'
                   % (code, '  '.join('%s=%08X' % (libelle(o), d.u32(rob + o) or 0)
                                      for o in champs)))
        ret = d.u64(ctx.Rsp)
        if not ret or ret in attente:
            return
        attente[ret] = (code, rob, avant, charge, ent)
        r = instrument.PointArret('retour %d' % code, ret, max_coups=1)
        r.silencieux = True
        d.bps.append(r)
        d.armer_logiciel(r)

    def tic(d, t):
        if etat['pose'] or t < pose_a:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        etat['pose'] = True
        for c in codes:
            h = d.u64(b + table + pas * c)
            if not h:
                d.dire('  code %d : aucun gestionnaire installe' % c)
                continue
            bp = instrument.PointArret('gestionnaire liste%d code %d' % (liste, c), h,
                                       max_coups=coups)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  t=%.0f s : %d gestionnaire(s) de la liste %d sous surveillance'
               % (t, len(codes), liste))

    dbg.on_bp = sur_bp
    dbg.tic = tic

    if scenario and os.path.exists(scenario):
        with open(scenario, 'rb') as fp:
            data = fp.read()
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(data)
    print('liste %d, codes surveilles : %s' % (liste, codes))
    print('journal : %s' % journal)
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    with open(journal, encoding='utf-8') as fp:
        for ligne in fp:
            if ligne.startswith(('  ==', '     ', '  code', '  t=', '  --', '  combattant')):
                sys.stdout.write(ligne)

    print('\n--- verdict ---')
    for c in codes:
        rel = [r for r in resultats if r[0] == c]
        if not rel:
            print('code %-3d : JAMAIS VU (aucun passage pendant la fenetre)' % c)
            continue
        tous = sorted({m for _, mots, _ in rel for m in mots})
        pred = PREDIT.get(c, [])
        ok = [p for p in pred if p in tous]
        print('code %-3d : %d passage(s), %d mot(s) change(s) au total'
              % (c, len(rel), len(tous)))
        if pred:
            print('           predit %s -> observe %s%s'
                  % (' '.join(libelle(p) for p in pred),
                     ' '.join(libelle(p) for p in ok) or 'RIEN',
                     '' if len(ok) == len(pred) else '   (INCOMPLET)'))
        else:
            print('           aucune ecriture directe predite ; observe : %s'
                  % (' '.join(libelle(m) for m in tous[:10]) or 'rien'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
