#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA TABLE DE CORRESPONDANCE DES OBJETS : VF5 (2007) -> Final Showdown.

POURQUOI. Chaque rival du mode Quest porte son costume dans `npc_tbl` : deux
listes de 24 identifiants d'objets (`+0x18` et `+0x48`), que le jeu de 2007
etend en un champ de mille bits dans la fiche du combattant. Final Showdown a
le meme mecanisme -- un `std::bitset` de DEUX mille bits en
`dossier_joueur + 0x160` -- mais il a RENUMEROTE ses objets : Akira en a 401
en 2007 et 1 004 dans FS. Un identifiant de 2007 ne designe donc pas le meme
objet dans FS, et poser le costume d'un rival sans traduire ses numeros
habillerait n'importe qui n'importe comment.

CE QUI SERT DE CLEF, ET POURQUOI ELLE EST SURE. Les deux tables portent, pour
chaque objet, un LIBELLE INTERNE de modele -- `ATAMA_01`, `BANDANA_01`,
`OUTER_01_H_MUNE`... C'est le nom de la piece dans l'archive de modeles, pas
un numero : il n'a pas bouge entre les deux jeux. On apparie la-dessus, et on
verifie sur la CATEGORIE (le champ `type`) : deux objets de meme libelle et de
categorie differente ne sont pas le meme objet.

LA DISPOSITION est celle que `tools/dlc/item_names.py` avait etablie pour
2007 ; la mesure du 2026-09-29 est que **Final Showdown emploie exactement la
meme** -- meme en-tete `{magie, nombre, decalage}`, memes enregistrements de
0x50 octets, meme petit-boutisme. Seule la magie differe.

    +0x04 pointeur du nom        +0x10 type (categorie)
    +0x28 pointeur du libelle    +0x44 pointeur du picto
    +0x48 code K MMM V III : K genre, MMM numero d'objet, V variante de
                             couleur, III identifiant dans la table

    py -3 tools/objets_correspondance.py            la table + le rapport
    py -3 tools/objets_correspondance.py --detail aki   objet par objet
"""
import argparse
import json
import os
import re
import struct
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
X360 = os.path.join(RACINE, 'extracted', 'quest', 'chritm_x360')
FS = os.path.join(RACINE, 'extracted', 'APM3_FS_farc', 'chritm_tbl')
SORTIE = os.path.join(RACINE, 'analysis', 'quest', 'objets_2007_vers_fs.json')

PERSOS = {
    'aki': 'Akira', 'aoi': 'Aoi', 'bra': 'Brad', 'dur': 'Dural', 'goh': 'Goh',
    'jak': 'Jacky', 'jef': 'Jeffry', 'kag': 'Kage', 'krt': 'Jean',
    'lau': 'Lau', 'lei': 'Lei-Fei', 'lio': 'Lion', 'mon': 'Eileen',
    'msk': 'El Blaze', 'pai': 'Pai', 'sar': 'Sarah', 'shu': 'Shun',
    'tak': 'Taka-Arashi', 'van': 'Vanessa', 'wol': 'Wolf',
}


def chaine(d, off):
    if not 0 < off < len(d):
        return None
    fin = d.find(b'\0', off)
    return d[off:fin].decode('utf-8', 'replace')


def lire_table(chemin):
    """Les enregistrements d'un <code>itm_tbl.bin, 2007 ou Final Showdown."""
    with open(chemin, 'rb') as fh:
        d = fh.read()
    _, nombre, debut = struct.unpack_from('<3I', d, 0)
    if debut + nombre * 0x50 > len(d):
        raise ValueError('%s : en-tete incoherent (%d x 0x50 au-dela de %d)'
                         % (os.path.basename(chemin), nombre, len(d)))
    out = []
    for k in range(nombre):
        o = debut + k * 0x50
        (code,) = struct.unpack_from('<I', d, o + 0x48)
        if code == 0:
            continue
        libelle = chaine(d, struct.unpack_from('<I', d, o + 0x28)[0])
        # L'IDENTIFIANT SE LIT DANS LE LIBELLE, PAS DANS LE CODE -- mesure du
        # 2026-09-29. Le code est `K MMM V III` avec III sur TROIS chiffres :
        # il reboucle au-dela de 999, et Final Showdown depasse le millier
        # (Kage : 913 objets, et des numeros jusqu'a 1xxx). Pris modulo 1000,
        # l'objet « 1001 PANTS_10 » d'Akira se fait passer pour le « 001
        # ATAMA_01 ». Le libelle, lui, porte le numero en clair et il est
        # confirme par le CSV du jeu (765 noms sur 768 a l'identique).
        m = re.match(r'^\s*(\d+)\s', libelle or '')
        out.append(dict(
            rang=k,
            nom=chaine(d, struct.unpack_from('<I', d, o + 4)[0]),
            type=struct.unpack_from('<I', d, o + 0x10)[0],
            libelle=libelle,
            picto=chaine(d, struct.unpack_from('<I', d, o + 0x44)[0]),
            genre=code // 10000000,
            modele=(code // 10000) % 1000,
            variante=(code // 1000) % 10,
            id=int(m.group(1)) if m else code % 1000,
        ))
    return out


def clef(enr):
    """Le libelle de modele, sans son numero de tete : « 003 OUTER_01 » -> OUTER_01."""
    lib = enr['libelle'] or ''
    m = re.match(r'^\s*\d+\s+(.*)$', lib)
    return (m.group(1) if m else lib).strip().upper()


def apparier(a2007, afs):
    """{id 2007 -> id FS}, plus ce qui n'a pas trouve preneur.

    LA CLEF EST LE NOM JAPONAIS, et c'est une mesure, pas un choix de style.
    Le libelle de modele ne distingue PAS les variantes de couleur : les
    seize bandanas d'Akira portent tous « BANDANA_01 », et ni le champ
    « variante » du code ni son champ de tete ne les separent -- 012 est le
    rouge, 112 le noir, 116 le bleu, et le code ne dit que « modele 2,
    variante 3 » pour les trois. La couleur ne vit que dans la TEXTURE, et
    dans le nom.

    Or les deux jeux ont la meme table japonaise a la racine de leur media :
    « 赤鉢巻 » en 2007 est « 赤鉢巻 » dans Final Showdown. Mesure sur Akira :
    198 objets sur 198 retrouves par le nom, et TOUS uniques.

    On apparie donc par le nom, en verifiant le modele quand les deux le
    portent ; le couple (libelle, categorie, variante) ne sert plus que de
    repli pour les objets sans nom.
    """
    par_nom = {}
    for e in afs:
        if e['nom']:
            par_nom.setdefault(e['nom'], []).append(e)
    par_clef = {}
    for e in afs:
        par_clef.setdefault((clef(e), e['type'], e['variante']), []).append(e)

    table, orphelins = {}, []
    par_nom_n = par_clef_n = discord = 0
    for e in a2007:
        cands = par_nom.get(e['nom'] or '\0')
        if cands and len(cands) == 1:
            f = cands[0]
            if clef(e) and clef(f) and clef(e) != clef(f):
                discord += 1          # meme nom, modele different : on le dit
            table[e['id']] = f['id']
            par_nom_n += 1
            continue
        k = (clef(e), e['type'], e['variante'])
        repli = par_clef.get(k) or par_clef.get((clef(e), e['type'], 0))
        if repli:
            table[e['id']] = repli[0]['id']
            par_clef_n += 1
        else:
            orphelins.append(e)
    return table, orphelins, par_nom_n, par_clef_n, discord


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--detail', metavar='CODE',
                    help='imprime objet par objet pour ce personnage')
    ap.add_argument('--sortie', default=SORTIE)
    a = ap.parse_args()

    if not os.path.isdir(X360) or not os.path.isdir(FS):
        print('Tables absentes.\n  2007 : %s\n  FS   : %s' % (X360, FS))
        return 1

    tout, lignes = {}, []
    total_2007 = total_lie = total_orph = 0
    for code in sorted(PERSOS):
        p2007 = os.path.join(X360, code + 'itm_tbl.bin')
        pfs = os.path.join(FS, code + 'itm_tbl.bin')
        if not (os.path.exists(p2007) and os.path.exists(pfs)):
            continue
        a2007, afs = lire_table(p2007), lire_table(pfs)
        table, orphelins, par_nom, par_repli, discord = apparier(a2007, afs)
        tout[code] = {str(k): v for k, v in sorted(table.items())}
        total_2007 += len(a2007)
        total_lie += len(table)
        total_orph += len(orphelins)
        lignes.append((code, PERSOS[code], len(a2007), len(afs), par_nom,
                       par_repli, len(orphelins), discord))
        if a.detail == code:
            par_id = {e['id']: e for e in afs}
            for e in a2007:
                f = par_id.get(table.get(e['id']))
                print('  %3d %-28s -> %s' % (
                    e['id'], clef(e),
                    ('%3d %s' % (f['id'], f['nom'] or '')) if f else 'ABSENT DE FS'))

    print()
    print('  %-4s %-13s %7s %7s %8s %7s %8s %8s' %
          ('code', 'personnage', '2007', 'FS', 'par nom', 'repli', 'absents', 'ecarts'))
    print('  ' + '-' * 68)
    for c, n, n7, nf, nn, nr, no, nd in lignes:
        print('  %-4s %-13s %7d %7d %8d %7d %8d %8d' % (c, n, n7, nf, nn, nr, no, nd))
    print('  ' + '-' * 68)
    print('  %-18s %7d %7s %8d %7s %8d' %
          ('TOTAL', total_2007, '', total_lie, '', total_orph))

    os.makedirs(os.path.dirname(a.sortie), exist_ok=True)
    with open(a.sortie, 'w', encoding='utf-8') as fh:
        json.dump(tout, fh, indent=1, sort_keys=True)
    print('\n  ecrit : %s' % os.path.relpath(a.sortie, RACINE))
    return 0


if __name__ == '__main__':
    sys.exit(main())
