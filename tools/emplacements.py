#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Quels emplacements sont LIBRES, et lesquels sont deja pris.

Ecrit le 2026-09-09, apres avoir casse `trm` en le prenant pour un emplacement
vierge. La regle du chantier, posee par Frederic :

    on AJOUTE des decors, on n'en REMPLACE aucun --
    sauf, eventuellement, les decors d'essai.

Encore faut-il savoir lesquels sont vraiment d'essai ET vraiment libres. Cet
outil ne le devine pas, il le MESURE, sur quatre preuves independantes :

  1. LA TABLE DES DESCRIPTEURS (0x180403430, 41 x 0xF0). Un decor d'essai a une
     signature reconnaissable en +0x14 : DEUX objets seulement -- +0x18, +0x20
     et +0x24 valent -1 -- et les deux appartiennent a son propre objset. Un
     vrai decor en a cinq.

     PREMIERE VERSION, TROP ETROITE : j'avais fige les rangs a 0 et 1, et
     `ts2` (rangs 1 et 2) et `ts3` (1 et 2) sont ressortis « vrais decors ».
     Une enumeration ne vaut que sa premisse : on teste la FORME (deux objets,
     du bon objset), pas des valeurs devinees.
  2. LA GRILLE DE SELECTION (0x180400210, 21 cases, indice en +0x08).
  3. LA LISTE D'APERCUS de 0x180174BF0 -- 26 entrees, construites en dur sur
     la pile. Un emplacement qui y figure n'est pas d'essai.
  4. NOS PROPRES LANCEURS : tout code a trois lettres cite dans tools/*.cmd
     designe un emplacement qu'un correctif valide utilise deja.

C'est la preuve 4 qui manquait le 2026-09-08 : `trm` porte le decor TERMINAL,
repare et valide a l'ecran le 2026-09-05 (`decor_TRM.cmd`), et `ts2` est ce que
l'ecran Customize charge d'origine (`decor_TS2.cmd`).

    py -3 tools/emplacements.py
    py -3 tools/emplacements.py --libres      (juste la liste, pour un script)
    py -3 tools/emplacements.py --pourquoi trs   (les raisons, une par ligne)

`--pourquoi` existe parce que le garde-fou se mordait la queue : des qu'un
lanceur NOMME l'emplacement qu'il pose, la preuve 4 le declare pris, et
`importer_decor.py --vers` le refuse -- y compris a ce lanceur-la. La sortie
distingue donc ce qui interdit vraiment (`descripteur`, `grille`, `apercu` :
le moteur s'en sert) de ce qui n'est qu'une RESERVATION par l'un de nos `.cmd`
(`lanceur <nom>`), qu'un lanceur peut lever pour lui-meme via `--pour`.
"""
import os
import re
import struct
import sys

import pefile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
DLL = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                   'vf5fs-pxd-w64-Retail_APM3.dll.origine')
BASE = 0x180000000
TABLE = 0x180403430
PAS = 0xF0
GRILLE = 0x180400210
GRILLE_CASES = 21

CODES = ['tst', 'ts2', 'ts3', 'wht', 'ban', 'ter', 'nyc', 'cas', 'riv', 'jin',
         'sin', 'djo', 'umi', 'hai', 'are', 'slk', 'yuk', 'tak', 'aur', 'bar',
         'tan', 'du1', 'du2', 'du3', 'du4', 'du5', 'trm', 'cid', 'trs',
         'evo00', 'evo01', 'evo02', 'evo03', 'evo04', 'evo05', 'evo06',
         'evo07', 'evo08', 'evo09', 'gym', 'smo']

# Les indices que la liste d'apercus de 0x180174BF0 porte, releves au
# desassembleur : 4..25 puis 39, 40, 41 (41 = la case ALEA).
APERCUS = set(range(4, 26)) | {39, 40, 41}


def descripteurs(pe):
    """Rend {indice: (objset, est_une_signature_de_decor_d_essai)}."""
    out = {}
    for i in range(len(CODES)):
        d = pe.get_data(TABLE + i * PAS - BASE, PAS)
        objset = struct.unpack_from('<I', d, 0x10)[0]
        objets = struct.unpack_from('<5I', d, 0x14)
        vides = (objets[1], objets[3], objets[4]) == (0xFFFFFFFF,) * 3
        siens = all(v != 0xFFFFFFFF and (v >> 16) == objset
                    for v in (objets[0], objets[2]))
        out[i] = (objset, vides and siens)
    return out


def grille(pe):
    d = pe.get_data(GRILLE - BASE, GRILLE_CASES * 0x20)
    return {struct.unpack_from('<i', d, i * 0x20 + 8)[0]
            for i in range(GRILLE_CASES)}


def cites_par_nos_lanceurs():
    """Les codes qu'un de nos lanceurs .cmd nomme -- donc deja utilises."""
    pris = {}
    mot = re.compile(r'\b(%s)\b' % '|'.join(CODES))
    for n in sorted(os.listdir(ICI)):
        if not n.endswith('.cmd'):
            continue
        t = open(os.path.join(ICI, n), 'rb').read().decode('latin-1')
        # on ignore les lignes de commentaire : elles CITENT sans utiliser
        utile = '\n'.join(l for l in t.split('\r\n')
                          if not l.lstrip().lower().startswith(('rem', 'echo')))
        for c in set(mot.findall(utile)):
            pris.setdefault(c, []).append(n)
    return pris


def main():
    argv = sys.argv[1:]
    pe = pefile.PE(DLL, fast_load=True)
    desc = descripteurs(pe)
    dans_grille = grille(pe)
    par_lanceur = cites_par_nos_lanceurs()

    libres, pris = [], []
    for i, code in enumerate(CODES):
        objset, essai = desc[i]
        raisons = []
        if not essai:
            raisons.append('vrai decor (cinq objets)')
        if i in dans_grille:
            raisons.append('case de la grille')
        if i in APERCUS:
            raisons.append('apercu en dur')
        if code in par_lanceur:
            raisons.append('utilise par %s' % ', '.join(sorted(par_lanceur[code])))
        (pris if raisons else libres).append((i, code, objset, raisons))

    if '--libres' in argv:
        print(' '.join(c for _, c, _, _ in libres))
        return 0

    if '--pourquoi' in argv:
        # Une raison par ligne, etiquetee, pour qu'un script puisse separer ce
        # que le MOTEUR utilise de ce qu'un de nos lanceurs a seulement
        # reserve. Rien n'est imprime si l'emplacement est libre.
        i = argv.index('--pourquoi') + 1
        quel = argv[i] if i < len(argv) else ''
        if quel not in CODES:
            print('--pourquoi attend un code parmi : %s' % ' '.join(CODES),
                  file=sys.stderr)
            return 1
        k = CODES.index(quel)
        objset, essai = desc[k]
        if not essai:
            print('descripteur vrai decor (cinq objets)')
        if k in dans_grille:
            print('grille case de la grille de selection')
        if k in APERCUS:
            print('apercu apercu construit en dur')
        for n in sorted(par_lanceur.get(quel, [])):
            print('lanceur %s' % n)
        return 0

    print('=' * 74)
    print('EMPLACEMENTS -- on AJOUTE, on ne remplace rien (sauf decors d essai)')
    print('=' * 74)
    print('\nLIBRES : %d' % len(libres))
    for i, code, objset, _ in libres:
        print('   %2d  %-6s objset %-4d' % (i, code, objset))
    print('\nPRIS : %d' % len(pris))
    for i, code, objset, raisons in pris:
        if 'vrai decor (cinq objets)' in raisons and len(raisons) > 1:
            raisons = ['vrai decor']
        print('   %2d  %-6s %s' % (i, code, ' + '.join(raisons)))
    print('\n' + '=' * 74)
    print('Les deux pieges du 2026-09-08 sont dans la liste PRIS :')
    print('  trm -> le decor TERMINAL, repare et valide le 2026-09-05')
    print('  ts2 -> ce que l ecran Customize charge d origine')
    print('Un emplacement deja repare n est pas un emplacement libre.')
    print('=' * 74)
    return 0


if __name__ == '__main__':
    sys.exit(main())
