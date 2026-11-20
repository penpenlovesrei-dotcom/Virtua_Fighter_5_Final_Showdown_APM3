#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""LES TEXTES DU MODE QUEST : l'inventaire, releve dans le code de 2007.

Pourquoi. Porter les ecrans du Quest ne sert a rien sans leurs libelles, et il
n'etait pas question de les deviner : ils sont NOMMES par un numero dans le
code de la version Xbox 360, et le numero indexe `media/lang/<lg>/
string_array.bin` -- un tableau de pointeurs 32 bits GROS-BOUTISTES vers des
chaines UTF-8 (7 586 entrees).

Comment. Le getter est `FUN_82322798(id)` (borne `0x1D9F`, et un decalage de
0x2A sur les 42 premiers identifiants selon la manette detectee -- les
pictogrammes de boutons). On balaie le `.text` : chaque `bl 0x82322798`
precede d'un `li r3, imm` donne un identifiant demande. On ne garde que les
appels qui vivent DANS le code du Quest.

LA LACUNE, MESUREE LE 2026-09-26. Ce balayage ne voit que le `li r3, imm`
qui PRECEDE l'appel. Or le menu de la maison du Quest ecrit ses six
identifiants dans un TABLEAU DE PILE (`auStack_50[0] = 0x219; ...`) et les
relit dans la boucle : `FUN_8230BEB0` demande 0x219, 0x21A, 0x21C..0x21F et
le balayage n'en voyait AUCUN. Huit libelles manquaient, dont le titre de
la fenetre des lieux (535) et deux de ses trois lignes (599, 602).

`--immediats` corrige, et il le fait sans deviner : il releve TOUT immediat
plausible (`li rN, imm`, 0 < imm < borne) charge dans le MODULE du Quest.
Le module, c'est `0x82300000..0x82320000` -- ce n'est pas un chiffre rond
pris au hasard : c'est la plage d'ou `quest_x360.c` et
`quest_gestion_x360.c` ont ete decompiles, et la mesure du 2026-09-26 y
trouve 190 des 272 fonctions que le graphe d'appels rattache au Quest
(les 82 autres sont des utilitaires partages : AET, texte, tri). La
remontee par le graphe seule ne suffisait pas -- `FUN_8230BEB0`, le menu
de la maison, n'y figure pas. C'est une sur-approximation assumee -- une longueur, un nombre
d'images ou une couleur peuvent y passer -- mais elle ne DEPLACE aucun
identifiant : chaque chaine de trop coute quelques octets a la fin du
tableau, et rien d'autre.

    py -3 tools/quest_textes.py                  l'inventaire
    py -3 tools/quest_textes.py --langue fr      les memes, en francais
    py -3 tools/quest_textes.py --tous           tout le jeu, pas que le Quest

Sortie : `analysis/quest/textes.md`.
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import quest_x360 as qx                                     # noqa: E402

GETTER = 0x82322798
BORNE = 0x1DA0
X360 = r'C:\Users\frede\Desktop\VF5 FS DECOMP\X360_VF5\media'


def chaines(langue='en'):
    """Le tableau de `string_array.bin`, resolu. Rend une liste de str."""
    chemin = os.path.join(X360, 'lang', langue, 'string_array.bin')
    d = open(chemin, 'rb').read()
    n = struct.unpack_from('>I', d, 0)[0] // 4
    out = []
    for i in range(n):
        o = struct.unpack_from('>I', d, 4 * i)[0]
        if o == 0 or o >= len(d):
            out.append('')
            continue
        f = d.index(b'\x00', o)
        out.append(d[o:f].decode('utf-8', 'replace'))
    return out


def appels(img):
    """Les `bl GETTER` du `.text`, avec l'identifiant charge dans r3.

    On suit `li r3, imm` (= `addi r3, r0, imm`) et `lis`+`ori`, et on rend
    `(site, id)`. Un site sans constante juste avant rend `None`.
    """
    d = img.d
    a, n = img.sections['.text']
    out = []
    o = a - qx.BASE
    fin = o + n
    r3 = None
    while o < fin - 4:
        w = struct.unpack_from('>I', d, o)[0]
        op = w >> 26
        if op == 14:                                   # addi
            rt = (w >> 21) & 31
            ra = (w >> 16) & 31
            if rt == 3 and ra == 0:
                imm = w & 0xFFFF
                r3 = imm - 0x10000 if imm & 0x8000 else imm
            elif rt == 3:
                r3 = None
        elif op == 18:                                 # b / bl
            lk = w & 1
            li = w & 0x03FFFFFC
            if li & 0x02000000:
                li -= 0x04000000
            cible = (qx.BASE + (o - (a - qx.BASE))) if False else 0
            cible = (0 if (w & 2) else (qx.BASE + o - (a - qx.BASE)))
            cible = (li if (w & 2) else (qx.BASE + (o - (a - qx.BASE)) + li))
            # `o` est un offset fichier ; l'adresse de l'instruction :
            va = qx.BASE + (o - (a - qx.BASE)) + (a - qx.BASE)
            va = a + (o - (a - qx.BASE))
            cible = li if (w & 2) else va + li
            if lk and cible == GETTER:
                out.append((va, r3))
            r3 = None
        elif op in (31, 32, 36) and ((w >> 21) & 31) == 3:
            r3 = None
        o += 4
    return out


# Le module du Quest dans le `.text` de 2007. Voir le pave du haut.
MODULE = (0x82300000, 0x82320000)


def immediats(img, quest, debuts):
    """Tout `li rN, imm` plausible charge dans le MODULE du Quest.

    Rend {identifiant: [(site, proprietaire), ...]}. Voir le pave du haut :
    c'est une sur-approximation, et c'est voulu.
    """
    import bisect
    d = img.d
    a, n = img.sections['.text']
    out = {}
    o = a - qx.BASE
    fin = o + n
    while o < fin - 4:
        w = struct.unpack_from('>I', d, o)[0]
        if (w >> 26) == 14 and ((w >> 16) & 31) == 0:      # li rN, imm
            imm = w & 0xFFFF
            if 0 < imm < BORNE:
                va = a + (o - (a - qx.BASE))
                k = bisect.bisect_right(debuts, va) - 1
                proprio = debuts[k] if k >= 0 else 0
                if proprio in quest or MODULE[0] <= va < MODULE[1]:
                    out.setdefault(imm, []).append((va, proprio))
        o += 4
    return out


def main():
    a = sys.argv[1:]
    langue = a[a.index('--langue') + 1] if '--langue' in a else 'en'
    tous = '--tous' in a
    import bisect
    img = qx.Image()
    fonctions = img.fonctions()
    debuts = [f for f, _ in fonctions]
    ens_debuts = set(debuts)

    quest = set()
    if not tous:
        classes = img.classes()
        racines = set()
        for nom, vts in classes.items():
            if not nom.startswith(('TaskQuest', 'TaskTournament',
                                   'TaskItemShop', 'TaskEmblemEdit',
                                   'TaskNewEmblemList', 'TaskNewItemList',
                                   'TaskGameItemFight', 'TaskGameRank',
                                   'TaskLiveRankingUpdate',
                                   'TaskRankingUpdate', 'QuestAet')):
                continue
            for vt in vts:
                racines.update(img.methodes(vt, ens_debuts))
        app, appelants = qx.graphe(img, fonctions)
        quest = qx.propre(racines, app, appelants)

    vus = {}
    for site, ident in appels(img):
        k = bisect.bisect_right(debuts, site) - 1
        proprio = debuts[k] if k >= 0 else 0
        if not tous and proprio not in quest:
            continue
        if ident is None or not (0 <= ident < BORNE):
            continue
        vus.setdefault(ident, []).append((site, proprio))

    if '--immediats' in a and not tous:
        for ident, sites in immediats(img, quest, debuts).items():
            vus.setdefault(ident, []).extend(sites)

    tab = chaines(langue)
    lignes = ['# Les textes du mode Quest, releves dans le code de 2007', '',
              'Getter `FUN_82322798(id)`, table `media/lang/%s/'
              'string_array.bin` (%d entrees).' % (langue, len(tab)), '',
              '| id | texte (%s) | sites |' % langue, '|---:|---|---|']
    for ident in sorted(vus):
        txt = tab[ident] if ident < len(tab) else ''
        txt = txt.replace('|', chr(92) + '|').replace(chr(10), ' / ')
        lignes.append('| %d | %s | %s |'
                      % (ident, txt,
                         ' '.join('0x%08X' % s for s, _ in vus[ident][:4])))
    lignes += ['', '%d identifiant(s) distinct(s), %d site(s).'
               % (len(vus), sum(len(v) for v in vus.values()))]
    sortie = os.path.join(RACINE, 'analysis', 'quest', 'textes.md')
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    with open(sortie, 'w', encoding='utf-8') as fp:
        fp.write(chr(10).join(lignes) + chr(10))
    apercu = chr(10).join(lignes[:45])
    print(apercu.encode('ascii', 'replace').decode('ascii'))
    print('...')
    print('%s ecrit' % sortie)
    return 0


if __name__ == '__main__':
    sys.exit(main())
