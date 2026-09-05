# MANIFEST — SHA-256 des fichiers importants

Tous les hashes ci-dessous sont **intégraux**. Les originaux n'ont pas été modifiés :
les fichiers marqués « extrait » ont été produits dans `VF5RE\extracted\` à partir des
archives d'origine, laissées intactes.

| Source | Fichier | Taille (o) | SHA-256 |
|---|---|---:|---|
| LIND_FS | `vf5fs.7z` (original) | 5 369 053 866 | `7cbdab435da92c1431f5af76c0d89bac0ab3fc3981f7f3f2103ed682132587fe` |
| LIND_FS | `vf5fs.bin` — image ext3, extrait | 2 998 927 360 | `eaf2a5d320ec8dea31f3fa679f5e18c3d00aa44d56969c283fe26fc2df05157d` |
| LIND_FS | `vf5fs_ext.bin` — image ext3, extrait | 3 250 585 600 | `8773de9ef3826d3a481e8f1297b0788594b51a2d02212626fc6463477c2bf9c7` |
| LIND_FS | `disk1/vf5` — ELF principal, extrait | 11 867 956 | `8862c9b1afdaea82f549d576be4389595f568b9dedce097bc55bb5ecadd1820b` |
| LIND_FS | `disk1/libalpb.so` | 198 800 | `7e3539ff9af536ae67b23b57413aee41d584d77cfc3a05e3aeacf0fc54a631a0` |
| LIND_FS | `disk1/libsama.so` | 1 247 324 | `b32cfa324d82040c1d4d8a21ad2447d079ced4f8bd130aa1179f2e491fe3d4ae` |
| LIND_FS | `disk1/libbdlog.so` | 11 748 | `2c27493f0eb5d9a05defa8bded7fdc8a7487f2c800dca18ba11c8f76682bcdde` |
| APM3_FS | `vf5` — ELF principal | 12 038 036 | `804e1be3246f06381854dc3c88a49c61ec30f352000009044ba2f2ad70eb5ebd` |
| APM3_FS | `libalpb.so` | 198 800 | `7e3539ff9af536ae67b23b57413aee41d584d77cfc3a05e3aeacf0fc54a631a0` |
| APM3_FS | `libsama.so` | 1 247 324 | `b32cfa324d82040c1d4d8a21ad2447d079ced4f8bd130aa1179f2e491fe3d4ae` |
| APM3_FS | `libbdlog.so` | 11 748 | `2c27493f0eb5d9a05defa8bded7fdc8a7487f2c800dca18ba11c8f76682bcdde` |
| APM3_FS | `drv/ssound/phase2_rc8a/lib/libsegaapi.so` | 67 784 | `0e97c980b76eaf32966035f03dfd825266deef5c1eca8b28066e2007c67f4659` |
| PS3_FS | PKG retail (original) | 2 049 389 840 | `0320794ee5b1af3da18a834b4d4ff629fd5ed26709795f97363349f86beaa7e2` |
| PS3_FS | `USRDIR/EBOOT.BIN` — extrait, **toujours chiffré SCE** | 3 783 280 | `68b5391f3cbb53541c84b514c75618513fd2768ef9979eab62209d1c26faaea8` |
| PS3_FS | `PARAM.SFO` — extrait | 1 092 | `8bb7a7daad887bfab3f563cd186818475da3a46a07a09e6637a77bf6d4cd7ce9` |
| X360_FS | archive RAR (original) | 1 983 848 551 | `6fe5097ebe326f9771a65f20d06a5f1e1686e37d3067e527ca1fae613ca620db` |
| X360_FS | conteneur LIVE `584111FE/000D0000/7D2D…3B1058` — extrait | 2 051 182 592 | `2a9871b1d360e757f3f71ae1dd677b7dff08ab68ef01702e2d170f83b5067406` |
| X360_FS | `TU_1C424FU_0000004000000.0000000000081` — extrait | 729 088 | `d361715b39aa7029310518b979f1ccbc22dc1f5092e59f2723524f3e90fef10d` |
| APM3_US | `runtime/media/eve.exe` | 33 961 984 | `e17c024d4c234c288dd8e34dde2a55e3efef38ef617be204250356539e1b7ffe` |
| APM3_US | `runtime/media/vf5fs/vfes.exe` | 1 987 072 | `540a113e632da32d30cb71df1d329f78ab3b00203c532eaa3a98f72615474721` |
| APM3_US | `runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll` | 6 965 248 | `045c06966ad25f10b10cd854bcdfef588c640a1d785f38b03e97f6ea0c837eef` |
| APM3_US | `runtime/media/apm.dll` | 1 269 760 | `a91ca49bbe728413b87343b3405f9be93ebc08d10f991b0e7004f89c842021e7` |
| PC_REVO | `runtime/media/VFREVO.exe` | 48 840 408 | `7b4e2d9bf6c651d5ed13bc933d8521cc2ce758e68b067c16115ad9d896acb972` |
| PC_REVO | `runtime/media/vf5fs/vf5fs-pxd-w64-d3d12_SteamRetail.dll` | 7 223 296 | `68f042fc3b02699bd7f41c00f16eb0256913980f1828e7ed146937bf0a3b16c0` |

## Observations tirées du manifeste

- `libalpb.so`, `libsama.so`, `libbdlog.so` sont **identiques octet pour octet** entre
  Rev A et Rev B 6.0000. Les bibliothèques d'environnement arcade n'ont pas bougé entre
  les deux révisions. Confiance : **CONFIRMED**.
- Les deux ELF `vf5` diffèrent (11 867 956 o contre 12 038 036 o) : ce sont bien deux
  révisions distinctes du jeu, pas deux copies.
- `EBOOT.BIN` commence par `53 43 45 00` (`SCE\0`), version d'en-tête 2, révision de clé
  0x0019, type 0x0001 : c'est un **SELF NPDRM chiffré**. Il n'est pas exploitable en l'état.

## Inventaires complets

Le détail fichier par fichier (avec type détecté par signature) est dans
`analysis/inventory/*.csv`, régénérable par `py -3 tools/inventory_sources.py`.

| Source | Fichiers | Volume |
|---|---:|---:|
| LIND_FS | 1 archive → 2 images ext3 | 5,00 Go → 6,25 Go |
| APM3_FS | 8 951 | 5,88 Go |
| PS3_FS | 2 (PKG + rap) → 375 éléments | 1,91 Go |
| X360_FS | 1 archive → 2 conteneurs STFS | 1,85 Go |
| APM3_US | 1 059 | 10,76 Go |
| PC_REVO | 6 699 | 20,60 Go |
