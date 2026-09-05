#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les libelles du jeu, resolus depuis `string_array.farc`.

Les entrees de menu ne sont pas des chaines du binaire : ce sont des
**identifiants de texte** passes a `0x1801EFD10`, qui les resout dans une table
chargee en `0x180753900` (borne `0x5A0C` = 23052 entrees). Sans cette table, un
menu desassemble ne se laisse pas nommer -- on lit `mov [rbp-0x50], 0x177` et on
ne sait pas que c'est « SINGLE PLAYER ».

La table est `string_array.farc` du `.par` : 1 165 900 octets, NON compresse, un
FArc de deux fichiers -- `string_array_en.bin` (offset 0x44, 0x73770 octets) et
`string_array_jp.bin`. Piege : le fichier est **gros-boutiste** (il vient de la
PS3), alors que tout le reste du moteur x64 est petit-boutiste. C'est un tableau
de pointeurs u32 BE vers des chaines UTF-8 terminees par zero, indexe par
l'identifiant.

    py -3 tools/libelles.py 0x177              un identifiant
    py -3 tools/libelles.py 0x177 0x183        une plage
    py -3 tools/libelles.py --chercher DOJO    par le texte
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import sllz                                                  # noqa: E402

PAR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_data.par')
CACHE = os.path.join(RACINE, 'extracted', 'string_array_en.bin')
FARC_EN = (0x44, 0x73770)          # offset et taille dans le FArc


def table():
    """Rend le contenu de `string_array_en.bin`, en le sortant du .par au besoin."""
    if os.path.exists(CACHE):
        with open(CACHE, 'rb') as fp:
            return fp.read()
    tmp = CACHE + '.farc'
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    # `sllz.py` n'expose que sa ligne de commande : on la reutilise telle quelle
    # plutot que de dupliquer la lecture d'index.
    sauve = sys.argv
    sys.argv = ['sllz', 'sortir', PAR, 'string_array.farc', tmp]
    try:
        sllz.main()
    finally:
        sys.argv = sauve
    with open(tmp, 'rb') as fp:
        d = fp.read()
    en = d[FARC_EN[0]: FARC_EN[0] + FARC_EN[1]]
    with open(CACHE, 'wb') as fp:
        fp.write(en)
    os.remove(tmp)
    return en


def texte(en, i):
    if i < 0 or 4 * i + 4 > len(en):
        return None
    p = struct.unpack_from('>I', en, 4 * i)[0]        # GROS-BOUTISTE
    if p <= 0 or p >= len(en):
        return None
    fin = en.find(b'\0', p)
    return en[p:fin].decode('utf-8', 'replace')


def _sortie_sure():
    # La console Windows est en cp1252 : les libelles japonais et les
    # pictogrammes du jeu la font planter. On remplace au lieu d'echouer.
    try:
        sys.stdout.reconfigure(errors='backslashreplace')
    except Exception:
        pass


def main():
    _sortie_sure()
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    en = table()
    if argv[0] == '--chercher':
        motif = argv[1].lower()
        n = 0
        for i in range(len(en) // 4):
            t = texte(en, i)
            if t and motif in t.lower():
                print('  0x%03X  %r' % (i, t))
                n += 1
                if n >= 200:
                    print('  ... (arrete a 200)')
                    break
        return 0
    lo = int(argv[0], 0)
    hi = int(argv[1], 0) if len(argv) > 1 else lo
    for i in range(lo, hi + 1):
        print('  0x%03X  %r' % (i, texte(en, i)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
