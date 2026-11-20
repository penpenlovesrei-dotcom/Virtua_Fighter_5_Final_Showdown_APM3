#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""QUI TOUCHE CETTE ADRESSE, Y COMPRIS DANS LA GREFFE.

`pe_disasm.py xref` ne parcourt que les sections d origine : la `.greffe` lui
echappe, et elle rend donc " 0 reference " pour une globale que NOS relais
lisent et ecrivent. Or c est precisement la que vivent les drapeaux.

On desassemble ici TOUTE section executable, greffe comprise, et on retient
toute instruction dont l operande RIP-relatif tombe sur la VA demandee. Le
desassemblage lineaire deraille sur les donnees ; on reprend donc apres chaque
octet indecodable au lieu de s arreter (piege connu :
reference_desassemblage_lineaire_deraille).

    py -3 greffe_xref.py <dll> <va> [<va> ...]
"""
import sys

import capstone
import pefile


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    chemin = sys.argv[1]
    cibles = {int(a, 0) for a in sys.argv[2:]}
    pe = pefile.PE(chemin, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    d = open(chemin, 'rb').read()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    total = 0
    for s in pe.sections:
        if not (s.Characteristics & 0x20000000):
            continue
        nom = s.Name.rstrip(b'\0').decode('latin-1')
        va = base + s.VirtualAddress
        off = s.PointerToRawData
        taille = min(s.Misc_VirtualSize, s.SizeOfRawData)
        code = d[off:off + taille]
        print('-- %s : 0x%X, %d octets' % (nom, va, taille))
        i = 0
        vus = 0
        while i < len(code):
            fini = True
            for ins in md.disasm(code[i:], va + i):
                fini = False
                for op in ins.operands:
                    if op.type != capstone.x86.X86_OP_MEM:
                        continue
                    if op.mem.base != capstone.x86.X86_REG_RIP:
                        continue
                    t = ins.address + ins.size + op.mem.disp
                    if t in cibles:
                        print('   0x%X  %-26s %s %s'
                              % (ins.address, ins.bytes.hex(),
                                 ins.mnemonic, ins.op_str))
                        vus += 1
                i = ins.address - va + ins.size
            if fini:
                i += 1          # octet indecodable : on reprend apres
        total += vus
        print('   %d reference(s)' % vus)
    print()
    print('%d reference(s) en tout' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())
