#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mesurer le PAS DE LIGNE de la planche de police, au lieu de le deviner.

Trois essais de disposition ont echoue a l'ecran. On arrete de regler a la
vue : une planche de caracteres est une image, et une image a une periodicite
verticale forte. On la mesure par autocorrelation sur les octets bruts.

    score(P) = nombre d'octets egaux entre data[i] et data[i+P]

Le vrai pas de ligne (en octets) sort en tete, et ses multiples aussi -- c'est
la signature qui confirme. On imprime aussi le pas de CELLULE (hauteur d'une
case de caracteres), qui doit etre un multiple entier du pas de ligne.

    py -3 tools/mesurer_atlas.py
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
ATLAS = os.path.join(RACINE, 'extracted', 'font_gothic.bin')
CARTE = os.path.join(RACINE, 'extracted', 'fontmap.bin')


def autocorr(data, deb, n, pas):
    """Nombre d'octets identiques entre data[deb:deb+n] et data[deb+pas:...]."""
    a = data[deb:deb + n]
    b = data[deb + pas:deb + pas + n]
    if len(b) < n:
        return 0.0
    return sum(1 for x, y in zip(a, b) if x == y) / float(n)


def main():
    data = open(ATLAS, 'rb').read()
    print('planche : %s octets' % len(data))
    vals = sorted(set(data))
    print('valeurs distinctes : %d -> %s'
          % (len(vals), ' '.join('%02X' % v for v in vals)))
    print()

    # On mesure loin du debut : les premieres cases d'une planche sont souvent
    # vides, et du vide s'auto-correle parfaitement a TOUS les pas.
    # On cherche une zone dense (beaucoup d'octets non nuls).
    BLOC = 65536
    meilleure, densite_max = 0, -1.0
    for deb in range(0, len(data) - BLOC, BLOC):
        d = sum(1 for v in data[deb:deb + BLOC] if v) / float(BLOC)
        # on veut de l'encre, mais pas du plein : entre 15 % et 60 %
        if 0.15 < d < 0.60 and d > densite_max:
            densite_max, meilleure = d, deb
    print('zone de mesure : offset 0x%X, densite %.1f %% d\'encre'
          % (meilleure, densite_max * 100))
    print()

    N = 32768
    scores = []
    for pas in range(8, 8193):
        scores.append((autocorr(data, meilleure, N, pas), pas))
    scores.sort(reverse=True)

    print('MEILLEURS PAS (autocorrelation) :')
    for s, p in scores[:25]:
        print('   pas %5d octets   %.4f' % (p, s))
    print()

    # Le plus petit pas fortement correle est le pas de ligne.
    seuil = scores[0][0] * 0.97
    forts = sorted(p for s, p in scores if s >= seuil)
    print('pas >= 97 %% du meilleur : %s' % forts[:20])
    if forts:
        base = forts[0]
        print()
        print('PAS DE LIGNE retenu : %d octets' % base)
        multiples = [p for p in forts if p % base == 0]
        print('   ses multiples presents : %s' % multiples[:12])
        if len(data) % base == 0:
            print('   la planche fait %d lignes (%d %% %d == 0) OK'
                  % (len(data) // base, len(data), base))
        else:
            print('   ATTENTION : %d n\'est pas multiple de %d'
                  % (len(data), base))

    print()
    print('--- carte fontmap.bin ---')
    c = open(CARTE, 'rb').read()
    print('entete : %s' % ' '.join('%02X' % v for v in c[:64]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
