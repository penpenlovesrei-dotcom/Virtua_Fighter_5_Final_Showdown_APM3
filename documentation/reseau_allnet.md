# L'appariement ALL.Net — qui allume le réseau, et ce que le jeu attend de SEGA

Relevé statique du 2026-09-05, sur
`runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll.origine` (PE MSVC x64,
base `0x180000000`), `runtime/media/vf5fs/vfes.exe.origine` (base
`0x140000000`) et `runtime/media/vf5fs/apm.reelle.dll` (base `0x180000000`).

Ce document complète `analysis/reseau.md` (l'inventaire des classes) : celui-ci
regarde **ce qu'il y a en amont** de la machine à états (qui la crée, qui
l'allume) et **à côté** (le dialogue HTTP avec les serveurs de SEGA).

---

## 0. Résumé

Le réseau n'est pas bouchonné et il n'est **gardé par aucun réglage du jeu**.
Il est tenté **à chaque trame**, et il s'arrête sur deux conditions, toutes
deux fournies par **`apm.dll`** :

    Sequence_isTest()   doit être FAUX
    AllnetAuth_isGood() doit être VRAI

puis sur la **validation de sept paramètres**, eux aussi tous fournis par
`apm.dll`. Notre stub répond déjà aux deux conditions, mais **quatre de ses
sept valeurs sont refusées** parce qu'elles n'ont pas la bonne longueur (§7).

Le moteur embarque **deux bibliothèques SEGA distinctes**, compilées
séparément, chacune avec sa bannière :

| bibliothèque | bannière | adresse | rôle |
|---|---|---|---|
| **`abaasgs`** | `abaasgs Ver.57fe45a Build:Dec 11 2019 20:13:29` | `0x1805BD6E1` | le **serveur de titre** (GS) : sauvegardes joueur, classements, journaux |
| **`abaaslink`** | `abaaslink Ver.0f03646 Build:Sep  8 2020 18:06:26` | `0x1805C6291` | l'**appariement** (Link) : TURN, STUN, NAT, mise en relation des bornes |

Chacune parle **HTTP** à un serveur ALL.Net qui lui est propre, avec son propre
jeu de chemins `/api/...`. Le transport de jeu (STUN/TURN/UDP) n'intervient
qu'**après** que ce dialogue HTTP a réussi.

Le client HTTP est **libcurl**, statiquement lié (bannières
`# Netscape HTTP Cookie File`, `http://curl.haxx.se/docs/http-cookies.html`,
zlib `deflate 1.2.8`).

**Verdict du 2026-09-06 sur le chiffrement (§6) : nous pouvons fabriquer le
corps HTTP.** Le corps est `en-tête(16 octets, en clair) || AES-256-CBC(zlib(JSON))`,
l'en-tête sert d'IV, et la clé vaut `SHA256(gameId) XOR` une constante de
32 octets écrite en clair dans le moteur (`0x1805CC5D0`). Comme le `gameId`
est fourni par **notre** `apm.dll`, **rien dans cette chaîne ne nous
manque**. La compression et le chiffrement ne peuvent pas être désactivés
depuis le serveur : ils sont câblés à « oui » par un immédiat du moteur
(§6.5).

---

## 1. Qui crée la machine, et qui l'allume

### 1.1 La chaîne complète, établie

    vfes.exe
      |  passe a module_start(args=0x70, argp) un bloc de 0x70 octets
      |  dont argp+0x68 = un OBJET D'INTERFACE (vtable dans vfes.exe)
      |  et dans lequel le moteur ECRIT deux rappels (argp+0x30, argp+0x40)
      v
    module_start                      0x180214C50   (export du moteur)
      |  mov ecx, 0x108 ; call 0x180218930          <- new AbaasManager (0x108 o)
      |  call 0x180218A10                           <- AbaasManager::AbaasManager
      |  singleton range en 0x180C3BDD8
      v
    rappel de trame                   0x180214790   (ecrit dans argp+0x30)
      |  cmp rcx, 0x20270 ; jne ...                 <- code de message
      |  call [hote+0xF0]                           <- Core_execute
      |  if (singleton) call 0x180218F90            <- INCONDITIONNEL
      v
    AbaasManager::update              0x180218F90
      |  ...
      |  cmp qword ptr [rbx+0x10], 0 ; jne          <- LinkMain deja cree ?
      |  test eax, eax ; jne                        <- compte a rebours [rbx+0xAC]
      |  call 0x180219BF0
      v
    AbaasManager::setupLink           0x180219BF0
      |  call [hote+0x1A0]  Sequence_isTest     -> si VRAI, abandon
      |  call [hote+0x0A0]  AllnetAuth_isGood   -> si FAUX, abandon
      |  new LinkMain (0x10 o) ; remplit 7 parametres
      v
    am::abaas::LinkMain::setup        0x1802CAC30  (thunk PIMPL, FEUILLE)
      |  mov rcx, [rcx] ; jmp
      v
    LinkMain::ImplLink::setup         0x1802C9D20  (validation des parametres)

La mise en route de l'appariement (`LinkMain::start`) est ailleurs :

    LinkMain::start (public, thunk)   0x1802CAF20  <- appele de 0x18022C5D0
    LinkMain::ImplLink::start         0x1802CAC40
      |  call 0x1802C7A20   ImplLink::checkMatchingParameter

### 1.2 Réponse : **inconditionnel, puis gardé par `apm.dll`**

- La **création** de `AbaasManager` dans `module_start` est **inconditionnelle** :
  aucun test ne la précède (cf. §1.3).
- Son **update** est appelé **à chaque trame**, sans condition autre que
  « le singleton existe ».
- `setupLink` est **retenté à chaque trame** tant que `LinkMain` n'existe pas
  (`[rbx+0x10] == 0`) et que le compte à rebours `[rbx+0xAC]` est nul. Il n'y a
  donc **pas d'abandon définitif** : le jeu réessaie indéfiniment.
- La **seule** garde est à l'intérieur de `setupLink`, et c'est `apm.dll`.

### 1.3 Le désassemblage de la création, dans `module_start`

    0x180214CD8  call qword ptr [rax + 0xf0]        ; hote->Core_execute (init)
    0x180214CDE  mov rcx, qword ptr [rip + 0xa270f3] ; -> 0x180C3BDD8
    0x180214CE5  test rcx, rcx
    0x180214CE8  je 0x180214cf4
    0x180214CEA  mov rax, qword ptr [rcx]           ; detruit l'ancien
    0x180214CED  mov edx, 1
    0x180214CF2  call qword ptr [rax]
  > 0x180214CF4  mov ecx, 0x108
    0x180214CF9  call 0x180218930                   ; operator new(0x108)
    0x180214CFE  test rax, rax
    0x180214D01  je 0x180214d0b
    0x180214D03  mov rcx, rax
    0x180214D06  call 0x180218a10                   ; AbaasManager::AbaasManager
  > 0x180214D0B  ...
    0x180214D13  mov qword ptr [rip + 0xa270be], rax ; -> 0x180C3BDD8 (singleton)

Aucun `cmp`, aucun `test` conditionnant l'allocation : le sous-système ALL.Net
existe dans **toutes** les exécutions du build APM3.

### 1.4 Le désassemblage de la garde, dans `setupLink`

    0x180219BF0  push rdi
    ...
    0x180219C0D  mov rcx, qword ptr [rip + 0xa21ae4]  ; -> 0x180C3B6F8 (objet hote)
    0x180219C14  mov rax, qword ptr [rcx]             ; sa vtable
    0x180219C17  call qword ptr [rax + 0x1a0]         ; Sequence_isTest()
    0x180219C1D  test al, al
    0x180219C1F  je 0x180219c34                       ; FAUX -> on continue
  > 0x180219C21  xor al, al                           ; VRAI -> on rend faux
    ...
    0x180219C33  ret
  > 0x180219C34  mov rcx, qword ptr [rip + 0xa21abd]  ; -> 0x180C3B6F8
    0x180219C3B  mov rax, qword ptr [rcx]
    0x180219C3E  call qword ptr [rax + 0xa0]          ; AllnetAuth_isGood()
    0x180219C44  test al, al
    0x180219C46  je 0x180219c21                       ; FAUX -> abandon

Et la garde de réessai, en queue d'`AbaasManager::update` :

    0x18021915B  mov eax, dword ptr [rbx + 0xac]      ; compte a rebours
    0x180219161  test eax, eax
    0x180219163  je 0x18021916d
    0x180219165  dec eax
    0x180219167  mov dword ptr [rbx + 0xac], eax
  > 0x18021916D  cmp qword ptr [rbx + 0x10], 0        ; LinkMain deja la ?
    0x180219172  jne 0x180219180
    0x180219174  test eax, eax                        ; compte a rebours ecoule ?
    0x180219176  jne 0x180219180
    0x180219178  mov rcx, rbx
    0x18021917B  call 0x180219bf0                     ; setupLink

---

## 2. Le pont `apm.dll` <-> moteur : la vtable de l'objet hôte

**Le moteur n'importe rien d'`apm.dll`** : ses seuls imports sont
`KERNEL32`, `ADVAPI32`, `ole32`, `OLEAUT32`, `D3DCOMPILER_47`, **`bcrypt`
(13 fonctions)** et **`WS2_32` (28 fonctions)**. Il n'exporte que
`module_start` et `module_stop`.

C'est **`vfes.exe`** qui importe `apm.dll` (57 fonctions) et qui passe au
moteur, dans `argp+0x68`, un **objet C++ d'interface** dont chaque créneau de
vtable est un thunk vers une fonction d'`apm.dll`.

La vtable est en **`vfes.exe` RVA `0x1AF710`** (VA `0x1401AF710`), 57 créneaux,
**exactement une fonction d'`apm.dll` par créneau** :

| créneau | offset | thunk | fonction `apm.dll` |
|---|---|---|---|
| 0-15 | +0x000..+0x078 | `0x140002930`+ | `Aime_*` (16) |
| 16 | +0x080 | `0x140002A30` | `ApmSystemSetting_getAdvertizeSound` |
| 17 | +0x088 | `0x140002A40` | `ApmSystemSetting_getFixedTitle` |
| 18 | +0x090 | `0x140002A50` | `ApmSystemSetting_getMatchingGroup` |
| 19 | +0x098 | `0x140002A60` | `ApmSystemSetting_getTimeToClosingTime` |
| **20** | **+0x0A0** | `0x140002A70` | **`AllnetAuth_isGood`** |
| 21 | +0x0A8 | `0x140002A80` | `AllnetAuth_getAbaasGsServerName` |
| **22** | **+0x0B0** | `0x140002A90` | **`AllnetAuth_getAbaasLinkServerName`** |
| **23** | **+0x0B8** | `0x140002AA0` | **`AllnetAuth_getLocationId`** |
| 24 | +0x0C0 | `0x140002AB0` | `AllnetAuth_getLocationName` |
| **25** | **+0x0C8** | `0x140002AC0` | **`AllnetAuth_getCountryCode`** |
| 26-29 | +0x0D0..+0x0E8 | | `Backup_*` |
| 30 | +0x0F0 | `0x140002B10` | `Core_execute` |
| 31-32 | +0x0F8..+0x100 | | `Core_isExitNeeded`, `Core_exitGame` |
| 33-39 | +0x108..+0x138 | | `Credit_*` |
| 40 | +0x140 | | `Emoney_isOpenMainWindow` |
| 41-42 | +0x148..+0x150 | | `Error_isOccurred`, `Error_setDeviceLost` |
| 43-46 | +0x158..+0x170 | | `Input_isOn`, `Input_isOnNow`, `Input_isGamepadDetect`, `Input_setGamepadConfig` |
| 47-51 | +0x178..+0x198 | | `Sequence_clearBackup`, `getBookkeeping`, `beginPlay`, `continuePlay`, `endPlay` |
| **52** | **+0x1A0** | `0x140002CD0` | **`Sequence_isTest`** |
| **53** | **+0x1A8** | `0x140002CE0` | **`System_getBoardId`** |
| **54** | **+0x1B0** | `0x140002CF0` | **`System_getKeychipId`** |
| **55** | **+0x1B8** | `0x140002D00` | **`System_getGameId`** |
| **56** | **+0x1C0** | `0x140002D10` | **`System_getGameVersion`** — rend un **pointeur vers `{ u32 major; u32 minor; }`**, pas une chaîne (voir §11) |

L'objet hôte est mémorisé par le moteur en **`0x180C3B6F8`** (posé dans
`module_start` depuis `argp+0x68`).

**Réponse à la question 5 : oui, `apm.dll` est entièrement dans la boucle.**
Elle fournit la garde, l'URI des deux serveurs, et les six identifiants de
borne. Rien de tout cela ne vient d'un fichier de configuration ni du registre.

---

## 3. Les sept paramètres de `LinkMain::setup`, et leurs contraintes

### 3.1 D'où vient chaque valeur (`setupLink`, `0x180219BF0`)

Le bloc de paramètres est construit sur la pile en `[rsp+0x70]` par le
constructeur `0x1802C4290`, puis rempli :

| écrit à | par | fonction `apm.dll` |
|---|---|---|
| param **+0x00** | `call [rax+0xb0]` puis `0x18021A470` | `AllnetAuth_getAbaasLinkServerName` |
| param **+0x20** | `call [rax+0x1b8]` puis `0x18021A470` | `System_getGameId` |
| param **+0x40** | `mov word ptr [rsp+0xb0], 1` | *constante* |
| param **+0x42** | `call [rax+0xb8]` ; `mov word ptr [rsp+0xb2], ax` | `AllnetAuth_getLocationId` |
| param **+0x48** | `call [rax+0xc8]` puis `0x18021A470` | `AllnetAuth_getCountryCode` |
| param **+0x68** | `call [rax+0x1b0]` ; **`lea rcx,[rax+0x22]`** | `System_getKeychipId` |
| param **+0x88** | `call [rax+0x1a8]` ; **`lea rcx,[rax+0x22]`** | `System_getBoardId` |
| param **+0xA8** | *non écrit ici* — vient du constructeur | délai serveur |

Le désassemblage, pour les deux cas à `+0x22` :

    0x180219CF6  mov rcx, qword ptr [rip + 0xa219fb]  ; objet hote
    0x180219CFD  mov rax, qword ptr [rcx]
    0x180219D00  call qword ptr [rax + 0x1b0]         ; System_getKeychipId
    0x180219D06  lea rcx, [rax + 0x22]                ; <<< +0x22 !
    0x180219D0A  lea rdx, [rsp + 0xd8]                ; param+0x68
    0x180219D12  call 0x18021a470                     ; affectation de chaine

    0x180219D17  mov rcx, qword ptr [rip + 0xa219da]
    0x180219D1E  mov rax, qword ptr [rcx]
    0x180219D21  call qword ptr [rax + 0x1a8]         ; System_getBoardId
    0x180219D27  lea rcx, [rax + 0x22]                ; <<< +0x22 !
    0x180219D2B  lea rdx, [rsp + 0xf8]                ; param+0x88
    0x180219D33  call 0x18021a470

puis l'appel :

    0x180219D38  mov qword ptr [rsp + 0x28], 0
    0x180219D41  mov qword ptr [rsp + 0x68], 0
    0x180219D4A  lea r8, [rsp + 0x28]                 ; sortie (message d'erreur)
    0x180219D4F  lea rdx, [rsp + 0x70]                ; les parametres
    0x180219D54  mov rcx, qword ptr [rdi + 0x10]      ; le LinkMain
    0x180219D58  call 0x1802cac30                     ; LinkMain::setup

Si `setup` rend non nul, `setupLink` **détruit le `LinkMain`** (`0x1802C4FB0`
puis `operator delete` de 0x10 octets), remet `[rdi+0x10]` à zéro et rend faux
— d'où le réessai à la trame suivante.

### 3.2 Les contraintes, lues dans `ImplLink::setup` (`0x1802C9D20`)

Chaque champ est validé, dans cet ordre, avec son message. `std::string` MSVC
fait 0x20 octets : tampon SSO de 16, taille en `+0x10`, capacité en `+0x18`.

| offset | champ | test exact | message |
|---|---|---|---|
| `+0x00` | **serverURI** | `cmp qword ptr [rdx+0x10], 0` -> **taille non nulle** | `Error: server URI is empty` |
| `+0x20` | **gameId** | `cmp qword ptr [rdx+0x30], 4` -> **taille == 4** | `Error: game id (%s) is invalid` |
| `+0x40` | **majorVersion** (u8) | `cmp al, 0x63` -> **<= 99** | `Error: majorVersion (%u) is invalid` |
| `+0x41` | **minorVersion** (u8) | `cmp al, 0x63` -> **<= 99** | `Error: minorVersion (%u) is invalid` |
| `+0x68` | **keychipId** | `cmp qword ptr [rdx+0x78], 0xb` -> **taille == 11** | `Error: keychip id (%s) is invalid` |
| `+0x88` | **mainId** | `cmp qword ptr [rdx+0x98], 0xb` -> **taille == 11** | `Error: main id (%s) is invalid` |
| `+0xA8` | **serverTimeout** (u32) | `lea eax,[r9-1] ; cmp eax,0x1c ; ja` -> **1..29** | `Error: server timeout (%u) is invalid` |
| `+0x48` | **countryCode** | `cmp qword ptr [rdx+0x58], 3` -> **taille == 3** | `Error: country code (%s) is invalid` |
| `+0x48` | **countryCode** | boucle alphabétique | `Error: country code (%s) include not alphabet` |

Le désassemblage de trois d'entre eux, à l'appui :

    ; gameId : taille exactement 4
    0x1802C9DC8  cmp qword ptr [rdx + 0x30], 4
    0x1802C9DCD  je 0x1802c9e03
    ...          -> "Error: game id (%s) is invalid"

    ; keychipId : taille exactement 11
    0x1802C9E61  cmp qword ptr [rdx + 0x78], 0xb
    0x1802C9E66  je 0x1802c9e9c
    ...          -> "Error: keychip id (%s) is invalid"

    ; countryCode : taille exactement 3
    0x1802C9EF1  cmp qword ptr [rdx + 0x58], 3
    0x1802C9EF6  je 0x1802c9f2c
    ...          -> "Error: country code (%s) is invalid"

    ; serverTimeout : 1..29
    0x1802C9EDD  mov r9d, dword ptr [rdx + 0xa8]
    0x1802C9EE4  lea eax, [r9 - 1]
    0x1802C9EE8  cmp eax, 0x1c
    0x1802C9EEB  ja 0x1802cabe2

En tête, la garde de ré-entrée :

    0x1802C9D67  cmp byte ptr [rcx + 0x1de0], 0
    0x1802C9D6E  je 0x1802c9d97
    ...          -> "Error: setup() is already called."  (rend -3)

### 3.3 Ce que rend vraiment `System_getKeychipId` (`apm.reelle.dll`)

Le `+0x22` du moteur n'est pas une coïncidence : la vraie `apm.dll` rend un
**pointeur vers un tampon statique à deux champs**.

    0x180016440  System_getKeychipId:
      lea  rcx, [rsp+0x20]
      call 0x180021770                  ; -> rax = objet source
      mov  rbx, rax
      lea  rcx, [rip+0x1150F7]          ; -> 0x18012B560       (statique)
      mov  edx, 0x11                    ; 17 octets
      call qword ptr [rip+0x753B1]      ; copie  statique+0x00 <- [src]
      lea  r8,  [rbx + 0x22]            ; <<< +0x22 dans la SOURCE
      mov  edx, 0xc                     ; 12 octets
      lea  rcx, [rip+0x1150FB]          ; -> 0x18012B582 = statique+0x22
      call qword ptr [rip+0x7539B]      ; copie  statique+0x22 <- [src+0x22]
      lea  rax, [rip+0x1150CC]          ; -> 0x18012B560, la BASE du statique
      ret

Donc la structure rendue est :

    +0x00 : 17 octets  (0x11) — identifiant long, 16 caractères + NUL
    +0x22 : 12 octets  (0x0C) — identifiant court, **11 caractères + NUL**

et c'est le champ `+0x22`, de 11 caractères, que le moteur lit — exactement la
longueur que `setup` exige. `System_getBoardId` (`0x180016340`) a la **même
forme**, aux mêmes offsets.

`AllnetAuth_getAbaasLinkServerName` (`0x180009960`) convertit une chaîne
**UTF-16** (`cmp word ptr [rax + r8*2], 0`) en chaîne étroite : le moteur
reçoit bien un `const char *`.

---

## 4. Les URL, les chemins, les hôtes — relevé complet

### 4.1 Serveur d'appariement (`abaaslink`) — **le contrat à refaire**

| adresse | chemin |
|---|---|
| `0x1805C8DE8` | `/api/alive` |
| `0x1805C8DF8` | `/api/turninfo` |
| `0x1805C8E08` | `/api/match` |
| `0x1805C8E18` | `/api/config` |
| `0x1805C8E28` | `/api/log/match_summary` |
| `0x1805C8E40` | `/api/log/match_path_quality` |

Ces six chemins sont contigus en `.rdata` : un seul tableau, une seule
bibliothèque. Ils sont préfixés par l'URI que rend
`AllnetAuth_getAbaasLinkServerName`.

Leur usage se lit dans les noms de méthodes de la machine à états :

    0x1805C93B8  Error : getTurnServerInfo() %d.
    0x1805C93E0  am::abaas::LinkMainStateSetup::requestTurnInfo     -> /api/turninfo
    0x1805C9430  am::abaas::LinkMainStateSetup::responseTurnInfo
    0x1805C9460  Error : httpStatus %d.
    0x1805C94B8  am::abaas::LinkMainStateSetup::requestMatchSetting -> /api/config
    0x1805C94F0  am::abaas::LinkMainStateSetup::responseMatchSetting
    0x1805C9550  am::abaas::LinkMainStateSetup::requestCheckNatType -> STUN
    0x1805C95E8  am::abaas::LinkMainStateStandby::sendCheckServer   -> /api/alive
    0x1805C9620  am::abaas::LinkMainStateStandby::recvCheckServer
    0x1805C98C8  http status : %u                                   (MatchingMatch)

### 4.2 Serveur de titre (`abaasgs`)

| adresse | chemin |
|---|---|
| `0x1805BE128` | `/api/user/load` |
| `0x1805BE138` | `/api/user/save` |
| `0x1805BE148` | `/api/user/heartbeat` |
| `0x1805BE160` | `/api/ranking/list` |
| `0x1805BE178` | `/api/ranking/archive` |
| `0x1805BE190` | `/api/ranking/aggregate` |
| `0x1805BE1A8` | `/api/data/load` |
| `0x1805BE1B8` | `/api/data/save` |
| `0x1805BE1C8` | `/api/server/alive` |
| `0x1805BE1E0` | `/api/log/upload` |
| `0x1805BE1F0` | `/api/code/convert` |
| `0x1805BE208` | `/api/code/create` |

Juste avant, `0x1805BE110` : le gabarit `%s%s%s`, et `0x1805BE118` : le schéma
**`http://`** — en clair, pas `https://`.

### 4.3 Aucun nom d'hôte codé en dur

**Aucune** chaîne du moteur ne contient un nom d'hôte de SEGA : ni `allnet`,
ni `naominet`, ni `sega.jp`, ni `.co.jp`. Balayage complet des 73 428 chaînes
ASCII du binaire. L'URI est **fournie par `apm.dll`**, pas écrite dans le jeu.

Il n'y a donc **pas de nom à détourner par le fichier `hosts`** : il y a un
paramètre à remplir. C'est plus simple.

### 4.4 Le port : `Udp::validatePortConfig`

    0x1805CA040  am::abaas::Udp::validatePortConfig
    0x1805CA0B0  Error: socket(). ErrorCode %u.
    0x1805CA118  am::abaas::Udp::bindAddress
    0x1805CA138  Error: bind(). ErrorCode %u.

Le port UDP local est un paramètre validé, pas une constante repérable dans les
chaînes.

---

## 5. Le contrat JSON — les clés que notre serveur devra honorer

Les clés sont groupées par table en `.rdata`, ce qui identifie leur requête.

### 5.1 `/api/config` — ce que le serveur d'appariement DIT au jeu (`0x1805CBD90`)

    polling
    log_server_host
    log_server_port

Le serveur désigne donc lui-même l'hôte et le port du serveur de
journalisation, et la cadence d'interrogation (`polling`).

> **Correction du 2026-09-06.** Ce paragraphe listait aussi `host` et `port`,
> parce que les cinq chaînes sont contiguës en `.rdata`. Le balayage des
> références les sépare : `polling` / `log_server_host` / `log_server_port`
> ne sont lues que par `0x1802F23D0` (réponse à `/api/config`), tandis que
> `host` (`0x1805CBDE8`) et `port` (`0x1805CBDF0`) ne sont lues que par
> `0x1802F2960` (réponse à `/api/turninfo`, §10.2). **Contiguïté n'est pas
> appartenance.**

### 5.2 `/api/match` — la demande d'appariement (`0x1805CC478`)

    req_id      route       country
    rating_min  rating_max
    member_min  member_max
    scope
    nat_mtype   nat_ftype
    title_key
    _list       _type       condition_change
    status      members

`nat_mtype` / `nat_ftype` sont les deux types que `StunChecker` mesure avant
d'envoyer la demande : le nom RTTI en `0x180669AA0` est

    .?AV?$_Func_base@XW4NATMappingType@StunChecker@abaas@am@@W4NATFilterType@234@@std@@

Le jeu **mesure son NAT par STUN, puis l'annonce au serveur**, qui apparie en
conséquence. `members` et `status` sont ce que la réponse rend : la liste des
pairs.

### 5.3 Télémétrie de fin de partie (`0x1805CC308`)

    match_id     match_started   match_connected   match_finished
    player_num   path_types      match_summary
    loss         path_qualities  match_path_quality

Sans conséquence sur le jeu, mais le serveur doit répondre sans erreur.

### 5.4 Empreinte machine, envoyée au serveur (`0x1805CBFE0`)

    system   lib_hash    os_name      os_ver
    manufacturer  model  locale       boot_time
    timezone      nic_count           memory_size

Récoltée par **WMI**, requêtes SQL en clair (classe RTTI
`am::abaas::SystemInfo::ImplWmi`, `0x18066B410`) :

    0x1805CC090  select * from Win32_PhysicalMemory
    0x1805CC0D0  select * from Win32_TimeZone
    0x1805CC100  select * from Win32_OperatingSystem
    0x1805CC158  select * from Win32_ComputerSystem
    0x1805CC1F0  select * from Win32_NetworkAdapter where AdapterTypeId = 0

### 5.5 Le jeton de session (`am::abaas::Task`, `0x1805BE430`)

    0x1805BE438  %d.%02d
    0x1805BE440  "seq_id":"
    0x1805BE450  "token":"

La réponse porte un **`seq_id`** et un **`token`**, extraits par recherche
littérale de ces deux préfixes. Le format est donc du **JSON**, et notre
serveur doit rendre au moins ces deux champs.

### 5.6 La configuration de cabine, servie par le serveur de titre (`0x180551578`)

    free_buckets   keys   collections   collection_id   key_name
    val1 .. val8
    aime_paid   aime_free   guest_play
    cabinet_properties   value

    misc_hour_of_daystart
    misc_enable_daily_bonus
    misc_other_location_win_streak_max
    misc_guest_other_location_win_streak_max
    misc_life_per_credit
    misc_abort_disconnect_limit
    misc_enable_allnet_accounting
    misc_enable_disconnect_penalty_level_pt
    rule_global_round     rule_global_time     rule_global_energy
    matching_range_interval
    matching_range_rate_diff_
    matching_range_black_max_
    matching_range_black_local_max_
    matching_range_black_pass_max_
    matching_rate_diff_rematch
    matching_rudp_exclusion_time_sec
    misc_*    rule_*    matching_*        (les trois prefixes de filtrage)

`misc_enable_allnet_accounting` **n'est donc pas une garde du réseau** : c'est
une clé de configuration *reçue* du serveur, qui n'existe que si le réseau
fonctionne déjà. Elle ne peut pas conditionner sa mise en route.

---

## 6. La forme du corps HTTP — **entièrement dérivable** (relevé du 2026-09-06)

> **Verdict, d'abord.** Oui, nous pouvons fabriquer une réponse que le jeu
> acceptera. Pour le serveur d'appariement (`abaaslink`), **la clé AES est
> calculée à partir du seul `gameId`** — c'est-à-dire à partir d'une valeur que
> **notre propre `apm.dll` fournit**. Rien n'est négocié, rien ne vient de la
> puce, rien n'est propre à SEGA. Le reste (§6.7) est du zlib et de l'AES-CBC
> standard.

### 6.1 La chaîne, et où elle se lit

`am::abaas::HttpData` (bannière `0x1805C4F70`, GS) et
`am::abaas::link::HttpData` (`0x1805CC6E8`, Link) sont **deux compilations de
la même classe**. Le chantier Link est le suivant :

| méthode | adresse |
|---|---|
| `link::HttpData::HttpData` | `0x1802FA370` |
| `link::HttpData::setParam` | `0x1802FB6D0` |
| `link::HttpData::makeRequestData` | `0x1802FA7F0` |
| `link::HttpData::makeResponseData` | `0x1802FACA0` |
| `link::HttpData::encrypt` | `0x1802FA650` |
| `link::HttpData::decrypt` (inline dans makeResponseData) | `0x1802FB003` |
| `HttpData::setUseCompressEncrypt` (partagée) | `0x1802BC8D0` |
| `HttpData::setParam` (GS) | `0x1802BC8E0` |

et les primitives, partagées par les deux bibliothèques :

| primitive | adresse | remarque |
|---|---|---|
| `util::crypt::Aes::Aes` | `0x1802BCE50` | ouvre le fournisseur |
| `util::crypt::Aes::CryptKey::setKey` | `0x1802BD700` (thunk `0x1802BD6F0`) | |
| `util::crypt::Aes::encryptCbc` | `0x1802BD390` | |
| `util::crypt::Aes::decryptCbc` | `0x1802BD150` | |
| `util::hash::Calcurator` ctor | `0x1802E3A30` | |
| `util::compression::Zlib::compress` | `0x1802BD9E0` | |
| table CRC-32 / CRC-32 | `0x1802BCD10` / `0x1802BCE10` | poly `0xEDB88320` |

### 6.2 L'algorithme : **AES-256-CBC**, par CNG, bourrage PKCS#7

Les 13 imports `bcrypt.dll` du moteur (IAT `0x180346558`..`0x1803465B8`) sont
`BCryptOpenAlgorithmProvider`, `BCryptCloseAlgorithmProvider`,
`BCryptGetProperty`, `BCryptSetProperty`, `BCryptGenerateSymmetricKey`,
`BCryptDestroyKey`, `BCryptEncrypt`, `BCryptDecrypt`, `BCryptCreateHash`,
`BCryptHashData`, `BCryptFinishHash`, `BCryptDestroyHash`, `BCryptGenRandom`.
Tous passent par les thunks `0x1803310D1`..`0x180331119`.

`BCryptOpenAlgorithmProvider` n'a que **trois** sites d'appel :
`0x1802BCF6F` (AES), `0x1802CB257` et `0x1802E3F25` (les deux hacheurs).
Le site AES, dans `util::crypt::Aes::Aes` :

    0x1802BCF64  lea rdx, [rip + 0x30833d]   ; -> 0x1805C52A8  L"AES"
    0x1802BCF6F  call 0x1803310d1            ; BCryptOpenAlgorithmProvider
    ...
    0x1802BCF84  mov r9d, 0x20                            ; 32 octets
    0x1802BCF8A  lea r8, [rip + 0x30833f]    ; -> 0x1805C52D0  L"ChainingModeCBC"
    0x1802BCF91  lea rdx, [rip + 0x308358]   ; -> 0x1805C52F0  L"ChainingMode"
    0x1802BCF9C  call 0x1803310d7            ; BCryptSetProperty

Donc **AES en mode CBC**, sans ambiguïté.

`encryptCbc` (`0x1802BD390`) a sept paramètres :

    encryptCbc(this, const void* in, uint32 inSize, void* out,
               uint32* pOutSize, const uint8 iv[16], bool addPadding)

* `BCryptEncrypt` est appelé avec **`dwFlags = 0`** (pas de
  `BCRYPT_BLOCK_PADDING`) et **`cbIV = 0x10`** ;
* le bourrage est fait **à la main**, en amont :

        0x1802BD47F  mov eax, r15d        ; inSize
        0x1802BD482  and eax, 0xf
        0x1802BD485  mov r14d, 0x10
        0x1802BD48B  sub r14d, eax        ; n = 16 - (inSize % 16)
        ...
        0x1802BD4D1  movzx eax, r14b
        0x1802BD4D5  rep stosb            ; n octets de valeur n

  c'est **PKCS#7 exactement** (bloc entier ajouté quand la taille est déjà
  multiple de 16) ;
* quand `addPadding` vaut 0, la fonction **recopie l'IV final** dans le tampon
  du 6e paramètre (mode chaîné) ; `HttpData` passe toujours **1**
  (`0x1802FA6CF` et `0x1802FA761` : `mov byte ptr [rsp+0x30], 1`).

### 6.3 La clé : **SHA-256(gameId) XOR une constante du binaire**

`link::HttpData::setParam` (`0x1802FB6D0`) fait, dans l'ordre :

1. `memcpy(this+0x1C, seed.data(), 4)` — **quatre octets** ;
2. construit un hacheur `util::hash::Calcurator` avec l'algorithme **2** :

        0x1802FB764  lea edx, [rax + 2]         ; algo = 2
        0x1802FB767  lea rcx, [rbp - 0x29]
        0x1802FB76B  call 0x1802e3a30           ; ctor

   et la table d'algorithmes du constructeur (`0x1802E3B31`) est
   `0 = MD5 (0x10)`, `1 = SHA1 (0x14)`, **`2 = SHA256 (0x20)`**,
   `3 = SHA384 (0x30)`, `4 = SHA512 (0x40)` — chaînes larges en
   `0x1805CA288`..`0x1805CA2C0`. Donc **SHA-256** ;
3. hache la graine (`init` `0x1802E4030`, `execute` `0x1802E3D70`,
   `getResult` `0x1802E3DF0` -> `rcx` = 32 octets). La graine est d'abord
   recopiée octet par octet dans un tampon local de **4 octets**
   (`0x1802FB7C4`..`0x1802FB7E1`) ; `execute(this, données, longueur)` reçoit
   la longueur dans `r8d`, qui contient encore `seed.size()` chargé en
   `0x1802FB7AF` — donc **la longueur hachée est celle du `gameId`, 4**.
   `getResult` (`0x1802E3E01`) rend `[objet+0x48]` octets, soit 0x20 ;
4. **déchiffre une constante de 32 octets par XOR 0x67** :

        0x1802FB85D  mov r8d, 0x20
        0x1802FB863  lea r9, [rip + 0x2d0d66]   ; -> 0x1805CC5D0
        0x1802FB870  movzx eax, byte ptr [rdx + r9]
        0x1802FB875  xor al, 0x67
        0x1802FB877  mov byte ptr [rbp + rdx + 0x17], al

5. **XOR le condensat avec cette constante** (`0x1802FB8A0`, par blocs de 16 en
   SSE puis octet par octet) ;
6. `setKey(this->aes, cle)` via `0x1802BD6F0`, qui force **`r8d = 0x20`** :

        0x1802BD6F0  mov rcx, qword ptr [rcx + 0x18]
        0x1802BD6F4  mov r8d, 0x20                 ; cbSecret = 32
        0x1802BD6FA  jmp 0x1802bd700               ; CryptKey::setKey

   donc **AES-256**.

**La constante, à l'adresse `0x1805CC5D0`** (32 octets, en clair dans le
`.rdata` du moteur) :

    dans le binaire : 3f d1 1a 19 4b cd 95 a8 ab cb 14 8d a3 62 e1 f7
                      ed 9d fd 00 3e 14 15 42 dd 8d 2c fe ca 35 74 d9
    apres XOR 0x67  : 58 b6 7d 7e 2c aa f2 cf cc ac 73 ea c4 05 86 90
                      8a fa 9a 67 59 73 72 25 ba ea 4b 99 ad 52 13 be

La **même** constante est en `0x1805C4E80` pour la bibliothèque GS
(`0x1802BC960` : même boucle, même `xor al, 0x67`). Les deux bibliothèques
partagent le sel ; elles diffèrent par ce qu'elles XORent avec.

**Et la graine est le `gameId`.** `ImplLink::setup` recopie le bloc de
paramètres champ par champ ; le `lea` est explicite :

    0x1802C9F9B  lea r14, [rbx + 0x20]        ; rbx = bloc de parametres
                                              ; +0x20 = gameId (§3.2)

et `r14` est ce qui devient la graine (`0x1802CA131` -> struct `rbp+0x200`,
puis `0x1802EC33B` : `lea r9, [r15 + 0x20]` -> 4e argument de `setParam`).
Cohérent avec le `memcpy` de **4 octets** du point 1, et avec la contrainte
« `gameId` de taille exactement 4 » de `ImplLink::setup` (§3.2).

**Formule :**

    cle_AES256 = SHA256(gameId_4_octets) XOR 58b67d7e2caaf2cfccac73eac4058690
                                             8afa9a6759737225baea4b99ad5213be

Trois exemples calculés (le `gameId` réel de SEGA nous est inconnu, mais
**c'est notre stub qui le fournit**, donc nous le choisissons) :

| `gameId` | clé AES-256 |
|---|---|
| `"0000"` | `c247264d42c064d65e294435f4b76032bd9ff39ba0a49556562495fccd373a1e` |
| `"VF5F"` | `bfea5cf9e4fe2dae5088b8110c82aff447f52ea9f2c4f10b6917835618fac4fa` |
| `"SDHF"` | `17f7bd8743ea7e007cdc77684e596930a5dbbff979dc2c6fe33885ce43b91221` |

### 6.4 Le format du corps : **en-tête de 16 octets, qui est aussi l'IV**

`makeRequestData` (`0x1802FA7F0`) construit un en-tête sur la pile en
`[rsp+0x58]`, puis :

    0x1802FAA6D  mov rdx, [rsp+0x48]      ; taille du corps traite
    0x1802FAA72  add rdx, 0x10
    0x1802FAA7C  call 0x180012fb0         ; out.resize(taille + 16)
    0x1802FAAB4  movups xmm0, [rsp+0x58]  ; l'en-tete
    0x1802FAAB9  movups [rcx], xmm0       ; ecrit AU DEBUT du corps
    0x1802FAB14  call 0x18029ee00         ; memcpy(out+16, corps, taille)

et ce **même en-tête est passé comme IV** au chiffrement
(`0x1802FA97D : lea r9, [rsp+0x58]` -> `link::HttpData::encrypt` -> 6e argument
d'`encryptCbc`). À la réception, l'IV est de même les 16 premiers octets reçus
(`0x1802FAFDD : lea rax, [rsp+0x500]`, la copie de l'en-tête).

    corps HTTP = EN-TETE(16 octets, en clair) || AES-256-CBC(zlib(JSON))
    IV = l'EN-TETE lui-meme

**En-tête de REQUÊTE** (jeu -> serveur), construit en `0x1802FA86E`..`0x1802FA89A` :

| octets | contenu | d'où |
|---|---|---|
| 0 | `0x01` | constante (`mov word ptr [rsp+0x58], 0x101`) |
| 1 | `0x01` | constante |
| 2 | `majorVersion` — **vaut 1** | `[this+0x18]`, posé par `setParam` |
| 3 | `minorVersion` — **vaut 0** | `[this+0x19]`, posé par `setParam` |
| 4..7 | les **4 octets du `gameId`**, tels quels | `[this+0x1C]` |
| 8..11 | **CRC-32 du JSON en clair**, gros-boutien | `bswap` en `0x1802FA869` |
| 12..15 | **aléa 32 bits** | `rand_s`, `call 0x18031A864` |

*(les octets 2 et 3 sont bien `majorVersion`/`minorVersion` : `setParam` les
reçoit de `[struct+0x40]` / `[struct+0x41]`, et `ImplLink::setup` remplit ces
deux champs depuis `param+0x40` / `param+0x41` en `0x1802C9FBE`..`0x1802C9FCF`,
qui sont les deux versions validées `<= 99` du §3.2 — **ce ne sont pas des
drapeaux de compression**.)*

**En-tête de RÉPONSE** (serveur -> jeu), vérifié en `0x1802FAD7F`..`0x1802FB36B` :

| octets | contenu | contrôle |
|---|---|---|
| 0 | `0x01` | `cmp bl, 1` ; sinon **retour −6** |
| 1 | `0x01` | `cmp al, 1` ; sinon **retour −7** |
| 2..3 | **code de retour**, u16 gros-boutien | `rol ax, 8` puis rendu au 4e argument ; **doit valoir 0** pour que le corps soit décodé |
| 4..7 | **CRC-32 du JSON en clair**, gros-boutien | comparé en `0x1802FB364` ; sinon **retour −8** |
| 8..11 | **taille du JSON décompressé**, gros-boutien | sert au `resize` avant `uncompress` (`0x1802FB124`..`0x1802FB158`) |
| 12..15 | ignoré | |

Les deux en-têtes ne sont donc **pas la même structure** : c'est une union à
deux branches, qui ne partage que les deux octets de version. En particulier
la réponse ne redit pas si elle est compressée ou chiffrée : **le client
applique ses propres réglages** (§6.5) dans les deux sens.

Taille minimale d'une réponse : **17 octets** — `makeResponseData` refuse
`< 16` (`ERROR: srcData size is invalid`, retour −1) et le chemin de décodage
exige `> 16` (`0x1802FAE80 : cmp r9, 0x10 ; jbe`).

### 6.5 **L'interrupteur existe, mais il est câblé à « oui »**

`HttpData` porte deux octets de réglage, distincts des octets d'en-tête :

    [this+0x21]  = « compresser »      teste en 0x1802FA8B2 (requete)
                                       et  en 0x1802FB15E (reponse)
    [this+0x22]  = « chiffrer »        teste en 0x1802FA973 (requete)
                                       et  en 0x1802FAF69 (reponse)

Ils sont posés par la fonction la plus courte du chantier :

    0x1802BC8D0  mov byte ptr [rcx + 0x21], dl      ; compresser
    0x1802BC8D3  mov byte ptr [rcx + 0x22], r8b     ; chiffrer
    0x1802BC8D7  ret

Le constructeur les met déjà tous deux à 1
(`0x1802FA3A7 : mov word ptr [rbx+0x20], 0x100` puis
`0x1802FA3AD : mov byte ptr [rbx+0x22], 1`), et l'unique site d'appel de
`0x1802BC8D0` les relit d'une structure de configuration
(`0x1802EC293`..`0x1802EC2A5`, puis `0x1802EC35D`..`0x1802EC370`) — structure
que `ImplLink::setup` remplit avec une **constante immédiate** :

    0x1802CA070  mov dword ptr [rbp + 0x1a8], 5       ; delai serveur (ecrase ensuite
                                                      ; par param+0xA8)
    0x1802CA07A  mov dword ptr [rbp + 0x1ac], 0x80
    0x1802CA08A  lea rdx, [rip + 0x2fccc7]            ; "abaaslink"  (agent)
    0x1802CA09D  mov word ptr [rbp + 0x1d0], 0x101    ; <<< +0x28 = 1, +0x29 = 1
                                                      ;     compresser = OUI
                                                      ;     chiffrer   = OUI

**Il n'y a donc aucun moyen, côté serveur ni côté configuration, de demander du
clair.** Le seul interrupteur est ce `0x0101` immédiat dans le moteur : deux
octets à `0x1802CA0A4` (fichier) qui, mis à `0x0000`, désactiveraient
compression **et** chiffrement dans les deux sens. C'est une piste de repli,
pas une nécessité — et elle n'a **pas** été essayée (lecture seule).

Prémisse qui borne : cette conclusion ne vaut que pour les **six** `HttpData`
du serveur d'appariement, construits dans la boucle `0x1802EC330`..`0x1802EC37A`
(`cmp ebx, 6`), un par chemin `/api/...` du §4.1. Le côté GS a sa propre
instance et sa propre configuration, non lue.

### 6.6 La compression : zlib, niveau 6, format zlib (pas raw deflate)

`util::compression::Zlib::compress` (`0x1802BD9E0`) :

    0x1802BDA6A  lea r8, [rip + 0x307afb]   ; -> 0x1805C556C  "1.2.8"
    0x1802BDA71  mov r9d, 0x58              ; sizeof(z_stream) = 88
    0x1802BDA7B  lea edx, [r9 - 0x52]       ; niveau = 6
    0x1802BDA7F  call 0x18029ce80           ; deflateInit_(strm, 6, "1.2.8", 88)

`deflateInit_` (et non `deflateInit2_`) : **`windowBits = 15`, format zlib
RFC 1950** (en-tête `78 9c`, somme Adler-32 en queue). Pas de raw deflate, pas
de gzip.

Ordre : **JSON -> zlib -> AES** à l'émission, **AES -> zlib -> JSON** à la
réception. C'est visible dans `makeRequestData` (compression en `0x1802FA8C3`
avant chiffrement en `0x1802FA98A`) et dans `makeResponseData` (déchiffrement
en `0x1802FB003` avant décompression en `0x1802FB1F7`).

Type MIME : `Content-Type: application/octet-stream` (`0x1805C3868`, posé en
`0x1802EC2C1`).

### 6.7 Recette complète pour notre serveur (côté `abaaslink`)

    K   = SHA256(gameId)  XOR  58b67d7e2caaf2cfccac73eac4058690
                               8afa9a6759737225baea4b99ad5213be

    lire une requete :
      h    = corps[0:16]                       # aussi l'IV
      assert h[0] == 1 and h[1] == 1
      # h[2], h[3] = majorVersion, minorVersion ; h[4:8] = gameId
      clair = zlib.decompress(unpad_pkcs7(AES256_CBC_decrypt(K, iv=h, corps[16:])))
      assert crc32(clair) == be32(h[8:12])
      json.loads(clair)

    fabriquer une reponse :
      z    = zlib.compress(json_utf8, 6)        # format zlib, pas raw
      h    = bytes([1, 1]) + be16(0)            # 0 = succes
           + be32(crc32(json_utf8))
           + be32(len(json_utf8))
           + os.urandom(4)
      corps = h + AES256_CBC_encrypt(K, iv=h, pad_pkcs7(z))

Ce que **nous ne savons pas** : si le serveur doit renvoyer un code HTTP 200
(`Error : httpStatus %d.`, `0x1805C9460`, existe mais son test n'a pas été
lu), et si un en-tête HTTP particulier est exigé en retour.

### 6.8 Le côté GS (`abaasgs`) : là, il manque bien une clé

`HttpData::setParam` du GS (`0x1802BC8E0`) ne hache rien : il XORe la **même**
constante de 32 octets avec un **tampon de 32 octets fourni par l'appelant**
(cinquième argument, une paire début/fin lue en `0x1802BC987`) :

    cle_GS = titleKey  XOR  58b6...13be

et `GsMain::ImplGs::setTitleServerConfig` (`0x1805BD7E8`) refuse tout
`titleKey` dont la taille n'est pas 32 (`ERROR: titleKey's size is not 32Byte.`,
`0x1805BD898`).

**Ce `titleKey` n'est pas un secret de SEGA.** L'appelant a été remonté le
2026-09-06 : `0x1802198B0` recopie **32 octets d'un littéral du binaire**,
`0x1805511D8`, par une boucle explicite (`0x180219A35`…`0x180219A66`,
`cmp rbx, 0x20`). Ce littéral n'a **qu'une seule référence** dans tout le
binaire, celle-là.

    titleKey = 1469b0169c238709ea4f1bace7021748
               1d6230e6db2abe2f9d17e6336f433481

    cle_GS   = 4cdfcd68b08975c626e36846230791d8
               9798aa818259cc0a27fdadaac211273f

**Vérifié à l'exécution** (§14.3) : avec cette clé, `/api/data/load` du serveur
de titre se déchiffre et se lit.

---

## 7. **Ce que notre `apm.dll` devrait fournir en plus** — le livrable

`tools/apm_stub.c` exporte déjà les huit fonctions concernées, avec la bonne
convention d'appel. **Les valeurs, elles, sont refusées** : le stub rend
partout la chaîne `"0000"`, qui n'a la bonne longueur que par hasard pour
`gameId`.

| créneau | fonction | notre stub aujourd'hui | ce que `setup` exige | verdict |
|---|---|---|---|---|
| +0x1A0 | `Sequence_isTest` | scénario (faux hors menu) | **faux** | OK |
| +0x0A0 | `AllnetAuth_isGood` | `return 1` | **vrai** | OK |
| +0x0B0 | `AllnetAuth_getAbaasLinkServerName` | `"0000"` | **URI non vide** — techniquement accepté, mais libcurl ne pourra rien en faire | **à changer** : `"http://127.0.0.1:8080"` |
| +0x1B8 | `System_getGameId` | `"0000"` (4) | **4 caractères** | OK par hasard |
| +0x0C8 | `AllnetAuth_getCountryCode` | `"0000"` (4) | **3 caractères, alphabétiques** | **CASSÉ** -> `"JPN"` |
| +0x1B0 | `System_getKeychipId` | `const char* "0000"` | **pointeur vers une struct**, id de **11 caractères en `+0x22`** | **CASSÉ** (mauvaise forme *et* mauvaise longueur) |
| +0x1A8 | `System_getBoardId` | `const char* "0000"` | idem, **11 caractères en `+0x22`** | **CASSÉ** |
| +0x0B8 | `AllnetAuth_getLocationId` | `long long` `0` | u16 lu dans `ax` ; non validé par `setup` | tolérable, mais à donner |

Et pour le serveur de titre (`abaasgs`) :

| créneau | fonction | à fournir |
|---|---|---|
| +0x0A8 | `AllnetAuth_getAbaasGsServerName` | l'URI du serveur GS |
| +0x0C0 | `AllnetAuth_getLocationName` | nom de boutique |

**Trois corrections suffisent à faire passer `LinkMain::setup`** :

1. `AllnetAuth_getCountryCode` -> une chaîne de **3 lettres** (`"JPN"`).
2. `System_getKeychipId` -> un pointeur vers un tampon statique d'au moins
   `0x22 + 12` octets, dont l'octet `+0x22` commence une chaîne de **11
   caractères** terminée par NUL.
3. `System_getBoardId` -> la même forme, 11 caractères en `+0x22`.

Plus, pour que le dialogue HTTP aille quelque part :

4. `AllnetAuth_getAbaasLinkServerName` -> une **vraie URI** vers notre serveur.

*(Rappel : ce document est en lecture seule. Rien n'a été modifié dans
`tools/apm_stub.c` ni dans `tools/gen_apm_stub.py`.)*

> **Piège à noter.** `tools/apm_stub.c` **n'est pas une source** : il est
> **régénéré à chaque exécution de `tools/gen_apm_stub.py`**. Une correction
> écrite dans le `.c` disparaît à la compilation suivante. Les quatre
> corrections ci-dessus ont été portées dans le **générateur** (fait, hors de
> cette session), pas dans le produit.
>
> **Et une conséquence nouvelle, depuis le §6.3 :** le `gameId` que rend
> `System_getGameId` n'est plus seulement « quatre caractères quelconques ».
> C'est **la graine de la clé AES**. Le stub et le serveur doivent employer la
> **même** valeur, sans quoi le serveur déchiffrera du bruit. Comme le serveur
> peut relire le `gameId` dans les octets 4..7 de l'en-tête reçu (§6.4), il n'a
> pas besoin de le connaître à l'avance — mais il ne peut pas non plus
> l'ignorer.

---

## 8. Les identifiants de borne — récapitulatif (question 6)

| identifiant | lu par | forme exigée |
|---|---|---|
| **URI serveur Link** | `AllnetAuth_getAbaasLinkServerName` (hôte +0x0B0) | non vide |
| **URI serveur GS** | `AllnetAuth_getAbaasGsServerName` (hôte +0x0A8) | non vide (`ERROR: strServerURI is empty.`) |
| **gameId** | `System_getGameId` (hôte +0x1B8) | 4 caractères |
| **keychipId** (n° de série) | `System_getKeychipId` (hôte +0x1B0), champ `+0x22` | 11 caractères |
| **mainId / boardId** | `System_getBoardId` (hôte +0x1A8), champ `+0x22` | 11 caractères |
| **countryCode** | `AllnetAuth_getCountryCode` (hôte +0x0C8) | 3 lettres |
| **locationId** (boutique) | `AllnetAuth_getLocationId` (hôte +0x0B8) | u16 |
| **regionCode** | *exporté par la vraie `apm.dll` (`AllnetAuth_getRegionCode`, `System_getRegionCode`) mais **absent de la vtable de `vfes.exe`*** | non utilisé |
| **titleKey** | posé par `GsMain::setTitleServerConfig` | 32 octets |
| **majorVersion / minorVersion** | constante `1` / `0` dans le moteur | <= 99 |
| **serverTimeout** | défaut du constructeur `0x1802C4290` | 1..29 |

La vraie `apm.dll` exporte aussi `AllnetAuth_isDevelop`,
`AllnetAuth_getLocationNickname`, `AllnetAuth_getRegionName`,
`System_getAppRootPath`, `System_getResolution` — mais **`vfes.exe` ne les
importe pas** : elles ne sont pas dans la vtable de 57 créneaux, donc le moteur
ne peut pas les voir.

---

## 9. Ce qui n'est PAS établi

*(les trois premiers points de la version du 2026-09-05 sont résolus par le
§6 : algorithme, clé, IV, bourrage, sens de la compression. Ils sont conservés
biffés pour mémoire.)*

- ~~**Le côté GS.** L'appelant de `GsMain::ImplGs::setTitleServerConfig`~~ —
  toujours non remonté, mais **ce n'est plus le trou le plus gênant** : la clé
  du serveur d'appariement ne dépend pas du `titleKey` (§6.3). Le `titleKey`
  reste inconnu pour le serveur de **titre** seulement.
- ~~**L'algorithme exact de dérivation de clé.**~~ Résolu : SHA-256 du
  `gameId`, XOR d'une constante du binaire, AES-256-CBC, IV = en-tête de
  16 octets, bourrage PKCS#7 fait à la main (§6.2, §6.3, §6.4).
- **La forme précise du JSON** *des requêtes*. Les clés des **réponses** de
  `/api/turninfo` et `/api/config` sont désormais lues avec leurs types (§10) ;
  celles de `/api/match` ne le sont pas, et leur imbrication non plus.
  `_list`, `_type` sont vraisemblablement des suffixes concaténés, ce n'est
  toujours pas vérifié.
- **Le champ param+0x42.** Il reçoit le mot de poids faible de
  `AllnetAuth_getLocationId`, et `setup` ne le valide pas. Que le serveur en
  fasse quelque chose est une **supposition**.
- **Le port UDP** et l'adresse locale (`localIpAddress`, `0.0.0.0`) : leurs
  valeurs par défaut viennent du constructeur `0x1802C4290`, qui n'a pas été
  lu.
- **`LinkMain::start`.** Appelé depuis `0x18022C5D0`, dans la région
  d'appariement du jeu. **Ni cette fonction ni ses gardes n'ont été lues** : on
  ne sait pas encore ce qui décide d'entrer en appariement une fois `setup`
  réussi. (La machine à états elle-même est le sujet d'un autre agent.)
- **Les valeurs réelles de SEGA** (le `gameId` à 4 lettres de VF5FS, un
  `keychipId` plausible) n'ont pas été trouvées dans les binaires dont nous
  disposons. Pour notre propre serveur, elles peuvent être arbitraires — seule
  la **longueur** est vérifiée côté jeu.
- **Rien n'a été exécuté.** Tout ci-dessus est de la lecture statique ; aucune
  de ces conclusions n'a été confirmée par un lancement du jeu.
- **Le générateur, pas le produit.** `tools/apm_stub.c` est **régénéré à chaque
  exécution de `tools/gen_apm_stub.py`** : toute correction écrite directement
  dans le `.c` est perdue à la compilation suivante. Le fichier qui fait foi
  est le générateur.

---

## 10. La spécification du serveur minimal `abaaslink`

Cette section est écrite pour qu'on puisse coder le serveur **en la lisant
seule**. Elle ne couvre que le serveur d'**appariement** (`abaaslink`) ; le
serveur de titre (`abaasgs`) a sa propre clé et n'est pas requis pour
l'appariement.

### 10.1 L'enveloppe, identique sur les six chemins

* **Méthode** : POST (à confirmer — non lu ; `Content-Type:
  application/octet-stream` est bien posé, `0x1802EC2C1`).
* **URL** : `<serverURI>` + le chemin littéral. Le `serverURI` est ce que rend
  `AllnetAuth_getAbaasLinkServerName` — **notre stub**. La concaténation est
  brute (`0x1802D5C7C` : `operator+(base, "/api/turninfo")`), donc le
  `serverURI` **ne doit pas** se terminer par `/`.
* **Corps** : `EN-TETE(16) || AES-256-CBC(zlib(JSON))`, dans les deux sens.
* **Clé** : `SHA256(gameId) XOR 58b67d7e…13be` (§6.3). Le serveur la calcule
  lui-même à partir du `gameId` qu'il lit dans les octets 4..7 de l'en-tête
  reçu — **il n'a donc rien à connaître d'avance**.
* **En-tête de réponse** (§6.4) :

      octet 0     : 0x01
      octet 1     : 0x01
      octets 2-3  : code de retour, u16 gros-boutien, 0 = succes
      octets 4-7  : CRC-32 du JSON en clair, gros-boutien
      octets 8-11 : taille du JSON en clair, gros-boutien
      octets 12-15: 4 octets libres (aleatoires)

  et ces 16 octets sont aussi l'**IV**.
* **Statut HTTP** : `responseTurnInfo` exige `200` explicitement
  (`0x1802D9696 : mov ecx, 0xc8 ; cmp ax, cx`) puis exige que le code de
  retour des octets 2-3 soit **0** (`0x1802D96A4`). Les deux contrôles sont
  successifs ; échouer l'un ou l'autre renvoie la machine sur son chemin
  d'erreur.
* **Corps de réponse minimal** : 17 octets. Moins de 16 = `ERROR: srcData size
  is invalid` ; exactement 16 = le corps est ignoré (§6.4).

### 10.2 `/api/turninfo` — **le premier, et celui qui donne les identifiants TURN**

C'est l'état 0 de `LinkMainStateSetup` :
`requestTurnInfo` `0x1802D8F80` -> `responseTurnInfo` `0x1802D9620`, et le
décodage du JSON est `0x1802F2960`.

**Requête.** Corps JSON **vide** : la chaîne passée à l'émetteur est construite
vide juste avant l'appel (`0x1802D5C95`..`0x1802D5CA3`, puis
`0x1802D5CAD : lea r9, [rsp+0x38]`). *Non vérifié à l'exécution* — c'est une
lecture du site d'appel, pas une capture réseau.

**Réponse.** Un objet JSON (le nœud racine doit être de type 5 = objet) avec
**exactement quatre clés**, toutes obligatoires — chacune est cherchée, son
type est comparé, et un type faux fait échouer tout le décodage :

| clé | type attendu | code du contrôle | destination |
|---|---|---|---|
| `host` | **chaîne** (type 3) | `0x1802F2A6E : cmp ebx, 3` | `TurnContext::setTurnServerAddress` |
| `port` | **nombre** (type 2) | `0x1802F2BA2 : cmp ebx, 2` | idem, en u16 |
| `id` | **chaîne** (type 3) | `0x1802F2CBC : cmp ebx, 3` | session `+0x188` : **le `username` TURN** |
| `pw` | **chaîne** (type 3) | `0x1802F2DF1 : cmp ebx, 3` | session `+0x1A8` : **le `password` TURN** |

*(les littéraux : `host` `0x1805CBDE8`, `port` `0x1805CBDF0`, `pw`
`0x1805CBDF8`, et `id` `0x180551644` — ce dernier est **partagé** avec la table
de configuration de cabine du §5.6 : c'est de la mutualisation de littéral par
l'éditeur de liens, pas une parenté.)*

**Il n'y a PAS de clé `realm`, ni de `ttl`, ni d'`uri`.** Le `realm` n'est pas
transmis par HTTP : le jeu suit le protocole TURN standard à identifiants de
longue durée, où c'est le serveur TURN lui-même qui annonce son `REALM` (et son
`NONCE`) dans sa réponse `401`. **Un coturn n'a donc qu'à déclarer un
utilisateur portant l'`id` et le `pw` que ce JSON aura donnés** ; le `realm`
est celui de coturn (`--realm`), et le jeu s'y conformera.

**Réponse minimale, en clair, avant enveloppe :**

    {"host":"127.0.0.1","port":3478,"id":"vf5","pw":"vf5"}

À chiffrer et préfixer comme au §10.1, avec le code de retour à 0.

*Ce que je ne sais pas encore* : si `host` peut être un nom (il finit dans
`createRemoteAddress`, `0x1805C7E68`, non lu) ou doit être une adresse IPv4
littérale ; si `port` doit tenir sur 16 bits (il est lu en `word`,
`0x1802D9739 : movzx r8d, word ptr [rbp-0x19]`, donc **oui, 0..65535**) ;
et si des clés supplémentaires sont tolérées (le décodeur ne fait que des
recherches par nom, donc **oui selon toute vraisemblance** — mais ce n'est pas
vérifié).

### 10.3 `/api/config` — le réglage de l'appariement

`LinkMainStateSetup::requestMatchSetting` (`0x1805C94B8`) /
`responseMatchSetting` (`0x1805C94F0`) ; décodage `0x1802F23D0`.

| clé | type attendu | code du contrôle |
|---|---|---|
| `polling` | **nombre** (type 2) | `0x1802F24DE : cmp ebx, 2` |
| `log_server_host` | **chaîne** (type 3) | `0x1802F25F6 : cmp ebx, 3` |
| `log_server_port` | **nombre** (type 2) | `0x1802F272B : cmp ebx, 2` |

Réponse minimale plausible :

    {"polling":1000,"log_server_host":"127.0.0.1","log_server_port":80}

*Non établi* : l'unité de `polling` (millisecondes ? secondes ?), et si les
trois clés sont toutes obligatoires ou seulement lues quand elles existent.
Le motif du décodeur (`type != attendu` -> saut par-dessus l'affectation, sans
message d'erreur, cf. `0x1802F24DE`/`jne`) suggère qu'une clé **absente** est
simplement ignorée et laisse la valeur par défaut — à confirmer.

### 10.4 `/api/alive` — le battement de cœur

`LinkMainStateStandby::sendCheckServer` (`0x1805C95E8`) /
`recvCheckServer` (`0x1805C9620`). **Aucune clé JSON ne lui a été rattachée**
par le balayage des références : la réponse minimale est probablement un objet
vide, `{}`, avec le code de retour à 0. **Non vérifié.**

### 10.5 `/api/match` — l'appariement proprement dit

Les clés du §5.2 (`req_id`, `route`, `country`, `rating_min`/`max`,
`member_min`/`max`, `scope`, `nat_mtype`, `nat_ftype`, `title_key`,
`condition_change`, `status`, `members`, `key`, `num`, `_list`, `_type`) sont
relevées mais leur sens de circulation n'était pas départagé. **Il l'est
désormais : voir §12.** Et les deux fonctions désignées ici, `0x1802F6370` et
`0x1802F6F40`, **ne concernent pas `/api/match`** — ce sont les encodeurs des
deux journaux de fin de partie (§12.1). La présomption qui les rattachait à
l'appariement venait du seul fait qu'elles emploient la clé `port` ; c'était
une coïncidence de littéral.

Ce qui est sûr : le jeu **mesure son type de NAT par STUN avant** d'appeler ce
chemin (`requestCheckNatType`, `0x1805C9550`), donc `/api/turninfo` et
`/api/config` doivent avoir abouti, et un serveur STUN/TURN doit répondre,
**avant** que `/api/match` ne soit sollicité.

### 10.6 `/api/log/match_summary` et `/api/log/match_path_quality`

Télémétrie de fin de partie (§5.3). Sans conséquence sur le déroulement, mais
le serveur doit répondre 200 avec un en-tête valide et le code de retour 0,
sans quoi le client journalise une erreur. Réponse minimale : `{}`.

### 10.7 Ordre d'appel

    LinkMain::setup            <- valide les 7 parametres (apm.dll)  §3
      LinkMainStateSetup
        etat 0 : /api/turninfo      -> host, port, id, pw
        etat 1..3 : /api/config     -> polling, log_server_*
                    STUN            -> nat_mtype, nat_ftype
      LinkMain::start            <- declenche par le jeu (0x18022C5D0)
      LinkMainStateStandby
        /api/alive  (cadence : `polling`)
      LinkMainStateMatching
        /api/match
      fin de partie
        /api/log/match_summary, /api/log/match_path_quality

La table de sauts de `LinkMainStateSetup::update` est en `0x1802D9220` (six
états : `0x1802D8FD6`, `0x1802D9079`, `0x1802D9086`, `0x1802D9093`,
`0x1802D91E7`, `0x1802D91F7`). Le détail de cette machine est le sujet de
`analysis/reseau_machine.md`.

### 10.8 Ce qu'il reste à savoir avant d'écrire le serveur

- ~~La méthode HTTP~~ — **lue, c'est POST** (§13).
- ~~Le corps des requêtes~~ — **l'enveloppe commune est lue** (§13.2) ; il
  reste le corps propre à `/api/config` et `/api/log/*`.
- **Si `/api/alive` attend un contenu.**
- **Ce que le serveur doit répondre à `/api/match`** pour qu'un appariement
  aboutisse — c'est le seul point qui demande encore un vrai travail de
  lecture.
- **Le `gameId` réel de SEGA** reste inconnu ; sans importance, puisque c'est
  notre `apm.dll` qui le fournit et que le serveur le relit dans l'en-tête.


---

## 11. Le mur du serveur de titre, et sa chute (2026-09-06)

Le passage des six chaînes du chemin `setupLink` en UTF-16 a **réussi**, et
c'est précisément ce qui a fait apparaître le plantage suivant : en ASCII, le
`gameId` ne survivait pas à la conversion, sa taille valait 0, et
`am::abaas::GsMain::ImplGs::setTitleServerConfig` (`0x1802942A0`) **refusait la
configuration au tout premier contrôle**. Le reste du chemin n'était donc
jamais parcouru. La correction n'a pas cassé le réseau : elle a ouvert la
porte 1.

### 11.1 Les cinq contrôles de `setTitleServerConfig`

La structure de configuration reçue en `rdx` :

| offset | champ |
|---|---|
| `+0x00` | `std::string serverURI` (taille en `+0x10`) |
| `+0x20` | `std::string gameId` (taille en `+0x30`) |
| `+0x40` | `u8 majorVersion` |
| `+0x41` | `u8 minorVersion` |
| `+0x48`/`+0x50` | `std::vector<u8> titleKey` |

Les contrôles, **dans cet ordre** — le premier qui échoue rend `-2` et le
reste n'est jamais atteint :

| ordre | contrôle | message |
|---|---|---|
| 1 | `[rdx+0x30] == 4` | `ERROR: gameId(%s) is invalid.` |
| 2 | `[rdx+0x40] <= 0x63` | `ERROR: majorVersion(%d) is invalid.` |
| 3 | `[rdx+0x41] <= 0x63` | `ERROR: minorVersion(%d) is invalid.` |
| 4 | `[rdx+0x10] != 0` | `ERROR: strServerURI is empty.` |
| 5 | `[rdx+0x50] - [rdx+0x48] == 0x20` | `ERROR: titleKey's size is not 32Byte.` |

### 11.2 `System_getGameVersion` n'est pas un getter de chaîne

Les **deux** sites d'appel du créneau `+0x1C0` lisent le retour de la même
façon : un pointeur, l'octet `+0` pour le majeur, l'octet `+4` pour le mineur.
C'est la forme d'un `struct { uint32_t major; uint32_t minor; }`.

    0x180219A14  call [rax+0x1C0]              ; la configuration du serveur de titre
    0x180219A1A  mov  rax, qword ptr [rax]     ; il lit HUIT octets
    0x180219A1D  mov  byte ptr [rbp-9],  al    ; majorVersion = octet 0
    0x180219A20  shr  rax, 0x20
    0x180219A24  mov  byte ptr [rbp-8],  al    ; minorVersion = octet 4

    0x1800DE298  call [rax+0x1C0]              ; l'événement `vfes_se_title`
    0x1800DE2A6  movzx eax, byte ptr [rax]     ; octet 0        (NULL toléré ici)
    0x1800DE2AF  movzx eax, byte ptr [rcx+4]   ; octet 4

Notre stub rendait `const char *"0000"`. Le moteur y lisait donc `0x30` et
`0x00` : **version « 48.00 »**. Mesuré, et non deviné :

    2.7 ms  version GS : major=48 minor=0 -> "48.00"

### 11.3 Le défaut est dans le binaire d'origine

`setTitleServerConfig` accepte jusqu'à **99** pour chaque moitié, alors que le
formateur qui suit n'a qu'un tampon de **cinq** octets :

    0x18029E6D7  mov  edx, 5
    0x18029E6E0  call sprintf_s(buf, 5, "%d.%02d", major, minor)

« 1.00 » tient. « 48.00 » demande six octets avec le NUL : `sprintf_s` rend
`-2` (`ERANGE`) et la CRT tue le processus par `_invalid_parameter`
(`0x180303B20` → `__fastfail` en `0x180303B38`, code `0xC0000409`). **Le majeur
doit donc tenir en un seul chiffre** — c'est un défaut de SEGA, jamais visible
avec de vraies valeurs, mais il nous borne. `tools/gen_apm_stub.py` le garde
par une assertion.

### 11.4 Où en est le réseau, mesuré le 2026-09-06

Correction portée : `System_getGameVersion` rend un pointeur vers
`{ 1u, 0u }`. Résultat de `tools\pister_link.cmd`, 45 s :

| point | passages | lecture |
|---|---|---|
| `_invalid_param` | **0** | plus de plantage |
| `versionGS` | 1 | `major=1 minor=0 -> "1.00"` |
| `ImplSetup` | 1 | les cinq paramètres arrivent entiers |
| `okGameId` / `okKeychipId` / `okMainId` / `okCountry` | 1 chacun | **les quatre validations passent** |
| `SetupLink` | **1** | une seule tentative : elle a **réussi** (elle était retentée à chaque trame tant qu'elle échouait) |
| `tic Setup` | 20 661 | la machine tourne dans son fil dédié |
| `tic Unavailable` | **0** | elle n'a **pas** abandonné |

Les paramètres reçus par `ImplLink::setup`, relus en mémoire :

    serverURI    taille=21    http://127.0.0.1:8080
    gameId       taille=4     0000
    countryCode  taille=3     JPN
    keychipId    taille=11    A69E01A8888
    mainId       taille=11    AAVE01A8888

**Il n'y a plus aucun maillon manquant côté jeu.** La machine reste dans
`Setup` parce que personne ne répond sur `127.0.0.1:8080` et `:8081`. Le
prochain travail est le serveur minimal du §10, et non plus le binaire.


---

## 12. `/api/match` : les deux sens, lus (2026-09-06)

### 12.1 D'abord, une fausse piste corrigée

Le §10.5 désignait `0x1802F6370` et `0x1802F6F40` comme « deux décodeurs à
lire » pour `/api/match`. Ce sont en réalité des **encodeurs**, et ils servent
les deux journaux de télémétrie. Leurs littéraux le disent sans ambiguïté :
chacun se termine par la clé qui nomme son propre point d'entrée.

| fonction | appelée depuis | corps produit |
|---|---|---|
| `0x1802F6370` | `0x1802FA050` | `/api/log/match_summary` |
| `0x1802F6F40` | `0x1802E2280` = `LinkMainStatePlaying::tic` | `/api/log/match_path_quality` |

Le motif d'écriture, répété champ par champ :

    mov  dword ptr [rsp+0x38], <type>     ; 2 = nombre, 3 = chaine, 4 = tableau, 5 = objet
    <la valeur dans [rsp+0x40]>           ; un double pour les nombres
    lea  rax, <litteral de la cle>        ; -> [rsp+0x48]
    call 0x180221C40                      ; fabrique le noeud
    call 0x1802D4F50                      ; localise le membre par son nom
    call 0x18021DE40                      ; l'affecte

Les nombres passent par `_finite` (`0x18030C744`) avant d'être posés ; un
non-fini fait échouer tout l'encodage.

**`match_summary` :**

    {"match_summary":{
       "match_id":<nombre>,
       "ip":"<chaine>", "port":<nombre>,
       "match_started":"<chaine>", "match_connected":"<chaine>",
       "match_finished":"<chaine>",
       "player_num":<nombre>,
       "path_types":[ {"ip":"<chaine>","port":<nombre>,"type":<nombre>}, ... ]
    }}

**`match_path_quality` :**

    {"match_path_quality":{
       "match_id":<nombre>,
       "ip":"<chaine>", "port":<nombre>,
       "path_qualities":[ {"ip":"<chaine>","port":<nombre>,"type":<nombre>,
                           "rtt":<nombre>,"loss":<nombre>}, ... ]
    }}

À noter : **`match_id` est un NOMBRE**, malgré son nom, et les trois horodatages
sont des **chaînes**.

### 12.2 Le vrai `/api/match`

Le point d'entrée est enveloppé par `0x1802D5ED0`, appelé depuis `0x1802DC780`
et `0x1802DDE30`. Les dix-huit littéraux du §5.2 se répartissent **proprement
entre deux fonctions**, et c'est ce partage qui départage le sens de
circulation — aucune clé n'apparaît dans les deux.

| fonction | rôle | motif |
|---|---|---|
| **`0x1802F8CD0`** | **encodeur de la requête** | une occurrence par clé, précédée d'un tag de type |
| **`0x1802F7DF0`** | **décodeur de la réponse** | deux occurrences par clé : la recherche, puis le `cmp` de type |

**Ce que le jeu ENVOIE** (`0x1802F8CD0`) :

| clé | type |
|---|---|
| `user_id` | nombre |
| `req_id` | chaîne |
| `route` | chaîne |
| `country` | chaîne |
| `rating` | nombre |
| `rating_min` / `rating_max` | nombre |
| `member_min` / `member_max` | nombre |
| `scope` | nombre |
| `nat_mtype` / `nat_ftype` | nombre |
| `title_key1` … `title_key6` | chaîne — **six clés numérotées**, voir §12.5 |
| `param1_list` … `param3_list` | nombre — **trois**, voir §12.5 |
| `param1_type` … `param3_type` | tableau — **trois**, voir §12.5 |
| `condition_change` | nombre |
| `match` | **objet** — l'enveloppe qui contient tout ce qui précède |

**Ce que le jeu ATTEND** (`0x1802F7DF0`), avec le type exigé et l'adresse du
contrôle :

| clé | type attendu | contrôle |
|---|---|---|
| `status` | **nombre** | `0x1802F7F0A` |
| `req_id` | **chaîne** | `0x1802F8022` |
| `match` | **objet** | `0x1802F8157` |
| `route` | **chaîne** | `0x1802F8780` |
| `ready` | **nombre** | `0x1802F8930` |

`key`, `num` et `members` sont lues dans la partie imbriquée (sous `match`,
puis dans la boucle sur `members`) ; leur type n'est pas encore relevé.

**Deux clés que le §5.2 n'avait pas vues** apparaissent ici : `user_id` et
`rating` côté requête, `ready` côté réponse. Et **`ready` n'est pas dans le
bloc de littéraux du §5.2** : l'énumération de ce paragraphe n'était donc pas
exhaustive — elle listait un bloc contigu, pas l'ensemble des clés du chemin.

### 12.3 `_list` et `_type` sont bien des suffixes — vérifié

Le §10.4 le supposait sans le vérifier. C'est **une concaténation**, et elle
emploie exactement la même fonction que la construction des URL
(`0x18008BB50`, celle qui colle `baseURL + "/api/match"`) :

    0x1802F98CB  lea  r8, "_list"          ; le suffixe
    0x1802F98D2  lea  rdx, [rbp + 0x40]    ; le prefixe, une std::string
    0x1802F98D6  lea  rcx, [rbp + 0x60]    ; le resultat
    0x1802F98DA  call 0x18008BB50          ; concatenation

La clé émise est donc `<prefixe>_list`, et de même `<prefixe>_type` en
`0x1802F9AD2`. **Le préfixe est lu au §12.5.**

### 12.4 Ce qui reste ouvert sur ce chemin

- **Le type de `key`, `num`, `members`** dans le décodeur.
- **Ce que valent les champs** des trois enregistrements de `r13+0x140` et des
  six chaînes de `title_key<n>` — les clés sont nommées, les valeurs non.
- **L'imbrication exacte de la réponse** : `match` est un objet, `members` une
  liste — mais l'arbre complet n'est pas dessiné.
- Rien de tout ceci n'a été **capturé à l'exécution** : c'est de la lecture de
  code. Le jeu n'atteint pas encore `/api/match`, faute de serveur.


### 12.5 Le préfixe : `param` et un indice à partir de 1

Ce ne sont pas des clés à préfixe variable : ce sont des clés **numérotées**,
fabriquées par une conversion entière suivie d'une insertion en tête.

La conversion, c'est la division par 10 par multiplication magique
(`0xCCCCCCCCCCCCCCCD`), les chiffres écrits à rebours dans un tampon de pile
qui finit en `[rbp+0xC5]` :

    0x1802F9670  dec  r9                     ; on recule d'un chiffre
    0x1802F9673  mov  rax, rsi               ; rsi = 0xCCCC...CD
    0x1802F9676  mul  r8
    0x1802F9679  shr  rdx, 3                 ; rdx = r8 / 10
    ...
    0x1802F968B  add  r8b, 0x30              ; le reste, en ASCII
    0x1802F968F  mov  byte ptr [r9], r8b
    0x1802F9698  jne  0x1802F9670

Puis le littéral est inséré **devant** les chiffres (`insert(0, ...)` de MSVC,
avec son recouvrement en trois `memcpy`) :

    0x1802F969A  lea  rsi, "param"           ; 0x1803FA0EC
    0x1802F96E4  lea  r10, 0x1803FA0F1       ; "param" + 5, la borne
    0x1802F973D  call memcpy                 ; on décale les chiffres de 5
    0x1802F974B  call memcpy                 ; on pose "param" devant

**Les deux boucles, et leurs bornes lues au désassembleur :**

| boucle | indice | pas / borne | clés émises |
|---|---|---|---|
| `0x1802F931F`…`0x1802F9630` | `r14`, `inc` **avant** usage → **part à 1** | `rsi += 0x20`, `cmp rsi, 0xC0` → **6 tours** | **`title_key1` … `title_key6`** |
| `0x1802F963C`…`0x1802F9BAC` | `r15`, `inc` **avant** usage → **part à 1** | `r14 += 0x28`, `cmp r14, 0x78` → **3 tours** | **`param1` … `param3`**, chacun en `_list` et `_type` |

Le pas de la première boucle est `0x20` : c'est un tableau de **six
`std::string`**. Celui de la seconde est `0x28` : **trois enregistrements de
40 octets**, à partir de `r13+0x140`, dont le premier dword fournit la valeur
de `param<n>_list` (`0x1802F981D : movd xmm6, dword ptr [r14 + rsi]`).

**La requête `/api/match` porte donc, en tout, six clés `param` :**

    "param1_list":<nombre>, "param1_type":[...],
    "param2_list":<nombre>, "param2_type":[...],
    "param3_list":<nombre>, "param3_type":[...]

et six `title_key<n>`. Aucune des deux n'est la clé simple `title_key` que le
§5.2 avait relevée : ce paragraphe listait le **littéral**, pas la clé émise.


---

## 13. Le transport HTTP, lu (2026-09-06)

### 13.1 C'est POST, et libcurl est configuré en clair

`am::abaas::link::Request::sendData` (`0x1802EBAC0`) finit par
« post request data » (`0x180292620` → `0x1802922B0`), et là les options
libcurl sont posées une par une par `curl_easy_setopt` (`0x180294C90`), après
un `curl_easy_init` (`0x180294C40`) :

| site | option | valeur |
|---|---|---|
| `0x18029238B` | `0x2727` = **CURLOPT_HTTPHEADER** | la `slist` de `[rsi+0x58]` |
| `0x1802923A6` | `0x2722` = **CURLOPT_USERAGENT** | `[rsi+0x38]` |
| `0x1802923C2` | `0x2712` = **CURLOPT_URL** | l'URL construite par l'appelant |
| `0x1802923D6` | `0x4E` = **CURLOPT_CONNECTTIMEOUT** | `[rsi+0xA0]` |
| `0x1802923E5` | `0x0D` = **CURLOPT_TIMEOUT** | `0` (aucun) |
| `0x1802923F8` | `0x13` = **CURLOPT_LOW_SPEED_LIMIT** | `0x400` (1 ko/s) |
| `0x18029240C` | `0x14` = **CURLOPT_LOW_SPEED_TIME** | `[rsi+0xA0]` |
| `0x18029241D` | `0x4B` = **CURLOPT_FORBID_REUSE** | `1` |
| **`0x18029242E`** | **`0x2F` = CURLOPT_POST** | **`1`** |
| `0x18029243E` | `0x271F` = **CURLOPT_POSTFIELDS** | le corps chiffré |
| `0x180292453` | `0x3C` = **CURLOPT_POSTFIELDSIZE** | sa longueur |
| `0x180292467` | `0x4E2B` = **CURLOPT_WRITEFUNCTION** | `0x180292590` |
| `0x180292477` | `0x2711` = **CURLOPT_WRITEDATA** | le tampon de réponse |
| `0x180292497` | `0x75C2` = **MAX_RECV_SPEED_LARGE** | `[rsi+0xA4] << 10`, si non nul |
| `0x1802924A7` | `0x75C1` = **MAX_SEND_SPEED_LARGE** | idem |

Puis `curl_multi_add_handle` (`0x180295370`). **Aucun `CURLOPT_CUSTOMREQUEST`,
aucun `CURLOPT_HTTPGET`** : toutes les requêtes sont des POST.

L'unique en-tête ajouté est le type MIME, posé par `0x180292660` (message
d'erreur « Error: failed to set content type. ») via `curl_slist_append`
(`0x180294E80`) : **`Content-Type: application/octet-stream`**, pour les deux
bibliothèques (`0x1802EC2C1` pour `abaaslink`, `0x1802B6289` pour `abaasgs`).

### 13.2 L'enveloppe commune injectée dans chaque corps

`Request::sendData` ne prend pas le JSON de l'appelant tel quel : il **recoud**
un bloc commun juste avant l'accolade fermante.

    0x1802EBB60  si le corps de l'appelant est vide -> "{}"
    0x1802EBBB2  recherche du DERNIER '}' (0x7D), à rebours
    0x1802EBCD7  insertion d'une ',' à cette position
    0x1802EBD62  insertion du bloc commun juste après

Le bloc commun est fabriqué par `0x1802EA760`, littéral par littéral, dans cet
ordre (`0x1805C3530` et suivants) :

    "client":{"serial":"<keychipId>","game_id":"<gameId>",
              "game_ver":"<major>.<minor>","location_id":<nombre>,
              "create_time":"<horodatage>"}

Donc le corps réellement posté vaut, avant chiffrement :

    { <le corps propre à la route> , "client":{ ... } }

et pour une route sans corps propre, simplement `{"client":{...}}`.

**Conséquence pour le serveur minimal** : il reçoit toujours au moins le bloc
`client`, et peut s'en servir pour identifier la borne — `serial` et `game_id`
sont ceux que **notre** `apm.dll` fournit.

### 13.3 Les deux familles de routes

Le tableau de six chemins de `abaaslink` est en `0x1806613C0`, chacun avec son
enveloppe et son numéro de créneau (le `dl` de `0x1802D57C0`) :

| créneau | chemin | fonction qui la construit |
|---:|---|---|
| 0 | `/api/alive` | `0x1802D5610` |
| 1 | `/api/turninfo` | `0x1802D5C50` |
| 2 | `/api/match` | `0x1802D5ED0` |
| 3 | `/api/config` | `0x1802D5B00` |
| 4 | `/api/log/match_summary` | `0x1802D5E20` |
| 5 | `/api/log/match_path_quality` | `0x1802D5D70` |

L'URL est `baseURL + chemin`, concaténée par `0x18008BB50` à partir de
`[this+0x4D0]`. Le serveur de titre (`abaasgs`) a sa propre famille, en
`0x1805BE128` : `/api/user/load`, `/api/user/save`, `/api/user/heartbeat`,
`/api/ranking/*`, `/api/data/*`, `/api/server/alive`, `/api/log/upload`,
`/api/code/*`.


---

## 14. Le serveur minimal tourne (2026-09-06)

`tools/serveur_allnet.py`, lanceur `tools/serveur_allnet.cmd`. Il ne devine
rien : il répond au minimum et **journalise tout** dans
`analysis/serveur_allnet.txt`.

### 14.1 Le mur qui n'était pas où on croyait : l'URL était de notre main

Première tentative : le serveur écoutait sur 8080/8081, la sonde montrait
**37 POST émis**… et **zéro reçu**. Un point d'arrêt juste avant
`curl_easy_setopt(CURLOPT_URL)` (`0x1802923BA`, `r8` porte l'URL) a tranché :

    URL donnee a libcurl : b'http://http://127.0.0.1:8080:80/api/turninfo'

**Le moteur construit l'URL lui-même**, en collant trois morceaux dont deux
littéraux voisins de la table des chemins :

    "http://" (0x1805BE118) + <nom d'hote> + ":80" (0x1805BE120) + <chemin>

Les deux `*ServerName` doivent donc rendre un **nom d'hôte nu**, et le port est
**câblé à 80** pour les deux bibliothèques. Elles partagent donc un seul
serveur et se distinguent par leurs chemins, qui sont disjoints.
`tools/gen_apm_stub.py` rend désormais `"127.0.0.1"`.

*(Le binaire n'a pas été touché : le port 80 était libre. Au besoin, `":80"`
dispose de huit octets — `":8080"` y tiendrait.)*

### 14.2 La recette du §6.7 est validée de bout en bout

Première requête reçue, déchiffrée et lue :

    [link] POST /api/turninfo   128 octets
    en-tete : 01010100 30303030 0a72c129 99d42b3a
    version 1.00   gameId b'0000'
    JSON : {"client":{"serial":"A69E01A8888","game_id":"0000",
                      "game_ver":"1.00","location_id":0,
                      "create_time":"20260906134850"}}

L'en-tête se lit exactement comme le §6.7 l'annonçait — `01 01` puis
major/minor, puis le `gameId`, puis le CRC-32 (il **concorde** : aucune alerte
n'a été levée), puis quatre octets aléatoires. Et l'enveloppe `client` du
§13.2, lue statiquement, est confirmée mot pour mot.

### 14.3 Le serveur de titre se déchiffre aussi

    [gs] POST /api/data/load   160 octets
    JSON : {"free_buckets":{"keys":["misc_*","rule_*","matching_*"]},
            "client":{...}}

C'est la **preuve** que `cle_GS = titleKey XOR constante` est juste : un
déchiffrement AES-256-CBC qui rend du zlib valide dont le CRC concorde ne se
produit pas par hasard. Le §6.8 est clos.

Et `/api/data/load` nomme au passage trois seaux de données que le jeu
réclame : `misc_*`, `rule_*`, `matching_*`.

### 14.4 Le mur suivant : il n'y a pas de STUN

Après ces deux échanges, **le jeu se tait**. C'est cohérent avec le §10.5 :
il mesure son type de NAT par STUN (`requestCheckNatType`, `0x1805C9550`)
**avant** d'appeler `/api/match`. Notre réponse à `turninfo` l'envoie sur
`127.0.0.1:3478`, où rien n'écoute.

Le prochain geste est donc un **coturn** (ou un répondeur STUN minimal) sur
3478, avec l'utilisateur `vf5` / `vf5` que notre `turninfo` annonce. Le
protocole est du STUN/TURN standard, magic cookie `0x2112A442` : rien à
ré-inventer.
