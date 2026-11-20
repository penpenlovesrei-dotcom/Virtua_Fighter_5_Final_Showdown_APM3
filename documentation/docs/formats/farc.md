# Format FARC — archive SEGA

Format d'archive employé par VF5FS sur **toutes** les plateformes, de la Lindbergh (2010)
à R.E.V.O. (2025). Lecteur : `tools/farc.py`.

Niveau de confiance : **CONFIRMED**. Le format a été déduit des en-têtes du dump, et le
décompresseur a été validé : le `mothead_AKI.bin` extrait de
`PC_REVO/rom_200/resident.farc` est **identique au SHA-256** au fichier libre
`PC_REVO/rom_200/rob/mothead_AKI.bin` (190 108 o,
`B54A83C0765AFBC809D8B18E10A96BB79E5198A6104F57C746628F938BEF0109`).

## Structure

Tous les entiers sont **gros-boutistes**, y compris dans les versions x86 du jeu — seul le
conteneur l'est ; les données à l'intérieur suivent l'endianness de la plateforme.

```
offset  taille  champ
0x00    4       magic       'FArc' | 'FArC' | 'FARC'
0x04    4       header_size octets apres ce champ jusqu'au debut des donnees
0x08    4       alignment   alignement des donnees (1, 0x10 ou 0x40 observes)
0x0C    …       table des entrees, jusqu'a 8 + header_size
```

Chaque entrée :

```
        n+1     nom             chaine terminee par NUL
        4       offset          position des donnees dans le fichier
        4       csize           octets stockes
        4       usize           octets une fois decompresses   <- 'FArC' uniquement
```

`8 + header_size` donne à la fois la fin de la table et l'offset de la première entrée
(avant alignement).

## Les trois modes de stockage

| magic | `usize` | Contenu à `offset` |
|---|---|---|
| `FArc` | champ absent | données brutes, `csize` octets |
| `FArC` | > 0 | flux **gzip** (`1F 8B`), `csize` octets stockés → `usize` octets |
| `FArC` | **0** | données brutes, `csize` octets |

Le troisième cas est le piège : une archive `FArC` peut contenir des entrées non
compressées, signalées par `usize = 0` et non par l'égalité des tailles. C'est le cas des
`envmap_correct_*.txt` de `rom_200/resident.farc` (25 à 28 octets chacun — trop courts pour
que la compression soit rentable).

Le flux compressé est du **gzip**, pas du deflate brut ni du zlib : en-tête complet avec
l'indicateur FNAME, qui répète le nom du fichier. `tools/farc.py` accepte tout de même zlib
et deflate brut en repli, au cas où d'autres variantes existent.

## Exemple lu octet par octet

`APM3_FS/rom/rob/mot_db.farc` :

```
46 41 72 43   'FArC'
00 00 00 1B   header_size = 27
00 00 00 01   alignment = 1
6D 6F 74 5F 64 62 2E 62 69 6E 00    "mot_db.bin\0"   (11 octets)
00 00 00 23   offset = 0x23 = 8 + 27
00 01 46 D8   csize  = 83 672
00 04 6D 40   usize  = 290 112
1F 8B 08 08 …  flux gzip, nom interne "mot_db.bin"
```

Vérification : 4 (alignment) + 11 (nom) + 12 (trois champs) = 27 = `header_size`. ✓

`APM3_FS/rom/live_data.farc` est un `FArc` à `alignment = 0x40` : la table finit à
`8 + 0x50 = 0x58`, et la première donnée est alignée à `0x80`.

## Utilisation

```bash
py -3 tools/farc.py list <archive>
py -3 tools/farc.py extract <archive> <destination>
py -3 tools/farc.py extract-all <racine> <destination>
```

`extract-all` parcourt une arborescence, reconnaît les archives à leur signature (pas à leur
extension) et reproduit la hiérarchie.

## Variante `FARC`

La signature `FARC` (majuscules) existe dans d'autres jeux de la même famille et désigne une
variante chiffrée ou étendue. **Aucune occurrence dans nos six sources** — le lecteur la
refuse explicitement plutôt que de deviner.

## Ce que les archives contiennent

Constat après extraction des archives de données de `APM3_FS` :

| Archive | Entrées | Contenu notable |
|---|---:|---|
| `rom/rob/mot_db.farc` | 1 | `mot_db.bin`, 290 112 o — base de données de mouvements |
| `rom/rob/mot_<CHR>.farc` | 1 | `mot_<CHR>.bin` — animations, un gros blob par personnage |
| `rom/cid_table.farc` | 41 | `cid_table.bin` + `charaimage_IDlist_<CHR>_{A3D,AET}.csv` |
| `rom/chritm_tbl.farc` | 41 | `<chr>itm_tbl.bin` + **`<chr>_itm.csv`** |
| `rom/gm_itm_tbl.farc` | 13 | tables d'objets |
| `rom/shader.farc` | 2 724 | programmes `.vp` / `.fp` (shaders ARB) |
| `rom/live_data.farc` | 3 | `live_frz_tbl.bin`, `live_voice_data.bin`, `mot_attrib.bin` |
| REVO `rom_200/resident.farc` | 208 | `mothead_*.bin`, `STG*_COLI*.bin`, `fog_/light_/wind_/envmap_*.txt` |

Plusieurs archives contiennent des **CSV en clair** (`<chr>_itm.csv`,
`charaimage_IDlist_*.csv`) : ce sont des tables de correspondance lisibles directement, à
exploiter avant tout travail de désassemblage.
