# -*- coding: utf-8 -*-
r"""Index de TOUTES les references absolues du code d'un ELF Lindbergh
(x86-32) : {adresse visee: [(adresse d'instruction, mnemonique, operandes)]}.

Pourquoi : chez VF5 R, certaines donnees d'effet ne sont pas dans une table
figee mais dans `.bss`, remplie au demarrage par un constructeur statique. Pour
les lire, il faut trouver qui ECRIT a ces adresses -- une question qu'un
index repond en une ligne, la ou un desassemblage fonction par fonction
demanderait de deviner laquelle regarder.

Desassemblage LINEAIRE de `.text` (capstone, ~10 s), mis en cache a cote de
l'ELF (`<elf>.refs.pickle`), refait si l'ELF change.

    py -3 tools/index_elf.py r 0x8BE4DA0 0x8BE4DE0     qui touche cette plage
"""
import os
import pickle
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import tables_generation as tg                                  # noqa: E402


def sections_completes(chemin):
    d = open(chemin, 'rb').read()
    shoff, = struct.unpack_from('<I', d, 0x20)
    shentsize, shnum, shstrndx = struct.unpack_from('<HHH', d, 0x2E)
    stro = struct.unpack_from('<6I', d, shoff + shstrndx * shentsize)[4]
    out = {}
    for i in range(shnum):
        nm, typ, flg, addr, off, size = struct.unpack_from(
            '<6I', d, shoff + i * shentsize)
        n = d[stro + nm:d.index(b'\x00', stro + nm)].decode()
        out[n] = (addr, off, size, typ)
    return out


def index(gen):
    chemin = tg.GENERATIONS[gen]['elf']
    cache = chemin + '.refs2.pickle'
    if os.path.exists(cache) and os.path.getmtime(cache) > \
            os.path.getmtime(chemin):
        return pickle.load(open(cache, 'rb'))
    import capstone
    s = sections_completes(chemin)
    d = open(chemin, 'rb').read()
    va0, o0, sz, _ = s['.text']
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True
    md.skipdata = True
    bas = min(v[0] for n, v in s.items() if n in ('.rodata', '.data', '.bss'))
    haut = max(v[0] + v[2] for n, v in s.items()
               if n in ('.rodata', '.data', '.bss'))
    refs = {}
    for ins in md.disasm(d[o0:o0 + sz], va0):
        if ins.id == 0:
            continue
        try:
            ops = ins.operands
        except Exception:
            continue
        for op in ops:
            v = None
            # un deplacement absolu, AVEC OU SANS registre de base : les
            # boucles de recherche lisent `[edx + table]` (VF5 R, BREATH)
            if op.type == capstone.x86.X86_OP_MEM:
                v = op.mem.disp & 0xFFFFFFFF
            elif op.type == capstone.x86.X86_OP_IMM:
                v = op.imm & 0xFFFFFFFF
            if v is not None and bas <= v < haut:
                refs.setdefault(v, []).append((ins.address, ins.mnemonic,
                                               ins.op_str))
    pickle.dump(refs, open(cache, 'wb'))
    return refs


def main():
    gen = sys.argv[1]
    a, b = int(sys.argv[2], 16), int(sys.argv[3], 16)
    r = index(gen)
    for v in sorted(x for x in r if a <= x < b):
        for ad, mn, op in r[v]:
            print('%X  <- %X  %s %s' % (v, ad, mn, op))


if __name__ == '__main__':
    main()
