---
name: reference_vf5_grille_agrandir
description: "VF5 — la grille de sélection des décors s'agrandit : place contiguë jusqu'à 43 cases, et une case SANS ancre se place toute seule."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-07T22:03:42.008Z
---

Deux faits mesurés le 2026-09-07 qui font passer de « détourner une case » à
« en ajouter une ».

**La place est contiguë.** Les deux tables de cases se suivent, et la liste
d'exclusion ne commence qu'après :

    0x180400210   grille hors ligne    21 cases x 0x20
    0x1804004B0   grille bornes liees  22 cases x 0x20
    0x180400770   liste d'exclusion

soit **0x560 = 43 cases**. La table des bornes liées n'est lue que si
`[0x180C3B6F0]+0x1FE10` est non nul ; en console il est nul, la branche hors
ligne tourne (`0x180174B6D`), et la capture d'écran le confirme (3 × 7).

**Une case n'a PAS besoin d'ancre.** `0x180173BD0` retient la dernière case
ancrée (`+0x60` colonne, `+0x64` ligne), calcule deux gradients (`xmm11` par
colonne, `xmm10` par ligne) et **extrapole** toute case dont `+0x18` est nul.
C'est l'exact inverse de l'erreur qui avait empilé les cases : repointer
`+0x18` sur une ancre **déjà utilisée** donne à deux cases la même position
(voir [[reference_vf5_case_grille_ancrage]]).

Case, 0x20 octets : `+0x00` colonne, `+0x04` ligne, `+0x08` index du décor,
`+0x0C` 0x14C, `+0x10` 0x14B, `+0x14` 0, `+0x18` `char*` ancre.

**Quatre compteurs**, et quatre seulement :

    0x1801746D2  mov r8d, 0x15    le compte donne au constructeur
    0x18017493C  cmp rbx, 0x15    la boucle qui cherche la case ALEA
    0x180174BBE  cmp rax, 0x15    la boucle index de decor -> case
    0x180174AA0  cmp rsi, 0x2A0   la borne du tirage au sort (en OCTETS)

Les autres `0x15` du voisinage sont des identifiants de calques AET
(`0x18017481B`, `0x180174FBC`, `0x180175056`, `0x180175129`) ou l'index du
décor `du1` (`0x180174E13`) : les toucher n'a rien à voir avec le compte.

**L'aperçu, lui, est du CODE.** La liste n'est pas une table : elle est
construite instruction par instruction sur la pile vers `0x180174BF0`
(`mov [rbp+0xD0], 0x14 ; lea rax, "tan" ; …`, 0x18 octets par entrée). Une case
neuve n'a donc pas d'aperçu tant qu'on n'écrit pas de code dans une caverne.

**How to apply:** `patch_moteur.py --grille-ajout` (option ajoutée le
2026-09-08, lanceur `tools/decors_ajoutes.cmd`) porte la grille à 25 cases avec
du2..du5 sur une 4e ligne. Incompatible avec `--decors-dural-grille`, qui
détourne les mêmes décors sur quatre cases existantes.
