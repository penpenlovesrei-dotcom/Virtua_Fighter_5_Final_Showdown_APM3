#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Masque une entree dans l'index de `vf5fs_data.par`, pour que le moteur
retombe sur le fichier libre de `vf5fs_media/`.

Pourquoi : le moteur consulte **d'abord** l'archive `PARC`. Ce qui s'y trouve
est lu depuis l'archive et le disque n'est jamais interroge -- mesure faite au
point d'arret sur `CreateFileW` (`analysis/import_decors.md`). Deposer un
fichier a cote ne sert donc a rien tant que son nom est dans l'index.

Le remede le moins invasif : **changer un seul octet du nom dans l'index**.
`stgdjo.farc` devient `stgdjo.far_`, le moteur ne le trouve plus, et il retombe
sur l'arborescence libre. Aucun deplacement de donnees, aucune reconstruction de
4 Go, et l'operation se defait en remettant l'octet d'origine.

SECURITE. Le `.par` de l'atelier est un **lien dur** vers celui du dump, qui est
en lecture seule par regle du projet : ecrire dedans ecrirait dans le dump.
L'outil REFUSE donc d'ecrire dans un fichier dont le compteur de liens est
superieur a 1.

Usage :
    py -3 tools/par_masquer.py --lister stgdjo.farc
    py -3 tools/par_masquer.py --masquer stgdjo.farc djo.ibl fog_djo.txt
    py -3 tools/par_masquer.py --rendre  stgdjo.farc
"""
import mmap
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
PAR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_data.par')
MASQUE = ord('_')


def liens(chemin):
    """Le nombre de liens durs. > 1 = le fichier est partage avec le dump."""
    try:
        return os.stat(chemin).st_nlink
    except OSError:
        return 0


def fin_du_pot(m):
    """Fin du pot de noms de l'en-tete PARC -- au-dela, ce sont des DONNEES.

    En-tete gros-boutiste : `+0x10` nombre de dossiers, `+0x14` offset de leur
    table, `+0x18` nombre de fichiers, `+0x1C` offset de leur table. Les noms
    occupent `0x20` jusqu'a la premiere de ces deux tables.

    Sans cette borne l'outil masquerait aussi les occurrences situees DANS les
    fichiers archives : `STGDJO_COLI.000.bin` en a trois, dont deux vers
    0xEDD000 -- a 15 Mo, donc au coeur des donnees. Les ecraser corromprait un
    fichier au lieu de cacher un nom.
    """
    if m[:4] != b'PARC':
        return len(m)
    off_dos, off_fic = struct.unpack('>I', m[0x14:0x18])[0], \
        struct.unpack('>I', m[0x1C:0x20])[0]
    return min(off_dos, off_fic)


def positions(m, nom, borne=None):
    """Occurrences du nom suivies d'un zero, DANS le pot de noms seulement.

    LA BORNE EST PASSEE A `find`, ET CE N'EST PAS UN DETAIL DE STYLE.

    La version qui cherchait dans tout le fichier et s'arretait APRES coup
    (`if i >= borne: break`) balayait quand meme les 3,99 Go : une fois la
    derniere occurrence du pot trouvee, le `find` suivant lisait l'archive
    entiere pour conclure « plus rien ». Environ deux secondes par recherche,
    deux recherches par nom (le clair et le masque), neuf noms par decor --
    **16 secondes par appel**, et `decor_5r_akira.cmd` en fait trois avant de
    demarrer, dont deux qui n'ont rien a retirer. Mesure du 2026-09-10.

    En donnant `borne` a `find`, la recherche s'arrete a 0x1D640 octets. Et
    c'est aussi plus juste : on ne regarde plus jamais dans les DONNEES, ou
    `STGDJO_COLI.000.bin` a deux occurrences vers 0xEDD000.
    """
    if borne is None:
        borne = fin_du_pot(m)
    cible = nom.encode()
    out, i = [], m.find(cible, 0, borne)
    while i >= 0:
        if m[i + len(cible):i + len(cible) + 1] == b'\x00':
            out.append(i)
        i = m.find(cible, i + 1, borne)
    return out


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    par = PAR
    if '--par' in argv:
        par = argv[argv.index('--par') + 1]
        argv = [a for j, a in enumerate(argv)
                if j not in (argv.index('--par'), argv.index('--par') + 1)]
    if not os.path.exists(par):
        print('archive introuvable : %s' % par)
        return 1

    action = None
    for a in ('--lister', '--masquer', '--rendre'):
        if a in argv:
            action = a
            noms = argv[argv.index(a) + 1:]
            break
    if action is None:
        print(__doc__)
        return 1
    noms = [n for n in noms if not n.startswith('--')]
    if not noms:
        print('aucun nom donne')
        return 1

    n = liens(par)
    print('archive : %s' % par)
    print('liens durs : %d%s' % (n, '' if n <= 1 else '   <-- PARTAGE AVEC LE DUMP'))
    if action != '--lister' and n > 1:
        print('\nREFUS : ce fichier est un lien dur vers le dump en lecture seule.')
        print('        Cassez le lien par une vraie copie avant de le modifier :')
        print('        cp vf5fs_data.par vf5fs_data.par.copie')
        return 2

    mode = 'r+b' if action != '--lister' else 'rb'
    acces = mmap.ACCESS_WRITE if action != '--lister' else mmap.ACCESS_READ
    with open(par, mode) as fp:
        m = mmap.mmap(fp.fileno(), 0, access=acces)
        try:
            for nom in noms:
                masque = nom[:-1] + chr(MASQUE)
                pos_clair = positions(m, nom)
                pos_masque = positions(m, masque)
                print('\n%s' % nom)
                print('   visible : %s' % (['0x%X' % p for p in pos_clair] or 'aucune'))
                print('   masque  : %s' % (['0x%X' % p for p in pos_masque] or 'aucune'))
                if action == '--masquer':
                    for p in pos_clair:
                        m[p + len(nom) - 1] = MASQUE
                    if pos_clair:
                        print('   -> %d entree(s) masquee(s) en « %s »'
                              % (len(pos_clair), masque))
                elif action == '--rendre':
                    for p in pos_masque:
                        m[p + len(nom) - 1] = ord(nom[-1])
                    if pos_masque:
                        print('   -> %d entree(s) rendue(s) en « %s »'
                              % (len(pos_masque), nom))
            if action != '--lister':
                m.flush()
        finally:
            m.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
