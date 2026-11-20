# -*- coding: utf-8 -*-
"""Lire les signatures d'un DXBC embarque dans un conteneur GSVS.

Pour un nuanceur de SOMMETS, OSGN donne par element :
    Mask           les composantes DECLAREES
    ReadWriteMask  pour une SORTIE : les composantes JAMAIS ECRITES
donc une sortie declaree et non ecrite se lit sans desassembler.
"""
import struct
import sys

NOMS = {0: 'UNDEFINED', 1: 'POSITION', 2: 'CLIP_DISTANCE', 3: 'CULL_DISTANCE'}


def chunks(d, base):
    tot, chunk_count = struct.unpack_from('<II', d, base + 24)
    offs = struct.unpack_from('<%dI' % chunk_count, d, base + 32)
    out = {}
    for o in offs:
        nom = d[base + o:base + o + 4].decode('latin-1')
        taille, = struct.unpack_from('<I', d, base + o + 4)
        out.setdefault(nom, []).append((base + o + 8, taille))
    return out


def sig(d, deb, taille, titre):
    n, offs = struct.unpack_from('<II', d, deb)
    print('  %s : %d element(s)' % (titre, n))
    for i in range(n):
        (nm, idx, sv, ct, reg, mask, rwm, _z) = struct.unpack_from(
            '<IIIIIBBH', d, deb + 8 + i * 24)
        nom = d[deb + nm:d.index(b'\x00', deb + nm)].decode('latin-1')
        print('    %-16s idx=%d reg=%-3d mask=%X nonecrit/lu=%X  sysval=%s'
              % (nom, idx, reg, mask, rwm, NOMS.get(sv, sv)))


def main():
    for chemin in sys.argv[1:]:
        d = open(chemin, 'rb').read()
        base = d.find(b'DXBC')
        print('== %s  (DXBC a 0x%X, %d octets) ==' % (chemin, base, len(d)))
        c = chunks(d, base)
        print('  chunks :', ' '.join(sorted(c)))
        for nom, titre in (('ISGN', 'entrees'), ('OSGN', 'sorties'),
                           ('OSG5', 'sorties5')):
            for deb, taille in c.get(nom, []):
                sig(d, deb, taille, titre)
        for nom in ('SHDR', 'SHEX'):
            for deb, taille in c.get(nom, []):
                ver, = struct.unpack_from('<I', d, deb)
                dw, = struct.unpack_from('<I', d, deb + 4)
                print('  %s : version %08X, %d dwords' % (nom, ver, dw))
        print()


if __name__ == '__main__':
    main()
