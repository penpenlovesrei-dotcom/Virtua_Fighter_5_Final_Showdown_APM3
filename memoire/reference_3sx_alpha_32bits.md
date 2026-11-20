---
name: reference_3sx_alpha_32bits
description: "3SX halvait l'alpha des textures 32 bits (convention PS2 0-128) — tout remplacement HD sortait à moitié transparent."
metadata: 
  node_type: memory
  type: reference
  originSessionId: c242bf71-58d0-4715-8a79-c53741fe7284
  modified: 2026-08-13T20:47:48.261Z
---

`flPS2ConvertContext` ([flps2vram.c](C:/Temp3sx/src/sf33rd/AcrSDK/ps2/flps2vram.c), ~ligne 1115)
convertissait l'alpha des textures **32 bits** dans les deux sens : `0xFF → 0x80` à l'entrée du pool,
`0x80 → 0xFF` à la sortie. C'est la convention du GS PS2, où l'alpha d'une texture va de 0 à **128**.

Le port rend par un shader qui lit l'alpha sur 0-255 (`direct.frag`, `_28.zyxw * vColor`), donc
**0x80 valait 50 % d'opacité** : tout remplacement 32 bits — portraits `art_remix` comme pages
`tex_remix` — sortait fusionné avec le fond. Supprimé dans les deux sens le 2026-08-13.

Sans risque : le jeu **n'a aucune texture 32 bits**, le dump d'un démarrage complet ne contient que
du 4 bpp, du 8 bpp et une seule page 16 bpp.

**Ce qui l'a démasqué** : dessiner le même quad **deux fois**. Toutes les lectures de code disaient
« opaque » (alpha du sommet à 255, fusion `SRC_ALPHA` standard, shader sans facteur) ; la seconde
passe a densifié l'image, ce qui prouvait une fusion sans rien avoir à interpréter. À réutiliser
quand le code affirme une opacité que l'écran dément.

Le shader attend le **BGRA** et remet l'ordre lui-même (`.zyxw`), d'où l'échange d'octets dans
`art_remix.c`.

Voir [[project_3sx_hd_assets]].
