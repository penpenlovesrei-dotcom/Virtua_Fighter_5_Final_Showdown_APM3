# Format `mothead_<CHR>.bin` — données de mouvement

Fichier de données de combat, un par personnage, dans `rom/rob/`.
Petit-boutiste (contrairement au conteneur FARC qui l'entoure, gros-boutiste).

Corpus de validation : **104 fichiers, 64 distincts au SHA-256**, quatre jeux de données —
arcade 2.000 (Rev A, 21), arcade 6.000 (Rev B, 21), R.E.V.O. `rom/` (21 + 20 doublons dans
`resident.farc`), R.E.V.O. `rom_200/` (21).

Lecteur : `tools/mothead.py`. Inventaire des codes : `analysis/mothead_opcodes.csv`.
Désassemblage : `analysis/disasm_mothead_section1.txt` (les quatre fonctions de la
section 1), `analysis/disasm_mothead_handlers.txt` (les 84 gestionnaires de codes),
`analysis/disasm_mothead_consumers.txt` (les consommateurs de l'état) et
`analysis/disasm_mothead_readers.txt` + `analysis/disasm_mothead_readers2.txt`
(les lecteurs des champs, code par code), `analysis/disasm_mothead_ondemand.txt`
(les codes réclamés à la demande) et `analysis/disasm_mothead_list2.txt` (la liste 2).
Relevés : `analysis/mothead_state_readers.csv` et `analysis/mothead_list2_consumers.csv`.
Relevé exhaustif des accès : `analysis/mothead_state_readers.csv`.

---

## 1. En-tête du fichier — 32 octets

```
0x00  u32  nombre de sections      toujours 2
0x04  u32  offset de la section 1  toujours 32
0x08  u32  offset de la section 2  variable
0x0C  u32 x5  zeros
```

**Vérifié sur 104/104 fichiers.** Confiance : **CONFIRMED**.

| Section | Plage | Contenu |
|---|---|---|
| 1 | `[32, off2)` | données de mouvement |
| 2 | `[off2, EOF)` | bloc `CCD` |

Dans tout ce qui suit, **`s1` désigne l'offset 32**, base de la section 1. Tous les offsets
stockés dans la section 1 sont **relatifs à `s1`**.

---

## 2. Section 1 — les mouvements

Trois zones qui se suivent :

```
s1+0x00                en-tete de section, 32 octets
s1+0x20 .. s1+tbl      enregistrements et charges utiles
s1+tbl .. off2         table de recherche par identifiant d'animation
```

### 2.1 En-tête de section — 32 octets

```
+0x00  u32  index du jeu d'animation
+0x04  u32  plus petit identifiant d'animation du jeu   (id_min)
+0x08  u32  plus grand identifiant d'animation          (id_max)
+0x0C  u32  offset de la table de recherche, relatif a s1
+0x10  u32 x4  zeros
```

`id_min` et `id_max` sont **exactement** le minimum et le maximum du jeu d'animations du
personnage tel que le donne `mot_db.bin` — vérifié sur les 21 personnages de l'arcade 6.000,
21/21. Confiance : **CONFIRMED** (voir aussi §4, le code fait le même test).

L'**index du jeu d'animation** correspond à la position du jeu dans la liste de `mot_db.bin`
**privée de `AUTH_CMN`** (le seul jeu vide en dehors de `ADV`) : cela colle pour 20
personnages sur 21. Seul `TAK` porte 46 là où cette règle donnerait 40. Confiance :
**LIKELY**, avec cette exception non expliquée.

**Conséquence pratique, mesurée : ne pas s'en servir comme d'un index.** Passé tel quel à la
table de `tools/motdb.py`, ce champ ne fait tomber que **881 identifiants sur 9 140** dans le
jeu du personnage — 9,6 %. Le lien fiable est le **nom** : `mothead_XXX.bin` ↔ le jeu nommé
`XXX`, qui donne **9 140 sur 9 140**. C'est ce que vérifie
`py -3 tools/mothead.py ids <mot_db.bin> <dossier>`, désormais appelé par
`verifier_formats.cmd`.

### 2.2 La table de recherche

```
nombre d'entrees = id_max - id_min + 1, bourre a un multiple de 32 octets
entree[id - id_min] = offset de l'enregistrement, relatif a s1   (0 = animation absente)
```

Le bourrage vaut 0 à 7 entrées et amène toujours la fin de la table exactement sur `off2`.

**Vérification décisive.** Sur les 21 fichiers de l'arcade 6.000, chaque entrée non nulle
tombe sur un identifiant qui existe dans `mot_db.bin`, et **appartient au jeu d'animation du
personnage lui-même**, sans une seule exception :

| | AKI | AOI | BRA | CMN | DUR | GOH | JAK | JEF | KAG | KRT | LAU |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| entrées pourvues | 366 | 515 | 375 | 789 | 612 | 467 | 340 | 427 | 412 | 256 | 310 |
| identifiants connus | 366 | 515 | 375 | 789 | 612 | 467 | 340 | 427 | 412 | 256 | 310 |
| du bon personnage | 366 | 515 | 375 | 789 | 612 | 467 | 340 | 427 | 412 | 256 | 310 |

(idem pour `LEI` 408, `LIO` 361, `MON` 290, `MSK` 408, `PAI` 393, `SAR` 357, `SHU` 449,
`TAK` 361, `VAN` 697, `WOL` 547.)

Confiance : **CONFIRMED**.

### 2.3 Un enregistrement — 32 octets d'en-tête

```
+0x00  u32  drapeaux 0
+0x04  u32  drapeaux 1
+0x08  u32  drapeaux 2
+0x0C  u32  drapeaux 3
+0x10  u16  drapeaux 4
+0x12  u16  drapeaux 5
+0x14  u32  offset de la liste 1, relatif a s1   (0 = liste absente)
+0x18  u32  offset de la liste 2
+0x1C  u32  offset de la liste 3
```

Les enregistrements commencent tous sur un multiple de 32.
Les quatre premiers champs sont des **mots de drapeaux** : le moteur les recopie tels quels
dans l'état du personnage puis teste des bits isolés (§4). 254 valeurs distinctes pour le
champ 0 sur le corpus ; sémantique **UNKNOWN**.

Sur les **36 135 enregistrements** des quatre jeux de données, les trois offsets de liste sont
**toujours** soit nuls, soit un offset valide `≥ base+0x20`, et le plus petit offset non nul
vaut **toujours exactement `base+0x20`** (36 135 / 36 135). Combinaisons observées :

| liste 1 | liste 2 | liste 3 | enregistrements |
|:--:|:--:|:--:|---:|
| ● | ● | · | 25 680 |
| ● | · | · | 5 661 |
| ● | ● | ● | 3 301 |
| · | · | · | 961 |
| · | ● | · | 317 |
| ● | · | ● | 215 |

Confiance : **CONFIRMED**.

### 2.4 Les trois listes

```
liste 1   entrees de 8 octets    u32 code, u32 offset de charge utile
liste 2   entrees de 12 octets   u32 code, u32 trame, u32 offset de charge utile
liste 3   tableau de u32         offset de charge utile (16 octets), termine par 0
```

Les listes 1 et 2 se terminent sur un **code négatif** (`0xFFFFFFFF`). Le moteur arrête aussi
la liste 1 sur une charge utile nulle — cas qui **n'apparaît jamais** dans les données
(0 sur 131 080 entrées). En liste 2, la charge utile nulle est licite : 10 211 entrées sur
119 173.

Conformité sur les 36 135 enregistrements des quatre jeux de données
(131 080 entrées de liste 1, 119 173 de liste 2, 9 221 de liste 3) :

| Contrôle | Résultat |
|---|---|
| liste 1 : charges dans la section, offsets décroissants | 34 857 / 34 857 |
| liste 2 : charges dans la section, offsets décroissants | 29 298 / 29 298 |
| liste 2 : champ *trame* croissant le long de la liste | 29 298 / 29 298 |
| liste 3 : charges dans la section | 3 516 / 3 516 |

Confiance : **CONFIRMED**.

**Le champ *trame* de la liste 2** va de 0 à 280 et croît le long de chaque liste : la liste 2
est une **chronologie d'événements datés** dans l'animation. Confiance : **SUPPORTED** — le
code le corrobore (§4, code 6 : la valeur est convertie en flottant et servie à un calcul de
trajectoire).

**Les charges utiles sont partagées.** Elles ne sont pas contenues dans l'enregistrement qui
les désigne : deux mouvements aux mêmes paramètres pointent le même bloc, et une charge peut
se trouver n'importe où dans la zone des enregistrements, y compris avant. C'est un pool
dédupliqué à la compilation, comme le pool de flottants du CCD.

### 2.5 Taille des charges utiles

La taille se déduit de l'écart jusqu'à la charge suivante du fichier : le **minimum** observé
sur tout le corpus est la taille réelle, les écarts plus grands venant du partage. Elle est
**déterminée par le code** — c'est-à-dire que le code est bien un opcode.

Liste 1, 51 codes employés dans la plage 0–83 :

| code | taille | emplois | | code | taille | emplois | | code | taille | emplois |
|---:|---:|---:|---|---:|---:|---:|---|---:|---:|---:|
| 0 | 24 | 1 676 | | 45 | 24 | 4 808 | | 61 | 40 | 1 560 |
| 1 | 6 | 30 390 | | 46 | 6 | 4 796 | | 62 | 8 | 52 |
| 2 | 20 | 3 136 | | 47 | 8 | 3 930 | | 63 | 12 | 2 287 |
| 3 | 32 | 13 254 | | 48 | 16 | 358 | | 64 | 4 | 228 |
| 4 | 8 | 653 | | 49 | 20 | 1 360 | | 65 | 12 | 5 417 |
| 5 | 18 | 12 567 | | 50 | 16 | 41 | | 66 | 4 | 237 |
| 10 | 6 | 4 | | 51 | 12 | 1 207 | | 67 | 2 | 56 |
| 12–15 | 6 | 586 | | 52 | 12 | 12 983 | | 68 | 28 | 36 |
| 20–22 | 6 | 300 | | 53 | 8 | 124 | | 69 | 2 | 16 |
| 43 | 8 | 316 | | 54 | 2 | 14 288 | | 70 | 4 | 2 165 |
| 44 | 16 | 140 | | 55 | 16 | 251 | | 71 | 2 | 649 |
| | | | | 56 | 12 | 1 916 | | 72 | 12 | 55 |
| | | | | 58 | 48 | 980 | | 73 | 12 | 5 900 |
| | | | | 59 | 2 | 1 336 | | 74–76 | 4/4/20 | 262 |
| | | | | 60 | 40 | 443 | | 80–83 | 8/24/4/100 | 317 |

Liste 2, 44 codes dans la plage 0–54 ; liste 3, un seul type, 16 octets.
Le détail complet, **avec le nom de chaque code**, est dans `analysis/mothead_opcodes.csv` ;
la §3 explique d'où viennent ces noms.

**Quatre codes de liste 2 n'ont jamais de charge utile** — ce sont de purs jalons de
trame : code 5 (8 760 emplois, trames 0–245), code 6 (1 194, trames 1–230),
code 30 (60, trames 40–75), code 31 (197, trames 7–250). Tous les autres codes en portent
une systématiquement. Confiance : **CONFIRMED**.

---

## 3. Les codes de la liste 1 — lecture des 84 gestionnaires

Le répartiteur `0x1801633C0` (§4) appelle, pour chaque entrée, le gestionnaire
`0x1804210D0[code]` avec trois arguments :

```
rcx -> ctx, trois pointeurs sur la pile :
         ctx[0x00] = ROB          l'objet combattant
         ctx[0x08] = ROB + 0x338
         ctx[0x10] = ROB + 0x798  l'etat de mouvement, celui que 0x1801651D0 remplit
rdx = la charge utile
r8  = l'entree de 8 octets elle-meme
```

Les 84 entrées donnent **81 gestionnaires distincts** (aucun partagé), tous groupés entre
`0x18015FC90` et `0x180162D60` sauf le code 61 (`0x18000AF20`). Trois entrées sont nulles :
les codes **43, 44 et 71**, qui existent pourtant dans les données (79, 29 et 649 emplois) —
ce répartiteur les ignore, ils sont traités ailleurs.

**Les 84 gestionnaires sont désassemblés dans `analysis/disasm_mothead_handlers.txt`** et le
résultat de leur lecture est tabulé dans `analysis/mothead_opcodes.csv` (nom, taille de
charge, champ d'état écrit, adresse du gestionnaire, niveau de confiance, description).

Deux constats de forme, valables sur les 84 :

1. **Un code = un champ (ou un groupe de champs) de l'état de mouvement.** Les gestionnaires
   sont presque tous de simples recopies typées. Les offsets d'état croissent avec le numéro
   de code : l'état de mouvement est une grande structure et le numéro de code en est
   pratiquement l'index de champ.
2. **33 des 84 codes ne sont jamais employés** dans les 84 fichiers du corpus
   (6–9, 11, 16–19, 23–42, 57, 77–79). Le moteur sait les traiter, les données ne s'en
   servent pas.

### 3.1 Le code 3 — l'attaque

C'est le code le plus riche, et le seul dont tous les sous-champs sont identifiés ou cernés.
Il pose `état+0x7C = 1` et incrémente le compteur `état+0x78`. Il est porté par **841 des 986
animations `KI`** (*kick*) et **730 des 890 `PU`** (*punch*).

| Champ | Type | État | Ce que c'est | Confiance |
|---|---|---|---|---|
| `+0x00` | u32 | `0x80` | drapeaux ; 6 valeurs seulement : 2, 6, 10, 14, 34, 66 | UNKNOWN |
| `+0x04` | s16 | `0x84` | **code directionnel 0–62**, remappé en miroir par la table `0x18041F0C0` | CONFIRMED |
| `+0x06` | s16 | `0x88` | **niveau d'attaque** : 1 = haut, 2 = milieu, 3 = bas ; indexe la table `0x18063D060` (§3.7) | CONFIRMED |
| `+0x08` | u16 | `0x8C`, `0x8E` | **dégâts** 0–100 ; `0x8E` = valeur mise à l'échelle, lue par `0x1801423B0` | CONFIRMED |
| `+0x0C` | u32 | `0x94` | vaut 0 sur 3 361 des 3 363 entrées | UNKNOWN |
| `+0x10` | u16 | `0x98` | **angle binaire 16 bits**, nié en miroir | CONFIRMED |
| `+0x12` | s16 | `0x9C` | **indice de réaction dans `yarare.bin`** | CONFIRMED |
| `+0x14` | u32 | `0xA0` | drapeaux ; **bits 0 et 1 échangés en miroir** → gauche / droite | CONFIRMED |
| `+0x18` | u32 | `0xA4` | drapeaux ; vaut 0 sur 3 247 des 3 363 | UNKNOWN |
| `+0x1C` | u16 | `0xA8` | 0–12 ; vaut 7 sur 39 des 70 coups bas | UNKNOWN |

**La table miroir `0x18041F0C0`** compte 63 entrées et n'est faite que d'échanges par paires
(`1↔2`, `3↔4`, `5↔6`, `7↔8`, `9↔10`, `11↔12`, `22↔23`, `24↔25`, `28↔29`, `30↔31`…), les
autres valeurs restant fixes. C'est une table gauche/droite : le champ `+0x04` est donc un
code directionnel. Ce que la direction désigne exactement reste **UNKNOWN**.

**L'indice de réaction.** `0x180166400(indice, 0)` borne son argument à `0x6B` = 107 et
indexe le global `0x180756E28`, écrit par `ParseYarare` — c'est-à-dire **`yarare.bin`, dont
`mot_tables.md` a établi qu'il contient exactement 108 enregistrements**. Le bloc de
`0x50` octets rendu est copié deux fois, en `état+0xAC` et `état+0xFC`. Côté données, les
**3 363 valeurs du champ `+0x12` sont toutes dans [0, 106]**. Le lien coup → réaction est
donc établi de bout en bout. Confiance : **CONFIRMED**.

**Les dégâts.** `0x180177CF0(v, mod)` calcule `v × (mod + 125) × 8 / 1000`, soit
`v × (1 + mod/125)` : une mise à l'échelle centrée sur 100 %, `mod` étant lu en
`ctx[1]+0x24C`. Le champ brut va de 0 à 100, vaut **0 sur toutes les animations `_MISS`**
(`AKI_AKIRA_BPK_MISS`, `AKI_NEW_ATM_HI_MISS`, `AKI_NEW_ATM_LOW_MISS`) et se répartit comme on
attend de dégâts : mode à 20, puis 25, 10, 16, 18, 15.

```
AKI_RPU_00           10       AKI_TA_CHOZAN        35
AKI_TA_CHOZAN_FAST   25       AKI_TA_PU_KOUHI_DA   40
AKI_SY_PU_BYAKO_TA   30       AKI_TA_TETUZAN       80
```

**Le niveau d'attaque.** En partageant les animations sur leur nom (`HI`/`JYO` contre
`MID`/`CHU` contre `LOW`/`GE`), le champ `+0x06` se sépare nettement :

| Groupe de noms | valeur dominante de `+0x06` |
|---|---|
| haut (`HI`, `JYO`) | **1** (17 sur 31) |
| milieu (`MID`, `CHU`) | **2** (39 sur 60) |
| bas (`LOW`, `GE`) | **3** (42 sur 70) |

Et sur l'ensemble du roster la distribution est `2` (1 582) > `1` (777) > `3` (403), l'ordre
attendu entre coups moyens, hauts et bas. Le champ prend 14 valeurs en tout : les valeurs
au-delà de 3 restent **UNKNOWN**.

**L'angle.** Le champ `+0x10` ne prend que des angles binaires ronds — `0`, `0x8000` (180°),
`0x4000` (90°), `0xC000` (270°), `0x2000` (45°), `0x2AAA` (60°), `0xE000` (315°) — et le
gestionnaire du code 54, qui écrit dans un champ du même genre, **nie** la valeur quand le
combattant est en miroir. Confiance : **CONFIRMED**.

### 3.2 Les codes 6 à 42 — une table de 32 fenêtres temporelles

Trente-sept codes forment une seule famille. L'état contient, de `0x154` à `0x2D3`, un
**tableau régulier de 32 fenêtres de 12 octets** (la zone se referme exactement sur `0x2D4`,
où commence le champ du code 2) :

```
fenetre[i]  a  etat + 0x154 + 12*i
    +0  f32  debut  (ecrit seulement si le s16 de la charge est > 0)
    +4  f32  fin    (ecrit si >= 0, puis borne par duree-1)
    +8  f32  valeur (ecrit si != -1)
```

La charge utile fait 6 octets : trois `s16`. Trente-deux codes écrivent une fenêtre chacun,
et **six codes en écrivent plusieurs d'un coup** :

| Code | Fenêtres écrites |
|---:|---|
| 5 | #0, #1, #2, #3, #4, #6 (trois triplets différents) |
| 11 | #2, #3, #4 |
| 20 | #10, #11, #12 |
| 26 | #15, #16, #17 |
| 32 | #20, #21, #22 |
| 40 | #27, #28, #29 |

Les groupes de trois consécutives évoquent le triplet haut / milieu / bas du jeu, mais
**rien ne le prouve** : aucun consommateur de ces fenêtres n'a pu être localisé, l'état étant
incorporé dans `ROB` à l'offset `0x798` et les offsets `0x154`+ étant trop banals pour un
balayage. Le **rôle de chaque fenêtre reste UNKNOWN**.

Dans les données, seules les fenêtres #0 à #8 et #10 à #14 sont jamais renseignées, via les
codes 5, 10, 12, 13, 14, 15, 20, 21 et 22. Le code 5 accompagne les mêmes animations que le
code 3 (`KI`/`PU`) : ce sont les fenêtres temporelles du coup.

### 3.3 Les codes 45 et 46 — la prise, des deux côtés

Le code 45 est porté par **418 des 534 animations `NA`** (*nage*, la prise) et le code 46 par
**440 des 583 `YA`** (*yarare*, l'encaissement). Ils écrivent dans les mêmes champs d'état.

Code 45, charge de 24 octets :

| Champ | Type | Ce que c'est |
|---|---|---|
| `+0x00` | u32 | **identifiant de l'animation du partenaire** — 4 808 / 4 808 valides |
| `+0x08` | u16 | **dégâts**, mis à l'échelle par `0x180177CF0` puis `0x180177D20` (×1,25 sous condition) |
| `+0x0A` | s16 | repère de trame ; s'il est négatif, reprend `état+0x6C` |
| `+0x14` `+0x16` | s16 | deux repères de trame |
| `+0x04` `+0x0C` `+0x10` | u32 | UNKNOWN |

Les couples se lisent d'eux-mêmes une fois les noms résolus par `mot_db.bin` :

| Animation de l'enregistrement | Identifiant désigné |
|---|---|
| `AKI_HIKI2MAWA_NA` | `CMN_HIKI2MAWA_YA` |
| `AKI_HIKINA_NA` | `CMN_HIKINA_YA` |
| `AKI_NEW_NAGE_01_N` | `CMN_AKI_NEW_NAGE_01_Y` |
| `AKI_PG_ZENSOU2TEN_N` | `CMN_PG_ZENSOU2TEN_Y` |
| `AKI_SP_SENRIN_NA` | `CMN_COMBO01_YA` |
| `AK_BACK_NA` | `CMN_BACK_YA` |

### 3.4 Le code 0 — un tirage aléatoire pondéré

Le seul gestionnaire qui ne soit pas une recopie. Il ne s'exécute que si `état+0x54` vaut
encore `-1`, puis :

1. parcourt **le reste de la liste 1** en collectant toutes les entrées de code 0 ;
2. cumule le `u16` en `+0x16` de chaque charge — c'est un **poids** ;
3. tire un nombre au hasard (`0x1802CAC30`), le réduit modulo le poids total, et choisit
   l'entrée correspondante ;
4. recopie les six valeurs de la charge retenue en `état+0x54` … `0x68`.

Il est porté par **73 des 73 poses `VFX_RO`** (les poses d'introduction de round) et 77 des
127 `KAMAE` (les gardes).

**Ce qui est tiré au sort est la transition de fin d'animation.** Le champ `état+0x54` que ce
code écrit pilote un `switch` à six modes dans `0x180133010`, dont toutes les branches
appellent `0x180178A50` pour changer d'animation — le détail est en §4. Les six champs de la
charge utile sont donc nommés :

```
+0x00 s16  mode (0 a 5)                 -> etat+0x54
+0x04 u32  identifiant d'animation      -> etat+0x58   (mode 0)
+0x08 u32  option, bit 0 utilise        -> etat+0x5C
+0x0C u32  identifiant d'animation      -> etat+0x60   (mode 1)
+0x10 u32  option, bit 0 utilise        -> etat+0x64
+0x14 s16  seuil d'attente              -> etat+0x68   (mode 1)
+0x16 u16  poids du tirage
```

Répartition des modes sur le corpus : 0 → 652, 1 → 204, 2 → 4, 3 → 304, 4 → 464, 5 → 48.
Confiance : **CONFIRMED**.

### 3.5 Les autres codes nommés

| Code | Nom | Ce qui l'établit | Confiance |
|---:|---|---|---|
| 2 | saut | 113/131 des `JUMP` ; trajectoire trigonométrique | LIKELY |
| 47 | ajout dans un tableau | 5 cases de 8 o à `0x310`, case libre = `u16` −1 ; même famille que 65 | CONFIRMED |
| 49 | liste conservée | compte les entrées et garde le pointeur de la première | CONFIRMED |
| 50 | dégâts de rechange | écrit `0x8E` **et** `0x90` ; `0x1801423B0` choisit `0x90` selon l'état de la victime | SUPPORTED |
| 54 | orientation | angle binaire nié en miroir ; 600/606 des `TURN` | CONFIRMED |
| 56 | changement d'appui | 106/128 des `TASY` et `SYTA`, 424/606 des `TURN` | LIKELY |
| 58 | charge conservée | mémorise le pointeur des 48 octets sans les lire | CONFIRMED |
| 60 | drapeau *sabaki* | pose un bit et **ignore** ses 40 octets ; 16/31 des `SBK` (dont `SBK_PARING`) | LIKELY |
| 63 | mise en scène | 73/73 des `VFX_RO` | LIKELY |
| 64 | flottant à seuil | écrit seulement si > −1e−6 ; 7/8 des `WIN` | CONFIRMED (mécanique) |
| 65 | une condition parmi dix | 10 cases de 12 o à `0x3D0` ; `0x18017382C` les balaie et répartit sur le type (`+0x08`, valeurs 0, 1, 5) par une table de six cas (§3.11) | SUPPORTED |
| 73 | masque de réaction | *popcount* d'un `u32`, retouche le bloc *yarare* copié par le code 3 | SUPPORTED |
| 76–79 | volumes supplémentaires | 4 sous-blocs de 20 o ; 8/11 des `KAKATO` (coups de talon) | LIKELY |

Les codes **43, 44 et 71** n'ont pas de gestionnaire ici : ils ne passent par aucune table et
sont réclamés à la demande. Voir §3.9.

**Six des 51 codes de liste 1 employés restent `UNKNOWN`** (61, 62, 67, 74, 75, 80 — voir
§3.7, §3.8 et §3.9) : leur mécanique est décrite dans le CSV
(quels champs de charge, quels champs d'état, quels appels), mais rien ne permet encore de
les nommer.

### 3.6 Les codes de la liste 2

La liste 2 n'a **pas de table de répartition** : chaque code est cherché directement par les
fonctions qui en ont besoin, via `MothFindPayload` (§4) ou une boucle écrite en ligne. Seize
codes sur 44 se laissent qualifier ; le détail et la méthode sont en §3.10.

| Code | Ce que c'est | Ce qui l'établit |
|---:|---|---|
| 2 | angle de rotation, daté | ses 114 valeurs sont des angles binaires 16 bits ; `TURN` 601/606 |
| 4 | sélecteur temporel | `0x180146E30` compare le champ trame de chaque entrée à la trame courante |
| 5, 6, 30, 31 | jalons de trame purs | **jamais** de charge utile ; le code 6 est lu par `0x18014F140` qui convertit sa trame en flottant pour un calcul de trajectoire |
| 7 | angle et deux flottants | `UK` (*ukemi*) 21/22, `JUMP` 21/131 |
| 11 | valeur cumulée dans `état+8` | `0x1801651D0` la parcourt et additionne le `u16` |
| 14, 27 | les mouvements de boisson de Shun | `DRINK` 6/20, `NOMI` 9/36, `SHU` 15/270 |
| 17, 30, 31 | collision murale | `KABE` (mur) 50/107, 15/107, 25/107 |
| 18 | bifurcation datée vers une autre animation | `+0x08` = identifiant valide 2 096/2 096 ; `CATCH` 20/88 |
| 19 | cible d'animation | `+0x04` = identifiant valide 160/160 |
| **26** | **le numéro de posture** | `0x180178FC0` l'écrit dans `ROB+0x554` ; ses 474 valeurs sont exactement `[0, nposture-1]` du personnage (§3.10) |
| 32 | esquive latérale | `DFF` (`TA_MOVE_DFF_L` / `_R`) 42/44 |
| 51 | distance | `FAR` 44/45, `OFF` 90/192 |

Le champ *trame* va de 0 à 280 et croît le long de chaque liste : c'est bien une chronologie.

### 3.7 Les lecteurs des champs d'état

> **Les offsets d'état donnés dans cette section et les suivantes valent pour le build
> R.E.V.O. (2025).** Ils ne sont pas les mêmes dans la famille arcade : le portage a remplacé
> deux `std::vector` par des tableaux de taille fixe, ce qui décale tout ce qui suit.
> À partir de `état+0x310` il faut retrancher `0x18`, et à partir de `état+0x3D0` retrancher
> `0x78`. Vérifié sur les 84 gestionnaires des deux binaires et confirmé à l'exécution :
> `analysis/INSTRUMENTATION.md` §4.4.

Une fois su que l'état vit à `ROB+0x798` (§4), on peut chercher **qui lit** le champ que
chaque gestionnaire écrit : un accès `[reg + 0x798 + X]` vise le champ `X`. Le relevé complet
— offset, code, fonction, site, lecture ou écriture — est dans
`analysis/mothead_state_readers.csv` (1 274 lignes, 210 offsets, 667 lectures) ; les
désassemblages qui suivent sont dans `analysis/disasm_mothead_readers.txt`.

Deux fonctions écrivent presque tous les champs et ne servent qu'à les recopier —
`0x1802A2B80` (59 champs) et `0x1802A5080` (23 champs) : ce sont des sérialiseurs, pas des
consommateurs. Elles sont utiles à un autre titre : elles **confirment l'inventaire des
champs** déduit des gestionnaires.

#### Codes 52 et 53 — deux masques de 64 bits croisés par le niveau d'attaque

`0x18013FF80(attaquant, cible)` est le nœud :

```
0x18013FF86  mov    r10, [rdx+0xB00]        ; etat+0x368 de la CIBLE      (code 53)
0x18013FF97  and    r10d, [rcx+0xAF8]       ; etat+0x360 de l'ATTAQUANT   (code 52)
0x18013FFA8  and    r11d, [rcx+0xAFC]       ; etat+0x364
0x18013FFB4  movsxd rax, [rcx+0x820]        ; etat+0x88 = le NIVEAU d'attaque
0x18013FFBB  lea    rcx, [0x18063D060]      ; table indexee par le niveau
0x18013FFCC  movsxd r8, [rcx+rax*4]         ; numero de bit
0x18013FFD8  shl    ebx, cl                 ; 1 << (bit & 31)
0x18013FFDA  test   [rdx+r8*4+0xB00], ebx   ; ce bit est-il mis chez la cible ?
             ... puis popcount SIMD du ET des deux masques
```

Les deux `u32` du code 52 forment donc un **masque de 64 bits porté par l'attaquant**, ceux du
code 53 **le masque de la cible**, et le bit examiné est choisi par le **niveau d'attaque**.
`0x180141350` teste d'abord le bit 29 du masque attaquant avant d'appeler.

La table `0x18063D060` ne rend que quatre bits distincts pour les quinze niveaux :

| Niveaux | Bit testé |
|---|---:|
| 1, 7 | 24 |
| 2, 4, 14 | 25 |
| 3, 5, 6, 12, 13 | 26 |
| 0, 8, 9, 10, 11 | 36 |

C'est **la confirmation indépendante du niveau d'attaque** : les quinze valeurs du champ
`+0x06` du code 3 se regroupent en quatre catégories, et le regroupement `1` / `2` / `3`
retrouve exactement la partition haut / milieu / bas obtenue par les noms d'animations
(§3.1). Le bit 36 n'est **jamais** mis dans les données du code 53 : les niveaux qui s'y
rattachent — dont le niveau 0 et les niveaux 8 à 11, ceux que `0x1801423B0` traite déjà à
part — ne passent donc jamais ce test. Confiance sur les deux masques : **SUPPORTED** ;
l'interprétation « garde » reste **LIKELY**.

#### Code 59 — un décalage d'angle

`0x1801651D0` lit `état+0x3B8` et l'ajoute **à la fois** à `état+0x98` (l'angle du coup, écrit
par le code 3) et à `état+0x374` (l'orientation, écrite par le code 54) :

```
0x180165337  movzx ecx, word [rbx+0x3B8]
0x180165346  add   cx, word [rbx+0x98]
0x18016534D  add   ax, word [rbx+0x374]
```

Ces deux champs sont des angles binaires 16 bits déjà établis : le code 59 en est donc un
troisième, appliqué en décalage aux deux. Confiance : **SUPPORTED**.

#### Codes 4, 69, 72, 82

| Code | Ce que le lecteur montre | Confiance |
|---:|---|---|
| 4 | deux `f32` ; `0x180162B90` les initialise à **1.2** et **1.0**, les données ne contiennent que des valeurs rondes (1.5, 1.3, 2.0, 0.8 ; 1.0, 0.6, 0.75), et `0x18013E030` applique le second en facteur à un entier converti en flottant → **deux coefficients** | LIKELY |
| 69 | `0x18014F2CD` lit `état+0x450` en **masque de bits** : *popcount*, puis `mov eax,[rsi+rdx*4+0xBE8] ; bt eax,ecx` | SUPPORTED |
| 72 | trois `f32` lus par `0x180132AEB`, multipliés par un sinus/cosinus et **soustraits d'un triplet de position** ; les données donnent `(0, 0, 0.02 … 0.07)` → **un petit déplacement sur un axe** | LIKELY |
| 82 | deux `u16` que `0x180143490` **additionne** à des valeurs calculées (`add di, [rsi+0xC9A]`) | LIKELY |

#### Les dix codes qui restaient

Seize codes étaient encore `UNKNOWN` à ce stade. Six d'entre eux — **43, 44, 61, 62, 67,
71** — n'écrivent aucun champ d'état : la méthode ne s'y applique pas. Les dix autres sont
traités en §3.8.

### 3.8 Les dix derniers codes qui écrivent un champ

Sept des dix se sont laissés qualifier ; trois gardent leur type mais pas leur sens.
Désassemblages : `analysis/disasm_mothead_readers2.txt`.

#### Deux nouveaux champs d'identifiant d'animation

**Code 55** — le champ `+0x04` vaut `-1` dans 211 cas sur 251 ; les 40 autres sont **tous** des
identifiants valides du bon personnage, et les couples se lisent seuls :

| Animation de l'enregistrement | Identifiant désigné |
|---|---|
| `CMN_K_LFLG_YORO` | `CMN_K_LFLG_KAI` |
| `CMN_K_URG_YORO` | `CMN_K_URG_KAI` |
| `CMN_AT_SRCHU` | `CMN_S_SRCHUKAI` |
| `CMN_S_SLJAK` | `CMN_S_SLJAKKAI` |

`YORO` est le chancellement (*yoroke*), `KAI` le dégagement (*kai*, 解). Le code 55 relie donc
une animation de chancellement à **son animation de sortie**, ce qui recoupe son profil
lexical (`YORO` 19/43, `OKOSHI` 8/18). Ses autres champs : `+0x00` ∈ {1, 2, 4},
`+0x0C` ∈ {0, 10}, `+0x0E` = `-1` ou 15 à 34 — des trames. Confiance : **SUPPORTED**.

**Code 83** — le gestionnaire ne lit que **8 octets**, pas les 100 que l'écart entre charges
laissait croire :

```
0x180162B60  mov eax, [rdx]          ; +0x00
0x180162B66  cmp eax, -1
0x180162B6B  mov eax, [r8]           ; si -1 : etat+0x00, l'animation COURANTE
0x180162B6E  mov [r8+0x504], eax
0x180162B7D  mov eax, [rdx+4]        ; sinon +0x04 -> etat+0x508
```

Dans les données, **36 valeurs sur 36** sont des identifiants du personnage, et les couples
sont systématiquement les quatre variantes directionnelles pointant vers la variante `_F` :

```
CMN_LITTLE_BOUND_AO_{B,F,L,R}  ->  CMN_LITTLE_BOUND_AO_F
CMN_YAR_DWN_FENCE_{B,F,L,R}    ->  CMN_YAR_DWN_FENCE_F
```

C'est **l'animation de référence du groupe directionnel**. Confiance : **SUPPORTED**.

#### Un troisième masque de 64 bits — code 68

`0x1801405D0` lit `état+0x454` exactement comme `0x18013FF80` lit ceux des codes 52 et 53 :

```
0x1801406BF  mov  ecx, [rbx+0xBEC]          ; etat+0x454
             ... popcount ...
0x18014078F  mov  eax, [rbx+rdx*4+0xBEC]
0x180140796  bt   eax, ecx
0x18014079F  mov  rcx, [rbx+0xBEC]          ; le qword 0x454+0x458
0x1801407A9  and  eax, ecx
```

Et cette même fonction lit aussi le masque du code 52. Les valeurs de `+0x00`
(`0x03000021`, `0x04000012`, `0x030D0000`) portent bien les bits 24 et 25, ceux de la famille
haut/milieu/bas. Suivent sept paramètres : deux `u16`, un `u16` de défaut **100**, un `s8`
toujours 1, un `s16` en flottant, un coefficient de défaut **1.0f** (valeurs 0.5 et 0.25) et un
`u32` (42 ou 362). Confiance : **SUPPORTED** sur le masque.

#### Trois mécaniques établies

| Code | Ce que le lecteur montre | Confiance |
|---:|---|---|
| 70 | `+0x00` vaut toujours 1 ; `+0x02` ∈ {1, 2, 3} est relu en octet, **nié**, puis `0x180177C20` fait `ROB+0x588 += valeur` : le code **retranche 1 à 3 de ce compteur** | SUPPORTED |
| 66 | `0x18013C9FF` lit `état+0x448` et, s'il vaut `-1` (le défaut), prend `ROB+0x4E6` à la place : **une valeur qui écrase un défaut**. Données : 20, 21, 25, 35, 40 | LIKELY |
| 51 | `0x18014FAD0` relit `état+0x350` et `+0x354` en flottants à côté de `ROB+0x5A0`, dans le module du calcul de trajectoire `0x18014F140` : **des paramètres de trajectoire**. Données : `+00` ∈ {0,1,2,3,5,999}, `+02` de 20 à 60, `+04` = `-1` ou 37 à 80 | LIKELY |

#### Code 81 — une requête déposée dans un singleton

Le gestionnaire lui-même trahit sa destination : si le bit 2 des drapeaux est mis, il **saute
dans `0x180141CA0`**, qui recompose les six champs en une structure de 24 octets et appelle
`0x18004CF30` :

```
0x18004CF30  mov     rax, [0x1806B84C0]
0x18004CF37  vmovups xmm0, [rcx]
0x18004CF3B  vmovups [rax+0xA4], xmm0
0x18004CF43  vmovsd  xmm1, [rcx+0x10]
0x18004CF48  vmovsd  [rax+0xB4], xmm1
0x18004CF50  mov     byte [rax+0xA0], 1     ; requete en attente
```

Le module qui détient ce singleton (`0x180049000`–`0x180050000`) porte la chaîne
**`NAGE_VF4`** — un nom de caméra de prise à la manière de VF4. Les valeurs vont dans ce sens :
trois flottants ronds (3.0, 2.0, 4.0 le plus souvent), un entier de 25 à 130, et `-1` ou 40.
Confiance : **LIKELY**.

#### Ce qui garde son type mais pas son sens

| Code | Type établi | Pourquoi ça s'arrête là |
|---:|---|---|
| 74 | un `f32` dont le gestionnaire **force le signe positif** ; défaut 0.05, valeurs 0.03 à 0.08 | les deux seuls sites trouvés sont des recopies de bloc (`vmovaps`) |
| 75 | un `s16` converti en flottant, **valeur unique 9** dans tout le corpus ; défaut `-1.0f` ; `0x1801440EC` ne s'en sert que s'il est strictement positif | une seule valeur : rien à corréler |
| 80 | un `s16` en flottant (toujours 80) et un `u32` qui vaut `-1.0f` | le seul lecteur trouvé lit le qword `0x4E0` comme un compteur de boucle, ce qui **contredit les types** : c'est un faux positif, écarté |

**Neuf codes de liste 1 restent donc `UNKNOWN`** : 43, 44, 61, 62, 67 et 71 n'écrivent aucun
champ d'état — la méthode ne s'y applique pas ; 74, 75 et 80 en écrivent un dont le type est
connu mais dont aucun lecteur exploitable n'a été trouvé.

### 3.9 Les codes 43, 44 et 71 — il n'y a pas de second répartiteur

Les trois entrées nulles de la table `0x1804210D0` s'expliquent simplement : **ces codes ne
passent par aucune table**. Ils sont réclamés à la demande, par deux moyens.

**`0x180164720` est un chercheur générique**, et non le chercheur de liste 2 que la §4
décrivait d'abord. Son deuxième argument choisit la liste :

```
0x180164726  cmp  edx, 1
0x180164730  jne  0x18016476D          ; -> liste 1
0x180164732  call 0x180164400          ; liste 2 : enregistrement+0x18, pas de 12
0x18016476D  call 0x180164400          ; liste 1 : enregistrement+0x14, pas de 8
             ... les deux boucles s'arretent sur un code negatif ...
0x1801647A7  lea  rcx, [rax+4]         ; epilogue commun : +4 pour la liste 1, +8 pour la 2
0x1801647AB  movsxd rdx, [rcx]
0x1801647B4  lea  rax, [rcx+rdx]       ; rend LA CHARGE UTILE, pas l'entree ; 0 si absente
```

Ses **38 sites d'appel** passent le code en immédiat : 0, 1, 2, 3, 18, 43, 45, 46, 47, 51,
55, 68 et 71. C'est donc la voie normale d'accès à la liste 1 en dehors du répartiteur —
et **uniquement** à la liste 1 : les 38 sites passent tous `edx = 0`, jamais 1 (§3.12).

Le second moyen est la **boucle écrite en ligne** dans la fonction consommatrice, comme
`0x1801401B0` le fait pour le code 44 :

```
0x1801401C4  call   0x180164400
0x1801401C9  movsxd r8, [rax+0x14]     ; l'offset de la liste 1
0x1801401E2  add    rbx, rax
0x1801401F5  cmp    eax, 0x2C          ; code 44
0x1801401FD  add    rbx, 8
```

#### Code 43 — l'angle et l'ampleur de la projection

`0x180143490` réclame la charge du code 43 puis en lit un `u16` en `+0x00` et un `f32` en
`+0x04` ; **si le code est absent, il retombe sur `état+0x500` et `+0x504`**, les champs
qu'écrivent les codes 82 et 83.

Les **13 valeurs du `u16` sont toutes des multiples de 256** — `0xCC00`, `0x3000`, `0x3200`,
`0x2400`, `0x1B00`, `0x1800` — c'est-à-dire des **angles binaires 16 bits**, comme ceux des
codes 3, 54 et 59. Le `f32` vaut 2.0, 0.12, 0.08, 0.03, 0.13, 0.1, 0.25 : une amplitude. Et la
même fonction lit `ROB+0x434`, le champ que `RobApplyHit` remplit avec la racine carrée des
dégâts.

Le profil lexical va dans le même sens : `FUTTOBI` (吹っ飛び, projection) 27/34, `KIRIMOMI`
(chute en vrille) 10/14, `AIR` 20/31, `DW` 33/235. Confiance : **SUPPORTED**.

#### Code 44 — un coefficient du même domaine

`0x1801401B0` en lit le `f32` en `+0x00` (`-1.0`, ou 0.5 à 0.9) et le `u32` en `+0x0C` (bits 0
à 16). Même domaine que le code 43 : `AIR` 10/31, `FUTTOBI` 8/34, `AO` 7/63, `DOWN` 8/94.
Confiance : **LIKELY**.

#### Code 71 — un marqueur dont la charge est constante

Deux consommateurs, tous deux par `MothFindPayload` :

- `0x180179430` compare son `u16` à une valeur et pose un octet de drapeau si elle correspond,
  puis appelle `0x180081A70` avec l'index `0x1D` ;
- `0x18009C01B` **incrémente deux compteurs bornés** en `ROB+0x1A0` et `ROB+0x290`.

Le `u16` vaut **0 dans les 649 emplois** du corpus : seule la présence du code compte, et rien
de plus n'est déductible des données. Confiance : **SUPPORTED** sur la mécanique, le sens du
marqueur restant ouvert.

### 3.10 La liste 2 — les consultations d'appoint

**Correction, 2026-09-02.** Cette section affirmait que la liste 2 n'a pas de table de
répartition. **Elle en a une** : voir §3.11. Ce qui suit reste exact, mais ne décrit que la
seconde voie d'accès.

Douze fonctions consultent la liste 2 **hors frise**, en passant par le champ `+0x18` de
l'enregistrement obtenu par `MothGetRecord`, pour demander « cette animation a-t-elle un code
tel ? » sans attendre sa trame. Entre elles, elles cherchent sept codes — 3, 4, 6, 11, 18, 26
et 34. Le relevé des sites est dans `analysis/mothead_list2_consumers.csv`. Ces sept codes ont
donc **deux** voies de lecture ; les 37 autres n'ont que la frise, ce qui les avait fait
croire inertes.

Faute de consommateur pour la majorité, la charge utile de **chacun des 44 codes** a été typée
sur les données ; c'est désormais dans la colonne `description` de
`analysis/mothead_opcodes.csv`. Quatre codes se sont laissés qualifier.

#### Code 26 — le numéro de posture

`0x180178FC0` charge la posture courante depuis `ROB+0x554`, puis cherche le code 26 dans la
liste 2 et, s'il le trouve, **remplace la posture par le premier octet de sa charge** :

```
0x180179038  movzx esi, byte [rbx+0x554]     ; la posture courante
0x18017903F  call  0x180164400               ; MothGetRecord
0x180179044  movsxd rdx, [rax+0x18]          ; la liste 2
0x180179065  cmp   eax, 0x1A                 ; code 26
0x18017907C  movzx esi, byte [rax]           ; <- la charge remplace la posture
```

`ROB+0x554` est exactement l'argument *posture* que `0x180147680` passe ensuite à
`GetMotionForRole` (§4). La vérification sur les données est sans appel : les **474 valeurs du
code 26 tombent toutes dans `[0, nposture-1]`** du personnage, tel que `rob_cmn_mottbl.bin`
donne ce nombre :

| | LEI | SHU | KAG | VAN | DUR | LAU | SAR | AKI, JEF, LIO, WOL… |
|---|---|---|---|---|---|---|---|---|
| postures (`rob_cmn_mottbl`) | 7 | 6 | 3 | 3 | 2 | 2 | 2 | 1 |
| valeurs du code 26 | 0–6 | 0–5 | 0–2 | 0–2 | 0–1 | 0–1 | 0–1 | 0 |

Aucune exception sur 474. Confiance : **CONFIRMED**. C'est le troisième point de jonction
entre `mothead` et `rob_cmn_mottbl.bin`, après le rôle et l'identifiant d'animation.

#### Code 2 — l'angle de rotation, daté

Les **114 valeurs** de sa charge de 2 octets sont des angles binaires 16 bits :
`0xC000` (270°) 4 252 fois, `0x4000` (90°) 2 660, `0x8000` (180°) 2 546, puis `0x2000` (45°),
`0xE000` (315°), `0x1555` (30°). C'est le **pendant daté du code 54 de la liste 1**, et il est
porté par 601 des 606 animations `TURN`. Confiance : **SUPPORTED**.

#### Codes 4 et 7

`0x180146E30` reçoit la trame courante en `xmm1`, parcourt la liste 2 à la recherche du
code 4, **compare le champ trame de chaque entrée à la trame courante** et retient la dernière
passée — ce qui confirme au passage, côté code, que le deuxième champ d'une entrée de liste 2
est bien une trame. Le code 4 est donc un **sélecteur temporel**. Confiance : **LIKELY**.

Le code 7 porte un angle binaire en `+0x00` (`0x8000`, `0`, `0xC000`, `0x4000`) puis deux
flottants : un petit (0.005 à 0.07) et un grand signé (−4, −35, −5, 20). Porté par 21 des 22
`UK` (*ukemi*, la roulade de récupération) et 21 des 131 `JUMP`. Confiance : **LIKELY**.

#### Ce que le typage des données donne pour les autres

Quelques régularités valent d'être notées, même sans consommateur :

- **codes 21, 22, 24 et 52** n'apparaissent **qu'à la trame 0** (5, 19, 382 et 50 entrées) :
  ce sont des propriétés statiques rangées dans la liste datée.
- **codes 15 et 16** ont la même forme curieuse : le `u16` bas vaut toujours 0 et la valeur
  utile est le `u16` haut, qui vaut 1, 2 ou 3.
- **code 33** : son troisième champ vaut `1.0f` dans 2 848 cas sur 2 900 — un coefficient.
- **code 10** : toutes ses valeurs sont des multiples de 5 (0, 5, 10, 15, 20, 30).
- **code 13** : trames 1 à 30 seulement, et son troisième champ vaut 120 dans 816 cas sur 900.
- **code 9**, le code le plus employé du format (22 684 entrées), tient dans un `u16` de 0 à
  15 et **n'a aucun consommateur retrouvé**.

**Vingt-huit des 44 codes de liste 2 restent `UNKNOWN`.** Le format de leur charge est
maintenant établi pour tous ; ce qui manque est le site qui les lit.

### 3.11 Les codes 0 et 9 : trouvés — et pourquoi ils avaient échappé

**Correction, 2026-09-02.** La version précédente de cette section concluait qu'aucun
consommateur n'existait pour les codes 0 et 9, après cinq voies épuisées. **C'était faux, et
les cinq voies expliquent pourquoi** : elles cherchaient toutes une *comparaison* du code.

Il existe un répartiteur de liste 2, et il **n'a jamais comparé un code** :

```
MothRunList2   APM3 0x180152CE0        R.E.V.O. 0x18015D3A0
  rdx = [etat+0x498]                   ; le CURSEUR de parcours
  ebx = (int)xmm2                      ; la trame courante
boucle:
  if ([rdx+4] > ebx) sortir            ; entree pas encore echue
  rax = (s32)[rdx]                     ; le CODE
  if (rax >= 0x37) passer              ; 55 codes
  r10 = table[rax].gestionnaire        ; INDICE, pas comparaison
  if (r10) {
      if (table[rax].drapeau & 1 && ebx > 0 && ebx - [rdx+4] > 1) passer
      charge = [rdx+8] ? &[rdx+8] + [rdx+8] : NULL
      r10(&ctx + table[rax].delta, charge, rdx)
  }
passer:
  rdx += 12 ; [etat+0x498] = rdx       ; le curseur AVANCE et reste avance
  if ((s32)[rdx] >= 0) recommencer
```

Trois choses en découlent, et chacune annule une des cinq voies :

1. **Le code est un indice de table, jamais une valeur comparée.** Chercher
   `cmp r32, K` ou `test r32, r32` ne pouvait donc rien rendre (voie 2), et
   `MothFindPayload` n'a effectivement rien à voir avec la liste 2 (voie 1).
2. **La répartition se fait par `call r10`, pas par un saut indirect.** La voie 4 cherchait
   un saut : il n'y en a pas, et il n'en fallait pas.
3. **Le parcours ne lit pas le pointeur de base `état+0x518`, mais un curseur voisin,
   `état+0x510`** (APM3 : base `0x4A0`, curseur `0x498`), que `0x18015D490` (APM3
   `0x180152DE0`) remet à la base à chaque installation d'enregistrement. La voie 3 n'a
   examiné que le champ de base, et a conclu à juste titre que personne ne le relit : le
   lecteur est le champ d'à côté.

**La liste 2 est donc une frise chronologique**, consommée une fois, dans l'ordre des trames,
le curseur ne revenant jamais en arrière — et non un dictionnaire qu'on interroge par code.
Le drapeau `+0x18` bit 0 de la table (codes **0, 1, 8, 25 et 31**) signifie *n'agit qu'à la
trame exacte* : si la trame courante a dépassé l'entrée de plus d'une unité, l'entrée est
sautée sans rattrapage. Cela n'a de sens que pour une frise.

**La table compte 55 entrées de 32 octets** — `0x180648840` sur APM3, `0x180641350` sur
R.E.V.O. — et **les 55 ont un gestionnaire** dans les deux builds, avec le même profil de
drapeaux. Sur APM3 elle est remplie à l'exécution par l'initialiseur `0x180003D30` (elle est
nulle dans le fichier) ; sur R.E.V.O. elle est complète dans le fichier. Relevé complet :
`analysis/mothead_liste2_gestionnaires.csv`.

Contrôle sur les données, les 104 fichiers des quatre jeux : **le code de liste 2 le plus
grand rencontré est 54**, exactement la borne du répartiteur.

#### Code 0 — un effet sonore daté. CONFIRMED

Le gestionnaire (`0x180154D60`) teste la charge, puis appelle `0x1801879C0`, qui borne son
argument à `0x19A = 410` et rend `table_0x180401730[charge]` : **un tableau de 410 noms de
sons**, `fd_gard00`, `fd_punch_00`, `fd_kick_01st`, `fd_jump_00`, `fd_LANDING_GROUND_LAU`,
`fd_vfxse_hone01`… Le nom part ensuite dans `0x180185C20(catégorie = 2, nom)`.

Sur tout le corpus : **16 089 charges, 71 valeurs distinctes, toutes entre 1 et 391** — aucune
hors de la table. Et le gestionnaire a été **vu s'exécuter en combat**, sur l'entrée
`code=0 trame=114`, charge `13` = `fd_down0244`.

#### Code 9 — un commutateur de bits daté. CONFIRMED

Le gestionnaire (`0x180154A20`) borne la charge `u16` à 17 et saute dans un commutateur de
**18 cas** qui pose ou efface un bit du masque `état+0x4A8` (`ROB+0xD48`) :

| charge | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| effet | `=1` | efface bit 0 | `\|2` | `\|4` | `=0` | `\|8` | `\|0x10` | `\|0x20` | `\|0x40` | `\|0x80` | `\|0x100` | `\|0x200` | `\|0x400` | `\|0x800` | `\|0x1000` | `\|0x2000` | `\|0x8000` | `\|0x10000` |

Sur tout le corpus : **28 224 charges et exactement 18 valeurs distinctes, 0 à 17** — la borne
du commutateur, et pas une valeur de plus. Vu s'exécuter en combat.

C'était le code le plus employé du format (22 684 entrées) ; il est maintenant établi.

#### Ce que la recherche a trouvé au passage : le consommateur du code 65

`0x18017382C` semblait chercher les codes 2, 3 et 5 dans une liste de pas 12. C'est un **faux
positif**, et instructif :

```
0x18017383B  lea   rdx, [rbx+0xB68]      ; 0xB68 = 0x798 + 0x3D0
0x180173854  cmp   byte [rdx], 0xFF      ; case libre ?
0x180173859  movsx rax, word [rdx+8]     ; le type
0x18017385E  cmp   eax, 5 ; ja skip
0x180173863  mov   ecx, [0x180173A04 + rax*4]
0x18017386E  jmp   rcx                   ; table de six cas
0x1801738B7  add   rdx, 0xC
0x1801738BB  cmp   r8, 0xA               ; dix cases
```

`0x3D0` est le tableau que remplit le **code 65 de la liste 1**. Ce fragment le balaie, saute
les cases libres et répartit sur le mot en `+0x08` par une table de six cas, chacun étant un
prédicat sur le contexte. Les données confirment la borne : ce champ ne vaut que **0, 1 ou 5**.
Le code 65 passe donc de « ajout dans un tableau » à **une condition de branchement parmi dix**.
Confiance : **SUPPORTED**.

Les deux lignes correspondantes de `analysis/mothead_list2_consumers.csv` sont marquées
`FAUX POSITIF`.

### 3.12 Ce que le répartiteur change pour la liste 2

La version précédente de cette section concluait : « le DLL ne cherche que sept des 44 codes
de la liste 2 ; les 37 autres, 78 % des entrées, ne sont jamais consultés ». **Cette
conclusion est retirée.** Elle reposait sur une prémisse fausse — que toute lecture de la
liste 2 passe par le champ `+0x18` de l'enregistrement, obtenu par `MothGetRecord`. Le
répartiteur, lui, lit le curseur rangé dans l'état, et n'appelle jamais `MothGetRecord`.

Ce qui reste vrai du relevé précédent : les **douze fonctions** de
`analysis/mothead_list2_consumers.csv` accèdent bien à la liste 2 par l'enregistrement, et
cherchent bien les codes 3, 4, 6, 11, 18, 26 et 34. Ce sont des **consultations d'appoint**,
hors frise : on demande « cette animation a-t-elle un code 26 ? » sans attendre sa trame. Sept
codes ont donc deux voies de lecture, les autres une seule.

État de la liste 2 après correction :

| | avant | après |
|---|---|---|
| codes avec un gestionnaire identifié | 7 sur 44 | **44 sur 44** (et 55 sur 55 dans la table) |
| entrées jamais consultées | 93 141 sur 119 173 | **aucune** |
| codes `UNKNOWN` | 28 | **0** |
| confiance des 44 codes employés | 1 `CONFIRMED`, 1 `SUPPORTED`, 14 `LIKELY`, 28 `UNKNOWN` | **15 `CONFIRMED`, 19 `SUPPORTED`, 10 `LIKELY`** |

Les 55 gestionnaires ont été lus un à un : rôle, champ écrit et forme de la charge dans
`analysis/mothead_liste2_roles.md`. Douze d'entre eux ont ensuite été **vus s'exécuter dans un
combat**, avec un instantané du `ROB` avant et après l'appel (`tools/oracle_liste2_vivant.py`)
— ce qui les fait passer de `LIKELY` à `SUPPORTED`. Six codes s'y révèlent porter une **trame
de fin** dans le premier `u16` de leur charge : les codes 17, 29, 33, 51, 52 et 53, vérifiés
sur tout le corpus. Le résultat structurant est que **quatorze codes de la
liste 2 sont des codes de la liste 1 datés** : leur gestionnaire fait `add rcx, 0x18` et saute
dans le gestionnaire de liste 1 correspondant. C'est pour cela que le contexte compte six
cases et non trois — les trois dernières rejouent la convention de la liste 1.

| code de liste 2 | 36 | 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| code de liste 1 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 52 | 58 | 65 |

Les codes 38 à 46 visent donc **les neuf premières fenêtres temporelles** : la liste 1 les pose
à l'installation de l'animation, la liste 2 les repose à une trame donnée.

Pour le modding, la conséquence s'inverse : **tous les codes de la liste 2 ont un effet**, et
le travail restant est de lire 40 gestionnaires courts, tous rassemblés entre `0x180152DF0` et
`0x180155440` dans le build APM3.

Récit complet de la reprise : `analysis/liste2_repartiteur.md`.

## 4. Le code du moteur

Tout ce qui précède a été retrouvé dans `vf5fs-pxd-w64-d3d12_SteamRetail.dll` (R.E.V.O.),
qui porte le même moteur que l'arcade 6.000.

### `0x180164400` — la recherche par identifiant

```
0x180164515  mov  eax, [rcx+4]        ; id_min
0x180164518  cmp  eax, edi            ; identifiant demande
0x18016451A  ja   echec
0x18016451C  cmp  [rcx+8], edi        ; id_max
0x18016451F  jb   echec
0x180164521  movsxd rdx, [rcx+0Ch]    ; offset de la table
0x180164525  add  rcx, 0Ch
0x18016452D  lea  rsi, [rcx+rdx]      ; base de la table
0x180164531  sub  edi, eax            ; id - id_min
0x180164533  movsxd rax, [rsi+rdi*4]  ; entree
0x18016453B  test eax, eax
0x18016453D  je   echec
0x18016453F  add  rax, rcx            ; -> enregistrement
```

C'est **exactement** la structure du §2.1 et du §2.2. En cas d'échec la fonction rend un
enregistrement vide statique en `0x180641A88`, dont les trois offsets de liste sont nuls —
ce qui confirme aussi la disposition du §2.3. Confiance : **CONFIRMED**.

Une nuance de forme : dans le fichier, les offsets sont relatifs à `s1` ; **le chargeur les
convertit sur place en offsets relatifs au champ qui les porte** (`add rax, rcx` ci-dessus),
comme il le fait déjà pour `rob_cmn_mottbl.bin` (voir `mot_tables.md`). Le code lit donc la
forme relocalisée, `tools/mothead.py` lit la forme disque.

### `0x1801633C0` — le répartiteur de la liste 1

```
rbx = liste 1
  rdx = [rbx+4] ; charge utile ; si 0 -> fin
  rax = [rbx]   ; code ; si negatif -> fin
  r9  = [0x1804210D0 + rax*8]        ; table de gestionnaires
  si r9 : appel r9(contexte, charge, entree)
  rbx += 8
```

La table `0x1804210D0` compte **exactement 84 entrées** (codes 0 à 83) — la borne haute des
codes observés dans les données est 83. Elle a **une seule référence** dans tout le DLL, ici.
Trois entrées sont nulles (codes 43, 44, 71), pour des codes qui existent pourtant dans les
données : ce répartiteur les ignore, ils doivent être traités ailleurs.

Les adresses des 84 gestionnaires sont dans `analysis/mothead_opcodes.csv`, et **tous ont été
lus** : le résultat est la §3, le désassemblage complet est dans
`analysis/disasm_mothead_handlers.txt`. Quelques-uns, pris au hasard, corroborent les tailles
mesurées sur les données :

| code | taille mesurée | ce que fait le gestionnaire |
|---:|---:|---|
| 52 (0x34) | 12 | `0x180162170` : lit `u32 +0`, `u32 +4`, `s16 +8` |
| 54 (0x36) | 2 | `0x1801621C0` : lit `u16 +0`, le **nie** si un drapeau est mis, écrit en `état+0x374` |
| 64 (0x40) | 4 | `0x180162480` : lit un **flottant** en `+0`, le compare à une constante |
| 66 (0x42) | 4 | `0x1801624F0` : lit `u16 +0` et `s16 +2` |
| 47 (0x2F) | 8 | `0x180161E90` : parcourt 5 entrées de 8 octets de l'état |

La négation conditionnelle du code 54 et sa charge de 2 octets valant souvent `0x8000`
suggèrent un **angle binaire 16 bits** (`0x8000` = 180°) miroité selon le côté. Confiance :
**LIKELY**.

### `0x180164720` — la recherche d'une charge utile, dans l'une ou l'autre liste

```
cmp  edx, 1
jne  liste1
liste2 :  rax = enregistrement + 0x18 + [enregistrement+0x18] ; pas de 12
liste1 :  rax = enregistrement + 0x14 + [enregistrement+0x14] ; pas de 8
  les deux : ecx = [rax] ; si negatif -> fin ; si ecx == code cherche -> sortie
epilogue : rcx = rax + (4 pour la liste 1, 8 pour la liste 2)
           rdx = (s32)[rcx] ; si 0 -> rend 0
           rend rcx + rdx   ; LA CHARGE UTILE
```

Les deux pas et le terminateur négatif confirment le §2.4. **Cette fonction couvre les deux
listes**, selon son deuxième argument, et **rend la charge utile, pas l'entrée**. C'est la voie
d'accès normale à un code donné en dehors du répartiteur de la liste 1 : 38 sites d'appel,
les codes passés en immédiat étant 0, 1, 2, 3, 18, 43, 45, 46, 47, 51, 55, 68 et 71 (§3.9).

### `0x1801651D0` — l'installation d'un enregistrement

Recopie l'en-tête de 32 octets dans l'état du personnage et branche les trois listes :

```
etat[0x518] = liste 2                 etat[0x0C..0x18] = drapeaux 0..3
etat[0x960] = liste 3                 etat[0x4C] = drapeaux 4 ; etat[0x4E] = drapeaux 5
liste 1 -> passee a 0x1801633C0
bt drapeaux0, 8   -> etat[0x374] = 0x8000
bt drapeaux0, 21  -> etat[0x3B8] = 0x8000
```

Il parcourt ensuite la liste 2 à la recherche du **code 11**, dont la charge utile est un
`u16` accumulé dans `état+8`.

Enfin, `0x18014F140` cherche le **code 6** de la liste 2 et convertit son champ *trame* en
flottant pour un calcul de trajectoire (racine carrée, division) : c'est la confirmation
directe que le deuxième champ d'une entrée de liste 2 est bien une trame, et que le code 6
n'a pas de charge utile.

### Où vit l'état de mouvement, et qui le lit

`0x1801651D0` n'a **qu'un seul appelant**, `0x180178A50`, et celui-ci commence par :

```
0x180178A64  movzx eax, byte ptr [rcx+0x2EB4]
0x180178A6B  lea   rdi, [rcx+0x798]        ; <- l'etat de mouvement
```

`rcx` est le `ROB`, l'objet combattant. **L'état de mouvement que remplissent les 84
gestionnaires est incorporé dans `ROB` à l'offset `0x798`** — il n'est pas alloué à part et
personne ne le pointe : c'est ce qui rend les consommateurs difficiles à trouver par un
balayage d'offsets. Vingt fonctions du DLL calculent ce `+0x798`.

`0x180178A50` est le **point d'entrée du changement d'animation** d'un combattant : il
recopie `état+0x0C … 0x2B` dans `état+0x2C …`, appelle `0x180163C60`, puis `0x1801651D0`.
Confiance : **CONFIRMED**.

### `0x180163170` et `0x180162B90` — les remises à zéro

Deux fonctions du même module initialisent l'état, et **donnent les valeurs par défaut, donc
le type, de chaque champ** écrit par les gestionnaires :

`0x180163170` (`MothStateReset`) pose entre autres `état+0x54 = -1`, `état+0x344 = 0`,
`état+0x374 = 0`, `état+0x460 = 100`, `état+0x488 = 0.05f`, et **met à `-1` les cinq mots de
`0x310` à `0x330` par pas de 8** — exactement les cinq cases du tableau que remplit le code 47.

`0x180162B90` (`MothAttackReset`) efface les champs de l'attaque (`0x7C` à `0xA8`), **recharge
l'entrée `yarare` numéro 0** par `0x180166400` et la recopie en `0xAC` et `0xFC` — le même
geste que le code 3 —, puis initialise les 32 fenêtres :

```
0x180162C7C  mov [rbx+0x14C], 3F99999A     ; 1.2f
0x180162C86  mov qword [rbx+0x150], 3F800000 ; 0x150 = 1.0f, 0x154 = 0
0x180162C91  mov [rbx+0x15C], BF800000     ; -1.0f
0x180162C9B  mov [rbx+0x158], BF800000     ; -1.0f
0x180162CA5  mov [rbx+0x160], 0            ; fenetre suivante
0x180162CAB  mov [rbx+0x168], BF800000
0x180162CB5  mov [rbx+0x164], BF800000
     ... 32 fois, pas de 12 octets
```

Cela **établit l'ordre des trois champs d'une fenêtre** : `+0` vaut 0 par défaut, `+4` et `+8`
valent `-1.0f`. Confiance : **CONFIRMED**.

### `0x1801423B0` — l'application du coup, et la preuve des dégâts

```
0x1801423C5  lea   r13, [rcx+0x798]          ; rcx = attaquant, r13 = son etat
             rsi = ROB de la victime
0x1801423E6  movzx ecx, word [r13+0x90]      ; degats de rechange
0x1801423EE  movzx edx, word [r13+0x8E]      ; degats effectifs
             si 0x90 >= 0 et que la victime porte le bit 10, 11 ou 23 de ROB+0x7B4 :
0x18014241C    movzx edx, cx                 ; on prend 0x90
0x180142426  call  0x1801788D0(victime, ..., degats)
             puis xmm = sqrt(degats * k) * k' -> victime+0x434
```

`0x1801788D0` écrit la valeur reçue en `victime+0x430` et `+0x4C6`. Le champ `+0x08` du code 3
est donc bien **les dégâts**, et la secousse appliquée à la victime est proportionnelle à leur
racine carrée. Cela fait passer les dégâts de **SUPPORTED à CONFIRMED**, et nomme le code 50 :
il écrit `0x8E` **et** `0x90`, c'est-à-dire la valeur de rechange que ce site choisit selon
l'état de la victime.

### `0x180133010` — ce que le code 0 tire au sort

Le champ `état+0x54`, écrit par le code 0, pilote un `switch` à six cas (table de saut
`0x1801331C4`, valeur par défaut `-1` = ne rien faire). **Toutes les branches appellent
`0x180178A50`**, c'est-à-dire changent d'animation :

| Mode | Emplois | Ce que fait la branche |
|---:|---:|---|
| 0 | 652 | va à l'identifiant `état+0x58` (si ≠ −1), option `état+0x5C & 1` |
| 1 | 204 | va à `état+0x60` **quand le compteur `ROB+0x5BC` atteint le seuil `état+0x68`**, et seulement si les bits 19 et 20 des drapeaux 0 de l'enregistrement cible sont libres |
| 2 | 4 | résout un **rôle** selon le bit 5 de `ROB+0x338` |
| 3 | 304 | résout un rôle `0x8F` ou `0` selon le bit 0 de `ROB+0x33A` |
| 4 | 464 | rien ici — traité ailleurs |
| 5 | 48 | résout le rôle `0x49` si le bit 22 de `état+0x1C` est mis |

Le code 0 tire donc au sort, avec les poids que porte chaque entrée, **la transition de fin
d'animation**. Cela nomme ses six champs :

```
+0x00 s16  mode (0 a 5)                 -> etat+0x54
+0x04 u32  identifiant d'animation      -> etat+0x58   (mode 0)
+0x08 u32  option, bit 0 utilise        -> etat+0x5C
+0x0C u32  identifiant d'animation      -> etat+0x60   (mode 1)
+0x10 u32  option, bit 0 utilise        -> etat+0x64
+0x14 s16  seuil d'attente              -> etat+0x68   (mode 1)
+0x16 u16  poids du tirage
```

Le champ `+0x0C` n'est renseigné que 4 fois dans tout le corpus, et **les 4 valeurs sont des
identifiants d'animation valides du bon personnage** (`DMY_MUE_KUBI_HIZA2_YA_R` →
`CMN_KUBI_HAZUSI_Y`, un dégagement de prise à la nuque). Confiance : **CONFIRMED**.

### `0x180166240` — la jonction avec `rob_cmn_mottbl.bin`

Les modes 2, 3 et 5 passent par `0x180147680`, qui prend un **numéro de rôle**, lit la posture
en `ROB+0x554` et l'index du personnage en `ROB+0x10`, puis appelle `0x180166240`. Celui-ci lit
le global `0x180756E20` — celui qu'écrit `ParseRobCmnMotTbl` — et applique **exactement** la
structure décrite dans `mot_tables.md` :

```
0x180166245  mov  rax, [0x180756E20]        ; rob_cmn_mottbl
0x18016626C  cmp  ecx, [rax]                ; index de personnage < 21
0x180166275  cmp  r8d, [rax+4]              ; role < 363
0x18016627E  cmp  edi, [r10+rax*8+4]        ; posture < nb de postures de l'entree
0x180166297  movsxd rax, [rcx+rdi*4]        ; bloc[role]
```

La boucle du moteur de combat se referme donc sur elle-même :

```
mothead : enregistrement -> code 0 -> mode -> role
                                       |
                          rob_cmn_mottbl (perso, posture, role)
                                       |
                                identifiant d'animation
                                       |
                          0x180178A50 -> 0x1801651D0 -> enregistrement mothead suivant
```

Confiance : **CONFIRMED**. Désassemblage : `analysis/disasm_mothead_consumers.txt`.

### Les 32 fenêtres n'ont toujours pas de consommateur

Deux pistes ont été suivies et **écartées** : `0x18007E190` et le couple
`0x180070660` / `0x180070B36` touchent bien des offsets `0x154 + 12i`, mais sur d'autres
structures — la seconde travaille sur le global `0x1806B9788` avec ses propres tableaux
parallèles en `0xBC`, `0xC4`, `0x104`, `0x110`. Aucune fonction du DLL n'indexe
`état + 0x154 + 12·i`, et aucune de celles qui détiennent le pointeur d'état ne lit cette
plage. Le rôle des fenêtres reste **UNKNOWN**.

### Autres sites de consultation de la liste 2

| code | sites |
|---:|---|
| 1 | `0x180142563`, `0x180318518` |
| 3 | `0x1801AB458`, `0x1801AB4B0`, `0x1801AF236`, `0x1801AF280`, `0x18031832A` |
| 4 | `0x180146E81`, `0x180146EE0`, `0x180146F70`, `0x180146FE5`, `0x1801738A8` |
| 5 | `0x1801738AE` |
| 6 | `0x18014F190`, `0x1801AB410`, `0x1801FE120` |
| 11 | `0x180165390`, `0x1801653E0` |
| 18 | `0x180144F21`, `0x180144F81`, `0x1801AB680`, `0x1801ABC80`, `0x1801ABD60` |
| 19 | `0x1800CAA77` |
| 26 | `0x180144CA6`, `0x180144CF4` |
| 34 | `0x1801FE168`, `0x1801FE1C1` |

---

## 5. Section 2 — le bloc `CCD`

### En-tête, 32 octets

```
0x00  u32  magic       0xFF444343  =  'C' 'C' 'D' 0xFF
0x04  u32  header_size toujours 32
0x08  u32  c1          nombre d'enregistrements
0x0C  u32  c2          toujours c1 - 3
0x10  u32  pool_off    offset du pool de flottants, relatif au debut du CCD
0x14  u32  pool_size   taille du pool, en octets
0x18  u32  0xFFFFFFFF
0x1C  u32  0xFFFFFFFF
```

### Disposition

```
[0, 32)                     en-tete
[32, 32 + c1*8)             c1 enregistrements de 8 octets
[32 + c1*8, pool_off)       bourrage d'alignement (0 ou 8 octets)
[pool_off, pool_off+size)   pool de flottants
```

avec deux invariants :

```
pool_off            = align16(32 + c1 * 8)
pool_off + pool_size = taille de la section 2
```

**Vérifiés sur 85/85 fichiers, quatre versions.** Confiance : **CONFIRMED**.

Il y a exactement **un** marqueur `CCD\xFF` par fichier — aucun autre marqueur ASCII aligné
n'existe dans ces fichiers. Le magique n'est comparé nulle part dans le DLL.

### Les enregistrements de 8 octets

Deux `u32`. Le second prend souvent de petites valeurs (`0`, `3`, `4`, `8`, `0x0C`) ou
`0xFFFFFFFF`. Aperçu du début du CCD d'Akira :

```
(0x41, 0)  (0x123, 0)  (0x2E, 0x0C)  (0x3A, 0)  (0x2F, 0x0C)  (0x12B, 0)
(0x40, 0)  (0x12B, 8)  (0x12B, 4)    (0x25, 3)  (0x25, -1)    (0x25, 0)
```

Sémantique : **UNKNOWN**.

Volumétrie de `c1`, arcade 6.000 : de 1 907 (`KRT`) à 8 028 (`WOL`), 3 009 pour `AKI`.

### Le pool de flottants

Bloc final de 12 à 76 octets, soit 3 à 19 flottants IEEE-754 simple précision. Ce sont des
valeurs rondes : `0.0`, `2.3`, `10.0`, `15.0`, `9.0`, `6.0`, `3.0`, `-6.0`, `-9.0`, `2.0`,
`24.0` pour Akira.

**Ce n'est pas une structure : c'est un pool de constantes dédupliqué**, rangé dans l'ordre de
première utilisation. Trois observations le montrent :

1. sa longueur varie d'un personnage à l'autre (3 valeurs pour `KRT`, 19 pour `KAG`) ;
2. les premières valeurs sont les mêmes partout — `0.0`, puis `2.3`, puis `10.0` ;
3. quand une valeur change, les suivantes **se décalent d'un cran** au lieu d'être
   remplacées — comportement caractéristique d'une table reconstruite à la compilation.

Confiance : **SUPPORTED**.

---

## 6. Ce que les versions révèlent

### `2.000` (Rev A) → `6.000` (Rev B) : refonte des mouvements

- Aucun `mothead_` ne survit intact.
- Le nombre d'enregistrements CCD change (Akira : 3 001 → 3 009).
- **Le pool de flottants est inchangé pour 19 personnages sur 21.** Seules exceptions :
  `DUR` gagne six valeurs, `JEF` en perd une.

Autrement dit : la refonte Rev A → Rev B a réécrit les mouvements sans toucher aux constantes.

### `6.000` → `2.00` (R.E.V.O.) : une constante partagée, changée partout

Pour **les 21 personnages**, une même valeur `10.0` devient `13.0` dans le pool. Elle se
trouve à l'indice 2 pour la plupart, 3 pour `SHU`, 4 pour `CMN` et `DUR`, 6 pour `MON` —
l'indice dépend de l'ordre de première utilisation propre à chaque personnage.

Le cas d'Akira est le plus parlant : sur les **24 156 octets** de son bloc CCD,
**un seul octet diffère** entre l'arcade 2011 et R.E.V.O. 2025 — celui qui fait passer
ce flottant de `10.0` à `13.0`.

Chez les personnages qui utilisaient encore `10.0` ailleurs, la valeur est réinsérée plus loin
dans le pool et décale la suite (`JAK` : `10.0` réapparaît à l'indice 6, poussant sept valeurs
d'un cran ; idem pour `KAG`, `WOL`, `SAR`, `PAI`, `VAN`, `AOI`).

**Ce que cette constante représente est UNKNOWN.**

---

## 7. Le chargeur, côté code

Dans `vf5fs-pxd-w64-d3d12_SteamRetail.dll`, **une seule fonction** référence les chemins
`mothead_` : **`0x180164840`** (2 443 octets). Elle référence les deux variantes —
`./rom/rob/mothead_` (`0x180421380`) et `./rom_200/rob/mothead_` (`0x180421398`) — et
choisit entre elles sur un booléen reçu en troisième argument (`r8b`), testé à
`0x18016489A` :

```
0x18016489A  test bl, bl
0x18016489C  je   0x180164d32     ; bl == 0  ->  ./rom_200/rob/mothead_
0x1801648A2  lea  r10, [rip+…]    ; bl != 0  ->  ./rom/rob/mothead_
```

Le jeu de données de gameplay est donc sélectionné **à l'exécution, par un drapeau**, et non
par configuration de build. Même schéma pour `ctrl_` (`0x18005A910`). Confiance :
**CONFIRMED**.

Elle porte le message d'erreur `request_load_mhd_file(): illegal file_id(%d).` : le module
s'appelle **`mhd`** dans le code d'origine, et le DLL contient le type RTTI `UMhdFile`.

Cette fonction ne fait que **construire le chemin et déposer une demande** auprès du
gestionnaire de ressources (objet global `0x180756D78`). C'est `0x180164400` qui, plus tard,
rend l'enregistrement d'une animation à partir du tampon chargé.

Désassemblage : `analysis/disasm_mothead_loader.txt` (le chargeur) et
`analysis/disasm_mothead_section1.txt` (les quatre fonctions de la section 1).

---

## 8. Ce qui reste à faire

**Les deux verrous durs de ce document sont tombés le 2026-09-02.** Les deux tenaient à une
adresse de base fausse, pas à un manque de recherche.

1. ~~Le rôle des 32 fenêtres temporelles~~ — **ouvert**. L'état de mouvement est à
   `ROB+0x8A0` dans le build APM3, pas `ROB+0x798` : les consommateurs tiennent le ROB et
   adressent les fenêtres en ROB-relatif (`[rdi+0x9F8]`), d'où l'échec des recherches menées
   sur les offsets d'état. 115 accès flottants sur 15 fonctions, les 32 fenêtres touchées.
   Reste à **nommer** chaque fenêtre : `analysis/fenetres_temporelles.md`,
   `analysis/mothead_fenetres_sites.csv`.
2. ~~Les 37 codes de liste 2 que le DLL ne cherche jamais~~ — **ouvert**, et la conclusion
   était fausse. Il existe un répartiteur, `MothRunList2`, qui **indexe** une table de 55
   gestionnaires avec le code au lieu de le comparer, et qui lit un **curseur** voisin du
   pointeur cherché (`état+0x510` et non `0x518`). Les 55 codes ont un gestionnaire dans les
   deux builds ; les codes 0 et 9 sont établis. Voir §3.11 et
   `analysis/liste2_repartiteur.md`.
3. **Les codes 61, 62 et 67 de la liste 1**, qui n'écrivent aucun champ d'état : 61 a un
   gestionnaire hors module, 62 écrit sur `ctx[1]`, 67 transmet à `ROB+0x5D38`.
4. **Les codes 74, 75 et 80** : type établi, aucun lecteur exploitable.
5. **Le mode 4 du code 0 de la liste 1** (464 emplois, le plus fréquent) : la branche de
   `0x180133010` ne fait rien, il est donc traité ailleurs.
6. **Les six mots de drapeaux** de l'en-tête d'enregistrement. Deux bits sont localisés : les
   bits 8 et 21 du mot 0 posent `0x8000` dans deux champs de l'état.
7. **Le sens des masques de 64 bits** (codes 52, 53, 68) au-delà des bits 24 à 26 et 36, et
   les champs `+0x00`, `+0x0C`, `+0x18` et `+0x1C` du code 3.
8. **Identifier les paires de 8 octets du CCD.**
9. **Élucider la constante `10.0` → `13.0`** appliquée aux 21 personnages en 2.00.
10. `CCD` reste un sigle non résolu. Ne pas le développer sans preuve.

## Voir aussi

- `docs/formats/mot_tables.md` — `mot_db.bin` et `rob_mot_tbl.bin`, entièrement décodés.
- `docs/formats/farc.md` — le conteneur.
- `analysis/CHARACTERS.md` — correspondance des codes de personnage.
- `analysis/mothead_opcodes.csv` — inventaire des codes, tailles, gestionnaires.

## Outillage

```bash
py -3 tools/mothead.py info    <mothead.bin>
py -3 tools/mothead.py list    <mothead.bin> [<mot_db.bin>]
py -3 tools/mothead.py rec     <mothead.bin> <id> [<mot_db.bin>]
py -3 tools/mothead.py check   <fichier|dossier> ...
py -3 tools/mothead.py opcodes <fichier|dossier> ...
```

Exemple, un mouvement d'Akira lu de bout en bout :

```
$ py -3 tools/mothead.py rec .../mothead_AKI.bin 20155 .../mot_db.bin
animation 20155  AKI_TA_PG_JYUNHO_N
enregistrement s1+0x000280
  drapeaux  00280101 00000000 00000000 00000000   0000 0000
  liste 1 (3) :
    code  1 (0x01)  charge s1+0x00033C  090023004c00...
    code 45 (0x2D)  charge s1+0x000324  bc4e0000...        <- 0x4EBC = 20156 = CMN_TA_PG_JYUNHO_Y
    code 54 (0x36)  charge s1+0x000320  0080               <- 0x8000
  liste 2 (4) :
    code  0 (0x00)  trame   9  charge s1+0x0002EC
    code  1 (0x01)  trame  10  charge s1+0x0002E8
    code  2 (0x02)  trame  24  charge s1+0x0002E4
    code 12 (0x0C)  trame  30  charge s1+0x0002DC
```

Aucun fichier des dumps n'a été modifié : tout est lu depuis les sources en lecture seule.
