---
name: project-fv2-inventaire-2d
description: "Inventaire des éléments 2D de FV2 — seules les textures VROM sont patchables en ROM, le reste vient du flux compressé."
metadata: 
  node_type: memory
  type: project
  originSessionId: da10af44-fc5f-401d-9b3a-2c0a9d501b3b
  modified: 2026-08-08T12:32:59.000Z
---

Inventaire mené le 2026-08-08 à la demande de Frédéric, pour pouvoir remplacer
les graphismes 2D en SD ou HD plus tard. Outil : `fv2mod\inventaire.py`.
Détail au **§9 bis du HANDOFF.md**, qui fait foi.

**Le résultat central, mesuré et contre-intuitif** : sur Fighting Vipers 2,
presque rien n'est en clair dans la ROM. Trois familles :

- **textures Real3D présentes en VROM** — portraits, chiffres, logo :
  **patchables définitivement** (VROM non compressée, cf.
  [[project_fv2_portraits]]) ;
- **plan de tuiles** (fonds, bannières, logos de noms, texte du HUD) : les
  motifs sont introuvables en clair — zéro occurrence sur 20 motifs témoins,
  cherchés en banked_crom, VROM, CROM et RAM, dans trois ordres d'octets ;
- **la majorité des textures 3D** : idem — 2 dalles sur 50 seulement retrouvées
  en VROM pour la scène DAM, et rien en polygon RAM, file de textures, RAM ni
  banked_crom.

Tout ce qui n'est pas en VROM vient donc du flux compressé en CROM, et n'est
modifiable qu'en runtime. Deux fausses pistes déjà écartées, ne pas les
reprendre : le cache VROM a été vérifié **au bit près** contre une construction
indépendante, et l'hypothèse « textures 8 bits » tombe (5,5 % de la planche).

**Atlas d'interface trouvé** : quatre textures 256x256 qui se suivent en VROM,
espacées de `0x2AAA8` — `0x0140A6A8` portraits clairs, `0x01435150` portraits
sombres, `0x0145FBF8` chiffres 0-9, `0x0148A6A0` logo FIGHTING VIPERS 2.

**La reconnaissance automatique dégrossit seulement** (10-17 % de la planche).
Le sens fiable est l'inverse et suffit en pratique :
`py inventaire.py <state> --localiser X,Y` rend l'offset VROM d'une image
repérée sur la planche de textures.

Couverture actuelle limitée aux save states existantes — scènes `SELECT`,
`HANGAR`, `DAM`. Elle s'étend en capturant d'autres save states (F5).
