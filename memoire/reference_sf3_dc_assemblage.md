---
name: reference-sf3-dc-assemblage
description: "Le morceau de sprite de 8 octets des F_ETCnn de SF3 Dreamcast — taille dans le quartet de code, x et y au centre, tuiles en colonnes."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5f3c41f0-2b77-45a7-8d09-bf605c51530c
  modified: 2026-08-27T15:58:34.619Z
---

Le morceau de 8 octets de la section 2 d'un asset `F_ETCnn` se lit :

    u16 index de tuile   (bloc = index >> 4, rang dans le bloc = index & 15)
    u16 palette          (bits 0-8 offset, bits 9/11/12 drapeaux — voir [[reference-sf3-dc-palettes]])
    u16 y                (12 bits)
    u16 code << 12 | x   (x signé sur 12 bits)

**Le quartet `code` porte la taille en tuiles :**

    largeur = 1 << (((code >> 2) & 3) - 1)      hauteur = 1 << ((code & 3) - 1)

Seules neuf valeurs existent — `5,6,7,9,a,b,d,e,f` — les 3×3 combinaisons de 1, 2 et 4.
Le même calcul est dans le code SH-4, à l'offset 10 de l'enregistrement RAM de 16 octets
que dessine `0x8C0F693C` : `0x8C0F6B06` et `0x8C0F6B20`, avec `r9 = 3`.

**`x` et `y` sont des centres, pas des coins :** `coin = (x - 8*largeur, y - 8*hauteur)`.
C'est le piège qui a fait échouer les tentatives précédentes.

**Les tuiles d'un morceau se suivent en colonnes** (la hauteur d'abord), comme le CPS3.

**Trois mesures le prouvent, aucune interprétable de travers :**
- l'écart entre l'index d'un morceau et celui du suivant vaut `largeur × hauteur`,
  code par code, sur les 7313 sprites des deux jeux ;
- le chevauchement des rectangles de morceaux tombe à **2,35 %** avec cette convention,
  contre 15 à 23 % pour les trois autres combinaisons (largeur/hauteur inversées,
  coin au lieu du centre) ;
- l'acolyte de Gill (`F_ETC41`, sprites 9 et 10, palette 871) sort **identique** à la
  capture Flycast `reference-gill-acolyte.png`.

**Why:** deux sessions avaient buté là-dessus en essayant des dispositions ; c'est le
désassemblage de la boucle de dessin `0x8C0F693C` qui a donné la réponse, comme les
trois fois précédentes sur ce chantier.

**How to apply:** `dc-decors/outils/assemblage.py`, lanceurs `rendre-sprites.cmd` et
`sprite.cmd`, doc `dc-decors/ASSEMBLAGE.md`. Voir aussi [[reference-sf3-dc-fetc]] et
[[project-sf3-dc-decors]].
