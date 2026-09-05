# Ce que VF5 R apporte en decors

Dump ajoute le 2026-09-03 : `vf5r.7z`, 4,66 Go, deux images ext Linux
(`vf5r.bin` 2,5 Go = disque systeme, `vf5r_rom.bin` 2,9 Go = disque de donnees),
extraites dans `extracted/LIND_R/`. Inventaires dans
`analysis/inventory/LIND_R_sys.listing.txt` et `LIND_R_rom.listing.txt`.

---

## 1. De quoi est fait un decor

Releve sur `ARE` dans le dump APM3 — c'est la recette a reproduire pour toute
transplantation :

| fichier | role | taille (ARE) |
|---|---|---:|
| `rom/objset/stgare.farc` | **geometrie et textures** | 22,1 Mo |
| `rom/auth_3d/STGARE.farc` | animation du decor | 32 Ko |
| `rom/auth_3d/EFFSTGARE.farc` | effets | 45 Ko |
| `rom/STGARE_COLI.000.bin` | collision | 4,3 Ko |
| `rom/ibl/are.ibl` | eclairage par image | 542 Ko |
| `rom/light_param/{fog,glow,light,wind}_are.txt` | parametres d'eclairage, **en texte clair** | ~2 Ko |
| `rom/sound/se_stage_are.csb` | ambiance | 641 Ko |
| `rom/sound/bgm/*.adx` | musiques | 3 a 6 Mo |

Neuf a soixante fichiers par decor, 25 a 200 Mo. Les parametres d'eclairage sont
en **texte lisible** : c'est la partie la plus facile a transposer.

---

## 2. Le compte des decors : identique des deux cotes

Les deux jeux declarent **41 emplacements** `objset/stg*.farc`. Le tri par taille
les separe sans ambiguite :

- **24 decors reels dans APM3** (plus de 5 Mo) :
  `ARE AUR BAN BAR CAS DJO DU1 DU2 DU3 DU4 DU5 GYM HAI JIN NYC RIV SIN SLK SMO TAK TAN TER UMI YUK`
- **23 dans VF5 R** : les memes, **moins `DU5`**.
- **17 entrees d'essai**, vides ou minuscules, **identiques dans les deux jeux** :
  `CID EVO00`-`EVO09 TRM TRS TS2 TS3 TST WHT` (0 a 1,2 Mo).

Une remarque au passage : `EFFSTGDUR` existe des deux cotes mais **il n'y a
aucun `stgdur.farc`**. Le decor « DUR » n'est pas un decor : c'est un jeu
d'effets, et les vrais decors de Dural sont `DU1` a `DU5`.

### Conclusion, et elle est negative

**VF5 R n'apporte aucun decor nouveau.** Tout ce qu'il a, APM3 l'a — et APM3 a
`DU5` en plus. Il faut le dire avant d'esperer : l'import « de nouveaux decors »
depuis VF5 R n'a pas d'objet.

Confiance : **CONFIRMED** (comparaison des inventaires complets des deux dumps).

---

## 3. Mais il apporte des versions PLUS RICHES des memes decors

C'est le vrai gisement. Les tailles ne concordent pas, et pas au hasard :

| decor | VF5 R | APM3 | ecart |
|---|---:|---:|---|
| **DJO** | 18,1 Mo | 10,0 Mo | **VF5 R + 8,1 Mo** |
| **SIN** | 23,8 Mo | 15,8 Mo | **VF5 R + 8,1 Mo** |
| **SMO** | 27,5 Mo | 20,3 Mo | **VF5 R + 7,3 Mo** |
| **NYC** | 27,9 Mo | 21,0 Mo | **VF5 R + 6,9 Mo** |
| **DU3** | 30,9 Mo | 26,6 Mo | **VF5 R + 4,3 Mo** |
| DU2 | 25,4 Mo | 23,0 Mo | VF5 R + 2,4 Mo |
| BAR | 14,9 Mo | 13,7 Mo | VF5 R + 1,3 Mo |
| CAS | 27,5 Mo | 26,6 Mo | VF5 R + 0,8 Mo |
| HAI | 21,4 Mo | 20,6 Mo | VF5 R + 0,8 Mo |
| GYM | 7,4 Mo | 20,8 Mo | APM3 + 13,3 Mo |
| JIN | 16,1 Mo | 20,9 Mo | APM3 + 4,8 Mo |
| BAN | 22,6 Mo | 26,9 Mo | APM3 + 4,3 Mo |
| TER, YUK | 12,5 / 17,7 Mo | 15,9 / 21,1 Mo | APM3 + 3,4 Mo |
| SLK | 15,2 Mo | 18,2 Mo | APM3 + 3,1 Mo |
| AUR | 26,7 Mo | 26,7 Mo | a l'octet pres |

Cinq decors ont **perdu 4 a 8 Mo** en passant de R a Final Showdown — DJO, SIN,
SMO, NYC, DU3. Trois en ont gagne autant — GYM, JIN, BAN. Et `AUR` n'a pas
bouge d'un octet.

Ce n'est donc pas une recompression globale : ce sont des **remaniements decor
par decor**. La version R de DJO, SIN, SMO ou NYC contient quelque chose que la
version Final Showdown n'a plus.

Confiance : **SUPPORTED**. La taille dit qu'ils different, pas ce qui differe.
Il faut ouvrir les `.farc` et comparer les objets pour savoir si c'est de la
geometrie, des textures, ou seulement un empaquetage different.

---

## 4. Ce qui est deja acquis sans rien importer

Le dump APM3 porte **278 pistes de musique**, et leurs prefixes trahissent trois
generations deja presentes :

| prefixe | pistes |
|---|---:|
| `h_` | 73 |
| `vf5fs_` | 61 |
| `vf5b_` | 36 |
| **`vf5r_`** | **29** |
| **`vf5rb_`** | **23** |
| `vf5d_` | 22 |
| `kusudama_` | 19 |
| `vftv_` | 11 |

Chaque decor a d'ailleurs ses trois versions cote a cote — pour ARE :
`vf5fs_bgm_are.adx`, `vf5r_are.adx`, `h_are_vf5.adx`. **Les musiques de VF5 R
sont deja dans le jeu.** Si le but est de retrouver l'ambiance de R, la moitie
du chemin est faite avant d'avoir touche a quoi que ce soit.

---

## 5. La prochaine mesure

1. **Comparer le contenu de `stgdjo.farc`** entre les deux dumps — c'est le plus
   gros ecart (+8,1 Mo cote R) sur un decor de taille moyenne. Lister les objets
   des deux archives et faire la difference : on saura enfin *ce qui* a ete
   retire.
2. **Comparer les `light_param/*.txt`**, qui sont en texte clair : c'est la
   transposition la moins risquee, et elle change visiblement l'image.
3. Ne rien transplanter avant d'avoir verifie que le format `objset` de 2008 est
   lu par le moteur de 2010. Rien ne le garantit.
