#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resume les 55 gestionnaires de la liste 2 de mothead (build APM3).

Le repartiteur MothRunList2 (0x180152CE0) les appelle ainsi :
    gestionnaire(rcx = &ctx, rdx = charge utile, r8 = entree de 12 octets)
    ctx = [ROB, ROB+0x440, [ROB+0x20]+0x30C0, ROB, ROB+0x440, ROB+0x8A0]
soit, en offsets d'etat (etat = ROB+0x8A0) :
    [rcx+0x00] et [rcx+0x18] = ROB          [rcx+0x08] et [rcx+0x20] = ROB+0x440
    [rcx+0x10] = un autre objet             [rcx+0x28] = l'etat de mouvement

Le script suit les sauts de queue, note les lectures de la charge utile, les
ecritures dans les champs derives de ctx, et les appels.

Usage :
    py -3 tools/lire_gestionnaires_liste2.py            tableau resume
    py -3 tools/lire_gestionnaires_liste2.py --code 20  desassemblage d'un seul
"""
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_disasm import Image, func_bounds                      # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG   # noqa: E402
import capstone                                               # noqa: E402

DLL = 'runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll'
ETAT = 0x8A0
# Le contexte a SIX entrees, et ce n'est pas un hasard : les trois dernieres
# rejouent la convention de la liste 1 (ROB, ROB+0x440, etat). Un gestionnaire de
# liste 2 qui fait « add rcx, 0x18 » delegue donc a un gestionnaire de liste 1.
CTX = {0x00: ('ROB', 0), 0x08: ('ROB', 0x440), 0x10: ('OBJ', 0),
       0x18: ('ROB', 0), 0x20: ('ROB', 0x440), 0x28: ('ROB', ETAT)}


def nom_champ(base, off):
    if base != 'ROB':
        return 'obj+0x%X' % off
    if off >= ETAT:
        return 'etat+0x%03X' % (off - ETAT)
    return 'ROB+0x%X' % off


def lire(img, va, vus=None, prof=0):
    """Suit une fonction et ses sauts de queue ; rend la liste d'instructions."""
    vus = vus if vus is not None else set()
    if va in vus or prof > 3:
        return []
    vus.add(va)
    fb = func_bounds(img, va)
    n = (fb[1] - fb[0]) if fb and fb[0] == va else 0x180
    off = img.va2off(va)
    if off is None:
        return []
    blob = img.data[off:off + n]
    out = []
    for ins in img.md.disasm(blob, va):
        out.append(ins)
        if ins.mnemonic == 'ret':
            break
        if ins.mnemonic == 'jmp' and ins.operands and ins.operands[0].type == X86_OP_IMM:
            cible = ins.operands[0].imm
            if not (va <= cible < va + n):
                out += lire(img, cible, vus, prof + 1)
                break
    return out


def analyser(img, va):
    ins_l = lire(img, va)
    # provenance : registre -> (base, offset)
    prov = {'rcx': ('CTX', 0), 'rdx': ('CHARGE', 0), 'r8': ('ENTREE', 0)}
    lectures, ecritures, appels, notes = [], [], [], []
    decalage = 0                      # « add rcx, 0x18 » : on glisse dans le contexte
    for ins in ins_l:
        ops = ins.operands
        txt = '%s %s' % (ins.mnemonic, ins.op_str)
        # mov rX, [rcx+K] : on adopte la base du contexte
        if ins.mnemonic in ('mov', 'lea') and len(ops) == 2 and ops[0].type == X86_OP_REG:
            dst = ins.reg_name(ops[0].reg)
            if ops[1].type == X86_OP_MEM and ops[1].mem.base:
                b = ins.reg_name(ops[1].mem.base)
                d = ops[1].mem.disp
                if prov.get(b, (None,))[0] == 'CTX' and ins.mnemonic == 'mov'                         and (d + prov[b][1]) in CTX:
                    prov[dst] = CTX[d + prov[b][1]]
                elif prov.get(b, (None,))[0] == 'CTX' and ins.mnemonic == 'lea':
                    prov[dst] = ('CTX', prov[b][1] + d)
                elif prov.get(b, (None,))[0] == 'CHARGE':
                    lectures.append((d, ins.op_str.split(',')[0].strip(), txt))
                    prov.pop(dst, None)
                elif prov.get(b, (None,))[0] == 'ENTREE':
                    notes.append('lit l entree +%d' % d)
                    prov.pop(dst, None)
                elif prov.get(b, (None,))[0] == 'ROB' and ins.mnemonic == 'lea':
                    prov[dst] = ('ROB', prov[b][1] + d)
                else:
                    prov.pop(dst, None)
            elif ops[1].type == X86_OP_IMM:
                prov.pop(dst, None)
            elif ops[1].type == X86_OP_REG:
                s = ins.reg_name(ops[1].reg)
                if s in prov:
                    prov[dst] = prov[s]
                else:
                    prov.pop(dst, None)
        elif ins.mnemonic == 'add' and len(ops) == 2 and ops[0].type == X86_OP_REG \
                and ops[1].type == X86_OP_IMM:
            r = ins.reg_name(ops[0].reg)
            if prov.get(r, (None,))[0] == 'ROB':
                prov[r] = ('ROB', prov[r][1] + ops[1].imm)
            elif prov.get(r, (None,))[0] == 'CTX':
                prov[r] = ('CTX', prov[r][1] + ops[1].imm)
                if r == 'rcx':
                    decalage = prov[r][1]
                    notes.append('delegue : add rcx, 0x%X' % ops[1].imm)
        # ecritures et lectures dans un champ derive de ctx
        for i, op in enumerate(ops):
            if op.type == X86_OP_MEM and op.mem.base:
                b = ins.reg_name(op.mem.base)
                p = prov.get(b)
                if p and p[0] in ('ROB', 'OBJ'):
                    champ = nom_champ(p[0], p[1] + op.mem.disp)
                    ecrit = (i == 0 and ins.mnemonic in
                             ('mov', 'or', 'and', 'xor', 'add', 'sub', 'inc', 'dec',
                              'vmovss', 'vmovsd', 'vmovups', 'movss', 'bts', 'btr'))
                    ecritures.append((champ, 'ecrit' if ecrit else 'lit', txt))
                elif p and p[0] == 'CHARGE':
                    lectures.append((op.mem.disp, '', txt))
        if ins.mnemonic == 'call' and ops and ops[0].type == X86_OP_IMM:
            appels.append(ops[0].imm)
        if ins.mnemonic == 'jmp' and ops and ops[0].type == X86_OP_IMM \
                and not (va <= ops[0].imm < va + 0x180):
            appels.append(ops[0].imm)
    return ins_l, lectures, ecritures, appels, notes


def main():
    img = Image(DLL)
    ges = {}
    for r in csv.DictReader(io.open('analysis/mothead_liste2_gestionnaires.csv',
                                    encoding='utf-8')):
        if r['gestionnaire_APM3']:
            ges[int(r['code'])] = int(r['gestionnaire_APM3'], 16)

    if '--detail' in sys.argv:
        deb = int(sys.argv[sys.argv.index('--detail') + 1])
        fin = int(sys.argv[sys.argv.index('--detail') + 2]) if len(sys.argv) >             sys.argv.index('--detail') + 2 and not sys.argv[sys.argv.index('--detail') + 2]            .startswith('-') else deb
        for c in sorted(k for k in ges if deb <= k <= fin):
            ins_l, lec, ecr, ap, notes = analyser(img, ges[c])
            print('--- code %d -> 0x%X (%d instructions) ---' % (c, ges[c], len(ins_l)))
            for n in dict.fromkeys(notes):
                print('    NOTE %s' % n)
            vus = set()
            for ins in ins_l:
                t = '%s %s' % (ins.mnemonic, ins.op_str)
                garder = (ins.mnemonic in ('call', 'cmp', 'test', 'vcomiss', 'vucomiss')
                          or any(t == x[2] for x in ecr) or any(t == x[2] for x in lec)
                          or ins.mnemonic.startswith('j') and ins.mnemonic != 'jmp')
                if garder and t not in vus:
                    vus.add(t)
                    print('    0x%X  %s' % (ins.address, t))
            print()
        return 0

    if '--code' in sys.argv:
        c = int(sys.argv[sys.argv.index('--code') + 1])
        ins_l, lec, ecr, ap, notes = analyser(img, ges[c])
        print('code %d -> 0x%X, %d instruction(s)' % (c, ges[c], len(ins_l)))
        for ins in ins_l:
            print('  0x%016X  %-22s %s %s'
                  % (ins.address, ins.bytes.hex(), ins.mnemonic, ins.op_str))
        return 0

    print('%-5s %-13s %-4s %-34s %-26s %s'
          % ('code', 'gestionnaire', 'ins', 'champs touches', 'charge lue', 'appels'))
    for c in sorted(ges):
        ins_l, lec, ecr, ap, notes = analyser(img, ges[c])
        champs = []
        for ch, sens, _ in ecr:
            e = ('%s%s' % ('=' if sens == 'ecrit' else '?', ch))
            if e not in champs:
                champs.append(e)
        offs = sorted({d for d, _, _ in lec})
        print('%-5d 0x%-11X %-4d %-34s %-26s %s'
              % (c, ges[c], len(ins_l), ' '.join(champs)[:34],
                 ' '.join('+%d' % o for o in offs)[:26],
                 ' '.join('0x%X' % a for a in ap[:3])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
