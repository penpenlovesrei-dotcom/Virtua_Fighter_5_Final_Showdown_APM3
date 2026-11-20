#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L encodeur BC1/BC3, mais VECTORISE -- le meme resultat, cent fois plus vite.

POURQUOI. `tools/bc.py` encode bloc par bloc, en Python : lisible, et c est ce
qu il fallait pour etablir le format. Mais une texture de decor fait
2048 x 2048, et une version HD 4096 x 4096 -- un MILLION de blocs pour le seul
niveau zero, plus les douze niveaux de mip. En Python pur cela se compte en
minutes par texture ; il y en a 332 dans `stgnyc`.

CE FICHIER NE CHANGE NI LE FORMAT NI LA METHODE : memes bornes par boite
englobante, meme tour de moindres carres, memes regles de mode. Il fait
seulement tout d un coup, avec numpy. `bc.encoder` s en sert quand numpy est
la, et retombe sur la version lisible sinon -- laquelle reste la REFERENCE :
`--comparer` confronte les deux sur une image et refuse tout ecart de PSNR.

    py -3 tools/bc_rapide.py --comparer <image.png>
"""
import struct
import sys


def _q565(c):
    """Quantifie un (N,3) en u16 565, et rend aussi la couleur reconstruite."""
    import numpy as np
    r = (c[..., 0] >> 3).astype(np.uint32)
    g = (c[..., 1] >> 2).astype(np.uint32)
    b = (c[..., 2] >> 3).astype(np.uint32)
    v = (r << 11) | (g << 5) | b
    rr = (r << 3) | (r >> 2)
    gg = (g << 2) | (g >> 4)
    bb = (b << 3) | (b >> 2)
    return v, np.stack([rr, gg, bb], axis=-1).astype(np.int32)


def _de565(v):
    import numpy as np
    r = (v >> 11) & 0x1F
    g = (v >> 5) & 0x3F
    b = v & 0x1F
    return np.stack([(r << 3) | (r >> 2), (g << 2) | (g >> 4),
                     (b << 3) | (b >> 2)], axis=-1).astype(np.int32)


def _indices(rgb, pal, borne):
    """rgb (N,16,3), pal (N,4,3) -> indices (N,16), parmi les `borne` premiers."""
    import numpy as np
    d = rgb[:, :, None, :] - pal[:, None, :borne, :]
    return (d * d).sum(-1).argmin(-1).astype(np.uint32)


def _palette(c0v, c1v, trois):
    """Les quatre couleurs, en mode 4 couleurs ou 3 + transparent."""
    import numpy as np
    p0, p1 = _de565(c0v), _de565(c1v)
    if trois:
        p2 = (p0 + p1) // 2
        p3 = np.zeros_like(p0)
    else:
        p2 = (2 * p0 + p1) // 3
        p3 = (p0 + 2 * p1) // 3
    return np.stack([p0, p1, p2, p3], axis=1)


def _blocs_couleur(rgb, tr):
    """(N,16,3) et (N,16) booleen -> (N,) c0, (N,) c1, (N,) bits."""
    import numpy as np
    n = rgb.shape[0]
    alpha = tr.any(1)                       # les blocs a trois couleurs
    hi = rgb.max(1)
    lo = rgb.min(1)
    c0v, _ = _q565(hi)
    c1v, _ = _q565(lo)

    # MODE 4 COULEURS : il faut c0 > c1. Un bloc uni donne c0 == c1 ; on
    # descend c1 d un cran, comme la version lisible.
    egal = (c0v <= c1v) & ~alpha
    c1v = np.where(egal & (c0v > 0), c0v - 1, c1v)
    c0v = np.where(egal & (c0v == 0), np.uint32(1), c0v)
    # MODE 3 COULEURS : il faut c0 <= c1 ; on echange au besoin.
    ech = alpha & (c0v > c1v)
    c0v, c1v = (np.where(ech, c1v, c0v), np.where(ech, c0v, c1v))

    pal4 = _palette(c0v, c1v, False)
    pal3 = _palette(c0v, c1v, True)
    idx = np.where(alpha[:, None],
                   _indices(rgb, pal3, 3), _indices(rgb, pal4, 4))
    idx = np.where(tr, np.uint32(3), idx)

    # UN TOUR DE MOINDRES CARRES, et seulement sur les blocs a quatre
    # couleurs -- exactement comme la version lisible.
    m = ~alpha
    if m.any():
        poids = np.array([1.0, 0.0, 2.0 / 3.0, 1.0 / 3.0])
        wv = poids[idx[m]]                              # (M,16)
        pm = rgb[m].astype(np.float64)
        A = (wv * wv).sum(1)
        B = (wv * (1.0 - wv)).sum(1)
        C = ((1.0 - wv) * (1.0 - wv)).sum(1)
        X = (wv[..., None] * pm).sum(1)                 # (M,3)
        Y = ((1.0 - wv)[..., None] * pm).sum(1)
        det = A * C - B * B
        ok = np.abs(det) > 1e-6
        n0 = np.clip((C[:, None] * X - B[:, None] * Y)
                     / np.where(det, det, 1.0)[:, None] + 0.5, 0, 255)
        n1 = np.clip((A[:, None] * Y - B[:, None] * X)
                     / np.where(det, det, 1.0)[:, None] + 0.5, 0, 255)
        d0v, _ = _q565(n0.astype(np.int32))
        d1v, _ = _q565(n1.astype(np.int32))
        ech2 = d0v < d1v
        d0v, d1v = (np.where(ech2, d1v, d0v), np.where(ech2, d0v, d1v))
        ok &= (d0v > d1v)
        npal = _palette(d0v, d1v, False)
        nidx = _indices(pm.astype(np.int32), npal, 4)
        # on ne garde le nouveau couple que s il fait MIEUX
        def err(p, i):
            q = np.take_along_axis(p, i[:, :, None].astype(np.intp), axis=1) \
                if False else p[np.arange(p.shape[0])[:, None], i.astype(np.intp)]
            d = pm.astype(np.int32) - q
            return (d * d).sum((1, 2))
        mieux = ok & (err(npal, nidx) < err(pal4[m], idx[m]))
        c0m, c1m, im_ = c0v[m].copy(), c1v[m].copy(), idx[m].copy()
        c0m[mieux] = d0v[mieux]
        c1m[mieux] = d1v[mieux]
        im_[mieux] = nidx[mieux]
        c0v[m], c1v[m], idx[m] = c0m, c1m, im_

    bits = np.zeros(n, dtype=np.uint32)
    for i in range(16):
        bits |= (idx[:, i] & 3) << np.uint32(2 * i)
    return c0v.astype(np.uint16), c1v.astype(np.uint16), bits


def _blocs_alpha(av):
    """(N,16) -> (N,8) octets d alpha BC3."""
    import numpy as np
    n = av.shape[0]
    a0 = av.max(1).astype(np.int32)
    a1 = av.min(1).astype(np.int32)
    pal = [a0, a1] + [((7 - k) * a0 + k * a1) // 7 for k in range(1, 7)]
    pal = np.stack(pal, axis=1)                          # (N,8)
    d = np.abs(av[:, :, None].astype(np.int32) - pal[:, None, :])
    idx = d.argmin(-1).astype(np.uint64)
    idx = np.where((a0 == a1)[:, None], np.uint64(0), idx)
    bits = np.zeros(n, dtype=np.uint64)
    for i in range(16):
        bits |= (idx[:, i] & np.uint64(7)) << np.uint64(3 * i)
    out = np.zeros((n, 8), dtype=np.uint8)
    out[:, 0] = a0.astype(np.uint8)
    out[:, 1] = a1.astype(np.uint8)
    for k in range(6):
        out[:, 2 + k] = ((bits >> np.uint64(8 * k)) & np.uint64(0xFF)).astype(
            np.uint8)
    return out


def encoder(im, format_txp):
    import numpy as np
    w, h = im.size
    if w % 4 or h % 4:
        raise SystemExit('le BC demande des cotes multiples de 4 (%dx%d)'
                         % (w, h))
    a = np.asarray(im.convert('RGBA'), dtype=np.int32)
    bh, bw = h // 4, w // 4
    b = a.reshape(bh, 4, bw, 4, 4).transpose(0, 2, 1, 3, 4).reshape(-1, 16, 4)
    rgb = b[..., :3]
    al = b[..., 3].astype(np.uint8)
    bc1 = (format_txp == 6)
    tr = (al < 128) if bc1 else np.zeros(al.shape, dtype=bool)
    c0, c1, bits = _blocs_couleur(rgb, tr)
    coul = np.zeros(c0.shape[0], dtype=[('c0', '<u2'), ('c1', '<u2'),
                                        ('bits', '<u4')])
    coul['c0'], coul['c1'], coul['bits'] = c0, c1, bits
    coul = coul.view(np.uint8).reshape(-1, 8)
    if bc1:
        return coul.tobytes()
    return np.concatenate([_blocs_alpha(al), coul], axis=1).tobytes()


def main(argv):
    if len(argv) < 2 or argv[0] != '--comparer':
        print(__doc__)
        return 1
    import math
    from PIL import Image
    import io as _io
    sys.path.insert(0, __file__.replace(chr(92), '/').rsplit('/', 1)[0])
    import bc as lent
    import txp
    im = Image.open(argv[1]).convert('RGBA')
    w, h = im.size
    print('%s : %dx%d' % (argv[1], w, h))
    for f, cc, nom in ((6, b'DXT1', 'BC1'), (9, b'DXT5', 'BC3')):
        import time
        t0 = time.time()
        a = lent._encoder_lisible(im, f) if hasattr(lent, '_encoder_lisible') \
            else lent.encoder(im, f)
        t1 = time.time()
        b = encoder(im, f)
        t2 = time.time()

        def psnr(oct_):
            brut = txp.entete_dds(w, h, cc, len(oct_)) + oct_
            relu = Image.open(_io.BytesIO(brut)).convert('RGBA')
            x, y = im.tobytes(), relu.tobytes()
            s = n = 0
            for i in range(0, len(x), 4):
                if x[i + 3] >= 128:
                    for k in range(3):
                        d = x[i + k] - y[i + k]
                        s += d * d
                        n += 1
            return 10 * math.log10(255.0 * 255.0 / (s / float(n))) if n else 99

        identiques = (a == b)
        print('   %s  lisible %.2f s (%.1f dB)   vectorise %.2f s (%.1f dB)'
              '   %s' % (nom, t1 - t0, psnr(a), t2 - t1, psnr(b),
                         'OCTET POUR OCTET' if identiques else 'differents'))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
