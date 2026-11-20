---
name: project_3sx_chaine_traduction
description: "La chaîne d'outils qui traduit les textes de 3SX : catalogue UTF-8 en entrée, tables C vérifiées en sortie."
metadata: 
  node_type: memory
  type: project
  originSessionId: a058425c-294d-45ef-8ac9-baf6a4cfd208
  modified: 2026-08-25T22:21:09.579Z
---

Construite le 2026-08-25, dans `C:\Temp3sx\tools\`. Documentée par
`C:\Temp3sx\docs\traduction_texte.md`. Périmètre : citations de victoire, dialogues
d'avant-combat et fins — voir [[project_3sx_traduction]].

**La traduction française est écrite** (2026-08-26) : 540 messages, 986 lignes, les 20
personnages. 0 erreur, 0 alerte.

**Build de test** : `C:\3sx-fr`, clone de l'amont `513380f9` avec les deux patches
(`effb6-accents.patch`, `langue-fr.patch`) et `message/fr/`. Raccourci **3SX francais** sur
le bureau, vers `C:\3sx-fr\3SX-francais.cmd`. La ligne `Options > Screen Adjust > LANGUAGE`
fait défiler **EN, JP, FR** ; `Get_Default_Language` choisit FR sur une machine en français.
Compilé sans un seul avertissement, et le jeu se lance.
**Le texte n'a encore été vu par personne à l'écran.**

**Le build de test a son propre profil**, `C:\3sx-fr\profil`, avec une jonction vers les
resources partagées. Ce n'est pas du confort : le choix de langue va dans la sauvegarde, et
`C:\3sx-up` ne connaît que EN et JP — en relisant FR il irait chercher
`Letter_Data_64[9][2]`, qui vaut `NULL` chez lui. Contrepartie : sauvegarde vierge.

**Le principe** : le traducteur n'écrit ni code ni échappement. Il remplit
`traduction\fr.txt` en français accentué ordinaire ; le générateur produit les tables C.
Deux lanceurs : `traduire-extraire.cmd` puis `traduire-generer.cmd`. Les deux sont
relançables — les blocs déjà traduits sont conservés, les blocs vides restent en anglais,
donc on peut compiler et jouer à tout moment avec une traduction partielle.

**L'encodage des accents s'est joué sur une observation** : `src_han_alpha2` (effb6.c) est
du **code source, pas de la donnée** — seul l'indice compte, il désigne l'objet
`j + 256 + 0x7F30`. Les jetons sont donc libres. Ceux d'origine (`%` `)` `(` `,`)
apparaissent dans les textes anglais — `(A` quatre fois, dans `(ALEX)` — et auraient
corrompu l'anglais. Remplacés par des octets qu'aucun texte n'emploie, vérifié sur les 58
fichiers de personnages plus msgsysdir/msgextra/msgmenu :
`` ` `` grave, `*` aigu, `^` circonflexe, `=` tréma, `~` tilde, `;` cédille.

**Ce qui est prouvé, pas supposé** : `tools/msg_verifier.py` rejoue l'ancien et le nouveau
lecteur sur les 1158 lignes anglaises et compare les suites de numéros d'objet — 0
différence, donc le changement de `effb6.c` est neutre pour l'anglais. Puis il relit les
986 lignes générées en remontant des numéros d'objet vers les caractères — 0 faute.
`traduire-generer.cmd` lance ce contrôle à chaque génération.

**Piège payé** : le contrôle de largeur mesurait la colonne sans compter le retrait que le
jeu ajoute (3 pour citations/fins, 2 pour dialogues). Il laissait donc passer des lignes
trois colonnes trop loin. Corrigé : le budget de frappe est de **40 signes**, une seule
règle pour tout, et `msg_build.py` relit le retrait dans l'original.

**Vérifié aussi** : les 118 fichiers générés et le `effb6.c` corrigé compilent avec les
flags exacts du projet (`-Wall -Werror` plus les `-Wno-*` du CMakeLists), sortie vide,
code 0. Et `file(GLOB_RECURSE GAME_SRC CONFIGURE_DEPENDS src/*.c)` dans le CMakeLists amont
prend les nouveaux fichiers sans rien déclarer.

**Deux pièges du terrain** :
- `C:\3sx-up` est en **CRLF** dans la copie de travail alors que les blobs sont en LF ; les
  outils normalisent en LF et restituent la convention d'origine. Voir
  [[reference_3sx_amont_decalages]].
- `pl_tlk_tbl` de l'amont fait pointer Akuma (14) et Q (17) sur le tlk d'un voisin, faute de
  fichier propre. Le générateur reproduit cet aiguillage en le relisant dans `msgtable_en.c`
  plutôt qu'en le recalculant.

**Les lanceurs n'écrivent dans aucun clone par défaut** : la sortie va dans
`traduction\message_fr\`, et `CIBLE` en tête de `traduire-generer.cmd` permet de viser un
clone de travail. `C:\3sx-up` est lu seulement.
