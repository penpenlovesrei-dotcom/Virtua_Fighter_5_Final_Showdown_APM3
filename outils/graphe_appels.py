#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le graphe d'appels du moteur, bati par BALAYAGE LINEAIRE, et sa remontee.

Deux precautions, chacune payee sur ce chantier :

1. **Les appels se cherchent par motif d'octets**, pas en desassemblant les
   seules fonctions de `.pdata`. On balaie toute la section executable a la
   recherche de `E8`/`E9` + rel32. Rien ne peut manquer.

2. **Une entree `.pdata` n'est pas une fonction.** Quand son `UNWIND_INFO`
   porte le drapeau `UNW_FLAG_CHAININFO` (0x04), l'entree n'est qu'un FRAGMENT
   d'une fonction plus grande, et il faut remonter a l'entree mere. Sans cela,
   « appelee par 0x1802C4466 » designe un morceau anonyme au lieu de la
   fonction qui le contient.

Le site d'appel, lui, est toujours dans une fonction qui a une entree
`.pdata` : sur x64, appeler impose de reserver l'espace d'ombre, donc un
prologue, donc une entree de deroulement. Le graphe des APPELANTS est donc
complet ; c'est le graphe des APPELES qui reste minorant (appels indirects par
vtable).

Usage :
    py -3 tools/graphe_appels.py appelants 0x1802C2B40
    py -3 tools/graphe_appels.py remonter  0x1802C2B40 --prof 6
    py -3 tools/graphe_appels.py appeles   0x1802D9920
"""
import collections
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import pe_disasm as P                                          # noqa: E402
import rtti                                                    # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')


def entrees_pdata(img):
    """(debut, fin, rva_unwind) pour chaque entree, non fusionnees."""
    sec = next((s for s in img.secs if s['name'] == '.pdata'), None)
    if sec is None:
        return []
    blob = img.data[sec['off']:sec['off'] + sec['rsize']]
    out = []
    for i in range(0, len(blob) - 11, 12):
        beg, end, unw = struct.unpack_from('<III', blob, i)
        if beg == 0 and end == 0 or end <= beg:
            continue
        out.append((img.base + beg, img.base + end, unw))
    out.sort()
    return out


def fonctions_reelles(img):
    """Bornes des VRAIES fonctions : les fragments chaines sont rattaches.

    Rend (debuts_tries, deb -> fin) ou `deb` est le debut de la fonction mere.
    """
    ent = entrees_pdata(img)
    mere = {}
    for deb, fin, unw in ent:
        p = deb
        vu = set()
        u = unw
        while u and u not in vu:
            vu.add(u)
            o = img.va2off(img.base + u)
            if o is None:
                break
            ver_flags, _prol, n_codes, _fr = img.data[o:o + 4]
            if not (ver_flags >> 3) & 0x04:                   # pas de chainage
                break
            saut = 4 + 2 * ((n_codes + 1) & ~1)
            pb, _pe, pu = struct.unpack_from('<III', img.data, o + saut)
            p = img.base + pb
            u = pu
        mere[deb] = p
    bornes = {}
    for deb, fin, _u in ent:
        m = mere[deb]
        b = bornes.get(m)
        bornes[m] = (min(b[0], deb) if b else m, max(b[1], fin) if b else fin)
    return sorted(bornes), {k: v[1] for k, v in bornes.items()}


def construire(img):
    debuts, fins = fonctions_reelles(img)

    def contenant(va):
        lo, hi = 0, len(debuts) - 1
        r = None
        while lo <= hi:
            m = (lo + hi) // 2
            if debuts[m] <= va:
                r = debuts[m]
                lo = m + 1
            else:
                hi = m - 1
        return r if r is not None and va < fins[r] else None

    appels = collections.defaultdict(set)      # appelant -> {cibles}
    appelants = collections.defaultdict(set)   # cible -> {appelants}
    sites = collections.defaultdict(list)      # cible -> [(site, appelant)]
    for s in img.secs:
        if not s['exec']:
            continue
        blob = img.data[s['off']:s['off'] + s['rsize']]
        base = s['va']
        for i in range(len(blob) - 4):
            if blob[i] != 0xE8 and blob[i] != 0xE9:
                continue
            rel = struct.unpack_from('<i', blob, i + 1)[0]
            cible = base + i + 5 + rel
            if img.sec_of(cible) is None or not img.sec_of(cible)['exec']:
                continue
            src = base + i
            f = contenant(src)
            if f is None:
                continue
            if cible == f:                     # queue d'appel a soi-meme
                continue
            appels[f].add(cible)
            appelants[cible].add(f)
            if len(sites[cible]) < 40:
                sites[cible].append((src, f))
    return debuts, fins, contenant, appels, appelants, sites


def noms(img):
    """va(fonction) -> classe::creneau, quand une vtable la designe."""
    tds, cols, vtables = rtti.collecter(img)
    out = {}
    for va, nom in vtables:
        for i in range(24):
            q = img.read(va + i * 8, 8)
            if len(q) < 8:
                break
            v = struct.unpack('<Q', q)[0]
            s = img.sec_of(v)
            if s is None or not s['exec']:
                break
            out.setdefault(v, '%s[%d]' % (nom, i))
    return out


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    mode, cible = sys.argv[1], int(sys.argv[2], 0)
    prof = 4
    if '--prof' in sys.argv:
        prof = int(sys.argv[sys.argv.index('--prof') + 1])
    img = P.Image(MOTEUR)
    debuts, fins, contenant, appels, appelants, sites = construire(img)
    nm = noms(img)

    def etiq(va):
        n = nm.get(va)
        return '0x%X%s' % (va, ('  <%s>' % n) if n else '')

    if mode == 'appelants':
        c = contenant(cible) or cible
        print('%s  (fonction 0x%X)' % (etiq(cible), c))
        for src, f in sorted(sites.get(cible, ())):
            print('  site 0x%-11X dans %s' % (src, etiq(f)))
        if not sites.get(cible):
            print('  aucun appel direct (vtable, table de pointeurs, ou mort)')
    elif mode == 'appeles':
        c = contenant(cible) or cible
        for t in sorted(appels.get(c, ())):
            print('  -> %s' % etiq(t))
    elif mode == 'remonter':
        vus = {cible}
        niveau = [cible]
        for d in range(prof):
            suiv = []
            print('--- niveau %d ---' % d)
            for f in niveau:
                for a in sorted(appelants.get(f, ())):
                    print('  %s  <- appelle %s' % (etiq(a), etiq(f)))
                    if a not in vus:
                        vus.add(a)
                        suiv.append(a)
            if not suiv:
                print('  (racine atteinte)')
                break
            niveau = suiv
    return 0


if __name__ == '__main__':
    sys.exit(main())
