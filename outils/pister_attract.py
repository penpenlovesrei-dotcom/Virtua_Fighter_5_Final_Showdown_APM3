#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pourquoi l'attract ne se joue pas : que repond l'hote a la requete 14 ?

`CS_DEMO` (sous-etat 6, entree `0x1803A0660`) sort au bout d'un demi-seconde,
et cela **sans aucun de nos correctifs** -- controle du 2026-09-06 sur le
binaire remis a `.origine`. Ce n'est donc pas une regression du chantier.

Son gestionnaire d'entree (`0x1800DDC40`) interroge l'objet de configuration
de l'hote (`0x180C3B6F0`, champ `+0x1FE10` = la fonction, `+0x1FE18` = son
contexte) avec le code 14, et **exige la reponse 2** :

    0x1800DDC7A  lea  edx, [r8 + 0xE]     ; 14
    0x1800DDC85  call rax
    0x1800DDC87  cmp  eax, 2              ; != 2 -> abandon

et sa mise a jour (`0x1800DD4F0`) sort des que la scene n'est plus vivante :

    0x1800DD548  call 0x1800E8800         ; "la scene joue-t-elle encore ?"
    0x1800DD558  mov  al, 1               ; faux -> j'ai fini

On lit donc les deux : la reponse a la requete 14, et l'etat de la scene.

    py -3 tools/pister_attract.py --secondes 60
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
    ('entree CS_DEMO',   0x0DDC40),   # le gestionnaire d'entree du sous-etat
    ('reponse requete 14', 0x0DDC87),  # juste apres le call : eax = la reponse
    ('maj CS_DEMO',      0x0DD4F0),
    ('scene vivante ?',  0x0DD54D),   # juste apres 0x1800E8800 : al = la reponse
    ('sortie CS_DEMO',   0x0DD558),   # la branche "j'ai fini"
    ('TaskMovie ?',      0x0E8800),   # le predicat lui-meme
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
    journal = os.path.join(RACINE, 'analysis', 'pister_attract.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'compte': collections.Counter(), 't0': None,
          'vus': set()}

    def note(txt):
        fichier.write(txt + os.linesep)
        fichier.flush()

    def sur_bp(d, bp, ctx, tid):
        et['compte'][bp.nom] += 1
        if et['t0'] is None:
            et['t0'] = time.time()
        ms = (time.time() - et['t0']) * 1000.0
        n = et['compte'][bp.nom]

        if bp.nom == 'reponse requete 14' and n <= 6:
            note('%9.1f ms  requete 14 -> eax = %d   (%s ; il faut 2)'
                 % (ms, ctx.Rax & 0xFFFFFFFF,
                    'ACCEPTE' if (ctx.Rax & 0xFFFFFFFF) == 2 else 'REFUSE'))
            return
        if bp.nom == 'scene vivante ?' and n <= 6:
            note('%9.1f ms  scene vivante ? al = %d'
                 % (ms, ctx.Rax & 0xFF))
            return
        if bp.nom not in et['vus']:
            et['vus'].add(bp.nom)
            note('%9.1f ms  PREMIERE FOIS : %s' % (ms, bp.nom))

    def tic(d, t):
        if et['pose']:
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

    print('MESURE : pourquoi l attract ne se joue pas.')
    print('  Laissez tourner. Aucune touche.')
    print()
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    lignes = []

    def dit(t=''):
        lignes.append(t)

    dit()
    dit('=' * 72)
    dit('COMPTES :')
    for nom_, _ in POINTS:
        dit('   %-20s %d' % (nom_, et['compte'][nom_]))
    dit()
    dit('RELEVE :')
    with open(journal, encoding='utf-8') as fp:
        for l in fp:
            if 'requete 14' in l or 'scene vivante' in l or 'PREMIERE' in l:
                dit('   ' + l.rstrip())
    bilan = os.path.join(RACINE, 'analysis', 'pister_attract_bilan.txt')
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
