#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Lecteur de metadonnees .NET et desassembleur CIL, sans dependance.

POURQUOI CET OUTIL

L'interface APM3 n'est pas du x86 : `Apmv3System.exe` et `emoneyUI.exe` sont
des applications **Unity**, et toute leur logique est dans du **C# compile en
CIL** -- `Assembly-CSharp.dll`. `capstone` n'y voit rien. Il faut lire les
metadonnees ECMA-335 : les tables de types, de methodes, de champs, les tas de
chaines, et les corps de methodes.

CE QU'IL SAIT FAIRE

    py -3 tools/dotnet.py <assembly.dll> --types
    py -3 tools/dotnet.py <assembly.dll> --type <NomDeClasse>
    py -3 tools/dotnet.py <assembly.dll> --methode <Classe.Methode>
    py -3 tools/dotnet.py <assembly.dll> --chaines [--grep MOTIF]
    py -3 tools/dotnet.py <assembly.dll> --cherche MOTIF

LA STRUCTURE, pour qui reprendra

    PE -> repertoire de donnees 14 (CLI header, 72 octets)
       -> +8  : RVA/taille des METADONNEES
    Metadonnees : signature 'BSJB', version, puis N flux nommes --
       `#~` les tables, `#Strings` les noms, `#US` les chaines litterales,
       `#Blob` les signatures, `#GUID`.
    `#~` : en-tete de 24 octets (dont `heap_sizes` en +6, qui dit si les index
    de tas font 2 ou 4 octets), un masque `valid` de 64 bits disant quelles
    tables existent, un masque `sorted`, puis le nombre de lignes de chaque
    table presente, puis les lignes elles-memes, a la file.

    La taille d'une ligne depend du nombre de lignes des tables qu'elle
    reference : c'est pour cela qu'il faut compter TOUTES les tables avant de
    pouvoir en lire UNE. C'est le piege du format.
"""
import os
import struct
import sys

import pefile

# --- les tables qu'on decode vraiment. Les autres sont juste MESUREES, ce qui
# --- suffit a franchir leurs lignes pour atteindre les suivantes.
NOMS_TABLES = {
    0x00: 'Module', 0x01: 'TypeRef', 0x02: 'TypeDef', 0x04: 'Field',
    0x06: 'MethodDef', 0x08: 'Param', 0x09: 'InterfaceImpl',
    0x0A: 'MemberRef', 0x0B: 'Constant', 0x0C: 'CustomAttribute',
    0x0D: 'FieldMarshal', 0x0E: 'DeclSecurity', 0x0F: 'ClassLayout',
    0x10: 'FieldLayout', 0x11: 'StandAloneSig', 0x12: 'EventMap',
    0x14: 'Event', 0x15: 'PropertyMap', 0x17: 'Property',
    0x18: 'MethodSemantics', 0x19: 'MethodImpl', 0x1A: 'ModuleRef',
    0x1B: 'TypeSpec', 0x1C: 'ImplMap', 0x1D: 'FieldRVA',
    0x20: 'Assembly', 0x21: 'AssemblyProcessor', 0x22: 'AssemblyOS',
    0x23: 'AssemblyRef', 0x24: 'AssemblyRefProcessor',
    0x25: 'AssemblyRefOS', 0x26: 'File', 0x27: 'ExportedType',
    0x28: 'ManifestResource', 0x29: 'NestedClass',
    0x2A: 'GenericParam', 0x2B: 'MethodSpec', 0x2C: 'GenericParamConstraint',
}

# Les index composites : (nom, [tables visees], bits d'etiquette)
CODES = {
    'TypeDefOrRef': ([0x02, 0x01, 0x1B], 2),
    'HasConstant': ([0x04, 0x08, 0x17], 2),
    'HasCustomAttribute': ([0x06, 0x04, 0x01, 0x02, 0x08, 0x09, 0x0A, 0x14,
                            0x17, 0x11, 0x1A, 0x1B, 0x00, 0x0E, 0x20, 0x23,
                            0x26, 0x27, 0x28, 0x2A, 0x2B, 0x24], 5),
    'HasFieldMarshal': ([0x04, 0x08], 1),
    'HasDeclSecurity': ([0x02, 0x06, 0x20], 2),
    'MemberRefParent': ([0x02, 0x01, 0x1A, 0x06, 0x1B], 3),
    'HasSemantics': ([0x14, 0x17], 1),
    'MethodDefOrRef': ([0x06, 0x0A], 1),
    'MemberForwarded': ([0x04, 0x06], 1),
    'Implementation': ([0x26, 0x23, 0x27], 2),
    'CustomAttributeType': ([0xFF, 0xFF, 0x06, 0x0A, 0xFF], 3),
    'ResolutionScope': ([0x00, 0x1A, 0x23, 0x01], 2),
    'TypeOrMethodDef': ([0x02, 0x06], 1),
}

# Le schema de chaque table : suite de champs.
#   'u2' 'u4'  entiers ; 'S' index #Strings ; 'B' #Blob ; 'G' #GUID
#   ('t', 0x02) index simple vers une table ; ('c', 'TypeDefOrRef') composite
SCHEMAS = {
    0x00: ['u2', 'S', 'G', 'G', 'G'],
    0x01: [('c', 'ResolutionScope'), 'S', 'S'],
    0x02: ['u4', 'S', 'S', ('c', 'TypeDefOrRef'), ('t', 0x04), ('t', 0x06)],
    0x04: ['u2', 'S', 'B'],
    0x06: ['u4', 'u2', 'u2', 'S', 'B', ('t', 0x08)],
    0x08: ['u2', 'u2', 'S'],
    0x09: [('t', 0x02), ('c', 'TypeDefOrRef')],
    0x0A: [('c', 'MemberRefParent'), 'S', 'B'],
    0x0B: ['u2', ('c', 'HasConstant'), 'B'],
    0x0C: [('c', 'HasCustomAttribute'), ('c', 'CustomAttributeType'), 'B'],
    0x0D: [('c', 'HasFieldMarshal'), 'B'],
    0x0E: ['u2', ('c', 'HasDeclSecurity'), 'B'],
    0x0F: ['u2', 'u4', ('t', 0x02)],
    0x10: ['u4', ('t', 0x04)],
    0x11: ['B'],
    0x12: [('t', 0x02), ('t', 0x14)],
    0x14: ['u2', 'S', ('c', 'TypeDefOrRef')],
    0x15: [('t', 0x02), ('t', 0x17)],
    0x17: ['u2', 'S', 'B'],
    0x18: ['u2', ('t', 0x06), ('c', 'HasSemantics')],
    0x19: [('t', 0x02), ('c', 'MethodDefOrRef'), ('c', 'MethodDefOrRef')],
    0x1A: ['S'],
    0x1B: ['B'],
    0x1C: ['u2', ('c', 'MemberForwarded'), 'S', ('t', 0x1A)],
    0x1D: ['u4', ('t', 0x04)],
    0x20: ['u4', 'u2', 'u2', 'u2', 'u2', 'u4', 'B', 'S', 'S'],
    0x21: ['u4'],
    0x22: ['u4', 'u4', 'u4'],
    0x23: ['u2', 'u2', 'u2', 'u2', 'u4', 'B', 'S', 'S', 'B'],
    0x24: ['u4', ('t', 0x23)],
    0x25: ['u4', 'u4', 'u4', ('t', 0x23)],
    0x26: ['u4', 'S', 'B'],
    0x27: ['u4', 'u4', 'S', 'S', ('c', 'Implementation')],
    0x28: ['u4', 'u4', 'S', ('c', 'Implementation')],
    0x29: [('t', 0x02), ('t', 0x02)],
    0x2A: ['u2', 'u2', ('c', 'TypeOrMethodDef'), 'S'],
    0x2B: [('c', 'MethodDefOrRef'), 'B'],
    0x2C: [('t', 0x2A), ('c', 'TypeDefOrRef')],
}


class Assembly(object):
    def __init__(self, chemin):
        self.pe = pefile.PE(chemin, fast_load=True)
        self.pe.parse_data_directories()
        self.brut = bytes(self.pe.__data__)
        self.chemin = chemin
        self._metadonnees()
        self._tables()

    # --- acces bas niveau ------------------------------------------------
    def off(self, rva):
        return self.pe.get_offset_from_rva(rva)

    def _metadonnees(self):
        d = self.pe.OPTIONAL_HEADER.DATA_DIRECTORY[14]
        if not d.VirtualAddress:
            raise SystemExit('%s : pas d\'en-tete CLI (ce n\'est pas du .NET)'
                             % os.path.basename(self.chemin))
        cli = self.off(d.VirtualAddress)
        md_rva, md_taille = struct.unpack_from('<II', self.brut, cli + 8)
        m = self.off(md_rva)
        if self.brut[m:m + 4] != b'BSJB':
            raise SystemExit('signature de metadonnees absente')
        n = struct.unpack_from('<I', self.brut, m + 12)[0]
        o = m + 16 + ((n + 3) & ~3) + 4          # version + flags
        nflux = struct.unpack_from('<H', self.brut, o - 2)[0]
        self.flux = {}
        for _ in range(nflux):
            dec, taille = struct.unpack_from('<II', self.brut, o)
            o += 8
            fin = self.brut.index(b'\x00', o)
            nom = self.brut[o:fin].decode('ascii')
            o = fin + 1
            o = (o + 3) & ~3
            self.flux[nom] = (m + dec, taille)
        self.md = m

    def chaine(self, i):
        d, _ = self.flux['#Strings']
        f = self.brut.index(b'\x00', d + i)
        return self.brut[d + i:f].decode('utf-8', 'replace')

    def litterale(self, i):
        """Une chaine du tas #US, designee par un jeton 0x70xxxxxx."""
        d, _ = self.flux['#US']
        o = d + i
        n, o = self._compresse(o)
        if n == 0:
            return ''
        return self.brut[o:o + n - 1].decode('utf-16-le', 'replace')

    def _compresse(self, o):
        b = self.brut[o]
        if b & 0x80 == 0:
            return b, o + 1
        if b & 0xC0 == 0x80:
            return ((b & 0x3F) << 8) | self.brut[o + 1], o + 2
        return (((b & 0x1F) << 24) | (self.brut[o + 1] << 16)
                | (self.brut[o + 2] << 8) | self.brut[o + 3]), o + 4

    # --- les tables ------------------------------------------------------
    def _tables(self):
        d, _ = self.flux['#~']
        self.heaps = self.brut[d + 6]
        valid = struct.unpack_from('<Q', self.brut, d + 8)[0]
        o = d + 24
        self.lignes = {}
        for t in range(64):
            if valid >> t & 1:
                self.lignes[t] = struct.unpack_from('<I', self.brut, o)[0]
                o += 4
        self.taille_index = {}
        for t in self.lignes:
            self.taille_index[t] = 4 if self.lignes[t] >= 0x10000 else 2
        # taille d'un champ, une fois toutes les tables comptees
        self.debut = {}
        for t in sorted(self.lignes):
            self.debut[t] = o
            o += self.lignes[t] * self._taille_ligne(t)
        self.fin_tables = o

    def _taille_champ(self, c):
        if c == 'u2':
            return 2
        if c == 'u4':
            return 4
        if c == 'S':
            return 4 if self.heaps & 1 else 2
        if c == 'G':
            return 4 if self.heaps & 2 else 2
        if c == 'B':
            return 4 if self.heaps & 4 else 2
        if c[0] == 't':
            return self.taille_index.get(c[1], 2)
        tables, bits = CODES[c[1]]
        maxi = max((self.lignes.get(x, 0) for x in tables if x != 0xFF),
                   default=0)
        return 4 if maxi >= (1 << (16 - bits)) else 2

    def _taille_ligne(self, t):
        return sum(self._taille_champ(c) for c in SCHEMAS.get(t, ['u4']))

    def ligne(self, t, i):
        """La ligne `i` (1-based) de la table `t`, comme liste de valeurs."""
        o = self.debut[t] + (i - 1) * self._taille_ligne(t)
        out = []
        for c in SCHEMAS[t]:
            n = self._taille_champ(c)
            v = int.from_bytes(self.brut[o:o + n], 'little')
            out.append(v)
            o += n
        return out

    # --- ce qui nous interesse -------------------------------------------
    def types(self):
        """[(indice, espace de noms, nom, 1re methode, 1er champ), ...]"""
        out = []
        n = self.lignes.get(0x02, 0)
        for i in range(1, n + 1):
            # ATTENTION : dans TypeDef, le NOM precede l'ESPACE DE NOMS.
            # Les intervertir donnait « Main / Apm.System.AbaasGs » au lieu de
            # « Apm.System.AbaasGs / Main ».
            f, nom, ns, ext, ch, me = self.ligne(0x02, i)[:6]
            out.append((i, self.chaine(ns), self.chaine(nom), me, ch))
        return out

    def methodes_de(self, i):
        """Les methodes du type `i` : [(indice, nom, rva), ...]"""
        types = self.types()
        deb = types[i - 1][3]
        fin = types[i][3] if i < len(types) else self.lignes.get(0x06, 0) + 1
        out = []
        for m in range(deb, fin):
            rva, impl, flags, nom, sig, par = self.ligne(0x06, m)
            out.append((m, self.chaine(nom), rva))
        return out

    def champs_de(self, i):
        types = self.types()
        deb = types[i - 1][4]
        fin = types[i][4] if i < len(types) else self.lignes.get(0x04, 0) + 1
        return [(f, self.chaine(self.ligne(0x04, f)[1]))
                for f in range(deb, fin)]

    def corps(self, rva):
        """Le CIL brut d'une methode, ou None."""
        if not rva:
            return None
        o = self.off(rva)
        b = self.brut[o]
        if b & 3 == 2:                              # en-tete court
            return self.brut[o + 1:o + 1 + (b >> 2)]
        taille = struct.unpack_from('<I', self.brut, o + 4)[0]
        entete = (struct.unpack_from('<H', self.brut, o)[0] >> 12) * 4
        return self.brut[o + entete:o + entete + taille]


# --- desassemblage CIL, le sous-ensemble utile --------------------------
OPS = {
    0x00: ('nop', 0), 0x01: ('break', 0), 0x02: ('ldarg.0', 0),
    0x03: ('ldarg.1', 0), 0x04: ('ldarg.2', 0), 0x05: ('ldarg.3', 0),
    0x06: ('ldloc.0', 0), 0x07: ('ldloc.1', 0), 0x08: ('ldloc.2', 0),
    0x09: ('ldloc.3', 0), 0x0A: ('stloc.0', 0), 0x0B: ('stloc.1', 0),
    0x0C: ('stloc.2', 0), 0x0D: ('stloc.3', 0), 0x0E: ('ldarg.s', 1),
    0x0F: ('ldarga.s', 1), 0x10: ('starg.s', 1), 0x11: ('ldloc.s', 1),
    0x12: ('ldloca.s', 1), 0x13: ('stloc.s', 1), 0x14: ('ldnull', 0),
    0x15: ('ldc.i4.m1', 0), 0x16: ('ldc.i4.0', 0), 0x17: ('ldc.i4.1', 0),
    0x18: ('ldc.i4.2', 0), 0x19: ('ldc.i4.3', 0), 0x1A: ('ldc.i4.4', 0),
    0x1B: ('ldc.i4.5', 0), 0x1C: ('ldc.i4.6', 0), 0x1D: ('ldc.i4.7', 0),
    0x1E: ('ldc.i4.8', 0), 0x1F: ('ldc.i4.s', 1), 0x20: ('ldc.i4', 4),
    0x21: ('ldc.i8', 8), 0x22: ('ldc.r4', 4), 0x23: ('ldc.r8', 8),
    0x25: ('dup', 0), 0x26: ('pop', 0), 0x28: ('call', 'T'),
    0x29: ('calli', 'T'), 0x2A: ('ret', 0), 0x2B: ('br.s', 1),
    0x2C: ('brfalse.s', 1), 0x2D: ('brtrue.s', 1), 0x2E: ('beq.s', 1),
    0x2F: ('bge.s', 1), 0x30: ('bgt.s', 1), 0x31: ('ble.s', 1),
    0x32: ('blt.s', 1), 0x38: ('br', 4), 0x39: ('brfalse', 4),
    0x3A: ('brtrue', 4), 0x3B: ('beq', 4), 0x3C: ('bge', 4),
    0x3D: ('bgt', 4), 0x3E: ('ble', 4), 0x3F: ('blt', 4),
    0x58: ('add', 0), 0x59: ('sub', 0), 0x5A: ('mul', 0), 0x5B: ('div', 0),
    0x6F: ('callvirt', 'T'), 0x72: ('ldstr', 'S'), 0x73: ('newobj', 'T'),
    0x74: ('castclass', 'T'), 0x75: ('isinst', 'T'), 0x7B: ('ldfld', 'T'),
    0x7C: ('ldflda', 'T'), 0x7D: ('stfld', 'T'), 0x7E: ('ldsfld', 'T'),
    0x80: ('stsfld', 'T'), 0x8C: ('box', 'T'), 0x8D: ('newarr', 'T'),
    0x8E: ('ldlen', 0), 0xA2: ('stelem.ref', 0), 0x9A: ('ldelem.ref', 0),
    0x14: ('ldnull', 0), 0x26: ('pop', 0), 0x39: ('brfalse', 4),
}


def desassembler(asm, cil):
    out = []
    i = 0
    while i < len(cil):
        deb = i
        b = cil[i]
        i += 1
        if b == 0xFE:                     # prefixe deux octets
            b2 = cil[i]
            i += 1
            out.append('IL_%04X:  fe %02x' % (deb, b2))
            if b2 in (0x01, 0x02, 0x03, 0x04, 0x05, 0x06):
                i += 4
            continue
        nom, arg = OPS.get(b, ('.%02x' % b, 0))
        texte = ''
        if arg == 'S':
            jeton = struct.unpack_from('<I', cil, i)[0]
            i += 4
            texte = '  "%s"' % asm.litterale(jeton & 0xFFFFFF)
        elif arg == 'T':
            jeton = struct.unpack_from('<I', cil, i)[0]
            i += 4
            texte = '  %s' % nom_du_jeton(asm, jeton)
        elif isinstance(arg, int) and arg:
            v = int.from_bytes(cil[i:i + arg], 'little',
                               signed=(nom.endswith('.s') or arg == 1))
            i += arg
            texte = '  %d' % v
        out.append('IL_%04X:  %-12s%s' % (deb, nom, texte))
    return out


def nom_du_jeton(asm, jeton):
    t, i = jeton >> 24, jeton & 0xFFFFFF
    if not i:
        return '0x%08X' % jeton
    try:
        if t == 0x0A:                                  # MemberRef
            parent, nom, _ = asm.ligne(0x0A, i)
            return '%s' % asm.chaine(nom)
        if t == 0x06:                                  # MethodDef
            return asm.chaine(asm.ligne(0x06, i)[3])
        if t == 0x04:                                  # Field
            return asm.chaine(asm.ligne(0x04, i)[1])
        if t == 0x01:                                  # TypeRef
            _, nom, ns = asm.ligne(0x01, i)
            return '%s%s' % (asm.chaine(ns) + '.' if asm.chaine(ns) else '',
                             asm.chaine(nom))
        if t == 0x02:                                  # TypeDef
            l = asm.ligne(0x02, i)
            return '%s%s' % (asm.chaine(l[2]) + '.' if asm.chaine(l[2]) else '',
                             asm.chaine(l[1]))
    except Exception:
        pass
    return '0x%08X' % jeton


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    asm = Assembly(argv[0])

    if '--types' in argv:
        ts = asm.types()
        print('%d type(s) dans %s' % (len(ts), os.path.basename(argv[0])))
        for i, ns, nom, _, _ in ts:
            n = len(asm.methodes_de(i))
            print('   %4d  %-42s %-30s %3d methode(s)'
                  % (i, ns or '(global)', nom, n))
        return 0

    if '--type' in argv:
        cible = argv[argv.index('--type') + 1].lower()
        for i, ns, nom, _, _ in asm.types():
            if cible not in nom.lower():
                continue
            print('=== %s%s  (type %d)' % (ns + '.' if ns else '', nom, i))
            ch = asm.champs_de(i)
            print('   %d champ(s) :' % len(ch))
            for _, c in ch:
                print('      %s' % c)
            me = asm.methodes_de(i)
            print('   %d methode(s) :' % len(me))
            for m, n, rva in me:
                cil = asm.corps(rva)
                print('      %-46s %s' % (n, ('%d octets de CIL' % len(cil))
                                          if cil else '(abstraite)'))
            print()
        return 0

    if '--methode' in argv:
        cible = argv[argv.index('--methode') + 1]
        cls, _, meth = cible.rpartition('.')
        for i, ns, nom, _, _ in asm.types():
            if cls and cls.lower() not in nom.lower():
                continue
            for m, n, rva in asm.methodes_de(i):
                if n.lower() != meth.lower():
                    continue
                cil = asm.corps(rva)
                print('=== %s.%s  (%d octets)' % (nom, n, len(cil or b'')))
                if cil:
                    for l in desassembler(asm, cil):
                        print('   %s' % l)
                print()
        return 0

    if '--cherche' in argv:
        motif = argv[argv.index('--cherche') + 1].lower()
        for i, ns, nom, _, _ in asm.types():
            if motif in nom.lower():
                print('type    %s' % nom)
            for m, n, rva in asm.methodes_de(i):
                if motif in n.lower():
                    print('methode %s.%s' % (nom, n))
            for _, c in asm.champs_de(i):
                if motif in c.lower():
                    print('champ   %s.%s' % (nom, c))
        return 0

    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
