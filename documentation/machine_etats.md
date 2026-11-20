# La machine à états de `vfes.exe` — et comment entrer en mode entraînement

Session du 2026-09-02. Le but était d'atteindre l'écran de test d'entrées du menu opérateur,
pour nommer les treize codes de boutons. Cet écran s'est révélé hors d'atteinte — mais la
route y menant a livré mieux : **le mode entraînement**, où le partenaire ne bouge pas.

---

## 1. Le menu opérateur

`Sequence_isTest` est un des 57 exports d'`apm.dll`. Le stub le rendait faux ; il est
désormais piloté par le scénario (`test = 1` dans `apm_entrees.txt`), sans recompilation.
Le jeu démarre alors dans **`GAME TEST MODE`** :

```
BOOKKEEPING / GAME ASSIGNMENTS / SOUND SETTING / BACKUP DATA CLEAR
SUB SYSTEM TEST MODE / EXIT
        SELECT WITH SERVICE BUTTON AND PRESS TEST BUTTON
```

### Deux codes d'entrée nommés

Le pied de page nomme les deux boutons, et le relevé du stub dit lesquels le jeu interroge :
en mode test, `Input_isOnNow` est appelé pour **0, 1, 7 et 8** — le code **1 n'apparaît nulle
part ailleurs**. Vérifié à l'écran :

| code | bouton | preuve |
|---:|---|---|
| **1** | **SERVICE** | déplace le curseur du menu, capture à l'appui |
| **0** | **TEST** | valide : appuyé sur `EXIT`, le jeu quitte le mode test |

Confiance : **CONFIRMED**.

**Piège de mesure** : les menus appliquent une **auto-répétition**. Un appui de 350 ms balaie
les six lignes et ramène le curseur à son point de départ — ce qui donne l'illusion que rien
n'a bougé, et m'a d'abord fait conclure à tort que le code 1 n'était pas SERVICE. Mesure :
80 ms ⇒ trois lignes, 40 ms ⇒ deux, **20 ms ⇒ une seule**. Le stub relit donc son scénario
toutes les **30 ms** et non 250 : à 250 ms, aucune impulsion assez brève n'était possible.
`tools/menu_test.py` navigue en **lisant la position du chevron** dans une capture, plutôt
qu'en comptant les pas.

### L'écran de test d'entrées est hors d'atteinte

`SUB SYSTEM TEST MODE` rend la main au menu **système** de la borne, servi par la vraie
`apm.dll` via `Core_execute`. Notre stub rend la main immédiatement : le jeu s'arrête. Le menu
du jeu, lui, n'a **aucun écran de test d'entrées**. La voie est donc fermée tant qu'on n'écrit
pas un `Core_execute` qui simule le shell ALL.Net — ce qui n'en vaut pas la peine.

`GAME ASSIGNMENTS`, en revanche, se lit : `SINGLE DIFFICULTY`, `SINGLE RULE 2/45/220`,
`ENABLE LOCAL MATCH`, `ENABLE GLOBAL MATCH`, `ENABLE CONTINUE`, `ENABLE DEMO SKIP`… et une
ligne qui a tout changé : **`TRAINING TIME LIMIT(min) 7`**.

---

## 2. La machine à états

Le moteur en tient une, nommée. **`0x1800DA800`** en est le changement d'état :

```
SetState(ecx = etat de tete, edx = sous-etat)
    [0x18070C4F0] = etat de tete courant
    [0x18070C50C] = sous-etat courant
    journalise « [ancien]->[nouveau] » avec les noms
```

Il y a **deux** tables de noms, et non une :

| table | adresse | entrées | contenu |
|---|---|---:|---|
| états de tête | `0x1803A0C80` | 11 | `STARTUP`, `ADVERTISE`, `GAME`, `DATA_TEST`, `MENU`, `CS_TERM`, `CS_TRAINING`, `ONLINE`, `APM3`, `APM3_TESTMODE`, `MAX` |
| sous-états | `0x1803A0CE0` | 56 | `DATA_INITIALIZE` … `APM3_TESTMODE_MAIN`, `MAX` |

Le découpage se prouve tout seul : `SetState` écrit le sentinelle **`0x37` = 55**, qui est
exactement le `MAX` de la seconde table. Confiance : **CONFIRMED**.

Les sous-états qui nous concernent :

| n° | nom |
|---:|---|
| 48 | `APM3_ENTRY` |
| 49 | `APM3_SELECTOR` |
| 50 | `APM3_GAME_VS` |
| 51 | `APM3_GAMEOVER` |
| **52** | **`APM3_TRAINING`** |
| 53 | `APM3_ONLINE_VS` |
| 54 | `APM3_TESTMODE_MAIN` |

### Le parcours réel, relevé

`tools/tracer_etats.py --tracer` pose un point d'arrêt sur `SetState` et imprime chaque
transition en clair :

```
 1  etat [STARTUP] -> [APM3]   sous-etat [CS_TITLE]       -> [MAX]
 2  etat [APM3]    -> [MAX]    sous-etat [APM3_ENTRY]     -> [APM3_SELECTOR]
 3  etat [APM3]    -> [MAX]    sous-etat [APM3_SELECTOR]  -> [APM3_GAME_VS]
```

Trois transitions, pas une de plus, de l'écran-titre au combat. Le premier START fait
`ENTRY → SELECTOR` (la sélection de personnage), le second `SELECTOR → GAME_VS` (le combat).

---

## 3. Le mode entraînement, par déviation

`APM3_TRAINING` est le **frère** de `APM3_GAME_VS` dans la même énumération. Il suffit donc,
au moment où le jeu demande le sous-état 50, d'écrire 52 dans `rdx` :

```
py -3 tools/tracer_etats.py --devier 50 52
```

Le jeu emprunte alors **sa propre machinerie de transition** — bien plus sûr que d'écrire
l'état en mémoire. Résultat, vérifié à l'écran (`analysis/training_01.png`,
`training_02.png`) :

- l'écran de chargement affiche « en mode DOJO, le bouton SELECT remet les personnages en
  place » ;
- puis la scène d'entraînement s'ouvre, avec l'affichage des **données de trame** — 攻撃発生
  (apparition de l'attaque), `HIT`, 硬化差 (avantage) — et un **partenaire qui ne bouge pas**.

Confiance : **CONFIRMED**.

### Pourquoi cela compte

Toutes les mesures d'entrée avaient échoué pour la même raison : l'adversaire géré par la
machine agit pendant qu'on mesure. Sur 48 mesures d'une passe complète en combat, **une seule**
s'était répétée. En mode entraînement, **seul le joueur agit** : la mesure redevient possible.
`tools/carte_entrees.py --dojo` pose la déviation lui-même, dès le chargement du moteur.

L'affichage des données de trame est en outre un **contrôle croisé** pour les 32 fenêtres
temporelles : le jeu y affiche lui-même les trames d'apparition et d'avantage.
