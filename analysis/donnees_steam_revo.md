# LIRE LES DONNÉES EN PLACE DANS LE DOSSIER STEAM DE R.E.V.O.

Mesure du **19 novembre 2026**. Source lue, en **lecture seule et sans rien
écrire** :

```
C:\Program Files (x86)\Steam\steamapps\common\VFREVO\runtime\media\vf5fs
```

Question de Frédéric : *« peut-on lire directement certaines données du fichier
d'installation de Virtua Fighter REVO Steam — musiques, voix, modèles 3D,
textures — et quelle version est la meilleure ? »*

Ce document distingue partout le **MESURÉ** (empreinte calculée, image
regardée, journal relu) du **supposé**. Il complète
[APM3_SUR_DONNEES_REVO.md](APM3_SUR_DONNEES_REVO.md) du 4 novembre, et **ferme
sa réserve §7.3** (`mot_db.farc`, « personne n'a regardé en quoi »).

---

## 1. La réponse courte

**Il n'y a rien à « lire autrement » : les données de REVO Steam et celles du
dump d'arcade APM3 sont les mêmes octets.** Sur les 1 862 fichiers de
`vf5fs_data.par`, **1 861 sont identiques au SHA-256**, et le seul qui diffère
est un fichier de noms où *Dural* s'appelle autrement.

La question n'est donc pas « peut-on lire les données de REVO », mais
**« pourquoi en garder une copie ? »**. Et la réponse d'architecture est que
l'on peut pointer dessus : **huit ouvertures de fichier, toutes passées par une
seule fonction de l'hôte, toutes avec un chemin absolu** — c'est mesuré dans
nos propres journaux, pas déduit.

---

## 2. Les empreintes, mesurées

### 2.1 Les trois archives, en entier

| archive | taille | SHA-256 (début) |
|---|---|---|
| `vf5fs_data.par` **Steam REVO** | 3 987 499 008 | `A36BCF83CBA813FB…` |
| `vf5fs_data.par` **APM3** (`FS APM3\banc`) | 3 987 499 008 | `AB476ED0B89C8D1A…` |
| `ws_sound.par` **Steam REVO** | 4 759 552 | `3C0DDF8C9B5F4F16…` |
| `ws_rob_data.par` **Steam REVO** | 3 231 744 | `A47402AC3A126E5D…` |

Les deux `vf5fs_data.par` font **exactement la même taille** et **n'ont pas la
même empreinte**. Il fallait donc descendre d'un cran : c'est fait au §2.2.

Trois empreintes de contrôle, qui situent les copies de l'atelier :

| copie | SHA-256 | verdict |
|---|---|---|
| `FS REVO\vf5fs_data.par` | `A36BCF83…` | **identique à Steam, à l'octet près** |
| `FS REVO\ws_rob_data.par` | `A47402AC…` | identique à Steam |
| `FS REVO\ws_sound.par` | `3C0DDF8C…` | identique à Steam |
| `FS APM3\banc_revo\vf5fs_data.par` | `CAB35EAF…` | **notre copie masquée** (§2.3) |
| `FS APM3\banc_revo\ws_rob_data.par` | `318BB664…` | **build REVO antérieur** (§2.4) |

> **Le banc `FS REVO` tourne déjà sur une copie bit à bit du fichier de Steam.**
> Pointer sur Steam ne changerait donc rien à ce qu'il lit — seulement à ce
> qu'il faut avoir sur le disque.

### 2.2 Entrée par entrée : 1 861 sur 1 862 identiques

Outil écrit pour la mesure (empreinte SHA-256 des octets **stockés** de chaque
entrée, sans rien extraire) ; il lit l'index PARC avec `VF5RE\tools\par_inventaire.py`.

```
vf5fs_data.par  STEAM REVO   1862 entrées
vf5fs_data.par  APM3         1862 entrées
communs 1862    seulement REVO 0    seulement APM3 0
offsets différents : 0
communs mais SHA-256 DIFFÉRENT : 1
    mot_db.farc    REVO 83 726 o    APM3 83 728 o
```

Et dans l'en-tête, le pot de noms et la table des fichiers — 180 608 octets —
**6 octets diffèrent**, tous dans l'enregistrement de `mot_db.farc` : sa taille
(deux fois) et un champ de quatre octets en `+0x1C`. Le reste de la table est
identique au bit près.

**Contrôle de l'instrument** (CLAUDE.md §4 : un contrôle doit pouvoir échouer).
Le même outil, passé sur les deux `ws_rob_data.par`, rend **404 entrées
identiques sur 405 et nomme la différente** (`ws_enemy_data.txt`). Il sait donc
dire « différent » quand ça l'est, et « identique » quand ça l'est.

### 2.3 Les 26 noms de `banc_revo` ne sont pas des données

`FS APM3\banc_revo\vf5fs_data.par` présente 26 noms que Steam n'a pas
(`aet_db.bi_`, `spr_n_cmn.far_`, `stgnyc.far_`…). Ce sont les **renommages
d'un octet** de `VF5RE\tools\par_masquer.py`, posés par l'atelier pour faire
retomber le moteur sur les fichiers libres. Les **1 836 autres entrées sont
identiques au SHA-256**, offsets compris. Aucune donnée n'y a changé.

### 2.4 `mot_db.farc` : la réserve §7.3 est fermée

Les deux `mot_db.bin` décompressés font **290 208 octets tous les deux** et
diffèrent en **628 octets, répartis en 202 plages**. Les 202 plages, sans
exception, sont **le même renommage** :

```
APM3  :  DUR_BLACK…   DUR_BLK_…   DMY_BLK_…   BLACK_BACK…
REVO  :  DUR_VANES…   DUR_VAN_…   DMY_VAN_…   VANES_BACK…
```

`BLACK` → `VANES` et `BLK` → `VAN`, à longueur égale — d'où la taille
inchangée, et d'où les deux octets d'écart du `.farc`, qui viennent de la seule
recompression SLLZ. **Dural, et rien d'autre.** C'est exactement la ligne de
[MODERN_DATA_LINEAGE.md](MODERN_DATA_LINEAGE.md) §3 : *« le seul écart est
Dural »*, et le `mot_db` de REVO suit la branche console.

---

## 3. Famille par famille

Rappel de la topologie, elle vaut pour les deux versions : ce qui est **dans**
`vf5fs_data.par` vient de l'archive ; ce qui n'y est pas retombe sur
l'arborescence libre `vf5fs_media\` (mesuré au point d'arrêt sur `CreateFileW`,
[import_decors.md](import_decors.md) §2).

### 3.1 Le tableau

| famille | où elle vit | REVO Steam vs APM3 | qualité mesurée | meilleure source |
|---|---|---|---|---|
| **Musiques (BGM)** | libre, `vf5fs_media\rom\sound\bgm\` | **270 communes, 270 identiques au SHA-256.** REVO en a **67 de plus**, APM3 **15 de plus** | ADX type 3, ADPCM 4 bits, **48 000 Hz stéréo, ~432 kbit/s** des deux côtés ; la famille `h_*` est à 22 050 Hz des deux côtés | **REVO** (même qualité, +67 titres) |
| **Voix** | libre `…\voice\auth_voice\` (466) + banques `vo_*.acb` **dans** le `.par` (20, 12,7 Mo) | **467 fichiers libres communs, 467 identiques.** Les 20 `vo_*.acb` et 19 `auth_*.acb` du `.par` sont identiques | ADX mono **44 100 Hz, ~200 kbit/s** (463 fichiers sur 466 ; 3 à 16 000 Hz), 818 s au total | **égalité** — mêmes octets |
| **Modèles 3D personnages** | **dans** le `.par` : `<xxx>itm.farc` + `<xxx>itm_patch.farc` (62 fichiers, 2,81 Go), squelettes `aki.farc`… | **identiques au SHA-256** | `akiitm733_obj.bin` : magie `0x05062500`, objets et jeux de textures déclarés comme sur la borne | **égalité** — mêmes octets |
| **Modèles 3D décors** | **dans** le `.par` : 41 `stg*.farc` (538 Mo) | **identiques au SHA-256** | `stgnyc_obj.bin` : **390 objets, 332 textures** | **égalité** — mêmes octets |
| **Textures personnages** | dans les mêmes `<xxx>itm*.farc`, bloc TXP | **identiques au SHA-256** | `akiitm733_tex.bin` : 25 textures, **DXT1 ×13 / DXT5 ×12**, jusqu'à **1024×512**, 11 niveaux de mip | **égalité** — mêmes octets |
| **Textures décors** | dans les `stg*.farc`, bloc TXP | **identiques au SHA-256** | `stgnyc_tex.bin` : 332 textures, **DXT1 ×184 / DXT5 ×148**, **neuf planches 2048×2048** à 12 niveaux de mip | **égalité** — mêmes octets |
| *(hors demande)* **2D / interface** | dans le `.par`, 1 115 `spr_*`/`aet_*` (407 Mo) | identiques | — | égalité |
| *(hors demande)* **Films** | libre, `rom\movie\` | **5 films sur 7 diffèrent en taille** | les `.usm` de REVO sont **bien plus gros** (`vf5end.usm` 605 Mo contre 120 Mo) | **REVO, probablement** — voir la réserve du §6 |

### 3.2 Les images ont été REGARDÉES, pas seulement comptées

CLAUDE.md §7 : *« une statistique sur une image n'est pas une lecture de
l'image »*. Deux textures ont donc été sorties **du `.par` de Steam
directement**, converties en PNG et **affichées** :

* `akiitm__tex018.png`, 1024×512 DXT1, 11 mips — c'est bien une **planche de
  costume** : le blouson noir et rouge d'Akira, coutures, poche et bouton
  lisibles ;
* `stgnyc__tex315.png`, 2048×2048 DXT1, 12 mips — c'est bien l'**atlas du
  décor City** : façades d'immeubles éclairées, tôle rouillée, plaque
  d'immatriculation, et le panneau *SPORT CHANNEL*.

La chaîne complète **PARC → FArC → TXP → image** fonctionne donc de bout en
bout sur le fichier de Steam, sans copie et sans modification.

### 3.3 Ce que REVO a en plus, et APM3 en moins

| | REVO Steam | APM3 |
|---|---|---|
| BGM en plus | **67** : 19 `dlc2_ryu_*`, 20 `dlc2_vf3_*`, 20 `dlc3_tkn_*`, 4 `vf5revo_bgm_*`, 3 `vf5revo_jng_*` | — |
| BGM manquants | — | **15** `vf5ps3_*` (b03map…j26) |
| archives en propre | `ws_sound.par` (1 entrée, `se_ws_adam.acb`, 4,76 Mo), `ws_rob_data.par` (405 entrées) | — |
| couche `rom_200\` | **oui** : `chritm_tbl.farc` 13,57 Mo, `resident.farc` + révisions `.r2421`/`.r2427`, `string_array.farc`, 41 `rob\`, 20 `training\` | absente |
| `rom\rob\` libre | **oui**, 91 fichiers (127 Mo) qui doublent la couche d'arcade | absent |
| nuanceurs | `shader_pxd_w64.farc` **vidé à 9 026 o** + `shader_pxd_w64_d3d12.farc` 53 778 o | `shader_pxd_w64.farc` **10 530 083 o** (D3D11) + `shader_vf5_w64.farc` |

L'arborescence libre de Steam pèse **4 010 439 384 o** (3,74 Go) pour 970
fichiers, dont **2,22 Go de films** et **1,62 Go de musique**.

> **Attention à ne pas comparer les films de travers.** Le `rom\movie\` du dump
> APM3 de l'atelier a été **enrichi par le projet** : il contient
> `vf5REVOadv.usm`, `vf5REVOend.usm`, `vf5adv.usm.ecarte`, `vf5Radv.usm`… Ce
> n'est plus un témoin vierge. Les écarts de films du §3.1 sont donc **mesurés
> mais non interprétables** tant qu'on ne les refait pas contre
> `SOURCES\APM3_FS`.

---

## 4. Lire en place depuis le dossier Steam : ce que ça demande

### 4.1 Qui ouvre les fichiers aujourd'hui — et c'est déjà mesuré

CLAUDE.md §4.1 : *la sonde parle-t-elle déjà ?* **Oui.** Les 486 journaux
d'hôte du disque le disent tous pareil. Les huit premières lignes de
`FS REVO\host_log.txt` :

```
[ouvrir] n1  …/FS REVO/vf5fs_data.par                                  -> OK
[ouvrir] n2  …/FS REVO/ws_rob_data.par                                 -> OK
[ouvrir] n3  …/FS REVO/ws_sound.par                                    -> OK
[ouvrir] n4  …/FS REVO/vf5fs_media/w64/shader_pxd_w64_d3d12.farc       -> OK
[ouvrir] n5  …/FS REVO/vf5fs_media/rom_200/string_array.farc           -> OK
[ouvrir] n6  …/FS REVO/vf5fs_media/rom_200/chritm_tbl.farc             -> OK
[ouvrir] n7  …/FS REVO/vf5fs_media/rom_200/rob/mothead_CMN.bin         -> OK
[ouvrir] n8  …/FS REVO/vf5fs_media/rom_200/resident.farc               -> OK
```

**Huit ouvertures, et huit seulement**, dans tous les journaux qui en portent
(484 sur 486). C'est cohérent avec `MENU.md` : *« `vf5fs_data.par` est ouvert
une fois et lu »* — tout le reste est une **fenêtre** dans l'archive déjà
ouverte, pas un `open()`.

Ces huit passent par **une seule fonction de l'hôte**,
`OuvrirFichier` (`FS REVO\host_revo\vf5fs_host.cpp` ≈ ligne 23799), qui fait
exactement ceci :

```c
HANDLE f = CreateFileA(p, GENERIC_READ, FILE_SHARE_READ|FILE_SHARE_WRITE, …);
```

et **`p` est déjà un chemin absolu** fourni par le module. Les deux autres
routes de données sont elles aussi chez nous :

* le **son** : cran 28 `SetFile`, puis notre décodeur ADX ; le journal montre
  `…/vf5fs_media/rom/sound/bgm/vfes_se_logo_sega.adx  2 voie(s), 48000 Hz` ;
* le **film** : cran 34 `SetFile`, qui reçoit du relatif et que
  `NoterRacineMedia()` complète avec `g_racineMedia`.

La racine vient de l'hôte lui-même : au démarrage il fait
`GetModuleFileNameA(nullptr, …)` puis `SetCurrentDirectoryA(dir)` — **la racine
des données, c'est le dossier de l'hôte**.

### 4.2 Côté module, les chemins sont dans des cases modifiables

Dans `vf5fs-pxd-w64-d3d12_SteamRetail.dll`, l'accesseur `FUN_1802cb470(i)`
(`VF5RE\code_decompile\FUN_1802cb470.c`) rend `s__vf5fs_data + i * 0x104`, borné
à `i < 4`. Les quatre cases, relevées dans la section **inscriptible** du
binaire, valent :

```
créneau 0   "/vf5fs_data"      créneau 2   "/ws_sound"
créneau 1   "/ws_rob_data"     créneau 3   "/vf5fs_media"
```

et l'extension `par` est une chaîne à part. Ce sont **quatre tampons de 0x104 =
260 octets, soit MAX_PATH chacun** — pas des constantes en lecture seule. Le
module d'APM3 a le même dispositif avec deux cases (`/vf5fs_data`,
`/vf5fs_media`).

> **Non vérifié, et il faut le dire** : *qui* écrit dans ces quatre cases, et si
> un chemin absolu posé là survit à l'initialisation. Le relevé ci-dessus dit
> que la place existe et qu'elle est inscriptible ; il ne dit pas que le module
> l'accepterait. Cette question-là demanderait Ghidra, pas un grep.

### 4.3 Le verdict

**Oui, c'est lisible en place, et le chemin le moins cher ne touche pas au
module.** Trois gestes, tous dans l'hôte :

1. une **racine de données** configurable (variable d'environnement, par
   exemple `VF5_DONNEES=C:\Program Files (x86)\Steam\steamapps\common\VFREVO\runtime\media\vf5fs`),
   avec repli sur le dossier de l'hôte si elle est absente ou introuvable ;
2. dans `OuvrirFichier`, **substituer le préfixe** avant `CreateFileA` : si le
   chemin absolu commence par le dossier de l'hôte, le réécrire sur la racine
   Steam ; sinon, laisser tel quel ;
3. la même substitution appliquée à `g_racineMedia` (films) et à
   `son_revo_racine()` (son) — les deux la reçoivent déjà par une seule ligne
   chacune.

Coût : **3,71 Go de `.par` + 3,74 Go d'arborescence libre en moins dans le
paquet**, et plus aucune donnée de SEGA redistribuée. Pour situer : le disque
du projet porte aujourd'hui **cinq copies** du `vf5fs_data.par` de 3 987 499 008
octets (`FS REVO`, `FS APM3\banc`, `FS APM3\banc_revo`, `SOURCES\APM3_US`,
`REVO test avec YAMP LJ`), plus une variante de 4 139 423 218 o.

### 4.4 Ce qui casse, nommé d'avance

| | ce qui casse | parade |
|---|---|---|
| **1** | **`par_masquer.py` devient impossible.** Masquer une entrée écrit dans le `.par` ; le `.par` de Steam est intouchable par règle de projet. Or c'est la recette de tous les décors importés et de toutes les textures HD 3D. | faire la substitution **dans `OuvrirFichier`** : si le nom demandé a une version à nous, servir la nôtre. Le masquage devient une table de l'hôte, pas une écriture dans l'archive. |
| **2** | **Le `.par` serait ouvert en lecture seule et partagé avec Steam.** `OuvrirFichier` demande déjà `GENERIC_READ` + `FILE_SHARE_READ\|FILE_SHARE_WRITE` : rien à changer. | aucune |
| **3** | **Le chemin Steam contient des espaces ET des parenthèses** : `C:\Program Files (x86)\…`. Dans un `.cmd`, une parenthèse non échappée à l'intérieur d'un bloc `( … )` est une erreur de syntaxe — c'est le piège d'écriture de CLAUDE.md §5 dans sa version la plus coûteuse. | guillemets systématiques, et pas de `set` du chemin à l'intérieur d'un bloc parenthésé |
| **4** | **`MAX_PATH`.** Les cases du module font 260 octets. Le chemin complet du `.par` de Steam en fait 88 : il passe. Un déplacement de la bibliothèque Steam sur un chemin long le ferait tomber. | mesurer la longueur au démarrage et refuser proprement |
| **5** | **Steam met à jour.** Mesuré ici : `FS APM3\banc_revo\ws_rob_data.par` (3 229 696 o, monté le 4 novembre) **n'est pas** celui que Steam porte aujourd'hui (3 231 744 o) ; le seul écart est `ws_enemy_data.txt`. `vf5fs_data.par`, lui, n'a pas bougé. | ne **jamais** verrouiller sur une empreinte de fichier entier : vérifier la présence et le format, pas le hachage |
| **6** | **Les nuanceurs D3D11 sont vides chez REVO** (9 026 o contre 10,5 Mo). Sans objet pour notre hôte, qui charge le module **D3D12** de REVO ; fatal pour un banc qui chargerait le module D3D11 d'APM3. | ne pas mélanger les deux bancs ; `monter_banc_revo.cmd emprunt` reste la seule route D3D11 |
| **7** | **`EasyAntiCheat` est présent** dans `runtime\media\`. Nous ne lançons pas `VFREVO.exe` ; lire des fichiers avec notre propre processus ne le concerne pas. | **non vérifié** : rien n'a été testé à ce sujet, et rien ne doit l'être sans accord |

---

## 5. « Preuve de possession » : la réponse franche

**Lire le dossier Steam prouve que des fichiers sont présents à un chemin. Cela
ne prouve pas une licence.** Le dossier se copie, se partage et se déplace ;
un utilisateur qui n'a jamais acheté REVO peut poser la même arborescence au
même endroit et notre build démarrera.

Ce qu'on gagne est réel, mais ce n'est pas celui-là :

1. **Nous ne redistribuons aucune donnée de SEGA.** 7,45 Go de matière sortent
   du paquet. C'est l'objectif §1 de CLAUDE.md tenu à la lettre : *« avec les
   seules données qu'un possesseur de REVO détient légitimement »*.
2. **C'est un verrou de courtoisie, pas un DRM** : il décourage l'usage sans le
   jeu, il ne l'empêche pas.

Une vraie preuve de possession passerait par l'API Steam (`SteamAPI_Init` puis
une vérification de propriété du jeu), ce qui suppose un client Steam ouvert et
une session — et resterait contournable. **Rien de tel n'a été tenté ni mesuré
ici**, et cela touche au DRM : c'est une décision de Frédéric, pas une
initiative.

---

## 6. Ce qui n'a PAS été vérifié

1. **Qui écrit dans les quatre cases de chemin du module**, et si un chemin
   absolu y survit (§4.2). Relevé statique seulement.
2. **Rien n'a été lancé.** Aucune course, aucun jeu démarré, `VFREVO.exe` jamais
   touché. Le verdict du §4.3 est une lecture du code et des journaux, pas une
   mesure à l'écran — et CLAUDE.md §3 rappelle que **c'est l'écran qui tranche**.
3. **Le son n'a pas été écouté.** Les en-têtes ADX sont lus, les octets sont
   identiques ; personne n'a entendu une piste.
4. **Les films ne sont pas comparables en l'état** : le `rom\movie\` d'APM3 de
   l'atelier a été enrichi de fichiers REVO par le projet (§3.3). Refaire la
   mesure contre `SOURCES\APM3_FS` avant toute conclusion. Et aucune résolution
   de `.usm` n'a été relevée — seulement des tailles.
5. **Le nombre de polygones n'a pas été compté.** Il n'en avait pas besoin : les
   `.farc` d'objset sont identiques au SHA-256 des deux côtés, donc la géométrie
   l'est aussi. Mais la mesure « tant de triangles par personnage » reste à
   faire si elle est voulue pour elle-même.
6. **Les 19 `auth_*.acb` à 4 960 o** sont suspects de n'être que des index ; le
   contenu d'onde n'a pas été ouvert.
7. **`EasyAntiCheat`** : aucune interaction, aucune mesure (§4.4, ligne 7).

---

## 7. Refaire les mesures

Les outils écrits pour ce document sont dans le dossier de travail temporaire
de la session (`…\scratchpad`) : `par_empreintes.py` (SHA-256 par entrée d'un
`.par`), `comparer.py`, `comparer_tables.py`, `lire_objset_steam.py` (TXP →
PNG depuis une archive quelconque), `adx_entete.py`. Ils ne dépendent que de
`VF5RE\tools\` (`par_inventaire`, `farc`, `textures_hd`, `txp`) et **n'écrivent
jamais dans le dossier lu**. S'ils doivent servir encore, leur place est
`VF5RE\tools\`.

```
py -3 -I par_empreintes.py "<...>\VFREVO\runtime\media\vf5fs\vf5fs_data.par" a.csv
py -3 -I par_empreintes.py "FS APM3\banc\vf5fs_data.par"                     b.csv
py -3 -I comparer.py a.csv b.csv
```
