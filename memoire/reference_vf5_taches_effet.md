---
name: reference_vf5_taches_effet
description: "VF5 — les tâches d'effet d'un décor sont listées au +0x20 de 0x18034D570 ; EFFECT_WALL n'est pas créée d'office."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-10T21:16:41.135Z
---

Une entrée de `0x18034D570` (41 × `0x60`, indexée par le décor) porte **deux**
listes, pas une :

    +0x00   8 identifiants d'objset a charger EN PLUS, fin -1   (toutes vides)
    +0x20  16 indices de TACHES D'EFFET a creer,       fin -1   (PAS vides)

Le `+0x20` est lu par `0x18006F380` ; les noms sont en clair dans
`0x18034E4D0` (0 HIT, 1 AUTH3D, **2 WALL**, 3 LEAF, 5 SNOW, 7 RIPPLE,
9 THUNDER, 16 FOG_ANIM, 17 WET_CLOTH…). Toujours créées (`0x18034D530`) :
HIT, AUTH3D, DOWN, MOVE, PARTICLE, POISON — **WALL n'en est pas**, et 32 décors
sur 41 la demandent.

Le décor ajouté clonait l'entrée 0, qui ne demande rien : `TaskEffectWall`
n'existait pas, sa table indexée par le décor n'était jamais consultée, et les
barrières restaient invisibles. Les flammes marchaient (AUTH3D est toujours là)
et la collision aussi — elle vient du descripteur `+0xB8`/`+0xC0`, posée par
`0x18010CA20`…`0x18010CA60`. « Invisible mais on bute dedans » est la signature
exacte de ce défaut.

Le chantier avait écrit « les 41 entrées sont toutes vides » : mesure faite sur
**4 octets d'un enregistrement de 96**. Une entrée se compare en entier à celle
du modèle, ou pas du tout.

**`setStage` n'est PAS toujours le lecteur.** Le créneau 7 de LEAF, RIPPLE,
WATER_RING et SNOW_RING est un simple setter (il range l'indice en `+0x58`) ;
WET_CLOTH range en `+0x60`. C'est la **mise à jour** (créneau 1) qui va chercher
la table. Chercher la table dans le `setStage` ne pouvait rien donner. Les
vtables se lisent d'un coup : `py -3 tools/rtti.py --grep TaskEffect`.

**Chaque tâche a sa propre forme de données**, et il y en a six : tableau dense
indexé par le décor (DOWN, MOVE — une mine, ni borne ni terminateur), liste à
terminateur (SNOW), chaîne de comparaisons déroulée (BREATH, FOG_ANIM, SPLASH,
THUNDER, LEAF, RIPPLE, SNOW_RING — voir [[reference_vf5_chaine_deroulee]]),
tableau borné par une **adresse de fin littérale** (RINGOUT_SPLASH), **aucune
table** avec un objet nommé par un littéral (WATER_RING), et **bouchonnée**
(ELE_BOARD).

Voir [[reference_vf5_clone_pointe]], [[reference_tables_indexees_par_etage]],
[[project_vf5_import_5r]] ; doc qui fait foi `analysis/decors.md` §17.5, §19
et §20.
