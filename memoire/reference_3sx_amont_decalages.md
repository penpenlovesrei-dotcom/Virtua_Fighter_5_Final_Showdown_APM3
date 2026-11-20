---
name: reference_3sx_amont_decalages
description: "L'amont de 3SX remanie sans cesse les menus — chaque remontée décale nos index de tables parallèles."
metadata: 
  node_type: memory
  type: reference
  originSessionId: c242bf71-58d0-4715-8a79-c53741fe7284
  modified: 2026-08-25T16:49:57.645Z
---

Le mod 3SX vit dans des **tables parallèles indexées par position** — `Menu_Letter_Data` (eff61.c),
`Slide_Pos_Data_61` et `Slide_Pos_Data_64` (sel_data.c), `Letter_Data_64` (eff64.c), `AT_Jmp_Tbl` et
`Convert_Buff` (menu.c). L'amont touche ces menus à presque chaque version, donc **une remontée est
un portage, jamais une fusion**, et rien de ce qui casse ne se voit à la compilation.

Décalages déjà payés, vérifiés sur la donnée :

- `251f025` → `a5284f22` : ligne **Sound Mode** retirée et `Sound_Data_Max` passé de `[3][6]` à
  `[3][5]` (donc `SOUND_ITEM_BGM_TYPE` 3 → 2) ; `Auto_Save` et `SoundMode` sortis de la sauvegarde
  (tous les `Convert_Buff[3][1][N]` reculent de un) ; écrans Save/Load Direction retirés (nos écrans
  21-24 → 19-22) ; une entrée de moins dans `Menu_Letter_Data` (`DISPLAY_LABEL_FIRST`,
  `BACKGROUND_STAGE_FIRST`, `CUSTOM_THEME_FIRST` reculent de un).
- `a5284f22` → `513380f9` : le **sélecteur de langue** prend l'index 18 de `Slide_Pos_Data_64`, où
  nos colonnes de valeurs commençaient (les quatre `*_VALUE_POS_FIRST` avancent de +1) ; et
  `Get_ramcnt_address` est renommé `Get_ramcnt_pointer`.

**Parades adoptées** : les tables dont aucun en-tête n'impose la taille sont dimensionnées par leur
contenu — `Menu_Letter_Data[]`, `Slide_Pos_Data_61[][2]`, `AT_Jmp_Tbl[]` — et l'ouverture de la page
Display passe par la table `option_routines` de l'amont plutôt qu'un calcul d'offset.

**Piège de rebasage** : `core.autocrlf = true` sur ce dépôt alors que les blobs sont en **LF**. Des
commits faits en CRLF font conflicter des fichiers entiers. Vérifier par
`git cat-file blob <rev>:<fichier> | head -c 24 | xxd` avant de conclure à un conflit de contenu, et
rebaser avec `git -c core.autocrlf=false`.

Voir [[project_3sx_bgm_remix]] et [[feedback_verifier_le_build]].
