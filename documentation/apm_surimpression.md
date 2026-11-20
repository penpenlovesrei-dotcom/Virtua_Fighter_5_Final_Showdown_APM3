# Les badges barrés en surimpression : d'où ils viennent

> **CE DOCUMENT EST UN JOURNAL D'ENQUÊTE.** Le document qui **fait foi** sur
> l'interface APM3 — images, sons, messages, réseau, lancement hors ligne —
> est **`analysis/interface_apm3.md`**. On garde celui-ci pour le chemin
> parcouru et les fausses pistes ; en cas de divergence, l'autre l'emporte.

Question de Frédéric, 2026-09-09, sur une capture de l'écran-titre : six badges
grisés et barrés aux quatre coins, plus un `Processeur graphique / 0 % / 55 °C`
en rouge. Outil écrit pour y répondre : `tools/apm_icones.py`.

## 1. Le JEU ne les contient pas

* **aucune chaîne française** dans le moteur — `Processeur graphique`,
  `Enregistrement`, `Micro`, `Caméra` : zéro occurrence. VF5 ne connaît que
  japonais et anglais (un octet, `moteur+0x64D956`) ;
* **aucun nom d'asset d'icône** : rien en `icon`, `ico_`, `no_`, `ng_`,
  `caution`, `warn`, `rec`, `mic`, `cam` ;
* **les compositions de l'écran-titre sont au complet** et n'en portent pas :
  `misc_title`, `misc_title_plate`, `misc_title_string`, `misc_title_disp_vf5`,
  la scène `TITLE` / `TITLE_TV`, le fond `rom/movie/vf5title_bg.sfd`. Le seul
  texte que le jeu dessine là est `PRESS START BUTTON`.

## 2. Le système APM, lui, en a — et par paires

`APM_V1.04_internal_0` embarque **deux applications Unity** qui dessinent
par-dessus le jeu : `emoneyUI.exe` et `Apmv3System.exe`.

`emoneyUI_Data/Managed/Assembly-CSharp.dll` nomme exactement ce vocabulaire :

    EnableEmoneyIcon     emoneyBackgroundSpriteOnDisable
    EnableGamePadIcon    gamePadBackgroundSpriteOnDisable
    HeadphoneVolumeIcon  iconAlignment / iconAxis / iconX / iconY / iconSize

et ses textures viennent par paires **`_enable` / `_disable`**, au format des
badges de coin :

| texture | taille | format |
|---|---|---|
| `btn_emoney_enable` / `btn_emoney_disable` | 74 × 48 | RGBA32 |
| `btn_pad_enable` / `btn_pad_disable` | 74 × 48 | RGBA32 |
| `btn_volume_enable` | 74 × 48 | RGBA32 |
| `headphone` | 89 × 95 | RGBA32 |
| `BrandIconFrame` | 128 × 128 | DXT5 |

Les `_enable` sont **bleues**, les `_disable` **grises** — mais **sans barre**.

`Apmv3System_Data/resources.assets` porte les 44 autres, dont :

| texture | ce que c'est |
|---|---|
| `EMoney` | une carte ¥ |
| `Network` | un schéma réseau |
| `Speaker` | un haut-parleur |
| **`NotAllow`** | **le cercle barré d'interdiction** |
| `VolumeOff` | haut-parleur avec une croix |
| `AimeCard`, `AimeReader` | la carte et son lecteur |

**`NotAllow` est l'ingrédient qui manquait** : le système superpose ce symbole
à une icône pour la marquer indisponible. Icône grisée + `NotAllow` = un badge
grisé et barré.

## 3. Ce qui est prouvé, et ce qui ne l'est pas

**Prouvé** : le jeu n'y est pour rien, et le système APM possède exactement ce
type de badge — format de coin, paires actif/inactif, symbole d'interdiction,
et le placement par `iconAlignment` / `iconX` / `iconY`.

**Non prouvé** : que les six badges de la capture soient *ces* images-là. À la
résolution de la capture chaque badge fait ~40 px ; je n'ai pas de comparaison
pixel à pixel. Les planches sont dans `extracted/apm_icones/` — c'est à l'œil
que ça se tranche.

**Séparé du reste** : le `Processeur graphique / 0 % / 55 °C` en rouge est en
français, donc ni le jeu ni le système APM (japonais/anglais). C'est une
surcouche de monitoring GPU, à couper dans son application.

## 4. L'ISO du système est illisible

`ALL.Net P-ras Multi Version 2 (Japan) (Rev A).iso` : **entièrement chiffrée** —
entropie 8,00 bits/octet de bout en bout, aucun descripteur ISO9660 au
secteur 16, en-tête `2923be84e16cd6ae…`. On ne peut ni confirmer ni infirmer sa
part. Cohérent avec ce qu'on savait : la clé vient de la puce, pas du disque.

## 5. L'outil

`tools/apm_icones.py` lit un `*.assets` Unity : il retrouve un `Texture2D` par
son nom préfixé de sa longueur, lit `largeur / hauteur / taille / format`, puis
le bloc `streamData { offset, size, chemin }` qui désigne le `.resS`. Il décode
le **RGBA32** et le **BC3 (DXT5)**, et écrit des PNG sans dépendance. Les
lignes Unity sont rangées de bas en haut.

    py -3 tools/apm_icones.py
    py -3 tools/apm_icones.py --assets Apmv3System_Data/resources.assets \
        --noms NotAllow EMoney Network Speaker VolumeOff


---

## 6. L'inventaire complet (2026-09-09)

**109 textures** dans le dossier APM, **96 extraites** — `extracted/apm_icones/`,
planche `_planche_tout.png`. Les 13 restantes sont en **BC7**, non décodé.

Ce que le balayage complet a ajouté :

* **`brn_volume_disable`** — la troisième paire manquait à mon premier passage
  parce que **SEGA a fait une faute de frappe** : `brn_` au lieu de `btn_`.
  Chercher un nom qu'on suppose, c'est chercher sa propre hypothèse ;
* **`EmoneyIconNotAvailableBar`** (256 × 256, BC7) — **la barre** qui traverse
  l'icône, et `EmoneyIconAvailableFrame` / `EmoneyIconNotAvailableFrame`
  (256 × 256, DXT5) : le cadre bleu et le cadre gris. Le badge se compose donc
  en trois couches — cadre + icône + barre ;
* les logos **e-money** (`0001-01-00` … `0009-01-00`), `iD`, les transports,
  `R Pay`, la carte **Aime**, le logo **ALL.Net P-ras MULTI** ;
* tout le jeu de boutons de manette (`button_a_on`…`button_y_on`,
  `arrow_*_on`, `b_trigger_*`, `b_axis_*`) et les panneaux `b_base` /
  `panel_c_base` (1000 × 350, RGB24) ;
* l'iconographie du menu opérateur : `Bookkeeping`, `ClearBackup`, `Firm`,
  `InputTest`, `Matching`, `Advertize`, `Setting`, `Clock`, `Download`,
  `AppList`, `Touch`, `NotAllow`, `VolumeOn` / `VolumeOff`.

## 7. Le catalogue des erreurs

`am_resources/*.dll` sont des DLL de ressources : leurs tables `RT_STRING`
portent **37 erreurs** et **36 avertissements**, chacun avec son numéro, son
comportement de reset et son domaine. Extraits utiles quand on lance le système
sans matériel :

| numéro | message |
|---|---|
| 949 | `Keychip Not Found` — reset=shutdown |
| 6401 | `I/O board is not connected to main board` |
| 5501 | `Touch Panel Not Found` |
| 701 / 702 | `Available application list could not get` |
| 703 | `Available application not found` |
| 6501 | `Aime Card Reader Not Found` |
| 8005 | `Network type error (WAN)` |
| 8106 | `ALL.Net System Caution` |

## 8. La mesure du lancement hors ligne

`tools/apm_hors_ligne.cmd`, essai du 2026-09-09 :

```
emoneyUI      arrete tout seul apres  8 s (code 0)   0 connexion
Apmv3System   arrete tout seul apres 17 s (code 0)   0 connexion
```

Unity 2017.3.0f3, D3D11, aucune exception dans les journaux : les applications
démarrent, affichent **leur propre écran d'erreur** puis se terminent
proprement. **Aucune connexion sortante observée.**


---

## 9. Tout le reste du dossier : images, sons, vidéos (2026-09-09)

Question de Frédéric : « pas d'autres images que des icônes — fonds d'écran,
jaquettes ? Et le son, les musiques ? » Balayage complet du dossier.

### Images

| source | quantité |
|---|---|
| textures Unity (`*.assets`) | **109**, dont 96 extraites — 13 en BC7 non décodé |
| PNG en clair sur le disque | **78 fichiers, 13 DISTINCTS** — six copies du même jeu |

Les 78 PNG sont dans `tfps-res-{dev,pro,stg}` et leurs variantes `-proxy` :
c'est le **système de paiement Thinca** (*Thinca Front Payment System*), livré
en six environnements identiques. Les 13 images distinctes sont les **logos de
marques e-money**, 256 × 256, avec leurs déclinaisons `_bg` et `_wh` :

    nanaco · 楽天Edy (Rakuten Edy) · iD · 交通系 (transports) ·
    WAON · PASELI · SAPICA

`resource.xml` les nomme, et `env.json` donne leurs points d'accès :
`shop.tfps.thincacloud.com`, `tasms-api-basis.thincacloud.com`,
`api-aime.am-all.net`.

**Ni fond d'écran, ni jaquette de jeu.** Les seuls « fonds » sont des panneaux
d'interface : `b_base` et `panel_c_base` (1000 × 350, RGB24, l'écran de test
manette), `BalanceBackground`, `PayToCoinBackground`, `Header` (300 × 300).
Les jaquettes des jeux ne sont pas là : la liste d'applications (`AppList`) les
reçoit par le réseau, avec les jeux.

### Sons

**114 fichiers `.wav`, 17,5 Mo — mais 19 DISTINCTS seulement**, eux aussi
répliqués six fois par environnement. Tous courts, mono 44,1 kHz 16 bits
(deux en stéréo), de **0,22 s à 3,59 s** : ce sont les **jingles de paiement**
— pose de la carte, succès, erreur, solde — un jeu par marque, plus un jeu
générique `9999-*`.

**Aucune musique.** Et **aucun `AudioClip` Unity** dans les dix fichiers
d'assets : les deux applications ne portent pas un seul son en propre, elles
jouent ces WAV par la DLL de paiement.

### Vidéos

**Aucun fichier vidéo dans le dossier** — ni `.mp4`, ni `.wmv`, ni `.usm`, ni
`.bik`. Aucun `VideoClip` ni `MovieTexture` dans les assets.

Le lecteur, lui, est là : **AVPro Video** est présent en greffon, et
`Assembly-CSharp.dll` porte toute la machinerie de publicité —
`<Advertize>c__Iterator0`, `EnableAdvertizeSound`, `IsPlayingMovie`,
`OnMovieEnd`, `GetAdvertizeMessage`. La borne joue donc bien des vidéos
publicitaires, mais **les fichiers arrivent par le réseau** (`net_delivery`,
l'icône `Download`), ils ne sont pas livrés avec le système.

### En résumé

Ce dossier est un **système d'exploitation d'arcade**, pas un jeu : de
l'iconographie d'interface, des logos de moyens de paiement, des jingles de
transaction. Tout le contenu — jaquettes, vidéos, musiques — vient d'ailleurs.
