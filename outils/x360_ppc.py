#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Lire l'image PowerPC de VF5 FS sur Xbox 360.

L'image sort de `tools/x360_fs.cmd` : `extracted/X360_FS/sel/default.img`,
17,6 Mo, PE gros-boutiste charge a `0x82000000`.

POURQUOI (2026-10-01). Deux ecrans de la borne APM3 -- « select part » et
« select item » -- tiennent la position de leur curseur dans leur PROPRE
grille (`+0xEE0`, `+0x9D0`+`+0x9C8`), et le seul code qui la deplacait est un
consommateur de messages dont plus personne n'est le producteur. Ecrire cette
liaison a partir de rien serait l'inventer. La version Xbox 360 porte la meme
interface -- les noms de planches `part_win`, `p_part_plt_lt` et
`p_yaji_left_c` y sont -- et elle, elle marche. On va donc la LIRE.

CE QUE FAIT CET OUTIL, et comment on cherche une chaine en PowerPC : il n'y a
pas d'adressage relatif au compteur de programme comme en x64. Une adresse
s'y construit en DEUX instructions :

    lis   rX, haut16          ; rX = haut16 << 16
    addi  rX, rX, bas16       ; rX += bas16, SIGNE

`addi` signe son immediat : quand `bas16 >= 0x8000`, l'assembleur compense en
mettant `haut16 + 1` dans le `lis`. Oublier cela fait manquer une reference
sur deux. On balaie donc tous les couples `lis`/`addi` (ou `ori`, qui lui ne
signe pas) sur le meme registre, sans instruction qui reecrive ce registre
entre les deux.

Usage :
    py -3 tools/x360_ppc.py sections
    py -3 tools/x360_ppc.py chaines <motif>
    py -3 tools/x360_ppc.py xref <va>            qui construit cette adresse
    py -3 tools/x360_ppc.py func <va> [--max N]  desassemble a partir de la
"""
import os
import re
import struct
import sys

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
IMAGE = os.path.join(RACINE, 'extracted', 'X360_FS', 'sel', 'default.img')


# ---------------------------------------------------------------------------
# LA TABLE DE CORRESPONDANCE, et comment elle a ete MESUREE (2026-10-01)
#
# `TaskCsMenu::update` existe dans les deux builds et fait la meme chose dans
# le meme ordre. Cote borne c'est `0x1801BBBE0`, cote Xbox 360 `0x82217B30`.
# En les lisant cote a cote, instruction par instruction, les champs se
# nomment d'eux-memes -- aucune supposition :
#
#     APM3                                X360
#     cmp byte [rcx+0x231], 0             lbz  r11, 0x1c1(r3)
#     cmp dword [rcx+0x224], 0            lwz  r11, 0x1b4(r31)
#     mov esi, [rcx+0x58]                 lwz  r27, 0x4c(r31)
#     movzx r8d, byte [rbx+0x228]         lbz  r5,  0x1b8(r31)
#     call 0x1801A2EC0  (deplaceur V)     bl   0x821FE600
#     call [rax+0x38]   (accepteur V)     bctrl sur le creneau [6]
#     mov [rbx+0x58], esi  (RESTAURE)     stw  r27, 0(r29)
#     cmp dword [rbx+0x22c], 0            lwz  r11, 0x1bc(r31)
#     mov esi, [rbx+0x5c]                 lwz  r27, 0x50(r31)
#     movzx r8d, byte [rbx+0x230]         lbz  r5,  0x1c0(r31)
#     call 0x1801A2D60  (deplaceur H)     bl   0x821FE770
#
# L'ecart vient de la taille des pointeurs : la borne est en 64 bits, la
# Xbox 360 en 32. Les champs ne sont pas aux memes offsets, mais ils sont
# dans le MEME ORDRE et jouent le MEME role.
CHAMPS = {
    'curseur vertical':    (0x58,  0x4C),
    'curseur horizontal':  (0x5C,  0x50),
    'compte vertical':     (0x224, 0x1B4),
    'bouclage vertical':   (0x228, 0x1B8),
    'compte horizontal':   (0x22C, 0x1BC),
    'bouclage horizontal': (0x230, 0x1C0),
    'sauter une trame':    (0x231, 0x1C1),
}

# Les deux repartiteurs jumeaux, et les deux deplaceurs.
REPARTITEUR = (0x1801BBBE0, 0x82217B30)
DEPLACEUR_V = (0x1801A2EC0, 0x821FE600)
DEPLACEUR_H = (0x1801A2D60, 0x821FE770)


class Refus(Exception):
    pass


class Image:
    def __init__(self, chemin=IMAGE):
        if not os.path.exists(chemin):
            raise Refus('%s absent -- lancez tools/x360_fs.cmd' % chemin)
        with open(chemin, 'rb') as fp:
            self.d = fp.read()
        e = struct.unpack_from('<I', self.d, 0x3C)[0]
        if self.d[e:e + 4] != b'PE\x00\x00':
            raise Refus('pas de signature PE')
        self.machine, n = struct.unpack_from('<HH', self.d, e + 4)
        taille_opt = struct.unpack_from('<H', self.d, e + 20)[0]
        self.base = struct.unpack_from('<I', self.d, e + 24 + 28)[0]
        s0 = e + 24 + taille_opt
        self.secs = []
        for k in range(n):
            s = self.d[s0 + 40 * k:s0 + 40 * (k + 1)]
            nom = s[:8].rstrip(b'\x00').decode('latin-1')
            vsize, rva, rsize, roff = struct.unpack_from('<IIII', s, 8)
            car = struct.unpack_from('<I', s, 36)[0]
            self.secs.append(dict(nom=nom, va=self.base + rva, vsize=vsize,
                                  exec=bool(car & 0x20000000)))
        # L'IMAGE EST DEJA TELLE QU'EN MEMOIRE : le decompresseur rend
        # l'image chargee, pas le fichier. L'offset vaut donc la RVA.
        self.md = capstone.Cs(capstone.CS_ARCH_PPC,
                              capstone.CS_MODE_32 | capstone.CS_MODE_BIG_ENDIAN)

    def off(self, va):
        o = va - self.base
        if not 0 <= o < len(self.d):
            raise Refus('VA 0x%X hors image' % va)
        return o

    def lire(self, va, n):
        o = self.off(va)
        return self.d[o:o + n]

    def section_de(self, va):
        for s in self.secs:
            if s['va'] <= va < s['va'] + s['vsize']:
                return s
        return None


def chaines(img, motif):
    """Les chaines ASCII qui contiennent `motif`, avec leur adresse."""
    m = motif.encode('latin-1')
    out = []
    i = 0
    while True:
        i = img.d.find(m, i)
        if i < 0:
            break
        # remonter au debut de la chaine
        j = i
        while j > 0 and 32 <= img.d[j - 1] < 127:
            j -= 1
        k = i
        while k < len(img.d) and 32 <= img.d[k] < 127:
            k += 1
        out.append((img.base + j, img.d[j:k].decode('latin-1')))
        i = k if k > i else i + 1
    # dedoublonner en gardant l'ordre
    vus, res = set(), []
    for va, s in out:
        if va not in vus:
            vus.add(va)
            res.append((va, s))
    return res


def constructeurs(img, cible, fenetre=12):
    """Les couples `lis`/`addi|ori` qui fabriquent `cible`.

    `fenetre` est le nombre d'instructions pendant lesquelles on accepte que
    le `addi` arrive apres le `lis`. Au-dela, et des que le registre est
    reecrit, on abandonne le couple : sinon on invente des references.
    """
    trouves = []
    for s in img.secs:
        if not s['exec']:
            continue
        deb = s['va']
        data = img.lire(deb, s['vsize'])
        n = len(data) // 4
        # on pre-decode une fois, c'est beaucoup plus rapide
        mots = struct.unpack('>%dI' % n, data[:n * 4])
        hauts = {}                   # registre -> (adresse, valeur<<16)
        for i, w in enumerate(mots):
            va = deb + 4 * i
            op = w >> 26
            rt = (w >> 21) & 31
            ra = (w >> 16) & 31
            imm = w & 0xFFFF
            if op == 15:                      # addis / lis
                base = (imm << 16) if ra == 0 else None
                if base is None:
                    hauts.pop(rt, None)
                else:
                    hauts[rt] = (va, base, i)
                continue
            if op == 14:                      # addi
                h = hauts.get(ra)
                if h is not None and i - h[2] <= fenetre:
                    bas = imm - 0x10000 if imm & 0x8000 else imm
                    if (h[1] + bas) & 0xFFFFFFFF == cible:
                        trouves.append((h[0], va))
                if rt != ra:
                    hauts.pop(rt, None)
                elif ra not in hauts:
                    hauts.pop(rt, None)
                continue
            if op == 24:                      # ori
                h = hauts.get(ra)
                if h is not None and i - h[2] <= fenetre:
                    if (h[1] | imm) == cible:
                        trouves.append((h[0], va))
                hauts.pop(rt, None)
                continue
            # toute autre ecriture du registre invalide le haut retenu
            if op in (31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43,
                      44, 45, 46, 47, 7, 8, 10, 11, 12, 13, 28, 29, 30, 21,
                      23, 20):
                hauts.pop(rt, None)
    return trouves


def rtti(img, filtre=None):
    """Les classes et leurs vtables, par la RTTI de MSVC.

    Disposition, en 32 bits et en GROS-BOUTISTE :

        TypeDescriptor        +0 vfptr  +4 libre  +8 le nom ".?AVFoo@@"
        CompleteObjectLocator +0 signature  +4 offset  +8 cdOffset
                              +12 -> TypeDescriptor  +16 -> ClassDescriptor
        vftable               [-1] -> CompleteObjectLocator, puis les
                              creneaux virtuels

    On remonte donc du NOM au descripteur (nom - 8), du descripteur au
    localisateur (une adresse qui le vise, moins 12), et du localisateur a la
    vtable (une adresse qui le vise, plus 4).
    """
    import re as _re
    noms = {}
    for m in _re.finditer(rb'\.\?AV([A-Za-z0-9_]{2,60})@@', img.d):
        noms[img.base + m.start() - 8] = m.group(1).decode('latin-1')

    # un index des mots de 32 bits gros-boutistes : valeur -> adresses
    n = len(img.d) // 4
    mots = struct.unpack('>%dI' % n, img.d[:n * 4])
    ou = {}
    for i, w in enumerate(mots):
        if 0x82000000 <= w < 0x83000000:
            ou.setdefault(w, []).append(img.base + 4 * i)

    out = []
    for td, nom in sorted(noms.items(), key=lambda kv: kv[1]):
        if filtre and filtre.lower() not in nom.lower():
            continue
        vt = []
        for a_col in ou.get(td, ()):
            col = a_col - 12
            for a_vt in ou.get(col, ()):
                vt.append(a_vt + 4)
        out.append((nom, td, sorted(set(vt))))
    return out


def desassembler(img, va, n=40):
    data = img.lire(va, n * 4)
    out = []
    for i in img.md.disasm(data, va):
        out.append((i.address, i.bytes.hex(), i.mnemonic, i.op_str))
    return out


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    img = Image()
    if a[0] == 'sections':
        print('machine 0x%X, base 0x%X, %d octets'
              % (img.machine, img.base, len(img.d)))
        for s in img.secs:
            print('  %-9s 0x%08X  0x%07X  %s'
                  % (s['nom'], s['va'], s['vsize'], 'code' if s['exec'] else ''))
        return 0
    if a[0] == 'chaines':
        for va, s in chaines(img, a[1]):
            print('0x%08X  %s' % (va, s))
        return 0
    if a[0] == 'carte':
        print('machine 0x%X, base 0x%X, %d octets'
              % (img.machine, img.base, len(img.d)))
        for sec in img.secs:
            print('  %-9s 0x%08X  0x%07X  %s'
                  % (sec['nom'], sec['va'], sec['vsize'],
                     'code' if sec['exec'] else ''))
        print()
        print('LES CHAMPS DU CURSEUR, mesures sur les deux repartiteurs')
        print('  %-22s %-10s %s' % ('role', 'borne', 'Xbox 360'))
        for role, (a_apm, a_360) in CHAMPS.items():
            print('  %-22s +0x%-7X +0x%X' % (role, a_apm, a_360))
        print()
        print('  repartiteur   borne 0x%X   X360 0x%X' % REPARTITEUR)
        print('  deplaceur V   borne 0x%X   X360 0x%X' % DEPLACEUR_V)
        print('  deplaceur H   borne 0x%X   X360 0x%X' % DEPLACEUR_H)
        print()
        t = rtti(img)
        print('%d types RTTI, dont %d avec une vtable'
              % (len(t), sum(1 for _, _, v in t if v)))
        return 0
    if a[0] == 'rtti':
        filtre = a[1] if len(a) > 1 else None
        for nom, td, vt in rtti(img, filtre):
            print('%-34s descripteur 0x%08X  vtable %s'
                  % (nom, td, ', '.join('0x%08X' % v for v in vt) or '(aucune)'))
        return 0
    if a[0] == 'vtable':
        va = int(a[1], 0)
        n = int(a[a.index('--max') + 1]) if '--max' in a else 20
        for k in range(n):
            f = struct.unpack('>I', img.lire(va + 4 * k, 4))[0]
            print('  [%2d] 0x%08X' % (k, f))
        return 0
    if a[0] == 'xref':
        cible = int(a[1], 0)
        t = constructeurs(img, cible)
        print('%d construction(s) de 0x%08X' % (len(t), cible))
        for lis, addi in t:
            print('  lis 0x%08X / addi 0x%08X' % (lis, addi))
        return 0
    if a[0] == 'func':
        va = int(a[1], 0)
        n = int(a[a.index('--max') + 1]) if '--max' in a else 40
        for adr, b, m, o in desassembler(img, va, n):
            print('0x%08X  %-10s %-10s %s' % (adr, b, m, o))
        return 0
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
