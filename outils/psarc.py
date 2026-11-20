#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lecteur d'archives PSARC (PlayStation Archive), version 1.4 / zlib.

Ecrit d'apres le format, sans outil tiers. C'est le dernier verrou sur le
chemin du menu console : les planches `aet_n_*` ne sont ni dans le dump APM3,
ni lisibles cote Xbox 360 (chaque fichier y est enferme dans un conteneur
compresse de magie `0F F5 12 ED`, dont le decompresseur vit dans un XEX
chiffre + LZX). Cote PS3, en revanche, tout est en clair -- il ne restait qu'a
ouvrir `USRDIR/rom.psarc`.

En-tete, gros-boutiste :

    0x00  'PSAR'
    0x04  version majeure (u16), mineure (u16)      -- ici 1.4
    0x08  compression, 4 octets                     -- 'zlib'
    0x0C  longueur totale de l'en-tete + sommaire
    0x10  taille d'une entree de sommaire           -- 0x1E
    0x14  nombre d'entrees
    0x18  taille de bloc                            -- 0x10000
    0x1C  drapeaux

Une entree de sommaire, 30 octets :

    0x00  empreinte MD5 du nom (16 o)
    0x10  index du premier bloc (u32)
    0x14  taille decompressee (40 bits)
    0x19  deplacement dans le fichier (40 bits)

Suit la table des tailles de blocs. **L'entree 0 est le manifeste** : la liste
des noms, une par ligne, compressee comme n'importe quel fichier. Les entrees
suivantes sont dans le meme ordre que ces noms.

Usage :
    py -3 tools/psarc.py lister <archive>
    py -3 tools/psarc.py extraire <archive> <dossier> --motif aet_n_
"""
import os
import struct
import sys
import zlib


def be(d, o, n):
    v = 0
    for i in range(n):
        v = (v << 8) | d[o + i]
    return v


class Psarc:
    def __init__(self, chemin):
        self.fp = open(chemin, 'rb')
        t = self.fp.read(32)
        if t[:4] != b'PSAR':
            raise ValueError('pas une archive PSARC : %r' % t[:4])
        self.maj, self.min = struct.unpack_from('>HH', t, 4)
        self.compression = t[8:12]
        self.toc_len, self.taille_entree, self.n, self.taille_bloc = \
            struct.unpack_from('>4I', t, 12)
        self.fp.seek(32)
        brut = self.fp.read(self.toc_len - 32)
        self.entrees = []
        for i in range(self.n):
            o = i * self.taille_entree
            self.entrees.append({
                'bloc0': be(brut, o + 0x10, 4),
                'taille': be(brut, o + 0x14, 5),
                'offset': be(brut, o + 0x19, 5),
            })
        reste = brut[self.n * self.taille_entree:]
        # largeur d'une taille de bloc : 2, 3 ou 4 octets selon la taille de bloc
        b, self.largeur = self.taille_bloc, 1
        while b > 0x100:
            b >>= 8
            self.largeur += 1
        nb = len(reste) // self.largeur
        self.blocs = [be(reste, k * self.largeur, self.largeur) for k in range(nb)]
        self.noms = self._manifeste()

    def _contenu(self, e):
        self.fp.seek(e['offset'])
        out = bytearray()
        k = e['bloc0']
        while len(out) < e['taille']:
            n = self.blocs[k]
            k += 1
            if n == 0:
                out += self.fp.read(self.taille_bloc)
                continue
            d = self.fp.read(n)
            if d[:1] == b'\x78':
                try:
                    out += zlib.decompress(d)
                except zlib.error:
                    out += d
            else:
                out += d
        return bytes(out[:e['taille']])

    def _manifeste(self):
        d = self._contenu(self.entrees[0])
        noms = [l.strip() for l in d.decode('latin-1').replace('\r', '\n').split('\n')]
        return [n for n in noms if n]

    def liste(self):
        out = []
        for i, e in enumerate(self.entrees[1:], start=1):
            nom = self.noms[i - 1] if i - 1 < len(self.noms) else '?%d' % i
            out.append((nom, e))
        return out

    def contenu(self, e):
        return self._contenu(e)


def main():
    argv = sys.argv[1:]
    if len(argv) < 2:
        print(__doc__)
        return 1
    action, arch = argv[0], argv[1]
    motifs = []
    if '--motif' in argv:
        motifs = [x.strip().lower() for x in argv[argv.index('--motif') + 1].split(',')]

    a = Psarc(arch)
    print('PSARC %d.%d  %s  %d entrees  blocs de 0x%X  (%d tailles de bloc, %d o chacune)'
          % (a.maj, a.min, a.compression.decode(), a.n, a.taille_bloc,
             len(a.blocs), a.largeur))
    liste = a.liste()
    if motifs:
        liste = [(n, e) for n, e in liste if any(m in n.lower() for m in motifs)]
    print('%d fichier(s)%s' % (len(liste), ' apres filtrage' if motifs else ''))

    if action == 'lister':
        for n, e in liste[:120]:
            print('  %-44s %9d o' % (n, e['taille']))
        return 0

    if action == 'extraire':
        dest = argv[2]
        for n, e in liste:
            p = os.path.join(dest, n.lstrip('/'))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            d = a.contenu(e)
            with open(p, 'wb') as fp:
                fp.write(d)
            print('  %-44s %9d o   %s' % (n, len(d),
                  'ok' if len(d) == e['taille'] else 'TAILLE INATTENDUE'))
        print('%d fichier(s) ecrit(s) dans %s' % (len(liste), dest))
        return 0

    print('action inconnue : %s' % action)
    return 1


if __name__ == '__main__':
    sys.exit(main())
