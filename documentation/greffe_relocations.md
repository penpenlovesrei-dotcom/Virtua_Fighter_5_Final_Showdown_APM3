# Greffer une section AVEC ses relocations

Établi le 2026-09-09 sur `vf5fs-pxd-w64-Retail_APM3.dll.origine`.
Outil : **`tools/pe_sections.py`** (`--essai` pour l'auto-contrôle,
`--etat <dll>` pour l'inventaire).

C'est la **clé de voûte du vrai ajout de décors**. Tant qu'une section greffée
n'avait pas de relocations, aucun descripteur de décor ne pouvait y vivre.

---

## 1. La contrainte qu'on payait depuis le début

La DLL est **rebasée** à l'exécution — mesuré trois fois, à trois adresses
différentes (`0x7FFDB0620000` le 2026-09-08, `0x7FFC81C70000` aujourd'hui).
Une section ajoutée après coup n'apparaît dans **aucun** bloc de la table de
relocations : une adresse d'image qu'on y écrit reste à la base préférée
`0x180000000` et ne désigne plus rien une fois le module chargé.

D'où la règle qui encadrait toute la greffe de `--variantes` : *aucun pointeur
absolu, tout en RIP-relatif, les tables de chaînes à pas fixe*.

Elle a fini par bloquer le chantier des décors, et pas à la marge :

| ce qui manquait | conséquence |
|---|---|
| `+0xC0` — la table des **murs** | un dojo sans murs : ring-out là où il n'y en a pas |
| `+0x70`…`+0xB0` — les neuf reprises de musique | seule la piste principale joue |
| `+0x00` / `+0x08` — les noms `STGxxx` / `EFFSTGxxx` | on ne pouvait pas nommer l'auth_3d d'un décor neuf |

Un descripteur de décor porte **dix-sept** pointeurs ; un emplacement d'essai
n'en a que **sept** relogés. Le clonage statique laissait donc dix champs à
zéro. Ce n'est pas une limite du chantier : c'est une limite du format, et
c'est elle qu'on lève ici.

---

## 2. La levée : la table de relocations est un couple, pas une section

Le chargeur ne cherche pas la section `.reloc`. Il lit le **répertoire de
données n° 5**, un couple *(RVA, taille)* à `optional_header + 152` en PE32+.
La table peut donc vivre **n'importe où**.

La recette tient en quatre gestes :

1. lire les **209 blocs** d'origine — 29 643 entrées utiles ;
2. y ajouter les nôtres, groupées par page de 4 Ko, type **10 (`DIR64`)` ;
3. écrire le tout dans une section neuve (`.reloc2`) ;
4. repointer le répertoire.

Deux détails du format qui ne pardonnent pas :

* la taille d'un bloc **doit être un multiple de quatre** — on complète par une
  entrée `ABSOLUTE` (type 0) quand le nombre d'entrées est impair. C'est ce que
  fait l'éditeur de liens ;
* les pages doivent croître. Nos sections étant les dernières de l'image, il
  suffit d'ajouter nos blocs à la fin.

### Pourquoi pas le mou de `.reloc` ?

Il existe : `.reloc` fait 61 112 octets utiles pour 61 440 bruts, soit **328
octets** libres. C'est assez pour une poignée de blocs, pas pour une table de
décors — 128 descripteurs demandent plus de deux mille entrées. Et une table
qu'on agrandit en place casse le jour où elle déborde, sans rien dire.

---

## 3. La place disponible

```
6 sections d'origine, et 184 octets libres entre la fin de la table des
sections (0x348) et le premier octet de données (0x400)
   -> quatre en-têtes de section de plus, à 40 octets pièce
```

Trois sont désormais prévues, et **l'ordre compte** :

| ordre | section | qui la pose | pourquoi cet ordre |
|---|---|---|---|
| 1 | `.greffe` | `patch_moteur.py` | ses réglages sont documentés à des adresses fixes (`0x180EA1618`…) : elle doit rester en `0x180EA1000` |
| 2 | `.decors` | le chantier des décors | tables de descripteurs, de codes, de chaînes |
| 3 | `.reloc2` | `pe_sections.py` | la table reconstruite, **posée en dernier** puisqu'elle décrit les deux autres |

Une quatrième reste libre.

---

## 4. Ce qui est vérifié, et comment

`py -3 tools/pe_sections.py --essai` travaille sur une copie de `.origine` et
relit le résultat **avec `pefile`** — l'outil qui écrit ne doit pas être celui
qui se donne raison :

```
origine : 6 sections, 29643 relocations utiles
greffe  : .decors en 0x180EA1000, 65536 octets
reloc   : table reecrite en RVA 0xEB1000, 61136 octets
apres   : 8 sections, 29646 relocations utiles
rebasage simule : 3 pointeurs corriges dans .decors
AUCUNE FAUTE.
```

Les trois témoins sont placés exprès : un au début d'une page, un au milieu, et
un en `0xFF8` — le cas limite, huit octets qui finissent exactement sur la fin
de page.

### Et le contrôle qui compte : le chargeur de Windows

Le format bien écrit ne prouve pas que le chargeur l'accepte. On a donc greffé
`.decors` sur la DLL **déjà patchée** du build console, écrit `0x180403430` en
dur dedans, reconstruit la table, lancé le jeu, et lu la mémoire du processus :

```
vfes.exe pid 19648 ; moteur charge en 0x7FFC81C70000
delta de rebasage : 0x7FFB01C70000
  temoin en 0x7FFC82B12000 : 0x7FFC82073430
  attendu                  : 0x7FFC82073430
RELOCATION APPLIQUEE.
```

**Le jeu démarre avec neuf sections et une table de relocations reconstruite,
et notre pointeur absolu est corrigé comme ceux du jeu.** À partir d'ici, une
section greffée est une section comme une autre.

---

## 5. Ce que ça ouvre

* un **descripteur de décor complet** dans une section à nous, murs et musiques
  compris — plus de champs à mettre à zéro ;
* la **table des 41 descripteurs déplaçable** : il suffit de repointer les
  quatre `lea` qui la chargent et de lever les huit bornes (voir
  `analysis/ajouter_un_decor.md` §3.3 et §4) ;
* la **table des codes à trois lettres** (`0x18039F7A0`), qui est une table de
  pointeurs — donc impossible à greffer sans relocations ;
* la **grille de sélection**, si elle doit dépasser 43 cases.

## 6. Ce que ça ne règle pas

Les **bases de données** restent à faire, et c'est là qu'est le travail :

| base | forme | état |
|---|---|---|
| `auth_3d_db.bin` | **TEXTE** — `#A3DA`, `category.74.value=STGDJO`, `uid.703.value=A S010A010_DJO_STG_01` | ajouter un décor = éditer du texte |
| `obj_db.bin` | compte + table de 0x24 o + pot de chaînes | lu (§`ajouter_un_decor.md` 1), à reconstruire |
| `tex_db.bin` | compte + table + pot de chaînes | même famille, pas encore ouvert |

Et la **somme de contrôle PE** n'est pas recalculée : Windows ne la vérifie que
pour les images noyau, et le jeu démarre. À noter, pas à corriger.
