#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Ecrit un fichier DANS le `.par`, en l'ajoutant a la fin et en repointant son
entree d'index.

POURQUOI IL FAUT EN VENIR LA (mesure du 2026-09-10)

Masquer un nom dans l'index suffit pour la plupart des fichiers : le moteur ne le
trouve plus dans l'archive et retombe sur `vf5fs_media/`. C'est ce qui marche
pour `auth_3d_db.bin` -- `tracer_fichiers.py` le voit s'ouvrir sur le disque.

**Mais pas pour `obj_db.bin`.** Son chargeur (`0x1800F97E0`) compose bien
`./rom/objset/obj_db.bin`, et il recoit les octets **de l'archive**, masquage ou
pas : essaye en changeant le dernier caractere du nom (`obj_db.bi_`), puis le
premier (`Xbj_db.bin`), et en retirant le fichier pose -- le vecteur d'objsets
du moteur garde ses 6044 entrees d'origine, et notre objset 6150 reste
introuvable. Les entrees de l'index ne portent aucun hachage de nom, donc ce
n'est pas le masquage qui echoue : c'est ce chargeur-la qui resout dans
l'archive d'abord. Voir `REPRISE.md` (42).

Il faut donc mettre nos octets DANS le `.par`.

COMMENT, ET POURQUOI C'EST SANS DANGER POUR L'ORIGINAL

    en-tete PARC (gros-boutien)  +0x10 n_dossiers  +0x14 table des dossiers
                                 +0x18 n_fichiers  +0x1C table des fichiers
    noms      tableau a PAS FIXE des 0x20, dossiers puis fichiers
    entree    0x20 octets : drapeaux, taille, taille comprimee, offset,
              trois zeros, un horodatage

`0x80000000` dans les drapeaux = comprime (SLLZ). Un membre NON comprime a
`drapeaux = 0` et `taille == taille comprimee` (verifie sur `stgdjo.farc`,
`mot_db.farc`, `se_stage_djo.acb`).

On n'ecrase donc RIEN : les octets d'origine du membre restent ou ils sont, on
ajoute les nouveaux **a la fin de l'archive** et on ne change que les 32 octets
de son entree d'index. `--rendre` remet ces 32 octets, et l'archive redevient
exactement ce qu'elle etait a l'octet pres (elle garde juste une queue inerte
que plus rien ne pointe).

L'entree d'origine est gardee dans `analysis/par_entrees_origine.json`. Sans ce
fichier, `--rendre` refuse : il ne devinera pas un offset.

LES TROIS REFUS

  . **liens durs** : `vf5fs_data.par` du dump est en lecture seule et notre
    copie a longtemps ete un LIEN DUR vers lui. Ecrire dedans ecrirait dans le
    dump. On refuse si le fichier a plus d'un lien ;
  . **offset sur 32 bits** : l'offset est un dword. On refuse si la fin de
    l'archive plus les octets depasse 4 Go ;
  . **taille sur 32 bits** aussi, pour la meme raison.

    py -3 tools/par_ecrire.py --etat obj_db.bin
    py -3 tools/par_ecrire.py --remplacer obj_db.bin --par <fichier>
    py -3 tools/par_ecrire.py --rendre obj_db.bin
"""
import json
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import par_masquer                                             # noqa: E402

PAR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_data.par')
MEMOIRE = os.path.join(RACINE, 'analysis', 'par_entrees_origine.json')
ALIGNEMENT = 0x800
LIMITE = 0x100000000


def index(fp):
    """Rend (n_dos, off_dos, n_fic, off_fic, pas, noms, entrees)."""
    fp.seek(0)
    tete = fp.read(0x40)
    if tete[:4] != b'PARC':
        raise SystemExit('ce n\'est pas une archive PARC')
    n_dos, off_dos, n_fic, off_fic = struct.unpack('>IIII', tete[0x10:0x20])
    pas = (min(off_dos, off_fic) - 0x20) // (n_dos + n_fic)
    fp.seek(0x20)
    noms = fp.read((n_dos + n_fic) * pas)
    fp.seek(off_fic)
    entrees = fp.read(n_fic * 0x20)
    return n_dos, off_dos, n_fic, off_fic, pas, noms, entrees


def rang_de(noms, pas, n_dos, n_fic, nom):
    for k in range(n_fic):
        i = (n_dos + k) * pas
        if noms[i:i + pas].split(b'\x00')[0].decode('latin-1') == nom:
            return k
    return None


def dire_entree(etiquette, brut):
    f, taille, comp, off, _, _, _, ts = struct.unpack('>8I', brut)
    print('   %-10s drapeaux %08X  taille %10d  comprimee %10d  offset 0x%X%s'
          % (etiquette, f, taille, comp, off,
             '  (SLLZ)' if f & 0x80000000 else ''))


def memoire_lire():
    if os.path.exists(MEMOIRE):
        with open(MEMOIRE, 'r', encoding='ascii') as fp:
            return json.load(fp)
    return {}


def memoire_ecrire(m):
    os.makedirs(os.path.dirname(MEMOIRE), exist_ok=True)
    with open(MEMOIRE, 'w', encoding='ascii') as fp:
        json.dump(m, fp, indent=2, sort_keys=True)


def controler_liens():
    n = par_masquer.liens(PAR)
    print('liens durs : %s' % n)
    if n and n > 1:
        print('REFUS : le .par a %d liens durs. Ecrire dedans ecrirait dans le '
              'dump en lecture seule. Cassez le lien par une VRAIE copie '
              'd\'abord.' % n)
        return False
    return True


def etat(nom):
    with open(PAR, 'rb') as fp:
        n_dos, _, n_fic, off_fic, pas, noms, entrees = index(fp)
    k = rang_de(noms, pas, n_dos, n_fic, nom)
    if k is None:
        print('%s : introuvable dans l\'index (masque ?)' % nom)
        return 1
    print('%s : rang %d' % (nom, k))
    dire_entree('en place', entrees[k * 0x20:(k + 1) * 0x20])
    m = memoire_lire().get(nom)
    if m:
        dire_entree('d origine', bytes.fromhex(m['entree']))
        print('   (une entree d origine est gardee : --rendre peut revenir)')
    else:
        print('   (aucune entree d origine gardee : jamais remplacee)')
    return 0


def remplacer(nom, source):
    if not os.path.exists(source):
        print('introuvable : %s' % source)
        return 1
    if not controler_liens():
        return 2
    octets = open(source, 'rb').read()
    with open(PAR, 'r+b') as fp:
        n_dos, _, n_fic, off_fic, pas, noms, entrees = index(fp)
        k = rang_de(noms, pas, n_dos, n_fic, nom)
        if k is None:
            print('REFUS : %s est introuvable dans l\'index. S\'il est MASQUE, '
                  'rendez-le d\'abord : py -3 tools/par_masquer.py --rendre %s'
                  % (nom, nom))
            return 2
        vieille = entrees[k * 0x20:(k + 1) * 0x20]
        print('%s : rang %d' % (nom, k))
        dire_entree('avant', vieille)

        fp.seek(0, os.SEEK_END)
        fin = fp.tell()
        neuf = (fin + ALIGNEMENT - 1) // ALIGNEMENT * ALIGNEMENT
        if neuf + len(octets) >= LIMITE:
            print('REFUS : l\'offset ou la taille depasserait 4 Go '
                  '(fin 0x%X + %d octets).' % (neuf, len(octets)))
            return 2
        if len(octets) >= LIMITE:
            print('REFUS : %d octets ne tiennent pas dans un dword.'
                  % len(octets))
            return 2
        if neuf > fin:
            fp.seek(fin)
            fp.write(b'\x00' * (neuf - fin))
        fp.seek(neuf)
        fp.write(octets)

        f, taille, comp, off, z1, z2, z3, ts = struct.unpack('>8I', vieille)
        neuve = struct.pack('>8I', f & ~0x80000000, len(octets), len(octets),
                            neuf, z1, z2, z3, ts)
        fp.seek(off_fic + k * 0x20)
        fp.write(neuve)
        fp.flush()

        # --- controle : on relit l'entree ET les octets par l'index ---------
        fp.seek(off_fic + k * 0x20)
        relue = fp.read(0x20)
        if relue != neuve:
            print('REFUS : l\'entree relue ne correspond pas a ce qu\'on a '
                  'ecrit. Rien ne garantit l\'etat de l\'archive.')
            return 3
        f2, t2, c2, o2 = struct.unpack('>4I', relue[:16])
        fp.seek(o2)
        temoin = fp.read(min(t2, 1 << 20))
        if temoin != octets[:len(temoin)]:
            print('REFUS : les octets relus a l\'offset de l\'index ne sont pas '
                  'ceux du fichier.')
            return 3
    dire_entree('apres', neuve)
    print('   %d octets poses a 0x%X, NON comprimes ; les octets d\'origine '
          'sont intacts la ou ils etaient.' % (len(octets), neuf))
    m = memoire_lire()
    if nom not in m:
        m[nom] = {'rang': k, 'entree': vieille.hex()}
        memoire_ecrire(m)
        print('   entree d\'origine gardee dans analysis/par_entrees_origine.json')
    else:
        print('   (l\'entree d\'origine etait deja gardee : on n\'y touche pas)')
    return 0


def rendre(nom):
    m = memoire_lire()
    if nom not in m:
        print('REFUS : aucune entree d\'origine gardee pour %s. Rien a rendre '
              '-- et on ne devine pas un offset.' % nom)
        return 2
    if not controler_liens():
        return 2
    with open(PAR, 'r+b') as fp:
        n_dos, _, n_fic, off_fic, pas, noms, entrees = index(fp)
        k = rang_de(noms, pas, n_dos, n_fic, nom)
        if k is None:
            print('REFUS : %s introuvable dans l\'index.' % nom)
            return 2
        if k != m[nom]['rang']:
            print('REFUS : %s est au rang %d, l\'entree gardee dit %d.'
                  % (nom, k, m[nom]['rang']))
            return 2
        fp.seek(off_fic + k * 0x20)
        fp.write(bytes.fromhex(m[nom]['entree']))
    dire_entree('rendue', bytes.fromhex(m[nom]['entree']))
    del m[nom]
    memoire_ecrire(m)
    print('   l\'archive pointe de nouveau ses octets d\'origine.')
    return 0


def main():
    argv = sys.argv[1:]
    if '--etat' in argv:
        return etat(argv[argv.index('--etat') + 1])
    if '--rendre' in argv:
        return rendre(argv[argv.index('--rendre') + 1])
    if '--remplacer' in argv:
        nom = argv[argv.index('--remplacer') + 1]
        if '--par' not in argv:
            print('--remplacer <nom> demande --par <fichier>')
            return 1
        return remplacer(nom, argv[argv.index('--par') + 1])
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
