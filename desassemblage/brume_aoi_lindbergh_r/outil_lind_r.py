# -*- coding: utf-8 -*-
"""L'ELF Lindbergh de VF5 R : index des APPELS, desassemblage, flottants.

Desassemblage LINEAIRE de `.text` (capstone, ~10 s), mis en cache a cote de
l'ELF (`vf5.calls.pickle`). Jumeau de `VF5RE/tools/index_elf.py`, qui indexe
les references aux DONNEES ; celui-ci indexe les `call`/`jmp`, ce dont on a
besoin pour remonter d'un talon PLT a ses appelants.

    py -3 outil_lind_r.py appels 0x08053A98     qui appelle cette adresse
    py -3 outil_lind_r.py func   0x0811715E --max 420
    py -3 outil_lind_r.py f32    0x08764570 2   lire des flottants
"""
import os
import pickle
import struct
import sys

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
ELF = os.environ.get('VF5R_ELF') or os.path.join(
    RACINE, 'VF5RE', 'extracted', 'LIND_R', 'id', 'disk0', 'vf5')
CACHE = ELF + '.calls.pickle'


def sections(d):
    shoff, = struct.unpack_from('<I', d, 0x20)
    shentsize, shnum, shstrndx = struct.unpack_from('<HHH', d, 0x2E)
    stro = struct.unpack_from('<6I', d, shoff + shstrndx * shentsize)[4]
    out = {}
    for i in range(shnum):
        nm, typ, flg, addr, off, size = struct.unpack_from(
            '<6I', d, shoff + i * shentsize)
        n = d[stro + nm:d.index(b'\x00', stro + nm)].decode()
        out[n] = (addr, off, size, typ)
    return out


def charger():
    d = open(ELF, 'rb').read()
    return d, sections(d)


def off(secs, va):
    for n, (a, o, s, t) in secs.items():
        if t != 8 and a and a <= va < a + s:
            return o + (va - a)
    return None


def index_appels():
    if os.path.exists(CACHE):
        return pickle.load(open(CACHE, 'rb'))
    d, secs = charger()
    va0, o0, sz, _ = secs['.text']
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.skipdata = True
    appels = {}
    for ins in md.disasm(d[o0:o0 + sz], va0):
        if ins.mnemonic in ('call', 'jmp') and ins.op_str.startswith('0x'):
            try:
                t = int(ins.op_str, 16)
            except ValueError:
                continue
            appels.setdefault(t, []).append((ins.address, ins.mnemonic))
    pickle.dump(appels, open(CACHE, 'wb'))
    return appels


def main():
    a = sys.argv[1:]
    d, secs = charger()
    if a[0] == 'appels':
        t = int(a[1], 0)
        ap = index_appels()
        for ad, mn in sorted(ap.get(t, [])):
            print('0x%08X  %s' % (ad, mn))
        print('# %d' % len(ap.get(t, [])))
        return 0
    if a[0] == 'func':
        va = int(a[1], 0)
        n = int(a[a.index('--max') + 1]) if '--max' in a else 80
        o = off(secs, va)
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        for x in md.disasm(d[o:o + n * 12], va):
            print('  0x%08X  %-20s %s %s'
                  % (x.address, x.bytes.hex(), x.mnemonic, x.op_str))
            n -= 1
            if n <= 0:
                break
        return 0
    if a[0] == 'f32':
        va = int(a[1], 0)
        n = int(a[2]) if len(a) > 2 else 8
        o = off(secs, va)
        if o is None:
            print('hors fichier (bss ?)')
            return 1
        for i in range(n):
            w, = struct.unpack_from('<I', d, o + i * 4)
            f, = struct.unpack_from('<f', d, o + i * 4)
            print('0x%08X  %08X  %g' % (va + i * 4, w, f))
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())
