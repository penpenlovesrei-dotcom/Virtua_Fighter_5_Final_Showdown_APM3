# Les objets et les DLC : VF5 (2007) ↔ Final Showdown

Chantier mené dans une **autre séance**, le 2026-09-13, depuis
`Desktop\SEPTEMBRE\VF5 CUSTOM DLC`. Replié dans ce projet le 2026-09-27 à la
demande de Frédéric. Rien n'a été refait : ce document reprend son état, et
dit ce qui a bougé en le rapatriant.

## Ce qui a été établi

| source | d'où | contenu |
|---|---|---|
| **DLC de Final Showdown** | le paquet STFS `408E3ECB…5158` | 5 111 objets, 10 222 fichiers |
| **VF5 (2007)** | `Virtua Fight3r 5 AnDreXplay` | 1 606 objets + `_Commun`, 3 213 fichiers |
| **FS, jeu de base** | le paquet XBLA `584111FE\000D0000\7D2DF36B…` | 679 objets + `_Commun`, 1 360 fichiers |

La TU1 ne porte **aucun objet** — seulement `default.xexp` et
`string_array.farc`.

**La comparaison** (`analysis/dlc/Comparaison_VF5_FS_Items.xlsx`, noms anglais
de VF5) : **590 identiques, 891 modifiés, 5 refaits, 37 incertains, 83 absents
du FS**. Les 1 081 modèles de VF5 qui portent un nom en jeu ont **tous** un
équivalent dans Final Showdown ; les 83 absents sont des fichiers sans nom
(27 textures seules, 56 pièces de costume).

## Ce qui restait ouvert

* **Les noms des objets de FS.** `media/rom/chritm_tbl.farc` du FS Xbox est
  compressé en **XMemCompress** (LZX, signature `0x0FF512ED`) et n'est pas lu.
  Les objets de FS n'y sont donc désignés que par leur nom interne.
  *À rapprocher de ce que ce projet sait déjà* : le `chritm_tbl.farc` du dump
  APM3 est **non compressé** et déjà extrait en CSV
  (`extracted/csv_utf8/APM3_FS/chritm_tbl/`, 14 444 objets sur 20
  personnages) — voir `analysis/CHARACTERS.md`. Il y a peut-être là de quoi
  refermer ce point sans toucher au LZX.
* Les **2 249 variantes de couleur** de VF5 : la comparaison se fait par
  modèle, pas une à une.
* Les **37 correspondances « Incertain »** (onglet du classeur), à trancher à
  la main.

## Où sont les choses, maintenant

| | où |
|---|---|
| la chaîne d'outils | `tools/dlc/` |
| les résultats | `analysis/dlc/` — les deux classeurs et `vf5_item_names_en.json` |
| **les données** | `Desktop\VF5 FS DECOMP\X360_VF5_DLC` — voir plus bas |

Deux gigaoctets de paquets Xbox 360 et trois arborescences d'extraction n'ont
rien à faire dans ce dépôt — d'autant qu'il est **public** (voir
`reference_vf5_depot_public`).

**Le 2026-09-27, le ménage.** Le dossier d'origine,
`Desktop\SEPTEMBRE\VF5 CUSTOM DLC` (14 Go), peut partir en entier — vérifié
avant de le dire :

* le **paquet DLC** (2 Go) était le SEUL exemplaire de la machine — il a été
  recopié dans `Desktop\VF5 FS DECOMP\X360_VF5_DLC`, copie contrôlée au
  **SHA-256** sur les 2 075 852 800 octets, pas à la taille ;
* le **jeu de 2007** (4,9 Go) était un doublon exact, à l'octet près sur les
  1 285 fichiers, de `VF5 FS DECOMP\X360_VF5\media` ;
* le **paquet XBLA de FS** (2,05 Go) était un doublon exact de
  `VF5RE\extracted\X360_FS\` ;
* les trois **EXTRACTION** (6,6 Go) et les gros `.json` d'`outils\` (33 Mo) se
  refabriquent par la chaîne ci-dessous.

`tools/dlc/sources.py` cherche chaque source dans **plusieurs emplacements** et
prend le premier qui répond. Éprouvé en rendant `SEPTEMBRE` invisible : les trois
sources sont retrouvées et les archives réellement lues (19 / 21 / 19). Les
dossiers d'extraction suivent la racine retenue, jamais le dépôt.
`VF5_DLC_RACINE` passe devant tout, si les données déménagent encore.

**Un piège au rapatriement.** **`stfs.py` existait déjà** dans `tools/` —
le nôtre, écrit le 2026-09-03 d'après la spécification Free60 pour aller
chercher les `aet_n_*` du menu console. Celui de l'autre séance est
différent : il suit la disposition de Velocity et sait vérifier les
empreintes. Les deux sont gardés — le sous-dossier `tools/dlc/` évite le
choc, et **rien de validé n'est remplacé**.

## La chaîne, dans l'ordre

Tout se lance depuis `tools/dlc/`.

```
extract_raw.py vf5 | fs | dlc          extraction brute + vérification
inventory_games.py  -> games_inventory.json   maillages, empreintes, textures
thumbs_games.py     -> thumbs.json            miniatures 8x8 des textures
item_names.py       -> vf5_item_names_en.json noms des objets de VF5
match_items.py games_inventory.json thumbs.json vf5_item_names_en.json matches.json
make_comparison_xlsx.py matches.json Comparaison_VF5_FS_Items.xlsx
```

Les lecteurs : `stfs.py` (paquets STFS, `--verify`), `vf5fs.py` (archives
FArC, jeux d'objets, textures TXP en DXT1/DXT5/RGB5/RG88), `sources.py` (où
vivent les archives des trois sources). Les anciens, du temps où seul le DLC
était étudié : `farc_list.py`, `inventory.py`, `extract.py`, `make_xlsx.py`.

## Ce que cela donne au mode Quest

Le Quest de 2007 distribue des **objets** et des **emblèmes** : c'est sa
monnaie de progression. La table des noms de VF5,
`analysis/dlc/vf5_item_names_en.json`, est donc la source des libellés que la
boutique et la liste d'emblèmes afficheront — et la comparaison dit, objet par
objet, ce que Final Showdown possède déjà. Voir `analysis/mode_quest.md` §9.
