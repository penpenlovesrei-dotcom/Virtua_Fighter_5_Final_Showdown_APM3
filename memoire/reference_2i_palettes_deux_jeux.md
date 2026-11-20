---
name: reference-2i-palettes-deux-jeux
description: "2nd Impact a DEUX jeux de palettes, et le vert pur 0x03E0 dénonce une palette fausse sans capture."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7f4afaf5-d8a3-4dd5-9905-114b9a59832e
  modified: 2026-09-02T17:30:34.881Z
---

**2nd Impact a deux jeux de palettes**, comme New Generation — ce qui n'était pas su :

    0x8C1D5D38   table d'index du JEU 1, destination 0x02000
    0x8C1D5D16   table d'index du JEU 2, destination 0x12000
                 (34 octets avant, soit 17 bandes x 2)

    entree = 0x8C1E4B50 + index*12 = { source RAM, destination, taille }
    base   = (source - 0x02798000) / 128        nb = taille / 128

**13 décors sur 14** confirment le jeu 2 par sa destination `0x12000` : ce n'est pas une
lecture décalée au hasard. Les bases du groupe de drapeaux 9 dans `bases.BASES_2I` avaient
été calées à l'œil et étaient fausses ; elles sont maintenant celles du jeu 2. Exception
laissée : `bg0a` (Oro) garde 1674, **validé à l'écran**.

**LE DÉTECTEUR DE PALETTE FAUSSE, sans aucune capture** : le vert pur `0x03E0` est la
couleur de remplissage des cases de palette **non initialisées** (les palettes 1246 à 1253
en sont entièrement faites). Un pixel de cette couleur dénonce donc un index tombant sur
une case vide, c'est-à-dire une palette fausse. Il a tranché net sur le groupe 9 :
Hugo 850 cases vertes → 0, Yang 270 → 0, bg08 16 → 0, sans régression ailleurs.

**Sa limite** : il élimine, il ne choisit pas. Sur le groupe 1 de Hugo il reste huit
palettes candidates pour un seul offset — c'est là qu'une capture Dreamcast trancherait.

**Un objet ne porte qu'UNE palette de 64.** Or des sprites mélangent plusieurs palettes
entre leurs morceaux (21 chez Hugo, 11 chez Yang). `animer2i` fabrique donc désormais une
palette EFFECTIVE par objet — `assemblage.poser_1555` compose en ARGB1555 vrai, chaque
morceau avec sa palette, puis on réindexe. Attention : `palettes.lire` convertit en RGB8
par `v*255//31`, ce qui n'est **pas inversible** ; utiliser `palettes.lire_brut`.

Deux objets de Hugo demandent 78 et 93 couleurs : il faudra les servir en plusieurs
palettes, comme on sert déjà les grilles trop larges en morceaux de colonnes.

Voir `dc-decors/DONNEES-2I.json` (généré par `outils/inventaire.py`) et
[[reference-2i-sens-axe-vertical]].
