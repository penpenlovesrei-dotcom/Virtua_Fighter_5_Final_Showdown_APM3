---
name: reference_sf3_dc_pool_tuiles
description: "Le champ « tuile » d'un morceau de SF3 Dreamcast indexe le pool d'un asset F_ETC, désigné par la clé enr+12."
metadata: 
  node_type: memory
  type: reference
  originSessionId: d8349b3e-1653-4777-8c03-2b86bf71ea1e
  modified: 2026-08-28T15:06:23.559Z
---

Dans SF3 Dreamcast, une tuile de sprite **n'a de sens que dans le contexte d'une clé** —
le champ `+12` de l'enregistrement RAM de 16 octets, que `etat2.py` nommait à tort
« palette ». Le vrai champ palette est `+2`.

    bloc  = tuile >> 4   (>> 3 pour la seule clé 0x0160)
    rang  = tuile & 15
    fiche = 0x8C602384 + (clé & 0xFF) * 24      <- table d'installation des assets
    fiche[+8](bloc, tampon, fiche[+12]) -> 4096 octets = 16 tuiles de 16x16 en 8 bits
    la tuile = tampon[rang * 256 : rang * 256 + 256]

`fiche[+12]` pointe la section 3 d'un `F_ETCnn` : `blocs[i]` de `fetc.lire()` est
exactement ce que le jeu dégonfle. Le cache de textures `0x8C0F719E` le confirme, son
identité 32 bits étant `(palette << 22) | ((clé & 127) << 15) | tuile`.

**L'emplacement de palette vient de l'élément, pas toujours du morceau** : bit 5 de
l'octet `+9` de l'élément de la liste d'affichage. Armé → le mot `+8` de l'élément ;
éteint → le champ `+2` du morceau. C'est ce bit qui manquait : sans lui la grande
majorité des éléments tombent sur le bloc de palettes des combattants.

**Taille** : le mot `+8` donne `hauteur = ((w>>8)&127)+1` et `largeur = (w&127)+1` —
l'inverse de ce que nommait `etat2.py`.

Voir `ASSEMBLAGE.md`, `outils/pools.py` (187/187 vérifiés) et `outils/elements.py`.
Lié à [[reference_sf3_dc_fetc]], [[reference_sf3_dc_palettes]],
[[reference_sf3_dc_assemblage]], [[project_ajouter_decors_3sx]].
