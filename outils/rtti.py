#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reconstruit le RTTI MSVC x64 d'un PE : classe <-> vtable.

`tools/extract_rtti.py` ne sait lire que l'ABI Itanium (le build PS3, ELF).
Le moteur APM3 est un PE MSVC : ses noms de classes se retrouvent par une
chaine tout autre, et jusqu'ici elle etait refaite a la main a chaque fois.

La chaine, dans ce sens :

    TypeDescriptor          nom `.?AVMaClasse@@`, la structure commence
                            0x10 octets AVANT la chaine
    CompleteObjectLocator   { signature=1, offset, cdOffset,
                              rva(TypeDescriptor), rva(ClassDescriptor),
                              rva(self) }   <- 24 octets, et `rva(self)` est
                            ce qui rend la reconnaissance sure
    vtable                  le qword qui PRECEDE la vtable pointe sur le COL ;
                            la vtable commence donc 8 octets apres.

Sortie : une ligne par vtable, triee par nom de classe.

    py -3 tools/rtti.py                       le moteur, sur stdout
    py -3 tools/rtti.py --out analysis/rtti_apm3.txt
    py -3 tools/rtti.py --grep AVLink         ne garder que ces classes
    py -3 tools/rtti.py --pe chemin.dll

Toujours lu sur `.origine` : le RTTI ne bouge pas, mais on n'analyse jamais le
binaire patche.
"""
import os
import re
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                        # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')


def joli(mangled):
    """`.?AVTaskMenuMain@@` -> `TaskMenuMain` ; garde les espaces de noms."""
    s = mangled
    if s.startswith('.?A'):
        s = s[3:]
    if s[:1] in ('V', 'U'):                  # V = class, U = struct
        s = s[1:]
    if s.endswith('@@'):
        s = s[:-2]
    parts = [p for p in s.split('@') if p]
    return '::'.join(reversed(parts)) if len(parts) > 1 else s


def collecter(img):
    base = img.base
    # 1. les TypeDescriptor, par leur nom
    tds = {}                                             # va(TD) -> mangled
    for m in re.finditer(rb'\.\?A[VU][\x21-\x7e]{1,250}?@@\x00', img.data):
        va = img.off2va(m.start())
        if va is None:
            continue
        tds[va - 0x10] = m.group()[:-1].decode('latin-1')

    # 2. les CompleteObjectLocator : 24 octets, signature 1, self-RVA exact
    cols = {}                                            # va(COL) -> va(TD)
    for s in img.secs:
        if s['exec']:
            continue
        blob = img.data[s['off']:s['off'] + s['rsize']]
        for off in range(0, max(0, len(blob) - 24), 4):
            sig, _o, _c, td, _cd, self_ = struct.unpack_from('<6I', blob, off)
            if sig != 1:
                continue
            va = s['va'] + off
            if base + self_ != va:
                continue
            if base + td in tds:
                cols[va] = base + td

    # 3. les vtables : le qword qui precede pointe sur un COL
    vtables = []                                         # (va(vt), nom)
    for s in img.secs:
        if s['exec']:
            continue
        blob = img.data[s['off']:s['off'] + s['rsize']]
        for off in range(0, max(0, len(blob) - 8), 8):
            q = struct.unpack_from('<Q', blob, off)[0]
            if q in cols:
                vtables.append((s['va'] + off + 8, joli(tds[cols[q]])))
    return tds, cols, vtables


def main():
    argv = sys.argv[1:]
    chemin = MOTEUR
    if '--pe' in argv:
        chemin = argv[argv.index('--pe') + 1]
    motif = None
    if '--grep' in argv:
        motif = re.compile(argv[argv.index('--grep') + 1], re.I)

    img = P.Image(chemin)
    tds, cols, vtables = collecter(img)

    lignes = ['# %s' % os.path.basename(chemin),
              '# %d TypeDescriptor, %d CompleteObjectLocator, %d vtables'
              % (len(tds), len(cols), len(vtables)),
              '# vtable            creneaux [0] [1] [2] ...   classe',
              '']
    for va, nom in sorted(vtables, key=lambda t: (t[1], t[0])):
        if motif and not motif.search(nom):
            continue
        creneaux = []
        for i in range(4):
            q = img.read(va + i * 8, 8)
            if len(q) < 8:
                break
            creneaux.append('0x%X' % struct.unpack('<Q', q)[0])
        lignes.append('0x%09X  %-58s %s'
                      % (va, ' '.join(creneaux), nom))

    texte = os.linesep.join(lignes) + os.linesep
    if '--out' in argv:
        dest = argv[argv.index('--out') + 1]
        if not os.path.isabs(dest):
            dest = os.path.join(RACINE, dest)
        with open(dest, 'w', encoding='utf-8') as fp:
            fp.write(texte)
        print('%d vtables -> %s' % (len(vtables), dest))
    else:
        sys.stdout.write(texte)
    return 0


if __name__ == '__main__':
    sys.exit(main())
