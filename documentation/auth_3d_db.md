# `auth_3d_db.bin` — la base des jeux d'animation, et elle est en clair

Établi le 2026-09-09. Outil : **`tools/a3d_db.py`**.
Complète `analysis/ajouter_un_decor.md` §3.2, qui l'annonçait « pas encore
ouvert ».

---

## 1. C'est du TEXTE, et ça change tout

223 565 octets, 8 172 lignes, **zéro octet non imprimable**. Déclarer
l'animation d'un décor neuf n'est donc pas un format à rétro-concevoir : c'est
une édition de texte.

```
#A3DA__________
# date time was eliminated.
category.0.value=ADV
…
category.length=92
uid.0.category=ADV
uid.0.size=2960
uid.0.value=A A010A010_MON_ADV
…
uid.length=3469
```

| clé | ce que c'est |
|---|---|
| `category.<i>.value` | le nom d'une **archive** : `STGDJO` → `auth_3d/STGDJO.farc` |
| `uid.<j>.category` | à quelle archive appartient ce jeu d'animation |
| `uid.<j>.value` | `A <nom du .a3da>` — le `A ` de tête est un marqueur de type |
| `uid.<j>.size` | une taille par enregistrement |

92 catégories, 3 469 uids. **1 166 uids n'ont ni catégorie ni taille**, juste
une valeur : ils ne sont attachés à aucune archive.

Le moteur compose le chemin par **`auth_3d/%s.farc`** (`0x1803F9438`), et charge
la base depuis **`rom/auth_3d/auth_3d_db.bin`** (`0x180348C30`). Dans le `.par`
elle est sous le nom plat `auth_3d_db.bin`, compressée.

---

## 2. La règle qui commande tout : les clés sont triées comme des CHAÎNES

`category.10.value` vient **avant** `category.2.value`, et `category.length`
après `category.9.value` — « l » passe après les chiffres.

Ce n'est pas une curiosité de présentation : c'est ce qui permet de vérifier
qu'on a compris le format. `a3d_db.py` ne garde pas les lignes, il garde les
**paires**, et les réécrit triées. Si le tri est le bon, l'aller-retour rend le
fichier **identique à l'octet près** :

```
py -3 tools/a3d_db.py --essai
   223565 octets, 2 lignes d en-tete, 8169 paires
   92 categories, 3469 uids
   reecrit : 223565 octets
   ALLER-RETOUR IDENTIQUE A L OCTET PRES.
```

Tant que cet essai passe, on sait qu'on peut écrire dans ce fichier.

---

## 3. Ajouter l'animation d'un décor

```
py -3 tools/a3d_db.py --lister                 les 92 catégories
py -3 tools/a3d_db.py --montrer STGDJO         ses uids
py -3 tools/a3d_db.py --ajouter STGTRS --depuis STGDJO --sortie <fichier>
```

Le dojo, pour donner l'échelle :

```
STGDJO     : 3 uids  — S010A010_DJO_STG_01, _02, _03
EFFSTGDJO  : 6 uids  — STGDJO_EFF_DOWNKEMU, _FIRE, _FIRE_REFLECT,
                       _HATA, _KABE_REACT, _DASH
```

**Deux décisions de conception, et elles se justifient :**

* **la catégorie est insérée dans l'ordre alphabétique, et tout est
  renuméroté.** Les 92 d'origine sont classées par nom ; rien ne dit que le
  moteur ne fasse pas une dichotomie dessus, et on ne prend pas ce risque pour
  économiser vingt lignes ;
* **les uids sont ajoutés à la fin, sans rien renuméroter.** Ceux de `STGDJO`
  sont 703, 704, 705, au milieu des autres : le numéro d'un uid est un
  identifiant, pas un rang.

### Les noms de `.a3da` sont recopiés VERBATIM — c'est voulu

`importer_decor.py --vers` réécrit **les deux entrées de l'objset** dans
l'en-tête du `FArC`, **pas** les `.a3da` de l'archive d'animation. Une archive
importée puis renommée porte donc toujours `S010A010_DJO_STG_01`. Substituer le
code donnerait des noms qui n'existent dans aucune archive, et **le décor se
chargerait sans son animation, en silence**. `--renommer` le fait quand même,
pour le jour où l'archive sera réécrite aussi.

### Mesure : la substitution de catégorie fait 17 lignes

```
+ category.87.value=STGTRS      (et STGUMI STGYUK TAK VAN WOL décalées)
+ category.length=93
+ uid.3469/3470/3471 .category .size .value
+ uid.length=3472
```

Le fichier produit **se relit et se réécrit à l'octet près**.

---

## 4. Ce que ça ne dit pas encore

**Une seconde table nomme les mêmes archives, et personne ne la lit.**
`0x18054E180` porte **249 entrées de 16 octets** — `{const char* chemin;
size_t}` — dont les 93 `auth_3d/…`, puis `objset/…`, `rob/mot_…`,
`string_array`… La seconde valeur n'est pas le nombre d'uids (`adv` : 400 dans
la table, 12 uids dans la base) : c'est une taille ou un budget.

**Un balayage linéaire de toute la plage, `.text` et données comprises, ne
trouve AUCUNE référence.** C'est le genre d'affirmation qui demande un balayage
linéaire, et c'en est un — mais il reste à confirmer avant de s'y fier. Si la
table est morte, un décor ajouté n'a rien à y faire. Si elle ne l'est pas, elle
est la prochaine à étendre.

**Et `size` n'est pas expliqué.** Il est recopié du modèle. Pour un décor
importé dont les `.a3da` sont ceux du modèle, c'est exact par construction ;
pour une animation neuve, il faudra savoir ce que ce nombre compte.
