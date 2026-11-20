# Ajouter un décor à VF5FS APM3 : ce qu'il faut toucher, et dans quel ordre

Établi le 2026-09-07 sur `vf5fs-pxd-w64-Retail_APM3.dll.origine` et sur
`vf5fs_data.par`. Complète `analysis/decors.md` (le code) et
`analysis/import_decors.md` (la livraison des fichiers).

> **LA RECETTE À JOUR EST DANS `analysis/decors.md` §16 et §17** (2026-09-10),
> et elle est plus large que ce document : **dix** fichiers et non neuf,
> **six** tables indexées par le décor et non trois, `obj_db` **écrit dans le
> `.par`** parce que les bases sont embarquées dans le binaire, et les objets
> **renommés** parce que leur index est global. Ce qui suit reste juste sur la
> table des descripteurs, les bornes et la grille ; pour tout le reste, §16-17
> a la priorité.

---

## 1. La bonne nouvelle : l'identifiant d'un décor est une DONNÉE

C'est le point qui décide de la faisabilité, et il est prouvé.

Le descripteur d'un décor (`0x180403430 + index*0xF0`) porte en `+0x10` un
**identifiant d'objset**, passé tel quel à `0x1800F9C60` pour demander la
géométrie. On pouvait croire cet identifiant câblé. Il ne l'est pas : il est
recherché par **dichotomie** dans un vecteur construit au démarrage
(`0x1800F9450` → `[0x18070FA90]`, enregistrements de 0x200 octets, clef = le
dword de tête), et ce vecteur est rempli par `0x18006B7E0`, qui lit :

```
0x1800F9803  lea rdx, "./rom/objset/"
0x1800F981A  lea rdx, "obj_db.bin"
```

**`rom/objset/obj_db.bin`** (1 141 248 o dans le `.par`, extrait dans
`extracted/obj_db.bin`). Son format se lit sans peine :

| | |
|---|---|
| `+0x00` u32 | 0x179C — nombre de jeux d'objets |
| `+0x04` u32 | 0x1805 |
| `+0x08` u32 | **0x042760 — la table des jeux d'objets** |
| `+0x0C` u32 | 0x4550 = 17 744 — nombre d'objets |
| `+0x10` u32 | 0x0F3F80 — la table des objets, 8 o par entrée, elle finit **exactement** sur la fin du fichier |
| `0x20`… | le pot commun des chaînes, terminées par zéro |

Chaque jeu d'objets fait **0x24 octets** :

```
+0x00  u32  offset du NOM         "STGARE"
+0x04  u32  IDENTIFIANT           22
+0x08  u32  offset du fichier obj "stgare_obj.bin"
+0x0C  u32  offset du fichier tex "stgare_tex.bin"
+0x10  u32  offset de l'archive   "stgare.farc"
+0x14..+0x20  quatre u32 à zéro
```

Vérification croisée, et c'est elle qui emporte la décision : **les 41
identifiants du descripteur correspondent un pour un à `obj_db.bin`**, y compris
les trois qui cassent la suite :

```
STGARE  index 22  id   22        STGDU4  index 32  id   33
STGDJO  index 28  id   28        STGDU5  index 33  id 5529   <-
STGDU1  index 29  id   30   <-   STGGYM  index 51  id 2847   <-
STGDU2  index 30  id   31        STGSMO  index 52  id 2848   <-
```

L'identifiant **n'est pas la position** dans la table, l'espace des
identifiants est **troué** (29 n'est attribué à personne) et il accepte des
valeurs très hautes. `stgdu5`, `stggym` et `stgsmo` ont manifestement été
ajoutés après coup, avec des identifiants pris ailleurs. **On peut donc faire
la même chose : rien dans le moteur ne borne cet espace.**

Confiance : **CONFIRMED** (table lue, 43 entrées `STG*` recoupées avec le
descripteur du binaire).

---

## 2. La famille complète des bases de données

`obj_db.bin` n'est pas seul. Le `.par` en porte six, toutes lues au démarrage :

| fichier | taille | ce qu'il nomme |
|---|---:|---|
| `obj_db.bin` | 1 141 248 | les jeux d'objets (géométrie) — **id ↔ nom ↔ `.farc`** |
| `tex_db.bin` | 841 776 | les textures |
| `spr_db.bin` | 1 524 752 | les sprites (les icônes `stage_icon_*_c`) |
| `aet_db.bin` | 45 520 | les scènes AET (les calques `ban_stay`, `dur_stay`…) |
| `auth_3d_db.bin` | 223 565 | les jeux d'animation — **`STGARE`, `EFFSTGARE`** |
| `mot_db.bin` | 290 208 | les mouvements |

C'est la famille de bases du moteur SEGA de cette génération. Un décor complet
touche **`obj_db`**, **`tex_db`** et **`auth_3d_db`** ; ses icônes de menu
touchent **`spr_db`** et **`aet_db`**.

---

## 3. La recette, dans l'ordre des dépendances

### 3.1 Les fichiers du décor (voir `import_decors.md`)

```
rom/objset/stgXXX.farc          geometrie + textures  (obj + tex)
rom/auth_3d/STGXXX.farc         animation du decor
rom/auth_3d/EFFSTGXXX.farc      effets
rom/STGXXX_COLI.000.bin         collision
rom/ibl/xxx.ibl                 eclairage par image
rom/light_param/{light,fog,glow,wind,envmap_correct}_xxx.txt
rom/sound/se_stage_xxx.csb      ambiance   (facultatif)
rom/sound/bgm/*.adx             musiques   (facultatif : on peut reutiliser)
```

**Piège de livraison, déjà payé** : ce qui est dans le `.par` vient du `.par`.
Un fichier neuf dont le nom n'existe pas dans l'archive est cherché sur
l'arborescence libre `vf5fs_media/` — donc un décor **nouveau** se dépose
librement, sans toucher au `.par`. C'est le cas facile. C'est le
**remplacement** d'un décor existant qui oblige à masquer l'entrée
(`tools/par_masquer.py`).

### 3.2 Les bases de données

1. **`obj_db.bin`** : une entrée de 0x24 octets, avec un identifiant libre
   (prendre par exemple 6000, l'espace est troué et non borné), le nom
   `STGXXX`, et les trois noms de fichiers. Incrémenter le compte en `+0x00`.
   Les chaînes vont dans le pot commun — donc le fichier se **reconstruit**,
   il ne se rustine pas en place.
2. **`tex_db.bin`** : les textures du décor, même logique.
3. **`auth_3d_db.bin`** : les deux jeux `STGXXX` et `EFFSTGXXX`, sans quoi
   l'état 2 du chargeur (`0x18003C200`) ne trouvera rien.

### 3.3 Le moteur : le descripteur et le code à trois lettres

Deux tables parallèles, **41 entrées chacune, indexées par le même index** :

| table | contenu | borne écrite dans le code |
|---|---|---|
| `0x18039F7A0` | 41 pointeurs vers le code à 3 lettres (`"are"`) | `0x1800D7130 : cmp ecx, 0x28` |
| `0x180403430` | 41 descripteurs de `0xF0` octets | `0x18018EF6C : cmp edx, 0x29`, `0x18018F5E1 : cmp r9, 0x2670` |

Le champ décisif du descripteur est `+0x10` — l'identifiant `obj_db`. Le reste
est décrit champ par champ dans `analysis/decors.md` §2.

**Deux voies, et elles n'ont pas le même coût :**

* **Voie A — recycler un emplacement.** On écrase l'un des 17 décors d'essai
  (`tst ts2 ts3 wht trm cid trs evo00..evo09`) : on garde 41, on ne touche à
  aucune borne, on ne touche à aucune table indexée par le décor. C'est la voie
  à prendre en premier. Elle coûte un descripteur (0xF0 octets) et un
  pointeur.
* **Voie B — passer à 42.** Il faut alors déplacer les deux tables (elles sont
  en `.rdata`, coincées entre voisines : pas de place derrière), et corriger
  **au moins six bornes** : `0x1800D7130`, `0x18018EF6C`, `0x18018F3D6`,
  `0x18018F560`, `0x18018F630`, `0x18018FCF0`, `0x18018F5E1`. Plus les tables
  de la grille de sélection (§3.4). Réaliste, mais ce n'est plus une retouche.

**Ne pas oublier le nom.** `0x18018F590` résout un nom (`"STGDJO"`) en index par
`strcmp` sur les 41 descripteurs, et c'est **par ce chemin** que
`rom/game_score.txt` associe un personnage à son décor. Renommer un descripteur
sans corriger `game_score.txt` fait rendre `-1`, et `-1` ne demande aucun décor :
l'écran ne change pas, et rien ne le signale.

### 3.4 Les écrans (facultatif, mais c'est ce qui rend le décor choisissable)

* **La liste des aperçus**, dans `TaskSelStage` (`0x180174BF0`) : 25 entrées de
  0x18 octets `{index, "xxx", "xxx_stay"}`, terminées par un index `-1`. Les
  deux chaînes sont des calques AET.
* **La grille d'icônes**, deux tables de 0x20 octets choisies selon
  `[0x180C3B6F0]+0x1FE10` (`0x180174B60`) :
  * `0x180400210`, **21 entrées, 3 lignes × 7 colonnes**, avec l'icône
    (`stage_icon_are_c`) — la grille hors-ligne ;
  * `0x1804004B0`, **22 entrées, 2 × 11**, sans icône — la variante bornes
    liées.
  * enregistrement : `+0x00` colonne, `+0x04` ligne, `+0x08` **index du
    décor**, `+0x0C`/`+0x10` = 332/331 (le pas de cellule), `+0x18` nom
    d'icône.
  * Les cinq décors de Dural : la grille hors-ligne n'en porte **qu'un**
    (`du1`, index 21, case ligne 2 colonne 6). `du2`..`du5` n'y sont pas.

~~**Réserve à ne pas taire** : rien ne prouve que `TaskSelStage` soit
piloté.~~ **Levée le 2026-09-07** : `TaskSelStage` est un MEMBRE de
`TaskSelector` (`+0x3B0`), enregistré comme tâche **`SEL_STAGE`** en
`0x18016CC6C`, depuis `TaskSelector::update` (`0x18016C8CE`). Il est donc bien
piloté — et l'écran s'affiche, capture à l'appui.

---

## 4. Les tables indexées par le décor : l'inventaire à faire avant de bouger

Le chantier 3SX a laissé une leçon transposable : *une trentaine de tables
indexées par l'étage, et trois qui plantent SANS message*. Ici, l'inventaire
des lectures indexées par l'index de décor, tel qu'il ressort du balayage :

| site | table / effet | ce qui se passe hors bornes |
|---|---|---|
| `0x1800D7130` | `0x18039F7A0[i]` | `cmp ecx,0x28 ; ja ret` — **protégé** |
| `0x18018EF6C` | `0x180403430 + i*0xF0` | `cmp edx,0x29 ; jae` → descripteur nul — **protégé** |
| `0x18018F3D0` | musiques `+0x70 + type*8` | `cmp r10d,0x29` — **protégé** |
| `0x18018F560` | nom | `cmp ecx,0x29` — **protégé** |
| `0x18018F630` | propriété `+0xD4` | `cmp ecx,0x29` — **protégé** |
| `0x18018FCF0` | la demande | `cmp ecx,0x29 ; jge ret` — **protégé** |
| `0x18018F590` | nom → index | borne `0x2670` = 41×0xF0 — **protégé** |
| `0x180174B60` | grille (21 ou 22) | boucle bornée, rend 0 si absent — **protégé** |
| `0x18018F15D` | effet de scène des index **8 et 9** | comparaison directe, pas de table |
| `0x18018FAC6` | drapeau de rendu des index **0x10 et 0x28** | idem |
| `0x1801B648D`, `0x1801B6507` | compteurs de parties, `41` entrées de 0x10 o | `cmp r8d,0x29` — **protégé, et à NE PAS lever** : voir §7.5. (`0x1801B5F7F`, qu'une version antérieure de ce tableau citait, est un début de fonction `.pdata`, pas une comparaison.) |

**Aucune table indexée par le décor n'est laissée sans borne.** C'est la
différence avec le chantier 3SX : passer à 42 décors demande de lever des
bornes, pas de deviner où ça plantera.

---

## 5. Ce qui reste ouvert

1. ~~**La structure interne de `obj_db.bin` au-delà de la table des jeux
   d'objets**…~~ **Expliquée le 2026-09-09** : la zone est le **second pot de
   chaînes**, les noms d'objets, et il commence à `0x77950` — exactement où
   finit la table des jeux. Le reconstructeur existe : `tools/obj_db.py`,
   aller-retour à l'octet près. Voir `analysis/obj_db.md`.
2. ~~**`auth_3d_db.bin` et `tex_db.bin`** ne sont pas encore ouverts.~~
   **`auth_3d_db.bin` est ouvert** le 2026-09-09 : c'est du TEXTE, un
   dictionnaire `clé=valeur` trié comme des chaînes — voir
   `analysis/auth_3d_db.md` et `tools/a3d_db.py`. **`tex_db.bin` aussi**, le
   même jour : `analysis/tex_db.md` et `tools/tex_db.py`. Les trois bases sont
   lues et réécrites, aller-retour à l'octet près.
3. **La liaison objet↔indice** : les champs `+0x14`…`+0x34` du descripteur sont
   des identifiants d'objets `auth_3d`. Un décor importé d'une autre génération
   ne les respecte pas — c'est exactement ce qui avait fait boucler l'essai DJO
   de VF5 R sur l'écran de chargement (`import_decors.md` §7). **Un décor
   s'importe avec sa génération entière.**
4. ~~**`TaskSelStage` est-il piloté ?**~~ Oui, mesuré — voir §3.4.
5. **L'aperçu d'un décor est du CODE**, pas une table : construit instruction
   par instruction vers `0x180174BF0`. Ajouter un aperçu demande une caverne.
   Voir §6.4.

---

## 6. AJOUTER sans remplacer, et rendre sélectionnable (mesuré le 2026-09-07)

### 6.1 Il y a déjà **dix-sept** emplacements libres

`tst ts2 ts3 wht trm cid trs evo00…evo09` sont des décors d'essai, de 0 à
1,2 Mo. Les occuper, ce n'est pas remplacer un décor : **aucun décor réel n'est
perdu, et aucune borne n'est touchée** — la table reste à 41. C'est la voie A,
et `du5`, `gym`, `smo` prouvent qu'elle est celle du studio lui-même : ajoutés
après coup, avec des identifiants d'objset pris ailleurs (5529, 2847, 2848).

Ce qu'un emplacement recyclé demande, décor importé par décor importé :

| pièce | ce qu'il faut faire | coût |
|---|---|---|
| `stgXXX.farc` | renommer l'archive **et ses deux entrées internes** (`stgdur_obj.bin` → `stgtrm_obj.bin`, même longueur : substitution d'octets en place) | fichiers |
| `ibl`, `light_param` | renommer au code à trois lettres de l'emplacement | fichiers |
| collision | l'emplacement pointe sur `rom/STGDU1_COLI.000.bin` ; écrire la vraie chaîne dans le mou de `.rdata` comme `--du2-collision` | ~140 o de mou restants |
| descripteur `+0x14`…`+0x34` | y écrire les identifiants d'objets **réels** de l'objset importé | option de patcheur |
| `auth_3d` | **non bloquant** : `du1` n'a aucun `auth_3d/STGDU1.farc` et se charge quand même. La porte 4 tolère un jeu absent | rien |

Au-delà de dix-sept, il faut la voie B (table à 42+), et là il faut déplacer les
deux tables et lever huit bornes. **Inutile tant que les dix-sept ne sont pas
pris.**

### 6.2 La grille peut grandir — mais PAS là où on l'a cru

> **CORRIGÉ le 2026-09-09.** Ce qui suit annonçait « 0x560 octets d'affilée =
> 43 cases ». **C'est faux** : après la seconde table viennent deux qwords
> (`-1`, `0`) puis, immédiatement, **les chaînes `stage_icon_*_c` que la grille
> elle-même pointe** — `0x180400778` porte `stage_icon_are_c`. Y écrire des
> cases détruirait les noms d'icônes. La grille **déménage** désormais dans
> `.decors` avec ses relocations (`--grille-table`), et sa taille n'est plus
> bornée par ses voisines. Le reste de la section garde sa valeur : les
> compteurs y sont justes.

Les deux tables de cases sont **adjacentes**, et suivies immédiatement de la
liste d'exclusion :

```
0x180400210   grille hors ligne     21 cases x 0x20   = 0x2A0
0x1804004B0   grille bornes liees   22 cases x 0x20   = 0x2C0
0x180400770   liste d'exclusion (premiere entree -1 : n'exclut rien)
```

Soit **0x560 octets d'affilée = 43 cases**. La seconde table ne sert qu'au mode
bornes liées, que ce build n'utilise pas : on peut donc étendre la première
jusqu'à 43 cases, ou plus prudemment **28 (4 lignes x 7)**, et pointer les deux
`lea` sur la même table.

Les compteurs à corriger sont **trois seulement** — les autres `0x15` du
voisinage sont des identifiants de calques AET ou l'index du décor `du1`, pas
des comptes :

```
0x1801746D2   mov r8d, 0x15    le compte passe au constructeur (0x180173BD0)
0x1801746C3   mov r8d, 0x16    idem, variante bornes liees
0x18017493C   cmp rbx, 0x15    boucle qui cherche la case ALEA
0x180174BBE   cmp rax, 0x15    boucle index de decor -> case
```
plus la borne `0x2A0` du tirage au sort, dans `0x1801749F0`.

### 6.3 Les nouvelles cases se placent toutes seules

Lu dans `0x180173BD0`, et c'est le point qui rend la 4e ligne possible :

* si la case a une **ancre** (`+0x18`, un `stage_icon_xxx_c`), sa position vient
  du sprite : `0x1800298B0(nom)` puis `[rax+0x40]` (x, y) et `[rax+0x48]` ;
* le constructeur garde la dernière case ancrée (`+0x60` colonne, `+0x64`
  ligne) et calcule deux **gradients** — `xmm11` par colonne, `xmm10` par
  ligne ;
* **une case SANS ancre est extrapolée** : `position = référence + (colonne −
  colonne_de_référence) × gradient`.

Une nouvelle case n'a donc **pas besoin d'icône** : on met `+0x18 = 0` et elle
se pose au pas régulier de la grille. C'est exactement l'inverse de l'erreur du
2026-09-07 (repointer `+0x18` sur une ancre existante empilait les cases).

Reste à voir **à l'écran** si une 4e ligne tombe dans le cadre : la grille
occupe le tiers bas. C'est une mesure d'image, pas de code.

### 6.4 La vraie limite : l'aperçu est du CODE, pas une table

La liste des aperçus n'est pas une table de données : elle est **construite
instruction par instruction** sur la pile, autour de `0x180174BF0` —
`mov [rbp+0xD0], 0x14 ; lea rax, "tan" ; mov [rbp+0xD8], rax ; lea rax,
"tan_stay" ; …`, 0x18 octets par entrée. Ajouter un aperçu, c'est donc écrire
du code dans une caverne, pas ajouter une ligne.

Trois issues, par coût croissant :

1. **ne rien faire** : la nouvelle case n'a pas d'aperçu. On voit si c'est
   gênant ;
2. **détourner une entrée existante** : les cinq décors de Dural partagent déjà
   `dur`/`dur_stay` ; changer l'immédiat d'index d'une de ces entrées la donne
   à un autre décor ;
3. **recopier la construction dans une caverne** et détourner l'appel — la plus
   grosse caverne `int3` fait 21 octets, il faut donc du mou, pas une caverne.

---

## 7. Les deux tables DÉPLACÉES — la voie B commence ici (2026-09-09)

`--decors-table [N]`, lanceur `tools/decors_table.cmd`, contrôle
`tools/verifier_decors_table.py`. Le préalable est
`analysis/greffe_relocations.md` : une section greffée porte désormais ses
relocations.

### 7.1 Ce qui bouge, et rien d'autre

| table | où elle était | où elle est |
|---|---|---|
| 41 descripteurs de `0xF0` | `0x180403430` | `.decors` + 0 |
| 41 pointeurs de code à trois lettres | `0x18039F7A0` | `.decors` + `0x2670` |

**556 pointeurs** suivent, chacun avec sa relocation. On ne devine aucun
décalage : **une relocation est recopiée là où `.origine` en a une**. La mesure
qui l'autorise : 515 pointeurs dans la table des descripteurs, à dix-sept
décalages (`+0x00 +0x08 +0x48 +0x50 +0x58 +0x60 +0x68 +0x70`…`+0xB0 +0xC0`),
répartis en 17 décors à 7 pointeurs (les emplacements d'essai), 12 à 16 et 12 à
17 ; plus les 41 de la table des codes, relogés 41 sur 41.

Le bloc des **murs** (`0x1804033E0`…`0x180403430`, cinq blocs de 16 octets, des
triplets 0/1/2) n'est **pas** relogé : ce sont des données, pas des pointeurs.
Il reste donc où il est, et `+0xC0` le vise toujours.

### 7.2 Les huit sites, énumérés et non devinés

`tools/refs_plage.py` cherche les références à une **plage**, pas à une
adresse : le moteur n'entre pas que par le premier octet d'une table.

| champ `disp32` | table | vise |
|---|---|---|
| `0x18018EF7B` | descripteurs | `+0x00` — le gestionnaire (`0x18018EF40`) |
| `0x18018F3DF` | descripteurs | `+0x00` — la musique |
| `0x18018F409` | descripteurs | **`+0x70`** — la base des neuf reprises |
| `0x18018F56B` | descripteurs | `+0x00` — le nom |
| `0x18018F59B` | descripteurs | `+0x00` — nom → index (`0x18018F590`) |
| `0x18018F642` | descripteurs | `+0x00` — la propriété `+0xD4` |
| `0x1800D6148` | codes | `+0x00` |
| `0x1800D713B` | codes | `+0x00` — compose `ibl/` et `light_param/` |

**Le champ à réécrire est le `disp32`, pas l'adresse d'instruction.** Capstone,
partant d'un octet mal aligné, lit parfois `lea eax` là où il y a `lea rax` :
l'adresse rapportée est alors décalée d'un octet, mais le `disp32` — dernier
champ de l'instruction — est au même endroit dans les deux lectures.

### 7.3 Aucune borne n'est levée, et c'est voulu

À `N = 41` le correctif ne touche **pas une seule** des huit bornes. Le jeu doit
donc se comporter exactement comme avant, ce qui permet de séparer « le
déplacement est faux » de « la borne est fausse ». `--decors-table <N>` avec
`N > 41` les lève ; la borne des « compteurs de parties » (`0x1801B5F87`) est
marquée **à relire** et le patcheur refuse de dépasser 41 tant qu'elle l'est.

### 7.4 Ce qui est vérifié

`verifier_decors_table.py`, sans lancer le jeu : octets identiques, huit sites
repointés, 556 relocations posées — ni une de moins ni une de trop —, aucune
relocation d'origine perdue, et un rebasage simulé qui corrige les 515
pointeurs.

Puis **dans le processus vivant**, le descripteur du dojo lu à sa nouvelle
adresse :

```
moteur en 0x7FFC62390000  (delta 0x7FFAE2390000)
   +0x00 nom auth_3d  ok   STGDJO
   +0x08 eff auth_3d  ok   EFFSTGDJO
   +0x48 collision    ok   rom/STGDJO_COLI.000.bin
   +0x68 musique      ok   rom/sound/bgm/vfes_bgm_stg_djo.adx
   +0xC0 MURS         ok
   code du decor 11 : 'djo'      code du decor 28 : 'trs'
```

**Pas encore vu à l'écran.** C'est `tools/decors_table.cmd` qui le montre, et
ce qu'il faut regarder est écrit dedans : rien ne doit avoir changé.

### 7.5 La septième borne ne se lève pas : c'est une taille de tableau

La boucle des **compteurs de parties** n'indexe pas une table de `.rdata` :
elle recopie des compteurs d'un objet vers un autre.

```
0x1801B6483  cmp r8d, 0x22    la version deroulee par huit  (N - 7)
0x1801B648D  cmp r8d, 0x29    l'entree de la boucle
0x1801B6507  cmp r8d, 0x29    la boucle simple
    source       [r14 + 0x11FC + i*8]      parties, victoires
    destination  [rdi + 0x1A2EC + i*0x10]  trois dwords et un ratio
```

**Les deux tableaux font exactement 41 entrées**, et deux instructions qui
suivent la boucle le prouvent : `lea rsi, [rdi + 0x1A580]` — or
`0x1A2EC + 41*0x10 = 0x1A57C` — et `lea rbx, [r14 + 0x1348]` — or
`0x11FC + 41*8 = 0x1344`. Le champ suivant commence juste après.

Lever cette borne écrirait dans le champ d'à côté. Elle reste à 41 : les décors
ajoutés n'auront pas de compteur de parties, et `patch_moteur.py` le dit dans
son compte rendu.

**À retenir avant de lever la suivante** : toutes les bornes à 41 ne sont pas
des bornes de table. Certaines sont des **tailles de tableau dans une
structure**, et la seule façon de les distinguer est de regarder ce qui suit le
tableau.
