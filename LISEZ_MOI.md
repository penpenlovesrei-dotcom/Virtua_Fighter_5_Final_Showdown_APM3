# VF5 Final Showdown, build arcade APM3 — rétro-ingénierie

Ce dossier rassemble le travail de rétro-ingénierie de **Virtua Fighter 5
Final Showdown, build arcade APM3** (SEGA ALLS, Windows x64), pour qu'un
tiers puisse le reprendre sans rien avoir à redécouvrir.

Il a été extrait le **2026-11-01** du dépôt de travail
`C:\Users\frede\Desktop\VF5RE`. `MANIFESTE.txt` donne, fichier par fichier,
d'où chacun vient, et les empreintes SHA-256 des binaires.

---

## Commence par là

1. **`ETAT_DECOMPILATION.md`** — l'état réel, chiffré et reproductible, de ce
   qui est décompilé et de ce qui ne l'est pas. À lire en premier : il évite
   de croire le travail plus avancé qu'il ne l'est.
2. **`ANALYSER_ET_MESURER.cmd`** — double-clic. Reconstruit la base Ghidra du
   moteur (deux minutes) et refait toutes les mesures devant toi.
3. **`documentation/mode_quest.md`** — 7 981 lignes, le chantier en cours :
   porter le mode Quest de la version Xbox 360 de 2007 vers le build arcade.
4. **`documentation/_journal/REPRISE_QUEST.md`** — le prompt de reprise de la
   dernière séance : où le travail s'est arrêté, et le piège suivant.

---

## La pièce centrale, en trois phrases

Le jeu est `vfes.exe` (base `0x140000000`), un lanceur de 2 Mo qui charge
`vf5fs-pxd-w64-Retail_APM3.dll` (base `0x180000000`), 7 Mo, où vit tout le
jeu. La borne attend une troisième DLL, `apm.dll`, que SEGA fournit pour
parler au matériel d'arcade : elle a été **remplacée par une greffe** à nous
(`outils/quest_runtime.c`, compilée par `outils/gen_apm_stub.py`), qui
réimplémente 57 de ses 106 exports et sert de point d'entrée pour ajouter du
code au jeu sans toucher au moteur.

Le moteur est **PXD**, le moteur maison de SEGA : le même que Yakuza 6 et que
Project DIVA. C'est pourquoi les planches d'interface 2D sont au format
**AET**, et les sprites au format **FARC/SPRSET** — les outils publics de la
communauté DIVA s'y appliquent.

---

## La carte du dossier

| dossier | contenu | volume |
|---|---|---|
| `binaires/` | les binaires de référence, originaux **et** patchés, avec leurs SHA-256 | 7 fichiers, 19 Mo |
| `documentation/` | **66 documents d'analyse** `.md`, le cœur du savoir, plus `_journal/` (les prompts de reprise et le journal de bord) et `docs/formats/` (les formats de fichiers du jeu) | 76 fichiers, 2,6 Mo |
| `code_decompile/` | le **C sorti du décompilateur Ghidra**, 228 fichiers : 411 fonctions du moteur, 619 fonctions PowerPC des versions Xbox 360 | 1,8 Mo |
| `desassemblage/` | l'assembleur commenté des fonctions charnières | 36 fichiers |
| `donnees/` | relevés, tables, inventaires : `.json`, `.csv`, `.txt`, listings d'archives | 143 fichiers, 24 Mo |
| `csharp_apm3/` | les 13 classes C# du système de borne `Apmv3System` (Unity) | 13 fichiers |
| `outils/` | **248 scripts Python** : patcheurs, lecteurs de formats, sondes, générateurs — plus les lanceurs `.cmd` et la greffe en C | 398 fichiers, 2,9 Mo |
| `mesures/` | les scripts Ghidra qui produisent les chiffres d'`ETAT_DECOMPILATION.md` | 7 fichiers |

**Ce qui a été volontairement laissé de côté :** les 396 Mo de captures
d'écran (`*.png` — relevés visuels, balayages, sondes), les outils tiers
livrés dans `tools/` (Sofdec2, PARtool, PS4 PKG Tool, convertisseur ADX), les
données de jeu extraites (`extracted/`, plusieurs Go), et les projets Ghidra
eux-mêmes — ces derniers parce qu'ils ne contenaient **aucune annotation
humaine** et se refont en deux minutes (voir `ETAT_DECOMPILATION.md`, §1).

Si tu partages ce dossier, note que `binaires/` contient du code de jeu
commercial : il est isolé dans son propre sous-dossier pour pouvoir être
retiré d'un seul geste.

---

## Les outils à connaître, par usage

**Lire le code du moteur**

- `DECOMPILER.cmd 0x180171F40` — le C d'une fonction, par adresse.
- `outils/pe_disasm.py` — désassemblage ciblé, recherche de références
  croisées, remontée au début d'une fonction. Autonome (capstone + pefile),
  sans Ghidra.
- `outils/couverture.py` — la surface qu'un mode de jeu atteint vraiment,
  par graphe d'appels directs.

**Les formats de fichiers du jeu**

- `outils/aet.py` et `outils/arbre_aet.py` — les planches d'interface 2D.
  `arbre_aet.py` déplie une composition récursivement et donne la position
  absolue de chaque élément : **toute la mise en page d'un écran est dans la
  planche**, il n'y a rien à chercher à l'écran.
- `outils/bases_2d.py` — reconstruit les planches et jeux de sprites, et sait
  importer une composition d'une autre version du jeu.
- `outils/textures_2007.py` — sort les textures d'un `spr_*.farc` en PNG.
- `documentation/docs/formats/` — les formats écrits noir sur blanc : `farc.md`,
  `mothead.md`, `mot_tables.md`, `apm_input.md`, `xbox360_outils.md`.

**Modifier le jeu**

- `outils/patch_moteur.py` — **le** patcheur du moteur. Toute modification du
  moteur passe par lui, jamais par un éditeur hexadécimal : il part toujours
  du `.origine` et réécrit, ce qui rend chaque patch rejouable.
- `outils/gen_apm_stub.py` + `outils/quest_runtime.c` — la greffe compilée
  dans `apm.dll` (gcc, MSYS2). C'est là qu'on ajoute du code au jeu.
- `outils/patch_resolution.py` — le seul outil qui touche `vfes.exe`.

---

## Les règles de travail, apprises à la dure

Elles ne sont pas des préférences : chacune a coûté une séance.

1. **Aucune supposition. On lit le code, on décompile, on mesure.** Un essai
   à l'écran ne remplace pas une lecture : cinq essais de dessin de sprite ont
   été dépensés là où une seule décompilation montrait que le modèle copié
   était le mauvais (`documentation/mode_quest.md`, §37.26).
2. **Vérifier le dossier avant de construire dessus.** Deux « faits »
   documentés se sont révélés faux. Quand un chiffre compte, remesure-le dans
   le `.origine`.
3. **Un essai qui ne distingue pas deux hypothèses ne mesure rien.** Déclarer
   768 sur une planche de 720 ne changeait rien, parce que 768 était déjà la
   valeur par défaut. Il fallait l'inverse.
4. **Après chaque patch, relire les sites dans le binaire PRODUIT**, au
   désassembleur — jamais dans le script qui les écrit. Le patcheur réécrit
   des fonctions entières ; ce que tu crois avoir posé n'est pas toujours ce
   qui est là.
5. **Ne jamais patcher pendant que le jeu tourne.** Vérifie avec `tasklist`.
6. **Ne jamais écrire directement un fichier du dépôt** : écrire à côté, puis
   `os.replace`. Une écriture interrompue a déjà détruit un source.
7. **Les maillons retirés** : quand une fonctionnalité manque dans le build
   arcade, elle est rarement absente — la valeur est posée puis effacée, ou
   l'appel est remplacé par un bouchon. Cherche le motif avant de réinventer.

---

## Ce qui reste à faire, par ordre de rendement

1. **L'exécutable `vfes.exe` est vierge** : 0,6 % de ses 5 548 fonctions ont
   été regardées, et il porte le son. C'est le plus gros gisement.
2. **Annoter la base Ghidra du moteur.** Zéro fonction renommée sur 13 856,
   alors que `documentation/` contient de quoi en nommer plusieurs centaines.
   Un script qui lirait les `.md` et poserait les noms ferait gagner un temps
   considérable à tous les suivants.
3. **Finir le mode Quest** — l'état exact est dans
   `documentation/_journal/REPRISE_QUEST.md` : les deux pavés
   « Main Costume / Type A » à dessiner, le cadre de la monnaie, les deux
   fenêtres du bas, huit libellés de tournoi absents de l'import.
4. **`apmgamepad.dll`** n'a jamais été ouverte (222 fonctions, 10 exports).
