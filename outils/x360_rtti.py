#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Classe <-> vtable dans l'image PowerPC : le pont qui manquait.

CE QU'IL CORRIGE (2026-10-04). Le journal (113) a conclu « le RTTI ne mene pas
aux vtables cote console, les descripteurs ne sont references nulle part », et
en a deduit qu'on ne pouvait pas trouver la mise a jour d'une classe cote
Xbox 360. C'ETAIT FAUX, et l'erreur tenait a HUIT OCTETS :

    en PE 64 bits  TypeDescriptor = { void* pVFTable; void* spare; char nom[] }
                   -> la structure commence 0x10 avant la chaine
    en PE 32 bits  les deux pointeurs font quatre octets
                   -> elle commence 0x8 avant la chaine

`tools/rtti.py` est ecrit pour le moteur x64 et cherche donc a -0x10. Applique
tel quel a une image 32 bits, il cherche des references a une adresse qui ne
designe rien, n'en trouve aucune, et le releve vide passe pour une reponse.
C'est le piege deja consigne : « un releve vide n'est pas une reponse ».

Et la difference ne s'arrete pas la : le COL x64 porte des RVA et un
`rva(self)` qui rend la reconnaissance sure ; le COL 32 bits porte des adresses
ABSOLUES et n'a pas de `self`. On le reconnait donc autrement -- signature
nulle et `pTypeDescriptor` a +0xC.

    TypeDescriptor        nom `.?AVMaClasse@@`, structure a -8
    COL                   { signature=0, offset, cdOffset, pTD, pCHD }
    vtable                le mot qui PRECEDE la vtable pointe sur le COL ;
                          la vtable commence donc 4 octets apres.

Le creneau 2 est la mise a jour pour toutes les taches du moteur -- verifie des
deux cotes sur `customize::ItmEqTask`, `customize::ItemMain`, `TaskRobSingle`
et `TaskRobVersus`.

Usage :
    py -3 tools/x360_rtti.py                     tout, trie par nom
    py -3 tools/x360_rtti.py --grep TaskRob      ne garder que ces classes
"""
import os
import re
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import x360_ppc                                              # noqa: E402


def charger():
    img = x360_ppc.Image()
    return img, img.d


def mot(d, va):
    o = va - 0x82000000
    return struct.unpack_from('>I', d, o)[0]


def table(grep=None):
    img, d = charger()
    # 1. les descripteurs de type : la chaine, et la structure a -8.
    noms = {}
    for m in re.finditer(rb'\.\?AV[\x20-\x7E]{1,200}?@@', d):
        va_nom = m.start() + 0x82000000
        noms[va_nom - 8] = m.group().decode('latin-1')

    # 2. toutes les references absolues, en un seul balayage.
    refs = {}
    for o in range(0, len(d) - 3, 4):
        v = struct.unpack_from('>I', d, o)[0]
        if 0x82000000 <= v < 0x82000000 + len(d):
            refs.setdefault(v, []).append(o + 0x82000000)

    # 3. descripteur -> COL -> vtable.
    out = []
    for td, nom in noms.items():
        if grep and grep not in nom:
            continue
        for r in refs.get(td, ()):
            col = r - 0xC
            try:
                if mot(d, col) != 0 or mot(d, col + 0xC) != td:
                    continue
            except struct.error:
                continue
            for v in refs.get(col, ()):
                creneaux = []
                for i in range(1, 9):
                    try:
                        creneaux.append(mot(d, v + 4 * i))
                    except struct.error:
                        break
                out.append((nom, v + 4, creneaux))
    return sorted(out, key=lambda x: x[0])


def main():
    grep = None
    if '--grep' in sys.argv:
        grep = sys.argv[sys.argv.index('--grep') + 1]
    liste = table(grep)
    print('# %d vtable(s)' % len(liste))
    print('# vtable      creneaux [0] [1] [2=update] [3] ...   classe')
    for nom, vt, cre in liste:
        # On s'arrete au premier mot qui ne ressemble pas a du code : les
        # vtables sont suivies de donnees, et les imprimer ferait croire a
        # des creneaux qui n'existent pas.
        bons = []
        for c in cre:
            if not (0x82000000 <= c < 0x82600000):
                break
            bons.append(c)
        print('0x%08X  %s   %s'
              % (vt, ' '.join('0x%08X' % c for c in bons) or '(aucun)', nom))
    return 0


if __name__ == '__main__':
    sys.exit(main())
