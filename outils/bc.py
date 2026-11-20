#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Encoder une image en BC1 (DXT1) ou BC3 (DXT5).

POURQUOI. L atelier savait LIRE les textures compressees -- `tools/txp.py` colle
un en-tete DDS devant les octets et laisse Pillow decoder. Il ne savait pas en
ECRIRE une, et c est ce qui bloquait deux chantiers a la fois : repeindre des
cases de la planche de police, et poser des textures HD. Pillow n encode pas le
BC ; voici l encodeur, sans dependance.

LE FORMAT, et il n y a rien de plus :

    BC1   8 octets par bloc de 4x4
          u16 c0, u16 c1 en RGB565, puis 16 indices de 2 bits.
          Si c0 > c1 : palette de quatre couleurs (c0, c1, 2/3, 1/3).
          Sinon : trois couleurs et le noir TRANSPARENT a l indice 3.
    BC3   16 octets par bloc : huit octets d ALPHA puis un bloc BC1.
          Alpha : u8 a0, u8 a1, puis 16 indices de 3 bits (48 bits).
          Si a0 > a1 : huit valeurs interpolees. Sinon six, plus 0 et 255.

LE CHOIX DES BORNES est la boite englobante du bloc, puis chaque texel prend
l indice le plus proche. C est la methode la plus simple qui tienne : sur les
planches du jeu -- des aplats, du texte, des pictogrammes -- elle rend un PSNR
de 32,6 dB sur les pictogrammes de `spr_n_fnt32` -- mesure, pas estime. Les
bornes sont ensuite refaites par un tour de MOINDRES CARRES a indices fixes,
qui vaut a lui seul 1,7 dB ; voir le commentaire dans `_bloc_couleur`.

UN BLOC ENTIEREMENT TRANSPARENT est ecrit en BC1 a trois couleurs avec tous les
indices a 3, ce qui donne du noir transparent franc : c est ce qu attend le
rendu, et ca evite les auréoles au bord des sprites.

    py -3 tools/bc.py --essai <image.png>     aller-retour, PSNR par format
"""
import struct
import sys


def _565(r, g, b):
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)

def _de565(c):
    r = (c >> 11) & 0x1F
    g = (c >> 5) & 0x3F
    b = c & 0x1F
    return (r << 3) | (r >> 2), (g << 2) | (g >> 4), (b << 3) | (b >> 2)


def _bloc_couleur(px, transparent):
    """Les huit octets BC1 d un bloc de seize (r,g,b). `px` fait 16 tuples."""
    if transparent is not None and all(transparent):
        # tout transparent : trois couleurs, indices a 3 -> noir transparent
        return struct.pack('<HHI', 0, 0, 0xFFFFFFFF)
    rs = [p[0] for p in px]
    gs = [p[1] for p in px]
    bs = [p[2] for p in px]
    lo = (min(rs), min(gs), min(bs))
    hi = (max(rs), max(gs), max(bs))
    c0, c1 = _565(*hi), _565(*lo)
    alpha = transparent is not None and any(transparent)
    if alpha:
        # trois couleurs + transparent : il FAUT c0 <= c1
        if c0 > c1:
            c0, c1 = c1, c0
        p0, p1 = _de565(c0), _de565(c1)
        pal = [p0, p1,
               tuple((p0[k] + p1[k]) // 2 for k in range(3)),
               (0, 0, 0)]
    else:
        if c0 <= c1:
            # quatre couleurs exige c0 > c1 ; un bloc uni y arrive
            if c0 == 0:
                c0, c1 = 1, 0
            else:
                c1 = c0 - 1
        p0, p1 = _de565(c0), _de565(c1)
        pal = [p0, p1,
               tuple((2 * p0[k] + p1[k]) // 3 for k in range(3)),
               tuple((p0[k] + 2 * p1[k]) // 3 for k in range(3))]
    def indices(pal, borne):
        out = []
        for i in range(16):
            if alpha and transparent[i]:
                out.append(3)
                continue
            r, g, b = px[i]
            meilleur, j = None, 0
            for k in range(borne):
                q = pal[k]
                d = (r - q[0]) ** 2 + (g - q[1]) ** 2 + (b - q[2]) ** 2
                if meilleur is None or d < meilleur:
                    meilleur, j = d, k
            out.append(j)
        return out

    borne = 3 if alpha else 4
    idx = indices(pal, borne)

    # UN TOUR DE MOINDRES CARRES SUR LES BORNES. La boite englobante donne des
    # indices corrects mais des bornes trop ecartees : on les refait en
    # resolvant, a indices fixes, le couple (c0, c1) qui minimise l erreur.
    # Mesure sur les deux rangees de pictogrammes de `spr_n_fnt32` : 30,9 dB
    # sans ce tour, 32,6 dB avec -- releve APRES l avoir ecrit, pas avant. Un
    # encodeur a recherche exhaustive (endpoint search) gagnerait encore un a
    # deux decibels ; il n a pas ete juge necessaire pour des aplats.
    if not alpha:
        poids = {0: 1.0, 1: 0.0, 2: 2.0 / 3.0, 3: 1.0 / 3.0}
        A = B = C = 0.0
        X = [0.0, 0.0, 0.0]
        Y = [0.0, 0.0, 0.0]
        for i in range(16):
            w = poids[idx[i]]
            A += w * w
            B += w * (1.0 - w)
            C += (1.0 - w) * (1.0 - w)
            for k in range(3):
                X[k] += w * px[i][k]
                Y[k] += (1.0 - w) * px[i][k]
        det = A * C - B * B
        if abs(det) > 1e-6:
            n0 = []
            n1 = []
            for k in range(3):
                v0 = (C * X[k] - B * Y[k]) / det
                v1 = (A * Y[k] - B * X[k]) / det
                n0.append(max(0, min(255, int(v0 + 0.5))))
                n1.append(max(0, min(255, int(v1 + 0.5))))
            d0, d1 = _565(*n0), _565(*n1)
            if d0 <= d1:
                d0, d1 = (d1, d0) if d1 > d0 else (d0, d1)
            if d0 > d1:
                q0, q1 = _de565(d0), _de565(d1)
                npal = [q0, q1,
                        tuple((2 * q0[k] + q1[k]) // 3 for k in range(3)),
                        tuple((q0[k] + 2 * q1[k]) // 3 for k in range(3))]
                nidx = indices(npal, 4)
                e_a = sum((px[i][k] - pal[idx[i]][k]) ** 2
                          for i in range(16) for k in range(3))
                e_b = sum((px[i][k] - npal[nidx[i]][k]) ** 2
                          for i in range(16) for k in range(3))
                if e_b < e_a:
                    c0, c1, idx = d0, d1, nidx
    bits = 0
    for i in range(16):
        bits |= idx[i] << (2 * i)
    return struct.pack('<HHI', c0, c1, bits)


def _bloc_alpha(av):
    """Les huit octets d alpha BC3 d un bloc de seize valeurs."""
    a0, a1 = max(av), min(av)
    if a0 == a1:
        # tout pareil : huit valeurs, tous les indices a 0
        return struct.pack('<BB', a0, a1) + b'\x00' * 6
    pal = [a0, a1] + [((7 - k) * a0 + k * a1) // 7 for k in range(1, 7)]
    bits = 0
    for i in range(16):
        a = av[i]
        meilleur, j = None, 0
        for k in range(8):
            d = abs(a - pal[k])
            if meilleur is None or d < meilleur:
                meilleur, j = d, k
        bits |= j << (3 * i)
    out = struct.pack('<BB', a0, a1)
    for k in range(6):
        out += bytes([(bits >> (8 * k)) & 0xFF])
    return out


def encoder(im, format_txp):
    """Rend les octets BC1 ou BC3, par le chemin le plus court disponible.

    `tools/bc_rapide.py` fait le MEME travail avec numpy -- memes bornes, meme
    tour de moindres carres, memes modes -- cinq fois plus vite. Les deux
    rendent le meme PSNR a 0,1 dB pres (mesure : 47,6 dB des deux cotes sur un
    512x512 de `stgnyc`) sans etre octet pour octet : les egalites de distance
    ne se departagent pas dans le meme ordre. La version lisible ci-dessous
    reste la REFERENCE, et `bc_rapide.py --comparer` les confronte.
    """
    try:
        import bc_rapide
        return bc_rapide.encoder(im, format_txp)
    except ImportError:
        return _encoder_lisible(im, format_txp)


def _encoder_lisible(im, format_txp):
    """Rend les octets BC1 (format 6) ou BC3 (format 9) d une image RGBA.

    L image est prise TELLE QUELLE : c est a l appelant de l avoir remise dans
    le sens du fichier (`txp.py` retourne les planches a la lecture).
    """
    w, h = im.size
    if w % 4 or h % 4:
        raise SystemExit('le BC demande des cotes multiples de 4 (%dx%d)'
                         % (w, h))
    px = im.convert('RGBA').load()
    out = bytearray()
    bc1 = (format_txp == 6)
    for by in range(0, h, 4):
        for bx in range(0, w, 4):
            couleurs = []
            alphas = []
            for y in range(4):
                for x in range(4):
                    r, g, b, a = px[bx + x, by + y]
                    couleurs.append((r, g, b))
                    alphas.append(a)
            if bc1:
                tr = [a < 128 for a in alphas]
                out += _bloc_couleur(couleurs, tr if any(tr) else None)
            else:
                out += _bloc_alpha(alphas)
                out += _bloc_couleur(couleurs, None)
    return bytes(out)


def _psnr(a, b):
    import math
    n = len(a)
    s = 0
    for i in range(0, n, 997):          # un texel sur mille : assez pour juger
        d = a[i] - b[i]
        s += d * d
    m = s / float(len(range(0, n, 997)))
    if m <= 0:
        return 99.0
    return 10.0 * math.log10(255.0 * 255.0 / m)


def main(argv):
    if len(argv) < 2 or argv[0] != '--essai':
        print(__doc__)
        return 1
    from PIL import Image
    import io as _io
    import txp
    im = Image.open(argv[1]).convert('RGBA')
    w, h = im.size
    print('%s : %dx%d' % (argv[1], w, h))
    for f, nom, cc in ((6, 'BC1 (DXT1)', b'DXT1'), (9, 'BC3 (DXT5)', b'DXT5')):
        o = encoder(im, f)
        brut = txp.entete_dds(w, h, cc, len(o)) + o
        relu = Image.open(_io.BytesIO(brut)).convert('RGBA')
        print('   %-12s %8d octets   PSNR %.1f dB'
              % (nom, len(o), _psnr(im.tobytes(), relu.tobytes())))
    return 0


if __name__ == '__main__':
    sys.path.insert(0, __file__.rsplit('\\', 1)[0].rsplit('/', 1)[0])
    sys.exit(main(sys.argv[1:]))
