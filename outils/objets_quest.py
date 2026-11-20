#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA BOUTIQUE DU QUEST : la table des objets, posee a cote du jeu.

Le mode Quest de 2007 vend des pieces de costume (libelle 937 « Item shop »,
291 « Select an item to buy », 998 « Already purchased », 999 « %dG »). Pour
les vendre il faut trois choses, et les trois se lisent :

  * QUELS objets -- la table `chritm_tbl` du jeu, une par personnage, dont ce
    projet sait deja lire la disposition (`tools/objets_correspondance.py`) ;
  * LEUR NOM -- celui de 2007 en anglais, `analysis/dlc/vf5_item_names_en.json`,
    releve par une autre seance ;
  * LEUR PRIX -- la colonne **Point** du CSV de Final Showdown
    (`extracted/csv_utf8/APM3_FS/chritm_tbl/<code>_itm.csv`). C'est le jeu qui
    la donne, on ne l'invente pas.

Et il faut le NUMERO de l'objet DANS Final Showdown, pas celui de 2007 : c'est
`analysis/quest/objets_2007_vers_fs.json` qui traduit, par le nom japonais.

Le fichier ecrit, `quest_objets.bin`, est lu par `tools/quest_runtime.c` :

    "QOBJ"  u32 version=1   u32 nb_persos
    puis nb_persos x u32 : le decalage de la table de chaque personnage
    table : u32 nombre, puis par objet { u16 id_fs, u16 prix, u32 nom }
    le pot de chaines, en UTF-8 termine par zero

    py -3 tools/objets_quest.py --ecrire
    py -3 tools/objets_quest.py --lister aki
"""
import argparse
import csv
import io
import json
import os
import struct
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIBLE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'quest_objets.bin')
NOMS = os.path.join(RACINE, 'analysis', 'dlc', 'vf5_item_names_en.json')
TRAD = os.path.join(RACINE, 'analysis', 'quest', 'objets_2007_vers_fs.json')
CSV = os.path.join(RACINE, 'extracted', 'csv_utf8', 'APM3_FS', 'chritm_tbl')

PERSOS = ['aki', 'aoi', 'bra', 'goh', 'jak', 'jef', 'kag', 'lau', 'lei',
          'lio', 'pai', 'sar', 'shu', 'van', 'wol', 'msk', 'mon', 'krt',
          'tak']
PRIX_DEFAUT = 500


def prix_fs(code):
    """{id FS: prix}, colonne « Point » du CSV du jeu."""
    p = os.path.join(CSV, code + '_itm.csv')
    out = {}
    if not os.path.exists(p):
        return out
    for r in csv.DictReader(io.open(p, encoding='utf-8')):
        try:
            i = int(r['ID'])
        except (TypeError, ValueError):
            continue
        try:
            out[i] = int(r.get('Point') or 0)
        except ValueError:
            out[i] = 0
    return out


def construire():
    noms = json.load(io.open(NOMS, encoding='utf-8'))
    trad = json.load(io.open(TRAD, encoding='utf-8'))
    tables = []
    for code in PERSOS:
        t, prix = [], prix_fs(code)
        for e in noms.get(code, []):
            fs = trad.get(code, {}).get(str(e['id']))
            if fs is None:
                continue                      # sans equivalent dans FS
            nom = e.get('name') or ''
            if not nom or nom == 'NO NAME':
                continue
            p = prix.get(fs, 0) or PRIX_DEFAUT
            t.append((fs, min(p, 65535), nom))
        t.sort()
        tables.append(t)
    return tables


def ecrire(tables):
    pot, chaines = bytearray(), {}

    def poser(s):
        if s not in chaines:
            chaines[s] = len(pot)
            pot.extend(s.encode('utf-8') + b'\0')
        return chaines[s]

    corps, decalages = bytearray(), []
    for t in tables:
        decalages.append(len(corps))
        corps += struct.pack('<I', len(t))
        for fs, prix, nom in t:
            corps += struct.pack('<HHI', fs, prix, poser(nom))
    entete = bytearray(b'QOBJ' + struct.pack('<II', 1, len(tables)))
    base_corps = len(entete) + 4 * len(tables)
    for d in decalages:
        entete += struct.pack('<I', base_corps + d)
    base_pot = base_corps + len(corps)
    # les decalages de nom sont relatifs au pot : on les rend absolus
    out = bytearray(entete + corps)
    o = base_corps
    for t in tables:
        n = struct.unpack_from('<I', out, o)[0]
        o += 4
        for _ in range(n):
            fs, prix, dn = struct.unpack_from('<HHI', out, o)
            struct.pack_into('<HHI', out, o, fs, prix, base_pot + dn)
            o += 8
    out += pot
    with open(CIBLE, 'wb') as fh:
        fh.write(out)
    return len(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--ecrire', action='store_true')
    ap.add_argument('--lister', metavar='CODE')
    a = ap.parse_args()
    tables = construire()
    if a.lister:
        i = PERSOS.index(a.lister)
        for fs, prix, nom in tables[i][:40]:
            print('  FS %-5d %6d G  %s' % (fs, prix, nom))
        print('  %d objets' % len(tables[i]))
        return 0
    n = ecrire(tables)
    print('  %s ecrit : %d octets' % (os.path.relpath(CIBLE, RACINE), n))
    for c, t in zip(PERSOS, tables):
        print('    %-4s %4d objets' % (c, len(t)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
