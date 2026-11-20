# INITIAL_REPORT — phase 0 et phase 1

Projet : rétro-ingénierie de la famille Virtua Fighter 5, cible principale **Final Showdown
arcade**. Rapport obligatoire avant toute décompilation de masse (§34).

Espace de travail : `C:\Users\frede\Desktop\VF5RE\`
Sources : lues, jamais modifiées. Les extractions vont dans `VF5RE\extracted\`.

> **Ce rapport couvre les phases 0 et 1 et reste valide.** Les travaux menés depuis
> (formats de données, désassemblage) sont documentés dans `docs/formats/` et résumés dans
> `REPRISE.md` à la racine de l'espace de travail. **`REPRISE.md` fait foi sur l'état
> courant** ; ce rapport-ci fait foi sur l'inventaire et l'identification des versions.

---

## 1. Quelles sources locales existent réellement ?

Les six chemins annoncés existent tous. Aucune source absente n'a été supposée.
`ARCADE_FS_REVA/REVB/REVB_60000`, `UM_PS4`, `UM_PS5`, `VF5R_ARCADE`, `VF5_ARCADE` n'existent
pas en tant que répertoires distincts — mais **les deux révisions arcade sont bien présentes**,
sous d'autres noms (voir §4).

| ID | Fichiers | Volume | État |
|---|---:|---:|---|
| LIND_FS | 1 archive → 2 images ext3 | 5,00 → 6,25 Go | ouvert |
| APM3_FS | 8 951 | 5,88 Go | déjà extrait |
| PS3_FS | 2 → 375 éléments | 1,91 Go | dépaqueté |
| X360_FS | 1 archive → 2 conteneurs STFS | 1,85 Go | **non ouvert** |
| APM3_US | 1 059 | 10,76 Go | déjà extrait |
| PC_REVO | 6 699 | 20,60 Go | installé |

### Deux étiquettes trompeuses, corrigées

- **`APM3_FS` n'est pas un dump APM3 : c'est du Lindbergh.** ELF32 `EM_386`,
  `DT_NEEDED libsegaapi.so`, GLUT/GLX, toolchain MontaVista, `.gdbinit` en registres `eax`,
  `tools/lindbergh/`, `alpbExGetLindberghSerialID`, classes `CriSoundRendererLindbergh`.
  C'est le contenu de la partition `/home/disk1` d'un disque Lindbergh. **CONFIRMED.**
- **`APM3_US` contient deux jeux** : `eve.exe` (VF5 eSports) et `vf5fs/vfes.exe`
  (Ultimate Showdown), sur base **Windows x64**, pas Linux. **CONFIRMED.**

---

## 2. Quels fichiers contiennent-elles ?

Détail complet : `SOURCE_INVENTORY.md` et `analysis/inventory/*.csv`.
L'essentiel pour la suite :

- `APM3_FS/rom/rob/` — 89 fichiers, 120,5 Mo : `mothead_<CHR>.bin` (données de coups),
  `ctrl_<CHR>.bin` (commandes), `mot_<CHR>.farc` (animations), `rob_mot_tbl.bin`,
  `mot_db.farc`, plus `bone_data.bin` à la racine de `rom/`.
- 41 fichiers `STG*_COLI*.bin` : collisions de décor, une par arène.
- `rom/rob_ai/` : 27 fichiers **texte** (`ai_data_2500…2740.txt`) — l'IA est configurée en clair.
- `rom/light_param/` : 164 fichiers **texte** (`fog_`, `glow_`, `light_`, `wind_` × 41 décors).
- Format d'archive propriétaire **FARC** (`FArc` brut, `FArC` compressé zlib), 851 occurrences.
- Audio et vidéo : middleware **CRI** (`.adx`, `.csb`, `.sfd`, `.usm`).

---

## 3. Quels hashes ont été calculés ?

Voir `MANIFEST.md` : 24 fichiers importants hachés intégralement en SHA-256, plus un inventaire
complet de 18 000+ fichiers dans `analysis/inventory/*.csv`.

Fait notable : `libalpb.so`, `libsama.so` et `libbdlog.so` sont **identiques octet pour octet**
entre Rev A et Rev B 6.0000 — l'environnement arcade n'a pas bougé entre les deux révisions.

---

## 4. Quelles versions sont présentes ? Quelle révision arcade ?

Détail et preuves : `VERSIONS.md`. Chaque révision arcade est identifiée par **deux signaux
indépendants** : le bloc de version interne du binaire, et le CRC32 utilisé par
`lindbergh-loader` (calculé sur `fichier[0x0A…0x400A]`).

| Source | Révision | Release | Construit le | CRC32 | Confiance |
|---|---|---|---|---|---|
| `LIND_FS` | **VF5FS Rev A** (DVP-5019A, SBUV) | 2.000 | 2010-06-28 | `0xBAE2BE62` | CONFIRMED |
| `APM3_FS` | **VF5FS Rev B ver 6.0000** (DVP-5020, SBXX) | 6.000 | 2011-10-17 | `0x034C0D02` | CONFIRMED |
| `PS3_FS` | `NPEB00913` v01.00 (PSN Europe) | — | — | — | CONFIRMED |
| `X360_FS` | Title `584111FE` + TU1 | — | — | — | CONFIRMED |
| `APM3_US` | moteur FS 6.000, portage 2016-06-30 | 6.000 | 2016-06-30 | — | CONFIRMED |
| `PC_REVO` | `VFREVO.exe` 1.0.0.0 ; moteur FS 6.000, même portage | 6.000 | 2016-06-30 | — | CONFIRMED |

**Nous disposons donc de deux révisions arcade complètes et distinctes** — exactement ce que
demande la phase 7 (comparaison de révisions), disponible dès maintenant.

Anomalie à résoudre : le script `game` de `APM3_FS` porte `gameid=SBUV` (identifiant Rev A)
alors que son binaire est la Rev B 6.0000. **UNKNOWN.**

---

## 5. Quels ELF existent, quelle architecture, quel est l'ELF principal ?

**ELF principal : `vf5`**, unique exécutable du jeu, dans les deux révisions.

| | Rev A (`LIND_FS/disk1/vf5`) | Rev B 6.0000 (`APM3_FS/vf5`) |
|---|---|---|
| Classe | ELF32 LE `EXEC` `EM_386` | ELF32 LE `EXEC` `EM_386` |
| Taille | 11 867 956 o | 12 038 036 o |
| Entrée | `0x080542E0` | `0x08054380` |
| `.text` | — | `0x08054380`, `0x00868B08` (8,8 Mo) |
| `.rodata` | — | `0x088CC540`, `0x001A2940` |
| `.data` / `.bss` | — | `0x08BA05C0` / `0x08BB2640` (`0x0081CFC0`) |
| `.symtab` | absent | **absent (0 symbole)** |
| `.dynsym` | — | 762 entrées (imports seulement) |

Autres ELF du dump `APM3_FS` : 182 `DYN` (bibliothèques partagées), 52 `REL` (dont les modules
noyau NVIDIA), 10 `EXEC` — presque tous appartiennent au pilote NVIDIA ou aux outils système,
pas au jeu.

**Anomalie à traiter en priorité : la section `PSFD00`**, type `PROGBITS`, à `0x088BCE88`,
62 Ko, placée entre `.text` et `.fini` dans le segment exécutable. Nom hors convention.
**UNKNOWN** — à identifier avant toute décompilation de masse.

---

## 6. Quelles bibliothèques sont utilisées ?

18 `DT_NEEDED` : `libalpb.so`, `libsama.so`, `libbdlog.so`, `libpcsclite.so.1`,
`libsegaapi.so`, `libglut.so.3`, `libGLU.so.1`, `libGL.so.1`, `libXmu.so.6`, `libXext.so.6`,
`libX11.so.6`, `libz.so.1`, `libm.so.6`, `libgcc_s.so.1`, `libpthread.so.0`, `libc.so.6`,
`libdl.so.2`, `libstdc++.so.6`. `DT_RPATH = "."`.

Compilé avec **GCC 3.4.3 MontaVista** (aussi 3.3.1 pour certains objets), d'après `.comment`.

Répartition des 421 imports : 163 OpenGL, 30 GLUT, 24 `alpbEx*`, 22 `SEGAAPI_*`, 2 GLU,
1 X11, le reste en libc/libstdc++/libm/libpthread/libz/libdl. Détail : `API_MATRIX.md`.

---

## 7. Qu'est-ce qui relève de Lindbergh, du moteur, du tiers ?

Classification complète : `CODE_CLASSIFICATION.md`, établie sur 168 types RTTI démanglés et
les chaînes `__PRETTY_FUNCTION__` résiduelles.

- **GAME** — l'entité combattante s'appelle **`Rob`**. Tâches clés : `TaskRobBase`,
  `TaskRobCtrl`, `TaskRobCollision`, `TaskRobColliAttack`, `TaskRobMotionModifier`,
  `TaskRobPrepareAction`, `TaskRobAI`. Arbitrage : `TaskGameVs`, `TaskGameVsJudge`,
  `TaskGameVsRoundNo`, `TaskGameVsWinner`.
- **MOTEUR SEGA** — bibliothèque socle `prj::` (avec **sa suite de tests unitaires embarquée
  dans le binaire de production**), système de tâches (`Task`, `SysFrameRate`), `a3d::`
  (auth_3d), `AetMgr` (2D), 22 classes `TaskEffect*`, couche `File::` + FARC, et une boîte à
  outils de débogage `dw::` avec des panneaux d'inspection de mouvements (`DataTestMotDw`,
  `RobTraceDw`).
- **LINDBERGH / ARCADE** — `test_mode::` (~45 classes nommant les réglages de gameplay),
  `terminal::` et `tv::` (VF.NET), `BackupRamDevice`, `TaskIcrw`, et les fonctions
  **liées statiquement** `amJvs*`, `amDongle*`, `amDipsw*`.
- **TIERS** — middleware **CRI** (CriFs, CriAu/ADX2, CriSr avec back-end
  `CriSoundRendererLindbergh`), libstdc++/libc MontaVista, zlib, GLUT/GLU/GL/X11.

---

## 8. Quels loaders éclairent les interfaces ?

`lindbergh-loader` a été cloné et lu (`LOADER_ARCHAEOLOGY.md`). Apport principal : il fournit
**des adresses vérifiées dans notre binaire Rev B 6.0000** — huit fonctions arcade, un global,
le site d'appel `glProgramStringARB`, et quatre fonctions du calcul d'exposition.

Ces adresses ont été **validées de façon indépendante** : le loader réécrit sept chaînes de
chemin à des adresses précises ; j'ai vérifié six d'entre elles contre mon extraction de
chaînes, avec correspondance exacte (`0x088CD42A` = `/home/disk2/ram/to.txt`, etc.).
Voir `analysis/functions.csv` pour les 17 premières entrées de la base de fonctions.

Les trois autres dépôts cités (`linuxloader`, `lindbergh-install`, `Lindbergh-Emulator`) et
`TeknoParrot` n'ont **pas** encore été étudiés.

---

## 9. Qu'est-ce qui est comparable entre les versions ?

`MODERN_DATA_LINEAGE.md` et `comparisons/rob_data_matrix.csv`. Résultat central, mesuré au
SHA-256 intégral :

- **Rev A → Rev B 6.0000 : refonte du gameplay.** Aucun des 21 `mothead_*.bin` ni des 20
  `ctrl_*.bin` ne survit ; 18 animations sur 26 changent.
- **Arcade 6.0000 → R.E.V.O. (2025) : 20 `mothead_` sur 21 et 19 `ctrl_` sur 20 sont
  identiques bit à bit**, ainsi que `rob_mot_tbl.bin`. Seul Dural diffère, et sur ce point
  R.E.V.O. suit la PS3.
- **Ultimate Showdown et R.E.V.O. embarquent le moteur FS lui-même** : leurs DLL
  `vf5fs-pxd-w64-*` portent le même bloc de version — source `vf5fscs_source/20120711_update_1.1`,
  snapshot 2012-07-04, portage 2016-06-30, release **6.000 / VERSION A / REVISION 1**.

Conséquence stratégique : **`vf5fs-pxd-w64-d3d12_SteamRetail.dll` (7,22 Mo, x64) est le même
code que l'ELF Lindbergh**, dans une forme bien plus facile à décompiler. C'est une pierre de
Rosette utilisable dès la phase 3, avant même PS3 et X360.

---

## 10. Ce qui bloque, et ce qu'il faut pour débloquer

| Verrou | Source | Ce qu'il faut |
|---|---|---|
| `EBOOT.BIN` est un SELF NPDRM chiffré (`SCE\0`, clé rév. `0x0019`) | PS3_FS | déchiffreur SCE + klicensee (le `.rap` fourni la contient) |
| Conteneur STFS non ouvert | X360_FS | extracteur STFS, puis décodeur XEX2 |
| `rom.psarc` non ouvert | PS3_FS | dépaqueteur PSARC |
| ~~`.par` non ouverts~~ | APM3_US, PC_REVO | **levé** — `tools/PARtool v1.3.windows-x64/ParTool.exe` fonctionne |
| ~~`.farc` non ouverts~~ | toutes | **levé** — `tools/farc.py`, format documenté dans `docs/formats/farc.md` |
| Section `PSFD00` non identifiée | APM3_FS | analyse en désassemblage |

---

## 11. Questions ouvertes

Mise à jour au fil des travaux. Les questions résolues depuis sont barrées, avec le renvoi.

1. Que contient la section `PSFD00` ? Protection, code généré, données ?
2. Pourquoi le script `game` de la Rev B 6.0000 porte-t-il `gameid=SBUV` (identifiant Rev A) ?
3. Où est la boucle principale ? GLUT fournit-il la boucle, ou le jeu la pilote-t-il ?
   Indices : 30 imports GLUT, classe `SysFrameRate`, tâche `TaskPlayFrameSpeed`.
4. ~~Quelle est la structure de `mothead_*.bin` ?~~ **Partiellement résolue** —
   en-tête et bloc `CCD` décodés et vérifiés sur 85 fichiers, voir `docs/formats/mothead.md`.
   Reste : la section 1 (les mouvements eux-mêmes) et le sens des paires de 8 octets du CCD.
   Ce n'est **pas** une structure à enregistrements fixes, contrairement à l'hypothèse initiale.
5. `mothead_` contient-il les hitboxes, ou sont-elles ailleurs
   (`TaskRobColliAttack`, `bone_data.bin`) ?
6. `libsama.so` et `libbdlog.so` sont déclarées mais aucun de leurs symboles n'est importé :
   dépendances de `libalpb.so`, ou chargées par `dlopen` ?
7. Le `mothead_` de la PS3 est-il dans `rom.psarc`, et est-il identique à celui de l'arcade ?
8. `VFREVO.exe` partage-t-il du code avec FS, ou est-ce une enveloppe entièrement séparée ?
9. Les 41 `STG*_COLI*.bin` décrivent-ils les murs et le ring-out ? Le nom
   `STGBAN_COLI_wall.000.bin` le suggère. On sait maintenant qu'ils sont aussi empaquetés
   dans `rom_200/resident.farc` de R.E.V.O.
10. `rom/rob_ai/*.txt` est en clair : quel est son langage, et qui le lit (`TaskRobAI`) ?
    Le chargeur est identifié côté R.E.V.O. : `0x1800942C8`.
11. Que représente la constante flottante `10.0` que R.E.V.O. 2.00 passe à `13.0` pour
    **les 21 personnages** ? Voir `docs/formats/mothead.md`.
12. Que contiennent les enregistrements de 96 octets de `yarare.bin` ?
    Voir `docs/formats/mot_tables.md`.
13. Que signifient les préfixes des noms d'os (`n_`, `e_`, `kl_`, `kg_`, `cl_`) ?

---

## 12. Ce que je propose ensuite

*(État au moment de la rédaction ; la liste à jour est dans `REPRISE.md`.)*

1. ~~**Écrire le dépaqueteur FARC**~~ — **fait**, `tools/farc.py`, `docs/formats/farc.md`.
2. **Attaquer `mothead_*.bin`** — en cours. En-tête et `CCD` faits ; la section 1 reste
   ouverte. Le meilleur levier disponible est désormais la table d'identifiants d'animation
   (`docs/formats/mot_tables.md`) : chercher dans la section 1 des identifiants connus plutôt
   que de deviner la structure.
3. **Charger les deux ELF dans deux bases Ghidra séparées**, amorcées par `functions.csv`,
   et remonter de `main` vers la boucle principale. **Pas commencé** — Ghidra n'est pas
   installé sur la machine.
4. ~~**Utiliser `vf5fs-pxd-w64-d3d12_SteamRetail.dll` comme pierre de Rosette**~~ —
   **commencé et fructueux** : 14 178 fonctions bornées par `.pdata`, carte des chargeurs de
   données établie, 11 nouvelles fonctions dans `functions.csv`.
5. Seulement ensuite : PS3, X360, puis les enveloppes modernes.

---

## Fichiers produits par cette phase

Liste d'origine, conservée. L'inventaire complet et à jour de l'espace de travail est dans
`REPRISE.md`.

```
analysis/SOURCES.md                 referentiel des six sources
analysis/MANIFEST.md                SHA-256 des fichiers importants
analysis/SOURCE_INVENTORY.md        inventaire detaille
analysis/VERSIONS.md                identification des versions, avec preuves
analysis/LOADER_ARCHAEOLOGY.md      apport des loaders + validation croisee
analysis/API_MATRIX.md              jeu -> API -> loader -> materiel
analysis/CODE_CLASSIFICATION.md     GAME / MOTEUR / LINDBERGH / TIERS
analysis/MODERN_DATA_LINEAGE.md     ce que US et REVO ont herite
analysis/functions.csv              base de fonctions, avec preuve et confiance
analysis/inventory/*.csv            inventaire complet, 18 000+ fichiers
analysis/API_MATRIX_raw.txt         imports classes par bibliotheque
analysis/rtti_vf5_lind.txt          168 types RTTI demangles
analysis/strings_vf5_lind.txt       chaines de la Rev B 6.0000, avec adresses virtuelles
analysis/strings_vf5_lindimg.txt    chaines de la Rev A 2.000
analysis/strings_pxd_us.txt         chaines du DLL Ultimate Showdown
analysis/strings_pxd_revo.txt       chaines du DLL R.E.V.O.
comparisons/rob_data_matrix.csv     matrice d'identite des donnees de combat, 5 versions

tools/inventory_sources.py          inventaire + typage par signature + SHA-256
tools/scan_elf.py                   lecteur ELF 32/64 LE/BE
tools/dump_section.py               extraction de section
tools/extract_strings.py            chaines avec offset et adresse virtuelle
tools/extract_rtti.py               noms de types Itanium C++ ABI
tools/api_matrix.py                 imports -> bibliotheque fournisseur
tools/summarize_inventory.py        resumes d'inventaire
tools/compare_assets.py             comparaison de deux inventaires
tools/compare_dirs.py               comparaison de N repertoires au SHA-256
tools/unpack_ps3_pkg.py             depaqueteur PKG PS3 retail
tools/loaders/lindbergh-loader/     clone de reference (lecture seule)
```

Produits **depuis** la phase 0/1 :

```
analysis/CHARACTERS.md              roster, codes internes, vocabulaire du corps
analysis/disasm_mothead_loader.txt  desassemblage de la fonction 0x180164840
docs/formats/farc.md                format d'archive FARC
docs/formats/mothead.md             format mothead_<CHR>.bin
docs/formats/mot_tables.md          mot_db.bin et rob_mot_tbl.bin
extracted/csv_utf8/                 tables CSV converties de CP932 en UTF-8
extracted/APM3_FS_farc/             archives FARC de l'arcade, extraites
extracted/PC_REVO_farc/             archives FARC de R.E.V.O., extraites

tools/farc.py                       lecteur d'archives FARC
tools/convert_csv.py                CP932 -> UTF-8
tools/pe_disasm.py                  desassemblage PE x64 (pefile + capstone, .pdata)
tools/motdb.py                      base d'animations : mot_db + rob_cmn_mottbl
tools/find_ptr_table.py             tables de pointeurs vers chaines dans un ELF
```

Tous les scripts sont reproductibles et n'écrivent que dans `VF5RE\`.
