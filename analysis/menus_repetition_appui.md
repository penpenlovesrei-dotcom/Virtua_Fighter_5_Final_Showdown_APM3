# La répétition d'appui dans les menus — trajet, cause, correctif (2026-11-19)

Demande de Frédéric : « dans les menus, la navigation est un peu hasardeuse,
j'ai l'impression qu'un appui, s'il est un peu trop long, enregistre plusieurs
appuis et donc plusieurs validations. Vérifie et corrige si nécessaire. »

**Aucune course n'a été lancée pour écrire ce document.** Tout ce qui est dit
« mesuré » ci-dessous l'est par lecture de binaire, lecture de code, lecture de
fichier ou relevé de journal déjà sur le disque. Ce qui n'est pas mesuré est
nommé comme tel au §6.

---

## 0. La réponse en quatre lignes

La fenêtre de front de notre `apm.dll` vaut **34 ms** au lieu des **10 ms**
établies par la mesure du 2026-09-05. À 60 images/s une trame dure 16,7 ms :
**trois scrutations du moteur tombent dans 34 ms**, et comme *rien*, dans le
moteur, ne dédoublonne une validation, l'appui est validé deux ou trois fois.

La faute n'est pas dans le code de la greffe : elle est dans le **fichier de
disposition que `jouer.cmd` installe**, `VF5RE/tools/scenarios/jouer.txt`, qui
**n'a pas de ligne `front`** — il date du 2026-09-03, soit **deux jours avant**
le correctif, et n'a jamais été repris. Le correctif de 2026-09-05 n'a été posé
que dans l'autre fichier, `VF5RE/tools/apm_entrees.txt`, que `jouer.cmd` ne
copie pas.

---

## 1. Le trajet complet d'un appui, fonction par fonction

Les adresses du moteur sont lues dans
`SOURCES/APM3_US/runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll` (image
intacte, base `0x180000000`) et dans `vfes.exe` (base `0x140000000`) du même
dump, par `VF5RE/tools/pe_disasm.py`. **Mesuré.**

| # | Où | Quoi |
|---|---|---|
| 1 | `apm.dll` (notre greffe) — `lire_clavier()`, `gen_apm_stub.py:836` | `GetAsyncKeyState(touche) & 0x8000` par code, donc **l'état TENU**, sans consommation de front. Garde `if (g_touche[i] && …)` en ligne 856 |
| 2 | `apm.dll` — `lire_manette()`, `:865` | XInput ; accord `if (m1 && (b & m1) == m1)` en ligne **920**. Le `m1 &&` interdit qu'un masque vide soit affirmé (voir §5, fiche CODE 6) |
| 3 | `apm.dll` — `maj()`, `:1178` | `g_masque = scenario \| impulsion \| clavier \| manette` ; puis `g_montants = ~avant & g_masque`, `g_descendants = ~g_masque & avant` ; puis, **sur le seul front montant**, `g_presse[i] = t` (ligne 1249-1250). Copie fidèle de `0x180013EF0` de la vraie `apm.dll` |
| 4 | `apm.dll` — `entree()`, `:3160` | `Input_isOn` → `g_masque & (1<<code)`. `Input_isOnNow` → **le même bit TENU, PLUS** `r = (tt - g_presse[code] < g_front)` (ligne **3209**) : une **fenêtre de temps**, pas un bit de front |
| 5 | `apm.dll` exports `:3298`, `:3301` | `Input_isOn(int)` et `Input_isOnNow(int)` |
| 6 | `vfes.exe` troncs | `0x140002BE0 : mov ecx,edx ; jmp [0x140133580]` → `Input_isOn`<br>`0x140002BF0 : mov ecx,edx ; jmp [0x140133578]` → `Input_isOnNow`<br>Le `this` est jeté, le code passe en premier argument. **Désassemblé, mesuré** |
| 7 | table d'interface | base `0x1401AF710` ; créneau **`+0x158` = `Input_isOn`**, **`+0x160` = `Input_isOnNow`**. L'objet vu du moteur est `[0x180C3B6F8]` |
| 8a | moteur — `0x1801A2BC0` **VALIDER** | `mov rcx,[0x180C3B6F8] ; mov edx,7 ; mov rax,[rcx] ; call [rax+0x160]` — c'est-à-dire **`Input_isOnNow(7)` en direct**. Puis `neg al ; sbb ; neg ; dec` → rend **0** si front, **-1** sinon. **Désassemblé, mesuré** |
| 8b | moteur — `0x1801A2B90` **ANNULER** | identique avec `edx = 8` : `Input_isOnNow(8)`. **Mesuré** |
| 8c | moteur — `0x1801A2CA0` **TENU** | ne touche pas la greffe : il lit les tableaux du moteur en `0x180751040` / `0x180751174` / `0x180751280` |
| 9 | moteur — le curseur partagé `0x1801BBBE0` (corps `0x1801BBC05`) | `0x1801BBCC6 call 0x1801A2B90` → si front, `call [r8+0x48]` = annuler<br>`0x1801BBCDD call 0x1801A2BC0` → `test eax,eax ; js` → sinon `0x1801BBCEE call [r8+0x50]` = **LE VALIDATEUR**. **Désassemblé, mesuré** |
| 10 | moteur — le validateur des OPTIONS `0x1801A8090` | `mov eax,[liste+0x58] ; mov [liste+0x2F8],eax ; mov byte [liste+0x2F0],1` |

### Où le front est censé être détecté, et par qui

**Par `apm.dll`, et par elle seule, pour les validations.** C'est le point
décisif, et il est désassemblé : entre l'étape 8a et l'étape 9 il n'y a
**aucun** état, aucun compteur, aucun « appui précédent ». `0x1801BBCDD`
appelle le prédicat et, s'il rend 0, appelle le validateur — dans la même
instruction. **Si `Input_isOnNow(7)` rend vrai sur N trames consécutives, le
validateur est appelé N fois.** Le moteur ne dédoublonne rien.

La vraie `apm.dll` tient ce contrat : `0x180013EF0`, appelée une seule fois par
trame depuis `Core_execute+0xFB`, publie un masque de **fronts montants** en
`0x18012B2F8` qui ne vit **qu'une trame**. `Input_isOnNow` y teste un bit.

### Le chemin des DIRECTIONS est différent, et il est sain

Les directions ne passent pas par `Input_isOnNow` : `0x180243ED0`, le lecteur
d'entrées du moteur, interroge les treize codes par **`Input_isOn`** (`+0x158`)
et compose un masque arcade en `0x180751050 + joueur*0x54`, où il tient
**lui-même** un historique :

```
+0x08 tenu    +0x0C tenu a la trame precedente    +0x10 front montant
+0x14 relache +0x18 repetition  (masque [rsi+0xA8], retard [rsi+0xAC], periode [rsi+0xAD])
```

Mesure du 2026-09-04 (`analysis/menu_console.md` §7, CONFIRMED) :
`masque repetition = 0x000FF0C9`, `retard 24`, `periode 3`, et
`haut -> tenu 0x1000  front 0x1000`. **L'état de manette du moteur est correct,
fronts compris.** L'auto-répétition des directions au-delà de 24 trames
(400 ms) est le comportement voulu de SEGA, pas un défaut de la greffe.

---

## 2. Les trois hypothèses, départagées par lecture

| | Hypothèse | Verdict | Sur quoi |
|---|---|---|---|
| **(a)** | la greffe rend un bouton MAINTENU comme une succession de fronts montants | **FAUSSE** | `lire_clavier()` teste `& 0x8000`, l'état tenu, et ne consomme aucun front (le bit `0x0001` de `GetAsyncKeyState` n'est pas lu). `maj()` calcule `g_montants = ~avant & g_masque` : un bouton tenu produit **exactement un** front montant, et `g_presse[i]` n'est réécrit que là. Lecture de code, `gen_apm_stub.py:856`, `:920`, `:1245-1250` |
| **(b)** | le moteur fait sa détection de front sur un compteur ou un « appui précédent » que la greffe ne tient pas à jour | **FAUSSE pour les validations, VRAIE mais saine pour les directions** | Pour valider, `0x1801A2BC0` appelle `[rax+0x160]` = `Input_isOnNow` **directement** : le moteur ne tient aucun historique de ce côté, il délègue le front à la greffe. Pour les directions, il tient bien un historique (`+0x0C`, `+0x10`, `+0x18`) à partir de `Input_isOn`, et il est correct (mesure du 2026-09-04) |
| **(c)** | la relecture d'`apm_entrees.txt` toutes les 30 ms ré-affirme l'appui et casse le front | **FAUSSE, et la cadence annoncée est fausse aussi** | `maj()` ne relit le fichier que si `now - g_dernier_test > (g_npas > 0 ? 30 : 500)` (`:1193-1198`). `jouer.txt` **n'a aucun pas de scénario** (`g_npas = 0`) : la relecture est donc à **500 ms**, pas 30. Et `charger()` ne reparse que si la date du fichier a changé. Surtout, la relecture ne touche pas l'appui : le clavier est relu en direct à **chaque** `maj()`, et le scénario est vide. (La bannière de `VF5RE/jouer.cmd` annonce « toutes les 30 ms » : c'est inexact, voir §4 correctif C) |

---

## 3. LA CAUSE, DÉSIGNÉE ET MESURÉE

### 3.1 Le code : la fenêtre vaut 34 ms, et elle est remise à 34 à chaque relecture

```c
/* gen_apm_stub.py:324 */
static unsigned  g_front = 34;         /* ms pendant lesquelles isOnNow reste vrai */

/* gen_apm_stub.py:992, dans charger() -- la remise a zero AVANT de lire le fichier */
    g_front = 34;

/* gen_apm_stub.py:1044-1047 -- le seul ecrivain */
            } else if (!_strnicmp(p, "front", 5)) {
                char *r = p + 5;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                g_front = (unsigned)atoi(r);
            }

/* gen_apm_stub.py:3209 -- l'usage */
            r = (tt - g_presse[code] < g_front) ? 1 : 0;
```

**Conséquence mesurée par lecture** : sans ligne `front` dans le fichier,
`g_front` vaut 34 ms, et il y est remis à **chaque** relecture. Aucune dérive
possible, aucun hasard : c'est 34, toujours.

### 3.2 Le fichier : celui que `jouer.cmd` installe n'a pas la ligne

`VF5RE/jouer.cmd` installe la disposition par cette ligne :

```
copy /y "tools\scenarios\jouer.txt" "runtime\media\vf5fs\apm_entrees.txt" >nul
```

Relevé exhaustif des sept fichiers de scénario du disque :

| fichier | ligne `front` |
|---|---|
| `VF5RE/tools/apm_entrees.txt` | `front   = 10` |
| `FS APM3/outils/apm_entrees.txt` | `front   = 10` |
| `FS APM3/banc_revo/apm_entrees.txt` | `front   = 10` |
| `FS APM3/banc_gog/apm_entrees.txt` | `front   = 10` |
| **`VF5RE/tools/scenarios/jouer.txt`** | **ABSENTE → 34 ms** |
| **`VF5RE/runtime/media/vf5fs/apm_entrees.txt`** | **ABSENTE → 34 ms** |
| `FS APM3/outils/scenarios/jouer.txt` | ABSENTE → 34 ms |

Les deux derniers du jeu vivant sont **identiques**, SHA-256
`5206a6189a7e8362230a209262ff75f2376c565492a64e46ec46cd48be1be760`, 2 524 o,
ASCII pur, fins de ligne LF, 67 lignes.

### 3.3 La chronologie, qui nomme la régression

| date | fichier | fait |
|---|---|---|
| 2026-09-03 08:17 | `VF5RE/jouer.cmd` | créé |
| **2026-09-03 08:31** | **`VF5RE/tools/scenarios/jouer.txt`** | **créé, sans ligne `front`** |
| 2026-09-05 | `analysis/carte_options.md` §10 | la mesure établit `front = 10` |
| 2026-10-10 23:34 | `VF5RE/tools/apm_entrees.txt` | porte `front = 10` |
| — | `jouer.txt` | **jamais repris depuis le 2026-09-03** |

Le correctif du 2026-09-05 a été posé dans le **modèle** `apm_entrees.txt`
— avec le commentaire de mesure, encore lisible lignes 35-42 — mais **pas** dans
`jouer.txt`, qui est le fichier que l'on joue. `jouer.txt` **précède** le
correctif de deux jours.

### 3.4 Le relevé des journaux : la sonde a déjà parlé

Règle n°1 de la liste de contrôle. Tous les `*.txt` et `*.log` du disque ont été
grepés en bloc ; **46** portent la ligne `[apm] entrees: … front=… ms`, et
46 = 34 + 6 + 6, donc le relevé ci-dessous est **exhaustif**, sans reste :

```
34 x  front=10 ms      (2026-10-04 -> 2026-10-13)
 6 x  front=34 ms      (2026-09-01 21:54, 2026-09-03 08:43, 08:47)
 6 x  front=150 ms     (2026-09-03 08:58, 08:59, 09:01)
```

Lecture : **aucune course n'a jamais été journalisée avec le fichier
`jouer.txt`.** Les 34 relevés à 10 ms viennent tous des outils
`pister_*` / `sp_*` / `sonde_mode`, qui installent `apm_entrees.txt`. Les
relevés à 34 et 150 ms sont **antérieurs** au correctif du 2026-09-05.

C'est donc bien un **trou de mesure** : le chemin que Frédéric emprunte pour
jouer, `jouer.cmd`, n'a jamais été instrumenté, et c'est le seul qui porte la
valeur fautive.

### 3.5 Le compte de trames, et pourquoi le symptôme est « hasardeux »

La vraie `apm.dll` échantillonne une fois par trame. Notre greffe aussi :
`maj()` est appelée depuis `Core_execute`, et le rapport est **mesuré** dans
`FS APM3/donnees/cadence.txt` (30 s de jeu, journal du stub actif) :

```
Core_execute      1142
Input_isOn       14807     ->  12,97 par Core_execute, soit les 13 codes
Input_isOnNow     4556     ->   3,99 par Core_execute, soit les 4 codes 0/7/8/15
```

Une trame du moteur = un battement = un `maj()`. Le garde-fou des 50 ms de
`entree()` (`:3189`) ne se déclenche donc jamais en marche normale.

À 60 images/s, les scrutations tombent à t ≈ 0 / 16,7 / 33,3 / 50,0 ms après le
front :

| `front` | scrutations dans la fenêtre | validations |
|---:|---|---|
| **34 ms** (en vigueur) | 0 ; 16,7 ; **33,3** — trois | **2 ou 3** |
| 20 ms (essayé le 09-05) | 0 ; 16,7 — deux | 2 |
| **10 ms** (mesuré bon) | 0 — une | **1** |

33,3 ms est à **0,7 ms** de la borne des 34 : selon la gigue d'affichage, la
troisième scrutation tombe dedans ou non. **C'est exactement « hasardeux » :
2 validations parfois, 3 d'autres fois, et jamais la même chose.**

Et la dépendance à la durée que Frédéric décrit se lit dans le code : la
fenêtre est gardée par l'état **TENU** (`entree()` teste
`g_masque & (1<<code)` *avant* la fenêtre). Un appui relâché dans la première
trame ne rend vrai qu'une fois ; **tenu au-delà de ~17 ms, il rend vrai deux ou
trois fois.** « Un appui, s'il est un peu trop long » — le code dit la même
chose que l'écran.

### 3.6 La mesure à l'écran existe déjà, et elle est unanime

`analysis/carte_options.md` §10, « La double validation : la fenêtre d'entrée,
mesurée (2026-09-05) », sur le même symptôme rapporté par Frédéric — « un appui
sur Entrée validait deux fois » — avec `tools/pister_validation.cmd` :

```
Curseur      881
Predicat     872        -> 0,99 par tour : le curseur tourne UNE fois par trame
dont presse  2

   9008.5 ms  PREDICAT : presse
   9025.3 ms  PREDICAT : presse      <- 16,8 ms plus tard = UNE TRAME
   9025.9 ms  VALIDER
```

Conclusion de l'époque, que le présent document ne fait que re-désigner :
« Le curseur partagé ne tourne qu'une fois par trame : ce n'est pas un double
site d'appel. C'est **la fenêtre de `Input_isOnNow`** du stub », et « la fenêtre
doit être plus courte qu'une trame, 16,7 ms à 60 images/s ».

---

## 4. LE CORRECTIF, prêt à poser — NON APPLIQUÉ

Je n'ai rien écrit dans `quest_runtime.c`, `gen_apm_stub.py`,
`apm_tremplins.asm` ni leurs copies de `FS APM3/outils/`, et je n'ai rien
recompilé.

**Bonne nouvelle : le correctif A suffit et n'exige NI recompilation NI
relance.** Il ne touche qu'un fichier de données.

### Correctif A — OBLIGATOIRE : la ligne `front` dans `jouer.txt`

**Fichier** : `C:\Users\frede\Documents\RECOMP\Virtua Fighter 5 FS\VF5RE\tools\scenarios\jouer.txt`
**Encodage** : ASCII pur, fins de ligne **LF** (pas CRLF) — ne pas introduire
d'accent ni de CRLF.
**Lieu** : ligne 13, juste avant `journal = 0`.

```diff
--- a/VF5RE/tools/scenarios/jouer.txt
+++ b/VF5RE/tools/scenarios/jouer.txt
@@ -10,6 +10,16 @@
 # Le clavier n'agit que si la fenetre du jeu est au premier plan.
 # ---------------------------------------------------------------------------
 
+# --- la fenetre de front -----------------------------------------------------
+# front = <ms> : duree pendant laquelle Input_isOnNow reste vrai apres un appui.
+# ELLE DOIT ETRE PLUS COURTE QU'UNE TRAME (16,7 ms a 60 images/s), sinon
+# plusieurs scrutations du moteur tombent dedans et UN appui vaut PLUSIEURS
+# validations -- le moteur ne dedoublonne rien (0x1801BBCDD appelle le
+# validateur a chaque fois que 0x1801A2BC0 rend un front).
+# MESURE du 2026-09-05 (tools/pister_validation.cmd) : 150 ms -> 9 validations,
+# 20 ms -> encore double, 10 ms -> une seule. Sans cette ligne le stub retombe
+# sur son defaut de 34 ms, soit 2 a 3 validations par appui.
+front   = 10
+
 journal = 0
 clavier = 1
 manette = 1
```

Après l'édition, relancer `VF5RE\jouer.cmd` : il recopie `jouer.txt` sur
`runtime\media\vf5fs\apm_entrees.txt`.

**Le diff ci-dessus a été vérifié par un contrôle qui discrimine** (règle du §4
de `CLAUDE.md` : il doit pouvoir échouer sur la faute réelle et réussir sur la
pose juste). Le contrôle réimplémente le parseur du stub
(`gen_apm_stub.py:992-1047` : défaut 34, écrasé par une ligne `front`) et le
passe sur les deux versions du fichier :

```
TEMOIN NEGATIF -- doit rendre 34 (la faute reelle)
  jouer.txt actuel             g_front = 34   attendu 34   OK
TEMOIN POSITIF -- doit rendre 10 (la pose juste)
  jouer.txt corrige            g_front = 10   attendu 10   OK
INTEGRITE DE LA POSE
  aucune ligne perdue        OK
  reste ASCII pur            OK
  reste en LF (aucun CRLF)   OK
  lignes ajoutees            11 (attendu 11)
```

Le point d'insertion `journal = 0` a été vérifié **unique** dans le fichier.
Le contrôle et la **copie corrigée prête à recopier** sont dans le bac à sable
de session (effaçable par un redémarrage, donc à reporter dans le projet) :

```
C:\Users\frede\AppData\Local\Temp\claude\ccb47ad791f921bb\464f50e0-85fb-4425-bc18-5344bc3e327b\scratchpad\verifier_front.py
C:\Users\frede\AppData\Local\Temp\claude\ccb47ad791f921bb\464f50e0-85fb-4425-bc18-5344bc3e327b\scratchpad\jouer_corrige.txt
```

Réserve : ce contrôle prouve que **le fichier dira 10**. Il ne prouve pas que
**l'écran validera une fois** — voir §6.1.

**Variante à chaud, si le jeu tourne déjà** : écrire la même ligne
`front   = 10` directement dans
`C:\Users\frede\Documents\RECOMP\Virtua Fighter 5 FS\VF5RE\runtime\media\vf5fs\apm_entrees.txt`.
Le stub voit la date changer dans la demi-seconde et applique la valeur **sans
relancer le jeu** — c'est l'essai le moins coûteux pour trancher à l'écran.
Mais il faut **aussi** poser le correctif A, sinon le prochain `jouer.cmd`
écrase le fichier et réintroduit les 34 ms.

### Correctif B — RECOMMANDÉ : que le défaut de la greffe ne soit plus fautif

Tant que le défaut vaut 34, **tout fichier sans ligne `front` rejouera le même
bug.** Il y en a déjà trois sur le disque. Deux occurrences, un seul littéral
chacune.

**Fichier** : `C:\Users\frede\Documents\RECOMP\Virtua Fighter 5 FS\VF5RE\tools\gen_apm_stub.py`
(**lecture seule pour moi — c'est toi qui poses**)

```diff
--- a/VF5RE/tools/gen_apm_stub.py
+++ b/VF5RE/tools/gen_apm_stub.py
@@ -324 +324 @@
-static unsigned  g_front = 34;         /* ms pendant lesquelles isOnNow reste vrai */
+static unsigned  g_front = 10;         /* ms pendant lesquelles isOnNow reste vrai :
+                                        * PLUS COURT QU'UNE TRAME (16,7 ms a 60 i/s),
+                                        * sinon un appui vaut plusieurs validations.
+                                        * Mesure du 2026-09-05, carte_options.md §10. */
@@ -992 +992 @@
-    g_front = 34;
+    g_front = 10;    /* defaut : plus court qu'une trame (carte_options.md §10) */
```

Et, dans le commentaire d'`entree()` qui décrit encore l'ancienne valeur —
**lignes 3205 à 3207**, les deux lignes à remplacer étant 3206 et 3207 :

```diff
@@ -3205,3207 +3205,3213 @@
              * On garde donc la fenetre de temps, qui marche. Elle dure
-             * g_front = 34 ms, soit deux trames au lieu d'une : c'est un ecart
-             * connu et mesure avec l'original, pas un oubli. */
+             * g_front = 10 ms par defaut : PLUS COURT qu'une trame, donc une
+             * seule scrutation du moteur tombe dedans -- l'original, lui, tient
+             * un vrai bit de front d'une trame. A 34 ms (l'ancien defaut) deux a
+             * trois scrutations tombaient dedans et UN appui valait DEUX OU TROIS
+             * validations : le moteur ne dedoublonne rien, 0x1801A2BC0 rend
+             * Input_isOnNow(7) tel quel et 0x1801BBCDD appelle le validateur a
+             * chaque front. Mesure : carte_options.md §10 (2026-09-05) et
+             * analysis/menus_repetition_appui.md (2026-11-19). */
```

Le correctif B **exige de reconstruire `apm.dll`** ; le correctif A non. Poser A
d'abord, trancher à l'écran, poser B ensuite pour que la faute ne revienne pas.

### Correctif C — cosmétique : la bannière de `jouer.cmd` annonce une cadence fausse

**Fichier** : `C:\Users\frede\Documents\RECOMP\Virtua Fighter 5 FS\VF5RE\jouer.cmd`
(ASCII sans accent, règle du §5 de `CLAUDE.md`)

**Ligne 20** (la ligne 19 est `echo    La disposition se change dans
tools\scenarios\jouer.txt : le stub`) :

```diff
--- a/VF5RE/jouer.cmd
+++ b/VF5RE/jouer.cmd
@@ -20 +20 @@
-echo    relit le fichier toutes les 30 ms, sans relancer le jeu.
+echo    relit le fichier toutes les 500 ms, sans relancer le jeu.
```

Mesure : `gen_apm_stub.py:1193-1198`, `now - g_dernier_test > (g_npas > 0 ? 30 : 500)`.
`jouer.txt` n'a aucun pas de scénario, donc `g_npas = 0`, donc **500 ms**. Les
30 ms ne valent que lorsqu'un scénario joue. Sans conséquence sur le bug, mais
c'est cette ligne qui a fait naître l'hypothèse (c).

### Ce que le correctif NE touche pas, et pourquoi

- **`quest_runtime.c`** : aucun rôle dans le trajet de l'entrée. Les trois
  occurrences de « front » qu'il porte (lignes 2449, 2456, 4124) sont le Quest
  et un commentaire. Non modifié, non à modifier.
- **`apm_tremplins.asm`**, **les copies de `FS APM3/outils/`** : non touchés.
- **Le moteur (`vf5fs-pxd-w64-Retail_APM3.dll`)** : **aucun octet à changer.**
  Le moteur est conforme ; c'est la greffe qui doit tenir le contrat du front.
- **L'auto-répétition des directions** (`retard 24`, `periode 3`,
  `masque 0x000FF0C9`) : c'est le comportement voulu de SEGA, mesuré correct le
  2026-09-04. Ne pas y toucher sans une demande explicite de Frédéric.

---

## 5. La quatrième piste : la fiche CODE 6 a été RÉSOLUE, pas retirée

La consigne demandait de distinguer trois états. **Mesuré : résolue dans le
code.**

- La fiche est dans `FS APM3/documentation/_journal/A FAIRE.txt` **ligne 325**,
  datée 2026-11-04.
- Elle est **absente** de `VF5RE/A FAIRE.txt` (14 novembre) : `grep -a "CODE 6"`
  rend zéro.
- `grep -a "CODE 6"` rend aussi **zéro** dans `VF5RE/code_decompile/MENU.md` et
  dans `VF5RE/REPRISE.md`. **Aucune trace écrite de sa résolution** — c'est une
  absence de journal, pas une absence de correctif.
- **Mais le code porte la garde** que la fiche demandait d'aller vérifier.
  `gen_apm_stub.py:920` :

  ```c
  if (m1 && (b & m1) == m1) m |= (1u << i);
  else if (m2 && (b & m2) == m2) m |= (1u << i);
  ```

  Le `m1 &&` interdit qu'un masque **vide** soit affirmé : l'accord
  `(etat & 0) == 0` n'est jamais atteint. Même garde côté clavier, ligne 856
  (`if (g_touche[i] && …)`). Et les lignes 828-831 effacent explicitement
  `g_bouton[6]` et `g_bouton[15]` en mode arcade, avec le commentaire qui
  énonce le raisonnement de l'accord.

**Donc : le défaut « tout code non câblé est affirmé en permanence » n'existe
pas dans la version vivante de `gen_apm_stub.py`.** La fiche a été retirée de la
liste du 14 novembre parce qu'elle était réglée ; ce qui manque, c'est la ligne
de journal qui le dise. Le `On(6) = OUI` du 4 novembre s'explique sans défaut :
`jouer.txt` câble `touche 6 = espace` et `bouton 6 = back`, donc le code 6 **a**
un bouton, et l'affirmer est correct.

**Réserve honnête** : je n'ai pas comparé octet à octet la copie figée
`FS APM3/outils/gen_apm_stub.py` à la vivante ; je n'ai lu la garde que dans la
vivante, qui est celle qui fait foi.

### Au passage, un symptôme voisin déjà corrigé — vérifié, pas supposé

`carte_options.md` §6 décrit un raccourci de borne : `0x1801A7C91` interroge
« le bit 0 est-il **TENU** ? » (`0x1801A2CA0`), et si oui force l'entrée 5,
`OPTION INFO`. Comme le bit 0 **est** le code 7, c'est-à-dire Entrée, valider en
tenant la touche détournait vers la page d'informations — un second symptôme
dépendant de la durée, qui aurait pu se confondre avec celui-ci.

**Mesuré : le correctif est bien posé dans la DLL installée.** Désassemblage
comparé de `0x1801A7C7C` :

```
SOURCES/APM3_US/.../vf5fs-pxd-w64-Retail_APM3.dll   75 5f    jne 0x1801A7CDD
VF5RE/runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll   eb 5f    jmp 0x1801A7CDD
```

Le saut est inconditionnel (`--options-raccourci`, deux octets). Ce n'est donc
**pas** une cause du symptôme actuel. Écarté par mesure.

---

## 6. CE QUE JE N'AI PAS PU VÉRIFIER SANS LANCER LE JEU

Nommé, et pas enterré.

1. **Que `front = 10` supprime bien le symptôme sur le chemin `jouer.cmd`.**
   La valeur 10 a été mesurée à l'écran le **2026-09-05**, mais sur le chemin
   `apm_entrees.txt` et avec la greffe de l'époque. Aucun journal du disque ne
   montre une course avec `jouer.txt`. **C'est l'écran qui tranche, pas le
   journal** : il faut poser le correctif A et compter les validations à l'écran.
2. **Le nombre exact de validations aujourd'hui : 2 ou 3.** Le calcul donne
   trois scrutations dans 34 ms à 60,0 images/s exactement, la troisième à
   0,7 ms de la borne. Je n'ai mesuré ni la cadence réelle du jeu chez Frédéric
   (les 38 battements/s de `cadence.txt` sont sous débogueur, avec
   `journal = 1`, que la doc dit faire tomber de 60 à 25 images/s), ni la gigue.
   **« Plusieurs » est mesuré ; « trois » est calculé.**
3. **Si une part du « hasardeux » vient d'ailleurs que de la validation.**
   Je n'ai désassemblé que le chemin de la validation et du curseur partagé
   (`0x1801BBBE0`). Les écrans qui lisent le masque arcade **brut** — la grille
   de sélection de personnage, d'après `menu_console.md` §10.2 — n'ont pas été
   vérifiés un par un. S'il reste du flottement **après** le correctif A, c'est
   là qu'il faudra regarder, et il faudra alors que Frédéric nomme **l'écran**.
4. **Si des appuis se perdront à 10 ms.** Le §10 du 2026-09-05 prévient :
   « trop courte, les appuis se perdent ». Le code dit que non — `maj()` et la
   scrutation du moteur tombent dans la même trame, donc `tt - g_presse` vaut
   moins d'une milliseconde à la première lecture — mais **je ne l'ai pas
   mesuré à l'écran sur cette greffe-ci**. Si des appuis se perdent, la fenêtre
   se règle à chaud entre 10 et 16 ms sans recompiler.
5. **Que `Core_execute` batte encore une fois le moteur chargé.** Le rapport
   13 `Input_isOn` par `Core_execute` de `cadence.txt` le dit pour les 30
   premières secondes. Au-delà, le commentaire de `gen_apm_stub.py:1986` laisse
   la question ouverte, et **aucun journal du disque ne porte de ligne
   `RES … tour 600` ou `tour 6000`** qui trancherait. C'est une **absence**, pas
   une mesure : trois états, et je ne sais pas lequel. Sans conséquence sur ce
   correctif (le garde-fou des 50 ms de `entree()` maintient alors
   `Input_isOn` vivant, et la fenêtre de 10 ms reste plus courte qu'une trame),
   mais à ne pas confondre avec une preuve.
6. **Les copies figées de `FS APM3/`** n'ont pas été comparées octet à octet aux
   sources vivantes de `VF5RE/tools/`. J'ai lu les vivantes, qui font foi.

---

## 7. Récapitulatif pour la pose

| | | |
|---|---|---|
| **Cause** | fenêtre de front à **34 ms** au lieu de **10 ms** ; le moteur ne dédoublonne rien | mesurée |
| **Pourquoi** | `VF5RE/tools/scenarios/jouer.txt` (03/09, 08:31) n'a pas la ligne `front` ; il **précède de deux jours** le correctif du 05/09, posé seulement dans `apm_entrees.txt` | mesurée |
| **Correctif A** | `front   = 10` dans `jouer.txt` ligne 13 — **ni recompilation ni relance** | à poser |
| **Correctif B** | défaut `34` → `10`, `gen_apm_stub.py` lignes **324** et **992** — exige de reconstruire `apm.dll` | à poser |
| **Correctif C** | bannière de `jouer.cmd` : 30 ms → 500 ms | cosmétique |
| **Moteur** | **aucun octet à changer** | mesuré |
| **Reste à trancher** | compter les validations **à l'écran** après le correctif A | Frédéric |
