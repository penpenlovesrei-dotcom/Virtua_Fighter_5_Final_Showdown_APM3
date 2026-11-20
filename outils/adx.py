#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Decoder un fichier ADX de CRI, et le rendre en WAV.

POURQUOI. L ADX est partout dans ces jeux : la piste son de chaque `.sfd` en
est, et l image de VF5 R porte a elle seule **3 958** `.adx` de voix sous
`/tv/sound/voice/`. Aucun lecteur ordinaire ne les ouvre, et VLC non plus --
essaye le 2026-10-11, il tombe sur son demultiplexeur mjpeg et rend un fichier
vide. L atelier n avait pas de decodeur ; en voici un, sans dependance.

L EN-TETE, gros-boutiste :

    +0x00 u16  0x8000, la magie
    +0x02 u16  ou commencent les donnees, MOINS QUATRE -- un piege classique
    +0x04 u8   type d encodage : 0x03 = ADPCM standard
    +0x05 u8   taille de bloc, 18 octets
    +0x06 u8   bits par echantillon, 4
    +0x07 u8   nombre de canaux
    +0x08 u32  frequence
    +0x0C u32  nombre total d echantillons
    +0x10 u16  frequence de coupure du filtre passe-haut
    +0x12 u8   version       +0x13 u8  drapeau de chiffrement

LES DEUX COEFFICIENTS NE SONT PAS DANS LE FICHIER : ils se CALCULENT a partir
de la coupure et de la frequence. C est la seule subtilite du format --

    a = V2 - cos(2 PI coupure / frequence)      b = V2 - 1
    c = (a - racine((a+b)(a-b))) / b
    k1 = c * 2   k2 = -(c * c)                  les deux en virgule fixe Q12

UN BLOC fait 18 octets par canal : un facteur d echelle sur 16 bits, puis 32
demi-octets signes (-8 a 7). Chaque echantillon vaut
`nibble * echelle + (k1*h1 + k2*h2) >> 12`, ecrete a 16 bits. Les canaux
alternent bloc par bloc.

    py -3 tools/adx.py info <fichier.adx>
    py -3 tools/adx.py wav  <fichier.adx> <sortie.wav>
"""
import math
import struct
import sys


def entete(d):
    if d[:2] != b'\x80\x00':
        raise SystemExit('pas la magie 0x8000 : ce n est pas un ADX')
    debut = struct.unpack_from('>H', d, 2)[0] + 4
    typ, bloc, bits, canaux = d[4], d[5], d[6], d[7]
    freq, total = struct.unpack_from('>II', d, 8)
    coupure = struct.unpack_from('>H', d, 0x10)[0]
    version, chiffre = d[0x12], d[0x13]
    return {'debut': debut, 'type': typ, 'bloc': bloc, 'bits': bits,
            'canaux': canaux, 'freq': freq, 'total': total,
            'coupure': coupure, 'version': version, 'chiffre': chiffre}


def coefficients(coupure, freq):
    """Les deux coefficients du predicteur, en Q12. Calcules, jamais lus."""
    r2 = math.sqrt(2.0)
    a = r2 - math.cos(2.0 * math.pi * coupure / freq)
    b = r2 - 1.0
    c = (a - math.sqrt((a + b) * (a - b))) / b
    return int(c * 2.0 * 4096.0), int(-(c * c) * 4096.0)


def decoder(d):
    """Rend (en-tete, echantillons entrelaces) en entiers 16 bits signes."""
    e = entete(d)
    if e['type'] != 3:
        raise SystemExit('type d encodage %d non gere (seul 0x03 l est)'
                         % e['type'])
    if e['chiffre']:
        raise SystemExit('ce fichier est chiffre (drapeau +0x13 = %d)'
                         % e['chiffre'])
    k1, k2 = coefficients(e['coupure'], e['freq'])
    nc, bloc = e['canaux'], e['bloc']
    par_bloc = (bloc - 2) * 2                      # 32 echantillons
    h1 = [0] * nc
    h2 = [0] * nc
    out = []
    o = e['debut']
    reste = e['total']
    n = len(d)
    while reste > 0 and o + bloc * nc <= n:
        voies = []
        for c in range(nc):
            base = o + bloc * c
            echelle = struct.unpack_from('>h', d, base)[0]
            v = []
            a, b = h1[c], h2[c]
            for i in range(par_bloc):
                octet = d[base + 2 + (i >> 1)]
                nib = (octet >> 4) if (i & 1) == 0 else (octet & 0x0F)
                if nib >= 8:
                    nib -= 16
                s = nib * echelle + ((k1 * a + k2 * b) >> 12)
                if s > 32767:
                    s = 32767
                elif s < -32768:
                    s = -32768
                v.append(s)
                b = a
                a = s
            h1[c], h2[c] = a, b
            voies.append(v)
        combien = min(par_bloc, reste)
        for i in range(combien):
            for c in range(nc):
                out.append(voies[c][i])
        reste -= combien
        o += bloc * nc
    return e, out


def ecrire_wav(chemin, e, ech):
    n = len(ech)
    octets = struct.pack('<%dh' % n, *ech)
    nc, freq = e['canaux'], e['freq']
    bloc = nc * 2
    entete_wav = b'RIFF' + struct.pack('<I', 36 + len(octets)) + b'WAVE'
    entete_wav += b'fmt ' + struct.pack('<IHHIIHH', 16, 1, nc, freq,
                                        freq * bloc, bloc, 16)
    entete_wav += b'data' + struct.pack('<I', len(octets))
    with open(chemin, 'wb') as fp:
        fp.write(entete_wav)
        fp.write(octets)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd, src = argv[0], argv[1]
    d = open(src, 'rb').read()
    if cmd == 'info':
        e = entete(d)
        k1, k2 = coefficients(e['coupure'], e['freq'])
        print('%s : %d canaux, %d Hz, %d echantillons (%.2f s)'
              % (src, e['canaux'], e['freq'], e['total'],
                 e['total'] / float(e['freq'])))
        print('   donnees a 0x%X, bloc %d o, coupure %d Hz, version %d'
              % (e['debut'], e['bloc'], e['coupure'], e['version']))
        print('   coefficients Q12 : %d, %d' % (k1, k2))
        return 0
    if cmd == 'wav':
        if len(argv) < 3:
            print(__doc__)
            return 1
        e, ech = decoder(d)
        ecrire_wav(argv[2], e, ech)
        print('%s -> %s : %d canaux, %d Hz, %.2f s'
              % (src, argv[2], e['canaux'], e['freq'],
                 len(ech) / float(e['canaux'] * e['freq'])))
        return 0
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
