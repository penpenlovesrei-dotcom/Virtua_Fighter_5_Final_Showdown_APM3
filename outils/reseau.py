#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cartographie du TRANSPORT RESEAU du moteur APM3.

Ne dependant que de `pe_disasm`, cet outil repond a trois questions que
`.pdata` seul ne sait pas trancher :

  * `iat`      liste les creneaux d'importation (ws2_32 et voisins) avec leur
               VA de creneau -- c'est cette VA que le code appelle en
               `call qword ptr [rip+disp32]`.
  * `appels`   BALAYAGE LINEAIRE de `.text`, octet par octet, a la recherche
               de tout `FF 15 disp32` (call indirect RIP-relatif) et de tout
               `FF 25 disp32` (jmp thunk) qui vise un creneau d'IAT donne.
               `.pdata` ne liste pas les fonctions FEUILLES : un balayage par
               entrees `.pdata` rate donc des appelants. Ici on balaye la
               section entiere.
  * `const`    cherche un entier 32 bits (ex. le magic cookie STUN
               0x2112A442) partout : en donnee brute, dans les deux
               boutismes, et en immediat d'instruction.

Toujours sur `.origine`.

    py -3 tools/reseau.py iat
    py -3 tools/reseau.py iat --grep ws2_32
    py -3 tools/reseau.py appels ws2_32
    py -3 tools/reseau.py appels socket,connect,sendto
    py -3 tools/reseau.py const 0x2112A442
"""
import os
import re
import struct
import sys

import capstone
import pefile

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                        # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')


def imports(img):
    """VA du creneau d'IAT -> (dll, nom). Charge les repertoires a la demande."""
    img.pe.parse_data_directories(directories=[
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT']])
    out = {}
    for attr in ('DIRECTORY_ENTRY_IMPORT', 'DIRECTORY_ENTRY_DELAY_IMPORT'):
        for ent in getattr(img.pe, attr, []) or []:
            dll = ent.dll.decode('latin-1') if ent.dll else '?'
            for imp in ent.imports:
                nom = imp.name.decode('latin-1') if imp.name \
                    else 'ord_%d' % (imp.ordinal or 0)
                if imp.address:
                    out[imp.address] = (dll, nom)
    return out


def balayage_indirects(img):
    """Balayage LINEAIRE de chaque section executable.

    Rend une liste (va_instruction, kind, va_cible) pour :
      FF 15 disp32   call qword ptr [rip+disp32]
      FF 25 disp32   jmp  qword ptr [rip+disp32]
    La cible est `fin_instruction + disp32`, donc le CRENEAU d'IAT.
    Aucun desassemblage complet n'est requis : le motif est reconnu a
    l'octet, ce qui evite d'etre borne par `.pdata`.
    """
    hits = []
    for s in img.text_sections():
        blob = img.data[s['off']:s['off'] + min(s['rsize'], s['vsize'])]
        base = s['va']
        i = 0
        n = len(blob)
        while i < n - 5:
            if blob[i] == 0xFF and blob[i + 1] in (0x15, 0x25):
                disp = struct.unpack_from('<i', blob, i + 2)[0]
                fin = base + i + 6
                hits.append((base + i,
                             'call' if blob[i + 1] == 0x15 else 'jmp',
                             fin + disp))
            i += 1
    return hits


def balayage_directs(img, cibles):
    """Balayage LINEAIRE : E8/E9 rel32 vers une des `cibles` (set de VA)."""
    hits = []
    for s in img.text_sections():
        blob = img.data[s['off']:s['off'] + min(s['rsize'], s['vsize'])]
        base = s['va']
        n = len(blob)
        i = 0
        while i < n - 4:
            if blob[i] in (0xE8, 0xE9):
                rel = struct.unpack_from('<i', blob, i + 1)[0]
                t = base + i + 5 + rel
                if t in cibles:
                    hits.append((base + i,
                                 'call' if blob[i] == 0xE8 else 'jmp', t))
            i += 1
    return hits


def balayage_rip(img, cibles):
    """Balayage LINEAIRE de toute reference RIP-relative a une donnee.

    Methode BRUTE, et volontairement : pour chaque position `i` de `.text`,
    on lit les 4 octets comme un disp32 et on teste l'egalite EXACTE
    `fin_instruction + disp32 == cible`, ou `fin_instruction = va(i) + 4`
    (un disp32 RIP-relatif termine toujours l'instruction, sauf quand un
    immediat le suit -- cas traite plus bas).

    Ce test ne RATE rien : toute reference RIP-relative a la cible produit
    forcement un disp32 a cette valeur. En revanche il peut rendre des FAUX
    POSITIFS (une suite d'octets qui n'est pas un disp32). On tente donc de
    decoder l'instruction en arriere pour qualifier chaque touche, mais on
    la garde meme si le decodage echoue -- c'est l'inverse de la premiere
    version, qui exigeait un decodage reussi et perdait de vraies touches.

    `imm` couvre `mov dword ptr [rip+d], imm32` et consorts, ou le disp32
    est suivi de 1, 2 ou 4 octets d'immediat.
    """
    hits = []
    for s in img.text_sections():
        blob = img.data[s['off']:s['off'] + min(s['rsize'], s['vsize'])]
        base = s['va']
        n = len(blob)
        for i in range(n - 4):
            d = struct.unpack_from('<i', blob, i)[0]
            for suffixe in (0, 1, 2, 4):
                if base + i + 4 + suffixe + d not in cibles:
                    continue
                mn, ops = '?', '(non decode)'
                for back in range(1, 16):
                    st = i - back
                    if st < 0:
                        break
                    try:
                        ins = next(img.md.disasm(blob[st:st + 16],
                                                 base + st, 1))
                    except StopIteration:
                        continue
                    if ins.address + ins.size != base + i + 4 + suffixe:
                        continue
                    ok = False
                    for op in ins.operands:
                        if (op.type == capstone.x86.X86_OP_MEM
                                and op.mem.base == capstone.x86.X86_REG_RIP
                                and ins.address + ins.size
                                + op.mem.disp in cibles):
                            ok = True
                    if ok:
                        mn, ops = ins.mnemonic, ins.op_str
                        break
                hits.append((base + i - 3, mn, ops,
                             base + i + 4 + suffixe + d))
                break
    return hits


def cmd_iat(img, argv):
    motif = None
    if '--grep' in argv:
        motif = re.compile(argv[argv.index('--grep') + 1], re.I)
    imps = imports(img)
    for va in sorted(imps):
        dll, nom = imps[va]
        if motif and not (motif.search(dll) or motif.search(nom)):
            continue
        print('0x%09X  %-22s %s' % (va, dll, nom))
    print('%d importation(s)' % len(imps))


def cmd_appels(img, argv):
    filtre = argv[0] if argv else ''
    imps = imports(img)
    voulus = {}
    for va, (dll, nom) in imps.items():
        for f in filtre.split(','):
            f = f.strip()
            if f and (f.lower() in dll.lower() or f.lower() == nom.lower()):
                voulus[va] = (dll, nom)
    if not voulus:
        print('aucune importation ne correspond a %r' % filtre)
        return
    ind = balayage_indirects(img)
    par_slot = {}
    for va_ins, kind, cible in ind:
        if cible in voulus:
            par_slot.setdefault(cible, []).append((va_ins, kind))
    # deuxieme passe : thunks (jmp [iat]) appeles en E8/E9
    thunks = {}
    for cible, lst in par_slot.items():
        for va_ins, kind in lst:
            if kind == 'jmp':
                thunks[va_ins] = cible
    directs = balayage_directs(img, set(thunks)) if thunks else []

    for cible in sorted(voulus, key=lambda v: voulus[v][1]):
        dll, nom = voulus[cible]
        lst = sorted(par_slot.get(cible, []))
        print('\n=== %s!%s   creneau 0x%X   %d site(s) directs'
              % (dll, nom, cible, len(lst)))
        for va_ins, kind in lst:
            fb = P.func_bounds(img, va_ins)
            marque = ' [THUNK]' if kind == 'jmp' else ''
            print('    %-4s 0x%09X   fonction .pdata 0x%X%s'
                  % (kind, va_ins, fb[0] if fb else 0, marque))
        for va_ins, kind, t in sorted(directs):
            if thunks.get(t) != cible:
                continue
            fb = P.func_bounds(img, va_ins)
            print('    via thunk 0x%X : %s 0x%09X   fonction .pdata 0x%X'
                  % (t, kind, va_ins, fb[0] if fb else 0))


def cmd_const(img, argv):
    val = int(argv[0], 0)
    le = struct.pack('<I', val)
    be = struct.pack('>I', val)
    print('# valeur 0x%08X ; LE=%s BE=%s' % (val, le.hex(), be.hex()))
    for etq, motif in (('LE', le), ('BE', be)):
        for m in re.finditer(re.escape(motif), img.data):
            va = img.off2va(m.start())
            s = img.sec_of(va) if va else None
            print('  %s  off=0x%08X  va=%s  section=%s'
                  % (etq, m.start(), ('0x%09X' % va) if va else '-',
                     s['name'] if s else '?'))


def cmd_appelants(img, argv):
    """Balayage LINEAIRE de `.text` : tout E8/E9 rel32 visant la cible.

    `.pdata` ne liste pas les fonctions FEUILLES ; un parcours par entrees
    `.pdata` sous-compte donc les appelants. Ici on lit chaque octet.
    """
    cible = int(argv[0], 0)
    hits = balayage_directs(img, {cible})
    for va_ins, kind, _t in sorted(hits):
        fb = P.func_bounds(img, va_ins)
        print('  %-4s 0x%09X   fonction .pdata %s'
              % (kind, va_ins, ('0x%09X' % fb[0]) if fb else 'AUCUNE (feuille)'))
    print('%d appelant(s) directs de 0x%09X (balayage lineaire)'
          % (len(hits), cible))


def cmd_refs(img, argv):
    """Balayage LINEAIRE : toute reference RIP-relative a une donnee."""
    cible = int(argv[0], 0)
    hits = balayage_rip(img, {cible})
    for va, mn, ops, _c in sorted(hits):
        fb = P.func_bounds(img, va)
        print('  0x%09X  %-6s %-38s fonction .pdata %s'
              % (va, mn, ops, ('0x%09X' % fb[0]) if fb else 'AUCUNE (feuille)'))
    print('%d reference(s) a 0x%09X (balayage lineaire)' % (len(hits), cible))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    img = P.Image(MOTEUR)
    cmd = sys.argv[1]
    argv = sys.argv[2:]
    if cmd == 'iat':
        cmd_iat(img, argv)
    elif cmd == 'appels':
        cmd_appels(img, argv)
    elif cmd == 'const':
        cmd_const(img, argv)
    elif cmd == 'appelants':
        cmd_appelants(img, argv)
    elif cmd == 'refs':
        cmd_refs(img, argv)
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
