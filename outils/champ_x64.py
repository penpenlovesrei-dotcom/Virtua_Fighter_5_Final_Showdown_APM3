#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Qui lit, et surtout qui ECRIT, un champ d'objet dans le moteur APM3.

Le pendant x64 de `tools/x360_champ.py`. Meme question, autre jeu
d'instructions -- et en x64 elle est NETTEMENT plus delicate, pour une raison
qu'il faut avoir en tete avant de lire un releve :

    EN POWERPC un acces memoire tient en UN mot de forme D, et le
    deplacement y occupe seize bits fixes. Le balayage est EXACT.

    EN X64 l'instruction est de longueur variable et le deplacement est un
    champ du ModRM/SIB, a une position qui depend du reste. On ne peut donc
    PAS chercher le motif d'octets : il faut DESASSEMBLER.

Et desassembler lineairement un binaire x64 DERAILLE -- c'est consigne dans
le briefing, et ca s'est paye. Un octet de donnee au milieu du code decale
tout ce qui suit, et le flot se recale au bout de quelques instructions sans
rien dire. Un releve fait d'une seule passe lineaire porterait donc des
instructions FANTOMES, et une seule suffit a faire conclure faux.

CE QUE CET OUTIL FAIT CONTRE CA : il desassemble la section depuis PLUSIEURS
points de depart decales (par defaut seize, un par octet), et ne retient un
acces que si on le retrouve a l'IDENTIQUE -- meme adresse, memes octets --
depuis au moins `--accord` deputs differents. Une instruction fantome naît
d'un recalage particulier et ne survit pas au changement de depart ; une
vraie instruction est vue par tous les deputs qui la rejoignent, et ils se
rejoignent toujours.

C'est plus lent qu'une passe unique, et c'est le prix d'un releve sur lequel
on peut ecrire du code.

POURQUOI MAINTENANT (2026-10-03). La page `TaskSelItemMenu` calcule son index
de grille ainsi (`0x1801C8139`) :

    mov   r8,  [rcx+0x9d0]
    add   r8,  [rcx+0x9c8]
    mov   rax, [rcx+0x9b0]        ; la table
    movzx ebp, word [rax+r8*2]    ; table[somme]

et son homologue Xbox 360 (`0x82231BA0`) fait mot pour mot la meme chose avec
`+0x750`, `+0x74C` et `+0x73C`. Cote console on sait lequel est quoi : `+0x750`
est borne par `cmplwi r11, 0x28`, `+0x74C` ne bouge que par pas de huit. Cote
borne on ne le sait PAS -- et l'ordre des deux lectures ne prouve rien, une
addition etant commutative et le compilateur libre de l'ordonner. Les
inverser donnerait un curseur qui defile sans bouger.

La preuve se lit donc ailleurs : dans ce que les AUTRES sites font de ces
deux champs. C'est ce que cet outil rend.

Usage :
    py -3 tools/champ_x64.py 0x9d0 0x9c8
    py -3 tools/champ_x64.py 0x9d0 --ecritures
    py -3 tools/champ_x64.py 0xee0 --plage 0x1801C0000 0x1801D0000
"""
import os
import sys

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
import pe_disasm as P                                        # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll')

# Les registres qui ne designent JAMAIS un objet : une pile n'est pas un
# `this`. Les retenir noierait le releve sous les variables locales.
PILE = (capstone.x86.X86_REG_RSP, capstone.x86.X86_REG_RBP,
        capstone.x86.X86_REG_RIP)


def acces(img, dep, lo=None, hi=None, deputs=16, accord=3):
    """Les acces memoire au deplacement `dep`, confirmes par plusieurs passes.

    Rend un dictionnaire {adresse: (octets, texte, ecriture, accords)}.
    """
    vus = {}
    for s in img.secs:
        if not s.get('exec'):
            continue
        va0, n = s['va'], s['vsize']
        if lo is not None:
            va0 = max(va0, lo)
            n = min(s['va'] + s['vsize'], hi) - va0
        if n <= 0:
            continue
        base_off = s['off'] + (va0 - s['va'])
        blob = img.data[base_off:base_off + n]
        for d in range(deputs):
            # CAPSTONE S'ARRETE AU PREMIER OCTET INDECODABLE, ET IL NE DIT
            # RIEN. Le premier jet de cet outil n'avait pas cette boucle : il
            # rendait « 0 acces » pour un champ dont on avait l'instruction
            # sous les yeux, parce que chaque passe mourait quelques
            # centaines d'octets apres son depart. Un releve vide n'est donc
            # jamais une reponse tant qu'on n'a pas REPRIS apres l'octet
            # fautif -- un octet plus loin, et on recommence.
            i = d
            while i < len(blob):
                fin = i
                for x in img.md.disasm(blob[i:], va0 + i):
                    fin = (x.address - va0) + x.size
                    _retenir(vus, x, dep)
                # `fin == i` : meme la premiere instruction est indecodable.
                # On avance d'un octet, sinon on boucle sans fin.
                i = fin + 1 if fin > i else i + 1
    return {va: tuple(v) for va, v in vus.items() if v[3] >= accord}


def _retenir(vus, x, dep):
    """Retient `x` si l'un de ses operandes memoire porte le deplacement."""
    for op in x.operands:
        if op.type != capstone.x86.X86_OP_MEM:
            continue
        if op.mem.disp != dep:
            continue
        if op.mem.base in PILE or op.mem.base == 0:
            continue
        e = vus.get(x.address)
        if e is None:
            # L'ECRITURE SE RECONNAIT A LA PLACE DE L'OPERANDE, pas au
            # mnemonique : `mov [rcx+8], rax` ecrit, `mov rax, [rcx+8]` lit,
            # et c'est le meme `mov`. capstone range le premier operande en
            # tete. `cmp` et `test` touchent la memoire sans l'ecrire.
            prem = x.operands[0]
            ecrit = (prem.type == capstone.x86.X86_OP_MEM
                     and prem.mem.disp == dep
                     and x.mnemonic not in ('cmp', 'test'))
            vus[x.address] = [x.bytes.hex(),
                              '%s %s' % (x.mnemonic, x.op_str), ecrit, 0]
        elif e[0] != x.bytes.hex():
            # Deux deputs ne s'accordent pas sur les octets de cette
            # adresse : l'un des deux est un fantome. On ne compte pas
            # l'accord, et le seuil l'ecartera.
            return
        vus[x.address][3] += 1
        return


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    ecritures = '--ecritures' in a
    lo = hi = None
    if '--plage' in a:
        k = a.index('--plage')
        lo, hi = int(a[k + 1], 0), int(a[k + 2], 0)
        del a[k:k + 3]
    chemin = MOTEUR + ('' if '--patche' in a else '.origine')
    deps = [int(x, 0) for x in a if not x.startswith('--')]
    img = P.Image(chemin)
    print('image : %s' % os.path.basename(chemin))
    for dep in deps:
        liste = acces(img, dep, lo, hi)
        ecr = {k: v for k, v in liste.items() if v[2]}
        print()
        print('+0x%X : %d acces confirme(s), dont %d ECRITURE(S)'
              % (dep, len(liste), len(ecr)))
        print('-' * 72)
        for va in sorted(liste):
            octets, texte, est_ecr, n = liste[va]
            if ecritures and not est_ecr:
                continue
            print('  0x%09X  %-5s %-46s [%d deputs]'
                  % (va, 'ECRIT' if est_ecr else 'lit', texte, n))
    return 0


if __name__ == '__main__':
    sys.exit(main())
