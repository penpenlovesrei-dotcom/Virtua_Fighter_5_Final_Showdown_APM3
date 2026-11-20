# Convertir les films SFD en USM sans perdre une image

Établi le 2026-09-08. Outils : `tools/sfd.py` (lecteur Sofdec1),
`tools/usm.py` (lecteur Sofdec2), `tools/usm_mux.py` (le multiplexeur),
lanceur `tools/sfd_vers_usm.cmd`.

---

## 1. Pourquoi c'est un REMBALLAGE et non une conversion

C'est le fait qui décide de tout, et il est mesuré :

| | `.sfd` (Sofdec1) | `.usm` (Sofdec2) |
|---|---|---|
| conteneur | flux de programme MPEG | morceaux `CRID` / `@SFV` / `@SFA` |
| vidéo | **MPEG-1** | `mpeg_codec = 1` → **MPEG-1** (Sofdec.Prime) |
| audio | **ADX** | `audio_codec = 2` → **ADX** |

Vérification faite sur `vf5adv.usm` du jeu : son flux vidéo ne contient
**aucun code d'extension MPEG-2** (`00 00 01 B5`) — seulement des en-têtes de
séquence, des GOP, des images et des tranches. C'est du MPEG-1, exactement
comme dans un `.sfd`.

**Il n'y a donc rien à convertir.** On démultiplexe, on redécoupe, on remballe.

C'est la différence avec le Scaleform Video Encoder du dossier « MP4 to USM » :
`medianoche.exe` **décode puis réencode** en H.264. Il produit un USM lisible,
mais il repasse par la compression.

## 2. La preuve, et elle est arithmétique

Le flux vidéo et le flux ADX ressortis du `.usm` produit ont la **même
empreinte MD5** que ceux du `.sfd` d'origine :

```
vf5moe      video  52 209 294 o   4d9bef4b0a77b70c7cef10e5cdbed4bf   IDENTIQUE
            audio     976 698 o   f02d829d80f6224176f26cc35e219f9f   IDENTIQUE
vf5verBadv  video 206 916 206 o                                      IDENTIQUE
            audio   4 359 186 o                                      IDENTIQUE
```

Pas un octet perdu.

## 3. Le format USM, relevé sur les films du jeu

Un morceau, en-tête de 0x20 octets, tout en gros-boutiste :

```
+0x00 signature   +0x04 u32 taille (sans les 8 premiers octets)
+0x09 u8 déplacement de la charge   +0x0A u16 bourrage de fin
+0x0C u8 voie     +0x0F u8 type (0 donnée, 1 en-tête, 2 fin, 3 métadonnées)
+0x10 u32 date    +0x14 u32 cadence
```

Ordonnancement d'un film Prime + ADX (`vf5adv.usm`) :

```
CRID type 1   CRIUSF_DIR_STREAM, bourré jusqu'à 0x800
@SFV type 1   VIDEO_HDRINFO
@SFA type 1   AUDIO_HDRINFO
@SFV type 2   "#HEADER END     ==============="
@SFA type 2   idem
@SFV type 3   VIDEO_SEEKINFO
@SFV type 2   "#METADATA END   ==============="
...           morceaux de données entrelacés par le temps
@SFV type 2   "#CONTENTS END   ==============="
@SFA type 2   idem
```

Trois mesures qui ont évité autant de suppositions :

* **une image par morceau vidéo** — 7304 morceaux `@SFV` de donnée pour
  `total_frames = 7304` ;
* **un morceau audio = 50 blocs ADX = 1600 échantillons** (1800 octets en
  stéréo) ; le tout premier ne porte que l'en-tête ADX (288 octets) ;
* `VIDEO_SEEKINFO.ofs_byte` est l'**offset absolu dans le fichier** du morceau
  vidéo, une ligne par début de GOP (598 lignes pour 7304 images). Vérifié en
  comparant les valeurs de la table aux positions réelles des morceaux.

Chaque morceau est bourré pour que sa taille totale soit multiple de 0x20.

## 4. Ce qui reste incertain, et il faut le dire

**Le champ `date` des morceaux vidéo.** Chez CRI il avance de ~49,95 par image
à une cadence de 6000, ce qui donne une durée totale **moitié** de la vraie
(60,8 s pour un film de 121,7 s), alors que l'audio, lui, est juste. Les cinq
films du jeu ont tous ce décalage : c'est une convention de leur outil, et le
lecteur se cadence donc sur `framerate_n / framerate_d`. On reproduit la
convention observée (`--dates cri`, par défaut) ; `--dates justes` écrit le
temps réel. Si le son décroche à l'écran, c'est le premier bouton à tourner.

**Les pistes AIX sont gérées** (2026-09-08). Voir §7.

**Rien n'a encore été joué dans le jeu.** Les fichiers se relisent avec notre
propre lecteur et leurs flux sont intacts ; c'est tout ce qui est prouvé.

## 5. Ce que ça ouvre

Le dump `X360_VF5` (VF5 vanilla) porte cinq films que notre build n'a pas :

```
vf5adv.sfd        232 Mo   -> 5400 images 1280x720 a 60/s
vf5end.sfd        191 Mo
vf5moe.sfd         54 Mo   ->  510 images  640x480 a 30/s
vf5verBadv.sfd    228 Mo   -> 4708 images 1280x720 a 60/s
vf5verCadv.sfd    209 Mo
```

Les deux intros `verB` et `verC` sont **exactement au format des films
d'APM3** — 1280×720, 60 images/s, MPEG-1 + ADX. Elles peuvent remplacer
`vf5adv.usm` par simple dépôt de fichier, `rom/movie` étant lu depuis
l'arborescence libre et non depuis le `.par` (mesuré dans
`import_decors.md` §2).

---

## 6. Extraction des SFD des versions Xbox 360 (2026-09-08)

Les deux dumps Xbox 360 ne se ressemblent pas :

* **VF5 vanilla** (`X360_VF5`) : cinq `.sfd` en fichiers libres sous
  `media/movie/` ;
* **Final Showdown** (`X360_FS`) : un paquet **STFS** de 2,05 Go
  (`584111FE/000D0000/7D2DF36B…`, magie `LIVE`, 2370 entrées), ouvert par
  `tools/stfs.py`. Il ne contient **qu'un seul film**, `vf5end.sfd`, et
  **aucun `.usm`**.

Les six sont réunis dans `extracted/sfd_x360/`, préfixés par leur version.
Inventaire par `tools/sfd_inventaire.py` (qui ne lit que les premiers
mégaoctets : l'en-tête de séquence MPEG est en tête du premier paquet vidéo,
l'en-tête ADX en tête du premier paquet audio) :

```
film                                octets  image       cadence  son
fs_vf5end.sfd                    145311744  1280x720    60.000/s ADX 2 canaux 44100 Hz, 82.0 s
vanilla_vf5adv.sfd               232202240  1280x720    60.000/s ADX 2 canaux 48000 Hz, 90.0 s + AIX
vanilla_vf5end.sfd               191207424  1280x720    60.000/s ADX 2 canaux 44100 Hz, 74.0 s
vanilla_vf5moe.sfd                53989376  640x480     30.000/s ADX 2 canaux 48000 Hz, 18.1 s
vanilla_vf5verBadv.sfd           227686400  1280x720    60.000/s ADX 2 canaux 48000 Hz, 80.7 s + AIX
vanilla_vf5verCadv.sfd           209416192  1280x720    60.000/s ADX 2 canaux 44100 Hz, 80.1 s + AIX
```

Cinq des six sont en **1280×720 à 60 images/s**, exactement la définition des
films d'APM3. Trois portent une seconde piste **AIX** (le multilingue de CRI),
qui reste écartée à la conversion.

À noter : le `vf5end.sfd` de la Xbox 360 Final Showdown (145 311 744 o) n'est
**pas** celui du Lindbergh Final Showdown (145 477 632 o) — 165 888 octets
d'écart. Ce sont deux masters différents.


---

## 7. Le multipiste audio : l'AIX déplié

`vf5verBadv.sfd` porte **deux** flux audio : un ADX simple (4,4 Mo, la piste
principale) et un conteneur **AIX** de 13 Mo — le multipiste de CRI.

Format relevé sur ce fichier, tout en gros-boutiste :

```
en-tete
  +0x00  'AIXF'
  +0x04  u32  offset du premier AIXP, moins 8
  +0x20  u32  offset des donnees (0x1800)
  +0x24  u32  taille totale des donnees
  +0x28  u32  nombre d'echantillons     +0x2C  u32  frequence
  +0x40  u8   NOMBRE DE FLUX
  +0x48  par flux : u32 frequence, u8 canaux, 3 octets de bourrage

morceau AIXP
  +0x00  'AIXP'
  +0x04  u32  taille de la charge, BOURRAGE COMPRIS
  +0x08  u8   numero du flux       +0x09  u8  nombre de flux
  +0x0A  u16  longueur UTILE       +0x0C  u32  numero de bloc (-1 = l'en-tete)
  +0x10  la charge
```

Les trois premiers `AIXP` (numéros 0, 1, 2) portent chacun l'**en-tête ADX** de
leur flux ; les suivants leurs blocs. Recoller flux par flux les charges utiles
rend donc trois fichiers ADX complets — sans rien décoder ni recalculer.

Chaque flux devient une **voie `@SFA`**, qui est précisément le mécanisme
multipiste de Sofdec2. `vf5verBadv` sort en **quatre voies** :

```
video                          206 916 206 o   IDENTIQUE
audio voie 0 (ADX principal)     4 359 186 o   IDENTIQUE
audio voie 1 (AIX 1)             4 320 058 o   IDENTIQUE
audio voie 2 (AIX 2)             4 320 058 o   IDENTIQUE
audio voie 3 (AIX 3)             4 320 058 o   IDENTIQUE
```

Les trois flux AIX ont des empreintes **différentes** (`161aef7c…`,
`2df065f1…`, `8653...`) : le désentrelacement route bien chaque morceau vers
son flux, ce ne sont pas trois copies.

`--pistes N` limite le nombre de voies écrites, si le moteur s'étranglait sur
quatre.
