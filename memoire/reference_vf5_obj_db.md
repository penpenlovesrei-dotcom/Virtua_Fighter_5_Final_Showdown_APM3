---
name: reference_vf5_obj_db
description: "VF5 — l'identifiant d'objset d'un décor vient de rom/objset/obj_db.bin, pas du code ; l'espace est troué et non borné, donc ajouter un décor est possible."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-07T16:26:34.144Z
---

Le descripteur d'un décor porte en `+0x10` un **identifiant d'objset**. On
pouvait le croire câblé : il ne l'est pas. `0x1800F9450` le cherche par
**dichotomie** dans un vecteur construit au démarrage par `0x18006B7E0`, à
partir de `"./rom/objset/" + "obj_db.bin"` (`0x1800F9803`, `0x1800F981A`).

`rom/objset/obj_db.bin` : en-tête 0x20 o, pot commun de chaînes, puis une table
de **0x24 octets par jeu d'objets** —
`{offset du nom, IDENTIFIANT, obj.bin, tex.bin, .farc}`.

La preuve que l'espace est libre : les 43 entrées `STG*` recoupent le
descripteur du moteur une par une, **y compris celles qui cassent la suite** —
`STGDU5 = 5529`, `STGGYM = 2847`, `STGSMO = 2848`, et l'identifiant 29 n'est
attribué à personne. L'identifiant **n'est pas la position** dans la table.
Ces trois décors ont été ajoutés après coup exactement comme on voudrait le
faire.

Cinq bases sœurs suivent la même logique : `tex_db`, `spr_db`, `aet_db`,
`auth_3d_db`, `mot_db`.

**Why:** j'allais annoncer « ajouter un décor demande de recompiler le moteur ».
C'est faux, et il a suffi de suivre l'identifiant au lieu de le supposer.

**How to apply:** la recette complète est dans
`VF5RE/analysis/ajouter_un_decor.md`. Voie courte : recycler l'un des 17
emplacements d'essai (`tst ts2 ts3 wht trm cid trs evo00..evo09`) — aucune
borne à lever. Les onze tables indexées par le décor sont **toutes bornées**,
contrairement au piège de [[reference_tables_indexees_par_etage]].
Voir [[reference_vf5_index_decor_game_score]].
