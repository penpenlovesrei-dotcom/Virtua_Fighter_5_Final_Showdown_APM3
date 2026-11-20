---
name: project-shin-akuma
description: "Shin Akuma n'est pas a extraire de 2I : il est entier dans la ROM d'arcade de 3rd Strike, 21e personnage, et le port l'a retire."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1b6a7297-36d0-4db2-9df6-56a319b1221c
  modified: 2026-09-01T16:25:21.814Z
---

Trouve le 01/09/2026, en partant de « Shin Akuma existe dans 2I, extrais-le ».

**Il n'y a rien a aller chercher dans 2nd Impact.** Shin Gouki est **entier dans la ROM
d'arcade de 3rd Strike**, entre Akuma et Chun-Li, en personnage 15 d'un roster de 21.
C'est le portage console qui l'a retire : `constants.h` garde `CHAR_SHIN_AKUMA = 15` sous
`#if CPS3`, et `charid.c` **recycle son slot charset 17** pour le personnage bonus.

Deux tables independantes le designent : le tableau maitre `0x18B1B4` (23 lignes de 0x6C =
24 pointeurs + `CharInitData2`, dans l'ordre des `plid_data`, qui saute 17) et la table
`prot` `0x5FBF40` (21 entrees, dans l'ordre des numeros de personnage, indice 15).

**Why :** ca change entierement le chantier — rallumer ce que 3S contient deja au lieu de
reconstruire un personnage de 2I dans un autre moteur. Et il **partage les sprites
d'Akuma** : 581 des 606 `cg` de ses scripts sont ceux d'Akuma, il n'en manque que 25.

**How to apply :** tout est dans `C:\Users\frede\Downloads\3sx-outils\shin-akuma\` —
`RAPPORT.md` (la demonstration et ce qui reste), `shin.py` (qui **s'auto-verifie** en
redonnant 496/500 des couples que le port connait deja), les 25 sections extraites.
La carte est complete, l'integration ne l'est pas. Voir
[[reference-coherence-nest-pas-role]] : ici le role est prouve par deux mesures
independantes, pas par une regularite.
