#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Inventaire d'un `vf5fs_data.par`, sans rien extraire.

Le format PARC de ce jeu, mesure le 2026-09-08 sur l'archive APM3 :

    +0x00  'PARC'
    +0x10  nombre de DOSSIERS      +0x14  offset de leur table
    +0x18  nombre de FICHIERS      +0x1C  offset de leur table
    tout en GROS-BOUTIEN.

    Les NOMS sont un tableau a PAS FIXE qui commence en 0x20 : les dossiers
    d'abord, puis les fichiers. Le pas se deduit --
    (min(table_dossiers, table_fichiers) - 0x20) / (n_dossiers + n_fichiers).

    Une entree de fichier fait 0x20 octets : drapeaux, taille, taille
    comprimee, offset ; 0x80000000 dans les drapeaux = comprime (SLLZ).

    py -3 tools/par_inventaire.py <archive.par>
    py -3 tools/par_inventaire.py <archive.par> --grep "^stg"
    py -3 tools/par_inventaire.py <a.par> --contre <b.par>
"""
import os
import re
import struct
import sys


def lire(chemin):
    """Rend [(nom, taille, comprime, offset), ...] et la liste des dossiers."""
    fp = open(chemin, 'rb')
    tete = fp.read(0x40)
    if tete[:4] != b'PARC':
        raise SystemExit('%s : ce n\'est pas une archive PARC' % chemin)
    n_dos, off_dos, n_fic, off_fic = struct.unpack('>IIII', tete[0x10:0x20])
    pas = (min(off_dos, off_fic) - 0x20) // (n_dos + n_fic)
    fp.seek(0x20)
    brut = fp.read((n_dos + n_fic) * pas)
    noms = [brut[i * pas:i * pas + pas].split(b'\x00')[0]
            .decode('ascii', 'replace') for i in range(n_dos + n_fic)]
    fp.seek(off_fic)
    ent = fp.read(n_fic * 0x20)
    fp.close()
    fichiers = []
    for i in range(n_fic):
        dr, taille, comp, offset = struct.unpack_from('>IIII', ent, i * 0x20)
        fichiers.append((noms[n_dos + i], taille, comp, offset,
                         bool(dr & 0x80000000)))
    return noms[:n_dos], fichiers


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    chemin = argv[0]
    motif = None
    if '--grep' in argv:
        motif = re.compile(argv[argv.index('--grep') + 1], re.I)
    contre = argv[argv.index('--contre') + 1] if '--contre' in argv else None

    dossiers, fichiers = lire(chemin)
    print('%s' % os.path.basename(chemin))
    print('   %d dossiers, %d fichiers, %.2f Go d\'archive'
          % (len(dossiers), len(fichiers), os.path.getsize(chemin) / 2**30))

    if contre:
        d2, f2 = lire(contre)
        a = {n for n, _, _, _, _ in fichiers}
        b = {n for n, _, _, _, _ in f2}
        ta = {n: t for n, t, _, _, _ in fichiers}
        tb = {n: t for n, t, _, _, _ in f2}
        print('%s' % os.path.basename(contre))
        print('   %d dossiers, %d fichiers, %.2f Go'
              % (len(d2), len(f2), os.path.getsize(contre) / 2**30))
        print()
        print('communs %d   seulement A %d   seulement B %d'
              % (len(a & b), len(a - b), len(b - a)))
        differents = sorted(n for n in a & b if ta[n] != tb[n])
        print('communs mais de TAILLE DIFFERENTE : %d' % len(differents))
        if motif:
            for titre, jeu in (('SEULEMENT DANS A', sorted(a - b)),
                               ('SEULEMENT DANS B', sorted(b - a))):
                choix = [n for n in jeu if motif.search(n)]
                print('\n--- %s (%d sur %d) ---' % (titre, len(choix), len(jeu)))
                for n in choix[:60]:
                    print('   %-32s' % n)
            choix = [n for n in differents if motif.search(n)]
            print('\n--- TAILLES DIFFERENTES (%d) ---' % len(choix))
            for n in choix[:60]:
                print('   %-32s A %10d   B %10d' % (n, ta[n], tb[n]))
        return 0

    if motif:
        choix = [f for f in fichiers if motif.search(f[0])]
        print('\n%d fichiers retenus :' % len(choix))
        for n, t, c, o, z in sorted(choix):
            print('   %-32s %10d o%s' % (n, t, '   (comprime)' if z else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
