#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TOUS LES CHAMPS d'une structure atteinte par un POINTEUR GLOBAL.

Le releve par deplacement a une limite de principe, et elle a failli faire
conclure faux (2026-10-04) :

    `champ_x64.py 0x796` et `voisinage_x64.py --couvre 0x796` rendent CINQ
    lectures et AUCUNE ecriture. Mais un octet peut etre ecrit par une
    instruction qui ne porte pas son deplacement :

        mov [rax + rcx], dl        ; rcx = index*0xFA88 + 0x796, calcule
        add rcx, 0x700 ; mov [rcx + 0x96], dl

    Aucun balayage par deplacement ne les voit. « Un releve vide n'est pas
    une reponse » : il faut donc une mesure qui ne repose pas sur le
    deplacement.

CE QUE CELUI-CI FAIT. Il part du GLOBAL -- le pointeur, pas la structure --
recense tous les sites qui le chargent, et suit le registre charge vers
l'avant, instruction par instruction, en relevant chaque acces memoire qui
l'emploie comme base. On obtient l'inventaire des champs REELLEMENT touches,
avec le code qui les touche, sans avoir a deviner un seul deplacement.

Le suivi s'arrete a `ret`, a un saut sortant, et des que le registre suivi est
reecrit -- au-dela on suivrait un autre objet, et un releve faux coute plus
cher qu'un releve absent. Il ne traverse pas les appels : un champ pose par
une fonction qui recoit `&champ` en argument n'y figurera pas, et c'est dit
plutot que tu.

Usage :
    py -3 tools/champs_globale.py 0x180C3B6F0
    py -3 tools/champs_globale.py 0x180C3B6F0 --ecritures
    py -3 tools/champs_globale.py 0x180C3B6F0 --autour 0x796 0x40
"""
import os
import struct
import sys

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                        # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')

SUIVI_MAX = 48          # instructions suivies apres le chargement


def sites(img, cible):
    """Les adresses qui chargent `cible` en RIP-relatif, et le registre vise.

    On cherche la FENETRE de quatre octets qui porte le deplacement, puis on
    recule pour retrouver l'instruction entiere : c'est exact, et ca attrape
    les formes `48 8b 05` (qword) que le decodage a un octet pres laisse
    passer -- le defaut de `refs_lineaires.py`, vu le 2026-10-04 : il rendait
    495 « mov ecx, dword » pour des `mov rcx, qword`.
    """
    out = []
    for s in img.secs:
        if not s.get('exec'):
            continue
        va0, n, off = s['va'], s['vsize'], s['off']
        b = img.data[off:off + n]
        for i in range(0, n - 4):
            if va0 + i + 4 + struct.unpack_from('<i', b, i)[0] != cible:
                continue
            for recul in range(3, 11):
                a = va0 + i - recul
                o = img.va2off(a)
                if o is None:
                    continue
                g = list(img.md.disasm(img.data[o:o + 16], a))
                if g and g[0].size == recul + 4 and g[0].operands:
                    d = g[0].operands[0]
                    if d.type == capstone.x86.X86_OP_REG:
                        out.append((a, d.reg, g[0]))
                    break
    return out


def champs(img, cible):
    """{(dep, ecrit): [(adresse, texte), ...]} pour chaque champ touche."""
    trouves = {}
    for va, reg, ins in sites(img, cible):
        o = img.va2off(va)
        if o is None:
            continue
        suivi = reg
        for k, x in enumerate(img.md.disasm(img.data[o:o + 16 * SUIVI_MAX],
                                            va)):
            if k == 0:
                continue
            if k > SUIVI_MAX or x.mnemonic in ('ret', 'jmp'):
                break
            touche = False
            for op in x.operands:
                if op.type != capstone.x86.X86_OP_MEM:
                    continue
                if op.mem.base != suivi and op.mem.index != suivi:
                    continue
                touche = True
                prem = x.operands[0]
                ecrit = (prem.type == capstone.x86.X86_OP_MEM
                         and prem.mem.disp == op.mem.disp
                         and x.mnemonic not in ('cmp', 'test', 'lea'))
                cle = (op.mem.disp, ecrit)
                trouves.setdefault(cle, []).append(
                    (x.address, '%s %s' % (x.mnemonic, x.op_str)))
            # LE REGISTRE SUIVI EST-IL REECRIT ? Au-dela on suivrait un
            # autre objet. On le demande a capstone (`regs_access`) au lieu
            # de regarder le premier operande : `test rdx, rdx` -- la garde
            # que TOUTE fonction de ce genre pose avant de deriver le
            # pointeur -- a son premier operande en registre sans rien y
            # ecrire. Le premier jet s'arretait dessus et perdait le site
            # 0x18013AC9C, celui-la meme qu'on cherchait (2026-10-04).
            if not touche:
                _, ecrits = x.regs_access()
                if suivi in ecrits:
                    break
    return trouves


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    cible = int(a[0], 0)
    ecritures = '--ecritures' in a
    autour = None
    if '--autour' in a:
        k = a.index('--autour')
        autour = (int(a[k + 1], 0), int(a[k + 2], 0))
    chemin = MOTEUR + ('' if '--patche' in a else '.origine')
    img = P.Image(chemin)
    print('image : %s' % os.path.basename(chemin))
    print('global : 0x%X' % cible)
    liste = sites(img, cible)
    print('%d site(s) chargent ce pointeur' % len(liste))
    tr = champs(img, cible)
    deps = sorted({d for d, _ in tr})
    if autour:
        lo, hi = autour[0] - autour[1], autour[0] + autour[1]
        deps = [d for d in deps if lo <= d <= hi]
    print('%d champ(s) distinct(s) touche(s)' % len(deps))
    print('=' * 78)
    for d in deps:
        lec = tr.get((d, False), [])
        ecr = tr.get((d, True), [])
        if ecritures and not ecr:
            continue
        print('+0x%-7X %2d lecture(s)  %2d ECRITURE(S)' % (d, len(lec),
                                                           len(ecr)))
        for va, t in sorted(set(ecr)):
            print('      ECRIT  0x%09X  %s' % (va, t))
        if not ecritures:
            for va, t in sorted(set(lec)):
                print('      lit    0x%09X  %s' % (va, t))
    return 0


if __name__ == '__main__':
    sys.exit(main())
