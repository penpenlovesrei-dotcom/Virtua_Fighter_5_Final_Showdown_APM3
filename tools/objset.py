#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Lit un `*_obj.bin` (jeu d'objets SEGA, magie 0x05062500) et rend ses NOMS.

Pourquoi cet outil : identifier un decor par un balayage d'ASCII rend du bruit
(19 298 faux noms sur `stgdur_obj.bin`, essai du 2026-09-07). Les noms sont
dans une table, pas dans le tas : il faut la lire.

En-tete, 0x40 octets, tout en petit-boutiste :

    +0x00  u32  magie 0x05062500
    +0x04  u32  NOMBRE d'objets
    +0x08  u32  plus grand identifiant d'objet
    +0x0C  u32  offset de la table des objets      (0x40)
    +0x10  u32  fin de la zone des identifiants de texture
    +0x14  u32  offset de la TABLE DES NOMS        (nombre x u32 -> chaines)
    +0x18  u32  offset de la table des IDENTIFIANTS (nombre x u32)
    +0x1C  u32  offset des identifiants de texture
    +0x20  u32  NOMBRE de textures

Usage :

    py -3 tools/objset.py <fichier_obj.bin> [...]      la liste des noms
    py -3 tools/objset.py --entete <fichier>           l'en-tete seule
    py -3 tools/objset.py --grep motif <fichier> [...] filtre insensible
"""
import os
import struct
import sys


class Objset(object):
    def __init__(self, chemin):
        self.chemin = chemin
        d = open(chemin, 'rb').read()
        self.brut = d
        magie, = struct.unpack_from('<I', d, 0)
        if magie != 0x05062500:
            raise ValueError('%s : magie 0x%08X inattendue' % (chemin, magie))
        (self.nombre, self.id_max, self.off_objets, self.fin_tex,
         self.off_noms, self.off_ids, self.off_tex, self.nb_tex) = \
            struct.unpack_from('<8I', d, 4)

    def noms(self):
        d = self.brut
        sortie = []
        for i in range(self.nombre):
            po, = struct.unpack_from('<I', d, self.off_noms + i * 4)
            fin = d.find(b'\x00', po)
            sortie.append(d[po:fin].decode('ascii', 'replace'))
        return sortie

    def ids(self):
        return list(struct.unpack_from('<%dI' % self.nombre,
                                       self.brut, self.off_ids))


def main():
    argv = sys.argv[1:]
    motif = None
    if '--grep' in argv:
        i = argv.index('--grep')
        motif = argv[i + 1].lower()
        del argv[i:i + 2]
    entete_seule = '--entete' in argv
    argv = [a for a in argv if not a.startswith('--')]
    if not argv:
        print(__doc__)
        return 1
    for chemin in argv:
        o = Objset(chemin)
        print('=== %s' % os.path.basename(chemin))
        print('    %d objets, id max %d, %d textures'
              % (o.nombre, o.id_max, o.nb_tex))
        if entete_seule:
            continue
        noms = o.noms()
        ids = o.ids()
        for n, (nom, ident) in enumerate(zip(noms, ids)):
            if motif and motif not in nom.lower():
                continue
            print('    %3d  id %5d  %s' % (n, ident, nom))
    return 0


if __name__ == '__main__':
    sys.exit(main())
