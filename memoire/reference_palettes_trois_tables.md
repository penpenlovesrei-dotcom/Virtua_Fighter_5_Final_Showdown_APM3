---
name: reference_palettes_trois_tables
description: "Les index de transfert de palettes de 2I et NG sont dans TROIS tables lues par le chargeur d'étage, pas passés en dur."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-06T11:31:16.225Z
---

Le chargeur d'étage (2I `0x8C0DA450`, NG `0x8C03ABC6`) lit la bande puis indexe **trois
tables d'affilée**, une par transfert :

| | 2nd Impact | New Generation | index |
|---|---|---|---|
| second jeu, dst `0x12000` | `0x8C1D5D14` | `0x8C18ABE4` | `bande*2` |
| premier jeu, dst `0x2000` | `0x8C1D5D38` | `0x8C18AC10` | `bande*2` |
| **secondaire** | **`0x8C1D5D66`** | **`0x8C18AC46`** | **`(bande-1)*2`** |

La troisième est indexée par `bande - 1` : la bande 0 n'en a pas et le code saute sa
lecture. Elle rend les neuf valeurs qu'on avait relevées à la main dans les scripts
d'étage (l'ancien `EN_DUR`), **les neuf exactes**, et sept bandes de plus.

**Ne jamais calculer un index : le lire.** `transfert(52 + bande)` marche pour les bandes
0 à 16 et casse ensuite — NG en a dix-neuf, et `52 + 17` tombe sur l'entrée 69, le second
jeu de la bande 0. Ça donnait à la bande 17 la base 25 au lieu de 338, et 64 476 pixels
verts fantômes.

Voir [[reference_2i_palettes_deux_jeux]], [[reference_decors_doc_unique]].
