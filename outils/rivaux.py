#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""LES MILLE RIVAUX DU MODE QUEST : poser `npc_tbl.bin` dans Final Showdown.

POURQUOI UN FICHIER, ET PAS DES CHAINES. Les libelles du Quest sont partis
dans `string_array.farc` (voir `textes_quest.py`) parce que ce sont des
libelles : le moteur de FS les resout par leur numero. Les rivaux, non. Un
rival n'est pas une chaine : c'est un enregistrement de 0x90 octets qui porte
son nom, sa replique en deux lignes, SON PERSONNAGE, et les reglages de son
IA. L'etape 4 -- se battre contre un rival -- en aura besoin en entier. On
pose donc le fichier tel quel, et `apm.dll` le lit.

CE QUE FINAL SHOWDOWN EN A : RIEN. `npc_tbl` n'existe ni dans son `.par` ni
dans `vf5fs_media/` -- les rivaux sont partis avec le mode. La place est donc
libre, et poser le fichier ne masque rien, ne deplace rien, n'ecrase rien.
C'est le cas le plus simple qu'on ait rencontre dans ce portage.

LA DISPOSITION, MESUREE LE 2026-09-27 (et lue dans `FUN_8230DDF0`, qui recopie
l'enregistrement dans l'objet du rival) :

    1000 enregistrements de 0x90 octets, puis le reservoir de chaines
    l'enregistrement n vit en n * 0x90 ; au-dela de 999, le jeu prend
    `n % 1000` (`FUN_8230DDF0`)

    +0x00  u32  offset ABSOLU du NOM            (10 caracteres au plus)
    +0x04  u32  offset de la replique, ligne 1
    +0x08  u32  offset de la replique, ligne 2
    +0x14  u8   LE PERSONNAGE, 0..16 -- dix-sept valeurs, ~59 rivaux chacune
    +0x15  u8   0..3      +0x16  u8  0..3
    +0x18  24 x u16 puis 24 x u16   la tenue (deux jeux)
    +0x78  u32  (& 0x3FF lu par le jeu ; nul dans la table)
    +0x88  u8   0..7      +0x89  u8  0..4     +0x8A  u8  1..4   l'IA
    +0x8C  u16

Les entiers sont GROS-BOUTISTES (Xbox 360) et les chaines de l'UTF-8. Le
fichier de la RACINE du media est le japonais ; ce sont les `lang/<lg>/` qui
portent les traductions -- et Frederic a demande l'anglais.

    py -3 tools/rivaux.py --ajouter            pose la table (anglais)
    py -3 tools/rivaux.py --ajouter --langue fr
    py -3 tools/rivaux.py --controle
    py -3 tools/rivaux.py --retirer
    py -3 tools/rivaux.py --lister 0 12        affiche douze rivaux
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)

# Le media du VF5 de 2007. Deux copies existent sur le Bureau, a l'octet pres
# (mesure du 2026-09-27) : on prend la premiere qui repond, pour qu'effacer
# l'autre ne casse rien. Voir `analysis/dlc_objets.md`.
BUREAU = os.path.join('C:' + os.sep, 'Users', 'frede', 'Desktop')
SOURCES = (
    os.path.join(BUREAU, 'VF5 FS DECOMP', 'X360_VF5', 'media'),
    os.path.join(BUREAU, 'SEPTEMBRE', 'VF5 CUSTOM DLC',
                 'Virtua Fight3r 5 AnDreXplay', 'Virtua Fighter 5', 'media'),
)
ROM = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media', 'rom')
CIBLE = os.path.join(ROM, 'npc_tbl.bin')
PAR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_data.par')

NOMBRE = 1000
PAS = 0x90
O_NOM = 0x00
O_DIT1 = 0x04
O_DIT2 = 0x08
O_PERSO = 0x14


class Refus(Exception):
    pass


def source(langue):
    """Le `npc_tbl.bin` de la langue demandee, ou un refus qui DIT ou l'on a
    cherche."""
    essayes = []
    for m in SOURCES:
        p = os.path.join(m, 'lang', langue, 'npc_tbl.bin')
        essayes.append(p)
        if os.path.exists(p):
            return p
    raise Refus('table des rivaux introuvable ; cherche dans :%s%s'
                % (os.linesep,
                   os.linesep.join('    ' + p for p in essayes)))


def lire(octets):
    """{numero: (nom, ligne 1, ligne 2, personnage)} -- la table, decodee."""
    if len(octets) < NOMBRE * PAS:
        raise Refus('%d octets : il en faut au moins %d pour mille '
                    'enregistrements' % (len(octets), NOMBRE * PAS))

    def chaine(o):
        if o == 0 or o >= len(octets):
            return ''
        f = octets.index(b'\x00', o)
        return octets[o:f].decode('utf-8', 'replace')

    out = {}
    for n in range(NOMBRE):
        b = n * PAS
        nom, d1, d2 = struct.unpack_from('>III', octets, b + O_NOM)
        out[n] = (chaine(nom), chaine(d1), chaine(d2), octets[b + O_PERSO])
    return out


def controle():
    """Liste des defauts ; vide si la table est en place et coherente."""
    fautes = []
    if not os.path.exists(CIBLE):
        return ['npc_tbl.bin absent de vf5fs_media/rom']
    d = open(CIBLE, 'rb').read()
    try:
        table = lire(d)
    except Refus as e:
        return [str(e)]
    vides = [n for n, v in table.items() if not v[0]]
    if vides:
        fautes.append('%d rivaux sans nom (le premier : %d)'
                      % (len(vides), vides[0]))
    persos = set(v[3] for v in table.values())
    if not persos <= set(range(17)):
        fautes.append('personnages hors 0..16 : %s'
                      % sorted(persos - set(range(17))))
    return fautes


def ajouter(langue='en', verbeux=True):
    src = source(langue)
    d = open(src, 'rb').read()
    table = lire(d)                       # il doit se lire avant d'etre pose
    os.makedirs(ROM, exist_ok=True)
    with open(CIBLE, 'wb') as fp:
        fp.write(d)
    if verbeux:
        print('  %s -> %s' % (src, CIBLE))
        print('  %d rivaux, %d octets, langue %s'
              % (len(table), len(d), langue))
        print('  exemples : %s'
              % ', '.join(table[n][0] for n in range(4)))
    return len(table)


def retirer(verbeux=True):
    if os.path.exists(CIBLE):
        os.remove(CIBLE)
        if verbeux:
            print('  npc_tbl.bin retire de vf5fs_media/rom')
    elif verbeux:
        print('  npc_tbl.bin n y etait pas')


def lister(debut, combien, langue='en'):
    p = CIBLE if os.path.exists(CIBLE) else source(langue)
    table = lire(open(p, 'rb').read())
    print('%s' % p)
    for n in range(debut, min(debut + combien, NOMBRE)):
        nom, d1, d2, perso = table[n]
        dit = (d1 + ' ' + d2).strip()
        print('  %4d  perso %2d  %-12s  %s'
              % (n, perso, nom,
                 dit.encode('ascii', 'replace').decode('ascii')))


def main():
    a = sys.argv[1:]
    langue = a[a.index('--langue') + 1] if '--langue' in a else 'en'
    try:
        if '--ajouter' in a:
            ajouter(langue)
            print('  IL FAUT ENCORE : recompiler apm.dll '
                  '(tools/gen_apm_stub.py) -- c est elle qui lit la table.')
            return 0
        if '--retirer' in a:
            retirer()
            return 0
        if '--lister' in a:
            i = a.index('--lister')
            deb = int(a[i + 1]) if len(a) > i + 1 and a[i + 1].isdigit() else 0
            n = int(a[i + 2]) if len(a) > i + 2 and a[i + 2].isdigit() else 12
            lister(deb, n, langue)
            return 0
        if '--controle' in a:
            fautes = controle()
            if fautes:
                for f in fautes:
                    print('  DEFAUT : %s' % f)
                return 1
            print('  table des rivaux : CONFORME (1000 rivaux)')
            return 0
    except Refus as e:
        print('REFUS : %s' % e)
        return 2
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
