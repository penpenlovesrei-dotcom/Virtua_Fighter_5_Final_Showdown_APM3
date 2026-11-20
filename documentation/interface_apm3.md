# L'interface APM3 : le système qui entoure le jeu

Établi le 2026-09-09. **Document qui fait foi** sur le système ALL.Net P-ras
Multi — son interface, ses images, ses sons, ses messages, son réseau.
`analysis/apm_surimpression.md` est le journal de l'enquête qui y a mené ;
en cas de divergence, **c'est ce fichier qui l'emporte**.

Source : `C:\Users\frede\Desktop\VF5 FS DECOMP\APM_V1.04_internal_0` (241 Mo).
Outils écrits pour ce chantier : `tools/apm_icones.py` (textures Unity),
`tools/apm_sons.py` (les WAV), `tools/apm_lancer.py` +
`tools/apm_hors_ligne.cmd` (l'essai hors ligne, sous mesure).

---

## 1. Ce qu'est ce dossier

Un **système d'exploitation d'arcade**, pas un jeu. Il tourne sur la carte ALLS
et lance les jeux ; VF5 FS en est un.

| pièce | rôle |
|---|---|
| `amdaemon.exe` (8,4 Mo) | le démon AM : réseau ALL.Net, comptabilité, carte Aime, entrées/sorties |
| `Apmv3System.exe` (Unity) | le **menu opérateur** et la liste des applications |
| `emoneyUI.exe` (Unity) | la **surcouche de paiement** dessinée par-dessus le jeu |
| `hwvalue.exe` | lit la puce : `modeltype`, `dipsw` — décide standalone / serveur / client |
| `ThincaPayment.dll`, `thincahttpclient.dll` | le système de paiement Thinca |
| `lib/` | **`apm.dll`, `apm_x86.dll`, `apmgamepad.dll`, `apmgamepad_x86.dll`** |
| `am_resources/` | huit DLL de ressources : les messages d'erreur, en trois langues |
| `daemon_config/` | `common.json`, `client.json`, `server.json`, `standalone.json` |
| `tfps-res-{dev,pro,stg}` (+ `-proxy`) | les ressources de paiement, six environnements |
| `aime_firm/`, `led/`, `touch/`, `usbio/` | les micrologiciels des cartes |
| `[SYSTEM]/` | des restes de métadonnées NTFS du dump |

**`lib/apm.dll` est le vrai `apm.dll`** que `vfes.exe` importe, et c'est
exactement notre `runtime/media/vf5fs/apm.reelle.dll` — même SHA-256
(`a91ca49bbe728413b873`), 1 269 760 octets. Idem pour `apmgamepad.dll`
(`92fe8f90b508d1a90e74`). Notre stub le remplace ; l'original est ici.

---

## 2. Le démarrage — et pourquoi `game.bat` ne doit JAMAIS être lancé

`game.bat` est le script de démarrage de la borne. Sur un PC ordinaire il est
**destructeur** :

```
rmdir /s /q Y:\                              efface un lecteur entier
reg add "HKLM\System\SEGA\SystemProperty\..." ecrit dans la base de registre
usbio\pxUpdateIoFirm.exe  update_15257_...mot   FLASHE la carte USB IO
led\fut_Nu.exe -P:COM2: -B:115200 -F:...hex     FLASHE la carte LED
touch\TPCUpdateTool.exe 0 -FW ...bin            FLASHE la dalle tactile
reg add "...\amVideo\PortSetting" ...           reconfigure les sorties video
```

Il attend aussi les lecteurs `X:` (le système), `Y:` (SDEM), `W:` (le jeu),
`S:`, `D:`. Rien de tout cela n'existe sur un PC.

`exec_am_daemon.ps1` appelle `hwvalue.exe modeltype` : code de sortie **5** =
`standalone`, sinon `dipsw` décide serveur ou client. Puis il lance
`amdaemon.exe` avec `daemon_config\common.json` plus le fichier du type.

---

## 3. Le réseau : un seul binaire sort

C'est le point qui rend l'étude sûre, et il est **doublement confirmé**.

| binaire | noms de domaine | API réseau |
|---|---|---|
| **`amdaemon.exe`** | `aime.naominet.jp`, `naominet.jp`, `ib.naominet.jp`, `at.sys-all.net`, `amlog.sys-all.net`, `d-amlog.sys-all.net` | `connect`, `WinHttpOpen`, `getaddrinfo`, `send` |
| `Apmv3System.exe` | 2, les schémas XML de son manifeste | **aucune** |
| `emoneyUI.exe` | 2, idem | **aucune** |
| `ThincaPayment.dll` | 1 | `connect`, `send` |

Et **`firewall.cfg` du système ne contient qu'une ligne** :

```
x:\amdaemon.exe
```

SEGA n'ouvre le pare-feu que pour lui. Les deux applications Unity parlent au
démon en local par `AMDaemon.NET.dll` / `amdaemon_api.dll`.

Les points d'accès de paiement sont dans `tfps-res-pro/env.json` :
`shop.tfps.thincacloud.com`, `tasms-api-basis.thincacloud.com`,
`api-aime.am-all.net`.

Dans `daemon_config/common.json` : `allnet_auth`, `allnet_accounting`,
`network`, `aime`, `usb_io`, `apm` — tous à `true`, tous coupables par
configuration.

---

## 4. La surcouche : les badges de coin

C'est elle qu'on voit sur une capture de l'écran-titre de VF5, aux quatre
coins. **Le jeu n'y est pour rien** : aucune chaîne française dans son moteur,
aucun nom d'asset d'icône, et ses compositions de titre sont au complet
(`misc_title`, `misc_title_plate`, `misc_title_string`, `misc_title_disp_vf5`).

`emoneyUI_Data/Managed/Assembly-CSharp.dll` nomme le mécanisme :

    EnableEmoneyIcon      emoneyBackgroundSpriteOnDisable
    EnableGamePadIcon     gamePadBackgroundSpriteOnDisable
    HeadphoneVolumeIcon   iconAlignment / iconAxis / iconX / iconY / iconSize

**Un badge se compose en trois couches** : un **cadre**
(`EmoneyIconAvailableFrame` bleu / `EmoneyIconNotAvailableFrame` gris,
256 × 256), une **icône**, et au besoin la **barre**
`EmoneyIconNotAvailableBar` (256 × 256, BC7).

Les trois paires de coin, 74 × 48 RGBA32 :

| actif | inactif |
|---|---|
| `btn_emoney_enable` (bleu, carte sur lecteur) | `btn_emoney_disable` (gris) |
| `btn_pad_enable` (bleu, manette) | `btn_pad_disable` (gris) |
| `btn_volume_enable` (bleu, casque) | **`brn_volume_disable`** (gris) |

> **`brn_`, pas `btn_`.** SEGA a fait une faute de frappe sur ce seul nom. Ma
> première recherche, faite sur le nom que je supposais, ne l'a pas trouvé —
> je cherchais mon hypothèse. Le balayage complet l'a rendu.

---

## 5. Les images : 109 textures, 13 logos

`tools/apm_icones.py` lit un `*.assets` Unity : il retrouve un `Texture2D` par
son nom préfixé de sa longueur, lit `largeur / hauteur / taille / format`, puis
le bloc `streamData { offset, size, chemin }` qui désigne le `.resS`. Il décode
**RGBA32, RGB24, DXT1 (BC1) et DXT5 (BC3)**, et écrit des PNG sans dépendance.
Les lignes Unity sont rangées **de bas en haut**.

| source | quantité |
|---|---|
| textures Unity, dix fichiers d'assets | **109** — 96 extraites, **13 en BC7 non décodé** |
| PNG en clair sur le disque | **78 fichiers, 13 DISTINCTS** (six copies) |

Sorties : `extracted/apm_icones/` (planche `_planche_tout.png`) et
`extracted/apm_tfps/` (planche `_planche_marques.png`).

**Ce qu'on y trouve** : les six badges de coin ; le cercle barré `NotAllow` ;
tout le jeu de boutons de manette (`button_a_on`…`button_y_on`, `arrow_*_on`,
`b_trigger_*`, `b_axis_*`) et ses panneaux `b_base` / `panel_c_base`
(1000 × 350, RGB24) ; l'iconographie du menu opérateur — `Bookkeeping`,
`ClearBackup`, `Firm`, `InputTest`, `Matching`, `Advertize`, `Setting`,
`Clock`, `Download`, `AppList`, `Touch`, `VolumeOn` / `VolumeOff` ; la carte
**Aime** et son lecteur ; le logo **ALL.Net P-ras MULTI**.

**Les 13 logos de marques e-money**, 256 × 256, avec leurs variantes `_bg` et
`_wh` : `nanaco`, `楽天Edy`, `iD`, `交通系`, `WAON`, `PASELI`, `SAPICA`.
`tfps-res-pro/resource.xml` les nomme.

**Ni fond d'écran, ni jaquette de jeu.** Les seuls « fonds » sont des panneaux
d'interface. Les jaquettes arrivent avec les jeux, par le réseau.

---

## 6. Les sons : 19 jingles, aucune musique

`tools/apm_sons.py` → `extracted/apm_sons/` (3,0 Mo, plus `_index.txt`).

**114 fichiers `.wav` dans le dossier, 19 DISTINCTS** (SHA-256) : les six
`tfps-res-*` sont six copies du même jeu.

| fichier | format | durée | marque (id) |
|---|---|---|---|
| `0001-02-00/01/02` | mono 44,1 kHz | 2,00 / 1,00 / 1,80 s | nanaco |
| `0002-02-00/01/02` | mono, le dernier à **48 kHz** | 1,30 / 2,00 / 2,20 s | 楽天Edy |
| `0003-02-00/01/02/03` | mono 44,1 kHz | 1,66 / 0,76 / 1,51 / 0,65 s | iD |
| `0005-02-00/01/03` | mono 44,1 kHz | 0,22 / 2,10 / 0,34 s | 交通系 **et** SAPICA |
| `0006-02-00/01` | mono 44,1 kHz | 0,29 / 0,90 s | WAON |
| `0008-02-00/01` | **stéréo** 44,1 kHz | 2,47 / 2,70 s | PASELI |
| `9999-02-01` | mono 44,1 kHz | 3,59 s | partagé : 交通系, WAON, nanaco, SAPICA |
| `9999-02-99` | mono 44,1 kHz | 1,06 s | générique |

Deux détails que seule la déduplication montre : `0007-02-01.wav` **est** le
même fichier que `0005-02-01.wav` (d'où ses douze copies), et les deux sons
nanaco `-02-01` / `-02-02` n'existent que dans **trois** environnements sur six.

`resource.xml` relie chaque son à sa marque par un `id` de 0 à 3 **dont il ne
documente pas le sens** : l'id est gardé tel quel plutôt que d'inventer
« succès » ou « erreur ».

**Aucune musique**, et **aucun `AudioClip` Unity** dans les dix fichiers
d'assets : les deux applications ne portent pas un son en propre.

---

## 7. Les vidéos : le lecteur, pas les films

**Aucun fichier vidéo** dans le dossier — ni `.mp4`, ni `.wmv`, ni `.usm`, ni
`.bik` — et aucun `VideoClip` ni `MovieTexture` dans les assets.

Mais le lecteur est là : **AVPro Video** en greffon, et toute la machinerie de
publicité dans `Assembly-CSharp.dll` — `<Advertize>c__Iterator0`,
`EnableAdvertizeSound`, `IsPlayingMovie`, `OnMovieEnd`, `GetAdvertizeMessage`.
La borne joue des vidéos publicitaires ; **les fichiers arrivent par le
réseau** (`net_delivery`, l'icône `Download`).

---

## 8. Les messages d'erreur : 233 chaînes, trois langues

`am_resources/` : huit DLL de ressources, tables `RT_STRING`.

| fichier | messages |
|---|---|
| `error.{english,japanese,chinese}.dll` | **37** chacun |
| `warning.{english,japanese,chinese}.dll` | **36** chacun |
| `error.common.{english,japanese}.dll` | **7** chacun |

Chaque ligne porte son numéro, son comportement de reset et son domaine :

```
Keychip Not Found number=949 sub=0 reset=shutdown tag=common
I/O board is not connected to main board number=6401 sub=0 reset=any tag=io
Touch Panel Not Found number=5501 sub=0 reset=any tag=
Available application not found number=703 sub=0 reset=any tag=
Aime Card Reader Not Found number=6501 sub=0 reset=any tag=aime
ALL.Net System Caution number=8106 sub=0 reset=any tag=accounting_A_B2
Network type error (WAN) number=8005 sub=0 reset=any tag=auth
```

Les domaines : `common`, `io`, `coin_selector_AS6DB`, `network`,
`network_mass`, `lan_install`, `auth`, `accounting`, `accounting_A_B2`,
`aime`, `amdaemon`, `emoney`, `aimepay`.

**Sans matériel ni démon**, les candidats sont 949 (pas de clé), 6401 (pas de
carte I/O), 5501 (pas de dalle), 701 / 702 / 703 (pas de liste
d'applications).

---

## 9. Les lancer hors ligne : la mesure

`tools/apm_hors_ligne.cmd` — prépare un **bac à sable** (`runtime/apm_bac`,
copie de 241 Mo), désamorce la configuration de la copie
(`allnet_auth`, `allnet_accounting`, `network`, `aime`, `usb_io`, `apm` → faux),
lance les deux applications **sans le démon**, et relève leurs connexions TCP
chaque seconde.

Essai du 2026-09-09 :

```
emoneyUI      arrete tout seul apres  8 s (code 0)   0 connexion
Apmv3System   arrete tout seul apres 17 s (code 0)   0 connexion
```

Unity 2017.3.0f3, D3D11, aucune exception : elles démarrent, affichent **leur
propre** écran d'erreur, se terminent proprement. **Aucune connexion sortante
observée.**

**Ce que le script ne fait jamais** : `game.bat` (§2), ni pare-feu, ni `hosts`,
ni base de registre — ce sont des réglages système, c'est la décision de
Frédéric ; ni le dossier d'origine, tout se passe dans la copie.

**Le risque résiduel, dit** : `UnityPlayer.dll` embarque le rapport de
plantage Unity (`perf-events.cloud.unity3d.com`) et `WSAStartup` /
`getaddrinfo`. Il ne part qu'en cas de plantage, et je ne peux pas le prouver
inerte — d'où la mesure plutôt qu'une promesse. Pour une garantie dure :
couper le réseau avant de lancer.

---

## 10. L'ISO du système est illisible

`ALL.Net P-ras Multi Version 2 (Japan) (Rev A).iso` (1,0 Go) est **entièrement
chiffrée** : entropie 8,00 bits/octet de bout en bout, aucun descripteur
ISO9660 au secteur 16, en-tête `2923be84e16cd6ae…`. Cohérent avec ce qu'on
savait — la clé vient de la puce, pas du disque. On ne peut ni confirmer ni
infirmer ce qu'elle contient.

---

## 11. Deux leçons d'outillage, payées ici

* **Chercher un nom qu'on suppose, c'est chercher son hypothèse.**
  `brn_volume_disable` a échappé à trois recherches ciblées ; seul le balayage
  complet de la table des textures l'a rendu. Énumérer d'abord, filtrer après.
* **Une signature de structure se teste sur sa FORME, pas sur des valeurs.**
  Mon premier détecteur de décor d'essai figeait les rangs d'objets à 0 et 1 ;
  `ts2` et `ts3` (rangs 1 et 2) en sont sortis « vrais décors ». Même faute que
  le pas de table figé à `0xF0` dans `comparer_builds.py`.
