# Le build APM3 EST le build console

Question du 2026-09-03 : puisque la version APM3 semble liee a la PS3, peut-on
rapatrier les menus, les modes et Dural depuis la PS3 ? La reponse tient en deux
constats opposes : **la parente est bien plus forte qu'un « semble »**, et
**il n'y a rien a rapatrier**.

---

## 1. La machine a etats enumere tout le parcours console

`tools/tracer_etats.py` lit les deux tables de noms du binaire APM3. Sur les
**56 sous-etats**, seuls **sept** appartiennent a la borne (48 a 54). Les
quarante-huit autres sont le jeu console :

| plage | contenu |
|---|---|
| 3 a 6 | `CS_TITLE`, `CS_SIGNIN`, `CS_AUTOLOAD`, `CS_DEMO` |
| 7 a 20 | `LOGO`, `RATING`, `DEMO`, `TITLE`, `TITLE_TV`, `SELECTOR`, `MODE_SELECTOR`, `VS`, `GAMEOVER`, et les quatre etats `*_TERMINAL` |
| **21 a 35** | **quinze etats `DATA_TEST_*`** : `MISC`, `OBJ`, `STG`, `MOT`, `COLLISION`, `SPR`, `AET`, `AUTH_3D`, `CHR`, `ITEM`, `PERF`, `TNMT`, `BATTLE`, `KOTSP_SS` |
| 36 a 41 | `MENU_MAIN`, `CS_TERM_CUSTOMIZE`, `CS_TERM_REPLAY_PLAY`, `CS_TERM_LAST_PLAY`, `CS_TERM_CLIP_PLAY`, `CS_TRAINING` |
| 42 a 47 | les sept etats `ONLINE_*` |
| 48 a 54 | `APM3_*` -- la borne |

Les etats de tete disent la meme chose : `MENU`, `CS_TERM`, `CS_TRAINING`,
`ONLINE` cotoient `APM3` et `APM3_TESTMODE`.

Confiance : **CONFIRMED**.

## 2. Et le code de ces menus est compile dedans

Les noms d'etats ne prouvent rien a eux seuls -- une table de noms survit a la
suppression du code qu'elle nomme. Le controle est ailleurs : **les chaines de
menu console sont referencees par du code**, comptees par motif de deplacement
rip-relatif :

| chaine | references |
|---|---:|
| `ARCADE MENU` | 2 (`0x1801DDF95`, `0x1801E3E00`) |
| `VERSUS MENU` | 2 (`0x1801DDFC3`, `0x1801E3D0B`) |
| `SCOREATTACK MENU` | 2 (`0x1801DDD7A`, `0x1801E2FEC`) |
| `LICENCECHALLENGE MENU` | 2 (`0x1801DDDB6`, `0x1801E3018`) |
| `MAIN MENU` | 1 (`0x1801E46D7`) |
| `p_menutxt_PS3_lt` | 1 (`0x1801E0E7B`) |
| `UNLOCK_DURAL` | 1 (`0x1801E349E`) |

Deux voisinages nets, `0x1801DDxxx` et `0x1801E2xxx`-`0x1801E4xxx` : le code des
menus console **n'a pas ete retire**, il n'est pas emprunte.

Confiance : **SUPPORTED**. Un site d'appel n'est pas un menu qui s'affiche ; il
faudra le voir a l'ecran.

### Fausse piste ecartee

Une table de 56 pointeurs a `0x1803465C8` a l'air d'etre le repartiteur des
sous-etats. Elle ne l'est pas : ses quatre premieres entrees (`0x64148E`…) ne
sont meme pas des adresses valides, et la plupart des cibles ne sont pas des
debuts de fonction au sens de `.pdata`. Une table reguliere n'est pas une table
identifiee -- le repartiteur reste a trouver.

---

## 3. Ce qu'on ne peut pas faire

**Rapatrier du code depuis la PS3 est impossible.** Le binaire PS3 est du
PowerPC (Cell PPU), le binaire APM3 du x86-64. Aucune fonction ne se transporte
de l'un a l'autre. Tout ce qu'on obtiendra viendra de ce qui est **deja dans le
binaire APM3**, ou devra etre reecrit.

Heureusement, c'est justement ce que dit la section 2 : il n'y a rien a
rapatrier, parce que c'est deja la.

---

## 4. Ce qui va coincer

Le travail n'est donc pas un portage mais une **atteignabilite** : amener la
machine a etats sur un etat qu'elle n'emprunte jamais. C'est exactement la
manoeuvre qui a ouvert le mode DOJO (`--devier 50 52`). Trois obstacles connus :

1. **Les predicats neutralises.** Le garde qui commande `UNLOCK_DURAL` consulte
   `0x180007450`, qui est `xor al, al ; ret` -- **il rend toujours zero**. Ce
   build ne supprime pas les conditions console, il les court-circuite. Certaines
   devront etre forcees ; d'autres menent a du code dont les donnees ne sont pas
   livrees.
2. **Les ressources.** Chaque etat veut ses planches d'interface. `p_menutxt_PS3_lt`
   est un nom de scene : reste a verifier qu'il est present dans les `.farc` du
   dump APM3, et non seulement dans celui de la PS3.
3. **Les arriere-plans.** `CS_SIGNIN`, `CS_AUTOLOAD`, les sept `ONLINE_*` et les
   quatre `CS_TERM_*` supposent une sauvegarde de profil, un serveur, un
   terminal. Rien de tout cela n'existe ici -- et notre `apm.dll` est un bouchon.

## 5. L'ordre de difficulte

| cible | pourquoi |
|---|---|
| **`DATA_TEST_*` (21 a 35)** | le plus prometteur : un visualiseur de developpement, sans reseau ni sauvegarde. `DATA_TEST_CHR` et `DATA_TEST_MOT` montreraient **Dural directement**, sans passer par la grille de selection. |
| `CS_TRAINING` (41), `MENU_MAIN` (36) | code present, ressources a verifier |
| `CS_TERM_*` (37 a 40) | supposent un terminal et une sauvegarde |
| `ONLINE_*` (42 a 47) | supposent un serveur ; sans espoir hors ligne |

## 6. Dural n'a besoin de rien de tout cela

A retenir : **Dural ne demande aucun apport de la PS3.** Ses donnees sont
completes dans le dump APM3 (726 roles sur 726, `mothead_DUR.bin`,
`ctrl_DUR.bin`), et l'accesseur `0x18012CA90` accepte l'indice 20 -- voir
`analysis/dural.md`. Ce qui manque n'est pas une donnee, c'est **un moyen de le
choisir**. Un probleme d'interface, pas de contenu.

---

## 7. « Terminal » = la personnalisation des personnages

Precision de Frederic, qui recadre toute la lecture des etats `*_TERMINAL` et
`CS_TERM_*` : le **terminal** est le poste de personnalisation, distinct de la
borne de jeu. `CS_TERM` est donc la transposition console de ce poste, et ses
quatre sous-etats se lisent alors sans ambiguite :

| sous-etat | role |
|---:|---|
| 37 `CS_TERM_CUSTOMIZE` | **la personnalisation** |
| 38 `CS_TERM_REPLAY_PLAY` | relecture des combats |
| 39 `CS_TERM_LAST_PLAY` | la derniere partie |
| 40 `CS_TERM_CLIP_PLAY` | les clips |

Et les quatre etats `*_TERMINAL` (13 a 16 : `LOGO`, `MANUAL`, `TITLE`, `LOOP`)
sont l'attente du poste lui-meme.

### Le dump APM3 porte tout le materiel du terminal

- **le son** : `se_terminal.csb` (18,4 Mo), `se_terminal_fb.csb` (14,9 Mo), et
  toute la serie `se_tv_*` (VF.TV) ;
- **les planches d'interface** : `aet_t_item`, `aet_t_itemcmn`, `aet_t_itemcol`,
  `aet_t_itemex`, `aet_t_itemwin`, `aet_t_capsule`, `aet_t_pupil`, `aet_t_sel`,
  plus les `aet_l_*` du panneau d'informations ;
- **les sprites** : `spr_t_item*.farc`, et **une planche par personnage**,
  `spr_t_itmaki.farc` … `spr_t_itmwol.farc`.

### Ou Dural s'arrete

Ces planches par personnage sont **dix-neuf**. Il n'y a **pas de
`spr_t_itmdur.farc`** — ni dans APM3, ni dans le dump R.E.V.O.

Or ses articles, eux, existent : `dur_itm.csv` porte ses quatre finitions de
corps (argent, or, verre, platre). **La donnee est la, l'icone ne l'est pas.**

C'est la meme forme d'absence que pour la grille de selection : Dural est complet
partout ou le moteur le lit, et absent partout ou l'interface le montre. Deux
manques d'interface, aucun manque de contenu.

Confiance : **CONFIRMED** (inventaires `analysis/inventory/APM3_FS.csv` et
`PC_REVO.csv`, et `extracted/csv_utf8/APM3_FS/chritm_tbl/`).

---

## 8. Ce qu'on a reellement de la PS3 : presque rien

Il faut le dire clairement, parce que cela ferme la question du « rapatriement » :

| element | etat |
|---|---|
| `EBOOT.BIN` (3,8 Mo) | **conteneur SCE/SELF chiffre**, entropie **8,000** — zero chaine lisible. Illisible en l'etat. |
| donnees extraites | **46 fichiers**, tous `rom/rob/mot_*.farc` (les archives de mouvements). Rien d'autre. |
| le reste du `.pkg` (2,0 Go) | non deballe |

Donc, aujourd'hui : **le code PS3 est une boite fermee, et aucune ressource
d'interface PS3 n'est extraite**. Meme si le portage PowerPC vers x86-64 etait
concevable — il ne l'est pas — il n'y aurait rien a copier.

Le materiel des menus console est a chercher **dans le dump APM3**, ou il est,
et non dans la PS3, ou il n'est pas accessible.
