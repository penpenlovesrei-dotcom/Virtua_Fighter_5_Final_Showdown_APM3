---
name: reference-tables-indexees-par-etage
description: "Ajouter un etage a 3SX demande d'etendre une trentaine de tables ; quatre d'entre elles plantent SANS message."
metadata: 
  node_type: memory
  type: reference
  originSessionId: d8d62c33-dc93-4caa-8109-4cbb89f7f7af
  modified: 2026-08-31T21:47:41.343Z
---

Ajouter un etage au port oblige a etendre **une trentaine de tables indexees par l'etage**.
Quatre essais de suite de Frederic ont chacun coute un bug de dimension, et **trois sur
quatre ne disent rien du tout** — ni erreur, ni trace.

| table | fichier | ce qu'elle casse |
|---|---|---|
| `Letter_Data_99[5][N]` | `eff99.c` | plantage du SELECTEUR (indexee par `VS_Stage`) |
| `scr_obj_data[N]` | `eff05.c` | doit etre REMPLIE : `eff05` la deref des que le compte est non nul |
| `ldreq_result[N]` | `gd3rd.c` | **gel muet** apres l'ecran de versus |
| `spans[]`, `ldreq_tbl[]`, `color_file[]` | `gd3rd_data.c`, `color3rd.c` | « duplicate transfer », un etage charge l'archive d'un autre |
| `decor_anim_par_etage` | genere | `signed char` : au-dela de 127 fiches l'index se replie en negatif, les objets DISPARAISSENT sans rien dire |

**Why :** le C complete a zero ce qu'on n'initialise pas, ce qui convient a la plupart des
tables mais pas a celles ou zero a un sens : `bgrw_on` a zero designe l'entree 0 au lieu de
« aucune animation », `limit_tbl3` a zero colle la camera a l'origine, `bg_index_tbl` a zero
renvoie tout le monde sur le fond de Gill.

**How to apply :**

* Faire GENERER les macros par l'outil plutot qu'editer les tables a la main, puis verifier
  apres coup que chacune porte le bon nombre d'entrees. Un decompte faux decale
  silencieusement toutes les tables suivantes.
* Un audit des tableaux dont la taille vaut une borne d'etage (22, 37, 57, 176, 294, 339) a
  ete fait le 31/08/2026 : aucun autre n'est indexe par l'etage. Si un nouveau symptome
  apparait, ce sera par une table dont la taille ne ressemble a aucune borne connue.
* **Tester le code de sortie de la compilation, pas la sortie d'un `grep`** — sinon on
  installe un exe issu d'une compilation ratee, ce qui est arrive deux fois. Voir
  [[feedback-verifier-le-build]].
