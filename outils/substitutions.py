#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Cherche les SUBSTITUTIONS d'une valeur par une autre dans `.text`.

Motif vise : une comparaison a `source` suivie, dans les quelques
instructions qui suivent, d'un immediat `cible`. C'est la forme qu'ont pris
les trois bouchons « du1 -> du2 » de VF5 :

    cmp eax, 0x15 ; jne ... ; mov [..], 0x16          (0x180175320)
    cmp eax, 0x15 ; mov ecx, 0x16 ; cmove eax, ecx    (0x180175390)

Un seul de ces sites manquant suffit a rendre un decor inatteignable, et rien
ne le signale. On les enumere donc, plutot que de les trouver un par un.

    py -3 tools/substitutions.py 0x15 0x16
    py -3 tools/substitutions.py 0x15 0x16 --fenetre 10 --patche
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
    if len(args) < 2:
        print(__doc__)
        return 1
    src, dst = int(args[0], 0), int(args[1], 0)
    fen = 8
    if '--fenetre' in sys.argv:
        fen = int(sys.argv[sys.argv.index('--fenetre') + 1], 0)
    chemin = MOTEUR + ('' if '--patche' in sys.argv else '.origine')
    img = P.Image(chemin)
    n = 0
    for s in img.secs:
        if not s['exec']:
            continue
        blob = img.data[s['off']:s['off'] + s['rsize']]
        pos = 0
        while pos < len(blob):
            avance = 0
            suite = []
            for ins in img.md.disasm(blob[pos:], s['va'] + pos):
                avance = ins.address - s['va'] + ins.size
                suite.append(ins)
                if len(suite) > fen + 1:
                    suite.pop(0)
                if ins.mnemonic != 'cmp':
                    continue
                if not any(o.type == X.X86_OP_IMM and o.imm == src
                           for o in ins.operands):
                    continue
                # on regarde la fenetre QUI SUIT, en re-desassemblant
                off = img.va2off(ins.address)
                bloc = img.data[off:off + 15 * (fen + 1)]
                apres = list(img.md.disasm(bloc, ins.address))[:fen + 1]
                touche = [i for i in apres[1:]
                          if any(o.type == X.X86_OP_IMM and o.imm == dst
                                 for o in i.operands)]
                if not touche:
                    continue
                fb = P.func_bounds(img, ins.address)
                print('== 0x%X  %s' % (ins.address,
                                       ('dans 0x%X' % fb[0]) if fb
                                       else '(hors .pdata)'))
                for i in apres:
                    marque = '  <<<' if i in touche else ''
                    print('   0x%-11X %-22s %s %s%s'
                          % (i.address, i.bytes.hex(), i.mnemonic, i.op_str,
                             marque))
                n += 1
            pos = avance if avance > pos else pos + 1
    print('== %d site(s) « %d -> %d »' % (n, src, dst))
    return 0


if __name__ == '__main__':
    sys.exit(main())
