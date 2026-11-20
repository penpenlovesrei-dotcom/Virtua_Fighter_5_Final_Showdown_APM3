# Le chemin de rendu des tâches d'effet (APM3)

Lecture statique de `VF5RE/analysis/vf5fs_apm3_origine.dll` (image non patchée,
base `0x180000000`), REA / provider Ghidra. **Aucun binaire n'a été exécuté.**

Note : ce provider **refuse les mutations de base** sur Windows
(`set_addresses_names` → « Windows Ghidra P0 does not admit database mutation »).
Les noms neufs ci-dessous sont donc **proposés dans cette note**, pas posés dans
le projet Ghidra.

---

## 0. Le résultat en une ligne

La « passe 4 » est **un seul octet booléen global**, `*(char*)(g_pRenderPassMgr + 4)`,
sans compteur de références, **écrit par trois tâches d'effet sœurs**
(`TaskEffectFogRing`, `TaskEffectRipple`, `TaskEffectSnowRing`). Deux de ces
trois tâches le remettent à **0 depuis leur destructeur, sans aucune garde**
« avais-je démarré ? ». Quand il vaut 0, `RenderPass_ExecuteOne(4)` **retourne
immédiatement** : *aucun* rappel de dessin d'effet n'est appelé, bien que la
liste les contienne toujours. Et le désenregistrement se fait **par étiquette**,
étiquette qui vaut `0` pour les trois tâches : il retire **le premier** rappel
de la liste, pas forcément le sien.

Adresses exactes du verrou :

| fait | adresse |
|---|---|
| l'octet lui-même | `g_pRenderPassMgr + 4`, soit `*(longlong*)0x18070FC68 + 4` |
| la garde qui le lit et fait tomber la passe | `0x18010C33A` (début de `FUN_18010C330`) |
| mis à **0** à l'init du renderer | `FUN_18010BF50`, écriture `*(u32*)(base+1) = 0` (octets 1,2,3,**4**) |
| mis à **1** par `TaskEffectFogRing` | `0x180072538` (`MOV DL,1`) + `0x18007253A` (`MOV ECX,4`), appel `0x18007253F` |
| mis à **0** par `TaskEffectFogRing::dest()` | `0x1800720C1` (`XOR EDX,EDX`) + `0x1800720C3` (`LEA ECX,[RDX+4]`), appel `0x1800720C6` |
| mis à **0** par `TaskEffectRipple::dest()` | `0x18007A74A` + `0x18007A74C`, appel `0x18007A74F` |
| mis à **0** par `TaskEffectSnowRing` (term) | `0x18007D73A` + `0x18007D73C`, appel `0x18007D73F` |

---

## 1. Les fonctions du périmètre, ce qu'elles font

### `FUN_18010CA20(int passe, u8 valeur)` → **`RenderPass_SetEnabled`**

Lu dans le binaire, corps entier :

```c
*(undefined1 *)(param_1 + DAT_18070fc68) = param_2;
```

C'est **un tableau d'octets de drapeaux indexé par numéro de passe**, à l'offset 0
de l'objet gestionnaire. Rien d'autre. Pas de compteur, pas de masque, pas de
borne : `RenderPass_SetEnabled(4,1)` écrit `1` dans l'octet `base+4`,
`RenderPass_SetEnabled(4,0)` y écrit `0`. **La dernière écriture gagne.**

Son getter est `FUN_18010BED0(int passe)` → **`RenderPass_IsEnabled`** :
`return *(u8*)(passe + DAT_18070FC68);` — un seul lecteur statique,
`FUN_18018B010`.

`DAT_18070FC68` = **`g_pRenderPassMgr`**, pointeur global (stocké comme
`longlong`) vers l'objet gestionnaire de rendu. Les 49 références à ce global
tiennent **toutes** entre `0x18010B076` et `0x18010CA60` : un seul module.

Les 18 sites d'appel de `RenderPass_SetEnabled`, désassemblés un par un
(index / valeur lus dans `ECX`/`DL`) :

| passe | allumée par | éteinte par |
|---|---|---|
| 0 | `FUN_1800E81E0` (`0x1800E826A`) | `FUN_1800E8690` (`0x1800E86B1`) |
| 2 | `FUN_18018F680` (`0x18018FA70`) | `FUN_18018F230` (`0x18018F35C`) |
| 3 | `FUN_18018F680` (`0x18018FAB3`) | `FUN_18018F230` (`0x18018F34B`) |
| **4** | **FogRing `0x18007253F`, Ripple `0x18007AED7`, SnowRing `0x18007D8DF`** | **FogRing `0x1800720C6`, Ripple `0x18007A74F`, SnowRing `0x18007D73F`** |
| 7 | `FUN_1800E81E0` (`0x1800E8261`) | `FUN_1800E8690` (`0x1800E86BB`) |
| 13 | `FUN_1801A8300` (`0x1801A834B`), `FUN_1801B0C90` (`0x1801B0CD7`) | `FUN_1801AAEF0` (`0x1801AAF2E`), `FUN_1801B1189` (`0x1801B1193`) |

**La passe 4 est la seule que trois émetteurs indépendants se partagent.**

### `FUN_18010BDC0(int etiquette, void(*f)(void*), void* ctx)` → **`RenderPass4_RegisterDrawCallback`**

Lu : un `push_back` de `std::list`. La tête de liste est à `g_pRenderPassMgr + 0x400`,
le compte à `+0x408`. Le nœud fait **0x28 octets** :
`{next(+0), prev(+8), etiquette(+0x10, int), f(+0x18), ctx(+0x20)}`.

- **Il n'y a qu'UNE liste**, celle de `+0x400`. Le premier paramètre (le `0` des
  tâches d'effet) **n'est pas un sélecteur de liste** : il est simplement rangé
  dans le nœud comme **étiquette**.
- **Pas de tri** : insertion en queue (`head->prev`).
- **Pas de plafond utile** : le seul garde-fou est
  `if (lVar3 != 0x666666666666665) ... else FUN_1802FBD0C("list<T> too long")` —
  la limite théorique de `std::list` de MSVC, pas une borne de jeu.
- **Trois sites d'enregistrement seulement** : `0x180072130` (FogRing, rappel
  `FUN_1800729C0`), `0x18007AE10` (Ripple, rappel `LAB_18007B470`),
  `0x18007D820` (SnowRing, rappel `LAB_18007DF90`). **Les trois passent `0`.**

### `FUN_18010BE60(int etiquette)` → **`RenderPass4_UnregisterDrawCallbackByTag`**

Lu : parcourt la liste, s'arrête au **premier** nœud dont `(int)nœud[+0x10] == etiquette`,
le délie, décrémente `+0x408`, libère 0x28 octets.

> **C'est une seconde faute, du même tonneau.** L'étiquette est l'identité, et
> les trois tâches utilisent l'identité `0`. Si deux rappels sont enregistrés,
> `Unregister(0)` retire **celui de l'autre**. Les trois sites de
> désenregistrement (`0x180072080`, `0x18007A700`, `0x18007D6F0`) passent `0`.

### `FUN_18010C330(int passe)` → **`RenderPass_ExecuteOne`**

C'est **l'exécuteur de passe**, et c'est lui qui tranche. Première instruction
utile, à `0x18010C33A` :

```c
if (*(char *)(DAT_18070fc68 + passe) == '\0') {
  *(u64*)(base + 0x38  + passe*8) = 0;   /* chrono CPU  de la passe */
  *(u64*)(base + 0xb8  + passe*8) = 0;   /* chrono GPU  de la passe */
  goto fin;                              /* RIEN n'est fait */
}
```

Puis `*(int*)(base + 0x418) = passe` (index de passe courant, lisible par
`FUN_18010BEB0`), et un `switch(passe)`. **Le cas 4 est exactement le parcours
de la liste** (lu à `0x18010C3DA`…`0x18010C40B`) :

```c
case 4:
  node = ((list*)(base+0x400))->head->next;
  if (node != head) do {
    if ((code*)node[3] != 0) (*(code*)node[3])(node[4]);   /* f(ctx) */
    node = (longlong*)*node;
  } while (node != head);
  FUN_180007440();
  break;
```

Donc, lu dans le binaire :

- **aucun filtre par étiquette** : l'étiquette rangée dans le nœud (`node[2]`)
  **n'est jamais relue** par le parcours ;
- **aucun plafond d'itérations**, aucun tri, aucune condition de scène ;
- **aucun `BindAsOutput`/`End` englobant** : contrairement aux cas 5, 6, 7, 8
  (qui ouvrent/ferment avec `FUN_180102340` / `thunk_FUN_180248BA0`), le cas 4
  n'ouvre rien — **chaque rappel doit poser sa propre cible de rendu** ;
- le seul test, c'est `f != NULL`.

Les autres cas, pour situer la passe 4 dans la trame : 0 = `FUN_18010BB40`,
2 = `FUN_18010B570`, 3 = `FUN_18010B940`, **4 = les effets**, 5 = scène +
`base+0x158`, 6/7 = opaque/transparent, 8 = ombres (lit `base+0x14B`, `0x14C`,
`0x14D` et `base+0x3F4`), 9 = `FUN_180103510` (le décor), 10 = effacement
(`base+0x380`), 11/12/13 = `FUN_180187A10(0|3|2)`, 15 = fin de trame.

### `FUN_18010C230(void)` → **`RenderPass_ExecuteAll_0_to_15`**

Seul appelant de `RenderPass_ExecuteOne`. Boucle `for (p = 0; p <= 0xF; p++)` —
**16 passes, et 4 est dedans**. Un bloc de saut dépend du global
`DAT_180C3B6F0` (flags `+0x625`, `+0x626`) ; j'ai déroulé les quatre branches :

| état | passes sautées |
|---|---|
| `DAT_180C3B6F0 == 0` | aucune — tout est exécuté |
| `[0x626] != 0` et `[0x625] == 0` | 0, 2, 3, 5, 6, 7, 8, 9 |
| `[0x626] == 0`, `FUN_1800E8800() != 0` | 11, 13, 14 |
| `[0x626] == 0`, sinon | 10..15 ou 11..14 selon `FUN_180203540` / `FUN_1800BA0A0` / état `0x25` |

**Dans aucune branche la passe 4 n'est sautée.** Elle est donc toujours
dispatchée vers `RenderPass_ExecuteOne(4)`, chaque trame.

### `FUN_18010BF50(…)` → **`RenderPassMgr_Init_TargetsAndPassFlags`**

Init du gestionnaire (appelant unique : `FUN_1800D92A0`). Il écrit d'abord
`0x01010101` dans les quatre dwords `base+0`…`base+0xF` (**16 passes, toutes à
1**), puis **rétablit six d'entre elles à 0** :

```c
*(u32*)((char*)base + 1) = 0;   /* octets 1, 2, 3, 4  ← LA PASSE 4 */
*(u8 *)((char*)base + 6) = 0;   /* octet 6 */
*(u8 *)(base + 2)        = 0;   /* octet 8 */
```

État des drapeaux juste après l'init, lu octet par octet :

```
passe   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
valeur  1  0  0  0 [0] 1  0  1  0  1  1  1  1  1  1  1
```

**La passe 4 part éteinte.** Rien ne l'allume jamais, sauf l'init d'une tâche
d'effet. Et à l'intérieur de ce même init, la boucle sur les 11 descripteurs de
cible (`&DAT_1803A4FD0`, 11 × 24 octets, pas de 0x38 dans l'objet depuis
`base+0x188`) crée **toutes** les cibles : j'ai lu la table, les 11 entrées ont
bien `0x11E` comme premier dword, donc le `if (puVar5[-5] == 0x11e)` passe pour
les onze. **Il n'y a pas de borne là.**

### `FUN_18010BEF0(int slot)` → **`RenderTarget_GetCurrentBySlot`**

```c
return ((longlong)*(int *)(&DAT_1803A50E0 +
          ((longlong)*(int *)(base + 0x15c + slot*4) + slot*3) * 4) + 7)
       * 0x38 + base;
```

Lecture : `base + 0x15C + slot*4` est un **curseur d'anneau** par slot ;
`DAT_1803A50E0` est une table de **3 entrées par slot** (10 slots) qui mappe
le curseur sur un **index de cible** ; le descripteur rendu est
`base + 0x188 + index*0x38` (car `(index+7)*0x38 = 0x188 + index*0x38`).

Table `DAT_1803A50E0` lue : slot 0 → {2,0,0}, slot 1 → {1,1,1}, slot 2 → {3,3,3},
slot 3 → {4,4,4}, slot 4 → {5,5,5}, **slot 5 → {6,6,6}**, slot 6 → {7,7,7},
slot 7 → {8,8,8}, slot 8 → {9,9,9}, slot 9 → {10,10,10}.

Donc **`RenderTarget_GetCurrentBySlot(5)` rend toujours la cible n° 6**, quelle
que soit la valeur du curseur. D'après la table de descripteurs, la cible 6 est
`{0x11E, 512, 512, 0, 0x1D6, 0}` — **512×512, et créée**. Pas de borne ici
non plus. (Pour mémoire : la cible 9 est `{0x11E, 1280, 720, …}`, l'écran.)

Variante à deux paramètres : `FUN_18010BF20(slot, anneau)` →
**`RenderTarget_GetBySlotAndRing`**, même table sans passer par le curseur.

### `FUN_18010CCA0(descripteur, int index)` → **`RenderTarget_BindAsOutput`**

```c
if (index < 0 || index > *(int*)(p+0x1c)) return 0xffffffff;
FUN_18024AC90(0xa35, *(u32*)(*(longlong*)(p+0x28) + index*4));  /* pose la cible */
if (FUN_18024ACC0(0xa35) != 0xa1a) return 0xffffffff;            /* état refusé */
FUN_180007440();
... largeur = FUN_180195840(surf, index), hauteur = FUN_180195590(surf, index)
FUN_180252990(0x447, 0x15, w, h, 1/w, 1/h);    /* constantes de résolution */
FUN_180252990(0x48b, 0x18, w, h, 1/w, 1/h);
return 0;
```

Ce que le rappel en obtient : **la cible de rendu posée** (registre d'état
`0xA35`) **et les constantes `w, h, 1/w, 1/h`** publiées dans deux emplacements
de paramètres de shader (`0x447/0x15` et `0x48B/0x18`). Ce n'est pas un matériau
ni un lot de dessin : c'est « ouvre cette cible et dis au shader sa taille ».

**Elle peut échouer** et rendre `-1` (index hors bornes, ou état `0xA35`
différent de `0xA1A`). Dans le rappel du FogRing **ce retour est ignoré** : le
dessin continue quand même.

---

## 2. Le chemin complet, de l'enregistrement à l'écran

Pour `TaskEffectFogRing` (vtable `0x18034F6A0`, confirmée par `rtti_apm3.txt`) :

1. **`FUN_180072130`** → `TaskEffectFogRing_InitForStage(obj, decor)`.
   `*obj = 1`, puis **tout le reste est sous la garde
   `if (decor == DAT_1806431C8)`**, et `DAT_1806431C8 = 0x16` (**décor 22**).
   Dans la garde : `*obj = DAT_1806431CC` — lu : **1** — 2000 particules
   (`DAT_1806431D0 = 0x7D0`), allocations, puis
   `RenderPass_SetEnabled(4,1)` et
   `RenderPass4_RegisterDrawCallback(0, FUN_1800729C0, obj)`.
2. **chaque trame** : `RenderPass_ExecuteAll_0_to_15` → `RenderPass_ExecuteOne(4)`
   → garde `base+4` → parcours de la liste → `FUN_1800729C0(obj)`.
3. **`FUN_1800729C0`** → `TaskEffectFogRing_Draw(obj)`. Deuxième garde, lue :
   `if (*obj == 0) return;` — l'octet de la tâche, chargé depuis les données
   (= 1 pour le décor 22). Puis :
   - `p = RenderTarget_GetCurrentBySlot(5)` → cible 6 (512×512) ;
   - `RenderTarget_BindAsOutput(p, 0)` *(retour ignoré)* ;
   - viewport = taille de la cible, effacement à la couleur `obj+0x40` ;
   - **`if (FUN_1800EC090(0x16) != 0) FUN_1800EA4C0(0x16, 0, 0);`** —
     l'**objset 22** est dessiné dans la cible ;
   - `FUN_18010D190(p)` ferme la cible ;
   - `dst = RenderTarget_GetCurrentBySlot(2)` → cible 3 ;
     `FUN_1800D1F30(dst, 0, p, 0, {0.8,0.8,0.8,1.0})` — composition ;
   - **`FUN_18010CA10(*(u64*)(dst+8))`** → publie la texture dans
     `g_pRenderPassMgr + 0x410`.
4. **passe 9** : `RenderPass_ExecuteOne(9)` → `FUN_180103510`, qui appelle
   `FUN_18010BEC0()` (= lit `base+0x410`) et, si non nul, **lie cette texture
   au slot `0x22B`** autour du dessin des objsets `0x14` (20) puis `0x13` (19).

> **La brume n'arrive donc pas à l'écran par la passe 4.** La passe 4 ne fait
> que remplir une cible hors écran et publier son handle. Ce qui la rend
> visible, c'est la passe **9**, et seulement **à travers les objsets 19 et 20**,
> dont le dessin est lui-même gardé par `FUN_1800EC090(0x14) > 0` et
> `FUN_1800EC090(0x13) > 0`. Trois objsets doivent être chargés pour voir quoi
> que ce soit : **22** (la brume elle-même), **19 et 20** (les surfaces qui
> l'échantillonnent).

Pour `TaskEffectRipple` (vtable `0x18034EF10`) : init `FUN_18007B030`, chargeur
de données **`FUN_18007AE10`** gardé par `decor == DAT_1806432E0` (**4**) ou
`decor == DAT_18064330C` (**15**), rappel `LAB_18007B470`, et les mêmes deux
appels `RenderPass_SetEnabled(4,1)` + `Register(0, …)`.

Pour `TaskEffectSnowRing` (vtable `0x18034F490`) : init `FUN_18007DA60` qui
appelle **`FUN_18007D820`**, gardé par `decor == DAT_180643450` (**16**),
rappel `LAB_18007DF90`, mêmes deux appels. Son extinction `FUN_18007D6F0` est
la seule des trois à être **gardée** (`if (*obj != 0) { … *obj = 0; }`).

---

## 3. La réponse à la question qui tranche

> *Un rappel enregistré par `FUN_18010BDC0(0, f, ctx)` depuis l'init d'une tâche
> d'effet est-il réellement appelé à chaque image pendant un combat ?*

**Non — pas inconditionnellement. Il l'est si et seulement si l'octet
`*(char*)(g_pRenderPassMgr + 4)` vaut autre chose que 0 à cette image.**

C'est la seule condition, et elle est entière :

- la boucle de trame **dispatche toujours** la passe 4 (établi §1, les quatre
  branches de `FUN_18010C230`) ;
- le parcours, une fois la garde franchie, appelle **tous** les rappels, sans
  plafond, sans tri, sans filtre par étiquette, sans drapeau de scène ;
- l'octet est **mis à 0 par l'init du renderer** et n'est relevé que par une
  init de tâche d'effet ;
- il est **remis à 0 par le destructeur de n'importe laquelle des trois
  tâches**, sans compteur et — pour FogRing et Ripple — **sans garde**.

Donc : une init de tâche d'effet suivie d'une extinction d'une tâche sœur laisse
la passe 4 éteinte, et **tous** les rappels encore enregistrés deviennent muets
d'un coup. C'est bien un **défaut partagé** par les deux chantiers (la brume
d'Aoi et l'eau d'Eileen) : même octet, même absence de compteur, même étiquette
`0`.

---

## 4. Comment le vérifier sans lancer le jeu

Trois contrôles purement statiques, chacun capable d'échouer sur une faute
réelle :

1. **Le drapeau part-il à 0 ?** Lire les 4 octets à l'offset de fichier
   correspondant à `0x18010BF50` + l'instruction `MOV dword [reg+1], 0`. Un
   contrôle qui réussit sur l'image intacte doit **échouer** si on remplace ce
   `0` par `1`.
2. **Combien d'émetteurs pour la passe 4 ?** Désassembler les 18 sites d'appel
   de `0x18010CA20` et compter ceux dont `ECX == 4`. L'image d'origine en donne
   **six** : trois à `DL=1`, trois à `DL=0`. Un contrôle juste doit lire
   `ECX`/`DL` **au site d'appel**, pas compter une chaîne.
3. **L'étiquette est-elle unique ?** Les trois `FUN_18010BDC0(…)` et les trois
   `FUN_18010BE60(…)` ont tous `ECX = 0` (`XOR ECX,ECX`). Un contrôle qui
   compare le **nombre d'étiquettes distinctes** (1) au **nombre de rappels**
   (3) échoue sur l'image d'origine : c'est l'écart qui est la faute, pas un
   compte absolu.

Rien de tout cela ne demande une course.

---

## 5. CE QUI N'EST PAS MESURÉ

Je nomme ce que je n'ai **pas** pu établir.

- **L'ordre réel init/dest à l'exécution.** Les destructeurs sont les slots 3
  des vtables (`0x180072080`, `0x18007A700`) et ne sont appelés
  qu'**indirectement** : `procedure_callers` rend une liste **vide** pour
  `0x18007A700`. Je n'ai donc **pas** pu prouver statiquement que, lors d'un
  changement de décor ou d'un redémarrage de manche, l'extinction d'une tâche
  tombe **après** l'init de l'autre. Que la faute soit *possible* est lu ;
  qu'elle se produise sur l'écran de Frédéric n'est **pas mesuré**.
- **Si deux de ces trois tâches coexistent sur un même décor.** Les gardes de
  données lues disent décor 22 pour FogRing, 4 et 15 pour Ripple, 16 pour
  SnowRing — donc *dans ces données-là*, pas de coexistence. Je n'ai **pas**
  vérifié quelles tâches la table d'effets du décor (`0x18034D530`/`0x18034D570`,
  §17 de `decors.md`) fait réellement **créer** par décor, ni ce que les décors
  ajoutés par le chantier demandent. **C'est la mesure qui reste à faire, et
  elle est statique.**
- **Qui remet la passe 4 à 1 après une extinction.** Personne, d'après les 18
  sites d'appel — mais je n'ai cherché que les écritures passant par
  `FUN_18010CA20`. Une écriture directe dans `base+4` par un autre module
  n'apparaîtrait pas dans les 49 xrefs de `DAT_18070FC68`, qui ne couvrent que
  les accès **par ce global**. **Non exclu.**
- **Le contenu de `DAT_180C3B6F0`** (flags `+0x625`, `+0x626`) : je n'ai pas
  établi à quoi correspond cet objet ni son état pendant un combat. Ça n'affecte
  pas la conclusion (la passe 4 est dispatchée dans **toutes** les branches),
  mais la lecture des autres passes en dépend.
- **`FUN_18010D190`** (la fermeture de cible, appelée par le rappel et par les
  cas 10/15) : **non décompilée**. Je ne sais pas si elle peut échouer.
- **`FUN_18024AC90` / `FUN_18024ACC0` / `0xA35` / `0xA1A`** : je lis que c'est
  un registre d'état graphique et une valeur attendue, je ne les ai **pas**
  identifiés. Donc je ne sais **pas** dans quelles conditions
  `RenderTarget_BindAsOutput` rend `-1`. Comme le rappel ignore ce retour, ça
  pourrait produire un dessin dirigé vers la mauvaise cible — **hypothèse non
  vérifiée**.
- **Les objsets 19, 20, 22.** J'ai lu que la brume n'est visible qu'à travers
  eux (§2), mais je n'ai **pas** vérifié qu'ils sont chargés par le décor visé,
  ni que leurs matériaux échantillonnent bien le slot `0x22B`.
- **Les rappels de Ripple et SnowRing** (`LAB_18007B470`, `LAB_18007DF90`) :
  Ghidra n'y a pas créé de fonction, je ne les ai **pas** décompilés. Je n'ai
  donc **pas** vérifié qu'ils ont, comme FogRing, une seconde garde sur l'octet
  `*obj`, ni vers quelle cible ils écrivent.
- **Les noms neufs ne sont pas posés** dans la base Ghidra : le provider refuse
  toute mutation sur cette plateforme. Ils n'existent que dans cette note.
