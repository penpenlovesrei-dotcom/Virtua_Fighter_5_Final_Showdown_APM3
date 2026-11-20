# -*- coding: utf-8 -*-
"""Lecture minimale d un minidump : l exception, le module fautif, et RIP.

MINIDUMP_MODULE fait 112 octets, et le RVA du nom est a l offset 24 :
    ULONG64 BaseOfImage        0
    ULONG32 SizeOfImage        8
    ULONG32 CheckSum          12
    ULONG32 TimeDateStamp     16
    RVA     ModuleNameRva     20   <- (apres 4 octets de bourrage a 8 ?)
"""
import os
import struct
import sys

p = sys.argv[1]
d = open(p, 'rb').read()
assert d[:4] == b'MDMP', d[:4]
nstreams, rva = struct.unpack_from('<II', d, 8)
mods = []
exc = None
for i in range(nstreams):
    t, sz, off = struct.unpack_from('<III', d, rva + 12 * i)
    if t == 6:
        exc = (sz, off)
    elif t == 4:
        n = struct.unpack_from('<I', d, off)[0]
        pas = (sz - 4) // n if n else 0
        for k in range(n):
            b = off + 4 + pas * k
            base, taille = struct.unpack_from('<QI', d, b)
            nom = '?'
            for cand in (20, 24):
                nrva = struct.unpack_from('<I', d, b + cand)[0]
                if 0 < nrva < len(d) - 4:
                    ln = struct.unpack_from('<I', d, nrva)[0]
                    if 0 < ln < 1024 and nrva + 4 + ln <= len(d):
                        nom = d[nrva + 4:nrva + 4 + ln].decode(
                            'utf-16-le', 'replace')
                        break
            mods.append((base, taille, os.path.basename(nom)))
        print('(MINIDUMP_MODULE : %d octets par entree, %d modules)' % (pas, n))

sz, off = exc
tid, _al, code, flags, rec, adr = struct.unpack_from('<IIIIQQ', d, off)
nb = struct.unpack_from('<I', d, off + 32)[0]
params = struct.unpack_from('<%dQ' % min(nb, 15), d, off + 40)
print('exception 0x%08X   adresse fautive 0x%X' % (code, adr))
print('parametres : %s' % ['0x%X' % x for x in params])
for base, taille, nom in mods:
    if base <= adr < base + taille:
        print('DANS %s   base 0x%X   offset 0x%X' % (nom, base, adr - base))
        print('VA rebasee a 0x180000000 : 0x%X' % (0x180000000 + (adr - base)))
        break
else:
    print('hors de tout module charge')
for base, taille, nom in mods:
    if 'APM3' in nom.upper() or nom.lower().startswith('vfes'):
        print('  module %-44s base 0x%X  taille 0x%X' % (nom, base, taille))
