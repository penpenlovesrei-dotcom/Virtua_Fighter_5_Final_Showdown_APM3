# La table des scenes : ou brancher le mode APM3

Mesure du 6 novembre 2026, par le motif (numero croissant, pas de 32 octets,
`fn1` dans `.text`) -- **aucun offset recopie a la main**.

```
APM3  FS APM3/banc/vf5fs-pxd-w64-Retail_APM3.dll         6 965 248 o
      table a la VA 0x1803A05A0   55 entrees   bouchon 0x180029FB0 (31 fois)
REVO  FS REVO/vf5fs-pxd-w64-d3d12_SteamRetail.dll        7 229 952 o
      table a la VA 0x1803C87F0   73 entrees   bouchon 0x180026620 (32 fois)
```

Trouvee en partant d'un fait deja etabli : `VF5FS+0xe2470` est le gestionnaire
de `SELECTOR`, et il est cite depuis `0x1803C8A60` -- qui est dans `.rdata`.

## 1. LA STRUCTURE, 32 OCTETS PAR ENTREE

```c
struct EntreeScene {          // 32 octets
    uint32_t numero;          // +0x00  le numero du sous-etat, = l'index
    uint32_t drapeau;         // +0x04  0 ou 1
    void*    fn_entree;       // +0x08
    void*    fn_maj;          // +0x10
    void*    fn_sortie;       // +0x18
};
```

Le numero a `+0x00` est egal a l'index dans tous les cas mesures (0 a 72 cote
REVO, 0 a 54 cote APM3) : c'est ce qui identifie la table sans ambiguite.

ETABLI : les trois pointeurs, leur ordre dans la structure, et que `fn_maj`
de `SELECTOR` vaut bien `0xe2470`, le gestionnaire qu'on connait deja.
LIKELY, pas mesure : que `fn_entree` et `fn_sortie` soient bien l'entree et
la sortie (la position le suggere, je ne les ai pas lues).

## 2. LE RESULTAT QUI DECIDE

**Les 7 sous-etats `APM3_*` EXISTENT dans la table de REVO, avec les bons
numeros, et leurs trois pointeurs valent tous le bouchon.**

Cote REVO -- les 7 entrees a remplacer, avec leur adresse exacte :

```
  sous-etat           n    entree de table    fn_entree  fn_maj  fn_sortie
  APM3_ENTRY          52   0x1803C8E70   0x180026620  0x180026620  0x180026620 
  APM3_SELECTOR       53   0x1803C8E90   0x180026620  0x180026620  0x180026620 
  APM3_GAME_VS        54   0x1803C8EB0   0x180026620  0x180026620  0x180026620 
  APM3_GAMEOVER       55   0x1803C8ED0   0x180026620  0x180026620  0x180026620 
  APM3_TRAINING       56   0x1803C8EF0   0x180026620  0x180026620  0x180026620 
  APM3_ONLINE_VS      57   0x1803C8F10   0x180026620  0x180026620  0x180026620 
  APM3_TESTMODE_MAIN  58   0x1803C8F30   0x180026620  0x180026620  0x180026620 
```

Cote APM3 -- l'oracle, les 21 fonctions a lire pour savoir quoi ecrire :

```
  APM3_ENTRY          48   entree 0x18023DDA0  maj 0x18023A320  sortie 0x18023C380
  APM3_SELECTOR       49   entree 0x18023E120  maj 0x18023B5E0  sortie 0x1800DBB70
  APM3_GAME_VS        50   entree 0x18023DE30  maj 0x18023A5D0  sortie 0x18023C3F0
  APM3_GAMEOVER       51   entree 0x18023DDC0  maj 0x18023A530  sortie 0x18023C390
  APM3_TRAINING       52   entree 0x18023E180  maj 0x18023B8F0  sortie 0x18023C770
  APM3_ONLINE_VS      53   entree 0x18023DF10  maj 0x18023AD10  sortie 0x18023C4B0
  APM3_TESTMODE_MAIN  54   entree 0x180241D80  maj 0x180007450  sortie 0x180241D60
```

## 3. CE QUE CA VEUT DIRE POUR LA REINTEGRATION

Le point d'accroche n'est pas du code a rapiecer : c'est **21 pointeurs a
ecrire**, 3 par sous-etat, dans `.rdata` (donc `VirtualProtect` d'abord). Nos
fonctions prennent la place du bouchon, le module les appelle comme il
appellerait les siennes.

C'est beaucoup plus propre que ce que je croyais au SS 294 : SEGA a laisse les
emplacements en place.

## 4. UN AUTRE FAIT, QUI CORRIGE UNE IDEE RECUE

**`LOGO`, `RATING`, `DEMO`, `TITLE`, `TITLE_TV`, `LOGO_TV`, et les quatre
`*_TERMINAL` sont BOUCHONNES DANS LES DEUX MODULES.** Pas seulement dans REVO :
dans APM3 aussi, celui qui tourne sur une borne.

Donc ces dix sous-etats ne sont pas « la chaine de demarrage d'arcade » : ce
sont des restes d'une variante de borne que ce code-la n'utilise pas. APM3
demarre par `CS_TITLE` / `CS_DEMO` comme REVO, puis entre dans `APM3_ENTRY`.
Ma formule du SS 292-293, « le demarrage d'arcade est encore compile », etait
donc trop genereuse : il n'a jamais ete compile, ni ici ni la.

Autres bouchonnes des deux cotes : les 15 `DATA_TEST_*`.
Bouchonnes differemment dans REVO : les 6 `ONLINE_*` pointent tous
`0x18000BA20`, pas le bouchon ordinaire.

## 5. LA TABLE DE REVO EN ENTIER (VA 0x1803C87F0)

```
n   sous-etat                  drap fn_entree    fn_maj       fn_sortie     etat
0   DATA_INITIALIZE            1  0x1800E64E0  0x1800E56B0  0x1800E5B20   reel
1   SYSTEM_STARTUP             1  0x1800E6580  0x1800E58A0  0x1800E5BC0   reel
2   WARNING                    1  0x1800E6660  0x1800E58C0  0x1800E5C00   reel
3   CROSSPLAY_WARNING          1  0x1800E5D20  0x1800E54D0  0x1800E59A0   reel
4   OFFLINE_WARNING            1  0x1800E64F0  0x1800E56C0  0x1800E5B60   reel
5   CS_TITLE                   0  0x1800E5ED0  0x1800E55B0  0x1800E5A20   reel
6   CS_SIGNIN                  0  0x1800E5E50  0x1800E5570  0x180026620   reel
7   CS_AUTOLOAD                0  0x1800E5D40  0x1800E54F0  0x1800E59C0   reel
8   CS_DEMO                    0  0x1800E5D70  0x1800E5510  0x1800E59F0   reel
9   LOGO                       1  0x180026620  0x180026620  0x180026620   BOUCHON
10  RATING                     1  0x180026620  0x180026620  0x180026620   BOUCHON
11  DEMO                       1  0x180026620  0x180026620  0x180026620   BOUCHON
12  TITLE                      1  0x180026620  0x180026620  0x180026620   BOUCHON
13  TITLE_TV                   1  0x180026620  0x180026620  0x180026620   BOUCHON
14  LOGO_TV                    1  0x180026620  0x180026620  0x180026620   BOUCHON
15  LOGO_TERMINAL              1  0x180026620  0x180026620  0x180026620   BOUCHON
16  MANUAL_TERMINAL            1  0x180026620  0x180026620  0x180026620   BOUCHON
17  TITLE_TERMINAL             1  0x180026620  0x180026620  0x180026620   BOUCHON
18  LOOP_TERMINAL              1  0x180026620  0x180026620  0x180026620   BOUCHON
19  SELECTOR                   1  0x1800E3F90  0x1800E2470  0x1800E2F60   reel
20  MODE_SELECTOR              1  0x1800E3F70  0x1800E2010  0x1800E2F40   reel
21  VS                         1  0x1800E3D70  0x1800E1C20  0x1800E2CE0   reel
22  GAMEOVER                   1  0x1800E3D40  0x1800E1BC0  0x1800E2B70   reel
23  WORLD_STAGE_MAIN           1  0x18000B830  0x18000B3D0  0x18000B4F0   reel
24  WORLD_STAGE_TOURNAMENT     1  0x18000B860  0x18000B3D0  0x18000B510   reel
25  DATA_TEST_MAIN             1  0x180026620  0x180026620  0x180026620   BOUCHON
26  DATA_TEST_MISC             1  0x180026620  0x180026620  0x180026620   BOUCHON
27  DATA_TEST_OBJ              0  0x180026620  0x180026620  0x180026620   BOUCHON
28  DATA_TEST_STG              0  0x180026620  0x180026620  0x180026620   BOUCHON
29  DATA_TEST_MOT              0  0x180026620  0x180026620  0x180026620   BOUCHON
30  DATA_TEST_COLLISION        1  0x180026620  0x180026620  0x180026620   BOUCHON
31  DATA_TEST_SPR              1  0x180026620  0x180026620  0x180026620   BOUCHON
32  DATA_TEST_AET              1  0x180026620  0x180026620  0x180026620   BOUCHON
33  DATA_TEST_AUTH_3D          1  0x180026620  0x180026620  0x180026620   BOUCHON
34  DATA_TEST_CHR              0  0x180026620  0x180026620  0x180026620   BOUCHON
35  DATA_TEST_ITEM             1  0x180026620  0x180026620  0x180026620   BOUCHON
36  DATA_TEST_PERF             1  0x180026620  0x180026620  0x180026620   BOUCHON
37  DATA_TEST_TNMT             1  0x180026620  0x180026620  0x180026620   BOUCHON
38  DATA_TEST_BATTLE           1  0x180026620  0x180026620  0x180026620   BOUCHON
39  DATA_TEST_KOTSP_SS         0  0x180026620  0x180026620  0x180026620   BOUCHON
40  MENU_MAIN                  1  0x1800E4210  0x18000BA20  0x1800E4130   reel
41  CS_TERM_CUSTOMIZE          1  0x180211F90  0x180211A80  0x180211E90   reel
42  CS_TERM_REPLAY_PLAY        1  0x180212020  0x180211D10  0x180026620   reel
43  CS_TERM_LAST_PLAY          1  0x180211FD0  0x180211B20  0x180211EB0   reel
44  CS_TERM_CLIP_PLAY          1  0x180211F80  0x1802119C0  0x180211E40   reel
45  CS_TRAINING                1  0x180212140  0x180212070  0x1802120D0   reel
46  ONLINE_STARTUP             1  0x18000BA20  0x18000BA20  0x18000BA20   reel
47  ONLINE_SELECTOR            1  0x18000BA20  0x18000BA20  0x18000BA20   reel
48  ONLINE_MENU                1  0x18000BA20  0x18000BA20  0x18000BA20   reel
49  ONLINE_MATCHING            1  0x18000BA20  0x18000BA20  0x18000BA20   reel
50  ONLINE_GAME                1  0x18000BA20  0x18000BA20  0x18000BA20   reel
51  ONLINE_OVER                1  0x18000BA20  0x18000BA20  0x18000BA20   reel
52  APM3_ENTRY                 1  0x180026620  0x180026620  0x180026620   BOUCHON
53  APM3_SELECTOR              1  0x180026620  0x180026620  0x180026620   BOUCHON
54  APM3_GAME_VS               1  0x180026620  0x180026620  0x180026620   BOUCHON
55  APM3_GAMEOVER              1  0x180026620  0x180026620  0x180026620   BOUCHON
56  APM3_TRAINING              1  0x180026620  0x180026620  0x180026620   BOUCHON
57  APM3_ONLINE_VS             1  0x180026620  0x180026620  0x180026620   BOUCHON
58  APM3_TESTMODE_MAIN         1  0x180026620  0x180026620  0x180026620   BOUCHON
59  RANK_MATCH_STARTUP         1  0x180218720  0x180213F70  0x180215780   reel
60  RANK_MATCH_MATCHING        1  0x1802183C0  0x1802135D0  0x1802156A0   reel
61  RANK_MATCH_GAME            1  0x180218230  0x180213170  0x1802155D0   reel
62  RANK_MATCH_OVER            1  0x1802184A0  0x180213CF0  0x1802156F0   reel
63  ROOM_MATCH_STARTUP         1  0x180218720  0x180214A80  0x180215D90   reel
64  ROOM_MATCH_MENU            1  0x180218C80  0x180214760  0x180026620   reel
65  ROOM_MATCH_MATCHING        1  0x180218BA0  0x1802145F0  0x180215AC0   reel
66  ROOM_MATCH_GAME            1  0x180218980  0x1802140E0  0x180215970   reel
67  ROOM_MATCH_OVER            1  0x180218CD0  0x180214A20  0x180215B00   reel
68  TOURNAMENT_STARTUP         1  0x180218720  0x180215380  0x180215D90   reel
69  TOURNAMENT_MENU            1  0x180219230  0x1802151D0  0x180026620   reel
70  TOURNAMENT_MATCHING        1  0x180219150  0x1802150B0  0x1802160B0   reel
71  TOURNAMENT_GAME            1  0x180218F30  0x180214BE0  0x180215F80   reel
72  TOURNAMENT_OVER            1  0x180219280  0x180215320  0x1802160E0   reel
```

## 6. LA TABLE D'APM3 EN ENTIER (VA 0x1803A05A0)

```
n   sous-etat                  drap fn_entree    fn_maj       fn_sortie     etat
0   DATA_INITIALIZE            1  0x1800DE3A0  0x1800DD6D0  0x1800DDA00   reel
1   SYSTEM_STARTUP             1  0x1800DE430  0x1800DD790  0x1800DDA80   reel
2   WARNING                    1  0x1800DE510  0x1800DD7C0  0x1800DDAF0   reel
3   CS_TITLE                   0  0x1800DDE00  0x1800DD600  0x1800DD930   reel
4   CS_SIGNIN                  0  0x1800DDDC0  0x1800DD5C0  0x180029FB0   reel
5   CS_AUTOLOAD                0  0x1800DDC10  0x1800DD4D0  0x1800DD880   reel
6   CS_DEMO                    0  0x1800DDC40  0x1800DD4F0  0x1800DD8B0   reel
7   LOGO                       1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
8   RATING                     1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
9   DEMO                       1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
10  TITLE                      1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
11  TITLE_TV                   1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
12  LOGO_TV                    1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
13  LOGO_TERMINAL              1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
14  MANUAL_TERMINAL            1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
15  TITLE_TERMINAL             1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
16  LOOP_TERMINAL              1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
17  SELECTOR                   1  0x1800DCA90  0x1800DB270  0x1800DBB70   reel
18  MODE_SELECTOR              1  0x1800DCA70  0x1800DAE20  0x1800DBB50   reel
19  VS                         1  0x1800DC890  0x1800DAAC0  0x1800DBAC0   reel
20  GAMEOVER                   1  0x1800DC860  0x1800DAA60  0x1800DB950   reel
21  DATA_TEST_MAIN             1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
22  DATA_TEST_MISC             1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
23  DATA_TEST_OBJ              0  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
24  DATA_TEST_STG              0  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
25  DATA_TEST_MOT              0  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
26  DATA_TEST_COLLISION        1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
27  DATA_TEST_SPR              1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
28  DATA_TEST_AET              1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
29  DATA_TEST_AUTH_3D          1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
30  DATA_TEST_CHR              0  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
31  DATA_TEST_ITEM             1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
32  DATA_TEST_PERF             1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
33  DATA_TEST_TNMT             1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
34  DATA_TEST_BATTLE           1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
35  DATA_TEST_KOTSP_SS         0  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
36  MENU_MAIN                  1  0x1800DCCA0  0x180007450  0x1800DCBE0   reel
37  CS_TERM_CUSTOMIZE          1  0x1801E50B0  0x1801E4ED0  0x1801E4FF0   reel
38  CS_TERM_REPLAY_PLAY        1  0x1801E50A0  0x1801E4EC0  0x1801E4FE0   reel
39  CS_TERM_LAST_PLAY          1  0x1801E50A0  0x1801E4EC0  0x1801E4FE0   reel
40  CS_TERM_CLIP_PLAY          1  0x1801E50A0  0x1801E4EC0  0x1801E4FE0   reel
41  CS_TRAINING                1  0x1801E51A0  0x1801E50F0  0x1801E5140   reel
42  ONLINE_STARTUP             1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
43  ONLINE_SELECTOR            1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
44  ONLINE_MENU                1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
45  ONLINE_MATCHING            1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
46  ONLINE_GAME                1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
47  ONLINE_OVER                1  0x180029FB0  0x180029FB0  0x180029FB0   BOUCHON
48  APM3_ENTRY                 1  0x18023DDA0  0x18023A320  0x18023C380   reel
49  APM3_SELECTOR              1  0x18023E120  0x18023B5E0  0x1800DBB70   reel
50  APM3_GAME_VS               1  0x18023DE30  0x18023A5D0  0x18023C3F0   reel
51  APM3_GAMEOVER              1  0x18023DDC0  0x18023A530  0x18023C390   reel
52  APM3_TRAINING              1  0x18023E180  0x18023B8F0  0x18023C770   reel
53  APM3_ONLINE_VS             1  0x18023DF10  0x18023AD10  0x18023C4B0   reel
54  APM3_TESTMODE_MAIN         1  0x180241D80  0x180007450  0x180241D60   reel
```

## 7. CE QUI RESTE A MESURER

1. **La table des MODES.** Il faut que le mode `APM3` (numero **9** dans REVO,
   8 dans APM3) soit atteignable. Une table par mode existe probablement sur
   le meme principe ; elle n'est pas encore cherchee.
2. **Qui ecrit le numero de sous-etat.** Les emplacements existent ; encore
   faut-il que quelque chose demande `APM3_ENTRY`. Dans REVO ce quelque chose
   est parti avec le code.
3. **Les 21 fonctions d'APM3**, a lire une par une.
4. **Le drapeau a `+0x04`** : 0 ou 1 selon l'entree, sens inconnu.
