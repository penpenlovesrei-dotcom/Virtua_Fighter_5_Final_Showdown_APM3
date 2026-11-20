#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Squelette annote de 0x180227790 : appels, chaines, immediats remarquables."""
import os
import struct
import sys

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                          # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')
img = P.Image(MOTEUR)

LO = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0x180227790
HI = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x18022945D


def cstr(va, n=64):
    o = img.va2off(va)
    if o is None:
        return None
    b = img.data[o:o + n]
    k = b.find(b'\x00')
    if k < 2:
        return None
    s = b[:k]
    if all(32 <= c < 127 for c in s):
        return s.decode('ascii')
    return None


def deref_str(va):
    """va pointe-t-il sur un pointeur vers une chaine ?"""
    q = img.read(va, 8)
    if len(q) < 8:
        return None
    v = struct.unpack('<Q', q)[0]
    if not (0x180000000 <= v < 0x181000000):
        return None
    return cstr(v)


o = img.va2off(LO)
code = img.data[o:o + (HI - LO)]
cibles = set()
lignes = []
for ins in img.md.disasm(code, LO):
    txt = None
    if ins.mnemonic == 'call' and ins.op_str.startswith('0x'):
        txt = 'CALL %s' % ins.op_str
        cibles.add(int(ins.op_str, 16))
    elif 'rip' in ins.op_str:
        for op in ins.operands:
            if (op.type == capstone.x86.X86_OP_MEM
                    and op.mem.base == capstone.x86.X86_REG_RIP):
                t = ins.address + ins.size + op.mem.disp
                s = cstr(t)
                d = deref_str(t)
                if s:
                    txt = '"%s"  (0x%X)' % (s, t)
                elif d:
                    txt = '[0x%X] -> "%s"' % (t, d)
    if txt:
        lignes.append('  0x%-11X %-8s %-40s %s'
                      % (ins.address, ins.mnemonic, ins.op_str[:40], txt))

print('=== squelette : appels + chaines ===')
for l in lignes:
    print(l)
print()
print('=== cibles d\'appel distinctes (%d) ===' % len(cibles))
for c in sorted(cibles):
    print('  0x%X' % c)
