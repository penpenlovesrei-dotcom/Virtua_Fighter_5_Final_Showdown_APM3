---
name: reference-2i-sens-axe-vertical
description: "Le sens de l'axe vertical des décors 3SX, mesuré — et la règle de méthode qu'il a coûtée."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7f4afaf5-d8a3-4dd5-9905-114b9a59832e
  modified: 2026-09-02T04:58:14.822Z
---

**Mesuré le 02/09/2026**, en déplaçant l'acolyte de `bg00` (seul sprite dont la position
soit validée à l'écran, 288/81, et figé sur son image 0) de `y 81` à `y 113`. Frédéric :
**« monté »**. Donc :

    position_y ↑  ->  vers le HAUT
    bank_y     ↑  ->  vers le BAS      (y = 1024 - bank_y - (ligs-1)*16)
    sol        ↑  ->  vers le BAS

**Un sprite trop haut se corrige en AUGMENTANT `sol`.** `sol` vaut 1023 pour les quatorze
décors — c'est la constante du repère, pas une propriété mesurable du dessin.

**La règle de méthode, et elle a coûté trois régressions** (Sean dégradé deux fois, Necro
déplacé alors qu'il n'était pas signalé) : un axe a deux sens, donc une chance sur deux. Il
ne se déduit pas d'un commentaire de code — `njScale(0,1,-1,1)` inverse le y mais
`scr_trans` capture `BgMATRIX` avant, et les deux lectures se défendent. **Il se mesure, et
l'essai prend trente secondes.** Avant de corriger une position, vérifier le sens.

Deux pièges voisins, mesurés le même jour :

* **aucun élément n'est peint dans sa banque** — testé sur les 30 éléments des 14 décors,
  zéro correspondance. Il n'existe donc pas de référence interne pour vérifier une position
  ailleurs que sur `bg00` ;
* « la dernière ligne non vide » n'est **pas** le sol : chez `bg05` ce n'est qu'un bout de
  sprite de 6 px de large, son plan proche étant un premier plan découpé.

Voir [[reference-lire-le-code-pas-l-image]] et le bilan complet dans
`dc-decors/BILAN.md`.
