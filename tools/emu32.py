# -*- coding: utf-8 -*-
r"""Un emulateur MINIMAL de x86-32, pour rejouer un constructeur statique.

Pourquoi : chez VF5 R et ver.B, l'enregistrement de `TaskEffectFogAnim` n'est
pas une table figee : un constructeur l'assemble sur la pile (immediats,
copies de registres) puis le recopie dans `.bss` -- par des `mov` chez R, par
un `rep movsd` chez ver.B. Pour LIRE la donnee, on rejoue ce code.

Ce n'est pas un emulateur general : il connait les instructions qu'on a
rencontrees (mov/movzx/lea/xor/add/sub/cld/rep movsd/push/pop/leave, et
`movss` sur 32 bits -- l'anneau de brume de VF5 R charge un flottant par
xmm0) et REFUSE toute autre (on ne devine pas l'effet d'une instruction
inconnue).
Les `call` sont sautes : on ne les rejoue qu'entre deux, dans des plages ou
aucun appel ne touche la donnee -- c'est a l'appelant de choisir la plage.

    ecritures = rejouer(elf, debut, fin)     {adresse: octet}
"""
import struct

import capstone
from capstone import x86


class Refus(Exception):
    pass


def rejouer(elf, debut, fin, pile=0x7FFF0000):
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True
    reg = dict(eax=0, ebx=0, ecx=0, edx=0, esi=0, edi=0, ebp=pile, esp=pile)
    xmm = {}                            # les 32 bits bas, seuls lus par movss
    mem = {}

    def lire(a, n):
        out = bytearray()
        for k in range(n):
            if a + k in mem:
                out.append(mem[a + k])
            else:
                o = elf.off(a + k)
                out.append(elf.d[o] if o is not None else 0)
        return bytes(out)

    def ecrire(a, octets):
        for k, b in enumerate(octets):
            mem[a + k] = b

    def adresse(op):
        m = op.mem
        a = m.disp
        if m.base:
            a += reg[md.reg_name(m.base)]
        if m.index:
            a += reg[md.reg_name(m.index)] * m.scale
        return a & 0xFFFFFFFF

    def valeur(op, taille=4):
        if op.type == x86.X86_OP_IMM:
            return op.imm & ((1 << (8 * taille)) - 1)
        if op.type == x86.X86_OP_REG:
            n = md.reg_name(op.reg)
            if n in reg:
                return reg[n]
            if n in ('al', 'bl', 'cl', 'dl'):
                return reg['e' + n[0] + 'x'] & 0xFF
            raise Refus('registre %s' % n)
        if op.type == x86.X86_OP_MEM:
            return int.from_bytes(lire(adresse(op), op.size), 'little')
        raise Refus('operande')

    def poser(op, v):
        if op.type == x86.X86_OP_REG:
            n = md.reg_name(op.reg)
            if n in reg:
                reg[n] = v & 0xFFFFFFFF
                return
            if n in ('al', 'bl', 'cl', 'dl'):
                r = 'e' + n[0] + 'x'
                reg[r] = (reg[r] & ~0xFF) | (v & 0xFF)
                return
            raise Refus('registre %s' % n)
        if op.type == x86.X86_OP_MEM:
            ecrire(adresse(op), (v & ((1 << (8 * op.size)) - 1)).to_bytes(
                op.size, 'little'))
            return
        raise Refus('destination')

    a = debut
    while a != fin:
        o = elf.off(a)
        ins = next(md.disasm(elf.d[o:o + 16], a))
        mn, ops = ins.mnemonic, ins.operands
        if mn in ('mov', 'movzx'):
            poser(ops[0], valeur(ops[1]))
        elif mn == 'movss':
            n0 = md.reg_name(ops[0].reg) if ops[0].type == x86.X86_OP_REG \
                else None
            n1 = md.reg_name(ops[1].reg) if ops[1].type == x86.X86_OP_REG \
                else None
            if n0 and n0.startswith('xmm') and ops[1].type == x86.X86_OP_MEM:
                xmm[n0] = int.from_bytes(lire(adresse(ops[1]), 4), 'little')
            elif n1 and n1.startswith('xmm') and \
                    ops[0].type == x86.X86_OP_MEM:
                if n1 not in xmm:
                    raise Refus('%X : %s jamais charge' % (a, n1))
                ecrire(adresse(ops[0]), struct.pack('<I', xmm[n1]))
            else:
                raise Refus('%X : movss %s' % (a, ins.op_str))
        elif mn == 'lea':
            poser(ops[0], adresse(ops[1]))
        elif mn == 'xor' and ops[0].type == x86.X86_OP_REG and \
                ops[1].type == x86.X86_OP_REG and ops[0].reg == ops[1].reg:
            poser(ops[0], 0)
        elif mn in ('add', 'sub'):
            v = valeur(ops[0]) + (valeur(ops[1]) if mn == 'add'
                                  else -valeur(ops[1]))
            poser(ops[0], v)
        elif mn == 'cld':
            pass
        elif mn == 'rep movsd':
            n = reg['ecx']
            ecrire(reg['edi'], lire(reg['esi'], 4 * n))
            reg['edi'] += 4 * n
            reg['esi'] += 4 * n
            reg['ecx'] = 0
        elif mn == 'call':
            pass
        elif mn == 'push':
            reg['esp'] -= 4
            ecrire(reg['esp'], struct.pack('<I', valeur(ops[0])))
        elif mn == 'pop':
            poser(ops[0], struct.unpack('<I', lire(reg['esp'], 4))[0])
            reg['esp'] += 4
        elif mn in ('nop',):
            pass
        else:
            raise Refus('%X : %s %s' % (a, mn, ins.op_str))
        a += ins.size
    return mem


def lire_ecrit(mem, a, n):
    """Les `n` octets ECRITS a partir de `a`, ou None s'il en manque un."""
    if not all(a + k in mem for k in range(n)):
        return None
    return bytes(mem[a + k] for k in range(n))
