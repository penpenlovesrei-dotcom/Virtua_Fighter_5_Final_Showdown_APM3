#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MESURE, et rien d'autre : qui lit quel bit du masque arcade, et quels
codes du stub `apm.dll` le moteur interroge reellement.

Ecrit pour le VOLET A (« le mode TERMINAL ne valide ni n'annule »). Avant
d'ajouter la moindre lecture dans `0x180243ED0`, il faut savoir :

  1. quels codes `Input_isOn` / `Input_isOnNow` le moteur demande deja
     (donc quels codes du stub sont LIBRES) ;
  2. quelles fonctions lisent les bits 8 (`0x100`) et 11 (`0x800`) du
     masque arcade -- si une autre que l'ecran de personnalisation les lit,
     leur donner une source CHANGE SON COMPORTEMENT ;
  3. ou poser un detour de cinq octets dans `0x180243ED0` sans avaler ni
     une cible de saut ni une frontiere d'instruction.

Aucune supposition : tout sort du desassemblage du `.origine`.

    py -3 tools/boutons_terminal.py              tout
    py -3 tools/boutons_terminal.py --codes      seulement les codes du stub
    py -3 tools/boutons_terminal.py --masques    seulement les bits du masque
    py -3 tools/boutons_terminal.py --detour     seulement le site du detour
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import capstone                                              # noqa: E402
import pe_disasm as P                                        # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')

# Les deux lecteurs de masque arcade. Mesures (desassemblage, pas suppose) :
#   0x1801A2CA0(ecx = masque, dl)  dl != 0 -> champ +0x18 (repetition)
#                                  dl == 0 -> champ +0x10 (FRONT)
#   0x1801A2C10(ecx = masque)      champ +0x08 (TENU)
# Les deux rendent l'indice du joueur, ou -1.
LECTEURS = {0x1801A2CA0: 'front/repet', 0x1801A2C10: 'tenu'}
# Le creneau de vtable de l'objet d'entrees [0x180C3B6F8].
CRENEAUX = {0x158: 'Input_isOn', 0x160: 'Input_isOnNow'}
ENTREES_OBJET = 0x180C3B6F8
LECTEUR_MOTEUR = 0x180243ED0            # celui qui compose le masque
MASQUE_BASE = 0x180751040               # l'etat d'entrees, 0x54 par joueur

BITS_SANS_SOURCE = {8: '0x100', 10: '0x400', 11: '0x800',
                    20: '0x100000', 21: '0x200000', 22: '0x400000',
                    23: '0x800000'}


def pdata(img):
    """Les (debut, fin) de .pdata, tries. Une entree = un FRAGMENT."""
    d = img.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
    va, taille = img.base + d.VirtualAddress, d.Size
    brut = img.read(va, taille)
    out = []
    for i in range(0, len(brut) - 11, 12):
        deb, fin, _ = struct.unpack_from('<III', brut, i)
        if deb and fin > deb:
            out.append((img.base + deb, img.base + fin))
    out.sort()
    return out


def fonction_de(frag, va):
    """Le fragment .pdata qui contient `va`, ou None."""
    lo, hi = 0, len(frag)
    while lo < hi:
        mi = (lo + hi) // 2
        if frag[mi][0] <= va:
            lo = mi + 1
        else:
            hi = mi
    if lo and frag[lo - 1][0] <= va < frag[lo - 1][1]:
        return frag[lo - 1]
    return None


def balayer(img, frag):
    """Desassemble chaque fragment, et rend les trois releves.

    Suivi minimal de registres : le dernier immediat charge dans `ecx` et
    dans `edx`. C'est tout ce dont les deux lecteurs ont besoin (le masque
    arrive en `ecx`, le code en `edx`).
    """
    md = img.md
    appels, codes, refs = [], [], []
    for deb, fin in frag:
        off = img.va2off(deb)
        if off is None:
            continue
        brut = img.data[off:off + (fin - deb)]
        ecx = edx = None
        for ins in md.disasm(brut, deb):
            m, ops = ins.mnemonic, ins.op_str
            if m == 'mov' and ops.startswith('ecx, 0x'):
                ecx = int(ops.split(', ')[1], 16)
            elif m == 'mov' and ops.startswith('ecx, ') and \
                    ops.split(', ')[1].isdigit():
                ecx = int(ops.split(', ')[1])
            elif m == 'xor' and ops == 'ecx, ecx':
                ecx = 0
            elif m == 'mov' and ops.startswith('edx, 0x'):
                edx = int(ops.split(', ')[1], 16)
            elif m == 'mov' and ops.startswith('edx, ') and \
                    ops.split(', ')[1].isdigit():
                edx = int(ops.split(', ')[1])
            elif m == 'xor' and ops == 'edx, edx':
                edx = 0
            elif m == 'lea' and ops.startswith('edx, [rbp'):
                # l'idiome de 0x180243ED0 : rbp = l'indice du joueur, et le
                # code demande vaut « base + joueur » (ou « base + 16*joueur »
                # une fois --joueur2 pose).
                try:
                    edx = ('rbp', int(ops.split('+')[1].rstrip(']'), 0))
                except (IndexError, ValueError):
                    edx = ('rbp', None)
            elif ops.startswith('ecx,') or ops.startswith('edx,'):
                if m not in ('cmp', 'test'):
                    if ops.startswith('ecx,'):
                        ecx = None
                    else:
                        edx = None
            if m == 'call' and ops.startswith('0x'):
                cible = int(ops, 16)
                if cible in LECTEURS:
                    appels.append((ins.address, (deb, fin), cible, ecx, edx))
            elif m == 'call' and ops.startswith('qword ptr [rax + 0x1'):
                try:
                    cr = int(ops.split('+ ')[1].rstrip(']'), 16)
                except ValueError:
                    cr = None
                if cr in CRENEAUX:
                    codes.append((ins.address, (deb, fin), cr, edx))
            # toute reference a l'etat d'entrees lui-meme
            for x in ins.operands:
                if x.type == capstone.x86.X86_OP_MEM and \
                        x.mem.base == capstone.x86.X86_REG_RIP:
                    cible = ins.address + ins.size + x.mem.disp
                    if MASQUE_BASE <= cible < MASQUE_BASE + 0x54 * 2:
                        refs.append((ins.address, (deb, fin), cible,
                                     '%s %s' % (m, ops)))
    return appels, codes, refs


def nom(va):
    return '0x%X' % va


def montrer_codes(codes):
    print('=' * 78)
    print('1. LES CODES QUE LE MOTEUR DEMANDE AU STUB apm.dll')
    print('=' * 78)
    print()
    print('Tout appel a `[objet_entrees + 0x158]` (Input_isOn) ou `+0x160`')
    print('(Input_isOnNow), avec le code demande.')
    print()
    fixes, variables = {}, []
    for site, fn, cr, edx in codes:
        if isinstance(edx, int):
            fixes.setdefault(edx, []).append((site, fn, cr))
        else:
            variables.append((site, fn, cr, edx))
    print('%-6s %-14s %-8s %s' % ('code', 'creneau', 'sites', 'fonctions'))
    print('-' * 78)
    for code in sorted(fixes):
        crs = sorted({CRENEAUX[c] for _, _, c in fixes[code]})
        fns = sorted({fn[0] for _, fn, _ in fixes[code]})
        print('%-6d %-14s %-8d %s'
              % (code, '/'.join(crs), len(fixes[code]),
                 ' '.join(nom(f) for f in fns[:6])
                 + (' ...' if len(fns) > 6 else '')))
    print()
    if variables:
        print('Sites a code CALCULE (idiome `lea edx, [rbp+N]`) :')
        for site, fn, cr, edx in variables:
            print('   0x%X  dans %s  %s  edx = %s'
                  % (site, nom(fn[0]), CRENEAUX[cr], edx))
        print()
    pris = set(fixes)
    for _, _, _, edx in variables:
        if isinstance(edx, tuple) and edx[1] is not None:
            # joueur 0 et joueur 1 : base + 0 et base + 16 (apres --joueur2)
            pris.add(edx[1])
            pris.add(edx[1] + 16)
    libres = [c for c in range(32) if c not in pris]
    print('CODES PRIS  : %s' % ', '.join(str(c) for c in sorted(pris)))
    print('CODES LIBRES (0..31) : %s' % ', '.join(str(c) for c in libres))
    print()
    return pris, libres


def montrer_masques(appels):
    print('=' * 78)
    print('2. QUI LIT QUEL BIT DU MASQUE ARCADE')
    print('=' * 78)
    print()
    par_fonction = {}
    for site, fn, cible, ecx, _ in appels:
        par_fonction.setdefault(fn, []).append((site, cible, ecx))
    print('%d sites d appel, dans %d fonctions.'
          % (len(appels), len(par_fonction)))
    print()
    print('%-14s %-7s %-12s %s' % ('fonction', 'sites', 'lecteur', 'masques'))
    print('-' * 78)
    for fn in sorted(par_fonction):
        sites = par_fonction[fn]
        lect = sorted({LECTEURS[c] for _, c, _ in sites})
        masques = sorted({e for _, _, e in sites if e is not None})
        inconnus = sum(1 for _, _, e in sites if e is None)
        print('%-14s %-7d %-12s %s%s'
              % (nom(fn[0]), len(sites), '/'.join(lect),
                 ' '.join('0x%X' % m for m in masques),
                 '  (+%d calcules)' % inconnus if inconnus else ''))
    print()
    print('LES BITS SANS SOURCE, ET QUI LES DEMANDE :')
    print()
    for bit in sorted(BITS_SANS_SOURCE):
        val = 1 << bit
        porteurs = {}
        for site, fn, cible, ecx, _ in appels:
            if ecx is not None and ecx & val:
                porteurs.setdefault(fn, []).append((site, cible, ecx))
        if not porteurs:
            print('   bit %-2d %-10s : PERSONNE ne le lit.'
                  % (bit, BITS_SANS_SOURCE[bit]))
            continue
        print('   bit %-2d %-10s : %d site(s), %d fonction(s)'
              % (bit, BITS_SANS_SOURCE[bit],
                 sum(len(v) for v in porteurs.values()), len(porteurs)))
        for fn in sorted(porteurs):
            for site, cible, ecx in porteurs[fn]:
                print('        0x%X  dans %-12s  %-11s  masque 0x%X'
                      % (site, nom(fn[0]), LECTEURS[cible], ecx))
    print()


def montrer_refs(refs):
    print('=' * 78)
    print('3. TOUTE AUTRE REFERENCE A L ETAT D ENTREES (0x%X + 0x54*joueur)'
          % MASQUE_BASE)
    print('=' * 78)
    print()
    if not refs:
        print('   aucune, hors les deux lecteurs.')
    for site, fn, cible, txt in refs:
        print('   0x%X  dans %-12s  -> 0x%X   %s'
              % (site, nom(fn[0]), cible, txt))
    print()


def montrer_detour(img):
    print('=' * 78)
    print('4. OU POSER LE DETOUR DANS 0x%X' % LECTEUR_MOTEUR)
    print('=' * 78)
    print()
    frag = pdata(img)
    f = fonction_de(frag, LECTEUR_MOTEUR)
    deb, fin = f
    off = img.va2off(deb)
    brut = img.data[off:off + (fin - deb)]
    ins = list(img.md.disasm(brut, deb))
    cibles = set()
    for i in ins:
        if i.group(capstone.CS_GRP_JUMP) and i.op_str.startswith('0x'):
            cibles.add(int(i.op_str, 16))
    print('Fragment .pdata : 0x%X .. 0x%X (%d octets, %d instructions)'
          % (deb, fin, fin - deb, len(ins)))
    print('Cibles de saut INTERNES : %s'
          % ' '.join('0x%X' % c for c in sorted(cibles)))
    print()
    print('Les plus courtes suites de >= 5 octets qui n avalent AUCUNE cible')
    print('de saut et qui tombent pile sur des frontieres d instruction :')
    print()
    print('%-22s %-6s %s' % ('plage', 'octets', 'instructions avalees'))
    print('-' * 78)
    n = len(ins)
    trouves = []
    for i in range(n):
        if ins[i].address in cibles:
            continue              # la premiere instruction EST une cible
        for j in range(i + 1, n + 1):
            a = ins[i].address
            b = ins[j].address if j < n else fin
            if b - a > 24:
                break
            if j - 1 > i and ins[j - 1].address in cibles:
                break
            if b - a < 5:
                continue
            trouves.append((a, b, list(ins[i:j])))
            break
    for a, b, bloc in trouves:
        print('0x%X..0x%X  %-6d %s'
              % (a, b, b - a,
                 ' ; '.join('%s %s' % (k.mnemonic, k.op_str)
                            for k in bloc)[:56]))
    print()
    return trouves


def main():
    argv = sys.argv[1:]
    tout = not argv
    img = P.Image(MOTEUR)
    frag = pdata(img)
    print()
    print('MESURE DES ENTREES -- %s' % os.path.basename(MOTEUR))
    print()
    if tout or '--codes' in argv or '--masques' in argv:
        appels, codes, refs = balayer(img, frag)
        if tout or '--codes' in argv:
            montrer_codes(codes)
        if tout or '--masques' in argv:
            montrer_masques(appels)
            montrer_refs(refs)
    if tout or '--detour' in argv:
        montrer_detour(img)
    return 0


if __name__ == '__main__':
    sys.exit(main())
