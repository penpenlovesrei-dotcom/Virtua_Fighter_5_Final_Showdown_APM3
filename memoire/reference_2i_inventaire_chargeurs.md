---
name: reference_2i_inventaire_chargeurs
description: "64 chargeurs de décor atteints par les routines d'étage ; aucun n'écrit la profondeur."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-04T16:27:45.654Z
---

`outils/inventaire_spawners.py` énumère, pour chaque bande, tous les chargeurs que sa
routine d'étage atteint (`jsr`/`jmp`, trois niveaux), et fait décoder chacun par
`spawners2i.analyser` : pas, carte *rang du champ → offset dans l'objet*, bloc résolu par
son argument et par z. `outils/blocs2i.py` en tire directement les objets d'un décor.

**553 fonctions atteintes, pas 97.** Le parcours partageait un même ensemble « déjà vu »
entre toutes les bandes : le premier décor qui atteignait un chargeur partagé se
l'appropriait et tous les autres le perdaient. L'ensemble doit être **local à chaque
bande**. Corrigé le 04/09/2026 ; toute mesure antérieure « sur les 97 fonctions » est à
refaire.

**64 chargeurs lisibles ; `animer2i.TABLES` n'en exploitait que 6.** Les cinq gros sont
partagés : `8C0233B6` (14 décors), `8C02356A` (11), `8C02E1FE` (10), `8C028792` (8),
`8C025A9A` (8).

Deux faits mesurés qui commandent le reste :

* **la profondeur EST dans les blocs** : c'est `+556` (`my_priority`), et elle vaut le
  numéro de palette — voir [[reference_2i_profondeur_palette]]. J'avais écrit ici le
  contraire en cherchant `position_z` à `+76`, offset calculé dans une structure du port
  sans rapport avec l'objet 2I ;
* un chargeur qui n'écrit pas `+102` ne dit **rien** de l'endroit où va son objet. Prendre
  un autre champ qui y ressemble (`+84/+86`) est la faute qui a mal placé le panneau
  vertical de Yun. Voir [[feedback_analogie_nest_pas_lecture]].

Offsets écrits, tous chargeurs confondus : `+102` x et `+106` y (16 chacun), `+88` palette
(13), `+456` script (12), `+554` drapeaux et `+558` plan (10), `+118` (10), `+32` (8),
`+68` (6), et `+150/+152` la paire repos/action (1). Voir
[[reference_2i_paire_repos_action]] et [[reference_2i_objet_est_un_work]].
