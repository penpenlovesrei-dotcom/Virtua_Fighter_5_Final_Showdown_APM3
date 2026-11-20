"""Qui lit, et surtout qui ECRIT, un champ d'objet dans l'image Xbox 360.

POURQUOI (2026-10-03). La page « select part » de la borne tient la position
de son curseur dans sa PROPRE grille, et le seul code qui la deplacait est un
consommateur de messages dont plus personne n'est le producteur. Cote Xbox
360 la meme page marche, et sa mise a jour (`0x82231A50`) calcule son index
ainsi :

    lwz  r10, 0x750(r31)      ; le defilement
    lwz  r11, 0x74c(r31)      ; la position dans la page
    lwz  r9,  0x73c(r31)      ; la table
    add  r8, r10, r11
    slwi r7, r8, 1
    lhzx r30, r7, r9          ; table[defilement + position]

Reste LA question : qui ECRIT `+0x750` et `+0x74C` ? C'est la liaison
curseur -> grille, celle qu'il ne faut surtout pas inventer.

`xref` de `x360_ppc.py` cherche une ADRESSE construite en deux instructions.
Un champ d'objet, lui, ne se construit pas : il s'ecrit en UN mot, de la
forme D :

    op<<26 | S<<21 | A<<16 | deplacement sur 16 bits

Il suffit donc de balayer les sections executables et de retenir les mots
dont les seize bits bas valent le deplacement cherche et dont l'opcode est
une lecture ou une ecriture memoire. C'est exact, pas heuristique : aucun
autre encodage ne peut produire ce couple.

LE PIEGE A NE PAS OUBLIER : un deplacement est SIGNE. `0x750` se lit tel
quel, mais un champ au-dela de `0x7FFF` apparait en negatif, et le registre
de base a alors ete corrige en amont. On refuse donc tout deplacement
superieur a 0x7FFF plutot que de rendre un releve faux en silence.

Usage :
    py -3 tools/x360_champ.py 0x750
    py -3 tools/x360_champ.py 0x750 --ecritures
    py -3 tools/x360_champ.py 0x750 0x74c --registre r31
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import x360_ppc


# Les formes D qui touchent la memoire. Le nom sert au releve ; le booleen
# dit si c'est une ECRITURE -- c'est la seule colonne qui compte ici.
FORMES = {
    32: ('lwz', False), 33: ('lwzu', False),
    34: ('lbz', False), 35: ('lbzu', False),
    40: ('lhz', False), 41: ('lhzu', False),
    42: ('lha', False), 43: ('lhau', False),
    36: ('stw', True), 37: ('stwu', True),
    38: ('stb', True), 39: ('stbu', True),
    44: ('sth', True), 45: ('sthu', True),
    48: ('lfs', False), 50: ('lfd', False),
    52: ('stfs', True), 54: ('stfd', True),
}


def acces(img, dep, ecritures_seules=False, registre=None):
    """Tous les acces memoire au deplacement `dep`, dans le code."""
    if not 0 <= dep <= 0x7FFF:
        raise x360_ppc.Refus(
            'deplacement 0x%X hors de la plage non signee : au-dela de 0x7FFF '
            'il est NEGATIF dans le code et le releve serait faux' % dep)
    out = []
    for s in img.secs:
        if not s['exec']:
            continue
        va0 = s['va']
        o0 = img.off(va0)
        brut = img.d[o0:o0 + s['vsize']]
        for i in range(0, len(brut) - 3, 4):
            w = int.from_bytes(brut[i:i + 4], 'big')
            if (w & 0xFFFF) != dep:
                continue
            forme = FORMES.get(w >> 26)
            if forme is None:
                continue
            nom, est_ecriture = forme
            if ecritures_seules and not est_ecriture:
                continue
            rs = (w >> 21) & 31
            ra = (w >> 16) & 31
            if ra == 0:
                # `rA = 0` veut dire la valeur zero, pas le registre r0 :
                # c'est un acces absolu, jamais un champ d'objet.
                continue
            if ra == 1:
                # r1 EST LE POINTEUR DE PILE en PowerPC, et une variable
                # locale n'est pas un champ d'objet. Sans ce filtre l'outil
                # rend des `lbz r6, 0x50(r1)` comme s'ils lisaient le curseur
                # horizontal d'une page -- c'est arrive le 2026-10-04, et une
                # mesure fausse coute plus cher qu'une mesure absente. Le
                # pendant x64 filtrait deja rsp et rbp ; celui-ci l'avait
                # oublie.
                continue
            if registre is not None and ra != registre:
                continue
            out.append(dict(va=va0 + i, mot=w, nom=nom, ecriture=est_ecriture,
                            rs=rs, ra=ra))
    return out


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 0
    ecritures = '--ecritures' in a
    registre = None
    if '--registre' in a:
        k = a.index('--registre')
        registre = int(a[k + 1].lstrip('rR'))
        del a[k:k + 2]
    deps = [int(x, 0) for x in a if not x.startswith('--')]
    img = x360_ppc.Image()
    for dep in deps:
        liste = acces(img, dep, ecritures, registre)
        ecr = [x for x in liste if x['ecriture']]
        print()
        print('+0x%X : %d acces, dont %d ECRITURE(S)%s'
              % (dep, len(liste), len(ecr),
                 '' if registre is None else '  [base r%d seulement]' % registre))
        print('-' * 70)
        for x in liste:
            print('  0x%08X  %-6s %-3s r%-2d, 0x%X(r%d)'
                  % (x['va'], 'ECRIT' if x['ecriture'] else 'lit',
                     x['nom'], x['rs'], dep, x['ra']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
