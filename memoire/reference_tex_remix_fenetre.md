---
name: reference-tex-remix-fenetre
description: "La substitution de pages de tex_remix reste ouverte tant que current_stage n'est pas remis à -1 — nos pages débordent alors dans les menus."
metadata: 
  node_type: memory
  type: reference
  originSessionId: a42b6c0d-1a36-40d8-b5ab-289a8f4629c0
  modified: 2026-08-29T22:02:27.922Z
---

Résolu le 29/08/2026, après une soirée à chercher au mauvais endroit.

`TexRemix_Substitute` remplace une page dès que **deux** conditions sont réunies :
`current_stage >= 22` **et** le couple `(from->first, from->index)` correspond à un de nos
`stage<N>/<liste>-<page>.tex`. Il n'y a **aucune** autre borne — ni sur l'écran en cours,
ni sur le moment.

Or `TexRemix_SetStage(bg_w.stage)` n'était appelé qu'une fois, au chargement de l'étage
(`bg.c`), et jamais annulé. `current_stage` restait donc à 22 pour tout le reste de la
partie : les menus d'après-combat chargent leurs propres pages, et **toutes celles dont
les numéros coïncidaient recevaient les nôtres**. Symptôme : le ciel étoilé de Gill
traversant l'écran de sélection et l'écran WINNER.

**Correction :** `TexRemix_SetStage(-1)` à la fin du chargement de l'étage. Nos pages n'ont
besoin d'être substituées que là.

**La leçon, pour New Generation et la suite :** une substitution par NUMÉRO de page n'est
pas bornée par le contexte. Toute fenêtre de ce genre s'ouvre et se referme
explicitement, et le test qui le prouve est « jouer, sortir, regarder l'écran suivant ».

Voir [[feedback-pas-de-donneur]] et [[project-ajouter-decors-3sx]].
