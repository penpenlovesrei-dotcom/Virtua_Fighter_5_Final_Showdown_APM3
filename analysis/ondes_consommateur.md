# Les ondes d'eau : qui consomme ce que `TaskEffectRipple` produit

Build : `VF5RE/analysis/vf5fs_apm3_origine.dll` (image NON patchee, `sha256
045c0696…c0837eef`, base `0x180000000`). Lecture statique seule, via REA /
Ghidra 12.1.2. **Aucun binaire n'a ete execute.**

> **Reponse courte, d'abord.** Le bloc `gestionnaire+0x328` / `+0x32C` n'a
> **aucun lecteur** : c'est de la statistique de mise au point, morte dans ce
> build, exactement comme son voisin `+0x330`. **Mais la tache des ondes n'est
> pas pour autant un producteur sans consommateur** : son vrai produit ne passe
> pas par la, il passe par **un autre gestionnaire** (`DAT_18070fc68`, champ
> `+0x410`), et ce champ **est lu**, par deux passes de rendu. La chaine de la
> tache au pixel est **entiere** dans ce build.

---

## 1. Deux gestionnaires, pas un — c'est tout le malentendu

L'enquete partait de « l'objet rendu par `FUN_18006F350` ». Cet objet n'est pas
le gestionnaire de rendu. Il y en a **deux**, et ils n'ont rien a voir :

| nom neuf | adresse | ce que c'est | accesseur |
|---|---|---|---|
| `g_BlocStatsDebug` | **`0x180677330`** (objet global, pas alloue) | bloc de **comptes-rendus** que chaque tache remplit pour un afficheur de mise au point | `StatsDebug_obtenirBloc` = **`0x18006F350`** |
| `g_ptrGestRendu` | **`0x18070FC68`** (pointeur vers l'objet) | le **vrai** gestionnaire de rendu : octets d'activation des passes, cibles de rendu, liste de rappels, texture publiee | pas d'accesseur : adresse directe |

`StatsDebug_obtenirBloc` (`0x18006F350`) tient en une instruction :

    undefined * FUN_18006f350(void) { return &DAT_180677330; }

**Fait mesure, et c'est lui qui rend l'enquete decidable** : `0x180677330` n'a
**qu'une seule** reference croisee dans toute l'image — `0x18006F350`. Donc
*aucun* code n'adresse ce bloc autrement qu'en appelant l'accesseur. Le champ de
40 appelants est donc le champ **complet** des utilisateurs du bloc, pas un
echantillon.

Le bloc n'est pas entierement mort : `FUN_18018F680` **lit** `*(octet*)(bloc+4) & 2`
et **ecrit** `bloc+0x790` (un compte) et `bloc+0x7A0..` (8 identifiants). Le bloc
va donc au moins jusqu'a `0x7C0`. C'est la **zone `+0x300..+0x350`** qui est
morte, pas le bloc.

---

## 2. La carte de `g_BlocStatsDebug` `+0x320`..`+0x340` (et ses bords utiles)

Tous les deplacements ci-dessous sont **des ecritures**. La colonne « lu par »
est vide partout, et la section 3 dit comment c'est etabli.

| depl. | taille | valeur ecrite | ecrit par | lu par |
|---|---|---|---|---|
| `+0x300` | 4 | `1` | `0x1800747D0`, `0x180074AB0` | — |
| `+0x308` | 4 | `6000` | idem | — |
| `+0x30C` | 4 | `6000` | idem | — |
| `+0x310` | 8 | pointeur de tampon d'ombres | idem | — |
| `+0x318` | 4 | `0x4B0` (1200) | idem | — |
| `+0x31C` | 4 | `compte * 3` (triangles) | idem | — |
| `+0x320` | 8 | pointeur | idem (`lVar6 + 800`) | — |
| **`+0x328`** | 4 | **`1`** quand la tache des ondes vit | **`TaskEffectRipple_chargerDecor`** `0x18007AE10` (site `0x18007B00C`) | **— personne** |
| **`+0x32C`** | 4 | **`(decor == 4)`** | idem (site `0x18007B019`) | **— personne** |
| `+0x328`..`+0x32F` | 8 | **`0`** d'un coup (un seul `mov qword`) | **`TaskEffectRipple_dest`** `0x18007A700` (site `0x18007A76F`) | — |
| `+0x330` | 4 | `1` / `0` (WATER\_RING) | `0x180085640` (`init`) / `0x1800855F0` (`dest`) | — (deja prouve non lu par point d'arret, `eau_slk_console.md`) |
| `+0x334` | — | **aucune ecriture observee** | — | — |
| `+0x338` | 4 | indice de descripteur de la **cible de rendu des ondes** | **`TaskEffectRipple_majParImage`** `0x18007A600` | — |
| `+0x33C` | 4 | **largeur** de cette cible | idem | — |
| `+0x340` | 4 | **hauteur** de cette cible | idem | — |
| `+0x344` | — | aucune ecriture observee | — | — |
| `+0x348` | 4 | indice de descripteur de la **texture d'emetteur** | idem | — |
| `+0x34C` | 4 | largeur | idem | — |
| `+0x350` | 4 | hauteur | idem | — |

Deux remarques **lues**, non deduites :

* `+0x300..+0x320` et `+0x328..+0x350` ont **exactement la meme forme** :
  « present oui/non », puis « capacite », puis « ce qui est dedans ». Les deux
  ecrivains de `+0x300` (`0x1800747D0` et `0x180074AB0`) ecrivent la **meme**
  sequence de sept champs, mot pour mot. C'est une **page de statistiques**.
* `+0x338` ne contient pas un identifiant de texture mais
  `FUN_180254550(texture->+0x10)`, soit `*(u32*)(table + (id-1)*0x98 + 0xE3CC8)` :
  un **indice dans la table des descripteurs**. Une valeur bonne a *afficher*,
  pas a *lier*.

**Ce que j'en deduis** (et c'est une deduction, pas une lecture) : la zone
`+0x300..+0x350` de `g_BlocStatsDebug` est la page de mise au point « memoire /
effets » d'un build de developpement ; dans le build Retail APM3 le lecteur a
ete retire a la compilation, les ecrivains non.

---

## 3. Point 2 : le consommateur de `+0x328` et `+0x32C` — **il n'y en a pas**

La preuve se fait en trois pas, chacun verifiable :

1. **`0x180677330` n'a qu'une reference** : `0x18006F350`. Donc tout porteur du
   pointeur l'obtient de l'accesseur.
2. **Balayage d'octets sur toute `.text`** (`0x180001000`..`0x180340000`,
   3 403 777 octets, recherche complete, pas echantillonnee) du deplacement sur
   32 bits :
   * `0x328` (`28 03 00 00`) : **76 occurrences**. Intersection avec les
     40 appelants de l'accesseur : **deux**, `0x18007AE10` et `0x18007A700` —
     les deux ecrivains.
   * `0x32C` (`2C 03 00 00`) : 45 occurrences. Intersection : **une**,
     `0x18007AE10`.
   * `0x338` (`38 03 00 00`) : 65 occurrences. Intersection : **une seule
     apparente**, `0x18018F680` au site `0x18018F7C0` — et c'est un **faux
     positif** : les octets lus la sont `0F 85 38 03 00 00`, c'est le `rel32`
     d'un `jnz`, pas un deplacement de structure. (Verifie par lecture d'octets
     a `0x18018F7B4`.)
   * `0x348` (`48 03 00 00`) : 67 occurrences. Intersection : **une**,
     `0x18007A600` — l'ecrivain.
3. **Balayage masque** `20 03 00 00` / masque `E0 FF FF FF` (donc tout
   `0x320`..`0x33F`) sur `0x18006F000`..`0x1800C4000` : parmi les appelants de
   l'accesseur, seuls `0x1800747D0`, `0x180074AB0`, `0x18007A600`,
   `0x18007A700`, `0x18007AE10`, `0x1800855F0`, `0x180085640` touchent cette
   fenetre. **Tous en ecriture.**

> **Le piege que ca evite.** La consigne disait justement qu'un balayage du
> deplacement `0x328` avait trouve 40 acces et ne concluait rien, « le
> deplacement appartenant a des dizaines d'objets ». C'est vrai, et c'est
> pourquoi le balayage seul ne suffit pas : ce qui tranche, c'est
> **l'intersection du balayage avec le champ clos des 40 appelants**, lui-meme
> clos parce que le global n'a qu'une reference. Les deux faits se tiennent
> ensemble ; aucun ne suffit seul.
>
> **La limite honnete qui reste** : un appelant pourrait passer le pointeur en
> argument a une fonction qui, elle, lit `+0x328`. Je n'ai **pas** decompile les
> 40 appelants pour l'exclure un par un. Ce qui l'exclut en pratique : les deux
> fonctions a l'exterieur du champ qui ecrivent une forme de descripteur en
> `+0x320/+0x328/+0x338/+0x348` (`FUN_18007D300`, `FUN_180083D50`) travaillent
> sur un **autre** objet — `FUN_18007D300` est un constructeur qui met a zero
> `0x5D0 + 0xC*0x100` octets d'affilee, verifie. Voir « CE QUI N'EST PAS
> MESURE ».

---

## 4. Point 3 : le rappel de dessin, et le chemin complet de la tache au pixel

### 4.1 `LAB_18007B470` est un **tremplin de 5 octets**

C'est pour ca que Ghidra n'en fait pas une fonction. Octets lus a
`0x18007B470` : `E9 FB FB FF FF` = `jmp 0x18007B070`. Un tremplin d'edition de
liens incrementale. Le vrai corps est a **`0x18007B070`**, et Ghidra le connait
tres bien sous ce nom.

* `thunk_TaskEffectRipple_dessiner` = `0x18007B470`
* **`TaskEffectRipple_dessiner` = `0x18007B070`**

### 4.2 Le chemin, fonction par fonction, avec son nom neuf

| # | nom neuf | adresse | role **lu** |
|---|---|---|---|
| 1 | `TaskEffectRipple_init` | `0x18007B030` | 52 octets : appelle le vtable `+0x58`, puis `chargerDecor(g_TaskEffectRipple, decor)`, puis trace `"TaskEffectRipple::init()\n"` |
| 2 | `TaskEffectRipple_chargerDecor` | `0x18007AE10` | recopie l'enregistrement de decor ; `GestRendu_activerPasse(4,1)` ; **inscrit le rappel** ; alloue les deux chaines ; ecrit la page de stats `+0x328/+0x32C` |
| 3 | `GestRendu_activerPasse` | `0x18010CA20` | **une instruction** : `*(octet*)(g_ptrGestRendu + n) = v`. L'octet `[+4]` est l'interrupteur de la **passe 4** |
| 4 | `GestRendu_inscrireRappelPasse4` | `0x18010BDC0` | pousse `{0, &thunk…, tache}` dans la **liste** a `g_ptrGestRendu + 0x400` |
| 5 | `GestRendu_executerToutesLesPasses` | `0x18010C230` | boucle `i = 0..15`, appelle la passe `i` |
| 6 | `GestRendu_executerPasse` | `0x18010C330` | **garde en tete de fonction** : `if (*(char*)(g_ptrGestRendu + i) == 0) return;` — c'est l'octet du n° 3. Puis `switch(i)`. **`case 4:` parcourt la liste de `+0x400` et appelle `(*(code*)n[3])(n[4])`** |
| 7 | **`TaskEffectRipple_dessiner`** | **`0x18007B070`** | voir 4.3 |
| 8 | `GestRendu_obtenirCibleRendu` | `0x18010BEF0` | `((DAT_1803A50E0[ *(int*)(gest+0x15C+i*4) + i*3 ] + 7) * 0x38) + gest` : les cibles vivent **dans** le gestionnaire |
| 9 | `Ondes_deriverNormale` | `0x1800D22B0` | prend **trois** cibles + 4 flottants, appelle `FUN_1800D2340` : c'est la passe qui fabrique la **normale** a partir de trois etats de hauteur |
| 10 | `GestRendu_publierTextureOndes` | `0x18010CA10` | **une instruction** : `*(u64*)(g_ptrGestRendu + 0x410) = texture` |
| 11 | `GestRendu_obtenirTextureOndes` | `0x18010BEC0` | **une instruction** : `return *(u64*)(g_ptrGestRendu + 0x410)` |
| 12 | `GestRendu_passe7_sceneOpaque` | `0x18010B1F0` | **LIT `+0x410`** et **lie la texture** autour du dessin de la scene (voir 4.4) |
| 13 | `GestRendu_passe9_composition` | `0x180103510` | **LIT `+0x410`** deux fois, via `GestRendu_obtenirTextureOndes`, autour des programmes `0x14` et `0x13` |

Et le reste du cablage, lu : `TaskEffectRipple_majParImage` (`0x18007A600`) est
ce qui **arme** le rappel chaque image (`*(octet*)(tache+4) = 1`), et
`TaskEffectRipple_dest` (`0x18007A700`) libere les deux chaines,
`GestRendu_activerPasse(4,0)` **eteint la passe**, et
`GestRendu_retirerRappelPasse4` (`0x18010BE60`) desinscrit le rappel.

### 4.3 Ce que fait vraiment `TaskEffectRipple_dessiner` (`0x18007B070`)

Decompile en entier. Dans l'ordre :

1. Prend **trois** cibles de rendu : `GestRendu_obtenirCibleRendu(base + 0..2)`,
   ou `base = 2` si `*(char*)(tache+0x28) != 0`, sinon **`5`**. Triple tampon.
2. **Garde :** `if (*(char*)(tache + 4) != 0) { … }`. Tout le corps de
   simulation est sous cette garde. L'octet est pose a `1` par
   `TaskEffectRipple_majParImage` et remis a `0` **a la fin** du rappel : c'est
   un **coup unique par image**, pas un interrupteur persistant.
3. Avance le compteur `tache+0xB158` modulo 3, fixe la cible courante
   (`FUN_18010CCA0`), l'efface (`FUN_18010D240`), ouvre une passe
   (`FUN_180248BC0(0x82800)`), cadre et ciseaux sur `largeur-2 / hauteur-2`.
4. **Le pas de simulation** : `if (FUN_1800EC090(0x16) != 0)` — programme de
   nuanceur **`0x16` = 22**. Si present : groupe `0x224`, emplacement **`0x11E`**
   = *la cible precedente*, puis `FUN_1800EA4C0(0x16,0,0)` = le dessin. Donc la
   hauteur d'eau se propage en lisant l'etat precedent et en ecrivant l'etat
   courant. **Si le programme 22 n'est pas monte, ce pas est saute en silence.**
5. **Le pas de normale** : seconde passe (`0x82000`), ecrit quatre flottants a
   `tache+0xB160..0xB16F` (les deux premiers viennent de l'enregistrement de
   decor, les deux derniers sont `{5e-5, 0.999}` si `*(int*)(tache+0x2C) > 0` —
   et `chargerDecor` y met `0x3C` = 60, donc **c'est toujours cette branche**),
   puis **`Ondes_deriverNormale(cible[i+2], cible[i+1], cible[i], tache+0xB160)`**.
6. **L'emetteur** : si `*(int*)(tache+0x24) != -1` et que `FUN_1801957A0`
   resout la texture, il **recopie cette texture dans la cible** via
   `FUN_1800D1FA0`, a l'echelle `{1,1}`.
7. **Et pour finir, hors de la garde du 2** :
   `GestRendu_publierTextureOndes(cible[(compteur+2)%3]->+8)`, puis
   `*(octet*)(tache+4) = 0`.

**Reponses aux trois questions du point 3** :
* **Textures liees** : l'etat precedent des ondes, a l'emplacement `0x11E` du
  groupe `0x224` ; et, s'il existe, la texture d'emetteur `tache+0x24`.
* **Nuanceur demande** : le programme **`0x16` (22)** pour la propagation, et
  `FUN_1800D2340` pour la derivation de normale.
* **Ecrit-il dans une cible de rendu ?** **Oui.** Dans l'une des trois cibles du
  groupe `2..4` ou `5..7`, celle que designe `(tache+0xB158)`. Et **oui**, elle
  est relue ensuite comme texture — par les deux passes du 4.4.

### 4.4 Qui la relit — la reponse qui manquait

`GestRendu_passe7_sceneOpaque` (`0x18010B1F0`), **lu tel quel** :

    if (*(longlong *)(gest + 0x410) != 0) {
      FUN_180256d50(0x22b);
      FUN_180256da0(*(u32*)(*(longlong*)(gest+0x410) + 0x14),      // emplacement
                    *(u32*)(*(longlong*)(gest+0x410) + 0x10));     // texture
      FUN_180256d50(0x21d);
    }
    …  tout le dessin de la scene opaque  …
    if (*(longlong *)(gest + 0x410) != 0) {
      FUN_180256d50(0x22b);
      FUN_180256da0(*(u32*)(*(longlong*)(gest+0x410) + 0x14), 0);  // on delie
    }

La texture des ondes est donc **liee en global autour de toute la scene
opaque**, a l'emplacement que l'objet texture **declare lui-meme** en `+0x14`.
`GestRendu_passe9_composition` (`0x180103510`) fait la meme chose deux fois,
autour des programmes `0x14` et `0x13`, en passant par
`GestRendu_obtenirTextureOndes`.

`GestRendu_obtenirTextureOndes` (`0x18010BEC0`) n'a **qu'un appelant** :
`0x180103510`. Et `+0x410` n'est lu en direct que dans `0x18010B1F0`. Donc les
consommateurs sont **exactement deux**, et ils sont tous les deux des passes de
rendu reellement reparties par `0x18010C330`.

### 4.5 La passe 4 est-elle reellement repartie ? **Oui**

`GestRendu_executerToutesLesPasses` (`0x18010C230`) boucle `i = 0..15`.
J'ai deroule le filtre a la main pour `i = 4`, sur les quatre branches :

* `bVar2` vaut `true` seulement si `i == 0 || (i > 1 && (i < 4 || i-5 < 5))`.
  Pour `i = 4` : `i < 4` faux, `4-5` non signe = `0xFFFFFFFF`, pas `< 5`.
  Donc **`bVar2 = false`**.
* Les trois branches de `[DAT_180c3b6f0 + 0x626] == 0` menent toutes a
  `LAB_18010C2D9` pour `i = 4` (`i == 0xB` faux, `i-0xD < 2` faux,
  `5 < i-10` vrai, `3 < i-0xB` vrai), et `LAB_18010C2D9` fait
  `if (!bVar2) goto appel`.
* La branche `[+0x626] != 0` tombe directement sur `LAB_18010C2D9`.

**Dans les quatre cas, `FUN_18010C330(4)` est appele.** La passe 4 n'est donc
jamais filtree a ce niveau ; la seule garde qui reste est l'octet
`g_ptrGestRendu[4]`, que `chargerDecor` allume et que `dest` eteint.

---

## 5. Point 4 : les deux chaines de 14 x `0x14` octets

`chargerDecor` alloue **deux** chaines (boucle `lVar9 = 2`) de
`14 * 0x14` octets, rangees **dans la tache**, a `tache+0xB110` et
`tache+0xB118` ; le compte 14 est a `tache+0xB108`. Deux chaines = **un
combattant chacune** (c'est une deduction ; ce qui est lu, c'est « deux »).

Chaque element fait `0x14` octets. Mis a `{-1, 0, 0, 0, 0}` puis rempli :

| depl. | source | contenu |
|---|---|---|
| `+0x00` | `DAT_180350E30[i]` | **identifiant de noeud du squelette** |
| `+0x04` | `DAT_180350E68[i]` | **rayon** de l'onde, en flottant |
| `+0x08`..`+0x13` | remis a zero | 12 octets de travail (non identifies) |

Les deux tables, **octets lus** a `0x180350E30` (14 entiers, `0x38` octets) et
`0x180350E68` (14 flottants, `0x38` octets) — elles sont contigues :

| i | noeud | rayon |
|---|---|---|
| 0 | 5 | 0,22 |
| 1 | 10 | 0,20 |
| 2 | 71 | 0,12 |
| 3 | 100 | 0,12 |
| 4 | 72 | 0,10 |
| 5 | 101 | 0,10 |
| 6 | 73 | 0,08 |
| 7 | 102 | 0,08 |
| 8 | 133 | 0,12 |
| 9 | 139 | 0,12 |
| 10 | 131 | 0,12 |
| 11 | 137 | 0,12 |
| 12 | 132 | 0,08 |
| 13 | 138 | 0,08 |

**A quoi ca sert** : ce sont les **points du squelette qui emettent une onde**,
avec le rayon de chacun. La structure par paires est lue, pas supposee :
`(71,100)`, `(72,101)`, `(73,102)`, `(133,139)`, `(131,137)`, `(132,138)` — six
paires au rayon **identique** dans la paire, et de rayon decroissant 0,12 →
0,10 → 0,08 le long d'une chaine. Les deux premieres (`5` a 0,22 et `10` a 0,20)
sont seules et ont les plus gros rayons. **Ce que j'en deduis** : `5` et `10`
sont le bassin et le torse, `71/72/73` et `100/101/102` les deux jambes
(cuisse / tibia / pied, rayon qui diminue), `131..139` les deux bras. Je n'ai
**pas** verifie ces numeros contre la table de noeuds d'`AUTH_3D`.

---

## 6. L'enregistrement de decor : `0x1806432E0`, et une trouvaille

`chargerDecor` compare `param_2` a `DAT_1806432E0[0]` et a `DAT_18064330C[0]`,
et **sort sans rien faire** si aucun ne correspond. Deux enregistrements de
`0x2C` octets, contigus. Octets lus :

| depl. | enregistrement 0 (`0x1806432E0`) | enregistrement 1 (`0x18064330C`) | va dans |
|---|---|---|---|
| `+0x00` | **decor 4** | **decor 15** | la comparaison |
| `+0x04` | 0,4 | 0,4 | `tache+0x08` |
| `+0x08` | 0,8 | 0,8 | `tache+0x0C` |
| `+0x0C` | 0,02 | 0,1 | `tache+0x10` |
| `+0x10` | 0,1643 | 0,1904 | `tache+0x18` |
| `+0x14` | 0,56 | 0,505 | `tache+0x1C` |
| `+0x18` | 1,0 | 1,0 | `tache+0xB160` |
| `+0x1C` | **-1** | **9207** | `tache+0x24` (**id de texture d'emetteur**) |
| `+0x20` | 0 | 1 | `tache+0x28` (choix du groupe de cibles : **5** ou **2**) |
| `+0x24` | 1,0 | 4,0 | `tache+0x30` |

Et voila le point qui compte pour le decor d'Eileen :

> **L'enregistrement du decor 15 porte la texture `9207`.** D'apres les mesures
> deja au dossier, `9207` = `F_VF5S_SLK00_KA_WATER_N`, la normale **plate** du
> materiau d'eau de `slk`. Ce n'est donc **pas** une normale que la tache est
> censee remplacer : c'est la texture que la tache **recopie dans sa cible**
> (etape 6 du 4.3) comme **graine** de la simulation. **Le decor 15 de la table
> d'origine est le decor d'eau de `slk`.**

Aussi : `tache+0x28` vaut 1 pour le decor 15, donc le groupe de cibles est
**`2,3,4`**, et pas `5,6,7`. Les deux decors n'utilisent pas le meme triplet.

---

## 7. Point 5 : conclusion

**Non, la tache des ondes n'est pas un producteur sans consommateur.** Son
produit — la cible de rendu qui contient la hauteur puis la normale — est
**publie** par `GestRendu_publierTextureOndes` (`0x18010CA10`) dans
`g_ptrGestRendu+0x410`, et **lu** par deux passes qui le **lient comme texture**
autour de leurs dessins : `GestRendu_passe7_sceneOpaque` (`0x18010B1F0`) et
`GestRendu_passe9_composition` (`0x180103510`). La passe 4 est reellement
repartie par `0x18010C330`, sous la seule garde de l'octet `g_ptrGestRendu[4]`
que `chargerDecor` allume.

**Ce qui est bien un producteur sans consommateur, c'est la page de
statistiques** : `g_BlocStatsDebug+0x300..+0x350`, et donc `+0x328`, `+0x32C`,
`+0x338`, `+0x340`, `+0x348`, exactement comme `+0x330`. **Cesser de les
regarder.** Ce ne sont pas des interrupteurs ; les allumer ne changerait rien, et
les voir allumes ne prouve rien d'autre que « la tache s'est initialisee » —
ce qu'on savait deja.

### Ou l'eau peut encore se perdre, et comment le verifier **sans lancer**

Quatre endroits, par ordre de cout de verification. Chacun est un **fait
statique**, lisible sur disque.

1. **L'octet d'activation de la passe 4** (`g_ptrGestRendu[4]`). Il n'est allume
   que si `chargerDecor` **atteint sa fin**, donc seulement si l'identifiant de
   decor vaut `DAT_1806432E0[0]` ou `DAT_18064330C[0]`. Dans l'image d'origine
   ce sont **4 et 15**. *Verification* : lire ces deux mots dans l'image
   **patchee** (`.greffe`) et les comparer a l'identifiant reel du decor
   d'Eileen tel qu'il est passe a `TaskEffectRipple_init` via
   `param_1[0xB]`. Si le balayage a mis 53 et 72 dans la table mais que le
   decor sert sous un autre numero, `chargerDecor` sort avant tout, et
   **`+0x328` resterait a 0** — or la consigne dit que la tache s'initialise ;
   il faudrait verifier **lequel** des deux faits est vrai, car
   `TaskEffectRipple_init` trace `"init()"` **meme quand `chargerDecor` est
   sorti a vide** (la trace est **apres** l'appel, pas dedans). **Le journal
   `init()` ne prouve donc pas que la tache s'est chargee.** C'est le piege le
   plus probable, et il ne coute pas une course.
2. **Le programme de nuanceur `0x16` (22).** `FUN_1800EC090(0x16)` lit
   `*(u32*)(DAT_18070F6A0 + 0x38 + 0x16*0x30)`. S'il rend 0, le pas de
   propagation est saute **sans un mot**, la cible garde son contenu, et la
   normale derivee est plate. *Verification* : etablir a quel programme
   l'indice 22 correspond dans la table des programmes, et confirmer que c'est
   bien `ripple.0.vp`/`ripple.0.fp`. Les notes disent les nuanceurs « montes »
   1/1 et 2/2 — **montes** et **a l'indice 22** ne sont pas la meme chose.
   C'est le second controle a faire.
3. **Le groupe de cibles de rendu.** Pour le decor 15, `tache+0x28 = 1`, donc
   `GestRendu_obtenirCibleRendu(2)`, `(3)`, `(4)`. Ces trois cibles existent-elles ?
   *Verification* : lire `DAT_1803A50E0` et les indices
   `g_ptrGestRendu+0x15C+i*4` pour `i = 2,3,4`, et verifier que
   `FUN_18010BEF0` tombe sur des descripteurs alloues et non sur l'entree 0.
4. **L'emplacement de liaison.** `0x18010B1F0` lie la texture a l'emplacement
   que l'objet texture declare en `+0x14`. **Il faut que le materiau d'eau lise
   cet emplacement-la.** Les notes au dossier disent que le materiau d'eau de
   `slk` porte `9207` **en emplacement 2**. Si le materiau fixe lui-meme son
   emplacement 2 apres la liaison globale, il **ecrase** la normale des ondes
   par la normale plate, et tout le reste de la chaine peut marcher sans que
   rien ne se voie. *Verification* : lire `texObj+0x14` pour une cible du
   groupe 2 et le comparer a l'emplacement que le nuanceur `WATER01` declare
   pour sa normale. C'est le controle qui tranche **vraiment** sur l'ecran.

---

## CE QUI N'EST PAS MESURE

Tout ce qui suit est une **absence de verification de ma part**, pas un fait.

* **Les noms n'ont pas pu etre poses dans la base.** Toutes mes huit tentatives
  `set_address_name` ont ete **refusees**, pas ignorees :
  `capability_unavailable` / `"Windows Ghidra P0 does not admit database
  mutation"`. Les noms neufs de cette note ne vivent donc **que dans cette
  note**. Refus et absence ne sont pas la meme chose : rien n'a ete renomme,
  et rien n'a echoue silencieusement.
* **Je n'ai pas decompile les 40 appelants** de `StatsDebug_obtenirBloc` un par
  un. L'exclusion d'un lecteur de `+0x328` repose sur l'intersection
  balayage x champ clos (section 3), pas sur une lecture exhaustive. Un appelant
  qui **passerait le pointeur en argument** a une fonction lisant `+0x328`
  echapperait a mon controle. Je le crois tres improbable — le bloc est un
  global a accesseur, pas un objet qui circule — mais je ne l'ai pas prouve.
* **Je n'ai pas verifie que `FUN_18010C230` est appele chaque image.** J'ai
  prouve que, **s'il** est appele, la passe 4 passe le filtre. Son appelant n'a
  pas ete remonte.
* **L'identite de `FUN_1800D2340`** (le vrai dessin de derivation de normale,
  appele par `Ondes_deriverNormale`) n'a pas ete decompilee. Je dis « derive une
  normale a partir de trois etats » **parce que** `0x1800D22B0` recoit trois
  cibles et quatre flottants, pas parce que j'ai lu le nuanceur.
* **Les numeros de noeuds du squelette** (5, 10, 71..73, 100..102, 131..139)
  n'ont pas ete confrontes a la table de noeuds d'`AUTH_3D`. Bassin / torse /
  jambes / bras est une **lecture de la structure par paires et des rayons**,
  pas une correspondance etablie.
* **Que `9207` soit `F_VF5S_SLK00_KA_WATER_N`** est repris des notes
  anterieures, pas revrifie par moi dans cette session. Ce que j'ai lu, c'est le
  nombre `0x23F7` a `0x18064332C`.
* **L'identifiant reel du decor d'Eileen** dans ce build, et donc le point 1 de
  la section 7, n'est **pas** verifie. Je n'ai lu que l'image d'origine : la
  table y contient 4 et 15. Ce que le balayage a mis dans `.greffe`, et sous
  quel numero le decor d'Eileen se charge, reste a lire.
* **L'indice 22 du programme de nuanceur** n'a pas ete relie a `ripple.0.fp`.
* **`g_BlocStatsDebug+0x334` et `+0x344`** : je n'ai trouve **aucun** ecrivain.
  Ca peut vouloir dire « champ non utilise », ou « ecrivain que mon balayage n'a
  pas vu » (un acces par registre d'index, par exemple, que la recherche d'un
  deplacement sur 32 bits ne voit pas). Je n'ai pas tranche.
* **Rien n'a ete execute.** Aucune des quatre verifications de la section 7
  n'exige de lancer le jeu ; aucune n'a ete faite ici.
