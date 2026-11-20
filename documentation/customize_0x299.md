# Le libellé 0x299 « Customize », et la fonction 0x180227790

Écrit le 2026-09-05. Binaire lu : `runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll.origine`
(PE MSVC x64, base `0x180000000`). **Lecture seule** : rien n'a été patché, le
jeu n'a pas été lancé.

Ce document répond à deux demandes distinctes de Frédéric :

1. désassembler le chemin du libellé `0x299` = `Customize` ;
2. désassembler `0x180227790`.

*Spoiler du point 2, écrit tout de suite pour qu'on ne le cherche pas : les deux
sujets **n'ont rien à voir**. `0x180227790` n'est pas dans le chemin Customize.*

---

## 0. Ce que les documents existants établissaient déjà

Pour ne pas refaire, et pour dire ce que j'ajoute.

* `analysis/carte_customize.md` — carte automatique de la zone
  `0x1801C0000`-`0x1801D2000` (312 fonctions, 68 363 octets). Elle établit **la
  géographie** de l'écran de personnalisation : qui appelle qui *dans la zone*,
  les chaînes nommées (`CUST_MAIN`, `CUST_EQUIP`, `CUSTOM MENU`, `COSTUME MENU`,
  `SEL ITEM MENU`, `SEL PART MENU`, `CUSTOMIZE MENU`, `EXCLUSIVE WARNING`,
  `POINT OVER WARNING`, `ERASE_CONFIRM`, `FULL NOTICE`, `CARD SELECTOR`,
  `DATA SELECTOR`, `CHAR SELECTOR`, `rom/sound/bgm/vfes_bgm_cus.adx`), et les
  bouchons appelés. Elle ne dit **ni** qui ouvre cet écran, **ni** par quel
  libellé, **ni** si le chemin est complet. C'est une carte, pas un itinéraire.
* `analysis/menu_console.md` §8.4 — « TERMINAL | `TERMINAL MENU` | Customize
  (0x299), Replays (0x29A) ». Le fait est posé, sans le code à l'appui.
* `analysis/menu_console.md` §12.1 — attribue le dessin du TERMINAL à
  `0x1801E17A0` et la mise à jour à `0x1801DD6A0`. **C'est faux, et je le
  corrige en §1.3 ci-dessous** (ce sont les créneaux de `TaskMenuScoreAttack`).
* `analysis/couverture_console.md` §3 — « **`0x180227790`, 7373 octets, aucune
  chaîne, jamais nommée.** La plus grosse fonction de la surface console qu'on
  n'a jamais ouverte. » C'est exactement la commande du point 2.
* `analysis/parente_console.md` / `machine_console.md` — sous-état **37
  `CS_TERM_CUSTOMIZE`** existe dans la table des sous-états.
* `analysis/mode_selector.md` — mode **5 `CS_TERM`**, table `0x1803A0398`,
  parcours `CUSTOMIZE → REPLAY_PLAY → LAST_PLAY → CLIP_PLAY`.

Ce que j'ajoute : le **code**, site par site, du libellé jusqu'à la demande de
sous-état, plus le désassemblage de `0x180227790`.

---

## 1. Le libellé 0x299

### 1.1 Sa valeur, vérifiée

    py -3 tools/libelles.py 0x290 0x2A5
      0x299  'Customize'
      0x29A  'Replays'

### 1.2 Balayage linéaire de la valeur `0x299` dans tout le binaire

28 occurrences du motif `99 02 00 00`, dont l'immense majorité sont des faux
positifs (déplacements mal alignés à l'intérieur d'autres instructions). Après
décodage arrière, les porteurs **réels** de l'immédiat `0x299` sont :

| site | instruction | fonction | verdict |
|---|---|---|---|
| `0x1801E1B55` | `mov dword [rbp+0x80], 0x299` | `0x1801E1B10` | **vrai identifiant** |
| `0x1801E1B5F` | `mov dword [rbp+0x84], 0x29A` | `0x1801E1B10` | **vrai identifiant** (`Replays`) |
| `0x1801C5315` | `mov ecx, 0x299` puis `call 0x1801EFD10` | `0x1801C51B0` | **vrai identifiant** (résolveur de texte) |
| `0x18009E7DF`, `0x18009EC40` | `cmp byte [rbx+0x299], 0` | `0x18009E380` | faux positif : décalage de champ |
| `0x1801ABCBD` | `cmp byte [rbx+0x299], 0` | `0x1801ABC40` | faux positif |
| `0x180229A18` | `cmp byte [rbx+0x299], 0` | `0x1802299B0` | faux positif |
| `0x1801E19C1` | `lea rsi, [rdi+0x299]` | `0x1801E17A0` | faux positif |

Autrement dit : **deux endroits** dans les 3,13 Mo du moteur écrivent
réellement l'identifiant `0x299`. Le premier le met dans une table d'entrées de
menu ; le second le donne au résolveur `0x1801EFD10` pour l'écrire à l'écran.

Le dernier faux positif mérite d'être signalé : `0x299` est aussi un **décalage
de champ** dans l'objet « page de menu » (un tableau d'états, un octet par
entrée). C'est très probablement ce qui a fait attribuer à tort le dessin du
TERMINAL à `0x1801E17A0` dans `menu_console.md` §12.1.

### 1.3 La table d'entrées qui porte 0x299 : la page `TaskMenuTerminal`

    0x1801E1B10  mov rax, rsp / push rbp ...          ; prologue
    0x1801E1B52  mov rsi, rcx                         ; rsi = la page
    0x1801E1B55  mov dword [rbp+0x80], 0x299          ; entree 0 = « Customize »
    0x1801E1B5F  mov dword [rbp+0x84], 0x29A          ; entree 1 = « Replays »

La table est **construite sur la pile**, à chaque trame de dessin. Ce n'est pas
une table statique de `.rdata` : c'est pour cela qu'aucun balayage de données
ne la trouvait.

`0x1801E1B10` est le **créneau [4] (dessin)** de la vtable `0x180532A28`, que
`analysis/rtti_apm3.txt` nomme **`TaskMenuTerminal`** :

| créneau | adresse | rôle |
|---:|---|---|
| [0] `0x180532A28` | `0x1801DB270` | destructeur |
| [1] `0x180532A30` | `0x1801E4300` | **entrée** (279 o) |
| [2] `0x180532A38` | `0x1801DD7A0` | **mise à jour** (543 o) |
| [3] `0x180532A40` | `0x1801A82D0` | fermeture (partagée avec Arcade, Training, Option) |
| [4] `0x180532A48` | `0x1801E1B10` | **dessin** (812 o) |
| [7] `0x180532A60` | `0x1801AB960` | entrée sélectionnable ? |
| [9] `0x180532A70` | `0x1801DB760` | **annuler** |
| [10] `0x180532A78` | `0x1801DE340` | **VALIDER** |

Confirmation croisée par l'entrée `0x1801E4300` :

    0x1801E432B  mov dword [rdi+0x224], 1     ; DERNIER INDICE = 1 -> DEUX entrees

ce qui colle exactement aux deux identifiants écrits par le dessin.

**Correction à `menu_console.md` §12.1.** Ce document attribue à la page
TERMINAL la mise à jour `0x1801DD6A0` et le dessin `0x1801E17A0`. Ces deux
fonctions sont en réalité les créneaux [2] et [4] de la vtable `0x1805326C8`,
que le RTTI nomme **`TaskMenuScoreAttack`**. La vraie page TERMINAL est
`0x180532A28`, mise à jour `0x1801DD7A0` (un chiffre d'écart). Conséquence
directe : l'affirmation « `0x1801DD6A0` est le seul site du moteur à poser le
type de partie 1 » ne concerne pas TERMINAL mais **Score Attack** — et « type
de partie 1 = score attack » redevient une hypothèse plausible, contrairement à
ce que dit ce paragraphe.

### 1.4 Le validateur : `0x1801DE340`, et il est complet

Le répartiteur générique des pages de menu est `0x1801BBBE0`
(`TaskCsMenu::update`, créneau [2] de `0x18052F6C0`) :

    0x1801BBCC6  call 0x1801A2B90        ; code d'ANNULATION presse ?
    0x1801BBCCD  js   0x1801BBCDD        ; non
    0x1801BBCD7  call qword [r8+0x48]    ; vtable[9]  = annuler
    0x1801BBCDD  call 0x1801A2BC0        ; code de VALIDATION presse ?
    0x1801BBCE4  js   0x1801BBCF2        ; non
    0x1801BBCEE  call qword [r8+0x50]    ; vtable[10] = VALIDER

(`[9]` = `+0x48`, `[10]` = `+0x50` : la convention annoncée est vérifiée.)

La mise à jour du TERMINAL `0x1801DD7A0` appelle ce répartiteur en
`0x1801DD933`, mais **seulement** quand `[page+0x2F8] == 0`, c'est-à-dire quand
aucun sous-écran enfant n'est ouvert. Le validateur atteint est donc
`0x1801DE340` :

    0x1801DE340  mov [rsp+0x10], rbx / push rsi / sub rsp, 0x20
    0x1801DE34A  cmp qword [rcx+0x2F8], 0   ; un sous-ecran est-il deja ouvert ?
    0x1801DE352  mov esi, edx               ; esi = le code d'entree recu
    0x1801DE354  mov rbx, rcx               ; rbx = la page
    0x1801DE357  jne 0x1801DE42E            ; oui -> ne rien faire du tout
    0x1801DE362  mov edi, [rcx+0x58]        ; edi = INDICE DU CURSEUR
    0x1801DE365  test edi, edi
    0x1801DE367  jne 0x1801DE39F            ; != 0 -> branche « Replays »

    ; ---------- edi == 0 : CUSTOMIZE ----------
    0x1801DE369  call 0x1801B7010           ; garde REELLE (cf. 1.5)
    0x1801DE36E  test al, al
    0x1801DE370  je   0x1801DE429           ; fausse -> RIEN
    0x1801DE376  call 0x180029FB0           ; ** BOUCHON, rend TOUJOURS VRAI **
    0x1801DE37B  test al, al
    0x1801DE37D  je   0x1801DE429           ; (branche morte)
    0x1801DE383  mov  edx, esi
    0x1801DE385  mov  rcx, rbx
    0x1801DE388  call 0x1801BC010           ; figer / fermer la page
    0x1801DE38D  lea  ecx, [rdi+5]          ; edi==0 -> ecx = 5
    0x1801DE390  call 0x1800DA9A0           ; demander le MODE 5 = CS_TERM
    0x1801DE395  lea  ecx, [rdi+0x25]       ; edi==0 -> ecx = 0x25 = 37
    0x1801DE398  call 0x1800DA9C0           ; demander le SOUS-ETAT 37 CS_TERM_CUSTOMIZE
    0x1801DE39D  jmp  0x1801DE3E2

    ; ---------- edi == 1 : REPLAYS ----------
    0x1801DE39F  call 0x1801BC010
    0x1801DE3A4  cmp  edi, 1
    0x1801DE3A7  jne  0x1801DE402           ; indice > 1 : refermer la page
    0x1801DE3A9  lea  rdi, [rbx+0x300]      ; sous-tache logee DANS la page
    0x1801DE3C4  lea  rdx, [rip+...] -> "REPLAY MENU"
    0x1801DE3D2  call 0x180245830           ; demarrer la sous-tache
    0x1801DE3DB  mov  [rbx+0x2F8], rdi      ; l'enregistrer comme enfant courant

Les deux `lea ecx, [rdi+N]` sont l'astuce du compilateur : `rdi` vaut 0 sur
cette branche, donc `5` et `0x25`. **Il n'y a aucun calcul indexé par
l'entrée** : Customize est câblé en dur sur mode 5 / sous-état 37.

**Réponse à la question 3 : le chemin est INTACT.** Valider `Customize`
demande le mode **5 `CS_TERM`** et le sous-état **37 `CS_TERM_CUSTOMIZE`**,
tous deux **vivants** (cf. 1.6). Aucun maillon ne manque à ce site.

### 1.5 Les deux gardes, et ce qu'elles valent

**`0x180029FB0`** est le bouchon *permissif* du moteur :

    0x180029FB0  mov al, 1 ; ret

Il rend toujours vrai, donc le `je` qui le suit n'est jamais pris : il
**n'empêche rien**. C'est bien la signature d'un maillon retiré (à l'origine, un
prédicat réel — vraisemblablement « la personnalisation est-elle disponible /
le contenu est-il installé ? »), mais retiré **dans le sens qui nous arrange**.

**`0x1801B7010`** est la seule garde réelle, et elle n'est pas un bouchon :

    0x1801B7010  sub rsp, 0x28
    0x1801B7014  lea rcx, [rip+0x59AFE5]    ; -> 0x180752000
    0x1801B701B  call 0x180244EA0           ; « cette tache tourne-t-elle ? »
    0x1801B7020  test al, al
    0x1801B7022  sete al                    ; rend la NEGATION
    0x1801B7029  ret

`0x180752000` est identifié sans ambiguïté par le seul site qui la démarre,
`0x1801B76B7` :

    0x1801B76F5  lea r8, [rip+0x376E2C]  ; -> "TaskCsSystemSaveData(LOAD)"
    0x1801B7727  call 0x1802456B0        ; demarrer la tache

C'est donc **la tâche de sauvegarde système**, et `0x1801B7010` veut dire
« aucune opération de sauvegarde n'est en cours ». Détail qui achève de la
rendre inoffensive : le site qui la démarre est lui-même gardé par
`0x180007450` (bouchon qui rend **faux**, en `0x1801B769B`), donc dans ce build
la tâche de sauvegarde n'est **jamais** lancée, et `0x1801B7010` rend
**toujours vrai**.

### 1.6 Ce que fait le sous-état 37, une fois demandé

Table des sous-états `0x1803A05A0`, entrée de clef **37** (position 37), lue
directement dans le binaire :

    sous-etat 37 CS_TERM_CUSTOMIZE :
      entree 0x1801E50B0   milieu 0x1801E4ED0   sortie 0x1801E4FF0

**Aucun des trois n'est un bouchon.** (Pour comparaison, le sous-état 36
`MENU_MAIN` a bien `0x180007450` comme milieu, et les modes 1, 3, 7, 9 ont
`0x180029FB0` aux trois places.)

    ; ---- ENTREE ----
    0x1801E50B0  call 0x1801C5C50        ; rax = l'objet customize global [0x1807525E8]
    0x1801E50BC  call 0x1801C5B00(rax)   ; l'armer : 0x1801C46F0 (init) + 0x1801CE300
    0x1801E50CD  call 0x1800D41E0([0x18039F560], 8)
    0x1801E50DA  call 0x180087260(0x4F, 8)

    ; ---- MILIEU (une fois par trame) ----
    0x1801E4ED4  call 0x1801C5C50
    0x1801E4EDC  call 0x1801C4D60(rax)   ; le SEQUENCEUR (cf. ci-dessous)
    0x1801E4EE3  je   0x1801E4F04        ; pas fini -> voie de secours
    0x1801E4EE5  mov  ecx, 4
    0x1801E4EEA  call 0x1800DA9A0        ; fini -> retour au mode 4 MENU

    ; ---- SORTIE ----
    0x1801E4FFC  call 0x1801C5140(objet) ; arret du son, 0x1802450A0, nettoyage

Le cœur est `0x1801C4D60`, une **machine à étapes** pilotée par `[objet+0x00]`,
avec une table de sauts en `0x1801C4EBC` (index d'octets en `0x1801C4EDC`).
Sur 41 étapes déclarées, **sept seulement font quelque chose** ; les 34 autres
tombent sur le cas par défaut `0x1801C4EAE` (ne rien faire) :

| étape | code | ce qu'elle fait |
|---:|---|---|
| 0 | `0x1801C4D90` | `0x18018FB20(0, "STAGE_TASK")` — charger le décor, puis `0x18018FCF0(1)` |
| 1 | `0x1801C4DBE` | attendre `0x18018FE50()`, puis `0x1800D7130(1)` |
| 2 | `0x1801C4DE3` | attendre `0x1800D9020()`, puis **`[objet] = 10`** (saute 3→9) |
| 10 | `0x1801C4E02` | `0x1801C3350` → **`0x180245830(0x1807521A0, "CUST_MAIN")`** : la page de personnalisation est créée |
| 11 | `0x1801C4E3C` | `0x1800B5860`, puis BGM `rom/sound/bgm/vfes_bgm_cus.adx` par `0x180185DA0` |
| 12 | `0x1801C4E84` | tant que `0x180244EA0(tâche CUST_MAIN)` est vraie, rester ; sinon **`[objet] = 40`** |
| 40 | `0x1801C4EA7` | `0x180186D40(0)`, puis rendre vrai → le milieu demande le mode 4 MENU |

C'est la lecture qui manquait à `carte_customize.md` : les « fonctions »
`0x1801C4E02`, `0x1801C4E3C`, `0x1801C4E84` qu'elle liste comme distinctes sont
en réalité des **fragments `.pdata` chaînés** de `0x1801C4D60`. Le piège annoncé,
pris sur le fait.

### 1.7 L'autre porteur de 0x299 : `0x1801C51B0`

    0x1801C5315  mov ecx, 0x299
    0x1801C531A  call 0x1801EFD10        ; resolveur string_array
    0x1801C5322  call 0x18019B300        ; poser le texte

`0x1801C51B0` est **dans l'écran de personnalisation lui-même** (zone
`0x1801Cxxxx`). Elle écrit les gabarits `p_small_head_lt`, `p_txt_01_lt`,
`p_txt_03_rt`, appelle `0x1801C5540` (`p_txt_term_name_c`,
`p_txt_term_chara_name_c`, `p_term_chara_icon_c`, `p_txt_term_cos_plt_c`) et
référence la scène `0x150 = SELSTG_WXGA`. C'est le **bandeau de titre du poste
terminal**, qui réaffiche « Customize » une fois dans l'écran. Elle n'a aucun
appelant direct : elle est atteinte par vtable.

### 1.8 Bilan du point 1

    menu principal (entree 4 « TERMINAL », id 0x17C)
      -> sous-page TaskMenuTerminal (vtable 0x180532A28, logee a menu+0x2328)
         -> dessin  0x1801E1B10 : entrees { 0x299 Customize, 0x29A Replays }
         -> valider 0x1801DE340, curseur = 0
            -> garde 0x1801B7010  : « pas de sauvegarde en cours »  -> VRAIE
            -> garde 0x180029FB0  : bouchon permissif               -> VRAIE
            -> 0x1800DA9A0(5)     : mode 5 CS_TERM        [VIVANT]
            -> 0x1800DA9C0(37)    : sous-etat 37 CUSTOMIZE [VIVANT]
               -> entree 0x1801E50B0 -> 0x1801C5B00 -> 0x1801C46F0
               -> milieu 0x1801E4ED0 -> sequenceur 0x1801C4D60
                  etape 0  : scene STAGE_TASK
                  etape 10 : tache « CUST_MAIN »   <- l'ecran de personnalisation
                  etape 11 : BGM vfes_bgm_cus.adx
                  etape 12 : attendre la fin de CUST_MAIN
                  etape 40 : rendre vrai -> mode 4 MENU
               -> sortie 0x1801E4FF0 -> 0x1801C5140

**Il n'y a pas de maillon manquant sur ce chemin.** Contrairement à SINGLE
PLAYER et OFFLINE VERSUS (où il fallait fabriquer la demande de mode `GAME`),
TERMINAL/Customize **demande déjà** son mode et son sous-état, et les deux sont
vivants. C'est cohérent avec `menu_console.md` §8.5 : « Seul TERMINAL débouche
sur un mode vivant (`CS_TERM`) ».

---

# 2. La fonction `0x180227790`

Rappel de la commande : `couverture_console.md` §3 la désignait comme « la plus
grosse fonction de la surface console qu'on n'a jamais ouverte » — 7373 octets,
aucune chaîne, jamais nommée. Elle **n'a aucun rapport avec Customize** : elle
n'est pas sur le chemin du §1, et rien de ce qui suit ne le modifie.

## 2.1 Ses bornes : UNE seule fonction, pas des fragments chaînés

Le piège annoncé (une entrée `.pdata` n'est souvent qu'un fragment) ne joue pas
ici. Les entrées brutes autour de la cible :

| entrée `.pdata` | taille | `UNWIND_INFO` | chaînée ? |
|---|---:|---|---|
| `0x180227790` .. `0x18022945D` | **7373 o** | `0x180625178`, flags=2, 13 codes | **non** |
| `0x180229460` .. `0x1802299A7` | 1351 o | `0x1806278E0` | non |
| `0x1802299B0` .. `0x180229BF7` | 583 o | `0x1805FC738` | non |

Aucune autre entrée du binaire ne se rattache à elle par `UNW_FLAG_CHAININFO`.
**C'est bien une seule fonction de 7373 octets, d'un seul tenant.** Ce que le
drapeau ajoute : `flags=2` = `UNW_FLAG_UHANDLER`, donc la fonction a un
gestionnaire de **déroulement** — elle possède des objets locaux à détruire.
C'est du C++ avec destructeurs, et cela va se confirmer.

Son cadre de pile le dit aussi :

    0x1802277A0  lea rbp, [rsp - 0x3890]
    0x1802277A8  mov eax, 0x3990
    0x1802277AD  call 0x1802FE0E0        ; __chkstk
    0x1802277B2  sub rsp, rax            ; cadre de 0x3990 = 14 736 octets

Quatorze kilooctets de pile locale : elle construit beaucoup d'objets.

## 2.2 Ses appelants : un seul, et il mène à `APM3_GAMEOVER`

Balayage linéaire de tout le binaire (`refs_lineaires.py --data`, qui cherche
aussi les pointeurs 64 bits en `.rdata`) : **une seule référence dans les
3,13 Mo.**

    cible 0x180227790 : 1 reference(s)
      0x18021A305    appel    dans 0x18021A2E0

Elle n'est dans **aucune vtable**, dans **aucune table de pointeurs**. Le RTTI
ne la nomme donc pas. La remontée est courte et se termine tout de suite :

    0x180227790
      <- 0x18021A2E0          (154 o, appel unique)
         <- 0x18023DDC0       (102 o, aucun appelant direct)

`0x18023DDC0` n'a elle-même aucun appelant direct — parce qu'elle est appelée
par la machine à états. Une seule référence, en `.rdata` :

    cible 0x18023DDC0 : 1 reference(s)
      0x1803A0C08    ptr64[.rdata]

`0x1803A0C08` est dans la **table des sous-états**. Les entrées y font quatre
qwords — clef, entrée, milieu, sortie — et celle qui nous concerne est :

    0x1803A0C00 : 0x0000000100000033      ; clef 0x33 = 51
    0x1803A0C08 : 0x000000018023DDC0      ; ENTREE
    0x1803A0C10 : 0x000000018023A530      ; milieu
    0x1803A0C18 : 0x000000018023C390      ; sortie

La table des **noms** de sous-états commence à `0x1803A0CE0` (index 0 =
`DATA_INITIALIZE`) ; l'index 51 est en `0x1803A0CE0 + 8*51 = 0x1803A0E78` :

    0x1803A0E78 : -> "APM3_GAMEOVER"

Vérification croisée sur les voisins, qui confirme l'alignement de la table :
la clef 0x31 = 49 donne `APM3_SELECTOR` avec la sortie `0x1800DBB70`, exactement
ce que `machine_console.md` avait relevé (« `APM3_SELECTOR` partage le même
gestionnaire de sortie `0x1800DBB70` »).

**`0x180227790` est donc atteinte une fois, à l'entrée du sous-état 51
`APM3_GAMEOVER` — c'est-à-dire au moment précis où une partie se termine sur la
borne.**

## 2.3 Son appelant immédiat `0x18021A2E0`, qui dit tout de sa signature

154 octets, lisibles en entier :

    0x18021A2E0  push rbx / sub rsp, 0x50
    0x18021A2EF  mov  rbx, rcx
    0x18021A2F2  cmp  qword [rcx+0x08], 0   ; pas de canal -> ne rien faire
    0x18021A2F7  je   0x18021A36E
    0x18021A2F9  cmp  qword [rcx+0x38], 0   ; deja en cours -> ne rien faire
    0x18021A2FE  jne  0x18021A36E
    0x18021A300  lea  rcx, [rsp+0x28]       ; <- une std::string LOCALE
    0x18021A305  call 0x180227790           ; ** LA FABRIQUER **
    0x18021A30B  lea  r8, [rsp+0x28]        ; 3e argument = la chaine produite
    0x18021A310  mov  dl, 3                 ; 2e argument = 3
    0x18021A312  mov  rcx, qword [rbx+0x08] ; 1er argument = le canal
    0x18021A316  call 0x180294670           ; ** L'ENVOYER **
    0x18021A31B  test eax, eax
    0x18021A31D  jne  0x18021A335           ; echec -> on n'arme rien
    0x18021A31F  mov  rax, qword [rip+...]  ; -> [0x180C3BDD8] = singleton reseau
    0x18021A326  lea  rcx, [rip-0xC0D]      ; -> 0x180219720 = etape suivante
    0x18021A32D  mov  qword [rax+0x38], rcx ; armer la suite
    0x18021A331  mov  qword [rax+0x58], rbx
    ; ---- destructeur inline de la std::string locale ----
    0x18021A335  mov  rdx, qword [rsp+0x40] ; _Myres (capacite)
    0x18021A33A  cmp  rdx, 0x10
    0x18021A33E  jb   0x18021A36E           ; <16 : petite chaine, rien a liberer
    0x18021A343  mov  rcx, qword [rsp+0x28] ; le tampon alloue
    0x18021A369  call 0x1802FDD80           ; operator delete

La queue est la **destruction en ligne d'un `std::string` MSVC** : tampon en
`+0x00`, `_Mysize` en `+0x10`, `_Myres` en `+0x18`, seuil SSO à 16 caractères,
libération par `0x1802FDD80` (= `operator delete`). Il n'y a pas d'ambiguïté.

D'où la signature :

    std::string* __fastcall 0x180227790(std::string* resultat);

**`0x180227790` fabrique une chaîne de caractères, et n'est appelée que pour
cela.** Ce que `0x18021A2E0` en fait ensuite : `0x180294670(canal, 3, &chaine)`,
puis armement du singleton `[0x180C3BDD8]`. Ce singleton est celui que
`reseau_allnet.md` a déjà identifié comme l'**`AbaasManager`** (créé en
`0x180214CF9` par `operator new(0x108)` puis `0x180218A10`). Le `3` est un code
de requête.

*(à compléter : 2.4 ce qu'elle sérialise, 2.5 sa structure, 2.6 non établi)*

---

# 3. « Aucun bouton ne valide ni n'annule » — la mesure, et ce qu'elle corrige

Écrit le 2026-09-30. Binaire lu : `vf5fs-pxd-w64-Retail_APM3.dll.origine`,
**lecture seule**, le jeu n'a pas été lancé. Outil :
`tools/boutons_terminal.py` (`py -3 tools/boutons_terminal.py`), qui balaie les
14 100 fragments `.pdata` du moteur et relève :

* les **121 sites** qui appellent `0x1801A2CA0` (front/répétition) ou
  `0x1801A2C10` (tenu) avec le masque qu'ils demandent ;
* les **47 sites** qui appellent `Input_isOn` (`+0x158`) ou `Input_isOnNow`
  (`+0x160`) sur l'objet `[0x180C3B6F8]`, avec le code demandé ;
* toute autre référence à l'état d'entrées `0x180751040 + 0x54*joueur` ;
* les emplacements de détour possibles dans `0x180243ED0`.

## 3.1 CE QUI ÉTAIT ÉCRIT, ET QUI EST FAUX

`menu_console.md` §15.6 concluait, **d'après la légende d'une capture**
(« ✕ Back  ◯ Enter ») et non d'après le code :

> « les deux masques que l'écran lit pour ces deux actions sont `0x100` (bit 8)
> et `0x800` (bit 11) — et ces deux bits n'ont aucune source. […] C'est pour ça
> que rien ne valide et que rien ne revient. »

**Les trois affirmations sont fausses**, et le désassemblage le dit sans
ambiguïté.

### a) Valider et annuler ne passent pas par le masque arcade

    0x1801A2BC0   VALIDER     sub rsp,0x28
                              rcx = [0x180C3B6F8] ; edx = 7
                              call qword [rax+0x160]     ; Input_isOnNow(7)
                              neg al / sbb / neg / dec   ; presse -> 0, sinon -1

    0x1801A2B90   ANNULER     idem, edx = 8              ; Input_isOnNow(8)

Le créneau `+0x160` est `Input_isOnNow`, **pas** le masque. Les codes 7 et 8
sont le clavier : **Entrée** et **W**. Les deux ont une source depuis toujours.

Le répartiteur générique des pages de menu, `0x1801BBBE0`
(`TaskCsMenu::update`), est exactement celui du §1.4 :

    0x1801BBC32  call 0x1801A2EC0(&curseur, nb, boucle)  ; colonnes  -> vtable[7]
    0x1801BBC92  call 0x1801A2D60(&curseur, nb, boucle)  ; lignes    -> vtable[8]
    0x1801BBCC6  call 0x1801A2B90                        ; ANNULER   -> vtable[9]
    0x1801BBCDD  call 0x1801A2BC0                        ; VALIDER   -> vtable[10]

et **toutes** les pages du sous-système de personnalisation y finissent leur
mise à jour :

| classe (RTTI) | vtable | mise à jour | appelle `0x1801BBBE0` en |
|---|---|---|---|
| `TaskCustomizeMenu` | `0x180530420` | `0x1801C7110` | `0x1801C72B1` |
| `TaskSelItemMenu` | `0x1805304E0` | `0x1801C7440` | `0x1801C7639` |
| `TaskSelPartMenu` | `0x180530540` | `0x1801C7670` | (via `0x1801C7D00`) |
| `TaskCostumeMenu` | `0x1805303C0` | `0x1801C6F50` | `0x1801C70CF` |
| `TaskHelpWindow` | `0x180530480` | `0x1801C7390` | `0x1801C73FE` |
| `CharSelector` | `0x180530F30` | `0x1801CEDD0` | `0x1801CEE3C` |
| `DataSelector` | `0x180530F90` | `0x1801CEE60` | `0x1801CEECD` |
| `TaskDataSelector` | `0x180530FF0` | `0x1801CEEF0` | `0x1801CF1BA` |

`TaskSelItemMenu` fait même les deux lectures **en propre**, avant de passer la
main au répartiteur :

    0x1801C760C  mov ecx, 0x200 ; call 0x1801A2CA0  ; une piece vient de tomber ?
    0x1801C7618  jns  0x1801C763E                   ; oui -> on ignore la trame
    0x1801C761A  call 0x1801A2BC0                   ; VALIDER (Entree)
    0x1801C7623  call 0x1801A2B90                   ; ANNULER (W)
    0x1801C762C  mov dword [rbx+0x234], 1
    0x1801C7639  call 0x1801BBBE0

**Conclusion : la chaîne d'entrées de l'écran de personnalisation est
INTACTE.** Il n'y a aucune touche à câbler pour valider, annuler ou bouger le
curseur.

### b) Les bits 8 et 11 de cet écran sont la CAMÉRA

Les deux seuls sites de la zone qui demandent `0x100` et `0x800` sont dans
`0x1801C7890`, qui est le contrôleur de **caméra** de l'écran :

    0x1801C78AF  ecx = 0x40    tenu   ; bit 6 = X (croix) MAINTENU
    0x1801C78BB  jne ...              ; sans X, pas de rotation
    0x1801C78BD  0x11000 / 0x44000    ; haut / bas   -> 0x1801C3900 (tangage)
    0x1801C790B  0x88000 / 0x22000    ; gauche/droite-> 0x1801C3BA0 (lacet)
    0x1801C794B  0x100000 .. 0x800000 ; les memes deux axes, au STICK
    0x1801C79CB  0x20 / 0x10   tenu   ; U / Y        -> 0x1801C30F0 (zoom)
    0x1801C7A12  0x100         front  -> 0x1801C3A70 : RECENTRER LA VUE
    0x1801C7A2F  0x800         front  -> deux appuis : CHANGER DE VUE
                                         (0x1801C3D30 puis 0x1801C3D50,
                                          compteur en 0x180752600)

`0x1801C3A70` pose `-24.0` (`0xC1C00000`) dans le descripteur de caméra et le
réapplique ; le site `0x800` incrémente un compteur, et au **deuxième** appui
appelle `0x1801CE460` puis remet le compteur à zéro. Ce sont des commandes de
vue, pas « Back » et « Enter ».

Les quatre masques `0x100000`..`0x800000` (bits 20-23) sont le **stick
analogique**, et ils font exactement ce que les quatre directions font déjà
quand X est maintenu. Les câbler n'ajouterait rien : c'est pour cela qu'ils
sont laissés tels quels.

### c) Les bits 8 et 11 ne sont pas propres à cet écran

C'est le point qui interdit la réparation « propre » qu'on croyait tenir —
ajouter des lectures dans `0x180243ED0`. Relevé exhaustif :

| bit | masque | qui le lit | ce qu'il en fait |
|---|---|---|---|
| 8 | `0x100` | `0x18016EC83` dans `0x18016E390` | sélecteur d'arcade : `0x1801AB3A0(j,2,1)` + son |
| 8 | | `0x1801A733A` dans `0x1801A7220` | `TaskOptionControl` : referme une page |
| 8 | | `0x1801C7A12` dans `0x1801C7890` | **customize : recentrer la vue** |
| 8 | | `0x1801E6998` dans `0x1801E67A0` | classificateur d'évènements → code `0x14` |
| 8 | | `0x18020787F` dans `0x180206E10` | `0x1802068C0` puis état `0xE` |
| 10 | `0x400` | `0x1801E6962`, `0x1801F353F`, `0x18020BEB7` | trois écrans |
| 11 | `0x800` | `0x1801C7A2F` dans `0x1801C7890` | **customize : changer de vue** |
| 11 | | `0x1801E6947` dans `0x1801E67A0` | classificateur → code `0x0D` |
| 20-23 | | `0x1801C7890` seul | le stick, redondant avec les directions |

Donner une source au bit 8 dans le lecteur d'entrées **réveillerait le
sélecteur d'arcade, l'écran OPTIONS et `0x180206E10`** en même temps. C'est
précisément le piège annoncé (« une garde partagée retirée casse les autres
cas »), pris dans l'autre sens : ici c'est une *source* partagée qu'on
ajouterait.

D'où le choix : **accrocher les deux sites d'appel, et eux seuls.**

### d) Le code 15 n'est pas libre

`patch_moteur.py` écrivait, à propos du relais de sortie (`--transition-game`) :
« le **15**, libre entre les codes du joueur 1 (0 à 14) et ceux du joueur 2
(18 à 30) ». Le balayage le dément :

    0x1801248FF  mov edx, 0xf
    0x18021490F  call qword [rax+0x160]      ; Input_isOnNow(15)

dans la fonction `0x1802146F0` (le gestionnaire de messages du module réseau,
`cmp rcx, 0x20270`, celui qui range l'interface hôte en `[0x180C3B6F0]`). Le
résultat y arme `or [rbx+0x10], 0x40`. Échap peut donc, en plus de quitter le
mode, poser ce drapeau-là. Le relais de sortie n'est pas retiré pour autant —
il est **validé à l'écran** — mais le commentaire est corrigé.

**Les codes réellement libres des 32 créneaux du stub sont 16, 17 et 31 :**

    codes pris : 0..15 (le moteur les lit tous)
                 18..30 (le joueur 2, une fois `--joueur2` pose : code + 16)
    codes libres : 16, 17, 31

## 3.2 `--terminal-boutons` : ce que l'option fait, et ce qu'elle ne fait pas

Deux sites, deux relais de 35 octets dans la zone `TERM` de la section
`.greffe` (0x100 octets, posée avant `GRE_GEN` ; `verifier_disposition()`
refuse tout recouvrement) :

| site | octets d'origine | devient | code | touche | effet |
|---|---|---|---|---|---|
| `0x1801C7A12` | `e8 89 b2 fd ff` | `call GRE_TERM+0x00` | 16 | **B** | recentrer la caméra |
| `0x1801C7A2F` | `e8 6c b2 fd ff` | `call GRE_TERM+0x30` | 17 | **N** | changer de vue (deux appuis) |

Le relais :

    48 83 EC 28           sub rsp, 0x28          ; alignement + 32 o de reserve
    48 8B 0D <rip>        mov rcx, [0x180C3B6F8] ; l'objet d'entrees
    BA <code>             mov edx, code
    48 8B 01              mov rax, [rcx]
    FF 90 60 01 00 00     call qword [rax+0x160] ; Input_isOnNow -> al
    FE C8                 dec al                 ; 1 -> 0,  0 -> 0xFF
    0F BE C0              movsx eax, al          ; presse -> 0, sinon -1
    48 83 C4 28           add rsp, 0x28
    C3                    ret

`dec al` + `movsx` rend **exactement la convention de `0x1801A2CA0`** (l'indice
du joueur, ou -1), que les deux sites testent par `test eax, eax ; jne`. Les
`mov ecx, 0x100` / `mov ecx, 0x800` qui précèdent deviennent morts ; ils sont
laissés en place, on n'avale rien.

Les cinq octets remplacés sont un `call rel32` entier : ni cible de saut
(`0x1801C7A17` et `0x1801C7A34` le sont, et ne sont pas touchés), ni frontière
d'instruction avalée.

L'option pose la section `.greffe` elle-même si `--variantes` ne l'a pas déjà
posée : `console.cmd` n'a donc à changer que d'un mot.

**Ce que l'option NE fait pas :** elle ne répare ni la validation ni
l'annulation, parce qu'il n'y a rien à y réparer. Si l'écran ne répond
toujours pas, la cause est ailleurs — voir §3.4.

## 3.3 Le chemin complet, de TERMINAL à l'écran interactif

C'est la « zone utile » que §3.4 du cahier des charges demandait de
cartographier sans ouvrir les 312 fonctions.

    sous-etat 37 CS_TERM_CUSTOMIZE
      milieu 0x1801E4ED0 -> sequenceur 0x1801C4D60
        etape 10 : 0x1801C3350 -> 0x180245830(0x1807521A0, "CUST_MAIN")
                   vtable de l'objet : 0x18052FA80 = customize::ItemMain
                   (posee au demarrage par 0x180004D80)
                     [1] entree      0x1801C2E10
                     [2] MISE A JOUR 0x1801C2EC0 -> 0x1801C3D60
                     [3] fermeture   0x1801C3010

`0x1801C3D60` est une **machine à 0x47 états**, pilotée par `[objet+0x7C]`,
table d'index en `0x1801C4268` et table d'offsets en `0x1801C422C` (attention :
ces deux tables sont des DONNÉES à l'intérieur de la plage `.pdata` de la
fonction — un désassemblage linéaire y déraille). Quinze cas réels, quatorze
états vivants :

| état | code | ce qu'il fait |
|---:|---|---|
| 0 | `0x1801C3D9D` | remet tout à zéro, puis **`0x1801D0720(0)` — DÉMARRE LE SÉLECTEUR DE DONNÉES** ; → état 10 |
| 10 | `0x1801C3EAC` | **attend le sélecteur** : `0x1801CFDA0()` rend 0 tant qu'il tourne, **1** = rien choisi → état 0x46 (on s'en va), **2** = donnée choisie → état 20 |
| 20 | `0x1801C3F1D` | `0x1801CD1B0([objet+0x80])` : charger la donnée choisie |
| 21 | `0x1801C3F28` | → état 30 ou 40 selon `[objet+0x85]` |
| 30 | `0x1801C3F44` | `0x1801CBCE0(0)` |
| 31 | `0x1801C3F53` | attend `0x1801C6EB0()` ; si `0x1801CB020()` → état 40, **sinon retour au sélecteur (état 10)** |
| 40 | `0x1801C3FA2` | le modèle du personnage : `0x180187A30` / `0x180187C50` |
| 41 | `0x1801C3FE1` | attend `0x180187CC0()` → état 50 |
| 50 | `0x1801C4029` | `0x1801CE370(page,0)` + `0x1801CDCD0` |
| 51-53 | | `0x1801CD880`, puis `0x1801CE4F0` → état 60 |
| **60** | `0x1801C40A4` | **l'état interactif** : `0x1801C7A90()` chaque trame ; faux → on quitte |
| 70 | `0x1801C41B3` | rend vrai : `CUST_MAIN` se termine, l'étape 12 du séquenceur voit la tâche morte et passe à l'étape 40 → mode 4 MENU |

`0x1801CFDA0`, le verdict du sélecteur, en entier :

    rcx = [0x180752D30]              ; la tache TaskDataSelector
    call 0x180244F90                 ; sa scene existe-t-elle ?
      oui -> rend 0                  ; il tourne encore
    cmp byte [rcx+0x60], 0           ; son drapeau « je m'en vais »
      == 0 -> rend 1                 ; RIEN CHOISI : customize se referme
      != 0 -> rend 2                 ; donnee choisie : on continue

L'objet `[0x180752D30]` est alloué au démarrage (`0x1801CEB30`, `0x56E0`
octets, appelée par la liste de modules `0x1802441A0`) : il existe toujours.

**Conséquence, et c'est le fait neuf de la séance :** ce que l'on voit en
entrant dans TERMINAL → Customize **n'est pas** l'écran de personnalisation,
c'est le **sélecteur de données** (`CARD SELECTOR` / `DATA SELECTOR` /
`CHAR SELECTOR`). L'écran de personnalisation ne vient qu'après lui.

### `0x1801D0B80`, le démarrage du sélecteur, et la carte VF.NET

`0x1801D0720(0)` appelle `0x1801D0B80(selecteur, 0, 3, 0)`. Le `3` est un
champ de bits rangé en `[obj+0x5540]` ; le bit 0 déclenche ceci :

    0x1801D0C12  ecx = i ; call 0x180029FB0   ; « le personnage i est-il pris ? »
    0x1801D0C1F  sete al                       ; 0x180029FB0 rend TOUJOURS 1
    0x1801D0C24  [rbp+0x250+i] = al            ; donc 0 pour les dix-neuf

`0x180029FB0` est le **bouchon permissif** du moteur. Le prédicat « ce
personnage est-il déjà pris / verrouillé sur la carte ? » a donc été retiré, et
les dix-neuf cases sont marquées libres. **Le sélecteur ne réclame pas de carte
VF.NET pour s'afficher** : la seule chose que la carte lui donnait — la liste
des personnages déjà créés — est bouchonnée du bon côté. C'est la réponse à la
question « sur borne ils supposent une carte VF.NET » : **non, plus dans ce
build.**

Ce qui reste inconnu et ne se lit pas dans le binaire : si le sélecteur trouve
bien ses planches 2D. C'est de l'affichage, pas de l'entrée.

## 3.4 Ce qui reste comme cause possible, et ce qu'un seul lancement tranche

La chaîne d'entrées est mesurée intacte de bout en bout. Il reste donc deux
causes possibles à « l'écran s'ouvre et n'affiche que son décor » :

1. **`--wxga`.** L'octet de variante d'affichage `[0x1806490D0+0x20]` est lu à
   54 endroits de l'interface et décale des identifiants de scène. Le
   sélecteur de données et l'écran de personnalisation sont les écrans les
   plus riches en interface du build. `menu_console.md` §15.3 le désignait déjà
   comme le suspect numéro un, et l'essai n'a jamais été fait.
2. **Les planches 2D du sélecteur** ne se chargent pas, et l'écran répond aux
   touches sans rien montrer.

Les deux se distinguent en **un seul lancement**, et les deux lanceurs sont
prêts : `tools/terminal.cmd` (avec `--wxga`) et `tools/terminal_sans_wxga.cmd`.

## 3.5 `Replays` (libellé `0x29A`) : le chemin, suivi, et il n'est PAS bouchonné

Demandé au §3.4 du cahier des charges. Même méthode qu'au §1.

    TaskMenuTerminal, valider 0x1801DE340, curseur = 1
      0x1801DE3A9  rdi = page + 0x300           ; la sous-tache, LOGEE dans la page
      0x1801DE3C4  rdx -> 0x180532F38 "REPLAY MENU"
      0x1801DE3D2  call 0x180245830             ; la demarrer
      0x1801DE3DB  [page+0x2F8] = rdi           ; l'enregistrer comme enfant

La sous-tâche est un `TaskMenuReplay`, vtable **`0x1805329C8`** (RTTI) :

| créneau | adresse | rôle |
|---:|---|---|
| [1] | `0x1801E3FF0` | entrée |
| [2] | `0x1801DD400` | **mise à jour** |
| [4] | `0x1801E1430` | **dessin** : entrées `0x29B`, `0x29C`, `0x29D` |
| [9] | `0x1801DB6D0` | annuler |
| [10] | `0x1801DE240` | **valider** |

Les trois libellés, lus par `tools/libelles.py` :

    0x29B  'Your data'      0x29C  'Last game'      0x29D  'Online data'

Le validateur `0x1801DE240` :

* **curseur 0 — `Your data`** : garde `0x1801B7010` (toujours vraie, §1.5),
  puis `[page+0x2F1] = 1`, fermeture des deux scènes, `0x1801BAD00()`
  (qui pose `[0x180752190] = 1` et appelle le bouchon `0x180007450`) et
  `[page+0x2F4] = 1` ;
* **curseur 1 — `Last game`** : la page se referme, rien d'autre ;
* **curseur 2 — `Online data`** : `0x1801B0120(0, 3, 1)` ouvre la page des
  classements comme sous-page — la même fonction que `--menu-ranking`
  neutralisait, et elle n'a rien à jouer sans réseau.

La mise à jour `0x1801DD400` fait le reste, et **c'est elle qui demande le
mode et le sous-état** :

    0x1801DD4AE  cmp byte [rbx+0x2F1], 0    ; « Your data » a-t-il ete valide ?
    0x1801DD4D1  call 0x1801BB6A0           ; l'animation de sortie est-elle finie ?
    0x1801DD4E4  call 0x1801BACF0           ; le lecteur est-il pret ?
    0x1801DD4F0  mov byte [rbx+0x60], 1     ; oui -> armer
    ; ... a la trame suivante :
    0x1801DD47D  cmp byte [rbx+0x60], 0
    0x1801DD483  mov ecx, 5
    0x1801DD488  call 0x1800DA9A0           ; MODE 5 = CS_TERM
    0x1801DD48F  cmp dword [rbx+0x58], 1    ; le curseur
    0x1801DD493  sete cl
    0x1801DD496  add ecx, 0x26
    0x1801DD499  call 0x1800DA9C0           ; SOUS-ETAT 38, ou 39 si curseur == 1

Les deux sous-états visés, lus dans la table `0x1803A05A0` et nommés par
`0x1803A0CE0` :

| clef | nom | entrée | milieu | sortie |
|---:|---|---|---|---|
| 38 | `CS_TERM_REPLAY_PLAY` | `0x1801E50A0` → `0x1801BA8E0(0)` | `0x1801E4EC0` → `0x1801BA770` | `0x1801E4FE0` → `0x1801BA880` |
| 39 | `CS_TERM_LAST_PLAY` | *(les mêmes trois)* | | |

**Aucun des trois n'est un bouchon** (`0x180029FB0` / `0x180007450`). Le
sous-état 39 n'est cependant **pas atteignable** : seul le curseur 0 arme
`[page+0x2F1]`, et le curseur 0 donne `0x26 = 38`. `Last game` referme la page
sans rien demander.

**Verdict : `Replays` n'est pas bouchonné.** Il mène au sous-état 38
`CS_TERM_REPLAY_PLAY`, dont les trois gestionnaires sont vivants, et dont le
corps est le lecteur de reprises `0x1801BA770`/`0x1801BA8E0`/`0x1801BA880`
— jamais ouvert, et qui n'a probablement aucune reprise à lire sur un poste
sans sauvegarde. C'est à vérifier à l'écran, et c'est dans le lanceur
`tools/terminal.cmd`.

## 3.6 CE QUE L'ÉCRAN A DIT — ET LA VRAIE CAUSE (2026-09-30, après lancement)

Frédéric a lancé les deux essais. Ses observations, mot pour mot :

> « le décor est bien celui de la borne (trm) ; le premier écran est le
> SELECTEUR DE PERSONNAGE, puis des données du personnage sélectionné ;
> l'écran costume settings n'affiche pas les images des différents costumes ;
> **HAUT / BAS et GAUCHE/DROITE des flèches du clavier ne font pas bouger de
> curseur** ; ENTREE valide, W annule ; B recentre la camera, N change de
> vue ; X maintenu + les flèches font tourner le modèle ; la barre espace
> affiche le customisation menu. »
>
> « SUR Replays : il affiche Your data/Last game/online data. En cliquant
> dessus, cela n'aboutit à rien, **les commandes deviennent figées**. »

**Et c'est identique avec et sans `--wxga`.**

### Ce que cela valide, et ce que cela enterre

| | |
|---|---|
| `--terminal-boutons` | **validé à l'écran** : B recentre, N change de vue. Les deux relais font exactement ce que §3.1 b) annonçait. |
| §3.1 a) | **validé** : Entrée valide, W annule. La chaîne d'entrées était bien intacte. |
| §3.3 | **validé** : c'est le sélecteur de personnage qui s'ouvre en premier, pas l'écran de personnalisation. |
| `--wxga`, suspect n°1 de `menu_console.md` §15.3 | **ENTERRÉ**. Identique avec et sans. |
| §3.4, cause n°2 (« les planches 2D ne se chargent pas ») | **partiellement vrai, et cantonné** : tout se dessine sauf les six vignettes de costume. |

### La vraie cause : le compteur de crans, posé puis effacé

Le répartiteur `0x1801BBBE0` ne déplace un curseur que si le **compteur** de
la page est strictement positif :

    0x1801BBBFE  cmp dword [page+0x224], 0   ; crans VERTICAUX
    0x1801BBC19  jle ...                     ; <= 0 -> on ne bouge pas
    0x1801BBC69  cmp dword [page+0x22C], 0   ; crans HORIZONTAUX
    0x1801BBC70  jle ...                     ; <= 0 -> on ne bouge pas
    0x1801BBCC6  call 0x1801A2B90            ; ANNULER : toujours lu
    0x1801BBCDD  call 0x1801A2BC0            ; VALIDER : toujours lu

Un compteur à zéro donne **exactement** le symptôme : valider et annuler
marchent, rien ne bouge. Et `0x1801A2EC0` / `0x1801A2D60` — les deux seules
fonctions qui déplacent ces curseurs — **n'ont aucun autre appelant dans la
zone** : le compteur est le seul verrou.

`tools/curseur_customize.py` (lanceur : aucun, il s'appelle depuis
`controle_quest`) relève, page par page, ce que l'entrée (créneau 1) écrit
dans les quatre compteurs. Trois pages **posent** leur compte, puis
l'**effacent** quelques instructions plus loin :

| page | pose | valeur | efface en |
|---|---|---:|---|
| `TaskDataSelector` | `0x1801D051A` | H = 18 (dix-neuf crans, bouclés) | `0x1801D0562` |
| `TaskCustomizeMenu` | `0x1801CB5C7` | V = 6 (sept lignes) | `0x1801CB601` |
| `TaskExclWarning` | `0x1801CB68C` | V = 1 (deux lignes) | `0x1801CB6C6` |

Le compte posé est le **dernier indice**, pas le nombre —
`TaskMenuTerminal` pose 1 pour ses deux entrées. Les sept lignes de
`TaskCustomizeMenu` correspondent exactement à la capture de Frédéric :
*Return to customization, Costume settings, Change pose, Reset to default,
Undo changes, Exit without saving, Save and Exit*. Et les dix-neuf crans de
`TaskDataSelector`, au nombre de personnages de FS.

### La preuve que l'effacement est inconditionnel

`TaskCustomizeMenu` est linéaire — **zéro cible de saut** dans tout son
fragment :

    0x1801CB597  xor esi, esi                    ; esi = 0, jamais reecrit
    0x1801CB5C7  mov dword [rdi+0x224], 6        ; SEPT lignes
    0x1801CB5D1  call 0x1801BD0B0                ; la page est BATIE avec
    0x1801CB5E0  call 0x1801BE8E0(page+0x248, 0x0E)
    0x1801CB5EF  call 0x1801BDA20(page+0x248, 0x45)
    0x1801CB5F4  mov dword [rdi+0x22C], esi      ; 0
    0x1801CB5FA  mov byte  [rdi+0x230], sil      ; 0
    0x1801CB601  mov dword [rdi+0x224], esi      ; <-- LE SIX EST EFFACE
    0x1801CB607  mov byte  [rdi+0x228], sil      ; 0

Le compte **est utilisé** entre les deux : la page est construite avec ses
sept lignes, puis son curseur est neutralisé. C'est un maillon retiré, et
retiré après coup.

`TaskDataSelector` a deux branches entre la pose et l'effacement, mais elles
**convergent** : l'outil a d'abord refusé cette page, tant qu'il ne
distinguait pas « branches qui convergent » de « saut par-dessus ». Le test
final est plus fin, et il est écrit dans l'outil :

* aucune cible de saut dans `]pose, effacement]` n'est visée depuis
  l'extérieur de `[pose, effacement]` — sinon on entrerait dans la zone sans
  être passé par la pose ;
* aucun saut parti de `[pose, effacement[` ne vise au-delà de l'effacement —
  sinon on pourrait le sauter.

Les deux tiennent pour les trois pages.

### `--customize-curseur`

On neutralise les trois effacements, et rien d'autre. Aucune caverne, aucun
détour, **aucune valeur inventée** : 18, 6 et 1 sont les comptes que le
moteur se donne lui-même.

| site | octets | effet |
|---|---:|---|
| `0x1801D0562` | 13 | le choix du personnage garde ses dix-neuf crans bouclés |
| `0x1801CB5F4` | 26 | le *Customization menu* garde ses sept lignes |
| `0x1801CB6B9` | 26 | l'avertissement garde ses deux lignes |

**Ce que l'option ne fait pas.** Cinq autres pages — `CharSelector`,
`DataSelector`, `TaskCostumeMenu`, `TaskSelPartMenu`, `TaskSelItemMenu` —
n'ont **jamais** de compte non nul, nulle part dans le binaire. Il n'y a rien
à restaurer, et on n'invente pas un nombre de lignes. Elles restent sans
curseur, et c'est dit. C'est notamment le cas de *Costume settings* : ses six
« Type A..S » sont dessinés, mais aucun compte ne leur correspond dans le
code. Ce sera à trancher avec Frédéric, pas tout seul.

## 3.7 POURQUOI `Replays` FIGE — un bouchon, et un repli

Valider « Your data » (curseur 0) appelle `0x1801BAD00` :

    0x1801BAD04  rcx = [0x180752188]      ; l'objet « liste de reprises »
    0x1801BAD0B  edx = [rcx+0x08]         ; le nombre demande
    0x1801BAD0E  [rcx+0x0C] = 0           ; le nombre CHARGE, remis a zero
    0x1801BAD18  call 0x180007450         ; ** LE BOUCHON QUI REND FAUX **
    0x1801BAD1D  [0x180752190] = 1

`0x180007450` est `xor al,al ; ret` : **le chargement de la liste a été retiré
de ce build.** Or la mise à jour `0x1801DD400` n'arme la demande de mode
qu'après `0x1801BACF0` :

    0x1801BACF0  rax = [0x180752188] ; cmp dword [rax+0x0C], 0 ; seta al

c'est-à-dire « au moins une reprise chargée » — donc **jamais**. Le
validateur a pourtant **déjà fermé les deux scènes** de la page. Il ne reste
ni page vivante ni transition : l'écran est figé. Le symptôme est exact.

Ce que §3.5 disait — « `Replays` n'est pas bouchonné » — reste vrai du
**chemin d'état** : le sous-état 38 et ses trois gestionnaires sont bien
vivants. Ce qui est bouchonné, c'est le **chargement des données**, un cran
en amont. La nuance vaut d'être écrite : un chemin vivant ne garantit pas
qu'on l'atteigne.

`--replays-sans-gel` envoie le curseur 0 dans la branche « refermer la page »
— celle que « Last game » emprunte déjà — au lieu de la branche qui ferme les
scènes sans transition. Quatre octets en `0x1801DE257` :

    85 ff  test edi, edi     ->  90 90  nop nop
    75 56  jne 0x1801DE2B1   ->  eb 56  jmp 0x1801DE2B1

`rcx` (la page) et `esi` (le code reçu) sont intacts au point de saut.
**C'est un repli, pas une réparation** : il n'y a aucune reprise à lire, et
la fonction de chargement n'est pas dans le binaire — son appel a été
remplacé par le bouchon.

## 3.8 CE QUI RESTE OUVERT : les vignettes de costume

Les six cases de *Costume settings* sont **noires**. `p_cos_icon_c`
(`0x180530A48`, posé par `0x1801C9088` via `0x1801BCD70`) n'est qu'une
**ancre de position** dans la scène 2D, pas l'image : le gabarit dit *où*,
pas *quoi*. D'où vient l'image n'est pas établi, et je ne l'ai pas cherché à
moitié. C'est un chantier à part, et il commence par `0x1801C8F60`, la
fonction qui pose les trois ancres `p_small_head_lt`, `p_cos_icon_c` et
`p_txt_cos_type_c`.

## 3.9 LE SECOND VERROU : l'accepteur de vtable (2026-10-01)

Après `--customize-curseur`, Frédéric a relancé. Son retour :

> « seules les flèches **haut et bas** fonctionnent, et **uniquement dans le
> customisation menu** ; replays/your data ne gèle plus les commandes mais ne
> lance rien ; replays/online data **gèle toujours** les commandes. »

Un succès partiel qui dit exactement où regarder : `TaskCustomizeMenu` marche
(sept lignes), donc le mécanisme du compteur est le bon — mais le *Character
Select* ne bouge toujours pas, alors que ses dix-neuf crans survivent
désormais.

**Le compteur n'était que le premier verrou.** Voici le second, dans
`0x1801BBBE0`, juste après le déplacement :

    0x1801BBC72  mov  esi, [rbx+0x5C]      ; le curseur AVANT la boucle
    0x1801BBC80  (boucle)
    0x1801BBC92  call 0x1801A2D60          ; deplacer d'un cran
    0x1801BBC97  test al,al ; je 0x1801BBCC3
    0x1801BBCBA  call qword [r8+0x40]      ; ** vtable[8], l'ACCEPTEUR **
    0x1801BBCBD  test al, al
    0x1801BBCBF  je   0x1801BBC80          ; refuse -> on recommence
    ...
    0x1801BBCC3  mov  [rbx+0x5C], esi      ; ** LE CURSEUR EST RESTAURE **

Si l'accepteur refuse, la sortie de boucle **remet le curseur où il était** :
rien ne bouge, et aucun son ne joue. Le créneau `[7]` (`+0x38`) fait de même
pour le vertical, avec la restauration en `0x1801BBC66`.

Le relevé des créneaux 7 et 8 sur les onze pages du parcours :

| page | [7] vertical | [8] horizontal |
|---|---|---|
| `TaskCustomizeMenu` | `0x1801BD080` | `0x1801BD080` | ← **marche**, et c'est ce qu'il voit |
| `TaskCostumeMenu`, `TaskSelItemMenu`, `TaskSelPartMenu`, `TaskExclWarning`, `TaskHelpWindow` | `0x1801BD080` | `0x1801BD080` |
| `TaskMenuTerminal` *(témoin)* | `0x1801AB960` | `0x1801BD080` |
| `TaskMenuReplay` *(témoin)* | `0x1801E4D00` | `0x1801BD080` |
| `DataSelector` | `0x1801BD080` | `0x1801D0180` |
| **`CharSelector`** | **`0x180007450`** | `0x1801D0180` |
| **`TaskDataSelector`** | `0x1801BD080` | **`0x180007450`** |

`0x180007450` est `xor al,al ; ret` — le bouchon qui **refuse**. Et
`0x1801BD080`, celui que toutes les autres pages portent, est
`call 0x1801A3030 ; mov al,1 ; ret` : jouer le son du curseur, et accepter.
Rien de plus.

`--customize-curseur` remet donc `0x1801BD080` dans le **créneau 8 de
`TaskDataSelector`** — l'écran *Character Select*, celui dont le répartiteur
reçoit la tâche elle-même (`0x1801CF1B7 mov rcx, rdi ; call 0x1801BBBE0`).
Le créneau est dans `.rdata` et **relocalisé** (type 10) ; le patcheur refuse
s'il ne l'est pas.

**Ce qu'on ne touche pas** : le créneau 7 de `CharSelector`, bouchonné lui
aussi. `CharSelector` n'a **aucun compte vertical** nulle part dans le
binaire : `0x1801BBBE0` sort sur le `jle` bien avant d'appeler l'accepteur.
Le réparer n'aurait aucun effet, et on ne pose pas de correctif sans effet.
Et on ne touche pas au **corps** de `0x180007450`, partagé par des dizaines
de vtables : le site, jamais le corps.

## 3.10 `Online data` gelait pour une autre raison, déjà connue du dépôt

    0x1801DE2C3  call 0x1801B0120(0, 3, 1)   ; la page des CLASSEMENTS
    0x1801DE2C8  mov [rbx+0x2F8], rax        ; rangee comme sous-page

C'est mot pour mot ce que le commentaire de `SOUSMENU_RANKING` décrit pour le
menu principal : « sur une borne sans réseau, cette scène n'a rien à jouer et
ne se termine jamais : le menu restait suspendu derrière elle ».

Le remède tient en **un octet**. Après `--replays-sans-gel`, tout le monde
arrive en `0x1801DE2B1`, où `cmp edi, 2 ; jne 0x1801DE2FB` aiguille le
curseur 2 vers RANKING et les autres vers « refermer la page ». On compare à
**3** : plus personne ne vaut la comparaison, et les trois entrées referment
proprement la page.

`Replays` devient donc entièrement inerte — trois entrées qui rendent la main
au menu TERMINAL. C'est honnête : sur ce build il n'y a ni reprise
enregistrée, ni réseau. Mieux vaut une porte qui se referme qu'une porte qui
fige.

## 3.11 LES SIX VIGNETTES DE COSTUME : la chaîne est SAINE de bout en bout

`tools/vignettes_costume.py` (lanceur : `tools/vignettes_costume.cmd`).

**Comment l'écran choisit son image.** `0x1801C8F60` dessine la page ; pour
chaque case :

    0x1801C929E  call 0x1801CB030        ; -> ax = L'IDENTIFIANT du sprite
    0x1801C92AA  call 0x180189880(desc)  ; preparer
    0x1801C92AF  [desc+0x04] = id
    0x1801C92C8  [desc+0x0C] = 0x400000  ; drapeaux
    0x1801C92E3  call 0x180187C00(desc)  ; dessiner

et `0x1801CB030` bâtit **sur la pile** une table 19 × 6 d'identifiants —
le même idiome que la table d'entrées de menu du §1.3, invisible à tout
balayage de données :

    0x1801CB2CE  call 0x1801C3460        ; le PERSONNAGE, borne a 18
    0x1801CB2D5  cmp rbx, 6              ; le TYPE, borne a 6
    0x1801CB2F0  rax = [rbp + perso*8 + 0x50]
    0x1801CB2F5  eax = word [rax + type*2]

**Les sept contrôles, tous verts.**

| # | contrôle | résultat |
|---|---|---|
| 1 | la table 19 × 6 se reconstruit | 114 identifiants |
| 2 | ils existent dans `spr_db` | **114 / 114** — ce sont les `SPR_T_ITM<perso>_BODY01..06` |
| 3 | leurs rangs pointent où il faut | Akira : rangs 764 à 769 |
| 4 | les images sont dans la planche | `spr_t_itmaki.farc` a 770 sprites, et ses **six derniers sont `BODY01`..`BODY06`** |
| 5 | les dix-neuf planches sont dans le `.par` | oui, ~2,5 Mo chacune, dossier `2d` |
| 6 | l'écran charge la planche | état 40 de `CUST_MAIN` : table `0x18052FAE0` (45 = `SPR_T_ITMAKI`, 455, 456) → `0x180187C50`, **aucun bouchon** |
| 7 | notre `spr_db` n'a rien cassé | 0 planche modifiée, 0 sprite perdu, 0 sprite changé |

**Il n'y a donc aucun maillon manquant.** La cause est à l'exécution, et il
ne reste que trois possibilités, que seule une sonde sépare :

* la planche n'est jamais demandée au système de fichiers ;
* elle est ouverte mais `0x180187CC0` ne la déclare jamais prête ;
* tout passe, et c'est le **rang de dessin** — la vignette est derrière le
  fond de la fenêtre.

`tools/sonde_vignettes.py` mène le jeu seul jusqu'à *Costume settings* et
pose cinq points d'arrêt (`0x180187C50` charger, `0x180187CC0` prêt,
`0x180187A30` décharger, `0x1801CB030` l'identifiant rendu, et `CreateFileW/A`
filtré sur « itm »). Sa sortie nomme laquelle des trois.

## 3.12 LES VIGNETTES : LE VERDICT DE LA SONDE — rien n'est cassé, c'est l'ORDRE

Frédéric a lancé `tools/vignettes_costume.cmd`. Le journal
(`analysis/sonde_vignettes.txt`) et les six captures tranchent sans
ambiguïté.

**La chronologie, lue dans le journal :**

    t = 55..66 s   id vignette #1..#24   ecx = 0..5     <- « Costume settings »
                                                           dessine ses six cases
    capture t=66                                        <- ELLES SONT NOIRES
    t = 66..72 s   charger #14  ecx = 0x2D (45)         <- SPR_T_ITMAKI arrive ICI
    capture t=72                                        <- « Select Part » :
                                                           TOUTES les vignettes
                                                           d'objets s'affichent
    capture t=95                                        <- « Costume settings »
                                                           rouvert : LES SIX
                                                           COSTUMES EN COULEUR

**Les vignettes ne sont pas cassées.** La capture `vignettes_t095.png` montre
les six types d'Akira — gi blanc, tenues B, C, D, E, S — parfaitement
dessinés, derrière la boîte « All equipped items will be reset to defaults ».
Et `vignettes_t072.png` montre tout l'écran *Select Part* avec ses vignettes
d'objets (Hair/Hat, Forehead, Wrists, Belt, Legs, Outer, Pants), qui sont des
sprites `AKI_P_xxxx` de **la même planche**.

**La cause est donc l'ORDRE, et rien d'autre.** Le *Costume settings* que
Frédéric voyait noir est celui du **sélecteur de données**, qui s'ouvre
**avant** l'état 40 de `CUST_MAIN` — l'état qui charge
`spr_t_itm<personnage>`. La page demande ses six identifiants (le journal les
montre, types 0 à 5, en boucle), le moteur les résout correctement, mais la
planche n'est pas encore en mémoire : le sprite ne dessine rien, et la case
reste au fond de la fenêtre.

Cela ferme les sept contrôles du §3.11 : ils étaient tous verts parce que
**tout est sain**. La seule chose qui manquait était le moment.

Un détail du journal qui vaut d'être noté : `charger` compte **14 passages**
et `décharger` **4** ; `0x1801CB030` est appelé **9 391 fois** (six cases par
trame). Et **aucun `CreateFile` ne contient « itm »** : le moteur lit la
planche depuis `vf5fs_data.par`, déjà ouvert — l'absence de fichier « itm »
ne prouvait donc rien, et c'est la chronologie, pas le filtre de fichiers,
qui a donné la réponse.

### Ce que coûterait de le réparer, et pourquoi la question se pose

Il faudrait charger `spr_t_itm<perso>` **dès le sélecteur**, c'est-à-dire
avant l'état 40. Deux difficultés, dites plutôt que contournées :

* le personnage **change avec le curseur** (dix-neuf crans, désormais
  fonctionnels), donc il faudrait recharger à chaque cran — ~2,5 Mo par
  planche ;
* le chargement est asynchrone (`0x180187C50` puis `0x180187CC0`), donc il
  faudrait aussi une attente, là où le sélecteur n'en a pas.

C'est un vrai chantier pour un seul écran, alors que **l'écran de
personnalisation lui-même marche**. C'est à Frédéric de dire s'il le veut,
pas à moi de le décider.

## 3.13 `--vignettes-costume` : le correctif (2026-10-01)

Frédéric : « **il faut réparer les vignettes** ». Fait.

`0x1801C8F60` est le **créneau 4 (dessin) de `TaskCostumeMenu`**, et il n'a
**aucun appelant direct** : on détourne donc le **créneau**, pas le prologue.
Le relais s'assure que la planche du personnage courant est chargée, puis
saute dans le dessin d'origine. Il refait, mot pour mot, ce que l'état 40
fait déjà :

    sub  rsp, 0x38
    mov  [rsp+0x20], rcx                  ; la page, pour le dessin
    call 0x1801C5AB0                      ; l'objet d'etat du customize
    movzx ecx, byte [rax+0x116]           ; le PERSONNAGE
    xor  eax, eax ; cmp cl, 0x15 ; cmovb eax, ecx
    lea  rdx, [0x18052FAE0]               ; les 21 identifiants de planche
    mov  edx, [rdx + rax*4]
    lea  rax, [g_cos]
    cmp  edx, [rax]  ;  je FIN            ; ** LE GARDE : 9391 appels/minute **
    mov  [rsp+0x28], rdx
    mov  ecx, [rax] ; test ecx,ecx ; je +5
    call 0x180187A30                      ; decharger l'ancienne
    mov  rdx, [rsp+0x28]
    lea  rax, [g_cos]      ; mov [rax], edx
    lea  rax, [0x180752200]; mov [rax], edx    ; ** CUST_MAIN + 0x60 **
    mov  ecx, edx
    call 0x180187C50                      ; CHARGER
  FIN:
    mov  rcx, [rsp+0x20] ; add rsp, 0x38 ; jmp 0x1801C8F60

**Trois points qui font que c'est sûr.**

* **Le garde.** `0x1801CB030` est appelé 9 391 fois par minute (six cases par
  trame) ; sans le garde, on rechargerait 2,5 Mo à chaque trame. Avec, on ne
  charge qu'au changement de personnage — et le personnage peut changer, les
  dix-neuf crans du Character Select étant désormais vivants.
* **`CUST_MAIN + 0x60`.** Le relais y écrit l'identifiant. Sans cela, l'état
  40 chargerait une **seconde** fois la même planche et le compteur de
  références ne redescendrait jamais : 2,5 Mo perdus par passage. Avec,
  l'état 40 voit `!= -1`, décharge, puis recharge — le cycle reste équilibré.
* **La pile.** Le créneau est appelé avec `rsp % 16 == 0`, donc `rsp % 16 ==
  8` dans le relais ; `sub rsp, 0x38` rend l'alignement **et** les 32 octets
  de réserve, en laissant `[rsp+0x20]` et `[rsp+0x28]` libres. Le `jmp` final
  part avec la pile exactement comme le dessin l'attend — `0x1801C8F60`
  commence par `mov rax, rsp`.

Le créneau est relocalisé (type 10) ; le patcheur refuse s'il ne l'est pas.

### Ce qui restait non mesuré, et qui l'est maintenant

Le premier scénario de sonde **traversait le Character Select à coups
d'ENTRÉE** : il ne pouvait donc rien dire du correctif de l'accepteur
(créneau 8 de `TaskDataSelector`). `tools/sonde_vignettes.py` appuie
désormais sur gauche/droite — six fois dans le Character Select, trois fois
dans le *Costume settings* du sélecteur — et capture à t=46 (avant), t=52 et
t=56 (pendant). Si les dix-neuf crans répondent, le personnage change sous
le curseur et les images le montrent.

## 3.14 LES VIGNETTES SONT RÉPARÉES — ce que charger seul ne faisait pas (2026-10-01)

`vignettes_t052.png` : les six types d'Akira, **en couleur**, dans le
*Costume settings* du sélecteur. C'est l'écran qui était noir.

Il aura fallu **deux temps**, et le premier ne suffisait pas :

1. **charger la planche avant de dessiner** (le relais du créneau 4). La
   sonde a prouvé que le relais s'exécutait — `charger ecx=0x2D` passait
   désormais devant les `id vignette` — et les cases restaient noires dix
   secondes plus tard ;
2. **l'interroger à chaque trame** (`0x180187CC0`). Le chargement est
   asynchrone, et l'état 41 de `CUST_MAIN` est le seul endroit du moteur qui
   attend une planche. Pendant le sélecteur, **personne ne l'interroge** —
   et une planche que personne n'attend n'arrive jamais. Le relais pose donc
   la question à chaque dessin : `pret ? id=0x2D` compte 1 560 passages.

C'est le fait à retenir du chantier : dans ce moteur, **demander ne suffit
pas, il faut attendre**.

## 3.15 LE CURSEUR : la sous-page, et une fenêtre de 51 trames

La sonde a désigné le verrou que l'analyse statique ne pouvait pas voir :

    repartiteur  id=0xFE006B70  1138 passages   <- la tache mere
    repartiteur  id=0xFE006E10  1136 passages   <- +0x2A0 : CharSelector
    curseur H    COMPTE=18      1137 passages   <- la MERE, et elle seule
    curseur V    COMPTE=1 / 9 / 6               <- TERMINAL, menu principal,
                                                   Customization menu

La sous-page `CharSelector` est répartie autant que la mère et n'a **jamais**
de compte — alors que c'est **son** curseur que l'écran lit
(`0x1801CF1BF mov eax, [rdi+0x2FC]`, soit `[sous-page + 0x5C]`).
`0x1801D0B80` lui pose pourtant ses dix-neuf crans
(`[objet + 0x2A0 + 0x22C] = 18`), et son entrée `0x1801D0260` les efface.

**Aucune lecture d'une seule fonction ne pouvait les rapprocher** : la pose
et l'effacement vivent dans deux fonctions différentes, et
`curseur_customize.py` n'en examine qu'une à la fois. D'où le quatrième
effacement neutralisé — 12 octets en `0x1801D0262`.

Et la mesure du mécanisme, elle, est désormais nette :

    curseur V t=36.6 COMPTE=9 curseur=0  rep=0x004000 front=0x004000
    curseur V t=36.6 COMPTE=9 curseur=1  <<< A BOUGE

`0x4000` = bit 14 = BAS. Le déplacement, le masque de répétition et
l'écriture du curseur fonctionnent parfaitement — quand la page a un compte.

**Ce qui n'est toujours pas mesuré** : gauche/droite dans le *Character
Select*. La trace montre que cet écran n'a été actif que **51 trames**,
autour de t=42,6, parce que le démarrage du jeu avait décalé tout le
scénario de trois secondes et demie — les six appuis prévus à t=48..54 sont
tombés dans l'écran suivant. Un instant précis ne résiste pas à un démarrage
qui varie : le scénario martèle maintenant gauche/droite de t=40 à t=58, en
alternant, pour couvrir la fenêtre quel qu'en soit le décalage.

## 3.16 GAUCHE / DROITE DANS LE *CHARACTER SELECT* : mesuré, et vu à l'écran (2026-10-01)

C'est la question qui restait ouverte depuis §3.15. Réponse : **oui, elles
fonctionnent**, et pas seulement dans la trace — à l'écran.

Le martèlement a couvert la fenêtre, cette fois :

    curseur H  t= 44.7  COMPTE=18  curseur=0    rep=0x008000  page=0x19A64047EF0
    curseur H  t= 44.7  COMPTE=18  curseur=0    rep=0x008000  page=0x19A64048190
    curseur H  t= 44.8  COMPTE=18  curseur=18  <<< A BOUGE
    curseur H  t= 45.9  COMPTE=18  curseur=18   rep=0x002000
    curseur H  t= 46.0  COMPTE=18  curseur=0   <<< A BOUGE
    ... dix-huit fois, jusqu'a t=61,6

Trois faits s'y lisent.

**1. Le compte est posé, et il vaut 18.** `COMPTE=18`, soit dix-neuf crans
(0..18) : c'est exactement la valeur que `0x1801D0B80` pose et que
`0x1801D0260` effaçait avant `--customize-curseur`. La neutralisation tient.

**2. Les DEUX pages bougent ensemble.** `0x19A64048190 - 0x19A64047EF0 =
0x2A0` : la mère et la sous-page `CharSelector`. C'est bien la sous-page —
celle qui n'avait jamais de compte, celle dont le curseur est lu par
`0x1801CF1BF mov eax, [rdi+0x2FC]` — qui se déplace maintenant en même temps
que sa mère.

**3. Les codes de direction.** `0x8000` = bit 15 = GAUCHE (décrémente, et
depuis 0 reboucle sur 18) ; `0x2000` = bit 13 = DROITE (incrémente, et depuis
18 reboucle sur 0).

**La preuve à l'écran** est dans deux captures prises à quatre secondes
d'intervalle sur le même écran : `vignettes_t046.png` montre **Akira**
(cran 0), `vignettes_t050.png` montre **T-Arashi** (cran 18). Le nom change.

### La preuve qui n'était pas demandée : les vignettes suivent la sélection

`vignettes_t070.png` est la meilleure image de la séance. Le scénario a
laissé le curseur sur **T-Arashi**, et le *Costume settings* affiche **les six
costumes de Taka-Arashi** — le mawashi blanc, le yukata, le kimono noir, le
costume de ville, la tenue rouge, le short bleu. Pas ceux d'Akira.

Le journal dit comment : `decharger #5 id=0x1C8` puis `charger #15 id=0x1C8`
(456). Le relais de `GRE_COS` relit `[rax+0x116]` à chaque trame, voit que le
personnage a changé, décharge l'ancienne planche et demande la nouvelle. La
mémoire ne grossit pas et la bonne planche arrive : la paire
décharger/charger du correctif fait son travail sur un cas réel, pas
seulement sur le cas de démarrage.

### Ce que cette mesure ne prouve PAS, et le scénario corrigé

Le martèlement **alternait** gauche et droite. Or gauche depuis 0 et droite
depuis 18 rebouclent toutes deux sur l'autre extrémité : le curseur n'a donc
jamais visité un seul cran intermédiaire, il a fait dix-huit allers-retours
entre les deux butées.

« Il décrémente avec rebouclage » et « il saute à la butée » produisent
**exactement la même trace**. Les deux lectures sont vivantes, et rien dans
cet essai ne les sépare.

Le scénario de `tools/sonde_vignettes.py` **groupe** désormais les
directions : douze droites de suite (t=40,0 à t=53,2) puis six gauches
(t=54,4 à t=60,4). Douze droites consécutives doivent donner douze
personnages consécutifs — ce qu'aucun saut à la butée ne peut imiter. Les
cinq captures de t=42 à t=58 sont espacées d'un peu plus de trois appuis :
chacune doit porter un nom différent, et plus loin dans la liste que la
précédente.

## 3.17 LA CINQUIÈME FORME : quand il n'y a rien à neutraliser (2026-10-01)

Constat de Frédéric, à l'écran, qui ferme la question de §3.16 et en ouvre une
autre :

> « gauche et droite ne fonctionnent que sur l'écran Character Select, mais
> sur aucun autre écran du mode terminal »

### Ce que le relevé disait depuis le début, en une ligne qu'il fallait lire

`tools/curseur_customize.py` imprime, pour le *Costume settings* :

    TaskCostumeMenu   -> HORIZONTAL : 0, et jamais rien d autre

Les quatre entrées de `CUSTOMIZE_CURSEUR` avaient toutes la même forme — poser
puis effacer — et je cherchais cette forme-là. Celle-ci n'efface rien : **elle
n'a jamais rien posé**. Il n'y avait donc aucun `nop` à écrire, et c'est
précisément pour cela que la page est restée dans l'angle mort.

### Et pourtant le compte existe, le moteur le calcule lui-même

L'entrée `0x1801CB430` construit la liste des costumes **disponibles** :

    rdi = 0..4 : 0x18014D730(perso, rdi)  « ce type est-il débloqué ? »
                 si oui -> [rbx + 0x428 + n*8] = rdi ; n = [rbx+0x420]++
    rdi = 5..9 : au premier débloqué -> on range 5 (le « Type S »), on s'arrête

`[rbx+0x420]` est le nombre de vignettes. Ce n'est pas une déduction : la
boucle de dessin en fait sa borne, et tire chaque identifiant de la liste.

    0x1801C91F0  cmp qword [r15+0x420], rsi   ; la borne
    0x1801C9219  lea r14, [r15+0x428]         ; la liste
    0x1801C929B  mov rcx, [r14]
    0x1801C929E  call 0x1801CB030             ; l'identifiant de vignette
    0x1801C92F0  add r14, 8                   ; une vignette par entrée

**Et le curseur est bien l'indice de cette liste** : le cadre de sélection est
posé à `imul eax, [r15+0x5c], 0x7b` (`0x1801C9317`) — le même pas de 0x7B que
les vignettes (`add rdi, 0x7b`). Le compte à poser est donc `nombre − 1`,
comme partout ailleurs.

Puis, cinq instructions après avoir fini de compter :

    0x1801CB53A  mov [rbx+0x22c], ebp    ; ebp = 0

### Le correctif : `CURSEUR_REBATI`

On ne peut pas se contenter de `nop` — il n'y a rien à retirer, il faut
**écrire le calcul**. D'où une troisième table dans `patch_moteur.py`, où
l'ancien et le neuf font le même nombre d'octets, tous deux vérifiés par
désassemblage :

    0x1801CB53A  mov  eax, [rbx+0x420]      ; le compte que le moteur a fait
    0x1801CB540  test eax, eax
    0x1801CB542  je   0x1801CB546           ; liste vide -> on laisse zéro
    0x1801CB544  dec  eax
    0x1801CB546  mov  [rbx+0x22c], eax
    0x1801CB54C  mov  byte [rbx+0x230], 1   ; et ça boucle
    0x1801CB553  nop

**Vingt-six octets, et le droit d'en prendre treize de plus.** La séquence
effacée en compte vingt-six, dont les treize derniers remettent à zéro le
**vertical**, qui est *déjà* à zéro : `0x1801CB458` et `0x1801CB45E` l'ont
fait en tête de fonction, rien ne les réécrit entre les deux, et aucune des
cinq cibles de saut de la fonction ne tombe dans l'intervalle depuis
l'extérieur. On récupère donc leurs treize octets.

**Le garde-fou du zéro.** Sans le `test/je`, une liste vide donnerait `dec 0`
= −1, c'est-à-dire un compte énorme et un curseur parti dans le décor.

### Les pages encore sans compte, et ce qui manque pour trancher

| page | axe | état |
|---|---|---|
| `TaskCostumeMenu` | horizontal | **réparé ci-dessus** |
| `CharSelector` | vertical | aucune valeur posée nulle part dans le binaire |
| `DataSelector` | vertical | aucune valeur posée — mais voir ci-dessous |
| `TaskSelPartMenu` | les deux | aucune valeur posée |
| `TaskSelItemMenu` | les deux | aucune écriture du tout |

`DataSelector` — les cinq lignes `— — —` du premier écran — mérite une
réserve. Sa mise à jour `0x1801CEE60` appelle bien le répartiteur
`0x1801BBBE0` : le mécanisme est branché, seul le compte manque. Mais sur les
captures, **les cinq lignes sont vides**. Deux lectures tiennent debout :

1. le compte a été retiré comme ailleurs ;
2. le compte est le nombre de données **enregistrées**, et il vaut
   légitimement zéro faute de carte.

Rien dans le binaire ne les sépare, et je n'invente pas de valeur. Ce qui les
séparerait : une sonde qui imprime `[sous-page+0x224]` **et** le nombre
d'enregistrements du tableau `0x180752620` (fiches de 0x388 octets, indexées
par `[mère+0x5544]`). Tant que ce n'est pas mesuré, `DataSelector` reste
ouvert.

## 3.18 LES ÉCRANS RESTANTS : une correction, et une source d'entrée entière qui manque (2026-10-01)

Constat de Frédéric après vérification à l'écran :

> « droite gauche fonctionne sur les écrans "character select" et "costume
> settings", mais pas sur les autres. Aucune direction ne fonctionne sur les
> écrans "select part" et "select item". »

Le *Costume settings* de §3.17 est donc **validé**. Restent trois pages.

### Une correction : le piège des fragments `.pdata`, encore

J'ai d'abord relevé que `TaskSelPartMenu::update` **n'appelait pas** le
répartiteur `0x1801BBBE0`, et j'allais en faire un diagnostic. C'est faux. Le
relevé balayait le fragment `.pdata` de l'entrée, `0x1801C7670..0x1801C7884` —
et l'appel est ailleurs : `SelPartMenu::update` appelle `0x1801C7D00`, qui
appelle le répartiteur en `0x1801C7D34`. Même chose pour
`TaskCostumeMenu::update` (`0x1801C70CF`, hors du fragment
`0x1801C6F50..0x1801C6FB1`), dont le curseur marche pourtant.

**Une entrée `.pdata` n'est pas une fonction.** C'est écrit dans le dossier
depuis le début, et je me suis fait prendre quand même. La liste des appelants
de `0x1801BBBE0` (`pe_disasm xref`) l'aurait dit tout de suite — c'est elle
qu'il faut interroger, pas un balayage par fragment.

### `DataSelector` — réparé, et la réserve de §3.17 est levée

J'écrivais en §3.17 que deux lectures tenaient debout, dont « le compte vaut
légitimement zéro faute de données ». **C'est faux**, et la mesure le dit.

La page a un **second chemin d'entrée**, par message :

    0x1801CEE87  movzx edx, byte [rax]   ; le type du message
    0x1801CEE8A  sub dl, 3 ; cmp dl, 1   ; types 3 et 4
    0x1801CEE92  movzx edx, byte [rax+2]
    0x1801CEE96  mov [rdi+0x58], edx     ; LE MEME CURSEUR

Or l'octet de type de ce message (`0x180752248`) n'est écrit **qu'une seule
fois dans tout le binaire** : en `0x180004D97`, et c'est pour le mettre à
zéro. Personne ne poste jamais 3 ni 4. Les **deux** chemins d'entrée de cette
page sont coupés.

Quatre mesures indépendantes autorisent à poser la valeur :

1. la boucle de dessin se referme sur `0x1801CFB20 inc esi ; cmp esi, 5 ; jl`
   — **cinq lignes, un littéral**, sans dépendance aux données ;
2. le cadre de sélection est placé à `0x1801CF88F mov ecx,[rbx+0x58] ; lea
   edx,[rcx+rcx*8] ; shl edx,2` — curseur × 36 pixels, le montage même des
   vignettes ;
3. la mise à jour appelle le répartiteur (`0x1801CEECD`) ;
4. l'accepteur vertical (créneau 7) est `0x1801BD080`, le normal.

Correctif : dix-sept octets à écrire pour douze disponibles, donc un **relais
dans la greffe** (zone `GRE_DSEL`), comme pour les vignettes. Les douze octets
de `0x1801D029C` deviennent `jmp` + `nop`.

### `TaskSelItemMenu` et `TaskSelPartMenu` — le compte ne suffirait pas

Ces deux-là sont d'une autre espèce, et il faut le dire avant d'y toucher :
**leur dessin ne lit pas le curseur du répartiteur.**

| page | état de navigation | ce que le dessin lit |
|---|---|---|
| `TaskCostumeMenu` | `+0x5C` | `imul eax, [r15+0x5c], 0x7b` |
| `DataSelector` | `+0x58` | `[rbx+0x58] * 36` |
| `TaskSelItemMenu` | `+0x9D0` + `+0x9C8` | `0x1801C8139 : [rcx+0x9d0] + [rcx+0x9c8]` |
| `TaskSelPartMenu` | `+0xEE0` | `0x1801CA140 : [rdi+0xee0]` |

Leur répartiteur est pourtant branché (`0x1801C7639` et `0x1801C7D34`) et
leurs accepteurs sont les normaux. Mais leur **grille** a sa propre position,
et le seul code qui la déplace est le consommateur de message :

    0x1801C7B7B  sub dl, 9 ; cmp dl, 1    ; types 9 et 10
    0x1801C7B83  movzx ecx, word [rax+6]
    0x1801C7B87  mov [rdi+0x9d0], rcx

Types 9 et 10 : **jamais postés**, comme les types 3 et 4. Leur producteur —
vraisemblablement le panneau tactile ou le lecteur de carte de la borne — a
été retiré en bloc.

Leur poser un compte ferait bouger `+0x58`/`+0x5C`, que **rien ne dessine et
rien ne relit** : `0x1801C7BF4` recalcule `+0x58` depuis la grille à chaque
trame, donc le déplacement serait effacé à la trame suivante. Ce serait un
curseur invisible.

Les réparer demande d'écrire la **liaison** `+0x58`/`+0x5C` → grille, c'est-à-
dire du code neuf qui n'a jamais existé dans ce binaire, avec deux inconnues
à mesurer d'abord : la géométrie de chaque grille (`SelItem` : 0x28 cases
visibles, défilement par 8 ; `SelPart` : **CINQ** catégories — « 24 » était
faux, corrigé le 2026-10-03, journal (99) : `0x1801C7D9F cmp rcx, 4 ; ja`
le dit littéralement — drapeaux de disponibilité en `+0xEC1`) et le point exact où recopier sans défaire le
défilement. Rien n'est posé tant que ce n'est pas mesuré.

---

# LE DÉCOR ARRIVE UNE ÉTAPE TROP TÔT (2026-10-12)

Constat de Frédéric, captures à l'appui :

- **console** : `Character Select` (Akira, NEW DATA / No custom data / --- / ---
  / ---) s'affiche **par-dessus le MENU PRINCIPAL**, sans décor ;
- **console, étape suivante** : un menu `Customize` — *Customize items* /
  *Edit data name* — toujours sur le menu principal, avec la fiche de la
  donnée (« Auburn », Vanessa, Main Costume Type A) ;
- **APM3** : le `Character Select` s'affiche **sur le décor 3D déjà chargé**.

> « le décor en 3D s'affiche trop tôt, et il manque une étape ».

## LA MESURE : DEUX SÉQUENCEURS, DEUX ORDRES

La pierre de Rosette tient, et elle est franche : **la fonction qui crée
`CUST_MAIN` est la même dans les deux builds**, instruction pour instruction.

| APM3 `0x1801C3350` | Xbox 360 `0x8222B7E0` |
|---|---|
| `lea rdx, "CUST_MAIN"` (`0x18052FB38`) | `addi r4, r11, 0xA48` → `0x82010A48` |
| `lea rcx, 0x1807521A0` | `addi r3, r10, 0x545C` → `0x829B545C` |
| `call 0x180245830` | `bl 0x823AD378` |
| `test al,al ; je` | `clrlwi ; cmplwi ; beq` |
| `[rbx+0x68]=rsi ; [rbx+0x70]=rdi ; [rbx+0x5C]=0` | `[r31+0x58]=r30 ; [r31+0x5C]=r29 ; [r31+0x50]=0` |

**Ce qui diffère, c'est le séquenceur.**

### Le nôtre — `0x1801C4D60`, piloté par `[objet+0x00]`

| étape | ce qu'elle fait |
|---:|---|
| **0** | `0x18018FB20(0, "STAGE_TASK")` — **LE DÉCOR** |
| 1 | attendre `0x18018FE50()`, puis `0x1800D7130(1)` |
| 2 | attendre `0x1800D9020()`, puis `[objet] = 10` |
| 10 | `0x1801C3350` → **`CUST_MAIN`** |
| 11 | BGM `vfes_bgm_cus.adx` |
| 12 | attendre la fin de `CUST_MAIN` |
| 40 | rendre vrai → mode 4 MENU |

### Celui de la console — `0x8222B8A8`, piloté par `[r31+0x4C]`

Cinq étapes (0 à 4), plus l'étape `0x28` (40) de sortie — un compteur qu'on
**incrémente** (`addi r11, r11, 1`), pas une table à numéros épars :

| étape | code | ce qu'elle fait |
|---:|---|---|
| **0** | `0x8222B8F4` | **attendre DEUX écrans** : `0x8239BAA8([r31+0x54])`, puis `0x8239BAA8(0x26B)` et `0x821C5CB8(0x20B)` ; ensuite `0x8222C3F8` (rend l'objet `0x829B54C8`) et `0x8222E138` |
| **1** | `0x8222B950` | `0x8239C508("STAGE_TASK", 0)` — **LE DÉCOR**, et seulement ici |
| 2 | `0x8222B984` | `0x8239C788()` puis `0x822AF548(0x1A)` |
| 3 | `0x8222B9AC` | … |
| 4 | `0x8222B9C4` | … |
| 40 | `0x8222B9D8` | la sortie |

> **Le décor est l'étape 1 sur console, l'étape 0 chez nous.** Et l'étape 0 de
> la console — celle qui tient le `Character Select` puis le menu `Customize`
> pendant que le menu principal est encore à l'écran — **n'existe pas** dans
> notre séquenceur. Les deux symptômes de Frédéric sont la même cause.

## CE QU'IL RESTE À MESURER AVANT DE TOUCHER

1. **Ce que sont les tâches `0x26B` et `0x20B`** que l'étape 0 attend. Les
   mêmes fonctions servent ailleurs avec d'autres identifiants
   (`TaskSelChara::update` X360 : `0x144` vers `0x8239BAA8`, `0x112` vers
   `0x821C5CB8`), et notre sélecteur appelle `0x180187CC0` avec `0x26` et
   `0x113` — la correspondance des identifiants est à établir.
2. **Ce que fait `0x8222E138`**, appelée en fin d'étape 0 : une vraie fonction
   (placement 2D, `bl 0x82378830`), probablement l'ouverture de l'écran.
3. **Si nos équivalents sont atteignables.** `TaskDataSelector`, `CharSelector`
   et `DataSelector` existent chez nous (vtables `0x180530FF0`, `0x180530F30`,
   `0x180530F90`) et sont construits en singletons par l'initialiseur statique
   `0x1802441A0` — donc présents, mais activés par un chemin qu'il faut
   trouver. `DataSelector` porte « les CINQ lignes de données du premier
   écran », exactement les cinq de la capture console.

**On ne déplace pas l'étape du décor avant d'avoir ces trois réponses** :
intervertir 0 et 10 à l'aveugle donnerait un `CUST_MAIN` sans décor chargé,
pas l'écran de la console.


---

# LE CORRECTIF : `--terminal-ordre` (2026-10-12)

La réserve posée plus haut — « on ne déplace pas l'étape du décor avant d'avoir
ces trois réponses » — est **levée par une mesure plus simple que les trois
questions**, et c'est la bonne nouvelle : il n'était pas nécessaire de savoir
ce que valent `0x26B` et `0x20B`, puisque **l'étape 0 d'APM3 est déjà celle de
la console, à l'identique**. Ce qui manquait, ce n'était pas une étape à
écrire : c'étaient trois étapes **vidées**, dont le contenu avait simplement
été remonté d'un cran.

## LES TROIS CAS VIDÉS, EN ENTIER

    cas 1    0x1801C2F40  mov dword [rbx+0x58], 2
             0x1801C2F47  movzx eax, dil ; mov rbx,[rsp+0x30] ; add rsp,0x20
                          pop rdi ; ret
    cas 2    0x1801C2F56  mov dword [rbx+0x58], 3        puis le même épilogue
    cas 3/4  0x1801C2F6C  mov byte [rbx+0x5C], 1
                          mov dword [rbx+0x58], 10       puis le même épilogue

## LES DEUX TABLES

    dwords  0x1801C2FBC : 1C2EF8 1C2F40 1C2F56 1C2F6C 1C2F86 1C2FA8 1C2FAB
    octets  0x1801C2FD8 : 00 01 02 03 03 06 06 06 06 06 04 06 ... (×29) ... 05

Les dwords sont des **offsets 32 bits depuis `0x180000000`** : la greffe y est
atteignable sans détour. Les états **3 et 4** partagent le quatrième dword ;
l'état 4 n'étant jamais atteint, le détour les sert tous les deux sans effet.

## LE SÉQUENCEUR DU MODE, ÉTAPE 0 → ÉTAPE 10

    0x1801C4D90  22 octets  ->  c7 06 0A 00 00 00   mov dword [rsi], 10
                                eb 1A               jmp 0x1801C4DB2
                                90 × 26
    0x1801C4DB2  cmp dword [rsi], 0x28 ; setge al ; add rsp,0x20 ; pop rsi ; ret

Avec `[rsi] = 10`, `setge` rend 0 : « pas fini », exactement ce que faisait
l'étape 0 d'origine après son `inc`.

## CE QUE L'ÉCRAN A DIT, ET CE QU'IL RESTE

La lucarne 3D de `CUST_MAIN` occupe **40,86 % de la largeur** — 784 px à
1920×1080, 523 px à 1280×720, **même fraction** : c'est la zone où le
personnage pose dans `Select Part`, et non un défaut d'affichage. Le gris
`0x606060` à sa droite est la place de l'interface, encore vide pendant les
deux écrans de sélection. **Sur console, c'est le menu principal qui occupe
cette place** : il y reste visible pendant tout le `Customize`, alors que chez
nous il est démonté à l'entrée du mode. C'est l'écart qui subsiste, et le menu
`Customize` (*Customize items* / *Edit data name*) reste absent — deux
chantiers distincts de l'ordre du décor.
