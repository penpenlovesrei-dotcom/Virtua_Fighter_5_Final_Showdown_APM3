# Les boutons gérés par la version APM3 — joueur 1 et joueur 2

Relevé le 2026-10-11 sur le build en place. Sources : la disposition compilée
dans `tools/gen_apm_stub.py` (`disposition()`), le fichier vivant
`runtime/media/vf5fs/apm_entrees.txt`, et la chaîne mesurée par
`tools/entrees.py` sur ce binaire.

**Rien dans le fichier vivant ne surcharge la disposition** : il ne porte que
`nom start = 7`, `front`, `clavier = 1`, `manette = 1`, `manette_joueur = 2`.

---

## 1. Les trois étages

Une touche ne parle pas directement au jeu. Elle traverse trois étages, et
c'est pourquoi « le bouton ne fait rien » peut vouloir dire trois choses
différentes :

    touche / bouton  ->  CODE APM (0 à 31)  ->  bit du masque arcade  ->  code logique
         (le stub)          Input_isOn            0x180243ED0            ce que le jeu lit

Le journal (`journal_fichier = 1`) les sépare :

    PAD    0x1000  A              la manette a changé
    MASQUE 0x000200  codes 9      ce que le stub en a tiré
    LU     Input_isOn(9) = OUI    ce que le moteur a demandé

---

## 2. Le partage des codes

Le stub a **32 créneaux**. Ils sont répartis ainsi, et ce partage est ce qui
explique le comportement de la manette dans les menus :

| créneau | à qui |
|---|---|
| 0 – 14 | **joueur 1** |
| 15 | la sortie de mode — hors boucle par joueur |
| 16 – 17 | les deux caméras de l'écran TERMINAL — hors boucle |
| 18 – 30 | **joueur 2** (les codes 2 à 14 décalés de 16) |
| 31 | libre |

`manette_joueur` décide où tombe la manette. **Il vaut 2** : le clavier tient
le joueur 1, la manette le joueur 2.

---

## 3. Le tableau, joueur 1

| code | rôle | clavier | manette si `manette_joueur = 1` |
|---|---|---|---|
| 0 | TEST (menu opérateur) | **F1** | — *(mode arcade : Affichage)* |
| 1 | SERVICE | **F2** | — *(mode arcade : XBOX)* |
| 2 | HAUT | **↑** | croix haut |
| 3 | BAS | **↓** | croix bas |
| 4 | GAUCHE | **←** | croix gauche |
| 5 | DROITE | **→** | croix droite |
| 6 | pièce | **Espace** | **Affichage** (⧉) |
| 7 | VALIDER / START | **Entrée**, et **X** | **Menu** (≡), et **A** |
| 8 | ANNULER | **W** | **B** |
| 9 | **P** — poing | **X** *(porte aussi le code 7)* | **A** *(idem)* |
| 10 | **K** — pied | **C** | **B** |
| 11 | valider (3ᵉ forme) | — | — |
| 12 | valider (4ᵉ forme) | — | — |
| 13 | **G** — garde | **V** | **X** |
| 14 | 4ᵉ bouton, « NO USE » | **Q** | **Y** |
| 15 | quitter le mode courant | **Échap** | **Affichage** (⧉) — *seulement si `manette_joueur = 1`* |
| 16 | recentrer la caméra (TERMINAL) | **B** | — |
| 17 | changer de vue (TERMINAL) | **N** | — |

## 4. Le tableau, joueur 2

La manette y est **aujourd'hui**, puisque `manette_joueur = 2`.

| code | = code J1 | rôle | manette |
|---|---|---|---|
| 18 | 2 | HAUT | croix haut / stick |
| 19 | 3 | BAS | croix bas / stick |
| 20 | 4 | GAUCHE | croix gauche / stick |
| 21 | 5 | DROITE | croix droite / stick |
| 22 | 6 | pièce | **Affichage** (⧉) |
| 23 | 7 | VALIDER / START | **Menu** (≡), et **A** |
| 24 | 8 | ANNULER | **B** |
| 25 | 9 | **P** — poing | **A** |
| 26 | 10 | **K** — pied | **B** |
| 27 | 11 | valider | — |
| 28 | 12 | valider | — |
| 29 | 13 | **G** — garde | **X** |
| 30 | 14 | **4ᵉ bouton** | **Y** |

> **CORRECTION du 2026-10-11** : une première version de ce tableau décalait
> ces codes de deux (elle donnait 18 et 19 pour inutilisés et faisait partir
> les directions à 20). C'est faux. `--joueur2` réserve 18 à 30, soit les
> **treize** codes 2 à 14 décalés de seize : `18 = 2`, donc HAUT. Le journal
> de Frédéric le disait déjà — `MASQUE 0x00800000 codes 23` sur START, et
> `d + 7 = 23`.

**ET UNE EXCEPTION, VOULUE** : la manette reçoit **en plus** les codes **7 et
8 du joueur 1**. Sans cela elle ne pourrait rien valider, car les menus ne
lisent que le joueur 1 (`0x1801A2BC0` valider, `0x1801A2B90` annuler). Les
**directions**, elles, ne sont pas doublées : les codes 2 à 5 font marcher le
combattant, et la manette déplacerait les deux personnages à la fois.

**Depuis le 2026-10-11, `A` ne participe plus à cette exception** (demande de
Frédéric) : le code 7 du joueur 1 n'est porté que par **Menu ≡**, et le code 8
par **B**. `A` garde ses deux codes à lui, **25** (le poing) et **23**
(valider côté joueur 2). Dans les menus, c'est donc le seul bouton Menu qui
valide.

---

## 5. Ce que le jeu fait vraiment de ces codes

Mesuré par `tools/entrees.py` sur ce binaire :

| code apm | bit du masque arcade | code logique | rôle réel |
|---|---|---|---|
| 7 | 0 | 7 | VALIDER |
| 8 | 1 | 8 | VALIDER (annuler) |
| 12 | 2 | 7 | VALIDER |
| 11 | 3 | 9 | VALIDER |
| 13 | 4 | 103 | **COMBAT — G** (garde) |
| 14 | 5 | 101 | **COMBAT — 4ᵉ bouton** |
| 9 | 6 | 100 | **COMBAT — P** |
| 10 | 7 | 102 | **COMBAT — K** |

**Il n'y a que quatre boutons d'action, et le jeu n'en emploie que trois** :
son écran `OPTIONS > Controls` affiche P, K, G — et « NO USE » sur le
quatrième.

**LB, RB, LT, RT ne sont branchés à rien**, et ce n'est pas un choix : le
masque arcade ne porte que douze bits, et ses bits 8, 10 et 11 ne sont
produits par aucun code d'entrée. L'écran Controls le dit lui-même, toutes ses
lignes de gâchette sont « NO USE ».

---

## 6. Deux points à vérifier avec toi

**(a) Ta remarque sur la touche Menu.** D'après la table, `Menu (≡)` est bien
`XINPUT_GAMEPAD_START` (0x0010) → code 7 = VALIDER, et `Affichage (⧉)` est
`XINPUT_GAMEPAD_BACK` (0x0020) → code 6 = **pièce** et code 15 = **quitter le
mode**. Or sur une borne, **c'est la pièce qui fait entrer le joueur 2**. Si
tu as vu le joueur 2 arriver en pressant Affichage, c'est cohérent : ce n'est
pas que Menu soit mal branché, c'est qu'Affichage met un crédit. À confirmer
bouton par bouton.

**(b) Un vrai défaut, mesuré.** Le stub définit `XI_LT = 0x0040` et
`XI_RT = 0x0080` en les fabriquant depuis les gâchettes analogiques
(`if (e.gl > 60) b |= XI_LT`). Mais dans XInput, **0x0040 et 0x0080 sont les
clics de stick** (LEFT_THUMB / RIGHT_THUMB). Un clic de stick est donc lu
comme une gâchette. Sans conséquence aujourd'hui — rien n'est branché sur LT
ni RT — mais à corriger avant de s'en servir.

---

## 7. Pour la revue touche par touche

Tout se règle **à chaud**, dans `runtime/media/vf5fs/apm_entrees.txt` (relu
toutes les 250 ms, sans relancer le jeu) :

    touche  <code> = <nom>      la touche du clavier
    touche2 <code> = <nom>      une seconde touche pour le même code
    bouton  <code> = <nom>      le bouton de manette
    bouton2 <code> = <nom>      un second bouton, combiné par OU

Noms de manette acceptés : `a b x y lb rb lt rt start back select menu
affichage view guide xbox haut bas gauche droite`.

**`X` et `A` portent DEUX codes.** `X` au clavier vaut **P** (code 9) et
**valider** (code 7) ; `A` à la manette fait de même. C'est sans danger, et
c'est mesuré : les codes 7, 8, 11 et 12 ne sortent qu'en codes logiques de
**validation** — aucun n'est un bouton de combat. En plein combat, le code 7
n'est donc lu par personne.

**Un masque à plusieurs boutons est un ACCORD, pas une alternative** :
`(état & masque) == masque`. Pour qu'un code réponde à l'un **ou** l'autre
bouton, il faut `bouton` et `bouton2`.
