---
name: reference_vf5_objset_lecture
description: "VF5 — un objset se LIT (tools/objset.py) : un décor n'a qu'un objet de ciel, et le champ +0x14 du descripteur est (objset << 16) | id d'objet."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-07T21:32:04.493Z
---

Balayer l'ASCII d'un `*_obj.bin` rend du bruit : 19 298 faux « noms » sur
`stgdur_obj.bin`. Deux identifications de décor s'y sont perdues.

**`tools/objset.py`** lit la table. En-tête de 0x40 octets, petit-boutiste :

    +0x00 magie 0x05062500   +0x04 NOMBRE d'objets   +0x08 plus grand id
    +0x0C table des objets   +0x14 TABLE DES NOMS    +0x18 table des ids
    +0x1C ids de texture     +0x20 nombre de textures

`+0x14` et `+0x18` ont chacun `nombre` entrées de 4 octets, dans le même ordre :
nom et identifiant se lisent en parallèle.

**Un décor de VF5 a trois à cinq objets réels**, le reste étant des effets
numérotés : `gnd`, `ring`, `sky`, parfois `sdw` et `reflect`. **Un seul objet de
ciel.** Toute théorie de « série de ciels » ou de cycle jour/nuit tombe.

**Le champ `+0x14`…`+0x34` du descripteur `0x180403430` est décodé** : mot haut
= identifiant d'objset, mot bas = identifiant d'objet **dans cet objset**.
Ordre des cases : `gnd`, `ring`, `sky`, `sdw`, `reflect`, —, puis trois objets
de l'objset 0 (effets communs) pour sept décors. Vérifié sur les 41.

    du1  objset 30    30:1  30:382  30:0
    djo  objset 28    28:114 28:118 28:117 28:116 28:115

**`tools/textures_decor.py`** fait la planche contact des textures d'un décor
(`--min`, `--planche`, `--dossier`) : quand les noms ne disent rien, l'image
tranche. Voir [[feedback_soumettre_les_images]].

**How to apply:** avant d'identifier un décor, lire ses objets avec
`objset.py`, puis regarder ses textures. Ne jamais conclure d'une couleur
d'éclairage ni d'un mot-clé trouvé au balayage.
