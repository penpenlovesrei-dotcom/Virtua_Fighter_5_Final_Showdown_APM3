---
name: reference_vf5_verb_textures_rangs
description: "VF5 ver.B ne numérote ni ses textures ni ses objets comme FS (VF5 R, si) : 3 277 collisions de texture ; il faut renuméroter NOTRE archive."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-11T05:38:04.364Z
---

Mesuré le 2026-09-11 contre la `tex_db` de FS :

    objsets de VF5 R poses : tout identifiant connu de FS = texture du meme decor
    objsets de ver.B       : 3 277 / 3 975 identifiants = AUTRE CHOSE chez FS

Les identifiants de texture d'un `*_obj.bin` sont en DEUX endroits seulement :
la liste de l'en-tête (`+0x1C` offset, `+0x20` nombre) et, dans chaque matériau
(0x4B0), les huit emplacements `+0x14 + t*0x78 + 4`. Objet : `+0x20` nombre de
matériaux, `+0x24` leur offset (relatif à l'objet). Vérifié : aucun emplacement
non vide ne sort de la liste. `variantes_vf5.ecrire_objset` renumérote par NOM
(nom connu de FS → numéro de FS ; sinon trou libre hors VF5 R), recomprime le
seul `_obj.bin` (gzip avec FNAME, comme SEGA) et recopie le `_tex.bin`.

Les RANGS d'objets diffèrent aussi (`STGDJO_GND` 114 chez FS, 0 chez ver.B) :
les cinq objets du descripteur se relisent dans le descripteur de ver.B
(ELF `0x852F220`, 28 × 0x70 ; GND +0x10, SKY +0x14, SDW +0x18, REFLECT +0x20),
contrôlés par nom.

Les `+0x2C..+0x34` du descripteur FS sont des TEXTURES (reflets d'objectif,
`F_VF5E_JIN00_IK_LENSFLARE_0`…), pas des uid.

Voir [[project_vf5_import_verb]], [[reference_vf5_chaque_generation_ses_tables]].
