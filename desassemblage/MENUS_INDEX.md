# MENUS_INDEX.md — les fonctions de menu, nommées, des deux côtés

Établi le **19 novembre 2026**, à la demande de Frédéric : « on modifie
fortement les menus du jeu, il faut décompiler et nommer les fonctions liées
aux menus ».

**Aucun jeu n'a été lancé. Aucun binaire n'a été patché. Ghidra n'a pas été
touché** (des verrous du 16 novembre traînent dans `VF5RE/ghidra/`). Tout ce
qui est nouveau ici est lu dans le **fichier** des deux modules par
`pefile` + `capstone`, bornes prises dans `.pdata`, noms de classe pris dans
le **RTTI MSVC**.

---

## 0. LE PIÈGE D'ADRESSES, À LIRE AVANT TOUT

Les deux modules ont la **même base d'image `0x180000000`** et des
**adresses différentes**. Une adresse de la colonne APM3 ne désigne **rien**
dans REVO, et réciproquement.

| | fichier | taille | md5 (12) |
|---|---|---:|---|
| **APM3** | `vf5fs-pxd-w64-Retail_APM3.dll` (`FS APM3/banc/`) | 6 965 248 o | `3214e19696de` |
| **REVO** | `vf5fs-pxd-w64-d3d12_SteamRetail.dll` (`FS REVO/`) | 7 229 952 o | `64fea1ce4db6` |

Les deux portent le même chemin de compilation
`vf5fscs_source/20120711_update_1.1` : **c'est le même source**, recompilé
deux fois. C'est ce qui rend la transposition possible — et c'est aussi ce
qui rend la confusion d'adresses facile.

Troisième binaire, à ne pas mélanger : `VFREVO.exe`, base **`0x140000000`**,
décompilé dans `VF5RE/code_decompile_vfrevo/` (444 fichiers). C'est l'hôte,
pas le moteur ; il ne contient aucune fonction de menu.

**Le numéro de créneau de vtable ne se transpose pas non plus.** Mesuré :
la vtable de `TaskMenuMain` a **onze** créneaux chez APM3 et **douze** chez
REVO — REVO en a inséré un en position 7. C'est la **taille** des fonctions
qui apparie la fin de la table (37 o / 16 o / 77 o des deux côtés), pas son
rang.

---

## 1. LE BILAN, EN COMPTES

### 1.1 Ce que le RTTI nomme, et c'est la découverte de cette séance

| | APM3 | REVO |
|---|---:|---:|
| vtables nommées par le RTTI, tout le module | **534** | **637** |
| dont **classes de menu** (`*Menu*`, `*Option*`, `*Selector*`, `*Pause*`, `*Cursor*`) | **54** | **54** |
| dont communes aux deux modules | **46** | **46** |
| propres à un seul module | 8 (`apm3TestMode::Menu*`) | 8 (voir §5.3) |
| **méthodes virtuelles distinctes** visées par ces vtables | **309** | **322** |
| dont bouchons / feuilles sans `.pdata` | 24 | 27 |
| **vraies fonctions** | 285 | **295** |
| **…avec un `.c` décompilé** | 4 | **22 (7 %)** |

**Le chiffre qui tranche : 22 sur 295.** Les 54 classes de menu de REVO ont
295 méthodes virtuelles réelles, et **sept pour cent** sont décompilées —
alors que `code_decompile/` compte 3 568 fichiers. Les notes ont travaillé
`TaskMenuMain` et les pages du menu principal ; les 53 autres classes sont
intactes. Côté APM3, c'est **4 sur 285**.

Mesuré le 19 novembre par `VF5RE/tools/rtti.py` sur les deux PE, et par
`.pdata` pour les bornes. Le relevé complet, classe par classe et créneau
par créneau, est dans **`menus/VTABLES_MENUS_APM3_VS_REVO.txt`** (729
lignes) — c'est le fichier à ouvrir en premier pour nommer une fonction de
menu.

### 1.2 Ce que les notes nomment, côté REVO

`VF5RE/code_decompile/MENU.md` fait **1 906 382 octets** et **40 711
lignes** ; sa partie **menu** (lignes 1 à 3 600, sections 1 à 16 puis
419.73 à 419.107) est la source. Après, le fichier passe à l'arc du rendu.

| | compte |
|---|---:|
| adresses `FUN_180…` distinctes citées dans la partie menu | **194** |
| …avec un `.c` dans `VF5RE/code_decompile` | **180** |
| …dont sous un **nom humain** et non `FUN_` | 7 |
| …sans aucun `.c` | **14** |
| parmi ces 14, **désassemblées aujourd'hui** dans `menus/revo_asm/` | **3** |
| handlers de sous-état de menu désassemblés en plus | 6 |

Les 7 noms humains du menu, côté REVO : `Entree_PortEstInscrit.c`
(`0x1800B1B10`), `LireObjetEntree.c` (`0x1800B21E0`), `InscrireJoueur.c`
(`0x1800B2F30`), `RemplirDescripteurMatch.c` (`0x1801AA1D0`),
`Match_PoserSorteEtVider.c` (`0x1801AABE0`), `DemanderPartie.c`
(`0x1801AAC20`), `Entree_QuelSlotAValide.c` (`0x1801B2980`).

### 1.3 Ce que les notes nomment, côté APM3

Onze notes portent les menus d'APM3 : `menu_console.md` (126 ko, le plus
gros), `carte_options.md`, `machine_console.md`, `mode_selector.md`,
`mode_de_jeu.md`, `couverture_console.md`, `parente_console.md`,
`machine_etats.md`, `etats_console_essais.md`, `liste2_repartiteur.md`,
`mothead_liste2_roles.md`.

| | compte |
|---|---:|
| adresses `0x180…` citées dans ces onze notes | **1 196** |
| dont hors `.text` (tables, globaux, données) | 172 |
| **fonctions distinctes** visées (résolues par `.pdata`) | **530** |
| adresses qui sont des **sites**, pas des débuts de fonction | **569** |
| fonctions de menu avec un `.c` décompilé | **4** |
| fonctions de menu avec un désassemblage commenté **avant** aujourd'hui | **14** |
| fonctions de menu **désassemblées aujourd'hui** | **35** |

Les deux cartes de zone auto-générées (`carte_menu.md`, 221 fonctions sur
`0x1801D9000`–`0x1801E6000` ; `carte_selecteur.md`, 411 fonctions sur
`0x180160000`–`0x180178000`) ne sont **pas** comptées ici : elles listent des
adresses avec leur taille et leurs appelants, elles ne **nomment** rien.

`couverture_console.md` donnait déjà la mesure du 4 septembre, et elle reste
vraie : sur les 646 fonctions atteintes par le parcours du mode console,
**67 sont nommées au moins une fois (10 %)** et **23 sont travaillées (4 %)**.

### 1.4 Le denominateur Ghidra

Chiffre reçu avec la mission, **non re-mesuré** (je n'ai pas ouvert Ghidra) :
dans la base Ghidra du moteur, **0 fonction sur 13 856 n'a été renommée à la
main** ; les 3 216 noms non-`FUN_` sont des `Unwind@`, des tables de `switch`
et de la libc. **Le savoir sur les menus est dans les `.md` et dans le RTTI,
pas dans Ghidra** — et c'est confirmé par le fait que les 54 classes de menu
se lisent dans le binaire sans Ghidra du tout.

---

## 2. CE QUI EST RAPATRIÉ

`FS APM3/desassemblage/` contenait **36 fichiers**. Aucun n'a été supprimé,
aucun n'a été écrasé. Il porte en plus le dossier `menus/`, **192 fichiers,
4,1 Mio** :

```
FS APM3/desassemblage/
  MENUS_INDEX.md                        <- ce fichier
  menus/
    VTABLES_MENUS_APM3_VS_REVO.txt      les 54 classes de menu, créneau
                                        par créneau, les deux modules en
                                        regard  (le point d'entrée)
    apm3/      37 fichiers   le désassemblage commenté des fonctions de
                             menu d'APM3 : 35 déposées aujourd'hui, plus
                             `apm3_menu_0x1E38ED.asm` et
                             `apm3_pages_sousmenus_0x1E1C51.asm` repris de
                             `VF5RE/desassemblages/`
    revo_asm/  11 fichiers   9 fonctions de menu de REVO qui n'ont AUCUN
                             `.c`, désassemblées aujourd'hui, plus les deux
                             `.asm` de REVO déjà écrits (le chargeur 2D du
                             sélecteur, la garde de l'écran d'attente)
    revo_c/   128 fichiers   le C décompilé des fonctions de menu de REVO,
                             copié de `VF5RE/code_decompile`
    notes/     15 fichiers   les notes, copiées OCTET POUR OCTET
```

**`notes/MENU.md` est identique à l'original** (`md5
d9237493cb042be46be301acf919e469` des deux côtés). Il est en **encodage
mixte** : le grepper avec `grep -a`, et **ne jamais le réécrire**.
`menu_console.md` et `mode_de_jeu.md` portent le suffixe `.VF5RE_20261119`
parce que `FS APM3/analysis/` en a déjà une version plus ancienne (89 ko et
25 ko contre 126 ko et 35 ko) — l'ancienne n'a pas été touchée.

`notes/rtti_apm3.txt` (534 vtables) et `notes/rtti_revo.txt` (637 vtables)
sont les deux relevés RTTI. Le second a été **produit aujourd'hui** ; il
n'existait pas.

**Deux notes ne sont PAS copiées, exprès** :
`FS APM3/analysis/menus_repetition_appui.md` et
`FS APM3/analysis/menu_echappe.md`. Elles sont de Frédéric, écrites
**le 19 novembre à 19:30 et 19:38**, pendant ce relevé, et elles sont déjà
au bon endroit. Je les cite au §3.2 bis et je recoupe trois de leurs
adresses avec le RTTI. Je ne les ai **pas** re-mesurées, et je n'ai touché
à rien de leur chantier (`VF5RE/tools/quest_runtime.c`,
`gen_apm_stub.py`, `poser_menu_echappe.py`, `jouer.cmd`).

---

## 3. LES FONCTIONS D'APM3 — le tableau

Les 35 lignes de §3 et §3.0 sont les fonctions **désassemblées
aujourd'hui** : un fichier `.asm` par ligne dans `menus/apm3/`, avec son
en-tête, ses bornes `.pdata` et la note d'où vient son nom.

**Une faute de méthode, attrapée par un contrôle, et il faut la dire.** Mon
premier dépôt chaînait les entrées `.pdata` **par adjacence** — fin de l'une
= début de la suivante. C'est faux : deux fonctions distinctes se touchent
souvent. `TaskMenuScoreAttack::draw` (`0x1801E17A0`, 880 o) avalait ainsi
`TaskMenuTerminal::draw` (`0x1801E1B10`) et rendait **1 692 o**, et
`MenuMain_EntrerLeSousEtat` rendait 81 o au lieu de 16. Le critère juste est
le **drapeau `UNW_FLAG_CHAININFO` (0x4)** de l'`UNWIND_INFO` : il *dit*
laquelle des deux entrées est une suite. Tous les `.asm` de ce dossier sont
bornés comme ça. Les deux contrôles qui l'ont prouvé : `page_scoreattack`
retombe à 880 o (négatif), et `menu_main_entree` finit sur un `ret`
franc (positif).

| adresse | nom proposé | ce qu'elle fait | d'où vient le nom | côté |
|---|---|---|---|---|
| `0x1800DA550` | `Etat_RepartiteurDesPhases` | LE répartiteur de la machine à états : lit la tête courante en `0x18070C4F0`, appelle l'un des trois gestionnaires du descripteur selon la phase. Tables : modes `0x1803A0190` (10 × 0x68), sous-états `0x1803A05A0` (55 × 0x20) | `analysis/machine_console.md` §1 | APM3 |
| `0x1800DA9A0` | `Etat_DemanderUnMode` | La **seule** porte publique pour demander un mode ; 27 sites d'appel dans tout le module. Pas d'entrée `.pdata` : feuille | `analysis/menu_console.md` §8.5 | APM3 |
| `0x1800DCCA0` | `MenuMain_EntrerLeSousEtat` | Sous-état 36 = `MENU_MAIN`, `fn_entree`. Sa phase 1 est le bouchon `0x180007450` : le sous-état ne finit jamais, c'est l'état de REPOS | `TABLE_DES_SCENES_APM3_VS_REVO.md` §6 ligne 36 | APM3 |
| `0x1800DCBE0` | `MenuMain_SortirDuSousEtat` | Sous-état 36 = `MENU_MAIN`, `fn_sortie` | `TABLE_DES_SCENES_APM3_VS_REVO.md` §6 ligne 36 | APM3 |
| `0x1801E36D0` | `TaskMenuMain::init` | Monte le menu principal : pose `[page+0x224]=9` en `0x1801E39D0` (**dernier indice**, donc DIX entrées 0 à 9), prédicat de grisement en `0x1801E39FA`, et en `0x1801E38ED` la séquence témoin `0x5140C` → `&page+0x29E8` → commande 74 | RTTI : vtable `0x180532AE8` créneau [1] ; `analysis/menu_console.md` §8.3 ; `desassemblages/apm3_menu_0x1E38ED.asm` | APM3 |
| `0x1801E0C80` | `TaskMenuMain::draw` | Le dessin de la page : boucle de 0 au dernier indice **inclus** (`0x1801E1079 cmp edi,[rsi+0x224]` / `jle`), lit l'état de chaque entrée dans `page+0x642+i` (0 normal, 1 grisée, 2 pas dessinée), résout chaque libellé par `0x1801EFD10`, et choisit en `0x1801E0D3D` entre `UNLOCK FULL GAME` et `DOWNLOAD CONTENT` par un `cmove` | RTTI : vtable `0x180532AE8` créneau [4] ; `analysis/menu_console.md` §8.2–8.3 | APM3 |
| `0x1801DDF30` | `TaskMenuMain::validate` | Le répartiteur de validation : première chose qu'il fait, il refuse toute entrée dont l'état `page+0x642+i` n'est pas 0 (`0x1801DDF4C`…`0x1801DDF65`) — **une entrée grisée ou masquée ne fait rien**. Une seule fonction, **15** entrées `.pdata` chaînées jusqu'à `0x1801DE1E3` | RTTI : dernier créneau non bouchonné [10] ; `analysis/menu_console.md` §8.2 | APM3 |
| `0x1801EFD10` | `Texte_ResoudreUnLibelle` | Résout un identifiant de texte dans la table chargée en `0x180753900` (borne `0x5A0C` = 23 052 entrées), qui est `string_array.farc` du `.par`. Jumeau de `FUN_1802316E0` de REVO | `analysis/menu_console.md` §8.1 | APM3 |
| `0x1801AB3A0` | `Option_OuvrirLaPage` | `(mode,type,drapeau)` ouvre l'une de DEUX pages : `type==2 && mode!=0` → page `0x1807513C8` scène `OPTION CONTROL`, sinon page `0x1807513C0` scène `OPTION`. **Huit appelants**, dont le menu console en `0x1801DE0D1` : l'écran d'options est partagé avec la pause et le terminal | `analysis/carte_options.md` §1 | APM3 |
| `0x1801DF100` | `Page_SinglePlayer` | Page fille `SINGLE PLAYER`. En-tête `0x177` gravé en `0x1801DF256`. Libellés `0x19E 0x19F 0x1A0 0x1A1` = Arcade / Score Attack / License Challenge / Special Sparring | `desassemblages/apm3_pages_sousmenus_0x1E1C51.asm` ; `MENU.md` §419.94 | APM3 |
| `0x1801E2190` | `Page_OfflineVersus` | Page fille `OFFLINE VERSUS`. En-tête `0x178` en `0x1801E2307`. Libellés `0x1AD 0x1A9 0x1CB 0x1D0 0x1D5`, **non consécutifs** = Round count / Time limit / Max health bar:1P / :2P / Stage select | `desassemblages/apm3_pages_sousmenus_0x1E1C51.asm` ; `MENU.md` §419.94 | APM3 |
| `0x1801E1E40` | `Page_Dojo` | Page fille `DOJO`. En-tête `0x17B` en `0x1801E1F93`. Libellés `0x217 0x218 0x219` gravés en `0x1801E1E8A` et suivants, **octet pour octet dans la même forme que ceux de REVO** = Tutorial / Command Training / Free Training | `desassemblages/apm3_pages_sousmenus_0x1E1C51.asm` ; `MENU.md` §419.94 | APM3 |
| `0x1801E1B10` | `Page_Terminal` | Page fille `TERMINAL`. En-tête `0x17C` en `0x1801E1C51`. Libellés `0x299 0x29A` = Customize / Replays | `desassemblages/apm3_pages_sousmenus_0x1E1C51.asm` ; `MENU.md` §419.94 | APM3 |
| `0x1801B0120` | `Ranking_OuvrirLaPage` | Destination de l'entrée 5 `SCOREBOARDS` : ouvre la scène `RANKING` | `analysis/menu_console.md` §8.3 ligne 5 | APM3 |
| `0x1800DCA90` | `Selector_EntrerLeSousEtat` | Sous-état **17** = `SELECTOR` (choix des combattants), `fn_entree`. Chez REVO ce sous-état porte le numéro **19** | `TABLE_DES_SCENES_APM3_VS_REVO.md` §6 ligne 17 | APM3 |
| `0x1800DB270` | `Selector_MettreAJour` | Sous-état 17 = `SELECTOR`, `fn_maj`. Son jumeau de REVO, `0x1800E2470`, est l'ancre qui a servi à identifier la table des scènes elle-même | `TABLE_DES_SCENES_APM3_VS_REVO.md` §1 et §6 | APM3 |
| `0x1800DBB70` | `Selector_SortirDuSousEtat` | Sous-état 17 = `SELECTOR`, `fn_sortie`. **Partagé** avec `APM3_SELECTOR` (sous-état 49), qui pointe la même adresse | `TABLE_DES_SCENES_APM3_VS_REVO.md` §6 lignes 17 et 49 | APM3 |
| `0x1800DCA70` | `ModeSelector_EntrerLeSousEtat` | Sous-état 18 = `MODE_SELECTOR`, `fn_entree`. **Ce n'est pas un écran** : un sas de trois gestionnaires, sans page, sans liste, sans libellé, sans curseur, sans lecture d'entrées, qui écrit un seul champ de session | `analysis/mode_selector.md` §1 | APM3 |
| `0x1800DAE20` | `ModeSelector_MettreAJour` | Sous-état 18, `fn_maj` (390 o). Jumeau de `0x1800E2010` de REVO, déjà décompilé sous le nom `SE20_MODE_SELECTOR_Phase1_MontageDuMatch.c` | `analysis/mode_selector.md` ; `TABLE_DES_SCENES…` §6 ligne 18 | APM3 |
| `0x1800DBB50` | `ModeSelector_SortirDuSousEtat` | Sous-état 18, `fn_sortie` (21 o) | `TABLE_DES_SCENES_APM3_VS_REVO.md` §6 ligne 18 | APM3 |
| `0x1801DC270` | `TaskMenuArcadeNormal::update` | Pose le **MODE DE JEU = 0** (Arcade) dans le dword `0x180751010`, première case d'un bloc de réglages de 16 octets, en `0x1801DC3A6`. Construit les 6 octets de réglages en `0x1801DC317`–`0x1801DC367` | RTTI (vtable `0x180532668` [2]) ; `analysis/mode_de_jeu.md` §1 et §3 | APM3 |
| `0x1801DD6A0` | `TaskMenuScoreAttack::update` | Pose le mode de jeu = **1** (Score Attack) en `0x1801DD73E`. **Corrige `vs_gameover.md` §2**, qui l'appelait « versus » | RTTI (vtable `0x1805326C8` [2]) ; `analysis/mode_de_jeu.md` §5 | APM3 |
| `0x1801DC050` | `TaskMenuArcadeLicenceChallenge::update` | Pose le mode de jeu = **2** en `0x1801DC179` | RTTI (vtable `0x1805327E8` [2]) ; `analysis/mode_de_jeu.md` §1 | APM3 |
| `0x1801A4160` | `TaskMenuTeam::update` | Pose le mode de jeu = **3** (Special Sparring) en `0x1801A4252` | RTTI (vtable `0x180410C50` [2]) ; `analysis/mode_de_jeu.md` §1 | APM3 |
| `0x1801DDB40` | `TaskMenuVersus::update` | Pose le mode de jeu = **4** (Versus) en `0x1801DDC43` | RTTI (vtable `0x1805328A8` [2]) ; `analysis/mode_de_jeu.md` §1 | APM3 |
| `0x1801E10E0` | `TaskMenuMulti::draw` | La page `MULTI MENU`. **Jumelle de `FUN_18020CC90` de REVO, dont `MENU.md` §419.92 ne savait pas ce qu'elle était** : en-tête `0x17C`, qui tombe entre `OFFLINE VERSUS` (`0x17B`) et `ONLINE BATTLE` (`0x17D`), lignes `0x1DC 0x1DD 0x1DE` = Custom Match / Create Match / Custom Match. **C'est une page EN LIGNE**, et le RTTI le dit | RTTI (vtable `0x180532B48` [4]) | APM3 |
| `0x1801E1430` | `TaskMenuReplay::draw` | La page `REPLAYS`. Jumelle de `FUN_18020CFB0`, que `MENU.md` §419.95 avait **déduite** de son en-tête `0x2A2` ; le RTTI confirme | RTTI (vtable `0x1805329C8` [4]) | APM3 |
| `0x1801E17A0` | `TaskMenuScoreAttack::draw` | Le panneau de résultats. Jumelle de `FUN_18020D2F0`, lignes `0x1C1 0x1C2 0x1C3` = `CLASS / HIGH SCORE / CLEAR` **telles quelles**, palier **+0** — c'est elle qui prouve qu'un `-3` global serait faux | RTTI (vtable `0x1805326C8` [4]) ; `MENU.md` §419.92 | APM3 |
| `0x1801A8420` | `TaskOption::draw` | L'en-tête `HELP & OPTIONS`. Jumelle de `FUN_1801B82D0` (en-tête `0x183`, ligne 7 du menu principal, palier **+3**, non corrigée) | RTTI (vtable `0x180411348` [4]) ; `MENU.md` §419.95 | APM3 |
| `0x1801DE340` | `TaskMenuTerminal::validate` | La validation de la page TERMINAL. 0 référence directe (méthode virtuelle) : c'est pour ça qu'elle était introuvable. **Elle est l'une des onze de `APM3_A_VIDER.txt`** | RTTI (vtable `0x180532A28` [10]) ; `desassemblages/APM3_A_VIDER.txt` | APM3 |
| `0x1801DE7B0` | `TaskMenuMain` créneau [3] | **Rôle non établi.** `mode_de_jeu.md` §5 écrit « [3] = ? ». Son jumeau de REVO est `0x18020A5B0` (617 o), sans `.c` non plus. Déposée pour qu'on puisse la lire | RTTI (vtable `0x180532AE8` [3]) | APM3 |
| `0x1801E46D0` | `MenuMain_EntrerLeSousEtat_corps` | **19 octets, et ils disent tout** : `mov rcx,[0x180753818]` ; `lea rdx,"MAIN MENU"` ; `jmp 0x180245830`. C'est le vrai contenu du `fn_entree` du sous-état 36 | mesure du 19 nov. : seul appel de `0x1800DCCA0` | APM3 |
| `0x1801DB870` | `MenuMain_SortirDuSousEtat_corps` | 12 octets : `mov rcx,[0x180753818]` ; `jmp 0x1802450A0` | mesure du 19 nov. : seul appel de `0x1800DCBE0` | APM3 |
| `0x180245830` | `Tache_CreerParNom` | **LA fabrique de tâches par nom d'APM3**, trouvée par les deux lignes ci-dessus. Thunk de 25 o (`r9d=2`, gestionnaire `[0x180C41340]+0x10`) qui saute sur le corps `0x1802456C0` (354 o). **165 références** dans le module, mesurées. Jumelle de `FUN_1802CD400` de REVO, qui en a **189** | mesure du 19 nov., par le corps du `fn_entree` de `MENU_MAIN` | APM3 |
| `0x1802450A0` | `Tache_DetruireParObjet` | Le pendant : retire la tâche quand le sous-état se termine. 133 o | mesure du 19 nov., par le corps du `fn_sortie` | APM3 |

**Et un global :** `0x180753818` est le `TaskMenuMain *` d'APM3 — le jumeau de
`DAT_18079B160` de REVO. Il est lu par les deux corps ci-dessus. Mesuré le
19 novembre ; ce n'est **pas** dans les notes existantes.

### 3.0 bis Les neuf pages de menu, nommées par le RTTI — la découverte

`MENU.md` §419.92 et §419.95 appelaient ces fonctions « les six pages sœurs
voisines de `FUN_18020C880` » et ne savaient pas ce qu'elles étaient. Elles
sont toutes le **créneau [4] (dessin)** d'une classe nommée, et le RTTI les
apparie des deux côtés d'un coup :

| classe | APM3 `[4]` dessin | REVO `[4]` dessin | ce que la page montre |
|---|---|---|---|
| `TaskMenuMain` | `0x1801E0C80` | `0x18020C880` | le menu principal, dix lignes |
| `TaskMenuArcade` | `0x1801DF100` | `0x18020AFC0` | `SINGLE PLAYER` |
| `TaskMenuVersus` | `0x1801E2190` | `0x18020DC80` | `OFFLINE VERSUS` |
| `TaskMenuTraining` | `0x1801E1E40` | `0x18020D960` | `DOJO` |
| `TaskMenuTerminal` | `0x1801E1B10` | `0x18020D640` | `TERMINAL` |
| `TaskMenuMulti` | `0x1801E10E0` | `0x18020CC90` | la page EN LIGNE (en-tête `0x17C`) |
| `TaskMenuReplay` | `0x1801E1430` | `0x18020CFB0` | `REPLAYS` |
| `TaskMenuScoreAttack` | `0x1801E17A0` | `0x18020D2F0` | `CLASS / HIGH SCORE / CLEAR` |
| `TaskOption` | `0x1801A8420` | `0x1801B82D0` | l'en-tête `HELP & OPTIONS` |

Les trois pages que `MENU.md` laissait « lues mais non corrigées, hors
priorité » ont donc maintenant un **nom** et un **jumeau APM3** : c'est ce
qu'il faut pour relever leurs immédiats justes de la même façon que les
quatre déjà faites.

### 3.1 Les 14 fonctions de menu d'APM3 déjà désassemblées avant aujourd'hui

Elles sont dans `FS APM3/desassemblage/` (racine), **pas** dans `menus/`, et
leur table est dans `desassemblage/README.md`. Toutes sont APM3, toutes
touchent le **TERMINAL / Customize** :

`0x1801C7440` `TaskSelItemMenu::update` · `0x1801C7B50` le consommateur de
message mort de « select item » · `0x1801C8110` le dessin de la grille ·
`0x1801C7D00` le curseur de « select part » · `0x1801CA040` son dessin ·
`0x180217E70` le résolveur de nom d'objset · `0x180038600` le demandeur
d'archive d'objets · `0x1801CBFE0` les marqueurs AET de la fenêtre ·
`0x1801C13B0` `customize::ItmEqTask::update` · `0x1801CE400` le basculement
de modèle · `0x180151CF0` `TaskRobSingle::update` · `0x1801437E0` le
publieur de la structure joueur · `0x1801C2EC0`
`customize::ItemMain::update` · `0x1801BBBE0` le répartiteur de curseur.

Le RTTI confirme deux de ces noms : `0x1801C7440` est bien le créneau [2] de
`?A0x976cdec3::TaskSelItemMenu` (vtable `0x1805304E0`), et `0x1801BBBE0`
celui de `TaskCsMenu` (vtable `0x18052F6C0`).

### 3.2 Les 4 fonctions de menu d'APM3 dont le C existe

Dans `FS APM3/code_decompile/` (en-tête `Binaire : vf5fs_apm3 /
vf5fs_apm3_origine.dll`), **non copiées ici** pour ne rien dupliquer :

| adresse | fichier | nom RTTI mesuré ce jour |
|---|---|---|
| `0x18016C570` | `Selecteur_Pas.c` | **`TaskSelector::update`** (vtable `0x1803FEFD8` [2]) |
| `0x18016C9C0` | `Selecteur_EscalierChoix.c` | — (8 o, un escalier de saut) |
| `0x18016CC30` | `Selecteur_EscalierStage.c` | — |
| `0x180173110` | `SelChara_PasGrillePort.c` | — |

C'est une **correction de nomenclature** que cette séance apporte :
`Selecteur_Pas` est `TaskSelector::update`, des deux côtés.

### 3.2 bis Le chemin de l'appui jusqu'au validateur (APM3) — et trois recoupements

Deux notes écrites par Frédéric **le 19 novembre, en parallèle de ce
relevé**, désassemblent ce trajet ; elles sont dans
`FS APM3/analysis/menus_repetition_appui.md` (§1) et
`FS APM3/analysis/menu_echappe.md` (§1). Je ne les ai **pas** re-mesurées ;
je les reprends et je recoupe trois de leurs adresses avec le RTTI.

| adresse | nom proposé | ce qu'elle fait | d'où vient le nom | côté |
|---|---|---|---|---|
| `0x1801A2BC0` | `Entree_FrontValider` | `Input_isOnNow(7)` en direct par `[rax+0x160]` de l'objet `[0x180C3B6F8]`, puis `neg/sbb/neg/dec` : rend **0** si front, **-1** sinon. 38 o | `analysis/menus_repetition_appui.md` §1 étape 8a | APM3 |
| `0x1801A2B90` | `Entree_FrontAnnuler` | Identique avec `edx = 8` : `Input_isOnNow(8)`. 38 o | idem, étape 8b | APM3 |
| `0x1801A2CA0` | `Entree_LireTenu` | Ne touche pas la greffe : lit les tableaux du moteur en `0x180751040` / `0x180751174` / `0x180751280` | idem, étape 8c | APM3 |
| `0x1801BBBE0` | **`TaskCsMenu::update`** — le curseur partagé | Corps en `0x1801BBC05`. `0x1801BBCC6 call 0x1801A2B90` → annuler `[r8+0x48]` ; `0x1801BBCDD call 0x1801A2BC0` → **le validateur `[r8+0x50]`**. **Entre le prédicat et le validateur il n'y a aucun état** : si `Input_isOnNow(7)` est vrai sur N trames, le validateur est appelé N fois | **RECOUPEMENT** : le RTTI en fait le créneau [2] de `TaskCsMenu` (vtable `0x18052F6C0`), 37 o — et son jumeau de REVO `0x1801DE510` fait **37 o aussi**. `desassemblage/README.md` l'appelait « le répartiteur de curseur » ; `menus_repetition_appui.md` §1 étape 9 | APM3 |
| `0x1801A8090` | **`TaskOptionMenu::validate`** | `mov eax,[liste+0x58] ; mov [liste+0x2F8],eax ; mov byte [liste+0x2F0],1` | **RECOUPEMENT** : créneau [10] de `TaskOptionMenu` (vtable `0x1804110A8`), 68 o — jumeau de REVO `0x1801B7FB0`, créneau [11], **68 o aussi**. `menus_repetition_appui.md` §1 étape 10 l'appelait « le validateur des OPTIONS » | APM3 |
| `0x180243ED0` | `Entree_LecteurDuMoteur` | 690 o. Interroge les treize codes par `Input_isOn` (`+0x158`) et compose un masque arcade en `0x180751050 + joueur*0x54`, avec son propre historique : `+0x08` tenu, `+0x0C` tenu à la trame précédente, `+0x10` front montant, `+0x14` relâché, `+0x18` répétition (masque `0x000FF0C9`, retard 24, période 3). **L'état de manette du moteur est correct, fronts compris** | `analysis/menus_repetition_appui.md` §1 ; mesure du 2026-09-04 reprise de `menu_console.md` §7 | APM3 |
| `0x18021489D` | `Mode_QuitterSurLeCode15` | Le site `0x18021490F` y lit `Input_isOnNow(15)` pour **quitter un mode et revenir au menu**. C'est ce que portait la touche ÉCHAPPE | `analysis/menu_echappe.md` §1 ; bornes `.pdata` mesurées ici (177 + 225 o chaînés) | APM3 |

**Pourquoi ces recoupements comptent.** Deux fonctions que les notes
désignaient par leur rôle (« le répartiteur de curseur », « le validateur des
OPTIONS ») ont maintenant un **nom de classe** et un **jumeau REVO de même
taille**. C'est la démonstration que la méthode du §3.3 marche sur des cas
déjà travaillés à la main : elle ne contredit rien et elle ajoute la colonne
qui manquait.

### 3.3 Les 29 classes de page de menu, par le RTTI — les deux modules

Créneaux `[0]` destructeur, `[1]` init, `[2]` mise à jour. **Chaque colonne
ne vaut que dans son module.**

| classe | APM3 vtable | APM3 [1] init | APM3 [2] update | REVO vtable | REVO [1] init | REVO [2] update |
|---|---|---|---|---|---|---|
| `TaskMenuMain` | `0x180532AE8` | `0x1801E36D0` | `0x1801DC620` | `0x18055A510` | `0x18020F1E0` | `0x1802079E0` |
| `TaskMenuMulti` | `0x180532B48` | `0x1801E3E60` | `0x1801DD190` | `0x18055A578` | `0x18020FB10` | `0x180208EE0` |
| `TaskMenuArcade` | `0x180532848` | `0x1801E2F00` | `0x1801DBE20` | `0x18055A238` | `0x18020EA50` | `0x180206EF0` |
| `TaskMenuArcadeNormal` | `0x180532668` | `0x1801E3270` | `0x1801DC270` | `0x18055A030` | `0x18020ED90` | `0x180207320` |
| `TaskMenuArcadeLicenceChallenge` | `0x1805327E8` | `0x1801E3080` | `0x1801DC050` | `0x18055A1D0` | `0x18020EBB0` | `0x180207110` |
| `TaskMenuScoreAttack` | `0x1805326C8` | `0x1801E4170` | `0x1801DD6A0` | `0x18055A098` | `0x18020FE40` | `0x180209410` |
| `TaskMenuVersus` | `0x1805328A8` | `0x1801E4560` | `0x1801DDB40` | `0x18055A2A0` | `0x180210370` | `0x1802098E0` |
| `TaskMenuTraining` | `0x180532968` | `0x1801E4420` | `0x1801DD9C0` | `0x18055A370` | `0x180210230` | `0x180209750` |
| `TaskMenuCommandTraining` | `0x180532908` | `0x1801E3510` | `0x1801DC510` | `0x18055A308` | `0x18020F030` | `0x1802078D0` |
| `TaskMenuTerminal` | `0x180532A28` | `0x1801E4300` | `0x1801DD7A0` | `0x18055A440` | `0x180210110` | `0x180209530` |
| `TaskMenuReplay` | `0x1805329C8` | `0x1801E3FF0` | `0x1801DD400` | `0x18055A3D8` | `0x18020FCC0` | `0x180209170` |
| `TaskMenuDlContent` | `0x180532A88` | `0x1801E36A0` | `0x1801DC600` | `0x18055A4A8` | `0x18020F1B0` | `0x1802079C0` |
| `TaskCsMenu` | `0x18052F6C0` | `0x1801BD120` | `0x1801BBBE0` | `0x180558270` | `0x1801DFBC0` | `0x1801DE510` |
| `TaskEndMenu` | `0x18039A160` | `0x1800A7A00` | `0x1800A4510` | `0x1803C2D00` | `0x1800A51B0` | `0x1800A1870` |
| `TaskOption` | `0x180411348` | `0x1801AA7C0` | `0x1801A6F70` | `0x18043A048` | `0x1801BA870` | `0x1801B6E50` |
| `TaskOptionMenu` | `0x1804110A8` | `0x1801AAFF0` | `0x1801A7B60` | `0x180439D78` | `0x1801BAFF0` | `0x1801B7A90` |
| `TaskOptionControl` | `0x180411188` | `0x1801AA8A0` | `0x1801A7220` | `0x180439E68` | `0x1801BA950` | `0x1801B70E0` |
| `TaskOptionSetting` | `0x1804111F8` | `0x1801AB190` | `0x1801A7D70` | `0x180439EE0` | `0x1801BB170` | `0x1801B7CA0` |
| `TaskOptionFile` | `0x180411268` | `0x1801AAD10` | `0x1801A77B0` | `0x180439F58` | `0x1801BAD00` | `0x1801B76E0` |
| `TaskOptionHowto` | `0x180411118` | `0x1801AAE50` | `0x1801A7980` | `0x180439DF0` | `0x1801BAE40` | `0x1801B78B0` |
| `TaskOptionInfo` | `0x1804112D8` | `0x1801AAEF0` | `0x1801A7A70` | `0x180439FD0` | `0x1801BAEE0` | `0x1801B79A0` |
| `TaskPause` | `0x1805337F0` | `0x1801E9140` | `0x1801E7C30` | `0x18055B0C0` | `0x1802260E0` | `0x180223670` |
| `TaskPauseMenu` | `0x180533790` | `0x1801E91F0` | `0x1801E7C60` | `0x18055B058` | `0x1802261D0` | `0x1802236A0` |
| `TaskSelector` | `0x1803FEFD8` | `0x18016CF80` | `0x18016C570` | `0x180428260` | `0x18017B850` | `0x18017AE30` |
| `TaskSelChara` | `0x1803FEF98` | `0x180170560` | `0x18016DA30` | `0x180428218` | `0x18017E9D0` | `0x18017C1E0` |
| `TaskSelCursor` | `0x1803FEF58` | `0x180173AD0` | `0x1801724B0` | `0x1804281D0` | `0x180182CD0` | `0x180181550` |
| `TaskSelStage` | `0x180400A18` | `0x180175140` | `0x180174250` | `0x180429D98` | `0x1801844E0` | `0x180183390` |
| `TaskSelCommon` | `0x1803FFCF8` | `0x180171D50` | `0x180171100` | `0x180428E70` | `0x180180C10` | `0x18017F790` |

Trois vérifications croisées, qui valident la méthode :
`TaskSelector::init` de REVO vaut `0x18017B850` — exactement le fichier
`desassemblages/module_chargeur_2d_selecteur_0x18017B850.asm` déjà écrit ;
`TaskCsMenu::init` de REVO vaut `0x1801DFBC0` — exactement la fonction dont
`MENU.md` §3 dit qu'elle crée `MENU_EXPLAIN` et `MENU_CONTROL` ; et
`TaskSelCursor::update` de REVO vaut `0x180181550`, que `VF5RE/a_vider.txt`
range sous « le CURSEUR : là où tout se décide ».

Le tableau complet (46 classes communes, tous les créneaux, les tailles, et
les 8 + 8 classes propres à un module) est dans
`menus/VTABLES_MENUS_APM3_VS_REVO.txt`.

---

## 4. LES FONCTIONS DE REVO — le tableau

### 4.1 La chaîne jusqu'au menu, et la tâche `MAIN MENU`

| adresse | nom proposé | ce qu'elle fait | d'où vient le nom | côté |
|---|---|---|---|---|
| `0x1800E4140` | `ModeMenu_Phase0` | Phase 0 du **mode 5 = MENU** : charge le voile, deux SPR (`0x268`, `0x269`) et un AET (`0x208`), puis attend. **Aucun test de `bloc+0x1FF08`** : le chargement du mode MENU ne dépend pas de notre répartiteur | `MENU.md` §1 | REVO |
| `0x1800E4080` / `0x1800E40C0` | `ModeMenu_Phase1` / `_Phase2` | Les deux autres phases du mode 5 | `MENU.md` §1 ; `CHAINES_DES_MODES_REVO.txt` position 2 | REVO |
| `0x1800E4210` | `MenuMain_Phase0` | Phase 0 du **sous-état 40 = MENU_MAIN** | `MENU.md` §1 ; `TABLE_DES_SCENES…` §5 ligne 40 | REVO |
| `0x18000BA20` | `Bouchon_XorAlRet` | **Deux octets, `XOR AL,AL ; RET`.** C'est la phase 1 de `MENU_MAIN`, donc le sous-état **ne finit jamais** : état de REPOS par construction. C'est aussi lui qui rend mortes la branche réseau du chemin (A) et le couple `UNLOCK FULL GAME` / `DOWNLOAD CONTENT` | `MENU.md` §10.5, désassemblé | REVO |
| `0x1800E4130` | `MenuMain_Phase2` | Phase 2 du sous-état 40 | `MENU.md` §1 | REVO |
| `0x1800E1B00` / `0x1800E1B20` | `Etat_DemanderUnMode` / `_UnSousEtat` | Les deux portes de transition du répartiteur de scènes | `MENU.md` §1 | REVO |
| `0x1800E1600` | `Etat_RepartiteurDesPhases` | Le répartiteur qui appelle les trois gestionnaires de phase | `code_decompile/CHAINE_DEMARRAGE.md` | REVO |
| `0x1802CD400` | `Tache_CreerParNom` | **La fabrique de tâches par nom** : `(objet, "NOM")`. 32 sites littéraux relevés, plus 4 noms passés par variable → **au moins 36** tâches nommées | `MENU.md` §3 | REVO |
| `0x1802CD130` | `Tache_Repartiteur` | Le répartiteur de tâches : c'est lui qui atteint `init` et `update`, qui n'ont aucun appelant direct | `MENU.md` §4 | REVO |
| `0x1802CCAB0` | `Tache_EstVivante` | Parcourt la liste des tâches vivantes (`*DAT_180EA7608`, chaînée par `[+0x10]`) et rend 1 si l'objet y est | `MENU.md` §10.3 | REVO |
| `0x180206570` / `0x1802056A0` | `TaskMenuMain_Allouer` / `_Construire` | Allocation (`0x3028` octets) et construction de `DAT_18079B160`. Le constructeur **pose une vtable nommée à chaque sous-objet embarqué** : c'est de là que viennent les 13 décalages du §10.1 | `MENU.md` §10.1 | REVO |
| `0x180205440` | `TaskMenuMain_ConstruireGroupeArcade` | Pose les six sous-objets de `+0x610` à `+0x1528` | `MENU.md` §10.1 | REVO |
| `0x1802065F0` | `TaskMenuMulti_Allouer` | `DAT_18079B168` | `MENU.md` §10.2 | REVO |
| `0x1801B3E40` / `0x1801B3F70` | `TaskMenuSetting_Construire` / `TaskMenuTeam_Construire` | Les deux globaux `DAT_180795C30` et `DAT_180795C38`, posés **avant tout** par `module_start → 0x1802C9120 → 0x1802C8B70` (appels inconditionnels) | `MENU.md` §10.1–10.2 | REVO |
| `0x18020F1E0` | `TaskMenuMain::init` | 11 556 o. **Deux chemins exclusifs** : si `bloc+0x1FF08` est nul, le chemin (A) monte le menu entier lui-même (fond `bg_base` AET `0x2A3`, trois gadgets, les tâches de sous-menu, la musique `vf5b_tkv.adx`) et `return 1` ; sinon chemin (B), qui n'affiche rien et attend l'hôte | RTTI (vtable `0x18055A510` [1]) ; `MENU.md` §4 et §6 | REVO |
| `0x1802079E0` | `TaskMenuMain::update` | 28 770 o. Porte le **switch de validation** du menu principal (11 entrées + l'entrée 12), et un second switch qui traduit `+0x28C4` en argument du voile | RTTI (vtable `0x18055A510` [2]) ; `MENU.md` §4–5 | REVO |
| `0x18020A5B0` | `TaskMenuMain_Creneau3` | Créneau [3] de la vtable, **rôle inconnu** | RTTI (vtable `0x18055A510` [3]) | REVO |
| `0x18020C880` | `TaskMenuMain::draw` | Le dessin des **dix lignes**. Quatrième étage du garde `bloc+0x1FF08`. Les dix identifiants `0x17A 0x17B 0x17D 0x17E 0x17F 0x181 0x182 0x183`, puis `0x185`, puis `0x186` ; en-tête `0x179`. Ancres de mise en page `p_main_head_lt`, `p_menutxt_PS3_lt`, `p_menutxt_02_rb` | RTTI (vtable `0x18055A510` [4]) ; `MENU.md` §419.83 | REVO |
| `0x180209CB0` | `TaskMenuMain::validate` | **Cité 13 fois dans `MENU.md` et jamais décompilé.** Lit l'état de l'entrée en `0x180209CD4` (`cmp byte [rcx+rdi+0x5fa], 0`) — le même champ que le `0x642` d'APM3. 77 o, la même taille que son jumeau `0x1801DDF30`. Désassemblé aujourd'hui : `menus/revo_asm/revo_menu_repartiteur_validation.asm` | RTTI (vtable `0x18055A510` [11]) ; `MENU.md` §419.83 | REVO |
| `0x1802117D0` | `Menu_LireLEtatDUneEntree` | `cmp byte [rax+rcx+0x5fa], 2` : teste l'état **2 = pas dessinée du tout**. 37 o, créneau [8], jumeau de `0x1801E4CD0` d'APM3 (37 o aussi). Désassemblé aujourd'hui | RTTI (vtable `0x18055A510` [8]) ; `MENU.md` §419.83 | REVO |
| `0x1801DFB00` | `TaskMenuMain_Creneau9` | 16 o, jumeau de `0x1801BD080` d'APM3 (16 o). **Rôle inconnu**, pas de `.c` | RTTI (vtable `0x18055A510` [9]) | REVO |
| `0x1801E1080` | `Menu_PoserLeCurseurSurLEntree` | Appelée par le dessin quand l'indice de boucle égale `[menu+0x58]`, l'entrée choisie : c'est ce qui place le curseur. Pas de `.c`. Désassemblée aujourd'hui | `MENU.md` §419.83 | REVO |
| `0x1802316E0` | `Texte_ResoudreUnLibelle` | Résout un identifiant de texte. Jumeau de `0x1801EFD10` d'APM3 | `MENU.md` §419.83, §419.94 | REVO |
| `0x180231570` | `Texte_SecondResolveur` | La seconde des deux fonctions de texte videes au §419.95 | `MENU.md` §419.95 | REVO |
| `0x18020A2B0` | `Menu_CurseurAConfirme` | Appelée sur `param_1 + 0x28E8` (l'objet curseur) juste avant le switch de validation | `MENU.md` §4, §5 | REVO |
| `0x180211420` | `TaskMenuMain_InscrireLesDouzeGestionnaires` | Le chemin (B) abonne `MAIN MENU` **douze** fois (et non « ~30 », corrigé au §11). Cinq des douze posent le no-op `0x18000AF60` | `MENU.md` §11.1–11.2 | REVO |
| `0x180081FE0` | `Evenement_AbonnerUnRappel` | `(id, fonction, contexte, en_queue)` : table `&DAT_18073AA28 + id*0x10`, nœuds de 5 qwords, liste libre `DAT_18073AA18`. **C'est le système d'événements interne du module**, pas un dialogue avec l'hôte | `MENU.md` §11.1 | REVO |
| `0x180081C50` | `Evenement_Distribuer_ET_PrevenirLHote` | Prévient l'hôte par `bloc+0x20348` — **un second créneau de rappel, indépendant de `+0x1FF08`**, que nous laissons nul à dessein. Puis appelle les abonnés en ordre inverse | `MENU.md` §11.4 | REVO |
| `0x180081D30` | `Evenement_Distribuer_SansLHote` | Le même, **sans** la notification. Un seul site, `0x1802CCE1B` | `MENU.md` §11.4 | REVO |
| `0x18020E540` | `MenuMain_Gestionnaire_4C_4E_56_50` | Le gestionnaire réel répété quatre fois (ids `0x4C`, `0x4E`, `0x56`, `0x50`) | `MENU.md` §11.2–11.3 | REVO |
| `0x18020E520` | `MenuMain_Gestionnaire_54` | Id `0x54` : pose le bit 2 de `[p+0x22]` | `MENU.md` §11.3 | REVO |
| `0x18020E570` | `MenuMain_Gestionnaire_5E` | Id `0x5E` : **écrit `1` dans `TaskMenuMain+0x2909`** puis appelle `0x180227F40(2)` / `0x180227FB0` | `MENU.md` §11.3 | REVO |
| `0x18000AF60` | `NoOp_Ret0` | `RET 0x0`, **une seule instruction.** Ghidra l'étiquette `_guard_check_icall` ; ce n'est pas une erreur, c'est le symbole. Cinq des douze inscriptions posent ce no-op | `MENU.md` §11.2 | REVO |
| `0x180210B10` / `0x180210BD0` | `TaskMenuMain_RemettreLesDrapeauxAZero` / `_GroupeArcade` | Énumèrent exactement les décalages `+0x60` du §10.1 : **le module confirme la liste lui-même** | `MENU.md` §10.3, §10.5 | REVO |
| `0x1801B5750` / `0x1801B5790` | `Predicat_RevenirChezTaskMenuSetting` / `…Team` | Rendent 0 si la tâche VIT, sinon `1` ou `2` selon `+0x60`. Le test du chemin (A) est `!= 2` : **`+0x60` est un drapeau « reviens chez moi »**, et toute la cascade est le chemin de RETOUR depuis un sous-menu, pas un choix de démarrage | `MENU.md` §10.3 | REVO |
| `0x1802603D0` / `0x1801FB550` / `0x1801F0460` | `Predicat_Training` / `_Terminal` / `_Replay` | Les trois autres prédicats de la cascade. Leurs classes ne sont **pas** relevées | `MENU.md` §10.4, §10.7 | REVO |
| `0x1801CF0C0` | `Menu_Portillon` | `FUN_1802CCA00(DAT_1807969A0) ^ 1` : « l'objet `DAT_1807969A0` n'est pas une tâche active ». Si ça ne passe pas, l'init rend 0 et recommence | `MENU.md` §10.6 | REVO |
| `0x1801A4180` / `0x1801A3F20` / `0x1801A4030` / `0x1801A3E10` / `0x1801A3EF0` | `Voile_*` | Le voile / `WAIT_SCREEN` : chargement, allumage, pose d'argument (`0→3, 1→4, 2→9, 3→2, 4→1, 5→5, 8→6, 9→7, 12→8, défaut→0`), création de la tâche, test | `MENU.md` §1, §5, §10.6 | REVO |
| `0x1801E16C0` / `0x1801E0470` | `Gadget_PoserLaSorte` / `_PoserLaRessource` | Les **trois gadgets** `+0x230`, `+0x280`, `+0x2D0` reçoivent `(7, 0x2B)`, `(1, 0x2A)`, `(0x19, 0x2C)`. Les sortes et les ressources ne sont **ni nommées ni rapprochées de l'atlas** | `MENU.md` §10.6 | REVO |
| `0x180025EB0` | `Aet_ChargerUnFond` | `(0x2A3, "bg_base", 1, 0x10000, "neu_s", "neu_e")` — **la même primitive que `logo_vf5` au titre** | `MENU.md` §6, §10.6 | REVO |

### 4.2 Les pages filles et les autres écrans (REVO)

Les huit premières lignes portent leur **nom RTTI mesuré le 19 novembre** :
jusqu'ici `MENU.md` ne les désignait que par leur adresse.

| adresse | nom proposé | ce qu'elle fait | d'où vient le nom | côté |
|---|---|---|---|---|
| `0x18020AFC0` | `TaskMenuArcade::draw` (`SINGLE PLAYER`) | En-tête `0x17A` en `0x18020B109` ; libellés `0x1A2 0x1A3 0x1A4 0x1A5`. **Décalage +4** sur APM3 | RTTI (vtable `0x18055A238` [4]) ; `apm3_pages_sousmenus_0x1E1C51.asm` ; `MENU.md` §419.94 | REVO |
| `0x18020DC80` | `TaskMenuVersus::draw` (`OFFLINE VERSUS`) | En-tête `0x17B` en `0x18020DDF1` ; libellés `0x1B1 0x1AD 0x1CF 0x1D4 0x1D9`. **+4** | RTTI (vtable `0x18055A2A0` [4]) ; idem | REVO |
| `0x18020D960` | `TaskMenuTraining::draw` (`DOJO`) | En-tête `0x17E` en `0x18020DAA6` ; libellés `0x21B 0x21C 0x21D`. **+4** | RTTI (vtable `0x18055A370` [4]) ; idem | REVO |
| `0x18020D640` | `TaskMenuTerminal::draw` (`TERMINAL`) | En-tête `0x17F` en `0x18020D77A` ; libellés `0x2A1 0x2A2`. **+8** — le palier le plus élevé | RTTI (vtable `0x18055A440` [4]) ; idem | REVO |
| `0x18020CC90` | `TaskMenuMulti::draw` | **C'est la page EN LIGNE**, et `MENU.md` §419.92 ne le savait pas. En-tête `0x17C`, qui tombe **entre** `OFFLINE VERSUS` (`0x17B`) et `ONLINE BATTLE` (`0x17D`) : la preuve directe, dans le code, que REVO a inséré des entrées. Lignes `0x1DC 0x1DD 0x1DE`. **NON corrigée** | RTTI (vtable `0x18055A578` [4]) ; `MENU.md` §419.92, §419.95 fait 3 | REVO |
| `0x18020CFB0` | `TaskMenuReplay::draw` (`REPLAYS`) | En-tête `0x2A2` = « Replays » de la page TERMINAL ; lignes `0x2A3 0x2A4 0x2A5` dans un panneau `p_small_head_lt`. Palier **+8**. NON corrigée | RTTI (vtable `0x18055A3D8` [4]) ; `MENU.md` §419.95 fait 2 | REVO |
| `0x18020D2F0` | `TaskMenuScoreAttack::draw` | Lignes `0x1C1 0x1C2 0x1C3` = `CLASS / HIGH SCORE / CLEAR`, **justes telles quelles** : palier **+0**. C'est elle qui prouve qu'un `-3` global serait faux | RTTI (vtable `0x18055A098` [4]) ; `MENU.md` §419.92 | REVO |
| `0x1801B82D0` | `TaskOption::draw` | En-tête `0x183` = « HELP & OPTIONS », ligne 7 du menu principal. Palier **+3**. NON corrigée | RTTI (vtable `0x18043A048` [4]) ; `MENU.md` §419.95 fait 2 | REVO |
| `0x1801DBA00` | `Page_QuiPosteSesIdentifiants` | **Elle ne grave AUCUN immédiat de pile** : elle POSTE ses identifiants (`0x19D`, `0x1A6`, …) à l'hôte par `bloc+0x1FF08` avec la **commande `0xC1` (193)**. Il y a donc **deux façons** pour une page de nommer son texte, et une correction d'immédiats ne touche que la première | `MENU.md` §419.95 fait 3 | REVO |
| `0x1801BB3A0` | `Option_OuvrirLaPage` | Crée `OPTION` ou `OPTION CONTROL`. Jumeau de `0x1801AB3A0` d'APM3 | `MENU.md` §3 | REVO |
| `0x1801C0100` | `Ranking_CreerLaTache` | Crée `RANKING` sur `&DAT_180795C70` ; joue `rom/sound/bgm/vfes_bgm_mnu.adx`. Entrée 10 du switch | `MENU.md` §3, §5 | REVO |
| `0x1801DFBC0` | `TaskCsMenu::init` | Crée `MENU_EXPLAIN` (`param_1+0x68`) et `MENU_CONTROL` (`param_1+0x138`) | RTTI (vtable `0x180558270` [1]) ; `MENU.md` §3 | REVO |
| `0x18017BB10` | `Selector_CreerLaTache` | Crée la tâche `SELECTOR` | `MENU.md` §3 | REVO |
| `0x1801FC240` | `DataSelector_CreerLaTache` | Crée `DATA SELECTOR` sur `DAT_18079A688 + lVar2` | `MENU.md` §3 | REVO |
| `0x1801BC1A0` | `Promotion_CreerLaTache` | Crée `PROMOTION` — **code mort** : atteint seulement derrière `FUN_18000BA20()`, qui rend toujours 0 | `MENU.md` §3, §10.5 | REVO |
| `0x18020E9B0` | `ReplayScore_CreerLaTache` | Crée `REPLAY_SCORE` sur `&DAT_18073D970` ; aussi cité comme lecteur de l'objet curseur `+0x28E8` | `MENU.md` §3, §4 | REVO |
| `0x180221BA0` · `0x1802A1030` · `0x180228040` · `0x1801FE310` · `0x1801B26B0` · `0x1801D7E60` | `MultiRnkchg_*` · `ClipDl_*` · `ReplayOnline_*` · `LicenceChallengeResult_*` · `DeviceConnection_*` · `Telemetry_*` | Les six autres fabriques de tâches d'écran du relevé | `MENU.md` §3 | REVO |
| `0x1800E5B20` · `0x1800E3CA0` · `0x18003F1A0` · `0x1800F07E0` · `0x1802230D0` · `0x180086350` · `0x1800863B0` · `0x1800E5BC0` · `0x1800666B0` · `0x1800E6580` · `0x1800E6660` · `0x1800E5D20` · `0x1800E64F0` · `0x1800E6510` | `Information_*` · `GameScore_*` · `Auth3d_*` · `Movie_*` · `TaskCredit_*` · `TaskEnding_*` · `TaskVsFinishEnding_*` · `Closing_*` · `DataInitialize_*` · `SystemStartup_*` · `Warning_*` · `OfflineWarning_*` (deux sites) · `Title_*` | Les quatorze dernières fabriques du relevé des 32 sites littéraux | `MENU.md` §3 | REVO |

### 4.3 Le switch de validation du menu principal (REVO)

Toutes dans `0x1802079E0`, après `0x18020A2B0(param_1 + 0x28E8)`. Le champ
`+0x28C4` est **l'index de l'entrée choisie**, posé à **17** par l'init —
qui n'est aucun cas du switch, donc `default`.

| entrée | commande hôte | fonctions du module | destination |
|---:|---|---|---|
| 0 | `188(2)` | `0x1802104E0(p,0)`, `0x18021A450` | mode 11 `RANK_MATCH` |
| 1 | `213` puis `188(3)` | `0x1802104E0(p,1)` | mode 12 `ROOM_MATCH` |
| 2 | `188(4)` | `0x1802104E0(p,2)` | mode 13 `TOURNAMENT` |
| 3 | `188(6)` | `0x1801AA1D0` (`RemplirDescripteurMatch.c`) + `0x1801AAD60(4,…)` + `0x1801D5920` | combat local, config complète |
| 4 | `188(5)` | `0x1801AA1D0` + `0x1801AAC20(0,…)` (`DemanderPartie.c`) + `0x1801D5920` | combat local, autre entrée |
| 5 | `188(7)` | `0x180260950(+0x28C5)`, `0x1802608B0(1)` | `0x1801AABE0(6,0,1)` → mode 7 `CS_TRAINING`, sorte 6 |
| 6 | `188(7)` | `0x180262890(+0x28C6)` | `0x1801AABE0(9,0,1)` |
| 7 | `188(7)` | `0x180240470(+0x28C7)`, `0x1802404D0(+0x28C8)` | `0x1801AABE0(10,0,1)` |
| 8 | `188(7)` | — | `0x1801AABE0(7, +0x28CD==0, 1)` |
| 9 | `188(7)` | — | `0x1801AABE0(8,0,1)` |
| 10 | — | `0x1801C0100(0,0,1)` | reste dans le menu |
| 0x10 (16) | — | `PostQuitMessage(0)` | **EXIT** — l'octet vaut 17, donc on ne l'atteint pas par défaut |

`0x1801AABE0(sorte, drapeau, lancer)` = `Match_PoserSorteEtVider.c` : pose
`DAT_180795928` et `DAT_180795935`, puis `0x1800E1B00(7)`. **Les cinq
entrées 5 à 9 mènent toutes au même mode ; c'est la SORTE qui les
distingue.** Source : `MENU.md` §5 et §419.97.

### 4.4 Les sous-états de menu de REVO, désassemblés aujourd'hui

Aucun des six n'avait de `.c`. Dans `menus/revo_asm/`.

| adresse | nom proposé | sous-état | d'où vient le nom |
|---|---|---|---|
| `0x180211F90` / `0x180211A80` / `0x180211E90` | `CsTermCustomize_Entrer` / `_MettreAJour` / `_Sortir` | 41 `CS_TERM_CUSTOMIZE` | `TABLE_DES_SCENES_APM3_VS_REVO.md` §5 |
| `0x180212140` / `0x180212070` / `0x1802120D0` | `CsTraining_Entrer` / `_MettreAJour` / `_Sortir` | 45 `CS_TRAINING` | `TABLE_DES_SCENES_APM3_VS_REVO.md` §5 |

### 4.5 Le sélecteur et `MODE_SELECTOR` (REVO), déjà décompilés sous un nom

| adresse | fichier dans `revo_c/` | nom RTTI mesuré ce jour |
|---|---|---|
| `0x18017AE30` | `Selecteur_Pas.c` | **`TaskSelector::update`** (vtable `0x180428260` [2]) |
| `0x18017B280` | `Selecteur_EscalierChoix.c` | — |
| `0x180181FE0` | `SelChara_PasGrillePort.c` | — |
| `0x1800E3F70` | `SE20_MODE_SELECTOR_Phase0.c` | sous-état 20, `fn_entree` |
| `0x1800E2010` | `SE20_MODE_SELECTOR_Phase1_MontageDuMatch.c` | sous-état 20, `fn_maj` |
| `0x1800E2F40` | `SE20_MODE_SELECTOR_Phase2.c` | sous-état 20, `fn_sortie` |
| `0x1800E3F90` / `0x1800E2470` / `0x1800E2F60` | `FUN_1800e3f90.c` / `FUN_1800e2470.c` / `FUN_1800e2f60.c` | sous-état 19 `SELECTOR` — `0x1800E2470` est l'**ancre** qui a identifié la table des scènes |

---

## 5. CE QUI EST TRANSPOSABLE, ET CE QUI NE L'EST PAS

### 5.1 Transposable — et c'est mesuré

1. **Le nom de classe et le rang de créneau des douze premiers créneaux.**
   Les 46 classes de menu communes ont les mêmes `[0]` destructeur,
   `[1]` init, `[2]` update, `[4]` dessin. C'est la méthode à utiliser pour
   nommer n'importe quelle fonction de menu dans l'un ou l'autre module.
2. **La structure des deux tables d'états.** `struct EntreeScene` de 32
   octets, `{numero, drapeau, fn_entree, fn_maj, fn_sortie}`, identique dans
   les deux modules : `0x1803A05A0` (55 entrées) chez APM3, `0x1803C87F0`
   (73 entrées) chez REVO.
3. **Les noms de sous-états et de modes**, avec leur **décalage** : les 7
   sous-états `APM3_*` existent dans les deux tables, et la chaîne de
   démarrage d'APM3 est décalée de **−2** par rapport à REVO.
   `MENU_MAIN` = 36 chez APM3, 40 chez REVO. `SELECTOR` = 17 / 19.
   `MODE_SELECTOR` = 18 / 20. `CS_TRAINING` = 41 / 45.
4. **La forme des sites de libellé.** Les trois lignes du DOJO d'APM3 sont
   gravées **octet pour octet dans la même forme** que celles de REVO ; seul
   l'immédiat diffère. C'est ce qui autorise une substitution d'immédiat
   sans toucher à l'encodage.
5. **Le champ d'état par entrée**, au même endroit relatif : `page+0x642+i`
   chez APM3, `menu+0x5FA+i` chez REVO ; `0` normal, `1` grisée,
   `2` pas dessinée. Et le compte est un **dernier indice**, pas un
   nombre : `page+0x224` / `menu+0x214` valent **9** pour **dix** entrées.

### 5.2 NON transposable

1. **Les adresses.** Jamais, dans aucun sens. Même base, adresses
   différentes.
2. **Les identifiants de texte.** Le décalage est **par morceaux** :
   **+3** sur `0x176`–`0x186`, **+4** sur `0x19E`–`0x219`, **+8** sur
   `0x299`–`0x29A`, **+0** sur `0x62`–`0x6E` et sur `0x1C1`–`0x1C3`. Un
   `-3` global est **faux**, et c'est la mesure qui le dit : il aurait cassé
   les trois pages à +4 et la page à +8.
3. **Le nombre de créneaux d'une vtable.** `TaskMenuMain` : 11 chez APM3,
   12 chez REVO, avec une insertion en position 7.
4. **Le numéro de sous-état et de mode**, sans passer par les tables de
   noms (`0x3C9110` / `0x3C9190` chez REVO).
5. **Huit classes de chaque côté n'existent pas en face** (§5.3).
6. **Ce qui est bouchonné n'est pas le même.** Chez APM3 le bouchon est
   `0x180029FB0` (31 fois dans la table) ; chez REVO c'est `0x180026620`
   (32 fois), et les six `ONLINE_*` de REVO pointent `0x18000BA20`, pas le
   bouchon ordinaire. Côté APM3, **les modes `GAME` et `CS_TRAINING` ont
   leurs trois gestionnaires vivants et personne ne les demande** : c'est le
   plafond du menu console d'APM3, et il n'existe pas chez REVO.

### 5.3 Les seize classes sans vis-à-vis

**Seulement chez APM3 (8)** — rien à transposer depuis REVO :
`apm3TestMode::MenuTop`, `MenuPageBase`, `MenuBookkeep`, `MenuGameAssign`,
`MenuGameAssignRule`, `MenuGameAssignRuleLocal`, `MenuSoundSetting`,
`MenuBackupClear`. C'est le menu opérateur de la borne.

**Seulement chez REVO (8)** — ne pas les chercher dans APM3 :
`TaskMultiRoomMatchMenu`, `TaskTrnCharaPause`, `TaskTrnTipPause`,
`TrnCharaPauseStrategy`, `TrnTipPauseStrategy`, `CTnmtPauseMsg`,
`replay::ReplayMenu`, `world_stage::WorldStageMenu`.

Les dix classes qui paraissaient propres à un module au premier relevé le
sont par un artefact : MSVC numérote les **espaces de noms anonymes** par un
hachage qui diffère d'un build à l'autre
(`?A0x23f84344::CharSelector` chez APM3 = `?A0x370dc8ff::CharSelector` chez
REVO). Le tableau les apparie sur le nom, en gardant les deux hachages.

---

## 6. LES TROUS QUI RESTENT — nommés

1. **273 des 295 méthodes virtuelles de menu de REVO n'ont pas de `.c`**, et
   **281 des 285** côté APM3. Le travail de décompilation des menus est à
   **7 %** d'un côté et à **1,4 %** de l'autre. Le tableau de
   `VTABLES_MENUS_APM3_VS_REVO.txt` donne la liste exacte des cibles.
2. **Onze adresses de la partie menu de `MENU.md` restent sans aucune
   lecture** : `0x1800545B0`, `0x1801E6DD0`, `0x1801EDAB0`, `0x1801EDEF0`,
   `0x1801EDF00`, `0x1801FA1B0`, `0x1801FA9A0`, `0x1801FAC90`,
   `0x180208EE0` (qui est `TaskMenuMulti::update`), `0x180210860`,
   `0x18064C160`. (Sur 14 ; j'en ai désassemblé 3.)
3. **Les créneaux `[3]` et `[9]` de `TaskMenuMain` n'ont aucun rôle établi**,
   des deux côtés : REVO `0x18020A5B0` (617 o) et `0x1801DFB00` (16 o),
   APM3 `0x1801DE7B0` (393 o, désassemblé aujourd'hui, **pas lu**) et
   `0x1801BD080` (16 o). `mode_de_jeu.md` §5 l'écrit lui-même : « `[3]` = ? ».
4. **Le libellé de chaque entrée du menu de REVO n'est pas dans le code** :
   il vient des ressources. Les dix identifiants sont lus, leur **texte**
   dépend de `string_array` et de la liste que l'hôte résout.
5. **La destruction d'objets AET à l'ouverture d'une page fille manque**, et
   ce n'est **pas** un décalage de libellé : « MAIN MENU » transparaît sous
   « SCOREBOARDS » et les deux légendes se superposent. Vu à l'écran, non
   corrigé, à traiter séparément.
6. **Le désassemblage n'est pas une décompilation.** Les 25 `.asm` d'APM3 et
   les 9 de REVO déposés ici donnent les instructions, les bornes exactes et
   les cibles d'appel ; ils ne donnent **pas** la structure. Pour la
   structure il faut Ghidra, et il faut ouvrir le bon projet :
   `VF5RE/ghidra/vf5fs_apm3.gpr` pour APM3,
   `VF5RE/ghidra/vf5fs_revo.gpr` pour REVO. **Je ne l'ai pas fait** : la
   mission l'interdit, et des verrous du 16 novembre traînent
   (`vf5fs_apm3.lock.orphelin_419363`, `…419395`).
7. **Les 11 fonctions d'APM3 de `VF5RE/desassemblages/APM3_A_VIDER.txt` ne
   sont toujours pas vidées dans Ghidra** : `FUN_180064000`,
   `FUN_18007DDA0`, `FUN_1800DDA80`, `FUN_18018C2F0`, `FUN_1801DE340`,
   `FUN_18022CE10`, `FUN_180239300`, `FUN_18023F6A0`, `FUN_180240AC0`,
   `FUN_1802411B0`, `FUN_18063DC60`. Deux d'entre elles sont nommées
   aujourd'hui : `0x1801DE340` est `TaskMenuTerminal::validate` (déposée
   dans `menus/apm3/terminal_valider.asm`), et `0x18023F6A0` est le
   créneau [3] de `apm3TestMode::MenuTop`.
8. **Rien ici n'est mesuré à l'écran.** Tout est lu dans les deux fichiers.
   La seule chose de ce dossier qui ait jamais été vue par Frédéric est le
   menu principal de REVO avec ses dix lignes (`MENU.md` §419.91) et le
   sous-menu DOJO corrigé (§419.94).

---

## 7. COMMENT REJOUER CE RELEVÉ

Les trois outils de cette séance vivent dans le bac à sable de la séance ;
ce dossier **est** le résultat. Les outils du chantier qu'ils appellent sont,
eux, permanents :

```
py -3 VF5RE/tools/rtti.py --pe <module> --out <sortie>    classe <-> vtable
py -3 VF5RE/tools/vtable.py 0x<deb> 0x<fin>               les créneaux, APM3
py -3 VF5RE/tools/bornes.py 0x<va>                        les bornes .pdata
py -3 VF5RE/tools/pe_disasm.py <module> func 0x<va>       le désassemblage
py -3 VF5RE/tools/apparier_fonctions.py <a> <va> <b> <vb> l'appariement octet
py -3 VF5RE/oracle_desassembler.py --apm3 0x<va>          APM3, sans Ghidra
```

`apparier_fonctions.py` a été essayé sur l'ancre
`TaskSelector::update` (APM3 `0x18016C570` ↔ REVO `0x18017AE30`) : l'ancre
s'apparie **à l'octet** après normalisation des déplacements relogeables, et
elle retrouve `Selecteur_EscalierChoix` (`0x18016C9C0` ↔ `0x18017B280`) —
mais **aucune** des quinze autres voisines. Le rendement est faible : les
deux builds ont trop divergé. **C'est le RTTI qui apparie, pas les octets.**
