# Dural est-il jouable dans le build arcade ?

Question posée le 2026-09-02. Dural est déblocable sur la version PS3 ; l'écran de sélection
du build arcade APM3 ne le propose pas. Ce document sépare ce qui est **mesuré** de ce qui
resterait à démontrer.

---

## 1. Les données sont complètes

Dural n'est pas un boss bricolé : il a **tout ce qu'a un personnage jouable**.

| | Dural | les 19 autres |
|---|---:|---|
| `ctrl_DUR.bin` (table de commandes) | **37 668 o** | 46 320 à 121 640 o |
| `mothead_DUR.bin` (mouvements) | **101 208 o** | 106 476 à 252 196 o |
| entrée dans `rob_cmn_mottbl` | **index 20, 2 postures** | 1 à 7 postures |
| rôles logiques pourvus | **726 / 726** | 363/363 à 2541/2541 |
| `mot_DUR.farc`, `mot_AUTH_DUR.farc` | présents | présents |
| `dur_itm.csv` (personnalisation) | **4 articles** (les finitions de corps) | 639 à 915 articles (vêtements) |
| `spr_t_itmdur.farc` (icônes du terminal) | **absent** | présent pour les 19 |

Deux lectures s'imposent :

- **Côté combat, il est entier.** Il y a exactement **20 fichiers `ctrl_*.bin`**, un par
  personnage, Dural compris — c'est la table qui traduit les entrées en mouvements. Et ses
  **726 rôles sur 726 sont pourvus** : le moteur peut résoudre chacune de ses animations
  logiques par `GetMotionForRole(20, posture, rôle)`. Il passe aussi les deux contrôles du
  chantier, `mothead` conforme et identifiants d'animation valides.
- **Côté habillage, il a exactement ce qu'il lui faut.** J'avais d'abord lu « 5 lignes contre
  640 à 916 » comme un vide. C'est faux : `dur_itm.csv` porte **quatre articles**, et ce sont
  les quatre finitions de corps de Dural — 鏡面反射体（銀）, 鏡面反射体（金）, ガラス, 石膏,
  soit argent, or, verre et plâtre. Toutes en `Type = REPLACE` avec un `Kisekae` couvrant
  **le corps entier** (ATAMA MUNE SENAKA HARA KOSI KATA_L/R UDE_L/R TE_L/R MOMO SUNE ASI),
  sur les dix emplacements de costume `1P` à `10P`. Dural n'a pas de garde-robe parce qu'il
  ne porte pas de vêtements : il a des matières. La donnée est complète et cohérente.

  Ce qui manque, en revanche, est ailleurs : **`spr_t_itmdur.farc` n'existe pas**. Les
  dix-neuf autres personnages ont leur planche d'icônes d'articles pour le terminal ; Dural
  non — ni dans le dump APM3, ni dans R.E.V.O. C'est une absence d'**interface**, pas de
  contenu. Voir `analysis/parente_console.md`.

Confiance : **CONFIRMED** (mesuré sur les fichiers du dump arcade 6.000).

---

## 2. `UNLOCK_DURAL` existe, mais ce n'est pas une porte

Le moteur porte la chaîne **`UNLOCK_DURAL`** (`0x180532CC8`), référencée une seule fois, en
`0x1801E349E` :

```
cmp byte ptr [rbx + 0x30e], dil
je  (sauter)
lea rdx, "UNLOCK_DURAL"
call 0x180245830
```

Or `0x180245830` ne fait que transmettre à `0x1802456C0` avec un mode `2` : c'est un
**lecteur de scène nommée**, comme pour `p_txt_01_lt` ou `neu_s` juste avant. `UNLOCK_DURAL`
est donc un **nom d'animation d'interface** — l'écran qu'on affiche quand Dural est débloqué —
et non un drapeau de déblocage.

Le voisinage le confirme : la chaîne est rangée entre `MAIN MENU`, `ARCADE MENU`,
`VERSUS MENU`, `SCOREATTACK MENU`, `LICENCECHALLENGE MENU` et `p_menutxt_PS3_lt` — **le menu
de la version console**. Le moteur est partagé entre les deux, et ces chaînes sont des restes
du build PS3, où le déblocage existe.

Autre indice dans la même fonction : le prédicat `0x180007450` qu'elle consulte **rend
toujours zéro** — c'est un stub dans ce build.

Confiance : **SUPPORTED**.

---

## 3. Le moteur accepte l'indice 20

C'est le resultat le plus fort de la journee, et il est **statique** : le moteur
n'a aucune borne qui exclue Dural.

L'accesseur qui traduit un indice de personnage en donnees est **`0x18012CA90`** :

```
0x18012CA90  cmp   ecx, 0x15          ; borne = 21
0x18012CA93  jae   echec              ; hors borne -> rend 0
0x18012CA95  movsxd rax, ecx
0x18012CA98  lea   rcx, [0x1803E79E0] ; table de 21 entrees, pas de 48 octets
0x18012CA9F  lea   rax, [rax+rax*2]
0x18012CAA3  add   rax, rax           ; rax = indice * 6
0x18012CAA6  mov   rax, [rcx+rax*8]   ; ... * 8 = pas de 48
```

La borne est **`0x15` = 21**, donc les indices **0 a 20 sont valides**, et la
table qu'elle indexe se lit en clair :

| indice | code | nom affiche |
|---:|---|---|
| 0 … 18 | AKI … TAK | Akira Yuki … Taka-Arashi |
| 19 | `TE2` | *(vide)* |
| **20** | **`DUR`** | **`DURAL`** |

Deux accesseurs jumeaux, `0x18012CAB0` et `0x18012CAE0` (celui-ci va chercher le
nom localise, identifiant `indice + 0x110`), portent **la meme borne `0x15`**.

Autrement dit : **Dural n'est pas exclu par le code, il est simplement absent de
la grille de selection.** L'indice 19 est un emplacement d'essai vide, ce qui
explique pourquoi la grille montre 19 combattants et pourquoi Dural porte 20.

Confiance : **CONFIRMED** (lu dans le binaire APM3).

### Ou le chargeur lit l'indice

Le chemin complet du nom de fichier, trouve par les references a `mot_%s.bin` :

```
0x180151F5E  mov  rax, [rdi+0x60]     ; l'objet joueur 1
0x180151F62  mov  ecx, [rax+0x10]     ; l'indice de personnage
0x180151F65  call 0x18012CA90         ; -> "LIO"
0x180151F6D  lea  r8, "mot_%s.bin"
```

Le joueur 2 a sa fonction jumelle en `0x18015209B`, avec `[rdi+0x68]`. C'est la
confirmation que **`ROB+0x10` est bien l'indice de personnage** et qu'il sert a
batir les noms de fichiers.

---

## 4. La substitution a l'execution n'a pas encore eu lieu

Un premier essai (`tools/forcer_dural.py`) pose un point d'arret sur
`0x180151F5E` et y ecrit 20 dans `joueur+0x10`. Resultat honnête :

```
BP chargement : 0 passage(s)
substitutions : 0
```

Le point d'arret **n'a jamais ete frappe** : Akira contre Lion, comme sans lui
(`analysis/dural_01..03.png`). Ce n'est donc pas « Dural a echoue » — c'est
« l'essai n'a pas eu lieu ». Deux causes possibles, non departagees :

- le point d'arret est pose a **t = 20 s**, alors que ce chargeur-la tourne peut-etre
  plus tot, ou dans une autre branche du dispatch (`0x180151ED9` est un
  saut par table : la fonction est un automate, et l'etat 1 n'est pas force emprunte) ;
- le chargement des mouvements passe par la fonction jumelle, ou par un troisieme
  site.

La prochaine mesure est simple : poser le point d'arret **des le chargement du
moteur**, sur les quatre sites de `mot_%s.bin` a la fois, et compter les passages
avant de chercher a ecrire quoi que ce soit.

---

## 5. Ce qui reste ouvert

- **La grille de selection** : toujours pas trouvee. Ni l'ordre affiche ni la
  table qui le porte ne se retrouvent dans les binaires, en octets comme en `u32`.
- **Le global du choix** : cherche par balayage memoire des deux binaires
  (31 Mo d'images, 260 Mo avec le tas) -- **zero adresse en zone d'image**. Le
  choix vit donc sur le TAS, dont les adresses ne survivent pas d'une execution
  a l'autre : la comparaison a deux passes doit se faire **dans une seule
  execution**, entre deux combats successifs.
- **La question de fond reste ouverte** : que le moteur accepte l'indice 20 ne
  dit pas qu'il sache jouer Dural. Ses fichiers sont complets cote combat
  (726/726 roles) mais vides cote personnalisation (5 lignes d'items) : un
  chargement de costume pourrait echouer la ou celui d'un personnage normal
  reussit.

---

## 6. La piste Xbox 360 (2026-09-03)

Question de Frederic : la version X360, ou Dural **est** deblocable, aiderait-elle,
son code etant plus proche du PC que celui de la PS3 ?

**La premisse architecturale est fausse.** La Xbox 360 tourne sur un **Xenon,
PowerPC gros-boutiste** ; la PS3 sur un Cell dont le PPU est lui aussi du
PowerPC. Les deux sont exactement aussi loin du x86-64 d'APM3. Aucun code ne se
transporte, ni de l'une ni de l'autre.

**Mais l'intuition pratique est juste**, pour une autre raison : la X360 est
bien plus **accessible** que la PS3.

| | PS3 | Xbox 360 |
|---|---|---|
| conteneur | `.pkg` chiffre, `EBOOT.BIN` en SCE/SELF | paquet STFS `LIVE`, 2,05 Go |
| donnees | non extraites (46 fichiers `mot_*.farc`) | **en clair dans le paquet** |
| executable | entropie **8,000**, zero chaine lisible | `XEX2` a `0xD7A000`, chiffrement de detail dont la cle est publique |

Verifie directement dans le paquet de 2 Go, sans rien extraire : on y lit
`default.xex`, `stgdjo.farc`, `mothead_DUR`, `ctrl_DUR`, `chritm_tbl`,
`spr_t_itmaki`... Les noms de fichiers sont accessibles tels quels.

### Ce que cette verification a deja donne gratuitement

**`spr_t_itmdur` est ABSENT de la Xbox 360 aussi**, alors que `spr_t_itmaki` y
est. Or c'est la version ou Dural se debloque.

Donc l'absence de planche d'icones d'articles pour Dural **n'est pas une coupe
de la version arcade** : il n'en a nulle part. C'est normal -- ses quatre
articles sont des finitions de corps, pas des vetements, et il n'a pas de grille
d'articles a montrer.

**Un des deux « manques d'interface » identifies pour Dural n'en est donc pas
un.** Il n'en reste qu'un seul : la case dans la grille de selection.

Confiance : **CONFIRMED**.

### Ce qu'il faudrait pour aller plus loin

Le reste est dans le `default.xex`, qui est compresse : `UNLOCK_DURAL`,
`ARCADE MENU`, `mot_%s.bin` n'apparaissent pas en clair. Il faudrait ecrire un
lecteur XEX -- dechiffrement par la cle de detail, puis decompression -- et
desassembler du PowerPC gros-boutiste. Faisable sans rien telecharger, mais
c'est un detour.

Ce qu'on y trouverait n'est pas du code a copier, mais **la logique de la grille
de selection lue comme une donnee**, dans un build ou Dural fonctionne.

---

## 7. L'entonnoir trouve : `CodeDuPersonnage` (2026-09-03)

Apres deux impasses -- le point d'arret materiel sur `ROB+0x10` (zero acces) et
le site `0x180151F5E` (zero passage, branche non empruntee) -- le bon angle
etait l'**entonnoir** : `CodeDuPersonnage` (`0x18012CA90`), par laquelle passe
toute traduction d'un indice en code a trois lettres.

`tools/pister_perso.py`. Mesure sur une partie complete :

```
CodeDuPersonnage : 494 passages
  indice 0 (AKI) et 8 (LIO) -- les deux personnages choisis
  trois sites d'appel :  moteur+0x14F5CA
                         moteur+0x62BF2
                         moteur+0x14FAEE
```

**Trois sites, et trois seulement.** C'est le point de passage oblige qu'on
cherchait depuis le matin.

### La substitution fonctionne

`--forcer 20 --depuis 0` remplace l'indice du joueur 1 par celui de Dural aux
trois sites, en laissant le joueur 2 intact :

```
CodeDuPersonnage(0 = AKI)  depuis moteur+0x14F5CA   >>> force a 20 (DUR)
CodeDuPersonnage(0 = AKI)  depuis moteur+0x62BF2    >>> force a 20 (DUR)
CodeDuPersonnage(0 = AKI)  depuis moteur+0x14FAEE   >>> force a 20 (DUR)
CodeDuPersonnage(14 = GOH) depuis ...               (non force)
```

Le combat tourne -- **192 passages de `MothApplyRecord`**, aucune exception. Le
moteur accepte donc de batir les noms de fichiers de Dural et de continuer.

`ROB+0x10` vaut toujours 0 : seul le **code** est substitue, pas l'indice du
combattant. C'est volontaire pour ce premier essai -- on separe les deux effets.

Captures soumises : `analysis/dur_essai_a.png`, `dur_essai_b.png`.

### Piege de methode, note pour ne pas le refaire

Trois executions ont ete perdues a croire l'outil muet : `pister_perso.py`
ecrit ses relevés dans **`analysis/pister_perso.txt`**, pas sur la console. La
sortie standard ne portait que l'en-tete du resume. Lire le journal.

---

## 8. DURAL EST CHARGE (2026-09-03)

Frederic, a l'ecran : « **dural est bien chargee** mais elle est completement
buggee et clignote ».

C'est le resultat que ce chantier cherchait depuis le matin. Le moteur APM3
**accepte de charger Dural** et continue a tourner.

### Ce qui a marche : la source, pas le champ

Deux impasses avaient precede, et elles s'expliquent maintenant :

| tentative | resultat | pourquoi |
|---|---|---|
| point d'arret materiel en ecriture sur `ROB+0x10` | 0 acces en 245 s | on surveillait **l'aboutissement**, ecrit avant que l'adresse existe |
| forcer `CodeDuPersonnage` (le code a 3 lettres) | pas de Dural | on changeait **le nom des fichiers**, pas le personnage |
| **ecrire dans `[rbx-0x10C]` au site `moteur+0x14F5C5`** | **Dural charge** | c'est **la source** : la structure de selection, en amont du ROB |

Le site :

```
moteur+0x14F5B3   mov ecx, dword ptr [rbx - 0x10c]   ; l'indice de personnage
moteur+0x14F5B9   cmp ecx, 0x15                      ; 21 = hors borne = pas de perso
moteur+0x14F5BC   je  (sauter)
moteur+0x14F5C5   call CodeDuPersonnage
```

Il passe **exactement deux fois**, une par joueur, au chargement du combat. Et
l'adresse `rbx-0x10C` est dans une plage **etrangere aux ROB** :

```
[rbx-0x10C] = 0x207672CB6FC  vaut 0   (AKI)     ROB 1 = 0x20762FD04D0
[rbx-0x10C] = 0x207672CB8C4  vaut 13  (BRA)     ROB 2 = 0x20762FD6238
```

`tools/pister_perso.py --forcer 20 --depuis 0` y ecrit l'indice de Dural.

### L'etat actuel : charge, mais incoherent

Trois reglages ont ete essayes, et l'activite du moteur les distingue nettement :

| reglage | `MothApplyRecord` | `SourceIndice` |
|---|---:|---:|
| aucun (temoin) | 116 | 2 |
| selection seule | 563 | 52 |
| selection **+** `ROB+0x10` (`--rob`) | **2299** | 55 |

Le bond du nombre de passages dit que le moteur travaille beaucoup plus --
compatible avec une resolution d'animations qui echoue et recommence.

**L'hypothese de travail** pour le clignotement : le modele est celui de Dural
mais quelque chose d'autre reste sur le personnage d'origine. `--rob` corrige
`ROB+0x10`, mais il reste au moins un troisieme endroit -- les tables de
mouvements sont chargees **avant** que le ROB existe, donc `mot_AKI.farc` a pu
etre charge la ou il faudrait `mot_DUR.farc`.

### La suite

Chercher ce qui, entre `[rbx-0x10C]` et le ROB, garde encore l'ancien indice.
Le chemin de chargement `mot_%s.bin` (`moteur+0x151F5E` et ses trois freres) est
le premier endroit ou regarder : il lit `[joueur+0x10]`, et ce `joueur` n'est
peut-etre pas le meme objet que celui de `rbx-0x10C`.

---

## 9. Le mecanisme est bon ; c'est Dural qui bloque

### Le temoin qui tranche

Meme manipulation, mais forcee sur **TAK (18)**, un personnage normalement
selectionnable :

| forcage | etat de mouvement du ROB 1 | changements |
|---|---|---:|
| aucun (temoin) | 0x1C, 0x41C7, 0x530, 0x8E2, 0xC43, 0xC57, 0xAD8 … | nombreux |
| **TAK (18)** | 0x36E2, 0xE1F, 0x4BA9, 0x4344, 0xC56, 0x43E5 … | **14** |
| **DUR (20)** | **0x510B, et plus rien** | **2** |

**La methode marche.** Forcer un personnage normal donne un combattant vivant.
Dural, lui, se fige sur un unique etat de mouvement -- ce que Frederic voit
comme « Dural qui reste couchee au sol ».

Confiance : **CONFIRMED**.

### Ce qui a ete elimine

- **les donnees ne manquent pas** : `mot_DUR.farc`, `mot_AUTH_DUR.farc`,
  `mothead_DUR.bin` et `ctrl_DUR.bin` sont **tous dans le `.par`**, comme ceux
  d'AKI, TAK et BRA ;
- **le moteur demande bien Dural** : les quatre sites d'appel de
  `CodeDuPersonnage` recoivent 20, y compris `moteur+0x62BF2`, celui qui
  alimente la liste de chargement ;
- **le ROB est coherent** : `--rob` met `ROB+0x10` a 20, la posture reste 0
  comme pour les autres.

### Une piste ecartee tout de suite

`moteur+0x180062B64` porte un `cmp edx, 0x13` suivi d'un `cmove edi, r14d` :
**si l'indice vaut 19, il est remplace par 0**. C'est le garde-fou de
l'emplacement mort `TE2`, pas une porte contre Dural. Aucune comparaison a 0x14
(20) n'existe dans les quatre zones qui manipulent le personnage.

### Ce que dit l'indication de Frederic

Sur PS3, Dural se debloque en **terminant le mode Arcade**. Cela oriente vers un
**drapeau de profil**, et non vers une donnee manquante -- ce qui colle avec ce
qu'on mesure. Rappel du garde trouve en `0x1801E349E` : il consulte
`0x180007450`, qui est `xor al, al ; ret` -- **toujours zero** dans ce build.
Si un drapeau equivalent conditionne aussi la *mise en route* de Dural et pas
seulement son affichage dans la grille, c'est lui qu'il faut trouver.

### La prochaine mesure

Comprendre **0x510B** : pourquoi cet etat de mouvement ne s'enchaine pas.
Comparer ce que `GetMotionForRole(20, 0, role_de_repos)` rend, contre
`GetMotionForRole(18, 0, meme_role)` qui fonctionne. Les 71 sites d'appel sont
deja repertories ; il suffit d'en instrumenter un.

---

## 10. La Xbox 360 n'apporte rien pour Dural (2026-09-03)

Verification faite directement dans le paquet STFS, sans rien extraire.

**Les planches d'interface de Dural sont deja dans APM3.** Les listes sont
identiques des deux cotes :

```
aet_c_mchaki .. aet_c_mchwol   dont aet_c_mchdur     (20 des deux cotes)
spr_c_mchaki .. spr_c_mchwol   dont spr_c_mchdur     (20 des deux cotes)
```

Dural a donc **sa planche de selection/combat** dans le build arcade, comme les
dix-neuf autres. Rien a importer.

Rappel du seul manque cote interface : `spr_t_itmdur` -- **absent du X360
aussi**, alors que c'est la version ou Dural se debloque. Ce n'est donc pas une
coupe : il n'a simplement pas de grille d'articles, ses quatre articles etant des
finitions de corps.

**Conclusion : cote donnees, Dural est complet dans APM3, interface comprise.**
Le blocage est ailleurs -- dans ce qui empeche son etat de mouvement `0x510B`
de s'enchainer.

---

## 11. `0x510B` est le REPOS de Dural (2026-09-04)

La « prochaine mesure » du paragraphe 9 est faite, et **sans lancer le jeu** :
l'oracle a deja etabli que `tools/motdb.py` rend exactement ce que rend
`GetMotionForRole` du moteur (14157/14157). Le calcul est donc statique.

```
0x510B  ->  mot_db : ('DUR', 'DUR_L_IDLE_TA')
            rob_cmn_mottbl : entree 20, posture 0, ROLE 0
```

| | TAK (18) | DUR (20) |
|---|---|---|
| role 0, posture 0 | `0x36E2` | `0x510B` |
| premier etat releve en jeu | `0x36E2` | `0x510B` |
| roles resolus dans `mot_db` | 349 / 363 | **356 / 363** |
| roles a zero | 0 | 0 |
| postures | 1 | 2 |
| jeux d animation | CMN 183, TAK 166 | CMN 247, DUR 109 |

**Les deux combattants demarrent sur leur repos, correctement resolu.** Dural
est meme mieux pourvue que Taka-Arashi. Ni la donnee ni `GetMotionForRole` ne
sont en cause.

La question change donc de forme : ce n'est pas « pourquoi Dural est-elle gelee
sur un etat casse », c'est **« pourquoi ne quitte-t-elle jamais son repos »**,
la ou TAK force par la meme methode enchaine 14 etats.

Confiance : **CONFIRMED** (lu dans `rob_cmn_mottbl.bin` et `mot_db.bin` du dump
APM3 6.000, par la methode que le moteur lui-meme a validee).

### Ce que `is_dural_unlocked` ne fait pas

Le drapeau trouve le 2026-09-03 dans le `vf5fs_game_config_t` (quartet haut de
`config+7`, global derive `0x180C3B700`) a ete pose puis mesure :

```
py -3 tools/patch_moteur.py --dural
py -3 tools/pister_perso.py --forcer 20 --depuis 0 --rob --etat
   ->  ROB1  perso DUR  posture 0  etat 0x510B     et plus rien
```

**Aucun changement.** C'est coherent avec la lecture statique : les cinq sites
qui lisent `0x180C3B700` (`0x1801D081D`, `0x1801DDD4F`, `0x1801E348E`,
`0x1801E490F`) sont tous dans le code d'interface console. Le drapeau ouvre la
grille de selection ; il ne touche pas au chemin de combat.

### La piste a ouvrir

Dural est l'indice **20**, le dernier. L'accesseur `0x18012CA90` est borne par
`cmp ecx, 0x15` (21) et l'accepte. Mais rien ne dit que **toutes** les tables
indexees par le personnage aient 21 entrees : une table de 20 laisserait Dural
lire hors borne ou rendre zero, et un enchainement d'animations qui ne trouve
pas sa suite reste sur place -- exactement ce qu'on observe.

Prochaine mesure proposee : chercher dans le moteur les gardes `cmp <reg>, 0x14`
(20) et `cmp <reg>, 0x13` (19) suivies d'un `jae`/`ja` et d'un `lea` de table,
au voisinage des sites qui manipulent l'indice de personnage. Une borne a 20 la
ou l'accesseur en admet 21, c'est la coupe qu'on cherche.

---

## 12. La machinerie de roles tourne aussi pour Dural (2026-09-04)

Mesure differentielle, meme dispositif, meme scenario, point d'arret sur
`GetMotionForRole` APM3 (`0x18015B310`), 125 s chacune.

| role demande | TAK (18) force | DUR (20) force |
|---:|---:|---:|
| 60, 63, 64, 65, 70, 71 | 2337 chacun | 1097 chacun |
| 361 | 784 | 367 |
| 205 / 206 | 71 | 4 |
| 211 / 212 | 16 | 1 |
| 72 / 73 | 83 / 5 | 5 / 5 |
| 0 | -- | 1112 |
| 3 | -- | 1097 |

**Dural sollicite exactement la meme famille de roles que le temoin.** La
resolution tourne pour elle, a la meme cadence par trame. Ce n'est donc ni la
donnee (356/363 roles pourvus), ni `GetMotionForRole`, ni la machinerie de
roles. Le blocage est **en aval** : quelque chose demande bien l'animation
suivante, l'obtient, et ne l'installe pas.

Les compteurs plus faibles chez Dural (205/206 : 4 contre 71 ; 211/212 : 1
contre 16) sont coherents avec un combattant qui ne bouge pas -- ce sont des
consequences, pas des causes.

**Piege de methode, note pour ne pas le refaire** : `MothOnMotionEnd`
(`0x180133010`) et `RoleToMotionId` (`0x180147680`) d'`analysis/functions.csv`
sont les adresses du build **Steam**, pas d'APM3. Les avoir prises pour des
adresses APM3 donne zero passage -- et zero passage se lit tres facilement, a
tort, comme « la machinerie ne tourne pas ». Toujours verifier la colonne
`binaire` du CSV. La regle du chantier « ne pas melanger les versions » vaut
aussi pour nos propres notes.

---

## 13. DURAL EST DANS LA GRILLE DE LA BORNE (2026-09-04)

Apres avoir ferme la route console (`analysis/machine_console.md` section 5 :
la page `CHAR SELECTOR` n'a aucun pilote), le regard s'est porte sur le
selecteur **reellement vivant**, celui du combat : sous-etats `SELECTOR` (17) et
`APM3_SELECTOR` (49), objet `[0x180714928]`, fonctions `0x18016Cxxx`.

### La table d'animations : 21 cases, dont Dural

`0x1801700B0` monte un tableau local d'entrees de 0x18 octets, chacune portant
deux noms d'animation. Dans l'ordre de la grille :

```
aki pai lau wol jef kag sar jak shu lio aoi lei van goh bra msk mon krt tak dur rnd
 0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20
```

**`dur` y est, avec son `dur_end`**, suivi de `rnd` (aleatoire). Vingt et une
cases.

### Le champ `+0` de chaque case porte l'indice ROB

Releve des immediats ecrits dans le tableau :

| case | rbp | valeur | personnage |
|---:|---|---:|---|
| 1 | -0x58 | 5 | PAI |
| 2 | -0x40 | 2 | LAU |
| 3 | -0x28 | 9 | WOL |
| 4 | -0x10 | 4 | JEF |
| 7 | +0x38 | 6 | JAK |
| 8 | +0x50 | 3 | SHU |
| 9 | +0x68 | 8 | LIO |
| 10 | +0x80 | 10 | AOI |
| 11 | +0x98 | 11 | LEI |
| 12 | +0xB0 | 12 | VAN |
| 13 | +0xC8 | 14 | GOH |
| 14 | +0xE0 | 13 | BRA |
| 15 | +0xF8 | 16 | MSK |
| 16 | +0x110 | 15 | MON |
| 17 | +0x128 | 17 | KRT |
| 18 | +0x140 | 18 | TAK |
| **19** | **+0x158** | **20** | **DUR** |

(Les cases 0, 5 et 6 -- AKI, KAG, SAR -- sont ecrites par registre et
n'apparaissent pas dans ce releve d'immediats.)

**Le selecteur de la borne a donc une case Dural, qui porte le bon indice ROB.**

### Ce que cela reinterprete

Les nombreux `cmp eax, 0x13` de cette zone (`0x18016C5BF`, `0x18016E334`,
`0x18016ED51`, `0x18016EF83`, `0x180170452`, `0x180170DE5`) ne sont **pas** une
borne de roster a 19, comme je l'avais d'abord lu. Dans la numerotation
d'affichage de la grille, **0x13 = 19 = la case de DURAL**. Ce sont des branches
specifiques a Dural, et `0x15` = 21 y sert de « aucun personnage ».

`0x180173AA0(selecteur, joueur)` rend le personnage survole :
`[objet + joueur*0x40 + 0x88]` -> cellule -> `[cellule+8]`.

### Ce qui reste a trouver

Ce qui rend la case 19 visible ou atteignable par le curseur. Ce n'est PAS
`is_dural_unlocked` : les cinq lecteurs de `0x180C3B700` sont tous dans le code
d'interface console, aucun dans `0x18016xxxx`. Une piste ecartee : le drapeau
lu en `0x1801703F7` (`[0x1806490D0+0x20]`) ne fait que decaler un identifiant
d'affichage de `0x149` a `0x14A`.

Prochaine mesure, dynamique cette fois, et faisable **en mode borne** qui
fonctionne deja : atteindre `APM3_SELECTOR` et lire le tableau de cases en
memoire -- combien sont peuplees, et quel etat porte la case 19.

Confiance : **CONFIRMED** pour la table et l'indice ; **UNKNOWN** pour la garde
qui la masque.

### 13.1 Mesure a l'ecran, et ce qu'elle elimine (2026-09-04)

**Frederic, a l'ecran : « elle n'apparait pas du tout ».** La case existe donc
en memoire mais n'est pas dessinee.

Le tableau lu dans le jeu qui tourne, 384 passages, une seule disposition :

```
case  0 AKI   case  5 KAG   case 10 AOI   case 15 MSK
case  1 PAI   case  6 SAR   case 11 LEI   case 16 MON
case  2 LAU   case  7 JAK   case 12 VAN   case 17 KRT
case  3 WOL   case  8 SHU   case 13 GOH   case 18 TAK
case  4 JEF   case  9 LIO   case 14 BRA   case 19 DUR
```

Vingt cases peuplees, la vingtieme etant Dural. La case 21 est du remplissage :
le tableau fait 20 entrees, pas 21.

**Pistes eliminees dans la meme seance** -- elles valent d'etre notees, car
chacune paraissait bonne :

- `0x1801700B0` n'est **pas** la boucle de dessin. C'est un *lookup* : il monte
  le tableau puis le parcourt pour trouver l'entree correspondant a un
  personnage donne (`cmp rax, 0x14` a `0x18017047B`). D'ou ses 384 appels.
- Les structures de **0x298 octets** ne sont pas touchees au selecteur : les
  points d'arret sur `0x18016EEBA` et `0x180237DC9` n'ont eu **aucun passage**.
- Les deux boucles bornees a 19 de `0x180197A10` liberent dix-neuf poignees de
  **son** (`load02`), pas des cases.
- Le drapeau lu en `0x1801703F7` (`[0x1806490D0+0x20]`) ne fait que decaler un
  identifiant d'affichage de `0x149` a `0x14A`.
- `CodeDuPersonnage` ne sert pas au dessin de la grille : au selecteur, il n'est
  demande que pour les deux personnages choisis. La grille passe par les noms
  d'animation du tableau, pas par le code a trois lettres.

**Prochaine mesure, et il faut d'abord un scenario qui RESTE au selecteur** --
`select_a.txt` le traverse et enchaine sur un combat, ce qui rend toute mesure
aveugle. Une fois immobile sur la grille, relever quelles planches et quelles
animations sont reclamees : la boucle qui les demande est la boucle de dessin,
et sa borne est ce qui s'arrete a dix-neuf.

### 13.2 La planche de la grille : `aet_s_selcha` (2026-09-04)

Mesure au point d'arret sur les scenes nommees, pendant que Frederic tenait
l'ecran de selection : **aucun code de personnage n'est demande**. La grille
n'est pas faite de scenes separees, c'est **une seule scene**, chargee avec
deux compagnes :

```
SEL_COMMON   depuis moteur+0x16C6FD
SEL_CHARA    depuis moteur+0x16CB5D
SEL_CURSOR   depuis moteur+0x16E18C
```

Les vingt cases sont donc des **calques** de la planche `aet_s_selcha`. C'est
pourquoi quatre recherches de « boucle de dessin bornee a 19 » n'ont rien
donne : il n'y a pas de boucle de ce genre.

Contrainte pratique decouverte au passage : **l'ecran de selection ne dure que
quinze secondes** (le decompte de la borne). D'ou
`tools/scenarios/rester_grille.txt`, qui amene le jeu sur `APM3_SELECTOR` et
l'y laisse -- verifie a la trace, sans intervention.

### Ce que dit la planche PS3

`extracted/PS3_2d/2d/aet_s_selcha.bin`, 311 952 octets. Occurrences des codes
de personnage dans ses chaines :

```
les 19 personnages : 30 a 34 chacun
dur : 15        rnd : 15
```

**Dural y est**, avec moitie moins de calques que les autres -- exactement comme
`rnd`. Ce sont des cases d'un type different, pas des cases absentes.

### Ce qui manque pour conclure : le decompresseur SLLZ

La planche de la BORNE est dans `vf5fs_data.par`, compressee. `ParTool.exe` ne
sait extraire que l'archive entiere (4 Go), d'ou `tools/sllz.py`, qui lit
l'index PARC et vise un seul fichier.

**Le lecteur d'index fonctionne** (format documente dans l'en-tete de l'outil,
etabli par l'arithmetique : (19 + 1862) * 64 + 0x20 = 0x1D660, exactement
l'offset des repertoires). Il donne :

```
aet_s_selcha.bin   312 464 o decompresses, 77 742 compresses, offset 0x174D000
```

**Le decompresseur, lui, n'est pas au point.** Le bloc est du `SLLZ` version 1
petit-boutiste, mais aucune des huit variantes classiques du LZSS (bit de
paire 0 ou 1, bits MSB ou LSB, deux encodages de paire, avec ou sans +1) ne
depasse **40 octets** sur 312 464. Le format de ce build n'est pas le LZSS
usuel ; c'est un chantier a part.

### L'indice que la taille donne

Borne 312 464 octets, PS3 311 952 : **512 octets d'ecart**. Une grille a
dix-neuf cases au lieu de vingt differerait de bien plus. Les deux planches
sont donc tres probablement de meme structure, et la case de Dural presente
des deux cotes.

Si cela se confirme, **la planche n'est pas la limite** : c'est le code qui lie
dix-neuf calques sur vingt. Confiance : **LIKELY**, et il faut le decompresseur
pour trancher.

### 13.3 SLLZ : ce qui est acquis, ce qui resiste (2026-09-04)

**Acquis, et deja utile : le lecteur d'index PARC** (`tools/sllz.py`). Il donne
l'acces a n'importe lequel des 1862 fichiers de `vf5fs_data.par` sans extraire
les 4 Go, ce qui manquait au projet depuis le debut -- `ParTool.exe` ne sait
extraire que l'archive entiere.

```
0x00  "PARC"                          gros-boutiste
0x10  nb repertoires   0x14 offset
0x18  nb fichiers      0x1C offset
0x20  table de noms, 64 octets par entree, repertoires puis fichiers
      (19 + 1862) * 64 + 0x20 = 0x1D660 = l'offset des repertoires : verifie
entree de fichier, 32 octets : drapeaux, taille, taille compressee, offset
```

**Le decompresseur, lui, resiste.** Methode employee, qui vaut d'etre notee :
plutot que de deviner, on se sert de la planche PS3 comme sortie attendue et on
laisse un chercheur reconstruire le codage -- litteral quand l'octet du flux
vaut l'octet attendu, paire sinon.

Ce que cette reconstruction etablit **solidement** : quatre groupes `0x55`
consecutifs donnent exactement

```
0x55 -> PAIRE litteral PAIRE litteral PAIRE litteral PAIRE litteral
```

soit, en bits de **poids faible d'abord**, `1,0,1,0,1,0,1,0` : **bit a 1 =
paire**. Et toutes ces paires se decodent en **mot de 16 bits petit-boutiste,
longueur = (v & 0xF) + 3, recul = (v >> 4) + 1**.

Ce qui **resiste** : le regroupement des drapeaux. Huit elements par octet de
drapeaux fait derailler a 41 octets, et le trace montre pourquoi -- on emet
`34`, `20`, `20`, `70`, `B0` la ou la PS3 n'a que des zeros. Ces octets ont
tout l'air d'etre des drapeaux intercales que le schema consomme comme des
donnees. Le premier groupe semble n'en couvrir que sept, ce qu'aucun LZSS
usuel ne fait.

Piege de methode a retenir : mon balayage de 32 variantes les notait sur la
**longueur du prefixe commun avec la PS3**. Or les deux fichiers different
(312 464 contre 311 952 octets). Le bon critere est que la longueur totale
tombe juste, pas que la sortie ressemble a la PS3.

**Voie de secours, si le format resiste encore** : le moteur decompresse la
planche lui-meme au chargement du selecteur. Avec
`tools/scenarios/rester_grille.txt`, qui parque le jeu sur `APM3_SELECTOR`, il
suffit de trouver le tampon et de le vider en memoire -- meme resultat, sans
decompresseur.

### 13.4 TRANCHE : la planche n'est pas la limite (2026-09-04)

Le decompresseur SLLZ fonctionne (voir plus bas), la planche de la borne est
extraite, et le verdict est net :

```
borne : extracted/APM3_2d/aet_s_selcha.bin      311 952 octets
PS3   : extracted/PS3_2d/2d/aet_s_selcha.bin    311 952 octets
IDENTIQUES au bit pres -- meme SHA-1
```

**La grille de la borne EST celle de la console.** Et Dural y a un jeu de
calques complet :

```
S_SELCHA_GRAPH_L_DUR          le portrait
S_SELCHA_NAME_DUR             le nom
S_SELCHA_STYLE_DUR            le style
dur / dur_end                 les animations d entree et de sortie
rend_chara_dur                le rendu
style_dur_1p / _1p_e / _2p / _2p_e     les quatre variantes, deux joueurs
chara_name_l_1p_dur2 / _2p_dur2
s_selcha_graph_l_dur__n.pic / s_selcha_name_dur.pic / s_selcha_style_dur.pic
```

Compare a TAK (temoin, 18 calques contre 15), il ne lui manque que deux
variantes mineures : `S_SELCHA_STYLE_TAK_E` et `rend_chara_tak_nor`.

**Conclusion : ni les donnees de combat, ni la grille, ni la planche ne limitent
Dural. C'est le CODE qui lie dix-neuf calques sur vingt.** Confiance :
**CONFIRMED**.

Une erreur d'arithmetique corrigee au passage : `0x4C290` vaut 311 952 et non
312 464. Les « 512 octets d'ecart » du paragraphe 13.2, et la prudence qu'ils
justifiaient, n'existaient pas.

### Le decompresseur SLLZ, et la lecon

`tools/sllz.py` decompresse maintenant. L'algorithme vient de **ParManager**
(Kaplas80), `ParLibrary/Sllz/Decompressor.cs`, MIT, lu et non execute :
https://github.com/Kaplas80/ParManager

Deux details que la reconstruction n'avait pas devines :

  * les bits du drapeau se lisent de **poids fort** d'abord, un bit a 1
    commandant une paire ;
  * le drapeau est decale, et recharge s'il est epuise, **AVANT** la lecture des
    octets de l'element -- pas apres. Ce decalage d'un cran donnait l'illusion
    que le premier groupe ne couvrait que sept elements, ce qui m'a fait
    chercher un format exotique la ou il n'y en avait pas.

La paire, elle, etait juste : mot de 16 bits petit-boutiste,
`distance = 1 + (v >> 4)`, `longueur = 3 + (v & 0xF)`.

**Lecon de methode** : j'ai passe une heure a reconstruire un format public
avant que Frederic demande « tu as regarde sur internet ? ». `ParTool.exe`
etait dans `tools/` depuis le debut du projet, et son auteur publie ses
sources. Chercher l'implementation existante AVANT de retro-concevoir.

### 13.5 Les quatre bornes a 18 : essai NEGATIF (2026-09-04)

Quatre sites bornent a `0x12` = 18 juste avant d'indexer les enregistrements de
case (`imul .., 0x298`) :

```
0x18016EB2D  cmp eax,  0x12 ; jg    offset fichier 0x16DF2F
0x18016EC37  cmp eax,  0x12 ; jg    offset fichier 0x16E039
0x18016EEBA  cmp r15b, 0x12 ; ja    offset fichier 0x16E2BD
0x180172391  cmp ebx,  0x12 ; ja    offset fichier 0x171793
```

Portes a `0x13` (`patch_moteur.py --dural-grille`), essayees a l'ecran :
**« rien ne change »**. Ces quatre-la sont donc du chemin d'ENTREE, pas
d'affichage. Le correctif a ete retire.

Deux autres pistes ecartees dans la meme passe :

- `0x1801721D0(objet, id)` et `0x180172210`, appelees avec des identifiants
  consecutifs 0x13, 0x14, 0x15, ne sont pas de l'affichage : elles **liberent**
  une poignee (`0x180029BE0`) et remettent le champ a zero.
- Les paires `mov edx, 0x13` / `mov edx, 0x14` reperees dans quatre fonctions
  ne sont pas des comptes conditionnels mais des appels successifs a ces
  memes liberations.

### Le fil qui reste : le selecteur SAIT dans quel mode il est

Son constructeur `0x180171D80` pose deux booleens opposes selon `game_mode` :

```
0x180171DFA  cmp byte [0x180C3B701], 0     ; game_mode != 0
0x180171E01  je  console
0x180171E03  cmp byte [0x180C3B702], 0     ; game_mode == 2
0x180171E0A  jne console
             borne   : al = 1, cl = 0
  console :  al = 0, cl = 1
0x180171E16  mov byte [selecteur + 0x124], cl    ; 1 en console
0x180171E1C  mov byte [selecteur + 0x125], al    ; 1 en borne
```

et `0x180171460` les relit (`cmp byte [rsi+0x124], 0` puis `[rsi+0x125]`).
Il y a **dix** lecteurs de `game_mode != 0` dans la zone du selecteur : le
sélecteur a donc bien deux comportements, et le nombre de cases en fait
probablement partie.

**Prochaine mesure, decisive et faisable** : forcer `game_mode = 0` ET le
sous-etat `SELECTOR` (l'ecriture directe des globaux fonctionne, voir
`analysis/machine_console.md` section 5 -- entree du mode et du sous-etat
executees, milieu tournant 1326 fois). Si la grille montre alors **vingt**
cases, la difference est l'une de ces dix branches, et il n'y a plus qu'a
bissecter. Si elle en montre toujours dix-neuf, le compte est ailleurs.

### 13.6 Essai en mode console : NEGATIF, et il elimine beaucoup (2026-09-04)

Montage : `game_mode = 0`, `is_dural_unlocked` pose, et le sous-etat `SELECTOR`
force par ecriture directe des globaux (`0x18070C4F0` = 2, `0x18070C50C` = 17,
les deux phases a 0).

Cote instruments, la machinerie tourne :

```
entree du sous-etat SELECTOR       1 passage
milieu du sous-etat              783 passages
montage de la table de grille   1472 passages
```

Frederic, a l'ecran : « le mode console est bugge, le menu s'affiche par-dessus
l'ecran de selection des personnages. **Dural est absente**. »

Deux enseignements, et le second est le plus utile :

1. **Forcer le sous-etat AFFICHE bien la grille.** Le levier fonctionne ; seul
   le mode `MENU`, qui continue de tourner en parallele, dessine par-dessus.
   Un prochain essai devra neutraliser la page de menu pour laisser le
   selecteur seul a l'ecran.

2. **La limite a dix-neuf n'est conditionnee NI par `game_mode` NI par
   `is_dural_unlocked`.** Elle est inconditionnelle dans ce build.

Cela **elimine** la piste des dix branches borne/console du selecteur, proposee
au paragraphe 13.5, et avec elle toute la famille « c'est un drapeau de mode
qui masque la case ». Le compte de dix-neuf est en dur.

### Ce qui reste, et comment le prendre

Recapitulatif des couches, toutes verifiees :

| couche | etat |
|---|---|
| donnees de combat | completes (356/363 roles) |
| table de la grille en memoire | 20 cases, la 19e est Dural |
| planche `aet_s_selcha` | identique a la console, calques de Dural complets |
| bornes d'index a 18 | du chemin d'ENTREE -- essai negatif |
| aiguillage borne/console | sans effet -- essai negatif |

**Prochaine mesure** : maintenant qu'on sait afficher la grille a volonte,
demander au jeu **quelles cases il dessine**. Poser un point d'arret sur la
pose d'un calque et relever les indices : si 0 a 18 passent et 19 jamais, le
site d'appel nomme la boucle et sa borne. C'est la meme methode qui a donne
`SEL_CHARA` -- interroger le jeu plutot que lire le binaire a l'aveugle.

### 13.7 LA CAUSE EST TROUVEE : la borne affiche la disposition VGA (2026-09-04)

`tools/aet.py` lit les planches AET (structure reprise d'`AetPlugin`, samyuu --
format partage avec Project DIVA et **explicitement documente pour Virtua
Fighter 5**). Applique a `aet_s_selcha.bin`, il donne :

```
VGA_MAIN    113 compositions, 1280x768
WXGA_MAIN   174 compositions, 1280x768
```

et, en resolvant le nom de chaque composition par le calque qui la designe :

| scene | composition | calques | Dural |
|---|---|---:|---|
| **VGA_MAIN** | `chara_rend_cos_l` | 19 | **absente** |
| | `chara_rend_cos_l_nor` | 19 | **absente** |
| **WXGA_MAIN** | `chara_rend_cos_l_1p` | 21 | **`rend_chara_dur`** |
| | `chara_rend_cos_l_2p` | 21 | **`rend_chara_dur`** |
| | `chara_rend_cos_l_nor` | 21 | **`rend_chara_dur`** |

La grille VGA compte **dix-neuf cases et n'a ni Dural ni aleatoire** ; la grille
WXGA en compte vingt et une. **Voila pourquoi Dural n'apparait pas : la borne
affiche la disposition VGA.**

Cela referme d'un coup deux anomalies restees en suspens :

  * `spr_c_mchdurvga` est la **seule** planche absente du registre des 862
    actifs -- la variante VGA n'ayant pas de case Dural, son sprite VGA n'a
    jamais existe ;
  * la question « quel code lie dix-neuf calques sur vingt » etait **mal
    posee**. Aucun code ne borne a dix-neuf : la composition VGA n'en contient
    que dix-neuf. Trois recherches de boucle bornee ont echoue pour cette
    raison.

Confiance : **CONFIRMED** (lu dans le fichier, compositions nommees).

### Ce qui reste, et une supposition corrigee

`--wxga` bascule l'octet `[0x1806490D0 + 0x20]` (offset fichier `0x6478F0`,
constante de `.data` que rien n'ecrit). Mesure a l'execution
(`tools/pister_vga.py`) : **`r13 = 1`, identifiant de scene `0x14A`** -- la
bascule opere. Mais a l'ecran, **toujours pas de Dural**.

Supposition a corriger : j'ai suppose toute la soiree que `SEL_CHARA` etait la
scene de la grille. **Elle n'existe ni comme scene ni comme composition de ce
fichier.** Les scenes s'appellent `VGA_MAIN` et `WXGA_MAIN` ; `SEL_CHARA` est
un nom d'entree de `aet_db`, et `0x149`/`0x14A` sont des identifiants de cette
base. L'octet a donc bascule **un** site sur les cinquante-quatre qui le lisent
-- celui de `0x1801700B0` -- et la grille elle-meme est instanciee ailleurs,
avec son propre identifiant, toujours en VGA.

**Prochaine mesure** : lire `aet_db` (les entrees `aet_*` et leurs
identifiants) pour savoir quel identifiant designe la grille, puis trouver le
site qui le choisit. `tools/sllz.py` sort `aet_db` du `.par` en une commande,
et `tools/aet.py` sait deja lire ce qui en sort.

---

## 14. LA GRILLE DE LA BORNE, EN ENTIER (2026-09-04)

Etat a l'ouverture de cette section : Dural **est dessinee** dans la grille
(les deux gardes `_dur` de la section 13 sont forcees), mais **le curseur ne
peut pas aller dessus**. Observation de Frederic, a l'ecran.

### 14.1 Comment on l'a trouve : la zone entiere, pas la fonction du jour

Reproche de methode, et il est juste : « je ne comprends pas pourquoi toutes
les fonctions de l'ecran de selection ne sont pas encore desassemblees ».
`tools/carte_zone.py` cartographie les 411 fonctions du selecteur en une
minute ; `tools/plage.py` (nouveau) desassemble une PLAGE, sans s'arreter au
premier `ret` -- une vraie fonction couvre souvent plusieurs entrees `.pdata`
chainees, et la prendre pour la fonction entiere fait conclure faux.

Le premier balayage « systematique » de la section 13 ne l'etait pas : il
cherchait les appels au predicat **autour des chaines `_dur`**, et n'en a
trouve que deux. En enumerant les appelants du bouchon `0x180007450` dans toute
la zone, il y en a **seize**. Deux suffisaient a la dessiner ; un autre la rend
atteignable.

### 14.2 La grille est une liste de cases, pas un tableau d'indices

`0x180173BD0(grille, table, nombre)` construit la liste :

    alloue nombre * 0x18 octets sous l'etiquette "SEL_DATA"  -> [grille+0x58]
    [grille+0x70] = nombre
    pour chaque i : [liste + i*0x18]        = &table[i]
                    [liste + i*0x18 + 0x14] = 0        <- le drapeau
    puis min/max des colonnes et des lignes -> +0x60 +0x64 +0x68 +0x6C

La table d'entree a un pas de **0x20 octets** : `+0x00` colonne, `+0x04` ligne,
`+0x08` numero de personnage, `+0x0C`/`+0x10` deux flottants, `+0x18` le nom de
la composition AET. Le curseur, lui, est un **pointeur de case**, pas un
indice : `0x180173AA0(sel, joueur)` rend `[[sel + joueur*0x40 + 0x88] + 8]`.

C'est pourquoi relever des bornes numeriques ne pouvait rien donner.

### 14.3 Les deux tables de disposition, lues dans le binaire

Elles se suivent, `0x1803FF0B0` puis `0x1803FF350` (21 x 0x20 = 0x2A0 : la
seconde commence exactement ou la premiere finit).

**Table A, `0x1803FF0B0` -- la borne. Sept colonnes, trois lignes, 21 cases :**

    ligne 0 :  TAK  AKI  PAI  LAU  WOL  JEF  KRT
    ligne 1 :  MON  KAG  SAR  JAK  SHU  LIO  MSK
    ligne 2 : [DUR] AOI  LEI  VAN  BRA  GOH  TE2

Dural est **en bas a gauche**, colonne 0, ligne 2, personnage 20.

**Table B, `0x1803FF350` -- la console. Onze colonnes, deux lignes, 21 cases**,
Dural en (10, 0). C'est la disposition que decrit le chemin de deplacement
« grille reguliere » du curseur, avec sa colonne 0..9 elargie a 0..10 quand
Dural est debloquee -- et c'est aussi celle des 21 calques de
`chara_icon_name_base_dur`. Le choix entre les deux tables ne depend pas de
WXGA mais de la presence d'un rappel de debogage (`[global + 0x1FE10]`) :
absent, on prend la table A. CONFIRMED (lecture du binaire).

### 14.4 La cause : la case est desactivee, explicitement

    0x18016E20B  call 0x180007450     ; predicat bouchonne -> rend 0
    0x18016E210  test al, al
    0x18016E212  jne 0x18016E221      ; si VRAI : on ne desactive rien
    0x18016E214  mov edx, 0x14        ; 20 = DURAL
    0x18016E21C  call 0x180173F50     ; pose 1 en +0x14 de sa case

`0x180173F50(grille, perso)` parcourt la liste et marque la case dont le `+8`
vaut `perso`. Et le deplacement du curseur (`0x180173110`, 1205 octets, sept
entrees `.pdata` chainees) cherche la case voisine ainsi :

    cmp byte ptr [rax + 0x14], 0
    jne case_suivante              <- une case marquee est SAUTEE

La case existe, elle est construite, elle est dessinee -- et le curseur passe a
cote. C'est exactement le symptome observe. CONFIRMED.

Le site voisin `0x18016E1D6` garde une SECONDE liste, `0x1803FF5F0` : AKI, LAU,
SHU, JEF, KAG, LIO, WOL, AOI, LEI, VAN, BRA, GOH, MON, MSK, DUR -- quinze
personnages desactives d'un coup, ce qui laisse SAR, PAI, JAK, KRT, TAK. C'est
un **roster de demonstration** (le tirage aleatoire de `0x180170560` pioche
dans exactement ces cinq-la). Ce predicat-la doit rester FAUX : on n'y touche
pas.

### 14.5 Correction d'une erreur de numerotation

Le commentaire de `GRILLE_BORNES` affirmait « dur = 19, rnd = 20 » dans une
numerotation d'affichage distincte. **C'est faux**, et les tables le disent en
clair : la case 19 de la table A porte le personnage **20**, et la grille de la
borne n'a **aucune** case aleatoire. Les quatre bornes `cmp .., 0x12` devaient
donc passer a **0x14**, pas a 0x13 -- porte a 0x13, on n'ouvrait que TE2 et
Dural restait dehors. C'est pourquoi `--dural-grille` seule n'avait rien
change.

Et c'est sans danger : le tableau d'enregistrements de 0x298 octets en compte
exactement vingt et un. `0x180141EBA` lit `[rdx + 0x35A8]`, soit 0x298 * 21 --
le premier champ apres le tableau. L'indice 20 est dans les bornes.

### 14.6 Ce qui est applique

`--dural-grille` fait desormais trois substitutions d'appel et quatre bornes :

    0x18016DC69  call 0x180007450 -> mov al,1   compositions `_dur` (dessin)
    0x18016E109  call 0x180007450 -> mov al,1   idem
    0x18016E20B  call 0x180007450 -> mov al,1   la case n'est plus desactivee
    0x18016EB2D / 0x18016EC37 / 0x18016EEBA / 0x180172391 : 0x12 -> 0x14

Les 207 autres appelants du bouchon `0x180007450` sont intacts : ce corps est
partage par repliement COMDAT entre plusieurs predicats bouchonnes distincts,
et c'est le **site d'appel** qui a un sens, jamais le corps.

### 14.7 VERIFIE A L'ECRAN : DURAL EST JOUABLE

Verdict de Frederic, 2026-09-04 : **« dural selectionnable, aucun defaut
perceptible pendant les combats, Dural est jouable. »**

Les trois points de la chaine sont donc valides d'un coup :

1. le curseur atteint sa case, en bas a gauche de la grille ;
2. la validation mene au combat ;
3. le combat se deroule sans defaut perceptible.

Le but du chantier ouvert le 2026-09-02 est atteint. Et il l'est **par la voie
propre** : aucun forcage a l'execution, aucun debogueur en fonctionnement, rien
qui doive tourner a cote du jeu. Sept substitutions statiques dans le moteur
(section 14.6), un drapeau de configuration (`--dural`), et la variante WXGA.
Le jeu se lance normalement.

Ce que cela invalide, et qu'il faut lire avec cet oeil-la :

* la piste « Dural se fige sur `0x510B` » (sections 8 et 9) etait une fausse
  alerte, deja corrigee en section 11 : `0x510B` est son repos, `DUR_L_IDLE_TA`.
  Elle ne s'est jamais figee ;
* la piste « il manque un drapeau de profil equivalent au deblocage console »
  etait juste dans son intuition mais fausse dans sa cible : le drapeau existe
  bien, c'est le predicat bouchonne `0x180007450` -- mais il fallait le forcer
  **aux bons sites d'appel**, pas chercher un stockage qui n'existe pas
  (`ctx+0xC` bit 0 : quatre lecteurs, zero ecrivain) ;
* la voie du forcage d'indice a l'execution (`tools/pister_perso.py`,
  section 8) reste valide comme instrument de mesure, mais n'est plus la voie
  de livraison.

### 14.8 La commande

    py -3 tools/patch_moteur.py --resolution 1280 720 --langue         --logo-japonais --dural --wxga --dural-grille

`--wxga` est necessaire : les compositions `_dur` n'existent que dans la scene
WXGA. `--dural` pose `is_dural_unlocked` dans le `vf5fs_game_config_t`.
`--dural-grille` fait les trois substitutions d'appel et les quatre bornes.
