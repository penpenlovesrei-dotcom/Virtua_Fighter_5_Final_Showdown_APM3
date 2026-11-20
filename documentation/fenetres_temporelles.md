# Les 32 fenêtres temporelles — le verrou est ouvert

Session du 2026-09-02. Le premier des deux verrous durs du chantier `mothead` — *à quoi
servent les 32 fenêtres temporelles de l'état de mouvement* — cesse d'être hors d'atteinte.
Deux choses l'ont débloqué, dans cet ordre : **un combat qui tourne**, et **une erreur
d'adresse corrigée**.

---

## 1. L'erreur qui bloquait la recherche statique

La documentation situe l'état de mouvement à **`ROB+0x798`**. C'est vrai du build
**R.E.V.O.** Ce ne l'est **pas** du build **APM3**, celui qui tourne ici.

`MothApplyRecord` du build APM3 (**`0x180158B40`**, unique appelant `0x18015A350`) construit
le contexte des gestionnaires ainsi :

```
0x180158B4A   lea rax, [rdx + 0x440]        ; ctx[1]
0x180158B69   mov [rsp+0x20], rdx           ; ctx[0] = ROB
0x180158B62   lea rax, [rdx + 0x8a0]        ; ctx[2] = l'etat de mouvement
```

| | ctx[1] | ctx[2] = état |
|---|---|---|
| R.E.V.O. (2025) | `ROB+0x338` | `ROB+0x798` |
| **APM3 (2021)** | **`ROB+0x440`** | **`ROB+0x8A0`** |

Écart constant : **`0x108`**. Confiance : **CONFIRMED** (lu dans le code, et vérifié à
l'exécution — le ROB relevé au point d'arrêt donne bien, à `+0x8A0+0x154`, la valeur par
défaut `(0.0, -1.0, -1.0)` que `0x180162B90` écrit dans les fenêtres).

**C'est ce `0x108` qui expliquait l'impasse.** Les consommateurs des fenêtres ne tiennent pas
un pointeur sur l'état : ils tiennent le **ROB**, et adressent les fenêtres par des
déplacements **relatifs au ROB** — `[rdi+0x9F8]`, pas `[rdi+0x158]`. Une recherche menée sur
les offsets d'état, ou sur le mauvais offset de base, ne pouvait rien trouver.

`tools/oracle_handlers.py` passe encore `ST = 0x798` : c'est **sans effet sur ses résultats**,
puisqu'il fabrique lui-même le contexte et que les gestionnaires ne font qu'utiliser les
pointeurs reçus. Mais la constante y est fausse pour APM3.

---

## 2. Ce que l'exécution a montré

`tools/pister_etat.py` mène le jeu au combat, pose un point d'arrêt logiciel sur
`MothApplyRecord` pour y lire `rdx` (le ROB), puis arme des points d'arrêt **matériels** sur
les fenêtres et relève l'adresse de chaque accès.

```
ROB = 0x000002023C4C8850   etat de mouvement = 0x000002023C4C90F0
DR0 arme sur etat+0x154 (4 o, r) -- 57 thread(s)
```

Relevé, combat en cours, martelage des boutons (`analysis/pistage_fenetres.txt`) :

| Site | Rôle | Valeurs vues |
|---|---|---|
| `+0x15ECDB`, `+0x15ECF7`… | **copieur d'état**, recopie champ par champ, entièrement déroulée, appelée à chaque trame. 3 141 accès. Bruit pur. | — |
| `+0x1584B8`, `+0x1584CC`, `+0x1584D2` | second parcours régulier, valeurs par défaut | `0.0`, `-1.0` |
| **`+0x155B58`, `+0x155BE5`, `+0x155C00`, `+0x155C0B`** | **un gestionnaire de code `mothead`** : il **écrit** les fenêtres | `22.0`, `23.0`, `46.0`, `28.0` |
| **`+0x133522`, `+0x13431C`** | **de vrais consommateurs** | `-1.0`, `28.0` |

Deux acquis immédiats :

- **les fenêtres sont datées en trames**, en flottants — `22.0`, `23.0`, `28.0`, `46.0` sont
  des numéros de trame, pas des durées ni des angles ;
- le gestionnaire `0x180155B30` **borne la fin de fenêtre à la durée de l'animation** :
  `xmm2 = état+0x004 − 1.0f`, et si la fin dépasse `xmm2`, elle y est ramenée. Le champ
  `état+0x004` est donc la longueur de l'animation. Confiance : **SUPPORTED**.

Le gestionnaire lit sa charge utile en `s16` et remplit **deux fenêtres d'un coup** :

```
charge +0x00 -> fenetre 1 champ 0     charge +0x02 -> fenetre 0 champ 0
charge +0x06 -> fenetre 1 champ 1     charge +0x08 -> fenetre 0 champ 1
charge +0x0C -> fenetre 1 champ 2     charge +0x0E -> (fenetre 0 champ 2)
```

Une valeur négative dans la charge signifie **« garder la valeur courante »** — le
gestionnaire relit alors le champ au lieu de l'écrire, ce qui explique les accès en lecture
relevés à `+0x155C0B`. Confiance : **SUPPORTED**.

---

## 3. Le relevé statique, une fois la bonne base connue

Le déblocage se paie ensuite en une seule passe. En cherchant, dans tout le moteur APM3, les
instructions dont le déplacement mémoire tombe dans `[ROB+0x9F4, ROB+0xB73]` — les 32 fenêtres
en ROB-relatif — et en ne gardant que les champs `+0`, `+4`, `+8` (les trois flottants d'une
fenêtre ; les autres restes viennent d'autres structures) :

La première passe rendait **547 accès sur 101 fonctions**. **Ce chiffre était faux**, et il
faut dire pourquoi : le filtre ne retenait que le déplacement mémoire, sans regarder la base
ni le type d'accès. Il ramassait donc des `lea rcx, [rip + 0xb14]`, des `lea r11, [rsp+0xb70]`
— une adresse de constante et un cadre de pile, sans rapport avec le ROB — et surtout tous les
objets qui ont, par hasard, un champ au même déplacement : un `lock xadd dword [rcx+0xa08]`
n'est pas une fenêtre de combat, c'est un compteur de références.

Un champ de fenêtre est un **flottant**. Le relevé n'a donc de sens qu'en exigeant trois
choses : une base qui soit un registre général (ni `rip` ni `rsp`), aucun index, et une
instruction flottante. Après ce resserrage :

**115 accès, 15 fonctions — et les 32 fenêtres restent toutes touchées.**
Relevé complet : `analysis/mothead_fenetres_sites.csv`. Ce qui a sauté : 364 accès non
flottants, 64 accès indexés, 4 accès sur `rip` ou `rsp`.

Quatre fonctions balaient presque toutes les fenêtres — copieurs et réinitialiseurs, sans
valeur d'interprétation : `0x18013329F` et `0x1801345F9` (27 fenêtres chacune),
`0x180251B8E` (19), `0x18024808F` (8). Les onze autres sont **spécifiques**, et c'est là que
se trouve le sens :

```
0x180132600  fenetre 0                     0x18024DC00, 0x18024DD20, 0x18024F380  fenetre 3
0x180133EA0  fenetres 1, 9, 19             0x180247660  fenetres 8 et 9
0x1801394F0  fenetres 7, 14, 25            0x1801150A0, 0x18011BD70  fenetres 20, 23, 25
0x18025F07F  fenetres 11, 14, 17, 19, 22, 25   0x18025E9B0  fenetres 27, 30, 31
```

Confiance : **SUPPORTED**. Ce qui est établi, c'est la **liste des sites** et le fait que
chaque fenêtre a des lecteurs qui lui sont propres. Ce qui ne l'est pas, c'est le **nom** de
chaque fenêtre : il faut lire ces onze fonctions. Le travail est désormais ordinaire — il ne
demande plus ni exécution, ni chance ; il tient en onze fonctions, et non en quatre-vingt-seize.

Un exemple lu jusqu'au bout, `0x18013329F` (site `+0x133522`) : la fonction choisit, **selon
des bits de drapeaux**, la valeur du champ 1 de la fenêtre 8 (`ROB+0xA58`), de la fenêtre 26
(`ROB+0xB30`), de la fenêtre 18 (`ROB+0xAD0`) ou de la fenêtre 0 (`ROB+0x9F8`), la compare à
un instant courant, et range le résultat dans `état+0x074`. Une fenêtre est donc bien **une
borne de trame conditionnelle**, choisie par des drapeaux.

---

## 3 bis. Les deux sélecteurs — ce qu'une fenêtre est vraiment

Des onze fonctions retenues, deux se détachent : **`0x18013329F` et `0x1801345F9` touchent
27 fenêtres chacune**. Ce ne sont pas des copieurs : ce sont des **sélecteurs**, et elles sont
jumelles.

`0x18013329F` est un arbre de tests à deux étages sur les mots de drapeaux du combattant. Un
premier test choisit un **groupe**, un second un **modificateur** dans le groupe, et la
fonction lit le **champ +4** de la fenêtre ainsi désignée, le compare à un instant, et range
le résultat dans `état+0x074`.

| test de groupe | sans modificateur | `dl & 0x40` | `al & 0x10` | `dl & 2` |
|---|---:|---:|---:|---:|
| `bl&1` ou `r8b&0x20` | **0** | 8 | 26 | 18 |
| `bpl & 4` | **1** | 9 (`sil&0x40`) | — | 19 |
| `bl & 0x10` | **3** | 11 | 28 | 21 |
| `bl & 8` | **4** | 12 | 29 | 22 |
| `cl&1` et `bl&1` | **5** | — | 30 | 23 |
| `al & 4` | **6** | 13 | 31 | 24 |
| `r8b & 8` | **7** | 14 (`dl&0x40`) | — | 25 |
| `al & 0x40` | **17** | | | |
| `al` bit 7 | **16** | | | |

`0x1801345F9` parcourt **exactement le même arbre, dans le même ordre** — 9, 19, 1, 14, 25, 7,
30, 23, 5, 17, 16, 12, 29, 22, 4, 11, 28, 21, 3, 13, 31, 24, 6, 8, 26, 18, 0 — mais lit le
**champ +8**. Les deux fonctions rendent donc deux champs de la *même* fenêtre.

**Une fenêtre n'est donc pas nommée par son indice : elle est choisie.** Le combattant est
dans un état ; cet état désigne un groupe ; trois bits de modificateur désignent la variante ;
et la fenêtre qui en résulte fournit ses bornes. C'est pourquoi vouloir « nommer la fenêtre 12 »
n'avait pas de sens en soi : la bonne question est *quel état du combattant mène à la
fenêtre 12*, et la réponse est ici — `bl & 8` avec `dl & 0x40`.

**Cinq fenêtres — 2, 10, 15, 20 et 27 — ne sont sélectionnées nulle part** et n'ont aucun
lecteur scalaire : seuls les copieurs les touchent. Elles occupent exactement les cases que
l'arbre ci-dessus laisse vides. Confiance : **SUPPORTED**.

### Les trois champs, et qui lit lequel

Les cinq fonctions qui lisent le **champ +0** ne sont pas quelconques : deux d'entre elles
reprennent **exactement un groupe de l'arbre ci-dessus**, avec les mêmes bits de modificateur.

| fonction | fenêtres | modificateurs employés |
|---|---|---|
| `0x180133EA0` | 9, 19, **1** | `r8b & 0x40` → 9, `cl` → 19, sinon 1 |
| `0x1801394F0` | 14, 25, **7** | `dil & 0x40` → 14, `dil & 2` → 25, sinon 7 |

Ce sont les groupes de base **1** et **7**. Chacune lit le champ +0 de la fenêtre qu'elle a
choisie et le **compare à un instant** (`vcomiss`). `0x1801394F0` enchaîne d'ailleurs sur
`0x18016A1C0`, la même fonction que les codes 20 à 24 de la liste 2 appellent après leur garde
d'entrée.

Le modèle se referme donc :

| champ | qui le lit | ce qu'il est |
|---|---|---|
| **+0** | les consommateurs de groupe, comparé à la trame courante | **le début de la fenêtre** |
| **+4** | `MothPickWindowHigh` (`0x18013329F`) ; borné à `état+0x004 − 1.0f` par le poseur | **la borne haute**, jamais au-delà de la durée de l'animation |
| **+8** | `MothPickWindowThird` (`0x1801345F9`), même arbre, même ordre | **une troisième borne** |

### Et ce que l'arbre teste : le masque de commande

Les deux sélecteurs ne sont pas des fonctions autonomes : `0x18013329F` et `0x1801345F9` sont
des **fragments**. Les vraies entrées sont `0x180133280` et `0x1801345E0`, toutes deux
`f(rcx = ROB)`, et toutes deux commencent par la même ligne :

```
mov ebx, dword ptr [rcx + 0x518]     ; le mot de requete
test ebx, ebx
je  (sortir)                          ; requete vide -> rien a selectionner
```

L'arbre ne teste donc pas des drapeaux épars mais **les octets d'un seul mot**, `ROB+0x518` :
`bpl = ebx >> 8`, `sil = ebx >> 24`, et `bl` est son octet bas.

Or `ROB+0x518` **reçoit la même valeur que `ROB+0x508`**. Les fonctions qui les écrivent le
font toujours par paire, à la même instruction près :

```
0x1801386B0   mov dword ptr [rsi + 0x508], eax
0x1801386B6   mov dword ptr [rsi + 0x518], eax
```

et `0x1801382AB`, qui fait cela trois fois, appelle dans la foulée les deux sélecteurs
(`0x180133280`, `0x1801345E0`), `MothGetRecord`, `0x18016A1C0` et le consommateur du groupe 7.

Et `ROB+0x508`, on l'a **mesuré** : c'est le **masque d'entrée du combattant**, celui qui
prend `0`, `1`, `0x15`, `0x40001`, `0x2080003` selon ce que le stub tient enfoncé.

**Une fenêtre temporelle est donc un créneau d'entrée.** Le combattant a une commande en cours
(un bouton, une direction, une combinaison) ; cette commande désigne un groupe ; trois bits de
modificateur désignent la variante ; et la fenêtre qui en résulte dit **entre quelles trames
cette commande est recevable** dans l'animation en cours. C'est exactement ce qu'un jeu de
combat appelle une fenêtre de *cancel*, d'enchaînement ou de *sabaki*.

Confiance : **SUPPORTED**. La chaîne est complète — le sélecteur lit `ROB+0x518` (lu dans le
code), `ROB+0x518` reçoit la valeur de `ROB+0x508` (lu dans le code, trois sites), et
`ROB+0x508` suit nos appuis (mesuré à l'exécution) — mais l'attribution nominale de chaque bit
du masque du combattant reste ouverte : la mesure code par code n'a pas convergé tant qu'un
adversaire actif partage la scène.

---

## 3 ter. Quel code pose quelle fenêtre — la table complète

En appliquant aux **84 gestionnaires de la liste 1** le même filtre strict (accès flottant
scalaire, base non indexée, registre issu de `ctx[2]`), la correspondance sort entière et sans
reste :

| code | fen. | code | fen. | code | fen. | code | fen. |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 6 | 0 | 17 | 10 | 28 | 19 | 37 | 27 |
| 7 | 1 | 18 | 11 | 29 | 20 | 38 | 28 |
| 8 | 2 | 19 | 12 | 30 | 21 | 39 | 29 |
| 9 | 3 | 21 | 13 | 31 | 22 | 41 | 30 |
| 10 | 4 | 22 | 14 | 33 | 23 | 42 | 31 |
| 12 | 5 | 23 | 15 | 34 | 24 | | |
| 13 | 6 | 24 | 16 | 35 | 25 | | |
| 14 | 7 | 25 | 17 | 36 | 26 | | |
| 15 | 8 | 27 | 18 | | | | |
| 16 | 9 | | | | | | |

**Trente-deux codes, trente-deux fenêtres, un pour un.** Et les six codes que cette liste
saute — 5, 11, 20, 26, 32 et 40 — sont exactement ceux qui en écrivent **plusieurs d'un
coup** :

| code | fenêtres écrites |
|---:|---|
| 5 | 0, 1, 2, 6 |
| 11 | 2, 3, 4 |
| 20 | 10, 11, 12 |
| 26 | 15, 16, 17 |
| 32 | 20, 21, 22 |
| 40 | 27, 28, 29 |

Les codes concernés vont de **5 à 42** sans trou, ce qui recoupe exactement la plage que
`docs/formats/mothead.md` annonçait, et **les 32 fenêtres sont couvertes**. Confiance :
**CONFIRMED** — la table est mécanique, et le premier essai, mené sans filtre sur le type
d'accès, avait produit quatre lignes fausses (codes 1, 3, 51, 57) qui ont disparu dès qu'on a
exigé un accès flottant : un `test byte [état+0x280], 8` n'est pas la lecture d'une fenêtre.

À quoi cela sert : pour modifier une fenêtre dans les données, on sait maintenant **quel code
de liste 1 écrire**, et la liste 2 offre les mêmes pour les neuf premières fenêtres, à une
trame donnée (§ correspondance liste 2 → liste 1).

---

## 4. Ce que cela change pour la suite

- Le second verrou — **les 37 codes de liste 2 que le DLL ne cherche jamais** — a été repris
  dans la foulée. **L'idée du ROB-relatif n'y était pour rien** : le balayage des accès à
  `ROB+0xD40` ne rend que deux instructions, aucune pertinente. Ce qui a marché est de la même
  famille sans être la même chose — une **base voisine et non une base décalée** : le parcours
  lit un curseur rangé à côté du pointeur cherché. Récit dans
  `analysis/liste2_repartiteur.md`. La leçon commune aux deux verrous est ailleurs : une
  énumération exhaustive ne vaut que ce que vaut la prémisse qui la borne.
- `tools/pister_etat.py --offsets <trois offsets>` permet d'interroger n'importe quelle
  fenêtre à l'exécution, en une passe de deux minutes et demie.
- L'outillage est en place : entrées scriptées, points d'arrêt logiciels et matériels,
  captures d'écran datées.
