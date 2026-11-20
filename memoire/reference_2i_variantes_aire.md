---
name: reference-2i-variantes-aire
description: "Les décors alternatifs de 2nd Impact — trois seulement (6, 8, 16), mesurés dans le binaire, et le 16 partage les blocs du 6."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7f4afaf5-d8a3-4dd5-9905-114b9a59832e
  modified: 2026-09-01T04:54:29.197Z
---

Les « décors alternatifs » de 2nd Impact, mesurés dans `SF3_2ND.BIN` le 01/09/2026 — deux
tables différentes, à ne pas confondre :

**1. La bande change avec l'aire** — table `0x8C1D591C`, `(décor*3 + aire) -> bande`. Balayée
sur les dix-sept décors : **le décor 8 est le SEUL** (bandes 8 / 9 / 9). Tous les autres sont
constants. C'est déjà posé dans le port — `bg_index_tbl[30] = { 56, 30, 30 }`.

**2. Les ÉLÉMENTS changent avec l'aire** — nombre en `0x8C17B918`, pointeur en `0x8C5F9C04`,
tous deux indexés `décor*3 + aire`. **Trois décors, et trois seulement : 6, 8 et 16.**

    decor  6 (bg06 Hugo)  2 / 3 / 3 elements   @ 8C17BA9E / 8C17BABE / 8C17BAEE
    decor  8 (Elena)      0 / 1 / 1            @ 8C17BB30 / 8C17BB20 / 8C17BB20
    decor 16 (bg10)       2 / 3 / 3            @ LES MEMES QUE LE DECOR 6

Le décor 16 porte **exactement les mêmes trois pointeurs** que le décor 6 : troisième chemin
indépendant qui confirme « bg10 = hugo bis ».

Chez Hugo c'est une **progression**, pas une répétition — les scripts le disent :

    aire 0 : scripts 17, 4
    aire 1 : scripts 20, 22, 4
    aire 2 : scripts 20, 21, 22

Le 17 n'est qu'au premier round, le 21 qu'au dernier, le 4 disparaît à la fin.

**Ce que coûte l'insertion** : les éléments sont cuits dans les pages, donc une variante
demande un ÉTAGE à part (comme bg08/bg09 = étages 56/30). Hugo et bg10 ayant trois variantes
distinctes chacun, il faut **quatre étages de plus** — `VS_STAGE_MAX` 57 → 61, et les ~34
tables indexées par l'étage de 58 à 62. Attention : [[reference-tables-indexees-par-etage]]
dit que trois d'entre elles plantent SANS message.

Voir [[project-ajouter-decors-3sx]] et [[reference-reprise-chantier]].
