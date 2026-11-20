# -*- coding: utf-8 -*-
"""L'INVENTAIRE DES BRUITAGES DEMANDES, par NOM, dans l'image de VF5 2007.

Le joueur est `FUN_822B3840(voie, nom)`, le nom etant une CHAINE dans r4.

DEUX DEFAUTS DE LA PREMIERE VERSION, et les deux rendaient « 0 nom » :

 1. les enveloppes SAUTENT au joueur, elles ne l'appellent pas :
        lis  r11, 0x8208 ; li r3, 0 ; addi r4, r11, 0x46B0 ; b 0x822B3840
    Ne chercher que `bl` (LK=1) les ratait toutes. On prend donc `b` ET `bl`,
    et on dit laquelle des deux ;
 2. la partie haute de l'adresse est construite dans UN AUTRE registre (r11),
    puis combinee dans r4. Exiger que le `lis` cible r4 ne resolvait rien.

D'ou une vraie propagation de constantes sur la fenetre qui precede l'appel :
`lis`, `li`, `addi`, `ori`, et tout le reste efface ce qu'il ecrit.

    py -3 bruitages2.py            tout le binaire
    py -3 bruitages2.py --quest    seulement le bloc du Quest
"""
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.getcwd(), 'tools'))
import capstone                                         # noqa: E402
from capstone import ppc                                # noqa: E402
import x360_ppc                                         # noqa: E402

IMG = os.path.join('extracted', 'X360_VF5', 'vf5_x360.img')
JOUEUR = 0x822B3840
QUEST = (0x82300000, 0x82321200)
FENETRE = 14


def sext(v, bits):
    s = 1 << (bits - 1)
    return (v & (s - 1)) - (v & s)


def chaine(img, a):
    try:
        b = img.lire(a, 80)
    except Exception:
        return None
    f = b.find(b'\x00')
    if f <= 0:
        return None
    s = b[:f]
    if not all(32 <= c < 127 for c in s):
        return None
    return s.decode('ascii')


def valeur_de_r4(img, md, va, r4):
    """Propage les constantes sur la fenetre avant `va`, rend r4 ou None."""
    deb = va - FENETRE * 4
    vals = {}
    for k in range(FENETRE):
        adr = deb + k * 4
        if adr >= va:
            break
        # MOT PAR MOT : un mot que capstone ne decode pas ne doit pas
        # arreter la fenetre (son generateur, lui, s'arrete).
        insn = next(md.disasm(img.lire(adr, 4), adr), None)
        if insn is None:
            continue
        m, ops = insn.mnemonic, insn.operands
        if m in ('bl', 'bla', 'bctrl'):
            for k in list(vals):
                vals.pop(k, None)
            continue
        if not ops or ops[0].type != ppc.PPC_OP_REG:
            continue
        d = ops[0].reg
        if m in ('lis', 'addis') and len(ops) >= 2 \
                and ops[-1].type == ppc.PPC_OP_IMM:
            vals[d] = (ops[-1].imm & 0xFFFF) << 16
        elif m == 'li' and ops[-1].type == ppc.PPC_OP_IMM:
            vals[d] = ops[-1].imm & 0xFFFFFFFF
        elif m in ('addi', 'ori', 'oris') and len(ops) == 3 \
                and ops[1].type == ppc.PPC_OP_REG and ops[1].reg in vals:
            b = vals[ops[1].reg]
            i = ops[2].imm
            if m == 'addi':
                vals[d] = (b + i) & 0xFFFFFFFF
            elif m == 'ori':
                vals[d] = (b | (i & 0xFFFF)) & 0xFFFFFFFF
            else:
                vals[d] = (b | ((i & 0xFFFF) << 16)) & 0xFFFFFFFF
        else:
            vals.pop(d, None)
    return vals.get(r4)


def main():
    quest_seul = '--quest' in sys.argv
    img = x360_ppc.Image(IMG)
    md = capstone.Cs(capstone.CS_ARCH_PPC,
                     capstone.CS_MODE_32 | capstone.CS_MODE_BIG_ENDIAN)
    md.detail = True
    r4 = next(n for n in range(1, 400) if md.reg_name(n) == 'r4')

    sites = []
    for s in img.secs:
        if not s['exec']:
            continue
        va0 = s['va'] & ~3
        brut = img.d[img.off(va0):img.off(va0) + s['vsize']]
        for i in range(0, len(brut) - 3, 4):
            w = struct.unpack_from('>I', brut, i)[0]
            if w >> 26 != 18 or (w & 2):
                continue
            va = va0 + i
            if va + sext(w & 0x03FFFFFC, 26) == JOUEUR:
                sites.append((va, 'bl' if (w & 1) else 'b '))
    print('image : %s' % os.path.basename(IMG))
    print('FUN_%08X : %d site(s) -- %d appels, %d sauts'
          % (JOUEUR, len(sites),
             sum(1 for _, f in sites if f == 'bl'),
             sum(1 for _, f in sites if f == 'b ')))

    noms, inconnus = {}, []
    for va, forme in sites:
        if quest_seul and not (QUEST[0] <= va < QUEST[1]):
            continue
        a = valeur_de_r4(img, md, va, r4)
        if a is None:
            inconnus.append((va, 'r4 non reconstruit'))
            continue
        s = chaine(img, a)
        if s is None:
            inconnus.append((va, '0x%08X : pas une chaine' % a))
            continue
        noms.setdefault(s, []).append((va, forme))

    print()
    print('=== %d nom(s) distinct(s) %s ==='
          % (len(noms), 'dans le Quest' if quest_seul else 'en tout'))
    for s in sorted(noms):
        v = noms[s]
        print('  %-24s %s' % (s, ' '.join('0x%08X(%s)' % (x, f.strip())
                                          for x, f in v[:6])))
    if inconnus:
        print()
        print('=== %d non resolu(s), et je ne devine pas ===' % len(inconnus))
        for va, p in inconnus:
            print('  0x%08X  %s' % (va, p))
    return 0


if __name__ == '__main__':
    sys.exit(main())
