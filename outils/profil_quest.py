#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""LE PROFIL DU QUEST : le lire, l'effacer, l'eprouver.

`apm.dll` ecrit `quest_profil.bin` a cote du jeu. C'est NOTRE fichier -- la
sauvegarde de la Xbox 360 vit dans un conteneur de profil qui n'a pas
d'equivalent ici -- mais il porte les memes champs que le profil de 2007, et
notamment les deux champs de bits que le Quest interroge pour ses ecrans :

    +0x74 chez la Xbox   1000 bits : le rival a ete RENCONTRE
    +0xF4 chez la Xbox   1000 bits : le rival a ete BATTU

Disposition, petit-boutiste (voir le pave de `tools/quest_runtime.c`) :

    +0x000  8    « QUESTPRF »          +0x008  u32  version (1)
    +0x010  128  RENCONTRE             +0x090  128  BATTU
    +0x110  u32  plus longue serie     +0x114  u32  nombre de combats
    +0x118  u32  temps de jeu, en secondes

LE POURCENTAGE DES RIVAUX n'est pas devine : le code de 2007 compte ceux qui
sont A LA FOIS rencontres et battus, puis multiplie par `_DAT_82006C1C`
(0,001) et `DAT_82003EDC` (100) -- le compte divise par dix.

    py -3 tools/profil_quest.py --lire
    py -3 tools/profil_quest.py --effacer
    py -3 tools/profil_quest.py --battre 250     EPROUVE : 250 rivaux battus
    py -3 tools/profil_quest.py --battre 0       les remet a zero

`--battre` sert a VOIR bouger le statut sans avoir a gagner mille combats.
Ce n'est pas de la progression : c'est une sonde, et elle le dit.
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
CHEMIN = os.path.join(JEU, 'quest_profil.bin')
NPC = os.path.join(JEU, 'vf5fs_media', 'rom', 'npc_tbl.bin')

MAGIE = b'QUESTPRF'
VERSION = 2
TAILLE = 0x150
O_VERSION = 0x008
O_RENCONTRE = 0x010
O_BATTU = 0x090
O_SERIE = 0x110
O_COMBATS = 0x114
O_SECONDES = 0x118
# LA CARRIERE (version 2, 2026-09-29). Les valeurs viennent du Quest de 2007 :
# argent de depart 50 000 et plafond 999 999 (sequence d'accueil 0x8230CF50),
# grade 0 = 10th kyu (verifie sur une capture du jeu), nom « NO-NAME ».
O_PERSO = 0x11C
O_ARGENT = 0x120
O_VICTOIRES = 0x124
O_DEFAITES = 0x128
O_GRADE = 0x12C
O_NOM = 0x130
O_NOM_TAILLE = 16
O_CREE = 0x140
KYU = ['10th kyu', '9th kyu', '8th kyu', '7th kyu', '6th kyu',
       '5th kyu', '4th kyu', '3rd kyu', '2nd kyu', '1st kyu']
PERSOS = ['AKIRA', 'AOI', 'BRAD', 'GOH', 'JACKY', 'JEFFRY', 'KAGE', 'LAU',
          'LEI-FEI', 'LION', 'PAI', 'SARAH', 'SHUN', 'VANESSA', 'WOLF',
          'EL BLAZE', 'EILEEN', 'JEAN', 'TAKA-ARASHI']


def grade_nom(g):
    return KYU[g] if 0 <= g < 10 else 'dan %d' % (g - 9)
BITS = 128
RIVAUX = 1000


def neuf():
    d = bytearray(TAILLE)
    d[0:8] = MAGIE
    struct.pack_into('<I', d, O_VERSION, VERSION)
    return d


def lire():
    """Le profil, ou None s'il n'existe pas / n'est pas des notres."""
    if not os.path.exists(CHEMIN):
        return None
    d = bytearray(open(CHEMIN, 'rb').read())
    if len(d) != TAILLE or bytes(d[0:8]) != MAGIE:
        return None
    if len(d) == 0x120 and struct.unpack_from('<I', d, O_VERSION)[0] == 1:
        d = bytearray(d) + bytearray(TAILLE - 0x120)
        struct.pack_into('<I', d, O_VERSION, VERSION)
        struct.pack_into('<I', d, O_PERSO, 0xFFFFFFFF)
        return d
    if struct.unpack_from('<I', d, O_VERSION)[0] != VERSION:
        return None
    return d


def bits(d, champ):
    """Les numeros des rivaux dont le bit est mis."""
    return [n for n in range(RIVAUX)
            if (d[champ + (n >> 3)] >> (n & 7)) & 1]


def poser(d, champ, n, valeur=True):
    if valeur:
        d[champ + (n >> 3)] |= 1 << (n & 7)
    else:
        d[champ + (n >> 3)] &= ~(1 << (n & 7)) & 0xFF


def noms():
    """{numero: nom} depuis npc_tbl.bin, si la table est posee."""
    if not os.path.exists(NPC):
        return {}
    d = open(NPC, 'rb').read()
    out = {}
    for n in range(RIVAUX):
        o = struct.unpack_from('>I', d, n * 0x90)[0]
        if o and o < len(d):
            out[n] = d[o:d.index(b'\x00', o)].decode('utf-8', 'replace')
    return out


def afficher():
    d = lire()
    if d is None:
        print('  pas de profil (%s)' % CHEMIN)
        print('  il se cree tout seul a la premiere entree dans le Quest.')
        return 1
    renc = bits(d, O_RENCONTRE)
    batt = bits(d, O_BATTU)
    deux = [n for n in batt if n in set(renc)]
    if struct.unpack_from('<I', d, O_CREE)[0]:
        perso = struct.unpack_from('<I', d, O_PERSO)[0]
        nom = bytes(d[O_NOM:O_NOM + O_NOM_TAILLE]).split(b'\0')[0]
        w = struct.unpack_from('<I', d, O_VICTOIRES)[0]
        l = struct.unpack_from('<I', d, O_DEFAITES)[0]
        r = (100.0 * w / (w + l)) if (w + l) else 0.0
        print('  carriere : %s, %s, %s'
              % (nom.decode('ascii', 'replace'),
                 PERSOS[perso] if perso < len(PERSOS) else '?',
                 grade_nom(struct.unpack_from('<I', d, O_GRADE)[0])))
        print('  %d G   W:%d  L:%d   win ratio %.2f %%'
              % (struct.unpack_from('<I', d, O_ARGENT)[0], w, l, r))
    else:
        print('  carriere : AUCUNE DONNEE -- le jeu ouvrira son ecran de'
              ' creation')
    s = struct.unpack_from('<I', d, O_SECONDES)[0]
    print('  %s' % CHEMIN)
    print('  temps de jeu        : %u s  (%d:%02d:%02d)'
          % (s, s // 3600, (s // 60) % 60, s % 60))
    print('  combats             : %u'
          % struct.unpack_from('<I', d, O_COMBATS)[0])
    print('  plus longue serie   : %u'
          % struct.unpack_from('<I', d, O_SERIE)[0])
    print('  rivaux rencontres   : %d / %d' % (len(renc), RIVAUX))
    print('  rivaux battus       : %d / %d' % (len(batt), RIVAUX))
    print('  rencontres ET battus: %d  -> statut %.1f %%'
          % (len(deux), len(deux) * 0.001 * 100.0))
    nm = noms()
    if nm and deux:
        print('  les premiers battus : %s'
              % ', '.join(nm.get(n, '?') for n in deux[:8]))
    return 0


def battre(combien):
    d = lire() or neuf()
    nb = 0
    for n in range(RIVAUX):
        vise = n < combien
        poser(d, O_RENCONTRE, n, vise or ((d[O_RENCONTRE + (n >> 3)]
                                           >> (n & 7)) & 1) == 1)
        poser(d, O_BATTU, n, vise)
        if vise:
            nb += 1
    struct.pack_into('<I', d, O_COMBATS, nb)
    struct.pack_into('<I', d, O_SERIE, min(nb, 99))
    os.makedirs(JEU, exist_ok=True)
    open(CHEMIN, 'wb').write(bytes(d))
    print('  SONDE : %d rivaux marques battus (et rencontres).' % nb)
    print('  le statut doit afficher %.1f %% sur sa premiere ligne.'
          % (nb * 0.001 * 100.0))
    print('  `--battre 0` les remet a zero ; `--effacer` supprime le profil.')


def main():
    a = sys.argv[1:]
    if '--effacer' in a:
        if os.path.exists(CHEMIN):
            os.remove(CHEMIN)
            print('  profil supprime ; il se recreera vide.')
        else:
            print('  il n y avait pas de profil.')
        return 0
    if '--battre' in a:
        i = a.index('--battre') + 1
        n = int(a[i]) if i < len(a) and a[i].lstrip('-').isdigit() else 0
        battre(max(0, min(RIVAUX, n)))
        return 0
    if '--lire' in a or not a:
        return afficher()
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
