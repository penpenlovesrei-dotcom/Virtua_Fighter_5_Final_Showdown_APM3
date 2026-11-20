#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La chaine d'entrees, de la touche du clavier au code que l'interface lit.

Trois etages, et c'est le deuxieme qui manquait :

  1. `apm.dll` (notre stub) rend `Input_isOn(code)` pour les codes 0 a 14.
     La correspondance touche -> code est dans `tools/gen_apm_stub.py`.

  2. `0x180243ED0` lit ces codes et **compose un masque de boutons arcade**
     range en `0x180751050 + joueur*0x54`. C'est la que « G, P, K, start,
     coin » prennent leur place dans un mot de 32 bits.

  3. `0x1801A2200` traduit ce masque en **codes logiques** (0 a 103) via une
     table de seize paires (masque, code) copiee au demarrage par
     `0x1801A2AB0` depuis `0x18040AEC0`. Ce sont ces codes-la que lisent
     `0x180190B80` (fronts) et `0x180190BC0` (tenus), donc toute l'interface :
     curseur de la grille, menus, validation.

    py -3 tools/entrees.py
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import pe_disasm as P                                        # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')
TABLE = 0x18040AEC0                 # seize paires (masque, code logique)

# `0x180243ED0`, joueur 1 : Input_isOn(code) -> bit du masque arcade.
# Releve instruction par instruction, pas devine.
APM3_VERS_BIT = {2: 12, 5: 13, 3: 14, 4: 15, 7: 0, 8: 1, 12: 2, 11: 3,
                 13: 4, 14: 5, 9: 6, 10: 7, 6: 9}
# `tools/gen_apm_stub.py`, table par defaut du stub.
#
# CORRIGEE le 2026-09-30 : elle datait d'avant le choix de Frederic (« la
# rangee W X C V, qui tombe sous la main gauche en AZERTY ») et annoncait
# encore A Z E R. Un outil de mesure qui ment est pire que pas d'outil.
TOUCHES = {0: 'F1 (TEST)', 1: 'F2 (SERVICE)', 2: 'Haut', 3: 'Bas', 4: 'Gauche',
           5: 'Droite', 6: 'Espace (piece)', 7: 'Entree (START)',
           8: 'W (carre)', 9: 'X (croix)', 10: 'C (rond)', 11: 'V (triangle)',
           12: 'T (L1)', 13: 'Y (R1)', 14: 'U (R2)',
           15: 'Echap (sortie)', 16: 'B (camera)', 17: 'N (vue)'}
# ce que l'interface fait de chaque code logique
ROLES = {2: 'lu par personne dans le menu ni le selecteur',
         3: 'curseur HAUT', 4: 'curseur BAS',
         5: 'curseur GAUCHE', 6: 'curseur DROITE',
         7: 'grille : VALIDER', 8: 'grille : VALIDER', 9: 'grille : VALIDER',
         11: 'grille : VALIDER -- MAIS AUCUN BIT NE LE PRODUIT',
         13: 'aucun bit ne le produit non plus', 99: 'non identifie',
         100: 'combat (P/K/G)', 101: 'combat', 102: 'combat', 103: 'combat'}

# CE QUE LE MASQUE ARCADE N'EST PAS.
#
# Ce fichier decrit la chaine du MASQUE. Il faut lire avec lui le fait que
# `tools/boutons_terminal.py` a mesure le 2026-09-30 : **les menus ne passent
# pas par le masque pour valider ni pour annuler**. `0x1801A2BC0` (VALIDER)
# et `0x1801A2B90` (ANNULER) appellent le creneau `+0x160` (`Input_isOnNow`)
# sur les codes **7** et **8** du stub, directement. Le masque sert au
# curseur, aux boutons de combat, a la piece, et aux ecrans qui lisent
# `0x1801A2CA0` / `0x1801A2C10` avec un masque explicite.
#
# Et le code **15** n'est PAS libre : `0x18021490F` fait `Input_isOnNow(15)`.
# Les codes reellement libres des 32 creneaux du stub sont **16, 17 et 31**
# (0 a 15 sont lus par le moteur ; `--joueur2` reserve 18 a 30 au joueur 2).
# Les 16 et 17 servent depuis `--terminal-boutons`.


def main():
    img = P.Image(MOTEUR)
    d = img.read(TABLE, 0x80)
    paires = [struct.unpack_from('<II', d, 8 * i) for i in range(16)]
    bit_vers_code = {}
    for masque, code in paires:
        for b in range(32):
            if masque >> b & 1:
                bit_vers_code[b] = code

    print('CHAINE COMPLETE DES ENTREES (joueur 1)')
    print()
    print('%-16s %-5s %-8s %-6s %s'
          % ('touche', 'apm', 'bit', 'code', 'role dans l interface'))
    print('-' * 74)
    for apm in sorted(APM3_VERS_BIT, key=lambda c: APM3_VERS_BIT[c]):
        bit = APM3_VERS_BIT[apm]
        code = bit_vers_code.get(bit)
        print('%-16s %-5d %-8s %-6s %s'
              % (TOUCHES.get(apm, '?'), apm, '%d (0x%X)' % (bit, 1 << bit),
                 code if code is not None else '--',
                 ROLES.get(code, '') if code is not None else
                 'aucun code logique'))
    print()
    print('Table de traduction 0x%X, seize paires (masque -> code) :' % TABLE)
    for masque, code in paires:
        bits = [b for b in range(32) if masque >> b & 1]
        print('   masque 0x%06X  bits %-10s -> code %3d   %s'
              % (masque, ','.join(str(b) for b in bits), code,
                 ROLES.get(code, '')))
    print()
    manquants = sorted(c for c in ROLES if c not in bit_vers_code.values())
    if manquants:
        print('Codes lus par l interface mais qu AUCUN bit ne produit : %s'
              % ', '.join(str(c) for c in manquants))
    return 0


if __name__ == '__main__':
    sys.exit(main())
