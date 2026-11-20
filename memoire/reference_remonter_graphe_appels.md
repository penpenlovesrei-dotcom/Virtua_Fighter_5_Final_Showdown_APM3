---
name: reference-remonter-graphe-appels
description: Pour savoir qui atteint une fonction, remonter le graphe d'appels est exact ; descendre rate des chemins.
metadata:
  type: reference
---

Pour établir qui appelle une fonction dans un binaire, **remonter est exact, descendre ne
l'est pas**. Une fonction n'est atteignable que si son adresse apparaît quelque part : soit
comme littéral chargé par `mov.l @(disp,PC)`, soit **dans une table de pointeurs** (et
c'est alors la table qui est chargée). On part de la cible et on remonte jusqu'à une racine
connue.

Sur SF3 2nd Impact : la descente depuis les scripts d'étage atteignait 4 spawners sur 32,
la remontée en atteint **12** — dont celui des chauves-souris d'Oro, introuvable depuis des
semaines.

**Deux bornages opposés le font échouer en silence :**

* le **prologue est entrelacé** avec d'autres instructions (`mov.l r14,@-r15 ; mov #0,r14 ;
  mov.l r13,@-r15`). S'arrêter au premier intrus rend une adresse *interne* que personne ne
  charge — la remontée conclut alors « aucun chemin ». Prendre le plus ancien empilement
  d'une grappe ;
* le **premier `rts` n'est pas la fin** (voir [[reference-sh4-fin-de-fonction]]).

**Comment l'appliquer :** `outils/remonter2i.py`. Toujours vérifier l'outil sur des cibles
dont la réponse est déjà connue avant de croire un « aucun chemin ». Voir
[[reference-2i-objet-est-un-work]] et [[reference-decors-doc-unique]].
