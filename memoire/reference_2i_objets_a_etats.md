---
name: reference_2i_objets_a_etats
description: "Un objet 2I enchaîne plusieurs scripts ; casse, débris et regards sont détectables dans le code."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-04T17:39:35.726Z
---

Notre `DecorAnimation` joue **un** script en boucle ; le jeu en enchaîne plusieurs par
objet. `outils/etats2i.py` lit ces machines à états : dans la routine que l'`id` désigne
dans `0x8C179FDC`, il relève les appels au poseur `0x8C0B4AD4` (`r6` = le script) et les
écritures en `objet+36` (`routine_no`, qu'aucun spawner n'écrit — tout objet naît en 0).

**14 routines sur 196 posent plusieurs scripts.** Chez Yun : la charrette (0, 1, 2), les
cages (7, 12, 34), le **fumeur (23, 24)** dont on ne pose qu'un.

**Les objets qui se brisent au contact** ont un second spawner. Celui des cages,
`0x8C02942E`, lit le bloc `0x8C17DDA8` : trois enregistrements — cage qui roule, cage
écrasée, barreaux — avec `+134 = 0x8000` et `+136 = 0xFFFF`, qui ont tout d'une vitesse.
Les oiseaux qu'on cherchait s'échappent à la casse : ids 82 (script 42) et 97 (44, 45), et
aucune routine d'étage ne les atteint. **Il n'y a pas d'oiseau dans la cage intacte.**

**Les regards qui suivent les combattants** se détectent à une lecture de `0x8C69D314` ou
`0x8C69D32E` — deux champs distants de 26 octets, les deux joueurs. **80 routines sur 196**
les lisent ; contre-épreuve, les deux routines des acolytes de Gill (ids 11 et 184) en font
partie, elles dont on savait déjà que les images sont des orientations.

Porter tout ça est un chantier de MOTEUR, pas d'extraction, et **ce n'est pas la priorité**.
Voir [[reference_2i_profondeur_palette]] et [[reference_2i_inventaire_chargeurs]].
