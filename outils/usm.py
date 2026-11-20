#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Lit un film CRI Sofdec2 (`.usm`) : ses morceaux, ses tables, ses flux.

Le format se lit sans documentation : tout y est gros-boutiste et auto-decrit.

UN MORCEAU (chunk), en-tete de 0x20 octets :

    +0x00  4o   signature : 'CRID' (index), '@SFV' (video), '@SFA' (audio),
                '@SBT' (sous-titres), '@ALP' (couche alpha)
    +0x04  u32  taille, SANS les huit premiers octets
    +0x08  u8   zero
    +0x09  u8   deplacement de la charge utile a partir de +0x08
    +0x0A  u16  bourrage a la fin
    +0x0C  u8   numero de voie
    +0x0D  u8   -            +0x0E  u8   -
    +0x0F  u8   type : 0 donnee, 1 entete, 2 fin de flux, 3 metadonnees
    +0x10  u32  date de la trame     +0x14  u32  cadence
    +0x18  u32  -                    +0x1C  u32  -

    charge utile = [8 + deplacement ; 8 + taille - bourrage[

UNE TABLE `@UTF`, le format de metadonnees de CRI :

    +0x00  '@UTF'      +0x04  u32 taille (apres ce champ)
    puis, RELATIF A +0x08 :
    +0x08  u32 offset des lignes      +0x0C  u32 offset des chaines
    +0x10  u32 offset des donnees     +0x14  u32 nom de la table
    +0x18  u16 nombre de colonnes     +0x1A  u16 longueur d'une ligne
    +0x1C  u32 nombre de lignes       +0x20  les colonnes

Une colonne : un octet de drapeaux, puis l'offset de son nom. Le quartet bas
des drapeaux donne le TYPE (0 u8, 1 s8, 2 u16, 3 s16, 4 u32, 5 s32, 6 u64,
7 s64, 8 float, 9 double, 0xA chaine, 0xB donnees), le quartet haut le
RANGEMENT : 0x10 rien, 0x30 une constante ecrite dans la colonne, 0x50 une
valeur par ligne.

    py -3 tools/usm.py info   <film.usm>
    py -3 tools/usm.py plan   <film.usm>        les morceaux, un par ligne
    py -3 tools/usm.py demux  <film.usm> <dossier>
"""
import os
import struct
import sys

SIGNATURES = (b'CRID', b'@SFV', b'@SFA', b'@SBT', b'@ALP', b'@CUE')
TYPES = {0: 'donnee', 1: 'entete', 2: 'fin', 3: 'metadonnees'}


# --------------------------------------------------------------- tables @UTF
def _lire_valeur(d, o, t):
    """Rend (valeur, taille) pour le type `t` a l'offset `o`."""
    fmt = {0: '>B', 1: '>b', 2: '>H', 3: '>h', 4: '>I', 5: '>i',
           6: '>Q', 7: '>q', 8: '>f', 9: '>d'}.get(t)
    if fmt:
        n = struct.calcsize(fmt)
        return struct.unpack_from(fmt, d, o)[0], n
    if t == 0xA:                                   # chaine : offset
        return struct.unpack_from('>I', d, o)[0], 4
    if t == 0xB:                                   # donnees : offset + taille
        return struct.unpack_from('>II', d, o), 8
    raise ValueError('type de colonne inconnu : 0x%X' % t)


def lire_utf(d, base=0):
    """Rend (nom_de_table, [dict par ligne]) pour la table @UTF a `base`."""
    if d[base:base + 4] != b'@UTF':
        raise ValueError('pas une table @UTF a 0x%X' % base)
    taille, = struct.unpack_from('>I', d, base + 4)
    r = base + 8                                   # tous les offsets partent d'ici
    (off_lignes, off_chaines, off_donnees, nom_table) = \
        struct.unpack_from('>4I', d, r)
    n_col, long_ligne = struct.unpack_from('>2H', d, r + 16)
    n_lig, = struct.unpack_from('>I', d, r + 20)

    def chaine(o):
        p = r + off_chaines + o
        return d[p:d.index(b'\x00', p)].decode('utf-8', 'replace')

    colonnes, o = [], r + 24
    for _ in range(n_col):
        drapeaux = d[o]
        o += 1
        nom = chaine(struct.unpack_from('>I', d, o)[0])
        o += 4
        typ, rangement = drapeaux & 0x0F, drapeaux & 0xF0
        constante = None
        if rangement == 0x30:
            constante, n = _lire_valeur(d, o, typ)
            o += n
        colonnes.append((nom, typ, rangement, constante))

    lignes = []
    for i in range(n_lig):
        p = r + off_lignes + i * long_ligne
        ligne = {}
        for nom, typ, rangement, constante in colonnes:
            if rangement == 0x10:
                ligne[nom] = None
                continue
            if rangement == 0x30:
                v = constante
            else:
                v, n = _lire_valeur(d, p, typ)
                p += n
            if typ == 0xA:
                v = chaine(v)
            elif typ == 0xB:
                deb, lg = v
                v = d[r + off_donnees + deb: r + off_donnees + deb + lg]
            ligne[nom] = v
        lignes.append(ligne)
    return chaine(nom_table), lignes, 8 + taille


# ------------------------------------------------------------------ morceaux
def morceaux(chemin):
    """Parcourt le fichier et rend un dict par morceau, sans tout charger."""
    taille = os.path.getsize(chemin)
    with open(chemin, 'rb') as fp:
        pos = 0
        while pos < taille:
            fp.seek(pos)
            tete = fp.read(0x20)
            if len(tete) < 0x20:
                return
            sig = tete[:4]
            if sig not in SIGNATURES:
                raise ValueError('signature inattendue %r a 0x%X' % (sig, pos))
            n, = struct.unpack_from('>I', tete, 4)
            depl = tete[9]
            bourrage, = struct.unpack_from('>H', tete, 0x0A)
            voie = tete[0x0C]
            typ = tete[0x0F]
            date, cadence = struct.unpack_from('>2I', tete, 0x10)
            debut = pos + 8 + depl
            fin = pos + 8 + n - bourrage
            yield {'pos': pos, 'sig': sig.decode('latin-1'), 'taille': n,
                   'depl': depl, 'bourrage': bourrage, 'voie': voie,
                   'type': typ, 'date': date, 'cadence': cadence,
                   'debut': debut, 'fin': fin, 'tete': tete}
            pos += 8 + n


def charge(fp, m):
    fp.seek(m['debut'])
    return fp.read(m['fin'] - m['debut'])


# ------------------------------------------------------------------ commandes
def cmd_info(chemin):
    print('%s   %d octets' % (os.path.basename(chemin),
                              os.path.getsize(chemin)))
    with open(chemin, 'rb') as fp:
        vus = 0
        for m in morceaux(chemin):
            if m['type'] not in (1, 3):
                continue
            d = charge(fp, m)
            if d[:4] != b'@UTF':
                continue
            nom, lignes, _ = lire_utf(d)
            print('\n--- %s (%s, voie %d, %d ligne(s)) ---'
                  % (nom, m['sig'], m['voie'], len(lignes)))
            for i, ligne in enumerate(lignes):
                if len(lignes) > 1:
                    print('  ligne %d' % i)
                for k, v in ligne.items():
                    if isinstance(v, bytes):
                        v = '<%d octets>' % len(v)
                    print('    %-24s %s' % (k, v))
            vus += 1
            if vus >= 8:
                print('\n(… autres tables non affichees)')
                break
    return 0


def cmd_plan(chemin, limite=40):
    compte, octets = {}, {}
    for i, m in enumerate(morceaux(chemin)):
        cle = (m['sig'], m['voie'], TYPES.get(m['type'], m['type']))
        compte[cle] = compte.get(cle, 0) + 1
        octets[cle] = octets.get(cle, 0) + (m['fin'] - m['debut'])
        if i < limite:
            print('0x%09X  %-4s voie %d  %-11s  taille %8d  depl %3d  '
                  'bourrage %5d  date %8d / %d'
                  % (m['pos'], m['sig'], m['voie'],
                     TYPES.get(m['type'], m['type']), m['taille'], m['depl'],
                     m['bourrage'], m['date'], m['cadence']))
        elif i == limite:
            print('...')
    print('\n%-6s %-5s %-12s %10s %14s' % ('flux', 'voie', 'type',
                                           'morceaux', 'octets'))
    for cle in sorted(compte):
        print('%-6s %-5d %-12s %10d %14d'
              % (cle[0], cle[1], cle[2], compte[cle], octets[cle]))
    return 0


def cmd_demux(chemin, dossier):
    os.makedirs(dossier, exist_ok=True)
    base = os.path.splitext(os.path.basename(chemin))[0]
    sorties = {}
    with open(chemin, 'rb') as fp:
        for m in morceaux(chemin):
            if m['type'] != 0:
                continue
            ext = {'@SFV': 'm2v', '@SFA': 'adx', '@SBT': 'sbt',
                   '@ALP': 'alp'}.get(m['sig'], 'bin')
            cle = (m['sig'], m['voie'])
            if cle not in sorties:
                nom = '%s_%s%d.%s' % (base, m['sig'][1:].lower(), m['voie'],
                                      ext)
                sorties[cle] = open(os.path.join(dossier, nom), 'wb')
                print('-> %s' % nom)
            sorties[cle].write(charge(fp, m))
    for f in sorties.values():
        f.close()
    return 0


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        print(__doc__)
        return 1
    cmd, chemin = a[0], a[1]
    if cmd == 'info':
        return cmd_info(chemin)
    if cmd == 'plan':
        return cmd_plan(chemin)
    if cmd == 'demux':
        return cmd_demux(chemin, a[2] if len(a) > 2 else '.')
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
