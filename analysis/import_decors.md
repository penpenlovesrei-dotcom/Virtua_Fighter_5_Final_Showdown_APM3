# Les decors de VF5 R sont-ils importables dans APM3 ?

Question du 2026-09-03. Reponse en trois parties : **le format, oui** ; **la
livraison, non — pas telle quelle** ; **le contenu, a verifier**.

> **REPONSE FINALE, 2026-09-07 : OUI.** Le decor DJO de VF5 R tourne dans APM3,
> vu a l'ecran. Il n'y a **aucun octet du moteur a changer** — les identifiants
> d'objets sont les memes dans les deux generations. Voir la section 8, qui
> corrige la section 7. Outil : `tools/importer_decor.py`, lanceur
> `tools/decor_5r_akira.cmd`, depistage `tools/depister_5r.cmd`.

---

## 1. Le format ne fait aucune difficulte

Compare sur `stgdjo.farc`, le plus gros ecart entre les deux versions.

### La preuve la plus forte : APM3 = Lindbergh, a l'octet pres

```
APM3_FS/rom/objset/stgdjo.farc      dd54b04f7d63011f6e64f6f450de1b91...
LIND_FS  (meme fichier)             dd54b04f7d63011f6e64f6f450de1b91...
VF5 R    (meme fichier)             a527b797f44694964da0df31ffc6085f...
```

Le fichier de la borne APM3 (Windows x64) est **identique au bit pres** a celui
du Lindbergh (Linux x86). Le format ne depend donc **ni du systeme ni de
l'architecture** : ces donnees traversent les plateformes sans conversion.
Confiance : **CONFIRMED**.

### Et il n'a pas change entre 2008 et 2010

| | VF5 R (2008) | Final Showdown (2010) |
|---|---|---|
| conteneur | `FArC`, en-tete 0x3A, alignement 1 | idem, **octet pour octet** |
| entrees | `stgdjo_obj.bin`, `stgdjo_tex.bin` | idem |
| geometrie, magie | `00 25 06 05`, en-tete 0x40 | idem |
| geometrie, objets | **119** | **171** |
| textures, magie | `TXP\x03` | idem |
| textures, nombre | 293 | 297 |
| textures, codecs | **176 x code 9, 116 x code 6** | **176 x code 9, 116 x code 6**, plus 3 x code 1 |
| textures, volume | **40,8 Mo** | 20,9 Mo |

La distribution des codecs est **la meme des deux cotes**, au nombre pres. Rien
a convertir, rien a reencoder.

Et l'ecart de volume s'explique enfin : ce n'est pas la geometrie qui a fondu —
elle a *grossi* (119 objets en 2008, 171 en 2010). Ce sont les **textures qui ont
ete divisees par deux** en passant a Final Showdown. C'est bien ce qu'on voit a
l'ecran : meme decor, aspect different.

Confiance : **SUPPORTED**.

---

## 2. Mais on ne peut pas simplement poser le fichier a cote

C'est la que la premiere tentative s'est cassee, et il a fallu arreter de
regarder l'ecran pour regarder le systeme.

### La mesure

`tools/tracer_fichiers.py` pose un point d'arret sur `KernelBase!CreateFileW` et
`CreateFileA` et journalise chaque chemin demande. Sur une partie complete, avec
un `stgdjo.farc` de VF5 R depose dans `vf5fs_media/rom/objset/` :

```
  4 x  ...\vf5fs_media\rom\sound\bgm\vfes_bgm_stg_hai.adx
  2 x  ...\vf5fs_data.par
  2 x  ...\vf5fs_media\w64\shader_pxd_w64.farc
```

**Le moteur n'a jamais tente d'ouvrir `rom/objset/stgdjo.farc` sur le disque.**
Le fichier depose n'a donc servi a rien, et aucune capture d'ecran ne pouvait le
dire : le selecteur de decor etant par defaut sur **Random**, on ne sait meme pas
quel decor s'etait charge. La bonne mesure n'etait pas a l'image, elle etait dans
les appels systeme.

### La regle, et elle est simple

En cherchant les noms dans l'archive :

| fichier | dans `vf5fs_data.par` ? | lu depuis |
|---|---|---|
| `stgdjo.farc` | **oui** (0x1A720) | l'archive |
| `stghai.farc` | **oui** (0x1AB60) | l'archive |
| `vfes_bgm_stg_hai.adx` | non | **le disque** |
| `shader_pxd_w64.farc` | non | **le disque** |
| `se_stage_are.csb` | non | **le disque** |

**Ce qui est dans le `.par` vient du `.par` ; ce qui n'y est pas retombe sur
l'arborescence libre `vf5fs_media/`.** Les sons et les films sont en fichiers
libres parce qu'ils ne sont pas dans l'archive — pas parce que le moteur
prefererait le disque.

Confiance : **CONFIRMED**.

### Les deux voies

1. **Neutraliser l'entree dans l'index du `.par`** — renommer `stgdjo.farc` en
   `stgdjo.far_` dans la table des noms. Le moteur ne le trouve plus, retombe sur
   le disque, et lit notre fichier. Quelques octets a changer, entierement
   reversible, sans reconstruire 4 Go.
2. Reconstruire le `.par` avec le nouveau fichier. Plus propre en sortie, mais il
   faut d'abord ecrire un ecrivain PARC.

La voie 1 est a essayer d'abord.

### PIEGE : le `.par` de notre atelier est un LIEN DUR vers le dump

```
2 liens  3987499008 octets  runtime/media/vf5fs/vf5fs_data.par
2 liens  3987499008 octets  .../VF5 FS DECOMP/APM3_US/.../vf5fs_data.par
                            ^ meme inode
```

**Ecrire dedans ecrirait dans le dump**, qui est en lecture seule par regle du
projet — et sans le moindre avertissement. Il faut donc **casser le lien par une
vraie copie** avant toute modification. C'est fait :
`runtime/media/vf5fs/vf5fs_data.par.copie`.

---

## 3. Ce qui reste incertain : le contenu, pas le format

Meme livre au bon endroit, un decor de 2008 peut etre refuse par un moteur de
2010 — non pour son format, mais pour ce qu'il contient :

- **le nombre d'objets differe** (119 contre 171). Tout ce qui designe un objet
  **par indice** doit venir de la meme generation : la collision
  (`STGDJO_COLI.000.bin`), l'animation (`auth_3d/STGDJO.farc`), les effets
  (`EFFSTGDJO.farc`), l'eclairage (`ibl/djo.ibl`, `light_param/*_djo.txt`).
  **Un decor s'importe en jeu complet, pas en un seul fichier.**
- **le volume de textures double** (40,8 Mo contre 20,9). Si l'allocation est
  dimensionnee sur le budget de Final Showdown, cela peut ne pas passer.
- les materiaux et les shaders ont pu changer entre les deux revisions ; le
  `shader_pxd_w64.farc` d'APM3 n'a pas d'equivalent Lindbergh.

## 4. La prochaine mesure

1. Sur la **copie** du `.par`, renommer l'entree `stgdjo.farc` dans l'index.
2. Deposer le jeu **complet** du decor DJO de VF5 R dans `vf5fs_media/rom/` :
   `objset/stgdjo.farc`, `auth_3d/STGDJO.farc`, `auth_3d/EFFSTGDJO.farc`,
   `STGDJO_COLI.000.bin`, `ibl/djo.ibl`, `light_param/{fog,glow,light,wind}_djo.txt`.
3. Relancer `tools/tracer_fichiers.py` pour **verifier que le moteur va bien
   chercher le fichier sur le disque** — la mesure, pas l'impression.
4. Seulement ensuite, regarder l'ecran — en **forcant le decor** au lieu de
   laisser le selecteur sur Random.

---

## 5. Lindbergh FS et APM3 FS : ce sont les MEMES fichiers

Question du 2026-09-03 : la qualite des textures des decors est-elle la meme
entre le Final Showdown Lindbergh et le Final Showdown APM3 ?

**Oui, et au sens le plus fort : ce sont les memes octets.**

### La geometrie et les textures

Les **41 archives `objset/stg*.farc`** existent des deux cotes, et **les 41 ont
exactement la meme taille** — pas un octet d'ecart, des `stgcid.farc` (743 o) aux
`stgban.farc` (28 186 804 o).

Trois verifiees a l'empreinte :

| decor | Lindbergh FS | APM3 FS | |
|---|---|---|---|
| `stgare` | `cac376953b9e1d9b2e15af9579586a92` | idem | **identique** |
| `stgtak` | `47320cb8ffd18a742566e4acc6f8076d` | idem | **identique** |
| `stgdjo` | `dd54b04f7d63011f6e64f6f450de1b91` | idem | **identique** |

### L'eclairage

Meme resultat sur les **206 fichiers** `ibl/*.ibl` et `light_param/*.txt` :
memes 206 des deux cotes, **toutes les tailles identiques**, aucun fichier
exclusif a l'une ou l'autre version.

Confiance : **CONFIRMED**.

### La nuance qui compte

Des donnees identiques ne garantissent pas une **image** identique. Le Lindbergh
rend sous Linux avec un GeForce 7 de 2006 ; APM3 rend en Direct3D 11. Le
`shader_pxd_w64.farc` n'a d'ailleurs **aucun equivalent Lindbergh** : le chemin
d'ombrage est du code different.

Ce qui peut donc differer a l'ecran, sans qu'un seul texel change : la resolution
de sortie, le filtrage anisotrope, l'anticrenelage, la precision des shaders.
**Les sources sont les memes ; le rendu peut ne pas l'etre.**

C'est aussi ce qui rend le chantier « resolution » interessant : a textures
egales, tout le gain visuel disponible est du cote du rendu.

---

## 6. Le repli sur le disque MARCHE -- mesure, pas impression

Suite du programme, 2026-09-03. `tools/par_masquer.py` change **un seul octet**
du nom dans l'index du `.par` : `stgdjo.farc` devient `stgdjo.far_`. L'outil
refuse d'ecrire si le fichier a plus d'un lien dur, pour ne pas toucher au dump.

Premier essai, un seul decor masque : **rien**. Le decor tire au sort n'etait pas
DJO -- le meme piege que la premiere fois. On masque donc **les 23 decors reels**
d'un coup, et la reponse arrive :

```
5497 x  ...\vf5fs_media\rom\objset\stgcas.farc
```

Cinq mille quatre cent quatre-vingt-dix-sept tentatives d'ouverture sur le
disque, pour un fichier absent. **Le moteur retombe bien sur l'arborescence
libre des qu'il ne trouve plus le nom dans l'archive.** Confiance : **CONFIRMED**.

On pose alors le `stgdjo.farc` de VF5 R **sous les 23 noms** (434 Mo), pour que
le tirage au sort ne puisse plus fausser la mesure :

```
2 x  ...\vf5fs_media\rom\objset\stgbar.farc
```

Deux ouvertures au lieu de 5497 : le fichier est **trouve et lu**, sans reessai.
Le conteneur et l'en-tete de 2008 sont donc acceptes par le moteur de 2010.

## 7. Mais le jeu ne finit pas de charger

Frederic, a l'ecran : « le jeu tourne en boucle sur l'ecran de loading ».

Le decor est donc **lu mais pas exploitable**. C'est exactement le risque annonce
en section 3 : le nombre d'objets differe (119 en 2008, 171 en 2010), et tout ce
qui designe un objet **par indice** vient d'ailleurs -- la collision
(`STGDJO_COLI.000.bin`), l'animation (`auth_3d/STGDJO.farc`), l'eclairage. Ici
l'`objset` venait de VF5 R et tout le reste de Final Showdown : le moteur cherche
des objets qui n'existent pas dans l'archive qu'on lui donne.

~~Note : VF5 R **n'a pas** de `auth_3d/STGDJO.farc` -- seulement
`EFFSTGDJO.farc`.~~ **FAUX, corrige le 2026-09-07** : il fait 37 811 octets et
porte les memes trois scenes `S010A010/020/030_DJO_STG_0*.a3da` que Final
Showdown. Le jeu complet du decor **est** transposable.

Etat remis a neuf : les 24 entrees rendues, les fichiers libres supprimes.

**Bilan.** Le mecanisme de livraison est acquis et mesure ; l'obstacle est le
**contenu**, comme annonce. La suite serait de comparer les listes d'objets des
deux `stgdjo_obj.bin` pour savoir si une correspondance est etablissable -- ou de
conclure que ces decors ne se transplantent pas sans leur generation entiere.

---

## 8. Et pourtant il s'importe : la mesure qui manquait (2026-09-07)

Les identifiants des cinq objets principaux de `djo` sont **les memes dans les
deux generations** -- `gnd` 114, `reflect` 115, `sdw` 116, `sky` 117,
`ring` 118 -- et le descripteur du moteur les demande deja tels quels
(`28:114 28:118 28:117 28:116 28:115`). Les 52 objets que Final Showdown a en
plus sont des effets, numerotes 0 a 113, absents du descripteur.

**Le binaire n'a donc rien a changer.** L'obstacle de la section 7 n'etait ni le
format ni les identifiants : c'etait le MELANGE -- objset de R, auth_3d, effets
et collision de Final Showdown. Un decor s'importe avec sa generation ENTIERE,
et l'outil `tools/importer_decor.py` refuse desormais un jeu incomplet.

`tools/par_masquer.py` a ete borne au pot de noms de l'en-tete PARC
(`0x20` .. `min(+0x14, +0x1C)`). Sans cette borne il masquait aussi les
occurrences situees dans les DONNEES archivees -- `STGDJO_COLI.000.bin` en a
deux vers `0xEDD000`.


---

## 9. Deux options ajoutées le 2026-09-08 — et ce qu'elles valent

### `--vers <code>` : poser un décor sous le code d'un AUTRE emplacement

    py -3 tools/importer_decor.py --poser djo --source VF5R --vers evo00

Les neuf pièces sont copiées sous le code de l'emplacement. Le point qui ne se
devine pas : **`obj_db.bin` cherche les deux entrées internes de l'archive sous
le nom de l'emplacement** (id 51 → `stgevo00_obj.bin`, `stgevo00_tex.bin`).
Elles sont donc réécrites **dans l'en-tête du `FArC` uniquement** — l'en-tête
porte sa longueur en gros-boutien en `+0x04` (0x3A pour `stgdjo.farc`) — parce
que la même chaîne réapparaît à `0x4C` dans le flux de données, et l'y écraser
corromprait l'archive.

**Éprouvé, jamais validé à l'écran** : l'essai a été fait sur `trm`, qui n'était
pas un emplacement libre, et tout a été défait. Voir `analysis/decors.md` §13.

### `--eclairage <source>` : l'éclairage d'une autre génération

    py -3 tools/importer_decor.py --poser djo --source VF5R --vers evo00 \
        --eclairage VF5FS_LIND

Écrite pour une **fausse piste** : j'avais accusé les réglages de VF5 R (glow
`exposure` 2.8 contre 2.0 en Final Showdown) d'une image ratée. Frédéric l'a
réfuté en reposant le même décor avec les mêmes fichiers sur `djo` — couleurs
correctes. **L'option n'est utilisée par aucun lanceur.** Elle reste parce que
la question se reposera pour une génération plus lointaine.

Ne pas confondre avec `--sans-eclairage`, qui ne pose rien : sur un emplacement
recyclé, cela laisserait l'éclairage du décor d'essai.

---

## 10. AJOUTER le dojo de VF5 R au lieu de le substituer (2026-09-09)

C'est la demande de Frédéric : « je veux ajouter proprement le décor VF5R
d'Akira ». Le lanceur qui existait, `decor_5r_akira.cmd`, **remplace** : il pose
les fichiers de 2008 sous le code `djo`, et le dojo de Final Showdown disparaît
tant qu'il est en place. La règle du chantier dit l'inverse — *on ajoute, on ne
remplace pas*.

Le build à part : **`tools/decor_5r_akira_ajout.cmd`**, et son défaiseur
**`tools/decor_5r_akira_ajout_retirer.cmd`**.

### 10.1 L'emplacement : `trs`, et il ne s'est pas choisi à l'estime

`tools/emplacements.py` en mesure quinze de libres. Deux critères les réduisent
à un :

* **trois lettres**, obligatoirement. `importer_decor.py --vers` réécrit les
  deux noms internes de l'archive (`stgdjo_obj.bin` → `stgtrs_obj.bin`) par
  substitution **en place** : `stgevo00_obj.bin` ne tient pas dans la place de
  `stgdjo_obj.bin`. Restent `tst ts3 wht cid trs`.
* le descripteur doit porter la **forme** d'un décor d'essai intact — deux
  objets de son propre objset, trois `-1`. C'est la garde qui a manqué à `trm`.

`trs` : indice 28, objset 44, descripteur `0x180404E70`. Mesure faite au
passage, et elle vaut pour la suite : **les six emplacements candidats portent
exactement les mêmes sept relocations** (`0x00 0x08 0x48 0x50 0x58 0x60 0x68`)
là où `djo` en a dix-sept. La liste des dix pointeurs à remettre à zéro n'est
donc pas propre à `trm` — elle vaut pour n'importe quel emplacement d'essai.

### 10.2 Ce que `--variantes-djo` était, et pourquoi il n'avait jamais marché

L'option existait depuis le 2026-09-08. Elle était **cassée en deux endroits**,
et personne ne l'a vu parce qu'elle n'a pas été relancée depuis :

| | |
|---|---|
| `VARIANTES_ANNEAU_DJO = ([11, 26], …)` | **26, c'est `trm`** — la barre espace aurait fait défiler vers le décor TERMINAL |
| `VARIANTES_TRM_INDEX = 29` | le clonage du descripteur visait `evo00`, **cinq lettres** : `importer_decor.py --vers` ne pouvait pas y renommer l'archive |

Autrement dit le correctif **posait le décor à un endroit et faisait défiler
vers un autre**. La leçon est celle du 2026-09-08 déjà écrite autrement : une
donnée dupliquée dans deux constantes finit par diverger. L'emplacement est
donc devenu un **argument**, `--variantes-djo <code>`, et l'indice, l'objset,
la chaîne de collision et l'anneau en sont tous **dérivés**.

### 10.3 Le garde-fou se mordait la queue

`emplacements.py` déclare pris tout code qu'un de nos `.cmd` nomme (preuve 4 —
c'est elle qui manquait le jour où `trm` a été cassé). Dès que
`decor_5r_akira_ajout.cmd` écrit `--vers trs`, `trs` devient « utilisé par
decor_5r_akira_ajout.cmd »… et `importer_decor.py --vers trs` le refuse, **y
compris à ce lanceur-là**. Le lanceur ne pouvait pas poser son propre décor.

Deux ajouts, et la garde reste entière :

* `emplacements.py --pourquoi <code>` rend les raisons **étiquetées**, une par
  ligne : `descripteur`, `grille`, `apercu` (le moteur s'en sert) contre
  `lanceur <nom>` (une simple réservation) ;
* `importer_decor.py --pour <lanceur.cmd>` lève la réservation **à la seule
  condition** que toutes les raisons soient des citations, et que les lanceurs
  qui citent soient celui-là et ses compagnons (`<souche>*.cmd`). Une raison de
  moteur ne se lève pas : seul `--forcer` passe outre.

### 10.4 Ce que le build touche, et ce qu'il ne touche pas

Côté **fichiers** — les neuf pièces de VF5 R posées sous le code `trs` dans
`vf5fs_media/rom/`, et les cinq noms qui existaient dans l'index du `.par`
masqués (`stgtrs.farc`, `trs.ibl`, `light/fog/glow/wind_trs.txt`). Les quatre
autres (`STGTRS_COLI.000.bin`, `STGTRS.farc`, `EFFSTGTRS.farc`) **n'existent
pas dans le `.par`** : le fichier libre est lu directement.

Côté **moteur** — le descripteur de `trs` reçoit un **clone complet** de celui
de `djo` (les quinze champs : `+0x2C..+0x34`, `+0xB8`, `+0xD0`, `+0xD4`, l'aire
12×12), et ne garde en propre que l'objset 44, les cinq objets `44:114 118 117
116 115` et la collision, écrite dans le mou de `.rdata` en `0x180641B80`.
`djo` n'est **pas touché** : les deux générations coexistent.

Côté **retour en arrière** — le binaire revient tout seul, `patch_moteur.py`
repartant toujours de `.origine`. Seuls les fichiers persistent, et
`decor_5r_akira_ajout_retirer.cmd` les rend.

### 10.5 État

Contrôle avant vol **passé** : les neuf fichiers posés, les noms masqués, et
les cinq objets que le descripteur demande présents dans l'objset posé
(`stgdjo_gnd`, `stgdjo_ring`, `stgdjo_sky`, `stgdjo_sdw`, `stgdjo_reflect`).
Le jeu **démarre et atteint l'écran-titre** (`analysis/ajout_5r_titre.png`).

**Pas encore vu à l'écran** : la bascule elle-même. STAGE SELECT, case du DOJO,
barre espace → `VIRTUA FIGHTER 5 FS` / `VIRTUA FIGHTER 5 R`.
