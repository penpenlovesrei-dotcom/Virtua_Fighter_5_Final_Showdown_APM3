#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""LES BRUITAGES DE L'INTERFACE APM3 -- extraction.

A NE PAS CONFONDRE avec `tools/apm_sons.py`, qui sort les 19 jingles du
systeme de paiement (nanaco, Rakuten Edy, iD, WAON, PASELI, cartes de
transport). Ceux-la ne sont PAS les sons de l'interface : ils appartiennent au
terminal Thinca, et je m'y etais trompe.

Les vrais bruitages de l'ecran de choix sont dans
`Apmv3System_Data/resources.resource`, en QUATRE banques FSB5, codees en
Vorbis. Aucune chaine ne les nomme : dans un build de sortie, Unity n'ecrit
pas les noms de type, et ces banques n'ont pas de table de noms. On les
numerote donc dans l'ordre du fichier.

CE QU'IL FAUT POUR LES DECODER, et pourquoi ce n'est pas evident : le Vorbis
d'une banque FSB5 est ampute de ses en-tetes, qu'il faut reconstruire a partir
d'un identifiant de livre de codes. C'est le travail de `python-fsb5`, qui
s'appuie sur libvorbis. Les trois DLL sont deja sur cette machine, dans le
MSYS2 -- mais ctypes ne les trouve pas tout seul, d'ou la redirection ci-dessous.

    py -3 -m pip install fsb5          (une fois)
    py -3 tools/apm_ui_sons.py
"""
import ctypes.util
import os
import struct
import sys

BIN = os.path.join('C:' + os.sep, 'msys64', 'mingw64', 'bin')
DLL = {
    'vorbis': os.path.join(BIN, 'libvorbis-0.dll'),
    'vorbisenc': os.path.join(BIN, 'libvorbisenc-2.dll'),
    'ogg': os.path.join(BIN, 'libogg-0.dll'),
}

SOURCE = os.path.join('C:' + os.sep, 'Users', 'frede', 'Desktop',
                      'VF5 FS DECOMP', 'APM_V1.04_internal_0',
                      'Apmv3System_Data', 'resources.resource')
ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(ICI, 'extracted', 'apm_ui_sons')


def preparer():
    """Fait pointer ctypes sur les libvorbis du MSYS2."""
    manquantes = [n for n, p in DLL.items() if not os.path.exists(p)]
    if manquantes:
        print('INTROUVABLE dans %s : %s' % (BIN, ', '.join(manquantes)))
        return False
    os.add_dll_directory(BIN)
    vrai = ctypes.util.find_library
    ctypes.util.find_library = lambda n: DLL.get(n, vrai(n))
    return True


def banques(donnees):
    """Rend (offset, taille, nb_sons) pour chaque FSB5 du fichier."""
    trouvees = []
    i = 0
    while True:
        j = donnees.find(b'FSB5', i)
        if j < 0:
            break
        if j + 28 > len(donnees):
            break
        ver, nsamp, hsize, nsize, dsize, mode = struct.unpack(
            '<IIIIII', donnees[j + 4:j + 28])
        if nsamp == 0 or nsamp > 4096:
            i = j + 4
            continue
        base = 60 if ver == 1 else 64
        total = base + hsize + nsize + dsize
        trouvees.append((j, total, nsamp))
        i = j + total
    return trouvees


def main():
    if not os.path.exists(SOURCE):
        print('INTROUVABLE : %s' % SOURCE)
        return 1
    if not preparer():
        return 1
    try:
        import fsb5
    except ImportError:
        print('Le module fsb5 manque.  py -3 -m pip install fsb5')
        return 1

    donnees = open(SOURCE, 'rb').read()
    trouvees = banques(donnees)
    print('=' * 68)
    print('BRUITAGES DE L INTERFACE APM3')
    print('=' * 68)
    print('  source : %s' % SOURCE)
    print('  %d banque(s) FSB5' % len(trouvees))
    print()

    os.makedirs(SORTIE, exist_ok=True)
    ecrits = 0
    for numero, (offset, taille, _) in enumerate(trouvees, 1):
        try:
            banque = fsb5.FSB5(donnees[offset:offset + taille])
            for son in banque.samples:
                nom = 'son%d.%s' % (numero, banque.get_sample_extension())
                brut = banque.rebuild_sample(son)
                open(os.path.join(SORTIE, nom), 'wb').write(brut)
                print('  %-10s %d voie(s)  %d Hz  %.3f s  %d octets'
                      % (nom, son.channels, son.frequency,
                         son.samples / float(son.frequency), len(brut)))
                ecrits += 1
        except Exception as e:                      # une banque abimee
            print('  banque %d : %s' % (numero, e))

    print()
    print('  %d fichier(s) dans %s' % (ecrits, SORTIE))
    if ecrits != len(trouvees):
        print('  ATTENTION : %d banque(s) sur %d seulement.'
              % (ecrits, len(trouvees)))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
