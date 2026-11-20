#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Quel CODE porte chaque bouton sur l'ecran STAGE SELECT ?

La mesure qui manque pour faire defiler les variantes d'un decor au bouton
SELECT. `TaskSelStage::update` (`0x18017425E`) n'interroge pas la manette
directement : il lit un tableau d'etats range dans l'objet, par deux fonctions
triviales --

    0x1801724A0(base, code)  ->  octet [(code + 2) * 0x40 + base]
    0x180172450(base, code)  ->  vrai si [rec+0x28] == 6 ou [rec+0x20] == 6

ou `base` vaut `rbx + 0x70`. La validation interroge les codes **0** et **1**
(`r13d = rsi + 1`, `rsi = 0`) ; les autres ne sont pas connus.

`TaskSelStage` est un MEMBRE de `TaskSelector` : singleton `[0x180714928]`,
champ `+0x3B0`. Le tableau est donc en

    [0x180714928] + 0x3B0 + 0x70

et on releve, pour les codes -2 a 13, l'octet `+0x00` et les deux mots
`+0x20` / `+0x28` de chaque enregistrement. Quand un bouton est presse, son
enregistrement bouge : l'outil dit lequel.

    py -3 tools/pister_selstage.py
    py -3 tools/pister_selstage.py --secondes 300

Le clavier reste a vous. Allez jusqu'a STAGE SELECT, puis pressez UN bouton a
la fois en laissant une seconde entre deux.
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
SCENARIO = """# ecrit par tools/pister_selstage.py -- le clavier mene.
front   = 10
journal = 0
clavier = 1
manette = 1
0       rien
"""

SELECTOR_RVA = 0x714928           # [0x180714928] : le singleton TaskSelector
SELSTAGE_OFF = 0x3B0              # TaskSelStage est un membre
ENTREES_OFF = 0x70                # le tableau d'etats dans TaskSelStage
PAS = 0x40
CODES = range(-2, 14)

# Ce que le clavier envoie, d'apres apm_entrees.txt (disposition du stub).
RAPPEL = """  fleches = directions      Entree = VALIDER       W = ANNULER
  X C V   = croix rond triangle   ESPACE = SELECT        T Y U = L1 R1 R2"""


def main():
    argv = sys.argv[1:]
    secondes = 300
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    journal = os.path.join(os.path.dirname(ICI), 'analysis',
                           'pister_selstage.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = True
    dbg.sortie = fichier
    et = {'base': 0, 'vu': {}, 'trouves': {}, 'annonce': False}

    def tic(d, t):
        b = d.base_de(MOTEUR)
        if not b:
            return
        selector = d.u64(b + SELECTOR_RVA)
        if not selector:
            return
        base = selector + SELSTAGE_OFF + ENTREES_OFF
        if base != et['base']:
            et['base'] = base
            d.dire('  tableau d entrees a 0x%X (t=%.1f s)' % (base, t))
        if not et['annonce']:
            et['annonce'] = True
            d.dire('  --- l ecran est la : pressez UN bouton a la fois ---')
        for code in CODES:
            rec = base + (code + 2) * PAS
            octets = d.read(rec, 0x30)
            if len(octets) < 0x30:
                return
            etat = (octets[0], int.from_bytes(octets[0x20:0x24], 'little'),
                    int.from_bytes(octets[0x28:0x2C], 'little'))
            avant = et['vu'].get(code)
            et['vu'][code] = etat
            if avant is None or etat == avant:
                continue
            if etat[0] or etat[1] == 6 or etat[2] == 6:
                et['trouves'].setdefault(code, 0)
                et['trouves'][code] += 1
                d.dire('  t=%6.1f s  CODE %3d  actif : +0x00=%d  +0x20=%d  '
                       '+0x28=%d' % (t, code, etat[0], etat[1], etat[2]))

    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)

    print('MESURE : quel code porte chaque bouton sur STAGE SELECT.')
    print()
    print('  Le jeu se lance ; le clavier est a vous.')
    print('  Allez jusqu a OFFLINE VERSUS puis STAGE SELECT.')
    print('  La, pressez UN bouton a la fois, une seconde entre deux :')
    print(RAPPEL)
    print()
    print('  journal : %s' % journal)
    print()
    dbg.run(EXE, JEU, secondes, ())
    fichier.close()

    print()
    print('=' * 66)
    if not et['trouves']:
        print('AUCUN code n a bouge.')
        print('  Soit l ecran STAGE SELECT n a pas ete atteint, soit le')
        print('  singleton n etait pas construit : le tableau se lit en')
        print('  [0x180714928] + 0x3B0 + 0x70, et il faut que TaskSelector')
        print('  existe. Le journal dit si l adresse a ete trouvee.')
    else:
        print('CODES VUS ACTIFS (dans l ordre ou ils ont bouge) :')
        for code, n in sorted(et['trouves'].items(),
                              key=lambda x: -x[1]):
            connu = {0: 'interroge par la validation',
                     1: 'interroge par la validation'}.get(code, '')
            print('   code %3d  %4d changement(s)  %s' % (code, n, connu))
        print()
        print('  Le code qui n a bouge QUE pendant vos appuis sur ESPACE est')
        print('  celui de SELECT : c est lui qui fera defiler les variantes.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
