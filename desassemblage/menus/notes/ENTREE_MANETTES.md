# L'entrée de REVO : les manettes se posent DANS LE BLOC

Lu le 2026-11-07 (SS 338.13), entièrement dans les décompilations de ce
dossier. **Rien ici n'est du code à compiler** : c'est une lecture du module.

## La disposition, mesurée

`FUN_18027A3F0(&DAT_180795950)` — appelée à chaque image par
[`FUN_1801B19A0`](FUN_1801b19a0.c) — recopie l'état des manettes depuis
**notre bloc** vers l'enregistrement interne du module :

```c
for (port = 0; port < 2; port++) {
    lVar9 = port * 0x54;                 // l'enregistrement du module (795950)
    lVar6 = port * 400;                  // 400 = 0x190 : LE PAS DU PAD
    lVar1 = DAT_180c8df28;               // NOTRE BLOC (celui qui porte +0x1FF08)
    *(byte*)(lVar9 + param_1) = *(byte*)(lVar6 + 0x108 + DAT_180c8df28);
    uVar3  = *(uint* )(lVar6 + 0x20 + lVar1);
    iVar11 = ROUND( *(float*)(lVar6 + 0x30 + lVar1) * 32768.0);
    iVar10 = ROUND(-*(float*)(lVar6 + 0x34 + lVar1) * 32768.0);
    ...
}
```

Donc, **relativement au bloc** :

| offset | champ | type |
|---|---|---|
| `+0x20 + port*0x190` | les boutons | `uint32` |
| `+0x30 + port*0x190` | axe X | `float`, −1..1, ×32768 |
| `+0x34 + port*0x190` | axe Y | `float`, **signe inversé** |
| `+0x108 + port*0x190` | **la manette est branchée** | `byte` |

soit `+0x108` pour le port 0 et `+0x298` pour le port 1.

**Recoupement indépendant** : l'hôte Lost Judgment de biggestsonicfan
(`FS REVO\reference\YAMP-biggestsonicfan\source\vf5fs\LJ\VF5FS.cpp`) écrit
« INPUT lives at +0x20: pad[2], **0x190 stride** », des axes en `float` mis à
l'échelle ±32767 avec l'axe Y inversé, et pose `m_port`, `m_user_id`,
`m_is_connected`. Les deux lectures concordent — et elles n'ont pas la même
source.

## Pourquoi ça commande l'attract

[`FUN_1801B2280`](FUN_1801b2280.c) est **la seule sortie de CS_DEMO qui ne
demande pas d'appui** :

```c
if ((&DAT_180795950)[port * 0x54] != '\0') return port;   // manette PRÉSENTE
return -1;
```

et cet octet est précisément celui recopié depuis `bloc+0x108`. Il ne s'agit
donc **pas** d'un bouton tenu : le module veut une manette **branchée**.
[`FUN_1801B2390`](FUN_1801b2390.c), lui, lit les deux séparément — présence
(`DAT_180795950`) et boutons (`DAT_180795960 & 0x1FF`).

## Deux autres chemins d'entrée, distincts

* **commande 364 (`0x16c`)** — [`FUN_1801B2CC0`](Entree_DecoderRolesDepuis364.c) : structure
  de 32 octets, `+0x00` identifiant (entrée), `+0x04` masque brut des boutons,
  `+0x08` présence. Elle garnit `DAT_180795A78 + port*0xD8`, **pas**
  l'enregistrement `795950`. Ce sont deux blocs différents.
* **commande 422 (`0x1a6`)** — [`FUN_1801B1A60`](FUN_1801b1a60.c) (arguments
  4 puis 0x1A) et [`FUN_1801B3C10`](FUN_1801b3c10.c) (argument 0x13).
  L'initialisation enregistre 12 à 13 rappels par `FUN_180081FE0(id, fn, 0, 0)`
  et nomme un objet **`"DEVICE CONNECTION"`**
  ([`FUN_1801B26B0`](FUN_1801b26b0.c)).

`_DAT_180795C10 = 0x101` : les **deux emplacements sont activés** dès
l'initialisation, et `(&DAT_180795AC8)[slot*0x36]` donne l'indice du
périphérique de l'emplacement.

## État de la mesure

`CONFIRMÉ` : les quatre champs, leurs offsets, le pas de 0x190, et le fait que
`FUN_1801B2280` lise la présence et non un bouton.
`NON RÉSOLU` : poser `+0x108 = 1` et `+0x298 = 1` (`VF5_MANETTE=2`, SS 338.13)
n'a pas fait sortir CS_DEMO de sa phase 1. La sonde de l'hôte n'évalue que
`FUN_1801B2390` et ne dit rien de `FUN_1801B2280` : **elle est à réparer avant
d'en tirer une conclusion.**


---

## SS 419.52 -- LES TROIS FONCTIONS D ENTREE SONT MORTES QUAND `+0x1FF08` EST NUL

Mesure du 8 nov 2026. `FUN_1801b2390`, `FUN_1802cb570` et `FUN_1802cb830`
commencent TOUTES par le meme test :

```
CMP  qword [RCX + 0x1ff08], 0
JZ   <sortie>                     ; les deux portes : XOR AL,AL = rend 0
```

Notre hote met `bloc+0x1FF08` a **NUL pendant tout CS_TITLE**
(`vf5fs_host.cpp`, `parTitre = (g_titreAet != 0) && (scTA == 5)`, defaut 1).
Donc pendant l ecran-titre :

- la porte 212 rend 0 **sans rien poster** -> la 225 n est jamais demandee ;
- `FUN_1801b2280`, la vraie lecture d entree, est **inatteignable** ;
- dans `FUN_1801b2390` le `CALL` de la cmd 242 est saute, son octet reste 0.

**PREUVE PAR LES DEUX COURSES** (journaux `host_log_s419_51_attribution.txt`
et celui du SS 419.52) : avec `VF5_TITRE_AET=1`, **0 appel** de la cmd 225 en
sous-etat 5 ; avec `VF5_TITRE_AET=0`, **au moins 8 appels** en sous-etat 5
(le journal a imprime 12 lignes = son PLAFOND exact, et la ligne du total
etait eteinte : le compte vrai n est PAS mesure, seul le passage de 0 a
non-zero l est). Meme code,
meme course, une variable.

### LA SORTIE SURVIVANTE DE `FUN_1801b2390` : UN BOUTON TENU

```
IMUL RCX, RDX, 0x54
LEA  RAX, [0x180795960]      ; table des BOUTONS (0x795950 = la PRESENCE)
MOV  EAX, [RCX + RAX]
TEST EBX, EAX                ; EBX = 0x1FF  (ou 8 si [0x180c8de1a] != 0)
JNZ  <rend le port = SORTIE>
```

Elle ne depend PAS du repartiteur. Mesure : `boutons [0x795960] p0=0x00000000`
-- l hote ecrit la presence (`VF5_MANETTE`), **jamais les boutons**.

### `FUN_1801b2280`, la vraie lecture

Avec le port 0 (`FUN_18000ba10` rend 0), elle rend **0 = la sortie si et
seulement si** l octet de `0x180795950 + port*0x54` est non nul ; sinon -1.
`VF5_MANETTE=2` le met a 1 : mesure 38/38.

## SS 419.70 — NOTRE PAD EST INCOMPLET : 4 champs écrits sur 14

Degré : **CONFIRMÉ** pour la disposition et pour ce que les hôtes de
référence écrivent (deux sources indépendantes, avec `static_assert`).
**SPÉCULATIF** pour « c'est la cause » : rien n'a encore été mesuré à
l'exécution.

Trouvé **en lisant YAMP**, pas en sondant.

### La structure complète — `pxd::csl_pad` / `pxd::lj_pad_t`

`FS REVO\chantier_yamp_revo\source\pxd\LJ\sl.h` l. 24-46 et
`FS GOG\yamp_son\source\Y6\sl.h` l. 18-40 la donnent **mot pour mot la
même**, avec `static_assert(sizeof(csl_pad) == 0x170)`,
`static_assert(sizeof(lj_pad_t) == 0x190)`,
`static_assert(offsetof(lj_pad_t, m_buttons) == 0xA0)` et
`static_assert(offsetof(lj_pad_t, m_port) == 0xE0)`.

| champ | dans le pad | **dans notre bloc** (port 0) | l'hôte l'écrit-il ? |
|---|---|---|---|
| `m_now` | `+0x00` | `+0x20` | **oui** |
| `m_push` | `+0x04` | `+0x24` | **NON** |
| `m_pull` | `+0x08` | `+0x28` | **NON** |
| `m_prev` | `+0x0C` | `+0x2C` | **NON** |
| `m_x1` | `+0x10` | `+0x30` | **oui** |
| `m_y1` | `+0x14` | `+0x34` | **oui** |
| `m_x2` | `+0x18` | `+0x38` | non |
| `m_y2` | `+0x1C` | `+0x3C` | non |
| `m_button_frame[32]` | `+0x20` | `+0x40..+0xBF` | **NON** |
| `m_buttons[32]` | `+0xA0` | `+0xC0..+0xDF` | **NON** |
| `m_prev_buttons[32]` | `+0xC0` | `+0xE0..+0xFF` | **NON** |
| `m_port` | `+0xE0` | `+0x100` | non |
| `m_user_id` | `+0xE4` | `+0x104` | non |
| `m_is_connected` | `+0xE8` | `+0x108` | **oui** |
| `m_is_remote` | `+0xE9` | `+0x109` | non |

**Nos quatre offsets tombent juste, et par l'arithmétique, pas par chance** :
`0x20 + 0x00 = 0x20`, `0x20 + 0x10 = 0x30`, `0x20 + 0x14 = 0x34`,
`0x20 + 0xE8 = 0x108`. Le `offsetof(m_port) == 0xE0` du `static_assert` place
`m_is_connected` à `0xE8`, donc notre `+0x108` est bien lui.

**Et `+0x2C`, c'est `m_prev`.** Je l'avais échantillonné à 0 en notant que
« ça ne prouve rien » : c'était 0 parce que **nous ne l'écrivons jamais**.

### Ce que les deux hôtes de référence écrivent, et nous non

`chantier_yamp_revo\source\input\Pad.cpp` (`csl_pad::set_state`) et
`yamp_son\source\Y6\sl.cpp` l. 559-568 font **la même chose** :

```cpp
m_prev = std::exchange(m_now, 0);   // l'etat PRECEDENT, garde d'une image a l'autre
m_x1 = m_y1 = 0.0f;
... setButton(b) : m_now |= (1u << b);  m_buttons[b] = 0xFF;  ...
m_push = ~m_prev & m_now;           // FRONT MONTANT : vient d'etre enfoncé
m_pull = m_prev & ~m_now;           // FRONT DESCENDANT
```

Et le commentaire de `vf5fs\LJ\VF5FS.cpp` l. 385 dit pourquoi les pads sont
`static` : « **persistent so m_prev/m_push/m_pull stay meaningful** ». Puis
l. 410 : `memcpy(&execute_info.pad[i], &s_pads[i], kLjPadCopyBytes)` —
**0xE0 octets**, tout le préfixe, pas quatre champs. Le fork GOG va plus
loin : `V6-VF5FS.cpp` l. 392 appelle `set_state` **directement sur**
`execute_info.pad[0]`.

### La conséquence à mesurer

Une navigation de menu se fait sur un **front**, pas sur un maintien : sinon
un appui d'un dixième de seconde descendrait de six crans. Si le menu de REVO
lit `m_push`, il lit **toujours zéro** chez nous, et aucune flèche ne peut le
faire bouger — ce qui concorde avec la mesure du SS 419.69 : huit appuis
HAUT/BAS entre les images 1385 et 1539, **aucune réaction**, alors que START
à l'image 1035 a déclenché `sy_charin00st` dans la même image.

Ce n'est pas démontré : START pourrait aussi passer par `m_now`. Ce qui est
démontré, c'est que **nous laissons dix champs sur quatorze à zéro alors que
les deux hôtes qui font tourner ce moteur les remplissent tous**.

### APM3 ne répond pas à cette question

Son entrée est `VF5RE\tools\loaders\lindbergh-loader\src\lindbergh\`
(`evdevInput.c`, `sdlInput.c`) : du Linux/evdev qui garnit l'**IO de la
carte** JVS. C'est le chemin de la commande 364 (le masque arcade), pas le
bloc de pads. Il ne dit rien de `m_push`.

### La réparation, et ce qu'elle n'est pas

Remplir le pad **comme `set_state`** : garder les deux pads d'une image à
l'autre, poser `m_prev` avant, `m_push` / `m_pull` après, et
`m_buttons[b] = 0xFF` par bouton tenu. Ce n'est **pas** un interrupteur et
**pas** une sonde : c'est la politique de remplissage des hôtes de référence,
appliquée aux champs que la structure définit déjà.

## SS 419.71 — LE PAD EST ÉCRIT EN ENTIER : posé et compilé, pas encore essayé

Degré : **CONFIRMÉ** pour la disposition (trois `static_assert` qui compilent)
et pour le fait que les dix champs manquants sont désormais écrits.
**INCONNU** pour l'effet : aucune course depuis.

### Ce qui remplace quatre affectations

`vf5fs_host.cpp`, après `LireClavier` : une structure `PadLJ` qui est le
préfixe de `0xE0` octets de `pxd::csl_pad`, et `RemplirPad(bloc, port, clav)`
qui applique la politique de `csl_pad::set_state` mot pour mot :

```c
p.m_prev = p.m_now;          // l'etat de l'image precedente
p.m_now  = c.bits;
p.m_x1 = c.x;  p.m_y1 = c.y;  p.m_x2 = p.m_y2 = 0.0f;
memset(p.m_buttons, 0, 32);
for (b) if (p.m_now & (1u << b)) p.m_buttons[b] = 0xFF;
p.m_push = ~p.m_prev & p.m_now;
p.m_pull = p.m_prev & ~p.m_now;

uint8_t* base = bloc + 0x20 + port * 0x190;
memcpy(base, &p, sizeof p);                  // les 0xE0
*(uint32_t*)(base + 0xE0) = port;            // m_port
*(int32_t*) (base + 0xE4) = port;            // m_user_id
base[0xE8] = 1;                              // m_is_connected
base[0xE9] = 0;                              // m_is_remote
```

`g_padOmbre[2]` est **statique** : c'est ce qui donne un sens à `m_prev`, la
raison même que YAMP écrit dans `VF5FS.cpp` l. 385. Les trois mots que l'hôte
ne posait pas sont en plus dans la ligne `338.14` du journal
(`push=` / `pull=` / `prev=`), pour que la course suivante les **montre**.

### Trois contrôles à la compilation, qui pouvaient échouer

```c
static_assert(sizeof(PadLJ) == 0xE0, ...);
static_assert(offsetof(PadLJ, m_buttons) == 0xA0, ...);
static_assert(offsetof(PadLJ, m_prev_buttons) == 0xC0, ...);
```

Ils compilent. La structure que l'hôte copie est donc **octet pour octet**
celle que les `static_assert` des deux forks de YAMP décrivent — ce n'est plus
une transcription à la main.

### La vérification faite AVANT d'écrire 0xE0 octets

Écrire un bloc de 224 octets à `bi + 0x20` écrase tout ce qui s'y trouvait. Les
seules écritures de l'hôte dans ce bloc sont `+0x00`, `+0x08`, `+0x10`, `+0x14`,
`+0x18`, `+0x663`, `+0x678`, `+0x1FF08`, `+0x1FF10` : **rien entre `0x20` et
`0xFF`**, pour aucun des deux ports (`0x20..0xFF` et `0x1B0..0x28F`).

Et j'ai failli me tromper de bloc : le `+0x38` de `VF5_CONSOLE` (SS 310) est
dans **`blk`**, le bloc de `module_start`, pas dans **`bi`** (execute_info) où
vivent les pads. Deux blocs différents qui ont tous deux un `+0x38`. Si
c'avait été le même, le remplissage aurait effacé l'octet qui choisit la
chaîne console à chaque image.

### Deux champs restent à zéro, et c'est voulu

`m_button_frame` (`+0x40`) et `m_prev_buttons` (`+0xE0` du pad) : `set_state`
ne les écrit pas non plus. Les laisser à zéro est **fidèle**, pas négligent. Si
une mesure montre un jour que le module les lit, ce sera une autre marche.

### Ce que la prochaine course doit montrer

* `419.71 : pad ECRIT EN ENTIER ...` une fois, à la première image.
* `338.14 : ... push=0x00002000 pull=0x00000000 prev=0x00000000` à l'appui,
  puis `push=0x00000000 pull=0x00002000` au relâchement. Si `push` reste nul
  alors qu'une flèche est tenue, le remplissage est faux et rien d'autre ne
  compte.
* Et la question de départ : **le curseur du menu bouge-t-il** quand on
  appuie sur HAUT/BAS. C'est Frédéric qui le voit, pas le journal.

Si le curseur ne bouge toujours pas avec `m_push` posé, alors le menu ne lit
pas les fronts du pad, et il faudra chercher **où** il lit — mais une cause
aura été ôtée pour de bon, et elle ne reviendra plus brouiller la suite.

## SS 419.72 — LES FRONTS SONT JUSTES, ET LE MODULE NE S'EN SERT PAS ENCORE

Degré : **CONFIRMÉ** pour le remplissage. **CONFIRMÉ** pour la faute.
Journal : `host_log_s419_72_pad.txt`, 1 371 images.

### Le remplissage est prouvé par la mesure

```
image 584 : bloc+0x20 = 0x00002000 [BAS ]  push=0x00002000 pull=0x00000000 prev=0x00000000
image 595 : bloc+0x20 = 0x00000000 []      push=0x00000000 pull=0x00002000 prev=0x00002000
image 800 : bloc+0x20 = 0x00005000 [HAUT GAUCHE] push=0x00004000 pull=0x00000000 prev=0x00001000
image 825 : bloc+0x20 = 0x00005000 [HAUT GAUCHE] push=0x00004000 pull=0x00008000 prev=0x00009000
```

C'est exactement `~prev & now` et `prev & ~now`, y compris sur les diagonales
où une touche entre pendant qu'une autre sort (image 825 : GAUCHE monte,
DROITE tombe, dans la même image). **`m_push` n'est plus jamais nul quand une
touche vient d'être enfoncée**, ce qui était le cas à toutes les images avant
le SS 419.71.

Le critère d'échec que le SS 419.71 s'était donné — « si `push` reste nul
alors qu'une flèche est tenue » — n'est pas rempli. Le remplissage est bon.

### Et pourtant rien ne bouge : parce que rien n'est visible

Frédéric : « **l'écran de chargement masque tout** ». Ce n'est donc pas une
question d'entrée : le menu est **recouvert**. Voir MENU.md §13.5, corrigé au
même numéro.

### LA « FAUTE » N'EN EST PAS UNE — corrigé

```
!!! EXCEPTION 0xC0000005 a VF5FS+0x2f7aee
    acces en lecture a l'adresse 0x310075
    rip=VF5FS+0x2f7aee  rbx=0x119795e7d40  rdi=0x0
```

`VF5FS+0x2F7AEE` est la **première instruction utile** de `FUN_1802F7AD0` :
`TEST dword ptr [RCX + 0x38], 0x40000000`. Donc `RCX = 0x31003D` — pas un
pointeur. La fonction est appelée avec un `this` de pacotille.

**CE N'EST PAS UNE FAUTE : c'est Frédéric qui a fermé la fenêtre**, et il a
dû me le dire. Ma comparaison était fautive — j'ai opposé une course **fermée
à la main** à une course qui s'était **terminée toute seule** (3 000 images,
code 0). La différence n'était pas le pad : c'était qui arrêtait la course.

La preuve était déjà dans le banc : la course du SS 419.69 **sans** journal,
fermée à la main à l'image 1 681, avait rendu **le même `0xC0000005`**, et le
journal du 419.66, fermé pareil, se coupe au milieu d'une ligne. Fermer la
fenêtre tue le processus pendant que le module est au milieu d'une image : il
touche un état déjà démonté, d'où le `this` de pacotille.

**La leçon :** un code de sortie ne se compare qu'entre courses arrêtées de la
MÊME façon. J'avais la bonne règle écrite — « un code de sortie non nul n'est
pas une faute » — et je l'ai quand même traitée comme une régression, parce que
je venais de changer quelque chose. Avoir touché au code rend suspect, il ne
rend pas coupable.

Les quatre `LIBERATION ETRANGERE` juste avant sont du même tonneau : c'est le
démontage.

Juste avant la faute, quatre `LIBERATION ETRANGERE` depuis
`vf5fs_host.exe+0x1321` : le module rend des pointeurs qui ne viennent pas de
nos allocateurs. À regarder, mais après l'essai ci-dessus.


---

# SS 419.150 / 419.151 — LA GRILLE DU SÉLECTEUR, ET SES DEUX VOCABULAIRES DE BITS

Lu le 2026-11-11, entièrement dans les décompilations de ce dossier plus le
désassembleur. **Rien ici n'est du code à compiler.**

## Les deux bouts ne parlaient pas les mêmes bits

[`FUN_180181FE0`](SelChara_PasGrillePort.c) — le lecteur d'entrée du curseur — teste
**quatre masques dans les bits 28-31** :

| adresse | instruction |
|---|---|
| `1801822d2` | `MOV EDX,0x10000000` ; `CALL FUN_1801b2c60` |
| `180182346` | `MOV EDX,0x20000000` ; `CALL FUN_1801b2c60` |
| `1801823b9` | `MOV EDX,0x40000000` ; `CALL FUN_1801b2c60` |
| `180182409` | `MOV EDX,0x80000000` ; `CALL FUN_1801b2c60` |

et [`FUN_1801B2C60`](Entree_EtatMaintenu.c), au **désassembleur** (Ghidra typait le
pas `0x36`, c'est `0xd8` — [[la-decompilation-ghidra-perd-des-parametres]]) :

```
CMP byte [slot + 0x795c10], 0   -> JZ : rend 0        ; presence
IMUL RAX,RAX,0xd8 ; MOVSXD R8,dword [RAX + 0x795ac8]  ; l'emplacement
IMUL RCX,R8,0x54  ; MOV EDX,dword [RCX + 0x795958]    ; L'ÉTAT
TEST R9D,EDX ; SETNZ AL
```

Or [`FUN_18027A3F0`](Entree_ConstruireEnregistrements.c) **recopie `bloc+0x20` verbatim** et n'y
ajoute que les bits 16-23 dérivés des axes (seuil `0x4651`). Les bits 28-31 ne
peuvent donc venir **que de nous** — et nous posions `CLV_UP..CLV_RIGHT`, les
bits **12-15**. Les bons bits existaient déjà dans `e.m364` depuis le SS 364,
mais `m364` n'allait que dans la commande 364.

**Mesure avant/après**, sur trois journaux du banc :

| journal | `sy_cursor_move` | états portant les bits 28-31 |
|---|---|---|
| `419_135` | 0 | 0 |
| `419_149` | 0 | 0 |
| `419_150` | **38** | **218** |

`etat` est passé de `0x00044000` au maximum à `0x80088000` / `0x40044000` /
`0x20022000` / `0x10011000` — chaque direction portant ses trois
représentations (bit du haut, bit de stick, bit `CLV_*`).

Correctif : `e.bits |= (e.m364 & 0xF0000000u)`, interrupteur
`VF5_CURSEUR_HAUT`. **Additif** : `scalars_search(0x20000000,
to_function=FUN_1801b2c60)` ne rend qu'**une** occurrence dans tout le module,
donc le combat ne voit aucun changement.

## Ce qui restait : le vertical est jeté avant d'être appliqué

À l'écran, après le 419.150 : **gauche et droite marchent, haut et bas font
gauche et droite.** La cause est dans `FUN_180181FE0` :

```c
uVar2 = 10;
if (*(char *)(param_1 + 0x100) == '\0') goto LAB_180182589;   // NOTRE CAS
uVar18 = uVar18 + local_res20;                                // LE DELTA Y
```

Le delta vertical est appliqué **une ligne après** le saut. Et
`LAB_180182589` enferme toute sa recherche dans `if (local_res8 != 0)` — le
delta **horizontal**. Un mouvement purement vertical tombe dans le balayage
qui suit, lequel ne fait que `uVar8 + 1` / `uVar12 - 1` et cherche la case la
plus proche **à la même ligne**.

Les quatre branches, dans notre chemin (`+0x101 == 0`) :

| masque | delta posé | code `local_res18` |
|---|---|---|
| `0x10000000` HAUT | `local_res20 = -1` | *(aucun — reste à 2)* |
| `0x20000000` BAS | `local_res20 = 1` | 3 |
| `0x40000000` GAUCHE | `local_res8 = -1` | 4 |
| `0x80000000` DROITE | `local_res8 = 1` | 5 |

## Les DEUX octets d'interrupteur ne commandent pas la même chose

| octet | ce qu'il commande |
|---|---|
| **`+0x100`** | l'algorithme (l. 282), le **dessin** ([`FUN_1801817F0`](FUN_1801817f0.c), 8 sites), le post de la cmd 6 ([`FUN_180182DC0`](FUN_180182dc0.c) l. 110), [`FUN_180181E70`](FUN_180181e70.c) l. 30 |
| `+0x101` | seulement le remappage haut/bas → horizontal (l. 246, 270, 364) |

Et `FUN_18017C1E0` ne pose que **`+0x1c8`**, c'est-à-dire `+0x100` : sur la
console, `+0x100 = 1` et `+0x101 = 0`. C'est l'état où le vertical marche.

**`+0x100 = 1` ne bloque pas la grille** : dans `FUN_180182DC0` le test
n'ajoute que le post de la cmd 6 ; le calcul des min/max (`+0x60`..`+0x6c`)
est hors du `if`. Mais les cases 3/4/5 de `FUN_1801817F0` ne dessinent
l'animation de déplacement et ne jouent `sy_cursor_move` que si l'octet vaut
0 — et à 1 elles passent la main au répartiteur, **nul** pendant le
sous-état 19. Essai : `VF5_CURSEUR_100`.

## L'ordre des appels, qui interdit de basculer l'octet

```
FUN_180181550  ->  FUN_180181fe0(curseur, 1)   le MOUVEMENT
               ->  FUN_180181fe0(curseur, 0)
FUN_180181580  ->  FUN_180181e70(curseur, 0/1)
               ->  FUN_1801817f0(curseur, 0/1) le DESSIN
```

Les appels au répartiteur de `FUN_180181FE0` sont tous aux lignes 78-118,
**avant** le saut de la ligne 282 : aucun passage par l'hôte entre le
mouvement et le dessin. On ne peut donc pas poser l'octet à 1 pour l'un et à
0 pour l'autre dans la même image.

## Les neuf décompilations versées le 11 nov 2026

| fichier | ce qu'il porte |
|---|---|
| [`FUN_180181fe0.c`](SelChara_PasGrillePort.c) | le lecteur d'entrée du curseur, les 4 masques, `LAB_180182589` |
| [`FUN_18017cc20.c`](FUN_18017cc20.c) | le pas de SEL_CHARA par port, **l'armement** (délai de 5 images) |
| [`FUN_18017c1e0.c`](FUN_18017c1e0.c) | les phases de SEL_CHARA ; pose `+0x1c8` |
| [`FUN_180181e70.c`](FUN_180181e70.c) | l'écrivain de `[rec+0]`, la présence |
| [`FUN_1801817f0.c`](FUN_1801817f0.c) | le dessin et le son du curseur, 8 tests de `+0x100` |
| [`FUN_180180c00.c`](FUN_180180c00.c) | rend `[VF5FS+0x759A38]` — **toujours 0** |
| [`FUN_18017f740.c`](FUN_18017f740.c) | rend **1 par défaut** ; `port*0xb` = 11 colonnes |
| [`FUN_180182860.c`](FUN_180182860.c) | place le curseur sur une case |
| [`FUN_180182dc0.c`](FUN_180182dc0.c) | bâtit SEL_DATA et les min/max de la grille |

Toutes par `py -3 VF5RE\vider_fonctions.py <nom...>` — **par adresse ou par
nom direct**, jamais par `--liste`, qui échoue une fois sur deux
([[ghidra-ouvrir-le-projet-revo-pc]]).
