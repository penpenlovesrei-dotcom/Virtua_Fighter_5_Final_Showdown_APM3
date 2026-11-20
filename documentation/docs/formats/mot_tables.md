# `mot_db.bin` et `rob_mot_tbl.bin` — la base d'animations

Deux fichiers de `rom/rob/` qui, ensemble, nomment toutes les animations du jeu et disent
quelle animation joue quel rôle pour chaque personnage.

Lecteur : `tools/motdb.py`. Tout ce qui suit est vérifié sur l'arcade 6.000.

---

## 0. Comment ils ont été trouvés

Ancrage par le code, pas par tâtonnement. Dans
`vf5fs-pxd-w64-d3d12_SteamRetail.dll`, la fonction **`0x1801664B0`** référence la chaîne
`./rom/rob/rob_mot_tbl.bin` et installe un rappel en `0x180166510`. Ce rappel ouvre le fichier
**comme une archive FARC** et y cherche deux entrées par leur nom :

```
0x180166545  lea rdx, [rip + …]   ; "rob_cmn_mottbl.bin"
0x180166569  call 0x180166030     ; parseur
0x18016656E  lea rdx, [rip + …]   ; "yarare.bin"
0x180166592  call 0x1801665E0     ; parseur
```

L'archive extraite contient **exactement ces deux entrées**, et rien d'autre. Confiance :
**CONFIRMED**.

Le parseur `0x180166030` commence par une **passe de relocation** : il lit un offset 32 bits,
le convertit en adresse absolue, puis réécrit sur place un offset relatif au champ lui-même.
C'est ce qui explique la forme des en-têtes ci-dessous.

---

## 1. `rob_mot_tbl.bin` — archive FARC

Malgré son extension `.bin`, c'est une archive `FArc` (alignement 64), deux entrées :

| Entrée | Taille | Rôle |
|---|---:|---|
| `rob_cmn_mottbl.bin` | 56 232 o | table des rôles d'animation |
| `yarare.bin` | 23 432 o | table des réactions aux coups (*yarare* = やられ) |

---

## 2. `rob_cmn_mottbl.bin` — les rôles d'animation

### En-tête

```
0x00  u32  nombre d'entrees            21
0x04  u32  dernier index de role       363   -> 363 roles par bloc
0x08  u32  offset du tableau d'entrees 0xDB00
```

### Tableau d'entrées — 21 paires de 8 octets

```
+0x00  u32  offset du tableau de blocs
+0x04  u32  nombre de postures
```

À cet offset : `nombre de postures` offsets de blocs, puis les blocs eux-mêmes.

**Règle de placement vérifiée sur les 21 entrées :**

```
debut_du_premier_bloc = align32(offset + nombre_de_postures * 4)
```

Les blocs d'une même entrée se suivent avec un pas **uniforme de 1472 octets**
(363 rôles × 4 = 1452 octets utiles, plus 20 octets où logent les tableaux voisins).
38 blocs distincts au total.

### Un bloc = 363 rôles

Chaque bloc est un tableau de 363 `u32`. L'**index est un rôle logique** partagé par tous les
personnages ; la **valeur est l'identifiant d'animation** propre au personnage.
`0xFFFFFFFF` et `0` marquent un rôle non pourvu.

C'est le mécanisme qui permet au code commun de dire « joue la garde en position ouverte »
sans connaître le personnage.

### Les 21 entrées sont les personnages

Identifiées en résolvant chaque identifiant par `mot_db.bin` et en prenant le jeu
d'animation dominant hors `CMN` :

| # | Perso | Postures | | # | Perso | Postures |
|---:|---|---:|---|---:|---|---:|
| 0 | AKI | 1 | | 11 | **LEI** | **7** |
| 1 | SAR | 2 | | 12 | VAN | 3 |
| 2 | LAU | 2 | | 13 | BRA | 1 |
| 3 | **SHU** | **6** | | 14 | GOH | 1 |
| 4 | JEF | 1 | | 15 | MON | 1 |
| 5 | PAI | 1 | | 16 | MSK | 1 |
| 6 | JAK | 1 | | 17 | KRT | 1 |
| 7 | KAG | 3 | | 18 | TAK | 1 |
| 8 | LIO | 1 | | 19 | AKI (doublon de 0) | 1 |
| 9 | WOL | 1 | | 20 | DUR | 2 |
| 10 | AOI | 1 | | | | |

L'entrée 19 pointe vers **le même bloc** que l'entrée 0 (`0xD540`).

Le nombre de postures n'est pas arbitraire : Lei-Fei en a 7, Shun 6, Kage et Vanessa 3,
Sarah, Lau et Dural 2, tous les autres 1. Cela recoupe les systèmes de postures connus de ces
personnages. Confiance sur l'identification des personnages : **CONFIRMED** (résolution par
les noms d'animations) ; sur l'interprétation « posture = stance de combat » : **LIKELY**.

Cet ordre n'est **pas** celui du roster de `Sasikae-Soutyaku_Sheet1.csv` : c'est un ordre
interne propre à cette table.

### Exemple lu — entrée 18 (TAK), rôles 0 à 23

| Rôle | ID | Nom |
|---:|---:|---|
| 0 | 14050 | `TAK_RIK_TA_KAMAE_01` |
| 1 | 14048 | `TAK_RIK_SY_KAMAE_01` |
| 2 | 14051 | `TAK_RIK_TA_SY_01` |
| 3 | 14049 | `TAK_RIK_SY_TA_01` |
| 4–6 | 14044/14046/14045 | `TAK_RIK_GU_TA_00_N` / `_ST_N` / `_EN_N` |
| 7–9 | 14040/14042/14041 | `TAK_RIK_GU_SY_00_N` / `_ST_N` / `_EN_N` |
| 10–11 | 14047/14043 | `TAK_RIK_GU_TA_SY_N` / `GU_SY_TA_N` |
| 12–15 | 14504… | `TAK_NEW_TURN_N_TATA_B` … |
| 16–23 | 14518… | `TAK_NEW_TURN_TATA_R/L` … |

On y lit le vocabulaire du moteur : `KAMAE` = garde/posture, `GU` = *guard*,
`TA`/`SY` = les deux appuis (positions ouverte / fermée), `ST`/`EN` = début / fin,
`TURN` = retournement, `DMY` = doublure.

---

## 3. `mot_db.bin` — nom de chaque animation

### En-tête

```
0x00  u32  version                1
0x04  u32  offset table des jeux  0x40
0x08  u32  offset (table d'index) 0x462A0
0x0C  u32  nombre de jeux         45
0x10  u32  offset noms d'os       0x46AE0
0x14  u32  nombre d'os            149
```

### Table des jeux — 45 enregistrements de 16 octets, à `0x40`

```
+0x00  u32  offset du nom du jeu
+0x04  u32  offset du tableau des noms d'animations (0 si vide)
+0x08  u32  nombre d'animations
+0x0C  u32  offset du tableau des identifiants (parallele au precedent)
```

45 × 16 = 720 octets ; la table finit à `0x310` et les noms commencent à `0x320`.
Les deux tableaux sont **parallèles** : `noms[k]` porte l'identifiant `ids[k]`.

Les 45 jeux correspondent aux archives `mot_*.farc` de `rom/rob/` :
`ADV`, `AKI`, `AOI`, les 21 `AUTH_*`, `BRA`, `CMN`, `DUR`, `ENB`, `GOH`, `JAK`, `JEF`, `KAG`,
`KRT`, `LAU`, `LEI`, `LIO`, `MON`, `MSK`, `PAI`, `SAR`, `SHU`, `TAK`, `TEST_DESIGN`,
`VAN`, `WOL`.

### Volumétrie

**11 026 animations nommées, aucun identifiant en double**, plage 1 à 21 133.

| Jeu | Nb | Jeu | Nb | Jeu | Nb |
|---|---:|---|---:|---|---:|
| CMN | 801 | VAN | 735 | DUR | 638 |
| WOL | 578 | AOI | 529 | GOH | 499 |
| SHU | 479 | JEF | 442 | MSK | 435 |
| LEI | 432 | KAG | 416 | PAI | 402 |
| BRA | 388 | LIO | 388 | TAK | 385 |
| AKI | 381 | SAR | 373 | JAK | 352 |
| LAU | 323 | MON | 328 | KRT | 282 |
| TEST_DESIGN | 233 | ENB | 11 | ADV / AUTH_CMN | 0 |

Les `AUTH_*` comptent 48 à 68 animations chacun (mises en scène), sauf `AUTH_DUR` (3).

### Table des os — 149 pointeurs, à `0x46AE0`

`n_hara_cp`, `kg_hara_y`, `kl_hara_xz`, `kl_hara_etc`, `n_hara`, `e_mune_cp`, `cl_mune`,
`n_mune_b`, `kl_mune_b_wj`, `kl_kubi`, `n_kao`, `e_kao_cp`, …

Vocabulaire japonais cohérent avec celui des tables d'objets (`CHARACTERS.md`) :
`hara` = ventre, `mune` = poitrine, `kubi` = cou, `kao` = visage, `momo` = cuisse.
Les préfixes `n_`, `e_`, `kl_`, `kg_`, `cl_` distinguent des familles d'os
(sens non établi — **UNKNOWN**).

---

## 4. `yarare.bin` — réactions aux coups

Décodage partiel, structure vérifiée :

```
0x00  u32  nombre d'enregistrements   108
0x04  u32  offset du tableau          0x20
0x08  u32  second nombre              185
0x0C  u32  second offset              0x2A60
```

Le tableau à `0x20` contient **exactement 108 offsets**, en ordre décroissant, avec un pas
régulier de **96 octets** : `0x29F0`, `0x2990`, `0x2930`, … `0x1D0`. Le tableau se termine à
`0x20 + 108×4 = 0x1D0`, c'est-à-dire précisément là où commence le dernier enregistrement.
La structure se referme donc exactement.

Contenu des enregistrements de 96 octets : **UNKNOWN**. Second bloc à `0x2A60`, 185 entrées :
**UNKNOWN**.

---

## 5. Ce que cela débloque

- Tout identifiant d'animation croisé ailleurs (dans `mothead_*.bin` notamment) peut
  désormais être **nommé**.
- Les 363 rôles offrent un référentiel commun pour comparer les personnages entre eux et
  les versions entre elles (`tools/motdb.py diff`).
- Les noms portent la sémantique du moteur (`KAMAE`, `GU`, `TA`/`SY`, `YA`, `KABE`) : c'est
  un lexique exploitable pour aborder `mothead_*.bin`.

## Outillage

```bash
py -3 tools/motdb.py sets  <mot_db.bin>
py -3 tools/motdb.py chars <rob_cmn_mottbl.bin> <mot_db.bin>
py -3 tools/motdb.py slots <rob_cmn_mottbl.bin> <mot_db.bin> 18
py -3 tools/motdb.py name  <mot_db.bin> 14050
py -3 tools/motdb.py diff  <mot_db.bin> <tblA> <tblB>
```
