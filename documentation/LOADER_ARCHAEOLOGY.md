# LOADER_ARCHAEOLOGY — ce que les loaders nous apprennent sur VF5FS

Objectif (§7 du cahier des charges) : les loaders **ne sont pas le moteur du jeu**. Leur
intérêt est de nous dire **ce que Final Showdown attend de son environnement**, et de nous
fournir des points d'ancrage vérifiables dans le binaire.

Source étudiée en profondeur : `lindbergh-loader/lindbergh-loader`, cloné en local dans
`tools/loaders/lindbergh-loader` (clone superficiel, lecture seule).

---

## 1. Le loader identifie le jeu par CRC32 de l'ELF

`hook.c:1629` :

```c
elf_crc = getCrc32((void *)(size_t)(info->dlpi_addr + info->dlpi_phdr[2].p_vaddr + 10), 0x4000);
```

`phdr[2]` est le premier segment `PT_LOAD` (`p_vaddr = 0x08048000`, `p_offset = 0`), donc la
zone hachée est **`fichier[0x0A … 0x400A]`**. `getCrc32` (`hook.c:167`) est un CRC-32
standard (polynôme réfléchi `0xEDB88320`, init `0xFFFFFFFF`, complément final).

Table de `config.h:81-83` :

| Constante | CRC32 | Média | Game ID |
|---|---|---|---|
| `VIRTUA_FIGHTER_5_FINAL_SHOWDOWN_REVA` | `0xBAE2BE62` | DVP-5019A | SBUV |
| `VIRTUA_FIGHTER_5_FINAL_SHOWDOWN_REVB` | `0x7CEE1D81` | DVP-5020 | SBXX |
| `VIRTUA_FIGHTER_5_FINAL_SHOWDOWN_REVB_6000` | `0x034C0D02` | DVP-5020 ver 6.00 | SBXX |

Nos deux binaires tombent exactement sur deux de ces entrées — voir `VERSIONS.md`.
Le loader connaît aussi `VF5` (SBLM, DVP-0008, Rev A/B/E), `VF5 Export` (DVP-0043) et
`VF5R` (SBQU, Rev D / Rev G) : ce sont les cibles futures de `HISTORICAL_LINEAGE.md`.

---

## 2. Adresses connues dans **notre** binaire Rev B 6.0000

`patch.c:3091-3125`, cas `VIRTUA_FIGHTER_5_FINAL_SHOWDOWN_REVB_6000`. Ces adresses ont été
établies par la communauté indépendamment de notre analyse.

| Adresse | Rôle d'après le loader | Nature |
|---|---|---|
| `0x088B1866` | `amDongleInit` | fonction |
| `0x088B0321` | `amDongleIsAvailable` | fonction |
| `0x088B0D17` | `amDongleUpdate` | fonction |
| `0x088B00B4` | `amDipswInit` | fonction |
| `0x088B0138` | `amDipswExit` | fonction |
| `0x088B01AD` | `amDipswGetData` | fonction |
| `0x088B0223` | `amDipswSetLed` | fonction |
| `0x093CE7C8` | `amDipswContext` | global |
| `0x08052B20` | site d'appel `glProgramStringARB` | fonction |
| `0x081489F7`, `0x08148BC8`, `0x081492C0`, `0x081494D0` | quatre points du calcul d'exposition (`hookVf5FSExposure`) | fonctions |
| `0x080E4FF5`, `0x081084D5` | sauts conditionnels forcés (`EB`) — contournement de vérification | octet |
| `0x081229F4` | octet `05` — contournement de vérification | octet |
| `0x0812326E` | fonction neutralisée (`stubReturn`) — vérification réseau | fonction |

### Validation croisée effectuée

Le loader réécrit sept chaînes de chemin. J'ai vérifié chacune contre mon extraction
indépendante des chaînes du binaire (`analysis/strings_vf5_lind.txt`) :

| Adresse patchée | Chaîne attendue | Chaîne trouvée à cette adresse |
|---|---|---|
| `0x088CD42A` | `/home/disk2/ram/to.txt` | identique ✓ |
| `0x088CD441` | `/home/disk2/ram/from.txt` | identique ✓ |
| `0x088CD45A` | `/home/disk2/ram/.tmp` | identique ✓ |
| `0x088CD48D` | `/home/disk2/ram` | identique ✓ |
| `0x088CD49D` | `/home/disk2/foo1` | identique ✓ |
| `0x088CD4AE` | `/home/disk2/foo2` | identique ✓ |

Six correspondances exactes à l'octet près. **Confiance : CONFIRMED** — la table du loader
décrit bien le binaire que nous détenons, et son espace d'adressage est directement
utilisable comme amorce pour Ghidra.

---

## 3. Ce que le loader doit fournir — donc ce que le jeu exige

Modules de `src/lindbergh/` et ce qu'ils révèlent des attentes du jeu :

| Module | Ce que le jeu attend |
|---|---|
| `baseBoard.c` | un périphérique carte de base Lindbergh (`/dev/lbb`) |
| `jvs.c` / `jvs.h` | un bus JVS sur port série pour entrées, pièces, sorties générales |
| `securityBoard.c` | un dongle de sécurité et sa carte |
| `eeprom.c`, `eepromSettings.c` | une EEPROM de sauvegarde des réglages |
| `cardReader.c` | un lecteur de cartes (P-ras / VF.NET) |
| `patchNetwork.c` | un réseau ALL.Net joignable |
| `glutHooks.c`, `glxHooks.c`, `x11Hooks.c` | GLUT + GLX + X11 comme couche de fenêtrage |
| `shaderPatches.c`, `shaderWork/vf5.c` | des shaders ARB `NV_*` propres au GPU NVIDIA d'origine |
| `resolution.c` | un mode natif 1280×768 |
| `libsegaapi/libsegaapi.c` | l'API son Sega (voir `API_MATRIX.md`) |
| `libposixtime` | des primitives de temps POSIX de l'époque |

`shaderWork/vf5.c` (22,6 Ko) existe spécifiquement parce que VF5/VF5FS emploie des programmes
de shader ARB dépendant d'extensions NVIDIA ; sur un GPU non-NVIDIA le loader doit les
réécrire. **Le renderer de VF5FS est donc lié au matériel NVIDIA de la Lindbergh.**
Confiance : **SUPPORTED**.

`hookVf5FSExposure` est propre à VF5FS : quatre fonctions du calcul d'exposition/bloom
doivent être détournées hors NVIDIA. Ce sont des points d'entrée directs vers le renderer,
à documenter en phase « rendering ».

---

## 4. Ce que le loader ne nous apprend pas

- Il ne dit rien du **game loop**, du moteur de combat, ni des formats de données.
- Il ne modélise pas `libalpb.so` / `libsama.so` / `libbdlog.so`, qui sont fournies telles
  quelles par le dump.
- Les fonctions `amJvs*`, `amDongle*`, `amDipsw*` sont **statiquement liées dans `vf5`** :
  elles n'apparaissent pas dans `.dynsym`. Le loader les détourne en mémoire, ce qui confirme
  qu'elles font partie du binaire du jeu, pas d'une bibliothèque partagée.

---

## 5. Dépôts restant à étudier

Le cahier des charges cite quatre autres dépôts. Ils n'ont pas encore été examinés :

| Dépôt | Intérêt attendu | État |
|---|---|---|
| `lindbergh-loader/linuxloader` | chargement ELF, environnement Linux d'époque | non étudié |
| `zognic/lindbergh-install` | image système, partitionnement `/home/diskN` | non étudié |
| `JayFoxRox/Lindbergh-Emulator` | ancienne approche, `ElfLdr`, `OpenSegaAPI` | non étudié |
| `teknogods/TeknoParrot` | couche arcade Windows, éventuellement APM3/ALLS | non étudié |

Priorité suggérée : `lindbergh-install` (pour comprendre la disposition `/home/disk0..disk9`
qui explique le script `game` de nos deux dumps), puis `Lindbergh-Emulator` pour
`OpenSegaAPI`. `TeknoParrot` deviendra pertinent au moment d'`APM3_US`.
