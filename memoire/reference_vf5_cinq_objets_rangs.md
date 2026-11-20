---
name: reference_vf5_cinq_objets_rangs
description: VF5 — les cinq objets d'un décor ne sont pas aux mêmes rangs d'un décor à l'autre ; ceux de djo sont un cas particulier.
metadata:
  type: reference
---

Le descripteur d'un décor demande cinq objets par `(objset << 16) | rang` —
gnd, ring, sky, sdw, reflect, dans cet ordre en `+0x14`..`+0x24`. **Les rangs
changent d'un décor à l'autre** :

    djo  114 118 117 116 115        aur  413 598 414  -1  -1
    ban  817 941 818  -1 942        gym    0 158   1  -1 151
    cas  151 181  -1 153 152        smo    0 308   1  -1  -1

`(114, 118, 117, 116, 115)` est vrai **pour `djo` seul**, le premier décor
ajouté. Écrit en dur pour les dix-neuf, il demandait chez les autres des
morceaux d'effet pris au hasard : plantage, chargement infini ou décor très
incomplet — **les trois symptômes de la même faute** (2026-09-10).

Deux corollaires mesurés :

* **`0xFFFFFFFF` = « pas d'objet » est une valeur normale.** Onze descripteurs
  du jeu en portent ; `aur` n'a ni `sdw` ni `reflect` ;
* **le rang doit exister dans l'archive posée.** `ban`, `jin` et `are` n'ont
  pas de `reflect` dans la géométrie de 2008 — le reflet est une addition de
  Final Showdown. `variantes_5r.ids_archive()` le mesure ; l'emplacement passe
  alors à « pas d'objet ».

**How to apply:** les cinq champs se recopient du MODÈLE, objset substitué et
rang inchangé. Et le contrôle doit les **relire chez le modèle**, pas répéter
la constante du patcheur — voir [[feedback_controle_qui_ment]],
[[reference_vf5_clone_pointe]], [[project_vf5_import_5r]].
