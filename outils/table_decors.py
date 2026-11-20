#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""La table des 41 decors du moteur, lue et mise a plat.

Deux tables paralleles, toutes deux indexees par le meme index 0..40 :

  * `0x18039F7A0`  41 pointeurs vers le CODE A TROIS LETTRES  ("are", "djo"...),
    utilise par le poseur d'ECLAIRAGE `0x1800D7130` pour fabriquer
    `./rom/ibl/<code>.ibl` et `./rom/light_param/{light,fog,glow,wind,
    envmap_correct}_<code>.txt` ;
  * `0x180403430`  41 descripteurs de 0xF0 octets, utilises par la tache
    `TaskStage` pour la GEOMETRIE, la collision, les effets et les musiques.

Le piege du chantier (memoire « Deux index de decor dans VF5 ») est la : ce
sont deux chemins distincts, et patcher l'un ne change rien a l'autre.

    py -3 tools/table_decors.py
    py -3 tools/table_decors.py --bgm      ajoute les 9 variantes de musique
    py -3 tools/table_decors.py --csv analysis/table_decors.csv
"""
import os
import re
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                          # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')

CODES = 0x18039F7A0            # 41 pointeurs vers "tst", "ts2", ...
TABLE = 0x180403430            # 41 descripteurs
PAS = 0xF0
N = 41


def chaine(img, va):
    if not va:
        return ''
    raw = img.read(va, 128)
    m = re.match(rb'[\x20-\x7e]{1,127}', raw or b'')
    return m.group().decode('latin1') if m else ''


def q(img, va):
    o = img.va2off(va)
    return struct.unpack_from('<Q', img.data, o)[0] if o is not None else 0


def d(img, va):
    o = img.va2off(va)
    v = struct.unpack_from('<I', img.data, o)[0] if o is not None else 0
    return v - 2**32 if v >= 2**31 else v


def main():
    img = P.Image(MOTEUR + '.origine')
    csv = None
    if '--csv' in sys.argv:
        csv = open(sys.argv[sys.argv.index('--csv') + 1], 'w',
                   encoding='utf-8', newline='\n')
        csv.write('index;code;nom;eff;objset_id;son_id;collision;'
                  'bgm_defaut;d0;d4;d8\n')
    print('%-3s %-6s %-10s %-12s %6s %7s  %s'
          % ('idx', 'code', 'nom', 'effets', 'objset', 'son', 'collision'))
    for i in range(N):
        code = chaine(img, q(img, CODES + 8 * i))
        r = TABLE + PAS * i
        nom = chaine(img, q(img, r + 0x00))
        eff = chaine(img, q(img, r + 0x08))
        objset = d(img, r + 0x10)
        son = d(img, r + 0x40)
        coli = chaine(img, q(img, r + 0x48))
        bgm = chaine(img, q(img, r + 0x68))
        print('%-3d %-6s %-10s %-12s %6d %7d  %s'
              % (i, code, nom, eff, objset, son,
                 coli.replace('rom/', '') or '-'))
        if '--bgm' in sys.argv:
            for k in range(9):
                v = chaine(img, q(img, r + 0x70 + 8 * k))
                if v:
                    print('        bgm[%d] %s' % (k, v))
            print('        bgm[9=defaut] %s' % (bgm or '-'))
        if csv:
            csv.write('%d;%s;%s;%s;%d;%d;%s;%s;%d;%d;%d\n'
                      % (i, code, nom, eff, objset, son, coli, bgm,
                         d(img, r + 0xD0), d(img, r + 0xD4),
                         d(img, r + 0xD8)))
    if csv:
        csv.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
