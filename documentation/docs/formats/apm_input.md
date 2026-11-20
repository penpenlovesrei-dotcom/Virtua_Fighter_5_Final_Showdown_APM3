# L'interface d'entrée d'`apm.dll` — et comment le stub tient la manette

Établi le 2026-09-02, sur `apm.reelle.dll` du dump `APM3_US` (la vraie bibliothèque de la
carte ALLS/APM3) et sur `vfes.exe` du même dump. Vérifié à l'écran sur le jeu en marche.

---

## 1. La signature

```c
char Input_isOn(int code);      /* le bouton est-il tenu ?            */
char Input_isOnNow(int code);   /* vient-il d'etre presse ?           */
```

**Un seul argument, le code du bouton.** `vfes.exe` n'appelle pas ces fonctions
directement : il expose une interface dont les méthodes sont des troncs, en `.text`, qui
jettent le `this` et transmettent le second argument :

```
0x140002BE0   mov ecx, edx
0x140002BE2   jmp qword ptr [0x140133580]      ; Input_isOn
0x140002BF0   mov ecx, edx
0x140002BF2   jmp qword ptr [0x140133578]      ; Input_isOnNow
```

Ces deux troncs figurent dans une table de pointeurs en `0x1401AF858`… : c'est le **moteur**
(`vf5fs-pxd-w64-Retail_APM3.dll`) qui les appelle, à travers cette table. C'est pourquoi une
recherche d'appels directs dans `vfes.exe` ne rend **rien** : il n'y en a aucun.

Conséquence pratique pour le stub : les exports doivent avoir la signature ci-dessus, avec le
code en **premier** argument. Confiance : **CONFIRMED**.

---

## 2. Les codes

`Input_isOn` de la vraie `apm.dll` (`0x180013B50`) traite trois cas :

| Code | Traitement |
|---|---|
| `0` | cas particulier : rendu faux quand `0x180012900()` est vrai |
| `2` à `14` | converti en **bit** par `0x180013510`, testé contre un masque matériel unique |
| `15` | cas particulier : rendu faux quand `0x1800128F0()` est vrai |

La conversion code → bit, lue dans la table de sauts de `0x180013510` :

| code | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bit | 0 | 1 | 2 | 3 | **aucun** | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |

Le **code 6 n'a pas de bit** : la vraie `apm.dll` rend toujours faux pour lui.

Il n'y a **pas d'indice de joueur** dans l'appel, et le masque testé est un seul mot global.

---

## 3. Ce que le jeu interroge

Relevé par le stub, sur 25 secondes à l'écran-titre (chaque appel journalisé avec son code) :

```
7066 x Input_isOnNow(0)   7066 x Input_isOnNow(7)   7066 x Input_isOnNow(8)
7062 x Input_isOnNow(15)
7065 x Input_isOn(2) (3) (4) (5) (6) (7) (8) (9) (10) (11) (12) (13) (14)
```

`Input_isOn` est interrogé pour **les treize codes 2 à 14**, un appel chacun par trame ;
`Input_isOnNow` seulement pour **0, 7, 8 et 15**. Confiance : **CONFIRMED**.

---

## 4. Le sens des codes

| Code | Sens | Confiance |
|---|---|---|
| **7** | **START** | **CONFIRMED** — à l'écran-titre il ouvre la sélection de personnage ; à la sélection il valide et lance le combat. Deux appuis suffisent à mener le jeu d'un démarrage à froid jusqu'à `ROUND 1`. |
| **0** | **TEST** (le bouton opérateur) | **CONFIRMED** — dans le menu opérateur il valide l'entrée pointée ; appuyé sur `EXIT`, le jeu quitte le mode test |
| **1** | **SERVICE** | **CONFIRMED** — il déplace le curseur du menu opérateur. Le jeu ne l'interroge **que** dans ce menu : `Input_isOnNow(1)` n'apparaît nulle part ailleurs |
| 8, 15 | interrogés en front, non identifiés | UNKNOWN |
| **2, 3, 4, 5** | **les quatre directions**, dans un ordre non encore attribué | LIKELY — quatre bits contigus (`0x1000` à `0x8000`) avec auto-répétition, voir §4 bis |
| 6, 9 à 14 | huit bits bas du masque d'interface, sens non établi | UNKNOWN |

Un balayage des codes 2, 3, 4, 5, 8, 9, 10 pendant un combat n'a **rien établi** : l'adversaire
géré par la machine agit en même temps, et une capture ne permet pas d'attribuer un mouvement
au bouton plutôt qu'à lui.

### Le menu opérateur, et l'auto-répétition

`Sequence_isTest` rendu vrai (directive `test = 1` du scénario) fait démarrer le jeu dans
`GAME TEST MODE`, dont le pied de page dit : « SELECT WITH SERVICE BUTTON AND PRESS TEST
BUTTON ». Le relevé du stub montre qu'en mode test le jeu interroge `Input_isOnNow` pour
**0, 1, 7 et 8** — le code **1 n'apparaît nulle part ailleurs**. Les deux codes se sont
laissés attribuer à l'écran (voir ci-dessus).

**Piège** : les menus appliquent une **auto-répétition**. Un appui de 350 ms balaie les six
lignes et ramène le curseur à son point de départ — on croit que rien n'a bougé. Mesure :
80 ms ⇒ trois lignes, 40 ms ⇒ deux, **20 ms ⇒ une seule**. C'est pourquoi le stub relit
désormais son scénario toutes les **30 ms** et non 250 : à 250 ms aucune impulsion assez
brève n'était possible. `tools/menu_test.py` navigue en lisant la position du chevron dans une
capture, plutôt qu'en comptant les pas.

L'**écran de test d'entrées**, lui, est hors d'atteinte : `SUB SYSTEM TEST MODE` rend la main
au menu *système* de la borne, servi par la vraie `apm.dll` via `Core_execute`. Le menu du jeu
n'en a pas. Voir `analysis/machine_etats.md`.

### Où le moteur range nos appuis

Le pistage de la liste 2 a livré la réponse par un autre bout. Les gestionnaires 20 à 24 et 51
consultent quatre champs du `ROB`, dont les valeurs relevées à l'exécution
(`tools/oracle_liste2_vivant.py --champs`) se lisent seules :

| champ | valeurs observées | lecture |
|---|---|---|
| `ROB+0x508` | `0`, `1`, `0x15`, `0x40001`, `0x80001`, `0x2080003` | **masque d'entrée courant**, il suit nos appuis |
| `ROB+0x510` | `0`, `1`, `0x40001`, `0x80003` | **masque d'entrée tamponné** |
| `ROB+0x90C` | `15.0` à `19.0`, en flottants | **trames restantes du tampon** |
| `ROB+0x91C` | `0` ou `1` | **tampon actif** |

C'est un **tampon d'entrée** de jeu de combat : une commande arrivée un peu tôt reste valable
quelques trames. Confiance : **SUPPORTED**.

### Les treize codes, et le bit que chacun allume

La mesure en mémoire est bruitée : l'adversaire géré par la machine agit dans le même combat.
La réponse propre est **statique**. `vfes.exe` publie son interface d'entrée dans une table de
troncs dont la base est `0x1401AF710` ; `Input_isOn` y occupe la case **`+0x158`** et
`Input_isOnNow` la case **`+0x160`**. Il suffit alors de chercher, dans le moteur, les
`call qword ptr [rax + 0x158]`.

Il y en a 48, répartis sur 22 fonctions. Une seule les concentre : **`0x180243ED0`**, treize
appels, un par code — et chaque réponse allume un bit précis d'un masque :

| code | bit | code | bit |
|---:|---:|---:|---:|
| 7 | `0x0001` | 10 | `0x0080` |
| 8 | `0x0002` | 6 | `0x0200` |
| 12 | `0x0004` | **2** | **`0x1000`** |
| 11 | `0x0008` | **5** | **`0x2000`** |
| 13 | `0x0010` | **3** | **`0x4000`** |
| 14 | `0x0020` | **4** | **`0x8000`** |
| 9 | `0x0040` | | |

Deux choses se lisent dans cette table. D'abord **les quatre codes 2, 3, 4 et 5 occupent
quatre bits contigus en haut du masque** — et la queue de la fonction leur applique une
**auto-répétition** (délai en `[rsi+0xac]`, période en `[rsi+0xad]`, division euclidienne à
l'appui) : c'est la signature d'une **navigation de menu**, donc de quatre **directions**.
Ensuite, la fonction ne sert **que le joueur 0** : `test ebp, ebp ; jne` saute tout le bloc
pour les autres. `0x180243ED0` est le lecteur d'entrées **de l'interface**, pas celui du
combattant — lequel passe par `ROB+0x508`.

Confiance : **CONFIRMED** pour la table code → bit ; **LIKELY** pour « les quatre bits hauts
sont les directions », qui repose sur l'auto-répétition et sur leur contiguïté, pas sur une
observation directe.

Ce qui manque encore est l'attribution nominale — lequel des quatre est *haut* — et le sens
des huit bits bas.

### La mesure en mémoire n'a pas convergé, et il faut le dire

`tools/carte_entrees.py` tient chaque code seul, en combat, et compare `ROB+0x508` et
`ROB+0x510` au repos et sous appui, sur **deux combattants** (on ne sait pas d'avance lequel
est le joueur) et sur **quatre passes** (l'adversaire géré par la machine bouge en même
temps). Sur les 48 mesures d'une passe complète, **une seule s'est répétée** :
`code 13 → ROB+0x508 ^ 0x15` sur le second combattant. Tout le reste est du bruit.

La conclusion honnête est que **le masque du combattant ne se laisse pas cartographier ainsi**
tant qu'un adversaire actif partage la scène : il ne suffit pas de répéter, il faudrait un
combat où seul le joueur agit. Le résultat statique ci-dessus, lui, ne dépend d'aucune
condition de course.

**Ce combat existe** : le mode entraînement, atteint en déviant la machine à états
(`analysis/machine_etats.md`). Le partenaire ne bouge pas. `tools/carte_entrees.py --dojo`
pose la déviation lui-même.

La passe en mode entraînement confirme d'abord une chose : **le second `ROB` ne change
jamais**, alors qu'en combat les deux bougeaient. Le partenaire est bien inerte. Mais la carte
code → bit ne se dégage toujours pas : les valeurs qui se répètent sont `0x00080003`,
`0x00080001` et `0x00000002`, c'est-à-dire un bit haut (`0x80000`) accompagné d'un petit
nombre dans le quartet bas. **`ROB+0x508` n'est donc pas un champ de bits « un bouton, un
bit »** : c'est un **mot de commande composite** — vraisemblablement une direction codée dans
le quartet bas et des drapeaux au-dessus. Confiance : **LIKELY**. Le décoder demande de lire
son producteur (`0x1801382AB` et voisins), pas de le mesurer bouton par bouton.

---

## 5. Le scénario d'entrées du stub

`tools/gen_apm_stub.py` génère un `apm.dll` dont `Input_isOn` et `Input_isOnNow` jouent un
scénario lu dans **`apm_entrees.txt`**, placé à côté de la DLL. Le fichier est relu dès que sa
date change (contrôle toutes les 250 ms) : **on modifie une séquence pendant que le jeu
tourne, sans recompiler ni relancer**.

```
nom start = 7          nomme un code
front   = 150          duree (ms) pendant laquelle isOnNow reste vrai apres un appui
journal = 0            0 coupe TOUT le journal du stub

0       rien           a partir de t=0 ms, rien de tenu
25000   start          a 25 s, START tenu
25300   rien
```

Les instants comptent à partir du **premier appel d'entrée**, c'est-à-dire du démarrage du
moteur. `journal = 1` fait annoncer chaque appel par `OutputDebugStringA` : très instructif,
mais sous débogueur ces 900 messages par seconde font tomber le jeu de 60 à 25 images par
seconde. Le mettre à `0` dès qu'on ne compte plus les appels.

Outils :

| Lanceur | Ce qu'il fait |
|---|---|
| `tools/lancer_vfes_combat.cmd` | lance le jeu, le laisse aller seul jusqu'au combat, capture l'écran |
| `tools/presser.cmd <codes>` | appuie sur des boutons dans le jeu déjà lancé, et capture |
| `tools/capture_fenetre.py` | capture la fenêtre du jeu en PNG |

---

## Les codes nommes

Trois codes etaient etablis depuis le menu operateur, trois autres l'ont ete le
2026-09-03 **en jouant** : le stub lit desormais le clavier et la manette, ce qui
rend chaque code essayable a la main.

| code | nom | comment il a ete etabli |
|---:|---|---|
| **0** | `TEST` | menu operateur : valide, et quitte sur `EXIT` |
| **1** | `SERVICE` | menu operateur : deplace le curseur |
| **7** | `START` | scenario : fait passer les ecrans |
| **8** | **`KICK`** | joue au clavier |
| **11** | **`GUARD`** | joue au clavier |
| **12** | **`PUNCH`** | joue au clavier |

Restent **inconnus** : `6`, `9`, `10`, `13`, `14`. Et les codes **2 a 5**, tenus
pour les quatre directions, ne sont qu'une **disposition de travail** : ils n'ont
jamais ete identifies un par un.

### Ce que la numerotation suggere, et pourquoi c'est a verifier

`P K G` ne tombe pas sur trois codes consecutifs : **12, 8, 11**. Deux lectures
possibles, et rien ne les departage encore :

- l'ordre du connecteur de la borne n'est pas l'ordre logique du jeu, et les
  codes sont simplement disperses ;
- **ou** le bloc `8..14` melange deux joueurs, auquel cas certains des inconnus
  (`9`, `10`, `13`, `14`) seraient les memes trois boutons pour le joueur 2 --
  et resteraient donc muets sur un poste unique.

La seconde hypothese se teste en une minute : si `9`, `10`, `13` et `14` ne font
**rien** alors que `8`, `11` et `12` agissent, c'est qu'ils appartiennent a
l'autre joueur.

### Pourquoi cela debloque les mesures

Le masque d'entrees du combattant est en `ROB+0x508` (voir
`analysis/liste2_repartiteur.md`). Jusqu'ici on savait le lire sans savoir ce
qu'il signifiait, faute de connaitre un seul bouton. Avec trois codes nommes,
`tools/carte_entrees.py` devient interpretable : on tient un bouton **connu** et
on regarde quel bit s'allume. C'est le verrou qui restait ouvert sur les neuf
groupes du selecteur de fenetres temporelles.

---

## La cadence reelle, lue dans `apm.reelle.dll`

Question du 2026-09-03 : a quelle frequence la vraie bibliotheque lit-elle la
manette ? Reponse mesuree dans le binaire, pas tiree de l'usage du metier.

### Un seul echantillonnage, dans `Core_execute`

La fonction **`0x180013EF0`** est la mise a jour des entrees. Elle n'a
**qu'un seul appelant** dans toute la bibliotheque : **`Core_execute+0xFB`**
(`0x180011E7B`). `Core_execute` est le battement de la carte, appele une fois par
trame par le jeu.

```
0x180013EF0  cmp  byte [0x18012B300], 0     ; manette activee ?
0x180013EFD  call apmGamepadIsXInputDevice
0x180013F02  call ...
0x180013F0B  lea  rcx, [0x18012B2F0]        ; &masque courant
0x180013F12  call apmGamepadGetApmInput     ; UNE lecture du materiel
0x180013F1B  eax = [0x18012B2EC]            ; precedent
0x180013F23  ecx = [0x18012B2F0]            ; courant
0x180013F2B  [0x18012B2F4] = eax ^ ecx      ; ce qui a change
0x180013F35  [0x18012B2EC] = ecx            ; le courant devient le precedent
0x180013F3D  [0x18012B2F8] = ~eax & ecx     ; fronts MONTANTS
0x180013F49  [0x18012B2FC] = ~ecx & eax     ; fronts DESCENDANTS
```

Cinq globaux, et le calcul de fronts classique :

| adresse | contenu |
|---|---|
| `0x18012B2EC` | masque precedent |
| `0x18012B2F0` | **masque courant** -- ce que lit `Input_isOn` |
| `0x18012B2F4` | ce qui a change |
| `0x18012B2F8` | **fronts montants** -- ce que lit `Input_isOnNow` |
| `0x18012B2FC` | fronts descendants -- `Input_isOffNow` |

`Input_isOn` et `Input_isOnNow` ne touchent donc **jamais** au materiel : elles
testent un bit dans un instantane pris une fois par trame.

Confiance : **CONFIRMED**.

### Le bit de chaque code

`0x180013510` traduit un code en bit, par table de sauts (`add ecx,-2 ;
cmp ecx,0xC ; ja`) : seuls les **codes 2 a 14** existent cote manette.

| code | bit | | code | bit |
|---:|---|---|---:|---|
| 2 | `0x001` | | 9 | `0x040` |
| 3 | `0x002` | | 10 | `0x080` |
| 4 | `0x004` | | 11 | `0x100` — **GUARD** |
| 5 | `0x008` | | 12 | `0x200` — **PUNCH** |
| **6** | **aucun (0)** | | 13 | `0x400` |
| 7 | `0x010` | | 14 | `0x800` |
| 8 | `0x020` — **KICK** | | | |

**Le code 6 n'a pas de bit** : ce n'est pas une entree de manette. C'est la
piece, qui passe par le chemin des credits.

Douze bits, donc, pour un joueur. Le second joueur ne passe pas par la : c'est
l'autre branche de `Input_isOn`, celle qui bâtit une structure de 0x38 octets et
interroge un conteneur (`0x18001F7D0`, `0x18001F810`) -- le chemin JVS de la
vraie borne.

### Ce que le jeu en fait, mesure a l'execution

Trente secondes de jeu, journal du stub actif :

| appel | total | par `Core_execute` |
|---|---:|---:|
| `Core_execute` | 1142 | 1 |
| `Input_isOn` | 14807 | **13** |
| `Input_isOnNow` | 4556 | **4** |

**Treize** : exactement le nombre de codes de la table (2 a 14). Le jeu interroge
donc **tous les codes, une fois par trame**, sur l'instantane unique.

### Consequence pour notre stub

Notre stub lit le materiel dans `Input_isOn` -- donc dix-sept fois par trame,
d'ou le cache de 4 ms qu'il a fallu ajouter. **Ce n'est pas la ou il faut lire.**
La place juste est `Core_execute`, appele une fois par trame : un echantillonnage,
zero cache, et le calcul de fronts vient gratuitement.

Cela corrigerait aussi une imprecision mesurable : notre `Input_isOnNow` rend
vrai pendant `g_front` = 34 ms, soit **deux trames**, la ou l'original ne le rend
vrai que sur **la trame du front**. Un coup declenche sur `isOnNow` peut donc
sortir deux fois chez nous.

### Le stub corrige (2026-09-03) -- a moitie

**Ce qui a ete garde.** `Core_execute` est desormais ecrite a la main dans le
stub, et c'est le seul endroit ou les entrees sont echantillonnees : une lecture
du materiel par battement au lieu de dix-sept. Le cache de 4 ms devient inutile
et a disparu.

**Ce qui a echoue.** Copier le vrai front d'une trame a CASSE le jeu : il n'a
plus jamais quitte `APM3_ENTRY` -- l'ecran noir signale par Frederic.

La mesure est pourtant sans ambiguite :

```
[apm] entrees: pas 1 a t=25000 ms, masque=0x00000080
[apm] fronts: courant=0x00000080 montants=0x00000080 descendants=0x00000000
...
[apm] Input_isOnNow(7)            <- appele juste apres, sans Core_execute entre
```

Le front **est** calcule (deux fois, pour les deux START du scenario),
`Input_isOnNow(7)` **est** appele 2660 fois -- et il ne rend **jamais** vrai.
Consommer le bit a la lecture n'a rien change non plus.

La cause n'est pas etablie. L'hypothese la plus plausible est une affaire de
**fils d'execution** : le jeu interrogerait les entrees ailleurs que la ou il
appelle `Core_execute`, et un front qui ne vit qu'une trame passerait entre les
deux -- l'ordre des lignes de journal, qui viennent de fils differents, ne
prouve rien. La vraie `apm.dll` n'a pas ce probleme parce qu'elle est appelee
depuis la carte, pas depuis notre bouchon.

**Ce qui est en place.** `Input_isOnNow` retrouve sa **fenetre de temps** de
`g_front` = 34 ms, qui marche. C'est deux trames au lieu d'une : l'ecart avec
l'original est connu, mesure et assume, pas oublie. Un coup declenche sur
`isOnNow` peut donc encore sortir deux fois -- si cela se voit en jouant, c'est
ici qu'il faudra revenir, avec un vrai relevé des fils.

Verification apres correction : le parcours complet est retrouve.

```
1  etat [STARTUP] -> [APM3]   sous-etat [CS_TITLE]      -> [MAX]
2  etat [APM3]    -> [MAX]    sous-etat [APM3_ENTRY]    -> [APM3_SELECTOR]
3  etat [APM3]    -> [MAX]    sous-etat [APM3_SELECTOR] -> [APM3_GAME_VS]
```
