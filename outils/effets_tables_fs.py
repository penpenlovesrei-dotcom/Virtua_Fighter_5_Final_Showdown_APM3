#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Les tables PAR DECOR des taches d'effet de Final Showdown, retrouvees dans
le code -- et les indices que chacune connait.

Pourquoi cet outil : la liste des taches d'un decor (table de 0x60 en
0x18034D570) ne dit QUE ce que le decor demande. Chaque tache va ensuite
chercher l'indice du decor dans SA PROPRE table ; absente de cette table, elle
retourne sans rien faire. C'est la seule raison pour laquelle un decor importe
a ses taches et pas ses effets.

La forme est toujours la meme, et c'est elle qu'on retrouve -- jamais une
adresse notee :

    cmp  edx, [rip+T0]        le champ 0 de l enregistrement 0 est l indice
    lea  rcx, [rip+T0]
    cmovne rcx, 0
    cmp  edx, [rip+T1]        T1 - T0 = LE PAS
    ...
    test rcx, rcx / je sortie   <-- pas dans la table : la tache ne fait rien

Le compilateur deroule quand les enregistrements sont peu nombreux (Ripple en
a deux) et fait une boucle bornee par -1 quand ils sont nombreux (Snow).

    py -3 tools/effets_tables_fs.py
    py -3 tools/effets_tables_fs.py --indices 15,72,9,48,40,60
"""
import argparse
import os
import struct
import sys

import capstone
import pefile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
sys.path.insert(0, ICI)

DLL = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                   'vf5fs-pxd-w64-Retail_APM3.dll.origine')


class Img(object):
    def __init__(self, chemin):
        self.pe = pefile.PE(chemin, fast_load=True)
        self.base = self.pe.OPTIONAL_HEADER.ImageBase
        self.secs = []
        for s in self.pe.sections:
            self.secs.append((s.Name.rstrip(b'\0').decode('latin-1'),
                              self.base + s.VirtualAddress,
                              s.Misc_VirtualSize))

    def rd(self, va, n):
        return self.pe.get_data(va - self.base, n)

    def sec(self, va):
        for n, a, t in self.secs:
            if a <= va < a + t:
                return n
        return None

    def i32(self, va):
        return struct.unpack('<i', self.rd(va, 4))[0]


def comparaisons(img, zone):
    """[(va, cible, mnemonique)] de tout `cmp/mov r32, [rip+x]` visant `zone`.

    Le desassemblage lineaire DERAILLE au premier octet indecodable -- une
    table de sauts, un bourrage -- et capstone s arrete la sans rien dire.
    On reprend donc un octet apres le point d arret, jusqu a la fin de la
    section ; c est la seule facon de voir tout le `.text`.
    """
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    deb, fin = zone
    out = []
    for nom, a, t in img.secs:
        if nom != '.text':
            continue
        code = img.rd(a, t)
        pos = 0
        while pos < len(code):
            avance = 0
            for ins in md.disasm(code[pos:], a + pos):
                avance = ins.address + ins.size - (a + pos)
                if ins.mnemonic not in ('cmp', 'mov', 'movsxd'):
                    continue
                for op in ins.operands:
                    if (op.type == capstone.x86.X86_OP_MEM
                            and op.mem.base == capstone.x86.X86_REG_RIP
                            and op.mem.index == 0):
                        c = ins.address + ins.size + op.mem.disp
                        if deb <= c < fin:
                            out.append((ins.address, c, ins.mnemonic))
            pos += max(avance, 1)
    return out


def tables(img, zone=(0x180643000, 0x180644000)):
    """Regroupe les comparaisons en TABLES : meme fonction, pas constant."""
    cmps = [(a, c) for a, c, mn in comparaisons(img, zone) if mn == 'cmp']
    cmps.sort()
    lots = []
    courant = []
    for a, c in cmps:
        if courant and a - courant[-1][0] > 0x60:
            lots.append(courant)
            courant = []
        courant.append((a, c))
    if courant:
        lots.append(courant)
    out = []
    for lot in lots:
        cibles = sorted(set(c for _, c in lot))
        if len(cibles) == 1:
            pas = None
        else:
            ecarts = set(cibles[i + 1] - cibles[i]
                         for i in range(len(cibles) - 1))
            pas = min(ecarts) if len(ecarts) == 1 else None
        out.append(dict(site=lot[0][0], base=cibles[0], pas=pas,
                        nombre=len(cibles), cibles=cibles))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pe', default=DLL)
    ap.add_argument('--zone', default='0x180643000,0x180644000')
    ap.add_argument('--indices', default='')
    a = ap.parse_args()
    deb, fin = [int(x, 16) for x in a.zone.split(',')]
    img = Img(a.pe)
    interet = [int(x) for x in a.indices.split(',') if x.strip()]
    print('# %s' % os.path.basename(a.pe))
    print('# zone 0x%X..0x%X' % (deb, fin))
    print('%-12s %-12s %-6s %-5s %s'
          % ('site', 'table', 'pas', 'nb', 'indices connus'))
    for t in tables(img, (deb, fin)):
        ind = [img.i32(c) for c in t['cibles']]
        marque = ''
        if interet:
            tr = [i for i in interet if i in ind]
            marque = '   <== %s' % ' '.join(str(i) for i in tr) if tr else ''
        print('0x%-10X 0x%-10X %-6s %-5d %s%s'
              % (t['site'], t['base'],
                 ('0x%X' % t['pas']) if t['pas'] else '-',
                 t['nombre'], ' '.join(str(i) for i in ind), marque))


if __name__ == '__main__':
    main()
