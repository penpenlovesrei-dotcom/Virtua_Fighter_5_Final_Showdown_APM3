# SOURCES — référentiel des sources locales

Établi le 2026-08-31. Toutes les sources sont traitées en **lecture seule**.
L'espace de travail du projet est `C:\Users\frede\Desktop\VF5RE\` (séparé des dumps).

## Table de référence

| ID | Version | Plateforme réelle | Chemin | SHA-256 de l'élément identifiant | Version / build | Analysé |
|---|---|---|---|---|---|---|
| `LIND_FS` | Final Showdown **Rev A** | Lindbergh (x86 Linux) | `Desktop\VF5 FS DECOMP\LIND_FS\vf5fs.7z` | `7cbdab43…2587fe` (archive) | ELF `disk1/vf5` : release **2.000**, 2010-06-28 | oui (phase 0/1) |
| `APM3_FS` | Final Showdown **Rev B ver 6.0000** | Lindbergh (x86 Linux) — **pas APM3** | `Desktop\VF5 FS DECOMP\APM3_FS\` | `804e1be3…eb5ebd` (`vf5`) | release **6.000**, 2011-10-17 | oui (phase 0/1) |
| `PS3_FS` | Final Showdown | PlayStation 3 (PPC64) | `Desktop\VF5 FS DECOMP\PS3_FS\*.pkg` | `0320794e…aa7e2` (PKG) | `NPEB00913`, APP_VER 01.00 | partiel (dépaqueté) |
| `X360_FS` | Final Showdown + TU1 | Xbox 360 (PPC64) | `Desktop\VF5 FS DECOMP\X360_FS\*.rar` | `6fe5097e…620db` (RAR) | Title ID `584111FE`, conteneur LIVE | non (conteneur STFS non ouvert) |
| `APM3_US` | VF5 eSports + Ultimate Showdown | **Sega ALLS/APM3 — Windows x64** | `Desktop\VF5 FS DECOMP\APM3_US\` | `045c0696…837eef` (`vf5fs-pxd-w64-Retail_APM3.dll`) | moteur FS release **6.000**, portage 2016-06-30 | oui (phase 0/1) |
| `PC_REVO` | R.E.V.O. World Stage | PC Windows x64 (D3D12) | `Program Files (x86)\Steam\steamapps\common\VFREVO\` | `68f042fc…3b16c0` (`vf5fs-pxd-w64-d3d12_SteamRetail.dll`) | `VFREVO.exe` 1.0.0.0 ; moteur FS release **6.000**, portage 2016-06-30 | oui (phase 0/1) |

Sources absentes (aucune supposition faite) : `ARCADE_FS_REVA` / `REVB` / `REVB_60000` en tant que
répertoires distincts, `UM_PS4`, `UM_PS5`, `VF5R_ARCADE`, `VF5_ARCADE`.
Les révisions arcade Rev A et Rev B 6.0000 sont bien présentes, mais dans `LIND_FS` et `APM3_FS`
respectivement — voir `VERSIONS.md`.

## Deux corrections d'étiquetage

Les noms de dossiers choisis à la constitution du dump ne correspondent pas au contenu réel :

1. **`APM3_FS` n'est pas un dump APM3.** C'est le contenu de la partition `/home/disk1` d'un
   disque **Lindbergh** : ELF32 x86, `libsegaapi.so`, GLUT/GLX, `tools/lindbergh/`,
   `.gdbinit` en registres `eax/eip`. Confiance : **CONFIRMED**.
2. **`APM3_US` est bien un dump APM3**, mais il contient **deux jeux** (`eve.exe` pour
   VF5 eSports, `vf5fs/vfes.exe` pour Ultimate Showdown), sur une base **Windows x64**.

## Fichiers produits

| Fichier | Contenu |
|---|---|
| `analysis/inventory/<ID>.csv` | inventaire complet : chemin, taille, type par signature, SHA-256 |
| `analysis/inventory/LIND_vf5fs*.listing.txt` | listing des deux images ext3 de `LIND_FS` |
| `analysis/MANIFEST.md` | hashes des fichiers importants |
| `comparisons/rob_data_matrix.csv` | matrice d'identité des données de combat entre 5 versions |

## Ce qui a été extrait des sources

Rien n'est écrit dans les dumps ; tout va dans `VF5RE\extracted\`.

| Destination | Origine | Outil |
|---|---|---|
| `extracted/LIND_FS/*.bin` | `vf5fs.7z` → deux images ext3 | 7-Zip |
| `extracted/LIND_FS/sel/`, `tree/` | contenu des images ext3 | 7-Zip (support Ext) |
| `extracted/PS3_FS/` | PKG retail, extraction sélective | `tools/unpack_ps3_pkg.py` |
| `extracted/X360_FS/` | archive RAR → deux conteneurs STFS | 7-Zip |
| `extracted/APM3_FS_farc/` | archives FARC de l'arcade | `tools/farc.py` |
| `extracted/PC_REVO_farc/` | archives FARC de R.E.V.O. | `tools/farc.py` |
| `extracted/csv_utf8/` | tables CSV converties de CP932 | `tools/convert_csv.py` |

## Outils tiers déposés dans `tools/`

| Outil | État |
|---|---|
| `PARtool v1.3.windows-x64/ParTool.exe` | fonctionne — archives `.par` (moteur Dragon) |
| `FFmpeg-based-ADX-converter/` | fonctionne — audio ADX |
| `PSN.PKG.Decryptor...` | redondant avec `unpack_ps3_pkg.py` ; **ne déchiffre pas les SELF** |
| `PARC.Archive.Importer.exe` | interface graphique, non scriptable |
| `FARC-v0.1.0-alpha2-.exe` | **échoue** sur les archives du jeu ; remplacé par `tools/farc.py` |
| `PS4 PKG Tool` | sans objet — aucune source PS4 dans le projet |

## Mode de hachage

Les fichiers ≤ 64 Mio sont hachés intégralement (`hash_mode=FULL`). Au-delà, l'inventaire
enregistre un condensé taille + premier Mio + dernier Mio (`hash_mode=HEADTAIL`) : suffisant
pour repérer un changement, **insuffisant pour affirmer une identité**. Toute conclusion
d'identité de ce rapport repose exclusivement sur des hashes `FULL`.
