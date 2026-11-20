# Les transitions de sous-états du mode TERMINAL — la Xbox 360 comme oracle

Déposé le 2026-11-19. **Rien n'a été lancé** : ni `vfes.exe`, ni `VFREVO.exe`,
ni aucune course. Tout ce qui suit a été lu **dans le fichier** des deux
images, en lecture seule :

- `FS APM3/binaires/vf5fs-pxd-w64-Retail_APM3.dll.origine`
  (md5 `3214e19696deed80e9da8e54f5e6afe8`, identique à la copie de `banc/`)
- l'image Xbox 360 de VF5FS (PE PowerPC gros-boutiste, base `0x82000000`)
- pour les contre-épreuves à trois builds : la DLL REVO.

**Un désassemblage n'est pas une décompilation.** Ce qui est déposé dans
`FS APM3/desassemblage/terminal/` est du **désassemblage** commenté, pas du C.
Aucune fonction n'a été décompilée ici.

Les relevés : `FS APM3/desassemblage/terminal/` — 11 fichiers, aucun écrasement
(le dossier était vide avant).

---

## 1. L'état des lieux — ce qui était déjà nommé, ce qui ne l'était pas

### 1.1 Déjà nommé et mesuré dans le projet (avant ce travail)

Côté **APM3**, le chemin d'entrée du TERMINAL était établi et mesuré :

| source | ce qu'elle donnait déjà |
|---|---|
| `VF5RE/PROMPT_TERMINAL_ET_QUEST.md` | entrée 4 TERMINAL du menu principal (libellé `0x17C`), vtable `TaskMenuTerminal` `0x180532A28`, `draw 0x1801E1B10` {`0x299` Customize, `0x29A` Replays}, `validate 0x1801DE340` et ses deux gardes, l'appel `0x1800DA9A0(5)` + `0x1800DA9C0(37)`, puis entrée `0x1801E50B0` → `0x1801C5B00` → `0x1801C46F0`, milieu `0x1801E4ED0` → séquenceur `0x1801C4D60` (pas 0, 1, 10 « CUST_MAIN », 11 BGM, 12 attente, 40 → mode 4 MENU), sortie `0x1801E4FF0` → `0x1801C5140`. Et le défaut d'entrée connu : bits 8, 11, 20-23 sans source, `0x180243ED0` ne remplissant que 0-7, 9, 12-19. |
| `FS APM3/desassemblage/MENUS_INDEX.md` | `Etat_RepartiteurDesPhases 0x1800DA550`, `Etat_DemanderUnMode 0x1800DA9A0`, `MenuMain_EntrerLeSousEtat 0x1800DCCA0`, `TaskMenuTerminal::validate 0x1801DE340`, `Tache_CreerParNom 0x180245830`, `Tache_DetruireParObjet 0x1802450A0`, `Entree_LireTenu 0x1801A2CA0`, `Entree_LecteurDuMoteur 0x180243ED0`, `0x180753818 = TaskMenuMain*`, plus le piège `.pdata` et ses trois contrôles publiés. |
| `…/menus/notes/TABLE_DES_SCENES_APM3_VS_REVO.md` | la table des **sous-états** d'APM3 en entier : 55 entrées de 32 o à `0x1803A05A0`, dont 37 `CS_TERM_CUSTOMIZE` = `0x1801E50B0` / `0x1801E4ED0` / `0x1801E4FF0`, et 38/39/40 tous trois = `0x1801E50A0` / `0x1801E4EC0` / `0x1801E4FE0`. |
| `…/menus/notes/rtti_apm3.txt` | les vtables du terminal par le RTTI : `TaskMenuTerminal 0x180532A28`, `TaskMenuCustomize 0x18052FCF8`, `TaskCustomizeMenu 0x180530420`, `TaskSelItemMenu 0x1805304E0`, `TaskSelPartMenu 0x180530540`, `CharSelector 0x180530F30`, `DataSelector 0x180530F90`, `TaskDataSelector 0x180530FF0`, `customize::ItemMain 0x18052FA80`, `customize::ItmEqTask 0x180530D10`. |
| `…/menus/VTABLES_MENUS_APM3_VS_REVO.txt` | les vtables APM3 ↔ REVO créneau par créneau. |

### 1.2 Ce qui n'était **pas** nommé — et que ce travail a mesuré

1. **Toute la machine à états de la Xbox 360.** Aucune note du projet ne
   nommait une seule fonction de transition côté console. Les seules
   adresses `0x82…` publiées concernaient le LZX, la pierre de Rosette des
   champs et quelques vtables de pages de personnalisation.
2. **La table des MODES d'APM3** (`0x1803A0190`).
   `TABLE_DES_SCENES_APM3_VS_REVO.md` §7.1 la portait noir sur blanc en
   « pas encore cherchée ». Elle est lue en entier ici.
3. **Les trois sous-états de lecture** `CS_TERM_REPLAY_PLAY`,
   `CS_TERM_LAST_PLAY`, `CS_TERM_CLIP_PLAY` : la table les donnait comme
   « trois fois les mêmes fonctions », sans que ces fonctions soient suivies.
   `PROMPT_TERMINAL_ET_QUEST.md` §3.4 disait explicitement que `Replays`
   (`0x29A`) n'avait jamais été tracé.
4. **Les deux gardes de sortie du mode CS_TERM** (`0x1801B6E40`,
   `0x1801B6FE0`) : jamais nommées, et c'est là qu'est le défaut principal
   (§4.1).
5. **La famille des 19 écrans autorisés du terminal** : inconnue du projet
   des deux côtés.
6. **`TaskMenuTerminal::update`** : le créneau `[2]` était recensé par taille
   dans les vtables, mais son contenu n'avait jamais été lu, ni apparié.

### 1.3 Ce que ce travail **n'a pas** comblé

- Les 19 écrans ne sont pas nommés **un par un** (seul le mécanisme l'est).
- `CARD`, `DATA SELECTOR` et `CHAR SELECTOR` ne sont toujours pas établis
  depuis le code ; la vtable `TaskDataSelector` est seulement **comparée**
  (§4.4), pas tracée.

---

## 2. La machine à états de la Xbox 360

Relevés : `x360_machine_etats.txt`, `x360_csterm_mode5.txt`,
`x360_csterm_sousetats.txt`, `x360_terminal_autorisation.txt`,
`x360_taskmenuterminal_update.txt`, `tables_machine_etats.txt`.

### 2.1 Les fonctions, nommées

| VA | taille | nom proposé | ce qu'elle fait, mesuré |
|---|---|---|---|
| `0x822BE7D0` | 632 o | **`Etat_UnPas`** | la pompe : un pas de mode puis un pas de sous-état, par image. |
| `0x822BE618` | 424 o | **`Etat_PasDeMode`** (SetState) | parcourt la table des modes `0x82063968`, pas `0x58`, borne `0x2C0` → **8 entrées** ; appelle le gestionnaire de phase du mode. |
| `0x822BE518` | 252 o | **`EtatSousEtat_UnPas`** | parcourt la table des sous-états `0x82063C28`, pas `0x14`, borne `0x3AC` → **47 entrées** ; phase lue en `[sgl+0x28]`, gestionnaire = `[desc + 4*(phase+2)]`, soit `+0x08` / `+0x0C` / `+0x10`. |
| `0x822BE458` | — | **`Etat_Singleton`** | rend `0x82A8CFE4`. |
| `0x822BE470` | — | **`Etat_DemanderUnMode`** | `[+0x04]=mode ; [+0x10]=1 ; [+0x2C]=0`. |
| `0x822BE490` | — | **`Etat_DemanderUnSousEtat`** | `[+0x20]=n ; [+0x2C]=1`. |
| `0x822BE4A8` | — | **`Etat_DrapeauDuSousEtat`** | lit `[desc+0x04]`. |
| `0x823ACDC0` | — | **`Taches_AttenteEnCours`** | rend 1 tant qu'une tâche vivante a `[tâche+0x0C] == 3`. **C'est la seule « durée » du système.** |
| `0x821FDCD0` | — | **`Ecran_Fondu`** | appelé avec 0 puis 2 autour de `TaskMenuTerminal::update`. |

**La phase.** Chaque descripteur porte trois gestionnaires. La phase vaut 0
(entrée), 1 (milieu), 2 (sortie), 3 (inerte). Un gestionnaire qui rend
**non nul** fait avancer la phase ; 0 → 1, 1 → 2, et finir la phase 2 rend 1
au cran supérieur, ce qui enchaîne le sous-état suivant de la chaîne du mode.
**Un milieu qui rend FAUX est donc l'état de repos voulu, pas une panne**
(voir §5.2).

**Le singleton** (`0x82A8CFE4` console, `0x18070C4F0` APM3) a la **même
disposition d'octets des deux côtés** — il ne contient aucun pointeur :

```
+0x00 mode courant        +0x1C sous-etat courant
+0x04 mode demande        +0x20 sous-etat demande
+0x08 mode precedent      +0x24 sous-etat precedent
+0x0C phase du mode       +0x28 phase du sous-etat
+0x10 drapeau changement  +0x2C drapeau changement
+0x14 compteur d'images   +0x2D drapeau applique
                          +0x30 compteur d'images
```

**Les descripteurs** (structure lue dans le code qui les **parcourt**, pas
devinée) :

| champ | mode X360 (0x58 o) | mode APM3 (0x68 o) | sous-état X360 (0x14) | sous-état APM3 (0x20) |
|---|---|---|---|---|
| identifiant (clef, pas la position) | `+0x00` | `+0x00` | `+0x00` | `+0x00` |
| drapeau | — | — | `+0x04` | `+0x04` |
| fn_entrée | `+0x04` | `+0x08` | `+0x08` | `+0x08` |
| fn_milieu | `+0x08` | `+0x10` | `+0x0C` | `+0x10` |
| fn_sortie | `+0x0C` | `+0x18` | `+0x10` | `+0x18` |
| chaîne des sous-états, 16 mots, sentinelle MAX | `+0x10` | `+0x20` | — | — |
| mode de retour | `+0x50` | `+0x60` | — | — |

### 2.2 Le mode 5 `CS_TERM` sur la console

```
entree 5  @0x82063B20  mode 5 = CS_TERM
   entree 0x822BEA48   milieu 0x822BEBF0   sortie 0x822BEAE8
   chaine : 36=CS_TERM_CUSTOMIZE -> 37=CS_TERM_REPLAY_PLAY
         -> 38=CS_TERM_LAST_PLAY -> 39=CS_TERM_CLIP_PLAY -> MAX
   mode de retour (+0x50) : 4 = MENU
```

Le **milieu `0x822BEBF0` est partagé avec le mode 6 `CS_TRAINING`** — le même
pointeur dans les deux entrées de table. C'est un fait structurel qui servira
d'ancrage à l'appariement (§3).

### 2.3 Les quatre sous-états du TERMINAL sur la console

```
n   sous-etat               drap fn_entree   fn_milieu   fn_sortie
36  CS_TERM_CUSTOMIZE        1   0x822BEB78  0x822BEC78  0x822BEBB0
37  CS_TERM_REPLAY_PLAY      1   0x822BEBD8  0x822BEBE8  0x822BEBE0
38  CS_TERM_LAST_PLAY        1   0x822BEBD8  0x822BEBE8  0x822BEBE0
39  CS_TERM_CLIP_PLAY        1   0x822BEBD8  0x822BEBE8  0x822BEBE0
```

Les trois sous-états de lecture partagent **les mêmes trois fonctions**, qui
sont des **relais d'une instruction** :
`0x822BEBD8 → 0x82216290`, `0x822BEBE8 → 0x822163B0`,
`0x822BEBE0 → 0x822164E8`.

### 2.4 Ce qui déclenche chaque passage, et les « durées »

**Il n'y a aucun compteur d'images dans ces transitions.** Les déclencheurs
mesurés, dans l'ordre de la chaîne :

1. **MENU → CS_TERM** : `TaskMenuTerminal::validate` demande le mode 5 puis
   le sous-état 36. C'est un **appui**, pas un délai.
2. **Entrée du mode (`0x822BEA48`)** : teste si le sous-état demandé est dans
   `0x25..0x27` (37..39) ; si oui elle crée la tâche nommée
   **`"REPLAY_SCORE"`** (chaîne à `0x820640A8`) ; sinon elle laisse passer
   vers `CS_TERM_CUSTOMIZE`.
3. **`CS_TERM_CUSTOMIZE`, entrée `0x822BEB78`** : crée la tâche
   **`"CUSTOMIZE MENU"`** (chaîne à `0x82010ACC`) par
   `Tache_CreerParNom` (`0x823AD378`), via `0x8222C970`.
4. **`CS_TERM_CUSTOMIZE`, milieu `0x822BEC78`** : appelle
   `0x821F7D00([page+0x116])` — « cet écran du terminal est-il autorisé ? » —
   et **retombe sur le MENU quand il ne l'est pas**. C'est la transition qui
   nous intéresse : voir §4.2.
5. **Sortie du mode (`0x822BEAE8`)** : détruit la tâche par
   `Tache_DetruireParObjet` (`0x823AC6F8`), puis **attend** —
   `Taches_AttenteEnCours` (`0x823ACDC0`) tient la phase tant qu'une tâche
   vivante porte `[tâche+0x0C] == 3`. **La « durée » d'une transition est
   cette attente, pas un nombre d'images.**
6. **Retour au titre** : `0x82214550` consomme `[terminal+0xA13E]` (demande de
   titre) ; **retour au menu** : `0x822145A0` consomme `[terminal+0xA13F]`.
   Les deux sont des **drapeaux posés ailleurs puis consommés**, donc des
   faits du jeu, pas des délais.

### 2.5 La famille des 19 écrans autorisés (console)

Objet terminal à `0x829AAA68`. Masque global en `terminal+0xA004`, créneaux
par joueur en `terminal+0x9FF8`.

| VA | taille | appelants | rôle mesuré |
|---|---|---|---|
| `0x82214FE8` | — | — | **`Terminal_EcranAutorise(index, joueur)`** : refuse `index >= 0x13` (19), puis lit le masque. |
| `0x821F7D00` | 92 o | 11 | un écran, en tenant compte du fondu. |
| `0x821F8108` | 124 o | 4 | **les 19** sont-ils tous autorisés ? |
| `0x821F8188` | 124 o | 3 | **au moins un** est-il autorisé ? |
| `0x8222C9F0` | — | — | donne l'index d'écran depuis une table de 150 fiches de `0x80` o, champ `+0x29` ; **défaut `0x15` = 21, délibérément hors des 19**. |
| `0x82214520` / `0x82214538` | — | — | poser / lire « terminal actif » (`terminal+0xA13D`). |

---

## 3. L'appariement avec APM3 — et sur quoi il est fondé

Relevés : `apm3_machine_etats.txt`, `apm3_csterm_mode5.txt`,
`apm3_csterm_sousetats.txt`, `apm3_terminal_gardes.txt`,
`apm3_taskmenuterminal_update.txt`.

**Aucun appariement ci-dessous ne repose sur une ressemblance de nom.** Les
deux builds ne portent aucun symbole. Les quatre fondements utilisés sont :
(a) une **chaîne littérale identique**, (b) une **constante ou un déplacement
de champ** identique, (c) la **structure du graphe d'appels** (même position
dans la même table, même partage de pointeur entre deux entrées), (d) la
**correspondance instruction par instruction**.

### 3.1 Le cœur de la machine

| rôle | Xbox 360 | APM3 | fondement |
|---|---|---|---|
| singleton | `0x822BE458` → `0x82A8CFE4` | `0x1800DA7E0` → `0x18070C4F0` | (b) **même disposition d'octets** du singleton, champ par champ ; la structure ne contient aucun pointeur, donc aucun décalage x64. |
| demander un mode | `0x822BE470` | `0x1800DA9A0` | (b) la **même séquence d'écritures** : `[+0x04]=arg`, `[+0x10]=1`, `[+0x2C]=0`. Trois déplacements, trois valeurs, même ordre. |
| demander un sous-état | `0x822BE490` | `0x1800DA9C0` | (b) `[+0x20]=arg`, `[+0x2C]=1`. |
| la pompe | `0x822BE7D0` + `0x822BE518` | `0x1800DA550` (644 o, **le pas de sous-état est inliné**) | (b) mêmes bornes de table lues dans le code : pas `0x14`/`0x20`, `cmp ecx,3` pour la phase inerte, MAX sous-état `0x37`. |
| pas de mode (SetState) | `0x822BE618` | `0x1800DA800` (405 o) | (b) `mov eax,[rax+0x60]` y range le **mode de retour** — ce qui **prouve** que `+0x60` d'APM3 est le `+0x50` de la console. |
| attente de tâche | `0x823ACDC0` | `0x180244F20` | (c) appelée au même endroit dans les deux sorties de mode, même test `[tâche+0x0C] == 3`. |

### 3.2 Le mode 5 et ses sous-états

```
APM3  entree 5  @0x1803A0398  mode 5 = CS_TERM
   entree 0x1801E5010   milieu 0x1801E4E60   sortie 0x1801E4F60
   chaine : 37=CS_TERM_CUSTOMIZE -> 38=CS_TERM_REPLAY_PLAY
         -> 39=CS_TERM_LAST_PLAY -> 40=CS_TERM_CLIP_PLAY -> MAX
   mode de retour (+0x60) : 4 = MENU
```

| rôle | Xbox 360 | APM3 | fondement |
|---|---|---|---|
| entrée du mode 5 | `0x822BEA48` | `0x1801E5010` (129 o) | (b) la console teste l'intervalle `0x25..0x27`, APM3 teste `0x26..0x28` par `add ecx,-0x26 ; cmp ecx,2 ; ja` — **les mêmes trois noms de sous-états**, décalés de 1 (§3.4) ; (a) les deux créent la tâche **`"REPLAY_SCORE"`** (`0x820640A8` console, `0x180532AD0` APM3 — **chaîne identique au caractère**). |
| milieu du mode 5 | `0x822BEBF0` | `0x1801E4E60` (96 o) | (d) **instruction par instruction** ; (c) **les deux sont aussi le milieu du mode 6 `CS_TRAINING`** dans la table des modes de leur build — un partage de pointeur qui ne peut pas être une coïncidence. |
| sortie du mode 5 | `0x822BEAE8` | `0x1801E4F60` | (c) même position de table, même appel à la destruction de tâche puis à l'attente. |
| `CUSTOMIZE` entrée | `0x822BEB78` | `0x1801E50B0` (54 o) | (a) tâche **`"CUSTOMIZE MENU"`** créée des deux côtés ; APM3 ajoute un `call 0x180087260(0x4F, 8)` que la console n'a pas. |
| `CUSTOMIZE` milieu | `0x822BEC78` | `0x1801E4ED0` (131 o) | (d) même squelette ; la divergence est au §4.2. |
| `CUSTOMIZE` sortie | `0x822BEBB0` | `0x1801E4FF0` (24 o) | (c) même position. |
| les trois lectures | `0x822BEBD8`/`BE8`/`BE0` → `0x82216290`/`163B0`/`164E8` | `0x1801E50A0`/`4EC0`/`4FE0` → `0x1801BA8E0`/`BA770`/`BA880` | (c) **même forme exacte** : trois relais d'une instruction partagés par les trois sous-états de lecture, dans les deux tables. |

### 3.3 `TaskMenuTerminal::update` — APM3 `0x1801DD7A0` (543 o) ↔ X360 `0x822B5AF8` (604 o)

Apparié par (c) **le même créneau `[2]` de la vtable de la même classe
nommée par le RTTI des deux images**, puis confirmé par (d). Les champs se
correspondent ainsi :

| APM3 | X360 | ce que c'est |
|---|---|---|
| `+0x240` | `+0x1C4` | — |
| `+0x298` | `+0x1FC` | — |
| `+0x2F0` / `+0x2F1` | `+0x234` / `+0x235` | — |
| **`+0x2F8`** | **`+0x238`** | **le pointeur vers l'écran de terminal ouvert — la vraie variable de sous-état du TERMINAL** |
| `+0x58` | `+0x4C` | le curseur |

Libellés et constantes communs aux deux : `0x5A0C`, `0xD`,
`0xE1`/`0xE2`/`0xE3`, et les valeurs d'état 3 et 6.
Fonctions appelées, appariées indépendamment :
`0x1802450A0 ↔ 0x823AC6F8` (destruction de tâche, déjà nommée par une autre
route), `0x180244F90 ↔ 0x823AC598` (tâche vivante),
`0x1801BBBE0 ↔ 0x82217B30` (**la pierre de Rosette déjà publiée** du projet).

Autre paire, fondée sur (b) : `0x1800D41E0(obj,n)` = `[obj+0x58]=n ; si n∈{1,2} [obj+0x64]=1`
↔ `0x822A5168` = `[obj+0x4C]=n ; si n∈{1,2} [obj+0x58]=1` ; objet
`[0x18039F560]` (statiquement `0x18070AFD0`) ↔ `[0x82061E84]` ; les deux
appelés avec le littéral 3 dans le milieu de la lecture. Et l'entrée :
`0x1801A2CA0(8,0)` et `(1,0)` ↔ `0x821FE420(8,0)` et `(1,0)`, même compteur
modulo 4.

### 3.4 Le décalage de numérotation — mesuré, pas supposé

`CS_TERM` est le **mode 5** dans les deux builds. Mais
`CS_TERM_CUSTOMIZE` est le sous-état **36** sur la Xbox 360 et **37** sur
APM3. L'écart vient de **`CS_DEMO`, inséré à l'index 6** dans le build
arcade — visible dans la chaîne du mode 0 d'APM3
(`0 → 1 → 6=CS_DEMO → 3 → 4 → 2 → 5`) là où la console fait
(`0 → 1 → 3 → 4 → 2 → 5`). Tous les sous-états au-delà de 5 sont donc
décalés de +1. REVO les décale encore (41-44).

Tailles des tables, mesurées :

| build | sous-états | pas | modes | pas |
|---|---|---|---|---|
| Xbox 360 | **47** à `0x82063C28` | `0x14` | **8** à `0x82063968` | `0x58` |
| APM3 | **55** à `0x1803A05A0` | `0x20` | **10** à `0x1803A0190` | `0x68` |
| REVO | 73 | — | — | — |

---

## 4. Les écarts qui expliqueraient des transitions « buggées »

### 4.1 Le plus grave : le retour au MENU depuis CS_TERM est du code mort dans APM3

`0x1801B6E40` est la garde « un retour au menu est-il demandé ? », jumelle de
la console `0x822145A0` qui ne fait que **consommer** `[terminal+0xA13F]`.
Dans APM3 elle contient :

- deux appels à `0x180029FB0` — le **bouchon TOUJOURS VRAI** (`mov al,1 ; ret`) ;
- un appel à `0x180244EA0` ;
- et un dernier `call 0x180007450` — le **bouchon TOUJOURS FAUX** — qui garde
  le **seul** `mov al,1` de la fonction, à `0x1801B6E97`.

J'ai vérifié par programme que **`0x1801B6E97` n'est la cible d'aucun saut
interne** à la fonction : les seules cibles internes sont `0x1801B6E8E` et
`0x1801B6E9E`. Le seul chemin vers ce `mov al,1` est donc la chute après un
résultat toujours nul.

> **`0x1801B6E40` ne peut jamais rendre 1.** Par conséquent le
> `mov ecx,4 ; call 0x1800DA9A0` (mode 4 = MENU) situé à `0x1801E4E8E` dans le
> milieu de `CS_TERM` est **inatteignable**.

En regard, `0x1801B6FE0` (garde du retour au **titre**, jumelle de
`0x82214550`) est **intacte**. D'où le symptôme : **CS_TERM ne peut sortir que
vers le mode 0 + sous-état 3 (`CS_TITLE`)** ; il ne revient jamais au MENU
comme sur la console.

**Ce qu'il faudrait changer** : rendre à `0x1801B6E40` un corps qui consomme
un drapeau, comme `0x822145A0` le fait avec `[terminal+0xA13F]` —
c'est-à-dire remplacer l'appel au bouchon FAUX par la lecture-et-remise-à-zéro
d'un octet de demande. Le `+0xA13F` d'APM3 n'est pas localisé (§6).

### 4.2 La deuxième branche du milieu de `CS_TERM_CUSTOMIZE` est morte aussi

Là où la console fait, dans `0x822BEC78` :

```
appel 0x821F7D00([page+0x116])     ; cet ecran est-il autorise ?
si NON -> retour au MENU, et remise a zero de l'ecran ouvert
```

APM3, dans `0x1801E4ED0`, appelle `0x180029FB0` — **toujours VRAI** — et le
`jne` qui suit est **toujours pris**. Donc le build arcade **ne refuse jamais
un écran de terminal** et **ne remet jamais `[this+0x2F8]` à zéro**. Un écran
interdit reste « ouvert » du point de vue de la tâche : c'est exactement la
forme d'une transition qui « reste collée ».

### 4.3 Toute la famille des 19 écrans a été remplacée par le bouchon VRAI

Corroboré par des **comptes d'appels qui concordent** sur cinq paires de
fonctions appariées indépendamment (et non par une ressemblance de nom) :

| paire | X360 | APM3 | appels à la garde |
|---|---|---|---|
| `TaskMenuTerminal::update` | `0x822B5AF8` | `0x1801DD7A0` | 2 ↔ 2 |
| `TaskMenuTerminal::draw` | `0x822B8AF0` | `0x1801E1B10` | 1 ↔ 1 |
| milieu `CS_TERM_CUSTOMIZE` | `0x822BEC78` | `0x1801E4ED0` | 1 ↔ 1 |
| `TaskRobSingle::update` (paire déjà nommée par le projet) | `0x82356840` | `0x180151CF0` | 1 ↔ 1 |
| milieu du mode GAME | `0x822C05D8` | `0x1800DA9D0` | 1 ↔ 1 |
| zone `TaskSelChara` | `0x8237A1A0` / `0x8237A660` | `0x18016E390` / `0x18016F0D0` | 2 et 2 ↔ 2 et 2 |

Comptes de sites d'appel des bouchons, mesurés en balayant `.text` pour
`call rel32` (APM3) et `bl` (console) :

| bouchon | APM3 | sites | Xbox 360 | sites |
|---|---|---|---|---|
| VRAI | `0x180029FB0` | **71** sur **45** fonctions | `0x82646398` | **43** |
| FAUX | `0x180007450` | **210** | `0x824CB790` | **260** |
| vide | `0x180007430` | **577** | `0x82217598` | **692** |
| rend 0 | `0x180007440` | **117** | — | — |

### 4.4 Deux divergences arcade/console à instruire plus tard

Comparaison de vtable, créneau par créneau (`tables_machine_etats.txt`).
Sur `TaskMenuTerminal` les tailles concordent à quelques pour cent sur
**tous** les créneaux :

| créneau | APM3 `0x180532A28` | taille | X360 `0x820632A8` | taille |
|---|---|---|---|---|
| `[0]` | `0x1801DB270` | 94 o | `0x822BBA38` | 80 o |
| `[1]` | `0x1801E4300` | 279 o | `0x822B59D0` | 292 o |
| `[2]` | `0x1801DD7A0` | 543 o | `0x822B5AF8` | 604 o |
| `[3]` | `0x1801A82D0` | 46 o | `0x822B4AA8` | 64 o |
| `[4]` | `0x1801E1B10` | 812 o | `0x822B8AF0` | 760 o |

Mais deux classes voisines décrochent, et dans le **sens inverse** de ce
qu'on attendrait d'un build appauvri :

- **`TaskDataSelector`** `[1]` **1087 o** (APM3) contre **260 o** (console),
  `[2]` **971 o** contre **220 o** — le lecteur de carte / VF.NET, bien plus
  gros côté arcade.
- **`TaskMenuCustomize`** `[4]` **910 o** contre **116 o**.

Ce ne sont pas des bouchons : ce sont des **implémentations arcade
différentes**. Elles n'ont pas été lues ici.

---

## 5. Corrections à apporter à des notes existantes

### 5.1 Le piège `.pdata` d'APM3 — deux fichiers du projet sont faux

Le chaînage des entrées `.pdata` ne se déduit **pas** de l'adjacence. Il faut
lire la `RUNTIME_FUNCTION` que l'`UNWIND_INFO` range **après** les codes de
déroulement, à l'offset `4 + 2*((CountOfCodes+1) & ~1)`, quand le drapeau
`UNW_FLAG_CHAININFO` (`0x4`) est posé : une suite **nomme** son primaire.

Preuve structurelle autour de `0x1801BBBE0` : entrées
`0x1801BBBE0..C05` (primaire), `C05..D01` (primaire `0x1801BBBE0`),
`D01..D3D` (primaire `0x1801BBBE0`), puis **nouveau primaire**
`0x1801BBD40..D5F` ; et l'octet en `0x1801BBD3C` est `c3` (`ret`).

Conséquences :

1. **`FS APM3/desassemblage/menus/VTABLES_MENUS_APM3_VS_REVO.txt` ne donne que
   la longueur du premier fragment.** Exemples mesurés :
   `TaskCsMenu::update` y est noté « 37 o » — elle fait **349 o** ;
   `TaskDataSelector[2]` « 16 o » — **971 o**.
2. **`FS APM3/desassemblage/repartiteur_curseur.txt` annonce 384 o et
   dépasse donc de 35 octets** dans la fonction suivante
   (`0x1801BBD40`).

Les trois contrôles publiés dans `MENUS_INDEX.md` §3 passent toujours avec la
règle corrigée (`0x1801E17A0` = 880 o, `0x1800DCCA0` = 16 o,
`0x1801DDF30` finissant en `0x1801DE1E3`).

### 5.2 `machine_console.md` §3 — l'affirmation est à retirer

La note appelle le milieu bouchonné de `MENU_MAIN` « la cause profonde du
*menu qui s'affiche mais ne fait rien* ». **C'est faux** : le build **retail
Xbox 360 fait exactement pareil** — sous-état 35 `MENU_MAIN`, milieu
`0x824CB790`, le bouchon FAUX. REVO aussi (`0x18000BA20`). Un milieu qui rend
FAUX est **l'état de repos conçu**, ce que `MENUS_INDEX.md` dit déjà pour
REVO.

### 5.3 `machine_etats.md` §2 — « il journalise » est à qualifier

J'ai d'abord pris `0x824CB790` pour un `printf`, parce que `SetState`
l'appelle avec un format et deux noms. Correction : `0x824CB790` est
`li r3,0 ; blr`, le **bouchon FAUX** de la console (260 sites). Donc le
journal d'états `"[%s]->[%s]\n"` est **inerte sur Xbox 360 aussi**, et son
équivalent APM3 `0x180215580` est un variadique vide
(`[rsp+0x18]=r8 ; xor eax,eax ; [rsp+0x20]=r9 ; ret`).

### 5.4 Un nom de vtable à corriger côté console

`documentation/x360_fs.md` §4 et `desassemblage/README.md` étiquettent la
vtable `0x82010F5C` / la fonction `0x82231A50` comme la page « part ». Le
**RTTI** (produit trois jours plus tard) dit que `0x82010F5C` est
**`TaskSelItemMenu`** ; `TaskSelPartMenu` est **`0x82010F88`**
(`[1]` `0x822359C8`, `[2]` `0x82235AA8`, `[4]` `0x82231700`).

### 5.5 Deux affirmations du projet, l'une confirmée, l'autre élargie

- **Confirmée par un troisième build** : les quatre sous-états `*_TERMINAL` et
  les 15 `DATA_TEST_*` sont bouchonnés **sur Xbox 360 aussi**
  (`TABLE_DES_SCENES` §4 avait raison).
- **Élargie** : les six `ONLINE_*` sont **réels sur la Xbox 360** (mode 7
  entrée `0x822C2270`, milieu `0x822C1568`, sortie `0x822C2368`), alors que
  le mode 7 est **entièrement bouchonné dans APM3** et dans REVO.
- Bilan des tables : Xbox 360 **22 sous-états réels / 25 bouchonnés** ;
  APM3 **24 réels / 31 bouchonnés**. Modes bouchonnés : console 2
  (`ADVERTISE`, `DATA_TEST`), APM3 3 (`ADVERTISE`, `DATA_TEST`, `ONLINE`).

---

## 6. Ce qui n'a **PAS** été vérifié

1. **Rien n'a été lancé et rien n'a été mesuré à l'écran.** Aucune course,
   aucun `vfes.exe`, aucun `VFREVO.exe`, aucune lecture de processus. Tout est
   statique. **C'est l'écran qui tranche** : aucune des conclusions du §4
   n'est confirmée par une image.
2. **Un désassemblage n'est pas une décompilation.** Les 11 fichiers déposés
   sont du désassemblage annoté. Aucun code C n'a été reconstruit, et aucune
   des fonctions nommées ici n'a été décompilée.
3. **L'identité** — par opposition à la correspondance de **position** — entre
   chaque site `0x180029FB0` d'APM3 et une fonction console précise qui a été
   retirée **n'est pas prouvée**. Je prouve que le bouchon est là, à la place
   d'un appel que la console fait ; je ne prouve pas que c'est *la même*
   fonction qui a été remplacée.
4. **Les 19 écrans ne sont pas nommés un par un.** Seul le mécanisme
   (index, masque, créneau joueur, défaut 21) est mesuré.
5. **Le rôle de `[page+0x116]`** (l'index passé à la garde), celui des champs
   `+0x5C` / `+0x60` du descripteur de mode d'APM3, et celui de `+0x58` de
   l'objet `[0x18039F560]` **pour cette classe** ne sont pas établis.
6. **Le `+0xA13F` d'APM3 n'est pas localisé.** La correction proposée au §4.1
   dit quelle **forme** doit prendre `0x1801B6E40`, pas quelle adresse lire.
7. **Contradiction non tranchée entre deux notes du projet** sur
   `0x1801A2CA0` : `PROMPT_TERMINAL_ET_QUEST.md` §3.2 en fait le lecteur de
   **front** prenant un **masque**, `MENUS_INDEX.md` §3.2 bis le nomme
   `Entree_LireTenu` (tenu). Les sites que j'ai mesurés passent de petits
   **codes** (8 et 1) et le retour est comparé en **signé** — ce qui ne
   départage pas les deux notes. Je ne l'ai pas résolu.
8. **Le `.pdata` PowerPC n'a pas été examiné pour un chaînage** analogue à
   celui du x64. Les tailles console sont donc des longueurs d'entrée simple.
   Contrôles positifs passés : `0x821A0568` à l'octet près contre l'écart à
   l'entrée suivante, et les comptes publiés pour `0x82217B30`,
   `0x82230818`, `0x82229750` ; contrôle négatif passé :
   `0x82217B34` correctement refusé comme non-début de fonction.
9. **Les divergences du §4.4** (`TaskDataSelector`, `TaskMenuCustomize`) n'ont
   pas été lues : seules leurs tailles sont comparées.
10. **Aucune correction n'a été appliquée.** Rien n'a été reconstruit, aucun
    fichier de `VF5RE/tools/` n'a été touché, et les notes fautives citées au
    §5 n'ont **pas** été modifiées — elles sont seulement signalées ici.

---

## 7. Résumé, avec les comptes mesurés

- **Table des modes** : Xbox 360 **8** entrées de `0x58` à `0x82063968`
  (2 bouchonnées) ; APM3 **10** entrées de `0x68` à `0x1803A0190`
  (3 bouchonnées). **Cette table d'APM3 n'avait jamais été lue** —
  `TABLE_DES_SCENES_APM3_VS_REVO.md` §7.1 la portait en « reste à mesurer ».
- **Table des sous-états** : Xbox 360 **47** entrées de `0x14`
  (**22 réelles / 25 bouchonnées**) ; APM3 **55** de `0x20` (24 / 31) ;
  REVO **73**.
- **`CS_TERM` = mode 5 des deux côtés** ; `CS_TERM_CUSTOMIZE` = **36**
  console / **37** APM3, l'écart venant de `CS_DEMO` inséré à l'index 6.
- **9 fonctions console nommées** pour la machine à états, **6 pour la
  famille des 19 écrans**, **plus les 12 fonctions du mode 5 et de ses
  sous-états** ; **21 paires APM3 ↔ Xbox 360** établies sur chaîne,
  constante, structure de table ou correspondance instruction par
  instruction.
- **2 branches mortes trouvées dans APM3**, toutes deux sur le chemin de
  sortie du TERMINAL : `0x1801B6E40` (retour au MENU, **jamais 1**, prouvé par
  l'absence de saut interne vers `0x1801B6E97`) et le refus d'écran dans
  `0x1801E4ED0` (garde remplacée par le bouchon VRAI).
- **5 paires de fonctions** aux **comptes d'appels identiques** (2↔2, 1↔1,
  1↔1, 1↔1, 1↔1) établissent que la famille d'autorisation des 19 écrans a
  été remplacée en bloc par le bouchon VRAI dans APM3.
- **Sites de bouchon** : APM3 VRAI **71** sur **45** fonctions, FAUX **210**,
  vide **577**, rend-0 **117** ; Xbox 360 VRAI **43**, FAUX **260**,
  vide **692**.
- **5 notes du projet à corriger** (§5), dont **2 fichiers de tailles de
  fonction faux** à cause du chaînage `.pdata` (`VTABLES_MENUS_APM3_VS_REVO.txt`,
  `repartiteur_curseur.txt`).
- **11 fichiers déposés** dans `FS APM3/desassemblage/terminal/`, **2 615
  lignes** et 144 ko en tout, aucun écrasement (le dossier était vide).
- **0 course, 0 jeu lancé, 0 fichier du projet modifié** hors cette note et
  les 11 relevés.
