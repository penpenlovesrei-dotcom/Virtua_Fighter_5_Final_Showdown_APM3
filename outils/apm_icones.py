#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Sort les icones de surimpression du systeme ALL.Net P-ras Multi.

D'ou vient la question : sur une capture de l'ecran-titre de VF5, six badges
grises et barres apparaissent aux quatre coins. Le JEU ne les contient pas --
aucun nom d'asset d'icone, et ses compositions de titre sont au complet
(`misc_title*`). Ils viennent de `emoneyUI.exe`, l'application UNITY du
systeme APM (`APM_V1.04_internal_0`), qui dessine par-dessus le jeu.

Ce que son `Assembly-CSharp.dll` nomme, et qui ne laisse pas de doute :

    EnableEmoneyIcon      emoneyBackgroundSpriteOnDisable
    EnableGamePadIcon     gamePadBackgroundSpriteOnDisable
    HeadphoneVolumeIcon   iconAlignment / iconAxis / iconX / iconY

et ses textures viennent par PAIRES `_enable` / `_disable`.

Format, lu dans `sharedassets0.assets` : un Texture2D Unity y porte son nom
prefixe de sa longueur, puis (aligne a 4) forcedFallbackFormat, downscaleFallback,
**largeur, hauteur, taille**, format (4 = RGBA32, 12 = DXT5), mipCount... et
plus loin un bloc `streamData` { offset, size, chemin } qui designe le `.resS`.
Les lignes y sont de BAS EN HAUT.

    py -3 tools/apm_icones.py
    py -3 tools/apm_icones.py --assets Apmv3System_Data/resources.assets         --noms NotAllow EMoney Network Speaker VolumeOff
"""
import os
import re
import struct
import sys
import zlib

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
APM = r'C:\Users\frede\Desktop\VF5 FS DECOMP\APM_V1.04_internal_0'
SORTIE = os.path.join(RACINE, 'extracted', 'apm_icones')
NOMS = ['btn_emoney_enable', 'btn_emoney_disable',
        'btn_pad_enable', 'btn_pad_disable',
        'btn_volume_enable', 'btn_volume_disable',
        'headphone', 'HeadphoneVolume1', 'HeadphoneVolume2',
        'HeadphoneVolume3', 'BrandIconFrame']


def png(chemin, larg, haut, rgba):
    """Ecrit un PNG 8 bits RVBA, sans dependance."""
    lignes = b''.join(b'\x00' + rgba[y * larg * 4:(y + 1) * larg * 4]
                      for y in range(haut))

    def bloc(typ, don):
        c = typ + don
        return (struct.pack('>I', len(don)) + c
                + struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF))

    with open(chemin, 'wb') as fp:
        fp.write(b'\x89PNG\r\n\x1a\n')
        fp.write(bloc(b'IHDR', struct.pack('>IIBBBBB', larg, haut, 8, 6, 0, 0, 0)))
        fp.write(bloc(b'IDAT', zlib.compress(lignes, 9)))
        fp.write(bloc(b'IEND', b''))


def bc3(brut, larg, haut):
    """Decode du DXT5 / BC3 (format Unity 12) en RVBA.

    Un bloc fait 16 octets : 8 pour l'alpha (deux bornes + 16 indices de 3
    bits) puis 8 pour la couleur (deux RGB565 + 16 indices de 2 bits).
    Sans cela, `NotAllow` -- le symbole BARRE que le systeme superpose a ses
    icones -- reste illisible, et c'est justement celui qu'on cherche.
    """
    sortie = bytearray(larg * haut * 4)
    bx, by = (larg + 3) // 4, (haut + 3) // 4
    o = 0
    for j in range(by):
        for i in range(bx):
            a0, a1 = brut[o], brut[o + 1]
            bits = int.from_bytes(brut[o + 2:o + 8], 'little')
            c0, c1 = struct.unpack_from('<HH', brut, o + 8)
            idx = struct.unpack_from('<I', brut, o + 12)[0]
            o += 16
            alphas = [a0, a1]
            if a0 > a1:
                alphas += [((7 - k) * a0 + k * a1) // 7 for k in range(1, 7)]
            else:
                alphas += [((5 - k) * a0 + k * a1) // 5 for k in range(1, 5)]
                alphas += [0, 255]

            def rgb(c):
                return (((c >> 11) & 31) * 255 // 31,
                        ((c >> 5) & 63) * 255 // 63,
                        (c & 31) * 255 // 31)
            r0, r1 = rgb(c0), rgb(c1)
            coul = [r0, r1,
                    tuple((2 * r0[k] + r1[k]) // 3 for k in range(3)),
                    tuple((r0[k] + 2 * r1[k]) // 3 for k in range(3))]
            for p in range(16):
                x, y = i * 4 + p % 4, j * 4 + p // 4
                if x >= larg or y >= haut:
                    continue
                c = coul[(idx >> (2 * p)) & 3]
                a = alphas[(bits >> (3 * p)) & 7]
                d = (y * larg + x) * 4
                sortie[d:d + 4] = bytes((c[0], c[1], c[2], a))
    return bytes(sortie)


def bc1(brut, larg, haut):
    """Decode du DXT1 / BC1 : 8 octets par bloc, deux RGB565 et 16 indices."""
    out = bytearray(larg * haut * 4)
    o = 0
    for j in range((haut + 3) // 4):
        for i in range((larg + 3) // 4):
            c0, c1 = struct.unpack_from('<HH', brut, o)
            idx = struct.unpack_from('<I', brut, o + 4)[0]
            o += 8

            def rgb(c):
                return (((c >> 11) & 31) * 255 // 31,
                        ((c >> 5) & 63) * 255 // 63,
                        (c & 31) * 255 // 31)
            r0, r1 = rgb(c0), rgb(c1)
            if c0 > c1:
                coul = [r0, r1,
                        tuple((2 * r0[k] + r1[k]) // 3 for k in range(3)),
                        tuple((r0[k] + 2 * r1[k]) // 3 for k in range(3))]
                alph = [255, 255, 255, 255]
            else:
                coul = [r0, r1, tuple((r0[k] + r1[k]) // 2 for k in range(3)),
                        (0, 0, 0)]
                alph = [255, 255, 255, 0]
            for p in range(16):
                x, y = i * 4 + p % 4, j * 4 + p // 4
                if x >= larg or y >= haut:
                    continue
                k = (idx >> (2 * p)) & 3
                c = coul[k]
                d = (y * larg + x) * 4
                out[d:d + 4] = bytes((c[0], c[1], c[2], alph[k]))
    return bytes(out)


def rgb24(brut, larg, haut):
    """RGB24 -> RVBA opaque."""
    out = bytearray(larg * haut * 4)
    for i in range(larg * haut):
        out[i * 4:i * 4 + 3] = brut[i * 3:i * 3 + 3]
        out[i * 4 + 3] = 255
    return bytes(out)


def texture(d, nom):
    """Rend (largeur, hauteur, format, offset, taille, fichier) ou None."""
    cible = nom.encode()
    i = d.find(cible)
    while i >= 0:
        if i >= 4 and struct.unpack_from('<I', d, i - 4)[0] == len(cible):
            deb = (i + len(cible) + 3) & ~3
            _, _, larg, haut, taille, fmt = struct.unpack_from('<6i', d, deb)
            if 0 < larg <= 4096 and 0 < haut <= 4096 and taille > 0:
                # le bloc streamData suit : on le repere par le chemin `.resS`
                m = re.search(rb'[\x20-\x7e]{5,40}\.resS', d[deb:deb + 0x200])
                if m:
                    p = deb + m.start() - 4          # longueur du chemin
                    off, tai = struct.unpack_from('<II', d, p - 8)
                    fic = d[p + 4:p + 4 + struct.unpack_from('<I', d, p)[0]]
                    return larg, haut, fmt, off, tai, fic.decode()
        i = d.find(cible, i + 1)
    return None


def main():
    argv = sys.argv[1:]
    base = APM
    if '--dossier' in argv:
        base = argv[argv.index('--dossier') + 1]
    fichier = 'emoneyUI_Data/sharedassets0.assets'
    if '--assets' in argv:
        fichier = argv[argv.index('--assets') + 1]
    assets = os.path.join(base, *fichier.split('/'))
    if not os.path.exists(assets):
        print('introuvable : %s' % assets)
        return 1
    noms = NOMS
    if '--noms' in argv:
        noms = [a for a in argv[argv.index('--noms') + 1:]
                if not a.startswith('--')]
    d = open(assets, 'rb').read()
    os.makedirs(SORTIE, exist_ok=True)

    print('=' * 70)
    print('LES ICONES DE SURIMPRESSION DU SYSTEME APM')
    print('   source : %s' % assets)
    print('=' * 70)
    sortis = 0
    for nom in noms:
        t = texture(d, nom)
        if not t:
            print('   %-22s introuvable' % nom)
            continue
        larg, haut, fmt, off, tai, fic = t
        etat = 'RGBA32' if fmt == 4 else ('format %d' % fmt)
        print('   %-22s %3d x %-3d  %-9s %6d o  @0x%X dans %s'
              % (nom, larg, haut, etat, tai, off, fic))
        if fmt not in (4, 3, 10, 12):
            print('      (format %d non decode ici -- BC7 notamment)' % fmt)
            continue
        res = os.path.join(os.path.dirname(assets), fic)
        with open(res, 'rb') as fp:
            fp.seek(off)
            brut = fp.read(tai)
        if fmt == 12:
            if len(brut) < ((larg + 3) // 4) * ((haut + 3) // 4) * 16:
                print('      donnees tronquees')
                continue
            brut = bc3(brut, larg, haut)
        elif fmt == 10:
            if len(brut) < ((larg + 3) // 4) * ((haut + 3) // 4) * 8:
                print('      donnees tronquees')
                continue
            brut = bc1(brut, larg, haut)
        elif fmt == 3:
            if len(brut) < larg * haut * 3:
                print('      donnees tronquees')
                continue
            brut = rgb24(brut, larg, haut)
        elif len(brut) < larg * haut * 4:
            print('      donnees tronquees')
            continue
        # Unity range ses lignes de BAS EN HAUT
        lignes = [brut[y * larg * 4:(y + 1) * larg * 4] for y in range(haut)]
        png(os.path.join(SORTIE, nom + '.png'), larg, haut,
            b''.join(reversed(lignes)))
        sortis += 1
    print()
    print('%d image(s) ecrite(s) dans %s' % (sortis, SORTIE))
    return 0


if __name__ == '__main__':
    sys.exit(main())
