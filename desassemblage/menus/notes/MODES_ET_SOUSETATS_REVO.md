# Modes et sous-etats du module R.E.V.O.

> **OU SONT LES ADRESSES ET LE VIDAGE (SS 379).** Ce fichier ne porte que les
> NOMS. Les trois gestionnaires de phase de chaque ligne, leur etat de vidage
> et les fichiers `.c` sont dans **`code_decompile/CHAINE_DEMARRAGE.md`**,
> genere par **`py -3 VF5RE\chaines_des_modes.py --md`**. Les noms ci-dessous
> sont d'ailleurs lisibles dans le binaire : `0x3C9110` (15 pointeurs, modes)
> et `0x3C9190` (74 pointeurs, sous-etats). **Ne pas ouvrir un troisieme
> fichier sur le meme sujet.**


Lu dans `vf5fs-pxd-w64-d3d12_SteamRetail.dll` le 6 novembre 2026.
Tables de noms du module : **0x3C9110** (15 modes) et **0x3C9190** (73 sous-etats). Dumpe par script depuis le PE -- aucun offset recopie a la main.

Chemin de compilation grave dans le binaire :

```
?D:/Project/vf5/vf5fscs_source/20120711_update_1.1/vf5fs
```

Donc : source **console** (`vf5fs`**cs**`_source`) du 11 juillet 2012, update 1.1.

ANCRES VERIFIEES contre nos propres journaux : modes 0=STARTUP, 2=GAME, 5=MENU ; sous-etats 0=DATA_INITIALIZE, 1=SYSTEM_STARTUP, 5=CS_TITLE, 6=CS_SIGNIN, 8=CS_DEMO, 19=SELECTOR, 20=MODE_SELECTOR. Si une seule tombe, la table est fausse.

> **CORRECTION DU 6 NOVEMBRE 2026.** Les etiquettes de ce fichier etaient
> fausses : j'avais ecrit « console (FS d'origine) » et « ajout R.E.V.O. » en
> le DEDUISANT des noms. Mesure faite depuis :
> `vf5fs-pxd-w64-Retail_APM3.dll` porte **lui aussi** `CS_TITLE`, `CS_DEMO`,
> `LOGO`, `TITLE_TERMINAL` et `APM3_SELECTOR`, et le **meme** chemin de
> compilation `vf5fscs_source/20120711_update_1.1`. Les deux chaines sont dans
> les DEUX modules ; REVO n'est pas une troisieme chaine. Les seuls vrais
> ajouts de l'ere REVO sont `CROSSPLAY_WARNING`, `OFFLINE_WARNING`,
> `WORLD_STAGE_*`, `RANK_MATCH_*`, `ROOM_MATCH_*`, `TOURNAMENT_*` et les modes
> `WORLD_STAGE`, `RANK_MATCH`, `ROOM_MATCH`, `TOURNAMENT`.
> Colonne : `A` = dans APM3, `R` = dans REVO.
> **Les numeros de ce fichier sont ceux de REVO. Ceux d'APM3 sont decales de
> -2 sur toute la chaine de demarrage.** Comparaison complete :
> `VF5RE/CHAINES_DEMARRAGE_APM3_VS_REVO.md`.

## Les 15 modes (0x3C9110)

```
 0  STARTUP                
 1  ADVERTISE              
 2  GAME                   
 3  WORLD_STAGE              R    ajout REVO (absent d'APM3)
 4  DATA_TEST              
 5  MENU                   
 6  CS_TERM                A+R  demarrage console
 7  CS_TRAINING            A+R  demarrage console
 8  ONLINE                 en ligne
 9  APM3                   A+R  nom APM3 (code RETIRE de REVO)
10  APM3_TESTMODE          A+R  nom APM3 (code RETIRE de REVO)
11  RANK_MATCH               R    ajout REVO (absent d'APM3)
12  ROOM_MATCH               R    ajout REVO (absent d'APM3)
13  TOURNAMENT               R    ajout REVO (absent d'APM3)
14  MAX                    
```

## Les 74 sous-etats (0 a 73) (0x3C9190)

```
 0  DATA_INITIALIZE          
 1  SYSTEM_STARTUP           
 2  WARNING                  
 3  CROSSPLAY_WARNING        R    ajout REVO (absent d'APM3)
 4  OFFLINE_WARNING          R    ajout REVO (absent d'APM3)
 5  CS_TITLE                 A+R  demarrage console
 6  CS_SIGNIN                A+R  demarrage console
 7  CS_AUTOLOAD              A+R  demarrage console
 8  CS_DEMO                  A+R  demarrage console
 9  LOGO                     A+R  demarrage arcade
10  RATING                   A+R  demarrage arcade
11  DEMO                     A+R  demarrage arcade
12  TITLE                    A+R  demarrage arcade
13  TITLE_TV                 A+R  demarrage arcade
14  LOGO_TV                  A+R  demarrage arcade
15  LOGO_TERMINAL            A+R  demarrage arcade
16  MANUAL_TERMINAL          A+R  demarrage arcade
17  TITLE_TERMINAL           A+R  demarrage arcade
18  LOOP_TERMINAL            A+R  demarrage arcade
19  SELECTOR                 
20  MODE_SELECTOR            
21  VS                       
22  GAMEOVER                 
23  WORLD_STAGE_MAIN         R    ajout REVO (absent d'APM3)
24  WORLD_STAGE_TOURNAMENT   R    ajout REVO (absent d'APM3)
25  DATA_TEST_MAIN           
26  DATA_TEST_MISC           
27  DATA_TEST_OBJ            
28  DATA_TEST_STG            
29  DATA_TEST_MOT            
30  DATA_TEST_COLLISION      
31  DATA_TEST_SPR            
32  DATA_TEST_AET            
33  DATA_TEST_AUTH_3D        
34  DATA_TEST_CHR            
35  DATA_TEST_ITEM           
36  DATA_TEST_PERF           
37  DATA_TEST_TNMT           
38  DATA_TEST_BATTLE         
39  DATA_TEST_KOTSP_SS       
40  MENU_MAIN                
41  CS_TERM_CUSTOMIZE        A+R  demarrage console
42  CS_TERM_REPLAY_PLAY      A+R  demarrage console
43  CS_TERM_LAST_PLAY        A+R  demarrage console
44  CS_TERM_CLIP_PLAY        A+R  demarrage console
45  CS_TRAINING              A+R  demarrage console
46  ONLINE_STARTUP           en ligne
47  ONLINE_SELECTOR          en ligne
48  ONLINE_MENU              en ligne
49  ONLINE_MATCHING          en ligne
50  ONLINE_GAME              en ligne
51  ONLINE_OVER              en ligne
52  APM3_ENTRY               A+R  nom APM3 (code RETIRE de REVO)
53  APM3_SELECTOR            A+R  nom APM3 (code RETIRE de REVO)
54  APM3_GAME_VS             A+R  nom APM3 (code RETIRE de REVO)
55  APM3_GAMEOVER            A+R  nom APM3 (code RETIRE de REVO)
56  APM3_TRAINING            A+R  nom APM3 (code RETIRE de REVO)
57  APM3_ONLINE_VS           A+R  nom APM3 (code RETIRE de REVO)
58  APM3_TESTMODE_MAIN       A+R  nom APM3 (code RETIRE de REVO)
59  RANK_MATCH_STARTUP       R    ajout REVO (absent d'APM3)
60  RANK_MATCH_MATCHING      R    ajout REVO (absent d'APM3)
61  RANK_MATCH_GAME          R    ajout REVO (absent d'APM3)
62  RANK_MATCH_OVER          R    ajout REVO (absent d'APM3)
63  ROOM_MATCH_STARTUP       R    ajout REVO (absent d'APM3)
64  ROOM_MATCH_MENU          R    ajout REVO (absent d'APM3)
65  ROOM_MATCH_MATCHING      R    ajout REVO (absent d'APM3)
66  ROOM_MATCH_GAME          R    ajout REVO (absent d'APM3)
67  ROOM_MATCH_OVER          R    ajout REVO (absent d'APM3)
68  TOURNAMENT_STARTUP       R    ajout REVO (absent d'APM3)
69  TOURNAMENT_MENU          R    ajout REVO (absent d'APM3)
70  TOURNAMENT_MATCHING      R    ajout REVO (absent d'APM3)
71  TOURNAMENT_GAME          R    ajout REVO (absent d'APM3)
72  TOURNAMENT_OVER          R    ajout REVO (absent d'APM3)
73  MAX                      
```

## Les DEUX chaines de demarrage

```
A+R  demarrage console :  CS_AUTOLOAD  CS_TITLE  CS_SIGNIN  CS_DEMO
A+R  demarrage arcade         :  LOGO  RATING  DEMO  TITLE  TITLE_TV
                          LOGO_TV  LOGO_TERMINAL  MANUAL_TERMINAL
                          TITLE_TERMINAL  LOOP_TERMINAL
```

**Celle qu'on execute, mesuree** (`host_log_s290_attract.txt`) :

```
DATA_INITIALIZE -> SYSTEM_STARTUP -> CS_DEMO -> CS_TITLE -> SELECTOR
```

C'est la chaine **console**. Aucun `APM3_*`, aucun `LOGO`/`RATING`/
`TITLE` d'arcade n'a jamais ete vu dans un de nos journaux.

`CROSSPLAY_WARNING` et `OFFLINE_WARNING` n'existaient pas dans le FS
de 2012 : ce sont des ajouts de l'ere R.E.V.O.
