---
name: project-fv2-menu-console
description: "Menu console de FV2 : le document qui fait foi est SupermodelSrc/Docs/MenuConsole.md."
metadata: 
  node_type: memory
  type: project
  originSessionId: 7d3168ca-275c-4d30-8e06-abc13121b915
  modified: 2026-08-16T12:00:27.574Z
---

**Le document qui fait foi est `SupermodelSrc\Docs\MenuConsole.md`** : chemin
des entrées, protocole son, détection d'état, les treize réglages de GAME
ASSIGNMENTS avec adresses, plages et valeurs d'usine, le VS DIAGRAM, et les
leçons de méthode. Ce qui suit n'en est que le résumé.

Le menu console de Fighting Vipers 2 se construit **dans le fork de
Supermodel** (`Src\Menu\`, `Src\OSD\SDL\MenuOverlay.*`), et non plus par
injection de PowerPC en RAM comme le décrit `fv2mod\HANDOFF.md` §9. Ce
changement de position lève quatre murs que ce document donnait pour bloquants.
Lanceur unique : `FV2 - Menu console.cmd`.

**Fait et vérifié à l'écran** : menu des modes par Start en démo, menu de pause
par Start en jeu ; `ARCADE`, `SURVIVAL`, `RANDOM`, `VERSUS` ; `OPTIONS` avec ses
réglages, `INITIALIZE`, et persistance par un fichier à nous ; `SOUNDS` ;
`STATS` ; roster complet ; région `EXPORT` ; freeplay.

**Le VS DIAGRAM est complet depuis le 2026-08-15.** Plus une seule ligne
déduite : `KUHN` est le bloc 13, `B.M.` le bloc 9, et RAXEL/TOKIO/SANMAN ont été
mesurés au passage.

**Page `DISPLAY`, vérifiée à l'écran le 2026-08-15** : première des trois lignes
en gras d'`OPTIONS`, avant `SOUNDS` et `STATS`, avec `WIDESCREEN ON/OFF` qui
bascule le 16/9 en cours de jeu — réglage relu à chaque image par les moteurs
3D, ciseau reposé, et fenêtre élargie à hauteur constante par le chemin de la
touche de plein écran. Lanceur d'essai séparé `FV2 - Menu DISPLAY.cmd`, écrit
distinct de `FV2 - Menu console.cmd` parce que le menu de pause était travaillé
en parallèle. **Défaut trouvé au passage, et corrigé** : `ResizeGLScreen`
n'appelait jamais `SDL_SetWindowSize` — invisible tant que seule la touche de
plein écran l'appelait, puisque SDL redimensionne alors la surface lui-même.
Détail en §13 bis de `MenuConsole.md`.

**Le 2026-08-16** : le menu de pause est complet — `TITLE SCREEN` et
`CHANGE YOUR VIPER` terminent le match hors écran en deux secondes, par trois
adresses trouvées au différentiel de dumps et vérifiées par écriture
(`0x581455` manches, `0x581406` chrono de manche, `0x58FD56` durée d'écran).
`SOUNDS` retient ses réglages. La manette du joueur 2 restait morte après
l'écran de décor — corrigé.

**Le jeu nomme ses propres états, et c'est capital.** Table contiguë de 80 noms
à `0x24494`, laissée par Sega. Deux octets — `MODE_MAIN`, `MODE_SUB` — et
`-menu-mode-log`, avec `FV2 - Relever les etats.cmd` qui écrit dans
`Analysis\modes.txt`. **Avant de mesurer une durée, chercher si le jeu a un nom
pour ce qu'on attend** : le replay s'appelle `REPLAY_DSP`, et cinq valeurs fixes
ont été essayées pour l'attendre au chronomètre.

**Mesuré sur deux relevés (§6 quater)** : `MODE_SUB` n'a de sens que pour
`GAME`, `SEL` et `ADV` — tous les autres modes laissent l'octet tel quel. `GAME`
est confirmé, ses vingt sous-états. **Trois découpages par les noms ont été pris
en défaut : une table contiguë ne dit pas où ses tranches commencent.**

**La tranche d'`ADV` est 50-61, pas 52-61** — mesuré à l'écran le 2026-08-16 avec
`-menu-title-freeze=N`, qui fige le jeu au sous-état demandé
(`FV2 - Essai ecran titre.cmd`). Sous-état 3 = le logo SEGA, sous-état 5 =
l'écran titre. `DONT_RECYCLE_INT/DSP` sont les deux premiers sous-états d'`ADV`,
pas une paire à part. **Et la correction d'avant avait le bon compte avec le
mauvais raisonnement** : douze était juste, mais les deux noms manquants étaient
avant la tranche et non après, donc rien de ce qui suit ne glisse et `ending_*`
garde 62-68. Une mesure juste peut porter une explication fausse, et
l'explication va plus loin que la mesure.

**Le gel coupe la voix de l'annonceur** : à 20 images on entend « Fighting
Vipers » sans le « 2 ». La carte son ne finit pas ce que le processeur ne demande
plus. 60 images laissent passer fondu et annonce ; 300 est déjà trop tard,
l'écran titre est passé.

**Le plan du §6 quinquies est écrit et compilé, étapes 0 à 3, le 2026-08-16 —
pas encore vu à l'écran.** Sept lecteurs de `entry1`, deux remplacés :

1. `OnWarningScreen` lit `WARNING_INT/DSP` au lieu d'une coïncidence entre deux
   valeurs. La laisse, l'abandon de 600 images et l'option
   `-menu-warning-frames` sont partis avec ;
2. `HoldVersus` gèle sur la dernière image du combat, reconnue par
   `MatchIsOver` = `NEXT_PROG_SEL` **et** `MODE_REQUEST` sorti de `GAME`.
   `VSEND_WINNER_FRAMES` n'existe plus ; `Alt+K` ne mesure plus rien.

**Deux faits mesurés le 2026-08-16 (`Analysis\versus_fin.txt`), qui ont coûté un
premier essai raté :**

- **`NEXT_PROG_SEL` arrive à la fin de chaque manche**, pas seulement du match.
  Ce qui les sépare est `MODE_REQUEST` : `req 07` = encore une manche, `req 12`
  (OVER_INT) = le match est fini. Et comme le répartiteur recopie la demande
  dans le mode avant de sauter, le voir depuis `GAME_DSP` désigne exactement la
  dernière image du combat ;
- **en Versus, `entry1` ne retombe pas à zéro au coup décisif** — il tombe après
  le GAME OVER, 451 images plus tard. C'est pourquoi aucune valeur de
  chronomètre ne pouvait convenir : le départ était mal placé, pas la durée.

**`entry1` ne se comporte pas pareil selon le mode, et c'est mesuré des deux
côtés.** En `ARCADE` perdu il tombe exactement à `JUDGE` (707 images avant
`NEXT_PROG_SEL`) ; en Versus, après le GAME OVER. Le §6 bis et le §6 ter avaient
donc raison tous les deux. Hypothèse non éprouvée : c'est la partie *du joueur*
qui s'arrête, et en Versus rien ne perd — une partie `ARCADE` gagnée le dirait.
Le journal de modes imprime maintenant une ligne `[entry1]` à chaque bascule
zéro / non-zéro ; sa valeur reste hors journal (état de tâche, §11).

**« Se détacher de `entry1` » n'était pas le bon objectif ; le bon est que
chaque lecteur pose sa question au byte qui y répond.**

**`entry1` ne commande plus rien, depuis le 2026-08-16.** Les sept lecteurs sont
passés aux modes, à la demande de Frédéric répétée trois fois. Seule lecture
restante : la ligne `[entry1]` du journal de modes, active uniquement avec
`-menu-mode-log`. Cinq des sept tombent au même instant qu'avant, à quelques
images près ; `OnWarningScreen` et `HoldVersus` sont les deux qui ont vraiment
changé.

**Start pendant l'écran de sélection : mis en quarantaine, à corriger.** Le menu
ne s'y ouvre plus du tout, et Start est rendu au jeu (c'est par lui que le joueur
2 rejoint). `InSelect` est testé dans `StartPressed` **et** dans la garde des
lignes de mode, parce que F2 ouvre encore le menu à la main. Ce qu'il faudrait y
faire est un choix non tranché — rien, `OPTIONS` seul, ou le menu des modes
complet ; la troisième demanderait de minuter une injection de Start dans un
écran de sélection déjà ouvert, jamais essayée. Détail au §10 de
`MenuConsole.md`.

**Réserve de Frédéric sur les cinq lecteurs restants — la mesure a tranché la
moitié.** Les **3 et 6 sont clos par la mesure** : `entry1` tombe 707 images
avant `NEXT_PROG_SEL`, donc bien au plus tôt, ce qu'ils veulent. Les **1, 2 et 5
ont leur défaut établi** : `entry1` dit « une partie tourne » dès l'apparition de
l'écran de sélection, 163 images avant `GAME_INT` en `ARCADE` mais **1498 images
en Versus**. Les 1 et 2 n'attendent qu'un choix de Frédéric (que doit faire Start
pendant la sélection ?). Le 5 a en plus un inconnu : **on ne sait pas quand le
jeu lit `SURVIVAL_FLAG`**, donc l'armer plus tard, à `GAME_INT`, pourrait arriver
après la lecture et faire disparaître `SURVIVAL MODE`.

**Inachevé au §6 ter** : les lignes `REMATCH` et `CHANGE STAGE` de l'écran de fin
de Versus, qui demandent de traverser l'écran de sélection tout seul. **Ne pas
repartir chercher une valeur de chronomètre.**

**Les saccades venaient du journal, pas des lectures.** `FV2 - Menu console.cmd`
passait `-menu-state-log` : une écriture console avec vidage de tampon chaque
seconde, dans la boucle de jeu. Retirée du lanceur le 2026-08-16, les images qui
sautaient pendant les combats ont disparu **et la navigation dans les menus est
devenue plus fluide**. Un instrument de mesure ne se laisse pas dans le lanceur
de tous les jours. Voir [[feedback_ne_pas_suggerer_arret]].

**Le menu des modes est posé sur le VRAI écran titre du jeu**, gelé dessus, au
lieu de recouvrir l'écran d'une illustration à nous pendant que la démo tourne.
Option `-menu-title-screen`, dans `FV2 - Menu console.cmd`. Le §6 sexies de
`MenuConsole.md` fait foi.

**Mesure neuve** : le répartiteur d'`ADV` lit `SUBMODE_REQUEST`, comme ceux de
`SEL` et de `GAME` — on le supposait seulement. Écrire `MODE_REQUEST = ADV_DSP`
et `SUBMODE_REQUEST = FV2_TITLE_INT` amène l'écran titre en **2 images**, contre
119 par le séquenceur d'attraction. Écrit une fois, jamais tenu.

**Deux pièges de ce chantier, tous deux payés à l'écran** : tout le tracé des
libellés peints vit dans la branche `STYLE_FULL`, donc basculer sur
`STYLE_PANEL` les fait retomber à la police du menu — le remède est une
soustraction (`SetBackgroundHidden`), pas un style de plus ; et un chemin qui ne
passe pas par `OpenMenu` doit confisquer les boutons lui-même, sinon le Start du
joueur arrive au jeu et ouvre l'écran de sélection.

**Trois règles apprises à la dure :**

1. **Ne jamais toucher au compteur de crédits.** Le jeu prend le sien sur un
   vrai Start — c'est ce qui fait marcher le freeplay sans son octet.
2. **Rendre les boutons un par un, au relâchement**, sinon le `Q` qui valide
   arrive au jeu à l'image suivante.
3. **Un doute a un sens.** La cohérence scène/pointeur ne doit pas commander
   `InAttract` : « je ne sais pas » devenait « une partie est en cours ».

**Trois points fermés par la mesure, à ne pas rouvrir** : ouvrir l'écran de
sélection par les écritures sur `entry1` casse le jeu, y compris depuis la
boucle d'attraction ; fixer le chrono de l'écran de sélection est impossible —
écrit une fois il est écrasé, écrit en boucle le combat ne démarre plus, et tout
son code a été retiré à la demande de Frédéric ; et **le VS DIAGRAM du jeu ne
liste que onze personnages**, donc il ne nommera jamais Del Sol, Kuhn ni B.M.
Notre tableau en montre quatorze : c'est un sur-ensemble, à ne pas « corriger ».

**Reste** : `ECRAN TITRE` et `SELECTION` du menu de pause, la boucle du Versus
(`-versus-loop`, éteinte), le remplacement des musiques qui n'a jamais produit
un son, et les blocs 12 et 15 sans personnage attribué.

Outil : `fv2mod\vs_blocs.py` lit le tableau du VS DIAGRAM **directement dans la
NVRAM**, sans lancer le jeu ni recompiler. Il remplace la sonde `PROBE` qui
vivait dans le menu.

**La séquence de fin, ouverte le 2026-08-19.** Tout est au **§6 septies de
`MenuConsole.md`**, qui fait foi. En résumé : on y va par `-goto-ending` ou
`Alt+L` (`MODE_REQUEST = 12`, écrit une fois) ; elle contient **huit rejeux de
451 images puis un écran final**, et chaque segment est en **deux moitiés** —
page de texte du générique, puis rejeu. Deux adresses trouvées par diff d'images
RAM : `ENDING_SEQ_PTR = 0x00580E8D` (le segment) et
`ENDING_REPLAY_ON = 0x0070E603` (la moitié). Les artworks de Frédéric couvrent
les rejeux seuls, par `-ending-art=<dossier>` ; les pages de texte restent au jeu
sur le fond aux couleurs inversées.

**Deux leçons de ce chantier**, valables ailleurs : un signal peut être **juste
dans le contexte où on l'a mesuré et muet dans celui où on veut s'en servir**
(l'index de scène ne bouge pas quand le ending est demandé à froid) ; et **un
menu se place dans le cadre du jeu, mais une image qui remplace un écran couvre
la fenêtre** — en `-wide-screen` les deux diffèrent.

**Coût mesuré à connaître** : à `-tilegen-scale=4 -tilegen-width=682` le jeu
tombe à **49,5 im/s**, la séquence s'étire et la musique finit avant les images.
À l'échelle 2, 60 im/s. Ce n'est pas dû aux artworks.

Voir [[project_fv2_mod]], [[project_tuiles_hd]], [[reference_supermodel_binaire]]
et [[feedback_lanceurs_cmd]].
