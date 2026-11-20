#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quelles scenes nommees le jeu reclame-t-il, et depuis ou ?

Pourquoi cet outil. La grille de selection de la borne contient VINGT cases, et
la vingtieme est Dural -- mesure en memoire, 384 passages (analysis/dural.md
section 13). Mais elle ne s'affiche pas. La boucle qui dessine les cases est
donc bornee a dix-neuf quelque part, et quatre recherches statiques ne l'ont pas
trouvee.

D'ou ce renversement : au lieu de chercher la boucle dans le binaire, on demande
au jeu ce qu'il reclame. Les cases de la grille jouent des animations nommees
-- "aki", "pai", ... "tak", et normalement "dur". Si "dur" n'est jamais demande
alors que les dix-neuf autres le sont, **l'adresse de retour du dernier appel
nomme la boucle de dessin**, et sa borne est le defaut.

Deux entonnoirs sont surveilles :

    0x1801BCD70   scene AET par nom   (rcx=objet, rdx=sortie, r8=NOM, r9b=drapeau)
    0x180245830   lecteur de scene nommee (rdx=NOM) -- celui de UNLOCK_DURAL

Il faut que le jeu RESTE sur l'ecran de selection pendant la mesure : un
scenario qui le traverse rend la mesure aveugle, ce qui a fait tourner deux
passes a vide le 2026-09-04.

    py -3 tools/pister_scenes.py --secondes 150
"""
import collections
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
SCENE_AET = 0x1BCD70          # RVA, nom en r8
SCENE_NOMMEE = 0x245830       # RVA, nom en rdx
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')
PERSOS3 = ('aki', 'sar', 'lau', 'shu', 'jef', 'pai', 'jak', 'kag', 'lio', 'wol',
           'aoi', 'lei', 'van', 'bra', 'goh', 'mon', 'msk', 'krt', 'tak', 'dur',
           'rnd')


def main():
    argv = sys.argv[1:]
    secondes, pose_a = 150, 10.0
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'jouer.txt')
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--a' in argv:
        pose_a = float(argv[argv.index('--a') + 1])
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 300000
    journal = os.path.join(RACINE, 'analysis', 'pister_scenes.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'noms': collections.Counter(),
          'sites': collections.defaultdict(collections.Counter)}

    def chaine(d, adr):
        if not adr:
            return None
        b = d.read(adr, 40)
        if not b:
            return None
        b = b.split(bytes([0]), 1)[0]
        if 1 <= len(b) <= 36 and all(32 <= c < 127 for c in b):
            return b.decode('latin-1')
        return None

    def sur_bp(d, bp, ctx, tid):
        adr = ctx.R8 if bp.nom == 'SceneAET' else ctx.Rdx
        n = chaine(d, adr)
        if not n:
            return
        et['noms'][n] += 1
        ret = d.u64(ctx.Rsp)
        if ret:
            nm, dp = d.module_of(ret)
            et['sites'][n]['%s+0x%X' % (nm, dp)] += 1

    def tic(d, t):
        if et['pose'] or t < pose_a:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        for n_, rva_ in (('SceneAET', SCENE_AET), ('SceneNommee', SCENE_NOMMEE)):
            bp = instrument.PointArret(n_, b + rva_, max_coups=300000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  points d\'arret sur les scenes nommees, a t=%.0f s' % t)

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
    print('--- les vingt-et-un codes de personnage, demandes ou non ---')
    manquants = []
    for p in PERSOS3:
        n = et['noms'].get(p, 0)
        site = ''
        if n:
            site = ' depuis ' + et['sites'][p].most_common(1)[0][0]
        else:
            manquants.append(p)
        print('  %-4s %6d appel(s)%s' % (p, n, site))
    print()
    if manquants:
        print('JAMAIS DEMANDES : %s' % ', '.join(manquants))
    else:
        print('Tous demandes -- la grille reclame bien les vingt et un.')
    print()
    print('--- les 25 noms les plus demandes, tous confondus ---')
    for n, c in et['noms'].most_common(25):
        print('  %6d  %-28s %s'
              % (c, n, et['sites'][n].most_common(1)[0][0] if et['sites'][n] else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
