---
name: reference-2i-annuaire-elements
description: "L'annuaire qui dit quel bloc d'éléments de décor appartient à quel décor de 2nd Impact — la deuxième d'une série de dix tables après 0x8C5F9B38."
metadata: 
  node_type: memory
  type: reference
  originSessionId: a42b6c0d-1a36-40d8-b5ab-289a8f4629c0
  modified: 2026-08-29T19:59:19.293Z
---

Résolu le 29/08/2026. C'était « le seul verrou » du chantier des décors 2I, et il était
dans la suite immédiate d'une table déjà connue.

`0x8C5F9B38` n'est pas une table isolée : c'est la **première d'une série de dix tables
de 51 entrées** (17 décors × 3 aires), posées bout à bout, la série s'arrêtant à
`0x8C5FA330`.

    0x8C5F9B38 + 0*204   les scripts d'animation      -> 0x8C12xxxx
    0x8C5F9B38 + 1*204   LES ELEMENTS DE DECOR        -> 0x8C17Bxxx
    0x8C5F9B38 + 2*204   un second jeu d'elements

Le pointeur d'un décor vaut **deux octets avant** son premier enregistrement ; le bloc va
jusqu'au pointeur distinct suivant : `nb = (suivant - annuaire[aire]) / 16`.

**L'épreuve qui discrimine** — celle qui manquait quand le span seul ne suffisait pas :
le numéro de script s'entend dans la table de scripts **de ce décor-là**, pas dans celle
du décor 0. L'index global obtenu doit tomber dans le `index_global` de l'asset F_ETC du
**même** décor. Trente éléments sur trente, décors 0 à 12.

Conséquence : `bg00` a **trois** éléments statiques, pas cinq. Les deux « étoiles
filantes » sont le bloc du décor 1, résolues par erreur avec la table du décor 0.

Outil : `outils/annuaire2i.py`. Voir [[reference-2i-chaine-sans-etat]] et
[[project-ajouter-decors-3sx]].
