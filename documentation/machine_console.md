# La machine a etats console de VF5FS, entierement cartographiee

Etabli le 2026-09-04, sur `vf5fs-pxd-w64-Retail_APM3.dll`. Ce document remplace
toute affirmation anterieure sur « ce que le build arcade a supprime du menu ».

---

## 1. Deux tables, et rien d'autre

Tout le pilotage tient dans deux tables de descripteurs et une fonction.

| | adresse | entrees | taille | clef |
|---|---|---:|---:|---|
| **modes** (tetes) | `0x1803A0190` | 10 | 0x68 | `+0x00` |
| **sous-etats** | `0x1803A05A0` | 55 | 0x20 | `+0x00` |

Chaque descripteur porte **trois gestionnaires** aux decalages `+0x08`, `+0x10`
et `+0x18`. Le repartiteur `0x1800DA550` les appelle selon une **phase** :

```
0x1800DA618  mov  r8d, [0x18070C4F0]      ; la TETE courante
0x1800DA61F  lea  r9,  [0x1803A0190]      ; table des modes
0x1800DA631  cmp  [rax + r9], r8d         ; recherche par clef, pas par position
0x1800DA657  imul r8, rdx, 0x68
0x1800DA66D  mov  r9, [r8 + rax*8 + 8]    ; gestionnaire[phase] du MODE
0x1800DA677  call r9
...
0x1800DA701  mov  edx, [0x18070C50C]      ; le SOUS-ETAT courant
0x1800DA707  lea  r8,  [0x1803A05A0]      ; table des sous-etats
0x1800DA714  cmp  [rax], edx              ; recherche par clef
0x1800DA71B  add  rax, 0x20
0x1800DA71F  cmp  rbx, 0x37               ; 55 entrees
0x1800DA738  mov  rdx, [rbx + rax*8 + 8]  ; gestionnaire[phase] du SOUS-ETAT
0x1800DA742  call rdx
```

**Piege, et il a coute une fausse conclusion le 2026-09-04** : les deux tables
sont indexees par leur champ `+0x00`, **pas par leur position**. Lire la table
des modes dans l'ordre donne `MENU` la ou est `GAME` et inversement. Une table
reguliere n'est pas une table identifiee.

### Les globaux du pilotage

| adresse | role |
|---|---|
| `0x18070C4F0` | tete courante |
| `0x18070C50C` | **sous-etat courant** |
| `0x18070C4FC` | phase du mode |
| `0x18070C518` | phase du sous-etat |
| `0x18070C510` | sous-etat demande |

`0x1800DA800` est le journaliseur/poseur : il ecrit la tete en `0x18070C4F0`,
imprime « [ancien]->[nouveau] » avec les tables de noms, et une tete valant
`0xA` (MAX) veut dire « ne change pas ».

---

## 2. Les dix modes

| id | tete | entree | milieu | sortie |
|---:|---|---|---|---|
| 0 | STARTUP | `0x1800DE3D0` | `0x1800DD700` | `0x1800DDA40` |
| 1 | ADVERTISE | **bouchon** | **bouchon** | **bouchon** |
| 2 | **GAME** | `0x1800DC7D0` | `0x1800DA9D0` | `0x1800DB890` |
| 3 | DATA_TEST | **bouchon** | **bouchon** | **bouchon** |
| 4 | **MENU** | `0x1800DCBF0` | bouchon | `0x1800DCB80` |
| 5 | **CS_TERM** | `0x1801E5010` | `0x1801E4E60` | `0x1801E4F60` |
| 6 | **CS_TRAINING** | `0x1801E5170` | `0x1801E4E60` | `0x1801E5110` |
| 7 | ONLINE | **bouchon** | **bouchon** | **bouchon** |
| 8 | **APM3** | `0x18023DC30` | bouchon | `0x18023C2A0` |
| 9 | APM3_TESTMODE | **bouchon** | **bouchon** | **bouchon** |

Quatre modes retires : `ADVERTISE`, `DATA_TEST`, `ONLINE`, `APM3_TESTMODE`.
**Six vivants, dont `MENU`, `GAME`, `CS_TERM` et `CS_TRAINING`** -- c'est-a-dire
tout le parcours console.

---

## 3. Les 55 sous-etats : 24 vivants, 31 retires

**Vivants** : `DATA_INITIALIZE`, `SYSTEM_STARTUP`, `WARNING`, `CS_TITLE`,
`CS_SIGNIN`, `CS_AUTOLOAD`, `CS_DEMO`, **`SELECTOR`**, **`MODE_SELECTOR`**,
`VS`, `GAMEOVER`, **`MENU_MAIN`**, `CS_TERM_CUSTOMIZE`, `CS_TERM_REPLAY_PLAY`,
`CS_TERM_LAST_PLAY`, `CS_TERM_CLIP_PLAY`, `CS_TRAINING`, `APM3_ENTRY`,
`APM3_SELECTOR`, `APM3_GAME_VS`, `APM3_GAMEOVER`, `APM3_TRAINING`,
`APM3_ONLINE_VS`, `APM3_TESTMODE_MAIN`.

**Retires** (bouchons aux trois gestionnaires) : `LOGO`, `RATING`, `DEMO`,
`TITLE`, `TITLE_TV`, `LOGO_TV`, les quatre `*_TERMINAL`, **les quinze
`DATA_TEST_*`**, et les six `ONLINE_*`.

Cela **confirme par une deuxieme voie** ce qui avait ete etabli le 2026-09-03
sur les `DATA_TEST_*` : ils ne sont pas seulement absents des menus, leurs
gestionnaires memes sont des bouchons.

Les trois gestionnaires qui nous interessent :

```
17 SELECTOR        entree 0x1800DCA90   milieu 0x1800DB270   sortie 0x1800DBB70
18 MODE_SELECTOR   entree 0x1800DCA70   milieu 0x1800DAE20   sortie 0x1800DBB50
36 MENU_MAIN       entree 0x1800DCCA0   milieu BOUCHON       sortie 0x1800DCBE0
```

`MENU_MAIN` a son entree et sa sortie, mais **son milieu est un bouchon** :
le menu principal peut donc s'ouvrir et se fermer, mais rien ne le fait vivre.
C'est la cause profonde du « menu qui s'affiche mais ne fait rien », et elle est
en amont de tout ce qu'on a corrige dans ses pages.

`SELECTOR`, lui, a ses trois gestionnaires.

---

## 4. Ce que cela change pour Dural

`is_dural_unlocked` n'agit qu'a un seul endroit du binaire : la page
**`CHAR SELECTOR`** (vtable `0x180533260`, construite au demarrage par
`0x1802441A0`, mise en place `0x1801D0800`), ou il fait passer la grille de
**18 a 20 cases** :

```
0x1801D0BAA  and   r8b, 0xF               ; 2 sans Dural, 6 avec
0x1801D0BD5  test  r8b, 4                 ; le bit 2, seule difference
0x1801D0BD9  mov   eax, 0x12              ; 18
0x1801D0BE5  mov   ecx, 0x14              ; 20
0x1801D0BF1  cmovne eax, ecx
0x1801D0BFB  mov   [rbp+0x22c], eax       ; le nombre de cases
```

Et le sous-etat `SELECTOR` qui pilote cette page **est vivant**. La route existe
donc entierement ; il reste a la faire emprunter.

### Ce qui ne marche pas, et pourquoi

- **Devier `shift_next_mode`** (`tracer_etats --devier`) pose la valeur mais
  n'execute pas les gestionnaires d'entree : mesure, `0x1801D0B80` n'est jamais
  appele. On change l'etiquette, pas l'etat.
- **Devier avant `CS_AUTOLOAD`** plante a `moteur+0xB1D33`, un accesseur
  `movzx eax, byte [rax+rcx+0xC]` dont la table est nulle : `CS_AUTOLOAD`
  l'alloue. **Meme adresse exactement** qu'en sautant `APM3_ENTRY` le
  2026-09-03 -- deux chantiers, un seul point de rupture.

### La prochaine mesure

Ecrire directement les globaux du repartiteur plutot que de devier :
`0x18070C50C = 17` (SELECTOR) et `0x18070C518 = 0` (phase entree), une fois
`CS_AUTOLOAD` passe. Le repartiteur appellera alors `0x1800DCA90`, l'entree du
sous-etat, qui est ce qui construit et arme la page.

---

## 5. Le verdict : la page `CHAR SELECTOR` n'a AUCUN pilote

Mesures et lectures faites, dans cet ordre :

1. **Ecrire les globaux marche la ou devier echoue.** En posant
   `0x18070C50C = 17` (SELECTOR) et `0x18070C518 = 0` (phase entree), le
   repartiteur appelle bel et bien les gestionnaires :

   | jalon | passages |
   |---|---:|
   | `0xDC7D0` entree du mode GAME | 1 |
   | `0xDCA90` entree de SELECTOR | 1 |
   | `0xDB270` milieu de SELECTOR | 1326 |

   C'est le levier qui manquait : **on peut faire tourner n'importe quel
   sous-etat vivant**, y compris ceux qu'aucune transition n'atteint.

2. **Mais `SELECTOR` ne pilote pas la grille console.** Ses deux gestionnaires
   travaillent sur un objet en `[0x180714928]` via les fonctions
   `0x18016Cxxx`/`0x18016Dxxx` : c'est le selecteur **de combat**, celui que
   `APM3_SELECTOR` partage (meme gestionnaire de sortie `0x1800DBB70`).
   Mesure : `0x1801D0B80`, la mise en place de la grille, **0 passage**.

3. **Et la page `CHAR SELECTOR` n'est appelee par personne.** Son constructeur
   `0x1801E57E0` range l'objet en **`0x180753848`**, et ce global n'a que
   **quatre references dans tout le binaire** : deux dans le constructeur, deux
   dans le destructeur `0x1801E5840`. Aucun code ne le lit pour mettre la page
   a jour ni pour la dessiner.

   Verification de la premisse : le constructeur appelle `0x180244C80(objet)`
   juste avant, ce qui pouvait etre un enregistrement dans une liste de pages
   -- auquel cas la page aurait un pilote invisible depuis le global. Lecture
   faite : `0x180244C80` est le **constructeur de la classe de base** (il pose
   la vtable `PN$`, met les champs a zero et copie le nom « unknown »). Ce n'est
   pas un registre. La conclusion tient.

**Donc** : dans le build APM3, la page qui porte le passage de 18 a 20 cases
existe en memoire, est construite a chaque demarrage, et **n'est jamais
affichee**. `is_dural_unlocked` agit sur un ecran mort.

Confiance : **SUPPORTED** (lecture statique complete des references ; pas de
contre-epreuve dynamique, qui demanderait un point d'arret sur la vtable de la
page).

### Ce que cela ferme, et ce que cela ouvre

**Ferme** : la route console vers Dural. Ni le menu (`MENU_MAIN` a son milieu
bouchonne), ni le forcage de sous-etat ne peuvent afficher cette grille,
puisqu'elle n'a pas de pilote du tout.

**Ouvre** : le selecteur reellement vivant est celui du combat --
`SELECTOR` (17) et `APM3_SELECTOR` (49), sur l'objet `[0x180714928]` et les
fonctions `0x18016Cxxx`. C'est **lui** qui affiche les 19 cases de la borne.
La question devient donc : *ce selecteur-la a-t-il, lui aussi, un nombre de
cases parametrable, et Dural peut-elle y etre ajoutee ?* C'est un chantier
net, et le levier d'exploration existe desormais (forcage des globaux).
