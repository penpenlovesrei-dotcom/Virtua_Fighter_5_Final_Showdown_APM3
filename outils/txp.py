#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lire les textures TXP des .farc 2D et les sortir en PNG.

Chaine complete, du conteneur au pixel :

    spr_n_XXX.farc          FArC : entete BE, entrees {nom, offset, taille
                            compressee, taille reelle}, donnees gzip
      -> spr_n_XXX.bin      jeu de sprites ; quelque part dedans, un TXP set
        'TXP\\x03'          u32 nombre, u32 groupe, u32[] offsets (relatifs)
          'TXP\\x04'        une texture : u32 mips, u32 groupe, u32[] offsets
            'TXP\\x02'      une image : u32 larg, u32 haut, u32 format,
                            u32 niveau, u32 taille, puis les octets

Formats rencontres : 1 = RGB8, 2 = RGBA8, 6 = DXT1, 9 = DXT5. Les deux
compresses sont rendus en collant un entete DDS devant les octets : Pillow
sait lire le DDS, inutile d'ecrire un decodeur BC.

    py -3 tools/txp.py --lister
    py -3 tools/txp.py --sortir spr_n_fnt32
    py -3 tools/txp.py --sortir toutes
"""
import gzip
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
DOSSIER_2D = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media',
                          'rom', '2d')
SORTIE = os.path.join(RACINE, 'extracted', '2d')

FORMATS = {0: 'A8', 1: 'RGB8', 2: 'RGBA8', 6: 'DXT1', 9: 'DXT5'}


def defarc(chemin):
    """Rend {nom: octets} pour un conteneur FArC (gzip)."""
    d = open(chemin, 'rb').read()
    assert d[:4] == b'FArC', d[:4]
    fin = 8 + struct.unpack_from('>I', d, 4)[0]
    o, sortie = 12, {}
    while o < fin:
        e = d.index(b'\0', o)
        nom = d[o:e].decode('ascii')
        o = e + 1
        off, comp, _unc = struct.unpack_from('>III', d, o)
        o += 12
        sortie[nom] = gzip.decompress(d[off:off + comp])
    return sortie


def textures(d):
    """Rend la liste des images d'un jeu de sprites."""
    i = d.find(b'TXP\x03')
    if i < 0:
        return []
    n = struct.unpack_from('<I', d, i + 4)[0]
    offs = struct.unpack_from('<%dI' % n, d, i + 12)
    out = []
    for k, o in enumerate(offs):
        t = i + o
        nm = struct.unpack_from('<I', d, t + 4)[0]
        so = struct.unpack_from('<%dI' % nm, d, t + 12)
        s = t + so[0]                       # niveau 0 seulement
        w, h, f, _lvl, taille = struct.unpack_from('<5I', d, s + 4)
        out.append({'i': k, 'larg': w, 'haut': h, 'format': f,
                    'octets': d[s + 0x18:s + 0x18 + taille],
                    'offset': s + 0x18, 'taille': taille})
    return out


def entete_dds(w, h, quatre_cc, taille):
    """128 octets exactement : magie + DDS_HEADER (124)."""
    e = b'DDS '
    e += struct.pack('<7I', 124, 0x000A1007, h, w, taille, 0, 0)
    e += b'\0' * 44                                   # dwReserved1[11]
    e += struct.pack('<2I', 32, 0x4) + quatre_cc      # DDS_PIXELFORMAT
    e += struct.pack('<5I', 0, 0, 0, 0, 0)
    e += struct.pack('<5I', 0x1000, 0, 0, 0, 0)
    assert len(e) == 128, len(e)
    return e


def image(t):
    """L image RENDUE A L ENDROIT.

    TOUTES les planches sont stockees de BAS EN HAUT, et pas seulement les
    compressees comme le croyait ce fichier. Mesure du 2026-10-11 :
    `spr_s_gamdan` tex06, du RGBA8, sort la tete en bas sans retournement --
    et `tools/schema_manette_xbox.py`, qui repeint une planche RGBA8 validee a
    l ecran, fait bien un `FLIP_TOP_BOTTOM` AVANT d ecrire. On retourne donc
    partout, et l ecriture retourne en sens inverse.
    """
    from PIL import Image
    w, h, f, o = t['larg'], t['haut'], t['format'], t['octets']
    if f == 2:
        return Image.frombytes('RGBA', (w, h), o).transpose(
            Image.FLIP_TOP_BOTTOM)
    if f == 1:
        return Image.frombytes('RGB', (w, h), o).convert('RGBA').transpose(
            Image.FLIP_TOP_BOTTOM)
    if f == 0:
        a = Image.frombytes('L', (w, h), o)
        im = Image.new('RGBA', (w, h), (255, 255, 255, 0))
        im.putalpha(a)
        return im.transpose(Image.FLIP_TOP_BOTTOM)
    if f in (3, 5):
        # DEUX FORMATS DE SEIZE BITS, mesures a 2,00 octets par texel :
        #   3 = RGB5    (565, opaque)      5 = RGBA4   (4444)
        # Les deux viennent de l enumeration du moteur, ou DXT1 vaut 6 : les
        # rangs 3 et 5 y sont RGB5 et RGBA4. La mesure confirme la largeur ;
        # l image, elle, se juge a l oeil -- cf. analysis/formats_16bits.png.
        import numpy as np
        v = np.frombuffer(o[:w * h * 2], dtype='<u2').astype(np.uint32)
        if f == 3:
            r = ((v >> 11) & 0x1F) * 255 // 31
            g = ((v >> 5) & 0x3F) * 255 // 63
            b2 = (v & 0x1F) * 255 // 31
            a = np.full_like(r, 255)
        else:
            a = ((v >> 12) & 0xF) * 17
            r = ((v >> 8) & 0xF) * 17
            g = ((v >> 4) & 0xF) * 17
            b2 = (v & 0xF) * 17
        arr = np.stack([r, g, b2, a], axis=-1).astype(np.uint8)
        return Image.frombytes('RGBA', (w, h), arr.tobytes()).transpose(
            Image.FLIP_TOP_BOTTOM)
    if f in (6, 9):
        cc = b'DXT1' if f == 6 else b'DXT5'
        import io
        brut = entete_dds(w, h, cc, len(o)) + o
        # Pillow rend le DDS de bas en haut : on remet la planche a l'endroit.
        im = Image.open(io.BytesIO(brut)).convert('RGBA')
        return im.transpose(Image.FLIP_TOP_BOTTOM)
    raise ValueError('format %d inconnu' % f)


def damier(im):
    from PIL import Image
    w, h = im.size
    fond = Image.new('RGBA', (w, h))
    px = fond.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = (60, 60, 60, 255) if ((x // 16) + (y // 16)) % 2 \
                else (30, 30, 30, 255)
    return Image.alpha_composite(fond, im).convert('RGB')


def main():
    a = sys.argv[1:]
    os.makedirs(SORTIE, exist_ok=True)
    noms = sorted(f for f in os.listdir(DOSSIER_2D) if f.endswith('.farc'))
    cible = None
    if '--sortir' in a:
        cible = a[a.index('--sortir') + 1]
        if cible != 'toutes':
            noms = [n for n in noms if n.startswith(cible)]
    for nom in noms:
        contenu = defarc(os.path.join(DOSSIER_2D, nom))
        for fich, d in contenu.items():
            open(os.path.join(SORTIE, fich), 'wb').write(d)
            ts = textures(d)
            print('%-22s %-22s %2d textures' % (nom, fich, len(ts)))
            for t in ts:
                marque = '%-6s %4dx%-4d %8d o' % (
                    FORMATS.get(t['format'], '?%d' % t['format']),
                    t['larg'], t['haut'], t['taille'])
                print('    tex%-3d %s' % (t['i'], marque))
                if cible:
                    base = fich[:-4]
                    f = os.path.join(SORTIE, '%s_tex%02d.png' % (base, t['i']))
                    try:
                        damier(image(t)).save(f)
                    except Exception as ex:            # noqa: BLE001
                        print('       -> ECHEC : %s' % ex)
    return 0


if __name__ == '__main__':
    sys.exit(main())
