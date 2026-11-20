# CHARACTERS — roster et codes internes

Confiance : **CONFIRMED**. Le tableau ci-dessous n'est pas déduit : il vient d'une table du
jeu, `chritm_tbl.farc → Sasikae-Soutyaku_Sheet1.csv`, qui donne les noms en toutes lettres
dans l'ordre interne, recoupée avec quatre autres sources concordantes.

## Correspondance code ↔ personnage

| # | Code | Nom (table du jeu) | Nom japonais (`charaimage_IDlist`) |
|---:|---|---|---|
| 1 | `AKI` | AKIRA | アキラ |
| 2 | `AOI` | AOI | — |
| 3 | `BRA` | BRAD | — |
| 4 | `GOH` | GOH | — |
| 5 | `JAK` | JACKY | — |
| 6 | `JEF` | JEFFRY | — |
| 7 | `KAG` | KAGE | — |
| 8 | `LAU` | LAU | — |
| 9 | `LEI` | LEI-FEI | — |
| 10 | `LIO` | LION | — |
| 11 | `PAI` | PAI | — |
| 12 | `SAR` | SARAH | — |
| 13 | `SHU` | SHUN | — |
| 14 | `VAN` | VANESSA | — |
| 15 | `WOL` | WOLF | — |
| 16 | `MSK` | **EL BLAZE** | — |
| 17 | `MON` | **EILEEN** | — |
| 18 | `KRT` | **KARATE** (Jean Kujo) | — |
| 19 | `TAK` | **TAKAARASHI** | — |
| — | `DUR` | Dural — non sélectionnable | — |
| — | `CMN` | données communes, pas un personnage | — |

Les quatre codes non évidents — `MSK` (masque → El Blaze, catcheur masqué), `MON` (singe →
Eileen, kung-fu du singe), `KRT` (karaté → Jean Kujo), `TAK` (Taka-Arashi) — sont **établis
par la table**, pas devinés.

## L'ordre a un sens

Les quinze premiers sont dans l'ordre alphabétique de leur code ; les quatre derniers sont
ajoutés à la suite, hors ordre. C'est l'ordre d'ancienneté dans la série, pas un tri.
Cet ordre est vraisemblablement l'index interne de personnage. Confiance : **LIKELY** —
à confirmer contre `cid_table.bin` ou `code_map.bin`.

## Sources concordantes

| Source | Ce qu'elle donne | Personnages |
|---|---|---|
| `chritm_tbl.farc → Sasikae-Soutyaku_Sheet1.csv` | noms complets en anglais, en colonnes | 19 |
| `rom/rob/ctrl_<CHR>.bin` | tables de commandes | 20 (avec `DUR`) |
| `rom/rob/mothead_<CHR>.bin` | données de coups | 21 (avec `DUR` et `CMN`) |
| chaînes `chara_icon_<xxx>_c` dans `vf5` | icônes de l'écran de sélection | 19 (sans `DUR`) |
| `chritm_tbl.farc → <chr>_itm.csv` | tables d'objets | 20 (avec `DUR`) |

`DUR` a bien un jeu de données de combat complet mais aucune icône de sélection : Dural est
jouable par le moteur, pas par le joueur.

## Vocabulaire des emplacements du corps

Extrait de `Sasikae-Soutyaku_Sheet1.csv` (24 emplacements) et de la colonne `Kisekae` des
tables d'objets. Ce vocabulaire servira pour `bone_data.bin` et les volumes de collision.

**Tête et visage** : `ZUJO` (sommet du crâne), `KAMI` (cheveux), `HITAI` (front), `ME` (yeux),
`MEGANE` (lunettes), `MIMI` (oreilles), `KUCHI` (bouche), `MAKE` (maquillage), `ATAMA` (tête).

**Torse** : `KUBI` (cou), `INNER`, `OUTER`, `MUNE` (poitrine), `SENAKA` (dos), `HARA` (ventre),
`KATA` / `KATA_L` / `KATA_R` (épaules), `BELT`, `KOSI` (hanches), `JOHA_MAE` (devant),
`JOHA_USHIRO` (derrière).

**Membres** : `U_UDE` (bras supérieur), `L_UDE` (avant-bras), `UDE_L` / `UDE_R`,
`TE` / `TE_L` / `TE_R` (mains), `MOMO` (cuisses), `SUNE` (tibias), `ASI` (jambes/pieds),
`KUTSU` (chaussures), `PANTS`, `HADA` (peau).

## Système d'objets — volumétrie

`chritm_tbl.farc` contient **14 444 objets** répartis sur 20 personnages (de 639 pour `TAK`
à 915 pour `KAG` ; `DUR` n'en a que 4).

Colonnes de `<chr>_itm.csv` :

```
Fix, Ver, ObjUid, ID, Category, Position, ItemName, Icon, ObjitmorgID, TexitmorgID,
ItmorgID, Dummy, Default, Attr, TexOrg, TexChg, Type, Kisekae, Haita, Style, Point,
Rem, CPU, GPU, ItemNameHira, Dbgset, HaitaItemID, Memo
```

- `Category` — 5 valeurs : `JOHA` (5 037), `ATAM` (4 503), `KAHA` (3 719), `FACE` (1 137),
  `HADA` (48).
- `Type` — 4 valeurs : `EQUIP` (2 998, ajout), `REPLACE` (736, substitution de maillage),
  `LOOKS` (274), `REM` (105).
- `Kisekae` — liste des parties de corps remplacées, d'où le vocabulaire ci-dessus.
- `CPU` et `GPU` — un coût par objet. Le jeu budgétise donc explicitement le rendu des
  tenues. À creuser : ces budgets sont-ils vérifiés à l'exécution ?
- `ObjUid` — identifiant textuel, ex. `AKIITM001_ATAM_ATAMA_01`, qui encode
  personnage + numéro + catégorie + emplacement + variante.

## Character Image — démos de pose

`cid_table.farc` décrit le système de démonstration personnalisable de la borne (lié aux
cartes VF.NET).

| Type | Plage d'ID | Nombre | Contenu |
|---|---|---:|---|
| `A3D` (motion) | 800–843 | 44 par personnage | poses, avec `SceneID` de la forme `P010A010` |
| `A3D` pour `KRT` et `TAK` | 800–828 | 29 | les deux derniers venus en ont moins |
| `AET` (arrière-plan 2D) | 850–968 | 119, communs | effets, avec un `.avi` associé |

Les colonnes japonaises donnent, pour chaque pose, une description littéraire
(ex. `両腕を交差させてから、勢いよく開く` — « croise les deux bras puis les ouvre d'un coup »)
et une distance de caméra (`遠･中･近` — loin / moyen / près).

## Fichiers convertis

Toutes les tables d'origine sont en **Shift-JIS (CP932)**. Copies UTF-8 lisibles :

```
extracted/csv_utf8/APM3_FS/chritm_tbl/*.csv     tables d'objets, 21 fichiers
extracted/csv_utf8/APM3_FS/cid_table/*.csv      Character Image, 40 fichiers
extracted/csv_utf8/PC_REVO/rom_200/resident/    paramètres de décor, 135 fichiers .txt
```

Conversion par `tools/convert_csv.py`. Les originaux extraits restent en CP932 dans
`extracted/APM3_FS_farc/`.

---

## L'indice de personnage à l'exécution — `ROB+0x10`

Établi le 2026-09-02. Les **71** sites d'appel de `GetMotionForRole` dans le build APM3
présentent tous le même motif : `mov ecx, [ROB+0x10]` et `movzx edx, byte [ROB+0x65C]`.
`ROB+0x10` est donc **l'indice du personnage**, c'est-à-dire l'entrée dans
`rob_cmn_mottbl.bin`, et `ROB+0x65C` la posture.

La table, obtenue par `RobMotTbl.label()` (jeu d'animations dominant de chaque entrée) :

| index | postures | perso | index | postures | perso | index | postures | perso |
|---:|---:|---|---:|---:|---|---:|---:|---|
| 0 | 1 | AKI | 7 | 3 | KAG | 14 | 1 | GOH |
| 1 | 2 | SAR | 8 | 1 | LIO | 15 | 1 | MON |
| 2 | 2 | LAU | 9 | 1 | WOL | 16 | 1 | MSK |
| 3 | **6** | SHU | 10 | 1 | AOI | 17 | 1 | KRT |
| 4 | 1 | JEF | 11 | **7** | LEI | 18 | 1 | TAK |
| 5 | 1 | PAI | 12 | 3 | VAN | 19 | 1 | **AKI (doublon)** |
| 6 | 1 | JAK | 13 | 1 | BRA | 20 | 2 | DUR |

L'entrée **19 est un doublon d'AKI** : elle partage la table de postures de l'entrée 0. C'est
le piège de relocation signalé dans `docs/formats/mot_tables.md` — relocaliser naïvement
applique deux fois le décalage aux champs partagés.

**Utilité pratique** : lire `ROB+0x10` dit **quel personnage est en jeu, sans aucune capture
d'écran**. `tools/oracle_liste2_vivant.py` l'affiche pour chaque combattant rencontré, ce qui
permet de savoir si un code propre à un personnage — le 27 pour Shun, le 19 pour Brad — était
seulement atteignable pendant la passe.
