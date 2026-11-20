#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Lit un film CRI Sofdec1 (`.sfd`) : c'est un flux de programme MPEG.

Rien d'exotique : les `.sfd` de Sofdec1 sont des MPEG Program Stream ordinaires.
On y trouve, dans l'ordre des paquets :

    00 00 01 BA   en-tete de pack
    00 00 01 BB   en-tete systeme
    00 00 01 BE   bourrage (a jeter)
    00 00 01 Ex   video, flux elementaire MPEG-1 ou MPEG-2
    00 00 01 BD   « private stream 1 » : c'est la que CRI met son ADX

Chaque paquet autre que BA porte une longueur sur 16 bits, puis un en-tete PES
dont il faut sauter les octets de bourrage et l'horodatage.

    py -3 tools/sfd.py plan  <film.sfd>
    py -3 tools/sfd.py demux <film.sfd> <dossier>
"""
import os
import struct
import sys

PACK = b'\x00\x00\x01\xba'
FIN = b'\x00\x00\x01\xb9'


def _entete_pes(d, o):
    """Rend (debut_charge, fin_charge) pour le paquet PES a l'offset `o`."""
    lg, = struct.unpack_from('>H', d, o + 4)
    fin = o + 6 + lg
    p = o + 6
    if d[o + 3] in (0xBE, 0xBF):            # bourrage / donnees privees 2
        return p, fin
    if (d[p] & 0xC0) == 0x80:               # PES MPEG-2
        n_ext = d[p + 2]
        p += 3 + n_ext
    else:                                   # PES MPEG-1
        while p < fin and d[p] == 0xFF:
            p += 1
        if (d[p] & 0xC0) == 0x40:
            p += 2
        if (d[p] & 0xF0) == 0x20:
            p += 5
        elif (d[p] & 0xF0) == 0x30:
            p += 10
        else:
            p += 1
    return p, fin


def paquets(chemin):
    """Parcourt le fichier par blocs et rend (identifiant, octets) par paquet."""
    BLOC = 8 << 20
    reste = b''
    base = 0
    with open(chemin, 'rb') as fp:
        while True:
            bloc = fp.read(BLOC)
            if not bloc:
                break
            d = reste + bloc
            o = 0
            while True:
                if o + 32 > len(d):
                    break
                if d[o:o + 3] != b'\x00\x00\x01':
                    o += 1
                    continue
                ident = d[o + 3]
                if d[o:o + 4] == PACK:
                    # MPEG-2 : 14 octets + bourrage (3 bits du 14e) ;
                    # MPEG-1 : 12 octets, sans bourrage. Les deux premiers
                    # bits du 5e octet tranchent (01 = MPEG-2).
                    if (d[o + 4] & 0xC0) == 0x40:
                        o += 14 + (d[o + 13] & 7)
                    else:
                        o += 12
                    continue
                if d[o:o + 4] == FIN:
                    o += 4
                    continue
                lg, = struct.unpack_from('>H', d, o + 4)
                if o + 6 + lg > len(d):
                    break
                deb, fin = _entete_pes(d, o)
                yield ident, d[deb:fin], base + o
                o = o + 6 + lg
            reste = d[o:]
            base += o


def cmd_plan(chemin):
    compte, octets, exemples = {}, {}, {}
    for ident, charge, _ in paquets(chemin):
        compte[ident] = compte.get(ident, 0) + 1
        octets[ident] = octets.get(ident, 0) + len(charge)
        if ident not in exemples:
            exemples[ident] = charge[:16]
    print('%s   %d octets' % (os.path.basename(chemin),
                              os.path.getsize(chemin)))
    print('\n%-6s %-26s %10s %14s  %s'
          % ('id', 'flux', 'paquets', 'octets', 'debut du premier'))
    for ident in sorted(compte):
        nom = ('video MPEG' if 0xE0 <= ident <= 0xEF else
               'audio MPEG' if 0xC0 <= ident <= 0xDF else
               'private stream 1' if ident == 0xBD else
               'private stream 2' if ident == 0xBF else
               'bourrage' if ident == 0xBE else
               'entete systeme' if ident == 0xBB else '?')
        print('0x%02X   %-26s %10d %14d  %s'
              % (ident, nom, compte[ident], octets[ident],
                 exemples[ident].hex(' ')))
    return 0


def cmd_demux(chemin, dossier):
    os.makedirs(dossier, exist_ok=True)
    base = os.path.splitext(os.path.basename(chemin))[0]
    sorties = {}
    for ident, charge, _ in paquets(chemin):
        if ident in (0xBE, 0xBB, 0xBF):
            continue
        if ident not in sorties:
            ext = 'm2v' if 0xE0 <= ident <= 0xEF else 'bin'
            nom = '%s_%02X.%s' % (base, ident, ext)
            sorties[ident] = open(os.path.join(dossier, nom), 'wb')
            print('-> %s' % nom)
        sorties[ident].write(charge)
    for f in sorties.values():
        f.close()
    return 0


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        print(__doc__)
        return 1
    if a[0] == 'plan':
        return cmd_plan(a[1])
    if a[0] == 'demux':
        return cmd_demux(a[1], a[2] if len(a) > 2 else '.')
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
