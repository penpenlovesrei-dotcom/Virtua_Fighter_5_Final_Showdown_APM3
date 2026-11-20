# LES SCENES `auth_3d` D'UN DECOR : QUI LES CREE, ET OU UN DECOR AJOUTE LES PERD

Releve le 2026-11-20. **Aucune course, aucun lancement.** Tout est lu
statiquement dans `VF5RE/analysis/vf5fs_apm3_origine.dll`
(sha256 `045c0696…0837eef`, image base `0x180000000`) avec REA/Ghidra, plus
**une** lecture d'octets de la DLL patchee du jour
(`VF5RE/runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll`, 2026-11-20),
signalee comme telle en §3.

Cette note repond au §21.5 point 1 de `analysis/brume_decor_aoi.md` :
« **qui remplit `[tache+0x68]`** ».

Les noms de fonctions ci-dessous sont **les noms que cette note propose**. Ils
n'ont pas pu etre poses dans la base Ghidra : le fournisseur refuse toute
mutation (`Windows Ghidra P0 does not admit database mutation`). Ils ne vivent
donc que dans ce document.

---

## 0. Correction prealable : `0x180070340` n'est PAS `setStage`

La vtable de `TaskEffectAuth3D` est en `0x18034EAF0`. Ses douze premiers
creneaux, **lus** (`read_bytes`, 96 octets) :

| creneau | adresse | role |
|---|---|---|
| 0 | `0x18006E5F0` | destructeur ; remet `[tache+0x58] = 0` |
| 1 | `0x180070340` | **init / attente** (cf. §2.5) |
| 2 | `0x18006FC30` | — |
| 3 | `0x180070250` | — |
| 4,5,6 | `0x180087430` | commun (trois fois la meme) |
| **7** | **`0x1800706B0`** | **`setStage(indice)` — c'est LUI qui remplit la liste** |
| 8 | `0x180070790` | — |
| 9 | `0x180087430` | commun |
| 10 | `0x1800708C0` | — |
| 11 | `0x180070850` | — |

`0x18006F380` appelle `(*vtable+0x38)(tache, indice)` : `+0x38` = creneau 7 =
`0x1800706B0`. `decors.md` §17.1 avait juste ; `brume_decor_aoi.md` §21.3
attribue par erreur le nom `setStage` a `0x180070340`, qui est le creneau 1.
La distinction compte : **`0x180070340` lit la liste, `0x1800706B0` l'ecrit.**

---

## 1. LE CHEMIN COMPLET, DU NOM DE CATEGORIE A LA SCENE JOUEE

### 1.1 `auth_3d_db.bin` est lu une fois, au demarrage

| nom propose | adresse | ce qui est lu |
|---|---|---|
| `a3d_db_demander_chargement_fichiers` | `0x180044540` | demande `rom/auth_3d/auth_3d_db.bin` (chaine `0x180348C30`, pointeur `0x180642020`) **et** `rom/auth_3d/auth_3d_setting.bin` ; pose deux rappels |
| `a3d_db_bin_parser_texte_A3DA` | `0x1800437F0` | le parseur de texte proprement dit |
| `a3d_db_apres_parse_dimensionner_tables` | `0x180038C20` | rappel d'apres-parse |

Ce que `0x1800437F0` **exige et fait** :

* **Garde d'entree** : taille > 0x0F **et** les octets 0..4 = `#A3DA` **et**
  l'octet 0x0F = `\n`. Sinon la fonction **ne parse rien et sort sans un mot**
  — la base reste vide.
* `category.length` -> dimensionne le vecteur des categories
  (enregistrements de **0x38**), puis remplit chacune depuis
  `category.<i>.value`.
* `uid.length` -> dimensionne le vecteur des uid (enregistrements de
  **0x50**), puis pour chaque `uid.<i>.value` :
  * `+0x00` = l'indice `i` ;
  * `+0x04` = **1 si la valeur commence par `A`**, 0 sinon. C'est le seul
    role du `A ` de `uid.3532.value=A STGJN5_EFF_MOYA` ;
  * le nom est pris a **valeur+2** (apres `A `) ;
  * et seulement si `+0x04 == 1` : lecture de `<valeur>.category` (rangee en
    `+0x28`) et de `<valeur>.size` (`+0x48`), inscription du couple
    (nom -> indice) dans l'index global des noms, et ajout du nom a la liste
    propre de la categorie.
* `0x1800388F0` trie l'index des noms a la fin.

`0x180038C20` ensuite : alloue le vecteur des categories **resolues** de
`0xF0` octets (une par categorie, nom en `+0xE0`), et un vecteur **dense
indexe par uid** de `0x88` octets dont `+0x7C` recoit l'indice de l'uid.
Les deux sont dimensionnes **depuis le fichier**, pas depuis une constante.

### 1.2 Du nom de categorie a l'archive

| nom propose | adresse | ce qui est lu |
|---|---|---|
| `a3d_categorie_par_nom_lineaire` | `0x180040E70` | parcours **lineaire** du vecteur de `0xF0`, `strcmp` sur `+0xE0`. Rend 0 si absent |
| `a3d_categorie_addref_et_charger` | `0x18003C200` | `++[cat+0xD8]` ; si le compte passe a 1, appelle le chargeur |
| `a3d_categorie_est_chargee` | `0x18003C1D0` | rend `[cat+0xE8] == 2` — **et rend `true` si la categorie est inconnue** |
| `a3d_categorie_composer_farc_et_charger` | `0x180038600` | compose `"rom/auth_3d/"` (chaine `0x180349CF8`) + `[cat+0xE0]` + `".farc"`, met `[cat+0xE8] = 1`, demande le fichier ; le rappel `0x180038BE0` met `[cat+0xE8] = 2` et range l'archive en `[cat+0xA0]` |

Le nom de l'archive vient donc **mot pour mot de la base**, jamais d'une table
du binaire. La chaine `auth_3d/%s.farc` (`0x1803F9438`) **ne sert pas aux
decors** : ses deux seuls references (`0x180151F6D`, `0x180152136`) sont dans
le chargeur de **personnage**, a cote de `auth_3d/NAGE_%s.farc`.

Le decor demande sa categorie d'effets depuis le descripteur `+0x08`
(`0x18018F945` -> `0x18003C200`, deja note dans `decors.md` ligne 164). Mais
ce n'est **pas** indispensable : la scene elle-meme reclame sa categorie
(§1.4).

### 1.3 D'un uid a une scene

| nom propose | adresse | ce qui est lu |
|---|---|---|
| `a3d_scene_creer_depuis_uid` | `0x18003C370` | rend une **poignee** de scene, ou `0xFFFFFFFF` |
| `a3d_poignee_scene_valide` | `0x180041A80` | poignee -> creneau valide ? |
| `a3d_scene_uid_depuis_poignee` | `0x180041440` | rend `[creneau+0x2C0]` = l'uid |

`0x18003C370(sortie, uid)`, **lu** :

1. `uid < ([db+0x10] - [db+0x08]) / 0x50` — borne par le **nombre d'uid de la
   base**, pas par une constante ;
2. l'enregistrement de `0x50` existe et son `+0x04 != 0` (c'est-a-dire : la
   ligne commencait par `A `) ;
3. l'enregistrement dense de `0x88` a `[db+0x270] + uid*0x88` porte bien
   `+0x7C == uid` ;
4. puis **balayage de 0x60 = 96 creneaux** de `0x2C8` octets a partir de
   `[db]`, a la recherche du premier dont `+0x560` est negatif (libre) ;
5. la poignee rendue est `(compteur & 0x7FFF) << 16 | numero_de_creneau`, et
   elle est empilee dans la file `[db+0x288..0x298]`.

Si l'une des quatre conditions tombe : **`0xFFFFFFFF`, sans un message.**

### 1.4 De la scene au fichier `.a3da`, et au jeu

| nom propose | adresse | ce qui est lu |
|---|---|---|
| `a3d_scene_demander_chargement` | `0x180044830` | `++[uid_rec+0x78]` ; au premier, `[uid_rec+0x80] = 1` puis **addref + chargement de la categorie de l'uid** ; `[creneau+0x2A0] = 1` |
| `a3d_uid_nom_de_categorie` | `0x180046500` | l'uid -> son nom de categorie (`uid_rec+0x28`) |
| `a3d_uid_nom_de_scene` | `0x1800465C0` | l'uid -> son nom de scene (`STGJN5_EFF_MOYA`) |
| `a3d_uid_resoudre_a3da_dans_archive` | `0x180044690` | si `[uid_rec+0x80] == 1` et la categorie est a l'etat 2 : compose `<nom>.a3da`, le cherche dans l'archive, range donnees et taille, met l'etat a **2** ; rend `etat == 2` |
| `farc_index_par_nom_sinon_moins_un` | `0x180215E60` | recherche **lineaire, exacte, sensible a la casse** dans les noms de l'archive (pas de `0x98`). **Rend -1 si absent** |
| `farc_donnees_par_index_sinon_zero` | `0x180215D70` | borne `0 <= i < n` ; **rend 0 hors borne** |
| `a3d_scene_maj_etat1_vers_etat2` | `0x18003CE30` | la mise a jour d'une scene : si `[creneau+0x2A0] == 1`, interroge `0x180044690` ; si prete, passe `[creneau+0x2A0]` a **2**, **parse le texte du `.a3da`** et le lie a la scene ; si `== 2` et la scene est active, joue l'animation |
| `a3d_scene_est_prete_etat2` | `0x180044640` | rend `[creneau+0x2A0] == 2` ; **rend `true` pour une poignee invalide** |

Donc : `0x180044830` demande, `0x18003CE30` + `0x180044690` resolvent, et
c'est l'etat `[creneau+0x2A0]` (1 = demande, 2 = liee) qui porte tout.

**Le trou le plus silencieux de tout le chemin est ici** : si
`farc_index_par_nom_sinon_moins_un` rend -1 (nom absent de l'archive, ou
casse differente), `0x180044690` met quand meme l'etat a **2** avec un
pointeur de donnees **nul** et une taille **nulle** (`0x180215D70` borne et
rend 0). La scene est alors declaree prete, parse un tampon vide, et **ne joue
rien, sans un mot et sans bloquer les autres**. (Lu pour `0x180215E60`,
`0x180215D70` et l'enchainement ; **deduit** pour le comportement du parseur
sur un tampon vide — voir §4.)

### 1.5 Les deux ecritures de `[tache+0x68]` et `[tache+0x58]` — LE POINT 1

**`[tache+0x68]` (le tampon) et `[tache+0x60]` (la capacite) sont ecrits en un
seul endroit : le constructeur `TaskEffects_ctor_liste_a3d_16_entrees`,
`0x18006DB10`** (les instructions sont en `0x18006DB9B`..`0x18006DBD0`, la ou
la vtable `0x18034EAF0` est posee ; ce sont les **deux seules** references a
cette vtable dans tout le binaire). Lu :

```c
puVar1 = param_1 + 0x15;                 // la sous-tache Auth3D, a +0xA8
*puVar1 = TaskEffectAuth3D::vftable;     // 0x18034EAF0
param_1[0x20] = 0;                       // tache+0x58 : NOMBRE = 0
param_1[0x21] = 0x10;                    // tache+0x60 : CAPACITE = 16
param_1[0x22] = param_1 + 0x23;          // tache+0x68 : tampon = tache+0x70
__ehvec_ctor_iter(param_1 + 0x23, 4, 0x10, …);  // 16 elements de 4 octets
```

Le tampon est donc **interne a la tache** : seize `uint32` a `tache+0x70`. Le
destructeur `0x18006E5F0` les detruit (`+0x70`, 4, 0x10) et remet `+0x58 = 0`.

**`[tache+0x58]` (le nombre) et le contenu du tampon sont ecrits en un seul
endroit : `TaskEffectAuth3D_setStage_remplit_liste_scenes`, `0x1800706B0`.**
Lu, en entier :

```c
void setStage(tache, indice) {
  p = &table_a3d_par_decor;              // lea en 0x1800706BC -> 0x18034FD20
  k = 4;                                 // le premier indice de la table
  do {
    if (k == indice) {                   // trouve
      uids = *(int **)(p + 8);
      if (uids == 0) return;
      if (indice == 8)    tache[0xB1] = 1;
      if (indice == 0x28) tache[0xB0] = 1;
      for (u = *uids; u != -1 && tache[0x58] != tache[0x60]; u = *++uids) {
        h = a3d_scene_creer_depuis_uid(u);          // 0x18003C370
        if (a3d_poignee_scene_valide(&h)) {         // 0x180041A80
          a3d_scene_demander_chargement(&h);        // 0x180044830
          n = tache[0x58];
          if (n + 1 <= tache[0x60])                 // capacite 16
            { tache[0x58] = n + 1; tampon[n] = h; }
        }
      }
      return;
    }
    k = *(int *)(p + 0x10);              // l'indice de l'entree suivante
    p += 0x10;
  } while (k != -1);                     // terminateur
  return;                                // indice inconnu : RIEN, en silence
}
```

C'est **le seul endroit** ou un decor peut perdre ses scenes sans bruit : un
indice absent de la table sort par le `while (k != -1)` et ne laisse ni trace
ni compteur. `[tache+0x58]` reste 0.

### 1.6 Et ce que `0x180070340` en fait

Le creneau 1, `TaskEffectAuth3D_init_attend_toutes_les_scenes`, lu :

```c
for (p = liste; p != fin; p += 4)
    if (!a3d_scene_est_prete_etat2(p)) return 0;   // 0x180044640
for (p = liste; p != fin; p += 4) {                // on ne joue qu'ensuite
    uid = a3d_scene_uid_depuis_poignee(p);         // 0x180041440
    … cas particuliers 1256/1257, 2036, puis 1159 1160 1249 1256 2029 …
    configure (0x180046360, 0x1800463B0, 0x1800460D0) ;
}
if (tache[0xB0]) 0x180087550(0x19, …);
if (tache[0xB0] || tache[0xB1]) 0x180087550(2, …), 0x180087550(3, …);
return 1;
```

**C'est un tout-ou-rien.** Tant qu'**une seule** scene de la liste n'a pas
atteint l'etat 2, la fonction rend 0 et **aucune** des scenes du decor n'est
configuree ni jouee. Une liste vide (`[tache+0x58] == 0`) rend 1 tout de
suite, et il ne se passe rien.

---

## 2. CE QUI BORNE UN DECOR AJOUTE

### 2.1 La table des scenes par decor : `0x18034FD20`, 22 entrees, associative

Lue entierement (`read_bytes`, 432 octets). Enregistrements de `0x10` :
`{int indice, 4 octets de bourrage, pointeur vers une liste d'uid terminee
par -1}`, **terminateur `{-1, 0}`** a `0x18034FE60`. Apres lui, en
`0x18034FE70`, commencent des **flottants** (0,0 / 0,00390625 / 240,0 / 600,0
/ 1000,0 / 6000,0 / 46080,0).

Les 22 indices presents, **dans l'ordre du binaire** :

    4 5 6 11 7 13 19 12 14 10 17 20 8 16 18 9 15 22 23 25 39 40

* **Pas de tableau dense indexe par le decor** ici, **pas de borne a 41** :
  c'est une liste d'association terminee. Un indice inconnu — 41, 48, 6156 —
  ne lit rien hors table et ne plante pas. **Il ne fait rien, en silence.**
* Les 19 indices manquants parmi les 41 d'origine (0..3, 21, 24, 26..38) n'ont
  **aucune** scene d'effet `auth_3d`. C'est une donnee, pas un manque.
* `jin` est l'indice **9** (`decors.md` : « 8 `riv`, 9 `jin`, 10 `sin` »), et
  son entree est `0x18034FCC0` = **`[1942, 3348]`**. `1942` est
  `STGJIN_EFF_MOYA` (`brume_decor_aoi.md` §21.3). La brume de `jin` passe donc
  bien par cette table dans le jeu d'origine.
  *(Le « `jin` (35) » du §21.2 de cette note-la est l'**objset**, pas
  l'indice.)*
* Les listes d'uid occupent `0x18034FBA0`..`0x18034FD20` (384 octets, lus) ;
  la plus longue est celle de l'indice 19 : **sept** uid.

### 2.2 La capacite de la liste : SEIZE scenes par decor

`[tache+0x60] = 0x10`, pose par le constructeur (§1.5), et le `setStage`
compare `n + 1 <= capacite` **avant** d'ecrire. Au-dela de seize uid, les
suivants sont **crees et charges** (`0x18003C370` + `0x180044830` sont appeles
avant le test) mais **jamais inscrits dans la liste** : ils ne seront ni joues
ni liberes. Silence complet.

C'est une vraie borne pour un decor ajoute : `patch_moteur.py` reserve
`EFFETS_UIDS_MAX = 40` uid par entree neuve (une place de 40, terminateur
compris), soit **plus du double de ce que la tache peut tenir**. Aucun decor
du jeu d'origine n'en demande plus de sept, et aucun decor ajoute mesure ici
n'en demande plus de neuf (§3) : la borne n'a donc **pas encore mordu**, mais
rien ne l'empeche.

### 2.3 Le plafond global de scenes : QUATRE-VINGT-SEIZE

Trois fonctions independantes portent la meme constante `0x60`, lue :
`0x18003C370` (balayage de 96 creneaux de `0x2C8`), `0x180041A80` et
`0x180044640` / `0x180041440` (`(poignee & 0x7FFF) < 0x60`). Toutes les scenes
`auth_3d` du jeu — decor, personnages, interface — partagent ces 96 creneaux.
Au 97e, `0x18003C370` rend `0xFFFFFFFF` et la scene n'existe pas.

### 2.4 La table VOISINE, elle, est dense et SANS borne : `0x18034D570`

Ce n'est pas la table des scenes, mais elle est sur le chemin (c'est elle qui
decide quelles **taches** d'effet existent) et elle se comporte a l'inverse :

* `effets_decor_precharger_objsets_sans_borne` (`0x18006F620`) fait
  `piVar3 = &DAT_18034D570 + indice * 0x60` **sans aucune borne**, lit jusqu'a
  huit identifiants d'objset a `+0x00`, puis publie l'entree dans
  `DAT_180642FE8` ;
* `effets_decor_creer_les_taches` (`0x18006F380`) relit `+0x20` de cette
  entree : jusqu'a seize indices de taches d'effet, `-1` pour finir.
* **Mesure de l'etendue** : 41 entrees de `0x60` = `0xF60`, soit
  `0x18034D570 + 0xF60 = 0x18034E4D0` — qui est **exactement**
  `PTR_s_EFFECT_HIT_18034E4D0`, le tableau des 23 pointeurs vers les noms
  `EFFECT_*`. Rien ne separe les deux.
* Pour l'indice 48, l'entree tomberait en `0x18034E770` (lu) :
  `+0x00 = 0x005F27C0` — une moitie de pointeur, donnee a
  `0x1800F9C60` comme un identifiant d'objset — et `+0x20 = 0x19930522`, la
  constante magique de l'allocateur MSVC, donnee a `0x18006F380` comme un
  **indice de tache** puis utilisee en
  `*(longlong *)(&DAT_180677270 + 0x19930522 * 8)`. C'est le precedent
  `TaskEffectDown`/`TaskEffectMove` d'un cran au-dessus : pas un silence, une
  lecture sauvage.
* C'est pourquoi `patch_moteur.py` **doit** demenager cette table-la ; sans
  cela aucun decor ajoute ne demarrerait. Mesure, dans la DLL patchee du jour :
  elle est bien demenagee (§3).

### 2.5 Ce qui n'est PAS une borne

* **Aucun `41` / `0x29` sur le chemin `auth_3d`.** Recherche faite sur les six
  fonctions du chemin : les seules constantes de borne lues sont `0x10` (la
  capacite de la liste), `0x60` (les 96 creneaux), `8` et `0x10` (les listes de
  taches de `0x18006F380`), et des bornes **calculees** depuis la taille de la
  base (`/0x50`, `/0x88`, `/0xF0`).
* **Aucune chaine de comparaisons sur des indices de decor codes en dur** dans
  le chemin de creation. Les comparaisons d'indices de `0x1800706B0` portent
  sur `8` et `0x28` (deux drapeaux `+0xB0`/`+0xB1`) ; celles de `0x180070340`
  portent sur des **uid**, pas sur des indices de decor.
* Le nom de l'archive n'est jamais pris dans le binaire : il est compose depuis
  la base (§1.2). La liste de chaines minuscules `auth_3d/effstgare` …
  `auth_3d/effstgyuk` en `0x18054A910`..`0x18054B038` (relevee par
  `search_strings`) **n'a aucune reference de code** et ne contient pas
  `effstgjn5` ; ce qu'elle est exactement n'est pas etabli (§4).

---

## 3. LE CAS `jn5` (INDICE 48) : LA SCENE EST-ELLE CREEE ? — LE POINT 5

### 3.1 Dans l'image d'origine : perdue, et on sait a l'octet pres

L'indice 48 n'est pas dans les 22 entrees de `0x18034FD20` (§2.1). Le
`setStage` `0x1800706B0` parcourt la table, atteint le terminateur
`{-1, 0}` en `0x18034FE60`, et **sort**. `[tache+0x58]` reste 0, le tampon des
seize entrees reste vide, `0x180070340` rend 1 sans rien faire.
**`STGJN5_EFF_MOYA` n'est pas creee du tout** — ni `0x18003C370`, ni
`0x180044830` ne sont appeles pour l'uid 3532. L'octet qui en decide est le
`int` d'indice de la derniere entree de la table, `0xFFFFFFFF` en
`0x18034FE60`.

### 3.2 Dans la DLL patchee du jour : la scene EST dans la liste

**Lecture d'octets** de
`VF5RE/runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll` (2026-11-20,
7 181 824 o). Le site `lea` de `0x1800706BC` porte un deplacement de
`+14 974 832` : la table est demenagee en **`0x180EB8630`**, dans la section
`.decors` (`va=0x00EB1000`, `vsize=0x15000`). Elle compte **60 entrees** puis
le terminateur : les 22 d'origine (pointeurs inchanges vers `.rdata`) puis 38
entrees neuves, indices 42 a 77 et 83, 84, pointant dans `.decors`.

L'entree de l'indice **48** est la 29e, pointeur `0x180EBA250` :

    uids = [3533, 3534, 3535, 3537, 3532]

**`3532` = `STGJN5_EFF_MOYA` y est.** Cinq uid, donc sous la capacite de
seize. Le modele `jin` (9) n'en demandait que deux (`1942`, `3348`) : les trois
autres viennent du registre `ANIMATIONS_VALIDEES` de `patch_moteur.py`.

**Donc, pour le build du jour, la reponse au point 5 est : la scene n'est PAS
perdue dans `[tache+0x68]`.** Elle est creee, demandee, et inscrite. Le §21.5
point 1 de `brume_decor_aoi.md` est **referme : ce n'est pas la.**

### 3.3 Les deux endroits ou elle peut encore mourir, en aval et en silence

Ordre de probabilite decroissante, **deduits** du code lu, **non mesures** :

1. **Le tout-ou-rien de `0x180070340`** (§1.6). Les cinq uid de l'indice 48
   doivent **tous** atteindre l'etat 2. Si l'un de `3533`, `3534`, `3535`,
   `3537` ne l'atteint jamais — son `.a3da` manquant ferait au contraire
   passer l'etat a 2 (§1.4), mais une categorie qui ne se charge pas, elle,
   laisse l'etat a **1** indefiniment — alors **MOYA ne joue pas**, bien
   qu'elle soit parfaitement declaree. C'est le mecanisme le plus proche du
   symptome : « tout est declare, rien ne se voit ».
2. **Le `.a3da` resolu a vide** (§1.4). `farc_index_par_nom_sinon_moins_un`
   est **exact et sensible a la casse**. Le nom cherche est
   `<uid.3532.value sans "A ">` + `.a3da`, soit `STGJN5_EFF_MOYA.a3da`, et il
   doit figurer **tel quel** dans l'index de `EFFSTGJN5.farc`. Un ecart de
   casse, ou un index d'archive ou le nom est range autrement, rend -1 — et la
   scene est alors declaree prete avec un tampon **nul**, sans bloquer les
   autres. Silence parfait.

Ces deux-la se tranchent **sans course** : en relisant l'index de
`EFFSTGJN5.farc` octet pour octet (les cinq noms attendus, casse comprise) et
la categorie de chacun des cinq uid dans la base posee. C'est la mesure que
cette note recommande ensuite.

---

## 4. CE QUI N'EST PAS MESURE

* **Les noms n'ont pas ete poses** dans la base Ghidra : REA refuse la
  mutation sur cette cible (`Windows Ghidra P0 does not admit database
  mutation`). Rien n'a ete ecrit dans le binaire ni dans la base ; ce document
  est le seul porteur des noms proposes.
* **Le comportement du parseur de `.a3da` sur un tampon nul** (§1.4) :
  `0x180011630(rec+0x18, 0, 0)` n'a pas ete ouvert. « Il parse un tampon vide
  et ne lie rien » est une **deduction** du fait que `0x180215D70` rend 0 hors
  borne et que l'etat passe quand meme a 2. Il pourrait aussi dereferencer 0.
* **`0x180215F40`** (la taille d'un fichier de l'archive) n'a pas ete lue ; on
  suppose qu'elle est bornee comme `0x180215D70`.
* **Les trois autres creneaux de la vtable** (`0x18006FC30`, `0x180070250`,
  `0x180070790`, `0x1800708C0`, `0x180070850`) n'ont pas ete ouverts. L'un
  d'eux pourrait vider la liste ; **la recherche d'un autre ecrivain de
  `[tache+0x58]` n'a pas ete menee exhaustivement** — elle l'a ete sur les
  deux seules references a la vtable et sur le `setStage`, pas par balayage de
  toutes les ecritures a `+0x58`.
* **Qui pose l'indice du decor** dans le gestionnaire de taches d'effet
  (`[gestionnaire+0x00]`, lu par `0x18006F380` et transmis a `setStage`) n'a
  pas ete remonte. On suppose, **sans l'avoir lu**, que c'est le meme indice
  que celui du descripteur de decor ; le fait que l'entree 11 de
  `0x18034FD20` porte les uid de `STGDJO_*` et l'entree 9 ceux de `jin` le
  corrobore, mais ne le prouve pas.
* **La liste de chaines minuscules `0x18054A910`..`0x18054B038`** (`auth_3d/
  effstg*`, `auth_3d/nage_*`, `auth_3d/stg*`) : sans reference de code, nature
  inconnue — index d'archive embarquee, trace de construction, ou liste de
  prechargement d'un autre sous-systeme. Elle ne contient **pas** `effstgjn5`,
  ce qui serait inquietant si elle servait au chargement ; rien ne dit qu'elle
  serve.
* **L'etat reel des cinq scenes de l'indice 48 a l'execution** n'est pas
  mesure : c'est tout l'objet du §3.3. Et **c'est l'ecran qui tranchera**, pas
  cette note.
* Les 38 entrees neuves de la table demenagee ont ete **lues** (indices et
  uid) ; leur **justesse** (chaque uid appartenant bien a la categorie
  `EFFSTG<CODE>` du decor) n'a pas ete verifiee ici — c'est le §6 de
  `controle_decor_neuf.py` qui le fait.
