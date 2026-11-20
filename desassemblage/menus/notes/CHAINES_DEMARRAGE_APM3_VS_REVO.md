# Les deux chaines de demarrage : APM3 (modele) contre REVO (cible)

Mesure du 6 novembre 2026. Deux fichiers, nommes :

```
APM3  FS APM3/banc/vf5fs-pxd-w64-Retail_APM3.dll                6 965 248 o
REVO  FS REVO/Virtua Fighter 5 REVO World Stage/runtime/media/
      vf5fs/vf5fs-pxd-w64-d3d12_SteamRetail.dll                 7 189 504 o
```

Tout est trouve par la chaine de caracteres puis par son pointeur -- **aucun
offset recopie a la main**. Les tables de noms :

```
APM3  modes  RVA 0x3A0C80 (11)    sous-etats  RVA 0x3A0CE0 (56)
REVO  modes  RVA 0x3BFC50 (15)    sous-etats  RVA 0x3BFCD0 (74)
```

Le banc de REVO (`FS REVO/vf5fs-pxd-w64-d3d12_SteamRetail.dll`, 7 229 952 o)
porte les **memes noms** a d'autres adresses (RVA 0x3C9110 / 0x3C9190).

## 0. Le meme arbre de source

Les DEUX binaires portent le meme chemin de compilation :

```
D:/Project/vf5/vf5fscs_source/20120711_update_1.1/vf5fs
```

Source **console** (`vf5fs`**cs**`_source`), 11 juillet 2012, update 1.1. REVO
n'est pas une rebase : c'est le meme arbre, plus tard.

## 1. REPONSE COURTE

**Aucune des deux chaines de demarrage ne manque dans REVO.** Les 10 sous-etats
d'arcade (`LOGO` -> `LOOP_TERMINAL`) et les 4 de console (`CS_TITLE` ->
`CS_DEMO`) sont dans les DEUX modules, **dans le meme ordre**. REVO n'enleve
rien a ces listes : il **insere** devant et **ajoute** derriere.

Ce qui manque dans REVO est ailleurs : **le mode APM3**, c'est-a-dire le code
qui fait tourner la borne apres le demarrage.

## 2. LES MODES (A = dans APM3, R = dans REVO)

```
    mode                       APM3    REVO
A R  STARTUP                    0       0      
A R  ADVERTISE                  1       1      
A R  GAME                       2       2      
- R  WORLD_STAGE                -       3      
A R  DATA_TEST                  3       4      
A R  MENU                       4       5      
A R  CS_TERM                    5       6      
A R  CS_TRAINING                6       7      
A R  ONLINE                     7       8      
A R  APM3                       8       9      
A R  APM3_TESTMODE              9       10     
- R  RANK_MATCH                 -       11     
- R  ROOM_MATCH                 -       12     
- R  TOURNAMENT                 -       13     
A R  MAX                        10      14     
```

REVO ajoute 4 modes : `WORLD_STAGE` (insere en 3), `RANK_MATCH`, `ROOM_MATCH`,
`TOURNAMENT`. Aucun mode retire -- `APM3` et `APM3_TESTMODE` sont toujours la.

## 3. LES SOUS-ETATS

```
    sous-etat                  APM3    REVO
A R  DATA_INITIALIZE            0       0      
A R  SYSTEM_STARTUP             1       1      
A R  WARNING                    2       2      
- R  CROSSPLAY_WARNING          -       3      
- R  OFFLINE_WARNING            -       4      
A R  CS_TITLE                   3       5      
A R  CS_SIGNIN                  4       6      
A R  CS_AUTOLOAD                5       7      
A R  CS_DEMO                    6       8      
A R  LOGO                       7       9      
A R  RATING                     8       10     
A R  DEMO                       9       11     
A R  TITLE                      10      12     
A R  TITLE_TV                   11      13     
A R  LOGO_TV                    12      14     
A R  LOGO_TERMINAL              13      15     
A R  MANUAL_TERMINAL            14      16     
A R  TITLE_TERMINAL             15      17     
A R  LOOP_TERMINAL              16      18     
A R  SELECTOR                   17      19     
A R  MODE_SELECTOR              18      20     
A R  VS                         19      21     
A R  GAMEOVER                   20      22     
- R  WORLD_STAGE_MAIN           -       23     
- R  WORLD_STAGE_TOURNAMENT     -       24     
A R  DATA_TEST_MAIN             21      25     
A R  DATA_TEST_MISC             22      26     
A R  DATA_TEST_OBJ              23      27     
A R  DATA_TEST_STG              24      28     
A R  DATA_TEST_MOT              25      29     
A R  DATA_TEST_COLLISION        26      30     
A R  DATA_TEST_SPR              27      31     
A R  DATA_TEST_AET              28      32     
A R  DATA_TEST_AUTH_3D          29      33     
A R  DATA_TEST_CHR              30      34     
A R  DATA_TEST_ITEM             31      35     
A R  DATA_TEST_PERF             32      36     
A R  DATA_TEST_TNMT             33      37     
A R  DATA_TEST_BATTLE           34      38     
A R  DATA_TEST_KOTSP_SS         35      39     
A R  MENU_MAIN                  36      40     
A R  CS_TERM_CUSTOMIZE          37      41     
A R  CS_TERM_REPLAY_PLAY        38      42     
A R  CS_TERM_LAST_PLAY          39      43     
A R  CS_TERM_CLIP_PLAY          40      44     
A R  CS_TRAINING                41      45     
A R  ONLINE_STARTUP             42      46     
A R  ONLINE_SELECTOR            43      47     
A R  ONLINE_MENU                44      48     
A R  ONLINE_MATCHING            45      49     
A R  ONLINE_GAME                46      50     
A R  ONLINE_OVER                47      51     
A R  APM3_ENTRY                 48      52     
A R  APM3_SELECTOR              49      53     
A R  APM3_GAME_VS               50      54     
A R  APM3_GAMEOVER              51      55     
A R  APM3_TRAINING              52      56     
A R  APM3_ONLINE_VS             53      57     
A R  APM3_TESTMODE_MAIN         54      58     
- R  RANK_MATCH_STARTUP         -       59     
- R  RANK_MATCH_MATCHING        -       60     
- R  RANK_MATCH_GAME            -       61     
- R  RANK_MATCH_OVER            -       62     
- R  ROOM_MATCH_STARTUP         -       63     
- R  ROOM_MATCH_MENU            -       64     
- R  ROOM_MATCH_MATCHING        -       65     
- R  ROOM_MATCH_GAME            -       66     
- R  ROOM_MATCH_OVER            -       67     
- R  TOURNAMENT_STARTUP         -       68     
- R  TOURNAMENT_MENU            -       69     
- R  TOURNAMENT_MATCHING        -       70     
- R  TOURNAMENT_GAME            -       71     
- R  TOURNAMENT_OVER            -       72     
A R  MAX                        55      73     
```

REVO ajoute 18 sous-etats, en 4 endroits :

```
apres WARNING    CROSSPLAY_WARNING  OFFLINE_WARNING                    (+2)
apres GAMEOVER   WORLD_STAGE_MAIN   WORLD_STAGE_TOURNAMENT             (+2)
avant MAX        RANK_MATCH_*  (4)  ROOM_MATCH_*  (5)  TOURNAMENT_* (5)
```

## 4. LA CONSEQUENCE QUI NOUS CONCERNE : LES NUMEROS BOUGENT

```
                        APM3   REVO
CS_TITLE                3      5      (+2)
CS_SIGNIN               4      6      (+2)
CS_DEMO                 6      8      (+2)
LOGO                    7      9      (+2)
TITLE                   10     12     (+2)
LOOP_TERMINAL           16     18     (+2)
SELECTOR                17     19     (+2)
APM3_ENTRY              48     52     (+4)
MAX                     55     73     (+18)
```

Toute la chaine de demarrage est **decalee de +2**. Un numero de sous-etat lu
dans APM3 et recopie dans un outil qui parle a REVO designe autre chose. C'est
vrai aussi pour les modes (+1 a partir de `DATA_TEST`).

## 5. CE QUI MANQUE VRAIMENT : LE CODE DU MODE APM3

Mesure par les noms de classes RTTI (`.?AV...@@` dans `.data`) :

```
APM3 : 634 noms      REVO : 772 noms      communs : 360
```

**Classes presentes dans APM3 et ABSENTES de REVO** -- le mode borne :

```
TaskApm3Entry                  (global)        l'entree en borne
TaskApm3TestMode               apm3TestMode    le test mode
TaskApmResult                  (global)        le resultat de borne
TaskTimer                      modeApm3        le compte a rebours
WaitingReadyWindow             modeApm3        l'attente du 2e joueur
MenuTop MenuBookkeep MenuGameAssign MenuGameAssignRule
MenuGameAssignRuleLocal MenuSoundSetting MenuBackupClear MenuPageBase
                               apm3TestMode    les 8 pages du test mode
```

Et toute la pile reseau de borne, `am::abaas` (ALL.Net / liaison borne a
borne) : ~45 classes `LinkMainState*`, `LinkPacket*`, `Turn*Sequencer`,
`StunChecker`, `ConnectivityChecker`, `Udp`, `LineQualityChecker`, plus
`util::Thread`, `util::crypt::Aes`, `impl::Curl`, `cs_session::PacketGate`.

**Classes ajoutees par REVO** (21 taches), dont : `TaskCsCrossplayWarning`,
`TaskCsOfflineWarning`, `TaskWorldStageManager`, `TaskTournamentManager`,
`tournament::Model::{EntryNode,MatchNode,TournamentTree}`, `replay::Task*`,
`TaskPsnServer`, `TaskRobRollback` (le netcode a rollback),
`TaskInvitationShiftScene`, `TaskTelemetryImpl`, `TaskLiveRankingUpdate`,
`TaskMultiRoomMatchMenu`, `TaskCredit`, `TaskIOConnection`,
`TaskFreepackMng`, `TaskTrnTipSelect`, `TaskTrnCharaTypeSelect`.

## 6. CE QUI RESTE DE L'ARCADE DANS REVO

Les classes des sous-etats d'arcade de DEMARRAGE sont **dans les deux** :

```
TaskTitleAdam      TaskMenuTerminal   TaskAutoLoad   TaskMovie
TaskSelector       TaskCsWarning      TaskMultiWarning
TaskMenuArcade     TaskMenuArcadeNormal   TaskMenuArcadeLicenceChallenge
```

Donc : **le demarrage d'arcade est encore compile dans REVO**. C'est le mode
APM3 (ce qui vient apres) qui a ete retire.

## 7. LES ASSETS DES CHAINES

```
                                   APM3   REVO
rom/movie/vf5adv.sfd                oui    oui
rom/movie/vf5end.sfd                oui    oui
rom/movie/vf5title_bg.sfd           oui    oui
rom/movie/vf5chara_sel_start.sfd    oui    oui
rom/movie/vf5chara_sel_loop.sfd     oui    oui
rom/movie/vf5match_sel_bg.sfd       oui    NON   <- retire par REVO
rom/movie/vf5end_us.sfd             NON    oui   <- ajoute par REVO
```

Aucun fichier `LOGO` / `RATING` / `DEMO` dans l'un ni dans l'autre : ces
sous-etats d'arcade ne lisent pas de `.sfd`.

## 8. ETABLI / NON ETABLI

CONFIRME : les deux listes de noms, les deux chemins de compilation, les
decalages d'indices, les classes RTTI presentes et absentes, les assets.

NON ETABLI : qu'un sous-etat d'arcade soit **atteignable** dans REVO. La
presence d'une classe prouve que le code est lie, pas qu'un chemin y mene. Le
repartiteur de scenes n'est pas une table plate de pointeurs (cherche :
aucune suite de 56 ni 74 pointeurs `.text`), c'est un `switch` -- il reste a
lire.
