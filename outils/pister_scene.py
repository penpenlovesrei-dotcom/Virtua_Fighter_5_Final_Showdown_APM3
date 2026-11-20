#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pourquoi les sous-sous-menus d'options ne se valident-ils pas ?

Constat de Frederic : « je n'arrive plus a valider les sous/sous menus a part
credits ».

Dans l'aiguillage de la page OPTION (`0x1801A6F70`), quatre des cinq lignes
demarrent une SCENE et n'avancent que si ca reussit ; `Credits` est la seule
qui n'en demarre pas -- elle passe par une fabrique. D'ou le soupcon :
`0x180245830` echoue. La meme fonction avait deja echoue deux fois sur trois
dans la mesure des sous-menus du 2026-09-05.

Elle a DEUX portes, et une seule mesure les separe :

    0x1802456ED  call 0x180244F90   ; l'objet a-t-il DEJA une scene ?
    0x1802456F4  je   suite         ; non -> chemin normal
    0x1802456F6  cmp  [rbx+0x18], 3 ; sinon l'ancienne doit etre dans cet etat
    0x1802456FA  jne  ECHEC
    0x180245700  cmp  [rbx+0x24], 4
    0x180245704  jne  ECHEC
    0x180245715  call 0x180245020   ; trouver/charger la scene nommee
    0x18024571C  je   ECHEC

Points d'arret :

    0x1802456F4  entree : on lit le NOM demande (r12) et « existe deja » (al)
    0x1802457F4  l'echec
    0x18024571C  apres le chargement : al
    les cinq sites de la page OPTION, pour attribuer chaque essai a sa ligne

Le clavier reste actif : c'est vous qui menez le jeu.

    py -3 tools/pister_scene.py
    py -3 tools/pister_scene.py --secondes 300
"""
import collections
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                            # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
POINTS = [
    ('Garde', 0x1A7023),        # le switch est-il seulement atteint ?
    ('Demande', 0x2456F4),      # le NOM demande (rbp) + « existe deja ? » (al)
    ('Resultat', 0x2457F4),     # l'epilogue : le verdict est dans DIL
    ('L0 How to Play', 0x1A705C),
    ('L1 Controls', 0x1A70AE),
    ('L2 Settings', 0x1A70F4),
    ('L3 Save Data', 0x1A713A),
    ('L5 Info', 0x1A7183),
]
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                              'apm_entrees.txt')
SCENARIO = """# ecrit par tools/pister_scene.py -- le clavier mene.
front   = 200
journal = 0
clavier = 1
manette = 1
0       rien
"""


def main():
    argv = sys.argv[1:]
    secondes = 300
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 200
    journal = os.path.join(RACINE, 'analysis', 'pister_scene.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'compte': collections.Counter(), 'recit': [],
          'noms': collections.Counter(), 'dernier': '?'}

    def note(txt):
        if len(et['recit']) < 80:
            et['recit'].append(txt)

    def sur_bp(d, bp, ctx, tid):
        et['compte'][bp.nom] += 1
        if bp.nom == 'Garde':
            page = ctx.Rbx & 0xFFFFFFFFFFFFFFFF
            valide = (d.read(page + 0xC0, 1) or b'\x00')[0]
            entree = int.from_bytes(
                d.read(page + 0xB8, 4) or b'\x00\x00\x00\x00', 'little')
            note('GARDE  validation=%d  entree=%d%s'
                 % (valide, entree,
                    '   -> le switch est SAUTE' if not valide else ''))
        elif bp.nom == 'Demande':
            brut = d.read(ctx.Rbp & 0xFFFFFFFFFFFFFFFF, 40) or b''
            m = re.match(rb'[\x20-\x7e]{1,38}', brut)
            et['dernier'] = m.group().decode() if m else '?'
            note('DEMANDE "%s"   scene deja presente : %s'
                 % (et['dernier'], 'OUI' if ctx.Rax & 0xFF else 'non'))
        elif bp.nom == 'Resultat':
            ok = ctx.Rdi & 0xFF
            et['noms']['%s -> %s' % (et['dernier'],
                                     'OK' if ok else 'ECHEC')] += 1
            note('   "%s" -> %s' % (et['dernier'], 'OK' if ok else 'ECHEC'))
        else:
            note('LIGNE %s -> %s' % (bp.nom, 'OK' if ctx.Rax & 0xFF else 'ECHEC'))

    def tic(d, t):
        if et['pose'] or t < 8.0:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        for nom_, rva in POINTS:
            bp = instrument.PointArret(nom_, b + rva, max_coups=200000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  points d\'arret poses a t=%.0f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)

    print('MESURE : pourquoi les sous-sous-menus d\'options ne s\'ouvrent pas.')
    print()
    print('  Le jeu va se lancer. Faites CECI :')
    print('     deux fois Entree            -> menu console')
    print('     descendez sur HELP & OPTIONS, validez')
    print('     essayez de valider CHAQUE ligne, une par une :')
    print('        How to Play, Controls, Settings, Save Data, Credits')
    print('     puis fermez le jeu.')
    print()
    print('  journal : %s' % journal)
    print()
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    lignes = []

    def dit(txt=''):
        lignes.append(txt)
        print(txt)

    dit()
    dit('=' * 70)
    dit('SCENES DEMANDEES :')
    if not et['noms']:
        dit('   aucune -- 0x180245830 n\'a pas ete appelee du tout.')
    for k, n in et['noms'].most_common():
        dit('   %-52s x%d' % (k, n))
    dit()
    dit('COMPTES :')
    for nom_, _ in POINTS:
        dit('   %-18s %d' % (nom_, et['compte'][nom_]))
    dit()
    dit('RECIT (les 80 premiers evenements, dans l ordre) :')
    for t in et['recit']:
        dit('   ' + t)
    bilan = os.path.join(RACINE, 'analysis', 'pister_scene_bilan.txt')
    with open(bilan, 'w', encoding='utf-8') as fp:
        fp.write(os.linesep.join(lignes) + os.linesep)
    print()
    print('bilan ecrit dans %s' % bilan)
    return 0


if __name__ == '__main__':
    sys.exit(main())
