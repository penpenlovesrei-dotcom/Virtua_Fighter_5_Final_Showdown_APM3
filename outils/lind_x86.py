#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE TROISIEME BUILD : l'ELF x86 de la borne Lindbergh.

`extracted/LIND_FS/sel/vf5` -- 11,8 Mo, ELF 32 bits petit-boutiste (EM_386),
`rom_version` du 28/06/2010, livre avec `libsama.so` : c'est un binaire
D'ARCADE, pas de console. Il porte `VF5FS` et `Final Showdown`.

POURQUOI IL COMPTE. Il donne un TROISIEME point de comparaison, et il est le
plus lisible des trois :

  . son RTTI est l'ABI Itanium, donc les noms de classes sont en clair et les
    vtables s'en deduisent sans ambiguite ;
  . il garde les LIBELLES DE TACHES a cote des noms de types --
    `TERMINAL_ITEM_EQUIP`, `TERMIAL_ITEM_MAIN` (la coquille est d'origine),
    `ROB_AI`, `ROB_PREPA` -- ce qu'aucun des deux autres n'a ;
  . il nomme l'espace `terminal::` la ou APM3 dit `customize::`. La
    personnalisation n'est donc PAS une exclusivite console : l'arcade l'a,
    par le terminal a carte. C'est ce qui a tranche la question du 2026-10-04.

ATTENTION A L'IDENTIFICATION. Le dossier s'appelle `LIND_FS`, mais ce qui
decide c'est le CONTENU : `terminal9ItmEq` et `libsama.so` disent arcade,
`customize` dirait APM3 ou console. Une image ne se nomme pas par son dossier
-- l'erreur a ete faite une fois, en prenant `X360_FS` pour la console de
2007 alors que c'est la Final Showdown console, et `X360_VF5` pour la FS alors
que c'est celle de 2007.

L'ABI Itanium, dans ce sens :

    nom mangle         `N8terminal9ItmEqTaskE`, une chaine terminee par 0
    typeinfo           { vptr, const char* nom, typeinfo* base }
                       -> le champ `nom` pointe la chaine ; le typeinfo
                          commence donc 4 octets avant ce champ
    vtable             { offset-to-top, typeinfo*, creneau 0, creneau 1, ... }
                       -> le mot qui precede la vtable pointe le typeinfo ;
                          la vtable commence 4 octets apres.

ET LE PIEGE DES CRENEAUX : GCC pose DEUX destructeurs virtuels (complet puis
liberant), MSVC un seul. Le creneau de la mise a jour n'est donc PAS le meme
numero des deux cotes -- 2 chez MSVC, 3 ici. On ne transpose pas un numero de
creneau, on reconnait la fonction.

Usage :
    py -3 tools/lind_x86.py rtti                     toutes les classes
    py -3 tools/lind_x86.py rtti --grep ItmEq
    py -3 tools/lind_x86.py func 0x0849893C          desassembler
    py -3 tools/lind_x86.py func 0x08498AF6 --max 70
"""
import os
import re
import struct
import sys

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
ELF = os.path.join(RACINE, 'extracted', 'LIND_FS', 'sel', 'vf5')


class Refus(Exception):
    pass


class Image(object):
    def __init__(self, chemin=ELF):
        with open(chemin, 'rb') as fp:
            self.d = fp.read()
        if self.d[:4] != b'\x7fELF' or self.d[4] != 1 or self.d[5] != 1:
            raise Refus('%s n est pas un ELF 32 bits petit-boutiste'
                        % os.path.basename(chemin))
        phoff, = struct.unpack_from('<I', self.d, 0x1c)
        phentsize, = struct.unpack_from('<H', self.d, 0x2a)
        phnum, = struct.unpack_from('<H', self.d, 0x2c)
        self.seg = []
        for i in range(phnum):
            t, off, va, _pa, fsz, _msz, _fl, _al = struct.unpack_from(
                '<8I', self.d, phoff + i * phentsize)
            if t == 1 and fsz:                       # PT_LOAD
                self.seg.append((va, off, fsz))
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        self.md.detail = True

    def off(self, va):
        for v, o, n in self.seg:
            if v <= va < v + n:
                return o + (va - v)
        raise Refus('0x%08X hors des segments charges' % va)

    def va(self, off):
        for v, o, n in self.seg:
            if o <= off < o + n:
                return v + (off - o)
        return None

    def lire(self, va, n):
        o = self.off(va)
        return self.d[o:o + n]

    def mot(self, va):
        return struct.unpack_from('<I', self.d, self.off(va))[0]

    # -- RTTI ------------------------------------------------------------
    def _refs(self):
        if getattr(self, '_r', None) is None:
            r = {}
            for v, o, n in self.seg:
                for k in range(0, n - 3, 4):
                    x = struct.unpack_from('<I', self.d, o + k)[0]
                    if x:
                        r.setdefault(x, []).append(v + k)
            self._r = r
        return self._r

    def vtables(self, grep=None):
        """[(nom mangle, adresse de vtable, creneaux)] -- une par classe."""
        refs = self._refs()
        out = []
        motif = re.compile(rb'(?:N(?:[0-9]+[A-Za-z_][A-Za-z0-9_]*)+E|'
                           rb'[0-9]+[A-Za-z_][A-Za-z0-9_]*)\x00')
        for m in motif.finditer(self.d):
            nom = m.group()[:-1].decode('latin-1')
            if grep and grep not in nom:
                continue
            v_nom = self.va(m.start())
            if v_nom is None:
                continue
            for champ in refs.get(v_nom, ()):
                ti = champ - 4                       # typeinfo = nom - 4
                for q in refs.get(ti, ()):
                    vt = q + 4
                    cre = []
                    for i in range(10):
                        try:
                            c = self.mot(vt + 4 * i)
                        except Refus:
                            break
                        if not any(v <= c < v + n for v, _o, n in self.seg):
                            break
                        cre.append(c)
                    if cre:
                        out.append((nom, vt, cre))
        return sorted(set((n, v, tuple(c)) for n, v, c in out))


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    img = Image()
    if a[0] == 'rtti':
        grep = a[a.index('--grep') + 1] if '--grep' in a else None
        liste = img.vtables(grep)
        print('# %d vtable(s)   (GCC : creneaux 0 et 1 = les DEUX destructeurs)'
              % len(liste))
        for nom, vt, cre in liste:
            print('0x%08X  %s   %s'
                  % (vt, ' '.join('0x%08X' % c for c in cre), nom))
        return 0
    if a[0] == 'func':
        va = int(a[1], 0)
        n = int(a[a.index('--max') + 1]) if '--max' in a else 60
        o = img.off(va)
        for x in img.md.disasm(img.d[o:o + n * 10], va):
            print('  0x%08X  %-22s %s %s'
                  % (x.address, x.bytes.hex(), x.mnemonic, x.op_str))
            n -= 1
            if n <= 0:
                break
        return 0
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
