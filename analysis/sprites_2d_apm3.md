# Le systeme de sprites 2D dans `vf5fs_apm3_origine.dll`

Binaire : `VF5RE/analysis/vf5fs_apm3_origine.dll`, PE x64, base 0x180000000,
sha256 `045c0696...0c837eef`. Lu avec REA/Ghidra 12.1.2, aucune mutation de base.
Le PDB `vf5fs-pxd-w64-Retail_APM3.pdb` est reference mais non charge : aucun nom
de fonction du jeu n'est disponible. Un seul symbole RTTI a survecu et il est
decisif : **`SPRSET::vftable`**, ecrit a l'ouverture de chaque entree de la table.

Tout ce qui suit est **LU** dans le binaire sauf ce qui est explicitement marque
DEDUIT.

## Noms proposes (aucun rename effectue, la plateforme les refuse)

| Adresse | Nom propose | Role (lu) |
|---|---|---|
| `0x180719900` | `g_spr_manager` | pointeur global vers le gestionnaire de sprites (objet de 0x838 octets) |
| `0x180719908` | `g_spr_db` | pointeur global vers la base `spr_db` |
| `0x18018a030` | `spr_manager_create` | alloue 0x838, cree le noeud sentinelle, construit 0x80 listes |
| `0x18018a0d0` | `spr_manager_destroy` | detruit, libere le sentinelle (taille **0x128**) |
| `0x180187ab0` | `spr_init` | **compte les planches** et appelle le peuplement |
| `0x18018c7d0` | `spr_sets_create_all` | **insere N `SPRSET` vides, cles 0..N-1** |
| `0x180187ed0` | `spr_map_buynode` | noeud 0x128 : cle a `+0x20`, valeur a `+0x28` |
| `0x18018a1d0` | `spr_map_alloc_node` | `operator new(0x128)` |
| `0x18018c3b0` | `spr_set_find_and_read_rect` | **resolveur** + lecture du rectangle |
| `0x18018c300` | `spr_rect_read` | lit le rectangle d'un `SPRSET` deja resolu |
| `0x180187a60` | `spr_get_rect_public` | wrapper : db -> handle -> rectangle |
| `0x18018c610` | `spr_db_find` | lookup dans `g_spr_db` (DEDUIT, un seul site d'appel) |
| `0x18018ca20` | `spr_put` | **le consommateur** : decode le handle, lit la table de rectangles |
| `0x180187af0`, `0x180187b10`, `0x180187c00` | `spr_put_kindN` | wrappers publics de `spr_put` |
| `0x180187cf0` | `spr_list_node_new` | alloue le noeud de liste d'affichage (0xf8) |
| `0x18018bbd0` | `spr_disp` | **rendu d'une passe, puis vidage et liberation des listes** |
| `0x180187a10` | `spr_disp_public` | wrapper de `spr_disp` |
| `0x18018b010` | `spr_draw_node` | emet la geometrie d'un noeud d'affichage |
| `0x18018e460` | `spr_db_load_task` | `./rom/2d/` + `spr_db.bin` |
| `0x18018d340` | `spr_db_parse` | deserialise `spr_db.bin` (offsets auto-relatifs) |

Remarque : `0x1803FFBD0` (cite dans la question) est un **autre** global que
`0x180719900`. Le systeme de sprites decrit ici passe exclusivement par
`0x180719900`.

## 1. Le resolveur, et ou vivent les planches

**Il n'y a pas de tableau de planches.** Le gestionnaire porte une
`std::map<uint32_t, SPRSET>` et le resolveur est un `lower_bound` MSVC **inline**,
pas une fonction separee. Noeud de map : `_Left` a `+0x00`, `_Parent` a `+0x08`,
`_Right` a `+0x10`, `_Color` a `+0x18`, `_Isnil` a `+0x19`, **cle (uint32) a
`+0x20`**, **valeur `SPRSET` a `+0x28`** (noeud de 0x128 octets, donc `SPRSET`
fait 0x100 octets).

Ou vit la table :

```
manager = *(void**)0x180719900        ; objet de 0x838 octets
manager + 0x00 : _Myhead  (noeud sentinelle de la map)
manager + 0x08 : _Mysize  (nombre de planches)
manager + 0x10 : 128 std::list de 0x10 octets  (4 passes x 32 sous-priorites)
manager + 0x828: passe courante par defaut (dword)
manager + 0x82c: mode courant par defaut (dword, initialise a 0x11)
```

Le resolveur, lu instruction par instruction a `0x18018ca6d` (dans `spr_put`) :

```
0x18018ca6d: MOV  RBP, [R12]            ; R12 = manager ; RBP = _Myhead
0x18018ca71: SHR  ECX, 0x10
0x18018ca74: MOV  RBX, RBP              ; RBX = "pas trouve"
0x18018ca77: AND  ECX, 0xfff            ; rang = (handle >> 16) & 0xfff
0x18018ca7d: MOV  RAX, [RBP + 0x8]      ; racine
0x18018ca81: CMP  byte [RAX + 0x19], DIL  ; DIL = 0 : _Isnil ?
0x18018ca85: JNZ  0x18018caa8
0x18018ca87: CMP  dword [RAX + 0x20], ECX
0x18018ca8a: JNC  0x18018ca92
0x18018ca8c: MOV  RAX, [RAX + 0x10]     ; a droite
0x18018ca90: JMP  0x18018ca98
0x18018ca92: MOV  RBX, RAX              ; candidat
0x18018ca95: MOV  RAX, [RAX]            ; a gauche
0x18018ca98: CMP  byte [RAX + 0x19], DIL
0x18018ca9c: JZ   0x18018ca87
0x18018ca9e: CMP  RBX, RBP
0x18018caa1: JZ   0x18018caa8
0x18018caa3: CMP  ECX, [RBX + 0x20]
0x18018caa6: JNC  0x18018caab
0x18018caa8: MOV  RBX, RBP              ; absent
0x18018caab: CMP  RBX, RBP
0x18018caae: LEA  RAX, [RBX + 0x28]     ; jeu = noeud + 0x28
0x18018cab2: CMOVZ RAX, RDI             ; RDI = 0 -> jeu = NULL
```

Convention d'appel du resolveur : il n'y en a pas, il est inline. **Les deux
seuls sites du binaire** ou un rang de planche est extrait d'un handle sont
`0x18018ca71`..`0x18018ca77` (dans `spr_put`) et `0x18018c3bd`..`0x18018c3c4`
(dans `spr_set_find_and_read_rect`). Verification : la recherche d'octets
`81 ?? ff 0f 00 00` et `25 ff 0f 00 00` sur toute l'image ne rend, hors CRT et
hors modules etrangers, que ces deux fonctions.

La fonction la plus proche d'un « resolveur appelable » est
**`0x18018c3b0`** : `RCX` = manager, `RDX` = tampon de sortie (4 flottants),
`R8D` = handle complet. Elle resout, obtient `jeu` ou `0`, puis appelle
`0x18018c300`. **Elle ne teste pas `+0xb8`** et passe `0` tel quel : un rang
absent y est un dereferencement de `0x10`. Son wrapper public est `0x180187a60`.

Le nombre de planches, lu a `0x180187ab0` :

```
0x180187ab0: MOV  RAX, [0x180719908]    ; g_spr_db
0x180187ab7: MOV  RCX, [RAX + 0x98]     ; fin du vecteur des planches
0x180187abe: SUB  RCX, [RAX + 0x90]     ; debut
...          division par 0x58
0x180187ad2: MOV  RCX, [0x180719900]
0x180187ae7: JMP  0x18018c7d0           ; (manager, N)
```

`N = (g_spr_db->sets_end - g_spr_db->sets_begin) / 0x58`, c'est-a-dire le nombre
d'entrees de planche de `spr_db.bin`. **Aucun plafond a 0xfff n'est applique** :
si `N > 4096`, les rangs au-dela ne sont plus atteignables par le champ de
12 bits (DEDUIT par absence de borne lue).

## 2. Le consommateur et l'expression exacte

Le consommateur est **`0x18018ca20`** (`spr_put`). Wrappers publics :
`0x180187af0` (ecrit 5 dans `[RCX]` puis saute), `0x180187b10`, `0x180187c00`.
Chacun charge `RCX = *(void**)0x180719900` et saute a `0x18018ca20`.

Le `SPRSET` (`jeu`, = noeud + 0x28) :

```
jeu + 0x00 : vftable  (SPRSET::vftable)
jeu + 0x0c : rang (dword)
jeu + 0x10 : qword  -> entete du blob SPR charge
jeu + 0x18 : qword  -> tableau de pointeurs d'objets texture
jeu + 0xb8 : octet  -> garde « planche chargee »
```

Le decodage du handle, lu a `0x18018cb66` (le handle est relu depuis le noeud
d'affichage, `R8 = noeud_de_liste + 0x10`) :

```
0x18018cb66: MOV   R10D, dword [R8 + 0x4]     ; h
0x18018cb6a: MOV   R11D, R10D
0x18018cb6d: AND   R11D, 0xf0000000
0x18018cb74: CMP   R11D, 0x10000000           ; quartet de tete == 1 ?
```

`index = h & 0xffff` (obtenu par `MOVZX R14D, R10W`, donc 16 bits, pas 12).

### Quartet de tete 1 : toute la texture

```
0x18018cb89: LEA   R9,  [RBX + 0x40]          ; RBX = noeud ; +0x40 = jeu + 0x18
0x18018cb91: MOV   RAX, [R9]                  ; tableau de textures
0x18018cb94: MOV   RDX, [RAX + RCX*0x8]       ; RCX = index
```

Dimensions par les `short` a `+0xc`/`+0xe` de l'objet texture (`0x18018cc09`,
`0x18018cc0d`), mode force a 9 (`0x18018ccef`). Conforme a la note REVO.

### Sinon : la table de rectangles — **ce n'est ni l'une ni l'autre des deux formes proposees**

L'offset stocke a `+0x10` est un **offset relatif a sa propre adresse**, pas un
pointeur. Lu a `0x18018cba1` :

```
0x18018cb9d: MOVZX R14D, R10W                 ; index = h & 0xffff
0x18018cba1: LEA   RAX, [RBX + 0x38]          ; RBX = noeud ; +0x38 = jeu + 0x10
0x18018cba5: MOV   RDX, RDI                   ; RDX = 0
0x18018cbac: MOV   RCX, [RAX]                 ; RCX = B = *(jeu + 0x10)
0x18018cbaf: ADD   RCX, R13                   ; R13 = 0x10 -> RCX = B + 0x10
0x18018cbb2: MOVSXD RAX, dword [RCX]          ; offset relatif, SIGNE
0x18018cbb5: TEST  EAX, EAX
0x18018cbb7: JZ    0x18018cbbd                ; 0 -> table = NULL
0x18018cbb9: LEA   RDX, [RCX + RAX*0x1]       ; RDX = table des rectangles
0x18018cbc9: LEA   RCX, [R14 + R14*0x4]       ; index * 5
0x18018cbcd: MOVSXD RDX, dword [RDX + RCX*0x8]  ; *(int32*)(table + index*0x28)
0x18018cbd5: MOV   RAX, [R9]                  ; R9 = jeu + 0x18
0x18018cbd8: MOV   RDX, [RAX + RDX*0x8]       ; objet texture
0x18018cbe2: MOV   [R8 + 0xa0], RDX           ; ecrit dans le noeud d'affichage
```

Expression a ecrire, sans ambiguite d'indirection :

```c
B        = *(int64_t  *)(jeu + 0x10);
off      = *(int32_t  *)(B + 0x10);              /* signe */
rects    = off ? (uint8_t*)(B + 0x10 + off) : NULL;
texindex = *(int32_t  *)(rects + index * 0x28);  /* dword a +0x00 */
texobj   = (*(void***)(jeu + 0x18))[texindex];
```

Le `0x10` sert **deux fois** : c'est a la fois la position du champ dans `B` et
la base contre laquelle l'offset est relatif. Ni `*(base+0x10) + 0x10 + i*0x28`
ni `*(*(base+0x10)+0x10) + i*0x28` ne sont corrects.

- **Pas de `0x28` : CONFIRME**, lu deux fois (`LEA RCX,[R14+R14*4]` suivi d'un
  acces d'echelle 8 a `0x18018cbcd`, `0x18018cc3a`, `0x18018cc48`, `0x18018cc56`,
  `0x18018cc5c`), et une troisieme fois en clair dans `0x18018c300`.
- **Index de texture = dword signe a `+0x00` : CONFIRME** (`0x18018cbcd`).

Reste de l'entree de 0x28 octets, lu a `0x18018cc3a`..`0x18018cc5c` (ce sont des
**flottants**, tronques en entier) :

```
+0x00 : int32  index de texture
+0x18 : float  u
+0x1c : float  v
+0x20 : float  largeur
+0x24 : float  hauteur
```

Les octets `+0x04`..`+0x17` ne sont lus par aucune des deux fonctions examinees.

Le mode vient d'une **seconde table, relative de la meme facon**, lu a
`0x18018cd07` :

```c
modes = *(int32_t*)(B + 0x1c) ? (B + 0x1c + *(int32_t*)(B + 0x1c)) : NULL;
mode  = *(int32_t*)(modes + index * 8 + 4);     /* pas 8, champ a +4 */
```

Ce mode n'est ecrit que si le mode deja present dans le noeud n'est pas `0x11`
(`CMP dword [R8+0x24], 0x11` a `0x18018ccd9`).

La meme expression, isolee et plus lisible, est dans **`0x18018c300`**
(`spr_rect_read`), qui recoit un `SPRSET` deja resolu :

```c
iVar1 = *(int *)(*(longlong *)(param_1 + 0x10) + 0x10);
lVar3 = 0;
if (iVar1 != 0) lVar3 = *(longlong *)(param_1 + 0x10) + 0x10 + iVar1;
fVar6 = (float)(int)*(float *)(lVar3 + 0x18 + uVar4 * 0x28);   /* u */
fVar5 = (float)(int)*(float *)(lVar3 + 0x1c + uVar4 * 0x28);   /* v */
iVar2 =       (int)*(float *)(lVar3 + 0x20 + uVar4 * 0x28);    /* w */
iVar1 =       (int)*(float *)(lVar3 + 0x24 + uVar4 * 0x28);    /* h */
```

## 3. Le moment : a chaque trame

La table de rectangles est lue **au depot (`spr_put`), pas au dessin** — et
`spr_put` est rejoue a chaque trame parce que les listes d'affichage sont
**detruites a chaque trame**.

Sites de lecture, tous dans `spr_put` :

| Adresse | Ce qui est lu |
|---|---|
| `0x18018cbb2` / `0x18018cbb9` | l'offset relatif, donc l'adresse de la table |
| `0x18018cbcd` | l'index de texture (le dword a `+0x00`) |
| `0x18018cc3a`..`0x18018cc5c` | u, v, largeur, hauteur |
| `0x18018cd15` / `0x18018cd25` | la table des modes |

Appele depuis : `0x180187af0`, `0x180187b10`, `0x180187c00` (wrappers publics),
chacun passant `RCX = *(void**)0x180719900`.

`spr_put` **recopie** tout dans un noeud d'affichage neuf (0xf8 octets, alloue
par `0x180187cf0`), charge utile a `noeud + 0x10` :

```
+0x04 : handle         +0xa0 : pointeur d'objet texture
+0x24 : mode           +0xc0 : drapeaux (bit0, bit1 : « deja calcule »)
+0xc4, +0xc8 : taille  +0xd0..+0xdc : u, v, largeur, hauteur
```

Et `spr_disp` (`0x18018bbd0`, appele par passe depuis l'automate de rendu
`0x18010c330`, cas 6, 0xb, 0xc, 0xd) parcourt les 32 listes de la passe a
`manager + 0x10 + passe*0x200`, appelle `0x18018b010` pour chaque noeud, puis
**remet la liste a vide et libere chaque noeud** (`FUN_1802fdd80(noeud, 0xf8)`).

Donc : **oui, si tu ecris ce dword pendant que l'ecran est affiche, le changement
prend effet a la trame suivante** — a la premiere trame ou le producteur rejoue
son `spr_put`. Que ce producteur rejoue bien chaque trame est DEDUIT du vidage :
une liste videe et liberee rend tout affichage persistant impossible sans un
nouveau depot.

`0x18018b010` ne redecode rien : la recherche d'octets dans tout son corps
(`0x18018b010`..`0x18018bbd0`) ne trouve **ni** `ff 0f 00 00` (masque 0xfff)
**ni** `00 00 00 10` (constante 0x10000000). Il ne voit que la charge utile du
noeud.

## 4. La garde `+0xb8` : CONFIRMEE

```
0x18018cabf: CMP   byte [RAX + 0xb8], DIL     ; RAX = jeu, DIL = 0
0x18018cac6: JZ    0x18018cd2e                ; abandon
```

`0x18018cd2e` saute par-dessus toute la creation de noeud et tout le dessin ; la
fonction rend `0` (via `R8`, nul). Le test precedent, `TEST RAX,RAX` /
`JZ 0x18018cd2e` a `0x18018cab6`/`0x18018cab9`, traite le cas « planche
absente ». **Absent et non charge menent au meme abandon, mais par deux tests
distincts.**

A noter : la branche « absente » du calcul de la table (`CMOVZ RAX, R13` avec
`R13 = 0x10`, a `0x18018cba8`) est morte, justement parce que ces deux tests
l'ont deja interceptee.

Et `0x18018c3b0` **n'a pas cette garde** (voir section 1).

## 5. Le rang 511

**Le moteur indexe par le rang nu, 0..N-1, sans biais ni decalage.** Lu dans
`0x18018c7d0` :

```c
uVar3 = 0;
if (param_2 != 0) {
  do {
    local_228 = SPRSET::vftable;      /* valeur neuve */
    ...
    local_128[0] = uVar3;             /* <- la CLE, c'est le compteur de boucle */
    lVar1 = FUN_180187ed0(param_1, local_128);   /* noeud 0x128 : cle a +0x20 */
    FUN_180188690(param_1, local_248, 0, lVar1 + 0x20, lVar1);  /* insertion */
    uVar3 = uVar3 + 1;
  } while (uVar3 < param_2);
}
```

Donc la map est **pre-peuplee** de `N` `SPRSET` vides de cle `0, 1, 2, ... N-1`,
`N` etant le nombre d'entrees de planche de `spr_db.bin` (section 1). Le champ
`id` present dans chaque entree de planche de `spr_db.bin` (le dword a `+0x00`
de l'entree de 0x10 octets, lu par `spr_db_parse` a `0x18018d340`) **n'est pas
utilise** pour la cle : seul le *nombre* d'entrees compte.

Conclusion : **le rang attendu par le moteur est l'ordinal de la planche dans le
tableau de planches de `spr_db.bin`, compte depuis 0.** Si `SPR_S_SELSTG` est
bien la 512e entree de ce tableau (indice 511) et si `spr_db.bin` contient au
moins 512 entrees, alors 511 est exactement la cle de la map, et le handle d'un
de ses sprites vaut `(0x1?? << 28) | (511 << 16) | index`.

Ce que je **ne peux pas trancher ici** : que « rang 511 » designe bien cet
ordinal-la, et non les bits 16..27 d'un handle lu ailleurs. Les deux coincident
seulement si les handles de `spr_db.bin` ont ete numerotes dans l'ordre du
fichier — ce que le moteur *suppose* en creant 0..N-1, mais ne verifie pas. Le
controle decisif se fait sur le fichier, pas sur le binaire : prendre l'entree de
sprite de `spr_s_selstg` dans `spr_db.bin`, lire son handle, et verifier que
`(handle >> 16) & 0xfff == 511`. C'est d'ailleurs le chemin que suit le jeu :
`0x180187a60` lit le handle a `+0x28` d'un enregistrement rendu par
`0x18018c610`, puis le passe tel quel au resolveur.

## CE QUI N'EST PAS MESURE

- **Rien n'a ete execute.** Aucun binaire lance, aucune memoire de processus lue.
- **`spr_db.bin` n'a pas ete ouvert.** Le rang 511 de `SPR_S_SELSTG` n'est donc
  pas verifie ; la section 5 dit ou regarder, elle ne conclut pas.
- **Qui appelle `spr_put`** n'est pas identifie. Les trois wrappers publics
  (`0x180187af0`, `0x180187b10`, `0x180187c00`) n'ont pas ete remontes jusqu'au
  lecteur AET. « Rejoue a chaque trame » est DEDUIT du vidage des listes dans
  `spr_disp`, pas observe sur un appelant.
- **`0x18018b010` n'a pas ete decompile** en entier. L'affirmation « il ne
  redecode rien » repose sur deux recherches d'octets negatives sur son corps et
  sur le fait qu'il ne recoit que la charge utile du noeud — pas sur une lecture
  instruction par instruction.
- **`0x18018c610`** (`spr_db_find`) n'a pas ete lu. Que l'enregistrement rendu
  porte le handle a `+0x28` est lu dans `0x180187a81`, mais la nature de cet
  enregistrement est DEDUITE.
- **`0x1803FFBD0`** et les fonctions d'apercu de decor (`0x180174BF0`,
  `0x180171F40`, `0x1801721D0`) n'ont pas ete relies a ce systeme. Elles passent
  par `0x180029xxx` (couche AET), pas par `0x180719900`. Le lien entre l'apercu
  de l'ecran de selection de decor et une planche de sprites reste a etablir.
- **Les octets `+0x04`..`+0x17`** de l'entree de 0x28 octets, et les champs du
  `SPRSET` autres que `+0x0c`, `+0x10`, `+0x18`, `+0xb8`, ne sont pas identifies.
- **Le quartet de tete autre que 0 et 1** n'est pas explore : le code ne teste
  que l'egalite a `0x10000000`, tout le reste tombe dans la branche « rectangle ».
- **Aucun ecran n'a ete regarde.** Tout ceci est statique.
