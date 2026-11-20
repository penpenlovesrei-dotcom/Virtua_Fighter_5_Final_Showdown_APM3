#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TOUT CE QUI TOUCHE UNE PLAGE D'OCTETS d'une structure, en UNE passe.

Pourquoi il manquait (2026-10-04). `champ_x64.py` cherche un deplacement
EXACT. Or un octet peut etre ecrit sans qu'aucune instruction ne porte son
deplacement :

  . par un acces PLUS LARGE -- `mov word [rcx+0x795], 0x0101` ecrit 0x795 ET
    0x796, et un releve au deplacement 0x796 n'en voit rien ;
  . par une base DEJA DECALEE -- du code qui tient `p = base+0x700` ecrit
    `[p+0x96]`, et le deplacement vu est 0x96.

Le premier cas se rattrape exactement : il suffit de retenir un acces des que
son INTERVALLE [dep, dep+taille[ recouvre l'octet cherche. Le second ne se
rattrape pas par deplacement, mais il se voit AUTREMENT : en relevant tout le
VOISINAGE de l'octet, on trouve les champs de la meme zone, et le code qui les
touche est le meme code.

« Un releve vide n'est pas une reponse. » Celui-ci dit donc, pour chaque octet
d'une plage, qui le lit et qui l'ecrit -- quelle que soit la largeur de
l'acces.

Meme precaution anti-fantome que `champ_x64.py` : seize deputs decales, et un
acces n'est retenu que si plusieurs deputs s'accordent sur ses octets.

Usage :
    py -3 tools/voisinage_x64.py 0x790 0x7A0
    py -3 tools/voisinage_x64.py 0x790 0x7A0 --couvre 0x796
    py -3 tools/voisinage_x64.py 0x0 0x40 --plage 0x1801C0000 0x1801D0000
"""
import os
import sys

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                        # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')

PILE = (capstone.x86.X86_REG_RSP, capstone.x86.X86_REG_RBP,
        capstone.x86.X86_REG_RIP)


def balayer(img, lo, hi, deputs=16, accord=3, plage=None):
    """{adresse: [octets, texte, ecrit, dep, taille, accords]}."""
    vus = {}
    for s in img.secs:
        if not s.get('exec'):
            continue
        va0, n = s['va'], s['vsize']
        if plage is not None:
            va0 = max(va0, plage[0])
            n = min(s['va'] + s['vsize'], plage[1]) - va0
        if n <= 0:
            continue
        blob = img.data[s['off'] + (va0 - s['va']):][:n]
        for d in range(deputs):
            i = d
            while i < len(blob):
                fin = i
                for x in img.md.disasm(blob[i:], va0 + i):
                    fin = (x.address - va0) + x.size
                    _retenir(vus, x, lo, hi)
                i = fin + 1 if fin > i else i + 1
    return {va: v for va, v in vus.items() if v[5] >= accord}


def _retenir(vus, x, lo, hi):
    for op in x.operands:
        if op.type != capstone.x86.X86_OP_MEM:
            continue
        dep, taille = op.mem.disp, op.size
        if dep + taille <= lo or dep >= hi:
            continue
        if op.mem.base in PILE or op.mem.base == 0:
            continue
        e = vus.get(x.address)
        if e is None:
            prem = x.operands[0]
            ecrit = (prem.type == capstone.x86.X86_OP_MEM
                     and prem.mem.disp == dep
                     and x.mnemonic not in ('cmp', 'test'))
            vus[x.address] = [x.bytes.hex(),
                              '%s %s' % (x.mnemonic, x.op_str),
                              ecrit, dep, taille, 0]
        elif e[0] != x.bytes.hex():
            return
        vus[x.address][5] += 1
        return


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        print(__doc__)
        return 1
    lo, hi = int(a[0], 0), int(a[1], 0)
    couvre = None
    if '--couvre' in a:
        couvre = int(a[a.index('--couvre') + 1], 0)
    plage = None
    if '--plage' in a:
        k = a.index('--plage')
        plage = (int(a[k + 1], 0), int(a[k + 2], 0))
    chemin = MOTEUR + ('' if '--patche' in a else '.origine')
    img = P.Image(chemin)
    print('image : %s' % os.path.basename(chemin))
    liste = balayer(img, lo, hi, plage=plage)
    if couvre is not None:
        liste = {k: v for k, v in liste.items()
                 if v[3] <= couvre < v[3] + v[4]}
        print('ce qui RECOUVRE l octet +0x%X :' % couvre)
    else:
        print('ce qui touche [+0x%X, +0x%X[ :' % (lo, hi))
    ecr = [v for v in liste.values() if v[2]]
    print('%d acces confirme(s), dont %d ECRITURE(S)' % (len(liste), len(ecr)))
    print('-' * 78)
    for va in sorted(liste):
        octets, texte, est_ecr, dep, taille, n = liste[va]
        print('  0x%09X  %-5s +0x%-5X %d o  %-42s [%d]'
              % (va, 'ECRIT' if est_ecr else 'lit', dep, taille, texte, n))
    return 0


if __name__ == '__main__':
    sys.exit(main())
