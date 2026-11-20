# -*- coding: utf-8 -*-
"""Lit ram/options.bin -- les reglages d OPTIONS que apm.dll tient depuis le
2026-10-09 -- et les lignes OPT du journal.

Le fichier porte un en-tete de deux mots de 32 bits (magie "VF5O", taille du
bloc) puis les 0x88 octets preleves dans la structure globale du moteur :

    0x00 .. 0x84   =   [0x180752148] + 0x4FD0 .. 0x5054
    0x84 .. 0x88   =   [0x180752148] + 0x5074 .. 0x5078

Les trois temoins lisibles sont aux adresses que le moteur lui-meme emploie :
0x5014 et 0x5018 (les volumes, " vcvtsi2ss " en 0x1801B9013 et 0x1801B9033),
0x5020 (Tips, accesseur 0x1801B8980).
"""
import io
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RAC = os.path.dirname(ICI)
FIC = os.path.join(RAC, 'runtime', 'media', 'vf5fs', 'ram', 'options.bin')
JRN = os.path.join(RAC, 'runtime', 'media', 'vf5fs', 'apm_journal.txt')

MAGIE = 0x4F354656
TETE = 0x4FD0
TAILLE = 0x88
TEMOINS = ((0x5014, 'volume 1 (mixeur, 0x1801B9013)'),
           (0x5018, 'volume 2 (mixeur, 0x1801B9033)'),
           (0x501C, 'champ 0x501C'),
           (0x5020, 'Tips      (accesseur 0x1801B8980)'))


def champ(d, va):
    """La valeur de 32 bits du champ d adresse va, prise dans le bloc."""
    o = va - TETE
    if o < 0 or o + 4 > len(d):
        return None
    return struct.unpack_from('<I', d, o)[0]


def main():
    print()
    print('  LES REGLAGES D OPTIONS ENREGISTRES')
    print('  ' + '=' * 68)
    print()
    if not os.path.exists(FIC):
        print('  %s' % FIC)
        print('  N EXISTE PAS ENCORE.')
        print()
        print('  C est normal avant le premier essai : apm.dll ne l ecrit')
        print('  qu une fois un reglage change. Lancez le jeu par')
        print('  tools\\item_porte.cmd, changez un volume dans OPTIONS >')
        print('  Settings, quittez par EXIT GAME, puis relancez ce lecteur.')
        print()
        return 0
    brut = io.open(FIC, 'rb').read()
    print('  %s' % FIC)
    print('  %d octets' % len(brut))
    if len(brut) < 8:
        print('  TROP COURT pour porter l en-tete : fichier inexploitable.')
        return 1
    magie, taille = struct.unpack_from('<II', brut, 0)
    ok = magie == MAGIE and taille == TAILLE and len(brut) == 8 + TAILLE
    print('  magie  0x%08X  %s' % (magie, 'VF5O, attendue'
                                   if magie == MAGIE else 'INATTENDUE'))
    print('  taille %d octets  %s' % (taille, 'attendue' if taille == TAILLE
                                      else 'INATTENDUE'))
    if not ok:
        print()
        print('  Le fichier n est pas au format attendu : apm.dll le refusera')
        print('  proprement et laissera les reglages du moteur en place.')
        return 1
    d = brut[8:]
    print()
    for va, nom in TEMOINS:
        print('  +0x%04X  %-34s %d' % (va, nom, champ(d, va)))
    print()
    print('  le bloc entier, 0x4FD0 .. 0x5054 puis 0x5074 .. 0x5078 :')
    for i in range(0, len(d), 16):
        va = TETE + i if i < 0x84 else 0x5074 + (i - 0x84)
        print('    0x%04X  %s' % (va, ' '.join('%02X' % b for b in d[i:i+16])))
    print()
    if not os.path.exists(JRN):
        print('  (pas de apm_journal.txt : la trace est effacee a chaque')
        print('   lancement par item_porte.cmd)')
        return 0
    lignes = [l.rstrip() for l in io.open(JRN, encoding='latin-1')
              if 'OPT ' in l]
    print('  LES LIGNES OPT DU JOURNAL (%d) :' % len(lignes))
    if not lignes:
        print('    aucune -- apm.dll n a pas atteint son tour de garde.')
    for l in lignes[-20:]:
        print('    %s' % l.strip())
    print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
