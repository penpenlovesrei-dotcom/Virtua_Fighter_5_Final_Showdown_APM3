# Prompt de reprise — VF5RE / mode Quest, séance du 2026-10-20

Colle ce texte au début d'une nouvelle session.

---

## Le contexte

Rétro-ingénierie de **Virtua Fighter 5 Final Showdown, build arcade APM3**
(SEGA ALLS), dans `C:\Users\frede\Desktop\VF5RE`. **Réponds en français.**

Le moteur est `runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll` (base
`0x180000000`), chargé par `vfes.exe` (base `0x140000000`). On **analyse
toujours le `.origine`**, on **patche toujours par `tools/patch_moteur.py`**,
et on lance par un double-clic sur un `.cmd`.

Le mode Quest est une **greffe** : `tools/quest_runtime.c`, compilé dans
`apm.dll` par `tools/gen_apm_stub.py`. Le portage se lit dans
`analysis/mode_quest.md` (**7 981 lignes, §1 à §37**). La référence est
**VF5 Xbox 360 de 2007** : `extracted/X360_VF5/vf5_x360.img`, base
`0x82000000`, son média 2D dans
`C:\Users\frede\Desktop\VF5 FS DECOMP\X360_VF5\media`.

## Les règles de travail, non négociables

- **Aucune supposition. On lit le CODE, on décompile, on mesure.** Les
  observations de Frédéric à l'écran priment sur toute déduction.
- **Ne pas enchaîner les essais à l'écran à la place d'une lecture.** C'est
  la faute qui a coûté le plus cher cette séance (§37.26) : cinq essais de
  dessin de sprite, alors qu'une seule décompilation montrait que le modèle
  copié était le mauvais.
- **Pas de sous-agents.** Tout doit être double-cliquable (`.cmd`).
- **Ne jamais patcher pendant que `vfes.exe` tourne** (`tasklist` avant).
- **Ne jamais lancer `tools/verifier_lanceurs.py` pendant une séance.**
- **Ne jamais écrire directement un fichier du dépôt** : écrire à côté, puis
  `os.replace`.
- **Après chaque patch, relire les sites dans la DLL PRODUITE**, au
  désassembleur. Jamais dans le script qui les écrit.
- Les `.cmd` du dépôt sont en **ASCII pur et CRLF**.
- Réponses courtes. Dire ce qui est **mesuré** et ce qui ne l'est pas.

---

# LA BOUCLE AUTOMATIQUE

    py -3 tools/essai_menu.py pas b b v

**DEUX bas, pas un** — le prompt précédent se trompait. OFFLINE VERSUS (1)
n'est pas grisée ; seules ONLINE VERSUS (2) et SCOREBOARDS (6) le sont. Un
seul BAS tombe donc sur OFFLINE VERSUS.

Timings MESURÉS le 2026-10-08, ne pas les réinventer : deux START à 18 000 et
24 000 ms tenus 400 ms ; navigation dès 30 000 ms, un pas toutes les 1 500 ms
tenu 300 ms. Captures dans `analysis/essai_pas_tNN.png`. Le clavier est rendu
à la fin.

Lanceur de référence : **`tools\questV2.cmd`** (jamais `quest.cmd`, qui est
une régression). `essai_menu.py` relance `vfes.exe` seul — les patches et les
bases sont déjà sur le disque.

---

# CE QUI A ÉTÉ FAIT CETTE SÉANCE

## 1. La cause du décalage de tout l'écran, trouvée dans le code (§37)

`FUN_180029000`, le constructeur du descripteur de calque AET, posait
l'espace de résolution à **9 (1280×768)** en dur, alors que les planches du
Quest sont en **1280×720**. Le moteur convertissait donc 768 → 720 et
rétrécissait tout de 0,9375 : un `y` de 720 sortait à 1012 px sur 1080
(mesuré : 1014), d'où la bande en bas.

**Corrigé** par `quest_creer_espace` (refait `0x180171F40` en écrivant
l'espace en `+0x38` du descripteur). Bande : **66 px → 8 px**.

Et le texte a son espace aussi : `0x18019B800(desc, {x,y,l,h}, 9)` range son
troisième argument en `desc+0x2C`. Passé à **13**, le recadrage
`y -= (768 − 720)` de `FUN_18016AF60` ne se déclenche plus.

**Plus aucun objet du Quest ne vit en cible 9** : on a déclaré 1280×720 à
notre planche importée `aet_qc_cmn` (§37.8), et le badge y a été déplacé.

## 2. Les ancres, confirmées par le code de 2007 (§37.11)

`FUN_82308B78(..., 0x423, ..., "<nom d'ancre>")` est l'API par laquelle 2007
place **chaque** texte de la carte. Les sept noms employés sont exactement
ceux de `player_info_win_1p`, et exactement les nôtres.

| ancre | position (1280×720) | |
|---|---|---|
| `p_ring_name_lt` | (275, 435) | le nom, **taille 24** |
| `p_player_info_01_lt` | (322, 472) | W / L |
| `p_player_info_02_lt` | (322, 502) | Win ratio |
| `p_dan_point_c` | (600, 448) | le badge, centré |
| `p_gold_win_172x50_lt` | (805, 489) | l'argent, **aligné à droite** |
| `p_gen_plate_c` | (288, 499) | la plaque ronde |
| `p_chara_face_c` | (727, 479) | le portrait |

**Et `aet_n_que`, la planche de la carte, a ses PROPRES repères à la racine**
(`p_name_lt` 279/435, `p_txt_01_lt` 323/473, `p_gen_c`, `p_dan_c`,
`p_emb_lt` 610/476).

## 3. Ce qui est posé et vérifié à l'écran

- le **titre Quest** : c'était une animation d'entrée (son cadre descend de
  −30 à 50) ; joué de `sta_s` à `sta_e`, il est à sa place ;
- le **portrait** : `chara_face_player`, marqueurs par code (`aki`, `pai`…
  et `<code>_end`) — **dix-sept, donc ni Jean ni Taka-Arashi** ;
- la **plaque ronde** `gen_base` : celle de FS est une composition **VIDE** ;
  importée de 2007 (`bases_2d.py --ajouter qccmn`, planche 533, scène 695) ;
- le **badge**, le nom, W/L, le ratio, l'argent : tous sur leurs ancres.

## 4. L'outil neuf

`tools/arbre_aet.py` déplie une composition AET, récursivement, avec la
position absolue de chaque élément. `tools/textures_2007.py` sort les
textures d'un jeu de sprites de 2007 en PNG.

---

# LES PIÈGES DE LA SÉANCE

1. **Les accents graves dans `py -3 -c "…"` lancé par bash sont des
   substitutions de commande** : tout ce qui est entre deux `` ` `` dispa­raît
   du commentaire écrit. Ça a frappé **trois fois**. Écrire le script avec
   l'outil Write, puis `py -3 -I <chemin>`.
2. **Un témoin posé à deux rangs a fait planter le jeu** (violation
   d'accès). Un essai qui tue le jeu coûte une passe et un rétablissement.
3. **Mesurer un objet gris sur un panneau gris ne donne rien** : la loi de
   projection obtenue avait une pente de 1,11, sans aucun sens physique.
4. **Déclarer 768 sur une planche de 720 ne change rien** (le résultat était
   déjà 9 par défaut) ; déclarer **720 sur une planche de 768 change tout**.
   Un essai qui ne distingue pas deux hypothèses ne mesure rien.

---

# CE QUI RESTE, dans l'ordre

## 1. Les deux pavés « Main Costume / Type A »

**L'image est trouvée** : `COL_ICO_MAIN_1_E` à `_4_E` et `COL_ICO_SUB_1_E`,
dans `spr_c_cmn` — **la planche commune de Final Showdown, en anglais**,
rien à importer. `spr_db.bin` donne leurs `info` : `0x1000F`, `0x10011`,
`0x10013`, `0x10015`, `0x1001B`.

**Ce qui est prouvé** (§37.19 à §37.26) : le SPRSET du jeu 1 est **prêt**
(drapeau `+0xB8` = 1, mesuré), la résolution `0x18018C610(base, 55095)` rend
bien `0x1000F`, et `0x180187C00` est le poseur qui résout (type `+0x00` = 0).

**Ce qui bloque** : le descripteur d'un sprite porte **une MATRICE** à partir
de `+0x60`, pas un couple position/taille. Le modèle à copier est
**`FUN_180023930`** (module AET), pas `0x180187B10` (qui construit un quad de
type 2, aux champs disposés autrement).

**La conclusion de §37.26, et c'est la piste à suivre** : s'il faut bâtir une
matrice de calque pour dessiner un sprite, **autant poser un calque**. Le
vrai travail est donc d'**ajouter une composition** qui dessine
`COL_ICO_MAIN_n` à une planche que nous contrôlons — `aet_qc_cmn` est
importée et modifiable.

En attendant, la greffe écrit les textes « Main Costume » / « Type A » aux
positions mesurées sur la capture de 2007 (centrés en x 891, y 429 et 446).
Les libellés de 2007 sont **596** (Main Costume), **597** (Sub Costume) et
**809** (Type A) — aucun des trois n'est dans notre import de 492 textes.

## 2. Le cadre de la monnaie, et les deux fenêtres du bas

**2007 n'a PAS de fenêtre pour l'argent** : `FUN_82308C90` résout
`p_gold_win_172x50_lt`, demande le libellé 999 (`%dG`) et écrit le texte,
point. Le cadre gris de la capture vient d'ailleurs — à chercher.

Les deux fenêtres du bas : la grande porte le libellé **128** (« Home: Adjust
various settings… »), **déjà importé** (notre 23143) ; la barre des commandes
ressemble à `sousa_win`, composition racine de `aet_q_cmn`.

## 3. Les huit libellés 641-648

Les noms des huit tournois officiels, absents de notre import : ils
s'afficheront vides.

## 4. Mettre à jour le mode dojo avec ce qu'on a appris de 2007

Le plus gros, pas commencé. **Commencer par demander à Frédéric ce que
« mettre à jour le dojo » doit donner à l'écran** — c'est une question pour
lui, pas une déduction.

---

# L'ÉTAT DU DÉPÔT

`apm.dll` compile, bases 2D **conformes**, `vfes.exe` arrêté.
`quest_sprite` est écrite et complète dans `quest_runtime.c`, son appel sous
`#if 0` avec renvoi au §37.26. Trois sondes restent en place (pointeurs du
contexte 2D, résolution d'un sprite, drapeau du SPRSET) : une ligne de
journal chacune.
