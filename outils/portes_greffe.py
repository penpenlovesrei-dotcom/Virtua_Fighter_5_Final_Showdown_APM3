#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""LES PORTES DE LA GREFFE : quel site du moteur saute dans quel relais.

Un relais ne dit pas d ou il est appele. On parcourt donc TOUT le `.text` et
on releve chaque `call` ou `jmp` dont la cible tombe dans `.greffe`. C est la
carte des detournements, et elle se lit sur la DLL PRODUITE -- jamais sur le
script qui l ecrit.

    py -3 portes_greffe.py <dll> [debut_cible] [fin_cible]
"""
import sys

import capstone
import pefile

SAUTS = {'call', 'jmp'}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    chemin = sys.argv[1]
    pe = pefile.PE(chemin, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    d = open(chemin, 'rb').read()
    secs = {}
    for s in pe.sections:
        nom = s.Name.rstrip(b'\0').decode('latin-1')
        secs[nom] = (base + s.VirtualAddress, s.Misc_VirtualSize,
                     s.PointerToRawData, s.SizeOfRawData)
    if '.greffe' not in secs:
        print('pas de section .greffe')
        return 1
    gva, gsize = secs['.greffe'][0], secs['.greffe'][1]
    deb = int(sys.argv[2], 0) if len(sys.argv) > 2 else gva
    fin = int(sys.argv[3], 0) if len(sys.argv) > 3 else gva + gsize

    tva, tsize, toff, traw = secs['.text']
    code = d[toff:toff + min(tsize, traw)]
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True

    print('cibles dans 0x%X .. 0x%X' % (deb, fin))
    print()
    trouves = []
    i = 0
    while i < len(code):
        fini = True
        for ins in md.disasm(code[i:], tva + i):
            fini = False
            if ins.mnemonic in SAUTS and len(ins.operands) == 1:
                op = ins.operands[0]
                if op.type == capstone.x86.X86_OP_IMM:
                    t = op.imm
                    if deb <= t < fin:
                        trouves.append((ins.address, ins.mnemonic, t))
            i = ins.address - tva + ins.size
        if fini:
            i += 1
    for a, m, t in sorted(trouves, key=lambda x: x[2]):
        print('   0x%X  ->  %-4s 0x%X' % (a, m, t))
    print()
    print('%d porte(s)' % len(trouves))
    return 0


if __name__ == '__main__':
    sys.exit(main())
