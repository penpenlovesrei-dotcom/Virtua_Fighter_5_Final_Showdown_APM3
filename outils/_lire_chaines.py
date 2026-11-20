#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lit des chaines ASCII a des VA donnees, sur .origine. Lecture seule."""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                        # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')


def main():
    img = P.Image(MOTEUR)
    for a in sys.argv[1:]:
        va = int(a, 0)
        raw = img.read(va, 160) or b''
        # coupe au premier NUL
        s = raw.split(b'\x00')[0]
        print('0x%09X  %r' % (va, s.decode('latin-1')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
