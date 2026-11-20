---
name: reference_vf5_case_grille_ancrage
description: "VF5 — le champ +0x18 d'une case de grille n'est pas son icône mais son ancrage de position ; le repointer empile les cases et casse le curseur."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-07T18:39:09.503Z
---

Une case de la grille de sélection de décor (`0x180400210`, 0x20 octets) porte
en `+0x18` un nom de sprite du genre `stage_icon_riv_c`. **Ce n'est pas l'icône
à dessiner : c'est l'ANCRAGE qui donne à la case sa position à l'écran.**

Le constructeur `0x180173BD0` le lit ainsi (`rsi = table + 4`, donc
`[rsi+0x14]` = case+0x18) :

    cmp  qword [rsi+0x14], 0            ; pas d'ancre -> position INTERPOLEE
    call 0x1800298B0(buf, [rsi+0x14])   ; resout le sprite par son NOM
    vmovsd xmm0, [rax+0x40]             ; -> x, y REELS du sprite
    vmovsd [r14+rdi+8], xmm0            ; la position de la case

Le 2026-09-07 j'ai fait pointer quatre cases sur le même sprite pour « changer
leur icône ». Elles ont reçu **les mêmes x et y** : cinq cases empilées au même
endroit. Frédéric, à l'écran : *« les icônes sont toujours les mêmes, seul DU1
est sélectionnable, le curseur saute toutes les autres, et DU1 est remplacé par
DU4 ou 5 »* — trois symptômes, une seule ligne fautive.

L'icône réellement dessinée est **peinte par la scène AET `SEL_STAGE`**. La
changer demande de toucher `spr_db`, `aet_db` et la planche du `.par`.

Les champs sûrs : `+0x00` colonne, `+0x04` ligne, `+0x08` **indice de décor** —
c'est le seul que le constructeur ne lit pas, donc le seul qu'on peut changer
sans rien déplacer.

**Why:** j'ai patché sans avoir lu `0x180173BD0`, en déduisant le rôle du champ
de son contenu. Un nom de ressource ne dit pas le rôle du champ ; seul son
consommateur le dit — voir [[reference_coherence_nest_pas_role]] et
[[feedback_lire_le_code_pas_l_image]].

**How to apply:** avant de repointer un champ, lire la fonction qui le
consomme. Et quand un correctif est retiré, le faire **refuser** par
`patch_moteur.py` plutôt que l'ignorer : les vieux lanceurs le portent encore.
Voir [[project_vf5_decors_dural]].
