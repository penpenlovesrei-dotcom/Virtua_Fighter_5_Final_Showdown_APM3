#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Inventaire rapide de films `.sfd` : image, cadence, son -- sans tout lire.

L'en-tete de sequence MPEG est au tout debut du premier paquet video, et
l'en-tete ADX au debut du premier paquet audio : quelques megaoctets suffisent
donc a decrire un film de 230 Mo.

    py -3 tools/sfd_inventaire.py <dossier ou fichiers...>
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import sfd as mod_sfd                                          # noqa: E402
import usm_mux                                                 # noqa: E402


def decrire(chemin):
    video, audios = None, []
    for ident, charge, _ in mod_sfd.paquets(chemin):
        if 0xE0 <= ident <= 0xEF and video is None and charge[:4] == \
                b'\x00\x00\x01\xb3':
            video = charge
        elif 0xC0 <= ident <= 0xDF and charge[:2] == b'\x80\x00':
            audios.append(charge)
        elif 0xC0 <= ident <= 0xDF and charge[:4] == b'AIXF':
            audios.append(charge)
        if video is not None and audios:
            break
    if video is None:
        return None
    larg, haut, num, den = usm_mux.lire_sequence(video)
    sons = []
    for a in audios:
        if a[:4] == b'AIXF':
            sons.append('AIX multilingue')
        else:
            import struct
            voies = a[7]
            freq, = struct.unpack_from('>I', a, 8)
            total, = struct.unpack_from('>I', a, 0x0C)
            sons.append('ADX %d canaux %d Hz, %.1f s'
                        % (voies, freq, total / freq))
    return larg, haut, num / den, sons


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    fichiers = []
    for x in a:
        if os.path.isdir(x):
            fichiers += [os.path.join(x, f) for f in sorted(os.listdir(x))
                         if f.lower().endswith('.sfd')]
        else:
            fichiers.append(x)
    print('%-28s %13s  %-11s %-8s %s'
          % ('film', 'octets', 'image', 'cadence', 'son'))
    for f in fichiers:
        d = decrire(f)
        if d is None:
            print('%-28s %13d  (pas de flux video MPEG)'
                  % (os.path.basename(f), os.path.getsize(f)))
            continue
        larg, haut, fps, sons = d
        print('%-28s %13d  %-11s %-8s %s'
              % (os.path.basename(f), os.path.getsize(f),
                 '%dx%d' % (larg, haut), '%.3f/s' % fps,
                 ' + '.join(sons) or 'aucun'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
