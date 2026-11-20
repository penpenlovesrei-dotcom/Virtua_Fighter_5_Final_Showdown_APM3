# Le mode Quest : comment il se JOUE

Lu dans le jeu de 2007, pas raconté. Deux sources, et elles se recoupent :
le code décompilé (`analysis/quest/*.c`) et **les 492 libellés du mode**, qui
sont la conception écrite en toutes lettres (`analysis/quest/textes.md`).

La notice est dans le jeu, libellé **523** :

> *Starting Quest Mode. On the Map Screen, select an Arcade Icon to display
> the Arcade Menu. You can choose any arcade, and fight against rivals to
> become the top player.*

Et le résumé du menu principal, libellé **86** : *« Fight rivals as you work
your way through different arcades. »*

## La boucle

1. **La carte.** Neuf repères. Libellé 127 : *« Choose your destination. You
   can adjust various settings at Home. »*
2. **Une salle.** On y voit **trois bornes**, chacune occupée par un rival.
3. **On s'assoit à une borne** et on se bat. Libellés 146, 147, 148 :
   *« Play against the opponent on Unit 1 / 2 / 3. »*
4. On gagne de l'**argent** (« Fight money », 997, compté en **G**, 999
   `%dG`), des **objets** et des **emblèmes**.
5. On dépense chez le marchand (**937** « Item shop »), on se **personnalise**,
   et on recommence ailleurs.
6. Par-dessus : les **tournois officiels**, au dôme.

Le but est la **note d'ensemble** (548 « Overall completion rating ») : battre
les mille rivaux, collecter les objets et les emblèmes.

## Les neuf lieux, et ce qu'ils valent

Chaque salle a son niveau de jeu — le texte le dit, et c'est la progression du
mode :

| id | lieu | ce que le jeu en dit (129-136) |
|---:|---|---|
| 528 | SEGA WORLD NORTH | *a well-known arcade where many **advanced** players gather* |
| 529 | SEGA WORLD SOUTH | *an **elite** arcade frequented by many **high-ranked** players* |
| 530 | SEGA WORLD ROUTE 101 | *a popular arcade, from **novices to advanced*** |
| 531 | CLUB SEGA DOWNTOWN | *crowded, many **beginning and intermediate*** |
| 532 | CLUB SEGA BAY AREA | *a wide range, especially **intermediate*** |
| 533 | SEGA ARENA COAST | *lively, welcoming, many **beginning** players* |
| 534 | SEGA ARENA EAST | *attracts **all skill levels** for friendly competition* |
| 535 | EVENT SQUARE | *the arena where **official tournaments** are held* |
| — | la maison | 128 : *Home: adjust various settings (**START** l'ouvre aussi)* |

Et `npc_tbl` porte le lieu de chacun des mille rivaux en `+0x88` : 130 à 138
par salle, **59** pour le huitième groupe.

## Les trois menus, et ils sont DIFFÉRENTS

C'est la correction que cette lecture a apportée : je dessinais le même menu
partout.

### Une salle d'arcade — `store_menu_win`

`FUN_82313EA8`. Deux colonnes. Le titre est le nom de la salle
(`p_store_menu_win_01_ct`, 640 × 100), pris dans un tableau de huit entiers
que Ghidra montre en **flottants dénormaux** — `7.39886e-43` vaut **528**
(voir `reference_entiers_en_flottants_denormaux`).

| ancre | x, y | contenu |
|---|---|---|
| `c_button_csr_a_01_lt` | 257, 136 | **« 1 »** (589) et le nom de l'occupant |
| `c_button_csr_a_02_lt` | 257, 224 | **« 2 »** (590) et son occupant |
| `c_button_csr_a_03_lt` | 257, 312 | **« 3 »** (591) et son occupant |
| `c_button_csr_b_01_lt` | 644, 136 | **« Tournament »** (592) et son état (593) |
| `c_button_csr_a_04_lt` | 644, 312 | **« Customize »** (594) |

Le nom de l'occupant se pose à **+122 en x, +12 en y** de l'ancre
(`DAT_8208E6F8`, `DAT_82000F0C`), et il vient de `FUN_8230DDF0(npc, tampon)` —
la table des rivaux. Les trois occupants sont trois numéros de rival rangés
dans la tâche en `+0x64`, `+0x68`, `+0x6C`.

Un occupant déjà battu porte l'**étoile** (`0x820117C8`), et celui qui
enchaîne les victoires porte sa bannière : **149** `%s is on a %d-win
streak!`

### Le dôme — `hall_menu_win`

`FUN_82311Cxx`. Trois entrées, une colonne (ancres `c_button_csr_c_01_lt`,
`d_01_lt`, `d_02_lt`, à 252 × 133 / 271 / 335) :

* **599** *Official Tournaments*, avec **600** *Currently not in progress.* en
  légende grise quand il n'y en a pas ;
* **601** *List of official tournaments* — 152 : *« View official tournaments
  you have cleared. »* ;
* **602** *Customize*.

### La maison — `home_menu_win`

Six lignes, ancres `p_home_menu_win_30_02_ct` (640 × 166) puis `_30_03_ct`
(640 × 330), pas de 30 :

| id | entrée | ce qu'elle fait (139-145) |
|---:|---|---|
| 537 | Customize | *purchase items or adjust settings* (153) |
| 538 | Status | *view various records* (138) |
| 540 | Quest settings | *adjust the difficulty level* (139) |
| 541 | Save | *save current settings* (141) |
| 542 | Return to Character Select | (142) |
| 543 | End Quest Mode | *and return to the Main Menu* (143) |

## L'économie

* **Fight money** (997), en **G** (999 `%dG`). On la gagne aux combats et aux
  tournois.
* **Item points** (996) — une seconde monnaie, pour les objets.
* La **boutique** (937 *Item shop*, 291 *Select an item to buy*, 998 *Already
  purchased*) vend des pièces de costume, rangées par **emplacement du
  corps** — trente catégories, 952 à 981 : *Head, Above head, Hair/Hat,
  Forehead, Face, Eyes, Glasses, Ears, Nose/Mouth, Neck, Inner wear, Outer
  wear, Chest, Back, Skin, Shoulders, Upper arms, Wrists, Hands, Belt, Hips,
  Pants, Shins, Toes…* et l'**Orb disc** (981), dont on ne peut posséder
  qu'un (1000, 1001).
* Les **emblèmes** : treize familles (571-584) — *Alphabet, Japanese, Animals,
  Food, Crests, Jobs, Characters, Space, Logos, Hobbies, Plants, Colors,
  Other, Bonus*. 588 : *« The following emblem(s) can now be used »*.
* Un secret, libellé **557** : *« When starting Quest Mode with a new
  character, hold LB while pressing OK on the introductory message to start
  with maximum money. »*

## Les tournois

Au dôme. Le sous-état **0x55** de 2007 (`QUEST_TOURNAMENT`).

* 629 *Do you want to enter this tournament?* ; 620 `Participants: %d`,
  621 `Rounds: %d`, 622 `Time: %d` ;
* les **lots** : 624 `1st place: %dG  2nd: %dG  3rd: %dG`, ou 625 un **objet**
  en premier prix, ou 626 un **emblème** ;
* le déroulé : *Round 1/2/3* (667-669), *Semifinals*, *Final*, *3rd Place
  Match* (678-680), puis *Match 1..12* ;
* le résultat : 702-704 *Lost in Round n*, 708 *Best 4*, 710 *3rd Place*,
  711 *2nd Place*, **712 *Champion*** ;
* 619 : quitter la salle **remet la série de victoires à zéro**.

## Le statut

Sept lignes (§9.20 de `mode_quest.md`), toutes issues du profil :

*Rivals defeated, Items collected, Emblems collected, Overall completion
rating* — quatre pourcentages — puis *Longest streak*, *Total number of
matches* / *Number of matches*, *Total playing time* / *Completion time*, ces
deux dernières paires basculant toutes les 180 images.

Depuis le statut : 554 *View rival list*, 555 *View emblem list*.

## Les neuf sous-états, et où nous en sommes

| sous-état | rôle | chez nous |
|---|---|---|
| 0x51 | accueil du mode | fait |
| 0x52-0x54 | transitions carte / salle | fait |
| 0x55 | tournoi | à faire |
| 0x56 | préparation du combat | à faire |
| 0x57 | combat (`QUEST_VS`) | le départ et le retour sont écrits |
| 0x58 | après le combat | à faire |
| 0x59 | sortie vers le menu | fait |

## Ce que cette lecture change tout de suite

1. **Le menu d'une salle est `store_menu_win`, pas `hall_menu_win`** — trois
   bornes et leurs occupants, plus Tournament et Customize. C'est LÀ qu'on se
   bat, et c'est ce qui manquait pour que le mode ait un sens.
2. Le dôme garde `hall_menu_win` et ses trois entrées de tournoi.
3. Le combat ne se choisit pas dans la liste des rivaux — **la liste est un
   registre** (554 *View rival list*, ouverte depuis le statut), pas un
   sélecteur. On se bat contre **l'occupant d'une borne**.
