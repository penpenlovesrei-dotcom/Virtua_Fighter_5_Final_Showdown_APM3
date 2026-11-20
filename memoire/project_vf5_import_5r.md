---
name: project_vf5_import_5r
description: "VF5 — le dojo d'Akira de VF5 R est AJOUTÉ et COMPLET à l'écran (indice 42) : géométrie, flammes et barrières, validé le 2026-09-10."
metadata: 
  node_type: memory
  type: project
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-10T12:00:46.658Z
---

## L'ACQUIS, VALIDÉ À L'ÉCRAN LE 2026-09-10

Le dojo d'Akira de **VF5 R** est le premier décor **vraiment ajouté** au jeu :
indice **42**, code `d5r`, objset **6150**. Aucun emplacement du jeu n'est
recyclé, `djo` reste intact. Géométrie, **flammes** et **barrières de ring**
(4 poteaux + 24 panneaux, carré 12×12) sont vues à l'écran.

Lanceur : `tools\dojo_5r_repli.cmd` → MENU → DOJO.

Les trois builds qui existent, et ils ne se marchent pas dessus :

| lanceur | ce qu'il fait |
|---|---|
| `tools\dojo_5r_repli.cmd` | **AJOUTE** l'indice 42 — le build du chantier |
| `tools\decor_5r_akira.cmd` | **REMPLACE** `djo` par la géométrie de 2008 (témoin) |
| `tools\dojo_5r_temoin.cmd` | le même build avec le dojo d'origine |

## LES TROIS CAUSES QU'IL A FALLU LEVER POUR LE MUR

Elles se sont présentées l'une après l'autre, toutes silencieuses :

1. l'index des noms d'objets est **global et trié** — un doublon rendait
   l'objset du modèle ; il faut renommer `STGDJO_` → `STGD5R_` dans `obj_db`,
   `auth_3d_db` et les `.a3da` ;
2. l'entrée de `TaskEffectWall` **ne porte que des pointeurs** : les 28
   morceaux sont dans les blocs qu'ils désignent, et ils nomment les objets par
   `(objset << 16) | rang` — voir [[reference_vf5_clone_pointe]] ;
3. **`EFFECT_WALL` n'était jamais créée** : les tâches d'effet d'un décor sont
   au `+0x20` de `0x18034D570` — voir [[reference_vf5_taches_effet]].

Le symptôme qui a tout donné, et c'est Frédéric qui l'a fourni : *« invisible,
mais la collision est bien gérée »*. La collision vient du descripteur
`+0xB8`/`+0xC0`, pas de la tâche.

## LES DIX-NEUF DÉCORS, POSÉS ET PATCHÉS (2026-09-10) — PAS ENCORE VUS

`tools\decors_5r.cmd` ajoute les **dix-neuf décors complets** de VF5 R aux
indices **42 à 60**, objsets 6150..6168. La table du lot est dans
`tools/variantes_5r.py`, et **elle ne vit qu'là** : `decor_neuf.py --poser-lot
5r` pose, `patch_moteur.py --decors-5r --variantes-5r` patche,
`controle_decors_5r.py` vérifie. Accès : **la barre espace** fait passer une
case de grille de Final Showdown à VF5 R (dix-neuf anneaux).

Trois règles que le lot a imposées :

* **un lot n'est pas N fois un** : les fichiers se posent un par un, les bases
  (`obj_db`, `auth_3d_db`) une seule fois — sinon chaque décor efface les
  autres, en silence ;
* **chaque décor clone SON modèle**, pas `djo`, dans les cinq tables où il
  apparaît ;
* **un modèle sans mur n'en donne pas** (`riv`, `smo`) — lui en fabriquer une
  entrée ferait pointer le clone sur le mur de `djo`.

`du1`..`du4` restent à faire : VF5 R range la scène des quatre décors de Dural
sous un seul nom, `STGDUR.farc`. `du5` n'existe pas dans VF5 R.

VF5 R n'apporte **aucun décor nouveau** — il a les mêmes que l'APM3, moins
`du5`. Ce qu'il apporte, ce sont des versions **plus riches** des mêmes lieux
(`djo` +8,1 Mo, `sin` +8,1, `smo` +7,3, `nyc` +6,9, `du3` +4,3).

**How to apply:** ne rien réinventer — la recette complète est
`analysis/decors.md` §16-17 et le journal `REPRISE.md` (46) (47) (48). Un décor
ajouté clone **son propre modèle** (le décor FS correspondant), pas `djo` :
descripteur, entrée de mur, liste de tâches d'effet. Voir
[[feedback_ajouter_jamais_remplacer]], [[feedback_ne_pas_defaire_le_valide]],
[[reference_vf5_obj_db]].
