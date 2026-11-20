#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QUEL GLYPHE LE MOTEUR DESSINE-T-IL VRAIMENT ? -- la sonde de OPTIONS > Controls.

CE QUI EST MESURE, ET CE QUI NE L EST PAS (2026-10-10).

Mesure 1 : l ecran Controls LIT BIEN les libelles 0x32F a 0x332. Les quatre
ont ete remplaces par « 1 », « 2 », « 3 », « 4 » et les quatre chiffres sont
apparus a l ecran, dans l ordre 1 2 4 3 -- c est-a-dire 0x32F, 0x330, 0x332,
0x331.

Mesure 2 : ces quatre libelles portent U+E002, U+E000, U+E001, U+E003 -- les
glyphes XBOX. Verifie dans les DEUX tables du `string_array.farc` VIVANT, celui
de `vf5fs_media/rom/`, pas seulement dans la copie du `.par`.

Mesure 3 : la planche `spr_n_fnt32` (identique a l octet pres dans le `.par` et
sur le disque) porte en rangee 56 colonnes 50-53 le B, le A, le Y et le X
colores, et en rangee 57 colonnes 9-12 le rond, la croix, le triangle et le
carre. `fontmap.bin` -- un seul exemplaire, aucun doublon -- envoie U+E000 a
U+E003 sur les PREMIERES. Image : `analysis/pictos_fnt32.png`.

ET POURTANT L ECRAN DESSINE LES SECONDES. Il y a donc une substitution que ni
le texte, ni la planche, ni `fontmap` n expliquent -- et ce n est pas la table
d echappements : celle-ci est un dictionnaire NOM -> glyphe (0x180005040 la
construit en std::string) et AUCUN des 23 052 libelles ne cite un `ESC_BTN_*`.
`--boutons-xbox` ne peut donc rien changer sur cet ecran, et c est pourquoi il
n a rien change.

CE QUE CETTE SONDE DEMANDE AU JEU. Elle pose quatre codepoints DIFFERENTS sur
les quatre lignes, et la capture dit ce que chacun dessine :

    ligne 1  0x32F  U+E000   « CIRCLE »  -- substitue ?
    ligne 2  0x330  U+E003   « SQUARE »  -- substitue ?
    ligne 3  0x332  U+E015   le rond PS3 -- lui, l est-il ?
    ligne 4  0x331  U+E01A   le P rouge  -- temoin hors de la plage

Le temoin est la pour qu un relevE vide ne passe pas pour une reponse : si le P
ne sort pas non plus, c est la chaine de dessin qu on regarde, pas la
substitution.

LA TABLE DES LIBELLES EST RENDUE A LA FIN, meme si l essai s interrompt.

    py -3 tools/pictos_essai.py
"""
import os
import shutil
import struct
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
TABLE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media',
                     'rom', 'string_array.farc')
SAUVE = TABLE + '.avant_pictos'

# Les deux membres du FArc : (offset, taille). Releves dans l en-tete.
MEMBRES = ((0x44, 428219), (0x68900, 649654))

# (identifiant, codepoint, ce qu on cherche a savoir)
ESSAI = (
    (0x32F, 0xE000, 'CIRCLE  : B xbox, ou rond PS3 ?'),
    (0x330, 0xE003, 'SQUARE  : X xbox, ou carre PS3 ?'),
    (0x332, 0xE015, 'le rond PS3 lui-meme'),
    (0x331, 0xE01A, 'le P rouge -- le temoin'),
)


def poser(chemin, paires):
    """Ecrit un codepoint a la place de chaque libelle cite.

    On ecrit EN PLACE, et seulement des chaines PLUS COURTES ou egales : la
    table est un tableau de pointeurs, deplacer une chaine demanderait de la
    reconstruire. Les quatre libelles visEs font trois octets plus le zero,
    c est-a-dire exactement un glyphe de la zone privee.
    """
    d = bytearray(open(chemin, 'rb').read())
    for base, _t in MEMBRES:
        for ident, cp, _q in paires:
            p = struct.unpack_from('>I', d, base + 4 * ident)[0]
            o = base + p
            b = chr(cp).encode('utf-8') + b'\x00'
            ancien = bytes(d[o:o + 4])
            if len(b) > 4:
                raise AssertionError('U+%04X ne tient pas en quatre octets' % cp)
            d[o:o + 4] = b + b'\x00' * (4 - len(b))
            print('  0x%03X base 0x%-6X %-14r -> U+%04X' %
                  (ident, base, ancien, cp))
    open(chemin, 'wb').write(bytes(d))


def main():
    if not os.path.exists(TABLE):
        print('ABSENT : %s' % TABLE)
        return 1
    print('Les quatre lignes de OPTIONS > Controls, et ce qu on leur demande :')
    for ident, cp, q in ESSAI:
        print('   0x%03X  U+%04X   %s' % (ident, cp, q))
    print()
    shutil.copyfile(TABLE, SAUVE)
    try:
        poser(TABLE, ESSAI)
        print()
        r = subprocess.run([sys.executable,
                            os.path.join(ICI, 'essai_menu.py'), 'controls'])
        code = r.returncode
    finally:
        shutil.copyfile(SAUVE, TABLE)
        os.remove(SAUVE)
        print('  table des libelles RENDUE.')
    print()
    print('A REGARDER : analysis/essai_controls_t58.png')
    print('   les quatre lignes, de haut en bas :')
    for ident, cp, q in ((0x32F, 0xE000, ''), (0x330, 0xE003, ''),
                         (0x332, 0xE015, ''), (0x331, 0xE01A, '')):
        print('     U+%04X' % cp)
    return code


if __name__ == '__main__':
    sys.exit(main())
