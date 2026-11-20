#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Compare deux tables d'exports PE, nom par nom et ordinal par ordinal.

A QUOI CA SERT. Un proxy de DLL ne vaut que s'il reproduit la table entiere --
les noms ET les numeros d'ordre ([[proxy-dll-reproduit-la-table-entiere]]). Un
export manquant se voit a l'execution par un refus de chargement sans message
utile ; un ordinal decale se voit par un appel qui part dans la mauvaise
fonction, et ca ne se voit pas du tout.

On valide donc l'instrument sur une reponse connue, avant de s'en servir.
Code de retour 0 si les deux tables concordent, 1 sinon.
"""
import io
import struct
import sys


def exports(chemin):
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

    rva, taille = struct.unpack_from("<II", d, pe + 24 + (112 if p64 else 96))
    if rva == 0 or taille == 0:
        return []
    o = off(rva)
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


vraie, notre = exports(sys.argv[1]), exports(sys.argv[2])
print("  vraie : %d exports    notre : %d exports" % (len(vraie), len(notre)))

dv, dn = dict((n, o) for o, n in vraie), dict((n, o) for o, n in notre)
fautes = []
for nom, ordi in sorted(dv.items()):
    if nom not in dn:
        fautes.append("ABSENT de notre table : %s (@%d)" % (nom, ordi))
    elif dn[nom] != ordi:
        fautes.append("ORDINAL FAUX : %s attendu @%d, trouve @%d"
                      % (nom, ordi, dn[nom]))
for nom in sorted(dn):
    if nom not in dv:
        fautes.append("EN TROP dans notre table : %s (@%d)" % (nom, dn[nom]))

if fautes:
    print("  >>> %d FAUTE(S) :" % len(fautes))
    for f in fautes[:30]:
        print("      " + f)
    sys.exit(1)
print("  >>> les deux tables concordent : memes noms, memes ordinaux.")
