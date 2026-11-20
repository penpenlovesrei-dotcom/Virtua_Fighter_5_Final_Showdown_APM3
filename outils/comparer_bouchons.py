# -*- coding: utf-8 -*-
"""LA TABLE DE CORRESPONDANCE : nos creneaux bouchonnes, leur homologue REVO.

On ne compare pas des adresses -- deux builds n ont pas la meme disposition. On
compare les VTABLES par NOM DE CLASSE (le RTTI est present des deux cotes) et,
pour chaque creneau, on regarde ce qu il porte :

    BOUCHON   la cible est une fonction de trois octets qui rend une constante
              (`xor al,al ; ret`, `ret`, `mov al,1 ; ret`, ...)
    VRAIE     tout le reste

Un creneau BOUCHON chez nous et VRAIE dans REVO est une coupe du build arcade,
et REVO dit ce qu elle faisait.
"""
import io
import os
import re
import struct
import sys

ICI = r'C:\Users\frede\Desktop\VF5RE\tools'
sys.path.insert(0, ICI)
import pe_disasm as P
import rtti

A = (r'C:\Users\frede\Desktop\VF5RE\runtime\media\vf5fs'
     r'\vf5fs-pxd-w64-Retail_APM3.dll.origine')
B = (r'C:\Program Files (x86)\Steam\steamapps\common\VFREVO\runtime\media'
     r'\vf5fs\vf5fs-pxd-w64-d3d12_SteamRetail.dll')

# Les corps qui ne font QUE rendre une constante. Releves, pas supposes : on
# imprime en fin de script la liste de ceux qu on a effectivement rencontres.
CORPS = {
    b'\x32\xc0\xc3': 'xor al,al ; ret        -> FAUX',
    b'\x33\xc0\xc3': 'xor eax,eax ; ret      -> 0',
    b'\xb0\x01\xc3': 'mov al,1 ; ret         -> VRAI',
    b'\xc3': 'ret                    -> rien',
    b'\xc2\x00\x00': 'ret 0                  -> rien',
    b'\x48\x33\xc0\xc3': 'xor rax,rax ; ret      -> 0',
    b'\x33\xc0\x48\x83\xc4': None,          # pas un bouchon : prologue
}


def charger(chemin):
    img = P.Image(chemin)
    _tds, _cols, vtables = rtti.collecter(img)
    exec_ = [(s['va'], s['va'] + s['vsize']) for s in img.secs if s['exec']]

    def executable(va):
        return any(lo <= va < hi for lo, hi in exec_)

    def creneaux(va):
        out = []
        for i in range(64):
            q = img.read(va + i * 8, 8)
            if len(q) < 8:
                break
            v = struct.unpack('<Q', q)[0]
            if not executable(v):
                break
            out.append(v)
        return out

    def corps(va):
        o = img.va2off(va)
        if o is None:
            return None
        d = img.data[o:o + 5]
        for motif, quoi in CORPS.items():
            if d.startswith(motif):
                return quoi
        return None

    tab = {}
    for va, nom in vtables:
        n = re.sub(r'\?A0x[0-9a-f]+::', '', nom)
        c = creneaux(va)
        if n not in tab or len(c) > len(tab[n][1]):
            tab[n] = (va, c)
    return img, tab, corps


imgA, tabA, corpsA = charger(A)
imgB, tabB, corpsB = charger(B)

communes = sorted(set(tabA) & set(tabB))
lignes = []
vus = {}
for n in communes:
    vaA, cA = tabA[n]
    vaB, cB = tabB[n]
    if len(cA) != len(cB):
        continue                       # vtables de formes differentes : on passe
    for i, (a, b) in enumerate(zip(cA, cB)):
        ca, cb = corpsA(a), corpsB(b)
        if ca and not cb:
            lignes.append((n, i, a, ca, b, len(cA)))
            vus[ca] = vus.get(ca, 0) + 1

print('APM3 %d classes, REVO %d, communes %d' % (len(tabA), len(tabB), len(communes)))
print('creneaux bouchonnes chez nous et POURVUS dans REVO : %d' % len(lignes))
print()
print('%-44s %4s  %-12s %-26s %s' % ('classe', 'cre', 'APM3', 'ce qu il rend', 'REVO'))
print('-' * 118)
for n, i, a, ca, b, t in sorted(lignes):
    print('%-44s %4d  0x%010X %-26s 0x%010X' % (n[:44], i, a, ca.split('->')[0].strip(), b))
print()
print('corps rencontres :')
for k, v in sorted(vus.items(), key=lambda t: -t[1]):
    print('   %-40s %d' % (k, v))
