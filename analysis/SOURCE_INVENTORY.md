# SOURCE_INVENTORY — inventaire complet des sources

Généré par `tools/inventory_sources.py`. Le détail fichier par fichier (chemin, taille, type
détecté **par signature** et non par extension, SHA-256) est dans `analysis/inventory/*.csv`.

---

## LIND_FS — Lindbergh Rev A

Une seule archive à l'origine : `vf5fs.7z` (5,00 Go), contenant deux **images de partition
ext3 brutes** (magie `0xEF53` à l'offset `0x438`) :

| Image | Taille | Contenu |
|---|---:|---|
| `vf5fs.bin` | 2 998 927 360 o | `/home` complet : `disk0`…`disk9`, plus `run.sh`, `debug.sh`, `runxbox.sh` |
| `vf5fs_ext.bin` | 3 250 585 600 o | `rom/objset/` : 86 fichiers, modèles de décors et personnages |

Arborescence utile de `vf5fs.bin` (partition `/home`) :

```
disk1/vf5              ELF principal, 11 867 956 o
disk1/game             script de lancement
disk1/libalpb.so  libsama.so  libbdlog.so
disk1/rom/             donnees de jeu (rob, 2d, sound, auth_3d, light_param, …)
disk1/drv/nvidia/8769/ pilote NVIDIA Linux 8769 (sources + .ko + libGL/GLU/glut/X11)
```

`vf5fs_ext.bin` contient les archives de décors (`stgare`, `stgaur`, `stgban`, `stgcas`,
`stgdjo`, `stggym`, `stghai`, `stgjin`, `stgnyc`, `stgriv`, `stgsin`, `stgslk`, `stgsmo`,
`stgtak`, `stgtan`, `stgter`, `stgts2`, `stgts3`, `stgtst`, `stgumi`, `stgyuk`, `stgevo00`…`09`)
et les archives d'objets par personnage (`takitm.farc` 105 Mo, `vanitm.farc` 121 Mo,
`wolitm.farc` 120 Mo, …), plus `tex_db.bin`. **Tous datés du 2010-06-28.**

Listings complets : `analysis/inventory/LIND_vf5fs_bin.listing.txt` (6,2 Mo) et
`LIND_vf5fs_ext_bin.listing.txt`.

**C'est la seule source du projet qui contienne une révision arcade complète et cohérente.**

---

## APM3_FS — Lindbergh Rev B ver 6.0000 (partition `/home/disk1` déjà extraite)

8 951 fichiers, 5,88 Go.

| Extension | Nombre | Volume | Nature |
|---|---:|---:|---|
| `.adx` | 5 398 | 944,8 Mo | audio CRI ADX |
| `.farc` | 851 | 3 956,2 Mo | archives FARC (757 compressées `FArC`, 95 brutes `FArc`) |
| (sans ext.) | 686 | 17,4 Mo | dont l'ELF `vf5`, scripts, bibliothèques |
| `.bin` | 618 | 68,3 Mo | tables binaires (`mothead_`, `ctrl_`, `*_COLI`, `tex_db`) |
| `.h` | 413 | 4,2 Mo | en-têtes — **du pilote NVIDIA**, pas du jeu |
| `.csb` | 104 | 387,8 Mo | banques sonores CRI |
| `.sfd` | 7 | 523,5 Mo | vidéos Sofdec |
| `.so` / `.ko` / `.a` | 132 | 52,3 Mo | bibliothèques et modules noyau |

Types détectés par signature : 757 `FArC`, 95 `FArc`, 182 `ELF32 LE DYN x86`,
52 `ELF32 LE REL x86`, 10 `ELF32 LE EXEC x86`, 18 scripts shell, 2 gzip.

Répartition par répertoire :

| Répertoire | Fichiers | Volume | Contenu |
|---|---:|---:|---|
| `rom/objset` | 104 | 3 357,3 Mo | modèles 3D (décors, personnages, objets) |
| `rom/sound` | 3 455 | 1 068,8 Mo | ADX / CSB |
| `rom/2d` | 1 115 | 454,2 Mo | interface, sprites |
| `rom/tv` | 2 026 | 426,2 Mo | contenus VF.NET / satellite |
| `rom/movie` | 2 | 345,0 Mo | Sofdec |
| **`rom/rob`** | **89** | **120,5 Mo** | **données de combat — voir ci-dessous** |
| `drv/nvidia` | 1 677 | 90,0 Mo | pilote NVIDIA 8769 |
| `rom/auth_3d` | 95 | 56,2 Mo | mises en scène 3D |
| `rom/ibl` | 42 | 22,2 Mo | éclairage image-based |
| `rom/terminal` | 35 | 16,4 Mo | terminal arcade |
| `rom/light_param` | 164 | 0,1 Mo | `fog_/glow_/light_/wind_` × 41 décors, en texte |
| `rom/rob_ai` | 27 | 1,1 Mo | `ai_data_2500…2740.txt`, `kotrial_enemy_data.txt` — **en texte** |
| `rom/replay` | 8 | 0,1 Mo | démonstrations |
| `tools/lindbergh` | 5 | 0,4 Mo | `mfetcherd`, `gdeliver.conf.tmpl`, `patch` |

### `rom/rob/` — le cœur du gameplay

| Motif | Nombre | Rôle |
|---|---:|---|
| `mothead_<CHR>.bin` | 21 (20 + `CMN`) | **en-têtes de mouvement** — la donnée de coups |
| `ctrl_<CHR>.bin` | 20 | **tables de commandes** — saisie → mouvement |
| `mot_<CHR>.farc` | 22 | animations |
| `mot_AUTH_<CHR>.farc` | 21 | animations de mise en scène |
| `mot_db.farc` | 1 | base de données de mouvements |
| `rob_mot_tbl.bin` | 1 | table d'indexation des mouvements |

Fichiers racine complémentaires : `bone_data.bin` (squelettes), `chritm_tbl.farc`,
`cid_table.farc`, `gm_itm_tbl.farc`, `gm_chip_tbl.farc`, `live_data.farc`, `sp_title_tbl.bin`,
`code_map.bin`, `iet.bin`, `shader.farc`, et 41 fichiers `STG*_COLI*.bin`
(**collisions de décor**, un par arène).

---

## PS3_FS — PlayStation 3

Deux fichiers d'origine : le PKG retail (2 049 389 840 o) et le `.rap` de licence (16 o).
Le PKG a été dépaqueté par `tools/unpack_ps3_pkg.py` : **375 éléments**.

Racine : `PS3LOGO.DAT`, `PARAM.SFO`, `ICON0.PNG`, `ICON1.PAM`, `PIC0.PNG`, `PIC1.PNG`.

```
USRDIR/EBOOT.BIN            3 783 280 o   SELF NPDRM chiffre  <-- verrou
USRDIR/chkboot.edat
USRDIR/ps3/SYSTEM.farc, REPLAY.farc, shader_cg.farc (17,3 Mo)
USRDIR/rom.psarc            62 938 004 o  archive PlayStation
USRDIR/rom/2d/              spr_c_mch<chr>.farc (19 personnages) + spr_n_*
USRDIR/rom/rob/             45 archives d'animation mot_*.farc
USRDIR/rom/sound/bgm , voice
USRDIR/rom/objset , movie
```

Point notable : `rom/rob/` **ne contient pas** les `mothead_*.bin` ni les `ctrl_*.bin` sur
PS3. Ils sont vraisemblablement dans `rom.psarc`. Confiance : **LIKELY** — à vérifier en
phase 5. Les shaders sont en **Cg** (`shader_cg.farc`), pas en ARB comme sur Lindbergh.

---

## X360_FS — Xbox 360

Deux conteneurs **STFS** (signature `LIVE`), non ouverts à ce stade :

| Fichier | Taille | Nom affiché |
|---|---:|---|
| `584111FE/000D0000/7D2DF36BD11FB8394C3D652339E6FE1DA1337B1058` | 2 051 182 592 o | `Virtua Fighter 5 FS` |
| `TU_1C424FU_0000004000000.0000000000081` | 729 088 o | `Virtua Fighter 5 FS Title Upda…` |

**Outils manquants : un extracteur STFS, puis un décodeur XEX2.** Le contenu de cette source
est donc entièrement `UNKNOWN` au-delà de l'identification du titre.

---

## APM3_US — Sega ALLS/APM3 (Windows x64), deux jeux

1 059 fichiers, 10,76 Go.

| Extension | Nombre | Volume | Nature |
|---|---:|---:|---|
| `.par` | 52 | 8 746,2 Mo | archives moteur Dragon (RGG) |
| `.adx` | 737 | 1 165,9 Mo | audio CRI |
| `.usm` | 6 | 1 015,9 Mo | vidéo CRI |
| `.dds` / `.bmp` | 58 | 23,3 Mo | textures |
| `.exe` / `.dll` | 7 | 43,3 Mo | code |
| `.cud`, `.bin`, `.gmt`, `.cmt`, `.json`, `.acf` | 187 | 12,2 Mo | données |

Exécutables et bibliothèques :

```
runtime/media/eve.exe                          33,96 Mo   VF5 eSports (moteur Dragon)
runtime/media/apm.dll , apm_x86.dll             2,22 Mo   couche materielle APM3
runtime/media/apmgamepad.dll , _x86.dll         0,12 Mo   entrees
runtime/media/vf5fs/vfes.exe                    1,99 Mo   Ultimate Showdown (hote)
runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll  6,97 Mo   moteur VF5FS porte
```

Les `.par` portent le nom de code **`adam`** (`cubemap_adam.par`, `entity_adam.par`,
`db.adam.ja.par`, `light_anim_adam.par`) ; les plus gros sont `chara.par` (1 782 Mo) et
`motion.par` (266 Mo).

---

## PC_REVO — R.E.V.O. World Stage (Steam)

6 699 fichiers, 20,60 Go.

| Chemin | Fichiers | Volume |
|---|---:|---:|
| `runtime/media/data` | 5 507 | 12 574,8 Mo |
| **`runtime/media/vf5fs`** | **975** | **7 657,8 Mo** |
| `runtime/dlc/wallpaper` | 135 | 488,1 Mo |
| `runtime/dlc/secret_materials` | 2 | 37,9 Mo |
| `runtime/media/reshade-shaders` | 20 | 32,0 Mo |

`runtime/media/data` contient les `.par` du moteur moderne (58 archives, 14,4 Go) : c'est
l'enveloppe R.E.V.O. `runtime/media/vf5fs` contient le moteur FS porté **et son arbre `rom/`
d'origine** :

```
vf5fs/vf5fs-pxd-w64-d3d12_SteamRetail.dll   7,22 Mo
vf5fs/EOSSDK-Win64-Shipping.dll
vf5fs/vf5fs_media/rom/rob        91 fichiers  121,1 Mo   <- donnees FS d'origine
vf5fs/vf5fs_media/rom/sound     804 fichiers  1 563,3 Mo
vf5fs/vf5fs_media/rom/movie       7 fichiers  2 115,9 Mo
vf5fs/vf5fs_media/rom_200/rob    41 fichiers    4,9 Mo   <- reequilibrage 2.00
vf5fs/vf5fs_media/rom_200/training , chritm_tbl.farc , resident.farc , string_array.farc
vf5fs/vf5fs_media/w64/shader_pxd_w64.farc , shader_pxd_w64_d3d12.farc
```

52 archives **FARC** (le format Lindbergh) coexistent avec les `.par` modernes. Les fichiers
`resident.farc.r2421` et `.r2427` semblent être des variantes de révision conservées.

R.E.V.O. ajoute deux personnages non présents sur Lindbergh :
`ctrl_DUR_cpu.bin` et `mothead_DUR_cpu.bin` (variante CPU de Dural).
