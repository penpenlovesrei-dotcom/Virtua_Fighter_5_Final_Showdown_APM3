---
name: reference-2i-drapeaux-miroirs
description: "Le champ « drapeaux » d'un morceau SF3 est le bit de miroir, pas une banque de palettes ; et l'index 0 fausse toute mesure de couleur."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-03T08:07:44.776Z
---

Dans le champ palette d'un morceau de sprite SF3 (`drapeaux << 9 | offset`), `drapeaux` ne
prend que quatre valeurs sur les quatorze assets de 2nd Impact — 1, 5, 9, 13 — et leurs
bits sont exactement ceux que `assemblage.morceaux` lit comme retournements : aucun,
vertical, horizontal, les deux. **Ce n'est pas un sélecteur de banque de palettes.**

La vraie séparation de banques est l'**offset** : le groupe bas tire sur le transfert
secondaire (passé en dur par le script d'étage, destination contiguë au premier jeu), le
groupe haut sur le premier jeu.

Et une mesure de couleur qui inclut **l'index 0** ne mesure rien : il est transparent et
n'est jamais peint. C'est en le comptant qu'on a cru voir « 850 cases vertes » chez Hugo
et rejeté la bonne base.

**Pourquoi :** deux lectures contradictoires du même champ coexistaient dans l'outillage
depuis des semaines, et la fausse envoyait 512 morceaux retournés chercher leurs couleurs
dans une palette lointaine — c'est le « vert fluo sur les vêtements » de Hugo.

**Comment l'appliquer :** `outils/banques2i.py` refait les trois épreuves (destination
contiguë, détecteur de vert index 0 exclu, nombre de palettes). Voir
[[reference-2i-palettes-deux-jeux]] et [[reference-decors-doc-unique]].
