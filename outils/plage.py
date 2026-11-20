#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Desassemble une PLAGE d'adresses, sans s'arreter au premier `ret`.

Une fonction reelle couvre souvent PLUSIEURS entrees `.pdata` chainees : la
prendre pour la fonction entiere fait lire un fragment et conclure faux (piege
rencontre le 2026-09-04 sur la mise a jour du menu console). Cet outil prend
des bornes explicites et rend tout ce qu'il y a entre.

    py -3 tools/plage.py 0x180173110 0x1801735C5
    py -3 tools/plage.py 0x180173110 0x1801735C5 --origine
"""
import os
import re
import sys

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                        # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    lo, hi = int(sys.argv[1], 0), int(sys.argv[2], 0)
    chemin = MOTEUR + ('.origine' if '--origine' in sys.argv else '')
    img = P.Image(chemin)
    off = img.va2off(lo)
    if off is None:
        # Le remplissage de fin de section vit ENTRE la taille virtuelle et la
        # taille brute : `va2off` le refuse, alors qu'il est bien projete en
        # memoire (il est dans SizeOfRawData). C'est la seule caverne du
        # binaire, il faut donc savoir la lire.
        for s_ in img.secs:
            if s_['va'] <= lo < s_['va'] + s_['rsize']:
                off = s_['off'] + (lo - s_['va'])
                break
    if off is None:
        print('adresse hors des sections : 0x%X' % lo)
        return 1
    blob = img.data[off:off + (hi - lo)]
    cibles = set()
    ins = list(img.md.disasm(blob, lo))
    for x in ins:
        if x.op_str.startswith('0x') and x.mnemonic[0] in 'jl':
            try:
                cibles.add(int(x.op_str, 16))
            except ValueError:
                pass
    for x in ins:
        note = ''
        for op in x.operands:
            if (op.type == capstone.x86.X86_OP_MEM
                    and op.mem.base == capstone.x86.X86_REG_RIP):
                t = x.address + x.size + op.mem.disp
                note = '  ; -> 0x%X' % t
                raw = img.read(t, 64)
                m = re.match(rb'[\x20-\x7e]{3,60}', raw) if raw else None
                if m:
                    note += '  "%s"' % m.group().decode('latin-1')
        etiq = '>' if x.address in cibles else ' '
        print('%s 0x%X  %-20s %s %s%s'
              % (etiq, x.address, x.bytes.hex(), x.mnemonic, x.op_str, note))
    return 0


if __name__ == '__main__':
    sys.exit(main())
