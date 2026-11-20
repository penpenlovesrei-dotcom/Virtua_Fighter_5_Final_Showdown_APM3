# VERSIONS — identification précise de chaque source

Chaque conclusion porte un niveau de confiance parmi
`UNKNOWN` / `SPECULATIVE` / `LIKELY` / `SUPPORTED` / `CONFIRMED`.

---

## Méthode : deux signaux indépendants pour l'arcade

**Signal 1 — bloc de version interne.** Les deux ELF `vf5` contiennent en `.rodata` un bloc
littéral : numéro de release, horodatage de snapshot SCM, horodatage de link, titre, et
chemin de build. Ce bloc est produit par la chaîne de build de Sega.

**Signal 2 — CRC32 du loader.** `lindbergh-loader` identifie chaque jeu par
`CRC32(fichier[0x0A … 0x400A])` (`hook.c:1629`, `getCrc32` à `hook.c:167`, table dans
`config.h:81-83`). Cette table a été constituée par la communauté à partir de dumps
étiquetés par leur média d'origine (référence DVP), **indépendamment** du bloc interne.

Les deux signaux concordent. C'est la base de la confiance `CONFIRMED` ci-dessous.

---

## 1. `LIND_FS` → Virtua Fighter 5 Final Showdown **Rev A**

| Élément | Valeur |
|---|---|
| ELF | `disk1/vf5`, ELF32 LE EXEC EM_386, entry `0x080542E0` |
| Release interne | **2.000** |
| Snapshot SCM | `2010-06-28T11:48:57+09:00` |
| Date de link | `2010-06-28 13:54:24` |
| Chemin de build | `/p114/prj114p/snapshot/release/2.000/vf5_root/vf5` |
| Titre | `Virtua Fighter5 Final Showdown` |
| CRC32 loader | `0xBAE2BE62` |
| Correspondance loader | `VIRTUA_FIGHTER_5_FINAL_SHOWDOWN_REVA`, média **DVP-5019A**, game ID **SBUV** |

**Conclusion : VF5FS Rev A, release 2.000, construite le 2010-06-28. Confiance : CONFIRMED.**

Le dump est **complet et cohérent** : `vf5fs.bin` porte `/home` (dont `disk1/vf5`,
`disk1/rom/`, `disk1/drv/`) et `vf5fs_ext.bin` porte `rom/objset/` (modèles de décors et
personnages), tous datés du 2010-06-28. C'est la seule source du projet qui offre une
révision arcade entière et auto-cohérente.

---

## 2. `APM3_FS` → Virtua Fighter 5 Final Showdown **Rev B ver 6.0000**

| Élément | Valeur |
|---|---|
| ELF | `vf5`, ELF32 LE EXEC EM_386, entry `0x08054380` |
| Release interne | **6.000** |
| Chaînes voisines | `REVISION 1`, `VERSION A` |
| Snapshot SCM | `2011-10-14T22:31:04+09:00` |
| Date de link | `2011-10-17 21:13:35` |
| Chemin de build | `/p114/prj114p/snapshot/release/6.000/vf5_root/vf5` |
| CRC32 loader | `0x034C0D02` |
| Correspondance loader | `VIRTUA_FIGHTER_5_FINAL_SHOWDOWN_REVB_6000`, média **DVP-5020**, game ID **SBXX** |

**Conclusion : VF5FS Rev B ver 6.0000, release 6.000, construite le 2011-10-17.
Confiance : CONFIRMED.**

**La plateforme est Lindbergh, pas APM3. Confiance : CONFIRMED.** Preuves convergentes :

- ELF32 `EM_386` avec `DT_NEEDED` sur `libsegaapi.so`, `libalpb.so`, `libsama.so`,
  `libbdlog.so`, `libglut.so.3`, `libGL.so.1`, `libX11.so.6` ;
- `.comment` : toolchain **MontaVista Linux**, GCC 3.4.3 / 3.3.1 ;
- `.gdbinit` de Sega écrit pour registres `eax`/`eip`/`eflags` (ix86) ;
- `tools/lindbergh/` présent à la racine ;
- classes RTTI `CriSoundRendererLindbergh`, `CriSrVocCoreLindberghHsr` ;
- pilote NVIDIA Linux 8769 dans `drv/nvidia/`.

### Anomalie ouverte : `gameid=SBUV` dans le script `game`

Le script `game` de cette source contient `gameid=SBUV`, qui est l'identifiant **Rev A**
d'après la table du loader, alors que le binaire est sans ambiguïté la Rev B 6.0000.
Deux lectures possibles, non départagées :

1. le dump mélange un `vf5` Rev B 6.0000 avec un script de partition hérité du média Rev A ;
2. la correspondance `SBUV`↔RevA / `SBXX`↔RevB de la table communautaire est imprécise.

Le script `game` de `LIND_FS` (Rev A) ne contient **aucun** `gameid` — il est plus court et
ne fait pas de `parted`/`mkfs`. Il ne permet donc pas de trancher.
**Confiance sur la résolution : UNKNOWN.** À reprendre en phase 7.

---

## 3. `PS3_FS` → VF5FS PlayStation 3, édition européenne

Source de vérité : `PARAM.SFO` extrait du PKG.

| Clé | Valeur |
|---|---|
| `TITLE` | `Virtua Fighter 5 Final Showdown` |
| `TITLE_ID` | `NPEB00913` |
| `APP_VER` / `VERSION` | `01.00` |
| `CATEGORY` | `HG` (jeu HDD, distribution PSN) |
| `PS3_SYSTEM_VER` | `04.0000` |
| `NP_COMMUNICATION_ID` | `NPWR02868_00` |
| Content ID du PKG | `EP0177-NPEB00913_00-VIRTUAFIGHTER5FS` (EP0177 = SEGA Europe) |
| PKG | révision `0x8000` (retail), type `0x0001` (PS3), 375 éléments |

**Conclusion : VF5FS PS3, PSN Europe, version de base 01.00, sans mise à jour.
Confiance : CONFIRMED.**

**Le build interne du jeu reste inconnu** : `USRDIR/EBOOT.BIN` est un SELF NPDRM chiffré
(`SCE\0`, révision de clé `0x0019`). Confiance sur le build : **UNKNOWN** tant qu'il n'est
pas déchiffré. Le fichier `EP0177-NPEB00913_00-VIRTUAFIGHTER5FS.rap` fourni est la licence
NPDRM (16 octets) qui permettra d'obtenir la klicensee.

---

## 4. `X360_FS` → VF5FS Xbox 360 (XBLA) + Title Update 1

| Élément | Valeur |
|---|---|
| Conteneur principal | signature `LIVE`, paquet STFS, 2 051 182 592 o |
| Nom affiché | `Virtua Fighter 5 FS` |
| Title ID | `584111FE` (répertoire `584111FE/000D0000/`) |
| Second conteneur | `TU_1C424FU_0000004000000.0000000000081`, signature `LIVE`, nom `Virtua Fighter 5 FS Title Upda…` |

**Conclusion : VF5FS Xbox 360, contenu XBLA sous Title ID `584111FE`, accompagné d'une
mise à jour de titre. Confiance : CONFIRMED.**

**Version/build du jeu : UNKNOWN.** Le contenu du paquet STFS n'a pas été ouvert ; le
`default.xex` interne sera par ailleurs chiffré/compressé XEX2. Deux outils manquent :
un extracteur STFS et un décodeur XEX2.

---

## 5. `APM3_US` → Sega ALLS/APM3, **deux jeux**

Le fichier `exe VF5ES.txt` fourni dans le dump indique lui-même le choix d'exécutable :

```
Version VF5 eSport          -> esport/runtime/media/eve.exe
Version Ultimate Showdown   -> esport/runtime/media/vf5fs/vfes.exe
```

| Élément | Valeur |
|---|---|
| Plateforme | **Windows x64** (PE), pas Linux |
| Couche arcade | `apm.dll` / `apm_x86.dll`, `apmgamepad.dll` |
| Jeu A | `eve.exe` (33,96 Mo) + données `.par` (archives moteur Dragon, nom de code **`adam`**) |
| Jeu B | `vfes.exe` (1,99 Mo) + `vf5fs-pxd-w64-Retail_APM3.dll` (6,97 Mo) + `vf5fs_media/` |

Bloc de version de `vf5fs-pxd-w64-Retail_APM3.dll` :

```
D:/Project/vf5/vf5fscs_source/20120711_update_1.1/vf5fs
2016-06-30T14:58:25+09:00        <- construction du portage
atsu_takashi                     <- auteur du build
2012-07-04T18:06:57+09:00        <- snapshot de la source VF5FS
Virtua Fighter5 Final Showdown
6.000 / VERSION A / REVISION 1
```

**Conclusions :**

- La plateforme est un système **Windows x64** de type ALLS/APM3. Confiance : **CONFIRMED**.
- `vfes.exe` n'est pas une réimplémentation : il pilote le **moteur VF5FS d'origine**
  encapsulé dans `vf5fs-pxd-w64-Retail_APM3.dll`, portage 2016 d'un snapshot de la branche
  **console** (`vf5fscs_source`, mise à jour 1.1 du 2012-07-11), release **6.000**.
  Confiance : **CONFIRMED**.
- `eve.exe` et les `.par` relèvent d'une technologie différente (archives et nomenclature du
  moteur Dragon de RGG). Confiance : **LIKELY** — le format `.par` et le nom de code `adam`
  le suggèrent fortement, mais l'exécutable n'a pas encore été analysé.

---

## 6. `PC_REVO` → Virtua Fighter 5 R.E.V.O. World Stage (Steam)

| Élément | Valeur |
|---|---|
| Exécutable | `VFREVO.exe`, 48,84 Mo, ressource version `1.0.0.0` |
| Produit / éditeur | `Virtua Fighter 5 R.E.V.O. World Stage` / `SEGA` |
| Moteur de combat | `vf5fs/vf5fs-pxd-w64-d3d12_SteamRetail.dll`, 7,22 Mo |
| Protections / SDK | EasyAntiCheat, `EOSSDK-Win64-Shipping.dll`, `steam_api64.dll`, `start_protected_game.exe` |
| Rendu | D3D12 + DLSS / FSR3 / XeSS |

Bloc de version du DLL : **identique à celui d'`APM3_US`** — même chemin de build
`D:/Project/vf5/vf5fscs_source/20120711_update_1.1/vf5fs`, même portage `2016-06-30`,
même auteur, même release **6.000 / VERSION A / REVISION 1**.

**Conclusions :**

- R.E.V.O. embarque le **même moteur VF5FS porté** qu'Ultimate Showdown arcade.
  Confiance : **CONFIRMED** (bloc de version identique dans les deux DLL).
- Le jeu ship **deux jeux de données de gameplay** : `vf5fs_media/rom/` (jeu FS d'origine) et
  `vf5fs_media/rom_200/` (rééquilibrage « 2.00 »). Confiance : **CONFIRMED**.
- `VFREVO.exe` est l'enveloppe moderne (shell, réseau, rendu) ; la simulation de combat est
  dans le DLL. Confiance : **SUPPORTED** — la séparation des fichiers et le contenu du DLL
  le montrent, mais le flux d'appel n'a pas encore été tracé.

---

## Récapitulatif

| ID | Verdict | Confiance |
|---|---|---|
| LIND_FS | VF5FS **Rev A**, release 2.000, 2010-06-28, Lindbergh | CONFIRMED |
| APM3_FS | VF5FS **Rev B ver 6.0000**, release 6.000, 2011-10-17, **Lindbergh** | CONFIRMED |
| PS3_FS | VF5FS PS3 `NPEB00913` v01.00 (EU) ; build interne inconnu | CONFIRMED / UNKNOWN |
| X360_FS | VF5FS X360 `584111FE` + TU1 ; build interne inconnu | CONFIRMED / UNKNOWN |
| APM3_US | ALLS/APM3 Windows : VF5 eSports (`eve.exe`) + Ultimate Showdown (moteur FS 6.000 porté en 2016) | CONFIRMED |
| PC_REVO | R.E.V.O. World Stage 1.0.0.0 ; même moteur FS 6.000 porté ; données `rom/` + `rom_200/` | CONFIRMED |
