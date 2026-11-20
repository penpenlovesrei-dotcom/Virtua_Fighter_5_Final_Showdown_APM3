#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Liste les chaines ASCII d'une plage d'OFFSETS FICHIER, avec leur RVA/VA si
le fichier est un PE.

    py -3 tools/zone_chaines.py <fichier> 0x397000 0x39B000 [--min 4]
"""
import argparse
import re
import sys

try:
    import pefile
except ImportError:
    pefile = None


def carte_pe(chemin):
    if pefile is None:
        return None
    try:
        pe = pefile.PE(chemin, fast_load=True)
    except Exception:
        return None
    base = pe.OPTIONAL_HEADER.ImageBase
    sect = []
    for s in pe.sections:
        sect.append((s.PointerToRawData, s.PointerToRawData + s.SizeOfRawData,
                     base + s.VirtualAddress,
                     s.Name.rstrip(b'\x00').decode('latin1')))
    return sect


def va_de(sect, off):
    if not sect:
        return None, ''
    for a, b, va, nom in sect:
        if a <= off < b:
            return va + (off - a), nom
    return None, ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fichier')
    ap.add_argument('debut')
    ap.add_argument('fin')
    ap.add_argument('--min', type=int, default=4)
    a = ap.parse_args()
    d = int(a.debut, 0)
    f = int(a.fin, 0)
    sect = carte_pe(a.fichier)
    with open(a.fichier, 'rb') as fh:
        fh.seek(d)
        donnees = fh.read(f - d)
    for mo in re.finditer(rb'[\x20-\x7e]{%d,}' % a.min, donnees):
        off = d + mo.start()
        va, nom = va_de(sect, off)
        print('off=0x%08X  va=%s  %-8s  %s'
              % (off, ('0x%09X' % va) if va else '     ---     ', nom,
                 mo.group(0).decode('latin1')))


if __name__ == '__main__':
    main()
