---
name: reference-2i-paire-repos-action
description: Un enregistrement de décor 2nd Impact porte deux scripts — repos et action — et on posait le repos.
metadata:
  type: reference
---

Les blocs du chargeur `0x8C028792` (id 18) de SF3 2nd Impact portent **deux** numéros de
script par enregistrement : `objet+150` (octet 12) et `objet+152` (octet 14). Le second vaut
toujours le premier plus un, et c'est une paire **(repos, action)** que la routine alterne.

Le repos peut avoir **zéro image** : chez Yun, 32 → 0 image et 33 → 12 images. Poser le
premier donnait des figures immobiles — « les 2 personnages devant le tram et les oiseaux
dans la cage ne sont pas animés ».

Notre moteur ne joue qu'un script : on pose **le plus riche des deux** (`sc2` dans
`animer2i.TABLES`).

**Pourquoi :** un champ non lu peut ressembler à un champ absent. Quand une figure sort
figée, vérifier d'abord si son enregistrement ne porte pas un second script.

**Comment l'appliquer :** `outils/planche_scripts.py` rend tous les scripts d'un décor en
une planche, ce qui permet d'identifier ce que l'utilisateur décrit ("le vieil homme au
panier") sans lui demander de captures supplémentaires. Voir
[[reference-decors-doc-unique]].
