#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Toutes les references a une adresse, par BALAYAGE LINEAIRE de `.text`.

Pourquoi cet outil existe. `pe_disasm.cmd_xref` itere sur `.pdata`. Or :

  * `.pdata` ne liste pas les fonctions FEUILLES (celles qui ne touchent ni la
    pile ni un registre non volatil) : les bouchons du moteur n'y sont pas ;
  * une fonction reelle couvre souvent plusieurs entrees `.pdata` chainees.

Consequence deja payee sur ce chantier : plusieurs « personne n'appelle X »
etaient faux. Une affirmation de non-reference exige un balayage lineaire.

Ici on ne desassemble pas : on cherche des MOTIFS D'OCTETS dans toute la
section executable, ce qui ne peut rien manquer (au prix de quelques faux
positifs, signales comme tels) :

  * `E8`/`E9` + rel32  tel que  fin + rel32 == cible      -> appel / saut
  * tout disp32 tel que fin_instruction + disp32 == cible -> reference
    RIP-relative. On ne sait pas ou finit l'instruction sans la decoder, donc
    on essaie les quatre queues possibles (0, 1, 2 et 4 octets d'immediat
    apres le deplacement), puis on VERIFIE en desassemblant en arriere.
  * l'adresse ecrite en clair sur 8 octets (pointeur absolu, vtable, table).

Usage :
    py -3 tools/refs_lineaires.py 0x1805C6DE0
    py -3 tools/refs_lineaires.py 0x1802D9920 --appels-seuls
    py -3 tools/refs_lineaires.py 0x1805C6DE0 --data     aussi hors `.text`
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import pe_disasm as P                                          # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')


def contenant(fs, va):
    lo, hi = 0, len(fs) - 1
    while lo <= hi:
        m = (lo + hi) // 2
        a, b = fs[m]
        if va < a:
            hi = m - 1
        elif va >= b:
            lo = m + 1
        else:
            return a
    return None


def decoder_autour(img, va, cible, recul=16):
    """Instruction couvrant `va` ET visant `cible` en RIP-relatif.

    On essaie CHAQUE depart possible et on garde celui qui verifie la
    condition, pas le premier qui decode : un depart mal aligne produit une
    instruction plausible mais fausse, et s'arreter dessus fait rater la vraie
    reference (defaut corrige le 2026-09-05, apres zero resultat sur un global
    dont `.pdata` donnait pourtant cinq references).
    """
    for r in range(1, recul):
        deb = va - r
        o = img.va2off(deb)
        if o is None:
            continue
        try:
            ins = next(img.md.disasm(img.data[o:o + 16], deb), None)
        except Exception:
            continue
        if not ins or not (ins.address <= va < ins.address + ins.size):
            continue
        if 'rip' not in ins.op_str:
            continue
        for op in ins.operands:
            import capstone
            if (op.type == capstone.x86.X86_OP_MEM
                    and op.mem.base == capstone.x86.X86_REG_RIP
                    and ins.address + ins.size + op.mem.disp == cible):
                return ins
    return None


def chercher(img, cible, avec_data=False):
    hits = []
    secs = img.secs if avec_data else [s for s in img.secs if s['exec']]
    for s in secs:
        blob = img.data[s['off']:s['off'] + s['rsize']]
        base = s['va']
        n = len(blob)
        # 1. appels / sauts relatifs
        if s['exec']:
            for i in range(n - 4):
                b = blob[i]
                if b not in (0xE8, 0xE9):
                    continue
                rel = struct.unpack_from('<i', blob, i + 1)[0]
                if base + i + 5 + rel == cible:
                    hits.append((base + i, 'appel' if b == 0xE8 else 'saut',
                                 None))
        # 2. references RIP-relatives (quatre queues possibles)
        if s['exec']:
            for i in range(n - 4):
                disp = struct.unpack_from('<i', blob, i + 4 - 4)[0] \
                    if False else struct.unpack_from('<i', blob, i)[0]
                if disp == 0:
                    continue
                for queue in (0, 1, 2, 4):
                    if base + i + 4 + queue + disp != cible:
                        continue
                    ins = decoder_autour(img, base + i, cible)
                    if ins is None:
                        continue
                    hits.append((ins.address, 'rip',
                                 '%s %s' % (ins.mnemonic, ins.op_str)))
                    break
        # 3. pointeur absolu sur 8 octets
        for i in range(0, n - 8, 4):
            if struct.unpack_from('<Q', blob, i)[0] == cible:
                hits.append((base + i, 'ptr64[%s]' % s['name'], None))
    # dedoublonner
    vus = set()
    out = []
    for va, genre, txt in hits:
        cle = (va, genre)
        if cle in vus:
            continue
        vus.add(cle)
        out.append((va, genre, txt))
    out.sort()
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    cible = int(sys.argv[1], 0)
    chemin = MOTEUR + ('' if '--patche' in sys.argv else '.origine')
    img = P.Image(chemin)
    fs = P.runtime_functions(img)
    hits = chercher(img, cible, avec_data='--data' in sys.argv)
    if '--appels-seuls' in sys.argv:
        hits = [h for h in hits if h[1] in ('appel', 'saut')]
    print('cible 0x%X : %d reference(s)' % (cible, len(hits)))
    for va, genre, txt in hits:
        f = contenant(fs, va)
        print('  0x%-12X %-12s %-46s %s'
              % (va, genre, txt or '',
                 ('dans 0x%X' % f) if f else '(hors .pdata)'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
