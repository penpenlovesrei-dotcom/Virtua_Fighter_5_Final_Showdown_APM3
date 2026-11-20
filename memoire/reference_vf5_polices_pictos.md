---
name: reference_vf5_polices_pictos
description: "VF5 a DEUX systèmes de texte ; la planche brute se mesure par autocorrélation, l'indice de fontmap est empaqueté, et les boutons Xbox sont déjà dans le jeu."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 61cff823-927b-4eea-81b1-5063c9d15cce
  modified: 2026-09-07T04:50:09.693Z
---

Deux systèmes de texte à ne pas confondre. `fontmap.bin` **ne décrit pas**
`font_gothic.bin` : il donne l'indice 33 pour `A`, alors que `font_gothic` porte
`A` en case 65, c'est-à-dire à son codepoint.

**`font_gothic.bin`** : police bitmap brute, 8 bits par pixel, sans en-tête.
Sa disposition ne se devine pas — trois essais à la vue ont échoué. Elle se
mesure par autocorrélation sur les octets (`tools/mesurer_atlas.py`) : pic net
à 32, avec ses multiples derrière. Les cases sont **bout à bout**, il n'y a
aucune rangée 2D — d'où l'échec de tout rendu « en largeur de ligne ». Et elle
est en **deux zones** : 256 cases 16×32 (512 o) jusqu'à l'octet `0x20000`, puis
des cases 32×32 (1024 o). Une seule taille de case donne un début lisible puis
de la bouillie.

**`fontmap.bin` (FMH3)** décrit les planches sprite `spr_n_fnt32`. Son indice de
glyphe est **empaqueté** : `(rangée << 8) | colonne`, pas linéaire.

**Les boutons** : la planche embarque déjà le jeu **Xbox 360 complet** (B A Y X,
START, BACK, LB/LT/RB/RT, LS/RS) à côté du jeu PlayStation, en `U+E000`–`E032`,
rangées 56-57. Passer à des boutons Xbox One / PS4 / PS5 est donc du repeignage
de cases 32×32, pas un système à écrire. Le schéma de manette DualShock 3 est à
part : `spr_n_cmnps3`, 512×512 **RGBA non compressée**.

Le document qui fait foi : `analysis/polices_et_pictos.md`.
Voir [[reference_reprise_vf5]] et [[feedback_lire_le_code_pas_l_image]].
