#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch STATIQUE de la resolution dans vfes.exe. Sans debogueur.

Pourquoi statique : forcer la resolution a l'execution demande de s'arreter sur
`RSSetViewports`, appelee a chaque passe de chaque trame. Le jeu devient
inutilisable -- ecran noir et lenteur. La bonne facon est de corriger le binaire
une fois pour toutes.

L'origine des 1920x1080, trouvee par recherche des immediats en `.text` : un
bloc d'initialisation de la configuration d'affichage, tot dans le programme.

    0x140002F9E  mov dword ptr [rbp-0x48], 0x3c    ; 60 Hz
    0x140002FD3  mov dword ptr [rbp-0x50], 0x780   ; largeur 1920
    0x140002FDA  mov dword ptr [rbp-0x4c], 0x438   ; hauteur 1080

Les deux immediats sont a l'octet 3 de leur instruction (`C7 45 xx` + imm32).

Ce que cela devrait entrainer, si l'hypothese est bonne : la fenetre, la chaine
d'echange, les cibles de rendu ET la vue suivent, puisque toutes en descendent.
C'est justement ce que le patch sert a verifier.

L'original est conserve sous `vfes.exe.origine` ; `--rendre` le remet.

Usage :
    py -3 tools/patch_resolution.py --lire
    py -3 tools/patch_resolution.py 1280 720
    py -3 tools/patch_resolution.py --rendre
"""
import os
import shutil
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')

# Deux binaires, deux configurations d'affichage independantes : corriger la
# seule vfes.exe laisse le moteur creer ses cibles et sa vue en 1920x1080.
#   fichier, [(adresse de l'immediat, valeur d'origine), ...]
BINAIRES = [
    ('vfes.exe', [
        # bloc d'init de l'affichage : 60 Hz juste au-dessus
        (0x140002FD3 + 3, 1920),      # mov [rbp-0x50], 0x780
        (0x140002FDA + 3, 1080),      # mov [rbp-0x4c], 0x438
    ]),
    ('vf5fs-pxd-w64-Retail_APM3.dll', [
        (0x1800E74A0 + 6, 1920),      # mov [rsi+0xa4], 0x780
        (0x1800E74AA + 6, 1080),      # mov [rsi+0xa8], 0x438
    ]),
]
EXE = os.path.join(JEU, 'vfes.exe')


def offset(chemin, va):
    """Adresse virtuelle -> deplacement dans le fichier, via les sections."""
    sys.path.insert(0, ICI)
    from pe_disasm import Image
    img = Image(chemin)
    for s in img.secs:
        if s['va'] <= va < s['va'] + max(s.get('vsize', 0), s['rsize']):
            return s['off'] + (va - s['va'])
    return None


def lire():
    out = []
    for nom, points in BINAIRES:
        chemin = os.path.join(JEU, nom)
        with open(chemin, 'rb') as fp:
            d = fp.read()
        for va, attendu in points:
            o = offset(chemin, va)
            out.append((nom, va, o, struct.unpack_from('<I', d, o)[0], attendu))
    return out


def main():
    argv = sys.argv[1:]
    if not os.path.exists(EXE):
        print('introuvable : %s' % EXE)
        return 1

    if '--rendre' in argv:
        n = 0
        for nom, _ in BINAIRES:
            orig = os.path.join(JEU, nom + '.origine')
            if os.path.exists(orig):
                shutil.copy2(orig, os.path.join(JEU, nom))
                n += 1
        if not n:
            print('aucun original conserve : rien a rendre')
            return 1
        print('%d binaire(s) rendu(s) a leur etat d origine' % n)
        for nom, va, o, v, att in lire():
            print('   %-32s 0x%X = %d' % (nom, va, v))
        return 0

    if '--lire' in argv or not argv:
        for nom, va, o, v, att in lire():
            print('   %-32s 0x%X (fichier 0x%X) = %-6d  (origine %d)'
                  % (nom, va, o, v, att))
        return 0

    try:
        larg, haut = int(argv[0]), int(argv[1])
    except (IndexError, ValueError):
        print(__doc__)
        return 1
    if not (256 <= larg <= 7680 and 144 <= haut <= 4320):
        print('resolution hors bornes : %dx%d' % (larg, haut))
        return 1

    for nom, points in BINAIRES:
        chemin = os.path.join(JEU, nom)
        orig = chemin + '.origine'
        if not os.path.exists(orig):
            shutil.copy2(chemin, orig)
            print('original conserve : %s.origine' % nom)
        with open(chemin, 'r+b') as fp:
            for (va, attendu), val in zip(points, (larg, haut)):
                o = offset(orig, va)
                fp.seek(o)
                avant = struct.unpack('<I', fp.read(4))[0]
                fp.seek(o)
                fp.write(struct.pack('<I', val))
                print('   %-32s 0x%X : %d -> %d' % (nom, va, avant, val))
    print('patche en %d x %d' % (larg, haut))
    return 0


if __name__ == '__main__':
    sys.exit(main())
