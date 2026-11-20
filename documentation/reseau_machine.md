# La machine à états `am::abaas::LinkMainState*` — bornes liées (APM3)

Relevé statique sur `runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll.origine`
(PE MSVC x64, base `0x180000000`). **Lecture seule.** Rédigé au fil de l'eau :
chaque section est datée de son état de vérification.

Le transport (STUN/TURN) et l'appariement HTTP ALL.Net sont traités ailleurs.
Ici : **la machine d'états elle-même — qui la fait tourner, dans quel ordre, et
où elle s'arrête.**

---

## 1. La disposition des vtables d'état — ÉTABLI

Relevé par `py -3 tools/vtable.py 0x1805C6CF0 0x1805C7060` (l'outil détecte les
frontières par le CompleteObjectLocator qui précède chaque table : c'est ce qui
évite de lire la fin de la table voisine).

Les quinze tables ont **exactement six créneaux**, tous du même moule.

### Le créneau [1] est l'IDENTIFIANT NUMÉRIQUE de l'état

Une grappe de petites fonctions consécutives, chacune `mov eax, N ; ret` :

    0x1802C8A50  b8 0b 00 00 00   mov eax, 0xb    ; ret
    0x1802C8A60  b8 05 00 00 00   mov eax, 5      ; ret
    0x1802C8A70  b8 07 00 00 00   mov eax, 7      ; ret
    0x1802C8A80  b8 09 00 00 00   mov eax, 9      ; ret
    0x1802C8A90  b8 06 ...        mov eax, 6      ; ret
    0x1802C8AA0                   mov eax, 0xa    ; ret
    0x1802C8AB0                   mov eax, 8      ; ret
    0x1802C8AC0                   mov eax, 3      ; ret
    0x1802C8AD0                   mov eax, 1      ; ret
    0x1802C8AE0                   mov eax, 2      ; ret
    0x1802C8AF0                   mov eax, 0x10   ; ret

Ce n'est ni un nom ni une durée : c'est `virtual int getId() const`.

| id | état | vtable | créneau [1] |
|---:|---|---|---|
| 0 | `LinkMainStateStartup` | `0x1805C6D70` | `0x1802983E0` (`xor eax,eax; ret`) |
| 1 | `LinkMainStateSetup` | `0x1805C6DA8` | `0x1802C8AD0` |
| 2 | `LinkMainStateStandby` | `0x1805C6DE0` | `0x1802C8AE0` |
| 3 | `LinkMainStatePlaying` | `0x1805C6FA0` | `0x1802C8AC0` |
| 4 | `LinkMainStatePlayEnd` | `0x1805C6FD8` | `0x1802985F0` |
| 5 | `MatchingAllocate` | `0x1805C6E18` | `0x1802C8A60` |
| 6 | `MatchingMatch` | `0x1805C6E50` | `0x1802C8A90` |
| 7 | `MatchingChannelBind` | `0x1805C6E88` | `0x1802C8A70` |
| 8 | `MatchingWaitReady` | `0x1805C6EC0` | `0x1802C8AB0` |
| 9 | `MatchingConnectivityCheck` | `0x1805C6EF8` | `0x1802C8A80` |
| 10 | `MatchingQualityCheck` | `0x1805C6F30` | `0x1802C8AA0` |
| 11 | `CleanupMatch` | `0x1805C6F68` | `0x1802C8A50` |
| **16** | `LinkMainStateUnavailable` | `0x1805C7010` | `0x1802C8AF0` |

Deux remarques qui comptent :

* **L'ordre des identifiants est l'ordre du scénario**, pas l'ordre des
  adresses : 0 Startup → 1 Setup → 2 Standby → (5…10 l'appariement) → 3 Playing
  → 4 PlayEnd → 11 CleanupMatch.
* **`Unavailable` vaut 16, pas 12.** Le trou 12–15 est le premier indice que
  l'énumération d'origine comptait des états que ce build ne construit pas, ou
  qu'`Unavailable` est délibérément mis hors de la plage « normale ».

### Piège d'ICF, à ne pas relire de travers

`LinkMainStateStartup` a en créneau **[2]** l'adresse `0x1802C8AD0`, c'est-à-dire
le corps `mov eax,1 ; ret` qui sert par ailleurs de `getId` à `Setup`. Ce n'est
pas un `getId` mal placé : l'éditeur de liens a **fusionné deux fonctions
identiques** (`/OPT:ICF`). `Startup::tic()` s'écrit `return 1;` — même corps,
même adresse. La même prudence vaut pour `0x180295ED0` (`ret 0`) et
`0x1802983E0` (`xor eax,eax; ret`), partagés par tout le binaire.

### Le rôle de chaque créneau

Table de base `am::abaas::LinkMainStateBase` (`0x1805C6CF8`) :

    [0] 0x1802C5F30   destructeur (scalar deleting destructor)
    [1] 0x1802FF5B0   PURE VIRTUAL (purecall)
    [2] 0x1802FF5B0   PURE VIRTUAL
    [3] 0x1802FF5B0   PURE VIRTUAL
    [4] 0x1802FF5B0   PURE VIRTUAL
    [5] 0x1802C9CA0   mov dword ptr [rcx+0x10], edx ; ret

Quatre virtuelles pures : la classe de base est abstraite, et impose à chaque
état de fournir `getId`, `tic`, un accusé et une remise à zéro.

| créneau | rôle | preuve |
|---|---|---|
| [0] | destructeur | position 0 MSVC ; corps commun `0x1802C6230` pour Startup/Standby/PlayEnd |
| [1] | `getId()` | `mov eax, N ; ret`, N = identifiant du tableau ci-dessus |
| [2] | **`tic()` — la trame** | le gros corps propre à chaque état (jusqu'à 3009 o pour QualityCheck) |
| [3] | `notify(bool)` / accusé | corps partagé `0x1802C95E0` : `cmp edx,1 ; jne … ; mov byte [rcx+0x18], dl` |
| [4] | `reset()` / sortie d'état | remet à zéro les champs propres (`[rcx+0x18]`, `[rcx+0x20]`, `[rcx+0x24]`…) |
| [5] | `setResult(int)` hérité | `mov [rcx+0x10], edx` — le SEUL non redéfini : tous les états le partagent |

Le créneau [5] est le canal de sortie commun : **chaque état écrit son code de
résultat en `this+0x10`**, et c'est le même code hérité de la base pour les
quinze. C'est là qu'il faudra regarder pour lire un échec.

Tailles des `tic()`, qui disent où est le travail réel :

    Startup                    return 1        (ICF avec 0x1802C8AD0)
    Setup                      0x1802D8F80     282 o
    Standby                    0x1802D9920      30 o   <-- minuscule
    MatchingAllocate           0x1802D9E20    1531 o
    MatchingMatch              0x1802DAAF0    2417 o
    MatchingChannelBind        0x1802DDB40     730 o
    MatchingWaitReady          0x1802DDE30     786 o
    MatchingConnectivityCheck  0x1802DEB40    1601 o
    MatchingQualityCheck       0x1802E1350    3009 o
    CleanupMatch               0x1802E2080      74 o
    Playing                    0x1802E2280    2665 o
    PlayEnd                    0x1802E2D00      71 o
    Unavailable                0x1802E2FA0      26 o   <-- minuscule

`Standby` à 30 octets et `Unavailable` à 26 : deux états qui ne font
pratiquement rien. Le premier est le point d'attente, le second le cul-de-sac.

---

## 2. Le pilote : qui fait tourner la machine — ÉTABLI

### 2.1 La chaîne, du point d'entrée du module au `tic()`

Toute la chaîne est établie par balayage linéaire (`refs_lineaires.py`), pas par
`.pdata` : chaque maillon ci-dessous n'a **qu'une seule** référence dans tout le
`.text`, ce qui rend le chemin unique.

    module_start                        0x180214C50   EXPORT du module
      └ pose 0x180214790 dans [hôte+0x30]  (rappel « trame »)
      └ pose 0x1802146F0 dans [hôte+0x40]  (rappel « fin »)
      └ alloue 0x108 o + ctor  0x180218A10  ->  AbaasManager  (global 0x180C3BDD8)

    [hôte+0x30] = 0x180214790            garde : rcx == 0x20270, sinon renvoie -1
      └ AbaasManager::update             0x180218F90     (si le global != 0)
          └ setupLink                    0x180219BF0     (si Link absent, cf. §2.3)
              └ new Link (16 o)          0x1802C3BE0
                  └ new ImplLink (0x1E90 o) + ctor  0x1802C2B40
              └ Link::setup              0x1802CAC30
                  └ ImplLink::setup      0x1802C9D20
                      └ CreateEventA -> [Impl+0x30]  (événement d'ARRÊT)
                      └ _beginthreadex(0x1802C9690, Impl)   via 0x1802E3950
                      └ [Impl+0x1DE0] = 1              (drapeau « démarré »)

    FIL DÉDIÉ, corps = 0x1802C9690  (ImplLink::threadMain)
      └ 0x1802C8CC0   LA BOUCLE   (une seule entrée .pdata, 0x1802C8CC0-0x1802C95DF)
      └ SetEvent([Impl+0x38]) puis fin du fil

**La machine ne tourne pas sur la trame du jeu.** Elle tourne dans un fil à
elle, créé par `_beginthreadex` (`0x180319CDC`, appelé depuis `0x1802E3950`,
message d'erreur `"Error : start() %d."` à `0x1802CAB00`). Le rappel de trame du
module ne fait que la *créer* ; il ne la cadence pas.

### 2.2 La boucle du fil — `0x1802C8CC0`

Elle est bornée par un seul enregistrement `.pdata` (0x1802C8CC0-0x1802C95DF,
2335 o) et boucle sur elle-même : le saut arrière est en

    0x1802C9530  cmp byte ptr [rsp + 0x30], 0
    0x1802C9535  je  0x1802C8D23            <-- retour en tête de boucle

`[rsp+0x30]` est posé en tête de boucle par

    0x1802C8D23  xor edx, edx                  ; délai 0
    0x1802C8D25  mov rcx, [r15 + 0x30]         ; l'événement d'arrêt
    0x1802C8D29  call WaitForSingleObject
    0x1802C8D2F  test eax, eax
    0x1802C8D31  sete byte ptr [rsp + 0x30]    ; 1 = signalé = on sort
    0x1802C8D38  je   0x1802C9519              ; sortie de boucle

et la queue de boucle appelle `Sleep(1)` (`0x180346078`, `ecx = 1`) juste avant
le saut arrière. **Cadence : ~1 kHz, indépendante des 60 Hz du jeu.**

### 2.3 Le cœur : l'appel de `tic()` (créneau [2])

    0x1802C9293  lea  rcx, [r15 + 0x6C0]   ; sous-objet ; call [vt+0x18]
    0x1802C929A  mov  rax, [rcx]
    0x1802C929D  call qword ptr [rax + 0x18]
    0x1802C92A0  mov  rcx, [r15 + 0x1C88]  ; <-- L'ÉTAT COURANT
    0x1802C92A7  mov  rax, [rcx]           ;     sa vtable
    0x1802C92AA  lea  rdx, [r15 + 0x80]    ;     le contexte partagé
    0x1802C92B1  call qword ptr [rax + 0x10]   ; <-- tic(contexte)
    0x1802C92B4  mov  [rbp - 0x48], eax        ; <-- LA VALEUR RENDUE

Puis sept octets d'état public sont recopiés sous verrou (`Impl+0x190`) :

    Impl+0x1B8..0x1BE   (privé, écrit par les états)  -->  Impl+0x1C98..0x1C9E

C'est ce bloc que lisent les accesseurs `Link::isXxx()` de `0x1802C8B00`,
`0x1802C8B40`, `0x1802C8B80`, `0x1802C8C00`, `0x1802C8C40`, `0x1802C8C80` —
tous bâtis sur le même moule (verrou `Impl+0x190`, un octet, déverrouillage), et
c'est `0x1802C8B00` (octet `+0x1C99`) qu'interroge `AbaasManager::update` en
`0x180219245`.

### 2.4 `tic()` rend l'IDENTIFIANT DE L'ÉTAT SUIVANT — ÉTABLI

C'est le point qui donne son sens à tout le reste :

    0x1802C9335  mov  rcx, [r15 + 0x1C88]
    0x1802C933C  mov  rax, [rcx]
    0x1802C933F  call qword ptr [rax + 8]   ; getId() de l'état COURANT
    0x1802C9342  cmp  dword ptr [rbp - 0x48], eax
    0x1802C9345  je   0x1802C94AE           ; même id -> AUCUNE transition

Autrement dit : `tic()` rend un `int`, la boucle le compare à `getId()` de
l'état courant, et **ne change d'état que s'ils diffèrent**. Un état qui veut
rester rend son propre identifiant.

Cela referme le piège d'ICF signalé au §1 : `Startup::tic()` partage le corps
`mov eax,1 ; ret` avec `Setup::getId()` parce que `Startup::tic()` s'écrit
littéralement `return 1;` — **Startup passe inconditionnellement à Setup, dès la
première trame du fil, sans aucune condition.**

### 2.5 La commutation d'état

Quand les identifiants diffèrent :

    0x1802C934B  mov  rcx, [r15 + 0x1C88]
    0x1802C9355  call qword ptr [rax + 0x20]   ; créneau [4] : sortie/remise à zéro
    0x1802C9358  lea  r13, [r15 + 0x40]        ; le CONTENEUR D'ÉTATS
    ... hachage FNV-1a (0xCBF29CE484222325 / 0x100000001B3) des 4 octets de l'id
    ... parcours du seau, comparaison sur [nœud+0x10]
    0x1802C948A  mov  rdx, [rax + 0x18]        ; le pointeur brut de l'état trouvé
    0x1802C948E  mov  [r15 + 0x1C88], rdx      ; il devient l'état courant

`Impl+0x40` est donc une **`std::unordered_map<int, shared_ptr<LinkMainStateBase>>`**
(disposition MSVC : `max_load_factor` = `0x3F800000` = 1.0f en `+0x40`, liste en
`+0x48`, taille en `+0x50`, tableau de seaux en `+0x58`) ; les nœuds font 0x28
octets — la constante `0x666666666666665` (= `max_size` pour 40 o) apparaît
telle quelle en `0x1802C2D35` et `0x1802C9435`. Clé en `nœud+0x10`, pointeur en
`+0x18`, bloc de comptage en `+0x20`.

**Attention (non établi, mais visible) :** si l'identifiant rendu n'existe pas
dans la carte, la branche `0x1802C93F7` **insère** une entrée neuve — dont le
`shared_ptr` est vide. `[Impl+0x1C88]` deviendrait nul et le `tic` suivant
déréférencerait zéro. Ce n'est donc pas un chemin prévu : les états ne peuvent
rendre que des identifiants présents dans la carte.

### 2.6 L'état initial est `Startup` (id 0)

À la fin de `ImplLink::setup`, juste avant la création du fil :

    0x1802CA1EC  xor  r12d, r12d               ; r12d = 0 et n'est pas réécrit
    0x1802CAA2B  mov  dword ptr [rsp + 0x38], r12d   ; clé = 0
    0x1802CAA30  lea  rcx, [rdi + 0x40]        ; la carte
    0x1802CAA39  call 0x1802C59E0              ; recherche
    0x1802CAA41  lea  rcx, [rdi + 0x1C88]
    0x1802CAA48  call 0x1802C5800              ; affectation du shared_ptr

**L'état courant part donc à `LinkMainStateStartup` (id 0)**, et le fil est créé
dans la foulée. Le premier `tic()` rend 1 → `Setup`.

### 2.7 Le chemin est-il atteint dans ce build ?

Ce qui est ÉTABLI :

* `module_start` (`0x180214C50`) est un **export** du module : le moteur hôte
  l'appelle. Il pose le rappel `0x180214790` et alloue l'`AbaasManager` **sans
  aucune garde** (0x180214CF4 : `mov ecx, 0x108 ; call 0x180218930`).
* Le rappel `0x180214790` **est gardé** : `cmp rcx, 0x20270 ; jne` → sortie
  immédiate avec `-1`. Le même nombre garde le second rappel `0x1802146F0`
  (0x1802146F9). Ce `0x20270` est fourni par l'hôte, pas par ce module.
* Dans `AbaasManager::update`, l'appel à `setupLink` est gardé par deux
  conditions seulement, et **retenté à chaque passage** :

        0x18021916D  cmp qword ptr [rbx + 0x10], 0   ; le Link existe déjà ?
        0x180219172  jne 0x180219180
        0x180219174  test eax, eax                   ; [rbx+0xAC], un compte à rebours
        0x180219176  jne 0x180219180
        0x18021917B  call setupLink

* `setupLink` lui-même abandonne tout de suite si l'une des deux gardes d'`apm.dll`
  échoue (`[0x180C3B6F8]` vtable, créneau `+0x1A0` vrai → sortie ; créneau `+0xA0`
  faux → sortie), et **détruit le `Link` qu'il vient de construire** si
  `Link::setup` rend non nul (0x180219D7F-0x180219D9D). Le prochain passage
  recommencera : aucun abandon définitif.

Ce qui n'est PAS établi ici : que `0x20270` soit effectivement l'identifiant que
l'hôte passe à ce module dans une partie normale (il faudrait le lire côté hôte,
pas ici), ni que les deux gardes d'`apm.dll` soient satisfaites sur cette
machine. **La conclusion bornée : le fil de la machine démarre dès que
`setupLink` réussit une fois, et rien dans ce module ne l'empêche de retenter.**

---

*(sections suivantes en cours de rédaction)*
