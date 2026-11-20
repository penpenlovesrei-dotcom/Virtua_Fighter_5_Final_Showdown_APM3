# Carte de la zone 0x1801C0000 - 0x1801D2000 (customize)

312 fonctions, 68363 octets de code.

Genere par `tools/carte_zone.py`. Pour chaque fonction : sa taille, ses appelants **internes a la zone**, les chaines qu'elle nomme, les globaux connus qu'elle lit, et les immediats remarquables.

## 0x1801C0220  (778 octets, 232 instructions)
- appelee par : 0x1801C0BD0

## 0x1801C0530  (320 octets, 92 instructions)
- appelee par : 0x1801C07B0

## 0x1801C0670  (320 octets, 92 instructions)
- appelee par : 0x1801C0BD0

## 0x1801C07B0  (1053 octets, 284 instructions)
- appelee par : 0x1801C07B0, 0x1801C2920
- appelle (dans la zone) : 0x1801C0530, 0x1801C07B0

## 0x1801C0BD0  (1069 octets, 285 instructions)
- appelee par : 0x1801C0BD0, 0x1801C21C0, 0x1801C2640
- appelle (dans la zone) : 0x1801C0220, 0x1801C0670, 0x1801C0BD0

## 0x1801C1000  (202 octets, 55 instructions)
- appelee par : 0x1801C21C0

## 0x1801C1100  (176 octets, 47 instructions)
- appelee par : 0x1801BF3D0, 0x1801BFAC0

## 0x1801C11B0  (36 octets, 10 instructions)
- appelee par : 0x1801BF78E, 0x18033BA40

## 0x1801C11E0  (94 octets, 27 instructions)
- appelee par : 0x1801C11E0, 0x1801C12F0, 0x1801C5810
- appelle (dans la zone) : 0x1801C11E0

## 0x1801C1240  (45 octets, 14 instructions)
- appelee par : 0x18033BAA6, 0x18033BB41

## 0x1801C1270  (116 octets, 32 instructions)
- appelee par : 0x1801BEFC0, 0x1801BF3D0, 0x1801BFAC0

## 0x1801C12F0  (150 octets, 41 instructions)
- appelee par : 0x1801C1730, 0x1801C21C0
- appelle (dans la zone) : 0x1801C11E0

## 0x1801C13B0  (893 octets, 200 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3830, 0x1801C42B0, 0x1801C4BD0, 0x1801C5AB0, 0x1801CE1F0, 0x1801CE400

## 0x1801C1730  (417 octets, 71 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C12F0

## 0x1801C19C0  (16 octets, 6 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C19D0  (104 octets, 23 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C1A38  (1 octets, 1 instructions)  **BOUCHON**
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C1BA0  (148 octets, 28 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- chaines : `CUST_EQUIP`

## 0x1801C1C34  (49 octets, 14 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C1C65  (20 octets, 6 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C1C80  (601 octets, 151 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C1EE0, 0x1801C21C0, 0x1801C2640

## 0x1801C1EE0  (722 octets, 200 instructions)
- appelee par : 0x1801C1C80
- **scenes** : 0x150=SELSTG_WXGA

## 0x1801C21C0  (1145 octets, 310 instructions)
- appelee par : 0x1801C1C80
- appelle (dans la zone) : 0x1801C0BD0, 0x1801C1000, 0x1801C12F0

## 0x1801C2640  (729 octets, 188 instructions)
- appelee par : 0x1801C1C80
- appelle (dans la zone) : 0x1801C0BD0

## 0x1801C2920  (708 octets, 166 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C07B0, 0x1801C5AB0
- immediats : mov 19 = DURAL

## 0x1801C2BF0  (316 octets, 75 instructions)
- appelee par : 0x1801C31A0, 0x1801C33A0, 0x1801C3950, 0x1801C3AE0, 0x1801C3C80

## 0x1801C2E10  (164 octets, 34 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3A00

## 0x1801C2EC0  (321 octets, 73 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3D60, 0x1801C5C50, 0x1801C5DB0

## 0x1801C3010  (122 octets, 31 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C5C50, 0x1801C5D60

## 0x1801C3090  (94 octets, 29 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- **appelle des bouchons** : 0x180007430

## 0x1801C30F0  (80 octets, 19 instructions)
- appelee par : 0x1801C7890
- appelle (dans la zone) : 0x1801C5AB0, 0x1801CE200

## 0x1801C3140  (96 octets, 24 instructions)
- appelee par : 0x1801C8422
- appelle (dans la zone) : 0x1801C5AB0, 0x1801CE200

## 0x1801C31A0  (227 octets, 55 instructions)
- appelee par : 0x1801C6FB1
- appelle (dans la zone) : 0x1801C2BF0, 0x1801C4BD0, 0x1801C5BD0, 0x1801C5C50

## 0x1801C3290  (171 octets, 42 instructions)
- appelee par : 0x1801C6FB1
- appelle (dans la zone) : 0x1801C4BD0

## 0x1801C3350  (75 octets, 20 instructions)
- appelee par : 0x1801C4E02
- chaines : `CUST_MAIN`

## 0x1801C33A0  (181 octets, 42 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C2BF0, 0x1801C4BD0

## 0x1801C3460  (21 octets, 5 instructions)
- appelee par : 0x1801C8A40, 0x1801C96C0, 0x1801CA410, 0x1801CA620, 0x1801CB030, 0x1801CC313, 0x1801CC45F, 0x1801CC960
- appelle (dans la zone) : 0x1801C5AB0

## 0x1801C34E0  (49 octets, 15 instructions)
- appelee par : 0x1801DC620
- appelle (dans la zone) : 0x1801D0090

## 0x1801C3511  (141 octets, 43 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801CFDE0

## 0x1801C359E  (17 octets, 6 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801CFFB0

## 0x1801C35AF  (114 octets, 25 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C4BD0, 0x1801C5A80

## 0x1801C3621  (27 octets, 7 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C363C  (17 octets, 5 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C3670  (146 octets, 33 instructions)
- appelee par : 0x1801C8110, 0x1801CBAD0
- appelle (dans la zone) : 0x1801C4B40, 0x1801C5AB0, 0x1801CE080

## 0x1801C3720  (80 octets, 20 instructions)
- appelee par : 0x1801CC960, 0x1801CCD70
- appelle (dans la zone) : 0x1801C5AB0

## 0x1801C3780  (169 octets, 51 instructions)
- appelee par : 0x1801CAC10

## 0x1801C3840  (133 octets, 31 instructions)
- appelee par : 0x1801CA620, 0x1801CAC10, 0x1801CC245
- appelle (dans la zone) : 0x1801C4B40, 0x1801C5AB0, 0x1801CE210

## 0x1801C38D0  (32 octets, 9 instructions)
- appelee par : 0x1801CBB80
- appelle (dans la zone) : 0x1801C5AB0

## 0x1801C3900  (80 octets, 19 instructions)
- appelee par : 0x1801C7890
- appelle (dans la zone) : 0x1801C5AB0, 0x1801CE200

## 0x1801C3950  (167 octets, 38 instructions)
- appelee par : 0x1801C7B50, 0x1801C7D00
- appelle (dans la zone) : 0x1801C2BF0, 0x1801C4B40

## 0x1801C3A00  (104 octets, 23 instructions)
- appelee par : 0x1801C2E10, 0x1801C3D71
- appelle (dans la zone) : 0x1801C5AB0, 0x1801CE200

## 0x1801C3A70  (104 octets, 24 instructions)
- appelee par : 0x1801C7890
- appelle (dans la zone) : 0x1801C5AB0, 0x1801CE200

## 0x1801C3AE0  (177 octets, 42 instructions)
- appelee par : 0x1801CAE71
- appelle (dans la zone) : 0x1801C2BF0, 0x1801C4BD0

## 0x1801C3BA0  (80 octets, 19 instructions)
- appelee par : 0x1801C7890
- appelle (dans la zone) : 0x1801C5AB0, 0x1801CE200

## 0x1801C3BF0  (18 octets, 6 instructions)
- appelee par : 0x1801C7890

## 0x1801C3C02  (55 octets, 13 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C5AB0, 0x1801CE200

## 0x1801C3C39  (6 octets, 3 instructions)  **BOUCHON**
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C3C40  (47 octets, 14 instructions)
- appelee par : 0x1801CAEC0
- appelle (dans la zone) : 0x1801C5C50, 0x1801CE370

## 0x1801C3C80  (173 octets, 38 instructions)
- appelee par : 0x1801CAC10
- appelle (dans la zone) : 0x1801C2BF0, 0x1801C4B40, 0x1801C5AB0, 0x1801CDD40

## 0x1801C3D60  (17 octets, 5 instructions)
- appelee par : 0x1801C2EC0

## 0x1801C3D71  (1184 octets, 250 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3A00, 0x1801C59B0, 0x1801C5AB0, 0x1801C5BD0, 0x1801C5C50, 0x1801C6EB0, 0x1801C7A90, 0x1801CB020, 0x1801CBCE0, 0x1801CBD10, 0x1801CD1B0, 0x1801CD880, 0x1801CDCD0, 0x1801CE370, 0x1801CE4F0, 0x1801CFD60, 0x1801CFDA0, 0x1801CFE90, 0x1801D0170, 0x1801D0720
- immediats : mov 20 = ALEATOIRE, cmp 21 = aucun

## 0x1801C4211  (158 octets, 12 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801CDA80

## 0x1801C42B0  (13 octets, 5 instructions)
- appelee par : 0x1801C13B0

## 0x1801C42BD  (59 octets, 14 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C4BD0

## 0x1801C42F8  (1 octets, 1 instructions)  **BOUCHON**
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C4300  (353 octets, 86 instructions)
- appelee par : 0x1801C4580
- appelle (dans la zone) : 0x1801C5810

## 0x1801C4470  (174 octets, 48 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- **appelle des bouchons** : 0x180007430

## 0x1801C4520  (83 octets, 21 instructions)
- appelee par : 0x1802441A0
- appelle (dans la zone) : 0x1801CD430

## 0x1801C4580  (63 octets, 16 instructions)
- appelee par : 0x180244410
- appelle (dans la zone) : 0x1801C4300

## 0x1801C45C0  (152 octets, 32 instructions)
- appelee par : 0x1802441A0

## 0x1801C4660  (42 octets, 10 instructions)
- appelee par : 0x180244410

## 0x1801C4690  (83 octets, 22 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C46F0  (1101 octets, 274 instructions)
- appelee par : 0x1801C5B00

## 0x1801C4C90  (193 octets, 50 instructions)
- appelee par : 0x1801CF42A
- chaines : `%s_%03d`
- immediats : mov 21 = aucun

## 0x1801C4D60  (162 octets, 44 instructions)
- appelee par : 0x1801E4ED0
- chaines : `STAGE_TASK`

## 0x1801C4E02  (58 octets, 15 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3350, 0x1801C3830

## 0x1801C4E3C  (201 octets, 51 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3830
- chaines : `rom/sound/bgm/vfes_bgm_cus.adx`

## 0x1801C4F10  (155 octets, 36 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- **appelle des bouchons** : 0x180029FB0

## 0x1801C4FAB  (74 octets, 17 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- immediats : mov 21 = aucun

## 0x1801C4FF5  (102 octets, 26 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C5060  (221 octets, 54 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801CD1B0
- **appelle des bouchons** : 0x180007430, 0x180007440
- immediats : mov 20 = ALEATOIRE

## 0x1801C5140  (53 octets, 15 instructions)
- appelee par : 0x1801E4FF0
- appelle (dans la zone) : 0x1801C3830, 0x1801CD850, 0x1801CDCD0

## 0x1801C5180  (34 octets, 10 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C51B0  (910 octets, 187 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C5540
- chaines : `p_small_head_lt`, `p_txt_01_lt`, `p_txt_03_rt`, `%s`
- **scenes** : 0x150=SELSTG_WXGA
- immediats : mov 18 (borne de roster)

## 0x1801C5540  (707 octets, 146 instructions)
- appelee par : 0x1801C51B0
- chaines : `p_txt_term_name_c`, `%s`, `p_txt_term_chara_name_c`, `p_term_chara_icon_c`, `p_txt_term_cos_plt_c`
- immediats : mov 18 (borne de roster)

## 0x1801C5810  (407 octets, 115 instructions)
- appelee par : 0x1801C4300, 0x1801CD690
- appelle (dans la zone) : 0x1801C10E0, 0x1801C11E0

## 0x1801C59B0  (131 octets, 36 instructions)
- appelee par : 0x1801C3D71, 0x1801CF03B

## 0x1801C5A40  (59 octets, 20 instructions)
- appelee par : 0x1801CF2D0

## 0x1801C5A80  (46 octets, 14 instructions)
- appelee par : 0x18016E390, 0x1801C35AF, 0x1801CF42A, 0x1801D0AF5, 0x1801E5BAA

## 0x1801C5AC0  (59 octets, 17 instructions)
- appelee par : 0x1801DD7A0
- immediats : mov 21 = aucun

## 0x1801C5B00  (64 octets, 17 instructions)
- appelee par : 0x1801E50B0
- appelle (dans la zone) : 0x1801C46F0, 0x1801CE300

## 0x1801C5B40  (135 octets, 29 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C5BD0  (125 octets, 27 instructions)
- appelee par : 0x1801C31A0, 0x1801C3D71
- appelle (dans la zone) : 0x1801CD7E0
- immediats : cmp 21 = aucun

## 0x1801C5C80  (35 octets, 7 instructions)
- appelee par : 0x1801DD7A0, 0x1801E4300
- chaines : `CUSTOMIZE MENU`

## 0x1801C5CB0  (159 octets, 42 instructions)
- appelee par : 0x1801B9230

## 0x1801C5D60  (68 octets, 18 instructions)
- appelee par : 0x1801C3010

## 0x1801C5DB0  (384 octets, 76 instructions)
- appelee par : 0x1801C2EC0

## 0x1801C5F40  (16 octets, 5 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C6060  (492 octets, 96 instructions)
- appelee par : 0x1801C6C10
- appelle (dans la zone) : 0x1801C5F50

## 0x1801C6250  (124 octets, 25 instructions)
- appelee par : 0x1801C65A0, 0x1801C6600

## 0x1801C62D0  (88 octets, 19 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C6330  (88 octets, 19 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C6390  (102 octets, 24 instructions)
- appelee par : 0x1801C6850, 0x1801C68B0

## 0x1801C63F6  (270 octets, 50 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C6504  (6 octets, 2 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C6510  (133 octets, 39 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- **appelle des bouchons** : 0x180007430

## 0x1801C65A0  (94 octets, 29 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C6250
- **appelle des bouchons** : 0x180007430

## 0x1801C6600  (226 octets, 60 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C6250
- **appelle des bouchons** : 0x180007430

## 0x1801C66F0  (174 octets, 48 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- **appelle des bouchons** : 0x180007430

## 0x1801C67A0  (174 octets, 48 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- **appelle des bouchons** : 0x180007430

## 0x1801C6850  (94 octets, 29 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C6390
- **appelle des bouchons** : 0x180007430

## 0x1801C68B0  (258 octets, 67 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C6390
- **appelle des bouchons** : 0x180007430

## 0x1801C69C0  (213 octets, 41 instructions)
- appelee par : 0x1802441A0

## 0x1801C6AA0  (42 octets, 10 instructions)
- appelee par : 0x180244410

## 0x1801C6AD0  (265 octets, 56 instructions)
- appelee par : 0x1802441A0

## 0x1801C6BE0  (42 octets, 10 instructions)
- appelee par : 0x180244410

## 0x1801C6C10  (75 octets, 17 instructions)
- appelee par : 0x1802441A0
- appelle (dans la zone) : 0x1801C6060

## 0x1801C6C60  (42 octets, 10 instructions)
- appelee par : 0x180244410

## 0x1801C6C90  (51 octets, 13 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C6CD0  (69 octets, 16 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C6D20  (59 octets, 15 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C6D60  (47 octets, 12 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C6D90  (64 octets, 15 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3830

## 0x1801C6DD0  (42 octets, 10 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801CB310

## 0x1801C6DFA  (55 octets, 10 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801CBC00

## 0x1801C6E31  (44 octets, 12 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801CAEC0

## 0x1801C6E60  (68 octets, 14 instructions)
- appelee par : 0x1801C8030
- appelle (dans la zone) : 0x1801C3830, 0x1801C3D30

## 0x1801C6ED0  (127 octets, 34 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C6F50  (97 octets, 22 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C6FB1  (309 octets, 78 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C31A0, 0x1801C3290, 0x1801C3660, 0x1801C3830, 0x1801CCD70

## 0x1801C70E6  (36 octets, 9 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C7110  (452 octets, 110 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660, 0x1801CACF0
- chaines : `vfes_se_window_close`

## 0x1801C72E0  (82 octets, 20 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C7332  (63 octets, 16 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660

## 0x1801C7371  (25 octets, 7 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C7390  (161 octets, 39 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C7440  (545 octets, 123 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660, 0x1801C7B50, 0x1801CAC10, 0x1801CBB60
- chaines : `p_part_plt_lt`

## 0x1801C7670  (532 octets, 137 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3650, 0x1801C3660, 0x1801C7D00, 0x1801C8450, 0x1801CAEC0, 0x1801CBEA0, 0x1801CBFE0, 0x1801CC440

## 0x1801C7890  (512 octets, 125 instructions)
- appelee par : 0x1801C7A90
- appelle (dans la zone) : 0x1801C30F0, 0x1801C3660, 0x1801C3830, 0x1801C3900, 0x1801C3A70, 0x1801C3BA0, 0x1801C3BF0, 0x1801C3D30, 0x1801C3D50

## 0x1801C7A90  (189 octets, 39 instructions)
- appelee par : 0x1801C3D71
- appelle (dans la zone) : 0x1801C3660, 0x1801C3830, 0x1801C38F0, 0x1801C7890

## 0x1801C7B50  (422 octets, 103 instructions)
- appelee par : 0x1801C7440
- appelle (dans la zone) : 0x1801C3650, 0x1801C3660, 0x1801C3830, 0x1801C3950, 0x1801CBB80, 0x1801CC130
- chaines : `CUSTOM MENU`, `vfes_se_window_op`, `vfes_se_cansel_01`

## 0x1801C7D00  (647 octets, 151 instructions)
- appelee par : 0x1801C7670
- appelle (dans la zone) : 0x1801C3660, 0x1801C3770, 0x1801C3830, 0x1801C3950, 0x1801C5AB0, 0x1801CBB80, 0x1801CBFE0
- chaines : `CUSTOM MENU`, `vfes_se_window_op`

## 0x1801C7F90  (24 octets, 7 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C7FA8  (101 octets, 17 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660
- chaines : `CONFIRM`

## 0x1801C800D  (20 octets, 6 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C8030  (150 octets, 38 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C6E60, 0x1801CBC00
- chaines : `COSTUME MENU`

## 0x1801C80D0  (59 octets, 15 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C8110  (355 octets, 85 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3670, 0x1801C3830, 0x1801CAC10
- chaines : `EXCLUSIVE WARNING`

## 0x1801C8280  (155 octets, 39 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801CAEC0, 0x1801CB310, 0x1801CBC00

## 0x1801C831B  (86 octets, 19 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- chaines : `vfes_se_error`

## 0x1801C8371  (177 octets, 40 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801CC960
- chaines : `SEL ITEM MENU`

## 0x1801C8422  (40 octets, 12 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3140, 0x1801C3830

## 0x1801C8450  (50 octets, 15 instructions)
- appelee par : 0x1801C7670

## 0x1801C8490  (50 octets, 13 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801C84D0  (83 octets, 24 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3650, 0x1801C3660
- immediats : mov 21 = aucun

## 0x1801C8530  (76 octets, 24 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660

## 0x1801C8580  (43 octets, 12 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660

## 0x1801C85B0  (74 octets, 18 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660

## 0x1801C8600  (207 octets, 47 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660

## 0x1801C86D0  (876 octets, 187 instructions)
- appelee par : 0x1801CA040
- appelle (dans la zone) : 0x1801C3770, 0x1801C3830, 0x1801C5AB0, 0x1801CBDD0
- chaines : `%s`, `%dpt(s)`

## 0x1801C8A40  (1310 octets, 274 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3460, 0x1801C3770, 0x1801C3830, 0x1801C5AB0, 0x1801CA410
- chaines : `head_tit_lt`, `%s`, `p_txt_item_point_lt`, `p_txt_item_point_count_rt`, `%d/10`, `p_sousa_win_01_lt`, `p_sousa_win_02_rb`, `p_cos_plt_c`
- immediats : mov 18 (borne de roster)

## 0x1801C8F60  (1067 octets, 213 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801CB030
- chaines : `p_small_head_lt`, `p_cos_icon_c`, `p_txt_cos_type_c`, `%s`
- immediats : mov 18 (borne de roster)

## 0x1801C9390  (802 octets, 165 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- chaines : `p_small_head_lt`, `%s`, `p_txt_01_lt`, `p_txt_03_rt`
- **scenes** : 0x150=SELSTG_WXGA
- immediats : mov 18 (borne de roster)

## 0x1801C96C0  (1574 octets, 319 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3460, 0x1801C3830
- chaines : `p_small_head_lt`, `%s`, `p_txt_01_lt`, `p_txt_02_rb`, `p_txt_yes_01_lt`, `p_txt_warning_item_c`, `p_txt_warning_item_icon_01_lc`, `p_txt_warning_item_icon_02_rc`
- immediats : mov 18 (borne de roster), mov 20 = ALEATOIRE

## 0x1801C9CF0  (760 octets, 151 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- chaines : `p_small_head_lt`, `p_txt_01_lt`, `%s`
- **scenes** : 0x150=SELSTG_WXGA
- immediats : mov 18 (borne de roster)

## 0x1801C9FF0  (25 octets, 7 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CA009  (42 octets, 10 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801CA620

## 0x1801CA033  (6 octets, 3 instructions)  **BOUCHON**
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CA040  (973 octets, 202 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C86D0
- chaines : `%s`

## 0x1801CA410  (514 octets, 112 instructions)
- appelee par : 0x1801C8A40
- appelle (dans la zone) : 0x1801C3460, 0x1801C3830
- chaines : `p_txt_01_lt`, `%s`, `p_txt_03_rt`, `%dpt(s)`

## 0x1801CA620  (1508 octets, 301 instructions)
- appelee par : 0x1801CA009
- appelle (dans la zone) : 0x1801C3460, 0x1801C3770, 0x1801C3830, 0x1801C3840, 0x1801C5AB0, 0x1801CBAD0, 0x1801CBDD0
- chaines : `p_txt_part_name_c`, `%s`, `p_itemsel_icon_c`, `p_itemsel_info_icon_c`, `p_yaji_up_c`, `p_yaji_down_c`, `newcsr_ud_hit`

## 0x1801CAC10  (218 octets, 51 instructions)
- appelee par : 0x1801C7440, 0x1801C8110
- appelle (dans la zone) : 0x1801C3650, 0x1801C3660, 0x1801C3780, 0x1801C3830, 0x1801C3840, 0x1801C3C80
- chaines : `POINT OVER WARNING`

## 0x1801CACF0  (21 octets, 6 instructions)
- appelee par : 0x1801C7110, 0x1801CAEC0

## 0x1801CAD05  (346 octets, 70 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C5AB0

## 0x1801CAE5F  (18 octets, 5 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CAE71  (48 octets, 10 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3830, 0x1801C3AE0

## 0x1801CAEA1  (18 octets, 5 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3830

## 0x1801CAEC0  (341 octets, 77 instructions)
- appelee par : 0x1801C6E31, 0x1801C7670, 0x1801C8280
- appelle (dans la zone) : 0x1801C3830, 0x1801C3C40, 0x1801C3C70, 0x1801CACF0

## 0x1801CB030  (722 octets, 120 instructions)
- appelee par : 0x1801C8F60
- appelle (dans la zone) : 0x1801C3460, 0x1801C3830
- immediats : cmp 18 (borne de roster)

## 0x1801CB310  (106 octets, 25 instructions)
- appelee par : 0x1801C6DD0, 0x1801C8280
- appelle (dans la zone) : 0x1801C4B40

## 0x1801CB380  (165 octets, 34 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CB430  (324 octets, 73 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660, 0x1801C5AB0
- immediats : mov 20 = ALEATOIRE

## 0x1801CB580  (186 octets, 36 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660

## 0x1801CB640  (246 octets, 52 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3650, 0x1801C3660

## 0x1801CB740  (162 octets, 34 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- chaines : `neu_s`, `p_txt_01_lt`

## 0x1801CB7F0  (447 octets, 88 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3650, 0x1801C3660, 0x1801CBB80, 0x1801CC130
- **scenes** : 0x150=SELSTG_WXGA

## 0x1801CB9B0  (281 octets, 57 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3650, 0x1801C3660, 0x1801CC440, 0x1801CCD70
- chaines : `part_win`

## 0x1801CBAD0  (140 octets, 36 instructions)
- appelee par : 0x1801CA620, 0x1801CC245
- appelle (dans la zone) : 0x1801C3670, 0x1801C3830

## 0x1801CBB80  (119 octets, 34 instructions)
- appelee par : 0x1801C7B50, 0x1801C7D00, 0x1801CB7F0
- appelle (dans la zone) : 0x1801C3770, 0x1801C3830, 0x1801C38D0, 0x1801C5AB0

## 0x1801CBC00  (216 octets, 52 instructions)
- appelee par : 0x1801C6DFA, 0x1801C8030, 0x1801C8280
- appelle (dans la zone) : 0x1801C3660
- chaines : `CONFIRM`

## 0x1801CBD10  (177 octets, 33 instructions)
- appelee par : 0x1801C3D71
- appelle (dans la zone) : 0x1801C3830, 0x1801C4B40
- chaines : `SEL PART MENU`, `BASE WINDOW`

## 0x1801CBDD0  (200 octets, 44 instructions)
- appelee par : 0x1801C86D0, 0x1801CA620

## 0x1801CBEA0  (317 octets, 65 instructions)
- appelee par : 0x1801C7670
- chaines : `sta_s`, `sta_e`, `all_s`, `all_e`, `end_s`, `end_e`, `part_win`

## 0x1801CBFE0  (332 octets, 68 instructions)
- appelee par : 0x1801C7670, 0x1801C7D00
- chaines : `head_s`, `head_e`, `face_s`, `face_e`, `arm_s`, `arm_e`, `bust_s`, `bust_e`, `lower_s`, `lower_e`, `part_win`

## 0x1801CC130  (21 octets, 7 instructions)
- appelee par : 0x1801C7B50, 0x1801CB7F0

## 0x1801CC145  (7 octets, 2 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CC14C  (8 octets, 2 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CC154  (241 octets, 57 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3770, 0x1801C3830, 0x1801C5AB0

## 0x1801CC245  (206 octets, 44 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3830, 0x1801C3840, 0x1801CBAD0

## 0x1801CC313  (63 octets, 14 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3460, 0x1801C3830

## 0x1801CC352  (80 octets, 20 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CC3A2  (138 octets, 36 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CC42C  (1 octets, 1 instructions)  **BOUCHON**
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CC42D  (6 octets, 2 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CC440  (31 octets, 9 instructions)
- appelee par : 0x1801C7670, 0x1801CB9B0

## 0x1801CC45F  (316 octets, 74 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3460, 0x1801C3660, 0x1801C3770, 0x1801C3830, 0x1801C5AB0

## 0x1801CC59B  (1 octets, 1 instructions)  **BOUCHON**
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CC5A0  (952 octets, 227 instructions)
- appelee par : 0x1801CCED0
- chaines : `sel_cursor_part`, `sel_cursor_category`

## 0x1801CC960  (1037 octets, 272 instructions)
- appelee par : 0x1801C8371
- appelle (dans la zone) : 0x1801C3460, 0x1801C3710, 0x1801C3720, 0x1801C3830

## 0x1801CCD70  (339 octets, 84 instructions)
- appelee par : 0x1801C6FB1, 0x1801CB9B0
- appelle (dans la zone) : 0x1801C3720, 0x1801C3830, 0x1801CCED0

## 0x1801CCED0  (733 octets, 115 instructions)
- appelee par : 0x1801CCD70
- appelle (dans la zone) : 0x1801CC5A0
- immediats : mov 18 (borne de roster), mov 19 = DURAL, mov 20 = ALEATOIRE, mov 21 = aucun

## 0x1801CD1B0  (636 octets, 137 instructions)
- appelee par : 0x1801C3D71, 0x1801C5060
- **appelle des bouchons** : 0x180029FB0

## 0x1801CD430  (423 octets, 97 instructions)
- appelee par : 0x1801C4520

## 0x1801CD5E0  (152 octets, 40 instructions)
- appelee par : 0x1801CD690

## 0x1801CD690  (230 octets, 50 instructions)
- appelee par : 0x1801CD780
- appelle (dans la zone) : 0x1801C5810, 0x1801CD5E0

## 0x1801CD780  (94 octets, 29 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801CD690
- **appelle des bouchons** : 0x180007430

## 0x1801CD7E0  (98 octets, 23 instructions)
- appelee par : 0x1801C5BD0

## 0x1801CD850  (41 octets, 8 instructions)
- appelee par : 0x1801C5140

## 0x1801CD880  (497 octets, 111 instructions)
- appelee par : 0x1801C3D71
- appelle (dans la zone) : 0x1801C1A40, 0x1801C1A50, 0x1801C2D30, 0x1801C4B40, 0x1801C5AB0

## 0x1801CDA80  (19 octets, 5 instructions)
- appelee par : 0x1801C4211

## 0x1801CDA93  (234 octets, 49 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CDB7D  (121 octets, 29 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CDBF6  (163 octets, 43 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CDC99  (55 octets, 11 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CDCD0  (99 octets, 29 instructions)
- appelee par : 0x1801C3D71, 0x1801C5140

## 0x1801CDD40  (145 octets, 43 instructions)
- appelee par : 0x1801C3C80
- appelle (dans la zone) : 0x1801CDDE0

## 0x1801CDDE0  (275 octets, 94 instructions)
- appelee par : 0x1801CDD40, 0x1801CE080, 0x1801CE210

## 0x1801CDEF3  (364 octets, 99 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CE05F  (27 octets, 9 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CE080  (299 octets, 86 instructions)
- appelee par : 0x1801C3670
- appelle (dans la zone) : 0x1801CDDE0

## 0x1801CE210  (233 octets, 66 instructions)
- appelee par : 0x1801C3840
- appelle (dans la zone) : 0x1801CDDE0

## 0x1801CE300  (38 octets, 10 instructions)
- appelee par : 0x1801C5B00

## 0x1801CE330  (53 octets, 15 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CE370  (132 octets, 39 instructions)
- appelee par : 0x1801C3C40, 0x1801C3D71

## 0x1801CE400  (86 octets, 25 instructions)
- appelee par : 0x1801C13B0

## 0x1801CE460  (99 octets, 27 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CE4F0  (244 octets, 66 instructions)
- appelee par : 0x1801C3D71
- chaines : `jH`

## 0x1801CE5F0  (423 octets, 81 instructions)
- appelee par : 0x1801CEB30, 0x1801CEBB0

## 0x1801CE7A0  (76 octets, 17 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CE7F0  (254 octets, 47 instructions)
- appelee par : 0x1801CE8F0

## 0x1801CE8F0  (220 octets, 63 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801CE7F0
- **appelle des bouchons** : 0x180007430

## 0x1801CE9D0  (161 octets, 45 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- **appelle des bouchons** : 0x180007430

## 0x1801CEA80  (161 octets, 45 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- **appelle des bouchons** : 0x180007430

## 0x1801CEB30  (75 octets, 17 instructions)
- appelee par : 0x1802441A0
- appelle (dans la zone) : 0x1801CE5F0

## 0x1801CEB80  (42 octets, 10 instructions)
- appelee par : 0x180244410

## 0x1801CEBB0  (75 octets, 17 instructions)
- appelee par : 0x1802441A0
- appelle (dans la zone) : 0x1801CE5F0

## 0x1801CEC00  (42 octets, 10 instructions)
- appelee par : 0x180244410

## 0x1801CEC30  (120 octets, 27 instructions)
- appelee par : 0x1802441A0

## 0x1801CECB0  (74 octets, 17 instructions)
- appelee par : 0x180244410

## 0x1801CED00  (172 octets, 34 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660

## 0x1801CEDD0  (26 octets, 6 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CEDEA  (59 octets, 18 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660

## 0x1801CEE25  (46 octets, 12 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CEE60  (26 octets, 6 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CEE7A  (60 octets, 18 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660

## 0x1801CEEB6  (46 octets, 12 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CEEF0  (16 octets, 7 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CEF00  (315 octets, 76 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660, 0x1801CFE30

## 0x1801CF03B  (485 octets, 89 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C59B0, 0x1801CFE30, 0x1801D0870, 0x1801D0AC0
- chaines : `ERASE_CONFIRM`

## 0x1801CF220  (29 octets, 6 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CF23D  (126 octets, 31 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- **appelle des bouchons** : 0x180029FB0

## 0x1801CF2D0  (346 octets, 73 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660, 0x1801C5A40, 0x1801CFE30, 0x1801D0870
- chaines : `vfes_se_error`, `FULL NOTICE`
- immediats : mov 18 (borne de roster)

## 0x1801CF42A  (87 octets, 18 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C4C90, 0x1801C5A80
- chaines : `%s_%03d`
- immediats : mov 21 = aucun

## 0x1801CF481  (30 octets, 8 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CF4A0  (23 octets, 6 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CF4C0  (50 octets, 12 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CF500  (114 octets, 26 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801CF580  (563 octets, 113 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- chaines : `p_ds_charaname_ct`, `%s`
- immediats : mov 18 (borne de roster)

## 0x1801CF7C0  (926 octets, 195 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- chaines : `p_txt_01_lt`, `p_txt_02_rb`, `p_yaji_left_c`, `p_yaji_right_c`, `newcsr_lr_large_hit`, `---`, `%s`
- **scenes** : 0x150=SELSTG_WXGA
- immediats : mov 18 (borne de roster)

## 0x1801CFB60  (497 octets, 113 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- chaines : `p_small_head_lt`
- immediats : mov 18 (borne de roster)

## 0x1801CFD60  (51 octets, 13 instructions)
- appelee par : 0x1801C3D71, 0x1801DD7A0

## 0x1801CFDA0  (49 octets, 15 instructions)
- appelee par : 0x1801C3D71, 0x1801DD7A0, 0x1801E36D0

## 0x1801CFDE0  (73 octets, 20 instructions)
- appelee par : 0x18016E390, 0x1801C3511

## 0x1801CFFB0  (71 octets, 20 instructions)
- appelee par : 0x18016E390, 0x1801C359E

## 0x1801D0000  (66 octets, 19 instructions)
- appelee par : 0x1801E5BAA

## 0x1801D0050  (49 octets, 15 instructions)
- appelee par : 0x1801E5B80

## 0x1801D0090  (67 octets, 21 instructions)
- appelee par : 0x18016E390, 0x1801C34E0

## 0x1801D0180  (77 octets, 23 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801D01D0  (136 octets, 35 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801D0280  (48 octets, 13 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801D0870

## 0x1801D02B0  (1087 octets, 229 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660, 0x1801D0870
- **appelle des bouchons** : 0x180029FB0
- chaines : `datasel_point`, `p_charasel_lt`, `CHAR SELECT`, `DATA SELECT`
- immediats : mov 21 = aucun, mov 18 (borne de roster)

## 0x1801D0720  (28 octets, 6 instructions)
- appelee par : 0x1801C3D71, 0x1801DD7A0

## 0x1801D073C  (58 octets, 15 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C3660, 0x1801D0B80

## 0x1801D0776  (31 octets, 6 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- chaines : `CARD SELECTOR`

## 0x1801D07A0  (92 octets, 20 instructions)
- appelee par : 0x18016E390
- appelle (dans la zone) : 0x1801D0B80
- chaines : `DATA SELECTOR`

## 0x1801D0800  (107 octets, 28 instructions)
- appelee par : 0x1801E6DE0
- appelle (dans la zone) : 0x1801D0B80
- chaines : `CHAR SELECTOR`
- globaux : is_dural_unlocked

## 0x1801D0870  (536 octets, 117 instructions)
- appelee par : 0x1801CF03B, 0x1801CF2D0, 0x1801D0280, 0x1801D02B0
- chaines : `cursor_tri_46`

## 0x1801D0AC0  (53 octets, 16 instructions)
- appelee par : 0x1801CF03B, 0x1801D0B80
- **appelle des bouchons** : 0x180029FB0

## 0x1801D0AF5  (116 octets, 28 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801C5A80

## 0x1801D0B69  (19 octets, 6 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801D0B80  (413 octets, 101 instructions)
- appelee par : 0x1801D073C, 0x1801D07A0, 0x1801D0800
- appelle (dans la zone) : 0x1801D0AC0
- **appelle des bouchons** : 0x180029FB0
- immediats : mov 18 (borne de roster), mov 20 = ALEATOIRE, cmp 18 (borne de roster)

## 0x1801D0D20  (107 octets, 33 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- **appelle des bouchons** : 0x180007430

## 0x1801D0D90  (102 octets, 26 instructions)
- appelee par : 0x1802441A0

## 0x1801D0E00  (42 octets, 10 instructions)
- appelee par : 0x180244410

## 0x1801D0E40  (194 octets, 37 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801D0F10  (49 octets, 10 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801D0F41  (131 octets, 22 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801D0FC4  (9 octets, 3 instructions)  **BOUCHON**
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801D1070  (170 octets, 34 instructions)
- appelee par : 0x18018FB20
- chaines : `ENVMAP`

## 0x1801D1120  (575 octets, 126 instructions)
- appelee par : 0x1800D6DA0

## 0x1801D1360  (72 octets, 16 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801D13A8  (822 octets, 177 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801D1730
- **appelle des bouchons** : 0x180007430

## 0x1801D16DE  (18 octets, 6 instructions)
- appelee par : _aucun appelant direct (vtable ?)_

## 0x1801D16F0  (44 octets, 14 instructions)
- appelee par : 0x18010C330

## 0x1801D1730  (555 octets, 98 instructions)
- appelee par : 0x1801D13A8

## 0x1801D1960  (130 octets, 38 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- **appelle des bouchons** : 0x180007430

## 0x1801D19F0  (94 octets, 29 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- **appelle des bouchons** : 0x180007430

## 0x1801D1A50  (402 octets, 79 instructions)
- appelee par : 0x1802441A0

## 0x1801D1BF0  (42 octets, 10 instructions)
- appelee par : 0x180244410

## 0x1801D1C20  (64 octets, 18 instructions)
- appelee par : 0x1801D1C80

## 0x1801D1C80  (664 octets, 163 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- appelle (dans la zone) : 0x1801D1C20
- chaines : `CLASS UP WINDOW`, `DIFFICULTY INFO WINDOW`

## 0x1801D1F20  (234 octets, 57 instructions)
- appelee par : _aucun appelant direct (vtable ?)_
- immediats : mov 21 = aucun

