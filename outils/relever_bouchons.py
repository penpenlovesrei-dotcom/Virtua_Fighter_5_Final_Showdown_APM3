# -*- coding: utf-8 -*-
"""LA TABLE DE CORRESPONDANCE, site par site.

LES COUPES NE SONT PAS DANS LES VTABLES -- mesure faite d abord : sur les 353
classes communes, aucun creneau n est bouchonne chez nous et pourvu dans REVO.
Les creneaux 5 et 6 le sont des DEUX cotes (virtuelles inutilisees), et les
vtables de REVO ont simplement un creneau de plus, ce qui decale la suite.

Les coupes sont donc DANS LE CODE : `call bouchon ; test al,al ; je` -- et pour
les comparer il faut APPARIER LES FONCTIONS, ce que seules les chaines
permettent. On ancre sur une chaine citee par la fonction et UNIQUE dans le
binaire.

LES BOUCHONS SE CHERCHENT PAR MOTIF, pas parmi les fonctions .pdata : une
fonction de trois octets n a pas d entree .pdata, et le premier jet en trouvait
DEUX au lieu des quatre reels.
"""
import os
import pickle
import sys

import capstone

ICI = r'C:\Users\frede\Desktop\VF5RE\tools'
sys.path.insert(0, ICI)
import pe_disasm as P
import graphe_appels as G

CAS = (('APM3', r'C:\Users\frede\Desktop\VF5RE\runtime\media\vf5fs'
        r'\vf5fs-pxd-w64-Retail_APM3.dll.origine', 0x180345000),
       ('REVO', r'C:\Program Files (x86)\Steam\steamapps\common\VFREVO'
        r'\runtime\media\vf5fs\vf5fs-pxd-w64-d3d12_SteamRetail.dll',
        0x180371000))

INT3 = b'\xcc'
CORPS = ((b'\x32\xc0\xc3', 'xor al,al ; ret   -> FAUX'),
         (b'\x33\xc0\xc3', 'xor eax,eax ; ret -> 0'),
         (b'\xb0\x01\xc3', 'mov al,1 ; ret    -> VRAI'),
         (b'\xc2\x00\x00', 'ret 0             -> rien'))


def analyser(nom, chemin, fin_text):
    img = P.Image(chemin)
    img.md.detail = True
    debuts, _fins = G.fonctions_reelles(img)
    bornes = sorted(debuts)

    def fonction_de(va):
        lo = None
        for d in bornes:
            if d > va:
                break
            lo = d
        return lo

    bouchons = {}
    for motif, quoi in CORPS:
        o = 0
        cle = INT3 + motif
        while True:
            o = img.data.find(cle, o)
            if o < 0:
                break
            va = img.off2va(o + 1)
            if va and va < fin_text:
                bouchons[va] = quoi
            o += 1

    def cstr(va, n=64):
        o = img.va2off(va)
        if o is None:
            return None
        b = img.data[o:o + n]
        k = b.find(b'\x00')
        if k < 5:
            return None
        s = b[:k]
        if not all(32 <= c < 127 for c in s):
            return None
        return s.decode('ascii')

    appels = {}
    chaines = {}
    for depart in range(16):
        va = 0x180001000 + depart
        while va < fin_text:
            off = img.va2off(va)
            if off is None:
                break
            bloc = img.data[off:off + 0x400]
            avance = 0
            for ins in img.md.disasm(bloc, va):
                avance += ins.size
                if ins.mnemonic == 'call' and ins.op_str.startswith('0x'):
                    t = int(ins.op_str, 16)
                    if t in bouchons:
                        appels.setdefault(fonction_de(ins.address), set()).add(
                            (ins.address, t))
                for op in ins.operands:
                    if (op.type == capstone.x86.X86_OP_MEM
                            and op.mem.base == capstone.x86.X86_REG_RIP):
                        s = cstr(ins.address + ins.size + op.mem.disp)
                        if s:
                            chaines.setdefault(
                                fonction_de(ins.address), set()).add(s)
            va += max(avance, 1)

    uniques = {}
    for f, ss in chaines.items():
        for s in ss:
            if img.data.count(s.encode() + b'\x00') == 1:
                uniques.setdefault(s, set()).add(f)
    ancres = dict((s, list(fs)[0]) for s, fs in uniques.items()
                  if len(fs) == 1)
    print('%s : %d fonctions | %d bouchons | %d fonctions en appellent un | '
          '%d ancres' % (nom, len(bornes), len(bouchons), len(appels),
                         len(ancres)))
    for va, quoi in sorted(bouchons.items()):
        print('      bouchon 0x%X  %s' % (va, quoi))
    return appels, chaines, ancres, bouchons


sortie = {}
for nom, ch, fin in CAS:
    sortie[nom] = analyser(nom, ch, fin)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'sites.pkl'), 'wb') as fp:
    pickle.dump(sortie, fp)
print('releve enregistre')
