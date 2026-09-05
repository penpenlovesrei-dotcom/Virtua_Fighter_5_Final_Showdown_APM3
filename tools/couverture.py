#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ce que le mode console touche vraiment, et ce qu'on en a lu.

Frederic, apres que le combat a demarre : « tu as desassemble tout le
fonctionnement du mode console ? tu avais omis les inputs playstation, il reste
quoi d'inconnu ? ». La reponse honnete demande un DENOMINATEUR, pas une
impression : on part des gestionnaires de la machine a etats, on suit le graphe
d'appels directs, et on compte.

Ce que l'outil NE fait pas : deviner ce qu'on a compris. Il donne la surface a
couvrir ; la liste de ce qui est lu est tenue a la main dans
`analysis/couverture_console.md`.

    py -3 tools/couverture.py
"""
import collections
import os
import re
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import capstone                                              # noqa: E402
import pe_disasm as P                                        # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')
TABLE_MODES = 0x1803A0190
TABLE_SOUS_ETATS = 0x1803A05A0
BOUCHONS = {0x180007430, 0x180007440, 0x180007450, 0x180029FB0, 0x1801294B0}
MODES = ['STARTUP', 'ADVERTISE', 'GAME', 'DATA_TEST', 'MENU', 'CS_TERM',
         'CS_TRAINING', 'ONLINE', 'APM3', 'APM3_TESTMODE']
# les modes que le parcours CONSOLE emprunte reellement
CONSOLE = {0, 2, 4, 5, 6}


def main():
    img = P.Image(MOTEUR)
    d = img.data
    fs = P.runtime_functions(img)
    debuts = sorted(a for a, b in fs)
    taille = {a: b - a for a, b in fs}
    fin = {a: b for a, b in fs}

    def contenant(va):
        i = 0
        for a in debuts:
            if a > va:
                break
            i = a
        return i if i and va < fin.get(i, 0) else None

    # graphe d'appels directs
    appels = collections.defaultdict(set)
    chaines = collections.defaultdict(list)
    for a, b in fs:
        o = img.va2off(a)
        if o is None:
            continue
        for x in img.md.disasm(d[o:o + (b - a)], a):
            if x.mnemonic == 'call' and x.op_str.startswith('0x'):
                appels[a].add(int(x.op_str, 16))
            for op in x.operands:
                if (op.type == capstone.x86.X86_OP_MEM
                        and op.mem.base == capstone.x86.X86_REG_RIP
                        and x.mnemonic == 'lea'):
                    t = x.address + x.size + op.mem.disp
                    raw = img.read(t, 64)
                    m = re.match(rb'[\x20-\x7e]{4,40}', raw) if raw else None
                    if m:
                        chaines[a].append(m.group().decode('latin-1'))

    def racines():
        out = []
        for i in range(10):
            o = img.va2off(TABLE_MODES + 0x68 * i)
            cle = struct.unpack_from('<I', d, o)[0]
            h = [struct.unpack_from('<Q', d, o + 8 + 8 * k) for k in range(3)]
            if cle in CONSOLE:
                out += [x[0] for x in h if x[0] not in BOUCHONS]
        for i in range(55):
            o = img.va2off(TABLE_SOUS_ETATS + 0x20 * i)
            h = [struct.unpack_from('<Q', d, o + 8 + 8 * k)[0] for k in range(3)]
            vivants = [x for x in h if x not in BOUCHONS]
            if len(vivants) == 3:                 # sous-etat entierement vivant
                out += vivants
        return sorted(set(out))

    vus = set()
    pile = [r for r in racines()]
    while pile:
        f = pile.pop()
        f = contenant(f) or f
        if f in vus or f in BOUCHONS:
            continue
        vus.add(f)
        for c in appels.get(f, ()):
            c2 = contenant(c) or c
            if c2 not in vus:
                pile.append(c2)

    octets = sum(taille.get(f, 0) for f in vus)
    print('SURFACE DU MODE CONSOLE (graphe d appels directs)')
    print()
    print('  fonctions du binaire     : %6d   (%d octets)'
          % (len(fs), sum(taille.values())))
    print('  atteintes depuis les gestionnaires vivants : %6d   (%d octets)'
          % (len(vus), octets))
    print('  soit %.0f %% du binaire' % (100.0 * octets / sum(taille.values())))
    print()
    print('  Rappel : ce chiffre est un MAJORANT de ce qu il faudrait lire, et')
    print('  un MINORANT de la surface reelle -- les appels indirects (vtables,')
    print('  rappels) n y sont pas.')
    print()
    zones = collections.Counter()
    for f in vus:
        zones[f & ~0xFFFF] += taille.get(f, 0)
    print('  par zone de 64 Ko, les douze plus grosses :')
    for z, n in zones.most_common(12):
        noms = []
        for f in vus:
            if f & ~0xFFFF == z:
                noms += [s for s in chaines.get(f, ())
                         if s.isupper() or '_' in s or ' ' in s]
        ech = ', '.join(dict.fromkeys(noms).keys()) if noms else ''
        print('    0x%09X  %6d o   %s' % (z, n, ech[:90]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
