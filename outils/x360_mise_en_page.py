# -*- coding: utf-8 -*-
"""LA MISE EN PAGE d'un ecran du Quest : ses fenetres et leurs libelles,
dans l'ordre ou il les pose.

L'IDIOME, lu sur la plus courte des six (FUN_8231D5E0, 480 octets) :

    FUN_822E39C0(ancres, &pos, "<nom de fenetre>", 0);   /* resout l'ANCRE  */
    FUN_8223BEB8(pos.x, pos.y);                          /* s'y place       */
    texte = FUN_82322798(<numero>);                      /* prend le TEXTE  */
    FUN_8223FE30(police, texte);                         /* dessine         */

Donc chaque nom de fenetre s'apparie au numero de libelle qui le suit. On
parcourt la fonction dans l'ordre, on note les deux evenements, et on rend la
suite. Les numeros sont ceux de 2007 ; `tools/quest_textes_map.h` les nomme.

Ce qui n'est PAS rendu : les coordonnees. Elles ne sont pas dans le code --
c'est l'ANCRE de la planche AET qui les porte (c'est la regle du 9.17 : le
Quest ne place pas son texte, il le POSE). Le code ne cite que le nom.
"""
import os
import re
import struct
import sys

sys.path.insert(0, os.path.join(os.getcwd(), 'tools'))
import capstone                                         # noqa: E402
from capstone import ppc                                # noqa: E402
import x360_ppc                                         # noqa: E402
import quest_x360 as Q                                  # noqa: E402

IMG = os.path.join('extracted', 'X360_VF5', 'vf5_x360.img')
TEXTE = 0x82322798          # FUN_82322798(numero) -> la chaine
MAP = os.path.join('tools', 'quest_textes_map.h')

FONCTIONS = [
    ('Announce', 0x82316A28), ('Entry', 0x82317150),
    ('MessageInfo', 0x8231AAA0), ('MatchInfo', 0x8231B1C0),
    ('List', 0x82319238), ('ResultInfo', 0x8231D5E0),
]


def libelles():
    out = {}
    if not os.path.exists(MAP):
        return out
    for l in open(MAP, encoding='utf-8', errors='replace'):
        m = re.search(r'\{\s*(\d+),\s*(\d+)\s*\},\s*/\*(.*?)\*/', l)
        if m:
            out[int(m.group(1))] = (int(m.group(2)), m.group(3).strip())
    return out


def sext(v, bits):
    s = 1 << (bits - 1)
    return (v & (s - 1)) - (v & s)


def chaine(img, a):
    try:
        b = img.lire(a, 72)
    except Exception:
        return None
    f = b.find(b'\x00')
    if f <= 2:
        return None
    s = b[:f]
    return s.decode('ascii') if all(32 <= c < 127 for c in s) else None


def main():
    img = x360_ppc.Image(IMG)
    bornes = dict(Q.Image().fonctions())
    noms = libelles()
    md = capstone.Cs(capstone.CS_ARCH_PPC,
                     capstone.CS_MODE_32 | capstone.CS_MODE_BIG_ENDIAN)
    md.detail = True
    r3 = next(n for n in range(1, 400) if md.reg_name(n) == 'r3')
    print('%d libelles nommes par quest_textes_map.h' % len(noms))

    for nom, deb in FONCTIONS:
        n = bornes.get(deb)
        print()
        print('=== %-12s 0x%08X, %s octets ===' % (nom, deb, n or '?'))
        if not n:
            continue
        vals = {}
        suite = []
        for k in range(n // 4):
            a = deb + k * 4
            w = struct.unpack('>I', img.lire(a, 4))[0]
            insn = next(md.disasm(img.lire(a, 4), a), None)
            # un bl vers le fournisseur de texte ?
            if w >> 26 == 18 and (w & 3) == 1:
                if a + sext(w & 0x03FFFFFC, 26) == TEXTE:
                    v = vals.get(r3)
                    suite.append(('libelle', a, v))
                vals = {k2: v2 for k2, v2 in vals.items() if k2 > 12 + r3}
                continue
            if insn is None:
                continue
            m, ops = insn.mnemonic, insn.operands
            if not ops or ops[0].type != ppc.PPC_OP_REG:
                continue
            d = ops[0].reg
            if m in ('lis', 'addis'):
                vals[d] = (ops[-1].imm & 0xFFFF) << 16
            elif m == 'li':
                vals[d] = ops[-1].imm & 0xFFFFFFFF
            elif m in ('addi', 'ori') and len(ops) == 3 \
                    and ops[1].type == ppc.PPC_OP_REG and ops[1].reg in vals:
                b = vals[ops[1].reg]
                vals[d] = ((b + ops[2].imm) if m == 'addi'
                           else (b | (ops[2].imm & 0xFFFF))) & 0xFFFFFFFF
                s = chaine(img, vals[d])
                if s and s.startswith('p_'):
                    suite.append(('fenetre', a, s))
            else:
                vals.pop(d, None)
        for quoi, a, v in suite:
            if quoi == 'fenetre':
                print('   0x%08X  FENETRE  %s' % (a, v))
            elif v is None:
                print('   0x%08X    libelle : numero non constant' % a)
            else:
                fs, txt = noms.get(v, (None, '(inconnu)'))
                print('   0x%08X    libelle %4d (0x%03X) -> %-6s  %s'
                      % (a, v, v, ('FS %d' % fs) if fs else '-', txt))
    return 0


if __name__ == '__main__':
    sys.exit(main())
