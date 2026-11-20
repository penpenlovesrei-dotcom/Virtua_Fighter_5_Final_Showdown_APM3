#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Squelette annote d'une ou plusieurs fonctions, bornes .pdata rattachees."""
import os
import struct
import sys

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                          # noqa: E402
import graphe_appels as G                                      # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')
img = P.Image(MOTEUR)
DEBUTS, FINS = G.fonctions_reelles(img)


def cstr(va, n=64):
    o = img.va2off(va)
    if o is None:
        return None
    b = img.data[o:o + n]
    k = b.find(b'\x00')
    if k < 2:
        return None
    s = b[:k]
    return s.decode('ascii') if all(32 <= c < 127 for c in s) else None


def deref_str(va):
    q = img.read(va, 8)
    if len(q) < 8:
        return None
    v = struct.unpack('<Q', q)[0]
    if not (0x180000000 <= v < 0x181000000):
        return None
    return cstr(v)


def dbl(va):
    q = img.read(va, 8)
    if len(q) < 8:
        return None
    return struct.unpack('<d', q)[0]


for arg in sys.argv[1:]:
    lo = int(arg, 0)
    hi = FINS.get(lo)
    if hi is None:
        print('0x%X : pas d\'entree .pdata' % lo)
        continue
    o = img.va2off(lo)
    code = img.data[o:o + (hi - lo)]
    print('===== 0x%X .. 0x%X  (%d o) =====' % (lo, hi, hi - lo))
    for ins in img.md.disasm(code, lo):
        txt = None
        if ins.mnemonic == 'call' and ins.op_str.startswith('0x'):
            txt = ''
        elif 'rip' in ins.op_str:
            for op in ins.operands:
                if (op.type == capstone.x86.X86_OP_MEM
                        and op.mem.base == capstone.x86.X86_REG_RIP):
                    t = ins.address + ins.size + op.mem.disp
                    s, d = cstr(t), deref_str(t)
                    if s:
                        txt = '"%s"  (0x%X)' % (s, t)
                    elif d:
                        txt = '[0x%X] -> "%s"' % (t, d)
                    elif ins.mnemonic in ('vmovsd', 'movsd', 'vmovss'):
                        txt = 'const 0x%X = %r' % (t, dbl(t))
                    else:
                        txt = '-> 0x%X' % t
        if txt is not None:
            print('  0x%-11X %-9s %-42s %s'
                  % (ins.address, ins.mnemonic, ins.op_str[:42], txt))
    print()
