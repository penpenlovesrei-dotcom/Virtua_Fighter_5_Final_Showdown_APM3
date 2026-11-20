#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vider une table de .rdata en qwords, avec resolution des chaines/fonctions."""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                          # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')
img = P.Image(MOTEUR)

lo = int(sys.argv[1], 0)
hi = int(sys.argv[2], 0)


def lire_str(va, n=64):
    o = img.va2off(va)
    if o is None:
        return None
    b = img.data[o:o + n]
    k = b.find(b'\x00')
    if k <= 0:
        return None
    s = b[:k]
    if all(32 <= c < 127 for c in s):
        return s.decode('ascii')
    return None


for va in range(lo, hi, 8):
    q = img.read(va, 8)
    if len(q) < 8:
        break
    v = struct.unpack('<Q', q)[0]
    s = img.sec_of(v) if v else None
    note = ''
    if s is not None:
        note = '[%s]' % s['name']
        if s['exec']:
            note += ' FONCTION'
        else:
            t = lire_str(v)
            if t:
                note += ' "%s"' % t
    print('0x%X : 0x%016X  %s' % (va, v, note))
