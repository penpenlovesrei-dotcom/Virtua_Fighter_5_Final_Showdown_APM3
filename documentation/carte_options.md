# HELP & OPTIONS — première carte

Établi le 2026-09-05 sur `vf5fs-pxd-w64-Retail_APM3.dll`. Zone lue d'un bloc :
`0x1801A6000`–`0x1801AC000`, 5 904 lignes de désassemblage.

C'est l'entrée **7** du menu console (libellé `0x180`, « HELP & OPTIONS »),
qui appelle `0x1801AB3A0` depuis `0x1801DE0D1`.

---

## 1. Une fabrique, deux pages

`0x1801AB3A0(mode, type, drapeau)` ouvre **l'une ou l'autre** de deux pages :

    type == 2 et mode != 0  ->  page 0x1807513C8, scene "OPTION CONTROL"
    sinon                   ->  page 0x1807513C0, scene "OPTION"

Elle a **huit appelants** : le menu console (`0x1801DE0D1`), `0x18016ECA1`,
`0x1801E3DA7`, `0x1801E8424`, `0x1801F81F6`, `0x18020790A`, `0x180207945`,
`0x18020E486`. L'écran d'options est donc partagé avec d'autres contextes
(pause, terminal…), ce qui compte pour la portée de tout correctif.

| page | singleton | taille | constructeur | vtable |
|---|---|---:|---|---|
| OPTION | `0x1807513C0` | 0x1570 | `0x1801A6120` | `0x180411348` |
| OPTION CONTROL | `0x1807513C8` | 0x438 | `0x1801A6490` | `0x180411188` |

### Les vtables

| créneau | OPTION | OPTION CONTROL |
|---|---|---|
| +0x00 destructeur | `0x1801A67B0` | `0x1801A68C0` |
| +0x08 init | `0x1801AA7C0` | `0x1801AA8A0` |
| +0x10 mise à jour | `0x1801A6F70` | `0x1801A7220` |
| +0x18 entrées | `0x1801A8140` | `0x1801A8160` |
| +0x20 dessin | `0x1801A8420` | `0x1801A8560` |
| +0x28, +0x30 | bouchon `ret 0` | bouchon `ret 0` |
| +0x38 | — | `0x1801AB820` |
| +0x40 | — | `0x1801AA620` |
| +0x48 | — | bouchon `ret 0` |
| +0x50 validation | — | `0x1801A7ED0` |

`OPTION` n'a que sept créneaux : sa validation vit dans sa mise à jour, pas
dans un créneau séparé.

---

## 2. Les six lignes, et où elles mènent

Le tableau des libellés est posé par le dessin `0x1801A9DC0`, six mots à
`[rsp+0x40]` — et **le dernier est un doublon** :

    0x1801A9E02  mov dword [rsp+0x40], 0x2F1
    0x1801A9E0A  mov dword [rsp+0x44], 0x2F2
    0x1801A9E12  mov dword [rsp+0x48], 0x2F3
    0x1801A9E1A  mov dword [rsp+0x4C], 0x2F4
    0x1801A9E22  mov dword [rsp+0x50], 0x2F5
    0x1801A9E2A  mov dword [rsp+0x54], 0x2F5     <- le meme

L'aiguillage est dans la mise à jour `0x1801A6F70`, sur `[page+0xB8]` (l'entrée
choisie), gardé par `[page+0xC0]` (la validation) :

| # | libellé | id | site | scène ouverte |
|---:|---|---|---|---|
| 0 | How to Play | `0x2F1` | `0x1801A703B` | `OPTION HOWTO` |
| 1 | Controls | `0x2F2` | `0x1801A707E` | `OPTION CONTROL` |
| 2 | Settings | `0x2F3` | `0x1801A70D0` | `OPTION SETTING` |
| 3 | Save Data | `0x2F4` | `0x1801A7116` | `OPTION FILE` |
| 4 | Credits | `0x2F5` | `0x1801A71D8` | page via `0x1801B11C0` |
| 5 | (doublon de Credits) | `0x2F5` | `0x1801A715C` | `OPTION INFO` |

**Aucune de ces six branches n'est bouchonnée.** Chacune démarre une scène par
`0x180245830` et retombe proprement si elle échoue. C'est différent du menu
principal, où `ACHIEVEMENTS` sautait vers un `ret 0`.

Reste à vérifier à l'écran : combien de lignes sont réellement dessinées (5 ou
6), et laquelle des deux entrées `Credits` est atteignable.

---

## 3. Ce que contiennent les sous-pages

Tous les identifiants de texte de la zone, résolus :

**Settings** (`OPTION SETTING`)

| id | texte |
|---|---|
| `0x2F6` | Volume: Sound Effects |
| `0x30C` | Volume: Music |
| `0x2F7`–`0x30B` | les valeurs 0 à 20 |
| `0x32A` | Autosave (`0x32B` OFF, `0x32C` ON) |

**Controls** (`OPTION CONTROL`)

| id | texte |
|---|---|
| `0x32D` / `0x32E` | 1P Controls / 2P Controls |
| `0x33D`–`0x341` | L1, L2, L3, R1, R2 |
| `0x34F` | NO USE |
| `0x359` | Vibration (`0x35A` OFF, `0x35B` ON) |
| `0x35C` | Type — `0x35D` Standard, `0x35E`–`0x362` Arcade stick 1 à 5 |
| `0x363` | Test settings |
| `0x364` / `0x365` | Exit |

**Save Data** (`OPTION FILE`)

| id | texte |
|---|---|
| `0x366` / `0x367` | Save / Load |
| `0x368` | Delete save data |
| `0x369` | Change storage device |
| `0x36A` / `0x36B` | New / Create a new one. |

**How to Play** (`OPTION HOWTO`) — trois pages

| id | texte |
|---|---|
| `0x36D` | Three ways to win! |
| `0x36E` | les trois conditions de victoire |
| `0x36F` / `0x370` | Health Bar / Time Limit |
| `0x371` | The basic controls! |
| `0x372`–`0x377` | Punch, Kick, Throw, déplacement, START |
| `0x379` / `0x37A` | les prises passent la garde ; la liste de coups |
| `0x37B` | Guard yourself well! |
| `0x37C`–`0x37F` | garde debout, garde accroupie, ce qu'elles couvrent |
| `0x380` | renvoi vers le Dojo |

Note : `0x36C`, le texte de l'avertissement épilepsie, appartient à la même
plage — mais il est dessiné par l'écran de chargement, pas par les options
(voir `menu_console.md` §18).

---

## 4. Le curseur, de bout en bout

`[page+0xB8]` et `[page+0xC0]` ne sont pas des champs de la page : ce sont le
`+0x58` et le `+0x60` de la **sous-page `OPTION MENU`**, construite à
`page+0x60` avec la vtable `0x1804110A8` (constructeur `0x1801A6120`,
`0x1801A615E lea rax -> 0x1804110A8`). D'où l'échec de toute recherche sur
`+0x284` : la liste s'adresse par son propre `this`.

| créneau | fonction | bornes |
|---|---|---|
| +0x08 init | `0x1801AAFF0` | |
| +0x10 mise à jour | `0x1801A7A70` – `0x1801A7C18` | |
| +0x18 entrées | `0x1801A82D0` – `0x1801A82FE` | |
| +0x20 dessin | `0x1801A9DC0` | le tableau des six libellés |
| +0x50 validation | `0x1801A8090` – `0x1801A80D4` | |

### Combien de lignes : 3 ou 5, selon d'où l'on vient

L'init lit le **type** passé à la fabrique, rangé en `0x1807513B8` :

    0x1801AB02B  cmp   dword [0x1807513B8], 1
    0x1801AB03E  mov   eax, 4
    0x1801AB043  cmove eax, ecx           ; ecx = 2
    0x1801AB046  mov   [liste+0x224], eax ; le DERNIER INDICE

Le menu console appelle `0x1801AB3A0(0, 0, 1)` :

    0x1801DE0C5  cmp  ecx, 7          ; l'entree HELP & OPTIONS
    0x1801DE0CA  mov  r8b, 1          ; drapeau : remettre le curseur a zero
    0x1801DE0CD  xor  edx, edx        ; type = 0
    0x1801DE0CF  xor  ecx, ecx        ; mode = 0
    0x1801DE0D1  call 0x1801AB3A0

`type = 0`, donc dernier indice **4** : **cinq lignes** depuis le menu console,
et la sixième étiquette (le doublon de `Credits`) n'est jamais dessinée.
Ailleurs — en pause, par exemple — le type peut valoir 1 et la liste se réduit
à **trois** lignes.

L'init lit aussi le mode courant : `0x1801AB002 call 0x1800DA7E0 ; cmp [rax], 4
; setne bl`, et passe ce booléen à `0x1801BE860` et `0x1801BE7E0`. La page ne
s'habille donc pas pareil selon qu'on vient du menu (mode 4) ou d'ailleurs.

### Qui bouge le curseur

C'est **le curseur partagé du moteur**, celui du menu principal
(`menu_console.md` §17) :

    0x1801A7B2C  cmp  byte [liste+0x2F8], 0
    0x1801A7B33  jne  0x1801A7B3D          ; <- la garde
    0x1801A7B38  call 0x1801BBBE0          ; masques 0x11000 et 0x88000

`0x1801BBBE0` avance `[liste+0x58]` dans `[0, liste+0x224]`, et
`[liste+0x5C]` dans `[0, liste+0x22C]`.

### La validation

    0x1801A8090  ...
    0x1801A80BE  mov  eax, [liste+0x58]     ; le curseur
    0x1801A80C1  mov  [liste+0x2F8], eax    ; <- ce que la garde relira
    0x1801A80C7  mov  byte [liste+0x2F0], 1

Valider range donc le curseur dans `+0x2F8`, et c'est ce champ qui gèle
ensuite la navigation.

### Une asymétrie, à vérifier à l'écran

`+0x2F8` reçoit **la valeur du curseur**, et la garde le teste contre zéro.
Pour les entrées 1 à 4, `+0x2F8 != 0` et la liste se fige — c'est voulu. Mais
pour l'**entrée 0 (`How to Play`)**, `+0x2F8` vaut 0 : la garde ne se ferme pas.

Prédiction, non vérifiée : en ouvrant `How to Play`, les directions
continueraient de déplacer le curseur des options en arrière-plan — le même
défaut que celui corrigé au menu principal. Un essai suffit à trancher :
entrer dans `How to Play`, presser haut/bas, ressortir, et regarder où est le
curseur.

---

## 5. Ce qui n'est pas encore établi

- **`[liste+0x60]`** (= `page+0xC0`), le drapeau que la mise à jour de la page
  teste avant d'aiguiller : la validation ne l'écrit pas, il est posé ailleurs.
- **Les 18 bouchons de la zone**, dont sept `0x180007450` (rend faux) :
  `0x1801A782A`, `0x1801A78DF`, `0x1801A7C2C`, `0x1801AB1E0`, `0x1801ABCCD`,
  `0x1801ABDEF`, `0x1801ABDF8`. Aucun n'est sur le chemin des cinq lignes.
- **Le contenu des sous-pages** (`OPTION SETTING`, `OPTION FILE`, `OPTION
  HOWTO`, `OPTION INFO`) n'est pas lu : seuls leurs libellés le sont.

---

## 6. Valider, annuler : un seul code chacun (2026-09-05)

Établi par la mesure puis par trois essais de Frédéric — « seul A fonctionne
dans le menu, T et R non », « A a la fonction annule », « ENTREE : valider ».

Le curseur partagé `0x1801BBBE0` interroge deux prédicats, chacun ne lisant
**qu'un seul code** de la borne, et appelle deux créneaux distincts :

    0x1801BBCC6  call 0x1801A2B90  (mov edx, 8 = la touche A)   -> +0x48  ANNULER
    0x1801BBCDD  call 0x1801A2BC0  (mov edx, 7 = Entrée)        -> +0x50  VALIDER

Ils rendent **0** si le bouton vient d'être pressé, **-1** sinon — d'où le `js`
de leurs appelants. Pour la liste des options, `+0x48` = `0x1801A6CB0` et
`+0x50` = `0x1801A8090`, ce dernier étant bien le validateur : il enregistre
`[liste+0x2F8] = [liste+0x58]`, l'entrée choisie.

**Donc : Entrée valide, A annule.** `T` et `R` ne sont lus par personne ici.

Attention : la table de `menu_console.md` §10.2, qui donne les bits 0 à 3 comme
« grille : VALIDER », vaut pour la **grille de sélection de personnage**, un
écran qui lit le masque arcade brut. Elle ne s'applique pas à ces menus. Les
étiquettes de créneaux du §1 de ce document venaient de la vtable du menu
principal ; pour cette classe, `+0x48` et `+0x50` sont **inversés**.

### Le raccourci de borne, et pourquoi il cassait tout

    0x1801A7C75  cmp  dword [0x1807513B8], 0  ; type == 0 -> chemin console
    0x1801A7C8E  lea  ecx, [rdx+1]            ; masque 1, le BIT 0 = code 7
    0x1801A7C91  call 0x1801A2CA0             ; ce bouton est-il TENU ?
    0x1801A7CA8  mov  dword [rbx+0x58], 5     ; -> force l'entrée 5, OPTION INFO
    0x1801A7CD4  mov  byte  [rbx+0x2F0], 1    ;    et valide

Sur borne, **tenir START ouvre la page d'informations**. Mais le bit 0 est le
code 7, c'est-à-dire **Entrée — la touche qui valide**. Au moment même où elle
valide, elle est tenue : le raccourci se déclenche et détourne vers l'entrée 5.
C'est exactement ce que la mesure montrait, `entree=5` quatre fois sur quatre.

Au clavier, le geste ne peut pas être distinct. `--options-raccourci` rend le
saut inconditionnel — deux octets, `75` → `eb` — et la navigation ordinaire
reprend.

## 7. Le libellé du menu

`HELP & OPTIONS` (id `0x180`) a été renommé **`OPTIONS`** le 2026-09-05, par
réécriture sur place dans `string_array_en.bin` du `.par`
(`tools/renommer_libelle.py 0x180 "OPTIONS"`, offset `0x100363C`). L'original
est gardé dans `analysis/libelles_renommes.json` ; `--rendre 0x180` le remet.

---

## 8. La disposition des touches (2026-09-05)

Choix de Frédéric : la rangée **W X C V**, sous la main gauche en AZERTY.
Écrite dans `tools/gen_apm_stub.py`, recompilée par `tools/construire_stub.cmd`.

| PlayStation | code borne | clavier (J1) | manette (J2) | rôle établi |
|---|---:|---|---|---|
| directions | 2–5 | flèches | croix directionnelle | curseur |
| START | 7 | **Entrée** | START | **VALIDER** dans les menus |
| SELECT | 6 | Espace | SELECT | pièce — lu par personne dans ces menus |
| carré □ | 8 | **W** | □ | **ANNULER** dans les menus |
| croix ✕ | 9 | **X** | ✕ | combat (code logique 100) |
| rond ○ | 10 | **C** | ○ | combat (102) |
| triangle △ | 11 | **V** | △ | grille : valider (code logique 9) |
| L1 / R1 / R2 | 12 / 13 / 14 | T / Y / U | L1 / R1 / R2 | combat |
| TEST / SERVICE | 0 / 1 | F1 / F2 | — | menu opérateur |
| sortie | 15 | Échap | BACK | quitter le mode courant |

Rappel de la section 6 : dans ces menus le moteur ne lit que **deux** codes —
le 7 pour valider, le 8 pour annuler. `T`, `R`, `V`… n'y sont lus par personne.

**Piège** : `construire_stub.cmd` redéploie `apm_entrees.txt`, qui contient par
défaut un **scénario** pressant START tout seul à 25 s et 33 s. Après toute
reconstruction du stub, remettre `clavier = 1`, `manette = 1` et un seul
`0 rien` — c'est ce qui est en place.

---

## 9. Le menu du Dojo, pour y poser « How to Play »

| # | libellé | id | destination |
|---:|---|---|---|
| 0 | Tutorial | `0x217` | page `0x180754A70` — **vivante**, pas un bouchon |
| 1 | Command Training | `0x218` | scène `COMMAND_TRAINING MENU` |
| 2 | Free Training | `0x219` | ferme le menu et lance l'entraînement |

Classe : vtable `0x180532968`, init `0x1801E4420` (`[+0x224] = 2`, donc trois
lignes), dessin `0x1801E1E40` (les trois libellés à `[rsp+0x40..0x48]`),
valider `0x1801DE440`, annuler `0x1801DB7C0`.

Ajouter une quatrième ligne demande quatre choses : porter `[+0x224]` à 3,
écrire un quatrième libellé dans le dessin, ajouter un cas à l'aiguillage, et
un relais qui ouvre la page d'options en présélectionnant l'entrée 0. Coût
estimé : une cinquantaine d'octets de caverne, alors que celle de `.text` n'a
plus que 23 octets contigus.

**Il y a de la place ailleurs** : le corps du raccourci désactivé par
`--options-raccourci`, `0x1801A7C89`–`0x1801A7CDB`, soit **82 octets** que plus
rien ne peut atteindre (le seul chemin y menait par `0x1801A7C7C`, devenu un
saut inconditionnel). C'est la caverne à utiliser.

---

## 10. La double validation : la fenêtre d'entrée, mesurée (2026-09-05)

Constat de Frédéric : un appui sur Entrée validait deux fois. Deux causes
possibles, séparées par `tools/pister_validation.cmd` :

    Curseur      881
    Predicat     872        -> 0,99 par tour : le curseur tourne UNE fois par trame
    dont presse  2

       9008.5 ms  PREDICAT : presse
       9025.3 ms  PREDICAT : presse      <- 16,8 ms plus tard = UNE TRAME
       9025.9 ms  VALIDER

Le curseur partagé ne tourne qu'une fois par trame : ce n'est pas un double
site d'appel. C'est **la fenêtre de `Input_isOnNow`** du stub.

`Input_isOnNow` n'y est pas un vrai front d'une trame mais une **fenêtre de
temps** (`front` ms) — compromis documenté dans `gen_apm_stub.py` : le vrai
front avait empêché le jeu de sortir d'`APM3_ENTRY`.

| `front` | trames couvertes | effet |
|---:|---|---|
| 150 ms | ~9 | neuf validations par appui |
| 20 ms | 2 | **encore double** — 20 > 16,7 |
| **10 ms** | 1 | une seule |

La règle est simple et il aura fallu la mesurer : **la fenêtre doit être plus
courte qu'une trame**, 16,7 ms à 60 images/s. Trop courte, les appuis se
perdent ; trop longue, ils comptent double.

Le stub relit `apm_entrees.txt` **à chaud** : la valeur s'ajuste pendant que le
jeu tourne. Le modèle `tools/apm_entrees.txt` porte la même valeur, sinon une
reconstruction du stub réintroduirait l'ancienne — et le scénario automatique
qui presse START tout seul à 25 s et 33 s.

---

## 11. La taille du cadre des sous-menus : ce que j'ai cherché (2026-09-05)

Frédéric : « pour moi, la taille des fenêtres des sous menus, c'est du code ».
J'avais répondu « c'est de la donnée » sans vérifier ; voici la vérification.

**Ce qui EST dans le code**, dans le dessin du menu Dojo `0x1801E1E40` :

| valeur | où | rôle |
|---|---|---|
| `32.0` | `0x1801E1F00` → `0x18019B830` | la **taille du texte** (écrit les champs de police `+0x24`…`+0x30`) |
| `3.0` / `4.0` | `0x1801E2007` / `0x1801E2014` | décalages de mise en page, `[rbp-0x2C]` et `[rbp-0x28]` |
| `"head_tit_ct"` | `0x1801E1EEF` | l'ancre du titre, via `0x1801BCD70` |
| `"p_txt_01_lt"` | `0x1801E1FC6` | l'ancre de la première ligne |

**Ce qui n'y est PAS** : aucune géométrie de cadre. Les deux seuls calques
demandés sont des ancres de texte. Et le cadre ne se redimensionne pas avec le
nombre de lignes — `[obj+0x224]` n'est lu que par la boucle de dessin
(`0x1801E2046`, `0x1801E2130`), jamais par un calcul de taille.

**Où il doit donc être** : dans la scène AET `TRAINING MENU` elle-même. Elle
n'est pas dans `aet_c_cmn.bin` (489 Ko, 697 calques, vérifié). Le moteur ne cite
qu'un seul nom de fichier AET, **`aet_db.bin`** — l'index qui dit quelle planche
porte quelle scène.

**Le chemin, si on l'ouvre** : `aet_db.bin` → la planche qui porte
`TRAINING MENU` → le calque du cadre → sa hauteur. Puis le remettre dans le
`.par`, comme pour le renommage du libellé (§7).

Réserve honnête : je n'ai pas trouvé de code qui dimensionne ce cadre, ce qui
ne prouve pas qu'il n'existe pas. Si la piste AET tombe à l'eau, il faudra
chercher un redimensionnement de calque appliqué à la scène après son
démarrage.
