#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""POURQUOI LE CURSEUR NE BOUGE PAS DANS L'ECRAN DE PERSONNALISATION.

Observation de Frederic, a l'ecran, le 2026-09-30 :

    « ENTREE valide, W annule ; HAUT / BAS et GAUCHE / DROITE des fleches du
      clavier ne font pas bouger de curseur »

et c'est vrai AVEC et SANS `--wxga`. Ses observations priment : le suspect
numero un de `menu_console.md` §15.3 est innocente.

Le repartiteur des pages de menu, `0x1801BBBE0`, se lit ainsi :

    0x1801BBBFE  cmp dword [page+0x224], 0   ; nombre de crans VERTICAUX
    0x1801BBC19  jle ...                     ; <= 0 -> aucun deplacement
    0x1801BBC69  cmp dword [page+0x22C], 0   ; nombre de crans HORIZONTAUX
    0x1801BBC70  jle ...                     ; <= 0 -> aucun deplacement
    0x1801BBCC6  call 0x1801A2B90            ; ANNULER : toujours lu
    0x1801BBCDD  call 0x1801A2BC0            ; VALIDER : toujours lu

Un compteur a zero donne donc EXACTEMENT le symptome : valider et annuler
marchent, rien ne bouge. Cet outil cherche, page par page, qui pose ces
compteurs et qui les efface.

    py -3 tools/curseur_customize.py
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import capstone                                              # noqa: E402
import pe_disasm as P                                        # noqa: E402
import boutons_terminal as B                                 # noqa: E402

MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')

CHAMPS = {0x224: 'V nombre', 0x228: 'V boucle',
          0x22C: 'H nombre', 0x230: 'H boucle'}

# Les pages du parcours TERMINAL -> Customize, par leur vtable (RTTI).
# creneau [1] = l'entree, celle qui arme la page.
PAGES = [
    ('TaskDataSelector', 0x180530FF0),
    ('CharSelector', 0x180530F30),
    ('DataSelector', 0x180530F90),
    ('TaskCustomizeMenu', 0x180530420),
    ('TaskCostumeMenu', 0x1805303C0),
    ('TaskSelItemMenu', 0x1805304E0),
    ('TaskSelPartMenu', 0x180530540),
    ('TaskExclWarning', 0x180530360),
    ('TaskHelpWindow', 0x180530480),
    # le temoin : celle-ci marche a l'ecran (le curseur y bouge)
    ('TaskMenuTerminal  [TEMOIN]', 0x180532A28),
]
REG32 = {'eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp',
         'r8d', 'r9d', 'r10d', 'r11d', 'r12d', 'r13d', 'r14d', 'r15d'}
REG8 = {'al': 'eax', 'bl': 'ebx', 'cl': 'ecx', 'dl': 'edx', 'sil': 'esi',
        'dil': 'edi', 'bpl': 'ebp', 'r8b': 'r8d', 'r9b': 'r9d',
        'r10b': 'r10d', 'r11b': 'r11d', 'r12b': 'r12d', 'r13b': 'r13d',
        'r14b': 'r14d', 'r15b': 'r15d'}


def vtable(img, va, n=12):
    d = img.read(va, 8 * n)
    return [struct.unpack_from('<Q', d, 8 * i)[0] for i in range(n)]


def etudier(img, frag, entree):
    """Les ecritures des quatre compteurs dans le fragment de `entree`.

    Suivi minimal : un registre mis a zero par `xor r, r` vaut 0 tant que
    rien ne le reecrit. C'est tout ce qu'il faut ici -- les valeurs posees
    sont des immediats, et les effacements des registres a zero.

    Rend aussi les CIBLES DE SAUT du fragment : sans elles, on ne peut pas
    distinguer « la page pose 6 puis l'efface » de « la page pose 6 dans une
    branche et 0 dans l'autre ». C'est toute la difference entre un maillon
    retire et un simple `if`.
    """
    f = B.fonction_de(frag, entree)
    if f is None:
        return None, [], set()
    deb, fin = f
    off = img.va2off(deb)
    zero = set()
    out = []
    cibles = []                       # (origine du saut, cible)
    for i in img.md.disasm(img.data[off:off + (fin - deb)], deb):
        if i.group(capstone.CS_GRP_JUMP) and i.op_str.startswith('0x'):
            cibles.append((i.address, int(i.op_str, 16)))
    for i in img.md.disasm(img.data[off:off + (fin - deb)], deb):
        m, o = i.mnemonic, i.op_str
        g = o.split(',')[0].strip()
        if m == 'xor' and ',' in o and g == o.split(',')[1].strip():
            zero.add(g)
            continue
        # toute autre ecriture dans un registre le sort de l'ensemble
        if g in REG32 and m != 'cmp' and m != 'test':
            zero.discard(g)
        if g in REG8 and m != 'cmp' and m != 'test':
            zero.discard(REG8[g])
        if m != 'mov' or not g.endswith(']'):
            continue
        for ch, nom in CHAMPS.items():
            if '+ 0x%x]' % ch not in o.lower():
                continue
            src = o.split('],')[1].strip()
            if src.startswith('0x'):
                val, sur = int(src, 16), True
            elif src.isdigit():
                val, sur = int(src), True
            elif src in REG32:
                val, sur = (0, True) if src in zero else (None, False)
            elif src in REG8:
                val, sur = (0, True) if REG8[src] in zero else (None, False)
            else:
                val, sur = None, False
            out.append((i.address, ch, nom, val, sur, src))
            break
    return (deb, fin), out, cibles


def main():
    img = P.Image(MOTEUR)
    frag = B.pdata(img)
    print()
    print('LE CURSEUR DE L ECRAN DE PERSONNALISATION -- %s'
          % os.path.basename(MOTEUR))
    print()
    print('`0x1801BBBE0` ne deplace un curseur que si son compteur est > 0.')
    print('Voici, page par page, ce que son ENTREE (creneau 1) ecrit dans les')
    print('quatre compteurs, DANS L ORDRE DU CODE. La DERNIERE ecriture de')
    print('chaque champ est celle qui compte.')
    print()
    morts = []
    for nom, vt in PAGES:
        v = vtable(img, vt)
        entree = v[1]
        bornes, ecr, cibles = etudier(img, frag, entree)
        print('=' * 74)
        print('%-28s vtable 0x%X   entree 0x%X' % (nom, vt, entree))
        if bornes:
            print('  fragment 0x%X .. 0x%X (%d o), %d cible(s) de saut'
                  % (bornes[0], bornes[1], bornes[1] - bornes[0],
                     len(set(c for _, c in cibles))))
        if not ecr:
            print('  aucune ecriture des compteurs dans ce fragment.')
            continue
        dernier, pose = {}, {}
        for site, ch, cnom, val, sur, src in ecr:
            etat = ('= %d' % val) if sur else ('= %s (non suivi)' % src)
            print('  0x%-10X %-9s %s' % (site, cnom, etat))
            if sur and val:
                pose[ch] = (site, val)
            dernier[ch] = (site, val, sur, src)
        verdict = []
        for ch, quoi in ((0x224, 'VERTICAL'), (0x22C, 'HORIZONTAL')):
            d = dernier.get(ch)
            if d is None:
                verdict.append('%s : jamais pose' % quoi)
                continue
            if not d[2]:
                verdict.append('%s : %s, non suivi' % (quoi, d[3]))
                continue
            if d[1]:
                verdict.append('%s : %d' % (quoi, d[1]))
                continue
            p = pose.get(ch)
            if p is None:
                verdict.append('%s : 0, et jamais rien d autre' % quoi)
                continue
            # LA PREUVE que l'effacement est inconditionnel. Il ne suffit pas
            # qu'aucune cible de saut ne tombe entre la pose et l'effacement :
            # deux branches qui CONVERGENT avant l'effacement l'atteignent
            # quand meme. Deux conditions, et elles suffisent :
            #   (a) toute cible de saut dans ]pose, effacement] n'est visee
            #       que depuis l'interieur de [pose, effacement] -- sinon on
            #       peut entrer dans la zone sans etre passe par la pose ;
            #   (b) aucun saut parti de [pose, effacement[ ne vise AU-DELA de
            #       l'effacement -- sinon on peut le sauter.
            dedans = [(o, c) for o, c in cibles if p[0] <= o <= d[0]]
            entrantes = [(o, c) for o, c in cibles
                         if p[0] < c <= d[0] and not (p[0] <= o <= d[0])]
            sortantes = [(o, c) for o, c in dedans if c > d[0]]
            if entrantes or sortantes:
                verdict.append('%s : %d en 0x%X puis 0 en 0x%X, mais le '
                               'chemin n est PAS force (%d saut(s) entrant(s),'
                               ' %d sortant(s)) -- ce sont des BRANCHES, pas '
                               'un effacement'
                               % (quoi, p[1], p[0], d[0],
                                  len(entrantes), len(sortantes)))
            else:
                verdict.append('%s : %d pose en 0x%X, **EFFACE** en 0x%X '
                               '(inconditionnel : aucun saut entrant ni '
                               'sortant)'
                               % (quoi, p[1], p[0], d[0]))
                morts.append((nom, quoi, p[0], p[1], d[0]))
        for v in verdict:
            print('  -> %s' % v)
    print('=' * 74)
    print()
    print('BILAN : %d compteur(s) poses puis EFFACES sur le meme chemin.'
          % len(morts))
    print()
    print('%-28s %-11s %-14s %-7s %s'
          % ('page', 'axe', 'pose en', 'valeur', 'efface en'))
    print('-' * 74)
    for nom, quoi, sp, val, se in morts:
        print('%-28s %-11s 0x%-12X %-7d 0x%X' % (nom, quoi, sp, val, se))
    print()
    print('Un compteur a zero = valider et annuler marchent, le curseur ne')
    print('bouge pas. C est le symptome de Frederic, mot pour mot.')
    print()
    print('Seul `0x1801BBBE0` deplace ces curseurs : `0x1801A2EC0` et')
    print('`0x1801A2D60` n ont aucun autre appelant dans la zone. Le compteur')
    print('est donc le SEUL verrou.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
