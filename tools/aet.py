#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lecteur de planches AET -- scenes, compositions, calques.

Le format AET est celui de Project DIVA, **et il est explicitement partage par
Virtua Fighter 5**. Structure reprise de `AetPlugin` (samyuu),
`src/comfy/file_format_aet_set.cpp`, lu et non execute :
https://github.com/samyuu/AetPlugin

Pourquoi ce lecteur. La grille de selection de la borne est une SEULE scene,
`SEL_CHARA`, dont les cases sont des calques. La table en memoire compte vingt
cases dont Dural, la planche contient ses calques -- mais elle ne s'affiche
pas. Reste une question que seul le fichier peut trancher : **la composition
place-t-elle vingt cases, ou dix-neuf ?**

Disposition, pointeurs 32 bits :

    fichier   suite de pointeurs de scenes, terminee par un zero

    scene     +0x00 nom (ptr)        +0x04 debut  +0x08 fin  +0x0C cadence
              +0x10 couleur de fond  +0x14 resolution (2 x i32)
              +0x1C camera (ptr)
              +0x20 nb compositions  +0x24 compositions (ptr)
              +0x28 nb videos        +0x2C videos (ptr)
              +0x30 nb audios        +0x34 audios (ptr)

    compo     +0x00 nb calques       +0x04 calques (ptr)     -- 8 octets
              la DERNIERE composition est la racine

    calque    +0x00 nom (ptr)   +0x04 debut  +0x08 fin  +0x0C decalage
              +0x10 echelle de temps  +0x14 drapeaux (u16)
              +0x16 qualite (u8)      +0x17 type (u8)
              +0x18 element (ptr)     +0x1C parent (ptr)
              +0x20 nb marqueurs      +0x24 marqueurs (ptr)
              +0x28 video (ptr)       +0x2C audio (ptr)      -- 48 octets

Usage :
    py -3 tools/aet.py <fichier.bin>              la liste des scenes
    py -3 tools/aet.py <fichier.bin> <scene>      les calques d'une scene
"""
import struct
import sys

TAILLE_CALQUE = 0x30
TYPES = {0: 'aucun', 1: 'video', 2: 'audio', 3: 'composition'}


class Aet:
    def __init__(self, chemin):
        with open(chemin, 'rb') as fp:
            self.d = fp.read()

    def u32(self, o):
        return struct.unpack_from('<I', self.d, o)[0]

    def f32(self, o):
        return struct.unpack_from('<f', self.d, o)[0]

    def chaine(self, o):
        if not o or o >= len(self.d):
            return ''
        fin = self.d.index(b'\0', o)
        return self.d[o:fin].decode('latin-1')

    def scenes(self):
        out = []
        o = 0
        while True:
            p = self.u32(o)
            if p == 0:
                break
            out.append(p)
            o += 4
        return out

    def scene(self, p):
        return dict(
            offset=p,
            nom=self.chaine(self.u32(p)),
            debut=self.f32(p + 4), fin=self.f32(p + 8),
            cadence=self.f32(p + 0xC),
            resolution=(self.u32(p + 0x14), self.u32(p + 0x18)),
            n_compo=self.u32(p + 0x20), compos=self.u32(p + 0x24),
            n_video=self.u32(p + 0x28),
            n_audio=self.u32(p + 0x30))

    def compositions(self, sc):
        out = []
        for i in range(sc['n_compo']):
            o = sc['compos'] + 8 * i
            out.append((self.u32(o), self.u32(o + 4)))
        return out

    def calques(self, n, p):
        out = []
        for i in range(n):
            o = p + TAILLE_CALQUE * i
            if o + TAILLE_CALQUE > len(self.d):
                break
            out.append(dict(
                nom=self.chaine(self.u32(o)),
                debut=self.f32(o + 4), fin=self.f32(o + 8),
                type=self.d[o + 0x17],
                element=self.u32(o + 0x18),
                parent=self.u32(o + 0x1C)))
        return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    a = Aet(sys.argv[1])
    ps = a.scenes()
    print('%d scene(s)' % len(ps))
    cible = sys.argv[2] if len(sys.argv) > 2 else None
    for p in ps:
        sc = a.scene(p)
        print('  scene "%s"  %d composition(s), %d video(s), %.0f images/s, %dx%d'
              % (sc['nom'], sc['n_compo'], sc['n_video'], sc['cadence'],
                 sc['resolution'][0], sc['resolution'][1]))
        if cible and cible.lower() not in sc['nom'].lower():
            continue
        compos = a.compositions(sc)
        for i, (n, ptr) in enumerate(compos):
            racine = ' (RACINE)' if i == len(compos) - 1 else ''
            if not cible and not racine:
                continue
            print('     composition %d%s : %d calque(s)' % (i, racine, n))
            for k, c in enumerate(a.calques(n, ptr)):
                print('        %3d  %-34s %-12s %.0f-%.0f'
                      % (k, c['nom'], TYPES.get(c['type'], '?%d' % c['type']),
                         c['debut'], c['fin']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
