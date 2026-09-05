# Atteindre les etats console : ce que les essais ont donne

Chantier n° 2 du programme du 2026-09-03. Trois essais, deux resultats nets et
une conclusion que j'avais d'abord tiree trop vite.

L'outil : `tools/tracer_etats.py`, auquel on a ajoute `--tete N` (certains
sous-etats n'appartiennent pas a l'etat de tete courant : les `DATA_TEST_*` sont
sous la tete 3 `DATA_TEST`, pas sous `APM3`, et il faut donc devier `ecx` en meme
temps que `edx`) et `--captures`.

---

## 1. `DATA_TEST` : la machine accepte, le code est vide

### La deviation passe

```
py -3 tools/tracer_etats.py --devier 49 21 --tete 3
```

```
5  etat [APM3] -> [MAX]  sous-etat [APM3_ENTRY] -> [APM3_SELECTOR]
                                  <<< DEVIE vers DATA_TEST_MAIN sous la tete DATA_TEST
6  etat [DATA_TEST] -> [ADVERTISE]  sous-etat [DATA_TEST_MAIN] -> [DATA_TEST_MISC]
```

Le jeu **entre** dans `DATA_TEST_MAIN` et enchaine **tout seul** vers
`DATA_TEST_MISC`. La machine a etats est donc bien cablee : ce n'est pas un
etat mort du point de vue de l'enumeration.

### Mais rien ne repond, et c'est mesure

`tools/scenarios/data_test.txt` martele les **treize codes d'entree** l'un apres
l'autre pendant une minute a l'interieur de l'etat, clavier et manette coupes
pour qu'aucune saisie parasite ne brouille la mesure. Quatre captures a 40, 60,
80 et 95 secondes :

```
8f4012d968567353d8cc
8f4012d968567353d8cc
8f4012d968567353d8cc
8f4012d968567353d8cc
```

**La meme empreinte SHA-256 pour les quatre.** Pas un pixel ne bouge en
cinquante-cinq secondes, sous n'importe quelle entree. L'ecran reste fige sur le
contenu precedent : l'etat ne dessine rien et ne reagit a rien.

### La cause, statique et sans appel

Chacun des quinze noms `DATA_TEST_*` apparait **exactement une fois** dans le
binaire -- dans la table de noms -- et il n'existe **aucune** chaine de menu de
debogage (`DATA TEST`, `OBJ TEST`, `MOT TEST`, `CHR TEST`...). Un visualiseur de
donnees affiche forcement des libelles ; il n'y en a pas un seul.

**Les quinze ecrans sont compiles hors de ce build Retail. Seule l'enumeration
survit.**

Confiance : **CONFIRMED**.

### Une piste ecartee, pour la deuxieme fois

J'ai cherche le repartiteur des sous-etats, qui aurait montre a quoi pointent
les entrees 21 a 35. Deux candidats, deux rejets :

- une table de 56 pointeurs a `0x1803465C8` : ses quatre premieres entrees ne
  sont meme pas des adresses valides ;
- une zone riche en pointeurs vers `0x180660B18` : la suite n'est **pas
  contigue**, donc ce n'est pas une table.

Une zone reguliere n'est pas une table identifiee. Le repartiteur reste
introuvable -- et il n'est plus necessaire : la mesure d'execution a tranche.

### Ce que cela ferme

La voie courte vers Dural passait par `DATA_TEST_CHR` (30) et `DATA_TEST_MOT`
(25), qui l'auraient montre sans passer par la grille de selection. **Cette voie
n'existe pas.** Il faudra revenir a la selection elle-meme.

---

## 2. `MENU_MAIN` : il S'AFFICHE, et il est VIDE

```
py -3 tools/tracer_etats.py --devier 49 36 --tete 4
```

**Frederic a conduit lui-meme**, et le verdict est le sien : « meme
comportement : ecran titre / ecran noir / **menu PS3 mais vide** ».

Le fond gris anime au logo *Final Showdown*, avec son cadre en bas, **est** le
chrome du menu console. Il se dessine. Il n'a simplement aucune entree.

### Mon erreur, et sa correction

Le matin meme, sur exactement la meme image, j'avais ecrit « le chrome du menu
s'affiche » -- Frederic avait corrige : « c'est un ecran de loading ». J'avais
donc note l'inverse. **C'etait bien le menu.** Les deux fois j'ai parle d'une
image au lieu de la faire regarder ; la seule chose qui a tranche, c'est qu'il y
navigue lui-meme, en voyant la sequence complete titre -> noir -> menu.

### Pourquoi il est vide, et c'est mesure

Les ressources d'entrees du menu **n'existent pas** dans les donnees APM3 : ni
`p_menutxt_PS3_lt`, ni `menutxt`, ni la moindre planche `aet_*_menu*` ou
`spr_*_menu*` -- ni dans l'inventaire, ni dans l'index du `.par`.

Et elles ne sont **pas non plus dans le paquet Xbox 360** : sur ses 231 planches
2D nommees, aucune ne porte `menu`. Le texte du menu ne vient donc pas d'une
planche : il est ailleurs -- dans l'executable, ou dans une table.

**Le candidat** : `rom/sp_title_tbl.bin`, 853 474 octets, present dans APM3 et
jamais examine. C'est le prochain endroit ou chercher.

Confiance : **le menu s'affiche, CONFIRMED** (vu par Frederic). **Ses entrees
sont absentes des planches, CONFIRMED.** Leur emplacement reel, **UNKNOWN**.

---

## 3. La lecon de methode, pour la troisieme fois

Trois erreurs de suite, toutes de la meme famille :

1. le decor « importe » juge sur une capture, alors que le selecteur etait sur
   **Random** et qu'on ne savait meme pas quel decor s'etait charge ;
2. le 720p declare bon parce que **l'ATS** etait bien mis en page, alors que la
   vue 3D restait cadree pour 1920 ;
3. le menu console declare affiche alors que c'etait **l'ecran de chargement**.

A chaque fois : une image regardee, une conclusion tiree. La mesure qui aurait
tranche existait dans les trois cas -- forcer le decor, comparer le champ de
vision, chercher les ressources du menu. **Ne pas conclure d'une capture ce
qu'une mesure peut dire.**

---

## 4. `APM3_ENTRY` : le traverser, jamais le sauter

L'ecran noir entre le titre et la selection est `APM3_ENTRY` (sous-etat 48).
Trace relevee pendant que Frederic y etait :

```
1  [t= 12,4 s]  STARTUP -> APM3     CS_TITLE   -> MAX
2  [t= 72,5 s]  APM3 -> STARTUP     APM3_ENTRY -> CS_TITLE   <- repart seul apres ~60 s
4  [t=113,5 s]  APM3 -> MAX         APM3_ENTRY -> APM3_SELECTOR
```

**Le sauter est impossible.** Forcer le sous-etat a `APM3_SELECTOR` en entrant
dans `APM3` donne, en moins d'une seconde :

```
EXCEPTION ACCESS_VIOLATION (1re chance)  a moteur+0xB1D33
EXCEPTION ACCESS_VIOLATION (2e chance)   a moteur+0xB1D33
```

`APM3_ENTRY` n'est donc pas un ecran d'attente inutile : il **prepare** ce que la
selection va lire. `moteur+0xB1D33` nomme l'endroit exact ou ca manque -- et
c'est peut-etre la meme structure que celle de `[rbx-0x10C]`, ou l'on ecrit
l'indice de Dural. A verifier : cela relierait deux chantiers.

**Le traverser marche.** `tools/tracer_etats.py --passer-entry` ecrit une
directive d'impulsion des que le jeu entre dans `APM3`, et le stub appuie sur
START. Un seul appui humain, plus d'ecran noir, plus de retour au titre.
Verifie a l'ecran : « c'est parfait ».

Cela a demande une nouveaute dans le stub, l'**impulsion a usage unique** --
`impulsion = start` / `duree = 150` -- declenchee par la **date du fichier** et
non par une heure absolue. C'etait la piece manquante : les pas d'un scenario
sont dates depuis le premier sondage d'entree, instant qu'un outil exterieur ne
connait pas.

Disponible dans le lanceur du Bureau, choix 1.
