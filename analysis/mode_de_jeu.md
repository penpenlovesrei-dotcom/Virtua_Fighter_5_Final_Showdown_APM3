# Le MODE DE JEU : `0x180751010`

Établi le 2026-09-05, sur `runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll.origine`
(binaire NON patché). Aucun patch, aucun lancement.

---

## 1. La réponse

Le mode de jeu est le **dword global `0x180751010`**. Ce n'est pas un champ de la
session : c'est la première case d'un **bloc de réglages de partie de 16 octets**,
`0x180751010`–`0x18075101F`, écrit d'un bloc au moment où une page de réglages
est validée, et lu ensuite partout dans le combat.

| valeur | mode | posée par |
|---:|---|---|
| **0** | **Arcade** | `TaskMenuArcadeNormal::update` — `0x1801DC3A6` |
| **1** | **Score Attack** | `TaskMenuScoreAttack::update` — `0x1801DD73E` |
| **2** | **License Challenge** | `TaskMenuArcadeLicenceChallenge::update` — `0x1801DC179` |
| **3** | **Special Sparring** | `TaskMenuTeam::update` — `0x1801A4252` |
| 4 | Versus | `TaskMenuVersus::update` — `0x1801DDC43` |
| 5 | *(jamais écrit dans ce build)* | — |
| 6 | Free Training | `TaskMenuTraining::update` — `0x1801DDA61` |
| 7 | Command Training | `TaskMenuCommandTraining::update` — `0x1801DC5A7` |
| 8 | (3ᵉ entrée du DOJO) | `TaskMenuTraining::update` — `0x1801DDA61` |
| 9 | *(jamais écrit dans ce build)* | — |

Les **quatre modes SINGLE PLAYER sont exactement les valeurs 0 à 3**, et le
binaire le dit lui-même : `0x1800B8B9F  call 0x18019C090 ; cmp eax, 3 ; ja` —
« si le mode est ≤ 3, prends les réglages solo ».

Le nom des modes n'est pas déduit : il vient du **RTTI MSVC** du binaire, qui
nomme les vtables des pages (`.?AVTaskMenuScoreAttack@@`,
`.?AVTaskMenuArcadeLicenceChallenge@@`, …). Voir §5.

---

## 2. Le bloc de réglages `0x180751010`–`0x18075101F`

| adresse | taille | rôle | accesseur en lecture |
|---|---|---|---|
| `0x180751010` | dword | **LE MODE DE JEU** | `0x18019C090` |
| `0x180751014` | word | santé max 1P | `0x18019C080` (rend `&0x180751014`) |
| `0x180751016` | word | santé max 2P | idem, `+2` |
| `0x180751018` | byte | limite de temps (× 60 → trames) | idem, `+4` |
| `0x180751019` | byte | nombre de rounds | idem, `+5` |
| `0x18075101A` | byte | niveau CPU | `0x18019C060` |
| `0x18075101B` | byte | annexe **Score Attack** | `0x18019C0A0` |
| `0x18075101C` | byte | annexe **Versus** | `0x18019C0B0` |
| `0x18075101D` | byte | annexe **Training** | `0x18019C070` |
| `0x18075101E` | byte | drapeau, posé à 1 par `0x18019C3C0` | — |
| `0x180751020` | qword | pointeur d'objet (`TaskTips`), sans rapport | — |

Le rôle des quatre premiers octets se lit dans le consommateur, `0x1800B8BA9` :

    0x1800B8B97  call 0x18019C080         ; rbx = &0x180751014
    0x1800B8B9F  call 0x18019C090         ; eax = le mode de jeu
    0x1800B8BA4  cmp  eax, 3
    0x1800B8BA7  ja   0x1800B8BD3         ; modes 4..9 : rien
    0x1800B8BA9  ecx = byte [rbx+4]       ; limite de temps
    0x1800B8BAD  edx = ecx * 0x3C
    0x1800B8BB4  cx  = word [rbx+0] + 1   ; santé 1P
    0x1800B8BBF  cx  = word [rbx+2] + 1   ; santé 2P
    0x1800B8BCB  eax = byte [rbx+5]       ; rounds

et dans le producteur, `TaskMenuArcadeNormal::update` (`0x1801DC317`–`0x1801DC367`),
qui construit ces 6 octets par `0x18019BBE0(dst, w0, w1, b4, b5)` à partir des
cinq réglages de la page (`[page+0x240]` … `[page+0x250]`), dont les libellés
d'aide sont `0x79`–`0x7D` : *Adjust CPU skill level*, *…the number of rounds*,
*…the time limit*, *…the health bar for the player*, *…for the CPU*.

---

## 3. Les cinq écrivains — inventaire EXHAUSTIF

Méthode : **balayage linéaire par motif d'octets** de la section `.text`
(la seule exécutable : `0x180001000`, vsize `0x34475C`), à la recherche de
toute valeur rel32 `disp` telle que `fin_instruction + disp == 0x180751010`.
Ce balayage ne dépend pas de `.pdata` ni des bornes de fonction — il ne peut
donc pas rater une feuille (piège documenté dans `menu_console.md` §13.1).

**Résultat : 8 références en tout**, toutes dans le même pâté de 0x800 octets.

| référence | instruction | nature |
|---|---|---|
| `0x18019BD47` | `cmp ebx, [0x180751010]` | lecture (dans `0x18019BD30`) |
| `0x18019C090` | `mov eax, [0x180751010] ; ret` | **l'accesseur en lecture** |
| `0x18019C1F8` | `mov ecx, [0x180751010]` | lecture (échelle de sauts, dans `0x18019C0C0`) |
| `0x18019C426` | `mov [0x180751010], ecx` | écriture (`0x18019C420`) |
| `0x18019C3D2` | `mov [0x180751010], ecx` | écriture (`0x18019C3D0`) |
| `0x18019C490` | `mov [0x180751010], ecx ; ret` | écriture (`0x18019C490`) |
| `0x18019C4A8` | `mov [0x180751010], ecx` | écriture (`0x18019C4A0`) |
| `0x18019C522` | `mov [0x180751010], ecx` | écriture (`0x18019C520`) |

Aucune autre écriture n'est possible par pointeur : le seul accesseur qui rende
une **adresse** est `0x18019C080`, et il rend `&0x180751014`, pas
`&0x180751010` ; ses quatre appelants (`0x1800B894C`, `0x1800B8B97`,
`0x1800B8F88`, `0x18023EC50`) ne font que **lire**.

### Les cinq setters, en clair

| setter | signature | ce qu'il pose en plus du mode |
|---|---|---|
| `0x18019C420` | `(type, const u8 reglages[6], u8 niveau, bool echanger)` | réglages, `[+0xA] = niveau` ; si `echanger`, `0x1801A3870(0,1)` puis `(1,0)` |
| `0x18019C4A0` | `(type, const u8 reglages[6], u8 annexe, bool echanger)` | réglages, `[+0xA] = 2` **forcé**, `[+0xB] = annexe` |
| `0x18019C520` | `(type, const u8 reglages[6], u8 annexe)` | réglages, `[+0xC] = annexe` |
| `0x18019C3D0` | `(type, u8 annexe, bool demander_mode)` | remet tout à zéro, `[+0xD] = annexe` ; si `demander_mode`, saute sur `0x1800DA9A0(6)` — **mode 6 CS_TRAINING** |
| `0x18019C490` | `(type)` | **rien d'autre** — trois octets, une seule instruction |

`0x18019C3A0(const u8[6])` pose les réglages **sans** toucher au mode ; un seul
appelant, `0x1800B89B6`.

### Les dix-neuf sites d'appel

| site | fonction (bornes `.pdata`) | classe RTTI | mode posé |
|---|---|---|---:|
| `0x1801DC3A6` | `0x1801DC270`–`0x1801DC50A` | `TaskMenuArcadeNormal::update` | **0** |
| `0x1801DCC63` | `0x1801DC620`–`0x1801DCE9D` | `TaskMenuMain::update` | 0 |
| `0x18023A427` | `0x18023A3C0` | chemin APM3 | 0 |
| `0x18023C727` | `0x18023C6D1` | chemin APM3 | 0 |
| `0x1801DD73E` | `0x1801DD6A0`–`0x1801DD799` | `TaskMenuScoreAttack::update` | **1** |
| `0x1801DC179` | `0x1801DC050`–`0x1801DC266` | `TaskMenuArcadeLicenceChallenge::update` | **2** |
| `0x1801A4252` | `0x1801A4160`–`0x1801A42C2` | `TaskMenuTeam::update` | **3** |
| `0x1801DDC43` | `0x1801DDB40`–`0x1801DDCFB` | `TaskMenuVersus::update` | 4 |
| `0x1801DCB6B` | `0x1801DC620`–`0x1801DCE9D` | `TaskMenuMain::update` | 4 |
| `0x1801BB661` | `0x1801BB4A3`–`0x1801BB685` | — (fin de boucle) | 4 |
| `0x1800DE006` | `0x1800DDE00`–`0x1800DE394` | gestionnaire de mode | 4 |
| `0x18023DFBB` | `0x18023DF10`–`0x18023E11C` | chemin APM3 | `rdi+3` (probablement 4) |
| `0x1801DCD19` | `0x1801DC620` | `TaskMenuMain::update` | 6 |
| `0x1801DDAAE` | `0x1801DD9C0`–`0x1801DDB3F` | `TaskMenuTraining::update` | 6 |
| `0x1801DDA61` | `0x1801DD9C0` | `TaskMenuTraining::update` | **6 / 7 / 8** selon `[page+0x58]` |
| `0x1801DCD71` | `0x1801DC620` | `TaskMenuMain::update` | 7 |
| `0x1801DC5A7` | `0x1801DC510`–`0x1801DC5FD` | `TaskMenuCommandTraining::update` | 7 |
| `0x1801DCDBF` | `0x1801DC620` | `TaskMenuMain::update` | 8 |
| `0x18023E198` | `0x18023E180`–`0x18023E1C9` | chemin APM3 | 8 |

Le calcul du DOJO, à `0x1801DDA45`, est la seule valeur non littérale du lot :

    0x1801DDA45  eax = [page+0x58]      ; le curseur de la page DOJO
    0x1801DDA4C  eax == 0  -> ecx = 6
    0x1801DDA53  eax == 1  -> ecx = 7 ; sinon ecx = 8
    0x1801DDA61  call 0x18019C3D0

**Les valeurs 5 et 9 ne sont écrites nulle part** dans ce build, alors qu'elles
sont testées (§7). Ce sont des branches mortes.

---

## 4. La symétrie qui verrouille la lecture

Chaque setter porte un octet annexe différent, et **chaque getter de cet octet
est gardé par le mode qui l'a posé** :

| octet | posé par | lu par | garde du lecteur |
|---|---|---|---|
| `0x18075101A` | `0x18019C420` (modes 0, 2, 3) | `0x18019C060` @ `0x1800B8AD4` | `cmp eax, esi ; ja` (les modes solo) |
| `0x18075101B` | `0x18019C4A0` (mode 1) | `0x18019C0A0` @ `0x1800B6B60` | `0x1800B6B56 : cmp eax, 1` |
| `0x18075101C` | `0x18019C520` (mode 4) | `0x18019C0B0` @ `0x18016C781` | `0x18016C777 : cmp eax, 4` |
| `0x18075101D` | `0x18019C3D0` (modes 6-8) | `0x18019C070` @ `0x1801E51D4` | `0x1801E51AD : sub ecx, 6 ; je` |

Un setter par famille de modes, un getter par famille, et le getter gardé par
la valeur que son setter pose. Il n'y a pas de coïncidence possible.

---

## 5. Comment les noms ont été obtenus : le RTTI

Le binaire est un PE MSVC x64 avec RTTI complet. En reliant
`TypeDescriptor` → `CompleteObjectLocator` → `vftable[-1]`, on obtient **532
vtables nommées**. Les pages de menu :

| vtable | classe |
|---|---|
| `0x180532AE8` | `TaskMenuMain` |
| `0x180532848` | **`TaskMenuArcade`** — la page des quatre modes |
| `0x180532668` | **`TaskMenuArcadeNormal`** — scène `NORMAL MENU` |
| `0x1805326C8` | **`TaskMenuScoreAttack`** — scène `SCOREATTACK MENU` |
| `0x1805327E8` | **`TaskMenuArcadeLicenceChallenge`** — scène `LICENCECHALLENGE MENU` |
| `0x1805328A8` | `TaskMenuVersus` |
| `0x180532908` | `TaskMenuCommandTraining` |
| `0x180532968` | `TaskMenuTraining` — la page DOJO |
| `0x1805329C8` | `TaskMenuReplay` |
| `0x180410C50` | **`TaskMenuTeam`** — la page atteinte par Special Sparring |
| `0x180410BF0` | `TaskMenuSetting` — scène `CARD SELECTOR` |
| `0x1805313A8` | `CTaskClassUpWindow` |
| `0x180532788` | `CTaskDifficultyChangeWindow` |
| `0x1805314C8` | `CLicenceChallengeResultTask` |

La disposition des vtables de page est régulière : `[2]` = mise à jour,
`[3]` = ?, `[4]` = dessin, `[9]` = annuler, `[10]` = valider.

C'est ce tableau qui corrige deux attributions des documents existants :

* `0x1801DD6A0` **n'est pas** « versus » (`vs_gameover.md` §2) : c'est
  `TaskMenuScoreAttack::update`. Le type 1 est donc **Score Attack**, pas versus.
* `0x1805328A8` **n'est pas** la page de réglages arcade (`menu_console.md`
  §19.1) : c'est `TaskMenuVersus`. Elle porte les mêmes cinq réglages, d'où la
  confusion.

---

## 6. La preuve par l'aval

### 6.1 « On enchaîne ou on finit » — `0x1800B1D80` (`0x1800B1D80`–`0x1800B1E33`)

C'est la fonction que l'arbitre appelle pour savoir si la série de combats est
terminée. Elle lit le mode **et lui seul** pour décider du nombre de combats :

    0x1800B1D90  ecx = [session+8]
                 ecx == 0 -> solo (suite ci-dessous)
                 ecx == 1 -> 0x1801A5F50([session+0x3F0])   ; equipe / Special Sparring
                 sinon    -> faux
    0x1800B1DB1  call 0x18019C090
    0x1800B1DB6  cmp  eax, 1                    ; SCORE ATTACK
    0x1800B1DBB  return [session+0x3F0] >= 7     ; SEPT combats
    0x1800B1DD0  call 0x18019C090
    0x1800B1DD5  cmp  eax, 2                    ; LICENSE CHALLENGE
    0x1800B1DDA  n = 0x1801D43C0()              ; nb de combats de la licence courante
    0x1800B1DDF  return [session+0x3F0] >= n
    0x1800B1E03  sinon (ARCADE, mode 0) :
                 si 0x180007450() : return [+0x3F0] >= 3
                 sinon             : return [+0x3F0] >= 8   ; HUIT combats

`0x1801D43C0` lit `[0x1807533B8]` (index de licence, borné à 0x32) et indexe la
table `0x1805319F0`. `0x1801A5F50` lit `[0x180751398]` (index d'équipe, borné à
0x14) et indexe `0x18040B3D8` (pas 0x20).

C'est exactement le « compteur qui décide d'enchaîner » demandé — et il est
gardé par `0x180751010`.

### 6.2 License Challenge — `0x1807533C0` et l'écran de résultat

* **Écriture** : `0x1801D3930` recopie 8 × 0x80 octets vers `0x1807533C0`. Elle
  est appelée par **`0x1801DDDB1`**, c'est-à-dire par la validation de la page
  des modes `0x1801DDD00`, **dans la branche `eax == 2`** — la branche qui ouvre
  `LICENCECHALLENGE MENU`.
* **Lecture** : `0x1801D40A0` (`lea rax, [0x1807533C0] ; ret`) a sept appelants,
  tous dans `0x1801D1C2D`–`0x1801D24A8` (les fenêtres `CTaskClassUpWindow` /
  `CTaskDifficultyInfoWindow`) plus `0x1801E3165`, à l'intérieur de
  `TaskMenuArcadeLicenceChallenge` (créneau `[1]`, `0x1801E3080`).
* **La garde** : l'entrée du sous-état 20 GAMEOVER, `0x1800DC860` :

      0x1800DC875  call 0x18019C090
      0x1800DC87A  cmp  eax, 2
      0x1800DC87D  jne  0x1800DC884
      0x1800DC87F  call 0x1801D2610

  et `0x1801D2610` pousse la scène **`"LICENCE CHALLENGE RESULT"`**
  (`0x180531528`, lue à `0x1801D2636`).

Mode 2 = License Challenge, sans ambiguïté.

### 6.3 L'arbitre de fin de combat — `0x1800DB4B0` (`0x1800DB4B0`–`0x1800DB88D`)

C'est le délégué de `0x1800DB100` (cas 0). Il lit le mode **quatre fois** :

| site | test | conséquence |
|---|---|---|
| `0x1800DB614` | `cmp eax, 3` | Special Sparring : `0x1801A5F40(2)` puis `edi = 0x14` GAMEOVER |
| `0x1800DB6DC`/`0x1800DB6E9` | `cmp eax, 1` | Score Attack : **saute** `0x1800B27A0(session, joueur)` — le combattant n'est pas réinitialisé, la série continue |
| `0x1800DB734` | `cmp eax, 2` | License Challenge : `edi = 0x14` GAMEOVER |
| `0x1800DB747` | `test eax, eax` | Arcade : `edi = 0x14` GAMEOVER |
| `0x1800DB786` | `cmp eax, 2` | License : `0x1801D8700()` / `0x1801D4B30()` décident continuer ou GAMEOVER |

### 6.4 La fin de partie — `0x18008B620`–`0x18008B978` (`TaskEnding`)

    0x18008B67B  call 0x18019C090
    0x18008B680  test eax, eax        ; mode 0 ARCADE
    0x18008B682  je   0x18008B699     ; -> joue "rom/movie/vf5end.sfd"
    0x18008B684  cmp  eax, 1          ; mode 1 SCORE ATTACK
    0x18008B68D  [tache+0x7C] = 3     ; -> saute le film
    ...
    0x18008B779  call 0x18019C090 ; cmp eax, 1 ; -> phase 3, puis 0x1800A8020

Arcade a une fin filmée ; Score Attack n'en a pas et part sur son écran à lui.

### 6.5 L'échelle de sauts de `0x18019C0C0`

    0x18019C1F8  ecx = [0x180751010]
    0x18019C1FE  ecx -= 2 ; je -> cas mode 2   ; passe par 0x1801D4290() (index de licence)
    0x18019C203  ecx -= 3 ; je -> cas mode 5
    0x18019C206  ecx -= 1 ; je -> cas mode 6
    0x18019C20B  ecx -= 1 ; je -> cas mode 7
    0x18019C215  cmp ecx, 1 ; -> cas mode 8, sinon défaut

Une fonction de sélection écrite comme un `switch (mode)` : la variable est bien
une énumération de mode, pas un compteur.

---

## 7. Les 98 lecteurs, condensés

`0x18019C090` a **98 appelants** (balayage linéaire `E8` + rel32). Répartition
des comparaisons qui suivent immédiatement l'appel :

| valeur testée | nb de sites | où, en gros |
|---:|---:|---|
| `== 0` | 4 | fin de partie, arbitre |
| `== 1` | 11 | `0x18008B6xx` (fin), `0x1800B1DB6`, `0x1800B6B56`, `0x1800B7C82`, `0x1800B8175`, `0x1800BB9D6`, `0x1800DB6E9`, `0x1800DB97B` |
| `== 2` | 26 | tout le circuit `lc::` (`0x1801D4xxx`, `0x1801D6xxx`, `0x1801D8730`, `0x1801D99xx`, `0x1801DA1F0`), GAMEOVER |
| `== 3` | 12 | `0x1800C381F`, `0x1800C7D72`, `0x1800DAA35`, `0x1800DAB4E`, `0x1800DB614`, `0x180173FA4`, `0x180198618/661/A08`, `0x1801E7F08` |
| `== 4` | 12 | `0x18016C777`, `0x1801A86F4`, `0x1801CFC8A`, `0x1801D0346`, `0x1801E85F3`, `0x1801E8F7C`, `0x1801E92FD` |
| `== 5` | 15 | `0x1800BCDD8` … `0x1800BEE2D`, tous sur `[obj+0x6C8]` — **branche morte** |
| `6..7` | 2 | `0x1801E514E` (`add eax,-6 ; cmp eax,1 ; jbe`), `0x1801E51AD` |
| `== 8` | 3 | `0x18016EB59`, `0x18016FBE5`, `0x1801AAB0E` |
| `== 9` | 2 | `0x1800938A7`, `0x180095D8A` — **branche morte** |
| `<= 3` | 1 | **`0x1800B8B9F`** — les quatre modes SINGLE PLAYER |
| autres | reste | tests composés (`cmp eax, esi`, `test eax,eax`) |

Les modes 3 et 4 partagent plusieurs chemins (`0x1800BB075`/`0x1800BB07F`,
`0x1800BBAB3`/`0x1800BBAC1`), de même que 4 et 5 (`0x1800B8F3B`/`0x1800B8F45`).

---

## 8. Pourquoi nos quatre entrées lancent toutes en Arcade

Le mode n'est **jamais** posé sur notre chemin, et `0` = Arcade.

La chaîne native pose le mode dans la **mise à jour** de la page de réglages
(créneau `[2]`), pas dans son validateur (créneau `[10]`). Dans
`TaskMenuArcadeNormal::update`, l'écriture est protégée par quatre gardes :

    0x1801DC2C9  call 0x1801BD9D0(page)        ; si vrai -> on saute tout
    0x1801DC2DD  call 0x1801BD9C0(page+0x258)  ; l'animation de sortie est-elle finie ?
    0x1801DC2ED  call 0x1801BD9C0(page+0x2B0)  ; idem
    0x1801DC301  call 0x180244F90(page+0x310)  ; la sous-scene est-elle partie ?
    0x1801DC30E  cmp  byte [page+0x60], 0      ; << « on lance » (et non « on annule »)
    0x1801DC3A6  call 0x18019C420(0, reglages, niveau, 0)

Le drapeau `[page+0x60]` est posé **par `0x1801BC010`**, le « son de
validation » :

    0x1801BC04C  mov byte ptr [rbx+0x60], 1
    0x1801BC050  mov dword ptr [rbx+0x234], 0

Notre greffe `--sp-lancer` remplace précisément ce `call 0x1801BC010`
(`0x1801DDE89`, `0x1800A48A9`, `0x1801DDE49`) — mais la caverne le **refait**
(`sp_lancer_cave()` appelle `SP_SON_VALIDER` avant `TRANSITION_CAVE`). Le
drapeau est donc bien posé. Ce qui manque, c'est le **temps** : la caverne
enchaîne immédiatement sur `0x1800DA9A0(2)` / `0x1800DA9C0(0x11)`, alors que la
mise à jour de la page n'écrira le mode que **plusieurs trames plus tard**,
une fois l'animation de sortie terminée — c'est-à-dire jamais, puisque le jeu
sera déjà passé au mode GAME.

### Ce qu'il faut poser

Le plus court : ajouter, dans la caverne, un appel à **`0x18019C490(mode)`**
(trois octets de corps, feuille, aucune pile) avant l'appel à `TRANSITION_CAVE`,
avec `ecx` = 0 / 1 / 2 / 3 selon la greffe.

| greffe | validateur | classe | `ecx` |
|---|---|---|---:|
| `0x1801DDE89` | `0x1801DDE80` | `TaskMenuArcadeNormal` | 0 |
| `0x1800A48A9` | `0x1800A48A0` | `TaskMenuScoreAttack` | 1 |
| `0x1801DDE49` | `0x1801DDE40` | `TaskMenuArcadeLicenceChallenge` | 2 |
| `0x1801A4399` | `0x1801A4390` | `TaskMenuTeam` (Special Sparring) | 3 |

**Avertissement — le validateur de Score Attack est PARTAGÉ.** `0x1800A48A0`
occupe le créneau `[10]` de **trois** vtables :

| vtable | classe |
|---|---|
| `0x18039A1B0` | `TaskEndMenu` |
| `0x180532718` | **`TaskMenuScoreAttack`** |
| `0x180532778` | `CTaskAllClearInfoWindow` |

La greffe existante `0x1800A48A9` se déclenche donc aussi pour `TaskEndMenu` et
`CTaskAllClearInfoWindow`. Les trois autres validateurs (`0x1801DDE80`,
`0x1801DDE40`, `0x1801A4390`) n'apparaissent, eux, que dans une seule vtable.
Si le mode 1 se met à être posé au mauvais moment, c'est la première piste.

La quatrième ligne est nouvelle : `TaskMenuTeam::validate` `0x1801A4390`
commence, elle aussi, par `call 0x1801BC010` à `0x1801A4399` — la greffe a donc
exactement la même forme que les trois autres, ce qui donne un point d'ancrage
à Special Sparring (voir §9).

Réserve : `0x18019C490` ne pose **que** le mode. Les six octets de réglages
(`0x180751014`–`0x180751019`) et l'octet annexe du mode restent ceux qu'a
laissés la dernière écriture. Pour un rendu fidèle il faudrait appeler le setter
de la famille, comme la page le fait elle-même :
`0x18019C420(0|2|3, reglages, niveau, 0)` ou `0x18019C4A0(1, reglages, annexe, …)`.
Ce n'est pas nécessaire pour que le mode change ; ça l'est pour que les rounds,
le temps et la santé suivent.

Bonne nouvelle pour License Challenge : ses données (`0x1807533C0`) sont déjà
chargées par `0x1801DDDB1`, à l'ouverture de la page, avant toute greffe.

---

## 9. Special Sparring : la chaîne native existe

L'entrée 3 de la page des modes, dans `0x1801DDD00` :

    0x1801DDDD2  cmp  eax, 3
    0x1801DDDD7  call 0x180029FB0        ; le bouchon « vrai »
    0x1801DDDE0  call 0x1801A5E90        ; -> pousse la scene "CARD SELECTOR"
    0x1801DDDE5  [page+0x2F8] = rax

`0x1801A5E90` rend le singleton `0x1807513A8` (`TaskMenuSetting`, vtable
`0x180410BF0`) et le pousse sous le nom de scène `"CARD SELECTOR"`
(`0x180410D50`).

Ensuite, `TaskMenuArcade::update` (`0x1801DBE20`–`0x1801DC047`) enchaîne :

    0x1801DBF2F  call 0x1801A5B70([page+0x2F8])
    0x1801DBF38  call 0x1801A5620() ; cmp eax, 2
    0x1801DBF49  call 0x1801A5600() -> 6 octets de reglages, recopies en [page+0x1340]
    0x1801DBF6B  call 0x1801A5EC0(reglages, edx)
                 -> pousse le singleton 0x1807513B0 = TaskMenuTeam

et `TaskMenuTeam::update` (`0x1801A4160`) pose enfin le mode 3 :

    0x1801A4236  cmp  byte [page+0x60], 0     ; meme garde que les autres
    0x1801A423C  r8b = [page+0x4D8]
    0x1801A4244  rdx = &[page+0x4D0]
    0x1801A424E  ecx = 3
    0x1801A4252  call 0x18019C420
    0x1801A4257  mov  dword [0x1807513A4], 0

Le singleton `0x1807513B0` est bien `TaskMenuTeam` : son constructeur y écrit la
vtable `0x180410C50` (`0x1801A3DE2`/`0x1801A3DE9`) puis se publie
(`0x1801A3F01 : mov [0x1807513B0], rsi`) ; il embarque un sous-objet
`TaskClearInfo` à `+0x320`.

Donc Special Sparring « ne lance rien » non pas parce que la chaîne manque,
mais parce qu'aucune greffe n'a été posée sur `TaskMenuTeam::validate`
(`0x1801A4390`), et que rien ne demande le mode GAME au bout.

---

## 10. Corrections aux documents existants

| document | ce qui y est écrit | ce qui est établi ici |
|---|---|---|
| `vs_gameover.md` §2 | « `0x1801DD6A0` pose 1 » sans nom ; « 1 = versus » | `0x1801DD6A0` = `TaskMenuScoreAttack::update` ; **1 = Score Attack**, **4 = versus** |
| `vs_gameover.md` §2 | « 2 et 3 = score attack / license challenge » ; « deux fonctions seulement » écrivent | **2 = License Challenge, 3 = Special Sparring** ; **cinq** setters, **dix-neuf** sites |
| `vs_gameover.md` §2 | « `0x1801DC050` = DIFFICULTY CHANGE WINDOW » | `0x1801DC050` = `TaskMenuArcadeLicenceChallenge::update`. `CTaskDifficultyChangeWindow` est la vtable `0x180532788`, mise à jour `0x1801DB9F0` |
| `menu_console.md` §19.1 | « `0x1805328A8` = réglages arcade » | `0x1805328A8` = `TaskMenuVersus` ; les réglages arcade sont `TaskMenuArcadeNormal`, vtable `0x180532668` |
| `menu_console.md` §19.4 | « Le champ qui porte le mode de jeu n'est pas identifié » | c'est `0x180751010` |

---

## 11. Ce qui n'est PAS établi

* **Les valeurs 5 et 9.** Elles sont lues (17 sites) mais écrites nulle part
  dans ce build. Hypothèse non vérifiée : modes réseau, retirés de la version
  APM3. Le balayage qui l'affirme est linéaire et couvre tout `.text` ; il ne
  couvre pas une écriture qui serait faite depuis `apm.dll` ou `vfes.exe` — je
  n'ai balayé que le moteur.
* **La valeur 8.** Écrite par la troisième entrée du DOJO et par `TaskMenuMain`,
  mais je n'ai pas identifié à quel libellé elle correspond (`TaskMenuTraining`
  a trois entrées ; seules deux ont une classe à elles).
* **`0x18023DFBB`** pose `ecx = rdi + 3`. `rdi` sert de borne de saturation
  quelques instructions plus haut (`cmp cl, dil ; cmova ecx, edi`) ; s'il vaut 1,
  le mode posé est 4. Non prouvé.
* **`[session+8]`.** Dans `0x1800B1D80` il vaut 0 pour le solo et 1 pour la
  branche « équipe » (`0x1801A5F50`). Cela cadre avec « nombre de joueurs », mais
  je ne l'ai pas démontré et la branche 1 est celle qu'emprunte Special Sparring
  d'après §9 — à vérifier avant de s'appuyer dessus.
* **Le rôle exact de `0x18075101E`** (posé à 1 par `0x18019C3C0`, dont l'unique
  appelant est `0x18016E039`) et de `0x18019BD30`.
* **Le mécanisme de §8** (« la mise à jour n'a pas le temps de tourner ») est
  déduit des gardes lues dans `TaskMenuArcadeNormal::update`, **pas mesuré**.
  Une trace à l'exécution le confirmerait ou l'infirmerait ; je n'ai rien lancé.
* **La correspondance libellé ↔ classe pour l'entrée 3** (`Special Sparring`
  → `TaskMenuSetting` sous le nom de scène `"CARD SELECTOR"`) repose sur
  l'aiguillage de `0x1801DDD00`, pas sur une capture d'écran.

---

## 12. Méthode et bornes

* Binaire : `vf5fs-pxd-w64-Retail_APM3.dll.origine`, base `0x180000000`.
  Une seule section exécutable, `.text` `0x180001000` (vsize `0x34475C`,
  `SizeOfRawData` `0x344800`) : tous les balayages la couvrent en entier.
* **Références à une donnée** : balayage linéaire octet par octet de `.text`,
  test `fin + disp32 == cible` pour tout `disp32` possible. Indépendant de
  `.pdata` et des bornes de fonction. `0x180751010` : 8 résultats, tous
  désassemblés et classés (§3).
* **Appelants d'une fonction** : balayage linéaire de `.text` pour `E8`/`E9` +
  rel32 pointant sur la cible. `0x18019C090` : 98 sites ; les cinq setters : 19.
* **Noms de classes** : reconstruction du RTTI MSVC x64 (TypeDescriptor →
  CompleteObjectLocator → `vftable[-8]`), 532 vtables nommées.
* **Bornes de fonction** : `.pdata`, en gardant à l'esprit qu'une fonction
  couvre souvent plusieurs entrées chaînées — les bornes citées au §3 sont celles
  de l'entrée qui contient le site, pas nécessairement celles de la fonction.
* Les déplacements `+0x58`, `+0x60`, `+0x240` cités sont ceux de la classe de
  base des pages de menu ; le balayage de `mov byte [reg+0x60], imm` du §8 a été
  borné à `0x1801A0000`–`0x1801F0000` (32 résultats).
