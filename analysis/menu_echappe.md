# Le menu de la touche ÉCHAPPE — posé le 2026-11-19

Demande de Frédéric : « déplace la fonction actuelle de la touche ECHAPPE sur
la touche Q. En te basant sur `Fighting Vipers 2`, ajoute un menu qui s'ouvre
avec la touche ECHAPPE et qui appelle les mêmes types d'options à valider
ensemble, une à une. »

**Posé et compilé. Non vérifié à l'écran** : c'est l'écran qui tranche, et
Frédéric seul lance le jeu.

---

## 1. Ce que portait ÉCHAPPE, et pourquoi ce n'est pas un déplacement de fonction

ÉCHAPPE ne portait pas une fonction : elle portait le **code 15**, et c'est le
**moteur** qui lit ce code — `Input_isOnNow(15)` en `0x18021490F` — pour
quitter un mode et revenir au menu. Rien dans la greffe ne décide de ce que le
code 15 fait. « Déplacer la fonction » se réduit donc à changer la touche du
code 15.

Deux conséquences, mesurées dans `gen_apm_stub.py` avant d'écrire :

| | |
|---|---|
| **`Q` était déjà prise** | elle était le défaut du **code 14**, le 4e bouton d'action, celui que l'écran OPTIONS > Controls affiche « NO USE ». Deux rôles sur une touche s'**additionneraient** : presser Q aurait quitté le mode **et** appuyé sur le 4e bouton. |
| **ÉCHAPPE devient le code 31** | le moteur ne lit que les codes 0 à 15, et `--joueur2` réserve 18 à 30. Des 32 créneaux du stub, 16 et 17 portent les deux boutons de caméra de l'écran terminal (mesure de `boutons_terminal.py`, 2026-09-30) : **le 31 était le dernier libre**, et personne dans le moteur ne le lit. |

La disposition posée :

```
    ECHAP   ouvre notre menu        code 31  (a nous seuls)
    Q       quitte le mode courant  code 15  (etait sur ECHAP)
    A       le 4e bouton, NO USE    code 14  (etait sur Q)
```

Le code 14 passe sur `A`, ce qui est **déjà** ce que la disposition vivante
donne (`tools/scenarios/jouer.txt` porte `touche 14 = a` depuis le
2026-09-03) : le défaut du C rejoint le fichier au lieu de le contredire.
La manette garde `BACK` sur le code 15, inchangée.

---

## 2. Ce qui est repris de Fighting Vipers 2, et ce qui ne pouvait pas l'être

Le menu de `fv2-recomp` (`src/host/menu.h`, `menu.cpp`, page racine dans
`main.cpp:4881`) est bâti sur **RmlUi**, au-dessus d'un hôte **SDL3** que ce
projet-là écrit lui-même. Nous n'avons ni l'un ni l'autre : notre hôte est le
`vfes.exe` de SEGA, et notre seul point d'entrée est la greffe. **Rien de son
code n'est transposable.**

Ce qui se transpose, c'est son **modèle**, et il est repris ligne pour ligne :

- une page de lignes, chacune avec son intitulé et son **aide** affichée sous
  les lignes quand elle est choisie (`menu_item::help`) ;
- des **titres de section** non sélectionnables (`menu_item::heading`) ;
- des lignes **à valider une à une** (`menu_item::activate`, Entrée) et des
  lignes **à choix** que Gauche/Droite changent (`menu_item::change`) ;
- et sa **règle**, écrite noir sur blanc dans son `main.cpp` : *« A line with
  nothing to switch keeps its place and is stepped over […] drawn, dimmed, and
  passed by — rather than quietly missing. Each says below why it is one. »*
  Une page dont les lignes montent et descendent selon ce qui est disponible
  se lit mal d'un coup d'œil.

L'ordre de sa page racine est gardé : Reprendre, Réglages d'arcade, Son,
Affichage, En ligne, Manettes, Quitter.

### Les cinq lignes qui agissent

| ligne | ce qu'elle fait | par quoi |
|---|---|---|
| Reprendre | referme le menu | — |
| Quitter le mode courant | rend la main au menu principal | pose le **code 15** |
| Ouvrir le menu TEST | le bouton TEST de la borne | pose le **code 0** |
| Ouvrir le menu SERVICE | le bouton SERVICE de la borne | pose le **code 1** |
| Quitter le jeu | écrit le profil du Quest s'il en court un, puis ferme | **deux** validations |

Les trois premières posent un appui par **`g_impulsion`** : un masque OR'é dans
`g_masque` par la composition des entrées, qui retombe seul au bout de
`g_impulsion_duree` (120 ms par défaut). C'est le canal que la ligne
`impulsion = …` d'`apm_entrees.txt` emploie déjà ; le menu s'en sert du dedans,
sans passer par le fichier.

### Les quatre lignes grisées, et ce qui manque à chacune

Ce ne sont pas des trous : chacune nomme une mesure du dossier.

| ligne | ce qui manque |
|---|---|
| Musique et volumes | seule la BGM du Quest est nommable (`quest_musique`). Les volumes n'ont pas été trouvés. |
| Résolution de rendu | elle est écrite dans `vfes.exe` **et** dans le moteur, et lue au démarrage. `patch_resolution.py` la change, et il faut relancer. |
| Jouer en ligne | le netcode de bornes liées du build APM3 est intact, mais il n'est exposé nulle part. |
| Disposition des touches | `apm_entrees.txt` se change à chaud, relu toutes les 500 ms sans relancer. |

---

## 3. Deux manques qui sont assumés, pas oubliés

**Le jeu n'est pas mis en pause.** `fv2-recomp` est un hôte : il arrête sa
boucle. Nous sommes une greffe **dans** la boucle de SEGA, et rien dans le
dossier ne dit comment l'arrêter. Le menu se dessine par-dessus un jeu qui
**continue dessous** — c'est pourquoi la première ligne le dit au lieu
d'annoncer « reprendre ».

**La manette ne pilote pas le menu.** Le clavier est confisqué au jeu pendant
que le menu est ouvert, par le même geste que la saisie du nom de données
(`g_nom_saisie` fait rendre 0 à `lire_clavier`) : sans cela, naviguer
piloterait le combattant. La manette, elle, n'est pas confisquée et ne navigue
pas.

---

## 4. La fenêtre de front, 34 ms → 10 ms

Posée dans le même geste, parce qu'elle touche les mêmes fichiers. C'est la
réponse au deuxième point de Frédéric — « un appui, s'il est un peu trop long,
enregistre plusieurs appuis et donc plusieurs validations » — et elle est
**mesurée** : voir `menus_repetition_appui.md` pour le détail.

En bref : `0x1801A2BC0` appelle `Input_isOnNow(7)` **en direct**, sans tenir le
moindre historique ; cette fenêtre décide donc à elle seule du nombre de
validations qu'un appui produit. À 60 i/s la trame dure 16,7 ms et les
scrutations tombent à 0 / 16,7 / 33,3 ms : **deux ou trois** dans une fenêtre
de 34. 10 ms est la valeur établie par la mesure du 2026-09-05
(`carte_options.md` §10).

La régression, nommée : le correctif de septembre n'avait été posé que dans
`tools/apm_entrees.txt` (qui porte bien `front = 10`), et `jouer.cmd` installe
`tools/scenarios/jouer.txt`, daté du 2026-09-03 — **deux jours avant** — qui
n'avait aucune ligne `front`. Or `charger()` remet `g_front = 34` à **chaque**
relecture. Le chemin par lequel Frédéric joue n'avait donc jamais porté le
correctif.

Les trois endroits qui la posent disent maintenant 10 : le défaut du C, la
remise à zéro du lecteur, et la ligne de `jouer.txt`.

**Les directions ne sont pas concernées** : elles passent par `Input_isOn` →
`0x180243ED0`, qui tient son propre historique (`+0x0C`, `+0x10`, `+0x18`) et
qui est correct. Aucun octet du moteur n'a été changé.

---

## 5. Les fichiers, et comment revenir en arrière

| fichier | ce que c'est |
|---|---|
| `VF5RE/tools/apm_menu.h` | **le menu**, 17 413 caractères, ASCII pur. Tout le code neuf est là. |
| `VF5RE/tools/poser_menu_echappe.py` | le poseur : **dix poses**, chacune avec son ancre unique, son témoin et son contrôle. Rejouable. |
| `VF5RE/tools/menu_echappe.cmd` | double-clic : pose puis reconstruit. `menu_echappe.cmd controler` ne fait que contrôler. |
| `VF5RE/tools/gen_apm_stub.py` | 4 poses : `g_apm_menu`, la confiscation du clavier, les deux liaisons de touches, les deux sites de `g_front`. |
| `VF5RE/tools/quest_runtime.c` | 3 poses : les deux déclarations, l'appel au sommet du rappel de rendu, l'inclusion d'`apm_menu.h` à la fin. |
| `VF5RE/tools/scenarios/jouer.txt` | la ligne `front = 10` qui manquait. |
| `VF5RE/jouer.cmd` | la bannière : les deux touches ajoutées, et « 30 ms » corrigé en « 500 ms » (la relecture est à 500, pas à 30). |

Chaque fichier touché a sa copie d'avant à côté de lui, en
`.avant_menu_echappe` — **y compris `runtime/media/vf5fs/apm.dll`**.

### Ce qui est vérifié, et comment

- **les dix poses** : relues dans les fichiers **produits**, chacune ×1, par
  `poser_menu_echappe.py --controler` ;
- **l'ancien état a disparu** : `g_touche[15] = VK_ESCAPE`, `g_touche[14] = 'Q'`
  et `g_front = 34` comptent ×0 — y compris dans la prose, parce qu'un
  commentaire qui mentait a été trouvé et corrigé (`gen_apm_stub.py`, le bloc
  de la fenêtre de temps) ;
- **l'encodage** : le compte de caractères non-ASCII de chaque fichier est
  **inchangé** par rapport à sa sauvegarde (6, 646 et 0) ;
- **la compilation** : `apm.dll` passe de 122 880 à **128 512 octets**, sans
  erreur, et les avertissements sont ceux d'avant ;
- **le menu est dans la DLL produite** : les dix textes du menu comptent ×1
  dans `apm.dll` et **×0** dans `apm.dll.avant_menu_echappe`.

### Ce qui n'est PAS vérifié

- **que le menu paraisse.** Le texte 2D du moteur ne sort que si le jeu de
  sprites de la police est enregistré dans le contexte 2D courant :
  `0x18018CA20` laisse **tomber** la commande, sans un mot, quand il ne l'est
  pas (c'est ce que `quest_diagnostic_police` surveille). Sur les écrans de
  menu et dans le Quest il l'est, c'est mesuré. **En plein combat, personne ne
  l'a vérifié** : le menu peut y être silencieusement invisible.
- **que les trois impulsions agissent** là où le menu s'ouvre. Poser le code 0
  hors d'un écran qui lit TEST ne fera rien.
- **que `front = 10` supprime le symptôme** sur le chemin `jouer.cmd` : jamais
  essayé là. Et « plusieurs » validations est mesuré, « deux ou trois » est
  calculé.
- **la mise en page** : les positions sont en espace 1280 × 720 et n'ont été
  relevées sur aucune capture.

---

## 6. Une chose trouvée en passant, qui demande une décision

`tools/scenarios/jouer.txt` et le code mesuré de `gen_apm_stub.py` **ne
disent pas la même chose** sur les codes d'action :

| | `jouer.txt` (2026-09-03) | `gen_apm_stub.py` (mesuré, octobre) |
|---|---|---|
| code 8 | KICK | **ANNULER** (menus seulement) |
| code 9 | *inconnu* (`v`) | **P** — le poing |
| code 10 | *inconnu* (`b`) | **K** — le pied |
| code 11 | GUARD | validation seulement |
| code 12 | PUNCH | validation seulement |
| code 13 | *inconnu* (`n`) | **G** — la garde |
| code 14 | *inconnu* (`a`) | le 4e, « NO USE » |

La mesure d'octobre vient du masque arcade que `0x180243ED0` compose, et le
commentaire du code dit que « les codes 8, 11 et 12 ne servent qu'à valider ».
Si elle est juste, alors en combat `W`, `X` et `C` — les trois touches sous la
main gauche — **ne frappent pas**, et ce sont `V`, `B`, `N` et `A` qui portent
P, K, G et le 4e bouton.

**Rien n'a été changé là.** C'est la configuration des boutons que Frédéric
demande au point 0 de son `A FAIRE.txt`, et elle se tranche à l'écran, pas
ici.


---

## 7. La course du 19 novembre 2026 : ce qu'elle a mesuré

**Deux lancements, un seul a mesuré quelque chose.**

Le premier n'a jamais démarré le jeu : `course_menu_echappe.cmd` appelait
`vfes.exe` **en nom nu** après un `pushd`, `cmd` ne l'a pas trouvé (9009), et
le script a quand même imprimé « la sonde est restée MUETTE : issue B ». Ce
verdict ne mesurait rien. Le dossier nommait déjà le piège — *chemin absolu à
l'invocation*. Corrigé : chemin absolu, garde d'existence, **issue Z**, et
**la taille des deux journaux comparée avant et après**, le script s'arrêtant
si `quest_journal.txt` n'a pas bougé. Les deux archives du lancement mort ont
été supprimées.

Le second a mesuré. `quest_journal.txt` : 201 743 → 202 343 octets.

```
[quest] menu ECHAPPE : ouvert
[quest] menu ECHAPPE : code 15 pose -- quitter le mode
[quest] menu ECHAPPE : ouvert
[quest] menu ECHAPPE : ferme
```

| issue | verdict |
|---|---|
| **A** — le menu vit | **CONFIRMÉE.** ÉCHAPPE atteint le code 31, le rappel de rendu tombe, la bascule marche. |
| **C** — texte avalé | **écartée.** La capture de Frédéric montre la page entière, lisible. |
| **D** — un appui long ne vaut qu'une validation | **CONFIRMÉE.** Entrée tenue une seconde : **une** ligne `code 15 pose`, pas deux ni trois. La fenêtre de front à 10 ms fait son travail, et c'est la réponse au point 2 de la demande. |
| **E** — 34 ms encore en vigueur | **écartée** par la même mesure. |

Et l'action a bien refermé le menu : sans cela le second `ouvert` n'aurait pas
pu arriver.

**NON VÉRIFIÉ.** Frédéric a validé la ligne 1 (« Quitter le mode courant »)
alors que la consigne disait de valider « Reprendre », ligne 0. Soit **HAUT
n'a pas pris** après son BAS, soit il a choisi cette ligne. Le journal ne
tranche pas, et je ne l'ai pas redemandé. **Q** (issue F) n'est pas
journalisée non plus : le moteur lit ce code 15, pas la greffe.

---

## 8. Ce que la capture a montré, et ce qui a été posé ensuite

Frédéric, devant l'écran : « **la souris n'est pas active sur cet écran,
beaucoup d'options sont grisées inaccessibles** » puis « **il faut un fond
pour que ce soit visible** ». La capture montre les trois à la fois : le menu
se pose sur un décor **qui continue de bouger dessous** — le jeu n'est jamais
mis en pause — et l'ombre noire de deux pixels de `quest_ecrire_ancre` ne
suffit pas sur un fond clair.

### 8.1 Le fond — `0x180195E60`

Trouvé **sans décompiler**, par un grep : `code_decompile/SYSTEME_2D.md` §9.2
établit, degré **CONFIRMÉ**, que `FUN_180195e60` est **la seule primitive de
quad sans texture du module**, et relève ses paramètres en lisant ce que son
unique appelant écrit sur la pile :

```
FUN_180195e60(float x1, float y1, float x2, float y2,
              0x11, 0x1D, couleur, 0)
```

Elle n'écrit **jamais** `+0x14` : le quad prend la **couche courante**. On
l'entoure donc du même sauver / poser / restaurer que `quest_ecrire_boite`, et
on garde sur `DAT_18075e010` — le gestionnaire qu'elle passe à `0x180199890`
sans le vérifier, et qui est nul avant que le système 2D soit monté.

Les couleurs sont en **ABGR** : `QUEST_COUL_JAUNE` vaut `0xFF00FFFF` et paraît
**jaune**, ce qui exclut l'ARGB.

**DEUX CHOSES NE SONT PAS VÉRIFIÉES, et c'est l'écran qui tranche :**

* **l'ordre.** Le quad porte le créneau 29, le texte son rang 127. Rien dans
  les notes ne dit lequel passe devant. Si le fond **recouvre** le menu, on
  verra un rectangle sombre et rien dedans.
* **l'alpha.** On ne sait pas si ce chemin mélange ou écrase. S'il écrase, le
  fond sera opaque au lieu d'être voilé — lisible quand même.

C'est pour ces deux raisons que **la touche `F` l'éteint et le rallume dans le
jeu** : une seule course répond aux deux questions, sans reconstruire entre
les deux.

### 8.2 La souris

Elle n'a **jamais** existé ici, et ce n'est pas une régression :
`fv2-recomp` a RmlUi et SDL3, qui portent un vrai pointeur ; nous dessinons
dans le contexte 2D du jeu depuis le rappel de rendu, et il n'y a aucun
pointeur à recevoir. On le fabrique : `GetCursorPos` → `ScreenToClient` →
`GetClientRect` → espace 1280 × 720. **La mise à l'échelle n'est pas
décorative** : le client n'est pas 1280 × 720, il est à la résolution que
`patch_resolution.py` a posée.

Le survol choisit la ligne — **et seulement s'il a bougé**, sinon une souris
posée quelque part reprendrait la main à chaque image et Haut/Bas seraient
inutilisables. Le clic gauche valide. Hors des lignes, le clic ne fait rien :
il ne ferme pas le menu, parce que rien ne dit à Frédéric que le dehors serait
une sortie.

**NON VÉRIFIÉ : que le curseur soit VISIBLE.** Le jeu peut le cacher à chaque
image par `WM_SETCURSOR`, et un `ShowCursor` n'y pourrait rien. C'est pourquoi
le retour est **la ligne surlignée**, pas la flèche.

### 8.3 La raison tronquée

Sur la capture, la raison sous « Résolution de rendu » finit par « il faut
relan ». `quest_ecrire_ancre` pose une boîte **large de 900** depuis x = 324,
soit un bord à **1224 sur 1280** — 95,6 % de la largeur, exactement là où la
capture coupe. La raison faisait 139 signes ; elle en fait **116**. Les trois
autres étaient déjà sous 120.

### 8.4 Ce qui a été contrôlé, et comment

* `apm.dll` : **128 512 → 130 048 octets**, empreinte MD5
  `E3FA93FA…` → `8DE630D3…`. Une taille **et** une empreinte, parce qu'un
  code de sortie 0 ne prouve rien.
* Les témoins dans le binaire construit : `fond allume`, `fond eteint`,
  `SOURIS choisir`, `puis relancer` → **×1 chacun** dans le produit, **×0**
  dans `apm.dll.avant_menu_echappe`.
* Le **contrôle négatif** : l'ancienne chaîne `il faut relancer` compte **×0**
  dans le produit. Un contrôle qui ne peut pas échouer ne vaut rien ; celui-ci
  échouerait si la raison n'avait pas été raccourcie.
* Les repères comptés **dans le corps du code**, lignes de commentaire
  exclues : `0x195E60` ×1, `GetCursorPos` ×1, `VK_LBUTTON` ×2,
  `apm_fond(APM_FOND_X1` ×1.
* Aucun avertissement nouveau à la compilation — et **aucun**
  `defined but not used` sur `apm_fond` ni `apm_souris`, ce qui prouve
  qu'elles sont appelées.

### 8.5 Les quatre lignes grisées

Elles ne sont pas un bug : **rien n'est branché derrière**, et chacune dit
pourquoi, à l'écran. Ce qu'il faudrait, par ordre de coût réel :

| ligne | ce qui manque |
|---|---|
| Disposition des touches | **la moins chère** : `apm_entrees.txt` est relu à chaud toutes les 500 ms. Il faut une page d'édition dans le menu, pas une découverte. |
| Résolution de rendu | elle est écrite dans `vfes.exe` **et** dans le moteur, lue au démarrage. `tools/patch_resolution.py` la change, mais il faut relancer le jeu. |
| Musique et volumes | seule la BGM du Quest est nommable (`quest_musique`). **Les volumes n'ont pas été trouvés** dans le module. |
| Jouer en ligne | le netcode de bornes liées est intact, mais **rien ne l'expose**, et le mur mesuré est ailleurs : aucun STUN sur `127.0.0.1:3478`. Voir `en_ligne_vf3_transposable.md`. |


---

## 9. « Le menu est toujours illisible » — la capture du 19 novembre, 20 h 38

Frédéric a joint une capture. Elle **tranche deux issues d'un coup**, et les
deux étaient nommées d'avance dans l'en-tête de `course_menu_echappe.cmd` :

- **issue U, acquise** : le jeu est dans une **fenêtre** titrée
  « Virtua Fighter 5 FS (PXD/64bit) ». `apm_fenetre.txt` est lu, le style est
  reposé, la fenêtre est centrée. Le journal l'avait dit —
  `fenetre : 1280 x 720 demandes, cadre 1296 x 759` — et **l'écran le
  confirme**, ce qui est le seul ordre qui compte.
- **issue I, tombée** : il n'y a **aucun fond**. Le menu se pose tel quel sur
  le MAIN MENU du jeu — lettres blanches du menu sur lettres blanches du jeu,
  d'où « illisible ». Ce n'est pas le menu qui manque : c'est le **quad**
  `0x180195E60` qui n'a rien mis à l'écran.

### 9.1 Pourquoi `quest_ecrire_ancre` ne suffisait pas

Elle pose **une** ombre noire, décalée de `+2,+2`. Une ombre détache d'un fond
**uni**. Elle ne détache pas d'un **texte** : là où le MAIN MENU a ses propres
lettres blanches, l'ombre tombe sur du blanc et ne sépare rien.

### 9.2 Le contour épais — le chemin qui, lui, est prouvé

`apm_ecrire()` dans `apm_menu.h` : **huit** copies noires autour de la lettre
(`-2,0,+2` en x croisé avec `-2,0,+2` en y, le centre exclu), puis la couleur
par-dessus. Neuf commandes de texte au lieu de deux : c'est plus cher, et
c'est le **seul** chemin dont on sache qu'il arrive à l'écran, puisque c'est
celui qui a dessiné la page de la capture.

Les **17** appels à `quest_ecrire_ancre(` du menu sont passés par lui ; il en
reste **zéro** dans `apm_menu.h`. Le contour reste utile même quand le fond
marchera.

### 9.3 La sonde du fond — trois états, pas deux

Un silence ne distingue pas une garde qui mord d'un appel qui part dans le
vide. `apm_fond()` dit donc, **une ligne, une fois, à l'instant où elle
arrive**, sans période et sans plafond, lequel des trois états tient :

| issue | ce que le journal dit | ce que ça ferme |
|---|---|---|
| **I1** | `fond : gestionnaire NUL, la garde a mordu` | `DAT_18075e010` est nul quand le menu dessine : le quad n'est **jamais** appelé. Ce n'est ni l'ordre ni le créneau. **La route du quad se ferme** — il faudra un sprite (`quest_sprite` existe et ne sert à rien). |
| **I2** | `fond : gestionnaire present, le quad est appele` | l'appel **a eu lieu** et l'écran ne montre rien : c'est l'**ordre** ou le créneau, comme l'issue H le prévoyait. **La route reste ouverte.** |
| **I3** | rien sur `fond :` | `apm_fond` n'est pas appelé, ou `g_quest_base` est nul avant la sonde. C'est le troisième état, et il ne se confond avec aucun des deux autres. |

### 9.4 Ce qui est mesuré, et ce qui ne l'est pas

Mesuré sur le binaire, avant toute course :

| contrôle | compte | attendu |
|---|---|---|
| exports de `apm.dll` | 57 | 57 |
| dépendances | **DLL du système seulement** | idem (le contrôle du bâti le vérifie et rend 1 sinon) |
| `fond : gestionnaire present` dans `apm.dll` | 1 | 1 |
| `fond : gestionnaire NUL` dans `apm.dll` | 1 | 1 |
| les deux dans `apm.dll.avant_menu_echappe` | 0 | 0 — **le contrôle négatif** |
| `quest_ecrire_ancre(` restants dans `apm_menu.h` | 0 | 0 |
| non-ASCII dans `apm_menu.h` | 0 | 0 |

**Non mesuré, et ça compte** : que le contour épais soit *suffisant*. Deux
pixels de noir sur un fond clair et chargé, c'est un pari — c'est l'issue **X**,
nommée d'avance. Et rien, dans aucun journal, ne dit pourquoi le quad est muet :
c'est précisément ce que la sonde va dire à la prochaine course.

### 9.5 Une faute attrapée par un contrôle, et pas par une course

Le poseur des consignes a d'abord écrit **28 sauts de ligne nus** dans un
`.cmd` qui est en CRLF — les guillemets triples d'un fichier Python en LF. Le
contrôle `sauts de ligne nus (hors CRLF)` a rendu 28 au lieu de 0 et **rien
n'a été écrit**. C'est l'office d'un contrôle : échouer sur une faute réelle.


## 10. Le menu passe hors du moteur : une fenêtre superposée en Direct2D

**Le 19 novembre 2026, 21 h 16.** Frédéric : « menu ECHAPPE illisible, tu ne
respectes absolument pas le modèle FV2 que je t'ai donné. Le curseur de la
souris n'est pas visible sur ce menu de type PC. Le ring out semble correct. »

Les deux premières phrases disent la même chose, et la troisième ferme
l'issue AA.

### 10.1 Pourquoi le chemin du jeu était une impasse, et c'est mesuré

La sonde du fond a rendu, dans la course du soir :

```
fond : gestionnaire NUL, la garde a mordu
```

`DAT_18075e010` est **nul** au moment où le menu dessine. Le quad
`0x180195E60` n'est donc **jamais appelé** : ce n'était ni l'ordre de dessin
ni le créneau, c'est que la primitive n'est pas atteignable depuis là. La
route du lot 2D du jeu se ferme — issue **I1**, et les issues I2 et I3 avec
elle.

Et le modèle que Frédéric donne depuis le début dit la même chose autrement :
**fv2-recomp dessine son menu avec SON PROPRE rendu** (SDL3 + RmlUi,
`src/host/menu.cpp`, `assets/ui/menu.rml`), par-dessus le jeu, et jamais avec
le rendu du jeu. FV2 est une recompilation : il possède son rendu. Ici le jeu
n'est pas recompilé — alors on prend la seule place équivalente.

### 10.2 APM3 rend en Direct3D **11**, pas 12

Mesuré sur les imports de `vfes.exe` : `d3d11.dll`, `dxgi.dll`, `d2d1.dll`,
`D3DCOMPILER_47.dll`. La ligne « l'image passe par D3D12 » du `CLAUDE.md`
parle de **l'hôte REVO**, qui est un autre chantier. J'avais dit D3D12 ici :
c'était faux.

Et le jeu **construit déjà Direct2D lui-même**, sur son propre `IDXGIDevice`
(`hote_apm3.md` §21.6) : `D2D1CreateFactory(SINGLE_THREADED)` →
`ID2D1Factory1::CreateDevice` → `ID2D1Device::CreateDeviceContext`. Le même
chemin nous est donc ouvert, sur le même périphérique.

### 10.3 Ce qui a été posé

`VF5RE/tools/reseau/apm_overlay.cpp` — accroche
`IDXGISwapChain::Present` **et** `Present1`, et dessine en Direct2D /
DirectWrite sur le tampon arrière.

L'accrochage ne connaît **aucune adresse du jeu** : la table de méthodes
d'une chaîne d'échange est partagée par toutes les instances de sa classe.
On fabrique donc une chaîne à nous, de 8 × 8, sur une fenêtre cachée
(`apm_ov_cachee`), on lit sa table, et on y pose nos deux fonctions. Celle du
jeu passe alors par nous sans qu'on ait eu à trouver son objet, et sans rien
supposer de son ordre de démarrage.

**On accroche les deux parce qu'on ne sait pas laquelle le jeu appelle**, et
chacune dit au journal sa première venue : le journal tranchera.

Le modèle visuel est celui de `menu.rcss`, en dp (1 dp = hauteur / 720) :
voile plein écran en dégradé horizontal `#040818f2` → `#04081850`, panneau à
9 % de la gauche, titre 40 dp gras italique `#ffd23f` souligné de 3 dp, fil
17 dp `#8fa3d6`, lignes 20 dp `#c3cff0`, valeurs `#ffd23f`, ligne choisie sur
une barre `#ffd23f` à 18 % avec un filet de 3 dp à gauche. Police « Barlow
Condensed », repli « Segoe UI ».

**Le panneau est plus large que celui de FV2** (900 dp au lieu de 520) et
c'est voulu : les lignes de FV2 portent des intitulés courts, les nôtres
portent en plus la **raison** de chaque ligne éteinte, longue de cent vingt
signes. Une de ces raisons a été tronquée à l'écran ce même jour parce que la
boîte s'arrêtait à 1224 sur 1280.

Côté menu, `tools/apm_menu.h` ne dessine plus : il **décrit** sa page
(`apm_ov_page_debut` / `apm_ov_page_ligne` / `apm_ov_page_fin`), pour les deux
pages — la racine et le salon. C'est le partage de fv2-recomp, où `menu.cpp`
remplit des `menu_item` sans savoir comment ils paraîtront.

### 10.4 Deux choses qui ne se devinent pas, et qui sont réglées

**La géométrie appartient à celui qui dessine.** Les ordonnées étaient
relevées côté C (`g_apm_y[]`) parce que le C dessinait. Maintenant c'est la
superposition qui décide où tombe chaque ligne, en dp d'une fenêtre dont le C
ignore la taille. Elle retient donc les rectangles **réellement dessinés**, et
le C demande `apm_ov_ligne_sous(x, y)` au lieu de recalculer. Les rectangles
sont retenus **en dp**, parce que `apm_souris` convertit déjà la souris dans
un espace haut de 720 : les deux côtés tombent dans le même espace sans que
l'un connaisse la résolution de l'autre.

**Un rang n'est pas une ligne.** La page envoyée porte 21 rangs pour 17
lignes : chaque ligne éteinte est suivie de sa raison, qui occupe un rang.
`g_apm_rang[]` garde la correspondance **à l'instant où on envoie** — le seul
endroit qui la connaisse — et vaut −1 pour un rang qui n'est pas une ligne.

### 10.5 Deux fautes trouvées **sans lancer**, dans mon propre code

1. **`monter()` rendait `false` sans un mot, sur six chemins.** `peindre` ne
   faisait alors rien, pour toujours, et le journal restait muet : le menu
   n'aurait pas paru sans qu'on sache pourquoi. Pire, après un échec à
   mi-chemin, `g_devdxgi` était déjà posé, donc la trame suivante prenait le
   raccourci `g_devdxgi == dxgi` et rendait `false` sans même réessayer — une
   impasse muette et définitive. **Un refus et une absence ne sont pas la même
   chose.** Les six causes se nomment maintenant, chacune une fois, et posent
   `g_mort`.
2. **Rien ne disait qu'une image avait été dessinée.** Si l'écran reste noir,
   « jamais dessiné » et « dessiné mais invisible » sont deux pannes opposées.
   Une ligne tombe maintenant à la **première image**, une fois, sans période
   et sans plafond, et elle porte le nombre de rangs et la taille de la cible :
   zéro rang serait une troisième panne encore.

### 10.6 Ce qui n'est pas couvert, et il faut le dire

`__try` / `__except` **n'existe pas chez le GCC de mingw**, qui compile cette
greffe. On ne peut donc pas rattraper une faute matérielle sur le fil de
rendu du jeu. À la place, chaque `HRESULT` et chaque pointeur est vérifié, et
au premier refus `g_mort` est posé pour de bon. Ça couvre les pannes que l'API
annonce ; ça ne couvre pas un déréférencement nul. **C'est la limite réelle de
cette route**, et c'est la rançon du choix B.

Et l'ancien dessin **reste**, derrière `apm_ov_vivant()` : si l'accrochage est
refusé, le menu reste pilotable comme avant au lieu de disparaître.

### 10.7 Le curseur de la souris

Le jeu l'efface, et un menu de type PC sans curseur ne se pilote pas.
`ShowCursor` est un **compteur**, pas un drapeau : on monte une fois à
l'ouverture, on redescend une fois à la fermeture, avec notre propre état pour
ne jamais poser deux fois dans le même sens. Appelé à chaque trame, le
compteur dériverait sans retour.

### 10.8 L'état mesuré, et ce qui ne l'est pas

Mesuré : `apm.dll` compile à **670 208 octets**, 7 objets réseau, dépendances
« seulement des DLL du système », et `d2d1.dll`, `d3d11.dll` et `DWrite.dll`
figurent désormais dans ses imports — ce qui prouve que la superposition a bien
été liée. Les chaînes `superpose : PREMIERE IMAGE dessinee`,
`REFUS -- ID2D1Factory1::CreateDevice`, `le jeu passe par Present1` et
`accrochage pose sur Present` sont présentes dans le binaire.

**Pas mesuré, et c'est l'essentiel : rien de tout cela n'a été vu à l'écran.**
Les issues S1 à S8 sont écrites d'avance dans l'en-tête de
`tools/course_du2_ringout.cmd`. C'est l'écran qui tranche.
