---
name: reference_xbox360_outils
description: "Lire un dump Xbox 360 — le dépôt emoose/xbox-reversing, ce qui y sert, et la limite (pas de XEX compressé)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 22b68e08-364a-4b50-b67a-c1f1efec0229
  modified: 2026-09-03T16:50:12.736Z
---

Lien donné par Frédéric le 2026-09-03, pour ouvrir le dump X360 de VF5 FS :

**https://github.com/emoose/xbox-reversing** (BSD-3-Clause)
Le README renvoie à **`idaxec`**, du même auteur, pour la version native du
chargeur XEX.

Ce qui sert :

- **`templates/xbox-360/XEX2.bt`** et ses quatre compagnons (`XEX2Headers.bt`,
  `XEX2OptionalHeaders.bt`, `XEX2FlagsAndEnums.bt`, `XEX2Functions.bt`) — la
  **spécification complète du format XEX2**, en gabarits 010 Editor, lisibles
  comme du texte. C'est la documentation qu'il faut pour écrire un lecteur.
- **`templates/xbox-360/Xbox360Container.bt`** — la disposition STFS.
- **`stfschk/`** — vérificateur de hachages STFS ; du code qui parcourt
  réellement un paquet, dont les tables de hachage à sauter (tous les 0xAA blocs).
- **`xbox360.py`** + **`x360_imports.py`** — chargeur XEX pour IDA, en Python :
  en-têtes, sections, imports, directement lisible comme source.

**MESURÉ le 2026-09-03, et c'est le mauvais cas** : l'en-tête de notre
`default.xex` (`FILE_FORMAT_INFO` à `0xD7A000 + 0x1B70`) donne **chiffrement 1
(AES) et compression 2 (LZX, fenêtre 0x8000)**, image de 16,8 Mo, ImageBase
`0x82000000`. Or `xbox360.py` ne gère que les XEX **non compressés**. Le dépôt
donne donc la spécification, pas le décodeur : il faudrait écrire un LZX complet.

La piste X360 n'est donc pas un détour mais un chantier à part entière — à ne
rouvrir que si la voie APM3 se ferme.

État de notre dump : paquet STFS `LIVE` de 2,05 Go, **blocs de données en
clair** — on lit `default.xex`, `XEX2` (0xD7A000), `stgdjo.farc`, `mothead_DUR`
directement dedans. Mais `UNLOCK_DURAL` et `ARCADE MENU` n'y sont pas : ils sont
dans l'exécutable.

Rappel : la 360 est du **PowerPC gros-boutiste**, pas plus proche du PC que la
PS3. Aucun code ne se transporte ; ce qu'on irait y chercher, c'est la logique
lue comme une donnée. Détail dans `docs/formats/xbox360_outils.md`.
