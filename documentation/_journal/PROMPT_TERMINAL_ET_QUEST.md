# PROMPT — Réparer le mode TERMINAL, et finir le portage du Quest (X360 → FS)

> À coller tel quel comme premier message d'une nouvelle séance.
> L'agent travaille **seul**, **en français**, et **sans poser de question**
> tant qu'il lui reste une tâche qui n'en dépend pas.

---

## 0. La mission, en deux phrases

1. **Réparer le mode TERMINAL** de la borne APM3 : l'écran s'ouvre et affiche
   son décor, mais **aucun bouton n'y valide ni n'y annule** — c'est mesuré,
   la cause est connue, la réparation est à écrire.
2. **Finir le portage du mode Quest** de VF5 Xbox 360 (2007) vers Final
   Showdown : le code de 2007 est décompilé à **323/323**, la carrière est
   écrite, il reste à **voir**, **corriger** et **compléter**.

Les deux volets se rejoignent : Customize, c'est la boutique du Quest.

---

## 1. Le terrain

| | |
|---|---|
| atelier | `C:\Users\frede\Desktop\VF5RE` |
| moteur | `runtime\media\vf5fs\vf5fs-pxd-w64-Retail_APM3.dll`, base `0x180000000` |
| **toujours analyser** | le **`.origine`** — jamais la DLL patchée |
| notre module | `apm.dll`, source `tools\apm_stub.c` + `tools\quest_runtime.c`, compilé par `tools\gen_apm_stub.py` (MinGW, `-Wall -Wextra`) |
| patcheur | `tools\patch_moteur.py` — il repart **toujours** de `.origine` |
| lanceur du Quest | `tools\quest.cmd` (menu du jeu : **SCOREBOARDS**) |
| journal de bord | `REPRISE.md` (entrées numérotées) + `PROMPT_REPRISE.md` |
| dossiers | `analysis\mode_quest.md`, `analysis\menu_console.md`, `analysis\customize_0x299.md`, `analysis\decors.md` |
| code 2007 décompilé | `analysis\quest\*.c` (323 fonctions), inventaire par `tools\quest_x360.py` |
| interpréteur | **`py -3`** — `python` est un stub inerte sur cette machine |

Le `.par` du jeu est un **lien dur vers un dump en lecture seule** : on ne
réécrit jamais dedans sans le dire. `analysis\reseau_allnet.md` porte une clé
AES : **il ne quitte jamais le dépôt privé**. La PR #1 est **publique** : aucun
octet de jeu dedans.

---

## 2. Les interdits — non négociables, verbatim de Frédéric

* « **alors deja on ne touche pas aux decors de FS, je t'interdit d'y modifier
  quoique ce soit.** » — seule exception écrite : « **La modification du decor
  de dural est OK.** »
* « **ne fait jamais de supposition** » et « **je ne lance plus rien de basé
  sur une supposition** ». Tout se lit dans le code ; s'il faut décompiler, on
  décompile. Une valeur « raisonnable » est un aveu : on cherche la **borne**
  ou la **table**.
* « **je t'interdis de lancer le jeu jusqu'a nouvel ordre** » — **toujours en
  vigueur**. Demander l'autorisation **une seule fois**, en tête de séance, en
  listant tout ce qu'un seul lancement permettrait de trancher ; puis
  **travailler sans**, jusqu'à sa réponse.
* « **non conserve online et remplace leaderboards** » — le Quest occupe
  **SCOREBOARDS** (état `DATA_TEST` / sous-état **35**). ONLINE n'est pas
  touché.
* « **laisse le jeu en anglais** ».
* « **ne relance pas les sous agents, reprends toi meme leur taches en les
  faisant les unes apres les autres** » — **aucun fan-out**. Une tâche, puis
  la suivante.
* Tout ce qui se lance a **son lanceur `.cmd`** double-cliquable (CRLF, ASCII
  pur, en-tête qui explique quoi faire) ; jamais une ligne à recopier.
* Ne reconstruire/patcher que si **`vfes.exe` ne tourne pas**. Ne jamais lancer
  `verifier_lanceurs.py` en tâche de fond **sans `--sans-patch`**.

---

## 3. VOLET A — LE MODE TERMINAL

### 3.1 Ce qui est établi (mesuré, pas supposé)

Chemin complet, `analysis\customize_0x299.md` §1.8 :

    menu principal, entree 4 « TERMINAL » (libelle 0x17C)
      -> TaskMenuTerminal, vtable 0x180532A28, logee en menu+0x2328
         dessin   0x1801E1B10 : { 0x299 Customize, 0x29A Replays }
         valider  0x1801DE340 (curseur 0)
            garde 0x1801B7010  -> VRAIE      garde 0x180029FB0 -> VRAIE
            0x1800DA9A0(5)  mode 5 CS_TERM          [VIVANT]
            0x1800DA9C0(37) sous-etat 37 CUSTOMIZE  [VIVANT]
         entree 0x1801E50B0 -> 0x1801C5B00 -> 0x1801C46F0
         milieu 0x1801E4ED0 -> sequenceur 0x1801C4D60
                etape 0  geometrie du decor  0x18018FCF0  (octet 0x1801C4DA6)
                etape 1  eclairage           0x1800D7130  (octet 0x1801C4DCB)
                etape 10 tache « CUST_MAIN » 0x180245830(0x1807521A0, ...)
                etape 11 BGM vfes_bgm_cus.adx par 0x180185DA0
                etape 12 attendre 0x180244EA0
                etape 40 0x180186D40(0) -> mode 4 MENU
         sortie 0x1801E4FF0 -> 0x1801C5140

**Il n'y a aucun maillon manquant sur ce chemin.** Le décor est réparé et
validé à l'écran (`--decor-perso trm`, les **deux** octets `0x1801C4DA6` et
`0x1801C4DCB` portent `b9 1a 00 00 00`). `trm` **n'est pas** un emplacement
libre : ne jamais le recycler.

### 3.2 LE DÉFAUT À RÉPARER

L'écran de personnalisation lit ses entrées **uniquement par le masque
arcade** — 26 sites, tous `0x1801A2CA0` (front) ou `0x1801A2C10` (tenu). Les
masques qu'il demande, et leur source :

| masque | bit | rôle à l'écran | source |
|---|---|---|---|
| `0x11000` `0x22000` `0x44000` `0x88000` | 12-19 | les quatre directions | **câblées** |
| `0x10`, `0x70` | 4,5,6 | Y, U, Z | câblées |
| `0x200` | 9 | Espace (pièce) | câblée |
| **`0x100`** | **8** | **✕ Back** | **AUCUNE** |
| **`0x800`** | **11** | **◯ Enter** | **AUCUNE** |
| **`0x100000` `0x200000` `0x400000` `0x800000`** | 20-23 | stick analogique | **AUCUNE** |

Parce que `0x180243ED0` — **le** lecteur d'entrées du moteur — ne remplit que
les bits **0-7, 9, 12-19**. Ce ne sont pas des touches mal choisies : ce sont
des boutons que le panneau de la borne n'a pas, alors que l'écran vient de la
console. **C'est pour ça que rien ne valide et que rien ne revient.**

La chaîne, pour mémoire (`tools\entrees.py`, qui l'imprime) :

    apm.dll (notre stub)  Input_isOn(code), codes 0..14 joueur 1, 18..30 joueur 2
      -> 0x180243ED0      compose le masque arcade en 0x180751050 + joueur*0x54
         code stub -> bit : 2:12  5:13  3:14  4:15  7:0  8:1  12:2  11:3
                            13:4  14:5   9:6  10:7   6:9
      -> 0x1801A2200      traduit le masque en codes logiques 0..103
         (table de 16 paires copiee de 0x18040AEC0 par 0x1801A2AB0)

### 3.3 La voie, et ce qu'il faut vérifier avant d'écrire

La réparation consiste à **donner une source aux bits manquants**, donc à
ajouter des lectures à `0x180243ED0`. Il y a un précédent exact dans le
dépôt : pour la sortie de mode, `patch_moteur.py` **ne passe pas par le
masque** et interroge `Input_isOn` directement — créneau **`+0x158`** de la
vtable de l'objet **`[0x180C3B6F8]`** — sur le code **15**, libre entre les
codes du joueur 1 (0-14) et ceux du joueur 2 (18-30).

Avant d'écrire une ligne, **mesurer** :

1. quels codes stub sont **réellement libres** (lire `tools\gen_apm_stub.py`
   et balayer les lectures de codes dans le moteur — ne pas se fier au
   commentaire de `patch_moteur.py`) ;
2. **où poser le détour** dans `0x180243ED0` : cinq octets pile, qui
   **n'avalent** ni une cible de saut ni une frontière d'instruction
   (`tools\pe_disasm.py` ; le désassemblage linéaire déraille, on reprend
   après l'octet indécodable) ;
3. **où mettre le code** : la caverne `.text` est pleine (136 octets sur
   164). Le dépôt sait **greffer une section exécutable avec ses relocations**
   (`analysis\greffe_relocations.md`, drapeaux `0xE0000060`) et
   `patch_moteur.py` en pose déjà une. Vérifier la place disponible **dans
   la greffe existante** avant d'en créer une autre, et
   `verifier_disposition()` doit refuser tout recouvrement ;
4. que les bits 8 et 11 **ne sont lus nulle part ailleurs** que dans cet
   écran (balayage linéaire des immédiats `0x100` et `0x800` passés à
   `0x1801A2CA0`/`0x1801A2C10`) — sinon on casse un autre écran. **Une garde
   partagée retirée casse les autres cas.**

Puis : une option `--terminal-boutons` dans `patch_moteur.py`, ajoutée à
`tools\console.cmd` et à `tools\quest.cmd`, plus un lanceur d'essai dédié
`tools\terminal.cmd`.

### 3.4 Ce qui n'est pas encore lu, et qui fait partie du volet

* **`Replays` (libellé `0x29A`)**, la deuxième entrée de TERMINAL : son
  chemin n'a **jamais** été suivi. Le faire comme le §1.8 l'a fait pour
  Customize, et dire s'il est bouchonné.
* **`CARD SELECTOR` / `DATA SELECTOR` / `CHAR SELECTOR`** : l'écran de
  personnalisation les nomme (`analysis\carte_customize.md`) ; sur borne ils
  supposent une carte VF.NET. Établir **par le code** ce que la borne attend,
  et si un profil local suffit.
* Le sous-système de personnalisation lui-même : **312 fonctions, 68 Ko,
  jamais ouvertes**. Ne pas l'ouvrir en entier — cartographier **la zone**
  utile, prémisse écrite.

### 3.5 Critère de réussite

Dans TERMINAL → Customize : le curseur bouge, **◯ valide**, **✕ revient**, et
la sortie rend la main au mode 4 MENU. Vu à l'écran, capture à l'appui.

---

## 4. VOLET B — LE MODE QUEST

### 4.1 Ce qui est POSÉ dans le jeu

Carte à neuf lieux, fenêtres, liste des rivaux (pagination, étoile des battus,
masquage `？？？？？`), statut, 492 libellés ajoutés à `string_array`
(23 052-23 543), `npc_tbl.bin` (mille rivaux) posé dans `rom/`, profil
persistant `quest_profil.bin`, **création de données** (choix du personnage,
NO-NAME / 10th kyu, 50 000 G versés à +500 par trame), **carte du joueur**
(nom, grade, W, L, win ratio, argent), **grade des rivaux** (`npc_tbl+0x7C`),
musique `vf5ps3_b03map.adx`, photo du lieu sous le curseur, contour noir sous
les libellés, et le **combat** qui part avec les bons combattants, le bon
décor, le bon temps, les bons rounds et la bonne force de CPU.

**Écrit, compilé, mais JAMAIS VU À L'ÉCRAN** (le jeu n'a pas été relancé
depuis) : l'après-combat (verdict, bit battu, série, argent, grade), l'écran
de rencontre et les deux répliques, les réglages de difficulté, la liste des
emblèmes, la **boutique** (3 382 objets, prix = colonne *Point* du CSV de FS),
le **tournoi** (trois tours), les **bruitages** de menu, le **picto de grade**
et la photo de lieu. **C'est la première chose à vérifier.**

### 4.2 Les repères du moteur de FS (déjà mesurés — ne pas les rechercher)

| | |
|---|---|
| session de combat | `DAT_1806F9C18`, créée par `0x1800B23A0` ; `+0x08` joueur courant, `+0x28+j*4` personnage, `+0x4E0` sous-objet combat |
| **le vainqueur** | `[session+0x4E0+0x1054]` |
| descripteur | 20 mots (0x50 o) posés par `0x1800B34D0(session+0x4E0, desc)` ; bâti par `0x1800B8540(session)` ; `[13]` temps, `[14]` santés, `[15]` rounds, `[17]` décor, `[19]` drapeaux (0x4C premier, 0x4E dernier — pour le Quest : les deux) |
| force du CPU | `0x18010ED40(joueur, u16, perso)` → `[fiche+0x1CF8]` ; 2007 : `npc_tbl+0x10` (float 0..1) +0,2/+0,4 selon la difficulté, +0,01/0,05/0,1 selon la série, ×30 (×31 en tournoi) ; FS : table 5×8 de `rom/game_score.txt` |
| dossier joueur | `[0x18070FB10] + 0x18 + j*0x5A0` ; `+0x160` = `std::bitset<2000>` des objets |
| texte 2D | recette `0x1801BC580` (rang 127) |
| sprite | `FUN_180189880(desc)` → `desc+0x04` id, `+0x0C` drapeaux, `+0x34` position → `FUN_180187C00(desc)` |
| son | amorce `0x180185AB0(nom)` ; BGM `0x180185DA0(voie, chemin, 0)`, arrêt `0x180186D40(voie)` |
| AET | `0x180171E90(ctx, rang, scène, calque, prio, flags)` / `0x180171F40(..., position, ..., début, fin)` ; `0x10000` boucle, `0x20000` une fois puis tient. **Jamais la composition entière** : `sta` une fois, `neu` en boucle, `end` ferme |
| planches importées | que (scène 683), qwin (685), tnt, tnto, **qdan (688)** |
| npc_tbl.bin | 0x90 o/enr., **gros-boutiste** : `+0x00` nom, `+0x04`/`+0x08` répliques, `+0x10` force, `+0x14` personnage, `+0x18` et `+0x48` deux listes de 24 objets, **`+0x7C` grade** (0 = 10th kyu, 42 valeurs), `+0x88` lieu |
| profil 2007 | `sauvegarde+0xC0` (`FUN_8230B5B8`) : `+0x08` difficulté, `+0x74` rencontrés (1000 bits), `+0xEC` argent (plafond 999 999), `+0xF4` battus, `+0x174`/`+0x178` W/L |
| notre profil v3 | 0x250 o : perso `0x11C`, argent `0x120`, W `0x124`, L `0x128`, grade `0x12C`, nom `0x130`, créé `0x140`, difficulté `0x144`, série `0x148`, objets `0x150` (250 o), emblèmes `0x24C` — **la migration reprend un profil v1/v2, elle ne le jette pas** |

### 4.3 Ce qui RESTE, dans l'ordre

1. **Voir à l'écran** tout le §4.1 alinéa 2, et corriger ce qui ne va pas.
2. **Le HUD du combat** : que l'adversaire soit le **rival**, avec son **nom**
   et son **costume**. Il faut cartographier le dossier `0x5A0` de FS : où vit
   le nom affiché pendant le combat, où vit la tenue portée, quelles fonctions
   habillent le combattant. C'est ce que Frédéric appelle « le vrai combat du
   mode Quest ».
3. **Le plantage intermittent** au lancement du combat : `tools\plantage_quest.cmd`
   écrit la section et l'adresse fautives dans `analysis\pister_plantage.txt`.
   **Sans adresse, on n'en parle pas.**
4. **Les gains réels de 2007** : l'argent (aujourd'hui 300 G + 100 G par cran,
   **règle de portage**), la montée de grade (aujourd'hui un cran tous les dix
   battus), le lot des tournois (2 000 G / 10 000 G). Tout cela est dans les
   323 fonctions : **le lire et remplacer nos règles**.
5. Les **objets et emblèmes gagnés** au combat (`npc_tbl+0x18` et `+0x48`, deux
   listes de 24) ; la **variante de couleur** d'un objet.
6. Le **tableau de tournoi** dessiné (planches `tnt`/`tnto`, sous-état `0x55`).
7. Les **vingt-deux titres `shogo`** : l'ordre est inconnu, il se lit dans les
   données de 2007.
8. La colonne **« dan »** de la liste des joueurs.
9. Hors de portée, à dire et à ne pas entreprendre : les **classements réseau**.

---

## 5. LE PROTOCOLE AUTONOME — automatiser tout ce qui peut l'être

### 5.1 La boucle, à chaque tâche

    lire le code (.origine)  ->  ecrire  ->  py -3 tools\gen_apm_stub.py
      ->  py -3 tools\controle_quest.py --tout   ->  journaliser
      ->  tache suivante, sans s'arreter

**Ne jamais filtrer la sortie de compilation** (pas de `| head`, pas de `2>&1`
sur MinGW) : `-Wall -Wextra` vivent **dans `gen_apm_stub.py`**, pas dans une
ligne gcc tapée à la main (sans le PATH MinGW, gcc meurt en silence et on lit
le code de retour de `head`).

### 5.2 Les trois outils d'automatisation à écrire (s'ils n'existent pas)

1. **`tools\controle_quest.py`** — *tout ce qui se vérifie SANS lancer le jeu*.
   Compile le module, patche une DLL de contrôle, puis **mesure dans le binaire
   produit** : les octets attendus à chaque site patché, les 492 libellés
   présents, `npc_tbl.bin` (taille, gros-boutisme, un enregistrement témoin),
   `quest_objets.bin` (en-tête `QOBJ`, nombre, prix non nuls), la musique
   copiée, les planches `que/qwin/tnt/tnto/qdan` déclarées, la disposition de
   la greffe sans recouvrement. **Code de sortie non nul au premier défaut**,
   rapport dans `analysis\controle_quest.txt`. Lanceur `tools\controle_quest.cmd`.
2. **`tools\sonde_quest.py`** — *le jeu mené tout seul, sans clavier*. Calquée
   sur `tools\sonde_decor.py`, qui fait déjà exactement cela pour un décor :
   elle lance `vfes.exe`, joue un scénario d'appuis (`apm_entrees.txt`, relu à
   chaud par notre stub toutes les 250 ms — format dans `tools\scenarios\*.txt`),
   pose au besoin des points d'arrêt (`tools\instrument.py`), **capture à heures
   fixes** (`tools\capture_fenetre.py`), relit `quest_journal.txt`, et rend un
   rapport + les PNG dans `analysis\sonde\`. Un scénario par écran :
   création de données, carte, lieu, rencontre, combat, après-combat, boutique,
   tournoi, emblèmes. **Le scénario manuel est sauvé avant et remis après.**
3. **`tools\regression.py`** — enchaîne `verifier_lanceurs.py --sans-patch`,
   `controle_quest.py --tout`, et compare la DLL produite à l'empreinte du
   dernier état validé, correctif par correctif. C'est le filet qui permet de
   toucher au patcheur sans rien défaire.

### 5.3 Ce qui exige Frédéric, et comment le lui demander

Un essai à l'écran ne se demande **que** quand le code a été lu et qu'il ne
tranche pas. Alors : **un seul message**, avec la liste complète de ce qu'un
unique lancement permettrait de trancher, **le lanceur `.cmd` prêt**, et ce
qu'il faut regarder. Entre-temps, l'agent continue les tâches qui n'en
dépendent pas. **Ses observations priment sur toute théorie** : s'il dit qu'il
l'a vu marcher, la théorie est fausse.

Toutes les captures produites lui sont **montrées, sans verdict** : c'est lui
qui tranche.

---

## 6. Les pièges déjà payés — ne pas les repayer

* **Vérifier l'encodage AVANT d'ouvrir un fichier en écriture** :
  `texte.encode('ascii')` d'abord. Un `«` dans un en-tête a **vidé
  `tools\quest.cmd`** (0 octet).
* **Grep le nom d'une variable globale avant de la déclarer** (collision
  `g_quest_phase`). Deux `static int` de même nom en C = **une** variable, et
  `-Wall` se tait.
* **Un détour de 5 octets ne doit rien avaler.**
* **Ne jamais recycler un emplacement « libre »** sans le vérifier : `trm`
  était TERMINAL, réparé et validé, et le recycler l'a cassé.
* **Ajouter, jamais remplacer** : dès que « ça marche », c'est une recette ;
  on construit à côté.
* **Recopier tout l'enregistrement** quand on clone une entrée de table.
* Les **backticks** sont mangés par bash dans une chaîne double-quotée :
  écrire les scripts Python **dans des fichiers**.
* **`py -3`**, jamais `python`.
* Écran à **250 %** : vérifier le premier plan avant une capture.

---

## 7. Rendu de séance

1. `REPRISE.md` : une entrée numérotée **(80)**, datée, qui dit ce qui a été
   **vu**, ce qui a été **écrit sans être vu**, et ce qui **n'est pas fait**.
2. `analysis\mode_quest.md` et `analysis\menu_console.md` : les sections
   correspondantes.
3. Une **fiche mémoire** par fait durable et non dérivable du code.
4. Un tableau final en trois colonnes : **porté et vu à l'écran** / **porté,
   pas encore vu** / **pas fait**. C'est ce qu'il réclame quand il demande où
   en est le portage.
