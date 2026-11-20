# LE SYSTEME 2D DE VF5FS : AET + SPR

Index du 7 novembre 2026 (SS 395 a 402). **A lire avant de decompiler quoi
que ce soit du 2D**, des deux cotes.

- Cote APM3 : `FS APM3\code_decompile\` -- **22 fichiers 2D, 2025 lignes,
  tous lus**, plus `FS APM3\analysis\texte_2d.md`.
- Cote REVO : ce dossier, `FUN_<adresse>.c`. **Faire `ls FUN_<adresse>.c`
  avant toute nouvelle decompilation** -- le 7 novembre, quatre fonctions
  « trouvees » etaient deja la.

## 0. LE BINAIRE, ET C'EST LA PREMIERE CHOSE A VERIFIER

Les adresses de ce fichier portent sur **`FS REVO\
vf5fs-pxd-w64-d3d12_SteamRetail.dll`, 7 229 952 octets**, celui que l'hote
charge (`kModuleDefaut`, resolu depuis `cd /d "%BANC%"` avec
`BANC=...\FS REVO`) et celui du projet Ghidra `vf5fs_revo`.

**Trois autres copies existent et sont des builds DIFFERENTS** :
`oracle_janvier2025\` (6 974 976 o), et `...World Stage\runtime\media\vf5fs\`
= `FS APM3\banc_revo\` (7 189 504 o). Un desaccord entre un balayage d'octets
et Ghidra n'est jamais une erreur de Ghidra : ce sont deux fichiers.

## 1. L'APPARIEMENT APM3 <-> REVO

Etabli **par la forme** (chaine d'appels, constantes, disposition), jamais par
l'adresse : les builds ne partagent aucune adresse.

```
APM3 : void FUN_180187a10(a,b) { FUN_18018bbd0(DAT_180719900, a, b); }
REVO : void FUN_180195d80(a,b) { FUN_180198990(DAT_18075e010, a, b); }

APM3 : void FUN_180187af0(c) { *c = 5; FUN_18018ca20(DAT_180719900, c); }
REVO : void FUN_180195e40(c) { *c = 5; FUN_180199890(DAT_18075e010, c); }
```

### Le systeme de sprites (SPR)

| role | APM3 | REVO |
|---|---|---|
| `SprMgr` | `DAT_180719900` | `DAT_18075E010` |
| `SprSet` | `DAT_180719908` | `DAT_18075E018` |
| **mettre un sprite en file** | `FUN_18018CA20` | **`FUN_180199890`** |
| rendre un GROUPE (32 paniers) | `FUN_18018BBD0` | `FUN_180198990` |
| dessiner UN sprite | — | `FUN_180197C30` |
| API « genre 5 » (texte) | `FUN_180187AF0` | `FUN_180195E40` |
| API generique | `FUN_180187C00` | cluster `0x180195D70`-`0x180196140` |
| initialiser le `SprMgr` | `FUN_18018C7D0` | a apparier |
| dessiner un caractere | `FUN_180108320` | a apparier |

### Le systeme d'animation (AET)

| role | APM3 | REVO |
|---|---|---|
| `AetSet` | `DAT_18066B738` | `DAT_1806AF3B8` |
| `AetMgr` | `DAT_18066B750` | `DAT_1806AF3D0` |
| creer, interne | `FUN_180026790` | `FUN_1800222A0` |
| detruire, interne | `FUN_180027430` | `FUN_180022EB0` |
| creer, API | `FUN_180029A90` | `FUN_180025E10` |
| **detruire par identifiant** | `FUN_180029BF0` | `FUN_180026140` |
| parcourir les couches (A L'ENVERS) | `FUN_180025440` | a apparier |
| evaluer une couche | `FUN_180025870` | a apparier |
| objet AET -> commande de sprite | `FUN_180023930` | a apparier |
| batir la transformation 2D | `FUN_180023650` | a apparier |
| resoudre un sprite par identifiant | `FUN_180027900` | a apparier |
| echantillonner une SEQUENCE | `FUN_180026530` | a apparier |
| poser les reglages de creation | `FUN_180027AE0` | a apparier |

`FUN_180026140` est ce que `FUN_1801A4180` (le lanceur du voile) appelle en
boucle sur un tableau de **19 identifiants** en `&DAT_18079573C`, en sautant
l'indice 0.

### Les modes d'ecran

| role | APM3 | REVO |
|---|---|---|
| **table des resolutions**, 17 x 0x1C | `DAT_1803FEB20` | **`0x180427F80`** |
| table des rapports, 17 x 17 paires | `DAT_180714010` | a apparier |
| bloc du **MODE COURANT** | `0x1806490D0` | **`0x180643BE0`** |
| remplir un descripteur de mode | `FUN_18016AEC0` | **`FUN_180179C60`** |
| rendre le bloc courant | `FUN_18016B0C0` | **`FUN_180179E70`** (40+ appelants) |
| poser le mode + batir la table | `FUN_18016B0D0` | **`FUN_180179E80`** (UN appelant) |
| convertir un point entre modes | `FUN_18016AF60` | a apparier |
| l'initialisation qui pose tout | `FUN_1800DA2C0` | **`FUN_1800E14C0`** |
| **le mode, en dur** | `FUN_1802447F0` | **`FUN_1802CB530` = `MOV EAX,0xD ; RET`** |

## 2. LES STRUCTURES -- ATTENTION AU DECALAGE DE -0x10

**La structure de sprite de REVO est celle d'APM3 decalee de -0x10.**

| champ | APM3 | REVO |
|---|---|---|
| genre (1 = ne dessine rien) | `+0x10` | `+0x00` |
| identifiant de sprite | `+0x14` | `+0x04` |
| drapeaux (bit `0x20000000` : pas de melange) | `+0x1C` | `+0x0C` |
| index de melange (table `DAT_1806440C0`) | `+0x20` | `+0x10` |
| **resolution SOURCE** (`0x11` = aucune) | `+0x30` | `+0x20` |
| **resolution DESTINATION** (`0x11` = aucune) | `+0x34` | `+0x24` |
| pointeur de TEXTURE | `+0xB0` | `+0xA0` |
| decalage des sommets | `+0xC0` | `+0xB0` |
| compte des sommets | `+0xC8` | `+0xB8` |
| drapeaux de construction | `+0xD0` | `+0xC0` |
| sprite suivant dans la chaine | — | `+0xF0` |

La **commande** de sprite (ce qu'on passe a la mise en file) :
`+0x00` genre (0 = sprite par identifiant, 2 = rectangle, 5 = texte),
`+0x04` identifiant (`0xFFFFFFFF` = aucun), `+0x08` la couleur empaquetee,
`+0x14` **couche** (`-1` -> `mgr[0x105]`), `+0x18` decalage de groupe,
`+0x1C` **priorite, le numero de panier 0..31**.

Le **panier** fait **0x10 octets** : tete en `+0` (ce que le rendu parcourt),
queue en `+8` (ce que la mise en file relit). Le tableau commence a `mgr + 8`,
32 paniers par groupe, `0x200` octets par groupe.
**REVO parcourt une liste simple ; APM3 une liste CIRCULAIRE a sentinelle.**

La **texture** : `+0x0C` largeur (`short`), `+0x0E` hauteur (`short`),
`+0x14` **format**, et `0x39a` veut dire « UV deja normalisees ».

L'**objet AET** : `+0x28`/`+0x2C` debut et fin, `+0x30` drapeaux
(bit `8` = couche desactivee, bit `0x100000` = **etirer a la taille de la
COMPOSITION**), `+0x34` couche, `+0x38` groupe, `+0x3C` priorite,
`+0x78`/`+0x7C`/`+0x80`/`+0x84` R, V, B, A, `+0x88` image courante,
`+0x9C` commande differee (rangee en `+0xA0..+0x180`), `+0x94` alpha heritee.

Le **descripteur de couche AET** fait 0x30 octets, parcouru **a l'envers** :
`+0x04` image de debut, `+0x08` de fin, `+0x0C` decalage de temps,
`+0x10` echelle de temps, `+0x14` drapeaux (bit 0 = visible),
`+0x17` genre (1 = sprite, 2 = desactive, 3 = sous-composition),
`+0x18` -> la sous-composition, `+0x28` -> les proprietes (opacite en `+0x3C`).

Le **bloc du mode courant** (`0x180643BE0` dans REVO) : `+0x00` l'index du
mode, `+0x0C` la largeur, `+0x10` la hauteur, `+0x18` le rapport en double,
`+0x20` la classe d'aspect.

Le **contexte de police** (`DAT_18070FB38` dans APM3) : `[0]`,`[1]` position,
`[6]`..`[9]` deux echelles, **`[0xE]` la couleur dont l'octet de poids fort
est l'ALPHA**, `[0x10]` drapeaux, `[0x16]` le mode (61 -> genre 5),
`[0x20]` le jeu de sprites, `[0x22]` une taille, `[0x3B]` l'alpha source / 255.

## 3. LA TABLE DES RESOLUTIONS (`0x180427F80`, identique dans les deux builds)

17 entrees de 0x1C octets : `+0x00` largeur flottante, `+0x04` hauteur
flottante, `+0x08` classe d'aspect (octet), `+0x14`/`+0x18` largeur et hauteur
en entiers. **`0x11` = « le mode courant ».**

| mode | taille | classe | mode | taille | classe |
|---|---|---|---|---|---|
| 0 | 320x240 | 0 | 9 | 1280x768 | 1 |
| 1 | 640x480 | 0 | 10 | 1360x768 | 1 |
| 2 | 800x600 | 0 | 11 | 1920x1200 | 1 |
| 3 | 1024x768 | 0 | 12 | 2560x1536 | 1 |
| 4 | 1280x1024 | 0 | **13** | **1280x720** | 1 |
| 5 | 1400x1050 | 0 | 14 | 1920x1080 | 1 |
| 6 | 1600x1200 | 0 | 15 | 2560x1440 | 1 |
| 7 | 800x480 | 1 | 16 | 3840x2160 | 1 |
| 8 | 1024x600 | 1 | | | |

**Le mode de REVO est 13 = 1280x720, en dur** (`FUN_1802CB530`), ce qui est
exactement notre cible de rendu. Rien a corriger de ce cote.

Le convertisseur est **centre** :
`sortie = (entree - 0.5 * taille[src]) * rapport + 0.5 * taille[dst]`,
avec `table[a*17 + b] = { largeur[a]/largeur[b], hauteur[a]/hauteur[b] }`.
**`DAT_180346D38` vaut donc 0.5** (confirme), et `DAT_180346D3C` vaut 1.0.

Le facteur VERTICAL est **ecrase** dans trois cas (meme classe d'aspect mais
un seul des deux modes dans `{10, 13..16}` -> y prend le rapport des
LARGEURS ; destination 3, 0xD ou 0xE -> constantes), plus une correction quand
la destination vaut 9 ou 3. **Une mise a l'echelle non uniforme autour du
centre est le comportement normal du moteur.**

## 4. LES DEUX CHAINES

### L'ordre de dessin, decide A LA CREATION

```
reglages de creation [0xb][0xc][0xd]          (FUN_180027AE0, APM3)
   -> objet AET +0x34 / +0x38 / +0x3c
      -> commande de sprite +0x14 / +0x18 / +0x1c   (FUN_180023930, APM3)
         -> index de panier (((cmd+0x18)+couche)*0x20 + (cmd+0x1c) + 1)*0x10
            -> l'ordre ou FUN_180198990 (REVO) les dessine
```

**Aucun tri nulle part ailleurs.** Agir sur le TIRAGE ne peut donc jamais
corriger un ordre -- c'est ce qui condamne les quatre criteres d'omission du
7 novembre.

### Les UV, ecrites en PIXELS

```c
v[0xc]  = v[0xc] / largeur_texture;                  // u
v[0x10] = (hauteur_texture - v[0x10]) / hauteur;     // v RETOURNE
```
sauf si le format de la texture vaut `0x39a`. Donc une fenetre mesuree
`u 2->18, v 14->30` sur une 32x32 veut dire que l'animation a authore
`u 2->18, v 2->18` : **un carre de 16x16 pixels**, c'est-a-dire un APLAT DE
COULEUR. Et la TAILLE du quad sort de la projection ortho de
`FUN_180198990`, pas des sommets.

### Le rendu d'un groupe

`FUN_180198990(mgr, groupe, resolution)` : si `resolution == 0x11`, prendre le
mode courant ; poser la projection ortho `(-fx, fx, fy, -fy)` avec
`fx = hauteur * 0.5 * mgr[0x810] * K / rapport_aspect` **et** un rectangle de
decoupe -- **sauf pour le groupe 1**, qui n'a ni l'une ni l'autre et joue a la
place sur `mgr+0x82C`. Puis les 32 paniers : dessiner, delier, liberer
(noeud de 0xF8 octets cote APM3).

Couche 11 -> groupe 0, couche 6 -> groupe 1, couche 13 -> groupe 2,
couche 12 -> groupe 3. La couche 10 fait un effacement reel
(`FUN_1802DC4E0(0x4000)`).

### Le cycle de vie d'un objet AET

Creer incremente un compteur en `[mgr+0x88]` et insere dans un **arbre
rouge-noir** en `[mgr+0x68]` ; detruire se fait **par identifiant**.
**Un objet AET SURVIT aux images.** `FUN_180198990` vide bien ses 32 paniers
a chaque image, mais les objets vivants les re-remplissent : du contenu d'une
scene precedente qui persiste est donc une **destruction manquante**, jamais
un tirage a omettre.

Le **fondu retire le quad** : la mise en file n'a lieu que
`if (seuil DAT_180346D34 < |alpha|)`. Chercher un quad a alpha decroissante
est une fausse piste par construction.

Une couche de sprite peut etre une **sequence animee** (`+0xC` le nombre
d'images, `+0x8` la cadence), et le bit 3 des drapeaux fait **fondre trois
images voisines**.

## 5. L'INSTRUMENT, ET LA LEÇON

Toutes les mesures du 7 novembre ont ete prises **au tirage D3D**, tout en
bas, ou un quad blanc plein ecran ne se distingue d'un fond legitime que par
sa taille -- quatre criteres, quatre echecs.

> **NUANCE AU SS 406.3.** J'avais ecrit ici « la taille n'etait pas une
> preuve ». Trop fort. La taille **absolue** sort de la projection ortho, et
> le facteur x differe du facteur y par construction, donc un depassement de
> la cible ne prouve pas qu'un quad est illegitime. Mais **dans un meme
> groupe et une meme projection, la taille EST discriminante** : le rideau
> mesure 1284.8 x 776.0 quand les contenus du meme site de tirage font
> 640x720 au maximum. Ce qui faisait clignoter le critere etait la lecture
> CPU des sommets, pas le critere lui-meme.

**Quand la question porte sur l'ORDRE ou la COMPOSITION, sonder la mise en
file (`FUN_180199890`) ou l'arbre des objets AET, jamais le tirage.**

La sonde qui reste a poser : parcourir l'arbre des objets AET une fois par
image et donner, par objet, l'identifiant (survit-il au changement de
sous-etat = la fuite), `+0x34`/`+0x38`/`+0x3C` (l'ordre),
`+0x78`..`+0x84` (la couleur), `+0x28`/`+0x2C`/`+0x88` (debut, fin, image
courante), et les bits `8` et `0x100000` de `+0x30`.

> **CORRIGE AU SS 407.** Cette ligne disait `[DAT_1806AF3D0 + 0x68]` : le
> pointeur de **REVO** avec l'offset d'**APM3**, exactement l'erreur contre
> laquelle la section 2 met en garde. Dans REVO, a partir du pointeur
> `VF5FS+0x6AF3D0` : l'arbre est en **`+0x60`**, sa taille en **`+0x68`**, le
> compteur d'identifiants en **`+0x78`**. (APM3 : `+0x68` et `+0x88`.)
> C'est ce que la sonde du SS 403 a effectivement lu. Que de la memoire du
module : **aucune intermittence possible**, contrairement a tout critere qui
relit la memoire des sommets.

## 6. LE REPARTITEUR DE COUCHES -- ET LE GROUPE QUI N'EST JAMAIS VIDE

Lu au SS 405 par references croisees, **sans aucune course**. C'est la partie
que la section 4 laissait implicite : qui appelle le rendu de groupe, et quand.

### Il n'existe qu'un seul chemin

| fonction | appelants |
|---|---|
| `FUN_180198990` (rendre un groupe) | **UN** : `FUN_180195D80` |
| `FUN_180195D80` | **QUATRE**, tous dans `FUN_180111AA0` |
| `FUN_180199890` (mettre en file) | 4, dans le cluster `0x180195Exx`-`0x180195Fxx` |
| `FUN_180025E10` (creer un objet AET) | 40 sites |

Les quatre enveloppes de mise en file : `FUN_180195E40` (<- `FUN_18010D6A0`),
`FUN_180195E60` (<- `FUN_18010BFB0`) et `FUN_180195F80` (<- `FUN_1801A8780`)
n'ont **qu'un** appelant chacune ; seule **`FUN_180195F40`** est l'API
generique, avec 40+ sites. Le gros du 2D passe donc par une seule porte.

### La carte couche -> groupe, lue en IMMEDIATS

| couche | l'appel, dans `FUN_180111AA0` | groupe | resolution |
|---|---|---|---|
| **6** | `FUN_180195d80(1, 0x11)` | **1** | `0x11` -- toujours |
| **11** | `FUN_180195d80(0, uVar7)` | **0** | `0xd` ou `0x11` |
| **12** | `FUN_180195d80(3, uVar7)` | **3** | idem |
| **13** | `FUN_180195d80(2, uVar7)` | **2** | idem |

`uVar7` vaut `0xd` sauf si l'octet d'autorisation de la couche 10 est nul ou
si la couche courante est < 11 ; comme le mode 13 **est** 1280x720, c'est sans
effet.

### Deux mecanismes eteignent une couche

**Un octet par couche**, premiere ligne de `FUN_180111AA0` :

```c
if (*(char *)(DAT_180754be8 + couche) == '\0') { ... goto LAB_180111fbf; }
```

Les 16 octets d'autorisation sont en `DAT_180754BE8 + 0..15`. Le meme bloc
porte `+0x418` la couche courante, `+0x38 + c*8` et `+0xB8 + c*8` les chronos
par couche, `+0x400` une liste de rappels.

**Le repartiteur lui-meme**, `FUN_180111930` : `bVar2` est vrai pour les
couches **`{0,2,3,5,6,7,8,9}`**, et `default:` ne dessine que `if (!bVar2)`.
Donc ces huit couches sont **sautees**. `+0x676` est un garde de premiere
image, pose a la fin de la premiere passe quand
`(cVar3 != 0) || (sous-etat != 41 && !cVar4 && !cVar5)`.

### Consequence : le groupe 1 n'est jamais vide

Sous nos conditions mesurees, **la couche 6 est sautee dans les DEUX passes**
-- a la premiere parce qu'elle n'est pas dans `{0xb,0xc,0xd,0xe}` et tombe
dans `default`, aux suivantes parce que `default` saute `{0,2,3,5,6,7,8,9}`.

`FUN_180198990` est le **seul** endroit qui dessine, delie et libere les 32
paniers d'un groupe. La couche 6 est le **seul** appelant qui lui passe le
groupe 1. Donc **tout sprite mis en file dans le groupe 1 y reste pour
toujours** : jamais dessine, jamais delie, jamais libere.

Et le groupe 1 est **exactement** celui que `FUN_180198990` traite a part :
ni projection ortho ni rectangle de decoupe (section 4). Les deux faits se
tiennent -- un groupe hors de la geometrie normale, et un groupe que personne
ne rend.

Les couches 11, 12 et 13 (groupes 0, 3, 2) ne sont sautees qu'a la premiere
passe : leurs sprites de l'image 1 sont dessines a l'image 2. Un residu d'une
image, pas une fuite.

**Ce que ca n'explique PAS :** le rideau blanc. Le SS 385 a releve sa pile
d'appel -- `0x111DA2`, l'instruction qui suit `CALL 0x180195d80` avec
`ECX = 0`, c'est-a-dire **la couche 11, groupe 0**, rendu a chaque image. Le
rideau est donc un sprite legitimement dessine, et le probleme est son
**rang parmi les 32 paniers du groupe 0**.

### L'effacement de la couche 10 est NOIR dans les deux branches

`FUN_1801104B0` s'est revele etre **mot pour mot** le meme effacement que
l'autre branche : sauver l'etat `0xb7`, poser la couleur, `FUN_1802DC4E0`,
restaurer. La seule difference est l'**alpha** de la couleur d'effacement --
`1.0` a la premiere passe, `0` ensuite -- et **la couleur est NOIRE dans les
deux cas**.

Donc notre repartiteur (`bloc+0x1FF08` non nul) ne change pas la nature de
l'effacement, et **le blanc des trois ecrans fixes ne vient pas de
l'effacement** : il vient d'un quad dessine.

### Ou le code s'arrete

La couche, le groupe et la priorite d'une commande de sprite viennent des
**reglages de creation de l'animation**, donc de **donnees**. Aucune lecture
de fonction ne dira quelle priorite porte le rideau. Le numero de panier est
la **variable de boucle** de `FUN_180198990` : il n'apparait meme pas dans une
pile d'appel. Le seul substitut accessible est le **rang du tirage dans
l'image**, que l'hote numerote deja (`VF5_TRACE_TIRAGES`, complete au SS 407
pour dire aussi quelle texture est liee en t0).


## 7. LE COMPOSITEUR D'IMAGE -- 16 PASSES, 4 COUCHES (SS 415, 8 nov. 2026)

Lu fonction par fonction, 27 fonctions, toutes deja sur le disque. La carte
des fichiers est dans `VF5RE/a_vider.txt`, section
<< LA CHAINE DU RENDU 2D >>.

**CECI CORRIGE LA FIN DE LA SECTION 6.** J'y avais ecrit : << aucune lecture
de fonction ne dira quelle priorite porte le rideau >> et << le numero de
panier est la variable de boucle de `FUN_180198990` >>. C'est vrai du cote
EMISSION, et faux du cote INSERTION : le creneau est le champ **`req+0x1c`**
d'une requete, ecrit par l'appelant, et `FUN_180196a00` lui donne **7** par
defaut. Une sonde posee dans `FUN_180199890` le lit. Le mur a bouge.

### L'image est faite de SEIZE PASSES

`FUN_180111930` boucle `i = 0..15` et appelle `FUN_180111aa0(i)` **dans
l'ordre croissant**. `FUN_180111aa0` saute la passe d'entree de jeu si
`DAT_180754be8[i] == 0`.

**Le portillon est un octet de NOTRE bloc : `DAT_180c8df28 + 0x676`.** Nul a
la premiere image, le module l'ecrit a 1 a la fin de celle-ci. Des la
deuxieme, les passes `{0,2,3,5,6,7,8,9}` sont **toujours sautees** ; seules
`{1, 4, 10, 11, 12, 13, 14, 15}` tournent. Notre hote lit deja cet octet
(`vf5fs_host.cpp` ligne 10003).

| passe | quoi |
|---|---|
| 6 | `FUN_180195d80(1, 0x11)` = la couche 1, **la SEULE passe 2D plate -- et elle ne tourne JAMAIS** |
| 10 | le vidage. Deux branches selon `bloc+0x1FF08`, les deux en NOIR, seul l'alpha differe (255.0 si `bloc+0x676` est nul, 0 sinon). `FUN_1801104b0` n'est PAS une commande de l'hote : c'est la meme sequence en ligne |
| 11 / 12 / 13 | les couches **0**, puis **3**, puis **2** |

Les couches 0, 2 et 3 sont dessinees en **PERSPECTIVE** (`FUN_180198990` avec
`param_2 != 1`) : troncon `FUN_1802d3600` proche 0.2 / loin 1500.0, regard
`FUN_1802dfb40`, puis decoupage `FUN_1802d8010` depuis `[gest+0x810..0x81c]`.
Seule la couche 1 reste plate -- et elle ne tourne pas.

### La geometrie, par le CONSTRUCTEUR (donc mesuree)

`FUN_180196fb0` : `0x830` octets, `0x80` elements de `0x10` depuis `+8` =
**128 creneaux = 4 couches x 32**. Les << 32 paniers >> de la section 1 sont
donc les 32 creneaux d'UNE couche, et il y a quatre couches.

| champ | quoi |
|---|---|
| `+0x008 .. +0x807` | 128 creneaux de `0x10` : `{tete, queue}` d'une liste doublement chainee (noeud : precedent `+0xe8`, suivant `+0xf0`) |
| `+0x808` / `+0x80c` | pose par `FUN_180199510` depuis `FUN_180179e70` (la resolution) |
| `+0x810 .. +0x81c` | le rectangle du decoupage |
| `+0x820` | **la couche courante** (0 a l'init) |
| `+0x824` | `0x11`, le mode par defaut (celui que `FUN_180199890` teste) |
| `+0x828` | pose par `FUN_180198990` a chaque passe de couche |

### Ou va une requete

`FUN_180199890` : couche = `req+0x14`, ou `[gest+0x820]` si `-1`, plus
`req+0x18` ; **creneau = `req+0x1c`**. Dans une couche, `FUN_180198990`
parcourt les **32 creneaux en ordre croissant** et emet chaque liste
tete->suivant par `FUN_180197c30`, puis la libere. `FUN_18019a010`, lui, ne
fait que VIDER les 4x32 listes : c'est le nettoyage de tete de passe, **pas**
l'emetteur (`FUN_18019acd0` est un simple desenchainement).

**L'ordre complet d'un tirage est donc : (passe croissante ; couche dans
l'ordre 0, 3, 2 ; creneau croissant ; insertion).** Ne jamais raisonner sur le
rang brut d'un tirage sans dire de quelle couche il vient.

### LE BLANC EST LE DEFAUT, ET IL EST VOULU

`FUN_180196a00` ecrit `0xFFFFFFFF` sur les octets **`+0x04..+0x0b`** d'une
requete neuve -- un seul `mov` de 8 octets pour DEUX champs :

* **`+0x04`** = l'identifiant de sprite. `0xFFFFFFFF` = **aucun sprite**.
* **`+0x08..+0x0b`** = **la couleur RGBA**, lue par la premiere ligne utile de
  `FUN_180197c30` : `FUN_1802cf1e0(o[0xa], o[0x9], o[0x8], o[0xb])`.
  Quatre `0xFF` = **blanc opaque**.

Et `+0x04 == 0xFFFFFFFF` prend le **chemin A** de `FUN_180199890`, qui **ne
lie AUCUNE texture** : il n'ecrit jamais le `+0xa0` du noeud. Le quad herite
de la texture en place -- la 32x32 par defaut.

**Donc une primitive sans texture dont l'appelant ne pose pas sa couleur est
un quad BLANC OPAQUE.** C'est le `(1,1,1,1)` mesure au SS 365, et le << fond
blanc >> que la section 6 constate sur les trois ecrans fixes. Autres defauts
d'une requete : couche `-1`, creneau **7**, mode 9.

Les primitives qui prennent ce chemin : `FUN_180195e60` (type 2) et
`FUN_180195f80` (type 3), toutes deux avec une couleur explicite en `+0x08`.
`FUN_180197c30` rend sans rien faire si `*req == 1`.

### Un identifiant de sprite se decode

`(h >> 0x10) & 0xfff` = le jeu (`FUN_180198810`) ; `h & 0xffff` = l'index.

* **quartet de tete `0x1`** = << toute la texture >> : `[jeu+0x18][index]`,
  dimensions par les `short` a `+0xc`/`+0xe` de l'objet texture, mode force
  a 9 ;
* sinon un rectangle dans la table a `[jeu+0x10]+0x10`, pas `0x28` : index de
  texture a `+0`, UV a `+0x18`/`+0x1c`, taille a `+0x20`/`+0x24` ; mode pris
  dans une seconde table a `[jeu+0x10]+0x1c`, pas 8, `+4`.

Si le jeu est absent ou `[jeu+0xb8] == 0`, **le tirage est ABANDONNE**
(`uVar12 = 0`) : un jeu manquant ne donne pas un quad blanc, il ne donne
rien.

### La chaine des textures, de bout en bout

`FUN_18019bab0` diffuse les textures une par une et **se rechaine lui-meme**
(`FUN_180279360`) : `+0xD0` = leurs identifiants, `+0xE0` = l'index
d'avancement, `+0x18` = le tableau resultat. Il appelle :

* **`FUN_1801a2ac0`** -- lit un bloc **`"TXP\x05"`** : `[1]` = nombre de
  sous-images, `[3]...` = leurs decalages, format a `+0xc` (-> 0x1bb, 0x1cf,
  0x1d6, 0x1ce, 0x1d5, 0x1d4, 0x7ea..0x7ed), largeur/hauteur a `+4`/`+8`.
  `[1] == 0` rend 0. Pour un identifiant dans `[0x1762, 0x17E0]` il ne pose
  **qu'un seul niveau** ;
* **`FUN_1801a15c0`** -- la creation a la GL : prendre une unite
  (`FUN_1802df650` / `FUN_1802df420`), poser enroulement/filtre/niveaux
  (`FUN_1802dfb00`), televerser chaque niveau (`FUN_1801a1f10`). Si un
  televersement rend `< 0`, l'objet est detruit et la fonction rend 0.

L'objet texture : `+0x0c` largeur, `+0x0e` hauteur, `[4]` unite, `[5]` cible,
`[6]` format, `[7]` niveaux, `[8]` octets. **Cible `0x11e` = 2D, `0x246` =
cube (6 faces, `[1]/6`), `0x39a` = RECTANGLE, et rectangle veut dire
coordonnees NON normalisees** (`FUN_180199890` ligne 159 : les deux facteurs
`1/largeur` et `1/hauteur` deviennent 1.0).

### Ce qui reste

Une seule question : quel `(couche, creneau)` portent les tirages du titre, et
lequel portent les deux quads blancs. Les trois champs sont `req+0x14`,
`req+0x18`, `req+0x1c`, consommes **a l'insertion** par `FUN_180199890` --
donc une sonde doit les lire la, pas a l'emission.


---

## 8. QUI POSE LE CRENEAU (SS 416, 8 nov. 2026)

Lu sur l'instance `:8192` (`vf5fs_revo`). **Tout ce qui suit est du
DESASSEMBLAGE**, pas de la decompilation : la decompilation s'est trompee deux
fois dans cette seance, et les deux fois le code machine l'a corrigee.

### 8.1 CECI REFUTE UNE PHRASE DE LA SECTION 7 -- degre CONFIRME

La section 7 dit : << le chemin A de `FUN_180199890` **ne lie AUCUNE texture**
: il n'ecrit jamais le `+0xa0` du noeud >>. **C'est FAUX.**

* `FUN_180199690` a **DEUX** parametres (`RCX` = &liste, `RDX` = la requete).
  Ghidra n'en montre qu'un et perd le second -- d'ou ma lecture fautive.
  Preuve : `180199690 MOV RDI,RCX` / `1801996a2 MOV RSI,RDX`.
* Elle alloue `0xF8` (`MOV ECX,0xf8` / `CALL 0x180279bd0`) puis
  `1801996bc MOV RDX,RSI` / `MOV RCX,RAX` / `CALL 0x180196850` : un
  **CONSTRUCTEUR DE COPIE**.
* `FUN_180196850` recopie champ par champ de `+0x00` a `+0xe7`, **`+0xa0`
  comprise** (`180196966 MOV RAX,[RDX+0xa0]` / `MOV [RCX+0xa0],RAX`), puis
  rend `RCX`.
* `0xF8` = `0xe8` de charge utile -- exactement l'etendue que `FUN_180196a00`
  initialise -- plus `prev +0xe8` et `suivant +0xf0`.

**Le noeud EST la requete, recopiee telle quelle.** Trois consequences :

1. une sonde lit `+0x14`/`+0x18`/`+0x1c` indifferemment sur la requete ou sur
   le noeud : ce sont les memes octets ;
2. le chemin A porte une texture quand la requete en porte une en `+0xa0`.
   Ce n'est pas << aucune texture >>, c'est **une texture par pointeur
   DIRECT, sans passer par le jeu de sprites** ;
3. **un quad blanc demande DEUX conditions**, pas une :
   `req+0x04 == 0xFFFFFFFF` **ET** `req+0xa0 == 0`.

Et l'insertion se fait **en QUEUE** (`[RDI+8]`) : dans un creneau, l'ordre de
tirage est l'ordre d'emission.

### 8.2 Les quatre enfileurs, et lequel ne pose rien

| enfileur | ce qu'il pose | creneau ? | couleur ? |
|---|---|---|---|
| `FUN_180195e40` | `[RCX] = 5`, puis saut. **4 instructions** | non | non |
| `FUN_180195f40` | resout `+0x04` si `[RCX] == 0` | non | non |
| `FUN_180195e60` | type 2, geometrie | **`+0x1c` <- argument** | **`+0x08` <- argument** |
| `FUN_180195f80` | type 3 | oui | oui |

`FUN_180195e60` ecrit `+0x1c` depuis `[RSP+0x188]` et `+0x08` depuis
`[RSP+0x190]` : **le creneau et la couleur sont des ARGUMENTS**. Elle laisse
`+0x14` au defaut `-1` (la couche courante).

**`FUN_180195e40` n'a qu'UN SEUL appelant dans tout le module :
`FUN_18010d6a0`** (`18010daaa`), qui appelle aussi `FUN_180195f40` douze
octets plus loin (`18010dab6`) -- les deux branches d'un meme `if`.

### 8.3 Le creneau n'est pas une constante : c'est un champ d'un BLOC D'ETAT

**`ETAT2D = *(void**)0x180754ab8`** -- c'est un POINTEUR qu'on dereference
(`18010d725 MOV RBX, qword ptr [0x180754ab8]`), pas un tableau. Ghidra l'a
type `float*`, ce qui lui fait rendre des copies d'ENTIERS comme des
flottants : c'est la deuxieme erreur de decompilation de la seance.

`0x180754ab8` a **38 references : 37 en LECTURE, UNE SEULE en ECRITURE**
(`FUN_18010cc70` a `18010cec9`). Toute la famille `0x18010c***`-`0x18010e***`
partage donc ce bloc.

| champ | quoi | preuve |
|---|---|---|
| `+0x30` / `+0x34` | une paire lue ensemble | `FUN_18010d3b0` |
| `+0x38` | **la couleur RGBA empaquetee** | `FUN_18010dbe0` |
| `+0x3b` | l'octet d'alpha, en 0..255 | `18010d740 MOVZX EAX,byte ptr [RBX+0x3b]` |
| `+0x50` | **LE CRENEAU, stocke en FLOTTANT** | `FUN_18010dc00` / `FUN_18010d3e0` |
| `+0x54` | `req+0x18`, un **ENTIER** | `18010da7d MOV EAX,dword ptr [RBX+0x54]` |
| `+0x58` | le mode : `61` ou autre | `18010da84 CMP dword ptr [RBX+0x58],0x3d` |

Les accesseurs, lus au desassemblage :

| fonction | role |
|---|---|
| **`FUN_18010dc00(int)`** | **pose le creneau** : `VCVTSI2SS` puis `VMOVSS [+0x50]` |
| **`FUN_18010d3e0() -> int`** | **lit le creneau** : `VCVTTSS2SI EAX,[+0x50]` |
| `FUN_18010dbf0(int)` | pose `+0x54` (donc `req+0x18`) |
| `FUN_18010dbe0(uint)` | pose la couleur `+0x38` **et rend l'ancienne** |
| `FUN_18010dc20(float)` | recalcule le seul octet d'alpha de `+0x38` |

### 8.4 `FUN_18010d6a0` -- l'emetteur, et ce qu'il ne pose PAS

Requete a `RSP+0x30`, construite par `FUN_180196a00` (`18010d79a`) et enfilee
depuis la meme adresse (`18010daa5`) -- les deux bouts concordent.

```
18010da62  VCVTTSS2SI RAX, dword ptr [RBX + 0x50]
18010da79  MOV  dword ptr [RSP + 0x4c], EAX     ; requete +0x1c  LE CRENEAU
18010da7d  MOV  EAX, dword ptr [RBX + 0x54]     ; un MOV ENTIER
18010da80  MOV  dword ptr [RSP + 0x48], EAX     ; requete +0x18
18010da84  CMP  dword ptr [RBX + 0x58], 0x3d    ; mode == 61 ?
18010daa5  LEA  RCX, [RSP + 0x30]
18010daaa  CALL 0x180195e40                     ; sinon FUN_180195f40
```

* `req+0x08` (la couleur) <- `ETAT2D+0x38` ;
* `req+0x1c` (le creneau) <- `(int)(float)ETAT2D+0x50` ;
* `req+0x18` <- `ETAT2D+0x54` ;
* **`req+0x14` (LA COUCHE) n'est JAMAIS ecrit** : il y a un trou a `RSP+0x44`
  entre `+0x10` et `+0x18`. Il reste donc au defaut `-1` du constructeur,
  c'est-a-dire **la couche courante `[gest+0x820]`**.

### 8.5 LE BLANC EST UN ETAT REMIS A BLANC, PAS SEULEMENT UN DEFAUT

A `1800da0ce`, juste APRES la sequence de dessin :

```
1800da0ce  MOV  ECX, 0xffffffff
1800da0d3  CALL 0x18010dbe0        ; la couleur de ETAT2D <- blanc opaque
```

Le meme `MOV ECX,0xffffffff` / `CALL FUN_18010dbe0` suit le poseur de creneau
a `1800d1658`. **La couleur est une variable GLOBALE COLLANTE qu'on remet a
blanc opaque apres usage.** Donc tout dessin de cette famille qui ne pose pas
sa couleur herite de `0xFFFFFFFF` -- et `FUN_18010d6a0` la recopie dans
`req+0x08`. C'est un mecanisme plus fort que le defaut du constructeur de la
section 7 : le blanc est **entretenu**.

### 8.6 Le releve des creneaux reellement poses -- degre CONFIRME

`FUN_18010dc00` a 13 appelants. Les constantes lues :

| site | valeur de `ECX` | creneau |
|---|---|---|
| `1800852a3` | `0x19` | **25** |
| `1800d9feb`, `1800da031`, `1800da074`, `1800da0ae` (`FUN_1800d9ed0`) | `0x19` | **25** |
| `1800d98da` (`FUN_1800d96e0`) | `0x19` | **25** |
| `1801a3ab3` (`FUN_1801a3a70`) | `0x16` | **22** |
| `1800d1651` (`FUN_1800d14d0`) | `ESI` | **variable (argument)** |

**Personne ne pose 7.** Le `7` du constructeur est donc la marque d'une
requete dont l'emetteur n'a JAMAIS appele `FUN_18010dc00`.

### 8.7 Ce qui reste -- degre SPECULATIF, a mesurer

L'ordre de tirage est (passe croissante ; couche **0, puis 3, puis 2** ;
creneau croissant ; emission). La mesure de l'image 400 donne : rangs 1-37 de
vrais atlas, rangs 38-39 les deux quads blancs, rangs 40-55 un seul atlas.

Si les deux quads blancs portent le creneau **7** par defaut, ils ne peuvent
pas etre entre deux groupes de la MEME couche, puisque 7 est inferieur a 22 et
a 25. L'hypothese qui colle au releve est donc :

* rangs 1-37 = **couche 0** ;
* rangs 38-39 = **couche 3, creneau 7** (le defaut, personne ne l'a pose) ;
* rangs 40-55 = **couche 2**.

Elle est falsifiable et elle se mesure en UN point : lire `req+0x14`,
`req+0x18`, `req+0x1c` a l'entree de `FUN_180199890`. Ne rien affirmer avant.


---

## 9. LA COUCHE, ET LA SEULE PRIMITIVE SANS TEXTURE (SS 416, suite)

### 9.1 La couche courante : un poseur, un liseur, et l'idiome sauver/restaurer

`grep -a 0x820` sur les 3311 fichiers de `code_decompile` rend 9 fichiers, 4
utiles : `FUN_180199440(gest)` **lit**, `FUN_18019b970(gest, couche)`
**pose**, `FUN_180199510` initialise a **0**. (`FUN_18010b840` est sans
rapport : une autre structure.)

Chacun n'a **qu'un seul appelant** -- les enveloppes publiques :
`FUN_180195e10()` lit la couche courante, **`FUN_180196120(couche)`** la pose.

`FUN_180196120` a **plus de 100 appelants, PAR PAIRES**. Mesure sur
`FUN_1800d9ed0` :

```
1800d9f2c  CALL 0x180195e10    ; lire la couche courante
1800d9f31  MOV  ECX, 0x3       ; COUCHE 3
1800d9f36  MOV  EBP, EAX       ; sauver l'ancienne
1800d9f38  CALL 0x180196120    ; poser
   ...                         ; FUN_18010dc00(0x19) = creneau 25, les dessins
1800da0ce  MOV  ECX, 0xffffffff
1800da0d3  CALL 0x18010dbe0    ; couleur <- blanc
1800da0da  CALL 0x180196120    ; restaurer (ECX = EBP)
```

**Consequence, degre CONFIRME : la couche d'un tirage est une propriete de la
ROUTINE APPELANTE, pas du systeme 2D.** Il y a une cinquantaine de telles
routines.

`FUN_1800dffd0` (la passe 2D de l'image) lit la couche et **la REPOSE
INCHANGEE** avant `FUN_180111930` : aucun changement de valeur. Mon ancienne
note << lit et repose la couche courante >> etait exacte et sans effet.

`FUN_1800d9ed0` dessine du TEXTE : `0x1803c78c0` porte `"FREE PLAY"`, et ses
voisines `"%s%s"` et `"%s\n"`.

### 9.2 `FUN_180195e60` est la SEULE primitive de quad sans texture -- CONFIRME

`FUN_180196a00` met `param_1 + 0x28` a 0, c'est-a-dire **`+0xa0 = 0`**, et
`FUN_180195e60` n'ecrit **jamais** `+0x04`. Elle prend donc toujours le
chemin A avec `+0xa0` nul : un quad **sans texture** dont la couleur est son
argument. (La section 7 l'ecartait au motif qu'elle << pose une couleur
explicite >> -- mauvais raisonnement : une couleur explicite peut etre
blanche.)

**Elle n'a qu'UN site d'appel : `FUN_18010bfb0`** (`18010c0b9`), plus une
reference DATA (`18125cd48`, une table de pointeurs).

Ses parametres, lus a l'ABI x64 (5e argument a `[RSP+0x20]` chez l'appelant,
`[RSP+0x180]` chez l'appelee apres son `SUB RSP, 0x158`) :

| ecrit par l'appelant | recu par l'appelee | champ | valeur |
|---|---|---|---|
| `[RSP+0x20] = 0x11` | `[RSP+0x180]` | `+0x20` / `+0x24` | **17** |
| `[RSP+0x28] = 0x1d` | `[RSP+0x188]` | **`+0x1c` LE CRENEAU** | **29** |
| `[RSP+0x30] = EBX` | `[RSP+0x190]` | `+0x08` la couleur | **variable** |
| `[RSP+0x38] = 0` | `[RSP+0x198]` | `+0x18` | **0** |

Et `+0x14` n'est jamais ecrit : **la couche courante**.

### 9.3 UNE ERREUR DE MA PART, CORRIGEE DANS LA MEME SEANCE

J'avais lu `0x18063e1d8` = `00 00 80 3f` quatre fois = `(1.0,1.0,1.0,1.0)` et
annonce << la couleur du quad est une constante litterale blanche dans
`.rdata` >>. **C'EST FAUX.**

```
18010c199  VMOVUPS XMM0, xmmword ptr [RAX]
18010c19d  VMOVUPS xmmword ptr [0x18063e1d8], XMM0
18010c1a5  CALL    0x18010bfb0
```

`0x18063e1d8` est un **GLOBAL MUTABLE de 16 octets** que `FUN_18010c0f0`
**ECRASE** juste avant l'appel, depuis le `[RAX]` rendu par `FUN_18000ba30`.
Le `(1,1,1,1)` lu n'est que sa **valeur initiale dans l'image statique**.
**Lire une valeur ne dit pas qu'elle est constante : il faut chercher les
ECRITURES.**

Ce qui reste vrai : `FUN_18000baa0(float *rgba)` est bien un empaqueteur
float4 -> RGBA8 (multiplication par `255.0` de `+0x0`, `+0x4`, `+0x8`,
`+0xc`, `VCVTTSS2SI`, octet bas, decalages et `OR`). Avec `(1,1,1,1)` il
rendrait `0xFFFFFFFF`.

### 9.4 Et ce chemin n'est PROBABLEMENT PAS le fond blanc -- la piste tombe

`FUN_18010c0f0` pose d'abord trois couleurs dans un tableau local :

```
18010c10c  MOV dword ptr [RAX + -0x38], 0xffff0000   ; bleu
18010c117  MOV dword ptr [RAX + -0x34], 0xff00ff00   ; vert
18010c13f  MOV dword ptr [RAX + -0x30], 0xff0000ff   ; rouge
18010c150  MOV ESI, 0x3                              ; trois iterations
```

Trois couleurs d'axes, et une boucle de trois. Et `FUN_18010bfb0` prend
**deux float3** (`[RCX+0,4,8]` et `[RDX+0,4,8]`), les projette deux fois par
`FUN_180066920`, puis remplit le rectangle obtenu : **une boite 3D projetee a
l'ecran**.

Au-dessus, `FUN_180026420` parcourt jusqu'a `0x60 = 96` poignees -- objets de
`0x230` octets a `G+0x218`, avec `G = *(void**)0x1806af3e0` et un controle de
generation `[slot+0x22c] == poignee` -- et appelle `FUN_180036060` sur
chacune ; `FUN_180035900` **s'appelle elle-meme** (parcours d'arbre).

**Degre ETAYE : ce chemin est un dessineur de reperes de DEBOGAGE (boite
englobante + axes rouge/vert/bleu), pas un fond blanc.** Les trois couleurs
d'axes argumentent contre. Donc la seule primitive de quad **sans texture** du
module n'explique probablement pas les deux quads blancs plein ecran, et il
faut les chercher parmi les quads **TEXTURES** -- ce que la section 8.1 rend
possible, puisque le chemin A porte une texture quand `+0xa0` est non nul.

### 9.5 Ou en est la question

**Acquis, degre CONFIRME** : les trois champs et leurs defauts ; qui les pose
(`FUN_18010dc00` pour le creneau, `FUN_180196120` pour la couche) ; le releve
des creneaux (**7 jamais pose**, 22, 25, 29, variable) ; et que la couche est
une propriete de la routine appelante.

**Non acquis** : quelle couche et quel creneau portent les 37 atlas du titre
et les deux quads. La lecture a atteint sa limite utile -- une cinquantaine de
routines posent la couche, et le module emet 2 quads par image parmi des
milliers de tirages. **Une sonde a l'entree de `FUN_180199890`, lisant
`req+0x14` / `req+0x18` / `req+0x1c`, repond en UNE course.** C'est une
mesure : elle ne change rien a l'ecran et revient au defaut.


---

## 10. LES TYPES DE PRIMITIVES, ET POURQUOI LE QUAD BLANC EST UN SPRITE

### 10.1 Le dispatch de `FUN_180197c30` -- degre CONFIRME

La QUEUE de `FUN_180197c30` (apres la ligne 336) soumet la geometrie selon
`*req` :

| type | soumission | sommets | qui l'emet |
|---|---|---|---|
| **1** | retour immediat (ligne 67) | -- | -- |
| **2** | `FUN_1802cf450(3, 0, 2)` | **2 : une LIGNE** | `FUN_180195e60` |
| **3** | `FUN_1802cf800(...)` + `FUN_1802cf450(9, 0, 4)` | **4 : un quad** | `FUN_180195f80` |
| **4** | idem + `FUN_1802cf450(4, 0, 4)` | **4** | via `FUN_180195f40` |
| **6** | boucle sur `req+0x2e`, 2 sommets par tour | polyligne | via `FUN_180195f40` |
| **0 / 5** | RIEN dans la queue | -- | le CORPS |

Et le CORPS (lignes 236-318) soumet `FUN_1802cf450(9, 0, 4)` -- **quatre
sommets, mode 9, le meme que le type 3** -- plus une variante a compte
variable (`FUN_1802cf450(9, 0, req[0x2e])`). **Le chemin SPRITE est donc le
chemin du quad.**

**Correction de la section 9.2 :** j'y ai appele `FUN_180195e60` << la seule
primitive de quad sans texture >>. Elle emet le type 2, donc **DEUX sommets :
une LIGNE**, pas un quad. Ca confirme la lecture du repere de debogage de 9.4.

### 10.2 `FUN_180195f80` : le seul rectangle PLEIN sans texture -- CONFIRME

`FUN_180195f80(const float rect[4], int mode, int creneau, const u8 col[4], int)` :

```
180195fa5  VMOVSS XMM7, dword ptr [RCX]        ; x
180195fa9  VADDSS XMM6, XMM7, [RCX + 0x8]      ; x + largeur
180195fbe  VMOVSS XMM9, dword ptr [RCX + 0x4]  ; y
180195fc3  VADDSS XMM8, XMM9, [RCX + 0xc]      ; y + hauteur
180195fb8  MOVZX  EAX, byte ptr [R9]           ; la couleur, 4 OCTETS repaquetes
18019601f  MOV    dword ptr [RSP+0x20], 0x3    ; type 3
180196033  MOV    dword ptr [RSP+0x3c], ESI    ; +0x1c  LE CRENEAU
180196037  MOV    dword ptr [RSP+0x28], EBX    ; +0x08  LA COULEUR
```

Elle n'ecrit **ni `+0x04` ni `+0xa0`** : chemin A, `+0xa0 == 0`, donc **aucune
texture liee -- elle herite de la 32x32 par defaut**. C'est exactement la
forme d'un quad blanc plein ecran.

**Mais elle n'a qu'UN site d'appel, et la chaine est fermee :**

`FUN_180195f80` <- `FUN_1801a8780(obj, rect, mode)` (creneau = `obj+0x24`,
couleur = 4 octets a `obj+0x0c`, `+0x18` = 0) <- `FUN_1801c58a0`, **qui n'a
AUCUN site d'appel** : elle n'est atteinte que par pointeur, depuis la vtable
`0x18043a890`, au **cran 4**.

### 10.3 Le nom de la classe, par le RTTI -- degre CONFIRME

`0x18043a888` porte `0x1805ea868`, un pointeur de DONNEES au milieu de
pointeurs de code : c'est le Complete Object Locator, donc la vtable commence
a `0x18043a890`.

```
+0x00 signature      = 1          (x64)
+0x04 offset         = 0x500      (base secondaire a +0x500 de l'objet)
+0x08 cdOffset       = 0
+0x0c TypeDescriptor = 0x6a6408
+0x14 pSelf          = 0x5ea868   -- egale sa propre adresse : structure VALIDE
```

`0x1806a6418` = **`.?AVTaskSession@@`** -> la classe est **`TaskSession`**.
(Sa voisine dans `.data` est `.?AVNPMatching2Session@@`.) Et
`FUN_1801c58a0` encadre tout son dessin par :

```
1801c5926  CALL 0x180195e10   ; lire la couche courante
1801c592e  MOV  ECX, 0x2      ; COUCHE 2
1801c5933  CALL 0x180196120   ; poser
1801c5943  CMP  qword ptr [RBX + 0x1dc8], RSI   ; iterer une liste
1801c5b6c  CALL 0x1801a8780   ; le rectangle plein
1801c5bae  LEA  RDX, [0x1803758c0]   ; "%s" : du texte
1801c5bc5  CALL 0x180196120   ; restaurer
```

**Degre ETAYE : c'est l'affichage de DEBOGAGE d'une session** (une liste
d'elements, chacun un rectangle plein et une etiquette), en couche 2.

ATTENTION : les references << DATA >> en `0x1812xxxxx` que `xrefs_list` rend
pour presque toute fonction sont la **table d'exceptions** (`.pdata`), pas des
vtables. Ne pas les lire comme des tables de pointeurs -- je l'ai fait une
fois dans cette seance. La vraie vtable etait celle en `0x18043a8b0`.

### 10.4 CE QUE CA TRANCHE

Les primitives **sans texture** sont maintenant toutes elucidees, et **aucune
n'est le quad blanc plein ecran** :

* type 2 = une LIGNE, pour le repere de debogage (boite englobante + axes RVB) ;
* type 3 = un rectangle plein, pour le seul affichage de debogage de
  `TaskSession`, en couche 2 ;
* types 4 et 6 = d'autres formes, par les 60 appelants de `FUN_180195f40`.

**Donc les deux quads blancs sont des SPRITES** (type 0 ou 5, dessines dans le
corps de `FUN_180197c30` a 4 sommets mode 9), dont la texture resout vers la
32x32 par defaut. Ca concorde avec les deux mesures deja au journal : la 32x32
est la texture par defaut, liee en onze creneaux, et les deux quads sont a
2,00 par image dans TOUS les sous-etats.

Leur emetteur est `FUN_18010d6a0` (ou un des 60 appelants de
`FUN_180195f40`), et **chacun de leurs parametres vient de l'ETAT au moment du
tirage** : la couleur de `ETAT2D+0x38` (remise a blanc apres chaque dessin,
section 8.5), le creneau de `ETAT2D+0x50`, le decalage de `ETAT2D+0x54`, la
couche de `[gest+0x820]` pose par l'une des ~50 routines.

**C'est pour cela que la lecture statique ne peut pas fermer la question, et
qu'une sonde la ferme en une course.** Les trois champs se lisent a l'entree
de `FUN_180199890` ; c'est une mesure, elle ne change rien a l'ecran.


---

## 11. SS 418 -- LE TITRE A DEUX CHEMINS, ET CELUI QU'ON EMPRUNTE EST MORT

### 11.1 Ce qui est lu, et ou

Rien ici n'est mesure sur le banc : tout est lu, dans le module
(`code_decompile/FUN_1800e5ed0.c`, CS_TITLE phase 0) et dans `VFREVO.exe`
(`code_decompile_vfrevo/`, deja sur le disque, 366 fichiers). Degre :
**ETAYE** par le code des deux cotes, concordant.

### 11.2 CS_TITLE phase 0 etape 2 : un `if` qui decide de tout

`FUN_1800E5ED0`, etape `mo+0x34 == 2` :

```c
if (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0) {   // NOTRE repartiteur
    if (!FUN_1800F07C0(DAT_1807514B8)) return 0;      // attendre
    FUN_1800F0960(DAT_1807514B8);
    local_res8[0] = 1;
    repartiteur(ctx, 0x10, local_res8);               // commande 16
    repartiteur(ctx, 0x12, 0);                        // commande 18
    FUN_1801946B0("vfes_se_title");
    *(int *)(lVar4 + 0x34) = 3;
    return 0;                                         // RIEN n'est charge
}
if (FUN_180196130(0x15f)) return 0;                   // attendre le SPR
if (FUN_1800262E0(0x12e)) return 0;                   // attendre l'AET
FUN_1801CF1F0(1);
*(int *)(lVar4 + 0x34) = 3;
```

Et a l'etape 3, meme forme : `+0x1FF08 == 0` batit `logo_vf5` /
`logo_vf5_short`, `loop_start`, `loop_end` ; sinon le module demande
`rom/movie/vf5title_bg.sfd` et ne batit RIEN.

**Il y a donc DEUX ecrans-titre, exclusifs :**

* **(A) celui du MODULE** -- ses propres ressources `0x15F` (SPR) et `0x12E`
  (AET), bati et joue par lui, **a la seule condition que `+0x1FF08` soit
  NUL** ;
* **(B) celui de l'HOTE** -- delegue par les commandes 16 et 18.

### 11.3 Ce que l'hote de SEGA fait du chemin (B)

Lu dans `VFREVO.exe`. La commande **14** (`FUN_1415ECC00`) alloue 0x58 et
ecrit une table de 18 identifiants, puis resout l'archive `0x1D` :

```
+0x00 = 0x1D  (l'archive, resolue par FUN_1411EB500 -> conteneur en +0x48)
+0x04 = 0x1801   +0x08 = 0x1802   +0x0C = 0x30FB   +0x10 = 0x30FC
+0x14 = 0x3662   +0x18 = 0x30FD   +0x1C = 0x3100   +0x20 = 0x36BD
+0x24 = 0x1803   +0x28 = 0x1A39   +0x2C = 0x3C6E   +0x30 = 0x3C6F
+0x34 = 0x3CB0   +0x38 = 0x25A6   +0x3C = 0x3D41   +0x40 = 0x3D42
+0x44 = 0x26C8   +0x50 = temoin « pret »
```

Les primitives de l'hote de SEGA, sur ce conteneur :

| fonction | role |
|---|---|
| `FUN_1411EB500(out, archive, 0)` | monter l'archive AET |
| `FUN_141065810(cont, out, id, -1)` | resoudre un identifiant en objet |
| `FUN_141060CE0(cont, id)` | **JOUER** |
| `FUN_141067150(obj, 3)` | **RELACHER** (raison 3) |
| `FUN_1402C51E0(obj, &txt)` | poser un texte |

D'ou : **cmd 16** = joue `0x1801` (+0x04) et `0x26C8` (+0x44), puis, si
`args[0] != 0`, joue `0x1A39` (+0x28) et ecrit `"Ver.%d.%02d"` dans `0x36BD`
(+0x20) ; **cmd 18** = joue `0x1802` (+0x08) ; **cmd 17** = relache cinq
couches ; **cmd 19** = arrete `0x1802`.

**Correction d'une fiche fausse.** J'avais note « couche AET 0x1802 par la
commande 18 ». `0x1802` n'est pas un numero de couche : c'est un
**identifiant de ressource dans l'archive 0x1D de `VFREVO.exe`**, et la
commande 18 le JOUE. La nuance porte toute la suite : l'image du chemin (B)
n'appartient pas au module, elle appartient a l'archive de l'hote.

### 11.4 La consequence, et elle est nette

Le chemin (B) demande a notre hote un lecteur AET **et** l'archive `0x1D`.
Nous n'avons ni l'un ni l'autre : `vf5fs_host.cpp` case 14 le dit depuis le
SS 414, mot pour mot -- « AUCUN lecteur AET dans l'hote, rien n'est charge ni
dessine ». Nos cases 14 a 23 comptent donc des `joue` / `relache` sur des
couches **vides**, ce qui est honnete et ne dessine rien.

Or notre repartiteur est non nul par defaut. **Le module emprunte donc
toujours (B), le chemin mort, et jamais (A), qu'il sait parcourir seul.**
C'est coherent avec la course du SS 417 : 1000 tirages sur 390 images de
CS_TITLE, soit 2,56 par image, quand les deux quads de fond font a eux seuls
2,00 par image ([[les-deux-quads-sont-le-fond-pas-un-rideau]]).

### 11.5 La cause, nommee -- et pourquoi ce n'est pas un interrupteur

> **Cause.** `bloc+0x1FF08` est non nul aux etapes 2 et 3 de CS_TITLE phase
> 0, donc le module delegue son ecran-titre a un hote qui n'a pas de lecteur
> AET, au lieu de le batir avec ses propres `0x15F` / `0x12E`.

La reparation est de rendre le repartiteur invisible au module **a ces deux
etapes precises**, pas d'omettre des tirages ni de forcer une texture. Le
mecanisme existe deja (SS 342, `VF5_SANS_RAPPEL`) et le SS 412 lui a fait le
seul reproche juste : il portait sur **tout** le sous-etat, donc aussi sur des
phases ou le module doit deleguer. L'etape est en `mo+0x34`, et l'hote la lit
deja -- `EtapeTitre()`. Borner le retrait a `sous-etat == 5 && (etape == 2 ||
etape == 3)` repond exactement a l'objection du 412, en se reglant sur le
`if` que le module porte en dur.

### 11.6 Ce que cette seance dit de la methode

Le resultat du 11.3 etait **deja transcrit dans `vf5fs_host.cpp`**, cases 14
a 20, avec les adresses SEGA en commentaire et la phrase sur le lecteur AET
manquant. Je l'ai re-derive dans Ghidra. C'est le piege que mes propres
fiches nomment deja -- [[agir-sur-mes-propres-notes]],
[[lire-la-sortie-des-sondes-posees]] -- et la lecon n'est pas « lire plus »
mais **lire son propre hote avant d'ouvrir un desassembleur**.

Ce qui est neuf, en revanche, et ne figurait nulle part : **le chemin (A)
existe et se passe entierement de l'hote.** Le lecteur AET manquant n'est
donc pas sur le chemin critique de l'ecran-titre ; il est contournable.

### 11.7 Premiere course du chemin (A) : le module FAUTE dans son propre free

**MESURE** (course du 8 nov 2026, 10:06). `VF5_TITRE_AET=1` par defaut,
l'hote rebati. Le jeu s'arrete sur `0xC0000005`.

Source : journal d'evenements Windows, `Application Error` 1000 --
**pas une supposition de ma part** :

```
Module defaillant : vf5fs-pxd-w64-d3d12_SteamRetail.dll
Exception code    : 0xc0000005
Fault offset      : 0x00000000002f7aee      -> Ghidra 0x1802F7AEE
```

La faute est **dans le module**, pas dans l'hote. Et c'est la premiere
instruction de `FUN_1802F7AD0` qui touche la memoire :

```
1802f7aee  F7413800000040  TEST dword ptr [RCX + 0x38], 0x40000000
```

Donc le `this` (`RCX`) est invalide a l'entree. L'unique appelant,
`FUN_1802F76A0`, est **le `free()` du module** :

```
1802f76a0  TEST RCX, RCX          ; p == 0 ? -> ne rien faire
1802f76a5  LEA  RDX, [RCX - 0x10] ; le BLOC = p - 0x10 (en-tete de 0x10)
1802f76a9  MOV  RCX, [RCX - 0x10] ; le premier qword de l'en-tete
1802f76ad  SAR  RCX, 0x10         ; >> 16 arithmetique ==> L'ALLOCATEUR
1802f76b1  JMP  FUN_1802F7AD0
```

**L'allocateur est range dans l'en-tete du bloc, decale de 16 bits**, et le
free le recupere par `SAR RCX, 0x10`. Si `[p-0x10]` vaut 0, `RCX` devient 0
et le `TEST [RCX+0x38]` faute a l'adresse `0x38` -- exactement l'image d'un
free sur un bloc **sans en-tete d'allocateur valide**.

Que `FUN_1802F7AD0` soit bien un free se lit sur place : il decremente le
compteur `[RDI+0x28]`, retranche de `[RDI+0x3C]`, et estampille le bloc avec
`R13W = 0x5246` = **`"FR"`**.

**Ce que ca ne dit PAS encore.** Quel bloc, et a quelle etape. Degre :
**ETAYE** pour « le module libere un bloc dont l'en-tete ne porte pas
d'allocateur valide » ; **INCONNU** pour la cause de cet en-tete invalide.
Deux pistes a mesurer, pas a trancher ici :

1. l'hote **substitue** l'allocateur du module (cran `0x168`, SS 101) et rend
   des blocs **sans** l'en-tete de 0x10 octets ; sur (B) ces blocs n'etaient
   jamais liberes par le free INTERNE, sur (A) ils le sont ;
2. l'hote possede deja un detecteur -- « **LIBERATION ETRANGERE** : %p ne
   vient pas de nos allocateurs » -- et il faut savoir s'il crie.

**Et la course n'a produit AUCUN journal** : le lanceur ne pose jamais
`VF5_JOURNAL`, et l'hote est muet par defaut (ligne 158 du lanceur, SS 305.9).
Omission de ma part, sans rapport avec la faute. La prochaine course doit
porter `VF5_JOURNAL=1` **et** `VF5_JOURNAL_SYNC=1`, sans quoi le tampon est
perdu avec le processus et la derniere ligne avant la faute n'arrive jamais
sur le disque.

### 11.8 La reparation est PAYEE -- mesure du 8 nov 2026

Deux courses de **500 images**, memes variables sauf la reparation :

| | avant (host_log.avant418.txt) | apres (VF5_TITRE_AET=1) |
|---|---|---|
| tirages, 500 images | **1000** | **9007** |
| ClearRenderTargetView | 510 | 510 |
| noeuds 2D a l'image 400 | **0** | **61** |

Le repartiteur passe a NUL aux deux etapes attendues, et nulle part ailleurs
(2 lignes `418 :` sur toute la course) :

```
418 : image 307 : repartiteur NUL pour CS_TITLE etape 2
418 : image 315 : repartiteur NUL pour CS_TITLE etape 3
```

1000 tirages, c'est 2,00 par image : les deux quads de fond, et rien d'autre.
9007, c'est 18,0 par image. **Le module batit bien son ecran-titre lui-meme.**

### 11.9 OU vit l'ecran-titre : la question du SS 415, repondue

Recensement des 61 noeuds a l'image 400 -- l'auto-test par noeud
(`+0x1c == panier`) passe **61 sur 61** :

| couche | creneau | noeuds |
|---|---|---|
| **0** | **1** | **45** |
| **3** | **25** | **15** |

Deux emplacements, pas davantage. Les noeuds portent de vrais sprites et de
vraies textures (`spr=0x021B0063` tex=`...D27D1EB8`, `spr=0x021B00A6`
tex=`...D11583E8`), en mode 9 -- le mode du quad lu statiquement au SS 416 --
et des alphas qui DESCENDENT d'un noeud au suivant (`0xFFFFFFFF`, puis
`0x66FFFFFF`, `0x62FFFFFF`) : une animation en cours de fondu.

**Et zero noeud << BLANC OPAQUE SANS SPRITE >>** (`spr == 0xFFFFFFFF &&
coul == 0xFFFFFFFF`) sur les 61. Les deux quads blancs ne sont donc PAS dans
ces listes -- ce qui concorde avec
[[les-deux-quads-sont-le-fond-pas-un-rideau]] : ils sont le fond, emis
ailleurs, et non un rideau pose par-dessus dans un creneau tardif.

### 11.10 L'auto-test d'identite a PRIS EN DEFAUT ses propres offsets

```
417 : IDENTITE du SprMgr 000001FF89E29630 -- [+0x814]=0 (ATTENDU 13)
      [+0x818]={1280.0, 720.0, 0.0, 0.0} (ATTENDU {0,0,1280,720})
      >>> LE POINTEUR OU LA DISPOSITION EST FAUX : tout releve est A JETER
```

Le motif attendu est la, **decale de 8 octets** : `{0,0,1280,720}` commence
en `+0x810`, pas en `+0x818`, et `+0x814` est le second zero, pas le mode.

D'ou venaient ces offsets ? Du **SS 404** -- et `grep "404 :"` ne rend AUCUNE
ligne, dans aucune course du dossier. La sonde 404 n'a jamais tourne : ses
offsets n'avaient jamais ete valides, ils avaient seulement ete ECRITS, puis
recopies dans la 417. L'auto-test les a attrapes a son premier tir reel.

**Les deux tests ne se contredisent pas** : celui par noeud porte sur la
region des listes (`mgr + 8 + gr*0x200 + k*0x10`) et passe 61 fois sur 61,
de facon independante ; celui d'identite porte sur les champs d'etat en fin
de bloc. C'est le second qui est faux. Le recensement du 11.9 tient ; la
geometrie et le mode restent **INCONNUS** en offset exact.

Au SS 418.2 l'auto-test ne suppose plus : il **balaie** `+0x800..+0x830`,
rapporte ou le motif et la valeur 13 se trouvent, vide les 12 mots en clair,
et dit << INTROUVABLE >> quand il ne trouve pas.

### 11.11 VALIDE A L'OEIL -- 8 novembre 2026

Course de **1800 images**, configuration par defaut du lanceur de
`host_revo` plus le seul journal. **Aucun** `VF5_SAUTER_TIRAGES`, **aucun**
`VF5_TITRE_TIENT`, **aucun** `VF5_SANS_RAPPEL`, sonde des creneaux eteinte.

> Reponse de l'utilisateur, qui seul juge de l'image : **<< L'ecran-titre
> s'affiche >>**.

| | valeur |
|---|---|
| images | 1800 en 31,43 s = **57,3 i/s** |
| tirages | **72 458** = 40,3 par image (2,00 avant la reparation) |
| echecs de Present | 0 |
| repartiteur ote | images 307 et 315 **seulement** |
| cout | `rappel+0x40` 7,85 ms sur 16,47 -- c'est le MODULE qui travaille |

C'est la premiere fois que l'ecran-titre arrive **par une cause otee** et non
par un interrupteur qui masque des tirages legitimes.

**Ce que cette course ne dit PAS**, et qu'il ne faut pas lui faire dire :
elle n'a rien mesure des trois autres ecrans fixes, ni de la SORTIE de
CS_TITLE (la destruction des objets AET du SS 412), ni du son.

### 11.12 LA SORTIE DE CS_TITLE -- mesuree, et pas de debordement

Course de **2700 images**, defauts du lanceur, sonde a l'image 2200.
Aucun interrupteur de confort, aucune manette simulee.

**La sortie arrive toute seule, par le delai du binaire** (1800 tics depuis
l'entree de phase 0, soit l'image 307) :

| image | ce qui se passe |
|---|---|
| 307 / 315 | CS_TITLE etapes 2 et 3 : le module batit son titre |
| **2117** | **CS_TITLE phase 2** -- le SS 412 tire pour `5=CS_TITLE`, pour la premiere fois de tout le chantier |
| 2119 | CS_DEMO phase 2 -- il entre et ressort en **2 images** (cf. [[cs-demo-ne-sort-que-par-la-242]]) |
| 2120 / 2128 | CS_TITLE de nouveau, etapes 2 et 3 : le titre est **rebati** |

Predit 2107, mesure 2117. La boucle attract <-> titre du binaire tourne.

**ET RIEN NE S'ACCUMULE.** C'etait la crainte du SS 412 (<< le 3eme ecran
deborde >>, destruction manquante des objets AET) :

| | noeuds 2D |
|---|---|
| image 400, **premiere** visite de CS_TITLE | **61** |
| image 2200, **deuxieme** visite, apres un cycle complet | **65** |

65 et non ~122 : la phase 2 libere bien, et les deux emplacements sont les
memes qu'au premier passage -- `(couche 0, creneau 1)` 49 noeuds et
`(couche 3, creneau 25)` 11. L'auto-test par noeud passe **65 sur 65**.
Degre : **ETAYE** sur UN cycle. Rien n'est mesure sur dix cycles.

### 11.13 Les offsets du SprMgr, enfin MESURES

L'auto-test corrige du SS 418.2 ne suppose plus, il balaie -- et il PASSE :

```
418.2 : motif {0,0,1280,720} TROUVE   valeur 13 TROUVEE
        >>> POINTEUR ET DISPOSITION PROUVES
418.2 : geometrie en +0x810
418.2 : mode d'ecran en +0x80C
418.2 : +0x800 : 00000000 00000000 3FE38E39 0000000D
418.2 : +0x810 : 00000000 00000000 44A00000 44340000
418.2 : +0x820 : 00000000 00000011 0000000D 00000000
```

| offset | contenu | lecture |
|---|---|---|
| `+0x808` | `0x3FE38E39` | **1,7778 en flottant = 16/9**, le rapport d'image |
| `+0x80C` | `0x0000000D` | **le mode d'ecran = 13** (le `MOV EAX,0xD` du SS 401) |
| `+0x810` | `{0, 0, 0x44A00000, 0x44340000}` | **{0, 0, 1280.0f, 720.0f}** |
| `+0x820` | `0` | la couche courante |
| `+0x824` / `+0x828` | `17` / `13` | non elucides |

**Tous les offsets du SS 404 etaient decales de +8** -- mode, geometrie et
<< facteur de projection >> compris. Voir
[[les-offsets-du-sprmgr-n-ont-jamais-ete-valides]].

### 11.14 MA DESCRIPTION DE LA REPARATION ETAIT TROP ETROITE

J'ai annonce un retrait du repartiteur << borne aux deux etapes 2 et 3 >>.
**C'est faux en pratique**, et le compteur de la sonde le prouve : il vaut 9
a l'image 315 et **1812** a l'image 2120, soit 1803 images de plus pour 1805
images ecoulees. Donc le repartiteur est NUL **presque tout le temps que dure
CS_TITLE**.

La raison : `mo+0x34` passe a 3 a l'image 315 et **n'en bouge plus** pendant
toute la phase 1. Mon test `etape == 2 || etape == 3` ne borne donc rien dans
le temps -- il equivaut, de fait, a `VF5_SANS_RAPPEL=5`, precisement ce que le
SS 412 jugeait << trop grossier >>.

Ce que ca change, et ce que ca ne change pas :

* **ca marche** : le titre s'affiche, la sortie a lieu, la boucle tourne, rien
  ne s'accumule ;
* le module ne peut plus appeler l'hote pendant CS_TITLE -- sans consequence
  connue ici, puisque les commandes 16/18 ne sont pas servies de toute facon ;
* la commande `0x19E` (414), que la sortie PAR APPUI reclame, est **sautee**.
  Cette course sort par le delai, donc elle ne le dit pas. **INCONNU.**
* le reproche de clignotement du SS 412 porte donc toujours sur ce code ; seul
  son oeil peut dire s'il clignote.

Si une bornure reelle devient necessaire, elle ne peut pas s'appuyer sur
`mo+0x34` : il faudrait la phase (`mo+0x28`), par exemple
`phase == 0 && (etape == 2 || etape == 3)`.

### 11.15 L'APPUI MARCHE, LA CHAINE AVANCE, ET LE MODULE FAUTE

Course du 8 nov 2026, 2700 images demandees, `VF5_CLAVIER=1`, reparation
**bornee a la phase 0** (SS 418.3). Elle n'est pas allee au bout.

#### Ce qui est ACQUIS

**1. La bornure par la phase ne casse rien.** L'utilisateur a vu
l'illustration du titre -- logo Virtua Fighter 5, fond, << FINAL SHOWDOWN >>.
Exiger `phase == 0` suffit donc, et le repartiteur peut revenir pendant le
maintien. La version large du SS 418 etait inutilement etendue.

**2. Le clavier marche de bout en bout.** Le journal porte la preuve, bit
pour bit :

```
338.14 : image 387 : bloc+0x20 = 0x00002000 [BAS ]    axes +0.0 / +1.0
338.14 : image 390 : bloc+0x20 = 0x00001000 [HAUT ]   axes +0.0 / -1.0
338.14 : image 398 : bloc+0x20 = 0x00000100 [START ]  axes +0.0 / +0.0
```

`0x100` = bit 8 = `BUTTON_START`, exactement la numerotation `sl::BUTTON`.
Le defaut etait **eteint** (`VF5_CLAVIER`), et le lanceur ne le pose pas.

**3. La sortie PAR APPUI passe, et la commande 414 n'etait pas un verrou.**
Sous-etats atteints, nouveaux : `2=WARNING` (phases 1 et 2) et
`6=CS_SIGNIN` (phase 2). Le mode demande **MENU**.

#### Ce qui CASSE

**Les tirages s'emballent.** Sur le titre : 40 par image. Juste avant la
faute, a l'image 731 :

```
DrawIndexedInstanced 906529 (+4505)  sur 1 image(s)
```

**4505 tirages en une image**, stables sur les six derniers releves (4451,
4466, 4490, 4467, 4505, 4505). Ce n'est pas une rampe, c'est un REGIME. Et
l'utilisateur, qui seul juge de l'image : << l'ecran etait bugge >>.

**Puis le module faute -- a la MEME adresse qu'hier.**

```
Module defaillant : vf5fs-pxd-w64-d3d12_SteamRetail.dll
Exception code    : 0xc0000005
Fault offset      : 0x2f7aee      ->  Ghidra 0x1802F7AEE
```

C'est `FUN_1802F7AD0`, le free interne, appele par `FUN_1802F76A0` qui
recupere l'allocateur dans l'en-tete du bloc (`[p-0x10] >> 16`). Deux fautes
identiques : ce n'est pas un accident d'extinction, **c'est reproductible**.

#### Ce que la mesure ECARTE deja

* **Notre allocateur n'est PAS en cause par le chemin evident.** Le detecteur
  << LIBERATION ETRANGERE >> de l'hote n'a crie **aucune** fois (`grep` = 0).
* **L'hote ne touche ni `FUN_180279BD0` ni `0x18064B360`** (grep dans
  `vf5fs_host.cpp` : zero occurrence). Or `FUN_180279BD0` est l'entree
  d'allocation du module -- un aiguillage par TLS
  (`GS:[0x58]` + `[0x18124F0A8]`, repli sur `[0x18064B360]`). Les blocs de
  0xF8 des requetes 2D viennent donc de **l'allocateur du module**, qui ecrit
  lui-meme l'en-tete que son free relit.

Donc l'hypothese << notre hote rend des blocs sans en-tete >> est
**AFFAIBLIE**, pas confirmee. Reste la plus simple compte tenu du reste :
**une corruption**. 4505 requetes par image x 0xF8 = ~1,1 Mio d'allocations
par image dans le tas du module ; un debordement y clobberait l'en-tete d'un
bloc voisin, et le free suivant lirait un allocateur invalide.

Degre : **ETAYE** pour la faute et sa reproductibilite ; **SPECULATIF** pour
la corruption. Ce qui n'est pas mesure : CE QUE sont ces 4505 tirages.

#### Le prochain pas, et il est unique

Relever la sonde des creneaux **pendant** le regime a 4505 (par exemple
`VF5_SONDE_CRENEAUX=700`) : elle dira les `(couche, creneau)`, les sprites et
les textures de ces tirages. Tant qu'on ne sait pas ce qu'ils dessinent, tout
le reste est une hypothese.

A noter aussi, dans le meme journal : `TaskSelector`, `TaskCsOfflineWarning`,
`TaskAutoLoad` et la tache de sauvegarde sont toutes
<< morte [ABSENTE de la liste] >>. Les ecrans qui devraient tourner ne
tournent pas, et pourtant quelque chose emet des milliers de quads.
