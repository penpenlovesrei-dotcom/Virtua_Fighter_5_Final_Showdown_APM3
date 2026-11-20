---
name: feedback_observation_puis_code
description: "Une capture Dreamcast ou une observation de Frédéric est le point de départ d'une recherche dans le code, jamais un réglage."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-04T16:27:23.970Z
---

**Toute capture de la version Dreamcast et toute observation que Frédéric donne doivent
ensuite être CHERCHÉES DANS LE CODE.** Si la donnée n'y est pas encore, il faut refaire une
analyse du code — pas combler le trou par un réglage.

Ce qu'il ne veut plus voir : une table de correction remplie à l'œil (`Z_OBJET`, `EXCLUS`)
pour faire coller l'image. Une observation dit *qu'il y a* un défaut et *où* le chercher ;
elle ne dit jamais la valeur à écrire.

**Why:** un réglage à l'œil fige une valeur que personne ne peut vérifier ni généraliser,
et il empêche l'automatisation complète de l'extraction, qui est le but du chantier. Il l'a
formulé après trois régressions d'affilée sur Yun, toutes issues de tables écrites à la
main.

**How to apply:**
* partir de l'observation → identifier l'objet concerné → remonter à son chargeur
  (`inventaire_spawners.py`, `blocs2i.py`, `chargeurs2i`, `spawners2i`) → lire le champ ;
* si le code ne porte pas l'information, le DIRE et chercher d'où elle vient, au lieu
  d'inventer une valeur. Exemple mesuré : **aucun des 97 chargeurs n'écrit `+76`
  (`position_z`)** — la profondeur n'est donc pas dans les blocs, et ce qui départage deux
  objets, c'est l'ORDRE DE CRÉATION, lui aussi dans le code (ordre des `jsr` de la routine
  d'étage, puis ordre des enregistrements) ;
* un élément peint dans le décor est TOUJOURS derrière ; si l'original le montre devant un
  personnage, c'est l'objet qui l'y met — le retirer est le contraire du correctif.

Voir [[feedback_analogie_nest_pas_lecture]], [[feedback_lire_le_code_pas_l_image]] et
[[reference_2i_peint_page_assemblee]].
