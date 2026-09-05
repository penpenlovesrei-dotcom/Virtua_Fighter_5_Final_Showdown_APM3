# Le réseau dans le build APM3 — premier relevé

Établi le 2026-09-05, par lecture statique de
`vf5fs-pxd-w64-Retail_APM3.dll.origine`, `vfes.exe`, `apm.reelle.dll` et, pour
comparaison, du moteur de R.E.V.O.

Question posée par Frédéric : peut-on ajouter du jeu en ligne, en s'inspirant de
[YAMPnet](https://github.com/biggestsonicfan/YAMPnet), ou en transplantant celui
de R.E.V.O. ?

---

## 1. Trois lignées, trois netcodes

| build | netcode | présent dans APM3 ? |
|---|---|---|
| R.E.V.O. (Steam) | **rollback** + appariement EOS | **absent** : 0 occurrence de `Rollback`, 0 de `EOS_`, 0 de `SteamAPI` |
| PS3 / Xbox 360 | **retard**, via PSN / Live | mode 7 `ONLINE` présent dans la table, **bouchonné aux trois gestionnaires** ; les six sous-états `ONLINE_*` aussi |
| **borne (ALL.Net)** | **bornes liées**, pair à pair | **présent, et entier** |

R.E.V.O. porte cinq classes dédiées — `AVTaskRobRollback`, `AVIoRollbackCtrl`,
`AVIoVsRollbackCtrl`, `AVRollbackTraceRobInfo`, `AVRollbackTraceUnit` — et 72
entrées d'API EOS de lobby. Rien de tout cela n'existe côté APM3 : ce n'est pas
bouchonné, c'est absent du binaire.

---

## 2. Le sous-système LINK, intact

Vingt-trois classes, relevées par leur RTTI :

**La machine à états principale**

    AVLinkMainStateBase
    AVLinkMainStateStartup
    AVLinkMainStateSetup
    AVLinkMainStateStandby
    AVLinkMainStateUnavailable
    AVLinkMainStateMatchingAllocate
    AVLinkMainStateMatchingChannelBind
    AVLinkMainStateMatchingConnectivityCheck
    AVLinkMainStateMatchingMatch
    AVLinkMainStateMatchingQualityCheck
    AVLinkMainStateMatchingWaitReady
    AVLinkMainStatePlaying
    AVLinkMainStatePlayEnd
    AVLinkMainStateBasePlayEndReceivable
    AVLinkMainStateCleanupMatch

**Le transport**

    AVLinkReceiveThread    AVLinkSend
    AVPacketBase           AVPacketGate      AVPacketMediator
    AVSendPacket           AVReceivePacket
    AVTaskSession

Ce n'est pas un vestige d'appariement : la chaîne va du démarrage jusqu'à la
**phase de combat** (`Playing`), la fin de partie et le nettoyage, avec un fil
de réception et un médiateur de paquets.

### Le transport est câblé

Le moteur importe **quatorze fonctions de `ws2_32`** :

    socket        connect       sendto        recvfrom      shutdown
    setsockopt    getsockopt    ioctlsocket   WSAIoctl
    getsockname   getpeername   ntohl  htonl  ntohs

`vfes.exe` n'en importe aucune ; `apm.reelle.dll` seulement `ntohl` et `htonl`.
**Le réseau est donc dans le moteur du jeu, pas dans l'hôte** — c'est une bonne
nouvelle : c'est la partie dont nous avons le binaire.

---

## 3. Le déterminisme est établi, par le jeu lui-même

Frédéric : « en mode 2 joueurs humains, le jeu doit être déterministe, comme
tous les jeux de combat ». Le binaire le confirme — il sait **rejouer** un
combat :

    AVTaskGameVsReplay      AVTaskMenuReplay        AVTaskReplayUpload
    AVTaskRobShortReplay    AVTaskRobShortReplay_Rec

et les scènes `REPLAY`, `REPLAY MENU`, `REPLAY_VS`, `REPLAY_SCORE`,
`ROB_SHORT_REPLAY`, `ROB_SHORT_REPLAY_REC`, `TERM_REPLAY_BUF`.

Un rejeu ne fonctionne que si la simulation est déterministe et pilotée par des
entrées enregistrées. C'est le prérequis de tout netcode à retard, et la
fondation de tout rollback — acquis sans avoir à le mesurer.

---

## 4. Les trois pistes, pesées

### a. Transplanter le netcode de R.E.V.O. — **écartée**

- Le rollback exige de photographier et restaurer l'état complet à chaque
  trame ; cette machinerie n'existe pas côté APM3.
- Les deux DLL sont des **frères, pas des jumeaux** : mêmes fonctions, adresses
  et dispositions d'objets différentes (R.E.V.O. range sa sous-page active en
  `+0x608`, APM3 en `+0x650`). Du code compilé ne se relocalise pas d'un binaire
  à l'autre sans réédition de liens, donc sans les sources.
- L'appariement dépend d'EOS et de Steam, avec authentification.
- Et recopier du code compilé de SEGA serait de la contrefaçon. **Lire** pour
  comprendre est de l'interopérabilité ; **copier** ne l'est pas.

### b. Écrire notre propre lockstep — possible, mais tout est à faire

La couture existe : **`apm.dll` est la source unique des entrées**
(`Input_isOn`, `Input_isOnNow`), appelée une fois par trame depuis
`Core_execute`, et elle sert déjà deux joueurs séparés (clavier en 1, manette
en 2). Brancher le joueur 2 sur un pair réseau est le même geste.

Reste à écrire : transport, appariement, gestion de la latence, et la
synchronisation d'une boucle que nous ne maîtrisons pas.

### c. Réveiller les bornes liées — **la piste à suivre**

Le netcode est déjà là, écrit par SEGA pour ce jeu, avec son appariement, son
transport et sa phase de combat. Il n'y a rien à inventer : il y a à comprendre
**ce qui l'empêche de démarrer**, et à lui fournir un pair.

C'est aussi la seconde stratégie de YAMPnet, qui ne réécrit pas le netcode des
jeux conçus comme deux cabinets reliés mais **fait passer le leur** par des
datagrammes UDP.

Et c'est le rôle que notre `apm.dll` joue déjà pour les entrées et les pièces :
répondre à la place de la carte arcade.

### d. Le rollback, si le retard ne suffit pas

Il faudrait écrire les trois choses qui manquent :

| il faut | APM3 |
|---|---|
| photographier l'état de simulation | rien — le rejeu enregistre des **entrées**, pas un état |
| le restaurer | rien |
| re-simuler N trames en une, sans dessiner | aucun point d'entrée connu |

La difficulté n'est pas le réseau : c'est d'énumérer **chaque octet mutable que
la simulation touche** — les deux ROB, la session, les collisions, le générateur
aléatoire, les minuteurs d'effets. Un octet oublié désynchronise une fois sur
cent, sans qu'on sache d'où.

Contournement possible, celui des émulateurs : photographier des **régions de
tas entières** (`VirtualQuery` puis `memcpy`) plutôt que des champs choisis.
Brutal, mais il ne demande pas de tout comprendre. Reste la troisième exigence,
avancer la simulation sans dessiner, qui suppose de trouver où le moteur sépare
mise à jour et rendu.

---

## 5. L'ordre de travail proposé

1. **Cartographier `AVLinkMain*` et `AVTaskSession`** : où la machine s'arrête,
   ce qu'elle attend d'ALL.Net, et si `apm.dll` peut lui répondre.
2. **Faire se parler deux instances**, d'abord en réseau local.
3. **Mesurer le retard** sur Internet. Conçu pour du local, il sera peut-être
   déjà jouable.
4. **Le rollback seulement si nécessaire** — chantier de plusieurs mois.

---

## 6. Ce qui n'est pas établi

- Aucune des classes `AVLink*` n'a été désassemblée. On ne sait pas encore où la
  machine s'arrête, ni si ses gestionnaires sont bouchonnés comme ceux du mode 7.
- On ne sait pas ce que le protocole attend d'ALL.Net : découverte, allocation
  de canal, jeton d'autorisation.
- On ne sait pas si `AVLinkMainStatePlaying` échange des **entrées** ou un
  **état** — ce qui change tout pour la latence tolérable.
- Le rejeu prouve le déterminisme de la simulation, pas son indépendance à la
  cadence d'affichage.
- Les fichiers VF5FS de Yakuza 6 (le build que fait tourner YAMP) n'ont pas été
  examinés : ce serait un troisième frère à comparer.
