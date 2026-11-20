#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repond a « qui lit ce champ de l'etat de mouvement », dans un combat qui tourne.

Enchainement, entierement automatique :

 1. lance vfes.exe sous debogueur (tools/instrument.py) ;
 2. le apm.dll de substitution joue le scenario d'entrees et mene le jeu jusqu'au
    combat (deux appuis sur START) ;
 3. une fois le combat en cours, pose un point d'arret LOGICIEL sur
    MothApplyRecord -- APM3 0x180158B40 -- ou rdx est le ROB du combattant ;
 4. lit rdx, en deduit l'etat de mouvement, arme jusqu'a quatre points d'arret
    MATERIELS en lecture sur les champs demandes, puis desarme le point logiciel ;
 5. releve, pour chaque acces, l'adresse de l'instruction qui l'a fait.

Disposition de l'etat, etablie sur le build APM3 (voir docs/formats/mothead.md) :
    MothApplyRecord(rcx = ?, rdx = ROB, r8 = liste 1) construit
        ctx[0] = ROB          ctx[1] = ROB + 0x440       ctx[2] = ROB + 0x8A0
    L'etat de mouvement est donc a ROB + 0x8A0 dans le build APM3, et non a
    ROB + 0x798 comme dans le build R.E.V.O. : ecart constant de 0x108.

Usage :
    py -3 tools/pister_etat.py                          fenetres 0x154, 0x158, 0x15C
    py -3 tools/pister_etat.py --offsets 0x154,0x160    d'autres champs
    py -3 tools/pister_etat.py --secondes 90 --a 50     duree, et instant de la pose
    py -3 tools/pister_etat.py --acces w                surveiller les ecritures
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
MOTH_APPLY_RECORD = 0x158B40          # RVA dans le moteur APM3
IMAGE_BASE = 0x180000000
ETAT_DANS_ROB = 0x8A0                 # build APM3 ; R.E.V.O. : 0x798
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')

# Le copieur d'etat : une fonction de recopie champ par champ, entierement
# deroulee, qui duplique tout l'etat de mouvement a chaque trame. Il lit donc
# les 32 fenetres sans rien en faire, et noierait n'importe quel releve.
COPIEUR = (0x15EB30, 0x1602AF)


def main():
    argv = sys.argv[1:]
    secondes = 90
    pose_a = 50.0
    acces = 'r'
    offsets = [0x154, 0x158, 0x15C]
    journal = os.path.join(RACINE, 'analysis', 'pistage_fenetres.txt')
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--a' in argv:
        pose_a = float(argv[argv.index('--a') + 1])
    if '--acces' in argv:
        acces = argv[argv.index('--acces') + 1]
    if '--offsets' in argv:
        offsets = [int(x, 0) for x in argv[argv.index('--offsets') + 1].split(',')]
    if '--journal' in argv:
        journal = argv[argv.index('--journal') + 1]
    scenario = None
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]
    if '--dr-max' in argv:
        dr_max = int(argv[argv.index('--dr-max') + 1])
    else:
        dr_max = 24

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv     # sourdine par defaut
    dbg.bp_max = 6                     # deux ROB au moins : on ne sait pas lequel est le joueur
    dbg.dr_max = dr_max
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier

    etat = {'pose': False, 'rob': None}

    def sur_bp(d, bp, ctx, tid):
        # --brut : les offsets sont comptes depuis le ROB et non depuis l'etat.
        # Sert par exemple a surveiller ROB+0x10, l'indice du personnage.
        brut = '--brut' in argv
        rob = ctx.Rdx
        if rob and rob not in etat.setdefault('robs', []):
            etat['robs'].append(rob)
            n = d.u32(rob + 0x10)
            d.dire('  ROB %d = 0x%016X   personnage %s'
                   % (len(etat['robs']), rob, n))
        if etat['rob'] is not None:
            if brut and len(etat['robs']) == 2 and not etat.get('deux'):
                etat['deux'] = True
                for off in offsets[:2]:
                    d.armer_materiel(etat['robs'][1] + off, 4, acces,
                                     'ROB2+0x%03X' % off)
                d.desarmer_logiciel(bp)
            return
        base_etat = rob if brut else rob + ETAT_DANS_ROB
        etat['rob'] = rob
        d.dire('  ROB = 0x%016X   etat de mouvement = 0x%016X'
               % (rob, rob + ETAT_DANS_ROB))
        for off in offsets[:2 if brut else 4]:
            d.armer_materiel(base_etat + off, 4, acces,
                             ('ROB1+0x%03X' if brut else 'etat+0x%03X') % off)

    def plages(d):
        b = d.base_de(MOTEUR)
        if b and not d.dr_plages_ignorees and '--tout' not in argv:
            d.dr_plages_ignorees.append((b + COPIEUR[0], b + COPIEUR[1]))

    def tic(d, t):
        plages(d)
        if not etat['pose'] and t >= pose_a:
            etat['pose'] = True
            b = d.base_de(MOTEUR)
            if not b:
                d.dire('  %s pas encore chargee a t=%.0f s' % (MOTEUR, t))
                etat['pose'] = False
                return
            bp = instrument.PointArret('MothApplyRecord', b + MOTH_APPLY_RECORD)
            d.bps.append(bp)
            d.armer_logiciel(bp)
            d.dire('  t=%.0f s : point d\'arret pose sur MothApplyRecord' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    if scenario:
        with open(scenario, 'rb') as fp:
            data = fp.read()
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(data)
        print('scenario : %s (%d octets) installe' % (scenario, len(data)))
    print('journal : %s' % journal)
    print('le jeu est mene au combat par le scenario d\'entrees ; pose a t=%.0f s' % pose_a)
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    with open(journal, encoding='utf-8') as fp:
        for ligne in fp:
            if ligne.startswith(('  ROB', '  DR', '  BP', '  ignore', '  capture')):
                sys.stdout.write(ligne)
    print('journal complet : %s' % journal)
    return 0


if __name__ == '__main__':
    sys.exit(main())
