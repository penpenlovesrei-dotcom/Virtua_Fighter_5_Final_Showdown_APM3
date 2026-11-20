#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Le mode Quest de VF5 Xbox 360 (2007), MESURE dans son executable.

Entree : l'image PE sortie par `tools/xex.py` (PowerPC gros-boutien, base
0x82000000). Rien n'est suppose : les classes viennent du RTTI, les bornes
des fonctions de `.pdata`, les appels du desassembleur.

  1. les CLASSES : chaque `.?AV<nom>@@` -> son CompleteObjectLocator (dont
     le champ +0x0C pointe le TypeDescriptor) -> la vtable (le mot qui suit
     un pointeur vers le COL) -> ses methodes ;
  2. les FONCTIONS : `.pdata` Xbox 360 = {debut, mot} ; longueur = bits 8-29
     du mot, en instructions ;
  3. le GRAPHE : chaque `bl` d'une fonction vers le debut d'une autre ;
  4. le code PROPRE a un ensemble de classes : leurs methodes, plus toute
     fonction dont TOUS les appelants sont deja dans l'ensemble (clos).

    py -3 tools/quest_x360.py [image]      le bilan du mode Quest
"""
import collections
import os
import re
import struct
import sys

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
IMAGE = os.path.join(RACINE, 'extracted', 'X360_VF5', 'vf5_x360.img')
BASE = 0x82000000

MOTIF_QUEST = re.compile(r'Quest|Tenpo|Tournament|ItemShop|GameRank|Emblem|'
                         r'NewItem|GameItemFight|RankingUpdate')


class Image(object):
    def __init__(self, chemin=IMAGE):
        self.d = open(chemin, 'rb').read()
        e = struct.unpack_from('<I', self.d, 0x3C)[0]
        n = struct.unpack_from('<H', self.d, e + 6)[0]
        t = struct.unpack_from('<H', self.d, e + 20)[0]
        self.sections = {}
        for k in range(n):
            s = self.d[e + 24 + t + 40 * k:e + 24 + t + 40 * (k + 1)]
            nom = s[:8].rstrip(b'\x00').decode('latin-1')
            vs, va = struct.unpack_from('<II', s, 8)
            self.sections[nom] = (BASE + va, vs)

    def u32(self, va):
        return struct.unpack_from('>I', self.d, va - BASE)[0]

    def dans(self, va, nom):
        a, n = self.sections[nom]
        return a <= va < a + n

    def fonctions(self):
        a, n = self.sections['.pdata']
        out = []
        for k in range(n // 8):
            debut, mot = struct.unpack_from('>II', self.d, a - BASE + 8 * k)
            if debut == 0:
                continue
            out.append((debut, ((mot >> 8) & 0x3FFFFF) * 4))
        return sorted(out)

    def classes(self):
        """{nom: [adresses de vtable]} par le RTTI."""
        d = self.d
        tds = {}
        for m in re.finditer(rb'\.\?AV(\w+)@@', d):
            tds[BASE + m.start() - 8] = m.group(1).decode()
        # COL : {0, decalage, cd, TypeDescriptor, hierarchie}, 32 bits BE
        cols = {}
        a_rd, n_rd = self.sections['.rdata']
        for off in range(a_rd - BASE, a_rd - BASE + n_rd - 20, 4):
            sig, dec, cd, td = struct.unpack_from('>IIII', d, off)
            if sig == 0 and td in tds and dec < 0x10000:
                cols[BASE + off] = tds[td]
        out = collections.defaultdict(list)
        for off in range(a_rd - BASE, a_rd - BASE + n_rd - 4, 4):
            p = struct.unpack_from('>I', d, off)[0]
            if p in cols:
                out[cols[p]].append(BASE + off + 4)
        return out

    def methodes(self, vt, debuts):
        out = []
        va = vt
        while True:
            p = self.u32(va)
            if p not in debuts:
                break
            out.append(p)
            va += 4
        return out


def graphe(img, fonctions):
    md = capstone.Cs(capstone.CS_ARCH_PPC,
                     capstone.CS_MODE_32 | capstone.CS_MODE_BIG_ENDIAN)
    debuts = set(f for f, _ in fonctions)
    appels = collections.defaultdict(set)
    appelants = collections.defaultdict(set)
    for f, n in fonctions:
        code = img.d[f - BASE:f - BASE + n]
        for k in range(0, len(code), 4):
            w = struct.unpack_from('>I', code, k)[0]
            if w >> 26 == 18 and (w & 2) == 0:     # bl, ou b de fin (saut)
                dep = w & 0x3FFFFFC
                if dep & 0x2000000:
                    dep -= 0x4000000
                cible = f + k + dep
                # un `b` vers le debut d'une AUTRE fonction est un appel
                # terminal ; vers la fonction elle-meme, une boucle
                if cible in debuts and (w & 1 or cible != f):
                    appels[f].add(cible)
                    appelants[cible].add(f)
    return appels, appelants


def references(img, fonctions):
    """{adresse: [(fonction, instruction)]} : les adresses construites par
    `lis rX, hi` puis `addi`/`ori`/chargement/rangement sur rX. Le suivi
    des registres est remis a zero a chaque fonction (et a chaque `bl`,
    qui ecrase les volatils r0, r3-r12)."""
    refs = collections.defaultdict(list)
    OPS = {14: 'addi', 24: 'ori', 32: 'lwz', 34: 'lbz', 40: 'lhz', 42: 'lha',
           36: 'stw', 38: 'stb', 44: 'sth', 48: 'lfs', 50: 'lfd', 52: 'stfs',
           54: 'stfd'}
    for f, n in fonctions:
        hi = {}
        for k in range(0, n, 4):
            a = f + k
            w = struct.unpack_from('>I', img.d, a - BASE)[0]
            op = w >> 26
            rd, ra = (w >> 21) & 31, (w >> 16) & 31
            imm = w & 0xFFFF
            if op == 15 and ra == 0:                       # lis rd, imm
                hi[rd] = imm << 16
                continue
            if op in OPS:
                base_r = ra if op != 24 else (w >> 21) & 31
                if base_r in hi:
                    lo = imm if op == 24 else (imm - 0x10000 if imm & 0x8000
                                               else imm)
                    refs[(hi[base_r] + lo) & 0xFFFFFFFF].append((f, a))
                if op in (14, 24):
                    cible = rd if op == 14 else ra
                    hi.pop(cible, None)
                elif op in (32, 34, 40, 42):
                    hi.pop(rd, None)
                continue
            if op == 18 and (w & 1):                        # bl
                for r in (0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
                    hi.pop(r, None)
    return refs


def propre(racines, appels, appelants):
    ens = set(racines)
    change = True
    while change:
        change = False
        for f in list(ens):
            for c in appels.get(f, ()):
                if c not in ens and appelants[c] and appelants[c] <= ens:
                    ens.add(c)
                    change = True
    return ens


def chercher_chaine(img, fonctions, motif):
    refs = references(img, fonctions)
    for m in re.finditer(motif.encode(), img.d):
        va = BASE + m.start()
        # remonter au debut de la chaine
        debut = va
        while img.d[debut - BASE - 1] not in (0,):
            debut -= 1
        fin = img.d.index(b'\x00', va - BASE)
        texte = img.d[debut - BASE:fin].decode('latin-1')
        qui = refs.get(debut, [])
        print('0x%08X %-40s %s' % (debut, texte[:40], ' '.join(
            '%08X@%08X' % (f, a) for f, a in qui[:6]) or '(aucune ref)'))


def main():
    if '--methodes' in sys.argv:
        # les vtables et methodes des classes du mode, une ligne par classe
        img = Image()
        debuts = set(f for f, _ in img.fonctions())
        cls = img.classes()
        for c in sorted(c for c in cls if MOTIF_QUEST.search(c)):
            for vt in cls[c]:
                print('%-28s vt 0x%08X  %s' % (c, vt, ' '.join(
                    '0x%08X' % m for m in img.methodes(vt, debuts))))
        return 0
    if '--chaine' in sys.argv:
        img = Image()
        chercher_chaine(img, img.fonctions(),
                        sys.argv[sys.argv.index('--chaine') + 1])
        return 0
    img = Image(sys.argv[1] if len(sys.argv) > 1 else IMAGE)
    fonctions = img.fonctions()
    taille = dict(fonctions)
    debuts = set(taille)
    print('%d fonctions dans .pdata, %d octets de code'
          % (len(fonctions), sum(taille.values())))
    cls = img.classes()
    appels, appelants = graphe(img, fonctions)
    quest = sorted(c for c in cls if MOTIF_QUEST.search(c))
    racines = set()
    print('\n%-30s %4s %6s' % ('classe', 'meth', 'octets'))
    for c in quest:
        m = set()
        for vt in cls[c]:
            m |= set(img.methodes(vt, debuts))
        racines |= m
        print('%-30s %4d %6d' % (c, len(m), sum(taille[x] for x in m)))
    ens0 = propre(racines, appels, appelants)
    # le MODE 0x13 et ses neuf sous-etats (tables 0x8201C9B8 et 0x8201CC90,
    # gestionnaires relus a la main le 2026-09-11), plus les deux rappels du
    # combat inscrits par QUEST_VS ; les bouchons 0x82143740/48 exclus
    mode = {0x823002D8, 0x82300360}
    ss = 0x8201CC90
    for i in range(0x51, 0x5A):
        e = ss + 0x14 * i
        mode |= {img.u32(e + 4 * k) for k in (2, 3, 4)}
    mode |= {0x82320A68, 0x8231FAE0}
    mode = {m for m in mode if m in debuts and m not in (0x82143740,
                                                         0x82143748)}
    # 0x822FCBE0 (entree de 0x59) sert aussi a 0x6C : il n'est pas au mode
    mode.discard(0x822FCBE0)
    racines |= mode
    ens = propre(racines, appels, appelants)
    octets = sum(taille[f] for f in ens)
    print('\ncode propre aux seules classes : %d fonctions, %d octets'
          % (len(ens0), sum(taille[f] for f in ens0)))
    print('CODE PROPRE au mode Quest (classes + mode 0x13 et ses sous-etats '
          '+ rappels du combat, et tout ce qu ils sont seuls a appeler) : '
          '%d fonctions, %d octets, ~%d instructions'
          % (len(ens), octets, octets // 4))
    # ce que le mode appelle HORS de lui : le socle partage
    dehors = set()
    for f in ens:
        dehors |= appels.get(f, set()) - ens
    print('fonctions PARTAGEES appelees par le mode : %d (%d octets)'
          % (len(dehors), sum(taille[f] for f in dehors)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
