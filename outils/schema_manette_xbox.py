#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""LES BOUTONS XBOX DANS OPTIONS > CONTROLS.

L ecran Controls (scene `OPTION CONTROL`, page 0x1807513C8, tache 0x1801A6490)
montre un SCHEMA DE MANETTE : `rom/2d/spr_n_cmnps3`, une DualShock 3 dessinee
en 512x512 RGBA8 non compressee. C est LUI qui porte les ronds et les croix --
pas le texte.

CE QUI A ETE ELIMINE AVANT D EN ARRIVER LA, et il faut le dire pour qu on ne
le refasse pas :

  . LE TEXTE N EST PAS LA SOURCE. Les quatre boutons de face de l ecran sont
    les identifiants 0x32F a 0x332 et ils citent DEJA les glyphes Xbox --
    0x32F = U+E002 (Y), 0x330 = U+E000 (B), 0x331 = U+E001 (A),
    0x332 = U+E003 (X) -- dans les DEUX tables, anglaise et japonaise.
  . LA PLANCHE N EST PAS LA SOURCE NON PLUS. `spr_n_fnt32` tex0 porte bien le
    jeu Xbox 360 a la rangee 56, colonnes 50 a 61 : B rouge, A vert, Y orange,
    X bleu, puis START, BACK, LB, LT. Verifie sur le build COURANT.

DEUX PIEGES MESURES

  1. LA TEXTURE EST STOCKEE A L ENVERS. `txp.py` ne retourne que les formats
     DXT (son FLIP_TOP_BOTTOM est dans la branche 6/9) ; le RGBA8 sort donc
     tel quel, c est-a-dire tete en bas. A l endroit, la disposition est bien
     celle d une DualShock : triangle en haut, carre a gauche, rond a droite,
     croix en bas. ON TRAVAILLE A L ENDROIT ET ON RETOURNE AVANT D ECRIRE.

  2. LES TRAITS DE LEGENDE ROUGES PASSENT SUR LES CUVETTES. Ils sont dans la
     texture, pas dessines par le moteur : les ecraser couperait les traits qui
     designent les boutons. On preserve donc tout pixel rouge.

LA CORRESPONDANCE TOMBE CASE POUR CASE, et c est ce qui rend l operation sure :

    triangle (haut)   -> Y        carre (gauche)  -> X
    rond (droite)     -> B        croix (bas)     -> A

C est a la fois la disposition physique d une manette Xbox et celle que le stub
pose (journal 165). Les traits de legende continuent donc de designer le bon
bouton, et les libelles du moteur (0x32F a 0x332) restent justes.

ON NE DESSINE RIEN : les quatre boutons sont DECOUPES dans la planche du jeu,
rangee 56 colonnes 50 a 53, et reduits a la taille de la cuvette (24 px). Leur
fond est noir opaque -- comme le corps de la manette -- donc le collage efface
la cuvette grise sans laisser de bord.

    py -3 tools/schema_manette_xbox.py --apercu     ecrit un PNG, ne touche rien
    py -3 tools/schema_manette_xbox.py --poser      remplace le .farc du jeu
    py -3 tools/schema_manette_xbox.py --retirer    remet l origine
"""
import gzip
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
DOSSIER_2D = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media',
                          'rom', '2d')
FARC = os.path.join(DOSSIER_2D, 'spr_n_cmnps3.farc')
ORIGINE = FARC + '.origine'
PLANCHE = os.path.join(RACINE, 'extracted', '2d', 'spr_n_fnt32_tex00.png')
APERCU = os.path.join(RACINE, 'analysis', 'schema_manette_xbox.png')

PAS = 33                      # le pas des cases de la planche
RANGEE = 56                   # la rangee des pictos Xbox
COLONNE = {'B': 50, 'A': 51, 'Y': 52, 'X': 53}

# Les quatre cuvettes, image A L ENDROIT. Mesurees en isolant le gris #656666 :
# chacune fait 24 px, et les centres sont a +/- 30 du centre de l amas.
CUVETTES = (('Y', 269, 110, 'triangle, en haut'),
            ('X', 239, 140, 'carre, a gauche'),
            ('B', 299, 140, 'rond, a droite'),
            ('A', 269, 170, 'croix, en bas'))
TAILLE = 24


def est_rouge(p):
    """Un trait de legende : rouge franc et opaque."""
    r, g, b, a = p
    return a > 100 and r > 140 and g < 70 and b < 70


def farc_lire(chemin):
    """{nom: octets} d un conteneur FArC, en-tete gros-boutiste, gzip."""
    d = open(chemin, 'rb').read()
    assert d[:4] == b'FArC', d[:4]
    tete = struct.unpack('>I', d[4:8])[0]
    alignement = struct.unpack('>I', d[8:12])[0]
    o = 12
    membres = []
    while o < tete + 8:
        fin = d.index(b'\0', o)
        nom = d[o:fin].decode('ascii')
        o = fin + 1
        dep, comp, reel = struct.unpack('>III', d[o:o + 12])
        o += 12
        membres.append((nom, gzip.decompress(d[dep:dep + comp]), reel))
    return membres, alignement


def farc_ecrire(chemin, membres, alignement):
    """Reconstruit le FArC. Le gzip est refait, les tailles sont remises."""
    tete = 4
    for nom, _, _ in membres:
        tete += len(nom) + 1 + 12
    dep = 8 + tete
    if alignement > 1:
        dep = (dep + alignement - 1) // alignement * alignement
    corps = b''
    entrees = b''
    for nom, brut, _ in membres:
        c = gzip.compress(brut, 9)
        entrees += nom.encode('ascii') + b'\0' + struct.pack(
            '>III', dep + len(corps), len(c), len(brut))
        corps += c
    d = b'FArC' + struct.pack('>II', tete, alignement) + entrees
    d += b'\0' * (dep - len(d))
    open(chemin, 'wb').write(d + corps)


def txp_pixels(bloc):
    """L offset et les dimensions de l unique image RGBA8 du TXP."""
    o = bloc.find(b'TXP\x02')
    assert o >= 0, 'pas de TXP\\x02'
    w, h, fmt, niveau, taille = struct.unpack('<IIIII', bloc[o + 4:o + 24])
    assert fmt == 2, 'format %d, on attendait 2 = RGBA8' % fmt
    return o + 24, w, h


def composer(brut):
    """Rend les octets RGBA8 avec les quatre boutons Xbox a la place des PS."""
    from PIL import Image
    dep, w, h = txp_pixels(brut)
    im = Image.frombytes('RGBA', (w, h), brut[dep:dep + w * h * 4])
    im = im.transpose(Image.FLIP_TOP_BOTTOM)          # a l endroit
    planche = Image.open(PLANCHE).convert('RGBA')
    avant = im.copy()
    for lettre, x, y, ou in CUVETTES:
        c = COLONNE[lettre]
        g = planche.crop((c * PAS, RANGEE * PAS,
                          c * PAS + 32, RANGEE * PAS + 32))
        g = g.resize((TAILLE, TAILLE), Image.LANCZOS)
        gp = g.load()
        ip = im.load()
        garde = 0
        for v in range(TAILLE):
            for u in range(TAILLE):
                if est_rouge(ip[x + u, y + v]):       # le trait de legende
                    garde += 1
                    continue
                # LE FOND DE LA PLANCHE N EST PAS NOIR PUR : elle est en DXT5,
                # et son fond sombre porte le bruit de la compression. Le
                # recopier tel quel pose un halo CARRE autour de chaque bouton.
                # La borne n est pas un seuil de luminance -- qui mangerait le
                # cerne sombre du bouton -- mais la GEOMETRIE : un bouton est un
                # disque. Hors du disque on ecrit le noir du corps de la
                # manette. La zone collee est exactement la cuvette ; les
                # cadres arrondis sont en dehors et ne sont pas touches.
                dedans = (u - (TAILLE - 1) / 2.0) ** 2 \
                    + (v - (TAILLE - 1) / 2.0) ** 2 <= (TAILLE / 2.0) ** 2
                ip[x + u, y + v] = gp[u, v] if dedans else (0, 0, 0, 255)
        print('   %-8s -> %s   colle en (%d,%d), %d px de trait preserves'
              % (ou, lettre, x, y, garde))
    return im, avant, dep, w, h


def main():
    if '--retirer' in sys.argv:
        if not os.path.exists(ORIGINE):
            print('pas de %s : rien a remettre' % ORIGINE)
            return 1
        os.replace(ORIGINE, FARC)
        print('origine remise : %s' % FARC)
        return 0
    source = ORIGINE if os.path.exists(ORIGINE) else FARC
    membres, alignement = farc_lire(source)
    print('%s : %d membre(s), alignement %d'
          % (os.path.basename(source), len(membres), alignement))
    nom, brut, reel = membres[0]
    im, avant, dep, w, h = composer(brut)
    if '--apercu' in sys.argv or '--poser' not in sys.argv:
        from PIL import Image
        duo = Image.new('RGBA', (w * 2 + 8, h), (30, 30, 30, 255))
        duo.alpha_composite(avant, (0, 0))
        duo.alpha_composite(im, (w + 8, 0))
        duo.convert('RGB').save(APERCU)
        print('apercu ecrit : %s  (avant | apres)' % APERCU)
        return 0
    if not os.path.exists(ORIGINE):
        import shutil
        shutil.copy2(FARC, ORIGINE)
        print('origine sauvegardee : %s' % ORIGINE)
    from PIL import Image
    pix = im.transpose(Image.FLIP_TOP_BOTTOM).tobytes()   # on la remet a l envers
    assert len(pix) == w * h * 4
    neuf = brut[:dep] + pix + brut[dep + w * h * 4:]
    assert len(neuf) == len(brut), (len(neuf), len(brut))
    membres[0] = (nom, neuf, reel)
    farc_ecrire(FARC, membres, alignement)
    print('pose : %s  (%d octets)' % (FARC, os.path.getsize(FARC)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
