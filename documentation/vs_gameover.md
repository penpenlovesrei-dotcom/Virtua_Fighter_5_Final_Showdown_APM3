# VS (19) et GAMEOVER (20) : ce qui se passe apres le combat

Desassemble le 2026-09-04, apres que le combat a demarre depuis le menu
console. Fait suite a `menu_console.md` (sections 8 a 11) et a
`machine_console.md`.

## 1. Les six gestionnaires, avec leurs vraies bornes

Les entrees `.pdata` sont chainees : la borne d'une entree n'est pas la fin de
la fonction. Bornes reelles, etablies au `tools/plage.py` :

| sous-etat | gestionnaire | plage | taille |
|---|---|---|---:|
| 19 VS | entree `0x1800DC890` | -> `0x1800DCA61` | 465 o |
| 19 VS | milieu `0x1800DAAC0` | -> `0x1800DAE1D` | 861 o |
| 19 VS | sortie `0x1800DBAC0` | -> `0x1800DBB4A` | 138 o |
| 20 GAMEOVER | entree `0x1800DC860` | -> `0x1800DC88B` | 43 o |
| 20 GAMEOVER | milieu `0x1800DAA60` | -> `0x1800DAABA` | 90 o |
| 20 GAMEOVER | sortie `0x1800DB950` | -> `0x1800DBAC0` | 368 o |

## 2. LE TYPE DE PARTIE : `0x180751010`

C'est la trouvaille de cette lecture, et elle commande tout le reste.

`0x18019C090()` rend le dword `[0x180751010]`. Il est ecrit par deux fonctions
seulement, `0x18019C420(type, ...)` et `0x18019C4A0(type, ...)`, et **sept
sites** les appellent :

| site | fonction | type pose |
|---|---|---:|
| `0x1801DCC61` | `0x1801DC620` -- **la page du menu console** | **0** |
| `0x18023A425` | `0x18023A3C0` -- le chemin APM3 | **0** |
| `0x18023C727` | `0x18023C6D1` -- APM3 | 0 |
| `0x1801DC3A6` | `0x1801DC270` | 0 |
| `0x1801DD73E` | `0x1801DD6A0` | **1** |
| `0x1801DC179` | `0x1801DC050` (`DIFFICULTY CHANGE WINDOW`) | calcule (2 ou 3) |
| `0x1801A4252` | `0x1801A4160` | calcule (3 ou 4) |

Les valeurs testees ailleurs vont de 0 a 5, et 8. Lecture la plus simple qui
tienne : **0 = solo/borne, 1 = versus, 2 et 3 = score attack / license
challenge, 4 = entrainement**.

## 3. La sortie de GAMEOVER ne fait quelque chose que pour le type 1

`0x1800DB950` est la fonction qui, sur le papier, decide « rejouer ou changer
de personnage ». Sa toute premiere decision :

    0x1800DB97B  call 0x18019C090        ; le type de partie
    0x1800DB980  cmp  eax, 1
    0x1800DB983  jne  0x1800DBA68        ; tout le reste est saute

Pour le type 1 seulement, elle lit la session, interroge `0x1800A78A0()` et :

* rend 0 -> `0x1800DA9C0(0x13)`, **sous-etat 19 VS** -- on rejoue ;
* rend 1 -> `0x1800DA9C0(0x11)`, **sous-etat 17 SELECTOR** -- on rechoisit ;
* autre -> rien.

Pour tous les autres types -- **dont le notre, 0** -- elle tombe en
`0x1800DBA68`, qui se contente de nettoyer les deux combattants
(`0x1800CC260`/`0x1800CC220`/`0x1800CC2D0`/`0x1800CC2F0`/`0x1800CB110`) et
rend vrai **sans demander aucun sous-etat**.

## 4. Mais le vrai arbitre est ailleurs : `0x1800DB100`

La suite du combat ne se decide pas dans GAMEOVER, elle se decide **dans le
milieu de VS**, qui appelle `0x1800DB100` et demande ce qu'elle rend :

    0x1800DABD2  call 0x1800DB100
    0x1800DABD7  mov  ecx, eax
    0x1800DABD9  call 0x1800DA9C0        ; demande ce sous-etat

`0x1800DB100(void)` -> identifiant de sous-etat. Valeur par defaut `0x13` (VS).
Elle branche sur `0x1800244D0(sous-objet de session)` :

| cas | resultat |
|---|---|
| 0 | delegue a `0x1800DB4B0` (989 o), qui rend `0x11`, `0x13` ou `0x14` selon le type de partie et l'issue |
| 1 | si `0x1800B2720(...)` -> **`0x14` GAMEOVER** ; sinon si `0x1800B1D30(session, table[joueur])` -> **`0x11` SELECTOR** ; sinon `0x13` VS, ou **`0x12` MODE_SELECTOR** si `0x1800244D0(...) == -1` |
| 2 | remet les deux joueurs (`0x1800B27A0`) et rend **`0x14` GAMEOVER** |
| autre | `0x1800B8540(session)` puis `0x13` VS |

**La chaine du combat s'auto-entretient donc**, contrairement a l'entree dans
le mode, qui elle manquait : VS -> GAMEOVER / SELECTOR / MODE_SELECTOR / VS.
Le milieu de VS demande aussi directement `0x11` (SELECTOR) quand
`0x1800BA070`/`0x1800B9FD0` le disent.

`0x18034B208` reapparait ici (`0x1800DB1F4`) : c'est la meme table que celle
lue par le selecteur en `0x18016CCBB`.

## 5. Les deux sorties de secours, au niveau du MODE

`0x1800DA9D0`, le milieu du mode GAME, surveille deux drapeaux a chaque trame :

    0x1800DA9DB  bl  = 0x1801B6FE0()     ; -> mode 0 STARTUP + sous-etat 3 CS_TITLE
    0x1800DA9E3  al  = 0x1801B6E40()     ; -> mode 4 MENU

Autrement dit, **meme si aucun sous-etat n'est demande, le mode peut rendre la
main au menu**. C'est la porte de sortie du parcours console, et elle existe
deja : nous n'avons rien a fabriquer de ce cote.

Le troisieme cas (`type == 3`, plus `0x1801B6E30()` et un bouchon) mene a
`0x1800DCB40`.

## 6. Le reste, en bref

**Entree de VS `0x1800DC890`** : coupe le son (`0x1801B7060(0)`), pose la phase
3 sur le gestionnaire `0x18039F560`, et **est gardee par un bouchon** --
`0x1800DC8CC call 0x180007450 ; jne 0x1800DCA5A` : a vrai, toute l'entree
serait sautee. Bouchonne a faux, elle s'execute : c'est ce qui nous sauve.

**Sortie de VS `0x1800DBAC0`** : reinstalle trois rappels par
`0x180087420(code, fonction, 0)` -- codes 9, 0xF, 0x10 vers `0x1800DBD60`,
`0x1800DC520` et `0x1800DBB90` --, et porte **une branche propre a la
console** : `cmp byte [0x180C3B701], 0 ; jne` -> si `game_mode == 0`, appelle
`0x1801E7C20`. C'est le seul endroit de VS/GAMEOVER ou la console diverge de la
borne.

**Entree de GAMEOVER `0x1800DC860`** : phase 4, et si le type vaut 2,
`0x1801D2610` (le circuit `CLASS UP WINDOW` / license challenge).

**Milieu de GAMEOVER `0x1800DAA60`** : rend « fini » quand `0x1800B9E10()` est
faux et que ni `0x18008B570()` ni `0x18008B580()` ne retiennent la main ; pour
le type 2, exige en plus `0x1801D2600()` et `0x1801D1C60()`.

## 7. Ce que cela predit, et qu'il faut voir a l'ecran

Notre parcours console tourne en **type 0**. Donc, a la fin d'un combat :

* `0x1800DB100` doit rendre `0x14` (GAMEOVER) ou `0x11` (SELECTOR) -- la chaine
  ne se rompt pas ;
* la sortie de GAMEOVER, elle, **ne demandera rien** ;
* et c'est `0x1801B6E40()`, au niveau du mode, qui doit ramener au menu.

Trois issues a distinguer : retour au menu console (chaine complete), retour a
l'ecran de selection (l'arbitre a choisi `0x11`), ou blocage sur l'ecran de fin
(personne ne demande la suite -- et c'est alors `0x1801B6E40` qu'il faut lire).

Confiance : **SUPPORTED** pour la lecture statique ; **UNKNOWN** pour ce qui se
passe reellement, aucun combat n'ayant encore ete mene a son terme.

---

## 8. MESURE : retour a l'ecran-titre -- et le maillon 4 (2026-09-04)

Verdict de Frederic, combat mene jusqu'au bout : **« retour a l'ecran titre
apres le combat »**.

Donc la prediction de la section 7 est verifiee sur l'essentiel -- **la chaine
ne se rompt pas** : le combat se termine, `0x1800DB100` fait son travail,
GAMEOVER passe, et le mode rend la main. Mais c'est la **premiere** des deux
sorties de secours qui a pris, pas la seconde.

### 8.1 Pourquoi le menu ne pouvait pas gagner

Les deux predicats lisent le meme contexte `[0x180752148]` :

    0x1801B6FE0 : ctx+0x68C1 ET ctx+0x68C2   -> vrai, puis efface 0x68C2
    0x1801B6E40 : ctx+0x68C1, puis trois autres verrous

et le dernier verrou du retour au menu est un bouchon :

    0x1801B6E8E  call 0x180007450   ; rend toujours 0
    0x1801B6E95  je   ...           ; toujours pris -> rend FAUX
    0x1801B6E97  mov  al, 1         ; jamais atteint

**Le retour au menu ne peut jamais rendre vrai.** Meme mal que la case de
Dural, que la porte `DLC STORE` et que le predicat de deblocage : un dernier
verrou bouchonne, sur un chemin par ailleurs complet.

`ctx+0x68C2`, lui, est pose par `0x1801BA100` -- une fonction utilisee comme
**rappel** (deux `lea rdx` seulement, dans `0x1801B87E0` et `0x1801B8C40`), qui
demande le titre quand son `rdx` est nul.

### 8.2 Le correctif, et pourquoi il est sans portee

On **ne touche pas** a `0x1801B6E40` : il a quatre appelants
(`0x1800DA9D0`, `0x1800DD700`, `0x1801DBBD0`, `0x1801E4E60`). On corrige la
**branche**, ou la portee est nulle : le mode 2 GAME n'a aucun demandeur dans
tout le moteur en dehors de notre caverne, donc `0x1800DA9D0` ne tourne que sur
notre parcours.

Les 17 octets de la branche « titre » deviennent la branche « menu », copiee
telle quelle de `0x1800DAA29` -- mode 4, **sans sous-etat** : c'est l'entree du
mode MENU qui pose le sien.

    0x1800DA9EC  mov  ecx, 4
    0x1800DA9F1  call 0x1800DA9A0        ; mode 4 MENU
    0x1800DA9F6  nop x7

(avant : `xor ecx,ecx ; call 0x1800DA9A0` puis `mov ecx,3 ; call 0x1800DA9C0`,
soit mode 0 STARTUP + sous-etat 3 CS_TITLE.)

C'est le **quatrieme maillon**, et il est dans `--transition-game` comme les
trois autres.

### 8.3 Le parcours console, au complet

    MENU_MAIN
      -> SINGLE PLAYER            maillon 1 : session creee, mode GAME, SELECTOR
      -> SELECTOR                 la grille, Dural comprise
      -> VS                       maillon 2 : la fin du selecteur mene au combat
      -> GAMEOVER / SELECTOR      arbitre 0x1800DB100, deja en place
      -> MENU_MAIN                maillon 4 : retour au menu, non au titre

### 8.4 VERIFIE : LE PARCOURS BOUCLE

Verdict de Frederic : **« retour au menu OK, on peut relancer un combat »**.

Le parcours console est donc complet et **cyclique** : menu -> selection ->
combat -> fin -> menu -> combat. Quatre maillons fabriques (sections 9 et 11 de
`menu_console.md`, section 8 ici), tout le reste etait deja la et n'attendait
que d'etre appele.

Ce que cela etablit au-dela du parcours lui-meme : **le mode GAME, ses quatre
sous-etats et l'arbitre de fin de combat sont intacts dans ce build**. Rien
n'avait ete retire du coeur ; ce qui manquait, ce sont les quelques
instructions qui y menent, et quatre predicats bouchonnes.
