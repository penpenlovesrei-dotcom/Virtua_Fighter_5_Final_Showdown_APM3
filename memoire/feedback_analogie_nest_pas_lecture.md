---
name: feedback_analogie_nest_pas_lecture
description: "Une analogie entre spawners n'est pas une lecture, et je l'ai présentée à Frédéric comme telle."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-04T16:11:18.233Z
---

Le 04/09/2026, Frédéric a arrêté le chantier après trois corrections ratées d'affilée sur
Yun. Ma faute de fond : **j'ai présenté des inférences comme des lectures du binaire.**

Le cas type : le bloc `0x8C17DD58` (spawner `0x8C028E62`) porte les champs `+456` (script),
`+84`, `+86`, `+556`. J'avais écrit « le binaire dit x 696 » — alors que **la position d'un
WORK est en `+102/+106`, et que ce spawner ne l'écrit jamais**. Que `+84/+86` soit la
position venait d'une analogie avec les spawners voisins. L'écran l'a contredite trois fois
avant que je la remette en cause.

**Why:** Frédéric arbitre sur des images ; si je qualifie de « mesuré » ce qui est déduit,
il ne peut plus faire le tri, et il perd son temps à relancer le jeu pour rien.

**How to apply:** dire « lu » seulement quand un outil a décodé le code (`spawners2i`,
`chargeurs2i`), et « déduit » partout ailleurs — dans les réponses comme dans les
commentaires du générateur. Quand une déduction est contredite à l'écran une fois, la
rouvrir immédiatement au lieu de chercher la cause ailleurs. Voir
[[reference_2i_peint_page_assemblee]], [[feedback_lire_le_code_pas_l_image]] et
[[reference_2i_objet_est_un_work]].

Deux pièges matériels vus le même jour : le `cp` de l'exe **échoue si le jeu est ouvert**
(fichier verrouillé) — le lanceur doit déployer lui-même ; et une recherche du littéral
d'une adresse dans le binaire peut la manquer alors que le spawner la lit bien.
