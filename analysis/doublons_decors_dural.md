# Les décors de Dural : y a-t-il des doublons ?

Mesure du 2026-11-19. Question de Frédéric : « pour les décors de Dural, il
semble y avoir des doublons, peux-tu le vérifier ? Propose-moi les décors à
supprimer. »

**Réponse courte, et elle n'est pas celle qu'on attendait : parmi les treize
décors de Dural du jeu, il n'y a AUCUN doublon aux octets.** Les treize ont
des empreintes SHA-256 distinctes, des codes distincts, des indices distincts,
et chacun n'apparaît qu'une fois dans l'anneau de la case `dur`.

Les doublons sont ailleurs, et ils sont gros : **deux arborescences entières de
décors recopiées sur le disque**, dont 280 Mo pour le seul Dural. Et une copie
libre est **corrompue d'un bit**.

Aucun jeu n'a été lancé. Rien n'a été supprimé : tout ce qui suit est une
proposition.

---

## 1. Ce qui a été mesuré, et par quel chemin

| mesure | chemin |
|---|---|
| empreintes des fichiers posés | SHA-256 sur `VF5RE/runtime/media/vf5fs/vf5fs_media/rom/` |
| empreintes des décors de Final Showdown | extraction SLLZ du `vf5fs_data.par` (`tools/sllz.py`) |
| contenu interne des archives | membres `FArC` décomprimés, empreinte de chaque membre (`tools/farc.py`) |
| table des 86 descripteurs | section `.decors` de la **DLL patchée**, pas `.origine` |
| table des codes à trois lettres | `.decors + 0x50A0` = `0x180EB60A0`, 86 pointeurs |
| grille de l'écran STAGE SELECT | `0x180400210`, 21 cases de 0x20, relue dans les deux DLL |
| anneaux de la barre espace | `.greffe` : `VAR_COMPTES` `+0x780`, `VAR_IDX` `+0x7D0`, `VAR_TEXTES` `+0xCD0` |
| conformité des entrées ajoutées | `tools/controle_decors_vf5.py` et `… r` (lecture seule) |
| scripts | `rom/game_score.txt` |

Les deux contrôles existants passent : « RIEN A REDIRE » sur les 21 entrées de
ver.B et sur les 23 de VF5 R. L'état posé est sain ; la question des doublons
est donc bien une question de rangement, pas de conformité.

---

## 2. La liste complète : treize décors de Dural dans le jeu

Les cinq de Final Showdown vivent **dans le `.par`** (indices 21-25, ils ne
sont pas des fichiers libres). Les huit autres sont **posés en fichiers** par
`decor_neuf.py`.

| idx | code | nom interne | objset | provenance | fichier de géométrie | taille | SHA-256 (préfixe) |
|---|---|---|---|---|---|---|---|
| 21 | `du1` | `STGDU1` | 30 | **VF5FS / APM3** (`.par`) | `stgdu1.farc` | 27 229 016 | `280dd81af86a6ec1` |
| 22 | `du2` | `STGDU2` | 31 | **VF5FS / APM3** (`.par`) | `stgdu2.farc` | 24 144 242 | `a5c11e703aa67937` |
| 23 | `du3` | `STGDU3` | 32 | **VF5FS / APM3** (`.par`) | `stgdu3.farc` | 27 894 787 | `7af62afc4e856d9e` |
| 24 | `du4` | `STGDU4` | 33 | **VF5FS / APM3** (`.par`) | `stgdu4.farc` | 26 188 937 | `52235964c6d22f58` |
| 25 | `du5` | `STGDU5` | 5529 | **VF5FS / APM3** (`.par`) | `stgdu5.farc` | 24 771 735 | `3b228300b70c4a82` |
| 78 | `drb` | `STGDRB` | 6186 | **VF5 ver.B** (Lindbergh 2007) | `stgdrb.farc` | 35 685 626 | `829537fa327180ae` |
| 79 | `d2b` | `STGD2B` | 6186 *(partagé)* | **VF5 ver.B** | — ciel `stgd2b.farc` | 225 351 | `0531b90be68f99ca` |
| 80 | `d3b` | `STGD3B` | 6186 *(partagé)* | **VF5 ver.B** | — ciel `stgd3b.farc` | 484 278 | `f40eb10a34fee3dc` |
| 81 | `d4b` | `STGD4B` | 6186 *(partagé)* | **VF5 ver.B** | — ciel `stgd4b.farc` | 486 977 | `eff0037c3a42349a` |
| 82 | `d15` | `STGD15` | 6191 | **VF5 R** (2008) | `stgd15.farc` | 27 365 558 | `44083ba107a53fe9` |
| 83 | `d25` | `STGD25` | 6192 | **VF5 R** | `stgd25.farc` | 26 639 120 | `048f050a3daf9a58` |
| 84 | `d35` | `STGD35` | 6193 | **VF5 R** | `stgd35.farc` | 32 408 169 | `ba0c300cfb12548f` |
| 85 | `d45` | `STGD45` | 6194 | **VF5 R** | `stgd45.farc` | 26 830 812 | `3726c0962e6c37e2` |

Le ciel de `drb` est un dixième objset à lui, `stgd1b.farc` (485 427 o,
`3d9e0b9e4e3fee29`), déclaré sous l'objset 6187 — il n'a ni code ni indice,
donc ni `.ibl` ni `light_param` à son nom : c'est `drb` qui porte l'éclairage.

**Les quatre entrées de ver.B partagent une seule géométrie.** C'est voulu, et
ce n'est pas un doublon : ver.B n'avait qu'**un** décor de Dural (`stgdur`,
35,7 Mo) sous quatre ciels. Descripteur `+0x10` = 6186 pour 78, 79, 80 et 81 ;
même catégorie d'effets `EFFSTGDRB` ; même collision `STGDRB_COLI.000.bin`.
Seuls changent le ciel (objsets 6187-6190) et l'éclairage.

### Poids, décor par décor (les huit posés)

| code | géométrie + ciel | `.ibl` | `light_param` | collision | `auth_3d` | **total** |
|---|---|---|---|---|---|---|
| `d15` | 27 365 558 | 554 431 | 2 292 | 5 744 | 6 592 | **27 934 617** |
| `d25` | 26 639 120 | 554 422 | 2 290 | 5 744 | 4 816 | **27 206 392** |
| `d35` | 32 408 169 | 554 429 | 2 276 | 4 080 | 16 256 | **32 985 210** |
| `d45` | 26 830 812 | 554 428 | 2 281 | 5 744 | 23 888 | **27 417 153** |
| `drb` | 35 685 626 + 485 427 | 554 423 | 2 284 | 5 360 | 29 952 | **36 763 072** |
| `d2b` | 225 351 | 554 432 | 2 283 | — | — | **782 066** |
| `d3b` | 484 278 | 554 428 | 2 272 | — | — | **1 040 978** |
| `d4b` | 486 977 | 554 417 | 2 279 | — | — | **1 043 673** |
| | | | | | | **155 173 161 o (148 Mo)** |

---

## 3. Les autres Dural du disque, qui ne sont PAS dans le jeu

| emplacement | contenu | taille | ce que c'est |
|---|---|---|---|
| `VF5RE/extracted/decors/VF5R/objset/stgdu1..4.farc` | 4 fichiers | 113 243 659 | **la source** de `d15..d45`. `_obj.bin` et `_tex.bin` sont identiques aux posés aux octets ; seuls les noms de membres du `FArC` changent |
| `VF5RE/extracted/decors/VF5_VERB/objset/stgdur + stgdu1..4` | 5 fichiers | 37 386 985 | **la source** de `drb`/`d1b..d4b` (les posés sont réécrits : textures renumérotées) |
| `VF5RE/extracted/decors/VF5FS_LIND/objset/stgdu1..5.farc` | 5 fichiers | 130 228 717 | copie de Final Showdown — **doublon, voir §5.3** |
| `SOURCES/APM3_FS/rom/objset/stgdu1..5.farc` | 5 fichiers | 130 228 717 | copie de Final Showdown — **doublon, voir §5.3** |
| `FS APM3/banc_revo/vf5fs_media/rom/` (Dural) | 9 objsets + soutien | ≈ 155 Mo | copie du jeu posé — **doublon, voir §5.2** |
| `SOURCES/PS3_VF5/PS3_GAME/USRDIR/objset/stgdur + stgdu1..4` | 5 fichiers | 37 417 927 | **une sixième famille**, jamais importée : le VF5 console PS3 |
| `SOURCES/APM3_US/.../data/stage/st_vf5_sanctuary1..5.par` | 5 fichiers | 41 019 392 | R.E.V.O. ; seul `sanctuary2` est entier (40 Mo), les quatre autres sont des souches de 190 464 o, **aux empreintes toutes différentes** |

Le PS3 n'est pas un doublon de ver.B, et c'est à l'octet qu'on le voit : trois
de ses quatre ciels ont **exactement la même taille** que ceux de ver.B
(485 426 / 484 272 / 486 760) et des **empreintes différentes**
(`5ec9174e…` contre `275067b8…`, `40ed092b…` contre `5593f110…`,
`0426deee…` contre `14283235…`). `stgdur` : 35 735 119 o contre 35 705 171.
C'est le piège que Frédéric a nommé — même nom, même taille, autres octets.

---

## 4. Qui référence quoi

| référence | ce qu'elle dit de Dural |
|---|---|
| **table des 86 descripteurs** (`.decors`, `0x180EB1000`, pas 0xF0) | 13 entrées, 21-25 / 78-81 / 82-85. Aucune entrée en double. Seul doublon de toute la table : l'indice **41**, code `x00`, qui recopie `STGDJO` — c'est la case **ALÉATOIRE** de la grille, pas un décor |
| **table des codes** (`.decors+0x50A0`) | 86 codes, **zéro doublon**. C'est elle qui fabrique `rom/ibl/<code>.ibl` et `rom/light_param/*_<code>.txt` |
| **grille STAGE SELECT** (`0x180400210`, 21 cases) | **une seule case pour Dural** : case 20, icône `stage_icon_dur_c`, indice 21. Identique octet pour octet dans `.origine` et dans la DLL patchée |
| **anneau de la barre espace** (`.greffe`, anneau 0) | `compte = 13`, indices `[21,22,23,24,25, 82,83,84,85, 78,79,80,81]`, puis `-1`. **Chaque indice une seule fois.** Libellés : SNOW, ECLIPSE, SUBMERSION, STORM, SPACE, puis les quatre « - VF5 R », puis « VIRTUA FIGHTER 5 - 1..4 » |
| **`rom/game_score.txt`** | `score.chara.20.stage=STGDU1` — **du1 seul**. Les douze autres ne sont atteignables que par l'anneau |
| **`obj_db` / `auth_3d_db`** | validés par `controle_decors_vf5.py` : chaque objset posé est déclaré une fois, ni plus ni moins que son archive |

Donc : **aucun décor de Dural n'est référencé deux fois, et aucun n'est
orphelin.** Les dix-neuf anneaux restants ont 3 variantes (FS / R / ver.B),
sauf `gym` et `smo` qui en ont 2 — ver.B ne les avait pas.

---

## 5. Les doublons établis par les octets

### 5.1 Parmi les treize décors : aucun

Les quatorze archives de géométrie (9 posées + 5 du `.par`) ont quatorze
empreintes distinctes. Descendu au niveau des **membres** `FArC` décomprimés
(`stg*_obj.bin` et `stg*_tex.bin`, 28 membres), **aucun membre d'un décor de
Dural n'est identique au membre d'un autre décor de Dural**. Le seul partage
est celui de la géométrie `drb` entre les indices 78-81, qui est la structure
même de ver.B.

Les quatre ciels de ver.B sont quatre images différentes aux octets : leurs
`_tex.bin` font `49575abb`, `5a2ca109`, `a7c0e24f`, `8a091161`.

### 5.2 La copie entière du jeu posé : `FS APM3/banc_revo`

`FS APM3/banc_revo/vf5fs_media/rom/` porte une **copie octet pour octet** des
décors posés. Pour Dural, les neuf objsets sont identiques :

```
829537fa327180ae  35 685 626  banc_revo/.../objset/stgdrb.farc
                              VF5RE/runtime/.../objset/stgdrb.farc
ba0c300cfb12548f  32 408 169  stgd35.farc   (idem)
44083ba107a53fe9  27 365 558  stgd15.farc   (idem)
3726c0962e6c37e2  26 830 812  stgd45.farc   (idem)
048f050a3daf9a58  26 639 120  stgd25.farc   (idem)
eff0037c3a42349a     486 977  stgd4b.farc   (idem)
3d9e0b9e4e3fee29     485 427  stgd1b.farc   (idem)
f40eb10a34fee3dc     484 278  stgd3b.farc   (idem)
0531b90be68f99ca     225 351  stgd2b.farc   (idem)
```

Les dossiers concernés, en entier :

| dossier de `banc_revo/vf5fs_media/rom` | fichiers | octets |
|---|---|---|
| `objset` | 47 | 994 466 693 |
| `2d` | 44 | 35 230 947 |
| `ibl` | 44 | 24 394 897 |
| `auth_3d` | 79 | 6 974 824 |
| `light_param` | 220 | 100 253 |
| **total** | **434** | **1 061 167 614 (1,0 Go)** |

**Dont Dural : 150 611 318 o d'objsets + ≈ 4,6 Mo de soutien.**

C'est le doublon le plus sûr à défaire, et pour une raison mesurable :
`FS APM3/outils/monter_banc_revo.cmd` **recrée ces cinq dossiers** quand on
l'appelle avec `mod` (lignes 138-142), et **les supprime lui-même** quand on
l'appelle sans (lignes 147-148, `rmdir /s /q`). Le banc est idempotent ; la
copie n'est pas une donnée, c'est un cache.

### 5.3 Les deux copies de Final Showdown, et celle qui est corrompue

`VF5RE/extracted/decors/VF5FS_LIND/objset/` et
`SOURCES/APM3_FS/rom/objset/` portent les **mêmes octets** pour les cinq
Dural de Final Showdown :

| fichier | taille | SHA-256 | VF5FS_LIND | SOURCES/APM3_FS | `.par` du jeu |
|---|---|---|---|---|---|
| `stgdu1.farc` | 27 229 016 | `280dd81af86a6ec1` | ✔ | ✔ | ✔ **identique** |
| `stgdu2.farc` | 24 144 242 | `a5c11e703aa67937` | ✔ | ✔ | ✔ **identique** |
| `stgdu3.farc` | 27 894 787 | `7af62afc4e856d9e` | ✔ | ✔ | ✔ **identique** |
| `stgdu4.farc` | 26 188 937 | `a7f07087812ac205` | ✔ | ✔ | ✘ **`52235964c6d22f58`** |
| `stgdu5.farc` | 24 771 735 | `3b228300b70c4a82` | ✔ | ✔ | ✔ **identique** |

Quatre des cinq sont donc une **troisième et une quatrième copie** de ce que le
`.par` du jeu contient déjà. 130 228 717 octets, deux fois.

**Et voilà le cheveu.** `stgdu4.farc` fait la même taille de part et d'autre et
diffère d'**un seul octet**, à l'offset `0x186AF00` : `0xB9` dans le `.par`,
`0xF9` dans les deux copies libres — un bit, `0x40`. Cet octet est **dans le
flux gzip du membre `stgdu4_tex.bin`**, et la conséquence est nette :

* le membre du `.par` se décomprime (empreinte `7a2eb1d2995faf6f`) ;
* celui des copies libres **échoue au CRC gzip**
  (`BadGzipFile: CRC check failed 0x768190a4 != 0x80056953`).

Les deux copies libres de `stgdu4.farc` sont **corrompues**, et elles le sont
de la même façon — elles descendent de la même extraction fautive. Le bon
exemplaire est celui du jeu.

Conséquence de méthode : `analysis/decors_lindbergh.csv` écrit
« FS Lind == APM3 » sur presque toutes ses lignes, dont `du4`. **Cette colonne
compare des tailles, pas des octets** (`tools/inventaire_decors.py`). Sur `du4`
elle se trompe. Et comme `VF5FS_LIND` et `SOURCES/APM3_FS` sont identiques aux
octets, les deux colonnes `FS_Lindbergh` et `FS_APM3` du CSV mesurent
probablement **la même matière deux fois** — je ne l'ai vérifié que sur Dural,
pas sur les 41 décors.

### 5.4 Les octets dupliqués qu'il ne faut PAS toucher

Un décor ajouté exige ses pièces **sous son propre code** : le chargeur
d'éclairage `0x1800D7130` compose `./rom/ibl/<code>.ibl`, et l'exemplaire du
`.par` rangé sous `du1` ne répond pas pour `d15`. Ces fichiers sont donc des
doublons d'octets **nécessaires** :

| fichier posé | identique à (dans le `.par`) | taille |
|---|---|---|
| `ibl/d15.ibl` | `du1.ibl` | 554 431 |
| `ibl/d35.ibl` | `du3.ibl` | 554 429 |
| `ibl/d45.ibl` | `du4.ibl` | 554 428 |
| `STGD15_COLI.000.bin` | `STGDU1_COLI.000.bin` | 5 744 |
| `STGD25_COLI.000.bin` | `STGDU1_COLI.000.bin` | 5 744 |
| `STGD45_COLI.000.bin` | `STGDU1_COLI.000.bin` | 5 744 |
| `STGD35_COLI.000.bin` | `STGDU3_COLI.000.bin` | 4 080 |
| `light_param/fog_d15`, `glow_d15`, `wind_d15` | `*_du1` | 704 |
| `light_param/wind_d25` | `wind_du2` | 218 |
| `light_param/fog_d35`, `glow_d35`, `wind_d35` | `*_du1`/`*_du3` | 687 |
| `light_param/light_d45`, `fog_d45`, `glow_d45`, `wind_d45` | `*_du4` | 2 256 |
| `light_param/wind_drb`, `wind_d2b` | `wind_du1` | 432 |
| `light_param/wind_d3b` | `wind_du3` | 199 |
| les 8 `envmap_correct_*` | `envmap_correct_du1` | 200 |

Environ **1,7 Mo**, et aucun n'est supprimable : enlever `d15.ibl` ne fait pas
tomber le décor, il fait **geler l'écran de chargement**, qui est exactement la
faute du 2026-09-10 sur `envmap_correct_*`.

À noter au passage, dans le même tableau : `d15`, `d35` et `d45` partagent
l'éclairage **exact** de `du1`, `du3` et `du4` — VF5 R n'a pas retouché ces
trois ambiances. `d25`, lui, a bien un `.ibl` propre (`4f0e72a5` contre
`4534db01` pour `du2`). **Ce sont ces trois-là, et elles seules, qui à l'écran
ont la même lumière que leur homologue Final Showdown** ; seule la géométrie
diffère. C'est probablement ce que Frédéric a vu.

---

## 6. La proposition, classée par sûreté

### Rang 1 — sûr, et le script le fait déjà lui-même

**Supprimer les cinq dossiers de décors de `FS APM3/banc_revo/vf5fs_media/rom`**
(`objset`, `2d`, `ibl`, `auth_3d`, `light_param`).

* récupéré : **1 061 167 614 o (1,0 Go)**, dont **≈ 155 Mo pour Dural**
* ce qui casse : **rien**. `monter_banc_revo.cmd` sans `mod` les supprime
  lui-même, et avec `mod` les recrée depuis `VF5RE/runtime`. Aucune table, aucun
  indice, aucune entrée d'écran ne les nomme : le banc est un jeu monté à côté
* commande de remise en état : `outils\monter_banc_revo.cmd mod`

### Rang 2 — sûr dès qu'un détail est corrigé

**Supprimer `VF5RE/extracted/decors/VF5FS_LIND/objset/stgdu1..du5.farc`.**

* récupéré : **130 228 717 o (124 Mo)**
* ce qui casse : `tools/inventaire_decors.py` lit la **taille** de ces cinq
  fichiers pour la colonne `FS_Lindbergh` de `analysis/decors_lindbergh.csv`.
  Les cinq lignes `du1`..`du5` y passeraient à `0`, comme les lignes `dur` et
  `evo*` le sont déjà pour les générations qui ne les ont pas. Le CSV ne serait
  pas faux, il serait muet sur ces cinq cases
* **aucune** table du moteur, aucun outil de pose, aucun contrôle ne les lit :
  `variantes_5r.py` lit `VF5R`, `variantes_vf5.py` lit `VF5_VERB`. On n'importe
  pas Final Showdown dans Final Showdown
* **avant de supprimer** : `stgdu4.farc` est corrompu ici. Si on veut garder une
  copie libre de `du4`, il faut la **réextraire du `.par`**, pas copier
  `SOURCES/APM3_FS` qui porte le même bit retourné

### Rang 3 — sûr, mais c'est l'autre moitié du même doublon

**Supprimer `SOURCES/APM3_FS/rom/objset/stgdu1..du5.farc`** *à la place* du
rang 2 (pas en plus : garder **une** copie libre).

* récupéré : les mêmes **130 228 717 o**
* ce qui casse : `SOURCES/` est l'inventaire des matières premières
  (`tools/inventory_sources.py`). Y creuser un trou se paie plus tard que dans
  `extracted/`. **Je recommande le rang 2 plutôt que celui-ci**
* dans les deux cas, `stgdu4.farc` restant est corrompu : à réextraire

### Rang 4 — possible, mais ce n'est plus une suppression de doublon

**Retirer un décor jouable de l'anneau de Dural.** Aucun n'est un doublon : le
faire est un choix d'auteur, pas un dédoublonnage. Si Frédéric veut alléger les
treize, les trois candidats les mieux fondés par la mesure sont **`d15`, `d35`
et `d45`** — les seuls dont l'éclairage est *identique aux octets* à celui de
leur homologue Final Showdown (§5.4), donc les seuls dont on puisse dire qu'ils
ne se distinguent que par la richesse du maillage.

* récupéré : `d15` 27 934 617 + `d35` 32 985 210 + `d45` 27 417 153 =
  **88 336 980 o (84 Mo)**
* **gardés** : les cinq de Final Showdown (21-25, intouchables), les quatre de
  ver.B (78-81, seule géométrie de Dural absente de toutes les versions
  ultérieures), et **`d25`** — le seul des quatre VF5 R dont l'ambiance diffère
* ce qui casse, et c'est précis :
  * l'anneau 0 doit passer de 13 à 10 : `VAR_COMPTES[0]` et `VAR_IDX[0]`. Ce
    sont des données de la greffe, **reposées à chaque reconstruction** — rien
    à éditer à la main
  * **l'indice glisse.** Retirer `d15` (82) de `variantes_5r.DURAL_5R` ferait
    remonter `d25`, `d35`, `d45` de 83-85 à 82-84, et **toute** la chaîne
    (descripteurs, `obj_db`, `auth_3d_db`, tables d'effet, `--decors-table 86`,
    `--decor-ecretage 86`) se décale. `controle_decors_vf5.py r` le verrait,
    mais c'est du travail pour rien
  * **la forme sûre** : retirer `d35` et `d45` par la **fin** (85 puis 84), ce
    qui ne décale personne, et laisser `d15` en place ; ou garder les indices et
    ne retirer que de l'anneau, auquel cas les fichiers restent sur le disque et
    on ne récupère rien
  * outil : `py -3 tools/decor_neuf.py --retirer d45` puis `--retirer d35`, et
    la ligne correspondante hors de `DURAL_5R`
* **je ne recommande pas ce rang 4.** Il coûte une reconstruction et un
  contrôle, il retire des décors que Frédéric a demandé d'importer, et il ne
  règle aucun doublon réel. Les rangs 1 et 2 rendent 1,1 Go sans toucher au jeu.

### Ce qu'il ne faut pas supprimer

* **les cinq de Final Showdown (21-25)** — `feedback_ne_pas_toucher_decors_fs` ;
  et ils sont dans le `.par`, pas en fichiers
* **`stgd1b.farc`** — il n'a ni code ni indice, on pourrait le croire orphelin.
  C'est le **ciel de `drb`**, objset 6187, déclaré dans `obj_db` et chargé par
  la liste `+0x00` de `0x18034D570`. Le supprimer ferait un `drb` sans ciel
* **`extracted/decors/VF5R`** et **`extracted/decors/VF5_VERB`** — ce sont les
  sources de pose ; `decor_neuf.py` les relit à chaque reconstruction
* **`SOURCES/PS3_VF5`** et **`SOURCES/APM3_US/.../st_vf5_sanctuary*`** — pas des
  doublons (§3), et ce sont des matières premières

---

## 7. Un défaut trouvé en chemin, et il n'a rien à voir avec les doublons

En relisant les collisions, un fait qui mérite d'être dit tout de suite.

**`--du2-collision` n'a plus d'effet dans ce build.** Mesure :

| ce qui est lu | indice 22, champ `+0x48` |
|---|---|
| ancienne table `0x180403430`, DLL patchée | `0x180641B60` → `rom/STGDU2_COLI.000.bin` ✔ le correctif est là |
| table vivante `.decors` `0x180EB1000`, DLL patchée | `0x180407920` → **`rom/STGDU1_COLI.000.bin`** |

Et la table vivante est bien `.decors` : en comptant les disp32 rip-relatifs de
`.text`, l'ancienne adresse `0x180403430` reçoit **5 références dans
`.origine` et 0 dans la DLL patchée** ; `0x180EB1000` en reçoit **0 puis 5**.
`--decors-table 86` a déménagé la table, et `--du2-collision` écrit ses trois
octets dans celle que plus personne ne lit.

Autrement dit : **le symptôme que Frédéric avait relevé — en ring out sur du2,
le personnage se pose sur un sol inexistant — est revenu**, et il revient dans
tous les lanceurs qui cumulent `--du2-collision` et `--decors-table`
(`item_porte.cmd`, `questV2.cmd`, `decors_vf5.cmd`). C'est une régression de
l'option, pas une régression de données.

Je ne l'ai **pas** corrigé : l'option vit dans `tools/socle_20261008.pyc`, et la
consigne était de ne rien reconstruire. À trancher par Frédéric.

---

## 8. Ce qui n'a PAS été vérifié

* **L'écran.** Rien de ce qui précède n'a été vu tourner ; aucun jeu n'a été
  lancé. C'est l'écran qui tranche.
* **Les ciels, en image.** Je n'ai comparé que des octets. Deux ciels aux
  empreintes différentes peuvent se ressembler à l'œil — et c'est très
  probablement le cas entre `du4`/`d45` (STORM) et `d3b` (ver.B, noté
  « orage » dans `analysis/decors.md` §21.4). Les planches
  `analysis/ciel_verb_du1..4.png` et `analysis/dural_nuit_le_point.png` citées
  par les notes **n'existent plus sur le disque** : il faudrait les refaire pour
  répondre. **Si « doublon » veut dire « ça se ressemble à l'écran », ma mesure
  ne répond pas à la question.**
* **La texture de ciel, isolée.** Pour `d15..d45` et `du1..du5`, le ciel est un
  objet parmi des centaines dans un `_tex.bin` de 37 à 54 Mo. J'ai montré que
  les `_tex.bin` entiers diffèrent ; je n'ai **pas** extrait la seule texture de
  ciel pour comparer variante par variante.
* **Le reste du CSV.** J'ai établi que `VF5FS_LIND` et `SOURCES/APM3_FS` sont
  identiques aux octets **sur les cinq Dural seulement**. Que ce soit vrai pour
  les 41 décors — et donc que les deux colonnes du CSV soient la même matière —
  est une **hypothèse**, pas une mesure.
* **`banc_gog`.** 2,8 Go, 665 fichiers. Je n'y ai pas cherché de décors de
  Dural (le `find` n'en a trouvé aucun), mais je n'ai pas inventorié le dossier.
* **L'indice 41 / code `x00`.** Son descripteur recopie `STGDJO` et la case 10
  de la grille (`stage_icon_rnd_c`) le désigne. Je conclus que c'est la case
  ALÉATOIRE parce que `GRILLE_COMPTES` nomme « la boucle qui cherche la case
  ALEA » et « la borne du tirage au sort » ; **je n'ai pas lu le code du tirage**
  pour le prouver.
* **L'intention du patcheur.** `--decors-table`, `--variantes-*`,
  `--du2-collision` sont dans `socle_20261008.pyc`, compilé. Tout ce que je dis
  de leur effet vient de la **DLL produite**, pas de leur source.
* **`obj_db`, à la main.** Je me suis appuyé sur
  `controle_decors_vf5.py` (« RIEN A REDIRE ») ; je n'ai pas recompté les
  déclarations d'objsets par un troisième chemin.

---

## 9. Résumé

* **Doublons parmi les treize décors de Dural du jeu : zéro.** Treize
  empreintes distinctes, treize codes distincts, treize indices distincts, un
  seul passage de chacun dans l'anneau. Le partage de géométrie entre les
  quatre entrées de ver.B est la structure de ver.B, pas un doublon.
* **Doublons de fichiers, eux bien réels : 1,19 Go**, dont **280 Mo de Dural** —
  la copie du jeu posé dans `FS APM3/banc_revo` (1,0 Go, dont 155 Mo de Dural)
  et la double copie libre des cinq Dural de Final Showdown dans
  `extracted/decors/VF5FS_LIND` **et** `SOURCES/APM3_FS` (124 Mo chacune, dont
  quatre sur cinq sont déjà dans le `.par`).
* **Un fichier corrompu**, trouvé par l'empreinte et non par la taille :
  `stgdu4.farc` des deux copies libres a un bit retourné à `0x186AF00` et son
  `stgdu4_tex.bin` échoue au CRC gzip. L'exemplaire du `.par` est sain.

**Recommandation.** Faire le rang 1 et le rang 2 : vider les cinq dossiers de
décors de `banc_revo` (que son propre script recrée) et retirer les cinq
`stgdu*.farc` de `extracted/decors/VF5FS_LIND/objset`. **1 191 396 331 octets
(1,11 Go) récupérés, et rien dans le jeu ne change** — aucun indice ne glisse,
aucune case de l'écran ne pointe dans le vide, aucun contrôle ne tombe. Ne pas
toucher aux treize décors eux-mêmes : il n'y a rien à dédoublonner là.

Et, séparément, trancher le §7 : `--du2-collision` n'atteint plus la table que
le moteur lit.

---

**Suite, 2026-11-20 :** le defaut `--du2-collision` signale ici est mesure et repare. Six references RIP-relatives, pas cinq, et **dix-sept** lanceurs concernes, pas trois. Voir [du2_collision_table_vivante.md](du2_collision_table_vivante.md).
