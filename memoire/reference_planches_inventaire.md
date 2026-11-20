---
name: reference-planches-inventaire
description: "Les planches d'inventaire de dc-decors — voir tout d'un coup au lieu d'un décor à la fois, et où sont les sprites manquants."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7f4afaf5-d8a3-4dd5-9905-114b9a59832e
  modified: 2026-09-02T17:30:51.754Z
---

`dc-decors/outils/planches.py` rend **tout ce que le port pose**, dans `dc-decors/planches/` :

    planches.py animes [2i]    les sprites animes, une planche par etage
    planches.py stages [2i]    les plans de chaque etage, cote a cote
    planches.py assets         TOUS les sprites de chaque asset F_ETC, numerotes

Le chantier corrigeait des positions et des couleurs sans jamais regarder l'ensemble : on
voyait un décor à la fois, dans le jeu, après compilation. Ces planches ont trouvé en une
fois le ciel minuscule d'Oro NG et les palettes fausses de Hugo.

**LES SPRITES MANQUANTS SONT DANS L'ASSET — aucune capture nécessaire.** `asset-*.png` les
montre tous avec leurs vraies couleurs et leurs numéros ; il suffit de dire lesquels
manquent à l'écran. L'ampleur : **2322 sprites dans les assets de 2I, 83 posés**. Yang en a
602 pour 2 objets posés.

Trois pièges de l'outil, corrigés et à ne pas réintroduire :

* chercher chaque tableau par regex dans les 17 Mo de `decor_objets_data.c` prend plus de
  dix minutes — **tout indexer en un seul `finditer`** ;
* les noms portent des chiffres (`a22o0_tuiles`) : lire les nombres après eux sans les
  sauter faisait afficher « pal 22 » au lieu de « pal 871 » ;
* les planches de stages rendent les pages que le JEU lit
  (`%APPDATA%/CrowdedStreet/3SX/resources/tex_remix/`), pas celles du dossier de travail —
  les deux ont déjà divergé d'une journée sans qu'on le voie.

**Ce qui ne marche PAS pour retrouver un sprite manquant** : parcourir les tables de blocs
en gardant ceux qui « se résolvent » dans l'asset du décor. Les blocs de Necro, d'Oro et de
Sean se résolvent aussi à 100 % chez Hugo. Seul l'appelant fait foi.

Voir [[reference-2i-palettes-deux-jeux]] et `dc-decors/BILAN.md`.
