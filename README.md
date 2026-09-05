# Virtua Fighter 5 Final Showdown — build arcade APM3

Rétro-ingénierie du portage arcade de *Virtua Fighter 5 Final Showdown* tournant
sur carte **SEGA ALLS / APM3**, et remise en service de ce que ce build avait
perdu par rapport à la version console.

Ce dépôt ne contient **que du travail original** : des documents d'analyse et
des outils. Aucune donnée de jeu, aucun binaire, aucun extrait d'archive.

---

## Ce qui a été fait

### Dural, jouable

Dural était présente dans les données mais inatteignable dans la grille de
sélection : sa case était **désactivée, pas absente**. Trois substitutions
d'appel et quatre bornes portées de 18 à 20 la rendent jouable, sans rien
ajouter au jeu. Détail : [`analysis/dural.md`](analysis/dural.md).

### Le menu console, remis en marche

Le build arcade conserve tout le mode console — les dix modes, les 55
sous-états, l'arbitre de fin de combat — mais **neuf maillons** avaient été
retirés ou bouchonnés. Le parcours complet a été rétabli :

| entrée | état |
|---|---|
| SINGLE PLAYER | quatre modes (Arcade, Score Attack, License Challenge, Special Sparring) |
| OFFLINE VERSUS | combat à deux, deux périphériques indépendants |
| DOJO | entraînement, plus une quatrième ligne « How to Play » |
| TERMINAL | écran de personnalisation, avec son décor d'origine |
| OPTIONS | quatre lignes, toutes atteignables |
| EXIT GAME | dixième ligne du menu, ferme le jeu |

Détail : [`analysis/menu_console.md`](analysis/menu_console.md) et
[`analysis/machine_console.md`](analysis/machine_console.md).

### Le désassemblage

Environ **10 %** des 8 541 fonctions du moteur ont été touchées, concentrées
sur un axe : machine à états, menu console et ses pages, sélecteur de
personnages, écran de personnalisation, entrées, gestionnaire de décor, écran
de chargement. Le compte et sa méthode sont dans
[`analysis/couverture_console.md`](analysis/couverture_console.md).

---

## Les documents

| document | sujet |
|---|---|
| [`machine_console.md`](analysis/machine_console.md) | les deux tables de pilotage : dix modes, 55 sous-états |
| [`menu_console.md`](analysis/menu_console.md) | le menu console, entrée par entrée, et les neuf maillons |
| [`dural.md`](analysis/dural.md) | la grille de sélection et le déblocage de Dural |
| [`mode_selector.md`](analysis/mode_selector.md) | le sous-état `MODE_SELECTOR`, et le chaînage des modes |
| [`vs_gameover.md`](analysis/vs_gameover.md) | `VS`, `GAMEOVER`, et l'arbitre de fin de combat |
| [`carte_options.md`](analysis/carte_options.md) | l'écran d'options, ses pages et son curseur |
| [`carte_customize.md`](analysis/carte_customize.md) | l'écran de personnalisation |
| [`couverture_console.md`](analysis/couverture_console.md) | ce qui est lu, et ce qui ne l'est pas |
| [`INSTRUMENTATION.md`](analysis/INSTRUMENTATION.md) | le débogueur et les sondes |
| [`MANIFEST.md`](analysis/MANIFEST.md) | les empreintes des fichiers étudiés |

---

## Les outils

Tous en Python 3, sans dépendance hors `capstone` et `pefile`.

| outil | rôle |
|---|---|
| `patch_moteur.py` | le patcheur unique — chaque correctif est une option, et repart toujours du binaire d'origine |
| `plage.py` | désassemble une **plage** d'adresses, sans s'arrêter au premier `ret` |
| `carte_zone.py` | cartographie une zone entière : appelants, appelés, chaînes, bouchons |
| `libelles.py` | résout un identifiant de texte depuis la table de chaînes |
| `renommer_libelle.py` | réécrit un libellé sur place dans l'archive |
| `sllz.py` | lecteur d'index PARC et décompresseur SLLZ |
| `instrument.py` | le débogueur : points d'arrêt, lecture de contexte, journal |
| `pister_*.py` | les sondes de mesure, une par question posée |
| `gen_apm_stub.py` | génère la bibliothèque de substitution qui remplace celle de la carte arcade |

Les lanceurs `.cmd` appliquent un jeu de correctifs et démarrent le jeu ; ils ne
servent que sur une installation existante.

---

## Méthode

Quelques règles que ce chantier a imposées, souvent en les payant :

- **Patcher le site d'appel, jamais le corps.** Les prédicats bouchonnés du
  build sont partagés par des centaines d'appelants : `0x180007450` en a 210.
  Le sens est dans l'appel, pas dans la fonction.
- **`.pdata` ne liste pas les fonctions feuilles.** Toute affirmation du type
  « personne n'appelle X » exige un balayage **linéaire** de `.text`. Une
  itération sur `.pdata` ne donne qu'un minorant — et a produit ici plusieurs
  conclusions fausses.
- **Une table régulière n'est pas une table identifiée.** Les tables de modes
  et de sous-états sont indexées par leur premier champ, pas par leur position.
- **Ne pas neutraliser une garde partagée.** La débrancher pour un cas la
  débranche pour tous ; il faut soigner ce qui remplit la variable testée.
- **Mesurer avant de corriger.** Chaque fois qu'une cause a été supposée plutôt
  que mesurée, elle s'est révélée fausse à l'écran.

---

## Ce que ce dépôt ne contient pas

Ni ROM, ni dump, ni archive de jeu, ni exécutable du jeu, ni asset extrait, ni
outil tiers. Les documents citent des adresses et des séquences d'octets à des
fins d'analyse ; ils ne permettent pas de reconstituer l'œuvre.

*Virtua Fighter* est une marque de SEGA. Ce travail n'est ni affilié à SEGA, ni
approuvé par SEGA.
