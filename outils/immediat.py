#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Toutes les instructions portant un IMMEDIAT donne, par balayage lineaire.

Sert a retrouver une constante de domaine (« 41 decors », « 21 personnages »)
la ou il n'y a ni chaine ni pointeur a suivre.

    py -3 tools/immediat.py 0x29
    py -3 tools/immediat.py 0x29 --mnemos cmp,mov
"""
import os
import sys

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                          # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')
X = capstone.x86


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__)
        return 1
    val = int(args[0], 0)
    mnemos = None
    if '--mnemos' in sys.argv:
        mnemos = set(sys.argv[sys.argv.index('--mnemos') + 1].split(','))
    img = P.Image(MOTEUR + '.origine')
    n = 0
    for s in img.secs:
        if not s['exec']:
            continue
        blob = img.data[s['off']:s['off'] + s['rsize']]
        pos = 0
        while pos < len(blob):
            avance = 0
            for ins in img.md.disasm(blob[pos:], s['va'] + pos):
                avance = ins.address - s['va'] + ins.size
                if mnemos and ins.mnemonic not in mnemos:
                    continue
                if ins.mnemonic[0] == 'j' or ins.mnemonic == 'call':
                    continue
                for op in ins.operands:
                    if op.type == X.X86_OP_IMM and op.imm == val:
                        fb = P.func_bounds(img, ins.address)
                        print('0x%-12X %-34s %s'
                              % (ins.address,
                                 '%s %s' % (ins.mnemonic, ins.op_str),
                                 ('dans 0x%X' % fb[0]) if fb
                                 else '(hors .pdata)'))
                        n += 1
                        break
            pos = avance if avance > pos else pos + 1
    print('== %d occurrence(s)' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
