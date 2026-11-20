---
name: reference_vf5_cablages_numero
description: "FS teste en dur des numéros de décor (16/39 grillage, 0x28 flashs…) et d'uid : un décor ajouté ne les déclenche jamais, il faut les lui rendre."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-11T18:03:20.374Z
---

Grillages invisibles de gm5/yk5 et flashs permanents de so5 venaient de là :
le moteur teste `décor == 16 || 39`, `== 0x28`, `uid == 0x7F4`… Pour les
trouver : appelants de l'accesseur « décor courant » (`0x18018F580` FS, 18 ;
`0x8108718` chez R, 10), plus les `param_2` des setStage et les uid des
tâches (décompiler les méthodes de TOUTES les tâches d'effet). Liste et
remède : `generation.CABLAGES`, `patch_moteur.CABLAGES_APPELS`, REPRISE (66).

Règle : on ne rend un comportement que si LA génération de l'entrée l'a
dans son code (l'immédiat est vérifié : smo = 0x27 chez R, 0x28 chez FS) ;
ce que seul FS teste (plan d'eau riv/jin, particules yuk/hai, public/néons)
reste fermé.

**How to apply:** un effet « qui ne se déclenche pas » ou « qui tourne en
permanence » sur un décor ajouté → chercher d'abord un test câblé sur le
numéro du décor ou de l'uid du modèle. Voir [[reference_vf5_sonde_decor]],
[[reference_vf5_chaque_generation_ses_tables]].
