# Les décors de VF5FS APM3 : sélection et chargement, désassemblés

Établi le 2026-09-07 sur `vf5fs-pxd-w64-Retail_APM3.dll.origine` (binaire NON
patché, base `0x180000000`). Toutes les adresses sont des VA.

Ce document remplace les notes éparses sur « le décor » dans `REPRISE.md` et
`tools/pister_decor.py`. Il ne remplace pas `analysis/decors_vf5r.md` et
`analysis/import_decors.md`, qui parlent des **fichiers**, pas du code.

Désassemblages bruts conservés :
`analysis/disasm_decors_A.txt` (la tâche et son automate),
`_B.txt` (le chargeur), `_C.txt` (l'API publique), `_D.txt` (constructeur),
`analysis/disasm_selstage.txt` (l'écran de sélection),
`analysis/disasm_match_setup.txt` (le constructeur de match).
Table mise à plat : `analysis/table_decors.csv`, outil `tools/table_decors.py`.

---

## 1. Le piège, d'abord : il y a DEUX index de décor, pas un

C'est ce qui avait fait perdre une séance (mémoire *« Deux index de décor dans
VF5 : géométrie et éclairage sont deux appels ; je patchais celui qui ne dessine
rien »*). Voici les deux, nommés :

| | table | ce qu'elle sert | consommateur |
|---|---|---|---|
| **éclairage** | `0x18039F7A0` — 41 pointeurs vers le code à 3 lettres (`"tst"`, `"are"`, …) | `./rom/ibl/<code>.ibl` et les cinq `./rom/light_param/*_<code>.txt` | `0x1800D7130` |
| **géométrie** | `0x180403430` — 41 descripteurs de **0xF0 octets** | objset, collision, effets, musiques, caméra | `TaskStage`, `0x18018F680` |

Les deux sont indexées par le **même** index 0..40. `0x1800D7130` n'est **pas**
« le chargeur de décor » : c'est le poseur de chemins d'éclairage. Il est appelé
par le vrai chargeur, à l'état 2, en `0x18018F8A3`.

```
0x1800D7130   cmp ecx, 0x28          ; 41 decors : 0..0x28
0x1800D7133   ja  ret
0x1800D7138   lea rax, [0x18039F7A0]
0x1800D713F   lea rcx, [0x18070BB40] ; le gestionnaire d'eclairage (singleton)
0x1800D7146   mov rdx, [rax + rdx*8] ; le code a trois lettres
0x1800D714A   jmp 0x1800D7150
```

et `0x1800D7150` construit six chemins dans l'objet, par `0x1800172B0` :

    ./rom/ibl/%s.ibl
    ./rom/light_param/light_%s.txt
    ./rom/light_param/fog_%s.txt
    ./rom/light_param/glow_%s.txt
    ./rom/light_param/wind_%s.txt
    ./rom/light_param/envmap_correct_%s.txt

`0x1800D6130` fait la même chose avec `"tst"` en dur — c'est l'initialisation.
`0x1800D9020` interroge l'avancement (`0x1800D6DA0`), et le chargeur l'attend.

---

## 2. La table des 41 descripteurs, `0x180403430`

Bornes prouvées par le code lui-même : `0x18018EF6C  cmp edx, 0x29` (41) et
`0x18018F5E1  cmp r9, 0x2670` (41 × 0xF0). Structure lue champ par champ dans
ses consommateurs :

| offset | type | rôle | lu par |
|---|---|---|---|
| `+0x00` | `char*` | nom du jeu d'animations `auth_3d` — `"STGARE"` | `0x18018F8BC`, `0x18018F590` |
| `+0x08` | `char*` | jeu d'effets — `"EFFSTGARE"` | `0x18018F945` |
| `+0x10` | `int` | **identifiant d'objset** (la géométrie et les textures) | `0x1800F9C60` (demander), `0x1800FB7E0` (attendre), `0x1800F8A40` (finir), `0x1800F86C0` (libérer) |
| `+0x14` `+0x18` `+0x1C` `+0x20` `+0x24` `+0x28` `+0x2C` `+0x30` `+0x34` | `int` | identifiants d'objets `auth_3d` du décor, `-1` = absent (fond, ciel, arrière-plans, caméra…) | `0x18018F030` |
| `+0x38` | `float` | échelle | `0x18018F1FA` |
| `+0x3C` | `int` | — | |
| `+0x40` | `int` | ressource optionnelle (`-1` partout **sauf `are` = 6107**) | `0x18018F7C8` → `0x1801957A0` → `0x180105830` |
| `+0x48` | `char*` | **collision** — `"rom/STGARE_COLI.000.bin"` | `0x18018F8B0` → `0x18005F100` |
| `+0x50` `+0x58` `+0x60` | `ptr` | trois blocs de paramètres en `.data` (limites, caméra) | `0x18018FE30` / `0x18018FE10` / `0x18018FDF0` |
| `+0x68` | `char*` | **musique par défaut** — `vfes_bgm_stg_are.adx` | `0x18018F3D0(i, 9)` |
| `+0x70`…`+0xB0` | `char*[9]` | **les neuf variantes de musique** : `vf1`, `vf2`, `vfk`, `vf3`, `vf4`, `vf4ev`, `vf5`, `vf5r`, `vf5fs` | `0x18018F3D0(i, type)` |
| `+0xB8` | `int` | ambiance / réverbération | `0x18010CA50` |
| `+0xBC` `+0xBD` | `byte` | deux drapeaux copiés dans `0x18070FD74` / `0x18070FD75` | `0x18018FA1C`, `0x18018FA4C` |
| `+0xC0` | `ptr` | descripteur sonore principal | `0x18010CA20/40/30` |
| `+0xC8` | `ptr` | descripteur sonore **de repli**, utilisé seulement si le « poids » de chargement reste sous `0x18034B438` | `0x18018FA92` |
| `+0xD0` `+0xD4` `+0xD8` | `int` | propriétés exposées par `0x18018F440`, `0x18018F630`, `0x18018F460` | |
| `+0xDC` | `float` | portée / brouillard, poussé dans l'objet de rendu `+0xDC` | `0x18018F7EC` |
| `+0xE0` | `int` | idem, `+0x2DC` de l'objet de rendu | `0x18018F7FD` |

`+0x70` porte bien **`Stage BGM Type`** (libellé `0x322`) : `0x18018F3D0(index,
type)` rend `table + index*0xF0 + 0x70 + type*8`, retombe sur `+0x68` si le
créneau est vide, et le type `9` demande directement le défaut.

Les 41 lignes sont dans `analysis/table_decors.csv`. Extrait :

```
idx code  nom      objset  collision
 4  ban   STGBAN     24    STGBAN_COLI.000.bin
11  djo   STGDJO     28    STGDJO_COLI.000.bin
14  are   STGARE     22    STGARE_COLI.000.bin
21  du1   STGDU1     30    STGDU1_COLI.000.bin
22  du2   STGDU2     31    STGDU1_COLI.000.bin   <- partage la collision de DU1
26  trm   STGTRM     43    STGDU1_COLI.000.bin   <- idem (decor d'essai)
39  gym   STGGYM   2847    STGGYM_COLI.000.bin
40  smo   STGSMO   2848    STGSMO_COLI.000.bin
```

Deux accesseurs par nom :

```
0x18018F590(const char* nom) -> index      strcmp sur les 41, -1 si absent
0x18018F560(int index)       -> const char* nom
0x18018F580()                -> index courant
```

---

## 3. `TaskStage` : la tâche qui charge le décor

RTTI : **`TaskStage`**, vtable `0x180408210`, singleton en **`0x1807499D8`**.
Construite par `0x18018EE30`, détruite par `0x18018EEA0`.
Créneaux : `0x18018EDD0` (init), `0x180029FB0` (**bouchon**, rend vrai),
`0x18018EF40` (**update**), `0x18018EFD0` (fin).

### Champs de l'objet

| offset | rôle |
|---|---|
| `+0x58` | **l'état** : 0 inactif, 1→4 chargement, **5 = en place**, 6→9 déchargement |
| `+0x5C` | **index du décor courant** |
| `+0x60` | **index demandé** (`-1` = rien) |
| `+0x68` | pointeur sur le descripteur, `0x180403430 + index*0xF0` |
| `+0x70`…`+0x75` | six drapeaux : quelles parties charger / décharger |
| `+0x78`…`+0xB4` | 16 dwords poussés par `0x18018FD20` |
| `+0xB8` | flottant (fondu d'entrée) |

### `0x18018EF40`, l'update — c'est court et ça dit tout

```
si +0x60 != -1 :
    si +0x58 == 0 :                     ; libre
        +0x58 = 1
        si demande < 0x29 : +0x68 = 0x180403430 + demande*0xF0
        sinon             : +0x68 = 0        ; 0x29 et au-dela = pas de decor
        +0x5C = demande ; +0x60 = -1
    sinon si +0x58 == 5 : appeler le DECHARGEUR (0x18018F230)   ; il faut sortir
                                                                ; l'ancien d'abord
si 1 <= +0x58 <= 4 : appeler le CHARGEUR   (0x18018F680)
si 6 <= +0x58 <= 9 : appeler le DECHARGEUR (0x18018F230)
```

### `0x18018F680`, le chargeur, état par état

**État 1** — pesée et son.
Additionne le « poids » des deux combattants (costumes et accessoires, via
`0x180150840` / `0x180150A00` / `0x18014D530`), lit `+0xBC`/`+0xB8`/`+0xBD` du
descripteur, arme le son `+0xC0`, et **si le poids reste sous le seuil
`0x18034B438`** arme aussi `+0xC8` (le son supplémentaire qu'on s'autorise quand
la scène est légère). Cas particuliers **index 0x28 (`smo`) et 0x10 (`yuk`)** :
`[objet_rendu + 0x334] = 0`. Puis `0x1800F9C60(objset_id, 1)` — **la demande de
géométrie** — et `+0x58 = 2`.

**État 2** — les fichiers annexes.
Attend l'objset (`0x1800FB7E0`), puis :

```
0x18018F8A3  0x1800D7130(+0x5C)         ; ECLAIRAGE : ibl + light_param
0x18018F8B0  0x18005F100(desc+0x48)     ; COLLISION : STGxxx_COLI.000.bin
0x18018F8BC  0x18003C200(desc+0x00)     ; auth_3d "STGxxx"
0x18018F945  0x18003C200(desc+0x08)     ; auth_3d "EFFSTGxxx"
             recense les effets dans [rendu+0x790] / [rendu+0x7A0..]  (max 8)
0x18018F94D  0x1801903D0(+0x5C)         ; sons d'ambiance propres au decor
```
puis `+0x58 = 3`.

**État 3** — la barrière d'attente. Ne passe que si **tout** est prêt :
objset, éclairage (`0x1800D9020`), `0x18005F720`, les deux jeux `auth_3d`
(`0x18003C1D0`), et `0x180190470`. Ensuite : `desc+0x40` → `0x1801957A0` →
`0x180105830` ; `desc+0xDC` et `desc+0xE0` poussés dans l'objet de rendu ;
`0x18006F620(+0x5C)` ; `0x18006F9C0(+0x70)` ; `+0x58 = 4`.

**État 4** — attend `0x18006FA60`, `0x1800F8A40(objset_id)`, `+0x58 = 5`.

**État 5** — en place. `0x18018F030` fait alors l'entrée en scène : joue les
objets `auth_3d` `+0x14`…`+0x2C`, arme la caméra, et **pour les index 8 (`riv`)
et 9 (`jin`) seulement** enregistre le rappel `0x18018FBC0` (identifiant `0x15`),
qui lit une petite table de deux entrées de 12 octets en `0x1806495F8` et
déclenche un effet de scène propre à ces deux décors.

### `0x18018F230`, le déchargeur

Table de sauts en `0x18018F3B4`, états 6→9 : arrête les sons et les effets,
libère l'objset par `0x1800F86C0(desc+0x10)`, remet `+0x68 = 0`, `+0x5C = -1`,
`+0x58 = 0`.

### Ambiances scénarisées

Quatre petites tâches nommées par le RTTI, toutes pilotées par le même
compte-à-rebours `+0x58` et le générateur `0x18030E650` :

| classe | vtable | ce qu'elle joue |
|---|---|---|
| `StageSoundTraffic` | `0x1804082A8` | `stg_car_passing` / `vfxse_traffic2` |
| `StageSoundBird` | `0x1804082E8` | `stg_vfv_kamome`, `stg_vfv_taki_bird` |
| `StageSoundFireFall` | `0x180408328` | |
| `StageSoundSpaceLight` | `0x180408368` | |

---

## 4. L'API publique de `TaskStage` — et elle est minuscule

Tout passe par des feuilles qui lisent le singleton `0x1807499D8`. Aucune autre
partie du binaire ne touche cet objet directement (balayage linéaire : **21
références, toutes dans `0x18018E`–`0x180190`**).

| fonction | rôle | appelants |
|---|---|---|
| **`0x18018FCF0(index)`** | **DEMANDER UN DÉCOR** | **3 seulement** |
| `0x18018FB20(nom, b)` | armer la tâche (nom `"STAGE"`) | 3 |
| `0x18018FDC0(drapeaux, b)` | poser `+0x70` | 5 |
| `0x18018FE50()` | « le décor n'est pas prêt » | 7 |
| `0x18018F630(index)` | propriété `+0xD4` du descripteur | 1 |
| `0x18018FD20(src)` | copier 16 dwords dans `+0x78` | 1 |
| `0x18018FDE0(f)` | poser `+0xB8` | 2 |
| `0x18018FDF0/E10/E30` | les trois blocs `.data` du descripteur | 3 / 3 / 5 |
| `0x18018F600(b)` | flottant `+0xE8`/`+0xE4` du descripteur | 7 |

Le demandeur, en entier :

```
0x18018FCF0  cmp ecx, 0x29
0x18018FCF3  jge  ret                       ; >= 41 : refuse (0x29 = ALEATOIRE)
0x18018FCF5  mov rax, [0x1807499D8]
0x18018FCFC  cmp ecx, [rax + 0x5C]
0x18018FCFF  je   ret                       ; deja ce decor : rien a faire
0x18018FD01  mov [rax + 0x60], ecx          ; LA DEMANDE
0x18018FD04  mov rax, [0x180C3B6F0]
0x18018FD10  mov [rax + 0x1FE20], ecx       ; recopie dans le bloc de session
```

**Ses trois appelants, et c'est toute la sélection de décor du jeu :**

| appelant | contexte |
|---|---|
| `0x1800BC6AD` (dans `0x1800BC5E0`) | **le combat** : `0x1800B48D0(params)` → `[params+0x4C]` |
| `0x1801C4DAB` (dans `0x1801C4D60`) | l'écran **Customize / TERMINAL**, index en dur (§6) |
| `0x1802035AA` (dans `0x180203550`) | la **démo / rejeu**, index dans `[objet+0xD0]` |

---

## 5. D'où vient l'index : les paramètres de partie, champ `+0x4C`

L'objet « paramètres de partie » porte le décor en **`+0x4C`**, lu par
l'accesseur feuille `0x1800B48D0` (`mov eax, [rcx+0x4c] ; ret`, 15 appelants).

### 5.1 La valeur de départ est « aléatoire »

`0x1800B56C0`, la remise à zéro des paramètres, écrit :

```
0x1800B56E4  [rcx+0x14] = 0x15    ; personnage 1P = 21 = aucun
0x1800B56EB  [rcx+0x18] = 0x15    ; personnage 2P
0x1800B571C  [rcx+0x4C] = 0x29    ; DECOR = 41 = ALEATOIRE / non choisi
0x1800B5723  [rcx+0x48] = 2
```

`0x29` est hors des 0..40 : `0x18018FCF0` le refuse, donc tant que personne ne
tranche, aucun décor n'est demandé.

### 5.2 Le constructeur de match, `0x1800B8540`

Il remplit une structure de configuration locale (base `[rsp+0x30]`) puis la
recopie dans les paramètres par `0x1800B34D0`, qui fait champ à champ :

    config+0x0C -> params+0x14   personnage 1P
    config+0x10 -> params+0x18   personnage 2P
    config+0x3C -> params+0x44   rounds
    config+0x40 -> params+0x48   cote
    config+0x44 -> params+0x4C   *** LE DECOR ***

et la configuration part elle aussi de `0x29` :

```
0x1800B85B4  mov r12d, 0x29
0x1800B85BA  mov [rsp+0x74], r12     ; config+0x44 = decor = aleatoire
...
0x1800B8BDF  mov [rsp+0x74], r12d    ; ce que r12d vaut a la fin
```

### 5.3 Et `r12d` vient du personnage : le décor « maison »

Dans la branche « contre l'ordinateur » :

```
0x1800B8AF6  mov ecx, [rsp+rbx+0x3c]   ; le personnage de l'ADVERSAIRE
0x1800B8AFA  call 0x1800AF400          ; -> son decor
0x1800B8AFF  mov r12d, eax
0x1800B8B02  cmp eax, 0x15             ; 21 = Dural
0x1800B8B05  jne suite
             ... 0x1800B2330(...)      ; cas particulier Dural
```

`0x1800AF400(personnage)` parcourt un vecteur de paires *(personnage, décor)*
tenu par le singleton **`0x1806F9C10`** — classe **`GameScoreSetting`** (RTTI,
vtable `0x18039AEA0`), qui analyse **`./rom/game_score.txt`**.

Ce fichier est dans l'archive (8 724 octets, extrait dans
`extracted/game_score.txt`) et il est en clair :

```
score.chara.0.name=AKI    score.chara.0.stage=STGDJO
score.chara.1.name=SAR    score.chara.1.stage=STGAUR
score.chara.2.name=LAU    score.chara.2.stage=STGBAN
score.chara.3.name=SHU    score.chara.3.stage=STGRIV
score.chara.4.name=JEF    score.chara.4.stage=STGUMI
score.chara.5.name=PAI    score.chara.5.stage=STGTAN
score.chara.6.name=JAK    score.chara.6.stage=STGNYC
score.chara.7.name=KAG    score.chara.7.stage=STGTER
score.chara.8.name=LIO    score.chara.8.stage=STGCAS
score.chara.9.name=WOL    score.chara.9.stage=STGYUK
score.chara.10.name=AOI   score.chara.10.stage=STGJIN
score.chara.11.name=LEI   score.chara.11.stage=STGSIN
score.chara.12.name=VAN   score.chara.12.stage=STGTAK
score.chara.13.name=BRA   score.chara.13.stage=STGBAR
score.chara.14.name=GOH   score.chara.14.stage=STGHAI
score.chara.15.name=MON   score.chara.15.stage=STGSLK
score.chara.16.name=MSK   score.chara.16.stage=STGARE
score.chara.17.name=KRT   score.chara.17.stage=STGGYM
score.chara.18.name=TAK   score.chara.18.stage=STGSMO
score.chara.19.name=TE2   score.chara.19.stage=STGTS3
score.chara.20.name=DUR   score.chara.20.stage=STGDU1
score.chara.length=21
```

Le nom `STGDJO` est converti en index par `0x18018F590`.

**Donc : en mode solo, le décor d'un combat est le décor maison de l'adversaire.
C'est une donnée de fichier, éditable, pas une constante du code.**

Le même fichier contient les **trois routes** (`score.route.0/1/2.enemy0..7`),
c'est-à-dire l'ordre des adversaires d'Arcade / Score Attack / License Challenge
— et donc, indirectement, la suite des décors :

```
route A : BRA WOL SHU LEI LAU AOI AKI DUR
route B : GOH TAK KAG MON VAN KRT AKI DUR
route C : LIO SAR MSK JAK JEF PAI AKI DUR
```

---

## 6. L'écran de sélection de décor : `TaskSelStage`

RTTI : **`TaskSelStage`**, vtable `0x180400A18`.
Destructeur `0x1801741A0`, `update` **`0x180174250`** (1 402 octets, chaînée),
`0x180175140`, `0x1801747E0`.

`0x180174BF0` construit la liste affichée : un tableau local de **27 entrées de
0x18 octets**, chacune portant deux noms de calques AET (`"ban"` / `"ban_stay"`,
`"ter"` / `"ter_stay"`, …) et **l'index de décor**. Les index posés sont
`4..0x14` (ban → tan), `0x15..0x19` regroupés sous le calque `"dur"` (DU1 à
DU5), `0x27` (gym), `0x28` (smo), puis **`0x29` sous le calque `"rnd"`** —
l'entrée *Random*.

Les décors d'essai (`tst`, `ts2`, `ts3`, `wht`, `trm`, `cid`, `trs`, `evo00` à
`evo09`) **n'apparaissent pas dans la liste** : ils existent dans la table mais
pas dans l'écran.

Le tirage au sort se lit à la validation :

```
0x18017474E  cmp dword [rbx+0x5C], 0x29    ; le curseur est sur RANDOM
0x180174752  jne suite
0x180174754  mov eax, [rbx+0x60]           ; le decor tire par la roulette
0x180174757  mov [rbx+0x5C], eax           ; il remplace RANDOM
```

Autrement dit **`0x29` n'atteint jamais `TaskStage`** : il est résolu ici, dans
l'écran, avant d'être posé dans les paramètres de partie.

### L'autorisation, elle, est une case de réglages

Le RTTI nomme **`Wrap_allow_stage_select`** (vtable `0x18034A5D8`) :

```
0x180046960  get : (dword [0x18066B8E8] >> 1) & 1
0x180046970  set : ecrit le BIT 1 de [0x18066B8E8]
```

C'est **le bit 1 du dword de configuration `0x18066B8E8`** qui commande le
libellé `0x1D5 Stage select` (aide `0x85 Adjust the stage selection method.`).
Le bit 0 du même dword est un autre réglage (accesseur voisin `0x1800468A0`).

---

## 7. Le troisième demandeur : l'écran TERMINAL / Customize

`0x1801C4D60` (`STAGE_TASK` du menu de personnalisation) :

```
0x1801C4D99  0x18018FB20("STAGE", 0)      ; armer la tache
0x1801C4DAB  0x18018FCF0(<index en dur>)  ; demander le decor
0x1801C4DBE  0x18018FE50()                ; attendre qu'il soit pret
```

C'est le site que `tools/decor_perso.cmd` patche, et le journal du 2026-09-05
avait déjà relevé qu'il y a **deux immédiats à changer**, pas un — le second
étant en `0x1801C3C4D` (`0x18018FDC0`, les drapeaux `+0x70`).

---

## 8. Le chemin complet, en une image

```
game_score.txt  ──► GameScoreSetting [0x1806F9C10] ──► 0x1800AF400(perso) ─┐
                                                                           │
ecran TaskSelStage (liste de 27, RANDOM=0x29 resolu sur place) ────────────┤
                                                                           ▼
                                     0x1800B8540  constructeur de match
                                     0x1800B34D0  config+0x44 -> params+0x4C
                                                                           │
                                     0x1800B48D0(params) ──────────────────┤
                                                                           ▼
                                     0x18018FCF0(index)   [0..40 seulement]
                                                                           │
                                     TaskStage [0x1807499D8] +0x60 = index │
                                                                           ▼
                                     0x18018EF40 update  ──► +0x68 = descripteur
                                                                           │
                          ┌────────────────────────────────────────────────┤
                          ▼                                                ▼
        0x18018F680 chargeur (etats 1→5)                    0x18018F230 dechargeur
          etat 1 : 0x1800F9C60(objset_id)         geometrie + textures
          etat 2 : 0x1800D7130(index)             ECLAIRAGE (ibl, light_param)
                   0x18005F100(coli)              collision
                   0x18003C200("STGxxx")          animations
                   0x18003C200("EFFSTGxxx")       effets
                   0x1801903D0(index)             ambiances
          etat 3 : barriere d'attente + camera
          etat 4 : 0x1800F8A40(objset_id)
          etat 5 : en place ──► 0x18018F030 entree en scene
```

---

## 8 bis. Le choix parmi les cinq décors de Dural est un bouchon

Ajouté le 2026-09-07. Juste après l'appel à `0x1800AF400`, le constructeur de
match traite un cas particulier :

```
0x1800B8AFA  call 0x1800AF400        ; le decor maison de l'adversaire
0x1800B8AFF  mov  r12d, eax
0x1800B8B02  cmp  eax, 0x15          ; 21 = du1, le decor de Dural
0x1800B8B05  jne  0x1800B8B24
0x1800B8B07  call 0x1800B23A0        ; l'objet de session [0x1806F9C18]
0x1800B8B14  call 0x1800B23B0        ; rcx + 0x50
0x1800B8B1C  call 0x1800B2330        ; <- LE CHOIX PARMI LES CINQ
0x1800B8B21  mov  r12d, eax
```

et `0x1800B2330` fait six octets :

```
0x1800B2330  b8 16 00 00 00   mov eax, 0x16     ; 22 = du2
0x1800B2335  c3               ret
```

Un seul appelant, argument ignoré, constante en retour. **Les cinq décors de
Dural sont dans le jeu, entiers, chargés par le chemin ordinaire ; un seul est
atteignable.**

`--decors-dural [premier]` (lanceur `tools\decors_dural.cmd`) réécrit le bloc
`0x1800B8B02`–`0x1800B8B20` en place — 31 octets, aucune caverne — par une
translation de cinq décors consécutifs vers `du1`…`du5`. Par défaut
`cas riv jin sin djo` → les décors maison de Lion, Shun Di, Aoi, Lei-Fei et
Akira.

Deux précautions, écrites dans le patcheur : `0x1800B8B21` (`mov r12d, eax`) est
**préservé**, parce que la voie License Challenge y saute depuis `0x1800B8A2D` ;
et la translation agit **avant** que l'index ne devienne le décor courant, donc
les cas particuliers indexés (8 et 9, 16 et 40) ne se déclenchent pas dessus.

## 9. Ce que ça ouvre concrètement

1. **Forcer un décor proprement** se fait en un seul point : `0x18018FCF0`, ou
   mieux `[params+0x4C]`. Les patchs par index en dur dans `0x1801C4D60` ne
   valent que pour l'écran Customize.
2. **Changer les décors des routes** ne demande aucun patch de code : il suffit
   d'éditer `score.chara.<n>.stage` dans `rom/game_score.txt`. Le fichier est
   dans le `.par`, donc la voie `tools/par_masquer.py` (§6 de
   `analysis/import_decors.md`) s'applique telle quelle.
3. **Les 17 décors d'essai existent dans la table mais pas dans l'écran.**
   Ajouter `trm`, `cid`, `trs` ou les `evo0x` à la liste de `0x180174BF0` est un
   patch de tableau local, pas une extension de la table des 41.
4. **Les neuf variantes de musique par décor** sont déjà câblées
   (`0x18018F3D0`) : `Stage BGM Type` a de quoi fonctionner sans rien ajouter.
5. **La règle de livraison ne change pas** : le `.par` d'abord, le disque en
   repli — et un décor s'importe **avec sa collision, ses `auth_3d` et son
   éclairage**, parce que les champs `+0x14`…`+0x34` du descripteur désignent des
   objets **par indice** dans l'objset (voir `analysis/import_decors.md` §3, où
   la tentative DJO de VF5 R avait bouclé sur l'écran de chargement pour cette
   raison exacte).

Confiance : **CONFIRMED** pour §1 à §7 (tout est lu dans le binaire ; les
non-références sont établies par balayage linéaire, `tools/refs_multi.py`, pas
par `.pdata`). **SUPPORTED** pour le rôle exact des champs `+0x14`…`+0x34` et
`+0xD0`…`+0xE0` du descripteur : leur consommateur est identifié, leur sémantique
fine ne l'est pas.

---

## 9. Ce que les séances du 2026-09-07 et 08 ont tranché

### Les champs `+0x14`…`+0x34` sont DÉCODÉS

La réserve ci-dessus (« SUPPORTED, sémantique fine non établie ») tombe. Le mot
**haut** est l'**identifiant d'objset**, le mot **bas** l'**identifiant d'objet
dans cet objset**. Vérifié sur les 41 descripteurs, en les recoupant avec les
`*_obj.bin` lus par **`tools/objset.py`** :

```
du1  objset   30    30:1  30:382  30:0
djo  objset   28    28:114 28:118 28:117 28:116 28:115
du5  objset 5529  5529:0 5529:1 5529:2   …   0:28600 0:28601 0:28602
```

Ordre des cases : `gnd`, `ring`, `sky`, `sdw`, `reflect`, —, puis trois objets
de l'**objset 0** (les effets communs) pour sept décors.

Corollaire qui change tout pour l'import : **si les identifiants d'objets sont
les mêmes dans les deux générations, il n'y a rien à patcher.** C'est le cas de
`djo` (114 à 118 des deux côtés) ; voir `analysis/import_decors.md` §8.

### Un décor n'a qu'UN objet de ciel

`tools/objset.py` lit la table des noms au lieu de balayer l'ASCII. Les cinq
décors de Dural n'ont chacun que trois à cinq objets réels — `gnd`, `ring`,
`sky`, parfois `sdw` et `reflect` — le reste étant des effets numérotés. Toute
théorie de « série de ciels » ou de cycle jour/nuit tombe avec.

### La grille de sélection peut GRANDIR

Voir `analysis/ajouter_un_decor.md` §6 pour le détail. En deux lignes : les
deux tables de cases se suivent (`0x180400210`, 21 cases ; `0x1804004B0`, 22
cases, morte en console) et la liste d'exclusion ne commence qu'en
`0x180400770` — soit **43 cases d'affilée**. Et `0x180173BD0` **extrapole** la
position de toute case dont l'ancre (`+0x18`) est nulle : une case neuve se
place seule. Quatre compteurs suivent : `0x1801746D2`, `0x18017493C`,
`0x180174BBE`, `0x180174AA0`.

`patch_moteur.py --grille-ajout` porte la grille à 25 cases (du2..du5 sur une
4e ligne), lanceur `tools/decors_ajoutes.cmd`.

### L'aperçu est du CODE

La liste des aperçus n'est pas une table : elle est construite instruction par
instruction sur la pile vers `0x180174BF0` (`mov [rbp+0xD0], 0x14 ; lea rax,
"tan" ; …`, 0x18 octets par entrée). Le point 3 du §8 ci-dessus — « ajouter
`trm` à la liste de `0x180174BF0` est un patch de tableau local » — est donc
**faux** : c'est un patch de code, qui demande une caverne.

---

## 10. Les variantes du SANCTUARY, nommées (2026-09-08)

Nommage donné par Frédéric, qui les a vues à l'écran. **Son observation prime
sur mes déductions par objets** — et elle les recoupe :

| décor | variante | ce que les objets disaient |
|---|---|---|
| du1 | **SNOW** | `MZ_saidan` (autel), `MZ_iseki` (ruines) |
| du2 | **ECLIPSE** ou **METEOR** | `MZ_inseki` (隕石, météore), `CGZ_gouka1` (豪火), `STGDU2_EFF_FIRE` |
| du3 | **SUBMERSION** | `CGZ_hamon` (ondes), effets `DOBON` (chute dans l'eau) |
| du4 | **STORM** | `sky3_cloudy_weather2/3`, `stgdu4_eff_sky_dome` |
| du5 | **SPACE** | `mars_CGZ_sky`, `CGZ_star1/2/3`, `CGZ_monn` (lune) |

**Il manque trois variantes : NIGHT, DAY, SUNSET.** À retrouver.

Cela recoupe deux choses déjà établies : la capture de 2007 montre le SANCTUARY
**de nuit** (§9 et `REPRISE.md` 2026-09-07 (13)), et R.E.V.O. range ces décors
en `st_vf5_sanctuary1..5.par`. La famille compte donc **huit** membres, dont
cinq seulement sont livrés dans Final Showdown.

### Ce qui est demandé, et où ça bute

Frédéric, 2026-09-08 : la quatrième ligne de cases est **refusée**. Une case
doit rester une case ; c'est le bouton **SELECT** qui doit faire défiler les
variantes du décor sous le curseur, et l'écran doit afficher, **sous la mention
de la taille du décor**, la génération : `Virtua Fighter 5` /
`Virtua Fighter 5R` / `Virtua Fighter 5 Final Showdown`.

Deux morceaux, et ils n'ont pas le même coût :

**1. Le défilement — tractable.** `TaskSelStage::update` (`0x18017425E`) lit
ses boutons par deux fonctions triviales :

```
0x1801724A0(base, code)  ->  octet [(code + 2) * 0x40 + base]
0x180172450(base, code)  ->  vrai si [rec+0x28] == 6 ou [rec+0x20] == 6
```

`base` est `rbx + 0x70`, un tableau d'enregistrements de 0x40 octets indexé par
`code + 2`. La validation interroge les codes **0** et **1**
(`r13d = rsi + 1`, `rsi = 0`). **Le code du bouton SELECT n'est pas connu** :
c'est la mesure qui manque, et `tools/pister_selstage.py` la fait.

Le défilement lui-même est ensuite une écriture dans `[rbx+0x5C]`, l'index du
décor sélectionné — le même champ que les quatre substitutions « du1 → du2 »
écrasaient.

**2. Le libellé — pas tractable en l'état.** La légende « Sanctuary / Single
Wall 16x16 » est **peinte dans la scène AET**, pas tirée de `string_array` :
`0x1801743D8` passe des noms de compositions (`stage_icon_name_out`) à
`0x180171E90`, il n'y a pas d'identifiant de texte. Écrire une ligne de plus
demande donc soit une composition AET qui n'existe pas, soit un appel de
dessin de texte — et ce dernier n'est pas identifié sur cet écran. Le
mécanisme existe ailleurs (le libellé « How to Play » du Dojo est un
identifiant `string_array`, `0x2F1`, écrit dans un emplacement de pile que le
dessinateur du menu relit) ; reste à trouver son équivalent ici.

---

## 11. Le défilement au SELECT — posé le 2026-09-08 (`--variantes`)

Lanceur `tools/variantes.cmd`. **Validé à l'écran le 2026-09-08** : Frédéric a chargé DU4 en faisant défiler à la barre espace.

### Les trois mesures qui l'ont rendu possible

1. **La barre espace est un canal libre.** Le stub la met sur le code brut
   **6**, et la vraie `apm.dll` ne l'affirme jamais (« le code 6 n'a pas de bit
   et rend toujours faux »). Rien ne se le dispute. Deux sites du moteur
   l'interrogent déjà — `0x18023B269` et `0x18023BA48` — donc la forme de la
   requête est connue ; on la copie de `0x1801A2BC0` (VALIDER, code 7) :

   ```
   mov rcx, [0x180C3B6F8] ; mov edx, 6 ; mov rax, [rcx] ; call [rax+0x160]
   ```

2. **`[rbx+0x5C]` n'est réécrit QUE quand le curseur bouge.** Le bloc
   `0x18017476B`–`0x180174781` est gardé par `test al,al ; je épilogue` en
   `0x180174769`. Une valeur qu'on y fait tourner **persiste** donc jusqu'au
   prochain déplacement — exactement le comportement voulu.

3. **`0x180174BF0(this)` rafraîchit l'aperçu**, et on le rappelle après chaque
   rotation.

### Le point d'accroche et la place

Le détour est posé en **`0x180174710`**, la queue commune jouée à chaque trame
(plusieurs `jmp 0x180174710` y mènent). Six octets repris —
`xor edx,edx ; lea rcx,[rbx+0x70]` — rejoués à la fin de la greffe.

**Pas de `sub rsp`** : le code d'origine appelle `0x1801724A0` juste après sans
rien ajuster, donc l'espace d'ombre est déjà réservé par le prologue et
l'alignement est bon. C'est le code voisin qui le prouve, pas un calcul.

**La place.** Le détour fait 76 octets ; les plus grandes cavernes `int3` en
font 20, et il n'y en a que quatre. On ajoute donc une **section** au fichier :

* la table des sections finit en `0x348` et `SizeOfHeaders` vaut `0x400` —
  **184 octets libres**, quatre en-têtes de plus ;
* le fichier s'arrête exactement où finit `.reloc` (6 965 248 octets), et cette
  taille est déjà alignée sur `FileAlignment` (0x200).

`.greffe` est donc posée en `0x180EA1000`, 4096 octets, `CODE|EXECUTE|READ`.
**Aucun octet existant n'est déplacé** : les offsets de tout le reste du
fichier ne bougent pas, et les correctifs déjà écrits restent valides. Le code
greffé n'utilise que de l'adressage relatif, donc il survit à un rebasage.

**Vérifié : le jeu se lance avec la section greffée.** C'est le seul risque
sérieux de la manœuvre, et il est levé.

### Ce qui manque, et qui se verra

**L'aperçu ne change pas** : les cinq décors de Dural partagent la planche AET
`dur`/`dur_stay`, et la légende est peinte dedans. Rien à l'image ne dit quelle
variante est choisie — il faut compter ses appuis. Le libellé demandé
(`Virtua Fighter 5` / `VF5R` / `VF5 Final Showdown`, sous la mention de la
taille) suppose de reconstruire `string_array` : **23052 identifiants, pas un
seul créneau libre**, aucun pointeur nul, aucune chaîne vide. Le fichier étant
dans le `.par`, la voie est celle déjà éprouvée — masquer le nom, poser un
fichier libre reconstruit — plus la borne `0x5A0C` à lever si l'on dépasse
23052.

Et `0x1801EFD10` n'est pas une table de consultation : c'est un **répartiteur**
qui passe l'identifiant au service `[[0x180C3B6F0]+0x1FE10]` avec la
**commande 0x74**. Le même répartiteur porte d'autres commandes — la 6
apparaît dans le constructeur de grille et dans `TaskSelStage`. C'est là qu'il
faudra chercher celle qui dessine.

### Correction du 2026-09-08 : il a fallu DEUX accroches

La première version écrivait `[rbx+0x5C]` en `0x180174710`. Elle faisait tout
ce qu'il fallait — 300 passages du détour, `al = 1` à chaque appui, index écrit
à 22 — et pourtant **seul du1 se chargeait**.

Un point d'arrêt **matériel** en écriture sur le champ
(`tools/pister_5c.py`, `[0x180714928]+0x3B0+0x5C`) a nommé les autres
écrivains, sans laisser place au raisonnement :

```
rva 0x17477D  ->  ecrit -1          (0x180174776)
rva 0x174784  ->  ecrit la case     (0x180174781, la RECOMPUTATION du curseur)
rva 0x175354  ->  1372 acces        (0x180175351, la ROULETTE de la case ALEA,
                                     alimentee par le tirage 0x1801749F0)
rva 0xEA1039  ->  du2               (notre greffe)
```

Notre écriture arrivait **avant** la recomputation, qui la défaisait dans la
même trame. D'où la forme actuelle :

| | |
|---|---|
| `0x180174710` (entrée A) | lit la barre espace, fait tourner un **numéro de variante gardé dans la greffe** — plus dans `[rbx+0x5C]`, qui ne nous appartient pas |
| `0x1801747C0` (entrée B) | **après** la recomputation, juste avant le rafraîchissement : applique le numéro. C'est elle qui a le dernier mot |
| `APPLIQUER` | si `[rbx+0x5C]` est dans l'anneau 21..25, y pose `21 + numéro` |

La greffe est passée en `CODE|EXECUTE|READ|WRITE` pour tenir la variable.

### Le libellé : cet écran ne dessine AUCUN texte

Mesure faite, et elle est négative sans appel : le résolveur de libellés
`0x1801EFD10` a **276 appelants** dans le moteur, et **pas un seul** dans
`0x18017xxxx`, l'écran de sélection.

Tout ce que cet écran affiche est de l'**art peint**, désigné par nom de
composition AET :

```
stage_icon_xxx_c    les 21 ancres de cases
xxx_stay            l'apercu, une couche par decor (dont un `ari_stay` inutilise)
stage_icon_name_out / _out_e / _in / _in_e     la plaque NOM + TAILLE
stage_name_l_base / _e, stage_graph_l_base, deco_tit_stage_out
```

Il n'y a donc **aucun identifiant de texte à fournir** : écrire
« Virtua Fighter 5R » sous la taille demande soit d'introduire un appel de
dessin de texte dans un écran qui n'en a jamais fait, soit de fabriquer l'art.

## 12. Le nom de la variante à l'écran — `--variantes-texte` (2026-09-08)

Suite du §11. L'écran ne dessinant aucun texte, on en introduit un.

**Où** : le **créneau 4 de `TaskSelStage`** (`0x180400A38`), qui était un
bouchon `ret 0` — donc aucun original à rappeler, et `this` est la tâche
elle-même. C'est la phase de **rendu** ; depuis l'update (créneau 2) l'appel
partait avec des paramètres parfaits et ne produisait rien.

**Quoi** : `0x18019B2E0(descripteur, 0x28, …)`, la fonction du « NOW LOADING ».
Descripteur neuf par `0x18019A8C0`, style neuf par `0x18019A9D0`, mode 2 par
`0x18019B6F0`, taille par `0x18019B830`. **Neuf passes** : huit noires décalées
de deux pixels pour le liseré, la blanche au centre — le contour à la main, sans
chercher une option du moteur.

**Deux gardes**, parce que le dessin est global : `[rbx+0x58] == 2` (l'écran est
en navigation) et `[rbx+0x5C]` dans l'anneau 21..25 (le curseur est sur Dural).

### Les deux fautes payées, et ce qu'elles apprennent

**1. Pointeurs absolus dans la greffe → `ACCESS_VIOLATION`.** La table de
chaînes portait des adresses calculées à la base préférée `0x180000000`, mais
la DLL est **rebasée** (`0x7FFDB0620000` à la mesure) et la section greffée n'a
**aucune relocation**. Le moteur lisait `r8 = 0x180EA1900` en terre inconnue.
Corrigé : plus un seul pointeur absolu, chaînes à **pas fixe de 16 octets**,
adresse calculée en RIP-relatif (`lea rcx,[rip+textes] ; shl rax,4 ;
lea r8,[rcx+rax]`). Vérifié : zéro mot de la greffe ne ressemble à une adresse.

**2. Monter le calque 2D → plantage.** Le texte passait sous l'AET parce que sa
commande ne pose pas `cmd+0x14` : il reste à `-1` et l'insertion retombe sur
`[contexte+0x828]`, le calque courant. Monter ce calque de 8 a fait planter le
jeu « juste avant de pouvoir sélectionner l'icône du décor de Dural ».

La raison se **lit** dans le constructeur du contexte, `0x18018A030` :
`new(0x838)` puis `0x1802FE160(ctx+0x10, 0x10, 0x80, …)` — **128 compartiments
de 16 octets**. L'indice d'insertion vaut
`(desc+0x24) + ((desc+0x28 + calque) << 5)`, donc **0..127 : quatre calques de
trente-deux rangs**. +8 calques réclamait l'indice 264.

**Le correctif** ne touche à aucun état global : il corrige notre seul
descripteur pour viser le **dernier compartiment**, le 127 —
`desc+0x28 = 3 - calque`, `desc+0x24 = 31` — et renonce à dessiner si le calque
courant dépasse déjà 3. Détail complet : `analysis/texte_2d.md` §8-9-10.

### Réglages, tous des données de la greffe

| adresse | rôle | défaut |
|---|---|---|
| `0x180EA1808` | plafond de calque — **ne pas augmenter** | 3 |
| `0x180EA180C` | rang dans le calque (0..31) | 31 |
| `0x180EA1810` / `0x180EA1814` | x, y | 640, **460** (position validée) |
| `0x180EA181C` | taille de police | 24 |

Lanceur `tools/variantes_texte.cmd`. Le repli sans dessin, validé à l'écran,
reste `tools/variantes.cmd`.

**Pas encore vu à l'écran.** Et la ligne de génération demandée
(`Virtua Fighter 5` / `5R` / `Final Showdown`, sous la mention de taille) reste
à écrire : c'est une seconde chaîne dans la même greffe, une fois la première
confirmée.

## 13. Ajouter le dojo de VF5 R sans remplacer : la tentative RATÉE (2026-09-08)

> **Rien de ce qui suit n'est en place.** L'essai a été défait le 2026-09-09 :
> `trm` est rendu à l'origine, `djo` reste ce que `decor_5r_akira.cmd` en fait.
> Cette section garde les mesures — elles servent à la reprise — et surtout les
> quatre fautes, qui sont la vraie matière.

Demande de Frédéric : « ajoute le même système pour le stage d'Akira, avec le
variant VF5R », c'est-à-dire **ajouter** au lieu de remplacer.

### Ce qui a été mesuré, et reste vrai

**L'emplacement.** `trm` — indice 26, objset 43 — est un des dix-sept décors
d'essai (§`ajouter_un_decor.md` 6.1). Il paraissait libre. **Il ne l'était
pas** : c'est le décor TERMINAL, réparé et validé à l'écran le 2026-09-05
(`--decor-perso`, deux octets, §`menu_console.md` 15.10).

**Un descripteur porte QUINZE champs utiles, pas trois.** Le diff `djo` / `trm`
champ par champ :

| champ | djo | trm | ce que c'est |
|---|---|---|---|
| `+0x10` | 28 | 43 | l'objset |
| `+0x14`…`+0x24` | `1C0072 1C0076 1C0075 1C0074 1C0073` | `2B0000 - 2B0001 - -` | les cinq objets, **empaquetés `(objset << 16) \| rang`** : objset 28, rangs 114 118 117 116 115 (gnd, ring, sky, sdw, reflect) |
| `+0x2C`…`+0x34` | 28389/90/91 | −1 | trois identifiants que **seuls huit décors** portent (ter, jin, djo, umi, slk, aur, tan, du5) |
| `+0x48` | `rom/STGDJO_COLI.000.bin` | `rom/STGDU1_COLI.000.bin` | la collision |
| `+0x68`…`+0xB0` | dix chaînes BGM | une seule | la musique et ses neuf reprises |
| `+0xB8` | 2 | 0 | 2 chez ban, cas, jin, djo, are, bar, gym |
| `+0xD0` | 1 | 0 | lu par `0x18018F440`, comparé à 0 et à 4 : il **aiguille un rendu** (`0x180084F58`, `0x18011F7D1`) |
| `+0xD4` | 2 | 0 | lu par `0x18018F630`, puis `cmp eax, 9` et un **saut indirect sur dix cas**, chacun posant une constante flottante différente dans `xmm8` (`0x180204863`) |
| `+0xE4`/`+0xE8` | 12 × 12 | 16 × 16 | la taille de l'aire |

**Les relocations bornent le clonage.** Dix champs de `djo` sont des pointeurs,
et une adresse d'image n'est juste que là où une **relocation** la suit au
rebasage. `djo` en a dix-sept, `trm` **sept** — `0x00 0x08 0x48 0x50 0x58 0x60
0x68`. Recopier une adresse ailleurs referait la faute des pointeurs absolus de
la greffe (§12).

**`obj_db.bin` cherche par le nom de l'emplacement.** L'entrée 43 nomme
`stgtrm.farc`, `stgtrm_obj.bin`, `stgtrm_tex.bin`. Un objset importé doit donc
voir ses **deux noms internes réécrits**, et seulement dans l'**en-tête** du
`FArC` (taille en gros-boutien en `+0x04`, 0x3A ici) : la même chaîne réapparaît
à `0x4C` dans le flux de données, et l'y écraser corromprait l'archive.
`importer_decor.py --vers <code>` le fait.

**L'aperçu de la grille est borné à 26 entrées.** `0x180174BF0` construit sa
liste sur la pile, `0x180175010` la parcourt (`cmp rax, 0x1a`), et faute de
trouver l'indice elle **efface les trois couches AET** (`0x18017502D`). Un
emplacement recyclé n'a donc pas d'aperçu : il faut rafraîchir sur la **base**
de l'anneau. `0x180174B60` fait la même chose pour la case de grille — il
balaie les 21 cases (`0x180174BBE cmp rax, 0x15`) et rend `NULL`.

**L'éclairage n'est pas dans le descripteur.** Table de 41 codes minuscules en
`0x18039F7A0`, lue par `0x1800D7130` (`cmp ecx, 0x28`), qui compose
`ibl/%s.ibl`, `light_param/{light,fog,glow,wind}_%s.txt` et
`light_param/envmap_correct_%s.txt`. Deux appelants : le combat
(`0x18018F8A3`, index = `[gestionnaire+0x5C]`) et l'écran customize
(`0x1801C4DD0`).

### Les quatre fautes

1. **`--decors-dural cas` dans le lanceur.** Elle réécrit `0x1800B8B02` en
   `cmp eax,7 ; jl ; cmp eax,11 ; jg ; add eax,14` — `cas riv jin sin djo →
   du1..du5`. **`djo` vaut 11 : il est dans la plage.** Tout combat au dojo
   chargeait `du5`. `decor_5r_akira.cmd` n'a jamais eu cette option, et c'est
   la seule différence entre les deux lanceurs. **Comparer les invocations
   avant tout le reste.**
2. **Recycler un emplacement déjà réparé.** `trm` était TERMINAL. Connaître le
   nom d'un décor ne dit rien de la forme de son enregistrement.
3. **L'état des fichiers était HÉRITÉ.** `patch_moteur.py` repart de
   `.origine` ; `importer_decor.py --poser` ne repart de rien. Un décor posé
   par un lanceur restait dans tous les autres. Corrigé : chaque lanceur
   **pose** son état (§`REPRISE.md` 2026-09-09).
4. **Accuser l'éclairage de VF5 R** (glow `exposure` 2.8 contre 2.0) alors
   qu'une capture de Frédéric le disculpait déjà. `importer_decor.py
   --eclairage <source>`, écrit pour cette fausse piste, existe mais ne sert à
   rien.

### Ce qu'il reste à trancher

La proposition d'intégration est en §14.


---

> **`trm` et `ts2` ne sont plus disponibles** — voir §14 : `trm` et `ts2` sont PRIS.

## 14. PROPOSITION — ajouter le dojo VF5 R sans rien casser (2026-09-09)

**Rien de ceci n'est appliqué.** C'est un plan, chiffré sur du code lu.

### 14.1 Ce qui est intouchable

| acquis | pourquoi on n'y touche pas |
|---|---|
| `decor_5r_akira.cmd` | validé deux fois ; il **remplace** `djo` et c'est très bien |
| `trm` (26) | c'est TERMINAL, réparé et validé (`--decor-perso`, §`menu_console.md` 15.10) |
| `ts2` (1) | ce que l'écran Customize charge d'origine, témoin de `decor_TS2.cmd` |
| l'anneau de Dural | `--variantes` / `--variantes-texte`, validés |

Le nouveau chantier doit être **un lanceur de plus**, pas une modification des
lanceurs existants.

### 14.2 L'emplacement d'accueil : `evo00` (indice 29, objset 51)

**La liste ne se suppose plus, elle se mesure** : `tools/emplacements.py`
croise quatre preuves — la forme du descripteur (deux objets, `+0x18`/`+0x20`/
`+0x24` à −1, tous deux du bon objset), la grille de sélection, la liste
d'aperçus, et **les codes que nos propres `.cmd` nomment**. Résultat :

    LIBRES (15) : tst ts3 wht cid trs evo00 evo01 … evo09
    PRIS        : trm (treize lanceurs), ts2 (decor_TS2.cmd), les 39 autres

C'est la quatrième preuve qui manquait le 2026-09-08 : `trm` est nommé par
**treize** lanceurs. `ts2` l'est par `decor_TS2.cmd`.

`evo00` est proposé plutôt que `tst` : l'indice 0 est le repli naturel de tout
ce qui remet un index à zéro, et rien n'oblige à courir ce risque quand
quatorze autres attendent.

**Vérifications faites :**

* la **grille** (21 cases, `0x180400210`, indice en `+0x08`) porte
  14 6 15 10 7 8 40 / 17 19 11 41 9 5 4 / 13 20 39 16 18 12 21 — aucun
  emplacement d'essai ;
* la **liste d'aperçus** de `0x180174BF0` couvre 4..25, 39, 40, 41 puis `-1` —
  aucun emplacement d'essai non plus ;
* `stgevo00.farc` existe dans le `.par` : le masquage habituel s'applique.

### 14.3 Le point dur, et sa solution : le descripteur

Un descripteur fait 0xF0 octets. Le §13 en donne le diff. Deux familles de
lecteurs, et elles ne se patchent pas de la même façon.

**Famille A — par le gestionnaire.** `0x18018EF40` consomme la demande et pose
le descripteur, à **une seule instruction** :

```
0x18018EF6C  cmp  edx, 0x29            ; index < 41 ?
0x18018EF71  imul r8, rdx, 0xF0
0x18018EF78  lea  rax, 0x180403430
0x18018EF7F  add  r8, rax
0x18018EF87  mov  [rcx+0x68], r8       <- LE SEUL SITE
0x18018EF8B  mov  [rcx+0x5C], edx
```

Tout ce qui passe par `gestionnaire+0x68` (les cinq objets, la collision,
`+0xD0`, `+0xD8`, l'aire, **et `+0xC0`**) suit ce pointeur.

**Famille B — par l'index, dans la table statique.** Quatre lecteurs
seulement, tous relevés au balayage linéaire de `0x180403430` :

| site | ce qu'il lit |
|---|---|
| `0x18018F560(index)` | `+0x00`, le code `STGxxx` (nom auth_3d) |
| `0x18018F590(nom)` | le balayage inverse nom → index |
| `0x18018F3D0(index, variante)` | la **musique** : `+0x70 + variante*8`, et si nul, les neuf puis `+0x68` |
| `0x18018F630(index)` | `+0xD4` |

### 14.4 Pourquoi le clonage statique seul ne suffit pas : `+0xC0`

`+0xB8` / `+0xC0` sont un **compte et un tableau** : `+0xC0` pointe dans un
petit bloc juste avant la table des descripteurs (`0x1804033E0`…`0x180403420`,
cinq blocs de 16 octets, des triplets 0/1/2). Douze décors seulement en ont —
ban, cas, riv, jin, sin, **djo**, umi, are, slk, bar, du3, gym : ceux qui ont
des **murs**. `djo` porte `+0xB8 = 2` et `+0xC0 → {0,1,1,0}`.

Or `evo00` n'a **pas de relocation** en `+0xC0` (comme `trm` : sept seulement,
`0x00 0x08 0x48 0x50 0x58 0x60 0x68`). Y écrire `0x1804033E0` en statique
donnerait une adresse à la base préférée, fausse dès le rebasage — la faute
déjà payée sur la greffe. Un dojo sans ses murs, c'est un ring-out là où il
n'y en a pas : ce n'est pas cosmétique.

### 14.5 Le plan, en deux étages

**Étage 1 — les fichiers, sans binaire.**

```
py -3 tools/importer_decor.py --poser djo --source VF5R --vers evo00
```

Neuf pièces renommées au code de l'emplacement, les deux noms internes du
`FArC` réécrits **dans l'en-tête seulement**, les neuf noms masqués dans le
`.par`. Déjà écrit et éprouvé (§13).

**Étage 2 — le binaire, trois écritures statiques et une accroche.**

| quoi | où | pourquoi |
|---|---|---|
| clone du descripteur de `djo` | `0x180403430 + 29*0xF0` | les quinze champs |
| `+0x10` ← 51, `+0x14`…`+0x24` ← `(51<<16)\|rang` | idem | l'objset de l'emplacement |
| `+0x48` ← `rom/STGEVO00_COLI.000.bin` | mou de `.rdata`, **après** DU2 (`0x180641B60`) et la place déjà prise | la collision importée |
| les dix pointeurs sans relocation ← 0 | `+0x70`…`+0xB0`, `+0xC0` | sinon adresses fausses au rebasage |
| **accroche sur `0x18018EF87`** | 5 octets → greffe | *voir ci-dessous* |

L'accroche remplace `mov [rcx+0x68], r8` par un saut vers la greffe, qui :

1. rappelle l'instruction déplacée ;
2. si `edx` (l'index demandé) vaut 29, remplace `[rcx+0x68]` par l'adresse
   d'un descripteur **construit une fois dans la greffe** : une copie octet
   pour octet du descripteur **vivant** de `djo` (`0x180403E80`, donc déjà
   relogé), avec `+0x10` et `+0x14`…`+0x24` réécrits.

**C'est ce qui lève la limite des relocations** : la copie est prise à
l'exécution, tous ses pointeurs sont justes, `+0xC0` compris. Les murs du dojo
suivent, et les neuf reprises de musique aussi pour tout ce qui passe par le
gestionnaire.

**Ce qui reste au statique, et c'est borné** : `+0x68` (musique) et `+0xD4`,
les deux seuls champs de la famille B qui comptent. `+0x68` est relocalisé chez
`evo00`, donc on peut y écrire la chaîne de `djo`. `+0xD4` est un entier.
`+0x70`…`+0xB0` restent nuls et `0x18018F3D0` **retombe alors sur `+0x68`** —
c'est écrit dans le code, pas espéré.

### 14.6 L'anneau et l'écran

Le mécanisme de `--variantes` marche déjà pour des indices non contigus : il
faut seulement une table d'anneaux au lieu d'un couple `(premier, longueur)`.
Le code en a été écrit puis retiré avec le reste ; il est décrit au §13.

Deux points mesurés qui l'encadrent :

* **l'aperçu se rafraîchit sur la BASE.** `0x180174BF0` ne connaît que
  26 indices et, faute de trouver, **efface** les trois couches AET
  (`0x18017502D`). L'entrée B pose donc la base, appelle l'aperçu, remet la
  variante ;
* **le curseur, lui, n'a rien à craindre.** `0x180174794` cherche la case de
  `[rbx+0x5C]` par `0x180174B60` et, s'il ne trouve pas, retombe sur la case
  `rnd` (41). Mais cette branche est celle du DÉPLACEMENT
  (`0x18017475C`), et elle s'exécute **avant** l'entrée B : à ce moment
  `[rbx+0x5C]` vaut encore la base, qui a une case. C'est déjà ce qui fait que
  du2..du5 — sans case — se chargent sans déranger le curseur.

### 14.7 Ce que ça coûte, et ce que ça ne casse pas

* **aucun décor réel perdu**, la table reste à 41, aucune borne levée ;
* **`djo` n'est pas touché** : `decor_5r_akira.cmd` continue de le remplacer,
  et le nouveau lanceur, lui, laisse `djo` d'origine et pose `evo00` ;
* **un lanceur de plus**, `dojo_5r_ajoute.cmd`, jamais les autres ;
* l'accroche `0x18018EF87` est un site à **un seul** écrivain — vérifié : la
  seule référence à `0x180403430` dans `0x18018EF40`.

### 14.8 L'ordre proposé, et où ça peut échouer

1. poser `evo00` et lancer `pister_import.py evo00 --controle` — si l'objset
   ne porte pas les rangs 114..118, on s'arrête là, sans essai à l'écran ;
2. patcher le descripteur statique seul, **sans** l'accroche, et regarder :
   si le décor s'affiche, il ne manque que les murs et la musique ;
3. ajouter l'accroche, et vérifier au débogueur que `[gestionnaire+0x68]`
   vaut bien l'adresse de la greffe pour l'indice 29 ;
4. seulement ensuite, brancher l'anneau `[11, 29]` et le libellé.

~~**Le risque qui reste, et il est réel** : `tex_db.bin`.~~ **Levé le
2026-09-09, et il n'existait pas** : les identifiants de texture d'une archive
importée sont déjà dans `tex_db.bin` sous leurs noms d'origine — le dojo y a ses
271 `F_VF5E_DJO00_*`. Un décor importé n'a rien à y ajouter. Ce qui manquait
était ailleurs : les noms d'auth_3d du descripteur et la table des murs. Voir
`analysis/tex_db.md`.

---

## 15. L'ÉCRÊTAGE — d'où vient l'indice, et où il était remplacé (2026-09-10)

Tout ce qui précède décrit ce que le moteur fait **avec** un indice de décor.
Cette section dit d'où l'indice **vient**, parce que c'est là que se jouait
l'échec du premier décor ajouté : il n'était pas rejeté, il n'était pas
**demandé**.

### 15.1 La chaîne complète

Chaque maillon vient d'une énumération **complète** de références, jamais d'un
candidat choisi à la lecture : 4 références au global du mode, 2 appelants du
poseur, 14 références au global des paramètres, 3 appelants de la demande, 21
références au singleton `TaskStage`.

    0x18020AE60  mov [0x180754A58], r9d       l'indice du mode
    0x18020AE67  cmp ecx, 1 ; jne             ... et si le mode vaut 1 :
    0x18020AE6E  mov eax, 0x27                    39 = gym
    0x18020AE73  mov ecx, 0x0B                    11 = djo
    0x18020AE78  cmovne eax, ecx                  selon dl
    0x18020AE7B  mov [0x180754A58], eax

    0x180209B0C  lea ebx, [rax - 1]           le defaut
    0x180209B0F  call 0x180244EA0             le mode console est-il actif ?
    0x180209B16  cmovne ebx, [0x180754A58]    si oui : l'indice du mode
    0x180209B31  call 0x180203E40 (ecx = ebx) les parametres du combat

    0x180203F0F  mov eax, 0x27                39 = gym, LE REPLI
    0x180203F1E  cmp ebp, 0x28                l'indice demande
    0x180203F2E  cmova ebp, eax               L'ECRETAGE
    0x180203F34  mov [params + 0xD0], ebp     params = [0x180754938]

    0x1802035A4  mov ecx, [params + 0xD0]
    0x1802035AA  call 0x18018FCF0             TaskStage::demander

    0x18018FCF0  cmp ecx, 0x29 ; jge          la borne (levee par --decors-table)
    0x18018FCFC  cmp ecx, [rax + 0x5C]        deja courant ? on ne fait rien
    0x18018FD01  mov [rax + 0x60], ecx        LA DEMANDE
    0x18018FD10  mov [0x180C3B6F0 + 0x1FE20], ecx   une copie ailleurs

    0x18018EF40  le validateur, a chaque trame :
    0x18018EF8B  mov [rcx + 0x5C], edx        la RECOPIE de la demande
    0x18018EF8E  mov [rcx + 0x60], -1         demande consommee

    0x18018F8A3  -> le chargeur, index = [TaskStage + 0x5C]

### 15.2 Les deux champs, et pourquoi surveiller `+0x5C` ne dit rien

`+0x60` est la **demande**, `+0x5C` le **courant**. `+0x5C` n'est écrit que par
**une seule instruction dans tout le binaire** — `0x18018EF8B`, la recopie du
validateur. Un point d'arrêt matériel sur `+0x5C` ne peut donc jamais nommer
autre chose que cette recopie ; c'est ce qui a fait perdre la séance du
2026-09-09. Le décideur est celui qui écrit `+0x60`, et il n'y en a **qu'un**,
`0x18018FD01`, atteint par trois appelants seulement.

Autre piège de la même famille : `TaskStage` est **créé et détruit** en cours de
partie (`0x18018EE30` publie le pointeur en `0x1807499D8`, `0x18018EEA0` le
remet à zéro). Un DR armé une fois sur `objet+0x5C` finit sur un bloc rendu au
tas — le journal du 2026-09-09 montrait `ntdll` écrivant `0xFEEEFEEE`, et
c'était ça. Une sonde doit **suivre le pointeur** : `pister_60_stage.py` arme un
DR sur le pointeur lui-même et réarme les autres à chaque création.

### 15.3 L'écrêtage, la septième borne — celle qu'aucune énumération ne rendait

    0x180203F1E  cmp ebp, 0x28
    0x180203F2E  cmova ebp, eax        ; eax = 39 (gym)

Tout indice **strictement au-dessus de 40** devient 39. Et `cmova` est **non
signé** : `-1`, que l'appelant `0x1801E51FB` pose en dur dans `r9d` pour dire
« aucun décor choisi », vaut `0xFFFFFFFF` — donc « au-dessus de 40 », donc gym.

C'est ce qui explique, d'un seul coup, tout ce qu'on observait :

* le décor 42 chargeait la Training Room ;
* la sonde ne voyait **qu'un** chargement, `index 39 (gym)` ;
* `--dojo-decor 42` ne changeait rien : le bloc 39/11 de `0x18020AE50` est dans
  la branche `mode == 1`, **mesurée à zéro passage**.

**Pourquoi les six bornes de `--decors-table` ne l'incluaient pas** : elles ont
toutes été trouvées en énumérant les *lecteurs des deux tables de décors*
(`refs_plage.py`). Celle-ci ne lit aucune table — elle assainit un indice avant
de le ranger dans les paramètres du combat. La leçon, qui vaut plus que la borne
elle-même : une borne n'est pas forcément un `jae` devant une table, ni une
sentinelle `je` sur une valeur ; **elle peut être un `cmov` avec valeur de
repli**.

Balayage de tout `.text` pour la forme « `cmp reg, 40/41` … `cmov` dans les
douze instructions » : quinze sites. Neuf sont le groupe `0x1800A2xxx` (le
classificateur sur 41..45, écarté le 2026-09-09), `0x1801750AF` est un `cmove`
sur 41 — le code aléatoire —, et `0x180203F1E` est le seul qui écrête un indice
de décor. **La prémisse de ce balayage, écrite pour pouvoir être attaquée** : il
ne voit que la forme `cmp`+`cmov`. Un écrêtage écrit en branchement
(`cmp` / `jbe` / `mov`) lui échapperait.

### 15.4 Les deux options, et ce qu'elles ne font pas

| option | ce qu'elle change |
|---|---|
| `--decor-ecretage <N>` | l'octet `0x180203F20` : la borne passe de 40 à N-1, comme `--decors-table` fait pour les six autres. Sans elle, un indice de 42 ne survit pas au trajet |
| `--decor-repli <i>` | l'immédiat `0x180203F10` : le repli n'est plus `gym` mais `i`. C'est le seul geste qui donne un décor **quand personne n'en demande** — le cas du DOJO |

Les deux se complètent : l'écrêtage laisse passer un indice demandé, le repli
choisit ce qu'on obtient quand la demande vaut `-1`. Aucune des deux ne rend le
décor ajouté **sélectionnable** : ça reste le travail de la grille et de
`--variantes`.

Note à vérifier le jour où l'aléatoire sera en jeu : avec la borne à 43, un
indice de 41 (le code « décor aléatoire ») n'est plus ramené à 39 **ici**. Il
était donc écrêté jusqu'à présent, ce qui veut dire que l'aléatoire est résolu
**avant** ce point — les sept sites qui testent 41 par égalité. Ce n'est pas
mesuré, c'est déduit ; le patcheur refuse de toute façon 41 comme indice.

---

## 16. CE QU'UN DÉCOR DEMANDE EN FICHIERS — onze, pas neuf (2026-09-10)

### 16.1 L'inventaire, lu dans le `.par` et non de mémoire

`py -3 tools/par_inventaire.py <archive> --grep "(?i)djo"` rend **onze** entrées.
C'est la liste de référence :

| fichier | qui le demande |
|---|---|
| `stg<code>.farc` | l'objset, par `obj_db` |
| `STG<CODE>_COLI.000.bin` | le descripteur, `+0x48` |
| `STG<CODE>.farc` | l'auth_3d du décor, `+0x00` |
| `EFFSTG<CODE>.farc` | l'auth_3d des effets, `+0x08` |
| `<code>.ibl` | `0x1800D71C1` |
| `light_<code>.txt` | `0x1800D71EA` |
| `fog_<code>.txt` | `0x1800D720E` |
| `glow_<code>.txt` | `0x1800D7232` |
| `wind_<code>.txt` | `0x1800D7256` |
| `envmap_correct_<code>.txt` | `0x1800D727A` — **le sixième chemin d'éclairage** |
| `se_stage_<code>.acb` | la liste d'association `0x180408850`, **avec défaut** |

Les six premiers chemins d'éclairage sont composés à partir du **code à trois
lettres** de la table `0x18039F7A0`, pas du descripteur.

### 16.2 `envmap_correct_*` : la pièce qui gelait le chargement

Elle n'existe **pas dans le dump VF5R** de 2008 — c'est un fichier de Final
Showdown, et les 41 décors du jeu en ont un. Un décor ajouté sans elle affiche
l'écran de chargement pour toujours.

Elle ne se voyait pas tant qu'on **remplaçait** : le code restant `djo`, et seuls
les neuf noms posés étant masqués dans le `.par`, l'`envmap_correct_djo.txt` de
l'archive répondait encore. C'est « le `.par` avant le disque » pris par l'autre
bout — ce que l'archive fournit encore masque ce qu'on a oublié de poser.

Contenu, pour `djo` : `1\n1\n1\n0\n0\n0\n0.15\n-0.75\n0.4\n`, 27 octets. Neuf
nombres, aucun nom de décor : la recopie du modèle est exacte.
`decor_neuf.py` l'extrait du `.par` (`extraire_du_par`, qui refuse un fichier
comprimé plutôt que de rendre des octets faux).

### 16.3 Le son d'ambiance : une LISTE D'ASSOCIATION, avec valeur par défaut

    0x1801903DC  lea rdx, [0x1804083A0]        le jeu de sons PAR DEFAUT (are)
    0x1801903EA  lea rax, [0x180408850]        la liste
    0x1801903F3  cmp [rax], ecx                l'indice du decor
    0x1801903F7  add rax, 0x10                 24 entrees {dword, qword}
    0x1801903FB  cmp [rax+8], 0                terminee par un pointeur nul
    0x180190404  mov rdx, [rax+8]              trouve : le jeu de sons du decor

Vingt-quatre entrées seulement, dans un ordre quelconque, pour 41 décors : les
décors d'essai n'en ont pas. **Un indice inconnu n'échoue pas** — il garde le
jeu de sons de `are`. Le décor ajouté a donc une ambiance, celle de `are`, et
rien ne bloque.

Chaque enregistrement fait 0x30 octets : le chemin `.csb`, puis jusqu'à cinq noms
de sons (`vfxse_wall_religious3`, `stg_vfvse_floor_kishimi`…).

Pour donner au décor ajouté l'ambiance de `djo` il faudrait ajouter
`{42, 0x1804084C0}` à la liste — mais elle est suivie **immédiatement** de ses
chaînes (`0x1804089E0` = `rom/sound/se_stage_are.csb`), donc il faut la déplacer,
comme les trois autres tables. Pas fait.

### 16.4 La leçon de forme

Troisième forme de table rencontrée sur ce chantier, et la seule qui pardonne :

| forme | exemple | un indice hors liste |
|---|---|---|
| table indexée | descripteurs `0x180403430`, codes `0x18039F7A0` | **mine** : `0x18018F590` déréférence `+0x00` |
| tableau dans une structure | compteurs de parties, `+0x1A2EC` | corrompt le champ suivant |
| liste d'association avec défaut | sons d'ambiance, `0x180408850` | **rien** : la valeur par défaut sert |

Avant de lever une borne ou d'ajouter une entrée, savoir dans laquelle des trois
on est. Et ne pas déduire la forme de la régularité : `0x180408850` est régulière
et n'est pas indexée.

---

## 17. LES SIX TABLES INDEXÉES PAR LE DÉCOR (2026-09-10)

C'est la carte à consulter avant d'ajouter quoi que ce soit. Quatre de ces six
tables n'existaient pas dans ce document il y a un jour, et **chacune manquante
donnait un symptôme différent, toujours silencieux**.

| table | VA | forme | ce qu'elle décide | si l'indice manque |
|---|---|---|---|---|
| descripteurs | `0x180403430` | 41 × `0xF0`, **pointeurs** | tout le décor | **mine** : `0x18018F590` déréférence `+0x00` |
| codes | `0x18039F7A0` | 41 × 8, **pointeurs** | le code à trois lettres, donc l'éclairage | chemins faux |
| grille | `0x180400210` | 21 × `0x20`, **pointeurs** | la case de STAGE SELECT | pas sélectionnable |
| objsets en plus | `0x18034D570` | 41 × `0x60`, entiers | les objsets à charger **avec** le décor | **chargement infini** : le moteur attend des objsets tirés de moitiés de pointeurs |
| effets a3d | `0x18034FD20` | 22 × `0x10`, **assoc.** | les animations d'effet (flammes, drapeaux) | rien ne s'allume, en silence |
| effets mur | `0x180355C30` | 32 × `0x40`, **assoc.** | le mur / la barrière | pas de mur, en silence |

**Deux formes, deux comportements.** Les quatre premières sont *indexées* : au
delà de leur dernière entrée elles lisent ce qui suit dans `.rdata` — la table
des objsets en plus lisait des moitiés de pointeurs et le chargement ne
finissait jamais. Les deux dernières sont des **listes d'association**
`{indice, données}` : un indice inconnu ne plante pas, il **ne fait rien**.
Avant de lever une borne ou d'ajouter une entrée, savoir dans laquelle des deux
familles on est (cf. §16.4).

### 17.1 Les effets : qui les déclenche

À l'état 3, `0x18006F380` donne l'indice du décor à **chaque tâche d'effet** :

    obj->vtable[7](obj, indice)      creneau 7 = setStage

et chaque tâche cherche cet indice dans **sa** table :

```c
// TaskEffectAuth3D::setStage   0x1800706B0   -> 0x18034FD20
//   {indice, pointeur vers une liste d'uid terminee par -1}
//   djo (11) -> [1193, 1191, 1192]
//   ... uid.1191.value = A STGDJO_EFF_FIRE
//       uid.1192.value = A STGDJO_EFF_FIRE_REFLECT
//       uid.1193.value = A STGDJO_EFF_HATA

// TaskEffectWall::setStage     0x1800843A0   -> 0x180355C30
//   {indice, trois pointeurs, quatre qwords a zero}
//   djo (11) -> {11, 0x180352060, 0x180352560, 0x180352568}
```

Les animations sont donc désignées **par numéro d'uid dans `auth_3d_db`**, pas
par nom. Une entrée neuve doit porter **nos** numéros, ceux que `decor_neuf.py`
a attribués — ils se lisent dans la base posée, ils ne se devinent pas.
`patch_moteur.uids_correspondants()` retrouve chaque animation du modèle par sa
valeur renommée et **garde l'ordre du modèle**, qui est l'ordre de jeu.

Les autres tâches d'effet (`TaskEffectHit`, `Snow`, `Rain`, `Leaf`, `Ripple`,
`Splash`…) ont le même créneau 7 et vraisemblablement la même forme de table.
Elles n'ont pas été ouvertes : le dojo n'en utilise aucune. **C'est la prémisse
à attaquer le jour où un décor ajouté aura de la pluie ou de la neige.**

### 17.2 L'index des noms d'objets est GLOBAL

`FUN_1800F8B50(nom)` : un vecteur `{nom, valeur}` de 16 octets,
`[gestionnaire+0xC8..+0xD0]`, **trié par nom**, lu par **dichotomie**, bâti
depuis `obj_db`. Deux objsets qui déclarent le même nom d'objet, c'est le
**premier** qui gagne.

Conséquence pour un décor ajouté : ses objets doivent être **renommés**
(`STGDJO_` → `STGD5R_`), et avec eux les uid d'`auth_3d_db` et le contenu des
`.a3da`, qui nomment leurs objets. Les **textures** ne bougent pas — elles
s'appellent `F_VF5E_DJO00_…`, sans `STGDJO_`, et `tex_db` les déclare
globalement sous ces noms-là.

C'est l'inverse de ce que ce document a longtemps affirmé : « les noms d'objets
se recopient VERBATIM » est vrai **dans l'archive**, faux **dans `obj_db`**.

### 17.3 Où sont les bases

Le binaire porte une **archive `FArC` embarquée** en `0x1804137F0` :
`mot_db`, **`obj_db`**, `tex_db`, `spr_db`, `aet_db`, `rob_mot_tbl`, plus
l'éclairage de `tst`. Le résolveur la consulte **avant** le `.par` et avant le
disque : masquer un nom dans l'index du `.par` ou poser un fichier libre ne sert
donc à **rien** pour ces six-là. `--obj-db-libre` masque le `n` de `obj_db.bin`
dans cet en-tête (un octet, `0x18041381C`), et le résolveur passe à la suite.
`auth_3d_db` n'y est **pas** — c'est la seule base dont le masquage du `.par`
fonctionnait, et c'est la preuve croisée.

### 17.4 Le mur : cloner son entrée ne clone PAS le mur (2026-09-10, 2e essai)

Le décor ajouté s'est affiché **avec ses flammes et sans ses barrières**.
Les deux manques avaient été traités de la même façon — une entrée clonée dans
la table de la tâche — et une seule des deux corrections pouvait marcher.

**Pourquoi les flammes, oui.** La table `TaskEffectAuth3D` porte un pointeur
vers une **liste de numéros d'uid**. On l'a reconstruite avec *nos* numéros
(3475, 3473, 3474 au lieu de 1193, 1191, 1192). Rien d'autre n'y est nommé.

**Pourquoi le mur, non.** L'entrée de `TaskEffectWall` ne porte **que des
pointeurs** : tout le mur est dans les **trois blocs** qu'ils désignent, et ces
blocs nomment leurs objets par `(objset << 16) | rang` — l'objset du **modèle**.

| champ | bloc de `djo` | contenu |
|---|---|---|
| `+0x08` | `0x180352060` | **28 morceaux** de `0x2C` : `{objet, 10 flottants}`, fin `-1` |
| `+0x10` | `0x180352560` | les **uid**, entiers, fin `-1` : `[1194]` |
| `+0x18` | `0x180352568` | les **paires** de `0x10` : `{intact, cassé, uid, uid}`, fin `-1` |
| `+0x20` | 0 | recopié dans `[tâche+0xD58]` |
| `+0x28`/`+0x30`/`+0x38` | 0 | trois arguments de plus de `0x1800848C0` |

Les 28 morceaux **sont** la barrière du ring, et ils se lisent comme un plan :

    4 x objset 28 rang 113  STGDJO_EFF_POLE    aux quatre coins (+-6, +-6),
                                               tournés -45 / 45 / 135 / 225
   24 x objset 28 rang  47  STGDJO_EFF_FENCE   a +-1, +-3, +-5 le long des
                                               quatre côtés, 0 / -90 / 180 / 90

et la paire dit ce qui les remplace quand elles cassent :
`{28:47 FENCE, 28:48 FENCE_KOWARE, 1194, 1194}`, avec
`uid.1194.value = A STGDJO_EFF_KABE_REACT`.

Un clone octet pour octet de l'entrée renvoie donc à **l'objset 28**, qui n'est
pas chargé dans un build d'ajout, et à **l'uid 1194**, qui est d'une autre
catégorie. `TaskEffectWall` ne trouve rien à poser : **pas de barrière, et pas
un message.**

**Le correctif** (`patch_moteur.mur_charge_modele` + la boucle des entrées
neuves) recopie les trois blocs dans `.decors` en substituant :

| | |
|---|---|
| l'objset | 28 → celui de `--objset` (6150), **le rang ne bouge pas** |
| les uid | 1194 → 3476, retrouvé par sa valeur renommée dans la base **posée** |
| les pointeurs `+0x08`/`+0x10`/`+0x18` | repointés ; leurs relocations existaient déjà chez le modèle, et le patcheur **refuse** si ce n'est pas le cas |

Le patcheur refuse aussi un bloc qui nommerait un objset autre que celui du
modèle, ou un uid absent de la liste du mur : on ne devine aucune
correspondance.

**Le contrôle qui manquait.** `controle_decor_neuf.py` §6 lit maintenant les
**deux** tables dans la DLL patchée, suit les trois blocs du mur et vérifie
que chaque objet nomme *notre* objset avec un rang qui existe dans l'archive
posée, et que chaque uid est de la catégorie `EFFSTG<CODE>`. Contrôle négatif :
l'entrée 43 — un clone de `djo` non corrigé, laissé exprès dans le build —
rend **36 fautes**, dont les 28 morceaux de mur. C'est exactement ce que
l'entrée 42 disait la veille, sans que rien ne le regarde.

**La leçon de forme, et c'est la troisième fois qu'elle se paie.** Une table
indexée par le décor a deux façons de mentir : ne pas avoir d'entrée (§17), ou
en avoir une qui **désigne les données du modèle**. Un clone n'est un clone que
si ce qu'il pointe est clone aussi. Avant de cloner une entrée, il faut lire
**ce qu'elle pointe** — et se demander ce qui, là-dedans, nomme le décor.

### 17.5 La SEPTIÈME table : les tâches d'effet à créer (2026-09-10, 3e essai)

L'entrée de mur de l'étage 42 était juste, et les barrières restaient
invisibles. La raison est un cran au-dessus : **`TaskEffectWall` n'existait
pas** pour le décor ajouté.

Les deux témoins de Frédéric l'ont encadrée sans ambiguïté :

| build | décor | barrières |
|---|---|---|
| `dojo_5r_repli.cmd` | `djo`, indice 11 (archive FS, objset 28) | **oui** |
| `dojo_5r_repli.cmd` | `d5r`, indice 42 (archive 2008, objset 6150) | non |
| `decor_5r_akira.cmd` | l'archive 2008 **à la place** de `djo`, indice 11 | **oui** |

Même binaire, même archive de 2008 : ce n'est donc ni la géométrie, ni la table
des murs. C'est l'**indice**.

#### Une entrée de `0x18034D570` n'est pas une liste, c'en est DEUX

Ce document écrivait : « les 41 entrées réelles sont **toutes vides** ».
C'était vrai des **quatre premiers octets**, et faux de l'entrée :

    +0x00   8 identifiants d'objset a charger EN PLUS, fin -1     (toutes vides)
    +0x20  16 indices de TACHES D'EFFET a creer,       fin -1     (PAS vides)

Le `+0x20` est lu par **`0x18006F380`**, le créateur des tâches d'effet, que
`FUN_18006F620` a pointé sur l'entrée du décor :

```c
for (p = &DAT_18034D530; *p != -1; p++)  creer_tache(*p);        // toujours
for (i = 0; i < 16; i++)                                          // par decor
    creer_tache(*(int *)(liste + 0x20 + i*4));
```

Les noms sont **en clair**, dans le tableau de pointeurs `0x18034E4D0` :

| | | | |
|---|---|---|---|
| 0 `EFFECT_HIT` | 1 `EFFECT_AUTH3D` | **2 `EFFECT_WALL`** | 3 `EFFECT_LEAF` |
| 4 `EFFECT_WATA` | 5 `EFFECT_SNOW` | 6 `EFFECT_YUKA` | 7 `EFFECT_RIPPLE` |
| 8 `EFFECT_RAIN` | 9 `EFFECT_THUNDER` | 10 `EFFECT_DOWN` | 11 `EFFECT_MOVE` |
| 12 `EFFECT_RINGOUT_SPLASH` | 13 `EFFECT_WATER_RING` | 14 `EFFECT_SPLASH` | 15 `EFFECT_SNOW_RING` |
| 16 `EFFECT_FOG_ANIM` | 17 `EFFECT_WET_CLOTH` | 18 `EFFECT_FOG_RING` | 19 `EFFECT_BREATH` |
| 20 `EFFECT_PARTICLE` | 21 `EFFECT_POISON` | 22 `EFFECT_ELE_BOARD` | |

**Toujours créées** (`0x18034D530`) : 0 HIT, 1 AUTH3D, 10 DOWN, 11 MOVE,
20 PARTICLE, 21 POISON. **`EFFECT_WALL` n'en est pas.** `djo` (11) demande
`[2]` ; **32 des 41 décors** demandent 2 = WALL, et la table dit aussi qui a
de la pluie, de la neige, du brouillard :

    4  : WALL RIPPLE SPLASH WET_CLOTH        16 : WALL SNOW BREATH
    5  : WALL LEAF                           21 : WALL SNOW BREATH WET_CLOTH
    13 : WALL THUNDER FOG_ANIM               23 : WALL RINGOUT_SPLASH WET_CLOTH
    14 : WALL FOG_ANIM ELE_BOARD             24 : WALL THUNDER
    15 : WALL WATER_RING RIPPLE SPLASH       0 3 25..29 40 : aucune

Cela **répond d'avance** à la question laissée ouverte au §17.1 (« les autres
tâches d'effet n'ont pas été ouvertes ») : elles n'ont pas de borne à lever, il
suffit que l'entrée du décor les demande.

#### Pourquoi les flammes marchaient et pas le mur

`EFFECT_AUTH3D` est **toujours créée** — donc les flammes, qui sont des
animations auth_3d, s'allumaient. `EFFECT_WALL` ne l'est pas : elle n'existait
pas, sa table indexée par le décor n'était jamais consultée, et les 28 morceaux
du mur restaient lettre morte. Et la **collision** était correcte parce qu'elle
ne vient pas de là : elle est posée depuis le descripteur `+0xB8`/`+0xC0` par
`0x18010CA20`…`0x18010CA60`, dans le chargeur de décor. D'où le symptôme exact :
**un mur qu'on ne voit pas et contre lequel on bute.**

#### Le correctif

Les entrées neuves de `0x18034D570` sont maintenant un **clone complet de
l'entrée du modèle**, comme le descripteur et comme l'entrée de mur — au lieu
d'un clone de l'entrée 0, qui ne demande aucune tâche. Le patcheur refuse si la
liste du modèle n'a pas de terminateur ou si elle est vide.

`controle_decor_neuf.py` a un **§7** qui lit la liste dans la DLL patchée et la
compare à celle du modèle.

#### La leçon, et c'est la même que 17.4, d'un cran

Un clone n'est un clone que si ce qu'il pointe l'est aussi (§17.4) — **et si
l'entrée entière est clonée**. « Toutes les entrées sont vides » était une
mesure faite sur les quatre premiers octets d'un enregistrement de 96. Une
entrée se compare **en entier** à celle du modèle, ou pas du tout.

## 18. LES DIX-NEUF DÉCORS DE VF5 R, AJOUTÉS D'UN COUP (2026-09-10)

Le dojo ajouté marche : les mêmes dix-neuf pièces de machinerie servent pour
les dix-huit autres. Ce qui change, c'est qu'un lot n'est pas dix-neuf fois un.

### 18.1 Ce que VF5 R a, et ce qu'il n'a pas

VF5 R n'apporte **aucun décor** que l'APM3 n'ait pas — il a les mêmes, moins
`du5`. Ce qu'il apporte, ce sont des **versions plus riches** des mêmes lieux
(`djo` +8,1 Mo, `sin` +8,1, `smo` +7,3, `nyc` +6,9, `du3` +4,3). Les ajouter,
c'est mettre les deux générations côte à côte.

Le relevé croisé — les 41 descripteurs du binaire contre
`extracted/decors/VF5R/` — donne :

| | |
|---|---|
| **19 décors COMPLETS** | ban ter nyc cas riv jin sin djo umi hai are slk yuk tak aur bar tan gym smo |
| `du1`..`du4` | il manque `auth_3d/STGDU<n>.farc` : VF5 R range la scène des quatre décors de Dural sous **un seul** nom, `STGDUR.farc`. Correspondance à établir, pas à deviner |
| `du5` | **n'existe pas** dans VF5 R |
| `tst ts2 ts3 wht trm cid trs evo00..evo09` | emplacements d'essai, 0 à 1,2 Mo, sans animation |

### 18.2 La table, à un seul endroit : `tools/variantes_5r.py`

`decor_neuf.py` pose, `patch_moteur.py` patche, `controle_decors_5r.py`
vérifie : les trois lisent **la même** table `(modèle, code, indice, objset)`.
C'est la leçon de `--variantes-djo` (2026-09-09) : un emplacement ne vit qu'à
un endroit.

Codes : `<1re lettre><3e lettre>5` — unique sur les dix-neuf, ne heurte aucun
code du jeu. `djo` garde `d5r`, parce qu'on ne renomme pas un build validé pour
l'élégance d'un schéma. Indices **42 à 60**, objsets **6150 à 6168** (plage
libre 6150..6349).

### 18.3 CHAQUE DÉCOR CLONE SON PROPRE MODÈLE

C'est le point qui commande tout le reste. Un décor ajouté n'est pas un clone
de `djo` : c'est un clone du décor **de Final Showdown correspondant**, dans
les **cinq** tables où il apparaît :

| | |
|---|---|
| le **descripteur** | musique, `+0xB8`/`+0xC0` (l'anneau), aire, propriétés de rendu |
| la table des **codes** | l'éclairage |
| les **objsets et tâches d'effet** (`+0x20`) | `EFFECT_WALL`, `SNOW`, `RIPPLE`… — §17.5 |
| la table des **murs** | et ses blocs de charge, §17.4 |
| la table des **animations d'effet** | par numéro d'uid |

### 18.4 Les quatre champs de mur qu'il a fallu décoder

Le dojo n'utilisait que trois blocs. Sept des dix-neuf modèles en portent
d'autres, et ils nomment eux aussi des objets et des uid :

| champ | forme | qui |
|---|---|---|
| `+0x20` | un **second** tableau de morceaux, même forme que `+0x08` (0x2C) | nyc |
| `+0x28` | **exactement deux** uid — l'animation du grillage, `EFF_SAKU_UP` / `_DOWN` (柵 = grillage) | yuk, gym |
| `+0x30` | des enregistrements de 0x10 `{objet, uid, ., .}`, fin −1 : les objets cassables | umi, hai, aur, tan |
| `+0x38` | un uid par enregistrement de `+0x30`, −1 quand il n'y en a pas | umi, hai, aur, tan |

Trois surprises, toutes mesurées :

* **`-1` est une valeur légitime** dans un champ d'objet : `ban` s'en sert pour
  dire qu'un panneau n'a **pas** de version cassée ;
* **les uid ne sont pas tous dans la liste `+0x10`** : `umi` cite 3361
  (`STGUMI_EFF_SAKU_BROKEN`) dans `+0x30`. On relève donc **tous** les uid du
  mur avant de traduire, en un seul appel ;
* **`tan` désigne un objet de `hai`** : son `+0x30` porte `34:545`, l'objet de
  `hai`, avec ses propres uid — l'enregistrement de `hai` a été recopié chez
  SEGA et seul l'uid a changé. L'objset n'est pas chargé quand on joue `tan`,
  donc l'objet ne fait rien, **dans le jeu d'origine déjà**. Le clone le
  recopie tel quel et le patcheur le **dit**.

### 18.5 Un modèle sans mur n'en donne pas

`riv` et `smo` n'ont **aucune** entree dans la table des murs — c'est une liste
d'association, tous les décors n'y sont pas. Leur fabriquer une entrée, fût-elle
inerte, ferait pointer le clone sur le mur de `djo` : exactement le défaut du
§17.4. Le patcheur n'en écrit donc pas, et `controle_decors_5r.py` vérifie que
l'entrée est **présente si et seulement si** le modèle en a une.

### 18.6 L'accès : un anneau par case

`--variantes-5r` pose **dix-neuf anneaux** de deux indices, un par case de la
grille : la barre espace fait passer la case de sa version Final Showdown à sa
version VF5 R, et le nom de la génération s'affiche. Dix-neuf des vingt et une
cases ont leur double ; les deux autres sont la case ALÉATOIRE et `du1`.

Cela a demandé de porter `VARIANTES_MAX_ANNEAUX` de 4 à **20** :

* les trois tableaux de la greffe (`VAR_COMPTES`, `VAR_IDX`, `VAR_TEXTES`)
  étaient à des offsets **en dur** ; ils sont maintenant dérivés, sinon ils se
  seraient recouverts en silence ;
* la borne du balayage, `cmp ecx, 20*8` = 160, ne tient plus dans un **imm8**
  signé : elle passe en imm32 au-delà de 127 ;
* `GREFFE_TAILLE` passe de `0x1000` à `0x3000` — le tableau des noms pèse
  20 × 8 × 32 = 5120 octets à lui seul.

**Et il y en avait un QUATRIÈME, oublié** (payé le 2026-09-10, « nombreux
plantages ») : `VAR_NUM`, le numéro courant de chaque anneau, gardait ses
**quatre** entrées en dur à `0x600`. Au cinquième anneau il lisait — et
**écrivait** — dans `VAR_RANG`, puis dans `VAR_DESC`, le descripteur de texte.
La sonde `pister_plantage.py` l'a nommé en une passe : `ACCESS_VIOLATION` en
`.greffe+0x1E7`, `mov eax, [rdx+rcx*4]` avec `rcx = 0x43EB0048` — un flottant lu
dans le descripteur. Il est dérivé maintenant, posé après `VAR_TEXTES`, et
`patch_moteur.verifier_disposition()` — appelée par `variantes_greffe` avant
d'assembler — refuse tout recouvrement. Journal (51).

### 18.7 Le contrôle

`controle_decors_5r.py` relit les dix-neuf dans la **DLL patchée** et rend un
tableau d'une ligne par décor : pièces posées, `obj_db`, `auth_3d_db`, tâches
d'effet, mur. Il refuse un objet ou un uid qui ne serait pas le nôtre, une
liste de tâches différente de celle du modèle, ou une entrée de mur en trop.

---

## 19. LES SEPT AUTRES TABLES D'EFFET (2026-09-10)

Frédéric : « tu vas finir d'analyser les sept autres tables d'effet (BREATH,
FOG_ANIM, SNOW, SPLASH, THUNDER, MOVE, DOWN) et les sons d'ambiance pour les
rétablir dans les décors ». C'est fait, et l'analyse a trouvé **une mine**.

### 19.1 Trois formes, et elles ne coûtent pas la même chose

`0x18006F380` donne l'indice du décor à chaque tâche d'effet créée, par le
créneau 7 de sa vtable. Chaque tâche va ensuite chercher ses données **à sa
façon**. Le décompilateur les a toutes rendues ; il y a exactement trois formes.

| forme | tâches | table | si l'indice manque |
|---|---|---|---|
| **tableau dense** indexé par le décor | `DOWN` (10), `MOVE` (11) | `0x18034FF20`, `0x180350820` — 41 `int` | **mine** : lit ce qui suit dans `.rdata` |
| **liste à pas fixe**, fin `-1` | `SNOW` (5) | `0x180643340`, pas `0x58` | rien |
| **chaîne de comparaisons déroulée** | `BREATH` (19), `FOG_ANIM` (16), `SPLASH` (14), `THUNDER` (9) | `0x1806430C0`, `0x180643130`, `0x180643490`, `0x180351B98` | rien, mais le nombre d'entrées est **dans le code** |

### 19.2 La mine : `DOWN` et `MOVE`

`t[indice]` se lit **sans aucune vérification** — ni terminateur, ni borne :

```c
iVar1 = *(int *)(&DAT_18034ff20 + (longlong)param_2 * 4);   // TaskEffectDown
```

À 41 entrées suivies de texte, tout indice ≥ 42 rendait des octets d'ASCII
(`1802723668` = `"dnuo"`) donnés à l'auth_3d **comme un numéro d'uid**. Et ces
deux tâches-là sont dans les six **toujours créées** (`0x18034D530`) : les
dix-neuf décors ajoutés y passaient tous, à chaque combat, depuis le début.

Les deux tableaux passent donc de 41 à `n` entrées dans `.decors`. Les valeurs
sont des uid, et elles se **traduisent** : `DOWN` = `STG<X>_EFF_DOWNKEMU` (la
poussière quand un combattant tombe — `SPLASH_DOWN` sur `riv` et `slk`, qui sont
des décors d'eau), `MOVE` = `STG<X>_EFF_DASH`. **`DASH` n'existe pas en 2008** :
c'est un ajout de Final Showdown, et les dix-neuf reçoivent `-1`, qui est la
bonne valeur.

### 19.3 Ce que le compilateur a déroulé, il l'a aussi payé en octets

Les quatre dernières tables ne se déplacent pas toutes seules : le compilateur a
déroulé la boucle de recherche en autant de `cmp` qu'il y a d'entrées.

```
0x180070E00  cmp edx, [rip+…]   ; 16 yuk
0x180070E1B  cmp edx, [rip+…]   ; 18 aur      TaskEffectBreath
0x180070E25  cmp edx, [rip+…]   ; 21 du1
```

Mais une chaîne déroulée occupe **entre 26 et 63 octets**, et un balayage tient
dans 26. On la remplace donc **sur place**, sans caverne :

```
    lea  CUR, [rip + table]
  L: cmp  dword ptr [CUR + décalage], -1     ; le terminateur
    je   AUCUN
    cmp  IDX, dword ptr [CUR + décalage]
    je   TROUVÉ
    add  CUR, pas
    jmp  L
  AUCUN:  jmp <sortie d'origine>
  TROUVÉ: <épilogue> puis on retombe sur la suite d'origine
```

| tâche | place | balayage | index | résultat | sortie |
|---|---|---|---|---|---|
| `BREATH` | 63 o | 33 o | `edx` | `r15` | `0x180070F92` |
| `FOG_ANIM` | 32 o | 24 o | `eax` | `rdx` | `0x180071B91` |
| `SPLASH` | 60 o | 27 o | `ebp` | `rsi` | `0x180080C6E` |
| `THUNDER` | 26 o | 26 o | `edx` | `rdi` | `0x180082693` |

**Le nombre d'entrées quitte le code pour les données.** Le patcheur refuse si le
balayage ne tient pas — on ne tronque jamais un patch de code.

`THUNDER` est le cas particulier : ses indices (13 `hai`, 24 `du4`) sont des
**littéraux**, pas un champ. Ses dossiers font `0x20` octets dont sept d'uid
(`SKY_DOME_H/M/L`, `KAMINARI1..4`) et un mot de bourrage en `+0x1C` — c'est là
qu'on écrit l'indice, et le balayage compare `[rdi+0x1C]`. Le registre porte
alors directement le dossier, comme avant.

### 19.4 Ce que chaque décor récupère

    bn5 SPLASH    rv5 SPLASH    sk5 SPLASH    ae5 FOG_ANIM
    hi5 THUNDER FOG_ANIM        yk5 SNOW BREATH        ar5 BREATH
    les dix-neuf : DOWN (DOWNKEMU), et l'ambiance sonore de leur modèle

`EFFETS_SERVIS` passe de `(2,)` à `(2, 5, 9, 14, 16, 19)`. Restent fermées, et
c'est écrit : `LEAF` (3), `RIPPLE` (7), `WATER_RING` (13) et `SNOW_RING` (15),
qui **partagent** `setStage 0x180076B00` ; `RINGOUT_SPLASH` (12), `WET_CLOTH`
(17) et `ELE_BOARD` (22), qui n'ont pas de `lea rip` en tête. Leur forme n'est
pas mesurée : on ne les demande donc pas.

### 19.5 Une animation appartient à UN mécanisme

La lecture des sept tables a nommé trois mécanismes de plus, et `hi5` en était la
victime : `animations_en_plus()` lui donnait `KAMINARI1..4` et `SKY_DOME_H/L/M`
**dans la liste auth_3d**, où elles auraient tourné en boucle — trois dômes de
ciel superposés et un éclair permanent. Elles appartiennent à `TaskEffectThunder`.
Idem `TOIKI` (le souffle dans le froid) pour `TaskEffectBreath`, sur `yk5` et
`ar5`. `EFFETS_AUTRES_MECANISMES` les reprend.

La règle n'a pas changé — **une animation appartient à un mécanisme** — c'est la
mesure qui a rattrapé la prémisse.

### 19.6 Une relocation sur un pointeur NUL fabrique un pointeur non nul

C'est la cause du dernier plantage d'aurora, et la sonde l'a donnée en une ligne :

    ACCESS_VIOLATION en 0x180084BF0, `mov eax, [rbp+4]`, rbp = 0x00007FF8892E0000
    base du module - 0x180000000 = 0x7FFA092E0000 - 0x180000000 = 0x7FF8892E0000

**`rbp` EST le delta de rebasage.** Le champ valait donc zéro dans le fichier et
portait quand même une relocation : le chargeur y a ajouté le delta, et
`if (param_6 != 0)` — la seule garde — a laissé passer.

C'est le `+0x30`/`+0x38` qu'on met à zéro quand 2008 n'a pas l'animation des
objets cassables (`ui5`, `hi5`, `ar5`, `tn5`) : l'entrée de mur est clonée **avec
les relocations du modèle**, puis le champ est remis à zéro — et la relocation
reste. Le garde-fou est général : le patcheur retire de la liste toute relocation
qui vise un quadruple mot nul, et le dit.

### 19.7 Le contrôle a été rendu honnête

`controle_decors_5r.py` avait sa **propre copie** de `EFFETS_SERVIS` — exactement
le défaut qui avait coûté onze fausses fautes la veille. Il lit désormais la
valeur chez le patcheur, et il vérifie en plus, pour chaque décor :

  * toute tâche demandée a bien une entrée à **notre** indice dans **sa** table
    (relue dans la DLL patchée, en suivant le `lea` — si une table n'a pas
    déménagé, la lecture tombe sur l'ancienne et le dit) ;
  * `DOWN[indice]` et `MOVE[indice]` valent `-1` ou un uid de **notre**
    catégorie `EFFSTG<CODE>`.

Témoin : `BREATH` trouve 56 et pas 57, `THUNDER` trouve 51 et pas 52, `SNOW`
trouve 54 et pas 55.

---

## 20. LES SEPT TÂCHES D'EFFET QUI RESTAIENT (2026-09-10)

Analysées pendant que Frédéric testait `decors_5r.cmd`. **Rien n'a été touché au
binaire** : lecture sur `.origine` et sur la copie du projet Ghidra.

Le point de départ était faux : ce document disait que `LEAF`, `RIPPLE`,
`WATER_RING` et `SNOW_RING` « partagent `setStage 0x180076B00` », comme si
c'était un obstacle. `FUN_180076B00` est en réalité un **simple setter** :

```c
void FUN_180076b00(longlong param_1, undefined4 param_2)
{ *(undefined4 *)(param_1 + 0x58) = param_2; return; }
```

Il range l'indice, et c'est **la mise à jour** qui va chercher la table.
`TaskEffectWetCloth::setStage` fait pareil (`+0x60`). Chercher la table dans le
`setStage` ne pouvait donc rien donner. Les vtables se lisent d'un coup avec
`py -3 tools/rtti.py --grep TaskEffect` — le créneau 7 est `setStage`, le
créneau 1 l'init.

### 20.1 Le tableau

| n° | tâche | où est la donnée | forme | ce qu'elle porte | décors 5R | coût |
|---|---|---|---|---|---|---|
| 3 | `LEAF` | `0x180643248`, lu dans l'**update** `0x180074EC0` | chaîne déroulée ×2, pas `0x0C` | 2 objets `(objset<<16)\|rang` | `tr5`, `jn5` | balayage + substitution d'objset |
| 7 | `RIPPLE` | `0x1806432E0`, via `FUN_18007AE10` depuis l'init | chaîne déroulée ×2, pas `0x2C` | flottants + 1 id de sprite | `bn5`, `sk5` | balayage ; **clone pur** |
| 12 | `RINGOUT_SPLASH` | `0x180350C10`, dans `setStage 0x180079A30` | tableau borné par une **adresse de fin littérale**, 4 × `0x20` | 2 uid `SPLASH_DOBON`/`_S` + un **pointeur** de chaîne | `rv5`, `jn5`, `sn5` | déménagement + fin à repointer + relocation |
| 13 | `WATER_RING` | **aucune table** | un **littéral** `0x27006E` dans `0x180085620` | l'objet 39:110 = `stgslk_water_ring` | `sk5` | **FAIT** le 2026-09-10 : stub dans `.greffe`, cf. `REPRISE.md` (60) |
| 15 | `SNOW_RING` | `0x180643450`, via `FUN_18007D820` | **une seule** entrée, pas `0x2C` | 4 id de sprite + l'objet 50:233 | `yk5` | balayage + substitution d'objset |
| 17 | `WET_CLOTH` | **aucune table** | un scalaire choisi par `index == 19` | rien qui soit propre au décor | `bn5`, `rv5`, `jn5`, `sn5` | **zéro** |
| 22 | `ELE_BOARD` | — | **bouchonnée** | — | `ae5` | **rien à faire** |

### 20.2 Les deux qui sont gratuites

**`WET_CLOTH` (17) n'a pas de table.** Son init lit l'indice rangé en `+0x60` et
ne s'en sert que pour choisir entre deux flottants :

```c
auVar1 = vpcmpeqd_avx(ZEXT416(*(uint *)(param_1 + 0x60)), ZEXT416(0x13));
auVar1 = vblendvps_avx(ZEXT416(DAT_180350C00), ZEXT416(DAT_18034AF50), auVar1);
```

`0x13` = 19 = `bar`. Or aucun des quatre décors qui demandent `WET_CLOTH` (4
`ban`, 8 `riv`, 9 `jin`, 10 `sin`) n'est le 19 : leurs clones prendront la même
branche que leurs modèles, sans rien changer. **Elle se rouvre telle quelle.**

**`ELE_BOARD` (22) est bouchonnée dans ce build.** Son créneau 7 pointe sur
`0x180215C00`, un stub générique à **un seul argument** (`*(byte*)(p+0x58) = 0`)
— ce n'est même pas un `setStage`. Et son init est `FUN_180029FB0` :

```c
undefined1 FUN_180029fb0(void) { return 1; }
```

`are` (14) la demande et n'obtient rien, **dans le jeu d'origine déjà**. La
rouvrir pour `ae5` ne rendrait rien de plus, mais ne coûterait rien non plus :
c'est de la fidélité au modèle, pas un effet. C'est le motif dominant de ce
build (cf. mémoire « Un dernier verrou bouchonné »).

### 20.3 `WATER_RING` : un objet en dur dans le code

Il n'y a pas de table du tout. L'init pose un drapeau global
(`gestionnaire+0x330 = 1`), et le créneau 4 dessine **un objet nommé par un
littéral** :

```c
if (*(char *)(param_1 + 0x5c) != '\0')
    FUN_1800ec520(0x27006e, FUN_180085680, 0);
```

`0x27006E` = `(39 << 16) | 110` = l'objet 110 de l'objset 39, celui de `slk` —
et l'archive de 2008 le porte au **même rang** : `110 = stgslk_water_ring`. Le
moteur est donc câblé sur un seul décor. Pour `sk5` il faudrait une greffe qui
substitue l'objset du décor courant à `39` — cinq octets au site d'appel et une
caverne. C'est le seul des sept qui demande du code neuf plutôt qu'un balayage.

### 20.4 `LEAF` et `SNOW_RING` nomment des objets, comme le mur

`LEAF` : deux entrées de `0x0C`, et les deux champs qui suivent l'indice sont des
`(objset << 16) | rang` — **exactement la convention du mur** (§17.4) :

    decor 5 (ter)  ->  42:1  42:0     0 = stgter_dummy_kage, 1 = stgter_dummy_sakura
    decor 9 (jin)  ->  35:524 35:523  absents de l'archive de 2008

`sakura`, ce sont les pétales. `tr5` peut donc les avoir ; **`jn5` non** : les
rangs 523 et 524 ne sont pas dans son archive de 2008. C'est le même verdict que
pour les animations manquantes — on retire, on ne devine pas.

`SNOW_RING` : **une seule** entrée, pour 16 `yuk`, et son `+0x24` est
`(50 << 16) | 233` = `stgyuk_eff_snowring`, présent dans l'archive de `yk5`.

### 20.5 `RINGOUT_SPLASH` : la troisième forme de borne

    piVar5 = &DAT_180350c10;
    do { ... piVar5 += 8; } while ((longlong)piVar5 < 0x180350c90);

Ni terminateur, ni compte : une **adresse de fin**, littérale, dans le code.
Quatrième forme de borne rencontrée sur ce chantier (après l'immédiat, le
`cmov` avec repli, et la taille en octets) — cf. mémoire « Chercher la borne ».
Quatre entrées de `0x20` : 8 `riv`, 10 `sin`, 9 `jin`, 23 `du3`.

Le dossier porte deux **uid** — `STG<X>_EFF_SPLASH_DOBON` et `_DOBON_S`, le
plouf quand un combattant tombe à l'eau — et un **pointeur** vers la chaîne
`"fd_vfv_landing_water"` en `+0x10`, donc une relocation à recopier. Les trois
décors concernés ont bien les deux animations en 2008 :

    RV5  STGRV5_EFF_SPLASH_DOBON  STGRV5_EFF_SPLASH_DOBON_S
    JN5  STGJN5_...               SN5  STGSN5_...

Et c'est **le même piège que `KAMINARI`** (§19.5) : `animations_en_plus()` les
donne aujourd'hui à la liste `auth_3d` de `jn5` et `sn5`, où elles tournent en
boucle. Le jour où `RINGOUT_SPLASH` sera servie, `SPLASH_DOBON` devra rejoindre
`EFFETS_AUTRES_MECANISMES`.

### 20.6 Ce que ça change pour le décor

    tr5  LEAF                       bn5  RIPPLE WET_CLOTH
    sk5  RIPPLE WATER_RING          rv5  WET_CLOTH RINGOUT_SPLASH
    jn5  WET_CLOTH RINGOUT_SPLASH   sn5  WET_CLOTH RINGOUT_SPLASH
    yk5  SNOW_RING                  ae5  ELE_BOARD (inerte)
    jn5  LEAF : impossible, l'objet n'est pas dans l'archive de 2008

---

## 21. LE VF5 D'ORIGINE (ver.B) : CE QUE SON BINAIRE DIT, ET COMMENT ON L'AJOUTE (2026-09-11)

Lanceur `tools\decors_vf5.cmd`, lot `tools/variantes_vf5.py`, contrôle
`tools/controle_decors_vf5.py`. Journal (63).

### 21.1 Les tables de ver.B, dans son ELF

`extracted/LIND_VF5/id/disk0/vf5` (ELF i386, build 20070530). `.rodata` en
`0x08521BA0` (fichier `0x4D9BA0`). Chaque table a été trouvée par une valeur
connue, puis parcourue jusqu'à ses bornes :

| table | adresse | forme | trouvée par |
|---|---|---|---|
| descripteurs | `0x852F220` | 28 × 0x70 | le pointeur vers « STGDJO » |
| tâches d'effet (+ objsets en plus) | `0x85FF520` | 28 × 0x60, comme `0x18034D570` | la liste de `slk` `[2,12,7,13,16]` |
| murs | `0x8600480` | {indice, morceaux, uid, paires, morceaux 2} × 0x14 | le pointeur vers les morceaux de `djo` |
| animations d'effet | `0x86001E0` | {indice, liste} × 8 | la liste de `djo` (HATA FIRE FIRE_REFLECT) |
| noms des tâches | pointeurs vers `EFFECT_HIT`… | 19 noms | la chaîne |

Descripteur de ver.B : `+0x00` nom auth_3d, `+0x04` nom des effets, `+0x08`
objset, `+0x0C` **second objset** (le ciel des Dural), `+0x10` GND, `+0x14` SKY,
`+0x18` SDW, `+0x1C` vide, `+0x20` REFLECT, `+0x24` REFRACT (jin seul),
`+0x28..+0x30` reflets d'objectif (textures), `+0x34` échelle, `+0x40`
collision, `+0x4C` musique, `+0x68`/`+0x6C` = FS `+0xDC`/`+0xE0`. Les rôles sont
vérifiés PAR NOM d'objet sur les 28 entrées.

Morceau de mur : `{objet, x y z, rx ry rz, sx sy sz}` = 0x28 (FS : 0x2C, un
entier inséré à +4).

La base de ver.B a les mêmes **19** tâches que VF5 R (pas de MOVE) ; son `+0x00`
nomme l'objset 45 = `EFFCMN`, que FS charge **toujours** (`0x18034D510`).

### 21.2 Les textures : la numérotation de ver.B n'est pas celle de FS

    objsets de VF5 R poses : tout identifiant connu de FS = une texture du MEME decor
    objsets de ver.B       : 3 277 / 3 975 identifiants = AUTRE CHOSE chez FS

D'où la renumérotation (`variantes_vf5.carte_textures`, déterministe) : nom
connu de FS → numéro de FS ; nom inconnu (1 381) → numéro libre dans les trous
de la `tex_db` de FS, hors de ceux de VF5 R (`extracted/_tex_ids_5r.json`). La
`tex_db` de ver.B est extraite en `extracted/decors/VF5_VERB/_db/` (avec
`obj_db` et `auth_3d_db`) ; elle a 24 octets de bourrage `0x90` en fin, que
`tex_db.py` refuse — `variantes_vf5._tex_db` lit sans.

Les `.a3da` de ver.B ne nomment AUCUNE texture (clés `curve`, `object`, `light`,
`camera_root`) : l'objset est le seul endroit à renuméroter.

### 21.3 Ce qui vient de ver.B, ce qui vient du modèle FS

| vient de ver.B (relu) | vient du modèle FS (cloné) |
|---|---|
| géométrie, textures (renumérotées), collision, éclairage (5 fichiers), animations | musique (9 reprises), anneau, propriétés de rendu, aire, `envmap_correct_*` (du `.par`), son d'ambiance |
| les cinq objets, les reflets d'objectif | les champs inconnus (`+0x3C`, `+0xD0..`) |
| la liste des tâches d'effet | les DOSSIERS des tâches servies (neige, souffle, tonnerre, ondes…) |
| le mur (converti) | — |
| la liste des animations d'effet | DOWN (poussière de chute) : l'uid du modèle, traduit par nom |

### 21.4 Dural

Une géométrie (`stgdur` → `drb`, objset 6186), quatre ciels (`stgdu1..4` →
`d1b`, `d2b`, `d3b`, `d4b`, objsets 6187..6190), quatre éclairages (`dur`,
`du2`, `du3`, `du4`). Les entrées 79..81 n'ont pas de géométrie à elles :
descripteur `+0x10` = 6186, et la liste `+0x00` de `0x18034D570` porte l'objset
du ciel. Planches : `analysis/ciel_verb_du1..4.png` (coucher de soleil, jour,
orage, nuit étoilée).

Modèle FS des quatre : `du1`. Ses descripteurs FS nomment une catégorie
auth_3d `STGDU1` **qui n'existe pas** dans la base de FS — preuve que le moteur
tolère un nom absent. `STGD2B`..`STGD4B` n'y sont pas non plus, comme les
`STGDU2..4` de ver.B.


---

## 22. CHAQUE GÉNÉRATION, SES EFFETS — ET LES SEPT TÂCHES QUI MANQUAIENT (2026-09-11)

Frédéric : « applique à VF5 R ses propres listes, rien ne doit venir de FS,
applique les effets VF5 à VF5, décompile les effets dont on ne sait pas se
servir si c'est nécessaire ». Le tableau du §21.3 est périmé : pour une entrée
SPÉCIALE (R 42-60, ver.B 61-81), la colonne « vient du modèle FS » ne garde plus
que musique, anneau, propriétés de rendu, aire, envmap et son d'ambiance.

### 22.1 La chaîne

    ELF de la génération ──> tools/generation.py ──> Traducteur ──> la DLL
         (relu, vérifié)       (format de FS)       (nos numéros)

`generation.py` est la SOURCE UNIQUE (patcheur et contrôles la lisent). Chaque
emplacement est vérifié à la lecture : l'instruction citée doit NOMMER la table
(`_verifier_ref`), un littéral doit être un `mov`/`cmp` à immédiat
(`_litteral`), un objet doit porter le nom attendu. Sinon : `Refus`.

`Traducteur` : uid par NOM (dernier mot de la valeur, `STG<src>_` → `STG<geo>_`,
catégorie posée `EFFSTG<eff>`) ; textures telles quelles chez R, par nom chez
ver.B, et dans nos objsets ; objets `(objset << 16) | rang` avec le rang
présent dans l'archive posée ; objset entier (YUKA). Ce qu'il ne sait pas
traduire est RETIRÉ, jamais deviné.

### 22.2 Les sept tâches, côté FS

| tâche | FS | forme | remède (greffe, zone `GRE_GEN`) |
|---|---|---|---|
| LEAF 3 | init `0x180074EC0` | 2 `cmp eax,[rip]` déroulés, `{indice, objet 1er, objet 2e}` (dessin `0x180074A50` : `[+0x5C]` puis `[+0x60]`) | `CHAINES['LEAF']` : balayage sur place (27 octets sur 35), `xor r8d,r8d` remis en tête ; table dans `.decors` |
| YUKA 6 | setStage `0x180086660` (ignore l'indice), init `0x1800861A0`/`0x180086300`, dessin `0x180085CB0` | 5 littéraux : `mov ecx,0x18` `0x1800861CB` ; `lea rax,[0x180356620]` `0x1800861EB` et `0x1800863BB` ; `mov edx,0x496` `0x180086675` ; `mov ecx,0x180000` `0x180085D1D` | créneau 7 (`0x18034EE98`) → stub qui écrit `{objset, uid, objet, -, &table}` dans une variable de la greffe (notre dossier ou les valeurs de FS) ; trois `call` vers `mov reg,[rip+var]; ret`, deux `lea` → `mov rax,[rip+var+0x10]` |
| RAIN 8 | init `0x180079170` recopie `0x180643280` (0x5C) dans l'état ; créneau 7 = `ret 0` `0x180007430` | un bloc sans indice | créneau 7 (`0x18034EFF8`) → stub de recopie (le nôtre, sinon celui de FS relu dans `.origine`) |
| RINGOUT_SPLASH 12 | setStage `0x180079A30` | tableau `0x180350C10` 4 × 0x20, fin littérale (`lea rdx` `0x180079B74`) ; pointeur de chaîne en +0x10 | déménage dans `.decors` (relocations), `lea` début/fin repointés ; `call 0x18006F350` (`0x180079729`) → stub « ne pas pousser » si `[élément+0x4C]` est le NaN |
| SNOW_RING 15 | `0x18007D820`, appelée de l'init `0x18007DA8A` | UN dossier `0x180643450` (0x2C) | `call` → stub de recopie → `jmp 0x18007D820` |
| WET_CLOTH 17 | init `0x180085940` | `vpcmpeqd` de l'indice avec `0x13` : 0,4 ou 0,001 | `mov eax,0x13` (`0x1800859AC`) → stub qui rend l'indice s'il est dans la liste « 0,4 » |
| FOG_RING 18 | `0x180072130`, appelée du setStage `0x180072B80` | UN dossier `0x1806431C8` (0x3C), texture en +0x1C (`0x1801957A0`) | `call` → stub de recopie → `jmp 0x180072130` |

Le stub de recopie : `lea rax,[table] ; mov r9d,n ; balayage sur [rax] ;
recopie qword par qword vers le dossier de FS ; jmp <fonction>`. La DERNIÈRE
entrée de sa table est l'original de FS, relu dans `.origine` : un décor de FS
relit exactement ses octets. rax/r8/r9 volatils, rcx/edx intacts.

**L'ordre, établi et non supposé** : `0x18006F380` (état 3) inscrit la tâche
(`0x180245830` → `0x1802456C0`, aucune méthode appelée), appelle
`vtable[7](tâche, indice)`, puis `vtable[10]`. L'init (créneau 1) tourne à la
première trame — WetCloth lit déjà l'indice rangé par son setStage.

### 22.3 Les sept tâches, côté générations

| tâche | VF5 R | ver.B |
|---|---|---|
| LEAF | littéraux `0x84BCAB2` (SAKURA) `0x84BCAD8` (KAGE) | `0x83911F3` / `0x8391229` |
| YUKA | objset `0x84C14C3`, table `0x883A080` (= celle de FS), uid `0x84C0F35`, objet `0x84C1434` | `0x8391E40`, `0x8603940`, `0x8391B97`, `0x83924BC` |
| RAIN | bloc `0x89A1700` (copie `0x84C32C7`.., mêmes décalages) | `.bss` `0x8947460`, constructeur `0x83940FD`.., copie `0x839385E` |
| RINGOUT_SPLASH | `0x883AC00`, 3 × 0x14 (riv sin du3), boucle `0x84C5480` | `0x8604520`, 2 × 0x14 (jin riv), `0x839511C` |
| SNOW_RING | — | `0x8661D00` (yuk) |
| WET_CLOTH | `0x84CB4C0` : `cmp [eax+0x58],0x13 ; cmove` 0,4 (init : drapeau 0) | `0x839BA82` : 0,001 pour tous |
| FOG_RING | `.bss` `0x8BE4DE0`, 2 × 0x3C (jin, du2), constructeur `0x84CCDE4` (rejoué : du2 = FS octet pour octet) | `.bss` `0x8947580` (sin), `0x839CDE7`.. |

**RINGOUT_SPLASH, les deux champs que FS a ajoutés.** Le dossier de FS fait 0x20
octets, ceux de R et ver.B 0x14. FS ajoute `+0x18` au y de la translation de
l'animation (`0x1800796B1`) et pousse `{uid, x, +0x1C, z, …}` dans une liste de
quatre de l'objet `0x180677330` (`0x180079733..0x180079786`). R (`0x84C4E30`,
`0x84C4D20`) et ver.B posent l'animation à la position calculée, sans décalage,
et ne poussent rien. D'où, pour eux : `+0x18 = 0,0` et `+0x1C = 0xFFFFFFFF`,
que le stub de `0x180079729` lit comme « ne pas pousser ». Le lecteur de cette
liste n'a pas été identifié (aucun accès direct ni `[reg+0x108]` hors l'écriture).

### 22.4 Où c'est servi

    LEAF tr5 trb     YUKA bn5 bnb       RAIN br5 ncb
    RINGOUT_SPLASH rv5 sn5 rvb jnb      SNOW_RING ykb
    WET_CLOTH rv5 sn5 br5(0,4) ncb rvb jnb skb ykb     FOG_RING jn5 snb

Les entrées clonées de FS (non spéciales) ne reçoivent aucune de ces tâches :
LEAF n'est pas clonée (`CHAINES_OBJETS`), les autres n'ont pas de dossier, et le
tri final retire toute tâche sans dossier posé.

---

## 23. LES COMPORTEMENTS CÂBLÉS SUR UN NUMÉRO, ET LES DURAL DE VF5 R (2026-09-11)

Journal complet : `REPRISE.md` (66). En bref :

* FS teste en dur des **numéros de décor** (grillage `16 ‖ 39`, reflet de
  gym `39`, plan de coupe S_REFL `10`, bar `0x13`, Auth3D `8` et `0x28`) et
  des **numéros d'uid** (Auth3D : IDOU/KAWA `0x4E8/0x4E9`, FLASH `0x7F4`).
  Une entrée ajoutée ne passe aucun de ces tests. `generation.CABLAGES`
  liste ceux que R et ver.B ont AUSSI (instruction vérifiée) ; le patcheur
  les rend par des stubs (`CABLAGES_APPELS`, `stub_alias`,
  `stub_a3d_setstage`, `stub_uid`, `stub_objet_reflet`), le contrôle les
  relit site par site. Ce que seul FS teste n'est pas rendu.
* Les tests câblés se trouvent par les appelants de l'accesseur « décor
  courant » : `0x18018F580` chez FS (18), `0x8108718` chez R (10). Les tests
  sur `param_2` d'un setStage et sur des uid ne passent PAS par lui : les
  137 méthodes des tâches d'effet ont été décompilées pour les trouver.
* Les quatre Dural de VF5 R (`d15..d45`, 82-85) : leurs catégories de scène
  `STGDU<n>` sont vides chez R comme chez FS — pas de pièce de scène.
* `tools/sonde_decor.py` force un décor, mène le jeu seul au combat et
  capture : c'est lui qui a tranché les grillages, les flashs et les
  fichiers de brouillard.

## 24. LES EMPREINTES DANS LA NEIGE : LE GEOMETRY SHADER QUE LE PORTAGE N'A PAS FAIT (2026-09-11)

Journal complet : `REPRISE.md` (67). En bref :

* Aucun décor de FS ne crée SNOW_RING : son code tourne pour la première
  fois sur PC avec ykb (ver.B). La logique est saine (sonde : les chevilles
  et les orteils ajoutent des milliers d'empreintes par combat ; os et
  squelettes identiques chez ver.B et FS).
* Une empreinte est un point de 6 pixels dans une cible de 512 × 512. Le
  moteur APM3 dessine en Direct3D 11, où un point fait un pixel ; le
  portage a donné un geometry shader (`GSFX`) aux cinq autres programmes de
  points, pas à `snow_footprint..vp`.
* Remède : `tools/shader_empreintes.py` pose `w64/shader_vf5_w64.farc` (le
  seul `snow_footprint..vp`, en `GSFX`) ; `patch_moteur.
  SHADER_EMPREINTES_SITE` fait lire ce membre-là dans notre archive. Celle
  de FS n'est pas touchée ; aucun décor de FS ne dessine d'empreinte.
* À retenir pour toute la suite : **les shaders d'APM3 sont du DXBC** dans
  `w64/shader_pxd_w64.farc` (GSVS / GSPS / GSFX + GSGS), pas les `.fp/.vp`
  ARB des archives Lindbergh. Un effet qui dépend d'un état OpenGL absent
  de Direct3D 11 (taille de point…) peut être muet sans que le code soit
  en cause.
