#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QUI APPELLE QUI dans l'image PowerPC de Final Showdown.

L'outil qui manquait, et il manquait DEUX fois (journal 100 et 103) :

  . pour trancher quelle direction change de categorie dans « select part » --
    la page part de la console ne lit pas les directions elle-meme, il faut
    donc remonter a sa mise a jour pour voir quel curseur elle consulte ;
  . pour trouver la fonction qui EQUIPE un objet sur le modele, que la borne
    ne fait plus.

`x360_ppc.py xref` ne sait chercher que les adresses CONSTRUITES, en
`lis`/`addi` sur deux instructions. Un appel, lui, est une seule instruction
de forme I, et il se lit exactement :

    bl cible   ->  mot & 0xFC000003 == 0x48000001
                   deplacement = sign_extend_26(mot & 0x03FFFFFC)
                   cible = adresse + deplacement

AA=1 (adresse absolue) et LK=0 (simple branchement) sont ecartes par le
masque. C'est EXACT, pas heuristique : aucun autre encodage ne produit ce
motif.

CE QUE CET OUTIL NE PEUT PAS VOIR, ET IL FAUT LE SAVOIR AVANT DE CONCLURE :
les appels INDIRECTS. Une methode virtuelle part en `bctrl`, apres un
`mtctr` charge depuis une vtable, et aucun balayage ne la relie a sa cible.
« Personne n'appelle X » ne veut donc dire que « aucun appel DIRECT » -- pour
une methode de vtable, c'est la regle, pas l'exception. Dans ce cas c'est
`x360_ppc.py vtable` qu'il faut, pas celui-ci.

Usage :
    py -3 tools/x360_appels.py vers 0x822352E4    qui appelle cette fonction
    py -3 tools/x360_appels.py depuis 0x82231A50  ce que cette fonction appelle
    py -3 tools/x360_appels.py vers 0x822352E4 --remonter
        remonte aussi d'un cran : les appelants des appelants
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import x360_ppc                                              # noqa: E402


def _cible(mot, adresse):
    """La cible d'un `bl`, ou None si ce mot n'en est pas un."""
    if (mot & 0xFC000003) != 0x48000001:
        return None
    d = mot & 0x03FFFFFC
    if d & 0x02000000:                      # le deplacement est SIGNE sur 26
        d -= 0x04000000
    return (adresse + d) & 0xFFFFFFFF


def tous_les_appels(img):
    """{appelant: cible} pour chaque `bl` des sections executables."""
    out = []
    for s in img.secs:
        if not s['exec']:
            continue
        va0 = s['va']
        brut = img.d[img.off(va0):img.off(va0) + s['vsize']]
        for i in range(0, len(brut) - 3, 4):
            mot = int.from_bytes(brut[i:i + 4], 'big')
            c = _cible(mot, va0 + i)
            if c is not None:
                out.append((va0 + i, c))
    return out


def debut_de(img, va, recul=0x800):
    """Le debut probable de la fonction qui contient `va`.

    On remonte jusqu'a un `mflr r12` (0x7D8802A6), le prologue que ce
    compilateur pose en tete de toute fonction qui appelle. A defaut on rend
    None plutot que de deviner : une borne fausse ferait pire que rien.
    """
    base = va - (va % 4)
    for k in range(0, recul, 4):
        a = base - k
        try:
            mot = int.from_bytes(img.lire(a, 4), 'big')
        except x360_ppc.Refus:
            return None
        if mot == 0x7D8802A6:               # mflr r12
            return a
    return None


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        print(__doc__)
        return 1
    quoi, va = a[0], int(a[1], 0)
    img = x360_ppc.Image()
    appels = tous_les_appels(img)

    if quoi == 'depuis':
        fin = va + 0x1000
        liste = [(s, c) for s, c in appels if va <= s < fin]
        print('ce que 0x%08X appelle (jusqu a 0x%X) : %d appel(s)'
              % (va, fin, len(liste)))
        vus = {}
        for s, c in liste:
            vus.setdefault(c, []).append(s)
        for c in sorted(vus):
            print('  -> 0x%08X   depuis %s'
                  % (c, ', '.join('0x%X' % x for x in vus[c][:4])))
        return 0

    if quoi != 'vers':
        print(__doc__)
        return 1

    liste = [s for s, c in appels if c == va]
    print('0x%08X : %d appel(s) DIRECT(S)' % (va, len(liste)))
    if not liste:
        print('  Aucun. Attention : une methode de vtable part en `bctrl` et')
        print('  n apparait dans AUCUN balayage. Essayez x360_ppc.py vtable.')
    fonctions = {}
    for s in sorted(liste):
        d = debut_de(img, s)
        fonctions.setdefault(d, []).append(s)
        print('  0x%08X   dans %s'
              % (s, ('0x%08X' % d) if d else 'fonction non bornee'))

    if '--remonter' in a:
        print()
        print('UN CRAN PLUS HAUT -- les appelants des appelants :')
        for f in sorted(x for x in fonctions if x):
            sup = [s for s, c in appels if c == f]
            print('  0x%08X <- %d appel(s)%s'
                  % (f, len(sup),
                     ('  : ' + ', '.join('0x%X' % x for x in sup[:6]))
                     if sup else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
