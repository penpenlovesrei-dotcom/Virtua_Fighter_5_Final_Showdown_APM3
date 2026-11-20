---
name: reference_decor_plusieurs_bandes
description: "Un décor porte plusieurs bandes (donc plusieurs banques de palettes), mais l'aire ne dit pas laquelle prendre."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-06T11:31:42.552Z
---

2I : bande = u16[0x8C1D591C + decor*6 + aire*2]      trois aires par décor
    NG : d["bandes"], une entrée par aire

Seize décors de 2I rendent trois fois la même bande ; **le décor 8 rend `[8, 9, 9]`** —
c'est le seul. En NG, plusieurs en portent deux : celui de `ng05` a `[5, 6, 6]`.

**L'AIRE N'EST PAS L'INDEX DE LA BANDE.** Prendre `bandes[aire]` corrige le décor NG 3
(`[5, 6, 6]`) et casse le décor 10 (`[18, 17, 17]`) : deux objets propres y repassent à 70
et 116 pixels verts. Les bandes 5 et 17 chargent la **même** base (338), 6 et 18 aussi
(380), et dans les deux décors les objets concernés veulent 380. La liste n'est donc pas
dans l'ordre des aires.

La règle appliquée est celle que le détecteur autorise, **éliminer** : garder `bandes[0]`,
et ne passer à une autre bande **du même décor** que si elle est propre là où la première
ne l'est pas. C'est `bande_de_palette()` dans `animerng.py`.

Ça a résolu les deux derniers objets faux : `n05o9` (la lanterne de ng05) et `a30o0`
(la tache magenta de bg08). Voir [[reference_palettes_trois_tables]],
[[reference_case_vide_est_un_canal]].
