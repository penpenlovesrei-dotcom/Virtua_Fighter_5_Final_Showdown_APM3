---
name: project-fv2-portraits
description: "Portraits de l'écran de sélection de FV2 — textures 3D en VROM non compressée, donc premier patch ROM permanent du projet."
metadata: 
  node_type: memory
  type: project
  originSessionId: da10af44-fc5f-401d-9b3a-2c0a9d501b3b
  modified: 2026-08-15T03:06:45.513Z
---

Objectif ouvert le 2026-08-08 : remplacer les portraits de l'écran de sélection
de Fighting Vipers 2, d'abord par des images fournies par Frédéric, puis en HD
si le premier essai réussit. Méthode retenue : **patch ROM permanent *et* mode
runtime pour itérer**, les deux demandés explicitement.

**Le fait qui change le projet** : les portraits ne sont pas dans la couche 2D
mais dans la **VROM**, qui n'est **pas compressée** — contrairement au
programme en CROM (cf. [[project_fv2_mod]]). C'est donc le premier patch
définitif possible sur disque ; tout le reste du projet était du runtime.

Planche de 256x256 en T1RGB5, 4x3 cases de 64x64 (11 portraits + une case
blanche vide), en **deux exemplaires** : offsets VROM déinterleavés
`0x140A6A8` (claire) et `0x1435150` (sombre, même dessin plus foncé). Vérifié
au bit près contre la texture RAM d'une save state.

Outils livrés dans `fv2mod\` : `tuiles.py` (couche 2D), `textures3d.py`
(texture RAM du Real3D), `vrom.py` (entrelacement / dalles / mipmaps /
T1RGB5), `portraits.py` (`exporter` / `injecter` / `runtime` / `verifier`).
Tout est documenté au **§9 ter du HANDOFF.md**, qui fait foi.

Deux pièges payés dans la séance, à ne pas refaire :
- les texels VROM sont rangés **par dalles de 8x8 permutées** (`decode8x8`), et
  les dalles balaient la planche entière de 256 de large — une recherche
  linéaire ligne par ligne ne trouve que la première dalle ;
- **Supermodel retrouve les fichiers ROM par CRC32, pas par nom** : un romset
  modifié est invisible sans un `Games.xml` dédié dépourvu d'attributs `crc32`,
  passé par `-game-xml-file=`.

**Trois ordres différents cohabitent, ne pas les confondre** (le §5 du HANDOFF
en documentait déjà deux) : l'ordre du curseur, l'ordre des identifiants de
combat, et l'**ordre de la planche de portraits** — donné par Frédéric :
`00 BAHN, 01 CHARLIE, 02 GRACE, 03 HONEY, 04 JANE, 05 MAHLER, 06 PICKY,
07 RAXEL, 08 SANMAN, 09 EMI, 10 TOKIO, 11 vide`, soit les neuf premiers en
ordre alphabétique puis EMI et TOKIO ajoutés à la suite.

Remplacement HD livré le 2026-08-08 : source
`Downloads\Fighting Vipers 2\assets\2a1d1806.png` (illustrations Dreamcast,
4x3 cases de 224x320, encore un autre ordre), découpée par `portraits_hd.py`,
romset produit en `ROMs\fvipers2p.zip` avec `fv2mod\mod\Games.xml`. Cases
sources **hautes** contre texture **carrée** : le mode `ecraser` rend mieux que
le recadrage, parce qu'à 64 px ce sont les casques et coiffures qui identifient
un personnage, pas la taille du visage.

**Vérifié en jeu et validé par Frédéric le 2026-08-08** : le romset patché se
charge et les portraits s'affichent. Piège pratique découvert au passage : le
romset modifié ayant un autre nom de jeu, Supermodel lui donne **sa propre
NVRAM** (`fvipers2p.nv`) — les réglages du TEST MENU faits sur l'original ne
suivent pas.

**Voie retenue depuis le 2026-08-15 : le dossier, pas la ROM.** Frédéric
préfère charger les portraits depuis des PNG plutôt que de les injecter. Le
lanceur `FV2 - Portraits HD.cmd` démarre Supermodel sur le romset **d'origine**
et écrit les planches dans la VROM du process. Les fichiers à éditer sont
`fv2mod\portraits_mod\claire\00.png` à `15.png` ; la planche source est
`Downloads\Fighting Vipers 2\assets\portraits.png` (+ son `.xcf`), redécoupée
par `py portraits_hd.py`.

La planche fait **16 cases**, pas 12 : les cinq dernières sont libres (blanc
uni `0x7FFF`) et reçoivent `11 KUHN, 12 DELSOL, 13 BM, 14 PEPSIMAN,
15 ALEATOIRE`. Placement **choisi, non mesuré** — le §6.2 laisse penser que
l'écran ne dessine rien au-delà de l'indice 10.

Reste ouvert : le **vrai** HD, c'est-à-dire une case au-delà de 64x64, exige un
fork de Supermodel — le matériel fixe la taille de texture. Même réserve que
[[project_3sx_hd_assets]]. Non entamé, ne pas le lancer sans que Frédéric le
demande.
