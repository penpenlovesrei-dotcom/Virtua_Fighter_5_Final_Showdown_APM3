# Les aperçus et les vignettes de l'écran de sélection de décor, par génération

Établi le 2026-11-19. Rien n'est lancé : tout est lu dans les fichiers de
données et dans `vf5fs-pxd-w64-Retail_APM3.dll.origine`.

Point 11 de Frédéric : *« au lieu de mettre uniquement une annotation sur la
version du décor choisi (VF5, VF5R ou VF5FS), je voudrais aussi changer
l'aperçu du décor dans la moitié supérieure de l'écran […] Fais la même chose
avec les petits rectangles des décors que l'on sélectionne dans la partie
inférieure. »*

**Les images sont sorties.** Dossier proposé et rempli :
`VF5RE\APERCUS_DECORS\`, **118 PNG**, outil `tools/apercus_decors.py`.

---

## 1. Comment l'écran trouve ses images aujourd'hui — mesuré

### 1.1 Les deux familles, et elles ne vivent pas au même endroit

Tout est dans **une seule planche**, `rom/2d/spr_s_selstg.farc` → `FArC`, une
entrée, `spr_s_selstg.bin` : **30 textures, 105 sprites**, planche n° **500**
(`0x01F4`) de `spr_db.bin`.

| | nom du sprite | identifiants | taille | où est le pixel |
|---|---|---|---|---|
| **grand aperçu** | `SPR_S_SELSTG_REND_STAGE_<PERSO>` | `0x5222`…`0x5235` (20) | 1024 × 500 | **une texture dédiée par décor** : `NOMERGE_D5COMP_000_0` … `_019_0`, 1024 × 512, DXT1 |
| **vignette** | `SPR_S_SELSTG_ICON_STAGE_<PERSO>` | `0x4E00`…`0x4E13` + `0x5CD7` (21) | 140 × 52 | **un rectangle dans une planche partagée** : `MERGE_D5COMP_0` pour 19, `MERGE_D5COMP_1` pour `smo` et `tak` |

Ce fait-là décide de tout ce qui suit : **remplacer un grand aperçu, c'est
remplacer une texture entière** — exactement ce que `tools/textures_hd.py`
sait déjà faire — alors que **remplacer une vignette, c'est repeindre un
rectangle** dans une planche que dix-neuf autres partagent.

### 1.2 Le chemin, du code au pixel

`TaskSelStage` (vtable `0x180400A18`, `update` `0x180174250`) **ne nomme aucun
sprite**. Il nomme des **marqueurs**.

`0x180174BF0` bâtit sur la pile 25 entrées de 0x18 octets
`{index de décor, "xxx", "xxx_stay"}` (`analysis/decors.md` §6). Ces deux
chaînes sont les **marqueurs** portés par deux calques de la composition
RACINE de `aet_s_selstg.bin`, scènes `VGA_MAIN` et `WXGA_MAIN` (1280 × 768) :

```
compo 58 (RACINE), calque 5  stage_name_l_base   0-3600  -> compo 30
compo 58 (RACINE), calque 6  stage_graph_l_base  0-3600  -> compo 57
     marqueurs : 0:ban 11:ban_stay 60:ter 71:ter_stay 120:nyc 131:nyc_stay
                 ... 1020:dur 1031:dur_stay 1080:gym 1091:gym_stay
                 1140:smo 1151:smo_stay 1200:rnd 2400:rnd_stay 2519:end
                 3000:ari 3011:ari_stay 3060:oro 3071:oro_stay
```

Le marqueur donne un **instant**, l'instant choisit le **calque** de la
composition pointée, le calque pointe une **sous-composition**, et c'est elle
qui porte le sprite :

```
marqueur "ban" -> t=0    -> compo 57 calque 0  "stage_rend_lau" -> compo 31
                         -> s_selstg_rend_stage_lau__n.pic
                         -> S_SELSTG_REND_STAGE_LAU, id 0x5222
```

**Les noms de sprite sont des codes de PERSONNAGE, les marqueurs des codes de
DÉCOR.** La correspondance n'est donc pas devinée : elle est lue dans le
fichier, marqueur par marqueur (§3).

Deux marqueurs de plus que de décors : **`ari` et `oro`**, à t=3000 et t=3060,
qui renvoient aux **mêmes** sous-compositions que `are` et `aur`. Ce sont deux
noms de rechange pour les deux mêmes lieux ; la table des icônes du binaire
écrit d'ailleurs `stage_icon_oro_c` là où l'AET écrit `stage_icon_aur_c`.

### 1.3 La grille du bas : l'ancre ne porte pas l'image

La grille est la table `0x180400210`, **21 cases de 0x20 octets**
(3 lignes × 7), choisie par `0x180174B60`, construite par `0x180173BD0`.
Le champ `+0x18` d'une case est un nom comme **`stage_icon_are_c`** — et ce
n'est **pas** un nom de sprite : c'est un **calque d'ancrage** de
`aet_s_selcmn.bin` (compo 188, calques 97 à 117, vingt-et-un, **tous de type
vidéo sans aucune source**). `0x1800298B0(objet, nom)` les retrouve par leur
nom et l'appelant y lit `+0x40`/`+0x44` : **x et y, rien d'autre**
(`documentation/mode_quest.md` §9.17 — 123 appelants, c'est une API courante).

L'image de la case, elle, vient de l'AET `aet_s_selstg` (compositions 3, 5
et 7, calques `s_selstg_icon_stage_<perso>.pic`).

À noter, parce que ça sert : les 21 noms d'ancre du binaire sont
`…_gym_c` et `…_oro_c`, et l'AET porte `…_jym_c` et `…_aur_c`. **Deux cases
sur vingt-et-une n'ont donc pas d'ancre** et sont placées par extrapolation
(`analysis/ajouter_un_decor.md` §6.3). Ce n'est pas un bogue de ce chantier,
c'est l'état du jeu.

---

## 2. Le dossier proposé, et comment le code y trouverait ses images

### 2.1 Le dossier

```
VF5RE\APERCUS_DECORS\
  LISEZMOI.md
  _SOURCE\        les trois `spr_s_selstg.farc` d'origine
  VF5FS\          apercu_<code>.png  vignette_<code>.png   (la reference)
  VF5R\           idem
  VF5\            idem
```

**Un nom par décor et par version** : le `<code>` à trois lettres nomme le
**lieu** (`ban`, `ter`, … `dur`, `gym`, `smo`, `rnd`), le **dossier** nomme la
génération. C'est la convention de `HD_TEXTURES\` (`EXTRACTED\` / `HD\`, un
nom qui *est* l'adresse de l'image), transposée.

Les PNG sont à leur **taille d'origine** : 1024 × 500 et 140 × 52 chez FS et
R, 1280 × 768 et 114 × 110 chez ver.B. Rien n'est recadré ici — c'est au
poseur de décider, et on ne jette pas de pixels en chemin.

### 2.2 Comment le code les trouverait — deux temps, par coût croissant

**Temps 1 — la repeinte, et elle ne change aucune instruction.**

Chaque grand aperçu est **seul sur sa texture**. Un poseur
`--apercus-decors` lit `APERCUS_DECORS\<VERSION>\apercu_<code>.png`, le met en
1024 × 500 dans une planche 1024 × 512, et écrit la texture du `<code>` dans
`rom\2d\spr_s_selstg.bin`. `tools/textures_hd.py` **reconstruit déjà le bloc
TXP entier et recalcule tous les offsets** ; la table d'adressage est celle-ci,
mesurée :

```
djo tex6   jin tex7   bar tex8   dur tex9   hai tex10  nyc tex11  umi tex12
ter tex13  gym tex14  ban tex15  sin tex16  cas tex17  slk tex18  are tex19
tan tex20  aur tex21  riv tex22  smo tex23  tak tex24  yuk tex25
```

Pour la vignette, même poseur mais **repeinte d'un rectangle** aux coordonnées
mesurées (`are` 338,138 ; `aur` 146,418 ; `ban` 2,362 ; … `smo` et `tak` sur
`MERGE_D5COMP_1`, 2,2 et 146,2), format 140 × 52.

*Piège à ne pas payer deux fois* : `txp.py` retourne les images DXT
verticalement après décodage (`FLIP_TOP_BOTTOM`). Le poseur doit re-retourner
avant de ré-encoder, sinon l'aperçu sort à l'envers — et une image à l'envers
dans une planche 1024 × 512 dont seules 500 lignes servent sort **décalée**,
pas seulement retournée.

Ce que ce temps 1 donne : l'écran montre l'image de la génération **choisie au
moment de la construction**. Il ne suit pas la barre espace.

**Temps 2 — suivre l'anneau de la barre espace.**

Les décors ajoutés ne sont pas des variantes cachées : ce sont des **décors à
part entière**, avec leur propre code à trois lettres et leur propre indice
(`outils/variantes_5r.py`, `outils/variantes_vf5.py`). La cible naturelle est
donc **un sprite par (décor, génération)**, nommé par le code de l'ajouté :

1. bâtir une planche supplémentaire `rom\2d\spr_s_selstg_gen.farc` portant,
   pour chaque code ajouté, `SPR_S_SELSTG_REND_STAGE_<CODE>` et
   `SPR_S_SELSTG_ICON_STAGE_<CODE>` — `bn5`, `bnb`, `d5r`, `dob`… ;
2. la déclarer dans `spr_db.bin` avec des identifiants libres :
   `tools/bases_2d.py` sait **déjà** ajouter une planche et des sprites, et
   `patch_moteur --bases-2d-libres` sait **déjà** démasquer `rom/2d/spr_db.bin`
   de l'archive `FArC` embarquée en `0x1804137F0` ;
3. au dessin, **substituer l'identifiant** : l'AET pousse `0x5222`… pour
   l'aperçu et `0x4E00`… pour la vignette, et le décor courant est dans
   `[TaskSelStage+0x5C]` — celui-là même sur lequel l'anneau de la barre
   espace agit déjà (`tools/variantes.cmd`).

Le point 3 est de la même famille que `--vignettes-costume`, qui reconstruit
déjà une table 19 × 6 d'identifiants de sprite (`0x1801CB030`). **Mais je ne
l'ai pas mesuré** : voir §5.

---

## 3. Le tableau décor × version × image

Correspondance **mesurée** marqueur → calque → sous-composition → sprite, et
confirmée **à l'œil** : les trois générations montrent bien le même lieu (le
contrôle le plus net est `yuk`, la cage de grillage sous la neige, bleu nuit
en FS, blanche en R, crépuscule en ver.B).

| code | ce que l'image montre | sprite FS / R | VF5 ver.B | VF5 R | VF5 FS | code ajouté ver.B | code ajouté R |
|---|---|---|:-:|:-:|:-:|---|---|
| `ban` | portail et muraille, montagnes | `…_LAU` | oui | oui | oui | `bnb` | `bn5` |
| `ter` | terrasse de bois, cerisiers | `…_KAG` | oui | oui | oui | `trb` | `tr5` |
| `nyc` | rue de ville la nuit | `…_JAK` | oui | oui | oui | `ncb` | `nc5` |
| `cas` | grande salle à lustres | `…_LIO` | oui | oui | oui | `csb` | `cs5` |
| `riv` | rivière, pitons karstiques | `…_SHU` | oui | oui | oui | `rvb` | `rv5` |
| `jin` | sanctuaire, verdure | `…_AOI` | oui | oui | oui | `jnb` | `jn5` |
| `sin` | pont dans la brume | `…_LEI` | oui | oui | oui | `snb` | `sn5` |
| `djo` | dojo sombre, braises rouges | `…_AKI` | oui | oui | oui | `dob` | `d5r` |
| `umi` | plage, palmiers | `…_JEF` | oui | oui | oui | `uib` | `ui5` |
| `hai` | hangar de bois | `…_GOH` | oui | oui | oui | `hib` | `hi5` |
| `are` | arène vitrée, projecteurs | `…_MSK` | oui | oui | oui | `aeb` | `ae5` |
| `slk` | falaises sculptées, échafaudage | `…_MON` | oui | oui | oui | `skb` | `sk5` |
| `yuk` | cage de grillage sous la neige | `…_WOL` | oui | oui | oui | `ykb` | `yk5` |
| `tak` | cascade et palmiers | `…_VAN` | oui | oui | oui | `tkb` | `tk5` |
| `aur` | aurore boréale | `…_SAR` | oui | oui | oui | `arb` | `ar5` |
| `bar` | salle vitrée, sol de verre | `…_BRA` | oui | oui | oui | `brb` | `br5` |
| `tan` | champ et rochers | `…_PAI` | oui | oui | oui | `tnb` | `tn5` |
| `dur` | colonnes et ruines | `…_DUR` | oui | oui | oui | `drb` `d2b` `d3b` `d4b` | `d15` `d25` `d35` `d45` |
| `gym` | salle de sport, ring | `…_KRT` | **non** | oui | oui | — | `gm5` |
| `smo` | arène de sumo | `…_TAK` | **non** | oui | oui | — | `so5` |
| `rnd` | « ??? » (vignette seule) | `…_RND` | **non** | vignette | vignette | — | — |

Lecture : « oui » = l'aperçu **et** la vignette sont sortis. `gym` et `smo`
n'existent pas en 2007 ; `rnd` n'a d'aperçu nulle part (sa case est une
animation, `random_top01`, et non une image).

### Ce que ça couvre, en comptes

* **44 décors ajoutés** au total : 23 côté VF5 R (19 lieux + 4 Dural),
  21 côté ver.B (17 lieux + 4 Dural, dont `drb` qui porte la géométrie).
* **38 images distinctes suffisent** — 20 pour R, 18 pour ver.B — et les
  38 sont là. Les huit Dural se partagent les deux `apercu_dur.png`, comme ils
  se partagent déjà `dur`/`dur_stay` dans le jeu d'origine.
* **Aucun décor ajouté ne reste sans image.**

---

## 4. Ce qui a été sorti, et d'où

| dossier | aperçus | taille | vignettes | taille |
|---|---:|---|---:|---|
| `APERCUS_DECORS\VF5FS` | **20** | 1024 × 500 | **21** | 140 × 52 |
| `APERCUS_DECORS\VF5R`  | **20** | 1024 × 500 | **21** | 140 × 54 |
| `APERCUS_DECORS\VF5`   | **18** | 1280 × 768 | **18** | 114 × 110 |

**118 PNG**, 59 Mo avec les trois `.farc` sources.

Sources, toutes déjà sur le disque — rien n'a été téléchargé ni dépaqueté de
`SOURCES\*.7z` :

| | image | chemin dans l'image |
|---|---|---|
| FS APM3 | `SOURCES\APM3_FS\` (déjà dépaqueté) | `rom/2d/spr_s_selstg.farc` |
| VF5 R | `VF5RE\extracted\LIND_R\vf5r_rom.bin` (ext2) | `/2d/spr_s_selstg.farc` |
| VF5 ver.B | `VF5RE\extracted\LIND_VF5\vf5.bin` (ext2) | `/disk1/rom/2d/spr_s_selstg.farc` |

`tools/ext2.py` existait déjà et lit ces images ; `tools/farc.py`, `tools/aet.py`
et `tools/txp.py` aussi. Le seul outil neuf est `tools/apercus_decors.py`, qui
ne fait que découper des sprites nommés — il n'y avait pas de découpeur de
sprite **par nom**, seulement des sorties de planche entière.

### Le piège de ver.B, et il est réel

L'écran de 2007 n'a pas la disposition de Final Showdown :

* son grand aperçu fait **1280 × 768** (le plein écran) et il est rangé en
  **deux morceaux** — `GRAPH_L_<CODE>01` 1024 × 768 et `GRAPH_L_<CODE>02`
  256 × 768 — que l'outil recolle gauche puis droite. Le raccord est invisible
  sur les dix-huit : vérifié à l'œil ;
* sa vignette est **presque carrée, 114 × 110**, et pas le rectangle large
  140 × 52 de FS. **Elle ne se pose pas telle quelle** ; il faudra la recadrer
  (bande centrale), pas l'étirer ;
* ver.B nomme ses sprites **par code de décor** (`GRAPH_L_BAN01`), R et FS
  **par code de personnage** (`REND_STAGE_LAU`). C'est pour ça que la
  correspondance du §3 est lue dans l'AET et non supposée : ver.B la
  **confirme** de l'extérieur, et les deux lectures concordent sur les dix-huit
  lieux communs.

---

## 5. Ce qui n'a PAS été vérifié

1. **Le point de substitution de l'identifiant de sprite n'est pas mesuré.**
   Je sais que l'AET pousse `0x5222`…/`0x4E00`… et que `SYSTEME_2D.md` §7
   décode un identifiant (`(h>>16)&0xfff` = la planche, `h&0xffff` =
   l'index) ; je **n'ai pas** trouvé ni désassemblé le site où l'on
   substituerait. Le temps 2 du §2.2 est donc une **proposition réalisable**,
   pas un chemin mesuré.
2. **Qu'une planche de sprites supplémentaire se charge sans toucher à
   `aet_db.bin`** : `bases_2d.py` ajoute toujours une planche AET *et* une
   planche de sprites ensemble. Une planche de sprites **seule**, sans scène
   AET, n'a jamais été posée dans ce chantier.
3. **Rien n'a été posé ni reconstruit.** Aucun `spr_s_selstg.bin` n'a été
   réécrit, aucune option de patcheur n'a été ajoutée, le binaire n'a pas
   bougé. Ce document et les 118 PNG sont tout ce qui a été produit.
4. **Rien n'a été vu à l'écran.** Les images ont été regardées en PNG, pas dans
   le jeu. Le cadrage exact de la vignette de ver.B recadrée, en particulier,
   est une mesure d'écran que je ne peux pas faire d'ici.
5. **La correspondance code de décor ↔ code de personnage** est mesurée dans
   l'AET et recoupée par les images ; les **noms de personnage** que j'ai
   employés pour l'expliquer (Lau pour `ban`, Jean pour `krt`…) sont, eux, une
   lecture et non une mesure. Rien dans le poseur n'en dépend : seul le code à
   trois lettres compte.
6. **`ari` et `oro`** : je constate deux marqueurs de plus que de décors, qui
   pointent les sous-compositions de `are` et `aur`, et une table d'icônes qui
   écrit `oro` là où l'AET écrit `aur`. Je n'ai **pas** cherché d'où vient
   cette seconde série de noms, ni si elle a un reste dans le code.
7. **Les générations console** (`SOURCES\PS3_VF5`, `SOURCES\X360_VF5`) portent
   elles aussi un `spr_s_selstg.farc` que je n'ai pas ouvert. Si une image de
   ver.B manquait ou sortait abîmée, c'est le premier repli.

---

## 6. En deux phrases

Le grand aperçu est **une texture entière par décor**, la vignette **un
rectangle dans une planche partagée**, et le code ne les nomme ni l'un ni
l'autre : il nomme un **marqueur** de `aet_s_selstg`, dont le nom *est* le
code à trois lettres du décor. Les **118 PNG** des trois générations sont dans
`VF5RE\APERCUS_DECORS\` — **20 décors couverts** en FS et en R, **18** en
ver.B, de quoi donner son image à **chacun des 44 décors ajoutés**.
---

## 7. LES APERÇUS DE VF5 ET DE VF5 R SONT POSÉS DANS LA PLANCHE (2026-11-20)

Frédéric : « au lieu de mettre uniquement une annotation sur la version du
décor choisi, change l'aperçu du décor dans la moitié supérieure de l'écran ».

**La moitié DONNÉES est faite et contrôlée. La moitié CODE ne l'est pas.**

### 7.1 Ce qui est en place

| pièce | état |
|---|---|
| l'outil | `VF5RE/tools/apercus_poser.py`, quatre actions `--essai --poser --controle --carte` |
| l'aller-retour | **identique à l'octet près** sur la planche d'origine : la carte du format est comprise |
| la planche posée | `rom/2d/spr_s_selstg.farc`, **68 textures** (30 + 38), 107 sprites, 18 959 836 o décomprimés |
| les 38 ajoutées | 20 VF5 R (index **30..49**) et 18 ver.B (index **50..67**), DXT1, 1024x512, comme les 30 d'origine |
| la carte | `VF5RE/analysis/apercus_index_textures.json`, lieu -> (fs, r, verb) |
| le `.par` | `spr_s_selstg.farc` **masqué** en `spr_s_selstg.far_` |

`gym` et `smo` n'ont pas de ver.B : leur entrée vaut `-1`, et c'est voulu.

Les trois aperçus de `jin` ont été **regardés en PNG**, pas comptés : FS, VF5 R
et ver.B sont à l'endroit, au bon cadrage. Et celui de **VF5 R montre
exactement la nappe de brume au premier plan** que Frédéric décrit sur `jn5` —
l'aperçu d'époque est, pour ce chantier-là, une mesure de plus.

### 7.2 DEUX FAUTES PAYÉES, et la seconde m'appartient

**1. La source n'était pas la planche du jeu.** `--poser` lisait
`APERCUS_DECORS/_SOURCE/APM3_spr_s_selstg.farc`, qui porte **105** sprites. La
planche que le moteur charge vient de `vf5fs_data.par` et en porte **107** :
il manquait `NAME_STAGE_GOH_E` et `NAME_STAGE_L_GOH_E`. Les 30 textures
différaient aussi. Un identifiant de sprite se décode en
`(rang de planche << 16) | index` : poser 105 sprites **décalait de deux tous
les index à partir du rang 32**, et tout l'écran se serait trompé de dessin.

**2. Et mon contrôle ne pouvait pas le voir.** Il comparait la planche posée à
**sa propre source**. C'est `CLAUDE.md` §4.6 mot pour mot : le contrôle visait
les mots, pas l'état. Un contrôle qui se mesure à ce qu'il a lui-même produit
ne peut échouer sur aucune faute d'amont.

**Le correctif** : l'arbitre est désormais `rom/2d/spr_db.bin`, la base que le
MOTEUR lit pour traduire un identifiant. Elle donne 107 noms pour la planche
511, dans l'ordre. `--controle` compare à elle, et il compare **aussi la
source**. Les deux états ont été vus :

    sur la planche fautive :  nombre de sprites 105 attendu 107   NON
    sur la planche juste  :   nombre de sprites 107 attendu 107   oui

Un contrôle qui échoue sur une faute réelle et réussit sur une pose juste.

**3. Et le `.par` passe AVANT le disque.** `spr_s_selstg.farc` y était encore
nommé : la planche posée sur le disque n'aurait **jamais** été lue. Masqué par
`tools/par_masquer.py` (un seul octet, réversible), et `--controle` le vérifie
désormais en trois états — nommé, masqué, archive illisible.

### 7.3 Le levier, lu dans `0x180174BF0`

La fonction qui rafraîchit l'aperçu bâtit sur la pile une table de **26
entrées de 0x18 octets** — `(indice de décor, nom A, nom B)` — la balaye en
`0x180175010`, et quand elle trouve `[RBX+0x5C]` elle joue **une composition
AET** par ces deux noms (`0x180171F40`). Elle sort sans rien faire si l'indice
n'a pas changé (`0x180174F55`), et **efface les trois couches** quand elle ne
trouve rien.

Donc : un lieu = une composition AET = **un sprite** = **une texture**. Faire
suivre la génération ne demande pas un dessin de plus, ça demande d'écrire
**un dword** — l'index de texture, à `+0x00` de l'enregistrement de `0x28`
octets du sprite, dans la table de rectangles de la planche chargée.

Les vingt sprites sont `REND_STAGE_<perso>`, index **71 à 90** selon
`spr_db.bin`, et le lieu s'en déduit par la table `LIEU_VERS_PERSO`
(`djo->aki, jin->aoi, bar->bra, dur->dur, hai->goh, nyc->jak, umi->jef,
ter->kag, gym->krt, ban->lau, sin->lei, cas->lio, slk->mon, are->msk,
tan->pai, aur->sar, riv->shu, smo->tak, tak->van, yuk->wol`).

### 7.4 CE QUI N'EST PAS FAIT, et il faut le dire

* **La greffe n'existe pas.** Rien n'écrit encore ce dword. À l'écran, l'aperçu
  reste aujourd'hui celui de Final Showdown quelle que soit la génération
  choisie par la barre espace.
* **Le résolveur de planche de CE binaire n'est pas identifié.** L'adresse
  `FUN_180198810` citée par `analysis/carte_sprite2d.md` vient du binaire
  **REVO**, pas de l'APM3 ; les octets du décodage (`shr 16 ; and 0xFFF`) n'ont
  **aucune occurrence** ici sous cette forme. Mesure en cours.
* **Les vignettes de la grille du bas** ne sont pas touchées : ce sont des
  rectangles dans une planche partagée, un autre travail.
* **Rien n'est passé à l'écran.** Aucune course n'a été demandée ni lancée.
---

## 8. LA GREFFE EST POSÉE : L'APERÇU SUIT LA GÉNÉRATION (2026-11-20)

Suite du §7, qui laissait la moitié code à faire. Elle est faite, posée et
contrôlée dans le binaire — **et elle n'est pas vue à l'écran.** C'est
Frédéric qui mesure l'écran.

### 8.1 Le levier, lu instruction par instruction

`carte_sprite2d.md` donne la table de rectangles à `[jeu+0x10]+0x10`. **Cette
note a été écrite sur le binaire de l'hôte REVO**, et dans l'APM3 l'expression
n'est ni `*(jeu+0x10)+0x10` ni `*(*(jeu+0x10)+0x10)` : le déplacement est
**auto-relatif**, le `0x10` servant à la fois de position du champ et de base
du déplacement. Lu en clair en `0x18018CB9A`..`0x18018CBCD` :

```
si [jeu+0xb8] == 0 : la planche n'est pas chargée, on abandonne
B    = *(int64*)(jeu + 0x10)
off  = *(int32*)(B + 0x10)            signé ; 0 = pas de table
rect = B + 0x10 + off + rang * 0x28
[rect + 0x00] = l'index de texture    <- le dword, lu en 0x18018CBCD
```

Se tromper d'un niveau, c'était écrire un entier dans un pointeur. La
différence ne se devinait pas : elle se lisait.

### 8.2 Et le résolveur de planche n'existe pas

Les planches ne sont **pas un tableau** : c'est une `std::map<uint32,
SPRSET>`, et MSVC a développé le `lower_bound` sur place. Le seul endroit où
il reste appelable, `0x18018C3B0`, rend des **flottants** — pas l'adresse
qu'on veut. On refait donc la descente, dix instructions recopiées de
`0x18018C3CD` :

| pièce | valeur |
|---|---|
| le conteneur | `*(void**)0x180719900` — lu en `0x180187A75`, pas supposé |
| `_Myhead` | `*(void**)conteneur` |
| la racine | `*(void**)(_Myhead + 8)` |
| le nœud | gauche `+0x00`, parent `+0x08`, droit `+0x10`, `_Isnil` `+0x19`, clé `+0x20`, **valeur `+0x28`** |

Et les clés sont les **ordinaux** : `0x18018C7D0` pré-remplit la carte avec N
`SPRSET` vides de clés 0..N-1. Le champ `id` de `spr_db.bin` ne sert pas de
clé ; c'est bien le **rang 511** qu'il faut.

On ne se contente pas du `lower_bound`, qui rend la première clé ≥ 511 : on
vérifie l'**égalité** avant de toucher quoi que ce soit, et la descente est
**bornée à 64 pas** — un arbre abîmé ne doit pas faire tourner le jeu sans
fin.

### 8.3 Où l'on se pose, et pourquoi là

À l'**entrée** de `0x180174BF0`, dont les treize premiers octets sont les
mêmes dans le `.origine` et dans la DLL du jour. `jmp rel32` + huit `nop`, et
le relais les rejoue avant de rendre la main en `0x180174BFD`.

**À l'entrée, donc avant la sortie rapide de `0x180174F55`.** Cette sortie
compare `[rbx+0x5c]` à sa valeur précédente — et quand la barre espace tourne,
`[rbx+0x5c]` ne bouge PAS : l'entrée B du socle rafraîchit toujours avec
l'indice de **base**, sinon la table de 26 entrées ne trouverait pas `jn5` et
effacerait les trois couches. Un relais posé après la sortie rapide n'aurait
donc jamais tourné au moment qui compte.

L'indice **réel**, celui qui porte la génération, l'entrée B le range dans un
créneau de la greffe du socle. **On le retrouve par contenu, jamais par
adresse** — on suit le `jmp` de `0x1801747C0` puis on cherche le motif
`8B 43 5C 89 05 <disp32>`. Trois états : trouvé, pas de détour
(`--variantes` absente), motif absent (le socle a changé). Dans ce build il
vit en `0x180EA1614`.

### 8.4 Ce qui est en place, mesuré dans le binaire produit

| pièce | état |
|---|---|
| l'option | `--apercus-generation`, dans `decors_vf5.cmd` |
| le relais | `0x180EB0D00`, 320 octets, relu au désassembleur |
| le détour | `0x180174BF0` → `e9 0b c1 d3 00` + huit `nop` |
| la table | 86 × 2 octets en `0x180EB0F00`, identique à `apercus_table_decors.json` |
| le créneau lu | `0x180EA1614`, celui que l'entrée B écrit |
| la DLL | md5 `e14d5572…`, était `4d100030…` (sauvegarde `.avant_apercus_20nov`) |
| les autres chantiers | `controle_decors_poses.py` : les six toujours en place |

Et `jin` donne bien ses trois textures : **7** en FS, **31** en VF5 R, **51**
en ver.B — exactement les trois qu'on a converties en PNG et **regardées**.

### 8.5 Les contrôles, et les deux états de chacun

`tools/controle_apercus.py`. Il a été vu **réussir** sur la pose juste et
**échouer** sur la sauvegarde d'avant (« LE PROLOGUE D ORIGINE EST INTACT —
rien n est pose »). `tools/apercus_generation.py --controle` relit chaque
entrée **à l'envers** et refuse qu'un lieu montre deux fois la même texture ;
on l'a vu échouer en faisant pointer `jin` VF5 R sur la texture de FS.

Une faute du contrôle lui-même, trouvée en le lançant : il désassemblait aussi
le **bourrage** de la zone et cherchait la dernière instruction, qui est un
zéro. Il refusait une pose juste. Corrigé : on cherche **le saut**, pas la fin,
et on exige qu'il soit unique et précédé du prologue rejoué.

### 8.6 CE QUI N'EST PAS MESURÉ

* **L'écran.** Rien n'a été lancé. Aucune course n'a été demandée.
* **Que `0x180174BF0` soit appelée à chaque trame de cet écran.** C'est lu
  dans l'entrée B du socle (`call 0x180174BF0` sans garde), pas observé.
* **Que la planche 511 soit chargée quand cet écran s'affiche.** Si elle ne
  l'est pas, `[jeu+0xb8]` vaut 0 et le relais ne fait rien — en silence, et
  c'est voulu.
* **Les vignettes de la grille du bas** : toujours intouchées.
---

## 9. L'ÉCRAN A TRANCHÉ — ET UNE RECONSTRUCTION AVAIT EFFACÉ 32 CHANTIERS

### 9.1 L'aperçu suit la génération. Mesuré à l'écran.

Course `20261120_1735`, lancée par `tools/course_apercus_20nov.cmd`. Frédéric,
sur la case d'Aoi, en appuyant sur ESPACE : **« oui, elle change »**. L'image
de la moitié haute suit le libellé de génération.

C'est l'issue **A1**, et elle **supersède le premier point du §8.6**, qui
disait « l'écran : rien n'a été lancé ».

Le journal de la course : 891 octets ajoutés, `vfes.exe` sorti en 0, aucune
trace d'exception — **A6** et **A7** écartées. Et il ne dit rien de l'aperçu,
par construction : cette course n'a aucune sonde.

**CE QUI N'EST PAS ENCORE RAPPORTÉ**, et qui ne l'est que par Frédéric :

* ~~que chacune des trois images soit le **bon** décor~~ — **rapporté : oui,
  les bons.** A1 est entière sur la case d'Aoi, et **A3 est écartée** ;
* que les **treize** générations de Dural suivent (3) ;
* qu'il existe une case où l'aperçu ne suit **pas** (**A8**).

### 9.2 La faute du jour : reconstruire avec une ligne plus étroite

Pour poser `--apercus-generation`, la greffe a été reconstruite par
`tools/decors_vf5.cmd`. **Une reconstruction repart du `.origine`** : toute
option absente de la ligne est un chantier qui disparaît du binaire, sans un
mot. Celle de `decors_vf5.cmd` portait **39** options là où le binaire en
place en portait **68**.

Trente-deux chantiers effacés — la brume d'Aoi, l'eau d'Eileen, `--menu-v2`,
les options, le terminal, le théâtre, le joueur 2 — et la résolution ramenée
de 1920×1080 à 1280×720. **À l'écran, le jeu avait l'air d'une ancienne
version.** C'est Frédéric qui l'a vu ; aucun contrôle ne l'avait dit.

**Et l'hôte l'avait dit, à la seconde 2 :**

```
[  2.000] RES  pas de zone VF5RESOL dans .greffe : le moteur n a pas ete
                patche avec --options-resolution
```

### 9.3 Pourquoi les contrôles n'ont rien vu

`controle_apercus.py` et `controle_decors_poses.py` ont tous deux rendu **0**
sur le binaire abîmé. Chacun ne regarde que **son** chantier. Aucun ne
vérifiait que la reconstruction **gardait** ce qui était déjà là. C'est le
§4.6 de `CLAUDE.md` sous une forme nouvelle : un contrôle qui vise ce qu'on
vient de poser ne voit pas ce qu'on vient de perdre.

Le diff entre les deux binaires faisait **187 plages, 7 830 octets**, là où la
greffe des aperçus en fait 505. Ce chiffre a été vu, et expliqué de travers
— mis sur le compte du réagencement de la greffe au lieu d'être cherché.

### 9.4 La provenance existait déjà

`runtime/media/vf5fs/ram/patch_empreinte.json`, que `patch_si_besoin.py`
écrit pour son cache, **garde la ligne entière** de la dernière
reconstruction. C'est `controle_decors_poses.py` qui l'a nommée, dans son
propre message d'échec. Elle était là depuis le 19 novembre à 23:24.

### 9.5 Deux gardes, chacune vue dans ses deux états

| garde | ce qu'elle fait | les états vus |
|---|---|---|
| `_garde_empreinte` | compare la ligne à l'empreinte **avant tout travail**, nomme chaque option qui tombe et chaque valeur qui change, et refuse sans rien écrire | refuse la ligne étroite (32 options + la résolution), passe la complète, cède à `--sans-empreinte` |
| l'enveloppe de `main` | remet la DLL d'avant dès que le patcheur rend autre chose que 0, ou qu'une zone `VF5XXXX` a disparu | vue remettre la DLL deux fois, sur un refus tardif puis sur un refus précoce |

L'enveloppe est nécessaire parce que `main` porte **52 `return 2` précoces**,
et que **le socle a déjà réécrit la DLL** quand ils tombent : la première
version de la garde, qui refusait à la fin, laissait la DLL dans l'état
socle-seul. Mesuré : `--options-v2 a besoin de --options-dural` a rendu 2 et
la DLL était passée de `4d100030` à `af5d8f06`.

**Et une faute de la garde elle-même, trouvée en la testant.** Elle passait là
où elle devait refuser : `io.open` dans un module qui n'importe pas `io`, et
un `except Exception` nu qui avalait le `NameError`. Elle rendait « pas
d'empreinte » au lieu de « illisible ». Le piège ne vise plus que `OSError`
et `ValueError`. *Un refus et une absence ne sont pas la même chose, et un
piège à tout faire les confond.*

### 9.6 Le contrôle qui prouve la réparation

Ni un marqueur ni un chantier : une **comparaison octet par octet** des trois
binaires contre le `.origine`, sur `.text`, `.rdata` et `.data`.

| | |
|---|---|
| octets que l'ancienne DLL patchait et qui seraient revenus au `.origine` | **0** |
| octets patchés à l'identique | 1 862 |
| octets patchés différemment (déplacements vers la greffe réagencée) | 31 |
| octets **ajoutés** | **13 — `0x180174BF0..0x180174BFC`, le détour, et rien d'autre** |

C'est le seul contrôle qui voyait les 726 octets que le compte des zones ne
voyait pas : il n'y a **pas de marqueur** pour la brume, l'eau ou le menu
grisé.

`decors_vf5.cmd` porte désormais les **70** options, avec le `rem` qui dit
pourquoi.
---

## 10. LE LIBELLÉ DE GÉNÉRATION, ALIGNÉ À GAUCHE

Frédéric, après avoir vu l'écran : « les 3 libellés n'ont pas la même longueur
et sont décalés par rapport à la gauche de l'écran, peux-tu faire en sorte que
la 1ère lettre du libellé soit toujours alignée de la même façon ? » — et :
« on laisse les aperçus de Dural tels quels ».

### 10.1 Pourquoi ils étaient décalés

Le relais du libellé, celui que `--variantes-texte` pose dans la greffe,
appelle l'envelopppeur de texte avec **le mot de drapeaux `0x28`** et un
descripteur dont **x1 == x2 == 640** — le milieu d'un écran de 1280. Le texte
est donc centré sur un **point**.

Les drapeaux se lisent en clair dans le **créneau 1 de
`app::PrintGC::vftable`** (`0x18034CC70`), soit `0x18019ADB0` :

| bit | ce qu'il fait |
|---|---|
| `0x01` | avance le curseur (`x1 += largeur`) |
| `0x02` | aligne à **droite** (`x1 − largeur`) |
| `0x04` | centre dans la boîte |
| **`0x08`** | **centre sur x1** (`x1 − largeur/2`) |
| `0x10` / `0x20` | les mêmes, en vertical |

`0x28` vaut `0x08 | 0x20`. **Sans aucun bit horizontal, l'origine reste `x1`
exactement** : c'est ce qui aligne les trois premières lettres.

**Et `0x18019B6F0`, auquel le relais passe 2, n'est PAS l'alignement : c'est
le sélecteur de POLICE** (`analysis/texte_2d.md`, correction du 2026-10-12).
Se tromper là, c'était changer la police en croyant déplacer le texte. Le grep
des notes avant de décompiler a servi exactement à ça.

### 10.2 Ce qui change : deux valeurs

| | avant | après |
|---|---|---|
| les drapeaux, en `0x180EA141D` | `0x28` | **`0x20`** |
| x1, en `0x180EA1620` | `640.0` | **`412.0`** |

`412 = 640 − 19 × 24 / 2` : 19 caractères pour « VIRTUA FIGHTER 5 FS », le plus
long des trois, et 24 px d'avance par caractère — la taille passée à
`0x18019B830` est 24.0, lue dans la greffe, et ce réglage vaut
`taille / chasse` avec une chasse de 48 pour la police 2. Le plus long des
trois libellés ne devrait donc pas bouger, et les deux autres s'aligner sur
lui.

**CETTE AVANCE EST DÉRIVÉE, PAS OBSERVÉE À L'ÉCRAN.** L'alignement, lui, n'en
dépend pas : si les trois tombent ensemble mais trop à gauche ou trop à
droite, c'est ce seul flottant qu'il faut bouger.

### 10.3 Repéré par contenu, jamais par adresse

Le socle place son relais où il veut, et il a déjà bougé deux fois. Deux
repères, mesurés le 2026-11-20 sur ce binaire :

* le site : `BA 28 00 00 00` + `48 8D 0D <d32>` + `E8 <d32→0x18019B2E0>` —
  **un seul dans toute la DLL**, là où un `mov edx,0x28` tout court y
  apparaît **81 fois** ;
* le x : le seul `vmovss xmm0,[rip+d32]` du corps du relais dont la cible
  porte `640.0` — **un seul**, l'autre valant 470.0 (le y).

Chacun rend **trois** états : trouvé, absent, ambigu. Le refus de la seconde
pose disait d'abord « `--variantes-texte` n'est pas posée » sur une DLL
**déjà alignée** : il cherche maintenant le même motif avec les drapeaux
d'après avant de conclure.

### 10.4 Les contrôles, et les trois qui étaient faux

`tools/libelle_gauche.py --controle` vise l'état : un seul site à `0x20`, plus
aucun à `0x28`, le bit `0x08` retiré, le `0x20` gardé, un seul x à 412.0, plus
aucun à 640.0. Vu **échouer** sur la DLL non posée, **réussir** après la pose,
dire « DÉJÀ POSÉ » à la seconde, et « section `.greffe` ABSENTE » sur le
`.origine`.

**Trois contrôles de la journée étaient faux, et ce sont des fichiers intacts
qui les ont fait tomber :**

1. le garde du pilote lisait `demandes` pour y chercher `--variantes-texte`.
   Mais `demandes = [a for a in argv if a in NOUVELLES]` : une option **du
   socle** n'y est jamais. Il a refusé une ligne juste — *un contrôle qui
   échoue sur une pose correcte ne vaut pas mieux qu'un contrôle qui passe sur
   un fichier cassé* ;
2. le poseur du `.cmd` comptait `>nul` dans **tout** le fichier : il y en a
   onze, un par commande. Ce qui compte, c'est qu'il y en ait un sur la ligne
   de patch, donc **sur la ligne aplatie** ;
3. le même poseur comparait les options de la ligne neuve à celles de **tout
   le fichier** : `--controle`, `--retirer`, `--poser-lot` et
   `--bases-seules`, qui appartiennent à d'autres commandes du `.cmd`, étaient
   comptées comme perdues.

Les deux derniers, c'est le §4.6 de `CLAUDE.md` mot pour mot : compter une
chaîne dans tout un fichier, ce n'est pas viser l'état.

### 10.5 La reconstruction, prouvée

| | |
|---|---|
| empreinte avant | `2A1F276CF41FDE4D4694CAC8CFCDAD0C` |
| empreinte après | `14AB5A7D68DFD14752E13647CCDCA0EA` |
| taille | 7 181 824 → **7 181 824** |
| octets différents | **3** — `0x6A4C1D` (le drapeau) et `0x6A4E22..23` (le flottant ; 640.0 et 412.0 partagent leurs deux octets bas) |
| zones gardées | les quatre : `VF5MODE`, `VF5NAME`, `VF5OPTV2`, `VF5RESOL` |
| contrôles | `libelle_gauche` 0, `controle_apercus` 0, `controle_decors_poses` 0 |

Et deux refus vus en vrai, chacun remettant la DLL d'avant en place : la ligne
sans `--variantes-texte`, et la ligne complète avant la correction du garde.

**`tools/decors_vf5.cmd` n'a PAS été rejoué en entier** : il **lance le jeu**
à la fin, et une course demande un « oui, lance ». Seule sa ligne de patch a
été exécutée — ses étapes d'avant (les deux bases, le shader `ykb`, `apm.dll`)
étaient déjà passées lors de la tentative refusée.

### 10.6 Ce que l'écran n'a pas encore dit

**Rien de la §10 n'est mesuré à l'écran.** Il reste à voir :

* que les trois premières lettres tombent bien au même endroit ;
* que `412.0` place le bloc où il faut — les trois alignés mais trop à gauche
  ou trop à droite est une issue à part entière, et elle ne remet pas
  l'alignement en cause ;
* que le libellé n'est pas rogné ni sorti de l'écran à 1920×1080.
---

## 11. L'ÉCRAN A TRANCHÉ L'ALIGNEMENT. LE PLACEMENT EST UN CHOIX.

### 11.1 Ce que l'écran a dit

Course **`20261120_1803`**, lancée par `tools/course_libelle_gauche_20nov.cmd`.
Les trois contrôles d'avant-course à 0, `vfes.exe` sorti en 0, journal
215 392 → 216 059 octets (667 ajoutés, **lus en entier**), **aucune
exception** — B9 et B11 écartées. Aucune sonde, par construction.

Frédéric, sur la case d'Aoi : **« il ne bouge plus »**. Les mots
« VIRTUA FIGHTER 5 » restent au même endroit, seule la fin change.

**L'ALIGNEMENT EST ACQUIS, ET MESURÉ À L'ÉCRAN.** Retirer le bit `0x08` du mot
de drapeaux était la bonne lecture : sans bit horizontal, l'origine reste
`x1`. L'issue B1 est tranchée et n'est plus à mesurer. Elle **supersède
le §10.6**, qui disait « rien de la §10 n'est mesuré à l'écran ».

Deux choses que le journal a corroborées au passage :

* `police mode 0 / 1 / 2`, trois descripteurs et rien de plus — il n'y a bien
  que **trois polices**, et le `edx=2` du relais était le sélecteur de police,
  pas l'alignement ;
* `fenetre : 1280 x 720 demandes` — 640 était donc réellement le milieu. Le
  placement est calculé pour **cette** largeur ; en 1920 il voudrait une autre
  valeur. **Non mesuré.**

### 11.2 Une phrase lue à l'envers, et une reconstruction pour rien

Frédéric, ensuite : **« décale de l'équivalent de 2 lettres vers la droite »**.
C'était une **consigne**. Elle a été lue comme la **description d'un défaut**
— « il est 2 lettres trop à droite » — et x1 est passé de 412 à **364**, avec
reconstruction, contrôles et tout. Sa réponse : **« non, je veux le
contraire !!!! décale PLUS vers la droite de 2 lettres »**.

Il n'y avait rien à deviner. Le sens d'une consigne ne se mesure pas : il se
lit, ou il se demande. Une reconstruction a été dépensée pour ça.

### 11.3 Les trois valeurs de x1, et ce qui les a produites

| x1 | d'où elle vient | empreinte de la DLL |
|---|---|---|
| 640.0 | le socle, le milieu de l'écran | `2A1F276CF41FDE4D4694CAC8CFCDAD0C` |
| 412.0 | **dérivée** : `640 − 19 × 24 / 2` | `14AB5A7D68DFD14752E13647CCDCA0EA` |
| 364.0 | la consigne lue à l'envers | `61C2608C79B47296B4B88DFEC81DFBB6` |
| **460.0** | **la consigne** : `412 + 2 × 24` | `9C7EC2D1F8EF5A63D49A493D2B6A6496` |

Taille inchangée à chaque fois (7 181 824), les quatre zones gardées, et
**un seul octet différent** entre deux valeurs de x1 : `0x6A4E22`. Rien
d'autre n'a bougé dans le binaire.

L'avance de **24 px par lettre reste dérivée, jamais mesurée à l'écran**. Si
un décalage demandé de 2 lettres n'en fait pas 2 à l'écran, c'est elle qui est
fausse — et c'est la seule chose de ce chantier qui tienne encore à un calcul.
Le réglage se fait désormais **en lettres**, par `LBG_X_LETTRES`.

### 11.4 Ce qui n'est pas mesuré

* que x1 = 460 place le bloc là où Frédéric le veut ;
* que le libellé soit entier à cette abscisse (issue B6) ;
* la fenêtre annoncée en 1280 × 720 alors que le moteur est patché en
  1920 × 1080 ;
* les treize générations de Dural et l'issue A8, laissées de côté à sa
  demande.
