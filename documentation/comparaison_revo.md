# APM3 CONTRE VF5 REVO (Steam) — 2026-10-09

Comparaison de `vf5fs-pxd-w64-Retail_APM3.dll` (notre build) et de
`vf5fs-pxd-w64-d3d12_SteamRetail.dll` (VF5 REVO, Steam). **Lecture seule** : on
s'en sert comme référence, on n'en copie rien.

On ne compare pas des adresses — deux builds n'ont pas la même disposition. On
compare des **présences** : en-tête, imports, classes RTTI, chaînes-témoins.

## 1. C'est le même moteur, cinq ans plus tard

| | APM3 | REVO |
|---|---|---|
| horodatage | **2021-05-19** | **2026-08-26** |
| base | `0x180000000` | `0x180000000` |
| exports | `module_start`, `module_stop` | identiques |
| taille d'image | 15,0 Mo | 19,4 Mo |
| `.text` | 3,40 Mo | 3,59 Mo (**+5,5 %**) |
| `.rdata` | 3,11 Mo | 2,89 Mo (**plus petit**) |
| `.data` (virtuel) | 8,53 Mo | 12,70 Mo (**+50 %**) |
| classes RTTI | 534 | 635 — **353 communes** |

## 2. LES IMPORTS DISENT TOUT

    APM3   ADVAPI32, bcrypt, ole32, WS2_32, OLEAUT32, D3DCOMPILER_47, KERNEL32
    REVO   EOSSDK-Win64-Shipping (108), steam_api64 (12), dxgi, USER32,
           D3DCOMPILER_47, KERNEL32

La pile réseau et la crypto **maison** de la borne disparaissent (sockets,
bcrypt, COM) ; Steam et Epic Online Services les remplacent.

## 3. Ce que REVO perd — la borne entière

* **`am::abaas::*`** : toute la pile ALL.Net — STUN/TURN, allocation de canal,
  contrôle de connectivité et de qualité de ligne, douze états de `LinkMain`.
  Le mot « abaas » passe de **267 occurrences à 0**.
* **`apm3TestMode::*`** : le menu TEST de la borne (`MenuTop`, `MenuBookkeep`,
  `MenuGameAssign`, `MenuBackupClear`, `MenuSoundSetting`).
* `TaskApm3Entry`, `TaskApmResult`, `modeApm3::TaskTimer`,
  `modeApm3::WaitingReadyWindow`, `cs_session::*`.
* `util::crypt::Aes`, `util::hash::Calcurator::CNG`, `util::rand::Bcrypt`,
  `util::compression::Zlib`, `impl::Curl`.
* La chaîne `QUEST` : **1 → 0**.

## 4. Ce que REVO gagne

* **Rendu D3D12** : `D3D12MA::*`, `cd3d12_mem_allocator`, et **`pbgl::*`** qui
  remplace notre `sbgl::*`. Avec les upscalers : `pxd::pfx::dlss`,
  `pxd::pfx::fsr3`, `pxd::pfx::xefg`.
* **Rollback netcode** : `TaskRobRollback`, `IoRollbackCtrl`,
  `IoVsRollbackCtrl`, `RollbackTraceRobInfo`, `RollbackTraceUnit`,
  `IoBuffering`.
* **Réseau moderne** : `CSessionSteamNet`, `CSessionEos`, `NPMatching2Session`,
  `PsnMatchControl`, et onze `MakeRoomState_*`.
* **Tournois** : `Tournament::Ctrl::*`, `Tournament::Model::*`,
  `TaskTournamentManager`, `world_stage::*`.
* **Replays** : `replay::OfflineReplay`, `ReplayMenu`, `ReplayStorage`,
  `TaskOnlineReplay`, `TaskReplayManager` — là où le nôtre est un bouchon
  (journal 15.14).
* **Stockage joueur** : `user_storage::UserStorage`, `VFPlayerDataStorage`.
* Menus : `TaskMenuSetting`, `TaskMenuTeam`, `TaskClearInfo`,
  `TaskMultiRoomMatchMenu`, et **`TaskCredit`**.
* `TaskCsCrossplayWarning`, `TaskCsOfflineWarning`, `TaskStreamingLayout`,
  `TaskTelemetryImpl`, `TaskFreepackMng`.

## 5. CE QUI NE BOUGE PAS — et c'est ce qui nous intéresse

Tous les témoins de notre chantier sont présents **dans les deux** :

    OPTION MENU / FILE / SETTING / HOWTO / CONTROL / INFO
    MENU_EXPLAIN, MENU_CONTROL, head_index, head_small
    choice_win_02 .. choice_win_08, sousa_win
    logo_jpn, logo_usu, SEGA_s, INFO_end, sega441.adx
    STGTST, STGCMN, EFFEFFCMN, NAGE_VF4, stgdur, se_*.csb
    TaskCsSystemSaveData, TaskCsWarning, TaskAutoLoad, string_array

Et l'aiguillage des OPTIONS est **le même, à l'instruction près** :

    APM3  0x1801A7116  cmp eax,3 -> « OPTION FILE » sur page+0xD98
          0x1801A715C  cmp eax,5 -> « OPTION INFO » sur page+0x1208
    REVO  0x1801B6FA1  cmp eax,3 -> « OPTION FILE » sur page+0xDB0
          0x1801B6FF2  cmp eax,5 -> « OPTION INFO » sur page+0x11F0

Les sous-objets ont glissé de 0x18, le reste est identique.

## 6. LE BOUCHON N'EST PAS UN MARQUEUR DE COUPE

Mesure contre-intuitive : les deux builds portent le même idiome
`xor al,al ; ret`, avec **3360 appels** chez nous et **3056** dans REVO. C'est
une virtuelle par défaut du moteur, pas une cicatrice d'arcade. Nos diagnostics
restent valides parce qu'ils portaient sur des **sites précis** — par exemple
`0x1801B769B`, le démarreur de `TaskCsSystemSaveData` — jamais sur l'existence
du bouchon.

## 7. Les films

REVO (`rom/movie/`) : `vf5adv` (812 Mo), `vf5end` (605), **`vf5end_us`** (605),
`vf5chara_sel_loop`, `vf5chara_sel_start`, `vf5match_sel_bg`, `vf5title_bg`.

**Et notre build en a déjà six sur disque** : `vf5adv` (335 Mo),
`vf5end` (120), `vf5chara_sel_loop`, `vf5chara_sel_start`, `vf5match_sel_bg`,
`vf5title_bg` — alors que le Movie Theater n'en joue qu'un. REVO n'apporte
que `vf5end_us`, et des versions bien plus lourdes (meilleure définition).

## 8. Ce qui n'est PAS vérifié

Si les chemins précis bouchonnés chez nous — la page Save Data, le chargement
des reprises, le tic absent de la page de MENU — sont **vivants** dans REVO. Il
faudrait remonter leurs vtables, build par build. C'est le prochain pas si on
veut s'en servir comme modèle.

## 9. Ce que ça change pour le chantier

REVO est une **meilleure pierre de Rosette que la Xbox 360** : même moteur,
même compilateur, mêmes noms de scènes et de classes, offsets voisins à
quelques octets près. Là où la X360 demandait de traduire du PowerPC et des
conventions différentes, REVO se lit à côté du nôtre, fonction par fonction.


---

# CE QU'ON PEUT EN TIRER — 2026-10-09

## A. Lire les prédicats que l'arcade a bouchonnés

**C'est le gain principal, et il est écrit dans le journal depuis le début du
projet sans avoir jamais été fait** (REPRISE.md, « la piste pour demain : se
servir vraiment de la pierre de Rosette »).

Le build arcade a bouchonné au moins trois prédicats — `0x180029FB0`
(`mov al,1 ; ret`), `0x180007450` (`xor al,al ; ret`), `0x180007430` (`ret 0`).
Chaque fois qu'un écran est mort chez nous, c'est l'un d'eux qui garde le
chemin. **Dans REVO, ces fonctions existent pour de vrai.**

### Un cas, vérifié aujourd'hui

`TaskCsSystemSaveData(LOAD)`, la tâche de sauvegarde système :

    APM3   0x1801B7699  mov ecx, ebx
           0x1801B769B  call 0x180007450      <- xor al,al ; ret
           0x1801B76A0  test al, al
           0x1801B76A2  je   0x1801B7731      <- on sort : JAMAIS lancee

    REVO   0x1801D6233  lea r8, "TaskCsSystemSaveData(LOAD)"
           ... la tache est demarree, sans ce garde-fou a cet endroit

Les deux fonctions ne sont pas alignées à l'instruction près — il faudra
remonter la fonction REVO pour l'affirmer. Mais le chemin est là, et vivant.

### La liste de ce qui attend ce traitement

| mort chez nous | où c'est écrit | ce que REVO en dirait |
|---|---|---|
| la page **Save Data** | journal 159 | ce que la page fait quand elle s'ouvre |
| le chargement des **reprises** | journal 15.14 | ce que `Your data` devait lire |
| le **tic** absent de la page de MENU | `menu_console.md` 6.4 | qui l'appelle, et quand |
| `TaskCsSystemSaveData` | ci-dessus | ce que la sauvegarde écrit |
| **Dural** qui ne quitte pas son repos | `analysis/dural.md` | en aval de `GetMotionForRole` |

## B. Les données plus récentes

| fichier | nous | REVO |
|---|---:|---:|
| `string_array.farc` (les textes) | 1,08 Mo | **1,19 Mo** (`rom_200/`) |
| `chritm_tbl.farc` (objets de personnalisation) | dans le `.par` | **13,5 Mo**, à plat |
| `resident.farc` | — | 3 révisions : `.r2421`, `.r2427`, courante |

Les trois révisions de `resident.farc` permettent de **dater les changements**
entre versions — un diff qu'on n'a nulle part ailleurs.

`extracted/PC_REVO_farc/rom_200/` contient déjà `chritm_tbl`, `resident` et
`string_array` extraits : le travail de dépaquetage est fait.

## C. Les films

REVO apporte **`vf5end_us.usm`**, et des versions bien plus lourdes de tout le
reste (`vf5adv` 812 Mo contre 335, `vf5end` 605 contre 120) — c'est-à-dire une
définition supérieure.

**Mais le gain immédiat n'est pas là** : notre propre build a déjà **six films**
sur disque (`vf5adv`, `vf5end`, `vf5chara_sel_loop`, `vf5chara_sel_start`,
`vf5match_sel_bg`, `vf5title_bg`), et le Movie Theater n'en joue qu'un parce que
le chemin est écrit en dur.

## D. CE QU'ON NE GAGNE PAS

* **Les décors** : 41 des deux côtés, **les mêmes noms**, à l'identique. Rien à
  prendre. Seule curiosité : la chaîne `STGDUR` existe dans REVO (`0x180431174`,
  collée à `STGDU1` et `EFFSTGDU1`) et **pas chez nous** — à creuser pour le
  chantier Dural, mais ce n'est pas une entrée de la table.
* **Le mode Quest** : la chaîne `QUEST` passe de 1 à 0. REVO ne l'a pas. Notre
  chantier Quest reste sans modèle.
* **Le code** : il ne se transplante pas. D3D12 contre D3D11, `pbgl` contre
  `sbgl`, dispositions différentes, et la `module_params_t` de REVO fait
  64 octets quand la nôtre en fait 112.
* **Le netcode** : le leur est Steam et EOS ; le nôtre est ALL.Net. Rien de
  commun.

## E. Le pas suivant, s'il est voulu

Une **table de correspondance** : pour chaque site bouchonné chez nous, le site
homologue dans REVO. La méthode est rodée — s'ancrer sur une chaîne-témoin
(elles sont toutes présentes des deux côtés), puis lire. Le coût est d'environ
une demi-heure par cas, et la carte servira ensuite à chaque nouveau blocage.


---

# D3D11 (nous) CONTRE D3D12 (REVO) — 2026-10-09

## Où vit la couche graphique

**Chez nous, elle est dans l'HÔTE, pas dans le moteur.** `vfes.exe` importe
`d3d11.dll`, `dxgi.dll` et `d2d1.dll` ; la DLL du moteur ne cite ni `d3d11` ni
`dxgi` — zéro occurrence. Chez REVO, c'est la DLL elle-même qui importe `dxgi`.

Et le backend change de nom avec l'API : **`sbgl` (5 occurrences chez nous)
devient `pbgl` (10 chez REVO)**, avec `pbgl::ccommand_list`,
`csystem_command_list`, `cpipeline_state_library::allocator_t` — le modèle
D3D12 : listes de commandes et cache d'états de pipeline.

## Ce que D3D12 apporte à REVO, mesuré

| | preuve |
|---|---|
| **DLSS 3.5** + Streamline + **Reflex** | `nvngx_dlss.dll`, `pfx_dlss3_5.dll`, `sl.common/.dlss/.reflex/.interposer.dll`, classe `pxd::pfx::dlss::context_st::cevent_hook` |
| **FSR 3.1** | `amd_fidelityfx_dx12.dll`, `pfx_fsr3_1.dll`, `pxd::pfx::fsr3::...` |
| **XeSS + XeFG** | `libxess.dll`, `libxess_fg.dll`, `libxell.dll`, `pfx_xess.dll`, `pfx_xefg.dll`, `pxd::pfx::xefg::...` |
| **allocateur mémoire explicite** | `D3D12MA::Allocation`, `BlockMetadata_TLSF`, `MemoryBlock`, `cd3d12_mem_allocator` ; `.data` virtuel passe de 8,53 à 12,70 Mo |
| **Agility SDK** | `d3d12/D3D12Core.dll` livré avec le jeu — runtime D3D12 indépendant de Windows |

Les trois upscaleurs sont livrés en **DX12** (`amd_fidelityfx_dx12.dll`) : ils
ne se branchent pas sur une pile D3D11.

## Ce que ça coûte

* **Les shaders sont repackagés** : REVO a `shader_pxd_w64_d3d12.farc` (53 Ko)
  et `shader_pxd_w64.farc` (9 Ko) là où nous avons **10,5 Mo** de
  `shader_pxd_w64.farc`. Nos shaders précompilés **DXBC** ne se réutilisent pas
  tels quels — D3D12 veut du **DXIL**.
* **D3D12 exige Windows 10+** et un pilote récent. D3D11 tourne partout, ce qui
  sur une borne est un argument, pas un détail.
* Barrières, descripteurs et tas passent à la charge de l'application — c'est ce
  que D3D11 faisait tout seul.

## Pour notre build : non applicable

Passer en D3D12 demanderait de réécrire **l'hôte** (`vfes.exe`, qui crée le
device) **et** de remplacer `sbgl` par `pbgl` dans la DLL. C'est le travail que
SEGA a fait pour REVO, pas un correctif binaire.

Note : le `ReShade.ini` et `reshade-shaders/` du dossier REVO ont été installés
à la main, ils ne viennent pas du jeu. ReShade fonctionne aussi en D3D11 — c'est
la seule voie d'amélioration de rendu ouverte à notre build sans toucher à l'API.
