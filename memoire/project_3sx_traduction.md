---
name: project_3sx_traduction
description: "Traduire 3SX — aucune couche multilingue à étendre ; les accents existent pour le texte long, jamais pour les menus."
metadata: 
  node_type: memory
  type: project
  originSessionId: c242bf71-58d0-4715-8a79-c53741fe7284
  modified: 2026-08-25T21:24:46.399Z
---

Objectif de l'utilisateur (2026-08-24) : **ajouter des langues** à 3SX, au-delà de l'anglais et du
japonais que propose le sélecteur amont depuis le commit `11197ed5` (« Language selector », #371).

**Périmètre précisé le 2026-08-25 : les citations de victoire, les dialogues d'avant-combat et les
fins. Pas les menus.**

**La ligne Japanese/English ne change pas ces textes-là.** Vérifié sur `513380f9` : `mpp_w.language`
n'est lu qu'à cinq endroits, tous graphiques ou de sauvegarde — `checkSelObjFileLoaded`
(`ef02_usa.bin` groupe 23 ↔ `ef02.bin` groupe 98), `chkNameAkuma` (eff76), `chkNameSuv` (effk6),
deux bannières d'eff35, et `sys_sub.c`. Les tables `pl_mes_tbl[20]`, `pl_tlk_tbl[20]`,
`pl_end_tbl[20]` sont indexées **par personnage**, toutes en `_usa`, et `message/` ne contient que
`en/`. Citations et fins restent en anglais quelle que soit la position de l'option. Les deux
variantes de `ef02` portent d'ailleurs le même alphabet ASCII, seulement redessiné.

**Les trois textes visés passent tous par `get_message_conn_data`** : `effb8.c:39` (kind 0,
citations), `effa6.c:121` (kind 1, dialogues), `efff9.c:161` (kind 2, fins). Un seul convertisseur,
donc une seule correction pour les trois. `effb6.c:337` est la visionneuse de l'object test.

**Volume** : 58 fichiers, 1 563 lignes, ~50 200 signes (766 lignes de citations, 242 de dialogues,
555 de fins ; Akuma et Q n'ont pas de dialogue). **Contraintes** : 2 lignes par message, 35 glyphes
par ligne (pas de retour automatique, la ligne sort de la boîte) ; et un plafond dur de 108 glyphes
non-espace par message — `CONN conn[108]` puis `while (1) {}` dans `get_message_conn_data`, donc
**un dépassement fige le jeu**. Marge actuelle confortable : le pire message fait 64/108.

Il n'y a pas de mécanisme de locale à étendre : il faut le construire. Vérifié dans le code, pas
déduit :

- `Language` (structs.h) ne connaît que `LANG_ENGLISH` et `LANG_JAPANESE`, et `Language_Toggle` est
  une **bascule binaire**, pas un parcours de liste.
- Un seul dossier de messages, `src/sf33rd/Source/Game/message/en/`, et ses tables sont des
  **singletons** : `msgMenuTbl[] = { &msgMenuTbl_usa }`. Rien n'est indexé par langue —
  `mess_tables[kind][pl]` (effb6.c) est indexé par **personnage**.
- Côté images, `checkSelObjFileLoaded()` (texgroup.c) échange `ef02.bin` contre `ef02_usa.bin`.
- Exceptions codées en dur par personnage : `eff35.c`, `eff76.c` (n° 14), `effk6.c` (n° 20).

**Fichiers à toucher pour une troisième langue** : `structs.h` (enum + toggle devenu cycle),
`main.c`/`main.h` (`Get_Default_Language`), un nouveau `message/<lang>/` calqué sur `en/` (~3 700
lignes : menu, système, extra, plus 20 tables de fin, 20 de dialogue, 20 de victoire),
`message/en/msgtable_en.c` (les singletons deviennent indexés), `effb6.c` (`mess_tables` et les jeux
de caractères `han_adrs`/`zen_adrs`), `texgroup.c`, les trois effets ci-dessus, `menu.c` + `eff64.c`
+ `sel_data.c` pour la ligne de menu, et `savesub.c` pour persister un choix non binaire.

**Inventaire des glyphes fait le 2026-08-25** — il fallait le faire avant d'écrire la couche
multilingue, et il change la donne. Détail et planches : `C:\Temp3sx\docs\traduction_police.md`,
outil `tools/font_inventory.py`, lanceur `inventaire-police.cmd`.

- **Police des messages** (groupe 38, fichier AFS 1458) : les 48 lettres accentuées sont **déjà
  dessinées dans la ROM**, dans `src_han_alpha2` (effb6.c). Jetons de deux octets ASCII, tête =
  accent : `%` tréma, `)` aigu, `(` grave, `^` circonflexe, `~` tilde, `,` cédille, sur
  `A E I O U` (+ minuscules), `N n`, `C c`. Aucun travail d'assets.
- **Deux verrous, tous deux dans le chemin anglais** (`hzSel == 0`, valeur écrite en dur à
  effb6.c:382) : la boucle `for (i = 0; i < 2; i++)` (effb6.c:495) n'explore jamais
  `han_adrs[2]`, et seul `^` ouvre un jeton de deux octets (effb6.c:480). Un jeton introuvable
  devient une espace, sans erreur.
- **Piège** : les textes anglais utilisent déjà ces têtes comme caractères — `(A` 4 fois, `(I` 3,
  `(N` 3, `, ` 189. Ouvrir les accents sans condition transformerait `(ALEX)` en `ÀLEX)`. Le
  paramètre `hzSel`, aujourd'hui inutilisé, est l'accroche pour ne les ouvrir que par langue.
- **Les menus sont un mur, mais ils sont hors périmètre.** `eff61/eff64/eff51/eff63` font
  `chr = base + octet` : l'octet ASCII brut est l'index. 96 glyphes par jeu (bases `0x7047` et
  `0x70A7`), `0x20`–`0x7F`, et le groupe 23 finit à `cg 0x7126`, pile au 96ᵉ du second. Un octet
  ≥ 0x80 ne désigne aucun objet. Seule conséquence ici : le **nom de la langue** dans la ligne
  d'option s'écrit sans accents — `FRANCAIS`, ce qui reste correct en capitales.
- Par langue : italien et portugais complets ; espagnol complet aux `¿ ¡` près ; français manque
  `ÿ œ æ` ; allemand manque `ß`. Les 80 emplacements libres de `src_han_alpha2` existent, mais
  y ajouter une tuile veut dire écrire dans `SF33RD.AFS`.

C'est du code **amont** : une traduction a davantage sa place dans une PR vers `crowded-street/3sx`
que dans notre branche de mod. Voir [[project_3sx_bgm_remix]] pour l'état de cette branche et
[[reference_3sx_amont_decalages]].
