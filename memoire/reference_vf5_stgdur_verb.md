---
name: reference_vf5_stgdur_verb
description: "VF5 — un dump Lindbergh de VF5 ver.B existe (Virtua Fighter 5.7z, non inventorié) et il contient stgdur.farc, 35,7 Mo, absent de toutes les versions ultérieures."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-07T16:53:15.243Z
---

`C:\Users\frede\Desktop\VF5 FS DECOMP\Virtua Fighter 5.7z` → `vf5.bin`,
3,77 Go : c'est un dump **Lindbergh de VF5 vanilla ver.B**
(`gameid=SBLM`, build `p73/prj73p/snapshot/overseas_edition/**20070530**`,
chaînes `vf5verB_jng*`). `SOURCES.md` le donnait pour absent sous le nom
`VF5_ARCADE` — **l'inventaire des sources était incomplet, vérifier le dossier
avant de conclure à une absence.**

Il contient **`objset/stgdur.farc`, 35 705 171 octets** — le plus gros objset de
tout le corpus, et **il n'existe dans aucune version ultérieure**. En ver.B il y
a **un seul** décor de Dural, entier, et `du1`…`du4` sont des emplacements vides
(225–486 Ko). En R, `dur` disparaît et les quatre se remplissent ; en Final
Showdown un cinquième s'ajoute. **Le décor de Dural a été découpé en quatre puis
en cinq.**

`decors_vf5r.md` concluait « le décor DUR n'est pas un décor, c'est un jeu
d'effets » : juste pour R et FS, faux en général — la conclusion tenait à ce que
seules deux générations étaient sous la main.

**Why:** c'est le seul contenu réellement absent d'APM3, donc la cible naturelle
du premier import — et il vient avec sa génération complète (`auth_3d`,
collision, `ibl`, `light_param`), ce qui est exactement la condition qui
manquait à l'essai DJO du 2026-09-03.

**How to apply:** tout est extrait et rangé à l'identique dans
`VF5RE/extracted/decors/{VF5_VERB,VF5R,VF5FS_LIND}/`, table dans
`analysis/decors_lindbergh.csv` (`tools/inventaire_decors.py`), document
`analysis/decors_lindbergh.md`. Le conteneur `FArC` ne bouge pas de 2007 à 2011
— mesuré. Voir [[reference_vf5_obj_db]] pour l'accueillir dans le moteur.
