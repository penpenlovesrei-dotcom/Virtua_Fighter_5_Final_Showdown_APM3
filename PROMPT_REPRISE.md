# Reprise — Virtua Fighter 5 Final Showdown, build arcade APM3

*À jour du 2026-09-10. Colle ce fichier entier comme premier message.*

> **Pourquoi DEUX fichiers de reprise, et pourquoi on les garde séparés.**
> `PROMPT_REPRISE.md` (ce fichier, ~500 lignes) est le **briefing** : l'état
> présent, ce qui marche, les pièges, les outils. C'est le seul à coller.
> `REPRISE.md` (3 300 lignes) est le **journal** : cinquante-deux entrées datées, qui
> disent *comment* on y est arrivé et *ce qui a été essayé et rejeté*.
>
> Les fusionner ferait un premier message de 3 000 lignes — l'inverse du but —
> ou perdrait l'historique des impasses, qui est ce qui empêche de les
> refaire. La règle est donc : **ce fichier ne raconte rien**, il renvoie au
> journal par date ; **le journal ne résume rien**, il ajoute des entrées.
> Quand les deux se contredisent, c'est ce fichier qui a tort : le journal est
> écrit au moment de la mesure.

---

Tu reprends un chantier de rétro-ingénierie sur **Virtua Fighter 5 Final
Showdown, build arcade APM3** (carte SEGA ALLS). Atelier :
`C:\Users\frede\Desktop\VF5RE`. Écris en français.

> **L'ÉTIQUETTE EST TRANCHÉE — ne la rouvre pas.** Le 2026-09-06, une séance a
> conclu à tort, à partir du nom de dossier `APM3_US` et d'un mémo, que ce
> chantier portait sur *Ultimate Showdown*, et a réécrit cet en-tête.
> **Frédéric a tranché : c'est Final Showdown APM3**, et tous les noms du
> chantier doivent y faire référence.
>
> À retenir pour ne pas refaire l'erreur : le dump `…\VF5 FS DECOMP\APM3_US`
> est bien celui d'où viennent nos binaires (empreinte SHA-256 identique à
> l'octet près, `045c0696…`), et le dossier `vf5fs_media\rom\movie` de
> l'atelier est un **lien symbolique** vers ce même dump. Il n'y a donc
> **qu'une seule version en jeu** dans tout le chantier, fichiers de film
> compris. Le `_US` du nom de dossier ne dit rien du titre.

Le moteur est `runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll` (3,4 Mo, base
`0x180000000`), lancé par `vfes.exe`. **Ne lis jamais le binaire patché pour
analyser** : lis `vf5fs-pxd-w64-Retail_APM3.dll.origine`, et passe `--origine`
aux outils. Le patcheur repart toujours de l'origine, donc un correctif retiré
de la ligne de commande disparaît vraiment.

**Où en est la lecture du binaire** (mesuré le 2026-09-08) : `.pdata` liste
**13 661 fonctions**, 3,13 Mo de code. Nos notes et nos outils en touchent
**1 647**, soit **12 % des fonctions et 20 % du code**. Le reste est
essentiellement CRT, STL et rendu bas niveau, jamais approchés. Le chiffre est
un majorant généreux — une adresse citée n'est pas une fonction comprise — et
il ne voit pas les fonctions **feuilles**, absentes de `.pdata`.

Le but du chantier : ce build arcade contient tout le **mode console** (dix
modes, 55 sous-états, l'arbitre de fin de combat) **et tout le netcode de bornes
liées**, mais des maillons en ont été retirés ou bouchonnés. On les refabrique,
un par un.

---

## 1. Ce qui marche, validé à l'écran

Lanceur unique, double-cliquable : **`tools\console.cmd`**. Il reconstruit
`apm.dll` en ASCII avant de patcher — indispensable, voir §2.

| | état |
|---|---|
| **Dural** | jouable dans la grille |
| **SINGLE PLAYER** | les **quatre** lignes lancent le combat — Arcade, Score Attack, License Challenge et **Special Sparring** (2026-09-06) |
| **Score Attack** | **pose bien son mode 1** — mesuré au débogueur le 2026-09-05 |
| **OFFLINE VERSUS** | à deux — clavier joueur 1, manette joueur 2 |
| **DOJO** | quatre lignes, `How to Play` ajoutée |
| **TERMINAL** | avec son vrai décor `trm` ; **Customize a un chemin intact** |
| **Légende du bas** | ne se superpose plus quand un sous-menu est ouvert (2026-09-06) |
| **ATTRACT** | joue **la vidéo de la borne**, remultiplexée en USM ; coupée par START, elle ramène au titre (2026-09-06) |
| **OPTIONS > Settings** | quatrième ligne **`Tips` Off/On** : elle commande le conseil des écrans de chargement (2026-09-06) |
| **OPTIONS**, **EXIT GAME**, **Échap** | voir `analysis/menu_console.md` |

*Le titre qui transparaît sous celui d'un sous-menu (« MAIN MENU » sous
« SINGLE PLAYER ») est l'**affichage normal**, tranché par Frédéric. Ne pas
le « corriger ».*

Touches (joueur 1, clavier) : flèches, **Entrée = valider**, **W = annuler**,
X/C/V = croix/rond/triangle, Espace = SELECT, T/Y/U = L1/R1/R2, F1/F2 =
TEST/SERVICE, Échap = sortir.

**Les lanceurs démarrent LENTEMENT.** Ils disent eux-mêmes « Le jeu tourne »
quand c'est parti ; ne pas les croire morts avant ce message.

### Les décors — LE CHANTIER EN COURS (2026-09-11)

> **LE LANCEUR À ESSAYER MAINTENANT : `tools\decors_vf5.cmd`** — les
> décors de VF5 R **et** ceux du **VF5 d'origine (ver.B)**, indices 42 à 81.
> La barre espace fait tourner chaque case : Final Showdown → VF5 R →
> VIRTUA FIGHTER 5. La case de Dural a **neuf** variantes : les cinq de FS
> et les **quatre de ver.B** (une géométrie, quatre ciels : coucher de
> soleil, jour, orage, nuit étoilée — `analysis/ciel_verb_du1..4.png`).
> Posé, patché, les deux contrôles verts — **pas vu à l'écran**. Journal
> (63), `analysis/decors.md` §21, lot `tools/variantes_vf5.py`.
>
> **Ce qui commande ver.B, mesuré** : ses identifiants de TEXTURE ne sont pas
> ceux de FS (3 277 collisions sur 3 975 : on renumérote NOTRE archive) ; ses
> RANGS d'objets non plus (on relit SON descripteur) ; et ses effets, ses murs
> et ses animations sont relus dans SES tables (ELF
> `extracted/LIND_VF5/id/disk0/vf5`). La table de VF5 R relue pareil donne
> `hai` sans THUNDER : ce que Frédéric avait vu sur hi5.
>
> **Depuis le 2026-09-11 (journal (65), `decors.md` §22), RIEN ne vient de FS
> pour les entrées 42-81** : listes, murs, animations, descripteurs et
> DOSSIERS d'effet sont relus dans le binaire de LA génération
> (`tools/generation.py`, source unique) et traduits (`Traducteur`). Les sept
> tâches que FS ne savait pas servir — LEAF, YUKA, RAIN, RINGOUT_SPLASH,
> SNOW_RING, WET_CLOTH, FOG_RING — le sont, par des stubs de la greffe
> (`GENERATION_STUBS`, `YUKA_*`, `RINGOUT_*` dans `patch_moteur.py`) ; un décor
> de FS relit toujours SES octets d'origine. Les deux contrôles relisent ces
> dossiers en suivant le code. **Rien de tout cela n'est vu à l'écran** :
> à regarder en priorité bn5/bnb (sol qui se casse), tr5/trb (pétales),
> jn5/snb (anneau de brume), br5/ncb (pluie), rv5/sn5/rvb/jnb (éclaboussure
> de ring-out), ykb (anneau de neige).
>
> **Même jour, deuxième retour (journal (66), `decors.md` §23)** : FS câble
> des comportements sur des NUMÉROS de décor et d'uid (grillage alterné,
> reflet de gym, plan de coupe de sin, bar, balancement de riv, flashs de fin
> de round de smo) ; ceux que R/ver.B ont aussi sont rendus
> (`generation.CABLAGES`). **Vu à la sonde : grillages de gm5/yk5 alternés,
> flashs de so5 en fin de round seulement.** Les **quatre Dural de VF5 R**
> sont posés en 82-85 (`d15..d45`), la case de Dural a 13 variantes ; le
> lanceur passe à `--decors-table 86 --decors-5r-dural`. **Restent ouverts,
> avec un constat mais sans correctif** : l'eau de skb (le ring de ver.B EST
> l'objet WATER_RING, rendu blanc par FS — choix à faire), les empreintes de
> ykb (même logique et mêmes données chez FS/R/ver.B, c'est le rendu des
> shaders de neige qui diffère), le brouillard de jn5 et la brume de sn5 (les
> fichiers sont LUS, FOG_RING tourne — il faut une référence de ce que
> Frédéric voit chez R), sk5 tout bleuté.
>
> **L'outil qui a tout tranché : `tools/sonde_decor.py <indice>`** — force un
> décor, mène le jeu seul au combat, capture, journalise les fichiers et des
> espions. Deux minutes et demie par décor, sans clavier.
>
> **Le lanceur VF5 R seul reste : `tools\decors_5r.cmd`** — les
> **DIX-NEUF décors de VF5 R**, ajoutés aux indices 42 à 60. Dans un écran de
> sélection de décor, la **barre espace** fait passer la case de sa version
> Final Showdown à sa version VF5 R. Posé, patché, contrôlé (`RIEN A REDIRE`
> sur les dix-neuf) — **pas encore vu à l'écran**. Journal (49),
> `analysis/decors.md` §18. Pour tout rendre : `decors_5r_retirer.cmd`.
>
> Le décor **42** (`d5r`, le dojo d'Akira) est le seul VALIDÉ à l'écran :
> géométrie, flammes et barrières, le 2026-09-10. C'est le témoin de la
> recette ; son lanceur seul reste `tools\dojo_5r_repli.cmd`.

<details>
<summary>Comment on y est arrivé (le dojo, décor par décor)</summary>

> **LE LANCEUR DU DOJO SEUL : `tools\dojo_5r_repli.cmd`.**
> MENU → DOJO → **choisir le dojo de VF5 R dans l'écran de sélection de décor**
> (le mode DOJO en a bien un — tranché le 2026-09-10, ne pas rouvrir). Ce qu'on
> veut voir : la géométrie de 2008, **ses flammes**, **son mur**.
>
> **LE DÉCOR AJOUTÉ S'AFFICHE** — validé à l'écran le 2026-09-10. Il aura fallu
> lever quatre verrous, et ils donnaient tous le **même** écran de chargement
> qui tourne :
>
> | le verrou | journal |
> |---|---|
> | l'**écrêtage** `cmova ebp, 39` : tout indice > 40 devenait `gym`, et `-1` aussi | (39) |
> | la **dixième pièce**, `envmap_correct_<code>.txt`, absente du dump VF5R | (40) |
> | les **bases embarquées dans le binaire** (`FArC` en `0x1804137F0`) | (42), (44) |
> | une **quatrième table indexée par l'étage** : les objsets à charger en plus | (45) |
>
> Puis deux manques — **pas de flammes, pas de mur**. Les flammes sont
> **vues à l'écran** (index des noms d'objets global et trié, un doublon rendait
> l'objset du modèle ; et chaque tâche d'effet a sa propre table indexée par le
> décor — journal (46)).
>
> **Les barrières ont demandé DEUX corrections de plus, et elles sont
> VALIDÉES À L'ÉCRAN le 2026-09-10.**
>
> 1. l'entrée de `TaskEffectWall` ne porte **que des pointeurs** : les 28
>    morceaux du mur (4 poteaux + 24 panneaux, carré de 12×12) sont dans les
>    blocs qu'ils désignent, et ces blocs nomment leurs objets par
>    `(objset << 16) | rang` — **l'objset du modèle** — plus l'uid 1194. Cloner
>    l'entrée ne clonait pas le mur. Journal (47), `decors.md` §17.4 ;
> 2. et surtout : **`EFFECT_WALL` n'était jamais CRÉÉE.** Les tâches d'effet
>    d'un décor sont listées dans le **`+0x20`** de `0x18034D570` — la table
>    qu'on croyait « toutes entrées vides », ce qui n'était vrai que de ses
>    quatre premiers octets. Nos entrées neuves clonaient l'entrée 0, qui ne
>    demande aucune tâche. Journal (48), `decors.md` §17.5.
>
> **Le symptôme collait exactement, et c'est Frédéric qui l'a donné** : « les
> barrières sont invisibles, mais la collision est bien gérée ». Les flammes
> marchaient parce que `EFFECT_AUTH3D` est **toujours** créée ; la collision
> marchait parce qu'elle vient du descripteur `+0xB8`/`+0xC0`, pas de la tâche.
>
> **UN CLONE N'EST UN CLONE QUE SI L'ENREGISTREMENT ENTIER L'EST, ET SI CE QU'IL
> POINTE L'EST AUSSI.** C'est la question à poser devant toute table indexée par
> le décor. Il y en a **sept** connues.
>
> `controle_decor_neuf.py` a maintenant un **§6** (les deux tables d'effets : nos
> objets, nos uid) et un **§7** (les tâches d'effet du décor, comparées à celles
> du modèle).

</details>

**La direction, tranchée par Frédéric le 2026-09-09** : recycler un emplacement
d'essai **n'est pas un ajout**, c'est un remplacement de décor inutilisé, et il
n'y en a pas assez pour les décors de VF5 R **et** du VF5 d'origine. On ajoute
de vraies entrées.

#### Ce qui est acquis, et validé à l'écran

| | validé |
|---|---|
| une section greffée peut porter ses **relocations** (`pe_sections.py`) | prouvé dans le processus vivant |
| les **trois tables** du chantier décors déménagées dans `.decors`, 577 relocations | **oui** — « rien n'a changé à l'écran » |
| la table portée à **44 décors**, six bornes levées, trois entrées neuves | **oui** — idem |
| le **nom de variante** écrit à l'écran (`--variantes-texte`) | **oui** |
| les **cinq décors de Dural** et la barre espace (`--variantes`) | **oui** |
| **le décor AJOUTÉ, indice 42, s'affiche dans le DOJO** | **oui** — 2026-09-10 |
| ses **flammes** | **oui** — 2026-09-10 |
| ses **barrières de ring** | **oui** — 2026-09-10, après deux causes (journal 47 puis 48) |

#### Le premier décor vraiment ajouté

Le dojo d'Akira de VF5 R, **indice 42**, code `d5r`, objset **6150**, auth_3d
`STGD5R` / `EFFSTGD5R`, collision `rom/STGD5R_COLI.000.bin`. Ses **dix-sept**
pointeurs sont valides — murs (`+0xC0`) et neuf reprises de musique comprises.
Un emplacement d'essai n'en portait que sept.

**La recette complète, telle qu'elle est aujourd'hui** (`analysis/decors.md`
§16-17 ; chaque ligne a été payée par un écran de chargement infini ou une
absence silencieuse) :

| | |
|---|---|
| **dix** fichiers posés sous `d5r` | les neuf de la génération source **plus** `envmap_correct_d5r.txt`, pris dans le `.par` sous le code du modèle. Aucun nom à masquer : ils n'existent pas dans le `.par` |
| `obj_db.bin` | une entrée d'objset, ses objets **RENOMMÉS** `STGDJO_` → `STGD5R_`, et le fichier **écrit DANS le `.par`** (`par_ecrire.py`) — le masquer ne sert à rien |
| `--obj-db-libre` | un octet dans le `FArC` **embarqué dans le binaire**, sinon le moteur lit sa copie à lui |
| `auth_3d_db.bin` | deux catégories, uid renommés comme les objets ; posé en fichier libre, nom masqué (celui-là n'est pas embarqué) |
| les `.a3da` | membres **et** contenu renommés, réécrits en `FArc` brut (`farc.ecrire_farc`) |
| **six** tables déplacées | descripteurs, codes, grille, objsets en plus, effets a3d, effets mur |
| trois immédiats | `--decors-table 44`, `--decor-ecretage 44`, `--decor-repli 42` |

| lanceur | ce qu'il donne |
|---|---|
| `tools\dojo_5r.cmd` | **le décor ajouté, vu depuis le DOJO** — pas de seconde manette |
| `tools\dojo_5r_temoin.cmd` | le même build avec le dojo d'origine |
| `tools\decor_ajoute.cmd` | le décor ajouté avec l'anneau `[11, 42]` sur STAGE SELECT (demande OFFLINE VERSUS) |
| `tools\decor_ajoute_retirer.cmd` | rend l'état d'origine |
| `tools\decors_44.cmd` | 44 décors, rien ne sélectionne les neufs — **validé** |
| `tools\decors_grille.cmd` | les deux tables + la grille déménagées — **validé** |
| `tools\decors_table.cmd` | les deux tables déménagées — **validé** |
| `tools\decors_5r.cmd` | **LE build du chantier** : les DIX-NEUF décors de VF5 R, indices 42 à 60, un anneau par case (barre espace) |
| `tools\decors_5r_retirer.cmd` | rend l'état d'origine des dix-neuf |
| `tools\decors_vf5.cmd` | **LE build du chantier depuis le 2026-09-11** : VF5 R (42-60) + VF5 ver.B (61-81), trois générations par case, neuf variantes pour Dural |
| `tools\decors_vf5_retirer.cmd` | retire ver.B (VF5 R reste posé) |
| `tools\controle_decors_vf5.py` | contrôle avant vol de ver.B : textures renumérotées, objets relus PAR NOM, tâches/murs/animations comparés aux tables de ver.B |
| `tools\variantes_vf5.py` | **la table du lot ver.B**, et les lecteurs de l'ELF de ver.B (descripteurs, tâches, murs, animations, textures) |
| `tools\generation.py` | **la source unique** de ce qu'une génération (VF5 R, ver.B) dit de ses décors : descripteurs, tâches, murs, animations, DOWN, et les dossiers de TOUTES les tâches d'effet, relus dans son ELF avec vérification de l'instruction qui les nomme. `py -3 tools/generation.py` les liste |
| `tools\tables_generation.py` | retrouve PAR VALEUR les tables d'une génération (descripteurs, tâches, murs, animations) ; `comparer` confronte à la DLL |
| `tools\emu32.py` | rejoue un constructeur statique x86-32 (les dossiers en `.bss` : FOG_ANIM, FOG_RING, RAIN) ; refuse toute instruction inconnue |
| `tools\index_elf.py` | qui lit/écrit une adresse d'un ELF Lindbergh (`py -3 tools/index_elf.py r 0xA 0xB`) |
| `tools\effets_generation.py` | typeinfo → vtable → données, pour chaque TaskEffect d'une génération |
| `tools\sonde_decor.py` | **LA SONDE D UN DÉCOR** : `py -3 tools/sonde_decor.py 54 --toutes 4 --depuis 72` force le décor 54, mène le jeu SEUL au combat (Arcade), capture dans `analysis/sonde/` ; `--fichiers fog_` journalise les ouvertures, `--bp 0x18007E420:nom[:mémoire]` pose des espions, `--histo 0x18007E322:nom:Rbp+xmm6` compte les valeurs prises. Remet le scénario manuel après |
| `tools\shader_empreintes.py` | **LE SHADER DES EMPREINTES DANS LA NEIGE** (ykb) : compile le geometry shader que le portage n a pas donne a `snow_footprint..vp` et pose `w64/shader_vf5_w64.farc` (ce seul membre, en `GSFX`) ; `--controle` relit. Les shaders d APM3 sont du DXBC (Direct3D 11), pas l ARB des archives Lindbergh. REPRISE (67) |
| `ghidra/vf5r_lind`, `ghidra/vf5verb_lind` | les ELF de R et ver.B analysés dans Ghidra (4-5 min chacun), pour décompiler leur code |
| `tools\controle_decors_5r.py` | contrôle avant vol des dix-neuf, dans la DLL patchée : pièces, bases, descripteur, tâches d'effet, mur |
| `tools\plantage_5r.cmd` | **LA SONDE DE PLANTAGE** : le jeu sous débogueur, le clavier reste à vous. Journal au fil de l'eau dans `analysis/pister_plantage.txt` — quel décor était demandé, quelle porte de l'état 3, et dans quelle SECTION l'exception tombe |
| `tools\variantes_5r.py` | **la table du lot** — modèle, code, indice, objset. Les trois outils la lisent, et elle ne vit qu'ici |
| `tools\dojo_5r_repli.cmd` | le décor 42 seul, vu du DOJO — le témoin validé de la recette |
| `tools\depister_5r_ajoute.cmd` | les **sept portes** de l'état 3 **pour un décor ajouté** : quels fichiers sont ouverts, où ça bloque |
| `tools\objset_pret.cmd` | compare l'enregistrement de notre objset à celui d'un objset prêt, champ par champ |
| `py -3 tools/pister_objset.py` | le moteur connaît-il notre objset ? Lit son vecteur trié dans le processus, **sans aucune navigation** (40 s, le jeu se ferme seul) |
| `tools\pister_60_dojo.cmd` | la sonde du champ `+0x60` : DR sur le *pointeur* de tâche, et quatre BP le long de la chaîne |
| `tools\pister_decor_ajoute.cmd` | **la sonde** : quel indice le jeu demande, et qui le demande |

#### TROIS PIÈGES D'INDICE, tous payés à l'écran le même jour

* **41 = 0x29 est le code « décor ALÉATOIRE »**, testé par égalité à sept
  endroits. Un décor posé là se fait tirer au sort. Les ajouts commencent à
  **42**, et le patcheur refuse 41 ;
* **le mode DOJO A BIEN un écran de sélection de décor** — tranché par Frédéric
  le 2026-09-10, contre ce qui était écrit ici depuis le 2026-09-09. Ne pas
  rouvrir : « le mode DOJO ne consulte jamais STAGE SELECT » était **faux**, et
  ça a coûté une séance. Ce qui est vrai du bloc `0x18020AE50` (39 `gym` / 11
  `djo` selon un drapeau) : il est dans la branche `mode == 1`, **mesurée à zéro
  passage**, donc `--dojo-decor` patche un immédiat qui ne s'exécute pas. Et
  quand rien n'est demandé (`r9d = -1`), c'est l'**écrêtage** `0x180203F2E` qui
  en fait 39. Le décor ajouté se choisit donc **à l'écran, dans le DOJO** ;
  `--decor-ecretage <N>` est ce qui le laisse survivre au trajet ;
* **une entrée de descripteur laissée à zéro est une mine** : `0x18018F590`
  balaie les N descripteurs et **déréférence `+0x00`**. Toute entrée au-delà de
  41 est donc un clone complet du modèle.

#### Les anciens lanceurs, et pourquoi ils restent

| lanceur | ce qu'il donne | vu à l'écran |
|---|---|---|
| `tools\decors_dural.cmd` | les cinq décors de Dural ; la grille en détourne quatre cases | **oui** |
| `tools\decor_5r_akira.cmd` | le dojo VF5 R qui **REMPLACE** `djo` | **oui** |
| `tools\decor_5r_akira_ajout.cmd` | le même, recyclé sur `trs` — **rend un décor PARTIEL**, gardé comme témoin de ce qu'un emplacement d'essai ne peut pas porter | oui, et raté |
| `tools\variantes.cmd` / `variantes_texte.cmd` | la barre espace, et le nom à l'écran | **oui** |
| `tools\decor_TRM.cmd` / `decor_TS2.cmd` | le décor de l'écran TERMINAL | **oui** |
| `tools\depister_5r.cmd` | les **sept portes** de l'état 3 d'un décor importé | outil |

#### Les faits qui commandent le chantier

* **importer un décor d'une autre génération ne demande aucune conversion** :
  les identifiants d'objets sont les mêmes (`gnd` 114, `reflect` 115, `sdw`
  116, `sky` 117, `ring` 118). L'échec de septembre venait du **mélange** des
  générations, pas du format ;
* **les longueurs de code doivent se correspondre** : `djo` (3) → `d5r` (3),
  `stgdjo` (6) → `stgd5r` (6), `EFFSTGDJO` (9) → `EFFSTGD5R` (9). Les noms
  internes des archives se substituent **en place** ;
* **les noms d'objets et de `.a3da` se recopient VERBATIM** : l'archive posée
  est celle du modèle, renommée. Un nom substitué ne correspondrait à rien, et
  le décor chargerait sans sa géométrie ou son animation, **en silence** ;
* **une case reste UNE case** (tranché le 2026-09-08) : la quatrième ligne de
  grille a été construite puis refusée, et le patcheur la refuse. C'est SELECT
  qui fait défiler les variantes.

Les cinq décors de Dural sont les variantes d'un même lieu, **nommées par
Frédéric** : du1 **SNOW**, du2 **ECLIPSE/METEOR**, du3 **SUBMERSION**, du4
**STORM**, du5 **SPACE**. **Il en manque trois : NIGHT, DAY, SUNSET.**

**Le défilement** (`--variantes`) a deux accroches : `0x180174710` lit la barre
espace (code **6**) et fait tourner le numéro ; `0x1801747C0` l'applique **après**
`0x180174781`, la recomputation du curseur — trouvée par un point d'arrêt
**matériel** en écriture sur `TaskSelStage+0x5C`. **Le nom à l'écran**
(`--variantes-texte`) est dessiné par le **créneau 4 de `TaskSelStage`**
(`0x180400A38`, un bouchon `ret 0`), en neuf passes ; détail dans
`analysis/texte_2d.md` §8-9-10.

### Les films (2026-09-08)

**`tools/usm_mux.py`** convertit un `.sfd` (Sofdec1) en `.usm` (Sofdec2)
**sans réencoder** : les deux portent du **MPEG-1** et de l'**ADX**, donc c'est
un remballage. Prouvé — les flux ressortis ont le même MD5 que ceux de la
source. Le multipiste **AIX** est déplié en voies `@SFA`. Lanceur
`tools/sfd_vers_usm.cmd` (glisser-déposer). Détail : `analysis/films_usm.md`.

Six films Xbox 360 sont extraits dans `extracted/sfd_x360/` — cinq de VF5
vanilla, un du paquet STFS de Final Showdown. Cinq sont en 1280×720 à 60/s,
la définition exacte des films d'APM3. **Aucun n'a encore été joué dans le
jeu.**

---

## 2. Le réseau — RÉSOLU, et un serveur répond (2026-09-06)

Le plantage au démarrage venait de **`System_getGameVersion`**, qui rendait la
chaîne `"0000"` alors que le moteur y lit **l'octet 0 comme majeur et l'octet 4
comme mineur** (deux sites, `0x180219A14` et `0x1800DE298`). D'où la version
« 48.00 », un `sprintf_s` dans un tampon de cinq octets, `ERANGE`, et
`_invalid_parameter`. Le stub rend désormais un pointeur vers `{1u, 0u}`.

Mesure après correction, 45 s :

    _invalid_param  0        plus de plantage
    versionGS       1        major=1 minor=0 -> "1.00"
    ImplSetup / okGameId / okKeychipId / okMainId / okCountry   1 chacun
    SetupLink       1        UNE tentative, reussie
    tic Setup       20661    la machine tourne
    tic Unavailable 0        elle n'a PAS abandonne

**Il ne manque plus aucun maillon côté jeu.** `tools/serveur_allnet.py`
(lanceur `tools/serveur_allnet.cmd`) répond sur `127.0.0.1:80` — le port est
câblé dans le moteur, qui construit l'URL en `"http://" + <hôte> + ":80" +
<chemin>`. Il déchiffre, lit le JSON, et répond. Premier échange reçu :

    [link] POST /api/turninfo   {"client":{"serial":"A69E01A8888","game_id":"0000",
                                 "game_ver":"1.00","location_id":0,...}}
    [gs]   POST /api/data/load  {"free_buckets":{"keys":["misc_*","rule_*","matching_*"]},...}

Le second prouve que **`clé_GS = titleKey XOR constante`** est juste. Le
`titleKey` est un **littéral du binaire** (`0x1805511D8`, 32 octets), recopié
par `0x180219A35` — pas un secret à deviner.

**Le mur suivant : il n'y a pas de STUN.** Le jeu mesure son type de NAT avant
`/api/match`, et notre `turninfo` l'envoie sur `127.0.0.1:3478` où rien
n'écoute. Un coturn ordinaire suffit (`vf5`/`vf5`).

---

## 3. Le réseau — ce qui est acquis, et c'est beaucoup

**Le nom n'est pas `AVLink*`** : le `AV` était la lettre de classe du mangling
MSVC. C'est **`am::abaas`** (ALL.Net). Deux bibliothèques SEGA distinctes :
`abaaslink` (appariement) et `abaasgs` (serveur de titre). Client HTTP =
**libcurl** statiquement lié.

**Le protocole est du STUN/TURN standard.** Magic cookie `0x2112A442` présent
(sept sites) : SEGA n'a pas dévié des RFC 5389 / 5766. **Un coturn ordinaire
suffit.**

**`ULinkPacketAppData` transporte des ENTRÉES de manette**, pas un état :
16 octets utiles, redondance sur dix trames = 150 ms de perte absorbée à 60 Hz.

**Le corps HTTP est entièrement fabricable par nous :**

    corps = en-tete 16 octets en clair || AES-256-CBC( zlib( JSON ) )
            et l'en-tete EST le vecteur d'initialisation

    cle = SHA256(gameId, 4 o) XOR <constante 32 o, litterale en 0x1805CC5D0>

La constante est masquée par un simple `xor al, 0x67` (`0x1802FB875`). La graine
est le `gameId`, que **nous** choisissons — et le serveur le relit dans les
octets 4 à 7 de l'en-tête reçu, donc il n'a pas besoin de le connaître d'avance.
Rien n'est négocié, rien ne vient de la puce. Bourrage PKCS#7 fait à la main
(`0x1802BD47F`), zlib RFC 1950 niveau 6 (`0x1802BDA7F`).

Compression et chiffrement sont **câblés** : `mov word ptr [rbp+0x1d0], 0x101`
en `0x1802CA09D`. Aucun moyen d'obtenir du clair par la configuration ; deux
octets à `0x1802CA0A4` le feraient.

Réponse minimale de `/api/turninfo` (quatre clés, types contrôlés, décodeur
`0x1802F2960`) :

    {"host":"127.0.0.1","port":3478,"id":"vf5","pw":"vf5"}

statut HTTP **200 exigé** (`cmp ax, 0xc8`, `0x1802D969B`). Pas de clé `realm` :
c'est le coturn qui annonce le sien dans son `401`.

**La machine à états** tourne dans un **fil dédié** à ~1 kHz (`0x1802C8CC0`),
pas sur la trame du jeu. Quinze états dans une `unordered_map<int, shared_ptr>` ;
créneau `[1]` = `getId()`, `[2]` = `tic()`, `[5]` = `setResult`. **`tic()` rend
l'identifiant de l'état suivant** ; on ne commute que s'il diffère du courant.
`Startup::tic()` s'écrit `return 1` → passe à `Setup` sans condition.

**Ce qui a été lu depuis** (2026-09-06, voir `analysis/reseau_allnet.md`
§§11 à 14) : la méthode est **POST** (`CURLOPT_POST = 1`, `0x18029242E`),
l'en-tête unique est `Content-Type: application/octet-stream`, l'enveloppe
`"client":{...}` est recousue dans chaque corps, `/api/match` a son encodeur
(`0x1802F8CD0`) et son décodeur (`0x1802F7DF0`) nettement séparés, `_list` et
`_type` sont des suffixes numérotés (`param1`…`param3`, `title_key1`…
`title_key6`), et le `titleKey` est trouvé.

*(Les deux « décodeurs à lire » `0x1802F6370` et `0x1802F6F40` étaient une
fausse piste : ce sont les **encodeurs des deux journaux de fin de partie**.)*

**Ce qui reste ouvert** : le corps de `/api/config`, le contenu attendu par
`/api/alive`, le type de `key`/`num`/`members` dans la réponse de `/api/match`,
et surtout **un serveur STUN/TURN sur 3478**.

Tout est dans `analysis/reseau_allnet.md` (1124 lignes, §10 = la spécification
du serveur minimal), `analysis/reseau_transport.md` (800),
`analysis/reseau_machine.md` (286).

---

## 4. Les pièges de ce binaire, tous payés au moins une fois

- **`tools/apm_stub.c` est un PRODUIT**, régénéré à chaque exécution de
  `gen_apm_stub.py`. Éditer le `.c` ne sert à rien : modifier le générateur.
- **Patcher le site d'appel, jamais le corps.** Les prédicats bouchonnés sont
  partagés par des centaines d'appelants : `0x180007450` (rend faux, 210
  appelants), `0x180007430` (`ret 0`), `0x180007440`, `0x180029FB0` (rend vrai).
- **`.pdata` ne liste pas les FEUILLES**, et une entrée n'est souvent qu'un
  FRAGMENT d'une fonction plus grande. Toute affirmation « personne n'appelle
  X » exige un **balayage LINÉAIRE** (`tools/refs_lineaires.py`). Exemple vécu :
  `ImplLink::setup` n'a aucun appelant direct — elle est atteinte par un `jmp`
  depuis un trampoline pimpl de deux instructions (`0x1802CAC30`).
- **L'ICF** fusionne les corps identiques : deux symboles à la même adresse ne
  partagent pas forcément un rôle.
- **Les vtables voisines se touchent** : lire quatre qwords à une adresse donne
  parfois la fin de la table précédente. `tools/vtable.py` détecte les
  frontières.
- **Le « AV » d'un nom RTTI est du mangling**, pas un préfixe.
- **`+0x224` d'une page est le DERNIER INDICE, pas un compte.**
- **Ne pas neutraliser une garde partagée.**
- **Une fonction voisine n'est pas la même fonction.** Deux fois payé.
- **Mesurer avant de corriger.** Chaque cause supposée plutôt que mesurée s'est
  révélée fausse. Les sondes écrivent **au fil de l'eau** — le débogueur se
  bloque parfois, et un bilan écrit à la fin serait perdu.
- **Une sonde qui pose ses points trop tard est aveugle** : le crash réseau
  tombait avant `t = 8 s`. Poser dès le chargement de la DLL.
- **Ne pas généraliser une correction au-delà de ce qui a été mesuré** : passer
  les 57 chaînes du stub en UTF-16 alors que la mesure n'en désignait que six a
  cassé les chemins `Aime_*` et `System_getGameVersion`.
- **Les heredocs `bash` mangent les antislashs.** Utiliser l'outil Write.
  Repayé le 2026-09-09 : `runtime\media\vf5fs\…` est devenu `runtime\media` +
  tabulation verticale + `f5fs`, `\v` et `\r` ayant été interprétés. Le `.cmd`
  restait valide et `cmd.exe` muet. `verifier_lanceurs.py` refuse désormais
  tout octet de contrôle autre que TAB/CR/LF — **un piège écrit ne protège de
  rien tant qu'un outil ne le voit pas.**
- **`python` est un stub inerte** sur cette machine : lancer `py -3`.
- **Un nom se lit dans sa TABLE, pas dans le tas d'octets.** Balayer l'ASCII
  d'un `*_obj.bin` a rendu 19 298 faux noms et deux identifications de décor
  fausses. `tools/objset.py` lit la table ; quand les noms ne disent rien,
  `tools/textures_decor.py` fait une planche contact et l'image tranche.
- **GHIDRA EST INSTALLÉ, ET LE PROJET EST FAIT.**
  `C:\Users\frede\Desktop\Nouveau dossier\ghidra_12.1.2_PUBLIC_…`, Java 21 dans
  le PATH, projet `ghidra/vf5fs_apm3` analysé (107 s). **`py -3 tools/decomp.py
  0x1800F9C60`** sort le C. Quatre tours de sondes n'avaient pas trouvé la
  quatrième table indexée par l'étage ; deux fonctions décompilées l'ont donnée
  en vingt minutes. Une sonde dit quelle branche s'exécute et ce que vaut un
  champ ; elle ne dit pas ce que le code **fait**.
- **L'INDEX DES NOMS D'OBJETS EST GLOBAL, TRIÉ, LU PAR DICHOTOMIE**
  (`FUN_1800F8B50`, `[gestionnaire+0xC8..+0xD0]`, bâti depuis `obj_db`). Deux
  objsets qui déclarent le même nom d'objet : c'est le **premier** qui gagne.
  Un décor ajouté doit donc **renommer** ses objets (`STGDJO_` → `STGD5R_`), et
  avec eux les uid d'`auth_3d_db` et le contenu des `.a3da`. Pas les textures
  (`F_VF5E_DJO00_…`, sans `STGDJO_`). Ce qui était écrit ici — « les noms
  d'objets se recopient VERBATIM » — est vrai **dans l'archive**, faux dans
  `obj_db`.
- **CHAQUE TÂCHE D'EFFET A SA PROPRE TABLE INDEXÉE PAR LE DÉCOR.** À l'état 3,
  `0x18006F380` donne l'indice à chacune (créneau 7 de sa vtable) :
  `TaskEffectAuth3D` → `0x18034FD20` (les animations, **par numéro d'uid**),
  `TaskEffectWall` → `0x180355C30`. Ce sont des **listes d'association** : un
  indice inconnu ne plante pas, il ne fait **rien**. Les autres (`Snow`, `Rain`,
  `Leaf`…) n'ont pas été ouvertes — le dojo n'en utilise aucune.
- **UN CLONE N'EST UN CLONE QUE SI L'ENREGISTREMENT ENTIER L'EST** (payé le
  2026-09-10). « Les 41 entrées de `0x18034D570` sont toutes vides » était une
  mesure faite sur les **quatre premiers octets** d'un enregistrement de 96. Le
  `+0x20` — la liste des tâches d'effet — ne l'est pas. Une entrée se compare
  **en entier** à celle du modèle, ou pas du tout.
- **UN CLONE N'EST UN CLONE QUE SI CE QU'IL POINTE L'EST AUSSI** (payé le
  2026-09-10, après un essai à l'écran). L'entrée de `TaskEffectWall` ne porte
  **que des pointeurs** : les 28 morceaux du mur, la liste d'uid et les paires
  intact/cassé sont dans les blocs qu'ils désignent, et ces blocs nomment leurs
  objets par `(objset << 16) | rang` — celui du **modèle** — plus l'uid 1194.
  Le décor s'affichait avec ses flammes et **sans ses barrières**, en silence.
  Le patcheur recopie désormais les trois blocs en substituant objset et uid.
  `analysis/decors.md` §17.4.
- **UNE QUATRIÈME TABLE EST INDEXÉE PAR L'ÉTAGE, ET SON ENTRÉE PORTE DEUX
  LISTES** : `0x18034D570`, 41 entrées de `0x60`. `+0x00` = les objsets à
  charger **en plus** (toutes vides), lue par `0x18006F620` et attendue par la
  porte de l'état 4 (`0x18006FA60`) ; **`+0x20` = les TÂCHES D'EFFET à créer
  pour ce décor**, lue par `0x18006F380` — et celle-là n'est **pas** vide.
  Noms en clair dans `0x18034E4D0` : 0 HIT, 1 AUTH3D, **2 WALL**, 3 LEAF,
  5 SNOW, 7 RIPPLE, 9 THUNDER, 16 FOG_ANIM, 17 WET_CLOTH… Toujours créées
  (`0x18034D530`) : HIT, AUTH3D, DOWN, MOVE, PARTICLE, POISON — **WALL n'en est
  pas**, et 32 décors sur 41 la demandent. Une entrée neuve clonée sur
  l'entrée 0 ne demande aucune tâche : le décor ajouté avait ses flammes
  (AUTH3D est toujours là) et **pas ses barrières**. Au-delà de 41 la lecture
  sort de la table et le chargement ne finit jamais. Déménagée par
  `--decors-table`, sans relocation (que des entiers) et un seul site
  (`0x18006F675`).
- **LES BASES SONT EMBARQUÉES DANS LE BINAIRE.** Archive `FArC` en
  `0x1804137F0` : `mot_db`, **`obj_db`**, `tex_db`, `spr_db`, `aet_db`,
  `rob_mot_tbl` et les fichiers d'éclairage de `tst`. Le résolveur la consulte
  **avant** le `.par` et avant le disque : masquer un nom dans l'index du `.par`
  ou poser un fichier libre ne sert donc à **rien** pour ces six-là.
  `--obj-db-libre` masque le `n` de `obj_db.bin` dans cet en-tête (un octet,
  `0x18041381C`) et le résolveur passe à la suite. Preuve croisée :
  `auth_3d_db` n'y est pas, et c'est la seule base dont le masquage marchait.
- **Une borne vérifiée APRÈS le balayage ne borne rien** (payé le 2026-09-10 :
  50 s d'attente par lanceur). `par_masquer.positions()` cherchait dans les
  3,99 Go et sortait de la boucle une fois la borne dépassée : le `find` qui
  suit la dernière occupation du pot lisait l'archive entière pour conclure
  « plus rien ». Deux recherches par nom, neuf noms, trois appels par lanceur.
  La borne se **passe à la fonction de recherche** (`m.find(cible, i+1, borne)`)
  — c'est 200 fois plus rapide *et* plus juste.
- **Borner une recherche de nom au pot de noms.** `par_masquer.py` masquait
  toutes les occurrences dans les 4 Go du `.par` : `STGDJO_COLI.000.bin` en a
  deux vers `0xEDD000`, **dans les données**. La borne se lit dans l'en-tête
  PARC (`0x20` à `min(+0x14, +0x1C)`).
- **Un lanceur ne doit pas pouvoir échouer en silence.** `decor_5r_akira.cmd`
  a été cru mort alors qu'il marchait : le démarrage est simplement **long**.
  Les lanceurs vérifient désormais que `vfes.exe` tourne, et le disent.
- **Aucun pointeur absolu dans la greffe — SAUF si on lui donne ses
  relocations (levé le 2026-09-09).** La DLL est **rebasée** à l'exécution, et
  une section ajoutée n'apparaît dans aucun bloc de relocation : une adresse
  écrite à la base préférée ne désigne rien. C'est encore vrai de `.greffe`,
  qui reste en **RIP-relatif** avec ses tables de chaînes à **pas fixe**.
  Mais `tools/pe_sections.py` sait désormais **reconstruire la table entière**
  ailleurs et repointer le répertoire de données n° 5 : une section greffée
  peut alors porter des pointeurs comme n'importe quelle section du jeu.
  Vérifié dans le processus vivant. Voir `analysis/greffe_relocations.md`.
  Les créneaux de vtable, eux, ont toujours été relogés.
- **Un `.cmd` s'écrit en CRLF.** Réécrit en fins de ligne Unix, `cmd.exe`
  ne lit plus ni les blocs `if ( … )` ni la continuation `^`, et ne dit rien.
  C'est ce qui a rendu `variantes_texte.cmd` inutilisable le 2026-09-08.
  `verifier_lanceurs.py` le détecte.
- **L'état des FICHIERS était hérité d'un lanceur à l'autre.** `patch_moteur.py`
  repart de `.origine` ; `importer_decor.py --poser` ne repart de rien : il
  dépose dans `vf5fs_media/rom/` et masque des noms du `.par`, et ça reste.
  Chaque lanceur **pose** donc son état en tête — et seulement si un fichier
  libre est là, un balayage du `.par` coûtant 16 s.
- **Deux options peuvent se contredire en silence.** `--decors-dural cas`
  translate les indices 7..11 vers du1..du5, et **`djo` vaut 11** : tout combat
  au dojo chargeait du5. Le patcheur refuse maintenant la combinaison avec
  `--variantes-djo`.
- **Un build marche, l'autre pas : DIFFER LES DEUX INVOCATIONS d'abord.**
  Avant les fichiers, avant le binaire. La différence a tenu à une option, et
  il a fallu que Frédéric le demande deux fois.
- **Une borne peut être un `cmov`, pas seulement un saut** (payé le 2026-09-10).
  `0x180203F1E cmp ebp, 0x28` + `0x180203F2E cmova ebp, 39` écrête tout indice
  de décor au-dessus de 40 vers `gym`, **avant** que `TaskStage` le voie. Les
  six bornes connues avaient été trouvées en énumérant les *lecteurs des tables
  de décors* ; celle-ci ne lit aucune table, donc aucune énumération ne pouvait
  la rendre. Et `cmova` est **non signé** : `-1` y est « au-dessus de 40 ».
  Corollaire de méthode : quand un indice ne survit pas, chercher aussi la forme
  `cmp`/`cmov`, et se demander ce que devient `-1`.
- **Une borne et une SENTINELLE se ressemblent.** `cmp edx, 0x29 ; jae`
  borne une table de 41 décors ; `cmp eax, 0x29 ; jne` teste la valeur 41, qui
  est le code « décor **aléatoire** ». Sept sites le font. Lever la borne rend
  41 adressable **sans** lui retirer son sens ailleurs : le décor ajouté s'y
  chargeait, et le tirage au sort aussi. **Le saut qui suit la comparaison
  tranche** — `jae`/`jb` bornent, `je`/`jne` testent une valeur.
- **Un emplacement déjà réparé n'est pas un emplacement libre.** `trm` est le
  décor TERMINAL, réparé et validé le 2026-09-05 ; le recycler l'a cassé.
- **Un emplacement d'accueil ne se met pas dans DEUX constantes.**
  `--variantes-djo` clonait le descripteur vers `evo00` et faisait défiler vers
  `trm` : deux constantes pour une seule donnée, divergées au premier
  changement, et l'option n'a jamais marché sans que rien ne le dise.
  L'emplacement est maintenant un **argument**, et tout en est dérivé.
- **Un code d'emplacement d'arrivée fait TROIS lettres.** `importer_decor.py
  --vers` réécrit `stgdjo_obj.bin` → `stgtrs_obj.bin` **en place** dans
  l'en-tête du `FArC` : `evo00` n'y tient pas. Libres à trois lettres :
  `tst ts3 wht cid trs`.
- **Le garde-fou des emplacements se mordait la queue** : un lanceur qui NOMME
  l'emplacement qu'il pose le rend « pris » aux yeux de la preuve 4, donc
  interdit à lui-même. `--pour <lanceur.cmd>` lève sa propre réservation, et
  elle seule.
- **`obj_db` ET `auth_3d_db` DÉCRIVENT L'ARCHIVE QU'ON POSE, PAS LE
  MODÈLE** (payé le 2026-09-10, « nombreux plantages, loadings infinis,
  décors très incomplets »). On y recopiait la déclaration du modèle Final
  Showdown alors qu'on pose la géométrie de 2008 : de **47 à 196 objets
  déclarés sans exister**, et jusqu'à **58 objets de 2008 non déclarés** —
  or ce sont ceux que ses propres `.a3da` nomment, et un nom introuvable
  dans l'index global ne se lie à rien, en silence.
  Et `auth_3d_db` déclarait des uid **sans leur `.a3da`** : `aur`, `umi`,
  `hai` et `tan` n'ont pas `EFF_SAKU_BROKEN`, que le `+0x30` de leur mur
  référence. Un uid déclaré sans son animation, c'est `TaskEffectWall`
  (créneau 1, `FUN_180044640`) qui l'**attend pour toujours** — chargement
  infini ou plantage. Les deux bases se lisent maintenant dans l'archive
  POSÉE (`variantes_5r.objets_archive()`), et le patcheur **tronque** ce
  que les animations manquantes servaient. `controle_decors_5r.py` vérifie
  les dix besoins de chaque décor. Journal (53).
- **LES CINQ OBJETS D'UN DÉCOR NE SONT PAS AUX MÊMES RANGS D'UN DÉCOR À
  L'AUTRE** (payé le 2026-09-10). `DECOR_NEUF_RANGS = (114, 118, 117, 116, 115)`
  — gnd, ring, sky, sdw, reflect — est vrai **pour `djo` seul** ; dix-huit
  modèles sur dix-neuf ont d'autres rangs (`aur` : 413 598 414 −1 −1). Écrire
  ceux de `djo` ailleurs demande des morceaux d'effet pris au hasard : ça
  plante, ça charge sans fin, ou le décor est très incomplet — **les trois
  symptômes de la même faute**. Les cinq champs se recopient du MODÈLE, objset
  substitué, rang inchangé. Et **`0xFFFFFFFF` = « pas d'objet » est une valeur
  normale** : onze descripteurs du jeu en portent. Enfin le rang doit exister
  dans l'archive posée — `ban`, `jin` et `are` n'ont pas de `reflect` en 2008,
  c'est une addition de Final Showdown. Journal (52).
- **UN CONTRÔLE NE DOIT PAS RÉPÉTER L'HYPOTHÈSE DE L'OUTIL QU'IL CONTRÔLE.**
  `controle_decors_5r.py` comparait les cinq objets aux rangs de `djo`, comme le
  patcheur : il validait donc exactement ce qui était faux. Il les lit
  maintenant dans le descripteur du modèle et vérifie leur présence dans
  l'archive. Même faute que `verifier_decors_table.py` et son `n = 41` en dur.
- **UN TABLEAU DE LA GREFFE SE DIMENSIONNE, IL NE SE RELIT PAS** (payé le
  2026-09-10, « nombreux plantages »). `VAR_NUM` gardait ses **quatre** entrées
  en dur pendant que `VARIANTES_MAX_ANNEAUX` passait de 4 à 20 : au cinquième
  anneau il lisait — et **écrivait** — dans `VAR_RANG`, puis dans `VAR_DESC`.
  Un tableau qui déborde chez le voisin ne dit rien ; le jeu tombe ailleurs,
  plus tard, « souvent ». `patch_moteur.verifier_disposition()` contrôle
  désormais que rien ne recouvre rien, et `variantes_greffe` l'appelle avant
  d'assembler. Journal (51).
- **Une profondeur 2D est un INDICE, et il est BORNÉ.** L'ordre de dessin vient
  de `contexte + 16*((desc+0x24) + 1 + ((desc+0x28 + calque) << 5))`, et le
  contexte (`new(0x838)`, `0x18018A030`) ne contient que **128 compartiments**
  : quatre calques de trente-deux rangs. Monter `[contexte+0x828]` de 8 a fait
  **planter le jeu**. Le bon geste est de corriger *son propre* descripteur
  pour viser le rang 127, pas de pousser un état global. Détail :
  `analysis/texte_2d.md` §9-10.

---

## 5. Les outils

Tous dans `tools/`, Python 3, dépendances `capstone` et `pefile`.

| outil | rôle |
|---|---|
| `patch_moteur.py` | **le** patcheur. Repart toujours de `.origine`, REFUSE si les octets attendus n'y sont pas |
| `gen_apm_stub.py` | génère et compile `apm.dll`. `--utf16` pour les six chaînes du chemin réseau |
| `rtti.py` | RTTI MSVC : classe ↔ vtable, 534 vtables (`analysis/rtti_apm3.txt`) |
| `vtable.py` | lit une vtable : créneaux, cibles, **frontières** |
| `refs_lineaires.py` | toutes les références à une adresse, par balayage linéaire |
| `graphe_appels.py` | graphe d'appels par balayage ; gère `UNW_FLAG_CHAININFO` |
| `reseau.py` | IAT `ws2_32`, ses appelants, recherche de constantes |
| `plage.py` | désassemble une **plage**, sans s'arrêter au premier `ret` |
| `carte_zone.py` | cartographie une zone : appelants, appelés, chaînes, bouchons |
| `libelles.py` | résout un identifiant de texte, ou cherche par texte |
| `instrument.py` | le débogueur : points d'arrêt, contexte, lecture mémoire |
| `pister_*.py` | une sonde par question. `pister_link` (réseau), `pister_mode` (mode de jeu), `pister_import` (un décor importé) |
| `substitutions.py` | énumère les sites « `cmp` source … immédiat cible » d'un coup |
| `objset.py` | lit les NOMS et les identifiants d'un `*_obj.bin` |
| `textures_decor.py` | planche contact des textures d'un décor |
| `comparer_builds.py` | compare DEUX builds par leurs **structures** : table des décors (pas déduit), 41 descripteurs champ par champ, chaînes témoins |
| `par_inventaire.py` | inventorie un `.par`, ou en compare deux (`--contre`) |
| `apm_icones.py` | lit un `*.assets` Unity : Texture2D, `streamData`, décodage RGBA32 / RGB24 / BC1 / BC3, sortie PNG sans dépendance |
| `apm_sons.py` | sort les 19 sons distincts du système de paiement |
| `apm_lancer.py` | lance les deux applications Unity de l'APM **hors ligne**, dans un bac à sable, en relevant leurs connexions |
| `emplacements.py` | quels emplacements de décor sont **libres**, et pourquoi les autres ne le sont pas. `--pourquoi <code>` étiquette les raisons : `descripteur`/`grille`/`apercu` (le moteur s'en sert) contre `lanceur <nom>` (une simple réservation) |
| `tex_db.py` | lit et réécrit `tex_db.bin`. Sa table étant **triée**, l'ajout est une INSERTION, pas un append. `--libres`, `--montrer <motif>` |
| `obj_db.py` | lit et **réécrit** `obj_db.bin` : deux pots de chaînes gardés en octets, ajout en fin. `--essai` prouve l'aller-retour à l'octet près ; `--libres` les identifiants d'objset disponibles |
| `a3d_db.py` | lit et écrit `auth_3d_db.bin`, un dictionnaire `clé=valeur` **trié comme des chaînes**. `--essai` prouve l'aller-retour à l'octet près ; `--ajouter <CAT> --depuis <CAT>` déclare l'animation d'un décor neuf |
| `refs_plage.py` | les références à une **PLAGE** d'adresses, en un seul balayage — à passer avant de déplacer une table. Rapporte le champ `disp32`, pas l'adresse d'instruction |
| `verifier_decors_table.py` | contrôle du déplacement des deux tables : octets, sites, relocations une par une, rebasage simulé |
| `pister_relocations.py` | pose le témoin relogeable et le relit **dans le processus vivant** — lanceur `essai_relocations.cmd` |
| `pe_sections.py` | greffe une section **et reconstruit la table de relocations** : un pointeur absolu y devient légitime. `--essai` = auto-contrôle relu par `pefile` |
| `decor_neuf.py` | pose ou retire tout ce qu'un décor **vraiment ajouté** demande côté fichiers : les neuf pièces, `obj_db`, `auth_3d_db`, et les deux seuls noms à masquer |
| `controle_decor_neuf.py` | contrôle avant vol d'un décor ajouté : descripteur, fichiers, bases, et **les objets demandés existent-ils dans l'archive posée** |
| `verifier_lanceurs.py` | **contrôle les 62 lanceurs** : caractères de contrôle parasites, fins de ligne, fichiers cités, et la ligne de patch réellement exécutée : fins de ligne, fichiers cités, et la ligne de patch réellement exécutée. À lancer après toute retouche d'un `.cmd` |
| `importer_decor.py` | pose ou retire le jeu complet d'un décor étranger. `--vers <code>` **ajoute** au lieu de remplacer (code à **trois lettres** obligatoirement : la substitution dans l'en-tête du `FArC` est en place) ; `--pour <lanceur.cmd>` lève la réservation que ce lanceur s'est faite à lui-même |
| `decomp.py` | **le décompilateur** : `py -3 tools/decomp.py 0x1800F9C60` sort le C. Ghidra 12.1.2 est installé (hors `Program Files`), projet `ghidra/vf5fs_apm3` déjà analysé (107 s). Chaque adresse est cherchée **dans** sa fonction |
| `par_masquer.py` | masque un nom dans l'index du `.par` (borné au pot de noms — et la borne est passée à `find`, sinon on balaie 3,99 Go) |
| `par_ecrire.py` | **écrit un fichier DANS le `.par`** : ajout en fin d'archive, entrée d'index repointée, entrée d'origine gardée pour `--rendre`. Indispensable pour `obj_db`, que le masquage ne cache pas |
| `farc.py` | lit **et écrit** les archives `FArc`/`FArC`. `ecrire_farc()` produit du brut : c'est ce qui permet de renommer les objets d'un décor importé |
| `pister_objset.py` | le moteur connaît-il notre objset ? Lit son vecteur trié dans le processus vivant, **sans navigation** |
| `pister_objset_pret.py` | compare l'enregistrement d'un objset au nôtre, champ par champ, quand l'état 4 s'éternise |
| `pister_objdb.py` | d'où viennent les octets d'`obj_db` : chemin composé, adresse rendue, nombre de jeux |
| `farc.py`, `stfs.py`, `psarc.py` | archives : FArc/FArC, paquets Xbox 360, PSARC |
| `sfd.py`, `usm.py`, `usm_mux.py` | films : lecteur Sofdec1, lecteur Sofdec2, **multiplexeur** |
| `sfd_inventaire.py` | image, cadence et son d'un `.sfd` en quelques secondes |

**Après `construire_stub.cmd`, remettre `apm_entrees.txt` en jeu manuel.** Et
`front = 10` — la fenêtre de `Input_isOnNow` doit rester plus courte qu'une
trame (16,7 ms), sinon chaque appui vaut double.

---

## 6. Les cavernes

Il n'y a pas de section libre : on greffe dans du code mort.

| caverne | taille | état |
|---|---|---|
| `.text` fin `0x18034575C`–`0x180345800` | 164 o | ~150 utilisés |
| raccourci désactivé `0x1801A7C89`–`0x1801A7CDB` | 82 o | 65 utilisés |
| « How to Play » mort `0x1801A703D`–`0x1801A707D` | 65 o | Arcade + Score Attack |
| « Credits » mort `0x1801A71D8`–`0x1801A71FC` | 37 o | License Challenge |

Les deux derniers ne sont morts **que si `--options-sans-howto` est appliqué**.

### Il y a en fait de la place à volonté : les bourrages `int3` (2026-09-06)

MSVC aligne ses fonctions à 16 octets et remplit l'écart avec `0xCC`. Le
moteur en compte **1431 plages d'au moins 14 octets**, dont plusieurs de 21.
Ce ne sont pas des octets « probablement libres » : on peut le **prouver**, en
vérifiant que la plage ne tombe dans aucune des 13 661 entrées de `.pdata`, et
qu'elle finit sur une frontière à 16.

Le balayage tient en dix lignes ; il est décrit au-dessus de `--options-tips`
dans `tools/patch_moteur.py`.

Déjà prises : `0x1802786EB` (libellé Tips), `0x18027718B` (garde Tips +
la chaîne), `0x1802758DB` (légende du bas). Il en reste des centaines.

### La collision qui a cassé License Challenge (corrigée le 2026-09-06)

`--sp-lancer` loge le lancement de License Challenge en `0x1801A71D8`.
`--legende-sousmenu` y logeait aussi sa caverne. Les deux sont dans
`console.cmd`, la légende passe en dernier : elle écrasait le lancement, et
`0x1801DDE49` sautait dans le code de la légende. **License Challenge était
cassé, sans un seul message.**

Le contrôle ne pouvait pas le voir : chaque correctif vérifie ses octets
attendus dans `.origine`, **jamais dans le fichier en cours d'écriture**. Deux
options peuvent donc se disputer une caverne en silence.

Deux corrections : la légende est partie dans un bourrage `int3`, et
`patch_moteur.py` tient désormais un **journal des octets écrits** qui refuse
toute collision (`_poser`). Une reprise volontaire de site se déclare
(`reprise=True`) ; tout le reste s'arrête.

---

## 7. Où lire

| document | sujet |
|---|---|
| `REPRISE.md` | le journal du chantier, séance par séance |
| `analysis/reseau_allnet.md` | **le netcode : clé AES, serveur minimal, §10** |
| `analysis/reseau_transport.md` | STUN/TURN, paquets, sockets, les deux fils |
| `analysis/reseau_machine.md` | la machine à états et son pilote |
| `analysis/mode_de_jeu.md` | le mode de jeu, ses cinq setters, et la mesure §13 |
| `analysis/customize_0x299.md` | Customize : chemin intact, aucun maillon manquant |
| `analysis/menu_console.md` | le menu console, entrée par entrée |
| `analysis/machine_console.md` | les deux tables : dix modes, 55 sous-états |
| `analysis/polices_et_pictos.md` | **les deux polices, les planches TXP, les boutons de manette** |
| `analysis/decors.md` | **le code des décors** : sélection, chargement, les 41 descripteurs |
| `analysis/greffe_relocations.md` | **greffer une section AVEC ses relocations** — la clé de voûte du vrai ajout de décors |
| `analysis/auth_3d_db.md` | **la base des jeux d'animation, en TEXTE** : catégories, uids, et comment en ajouter |
| `analysis/obj_db.md` | **les jeux d'objets** : la carte complète, l'empaquetage `(objset << 16) \| rang`, et comment en ajouter |
| `analysis/tex_db.md` | **les textures** : table TRIÉE, 910 plages d'identifiants libres, et pourquoi un décor importé n'y touche pas |
| `analysis/ajouter_un_decor.md` | ajouter un décor : les emplacements d'essai, §6 la grille |
| `analysis/import_decors.md` | importer un décor d'une autre génération, §8 la mesure qui débloque |
| `analysis/films_usm.md` | **SFD → USM sans perte**, le format, l'AIX, les films Xbox 360 |
| `analysis/knockout_trial.md` | KO Trial, présent sous le nom `Special Sparring` |
| `analysis/interface_apm3.md` | **le système APM3** : la surcouche, ses 109 textures, ses 19 sons, ses 233 messages d'erreur, son réseau — et pourquoi `game.bat` ne doit jamais tourner |
| `analysis/comparaison_builds.md` | **APM3 contre Yakuza 6** : mêmes données, un seul descripteur différent, le bouchonnage expliqué |
| `analysis/rtti_apm3.txt` | les 534 vtables nommées |
| `analysis/decomp_*.c` | le C sorti de Ghidra le 2026-09-10 : chargeur d objsets, résolveur, barrière de l état 3, tables d effets |
| `analysis/rtti_yakuza6.txt` | les 314 vtables du build Yakuza 6 |

Publié : **https://github.com/penpenlovesrei-dotcom/Virtua_Fighter_5_Final_Showdown_APM3**
(analyse et outils seulement, aucune donnée de jeu). Dépôt local :
`C:\Users\frede\Desktop\VF5RE-public`.

---

## 8. Comment travailler avec Frédéric

- Il juge **sur l'image**. Livrer une capture ou un lanceur, pas un verdict.
- **Toujours un lanceur `.cmd`**, double-cliquable, jamais une ligne à recopier.
- Ne pas proposer d'arrêter, ni demander « on continue ? ». Rendre la main
  seulement pour une vraie question ou un essai à faire.
- Une observation de sa part est un **point de départ d'analyse**, pas une
  valeur à régler à la vue.
- Quand il signale un défaut après une séance de correctifs, **relire ses
  propres patchs avant de désassembler le moteur**.
- **Les sous-agents coûtent très cher.** Sur la session du 2026-09-05, treize
  agents ont consommé 32 M de jetons — les deux tiers du total — dont neuf
  n'étaient que des relances après coupure de quota. N'en lancer que s'il le
  demande, un seul à la fois, et leur imposer d'écrire leur rapport **au fil de
  l'eau** : trois rapports ont été perdus faute de ça.
- **Répondre court.** Une question simple appelle une réponse simple : « ta
  réponse est bien trop longue pour une question simple » (2026-09-07). Le
  détail va dans les `.md`, pas dans le fil.
- **Instrumenter ce qu'on livre.** Il demande de lui-même « tu as instrumenté
  pour dépister les erreurs ? ». Un livrable qui peut échouer de plusieurs
  façons se livre avec l'outil qui les sépare.
- **« Ne me fais plus tester pour rien. »** (2026-09-08, après six essais
  d'affichage). Il compte les essais et les limite lui-même : « fait, et c'est
  la dernière fois. » Un essai se demande quand le code a été lu, pas pour
  départager deux hypothèses qu'un désassemblage tranche.
- **Ne pas tâtonner : désassembler.** Sa formule. Face à un comportement
  inexpliqué, chercher la **borne** ou la **table** dans le code plutôt que de
  régler une valeur « raisonnable ». Le plantage du 2026-09-08 tenait à une
  taille écrite en clair, `mov ecx, 0x838`.
- Quand il dit qu'il ne lira pas pendant trente minutes, **travailler sans
  s'arrêter** et livrer un état complet à son retour.


---

## 9. Le multiplexeur USM — LIVRÉ le 2026-09-08

Ce chantier était « ouvert, rien d'écrit ». Il est fait, et la prémisse qui le
rendait plausible s'est vérifiée : le flux vidéo d'un `.usm` est du **MPEG-1
standard** — aucune extension MPEG-2 `00 00 01 B5` dans `vf5adv.usm`. Donc
`mpeg_codec = 1` (« Sofdec.Prime ») **est** ce qu'un `.sfd` transporte déjà, et
`audio_codec = 2` est de l'ADX. **Il n'y a rien à convertir : on remballe.**

Trois inconnues annoncées à l'époque, toutes levées **par la mesure sur les
films du jeu**, jamais par supposition :

* structure des blocs `@SFV` / `@SFA` : **une image par morceau vidéo** (7304
  morceaux pour `total_frames = 7304`), **50 blocs ADX = 1600 échantillons**
  par morceau audio, le premier ne portant que l'en-tête ADX ;
* `VIDEO_SEEKINFO.ofs_byte` est l'**offset absolu dans le fichier**, une ligne
  par début de GOP — vérifié en comparant la table aux positions réelles ;
* `max_picture_size` et `metadata_size` : le message
  `E2010122901M: Playback work memory…` n'est jamais apparu, mais **rien n'a
  encore été joué dans le jeu** — c'est le seul essai qui reste.

Preuve de non-perte : les flux ressortis du `.usm` produit ont le **même MD5**
que ceux du `.sfd` d'origine, vidéo et audio, sur des films de 54 à 232 Mo. Le
multipiste **AIX** (morceaux `AIXP` étiquetés du numéro de flux) est déplié en
autant de voies `@SFA` — `vf5verBadv` sort en quatre voies, les quatre
identiques à la source.

Six films Xbox 360 sont extraits dans `extracted/sfd_x360/` : les cinq de VF5
vanilla, plus le `vf5end.sfd` du paquet STFS de Final Showdown (2,05 Go, ouvert
par `tools/stfs.py`, qui ne contient qu'un seul film et **aucun `.usm`**). Cinq
des six sont en **1280×720 à 60 images/s**, la définition exacte des films
d'APM3.

---

## Chantiers ouverts, à reprendre plus tard

### 1. Le VRAI ajout de décors — UN VALIDÉ, DIX-NEUF POSÉS

**Le premier décor vraiment ajouté est FINI** : géométrie, flammes et
barrières, vues à l'écran le 2026-09-10 (`tools\dojo_5r_repli.cmd`).

**Et les dix-huit autres sont posés et patchés** (`tools\decors_5r.cmd`,
indices 42 à 60), contrôlés dans la DLL — **pas encore vus à l'écran**. C'est
l'essai qui attend. Journal (49), `analysis/decors.md` §18.

Ce qui est **fait et validé à l'écran** :

| | doc |
|---|---|
| une section greffée porte ses **relocations** | `analysis/greffe_relocations.md` |
| **six** tables indexées par le décor déménagées dans `.decors`, 744 relocations | `analysis/decors.md` §17 |
| la table à **44 décors**, sept bornes levées | `analysis/ajouter_un_decor.md` §7 |
| les **trois bases** lues et réécrites, aller-retour à l'octet près | `auth_3d_db.md`, `obj_db.md`, `tex_db.md` |
| le **décor ajouté, indice 42, S'AFFICHE dans le DOJO** | journal (46) |
| ses **flammes** | journal (46) |
| ses **barrières de ring** | journal (47) et (48) |

Ce qui **reste** :

* ~~voir ses barrières~~ — **fait, 2026-09-10.** Il aura fallu deux causes :
  les trois blocs du mur nommaient l'objset du modèle (47), et surtout
  `EFFECT_WALL` n'était jamais créée (48) ;
* ~~les plantages~~ — **TROUVÉS ET CORRIGÉS le 2026-09-10**, par
  `tools\plantage_5r.cmd` : `VAR_NUM`, le numéro courant de chaque anneau,
  était déclaré **en dur à quatre entrées** et il y a vingt anneaux. Au-delà du
  quatrième il lisait **et écrivait** dans `VAR_RANG` puis dans le descripteur
  de texte de la greffe. Il est dérivé maintenant, et
  `verifier_disposition()` refuse tout recouvrement. **À revoir à l'écran** ;
* **voir les dix-neuf à l'écran** (`tools\decors_5r.cmd`) : la barre espace
  sur chaque case de la grille ;
* **`du1`..`du4` de VF5 R ne sont pas ajoutés** : VF5 R range la scène des
  quatre décors de Dural sous **un seul** nom, `STGDUR.farc`. La correspondance
  reste à établir. `du5` n'existe pas dans VF5 R ;
* ~~les autres tâches d'effet ne sont pas ouvertes~~ — **répondu le 2026-09-10**
  (journal 48). Elles n'ont aucune borne à lever : il suffit que le `+0x20` de
  l'entrée du décor dans `0x18034D570` les demande, et cette table dit déjà
  lesquelles chaque décor demande (4 = WALL RIPPLE SPLASH WET_CLOTH,
  16 = WALL SNOW BREATH, 13 = WALL THUNDER FOG_ANIM…). Un décor ajouté clone
  celle du modèle ;
* **l'aperçu de la case.** Le lecteur (`0x180175010`) ne connaît que 26 entrées
  et **efface les trois couches AET** quand il ne trouve pas. Pour l'étendre :
  `lea rcx, [rsp+0x50]` en `0x180175005` fait **cinq octets**, assez pour un
  `jmp rel32` vers une caverne qui pose `lea rcx, [rip+d]` — la construction
  sur la pile devient morte, et la borne `0x1a` (`0x18017502A`) suit ;
* **l'ambiance sonore** du décor ajouté est celle de `are` : la liste
  d'association `0x180408850` a une valeur par défaut, et elle est collée à ses
  chaînes, donc lui ajouter une entrée demande de la déplacer. Journal (40) ;
* **une base `obj_db` exacte** : 171 objets déclarés pour 119 présents dans
  l'archive de 2008. Des noms que rien ne charge, mais c'est faux ;
* ~~la table `0x18054E180`~~ : **tranchée le 2026-09-10, elle est MORTE.** 249
  entrées `{chemin, taille d'en-tête}` — aucune référence de code, et le qword
  de son adresse n'apparaît nulle part dans l'image. Ce n'était pas le
  résolveur ;
* **la septième borne ne se lèvera pas** : les compteurs de parties sont un
  tableau de 41 entrées **dans une structure**, pas une table (§7.5 de
  `ajouter_un_decor.md`). Les décors ajoutés n'auront pas de statistiques.

### 2. La manette 2 — SIGNALÉ LE 2026-09-09, non diagnostiqué

Frédéric : « la manette 2 est très mal gérée, je n'arrive plus à lancer le mode
versus ». OFFLINE VERSUS à deux était **validé le 2026-09-05** (clavier joueur
1, manette joueur 2, `--joueur2`, trois octets qui rebranchent un lecteur
d'entrées amputé). C'est donc soit une régression, soit un défaut jamais vu.

**Rien n'a été mesuré.** La première question à lui poser : la manette ne fait
*rien*, produit des entrées *fantômes*, ou pilote le *joueur 1* ? Les trois
demandent des mesures différentes.

C'est ce défaut qui oblige à passer par le DOJO pour voir un décor, donc il
n'est pas secondaire.

### 3. Les autres, inchangés

* **Trois variantes de Dural manquaient** : NIGHT, DAY, SUNSET. **ver.B les
  a** (2026-09-11) : ses quatre ciels de Dural sont un coucher de soleil, un
  jour, un orage et une nuit étoilée — ajoutés par `decors_vf5.cmd`, libellés
  provisoires « VIRTUA FIGHTER 5 - 1..4 », à nommer à l'écran.
* **La quatrième ligne de la grille est REFUSÉE.** `--grille-ajout` a été
  construite puis retirée, et le patcheur la refuse. Ne pas la reproposer :
  une case reste une case, la barre espace fait le reste.
* **Aucun film converti n'a été joué dans le jeu.** `rom/movie` est lu sur le
  disque et non dans le `.par` : un `.usm` se dépose librement.
* **Le décor de nuit de Dural.** La capture de 2007 est le SANCTUARY —
  l'architecture de `du1`, dont le **ciel** a changé entre VF5 et Final
  Showdown. Deux voies : remplacer la texture de `stgdu1_sky`, ou importer le
  `stgdur` de ver.B (35,7 Mo). **Cette seconde voie est maintenant simple** :
  c'est un décor ajouté de plus, avec `decor_neuf.py`.
* **L'habillage de KNOCK OUT TRIAL** : à peine commencé. L'ELF Lindbergh à
  désassembler est `extracted/LIND_FS/sel/vf5` (11,8 Mo, x86-32).
* **Le réseau** : il manque un STUN/TURN sur 3478 (§2).
