# Les décors des trois générations Lindbergh, extraits et comparés

Établi le 2026-09-07. Extraction complète dans **`extracted/decors/`**, table
dans **`analysis/decors_lindbergh.csv`**, outil **`tools/inventaire_decors.py`**.

---

## 1. Ce qui a été extrait, et d'où

| dossier | jeu | identification | source |
|---|---|---|---|
| `extracted/decors/VF5_VERB` | **Virtua Fighter 5 ver.B** | `gameid=SBLM`, chemin de build `p73/prj73p/snapshot/overseas_edition/**20070530**/vf5_root/vf5`, chaînes `vf5verB_jng*` | `Virtua Fighter 5.7z` → `vf5.bin` (3,77 Go) |
| `extracted/decors/VF5R` | **Virtua Fighter 5 R** | 2008-06-16 | `vf5r.7z` → `vf5r.bin` + `vf5r_rom.bin` |
| `extracted/decors/VF5FS_LIND` | **Final Showdown Rev A** | release 2.000, 2010-06-28 | `LIND_FS` → `vf5fs.bin` + `vf5fs_ext.bin` |

**`Virtua Fighter 5.7z` n'était pas inventorié** : `SOURCES.md` le donnait pour
absent (« `VF5_ARCADE` »). C'est bien un dump Lindbergh de VF5 vanilla ver.B, et
il apporte un décor que rien d'autre ne contient (§3).

Chaque jeu est rangé de la même façon, quel que soit le désordre d'origine :

```
<jeu>/objset/       stg*.farc          geometrie + textures
<jeu>/auth_3d/      STG*.farc          animation du decor
                    EFFSTG*.farc       effets
<jeu>/coli/         STG*_COLI*.bin     collision
<jeu>/ibl/          *.ibl              eclairage par image
<jeu>/light_param/  *.txt              parametres d'eclairage, en clair
```

| | objsets | auth_3d | coli | ibl | light_param | total |
|---|---:|---:|---:|---:|---:|---:|
| VF5 ver.B | 29 | 37 | 26 | 29 | 112 | **420,6 Mo** |
| VF5 R | 40 | 45 | 41 | 41 | 160 | **519,6 Mo** |
| FS Lindbergh | 41 | 47 | 42 | 42 | 164 | **539,9 Mo** |

**Piège de disposition, à retenir** : un décor est à cheval sur deux images.
Chez VF5 R la géométrie est sur le disque système (`vf5r.bin`,
`disk0/ext/rom/objset/`) et tout le reste sur le disque de données
(`vf5r_rom.bin`). Chez Final Showdown c'est l'inverse : la géométrie est dans
`vf5fs_ext.bin` (`rom/objset/`) et le reste dans `vf5fs.bin` (`disk1/rom/`),
`disk0` n'étant qu'un arbre de liens symboliques.

---

## 2. La table, décor par décor

Tailles de l'objset en octets. Colonne APM3 lue dans l'index du `.par`, sans
extraction.

Les faits qui ressortent :

* **`dur` : 35 705 171 octets dans ver.B, et il n'existe nulle part ailleurs.**
* **`du1`…`du4` sont des bouchons dans ver.B** — 225 à 486 Ko — puis deviennent
  de vrais décors dans R (26 à 32 Mo).
* `du5` apparaît en Final Showdown.
* `gym` et `smo` apparaissent en R ; `gym` passe de 7,8 Mo à 21,8 Mo en FS.
* les dix `evo00`…`evo09` apparaissent en R et **ne bougent plus d'un octet**.

Extrait :

```
decor    VF5 ver.B        VF5 R  FS Lindbergh      FS APM3
dur       35705171            -             -            -   DISPARU apres ver.B
du1         485426     27365558      27229016     27229016
du2         225356     26639120      24144242     24144242
du3         484272     32408169      27894787     27894787
du4         486760     26830812      26188937     26188937
du5              -            -      24771735     24771735   nouveau en FS
djo       20049278     18959314      10516296     10516296
gym              -      7807826      21782948     21782948
jin       19334276     16892057      21886056     21871895   <- FS Lind != APM3
```

---

## 3. La découverte : `stgdur.farc`, un décor de Dural que plus rien ne contient

`analysis/decors_vf5r.md` notait, à partir des deux seuls dumps disponibles
alors : *« `EFFSTGDUR` existe des deux côtés mais il n'y a aucun `stgdur.farc`.
Le décor "DUR" n'est pas un décor : c'est un jeu d'effets. »*

**Cette conclusion était juste pour R et FS, et fausse en général.** VF5 ver.B
porte un `objset/stgdur.farc` de **35,7 Mo** — le plus gros objset de tout le
corpus, plus gros qu'aucun décor de R ou de FS — avec ses compagnons
`auth_3d/STGDUR.farc`, `EFFSTGDUR.farc` et sa collision.

L'histoire se lit dans la table : en ver.B, **un seul** décor de Dural, entier
(`dur`), et quatre emplacements `du1`…`du4` réservés mais vides (225–486 Ko).
En R, `dur` disparaît et les quatre emplacements sont remplis. En Final
Showdown, un cinquième s'ajoute. **Le décor de Dural a été découpé en quatre
puis en cinq**, et la version d'origine — un seul grand décor — n'existe plus
que dans ver.B.

C'est le seul décor du corpus qu'aucune version ultérieure ne contient. Si un
import a un intérêt, c'est celui-là.

Confiance : **CONFIRMED** (fichier extrait, taille mesurée, absence vérifiée
dans les trois autres inventaires).

---

## 4. Une correction à `import_decors.md` §5

Ce document affirmait : *« les 41 archives `objset/stg*.farc` existent des deux
côtés, et les 41 ont exactement la même taille — pas un octet d'écart »* entre
le Final Showdown Lindbergh et l'APM3.

**Quarante sur quarante et une.** `stgjin.farc` fait **21 886 056** octets côté
Lindbergh et **21 871 895** côté APM3 — **14 161 octets d'écart**. Les
quarante autres sont bien identiques à l'octet.

L'affirmation d'origine reposait sur trois empreintes vérifiées (`are`, `tak`,
`djo`) et sur une comparaison de tailles qui a laissé passer celle-là. La règle
du chantier s'applique : une énumération ne vaut que ce que vaut son contrôle.

Et une deuxième correction, plus petite : `import_decors.md` §7 note que *« VF5
R n'a pas de `auth_3d/STGDJO.farc` — seulement `EFFSTGDJO.farc` »*. Le listing
de `vf5r_rom.bin` contient bien **`auth_3d\STGDJO.farc`, 37 811 octets**. Le
jeu complet du décor DJO de R est donc transposable ; ce n'est pas là que
l'essai avait échoué.

---

## 5. Ce que ça change pour l'import

1. **Le corpus est désormais complet** : quatre générations côte à côte, au
   même format, dans la même disposition. Toute comparaison objet par objet
   peut se faire sans retoucher aux images.
2. **`stgdur` est la cible naturelle du premier import** — c'est le seul
   contenu réellement absent d'APM3, et il vient avec son `auth_3d`, sa
   collision et son éclairage, donc **avec sa génération**. C'est exactement la
   condition qui manquait à l'essai DJO de 2026-09-03
   (`import_decors.md` §7 : l'`objset` venait de R et tout le reste de FS).
3. **La voie d'accueil est prête** : `ajouter_un_decor.md` montre que
   l'identifiant d'objset est une donnée de `obj_db.bin`, et que recycler l'un
   des 17 emplacements d'essai (`tst ts2 ts3 wht trm cid trs evo00..evo09`) ne
   demande de lever **aucune borne**.
4. **Le conteneur n'a pas bougé entre 2007 et 2011** — mesuré, pas supposé.
   Les quatre générations écrivent le même en-tête :

   ```
   VF5 ver.B  stgdur.farc   46417243 0000003a   FArC...:....stgdur_obj.bin ... stgdur_tex.bin
   VF5 ver.B  stgare.farc   46417243 0000003a   FArC...:....stgare_obj.bin ... stgare_tex.bin
   VF5 R      stgdjo.farc   46417243 0000003a   FArC...:....stgdjo_obj.bin ... stgdjo_tex.bin
   FS Lind    stgare.farc   46417243 0000003a   FArC...:....stgare_obj.bin ... stgare_tex.bin
   ```

   `FArC`, en-tête `0x3A`, deux entrées `<nom>_obj.bin` et `<nom>_tex.bin`.
   `import_decors.md` §1 l'avait établi de 2008 à 2010 ; c'est vrai **de 2007 à
   2011**.

5. **La réserve qui subsiste n'est donc plus le format, c'est le contenu** —
   comme en 2026-09-03. Le nombre d'objets d'un `objset` change d'une
   génération à l'autre (119 en 2008, 171 en 2010 pour DJO), et tout ce qui
   désigne un objet **par indice** doit venir de la même génération. Pour
   `stgdur`, cette condition est remplie : ses `auth_3d`, sa collision et son
   éclairage sont extraits avec lui.
