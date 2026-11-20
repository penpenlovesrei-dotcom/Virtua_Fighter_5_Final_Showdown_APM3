#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Genere la table d'exports d'apm.dll : le .def, les tremplins .asm, les noms.

POURQUOI UN GENERATEUR ET PAS UNE LISTE ECRITE A LA MAIN.

Un proxy de DLL doit reproduire la table ENTIERE -- les noms ET les numeros
d'ordre ([[proxy-dll-reproduit-la-table-entiere]]). apm.dll en expose 106, tous
nommes, ordinaux 1 a 106 en ordre alphabetique. Une liste recopiee se trompe ;
une liste relue de la vraie DLL ne se trompe pas. On relit donc la vraie table
a chaque compilation.

CE QUE LE GENERATEUR PRODUIT :

  apm_inerte.def      la table d'exports, chaque nom a son ordinal VRAI
  apm_tremplins.asm   106 tremplins nus + le tramway commun
  apm_noms.inc        le tableau de noms, pour que le journal nomme ce qu'il voit

POURQUOI DES TREMPLINS EN ASSEMBLEUR ET PAS DES FONCTIONS C.

On ne connait PAS les signatures des 106 fonctions. Les declarer en C, c'est
deviner le type de retour : une fonction qui rend un flottant le rend dans
XMM0, une qui rend une grosse structure recoit un pointeur cache en RCX et
doit le rendre dans RAX. Se tromper corrompt l'appelant au lieu de le mesurer,
et un instrument ne doit pas pouvoir tuer son sujet
([[instrument-ne-doit-pas-tuer-le-sujet]]).

Un tremplin qui journalise puis fait `jmp` vers la vraie fonction ne touche a
aucune convention : les arguments restent ou ils sont, la pile de l'appelant
est intacte, et la valeur de retour est celle de la vraie fonction, quel que
soit son type. C'est la SEULE facon correcte de relayer une signature inconnue.
"""
import io
import re
import struct
import sys

VRAIE = sys.argv[1] if len(sys.argv) > 1 else (
    r"..\..\SOURCES\lib\apm.dll")


def exports(chemin):
    """Relit la table d'exports d'un PE64. Noms et ordinaux, rien d'autre."""
    d = io.open(chemin, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    if d[pe:pe + 4] != b"PE\0\0":
        sys.exit("ECHEC : %s n'est pas un PE" % chemin)
    nSec, = struct.unpack_from("<H", d, pe + 6)
    tOpt, = struct.unpack_from("<H", d, pe + 20)
    p64 = struct.unpack_from("<H", d, pe + 24)[0] == 0x20B
    secs = []
    for i in range(nSec):
        o = pe + 24 + tOpt + i * 40
        vt, va, tb, pb = struct.unpack_from("<IIII", d, o + 8)
        secs.append((va, vt, pb, tb))

    def off(r):
        for va, vt, pb, tb in secs:
            if va <= r < va + max(vt, tb):
                return pb + (r - va)
        return None

    expRva, _ = struct.unpack_from("<II", d, pe + 24 + (112 if p64 else 96))
    o = off(expRva)
    base, = struct.unpack_from("<I", d, o + 16)
    _, nNom = struct.unpack_from("<II", d, o + 20)
    _, aNom, aOrd = struct.unpack_from("<III", d, o + 28)
    on, oo = off(aNom), off(aOrd)
    res = []
    for i in range(nNom):
        nr, = struct.unpack_from("<I", d, on + i * 4)
        h = off(nr)
        nom = d[h:d.index(b"\0", h)].decode("latin-1")
        ordi, = struct.unpack_from("<H", d, oo + i * 2)
        res.append((base + ordi, nom))
    return sorted(res)


tab = exports(VRAIE)
print("# %s : %d exports, ordinaux %d a %d"
      % (VRAIE, len(tab), tab[0][0], tab[-1][0]))

# Un nom non conforme a l'assembleur casserait la compilation sans le dire
# clairement : on le refuse tout de suite.
for _, n in tab:
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", n):
        sys.exit("ECHEC : nom inexploitable en assembleur : %r" % n)

# --------------------------------------------------------------- le .def
with io.open("apm_inerte.def", "w", newline="\r\n") as f:
    f.write("; GENERE PAR gen_table.py -- NE PAS MODIFIER A LA MAIN.\n")
    f.write("; Les ordinaux sont ceux de la vraie apm.dll, pas une renumerotation :\n")
    f.write("; un appelant qui importe par ordinal doit trouver la meme fonction.\n")
    f.write("LIBRARY apm\n")
    f.write("EXPORTS\n")
    for ordi, nom in tab:
        f.write("    %-42s @%d\n" % (nom, ordi))

# --------------------------------------------------------------- les noms
with io.open("apm_noms.inc", "w", newline="\r\n") as f:
    f.write("/* GENERE PAR gen_table.py -- NE PAS MODIFIER A LA MAIN. */\n")
    f.write("static const char* const kNoms[] = {\n")
    for _, nom in tab:
        f.write('    "%s",\n' % nom)
    f.write("};\n")
    f.write("static const int kNombre = %d;\n" % len(tab))

# --------------------------------------------------------------- les tremplins
#
# Disposition du cadre du tramway, 0x98 octets.
#
# A l'entree d'une fonction, RSP vaut 8 modulo 16 (le `call` de l'appelant a
# empile l'adresse de retour). Pour que NOTRE `call` presente un RSP aligne a
# 16 au callee, il faut retrancher un multiple de 16 PLUS 8 : 0x98 = 9*16 + 8.
# Se tromper ici fait fauter le premier `movaps` du callee, et la faute serait
# imputee a apm.dll alors qu'elle viendrait de nous
# ([[faute-chez-le-callee-est-une-consequence]]).
#
#   [rsp+00h..1Fh]  espace d'ombre des appels qu'on emet
#   [rsp+20h]       5e argument de ApmNoter
#   [rsp+28h]       RCX sauve        [rsp+30h]  RDX sauve
#   [rsp+38h]       R8 sauve         [rsp+40h]  R9 sauve
#   [rsp+48h]       l'indice
#   [rsp+50h/60h/70h/80h]  XMM0..XMM3 (alignes a 16 : RSP l'est apres le sub)
#
# On ne sauve QUE les registres volatiles qui portent des arguments. Les
# non-volatiles, le callee les preservera lui-meme.
with io.open("apm_tremplins.asm", "w", newline="\r\n") as f:
    f.write("; GENERE PAR gen_table.py -- NE PAS MODIFIER A LA MAIN.\n")
    f.write("; %d tremplins : journaliser, puis sauter. Aucune convention touchee.\n\n"
            % len(tab))
    f.write("EXTERN ApmNoter:PROC\n")
    f.write("EXTERN ApmCible:PROC\n\n")
    f.write(".code\n\n")
    f.write("""
; Tramway commun. L'indice arrive dans EAX, pose par le tremplin appelant.
; On journalise ce que le tremplin TRANSMET (les quatre registres
; d'arguments), pas une interpretation ([[instrument-cause-la-faute]]).
Tramway PROC
        sub     rsp, 98h
        mov     [rsp+28h], rcx
        mov     [rsp+30h], rdx
        mov     [rsp+38h], r8
        mov     [rsp+40h], r9
        mov     [rsp+48h], rax
        movaps  [rsp+50h], xmm0
        movaps  [rsp+60h], xmm1
        movaps  [rsp+70h], xmm2
        movaps  [rsp+80h], xmm3

        ; ApmNoter(indice, rcx, rdx, r8, r9)
        mov     ecx, eax
        mov     rdx, [rsp+28h]
        mov     r8,  [rsp+30h]
        mov     r9,  [rsp+38h]
        mov     rax, [rsp+40h]
        mov     [rsp+20h], rax
        call    ApmNoter

        ; ApmCible(indice) : la vraie fonction, ou notre reponse inerte.
        mov     ecx, dword ptr [rsp+48h]
        call    ApmCible

        ; On rend a l'appelant la pile et les registres exactement tels
        ; qu'il les a poses, puis on saute. Pas de `ret` ici : la valeur de
        ; retour est celle de la cible, quel que soit son type.
        movaps  xmm0, [rsp+50h]
        movaps  xmm1, [rsp+60h]
        movaps  xmm2, [rsp+70h]
        movaps  xmm3, [rsp+80h]
        mov     rcx, [rsp+28h]
        mov     rdx, [rsp+30h]
        mov     r8,  [rsp+38h]
        mov     r9,  [rsp+40h]
        add     rsp, 98h
        jmp     rax
Tramway ENDP

""")
    for i, (ordi, nom) in enumerate(tab):
        f.write("%s PROC\n        mov     eax, %d\n        jmp     Tramway\n%s ENDP\n\n"
                % (nom, i, nom))
    f.write("END\n")

print("ecrit : apm_inerte.def, apm_noms.inc, apm_tremplins.asm")
for ordi, nom in tab[:3]:
    print("   @%-3d %s" % (ordi, nom))
print("   ...")
for ordi, nom in tab[-2:]:
    print("   @%-3d %s" % (ordi, nom))
