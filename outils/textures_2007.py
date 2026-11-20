# -*- coding: utf-8 -*-
"""Sort les textures d un jeu de sprites de 2007 en PNG.

    py -3 sortir_textures_2007.py spr_n_que.farc [spr_n_qwin.farc ...]

Les PNG vont dans le scratchpad, nommes <archive>__texNN.png.
"""
import os
import sys

TOOLS = r'C:\Users\frede\Desktop\VF5RE\tools'
sys.path.insert(0, TOOLS)
import textures_hd as T                                  # noqa: E402
import txp                                               # noqa: E402

SRC = r'C:\Users\frede\Desktop\VF5 FS DECOMP\X360_VF5\media\rom\2d'
OUT = (r'C:\Users\frede\AppData\Local\Temp\claude'
       r'\C--Users-frede-Desktop-VF5RE'
       r'\286302d2-da8d-4adf-9c17-6ab3530084cc\scratchpad\tex2007')

os.makedirs(OUT, exist_ok=True)
for nom in sys.argv[1:]:
    chemin = os.path.join(SRC, nom)
    if not os.path.exists(chemin):
        print('absent : %s' % chemin)
        continue
    try:
        m = T.membres(chemin)
    except Exception as e:                                # noqa: BLE001
        print('%s : illisible (%s)' % (nom, e))
        continue
    for fich, d in m.items():
        if not fich.endswith('.bin'):
            continue
        _t, textures = T.lire_txp(d)
        if not textures:
            continue
        base = nom[:-5]
        print('%s : %d texture(s)' % (nom, len(textures)))
        for k, tex in enumerate(textures):
            n0 = tex['niveaux'][0]
            et = '%s__tex%02d.png' % (base, k)
            try:
                im = txp.image({'larg': n0['larg'], 'haut': n0['haut'],
                                'format': n0['format'],
                                'octets': n0['octets']})
                im.save(os.path.join(OUT, et))
                print('   %-28s %4d x %-4d' % (et, n0['larg'], n0['haut']))
            except Exception as ex:                       # noqa: BLE001
                print('   %-28s NON SORTIE : %s' % (et, ex))
print()
print('dossier : %s' % OUT)
