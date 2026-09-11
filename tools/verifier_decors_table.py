#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Controle du deplacement des deux tables de decors, SANS lancer le jeu.

Quatre questions, quatre reponses, toutes tirees de la DLL patchee et comparees
a `.origine` :

  1. les octets recopies sont-ils IDENTIQUES a la source ?
  2. les huit sites visent-ils bien la nouvelle table ?
  3. chaque pointeur de la source a-t-il sa RELOCATION dans la copie -- ni une
     de moins, ni une de plus ?
  4. un rebasage simule corrige-t-il les pointeurs de la copie ?

Le point 3 est le seul qui compte vraiment : une relocation oubliee ne se voit
pas au format, elle se voit a l'ecran, sous la forme d'un decor qui ne charge
pas ou d'un plantage au premier acces.

    py -3 tools/verifier_decors_table.py
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import pefile                                                  # noqa: E402
import patch_moteur as PM                                      # noqa: E402

BASE = 0x180000000
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
DLL = os.path.join(JEU, 'vf5fs-pxd-w64-Retail_APM3.dll')
ORIGINE = DLL + '.origine'


def relogees(pe):
    out = set()
    pe.parse_data_directories(directories=[
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_BASERELOC']])
    for b in pe.DIRECTORY_ENTRY_BASERELOC:
        for e in b.entries:
            if e.type == 10:
                out.add(BASE + e.rva)
    return out


def main():
    o = pefile.PE(ORIGINE, fast_load=True)
    p = pefile.PE(DLL, fast_load=True)
    sec = None
    for s in p.sections:
        if s.Name.rstrip(b'\x00') == b'.decors':
            sec = s
    if sec is None:
        print('la DLL patchee n a pas de section .decors : le correctif '
              '--decors-table n a pas ete applique.')
        return 1
    va = BASE + sec.VirtualAddress
    # Le nombre de decors ne se DEDUIT pas de la taille de section : elle est
    # arrondie a la page. Le lanceur le passe, et on controle les 41 d'origine
    # plus les entrees neuves.
    # LE NOMBRE DE DECORS SE LIT DANS LE BINAIRE, il ne se suppose pas.
    #
    # Il valait `DECORS_TABLE_N` (41) en dur. Le 2026-09-10, sur un build a 61
    # decors, ce controle a donc annonce ONZE FAUTES qui n'en etaient pas :
    # il cherchait la table des codes a +0x2670 alors qu'elle est a +0x3930, et
    # lisait l'entree 41 comme si c'etaient des codes. Un controle qui ment est
    # pire que pas de controle.
    #
    # La table des codes suit les descripteurs, alignee a 16 -- et 0xF0 est
    # deja un multiple de 16, donc `off_codes = n * 0xF0` exactement. Le site
    # du `lea` des codes donne son adresse : n s'en deduit.
    pas = PM.DECORS_TABLE_PAS
    champ, dec = PM.DECORS_CODES_SITES[0]
    vise = champ + 4 + struct.unpack('<i', p.get_data(champ - BASE, 4))[0] - dec
    n = (vise - va) // pas
    if not (PM.DECORS_TABLE_N <= n <= 256) or va + n * pas != vise:
        print('  (le site des codes vise 0x%X, soit %d descripteurs : ce n est '
              'pas un compte credible ; on retombe sur %d)'
              % (vise, n, PM.DECORS_TABLE_N))
        n = PM.DECORS_TABLE_N
    if '--n' in sys.argv:
        n = int(sys.argv[sys.argv.index('--n') + 1], 0)
    off_codes = (n * pas + 0xF) & ~0xF
    print('.decors en 0x%X, %d octets ; %d descripteurs en +0, codes en +0x%X'
          % (va, sec.Misc_VirtualSize, n, off_codes))
    print()

    fautes = []

    # 1. les octets -- on ne compare que les 41 d'origine : les suivantes sont
    #    des entrees NEUVES, qui n'ont pas de source a comparer.
    n41 = PM.DECORS_TABLE_N
    src_d = o.get_data(PM.DECORS_TABLE_VA - BASE, n41 * pas)
    cop_d = p.get_data(va - BASE, n41 * pas)
    src_c = o.get_data(PM.DECORS_CODES_VA - BASE, n41 * 8)
    cop_c = p.get_data(va + off_codes - BASE, n41 * 8)
    print('1. LES OCTETS RECOPIES')
    for quoi, a, b in (('descripteurs', src_d, cop_d), ('codes', src_c, cop_c)):
        if a == b:
            print('   %-14s %6d octets IDENTIQUES' % (quoi, len(a)))
        else:
            k = next(i for i in range(len(a)) if a[i] != b[i])
            fautes.append('%s : premier ecart a +0x%X' % (quoi, k))
            print('   %-14s ECART a +0x%X' % (quoi, k))

    # 2. les huit sites
    print()
    print('2. LES HUIT SITES')
    for sites, base_neuve, quoi in (
            (PM.DECORS_TABLE_SITES, va, 'descripteurs'),
            (PM.DECORS_CODES_SITES, va + off_codes, 'codes')):
        for champ, dec in sites:
            d = struct.unpack('<i', p.get_data(champ - BASE, 4))[0]
            vise = champ + 4 + d
            attendu = base_neuve + dec
            etat = 'ok' if vise == attendu else 'FAUX'
            if vise != attendu:
                fautes.append('site 0x%X vise 0x%X au lieu de 0x%X'
                              % (champ, vise, attendu))
            print('   0x%-12X %-14s -> 0x%X   %s' % (champ, quoi, vise, etat))

    # 3. les relocations, une par une
    print()
    print('3. LES RELOCATIONS')
    ro, rp = relogees(o), relogees(p)
    attendues, manquantes, en_trop = 0, [], []
    for k in range(0, n41 * pas, 8):
        if PM.DECORS_TABLE_VA + k in ro:
            attendues += 1
            if va + k not in rp:
                manquantes.append(va + k)
        elif va + k in rp:
            en_trop.append(va + k)
    for k in range(0, n41 * 8, 8):
        if PM.DECORS_CODES_VA + k in ro:
            attendues += 1
            if va + off_codes + k not in rp:
                manquantes.append(va + off_codes + k)
        elif va + off_codes + k in rp:
            en_trop.append(va + off_codes + k)
    print('   %d pointeurs dans la source, %d relocations posees dans la copie'
          % (attendues, attendues - len(manquantes)))
    if manquantes:
        fautes.append('%d relocation(s) MANQUANTE(S), ex. 0x%X'
                      % (len(manquantes), manquantes[0]))
        print('   %d MANQUANTE(S) : %s' % (len(manquantes),
                                           ' '.join('0x%X' % v
                                                    for v in manquantes[:6])))
    if en_trop:
        fautes.append('%d relocation(s) EN TROP, ex. 0x%X'
                      % (len(en_trop), en_trop[0]))
        print('   %d EN TROP : %s' % (len(en_trop),
                                      ' '.join('0x%X' % v
                                               for v in en_trop[:6])))
    perdues = ro - rp
    perdues = {v for v in perdues
               if not (PM.DECORS_TABLE_VA <= v < PM.DECORS_TABLE_VA + n41 * pas)}
    if perdues:
        fautes.append('%d relocation(s) d origine perdues' % len(perdues))
        print('   %d relocation(s) d ORIGINE perdues !' % len(perdues))
    else:
        print('   aucune relocation d origine perdue')

    # 3 bis. LA GRILLE, si elle a demenage
    off_grille = None
    if sec.Misc_VirtualSize > ((n * 8 + off_codes + 0xF) & ~0xF):
        off_grille = (off_codes + n * 8 + 0xF) & ~0xF
        print()
        print('3 bis. LA GRILLE DE SELECTION')
        gn, gpas = PM.GRILLE_TABLE_N, PM.GRILLE_TABLE_PAS
        src_g = o.get_data(PM.GRILLE_TABLE_VA - BASE, gn * gpas)
        cop_g = p.get_data(va + off_grille - BASE, gn * gpas)
        print('   %d cases en +0x%X : octets %s'
              % (gn, off_grille,
                 'IDENTIQUES' if src_g == cop_g else 'DIFFERENTS'))
        if src_g != cop_g:
            fautes.append('grille : octets differents')
        for champ, dec in PM.GRILLE_TABLE_SITES:
            d = struct.unpack('<i', p.get_data(champ - BASE, 4))[0]
            vise = champ + 4 + d
            attendu = va + off_grille + dec
            if vise != attendu:
                fautes.append('site grille 0x%X vise 0x%X au lieu de 0x%X'
                              % (champ, vise, attendu))
            print('   0x%-12X -> 0x%X   %s'
                  % (champ, vise, 'ok' if vise == attendu else 'FAUX'))
        manque = [k for k in range(0, gn * gpas, 8)
                  if (PM.GRILLE_TABLE_VA + k in ro) and (va + off_grille + k
                                                         not in rp)]
        print('   %d pointeurs d icone relogés, %d manquant(s)'
              % (sum(1 for k in range(0, gn * gpas, 8)
                     if PM.GRILLE_TABLE_VA + k in ro), len(manque)))
        if manque:
            fautes.append('grille : %d relocation(s) manquante(s)' % len(manque))
        # LES QUATRE COMPTES DOIVENT ETRE INTACTS : la grille garde 21 cases.
        for champ, taille, attendu, quoi in PM.GRILLE_TABLE_COMPTES:
            v = int.from_bytes(p.get_data(champ - BASE, taille), 'little')
            if v != attendu:
                fautes.append('compte de grille 0x%X = %d, attendu %d (%s)'
                              % (champ, v, attendu, quoi))
            print('   compte 0x%-12X %-6d %s' % (champ, v,
                                                 'intact' if v == attendu
                                                 else 'MODIFIE'))

    # 4. le rebasage simule
    print()
    print('4. LE REBASAGE SIMULE')
    delta = 0x7FFC81C70000 - BASE
    brut = bytearray(open(DLL, 'rb').read())
    corrigees = 0
    for k in range(0, n41 * pas, 8):
        if va + k not in rp:
            continue
        off = sec.PointerToRawData + k
        v = struct.unpack_from('<Q', brut, off)[0]
        struct.pack_into('<Q', brut, off, (v + delta) & 0xFFFFFFFFFFFFFFFF)
        corrigees += 1
    # le descripteur du dojo doit alors pointer ses chaines a la bonne place
    d_djo = 11 * pas
    for champ, quoi in ((0x00, 'STGDJO'), (0x48, 'collision'), (0xC0, 'murs')):
        off = sec.PointerToRawData + d_djo + champ
        v = struct.unpack_from('<Q', brut, off)[0]
        src = struct.unpack_from('<Q', src_d, d_djo + champ)[0]
        etat = 'ok' if v == src + delta else 'FAUX'
        if v != src + delta:
            fautes.append('djo +0x%02X (%s) : 0x%X au lieu de 0x%X'
                          % (champ, quoi, v, src + delta))
        print('   djo +0x%02X %-10s 0x%X -> 0x%X   %s'
              % (champ, quoi, src, v, etat))
    print('   %d pointeurs corriges dans la table deplacee' % corrigees)

    print()
    print('-' * 70)
    if fautes:
        print('%d FAUTE(S) :' % len(fautes))
        for f in fautes:
            print('   . %s' % f)
        return 1
    print('AUCUNE FAUTE. Les deux tables sont deplacees a l identique, les huit')
    print('sites les visent, et les %d pointeurs sont relogeables.' % attendues)
    print('-' * 70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
