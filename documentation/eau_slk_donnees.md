# L'EAU D'EILEEN (`slk`) — INVENTAIRE DES DONNÉES, QUATRE ARBRES

Mesuré le 2026-10-15. Tout est vérifié par empreinte, pas par le nom des
dossiers.

## 1. Il n'y a PAS quatre générations de données, il y en a TROIS

Empreinte sha1 du `stgslk_obj.bin` décompressé :

| source | taille | sha1 | objets / textures |
|---|---|---|---|
| Lindbergh **ver.B** | 6 600 736 | `4c147c61…` | 111 / 580 |
| **X360** `objset_x36` | 6 600 736 | **`4c147c61…`** | 111 / 580 |
| **PS3** `objset` | 6 600 736 | **`4c147c61…`** | 111 / 580 |
| Lindbergh **R** | 5 860 800 | `04d5f8bf…` | 136 / 358 |
| Lindbergh **FS** | 6 535 680 | `a41a5613…` | 188 / 355 |
| **APM3** (`.par`) | 6 535 680 | **`a41a5613…`** | 188 / 355 |

**ver.B = X360 = PS3**, octet pour octet. Seules les textures sont ré-encodées
par plateforme. **Lindbergh FS = APM3**, octet pour octet, y compris
`EFFSTGSLK.farc`, `slk.ibl`, les `light_param` et la collision.

Donc : **ver.B (= consoles), R, FS (= APM3)**.

PIÈGE : les identifiants de texture changent d'espace entre ver.B et R. Il faut
résoudre chaque génération avec SA base (`extracted\decors\VF5_VERB\_db\`,
`VF5R\_db\`, `extracted\tex_db.bin`). `tools/tex_db.py` refuse les trois bases
anciennes (8 ou 24 octets de queue en trop) — à corriger un jour.

## 2. Le matériau de `stgslk_eff_water`, le grand plan

| champ | ver.B / consoles | R | FS / APM3 |
|---|---|---|---|
| nb emplacements | **2** | **3** | **3** |
| drapeaux `+0x04` | `00000101` | `00008529` | `00008529` |
| second mot `+0x10` | `00000D70` | `00000E30` | `00001630` |
| mélange `+0x3D4` | `10000A80` | `10000A80` | `10000A80` |
| diffuse `+0x3D8` | (1,00 0,85 0,65) | **(0,10 0,10 0,10)** | (0,80 0,70 0,50) |
| alpha spéculaire | 0,600 | 0,350 | 0,500 |
| `+0x418` / `+0x41C` | 5,0 / 0,2 | 20,0 / 0,1 | 20,0 / 0,1 |
| empl. 0 | `MU_RINGOUTMIZU` | idem | idem |
| empl. 2 | `HR_BMP_000` | idem | idem |
| empl. 5 | **ABSENT** | `HR_MIZU` | `HR_MIZU` |

**ver.B n'a aucune carte d'environnement sur l'eau.** C'est R qui l'ajoute.

Et `MU_RINGOUTMIZU` (empl. 0) est, dans les TROIS générations, une image de
**sable beige nuageux** : c'est le FOND vu à travers l'eau, pas l'eau. Le
remplacer est donc une erreur.

## 3. Le matériau de `stgslk_water_ring`, le disque du ring

| | ver.B / consoles | R | FS |
|---|---|---|---|
| nom | `WaterRing_ISD015F5Z` | `…F3Z` | `…F3Z` |
| `+0x10` | **`00001570`** | `00000D70` | `00000D70` |
| B `+0x3E8` | **(0,500 0,370 0,190)** | (0,160 0,150 0,120) | **(0 0 0)** |
| C `+0x3F8` | (0 0 0,5 ; 0,35) | idem | **(1 1 1 ; 0,35)** |
| empl. 0/1/2 | `KA_NIGORI0`, `KA_NIGORI1`, `KA_WATER_N` | idem | **`HR_NIGORI0/1`** (2048²) |

Aspect mesuré des textures : ver.B `NIGORI0` gris-bleu sombre, `NIGORI1`
blanc bleuté froid avec un quadrillage d'ombres. Chez R, `NIGORI1` **devient
beige chaud**. Chez FS, sable chaud en 2048². **Les textures d'anneau les plus
« eau » sont celles de ver.B.**

`KA_WATER_N` est le **même fichier dans les trois** : RGB8 256×256, **bleu pur
uniforme (0,0,255)** — ce n'est pas une normale neutre (128,128,255).

## 4. L'animation : un feuilletage de 120 images

`STGSLK_EFF_WATER.a3da`, **identique ver.B et R**, daté du 11/01/2006 :

    play_control  begin 0  fps 60  size 120
    curve.0.name = WATER   0 -> 119
    object.0.tex_pat.0.name = F_VF5S_SLK00_HR_BMP_000   pat = WATER

120 images à 60 i/s, 2 s en boucle, qui remplacent `HR_BMP_NNN` dans
l'emplacement 2. Les 120 images existent dans les trois générations.

FS ajoute une courbe `SUNA` et un **morph** `STGSLK_EFF_SUNA_000` sur les mêmes
120 images — le sable de Final Showdown est un morph, pas une texture animée.

Aucune translation, rotation ni échelle non triviale dans aucun `.a3da` du
décor (sauf l'échelle 0,7 de `DOBON_S`). `STGSLK.farc` ne contient que des
caméras.

## 5. La collision : ver.B a DEUX sols

Deux fichiers seulement : ver.B = X360 = PS3 (3 184 o, 11 faces) et
R = FS = APM3 (2 672 o, 10 faces).

| | ver.B / consoles | R / FS |
|---|---|---|
| sol intérieur (−5…+5) | **y = 0,000** | **absent** |
| sol extérieur (−10…+10) | **y = −0,010** | y = 0,000 |
| murs | de −0,010 à 6,0 | de 0,0 à 6,0 |

Le plan d'eau est à y = 0. Donc **chez ver.B et sur console, la zone de
ring-out est 1 cm SOUS l'eau : le joueur y patauge**. Chez R et FS, un seul sol
plat exactement au niveau de l'eau.

## 6. L'ambiance

ver.B = **jour chaud** (brouillard 1,30/1,20/1,00, ambiante 0,700, IBL
`LIT_COL 0` chaude). R = **nuit** (brouillard bleu, lune ajoutée dans
`reflect`, IBL bleue, eau diffuse 0,1). FS = **jour neutre-blanc**, brouillard
resserré 30→139,5, sable ajouté.

`envmap_correct_slk.txt` est **absent des trois dumps Lindbergh** mais présent
et identique sur X360, PS3 et dans le `.par` d'APM3 :
`1 1 1 / 0 0 0 / 0.2 -0.85 0.4`.

## 7. Deux écarts de notre chantier avec les trois générations

Relevés dans l'arbre vivant, sans verdict :

1. `stgslk_eff_water` emplacement 0 pointe sur **12674** (`NIGORI0`) au lieu de
   **9261** (`MU_RINGOUTMIZU`), que les trois générations portent.
2. le mélange `+0x3D4` vaut **`00000A81`** au lieu de `10000A80` partout
   ailleurs.
