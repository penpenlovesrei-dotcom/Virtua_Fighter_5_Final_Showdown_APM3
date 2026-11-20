# Les cinq chantiers demandes

Enonces le 2026-09-03. Ce document ne planifie pas : il dit, pour chacun, **ce
qui est deja etabli**, **ce qui bloque**, et **quelle est la premiere mesure**.
Les quatre premiers sont ouverts. Le cinquieme est bloque sur du materiel qu'on
n'a pas.

---

## 1. Reactiver les menus de la version console

**Etabli.** Le binaire APM3 *est* le binaire console. Sur 56 sous-etats, sept
seulement sont ceux de la borne ; les 49 autres sont le parcours console, et le
code des menus est compile dedans (2 references par chaine de menu). Detail dans
`analysis/parente_console.md`.

**Ce qui bloque.** Rien de structurel — c'est un probleme d'**atteignabilite**.
Il faut amener la machine a etats sur un etat qu'elle n'emprunte jamais, comme
la deviation `50 -> 52` qui a ouvert le DOJO. Trois freins connus :

- les **predicats neutralises** (`0x180007450` = `xor al,al ; ret`, toujours zero) ;
- les **ressources** de chaque ecran, a verifier une par une dans les `.farc` ;
- les **arriere-plans** absents : sauvegarde de profil, serveur, terminal.

**Premiere mesure.** `py -3 tools/tracer_etats.py --devier 49 36` (au lieu de
`APM3_SELECTOR`, demander `MENU_MAIN`) puis capture. Trois minutes. Un ecran
noir, un gel ou un menu : les trois reponses sont informatives.

**Ordre a suivre**, du plus au moins accessible :

| cible | pourquoi |
|---|---|
| ~~`DATA_TEST_*` (21 a 35)~~ | **ECARTE** : compile hors du build. Quatre captures identiques a l'octet pres en martelant les 13 codes ; chaque nom n'apparait qu'une fois, dans la table de noms |
| `MENU_MAIN` (36), `CS_TRAINING` (41) | code present, ressources a verifier |
| `CS_TERM_*` (37 a 40) | le poste de personnalisation ; suppose une sauvegarde |
| `ONLINE_*` (42 a 47) | suppose un serveur ; sans espoir hors ligne |

---

## 2. Rendre Dural jouable

**Etabli.** Ses donnees sont completes : `mothead_DUR.bin`, `ctrl_DUR.bin`,
726 roles sur 726, quatre finitions de corps dans `dur_itm.csv`. Et surtout,
l'accesseur `0x18012CA90` borne par `cmp ecx, 0x15` : **l'indice 20 est valide**,
et la table qu'il indexe porte en 20 le code `DUR` et le nom `DURAL`.

**Ce qui bloque.** Uniquement l'**interface** : aucune case dans la grille de
selection, et pas de planche d'icones `spr_t_itmdur.farc`. La grille n'a pas ete
retrouvee, ni comme ordre affiche ni comme table.

**Ce qui a echoue, et pourquoi.** Deux impasses instructives :

- point d'arret **materiel en ecriture** sur `ROB+0x10` : **zero acces en 245 s**.
  Le champ est ecrit a la construction du ROB, avant que son adresse existe.
- **balayage memoire** du choix de personnage en zone d'image : **zero adresse**.
  Le choix vit sur le tas, dont les adresses ne survivent pas d'une execution a
  l'autre. La comparaison a deux passes doit donc se faire **dans une seule
  execution**, entre deux combats successifs.
- la substitution a `0x180151F5E` n'a **jamais ete frappee** : point d'arret pose
  trop tard, et cette fonction est un automate a saut par table.

**Premiere mesure.** Deux voies, la seconde etant nouvelle :

1. poser le point d'arret **des le chargement du moteur**, sur les quatre sites
   de `mot_%s.bin` a la fois, et compter les passages avant d'ecrire quoi que ce soit ;
2. ~~`DATA_TEST_CHR` et `DATA_TEST_MOT`~~ : **voie fermee**, ces ecrans sont
   compiles hors du build (voir `analysis/etats_console_essais.md`).

---

## 3. Choix de la resolution -- **FAIT**

Verifie a l'ecran en 1280x720 : « plus de zoom et fluide » (2026-09-03).

**Quatre immediats, dans DEUX binaires** -- `vfes.exe` (`0x140002FD6`,
`0x140002FDD`) et le moteur (`0x1800E74A6`, `0x1800E74B0`). Corriger `vfes.exe`
seul laisse le moteur creer ses cibles et sa vue en 1920x1080.

Outil `tools/patch_resolution.py`, lanceur `lancer_resolution.cmd`, originaux
conserves en `.origine`. Detail et impasses dans `analysis/resolution.md`.

Restent non essayes : les six autres modes du lanceur, et le passage a un
anticrenelage superieur (le jeu est deja en 8x sur ses cibles internes).

---

## 4. Tous les decors de Dural

**Etabli, et la moisson est bonne.** Le dump APM3 porte **26 decors**, dont
**six sont ceux de Dural** :

`EFFSTGDUR`, `EFFSTGDU1`, `EFFSTGDU2`, `EFFSTGDU3`, `EFFSTGDU4`, `EFFSTGDU5`

Chacun avec son ambiance sonore (`se_stage_du1.csb` … `se_stage_du5.csb`), et
`objset/dur.farc` pour les objets. Les vingt autres :

`ARE AUR BAN BAR CAS DJO GYM HAI JIN NYC RIV SIN SLK SMO TAK TAN TER TS3 UMI YUK`

**Ce qui bloque.** Comme pour le personnage : la **selection**. Il faut trouver
la table qui associe un decor a un combat, et l'ecran `aet_s_selstg` /
`spr_s_selstg` qui la presente.

**Premiere mesure.** Chercher la table des decors comme on a trouve celle des
personnages : un tableau de codes a trois lettres, borne par un `cmp`. La methode
a marche une fois, elle remarchera.

---

## 5. Importer les decors de VF5 R et VF5

**VF5 R est arrive** (2026-09-03) : `vf5r.7z`, 4,66 Go, deux images ext extraites
dans `extracted/LIND_R/`. Resultat complet dans `analysis/decors_vf5r.md`.

**Le resultat principal est negatif, et il faut le dire d'abord :** VF5 R
**n'apporte aucun decor nouveau**. Les deux jeux declarent 41 emplacements, dont
17 entrees d'essai identiques ; VF5 R a 23 decors reels, APM3 en a 24 — les
memes, plus `DU5`.

**Le gisement est ailleurs** : ce sont des **versions plus riches des memes
decors**. Cinq ont perdu 4 a 8 Mo en passant de R a Final Showdown — `DJO`
(-8,1), `SIN` (-8,1), `SMO` (-7,3), `NYC` (-6,9), `DU3` (-4,3) — quand trois
autres en gagnaient autant (`GYM` +13,3, `JIN` +4,8, `BAN` +4,3) et que `AUR` ne
bougeait pas d'un octet. Ce sont des remaniements decor par decor, pas une
recompression.

**Deja acquis sans rien importer** : les 278 pistes du dump APM3 comportent deja
**29 `vf5r_*` et 23 `vf5rb_*`**. Chaque decor a ses trois generations de musique
cote a cote. L'ambiance sonore de R est deja dans le jeu.

**Premiere mesure.** Ouvrir `stgdjo.farc` des deux cotes — le plus gros ecart sur
un decor de taille moyenne — et lister la difference d'objets. On saura alors
*ce qui* a ete retire, et si cela vaut d'etre remis.

**VF5 d'origine** n'est pas encore mis a disposition.

**Reserve.** Rien ne garantit que le format `objset` de 2008 soit lu par le
moteur de 2010. A verifier avant toute transplantation.

---

## L'ordre que je propose

1. ~~**Resolution**~~ — **fait**, verifie a l'ecran.
2. ~~**`DATA_TEST_*`**~~ — **fait, et negatif** : les quinze ecrans sont
   compiles hors du build. La voie courte vers Dural n'existe pas.
3. **Dural** — selon ce que donne le point 2.
4. **Decors** — meme methode que pour les personnages.
5. **Lindbergh** — comparer `disk0` et `disk1`, puis s'arreter faute de materiel.
