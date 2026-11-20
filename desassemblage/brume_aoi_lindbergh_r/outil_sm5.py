# -*- coding: utf-8 -*-
"""Desassembleur minimal de bytecode Direct3D 10/11 (SHEX/SHDR d'un DXBC).

Pourquoi : les nuanceurs du build Windows (APM3) sont des DXBC dans
`shader_pxd_w64.farc`, pas des programmes ARB en texte. Pour savoir si le
defaut lu dans les ARB (une sortie jamais ecrite) est AUSSI dans le build
Windows, il faut lire le bytecode.

    py -3 sm5.py <fichier .vp/.fp (conteneur GSVS ou DXBC brut)>
"""
import struct
import sys

OPS = {
    0: 'add', 1: 'and', 2: 'break', 3: 'breakc', 4: 'call', 5: 'callc',
    6: 'case', 7: 'continue', 8: 'continuec', 9: 'cut', 10: 'default',
    11: 'deriv_rtx', 12: 'deriv_rty', 13: 'discard', 14: 'div', 15: 'dp2',
    16: 'dp3', 17: 'dp4', 18: 'else', 19: 'emit', 20: 'emitthencut',
    21: 'endif', 22: 'endloop', 23: 'endswitch', 24: 'eq', 25: 'exp',
    26: 'frc', 27: 'ftoi', 28: 'ftou', 29: 'ge', 30: 'iadd', 31: 'if',
    32: 'ieq', 33: 'ige', 34: 'ilt', 35: 'imad', 36: 'imax', 37: 'imin',
    38: 'imul', 39: 'ine', 40: 'ineg', 41: 'ishl', 42: 'ishr', 43: 'itof',
    44: 'label', 45: 'ld', 46: 'ld_ms', 47: 'log', 48: 'loop', 49: 'lt',
    50: 'mad', 51: 'min', 52: 'max', 53: 'customdata', 54: 'mov',
    55: 'movc', 56: 'mul', 57: 'ne', 58: 'nop', 59: 'not', 60: 'or',
    61: 'resinfo', 62: 'ret', 63: 'retc', 64: 'round_ne', 65: 'round_ni',
    66: 'round_pi', 67: 'round_z', 68: 'rsq', 69: 'sample',
    70: 'sample_c', 71: 'sample_c_lz', 72: 'sample_l', 73: 'sample_d',
    74: 'sample_b', 75: 'sqrt', 76: 'switch', 77: 'sincos', 78: 'udiv',
    79: 'ult', 80: 'uge', 81: 'umul', 82: 'umad', 83: 'umax', 84: 'umin',
    85: 'ushr', 86: 'utof', 87: 'xor', 88: 'dcl_resource',
    89: 'dcl_constantbuffer', 90: 'dcl_sampler', 91: 'dcl_indexrange',
    92: 'dcl_gs_topology', 93: 'dcl_gs_inputprim', 94: 'dcl_maxout',
    95: 'dcl_input', 96: 'dcl_input_sgv', 97: 'dcl_input_siv',
    98: 'dcl_input_ps', 99: 'dcl_input_ps_sgv', 100: 'dcl_input_ps_siv',
    101: 'dcl_output', 102: 'dcl_output_sgv', 103: 'dcl_output_siv',
    104: 'dcl_temps', 105: 'dcl_indexable_temp', 106: 'dcl_globalflags',
}

TYPES = {0: 'r', 1: 'v', 2: 'o', 3: 'x', 4: 'imm', 5: 'imm64', 6: 's',
         7: 't', 8: 'cb', 9: 'icb', 10: 'label', 11: 'vPrim',
         12: 'oDepth', 13: 'null'}

XYZW = 'xyzw'


def operande(dw, i):
    t = dw[i]
    i += 1
    numcomp = t & 3
    selmode = (t >> 2) & 3
    sel = (t >> 4) & 0xFF
    optype = (t >> 12) & 0xFF
    numidx = (t >> 20) & 3
    reps = [(t >> (22 + 3 * k)) & 7 for k in range(numidx)]
    if (t >> 31) & 1:
        while True:
            e = dw[i]
            i += 1
            if not ((e >> 31) & 1):
                break
    idx = []
    for r in reps:
        if r == 0:
            idx.append(str(dw[i]))
            i += 1
        elif r == 1:
            idx.append('imm64')
            i += 2
        elif r == 2:
            s, i = operande(dw, i)
            idx.append('[%s]' % s)
        elif r == 3:
            a = dw[i]
            i += 1
            s, i = operande(dw, i)
            idx.append('%d[%s]' % (a, s))
        elif r == 4:
            i += 2
            s, i = operande(dw, i)
            idx.append('imm64[%s]' % s)
        else:
            idx.append('?')
    nom = TYPES.get(optype, 't%d' % optype)
    if optype == 4:
        n = 4 if numcomp == 2 else 1
        vals = [struct.unpack('<f', struct.pack('<I', dw[i + k]))[0]
                for k in range(n)]
        i += n
        return '(' + ', '.join('%g' % v for v in vals) + ')', i
    txt = nom + (''.join(idx) if len(idx) == 1 else '[' + ']['.join(idx) + ']')
    if numcomp == 2:
        if selmode == 0:                                   # masque
            txt += '.' + ''.join(XYZW[k] for k in range(4) if sel >> k & 1)
        elif selmode == 1:                                 # swizzle
            txt += '.' + ''.join(XYZW[(sel >> (2 * k)) & 3] for k in range(4))
        elif selmode == 2:                                 # une seule
            txt += '.' + XYZW[sel & 3]
    return txt, i


def desassembler(dw):
    i = 2                                                   # version, taille
    lignes = []
    while i < len(dw):
        t = dw[i]
        op = t & 0x7FF
        ln = (t >> 24) & 0x7F
        if op == 53:
            ln = dw[i + 1]
            lignes.append('customdata (%d dwords)' % ln)
            i += max(ln, 2)
            continue
        if ln == 0:
            lignes.append('?? opcode %d longueur 0' % op)
            break
        nom = OPS.get(op, 'op%d' % op)
        if (t >> 13) & 1:
            nom += '_sat'
        j = i + 1
        args = []
        if op in (104, 106, 94):                            # entiers nus
            args = [str(dw[j])]
        else:
            fin = i + ln
            while j < fin:
                try:
                    s, j = operande(dw, j)
                except IndexError:
                    break
                args.append(s)
        lignes.append('%-18s %s' % (nom, ', '.join(args)))
        i += ln
    return lignes


def main():
    for chemin in sys.argv[1:]:
        d = open(chemin, 'rb').read()
        base = d.find(b'DXBC')
        _, cc = struct.unpack_from('<II', d, base + 24)
        offs = struct.unpack_from('<%dI' % cc, d, base + 32)
        print('===== %s =====' % chemin)
        for o in offs:
            nom = d[base + o:base + o + 4].decode('latin-1')
            taille, = struct.unpack_from('<I', d, base + o + 4)
            if nom in ('SHEX', 'SHDR'):
                dw = struct.unpack_from('<%dI' % (taille // 4), d,
                                        base + o + 8)
                for k, l in enumerate(desassembler(dw)):
                    print('%4d  %s' % (k, l))
        print()


if __name__ == '__main__':
    main()
