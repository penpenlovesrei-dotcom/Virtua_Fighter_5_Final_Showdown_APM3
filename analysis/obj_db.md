# `obj_db.bin` — les jeux d'objets, et la carte est complète

Établi le 2026-09-09. Outil : **`tools/obj_db.py`**.
Complète `analysis/ajouter_un_decor.md` §1, qui laissait une « zone non
expliquée ».

C'est la base qui décide de la faisabilité d'un décor ajouté : l'identifiant
d'objset qu'un descripteur demande en `+0x10` est cherché ici, par dichotomie
dans un vecteur construit au démarrage (`0x1800F9450`, rempli par `0x18006B7E0`
qui lit `./rom/objset/` + `obj_db.bin`).

---

## 1. La carte, et il n'y a plus de zone inexpliquée

```
0x000000   en-tête, huit u32
0x000020   POT A : les chaînes de la table des jeux      272 192 o
0x042760   table des JEUX D'OBJETS   6044 × 0x24         217 584 o
0x077950   POT B : les noms d'objets                     509 488 o
0x0F3F80   table des OBJETS          17744 × 8           141 952 o
0x116A00   fin du fichier, à l'octet près
```

§5 de `ajouter_un_decor.md` disait « la zone `0x77890`–`0x0F3F80` n'est pas
expliquée ». **C'est le second pot de chaînes**, et il commence exactement où
finit la table des jeux — `0x77950`, l'adresse notée était approchée. Le
premier nom qu'on y lit est `TEST_00A`, celui de l'objet 0.

| structure | champs |
|---|---|
| **en-tête** | `+0x00` nombre de jeux · `+0x04` `0x1805` · `+0x08` offset de leur table · `+0x0C` nombre d'objets · `+0x10` offset de leur table · le reste à zéro |
| **jeu** (0x24 o) | `+0x00` offset du nom · `+0x04` **identifiant** · `+0x08` `…_obj.bin` · `+0x0C` `…_tex.bin` · `+0x10` `….farc` · quatre u32 à zéro |
| **objet** (8 o) | `+0x00` **identifiant empaqueté** `(objset << 16) \| rang` · `+0x04` offset du nom |

L'empaquetage est **celui du descripteur de décor** : `djo` demande
`0x1C0072 0x1C0076 0x1C0075 0x1C0074 0x1C0073`, soit objset 28, rangs
114 118 117 116 115 — `STGDJO_GND`, `_RING`, `_SKY`, `_SDW`, `_REFLECT`.
L'objset 28 porte **171 objets** ; le descripteur n'en nomme que cinq, les 166
autres sont des effets.

### Deux faits qui ne se devinent pas

* **Zéro est une valeur.** 191 jeux sur 6044 n'ont ni fichier d'objets, ni
  fichier de textures, ni archive : ce sont les objsets d'**items**
  (`AKIITM012`…), qui vivent dans l'archive d'un autre. Refuser le zéro faisait
  échouer la lecture dès le rang 70.
* **Ni l'une ni l'autre table n'est triée.** On peut donc ajouter à la fin sans
  rien réordonner — le moteur construit son index trié au démarrage.

---

## 2. La réécriture, et pourquoi elle est sûre

Les deux pots sont gardés **tels quels, en octets**, et on n'y ajoute qu'à la
fin. Les offsets du pot A ne bougent donc jamais (il commence à `0x20` avant
comme après) ; ceux du pot B se décalent d'une quantité connue — la croissance
du pot A plus les entrées de jeu ajoutées.

Sans ajout, le décalage est nul et le fichier ressort **identique à l'octet
près** :

```
py -3 tools/obj_db.py --essai
   1141248 octets ; 6044 jeux d objets ; 17744 objets
   pot A 272192 octets, pot B 509488 octets
   reecrit : 1141248 octets
   ALLER-RETOUR IDENTIQUE A L OCTET PRES.
```

---

## 3. Ajouter un jeu d'objets

```
py -3 tools/obj_db.py --montrer STGDJO
py -3 tools/obj_db.py --libres
py -3 tools/obj_db.py --ajouter STG5RD --id 6150 --depuis STGDJO \
                      --fichiers stg5rd --sortie <fichier>
```

Mesuré : un décor complet coûte **5 769 octets** — une entrée de jeu, 171
entrées d'objet, et leurs noms dans les deux pots. Le fichier produit se relit
et se réécrit à l'octet près.

**Les noms d'objets sont recopiés VERBATIM.** Une archive importée puis
renommée garde ses noms internes : seuls les **deux** noms de fichier changent,
et c'est `importer_decor.py --vers` qui les réécrit dans l'en-tête du `FArC`.

### Les identifiants : troués, non bornés, et il en reste

6044 jeux, identifiants de 0 à 6149, **66 plages libres**. La plus confortable
commence à **6150** et rien ne la borne. C'est déjà ce que le studio a fait :
`du5`, `gym` et `smo` portent 5529, 2847 et 2848, pris ailleurs.

### Un garde-fou qui a servi tout de suite

`--ajouter STGTRS` est **refusé** : `STGTRS` existe déjà, identifiant 44. Les
41 emplacements de décor ont tous leur entrée dans `obj_db` — c'est précisément
pourquoi `importer_decor.py --vers trs` fonctionnait côté fichiers sans toucher
à cette base. Un décor **vraiment** ajouté, lui, a besoin d'un nom neuf.

---

## 4. Ce qui reste

* le champ `+0x04` de l'en-tête vaut `0x1805` — une version, jamais vérifiée ;
* les quatre u32 à zéro de chaque jeu ne sont expliqués par rien ;
* **`tex_db.bin`** est la dernière des trois. Même famille (compte + table +
  pot), 841 776 octets, en-tête `0x6588` entrées à `0x9ABF0`.
