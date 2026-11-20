# Les polices et les pictogrammes de manette

Document de référence, mesuré le 2026-09-06. Tout ce qui suit a été lu dans les
fichiers ou vérifié à l'image ; rien n'est déduit d'une ressemblance.

---

## 1. Deux systèmes de texte, à ne pas confondre

| | `font_gothic.bin` | `spr_n_fnt32.farc` |
|---|---|---|
| nature | police bitmap brute, hors archive | planche de sprites, dans le `.par` |
| décrite par | rien : elle se suffit | `fontmap.bin` (FMH3) |
| adressage | le numéro de case **est** le codepoint | indice empaqueté `(rangée << 8) \| colonne` |
| compression | aucune, 1 octet par pixel | BC3 (DXT5) |
| glyphes | 7712 | 3669 + 127 |

`fontmap.bin` ne décrit **pas** `font_gothic.bin`. C'est le piège du chantier :
les deux sont des polices, les deux sont là, et les indices de l'un ne veulent
rien dire dans l'autre. La preuve tient en une ligne : `fontmap` donne l'indice
33 pour `A`, alors que `font_gothic` porte `A` en case 65 — c'est-à-dire à son
codepoint.

---

## 2. `font_gothic.bin` — la disposition, mesurée

7 766 016 octets, **aucun en-tête**, 247 valeurs distinctes (donc 8 bits par
pixel, une valeur d'alpha par octet — ce n'est pas du 4 bits).

La disposition ne se devine pas : trois essais à la vue ont échoué. Elle se
**mesure**, par autocorrélation sur les octets (`tools/mesurer_atlas.py`) :

```
pas    32 octets   0.7358      <- le pic
pas    64 octets   0.6364
pas    96 octets   0.5718
pas   128 octets   0.5224
pas  1024 octets   0.5172      <- bruit (0.50 = base)
```

Un pic à 32 avec ses multiples derrière, et rien à 1024 : les lignes font 32
octets **à l'intérieur d'une case**, et les cases sont bout à bout — pas de
rangée 2D. C'est pour cela qu'un rendu en « largeur de ligne » (2046, 2048,
2112…) ne donne jamais rien.

La planche est en **deux zones**, et c'est le second piège :

| zone | octets | case | nombre |
|---|---|---|---|
| demi-chasse | `0x00000`–`0x1FFFF` | 16 × 32 px, 512 o | 256 |
| pleine chasse | `0x20000`–fin | 32 × 32 px, 1024 o | 7456 |

La bascule est nette et se situe **exactement à la case 256**, soit l'octet
`0x20000`. Rendre toute la planche avec une seule taille de case donne un début
lisible puis de la bouillie — le symptôme exact observé.

Zone demi-chasse : 32 cases de garde, puis l'ASCII **à son codepoint**
(case 0x41 = `A`), puis les katakana demi-chasse. Zone pleine chasse : symboles,
grec, cyrillique, kana, kanji, ASCII pleine chasse.

    py -3 tools/planche_police.py --cases 0 128

---

## 3. `fontmap.bin` — le format FMH3

En-tête : magie `FMH3`, `+0x08` nombre de polices, `+0x10` la table des têtes.
Chaque tête :

| champ | sens |
|---|---|
| `+0x04` u8 ×4 | largeur/hauteur du glyphe, puis de la chasse |
| `+0x10` u32 | nombre de **colonnes** |
| `+0x14` u32 | nombre de glyphes |
| `+0x18` u32 | pointeur vers la table des glyphes |

Enregistrement de glyphe, 8 octets : `u16 codepoint`, `u16 texture`,
`u16 indice`, `u8 marge`, `u8 chasse`.

Les deux polices du fichier :

| | glyphe | chasse | colonnes | glyphes | texture |
|---|---|---|---|---|---|
| police 0 | 32×32 | 33×33 | 62 | 3669 | `spr_n_fnt32` tex0 (2048×2048) |
| police 1 | 48×48 | 48×48 | 21 | 127 | `spr_n_fnt32` tex1 (1024×512) |

**L'indice est empaqueté**, pas linéaire : `(rangée << 8) | colonne`. La
démonstration ne laisse pas de place au doute :

```
A       0x0021  -> rangée 0, colonne 33
a       0x0103  -> rangée 1, colonne 3     (la rangée 0 tient 62 colonnes,
                                            0x20..0x5D ; 0x5E,0x5F,0x60 puis a)
U+E00B  0x383D  -> rangée 56, colonne 61   <- la DERNIÈRE colonne
U+E00C  0x3900  -> rangée 57, colonne 0    <- et on repart à zéro
```

Le pixel du glyphe est donc en `(colonne × 33, rangée × 33)`, sur 32 × 32.

### 3.1 La disposition binaire du FMH3 — mesurée le 2026-10-09

Le fichier n'existe **que dans le `.par`**, et il y est **compressé en SLLZ** :
il n'y a pas de copie libre à ouvrir. `tools/echappements.py --fontmap` le sort
et le lit.

    0x00  'FMH3'
    0x08  u32  nombre de polices
    0x0C  u32  offset de la liste de pointeurs de polices

    une police :
    +0x04  u8 u8   largeur et hauteur de la CASE   (32, 32)
    +0x06  u8 u8   la CHASSE, pas de la grille     (33, 33)
    +0x10  u32     colonnes par rangée             (62)
    +0x14  u32     nombre de glyphes               (3669)
    +0x18  u32     offset de la table de glyphes

    une entrée de glyphe, 8 octets :
    +0x00  u16  le codepoint
    +0x02  u16  (0 pour tous les pictos)
    +0x04  u16  l'indice empaqueté `(rangée << 8) | colonne`
    +0x06  u8 u8  le chasse-avant et la largeur utile

Les deux polices : la 0 en `0x20` (32×32, 62 colonnes, 3669 glyphes, table en
`0x40`), la 1 en `0x7300` (48×48, 21 colonnes, 127 glyphes). **Aucun picto de
manette dans la seconde.**

---

## 4. Les conteneurs 2D

`rom/2d/*.farc` : magie `FArC`, en-tête **gros-boutiste**, entrées
`{nom\0, u32 offset, u32 taille compressée, u32 taille réelle}`, données gzip.

Dedans, un jeu de sprites contenant une pile TXP :

```
'TXP\x03'   u32 nombre, u32 groupe, u32[] offsets    le jeu de textures
  'TXP\x04'   u32 mips, u32 groupe, u32[] offsets      une texture
    'TXP\x02'   u32 larg, u32 haut, u32 format,
                u32 niveau, u32 taille, puis les octets
```

Formats rencontrés : 1 = RGB8, 2 = RGBA8, 6 = DXT1, 9 = DXT5. Les compressés se
lisent en collant un en-tête DDS de 128 octets devant les octets — Pillow fait
le reste, inutile d'écrire un décodeur BC. **Pillow rend le DDS de bas en
haut** : il faut retourner l'image.

    py -3 tools/txp.py --sortir toutes

---

## 5. Les pictogrammes de manette

Deux ressources bien distinctes.

### 5.1 Les pictos en ligne dans le texte — `spr_n_fnt32` tex0

Cinquante glyphes, `U+E000` à `U+E032`, aux **rangées 56 et 57** de la planche.
Ils s'écrivent dans les libellés comme des caractères ordinaires : la table de
textes contient par exemple `':Information  :Back  :Enter'`.

Ce que la planche porte, et c'est le point qui décide de tout :

| | contenu |
|---|---|
| `U+E000`–`E003` | **B, A, Y, X** — le jeu **Xbox 360**, pas PlayStation |
| `U+E004`–`E00B` | START, BACK, LB, LT (chacun sur deux cases) |
| `U+E00C`–`E013` | RB, RT, LS, RS |
| `U+E014`–`E018` | croix directionnelle, ○, ✕, △, □ — le jeu **PlayStation** |
| `U+E01A`–`E01C` | P, K, G (poing, pied, garde) |
| `U+E01D`–`E032` | flèches blanches, flèches rouges, rotations |

Autrement dit **le jeu Xbox 360 complet est déjà dans le binaire du jeu**, à
côté du jeu PlayStation. Passer aux boutons Xbox One / PS4 / PS5 ne demande donc
pas de système nouveau : c'est repeindre des cases de 32 × 32 à des coordonnées
connues, puis réencoder la texture en BC3.

### 5.2 Le schéma de manette — `spr_n_cmnps3`

Une seule texture, **512 × 512, RGBA8 NON compressée**, données à l'offset
`0xE8` du `.bin` (et `0xE8 + 512×512×4` fait exactement la taille du fichier).
C'est le dessin de la DualShock 3 avec ses traits de légende, celui de la page
des commandes.

Non compressée : on peut la remplacer pixel pour pixel, sans encodeur.

---

## 5.3 LA TABLE D'ÉCHAPPEMENTS — **c'est elle qui décide**, mesurée le 2026-10-09

**Et c'est le point que ce document ratait.** Les pictos de boutons des menus ne
viennent **ni** de la table de textes **ni** d'un choix de planche : le moteur
porte en `0x180534290` (offset `0x532E90`) une table de **paires
{glyphe UTF-8, nom}**, qu'il substitue dans les libellés.

**SEGA en a mis DEUX JEUX**, et c'est toute l'affaire :

| nom | glyphe | case | ce qu'il dessine |
|---|---|---|---|
| `ESC_BTN_CIRCLE` | `U+E000` | r56 c50 | le **B** Xbox |
| `ESC_BTN_CROSS` | `U+E001` | r56 c51 | le **A** |
| `ESC_BTN_TRIANGLE` | `U+E002` | r56 c52 | le **Y** |
| `ESC_BTN_SQUARE` | `U+E003` | r56 c53 | le **X** |
| `ESC_BTN_CIRCLE_PS3` | `U+E015` | r57 c9 | le ○ |
| `ESC_BTN_CROSS_PS3` | `U+E016` | r57 c10 | le ✕ |
| `ESC_BTN_TRIANGLE_PS3` | `U+E017` | r57 c11 | le △ |
| `ESC_BTN_SQUARE_PS3` | `U+E018` | r57 c12 | le □ |

Le reste de la table est **déjà Xbox** : `ESC_BTN_L1`–`R2` rendent LB, LT, RB,
RT (`U+E008`–`E00F`, deux cases chacun), `ESC_BTN_SELECT` rend BACK,
`ESC_BTN_START` le START ovale du 360. Viennent ensuite `ESC_BTN_P/K/G` et les
vingt-deux `ESC_STK_*` des notations de manche. **42 paires en tout.**

`tools/echappements.py` les relit et résout chaque glyphe jusqu'à sa case.

### Trois pistes qui ne mènent nulle part, et il faut le savoir

1. **La table de textes.** Vérifié sur les deux membres : **aucune** des 23 054
   chaînes ne porte un glyphe PlayStation (`U+E014`–`E018`). Les identifiants de
   l'écran Controls (`0x32F`–`0x332`) citent même déjà `U+E002`, `U+E000`,
   `U+E001`, `U+E003` — les Xbox.
2. **La planche.** Elle porte bien le jeu Xbox 360, et le fontmap y envoie bien.
3. **Le schéma de manette `spr_n_cmnps3`.** L'écran OPTIONS > Controls **n'en
   affiche aucun** — constaté sur capture. Le repeindre ne change rien là.

---

## 6. Ce qu'il reste à faire pour changer les boutons

**PÉRIMÉ DEPUIS LE 2026-10-09, et c'est une bonne nouvelle.** Pour passer les
menus aux boutons Xbox il n'y a **rien à repeindre du tout** : le jeu Xbox 360
est déjà dans la planche, et il suffit de faire pointer les quatre échappements
`_PS3` sur les glyphes de leurs homologues sans suffixe —
`patch_moteur.py --boutons-xbox`, **quatre octets**, un seul par glyphe :

    0x1805343BC   EE 80 95 -> EE 80 80     rond     -> B
    0x1805343D4   EE 80 96 -> EE 80 81     croix    -> A
    0x1805343EC   EE 80 97 -> EE 80 82     triangle -> Y
    0x180534408   EE 80 98 -> EE 80 83     carre    -> X

Chaque suite `glyphe + NUL` n'apparaît **qu'une fois** dans le binaire : aucun
littéral partagé, donc aucun effet de bord ailleurs. Les noms sont intacts.

Le repeignage ne redevient nécessaire que pour un jeu de boutons que la planche
**n'a pas** — Xbox One, PS4, PS5. La recette tient alors en quatre étapes :

1. Repeindre les cases voulues (rangées 56-57 de `spr_n_fnt32` tex0).
2. Réencoder la texture en BC3 et la remettre dans le TXP, taille identique.
3. Remplacer `spr_n_cmnps3` (RGBA brut, aucune contrainte) — **mais vérifier
   d'abord quel écran l'affiche** : ce n'est pas OPTIONS > Controls.
4. Reconstruire le `FArC` : gzip, en-tête gros-boutiste, tailles à jour.

**Et un piège mesuré** : `spr_n_cmnps3` est **stockée à l'envers**. `txp.py` ne
retourne que les formats DXT (son `FLIP_TOP_BOTTOM` est dans la branche
`f in (6, 9)`), donc le RGBA8 sort tête en bas. Ses traits de légende rouges
sont **dans la texture**, pas dessinés par le moteur.

Rien de tout cela ne touche `font_gothic.bin`, qui ne contient aucun picto de
manette — vérifié sur la planche entière.
