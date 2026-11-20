#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SLLZ : le compresseur des archives PAR, et le lecteur d'index PARC.

Pourquoi il a fallu l'ecrire. `vf5fs_data.par` fait 4 Go et `ParTool.exe` ne
sait extraire QUE l'archive entiere -- pas un fichier. Pour comparer une seule
planche (`aet_s_selcha.bin`, la grille de selection) entre la borne et la PS3,
extraire 4 Go etait absurde. On lit donc l'index et on decompresse le seul bloc
voulu.

L'index PARC est **gros-boutiste** :

    0x00  "PARC"          magie
    0x04  version
    0x10  nb repertoires  (u32 BE)
    0x14  offset des repertoires
    0x18  nb fichiers     (u32 BE)
    0x1C  offset des fichiers

et la table de noms occupe 0x20, a raison de **64 octets par entree**, les
repertoires d'abord puis les fichiers -- ce que confirme l'arithmetique :
(19 + 1862) * 64 + 0x20 = 0x1D660, exactement l'offset des repertoires.

Chaque entree de fichier fait 32 octets, gros-boutiste :

    +0x00  drapeaux   (0x80000000 = compresse SLLZ)
    +0x04  taille decompressee
    +0x08  taille compressee
    +0x0C  offset dans l'archive

Le bloc compresse porte son propre en-tete SLLZ, celui-ci **petit-boutiste** :

    0x00  "SLLZ"
    0x04  version (1)
    0x05  taille d'en-tete (0x10)
    0x08  taille decompressee
    0x0C  taille compressee

puis un flux LZSS classique : un octet de drapeaux commande huit elements,
bit a 1 = litteral, bit a 0 = paire (offset sur 12 bits, longueur sur 4).

Usage :
    py -3 tools/sllz.py lister  <par> [motif]
    py -3 tools/sllz.py sortir  <par> <nom> <destination>
"""
import mmap
import os
import struct
import sys


def decompresser(bloc):
    """SLLZ version 1.

    Algorithme repris de ParManager (Kaplas80), `ParLibrary/Sllz/Decompressor.cs`,
    sous licence MIT -- lu, pas execute. Deux details s'y jouent, et les deviner
    a coute une heure le 2026-09-04 :

      * les bits du drapeau se lisent de **poids fort** d'abord, et un bit a 1
        commande une PAIRE ;
      * le drapeau est decale, et rechargé s'il est epuise, **AVANT** que les
        octets de l'element soient lus -- pas apres. C'est ce decalage d'un cran
        qui donnait l'impression que le premier groupe ne couvrait que sept
        elements.

    La paire est un mot de 16 bits petit-boutiste :
        distance = 1 + (v >> 4)      longueur = 3 + (v & 0xF)
    d'ou une fenetre de 4096 octets et des longueurs de 3 a 18.
    """
    if bloc[:4] != b'SLLZ':
        raise ValueError('ce n est pas du SLLZ')
    boutisme = bloc[4]
    version = bloc[5]
    if boutisme != 0:
        raise ValueError('SLLZ gros-boutiste non gere')
    if version != 1:
        raise ValueError('SLLZ version %d non geree (la 2 est du zlib par blocs)'
                         % version)
    entete = struct.unpack_from('<H', bloc, 6)[0]
    taille = struct.unpack_from('<i', bloc, 8)[0]
    comp = struct.unpack_from('<i', bloc, 12)[0]
    data = bloc[entete: entete + (comp - 0x10)]

    out = bytearray(taille)
    ip = 0
    op = 0
    drapeau = data[ip]
    ip += 1
    reste = 8
    while op < taille:
        paire = drapeau & 0x80
        drapeau = (drapeau << 1) & 0xFF
        reste -= 1
        if reste == 0:
            drapeau = data[ip]
            ip += 1
            reste = 8
        if paire:
            v = data[ip] | (data[ip + 1] << 8)
            ip += 2
            distance = 1 + (v >> 4)
            longueur = 3 + (v & 0xF)
            for _ in range(longueur):
                out[op] = out[op - distance]
                op += 1
        else:
            out[op] = data[ip]
            ip += 1
            op += 1
    return bytes(out)


class Par:
    def __init__(self, chemin):
        self.chemin = chemin
        self.fp = open(chemin, 'rb')
        self.m = mmap.mmap(self.fp.fileno(), 0, access=mmap.ACCESS_READ)
        if self.m[:4] != b'PARC':
            raise ValueError('ce n est pas une archive PARC')
        self.ndir, self.odir, self.nfic, self.ofic = struct.unpack(
            '>IIII', self.m[0x10:0x20])

    def nom(self, i):
        b = self.m[0x20 + 64 * i: 0x20 + 64 * i + 64]
        return b.split(b'\x00', 1)[0].decode('latin-1')

    def entrees(self):
        for k in range(self.nfic):
            e = self.m[self.ofic + 32 * k: self.ofic + 32 * k + 32]
            drapeaux, taille, comp, offset = struct.unpack('>4I', e[:16])
            yield k, self.nom(self.ndir + k), drapeaux, taille, comp, offset

    def sortir(self, nom_cible):
        for k, n, drapeaux, taille, comp, offset in self.entrees():
            if n != nom_cible:
                continue
            if drapeaux & 0x80000000:
                bloc = self.m[offset: offset + comp]
                d = decompresser(bloc)
                if len(d) != taille:
                    raise ValueError('taille obtenue %d, attendue %d'
                                     % (len(d), taille))
                return d
            return bytes(self.m[offset: offset + taille])
        raise KeyError(nom_cible)


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    cmd = argv[0]
    if cmd == 'lister':
        p = Par(argv[1])
        motif = argv[2].lower() if len(argv) > 2 else ''
        n = 0
        for k, nom, dr, taille, comp, off in p.entrees():
            if motif and motif not in nom.lower():
                continue
            n += 1
            print('  %-34s %9d o  %s  offset 0x%X'
                  % (nom, taille,
                     'compresse %7d' % comp if dr & 0x80000000 else 'brut'.ljust(17),
                     off))
        print('%d entree(s)' % n)
        return 0
    if cmd == 'sortir':
        p = Par(argv[1])
        d = p.sortir(argv[2])
        with open(argv[3], 'wb') as fp:
            fp.write(d)
        print('%s : %d octets -> %s' % (argv[2], len(d), argv[3]))
        return 0
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
