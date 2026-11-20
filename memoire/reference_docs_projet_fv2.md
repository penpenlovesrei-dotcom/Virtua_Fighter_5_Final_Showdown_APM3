---
name: reference-docs-projet-fv2
description: "Le projet Model 3 a trois documents de reprise, pas un — vérifier lequel fait foi avant de conclure."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da10af44-fc5f-401d-9b3a-2c0a9d501b3b
  modified: 2026-08-15T03:22:10.606Z
---

Le chantier Model 3 s'est scindé en trois, menés dans des séances séparées, avec
un document de reprise chacun. **Ils se recoupent, et se sont déjà contredits.**

| document | fait foi sur |
|---|---|
| `SEGA Model 3\fv2mod\HANDOFF.md` | rétro-ingénierie du jeu : RAM, adresses, patchs runtime, VROM et textures 3D, portraits |
| `SEGA Model 3\SupermodelSrc\Docs\TuilesHD.md` | fork Supermodel : plan de tuiles HD, dump, packs d'assets, `-tilegen-scale` |
| `SEGA Model 3\SupermodelSrc\Docs\MenuConsole.md` | fork Supermodel : menu dans l'émulateur, modes, sound test, VS DIAGRAM |

**Le point d'entrée est `SEGA Model 3\INDEX.md`**, à la racine du dossier de jeu
(créé le 2026-08-15) : une page qui porte l'aiguillage **et** les invariants —
binaire à lancer, commande de compilation MSYS2, chemins, fermeture propre. Ces
faits n'y sont énoncés qu'une fois et les trois documents y renvoient ; c'est
leur duplication qui avait fait diverger le projet. Ne pas les recopier ailleurs.

Avant de conclure sur un sujet, vérifier quel document en est propriétaire — le
plan de tuiles appartient à `TuilesHD.md`, qui a déjà corrigé le HANDOFF
(`PRESS START BUTTON` est composé de tuiles, pas une image pré-rendue).

Les deux anciens `README` de `fv2mod` (prose de publication du 7 août, périmée
et contenant l'affirmation désormais fausse « aucun patch ROM permanent n'est
possible ») sont archivés dans `fv2mod\archive\`, hors du jeu de documents actif.

Piège concret déjà payé : **le binaire à lancer est
`SupermodelSrc\bin64\supermodel.exe`**, pas le `Supermodel.exe` de la racine qui
date de décembre 2025 et ne connaît ni le menu console ni les tuiles HD. Voir
[[reference_supermodel_binaire]]. Un lanceur écrit sans ça donne un jeu sans
aucune des fonctions du fork, sans erreur visible.

Voisins : [[project_fv2_mod]], [[project_fv2_portraits]],
[[project_fv2_inventaire_2d]], [[project_tuiles_hd]],
[[project_fv2_menu_console]].
