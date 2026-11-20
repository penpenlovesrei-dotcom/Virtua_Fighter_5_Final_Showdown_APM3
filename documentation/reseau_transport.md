# Le transport réseau et le format des paquets — build APM3

Relevé statique du 2026-09-05, sur
`runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll.origine`
(PE MSVC x64, base `0x180000000`, `.text` = `0x180001000`, vsize `0x34475C`).

Question posée : **qu'est-ce que ce jeu met sur le fil, et à qui parle-t-il ?**

Ce document est écrit **au fil de l'eau**. Les sections marquées « en cours »
ne sont pas closes.

---

## 0. En un mot

(à remplir en dernier)

---

## 1. Le magic cookie STUN `0x2112A442` — PRÉSENT

`py -3 tools/reseau.py const 0x2112A442` — **sept occurrences**, toutes en
**immédiat d'instruction dans `.text`**, aucune en donnée :

    LE  off=0x002EC535  va=0x1802ED135  .text
    LE  off=0x002ED03D  va=0x1802EDC3D  .text
    LE  off=0x002ED39D  va=0x1802EDF9D  .text
    LE  off=0x002ED83A  va=0x1802EE43A  .text
    LE  off=0x002EDC90  va=0x1802EE890  .text
    LE  off=0x002F0028  va=0x1802F0C28  .text
    LE  off=0x002F1B42  va=0x1802F1B42  .text

Écrit en **petit-boutiste** dans l'immédiat : c'est la valeur telle qu'elle
sort d'un `htonl` (ou telle qu'elle est comparée après `ntohl`). Sept sites,
c'est la signature d'un codec : quelques-uns écrivent le cookie, les autres le
vérifient.

**Conclusion : SEGA n'a pas dévié.** L'en-tête est celui de la RFC 5389.

## 2. Les classes du sous-système, relevées par RTTI

`py -3 tools/rtti.py --grep "Packet|Stun|Turn|Link|Hmac|Crypt"`.

Le namespace est **`am::abaas`** (« ABAAS » — le nom du middleware réseau de
SEGA ; c'est le même préfixe que celui du service ALL.Net d'appariement).

**Le transport**

    am::abaas::LinkSend                    vtable 0x1805C9198
    am::abaas::LinkSend::Impl              vtable 0x1805C91B8
    am::abaas::LinkSend::VImpl::CommThreadBase       0x1805C91A8
    am::abaas::LinkReceiveThread           vtable 0x1805C9308
    am::abaas::LinkReceiveThread::Impl     vtable 0x1805C9338
    am::abaas::LinkReceiveThread::VImpl::CommThreadBase 0x1805C9318
    am::abaas::std::VReceivePacket::shared_ptr::Fifo    0x1805C9328

**Les paquets et leurs attributs (AttributeHolder, un par type de paquet)**

    PacketBase                             0x1805C7C80
    PacketBase::Attribute::AttributeBase   0x1805C6D30
    SendPacket    0x1805C6D50      ReceivePacket   0x1805CBB90

**Les séquenceurs TURN** (nouveaux, non relevés jusqu'ici)

    TurnSequencer                  0x1805C8030
    TurnAllocateSequencer          0x1805CA7E0
    TurnAllocateRequestSuite       0x1805CA730
    TurnAllocateResponseSuite      0x1805CA788
    TurnRefreshSequencer           0x1805CAB98
    TurnRefreshRequestSuite        0x1805CAAE8
    TurnRefreshResponseSuite       0x1805CAB40
    TurnChannelBindSequencer       0x1805CAF98
    TurnChannelBindRequestSuite    0x1805CAEE8
    TurnChannelBindResponseSuite   0x1805CAF40
    TurnContext                    0x1805C7E60
    TurnWaiter                     0x1805CC578

**Le codec bas niveau**

    am::abaas::raw_packet::UStunAttributeHeader   (structure, vue par ses lambdas)
    am::abaas::raw_packet::W4LinkMethod           (énumération des méthodes)

Huit `_Func_impl_no_alloc` de lambdas paramétrées par
`raw_packet::UStunAttributeHeader` et `raw_packet::W4LinkMethod` :
`0x1805CB6B0 0x1805CB6E8 0x1805CB758 0x1805CB720` (attributs) et
`0x1805CB790 0x1805CB838 0x1805CB7C8 0x1805CB800` (méthodes) ;
plus quatre autres en `XAEAU` : `0x1805CBCF8 0x1805CBC88 0x1805CBD30
0x1805CBCC0`. Ce sont les tables de conversion nom<->code du protocole.

**HTTP côté appariement** (laissé à l'autre agent)

    am::abaas::link::HttpData      0x1805CC6E8
    am::abaas::link::Request       0x1805CB3B0
    am::abaas::link::Task          0x1805C90E8

**La cryptographie — la piste de la clé HMAC**

    util::crypt::Aes               vtable 0x1805C5290
    util::crypt::Aes::CryptKey     vtable 0x1805C52A0
    util::rand::Bcrypt             vtable 0x1805C7CE8

`util::rand::Bcrypt` : générateur d'aléa adossé à CNG (BCrypt* de Windows) —
c'est très probablement ce qui fabrique les **identifiants de transaction 96
bits** de STUN. `util::crypt::Aes` + `CryptKey` : une clé existe et se
*chiffre*, ce qui plaide contre un littéral en clair. **À vérifier.**

---

## 3. LA CLÉ HMAC — ÉTABLIE

**Elle n'est pas dans le binaire. Elle est calculée, et ses ingrédients viennent
du serveur d'appariement par HTTP.**

C'est le mécanisme de **crédential à long terme de la RFC 5389, §15.4**, à la
lettre :

    clé = MD5( username ":" realm ":" password )

### La chaîne, maillon par maillon

**a. Le hacheur générique** — `util::hash::Calcurator::CNG`

Constructeur `0x1802E3A30(this, algo, hmac)`. L'objet fait `0x98` octets :

    +0x00  vtable 0x1805CA280
    +0x40  pointeur sur le nom d'algorithme (chaîne large)
    +0x48  longueur du condensat
    +0x50  drapeau HMAC (bool)
    +0x51  64 octets remis à zéro (tampon de travail)

Le sélecteur d'algorithme, à `0x1802E3B31`, est un `switch` sur quatre
soustractions successives :

    algo=0 -> L"MD5"    (0x1805CA288)  longueur 0x10
    algo=1 -> L"SHA1"   (0x1805CA290)  longueur 0x14
    algo=2 -> L"SHA256" (0x1805CA2A0)  longueur 0x20
    algo=3 -> L"SHA384" (0x1805CA2B0)  longueur 0x30
    sinon  -> L"SHA512" (0x1805CA2C0)  longueur 0x40

**b. `util::hash::Calcurator::CNG::init(this, pbKey, cbKey)`** — `0x1802E3E60`
(entrée pratique par le thunk `0x1802E4030`, qui déréférence `this+0x18`).

C'est ici que se prouve le HMAC. À `0x1802E3F11` :

    0x1802E3F11  mov  rdx, qword ptr [rbx + 0x40]   ; nom de l'algorithme
    0x1802E3F15  lea  rcx, [rbx + 0x18]             ; &hAlgorithm
    0x1802E3F19  neg  al                            ; al = drapeau HMAC (+0x50)
    0x1802E3F1B  sbb  r9d, r9d                      ; r9d = -1 si drapeau, 0 sinon
    0x1802E3F1E  xor  r8d, r8d
    0x1802E3F21  and  r9d, 8                        ; r9d = 8 si drapeau
    0x1802E3F25  call 0x1803310D1                   ; BCryptOpenAlgorithmProvider

`8` est **`BCRYPT_ALG_HANDLE_HMAC_FLAG`**. Puis à `0x1802E3FD3`,
`BCryptCreateHash(hAlg, &hHash, pbHashObject, cb, pbSecret=r15, cbSecret=ebp,
0)` — `r15`/`ebp` sont les deux arguments `pbKey`/`cbKey` de `init`. La clé
entre bien par `pbSecret`.

**c. Le site qui fixe HMAC-SHA1 et la longueur de clé 16** — `0x1802EE1C1`,
dans la fonction `0x1802EDB30` (le sérialiseur de paquet) :

    0x1802EE1A3  lea  rdx, [rbp - 0x20]     ; tampon de 16 octets sur la pile
    0x1802EE1A7  mov  rcx, qword ptr [r14]  ; le paquet
    0x1802EE1AA  call 0x1802EC8B0           ; y récupère la clé
    ...
    0x1802EE1C1  mov  r8b, 1                ; hmac = VRAI
    0x1802EE1C4  lea  edx, [rax + 1]        ; rax=0 -> algo = 1 = SHA1
    0x1802EE1CB  call 0x1802E3A30           ; CNG(SHA1, HMAC)
    0x1802EE1D1  mov  r8d, 0x10             ; cbKey = 16
    0x1802EE1D7  lea  rdx, [rbp - 0x20]
    0x1802EE1DF  call 0x1802E4030           ; init(clé, 16)

**HMAC-SHA1, clé de 16 octets : la note de la session précédente est
confirmée.** (Deux autres sites du même sérialiseur font le même geste :
`0x1802EE62D` et `0x1802EEABC`.)

**d. D'où sort le tampon de 16 octets** — `0x1802EC8B0`

Cette fonction parcourt le vecteur d'attributs du paquet (`[rcx+0x40]` à
`[rcx+0x48]`), compare le nom de type de chaque attribut à

    0x180669E00 : ".?AULinkPacketAttrHMAC@abaas@am@@"

et, sur concordance, recopie **16 octets pris à `attribut+8`** :

    0x1802EC939  movups xmm0, xmmword ptr [rax + 8]
    0x1802EC93D  movups xmmword ptr [rdi], xmm0

Donc `ULinkPacketAttrHMAC` n'est pas un attribut qui porte le condensat : c'est
un attribut qui **porte la clé** (24 octets en tout : vptr + 16). Le
sérialiseur la lit, calcule le HMAC-SHA1 sur le paquet, et émet
MESSAGE-INTEGRITY.

**e. Qui remplit ces 16 octets** — les trois constructeurs de requête TURN

Références à la vtable `AttributeHolder<ULinkPacketAttrHMAC>` `0x1805CA9D8` :

    0x1802E5728  dans 0x1802E5410   TurnAllocateRequestSuite   creneau [3]
    0x1802E6EE8  dans 0x1802E6BD0   TurnRefreshRequestSuite    creneau [3]
    0x1802E91EC  dans 0x1802E8E00   TurnChannelBindRequestSuite creneau [3]

Le geste, identique aux trois (ici `TurnAllocateRequestSuite`) :

    0x1802E5700  lea  rdx, [rbp + 0x2b0]
    0x1802E5707  mov  rcx, qword ptr [rdi + 0x28]   ; le TurnContext
    0x1802E570B  call 0x1802CB8C0                   ; <- fabrique la clé
    0x1802E5710  mov  ecx, 0x18                     ; new de 24 octets
    ...
    0x1802E5727  lea  rax, [rip + 0x2e52aa]         ; -> 0x1805CA9D8
    0x1802E572E  mov  qword ptr [rcx], rax
    0x1802E5731  movups xmm0, xmmword ptr [rbp + 0x2b0]
    0x1802E5738  movups xmmword ptr [rcx + 8], xmm0 ; les 16 octets

**f. La fabrication elle-même** — `0x1802CB8C0`, méthode de `TurnContext`

    ostringstream oss;                         // 0xE8 octets, [rsp+0x70]
    oss << this->str_0x20;                     // 0x1802CB923
    oss << ":";                                // literal 0x1803FFAE4 = ":"
    oss << this->str_0x60;                     // 0x1802CB93F
    oss << ":";
    oss << this->str_0x40;                     // 0x1802CB96B
    std::string s = oss.str();
    CNG h(algo = 0 /* MD5 */, hmac = false);   // 0x1802CBA27 : xor edx,edx ; xor r8d,r8d
    h.init(nullptr, 0);                        // 0x1802CBA41
    h.execute(s.data(), s.size());             // 0x1802CBA61 -> 0x1802E3D70
    n   = h.getResultSize();                   // 0x1802E3DE0
    ptr = h.getResult();                       // 0x1802E3DF0
    if (n <= 0x10) memcpy(out, ptr, n);        // 0x1802CBAA7

Le littéral `0x1803FFAE4` vaut bien `":"` (octets `3A 00`).

**C'est mot pour mot la formule de la RFC 5389 §15.4.** Les trois champs de
`TurnContext` sont donc, dans l'ordre de concaténation :

    +0x20  username
    +0x60  realm
    +0x40  password

MD5 rend 16 octets — la « clé de 16 octets » n'est pas un choix de SEGA, c'est
la taille d'un condensat MD5.

### Ce que cela décide

**Un coturn ordinaire suffit**, et sans la moindre modification : le jeu
authentifie ses requêtes TURN par le mécanisme standard à long terme.
Il faut simplement que le serveur d'appariement lui **serve** un triplet
`username` / `realm` / `password` que le coturn accepte (`lt-cred-mech`, avec
le même realm et le même mot de passe).

Les identifiants **ne sont pas dans le binaire** : `LinkMainStateSetup`
les demande par HTTP à `/api/turninfo` (voir la section suivante). C'est donc
notre bouchon d'ALL.Net qui les fournira — nous les choisissons.

---

## 4. Les URL et les serveurs — à qui le jeu parle

Chaînes de `abaaslink` (offsets fichier) :

    0x5C79E8  /api/alive
    0x5C79F8  /api/turninfo
    0x5C7A08  /api/match
    0x5C7A18  /api/config
    0x5C7A28  /api/log/match_summary
    0x5C7A40  /api/log/match_path_quality

**Aucun nom d'hôte, aucun port, aucun `.sega` en dur.** L'URL de base est un
paramètre de configuration : `LinkMain::ImplLink::setup` refuse avec
`Error: server URI is empty` (0x5C5C90) si elle manque, et vérifie aussi
`game id`, `majorVersion`, `minorVersion`, **`keychip id`**, `main id`,
`server timeout`, `country code`.

Champs JSON de `/api/match` : `req_id route country rating_min rating_max
member_min member_max scope nat_mtype nat_ftype title_key _list _type
condition_change status key num members`.
De `/api/config` : `polling log_server_host log_server_port host port`.
Des journaux : `match_id match_started match_connected match_finished
player_num path_types match_summary rtt loss path_qualities
match_path_quality`.

`am::abaas::link::HttpData` a `compress` / `encrypt` / `decrypt` et
`setParam` calcule un condensat (`ERROR: hash init/execute/getResult`) ;
`util::crypt::Aes` + `Aes::CryptKey::setKey` avec `L"AES"` /
`L"ChainingModeCBC"` (offsets 0x5C3EA8 / 0x5C3ED0) chiffrent le corps HTTP.
**C'est le chantier de l'autre agent** — noté ici seulement parce que c'est par
là qu'arrivent les identifiants TURN.

Deux bibliothèques distinctes, avec leurs bandeaux de version :

    abaasgs   Ver.57fe45a  Build:Dec 11 2019 20:13:29   (0x5BC2E1)
    abaaslink Ver.0f03646  Build:Sep  8 2020 18:06:26   (0x5C4E91)

---

## 5. `ULinkPacketAppData` — DES ENTRÉES, ET RIEN QUE DES ENTRÉES

**Réponse : des entrées de manette. Seize octets de corps utile par envoi,
avec redondance sur dix trames.** Ce n'est pas un état de simulation.

### a. Le plafond dur : 1023 octets

`am::abaas::LinkMain::ImplLink::sendPacket` = **`0x1802C98A0`** (entrée par le
thunk `0x1802C9C90`, qui déréférence `this`). Signature reconstruite :

    int sendPacket(this, uint8_t joueur /*dl*/, const void* data /*r8*/,
                   size_t len /*r9*/)

Ses quatre gardes, à l'entrée :

    0x1802C98DC  cmp  dl, 8                        ; joueur < 8
    0x1802C98E8  cmp  eax, dword ptr [rcx+0x1C00]  ; joueur < nb de membres
    0x1802C98F4  test r8, r8                       ; data != NULL
    0x1802C98FD  cmp  r9, 0x400                    ; len < 0x400
    0x1802C9904  jae  0x1802C9C65                  ; -> retourne -2

**La charge utile applicative est plafonnée à 1023 octets** par appel. Le
conteneur, lui, en accepterait bien plus : `0x1802CB190` (`SendPacket::setData`)
vérifie `1 <= len <= 0xFFFE` avant de redimensionner le vecteur en `this+0x28`
puis d'y recopier. C'est donc `sendPacket` qui borne, délibérément.

### b. Ce que `sendPacket` construit

    pkt = make_shared<SendPacket>()            // 0x68 octets, vtable 0x1805C6D50
    pair = (this + 0x1680) + joueur * 0xB0     // table des pairs, pas de 0xB0
    0x1802C9CB0(pkt, pair)                     // destination
    pkt->setData(data, len)                    // 0x1802CB190 -> memcpy dans pkt+0x28
    chan = *(uint16_t*)(pair + 0x10)
    si chan != 0 :
        new AttributeHolder<ULinkPacketAttrChannelNumber>  // 0x11 octets
            vtable 0x1805C77A8 ; uint16 chan en +8       // 0x1802C99EE
    Bcrypt rng;                                 // 0x1802CB220, BCryptOpenAlgorithmProvider(L"RNG")
    rng.GenRandom(&tid, 12)                     // 0x1802CB310, r8d = 0xC
    new AttributeHolder<ULinkPacketAppData>     // 0x18 octets
        vtable 0x1805C77C8
        +0x08 : 8 octets de tid                 // movsd  0x1802C9BB3
        +0x10 : 4 octets de tid                 // mov    0x1802C9BC0
    pkt->attrs.push_back(...)
    0x1802D7510(this->linkSend /* [this+0x1C8] */, &pkt,
                *(uint16_t*)(this + 0x1C32))    // remise a LinkSend

Donc `ULinkPacketAppData` **porte les 12 octets d'identifiant de transaction**
(96 bits, tirés de `BCryptGenRandom`) — c'est-à-dire le champ d'en-tête STUN
lui-même, rangé comme un attribut, exactement comme `ULinkPacketAttrHMAC` porte
la clé. Le corps applicatif, lui, voyage dans le vecteur `PacketBase+0x28`.

### c. Le seul producteur : la boucle d'entrées

`sendPacket` n'a que **deux** appelants, tous deux dans `cs_session`
(balayage linéaire de tout `.text`, pas `.pdata`) :

    0x18022AA5B   dans 0x18022AA20   cs_session::PacketGate, créneau [1]
    0x18022CC61   dans 0x18022CB80   constructeur de message « type 3 »

Les deux passent **`xor edx, edx`** : joueur 0. En liaison à deux bornes, le
pair est toujours l'indice 0.

`0x18022CB80(const void* corps /*rcx*/, short len /*dx*/)` ajoute un en-tête
applicatif de **16 octets** :

    alloc(len + 0x10)
    [+0x00] u32  identifiant pris dans une table de pas 0x1AC (0x180C3FCB4)
    [+0x04] u32  3                    <- type de message, littéral
    [+0x08] u32  len
    [+0x0C] u32  somme de contrôle    <- 0x18022BC90(buf, len, 0x10)
    [+0x10] memcpy(corps, len)
    sendPacket(link, 0, buf, len + 0x10)

Et son **unique** appelant est `0x1801B1BCF`, dans `0x1801B18B0` :

    0x1801B1B1C  mov  edx, 0x10          ; len = 16
    0x1801B1BCB  lea  rcx, [rbp - 0x19]
    0x1801B1BCF  call 0x18022CB80

**Seize octets.** Total sur le fil, hors STUN/TURN : 16 + 16 = **32 octets**.

### d. Le contenu exact des seize octets

La fonction tient un **tampon circulaire de 1024 enregistrements de 8 octets**
en `rdi`, indexé par le numéro de trame masqué (`and r8d, 0x800003FF`, avec le
correctif de modulo négatif) et rebouclé par `mov r14d, 0x3FF ; cmovs r8d, r14d` :

    0x1801B1ACA  mov word  ptr [rdi + rax*8 + 4], r10w   ; le mot d'entrees, 16 bits
    0x1801B1AD0  mov dword ptr [rdi + rax*8], edx        ; le numero de trame

`r10w` est bien un masque de boutons : les instructions `0x1801B1A60`
à `0x1801B1A88` y insèrent des bits un par un (`or dx, 0x40`, `or r10w, 8`,
`or cx, r8w`…) selon les bits d'un octet source décalé (`shr al, 5`, `shr al, 6`,
`shr r9b, 2` puis `and al, 1`).

L'envoi est **cadencé**, pas fait à chaque trame :

    0x1801B1AD3  mov  r9d, dword ptr [rbx + 0xA8]   ; numero de trame
    0x1801B1ADE  idiv dword ptr [rbx + 0xDC]        ; intervalle d'envoi
    0x1801B1AE4  test edx, edx
    0x1801B1AE6  jne  0x1801B1BDB                   ; on n'envoie pas cette trame

Le corps assemblé, octet par octet :

    [rbp-0x19] u32  numero de trame          (r9d = [rbx+0xA8])   4 octets
    [rbp-0x15] u16  champ compacte           ((x & 0x1F) << 3) | ([rbx+0x60] & 7)
    [rbp-0x13] u8   entree de la trame en cours   (r10b, octet bas du masque)
    [rbp-0x12] u8   entree de la trame  -1
    [rbp-0x11] u8                       -2
    [rbp-0x10] u8                       -3
    [rbp-0x0F] u8                       -4
    [rbp-0x0E] u8                       -5
    [rbp-0x0D] u8                       -6
    [rbp-0x0C] u8                       -7
    [rbp-0x0B] u8                       -8
    [rbp-0x0A] u8                       -9
                                              = 4 + 2 + 1 + 9 = 16 octets

Les neuf octets de queue sont lus **à rebours** dans le tampon circulaire, par
le motif répété neuf fois

    movzx ecx, byte ptr [rdi + rax*8 + 4]   ; octet bas du mot d'entrees
    sub   r8d, 1
    cmovs r8d, r14d                          ; rebouclage sur 0x3FF
    movsxd rax, r8d

**C'est de la redondance d'entrées** : chaque datagramme réémet les neuf
entrées précédentes, pour qu'une perte n'oblige pas à retransmettre. C'est la
signature d'un netcode **à retard sur UDP**, pas d'un rollback et encore moins
d'un envoi d'état.

### e. Ce que cela fixe

- **Débit** : 32 octets applicatifs, plus l'en-tête STUN de 20 octets, plus les
  attributs, plus TURN/UDP/IP. On reste très en dessous de la centaine
  d'octets par envoi, et l'envoi n'est même pas par trame.
- **Latence tolérable** : la redondance couvre 9 trames, soit **150 ms à 60 Hz**.
  C'est la fenêtre de perte que le protocole absorbe sans rien redemander ;
  au-delà, il manque une entrée.
- **Un état de simulation est exclu** : il ne tiendrait pas dans 1023 octets, et
  la structure envoyée est une pile d'entrées passées, pas un instantané.

---

## 6. Les sockets — `am::abaas::Udp`

**Correction au relevé précédent** : le moteur importe **vingt-sept** fonctions
de `ws2_32`, pas quatorze. Aux quatorze déjà connues s'ajoutent `WSAStartup`,
`WSACleanup`, `WSAGetLastError`, `WSASetLastError`, `select`, `__WSAFDIsSet`,
`bind`, `closesocket`, `getaddrinfo`, `freeaddrinfo`, `inet_pton`, `htons`,
`recv`, `send`.

Le balayage linéaire (`py -3 tools/reseau.py appels ws2_32`) sépare nettement
**trois** familles de clients :

| plage | client | rôle |
|---|---|---|
| `0x18029xxxx`, `0x1802A7xxx`, `0x1802A8xxx` | libcurl embarqué | HTTP ALL.Net (TCP), `select`, `recv`/`send`, `WSAIoctl`, `getsockopt` |
| `0x1802CDB79`, `0x1802CDCC0` | résolution + connexion d'essai | `getaddrinfo` + `socket` + `connect` + `getsockname` : la façon habituelle de **découvrir sa propre adresse locale** sans rien émettre |
| `0x1802E3xxx` | **`am::abaas::Udp`** | le transport de jeu |

### `am::abaas::Udp::open` — `0x1802E3270`

Prend un bloc de configuration (`rdx`) et vérifie, dans cet ordre :

    [cfg+0x00] u16 famille  doit valoir 2 (AF_INET), sinon
                            "Error: Unsupported address family. %u."
    [cfg+0x08] i32 délai de réception, >= 0
    [cfg+0x04] i32 délai d'émission,  >= 0
    [cfg+0x90] i32 longueur d'adresse, > 0
    [cfg+0x02] u8  drapeau de réutilisation d'adresse
    [cfg+0x10]     le `sockaddr` local à lier

Puis :

    0x1802E332A  mov  edx, 2 ; xor r8d, r8d ; mov ecx, edx
    0x1802E3334  call socket           ; socket(AF_INET=2, SOCK_DGRAM=2, 0)

**UDP sur IPv4, un seul socket.** Aucune trace d'IPv6 : la famille 2 est
imposée et toute autre valeur est un refus.

Ensuite, si `[cfg+2]` :

    setsockopt(s, 0xFFFF /*SOL_SOCKET*/, 4 /*SO_REUSEADDR*/, &1, 4)   0x1802E339E
    bind(s, cfg+0x10, cfg->addrlen)                                   0x1802E33D8
    setsockopt(s, 0xFFFF, 0x1005 /*SO_RCVTIMEO*/, &timeval, 8)        0x1802E3450
    setsockopt(s, 0xFFFF, 0x1006 /*SO_SNDTIMEO*/, &timeval, 8)        0x1802E34B7

Les deux délais sont donnés en millisecondes dans la configuration et convertis
en `timeval{sec, usec}` par une division par 1000 (`imul` par `0x10624DD3`,
`sar 6`). *Détail notable : Winsock attend un `DWORD` de millisecondes pour
`SO_RCVTIMEO`, pas un `timeval` BSD — SEGA passe ici huit octets là où Windows
en lit quatre. Sans conséquence pratique, mais c'est un indice que le code vient
d'un portage.*

**Le socket est bloquant, avec des délais** — pas d'E/S superposées, pas
d'`WSAEventSelect` : le fil de réception fait du `select` en boucle serrée.

### `Udp::send` — `0x1802E3690`

    sendto(s, data, len, 0 /* pas de drapeau */, to, tolen)   0x1802E3709

### `Udp::recv` — `0x1802E3540`

    recvfrom(s, buf, *plen, 0, from, fromlen)                 0x1802E35D7

### `Udp::isReadable` — `0x1802E3120`

Monte un `fd_set` complet (FD_SETSIZE, 4 blocs de 128 octets recopiés) puis

    select(s + 1, &readfds, NULL, NULL, &timeval{0, timeout_us})   0x1802E31F5

Le `timeval` est bâti à `0x1802E314C` : `tv_sec = 0`, `tv_usec = edx`
(le paramètre).

### Adresses et ports : rien en dur

Aucun littéral d'adresse ni de port dans le code du transport. L'adresse de
liaison vient du bloc de configuration ; l'adresse du serveur TURN est posée
par `am::abaas::TurnContext::setTurnServerAddress` (message à `0x5C6A90`,
« Error: not set turnServer address. ») à partir de ce que rend
`/api/turninfo`. `inet_pton` n'est appelé qu'une fois, en `0x1802C7B57`
(fonction `0x1802C7A20`) : la conversion d'une adresse **textuelle** reçue en
configuration.

---

## 7. Les deux fils

### `LinkReceiveThread` — corps en `0x1802D8980`

Entrée du fil : `0x1802D8880`, qui appelle la boucle puis signale un événement.

    0x1802D89BD  mov  ecx, 0x10000
    0x1802D89C2  call operator new       ; tampon de réception de 65 536 octets

Boucle :

    0x1802D89E6  WaitForSingleObject(evt = [this+0x18], 0)
                 ; >= 1 (signalé) -> on sort
    0x1802D8A2A  Udp::isReadable(udp, 0x1F4)     ; select, 500 microsecondes
    0x1802D8A3D  cmp ebx, 0x64                   ; jusqu'a 100 tentatives
    0x1802D8A47  Sleep(1)                        ; puis on rend la main
    0x1802D8A52  sockaddr de 0x80 octets, addrlen = 0x80
    0x1802D8A6B  taille de réception = 0x10000
    0x1802D8A91  Udp::recv(...)
    0x1802D8AEC  0x1802F11B0(...)                ; DÉSÉRIALISATION
    0x1802D8B05  new de 0xB0 octets              ; ReceivePacket, vtable 0x1805C82B0

**Cadence : `select` à 500 µs, cent fois de suite (50 ms) avant un `Sleep(1)`.**
C'est une boucle de scrutation serrée, taillée pour la latence, pas pour
l'économie de CPU — cohérent avec une borne d'arcade.

Le tampon de 64 Kio est la borne haute d'un datagramme ; il ne dit rien de la
taille réellement utilisée, que la section 5 chiffre à 32 octets applicatifs.

### `LinkSend` — `LinkSend::Impl::sendAll` en `0x1802D7550`

Appelé depuis `0x1802C9520`, dans la fonction `0x1802C8CC0`, immédiatement
suivi de :

    0x1802C9525  mov  ecx, 1
    0x1802C952A  call Sleep              ; Sleep(1)

**Cadence : une passe d'émission par milliseconde.**

`sendAll` prend un verrou (`EnterCriticalSection` sur `this+0xA8`,
`0x1802D75CB`) puis parcourt la file `[this+0x68]` .. `[this+0x70]` — un
vecteur de `shared_ptr<SendPacket>`. Chaque entrée porte **une échéance** :

    0x1802D75F0  call 0x1802D0850              ; horloge
    0x1802D7603  cmp  qword [rsp+0x80], [r15]  ; maintenant >= échéance ?
    0x1802D760B  jl   suivant                  ; sinon on n'envoie pas

puis

    ebp = [r15+0x20]      ; longueur
    rsi = [r15+8]         ; données
    rcx = [r15+0x10]      ; RemoteAddress
    edi = [rcx+0x98]      ; longueur d'adresse
    0x1802D7623  call 0x1802CE1A0     ; -> sockaddr
    0x1802D763A  call 0x1802E3690     ; Udp::send

**C'est une file à échéances**, pas un simple tampon : le moteur sait
programmer une réémission dans le futur. C'est le mécanisme de retransmission
des requêtes STUN/TURN.

---

## 8. LA SÉRIALISATION — le sérialiseur unique `0x1802EDB30`

**Tout le trafic sortant passe par une seule fonction**, `0x1802EDB30`, appelée
depuis un seul site : `0x1802D7345`, dans `0x1802D7250` (une méthode de
`LinkSend::Impl`, celle qui prépare un `SendPacket` pour la file à échéances de
la §7). Balayage linéaire de tout `.text` : **un seul appelant**.

    int serialiser(shared_ptr<PacketBase>* pkt /*rcx*/,
                   uint8_t*  dst             /*rdx*/,   // tampon de 0x10000
                   uint32_t  capacite        /*r8d*/,   // 0x10000
                   uint32_t* longueur_ecrite /*r9*/,
                   const uint8_t* cle        /*[rsp+0x28]  = LinkSend::Impl+0x80*/,
                   size_t    taille_cle      /*[rsp+0x30]  = [LinkSend::Impl+0xA0]*/,
                   uint32_t  horodatage_ms   /*[rsp+0x38]*/)

Rendus : `0` succès, `-1` incohérence de longueur, `-2` argument invalide
(`dst` nul, `capacite-1 > 0xFFFF`, paquet nul).

Le corps est une **chaîne de neuf `if`** sur le type dynamique du paquet
(`0x1802CB110(pkt, &type_info)` = « ce paquet porte-t-il un attribut de ce
type ? », puis une boucle sur `pkt->attrs` de `+0x40` à `+0x48` qui compare les
noms décorés par `__std_type_info_compare` `0x1803011D4`). Chaque branche
construit **le même en-tête de 20 octets** et **une liste d'en-têtes
d'attributs**, puis appelle un écrivain générique.

### a. Les trois primitives d'écriture

    0x1802EF920(dst, u16 v)   ->  *(u16*)dst = htons(v) ; rend dst+2
    0x1802EF9C0(dst, u32 v)   ->  *(u32*)dst = htonl(v) ; rend dst+4
    0x1802EFA60(dst, src, n)  ->  memcpy ; rend dst+n

`htons`/`htonl` sont les **vraies importations `ws2_32`** (créneaux
`0x180346510` et `0x180346490`, vérifiés par `tools/reseau.py appels`),
enveloppées dans une `std::function` à chargement retardé (d'où le test à zéro
du créneau avant chaque appel). **Tout est donc en gros-boutiste, ordre
réseau.**

### b. L'en-tête, octet par octet — `0x1802EF890`

    0x1802EF890(dst, hdr):
        write_u16(dst,      hdr[0x00])      ; type du message
        write_u16(   ,      hdr[0x02])      ; longueur
        write_u32(   ,      hdr[0x04])      ; magic cookie
        copie hdr[0x08..0x13] octet par octet   ; identifiant de transaction
        rend dst + 20

    offset  taille  champ
    0       2       Message Type          (gros-boutiste)
    2       2       Message Length        (gros-boutiste, hors en-tête)
    4       4       Magic Cookie          (gros-boutiste)
    8       12      Transaction ID        (12 octets bruts, BCryptGenRandom)
                                          = 20 octets

**C'est l'en-tête de la RFC 5389 §6, à la virgule près.**

### c. Les deux écrivains génériques

`0x1802EF780(dst, hdr, vector<u32>* attrs, std::function* f)` — en-tête, puis
pour chaque en-tête d'attribut de la liste, `f(u32 en-tête, u8*& curseur)`.
C'est la voie des quatre paquets STUN/TURN.

`0x1802EF700(dst, hdr, u16 methode, std::function* f)` — en-tête, puis
`f(u16 methode, u8*& curseur)`. C'est la voie des paquets propriétaires.

`vector<u32>` : chaque entrée est un `UStunAttributeHeader` =
`{ u16 type ; u16 longueur }` **en ordre machine** ; le `type` et la
`longueur` sont convertis à l'écriture. La longueur totale se calcule par

    total = 20 ; pour chaque attribut : total += 4 + len + ((4 - (len & 3)) & 3)

soit **le remplissage à quatre octets de la RFC 5389 §15**.

### d. LES NUMÉROS D'ATTRIBUT — CE SONT CEUX DES RFC

Relevés en immédiat, dans l'ordre où chaque branche les empile. Le littéral
`0x000L000T` est le `u32` `{type, longueur}` tel que le compilateur l'a fusionné.

| branche | paquet (`type_info`) | méthode | immédiats d'attributs |
|---|---|---|---|
| 1 | `ULinkPacketBindingRequestStun` (`0x1806692C0`) | **0x0001** | `0x00040003` |
| 2 | `ULinkPacketAllcoateTurn` (`0x180669E30`) | **0x0003** | `0x0006`, `0x0014`, `0x0015`, `0x0004000D`, `0x00040019` |
| 3 | `ULinkPacketRefreshTurn` (`0x18066A038`) | **0x0004** | `0x0006`, `0x0014`, `0x0015`, `0x0004000D` |
| 4 | `ULinkPacketChannelBind` (`0x18066A1C8`) | **0x0009** | `0x0006`, `0x0014`, `0x0015`, `0x00080012`, `0x0004000C` |

Traduction :

| numéro | longueur | nom RFC | RFC |
|---|---|---|---|
| `0x0003` | 4 | CHANGE-REQUEST | 3489 §11.2.4 |
| `0x0006` | variable | USERNAME | 5389 §15.3 |
| `0x0008` | 20 | MESSAGE-INTEGRITY | 5389 §15.4 |
| `0x000C` | 4 | CHANNEL-NUMBER | 5766 §14.1 |
| `0x000D` | 4 | LIFETIME | 5766 §14.2 |
| `0x0012` | 8 | XOR-PEER-ADDRESS | 5766 §14.3 |
| `0x0014` | variable | REALM | 5389 §15.7 |
| `0x0015` | variable | NONCE | 5389 §15.8 |
| `0x0019` | 4 | REQUESTED-TRANSPORT | 5766 §14.7 |

Et les méthodes : **1 = Binding, 3 = Allocate, 4 = Refresh, 9 = ChannelBind**
— les valeurs de la RFC 5389 §18.1 et de la RFC 5766 §13.

Deux corroborations qui ne laissent pas de place au doute :

- **REQUESTED-TRANSPORT vaut 17.** `0x1802EE0AB : mov dword ptr [rbp], 0x11`
  juste avant d'empiler `0x00040019`. `17` est le numéro de protocole IANA
  d'UDP, c'est-à-dire exactement ce que la RFC 5766 §14.7 impose.
- **CHANGE-REQUEST porte ses drapeaux au bon octet.** `0x1802EDC7A..0x1802EDC8B`
  construit `cl ∈ {0, 2, 4, 6}` et l'écrit en `[rbp+3]`, soit le **dernier**
  octet de la valeur de 4 octets : `0x02` = *change port*, `0x04` = *change IP*.
  C'est la découverte de type de NAT de la RFC 3489, et cela alimente les
  champs `nat_mtype` / `nat_ftype` de `/api/match` (§4).

**Aucun numéro dans la plage privée `0x8000-0xFFFF` n'est écrit comme
attribut. Aucun numéro n'est décalé. Il n'y a pas d'attribut maison.**

### e. MESSAGE-INTEGRITY — posé à la main, après coup

Identique dans les branches 2, 3 et 4 (`0x1802EE1A3`, `0x1802EE5F1`,
`0x1802EEA80`). Le déclencheur est **la présence d'un NONCE** :

    cmp dword ptr [rbp+0x750], 0     ; longueur du nonce
    seta bl                          ; bl = « il faut signer »
    call 0x1802CB110(pkt, ULinkPacketAttrHMAC)
    si pas d'attribut HMAC et bl -> échec

Puis, avant l'écriture :

    lea r12d, [rcx + 0x18]       ; total += 24
    test bl, bl
    cmove r12d, ecx              ; ... seulement si on signe
    lea eax, [r12 - 0x14]
    mov word ptr [rbp+0xa], ax   ; LONGUEUR = total - 20, MESSAGE-INTEGRITY COMPRIS

C'est la subtilité de la RFC 5389 §15.4 : *le champ longueur doit déjà pointer
la fin de MESSAGE-INTEGRITY quand on calcule le condensat*. SEGA la respecte.

Ensuite (`0x1802EE1E4` et suivants) :

    HMAC-SHA1(clé 16 octets, tout ce qui est déjà écrit)   ; 0x1802E3D70
    write_u16(fin, 0x0008)                                 ; MESSAGE-INTEGRITY
    write_u16(   , 0x0014)                                 ; longueur 20
    memcpy   (   , condensat, 20)

`0x0008` et `20` sont **littéraux** (`mov edx, 8` puis `mov edx, edi` avec
`edi = 0x14`). La clé de 16 octets vient de `ULinkPacketAttrHMAC` et vaut
`MD5(username ":" realm ":" password)` — voir §3.

**Il n'y a PAS de FINGERPRINT (`0x8028`).** Aucun immédiat `0x8028` ni
`0x5354554E` (le XOR de la RFC 5389 §15.5) n'existe dans le binaire.

### f. Le résultat : un paquet Allocate, octet par octet

Premier envoi (sans nonce, donc sans MESSAGE-INTEGRITY — c'est la requête qui
provoque le `401 Unauthorized` et fournit realm et nonce) :

    00  00 03            type    = 0x0003  Allocate Request
    02  00 10            longueur = 16
    04  21 12 A4 42      magic cookie
    08  .. x12           identifiant de transaction (BCryptGenRandom)
    14  00 06 00 uu      USERNAME, longueur uu
    18  <username>       + remplissage à 4
    ..  00 14 00 rr      REALM
    ..  <realm>          + remplissage
    ..  00 0D 00 04      LIFETIME
    ..  <durée u32>
    ..  00 19 00 04      REQUESTED-TRANSPORT
    ..  11 00 00 00      17 = UDP, puis trois octets nuls

Second envoi (avec le nonce du serveur) : les mêmes attributs, plus

    ..  00 15 00 nn      NONCE
    ..  <nonce>          + remplissage
    ..  00 08 00 14      MESSAGE-INTEGRITY
    ..  <HMAC-SHA1, 20 octets>

**C'est un client TURN de manuel.**

---

## 9. LE SECOND PROTOCOLE — cookie `0x12B26FC4`

Les cinq autres branches du sérialiseur n'écrivent **pas** le cookie de la RFC.

    0x1802EEBCD  mov dword ptr [rsp+0x44], 0x12B26FC4
    0x1802EEDB2  mov dword ptr [rsp+0x44], 0x12B26FC4
    0x1802EEF47  mov dword ptr [rsp+0x44], 0x12B26FC4
    0x1802EF0D8  mov dword ptr [rsp+0x44], 0x12B26FC4
    0x1802EF24F  mov dword ptr [rsp+0x44], 0x12B26FC4

`0x12B26FC4` **n'est pas** `0x2112A442`. C'est le cookie maison de SEGA, et il
va avec des numéros de méthode maison, dans la plage haute :

| méthode | paquet | taille d'en-tête |
|---|---|---|
| `0x8000` | `ULinkPacketCommunicationConfirmation` | 24 |
| `0x8001` | `ULinkPacketResponseCommunicationConfirmation` | 24 |
| `0x8004` | `ULinkPacketLineQuality` | 26 |
| `0x8005` | `ULinkPacketResponseLineQuality` | 26 |
| `0x8010` | **`ULinkPacketAppData`** | 20 |

La table des tailles est explicite, en `0x1802EDAF0` :

    0x8000, 0x8001 -> 0x18   ; 20 + 4
    0x8004, 0x8005 -> 0x1A   ; 20 + 6
    tout le reste  -> 0x14   ; 20

C'est cette énumération que le RTTI appelle `raw_packet::W4LinkMethod` : les
quatre lambdas `0x1802ED620` (`cmp word ptr [rdx], 0x8000`), `0x1802ED830`
(`0x8001`), `0x1802ED8A0` (`0x8004`), `0x1802ED680` (`0x8005`) sont les quatre
écrivains de corps, et `0x8010` (AppData) n'a pas de corps du tout — juste une
somme de contrôle et la charge utile.

**Ce que cela veut dire : ces paquets-là ne sont pas du STUN.** Ils réutilisent
la *forme* de l'en-tête (20 octets, même disposition) mais ni le cookie ni les
numéros de méthode ne sont ceux de la RFC. Un serveur TURN qui les recevrait en
direct les rejetterait — et c'est voulu : **ils ne lui sont jamais adressés.**
Ils voyagent enveloppés dans un **ChannelData** (§10), que le relais transmet
sans jamais l'analyser.
