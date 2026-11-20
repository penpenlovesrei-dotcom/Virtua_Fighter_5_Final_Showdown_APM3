# -*- coding: utf-8 -*-
r"""Controle avant vol des DIX-NEUF decors de VF5 R, dans la DLL patchee.

DEPUIS LE 2026-09-11, CE CONTROLE COMPARE A VF5 R, PLUS A FINAL SHOWDOWN.

Frederic : « applique a VF5 R ses propres listes, rien ne doit venir de FS ».
Le patcheur relit desormais dans le binaire de VF5 R (`generation.py`) les
objets du descripteur, les taches d'effet, les murs, les animations, la
poussiere de chute et les dossiers d'effet. L'ancien controle attendait les
listes du MODELE FS : il aurait signale comme fautes exactement ce qu'on vient
de corriger (le tonnerre retire de hi5, les spectateurs rendus a bn5, les
quatre vrais panneaux de nc5).

Le controle est donc celui du VF5 d'origine, sur le lot de VF5 R : un seul
code pour les deux generations, et il relit la DLL par un autre chemin que le
patcheur. Voir `controle_decors_vf5.py`.

    py -3 tools/controle_decors_5r.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import controle_decors_vf5                                      # noqa: E402

if __name__ == '__main__':
    sys.exit(controle_decors_vf5.main('r'))
