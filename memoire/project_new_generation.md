---
name: project-new-generation
description: Les dix-neuf decors de New Generation sont montes dans 3SX aux etages 37 a 55 ; leurs bandes sont nommees dans le binaire.
metadata: 
  node_type: memory
  type: project
  originSessionId: d8d62c33-dc93-4caa-8109-4cbb89f7f7af
  modified: 2026-08-31T21:47:22.609Z
---

**New Generation est monte dans le port** (31/08/2026) : dix-neuf bandes aux **etages 37 a
55**, plus `bg08` et `bg10` de 2nd Impact aux etages **56 et 57**, jamais montes jusque-la.
Le port compte donc **58 etages** et `VS_STAGE_MAX = 57`.

**Les bandes sont NOMMEES dans le binaire**, table `0x8C1B7E98` : `H.S.(GILL)`,
`N.Y.(ALEX)`, `N.Y.(SEAN)`, `JAPAN(RYU)`, `JAPAN(KEN)`, `H.K.(YUN1/2)`, `LOND(DUD1/2)`,
`MOSC(NECR)`, `MUN (HUGO)`, `JAP(IBUK1/2/3)`, `NAI(ELEN1/2)`, `AMAZO(ORO)`, `H.K (YAN1/2)`,
`SELECT`. Trouvees APRES tout le reste, elles recoupent tout — Ryu et Ken partagent le stage
du Japon, Yun et Yang celui de Hong Kong.

**Why :** ces noms confirment les observations de Frederic sur les correspondances entre les
deux jeux, et ils expliquent pourquoi certains decors emettaient la meme sequence de blocs.
La bande 19 s'appelle `SELECT` : c'est l'ecran de selection, d'ou un vingtieme `.pvc` sans
script d'etage.

**How to apply :** l'etat complet et le prompt de reprise sont dans
`dc-decors/REPRISE.md` ; les structures de NG dans `dc-decors/NEW-GENERATION.md`. La chaine
d'outils a un ORDRE : `animer2i.py --ecrire` refait `decor_objets_data.c` en entier, puis
`animerng.py --ecrire` y ajoute New Generation. Voir [[reference-tables-indexees-par-etage]]
avant de toucher a un etage ajoute.
