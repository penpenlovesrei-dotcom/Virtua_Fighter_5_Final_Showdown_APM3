---
name: reference_vf5_etat_fichiers_herite
description: "VF5 — le patcheur repart de .origine, PAS les fichiers : un décor posé par un lanceur restait dans tous les autres. Chaque lanceur pose son état."
metadata:
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-08T22:32:32.689Z
---

**Le défaut, trouvé le 2026-09-08.** `patch_moteur.py` repart toujours de
`vf5fs-pxd-w64-Retail_APM3.dll.origine` : une option retirée de la ligne de
commande disparaît vraiment. **Côté FICHIERS il n'y avait pas d'équivalent.**
`importer_decor.py --poser` modifie l'arborescence libre `vf5fs_media/rom/` et
masque des noms dans l'index du `.par` — et cet état **survit d'un lanceur à
l'autre**.

Conséquence vécue : `decor_5r_akira.cmd` posait le dojo de VF5 R, et tous les
autres lanceurs le voyaient ensuite. Frédéric : « djo est bien version 5R au
lieu de FS !!! ». Et un `--vers trm` laissé en place gardait `trm` masqué dans
le `.par` sans ses fichiers : le décor TERMINAL ne chargeait plus rien.

**La règle.** Chaque lanceur **POSE** son état de fichiers en tête, il ne
l'hérite pas — c'est l'équivalent fichiers du `.origine` :

```
py -3 tools\importer_decor.py --retirer djo >nul 2>&1
py -3 tools\importer_decor.py --retirer trm >nul 2>&1
```

`variantes.cmd` et `variantes_texte.cmd` remettent djo et trm d'origine ;
`decor_5r_akira.cmd` remet trm puis pose djo.

**How to apply:** vérifier l'état sur les OCTETS, pas sur le message de
l'outil — `par_masquer.py --lister` dit « rendue » et le nom peut rester masqué
si un autre lanceur l'a re-masqué entre-temps. Lire l'index du `.par` et lister
`vf5fs_media/rom/`. Voir [[reference_vf5_par_avant_disque]],
[[project_vf5_import_5r]] et [[feedback_ne_pas_defaire_le_valide]].
