---
name: reference_vf5r_binaire_lisible
description: Le programme de VF5 R est dans l'atelier (LIND_R/vf5r.bin) et ses tables se retrouvent par leurs valeurs — c'est le comparateur qui manquait.
metadata:
  type: reference
---

`extracted/LIND_R/vf5r.bin` (2,4 Go, image Lindbergh, plusieurs copies) porte
**les tables du moteur de VF5 R**. Pas de symboles, mais on n'en a pas besoin :
on cherche le MOTIF FLOTTANT d'un enregistrement connu de Final Showdown
(`struct.pack('<fff', ...)`) et on lit l'enregistrement autour.

C'est le comparateur qui manquait au chantier des decors : il repond a
« est-ce que 2008 faisait pareil ? » sans capture d'ecran et sans supposition.
Exemple, decor d'Eileen (slk 15) : RIPPLE en 0x4915C6CC, SPLASH en 0x4915C798,
liste des taches en 0x48FEF4A0 -- **identiques a Final Showdown, octet pour
octet**, identifiants de particule compris.

**La numerotation des taches d'effet DIFFERE** : R en a 19, FS 23. FS a insere
`EFFECT_MOVE` en 11 (donc decalage de 1 au-dela) puis ajoute `PARTICLE`,
`POISON`, `ELE_BOARD`. Traduire un indice avant de comparer.

    R : 0 HIT 1 AUTH3D 2 WALL 3 LEAF 4 WATA 5 SNOW 6 YUKA 7 RIPPLE 8 RAIN
        9 THUNDER 10 DOWN 11 RINGOUT_SPLASH 12 WATER_RING 13 SPLASH
        14 SNOW_RING 15 FOG_ANIM 16 WET_CLOTH 17 FOG_RING 18 BREATH

`extracted/LIND_VF5/vf5.bin` existe aussi (VF5 d'origine), meme methode.

Voir [[reference_vf5_taches_effet]], [[project_vf5_import_5r]].
