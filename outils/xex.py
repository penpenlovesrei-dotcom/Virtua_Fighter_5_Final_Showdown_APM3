#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Ouvre un `default.xex` (XEX2, Xbox 360) chiffre et en compression
« basique », et en rend l'IMAGE PE telle qu'elle est chargee en memoire.

POURQUOI (2026-09-11) : le mode Quest n'existe que dans les VF5 console de
2007. L'ISO PS3 est chiffre sans sa cle de disque ; la version Xbox 360
(`VF5 FS DECOMP\X360_VF5`, base ver.C) a ses donnees en clair et un seul
verrou, son executable. Celui de FS X360 etait en LZX (sans decodeur ici) ;
celui de VF5 est en compression 1, « basique » : des blocs de donnees suivis
de zeros, rien a decompresser.

LE FORMAT (gabarits XEX2 d'emoose/xbox-reversing, cf. memoire)

    +0x00 'XEX2'   +0x04 drapeaux   +0x08 debut des donnees (image)
    +0x10 infos de securite          +0x14 nombre d'en-tetes optionnels
    +0x18 en-tetes : (cle, valeur) ; octet bas de la cle = 0x00/0x01 valeur
          en ligne, 0xFF decalage vers un bloc prefixe de sa taille
    0x3FF   FILE_FORMAT_INFO : taille, chiffrement (u16), compression (u16),
            puis (compression 1) des paires {octets de donnees, octets de
            zeros}
    0x10100 point d'entree        0x10201 adresse de base de l'image

    infos de securite : +0x04 taille de l'image, +0x110 adresse de
    chargement, +0x150 la cle AES du fichier, CHIFFREE par la cle commerciale

Le dechiffrement est un AES-128-CBC continu (vecteur nul) sur toutes les
donnees du fichier ; les zeros ne sont pas dans le fichier et ne comptent
pas dans la chaine. La cle commerciale est la cle publique qu'utilise
l'emulateur Xenia ; la cle de developpement (nulle) est essayee aussi.
L'image rendue commence par `MZ` : c'est la preuve que la cle est la bonne.

    py -3 tools/xex.py <default.xex> <sortie.img>
"""
import struct
import sys

from Crypto.Cipher import AES

CLE_COMMERCIALE = bytes.fromhex('20B185A59D28FDC340583FBB0896BF91')
CLE_DEVELOPPEMENT = bytes(16)


class Refus(Exception):
    pass


def entetes(d):
    if d[:4] != b'XEX2':
        raise Refus('pas un XEX2 (%r)' % d[:4])
    _, debut, _, secu, n = struct.unpack_from('>5I', d, 4)
    out = {}
    for i in range(n):
        k, v = struct.unpack_from('>II', d, 0x18 + 8 * i)
        out[k] = v
    return debut, secu, out


def lire(d):
    debut, secu, h = entetes(d)
    if 0x3FF not in h:
        raise Refus('pas de FILE_FORMAT_INFO')
    o = h[0x3FF]
    taille_info, chiffre, comp = struct.unpack_from('>IHH', d, o)
    if comp not in (1, 2):
        raise Refus('compression %d : on lit la « basique » (1) et la '
                    '« normale » (2, LZX)' % comp)
    if comp == 1:
        blocs = [struct.unpack_from('>II', d, o + 8 + 8 * k)
                 for k in range((taille_info - 8) // 8)]
    else:
        fenetre, bloc0 = struct.unpack_from('>II', d, o + 8)
        blocs = None
    taille_image = struct.unpack_from('>I', d, secu + 4)[0]
    base = struct.unpack_from('>I', d, secu + 0x110)[0]
    cle_fichier = d[secu + 0x150:secu + 0x160]
    brut = d[debut:]
    brut = brut[:len(brut) // 16 * 16]
    essais = [('commerciale', CLE_COMMERCIALE), ('developpement',
                                                 CLE_DEVELOPPEMENT)]
    if chiffre == 0:
        essais = [('aucune', None)]
    for nom, cle in essais:
        if cle is None:
            clair = brut
        else:
            session = AES.new(cle, AES.MODE_ECB).decrypt(cle_fichier)
            clair = AES.new(session, AES.MODE_CBC, bytes(16)).decrypt(brut)
        if comp == 1:
            if clair[:2] != b'MZ':
                continue
            img = bytearray()
            p = 0
            for n_d, n_z in blocs:
                img += clair[p:p + n_d]
                img += bytes(n_z)
                p += n_d
            if len(img) < taille_image:
                img += bytes(taille_image - len(img))
            return dict(image=bytes(img[:taille_image]), base=base, cle=nom,
                        entree=h.get(0x10100), blocs=len(blocs))
        # COMPRESSION NORMALE (2). Les donnees dechiffrees sont une CHAINE DE
        # BLOCS, et non le flot LZX lui-meme : chaque bloc commence par la
        # taille et l'empreinte du SUIVANT (4 + 20 octets), puis enchaine des
        # morceaux precedes de leur taille sur 16 bits gros-boutistes, la
        # taille zero fermant le bloc. On recolle tous les morceaux, et c'est
        # cela -- et cela seul -- qui forme le flot LZX.
        try:
            flot, n_blocs = _rassembler(clair, bloc0)
        except Refus:
            continue                      # mauvaise cle : la chaine deraille
        import lzx
        bits_fenetre = fenetre.bit_length() - 1
        if 1 << bits_fenetre != fenetre:
            raise Refus('fenetre LZX 0x%X non puissance de deux' % fenetre)
        try:
            img = lzx.decompresser(flot, taille_image, bits_fenetre)
        except lzx.Refus as e:
            raise Refus('LZX : %s' % e)
        if img[:2] != b'MZ':
            continue
        return dict(image=img, base=base, cle=nom,
                    entree=h.get(0x10100), blocs=n_blocs)
    raise Refus('aucune cle ne donne une image `MZ`')


def _rassembler(clair, bloc0):
    """Recolle les morceaux de la chaine de blocs en un seul flot LZX.

    Rend aussi le nombre de blocs. Leve `Refus` des que la chaine deraille :
    c'est ce qui sert a reconnaitre une mauvaise cle sans avoir a lancer le
    decompresseur.
    """
    flot = bytearray()
    p, taille, n = 0, bloc0, 0
    while taille:
        if p + 24 > len(clair) or taille > len(clair):
            raise Refus('chaine de blocs incoherente au bloc %d' % n)
        debut = p
        suivante = struct.unpack_from('>I', clair, p)[0]
        p += 4 + 20                       # taille du suivant, puis empreinte
        while True:
            if p + 2 > len(clair):
                raise Refus('morceau tronque au bloc %d' % n)
            m = struct.unpack_from('>H', clair, p)[0]
            p += 2
            if not m:
                break
            if p + m > debut + taille:
                raise Refus('morceau qui deborde son bloc (%d)' % n)
            flot += clair[p:p + m]
            p += m
        p = debut + taille
        taille = suivante
        n += 1
        if n > 100000:
            raise Refus('chaine de blocs sans fin')
    return bytes(flot), n


def sections_pe(img):
    e = struct.unpack_from('<I', img, 0x3C)[0]
    if img[e:e + 4] != b'PE\x00\x00':
        raise Refus('pas de signature PE')
    machine, n = struct.unpack_from('<HH', img, e + 4)
    taille_opt = struct.unpack_from('<H', img, e + 20)[0]
    s0 = e + 24 + taille_opt
    out = []
    for k in range(n):
        s = img[s0 + 40 * k:s0 + 40 * (k + 1)]
        nom = s[:8].rstrip(b'\x00').decode('latin-1')
        vsize, va, rsize, roff = struct.unpack_from('<IIII', s, 8)
        car = struct.unpack_from('<I', s, 36)[0]
        out.append((nom, va, vsize, car))
    return machine, out


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    d = open(sys.argv[1], 'rb').read()
    try:
        r = lire(d)
        machine, secs = sections_pe(r['image'])
    except Refus as e:
        print('REFUS : %s' % e)
        return 1
    open(sys.argv[2], 'wb').write(r['image'])
    print('image : %d octets, base 0x%X, point d entree 0x%X, cle %s, '
          '%d blocs' % (len(r['image']), r['base'], r['entree'] or 0,
                        r['cle'], r['blocs']))
    print('machine PE 0x%X (0x1F2 = PowerPC gros-boutien)' % machine)
    for nom, va, vsize, car in secs:
        print('  %-8s 0x%08X  0x%07X  %s' % (nom, r['base'] + va, vsize,
                                             'code' if car & 0x20000000
                                             else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
