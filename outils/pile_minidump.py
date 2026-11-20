#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""LA PILE DU FIL FAUTIF d un minidump, rebasee sur 0x180000000.

`lire_minidump.py` donne l adresse de la faute ; il ne dit pas PAR OU on y est
arrive. Ici on lit la pile du fil qui a leve l exception et on retient tout
mot de 64 bits qui tombe dans le moteur : ce sont les adresses de retour, donc
la chaine d appel -- la seule facon de savoir si un plantage vient de NOUS.

    py -3 tools/pile_minidump.py <dump> [--tout]
"""
import os
import struct
import sys

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
BASE_FICHIER = 0x180000000


def flux(d):
    """{type: (rva, taille)} du repertoire de flux."""
    assert d[:4] == b'MDMP', d[:4]
    n, rva = struct.unpack_from('<II', d, 8)
    out = {}
    for i in range(n):
        t, taille, r = struct.unpack_from('<III', d, rva + i * 12)
        out[t] = (r, taille)
    return out


def modules(d, f):
    """[(nom, base, taille)] du flux des modules."""
    if 4 not in f:
        return []
    rva = f[4][0]
    n = struct.unpack_from('<I', d, rva)[0]
    out = []
    pas = (f[4][1] - 4) // n
    for i in range(n):
        o = rva + 4 + i * pas
        base, taille = struct.unpack_from('<QI', d, o)
        # ModuleNameRva est en +0x14 (MINIDUMP_MODULE fait 108 octets :
        # base 0, taille 8, somme 0xC, date 0x10, nom 0x14, version 0x18).
        nom_rva = struct.unpack_from('<I', d, o + 0x14)[0]
        lg = struct.unpack_from('<I', d, nom_rva)[0]
        nom = d[nom_rva + 4:nom_rva + 4 + lg].decode('utf-16-le', 'replace')
        out.append((os.path.basename(nom), base, taille))
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    d = open(sys.argv[1], 'rb').read()
    f = flux(d)
    mods = modules(d, f)
    mo = [m for m in mods if m[0].lower() == MOTEUR.lower()]
    if not mo:
        print('le moteur n est pas dans ce dump')
        return 1
    _, mbase, mtaille = mo[0]
    print('%s charge en 0x%X (0x%X octets)' % (MOTEUR, mbase, mtaille))
    # le fil fautif
    if 6 not in f:
        print('pas de flux d exception')
        return 1
    ex = f[6][0]
    fil = struct.unpack_from('<I', d, ex)[0]
    code, _drap, _suiv, adr = struct.unpack_from('<IIQQ', d, ex + 8)
    print('fil fautif %d, exception 0x%08X a 0x%X' % (fil, code, adr))
    if mbase <= adr < mbase + mtaille:
        print('   soit, rebasee : 0x%X' % (BASE_FICHIER + adr - mbase))
    # sa pile
    if 3 not in f:
        print('pas de flux de fils')
        return 1
    rva = f[3][0]
    n = struct.unpack_from('<I', d, rva)[0]
    for i in range(n):
        o = rva + 4 + i * 48
        tid = struct.unpack_from('<I', d, o)[0]
        if tid != fil:
            continue
        # MINIDUMP_THREAD : id 0, ..., Teb 0x10, PILE en 0x18.
        deb, taille, mrva = struct.unpack_from('<QII', d, o + 0x18)
        pile = d[mrva:mrva + taille]
        print('pile : 0x%X, %d octets' % (deb, taille))
        print()
        print('les adresses de retour, du plus recent au plus ancien :')
        vus = 0
        for k in range(0, len(pile) - 8, 8):
            v = struct.unpack_from('<Q', pile, k)[0]
            if not (mbase <= v < mbase + mtaille):
                continue
            r = BASE_FICHIER + v - mbase
            marque = ''
            if r >= 0x180EA1000:
                marque = '   <- LA GREFFE : un de NOS relais'
            print('   pile+0x%05X  0x%X%s' % (k, r, marque))
            vus += 1
            if vus >= 60 and '--tout' not in sys.argv:
                print('   ... (--tout pour la suite)')
                break
        return 0
    print('le fil fautif n est pas dans la liste')
    return 1


if __name__ == '__main__':
    sys.exit(main())
