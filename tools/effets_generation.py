# -*- coding: utf-8 -*-
r"""Les TACHES D'EFFET d'une generation Lindbergh (ver.B, VF5 R), lues dans son
code : typeinfo -> vtable -> fonctions -> tables de donnees qu'elles lisent.

Les exécutables Lindbergh (g++, ABI Itanium) gardent le NOM de chaque classe
(`14TaskEffectSnow`) : le typeinfo le pointe en +4, et la vtable pointe le
typeinfo juste AVANT sa premiere fonction. On desassemble chaque fonction
(x86-32 : les tables sont des adresses ABSOLUES dans le code) et on releve
les adresses de donnees qu'elle touche.

    py -3 tools/effets_generation.py r   [Snow Breath ...]
    py -3 tools/effets_generation.py verb
"""
import os
import re
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import tables_generation as tg                                  # noqa: E402


def classes(e):
    """{nom de classe: [adresses des fonctions de la vtable]}."""
    d = e.d
    out = {}
    for m in re.finditer(rb'(\d{1,3})(TaskEffect[A-Za-z0-9_]*)\x00', d):
        n = int(m.group(1))
        nom = m.group(2)[:n - len(b'')] if False else m.group(2)
        if len(nom) != n:
            continue
        va_nom = e.va(m.start())
        if va_nom is None:
            continue
        for ti_ref in e.refs(va_nom):
            ti = ti_ref - 4                     # typeinfo : [vptr][nom]...
            for vt_ref in e.refs(ti):
                fonctions = []
                k = 0
                while True:
                    f = e.u32(vt_ref + 4 + 4 * k) if e.off(
                        vt_ref + 4 + 4 * k) else 0
                    if not (e.sections.get('.text') and
                            e.sections['.text'][0] <= f <
                            e.sections['.text'][0] + e.sections['.text'][2]):
                        break
                    fonctions.append(f)
                    k += 1
                if len(fonctions) >= 4:
                    out[nom.decode()] = fonctions
    return out


def references(e, f, longueur=0x600):
    """Les adresses de donnees touchees par la fonction `f` (desassemblage
    lineaire jusqu'au premier `ret` suivi d'un bourrage)."""
    import capstone
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True
    o = e.off(f)
    code = e.d[o:o + longueur]
    refs = []
    appels = []
    for ins in md.disasm(code, f):
        for op in ins.operands:
            v = None
            if op.type == capstone.x86.X86_OP_IMM:
                v = op.imm & 0xFFFFFFFF
            elif op.type == capstone.x86.X86_OP_MEM and op.mem.base == 0:
                v = op.mem.disp & 0xFFFFFFFF
            if v is None:
                continue
            for n in ('.data', '.rodata'):
                s = e.sections.get(n)
                if s and s[0] <= v < s[0] + s[2]:
                    refs.append((ins.address, n, v, ins.mnemonic, ins.op_str))
            b = getattr(e, 'bss', None)
            if b and b[0] <= v < b[0] + b[1]:
                refs.append((ins.address, '.bss', v, ins.mnemonic, ins.op_str))
        if ins.mnemonic == 'call' and ins.operands and \
                ins.operands[0].type == capstone.x86.X86_OP_IMM:
            appels.append(ins.operands[0].imm & 0xFFFFFFFF)
        if ins.mnemonic == 'ret':
            break
    return refs, appels


def main():
    gen = sys.argv[1] if len(sys.argv) > 1 else 'r'
    voulu = sys.argv[2:]
    g = tg.GENERATIONS[gen]
    e = tg.Elf(g['elf'])
    # .bss : NOBITS, absente de Elf.sections -- on l'ajoute pour la reconnaitre
    d = e.d
    shoff, = struct.unpack_from('<I', d, 0x20)
    shentsize, shnum, shstrndx = struct.unpack_from('<HHH', d, 0x2E)
    stro = struct.unpack_from('<6I', d, shoff + shstrndx * shentsize)[4]
    for i in range(shnum):
        nm, typ, flg, addr, off, size = struct.unpack_from(
            '<6I', d, shoff + i * shentsize)
        n = d[stro + nm:d.index(b'\x00', stro + nm)].decode()
        if n == '.bss':
            e.bss = (addr, size)
    cl = classes(e)
    for nom in sorted(cl):
        if voulu and not any(v.lower() in nom.lower() for v in voulu):
            continue
        print('== %s  %s' % (nom, ' '.join('%d:%X' % (i, f)
                                          for i, f in enumerate(cl[nom]))))
        for i, f in enumerate(cl[nom]):
            refs, appels = references(e, f)
            vus = sorted(set((n, v) for _, n, v, _, _ in refs if n != '.bss'))
            if vus:
                print('   %2d %X : %s' % (i, f, ' '.join(
                    '%s:%X' % (n[1:3], v) for n, v in vus)))


if __name__ == '__main__':
    main()
