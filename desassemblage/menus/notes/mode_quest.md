# Le mode Quest de VF5 (Xbox 360, 2007) : ce qu'il est, et ce que coûterait son portage vers FS

Étape 1 du chantier, demandée par Frédéric le 2026-09-11 : « lire le code du
mode Quest et le format de ses tables, puis donner une estimation chiffrée ».
Tout ce qui suit est **mesuré** dans l'exécutable et les données de la
version Xbox 360 (`VF5 FS DECOMP\X360_VF5`, base ver.C). Rien n'est supposé ;
ce qui reste à mesurer est dit comme tel (§7).

---

## 1. Rendre le code lisible

| étape | outil | résultat |
|---|---|---|
| déchiffrer `default.xex` | `tools/xex.py` | AES-128-CBC (clé commerciale publique, celle de Xenia), compression 1 « basique » : **image PE PowerPC gros-boutien de 15,7 Mo**, base `0x82000000`, 5 Mo de code |
| importer dans Ghidra | projet `ghidra/vf5x360_2007` | binaire brut, `PowerPC:BE:64:A2ALT-32addr`, 13 884 fonctions créées depuis `.pdata` (`tools/ghidra/PdataX360.java`) avant l'analyse |
| rendre le C lisible | `tools/ghidra/SauvegardesX360.java` | chaque fonction commence par `mflr r12 ; bl __savegprlr_N` et finit par `b __restgprlr_N` ; Ghidra croyait ces routines sans retour et coupait tout. Un « call fixup » neutre, ajouté **au programme** (SpecExtension), sur les 32 entrées `0x825FFA10`-`0x825FFA4C` et `0x825FFA60`-`0x825FFA9C` |
| décompiler | `tools/decomp.py --gen x360 <adresses>` | 238 + 206 + 15 fonctions décompilées sans un échec (`analysis/quest/*.c`, non publiés) |
| mesurer | `tools/quest_x360.py` | classes par le RTTI, fonctions par `.pdata`, graphe des `bl` et des `b` de fin, code propre à un ensemble |

---

## 2. Le mode dans la machine à états

La Xbox 360 a **124 sous-états** (FS APM3 : 55) et bien plus de modes. La
table des modes est en `0x8201C848` (enregistrements de 0x80 : identifiant,
entrée, milieu, sortie, liste des sous-états terminée par `0x7C`) ; celle des
sous-états en `0x8201CC90` (pas 0x14 : identifiant, drapeau, entrée, milieu,
sortie).

**Le Quest est le mode 0x13** — entrée `0x823002D8` (charge `npc_tbl.bin`),
sortie `0x82300360` — avec neuf sous-états :

| sous-état | entrée | milieu | sortie | rôle lu |
|---|---|---|---|---|
| 0x51 | `0x82300410` | `0x823004C8` | `0x82300618` | accueil du mode |
| 0x52-0x54 | `0x823006xx` | — | `0x823006xx` | transitions carte / salle |
| 0x55 | `0x82319B58` | — | `0x82319B90` | **tournoi** (`QUEST_TOURNAMENT`) |
| 0x56 | `0x82320DB0` | `0x8231FAB8` | — | préparation du combat |
| **0x57** | **`0x82320E08`** | `0x8231FEB8` | `0x82320F08` | **combat** (`QUEST_VS`) |
| 0x58 | `0x82300738` | `0x82300770` | `0x823007A8` | après le combat |
| 0x59 | `0x822FCBE0` (partagé) | `0x823007D0` | — | sortie vers le menu |

**Le combat passe par le circuit ordinaire du jeu.** `QUEST_VS` prépare les
deux fiches de joueur (`0x8218ABE8`), crée la tâche de combat nommée
`QUEST_VS` (`0x821E23B0`, la même fonction que les autres modes), et inscrit
deux rappels : événement 9 → `0x82320A68`, qui réécrit les statistiques du
rival (`0x8230DB40`) ; événement 0xF → `0x8231FAE0`. Le Quest ne touche donc
pas au combat : il fournit un adversaire et récupère un résultat.

---

## 3. Les 27 classes, et le volume de code

Toutes absentes de FS (comparaison au RTTI d'APM3, 429 classes) :

- **Quest** : `QuestAet` (le gestionnaire d'affichage, singleton `0x82ACB1F0`),
  `TaskQuestWelcome`, `TaskQuestHomeMenu`, `TaskQuestMap`, `TaskQuestTenpo`
  (la salle), `TaskQuestPlayerList`, `TaskQuestStatus`, `TaskQuestOption`,
  `TaskQuestEmblemList`, `TaskQuestCompleteEffects` ;
- **tournois** : `TaskTournament`, `…Announce`, `…Audience`, `…Entry`,
  `…List`, `…MatchInfo`, `…MessageInfo`, `…Opening`, `…ResultInfo` ;
- **récompenses** : `TaskItemShop`, `TaskNewItemList`, `TaskNewEmblemList`,
  `TaskEmblemEdit`, `TaskGameRank`, `TaskGameItemFight`,
  `TaskRankingUpdate`, `TaskLiveRankingUpdate`.

FS n'a d'approchant que le License Challenge (`CLicenceChallengeData`,
`TaskMenuArcadeLicenceChallenge`), `TaskRanking` et `TaskSelItemMenu`.

| mesure (`quest_x360.py`) | valeur |
|---|---|
| code **propre** au mode : méthodes des 27 classes + mode 0x13 et ses sous-états + rappels du combat + tout ce qu'eux seuls appellent | **323 fonctions, 108 924 octets, ~27 200 instructions PowerPC** |
| dont les seules classes | 272 fonctions, 97 564 octets |
| fonctions **partagées** du moteur que ce code appelle | **179** (37 884 octets) : interface AET, textes, fiches joueur, création de tâches, fichiers, son |

Le code occupe presque d'un bloc `0x82300000`-`0x82321200` (dont les options
en `0x82301000`-`0x82302200`, qui n'en sont pas). `.pdata` ne liste pas les
fonctions feuilles (le singleton `0x82308480` n'y est pas) : le compte est un
minorant de quelques fonctions.

---

## 4. Les données

### Les rivaux : `npc_tbl.bin`

Lu par `0x8230DC78` : **1 000 fiches de 0x90 octets** (144 000 = `0x23280`,
le premier décalage de l'en-tête), chacune avec trois pointeurs relatifs
relogés au chargement. La recopie vers une fiche joueur de 0xF8 octets
(`0x8230DDF0`) donne la disposition :

| fiche | taille | recopié en | lu |
|---|---|---|---|
| +0x00 +0x04 +0x08 | 3 pointeurs | +0x00 / +0x1F / +0x47 | **nom**, réplique ligne 1, ligne 2 (UTF-8) |
| +0x0C | u16 | +0x70 | à identifier |
| +0x0E | u8 | +0x72 | à identifier |
| +0x10 | u32 | +0x74 | à identifier |
| +0x14..+0x16 | 3 × u8 | +0x78..+0x7A | à identifier |
| +0x18 | **24 × u16** | +0x7C | objets de personnalisation, premier jeu |
| +0x48 | **24 × u16** | +0xAC | objets, second jeu |
| +0x78 | u32 & 0x3FF | +0xDC | à identifier |
| +0x88..+0x8A | 3 × u8 | +0xE0..+0xE2 | +0x88 sert de filtre (bit dans un masque) |
| +0x8C | u16 | +0xE4 | à identifier |

Plus un état VIVANT de 8 octets par rival (tables `0x82ACB930` et
`0x82ACD874`), sauvé et relu par `0x8230D880` / `0x8230D9B0` (200 tours de 5
rivaux) : ce que la sauvegarde du Quest retient de chaque rival.

**Langues** : racine en japonais, `lang/{en,fr,ge,it,sp}/npc_tbl.bin` —
**le français existe** (« steven jul — Je serai / le meilleur »), comme tous
les textes du mode (`string_array.bin`, 5 854 chaînes en anglais).

### Les salles

Les calques de la carte les nomment (`0x82309868`) : `zoom_swn`, `zoom_sws`,
`zoom_swr` (trois SEGA World), `zoom_csd`, `zoom_csb` (deux Club SEGA),
`zoom_sac`, `zoom_sae` (deux SEGA Arena), `zoom_dom_01`, `zoom_dom_02` (le
dôme des tournois officiels) — **neuf lieux**.

### L'interface

| planche | contenu | lue par |
|---|---|---|
| `aet_n_que.bin` + `spr_n_que.farc` (8,5 Mo) | carte et salles : 2 scènes, 66 compositions, 435 images ; 25 textures DXT5/RGBA8/RGB8 | `aet.py` et `txp.py` **tels quels** (même format qu'APM3, 1280 × 720, non tuilé) |
| `aet_n_qwin.bin` + `spr_n_qwin.farc` | les fenêtres (statut, magasin, salle…) : 124 compositions, 262 images | idem |
| `aet_n_tnt.bin`, `aet_n_tnto.bin` | tournois : 18 + 23 compositions | idem |
| `spr_c_emb*.farc` | emblèmes | idem |

La carte a été rendue en image (`analysis/quest/que_tex0_1024.png`) :
SEGA World, Club SEGA, Arena, maisons, flèches — lisible sans conversion.

### Les IA des rivaux

| version | fichiers | format |
|---|---|---|
| VF5 Xbox 360 | **280** `rom/rob_ai/ai_data_600..1369.bin` | **binaire**, 56 472 octets chacun (lus par `0x82250588`) |
| VF5 ver.B (Lindbergh) | mêmes noms, même taille | binaire |
| VF5 R (Lindbergh) | **326** `ai_data_628..5000.txt` | **texte** `#AIFTEXT` |
| FS APM3 | **26** `ai_data_2500..2720.txt` | texte `#AIFTEXT` |

Le texte de R et celui de FS ont **173 clés communes** sur 176 et 180 (FS
ajoute `ai_cancel.*` et `ai_hinp.*`, retire trois compteurs `ai_intr`). Les
IA de 2007 et de R ont **117 numéros communs** : de quoi établir la
correspondance binaire → texte.

### Les objets portés par les rivaux

Akira : 401 entrées dans la table de 2007, 1 004 dans celle de FS. Les objets
de 2007 sont rangés par numéro (`akiitm000`..`akiitm291`), mais sur 45 noms
d'objets lus dans ces fichiers, **13 seulement** se retrouvent tels quels dans
la liste de FS (`aki_itm.csv`) : FS a renommé ou réorganisé une partie de la
garde-robe.

---

## 5. Ce que le portage demande

FS n'a **aucune** ligne du Quest. Le porter, c'est :

1. **réécrire** ~27 200 instructions de logique (323 fonctions) contre le
   moteur de FS ;
2. **retrouver dans FS** les 179 services partagés qu'elles appellent (même
   lignée de moteur, RTTI des deux côtés pour s'ancrer : c'est le travail de
   correspondance déjà fait pour les tables de décors) ;
3. **ajouter un mode** à la machine de FS (10 modes, 55 sous-états) : un
   mode et neuf sous-états, par extension de table comme pour les décors ;
4. **convertir les données** : rivaux (1 000, textes en français compris),
   IA (280 binaires → texte), objets (correspondance à établir) ;
5. **poser l'interface** : planches et textures lisibles telles quelles, à
   déclarer dans les bases 2D de FS.

Hébergement du code neuf : la bibliothèque de substitution `apm.dll` (que
nous compilons déjà, `gen_apm_stub.py`) est chargée par le jeu — du C
compilé, plutôt que des milliers d'octets de stubs dans la greffe.

---

## 6. Estimation

En **séances** comparables à celles des décors :

| étape | contenu | séances |
|---|---|---:|
| 1. données | rivaux → format FS ; IA binaires → texte, **essai d'une IA de rival dans FS** ; correspondance des objets | 2 |
| 2. combat contre un rival | le VS de FS avec l'adversaire d'une fiche (personnage, costume, IA, nom), résultat rendu → **premier jalon jouable** (choix du rival dans un menu simple) | 2 |
| 3. écrans du Quest | carte, salle, liste des joueurs, statut, options, emblèmes, accueil ; le gestionnaire `QuestAet` | 4 |
| 4. tournois | les neuf classes `TaskTournament*` | 3 |
| 5. récompenses et sauvegarde | magasin, nouveaux objets et emblèmes, rangs, or, état des 1 000 rivaux | 2 |
| **total** | | **≈ 13** (fourchette 10-16) |

Un « Quest minimal » jouable (étapes 1 et 2) : **≈ 4 séances**.

---

## 7. Ce qui peut faire bouger l'estimation

- **L'IA** : le moteur de FS acceptera-t-il une IA de 2007 convertie ? Les
  numéros de coups qu'elle cite (`ai_atak.far.km0.N.index`) visent les tables
  de commandes de SON époque ; si FS les a renumérotées, il faut une table de
  passage par personnage. Un seul essai à la sonde tranche (étape 1).
- **Les objets** : 13 noms sur 45 retrouvés tels quels pour Akira. Sans
  correspondance complète, un rival porte l'équivalent FS le plus proche ou
  son costume par défaut.
- **Les 179 services** : s'ils se retrouvent dans FS aussi facilement que les
  tables de décors, l'étape 3 raccourcit ; sinon elle s'allonge.
- Les champs de la fiche marqués « à identifier » (§4) se lisent dans le code
  qui les consomme ; aucun n'est bloquant pour l'estimation.

---

## 8. Étape 3 — les écrans : les planches du Quest sont DANS les bases de FS (2026-09-11)

Premier morceau de l'étape 3, celui qui conditionne tout le reste : le moteur
de FS ne peut afficher une planche que si elle existe dans ses deux bases 2D.

### Ce qui bloquait, et qui ne se voyait pas

Les bases ne sont pas sur le disque : le binaire porte une **archive FArC
embarquée** en `0x1804137F0` (`mot_db`, `obj_db`, `tex_db`, `spr_db`,
`aet_db`, `rob_mot_tbl`, et le décor `tst`), et le `.par` en porte une
seconde copie. Le moteur consulte l'archive embarquée, puis le `.par`, puis le
disque. Il a donc fallu **deux** gestes, le second trouvé à la sonde (le
moteur lisait bien nos planches sur le disque, mais jamais nos bases) :

1. `patch_moteur --bases-2d-libres` masque un octet du nom de `spr_db.bin`
   (`0x18041384A`) et de `aet_db.bin` (`0x180413861`) dans l'archive
   embarquée — le même geste que `--obj-db-libre` ;
2. `bases_2d.py` masque les deux noms dans l'index du `.par`.

### Les deux formats, et ce qui les relie

    aet_db   en-tete {nb planches, table, nb scenes, table}
             planche 0x14 : {id, nom, fichier, rang, id du jeu de sprites}
             scene   0x0C : {id, nom, (rang de la planche << 16) | rang}
    spr_db   planche 0x10 : {id, nom, fichier, rang}
             sprite  0x0C : {id, nom, info} ; info = (rang << 16) | rang du
                            sprite, quartet de poids fort 1 = TEXTURE

Une **vidéo** d'une planche AET nomme son sprite ET le désigne par un
identifiant global. Le nom court du sprite dans son jeu (`EFF_PTCL`) devient
`N_QUE_EFF_PTCL` dans la vidéo et `SPR_N_QUE_EFF_PTCL` dans la base : c'est
par ce nom qu'on renumérote.

### Ce qui est posé

`tools/bases_2d.py --ajouter que qwin tnt tnto` repart des bases du binaire
d'origine, ajoute nos planches à la suite (rien de l'original n'est déplacé),
copie les fichiers dans `rom/2d/` et réécrit les identifiants de sprite dans
les copies :

| planche | id AET | scènes | jeu de sprites | contenu |
|---|---:|---|---:|---|
| `AET_N_QUE` | 526 | MAIN, MAIN_VGA | 623 (426 sprites, 25 textures) | la carte et les salles |
| `AET_N_QWIN` | 527 | MAIN | 624 (137 + 28) | les fenêtres |
| `AET_N_TNT` | 528 | MAIN | 625 (25 + 3) | les tournois |
| `AET_N_TNTO` | 529 | MAIN | 626 (77 + 7) | les tableaux de tournoi |

1 084 identifiants de sprite renumérotés, aucun laissé sans correspondance.
`--controle` relit les bases posées : l'original conservé entrée par entrée,
chaque vidéo visant un sprite existant, chaque fichier présent.

**Vu à la sonde** : le moteur ouvre bien `rom/2d/aet_db.bin` et
`rom/2d/spr_db.bin` (les nôtres), et le jeu est intact — écran de chargement,
polices, icônes, jauges et messages de combat (`analysis/quest/
bases_2d_avant_vol.png`). C'est la preuve que nos bases remplacent les
siennes sans rien casser.

### Le chemin d'affichage, repéré

    0x180027600            charge `aet_db`
    0x180029C20(id)        charge la PLANCHE d'identifiant `id` (cherche son
                           fichier dans la base, puis 0x180027740)
    0x180171E90(ctx, rang, id de scene, nom du calque, 0xF, 0x20000)
                           cree l'objet AET -- un objet VIVANT, rendu chaque
                           trame par AetMgr (voir `texte_2d.md` §2 et §7)

Il reste à appeler ces trois-là depuis du code à nous, au bon moment : c'est
le morceau suivant (le code du Quest logera dans `apm.dll`, que le jeu charge
déjà et qui reçoit la main à chaque image par `Core_execute`).

### Le code du Quest a sa place : `apm.dll`

Le jeu charge déjà notre `apm.dll` (`tools/gen_apm_stub.py`) et lui donne la
main **à chaque image** par `Core_execute`. Le Quest y logera : du C, compilé
par MinGW, qui appelle le moteur par pointeurs résolus sur SA base
(`GetModuleHandleA`), ce qui survit au rebasage — plutôt que des milliers
d'octets d'assembleur dans la greffe.

`tools/quest_runtime.c` est le premier jet, **inerte par défaut** : il ne fait
rien tant que le scénario d'entrées ne porte pas une ligne `quest = <secondes>`
(`tools/sonde_decor.py --quest 5` l'écrit le temps d'un essai).

### Ce que le premier essai a mesuré

1. **Nos planches sont dans la base VIVANTE du moteur.** Le module lit le
   vecteur de la base AET (`0x18066B738`, dichotomie de `0x1800248D0`, entrées
   de 0x58 octets) : **504 planches, identifiants 0 à 529** — les quatre
   nôtres comprises. La chaîne bases → moteur est donc bouclée.
2. **La base AET n'existe pas à tout moment** : pendant un combat, le global
   vaut 0 (le premier essai est mort là, dans la dichotomie). Le module
   attend désormais qu'elle soit là.
3. **Le chargement d'une planche plante encore** : `0x180029C20(526)` va
   jusqu'à `0x180027740`, qui meurt en `0x180027852` sur `mov rax,[rcx]` puis
   un appel virtuel — le pointeur choisi juste avant (`cmove rcx, rax`,
   `0x18002783D`) est nul. Autrement dit **il manque l'inscription de la
   planche dans le gestionnaire** (`0x18066B750`) : le moteur s'attend à y
   trouver une entrée préparée. C'est le maillon suivant à tracer
   (`0x1800268A0`, appelée par le chargeur de la base, est la piste : c'est
   elle qui prépare les entrées à partir du fichier).

Rien de tout cela ne change le jeu tant que la ligne `quest` n'est pas dans le
scénario : sans elle, `apm.dll` se comporte exactement comme avant.

### LA CARTE DU QUEST S'AFFICHE DANS FS (2026-09-11, vu à l'écran)

Frédéric l'a vue le premier, pendant les essais : « si, j'ai vu la map du
mode quest plusieurs fois s'afficher ». Capture :
`analysis/sonde/qs3.png` — l'île, les SEGA World, le Club SEGA, l'Arena, la
maison, le ballon, et le bandeau « Quest ».

**La recette, dans l'ordre, et chaque maillon a coûté un plantage :**

1. **Appeler le moteur depuis SON fil.** `Core_execute` (le battement de la
   carte) tourne sur un fil, et `Input_isOn` est appelée par le MOTEUR sur un
   autre (mesuré : 17188 contre 20792). Le Quest est donc piloté depuis
   `Input_isOn`, une fois par image au plus.
2. **Attendre les quatre globaux** : base AET `0x18066B738`, son gestionnaire
   `0x18066B750`, base des sprites `0x180719908`, son gestionnaire
   `0x180719900`. Pendant un combat, les deux premiers valent 0 — le premier
   essai est mort dans leur dichotomie.
3. **DIMENSIONNER le gestionnaire de sprites** : `0x180187AB0()` lui donne le
   nombre de planches de la base (`(fin - début) / 0x58`). Sans cela, le
   chargeur cherche la planche dans sa table, ne la trouve pas et reçoit un
   **pointeur nul** (`0x18018E5A0` → `0x18018DFB0`, `mov eax,[rcx+0x20]`) :
   le jeu meurt, même avec une planche D'ORIGINE — ce qui a disculpé nos
   données.
4. **Charger**, comme FS le fait (`0x18006B880`) : `0x180187C50(623)` le jeu
   de sprites, puis `0x180029C20(526)` la planche ; attendre que
   `0x180187CC0` et `0x180029D40` rendent 0 (ici : **0,5 à 1,8 s**).
5. **Créer les objets AET** :
   `0x180171E90(contexte, rang, scène, calque, priorité, 0x20000)` avec
   contexte = `*(void **)0x1803FFBD0`, scène 683 (`AET_N_QUE_MAIN`), et les
   calques de la racine : `map_base`, `map_aero`, `tit`.
6. **Les refaire** toutes les cinq secondes : une composition AET a une durée
   (celle de la carte : 630 images, ~10 s) et s'éteint à la fin.

C'est `tools/quest_runtime.c`, dans `apm.dll` — inerte tant que le scénario
d'entrées ne porte pas `quest = <secondes>` (`sonde_decor.py --quest 20`).

**Ce que cela prouve** : les planches du Quest, leurs sprites et leurs
animations passent entières dans le moteur de FS, sans conversion. Ce qui
reste pour l'étape 3 : en faire un vrai écran — un mode à part (plutôt que
posé par-dessus la sélection de personnage), le curseur sur les salles, les
fenêtres (`AET_N_QWIN`), et les textes.

### Une carte NAVIGABLE (2026-09-11, meme seance)

Deux ajouts, et la carte devient un ecran :

* **les salles**. Le calque `zoom_<salle>` de la scene montre la
  PHOTOGRAPHIE de la salle choisie -- les trois SEGA World, le Club SEGA,
  l'Arena, le dome. Les neuf noms sont ceux de la planche, dans l'ordre ou
  VF5 les enumere (`0x82309868` de la version Xbox 360) :
  `zoom_swn sws swr csd csb sac sae dom_01 dom_02`.
* **la manette**. C'est `apm.dll` qui la tient : le module lit son propre
  masque de boutons (codes du joueur 1 : 4 gauche, 5 droite, 7 START) et
  calcule ses fronts. Un appui sur droite change de salle, et les calques
  sont refaits -- vu a l'ecran : trois appuis, trois salles
  (`analysis/quest/quest_navigation.png`).

`tools/sonde_decor.py --touches 40:5,43:5` envoie des boutons autres que
START le temps d'un essai : c'est ainsi que la navigation a ete eprouvee
sans clavier.

Ce qui manque encore pour que ce soit un vrai ecran : qu'il soit SEUL
(aujourd'hui la carte se pose par-dessus le menu ou la selection de
personnage), c'est-a-dire un mode a lui dans la machine a etats ; puis les
fenetres (`AET_N_QWIN`), les textes et le curseur d'arrivee.


## 9. UN VRAI ÉCRAN : le Quest est un ÉTAT DU JEU (2026-09-12)

Frédéric : « crée un vrai écran quest car tu es toujours en surimpression »,
puis « non je veux un vrai ecran », puis, sur le choix du point d'entrée,
« non conserve online et remplace leaderboards ».

C'est fait. **MENU > SCOREBOARDS ouvre la carte du Quest, le menu est
démonté, et quitter la carte rend la main au menu.** Captures :
`analysis/sonde/qa_carte.png` (la carte seule), `qc_zoom.png` (une salle),
`qe_menu.png` (le retour au menu, curseur sur SCOREBOARDS).

### 9.1 L'état employé : DATA_TEST / DATA_TEST_KOTSP_SS

Aucun état n'a été inventé, et rien n'a été pris à un écran vivant. Le mode
**DATA_TEST** (identifiant 3, quinze sous-états 21 à 35) est **entièrement
bouchonné** dans ce build : ses trois gestionnaires, et les trois de chacun
de ses quinze sous-états, sont tous `0x180029FB0` — lu dans `.origine` :

```
0x180029FB0 : b0 01 c3        mov al, 1 ; ret
```

Le Quest prend le dernier, **35 `DATA_TEST_KOTSP_SS`**. ONLINE (mode 7,
lui aussi bouchonné) n'est pas touché : c'est ce qu'il a demandé.

### 9.2 Pourquoi trois gestionnaires ne suffisaient pas

Le répartiteur `0x1800DA550` appelle, à chaque image, **le gestionnaire de la
phase courante** — 0 entrée, 1 boucle, 2 sortie — pour le mode ET pour le
sous-état. La valeur rendue est le verdict : **1 = ma phase est finie**.

Un bouchon `mov al,1 ; ret` rend donc 1 : entrée, boucle, sortie s'enchaînent
en trois trames, et le mode s'achève aussitôt. Un écran qui **tient** exige
que la phase « boucle » rende **0**.

D'où trois pointeurs repointés vers la greffe, et trois seulement :

| créneau | rôle | stub |
|---|---|---|
| mode DATA_TEST `+0x10` | boucle | `QUEST_BOUCLE` — rend l'octet `sortie` |
| sous-état 35 `+0x10` | boucle | `QUEST_BOUCLE` |
| sous-état 35 `+0x18` | sortie | `QUEST_FIN` — remet la boîte à zéro, rend 1 |

Les créneaux « entrée » gardent le bouchon d'origine : `mov al,1 ; ret` est
exactement ce qu'on y mettrait.

**Le piège du mode.** Repointer le sous-état seul ne suffit pas : dès que le
MODE a fini ses trois phases, le répartiteur force le sous-état à sa phase de
sortie (`if (500 || 51c) 518 = 2`). Il fallait donc tenir les DEUX boucles.

### 9.3 L'entrée : SCOREBOARDS, et le site a été MESURÉ

`menu_console.md` donnait pour l'entrée 5 (SCOREBOARDS) la destination
`0x1801B0120` (scène `RANKING`). Sept `call` la visent. Un point d'arrêt sur
les sept, pendant que la sonde validait SCOREBOARDS, a tranché : **un seul
passage, en `0x1801DE09A`**. Le site cité par la doc, `0x1801DCE27`, n'est
jamais atteint à la validation — c'est celui de la mise à jour de la page.

Le premier essai avait patché `0x1801DCE27` : le stub n'a **jamais** été
appelé (`espion:aller : 0 passage(s)`), et le menu se figeait, la page
RANKING ouverte. Le compteur du point d'arrêt l'a dit en une sonde.

La branche est reconnaissable, et le patcheur l'EXIGE avant d'écrire :

```
0x1801DE08E  83 f9 05           cmp  ecx, 5          <- l'entree SCOREBOARDS
0x1801DE091  75 1e              jne  ...
0x1801DE093  41 b0 01           mov  r8b, 1
0x1801DE096  33 d2              xor  edx, edx
0x1801DE098  33 c9              xor  ecx, ecx
0x1801DE09A  e8 ...             call 0x1801B0120     <- devient QUEST_ALLER
0x1801DE09F  48 8b 5c 24 30     mov  rbx, [rsp+0x30]
0x1801DE0A4  48 89 87 50060000  mov  [rdi+0x650], rax
```

### 9.4 Comment on demande un changement d'état (et pas comme je croyais)

`0x1800DA800` (`SetState`) n'a **qu'un seul site d'appel dans toute la
`.text`** : le répartiteur lui-même. Vérifié par balayage de tous les `call`
relatifs. L'appeler depuis un gestionnaire de menu aurait changé le mode en
plein milieu de sa trame, sans lui laisser sa phase de sortie — c'est-à-dire
sans démonter l'écran : la surimpression, encore.

Les écrans passent par **deux poseurs de vœu** :

```
0x1800DA9A0(mode)  ->  [0x18070C4F4] = mode ; [0x18070C500] = 1 ; [0x18070C51C] = 0
0x1800DA9C0(sous)  ->  [0x18070C510] = sous ; [0x18070C51C] = 1
```

Le menu s'en sert déjà pour l'atelier (`case 10` de `0x1801DC620`) :
`mov ecx,5 ; call 0x1800DA9A0 ; mov ecx,0x25 ; call 0x1800DA9C0`. `QUEST_ALLER`
copie cet idiome mot pour mot, avec 3 et 35, et rend 0 — l'appelant range ce
zéro dans `[rdi+0x650]`, son « sous-écran courant », où c'est la valeur
normale quand il n'y en a pas.

### 9.5 Le retour au menu : un champ, pas un appel

Quand un mode s'achève, le répartiteur va au mode inscrit en **`+0x60` de son
enregistrement**. DATA_TEST y portait **1** (`ADVERTISE`, la démonstration) ;
`--quest-ecran` y écrit **4** (`MENU`). Quitter le Quest ramène donc au menu,
sans que `apm.dll` ait un seul appel à faire.

### 9.6 La boîte aux lettres « QUESTBOX »

Deux octets partagés, dans la greffe :

| offset | qui écrit | sens |
|---|---|---|
| `+0x0C` `actif` | le moteur (`QUEST_BOUCLE`) | 1 = la phase boucle tourne |
| `+0x0D` `sortie` | `apm.dll` | 1 = je quitte |
| `+0x10` `tours` | le moteur | une trame de boucle = +1 |

`apm.dll` la trouve en cherchant les huit octets `QUESTBOX` dans la section
`.greffe` du moteur : son adresse change d'un build à l'autre (ici
`0x180EA2F40`). **Sans boîte, le module est inerte** — c'est ce qui le rend
inoffensif sur un moteur non patché.

### 9.7 Ce que l'écran fait, aujourd'hui

`tools/quest.cmd`. Dans le menu : **SCOREBOARDS**.

| touche | code | effet |
|---|---:|---|
| gauche / droite | 4 / 5 | déplacer le repère d'un lieu à l'autre (neuf) |
| Entrée (START) | 7 | entrer : la photographie du lieu |
| W (carré) | 8 | revenir à la carte, puis au menu |

Deux réglages appris à l'écran :

* **`zoom_<salle>` n'est pas une vignette** : c'est la photographie de la
  salle EN PLEIN ÉCRAN. Posée d'office, elle masquait toute la carte. Elle
  n'apparaît donc qu'à la validation.
* **on ne repose plus les calques toutes les cinq secondes** : on demande au
  moteur si la composition est finie (`0x180171070(ctx, rang)` rend 1 quand
  le rang est libre ou l'objet arrivé au bout). À l'ancienne méthode, la
  carte rejouait son animation d'entrée en plein milieu.

En partant, les quatre rangs sont **rendus** (`0x1801721D0(ctx, rang)`) :
sans cela la carte survivrait par-dessus le menu jusqu'à la fin de sa
composition (630 images, ~10 s).

### 9.9 Le curseur sur les lieux (2026-09-12, même séance)

La composition racine de la scène `MAIN` a livré le curseur : à côté des neuf
`zoom_<salle>`, elle porte neuf calques **`ic_<lieu>`** (0-77 images) —

```
ic_csd  ic_dom  ic_hom  ic_csb  ic_sac  ic_sae  ic_swn  ic_swr  ic_sws
```

— et **`map_home_txt`** (0-630). Chacun a été affiché seul et photographié :
`ic_<lieu>` pose un **anneau orange** sous un lieu de la carte et en grossit
le bâtiment ; les neuf tombent sur neuf lieux **distincts**. `map_home_txt`
n'est pas une page : c'est la légende **« HOME »** sous la maison — elle est
donc posée en permanence, avec la carte.

**Appariement vérifié** : repère sur le Club SEGA rond → la photographie est
celle du Club SEGA rond (`analysis/sonde/p1_repere.png`, `p2_photo.png`).

Deux asymétries, lues dans la planche et non supposées :

* il y a **un seul `ic_dom`** pour **deux** `zoom_dom_01`/`dom_02` : le dôme
  porte deux tournois et un seul lieu. `zoom_dom_02` reste inemployée — c'est
  la progression du Quest qui choisira, pas la carte ;
* **`ic_hom`** n'a pas de `zoom_` : la maison n'est pas une salle. Valider
  dessus ne fait rien pour l'instant et le dit au journal ; elle aura sa
  fenêtre, dans `AET_N_QWIN`.

### 9.10 Les rangs du contexte AET, et leur borne

`0x180171E90` indexe le tableau du contexte **sans aucune borne** :
`param_1 + rang*4 + 0x5C`. Écrire au-delà casserait la structure en silence.
La borne sûre a été **mesurée** : balayage des 44 sites d'appel de
`creer`/`liberer`/`fini`, avec le `mov edx, imm32` qui les précède —

| rang employé par FS | 1, 7, 15, 16, 17, 18, 19, 20, 21, 22, 23 |
|---|---|

Le Quest prend **7 à 12**, tous en deçà :

| rang | calque | priorité |
|---:|---|---:|
| 7 | `map_base` | `PRIO` |
| 8 | `map_aero` | `PRIO+1` |
| 12 | `map_home_txt` | `PRIO+2` |
| 11 | `ic_<lieu>` | `PRIO+3` |
| 9 | `tit` | `PRIO+4` |
| 10 | `zoom_<salle>` | `PRIO+5` |

### 9.11 Un piège de la sonde : deux horloges

Les captures sont datées depuis le **lancement du processus**, le scénario
d'entrées depuis le **premier appel d'entrée** du moteur : il y a plusieurs
secondes d'écart. Deux captures prises à trois secondes d'un appui ont ainsi
montré le repère de l'index *précédent*, et j'ai failli conclure que deux
`ic_*` désignaient le même lieu. **Laisser six secondes entre un appui et sa
capture**, ou lire l'ordre dans le journal `[quest]`.

### 9.13 LES MARQUEURS : on ne joue jamais une composition entière (2026-09-12)

**Validé à l'écran par Frédéric.** C'est le maillon qui manquait, et il vient
du code de 2007 — après qu'il m'eut repris : « tu supposes des choses et tu ne
t'appuies plus sur le code de la version xbox pour transcrire son
comportement. » Il avait raison ; je tâtonnais sur l'API 2D de Final Showdown
au lieu d'aller lire comment le Quest s'en sert.

#### Ce que fait la version Xbox 360

Les fenêtres du Quest sont servies par un **porte-fenêtre**, membre `+0x238`
des tâches (`TaskQuestHomeMenu`, `TaskQuestTenpo`…). Sa méthode « jouer »,
**`FUN_822E4BF0(this, phase)`**, ne joue jamais la composition entière : elle
dresse quatre paires de **noms de marqueurs** et leur drapeau, et joue la
phase demandée.

| phase | marqueurs | drapeau | rôle |
|---:|---|---|---|
| 0 | `sta_s` → `sta_e` | `0x20000` | l'ouverture, **une fois** |
| 1 | `neu_s` → `neu_e` | `0x10000` | le repos, **en boucle** |
| 2, 3 | `end_s` → `end_e` | `0x20000` | la fermeture |

La planche et le nom du calque viennent d'une **table de 59 fenêtres** en
`0x82085700`, huit octets par entrée : `{identifiant de planche, nom du
calque}`. `hall_menu_win` y est l'indice 43, `home_menu_win` le 37, tous deux
sur la planche `0x423`.

#### Les marqueurs, dans nos propres planches

Ils se lisent dans le calque (`+0x20` nombre, `+0x24` table ; huit octets par
marqueur : l'image en flottant, puis le nom) :

| calque | `sta` | `neu` | `end` |
|---|---|---|---|
| `hall_menu_win`, `home_menu_win`, `status_win`, `player_list_win`, `embsel_win` | 0-27 | 28-88 | **89-97** |
| `ic_<lieu>` | 0-16 | **17-76** | — |
| `map_base` | `sta_s` 0 | 30-629 | — |
| `tit` | 0-20 | — | — |
| `zoom_<salle>` | 0-24 | — | — |
| `shutter` | `sta_s` 0, `stop` 63, `sta_e` 120 | | |

#### Ce que cela explique, et que le tâtonnement n'aurait pas trouvé

Deux observations de Frédéric, et une seule cause :

* **« les fenêtres s'ouvrent mais se referment au bout d'une seconde
  environ »** — je jouais 0→600, donc je traversais `end` (89-97, soit
  **1,6 s**) : la fenêtre jouait sa propre fermeture. La sonde le disait déjà
  sans que je sache le lire — `0x180171070` répondait « pas fini » à la trame
  300, l'objet était bien vivant : ce n'était pas une disparition, c'était une
  **animation de fermeture** ;
* **« l'icône tourne en boucle mais avec les étapes du démarrage
  incluses »** — je bouclais 0-77 au lieu de 17-76.

#### Sur Final Showdown : la forme longue du créateur

```
0x180171F40(ctx, rang, scene, calque, position, priorite, drapeau,
            marqueur_debut, marqueur_fin)
```

Les deux derniers arguments (pile `+0x38` et `+0x40`) sont les noms de
marqueurs ; `0x180171E90` est la même fonction avec ces deux champs mis à
zéro. FS s'en sert lui-même sur huit sites, avec `cha_out_start`/`cha_out_end`
(0x18016DC64), `stg_in_start`/`stg_in_end` (0x1801745E1) et
`loop_start`/`loop_end` (0x18017468E).

`tools/quest_runtime.c` transcrit la machine : chaque rang porte son nom et sa
phase ; à la pose on joue `sta` en `0x20000`, et dès que `0x180171070` dit
l'objet fini on enchaîne `neu` en `0x10000`. Un rang dont le nom n'a pas
changé n'est **jamais** reposé — reposer empile (`0x1801721D0` ne rend que la
racine de la composition, ses enfants continuent de se dessiner : à reposer
chaque trame, la photographie d'une salle blanchissait image sur image
jusqu'à la surexposition complète) et rejoue l'ouverture.

### 9.15 Les textes : l'inventaire, relevé dans le code de 2007

`tools/quest_textes.py` → `analysis/quest/textes.md`.

**La chaîne, de bout en bout, et lue :**

* la version Xbox charge `media/lang/<lg>/string_array.bin` par
  `FUN_82322900` dans le porteur `0x82AD1C48` ; `FUN_82322820` le déplie une
  fois (les offsets deviennent des pointeurs) dans `DAT_82AD1C40` ;
* le getter est **`FUN_82322798(id)`** — borné à `0x1D9F`, avec un décalage de
  `+0x2A` sur les 42 premiers identifiants selon la manette détectée (ce sont
  les pictogrammes de boutons) ;
* le fichier est un tableau de pointeurs **32 bits gros-boutistes** vers des
  chaînes UTF-8 : **7 586 entrées**, et il existe en `en`, `fr`, `ge`, `it`,
  `sp`. Même format que le `string_array.farc` de Final Showdown, qui en a
  23 052.

L'outil balaie le `.text`, garde les `bl 0x82322798` précédés d'un
`li r3, imm`, ne retient que ceux qui vivent dans le code propre au Quest, et
résout chaque identifiant dans la table de la langue demandée :

**83 identifiants distincts, 131 sites** — et c'était un plancher bien plus bas qu'on ne croyait : voir §9.18, le balayage ne voyait pas les chargements indirects, et l'inventaire est passé à **492**. Un extrait :

| id | texte |
|---:|---|
| 540 | Quest settings |
| 544 | STATUS |
| 545 | Rivals defeated |
| 548 | Overall completion rating |
| 558 | RIVAL LIST |
| 569 | EMBLEM LIST |
| 601 | List of official tournaments |
| 614 | The following tournament has begun: |
| 149 | %s is on a %d-win streak! |

C'est un **plancher**, pas un plafond : les libellés passés par un tableau ou
une variable (les noms des mille rivaux, ceux des objets) ne sont pas dans ce
compte — ils viennent de `npc_tbl.bin` et de `chritm_tbl.farc`.

#### Le mécanisme d'affichage existe des deux côtés

Les deux moteurs ont le même : une boîte de texte reçoit un **nom**, et le
gestionnaire la dessine.

| | Xbox 360 (2007) | Final Showdown |
|---|---|---|
| poser le nom | `FUN_822C8AA0(boite, nom)` | **`FUN_180245830(boite, nom)`** |
| le fond | `FUN_822C8910(boite, langue, nom, 1)` | `FUN_1802456C0(boite, langue, nom, 2)` |
| le gestionnaire | `DAT_829C649C` | `DAT_180C41340` |
| les noms | `QUEST_HOME_EXPLAIN`, `QUEST_MAP_CONTROL`… | `MENU_EXPLAIN`, `MENU_CONTROL`, `VS_RESULT_CONTROL`, `ROB_CONTROL` |

Le nom n'est **pas** la clé du texte : c'est l'étiquette de la boîte (copiée
sur 0x20 octets en `boite+0x22`, puis chaînée dans la liste du gestionnaire).
Le contenu, lui, arrive par identifiant — `0x1801EFD10(id)` sur Final
Showdown, `FUN_82322798(id)` sur Xbox.

#### Ce qui a été tranché

Frédéric a choisi la voie 1 : **les ajouter au `string_array.farc` de Final
Showdown**, comme `bases_2d.py` a ajouté les planches — le texte devient une
donnée du jeu, et le résolveur de FS le rend par son numéro de 2007.
`tools/textes_quest.py --ajouter` les pose à la suite sans rien déplacer ;
`patch_moteur.py --textes-quest` monte la borne du getter. Le DESSIN, lui,
reste le nôtre — mais à la recette du moteur, voir §9.16.

### 9.16 LE TEXTE S'AFFICHE (2026-09-26, vu à l'écran)

Frédéric : « je confirme que les textes sont enfin visibles ».

Quatre séances l'avaient manqué. Ce qui a débloqué n'est pas une trouvaille :
c'est d'avoir **arrêté de composer** un `app::PrintGC` à la main et d'être
allé lire comment Final Showdown dessine SES propres libellés.

#### D'abord, deux pistes fermées — par la lecture, pas par l'essai

**La police (`0x180199FB0`, mode 2).** Innocente. `0x180019AB0`, qui décide si
un caractère produit un glyphe, ne consulte **aucune police** : c'est
`ch >= 0x20 && ch != 0x7F`. Une police absente ne pouvait donc pas vider la
liste en silence — et le diagnostic posé dans `apm.dll` l'a confirmé à
l'exécution, les trois polices sont résidentes :

```
police mode 0 : descripteur ...100, sprite 0000018F
police mode 1 : descripteur ...140, sprite 0000D30D
police mode 2 : descripteur ...180, sprite 0000D3DB
```

**La méthode virtuelle `desc->vtable+8`** = `0x18019ADB0`. Innocente aussi :
elle **soumet toujours** dès qu'il y a un caractère imprimable et que le
drapeau de découpe `0x200` est éteint. Elle a quand même servi — elle montre
que la commande porte en `+0x04` **l'identifiant de sprite de la police**, et
que `0x18018CA20` laisse tomber la commande *sans un mot* quand ce jeu de
sprites lui est inconnu. C'était la première voie d'échec muet trouvée dans
cette chaîne, et il faut s'en souvenir.

Au passage, une erreur consignée le 12 est corrigée : `--sans-now-loading`
n'a pas supprimé « le seul autre appelant connu » du dessin de texte. Il y en
a **118** pour `0x18019B2E0`, **91** pour le constructeur. Le texte est
partout dans ce moteur.

#### La table des fenêtres est la MÊME des deux côtés

C'est elle qui a tout ouvert. La version Xbox lit une table de 59 entrées en
`0x82085700`, `{planche, nom du calque}`. Final Showdown porte **la même**, en
`0x18052E680` : **91 entrées de 24 octets**, `{planche, _, nom, _, _}` —
`cmn_win_s_01`, `pause_win_m`, `choice_win_04`, `board_win`… Son lecteur est
**`0x1801BC580`**, jumeau exact du `FUN_822E39C0` de 2007, et il dessine ses
libellés.

#### La recette de Final Showdown, transcrite

Trois gestes y figuraient que nous ne faisions pas :

| | ce que nous faisions | ce que fait Final Showdown |
|---|---|---|
| calque du contexte 2D | laissé où l'AET l'avait mis | **`0x180187AA0()` lu, `0x180187CB0(2)` posé, remis à la fin** |
| sous-mode du style | jamais posé | `0x18019B870(style, 2)` — la chasse propre à chaque glyphe |
| position | `+0x34`…`+0x40` écrits à la main | `0x18019B800(desc, {x,y,l,h}, 9)` |

Le premier est le plus parlant : **la Xbox fait le même geste, avec la même
valeur 2** (`FUN_822C29E8` puis `FUN_822C29D8(2)`, restauré par
`FUN_822C2A18`). Le troisième ne fait pas que poser des coordonnées : il pose
aussi `desc+0x2C = 9` et surtout **`desc+0x10 = 1`**, ce qui allume le
découpage `0x200` dans `0x18019AC70` — la boîte devient le cadre de découpe,
et les drapeaux `0x800` (retour à la ligne) prennent leur sens.

Le reste : mode de police **1** et non 2, couleur en `desc+0x08`, format la
chaîne `"%s"` du moteur (`0x180347CF8`), drapeaux `0x800 | alignement`.

```c
sauv = 0x180187AA0();              /* [contexte 2D + 0x828] */
0x180187CB0(2);
0x18019A8C0(desc);   0x18019A9D0(style);
0x18019B6F0(style, 1);   0x18019B870(style, 2);   0x18019B830(style, 30.0f);
desc+0x48 = style;
0x18019B800(desc, {x, y, largeur, hauteur}, 9);
desc+0x08 = couleur;
0x18019B2E0(desc, 0x800 | alignement, "%s", texte);
0x180187CB0(sauv);
```

**La profondeur n'était pas en cause.** Les deux témoins de l'essai — l'un au
compartiment 71 (celui de FS), l'autre au 127 (le nôtre, hérité du nom de
variante) — sont sortis **tous les deux**. Le rang 127 reste disponible pour
ce qui doit passer devant tout ; il n'est pas nécessaire ici.

### 9.17 LES ANCRES : le Quest ne place pas son texte, il le POSE

Rien n'est placé à l'œil. Les fenêtres de `AET_N_QWIN` portent des calques
qui ne dessinent rien — des **repères** — et le **suffixe de leur nom donne
l'alignement** : `_lt` gauche-haut, `_rt` droite-haut, `_ct` centre-haut, `_c`
centre. La version Xbox les lit par leur nom, `FUN_82166778(objet, nom)`, et
prend x/y/z en `+0x40/+0x44/+0x48`.

**Le jumeau chez Final Showdown est `0x1800298B0(objet, nom)`** : il parcourt
un vecteur d'enregistrements de **0x78 octets** dont le nom est en `+0x70`, et
rend une copie ; l'appelant y lit `+0x40` (x), `+0x44` (y), `+0x64`
(opacité). Il a **123 appelants** — c'est une API courante du moteur, pas une
curiosité.

L'inventaire complet des ancres est dans `analysis/quest/ancres_qwin.txt`,
sorti de la planche elle-même par `tools/aet.py` (le bloc de transformation
d'un calque est en `+0x28` : huit propriétés `{nombre de clés, pointeur}`,
origine, position, rotation, échelle, opacité).

| fenêtre | ancre | x, y |
|---|---|---|
| lieu | `p_hall_menu_win_01_ct` | 640, 100 |
| | `c_button_csr_c_01_lt` / `d_01_lt` / `d_02_lt` | 252, 133 / 271 / 335 |
| maison | `p_home_menu_win_30_02_ct` / `_30_03_ct` | 640, 166 / 640, 330 |
| joueurs | `p_plylist_win_01_ct` / `_02_ct` | 640, 95 / 640, 141 |
| | `p_plylist_win_name_36_03_lt` / `_dan_36_03_c` | 389, 216 / 854, 228 |
| statut | `p_status_win_01_ct` | 640, 135 |
| | `_hed_30_02_lt` / `_dat_30_02_rt` | 469, 194 / 821, 194 |

Les **pas** et les **écarts** viennent du code de 2007, lus un par un :

| | valeur | où |
|---|---|---|
| menu de la maison | +30 par ligne | `DAT_82011814` |
| lignes du statut | +32 par ligne | `DAT_820035F0` |
| colonnes du statut | −72 / +72 de l'ancre | `DAT_82084CB4` |
| lignes d'un lieu | x = 640, y = ancre +43 / +73 / +16 | `DAT_82015B9C`, `DAT_8208E5AC`, `DAT_82085A50`, `DAT_82003608` |

**La couleur des titres.** La Xbox pose `0xFFBFF560` — en ARGB gros-boutiste,
rouge 0xBF, vert 0xF5, bleu 0x60, un vert-jaune. Final Showdown range la
couleur octet par octet dans le sommet (`0x18019B4A0`), rouge en premier : le
même vert-jaune s'y écrit **`0xFF60F5BF`**.

### 9.18 L'inventaire des textes avait une lacune : 83 → 492

`quest_textes.py` ne voyait que le `li r3, imm` **collé à l'appel**. Or le
Quest range ses identifiants dans un **tableau de pile** et les relit en
boucle — `FUN_8230BEB0`, le menu de la maison, en charge six d'un coup
(`addi r11, r0, 0x219` … `0x21F`, puis `stw`). Le balayage n'en voyait
**aucun**. Huit libellés manquaient, dont le **titre de chaque lieu**.

`--immediats` corrige, et sans deviner : il relève tout immédiat plausible
(`li rN, imm`, `0 < imm < borne`) chargé dans le **module** du Quest,
`0x82300000..0x82320000`. Ce n'est pas un chiffre rond pris au hasard : c'est
la plage d'où `quest_x360.c` et `quest_gestion_x360.c` ont été décompilés, et
la mesure y trouve **190 des 272** fonctions que le graphe d'appels rattache
au Quest (les autres sont des utilitaires partagés : AET, texte, tri). La
remontée par le graphe seule ne suffisait pas — `FUN_8230BEB0` n'y figure
pas. C'est une sur-approximation **assumée** : une longueur ou un nombre
d'images peuvent y passer, mais aucun identifiant n'est déplacé, et chaque
chaîne de trop coûte quelques octets en fin de tableau.

**492 chaînes**, aux identifiants 23052 à 23543 ; la borne du résolveur
`0x1801EFD10` passe à 23544.

#### Les neuf lieux portent leur nom, et l'ordre se recoupe

| id | texte | lieu |
|---:|---|---|
| 528 | SEGA WORLD NORTH | `swn` |
| 529 | SEGA WORLD SOUTH | `sws` |
| 530 | SEGA WORLD ROUTE 101 | `swr` |
| 531 | CLUB SEGA DOWNTOWN | `csd` |
| 532 | CLUB SEGA BAY AREA | `csb` |
| 533 | SEGA ARENA COAST | `sac` |
| 534 | SEGA ARENA EAST | `sae` |
| 535 | EVENT SQUARE | `dom` |
| — | (la maison : pas de nom, un MENU) | `hom` |

C'est **exactement** l'ordre de `g_quest_zooms` et `g_quest_icones`, établi
séparément à l'écran le 2026-09-12, une icône par appui. Deux mesures
indépendantes qui tombent juste : l'ordre des lieux est le bon.

#### Ce que les fenêtres portent aujourd'hui

* **un lieu** — son nom en vert-jaune, puis *Official Tournaments*,
  *Currently not in progress.* (grisé), *List of official tournaments*,
  *Customize* ;
* **la maison** — six lignes : *Customize*, *Status*, *Quest settings*,
  *Save*, *Return to Character Select*, *End Quest Mode* ;
* **la liste des joueurs** — *RIVAL LIST* et le nom du lieu ;
* **le statut** — *STATUS* et ses six intitulés.

Les **valeurs** chiffrées du statut et la liste des joueurs sont venues le
lendemain : voir §9.19 et §9.20.

### 9.19 LES MILLE RIVAUX : `npc_tbl.bin` (2026-09-27, vu à l'écran)

Frédéric : « je vois les noms des rivaux et le statut ».

**Final Showdown n'a AUCUNE table de rivaux** — `npc_tbl` n'existe ni dans son
`.par` ni dans `vf5fs_media/`. Ils sont partis avec le mode. La place est donc
libre : poser le fichier ne masque rien, ne déplace rien, n'écrase rien. C'est
le cas le plus simple rencontré dans ce portage, et il tranche une question de
méthode.

#### Pourquoi un fichier, et pas des chaînes

Les libellés du Quest sont partis dans `string_array.farc` (§9.18) parce que
ce sont des libellés. **Un rival n'en est pas un** : c'est un enregistrement
de 0x90 octets qui porte son nom, sa réplique en deux lignes, *son
personnage*, et les réglages de son IA. L'étape 4 — se battre contre un
rival — en aura besoin en entier. On pose donc le fichier, et `apm.dll` le
lit : `tools/rivaux.py --ajouter`.

#### La disposition, lue puis mesurée

Lue dans `FUN_8230DDF0`, qui recopie l'enregistrement dans l'objet du rival :

```
1000 enregistrements de 0x90 octets, puis le réservoir de chaînes
l'enregistrement n vit en n * 0x90 ; au-delà de 999 le jeu prend n % 1000

  +0x00  u32  offset ABSOLU du NOM          (dix caractères au plus)
  +0x04  u32  offset de la réplique, ligne 1
  +0x08  u32  offset de la réplique, ligne 2
  +0x14  u8   LE PERSONNAGE
  +0x18  24 x u16 puis 24 x u16   la tenue, deux jeux
  +0x88  u8   +0x89  u8   +0x8A  u8   l'IA
```

Les entiers sont **gros-boutistes** et les chaînes de l'**UTF-8**.

`+0x14` n'a pas été déduit, il a été **compté** : dix-sept valeurs distinctes,
0 à 16, environ 59 rivaux chacune — c'est le personnage, et VF5 de 2007 en a
dix-sept.

**Le fichier de la racine du média est le JAPONAIS.** Ce sont les
`lang/<lg>/npc_tbl.bin` qui portent les traductions (en, fr, ge, it, sp). On
pose l'anglais, comme demandé.

```
   0  perso  0  steven jul    I will be the still coret t
   1  perso  4  WildStyle     Come get it!
   2  perso  1  AndySwat      Not in the face!
   3  perso  1  SGT. Angry    Anger is my fuel.
```

### 9.20 LA LISTE DES JOUEURS ET LE STATUT

Les deux fenêtres sont transcrites de la Xbox — `FUN_82311078` pour la liste,
la fonction voisine pour le statut — avec le même prologue que tout le reste
du Quest : calque 2D à 2, mode 9, et un **rang** propre à la fenêtre (9 pour
le statut, 0xB pour la liste).

#### La liste

Neuf lignes par page (`min(nombre, 9)`), pas de **36** (`DAT_82010304`),
taille **36** — le « 36 » du nom de l'ancre `p_plylist_win_name_36_03_lt` est
bien la taille de police. Le titre est 558 « RIVAL LIST » en vert-jaune, le
sous-titre le **nom du lieu** (528…535), et la ligne du bas, calée à droite
sur `p_plylist_player_ratio_rt`, compose 560 « Arcade completion rating: »
avec un pourcentage.

#### Le statut

Sept lignes. Les deux ancres donnent les deux colonnes, et le code de 2007 les
**écarte de 72 pixels chacune** (`DAT_82084CB4`) : l'intitulé part à
469 − 72 = 397, la valeur à 821 + 72 = 893, alignée à droite. Le pas est de 32
(`DAT_820035F0`), la taille 30 — encore le nombre inscrit dans le nom de
l'ancre.

| ligne | intitulé | valeur | format |
|---|---|---|---|
| 1-4 | 545 à 548 | profil `+0x60`…`+0x6C` | `%.1f` + 401 « % » |
| 5 | 549 Longest streak | `+0x70` | 402 « %d Wins » |
| 6 | 550 / 552 | `+0x78` / `+0x80` | 403 « %d » |
| 7 | 551 / 553 | `+0x74` / `+0x7C` | 404 « %d:%d:%d » |

**Les deux dernières lignes basculent, et le rythme a dû être retrouvé.** Le
code divise un compteur d'images et prend le bit 0 — mais le diviseur n'est
écrit nulle part en clair : c'est la multiplication magique `0x6C16C16D`
suivie d'un `>> 7`. En la faisant tourner, le diviseur est **180** : trois
secondes par page à soixante images par seconde. Page A « Total number of
matches » et « Total playing time » ; page B « Number of matches » et
« Completion time ».

#### Deux absences volontaires

**Les valeurs sont à zéro, et c'est exact.** Elles viennent du profil Quest du
joueur, qui n'existe pas encore de notre côté : un Quest neuf affiche bien des
zéros. On montre l'état initial plutôt que des chiffres inventés.

**La liste montrait les neuf premiers de la table, pas ceux du lieu** — et
c'était faux : la liste du lieu ne demande aucun profil, elle se lit dans
`npc_tbl` lui-même. Corrigé le lendemain, voir §9.21.

### 9.21 LE PROFIL DU QUEST (2026-09-27, vu à l'écran)

Frédéric : « OK ça fonctionne ».

**Ce que 2007 en fait.** Le profil vit en `+0xC0` de la sauvegarde du joueur
(`FUN_8230B5B8`), et le Quest n'y lit que deux choses pour ses écrans :

| | |
|---|---|
| profil + 0x74 | 1000 bits : le rival a été **rencontré** |
| profil + 0xF4 | 1000 bits : le rival a été **battu** |

`0xF4 − 0x74 = 0x80`, soit exactement 1000 bits arrondis à trente-deux u32.
Le test du jeu est `1 << (n & 0x1F) & champ[(n >> 3) & 0x1FFFFFFC]`.

**Le pourcentage de la première ligne du statut n'est pas deviné.** Il se lit
en clair :

```
compte = les rivaux À LA FOIS rencontrés ET battus
pourcentage = compte * _DAT_82006C1C * DAT_82003EDC
            = compte * 0,001 * 100          soit le compte divisé par dix
```

**Notre fichier.** On ne recopie pas la sauvegarde Xbox — elle est prise dans
un conteneur de profil qui n'a pas d'équivalent ici. `quest_profil.bin`, à
côté du jeu, porte les mêmes champs en petit-boutiste :

```
+0x000  8    « QUESTPRF »          +0x008  u32  version (1)
+0x010  128  RENCONTRÉ             +0x090  128  BATTU
+0x110  u32  plus longue série     +0x114  u32  nombre de combats
+0x118  u32  temps de jeu, en secondes
```

`tools/profil_quest.py` le lit, l'efface, et sait en fabriquer un d'essai
(`--battre N`) — une sonde, pas de la progression.

#### Le piège de l'horloge, et il a coûté un essai

Frédéric, à l'écran : « completion time / total playing time changent en
continu ». Le profil affichait **277 224 secondes — 77 heures — après
quelques minutes**.

`quest_tic` ne reçoit **pas un écart** : il reçoit l'horloge **absolue** du
module (`GetTickCount() − g_quest_t0`). La première version l'ajoutait telle
quelle à chaque image. On garde donc l'instant précédent et on n'ajoute que
la différence ; le repère est remis à zéro en sortant du Quest, sinon tout le
temps passé **dehors** rentrerait d'un coup à la visite suivante ; et l'écart
est écrêté à une seconde — un écran de chargement ne doit pas compter pour
dix minutes.

#### La liste par lieu ne demande aucun profil

`FUN_8230E018(vecteur, filtre, masque)` parcourt les mille rivaux et garde
ceux dont `npc_tbl[n] + 0x88` tombe dans le masque. **`+0x88` est le lieu** —
huit valeurs, 130 à 138 rivaux pour les sept premières, **59** pour la
huitième, mille en tout.

Le sous-titre de la fenêtre de 2007 se prend dans `{528…534, 556}` : les sept
lieux nommés, puis « Special » — et **non** 535 « EVENT SQUARE », le nom que
la carte donne au dôme. Nos sept premières salles valent donc lieu 0 à 6 mot
pour mot ; pour le dôme on prend le huitième, le seul restant, 59 rivaux
triés à la main, et le dôme est le lieu des tournois. **C'est une lecture,
pas une mesure** — elle est écrite pour être contredite.

Le feuilletage : en 2007 HAUT/BAS défilent et GAUCHE/DROITE changent de lieu.
Chez nous HAUT/BAS font tourner les trois fenêtres, alors GAUCHE et DROITE —
qui ne servaient à rien une fois un lieu ouvert — prennent le défilement.

#### Ce que le profil commande à l'écran

Le masquage (`？？？？？`, `0x8208E508`), l'étoile jaune des battus à trente
pixels à gauche (`0x820117C8`, `DAT_82011814`), la première ligne du statut,
le temps de jeu, et la ligne du bas de la liste : la page, puis combien des
rivaux de ce lieu sont connus.

**Une décision de portage, assumée.** Ouvrir un lieu marque ses rivaux comme
rencontrés. En 2007 le bit se pose au **combat**, et il n'y a pas encore de
combat ; sans cela la liste n'afficherait que des points d'interrogation et
le profil ne se verrait jamais. Le jour de l'étape 4, cette règle disparaît.

Les six premières lignes du statut restent à zéro, et c'est exact : elles
demandent des combats, des objets ou des emblèmes. Frédéric a tranché — pas
de profil fictif pour le moment.

### 9.22 LE CURSEUR, ET LE DÉPART AU COMBAT (2026-09-27)

Frédéric : « le curseur fonctionne sur les deux écrans ».

#### Les touches ont bougé, et pour une raison

Un curseur veut HAUT et BAS — c'est d'ailleurs ce que fait 2007. Le carrousel
des trois fenêtres, lui, n'existe pas là-bas : ce sont trois tâches
distinctes. Il passe donc sur GAUCHE/DROITE.

| un lieu ouvert | |
|---|---|
| **GAUCHE / DROITE** | la fenêtre : le lieu, les joueurs, le statut |
| **HAUT / BAS** | le curseur — la ligne du menu, ou le rival dans la liste |
| **VALIDER** | partir au combat contre le rival sous le curseur |
| **W** | revenir à la carte |

Sur la carte, rien ne change.

**Le curseur est la COULEUR, et rien d'autre** : la ligne choisie prend le
vert-jaune des titres. J'avais ajouté un chevron à gauche ; Frédéric l'a fait
retirer. En 2007 c'est une composition AET posée sur la ligne
(`FUN_8230A1C0`) ; ses ancres sont dans la planche et déjà mesurées —
`c_button_csr_c_01_lt`, `d_01_lt`, `d_02_lt`, à x = 252, y = 133 / 271 / 335.
Le jour du vrai surlignage, tout est là.

Dans la liste des rivaux, la page suit le curseur : elle ne se commande pas,
comme en 2007.

#### Partir au combat, et revenir

Le chemin est celui du jeu. `TRANSITION_CAVE` (`0x18034579C`, posée par
`--transition-game`) fait exactement ceci, et `apm.dll` l'imite :

```
0x1800B23A0()      la session existe-t-elle ?
0x1800B3620(0)     sinon la créer -- l'argument est le NOMBRE DE JOUEURS
0x1800DA9A0(2)     mode 2 = GAME
0x1800DA9C0(17)    sous-état 17 = SELECTOR
```

Pour le retour, on ne détourne rien : le moteur revient au **menu** de
lui-même après un combat — c'est le maillon que `--transition-game` a posé
(`0x1800DA9EC`) — et dès qu'il y est on redemande l'état du Quest, du geste
exact de SCOREBOARDS.

#### Deux défauts, et le journal les a nommés

**1. Une collision de nom, que le C ne signale pas.** Le drapeau du va-et-vient
s'appelait `g_quest_retour` — et `g_quest_retour` **existait déjà** : c'est le
code de retour du dessin de texte. Deux `static int` du même nom dans une même
unité de compilation forment une **définition provisoire** : le C n'en fait
qu'une seule variable, et **ni `-Wall` ni `-Wextra` ne disent rien**. Chaque
texte dessiné y posait 5, la machine de retour y lisait « reviens du combat »,
et redemandait l'état du Quest à chaque image — **2 913 fois dans un seul
journal**, avant même qu'une touche soit pressée. L'écran était repris en
boucle ; le curseur n'avait aucune chance de se voir.

C'est un piège structurel ici : `quest_runtime.c` est inclus dans
`apm_stub.c`, donc **tout le module est une seule unité de compilation**.

**2. Une phase manquante.** La machine n'en avait que deux : demander le
combat, puis guetter le MENU. Or au tour suivant le répartiteur n'a pas encore
agi sur le vœu — **le mode est encore le MENU** — donc elle concluait que le
combat était fini. Trois phases maintenant : attendre que le mode **quitte**
le menu, attendre qu'il y **revienne**, puis redemander le Quest. Plus un
renoncement au bout de dix secondes si rien ne part.

#### Ce qui manquait au combat — CORRIGÉ LE SOIR MÊME, voir §9.23

Le paragraphe qui tenait ici disait que « le champ qui porte le combattant
choisi n'est pas identifié dans ce projet » et renvoyait à une sonde sur
`0x18014F4A0`. **C'est faux depuis le soir du 2026-09-27** : le champ est
`session + 0x28 + joueur × 4`, et il s'est lu sans aucune sonde. Le détail,
et le plantage qu'il a révélé, sont en **§9.23**.

Le verdict du combat, lui, n'est toujours pas lu : le bit « battu » ne se pose
pas encore.

### 9.23 LE CHAMP DU COMBATTANT, ET LE PLANTAGE DE VS (2026-09-27, le soir)

Deux phrases de Frédéric ont mené ici, dans cet ordre : « le mode quest lance
actuellemnt le mode arcade, ce n'est pas son but. », puis, à l'essai suivant,
« le jeu crash au lacement du combat ».

#### Le champ est trouvé, et il n'a demandé aucune sonde — CONFIRMED

L'écrivain est `FUN_1800B2F80(session, joueur, p3, p4, p5, p6)` :

| écrit | ce que c'est |
|---|---|
| `session + 0x28 + j × 4` | **le PERSONNAGE du joueur j** |
| `+ 0x30`, `+ 0x38`, `+ 0x40` | trois autres champs par joueur, **non identifiés** |

La session est **`DAT_1806F9C18`** ; `FUN_1800B23A0()` la rend, et rend zéro
tant qu'elle n'existe pas.

**`FUN_1800B3620(n)` n'est pas un constructeur qui rend l'objet.** Son type
de retour est `undefined1` — **un booléen**. La lire comme un pointeur était
mon erreur du premier essai. Elle crée la session et **remplit chaque
`+0x28 + j×4` avec `0x15`**.

**Vingt et un, pas vingt.** `0x15` = 21 est la valeur « aucun » ; les
personnages vont de **0 à 20, Dural compris**. Ma garde `>= 20` rejetait donc
Dural, le seul personnage que ce chantier a ajouté.

La preuve est à l'exécution, dans `quest_journal.txt` :

```
[quest] combat : joueur perso 0 contre "BiG's Ring" perso 7 ; rival 294
```

Le bon rival, son personnage pris dans `npc_tbl + 0x14`, écrits dans la
session. **Ce qui manque n'est pas l'identification, c'est le chargement.**

#### Pourquoi le saut direct vers VS plante — LIKELY, et c'est à MESURER

Le sous-état **19 (VS)** est bien le combat, et poser les deux combattants
suffit à le *demander* — pas à le *tenir* : l'essai a planté le jeu.

La lecture du sélecteur dit pourquoi. Entre GAME/SELECTOR et VS, il ne retient
pas deux numéros : il **charge** les combattants — `0x1800B6D80` par joueur,
puis `0x18016CF00` et `0x180186D40` — avant de commettre son choix. C'est
exactement le sous-état **0x56 de 2007, « préparation du combat »** (§1), que
nous n'avons pas.

**Le niveau de confiance est LIKELY, pas CONFIRMED** : c'est une lecture du
chemin du sélecteur, pas une mesure du plantage. **L'adresse fautive n'a pas
été relevée.** La première chose à faire à la reprise est donc de la mesurer —
`tools\plantage_5r.cmd` met le jeu sous débogueur en laissant le clavier
libre, et dit dans quelle section et à quelle adresse l'exception tombe. Une
adresse vaut mieux qu'une déduction, et ce chantier l'a payé assez souvent.

#### Trois corrections portées dans le code le soir même

1. `QUEST_PERSOS` passe de 20 à **21** ;
2. la phase 1 de `quest_retour_de_combat` attendait que le mode **quitte le
   MENU** — or on part de **DATA_TEST, mode 3** : elle se déclenchait au
   premier tour. Le journal le disait en clair, `le combat est parti, mode 3`.
   Elle attend maintenant le mode **GAME** ;
3. le départ **revient au sélecteur** (`sous(17)`), avec le commentaire qui
   dit pourquoi. Ce n'est pas le but du mode — Frédéric l'a dit — c'est un
   palier assumé tant que la préparation n'existe pas. Un écran de trop vaut
   mieux qu'un plantage.

### 9.24 LA PRÉPARATION DU COMBAT EXISTE DÉJÀ DANS FS : LE SOUS-ÉTAT 18 (2026-09-29)

**Et d'abord, une correction.** Le §9.23 disait, en LIKELY, que le sélecteur
« charge les combattants (`0x1800B6D80` par joueur, `0x18016CF00`,
`0x180186D40`) ». **C'est faux, et le C de `0x1800DB270` le dit** : ces trois
appels sont dans la branche d'**entrée en piste**, pas dans celle qui commet le
choix. La vraie raison du plantage est ailleurs, et elle est maintenant lue.

#### Ce que l'entrée du combat exige — CONFIRMED, c'est écrit dans son C

`0x1800DC890`, l'entrée du sous-état 19 (VS) :

```c
uVar5 = FUN_1800b23a0();              /* la session */
uVar1 = FUN_1800b24b0(uVar5);         /* session + 0x4E0 */
uVar3 = FUN_1800244d0(uVar5);         /* [session+8] : le joueur courant */
FUN_1800b3100(uVar5);
iVar4 = FUN_1800244d0(uVar1);         /* [session+0x4E8] */
if (iVar4 == 0)      { ... appels indirects : UN combattant ... }
else if (iVar4 == 1) { ... appels indirects : DEUX combattants ... }
else goto LAB_1800dc9ce;              /* RIEN n'est installe */
```

`FUN_1800b2450(session+0x4E0, j)` rend `session + 0x4E0 + 0x68 + j*0x5A0` :
**la fiche du combattant**, 0x5A0 octets — le même pas que le dossier de
joueur `[0x18070FB10] + 0x18 + j*0x5A0`.

**Tout tient à `[session+0x4E8]`.** S'il ne vaut ni 0 ni 1, VS saute
l'installation et part sans combattants. C'est cela, et non le personnage, qui
manquait le 2026-09-27 : le personnage était bien posé, le journal le montrait.

#### Qui écrit ce champ : `MODE_SELECTOR`, le sous-état 18

`analysis/mode_selector.md` l'avait décrit en mars du chantier sans qu'on voie
à quoi il servirait : **« le sous-état qui n'a pas d'écran »**. C'est notre
préparation.

Sa queue `0x1800DAFA6` (§4.5 de ce document-là) fait, dans l'ordre :

| | |
|---|---|
| `0x1800B28B0(session+0x50, ebx)` | `[session+0x58] = (type de partie == 3)` → **0** chez nous |
| `0x1800B32E0(session+0x50, …)` | `[session+0x5C]` = un tirage 0/1/2 |
| `0x1800490E0` / `0x180049030` / `0x180049220` | le dossier du joueur |
| **`0x1800B8540(session)`** | **la préparation elle-même**, 2 026 octets |

Et `0x1800B8540` prend son cas 1P/2P dans `[session+0x58]`
(`FUN_1800244d0(FUN_1800b23b0())`), bâtit la structure du combat et la pose
dans le sous-objet par `0x1800B34D0` — d'où `[session+0x4E8]`.

**Puis la chaîne du mode fait le reste** : `GAME` (`0x1803A02C8`) enchaîne
`SELECTOR → MODE_SELECTOR → VS → GAMEOVER`. `MODE_SELECTOR` ne demande rien en
finissant ; le successeur de chaîne l'emmène dans VS tout seul.

#### Donc on ne transcrit rien

Le Quest pose deux gestes et un vœu :

```
0x1800B2FA0(session, 0, 1, 0)   le joueur 0 ENTRE EN PISTE
[session+0x28]     = son personnage        (APRES l'entree : elle les efface)
[session+0x28+4]   = le personnage du rival
0x1800DA9A0(2)     mode GAME
0x1800DA9C0(18)    sous-etat MODE_SELECTOR -- la PREPARATION
```

Deux conditions, lues elles aussi :

1. **le joueur doit être en piste.** `[session+0x0C + joueur]` est le drapeau
   (`0x1800B1D30`) ; sur la borne c'est le sélecteur qui le pose, par
   `0x1800B2FA0`. Cette fonction **remet le personnage à `0x15` et trois
   `-1`** : les personnages se posent donc *après* elle ;
2. **le joueur 1 doit rester dehors.** Si les deux drapeaux sont posés, la
   phase 2 de `MODE_SELECTOR` part dans l'autre branche et lit l'objet du
   sélecteur `[0x180714928]`, qui n'existe pas dans notre parcours. Le rival
   est un adversaire **contrôlé par la machine** — ce qu'il est dans le Quest.

Les trois autres champs de `0x1800B2F80` (+0x30, +0x38, +0x40) ne sont pas des
réglages : `0x1800B3100` les **recalcule** depuis `session+0x4FC`/`+0x504`
juste avant le combat. On n'y touche pas.

#### Ce qui reste à voir à l'écran

La voie directe est armée par défaut ; **`T` rebascule sur le sélecteur**, la
voie validée du 2026-09-27 — on ne défait pas ce qui marche. Le journal dit
laquelle est armée, et le nom du personnage des deux combattants.

Ce qui n'est pas établi : que le personnage du rival **tienne** jusqu'au
combat. Rien dans ce qui a été lu ne le réécrit, mais l'adversaire machine
d'une partie d'arcade est d'ordinaire choisi par l'échelle du mode ; si un
autre combattant apparaît, c'est là qu'il faudra regarder.

### 9.25 LE DESCRIPTEUR DU COMBAT, CHAMP PAR CHAMP (2026-09-29)

Frédéric : « je ne lance plus rien de basé sur une supposition. » Voici donc la
lecture, des deux côtés — le Quest de 2007 et Final Showdown — et la mesure qui
l'a déclenchée.

#### La mesure qui oriente tout

Le journal, à l'instant où le combat part depuis le Quest :

```
mode de jeu 9 ; persos relus 0 contre 7 ; en piste 1/0 ; cas 1P/2P 5
```

**Mode de jeu 9.** Ce n'est pas Arcade (0) : c'est la valeur d'un bloc **jamais
initialisé**, exactement ce que `mode_de_jeu.md` §13.1 avait déjà mesuré au
débogueur (`mode=9, sante=0/0, temps=0, rounds=0, cpu=0`). Et les deux
personnages, eux, **survivent** : 0 contre 7, le rival demandé.

#### Ce que le Quest de 2007 fait : il COMPOSE le combat

`FUN_82320300(joueur)`, l'entrée du sous-état 0x56, ne choisit pas un mode.
Elle bâtit une structure sur la pile et la remet au moteur par
`FUN_821DCD98(session+sous-objet, &structure)`.

Ce qu'elle y met : les deux fiches de joueur (1 488 octets chacune,
`FUN_822360C8`), le rival recopié de son enregistrement (nom `DAT_82AD1634`,
personnage `DAT_82AD16AC`, costume `DAT_82AD16B0`, IA), **un décor tiré au
hasard** dans une table de vingt montée sur la pile (`FUN_822C6DE8`),
**temps `0xA8C` = 2 700 trames = 45 s**, **santé `0xC9` = 201**,
**3 rounds**, et une **force de CPU** ajustée par le rang du rival et par le
profil du joueur.

#### Le jumeau dans FS, et il est exact

`FUN_821DCD98` ↔ **`0x1800B34D0(session+0x4E0, descripteur)`**. Même sous-objet,
même forme. Et `DAT_820036C0` (la table « l'autre joueur », {1,0}) a pour jumeau
**`DAT_18034B208`**.

Le descripteur fait **0x50 octets, vingt mots de quatre**. Voici ce que
`0x1800B34D0` en fait, et d'où `0x1800B8540` tire chaque valeur :

| # | offset | valeur, chez FS | va en (sous-objet) |
|--:|---|---|---|
| 0 | 0x00 | **0** — le CAS lu par l'entrée de VS : 0 = un combattant, 1 = deux | +0x08 (`session+0x4E8`) |
| 1 | 0x04 | `[session+0x58]` — le mode de partie, écrit par `MODE_SELECTOR` | +0x0C |
| 2 | 0x08 | 0 | +0x10 |
| 3-4 | 0x0C, 0x10 | **les PERSONNAGES**, `[session+0x28+j*4]` (`0x1800B23E0`) | +0x14, +0x18 |
| 5-6 | 0x14, 0x18 | `[session+0x30+j*4]` (`0x1800B23F0`) | +0x1C, +0x20 |
| 7-8 | 0x1C, 0x20 | `[session+0x38+j*4]` (`0x1800B2400`) | +0x24, +0x28 |
| 9-10 | 0x24, 0x28 | `[session+0x40+j*4]` (`0x1800B2410`) | +0x2C, +0x30 |
| 11-12 | 0x2C, 0x30 | 0 pour le joueur, **1 pour l'adversaire** | +0x34, +0x38 |
| 13 | 0x34 | **LE TEMPS**, en trames (secondes × 60) | +0x3C |
| 14 | 0x38 | **LA SANTÉ**, deux `short` : 1P en 0x38, 2P en 0x3A | +0x40 et +0x42 |
| 15 | 0x3C | **LES ROUNDS** | +0x44 |
| 16 | 0x40 | le joueur courant, `[session+8]` — il sert d'INDEX | +0x48 |
| 17 | 0x44 | **LE DÉCOR** | +0x4C |
| 18 | 0x48 | `[session+0x50+0x3F4]` | +0x50+joueur×4 |
| 19 | 0x4C | quatre octets de drapeaux (0x4C testé, 0x4D/0x4E/0x4F recopiés) | +0x5B, +0x5C, +0x61 |

La correspondance est confirmée deux fois : `0x1800B34D0` lit le mot 14 **en
deux `short`** — et `0x1800B8540` y écrit bien deux santés, `sVar7 + 1` pour
chacune. Une structure lue à l'aveugle ne tombe pas juste deux fois.

#### D'où viennent le temps, la santé et les rounds — et LÀ est le défaut

Dans `0x1800B8540`, deux sources, et une garde entre les deux :

```c
if (local_368._4_4_ == 0) {                /* le mode de partie de la session */
    temps  = FUN_180047de0(config + 0xa0) * 0x3c;
    sante  = FUN_180047de0(config + 0x48) + 1;   /* les deux joueurs */
    rounds = FUN_180047de0(config + 0x38);
}                                          /* config = 0x18066B830 : la BORNE */
...
if (FUN_18019c090() < 4) {                 /* LE MODE DE JEU, 0 a 3 */
    temps  = [0x180751018] * 0x3c;
    sante  = [0x180751014] + 1, [0x180751016] + 1;
    rounds = [0x180751019];
}
```

**Le bloc de réglages `0x180751014`-`0x180751019` n'est lu QUE si le mode de
jeu vaut 0 à 3.** Le nôtre vaut **9**. Le combat prend donc les réglages de la
**borne** (`0x18066B830` — 220 d'énergie, 2 rounds, 45 s, ceux qu'affiche le
lanceur), et rien de ce que le Quest voudrait. C'est, mot pour mot, « le mode
arcade qui se lance ».

#### Le décor : deux politiques, et elles diffèrent

FS le prend dans `0x1800AF400(personnage)` — une liste de paires
`{personnage, décor}` en `[0x1806F9C10 + 0xA0]`, bornée à 21 : **le décor
« maison » de l'adversaire**. Le Quest de 2007, lui, **tire au hasard** parmi
une vingtaine. Deux conceptions différentes ; celle de 2007 est un choix à
refaire, pas un défaut à corriger.

#### Ce que cela donne comme marche à suivre

Il n'y a **pas de mode de jeu à choisir** : il y a un descripteur à alimenter.
Deux voies, et la seconde est la plus sûre :

1. **écrire le descripteur nous-mêmes** et appeler `0x1800B34D0` — c'est
   littéralement ce que fait 2007, mais il faut alors reproduire aussi les
   quatre appels qui suivent (`0x1800B3340` ×2, `0x1800B2280`, `0x1800B28D0`,
   `0x1800B1BE0`) et les deux fiches de 1 488 octets ;
2. **poser les six octets de réglages** (`0x180751014`-`0x180751019` : santé
   1P, santé 2P, temps, rounds, niveau CPU) **et un mode de jeu dans 0..3**,
   puis laisser `0x1800B8540` faire son travail. Les valeurs du Quest sont
   connues : **santé 200 (→ 201), temps 45, rounds 3**.

La deuxième voie n'invente rien : elle remplit le bloc que le moteur lit déjà,
avec les nombres lus dans le jeu de 2007.

#### Ce qui n'est PAS encore lu, et qu'il ne faut pas supposer

* **la force du CPU** : 2007 la calcule (`FUN_8224D778`) à partir du rang du
  rival et du profil ; FS a un simple octet, `[0x18075101A]`. La conversion
  reste à établir ;
* **les deux fiches de 1 488 octets** (`FUN_822360C8` / `FUN_1800B8540`) : elles
  portent le costume et les objets. Non lues ;
* **les drapeaux du mot 19** ;
* et, mesuré mais non expliqué, **`[session+0x4E8] = 5`** avant la préparation :
  la valeur relevée par la sonde est antérieure à l'écriture du descripteur,
  elle ne dit donc rien de l'état réel du combat.

### 9.26 LA FORCE DU CPU, ET LES OBJETS DES RIVAUX (2026-09-29)

Deux questions de Frédéric, et elles se répondent dans la même fonction.

#### La force du CPU : une formule, et toutes ses constantes

`FUN_82320300` la calcule, `FUN_8224D778` la pose :

```c
force = (float)npc_tbl[rival] + 0x10;      /* LA FORCE PROPRE DU RIVAL */
if (profil.difficulte == 1) force += 0.2;  /* 0x82022658 */
if (profil.difficulte == 2) force += 0.4;  /* 0x820035B0 */
if (!tournoi && serie) {                   /* la serie de victoires en cours */
    if (serie >= 20)      force += 0.1;    /* 0x8201DA2C */
    else if (serie >= 10) force += 0.05;   /* 0x82002398 */
    else if (serie >= 2)  force += 0.01;   /* 0x82003A3C */
}
force = borne(force, 0.0, 1.0);            /* 0x82000A34 = 0 ; 0x82000B08 = 1 */

FUN_8224D778(force, 0) :  DAT_8284CA48 = (short)(force * 30.0);   /* 0x82011814 */
FUN_8224D7E8(force, …) :  DAT_8284CA60 = (short)(force * 31.0);   /* tournoi */
```

Les neuf constantes ont été **lues dans l'image**, pas devinées :
0,2 · 0,4 · 0,01 · 0,05 · 0,1 · 0 · 1 · 30 · 31.

**La force du rival est donc un flottant de 0 à 1 rangé en `npc_tbl + 0x10`** —
un champ que l'inventaire de `npc_tbl` n'avait pas encore nommé — et le moteur
la convertit en **un entier de 0 à 30**.

#### Et l'échelle de Final Showdown est LA MÊME

`0x1800B8540` prend la sienne dans `FUN_1800ACD80(niveau, combat)` : une table
**5 × 8** dans le singleton `GameScoreSetting` (`0x1806F9C10 + 0xD0`), c'est-à-dire
dans **`rom/game_score.txt`**, en clair dans l'archive
(`extracted/game_score.txt`) :

| niveau | combat 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| VERY_EASY | 2 | 3 | 4 | 7 | 9 | 10 | 11 | 14 |
| EASY | 3 | 5 | 6 | 11 | 13 | 13 | 15 | 21 |
| NORMAL | 4 | 6 | 8 | 14 | 17 | 18 | 21 | 28 |
| HARD | 5 | 8 | 10 | 18 | 22 | 25 | 28 | 31 |
| VERY HARD | 8 | 12 | 16 | 28 | 31 | 31 | 31 | 31 |

**De 2 à 31.** Exactement l'échelle de 2007 (`force × 30`, et 31 en tournoi).
Les deux jeux comptent la force du CPU dans la même unité ; il n'y a pas de
conversion à inventer, seulement une valeur à poser.

FS l'écrit par `FUN_18010ED40(joueur, valeur, personnage)`, qui la range en
**`[fiche + 0x1CF8]`** — un `u16` dans la fiche du combattant
(`DAT_18070FC78 + joueur × 0x1D28`). C'est le point d'entrée pour la nôtre.

Deux choses que cette table apprend au passage : la difficulté de FS a **cinq**
crans (`[0x18075101A]`, 0 à 4) et la force **monte avec le numéro du combat**
dans la série d'arcade — ce que le Quest, lui, ne fait pas : il la prend du
rival.

#### LES OBJETS ET LE COSTUME DES RIVAUX : oui, et c'est direct

`FUN_8230DDF0(rival, fiche)` recopie l'enregistrement de `npc_tbl` (0x90
octets) dans le bloc de travail `0x82AD1634` :

| npc_tbl | → fiche | ce que c'est |
|---|---|---|
| +0x00 / +0x04 / +0x08 | +0x00 / +0x1F / +0x47 | le nom et les deux répliques |
| +0x0C (u16), +0x0E (u8) | +0x70, +0x72 | — |
| **+0x10 (float)** | **+0x74** | **la force du CPU** |
| +0x14 | +0x78 | **le personnage** |
| +0x15, +0x16 | +0x79, +0x7A | — |
| **+0x18 : 24 × u16** | **+0x7C** | **liste d'objets n°1** |
| **+0x48 : 24 × u16** | **+0xAC** | **liste d'objets n°2** |

Puis `FUN_82320300` recopie les deux blocs de 0x30 octets **côte à côte** dans
sa fiche de combattant et les parcourt d'une traite — 2 × 24 identifiants —
pour allumer un bit par objet dans un champ de **mille bits** (31 mots), avec
un contrôle de borne qui se déclenche au-delà de 999. La fiche part ensuite au
moteur par `FUN_821D1A38` puis `FUN_82236060(0x827A99F8, fiche, joueur)`.

**Donc oui : chaque rival du Quest porte son costume personnalisé, sous forme
de quarante-huit identifiants d'objets**, et c'est le même mécanisme que la
personnalisation du joueur. Les noms de ces objets sont déjà chez nous —
`analysis/dlc_objets.md` et `analysis/dlc/vf5_item_names_en.json`.

Ce qui reste à faire de ce côté : trouver où FS range ce champ de mille bits
dans **sa** fiche de combattant (`0x1D28` octets), et vérifier que les
identifiants de 2007 désignent les mêmes objets que ceux de FS — la comparaison
des trois catalogues est déjà faite (590 identiques, 891 modifiés, 83 absents),
elle donnera la table de correspondance.

### 9.27 LE CHAMP D'OBJETS DE FS, LA TABLE DE CORRESPONDANCE, LES FICHES ET LES DRAPEAUX (2026-09-29)

Les quatre points demandés, dans l'ordre.

#### 1. Où Final Showdown range le champ d'objets — CONFIRMED par son propre message d'erreur

`0x1800B8540`, dans la branche du mode de partie 1, allume **tous** les objets
de l'adversaire :

```c
lVar20 = FUN_180101820(DAT_18070FB10, autre_joueur);   /* base + 0x18 + j*0x5A0 */
uVar25 = 0;
do {
    if (1999 < uVar25) FUN_1800934D0(lVar20 + 0x160);  /* hors bornes */
    *(u64 *)(lVar20 + 0x160 + (uVar25 >> 6) * 8) |= 1L << (uVar25 & 0x3F);
} while (++uVar25 < 2000);
```

Et `FUN_1800934D0` n'est pas une fonction anonyme : elle appelle
`FUN_1802FBD30("invalid bitset<N> position")`. **C'est un `std::bitset` de
2 000 bits, en `dossier_joueur + 0x160`.** Le dossier vaut `0x5A0` octets
(`FUN_180101820`), contre **mille** bits chez 2007. Final Showdown a doublé la
capacité — cohérent avec ses catalogues (Kage : 913 objets contre 279).

À noter pour plus tard : FS donne **tout** à son adversaire machine. Le Quest,
lui, lui donne la garde-robe du rival, et c'est précisément la différence
qu'on veut.

#### 2. La table de correspondance des objets — `tools/objets_correspondance.py`

Les deux jeux rangent leurs objets dans `chritm_tbl.farc`, une table par
personnage. **Mesure du jour : la disposition est la MÊME des deux côtés** —
en-tête `{magie, nombre, décalage}`, enregistrements de `0x50` octets,
petit-boutiste, les mêmes champs. Seule la magie diffère.

**Un piège, et il a failli fausser toute la table.** Le code `K MMM V III` de
`+0x48` porte l'identifiant sur **trois chiffres** : il reboucle au-delà de
999, et Final Showdown dépasse le millier. Pris modulo 1000, l'objet
« 1001 PANTS_10 » d'Akira se fait passer pour le « 001 ATAMA_01 ». L'identifiant
se lit donc **dans le libellé**, qui le porte en clair — et le CSV du jeu
(`extracted/csv_utf8/APM3_FS/chritm_tbl/aki_itm.csv`) le confirme :
**772 noms sur 772 identiques** après correction, 765 sur 768 avant.

La clef d'appariement est le **libellé interne du modèle** (`ATAMA_01`,
`OUTER_03_ZZC`…), contrôlé par la catégorie et la variante de couleur. Résultat :

| | |
|---|---|
| personnages communs | **18** (FS ajoute Jean et Taka-Arashi) |
| objets de 2007 | **3 401** |
| **appariés** | **3 401 (100 %)** |
| absents de FS | **0** |

#### 2 bis. Les variantes de couleur : c'est le NOM qui les sépare

Premier essai, la clef était le **libellé de modèle** — et il ne distingue
rien : les **seize** bandanas d'Akira portent tous « BANDANA_01 », et le code
`K MMM V III` dit pour chacun « modèle 2, variante 3 ». Le champ « variante »
ne varie pas, et le champ de tête (10, 20, 30, 40, 50) ne suit pas les
couleurs non plus. **La couleur ne vit que dans la texture, et dans le nom.**

Or les deux jeux ont la **même table japonaise** à la racine de leur média :
« 赤鉢巻 » en 2007 est « 赤鉢巻 » dans Final Showdown. Mesure sur Akira : les
**198 objets retrouvés par le nom, et tous uniques**. Sur les dix-huit
personnages :

| | |
|---|---|
| appariés **par le nom** | **3 393** |
| par le repli (libellé, catégorie, variante) | 8 |
| **sans équivalent** | **0** |

Cinquante appariements ont le bon nom et un **libellé de modèle différent** —
`OUTER_03` devenu `OUTER_03_ZZC`, `TE_04_TE_R` devenu `TE_04_UDE_R`. L'examen
les donne tous à numéro identique (23 → 23, 35 → 35) : FS a renommé le modèle,
pas changé l'objet. C'est donc le libellé qui a bougé, et le nom qui tient.

#### 3. Les deux fiches : ce ne sont pas 1 488 octets

**Correction de ce que j'ai écrit hier.** Le « 1 488 » venait de Ghidra, qui
dimensionne une variable de pile par l'écart jusqu'à la suivante. La taille
réelle se mesure au **pas du tableau** : `(&DAT_827A9A09)[joueur * 0x528]` dans
`FUN_82320300` — **0x528, soit 1 320 octets**. Son jumeau FS vaut **0x5A0,
1 440 octets** (`FUN_180101820`).

Disposition de la fiche de 2007, relevée sur les écritures de `FUN_82320300` :

| offset | contenu |
|---|---|
| +0x000 / +0x001 | deux octets d'état (0 et 1) |
| +0x059 | le **nom** du rival, 0x1F octets |
| +0x081 / +0x0A9 | ses deux **répliques**, 0x28 octets chacune |
| +0x0F8 | **le personnage** |
| +0x0F9…+0x0FF | sept octets venus de la queue de l'enregistrement du rival |
| +0x100 / +0x104 / +0x130 | trois mots du même |
| **+0x138** | **le champ d'objets, 31 mots = 1 000 bits** |
| +0x1B8 / +0x1B9 | deux octets de costume |
| **+0x1BA** | **les 2 × 24 identifiants d'objets**, l'un derrière l'autre |
| +0x423 | un octet de plus de l'enregistrement |

Côté Final Showdown, quatre points sont mesurés et le reste ne l'est pas :
`+0x01` (un booléen que `0x1800B8540` teste), `+0x117` (un octet que la queue
de `MODE_SELECTOR` passe à `0x180049030`), **`+0x160` le `bitset<2000>`**, et
`+0x410` (passé à un appel indirect). **Les deux dispositions ne coïncident
pas** — c'est une réécriture, pas un décalage constant : il faudra lire les
écrivains de FS un par un, et je ne l'ai pas fait.

Ne pas confondre avec la **fiche de combattant**, qui est un autre objet :
`[0x18070FC78] + joueur * 0x1D28` (7 464 octets), celle où `FUN_18010ED40`
range la force du CPU en `+0x1CF8`.

#### 4. Les drapeaux du mot 19 du descripteur

Quatre octets, et trois d'entre eux ont maintenant un sens. `0x1800B8540` les
compose ainsi (`iVar8` = `[session+0x50+0x3F0]`, le **numéro du combat dans la
série**) :

| octet | valeur | ce que ça dit |
|---|---|---|
| 0x4C | 1 si `iVar8 == 0` et `[session+0x50+0x45C] != 0` | **c'est le premier combat** |
| 0x4D | `mode de partie != 1`, forcé à 0 si `FUN_1800B2590` | (voir ci-dessous) |
| 0x4E | `FUN_1800B2680` | **c'est le dernier combat** |
| 0x4F | jamais écrit sur ce chemin — reste 0 | — |

`FUN_1800B2590(session+0x50)` : mode de partie 0 **et** combat n° 7 —
c'est-à-dire **le huitième et dernier** de la série d'arcade.
`FUN_1800B2680` dit la même chose en tenant compte du mode de jeu : pour
License Challenge (mode 2) c'est `combat == n-1` où `n` vient de
`FUN_1801D43C0` (le nombre d'épreuves de la licence courante), sinon `== 7`.

Et `0x1800B34D0` s'en sert : l'octet 0x4C, lorsque le cas vaut 0, décide de
poser `[sous-objet + 0x58 + joueur] = 1` ; l'octet du joueur adverse est posé
sans condition, et `+0x5A` vaut toujours 1. Les octets 0x4D, 0x4E, 0x4F vont
respectivement en `+0x5B`, `+0x5C` et `+0x61`.

**Pour le Quest, ces trois drapeaux se déduisent :** un combat du Quest est
toujours le premier ET le dernier de sa série — il n'y a pas de série.

### 9.28 L'ACCUEIL DU QUEST ET LA CARTE DU JOUEUR (2026-09-29)

Lu après avoir porté la décompilation du mode à **323 fonctions sur 323**.

#### L'accueil : `0x8230CF50`, onze étapes

`TaskQuestWelcome` elle-même est une coquille — sa seule méthode de vtable,
`0x8230D700`, est son destructeur. Le travail est dans la machine à onze états
de `0x8230CF50` :

| état | ce qu'il fait |
|---:|---|
| 0 | ouvre la fenêtre et demande le libellé **523** (`FUN_82322798(0x20B)`) — « *Starting Quest Mode. On the Map Screen, select an Arcade Icon…* » |
| 1 | attend la validation, et relève le **secret** (voir plus bas) |
| 2-4 | ferme la fenêtre, monte l'affichage de la carte |
| 5 | vise **l'argent courant + 50 000**, plafonné à **999 999** |
| 6 | trente trames d'attente |
| 7 | **+500 par trame** (10 000 avec le secret), un **son toutes les trois trames**, jusqu'à la cible |
| 8-9 | trente trames encore |
| 10 | fini |

**Le secret de la notice est mesuré.** Le libellé 557 dit « tenir LB en
validant le message d'introduction pour démarrer avec le maximum d'argent » :
c'est l'état 1 qui le relève (`FUN_822DAC30()`, bit 0x17, puis
`FUN_822D0D60(0x40)`), et il pose **999 999** d'emblée, en versant 10 000 par
trame au lieu de 500.

#### La fiche du joueur : `0x827A99F8 + 0x10 + joueur × 0x528`

C'est la carte que Frédéric montre (NO-NAME / 10th kyu / W:0 L:0 / Win ratio /
50000G). Champs relevés sur ses écrivains et ses lecteurs :

| offset | contenu |
|---|---|
| +0x059 | **le nom** (« NO-NAME ») |
| +0x0EC | **l'argent**, en G — libellé 999 `%dG` |
| +0x0F8 / +0x0F9 | **le personnage** et son **costume** |
| +0x100 | **W**, les victoires |
| +0x104 | **L**, les défaites |
| +0x130 / +0x138 | deux champs de bits (contrôlés par `FUN_822C5128`, le garde-fou de `bitset`) |
| +0x1B8 / +0x1B9 | deux octets de réglage |
| **+0x423** | **LE GRADE** — 0 = aucun ; le picto dessiné est `grade − 1` |

Le **win ratio** n'est pas stocké : `FUN_82308C90` le calcule,
`W / (W + L) × 100`, et l'écrit avec le libellé **400** « Win ratio: ».

#### Le grade est un PICTO, et Final Showdown a la planche

2007 nomme dix pictos, `gamdan_kyu01` à `gamdan_kyu10`, tous résolus par
`0x821D58C8`. La carte les dessine par `FUN_82308670(alpha, …, grade − 1,
position)`.

**Le binaire de Final Showdown porte `spr_s_gamdan`** — la planche des grades
est là, ses pictos se trouveront par leur nom comme les nôtres. Et **aucune
des 323 fonctions du Quest n'écrit `+0x423`** : le grade est tenu par le
moteur partagé, c'est le rang de VF5, pas une invention du mode.

#### Le profil de sauvegarde : `sauvegarde + 0xC0`

`FUN_8230B5B8` rend `FUN_822DAC40() + 0xC0`, ou zéro s'il n'y a pas de
sauvegarde. Champs touchés par le mode :

| offset | contenu |
|---|---|
| +0x001 / +0x002 / +0x003 | trois octets d'état (les données existent, le mode est ouvert) |
| +0x004 | comparé à `DAT_82AD172C` |
| +0x008 | **la difficulté** du Quest (0, 1, 2 — c'est elle qui donne +0,2 / +0,4 à la force du CPU) |
| +0x010, +0x014, +0x018 (15 × 4) | **la personnalisation** : recopiée vers la tâche par `0x82315C20`, relue par `0x82315D00` |
| +0x054 (15) et +0x063…+0x068, +0x06C, +0x070 | la suite de la même personnalisation |
| **+0x074** | **1 000 bits : rival RENCONTRÉ** |
| **+0x0F4** | **1 000 bits : rival BATTU** |
| **+0x174 / +0x178** | **W et L sauvegardés** (comparés à la fiche +0x100/+0x104) |
| +0x184 / +0x188 | deux mots |

La paire `0x82315C20` / `0x82315D00` est le va-et-vient complet entre le profil
et l'écran : quinze emplacements de quatre octets, quinze octets, et six
octets de plus. C'est le costume du joueur, et c'est le même mécanisme que les
deux listes de 24 objets des rivaux.

#### Ce que le portage n'a pas, et que cela chiffre

Le Quest tel qu'il se joue demande, dans l'ordre : le **CHARACTER SELECT** et
la **création de données**, le **nom**, l'**argent** (50 000 au départ), le
**grade** (picto), **W/L** et le ratio, la **personnalisation** (quinze
emplacements), et le **grade de chaque rival**. Le portage n'en a aucun.

### 9.29 LE GRADE DES RIVAUX, ET LE SÉLECTEUR DE DONNÉES (2026-09-29)

#### Le grade est en `npc_tbl + 0x7C` — CONFIRMED sur ses propres captures

Le champ `+0x0C` que je soupçonnais est **nul pour les mille rivaux** ; `+0x0E`
ne l'est que pour 201 d'entre eux, avec des valeurs toutes différentes — c'est
un index, pas un grade.

Le profil de chaque octet du registre le donne sans ambiguïté :

| octet | valeurs | lecture |
|---|---|---|
| **+0x7C** | **42 distinctes, 0 à 41**, réparties en cloche | **LE GRADE** |
| +0x7B | 8 valeurs : 0, 1, 3, 7, 15, 31, 63, 127 | un masque progressif |
| +0x82 | 0 à 22 | — |
| +0x86 | 0 à 10 | — |
| +0x83, +0x87 | 244 et 250 valeurs sur 256 | deux octets quasi aléatoires |

Et la vérification ne vient pas de moi : elle vient de **la capture d'écran de
Frédéric**, la salle SEGA ARENA COAST.

| à l'écran (2007) | rival | `+0x7C` |
|---|---:|---:|
| **Raeme 4th kyu** | 118 | **6** |
| **Qazi 10th kyu** | 7 | **0** |
| **JasonElbow 7th kyu** | 52 | **3** |

**0 = 10th kyu**, et l'échelle monte : 9th = 1, 8th = 2, 7th = 3 … 1st kyu = 9,
puis les dan. Quarante-deux crans, ce qui est l'échelle de rang de VF5.

Le joueur, lui, porte son grade en **`fiche + 0x423`**, dessiné en picto
(`gamdan_kyu01`…`kyu10`, §9.28) — et **Final Showdown a la planche**,
`spr_s_gamdan`.

#### Le CHARACTER SELECT et la création de données

Ce n'est **pas** du code propre au Quest : c'est le **sélecteur de données de
sauvegarde** du jeu, partagé. Trois fonctions, décompilées dans
`analysis/quest/x360_selecteur_donnees.c` :

| fonction | rôle |
|---|---|
| `0x82307D48` | le dessin de la liste : l'état du périphérique (libellés 1355-1358), les emplacements, **1352 « Create new data »**, **1354 « Play without using data »** |
| `0x82307AE0` | la confirmation d'effacement — **1527** « *Are you sure you want to delete the selected Character Data?* » |
| `0x823084E8` | la légende du bas (**25** « Initialize / Back / Toggle rankings ») |

Les emplacements viennent de `FUN_822DA8B8(périphérique, numéro)` : c'est la
sauvegarde Xbox qui les fournit, un par personnage. Les deux notices de
l'écran sont les libellés **1363** (« *Select the character data you want to
edit…* ») et **1368** (« *Select the character data to use…* »).

**Côté Final Showdown, les pages existent mais personne ne les pilote.**
`analysis/customize_0x299.md` relève les scènes `CARD SELECTOR`,
`DATA SELECTOR` et `CHAR SELECTOR` dans le binaire, et `analysis/dural.md`
note que **`CHAR SELECTOR` n'a aucun pilote** — la page est là, le code qui la
mène a été retiré avec le mode console. C'est donc un écran à refaire, comme
la carte du Quest l'a été : les planches sont dans le jeu, la machine est à
écrire.

#### Ce que cela donne comme marche à suivre pour la carrière

1. **le grade**, des deux côtés : il se lit (`npc_tbl + 0x7C` pour le rival,
   `fiche + 0x423` pour le joueur) et se dessine (`spr_s_gamdan`) ;
2. **l'argent** : `fiche + 0xEC`, et la séquence d'accueil qui verse 50 000 ;
3. **W / L** : `fiche + 0x100` / `+0x104`, persistés en `profil + 0x174` /
   `+0x178` ;
4. **le nom** : `fiche + 0x59` ;
5. **la création de données** : un écran à écrire, sur des planches présentes.

### 9.30 Ce qui manque

Dans l'ordre :

1. **le combat du Quest** — tout est lu : le descripteur (§9.25), la force
   du CPU (§9.26), le champ d'objets, la table de correspondance et les
   drapeaux (§9.27). Ce qui manque est d'ÉCRIRE : santé 200, temps 45,
   rounds 3, force prise dans `npc_tbl + 0x10`, costume traduit par
   `analysis/quest/objets_2007_vers_fs.json`, premier et dernier combat à 1 ;
2. **le verdict** — pour poser « battu », d'où descendent les quatre
   pourcentages, l'étoile, la série et le reste. **LU : voir le §14.**
3. l'écran de rencontre et la réplique du rival (`npc_tbl +0x04`/`+0x08`,
   déjà lues) ; **§16.1**
4. **les autres entrées des menus**, qui ne font rien aujourd'hui : Customize
   et la boutique (objets, argent, écran de personnalisation), Quest settings,
   les trois entrées du dôme, Tournament dans une salle, la liste des
   emblèmes. Quatre des six lignes de la maison sont câblées (Status, Save,
   Return to Character Select, End Quest Mode) **§18** ;
5. les objets et les emblèmes (`analysis/dlc_objets.md` porte la table des
   noms) **§18.3** ;
6. les tournois (sous-état 0x55 de 2007, planches `tnt`/`tnto` déjà
   déclarées) ; **§17**
7. la colonne « dan » de la liste des joueurs. **§16.3**

---

## 10. L'ARGENT DE 2007, BALAYÉ EN ENTIER — ET IL NE VIENT PAS DES COMBATS (2026-09-30)

La commande était nette : « Les gains réels de 2007 : l'argent (aujourd'hui
300 G + 100 G par cran, **règle de portage**), la montée de grade (aujourd'hui
un cran tous les dix battus), le lot des tournois (2 000 G / 10 000 G). Tout
cela est dans les 323 fonctions : le lire et remplacer nos règles. »

Les 323 fonctions ont été balayées sur le champ « argent ». **La prémisse est
fausse, et c'est un résultat, pas un échec** : le montant par combat n'y est
pas, parce qu'en 2007 **un combat ordinaire ne rapporte pas d'argent**.

### 10.1 Où vit le porte-monnaie — et la confusion à ne plus faire

    FUN_82235F28(base, creneau) = base + creneau * 0x528 + 0x10

C'est une **fiche de joueur de 0x528 octets**, indexée par le créneau de
sauvegarde, et l'argent y est en **`+0xEC`**, plafonné à **999 999**
(`if (0xF423E < x) x = 999999`, deux fois dans le code).

**Ce n'est PAS le bloc de `FUN_8230B5B8`.** Dans ce bloc-là, `+0x74` porte les
mille bits « rencontré » — 128 octets, donc jusqu'à `+0xF4` — et `+0xF4` les
mille bits « battu ». `+0xEC` y tombe **au milieu du premier champ de bits**.
`PROMPT_REPRISE.md` et le cahier de séance mêlaient les deux objets ;
les confondre en écriture corromprait les bits de rencontre.

### 10.2 Les TROIS seuls endroits qui écrivent l'argent

| # | où | ce qu'il fait |
|---|---|---|
| 1 | `quest_x360.c` l. 3232 | remise à zéro |
| 2 | la **création de données**, cas 5 à 7 de `FUN_82315xxx` | cible = `argent + 50 000` (ou 999 999 si `[état+0x150]`) ; versement de **+500 par trame** (ou +10 000), un son toutes les trois trames ; arrêt quand la cible est atteinte |
| 3 | **`FUN_82317F88`** | le paiement d'un **événement** |

Le cas 2 est déjà porté et vu à l'écran (entrée 79 du journal). Le cas 3 ne
l'est pas.

### 10.3 Les événements, et d'où sortent les 10 000 G

`FUN_82318B18` arme un événement `n` (0 à 14 ; 0-6 d'une famille, 7-14 de
l'autre, `DAT_82656B0C`). Chacun porte **trois récompenses** `{type, valeur}`,
lues dans `FUN_82315890(n)` :

    piVar10[-1] = TYPE    0 = un objet   (FUN_82317950)
                          1 = FUN_823179E8
                          2 = de l'ARGENT
    piVar10[ 0] = VALEUR  *(int *)(FUN_82315890(n) + (c*3 + i + 1) * 4)

avec deux règles visibles dans le code :

    if (evenement DEJA accompli)  valeur = valeur >> 1;      // la moitie
    if (n == 0x0D)                valeur = 10000;            // sauf celui-la

`FUN_82317F88` verse ensuite, avec le plafond :

    uVar8 = valeur + *(int *)(fiche + 0xEC);
    *(uint *)(fiche + 0xEC) = uVar8;
    if (0xf423e < uVar8) uVar8 = 999999;
    *(uint *)(fiche + 0xEC) = uVar8;

**Le « 10 000 G » du cahier des charges est donc confirmé**, et il appartient à
l'événement `0x0D`. Le « 2 000 G », lui, est une valeur de la table que rend
`FUN_82315890` — **cette fonction n'est pas dans le lot décompilé**. On ne
l'écrit donc pas : on la lira quand on la lira. **C'est lu : voir le §16.2.**

### 10.4 La montée en grade

Même balayage, même résultat : **aucune règle de montée en grade dans les 323
fonctions**. Le grade du rival est une donnée (`npc_tbl + 0x7C`, 42 valeurs) ;
celui du joueur n'est calculé nulle part dans ce lot.

### 10.5 Conséquence pour notre portage

Nos deux règles restent :

    argent = 300 G + 100 G par cran de grade du rival
    grade  = un cran tous les DIX rivaux battus, borne a 41

et elles sont désormais **documentées comme étrangères au modèle de 2007**, pas
comme une approximation de celui-ci. Le commentaire de `tools/quest_runtime.c`
(au-dessus de `quest_apres_combat`) porte tout ce qui précède, pour que
personne ne refasse le balayage.

Ce qu'il faudrait pour rendre le modèle d'origine : porter les **quinze
événements** et leur table de récompenses. C'est un chantier à part, et il
commence par `FUN_82315890`.

---

## 11. LE DOSSIER DE JOUEUR DE FS : CE QUI EST MESURÉ, ET CE QUI MANQUE (2026-09-30)

Commande §4.3 point 2 : « que l'adversaire soit le **rival**, avec son **nom**
et son **costume** ». Cela demande de cartographier le dossier de 0x5A0 octets.

**Ce qui est mesuré.** Un balayage des 14 100 fragments `.pdata` sur le facteur
`0x5A0` donne **23 fonctions**, dont onze le multiplient par un indice de
joueur. Leur idiome commun corrige un point du cahier de séance :

    0x1800B3470  imul rax, rbx, 0x5A0      ; rbx = l'indice du joueur
    0x1800B348C  add  rcx, 0x68            ; <- les dossiers commencent en +0x68
    0x1800B3493  add  rcx, rax

    0x1800B3A6E  lea  rbx, [rcx + 0x68]
    0x1800B3A72  imul rdx, rax, 0x5A0      ; rax = [rcx+0x48], le joueur courant

Le dossier du joueur `j` est donc à **`objet + 0x68 + j*0x5A0`**, et l'indice du
joueur courant vit en **`objet + 0x48`**. Le cahier annonçait `+0x18` : c'est
`+0x68`. Les onze porteuses :

    0x1800B1BE0  0x1800B3340  0x1800B3470  0x1800B38F0  0x1800B3A50
    0x1800B3B10  0x1800B3D70  0x1800B3EC0  0x1800FF970  0x180101970
    0x180101A30

**Ce qui n'est pas fait, et je le dis plutôt que de le supposer :** aucune de
ces onze n'a encore été lue jusqu'au champ du **nom affiché** ni à celui de la
**tenue portée**. Le point 2 du §4.3 reste donc **non fait**. Le prochain pas
est `0x1800B3470` (la plus courte, quatre arguments, elle appelle
`0x1800B0500` avec le dossier) et `0x1800B3EC0` (trois emplois du facteur,
c'est elle qui boucle sur les joueurs).


## 12. LE DOSSIER DE JOUEUR, CHAMP PAR CHAMP — LE NOM EST LOCALISÉ (2026-10-18)

Reprise du point laissé au §11 : « le prochain pas est `0x1800B3470` ».

### Ce que fait `0x1800B3470`, et une seconde structure par joueur

    0x1800B3485  rax = joueur * 0x5A0
    0x1800B348C  rcx = objet + 0x68 + rax        ; LE DOSSIER
    0x1800B3499  call 0x1800B0500(dossier, r8)   ; premiere pose
    0x1800B349E  rax = (joueur + joueur*8) << 6  ; = joueur * 0x240
    0x1800B34A9  rcx = objet + 0xBA8 + rax       ; UNE AUTRE TABLE
    0x1800B34C2  jmp 0x1800B10E0(cette table, r9); seconde pose

La fonction prend donc **deux** sources et les range à **deux** endroits : le
dossier de `0x5A0`, et une table jusqu'ici inconnue de **`0x240` octets par
joueur, a `objet + 0xBA8`**. Les deux poseurs (`0x1800B0500`, 3028 octets, et
`0x1800B10E0`) sont des copieurs champ par champ.

### Les chaines du dossier, et le NOM

`0x1800B0500` met la zone a zero puis appelle `0x1800133D0` (une copie de
chaine bornee) avec la longueur en `r8d` :

    0x1800B0551  r8d = 0x15 (21)   zone mise a zero des `dossier+0x05`
    0x1800B0564  call 0x1800133D0  -> CHAINE de 21 octets en **+0x05**
    0x1800B0576  r8d = 0x0B (11)
    0x1800B0588  call 0x1800133D0  -> chaine de 11 octets en **+0x1A**
    0x1800B05BD  r8d = 5
    0x1800B05CA  call 0x1800133D0  -> chaine de 5 octets en **+0x3C**

**Le champ du nom affiche est `dossier + 0x05`, 21 octets** -- vingt
caracteres plus le nul, ce qui est la longueur d un nom de joueur.

### La carte, telle qu elle se lit

| offset | taille | nature |
|---|---|---|
| +0x00 | 5 | octets copies un a un |
| **+0x05** | **21** | **chaine : le NOM** |
| +0x1A | 11 | chaine (10 caracteres) |
| +0x25 / +0x26 / +0x28 | 1 / 2 / 4 | scalaires |
| +0x30 / +0x38 | 8 / 4 | scalaires |
| +0x3C | 5 | chaine (4 caracteres) |
| +0x41 / +0x48 / +0x50..+0x56 | | scalaires |
| +0x59 | | une quatrieme chaine |

### Ce qui reste du point 2 du §4.3

Le **nom** est localise ; la **tenue portee** ne l est pas. Elle est
vraisemblablement l un des scalaires ci-dessus, ou dans la table de `0x240`
que `0x1800B10E0` remplit -- cette table est neuve et n a jamais ete lue.
Deux facons de trancher, sans rien patcher :

1. continuer `0x1800B0500` (3028 octets) jusqu a reconnaitre un champ qui
   ressemble a un identifiant de costume ;
2. recouper avec `ram/customize.bin`, que `apm.dll` sauve deja -- un dossier
   ecrit sur disque dit ses champs mieux qu un copieur.

La seconde est plus rapide et c est celle que je prendrais.

**Elle a ete prise : voir le §13 ci-dessous. La tenue est localisee.**


## 13. LA TENUE PORTÉE : DEUX JEUX DE 24 IDENTIFIANTS (2026-10-18)

Reprise du point laissé au §12, par la seconde voie qui y était proposée —
recouper avec `ram/customize.bin`. Rien n'a été patché, le jeu n'a pas été
lancé : tout ce qui suit est lu dans le fichier, dans les CSV du jeu et dans
le `.origine` au désassembleur.

### 13.1 Deux porteurs du même enregistrement, et une correction au journal

Le §11 écrivait « le cahier annonçait `+0x18` : c'est `+0x68` ». **Les deux
sont vrais, sur deux porteurs différents :**

    0x180101820(DAT_18070FB10, j)  ->  [0x18070FB10] + 0x18 + j*0x5A0
    0x1800B3470(objet, …)          ->  objet + 0x68 + j*0x5A0

Le premier est celui que les écrans de personnalisation modifient, et le seul
que `apm.dll` sauve. Les quatre chaînes relevées au §12 (`+0x05` sur 21,
`+0x1A` sur 11, `+0x3C` sur 5, `+0x59`) se lisent **telles quelles** dans la
sauvegarde à ces offsets : c'est le même type d'enregistrement, et les offsets
du §12 sont donc ceux de `customize.bin`. Que les deux pointeurs désignent la
même allocation n'est **pas** mesuré.

**Correction au journal.** `REPRISE.md` (126) appelle `+0x116` « le nom ».
C'est **le personnage** — l'entrée 89 du même journal l'avait déjà mesuré
(« le relais relit `[rax+0x116]` à chaque trame, voit le changement de
personnage »). Dans la sauvegarde il vaut **0**, soit AKIRA, et les objets
équipés sont effectivement ceux d'Akira. Le recoupement tient par les deux
bouts.

### 13.2 Le format de `ram/customize.bin`, relu dans notre propre stub

En-tête de 12 octets, puis deux blocs, et la somme boucle à l'octet près :

| fichier | taille | contenu |
|---|---|---|
| +0x00 | 4 | magie `"VF56"` |
| +0x04 | 4 | `0x0B40` = 2880 = 2 × `0x5A0` |
| +0x08 | 4 | `0x4B00` = 19200 = 150 × `0x80` |
| **+0x0C** | 2880 | **les deux enregistrements de travail** — l'offset 0 du bloc est l'offset 0 de l'enregistrement |
| **+0xB4C** | 19200 | **la table des personnages enregistrés**, 150 × `0x80` |

`12 + 2880 + 19200 = 22092`, la taille du fichier.

### 13.3 LA TENUE : un tableau à DEUX LIGNES, et le costume devant

`0x1801C3950` est le seul écrivain indexé du champ, et il donne la forme
entière :

    iVar1 = [écran + 0x78]                        ; LA LIGNE
    lVar2 = 0x180101820(DAT_18070FB10, 0)         ; toujours le joueur 0
    [lVar2 + 0x262 + (case + ligne*0x18)*2] = 0   ; 0x18 = 24 cases
    0x1801C4B40(lVar2 + 0x262 + ligne*0x30, pile) ; 0x30 = 48 = le pas d'une ligne
    0x1801C2BF0(…, [lVar2 + 0x260 + ligne], …)    ; +0x260 est indexé PAR LA LIGNE

`0x1801C31A0` écrit les deux octets ensemble (`[lVar1+0x261] = param_4` puis
`[lVar1+0x260] = param_3`, avec `si ligne == 0 alors param_4 = param_3`), et
relit `[ligne + 0x260 + lVar1]`. D'où :

| offset | taille | contenu |
|---|---|---|
| **+0x260** | 1 | le costume de la **ligne 0** |
| **+0x261** | 1 | le costume de la **ligne 1** |
| **+0x262** | 24 × u16 | **les objets portés, ligne 0** |
| **+0x292** | 24 × u16 | **les objets portés, ligne 1** |

**C'est octet pour octet la disposition de 2007** relevée au §9.27 : deux
octets de costume en `+0x1B8`/`+0x1B9`, puis « les 2 × 24 identifiants
d'objets, l'un derrière l'autre » en `+0x1BA`. Et c'est la forme des deux
listes de `npc_tbl` du §9.26 (`+0x18` et `+0x48`, écartées de `0x30`). Les
deux jeux rangent la tenue de la même façon ; il n'y a pas de conversion à
inventer.

**Deux lignes et pas trois** : les octets de costume sont deux, et
`+0x262 + 2*0x30 = +0x2C2`, où la sauvegarde porte déjà des flottants.

Le stub ne nomme que la ligne 0 (`CUST_PARTS 0x262`, « les 24 mots des
parties équipées »). Il recopie les 1440 octets en entier, donc **la ligne 1
est bien dans le fichier** — seul son journal l'ignore.

### 13.4 LES 24 CASES SONT NOMMÉES, et vérifiées une à une

L'ordre est celui de `extracted/csv_utf8/APM3_FS/chritm_tbl/Sasikae-Soutyaku_Sheet1.csv`,
qui porte exactement **24** lignes :

    0 ZUJO    1 KAMI    2 HITAI   3 ME        4 MEGANE  5 MIMI
    6 KUCHI   7 MAKE    8 KUBI    9 INNER    10 OUTER  11 KATA
   12 U_UDE  13 L_UDE  14 TE     15 JOHA_MAE 16 JOHA_USHIRO 17 BELT
   18 KOSI   19 PANTS  20 ASI    21 SUNE    22 KUTSU  23 HADA

La sauvegarde porte six cases non nulles, et **les six `Position` du CSV
d'Akira correspondent, six sur six** :

| case | position | id | objet (`aki_itm.csv`) |
|--:|---|--:|---|
| 1 | KAMI | 461 | `AKIITM041_ATAM_ATAMA_05` ピンクおさげヘアー |
| 10 | **OUTER** | 3 | `AKIITM003_JOHA_OUTER_01` 白八極胴着 |
| 13 | L_UDE | 78 | `AKIITM078_JOHA_UDED_01` 黒リストバンド |
| 17 | BELT | 7 | `AKIITM007_KAHA_BELT_01` 黒帯 |
| 19 | PANTS | 8 | `AKIITM008_KAHA_PANTS_01` 白八極パンツ |
| 20 | ASI | 9 | `AKIITM009_KAHA_ASI_01_ASI` 黒キックサポーター |

**La case 10, OUTER, est le vêtement** — « la tenue » au sens propre. Et
l'ensemble se lit : c'est le **costume 1P d'Akira** (sept objets : KAMI 001,
HITAI 002, OUTER 003, BELT 007, PANTS 008, ASI 009, L_UDE 078), **bandeau
retiré** (case 2 à zéro) et **cheveux remplacés** par l'objet 461, dont la
colonne `Default` est vide — un objet acquis, pas un objet de costume.

Un piège du CSV, et il a failli fausser la lecture : `ObjUid` et `ID` ne
portent pas le même numéro. L'objet 461 s'appelle `AKIITM041_…`. **C'est la
colonne `ID` qui est la clef**, et c'est elle que l'enregistrement range.

### 13.5 La table des personnages enregistrés porte les mêmes 24, en u32

Une seule entrée est occupée dans la sauvegarde. Elle s'aligne sur
l'enregistrement de travail avec un décalage constant de **deux mots** :

| entrée | taille | contenu |
|---|---|---|
| +0x00 | 4 | `1` — le créneau est occupé (la garde du moteur en `0x1801CFAA2` est « premier octet non nul ») |
| +0x04 | 4 | `0` — non identifié (voir §13.7) |
| **+0x08** | 24 × u32 | **les mêmes identifiants, un pour un** |
| +0x68 | 13 | `"TEST AKIRAX "` + nul — le nom que le `DataSelector` liste |
| +0x75 | 8 | `"GLNQQQS"` + nul — non identifié |

`+0x08 + 24*4 = +0x68` : le nom commence exactement où les 24 cases
finissent. Et l'élargissement u16 → u32 n'est pas une déduction :
`0x1801C4B40` le fait, 24 tours, `*(uint*)dst = (uint)*(ushort*)src`.

### 13.6 Ce que cela donne au point 2 du §4.3

Le point demandait l'adversaire **rival**, avec son **nom** et son
**costume**. Les deux pièces sont maintenant nommées des deux côtés :

| | 2007 (Xbox 360) | Final Showdown |
|---|---|---|
| costume | fiche `+0x1B8` / `+0x1B9` | enregistrement `+0x260` / `+0x261` |
| objets portés | fiche `+0x1BA`, 2 × 24 × u16 | `+0x262` et `+0x292`, 2 × 24 × u16 |
| source du rival | `npc_tbl + 0x18` et `+0x48`, 24 × u16 | — (à écrire) |
| personnage | `npc_tbl + 0x14` | enregistrement `+0x116` |

Les identifiants de 2007 ne désignent pas tous le même objet qu’en FS, et
la table qui les traduit **existe déjà** :
`analysis/quest/objets_2007_vers_fs.json`, 18 personnages, **3 401
entrées** (`id 2007` → `id FS`) — les 3 401 appariés du §9.27, bâtie le
2026-09-29. **Correction de ce que j’avais écrit ici : ce n’est pas à
faire, c’est fait.** Ce qui reste est de l’APPLIQUER à l’écriture.

### 13.7 Ce qui n'est PAS mesuré, et il faut le dire

- **ce que vaut `+0x260[ligne]`.** Il part dans `0x180139F70(personnage,
  valeur)`, qui indexe une table d'enregistrements de `0x60` octets (compte en
  `[table+0xC]`, décalage relatif en `[table+0x10]`), bornée par `compte-1`,
  avec **12 comme valeur spéciale « la dernière entrée »**. Que ce soit le
  numéro de costume (1P..10P) est cohérent avec le relevé de 2007 ;
  **ce n'est pas établi.** **LEVE : voir le §13.8.** Les deux octets valent `00 01` dans la sauvegarde,
  y compris chez le joueur 1 dont les 24 cases sont toutes à zéro — donc `1`
  est une valeur posée à l'initialisation, pas le résultat de la
  personnalisation ;
- **ce que sont les deux lignes** — laquelle est modifiée par quel écran ;
- la chaîne `"GLNQQQS"` de l'entrée de table, et son `+0x04` ;
- **le champ de 21 octets en `+0x05`.** Le §12 l'appelle « le nom affiché ».
  Il existe bien (le copieur `0x1800B0500` y pose une chaîne bornée à 21), mais
  dans la sauvegarde il porte `"0"`, et le nom que l'écran liste
  (`"TEST AKIRAX "`) est dans l'entrée de table, en `+0x68`. Lequel des deux
  le Quest doit écrire n'est pas tranché ;
- **qui lit `+0x262` en dehors de la zone de personnalisation.** Le balayage
  borné à `0x1801C0000`-`0x1801D2000` donne 25 accès dont 2 écritures ; le
  balayage du binaire **entier** tournait encore à la fin de la séance. C'est
  lui qui dira comment la tenue arrive au modèle et à la fiche de combattant
  (`[0x18070FC78] + joueur*0x1D28`).

### 13.8 `+0x260` EST BIEN LE NUMÉRO DE COSTUME — le balayage complet l'a donné

La réserve du §13.7 est **levée**. Le balayage du binaire entier (239 accès à
`+0x260`, 9 à `+0x261`, 40 à `+0x262`) a sorti `0x180147B40`, hors de la zone
de personnalisation, et elle dit tout en quinze lignes :

```c
undefined8 FUN_180147b40(int ligne, longlong enr)
{
  byte costume = *(byte *)(ligne + 0x260 + enr);
  if ((*(byte *)(enr + 0x116) < 0x15) && (costume < 10)) {
      ushort *porte = (ushort *)(enr + 0x262 + ligne * 0x30);
      uint   *stock = (uint *)FUN_180139f70(*(byte *)(enr + 0x116), costume);
      uint i = 0;
      while ((uint)*porte == *stock) {
          i++; porte++; stock++;
          if (0x17 < i) return 1;          /* les 24 identiques */
      }
      return 0;                            /* une case diffère */
  }
  return 1;
}
```

Cinq choses y sont **mesurées**, et trois d'entre elles étaient des réserves :

1. **`costume < 10` : dix costumes.** C'est exactement la colonne `Default`
   des CSV, `1P` à `10P`. `+0x260[ligne]` est donc le **numéro de costume**,
   de 0 à 9 — ce n'est plus une hypothèse ;
2. **`[enr + 0x116] < 0x15` : vingt et un personnages.** La borne confirme
   que ce champ est l'indice du personnage, et ferme la correction du §13.1 ;
3. **`0x180139F70(personnage, costume)` rend la tenue D'ORIGINE** de ce
   couple, en **24 × u32** — et ses enregistrements font `0x60` octets,
   soit `24 × 4`. La table que le §13.7 ne savait pas nommer est la table
   des costumes ;
4. la fonction compare les 24 cases portées à ces 24 cases d'origine et rend
   **1 si rien n'a été changé**, 0 sinon : c'est le « cette ligne est-elle
   encore le costume de série ? » du moteur ;
5. le pas `0x30` et le compte de 24 (`0x17 <`) sont confirmés une seconde
   fois, depuis une fonction qui n'a rien à voir avec `0x1801C3950`.

**Et la boucle se ferme sur la sauvegarde.** La ligne 0 porte le costume
**0**, et ses six objets sont le costume **1P** d'Akira. La ligne 1 porte le
costume **1** — donc 2P — et ses 24 cases sont à zéro : jamais ouverte. Les
`00 01` de `+0x260`/`+0x261` ne sont pas un drapeau, ce sont **les numéros de
costume des deux lignes**.

Le `12` spécial de `0x180139F70` (« la dernière entrée ») vient donc d'un
**autre** appelant que celui-ci, puisque la garde d'ici l'exclut. Non mesuré.

### 13.9 Qui touche le champ hors de la zone de personnalisation

Les porteurs relevés par le balayage complet, et ce qu'on en sait :

| site | fonction | ce que c'est |
|---|---|---|
| `0x1800B095A` / `0x1800B0964` | `0x1800B0500` | **le copieur du §12** : il recopie `+0x261` d'un enregistrement à l'autre. Les deux structures sont donc bien du même type |
| `0x1800B2B0C` / `0x1800B2B1A` | `0x1800B2930` | pose `+0x261` et prend l'adresse de `+0x262` — famille de la préparation du combat (`0x1800B8540`, `0x1800B3470`) |
| `0x180100190`, `0x180100E53`, `0x180109DC8` | `0x1800FFA70` et deux autres | la famille qui **possède** l'enregistrement (l'accesseur `0x180101820` y vit) |
| `0x180147B72`, `0x180147CC6`, `0x180147DFD`, `0x1801481AD`, `0x18014842C` | — | cinq prises d'adresse du tableau, dans le voisinage de la table des costumes (`0x180139F70`, `0x18014A630`). `0x180147B40` est la seule lue |
| `0x1800AFD56`, `0x1800B62FD`, `0x1800C4E1A`, `0x18020387D` | — | prises d'adresse, non lues |

**Deux écritures à écarter**, et c'est une limite de l'outil, pas une
mesure : `0x18006D851` écrit un **dword** en `+0x262` et `0x18010A69C` un
**octet**. Le tableau est fait de mots de 16 bits ; `champ_x64.py` balaye par
**déplacement** et ne sait pas de quel objet il s'agit. Ces deux-là portent
très probablement un autre objet au même déplacement — à ne pas inscrire au
compte des écrivains de la tenue sans l'avoir vérifié.

## 14. LE VERDICT DU QUEST : LES QUATRE POURCENTAGES, L'ÉTOILE, LA SÉRIE, ET LA POSE DE « BATTU » (2026-10-18)

Le point 2 du §9.30. Tout est lu dans `analysis/quest/*.c` et dans
`extracted/X360_VF5/vf5_x360.img` ; rien n'a été lancé.

### 14.1 Poser le bit : deux fonctions, et elles sont le vocabulaire du reste

    FUN_821D1798(&{champ, n}, b)    champ[(n>>3)&~3] |= 1<<(n&31)   si b
                                    champ[(n>>3)&~3] &= ~(1<<(n&31)) sinon
    FUN_821D1808(&{champ, n})       rend le bit n

Les deux prennent **une paire en pile** — l'adresse du champ puis l'indice —
et bornent l'indice à 999 (`FUN_822C5128` au-delà). C'est l'idiome du §9.21,
avec son écrivain.

### 14.2 « BATTU » SE POSE DANS `FUN_82320A68`, le rappel de l'événement 9

Le §2 avait nommé ce rappel (« événement 9 → `0x82320A68`, qui réécrit les
statistiques du rival ») sans le lire. Le voici, dans l'ordre, et c'est **tout
le verdict** :

```c
DAT_82AD1730 += FUN_821DDE10(session);          /* [session+0xAEC] - [session+0xAF0] */
if (FUN_821E3BB8() != 0) {                      /* = DAT_8279829C, un octet global */
    …
    FUN_8230DB40(DAT_82AD162C, 0x82AD1634);     /* les stats du rival */
    FUN_82315A10(gains);                        /* decremente [gains+0x90] et [+0x94] */

    if (FUN_821DD368(session) == DAT_82AD1618) {        /* [session+0xACC] = LE VAINQUEUR */

        if (bStack_14d != 0) {                          /* l'EMBLEME gagne */
            FUN_823178E0(&{emblemes + 0x7D, bStack_14d - 1}, 1);
        }
        …
        if (!FUN_823159D0(gains) && DAT_82AD172C < 999)  /* [gains+0x30] == 0 */
            DAT_82AD172C++;                              /* LA SERIE */

        profil = FUN_8230B5B8(DAT_82AD1618);
        FUN_821D1798(&{profil + 0xF4, DAT_82AD162C}, 1);   /* <<<< BATTU */
        if (*(uint *)(profil + 4) < DAT_82AD172C)
            *(uint *)(profil + 4) = DAT_82AD172C;          /* la PLUS LONGUE serie */

        if (FUN_82310098(profil, DAT_82AD1714, 0)) {       /* le LIEU est complet */
            static int recompense[8] = {8, 9, 6, 4, 5, 3, 7, 0x20};
            if (recompense[DAT_82AD1714] != 0x20)
                FUN_822DB578(recompense[DAT_82AD1714], -1);
        }
    }
    else {
        DAT_82AD172C = 0;                                  /* LA SERIE TOMBE */
    }
}
```

**Ce que cela établit :**

| | |
|---|---|
| le test de victoire | `[session + 0xACC] == DAT_82AD1618` — le champ du **vainqueur**, comparé à notre indice de joueur |
| « battu » | `FUN_821D1798(&{profil+0xF4, rival}, 1)` — **un seul site**, et il est sous le test de victoire |
| le rival | `DAT_82AD162C`, posé à la préparation du combat |
| **la série courante** | `DAT_82AD172C`, **+1 par victoire**, écrêtée à **999**, **remise à 0 dès une défaite** — et aussi à l’entrée d’un combat, §14.7 |
| **la plus longue série** | `profil + 0x04`, tenue par un **maximum** — jamais décrémentée |
| l'emblème du combat | champ de 256 bits en `emblemes + 0x7D`, bit `bStack_14d - 1` |
| le lieu complet | `FUN_82310098` + la table `{8, 9, 6, 4, 5, 3, 7, 0x20}` : les sept lieux nommés donnent une récompense, le huitième (`0x20`) n'en donne aucune |

**Le bit « rencontré » (`profil+0x74`) n'est PAS posé ici** — il se pose au
CHARGEMENT du rival, dans deux autres fonctions du mode. **Le §14.7 le
mesure, et corrige ce que cette phrase disait ensuite.** La décision de portage du §9.21 (ouvrir un lieu
marque ses rivaux rencontrés) reste donc un choix à nous, et elle ne
contredit rien de mesuré.

Deux gardes restent sans nom, et je ne les baptise pas : `DAT_8279829C`
(l'octet global qui autorise tout le bloc) et `[gains+0x30]` (qui empêche la
série de monter — le tournoi est le candidat, ce n'est pas lu).

### 14.3 LES QUATRE POURCENTAGES : trois comptes et une moyenne

`FUN_82310598` est le remplisseur de l'écran de statut, et il les pose côte à
côte en quatre flottants consécutifs :

```c
*(float *)(écran + 0x60) ← FUN_8230FF88(profil, …);    *(char *)(écran+0x84) = complet ?
*(float *)(écran + 0x64) ← FUN_82310238(fiche, [fiche+0xF8], …);  (écran+0x85)
*(float *)(écran + 0x68) ← FUN_823103C8(profil, …);               (écran+0x86)
*(float *)(écran + 0x6C) = (écran+0x68 + écran+0x60 + écran+0x64) * DAT_82003580;
if (écran+0x84 && écran+0x85 && écran+0x86) FUN_8230F488(…);   /* les trois a 100 % */
```

| rang | ce qui est compté | le champ de bits | le total |
|--:|---|---|---|
| 1 | **les rivaux** : à la fois **rencontrés** `profil+0x74` **et battus** `profil+0xF4` | 1 000 bits | 1 000 |
| 2 | **les objets** du personnage `[fiche+0xF8]` | 1 000 bits en `fiche+0x138` | les objets du catalogue de ce personnage, en sautant ceux dont `[rec+0x10] == -1` ou dont les bits 0 ou 1 de `[rec+0x00]` sont posés |
| 3 | **les emblèmes** | **256** bits en `emblèmes+0x7D` | l'énumération entière, en sautant le type `0xD` |
| 4 | **la moyenne des trois** | — | — |

Les trois premiers partagent la même formule, et les constantes sont **lues
dans l'image**, pas déduites :

    pourcentage = (compte / total) * DAT_82003EDC        DAT_82003EDC = 100,0
    moyenne     = (p1 + p2 + p3)  * DAT_82003580         DAT_82003580 = 0,333333343
    valeur de depart                                     DAT_82000A34 = 0,0

Un raccourci du code à ne pas prendre pour une autre règle : quand
`compte == total`, les trois rendent `DAT_82003EDC` **directement**, sans
division. Même résultat, et cela évite un `100,00001`.

Et la formule du §9.21 (`compte * 0,001 * 100`) est le **cas particulier** du
rang 1, où le total vaut mille : elle n'est pas une autre règle.

**Le catalogue d'objets** du rang 2 a un pas de `0x50` octets — c'est
`chritm_tbl`, dont le §9.27 avait déjà mesuré que la disposition est la même
des deux côtés. `FUN_82310370` est le même compte, pris depuis la session.

**Deux variantes du rang 1**, même compte, autre liste :

- `FUN_82310098(profil, lieu, …)` — filtre par `FUN_8230E018(vec, 0, 1 << lieu)`,
  donc par `npc_tbl + 0x88` (le lieu, §9.21). C'est elle que le verdict
  emploie pour savoir si un lieu est fini ;
- `FUN_8230FE40(objet, …)` — sur un vecteur déjà constitué en `objet + 0xA8`.

### 14.4 L'ÉTOILE : c'est le bit `+0xF4`, et elle se dessine après le nom

Dans la boucle de ligne de la liste des joueurs :

```c
texte = 0x8208E508;                              /* "？？？？？" */
if (profil && bit(profil + 0x74, rival)) {       /* RENCONTRÉ */
    FUN_82310F48(…);  texte = nom_compose;       /* le vrai nom */
}
FUN_8223C048(…blanc…);  FUN_8223FE30(0x82000F08, texte);
…
if (profil && bit(profil + 0xF4, rival)) {       /* BATTU */
    FUN_8223BEB8(x - dVar15, y);                 /* décalage vers la GAUCHE */
    FUN_8223C048(0xFFFFFF00);                    /* ARGB : opaque, R=FF G=FF B=00 = JAUNE */
    FUN_8223FE30(0x820117C8);                    /* l'ÉTOILE */
}
```

Les deux bits ne commandent donc **pas** la même chose, et c'est la
distinction qui manquait : **`+0x74` décide du NOM** (sans lui, cinq points
d'interrogation), **`+0xF4` décide de l'ÉTOILE**. Le §9.21 avait la couleur
et la position ; voici le test.

### 14.5 Le bas de l'écran de statut, et ce qu'il n'est pas

`FUN_82310598` recopie encore six champs du profil :

| écran | profil | ce qu'on en sait |
|---|---|---|
| +0x70 | `profil + 0x04` | **la plus longue série** (le verdict l'écrit, §14.2). Au-delà de **99**, l'écran pose en plus le libellé **`0x423`** |
| +0x74 | `profil + 0x188` | un `u32` |
| +0x78 | `profil + 0x184` | un `u32` |
| +0x7C | `profil + 0x180` | un `u32` |
| +0x80 | `profil + 0x17C` | un `u32` |
| +0x87 | `profil + 0x03` | un octet |

**Aucune des 323 fonctions n'écrit `profil + 0x17C` à `+0x188`.** — **FAUX, et c'est le §14.11 qui le corrige : `FUN_8230B5F8` et `FUN_8230B660` les écrivent, depuis la sortie du sous-état 0x57. Le relevé par déplacement, puis les deux parcours, ne les atteignaient pas.** Le statut
les lit, et ce qui les tient vit **hors** du code propre au mode — à prendre
dans le moteur partagé, probablement avec les compteurs de victoires et de
défaites du jeu. C'est une absence **mesurée**, pas une lacune de lecture :
le relevé a porté sur les 102 fichiers du lot.

À ne pas confondre : `profil + 0x6C` et `+0x70` sont **deux décomptes**, que
`FUN_82315A10` décrémente à chaque victoire (et une ou trois fois de plus
selon `FUN_824D4820()`), et que les deux fonctions d'options du Quest
(`FUN_82315CC0` / `FUN_82315D00`) rangent et relisent. Leur rôle n'est pas
mesuré.

### 14.6 Ce que cela change pour le portage

Le point 2 du §9.30 est **lu**. Ce qu'il reste à ÉCRIRE dans FS, et rien de
plus :

1. un champ de 1 000 bits « battu » et un de 1 000 bits « rencontré » — notre
   `quest_profil.bin` les a déjà (`+0x010` et `+0x090`) ;
2. la série : un entier qui monte de 1 par victoire, s'écrête à 999, tombe à
   0 sur une défaite, et dont le maximum se garde à part. **Notre fichier
   porte `+0x110` « plus longue série » ; il lui manque la série COURANTE**,
   qui en 2007 est une globale (`DAT_82AD172C`) et non un champ sauvé ;
3. le test de victoire : le champ du vainqueur de la session, comparé à notre
   joueur ;
4. les trois comptes du statut, chacun un parcours de champ de bits — les
   emblèmes sont 256, pas 1 000 ;
5. l'étoile : un second dessin, décalé, jaune, sous le bit « battu » ;
6. la récompense de lieu complet, table `{8, 9, 6, 4, 5, 3, 7, —}`.

### 14.7 Ce que la suite a fermé, et ce qu'elle n'a pas pu (même séance)

#### « RENCONTRÉ » se pose bien dans le Quest — correction du §14.2

J'avais écrit « aucun des 323 n'y écrit par ce chemin — à chercher du côté de
l'écran de rencontre, non mesuré ». La seconde moitié était fausse : **deux**
des 323 le posent, et toutes deux du même geste, juste après
`FUN_8230DDF0(rival, 0x82AD1634)` — le copieur de `npc_tbl` du §9.26 :

```c
FUN_8230DDF0(rival, 0x82AD1634);          /* charge la fiche du rival */
…
profil = FUN_8230B5B8(DAT_82AD1618);
if (profil != 0) {
    FUN_821D1798(&{profil + 0x74, DAT_82AD162C}, 1);   /* RENCONTRÉ */
}
```

| fonction | rôle |
|---|---|
| `0x8231FEB8` | **milieu du sous-état 0x57** (`QUEST_VS`) : l'adversaire SUIVANT. `FUN_82315120(rival, 0)` le choisit, le bit se pose, puis `FUN_8220D1E0(0x56)` redemande la préparation |
| `0x82320150` | **l'entrée d'un combat du Quest**. `FUN_82320150(rival)`, et `rival == -1` en tire un au hasard (`FUN_822499E8(0) % 1000`) |

**Le bit se pose donc au CHARGEMENT du rival, pas après le combat.** C'est ce
que le §9.21 disait déjà (« en 2007 le bit se pose au combat ») et que je
n'aurais pas dû rouvrir. La décision de portage du §9.21 — ouvrir un lieu
marque ses rivaux — reste un choix à nous, et elle a maintenant un site
précis à remplacer.

**Et `FUN_82320150` remet la série à zéro** : `DAT_82AD172C = 0` dès son
entrée. **La série courante ne survit pas à un retour au menu** : elle ne vit
que le temps d'une suite de combats. C'est une quatrième règle, à ajouter aux
trois du §14.2.

Ses appelants : une liste de rivaux de pas `0x24`, indexée par un curseur en
`+0x50` (`quest_x360.c:5809`, `x360_menu_arcade.c:383`), et un appel **sans
argument** (`quest_x360.c:14252`), donc au hasard.

#### Les deux gardes : ce qu'elles sont, et pourquoi je ne les nomme pas

`FUN_82315930()` rend une adresse **fixe**, `0x82656B08`. Donc
`[gains + 0x30]` est la globale `DAT_82656B38`, et la garde de la série
s'écrit aussi `FUN_823163C8() = DAT_82656B38 != 0`.

Ce n'est **pas un booléen, c'est un MASQUE** :

    FUN_823178A0()  ->  (FUN_82316270() & DAT_82656B38) != 0

| globale | taille | accès trouvés | ce qu'elle commande |
|---|---|---|---|
| `DAT_8279829C` | octet | 2, **lectures** (`0x821E3BC0`, `0x821E4050`) | autorise tout le bloc du verdict |
| `DAT_82656B38` | masque | 6, **lectures**, toutes dans le bloc du Quest (`0x823163D0` … `0x823178B8`) | non nul : la série ne monte pas, et `FUN_82320150` prend une autre fin |

**Aucun écrivain trouvé pour l'une ni pour l'autre**, et c'est une limite de
l'instrument, pas une mesure : un balayage par base reconstruite (`lis`,
`lis+addi`, `lis+ori`, fenêtre de trente instructions) ne voit pas une
écriture faite par un **pointeur reçu en registre**. Le tournoi reste le
candidat pour `DAT_82656B38` — le §2 lui donne son propre sous-état, `0x55` —
et ce n'est **pas** établi.

#### `profil+0x17C` à `+0x188` : le balayage par déplacement ne peut pas répondre

Relevé sur l'image de 2007 : **65, 57, 64 et 49 écritures** pour les quatre
déplacements. En cherchant les **grappes** — au moins trois des quatre
touchés de près sur le même registre de base — on en trouve une dizaine, et
**la plupart ont `r1` pour base**, c'est-à-dire la pile : ce sont des cadres
de fonction, pas notre structure. Rien, dans un relevé par déplacement, ne
dit quel objet tient le registre.

C'est le second angle mort documenté de cette famille d'outils (en-tête de
`tools/champs_accesseur.py`). **Ce qui manque est un suiveur de pointeur côté
PowerPC** — l'équivalent de `champs_accesseur.py` pour la valeur rendue par
`FUN_8230B5B8`. Je laisse donc les quatre champs sans nom, et je nomme
l'outil à écrire plutôt que de désigner une grappe plausible.

#### UN PIÈGE D'OUTILLAGE, et il a failli fausser ce relevé

`tools/x360_ppc.py` porte **en dur**
`IMAGE = extracted/X360_FS/sel/default.img` : l'image Xbox 360 de **FINAL
SHOWDOWN**, et non celle de 2007 (`extracted/X360_VF5/vf5_x360.img`).
`tools/x360_champ.py` passe par `x360_ppc.Image()` et hérite du défaut ; seul
`tools/quest_x360.py` pointe sur 2007.

Les deux images ont la même base `0x82000000`. `xref 0x8279829C` a donc rendu
« 0 construction », et `func 0x821E3BB8` un épilogue de pile — **sans une
seule erreur**, parce que ces adresses existent dans les deux images et n'y
veulent pas la même chose. Tranché en décodant les mots bruts de l'image de
2007 à la main :

    0x821E3BB8  3d608279  lis  r11, 0x8279
    0x821E3BBC  396b7cdc  addi r11, r11, 0x7CDC     ; r11 = 0x82797CDC
    0x821E3BC0  886b05c0  lbz  r3,  0x5C0(r11)      ; = 0x8279829C
    0x821E3BC4  4e800020  blr

ce qui confirme Ghidra, et non le désassembleur. C'est la règle « une image ne
se nomme pas par son dossier », cette fois appliquée à un **outil**. Pour lire
2007 : passer le chemin à `x360_ppc.Image(chemin)` — elle l'accepte.

### 14.8 `tools/x360_suivre.py` : l'outil qui manquait, et ce qu'il a rendu

Le §14.7 disait « ce qui manque est un suiveur de pointeur côté PowerPC ».
Il est écrit, validé, et posé avec son lanceur `tools/x360_suivre.cmd`.

#### Ce qu'il fait

Le pendant Xbox 360 de `champs_accesseur.py` : il recense les
`bl <accesseur>` **par un balayage exact des mots** (op 18, LK à 1 — donc
aucun désassemblage linéaire, donc aucun déraillement), puis suit le pointeur
rendu dans `r3` vers l'avant en retenant ses **alias** (`mr rD, rS` et
`addi rD, rA, n`) **et son passage par la pile** — `stw r3, 0x50(r1)` … plus
loin `lwz r31, 0x50(r1)`. Sans la pile on perdrait la trace au premier appel,
c'est-à-dire tout de suite.

**Deux défauts corrigés en cours de route, et ils valent d'être écrits :**

1. la première version s'arrêtait au premier branchement. Or la première
   chose que fait tout appelant est `cmplwi cr6, r3, 0 ; beq …`, le test de
   nullité : elle s'arrêtait donc à la **deuxième instruction** de chacun des
   21 sites, et rendait « aucun accès » — un zéro qui avait l'air d'une
   mesure. Un conditionnel ne termine pas le chemin **non pris** ; seul un
   branchement inconditionnel (`b`, `blr`, `bctr`) le termine ;
2. capstone 5.0.7 ne rend **pas** les formes indexées comme un accès
   mémoire : `stbx r10, r5, r11` sort en trois registres. Sans ce cas on
   perdait tout parcours de tableau — et la boucle de quinze octets du
   profil en est un.

#### LA VALIDATION, et elle est triple

On ne se sert pas d'un outil neuf sans l'avoir confronté à du **déjà su** :

| ce qui était connu | ce que l'outil rend |
|---|---|
| les douze champs d'options du Quest (`FUN_82315CC0` charge, `FUN_82315D00` sauve) : `+0x10`, `+0x14`, `+0x18`…`+0x1B`, `+0x54`, `+0x63`…`+0x68`, `+0x6C`, `+0x70` | **chacun avec exactement une lecture et une écriture**, et l'écriture dans `0x82315D18` |
| `profil + 0x04`, la plus longue série, écrite par le verdict (§14.2) | `0x82320C7C ECRIT stw r11, 4(r30)`, **dans `FUN_82320A68`** |
| le champ de 256 bits des emblèmes en `socle + 0x7D` (§14.3) | 7 accès, 0 écriture |

Les trois tombent juste, et la troisième sur un **autre** accesseur. L'outil
résout aussi les alias arithmétiques (`stb r4, 0(r9)` rendu comme `+0x18`,
parce que `r9 = profil + 0x18`) et la boucle indexée de `+0x54`.

#### Le socle, et la vraie forme de l'objet

`FUN_8230B5B8` n'est qu'un décalage :

    FUN_8230B5B8()  =  FUN_822DAC40() + 0xC0      (0 si le socle est nul)

Donc tout vit dans **un seul objet**, celui de `FUN_822DAC40` :

| socle | profil | contenu |
|---|---|---|
| +0x7D | — | **les 256 bits des emblèmes** |
| +0xC0 | +0x00 | le début du profil |
| +0xC4 | **+0x04** | **la plus longue série** |
| +0x134 | +0x74 | **rencontré**, 1 000 bits |
| +0x1B4 | +0xF4 | **battu**, 1 000 bits |
| +0x23C…+0x248 | +0x17C…+0x188 | les quatre `u32` du bas du statut |

#### La carte du profil de 2007, mesurée, avec ses écrivains

| profil | écrivain | où |
|---|---|---|
| +0x01 | `0x8230D538  stb` | `0x8230D518` |
| +0x03 | `0x823181B8  stb` | `0x823181AC` |
| **+0x04** | `0x82320C7C  stw` | **le verdict, `FUN_82320A68`** |
| +0x08 | `0x8230D54C  stw` et `0x8230E8A8  stw` | deux sites |
| +0x0C | `0x8230E8B0  stw` | `0x8230E894` |
| +0x10 … +0x70 | `0x82315D18` | les options du Quest, douze champs |
| +0x00, +0x02, +0xF4, +0x174, +0x178 | — | lectures seules sur ce chemin |

`+0x174` et `+0x178` sont lus en `0x8231FCF8` et juste après, dans
`FUN_8231FAB8` — le **milieu du sous-état 0x56**, la préparation du combat,
et écrits en `0x8231FD8C` / `0x8231FD98` (§14.9). **Ce qu'ils portent était
déjà écrit au §9.29, et je ne l'avais pas rapproché : ce sont les
VICTOIRES et les DÉFAITES**, `fiche + 0x100` / `+0x104` persistés en
`profil + 0x174` / `+0x178`.

#### CE QUE L'OUTIL N'A PAS PU, ET IL FAUT LE DIRE

**Les quatre `u32` restent sans écrivain, et sans lecteur.** Ni les 21
appelants de `FUN_8230B5B8`, ni les 14 de `FUN_822DAC40`, ne donnent **un
seul accès** à `+0x17C`…`+0x188` / `+0x23C`…`+0x248` — pas même la lecture
que `FUN_82310598` fait pourtant, et que le §14.5 a lue dans le C.

Ce zéro ne dit donc rien du binaire : **il dit la portée de l'outil.**
`FUN_82310598` prend le profil au début et lit ces champs très loin en aval,
après des branchements inconditionnels, et un suiveur à **chemin unique** ne
peut pas y arriver. Augmenter la borne de parcours de 160 à 1 200
instructions n'a rien changé — les 25 mêmes champs : ce n'est pas la
longueur, c'est le chemin.

**Ce qu'il faudrait maintenant** est le même suiveur sur le **graphe de flot**
et non sur une ligne droite : suivre les deux côtés de chaque conditionnel, et
rejoindre les blocs par les cibles de branchement. C'est une deuxième version
de `x360_suivre.py`, pas un autre outil.

Donc : le §14.5 restait ouvert, mais sa cible était resserrée — quatre
`u32` consécutifs en `socle + 0x23C`, dans l'objet de `FUN_822DAC40`.
**La version sur graphe de flot l'a tranché : voir le §14.9.**

### 14.9 LE PARCOURS SUR GRAPHE : le §14.5 est tranché

`--graphe` est ajouté à `tools/x360_suivre.py`, **à côté** du parcours en
ligne droite, qui n'est pas touché et rend toujours ses 25 champs
(non-régression vérifiée). Il suit les deux côtés de chaque conditionnel,
traverse les `b`, et reste borné à la fonction appelante par `.pdata`
(`quest_x360.Image().fonctions()`).

Une chose qui n'est **pas** un risque ici, et autant l'écrire : désassembler
la fonction d'une traite. En PowerPC chaque instruction tient en un mot de
quatre octets aligné — aucun recalage n'est possible. La règle du
désassemblage linéaire qui déraille est une règle x86.

#### Un défaut qui valait d'être attrapé

Première version : la clé de visite portait les **valeurs** des alias. Une
boucle de copie incrémente son registre d'alias à chaque tour
(`addi r9, r9, 4`) ; l'état différait donc à chaque passage, rien n'était
jamais « déjà vu », et le parcours s'élargissait sans fin — **4 221
« champs »** pour le profil, un par octet, chacun avec une écriture. **Un
relevé qui avait l'air d'une mesure.**

En ne gardant dans la clé que les registres **suivis**, et non leurs valeurs,
le second tour d'une boucle est déjà vu et le parcours converge :
**30 champs**. Le prix est dit dans le code : un champ atteint seulement au
N-ième tour n'est pas rendu — le relevé reste un **minorant**, ce qui est le
contrat annoncé.

#### La validation du mode graphe est son DELTA

Par rapport à la ligne droite il ajoute **exactement cinq** champs, et les
cinq sont ceux qu'on attendait :

- **`+0x74`**, « rencontré » — que le §14.8 signalait absent ;
- **`+0x17C`, `+0x180`, `+0x184`, `+0x188`** — les quatre du statut.

Rien d'autre. Un outil qui ajoute juste ce qui manquait, et rien de plus, se
tient.

#### LA RÉPONSE, et c'est une mesure, plus une portée

| champ | accès | où |
|---|---|---|
| +0x174 | lu **et ÉCRIT** | `0x8231FCF8` lit, `0x8231FD8C` écrit — `FUN_8231FAB8`, le milieu du sous-état **0x56** |
| +0x178 | lu **et ÉCRIT** | `0x8231FD04` lit, `0x8231FD98` écrit — même fonction |
| **+0x17C** | **lu une fois, écrit jamais** | `0x82310784` |
| **+0x180** | lu une fois, écrit jamais | `0x8231076C` |
| **+0x184** | lu une fois, écrit jamais | `0x82310754` |
| **+0x188** | lu une fois, écrit jamais | `0x8231073C` |

Les quatre lectures viennent de l'appel `0x823105CC`, c'est-à-dire de
**`FUN_82310598`** — l'écran de statut, celui-là même que le §14.5 avait lu
dans le C. **Le parcours y arrive** : son silence sur l'écriture n'est donc
plus un défaut de portée.

Et le même parcours depuis le socle (`FUN_822DAC40`, 14 appelants, graphe
complet) ne rend que **trois** champs — `+0x00`, `+0x7D` (les emblèmes, neuf
lectures, **toutes indexées**, ce que seule la prise en charge des formes
`lwzx` permet de voir) et `+0xC2`. **Rien** en `+0x23C`…`+0x248`.

**Donc : les quatre `u32` sont LUS par l'écran de statut, et ÉCRITS par
personne qui passe par l'un ou l'autre accesseur.** Leurs deux voisins
immédiats, eux, le sont — par la préparation du combat.

#### Les deux pistes qui restent, et je ne tranche pas

1. un **chargement en bloc** de la sauvegarde. Le profil est une tranche
   d'une structure sauvée (`socle + 0xC0`), et un `memcpy` ne laisse aucune
   écriture champ par champ : cela expliquerait qu'un champ soit lu sans
   jamais être écrit ;
2. un **troisième accesseur** du même objet, non identifié.

La première est la plus simple. **Le §14.10 la suit : son mécanisme existe et est mesuré, mais le passeur manque encore.**

#### Ce que cela donne au portage, quelle que soit la piste

Ces quatre `u32` **ne sont pas calculés par le Quest**. **À CORRIGER : ils le sont. Voir le §14.11.** Si notre
`quest_profil.bin` doit les porter, c'est à nous de décider ce qu'ils
comptent : rien dans les 323 fonctions ne le dira. Les six premières lignes
du statut que le §9.21 laissait à zéro gardent donc leur statut — un choix de
portage, pas une lecture.

### 14.10 OÙ VIT LE PROFIL : un tableau statique de 30, et un bloc de 4 096 octets

La piste 1 du §14.9 — « un chargement en bloc » — se vérifie par le code de
l'accesseur. Elle est **confirmée dans son mécanisme**, et elle donne la carte
de l'objet entier.

#### L'accesseur n'alloue rien : il calcule

    FUN_822DAC40(i)  =  i * 0x10C0 + 0x829CAE30      si i < 0x1E
                        0                            sinon

Soit **un tableau STATIQUE de 30 enregistrements de `0x10C0` octets** (4 288),
`0x829CAE30` à `0x829EA4B0`. Rien n'est sur le tas, et c'est pour cela que le
§14.9 ne trouvait aucun écrivain « ailleurs » : il n'y a pas d'ailleurs.

L'origine se construit en **deux** `addi` —
`lis r11,0x829D ; addi r11,r11,-0x5438 ; addi r11,r11,0x268` — d'où
`0x829CABC8 + 0x268`. C'est pourquoi `glob2`, qui ne reconnaît qu'un seul
`addi` après le `lis`, rendait « 0 accès » sur `0x829CAE30` : encore un zéro
qui n'était pas une mesure.

#### Deux sites seulement indexent ce tableau, et le second donne la carte

Un enregistrement de `0x10C0` ne se touche que par `mulli rD, rA, 0x10C0`
(`0x10C0` n'est pas une puissance de deux). **L'image entière en porte deux :**

| site | fonction |
|---|---|
| `0x822DAC4C` | l'accesseur `FUN_822DAC40` |
| `0x822DAAD8` | **`FUN_822DAA70`, l'EFFACEMENT** — un seul appelant, `0x82307CC8`, dans le bloc du Quest |

Et l'effacement nomme les champs, parce qu'il les efface un par un
(`FUN_825FFC10` = mise à zéro) :

```c
FUN_825FFC10(base + i*0x2000 + 0x3F980, 0, 0x2000);   /* le blob de sauvegarde */
lVar3 = base + i*0x10C0;
FUN_825FFC10(lVar3 + 0x268, 0, 0x7D);     /* = accesseur +0x00  */
FUN_825FFC10(lVar3 + 0x2E5, 0, 0x20);     /* = accesseur +0x7D  */
FUN_825FFC10(lVar3 + 0x305, 0, 0x20);     /* = accesseur +0x9D  */
FUN_825FFC10(lVar3 + 0x328, 0, 0x1000);   /* = accesseur +0xC0  */
```

L'origine de l'accesseur étant `brut + 0x268`, la soustraction tombe juste et
les tailles **parlent d'elles-mêmes** :

| accesseur | taille | ce que c'est |
|---|---|---|
| **+0x00** | `0x7D` = 125 o = **1 000 bits** | un champ de mille bits. Lu **indexé** en `0x822EB560` (`lwzx`) |
| **+0x7D** | `0x20` = **256 bits** | **les emblèmes** — c'est le champ du §14.3, et l'effacement en donne la taille exacte. Neuf lectures, toutes indexées |
| **+0x9D** | `0x20` = 256 bits | un **second** champ de 256 bits. **Aucun accès relevé** : le Quest ne le lit pas |
| **+0xC0** | **`0x1000` = 4 096** | **LE PROFIL**, effacé d'un seul coup |

Les quatre `u32` du statut sont en accesseur `+0x23C`…`+0x248`, donc **dans ce
bloc de 4 096 octets**, qui est traité en une seule opération.

#### L'API de sauvegarde, et ce qu'elle est

Les six appelants de `FUN_822DA548` (le fournisseur de base) dessinent une API
qui ne porte pas sur les enregistrements, mais sur **un blob de `0x2000`
(8 192) octets par joueur**, en `base + 0x3F980 + i*0x2000` :

| fonction | ce qu'elle fait |
|---|---|
| `FUN_822DA8B8(p, i)` | rend l'adresse du blob du joueur `i` |
| `FUN_822DA938(p, dst, n)` | **lit** le blob : `memcpy(dst, blob, n)`, `n <= 0x2000`. Si le créneau vaut `0x1E`, elle met `dst` à zéro au lieu de copier |
| `FUN_822DA9E0(p, src, n)` | **écrit** le blob : `memcpy(blob, src, n)` |
| `FUN_822DAB40()` | « la sauvegarde est-elle disponible ? » |

`FUN_825FFD30` est donc le `memcpy` et `FUN_825FFC10` le `memset`. Et
**`0x1E` — 30 — est la sentinelle « pas de créneau »**, la même borne que
l'accesseur : trente créneaux, le trente-et-unième veut dire « aucun ».

#### CE QUE JE NE DÉCLARE PAS

Le mécanisme d'un traitement en bloc **existe et est mesuré** : un blob de
8 192 octets par joueur avec un `memcpy` dans les deux sens, et un profil de
4 096 octets effacé d'un seul `memset`. Un champ lu sans être jamais écrit
champ par champ est cohérent avec cela.

Mais **le passeur entre le blob de `0x2000` et l'enregistrement de `0x10C0`
n'est pas identifié** : les deux copieurs travaillent vers un tampon fourni
par l'appelant, pas vers l'enregistrement. Tant que ce passeur n'est pas lu,
« les quatre `u32` viennent de la sauvegarde » reste une **piste cohérente,
pas une mesure**. La chercher, c'est trouver qui appelle `FUN_822DA938` avec
l'adresse d'un enregistrement.

#### Ce que cette séance a tout de même tranché

- le profil n'est pas un objet alloué mais **une tranche d'un tableau
  statique de trente créneaux**, ce qui ferme la question « où vit-il » ;
- trois champs de bits sont nommés avec leur **taille exacte**, dont un
  second champ de 256 bits que personne ne lit ;
- et pour le portage — **ce que je concluais ici est faux, le §14.11 le
  reprend** : les quatre `u32` SONT calculés par le Quest, par deux
  méthodes appelées à la sortie du combat.

### 14.11 LES QUATRE `u32` SONT TROUVÉS : deux paires, et le §14.5 est fermé

Le §14.10 disait : « le chercher, c'est trouver qui appelle `FUN_822DA938`
avec l'adresse d'un enregistrement ». C'était la mauvaise porte — et en la
poussant on a trouvé la bonne.

#### La mauvaise porte, et ce qu'elle a quand même appris

Les copieurs du blob ont **trois** appelants en tout, et tous les trois
échangent **`0x808` octets** (2 056), pas `0x1000` :

    FUN_821F6220 : FUN_822DA938(p, objet + 0x2070, 0x808)      lit
    FUN_821F64F8 : FUN_822DA938(p, objet + 0x40,   0x808)      lit
    FUN_821F65C8 : FUN_822DA9E0(p, [0x82650820 + p*4] + 0x1058, 0x808)  ecrit

Le tampon est **un autre objet** (table de pointeurs en `0x82650820`), et la
taille n'est pas celle du profil. **Il n'y a donc pas de passeur blob →
enregistrement**, et la piste du « chargement en bloc » du §14.9 tombe. Les
trois appelants du Quest de `FUN_822DA8B8` ne s'en servent que comme **test
d'existence du créneau** (`!= 0`), jamais pour lire le contenu.

#### La bonne porte : le pointeur part EN ARGUMENT

Le tableau est statique et deux sites seulement l'indexent (§14.10). Donc
tout autre code qui touche un enregistrement **reçoit** le pointeur — et un
`bl` oublie `r3` à `r12`, si bien qu'une écriture faite **dans l'appelée**
est invisible aux deux parcours. C'était le dernier trou, et il se nommait.

`x360_suivre.py` relève désormais ces passages (`PASSE ARG rN vers 0x…`).
Sur le profil, treize passages, dont deux qui partent de **`0x82320F68` — la
sortie du sous-état `0x57`** vers `0x8230B5F8` et `0x8230B660`, voisines
immédiates de l'accesseur. Les voilà :

```c
void FUN_8230B5F8(profil, n)              /* LA SOMME */
{
    if (n < 0) n = 0;
    if (profil[0x03] == 0) {
        profil[0x180] += n;  if (0x7FFFFFFE < …) profil[0x180] = 0x7FFFFFFF;
    }
    profil[0x188] += n;      if (… >= 0x7FFFFFFF) profil[0x188] = 0x7FFFFFFF;
}

void FUN_8230B660(profil)                 /* LE COMPTE */
{
    if (profil[0x03] == 0) {
        profil[0x17C] += 1;  if (999999 < …) profil[0x17C] = 999999;
    }
    profil[0x184] += 1;      if (… >= 999999) profil[0x184] = 999999;
}
```

#### CE QUE SONT LES QUATRE CHAMPS

**Ce ne sont pas quatre compteurs : ce sont DEUX paires**, la même grandeur
tenue deux fois — une fois sous condition, une fois sans.

| profil | statut | sens | plafond |
|---|---|---|---|
| **+0x17C** | +0x80 | un **compte**, +1 par combat, **si `profil[0x03] == 0`** | **999 999** |
| **+0x180** | +0x7C | une **somme** de `n`, **si `profil[0x03] == 0`** | `0x7FFFFFFF` |
| **+0x184** | +0x78 | le **même compte**, **sans condition** | 999 999 |
| **+0x188** | +0x74 | la **même somme**, **sans condition** | `0x7FFFFFFF` |

Et `profil[0x03]` est précisément l'octet que l'écran de statut recopie en
`+0x87` (§14.5) : il affiche donc **le drapeau et les deux paires**, ce qui
donne au relevé une cohérence qu'aucune des deux lectures n'avait seule.

#### La quantité sommée, et une garde qui s'éclaire

La sortie du sous-état `0x57` la compose :

```c
if (FUN_821E3BB8() == 0)                       /* DAT_8279829C, L'INVERSE */
    DAT_82AD1730 += FUN_821DDE10(session);     /* [session+0xAEC] - [session+0xAF0] */
profil = FUN_8230B5B8(joueur);
FUN_8230B5F8(profil, DAT_82AD1730);
FUN_8230B660(profil);
```

**Le §14.2 avait laissé `DAT_8279829C` sans nom ; sa nature se lit ici.** Le
verdict (`FUN_82320A68`) fait son accumulation sous `!= 0` ; cette sortie la
fait sous `== 0`. **Les deux conditions sont complémentaires** : ce n'est donc
pas une garde qui peut tout bloquer, c'est un **aiguillage** entre deux
chemins d'après-combat, et l'accumulation a lieu exactement une fois dans les
deux cas. Ce que l'octet distingue n'est pas mesuré ; qu'il distingue, l'est.

`FUN_821DDE10(session)` reste `[session+0xAEC] - [session+0xAF0]` — une
différence par combat, sommée sur la vie du profil. Je ne la baptise pas :
**le §14.12 borne la question, et montre que les cinq écritures de ces deux
champs posent ZERO.**

#### La remise à zéro confirme toute la carte

`FUN_8230B6B8(profil)`, atteinte depuis `0x823005E4`, remet le profil à neuf,
et chaque geste recoupe ce qui précède :

- elle met à zéro **`+0x17C`, `+0x180`, `+0x184`, `+0x188`** — les quatre ;
- `[+0x00] = 1`, `[+0x01] = 1`, `[+0x02] = 0`, `[+0x03] = 0` ;
- elle remplit **`+0x54`…`+0x62` de `0xFF`** et pose `+0x6C` et `+0x70` à
  `-1` — ce sont les champs d'options du §14.8, et `0xFF`/`-1` y veut dire
  « non réglé » ;
- et elle efface **deux régions de 132 octets, en `+0x70`…`+0xF0` et
  `+0xF0`…`+0x170`** : ce sont exactement les deux champs de **mille bits**,
  `rencontré` en `+0x74` et `battu` en `+0xF4` (125 octets chacun). La
  disposition du §9.21 est confirmée par son effaceur.

#### Le §14.5 est fermé, et ce que cela donne au portage

Les quatre `u32` sont **calculés par le Quest**, contrairement à ce que le
§14.9 et le §14.10 concluaient faute de pouvoir les atteindre. **Je corrige
cette conclusion.** Elle était juste sur les faits relevés et fausse sur
l'inférence : « aucun écrivain atteint » n'autorisait pas « aucun écrivain ».
C'est la borne de l'outil qui parlait, et il fallait un troisième relevé pour
la franchir.

Pour `quest_profil.bin`, cela fait **cinq** compteurs à tenir, pas un :

| notre fichier | 2007 | règle |
|---|---|---|
| `+0x110` plus longue série | `profil+0x04` | maximum de la série courante (§14.2) |
| à ajouter | `profil+0x17C` | +1 par combat si le drapeau est nul, plafond 999 999 |
| à ajouter | `profil+0x180` | somme de la différence du combat, même condition |
| `+0x114` nombre de combats | `profil+0x184` | +1 par combat, sans condition |
| à ajouter | `profil+0x188` | somme sans condition |

Et la série **courante** reste une globale, pas un champ sauvé (§14.7).

### 14.12 LA QUANTITÉ SOMMÉE : je ne la nomme pas, et voici pourquoi c'est une mesure

Le §14.11 laissait `FUN_821DDE10(session) = [session+0xAEC] - [session+0xAF0]`
sans nom. Ce qui suit ne le lui donne pas, mais borne la question — et sort
deux acquis au passage.

#### Ce n'est pas de l'argent, et le plafond le dit

Le §10.1 a mesuré que l'argent vit **ailleurs** : fiche de joueur de `0x528`,
`+0xEC`, plafonné à **999 999**. Les deux sommes du §14.11 sont plafonnées à
**`0x7FFFFFFF`**. Deux plafonds différents, deux grandeurs différentes : la
piste « c'est le gain du combat » est **écartée**, sans avoir à lire une ligne
de plus.

(Les deux **comptes**, eux, plafonnent bien à 999 999 — le même nombre que
l'argent. C'est le plafond d'affichage à six chiffres de ce jeu, pas un
indice de parenté.)

#### Les six accès, et le piège du déplacement partagé

Le balayage du déplacement sur l'image de 2007 donne **six accès à `+0xAEC` et
six à `+0xAF0`, toujours en paire, sur des instructions adjacentes** :

| site | ce que c'est |
|---|---|
| `0x821DC8A4` / `A8` | **`FUN_821DC7D0`**, la remise à zéro de la session |
| `0x821DDA4C` / `50` | un constructeur (`param_1[699] = 0 ; [700] = 0`) |
| `0x821DDAC8` / `CC` | un second constructeur |
| `0x821DDE10` / `14` | **la LECTURE**, et c'est notre différence |
| `0x821DF73C` / `40` | un troisième constructeur |
| `0x8228B1C0` / `C4` | **un AUTRE objet** — voir ci-dessous |

Le dernier a failli m'égarer : il relève la paire en **un seul mot de 64
bits**, la ET avec `[param_1+0x27A0]` et la passe à un testeur. Ce serait un
masque, pas un score. Mais son objet porte des champs jusqu'à `+0x27A0`, alors
que **notre** classe (vtable `PTR_FUN_8200F6D0`) contient deux fiches de
`0x528` et s'arrête vers `+0xAFC`. **Deux classes différentes au même
déplacement**, et c'est l'angle mort connu du balayage par déplacement — celui
que le §14.7 avait déjà rencontré avec `r1`.

#### LA MESURE, et la réserve qui va avec

Sur les cinq écritures de notre classe, **les cinq posent ZÉRO**. Ce sont des
constructeurs et une remise à zéro. Et la paire est lue **une seule fois**,
par `FUN_821DDE10`, comme une différence.

Donc, sur tout ce qu'un relevé par déplacement peut voir : **`FUN_821DDE10`
rend `0 - 0`**, et les deux sommes du profil accumuleraient zéro à chaque
combat.

**Je n'en conclus pas qu'elles valent zéro**, et la leçon du §14.11 est encore
chaude : « aucun écrivain vu » n'est pas « aucun écrivain ». Il reste une
sortie exacte — un rangement **indexé** (`stwx rS, rA, rB`), où le
déplacement n'apparaît pas dans l'instruction. Le §14.11 a été trouvé par un
troisième relevé ; celui-ci en demanderait un quatrième, par les formes
indexées sur cette classe.

**Ce que cela vaut pour le portage, et c'est opérationnel :** ne pas porter
`FUN_821DDE10` comme s'il portait une valeur. Si on écrit les deux sommes
`profil+0x180` / `+0x188`, il faut décider ce qu'elles additionnent — comme
pour les quatre champs, et pour la même raison.

#### Deux acquis qui ne se cherchaient pas

**1. La sentinelle du vainqueur.** `FUN_821DC7D0` pose `[session+0xACC] = 2`.
Or `+0xACC` **est** le champ du vainqueur (§14.11 : `FUN_821DD368` le rend).
Les joueurs valent 0 et 1 ; **2 veut donc dire « pas encore de vainqueur »**.
Le test de victoire du §14.2 — `[session+0xACC] == DAT_82AD1618` — ne peut
donc être vrai qu'après qu'un vainqueur a été posé, et il est faux par
construction en début de combat. C'est la garde qui manquait à la lecture du
§14.2.

**2. La classe de session, et sa taille.** `FUN_821DF6E0` la construit : deux
sous-objets de **`0x528`** à partir de `+0x68` (pas de `0x14A * 4`), ce qui
sont **les deux fiches de joueur du §10.1** — celles qui portent l'argent en
`+0xEC`. La session est donc le conteneur des deux fiches, et
`FUN_821DC7D0` en donne la carte, de `+0x00` à `+0xAF8` : les sentinelles à
`-1` (`+0x18`, `+0x1C`…`+0x2C`, `+0xAD8`, `+0xADC`, `+0xAF8`), les compteurs
à `0x15` (21) en `+0x10` et `+0x14`, et `+0xAF4 = 2`.


## 15. LE SON DU QUEST : le joueur de bruitages est identifié (2026-10-18)

Relevé en répondant à « est-ce que la gestion du son est prise en compte ? ».
La réponse était **non** — le son n'apparaissait dans ce document qu'une
fois, dans la liste des 179 services partagés du §3. Voici le premier
morceau, et il est petit mais net.

### 15.1 La musique : déjà faite

`tools/musique_quest.py` la porte, et elle est **lue**, pas choisie :
`sound/bgm/vf5ps3_b03map.adx`, demandée par `TaskQuestMap` (`0x8230CBC0`),
`TaskQuestHomeMenu` (`0x8230B7D0`) et `TaskQuestTenpo` (`0x82315500`).
Aucun autre morceau n'est demandé par ces trois-là. Côté FS, le moteur la
joue par `0x180185DA0(voie, chemin, 0)` et l'arrête par `0x180186D40(voie)`.

**Mais le mode entier en demande QUATRE : le §17.8 en trouve trois de plus,
celles des tournois.**

### 15.2 Les BRUITAGES : le joueur est `FUN_822B3840(voie, nom)`

`FUN_822D1198`, la fonction la plus appelée du Quest après le répartiteur
d'états — **23 appels** —, ne fait qu'une chose :

    void FUN_822D1198(void) { FUN_822B3840(0, 0x820846B0); }

et `0x820846B0` porte la chaîne **`vfv_ps3_ok`**. C'est donc **le bruitage de
validation**, et `FUN_822B3840(voie, nom)` est **le joueur de bruitages par
NOM** — pas par identifiant. Les noms sont des chaînes de l'image, donc
l'inventaire complet des bruitages du Quest se relève en listant les appels
de `FUN_822B3840` dans les 323 fonctions et en lisant leur argument.
**C'est fait : voir le §15.4.**

À ne pas confondre avec `FUN_8220D1E0(mode)` — 56 appels, le plus fréquent de
tous — qui n'est pas du son : `DAT_827A7E80 = mode ; DAT_827A7E88 = 1`, soit
**la demande de changement d'état** du §9.4, confirmée ici par son code.

### 15.3 Ce qui reste du son

1. l'inventaire des bruitages (lister `FUN_822B3840`, lire les noms) ;
2. la correspondance des noms avec FS : `vfv_ps3_ok` est un nom **de la
   version PS3 de 2007**. Rien ne dit que FS porte la même banque sous les
   mêmes noms — c'est à mesurer, comme l'a été la table des objets ;
3. le joueur côté FS : l'équivalent de `FUN_822B3840`, non identifié.

### 15.4 L'INVENTAIRE EST FAIT, et il est tout petit

Relevé sur l'image de 2007 par un balayage exact des branchements vers le
joueur, avec propagation de constantes pour reconstruire `r4`.

`FUN_822B3840` a **25 sites** : 21 `bl` et **4 sauts** (`b`). Dix noms
résolus, onze non — ceux-là sont tous en `0x8229xxxx`, dans le code de combat,
où `r4` vient d'une variable et non d'une constante. **Je ne les devine pas.**

#### Les deux enveloppes, et c'est tout le vocabulaire d'interface

La zone `0x82084660`-`0x820846F0` ne porte que **deux** noms de bruitage, et
chacun a son enveloppe de quatre instructions :

| enveloppe | voie | nom | chaîne | appels dans le Quest |
|---|---|---|---|---|
| `FUN_822D1198` | 0 | **`vfv_ps3_ok`** | `0x820846B0` | **23** |
| `FUN_822D11A8` | 0 | **`vfv_ps3_cancel`** | `0x820846BC` | **23** |

Vingt-trois et vingt-trois : la validation et l'annulation, à parité. C'est
la totalité des bruitages d'interface du mode.

#### Et un seul appel direct dans tout le Quest

| site | fonction | nom |
|---|---|---|
| `0x823078C0` | `0x82307870` (172 octets) | **`sy_charin00st_200`** |

Les autres noms résolus (`fd_LANDING_GROUND_LAU`, `fd_guard_off`,
`fd_success`, `fd_vfxse_sabaki1`, `fd_vfxse_sake2`, `sy_charin00st`,
`vfv_ps3_main_menu_close_51`) appartiennent au combat et aux menus du jeu,
pas au Quest.

#### Donc le son du Quest, en entier

1. une **musique** : `vf5ps3_b03map.adx` (§15.1), déjà portée ;
2. **deux bruitages d'interface** : `vfv_ps3_ok` et `vfv_ps3_cancel` ;
3. **un** bruitage de plus : `sy_charin00st_200`, dans une fonction du
   sélecteur de données.

**Porter le son du Quest, c'est donc poser un fichier de musique et câbler
deux bruitages.** Ce chantier est beaucoup plus petit que ce que le §15.3
laissait craindre, et la réserve sur la correspondance des noms avec FS tient
toujours : trois noms à retrouver, pas une banque.

#### Trois défauts d'outil, parce qu'ils se répéteront

Le premier relevé rendait **« 0 nom »**, trois fois de suite, et chaque fois
pour une raison différente. Aucune n'a levé d'erreur :

1. **les enveloppes SAUTENT, elles n'appellent pas.** Ne chercher que `bl`
   (LK=1) les ratait toutes. Il faut `b` **et** `bl` ;
2. **la partie haute de l'adresse se construit dans un AUTRE registre** :
   `lis r11, hi ; addi r4, r11, lo`. Exiger que le `lis` cible `r4` ne
   résolvait rien. Il faut une vraie propagation de constantes ;
3. **capstone arrête son flux au premier mot indécodable.** La fenêtre avant
   `0x822D11A4` s'arrêtait en `0x822D1190`, alors que l'enveloppe commence en
   `0x822D1198` : le mot `0x822D1194` n'est pas décodé (jeu Xenon), et
   `md.disasm` est un générateur qui ne reprend pas après. On perdait la
   moitié de la fenêtre. **En PowerPC on décode MOT PAR MOT** — chaque
   instruction tient en un mot aligné, donc un mot illisible ne doit coûter
   que lui-même.

Trois zéros qui avaient l'air de mesures. C'est le même piège qu'au §14.9 avec
les 4 221 champs, et qu'au §14.7 avec le `xref` sur la mauvaise image.


## 16. LES POINTS RESTANTS DU §9.30 (2026-10-18)

Reprise des points que le §9.30 laissait, dans l'ordre. Le son est au §15.

### 16.1 Point 3 — l'écran de rencontre et la réplique du rival

**Le chemin des données est complet, et il confirme le §9.27 par son
écrivain.** `FUN_82320300`, le constructeur du descripteur de combat, recopie
le bloc de travail du rival (`0x82AD1634`) champ par champ :

```c
FUN_822C4BA0(pile + 0x59, 0x82AD1634, 0x1F);   /* le NOM, 31 octets      */
FUN_822C4BA0(pile + 0x81, 0x82AD1653, 0x28);   /* REPLIQUE 1, 40 octets  */
FUN_822C4BA0(pile + 0xA9, 0x82AD167B, 0x28);   /* REPLIQUE 2, 40 octets  */
…
FUN_826001B8(pile + 0x138…, 0x82AD16B0, 0x30); /* les 24 u16, liste 1    */
FUN_826001B8(pile + …,      0x82AD16E0, 0x30); /* la liste 2             */
```

Les offsets `+0x59`, `+0x81`, `+0xA9` et les tailles `0x1F`/`0x28`/`0x28`
sont **exactement** ceux que le §9.27 avait relevés sur les écritures. La
carte est donc vérifiée deux fois, par deux chemins.

#### Le NOM est affiché, et à trois endroits

Cinq sites prennent l'adresse de `+0x59`, **tous dans le bloc du Quest** :

| site | fonction | ce qu'il en fait |
|---|---|---|
| `0x82308DD0` | `FUN_82308C90` | `FUN_8223FE30(0x82000F08, fiche + 0x59)` — **le dessine**, avec le même dessinateur que les noms de la liste des joueurs (§14.4) |
| `0x8231B14C`, `0x8231B538` | `FUN_8231AF98` | une liste : pour un joueur enregistré le nom vient de `FUN_82235F28(…) + 0x59` ; pour un PNJ, la fonction **recopie l'enregistrement de `npc_tbl` sur sa pile** (`FUN_8230DDF0`) et dessine le `+0x00` |
| `0x8231CF54` | `FUN_8231CD98` | — |
| `0x82320E88` | `FUN_82320E08` (**entrée du sous-état 0x57**) | `FUN_8218ABE8(…, fiche + 0x59)` — le nom part dans la **préparation des deux fiches de combat**, celle que le §2 avait nommée |

#### LES RÉPLIQUES, elles, ne sont lues par PERSONNE dans le Quest

Balayage de toute l'image sur les prises d'adresse `addi …, 0x81` et
`addi …, 0xA9` : **13 et 17 sites, et ZÉRO dans le bloc du Quest.** Les
répliques sont donc **recopiées dans le descripteur et jamais relues** par le
code propre au mode.

`FUN_8231AF98` est la preuve la plus nette : elle met à zéro trois tampons de
pile de **31, 40 et 40 octets** — le nom et les deux répliques —, remplit le
tout par `FUN_8230DDF0`, et **ne dessine que le nom**.

**Donc l'écran de rencontre avec la réplique n'existe pas dans ce code**, ou
il la fait dessiner par le moteur depuis le descripteur. Les 13 et 17 sites
hors du Quest sont du code moteur au même déplacement, et le §14.12 vient de
rappeler ce que vaut cette coïncidence : rien, sans suivre le pointeur. **Ce
qui reste** est de suivre le descripteur dans le moteur — les 42 sites qui
l'indexent (`mulli × 0x528`), dont `0x823551A8` qui en recopie 1 320 octets
d'un coup.

### 16.2 Point 5 — la table des récompenses des quinze événements

Le §10.3 butait sur `FUN_82315890`, « pas dans le lot décompilé ». Elle fait
une ligne :

    FUN_82315890(n)  =  n * 0x34 + 0x82656798          pour n de 0 a 14

**La table est donc statique : 15 enregistrements de `0x34` (52) octets en
`0x82656798`**, 780 octets, dont 252 non nuls. Treize `u32` par événement, et
elle se lit :

| mot | événements 0-6 | événements 7-14 | lecture |
|---|---|---|---|
| **0** | **528 … 534** | **641 … 648** | un **identifiant de libellé** |
| 1-9 | voir ci-dessous | zéros puis trois valeurs | **la matrice 3 × 3** du §10.3 |
| 10 | `0x10030F00`, `0x08052D00`… | `0x08032D00`, `0x10032D00`, `0x20032D00` | quatre octets |
| **11** | **1, 2, 4, 8, 16, 32, 64** | **255** | **un MASQUE de LIEU** |
| 12 | `0x13000000` | `0x000F0000`, `0x011E0000`, `0x04320000`… | deux octets utiles |

**Deux recoupements ferment la lecture du mot 0 et du mot 11 :**

- les libellés **528 à 534** sont, mot pour mot, ceux que le §9.21 avait
  relevés comme **les sept lieux nommés** (« le sous-titre se prend dans
  {528…534, 556} »). Les événements **0 à 6 sont donc les sept lieux** ;
- le mot 11 porte **une puissance de deux par événement** — 1, 2, 4 … 64 —
  c'est-à-dire `1 << lieu`, le même schéma que `FUN_8230E018(vec, 0, 1 << lieu)`
  du §9.21 et que `FUN_82310098` du §14.2. Les événements 7 à 14 portent
  **255**, soit *tous les lieux*.

Et la matrice du §10.3 (`(c*3 + i + 1) * 4`, c de 0 à 2) se lit directement :

| événement | récompense 0 | récompense 1 | récompense 2 |
|--:|---|---|---|
| 0 | 0 / **2000** / 1000 | 0 / 1000 / 600 | 30000 / 16000 / 10000 |
| 2 | 0 / **2000** / 1000 | 0 / 1000 / 600 | 20000 / 10000 / 6000 |
| 13 | 0 / 0 / 0 | 0 / 0 / 0 | **0 / 0 / 0** |

**Le « 2 000 G » du cahier des charges est trouvé** : c'est le mot 2, la
deuxième valeur de la première récompense, et il vaut 2000 pour les sept
événements de lieu. Le §10.3 disait « on ne l'écrit donc pas : on la lira
quand on la lira » — **c'est lu.**

Et l'événement **13** a ses neuf valeurs à **zéro**, ce qui s'accorde avec la
règle du §10.3 `if (n == 0x0D) valeur = 10000` : sa récompense n'est pas dans
la table, elle est en dur.

**Ce que je ne lis pas** : les mots 10 et 12. Le mot 10 porte des octets
réguliers (`0x0F` = 15 et `0x2D` = 45 reviennent, et 45 est la durée d'un
combat) et le mot 12 des couples croissants ((0,15), (1,30), (4,50), (8,70),
(10,80), (12,90), (14,100), (16,10)) qui ressemblent à des **conditions de
déclenchement**. Ressembler n'est pas être : non mesuré. **Le §17.10 lit le premier octet du
mot 12 — c'est un TYPE d'événement — et confirme le mot 11 par un second
lecteur. Et le §17.14 INTERPRETE la matrice : trois barèmes de prix x trois
places.**

### 16.3 Point 7 — la colonne « dan » de la liste des joueurs

Trouvée, et c'est une composition AET, pas un texte.

`FUN_82310F48(page, ligne, grade, priorité, noms)` — celle que le §14.4
voyait appeler quand le rival est « rencontré » — construit un objet AET :

```c
apcStack_f0[0] = "dan_icon1p";
apcStack_f0[1] = "dan_icon2p";
pcStack_dc  = apcStack_f0[DAT_820036C0[joueur]];   /* 1P ou 2P */
uStack_e0   = 0xE2;                                /* la scene */
uStack_d8   = uStack_d4 = FUN_821D4680(grade);
uStack_c4   = 2;                                   /* calque 2D = 2  */
uStack_b4   = 9;                                   /* mode 9         */
FUN_82166CC0(&uStack_e0);
```

`calque 2D = 2` et `mode 9` sont **exactement** l'idiome des fenêtres du
Quest relevé au §9.20. Et la valeur vient d'une table :

    FUN_821D4680(n)  =  PTR_DAT_8264FF90[n & 0xFF]

**`0x8264FF90` est une table de pointeurs de chaînes, et elle porte 42
entrées** — l'entrée 42 pointe sur « bad allocation », une chaîne étrangère :
la table s'arrête à 41. **Quarante-deux, soit exactement l'échelle de rang du
§9.29.**

Les chaînes sont les **nombres eux-mêmes** (« 0 », « 1 », … « 41 »), ce qui
est cohérent avec un **nom de calque** passé à la composition plutôt qu'avec
un texte dessiné.

**Une bizarrerie mesurée, que je ne m'explique pas :** de l'indice 0 à 20 la
table est l'identité, mais **à partir de 21 les triplets sont inversés** —
21→« 23 », 22→« 22 », 23→« 21 », puis 24→« 26 », 25→« 25 », 26→« 24 », et
ainsi jusqu'à 39→« 41 », 40→« 40 », 41→« 39 ». Sept triplets retournés. Si
on porte cette colonne, **il faut porter la table, pas la formule.**

### 16.4 Point 6 — les tournois : NON FAIT, et voici son périmètre

Je ne l'ai pas analysé, et je ne le maquille pas. Ce qui est **déjà** établi
ailleurs, et qui en dessine le périmètre :

- le **sous-état `0x55`** (`QUEST_TOURNAMENT`), entrée `0x82319B58`, sortie
  `0x82319B90`, sans fonction de milieu (§2) ;
- **neuf classes** : `TaskTournament`, `…Announce`, `…Audience`, `…Entry`,
  `…List`, `…MatchInfo`, `…MessageInfo`, `…Opening`, `…ResultInfo` (§3) ;
- les planches `tnt` / `tnto` sont **déjà déclarées** dans les bases de FS
  (§9.30 point 6) ;
- le **dôme est le lieu des tournois**, et c'est le huitième lieu, celui qui
  ne donne aucune récompense de complétion (§9.21, §14.2) ;
- le lot des tournois annoncé au cahier des charges (2 000 / 10 000 G) est
  maintenant **lu** : §16.2 ;
- et `FUN_8231AF98`, rencontrée au §16.1, dessine une liste de combattants
  mêlant joueurs enregistrés et PNJ — c'est **un candidat pour le tableau de
  tournoi**, non vérifié.

L'estimation du §6 reste de **trois séances** pour ce chantier. **Il est
commencé : voir le §17, qui pose la machine.**


## 17. LES TOURNOIS : le sous-état 0x55 et les neuf classes (2026-10-18)

Le §16.4 posait le périmètre sans l'analyser. Voici la machine.

### 17.1 Le sous-état 0x55 ne fait qu'UNE chose

```c
FUN_82319B58()  { FUN_822C8AA0(0x82AD0830, "QUEST_TOURNAMENT"); return 1; }  /* entree */
FUN_82319B90()  { FUN_822C7D50(0x82AD0830);                     return 1; }  /* sortie */
```

`0x8208ECD8` n'est pas une vtable : c'est **la chaîne « QUEST_TOURNAMENT »**.
Le sous-état crée donc **une tâche, par son NOM**, à l'objet **statique
`0x82AD0830`**, et la détruit en sortant. C'est le même mécanisme que la
tâche `QUEST_VS` du §2 — une usine à tâches indexée par un nom.

Il n'y a **pas** de fonction de milieu pour `0x55` (§2 le notait) : tout le
travail est dans les méthodes de la tâche.

### 17.2 La forme des neuf vtables : SIX méthodes, et le nom juste après

Les vtables portent **six** pointeurs, suivis immédiatement du nom de classe
en clair — ce qui explique qu'un dump trop long y lise des « adresses »
partagées qui ne sont que des octets de chaîne (`TOUR`, `NAME`, `NT_L`…).
Je m'y suis fait prendre une fois.

| classe | 0 | 1 | 2 | 3 | 4 | 5 |
|---|--:|--:|--:|--:|--:|--:|
| `TaskTournament` | 80 | 92 | 288 | 44 | *(feuille)* | **stub** |
| `…Announce` | 104 | 172 | 116 | 68 | **1712** | stub |
| `…Audience` | *80, partagée* | 124 | 336 | 68 | **stub** | stub |
| `…Entry` | 96 | 96 | 116 | 40 | **1644** | stub |
| `…List` | 136 | 156 | 300 | 328 | **976** | stub |
| `…MatchInfo` | 104 | 196 | 520 | 92 | **1080** | stub |
| `…MessageInfo` | 104 | 392 | 308 | 96 | **1268** | stub |
| `…Opening` | *80, partagée* | 124 | 160 | 128 | **stub** | stub |
| `…ResultInfo` | 104 | 204 | 280 | 64 | **480** | stub |

Les rangs sont **identifiés par lecture**, sur `TaskTournament` :

| rang | rôle | preuve |
|--:|---|---|
| 0 | **destructeur** | `FUN_8231B8D0() ; si (arg & 1) FUN_82142F48(objet)` — l'idiome du `delete` |
| 1 | **init** | pose `+0x4C = 0`, `+0x50 = 0`, `+0x54 = 0`, `+0x5C = 0`, **`+0x58 = 0x54`**, `+0x464 = 0`, et `+0x45C &= 0xF4` |
| 2 | **update** | un `switch` sur `[objet+0x4C]` |
| 3 | **fin** | `FUN_8231A6F0(objet + 0x45C) ; FUN_8230B4F8()` |
| 4 | **dessin** | `si ([objet+0x4C] != 1) retourne ; FUN_8231AF98(objet + 0x45C)` |
| 5 | **bouchon partagé** `0x823A7598`, **chez les neuf** | — |

**Audience et Opening ont le bouchon au rang 4** et partagent `0x821D1000`
(une fonction du moteur, du lot `_manque_quest`) au rang 0 : **elles ne
dessinent rien elles-mêmes.** Ce sont des porteuses d'état, pas des écrans.

### 17.3 LE DESSIN DU TABLEAU EST `FUN_8231AF98` — la réserve du §16.4 est levée

Le rang 4 de `TaskTournament` délègue à `FUN_8231AF98(objet + 0x45C)`. Or
c'est **exactement** la fonction rencontrée au §16.1, celle qui dessine une
liste mêlant joueurs enregistrés (`FUN_82235F28(…) + 0x59`) et PNJ (recopiés
de `npc_tbl` par `FUN_8230DDF0`). Le §16.4 la donnait comme « candidat pour
le tableau de tournoi, non vérifié » : **c'est vérifié, et `+0x45C` est le
sous-objet de la liste.**

Et cela confirme au passage le constat du §16.1 : **même là, seul le nom est
dessiné**, jamais les répliques.

### 17.4 Le séquenceur a DEUX niveaux

#### Niveau 1 — `[objet+0x4C]`, quatre étapes (le rang 2)

| étape | ce qu'elle fait |
|--:|---|
| 0 | attend que `FUN_8230B488()` **et** `FUN_8230B4E8()` rendent 0, puis étape 1 |
| 1 | appelle `FUN_8231F1D8(objet)` — le niveau 2. Tant qu'il rend non nul, on reste ; dès qu'il rend 0, on tombe dans le cas 2 |
| 2 | `FUN_82316380()` puis **`FUN_82317F88()`** ; pose `+0x58` puis étape 3 |
| 3 | quand `FUN_82308640(…, 0x11)` est vrai : `FUN_8220D1E0([objet+0x58])` puis `FUN_822B1610(0)` |

**La sortie du tournoi dépend du PAIEMENT D'UN ÉVÉNEMENT.** `FUN_82317F88`
est, mot pour mot, la fonction que le §10.2 avait identifiée comme « le
paiement d'un événement » :

    si FUN_82317F88() rend 0     ->  [objet+0x58] = 0x54
    sinon                        ->  FUN_82309EB0(…, 1, 0) ; [objet+0x58] = 0x58

et `0x54` est une transition carte/salle, `0x58` l'après-combat (§2). Donc
**un tournoi qui a payé sort par l'après-combat ; un tournoi qui n'a rien
payé retourne à la salle.** `FUN_8220D1E0` est bien le demandeur de
sous-état, confirmé au §15.4.

#### Niveau 2 — `[objet+0x50]`, treize étapes

`FUN_8231F1D8` (1 808 octets) porte un `switch` de **0 à 0xC**. Son travail
est de monter les écrans un par un, chacun comme une **sous-tâche créée par
son nom à un offset fixe** de l'objet du tournoi :

| offset | nom de tâche | classe | créée à l'étape |
|---|---|---|--:|
| **+0x60** | `TASK_TOURNAMENT_OPENING` | `…Opening` | 0 |
| **+0xBC** | `TASK_MATCH_INFO` | `…MatchInfo` | ~6 |
| **+0x1CC** | `TASK_RESULT_INFO` | `…ResultInfo` | 10 |
| **+0x310** | `TASK_MESSAGE_INFO` | `…MessageInfo` | 11 |
| **+0x404** | `TASK_AUDIENCE` | `…Audience` | 10 |
| +0x45C | — | la **liste** (§17.3) | — |
| +0x464 | — | un champ remis à zéro à l'init | — |

L'attente d'une sous-tâche se lit `FUN_822C80D0(objet + offset) == 0`, et son
démontage `FUN_822C7D50(objet + offset)`. L'étape 10 reboucle sur l'étape 2
quand `FUN_82316850` est vrai : **c'est la boucle des tours du tournoi.**

### 17.5 Entry et List ne sont PAS des sous-tâches du tournoi

Il n'existe **aucune** chaîne `TASK_TOURNAMENT_ANNOUNCE`, `…_ENTRY` ou
`…_LIST` dans la zone de noms — vérifié par balayage de
`0x8208E000`-`0x8208F800`, qui porte bien les dix-sept autres noms du mode.
Ces trois classes ne passent donc pas par l'usine à noms.

Chaque vtable a **exactement un** site de construction :

| classe | vtable | construite en |
|---|---|---|
| `TaskTournament` | `0x8208EFB8` | `0x8231C26C` — dans le bloc du Quest |
| `…Announce` | `0x8208EBB8` | `0x82318A34` — dans le bloc du Quest |
| **`…Entry`** | `0x8208EB9C` | **`0x826294A0` — HORS du bloc** |
| **`…List`** | `0x8208EC6C` | **`0x82629548` — HORS du bloc** |

`Entry` (l'inscription) et `List` (la liste des tournois d'une salle) sont
donc construites depuis `0x8262xxxx`, loin du mode : ce sont des **écrans
autonomes atteints depuis la salle**, pas des morceaux du tournoi en cours.
C'est cohérent avec le §9.30 point 4, qui listait « Tournament dans une
salle » comme une entrée de menu à câbler.

### 17.6 Un outil de plus, et pourquoi il manquait

`glob2` a rendu **« 0 construction »** sur les quatre vtables, y compris
celle de `TaskTournament`, qui est évidemment employée. Ce n'était pas une
mesure : **une vtable est une VALEUR QU'ON RANGE, pas une adresse qu'on
lit**, et `glob2` cherche des accès mémoire. Mauvais instrument.

D'où `xref2007.py` : il cherche la **construction** d'une constante
(`lis` seul, `lis`+`addi`, `lis`+`ori`, jusqu'à quatre mots d'écart). C'est
ce que fait `x360_ppc.py xref`, mais celui-là lit l'image de Final Showdown
(§14.7). C'est le quatrième zéro-qui-n'était-pas-une-mesure de la séance,
après les trois du §15.4.

### 17.7 Ce qui reste des tournois

1. **le contenu des treize étapes** du niveau 2 : je n'ai lu que leur
   enchaînement et les sous-tâches qu'elles montent, pas ce que chacune
   calcule ;
2. **les cinq grosses méthodes de dessin** — Announce 1712, Entry 1644,
   MessageInfo 1268, MatchInfo 1080, List 976, ResultInfo 480 octets — aucune
   n'est lue ;
3. **la composition du tableau** : **le tableau lui-même est lu au §17.8** ;
   restent le tirage et l'adversaire de chaque tour ;
4. `FUN_8230B488`, `FUN_8230B4E8`, `FUN_82316380`, `FUN_82308640`,
   `FUN_82316850` — cinq gardes et compteurs non lus, tous hors `.pdata`
   (des feuilles) ;
5. et le lien avec le dôme : le §9.21 dit que **le dôme est le lieu des
   tournois** et le §14.2 que c'est le huitième lieu, le seul sans récompense
   de complétion. Le code qui ouvre un tournoi depuis le dôme n'est pas
   identifié.

Le squelette est donc posé — une tâche nommée, six méthodes par classe, deux
niveaux de séquenceur, cinq sous-tâches placées, la sortie conditionnée au
paiement — et le remplissage reste à faire.

### 17.8 LE TABLEAU : 32 places, cinq tours, et trois tailles de tournoi

`FUN_8231B9A0(liste, taille)` le construit, et tout s'y recoupe. `liste` est
`objet + 0x45C`, le sous-objet que le rang 4 dessine (§17.3).

#### La taille du tournoi — trois valeurs

```c
liste[3] = taille;  liste[0] = 0x80;  liste[1] = liste[2] = 0;
if      (taille == 0x10) liste[4] = 1;      /* 16 participants */
else if (taille == 0x20) liste[4] = 2;      /* 32 participants */
else                     liste[4] = 0;      /*  8 participants */
```

La taille vient de **`[0x82656B10] & 0xFF`**, dans le bloc d'état statique du
Quest (celui de `FUN_82315930`, §14.7). **Trois tailles : 8, 16 et 32.** Et
`liste[4]` vaut 0, 1 ou 2 — soit *le nombre de tours au-delà de trois*, ce
qui est cohérent : 8 participants font 3 tours, 16 en font 4, 32 en font 5.

#### La planche et les trente-deux places

    FUN_82166AD0(0.0, …, 0x41B, "tnt_hyou_32", 0, 9, 0);

**`tnt_hyou_32`** — *hyou*, le tableau — et le **32** est dans le nom de la
composition : la planche porte toujours trente-deux places, quelle que soit
la taille du tournoi. Scène `0x41B`, **mode 9**, l'idiome des fenêtres du
Quest (§9.20).

Les places sont des **calques nommés par `sprintf`** :

    FUN_82249520(&tampon, 8, "%02d_lt", n + 1);     /* "01_lt" … "32_lt" */
    FUN_82141840(…, "p_name_", 7);                  /* le prefixe        */

soit **`p_name_01_lt` à `p_name_32_lt`**. Pour chacun, `FUN_82166778` cherche
le calque ; s'il existe on recopie sa position (`+0x40`, `+0x44`, `+0x48`),
sinon on met zéro. Chaque place occupe **28 octets** (7 flottants) à partir de
`liste + 0x18`, et porte son propre indice en `+0x18` de l'entrée. La boucle
tourne **32 fois** (`while (i < 0x20)`).

#### Les cinq tours, et le compte tombe juste

Une seconde boucle écrit son indice dans **62 entrées de `0x18` (24) octets**
à partir de `liste + 0x3A9` (`while (i < 0x3E)`), puis la fonction pose cinq
pointeurs :

| pointeur | cible | taille jusqu'au suivant | entrées de 24 o |
|---|---|--:|--:|
| `liste + 0x968` | `liste + 0x398` | `0x300` = 768 | **32** |
| `liste + 0x96C` | `liste + 0x698` | `0x180` = 384 | **16** |
| `liste + 0x970` | `liste + 0x818` | `0x0C0` = 192 | **8** |
| `liste + 0x974` | `liste + 0x8D8` | `0x060` = 96 | **4** |
| `liste + 0x978` | `liste + 0x938` | — | **2** |

Et la fonction pose, juste après, les deux suites qui le confirment :

    {0x20, 0x10, 8, 4, 2}        les participants par tour
    {1, 2, 3, 4, 5}              le numero du tour

**32 + 16 + 8 + 4 + 2 = 62**, exactement la borne `0x3E` de la seconde
boucle. **Le tableau est donc une élimination directe à cinq tours, cinq
tableaux chaînés dont chacun fait la moitié du précédent.** Rien n'est
supposé : les cinq pointeurs, les cinq tailles, les cinq numéros de tour et
le total de 62 se vérifient l'un par l'autre.

#### TROIS MUSIQUES DE TOURNOI — correction du §15.1

L'étape 0 du séquenceur choisit une musique par `FUN_822B1540(voie, chemin)`,
le joueur de BGM, parmi **trois** :

| chaîne | fichier |
|---|---|
| `0x82084904` | `sound/bgm/vf5ps3_b08tn1.adx` |
| `0x8208F338` | `sound/bgm/vf5ps3_b06tn1.adx` |
| `0x8208F354` | `sound/bgm/vf5ps3_b04tn1.adx` |

Le choix passe par `FUN_823158C0(x)` et par `FUN_82315A90(piVar2)`, qui rend
une phase comparée à **3** et à **6**.

**Le §15.1 disait « aucun autre morceau n'est demandé »** — c'était exact
pour `TaskQuestMap`, `TaskQuestHomeMenu` et `TaskQuestTenpo`, les trois que
`musique_quest.py` avait relevées, et **faux pour le mode entier** : le
tournoi en ajoute trois. **Porter les tournois demande donc quatre fichiers
de musique, pas un.**

#### Ce qui reste du tableau

- **d'où vient l'adversaire de chaque tour** : **lu au §17.9** — la position
  se CALCULE par division du numéro de match. `FUN_8231D7C0` (476 octets) et
  `FUN_8231D9A0` restent non lues ;
- **le tirage** : rien dans `FUN_8231B9A0` ne tire au sort. Elle **place** les
  trente-deux calques et chaîne les tours. **Le tirage est au §17.10** ;
- `FUN_82315A90` et `FUN_823158C0` sont des feuilles hors `.pdata`, non lues,
  et ce sont elles qui portent la phase et le choix de musique.

### 17.9 LE DÉROULÉ DES TOURS : six descripteurs, un compteur de match, et la sortie

Deux champs d'un octet du bloc d'état du Quest (`FUN_82315930()` =
`0x82656B08`) portent toute la progression :

| champ | rôle |
|---|---|
| **`+0x4C8`** | **le TOUR courant** |
| **`+0x4C9`** | **le MATCH courant dans ce tour** |

Et les tours sont décrits par un tableau d'**enregistrements de 8 octets en
`bloc + 0x498`** — `(tour + 0x93) * 8 + bloc`, et `0x93 * 8 = 0x498` —, **au
plus six** (toutes les boucles bornent à 6) :

| champ de l'enregistrement | contenu |
|---|---|
| `+5` | **le nombre de matchs du tour** |
| `+6` | **le TYPE du tour** : 3, 4 ou 5 |

C'est ce même enregistrement que `FUN_82315B00()` rend, et que
`FUN_8231A768` lisait au §17.8 : **la suite {32, 16, 8, 4, 2} est le champ
`+5` de ces enregistrements**, et le « `[iVar3+6] == 5` » y est un type de
tour. Deux lectures indépendantes de la même table.

#### L'avance, `FUN_82316850`, lue en entier

```c
tour = [bloc + 0x4C8];
desc = bloc + 0x498 + tour * 8;
if (desc[6] == 4) { [bloc + 0x38] = 1; return 0; }   /* LE TOURNOI EST FINI */
i = ++[bloc + 0x4C9];
if (i < desc[5]) return 1;                           /* encore un match ici */
if (desc[6] == 3)        -> cherche, parmi les six, le premier tour de type 5
else if (desc[6] != 5)   -> tour suivant ([bloc+0x4C8] = tour + 1)
else                     -> cherche le premier tour de type 4
[bloc + 0x4C9] = 0;                                  /* on repart au match 0 */
return 1;
```

**Trois choses se lisent là :**

1. **`desc[6] == 4` termine le tournoi** : la fonction pose `[bloc+0x38] = 1`
   et rend 0, ce qui fait sortir le séquenceur de son étape 10 (§17.4).
   ~~Le type 4 est donc la sentinelle de fin, pas un tour~~ — **FAUX : le
   type 4 est LA FINALE, et le §17.15 nomme les six types** ;
2. les types **3** et **5** ne vont pas au tour suivant : ils **sautent** au
   premier enregistrement d'un autre type (3 → cherche un 5, 5 → cherche un
   4). Le déroulé n'est donc pas linéaire : c'est une petite machine à sauts
   sur six cases ;
3. le compteur de match est **toujours remis à zéro** au changement de tour.

#### Et la position du joueur est CALCULÉE, pas stockée

`FUN_8231A768(liste)` ne lit aucune table de tableau : il **divise**.

```c
taille = [bloc + 8];                     /* 0x10 ou 0x20 */
if (FUN_82316558(bloc))      return liste[5] >> 3;
if (desc[6] == 5)            return liste[1];        /* la finale */
facteur = desc[5] >> (taille == 0x20 ? 2 : 1);
return [bloc + 0x4C9] / facteur;         /* le match courant / le facteur */
```

(les `trapWord` que rend Ghidra sont les contrôles de division par zéro et de
débordement que MSVC émet autour d'un `divwu` — pas du code du jeu.)

**Donc la place du joueur dans le tour courant se déduit du numéro de match
par une division**, exactement comme un indice d'élimination directe. Rien
n'est tiré au sort à ce moment-là, et rien n'est mémorisé par tour : la
position se recalcule. Pour 32 participants le facteur est
`nombre_de_matchs >> 2`, pour 16 `>> 1`, et la finale est un cas à part.

Un cas particulier mesuré, sans explication : pour une taille de 32 et un
tour de 2 matchs, la fonction rend **2 si `[bloc+0x4C9]` est non nul, 0
sinon** — un résultat binaire, pas une division.

#### Ce qui reste, et c'est maintenant une seule question

Les cinq écritures de `[bloc + 0x4C9]` sont toutes dans
`FUN_82316850`, **sauf une** : `0x82318990`, dans le voisinage immédiat du
constructeur de `TaskTournamentAnnounce` (dont la vtable se construit en
`0x82318A34`, §17.5). **C'est là qu'était le tirage, et il est lu : voir le §17.10.**

Le reste de la chaîne est désormais lu : la taille du tournoi
(`[bloc+8]`, trois valeurs), le tour (`+0x4C8`), le match (`+0x4C9`), les six
descripteurs de tour (`+0x498`), les cinq niveaux de tableau chaînés
(§17.8), les trente-deux calques `p_name_NN_lt` de la planche
`tnt_hyou_32`, la position calculée par division, la fin par le type 4, et la
sortie conditionnée au paiement (§17.4).

### 17.10 LE TIRAGE, ET IL BOUCLE SUR LA TABLE DES ÉVÉNEMENTS

`FUN_82318848(bloc, taille)` — 456 octets — est **la mise en place du
tournoi**, et elle fait deux choses.

#### 1. Elle remplit les six descripteurs de tour, trois barèmes selon la taille

Les enregistrements de 8 octets en `bloc + 0x498` sont écrits **octet par
octet**, et les offsets confirment la disposition du §17.9 : `+4`, `+5`, `+6`
de chaque record (`0x49C/0x49D/0x49E`, `0x4A4/0x4A5/0x4A6`, `0x4AC/0x4AD/0x4AE`,
`0x4B4/0x4B5/0x4B6`, `0x4BC/0x4BD/0x4BE`, `0x4C4/0x4C5/0x4C6`). **Six records,
et les trois barèmes sont en dur :**

| rec | 8 participants | 16 participants | 32 participants |
|--:|---|---|---|
| 0 | `+4`=8 `+5`=4 `+6`=0 | 16, 8, 0 | 32, 16, 0 |
| 1 | 4, 2, 3 | 8, 4, 1 | 16, 8, 1 |
| 2 | 2, 1, 4 | 4, 2, 2 | 8, 4, 2 |
| 3 | 2, 1, 5 | 2, 1, 4 | 4, 2, 4 |
| 4 | 0, 0, 6 | 2, 1, 5 | 2, 1, 3 |
| 5 | 0, 0, 6 | 0, 0, 6 | 2, 1, 5 |

(`+4` = les participants du tour, `+5` = ses matchs, `+6` = son type. Les
valeurs sont relevées des écritures, y compris la queue commune aux cas 8 et
16.)

Le parcours n'est **pas** l'ordre des indices : le §17.9 l'a montré, les
types 3 et 5 sautent au premier record d'un autre type. Pour 8 participants
cela donne `rec0` (type 0) → `rec1` (type 3) → saute au premier type 5,
`rec3` → saute au premier type 4, `rec2` → **fin**. Les records sont donc
rangés par niveau de tableau et visités par type.

#### 2. ELLE TIRE LA PLACE DU JOUEUR AU SORT

```c
[bloc + 8] = taille;  [bloc + 0x4C8] = 0;  [bloc + 0x4C9] = 0;
FUN_82318280(bloc, taille, pile);        /* la liste des rivaux */
hasard = FUN_822499E8(0);                /* le MEME generateur que le 14.7 */
entree = *(byte **)(bloc + 0x498);
for (i = 0; i < taille; i++) {
    *(u32 *)(entree + 4) = i;                       /* le numero de place */
    if (i == hasard % taille) {                     /* <<<< LE TIRAGE */
        entree[0] |= 0x40;                          /* « c'est moi »     */
        *(u32 *)(entree + 0xC) = [bloc + 0x4CC];
    } else {
        *(u32 *)(entree + 8) = pile[i];             /* un RIVAL          */
        entree[0] |= 0x80;                          /* « c'est un PNJ »  */
    }
    entree += 0x10;
}
```

**La place du joueur est `rand() % taille`.** Les entrées font **16 octets** :
drapeaux en `+0`, numéro de place en `+4`, identifiant du rival en `+8`,
donnée du joueur en `+0xC`. Deux bits se lisent : **`0x40` = le joueur**,
**`0x80` = un PNJ**.

`entree` est le **pointeur lu en `bloc + 0x498`**, c'est-à-dire les quatre
premiers octets du record 0 — les seuls que cette fonction n'écrit pas.
**Le §17.11 montre qu'il est posé AU LIEN, dans `.data`.**

#### 3. ET LES PARTICIPANTS VIENNENT DES RIVAUX DU LIEU DE L'ÉVÉNEMENT

`FUN_82318280(bloc, taille, sortie)` — 928 octets — ferme la boucle avec le
§16.2 :

```c
n      = [bloc + 0x00];                       /* le NUMERO D'EVENEMENT */
record = &DAT_82656798 + n * 0x34;            /* LA TABLE DU 16.2      */
masque = *(u32 *)(record + 0x2C);             /* le MOT 11             */
if (record[0x30] == 0x13) {                   /* le MOT 12, octet 0    */
    fiche = FUN_82235F28(0x827A99F8, [bloc + 0x133 * 4]);
    FUN_8230DBC8(*(u8 *)(fiche + 0xF9));
}
FUN_8230E018(…, …, masque);                   /* les rivaux DU LIEU    */
```

Trois recoupements, et aucun n'est une supposition :

- **`&DAT_82656798` et le pas `0x34`** sont exactement la table des quinze
  événements du §16.2 — `FUN_82315890` rendait `n * 0x34 + 0x82656798` ;
- **`+0x2C` est le mot 11**, celui que le §16.2 avait lu comme le **masque de
  lieu** (1, 2, 4 … 64 pour les sept événements de lieu, 255 pour les huit
  autres). Et il part dans **`FUN_8230E018`**, la fonction que le §9.21 avait
  mesurée : « parcourt les mille rivaux et garde ceux dont `npc_tbl[n]+0x88`
  tombe dans le masque ». Le mot 11 est donc **confirmé par un second
  lecteur** ;
- **`+0x30` est le mot 12**, que le §16.2 laissait non lu. Son premier octet
  vaut `0x13` pour les sept événements de lieu (`0x13000000`), et c'est
  exactement la valeur testée ici. **Le mot 12 porte donc, au moins dans son
  premier octet, un TYPE d'événement**, et `0x13` déclenche la lecture de la
  fiche du joueur.

**Donc : les participants d'un tournoi sont les rivaux du LIEU de
l'événement**, filtrés par le masque de la table des récompenses, et la place
du joueur parmi eux est tirée au sort.

#### Ce qui reste du tournoi

La chaîne est maintenant continue, de l'événement au tableau dessiné. Il
reste :

1. ~~qui pose le pointeur en `bloc + 0x498`~~ — **§17.11 : l'éditeur de liens** ;
2. ~~la suite de `FUN_82318280`~~ — **§17.11 : cascade de replis puis tirage
   sans remise** ;
3. les **six grosses méthodes de dessin** des classes (§17.7 point 2), toujours
   aucune ;
4. les mots **10** de la table des événements, et les octets 1-3 du mot 12.

### 17.11 `bloc + 0x498` et `FUN_82318280` : les deux dernières pièces

#### A. Personne n'écrit le pointeur, et c'est normal : il est posé AU LIEN

Le §17.10 laissait la question ouverte. Trois mesures la ferment :

1. l'instruction est bien un **chargement de pointeur** —
   `0x823189A4 lwz r11, 0x498(r31)` ;
2. **aucune écriture** : le balayage du déplacement `0x498` sur toute l'image
   donne 35 `stw`, et **pas une** dans le bloc du Quest (toutes en
   `0x8215xxxx`, `0x8234xxxx`, `0x824Dxxxx` — d'autres structures au même
   déplacement). `x360_suivre.py --graphe --champ 0x498` sur l'accesseur ne
   rend rien non plus ;
3. **le bloc est statique**, en `.data`, et l'image de `xex.py` est l'image
   **chargée** : on peut donc y lire l'état initial. Les six descripteurs y
   portent déjà leurs pointeurs.

| rec | adresse | pointeur initial | = bloc + | octets jusqu'au suivant | entrées de `0x10` |
|--:|---|---|---|--:|--:|
| 0 | `0x82656FA0` | `0x82656BA0` | `+0x098` | 512 | **32** |
| 1 | `0x82656FA8` | `0x82656DA0` | `+0x298` | 256 | **16** |
| 2 | `0x82656FB0` | `0x82656EA0` | `+0x398` | 128 | **8** |
| 3 | `0x82656FB8` | `0x82656F20` | `+0x418` | 64 | **4** |
| 4 | `0x82656FC0` | `0x82656F60` | `+0x458` | 32 | **2** |
| 5 | `0x82656FC8` | `0x82656F80` | `+0x478` | 32 | **2** |

**32 + 16 + 8 + 4 + 2 + 2 = 64 entrées, soit `0x400` octets exactement, de
`bloc + 0x098` à `bloc + 0x498`** — où commencent les six descripteurs
(6 × 8 = 48 octets, jusqu'à `+0x4C8`), immédiatement suivis du tour
(`+0x4C8`) et du match (`+0x4C9`). Le bloc est empaqueté à l'octet près, et
les trois chiffres se vérifient l'un l'autre.

**Donc il n'y a pas d'écrivain à trouver : les six tableaux de participants
sont alloués et chaînés par l'éditeur de liens.** C'est pour cela que tous
les balayages rendaient zéro — et cette fois le zéro *est* la mesure, parce
qu'on a pu lire la valeur initiale au lieu de déduire son absence.

À ne pas confondre avec les **cinq** pointeurs de `FUN_8231B9A0`
(`liste + 0x968`…`+0x978`, §17.8) : ceux-là sont du côté **affichage**, dans
l'objet de la liste, et il y en a cinq. Ici c'est le côté **données**, dans
le bloc d'état, et il y en a six — la sixième case de 2 entrées est ce qui
explique le sixième descripteur.

Et le modulo du tirage se lit en clair dans le même désassemblage :
`divwu` / `mullw` / `subf`, soit `hasard % taille`, avec le `twi 6, r29, 0`
de la division par zéro.

#### B. `FUN_82318280` : une cascade de replis, puis un tirage sans remise

**1. Le vivier part de la table des événements** (§17.10) :

```c
n      = [bloc + 0x00];                     /* le numero d'evenement */
record = &DAT_82656798 + n * 0x34;
masque = *(u32 *)(record + 0x2C);           /* le mot 11 : le LIEU */
if (record[0x30] == 0x13) { … lit la fiche du joueur … }
FUN_8230E018(vecteur, filtre, masque);      /* les rivaux du lieu */
```

**2. Puis il S'ÉLARGIT jusqu'à ce qu'il y ait assez de monde.** Le même motif
se répète **cinq fois** : on compte le vivier (`(fin - début) >> 2`, donc des
identifiants de 32 bits), et **si le compte est inférieur à la taille du
tournoi**, on vide et on recommence avec un critère plus large :

| essai | appel | ce qui est lâché |
|--:|---|---|
| 1 à 3 | `FUN_8230E018(vec, filtre, masque)` | — |
| 4 | `FUN_8230E018(vec, **0**, masque)` | **le filtre** |
| 5 | `FUN_8230E018(vec, **0**, **0**)` | **le filtre ET le masque** — les mille rivaux |

Le dernier recours est donc **le vivier entier**, sans lieu. Un tournoi ne
peut pas manquer de participants.

*Une réserve honnête :* les essais 1 à 3 sont **identiques dans le C
décompilé**. Soit l'objet `filtre` est modifié entre eux d'une façon que
Ghidra ne montre pas, soit le décompilateur a déplié une boucle. Je ne
tranche pas, et je ne prête pas aux trois premiers essais un critère que je
n'ai pas vu.

**3. Le choix est un tirage SANS REMISE** — un Fisher–Yates partiel :

```c
for (n = taille; n != 0; n--) {
    if (reste == 0) *sortie = vivier[0];        /* vivier vide : on repete le premier */
    else {
        j = FUN_822499E8(0) % reste;
        *sortie = vivier[j];                    /* on prend le j-ieme   */
        reste--;
        vivier[j] = vivier[reste];              /* le DERNIER prend sa place */
    }
    sortie++;
}
```

**Donc aucun doublon** tant que le vivier suffit, et le cas dégénéré (vivier
vide) recopie `vivier[0]` autant de fois qu'il faut au lieu de planter.

Un détail qui compte pour le portage : la fonction tire **`taille`** rivaux,
pas `taille - 1`. C'est `FUN_82318848` qui écrase ensuite l'une des places
par le joueur (§17.10) — **un rival tiré est donc jeté**, et lequel dépend du
`rand() % taille` de la place du joueur.

#### Ce qui reste des tournois, après ça

Les données sont closes de bout en bout : événement → masque de lieu →
vivier élargi par replis → tirage sans remise → trente-deux places →
place du joueur au hasard → six tableaux chaînés → six descripteurs de tour →
position par division → fin par le type 4 → sortie selon le paiement.

Il ne restait que **l'affichage**, et le §17.12 en fait l'inventaire : les
planches des six écrans, les trois tableaux, et le couple
`FUN_8231D7C0` / `FUN_8231D9A0` qui pose puis anime. **Seule la mise en
page reste non lue.**

### 17.12 LES SIX ÉCRANS ET LE TABLEAU À L'ÉCRAN

**La méthode, dite d'abord, parce qu'elle borne le résultat.** Ces huit
fonctions font 8 300 octets. Je ne les ai pas lues ligne par ligne : j'ai
mesuré **ce que chacune NOMME** — les constantes qu'elle construit et qui
tombent sur une chaîne. Un écran de ce moteur se nomme par ses planches AET,
donc nommer, ici, c'est identifier. Ce qui suit est donc **l'inventaire des
planches, pas la lecture de la mise en page.**

#### Les six écrans, chacun par ses fenêtres

| classe | planches AET citées |
|---|---|
| **Announce** (1712 o) | `p_que_info_win_01_ct`, `p_que_info_win_36_02_ct`, `p_que_info_win_03_ct`, `p_que_info_win_30_04_ct` |
| **Entry** (1644 o) | `p_rule_win_logo_01_c`, `p_rule_win_26_02_ct`, `p_rule_win_30_03_ct`, `p_rule_win_04_ct` |
| **MessageInfo** (1268 o) | `p_cmn_win_l_01a_l`, `p_cmn_win_l_01b_c`, `p_tnt_info_win_01_ct`, `p_tnt_info_win_02_ct` |
| **MatchInfo** (1080 o) | `p_tnt_vs_win_logo_c`, `p_tnt_vs_win_02_ct`, `p_tnt_vs_win_03_ct`, `p_tnt_vs_win_04_ct` |
| **List** (976 o) | `p_compe_list_win_01_ct`, `p_compe_list_win_hed_40_02_lt`, `p_compe_list_arrow_up_c`, `p_compe_list_arrow_down_c`, `p_compe_list_trophy_02_c` |
| **ResultInfo** (480 o) | `p_tnt_rslt_win_logo_c`, `p_tnt_rslt_win_02_ct`, `p_tnt_rslt_win_03_ct`, `p_tnt_rslt_win_04_ct` |

Trois choses s'en lisent sans rien supposer :

- **les suffixes sont ceux du §9.17** — `_c`, `_ct`, `_l`, `_lt` : le nom
  porte son alignement, exactement comme les autres fenêtres du Quest. Les
  planches des tournois ne sont donc pas un cas à part, elles suivent la même
  règle d'ancrage ;
- **les nombres dans les noms** (`_36_`, `_30_`, `_26_`, `_40_`) sont au même
  emplacement que dans les fenêtres déjà portées : ce sont les boîtes, pas des
  numéros de libellé ;
- **cinq des six citent `%s%s`** (`0x82000F80`), le format de concaténation
  que le §14.4 voyait déjà composer les noms. `ResultInfo` est la seule qui ne
  le cite pas — et c'est aussi la plus courte.

`List` est la seule à porter des **flèches** (`arrow_up`, `arrow_down`) et un
**trophée** : c'est bien la liste défilante des tournois d'une salle, ce que
le §17.5 déduisait de sa construction hors du bloc du Quest.

#### `FUN_8231D7C0` POSE le tableau — et il y a trois planches, plus la finale

```c
void FUN_8231D7C0(liste, byte tour)
{
    taille    = liste[4];                                 /* 0, 1 ou 2 (§17.8) */
    planches  = { "tnt_hyou_8", "tnt_hyou_16", "tnt_hyou_32" };
    scene     = 0x41B;
    plan      = planches[taille];                         /* <<<< par la TAILLE */
    if (FUN_82315940() == 1) plan = "tnt_hyou_32_filnal";  /* <<<< la FINALE */
    if ((liste[0] & 0x80) == 0) {
        if (taille == 0) { debut = fin = "sta_e"; }        /* figé à la fin */
        else {
            etapes = { 1, 2, 4, 6 };
            sprintf(buf, "ido%02d", etapes[tour]);         /* "ido01".."ido06" */
            calque = buf + "_s";
        }
    } else { debut = "sta_s"; fin = "sta_e"; }             /* l'entrée animée */
    calque_2D = 2;  mode = 9;
    liste[1] = liste[2] = tour;
    liste[0] |= 8;
}
```

**Quatre mesures :**

1. **`liste[4]` indexe directement les trois planches.** Le §17.8 avait lu que
   ce champ vaut 0, 1 ou 2 selon 8, 16 ou 32 participants, **depuis la mise en
   place** ; ici c'est l'index du tableau de planches, **depuis l'affichage**.
   Deux lectures indépendantes, même conclusion — et il y a donc bien
   **une planche par taille de tournoi** ;
2. **la finale a sa propre planche**, et son nom porte **une faute de frappe
   du jeu** : `tnt_hyou_32_filnal`, pas `final`. À reproduire telle quelle si
   on porte la planche — c'est le genre de détail qui coûte une séance ;
3. scène `0x41B`, **calque 2D = 2, mode 9** : l'idiome des fenêtres du Quest
   (§9.20), une troisième fois ;
4. **les étapes d'animation sont `{1, 2, 4, 6}`, indexées par le TOUR**, et
   formatées en `ido%02d` — *idō*, 移動, « déplacement ». Le tableau montre
   donc le déplacement du tour, et les quatre valeurs ne sont pas 1-2-3-4 :
   **1, 2, 4, 6**.

#### `FUN_8231D9A0` JOUE le déplacement

Même structure, mais elle construit **deux** noms de calque au lieu d'un :
`ido%02d` + **`_s`** (`0x8208F1FC`) et `ido%02d` + **`_e`** (`0x8208F228`).

C'est le schéma de marqueurs du §9.13 appliqué à un segment : **on joue de
`idoNN_s` à `idoNN_e`**. Et elle cite en plus **`tnt_move`**, la composition
du déplacement.

Donc la répartition est nette : **`FUN_8231D7C0` pose le tableau à une image
fixe, `FUN_8231D9A0` joue la transition d'un tour au suivant.** C'est bien le
couple que le §17.11 cherchait.

#### Ce que cela laisse

L'inventaire des planches des tournois est complet : **six fenêtres d'écran,
trois tableaux, un tableau de finale, une composition de déplacement, deux
flèches et un trophée.** Avec les suffixes d'ancrage, c'est ce qu'il faut pour
déclarer ces planches dans les bases 2D de Final Showdown — le §9.30 notait
déjà que `tnt`/`tnto` y sont déclarées.

**La mise en page est lue au §17.13** — quel libellé dans quelle fenêtre,
pour les six. Les POSITIONS, elles, ne sont pas dans le code : elles vivent
dans les ancres des planches AET (§9.17).

### 17.13 LA MISE EN PAGE DES SIX ÉCRANS, fenêtre par fenêtre et texte par texte

#### L'idiome, lu sur la plus courte des six

`FUN_8231D5E0` (ResultInfo, 480 octets) le donne en entier :

```c
if ([ecran+0x50] != 1 && [ecran+0x50] != 2) return;    /* l'etat interne */
FUN_822C29D8(2);  FUN_822C2A08(9);                     /* calque 2D = 2, mode 9 */
FUN_8223BC10(0xE);  FUN_8223C130(9);                   /* la police */
FUN_8223C048(0xFFFFFFFF);                              /* blanc */
ancres = ecran + 0x60;

FUN_822E39C0(ancres, &pos, "p_tnt_rslt_win_logo_c", 0);   /* RESOUT L'ANCRE */
FUN_8230A9B8(bloc, 0, 9, &pos);                           /* pose le logo   */

FUN_822E39C0(ancres, &pos, "p_tnt_rslt_win_02_ct", 0);
FUN_8223BEB8(pos.x, pos.y);                               /* s'y place      */
FUN_8223FE30(police, FUN_82322798(0x28E));                /* dessine le texte */
```

**Donc chaque nom de fenêtre s'apparie au libellé qui le suit**, et c'est cet
appariement qui EST la mise en page.

**Les coordonnées ne sont pas dans le code**, et ce n'est pas une lacune de
lecture : `FUN_822E39C0` les prend dans **l'ancre de la planche AET** à
partir du nom. C'est la règle du §9.17 — « le Quest ne place pas son texte,
il le POSE ». Le code ne cite que des noms ; les positions vivent dans les
planches.

Les numéros sont ceux de 2007, et `tools/quest_textes_map.h` les nomme (492
libellés). Ce qui suit est donc **le contenu réel des écrans**.

#### `List` — la liste des tournois d'une salle

| fenêtre | libellé | texte |
|---|--:|---|
| `p_compe_list_win_01_ct` | 601 | **List of official tournaments** |
| `p_compe_list_win_hed_40_02_lt` | 607 | **You have not cleared any tournaments.** |
| `p_compe_list_arrow_down_c` | 352 | OK |
| `p_compe_list_trophy_02_c` | — | le trophée |
| `p_compe_list_arrow_up_c` / `_down_c` | — | les deux flèches de défilement |

#### `Entry` — les règles, et la demande d'inscription

| fenêtre | libellé | texte |
|---|--:|---|
| `p_rule_win_logo_01_c` | — | le logo |
| `p_rule_win_26_02_ct` | 620 | **Participants: %d** |
| | 621 | **Rounds: %d** |
| | 622 | **Time: %d** |
| | 625 | **1st place: Item / 2nd place: %dG / 3rd place: %d…** |
| | 626 | **1st place: Emblem / 2nd place: %dG / 3rd place:…** |
| | 624 | **1st place: %dG / 2nd place: %dG / 3rd place: %dG** |
| | 627 | Official tournament. Place in the tournament… |
| `p_rule_win_30_03_ct` | 629 | **Do you want to enter this tournament?** |
| `p_rule_win_04_ct` | 348 / 349 | **Yes** / **No** |
| | 0 | la légende « .:Enter » |

#### `Announce` — DEUX cas dans la même fonction

La fonction porte deux blocs quasi jumeaux, et les libellés les séparent :

| | début de tournoi | fin / retour |
|---|---|---|
| `p_que_info_win_01_ct` | 617 *The following tournament has begun:* | 614 (même texte) |
| `p_que_info_win_36_02_ct` | 612 *Prize: %s* · 618 *Official Tournament* | 609 · 615 |
| `p_que_info_win_03_ct` | **1507** *This tournament will end. Is this okay?* | **616** *Return to the Arcade Screen.* |
| `p_que_info_win_30_04_ct` | 348 / 349 **Yes / No** | 352 **OK** |

Les trios 617/612/618 et 614/609/615 portent **le même texte anglais sous
deux numéros** : deux jeux de libellés pour deux contextes. Et les deux cas se
distinguent par leur pied — une confirmation Yes/No d'un côté, un simple OK de
l'autre.

#### `MatchInfo` — l'annonce du match

| fenêtre | libellé | texte |
|---|--:|---|
| `p_tnt_vs_win_logo_c` | — | le logo |
| `p_tnt_vs_win_02_ct` | *trois libellés non constants* | les deux combattants |
| `p_tnt_vs_win_03_ct` | 653 | **Beginning match…** |
| `p_tnt_vs_win_04_ct` | 352 | OK |

#### `MessageInfo` — la remise des prix

| fenêtre | libellé | texte |
|---|--:|---|
| `p_cmn_win_l_01a_l` / `_01b_c` | 660 | **Your result: %s** |
| | 665 | Did not win a prize. (Arcade-sponsored tourn…) |
| | 666 | Place in Official Tournaments to clear them… |
| `p_tnt_info_win_01_ct` / `_02_ct` | 660 | Your result: %s |
| | **651** | **Item** |
| | **650** | **Emblem** |
| | **649** | **Gold** |
| | 661 | **%s received as a prize.** |
| | 662 / 663 | … / received as a prize. |
| | 999 | **%dG** |

#### `ResultInfo` — le bilan

| fenêtre | libellé | texte |
|---|--:|---|
| `p_tnt_rslt_win_logo_c` | — | le logo |
| `p_tnt_rslt_win_02_ct` | 654 | **RESULT** |
| `p_tnt_rslt_win_03_ct` | 658 | **Final tournament results** |
| `p_tnt_rslt_win_04_ct` | 352 | OK |

### 17.14 ET LA MATRICE 3 × 3 DU §16.2 EST INTERPRÉTÉE

Le §16.2 avait lu la matrice des récompenses sans savoir ce que ses trois
lignes voulaient dire. **Les libellés d'`Entry` les nomment**, et les
chiffres tombent juste :

| ligne de la table | libellé d'Entry | valeurs de l'événement 0 |
|--:|---|---|
| 0 : mots 1, 2, 3 | **625** *1st place: **Item**, 2nd: %dG, 3rd: %d* | **0**, 2000, 1000 |
| 1 : mots 4, 5, 6 | **626** *1st place: **Emblem**, 2nd: %dG, 3rd:…* | **0**, 1000, 600 |
| 2 : mots 7, 8, 9 | **624** *1st place: %dG, 2nd: %dG, 3rd: %dG* | 30000, 16000, 10000 |

**Les trois lignes sont trois BARÈMES de prix, et les trois colonnes sont les
trois PLACES.** Le premier mot de chaque ligne vaut **zéro** pour les barèmes
« objet » et « emblème » — précisément parce que la première place n'y reçoit
pas d'or —, et il porte une somme dans le barème tout-or. Trois lectures
indépendantes qui se recoupent : la table (§16.2), les libellés (ici), et les
types de récompense de `MessageInfo` (**Item**, **Emblem**, **Gold**, les
libellés 651, 650, 649).

Le « 2 000 G » du cahier des charges est donc **le prix de la deuxième place
au barème « objet »**, et non un lot global.

#### Ce qui reste, et c'est peu

- les **libellés non constants** : **lus au §17.15**, et ils nomment les
  types de tour ;
- les **états internes** : **lus au §17.16** pour les six ;
- et les **positions** : **lues au §17.17**, dans `aet_n_qwin`.

### 17.15 LES LIBELLÉS VARIABLES, et ils NOMMENT les types de tour

Les libellés « non constants » du §17.13 sortent tous de petites tables, et
une fois résolus ils interprètent la machine du §17.9.

#### `MatchInfo` : le nom du TOUR, indexé par `desc[6]`

```c
local_1b0 = { 0x29B, 0x29C, 0x29D, 0x2A6, 0x2A7, 0x2A8 };
… FUN_82322798(local_1b0[*(byte *)(desc + 6)]);
```

| `desc[6]` | libellé | texte |
|--:|--:|---|
| **0** | 667 | **Round 1** |
| **1** | 668 | **Round 2** |
| **2** | 669 | **Round 3** |
| **3** | 678 | **Semifinals** |
| **4** | 679 | **Final** |
| **5** | 680 | **3rd Place Match** |

**C'est l'index du type de tour du §17.9**, et il porte son nom.

#### Ce que cela CORRIGE au §17.9

J'y avais écrit que le type 4 était « la sentinelle de fin, pas un tour ».
**C'est la FINALE.** La machine à sauts s'explique alors d'elle-même :

| depuis | vers | pourquoi |
|---|---|---|
| type 0, 1, 2 (Round 1-3) | le tour **suivant** | l'élimination directe ordinaire |
| type **3** (Semifinals) | le premier type **5** | **le match pour la 3e place se joue après les demies** |
| type **5** (3rd Place Match) | le premier type **4** | puis la **finale** |
| type **4** (Final) | **fin** | le contrôle est en tête : la finale jouée, l'appel suivant termine |

**L'ordre réel d'un tournoi est donc : Round 1 → Round 2 → Round 3 →
Semifinals → 3rd Place Match → Final → fin.** Et les records ne sont pas
visités dans l'ordre des indices **parce que le match pour la troisième place
est rangé après la finale mais joué avant elle**. Le §17.9 constatait les
sauts sans pouvoir les expliquer ; les voilà.

Vérification sur le barème à 8 participants du §17.10 — rec0 type 0 (4
matchs), rec1 type 3 (2), rec2 type 4 (1), rec3 type 5 (1) :

    rec0  Round 1      4 matchs   8 joueurs -> 4
    rec1  Semifinals   2 matchs   4 joueurs -> 2
    rec3  3rd Place    1 match
    rec2  Final        1 match    -> fin

Huit joueurs, quatre matchs au premier tour, deux demi-finales, un match de
classement et une finale. **Le compte tombe juste**, et il tombe juste aussi
pour 16 et 32 avec leurs barèmes respectifs.

#### `MatchInfo` : le nom du MATCH, indexé par le compteur

```c
local_190 = { 0x2A9 … 0x2B2 };
… FUN_82322798(local_190[*(byte *)(bloc + 0x4C9)]);
```

**Match 1** à **Match 10**, indexés par `bloc + 0x4C9` — le compteur de match
du §17.9. Dix noms : c'est la borne d'affichage, et le pire tour en a huit
(32 joueurs au premier tour en font seize, donc **la table est plus courte que
le pire cas** — à noter si on porte l'écran).

#### `MessageInfo` : le RÉSULTAT du joueur

```c
auStack_130 = { 0x2C8, 0x2C7, 0x2C6, 0x2C4, 0x2C0, 0x2BF, 0x2BE };
```

| index | libellé | texte |
|--:|--:|---|
| 0 | 712 | **Champion** |
| 1 | 711 | **2nd Place** |
| 2 | 710 | **3rd Place** |
| 3 | 708 | **Best 4** |
| 4 | 704 | **Lost in Round 3** |
| 5 | 703 | **Lost in Round 2** |
| 6 | 702 | **Lost in Round 1** |

Et il s'affiche dans le libellé **660 « Your result: %s »** du §17.13. Les
sept valeurs couvrent exactement les sorties possibles d'un tableau à cinq
tours.

#### `Announce` : le TYPE de prix, et le nom du tournoi

- `auStack_d0 = { 0x28B, 0x28A, 0x289 }` = **Item**, **Emblem**, **Gold** —
  les trois mêmes que `MessageInfo`, affichés dans **« Prize: %s »**
  (libellés 612 et 609). Cela recoupe une troisième fois les trois barèmes
  du §17.14 ;
- et le nom du tournoi :
  `FUN_82322798(*(u32 *)(&DAT_82656798 + n * 0x34))` — **le MOT 0 de la table
  des événements**. Le §16.2 l'avait lu comme « un identifiant de libellé » ;
  **c'est confirmé par son lecteur**, et puisque les mots 0 des événements 0 à
  6 valent 528 à 534, soit les sept lieux nommés du §9.21, **les sept premiers
  tournois portent le nom de leur lieu**.

### 17.16 LES GARDES DES SIX ÉCRANS

`FUN_822E2DD8(p)` ne fait qu'une chose : **`return *p == 4;`** — l'état 4
d'un objet de fenêtre veut dire « ouverte ». C'est le même test que le §16.1
voyait dans `FUN_82307610`.

Et l'objet de fenêtre **est aussi le jeu d'ancres** passé à `FUN_822E39C0` :

| écran | sous-objet | sa garde |
|---|---|---|
| `Announce` | **+0xB8** | la fenêtre est ouverte |
| `Entry` | **+0x5C** | la fenêtre est ouverte |
| `MessageInfo` | **+0x50** | la fenêtre est ouverte |
| `List` | **+0xD0** | la fenêtre est ouverte |
| `MatchInfo` | +0xD8 | `[écran + 0x10C] == 0` |
| `ResultInfo` | +0x60 | `[écran + 0x50]` vaut 1 ou 2 |

Quatre écrans sur six attendent donc **leur propre fenêtre**, et les deux
autres gardent sur une étape de leur tâche. Chaque écran n'a **qu'un** objet
de fenêtre, qui porte à la fois son état et ses ancres — c'est l'objet unifié
du §9.20.

#### Ce qui reste du mode Quest, après tout ça

Les tournois sont lus de la donnée au pixel, **positions comprises depuis le
§17.17**. Et du §9.30, les points 4 et 5 sont traités au **§18**.

### 17.17 LES POSITIONS : elles sont dans `aet_n_qwin`, et elles sont CONSTANTES

Le §17.13 disait que les positions ne sont pas dans le code mais dans les
ancres des planches. Les voici.

#### D'abord une surprise : ce n'est pas `aet_n_tnt`

Les six écrans de tournoi ne citent **aucun** calque de `aet_n_tnt.bin` ni de
`aet_n_tnto.bin`. **Toutes leurs fenêtres vivent dans `aet_n_qwin.bin`** — la
planche des *fenêtres* du Quest —, et chaque écran y est **une composition** :

| composition | écran |
|--:|---|
| **26** et **117** | `MessageInfo` (deux fois, aux mêmes positions) |
| **77** | `List` |
| **85** | `Entry` |
| **119** | `ResultInfo` |
| **121** | `MatchInfo` |

`aet_n_tnt` / `aet_n_tnto` portent donc le **tableau** (`tnt_hyou_*`,
`idoNN`, `tnt_move`) et non les fenêtres — ce qui est cohérent avec le §17.12,
où le code demandait la planche du tableau par un nom séparé.

#### Les positions, relevées

Scène `MAIN`, 1280 de large : **`x = 640` pour presque tout**, soit le centre
exact. Le suffixe `_ct` est donc bien « centre, haut », et son origine vaut
`(12, 0)` ; `_c` vaut `(12, 12)`, centré sur les deux axes.

| écran | fenêtre | position | origine |
|---|---|---|---|
| **ResultInfo** | `…rslt_win_logo_c` | 640, **148** | 12, 12 |
| | `…rslt_win_02_ct` (**RESULT**) | 640, **216** | 12, 0 |
| | `…rslt_win_03_ct` (*Final tournament results*) | 640, **531** | 12, 0 |
| | `…rslt_win_04_ct` (**OK**) | 640, **585** | 12, 0 |
| **MatchInfo** | `…vs_win_logo_c` | 640, **148** | 12, 12 |
| | `…vs_win_02_ct` (les combattants) | 640, **228** | 12, 0 |
| | `…vs_win_03_ct` (*Beginning match…*) | 640, **531** | 12, 0 |
| | `…vs_win_04_ct` (**OK**) | 640, **585** | 12, 0 |
| **Entry** | `p_rule_win_logo_01_c` | 640, **144** | 12, 12 |
| | `p_rule_win_26_02_ct` (les règles) | 640, **220** | 12, 0 |
| | `p_rule_win_30_03_ct` (*Do you want to enter…*) | 640, **432** | 12, 0 |
| | `p_rule_win_04_ct` (**Yes / No**) | 640, **462** | 12, 0 |
| **List** | `…list_win_01_ct` (le titre) | 640, **104** | 12, 0 |
| | `…list_arrow_up_c` | 640, **165** | 50, 12 |
| | `…list_win_hed_40_02_lt` | **410**, 200 | 0, 0 |
| | `…list_trophy_02_c` | **380**, 212 | 12, 12 |
| | `…list_arrow_down_c` | 640, **469** | 50, 12 |
| **MessageInfo** | `p_tnt_info_win_01_ct` | 640, **373** | 12, 0 |
| | `p_tnt_info_win_02_ct` | 640, **503** | 12, 0 |

**Aucune n'est animée** : les huit propriétés de la transforme portent une
clé unique, donc une valeur constante. La mise en page est donc entièrement
statique, et ces vingt lignes la décrivent en entier.

`List` est la seule à sortir du centre : son en-tête en `x = 410` et son
trophée en `x = 380` — c'est une liste alignée à gauche, et les deux flèches
restent centrées en haut et en bas de la zone de défilement (165 et 469).

#### UNE FENÊTRE MANQUE, et c'est un trou pour le portage

**`p_que_info_win_*`, les quatre fenêtres d'`Announce`, n'existent dans
AUCUNE des planches `aet_*.bin` du média de Final Showdown.** Balayage des
quatorze planches : zéro calque de ce nom.

Les cinq autres écrans sont donc posables tels quels ; **`Announce` demande
une planche que FS n'a pas**, et il faudra la prendre du média de 2007 comme
on a pris `vf5ps3_b03map.adx` (§15.1). C'est un constat, pas une estimation.

#### Une réserve d'OUTILLAGE, à vérifier avant de s'appuyer sur l'autre relevé

`tools/ancres_que.py` lit la position par **deux** indirections —
`v = u32(calque + 0x28)` puis `t = u32(v + 0x08)`, et prend `t + 0x10` /
`t + 0x18`. Or `tools/aet.py` documente, mesure à l'appui (les 640/384 de
`aet_n_adv`), que **le bloc de 48 octets EST en `calque + 0x28`**, avec
`Position.X` en `+0x14` et `Position.Y` en `+0x1C`.

Avec le chemin de `ancres_que.py` je lisais ici « animé ou sans
transformation » partout — et j'ai failli l'écrire. En passant par
`aet.transforme()`, les positions sortent, constantes et cohérentes
(640 = le centre). **Les deux lectures ne peuvent pas être toutes les deux
justes.** Je n'ai pas vérifié ce que cela change au relevé de la carte
(`analysis/quest/ancres_qwin.txt` et les ancres de `aet_n_que`) : à faire
avant de s'appuyer dessus.


## 18. LES ENTRÉES DE MENU INERTES, ET LES ÉCRANS D'OBJETS (2026-10-18)

Les points 4 et 5 du §9.30. Même méthode qu'au §17.13 : on relève les
fenêtres et les libellés, et `tools/quest_textes_map.h` les nomme.

### 18.1 LE MENU DE LA MAISON : six lignes, et un libellé SAUTÉ

Le dessin (`FUN_8230BEB0`, 468 octets, atteint par un thunk depuis le rang 4)
porte la table des lignes :

    local_80 = { 0x219, 0x21A, 0x21C, 0x21D, 0x21E, 0x21F };

| ligne | libellé | texte | câblée ? |
|--:|--:|---|---|
| 0 | 537 | **Customize** | **non** |
| 1 | 538 | **Status** | oui |
| 2 | 540 | **Quest settings** | **non** |
| 3 | 541 | **Save** | oui |
| 4 | 542 | **Return to Character Select** | oui |
| 5 | 543 | **End Quest Mode** | oui |

**Ce qui confirme le §9.30 au mot près** : quatre des six sont câblées, et les
deux qui ne le sont pas sont *Customize* et *Quest settings*.

**Et le libellé 539 est SAUTÉ** : la table va de `0x21A` à `0x21C`. Le 539
existe dans les textes de 2007 mais n'est pas dans le menu — et il ne figure
pas non plus dans notre import (`quest_textes_map.h` ne le porte pas). Une
septième ligne retirée avant la sortie, probablement.

Les deux lignes qui suivent dans la numérotation nomment l'écran voisin :
**544 « STATUS »** et **545 « Rivals defeated »**.

#### Le répartiteur a HUIT états, pas six

`FUN_8230C8A0` (le rang 2, l'update, 244 octets) est un pur répartiteur :

```c
if ([obj+0x4C] != [obj+0x50]) {       /* un changement demande */
    [obj+0x54] = [obj+0x4C];          /* l'etat precedent  */
    [obj+0x4C] = [obj+0x50];          /* le nouveau        */
    [obj+0x58] = 0;
}
switch ([obj+0x4C]) { case 0..7: … }
FUN_822E4D70(obj + 0x238);
```

Huit gestionnaires, dont deux portent une confirmation lue en clair :

| état | fonction | ce qu'il dit |
|--:|---|---|
| 5 | `0x8230BCC0` | **1504** *Are you sure you want to return to Character…* |
| 6 | `0x8230BDB8` | **1505** *Are you sure you want to return to the Main…* |

Les états 0 à 4 et 7 ne citent aucun libellé constant : ce sont le dessin, la
navigation et les sous-écrans.

### 18.2 `Quest settings` — l'écran existe, en entier

`TaskQuestOption`, rang 4 = `0x8230E360`, 896 octets :

| fenêtre | libellé |
|---|---|
| `p_q_opt_win_01_ct` | **540 « Quest settings »** — le même libellé que la ligne du menu |
| `p_q_opt_win_hed_30_02_lt` | variable : les intitulés des réglages |
| `p_q_opt_win_sel_30_02_rt` | variable : les valeurs choisies, **alignées à DROITE** (`_rt`) |
| `p_q_opt_win_30_03_ct` | variable |

La forme est celle d'un écran de réglages à deux colonnes — intitulé à gauche,
valeur à droite. **L'écran est écrit ; c'est son appel depuis le menu qui
manque**, ce qui est exactement ce que « inerte » voulait dire.

### 18.3 LES OBJETS ET LES EMBLÈMES : quatre écrans, tous présents

Point 5 du §9.30. Les quatre classes concernées portent leurs écrans :

#### `TaskItemShop` — la boutique (rang 2, 944 octets)

| fenêtre | rôle |
|---|---|
| `p_item_win_tit_ct` | le titre |
| `p_iteme_win_30_01_ct` | une ligne d'en-tête |
| `p_iteminfo_win_248x394_lt` | **le panneau de détail, 248 × 394** — la taille est dans le nom |
| `p_item_grid_01_lt` … `p_item_grid_05_lt` | **une grille de CINQ cases** |
| `p_itemshop_arrow_up/down/left/right_c` | quatre flèches |

et deux libellés : **291 « Select an item to buy. »** et **3 « .:Back
.:Enter »**. Une grille de cinq cases et quatre flèches : on défile en deux
dimensions.

#### `TaskQuestEmblemList` — la liste des emblèmes (rang 4, 856 octets)

| fenêtre | libellé |
|---|---|
| `p_embsel_win_01_ct` | **569 « EMBLEM LIST »** |
| `p_embsel_win_02_ct` | variable |
| `p_embsel_raito_rt` | **401 « % »** et **570 « Emblems collected: »** |
| `p_embsel_arrow_left_c` / `_right_c` | deux flèches |

`raito` est *ratio* en kana : c'est la fenêtre du pourcentage de collection,
alignée à droite. Elle se nourrit du champ de **256 bits** en `socle + 0x7D`
mesuré au §14.10.

#### `TaskNewItemList` — l'annonce des objets gagnés (rang 4, 736 octets)

`p_newitem_info_win_01_ct` avec **587 « Obtained the following item(s): »**,
`p_newitem_info_win_30_02_ct` (la liste), `p_newitem_info_win_03_ct` avec
**352 « OK »**, et deux flèches.

#### `TaskNewEmblemList` — son jumeau pour les emblèmes (604 octets)

Même forme, non détaillée ici.

### 18.4 Ce que cela change pour le portage, et ce qui reste

**Les écrans ne sont pas à écrire : ils sont écrits.** Pour *Customize*,
*Quest settings*, la boutique, les deux listes de nouveautés et la liste
d'emblèmes, le code de 2007 porte les fenêtres, les libellés et la
navigation. Ce qui manque est **le câblage** — l'appel depuis la ligne de
menu — et, côté FS, **les planches**.

Ce qui reste à mesurer :

1. **les planches** de ces écrans. Le §17.17 a montré que celles des tournois
   vivent dans `aet_n_qwin` et que **`p_que_info_win_*` manque à FS** : il
   faut le même relevé pour `p_home_menu_*`, `p_q_opt_*`, `p_item_*`,
   `p_embsel_*` et `p_newitem_*`. `tools/ancres_tnt.py` le fait, il suffit de
   lui donner ces motifs ;
2. **les libellés variables** de `Quest settings` : quels réglages, et quelles
   valeurs ;
3. **le lien menu → écran** : les huit états du répartiteur sont là, mais quel
   état ouvre quoi n'est lu que pour les deux confirmations ;
4. et les **trois entrées du dôme** et *Tournament dans une salle*, que le
   §9.30 citait : `TaskQuestTenpo` a son rang 4 en **feuille**, donc hors
   `.pdata`, et je ne l'ai pas relevé.

---

## 19. LES CINQ ÉCRANS, LA SALLE ET LE DÔME (2026-10-19)

Les quatre premiers points de la liste de reprise. Et d'abord un piège
d'outillage à lever, parce que tout le reste en dépend.

### 19.0 `ancres_que.py` LISAIT LA TRANSFORME AU MAUVAIS ENDROIT

La reprise laissait la question ouverte : `aet.py` dit que le bloc de 48
octets **est** ce que désigne le `u32` en `calque + 0x28` ; `ancres_que.py`
déréférençait une seconde fois. **Les deux ne pouvaient pas être justes.**

Mesure sur le cas dont la réponse est connue — la racine de la scène `MAIN`
de `aet_n_adv`, résolution 1280x768, dont les deux calques doivent donner le
centre :

| chemin | `logo_jpn` | `logo_usu` | `p_name_lt` de `aet_n_que` |
|---|---|---|---|
| **une** indirection (`aet.py`, `ancres_tnt.py`) | **(640, 384)** | **(640, 384)** | (279, 435) |
| **deux** indirections (`ancres_que.py`) | (None, None) | (None, None) | (0, 0) |

`aet.py` a raison. La seconde indirection lisait le **pointeur de clés
d'`Origine.X`** comme une adresse de bloc, d'où « animé » partout.
`ancres_que.py` est corrigé et rend maintenant les mêmes valeurs que
`ancres_tnt.py`.

**Et `analysis/quest/ancres_qwin.txt` est sain** : 182 lignes, aucune
mention « animé », valeurs plausibles — il n'est pas sorti du chemin fautif.
On peut s'y appuyer.

### 19.1 LES PLANCHES DES CINQ ÉCRANS — ET LA BOUTIQUE MANQUE À FS

`tools/ancres_ecrans.py`, posé pour ça, balaye les **quinze** `aet_*.bin` de
`runtime/media/vf5fs/vf5fs_media/rom/2d/` (et non six comme `ancres_tnt.py`),
parce qu'ici la réponse cherchée est un **manque** : il faut avoir regardé
partout pour l'affirmer.

Contrôle de l'instrument d'abord — il doit retrouver ce que le §17.17 a déjà
mesuré, et il le retrouve : `p_que_info_win` **introuvable dans les quinze**,
`p_status_win`, `p_store_menu_win` et `p_hall_menu_win` présents dans
`aet_n_qwin.bin`.

#### Ce que Final Showdown A

Tout dans `aet_n_qwin.bin`, scène `MAIN` :

| composition | calque | position | origine |
|--:|---|---|---|
| c87 | `p_home_menu_win_30_02_ct` | (640, 166) | (12, 0) |
| c87 | `p_home_menu_win_30_03_ct` | (640, 330) | (12, 0) |
| c83 | `p_q_opt_win_01_ct` | (640, 221) | (12, 0) |
| c83 | `p_q_opt_win_hed_30_02_lt` | (397, 287) | (0, 0) |
| c83 | `p_q_opt_win_sel_30_02_rt` | (992, 287) | (24, 0) |
| c83 | `p_q_opt_win_30_03_ct` | (640, 386) | (12, 0) |
| c81 | `p_embsel_win_01_ct` | (640, 96) | (12, 0) |
| c81 | `p_embsel_win_02_ct` | (640, 140) | (12, 0) |
| c81 | `p_embsel_win_03_ct` | (640, 435) | (12, 0) |
| c81 | `p_embsel_raito_rt` | (1021, 490) | (24, 0) |
| c81 | `p_embsel_arrow_left_c` / `_right_c` | (279, 154) / (1003, 154) | (12, 12) |
| c75 | `p_newitem_info_win_01_ct` | (640, 104) | (12, 0) |
| c75 | `p_newitem_info_win_30_02_ct` | (640, 200) | (12, 0) |
| c75 | `p_newitem_info_win_03_ct` | (640, 493) | (12, 0) |
| c75 | `p_newitem_arrow_up_c` / `_down_c` | (640, 165) / (640, 469) | (50, 12) |
| c70 | `p_newitem_info_win_01_ct` / `_03_ct` | (640, 104) / (640, 493) | (12, 0) |

Les compositions **c70 et c75 sont deux variantes** du même écran de
nouveautés : c70 sans liste ni flèches (un seul objet), c75 avec la liste
`_30_02_ct` et les deux flèches (plusieurs objets). La racine porte
`newitem_info_win` en (640, 360).

#### Ce que Final Showdown N'A PAS

**La boutique entière.** Les six noms que `TaskItemShop` demande (§18.3) sont
introuvables dans les quinze planches :

    p_item_win_tit_ct            INTROUVABLE
    p_iteme_win_30_01_ct         INTROUVABLE
    p_iteminfo_win_248x394_lt    INTROUVABLE
    p_item_grid_01..05_lt        INTROUVABLE
    p_itemshop_arrow_*_c         INTROUVABLE

Un balayage large (`--motif item --motif shop --motif grid`) ne rend que des
homonymes qui ne sont pas elle : `p_itemsel_icon_c` et `n_term_item_sel_bg`
(le **terminal**), `p_board_item_01..04_c` (`aet_n_cmn`),
`p_tnt_rslt_grid_01..04_lt` (les **tournois**), et `n_que_shop_*__n.pic` —
qui sont les **façades des salles sur la carte**, neuf images de décor, pas
une interface.

Et `p_home_menu_win_01_ct` n'existe pas non plus : **le menu de la maison n'a
pas de fenêtre de titre**, ses deux fenêtres sont `_30_02_ct` et `_30_03_ct`.
C'est cohérent avec son dessin (§19.3), qui n'en pose que deux.

**Donc la liste des manques de FS compte maintenant deux entrées** : les
quatre fenêtres d'`Announce` (`p_que_info_win_*`, §17.17) et **les six
fenêtres de la boutique**. Dans les deux cas il faudra les prendre au média
de 2007 — qui n'est pas extrait : `extracted/X360_menu/` ne porte que les
neuf planches de FS console, et `extracted/X360_VF5/` que l'image `.img`.

### 19.2 `Quest settings` EN ENTIER — deux réglages, deux commandes

`FUN_8230E360` (le rang 4 de `TaskQuestOption`, 896 octets) porte **quatre**
tables de pile, et la quatrième est un tableau de **pointeurs** :

```c
uStack_a0 = { 0x232, 0x236 };              /* les intitules        */
uStack_b0 = { 0x233, 0x234, 0x235 };       /* valeurs du reglage 0 */
uStack_d0 = { 0x238, 0x237 };              /* valeurs du reglage 1 */
uStack_98 = { 0x444, 0x445 };              /* les deux commandes   */
puStack_c8 = &uStack_b0;  puStack_c4 = &uStack_d0;
… FUN_82322798((*ppuVar5)[*piVar6]);       /* ppuVar5 = &puStack_c8 */
                                           /* piVar6  = obj + 0x154 */
```

Le titre est le libellé **540 « Quest settings »**, le même que la ligne du
menu. Les quatre lignes :

| ligne | fenêtre | intitulé | valeurs possibles | champ |
|--:|---|---|---|---|
| 0 | `hed_30_02_lt` / `sel_30_02_rt` | **562 Difficulty** | **563 Normal**, **564 Hard**, **565 Expert** | `[obj+0x154]` |
| 1 | `hed_30_02_lt` / `sel_30_02_rt` | **566 Commentary** | **568 Off**, **567 On** | `[obj+0x158]` |
| 2 | `_30_03_ct` | **1092 Return to defaults** | — | — |
| 3 | `_30_03_ct` | **1093 End adjustment** | — | — |

**Noter l'ordre de la seconde table : 568 *Off* d'abord, 567 *On* ensuite.**
L'index 0 est donc *Off*, et `[obj+0x158]` n'est pas un booléen naïf.

Le curseur est `[obj+0x4C]`, quatre positions ; en dessous de 2 il est posé
par `FUN_822E5380(x - 36, y)` (la colonne de droite), au-delà par
`FUN_822E3228(obj + 0x198)`.

#### Deux mesures de portée générale, tombées avec cet écran

**1. L'alignement est un OCTET DE TÊTE de la chaîne, pas un paramètre.**
Quatre sites dans cette seule fonction, et les quatre concordent avec le
suffixe du nom d'ancre :

| ancre | appel | préfixe |
|---|---|---|
| `p_q_opt_win_01_ct` | `FUN_8223FE30("%s%s", "\x02", t)` | **`\x02`** = centré |
| `..._hed_30_02_lt` | `FUN_8223FE30("%s", t)` | **aucun** = à gauche |
| `..._sel_30_02_rt` | `FUN_8223FE30("%s%s", "\x03", t)` | **`\x03`** = à droite |
| `..._30_03_ct` | `FUN_8223FE30("%s%s", "\x02", t)` | **`\x02`** = centré |

(`0x82000F80` = `"%s%s"`, `0x82000F88` = `"\x02"`, `0x82000F08` = `"%s"`,
`0x82010300` = `"\x03"`. Et `0x8208476C` = `"\x02%s"` — le même `\x02`
soudé au format, employé par la salle.)

**2. Le `_30_` du nom de fenêtre est l'INTERLIGNE, en pixels.** Le pas
vertical de la boucle est `DAT_82011814`, et il vaut **30.0**. La lecture
« `p_que_info_win_36_02_ct` a donc un interligne de 36 » est cohérente mais
**n'est pas mesurée** : elle demanderait de lire le pas d'`Announce`.

### 19.3 LE MENU DE LA MAISON : les huit états sont NOMMÉS, et le §18.1 est à corriger

#### Le dessin, d'abord — et la ligne *Save* est grisée sous condition

`FUN_8230BEB0` pose **deux** fenêtres, pas une :

    lignes 0 a 3  ->  p_home_menu_win_30_02_ct
    lignes 4 et 5 ->  p_home_menu_win_30_03_ct

Le curseur du menu est **`[obj+0x5C]`**, pas `+0x4C` (qui est l'état). Et à
la ligne 3 :

```c
if (iVar5 == 3) {
    FUN_82144c28();
    if (FUN_82144cb0() == '\0') uVar6 = 0xffffffffff7f7f7f;   /* grise */
}
```

**La ligne *Save* se grise quand `FUN_82144CB0()` rend 0.** Le même test
apparaît dans la navigation, où il fait **sauter** la ligne :

```c
if (*piVar8 == 3) { … if (FUN_82144cb0() == '\0') { *piVar8 = 4; } }
```

C'est très exactement le mécanisme que FS emploie pour ses entrées de menu
grisées (l'octet d'état, §5 de la reprise), mais écrit à la main, ligne par
ligne.

#### Le texte d'aide, et le libellé 539 enfin expliqué

L'état 0 écrit deux textes dans l'objet :

```c
auStack_50 = { 0x89, 0x8a, 0x8c, 0x8d, 0x8e, 0x8f };
[obj+0xAC]  = FUN_82322798(auStack_50[[obj+0x5C]]);   /* l'aide */
[obj+0x130] = FUN_82322798(3);                        /* « .:Back  .:Enter » */
```

| ligne | titre | aide |
|--:|---|---|
| 0 | 537 Customize | **137** *Purchase items or adjust settings.* |
| 1 | 538 Status | **138** *View various records.* |
| 2 | 540 Quest settings | **140** *Adjust difficulty level and commentary setti…* |
| 3 | 541 Save | **141** *Save current settings.* |
| 4 | 542 Return to Character Select | **142** *Return to the Character Select Screen.* |
| 5 | 543 End Quest Mode | **143** *End Quest Mode and return to the Main Menu.* |

**La table d'aide saute 139 exactement comme la table des titres saute 539**,
et le texte du 139 dit ce qui s'est passé : **139 = *Adjust the difficulty
level.*** contre **140 = *Adjust difficulty level and commentary
settings.*** La septième ligne retirée était un réglage de **difficulté
seule** ; elle a été **fondue** dans *Quest settings*, qui porte les deux
réglages du §19.2. Le §18.1 disait « une septième ligne retirée,
probablement » — c'est lu, et ce n'est pas une suppression, c'est une fusion.

#### Les huit états, et ce que chacun ouvre

L'état 0 (`FUN_8230C3A8`) est la navigation. Son sous-état 2 porte la table
ligne → état, et elle est **triviale : état = ligne + 1**.

| état | fonction | ce qu'il ouvre | démarre / attend |
|--:|---|---|---|
| 0 | `0x8230C3A8` | **la navigation du menu** | — |
| 1 | `0x8230B8E0` | **Customize** | `FUN_8230B4C0` / `FUN_8230B4B0` |
| 2 | `0x8230BAC8` | **Status** | `FUN_8230E9F0` / `FUN_8230EA08` |
| 3 | `0x8230BB68` | **Quest settings** | `FUN_8230E0D0` / `FUN_8230E0F0` |
| 4 | `0x8230BC08` | **Save** | `FUN_8230DB10` + `FUN_82315930`/`FUN_82315D00`, puis `FUN_821D05F8` |
| 5 | `0x8230BCC0` | **Return to Character Select** — confirmation **1504** | `FUN_82300238(1)` |
| 6 | `0x8230BDB8` | **Return to the Main Menu** — confirmation **1505** | `FUN_82300238(0)` |
| 7 | `0x8230C6D8` | **les effets de fin de Quest** — tâche `TASK_QUEST_COMPLET_EEFFECTS` | — |

L'état **7 n'est pas une ligne de menu** : il est demandé par le sous-état 1
de l'état 0, quand quatre conditions tiennent à la fois (`FUN_822DAC30` et
son bit 23, `FUN_8230FF88`, `FUN_82310238` sur `[profil+0xF8]`,
`FUN_823103C8`) — c'est la séquence de **Quest terminé**, déclenchée toute
seule à l'ouverture du menu.

Les deux confirmations ne diffèrent que par `FUN_82300238(1)` contre
`FUN_82300238(0)` et le libellé ; tout le reste de leur corps est identique,
y compris l'appel de vtable `(**(code **)(*FUN_82308480() + 0xC))()` et
`FUN_8220D1E0(0x59)`.

Trois noms de tâche/fenêtre sortent de là, et ils complètent le §15 :
`QUEST_HOME_MENU` (`0x8208E098`, la fenêtre de confirmation en `obj+0x140`),
`QUEST_HOME_EXPLAIN` (`obj+0x60`), `QUEST_HOME_CONTROL` (`obj+0xE4`), et
`sound/bgm/vf5ps3_b03map.adx` que l'état 1 **rejoue** en revenant de
*Customize*.

#### CE QUI EST À CORRIGER AU §18.1

Le §18.1 écrivait « quatre câblées » et donnait *Customize* et *Quest
settings* pour non câblées. **C'est faux pour le code de 2007 : les six
lignes sont câblées**, chacune vers son état, et chaque état appelle le
démarrage de son écran. La phrase du §9.30 d'où venait le « quatre » disait
« les autres entrées des menus, **qui ne font rien aujourd'hui** » — un
constat sur **l'état du portage**, pas sur le code de 2007. Le §18.1 l'a lu
comme une propriété du binaire d'origine.

### 19.4 `TaskQuestTenpo` : LA SALLE, ET LE DÔME

Le rang 4 (`0x82315138`) n'est pas un dessin : c'est un **répartiteur à deux
branches** sur `[obj+0xD0]` — `FUN_82313EA8` pour 0, `FUN_82311CD8` pour 1.
Voilà pourquoi `x360_mise_en_page.py` n'en tirait rien : la mise en page est
un étage plus bas, et le fait qu'il soit une feuille hors `.pdata` n'y était
pour rien.

Le rang 2 (`0x82315798`) répartit **sept** états sur le même `[obj+0xD0]`,
avec le trio `+0xD0` courant / `+0xD4` demandé / `+0xD8` précédent (et
`+0xDC` le sous-état), la même mécanique que le menu de la maison :

    0 -> 0x823130B8   1 -> 0x82312BF0   2 -> 0x82312E58   3 -> 0x82311790
    4 -> 0x823119F0   5 -> 0x823156E8   6 -> 0x82311C48

Et le rang 1 (`0x82315500`) choisit l'état d'entrée :

```c
if (FUN_82315158(obj + 0xE0))  etat = 5;
else if (FUN_82315308(obj + 0x210)) etat = 6;
else etat = ([obj+0x4C] == 7);          /* 1 pour le lieu 7, 0 sinon */
```

**`[obj+0x4C]` est le LIEU**, et le lieu **7** a son écran à lui.

#### La salle ordinaire (état 0, dessin `FUN_82313EA8`)

Le titre est `p_store_menu_win_01_ct` et son libellé est **`528 + [obj+0x4C]`**
— la table de pile `local_210 = { 528 … 535 }`, huit entrées :

| lieu | libellé | nom |
|--:|--:|---|
| 0 | 528 | SEGA WORLD NORTH |
| 1 | 529 | SEGA WORLD SOUTH |
| 2 | 530 | SEGA WORLD ROUTE 101 |
| 3 | 531 | CLUB SEGA DOWNTOWN |
| 4 | 532 | CLUB SEGA BAY AREA |
| 5 | 533 | SEGA ARENA COAST |
| 6 | 534 | SEGA ARENA EAST |
| **7** | **535** | **EVENT SQUARE** |

Les sept lieux du §9.21 en font **huit** : le huitième est le dôme, et c'est
pour lui que le rang 1 bascule sur l'état 1.

**Cinq lignes**, curseur `[obj+0x50]` :

| ligne | ancre | contenu | aide |
|--:|---|---|---|
| 0 | `c_button_csr_a_01_lt` | l'adversaire de la borne 1 | **146** *Play against the opponent on Unit 1.* |
| 1 | `c_button_csr_a_02_lt` | l'adversaire de la borne 2 | **147** *…Unit 2.* |
| 2 | `c_button_csr_a_03_lt` | l'adversaire de la borne 3 | **148** *…Unit 3.* |
| 3 | `c_button_csr_b_01_lt` | **592 Tournament** + **593 Currently not in progress.** | **150** *Participate in a tournament.* |
| 4 | `c_button_csr_a_04_lt` | **594 Customize** | **153** *Purchase items or adjust settings.* |

Les cinq ancres sont **exactement** les cinq que `ancres_qwin.txt` relève
dans la composition `store_menu_win` (§17.17), et le nom de l'ancre des trois
premières est **fabriqué** : `FUN_82249520(tampon, 0x20,
"c_button_csr_a_%02d_lt", i + 1)`.

Les trois adversaires sont trois tranches de **0x24 octets en `obj + 0x64`**.
Pour chacun : le nom par `FUN_8230DDF0`, le grade par `FUN_82309BA0`, le
portrait ou l'icône par `FUN_82309E20`, et — quand `FUN_821D1808` rend vrai
sur `[profil + 0xF4]` — une **étoile** : la chaîne `0x820117C8` vaut
`\x81\x9a`, soit **★ en Shift-JIS**, posée alignée à droite (`\x03`) en
couleur `0xFFFFFF00`. C'est le bit `+0xF4` du §14, et il se voit ici.

L'aide **149 « %s is on a %d-win streak! »** est montée à part, par
`FUN_82249520(tampon, 0x80, texte(149), nom, serie)`, et le tout est assemblé
dans `"%s\n%s%s"` avec un `\x14` au milieu (`0x8208E62C`) — un second code de
contrôle de texte, non identifié.

Ce que la validation fait, lu dans `FUN_823130B8` sous-état 3 :

| curseur | effet |
|--:|---|
| 0, 1, 2 | `FUN_82320150([obj+0x64 + i*0x24])` puis **`FUN_8220D1E0(0x56)`** — le sous-état du combat |
| 3 | `[obj+0xD4] = 3` → l'état 3 du répartiteur (`0x82311790`), **le tournoi dans une salle** |
| 4 | `[obj+0xD4] = 2` → l'état 2 (`0x82312E58`), **Customize** |

Et les libellés **589 « 1 »**, **590 « 2 »**, **591 « 3 »** de la table
`local_230` sont les **numéros de borne** — ils concordent avec les aides
146-148 (*Unit 1/2/3*). `FUN_82313EA8` ne les lit pas (il n'indexe
`local_230` qu'en [3] et [4]) : ils sont posés ailleurs, non relevé.

#### Le dôme (état 1, dessin `FUN_82311CD8`) — LES TROIS ENTRÉES

Titre `p_hall_menu_win_01_ct`, libellé **0x217 = 535 « EVENT SQUARE »**.
Trois lignes, et les trois ancres sont **en dur**, dans un tableau de
pointeurs de pile :

```c
apcStack_b0[0] = "c_button_csr_c_01_lt";
apcStack_b0[1] = "c_button_csr_d_01_lt";
apcStack_b0[2] = "c_button_csr_d_02_lt";
auStack_c0[0] = FUN_82317860(1) ? 599 : 600;
auStack_c0[1] = 0x259;  /* 601 */
auStack_c0[2] = 0x25a;  /* 602 */
```

| ligne | ancre | contenu | aide |
|--:|---|---|---|
| 0 | `c_button_csr_c_01_lt` | **599 Official Tournaments**, puis **600 Currently not in progress.** — ou, si `FUN_82317860(1)` rend vrai, le bloc du tournoi en cours (`FUN_82309FF8(…, FUN_82316390(1), …)`) | — |
| 1 | `c_button_csr_d_01_lt` | **601 List of official tournaments** | **152** *View official tournaments you have cleared.* |
| 2 | `c_button_csr_d_02_lt` | **602 Customize** | — |

Les trois ancres sont **exactement** les trois que `ancres_qwin.txt` relève
dans `hall_menu_win`. Le point 4 du §9.30 — « les trois entrées du dôme et
*Tournament dans une salle* » — est donc **lu en entier** : ce sont les trois
lignes ci-dessus, et la ligne 3 de la salle ordinaire.

### 19.5 CE QUE CES QUATRE ÉTAPES LAISSENT

- **la boutique n'a pas de planche dans FS** (§19.1) : six fenêtres à
  reprendre au média de 2007, qui n'est pas extrait ;
- `p_que_info_win_*` toujours manquant (§17.17), même média à sortir ;
- le pas vertical des fenêtres `_36_` n'est pas mesuré (§19.2) ;
- les libellés 589/590/591 (les numéros de borne) sont posés par une
  fonction non identifiée (§19.4) ;
- le code de contrôle de texte `\x14` (`0x8208E62C`) n'est pas identifié ;
- les états 2 à 6 de `TaskQuestTenpo` (`0x82312E58`, `0x82311790`,
  `0x823119F0`, `0x823156E8`, `0x82311C48`) sont décompilés mais non relevés.

### 19.6 LES MUSIQUES DU QUEST : UNE POSÉE, QUATORZE QUI MANQUENT — le §17.8 est à corriger

*(Le compte de ce paragraphe a été relevé une première fois à onze. Le §20.2
l'a porté à quatorze en lisant `FUN_8231E538` : trois jingles d'ouverture
s'ajoutent. Le tableau ci-dessous est celui du premier relevé ; le tableau
complet est au §20.2.)*

Relevé par `tools/quest_x360.py --chaine "vf5ps3_b"`, qui donne pour chaque
chaîne **qui construit son adresse** dans l'image de 2007.

#### Ce qui est posé, et joué

**`vf5ps3_b03map.adx`** — la musique de la carte, de la maison et des salles.
Cinq demandeurs :

    0x8230B7D0  0x8230B8E0   TaskQuestHomeMenu (dont l etat 1, §19.3)
    0x8230CBC0               TaskQuestMap
    0x82312E58  0x82315500   TaskQuestTenpo (son init, §19.4)

Elle est **dans le média de FS** (`rom/sound/bgm/vf5ps3_b03map.adx`,
5 836 800 octets, posée par `tools/musique_quest.py`) et **elle joue** : le
journal d'exécution `runtime/media/vf5fs/quest_journal.txt` du 2026-10-18
porte sept `[quest] musique du Quest lancee` et deux `arretee`. C'est une
mesure d'exécution, pas une lecture de code.

#### CE QUI MANQUE, et le §17.8 comptait trois au lieu de neuf

Le §17.8 écrit « **trois** musiques de tournoi : `vf5ps3_b08tn1`, `b06tn1`,
`b04tn1` — donc **quatre fichiers**, pas un ». **Il y en a neuf**, et une
seule fonction en demande les neuf : `FUN_8231F1D8`, le **niveau 2 du
séquenceur de tournoi** (celui que le §17.9 décrit au cas 1).

| chaîne | demandeurs | dans FS ? | dans le média de 2007 ? |
|---|---|:-:|:-:|
| `vf5ps3_b04tn1.adx` | `0x8231E538`, `0x8231F1D8` | **non** | oui |
| `vf5ps3_b06tn1.adx` | `0x8231E538`, `0x8231F1D8` | **non** | oui |
| `vf5ps3_b08tn1.adx` | `0x822D47B0`, `0x822D5FC8`, `0x822FE908`, `0x8231E538`, `0x8231F1D8` | **non** | oui |
| `vf5ps3_b05tn2.adx` | `0x8231F1D8` | **non** | oui |
| `vf5ps3_b07tn2.adx` | `0x8231F1D8` | **non** | oui |
| `vf5ps3_b09tn2.adx` | `0x8231F1D8` | **non** | oui |
| `vf5ps3_b10ke1.adx` | `0x8231F1D8` | **non** | oui |
| `vf5ps3_b11ke2.adx` | `0x8231F1D8` | **non** | oui |
| `vf5ps3_b12ke3.adx` | `0x8231F1D8` | **non** | oui |

**Les noms vont par paires `tnN` / `tnN+1`** — 04/05, 06/07, 08/09 — soit
**trois jeux de deux**, et non trois morceaux. `0x8231E538` ne demande que les
trois `tn1` ; `0x8231F1D8` demande les six, plus les trois `ke`. Ce que
`tn1`/`tn2` distinguent (entrée et boucle ? tour et finale ?) et ce que `ke`
désigne **ne sont pas lus** : il faut lire `FUN_8231F1D8` pour le dire, et
c'est le niveau 2 du séquenceur, treize étapes.

Deux autres, hors tournoi, demandées par `0x822F4F98` : `vf5ps3_b16tse.adx`
et `vf5ps3_b17tco.adx`. Et deux encore, `b13end` (`0x822CFD88`) et
`b02stg`/`b14stg`/`b15tim`, qui ne sont pas du mode Quest.

#### Où elles sont

    source   C:\Users\frede\Desktop\VF5 FS DECOMP\X360_VF5\media\sound\bgm\
    cible    runtime/media/vf5fs/vf5fs_media/rom/sound/bgm/

Le dossier source porte `b01men`, `b01men_51`, `b02stg`, `b03map`, `b04tn1`,
`b05tn2`, `b06tn1`, `b07tn2`, `b08tn1`, `b09tn2`, `b10ke1`, `b11ke2` et
`b12ke3`, ainsi que `j24`, `j25`, `j26`, `b16tse` et `b17tco`. **Les quatorze
manquantes sont donc toutes disponibles** : c'est une copie de fichiers, pas
une recherche.

`tools/musique_quest.py` ne connaît que `b03map` : il faudra l'étendre, ou
poser un outil du même dessin pour le lot.

---

## 20. LES PLANCHES RETROUVÉES, LES DOUZE MUSIQUES, ET TENPO AU COMPLET (2026-10-19)

Quatre chantiers, dans l'ordre demandé : les planches de 2007, le niveau 2 du
séquenceur de tournoi, les cinq états restants de `TaskQuestTenpo`, et les
points ouverts du §19.5.

### 20.1 LES PLANCHES MANQUANTES SONT TROUVÉES — et il n'y avait rien à extraire

**Le média 2D de 2007 était déjà extrait.** Le §19.1 concluait qu'il fallait
l'en tirer ; il était là depuis le début, à deux endroits :

    C:/Users/frede/Desktop/VF5 FS DECOMP/X360_VF5/media/rom/2d          265 fichiers
    C:/Users/frede/Desktop/VF5 FS DECOMP/X360_VF5/media/lang/en/rom/2d  la version ANGLAISE

Les deux portent vingt-sept `aet_*.bin` et **diffèrent** (`aet_n_cmn.bin` et
`aet_n_cstm.bin` ne sont pas identiques d'un dossier à l'autre). C'est celui
de `lang/en` que `tools/bases_2d.py` emploie déjà pour `que`, `qwin`, `tnt`,
`tnto` et `qdan` : c'est donc lui qui fait foi.

`tools/ancres_ecrans.py` reçoit `--2007` et `--dossier <d>` pour les lire. Et
**le lecteur AET de FS les lit sans rien changer** : les positions tombent sur
des entiers ronds, donc le format est petit-boutien des deux côtés — la
planche d'une Xbox 360 n'est pas gros-boutienne.

#### Les quatre fenêtres d'`Announce` sont dans `aet_n_cmn.bin` de 2007

Scènes `MAIN` et `MAIN_VGA`, composition c82 (c79 dans l'autre dossier),
positions identiques dans les deux :

| calque | position | origine |
|---|---|---|
| `p_que_info_win_01_ct` | (640, 185) | (12, 0) |
| `p_que_info_win_36_02_ct` | (640, 247) | (12, 0) |
| `p_que_info_win_03_ct` | (640, 346) | (12, 0) |
| `p_que_info_win_30_04_ct` | (640, 408) | (12, 0) |

#### La boutique est dans `aet_n_cstm.bin` — et ce sont DEUX écrans jumeaux

Et c'est la découverte du relevé : `aet_n_cstm.bin` porte **deux
compositions sœurs**, c4 et c5, qui partagent le titre, l'en-tête et la grille
de cinq cases, et ne diffèrent que par le panneau latéral et le jeu de
flèches.

| calque | position | c4 | c5 |
|---|---|:-:|:-:|
| `p_item_win_tit_ct` | (640, 95) | oui | oui |
| `p_iteme_win_30_01_ct` | (770, 141) | oui | oui |
| `p_item_grid_01_lt` | (520, 210) | oui | oui |
| `p_item_grid_02_lt` | (520, 266) | oui | oui |
| `p_item_grid_03_lt` | (520, 322) | oui | oui |
| `p_item_grid_04_lt` | (520, 378) | oui | oui |
| `p_item_grid_05_lt` | (520, 434) | oui | oui |
| `p_itempoint_win_248x72_lt` | (256, 451) | **oui** | non |
| `p_itemedit_arrow_up/down/left/right` | (770,192) (770,514) (538,154) (1003,154) | **oui** | non |
| `p_iteminfo_win_248x394_lt` | (256, 129) | non | **oui** |
| `p_itemshop_arrow_up/down/left/right` | mêmes quatre positions | non | **oui** |

**c4 est l'ÉDITEUR de tenue** (le panneau `248x72` des points, flèches
`itemedit`) et **c5 est la BOUTIQUE** (le panneau de détail `248x394`, flèches
`itemshop`) — celle que `TaskItemShop` demande au §18.3, avec sa grille de
cinq cases et ses quatre flèches, exactement.

La grille est **verticale, pas en deux dimensions** : cinq cases en x = 520,
de y = 210 à y = 434, pas de 56. Les quatre flèches servent donc au défilement
de la liste (haut/bas) et au changement de catégorie (gauche/droite), pas à
une navigation en grille — ce que le §18.3 supposait.

#### Les jeux de sprites sont là aussi

`spr_n_cmn.farc` et `spr_n_cstm.farc`, dans le même dossier. **Rien ne manque
plus pour ces deux écrans.** Ce qui reste est de les déclarer, et c'est la
recette éprouvée : deux entrées dans `PLANCHES` de `tools/bases_2d.py`, puis
`--ajouter`. Attention au nom : FS a déjà un `N_CMN`, et la note de `qdan`
rappelle qu'un nom d'emprunt a cassé 212 liens de sprites.

### 20.2 LES MUSIQUES DU TOURNOI : TROIS NIVEAUX, QUATRE MOMENTS, DOUZE FICHIERS

`FUN_8231F1D8` — le niveau 2 du séquenceur, treize étapes — et
`FUN_8231E538` — `TASK_TOURNAMENT_OPENING` — portent toute la logique.

#### Le niveau d'un tournoi, et il a un nom japonais

`FUN_8231E538` joue, à son étape 0, un jingle **et une voix**, indexés par
`[obj+0x58]` :

| `[obj+0x58]` | jingle | voix | `taikai` = 大会, « tournoi » |
|--:|---|---|---|
| 0 | `vf5ps3_j26.adx` | **`tnm_taikai_tenpo`** | *tenpo* = 店舗, **la salle** |
| 1 | `vf5ps3_j25.adx` | **`tnm_taikai_normal`** | le tournoi **officiel ordinaire** |
| 2 | `vf5ps3_j24.adx` | **`tnm_taikai_final`** | **la finale** |

**Les trois niveaux sont donc exactement les trois tournois du §19.4** :
*Tournament* à la ligne 3 d'une salle, *Official Tournaments* au dôme, et le
grand tournoi. La voix est jouée par `FUN_822B3AC0(nom)` — le joueur **par
nom** du §15, celui des bruitages.

#### Et le niveau choisit la musique, par `FUN_823158C0(événement)`

Les deux blocs de `FUN_8231F1D8` sont identiques à la chaîne près, et
`[obj+0x5C]` dit lequel on est en train de jouer :

```c
evt = *piVar2;                           /* le numero d evenement, 0..14 */
if (evt == 0xE)                 jouer(0, <b08tn1 | b09tn2>);
else if (FUN_823158c0(evt) != 0) {
    if (FUN_823158c0(evt) == 1) jouer(0, <b06tn1 | b07tn2>);
    /* sinon : RIEN n est joue */
} else                          jouer(0, <b04tn1 | b05tn2>);
```

| niveau | première moitié (`[obj+0x5C]=0`) | seconde moitié (`=1`) |
|---|---|---|
| `FUN_823158C0(evt) == 0` — la salle | `vf5ps3_b04tn1.adx` | `vf5ps3_b05tn2.adx` |
| `== 1` — officiel ordinaire | `vf5ps3_b06tn1.adx` | `vf5ps3_b07tn2.adx` |
| **événement 14** — le quinzième | `vf5ps3_b08tn1.adx` | `vf5ps3_b09tn2.adx` |

**`tn1` et `tn2` ne sont pas deux morceaux différents : c'est AVANT et APRÈS
LES DEMI-FINALES.** Le basculement de `[obj+0x5C]` de 0 à 1 se fait au cas 2
sous la condition `desc[6] == 3` — et le §17.15 a mesuré que le type de tour
**3 est `Semifinals`**. L'autre entrée du même bloc vient du cas 0 quand
`FUN_82315A90(evt)` rend 6.

**Et un trou qui n'existe pas.** J'avais écrit ici qu'« aucune musique n'est
jouée si `FUN_823158C0(evt) >= 2` ». **C'est faux**, et l'audit du §21.2 le
montre : `FUN_823158C0` est un pur test d'intervalle qui ne rend que 0 (pour
0..6), 1 (pour 7..14) ou -1 (hors bornes). Pour un événement valide la branche
muette est **inatteignable**. Je n'avais pas lu la fonction ; je l'avais
déduite de la forme du `if`.

#### Les trois `ke` sont LA FINALE

Cas 8, sous `desc[6] == 4` — et le §17.15 a mesuré que **4 est `Final`** :

```c
if (desc[6] == 4) {
    if (FUN_82315be8(bloc))  jouer(0, vf5ps3_b11ke2);
    else if (evt != 0xE)     jouer(0, vf5ps3_b10ke1);
    else                     jouer(0, vf5ps3_b12ke3);
}
```

`FUN_82315BE8` prend **le bloc du tournoi**, pas le numéro d'événement (§21.4
le lit) : il remonte `bloc + 0x488` par pas de -0x10, soixante-quatre fois, et
rend l'octet `+2` du premier enregistrement dont le bit `0x40` est posé.

`ke` est vraisemblablement 決勝 (*kesshō*, « finale ») — **lecture, non
mesurée** : le code ne nomme rien. Ce qui est mesuré, c'est que les trois ne
sont joués que sur le tour de type 4.

#### Deux de plus, et ce sont celles de *Customize*

`FUN_822F4F98` est la mise à jour de l'écran **Customize** du Quest (il crée
`CUSTOMIZE_MENU_EXPLAIN`, `CUSTOMIZE_MENU_CONTROL`, `CUSTOMIZE_PLAYER_INFO`
et la planche `cstm_title`) :

    [obj+0x58] == 1  ->  vf5ps3_b16tse.adx
    sinon            ->  vf5ps3_b17tco.adx

#### L'ÉTAT DES QUINZE FICHIERS

Relevé sur les trois arbres. « FS d'origine » est
`VF5 FS DECOMP/APM3_US/.../rom/sound/bgm`.

| fichier | 2007 | FS d'origine | notre arbre |
|---|:-:|:-:|:-:|
| `vf5ps3_b03map.adx` | oui | **import** | **oui, et il JOUE** |
| `vf5ps3_j24/j25/j26.adx` | oui | non | non |
| `vf5ps3_b04tn1/b05tn2.adx` | oui | non | non |
| `vf5ps3_b06tn1/b07tn2.adx` | oui | non | non |
| `vf5ps3_b08tn1/b09tn2.adx` | oui | non | non |
| `vf5ps3_b10ke1/b11ke2/b12ke3.adx` | oui | non | non |
| `vf5ps3_b16tse/b17tco.adx` | oui | non | non |

**`b03map` joue**, et c'est une mesure d'exécution, pas de code : le journal
`runtime/media/vf5fs/quest_journal.txt` du 2026-10-18 porte sept
`[quest] musique du Quest lancee` et deux `arretee`.

**Et FS ne l'a jamais eue.** La copie qui vit dans `APM3_US` porte la date de
l'extraction de 2007 (2018-02-21) alors que toutes les musiques propres à FS
sont du 2020-08-14 : c'est un import d'une séance précédente, pas du contenu
d'origine.

Les quatorze autres sont **toutes présentes** dans
`VF5 FS DECOMP/X360_VF5/media/sound/bgm`. C'est une copie de fichiers.
`tools/musique_quest.py` ne connaît que `b03map` ; il faut l'étendre au lot.

### 20.3 `TaskQuestTenpo` : LES SEPT ÉTATS, AU COMPLET

Le §19.4 avait lu l'init, le répartiteur et les deux dessins. Voici les cinq
états que l'on n'avait pas relevés. Le trio de champs est celui du §19.4 :
`+0xD0` courant, `+0xD4` demandé, `+0xD8` précédent, `+0xDC` sous-état.

**Et une formule revient partout** : `[obj+0xD4] = LZCOUNT([obj+0x4C] - 7) >> 5`,
qui vaut **1 si le lieu est 7, 0 sinon** — c'est-à-dire « retourne à l'écran
du dôme, ou à celui de la salle », le même test que l'init.

| état | fonction | ce qu'il est | il sort vers |
|--:|---|---|---|
| 0 | `0x823130B8` | la **navigation de la salle** (§19.4) | 0x56 (combat), état 3, état 2 |
| **1** | `0x82312BF0` | la **navigation du dôme** | état 3, état 4, état 2 |
| **2** | `0x82312E58` | **Customize** | `(lieu==7)` |
| **3** | `0x82311790` | l'**inscription à un tournoi** | **sous-état 0x55**, ou `(lieu==7)` |
| **4** | `0x823119F0` | la **liste des tournois officiels** | **sous-état 0x55**, ou état **1** |
| **5** | `0x823156E8` | une **annonce en attente** sur `[obj+0xE0]` | état 6, ou `(lieu==7)` |
| **6** | `0x82311C48` | une **annonce en attente** sur `[obj+0x210]` | `(lieu==7)` |

#### L'état 1 — le dôme, et sa première ligne se SAUTE

Fenêtre `QUEST_TENPO_EXPLAIN` (`0x8208E584`) ; curseur `[obj+0x50]`, borné à
2 par `FUN_822D0E18(curseur, 2, 0)`. Les trois textes d'aide :

| ligne | aide |
|--:|---|
| 0 | **150** *Participate in a tournament.* |
| 1 | **152** *View official tournaments you have cleared.* |
| 2 | **153** *Purchase items or adjust settings.* |

**Le libellé 151 est sauté**, comme 539 au §19.3 et 139 dans la table d'aide
de la maison : c'est le troisième fossile du même genre. Et la ligne de
commandes est le libellé **12** *« ..:Switch costumes  .:Back  .:Enter »*.

**La ligne 0 est inaccessible sans tournoi en cours** :

```c
if ((*curseur != 0) || (FUN_82317860(1) != 0)) { … }
else *curseur = 1;                 /* on la saute */
```

C'est la même mécanique que *Save* au menu de la maison (§19.3) : le code
force le curseur hors de la ligne morte, au lieu de poser un état sur
l'entrée. Et `FUN_82317860(1)` est le même prédicat « un tournoi officiel
tourne-t-il ? » que le dessin `FUN_82311CD8` emploie pour choisir entre le
libellé 600 et le bloc du tournoi.

La validation range la ligne dans `[obj+0xD4]` : **0 → état 3**
(l'inscription), **1 → état 4** (la liste), **2 → état 2** (Customize). Et le
bouton de retour demande le **sous-état 0x52** — la carte.

#### L'état 2 — Customize, et il rejoue la musique

Même forme que l'état 1 du menu de la maison (§19.3) : on démonte, on appelle
`FUN_8230B4C0`, on attend `FUN_8230B4B0`, on remonte, puis
`FUN_822B1540(0, "sound/bgm/vf5ps3_b03map.adx")`.

**Et c'est lui qui ARME les états 5 et 6.** À son sous-état 2 :

```c
FUN_82311fb0(obj + 0xE0,  [obj+0x5C]);
FUN_823120a8(obj + 0x210, [obj+0x5C]);
```

— les deux mêmes champs que l'init teste (`FUN_82315158(obj+0xE0)` → état 5,
`FUN_82315308(obj+0x210)` → état 6). **Les deux annonces en attente sont donc
celles des nouveautés obtenues en boutique** : les `TaskNewItemList` et
`TaskNewEmblemList` du §18.3, et c'est ce qui explique leurs deux variantes de
composition relevées au §19.1 (c70 sans liste, c75 avec).

#### Les états 3 et 4 — deux portes vers le même sous-état

Même squelette, deux objets statiques différents :

| | état 3 | état 4 |
|---|---|---|
| objet statique | `0x82AD0598` | `0x82AD0714` |
| ouverture | `FUN_823160E0` | `FUN_82318D20` |
| test | `FUN_823160C0` | `FUN_82318CF8` |
| fermeture | `FUN_823160F8` | `FUN_82318D30` |
| délai posé | `[obj+0x5BC] = 0x3C` (60 trames) | idem |
| à l'acceptation | `FUN_82318AF8(evt)` puis **`FUN_8220D1E0(0x55)`** | idem |
| au refus | `(lieu==7)` | **état 1** |

`0x55` est le sous-état du tournoi, celui de tout le §17. **Les deux entrées
du dôme y mènent**, et c'est pour cela que le §17 ne voyait qu'un point
d'entrée : il y en a deux, plus celui de la salle.

#### Les états 5 et 6 — la même attente, deux fois

Deux fonctions de dix lignes : ouvrir, attendre `FUN_822C80D0`, puis sortir.
L'état 5 regarde encore `FUN_82315308([obj+0x210])` avant de partir : s'il
reste quelque chose, il passe à l'état 6. **Les deux annonces s'enchaînent
donc** — d'abord les objets, puis les emblèmes. Toutes deux posent le libellé
**0** comme ligne de commandes.

### 20.4 LES POINTS OUVERTS DU §19.5 : TROIS TRANCHÉS, UN NON

#### Le `_NN_` du nom de fenêtre EST l'interligne — confirmé sur `_36_`

`FUN_82316A28` (`Announce`) emploie `DAT_82010304` = **36.0** pour avancer
après `p_que_info_win_36_02_ct`. Le §19.2 l'avait mesuré à **30.0** pour les
`_30_` de `Quest settings`. Deux noms, deux pas, et ils concordent.

**Une réserve honnête sur `p_que_info_win_30_04_ct`** : cette fenêtre, la
ligne *Yes* / *No*, n'a **pas de boucle**. Ses deux libellés (348 *Yes*, 349
*No*) sortent d'un seul tracé avec le format `0x82085944` = **`"%s%s\n"`** —
c'est le **`\n`** qui fait la seconde ligne, et le moteur de texte applique
alors l'interligne de la fenêtre. Le `DAT_82000F1C` = **24.0** que le code
ajoute là n'est pas un interligne : c'est le **déplacement du curseur** entre
*Yes* et *No*, posé seulement si `[obj+0x54] != 0`.

#### Les libellés 589 / 590 / 591 ne sont JAMAIS lus

Balayage de tous les immédiats `li`/`addi` valant `0x24D`, `0x24E` ou `0x24F`
dans le `.text` de 2007 — six sites :

    0x82313F50  li r11, 0x24D   dans FUN_82313EA8   (la salle)
    0x82313F58  li r11, 0x24E   dans FUN_82313EA8
    0x82313F60  li r11, 0x24F   dans FUN_82313EA8
    0x8243E780  li r7,  0x24F   dans FUN_8243E760   (hors du Quest)
    0x82440C58  li r7,  0x24D   dans FUN_82440BE8   (hors du Quest)
    0x824D70B0  li r7,  0x24D   dans FUN_824D7020   (hors du Quest)

**Seul `FUN_82313EA8` construit le trio**, et sa table `local_230` ne porte
que cinq entrées — `{589, 590, 591, 593, 594}` — dont il n'indexe que `[3]`
et `[4]`. Les trois premières sont **mortes** : les bornes de la salle ont
porté leur numéro à l'écran, puis ne l'ont plus porté. Les textes d'aide
146-148 disent toujours *Unit 1 / 2 / 3*. C'est le même fossile que le 539 du
§19.3 et le 151 du §20.3 — **trois dans le même mode**.

#### L'alignement par octet de tête se confirme sur plus de sites

Le §19.2 l'avait sur quatre tracés ; `Announce` en ajoute quatre, tous
concordants : `_01_ct`, `_36_02_ct`, `_03_ct` et `_30_04_ct` prennent le
format `"%s%s"` avec `"\x02"`. **Huit sites, zéro contre-exemple.**

#### Le code `\x14` n'est PAS identifié

Ce qui est mesuré : `FUN_82249768`, l'étage qui précède le rendu, est un
**convertisseur Shift-JIS → UTF-16** et rien d'autre — il décode par
`FUN_822496B0`, avance de 1, 2 ou 4 octets, et **ne filtre aucun octet de
contrôle**. Les `\x02`, `\x03` et `\x14` traversent donc l'étage de
conversion et arrivent au rendu comme U+0002, U+0003 et U+0014. Leur
interprétation vit plus bas que `FUN_8223F8F8`, et je ne l'ai pas trouvée.

### 20.5 CE QUI RESTE

- **déclarer** `aet_n_cmn` et `aet_n_cstm` de 2007 dans les bases 2D
  (`tools/bases_2d.py`), en se méfiant du nom : FS a déjà un `N_CMN` ;
- **poser les quatorze musiques** : étendre `tools/musique_quest.py` au lot ;
- `FUN_823158C0(evt)` rend le **niveau** d'un événement : la table n'est pas
  lue, et le §16 n'en parle pas. Le mot 12 octet 0 de la table des quinze
  événements est « un type » (§16) — c'est probablement lui ;
- `FUN_82315BE8(evt)`, qui choisit `b11ke2`, n'est pas lu ;
- le trou mesuré au §20.2 : **aucune musique pour un niveau ≥ 2 hors
  événement 14** ;
- l'interprétation des octets de contrôle de texte (`\x02`, `\x03`, `\x14`),
  en aval de `FUN_8223F8F8` ;
- et le `tnm_taikai_*` : trois **voix**, jouées par nom. Elles ne sont ni
  relevées ni posées, et le §15 n'en parlait pas.

---

## 21. AUDIT DU DOSSIER : CE QUE LA MESURE CONFIRME, ET CE QU'ELLE CONTREDIT (2026-10-19)

Reprise des affirmations chiffrées qui portent le dossier, remesurées une par
une. **Six sont confirmées, sept sont fausses ou imprécises** — dont une
écrite le jour même, au §20.2.

### 21.1 CE QUI TIENT

#### La table des quinze événements — exacte au mot près

`0x82656798`, pas `0x34`. Lue sur dix-sept entrées pour voir où elle s'arrête :
**l'entrée 15 porte des pointeurs** (`0x8208E914`, `0x8208EA48`) et la 16 du
bruit. **Il y a bien quinze événements, et pas un de plus.**

Et le mot 0 des événements 0 à 6 vaut **528, 529, 530, 531, 532, 533, 534** —
les sept lieux du §9.21, dans l'ordre. Confirmé.

#### `npc_tbl.bin` — et la preuve est dans le fichier lui-même

Le §4 annonce « 1000 enregistrements de 0x90 octets, puis le réservoir de
chaînes ». Mesure sur les 198 768 octets du fichier de 2007 :

    1000 x 0x90                      = 144 000 octets
    reservoir de chaines             =  54 768 octets
    offset du PREMIER NOM (mot 0)    = 0x23280 = 144 000  <-- il tombe JUSTE
    offsets de nom valides           = 1000 / 1000

**L'offset du premier nom est exactement la fin de la table.** Aucun autre pas
ne peut produire cela. Et les trois champs cités tiennent :

| champ | annoncé | mesuré |
|---|---|---|
| `+0x14` le personnage | 0..16, dix-sept valeurs | **17 valeurs, 0..16** |
| `+0x7C` le grade | 42 valeurs (0..41) | **42 valeurs, 0..41** |
| `+0x88` le lieu | le lieu du rival | **8 valeurs, 0..7** |

**Et le lieu 7 est sous-peuplé** : 59 rivaux, contre 130 à 138 pour chacun des
sept autres. Le lieu 7 est `EVENT SQUARE` (§19.4) — la **donnée confirme donc
le huitième lieu**, indépendamment du code, et avertit que le tirage sans
remise du §17 y puise dans 59 noms, pas 135.

#### Et trois lectures du jour qui tiennent

- l'alignement par octet de tête (`\x02` centré, `\x03` à droite) : **huit
  sites, zéro contre-exemple** (§20.4) ;
- le `_NN_` du nom de fenêtre est l'interligne : **36.0 pour `_36_`,
  30.0 pour `_30_`** (§20.4) ;
- les libellés 589/590/591 ne sont jamais lus : **balayage exhaustif des
  immédiats** (§20.4).

### 21.2 CE QUI EST FAUX — ET LE PREMIER EST DE CE MATIN

#### `FUN_823158C0` n'est pas un lecteur de table : c'est un test d'intervalle

Le §20.2 annonçait un « trou mesuré : aucune musique si
`FUN_823158C0(evt) >= 2` ». **La fonction entière :**

```c
undefined8 FUN_823158c0(int evt)
{
  if (evt < 0)      { if (evt < 7) return -1; }
  else if (evt < 7) return 0;
  if (0xe < evt)    return -1;
  return 1;
}
```

**Elle ne lit aucune donnée.** Elle rend **0** pour les événements 0 à 6,
**1** pour 7 à 14, **-1** hors bornes. Pour un événement valide, la branche
muette du §20.2 est **inatteignable** : le trou n'existe pas. Je l'avais
déduit de la forme du `if` sans lire la fonction appelée — exactement la faute
que les règles de travail interdisent.

**Et cela donne enfin le sens du « niveau »** : c'est la moitié de la table
où l'événement vit. Les sept premiers (les lieux) sont le niveau 0 ; les huit
suivants, le niveau 1 ; et l'événement 14 est traité à part, avant l'appel.
La correspondance avec les trois voix `tnm_taikai_tenpo` / `_normal` /
`_final` du §20.2 tient donc, mais pour une raison beaucoup plus simple que
je ne l'avais écrit.

#### `FUN_82317860` IGNORE SON ARGUMENT

Les §19.4 et §20.3 écrivent `FUN_82317860(1)` et `FUN_82317860(0)` comme si
l'argument choisissait quelque chose. **Il n'est jamais lu.** Désassemblé :

    0x82317860  mflr  r12
    0x82317864  stw   r12, -8(r1)
    0x82317868  stwu  r1, -0x60(r1)
    0x8231786C  bl    0x82316270          <- r3 n est pas touche
    0x82317870  lis   r11, 0x8265
    0x82317874  addi  r11, r11, 0x6B08
    0x82317878  lwz   r11, 0x2C(r11)      <- 0x82656B34
    0x8231787C  and   r11, r3, r11
    0x82317880  cntlzw r11, r11
    0x82317884  rlwinm r11, r11, 0x1B, 0x1F, 0x1F
    0x82317888  xori  r3, r11, 1

`return (FUN_82316270() & [0x82656B34]) != 0;` — **un prédicat global**, pas
un prédicat par niveau. Les deux appels sont le même appel.

#### `FUN_82315BE8` prend le BLOC, pas l'événement

Le §20.2 écrit `FUN_82315BE8(evt)`. La fonction remonte un tableau :

```c
p = bloc + 0x488;
for (i = 0x3F; i >= 0; i--, p -= 0x10)
    if (p[0] & 0x40) return p[2];
return -1;
```

Soixante-quatre enregistrements de 0x10 octets finissant en `bloc + 0x488`,
donc **commençant en `bloc + 0x98`**. Ce tableau n'est décrit nulle part dans
le dossier : c'est la liste des participants du tournoi, et le bit `0x40`
marque celui qu'on cherche. §20.2 corrigé.

#### Le « masque de lieu » du §16 ne vaut que pour la moitié de la table

Le §16 lit le mot 11 comme « le masque de lieu ». Mesuré :

| événements | mot 11 |
|---|---|
| 0 à 6 | `0x01`, `0x02`, `0x04`, `0x08`, `0x10`, `0x20`, `0x40` — **un bit, un lieu** |
| **7 à 14** | **`0xFF` pour les huit** — *tous* les lieux |

La lecture tient pour les sept premiers ; pour les huit autres, « masque de
lieu » veut dire « n'importe où ». Et **aucun événement ne porte le bit
`0x80`**, celui du huitième lieu (`EVENT SQUARE`) — cohérent avec le fait que
le dôme a son propre écran (§19.4).

#### Le « mot 12 octet 0 = un type » du §16 ne se vérifie pas

Mesuré sur les quinze :

| événements | mot 12 | octet 0 | octet 1 |
|---|---|--:|--:|
| 0 à 6 | `0x13000000` | **19** | 0 |
| 7 | `0x000F0000` | 0 | 15 |
| 8 | `0x011E0000` | 1 | 30 |
| 9 | `0x04320000` | 4 | 50 |
| 10 | `0x08460000` | 8 | 70 |
| 11 | `0x0A500000` | 10 | 80 |
| 12 | `0x0C5A0000` | 12 | 90 |
| 13 | `0x0E640000` | 14 | 100 |
| 14 | `0x100A0000` | 16 | 10 |

Un « type » prendrait quelques valeurs ; ici l'octet 0 vaut **19** pour les
sept lieux puis une suite croissante **0, 1, 4, 8, 10, 12, 14, 16**, et
l'octet 1, nul pour les sept lieux, suit **15, 30, 50, 70, 80, 90, 100** puis
retombe à **10**. Deux séries, pas un type. **Leur sens n'est pas lu** : il
faut trouver qui lit `0x82656798 + n*0x34 + 48`.

#### LES HUIT TOURNOIS OFFICIELS N'ONT PAS DE NOM DANS NOTRE IMPORT

Le mot 0 des événements **7 à 14** vaut **641, 642, 643, 644, 645, 646, 647,
648** — et `tools/quest_textes_map.h` **ne porte aucun des huit**. Le §16.2
n'en parle pas : il ne nomme que les sept lieux.

Ce sont donc **huit libellés manquants**, et ce sont les noms des huit
tournois officiels — ceux que `Announce` affiche
(`FUN_82322798(*(u32 *)(&DAT_82656798 + n * 0x34))`, §17.15) et que la liste
du dôme énumère. **Sans eux, les huit entrées de la liste officielle
s'afficheront vides.** C'est un manque pour le portage, à ajouter au relevé de
`tools/textes_quest.py`.

#### Les masques `0x82656B..` sont NULS dans l'image

`0x82656B08`, `0x82656B14`, `0x82656B34`, `0x82656B38` et les trente-deux
octets de `0x82656B40` valent **tous zéro** dans l'image. Ce sont des
variables d'exécution, pas des constantes. Toute lecture statique de ces
adresses rendrait « 0 » sans que cela veuille rien dire — **le neuvième zéro
qui n'est pas une mesure.**

### 21.3 UN DÉFAUT D'OUTILLAGE, ET IL ÉCRASE DEUX FICHIERS DU JEU

`tools/bases_2d.py --ajouter qdan` pose la planche des pictos de grade **sous
le nom de son fichier source**, `aet_s_gamdan.bin`. Or :

| | valeur mesurée |
|---|---|
| la base AET d'ORIGINE de FS | porte `AET_S_GAMDAN` = **planche 242**, fichier `aet_s_gamdan.bin`, rang 381, sprites 299 |
| le `.par` de FS | nomme encore **`aet_s_gamdan.bin`** (279 936 o, comprimé) **et `spr_s_gamdan.farc`** (178 810 o) |
| notre `rom/2d/aet_s_gamdan.bin` | **743 472 octets** — la taille exacte de celui de 2007 |

**Les deux ne peuvent pas être servis.** Le `.par` passe avant le disque — c'est
la raison même de `par_masquer` — et il n'est masqué **que** pour `aet_db.bin`
et `spr_db.bin`. Donc, de deux choses l'une :

- soit le `.par` gagne, et **nos pictos de grade ne viennent pas d'où le
  dossier le dit** ;
- soit le disque gagne, et **la planche 242 de Final Showdown est écrasée**
  depuis le 2026-09-30 — l'écran de montée en grade de FS dessinerait alors
  les calques de 2007.

**TRANCHÉ une heure plus tard, et c'est la PREMIÈRE branche : le `.par`
gagne. Voir le §22 — et la conséquence n'est pas celle qu'on craignait.** La note de `qdan` dans `bases_2d.py` disait seulement que le *jeu
de sprites* `SPR_S_GAMDAN` (299) de FS avait un contenu différent ; elle ne
disait pas que **la planche AET existe aussi**, et c'est là tout l'écart.

`ajouter()` reçoit donc deux clés neuves, `aet_pose` et `spr_pose` — le nom
sous lequel on écrit, distinct de la source — et un **refus** : un nom posé
qui est déjà le fichier d'une planche de la base d'origine arrête tout, à
moins que l'entrée ne porte `ecrase_fs=True`. `qdan` la porte, pour ne rien
changer sans l'avoir vu ; les deux entrées neuves du §21.5 ne la portent pas.

### 21.4 CE QUE L'AUDIT A APPRIS EN PASSANT : `FUN_82315A90`

Elle sert au §20.2 à choisir entre `tn1` et `tn2`, et le dossier ne la lisait
pas :

```c
desc = bloc + 0x498 + bloc[0x4C8] * 8;        /* le descripteur du tour */
if (desc[6] == 4)                   return 6; /* la Finale */
if (bloc[0x4C9] + 1 < desc[5])      return desc[6];   /* pas le dernier match */
if (desc[6] == 3)                   return 5;
if (desc[6] == 5)                   return 4;
return bloc[0x4A6 + bloc[0x4C8] * 8];         /* le type du tour SUIVANT */
```

C'est la **machine à sauts du §17.9, avec une anticipation** : quand on est au
dernier match d'un tour, elle rend déjà le type du tour qui vient (3 → 5,
5 → 4, sinon le `+6` du descripteur suivant, soit `0x49E + (i+1)*8`).

Et cela explique le branchement de `FUN_8231F1D8` cas 0 : `tn1` si le retour
est **< 3** (Round 1-3), rien si c'est **6** (la Finale, qui a ses `ke`), et
`tn2` dans tous les autres cas — c'est-à-dire **à partir des demi-finales**.
Le §20.2 l'avait dit par l'autre entrée (`desc[6] == 3` au cas 2) ; les deux
chemins concordent.

### 21.5 CE QUI A ÉTÉ POSÉ DANS LE JEU AUJOURD'HUI

#### Les quinze musiques

`tools/musique_quest.py` passe d'un fichier à **quinze**, chacun avec son
demandeur en commentaire. Posées depuis
`VF5 FS DECOMP/X360_VF5/media/sound/bgm` vers
`runtime/media/vf5fs/vf5fs_media/rom/sound/bgm`, à côté puis `os.replace`,
avec contrôle SHA-256 :

    deja la   vf5ps3_b03map      5 836 800 o
    posee     vf5ps3_j26           305 878 o    j25  420 322 o    j24  700 474 o
    posee     vf5ps3_b04tn1      4 079 616 o    b05tn2  5 982 208 o
    posee     vf5ps3_b06tn1      3 592 192 o    b07tn2  2 992 128 o
    posee     vf5ps3_b08tn1      4 491 264 o    b09tn2  2 441 216 o
    posee     vf5ps3_b10ke1      1 503 232 o    b11ke2  1 370 112 o
    posee     vf5ps3_b12ke3      1 441 792 o
    posee     vf5ps3_b16tse      4 540 416 o    b17tco  3 397 632 o

#### Les deux planches

`--ajouter que qwin tnt tnto qdan qcmn qcstm`, dans cet ordre, pour que les
identifiants que `tools/quest_runtime.c` porte en dur ne bougent pas. Ils
n'ont pas bougé :

| | avant | après |
|---|---|---|
| `AET_N_QUE` / scène `MAIN` | 526 / 683 | **526 / 683** |
| `AET_N_QWIN` / scène | 527 / 685 | **527 / 685** |
| `AET_N_TNT`, `AET_N_TNTO` | 528, 529 | **528, 529** |
| `AET_S_GAMDAN` / scène | 530 / 688 | **530 / 688** |

et les deux neuves :

| planche | id | fichier posé | sprites | scènes |
|---|--:|---|--:|---|
| `AET_N_CMN` (les quatre fenêtres d'`Announce`) | **531** | `aet_q_cmn.bin` | **628** | **690** MAIN, **691** MAIN_VGA |
| `AET_N_CSTM` (la boutique et l'éditeur) | **532** | `aet_q_cstm.bin` | **629** | **692** MAIN |

192 et 73 identifiants de sprite renumérotés, aucun orphelin. `--controle`
rend **CONFORMES**. Et les planches de FS sont intactes :
`aet_n_cmn.bin` fait toujours 578 160 octets (3 septembre),
`spr_n_cmn.farc` 529 139 (3 septembre).

`tools/ancres_ecrans.py` relit les fenêtres **dans les fichiers posés** :
`p_que_info_win` dans `aet_q_cmn.bin`, `p_item_grid` / `p_iteminfo_win` /
`p_itemshop_arrow` dans `aet_q_cstm.bin`.

**Rien n'est vérifié à l'écran.** Il reste à câbler : `quest_runtime.c` ne
connaît ni 531/628/690 ni 532/629/692.

### 21.6 CE QUE L'AUDIT LAISSE OUVERT

1. **`qdan` écrase-t-il la planche 242 de FS ?** (§21.3) — à voir à l'écran ou
   à la sonde. C'est le point le plus urgent : il touche FS, pas le Quest.
2. **Les huit libellés 641-648** manquent à l'import de textes.
3. **Le mot 12 de la table des événements** : deux séries d'octets dont le
   sens n'est pas lu.
4. Le tableau de **soixante-quatre enregistrements de 0x10** en `bloc + 0x98`
   (§21.2), jamais décrit.
5. Les octets de contrôle de texte `\x02`, `\x03`, `\x14` : leur lecteur est
   en aval de `FUN_8223F8F8`, non trouvé (§20.4).
6. Les trois voix `tnm_taikai_*` : ni relevées ni posées.

---

## 22. LE VERDICT : LE `.par` GAGNE, ET LE PICTO DE GRADE NE POUVAIT PAS S'AFFICHER (2026-10-19)

Le §21.3 laissait deux branches : soit le `.par` sert `aet_s_gamdan.bin` et nos
pictos ne viennent pas d'où le dossier le dit, soit le disque le sert et la
planche 242 de Final Showdown est écrasée. **C'est la première**, et la sonde
n'a pas eu besoin de lancer le jeu : la réponse est entièrement dans les
fichiers.

### 22.1 LA CHAÎNE DE MESURE, EN QUATRE MAILLONS

#### 1. Le `.par` est consulté AVANT le disque

Ce n'est pas une déduction : `tools/par_masquer.py` le porte en en-tête,
**mesuré au point d'arrêt sur `CreateFileW`** (`analysis/import_decors.md`).
Ce qui est dans l'archive est lu depuis l'archive, et le disque n'est jamais
interrogé.

#### 2. Et tout ce qu'une séance passée a voulu remplacer sur le disque est MASQUÉ

C'est la corroboration, et elle est accablante. L'index du `.par`, relu
aujourd'hui :

    aet_n_adv.bi_          8 448 o   (comprime)   <- masque
    spr_n_adv.far_       185 628 o                <- masque
    spr_n_cmnps3.far_     45 258 o                <- masque
    aet_db.bi_            45 520 o   (comprime)   <- masque
    spr_db.bi_         1 524 752 o   (comprime)   <- masque

Cinq noms dont le dernier caractère est devenu `_`. **Chaque fois qu'on a
voulu qu'un fichier du disque soit lu, il a fallu masquer son nom dans le
`.par`.** Et les trois premiers ont leur `.origine` posé à côté dans `rom/2d`,
preuve qu'ils ont bien été remplacés et que cela a marché.

#### 3. `aet_s_gamdan.bin` et `spr_s_gamdan.farc` NE SONT PAS masqués

    aet_s_gamdan.bin     279 936 o   (comprime)   <- intact
    spr_s_gamdan.farc    178 810 o                <- intact

Donc **le moteur sert les copies de Final Showdown**, et notre
`rom/2d/aet_s_gamdan.bin` (743 472 o, celui de 2007) **n'a jamais été lu.**

**Première conséquence, et c'est la bonne nouvelle : la planche 242 de Final
Showdown n'a jamais été écrasée.** La crainte du §21.3 était infondée — non
pas parce que le fichier n'a pas été écrit, mais parce que le fichier écrit
n'est pas celui que le moteur ouvre.

#### 4. Les deux planches ne partagent AUCUN nom de calque

La planche de FS, **extraite du `.par`** (`tools/sllz.py`, `Par.sortir`) :

| | calques | `s_gamdan_dan01`… | `shogo` |
|---|--:|--:|--:|
| **FS** (279 936 o, du `.par`) | 218 noms | **0** | **0** |
| **2007** (743 472 o, importée) | 236 noms | les 19 | les 22 |
| **en commun** | **0** | | |

FS nomme ses calques de grade `end_kyu01`, `end_kyu01_txt`, `end_dan01`… —
dix-huit `kyu` et vingt `dan`, préfixe `end_`, et **pas un seul `shogo`**.
Celle de 2007 les nomme `s_gamdan_kyu01`, `s_gamdan_dan01`, et porte les
vingt-deux titres.

### 22.2 CE QUE CELA VEUT DIRE : LE PICTO DE GRADE NE S'AFFICHAIT PAS

`tools/quest_runtime.c` demande le picto **par son nom**, dans la scène
`QUEST_SCENE_QDAN` = 688 :

```c
static const char *const kyu[10] = {
    0, "s_gamdan_kyu09", "s_gamdan_kyu08", … "s_gamdan_kyu01" };
static const char *const dan[10] = {
    "s_gamdan_dan01", … "s_gamdan_dan10" };
…
t[n].rang = QUEST_RANG_GRADE; t[n].scene = QUEST_SCENE_QDAN; t[n].nom = gr;
```

**Ces dix-neuf noms n'existent pas dans la planche que le moteur sert.** Le
picto de grade de la fiche du joueur, sur la carte du Quest, ne pouvait donc
pas être trouvé — et n'était pas dessiné.

**Et le dossier ne dit pas le contraire**, en y regardant de près. La note de
`quest_runtime.c` écrit « Les vrais pictos sont dans la planche de 2007 […] on
les monte donc comme tous nos autres calques » — c'est une **intention**. La
seule vérification citée (`quest_runtime.c`, ligne 893) porte sur la **valeur**
du grade — « *Raeme 4th kyu* est le grade 6, *Qazi 10th kyu* le grade 0,
vérifié sur une capture du jeu de 2007 » — c'est-à-dire sur `npc_tbl + 0x7C`,
pas sur le dessin. **Personne n'a jamais écrit avoir VU le picto.** Je l'avais
lu comme une confirmation ; ce n'en était pas une.

### 22.3 LA CORRECTION, ET ELLE N'ÉCRASE RIEN

Le mécanisme posé au §21.3 pour `qcmn` et `qcstm` sert ici aussi : `qdan`
reçoit un nom de fichier posé **à lui**.

    'qdan': …  aet_pose='aet_q_dan.bin', spr_pose='spr_q_dan.farc'

Ces deux noms sont absents du `.par`, donc **servis depuis le disque**, tandis
que `aet_s_gamdan.bin` et `spr_s_gamdan.farc` continuent d'être servis depuis
le `.par` à Final Showdown. **Les deux planches coexistent, et aucune n'est
écrasée.**

Reposé par `--ajouter que qwin tnt tnto qdan qcmn qcstm` :

| planche | id | fichier posé | sprites | scènes |
|---|--:|---|--:|---|
| `AET_N_QUE` | 526 | `aet_n_que.bin` | 623 | 683, 684 |
| `AET_N_QWIN` | 527 | `aet_n_qwin.bin` | 624 | 685 |
| `AET_N_TNT` | 528 | `aet_n_tnt.bin` | 625 | 686 |
| `AET_N_TNTO` | 529 | `aet_n_tnto.bin` | 626 | 687 |
| `AET_S_GAMDAN` | 530 | **`aet_q_dan.bin`** | 627 | 688, 689 |
| `AET_N_CMN` | 531 | `aet_q_cmn.bin` | 628 | 690, 691 |
| `AET_N_CSTM` | 532 | `aet_q_cstm.bin` | 629 | 692 |

**Les identifiants n'ont pas bougé** — ceux que `quest_runtime.c` porte en
dur (526, 527, 530, 683, 685, 688) sont intacts. `--controle` rend
**CONFORMES**.

Et le contrôle qui compte : `aet_q_dan.bin`, relu dans `rom/2d`, porte
**236 noms de calque, les dix-neuf que `quest_grade_calque()` demande, et les
vingt-deux titres `shogo`** — zéro absent.

### 22.4 CE QUI RESTE À VOIR (les deux fichiers morts sont retirés)

**Prédiction, pas mesure** : le picto de grade devrait maintenant apparaître
sur la fiche du joueur, en bas à gauche de la carte du Quest. Avant cette
correction il ne pouvait pas. C'est à l'écran que cela se juge, et c'est
Frédéric qui tranche.

#### Les deux fichiers morts sont retirés

Nos copies de 2007 sous les noms de FS -- `aet_s_gamdan.bin` (743 472 o) et
`spr_s_gamdan.farc` (1 042 268 o) -- ont été **retirées de `rom/2d`** le
2026-10-19, après trois contrôles :

1. elles sont **octet pour octet identiques** à `aet_q_dan.bin` et
   `spr_q_dan.farc`, qui restent (même SHA-256) -- donc rien n'est perdu, et
   `--ajouter qdan` les refabrique de toute façon ;
2. les seules entrées de base qui nomment encore ces deux fichiers sont
   **celles de Final Showdown** (`AET_S_GAMDAN` 242 rang 381, `SPR_S_GAMDAN`
   299 rang 450), servies depuis le `.par` où elles sont intactes
   (279 936 o et 178 810 o, non masquées) ;
3. aucun outil ne les cite comme **chemin** : la ligne 90 de `bases_2d.py` est
   le nom de la **source**, lue dans le média de 2007, et les deux autres
   mentions (`txp.py`, `quest_runtime.c`) sont des commentaires qui parlent du
   *jeu de sprites*, pas d'un fichier.

Après retrait : `--controle` rend **CONFORMES**, `aet_q_dan.bin` porte
toujours ses 236 noms dont les dix-neuf demandés et les vingt-deux `shogo`, et
les planches de FS dans `rom/2d` sont intactes (`aet_n_cmn.bin` 578 160 o,
`spr_n_cmn.farc` 529 139 o, tous deux du 3 septembre).

### 22.5 LA LEÇON D'OUTILLAGE, LA DIXIÈME

**« Le fichier est posé » n'est pas « le fichier est lu. »** Entre les deux il
y a un résolveur, et ici il a trois étages : l'archive FArC embarquée du
binaire, le `.par`, puis le disque. Le dossier connaissait cette chaîne — c'est
`par_masquer.py` qui la documente — et l'a quand même oubliée pour une
planche, pendant trois semaines, **sans qu'aucune erreur ne soit levée** : le
patcheur disait « appliqué », l'outil disait « posée », le contrôle disait
« CONFORMES », et le calque n'était pas dessiné.

Le garde-fou posé aujourd'hui dans `ajouter()` ferme cette porte : un nom posé
qui est déjà le fichier d'une planche de la base d'origine **arrête l'outil**.

---

## 23. LE MODE QUEST NE SE LANCE PLUS — CE QUI EST MESURÉ, ET L'ÉTAT RENDU (2026-10-19)

Constat de Frédéric après la pose du §21.5 et la correction du §22.3 : **le
mode Quest ne se lance pas.** Ce paragraphe dit ce que la mesure établit, ce
qu'elle n'établit pas, et dans quel état le dépôt est rendu.

### 23.1 CE QUE LE JOURNAL D'EXÉCUTION DIT

`runtime/media/vf5fs/quest_journal.txt`, fin du dernier lancement :

    [quest] boite QUESTBOX 140715758333760
    [quest] contexte 2D ... , calque 0, table des polices ... ; 0
    [quest] police mode 0 : descripteur ... , sprite 0000018F, jeu 0
    [quest] police mode 1 : descripteur ... , sprite 0000D30D, jeu 0
    [quest] police mode 2 : descripteur ... , sprite 0000D3DB, jeu 0
    [quest] profil Quest repris d'une version anterieure ; combats 13
    [quest] ecran Quest : planche et sprites demandes 526
    <fin du fichier>

**Le Quest démarre.** La boîte `QUESTBOX` est trouvée, le contexte 2D et les
trois polices sont pris, le profil est chargé. Puis l'étape 1 demande ses six
chargements — `charger_spr(623, 624, 627)` et `charger(526, 527, 530)` — et
**le journal s'arrête.**

Or l'étape 2 attend `etat(526)|etat_spr(623)|etat(527)|etat_spr(624)|
etat(530)|etat_spr(627)` et, au bout de **quinze secondes**, écrit
« planche TOUJOURS PAS prete, etat » puis quitte. **Cette ligne n'est pas
là.** Donc l'étape 2 n'a pas tourné quinze secondes : soit le jeu a été fermé
avant, soit il s'est arrêté pendant le chargement.

### 23.2 CE QUI AVAIT CHANGÉ

Trois choses, et une seule touche ce que l'étape 1 charge :

| changement | touche-t-il les six chargements ? |
|---|---|
| les **quatorze musiques** posées dans `rom/sound/bgm` | **non** — aucune n'est nommée par une base ni par FS ; seule `b03map` est demandée, et par l'étape 2, après |
| **`qcmn` et `qcstm`** ajoutés aux bases (planches 531, 532 ; sprites 628, 629) | **non directement** : la greffe ne les demande pas. Mais ils changent les deux bases |
| **`qdan` renommé** : la planche 530 passe de `aet_s_gamdan.bin` à `aet_q_dan.bin`, et le jeu de sprites 627 de `spr_s_gamdan.bin` à `spr_q_dan.bin` | **OUI, en plein** — 530 et 627 sont deux des six |

**Et c'est le troisième qui est le plus suspect**, pour la raison même du §22 :
avant le renommage, le jeu de sprites 627 résolvait `spr_s_gamdan.bin`, donc
le `.par` servait **celui de Final Showdown** (178 810 o). Après, 627 résout
`spr_q_dan.bin`, servi depuis le disque : **celui de 2007, 1 042 268 o, que
Final Showdown n'avait jamais chargé.** Le §22 a rendu vivant un chargement
qui, pendant trois semaines, ne s'était jamais produit.

**Ce n'est pas démontré.** Contre cette hypothèse : les jeux de sprites de
`que`, `qwin`, `tnt` et `tnto` viennent eux aussi du média de 2007, sont servis
depuis le disque, et se chargent. Le format n'est donc pas disqualifiant en
soi.

### 23.3 DEUX CONTRÔLES QUI ÉCARTENT MON CODE

**Le changement de `bases_2d.py` n'a pas abîmé les entrées existantes.**
Refaire `--ajouter que qwin tnt tnto qdan` et comparer, entrée par entrée, à
la base de ce matin : **505 planches contre 505, 638 scènes contre 638, et une
seule entrée différente** —

    refaite  : [530, 'AET_S_GAMDAN', 'aet_q_dan.bin',    504, 627]
    ce matin : [530, 'AET_S_GAMDAN', 'aet_s_gamdan.bin', 504, 627]

— exactement celle qu'on voulait changer, et **zéro** entrée de scène
différente. Les 14 octets d'écart de taille sont du remplissage de la table de
noms, pas de la corruption.

**Aucune borne n'est franchie.** Les identifiants, avant et après :

| | planches AET | scènes | planches SPR | sprites | id de sprite max |
|---|--:|--:|--:|--:|--:|
| origine de FS | 500 | 631 | 593 | 39 903 | 0xD78F |
| ce matin | 505 | 638 | 598 | 40 744 | 0xDAD8 |
| après la pose | 507 | 641 | 600 | 40 943 | **0xDB9F** |

56 223 reste loin de 65 535 : rien n'a débordé un champ de 16 bits.

### 23.4 UN DÉFAUT DE FOND, TROUVÉ EN CHEMIN

`ecrire_base()` **ne reproduit pas la base d'origine de FS à l'octet** :

    aet_db.bin   origine 45 520 o  ->  reecrite 45 473 o   premier ecart a 0x0C
    spr_db.bin   origine 1 524 752 o -> reecrite 1 519 753 o  premier ecart a 0x0C

Le contenu logique est le même (`--controle` rend CONFORMES et compare entrée
par entrée), mais **la disposition diffère** : notre écrivain range la table de
noms autrement que celui de SEGA. Cela vaut depuis le 2026-09-11, et le Quest
a fonctionné dans cet état — donc le moteur tolère la nouvelle disposition.
**Mais ce n'est plus un détail dès qu'on cherche une régression dans les
bases** : on ne peut pas comparer octet pour octet avec l'original pour
dédouaner l'outil. À garder en tête.

### 23.5 L'ÉTAT RENDU

**Le dépôt est revenu à l'état de ce matin pour tout ce qui touche la 2D**, à
l'octet :

| fichier | état |
|---|---|
| `rom/2d/aet_db.bin` | **rendu** tel qu'il était (45 838 o) — 505 planches, ids 526-530 |
| `rom/2d/spr_db.bin` | **rendu** (1 548 209 o) |
| `rom/2d/aet_s_gamdan.bin` | **remis** (743 472 o) |
| `rom/2d/spr_s_gamdan.farc` | **remis** (1 042 268 o) |
| `aet_q_dan.bin`, `spr_q_dan.farc` | **retirés** |
| `aet_q_cmn.bin`, `spr_q_cmn.farc` | **retirés** |
| `aet_q_cstm.bin`, `spr_q_cstm.farc` | **retirés** |

`--controle` rend **CONFORMES**. Les binaires sont ceux que `quest.cmd` a
produits (19:35) : `QUESTBOX` présent, et la ligne 3 saute bien vers la greffe
(`0x1801DE0C0 jmp 0x180EA2FA0`).

**Les quatorze musiques sont GARDÉES** dans `rom/sound/bgm` : elles n'entrent
dans aucune base, aucun nom de FS ne les désigne, et l'étape 1 ne les charge
pas. Si Frédéric veut un retour à l'identique, `py -3
tools/musique_quest.py --retirer` les reprend toutes.

Les outils gardent leurs changements — ils sont inertes tant qu'on ne les
lance pas : `bases_2d.py` (les clés `aet_pose`/`spr_pose`, le refus, `qcmn`,
`qcstm`, le renommage de `qdan`), `musique_quest.py`, `ancres_ecrans.py`,
`ancres_que.py`.

### 23.6 CE QU'IL FAUT MESURER ENSUITE, DANS CET ORDRE

1. **Relancer `tools/quest.cmd` sur l'état rendu.** S'il marche, la cause est
   dans ce qui a été ajouté, et la bissection vaut. S'il ne marche pas, elle
   est ailleurs — et il faudra regarder du côté du build de 19:35 et des
   musiques.
2. Puis **une seule chose à la fois** : d'abord `qcmn` et `qcstm` **sans**
   toucher à `qdan` ; si cela tient, le renommage de `qdan` ensuite. Le §22
   reste vrai sur le fond — le picto de grade ne pouvait pas s'afficher — mais
   **sa correction est à revalider**.
3. Et quand le chargement échoue, **il faut le voir** : l'étape 2 n'écrit son
   échec qu'au bout de quinze secondes et seulement si elle tourne. Une ligne
   de journal par chargement demandé, avec l'état rendu par
   `etat()`/`etat_spr()` à chaque trame, dirait **lequel** des six ne vient
   pas. C'est l'instrument qui manque.

---

## 24. LA BISSECTION : C'EST LE RENOMMAGE DE `qdan`, ET LE SUSPECT EST UNE TEXTURE (2026-10-19)

> **CE PARAGRAPHE DÉSIGNE LE MAUVAIS COUPABLE.** Le §24.3 accuse une texture
> en RGBA4 ; la cause réelle est le **nom du membre** dans l'archive de
> sprites, et le §25 la mesure. Le §24.4 disait « ce n'est pas prouvé » —
> c'était la bonne réserve, et elle a eu raison. Les mesures de formats du
> §24.3 restent justes ; c'est leur *interprétation* qui était fausse.

### 24.1 LES DEUX OBSERVATIONS DE FRÉDÉRIC

| état | le mode Quest |
|---|---|
| l'état de ce matin rendu (bases à l'octet, `qdan` sous son nom d'origine, pas de `qcmn`/`qcstm`) | **se lance** |
| `qcmn` et `qcstm` posés (planches 531, 532), `qdan` inchangé | **se lance** |
| `qdan` renommé en `aet_q_dan.bin` / `spr_q_dan.farc` (avec ou sans `qcmn`/`qcstm`) | **ne se lance pas** |

**Les deux planches neuves sont innocentes.** Le §23.2 avait désigné le bon
suspect : le renommage de `qdan`, parce qu'il touche deux des six chargements
de l'étape 1 — la planche 530 et le jeu de sprites 627.

### 24.2 CE QUE LE RENOMMAGE CHANGE, EN UNE PHRASE

Sous son nom d'origine, le jeu de sprites 627 résout `spr_s_gamdan.bin` : ce
nom **n'est pas masqué** dans le `.par`, donc le moteur sert **celui de Final
Showdown** (178 810 o). Sous le nom neuf, il résout `spr_q_dan.bin`, absent du
`.par`, donc servi depuis le disque : **celui de 2007**, 1 042 268 o comprimés,
**6 397 104 octets décompressés**, que Final Showdown n'avait **jamais**
chargé.

L'inventaire des noms masqués, relu aujourd'hui, le confirme et corrige au
passage le dossier : **vingt-cinq** noms sont masqués, pas vingt — les deux
bases, `auth_3d_db`, `string_array`, `stgnyc`, et les **neuf `aet_n_*` plus
onze `spr_n_*`**. C'est exactement la famille `n_` (les planches du menu
console). **Aucun `s_`, donc ni `aet_s_gamdan.bin` ni `spr_s_gamdan.farc`.**

### 24.3 LE SUSPECT : UNE TEXTURE DANS UN FORMAT UNIQUE AU JEU

Inventaire des formats de texture de **tous** les `spr_*.farc` de `rom/2d` :

| format | ce qu'il est | textures | fichiers |
|--:|---|--:|--:|
| 1 | RGB8 | 14 | 9 |
| 2 | RGBA8 | 71 | 15 |
| 3 | RGB5 (565) | 3 | 2 |
| **5** | **RGBA4 (4444)** | **1** | **1** |
| 6 | DXT1 | 22 | 11 |
| 9 | DXT5 | 68 | 15 |

**Le format 5 n'existe qu'une fois dans tout `rom/2d`**, et c'est dans
`spr_s_gamdan.farc` — notre copie de 2007 :

    tex00  2048x1024  format 5  (RGBA4)   4 194 304 o   <-- unique
    tex01  1024x512   format 6  (DXT1)      262 144 o
    tex02  2048x512   format 9  (DXT5)    1 048 576 o
    tex03  1024x512   format 9              524 288 o
    tex04   128x512   format 9               65 536 o
    tex05   128x256   format 9               32 768 o
    tex06   512x128   format 2  (RGBA8)     262 144 o

Tous les jeux de sprites que Final Showdown charge effectivement — `que`,
`qwin`, `tnt`, `tnto`, et les siens — n'emploient que **1, 2, 3, 6 et 9**. Le
format 3 (RGB5, seize bits lui aussi) est chargé sans problème, dans
`spr_n_qwin.farc` : **ce n'est donc pas « seize bits » qui coince, c'est
RGBA4 en particulier.**

### 24.4 CE QUI N'EST PAS PROUVÉ, ET IL FAUT LE DIRE

**Je n'ai pas montré que le moteur refuse le format 5.** Ce qui est établi est
une **coïncidence structurelle forte** : le seul chargement qui a changé est
celui d'un jeu de sprites qui contient la seule texture d'un format que rien
d'autre n'emploie dans cette build.

Et une tentative de mesure a échoué proprement : compter les mots de 32 bits
valant les constantes DXGI (28 = R8G8B8A8, 71 = BC1, 77 = BC3, 85 = B5G6R5,
115 = B4G4R4A4) dans `vfes.exe` rend 68, 13, 119, 29 et 58 occurrences. **Cela
ne prouve rien** : de petits entiers apparaissent partout dans un binaire de
2 Mo. Ce n'est pas une mesure, c'est du bruit, et il ne faut pas s'en servir.

**Il reste aussi à savoir LEQUEL des deux fichiers échoue.** `aet_pose` et
`spr_pose` sont des clés indépendantes : on peut renommer la planche AET
seule, ou le jeu de sprites seul. Deux lancements trancheraient, et le
deuxième dirait si la texture est bien en cause.

### 24.5 L'ÉTAT, ET LA SUITE

**Posé et qui marche** : les quinze musiques, et les planches `qcmn` (531,
sprites 628, scènes 690/691, fichier `aet_q_cmn.bin`) et `qcstm` (532, sprites
629, scène 692, `aet_q_cstm.bin`) — les quatre fenêtres d'`Announce` et la
boutique de 2007 sont déclarées dans les bases de Final Showdown.

**Suspendu** : la correction du §22. `qdan` garde son nom d'origine et
`ecrase_fs=True`. Le picto de grade reste invisible, comme il l'est depuis le
2026-09-30 — le §22 reste juste sur le fond, c'est sa *correction* qui ne
passe pas.

**La suite, dans cet ordre** :

1. renommer **le jeu de sprites seul** (`spr_pose` sans `aet_pose`) et lancer.
   S'il casse, la texture est en cause ; s'il tient, c'est la planche AET ;
2. si c'est la texture : réencoder `tex00` de RGBA4 (format 5) vers RGBA8
   (format 2) dans notre copie. La chaîne existe en entier —
   `tools/txp.py` décode le format 5, `tools/textures_hd.py` réécrit ces
   archives, et le §235 du journal dit la chaîne « éprouvée de bout en bout »
   sur `spr_n_term` tex07. L'archive gonflerait de 4 Mo à 8 Mo décompressés
   pour cette texture ;
3. et dans tous les cas, **poser l'instrument qui manque** (§23.6) : une ligne
   de journal par chargement demandé, avec l'état rendu à chaque trame, pour
   que la prochaine fois le journal dise *lequel* des six ne vient pas, au
   lieu de s'arrêter en silence.

---

## 25. LA VRAIE CAUSE : LE NOM DU MEMBRE DANS L'ARCHIVE (2026-10-19)

### 25.1 CE QUE LE §24 AVAIT MANQUÉ

Une archive de sprites n'est pas un fichier : c'est un **FArC**, et le jeu de
sprites vit dedans sous un **nom de membre**. La base nomme le fichier
`<pose>.bin` ; le moteur ouvre `<pose>.farc` et y cherche le membre
`<pose>.bin`.

Or `ajouter()` copiait l'archive **telle quelle** (`shutil.copyfile`). Quand
le nom posé diffère du nom source, le membre garde donc l'ancien nom :

| archive sur le disque | membre dedans | la base nomme | |
|---|---|---|---|
| `spr_n_que.farc` | `spr_n_que.bin` | `spr_n_que.bin` | OK |
| `spr_n_qwin.farc` | `spr_n_qwin.bin` | `spr_n_qwin.bin` | OK |
| `spr_s_gamdan.farc` | `spr_s_gamdan.bin` | `spr_s_gamdan.bin` | OK |
| **`spr_q_dan.farc`** | **`spr_s_gamdan.bin`** | **`spr_q_dan.bin`** | **NON** |
| **`spr_q_cmn.farc`** | **`spr_n_cmn.bin`** | **`spr_q_cmn.bin`** | **NON** |
| **`spr_q_cstm.farc`** | **`spr_n_cstm.bin`** | **`spr_q_cstm.bin`** | **NON** |

**Le membre n'était jamais trouvé, le jeu de sprites ne devenait jamais prêt,
et l'étape 2 attendait indéfiniment.** Voilà pourquoi le journal s'arrêtait
après « planche et sprites demandes 526 ».

Et `qcmn`/`qcstm` portaient **le même défaut**, muet seulement parce que la
greffe ne charge pas encore 628 et 629 : il aurait mordu le jour où la
boutique ou `Announce` seraient câblées.

### 25.2 LA CORRECTION

`ajouter()` réécrit maintenant l'archive avec le membre renommé, quand le nom
posé diffère de la source, par **`farc.comme()`** — qui préserve la variante
(`FArC`) et l'alignement du modèle. Ce n'est pas une précaution de style :
poser un `FArc` brut là où le jeu avait un `FArC` **ferme le jeu**, c'est
mesuré (journal du 2026-10-11, `spr_n_fnt32`).

Relu après la pose, sur les cinq archives :

    spr_n_que.farc    membre spr_n_que.bin    base spr_n_que.bin    OK
    spr_n_qwin.farc   membre spr_n_qwin.bin   base spr_n_qwin.bin   OK
    spr_q_dan.farc    membre spr_q_dan.bin    base spr_q_dan.bin    OK
    spr_q_cmn.farc    membre spr_q_cmn.bin    base spr_q_cmn.bin    OK
    spr_q_cstm.farc   membre spr_q_cstm.bin   base spr_q_cstm.bin   OK

toutes en `FArC`, alignement 0x1, et le membre de `spr_q_dan.bin` se relit :
6 397 104 octets, sept textures, formats 2, 5, 6, 9 — **inchangé**.

### 25.3 ET LE FORMAT RGBA4 N'Y ÉTAIT POUR RIEN

**Le mode Quest se lance**, avec le renommage complet de `qdan`, et le
journal le dit :

    [quest] ecran Quest : planche et sprites demandes 526
    [quest] musique du Quest lancee (rom/sound/bgm/vf5ps3_b03map.adx) 0
    [quest] planches PRETES apres (ms) 719

**Le moteur charge donc, pour la première fois, la planche de 2007 ET son jeu
de sprites — texture `tex00` en RGBA4 comprise.** Le format 5 est supporté.
Le §24.3 avait trouvé une vraie singularité et en avait tiré la mauvaise
conclusion : *la seule différence visible n'est pas forcément la cause.*

### 25.4 LE PICTO N'APPARAÎT TOUJOURS PAS — ET C'EST NORMAL

Capture de Frédéric, la fiche en bas à gauche de la carte :

    NO-NAME                    10th kyu
    W:    0   L:    0
    Win ratio: 0.00%           50000G

**Le joueur est au grade 0.** Et `quest_grade_calque()` rend **NULL** pour le
grade 0, de propos délibéré :

```c
static const char *const kyu[10] = {
    0, "s_gamdan_kyu09", "s_gamdan_kyu08", … "s_gamdan_kyu01" };
if (g < 10) return kyu[g];
```

Son commentaire dit pourquoi : « Le grade 0 est le 10e kyu, le plus bas, et la
planche n'a pas de picto pour lui : elle commence au 9e (`kyu09`). » Le
dessin teste `if (gr)` avant de poser le calque : **aucun picto n'est
demandé.** Mesuré aussi dans le fichier : `quest_profil.bin + 0x12C` vaut
**0**.

**Ce n'est donc pas un échec, c'est le comportement attendu à ce grade.** Et
la liste des rivaux n'aidera pas : son propre commentaire dit « tant que le
picto n'est pas dessiné, il est en toutes lettres » — elle écrit le grade en
texte.

**Le seul endroit qui demande un picto est la fiche du joueur, au grade ≥ 1.**
Pour le voir sans jouer, on pose le grade à la main : `quest_profil.bin`
`+0x12C` = 1 (9e kyu). C'est fait, l'ancien profil est gardé à côté, et le
reste des 592 octets est intact.

### 25.5 CE QUE CETTE SÉANCE A APPRIS SUR LA MÉTHODE

Trois fois de suite, aujourd'hui, la même faute et la même correction :

1. **§21.2** — j'ai déduit un « trou » dans `FUN_8231F1D8` de la *forme* d'un
   `if`, sans lire la fonction appelée. Elle ne lisait rien du tout.
2. **§24.3** — j'ai désigné une texture au format unique parce que c'était la
   seule singularité visible. La cause était ailleurs, à un étage que je
   n'avais pas regardé : le **contenant**, pas le contenu.
3. **§22** — « le fichier est posé » n'est pas « le fichier est lu ». Et
   maintenant : « le fichier est lu » n'est pas « le membre est trouvé ».

La règle qui aurait évité les trois : **descendre d'un étage avant de
conclure.** Le résolveur a trois niveaux (FArC embarqué, `.par`, disque) et
l'archive en a un quatrième (le membre). Chacun peut rendre « rien » sans
lever d'erreur.

### 25.6 L'ÉTAT

| | |
|---|---|
| les quinze musiques | **posées**, `b03map` joue (journal) |
| `qcmn` 531 / sprites 628 / scènes 690-691 | **posée**, `aet_q_cmn.bin` — les quatre fenêtres d'`Announce` |
| `qcstm` 532 / sprites 629 / scène 692 | **posée**, `aet_q_cstm.bin` — la boutique et l'éditeur |
| `qdan` 530 / sprites 627 | **renommée**, `aet_q_dan.bin` — la planche de FS n'est plus masquée par la nôtre |
| le mode Quest | **se lance**, planches prêtes en 719 ms |
| le picto de grade | **non vu** : le joueur était au grade 0, qui n'en a pas |

Reste à câbler 531/628/690 et 532/629/692 dans `tools/quest_runtime.c` : les
planches sont déclarées, personne ne les demande encore.

---

## 26. `questV2.cmd`, ET LA PLANCHE DE GRADE A DEUX FAMILLES (2026-10-19)

### 26.1 `quest.cmd` ÉTAIT UNE RÉGRESSION — constat de Frédéric

Le diff des deux lanceurs, option par option :

| | options |
|---|--:|
| `tools/item_porte.cmd` | **61** |
| `tools/quest.cmd` | **37** |

**`quest.cmd` n'apporte que cinq options**, dont trois comptent pour le mode
Quest (`--bases-2d-libres`, `--quest-ecran`, `--textes-quest` ;
`--options-sans-howto` est posée toute seule par le patcheur dès que
`--options-v2` et `--sp-lancer` sont là, et `--decors-dural cas` est son choix
propre).

**Et il en perd vingt-neuf** — c'est-à-dire tout le travail des trois
dernières semaines :

    --options-v2 --options-dural --options-resolution --options-mode
    --menu-griser --versus-joueur2 --versus-manette --terminal-ordre
    --film-cadres --films-theatre --nom-donnees --sans-ecran-epilepsie
    --sans-warning --item-basculer --selitem-grille --selitem-republier
    --selitem-ecreter --selpart-curseur --variantes-texte --variantes-5r
    --variantes-vf5 --decors-5r --decors-vf5 --decors-5r-dural
    --decors-table --grille-table --decor-ecretage --decor-repli
    --obj-db-libre

J'ai travaillé une journée entière sur ce lanceur-là sans le voir. **Le
dossier ne dit nulle part lequel des `.cmd` fait foi** — et c'est ce qui
manquait.

### 26.2 `tools/questV2.cmd`

Copie de `item_porte.cmd`, **mot pour mot**, plus quatre options :

    --bases-2d-libres   le moteur lit ./rom/2d/, ou les planches sont declarees
    --quest-ecran       la greffe, sur la branche morte de la ligne 3
    --textes-quest      les 492 chaines du mode
    --quest-degriser    item_porte grise QUEST MODE avec ONLINE VERSUS en UNE
                        instruction ; cette option passe l immediat de
                        0x1801E3A0A de 0x0101 a 0x0001

**Soixante-cinq options, et le patcheur les prend toutes** : aucun refus,
aucune greffe pleine. Relu dans la DLL produite :

    QUESTBOX                                      1 occurrence
    0x1801E3A0A  mov word [rbx+0x644], 1          entree 2 grisee, entree 3 a 0
    0x1801E3A03  mov byte [rbx+0x648], 1          entree 6 (SCOREBOARDS) grisee
    0x1801DE0C0  jmp 0x180EA4620                  la ligne 3 saute dans la greffe
    0x1801DDF54  cmp byte [rcx+rdi+0x642], 0 / je le validateur passe
    0x1801E4CD8  cmp byte [rax+rcx+0x642], 0 / je le curseur accepte

Le fichier est en **ASCII pur et CRLF** (les deux guillemets français de
`item_porte.cmd` sont devenus droits), 20 812 octets, 419 CRLF, zéro LF
solitaire.

### 26.3 LA PLANCHE DE GRADE PORTE DEUX FAMILLES, ET J'AI PRIS LA MAUVAISE

Capture de Frédéric, au grade 1 : ce n'est pas un picto qui s'affiche sur la
fiche, c'est **tout l'écran de montée en grade** — le cadre ouvragé, les
volutes, la bannière « Promoted to 9th kyu » et le bandeau « Official Rank »,
par-dessus la carte.

Le relevé de `aet_q_dan.bin` l'explique : la planche porte **deux familles**.

| famille | ce que c'est | compte |
|---|---|--:|
| `s_gamdan_kyu01..09`, `s_gamdan_dan01..10`, `s_gamdan_shogo_*` | **les écrans entiers** — ils entraînent `frame_kyu_top/side/bottom`, `effect_kyu`, `kyu_base`, les plaques de décor et le texte `s_gamdan_l_shokaku_kyu__c4.pic` | 9 + 10 + 22 |
| **`kyu_plate_01..09`**, **`dan_plate_01..10`** | **les plaques seules**, sans cadre ni effet | **9 + 10** |

Dix-neuf plaques : exactement le compte des grades 1 à 19. Et les vingt-deux
titres n'ont **pas** de plaque — au-delà du grade 19, on reste en toutes
lettres, comme le code le faisait déjà.

`quest_grade_calque()` prend donc les plaques. **Le sens de la numérotation
n'est PAS mesuré** : on suppose le même que celui des écrans (`_09` = 9e kyu,
le plus bas, donc le grade 1). Si les plaques sortent à l'envers, il suffit de
retourner la table `kyu`.

### 26.4 L'ÉTAT, ET CE QU'IL FAUT REGARDER

`tools/questV2.cmd` est posé, la DLL et `apm.dll` sont à jour, le profil est
au **grade 1** (9e kyu) pour que le picto soit demandé — l'ancien profil est
gardé à côté.

**À regarder, dans cet ordre** :

1. la fiche en bas à gauche de la carte : une **petite plaque** de grade, et
   non plus l'écran entier ;
2. si la plaque est là mais que c'est la mauvaise (1er kyu au lieu du 9e), la
   table `kyu` de `quest_grade_calque()` est à retourner ;
3. et tout le reste de `item_porte.cmd` doit continuer de marcher — OPTIONS à
   quatre sous-menus, la manette du joueur 2, VF.TERMINAL, le Movie Theater,
   les quatre-vingt-six décors. C'est le vrai enjeu de `questV2` : **ne rien
   perdre.**

Reste, non câblé : les planches `qcmn` (531, sprites 628, scènes 690-691) et
`qcstm` (532, sprites 629, scène 692) sont déclarées dans les bases, mais
`tools/quest_runtime.c` ne les demande pas encore.

---

## 27. LE PICTO DE GRADE N'EST PAS UN CALQUE NOMMÉ (2026-10-19)

### 27.1 DEUX ESSAIS, DEUX FOIS L'ÉCRAN ENTIER

`s_gamdan_kyu09`, puis `kyu_plate_09` : les deux font apparaître **tout
l'écran de montée en grade** par-dessus la carte — le cadre ouvragé, les
volutes, « Promoted to 9th kyu », « Official Rank ».

### 27.2 LA PLANCHE `aet_s_gamdan` EST CELLE DE L'ÉCRAN DE PROMOTION, ET RIEN D'AUTRE

Ses sept textures, exportées depuis `spr_q_dan.farc` :

| texture | taille | format | ce qu'elle porte |
|---|---|--:|---|
| tex00 | 2048x1024 | 5 (RGBA4) | **les textes** : les 22 titres (*Vanquisher*, *Conqueror*…), « Promoted to », « Official Rank », les ordinaux *1st*..*10th*, « kyu », « dan », et deux illustrations (statue, faucon) |
| tex01 | 1024x512 | 6 | une flamme et un halo rouge |
| tex02 | 2048x512 | 9 | **les cadres** : barres, volutes, joyaux, et les plaques de la bannière |
| tex03 | 1024x512 | 9 | d'autres volutes et barres |
| tex04-06 | petites | 9, 9, 2 | éclats et dégradés |

**Pas un seul petit badge.** Les `kyu_plate_NN` et `dan_plate_NN` sont les
**plaques de la bannière**, pas des pictos : c'est le cartouche sur lequel le
texte « Promoted to » se pose.

### 27.3 ET LE VRAI PICTO N'EST PAS UN CALQUE : C'EST UN EMPLACEMENT VIDE

Dans `aet_s_gamcmn` de 2007 — la planche du HUD de combat — quatre calques
portent le nom cherché :

    dan_icon_1p_c          pos (62, 157)   origine (12, 12)
    dan_icon_2p_c          pos (1218, 157) origine (12, 12)
    dan_icon_team_on_1p_c  pos (245, 140)  origine (12, 12)
    dan_icon_team_on_2p_c  pos (1039, 140) origine (12, 12)

Résolus jusqu'à leur surface : **24 x 24, et ZÉRO source.** Ce sont des
**bouchons**. L'AET déclare l'EMPLACEMENT ; c'est le **code** qui y pose, à
l'exécution, un sprite choisi d'après le grade.

Et c'est la même forme sur la carte du Quest : l'ancre `p_dan_c` de
`aet_n_que` est en (588, 447) avec une **origine (12, 12)** — 24 x 24, le
même emplacement.

`dan_icon` est d'ailleurs **introuvable dans les dix-huit planches de Final
Showdown** : la planche du HUD de 2007 n'est pas posée.

### 27.4 CE QUE NOTRE GREFFE NE SAIT PAS FAIRE — ET LE CODE LE DISAIT DÉJÀ

`tools/quest_runtime.c` ne sait poser que des **calques nommés**. Dessiner un
sprite par identifiant à une ancre, il ne sait pas. Son propre commentaire,
écrit le 2026-09-29, le dit en toutes lettres :

> « LE GRADE EST UN PICTO CHEZ 2007 […] **Tant que le dessin de sprite n'est
> pas écrit, on rend le grade EN TEXTE.** »

Je ne l'avais pas lu jusqu'au bout. La note qui suit — « Final Showdown a la
planche (`spr_s_gamdan`) » — m'a fait croire qu'il suffisait de nommer le bon
calque. **Il n'y a pas de bon calque.**

`quest_grade_calque()` rend donc **0** de nouveau : aucun picto n'est demandé,
le grade reste en toutes lettres, et rien de faux ne se dessine. Le profil est
rendu au **grade 0**, comme Frédéric l'avait.

### 27.5 CE QU'IL FAUDRAIT, ET DANS QUEL ORDRE

1. **savoir dessiner un sprite par identifiant à une ancre** — c'est la
   capacité qui manque à la greffe, et elle servirait aussi aux icônes
   d'objets, aux emblèmes et aux portraits ;
2. **trouver la table grade → identifiant de sprite** dans le code de 2007 :
   c'est elle qui remplit le bouchon `dan_icon_1p_c`. Le lecteur est à
   chercher autour de `FUN_82309BA0`, qui dessine déjà le grade d'un rival
   dans le menu d'une salle (§19.4) ;
3. et **poser la planche qui porte les 42 badges** — elle n'est pas
   `aet_s_gamdan`, et elle n'est dans aucune des dix-huit planches de FS. À
   trouver dans le média de 2007.

### 27.6 LA LEÇON, LA QUATRIÈME DE LA JOURNÉE

**Un nom qui ressemble à ce qu'on cherche n'est pas ce qu'on cherche.**
`s_gamdan_kyu09` *contient* « kyu09 » et désigne l'écran entier ;
`kyu_plate_09` ressemble encore plus à une plaque de grade et n'en est pas
une. Deux fois j'ai choisi sur le nom, sans résoudre ce que le calque
dessine. La troisième fois — en résolvant la surface jusqu'à ses sources — la
réponse est tombée en une commande : **24 x 24, zéro source.**

---

## 28. LE BADGE DE GRADE EST DANS `aet_c_cmn` / `spr_c_cmn` DE 2007 (2026-10-19)

Frédéric a montré le badge : une plaque rouge, « 10th kyu » en blanc, environ
130 x 30 — et il a vu juste sur les deux points. Le texte **est** dans
`tex00` de `spr_s_gamdan`, mais « la couleur ne colle pas et la résolution
semble trop élevée ». Les deux observations sont exactes, et elles disent
pourquoi ce n'était pas la bonne planche.

### 28.1 `spr_s_gamdan` PORTE LE MÊME TEXTE, MAIS EN GRAND

Ses sprites nommés, relevés dans la table (0x28 octets par enregistrement) :

    L_KYU_1 .. L_KYU_9      188 x 92   (L_KYU_2 : 196 x 92)
    L_DAN_1 .. L_DAN_10     170..238 x 92
    L_KYU, L_DAN            188 x 92 / 188 x 100
    L_KYU_NINTEI            252 x 110     « Official Rank »
    L_SHOKAKU_KYU           388 x 76      « Promoted to »

**188 x 92 contre 88 x 30** : c'est le texte de la **bannière de promotion**,
dessiné en grand, pas le badge. Et sa texture est en **RGBA4** (format 5),
d'où les teintes pâles — c'est une autre illustration, pas une autre
colorimétrie.

### 28.2 LE VRAI BADGE : `spr_c_cmn.farc`, 45 SPRITES

Balayage de **tous** les `spr_*.farc` du média de 2007, à la recherche de
sprites « kyu »/« dan » de moins de 260 x 70. **Deux fichiers répondent**, et
l'un porte tout :

| sprite | taille | ce que c'est |
|---|---|---|
| **`DAN_BASE1P`** | **102 x 30** | **la plaque ROUGE** (joueur 1) |
| `DAN_BASE2P` | 102 x 30 | la plaque BLEUE (joueur 2) |
| `DAN_BASEGREY` | 102 x 30 | la plaque GRISE |
| **`DAN_KYU_10`** | **88 x 30** | **« 10th kyu »** |
| `DAN_KYU_1` .. `DAN_KYU_9` | 74..78 x 28 | les neuf autres kyu |
| `DAN_DAN_1` .. `DAN_DAN_10` | 72..88 x 26 | les dix dan |
| `DAN_KAIDEN`, `DAN_MOSA`, `DAN_KYOUSHA`, `DAN_KOUSHA`, `DAN_TETSUJIN`, `DAN_TATSUJIN`, `DAN_MEIJIN`, `DAN_BUSHOU`, `DAN_TOUSHOU`, `DAN_MEISHOU`, `DAN_BUSEI`, `DAN_TOUSEI`, `DAN_KENSEI`, `DAN_BUSHIN`, `DAN_TOUSHIN`, `DAN_KENSHIN`, `DAN_BUOH`, `DAN_TOUOH`, `DAN_KENOH`, `DAN_KOUTEI`, `DAN_TAITEI`, `DAN_TENTEI` | 60..104 x 24..30 | **les vingt-deux titres** |

**Dix kyu + dix dan + vingt-deux titres = quarante-deux**, exactement
l'étendue de `npc_tbl + 0x7C` mesurée au §21.1 (42 valeurs, 0 à 41).

La texture qui les porte est **`tex08`, 512 x 1024, format 2 (RGBA8)** — d'où
les couleurs franches. Reconstitué à la main (`DAN_BASE1P` + `DAN_KYU_10`
centré) : **c'est la capture de Frédéric, à l'identique.**

### 28.3 ET IL Y A UN CALQUE NOMMÉ PAR GRADE — LE DESSIN DE SPRITE N'EST PAS NÉCESSAIRE

C'est ce qui change tout par rapport au §27. La planche `aet_c_cmn` de 2007
porte **un calque vidéo par grade**, chacun avec **une source** :

    c_cmn_dan_kyu_10.pic   surface  88x30   source C_CMN_DAN_KYU_10
    c_cmn_dan_kyu_9.pic    surface  76x28   source C_CMN_DAN_KYU_9
    …
    c_cmn_dan_dan_10.pic   surface  88x26   source C_CMN_DAN_DAN_10
    c_cmn_dan_kaiden.pic   surface  66x26   source C_CMN_DAN_KAIDEN
    …

**Des calques nommés, avec une surface réelle et une source** — exactement ce
que `tools/quest_runtime.c` sait déjà poser. Le §27 concluait qu'il fallait
d'abord écrire le dessin de sprite par identifiant : **c'était vrai pour
`dan_icon` (24 x 24, zéro source) dans `aet_s_gamcmn`, et faux pour
`aet_c_cmn`.** La bonne planche rend le problème facile.

### 28.4 CE QU'IL RESTE À FAIRE, ET C'EST COURT

1. **déclarer `aet_c_cmn` / `spr_c_cmn` de 2007** dans les bases 2D — une
   entrée `qccmn` dans `tools/bases_2d.py`, avec `aet_pose` / `spr_pose` à
   part : Final Showdown a son propre `aet_c_cmn.bin`, non masqué dans le
   `.par`. Le mécanisme est celui posé aujourd'hui (§21.3), et le renommage
   du **membre** d'archive (§25.2) est indispensable ;
2. **rendre à `quest_grade_calque()` sa table**, pointant cette fois les
   calques `c_cmn_dan_kyu_NN.pic` / `c_cmn_dan_dan_NN.pic` et les vingt-deux
   titres — et poser la **plaque** (`DAN_BASE1P`) dessous, à l'ancre
   `p_dan_c` de `aet_n_que` (588, 447), dont l'origine (12, 12) convient à un
   calque centré ;
3. et les vingt-deux titres donnent enfin **l'ordre des grades 20 à 41**, que
   le dossier disait « PAS établi ». L'ordre des sprites dans la table de
   `spr_c_cmn` est un candidat à vérifier, pas une réponse.

### 28.5 LA MÉTHODE QUI A FINI PAR MARCHER

Trois essais sur le nom ont échoué (`s_gamdan_kyu09`, `kyu_plate_09`, puis la
bonne planche cherchée à l'œil dans les images). **Ce qui a tranché en une
commande, c'est de chercher par la MESURE** : balayer tous les jeux de
sprites, filtrer sur la **taille** (moins de 260 x 70, puisque le badge fait
130 x 30), et lire les noms qui restent. Deux fichiers sur soixante-dix, et
la réponse était dans le premier.

---

## 29. « POURQUOI NE PAS UTILISER LE GRADE DE FS ? » — ET IL AVAIT RAISON (2026-10-19)

J'allais importer `aet_c_cmn` / `spr_c_cmn` de 2007. Question de Frédéric
avant que je le fasse. La mesure lui donne raison, et l'import est **annulé**.

### 29.1 FINAL SHOWDOWN A DÉJÀ LES BADGES

Son `aet_c_cmn` et son `spr_c_cmn`, extraits du `.par` (489 184 et
1 185 381 octets), portent **87 sprites `DAN_*`** et **166 calques `dan`**.
Parmi eux, exactement ce qu'il fallait :

| calque de FS | taille | celui de 2007 | identique ? |
|---|---|---|:-:|
| `c_cmn_dan_base1p.pic` | 102 x 30 | `c_cmn_dan_base1p.pic` 102 x 30 | **oui** |
| `c_cmn_dan_base2p.pic` | 102 x 30 | idem | **oui** |
| `c_cmn_dan_kyu_10_e.pic` | **88 x 30** | `c_cmn_dan_kyu_10.pic` 88 x 30 | **oui** |
| `c_cmn_dan_kyu_1_e` .. `_9_e` | 74..78 x 28 | idem | **oui** |
| `c_cmn_dan_dan_1_e` .. `_10_e` | 72..88 x 26 | idem | **oui** |

Le suffixe `_E` est la version **anglaise** — FS porte les deux langues, 2007
n'en portait qu'une. Les tailles sont les mêmes au pixel près.

**Rien à déclarer, rien à importer, rien à charger en plus, aucune collision
de nom.** La planche est l'identifiant **1**, son jeu de sprites le **0**, sa
scène `MAIN` la **5** — tout dans la base d'origine de Final Showdown.

### 29.2 CE QUE FS N'A PAS : LES VINGT-DEUX TITRES

Les grades 20 à 41 — `DAN_KAIDEN`, `DAN_MOSA`, `DAN_KENSEI`, `DAN_TENTEI`… —
n'existent que dans le média de 2007. Final Showdown les a remplacés par son
propre système de rangs en ligne : `DAN_BASE_BRZ`, `SLV`, `GLD`, `DIA`,
`MAS`, `SEI`, `STN`, `WOD`, chacun en trois à six paliers, 100 x 40.

C'est **la seule** raison qui justifierait d'importer `aet_c_cmn` de 2007, et
elle ne se présentera qu'au grade 20. En attendant, au-delà du grade 19 on
reste en toutes lettres.

### 29.3 CE QUI EST CÂBLÉ

`tools/quest_runtime.c` :

    #define QUEST_AET_CCMN    1     /* AET_C_CMN, la planche commune de FS */
    #define QUEST_SPR_CCMN    0     /* SPR_C_CMN */
    #define QUEST_SCENE_CCMN  5     /* AET_C_CMN_MAIN */

`quest_grade_calque()` rend les calques de FS, grade 0 → `kyu_10_e`,
grade 9 → `kyu_1_e`, grade 10 → `dan_1_e`, grade 19 → `dan_10_e`, 0 au-delà.

Le badge est dessiné en **deux calques**, comme 2007 le compose : la plaque
`c_cmn_dan_base1p.pic` en priorité `+4`, le libellé par-dessus en `+5`. Et
l'étape 1 charge désormais la planche commune (1 et 0) et l'attend comme les
cinq autres.

**ET LE GRADE 0 A MAINTENANT UN BADGE.** `aet_s_gamdan` n'avait pas de picto
pour le 10e kyu — c'est pour cela que la fiche restait nue au §25.4. La
planche commune, elle, porte `kyu_10`. Le profil de Frédéric est resté au
**grade 0**, intact, et le badge doit s'y voir.

### 29.4 L'ÉTAT

Bases **CONFORMES**, trois planches posées (`qdan` 530, `qcmn` 531,
`qcstm` 532), `qccmn` retiré, `apm.dll` recompilée, profil intact.

### 29.5 LA LEÇON

**Avant d'importer, regarder ce que la cible a déjà.** J'ai passé quatre
paragraphes (§27, §28) à chercher dans le média de 2007 un badge que Final
Showdown avait sous la main, dans sa planche la plus commune. La question qui
l'a trouvé n'était pas une mesure de plus : c'était « pourquoi ne pas
utiliser celui de FS ? »

---

## 30. LE BADGE NE SE DESSINAIT PAS : UN RANG HORS DU TABLEAU (2026-10-19)

Le câblage du §29 était bon — planche de FS, calques nommés, chargement
abouti (`planches PRETES apres 703 ms`) — et **rien ne se dessinait**. La
faute est à moi, et elle tient en un nombre.

### 30.1 LE TABLEAU DES RANGS FAIT VINGT-QUATRE CASES

```c
static const char *g_quest_pose[24];
static char g_quest_phase[24];
```

Indices **0 à 23**. Et j'avais pris :

    #define QUEST_RANG_GRADE    23      /* le libelle  -- dernier index valide */
    #define QUEST_RANG_PLAQUE   24      /* la plaque   -- HORS DU TABLEAU */

`g_quest_pose[24] = …` écrit **au-delà de la fin** du tableau, très
probablement dans `g_quest_phase[0]`, et la machine de pose part en vrille :
ni la plaque ni le libellé ne sont posés.

Et le rang n'est pas libre non plus côté moteur. Le relevé du 2026-09-12 —
le balayage des `mov edx, imm32` devant les 44 sites d'appel de
`creer`/`liberer`/`fini` — dit que **Final Showdown se sert des rangs 1, 7 et
15 à 23**. Le 24 n'est pas dans la liste, et `0x180171E90` indexe son tableau
**sans borne**.

### 30.2 LA PLAQUE PREND LE RANG 1

C'est le seul libre sous 23. Il appartient au **menu de Final Showdown**,
démonté pendant que notre état tient l'écran — le même raisonnement qui a
servi pour les rangs 15 à 23 (les neuf bâtiments et le libellé de grade).

    #define QUEST_RANG_PLAQUE   1

### 30.3 ET ON REND CE QU'ON OCCUPE

`quest_retirer_calques()` ne libérait que les rangs **7 à 13**. Les neuf
bâtiments (14 à 22) et le libellé de grade (23) restaient posés en quittant
l'écran — un défaut présent depuis le 2026-09-30 et jamais vu, parce que ces
calques finissent par s'éteindre d'eux-mêmes.

Le rang **1**, lui, ne pardonne pas : c'est celui du menu de FS, et on y
retourne en sortant. La fonction libère donc maintenant **1, 7 à 13, et 14 à
23**.

### 30.4 LA LEÇON

Un tableau de 24 cases et une constante à 24 : le dépassement d'un cran. Rien
ne l'a signalé — pas de garde, pas de journal, pas d'erreur. **Le compilateur
ne pouvait pas le voir** (les constantes ne sont pas comparées à la taille du
tableau), et le jeu non plus.

Ce qui l'a trouvé : relire **ce que la greffe fait du rang**, et non ce
qu'elle en dit. Le commentaire du fichier donnait pourtant la réponse en
clair, trois lignes au-dessus de ma constante : « FS se sert de 1, 7, et 15 a
23 ».

---

## 31. L'ORGANISATION DES FENÊTRES, DES SPRITES ET DES TEXTES — LA LOI QUI MANQUAIT (2026-10-19)

Trois essais ratés sur le badge de grade, et chacun a buté sur la même chose
sans que je la voie. Frédéric : « relis dans le code du jeu de 2007
l'organisation des fenêtres, sprites et textes. » La voici, mesurée.

### 31.1 LE JOURNAL A ÉLIMINÉ DEUX FAUSSES PISTES

L'instrument posé rend :

    [quest] c_cmn_dan_kyu_10_e.pic 0
    [quest]   ... calques deja dans la liste 5

Le calque **est demandé**, avec le bon grade, et **cinq** entrées seulement le
précèdent — la liste de 24 (élargie à 32) ne débordait pas. Mes deux
hypothèses précédentes — le rang hors tableau, la liste pleine — étaient
fausses **toutes les deux**. C'est la **création** qui échoue.

### 31.2 LA LOI : `creer` NE VOIT QUE LA COMPOSITION RACINE

Comparaison de ce qui marche et de ce qui ne marche pas, dans la même forme :

| calque | planche / scène | composition |
|---|---|---|
| `map_base`, `map_aero`, `tit`, `p_dan_c` | `aet_n_que` / MAIN | **65 sur 65 — RACINE** |
| `c_cmn_dan_base1p.pic` | `aet_c_cmn` / MAIN | 77 sur 103 — **sous-composition** |
| `c_cmn_dan_kyu_10_e.pic` | `aet_c_cmn` / MAIN | 79 et 80 sur 103 — **sous-composition** |

**Tout ce que la greffe a jamais posé avec succès est à la RACINE de sa
scène.** `0x180171E90(ctx, rang, scene, calque, prio, drapeaux)` cherche le
calque par son nom **dans la composition racine**, et rend sans bruit quand
il ne l'y trouve pas : pas d'erreur, pas de journal, rien à l'écran.

C'est la troisième façon, dans cette seule journée, qu'un relevé a de rendre
« rien » sans lever d'erreur — après le `.par` qui passe avant le disque
(§22) et le membre d'archive mal nommé (§25).

### 31.3 À LA RACINE, LE BADGE PORTE UN SEUL NOM

La racine de `AET_C_CMN_MAIN` compte 53 calques, dont :

    dan_icon1p      dan_icon1p_e     dan_icongray
    dan_icon2p      dan_icon2p_e
    dan_com_1p / 2p    dan_comko_1p / 2p
    dan_ai_1p / 2p     dan_deshi_1p / 2p

**Le badge entier est UNE composition** : plaque et libellé ensemble,
`_e` pour la version anglaise, `gray` pour la version grise, `1p` / `2p` pour
la couleur de plaque (rouge / bleue).

### 31.4 ET LE GRADE EST LE NOM D'UN MARQUEUR

`dan_icon1p_e` va de la trame 0 à la trame **2820**, et porte
**quarante-sept marqueurs** :

    trame    0  « 0 »        trame  600  « 10 »       trame 2700  « 45 »
    trame   60  « 1 »        ...                      trame 2760  « end »
    trame  120  « 2 »

**Un marqueur toutes les soixante trames, et son nom est le numéro du
grade.** Quarante-six grades, 0 à 45 — l'échelle de Final Showdown, plus
longue que les quarante-deux de 2007 (`npc_tbl + 0x7C`, §21.1). La
correspondance au-delà du grade 41 **n'est pas mesurée**.

C'est exactement l'idiome que la greffe emploie déjà pour les photos de lieu
(`sta_s` → `sta_e`, « une fois, puis elle tient sa dernière image »). On pose
donc la composition et on la joue de `<grade>` à `<grade+1>` : elle s'arrête
sur la bonne image et la garde.

### 31.5 CE QUI EST CÂBLÉ

    t[n].rang  = QUEST_RANG_GRADE;      t[n].scene = QUEST_SCENE_CCMN;  /* 5 */
    t[n].nom   = "dan_icon1p_e";        t[n].prio  = QUEST_PRIO + 5;
    t[n].sta_s = "<grade>";             t[n].sta_e = "<grade+1>";

**Un seul calque**, plus deux : la plaque est dans la composition. Le rang 1
n'est plus occupé, et `quest_grade_calque()` rend désormais un **nom de
marqueur**, pas un nom de calque.

### 31.6 CE QUE CETTE LOI CHANGE POUR LA SUITE

Elle vaut pour tout ce qui reste à câbler, et elle économisera les mêmes
erreurs :

- **les quatre fenêtres d'`Announce`** (`qcmn`, planche 531) et **la
  boutique** (`qcstm`, 532) : avant de les poser, il faut vérifier que leurs
  calques sont à la **racine** de leur scène. S'ils sont dans une
  sous-composition, c'est le nom de la composition racine qui les contient
  qu'il faut poser, et un marqueur qui choisit la variante ;
- **le grade des rivaux** dans le menu d'une salle et la liste : même badge,
  même composition, marqueur donné par `npc_tbl + 0x7C` ;
- et **ce qu'il faudrait pour aller plus loin** : un outil qui, pour un nom de
  calque donné, dise *dans quelle composition il vit, et si c'est la racine*.
  `tools/ancres_ecrans.py` relève déjà la composition (`c70`, `c83`…) ; il
  lui manque de dire laquelle est la racine, et c'est une ligne.

---

## 32. LE BADGE ÉTAIT DESSINÉ — EN (0, −24), HORS DE L'ÉCRAN (2026-10-19)

Le §31 avait la bonne loi et le bon calque. Le journal, après recâblage :

    [quest] 0 0

— le marqueur « 0 » demandé pour le grade 0. **La pose a lieu.** Ce n'était
donc plus « introuvable » : c'était **où**.

### 32.1 LA GÉOMÉTRIE, EN TROIS MESURES

| | origine | position |
|---|---|---|
| `dan_icon1p_e`, calque **racine** de `AET_C_CMN_MAIN` (scène **1280 x 768**) | **(640, 384)** | (640, 384) |
| son contenu, dans la composition : `c_cmn_dan_kyu_10_e.pic` | (44, 15) — son centre | **(0, 0)** |
| l'ancre visée, `p_dan_c` de `aet_n_que` | (12, 12) | **(588, 447)** |

Le moteur dessine à **`position_passée − origine`** — c'est ce que le
commentaire de `g_quest_centre` établissait déjà le 2026-09-30, pour les neuf
bâtiments.

Or on passait `g_quest_centre`, **(640, 360)**, qui convient aux
compositions de `aet_n_que` : leur scène fait 1280 x **720** et leur origine
(640, **360**). Mais `aet_c_cmn` fait 1280 x **768**, origine (640, **384**).

    (640, 360) − (640, 384) = (0, −24)

**Le badge se dessinait dans le coin haut-gauche, vingt-quatre pixels
au-dessus du bord.** Invisible, et le journal n'avait rien à signaler : la
pose avait bien eu lieu.

### 32.2 LA CORRECTION

    position = ancre + origine = (588 + 640, 447 + 384) = (1228, 831)

Le nombre dépasse l'écran, et c'est normal : ce n'est pas un point de
l'écran, c'est une valeur dont le moteur retranche l'origine.

### 32.3 CE QUE CELA AJOUTE À LA LOI DU §31

Poser un calque de FS demande **trois** choses, pas une :

1. **le nom doit être celui d'un calque de la composition RACINE** (§31.2) ;
2. **la variante se choisit par un MARQUEUR**, pas par un nom (§31.4) ;
3. **la position doit tenir compte de l'origine ET de la résolution de la
   scène d'où vient le calque.** `aet_n_que` est en 1280 x 720, `aet_c_cmn`
   en 1280 x 768 : la même constante « le centre » ne vaut pas pour les deux.

Ce troisième point n'était écrit nulle part, et il explique pourquoi
`g_quest_centre` — juste depuis trois semaines pour tout ce qui vient de
`aet_n_que` et `aet_n_qwin` — était faux dès qu'on empruntait une planche à
une autre scène.

---

## 33. LE BADGE DE GRADE : SUSPENDU, ET CE QUI EST ACQUIS (2026-10-19)

Six hypothèses, six échecs, et trop de temps pour un sprite. Constat de
Frédéric, et il a raison. Le badge est **suspendu derrière un interrupteur**
(`#define QUEST_BADGE 0` dans `tools/quest_runtime.c`) : le grade reste en
toutes lettres — lisible et juste — et il suffit de remettre `1` pour
reprendre, tout le reste étant en place.

### 33.1 LES SIX HYPOTHÈSES, ET CE QUE CHACUNE A APPRIS

| # | hypothèse | verdict | ce qui reste acquis |
|--:|---|---|---|
| 1 | le calque est `s_gamdan_kyu09` | **faux** | `aet_s_gamdan` est la planche de l'**écran de promotion** ; son texte fait 188x92 (§27) |
| 2 | c'est `kyu_plate_09` | **faux** | les `*_plate_*` sont les plaques de la **bannière**, pas des badges (§28) |
| 3 | il faut importer `aet_c_cmn` de 2007 | **inutile** | FS a déjà les mêmes calques, aux tailles exactes (§29) |
| 4 | le rang 24 est libre | **faux** | `g_quest_pose[24]` s'arrête à l'index 23 ; FS emploie 1, 7, 15-23 (§30) |
| 5 | la liste de calques déborde | **faux** | le journal : cinq entrées seulement précèdent le badge (§31.1) |
| 6 | le calque n'est pas trouvé | **faux** | l'instrument rend un **identifiant d'objet 20** : il EST créé (§33.2) |

### 33.2 L'INSTRUMENT, ET IL EST GARDÉ

Posé dans `quest_pose()` : après `creer2`, il lit l'identifiant que le moteur
range en **`ctx + rang * 4 + 0x5C`** — ce que la décompilation de
`0x180171F40` établit — et journalise, une fois par changement :

    [quest] badge : identifiant de l objet cree 20
    [quest] badge : position x 1228
    [quest] badge : position y 831
    [quest] dan_icon1p_e 5
    [quest] 0 69

**Nul = le calque n'existe pas ; non nul = il existe.** C'est la distinction
qu'on ne savait pas faire, et qui a coûté quatre allers-retours. Elle servira
pour tout ce qui reste à câbler.

### 33.3 CE QUI EST MESURÉ, ET QUI NE BOUGERA PLUS

- **le badge est `dan_icon1p_e`**, calque **racine** de `AET_C_CMN_MAIN`
  (planche 1, sprites 0, scène 5) ; `2p_e` pour le joueur 2, `icongray`
  pour la version grise ;
- **la composition fait 2820 trames et porte 47 marqueurs**, « 0 » à « 45 »
  puis « end », un toutes les 60 trames ;
- **chaque grade occupe un créneau de 60 trames**, et les noms des calques
  internes le confirment : `dan_10_kyu` 0→60, `dan_09_kyu` 60→120,
  `dan_01_kyu` 540→600, `dan_01_dan` 600→660. **Le nom du marqueur est le
  grade**, et 0 est bien le 10e kyu ;
- **la géométrie** : origine du calque racine (640, 384), scène **1280 x 768**
  (et non 720), contenu en (0, 0). Le moteur dessine à
  `position − origine`, donc viser l'ancre `p_dan_c` (588, 447) demande
  `position = (1228, 831)` ;
- **la loi générale** : `0x180171E90` ne trouve un calque que dans la
  composition **RACINE** de sa scène (§31.2).

### 33.4 CE QUI RESTE INCONNU

Le calque est créé, posé, avec le bon marqueur et une position calculée — et
rien n'apparaît. Les pistes non explorées, dans l'ordre où je les prendrais :

1. **la règle `position − origine` n'a jamais été lue dans le moteur.** Elle
   vient d'un commentaire du 2026-09-30, corroboré par les neuf bâtiments à
   l'écran. `0x180171F40` ne fait qu'empaqueter un descripteur et appeler
   `FUN_180029A90` : c'est **là** qu'il faudrait descendre ;
2. **le drapeau passé à `creer2`.** Les photos de lieu emploient `0x20000`
   (« une fois, puis tient la dernière image ») ; on ne sait pas ce que la
   même valeur fait sur une composition à quarante-sept créneaux ;
3. **l'opacité**. La transforme du calque racine n'a pas été relevée pour
   `Opacite` — si elle est animée et vaut 0 hors des moments où FS montre son
   HUD, rien ne se verra quoi qu'on fasse ;
4. **la priorité 69** contre les calques de la carte (64) et la fenêtre (70) :
   non vérifiée à l'écran.

### 33.5 CE QUE CETTE SÉANCE DEVRAIT CHANGER DANS LA MÉTHODE

**Poser l'instrument AVANT la troisième hypothèse, pas après la sixième.**
L'identifiant d'objet était lisible depuis le début — il tenait en quatre
lignes de C — et il aurait éliminé d'un coup les hypothèses 1, 2, 4, 5 et 6.
J'ai préféré six fois « essayer autre chose » à une fois « mesurer où ça
casse ».

---

## 34. LA RÈGLE DE POSITION, MESURÉE PAR BALAYAGE (2026-10-19)

Quatre calculs faux. Le cinquième essai n'en a pas été un : **on pose le même
calque cinq fois, à cinq positions, et on regarde.**

### 34.1 LE BALAYAGE

Cinq rangs libres (2 à 6 — Final Showdown emploie 1, 7 et 15 à 23), le même
calque `dan_icon1p_e`, cinq positions, et **un grade différent par rang** pour
qu'ils se reconnaissent à l'écran :

| rang | position passée | grade affiché |
|--:|---|---|
| 2 | (0, 0) | 10th kyu |
| 3 | **(640, 384)** | **1st dan** |
| 4 | (1228, 831) — une ancre retranchée | 10th dan |
| 5 | (1868, 1215) — deux ancres retranchées | 5th kyu |
| 6 | pointeur nul | 6th dan |

Les six objets ont été créés (identifiants 20 à 25 — l'instrument du §33.2).
**Un seul s'est affiché, et il portait « 1st dan ».**

### 34.2 LA RÈGLE EST LA PLUS SIMPLE DES CINQ

`position` est **le point où va le calque, exprimé dans l'espace de sa propre
scène**. Aucune ancre n'est à retrancher — ni une, ni deux.

Vérification sur l'abscisse, qui ne dépend pas du rapport d'image :

    640 / 1280 x 1920 = 960     et le badge etait a 960 pile

Mes quatre calculs précédents partaient tous du commentaire du 2026-09-30
(« créée avec une position nulle, elle se dessine décalée de −640, −360 »).
Ce commentaire décrit **un symptôme**, pas la règle : une composition
plein écran posée en (0, 0) *paraît* décalée parce que son contenu est
centré, pas parce que le moteur retranche l'ancre.

### 34.3 ET TOUT CELA EST DÉJÀ RELATIF À LA RÉSOLUTION

Remarque de Frédéric : « le jeu est affiché en 1080p, le positionnement doit
être relatif ». **Il l'est déjà**, et la preuve est dans le fichier :
`QUEST_CARTE_X` vaut `96.0f`, et sur une capture 1080p « NO-NAME » est à
145 px — soit `145 x 1280/1920 = 96,7`. Nos coordonnées vivent dans la scène ;
c'est le moteur qui met à l'échelle.

**Le seul piège est que les deux scènes n'ont pas la même hauteur :**

    AET_N_QUE_MAIN   (la carte)   1280 x 720
    AET_C_CMN_MAIN   (le badge)   1280 x 768

L'ancre `p_dan_c` est relevée à (588, 447) dans la planche de la **carte**,
donc en espace 720. Pour la dire au badge, la largeur est la même et la
hauteur se multiplie par `768/720` :

```c
#define QUEST_SCENE_QUE_H    720.0f
#define QUEST_SCENE_CCMN_H   768.0f
#define QUEST_ANCRE_DAN_X    588.0f
#define QUEST_ANCRE_DAN_Y    447.0f

static float g_quest_badge[3] = {
    QUEST_ANCRE_DAN_X,
    QUEST_ANCRE_DAN_Y * QUEST_SCENE_CCMN_H / QUEST_SCENE_QUE_H,  /* 476.8 */
    0.0f
};
```

Écrit en **calcul** et non en nombre tout cuit : si une planche change de
résolution, la constante suit.

### 34.4 LA RECETTE COMPLÈTE POUR EMPRUNTER UN CALQUE À FINAL SHOWDOWN

Elle tient en quatre points, et c'est ce qui servira aux autres sprites :

1. **le nom doit être celui d'un calque de la composition RACINE** de la
   scène (§31.2) — un calque enfoui dans une sous-composition ne sera jamais
   trouvé, et sans erreur ;
2. **la variante se choisit par un MARQUEUR**, dont le nom est l'index
   (§31.4) — et on passe **le même marqueur au début et à la fin**, sans quoi
   on tient la trame où le calque vient de finir (§32) ;
3. **la position est un point de l'espace de la scène d'origine du calque** —
   convertir si la scène visée n'a pas la même résolution (§34.2, §34.3) ;
4. **vérifier avec l'instrument** : l'identifiant d'objet en
   `ctx + rang * 4 + 0x5C` dit si le calque existe (§33.2), et un balayage
   de positions dit où il va.

### 34.5 CE QUI RESTE INCERTAIN

L'ordonnée mesurée du badge-témoin était d'environ 497 px là où le calcul
donne 540 — **quarante-trois pixels d'écart**, lus sur une capture, donc
peut-être une erreur d'appréciation de ma part. Si le badge arrive trop haut
ou trop bas sur la fiche, c'est de cet écart qu'il s'agira, et il se corrige
d'un seul nombre : `QUEST_ANCRE_DAN_Y`.

---

## 35. LE BADGE EST À L'ÉCRAN — ET LA RECETTE TROUVE LE CADRE EN UNE COMMANDE (2026-10-19)

### 35.1 LA RÈGLE EST VÉRIFIÉE À L'ÉCRAN

Le badge « 10th kyu » s'affiche sur la fiche. Mesuré sur la capture : centre
à environ (875, 640) de 1920x1080, soit **(583, 427)** en espace 1280x720,
pour une demande à (588, 447) — **cinq pixels en x, vingt en y**, dans la
marge de lecture d'une capture. La règle du §34 est bonne.

### 35.2 CE QUE LA CAPTURE DU JEU D'ORIGINE APPREND

Frédéric a comparé avec une capture du Quest de 2007 : **la fiche a un
bandeau rouge et un fond sombre**, le nom à gauche, le badge de grade à
droite du bandeau, un portrait, et une icône hexagonale de rang dans le
corps. Chez nous il n'y avait que du texte nu sur la carte.

Et une conséquence : **le badge EST l'affichage du grade**. Dans le jeu
d'origine il n'y a pas de « 10th kyu » écrit à côté — c'est le badge qui le
porte. Notre texte fait donc double emploi.

### 35.3 LE CADRE TROUVÉ, AVEC LA RECETTE DU §34.4

Une seule commande :

    py -3 tools/ancres_ecrans.py --motif waku --motif info_win --motif p_player

    RACINE   player_info_win_1p   composition  pos (640, 360)  org (640, 360)
    RACINE   player_info_win_2p   composition  pos (640, 360)  org (640, 360)

**`player_info_win_1p` est une composition RACINE de `aet_n_qwin`** — la
planche que la greffe charge déjà (527, scène 685) — de position et origine
(640, 360), dans la **même scène 1280x720** que la carte. Aucune conversion :
on lui passe sa propre position.

Et cela corrige une note du 2026-09-30, qui disait « `waku_1p` n'est pas le
cadre de la fiche : c'est une jauge. Retiré. » C'était exact — mais le vrai
cadre existait, sous un autre nom, dans la planche déjà chargée. **La
recherche de l'époque cherchait le bon objet avec le mauvais mot.**

Posé au rang 2, priorité `QUEST_PRIO + 2` (sous le badge, qui est à +5), avec
les marqueurs `sta_s`/`sta_e` puis `neu_s`/`neu_e` comme les fenêtres.

### 35.4 CE QUI RESTE SUR LA FICHE

En comparant à la capture de 2007, il manque encore :

- **le portrait du personnage** à droite du bandeau ;
- **l'icône hexagonale de rang** dans le corps, à gauche — c'est un second
  objet, distinct du badge « 10th kyu » ;
- **le pavé « Main Costume / Type A »** et le pavé de l'argent, qui sont des
  fenêtres à part ;
- et il faudra **retirer notre texte « 10th kyu »**, que le badge rend
  redondant — mais seulement une fois le cadre vérifié à l'écran, pour ne pas
  retirer la seule lecture du grade si le badge se plaçait mal.

Tous se cherchent de la même façon : `--motif` dans les planches posées, et
on ne retient que ce qui est **à la RACINE**.

---

## 36. LE CADRE DE LA FICHE APPARAIT — ET LA BOUCLE AUTOMATIQUE EXISTE (2026-10-19)

### 36.1 CE QUI A CHANGE

Le cadre `player_info_win_1p` etait cree (l'instrument rendait l'identifiant
24) mais invisible. Deux differences avec la fenetre qui, elle, s'affiche
(`home_menu_win`) :

| | la fenetre qui marche | mon cadre |
|---|---|---|
| position | **aucune** (donc NULL : `0x180171F40` ne copie rien, le calque garde la sienne) | explicite, (640, 360) |
| priorite | `QUEST_PRIO + 6` | `QUEST_PRIO + 2` |

Les deux variantes ont ete posees **en meme temps**, la boucle automatique
rendant l'essai gratuit :

    rang 2 : position NULLE,            priorite + 6   (comme la fenetre)
    rang 3 : position (640, 360),       priorite + 7

**Et le cadre apparait** — constat de Frederic a l'ecran. **On ne sait pas
encore laquelle des deux variantes est la bonne** : j'ai tue le jeu a 33 s,
avant les captures de la passe (« LE JEU S EST FERME (code 1) » dans le
journal de `essai_menu.py`). Une seule passe automatique le dira, en retirant
l'une des deux.

### 36.2 LA BOUCLE AUTOMATIQUE : ELLE EXISTAIT DEJA

Frederic : « tu as deja fait des automatisations de ce type, trouve les bons
timings dans les notes et codes. » Il avait raison, et j'ai perdu quatre
passes a les redecouvrir de travers.

**`tools/essai_menu.py`**, ecrit le 2026-10-08, fait tout : il tue le jeu, le
relance, joue un scenario horodate, capture a quatre instants, mesure le
pourcentage de pixels non noirs, et **rend le clavier** a la fin. Ses timings
sont MESURES :

    deux START pour franchir le titre : 18 000 ms et 24 000 ms, tenus 400 ms
    navigation a partir de 30 000 ms  : un pas toutes les 1 500 ms, tenu 300 ms
    code 3 = BAS, etabli le 2026-10-08 en pressant 2, 3, 4, 5 et en relevant
    la position de la ligne rouge du curseur

    py -3 tools/essai_menu.py pas b v      un BAS, puis valider

**Un BAS tombe sur QUEST MODE** : les lignes 1 et 2 sont grisees et le
curseur les saute. La passe rend quatre captures `analysis/essai_pas_tNN.png`.

Mes propres timings etaient faux des deux cotes : j'ai presse a 10 s (le
titre en demande deux, a 18 et 24 s), puis tenu 60 ms (trop court : rien) et
650 ms (trop long : sept crans d'un coup). La valeur juste, 300 ms, etait
ecrite dans le depot depuis onze jours.

### 36.3 UN DEFAUT D'OUTIL CORRIGE EN PASSANT

`tools/capture_fenetre.py` porte en en-tete, depuis le debut, l'avertissement
qu'il photographie **la zone d'ecran** et non la fenetre, et une garde
`devant()` qui refuse si elle est recouverte. **Mais `main()` appelait
`capturer(rect, sortie)` sans lui passer `hwnd`** : la garde ne tournait
jamais. Le piege s'est reproduit -- une capture de la fenetre de Frederic au
lieu du jeu, supprimee aussitot. `main()` insiste maintenant six fois sur la
mise au premier plan, **verifie**, et refuse sans rien ecrire.

### 36.4 L'ETAT

`tools/quest_auto.py` et `tools/quest_auto.cmd` (ecrits avant de retrouver
`essai_menu.py`) restent : ils savent lancer **et** piloter en une seule
commande, et leur scenario horodate preserve les reglages `clavier` /
`manette`. Mais **c'est `essai_menu.py` qui fait foi pour les timings**.

---

## 37. LE DÉCALAGE DE TOUT L'ÉCRAN : L'ESPACE DE RÉSOLUTION (2026-10-20)

### 37.1 CE QUE FRÉDÉRIC A VU

« Tous les éléments de l'écran, dont la carte, sont trop haut, on voit une
bande en bas de l'écran qui doit correspondre au décalage. »

Et la mesure le confirme : le bas de la carte tombait à **y = 1014** sur les
1080 pixels de la capture, laissant une bande de 66 pixels. Or
720 × 1080/768 = 1012,5.

### 37.2 LA CHAÎNE, LUE DANS LE MOTEUR

Le moteur connaît **dix-sept espaces de résolution**, table `0x1803FEB20`,
vingt-huit octets par entrée (largeur, hauteur, un drapeau) :

| mode | | mode | |
|---|---|---|---|
| 3 | 1024 × 768 | **13** | **1280 × 720** |
| **9** | **1280 × 768** | 14 | 1920 × 1080 |

Chaque objet AET porte **deux** de ces numéros : un espace **source** en
`+0x40` et un espace **cible** en `+0x8C`. Avant de dessiner,
`FUN_180023650` convertit sa position de l'un à l'autre :

    FUN_18016AF60(sortie, cible = [obj+0x8C], point = [obj+0x44], source = [obj+0x40])

et cette conversion est **centrée** :

    y' = (y - h_source/2) x h_cible/h_source + h_cible/2

Les deux champs se remplissent dans `0x180027AE0`, l'entrée 1 de
`AetObj::vftable` (en `0x180348818`) :

    *(u32 *)(objet + 0x40) = descripteur[0xE];   // la SOURCE, mot 0x38 du descripteur
    *(u32 *)(objet + 0x8c) = mode_detecte;       // la CIBLE

**La cible est juste.** `FUN_180027900` balaie les dix-sept modes et compare
la largeur et la hauteur de la scène (`scène + 0x14`, `scène + 0x18`) à
chacun ; pour nos planches, 1280 × 720, il trouve le mode 13. Il ne retombe
sur 9 que s'il ne trouve rien.

**La source était fausse**, et c'est une seule instruction. Dans
`FUN_180029000`, le constructeur du descripteur de calque :

    param_1[0xe] = 9;        // descripteur + 0x38 : 1280 x 768, EN DUR

Le moteur prenait donc nos planches, dessinées pour 720, pour du 768, et les
rétrécissait : un `y` de 720 ressortait à

    (720 - 384) x 0,9375 + 360 = 675   ->   675 x 1,5 = 1012 pixels

ce qui est, au pixel près, la mesure. L'abscisse, elle, était intacte, les
deux modes faisant 1280 de large — **c'est pourquoi le cadre de la fiche
tombait exactement juste en x et faux en y**, ce qui avait égaré le relevé.

### 37.3 LA CORRECTION

`0x180171F40` construit le descripteur sur sa pile et ne touche jamais
`+0x38`. La greffe refait donc elle-même ces trois gestes
(`quest_creer_espace` dans `tools/quest_runtime.c`) :

    0x029000   construire le descripteur
    0x029A90   créer l'objet, qui rend son identifiant
    0x029140   détruire le descripteur

en écrivant un champ de plus. Les offsets viennent de la décompilation de
`0x180171F40` :

    +0x00 u32  la scène              +0x34 u32  la priorité
    +0x08 ptr  le nom du calque      +0x38 u32  L'ESPACE SOURCE
    +0x10 ptr  le marqueur de début  +0x40 3xf  la position
    +0x18 ptr  le marqueur de fin    +0x28 u32  les drapeaux

L'espace posé est **celui de la planche d'où vient le calque** : 13 pour
`aet_n_que`, `aet_n_qwin`, `aet_q_cmn` et `aet_q_cstm`, qui déclarent toutes
1280 × 720 ; **9 pour `aet_c_cmn`**, la planche commune de 2007, qui déclare
1280 × 768. Source égale cible, la conversion devient l'identité.

Résultat mesuré : la bande du bas tombe de **66 pixels à 8**.

### 37.4 LE TEXTE A SON ESPACE, LUI AUSSI

Notre texte ne passe pas par un objet AET. Mais `quest_ecrire_boite` appelle

    0x18019B800(descripteur, {x, y, largeur, hauteur}, 9)

et cette fonction range son troisième argument dans `descripteur + 0x2C` :
c'est le même numéro de mode. Le texte restait donc en 768 pendant que les
calques passaient en 720.

Le résidu s'est mesuré à **66 pixels trop haut**, et c'est exactement la
branche de recadrage de `FUN_18016AF60` : quand la source vaut 9 ou 3 et la
cible 13 à 16,

    y -= (hauteur_source - 720)

soit 48 unités, soit 48 × 1080/768 = **67,5 pixels**. En posant 13 à la place
du 9, la source n'est plus ni 9 ni 3 : le recadrage ne s'applique plus, et
les ancres relevées dans les planches se disent telles quelles. Les deux
lignes d'information tombent alors à cinq pixels de leur ancre — le creux
au-dessus des majuscules.

### 37.5 UN TEST QUI N'A RIEN PROUVÉ, ET POURQUOI

Avant de lire le code, j'avais essayé de **déclarer 768** dans la résolution
des scènes de `aet_n_que` et `aet_n_qwin`. Les captures étaient identiques au
pixel. C'était cohérent et sans valeur : le comportement observé **était
déjà** celui du mode 9 par défaut, donc écrire 768 ne changeait rien. Un
essai qui ne distingue pas deux hypothèses ne mesure rien.

### 37.6 CE QUE LA PLANCHE DONNE, ET CE QU'IL NE FAUT PLUS CHERCHER À L'ÉCRAN

`player_info_win_1p` **est une composition** : elle porte ses sept repères,
dont le suffixe donne l'alignement et dont la taille (24 × 24) donne la
taille du texte.

| ancre | position (1280 × 720) | |
|---|---|---|
| `p_ring_name_lt` | (275, 435) | le nom |
| `p_player_info_01_lt` | (322, 472) | W / L |
| `p_player_info_02_lt` | (322, 502) | Win ratio |
| `p_dan_point_c` | (600, 448) | le badge, **centré** |
| `p_gold_win_172x50_lt` | (805, 489) | l'argent, fenêtre 172 × 50 |
| `p_gen_plate_c` | (288, 499) | la plaque, 56 × 62 |
| `p_chara_face_c` | (727, 479) | le portrait, 104 × 106 |

`analysis/quest/ancres_qwin.txt` les listait **depuis le 2026-10-19**.
`tools/arbre_aet.py`, écrit ce jour, déplie n'importe quelle composition et
les redonne.

**Et `aet_n_que`, la planche de la carte, a ses PROPRES repères à la racine** —
`p_name_lt` (279, 435), `p_txt_01_lt` (323, 473), `p_txt_02_lt` (323, 499),
`p_gen_c` (288, 499), `p_dan_c` (588, 447) et `p_emb_lt` (610, 476). C'est de
là que venait le « (588, 447) » du code, qui n'était donc pas une erreur mais
un relevé fait sur l'autre planche.

### 37.7 CE QUI EST POSÉ, ET CE QUI MANQUE ENCORE

Posés et vérifiés à l'écran : le cadre, le nom, les deux lignes, l'argent, le
badge de grade et **le portrait** (`chara_face_player`, marqueurs par code de
personnage — `aki`, `pai`, `lau`… et `<code>_end` seize trames plus loin ;
**dix-sept portraits, donc ni Jean ni Taka-Arashi**).

Trois mesures négatives, qui ferment des pistes :

1. **`gen_base`, la plaque ronde**, est bien une composition **racine** de
   `aet_c_cmn` — six billes `c_cmn_gen_ball.pic` en cercle, sept variantes
   (« 0 » à « 6 »), le compte venant de huit bits en `profil + 0x130` chez
   2007. Mais dans la planche **servie** (celle du `.par`), la composition
   est **VIDE** : elle existe, l'objet se crée, et rien ne se dessine. Il
   faut la réimporter avec son contenu. Et la variante « 0 » ne montre
   **aucune** bille.
2. **Les icônes de costume, le cadre de la monnaie et les fenêtres du bas ne
   sont dans AUCUNE de ces compositions.** La planche de 2007 et celle de
   Final Showdown donnent, pour `player_info_win_1p`, **exactement le même
   arbre** — sept repères et sept images de cadre.
3. **Le code de 2007 ne les pose pas par leur nom.** L'inventaire complet des
   noms de calque cités par les 623 fonctions décompilées du mode ne contient
   ni `gold_win`, ni `cos_icon`, ni `waku_1p` ; `FUN_8230AC50` ne pose que
   **trois** objets sur la fiche — `chara_face` (octet `+0xF8` du profil, le
   personnage), `gen_base` (le compte de bits) et `dan_icon1p` (octet `+0xF9`,
   le grade).

**La piste qui reste** est la table des fenêtres : `FUN_822E39C0` pose une
fenêtre **par INDEX**, lu dans le champ `+4` de l'objet fenêtre, et va
chercher sa planche et son nom dans `0x82085700` (59 entrées en 2007, 91 en
`0x18052E680` côté FS, lues par `0x1801BC580`). Une fenêtre posée ainsi
n'apparaît nulle part sous son nom dans le code : **il faut chercher qui
écrit ce champ `+4`**, et avec quel index, dans les tâches du Quest.

### 37.8 LA CIBLE 9 : ON NE L'A PAS MESURÉE, ON L'A SUPPRIMÉE

Frédéric, après trois replacements successifs du badge : « tu fais
systématiquement des erreurs sur le positionnement des objets ». Il avait
raison, et la cause était de méthode : je calais chaque objet un par un, au
lieu d'établir **une fois** la loi qui mène d'une ancre de planche à un
pixel d'écran.

Il y en avait deux, parce que la **cible** d'un objet est déduite de la
planche d'où il vient :

| objets | cible | loi |
|---|---|---|
| planches en 1280 × 720 (`que`, `qwin`, `qcmn`, `qcstm`) | 13 | `y_écran = 1,5 × ancre`, vérifié : le nom tombe à 670 pour 670 attendu |
| planches en 1280 × 768 (le badge, la plaque) | 9 | **jamais établie** |

Deux tentatives de la mesurer ont échoué, et les deux échecs sont
instructifs :

1. un témoin posé **deux fois** à deux hauteurs a fait **planter le jeu**
   (violation d'accès) — retiré aussitôt ;
2. la mesure de repli sur la plaque était polluée : le panneau de la fiche
   est gris comme elle. La pente obtenue, 1,11, n'a aucun sens physique, et
   poser un objet dessus aurait été une quatrième erreur.

**La sortie n'a pas été de mesurer mieux, mais de supprimer le cas
particulier.** La planche commune de 2007, `aet_qc_cmn`, est la NÔTRE : on
lui a déclaré **1280 × 720** (le champ `scène + 0x18`, que `FUN_180027900`
lit pour choisir le mode). Le moteur lui donne alors la cible 13, comme à
toutes les autres.

Et comme cette planche porte **aussi** le badge, sous son nom d'origine
`dan_icon1p` — mêmes tailles d'image que la version `_e` de Final Showdown,
88 × 30 pour le 10e kyu, et le libellé est bien en anglais — le badge y a été
déplacé. Plus un seul objet du Quest ne vit en cible 9 :

* la plaque `gen_base` tombe sur `p_gen_plate_c` (288, 499) **sans
  conversion** ;
* le badge tombe sur `p_dan_point_c` (600, 448) **sans conversion**, dans le
  bandeau rouge, à la hauteur du nom.

Le champ `espace` ajouté à `quest_calque` reste : il permet de forcer la
source d'un calque, et il documente le mécanisme. Mais plus aucun calque ne
s'en sert — **c'est le signe que le problème a été retiré, pas contourné.**

Note au passage : le test qui a échoué au §37.5 — déclarer 768 sur des
planches de 720 — est le symétrique exact de celui qui réussit ici. Il n'avait
rien changé parce que le résultat était 9 des deux côtés ; celui-ci change
tout parce qu'il fait passer la cible de 9 à 13.

### 37.9 LES PAVÉS « MAIN COSTUME », LE CADRE DE LA MONNAIE, LES DEUX FENÊTRES DU BAS

La capture de 2007 que Frédéric a fournie le 2026-10-20 les montre enfin :

* deux pavés à **bandeau doré**, superposés, à droite de la fiche —
  « Main Costume / Type A », et un second à demi caché dessous ;
* sous eux, un **cadre gris** qui contient « 50000G » ;
* en bas de l'écran, une **grande fenêtre** portant le texte du lieu survolé
  (« Home: Adjust various settings… ») et, sous elle, **la barre des
  commandes** (« START:Home Menu  A:Enter »).

Mesurés sur la capture, en ramenant à 1280 × 720 : les pavés de costume
occupent x ≈ 800 à 975, y ≈ 427 à 477 ; le cadre de la monnaie, y ≈ 503 à
546 — c'est-à-dire exactement l'ancre `p_gold_win_172x50_lt` **(805, 489)**,
dont le nom annonce la taille, 172 × 50. L'ancre existe donc bien pour la
monnaie ; **le cadre, lui, n'est dans aucune composition de la fiche.**

Ce qui est établi, et ce qui ferme des portes :

1. `player_info_win_1p` a le **même arbre** dans la planche de 2007 et dans
   celle de Final Showdown : sept repères, sept images de cadre. Rien de
   plus.
2. L'inventaire des noms de calque cités par les **623 fonctions**
   décompilées du Quest de 2007 ne contient ni `gold_win`, ni `cos_icon`.
3. La **table des fenêtres** de 2007 (59 entrées, `0x82085700`) ne contient
   qu'une entrée propre au Quest, `que_info_win` — une grande fenêtre
   centrée à quatre lignes, pas un pavé. Celle de Final Showdown (91
   entrées, `0x18052E680`) n'a rien non plus.
4. Son poseur, `FUN_822E39C0`, n'est appelé que depuis le code générique de
   l'interface (0x8214…, 0x822D…), **jamais depuis le Quest** (0x8230…).

**La piste ouverte, et elle est nommée.** Dans le fichier de textes anglais
de 2007 (`lang/en/string_array.bin`) :

    « Main Costume »  libelle 596
    « Sub Costume »   libelle 597
    « Type A »        libelle 809

Aucun des trois n'est dans notre import de 492 textes. Et le 596 n'est
construit qu'en **deux** endroits de l'image : `0x82295514`, dans
`FUN_822954B0` — un constructeur d'objet d'interface qui résout le texte par
`FUN_82142EE0(0x254)` puis le confie à `FUN_822953F8` — et `0x824D3FC4`, qui
est une table de données. `FUN_822954B0` n'a qu'un appelant,
`FUN_821DF6E0` (depuis `0x821DF768`), lui-même appelé depuis `0x821DF7C0`.

Autrement dit : **ces pavés ne sont pas des calques AET nommés, ce sont des
objets d'interface génériques**, construits par une chaîne qui part du
système de tenue et non du mode Quest. Pour les porter il faudra remonter
cette chaîne jusqu'au point où le Quest l'instancie — c'est là, et seulement
là, que la position des pavés sera écrite.

Le texte de la fenêtre du bas, lui, est **déjà importé** : « Home: Adjust
various settings. (You can also open the Home Menu by pressing START.) » est
le libellé **128** de 2007, notre 23143.

### 37.10 LES PAVÉS SONT DES IMAGES — ET JE NE LES AI PAS TROUVÉES

**La chaîne remonte jusqu'au Quest, et elle s'arrête sur un interrupteur.**
`FUN_822954B0` (qui résout le libellé 596) ← `FUN_821DF6E0` ← `FUN_821DF868`,
et ce dernier est appelé depuis le Quest, en `FUN_823002D8` — mais avec un
**booléen** :

    cVar1 = FUN_822D0C80(0);
    if (cVar1 == '\0') FUN_821DF868(1); else FUN_821DF868(0);

Ce n'est donc pas la création d'un pavé : le mode Quest **allume** un
composant d'interface global, qui porte son rendu et ses textes. Final
Showdown n'a pas ce composant.

**Correction de Frédéric, 2026-10-20 : « Main Costume », « Type A » n'est pas
du texte mais une image.** C'est donc un sprite qu'il faut trouver, pas un
libellé. Quatre balayages du média de 2007 n'ont rien donné :

1. les compositions **racine** des vingt-sept planches, sur les noms
   contenant « gold », « costume » ou commençant par « cos_ » : seulement des
   curseurs (`cos_main_cursor`), des plaques de rang en ligne (`aet_c_plt` :
   `rank_gold`, `taikai_gold`) et des boutons de boutique (`aet_t_item`) ;
2. les **noms de sprites** de tous les jeux de sprites : `COS_MAIN_ICON` et
   `COS_SUB_ICON` existent, dans `spr_n_cstm` — la planche que nous avons
   déjà importée (`qcstm`) — mais ils font **76 × 30**, c'est l'étiquette de
   l'écran Customize, pas un pavé ; `GOLD` (66 × 72), `GOLD_MOJI` (82 × 42),
   `GOLD_ICON` (166 × 182) ne conviennent pas davantage ;
3. les **surfaces de 160 à 180 de large sur 38 à 60 de haut** (la taille du
   pavé entier, mesurée sur la capture) : les seules de 172 × 50 sont les
   REPÈRES `p_gold_win_172x50_lt` eux-mêmes, qui n'ont pas de source ;
4. les **surfaces de 150 à 180 sur 18 à 32** (le bandeau seul) : rien de
   pertinent.

L'image existe donc, mais sous un nom que je n'ai pas prévu, dans une
planche que le média extrait ne contient pas, ou dans une autre version du
jeu que celle de la capture. **C'est la question à trancher avant de
continuer.**

**Ce qui a été posé en attendant**, aux positions mesurées sur la capture et
clairement comme pis-aller — du texte là où 2007 met une image :

| | position (1280 × 720) | |
|---|---|---|
| « Main Costume » | centré en x 891, y 429, taille 18 | libellé 596, repli en clair |
| « Type A » | centré en x 891, y 446, taille 24 | libellé 809, repli en clair |
| l'argent | **aligné à droite** en x 967, y 505 | c'était une vraie erreur : il était posé en haut à gauche de sa boîte de 172 × 50 |

Les trois libellés de 2007 — « Main Costume » 596, « Sub Costume » 597,
« Type A » 809, relevés dans `lang/en/string_array.bin` — **ne sont pas dans
notre import de 492 textes** : la greffe les demande et retombe sur la chaîne
en clair, comme pour « W:%6d ».

Les deux fenêtres du bas restent entières à faire ; leur texte, lui, est déjà
importé (libellé 128 → 23143).

### 37.11 COMMENT 2007 PLACE SES TEXTES : UNE ANCRE PAR SON NOM

La capture vient d'une vidéo de la version Xbox 360 — donc du média que nous
avons. L'image des pavés **doit** y être. En la cherchant, on a trouvé mieux :
**l'API que 2007 emploie pour placer la carte du joueur.**

`FUN_82308C90` — déjà connue du dossier pour le calcul du Win ratio — dessine
toute la carte, et chaque élément passe par :

    FUN_82308B78(..., 0x423, ..., "<nom de l ancre>")   -> rend la position
    FUN_8223BEB8(x, y)                                   -> pose le curseur
    FUN_8223C048(couleur)
    FUN_8223FE30(format, args...)                        -> ecrit

`0x423` = **1059**, la scène ; le dernier argument est le **nom de l'ancre,
en clair dans l'exécutable**. Les noms employés, lus à leurs adresses :

    0x8208BE7C  p_ring_name_lt          0x8208BE08  p_gen_plate_c
    0x8208BE68  p_player_info_01_lt     0x8208DCCC  p_gold_win_172x50_lt
    0x8208BE54  p_player_info_02_lt     0x8208BE2C  p_gold_win_lt  (2P)

Ce sont **exactement** les sept repères que `tools/arbre_aet.py` déplie dans
`player_info_win_1p`, et exactement ceux que la greffe utilise. La méthode est
donc confirmée par le code, et non plus seulement par la planche.

**ET L'ARGENT N'A PAS DE FENÊTRE.** `FUN_82308C90` résout
`p_gold_win_172x50_lt`, demande le libellé **999** (`%dG`) et **écrit le
texte**, un point c'est tout. Le cadre gris visible autour de « 50000G » sur
la capture ne vient donc pas du mode Quest.

**Où sont les pavés.** `FUN_821DF6E0` construit un objet qui contient **DEUX**
sous-objets identiques — la boucle appelle `FUN_821DF480` deux fois, à
0x14A mots d'écart : les pavés *Main* et *Sub*. Le mode Quest ne fait que
l'allumer, par `FUN_821DF868(drapeau)` depuis `FUN_823002D8`. Les noms des
images sont plus bas dans la chaîne de constructeurs
(`FUN_821DDFD8`, `FUN_821DE190`, `FUN_821DEB08`), qui reste à descendre.

**Ce qui est donc acquis** : le bloc de droite — deux pavés de costume et le
cadre de l'argent — est **un composant d'interface à part**, pas un calque de
la fiche ; il occupe la colonne x 805..977 que l'ancre de l'argent annonce ;
et le texte de l'argent, lui, est bien du Quest, posé à cette ancre.

### 37.12 QUATRE PISTES ÉCARTÉES, ET CELLE QUI RESTE

Le bloc de droite a été cherché par cinq chemins. Quatre sont **fermés**, et
il faut le dire aussi nettement que les réussites — sinon la prochaine séance
les refera.

| piste | ce qu'elle a rendu |
|---|---|
| `FUN_823092A8`, le dessin complet de la carte | calque 2, **espace 9**, puis `FUN_82308C90` (les textes de la fiche) et `FUN_82308838`. **Rien d'autre.** |
| `FUN_82308838` | les **noms de tournoi** : elle boucle sur deux entrées et écrit le libellé **634**, « Tournament ». Pas un pavé. |
| `FUN_821DF868`, l'« interrupteur » du §37.10 | **fausse piste** : le composant qu'il allume résout le libellé **464**, « Quick Match ». C'est le **jeu en ligne**. |
| `p_cos_icon_1p_lt` / `_2p_lt` | les ancres existent, et `FUN_822CD5A8` les emploie — mais elles vivent dans **`aet_c_loadcmn`**, la planche de l'**écran de chargement** (ses voisines s'appellent `matching_1p`, `pr_personal_pla_1p_match`). Ce sont les icônes de tenue d'avant-combat, pas celles de la carte. |

Et deux faits acquis, qui valent mieux qu'une piste :

* **`FUN_82308B78(..., 0x423, ..., "<nom d'ancre>")` est l'API par laquelle
  2007 place CHAQUE texte de la carte** — la méthode des ancres est donc
  confirmée par le code ;
* **l'argent n'a pas de fenêtre de fond** : 2007 résout
  `p_gold_win_172x50_lt`, demande le libellé 999 (`%dG`) et écrit, point.

**La voie qui reste, et elle n'a pas été essayée** : chercher l'image non par
son NOM mais par son CONTENU — extraire les textures des jeux de sprites de
2007 et y repérer celle qui porte les mots « Main Costume ». C'est lourd, mais
c'est la seule qui ne dépende pas de deviner un nom. À défaut, vérifier que
la vidéo d'où vient la capture montre bien la même révision du jeu que notre
média.

### 37.13 L'IMAGE DES PAVÉS, TROUVÉE — PAR SON CONTENU, PAS PAR SON NOM

La méthode du §37.12 a payé : **sortir les textures et les regarder**, au lieu
de deviner un nom.

    py -3 <scratchpad>/sortir_textures_2007.py spr_n_qwin.farc

réutilise `textures_hd.membres` + `lire_txp` + `txp.image` sur le média de
2007 et écrit les PNG. Vingt-huit textures pour `spr_n_qwin`, et la
**deuxième** (`spr_n_qwin__tex02`, 512 x 1024) porte les pavés, en clair :

    メインコスチューム  A / B / C / D タイプ     en DORE   (Main Costume)
    サブコスチューム    A / B / D タイプ        en ARGENTE (Sub Costume)

C'est bien une image, comme Frédéric le disait, et elle est dans une planche
que **nous avons déjà importée** (`qwin`, planche 527, sprites 624).

**Les noms des sprites** : `COL_ICO_MAIN_1` à `_4` et `COL_ICO_SUB_1` à `_4`
— huit pavés, un par type de tenue. Aucune recherche par « costume » ou
« cos » ne pouvait les trouver : ils s'appellent **COL**.

**Comment 2007 les place.** `FUN_8230A338`, dans le Quest, monte le
descripteur :

    nom du calque   « col_iconmove »        scene 0x423 = 1059
    ancre du texte  « p_col_txt_main_c »    drapeaux 0x20000, priorite 6
                                            espace 9

et ses appelants (`FUN_8230A470`, `0x82312ADC`) lui passent « main » et
« sub » — ce sont des **suffixes**, pas des coordonnées. `col_iconmove` est
une composition RACINE de `aet_n_qwin`, à (1335, 287), qui ne contient que
les deux ancres `p_col_txt_main_c` et `p_col_txt_sub_c` : c'est
l'**animation de bascule** entre tenue principale et secondaire (« icon
move »), douze trames.

**Ce qui bloque encore, et c'est précis** : `aet.py --sprite COL_ICO` ne
trouve **aucun calque** qui dessine ces sprites, ni dans la planche de 2007
ni dans celle de Final Showdown. Les pavés sont donc **dessinés directement
en sprite par le code**, à la position que l'ancre donne — pas posés comme
calque AET. La greffe, elle, ne sait aujourd'hui que poser des calques et
écrire du texte.

**La prochaine étape est donc nommée** : donner à la greffe le dessin d'un
sprite par son identifiant, puis poser `COL_ICO_MAIN_<type>` à l'ancre
`p_col_txt_main_c` de `col_iconmove`. Tout le reste est déjà en place.

### 37.14 LE DESSIN D'UN SPRITE : L'API EST TROUVÉE, LA COMMANDE RESTE À LIRE

Le dossier avait toujours **contourné** le dessin de sprite — « on les monte
comme tous nos autres calques, sans avoir à écrire le dessin d'un sprite »
(§ sur `qdan`). Pour les pavés, ce contournement n'est plus possible : aucun
calque AET ne dessine `COL_ICO_MAIN_*`.

**La chaîne du rendu 2D de Final Showdown, remontée :**

    0x18018CA20   depose une commande dans le contexte 2D
                  (deja connue : elle laisse TOMBER la commande, sans un mot,
                  quand le jeu de sprites n est pas enregistre)
       <- 0x180187AF0(descripteur)        depose une commande deja construite
       <- 0x180187B10(...)                CONSTRUIT et depose

**La signature réelle de `0x180187B10`**, lue au désassembleur parce que
Ghidra avait perdu les arguments flottants (ils arrivent en ZMM0/ZMM1) :

    vmovaps xmm9, xmm3 ; xmm7, xmm2 ; xmm8, xmm1 ; xmm6, xmm0
    ...
    vsubss xmm1, xmm7, xmm6      ->  x1 - x0
    vsubss xmm0, xmm9, xmm8      ->  y1 - y0
    vunpcklps xmm5, xmm6, xmm8   ->  (x0, y0)
    mov dword ptr [rsp+0x30], 2  ->  type de commande = 2

soit

    void dessiner(float x0, float y0, float x1, float y1,
                  u32 a5, u32 a6, u32 a7, u32 a8);

Les quatre flottants sont un **rectangle** (coin haut-gauche, coin
bas-droit) : `0x18018E7C0` reçoit la taille, et `(x0, y0)` va en `+0x64` du
descripteur. Les quatre entiers viennent de la pile ([rsp+0x190] à
[rsp+0x1A8] après `sub rsp, 0x168`, c'est-à-dire les arguments 5 à 8) : a5 est
écrit **deux fois** (`+0x50` et `+0x54`), a6 en `+0x4C`, a7 en `+0x30` du
corps, a8 en `+0x48`.

**CE QUI MANQUE, ET C'EST PRÉCIS** : aucun de ces arguments ne s'annonce
comme l'**identifiant du sprite**. Il est l'un des quatre entiers, ou il se
pose dans le descripteur avant l'appel. Le trancher demande de lire la
structure de commande de `0x18018CA20` — un vrai chantier, pas quinze lignes.

**Pourquoi on s'arrête là plutôt que d'essayer.** Un appel à une fonction
dont on devine la signature se paie comptant : le témoin posé le même jour
pour mesurer la cible 9 a fait **planter le jeu** (violation d'accès). Poser
un descripteur à moitié compris ferait pire. La prochaine séance a tout ce
qu'il faut pour finir : la chaîne, la signature, et l'ancre
`p_col_txt_main_c` où poser le résultat.

### 37.15 LA COMMANDE 2D, CHAMP PAR CHAMP — ET L'IDENTIFIANT DE SPRITE

`0x18018CA20(contexte, commande)` est le point où tout le 2D de Final
Showdown se dépose. Sa commande se lit ainsi :

| champ | rôle | d'où on le sait |
|---|---|---|
| `+0x00` | **type** de commande ; `2` pour un quad | `mov dword [rsp+0x30], 2` dans `0x180187B10` |
| `+0x04` | **IDENTIFIANT DU SPRITE** | voir ci-dessous |
| `+0x08` | argument 7 de `0x180187B10` | `mov [rsp+0x38], eax` |
| `+0x14` | le **calque** ; `-1` = celui du contexte | `if (desc+0x14 == -1) iVar18 = ctx[0x105]` |
| `+0x18` | rang dans le compartiment | indexe le contexte |
| `+0x1C` | compartiment | indexe le contexte |
| `+0x20`, `+0x24` | argument 5, **écrit deux fois** | `mov [rsp+0x50]` et `[rsp+0x54]` |
| `+0x34`, `+0x38` | la **position** (x, y) | `vmovsd [rsp+0x64], xmm5` |
| `+0x3C` | mis à zéro | |
| `+0xA0` | pointeur de ressource, employé quand il n'y a PAS de sprite | |

L'adressage du compartiment est celui que la greffe connaît déjà :

    contexte[ ((desc+0x18 + calque) * 0x20 + (desc+0x1C) + 1) * 2 ]

**L'identifiant de sprite est en `+0x04`, et sa lecture est sans ambiguïté :**

    if (*(uint *)(desc + 4) == 0xffffffff)  -> pas de sprite : un quad plein
    else  uVar6 = *(uint *)(desc + 4) >> 0x10 & 0xfff;   -> le JEU de sprites
                                                            (recherche dans l arbre)

**Les bits 16 à 27 donnent le jeu de sprites**, les bits bas l'indice dedans.
Et c'est exactement ce que le dépôt note depuis le 2026-10-11 dans
`quest_diagnostic_police` : « l'identifiant de sprite de la police est le
premier mot du descripteur de police, et son jeu en est les bits 16..27 ».
La greffe connaissait donc déjà ce format, sans savoir qu'il servait aussi
aux sprites.

**Ce qu'il reste à faire pour poser les pavés**, et c'est désormais mécanique :

1. un tampon de descripteur, initialisé par `0x180189880` ;
2. `+0x00 = 2`, `+0x04 = <jeu 624 << 16 | indice de COL_ICO_MAIN_n>` ;
3. la position en `+0x34` / `+0x38`, la taille par `0x18018E7C0(desc, (w, h))` ;
4. le compartiment en `+0x18` / `+0x1C`, comme le fait déjà
   `quest_ecrire_boite` pour le texte ;
5. `0x180187AF0(desc)` — qui ajoute le contexte et appelle `0x18018CA20`.

Reste à relever l'**indice** de `COL_ICO_MAIN_1..4` dans le jeu 624 : il se
lit dans `spr_db.bin` (`bases_2d.py` l'a renuméroté à l'import), et la ligne
de la base donne directement `(rang de la planche << 16) | rang`.

### 37.16 LE DESSIN DE SPRITE : ÉCRIT, SUSPENDU, ET CE QU'IL RESTE À TROUVER

**Les pavés sont déjà dans Final Showdown, en anglais.** `spr_db.bin` les
donne, et c'est la même surprise qu'au §29 pour le badge de grade :

    SPR_C_CMN_COL_ICO_MAIN_1_E .. _4_E   info 0x1000F 0x10011 0x10013 0x10015
    SPR_C_CMN_COL_ICO_SUB_1_E  .. _2_E   info 0x1001B 0x1001D

`info` est **exactement** le format attendu en `commande + 0x04` :
`jeu << 16 | rang`. Rien à importer, rien à renuméroter.

`quest_sprite(id, x, y, w, h, couleur)` est écrite dans
`tools/quest_runtime.c`, avec les mêmes gestes que `quest_ecrire_boite`
autour (le calque du contexte 2D monte à 2 et redescend). **Elle fait planter
le jeu** — violation d'accès `0xC0000005` à la première trame de l'écran
Quest. Deux tentatives, deux plantages ; l'appel est donc **suspendu sous
`#if 0`**, et le texte provisoire reste en place.

**Ce que le premier échec a appris**, et c'est acquis : `0x18018E7C0` reçoit
la taille **en entier, dans RDX** — `vunpcklps xmm1, xmm1, xmm0` empaquette
les deux flottants, puis `vmovq rdx, xmm1`. Déclarer un `double` les enverrait
dans xmm1. Le typedef est corrigé.

**Mais cela n'a pas suffi.** Les suspects qui restent, dans l'ordre :

1. **`0x180189880` n'est peut-être pas le constructeur de CETTE commande.**
   `FUN_180020CC0`, le constructeur d'`AetObj`, l'appelle aussi — sur
   `param_1 + 0x14`, une sous-structure. C'est donc un constructeur
   générique, et la commande 2D attend peut-être plus que ce qu'il pose.
2. **Le tampon fait 0x140 octets** ; la commande lit `+0xA0`, mais sa taille
   réelle n'a pas été mesurée.
3. **`0x180187AF0` passe `DAT_180719900`**, le gestionnaire de sprites, comme
   contexte — il doit être prêt ; la greffe charge bien `QUEST_SPR_CCMN`,
   mais rien ne dit que c'est le même objet.

**La mesure qui trancherait**, et qui n'a pas été faite : poser une sonde
dans `0x180187B10` — la seule construction de commande dont on soit sûr —
pour **relever le descripteur complet, octet par octet, tel que le jeu le
remplit**. Le comparer au nôtre dira en une fois ce qui manque. C'est la même
méthode que l'instrument du §31 (lire l'identifiant d'objet après `creer2`),
qui avait tranché six hypothèses d'un coup.

**L'état du dépôt** : `quest_sprite` est en place et compile, l'appel est
sous `#if 0`, le jeu tourne, et une passe de contrôle le confirme.

### 37.17 LE TÉMOIN QUI DÉDOUANE LE DESCRIPTEUR

Plutôt que de corriger notre construction à l'aveugle, on a appelé **la
fonction qui la fait**, `0x180187B10`, avec sa vraie signature — quatre
flottants en xmm0..xmm3 pour le rectangle, quatre entiers par la pile. Elle
ne pose pas `+0x04` : elle dessine donc un quad plein, sans sprite.

**Elle plante exactement comme le nôtre** — `0xC0000005`, à la première trame
de l'écran Quest. Le diagnostic se retourne : **ce n'est pas la construction
du descripteur.** Les soupçons du §37.16 sur `0x180189880` et sur la taille du
tampon tombent, puisque la fonction du jeu fait tout sur sa propre pile.

Un second essai a corrigé une vraie **erreur de lecture**, sans rien changer
au plantage. Dans

    contexte[ ((desc+0x18 + calque) * 0x20 + (desc+0x1C) + 1) * 2 ]

`+0x18` **s'ajoute au calque** avant la multiplication par 0x20 — il doit donc
rester petit — tandis que `+0x1C` est le **rang** dans le calque (0..31). Nous
passions `QUEST_ORDRE` (31) comme calque : l'index partait à plus de deux
mille entrées.

Et une mesure, posée parce qu'elle ne coûtait rien : à la trame où nous
dessinons,

    [quest] gestionnaire de sprites 0x719900   2677862795056   (0x26F...)
    [quest] base des sprites        0x719908   2677748404832

**ni l'un ni l'autre n'est nul.** Le gestionnaire est prêt. La première des
trois hypothèses du §37.16 est donc écartée elle aussi.

**Ce qui reste**, et c'est maintenant la seule piste : le dessin de sprite
exige un **état de rendu** que seule la boucle de Final Showdown établit. Le
texte, lui, ne passe pas par ce chemin — il emploie le descripteur que
`QUEST_RVA_DESC_NEUF` fournit, et le calque 2D monté à 2. Il faudra donc
regarder **d'où** Final Showdown appelle `0x180187AF0` dans une trame
ordinaire, et à quel moment de la trame — c'est-à-dire remonter ses
appelants, comme on l'a fait pour `0x82308C90` côté 2007.

**L'état du dépôt** : les deux témoins sont sous `#if 0`
(`QUEST_TEMOIN_QUAD` et l'appel à `quest_sprite`), `quest_sprite` reste
écrite et compile, le texte provisoire est en place, et une passe de contrôle
confirme que le jeu tourne.

### 37.18 LE SEUL APPELANT, ET LE CHAMP QUI MANQUAIT

`0x180187AF0` n'a **qu'un seul appelant** dans tout le moteur :
`FUN_180108320` — le dessin d'un **glyphe de police**. Il lit
`DAT_18070FB38` (la police, ses largeurs de caractères, son échelle) et
construit la commande ainsi :

    FUN_180189880(desc);                     l init
    ... une dizaine de champs poses a la main :
        +drapeaux (|= 2), echelles, teintes, la texture de la police
    FUN_18018E7C0(desc, taille);             la TAILLE
    FUN_18018E780(desc, u, v, w, h);         les COORDONNEES DE TEXTURE
    FUN_180187AF0(desc);                     le depot

**`0x18018E780` est l'appel qui manquait.** Nous posions six champs ; il en
faut une quinzaine, dont les UV — et les UV supposent d'avoir **résolu le
sprite** au préalable, c'est-à-dire de connaître son rectangle dans sa
texture.

Et cela explique du même coup le plantage du témoin du §37.17 :
`0x180187B10` **ne pose pas `+0x04`**, donc `0x18018CA20` prend sa branche
`0xFFFFFFFF` — celle qui déréférence **`+0xA0`**, un pointeur de ressource que
personne n'avait rempli. La fonction du jeu n'est donc utilisable que dans un
contexte où ce pointeur existe déjà ; appelée nue, elle plante aussi
sûrement que la nôtre.

**La voie propre est désormais claire, et elle est plus courte qu'il n'y
paraît** : poser `+0x04` fait prendre à `0x18018CA20` l'AUTRE branche, celle
qui cherche le sprite dans l'arbre par `(id >> 16) & 0xFFF` et en tire
lui-même la texture et les UV. C'est donc le bon chemin — mais il faut alors
que **tous les autres champs** que `FUN_180108320` remplit soient valides, et
`0x180189880` seul ne suffit pas.

**La mesure qui finira le travail** : relever le descripteur complet que
`FUN_180108320` passe à `0x180187AF0`, octet par octet — par une sonde posée
sur cette fonction, ou en lisant ses quinze écritures dans la décompilation —
puis le reproduire en ne changeant que `+0x04`, la position et la taille.
C'est mécanique, mais ce n'est pas deux lignes.

### 37.19 LE DESCRIPTEUR COMPLET — LE PLANTAGE CESSE

Relevé dans `FUN_180108320`, le dessin d'un glyphe, en comptant les offsets
depuis `local_168` :

| offset | ce que le jeu y met | nous |
|---|---|---|
| `+0x04` | l'identifiant du sprite (pris dans la police) | posé |
| `+0x08` | `police[0x0E]` | **manquait** |
| `+0x0C` | drapeaux, `\|= 2` | **manquait** |
| `+0x10` | `(police[0x10] >> 3) & 2` | **manquait** |
| `+0x14` | le calque ; `-1` = celui du contexte | posé |
| `+0x18` | s'ajoute au calque, puis x 0x20 | **inversé** |
| `+0x1C` | le rang, 0..31 | **inversé** |
| `+0x20` / `+0x24` | la couleur, **deux fois** | posé |
| `+0x34` / `+0x38` | la position | posé |
| `+0x40` / `+0x44` | **l'échelle** | **manquait** |
| `+0x58` | `police[0x11]` | **manquait** |
| `+0xAC` | **`0x2D`** | **manquait** |

Six champs posés sur douze, et deux inversés : voilà les trois plantages.

**Avec le descripteur complet, le jeu ne plante plus.** Quatre captures,
aucune fermeture. `quest_sprite` est donc appelable.

**Mais rien ne se dessine** — et le dossier sait déjà ce que ce silence
signifie. `quest_diagnostic_police` le note depuis le 2026-10-11 :

> `0x18018CA20` laisse TOMBER la commande, sans un mot, quand le jeu de
> sprites de la police n'est pas enregistré dans le contexte 2D.

C'est exactement le cas ici. `0x18018CA20` lit `(desc+4) >> 0x10 & 0xFFF`
— soit **1** pour nos pavés — et cherche ce **rang** de planche dans son
arbre. La greffe charge bien `QUEST_SPR_CCMN`, mais **charger n'est pas
enregistrer dans le contexte 2D** : ce sont deux choses différentes, et la
seconde n'a jamais été faite pour autre chose que la police.

**La prochaine étape est donc nommée, et elle est courte** : reprendre ce que
`quest_diagnostic_police` sait déjà faire — vérifier l'enregistrement du jeu
de sprites dans le contexte 2D — et l'appliquer au rang 1. Le reste du
chemin est désormais prouvé : le descripteur est juste, l'appel passe, le
sprite existe en anglais dans Final Showdown.

### 37.20 LE SPRITE NE SE DESSINE TOUJOURS PAS — CE QUI EST ÉCARTÉ

Avec le descripteur complet du §37.19, **`quest_sprite` ne plante plus**.
Mais rien n'apparaît, et trois essais ont écarté trois causes :

1. **Ce n'est pas la géométrie.** Un quad de 400 x 200 posé au centre de
   l'écran ne paraît pas davantage qu'un pavé de 172 x 40 dans son coin.
2. **Ce n'est pas l'identifiant de planche.** `SPR_C_CMN` porte
   l'identifiant **0** et le rang **1** ; l'`info` du sprite, `0x1000F`,
   désigne donc bien « jeu 1, rang 15 ». Essayé aussi avec « jeu 0 » :
   même silence.
3. **Ce n'est pas le chargement.** La greffe charge `QUEST_SPR_CCMN`, et le
   badge de grade — qui vient de la MEME planche — s'affiche parfaitement
   par la voie AET.

La commande est donc **acceptée puis abandonnée**, exactement comme le note
`quest_diagnostic_police` : `0x18018CA20` la laisse tomber sans un mot quand
le jeu de sprites n'est pas **enregistré dans le contexte 2D** — ce qui n'est
pas la même chose qu'être chargé.

**Ce qu'il faut lire ensuite**, et c'est maintenant la seule inconnue : dans
`0x18018CA20`, l'arbre parcouru (`puVar11`) vient du contexte ; il faut
identifier **où il est rempli**, c'est-à-dire la fonction qui inscrit un jeu
de sprites dans ce contexte, et l'appeler pour le rang 1. Les candidats sont
dans le module 0x180187xxx, qui porte déjà `PREPARE_SPR` (0x187AB0),
`CHARGER_SPR` (0x187C50) et `ETAT_SPR` (0x187CC0) — la greffe utilise les
trois, mais aucune ne fait cet enregistrement.

**L'état** : `quest_sprite` est écrite, complète et inoffensive ; son appel
est sous `#if 0` ; le texte provisoire tient la place ; le jeu tourne.

### 37.21 L'ARBRE DU CONTEXTE, ET LES DEUX POSEURS

**L'arbre est au tout début du contexte** : dans `0x18018CA20`,
`puVar11 = (undefined8 *)*param_1` — le contexte 2D commence par une map,
cherchée avec `(desc+0x04) >> 0x10 & 0xFFF`.

Et il y a **deux poseurs**, pas un :

    0x180187AF0(desc)   depose TEL QUEL
    0x180187C00(desc)   RESOUT d abord, puis depose :

        if (*desc == 0) {
            lVar1 = FUN_18018C610(base_des_sprites, desc[1]);
            desc[1] = *(int *)(lVar1 + 0x28);      /* l identifiant TRADUIT */
        }
        FUN_18018CA20(contexte, desc);

D'où une lecture du champ `+0x00` qui manquait : **type 0 = un sprite à
résoudre, type 2 = un quad plein**. `0x180187B10`, qui dessine un quad, pose
2 ; `FUN_180108320`, qui dessine un glyphe, laisse 0. Nous posions 2 tout en
donnant un identifiant de sprite : la traduction n'avait donc jamais lieu, et
l'arbre ne pouvait rien trouver.

Et l'identifiant attendu par `0x180187C00` est celui de **la base**
(`SPR_C_CMN_COL_ICO_MAIN_1_E` = 55095), pas le `info` composé.

**Essayé, et toujours muet** : type 0, identifiant 55095, dépôt par
`0x180187C00`. Le jeu ne plante pas, rien ne s'affiche.

Il reste donc une condition, et une seule piste sérieuse :
`FUN_18018C610(base, id)` échoue sans doute, parce que la base interrogée
(`DAT_180719908`) n'est pas `spr_db.bin` mais la table **en mémoire**, dont
les identifiants ne sont pas forcément ceux du fichier. **La mesure à faire
est petite** : journaliser la valeur que `FUN_18018C610` rend pour 55095 — si
elle est nulle, tout est dit, et il faudra prendre l'identifiant interne
plutôt que celui de la base.

**L'état** : `quest_sprite` est écrite, complète, inoffensive, son appel sous
`#if 0` ; le texte provisoire tient la place ; le jeu tourne.

### 37.22 LA RÉSOLUTION MARCHE — MESURÉE

La sonde demandée, posée dans la greffe et lue au journal :

    [quest] resolution de 55095 : enregistrement 2192757874000   (NON NUL)
    [quest]    son identifiant interne (+0x28) 65551             = 0x1000F

`0x18018C610(base, 55095)` **trouve bien notre sprite** et rend l'identifiant
composé `0x1000F` — exactement celui que `spr_db.bin` annonce. La traduction
de `0x180187C00` fonctionne donc, et `0x18018CA20` cherche ensuite le **jeu
1** dans l'arbre du contexte. **C'est cette recherche qui échoue.**

Tout le reste de la chaîne est donc prouvé : le descripteur (§37.19), le type
0 et les deux poseurs (§37.21), la résolution (ici). Il ne manque que
l'inscription du jeu dans l'arbre.

**Et `PREPARE_SPR` n'est pas cette inscription**, contrairement à ce qu'on
pouvait croire :

    void FUN_180187AB0(void)            /* = QUEST_RVA_PREPARE_SPR */
    {
        FUN_18018C7D0(contexte,
                      (base[0x98] - base[0x90]) / 0x58);   /* le NOMBRE de planches */
    }

Elle **dimensionne** le contexte à autant d'objets `SPRSET` qu'il y a de
planches dans la base — et la greffe l'appelle déjà. Les `SPRSET` vont dans
un vecteur ; l'arbre interrogé par `0x18018CA20`, lui, est `*contexte`, une
map à part.

**La dernière inconnue est donc : qui insère dans `*contexte`.** C'est une
recherche d'écriture sur l'offset 0 du contexte, ou d'appel d'insertion de
map avec `DAT_180719900` — une poignée de candidats dans le module
0x180187xxx / 0x18018Cxxx.

**L'état** : `quest_sprite` écrite et complète, son appel sous `#if 0`, les
deux sondes (pointeurs du contexte, résolution) laissées en place car elles
ne coûtent qu'une ligne de journal chacune, le texte provisoire affiché, le
jeu qui tourne.

### 37.23 LE DERNIER MAILLON : LE DRAPEAU « PRÊT » DU SPRSET

L'arbre **n'est pas vide**, et `PREPARE_SPR` n'est pas en cause.
`FUN_18018C7D0(contexte, n)` — ce qu'elle appelle — construit un objet
`SPRSET` par planche et l'**insère dans la map** :

    lVar1 = FUN_180187ED0(contexte, cle);              /* cherche la place */
    FUN_180188690(contexte, ..., lVar1 + 0x20, lVar1); /* insere           */

avec `n = (base[0x98] - base[0x90]) / 0x58`, soit les ~600 planches de la
base. **Le jeu 1 y est donc.**

Ce qui bloque est la condition d'acceptation de `0x18018CA20`, relue mot à
mot :

    if (sprset != 0 && *(char *)(sprset + 0xB8) != '\0') { ... dessiner ... }

Le `SPRSET` est trouvé, mais son **drapeau « prêt », en `+0xB8`, est nul**.
Voilà le sens exact de la note du 2026-10-11 : « le jeu de sprites n'est pas
enregistré dans le contexte 2D » — il est inscrit, mais **pas prêt**.

**Ce qui pose ce drapeau** est donc la dernière chose à trouver : le
chargement effectif du jeu DANS le contexte, par opposition au chargement de
ses octets. `QUEST_RVA_CHARGER_SPR` (0x187C50) est le candidat naturel, et la
greffe l'appelle déjà avec `QUEST_SPR_CCMN = 0` — l'**identifiant** de
`SPR_C_CMN`. Or la map est indexée par le **rang**, qui vaut **1**. Les deux
premières choses à essayer sont donc :

1. lire ce que `0x187C50` attend — identifiant ou rang — et, au besoin,
   l'appeler avec 1 ;
2. journaliser le drapeau `+0xB8` du `SPRSET` du jeu 1 avant et après, pour
   mesurer au lieu de supposer.

Le reste du chemin est entièrement prouvé : descripteur (§37.19), type 0 et
poseur résolvant (§37.21), résolution de l'identifiant (§37.22), insertion
dans la map (ici). Il ne manque que ce drapeau.

### 37.24 LE DRAPEAU VAUT 1 — ET L'HYPOTHÈSE DU §37.23 TOMBE

La sonde refait la recherche de `0x18018CA20` à l'identique — la map est au
début du contexte, cle en `+0x20`, fils en `+0x00` et `+0x10`, feuille en
`+0x19`, valeur en `+0x28` — et lit le drapeau. Au journal :

    [quest] SPRSET du jeu 1 : contexte   2683699710000
    [quest]    la valeur trouvee         2683582734104
    [quest]    son drapeau PRET en +0xB8 1

**Le SPRSET du jeu 1 existe et il est PRÊT.** L'hypothèse du §37.23 — « il
est inscrit mais pas prêt » — est donc **fausse**. La condition
d'acceptation de `0x18018CA20` est satisfaite :

    sprset != 0  &&  *(char *)(sprset + 0xB8) != 0      -> VRAI

Et avec l'appel réactivé (type 0, identifiant de base 55095, dépôt par
`0x180187C00`), **toujours rien à l'écran**, sans plantage.

**Tout ce qui précède est donc vérifié**, et il ne reste qu'un endroit où
chercher : **le compartiment**. Nous passons `desc+0x18 = 1` et
`desc+0x1C = 31` — les valeurs que `quest_ecrire_boite` emploie pour le
TEXTE, mais dans un descripteur de texte, où elles occupent d'autres champs
(`+0x24` et `+0x28`). Rien ne dit qu'un sprite déposé dans ce compartiment
soit rendu, ni même que ce couple soit valide ici.

**Les deux essais à faire, dans cet ordre :**

1. reprendre le compartiment que `FUN_180108320` passe pour un glyphe —
   `desc+0x18 = pfVar5[0x15]`, `desc+0x1C = (u32)pfVar5[0x14]` — en
   journalisant ces deux valeurs telles que le jeu les emploie ;
2. à défaut, essayer `desc+0x14 = 0` plutôt que `-1`, pour forcer le calque.

**L'état** : `quest_sprite` est appelée (elle ne plante pas et ne dessine
rien), les trois sondes sont en place et ne coûtent qu'une ligne de journal
chacune, le texte provisoire tient la place, le jeu tourne.

### 37.25 LE COMPARTIMENT NON PLUS — OÙ EN EST LE DESSIN DE SPRITE

Essayé : `desc+0x18 = 0`, `desc+0x1C = 0`, le premier compartiment du calque
courant, au lieu du couple `(1, 31)` que le texte emploie. **Aucun
changement** : pas de plantage, rien à l'écran.

**Le bilan de ce chantier, cause par cause.** Tout ce qui suit a été
MESURÉ, non supposé :

| ce qui a été vérifié | résultat |
|---|---|
| la structure de la commande (§37.15) | douze champs, relevés dans `FUN_180108320` |
| le descripteur complet (§37.19) | posé — **le plantage cesse** |
| le type `+0x00` et les deux poseurs (§37.21) | 0 = sprite à résoudre, 2 = quad ; `0x180187C00` résout |
| la résolution de l'identifiant (§37.22) | `0x18018C610(base, 55095)` rend **0x1000F** |
| l'inscription dans la map (§37.23) | `PREPARE_SPR` inscrit les ~600 planches |
| le drapeau « prêt » du SPRSET (§37.24) | **vaut 1** |
| le compartiment (ici) | ni `(1, 31)` ni `(0, 0)` |

**Il n'y a plus d'hypothèse étayée.** Chaque essai écarte une cause sans en
désigner une autre, et c'est le signe qu'il faut changer d'instrument :
relever le descripteur de `FUN_180108320` **à l'exécution** — pas dans la
décompilation — pour le comparer champ à champ au nôtre. Cela demande un
détour posé sur cette fonction (`tools/patch_moteur.py`), c'est-à-dire un
chantier en soi, mais c'est la seule mesure qui tranchera d'un coup, comme
l'instrument du §31 l'avait fait pour les calques.

**L'état du dépôt** : `quest_sprite` est écrite, complète, appelée et
inoffensive ; les trois sondes (pointeurs du contexte, résolution, drapeau du
SPRSET) restent en place et ne coûtent qu'une ligne de journal chacune ; les
textes « Main Costume » / « Type A » tiennent la place des images ; le jeu
tourne.

### 37.26 LE MAUVAIS MODÈLE — ET CE QUE LA LECTURE DU CODE MONTRE

Frédéric, après cinq essais infructueux : « tu as encore dérivé sur la
méthode, tu dois chercher dans le code, décompiler, ne jamais supposer ».
Il a raison, et voici ce que la lecture donne.

**`FUN_180108320` n'est pas un dessin de sprite.** Sa signature le dit :
`ulonglong FUN_180108320(ushort param_1)` — **un caractère**. Tout ce qu'elle
emploie vient de la police globale `DAT_18070FB38`. En relever les champs
pour en déduire « la » structure de commande était une erreur de départ.

**Le vrai dessin de sprite est `FUN_180023930`**, dans le module AET — l'un
des appelants de `0x180187C00`, trouvé en remontant ses appelants au lieu de
deviner. Sa construction :

    FUN_180189880(&local_128);     /* l init */
    ... les champs ...
    FUN_180187C00(&local_128);     /* le depot */

et sa disposition **n'est pas celle que nous copiions** :

| offset | `FUN_180023930`, le sprite AET | ce que nous posions |
|---|---|---|
| `+0x04` | l'identifiant du sprite | identique |
| `+0x08` | la **couleur**, composée par décalages | l'argument 7 de `0x180187B10` |
| `+0x0C` | des **drapeaux** : `\|= 0x10000`, `0x20000`, `0x10000000` | rien |
| `+0x10` | **1, 2 ou 3** selon le mode de fusion | rien |
| `+0x14` `+0x18` `+0x1C` | pris sur l'objet AET : `+0x34`, `+0x38`, `+0x3C` | calque et compartiment **devinés** |
| `+0x20` `+0x24` | l'objet AET `+0x8C`, deux fois | la couleur |
| `+0x60` et au-delà | **LA MATRICE** (`local_c8 = *param_2`) | rien |

**Le descripteur d'un sprite porte une matrice de transformation**, pas un
couple (position, taille). Sans elle, le quad est dégénéré — et c'est
l'explication du silence complet : la commande est acceptée (le SPRSET est
prêt, §37.24) puis dessinée en rien du tout.

`0x180187B10`, que nous prenions pour modèle, construit une commande de
**type 2** — un quad plein, aux champs disposés autrement. Mélanger les deux
dispositions ne pouvait mener nulle part, quel que soit le nombre d'essais.

**La suite, et elle est maintenant écrite dans le code** : reproduire
`FUN_180023930`. Cela demande les champs de l'objet AET qu'elle lit
(`+0x34`, `+0x38`, `+0x3C`, `+0x84`, `+0x8C`) et la **matrice**, que
`FUN_180023650` construit (§37.2) — c'est-à-dire reprendre le chemin AET
complet. Autrement dit : si nous devons bâtir une matrice de calque pour
dessiner un sprite, **autant poser un calque**, ce que la greffe sait déjà
faire — et le vrai travail devient d'ajouter la composition manquante à une
planche que nous contrôlons.
