# CODE_CLASSIFICATION — quatre catégories de code dans `vf5`

Base de preuve : noms de types RTTI Itanium ABI et chaînes `__PRETTY_FUNCTION__` extraits de
`APM3_FS/vf5` (Rev B 6.0000).
Fichiers : `analysis/rtti_vf5_lind.txt` (168 types démanglés), `analysis/strings_vf5_lind.txt`.

Le binaire n'a **pas** de `.symtab` (0 symbole) : les 762 entrées de `.dynsym` ne couvrent que
les imports. Toute la nomenclature ci-dessous provient donc de données résiduelles du
compilateur, pas d'une table de symboles.

---

## A. GAME — gameplay, combat, personnages, états

L'entité combattante s'appelle **`Rob`** dans tout le moteur (même convention que les autres
titres Sega de cette famille, où `ROB` désigne le personnage animé).

Tâches de combat identifiées :

| Classe | Rôle apparent |
|---|---|
| `TaskRobBase` | base de l'entité combattante |
| `TaskRobCtrl` | entrée → commande |
| `TaskRobPrepareControl`, `TaskRobPrepareAction` | préparation de la frame |
| `TaskRobCollision` | collisions |
| `TaskRobColliAttack` | volumes d'attaque |
| `TaskRobMotionModifier` | modification d'animation |
| `TaskRobDisp` | affichage du combattant |
| `TaskRobLoad`, `TaskRobInfo`, `TaskRobSound` | chargement, état, son |
| `TaskRobSingle`, `TaskRobVersus` | modes solo / versus |
| `TaskRobAI`, `TaskRobAILearn` | IA et apprentissage |
| `TaskRobShortReplay`, `TaskRobShortReplay_Rec` | replay court |

Arbitrage de match et de round :

`TaskGameVs`, `TaskGameVsJudge`, `TaskGameVsRoundNo`, `TaskGameVsWinner`, `TaskGameVsReplay`,
`TaskGameVs2d`, `TaskGameVsAuth3D`, `TaskGameOver`, `TaskGameContinue`, `TaskContinue`,
`TaskVsFinishEnding`, `TaskEnding`, `TaskBattleGameDisp`, `TaskGameScore`.

Sélection et scène : `TaskSelChara`, `TaskSelCharaImage`, `TaskSelStage`, `TaskSelCard`,
`TaskSelSingleMode`, `TaskSelCursor`, `TaskSelCommon`, `TaskSelector`, `TaskStage`.

Mode « KO Trial » et pédagogie : `TaskKoTrialKoDisp`, `TaskKoTrialAdviceDisp`,
`TaskKoTrialIntrudeStartDisp` / `…EndDisp`, `TaskKoTrialDefeatStartDisp` / `…EndDisp`,
`TaskKotAiDataDownload`.

**Roster confirmé — 19 personnages jouables + Dural**, par trois listes concordantes
(`rom/rob/ctrl_*.bin`, `rom/rob/mothead_*.bin`, chaînes `chara_icon_<xxx>_c`) :

`AKI AOI BRA DUR GOH JAK JEF KAG KRT LAU LEI LIO MON MSK PAI SAR SHU TAK VAN WOL`
(`DUR` n'apparaît pas dans la liste d'icônes de sélection ; `CMN` = données communes.)

---

## B. SEGA ENGINE / MIDDLEWARE — moteur et bibliothèques maison

### `prj::` — bibliothèque socle de Sega

Espace de noms `prj` (mangling `N3prj…E`). Contient au moins :
`prj::HeapManager`, `prj::LinkedListBase`, `prj::basic_substring_ref`,
`prj::xml::sax::XMLReaderImpl`, `prj::xml::sax::DefaultHandler`,
`prj::xml::sax::AttributesImpl`, `prj::xml::sax::SAXParseException`,
`prj_system_error_detail::system_error_category` / `generic_error_category`.

Le binaire de production embarque **la suite de tests unitaires** de cette bibliothèque :
`PrjChronoTest`, `PrjFsTest`, `PrjBase64Test`, `PrjAnyTest`, `PrjBitUtilTest`,
`PrjAlgorithmTest`, `PrjFixedStringTest`, `PrjFnmatchTest`, `PrjDateTimeTest`,
avec leurs données de test (`2002-01-31T10:00:01.123456789`, `The quick brown fox…`,
alphabet base64). C'est une source de noms et de sémantique **gratuite et fiable** : chaque
test nomme la fonction qu'il exerce.

Fonctions du système de fichiers nommées explicitement : `fs_rename_dir`, `fs_rename_file`,
`fs_create_dir_internal`, `fs_remove_file`, `fs_create_file`, `fs_last_write_time`,
`fs_last_access_time`, `fs_file_size`, `fs_is_directory`, `fs_is_file`, `fs_is_exists`,
`fs_getexecname`, `fs_remove_dir_internal`, `fs_cmp_file_internal`, `fs_copy_file_sub`,
`fs_subst_file`, `prj::<unnamed>::DirHandle::open/read/close`.

### Moteur graphique et scène

- `a3d::` — sous-système **auth_3d** (mise en scène 3D authorée) ; données dans `rom/auth_3d/`
  et tâches `TaskAuth3dE`, `TaskEffectAuth3D`, `TaskGameVsAuth3D`.
- `AetMgr` — gestionnaire d'animation 2D (données `rom/2d/`).
- Effets : `TaskEffect` et 20 spécialisations (`TaskEffectHit`, `TaskEffectRingoutSplash`,
  `TaskEffectRain`, `TaskEffectSnow`, `TaskEffectThunder`, `TaskEffectWata`,
  `TaskEffectWaterRing`, `TaskEffectFogAnim`, `TaskEffectWetCloth`, `TaskEffectLeaf`,
  `TaskEffectPoison`, `TaskEffectBreath`, `TaskEffectEleBoard`, `TaskEffectYuka`,
  `TaskEffectWall`, `TaskEffectDown`, `TaskEffectMove`, `TaskEffectParticle`,
  `TaskEffectRipple`, `TaskEffectSplash`, `TaskEffectSnowRing`, `TaskEffectFogRing`).
- Ordonnanceur : classe de base **`Task`**, plus `SysFrameRate` et `TaskPlayFrameSpeed`.
- Couche fichier : `File::exec_open` / `File::exec_load` / `File::wait`, format **FARC**.

### `dw::` — boîte à outils de fenêtres de débogage

`dw::Control`, `dw::List`, `dw::ListBox`, `dw::FillLayout`, `dw::ColorDialog`,
`dw::ScrollBar…`, `dw::KeyAdapter`, `dw::MouseAdapter`, `dw::SelectionAdapter`,
`dw::Display::RootKeySelection`, `dw::SysMenuSelectionListener`,
`dw::SelectionListenerLaunchXTerm` (!).

Au-dessus, des panneaux d'inspection propres au jeu : `DataTestMotDw` (listes personnage,
identifiant de mouvement, curseurs de frame / position / rotation / pas),
`DataTestMotCtrlDw` (caméra, `SyncFrameButtonProc`), `DataTestItemOffset`, `RobTraceDw`
(boutons Begin / Play / FF), `MaterialCenterDw`, `LvDataDw`, `DataTestOsageWind`.

**`DataTestMotDw` et `RobTraceDw` sont la piste la plus courte vers les données de mouvement** :
ce sont les outils que les développeurs eux-mêmes utilisaient pour inspecter `mothead_*.bin`.
Confiance : **LIKELY**.

Tâches de test associées : `TaskDataTestObj`, `TaskDataTestCollision`, `TaskDataTestMisc`,
`TaskPerfTest`, `TaskSS` (capture d'écran).

---

## C. LINDBERGH / ARCADE — matériel, exploitation, réseau

- `test_mode::` — menu de test arcade complet : ~45 classes
  (`test_mode::MenuGameSystemInformation`, `Exec_time_limit_vs`, `Exec_enemy_level_single_kt`,
  `Exec_energy_max_vs`, `Exec_allow_stage_select`, `UserFuncBookkeeping`,
  `UserFuncTouchPanelAdjustment`, `ExecPrasCardMemoryTest`, …).
  **Ces classes nomment directement les réglages de gameplay** (limite de temps, niveau
  ennemi, énergie, points) : ce sont des entrées vers les variables de match.
- `terminal::` et `tv::` — terminal VF.NET / satellite : `terminal::TaskTerminalCardInfo`,
  `terminal::VfnetInfo::FestaInfo` / `SisinInfo`, `terminal::ShutterOpen` / `ShutterClose`,
  `terminal::TouchReaction`, `tv::PupilRecent`, `tv::SisinNewsAfterTotalResult`.
- `BackupRamDevice` — sauvegarde en RAM secourue.
- `GfetcherdAuthBillingEventListener` — facturation ALL.Net.
- `TaskIcrw`, `TaskIcrwInfo` — lecteur/graveur de cartes IC.
- `TaskServer`, `TaskHttp`, `TaskAiDataUpload` / `Download`, `TaskBattleDataDownload`,
  `TaskReplayUpload`, `TaskRankingUpdate`, `TaskCardEdit` / `CardRecover` / `CardUpdate`.
- `TaskPoweron`, `TaskWarning`, `TaskClosing`, `TaskModeAppError`, `TaskWaitScreen`.
- Fonctions liées statiquement : `amJvs*`, `amDongle*`, `amDipsw*` (voir `API_MATRIX.md`).

---

## D. THIRD PARTY / RUNTIME

- **CRI Middleware** — le plus gros bloc tiers :
  - CriFs (système de fichiers) : `CriFsManagerCpk`, `CriFsManagerStandardCommon`,
    `CriFsLoaderCommon`, `CriFsGroupLoaderCommon` ;
  - CriAu / ADX2 (audio) : `CriAuCueSheet`, `CriAuVoice`, `CriAuSynth`, `CriAuPlayerLoc`,
    `CriAuObjLoc`, `CriAuCueLoc`, `CriAuAisacControl`, `CriAuTblCsb`, `CriAuTimer`,
    `CriAuFileLoaderForCriFs2`, `CriAuStmIoForFmp`, `CriAuSynthNumControlVoices` ;
  - CriSr (rendu sonore) : `CriSrVoice`, `CriSrVoiceRegMaster`, `CriSrTimer`,
    **`CriSoundRendererLindbergh`**, **`CriSrVocCoreLindberghHsr`** ;
  - CriAc : `CriAcDecoder`, `CriAcStreamControllerFile`.
  - Formats correspondants dans le dump : `.adx` (5 398 fichiers), `.csb`, `.sfd`.
- **libstdc++ / libc / libm / libpthread** (MontaVista, GCC 3.4.3) — 402 imports.
- **zlib** — `inflate`, `deflate`, `crc32`, `adler32`, `compress`, `uncompress`.
- **GLUT / GLU / GL / X11** — voir `API_MATRIX.md`.

---

## Point d'attention : la section `PSFD00`

`vf5` contient une section non standard **`PSFD00`**, de type `PROGBITS`, à
`0x088BCE88`, taille `0x0000F683` (62 Ko), insérée entre `.text` et `.fini`. Une section
portant un nom hors convention et placée dans le segment exécutable mérite d'être identifiée
avant toute décompilation de masse : elle peut relever de la protection anti-copie ou d'un
générateur de code Sega. **Statut : UNKNOWN.** À traiter en priorité en phase 3.

---

## Ce que cette classification ne dit pas

Les catégories ci-dessus sont établies **par nommage**, pas par analyse de flot de contrôle.
Un nom de classe indique une intention de conception, pas une frontière de module vérifiée.
Confiance globale de la classification : **LIKELY**.

## Ce qui a été confirmé depuis, côté R.E.V.O.

Le désassemblage de `vf5fs-pxd-w64-d3d12_SteamRetail.dll` (14 178 fonctions bornées par
`.pdata`) donne des adresses réelles pour la catégorie GAME. Chaque entrée est établie par
l'unicité de la référence à une chaîne de chemin de données :

| Donnée chargée | Fonction | Catégorie |
|---|---|---|
| `rom/rob/mothead_` et `rom_200/rob/mothead_` | `0x180164840` | GAME / combat |
| `rom/rob/ctrl_` et `rom_200/rob/ctrl_` | `0x18005A910` | GAME / combat |
| `rom/rob/rob_mot_tbl.bin` | `0x1801664B0` | GAME / animation |
| `rom/gm_itm_tbl.farc` | `0x18008E180` | GAME / objets |
| `rom/rob_ai/kotrial_enemy_data.txt` | `0x1800942C8` | GAME / IA |
| `rom/game_score.txt` | `0x1800AEB0F` | GAME |
| `rom/ibl` et `rom/light_param` | `0x1800DD0BD` | MOTEUR / rendu |
| `rom/font_image/` | `0x180084970` | MOTEUR / 2D |
| `rom/2d/` | 4 fonctions | MOTEUR / 2D |
| `rom/objset/` | 4 fonctions | MOTEUR / scène |

Fait notable : **seuls `mothead_` et `ctrl_` possèdent une variante `rom_200/`**, et le choix
se fait à l'exécution sur un booléen passé en argument. Ces deux fichiers portent donc à eux
seuls l'équilibrage du jeu — ce que confirme indépendamment la comparaison au SHA-256
(`comparisons/rob_data_matrix.csv`).

Détail et preuves : `analysis/functions.csv`, `docs/formats/mothead.md`,
`docs/formats/mot_tables.md`.
