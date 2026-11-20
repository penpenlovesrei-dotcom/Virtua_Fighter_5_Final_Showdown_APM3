#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Toutes les ECRITURES dans un champ d'objet, par desassemblage lineaire.

On cherche « mov [<registre> + <deplacement>], <source> » pour un deplacement
donne. C'est la seule facon de trouver qui pose un champ quand l'objet n'a pas
d'accesseur dedie : les setters en ligne n'apparaissent dans aucune table.

Le balayage est LINEAIRE sur toute la section executable, fonction par
fonction d'apres `.pdata` PUIS reprise brute sur les trous (les feuilles n'y
sont pas, piege deja paye deux fois sur ce chantier).

    py -3 tools/ecrit_champ.py 0x4C
    py -3 tools/ecrit_champ.py 0x4C --taille dword --lecture-aussi
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
    depl = int(args[0], 0)
    lecture = '--lecture-aussi' in sys.argv
    img = P.Image(MOTEUR + '.origine')
    fs = P.runtime_functions(img)
    md = img.md
    n = 0
    for s in img.secs:
        if not s['exec']:
            continue
        blob = img.data[s['off']:s['off'] + s['rsize']]
        pos = 0
        while pos < len(blob):
            avance = 0
            for ins in md.disasm(blob[pos:], s['va'] + pos):
                avance = ins.address - s['va'] + ins.size
                if ins.mnemonic not in ('mov', 'movzx', 'movsxd', 'lea'):
                    continue
                ops = ins.operands
                if len(ops) != 2:
                    continue
                dst, src = ops
                cible = None
                if dst.type == X.X86_OP_MEM and dst.mem.disp == depl:
                    cible = ('ecrit', dst)
                elif (lecture and src.type == X.X86_OP_MEM
                      and src.mem.disp == depl):
                    cible = ('lit', src)
                if cible is None:
                    continue
                m = cible[1].mem
                if m.base in (0, X.X86_REG_RIP, X.X86_REG_RSP,
                              X.X86_REG_RBP):
                    continue
                fb = P.func_bounds(img, ins.address)
                print('%-6s 0x%-12X %-30s  %s'
                      % (cible[0], ins.address,
                         '%s %s' % (ins.mnemonic, ins.op_str),
                         ('dans 0x%X' % fb[0]) if fb else '(hors .pdata)'))
                n += 1
            pos = avance if avance > pos else pos + 1
    print('== %d occurrence(s)' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
