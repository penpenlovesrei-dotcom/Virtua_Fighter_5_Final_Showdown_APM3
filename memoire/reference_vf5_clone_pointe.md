---
name: reference_vf5_clone_pointe
description: "VF5 — cloner une entrée de table indexée par le décor ne clone pas ce qu'elle pointe ; le mur nomme ses objets par (objset << 16) | rang."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-10T11:14:07.260Z
---

Une table indexée par le décor a **deux** façons de mentir : ne pas avoir
d'entrée pour l'indice ajouté, ou en avoir une **qui désigne les données du
modèle**. Un clone n'est un clone que si ce qu'il pointe l'est aussi.

Le cas payé le 2026-09-10, à l'écran : le décor ajouté (indice 42) s'affichait
avec ses flammes et **sans les barrières du ring**.

* `TaskEffectAuth3D` (`0x18034FD20`) porte un pointeur vers une **liste de
  numéros d'uid**, et rien d'autre — la remplir avec nos numéros suffisait ;
* `TaskEffectWall` (`0x180355C30`) ne porte **que des pointeurs**. Tout le mur
  est dans les trois blocs qu'ils désignent, et ils nomment leurs objets par
  `(objset << 16) | rang` : 28 morceaux (4 poteaux aux coins ±6, 24 panneaux),
  la liste d'uid, la paire `{intact, cassé, uid, uid}`. Objset **28**, uid
  **1194** — ceux de `djo`, qui n'est pas chargé dans un build d'ajout. Rien à
  l'écran, aucun message.

Le patcheur recopie désormais les trois blocs dans `.decors` en substituant
objset et uid, et `controle_decor_neuf.py` §6 le relit dans la DLL patchée.
Contrôle négatif gratuit : `--indice 43`, un clone non corrigé laissé exprès
dans le build, rend 36 fautes.

Voir [[reference_vf5_obj_db]], [[reference_tables_indexees_par_etage]],
[[project_vf5_import_5r]] ; doc qui fait foi `analysis/decors.md` §17.4.
