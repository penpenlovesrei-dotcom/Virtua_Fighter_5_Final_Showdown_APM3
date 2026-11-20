# API_MATRIX — VF5FS → API → loader → matériel

Établi sur `APM3_FS/vf5` (Rev B ver 6.0000), à partir de la table `.dynsym` de l'ELF et des
tables d'exports des bibliothèques **présentes dans le dump lui-même**. Le détail symbole par
symbole est dans `analysis/API_MATRIX_raw.txt`, régénérable par `tools/api_matrix.py`.

Répartition des 421 imports non définis :

| Fournisseur | Symboles | Nature |
|---|---:|---|
| `libGL.so.1.0.8769` (NVIDIA) | 163 | OpenGL |
| `libglut.so.3.8.0` | 30 | fenêtrage / boucle GLUT |
| `libalpb.so` | 24 | facturation et exploitation arcade Sega |
| `libsegaapi.so` (v2.08.0000) | 22 | audio Sega |
| `libGLU.so.1.3` | 2 | `gluLookAt`, `gluOrtho2D` |
| `libX11.so.6.2` | 1 | `XFree` |
| libc / libstdc++ / libm / libpthread / libz / libdl | 402 (reste) | runtime |

---

## 1. Audio

```
VF5FS  →  SEGAAPI_*  →  libsegaapi.so 2.08.0000  →  drv/ssound (carte son Lindbergh)
```

22 fonctions importées : `SEGAAPI_Init`, `SEGAAPI_Exit`, `SEGAAPI_CreateBuffer`,
`SEGAAPI_DestroyBuffer`, `SEGAAPI_UpdateBuffer`, `SEGAAPI_Play`, `SEGAAPI_PlayWithSetup`,
`SEGAAPI_Pause`, `SEGAAPI_Stop`, `SEGAAPI_Reset`, `SEGAAPI_SetLoopState`,
`SEGAAPI_SetReleaseState`, `SEGAAPI_SetSampleRate`, `SEGAAPI_GetPlaybackPosition`,
`SEGAAPI_SetPlaybackPosition`, `SEGAAPI_GetPlaybackStatus`, `SEGAAPI_SetChannelVolume`,
`SEGAAPI_SetSendLevel`, `SEGAAPI_SetSendRouting`, `SEGAAPI_SetSynthParam`,
`SEGAAPI_SetGlobalEAXProperty`, `SEGAAPI_SetUserData`.

Au-dessus, le jeu n'appelle pas SEGAAPI directement : il passe par le middleware **CRI**
(classes RTTI `CriAuVoice`, `CriAuSynth`, `CriAuCueSheet`, `CriSoundRendererLindbergh`,
`CriSrVocCoreLindberghHsr`). Le nom `CriSoundRendererLindbergh` montre que CRI dispose d'un
back-end spécifique à cette plateforme.

Chaîne complète :

```
Game (TaskRobSound, TaskMovie…)
  → CRI ADX2 / CriAu* (CriAuCueSheet, CriAuVoice, CriAuSynth)
    → CriSoundRendererLindbergh
      → SEGAAPI_*  (libsegaapi.so 2.08.0000)
        → pilote ssound (drv/ssound/phase2_rc8a)
          → carte son Lindbergh
```

Confiance : **SUPPORTED** (déduit des imports + noms de classes ; le flux d'appel n'est pas
encore tracé dans le code).

---

## 2. Rendu

```
VF5FS  →  OpenGL ARB + extensions NV  →  libGL.so.1.0.8769  →  GPU NVIDIA (Lindbergh)
```

163 symboles OpenGL importés, contre une seule fonction X11 (`XFree`) et 30 fonctions GLUT :
**le jeu délègue tout le fenêtrage à GLUT**, il ne parle pas directement à X11.

Les programmes de shaders sont des programmes ARB soumis via `glProgramStringARB`
(site d'appel connu à `0x08052B20`) et dépendent d'extensions NVIDIA — d'où le module
`shaderWork/vf5.c` du loader. Confiance : **SUPPORTED**.

Ressources associées dans le dump : `rom/shader.farc` (2,44 Mo).

---

## 3. Entrées, pièces, JVS

**Aucune bibliothèque JVS n'est importée dynamiquement.** Le code JVS est **statiquement lié
dans `vf5`** : les chaînes d'erreur nomment les fonctions de la bibliothèque AM de Sega.

| Fonction (extraite des chaînes de diagnostic) | Rôle apparent |
|---|---|
| `amJvsInit` / `amJvsExit` | ouverture / fermeture du bus |
| `amJvsSendRequest` / `amJvsAcknowledge` | transaction JVS |
| `amJvspClearPacket` | préparation de paquet |
| `amJvspReqSwInput` | lecture des boutons |
| `amJvspReqAnalogInput` | lecture des axes analogiques |
| `amJvspReqCoinInput` / `amJvspReqCoinDecrement` | monnayeur |
| `amJvspReqGeneralOutput1` / `amJvspAckGeneralOutput1` | sorties générales (lampes) |

Messages de contrôle présents : `JVS I/O board is not connected to main board.` et
`JVS I/O board does not fulfill the game spec.`

Le transport est série : le binaire importe `tcgetattr`, `tcsetattr`, `tcflush`,
`cfsetispeed`, `cfsetospeed` et référence `/dev/tts/0`, `/dev/tts/1`, `/dev/tts/USB0`.

```
VF5FS (amJvs*, lié statiquement)
  → termios sur /dev/tts/N
    → carte I/O JVS
      → boutons, joystick, monnayeur, lampes
```

Confiance : **SUPPORTED**.

---

## 4. Matériel de la carte de base et sécurité

Chemins de périphériques référencés dans le binaire :
`/dev/lbb` (Lindbergh Base Board), `/dev/i2c/0`, `/dev/input/js`, `/dev/console`,
`/dev/urandom`, `/dev/null`.

Le binaire importe `iopl`, `mount`, `umount`, `syscall`, `sched_setaffinity`,
`sched_getaffinity`, `setrlimit` : il agit directement sur le système.

Fonctions de sécurité **liées statiquement**, localisées par le loader :
`amDongleInit` (`0x088B1866`), `amDongleIsAvailable` (`0x088B0321`),
`amDongleUpdate` (`0x088B0D17`) ; réglages DIP via `amDipswInit` / `amDipswExit` /
`amDipswGetData` / `amDipswSetLed` autour de `0x088B00B4`, contexte global à `0x093CE7C8`.

---

## 5. Facturation et exploitation — `libalpb.so`

24 fonctions, toutes préfixées `alpbEx`. Elles couvrent trois domaines :

- **crédits et comptabilité** : `alpbExStartCredit`, `alpbExEndCredit`, `alpbExGetCreditCode`,
  `alpbExItemAccount`, `alpbExStartAccountingReport`,
  `alpbExLoadLastAccountingReportTime`, `alpbExLoadLastBgAccountingReportTime`,
  `alpbExLoadPlayHistory`, `alpbExGetNearFullEnable`, `alpbExSetNearFullEnable` ;
- **identité machine** : `alpbExGetLindberghSerialID`, `alpbExGetCardBindingSerialID`,
  `alpbExCheckCardMemory` ;
- **cycle de vie et réseau** : `alpbExInitialize`, `alpbExFinalize`, `alpbExExecServer`,
  `alpbExSetHostIpAddress`, `alpbExGetExecStatus`, `alpbExGetBackgroundStatus`,
  `alpbExGetIgnoreStatus`, `alpbExGetFgArReady`, `alpbExGetDisplayErrorNo`,
  `alpbExGetTime`, `alpbExSetOperationEnable`.

`alpbExGetLindberghSerialID` nomme explicitement la plateforme — preuve supplémentaire que
`APM3_FS` est un dump Lindbergh.

`libsama.so` et `libbdlog.so` sont déclarées en `DT_NEEDED` mais **aucun de leurs symboles
n'est importé par `vf5`** : elles sont vraisemblablement des dépendances de `libalpb.so`, ou
chargées via `dlopen`/`dlsym` (tous deux importés). Confiance : **LIKELY**, à vérifier en
lisant les `DT_NEEDED` de `libalpb.so`.

---

## 6. Système de fichiers et données

Le jeu accède à un arbre `/home/diskN` monté sur des partitions ext3 :
`/home/disk0` (exécutable), `/home/disk1` (données `rom/`), `/home/disk2` (RAM disque
inscriptible), `/home/disk8` (gros fichiers de test).

Le script `game` de la Rev B 6.0000 crée lui-même sa partition (`parted`, `mkfs.ext3 -L SBUV`,
`mount -t ext3 -o data=journal /dev/hdb5 /home/disk2`) avant de lancer `./vf5 -fs $1`.

Format d'archive propriétaire : **FARC** (signatures `FArc` non compressé, `FArC` compressé).
851 archives FARC dans `APM3_FS`. Les diagnostics du binaire nomment la couche :
`File::exec_open(): no farc file(%s).`, `File::exec_load(): file not found in farc. (%s)`.
Décompression par zlib (`inflate`, `uncompress` importés de `libz`).

---

## 7. Réseau

`ng_server.conf` décrit un serveur « NG » avec lobbies, salons et groupes ; le binaire
contient `MDATA VERSION STATUS`, `DVD version`, `NET version`, `DELIVER version`.
Les démons `gdeliver`, `gfetcherd`, `mfetcherd` (dans `tools/lindbergh/`) assurent la
distribution d'application et de données.

Le loader neutralise une vérification réseau à `0x0812326E` (`stubReturn`) : c'est le point
d'entrée à documenter en premier pour le sous-système réseau.

---

## 8. Ligne du temps de la boucle

Reste **UNKNOWN** à ce stade. Indices disponibles : GLUT fournit la boucle principale
(30 symboles importés), une classe RTTI `SysFrameRate` existe, et une tâche
`TaskPlayFrameSpeed` est présente. À traiter en phase 3.

---

## Tableau de synthèse

| Sous-système | Interface du jeu | Fourniture | Matériel |
|---|---|---|---|
| Audio | `CriAu*` → `SEGAAPI_*` | `libsegaapi.so` 2.08.0000 | carte son Lindbergh |
| Rendu | OpenGL ARB + ext. NV | `libGL.so.1.0.8769` | GPU NVIDIA |
| Fenêtrage | GLUT (30 sym.) | `libglut.so.3` | X11 |
| Entrées / pièces | `amJvs*` (statique) | termios `/dev/tts/N` | carte I/O JVS |
| Sécurité | `amDongle*` (statique) | `/dev/lbb`, `/dev/i2c/0` | dongle + carte de base |
| Facturation | `alpbEx*` | `libalpb.so` | ALL.Net |
| Fichiers | `File::` + FARC | ext3 `/home/diskN`, zlib | disque IDE |
| Réseau | NG server | `ng_server.conf`, `gdeliver` | ALL.Net |
| Threads / temps | `pthread_*`, `nanosleep`, `gettimeofday` | glibc MontaVista | — |
