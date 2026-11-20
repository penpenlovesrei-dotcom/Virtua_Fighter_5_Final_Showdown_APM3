---
name: reference-tables-indexees-par-personnage
description: "Ajouter un 21e personnage a 3SX : les tables a etendre ne se relevent pas en cherchant `[20] = {` - les pires sont les tableaux de pointeurs de fonction."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1b6a7297-36d0-4db2-9df6-56a319b1221c
  modified: 2026-09-01T21:08:14.075Z
---

Meme motif que [[reference-tables-indexees-par-etage]], mais pour le personnage.
Un premier relevé qui cherche `nom[20] ... = {` en rate **trois familles**, et la
premiere fait tomber le jeu :

1. **Les tableaux de pointeurs de fonction** — `void (*Char_Jmp_Tbl[20])(PLW*) = {`.
   La dimension n'est pas suivie d'un `=`. A l'indice 20 on lit un pointeur qui ne veut
   rien dire, et le jeu tombe **des qu'on l'appelle** (`0xC0000005`). Concernes :
   `Char_Jmp_Tbl`, `Follow_Jmp_Tbl`, `Passive_Jmp_Tbl`, `VS_Shell_Jmp_Tbl` (com_pl.c),
   les huit `Passive_*_tbl` (ck_pass.c), `end_main_jp` (end_main.c).
2. **Les dimensions ecrites en hexadecimal** — `Correct_VS_Air_Data[0x14]`.
3. **Celles ou le personnage est la DEUXIEME dimension** — `Shell_Dodge_Data[4][20]`,
   `homing_hos[2][20][2]`, `exdm_ix_data`, `paring_mark_data`, `ahj_empos_hos`...
4. **Celles dont la taille n'est PAS ECRITE** — `void (*const plxx_extra_attack_table[])()`
   dans `plpat.c`. Le compilateur la deduit de l'initialiseur : **aucun `20` n'apparait
   dans le source**, donc aucune recherche de `[20]` ne peut les voir. Celle-la fait
   tomber le jeu au premier coup porte. Aussi `normal_05` et `normal_06` (plpnm.c).

**Le seul balayage qui tient** ne cherche aucune dimension : il prend toutes les
definitions de tableau, **compte les elements de l'initialiseur**, et ne garde que les
symboles indexes quelque part par un numero de personnage.

**Et il faut exclure les dossiers PAR COMPOSANT DE CHEMIN, pas par sous-chaine.**
Exclure `"stb"` en sous-chaine ecarte aussi `src/bin2obj/as`**`stb`**`l.c` — le fichier
qui porte les treize tables de scripts d'attaque indexees par le personnage
(`_assadr_lv_9900`, `_asstbl_lv_*`). Trois balayages de suite l'ont manque a cause de ca,
et c'etait le plantage suivant : `wk->as` recupere une entree hors bornes, puis
`wk->as->char_ix` tombe.

Et `master_player`, dans les effets, **est un numero de personnage**, pas un numero de
joueur.

**Why :** les huit `Passive_*_tbl` sont indexes par le personnage de la **cible** : c'est
l'adversaire gere par la machine qui lit le numero du joueur humain. Le plantage arrive
donc au debut du combat, pas a la selection - loin de sa cause.

**How to apply :** le bon balayage croise **tous** les sites d'indexation par
`My_char` / `player_number` / `character_id` / `master_player` avec la dimension declaree
**du bon rang**, quelle que soit l'ecriture. Outil : `etendre_tables.py` dans
`Downloads\3sx-outils\shin-akuma\` (il refuse tout tableau ne comptant pas exactement 20
elements et recompte apres coup). Voir [[project-shin-akuma-build]].
