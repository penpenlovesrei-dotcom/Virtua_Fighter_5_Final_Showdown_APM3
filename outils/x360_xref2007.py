# -*- coding: utf-8 -*-
"""QUI CONSTRUIT CETTE CONSTANTE, dans l'image PowerPC de VF5 2007.

Le pendant de `x360_ppc.py xref` pour le bon binaire : celui-la porte en dur
l'image de FINAL SHOWDOWN (voir le 14.7), et les deux ont la meme base, donc
il repond autre chose sans erreur.

ET CE N'EST PAS LA MEME QUESTION QUE `glob2`. Celui-la cherche un ACCES
MEMOIRE a une adresse ; une vtable, elle, est une VALEUR QU'ON RANGE. Chercher
l'une avec l'autre rend « 0 acces » sur une vtable pourtant employee -- c'est
ce qui vient d'arriver sur les quatre vtables de tournoi.

On cherche donc la CONSTRUCTION de la valeur, sous ses trois formes :

    lis rX, hi                       -> hi<<16
    lis rX, hi ; addi rX, rX, lo     -> hi<<16 + lo
    lis rX, hi ; ori  rX, rX, lo     -> hi<<16 | lo

La paire peut etre separee par quelques instructions ; on accepte jusqu'a
quatre mots d'ecart, sur le MEME registre et sans qu'il soit reecrit.
"""
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.getcwd(), 'tools'))
import x360_ppc                                        # noqa: E402

IMG = os.path.join('extracted', 'X360_VF5', 'vf5_x360.img')
ECART = 5


def sdep(w):
    d = w & 0xFFFF
    return d - 0x10000 if d & 0x8000 else d


def main():
    cibles = [int(x, 0) for x in sys.argv[1:]]
    if not cibles:
        print(__doc__)
        return 1
    img = x360_ppc.Image(IMG)
    mots = []
    for s in img.secs:
        if not s['exec']:
            continue
        va0 = s['va'] & ~3
        brut = img.d[img.off(va0):img.off(va0) + s['vsize']]
        for i in range(0, len(brut) - 3, 4):
            mots.append((va0 + i, struct.unpack_from('>I', brut, i)[0]))
    print('image : %s  %d mots executables' % (os.path.basename(IMG), len(mots)))

    for cible in cibles:
        print()
        print('=== 0x%08X ===' % cible)
        n = 0
        for i, (va, w) in enumerate(mots):
            if w >> 26 != 15 or ((w >> 16) & 31) != 0:       # lis rX, hi
                continue
            rt = (w >> 21) & 31
            hi = (w & 0xFFFF) << 16
            if hi == cible:
                print('  0x%08X  lis r%d, 0x%04X        (valeur exacte)'
                      % (va, rt, w & 0xFFFF))
                n += 1
            for j in range(i + 1, min(i + 1 + ECART, len(mots))):
                va2, w2 = mots[j]
                o2, t2, a2 = w2 >> 26, (w2 >> 21) & 31, (w2 >> 16) & 31
                if o2 == 14 and a2 == rt:                     # addi rD, rX, lo
                    if ((hi + sdep(w2)) & 0xFFFFFFFF) == cible:
                        print('  0x%08X  lis r%d + addi r%d, %+d  -> 0x%08X'
                              % (va2, rt, t2, sdep(w2), cible))
                        n += 1
                elif o2 == 24 and a2 == rt:                   # ori rD, rX, lo
                    if ((hi | (w2 & 0xFFFF)) & 0xFFFFFFFF) == cible:
                        print('  0x%08X  lis r%d + ori  r%d, 0x%04X -> 0x%08X'
                              % (va2, rt, t2, w2 & 0xFFFF, cible))
                        n += 1
                if o2 in (15, 14, 24) and t2 == rt and a2 != rt:
                    break                                     # rX refait
        print('  -> %d construction(s)' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
