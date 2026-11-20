---
name: project-ajouter-decors-3sx
description: "Le but du chantier SF3 DC est d'AJOUTER les décors de 2nd Impact à 3SX, pas de repeindre ceux de 3rd Strike — et un 23e étage fonctionne déjà."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5f3c41f0-2b77-45a7-8d09-bf605c51530c
  modified: 2026-08-27T19:01:19.791Z
---

**Le but est d'ajouter, pas de repeindre.** Frédéric a dû le rappeler après qu'une partie
d'une session soit passée à repeindre le décor de Ken de 3rd Strike avec les pixels de 2nd
Impact via `tex_remix`. Ce travail-là n'est qu'une **preuve** que les pixels et les palettes
de 2I s'affichent correctement dans le moteur ; ce n'est pas le livrable.

**Un 23e étage existe et fonctionne** dans `C:\Temp3sx` (branche `tout-en-un`, 27/08/2026) :
sélectionnable en versus après `RANDOM`, jouable, et Necro — dont il emprunte le fichier de
textures — reste intact. Ce qu'il a fallu :

- une vingtaine de tableaux `[22]` → `[23]`. **Deux familles à ne pas confondre** :
  `bg_w.stage` choisit l'entrée, `bg_w.bg_index` choisit le fond et son script.
- `spans[42]` pour le bloc de chargement (`Push_LDREQ_Queue_BG(étage)` → `spans[étage+20]`)
- un `bg220.c` de deux plans, `ta_move_tbl[23]`, `bg_index_tbl[22] = {22,22,22}`
- une **clé par numéro de page** ajoutée à `tex_remix` : `tex_remix/stage22/<liste>-<page>.tex`,
  via `TexRemix_SetStage()` appelé depuis `bg.c`. C'est ce qui donne des pixels propres à un
  étage qui emprunte le fichier d'un autre.

**Ce qui bloque encore :** la composition. Un plan de 3SX est une grille de 8 × 4 pages de
128×128 dont **seules les rangées 2 et 3 sont visibles** (mesuré deux fois), et rouge/bleu
doivent être **échangés** dans les `.tex`. Mais on ne sait pas comment un atlas `.pvc` de 2I
se compose à l'écran, donc chaque découpe est une devinette — quatre essais, quatre échecs.
La piste à suivre en premier est `bg_map_tbl` / `stageXXX_map[64]`, 64 mots de 2 bits par
case, pas encore décodé.

**Why:** sans ça, on repeint au lieu d'ajouter, et on recompose à l'aveugle.

**How to apply:** tout est dans `dc-decors/RELAIS.md`, qui fait foi. Voir aussi
[[reference-sf3-dc-assemblage]], [[reference-sf3-dc-palettes]] et [[project-sf3-dc-decors]].
