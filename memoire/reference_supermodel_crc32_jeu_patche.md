---
name: reference-supermodel-crc32-jeu-patche
description: "Supermodel reconnait les ROM par leur CRC32 : une ROM patchee exige une entree de jeu a part, passee par -game-xml-file."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6a3a967f-1144-49b5-9b3c-9300693489a1
  modified: 2026-08-22T06:39:58.751Z
---

`GameLoader::File::Matches` (Src/GameLoader.cpp) compare les **CRC32**, pas les noms de fichiers : le zip est indexe par CRC (`files_by_crc`). Consequence pour tout patch ROM : des EPROM patchees ne correspondent plus a l'entree du jeu dans `Config/Games.xml`, et le jeu **n'est plus reconnu du tout** — l'erreur parle de fichier introuvable, pas de checksum, ce qui envoie chercher au mauvais endroit.

La sortie propre, sans toucher au `Games.xml` d'origine :

- generer une **definition de ROM a part** (ex. `Config/Games-vf3d.xml`) qui declare un nouveau nom de jeu avec les CRC32 recalcules, et la passer par **`-game-xml-file=Config/Games-vf3d.xml`** (option existante, cf. `Main.cpp`) ;
- le **parent doit etre un jeu racine** : `ParseXML` refuse un parent qui a lui-meme un parent ("More than one level of parents"). Pour un patch de `vf3tb`, le parent est donc `vf3`, et le nouveau noeud doit reprendre les regions propres a `vf3tb` (ici `banked_crom`) ;
- du coup le zip patche doit etre un **jeu complet**, pas un jeu de complement : Supermodel ne va chercher chez le parent que si le zip parent existe (`<parent>.zip` a cote) ;
- ne mettre dans le XML genere **que** le parent et le jeu patche : laisser aussi l'entree d'origine fait afficher "Multiple games found" ;
- le jeu changeant de nom, il a **sa propre NVRAM** (`NVRAM/<nom>.nv`) et ses propres sauvegardes d'etat. Recopier une fois celle d'origine evite de reperdre les reglages.

Etabli le 2026-08-22 en gravant le premier patch ROM permanent de [[project_vf3_model3]] (`graver.py`). Vaudra tel quel pour [[project_fv2_mod]] le jour ou son gzip sera regravable. Binaire concerne : celui de [[reference_supermodel_binaire]].
