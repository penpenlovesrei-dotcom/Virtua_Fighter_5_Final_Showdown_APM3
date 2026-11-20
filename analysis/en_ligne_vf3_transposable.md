# Le mode en ligne de `fv2-recomp` est-il transposable à VF5FS APM3 ?

Question de Frédéric, 2026-11-19 : *« parmi ces options, il y a le mode de jeu
en ligne. Il est adapté à la décompilation de Virtua Fighter 3, qui utilise le
bouton d'esquive qui n'existe plus dans Virtua Fighter 5. Est-ce transposable à
notre projet ? »*

Établi par **lecture seule** du projet voisin
`C:\Users\frede\Documents\RECOMP\Fighting Vipers 2\fv2-recomp` (rien n'y a été
écrit) et de nos propres notes. Aucune course, aucun lancement.

> **Verdict en une ligne : inutile de le transposer.** Le netcode de bornes
> liées de VF5FS fait déjà exactement le même travail — des entrées, un mot de
> 16 bits par trame, sur UDP avec STUN/TURN — et il est **entier dans le
> binaire**. Et le mode en ligne du voisin est, lui, **intransposable** : non
> pas à cause du bouton d'esquive, mais parce qu'il exige `save()` / `load()`
> de l'état complet de la simulation à chaque trame.

---

## 1. Ce que Frédéric a vu : le menu de `fv2-recomp`

MESURÉ — `src/host/main.cpp`, fonction `main_page` (lignes 4880-4911). Le menu
est une pile de pages, chaque entrée portant un libellé et sa phrase
d'explication : `Resume`, `Display`, `Sound`, `Game`, `Fighting Vipers 2`,
`Arcade settings`, **`Online`**, `Cheats`, `Controls`, `Quit`. C'est bien « des
options à valider une à une ».

L'entrée `Online` est **conditionnelle** (main.cpp:4903) :

    if (board.profile->online)
        p.items.push_back({ "Online", "Play someone over the network: host a match, or join one.", ... });
    else
        p.items.push_back({ "Online", "Online play isn't ready for " + board.profile->name
                                      + " yet: switch to Virtua Fighter 3 in Game > Version to play online.", ... });

Le drapeau `Profile::online` (`src/machine/profile.h:44`) est vrai pour
Virtua Fighter 3 Revision D **et** pour Fighting Vipers 2 Rev A
(`profile.cpp`, `FV2_REV_A`), faux pour les autres jeux de ROM. Frédéric a donc
raison sur le fond : **ce mode est taillé pour la lignée Model 3 de ce port**,
et son message d'indisponibilité renvoie littéralement à Virtua Fighter 3.

---

## 2. Ce qu'est réellement ce mode en ligne

MESURÉ, par lecture de `src/net/*`, `src/host/online.*`,
`src/host/vf3_netplay.*` et `docs/netplay.md`.

| Point | Ce que c'est |
|---|---|
| Bibliothèque | **aucune bibliothèque tierce** : `src/net` est une implémentation **maison**, écrite pour ce projet. Ni GGPO, ni GekkoNet, ni Steam. En-tête de `session.h` : « GGPO-style rollback between two players over a Link » |
| Modèle | **rollback** (spéculation + retour en arrière), pas du relais, pas du lockstep pur |
| Transport | UDP brut (`src/net/link.h`, `UdpLink`), un datagramme à la fois, non ordonné |
| Traversée de NAT | **STUN / TURN standard** (`src/net/stun.h`, RFC 5389 et 8656), perçage direct d'abord, relais TURN de Cloudflare en secours (`src/net/room_link.*`) |
| Appariement | un **lobby** = un Worker Cloudflare (`tools/lobby`), codes de salon à 6 lettres, jeton de 64 bits ; appariement aléatoire aussi |
| Retard d'entrées | `Config::delay` = 2 par défaut, **0 à 15 trames**, « Auto » calculé à partir du ping et de ce que la machine d'en face peut re-simuler |
| Rollback | `max_rollback = 7` trames ; au-delà on attend plutôt que de deviner plus loin |
| Désynchronisation | empreinte d'état toutes les `checksum_every = 30` trames (le doc dit 120 trames côté jeu), fin de partie annoncée « desync » |
| Cadence | fixe, **57,524 Hz** sur les deux côtés |
| Sécurité | `netfuzz` : 48 000 sessions, ~14 M de paquets abîmés, rien hors bornes (MESURÉ par eux, pas par nous) |
| Licence | **MIT**, `Copyright (c) 2026 mr-finster` ; `origin` = `github.com/mr-finster/vf3-recomp`, le dépôt local est le fork de Frédéric |

### Le modèle d'entrées : un mot de 16 bits, 10 bits utilisés

MESURÉ — `src/host/vf3_netplay.cpp:12` et `:19-32` :

    enum : uint16_t { UP = 1, DOWN = 2, LEFT = 4, RIGHT = 8, PUNCH = 16, KICK = 32,
                      GUARD = 64, ESCAPE = 128, START = 256, COIN = 512 };

    uint16_t pack(const m3::Controls &c, int p);   // un mot par joueur
    void unpack(uint16_t b, int p, m3::Controls &c);

Un `uint16_t` **par joueur et par trame**, dont **dix bits** sont employés :
quatre directions, P, K, G, **E (le bouton d'esquive)**, Start, Coin. `test` et
`service` ne passent jamais sur le fil. La session elle-même ne connaît que
`uint16_t` (`Session::step(uint16_t input)`, `Game::advance(const uint16_t
input[2], bool resim)`) : **le jeu seul interprète les bits.**

---

## 3. Ce que ce mode exige du jeu — c'est là qu'est le verrou

MESURÉ — `src/net/session.h`, l'interface que tout jeu doit fournir :

    struct Game {
        virtual bool begin(const std::vector<uint8_t> &blob) = 0;
        virtual void save(std::vector<uint8_t> &state) = 0;   // l'état avant la trame suivante
        virtual bool load(const std::vector<uint8_t> &state) = 0;
        virtual void advance(const uint16_t input[2], bool resim) = 0;
        virtual size_t hash_skip() const { return 0; }
    };

Et dans `src/net/session.cpp` :

* **`game.save(...)` est appelé à CHAQUE trame**, sans condition (ligne 666) ;
* `game.load(...)` est appelé dès qu'une devinette s'est révélée fausse
  (ligne 595) ; s'il échoue, la partie s'arrête en « desync » ;
* `advance(..., resim = true)` rejoue les trames **sans dessiner ni sonner**
  (`main.cpp:5719` : `game.tiles_on = false; board.run_frame();`).

Coût mesuré par eux (`docs/netplay.md`) : **sauvegarde 1,3 ms, restauration
1,5 ms**, en ne recopiant que les **pages de 4 Ko écrites depuis** la dernière
sauvegarde ; une copie complète de 27 Mo (≈ 4 ms) était « trop lente ».
`vf3soak` : 4 303 trames identiques avec un rollback de 7 trames à chaque trame.

**Pourquoi c'est possible chez eux :** la carte Model 3 est **leur** émulateur
et **leur** recompilateur. L'état de la simulation, ce sont leurs propres
tableaux, et `src/machine/state_io.h` les énumère champ par champ — « one
function lists the fields […] so the two can't drift apart ». Ils possèdent
chaque octet mutable du jeu. Nous possédons une DLL de SEGA.

---

## 4. Le bouton d'esquive n'est pas l'obstacle

MESURÉ des deux côtés :

* chez eux, `ESCAPE` vaut `0x80` : **un bit parmi seize**, dans un mot dont six
  bits sont déjà inutilisés ;
* chez nous, `ULinkPacketAppData` transporte lui aussi **un mot d'entrées de
  16 bits par trame** (`analysis/reseau_transport.md` §5 d :
  `mov word ptr [rdi + rax*8 + 4], r10w ; le mot d'entrees, 16 bits`).

Virtua Fighter 5 a **un bouton de moins** que Virtua Fighter 3 (P, K, G, sans
esquive). Un bouton en moins est **un bit en moins** : l'adaptation se réduirait
à retirer `ESCAPE` de `pack`/`unpack` et à renuméroter la table. C'est une
demi-journée, pas un obstacle. **La crainte de Frédéric n'est pas le problème.**

Le problème est ailleurs, et il est de nature différente : ce n'est pas le
format des entrées, c'est **la photographie de l'état**.

---

## 5. Ce que notre netcode sait déjà faire

MESURÉ — `analysis/reseau.md`, `documentation/reseau_transport.md`,
`documentation/reseau_machine.md`, `documentation/reseau_allnet.md`,
`memoire/reference_vf5_reseau.md`.

| Besoin d'un jeu en ligne | VF5FS APM3 |
|---|---|
| Transport | **présent** : `am::abaas::Udp`, 27 fonctions de `ws2_32` importées **par le moteur** (pas par `vfes.exe`) |
| Traversée de NAT | **présente, et standard** : `ULinkPacketBindingRequestStun` (RFC 5389), `ULinkPacketAllcoateTurn`, `RefreshTurn`, `ChannelBind`, `AttrHMAC`, magic cookie `0x2112A442` sur sept sites. **Un coturn ordinaire suffit** |
| Appariement | **présent** : HTTP ALL.Net (`abaaslink Ver.0f03646`), `/api/turninfo`, `/api/match`, `/api/config`, corps AES-256-CBC + zlib + CRC-32, contrat JSON relevé |
| Machine à états | **présente et complète** : 15 états `am::abaas::LinkMainState*`, de `Startup` à `CleanupMatch`, **`Playing` incluse** (`tic` de 2 665 octets), dans un **fil dédié à ~1 kHz** (`Sleep(1)`), indépendant des 60 Hz du jeu |
| Format d'échange | **des entrées, et rien que des entrées** : 16 octets utiles — n° de trame (4), champ compacté (2), l'entrée de la trame courante (1) et **les neuf précédentes** (9). Plafond dur de 1023 octets dans `sendPacket` (`0x1802C98A0`). Envoi **cadencé**, pas une fois par trame |
| Tolérance aux pertes | **9 trames de redondance = 150 ms à 60 Hz**, absorbées sans retransmission |
| Déterminisme de la simulation | **prouvé par le jeu lui-même** : il sait rejouer un combat (`AVTaskGameVsReplay`, `ROB_SHORT_REPLAY_REC`, `TERM_REPLAY_BUF`) à partir d'**entrées enregistrées** |
| Rollback | **absent** : zéro `Rollback`, zéro `EOS_`, zéro `SteamAPI` dans APM3 (c'est R.E.V.O. qui les porte) |

Et le point qui tranche la question posée : **avec les bornes liées, nous n'avons
jamais à injecter l'entrée du joueur distant.** Le code de SEGA lit son propre
panneau, l'empaquette, l'envoie, reçoit celui du pair et l'applique lui-même au
second combattant. C'est un problème que nous n'avons pas à résoudre — alors que
toute greffe extérieure (y compris `src/net`) nous l'imposerait, et que notre
seule couture d'entrées connue, `apm.dll`, est **un masque global de 12 bits
sans indice de joueur** (`documentation/docs/formats/apm_input.md` §2 : « Il n'y
a **pas d'indice de joueur** dans l'appel, et le masque testé est un seul mot
global ») — et que le mot d'entrée du combattant, `ROB+0x508`, est un **mot de
commande composite**, pas un champ de bits « un bouton, un bit » (§4 bis, même
fichier).

### Où nous en sommes, mesuré le 2026-09-06

`tools/pister_link.cmd`, 45 s (`donnees/pister_link.txt`, `..._bilan.txt`) :

| point | passages | lecture |
|---|---|---|
| `okGameId` / `okKeychipId` / `okMainId` / `okCountry` | 1 chacun | **les quatre validations passent** |
| `SetupLink` | **1** | une seule tentative : elle a **réussi** |
| `tic Setup` | 20 661 | la machine tourne dans son fil |
| `tic Unavailable` | **0** | elle n'a **pas** abandonné |

Puis (`documentation/reseau_allnet.md` §14) notre serveur minimal
`outils/serveur_allnet.py` a reçu, **déchiffré et lu** deux requêtes :
`POST /api/turninfo` (128 o) et `POST /api/data/load` (160 o), en-tête et CRC-32
concordants.

**Le mur actuel, nommé et unique : il n'y a pas de STUN sur `127.0.0.1:3478`.**
Le jeu mesure son type de NAT (`requestCheckNatType`, `0x1805C9550`) **avant**
d'appeler `/api/match`, et se tait quand personne ne répond. Un coturn avec
`vf5`/`vf5` suffit : le protocole est standard, rien à réinventer.

---

## 6. Le verdict

### a. Transposer le mode en ligne de `fv2-recomp` : **inutile, et de surcroît impossible tel quel**

**Inutile**, parce que notre jeu a déjà le même netcode, écrit par SEGA pour
lui : à retard, sur des entrées, un mot de 16 bits par trame, sur UDP avec
STUN/TURN, avec son appariement, son transport, sa machine à états et sa phase
de combat. On n'ajoute rien en greffant une seconde pile réseau par-dessus ;
on ajouterait un second problème.

**Impossible tel quel**, pour une raison technique qui n'est pas le bouton
d'esquive. `vfnet::Session` appelle `game.save()` à **chaque** trame et
`game.load()` dès qu'une devinette rate. Il nous faudrait donc les trois choses
que `analysis/reseau.md` §4 d énumérait déjà, et qui manquent toutes :

| il faut | APM3 |
|---|---|
| photographier l'état de simulation | rien — le rejeu enregistre des **entrées**, pas un état |
| le restaurer | rien |
| avancer N trames sans dessiner | aucun point d'entrée connu |

À quoi s'ajoutent quatre difficultés propres à notre cas, absentes du leur :

1. **Nous ne possédons pas l'état.** Chez eux, `state_io.h` liste les champs un
   par un. Chez nous, c'est le tas d'une DLL de 6 Mo de SEGA : deux ROB, la
   session, les collisions, le générateur aléatoire, les minuteurs. Un octet
   oublié désynchronise une fois sur cent.
2. **Le contournement « régions de tas entières » ne ferme pas.** `VirtualQuery`
   + `memcpy` ne capture ni l'état D3D12, ni celui des fils internes du moteur —
   dont le fil réseau à 1 kHz, qui tourne précisément pendant la photo.
3. **Avancer sans dessiner.** Chez eux, `board.run_frame()` avec `tiles_on =
   false`. Chez nous, mise à jour et rendu ne sont pas séparés à notre
   connaissance, et l'image passe par D3D12 que l'hôte enveloppe (CLAUDE.md §7).
4. **CLAUDE.md §2.** La règle écarte « par choix » la lecture de la mémoire d'un
   processus en marche, savestate compris. *Interprétation, à trancher par
   Frédéric* : la lettre de la règle visait le processus **REVO** (erreur 5) ;
   photographier **notre propre** processus hôte, qui charge la DLL APM3, n'est
   pas le même geste et ne demande aucun droit refusé. Mais le coût des points 1
   à 3 reste entier, et ne dépend pas de cette lecture de la règle.

### b. « Il suffit de l'exposer dans un menu » : presque — voici ce qui manque

Par ordre, et chacun chiffré en travail :

1. **Un répondeur STUN/TURN sur 3478.** Installer coturn avec
   `lt-cred-mech`, utilisateur `vf5`/`vf5`, le realm étant celui que coturn
   annonce dans son `401`. *Quelques heures.* C'est le prochain geste, et il est
   déjà nommé dans `documentation/_journal/A FAIRE.txt`.
2. **`/api/match` côté serveur.** Les deux sens sont lus
   (`reseau_allnet.md` §12), la recette du §10 est écrite, les deux journaux de
   télémétrie (`match_summary`, `match_path_quality`) sont décodés. *Jours.*
3. **Faire se parler deux instances**, d'abord en réseau local, et vérifier que
   la machine franchit `MatchingAllocate` → … → **`Playing`**. *Jours.*
4. **Mesurer le retard sur Internet.** Conçu pour deux bornes côte à côte, il
   sera peut-être déjà jouable ; la redondance de 9 trames dit que le protocole
   absorbe 150 ms de perte sans retransmettre, ce qui n'est pas le même nombre
   que la latence jouable. *À mesurer, pas à supposer.*
5. **Alors, et alors seulement, un menu.** Et il n'y a pas besoin d'en inventer
   un : APM3 porte déjà le **mode 7 `ONLINE`** dans sa table de modes, avec ses
   six sous-états, et l'entrée `ONLINE BATTLE` (`0x17A`) du `MULTI MENU` y mène
   (`analysis/menu_console.md`). **Mais ce mode-là est bouchonné à ses trois
   gestionnaires** : c'est le mode en ligne **PSN / Live des versions console**,
   pas celui des bornes liées. Les bornes liées ne passent pas par lui ; elles
   tournent dans leur fil, déclenchées par `setupLink`. *Donc : point ouvert.*
   **Non établi** : par quelle entrée d'interface une partie liée se propose au
   joueur dans ce build, et si elle s'en propose une du tout. À chercher du côté
   de `AbaasManager::update` et des accesseurs `Link::isXxx()`
   (`0x1802C8B00`…), pas du côté du mode 7.

### c. Une pièce du voisin reste réutilisable — en secours seulement

MESURÉ, et jamais essayé : `vfnet::Session::set_lockstep(true)` fait que
**aucune trame ne tourne sur une devinette** — `session.cpp:627` tient la trame
jusqu'à l'arrivée de l'entrée distante. Dans ce régime, `game.load()` n'est
jamais appelé, et `game.save()` (appelé, lui, à chaque trame) pourrait être un
corps vide. `src/net` serait alors un **transport + appariement + STUN/TURN +
lobby en lockstep pur, sous licence MIT**, utilisable sans rollback et sans
savestate.

C'est à garder **en secours**, si et seulement si les bornes liées se révélaient
impossibles à réveiller. Même alors, il resterait le problème que les bornes
liées nous épargnent : **où injecter l'entrée du joueur distant**, qui n'est pas
résolu (§5, `apm_input.md`).

---

## 7. Ce qui n'a pas été vérifié

* **Rien n'a été lancé.** Aucune course, ni chez nous ni chez le voisin. Tout
  ci-dessus est de la lecture de code et de notes.
* **Les mesures du voisin sont les leurs** : 1,3 ms de sauvegarde, 4 303 trames
  identiques, 48 000 sessions de `netfuzz`. Nous les citons, nous ne les avons
  pas refaites.
* **Aucune classe `am::abaas::LinkMainState*` n'a été exécutée au-delà de
  `Setup`.** `MatchingAllocate`, `Playing` et les autres sont lues
  statiquement ; qu'elles aboutissent est une **attente**, pas un fait.
* **La latence jouable de notre netcode n'est pas connue.** 9 trames de
  redondance ≠ 9 trames de retard tolérable. Le retard d'entrées appliqué par
  le jeu n'a pas été localisé.
* **L'entrée d'interface d'une partie liée n'est pas localisée** (§6 b 5).
* **Le sens de 8 des 13 codes d'entrée d'`apm.dll` n'est pas établi**
  (`apm_input.md` §4) ; et la phrase de `analysis/reseau.md` §4 b selon laquelle
  `apm.dll` « sert déjà deux joueurs séparés (clavier en 1, manette en 2) » est
  **en tension** avec `apm_input.md` §2 (masque global de 12 bits, sans indice
  de joueur). Point à trancher avant toute tentative d'injection.
* **Les fichiers VF5FS de Yakuza 6** (le build que fait tourner YAMPnet) n'ont
  toujours pas été examinés.

---

*Rédigé le 2026-11-19. Lecture seule de part en part : `fv2-recomp` n'a reçu
aucune écriture, et aucun binaire n'a été chargé.*
