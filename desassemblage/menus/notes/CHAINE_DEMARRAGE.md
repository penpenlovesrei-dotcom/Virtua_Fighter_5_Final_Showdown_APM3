# La chaine de demarrage de REVO, decompilee (SS 338.12)

Table des sous-etats : **VF5FS+0x3C87F0**, pas de 0x20, **73 entrees**,
**3 gestionnaires de phase** par entree (lue dans le binaire, pas recopiee).
C est, au bit pres, le `ModeSubTable { uint32_t name; bool pause_enable;
bool (*func[3])(); }` de YAMP.

Table des modes : **`VF5FS+0x3C8240`**, pas de 0x68, 14 lignes, dont
seuls les **3 premiers qwords sont des pointeurs** ; les suivants sont des
PAIRES de numeros de sous-etats. Ligne du mode 0 = STARTUP :
`1800E6510 / 1800E56E0 / 1800E5B80`, puis (0,1) (8,5) (6,2) (3,4) (7,73).

| # | sous-etat | phase 0 | phase 1 | phase 2 |
|---|---|---|---|---|
| 0 | **DATA_INITIALIZE** | [1800E64E0](FUN_1800e64e0.c) | `1800E56B0` *(saut, pas de fichier : voir plus bas)* | [1800E5B20](FUN_1800e5b20.c) |
| 1 | **SYSTEM_STARTUP** | [1800E6580](FUN_1800e6580.c) | [1800E58A0](FUN_1800e58a0.c) | [1800E5BC0](FUN_1800e5bc0.c) |
| 2 | **WARNING** | [1800E6660](FUN_1800e6660.c) | [1800E58C0](FUN_1800e58c0.c) | [1800E5C00](FUN_1800e5c00.c) |
| 3 | **CROSSPLAY_WARNING** | [1800E5D20](FUN_1800e5d20.c) | [1800E54D0](FUN_1800e54d0.c) | [1800E59A0](FUN_1800e59a0.c) |
| 4 | **OFFLINE_WARNING** | [1800E64F0](FUN_1800e64f0.c) | [1800E56C0](FUN_1800e56c0.c) | [1800E5B60](FUN_1800e5b60.c) |
| 5 | **CS_TITLE** | [1800E5ED0](FUN_1800e5ed0.c) | [1800E55B0](FUN_1800e55b0.c) | [1800E5A20](FUN_1800e5a20.c) |
| 6 | **CS_SIGNIN** | [1800E5E50](FUN_1800e5e50.c) | [1800E5570](FUN_1800e5570.c) | *bouchon* |
| 7 | **CS_AUTOLOAD** | [1800E5D40](FUN_1800e5d40.c) | [1800E54F0](FUN_1800e54f0.c) | [1800E59C0](FUN_1800e59c0.c) |
| 8 | **CS_DEMO** | [1800E5D70](FUN_1800e5d70.c) | [1800E5510](FUN_1800e5510.c) | [1800E59F0](FUN_1800e59f0.c) |

Les 3 gestionnaires du MODE 0 (STARTUP) : [1800E6510](FUN_1800e6510.c), [1800E56E0](FUN_1800e56e0.c), [1800E5B80](FUN_1800e5b80.c) ; le repartiteur qui les appelle est [1800E1600](FUN_1800e1600.c).

## Le verrou mesure de CS_DEMO (SS 338.8)

```c
FUN_1800E5510 (CS_DEMO phase 1) :
  if (FUN_1800F0780()) {                       // tache de demo vivante ?
      iVar2 = FUN_1801B2390();                 // -1 : ni bouton ni 242
      if (FUN_1802CB570() && FUN_1802CB830())  // cmd 212 ET cmd 225
          iVar2 = FUN_1801B2280();             // le port SI manette PRESENTE
      if (iVar2 < 0) return 0;                 // RESTE en phase 1
  }
  return 1;
```

La phase 2 (`FUN_1800E59F0`) est INCONDITIONNELLE et rend toujours 1,
donc le repartiteur arme `DAT_18075141D` des que la phase 1 finit.
Tout se joue donc en phase 1.

## Fermeture COMPLETE (2026-11-07)

Graines : les 29 gestionnaires ci-dessus, plus tout le sous-systeme d'entree.
Puis boucle "vider -> relire les FUN_ references -> vider" jusqu'au point fixe :

    tour  1 :  925 sur le disque, 1120 referencees, 195 manquantes
    tour  2 : 1120 sur le disque, 1291 referencees, 171 manquantes
    ...
    tour 16 : 2701 sur le disque, 2704 referencees,   3 manquantes
    tour 17 : 2704 sur le disque, 2704 referencees,   0 manquantes

**2704 fonctions, 13 Mio, zero referencee absente.** Il n'y a plus une seule
fonction appelee depuis la chaine de demarrage qui ne soit pas sur ce disque.
Ce dossier comptait 151 fichiers avant cette seance.

Voir aussi **[ENTREE_MANETTES.md](ENTREE_MANETTES.md)** : la disposition des
manettes dans le bloc de l'hote (pas de 0x190, presence en +0x108), qui
commande la seule sortie de CS_DEMO ne demandant pas d'appui.

## Une case sans fichier, et c'est mesure

`1800E56B0` (DATA_INITIALIZE phase 1) est un saut de 5 octets
`JMP 0x180066520`, et cette cible n'est pas une fonction pour Ghidra parce
qu'elle fait 11 octets :

    180066520  CMP dword ptr [0x1806BAD18], 0xC
    180066527  SETZ AL
    18006652A  RET

La phase 0 de DATA_INITIALIZE lance le chargement ; sa phase 1 demande
seulement **`DAT_1806BAD18 == 12`**. Il n'y a donc pas de fichier `.c` pour
elle, et ce n'est pas un manque.

## Ce que la chaine FAIT, mesure (SS 339, course de 1800 images)

Elle passe en entier. Progression relevee par la sonde bornee :

```
0 DATA_INITIALIZE -> 1 SYSTEM_STARTUP -> 8 CS_DEMO -> 5 CS_TITLE (img 307-490)
-> 6 CS_SIGNIN (491) -> 2 WARNING -> 3 CROSSPLAY_WARNING -> 4 OFFLINE_WARNING
-> 7 CS_AUTOLOAD -> [mode 5 = MENU] -> 40 MENU_MAIN (img 655, et il y reste)
```

`demande=73=MAX` est le **sentinelle de fin**, pas un sous-etat : ca resout la
paire `(7,73)` de la ligne du mode 0.

### Le sous-etat 40 = MENU_MAIN, et pourquoi il ne bouge plus

Ligne lue dans la table **vivante** (`VF5FS+0x3C87F0 + 40*0x20`) :

| champ | valeur |
|---|---|
| `+0x00` | `0x0000000100000028` (nom 0x28 = 40, pause_enable = 1) |
| `+0x08` | phase 0 -> [`FUN_1800E4210`](FUN_1800e4210.c) = `FUN_180210840(); return 1;` |
| `+0x10` | phase 1 -> [`FUN_18000BA20`](FUN_18000ba20.c) = **`return 0;`** |
| `+0x18` | phase 2 -> [`FUN_1800E4130`](FUN_1800e4130.c) = `FUN_180206B90(); return 1;` |

**Une phase 1 qui rend 0 veut dire « pas fini ».** MENU_MAIN y reste donc pour
toujours : c'est l'etat de REPOS de la chaine console, par construction dans
le binaire de SEGA. Le menu tourne comme une TACHE a cote. Le gestionnaire de
phase 0 du mode MENU est [`FUN_1800E4140`](FUN_1800e4140.c).

### CS_TITLE tient tout seul — [`FUN_1800E55B0`](FUN_1800e55b0.c)

| condition | CS_TITLE phase 1 |
|---|---|
| aucune manette, aucun appui | **rend 0 : l'ecran TIENT** |
| manette presente, apres `0xb4` = 180 tics | rend 1 : son `sy_charin00st`, commande 414 |
| `0x708` = 1800 tics (~30 s) sans rien | `FUN_1800E1B20(8)` : **demande CS_DEMO** |

La boucle attract <-> titre est donc dans le binaire. Dans les courses du
SS 338 elle etait court-circuitee par `VF5_MANETTE=2`, qui equivaut a tenir
START : CS_TITLE sortait a l'image 490 = 307 + 180.

### Fermeture, apres ajout des gestionnaires de MENU_MAIN

```
tour 1 : 2707 sur le disque, 2709 referencees, 2 manquantes
tour 2 : 2709 sur le disque, 2709 referencees, 0 manquantes
```

---

# LE MENU ET LE COMBAT (SS 377-378, 7 novembre 2026)

Ce fichier ne couvrait que la chaine de **demarrage**. L'utilisateur a demande
« tout est vraiment decompile dans le menu, les sous menus aussi, les
differents modes de jeu aussi ? ». Reponse mesuree, et le chantier qui a suivi.

## 1. La couverture, mesuree -- `py -3 VF5RE\chaines_des_modes.py`

L'outil qui lisait deja la table des modes **compte maintenant le vidage** de
chacune des 73 x 3 phases. Il distingue quatre cas, et c'est la distinction
qui compte : **bouchon** (rien a decompiler), **present**, **saut** (un `JMP`
de 5 octets vers autre chose), **absent**.

```
sous-etats a code REEL        : 35 / 73
  dont toutes phases presentes: 13
phases reelles                : 100  dont presentes 39, absentes 61
code_decompile                : 3179 fichiers .c
```

Les bouchons sont reperes **par leur repetition**, jamais par une adresse
ecrite ici : `0x180026620` sur 100 emplacements, `0x18000BA20` sur 19. Les 38
sous-etats entierement bouchonnes sont la chaine arcade (9-18), les
`DATA_TEST_*` (25-39), les `APM3_*` (52-58) et les `ONLINE_*` (46-51).

**Les 13 sous-etats complets** : 1 a 8 (la chaine de demarrage), **19
SELECTOR, 20 MODE_SELECTOR, 21 VS, 22 GAMEOVER** (vides le 7 novembre) et
**40 MENU_MAIN**.

### Correction de mes propres chiffres du SS 377

Le SS 377 annonçait « 9 complets, 27 phases presentes, 73 absentes ». Faux sur
deux points, et c'est ce fichier-ci qui portait la reponse :

1. il ne suivait pas les **sauts**, alors que la section « Une case sans
   fichier » ci-dessus disait deja que `1800E56B0` est un `JMP 0x180066520` ;
2. il a ete calcule avant les vidages du jour.

Les chiffres a citer sont ceux de l'outil, ci-dessus. Lecon : **l'index etait
deja ecrit ; un script jetable a re-mesure moins bien.**

## 2. Les 73 sous-etats, avec leurs fichiers

Tableau genere par `py -3 VF5RE\chaines_des_modes.py --md` :

| # | sous-etat | phase 0 | phase 1 | phase 2 |
|---|---|---|---|---|
| 0 | **DATA_INITIALIZE** | [1800E64E0](FUN_1800e64e0.c) | *saut -> 180066520, pas une fonction* | [1800E5B20](FUN_1800e5b20.c) |
| 1 | **SYSTEM_STARTUP** | [1800E6580](FUN_1800e6580.c) | [1800E58A0](FUN_1800e58a0.c) | [1800E5BC0](FUN_1800e5bc0.c) |
| 2 | **WARNING** | [1800E6660](FUN_1800e6660.c) | [1800E58C0](FUN_1800e58c0.c) | [1800E5C00](FUN_1800e5c00.c) |
| 3 | **CROSSPLAY_WARNING** | [1800E5D20](FUN_1800e5d20.c) | [1800E54D0](FUN_1800e54d0.c) | [1800E59A0](FUN_1800e59a0.c) |
| 4 | **OFFLINE_WARNING** | [1800E64F0](FUN_1800e64f0.c) | [1800E56C0](FUN_1800e56c0.c) | [1800E5B60](FUN_1800e5b60.c) |
| 5 | **CS_TITLE** | [1800E5ED0](FUN_1800e5ed0.c) | [1800E55B0](FUN_1800e55b0.c) | [1800E5A20](FUN_1800e5a20.c) |
| 6 | **CS_SIGNIN** | [1800E5E50](FUN_1800e5e50.c) | [1800E5570](FUN_1800e5570.c) | *bouchon* |
| 7 | **CS_AUTOLOAD** | [1800E5D40](FUN_1800e5d40.c) | [1800E54F0](FUN_1800e54f0.c) | [1800E59C0](FUN_1800e59c0.c) |
| 8 | **CS_DEMO** | [1800E5D70](FUN_1800e5d70.c) | [1800E5510](FUN_1800e5510.c) | [1800E59F0](FUN_1800e59f0.c) |
| 9 | **LOGO** | *bouchon* | *bouchon* | *bouchon* |
| 10 | **RATING** | *bouchon* | *bouchon* | *bouchon* |
| 11 | **DEMO** | *bouchon* | *bouchon* | *bouchon* |
| 12 | **TITLE** | *bouchon* | *bouchon* | *bouchon* |
| 13 | **TITLE_TV** | *bouchon* | *bouchon* | *bouchon* |
| 14 | **LOGO_TV** | *bouchon* | *bouchon* | *bouchon* |
| 15 | **LOGO_TERMINAL** | *bouchon* | *bouchon* | *bouchon* |
| 16 | **MANUAL_TERMINAL** | *bouchon* | *bouchon* | *bouchon* |
| 17 | **TITLE_TERMINAL** | *bouchon* | *bouchon* | *bouchon* |
| 18 | **LOOP_TERMINAL** | *bouchon* | *bouchon* | *bouchon* |
| 19 | **SELECTOR** | [1800E3F90](FUN_1800e3f90.c) | [1800E2470](FUN_1800e2470.c) | [1800E2F60](FUN_1800e2f60.c) |
| 20 | **MODE_SELECTOR** | [1800E3F70](SE20_MODE_SELECTOR_Phase0.c) | [1800E2010](SE20_MODE_SELECTOR_Phase1_MontageDuMatch.c) | [1800E2F40](SE20_MODE_SELECTOR_Phase2.c) |
| 21 | **VS** | [1800E3D70](FUN_1800e3d70.c) | [1800E1C20](FUN_1800e1c20.c) | [1800E2CE0](FUN_1800e2ce0.c) |
| 22 | **GAMEOVER** | [1800E3D40](FUN_1800e3d40.c) | [1800E1BC0](FUN_1800e1bc0.c) | [1800E2B70](FUN_1800e2b70.c) |
| 23 | **WORLD_STAGE_MAIN** | **18000B830 absent** | **18000B3D0 absent** | **18000B4F0 absent** |
| 24 | **WORLD_STAGE_TOURNAMENT** | **18000B860 absent** | **18000B3D0 absent** | **18000B510 absent** |
| 25 | **DATA_TEST_MAIN** | *bouchon* | *bouchon* | *bouchon* |
| 26 | **DATA_TEST_MISC** | *bouchon* | *bouchon* | *bouchon* |
| 27 | **DATA_TEST_OBJ** | *bouchon* | *bouchon* | *bouchon* |
| 28 | **DATA_TEST_STG** | *bouchon* | *bouchon* | *bouchon* |
| 29 | **DATA_TEST_MOT** | *bouchon* | *bouchon* | *bouchon* |
| 30 | **DATA_TEST_COLLISION** | *bouchon* | *bouchon* | *bouchon* |
| 31 | **DATA_TEST_SPR** | *bouchon* | *bouchon* | *bouchon* |
| 32 | **DATA_TEST_AET** | *bouchon* | *bouchon* | *bouchon* |
| 33 | **DATA_TEST_AUTH_3D** | *bouchon* | *bouchon* | *bouchon* |
| 34 | **DATA_TEST_CHR** | *bouchon* | *bouchon* | *bouchon* |
| 35 | **DATA_TEST_ITEM** | *bouchon* | *bouchon* | *bouchon* |
| 36 | **DATA_TEST_PERF** | *bouchon* | *bouchon* | *bouchon* |
| 37 | **DATA_TEST_TNMT** | *bouchon* | *bouchon* | *bouchon* |
| 38 | **DATA_TEST_BATTLE** | *bouchon* | *bouchon* | *bouchon* |
| 39 | **DATA_TEST_KOTSP_SS** | *bouchon* | *bouchon* | *bouchon* |
| 40 | **MENU_MAIN** | [1800E4210](FUN_1800e4210.c) | *bouchon* | [1800E4130](FUN_1800e4130.c) |
| 41 | **CS_TERM_CUSTOMIZE** | **180211F90 absent** | **180211A80 absent** | **180211E90 absent** |
| 42 | **CS_TERM_REPLAY_PLAY** | **180212020 absent** | **180211D10 absent** | *bouchon* |
| 43 | **CS_TERM_LAST_PLAY** | **180211FD0 absent** | **180211B20 absent** | **180211EB0 absent** |
| 44 | **CS_TERM_CLIP_PLAY** | **180211F80 absent** | **1802119C0 absent** | **180211E40 absent** |
| 45 | **CS_TRAINING** | **180212140 absent** | **180212070 absent** | **1802120D0 absent** |
| 46 | **ONLINE_STARTUP** | *bouchon* | *bouchon* | *bouchon* |
| 47 | **ONLINE_SELECTOR** | *bouchon* | *bouchon* | *bouchon* |
| 48 | **ONLINE_MENU** | *bouchon* | *bouchon* | *bouchon* |
| 49 | **ONLINE_MATCHING** | *bouchon* | *bouchon* | *bouchon* |
| 50 | **ONLINE_GAME** | *bouchon* | *bouchon* | *bouchon* |
| 51 | **ONLINE_OVER** | *bouchon* | *bouchon* | *bouchon* |
| 52 | **APM3_ENTRY** | *bouchon* | *bouchon* | *bouchon* |
| 53 | **APM3_SELECTOR** | *bouchon* | *bouchon* | *bouchon* |
| 54 | **APM3_GAME_VS** | *bouchon* | *bouchon* | *bouchon* |
| 55 | **APM3_GAMEOVER** | *bouchon* | *bouchon* | *bouchon* |
| 56 | **APM3_TRAINING** | *bouchon* | *bouchon* | *bouchon* |
| 57 | **APM3_ONLINE_VS** | *bouchon* | *bouchon* | *bouchon* |
| 58 | **APM3_TESTMODE_MAIN** | *bouchon* | *bouchon* | *bouchon* |
| 59 | **RANK_MATCH_STARTUP** | **180218720 absent** | **180213F70 absent** | **180215780 absent** |
| 60 | **RANK_MATCH_MATCHING** | **1802183C0 absent** | **1802135D0 absent** | **1802156A0 absent** |
| 61 | **RANK_MATCH_GAME** | **180218230 absent** | **180213170 absent** | **1802155D0 absent** |
| 62 | **RANK_MATCH_OVER** | **1802184A0 absent** | **180213CF0 absent** | **1802156F0 absent** |
| 63 | **ROOM_MATCH_STARTUP** | **180218720 absent** | **180214A80 absent** | **180215D90 absent** |
| 64 | **ROOM_MATCH_MENU** | **180218C80 absent** | **180214760 absent** | *bouchon* |
| 65 | **ROOM_MATCH_MATCHING** | **180218BA0 absent** | **1802145F0 absent** | **180215AC0 absent** |
| 66 | **ROOM_MATCH_GAME** | **180218980 absent** | **1802140E0 absent** | **180215970 absent** |
| 67 | **ROOM_MATCH_OVER** | **180218CD0 absent** | **180214A20 absent** | **180215B00 absent** |
| 68 | **TOURNAMENT_STARTUP** | **180218720 absent** | **180215380 absent** | **180215D90 absent** |
| 69 | **TOURNAMENT_MENU** | **180219230 absent** | **1802151D0 absent** | *bouchon* |
| 70 | **TOURNAMENT_MATCHING** | **180219150 absent** | **1802150B0 absent** | **1802160B0 absent** |
| 71 | **TOURNAMENT_GAME** | **180218F30 absent** | **180214BE0 absent** | **180215F80 absent** |
| 72 | **TOURNAMENT_OVER** | **180219280 absent** | **180215320 absent** | **1802160E0 absent** |

## 3. Demander une scene est une ECRITURE, pas un appel

Les deux « portes » du module font trois lignes chacune :

```c
void FUN_1800e1b00(int mode) {        // VF5FS+0xe1b00  -- DEMANDER UN MODE
    DAT_1807513f4 = mode;             // VF5FS+0x7513F4  mode demande
    DAT_180751400 = 1;                // VF5FS+0x751400  mode a lancer
    DAT_18075141c = 0;                // VF5FS+0x75141C  -> sous-etat par defaut
}
void FUN_1800e1b20(int sous_etat) {   // VF5FS+0xe1b20  -- DEMANDER UN SOUS-ETAT
    DAT_180751410 = sous_etat;        // VF5FS+0x751410
    DAT_18075141c = 1;                // VF5FS+0x75141C  engage
}
```

Fichiers : [FUN_1800e1b00.c](FUN_1800e1b00.c), [FUN_1800e1b20.c](FUN_1800e1b20.c).

**Largeurs lues au desassembleur (SS 380)** : `FUN_1800E1B00` fait
`MOV dword [0x1807513F4], ECX` puis `MOV byte [0x180751400], 1` et
`MOV byte [0x18075141C], 0` ; `FUN_1800E1B20` fait
`MOV dword [0x180751410], ECX` puis `MOV byte [0x18075141C], 1`.
**Un dword et DEUX OCTETS, pas trois int32** : ecrire 4 octets en
`+0x751400` ecraserait `+0x751401`, que le journal connait comme
« mode termine ».

**L'hote n'a donc pas besoin d'appeler `VF5FS+0xe1960`** : un dword et deux octets dans
l'image du module suffisent. Pas de convention d'appel a deviner, pas de
rentree dans le module au mauvais moment.

## 4. Le mode GAME possede exactement les quatre sous-etats du combat

`chaines_des_modes.py` le lit depuis le SS 309, avec les **vrais noms** pris
dans le binaire (`0x3C9110` pour les modes, `0x3C9190` pour les sous-etats) :

```
numero 2  GAME   phases 0x1800E3CA0 0x1800E1B30 0x1800E2AB0
   chaine : 19=SELECTOR -> 20=MODE_SELECTOR -> 21=VS -> 22=GAMEOVER -> 73=FIN
   +0x60  : 5=MENU
numero 5  MENU   phases 0x1800E4140 0x1800E4080 0x1800E40C0
   chaine : 40=MENU_MAIN -> 73=FIN
numero 3  WORLD_STAGE   chaine : 23 -> 41 -> 21=VS -> 24 -> 22  (VS est PARTAGE)
```

**Le premier de la chaine est le defaut** : demander le mode 2 seul mene a
**19 SELECTOR**, l'ecran de choix des personnages. Et `+0x60` porte le mode de
**retour** -- `5=MENU` pour GAME, ce qui explique le `FUN_1800e1b00(5)` de
SELECTOR a l'annulation.

## 5. Le prerequis qui decide du court-circuit

`FUN_1800b21e0()` rend `DAT_18073D9D8` (`VF5FS+0x73D9D8`), le gestionnaire de
combat. **Les quatre sous-etats le dereferencent des leur premiere ligne**
(`FUN_1800b2390(...)`). [FUN_1800b2110.c](FUN_1800b2110.c) le **DETRUIT** (il
met 0) et c'est la **phase 2 du mode GAME** ([FUN_1800e2ab0.c](FUN_1800e2ab0.c))
qui l'appelle ; il est donc bati par la **phase 0 du mode**
([FUN_1800e3ca0.c](FUN_1800e3ca0.c)).

**Donc on demande le MODE, pas le sous-etat.** Sauter directement a VS
dereferencerait un pointeur nul -- le court-circuit « sous-etat 21 » annonce
au SS 377 etait faux, et c'est la lecture qui l'a dit, pas un plantage.

## 6. La boucle du combat, et sept attentes amputees

[FUN_1800e2300.c](FUN_1800e2300.c) (appele par VS phase 1) choisit la suite et
ne rend que quatre valeurs : `0x13` SELECTOR, `0x14` MODE_SELECTOR, `0x15` VS
(revanche), `0x16` GAMEOVER.

```
20 MODE_SELECTOR --(DAT_18063DC08 : 0->1->2->3)--> FUN_1800e1b20(0x13)
19 SELECTOR  ---- annulation : FUN_1800e1b00(5) = RETOUR AU MENU
21 VS  ---------- FUN_1800e2300() --> 0x13 / 0x14 / 0x15 / 0x16
22 GAMEOVER ----- revanche : FUN_1800e1b20(0x15)  |  retour : (0x13)
```

**`FUN_18000BA20`, le bouchon `return 0`, est appele comme CONDITION a sept
endroits de ce chemin** : une fois dans VS phase 0, six fois dans
MODE_SELECTOR phase 1. Chaque `if (FUN_18000ba20()) return 0;` etait une
attente que REVO a retiree. Elles passent toutes immediatement -- a notre
avantage, mais c'est la preuve que le chemin est ampute.

Autres reperes lus dans les douze phases :

| repere | ce que c'est |
|---|---|
| `DAT_1807956D0` | le voile de transition : `FUN_1801a4180` le lance, `FUN_1801a3e70` dit s'il tourne. **VS phase 0 rend 0 tant qu'il tourne** : attente normale |
| [FUN_1801cf1f0.c](FUN_1801cf1f0.c) | ecrit un octet a `[DAT_180796DB0 + 0x11229]` : 1 au titre, 0 a l'entree du combat |
| [FUN_1800da490.c](FUN_1800da490.c) | `[&DAT_18074FE70 + 0x58] = n` et `+0x64 = 1` : **3** pour SELECTOR/MODE_SELECTOR/VS, **4** pour GAMEOVER |
| `FUN_1800bedc0("GAME_VS", ...)` | VS phase 0 nomme la scene |
| `FUN_180081FE0` / `FUN_180081ED0` | quatre rappels aux identifiants **9, 10, 0xF, 0x10**, poses a l'entree, retires a la sortie |
| cles `0x3C`..`0x45` | statistiques, soumises par VS phase 2 **seulement si le sous-etat demande vaut 0x16** |
| `DAT_180C8DE18` / `DAT_180C8DE19` | gardent deux blocs entiers de ce chemin |

**Piege restant** : le veto `FUN_1802CCA60()` est consulte en tete du
repartiteur. S'il rend vrai, la demande est **ignoree sans trace**.

## 7. Fermeture du MENU et du COMBAT -- nouveau point fixe

Meme boucle qu'au SS 338.12 (« vider -> relire les `FUN_` references ->
vider »), mais a partir de 21 racines : les deux racines par image du menu
(`FUN_1802079E0` 830 lignes, `FUN_18020F1E0`), les 12 phases de 19/20/21/22, et
les 3 phases des modes GAME et MENU.

```
tour 1 : 2726 sur le disque, 1157 referencees, 136 manquantes
tour 2 : 2861 sur le disque, 1297 referencees, 128 manquantes
...
tour 8 : 3176 sur le disque, 1516 referencees,   4 manquantes
tour 9 : 3179 sur le disque, 1516 referencees,   1 manquante
```

**3179 fichiers, 1516 fonctions atteintes, et la seule restante
(`0x1803C9EB8`) n'est pas une fonction** : c'est une adresse de la table des
noms de sous-etats que l'expression reguliere attrape. Le menu, ses
sous-menus internes et les quatre sous-etats du combat sont donc **fermes**.

Pourquoi la fermeture du SS 338.12 ne les avait pas pris : `FUN_1802079E0` est
la mise a jour par image d'une **TACHE**, enregistree par pointeur de
fonction, donc aucun appel direct ne part de MENU_MAIN vers elle.

## 8. Ce qui reste absent, et ce n'est pas un oubli

Parmi les 35 sous-etats a code reel, **22 gardent des phases absentes** :

* **les sous-menus qui sont des sous-etats a part** : `CS_TERM_CUSTOMIZE` (41),
  `CS_TERM_REPLAY_PLAY` (42), `CS_TERM_LAST_PLAY` (43), `CS_TERM_CLIP_PLAY` (44)
  et `CS_TRAINING` (45) -- mode CS_TERM (6) et CS_TRAINING (7) ;
* `WORLD_STAGE_MAIN` (23) et `WORLD_STAGE_TOURNAMENT` (24) -- mode 3 ;
* les **14 sous-etats en ligne** ajoutes par REVO : `RANK_MATCH_*` (59-62),
  `ROOM_MATCH_*` (63-67), `TOURNAMENT_*` (68-72) -- modes 11, 12, 13.

Ils ne sont pas dans la chaine menu/combat : ils se ferment quand on en aura
besoin, avec la meme boucle.

## Le sous-etat 40 = MENU_MAIN a DEUX chemins (SS 419, 8 nov 2026)

**Ce registre disait que la phase 1 de MENU_MAIN est un bouchon qui rend 0,
donc que le jeu y reste. C est vrai, et ce n est pas la fin de l histoire :
le menu vit dans sa TACHE, et cette tache a deux chemins exclusifs.**

L init de la tache `"MAIN MENU"` est [`FUN_18020F1E0`](FUN_18020f1e0.c), sa
mise a jour [`FUN_1802079E0`](FUN_1802079e0.c). L init ouvre sur :

```c
if (DAT_180c8df28 == 0 || *(longlong *)(DAT_180c8df28 + 0x1ff08) == 0) {
    // CHEMIN (A), 155 lignes : le module batit TOUT le menu, puis return 1
}
// CHEMIN (B) : ~30 gestionnaires, cmd 216, cmd 188(1), +0x28C4 <- 17,
// puis return 1 SEULEMENT si la commande 80 rend 1.
```

C est le motif de CS_TITLE au bit pres. **Avec notre repartiteur installe, le
module prend le chemin (B) et ne charge ni fond, ni sous-menus, ni musique.**

Tout est consigne dans [MENU.md](MENU.md) : la carte du switch de validation
(section 5), les deux chemins (section 6), la commande 80 de l oracle
(section 7), et **les predicats du chemin (A) tous nommes par leur vtable**
(section 10).

---

# LA BOUCLE DU TITRE : LA CAUSE, LUE ET OTEE (SS 419.8, 8 novembre 2026)

## 1. La question etait mal posee

Je cherchais << pourquoi CS_TITLE demande-t-il CS_SIGNIN ? >>. **Il le demande
par construction** : la demande vaut 6=CS_SIGNIN des la phase 0, aux 65 entrees
de CS_TITLE de la course du SS 419.7, et ce fichier le dit depuis le SS 338 --
`0 DATA_INITIALIZE -> 1 SYSTEM_STARTUP -> 8 CS_DEMO -> 5 CS_TITLE -> 6
CS_SIGNIN -> 2 WARNING -> ...`. La demande n'est pas la panne.

**La vraie question est : pourquoi CS_TITLE ne TIENT-il plus ?** Il sortait a
l'image 490 (= 307 + 180 tics) ; il sort maintenant a son 2e tic, 65 fois.

## 2. Le predicat de sortie, et ses DEUX appelants

`FUN_1800E55B0` (CS_TITLE phase 1) ouvre sur `iVar2 = FUN_1801B2390();` et
sort des que `-1 < iVar2`. Or `FUN_1801B2390` **appelle NOTRE repartiteur avec
la commande `0xF2` = 242** et un octet de sortie :

```c
local_res8[0] = '\0';
if (bloc+0x1FF08 != 0 && *(bloc+0x1FF08) != 0)
    repartiteur(ctx, 0xf2, local_res8);          // <<<< NOUS
...
if ((uVar4 & uVar3) == 0) {                      // aucun bouton tenu
    iVar2 = -1;
    if (local_res8[0] != '\0') iVar2 = iVar1;    // NOTRE octet force la sortie
    return iVar2;
}
```

**References croisees Ghidra sur `VF5FS+0x1B2390` : DEUX appelants, et un seul
octet pour les deux.**

| site | fonction | sous-etat |
|---|---|---|
| `0x1800E5537` | `FUN_1800E5510` | **8 = CS_DEMO** phase 1 |
| `0x1800E55B6` | `FUN_1800E55B0` | **5 = CS_TITLE** phase 1 |

Un octet non nul veut donc dire, selon l'appelant, << saute l'attract >> **ou**
<< sors de l'ecran du titre >>. C'est le meme octet.

## 3. Ce que l'hote repondait, et depuis quand

`lancer_config_complete.cmd` pose `VF5_SAUT_DEMO=1`. L'hote en fait
`g_demoImages = 1`, puis `if (g_demoImages > 0) --g_demoImages;` -> **0**, et
`g_modeSautDemo = true`. Donc `saute = nd > 0` est **vrai des le premier
appel** -- ce que le journal de la course confirme mot pour mot :

```
[cmd 242] demo : appel 1 -> octet 1   (VF5_SAUT_DEMO=0)
```

**Un seul appel journalise, octet 1, et le chemin compteur ne regarde pas le
sous-etat.** CS_TITLE recevait donc 1 a chacun de ses tics.

**Et c'etait deja diagnostique.** Le SS 341 avait lu exactement cela et ecrit
la bonne reponse -- 1 dans CS_DEMO, 0 ailleurs -- **derriere `VF5_TITRE_TIENT`,
eteint par defaut**, pendant que le lanceur de reference gardait la mauvaise.
Pire : l'en-tete du journal de l'hote l'ecrivait a chaque course,
<< saute la demo ET l'ecran du titre, car FUN_1800E55B0 lit le MEME octet >>.

## 4. LA CAUSE OTEE

La qualification par le sous-etat devient **le comportement**, sans option :
hors de CS_DEMO il n'y a aucun cas ou 1 est la bonne reponse, puisque 1 y veut
dire << sors de l'ecran que tu tiens >>. **`VF5_TITRE_TIENT` est retire du
code** (declaration, lecture d'environnement, en-tete). `VF5_SAUT_DEMO=N`
garde tout son sens, mais DANS CS_DEMO seulement, et le compteur n'avance plus
ailleurs.

Ecrire 0 n'est pas un risque : `FUN_1801B2390` met lui-meme l'octet a zero
avant l'appel, donc 0 est exactement l'etat d'avant.

**Etat : l'hote compile. RIEN N'A TOURNE.**

## 5. CE QU'IL FAUT REGARDER A LA PROCHAINE COURSE

**Le signal d'echec d'abord.** L'en-tete doit porter
`commande 242 ecrit 0 HORS de CS_DEMO`, et la ligne

```
[cmd 242] 419.8 : sous-etat 5 -> octet 0 -- hors CS_DEMO ...
```

doit paraitre pour le sous-etat **5**. Si elle ne parait que pour 8, ou pas du
tout, `FUN_1801B2390` n'est pas appelee depuis CS_TITLE et toute la section 2
est fausse.

Ensuite, par ordre :

| temoin | avant (mesure SS 419.7) | attendu |
|---|---|---|
| entrees dans CS_TITLE | **65** | **1** |
| entrees dans CS_SIGNIN / WARNING | 64 / 64 | 0 jusqu'a un appui |
| tirages par image a l'image 650 | **3553, en croissance** | **plat** |
| images par seconde | 5,2 | ~50 |
| sortie de CS_TITLE | a son 2e tic | sur `0x708` = 1800 tics (~30 s) vers CS_DEMO, ou sur START |

**La boucle attract <-> titre reste dans le binaire** : sans entree, CS_TITLE
repart vers CS_DEMO au bout de 1800 tics. C'est le jeu, pas une panne. Pour
aller au menu il faut un appui : `VF5_CLAVIER=1` et ENTREE
([[le-clavier-est-eteint-par-defaut]]).

Et c'est lui qui regarde l'ecran.

---

## 6. LA COURSE : LE GESTE EST PAYE (SS 419.8, 1200 images)

**Course du 8 novembre 2026, 1200 images, configuration de reference, clavier
eteint. Code de sortie 0. 20,99 s.**

### 6.1 Le signal d'echec est passe

La ligne attendue a paru, **et pour le sous-etat 5** :

```
[cmd 242] 419.8 : sous-etat 5 -> octet 0 -- hors CS_DEMO on ne force PAS
la sortie de cet ecran, car VF5FS+0x1B2390 sert AUSSI la phase 1 de CS_TITLE
```

`FUN_1801B2390` est donc bien appelee depuis CS_TITLE, et c'est bien notre
octet qui l'en faisait sortir.

### 6.2 Les temoins, apparies

| temoin | avant (SS 419.7) | apres | |
|---|---|---|---|
| entrees dans CS_TITLE | **65** | **1** (image 307, tenue jusqu'a 1199) | paye |
| entrees dans CS_SIGNIN | 64 | **0** | paye |
| entrees dans WARNING | 64 | **0** | paye |
| lignes `[etape]` de CS_TITLE | 131 | **3** (0 -> 2 a 307, 2 -> 3 a 315) | paye |
| tirages par image, regime du titre | 337 **croissant** jusqu'a 3676 | **33 a 52, PLAT** sur 893 images | paye |
| images par seconde | 5,2 | **57,2** | paye |

La boucle est fermee : un seul titre, bati une fois, tenu 893 images. Et le
regime de tirages retombe sur celui que le SS 418 avait valide a l'oeil pour
un ecran-titre sain -- ~40 tirages par image
([[l-ecran-titre-par-une-cause-otee]]).

Les tirages oscillent, avec une pointe a 48-52 pendant ~200 images vers
l'image 650-850 puis un retour a ~34 : periodique, probablement la boucle
d'animation `loop_start`/`loop_end`. **Non lu.**

### 6.3 CORRECTION D'UN CHIFFRE DU SS 419.7

La section 14.3 de `MENU.md` donnait << plat a 150-200 tirages par image
jusqu'a l'image 300 >>. **C'est faux.** La ligne du journal est

```
tirages : ... DrawIndexedInstanced 1118 (+46)  sur 1 image(s)
```

et le `(+N)` porte sur la fenetre `sur N image(s)`, qui n'est pas toujours 1.
Pendant DATA_INITIALIZE la fenetre fait 50 images, donc 150 tirages y valent
**3,0 par image**, pas 150. Les valeurs de la phase de boucle, elles, etaient
bien par image (388 fenetres de 1 image sur 398) : **337 a l'image 350 puis
807, 1263, 1694, 2181, 2605, 3128, 3676** -- la croissance et sa conclusion
tiennent. Seul le plancher etait faux.

**Toujours diviser par la fenetre.** Un `(+N)` sans son << sur N image(s) >>
ne se lit pas.

### 6.4 CE QUI RESTE

1. **Le clavier etait eteint dans cette course, par choix** -- pour que la
   mesure reste attribuable a un seul changement. ENTREE n'a donc aucun effet,
   et c'est normal : `VF5_CLAVIER=1` le rallume
   ([[le-clavier-est-eteint-par-defaut]]).
2. **CS_TITLE n'est pas repasse par CS_DEMO** : 893 images tenues, soit
   ~15,6 s, et le retour a l'attract se fait sur `0x708` = 1800 tics. Il
   faudrait une course plus longue pour le voir.
3. **<< PRESS START BUTTON >> ne parait plus a l'ecran** (observation de
   l'utilisateur, 8 nov). Non explique, non mesure. L'etape 3 est atteinte et
   tenue ; les commandes 16 et 18, qui jouent les couches du titre, sont
   servies par le module lui-meme sous `VF5_TITRE_AET=1`. **A LIRE** :
   quelle couche porte ce texte, et qui la joue.

---

## 7. << PRESS START BUTTON >> : LU (SS 419.9, 8 novembre 2026)

**Lecture seule. Aucune course, aucun geste. Degre : ETAYE pour les
references croisees, SPECULATIF pour la cause de la disparition.**

### 7.1 Ce n'est PAS une couche AET

Le texte est une **chaine du module**, a `0x1803C78A8`, voisine de deux autres
derriere une table de pointeurs :

```
PRESS OPTIONS BUTTON    PRESS START BUTTON    FREE PLAY
```

C'est le bandeau de credits d'une borne. Les seuls noms de couche que
CS_TITLE etape 3 demande sont `logo_vf5` / `logo_vf5_short`, avec les
reperes `loop_start` / `loop_end` -- **un seul objet AET, l'id `0x16B`**.

### 7.2 Qui lit la chaine : `TaskInformation`

Trois references de donnees : `FUN_1800DA260` (deux fois) et
`FUN_1800D96E0`. Les deux sont des virtuelles de la **meme classe**, trouvee
par le RTTI :

```
vtable 0x1803C7848  ->  localisateur 0x1805E71E8  ->  descripteur 0x1806A51F8
                    ->  ".?AVTaskInformation@@"
```

C'est la tache **`[INFORMATION]`** que le journal de l'hote liste depuis le
debut de la chaine (6 taches a l'image ~300, 11 ensuite). `FUN_1800D96E0` est
sa mise a jour par image ; `FUN_1800DA260` est appelee par elle, et c'est son
**unique** appelant.

### 7.3 QUELLE formule, et c'est `DAT_180C8DE18` qui tranche

Dans les deux fonctions, le meme choix :

```c
pcVar = "PRESS OPTIONS BUTTON";
if (DAT_180c8de18 == '\0') pcVar = "PRESS START BUTTON";
```

`DAT_180C8DE18` est **l'un des quatre drapeaux `0x180C8DE18..1B`** que
`module_start` lit a `VF5FS+0x274777`, ceux que `VF5_CONSOLE` touche. Le MEME
drapeau choisit `logo_vf5` plutot que `logo_vf5_short` a l'etape 3 de
CS_TITLE. **Sa valeur dans nos courses n'est PAS mesuree** -- et elle compte :
s'il est non nul, le bandeau dirait << PRESS OPTIONS BUTTON >>, pas START.

### 7.4 LE CHEMIN CLIGNOTANT EST DU CODE MORT DANS REVO -- **REFUTEE AU SS 419.12**

> **CETTE SECTION EST FAUSSE.** Mesure du SS 419.12 : `mode[+0x74FEC8]` passe de 0 a 1 a l'image 316 et `compteur[+0x74FECC]` avance d'une unite par image. Le module les ECRIT, par un pointeur que les references croisees n'attribuent pas a ces adresses. Le chemin clignotant est VIVANT. Voir la section 12.3. Ce qui suit est garde pour la trace du raisonnement.

Dans `FUN_1800D96E0`, le dessin explicite
`FUN_1800D9ED0(&DAT_1807501B8, 2, texte)` est garde par deux conditions :

```c
if (((DAT_18074fec8 != 1) && (DAT_18074fec8 != 2)) || ...
   || (((ulonglong)_DAT_18074fecc / 0x1e & 1) == 0)) goto LAB_1800d9827;
```

`/ 0x1e & 1` est un **clignotant de 30 images**. References croisees,
**mesurees** :

| global | references | ecritures | valeur statique |
|---|---|---|---|
| `DAT_18074FEC8` | **7, toutes READ** | **0** | `00 00 00 00` |
| `DAT_18074FECC` | **1, un READ**, depuis la fonction qui s'en sert | **0** | `00 00 00 00` |

**Personne, dans tout le module, n'ecrit ni le mode ni le compteur.** A 0, la
premiere condition (`!=1 && !=2`) est vraie : on saute le dessin, toujours.
**Le bandeau clignotant ne peut pas paraitre.** Ce sont les globales de
credits d'une borne ; leur ecrivain est dans ce que REVO a retire avec le mode
APM3 ([[les-classes-apm3-ne-sont-pas-reintegrables]]).

### 7.5 Ce qui reste donc, et ce qui n'est PAS la cause

`FUN_1800DA260(&DAT_1807501B8, 0, DAT_1807501B8)` est appelee
**inconditionnellement** a `LAB_1800D9827`, et elle choisit les memes chaines
sans passer par le clignotant. Un bandeau FIXE pourrait donc etre dessine la.
**Non mesure.**

**Le geste du SS 419.8 ne touche RIEN de tout ceci** : ni ces globales, ni
cette tache, ni ces branches. La disparition n'en vient pas.

**HYPOTHESE, SPECULATIF :** dans la course en boucle, 65 animations `logo_vf5`
se superposaient, chacune a un point different de sa ligne de temps ; il n'y en
a plus qu'une, tenue entre `loop_start` et `loop_end`. Si l'image du texte vit
dans l'AET **hors** de ce segment, elle paraissait alors et ne parait plus.
`FUN_180026220(obj, 0)` -- appelee seulement pour `logo_vf5` -- est le candidat
qui poserait ce segment : `FUN_180024450(DAT_1806AF3D0, obj, 0)`, **non lue**.

### 7.6 Pour trancher, par ordre de cout

1. **Lire** `FUN_180024450` : que fait le `0` passe apres l'objet ?
2. **Mesurer** `DAT_180C8DE18` dans une course : la formule attendue n'est
   peut-etre pas celle que l'utilisateur cherche.
3. **Mesurer** si `[INFORMATION]` est vivante et en phase 2, et si le dessin
   de `FUN_1800DA260` est atteint.

---

## 8. L'AetObj : SON CURSEUR DE TEMPS ET SON BOUCLAGE (SS 419.10)

**Lecture seule, desassembleur. Aucune course.**

### 8.1 MON HYPOTHESE DU 7.5 EST REFUTEE

J'avais suppose que `FUN_180026220(obj, 0)` **gelait** l'animation. Non.

La chaine, desassemblee parce que Ghidra perd les parametres ici
([[la-decompilation-ghidra-perd-des-parametres]]) :

```asm
FUN_180024450:
  VMOVAPS XMM6, XMM2          ; le 3e argument est un FLOTTANT, pas un entier
  CALL    0x180023880         ; cherche l'objet par son numero
  MOV     RCX, [RAX]          ; sa vtable
  VMOVAPS XMM1, XMM6
  MOV     RDX, [RCX + 0x60]
  CALL    RDX                 ; obj->virtuelle_0x60(obj, 0.0f)
```

`AetObj` a sa vtable a **`0x180374240`** (par le RTTI, `CLASSES_RTTI_REVO.txt`),
et son slot `+0x60` est `FUN_180024490`, **une seule instruction** :

```asm
VMOVSS dword ptr [RCX + 0x88], XMM1
RET
```

Donc `FUN_180026220(obj, 0)` ecrit **`0.0f` dans `AetObj+0x88`**.

### 8.2 CE QUE SONT CES CHAMPS -- lus dans l'avance de l'AetObj

La virtuelle `+0x20` de l'`AetObj`, `FUN_180020F80`, est son avance par image,
et elle nomme tout le bloc :

```asm
EDX = [RCX+0x30]                  ; les DRAPEAUX
if (EDX & 4) return 0;            ; bit 2 : en pause, on n'avance pas
RAX = [RCX+0x10]                  ; la composition
R8  = &[RCX+0x88]                 ; <<<< LE CURSEUR DE TEMPS
XMM0 = [RAX+0x0C]                 ; la cadence de la composition
XMM1 = XMM0 * [RCX+0x74]          ; x la VITESSE de l'objet
XMM2 = XMM1 / [0x1803744F8]       ; / une constante
XMM1 = [R8]                       ; le temps courant
if (EDX & 2) { [R8] = XMM1 - ... } ; marche ARRIERE
else {
    XMM0 = [RCX+0x2C]             ; l'image de FIN
    [R8] = XMM2 + XMM1            ; temps += dt
    if (temps > fin) {
        if (BT EDX,0x10) [R8] = [RCX+0x28];   ; BOUCLE : retour au DEBUT
        else if (!BT EDX,0x11) rend 1;        ; FINI
        else { EDX |= 1; [R8] = fin; }        ; cloue a la fin
    }
}
```

| champ | sens | degre |
|---|---|---|
| `AetObj+0x28` | image de DEBUT de boucle | ETAYE |
| `AetObj+0x2C` | image de FIN de boucle | ETAYE |
| `AetObj+0x30` | drapeaux : bit 2 pause, bit 1 marche arriere, bit 16 boucler, bit 17 clouer a la fin | ETAYE |
| `AetObj+0x74` | VITESSE (multiplie la cadence) | ETAYE |
| `AetObj+0x88` | **CURSEUR DE TEMPS** | ETAYE |

**Le `0` est donc un REMBOBINAGE a l'image 0, pas un gel.** La vitesse est en
`+0x74`, un autre champ, et le titre n'y touche pas.

### 8.3 CE QUE CELA DIT DU TEXTE MANQUANT

L'objet du titre est cree avec, dans sa demande, **`0x10000` en `+0x28`** --
et `0x10000` est `1 << 16`, le bit du **bouclage** dans les drapeaux lus
ci-dessus. Le menu passe le meme `0x10000` a `FUN_180025EB0(0x2A3, "bg_base",
1, 0x10000, "neu_s", "neu_e")`. **CORRIGE AU SS 419.11 : c'est ETAYE.** La traduction est
`FUN_180023F40`, la virtuelle `+0x08` de l'`AetObj` :
`drapeaux = demande[0x28] & 0xFFFF0000`, et `0x10000` est bien le bit 16.
Voir la section 9. **Et le curseur nait a `loop_start`, pas a 0** : c'est le
rembobinage qui le met a 0.

Si c'est bien le bouclage, alors le curseur part de **0** (notre
rembobinage), monte jusqu'a `loop_end`, puis **retombe sur `loop_start`, pas
sur 0**. Le segment `[0, loop_start)` est donc joue **UNE SEULE FOIS**, au
tout debut, et plus jamais.

**D'ou une explication, PROBABLE :** dans la course en boucle, l'etape 3 de
CS_TITLE tournait **65 fois** et creait 65 objets `logo_vf5`, chacun rembobine
a 0 : le segment d'introduction etait rejoue sans arret, par l'un ou l'autre.
Maintenant l'etape 3 tourne **une fois** : l'introduction passe une fois, puis
le curseur boucle dans `[loop_start, loop_end)` pour toujours. Si l'image du
texte vit hors de cette fenetre, elle a paru brievement au debut et ne
reparaitra plus.

**Ce n'est pas une regression du SS 419.8** : ce geste ne touche ni l'AetObj,
ni ses drapeaux, ni `TaskInformation`. Il a seulement fait que l'etape 3 ne
tourne plus qu'une fois -- ce qui est le comportement du binaire.

### 8.4 LE CANDIDAT CONCURRENT, NON ECARTE

`FUN_1800DA260(&DAT_1807501B8, 0, DAT_1807501B8)` est appelee
**inconditionnellement** par `FUN_1800D96E0` (section 7.5), sans passer par le
clignotant mort. Si `TaskInformation` est vivante et en phase 2, elle tourne a
chaque image et choisit les memes chaines. **Non mesure.** Deux candidats
restent donc : la fenetre de boucle de l'AET, ou ce chemin-la.

### 8.5 CE QUI TRANCHERAIT, et c'est une MESURE

Relever, pour l'objet `0x16B` du titre : `+0x88` (curseur), `+0x28` / `+0x2C`
(la fenetre), `+0x30` (les drapeaux) et `+0x74` (la vitesse), sur quelques
centaines d'images. Si le curseur boucle dans une fenetre qui ne contient pas
0, la section 8.3 est payee. L'hote sait deja ou vivent les noeuds du titre
([[ou-vit-l-ecran-titre-couche-0-creneau-1]]), mais **la sonde reste a
ecrire**, et [[un-invariant-sur-un-conteneur-vide-ne-verifie-rien]] vaut ici :
elle doit pouvoir echouer.

---

## 9. LA TRADUCTION, LUE : `0x10000` EST BIEN LE BIT DE BOUCLAGE (SS 419.11)

**Lecture seule. Le 8.3 passe de PROBABLE a ETAYE, et il gagne une nuance qui
change son sens.**

### 9.1 La chaine, en entier

| etape | fonction | ce qu'elle fait |
|---|---|---|
| 1 | `FUN_180025110(dst, src)` | **constructeur de COPIE** de la demande, champ par champ. **Aucune traduction.** |
| 2 | `FUN_1800222A0(mgr, demande)` | batit un `AetObj` dans une locale, puis l'insere dans le conteneur `mgr+0x60` sous un numero neuf (`mgr+0x78`) |
| 3 | `FUN_180023DB0` | resout le jeu, la composition et les DEUX reperes nommes, puis appelle la virtuelle `+0x08` de l'`AetObj` |
| 4 | **`FUN_180023F40`** (= `AetObj` slot `+0x08`) | **la traduction** |

### 9.2 Le point qui portait la conclusion

Dans `FUN_180023F40`, deux lignes :

```c
uVar4 = param_2[10] & 0xffff0000;      // param_2 = la DEMANDE, dword [10] = octet 0x28
*(uint *)(param_1 + 0x30) = uVar4;     // -> les DRAPEAUX de l'AetObj
```

`param_2[10]` est l'octet **`0x28`** de la demande -- exactement la ou CS_TITLE
etape 3 ecrit **`0x10000`**. Le masque `0xFFFF0000` ne garde que la moitie
haute, et `0x10000 & 0xFFFF0000 = 0x10000` = **bit 16**. Or le bit 16 est
precisement celui que l'avance teste par `BT EDX, 0x10` pour reboucler sur
`+0x28` (section 8.2).

**Donc : ETAYE. `0x10000` dans la demande EST le bit de bouclage.** Les 16 bits
BAS du meme champ sont masques -- ils ne sont pas des drapeaux.

### 9.3 Ce que la meme fonction nomme en plus

| ecriture | source | sens |
|---|---|---|
| `+0x28` / `+0x2C` | d'abord la composition (`+4`, `+8 - 1.0`), puis `param_5`, puis **les deux reperes resolus** `param_6` / `param_7` | **les reperes `loop_start` / `loop_end` POSENT la fenetre de boucle** |
| `+0x28` / `+0x2C` | `demande[8]` / `demande[9]` (octets `0x20` / `0x24`), **seulement si >= 0.0** | surcharges explicites. CS_TITLE y met `0xBF800000` = **-1.0** deux fois, donc : << emploie les reperes >> |
| `+0x30` bit 1 | pose tout seul si `fin < debut` | marche arriere, avec echange des deux bornes |
| **`+0x88`** | `blend(fin, debut, (drapeaux & 2) == 0)` | **le curseur est initialise au DEBUT DE LA FENETRE** (ou a la fin en marche arriere) |
| `+0x94` / `+0x98` | +-1.0 selon les bits 18 et 19 | miroir en X et en Y |
| `+0x74` | `demande[0x1c]` (octet `0x70`) | la vitesse |
| `+0x10` / `+0x18` / `+0x20` | la composition, un parametre, le repere | les ressources de l'objet |

### 9.4 LA NUANCE QUI CHANGE LE SENS DU 8.3

**Le curseur ne nait PAS a zero : il nait a `loop_start`.** C'est
`FUN_180026220(obj, 0.0f)` -- le rembobinage que CS_TITLE etape 3 appelle
juste apres, **et seulement pour `logo_vf5`, pas pour `logo_vf5_short`** -- qui
le ramene a l'image 0, donc AVANT la fenetre.

La ligne de temps est donc, ETAYEE de bout en bout :

```
0 .............. loop_start .............. loop_end
|<-- joue UNE SEULE FOIS -->|<--- boucle pour toujours --->|
^ le rembobinage nous met ici
```

Sans ce rembobinage, l'introduction ne serait **jamais** jouee. Avec, elle
l'est **une fois**. Et dans la course en boucle, l'etape 3 tournait 65 fois :
l'introduction redemarrait sans arret, par un objet ou par un autre.

**Si l'image du texte vit dans `[0, loop_start)`, elle paraissait alors et ne
reparait plus** -- et c'est le comportement du binaire, pas une regression du
SS 419.8. Reste **PROBABLE** : ou vit cette image dans la composition n'est pas
mesure.

### 9.5 Et le candidat concurrent reste ouvert

Le texte peut tout aussi bien venir de `TaskInformation` par le
`FUN_1800DA260` inconditionnel (section 7.5). Un vrai ecran-titre de VF5FS
fait CLIGNOTER << PRESS START BUTTON >> ; or le seul clignotant du module est
mort faute d'ecrivain (section 7.4). **Les deux pistes tiennent encore, et
seule une sonde les departage** : relever `+0x88`, `+0x28`, `+0x2C`, `+0x30`,
`+0x74` de l'objet `0x16B`, et l'etat de la tache `[INFORMATION]`.

---

## 10. LE BANDEAU : LA CAUSE EST LUE, ET C'EST LE MOTIF POUR LA 3e FOIS
## (SS 419.12)

**Lecture. La sonde est ecrite et l'hote compile. RIEN N'A TOURNE.**

### 10.1 Le dessinateur unique, et sa porte

Les deux chemins de la section 7 -- le clignotant mort de `FUN_1800D96E0` et
le `FUN_1800DA260` inconditionnel -- aboutissent au **MEME** dessinateur,
`FUN_1800D9ED0` (VF5FS+0xD9ED0). Et il ouvre sur ceci :

```c
void FUN_1800d9ed0(obj, int quoi, const char *texte)
{
  if ((DAT_180c8df28 == 0) || (*(longlong *)(DAT_180c8df28 + 0x1ff08) == 0)) {
      ...  FUN_18010D470(x, y, 9);  FUN_18010DC00(0x19);
           FUN_18010D660(&DAT_1803758C0, texte);  ...
  }
  return;
}
```

**C'est le motif, pour la TROISIEME fois :**

| ecran | fonction | porte |
|---|---|---|
| CS_TITLE (SS 418) | `FUN_1800E5ED0` etapes 1, 2, 3 | `bloc+0x1FF08 == 0` |
| MENU_MAIN (SS 419.6) | `FUN_18020F1E0` | `bloc+0x1FF08 == 0` |
| **le bandeau** (ici) | **`FUN_1800D9ED0`** | **`bloc+0x1FF08 == 0`** |

Avec notre repartiteur installe, le module **ne dessine rien** -- et, cette
fois, **il ne delegue rien non plus** : il n'y a AUCUNE commande dans cette
branche. Le module suppose simplement un hote qui a son propre bandeau.

### 10.2 CE QUI EXPLIQUE L'OBSERVATION, et la cause est CHEZ NOUS

Le bandeau ne peut donc paraitre que sur les images ou **nous** annulons le
repartiteur. Aujourd'hui, c'est uniquement la fenetre de `VF5_TITRE_AET` :
les etapes 2 et 3 de CS_TITLE phase 0, que le journal compte a **9 images**.

- Course en boucle (SS 419.7) : l'etape de CS_TITLE oscillait 0 -> 3 **131
  fois**, donc ces fenetres revenaient sans arret et le bandeau etait dessine
  tres souvent.
- Depuis le SS 419.8 : CS_TITLE entre **une fois**, la fenetre dure **9
  images**, et plus jamais.

**C'est l'explication de la disparition, et sa cause est notre repartiteur --
pas une regression du correctif de la commande 242**, qui ne touche ni ce
dessinateur, ni cette tache, ni ce drapeau.

Cela **annule le besoin** de l'hypothese de la fenetre de boucle AET
(section 8.3) : elle n'est pas refutee, elle n'est plus necessaire.

### 10.3 ET LE GESTE N'EST PAS DE LA MEME FORME -- donc il n'est PAS pose

Les deux appelants de `FUN_1800D9ED0` sont des virtuelles de
`TaskInformation`, donc une mise a jour **par image**. Annuler le repartiteur
pendant une initialisation ponctuelle, comme aux SS 418 et 419.6, ne sert a
rien ici : il faudrait l'annuler pendant toute la vie de la tache, c'est-a-dire
toute la course, ce qui couperait tout le reste.

**CORRIGE AU SS 419.13 (section 12) : le geste EST nommable.** Le
raisonnement ci-dessus est juste pour TOUTE la course, et faux pour CS_TITLE
seul -- ou le module n'a rien a deleguer. Annuler le repartiteur pendant tout
CS_TITLE suffit, et les quatre lectures qui le paient sont en section 12.

### 10.4 LA SONDE, ecrite (`VF5_SONDE_BANDEAU=<image>`, defaut ETEINT)

Elle releve six images a partir de l'image donnee, et ne change rien :

- `"INFORMATION"` est-elle dans la liste vivante (`VF5FS+0xEA7608`), et avec
  quelle phase / quel drapeau de vie ;
- la valeur VIVE de `bloc+0x1FF08`, et si l'hote l'annule pour cette image ;
- `mode[+0x74FEC8]`, `compteur[+0x74FECC]`, `etat[+0x7501B8]` ;
- les quatre drapeaux console `+0xC8DE18..1B`, **et la formule qui en
  decoule** : nul -> << PRESS START BUTTON >>, non nul -> << PRESS OPTIONS
  BUTTON >>.

**L'AUTO-TEST PEUT ECHOUER, et il le dit :**

1. si `"INFORMATION"` n'est pas dans la liste vivante, la sonde l'ecrit et ne
   releve **rien d'autre** -- parce qu'alors ses virtuelles ne tournent pas et
   le bandeau ne peut pas etre dessine, quel que soit le repartiteur ;
2. si elle est trouvee mais que ni le noeud ni l'objet qu'il pointe ne portent
   une phase dans `0..3` et une vie dans `{0,1}`, elle l'ecrit et s'arrete la.

C'est la lecon du SS 404 -- une sonde qui n'imprime jamais -- et de
[[un-invariant-sur-un-conteneur-vide-ne-verifie-rien]].

---

## 11. LA SONDE A TOURNE : la cause est PAYEE, et ma section 7.4 est REFUTEE
## (SS 419.12, course de 500 images, sonde a l'image 313)

**L'auto-test est passe** : `"INFORMATION"` est dans la liste vivante,
`vivante=1 phase=2`, lus sur l'objet que pointe le noeud. La tache tourne donc
sa mise a jour a chaque image, et ses deux virtuelles avec.

### 11.1 Le releve brut, six images

| image | `bloc+0x1FF08` | l'hote | `mode +0x74FEC8` | `compteur +0x74FECC` | `etat +0x7501B8` |
|---|---|---|---|---|---|
| 313 | **0** | ANNULE | 0 | 12 | 2 |
| 314 | **0** | ANNULE | 0 | 13 | 2 |
| 315 | **0** | ANNULE | 0 | 14 | 2 |
| 316 | **0** | laisse en place | **1** | 15 | 2 |
| 317 | `7FF72BFCEC60` | laisse en place | 1 | 16 | 2 |
| 318 | `7FF72BFCEC60` | laisse en place | 1 | 17 | 2 |

Drapeaux console `+0xC8DE18..1B` = **`00 00 01 00`** sur les six images.

### 11.2 CE QUI EST PAYE

1. **La cause.** Le repartiteur est NUL aux images 313 a 316 et non nul des
   317. `FUN_1800D9ED0` ne dessine que sur les premieres. Le bandeau ne peut
   donc paraitre que dans la fenetre de `VF5_TITRE_AET` -- les images 307 a
   316 -- et **plus jamais ensuite**. C'est exactement la lecture de la
   section 10, et c'est mesure.
2. **La formule.** `DAT_180C8DE18 = 0x00`, donc c'est bien
   << **PRESS START BUTTON** >>, pas << PRESS OPTIONS BUTTON >>.
3. **Les deux autres drapeaux console**, au passage : `DAT_180C8DE19 = 0`
   (d'ou l'etape 3 de CS_TITLE qui prend la branche AET) et
   `DAT_180C8DE1A = 1` (d'ou le masque de boutons `8` au lieu de `0x1FF` dans
   `FUN_1801B2390`).

### 11.3 CE QUI EST REFUTE -- par moi, contre moi

La section 7.4 concluait : << le chemin clignotant est du code MORT dans
REVO >>, parce que les references croisees donnaient **7 lectures et 0
ecriture** pour `DAT_18074FEC8`, et **1 lecture, 0 ecriture** pour
`DAT_18074FECC`. **C'est faux :**

- `mode[+0x74FEC8]` **passe de 0 a 1 entre l'image 315 et l'image 316** ;
- `compteur[+0x74FECC]` **avance d'une unite par image** : 12, 13, 14, 15, 16, 17.

L'hote ne les ecrit pas (verifie : les quatre seules occurrences dans
`vf5fs_host.cpp` sont les lectures de ma propre sonde). **C'est donc le module
qui les ecrit, par un pointeur que Ghidra n'attribue pas a ces adresses.**

Avec `mode = 1`, la premiere garde de `FUN_1800D96E0` (`!=1 && !=2`) est
FAUSSE : le chemin clignotant **est vivant**. Et `(compteur / 30) & 1` fait
exactement ce qu'il annonce -- 30 images cache, 30 images visible.

**La lecon :** << 0 ecriture dans les references croisees >> ne veut pas dire
<< jamais ecrit >>. Une ecriture faite par la base d'une structure n'est
attribuee a aucun champ. **Pour une valeur, la seule preuve est de la LIRE a
l'execution.** La sonde que j'avais ecrite pour une autre question est ce qui
m'a corrige.

### 11.4 OU EN EST LA QUESTION

Le bandeau est calcule, la tache vit, le clignotant tourne, la formule est la
bonne -- et **la seule chose qui l'empeche d'etre dessine est la presence de
notre repartiteur**. Il est donc dessine aux images 307-316 et nulle part
ailleurs.

**La reparation est nommable, pour la premiere fois :** annuler le repartiteur
**pendant tout CS_TITLE**, et pas seulement aux etapes 2 et 3 de sa phase 0.
Sur cet ecran le module dessine tout lui-meme, donc il n'a aucune raison de
voir un repartiteur. Deux consequences lues, pas supposees :

- la sortie de la phase 1 n'appellerait plus la commande `0x19E` = 414, qui
  est elle-meme sous `if (bloc+0x1FF08 != 0)` ;
- `FUN_1801B2390` ne poserait plus la commande 242 du tout, et son octet
  resterait a 0 -- ce qui est exactement ce que le SS 419.8 veut.

Le mecanisme existe deja (`VF5_SANS_RAPPEL=<sous-etats>`), et
[[la-reparation-du-titre-porte-sur-tout-cs-title]] dit comment borner :
par la phase `mo+0x28`, pas par l'etape `mo+0x34`. **Rien n'est pose.**

---

## 12. LA BORNURE A LA PHASE 0 EST OTEE : TOUT CS_TITLE (SS 419.13)

**Lecture, puis geste. L'hote compile. RIEN N'A TOURNE.**

Le SS 418.3 avait resserre la reparation a `phase == 0 && (etape == 2 || 3)`,
pour une seule raison : garder le repartiteur PRESENT en phase 1 afin que
`FUN_1800E55B0` puisse poser la commande 414 a la sortie du titre. **Cette
raison ne tient pas**, et les quatre lectures qui l'annulent sont faites.

> **AVERTISSEMENT (SS 419.14, section 13) : le compte d'appels donne ci-dessous
> est INCOMPLET.** La phase 1 delegue **QUATRE** commandes -- 212, 225, 242 et
> 414 -- parce que `iVar2` a DEUX sources. La section 13 les table toutes les
> quatre et **renforce** la conclusion : aucune ne change de comportement quand
> le repartiteur est nul.

### 11.1 La sortie par appui SURVIT -- le `return 1` est hors de la garde

`VF5RE/code_decompile/FUN_1800e55b0.c`, lu en entier :

```c
if (-1 < iVar2) {
  if ((DAT_180c8de18 == '\0') || ((bloc+0x10 & 2) != 0)) {
      bloc+0x10 |= 0x14;
      FUN_180194800(0, "sy_charin00st");          // le son de validation
      FUN_1801b3600(0);
      if (*(longlong *)(bloc + 0x1ff08) != 0) {   // <-- la garde
        if (FUN_1802c5090() == '\0') { ... repartiteur(ctx, 0x19e, 0); }
      }
      return 1;                                   // <-- AU MEME NIVEAU, APRES
  }
  bloc+0x10 |= 8;
}
```

**Seule la commande 414 est sautee.** Le son, les drapeaux et le `return 1`
sont tous hors de la garde.

### 11.2 Et l'hote ne fait RIEN de la commande 414

Mesure : `grep` sur l'hote ne trouve **aucun `case 414`** ni `case 0x19e`. Elle
tombe donc au `default:` du repartiteur, qui journalise le site d'appel et rend
le `ret = 1` initial -- << c'est fait >> sans rien faire. **Rien n'est perdu.**

### 11.3 La commande 242 se degrade DU BON COTE

`FUN_1801b2390` pose son octet local **avant** sa garde :

```c
local_res8[0] = '\0';                               // <-- AVANT
if ((bloc + 0x1ff08 != 0) && (*(code **)(bloc + 0x1ff08) != 0)) {
    repartiteur(ctx, 0xf2, local_res8);
}
...
if ((uVar4 & uVar3) == 0) {                         // aucun bouton
    iVar2 = -1;
    if (local_res8[0] != '\0') iVar2 = iVar1;
    return iVar2;                                   // -1 : le titre TIENT
}
return iVar1;                                       // bouton : il SORT
```

Repartiteur nul => la 242 n'est pas posee du tout, l'octet reste 0, et la
fonction rend -1 sans appui, `iVar1` sur appui. **C'est exactement ce que le
correctif du SS 419.8 obtient en REPONDANT 0 ; ici on l'obtient en OTANT
l'appel.** Les deux sont d'accord, et celui-ci ne depend plus de notre reponse.

### 11.4 Et c'est LA CAUSE DU BANDEAU (section 10)

`FUN_1800D9ED0`, unique dessinateur de << PRESS START BUTTON >>, ouvre sur
`if (bloc == 0 || bloc+0x1FF08 == 0)`, et ses deux appelants sont des
virtuelles de `TaskInformation` : une mise a jour **par image**. Borner a la
phase 0 le rendait donc invisible des l'entree en phase 1 -- ce que la course
du SS 419.9 a montre a l'ecran.

**La section 10.3 disait << annuler le repartiteur toute la vie de la tache
couperait tout le reste >>. C'etait vrai pour toute la course ; c'est FAUX pour
CS_TITLE, ou il n'y a rien a deleguer.** C'est ce qui rend le geste nommable.

### 11.5 Ce que les deux autres etapes gagnent

| etape | aujourd'hui (repartiteur present) | apres (nul) |
|---|---|---|
| 0 | cmd 113 (`FUN_1802316E0(0x44A)` + bool), 114 par image, 115 a la sortie | **sautees** -- elles sont des no-op ASSUMES chez nous, et le passage a l'etape 1 ne depend que de `FUN_1802C8460()`, hors de la garde. Rien n'est perdu. |
| 1 | cmd 15 ; notre `case 15` rend **0**, donc `iVar7 != 2` est VRAI et le module demande `rom/movie/vf5title_bg.sfd` | `FUN_1801960A0(0x15F)` + `FUN_180026180(0x12E)`, ses propres chargeurs. **Un GAIN** : FS n'a pas de film de titre. |
| 2, 3 | deja nuls depuis le SS 418 | inchange |

### 11.6 LE GESTE, et son temoin

`parTitre` passe de
`(scTA == 5) && (phSR == 0) && (etTA == 2 || etTA == 3)` a **`(scTA == 5)`**.
Aucun interrupteur neuf : `VF5_TITRE_AET` reste a **1 par defaut**, et son
sens s'elargit. La cle de dedoublonnage du journal devient le **couple**
(phase, etape), parce que `mo+0x34` reste a 3 toute la phase 1 -- sans quoi la
ligne n'aurait jamais reimprime au passage qu'on elargit.

**TEMOIN A LIRE, dans cet ordre :**

1. **les tirages par image** -- `40,3` est la marque de la version large
   (SS 412), `2,00` celle de l'absence de reparation. En dessous de 40, la
   phase 1 ne dessine pas et la lecture est fausse quelque part.
2. **la ligne `419.12`** doit montrer le repartiteur **NUL au-dela de l'image
   317**, et `"INFORMATION"` vivante en phase 2.
3. **une seule entree dans CS_TITLE**, comme au SS 419.8 : si la boucle
   revient, c'est la 242 et non le bandeau.

---

## 13. CORRECTION : LA PHASE 1 DELEGUE **QUATRE** COMMANDES (SS 419.14)

**Lecture seule, apres le geste du SS 419.13. L'hote compile. RIEN N'A
TOURNE.**

La section 12 affirmait que << les seuls appels que la phase 1 delegue sont la
242 et la 414 >>. **C'etait faux.** Je n'avais pas suivi la SECONDE source de
`iVar2`. L'en-tete de `FUN_1800E55B0`, relue :

```c
iVar2 = FUN_1801b2390();                       // cmd 242  (0xF2)
if (FUN_1802cb570() != '\0') {                  // cmd 212  (0xD4)
  if (FUN_1802cb830() != '\0') {                // cmd 225  (0xE1)
    if (0xb4 < (uint)(*(int *)(DAT_180ec2f40 + 0x68) - _DAT_1807514dc)) {
      iVar2 = FUN_1801b2280();                 // presence de manette
    }
  }
}
if (-1 < iVar2) { ... sortie du titre ... }
```

### 12.1 Ce que fait vraiment `FUN_1801B2280`

Elle **ne touche pas le repartiteur**. Elle lit `FUN_18000BA10()` (le port
courant) puis la table des manettes `DAT_180795950` **au pas de 0x54**, et rend
l'index du port present, sinon `0xFFFFFFFF`. Le pas concorde avec celui de
`FUN_1801B2390`, qui lit `(&DAT_180795960)[i * 0x15]` -- 0x15 dwords = 0x54
octets. Donc `+0x00` du dossier est un octet de presence et `+0x10` le masque
des boutons.

**C'est donc le chemin de sortie SANS BOUTON** : au-dela de 180 tics (~3 s),
la seule PRESENCE d'une manette suffit a rendre `iVar2 >= 0` et a faire sortir
le titre. Voir [[le-clavier-est-eteint-par-defaut]] et
[[les-manettes-se-posent-dans-le-bloc]] : `VF5_MANETTE` declare justement une
presence.

### 12.2 Mais ses deux portillons sont DEJA fermes, par nous

`FUN_1802CB570` et `FUN_1802CB830` ont la meme forme : poser une commande,
rendre `iVar1 == 1`, et rendre `false` si le repartiteur est nul.

| cmd | fonction | notre reponse AUJOURD'HUI | repartiteur NUL |
|---|---|---|---|
| **212** (0xD4) | `FUN_1802CB570` | **2** hors STARTUP (`g_titreSortie` = `true` par defaut) -> `false` | `false` : **IDENTIQUE** |
| **225** (0xE1) | `FUN_1802CB830` | **2** en dur depuis le SS 76 -> `false` | `false` : **IDENTIQUE** |
| **242** (0xF2) | `FUN_1801B2390` | **0** (SS 419.8) | pas posee, octet pre-zerofie : **IDENTIQUE** |
| **414** (0x19E) | notification de sortie | **aucun `case`**, defaut 1, personne ne la lit | pas posee : **rien n'est perdu** |

### 12.3 LA CONCLUSION EST RENFORCEE, PAS AFFAIBLIE

Les quatre lignes sont soit identiques, soit sans consequence. **Sur la phase
1, l'elargissement du SS 419.13 ne change RIEN, sauf qu'il rend le bandeau
dessinable.** Avant cette lecture, c'etait un pari sur deux commandes ; c'est
maintenant une table sur quatre.

Le chemin de sortie a 180 tics est **doublement ferme** par nos reponses 2/2 --
et il l'etait avant le geste. S'il faut un jour que le titre avance tout seul,
le levier est la : **deux commandes, pas un minuteur**.

### 12.4 LA LECON

J'ai ecrit << les seuls appels >> apres avoir lu UNE des deux sources de
`iVar2`. Le compte etait verifiable en quatre lignes de la meme fonction que
j'avais sous les yeux, et une fiche de memoire portait deja l'avertissement :
[[compter-avant-d-annoncer-un-nombre]]. << Seuls >> et << tous >> sont des
quantificateurs : ils demandent un COMPTE, pas un echantillon.

---

## 14. LE MASQUE DES BOUTONS ACCEPTES VAUT `0x8` (SS 419.15)

**Lecture, et relecture d'un journal DEJA ecrit. Aucun geste. RIEN N'A
TOURNE.**

L'observation << la touche entree n'a aucun effet >> est restee ouverte
plusieurs seances. Elle a une explication **mesuree**, et elle n'est pas dans
notre code clavier.

### 14.1 La chaine, reduite a sa plus simple expression

`FUN_18000BA10` est un **`return 0` en dur** (decompile : deux instructions).
Donc dans `FUN_1801B2390` le port consulte est **toujours 0**, la boucle de
balayage ne tourne jamais, et la fonction se reduit a :

```c
uVar4 = 0x1ff;
if (DAT_180c8de1a != '\0') uVar4 = 8;        // <-- le masque
...
uVar3 = (&DAT_180795960)[0];                 // boutons du port 0
if ((uVar4 & uVar3) == 0) { ... return -1; } // le titre TIENT
return 0;                                    // il SORT
```

### 14.2 Et le masque est MESURE, pas deduit

Le journal de la course du SS 419.8 porte deja la ligne, par la sonde du
SS 339 :

```
0x1801B2390 rend -1   | octet de la 242 = -1  | masque [0xC8DE1A]=1 -> 0x8
boutons [0x795960] p0=0x00000000 p1=0x00000000   | presence [0x795950] p0=0 p1=0
```

Et la sonde du bandeau le confirme par l'autre bout :
`drapeaux console[+0xC8DE18..1B]=00 00 01 00`, donc `DAT_180C8DE1A = 1`.

**Le masque vaut `0x8` : un seul bit accepte, le bit 3.**

### 14.3 Or l'hote met ENTREE sur le bit 8

`CLV_START = 1u << 8` et `start = tenu(VK_RETURN)`. Donc
**`0x100 & 0x8 = 0`** : ENTREE ne peut pas faire sortir le titre par ce
predicat. Le bit 3 est `CLV_Y`, que l'hote cable sur **`W`** (Garde).

### 14.4 CE QUI RESTE INCONNU, et c'est le point qui decide

L'hote ecrit l'etat des boutons dans **`bloc+0x20`** (mesure :
`bloc+0x20 = 0x00000100 [START]`). Le module, lui, lit **`VF5FS+0x795960`**.
**Rien ne mesure que ces deux tables numerotent les bits pareil**, et la table
de l'hote marque elle-meme `CLV_A`/`B`/`Y` comme NON CONFIRMES -- seuls
`UP..RIGHT` viennent de l'enum pxd.

Deux lectures tiennent donc, et elles se departagent par une seule mesure :

| hypothese | consequence | ce qui la soutient |
|---|---|---|
| **(a)** le bit 3 est bien Garde | le titre veut Garde, et `W` le fait sortir | la table de l'hote |
| **(b)** le bit 3 est START dans la numerotation du MODULE | notre hote met START sur le mauvais bit | l'ecran dit << PRESS START BUTTON >>, et un ecran-titre de console accepte START |

**(b) est la plus vraisemblable** -- un ecran qui reclame START n'accepte pas
la seule garde -- mais elle n'est pas mesuree, et je ne touche a rien avant.

### 14.5 LA MESURE QUI TRANCHE, et la sonde existe deja

La sonde du SS 339 imprime deja `boutons [0x795960] p0=0x%08X`. Il suffit
d'une course avec **`VF5_CLAVIER=1`** en tenant une touche :

- si tenir **ENTREE** fait apparaitre `0x00000008` -> hypothese **(b)**, le
  module renumerote, et notre `CLV_START` est a corriger ;
- si tenir ENTREE donne `0x00000100` et tenir **W** donne `0x00000008`, ->
  hypothese **(a)**, la numerotation est partagee et le titre veut vraiment la
  garde ;
- si les deux donnent `0x00000000`, le pont `bloc+0x20` -> `+0x795960` ne
  passe pas du tout, et c'est LUI le defaut.

**Limite de l'instrument, a dire avant la course** : cette sonde est bornee a
`if (sCour == 8)`, donc elle n'imprime **que pendant CS_DEMO**. Il faut tenir
la touche a ce moment-la, pas sur l'ecran-titre.

### 14.6 ET UNE AFFIRMATION A MOI QUI TOMBE

Ma fiche `le-clavier-est-eteint-par-defaut` disait : << l'appui FAIT SORTIR
CS_TITLE : sous-etats 2=WARNING et 6=CS_SIGNIN atteints >>. **Cette mesure
date de l'epoque de la boucle** (SS 419.7), ou la chaine parcourait
CS_TITLE -> CS_SIGNIN -> WARNING **toute seule, 64 fois**, parce que l'octet
de la 242 valait 1. Atteindre ces deux sous-etats ne prouvait donc rien sur
l'appui. La moitie mesuree de la fiche reste vraie (ENTREE pose bien le bit 8
dans `bloc+0x20`) ; la conclusion qu'on en tirait, non.

### 14.7 ET LA PREMIERE CAUSE EST EN AMONT : LE CLAVIER EST ETEINT

Mesure sur le lanceur de reference, `host_revo/lancer_config_complete.cmd`
(173 lignes, c'est bien le bon) : il ne pose **aucun** de ces cinq
interrupteurs.

| interrupteur | pose par le lanceur ? | defaut dans le code | consequence |
|---|---|---|---|
| `VF5_CLAVIER` | **non** | **eteint** | aucune touche n'arrive dans le bloc |
| `VF5_MANETTE` | **non** | 0 | aucune manette declaree |
| `VF5_TITRE_AET` | non | **1** | la reparation du titre est ACTIVE quand meme |
| `VF5_SONDE_BANDEAU` | non | eteint | la sonde du bandeau ne tourne pas |
| `VF5_EVTS` | non | **ARME** | l'evenement DLC `0x3A` est poste a l'image 600 |

**Il y a donc DEUX causes independantes a << la touche entree n'a aucun
effet >>, et la premiere suffit a elle seule :**

1. **en amont, la configuration** : le clavier est eteint, donc **aucun** bit
   ne part vers le bloc. Rien de ce que le module accepte ou refuse n'entre en
   jeu.
2. **en aval, le masque** : meme clavier allume, le module n'accepte que le
   bit 3 et ENTREE pose le bit 8 (section 14.3).

C'est la lecon de [[lire-l-en-tete-du-journal-de-l-hote]], repayee : l'en-tete
du journal imprime `clavier (SS 338.14) : eteint` a **chaque** course.

**Pour la prochaine course il faut donc, en plus des temoins du titre :**
`VF5_CLAVIER=1` pour qu'une touche existe, `VF5_EVTS=0` parce que l'evenement
DLC est arme par defaut et polluerait la mesure
([[un-interrupteur-de-mesure-laisse-arme]]), et tenir la touche **pendant
CS_DEMO** puisque la sonde qui imprime `boutons [0x795960]` y est bornee.

---

## 15. LA COURSE EST PAYEE, ET LA CAUSE DU REFUS D'ENTREE EST CHEZ NOUS
## (SS 419.17, course de 2000 images)

**Course : `VF5_IMAGES=2000 VF5_JOURNAL=1 VF5_EVTS=0 VF5_CLAVIER=1
VF5_SONDE_BANDEAU=310`. Sortie 0, 2000 images montrees, 0 echec de Present,
81978 tirages.**

### 15.1 Le geste du SS 419.13 est PAYE, sur les trois temoins

| temoin | attendu | MESURE |
|---|---|---|
| entrees dans CS_TITLE | une seule | **une** : derniere transition image 307, puis `5=CS_TITLE phase=1` dans **34 releves sur 35** jusqu'a l'image 2000 |
| tirages par image | ~40,3 (version large) contre 2,00 (sans reparation) | **40,7 a 60,2** sur les cinq dernieres fenetres de 50 images |
| le repartiteur en PHASE 1 | nul, ce que la version etroite ne faisait jamais | **`418 : image 316 : repartiteur NUL pour CS_TITLE PHASE 1 etape 3`** |

Les trois lignes `418` sont : image 307 (phase 0 etape 2), 315 (phase 0 etape
3) et **316 (phase 1 etape 3)**. La troisieme n'existe que grace a la cle de
dedoublonnage (phase, etape) posee au meme SS : `mo+0x34` reste a 3, donc une
cle sur l'etape seule ne l'aurait jamais imprimee.

### 15.2 ET LE BANDEAU EST A L'ECRAN

**Valide a l'oeil : << PRESS START BUTTON >> s'affiche.** C'est la consequence
annoncee par la lecture de la section 10 : `FUN_1800D9ED0` ne dessine que si
`bloc+0x1FF08` est nul, et ses appelants sont une mise a jour PAR IMAGE. Borner
a la phase 0 le faisait disparaitre des la phase 1 ; l'elargissement le rend.

### 15.3 ENTREE NE FAIT RIEN -- CONFIRME, et des DEUX cotes

| bout de la chaine | mesure |
|---|---|
| l'appui arrive-t-il ? | **oui** : `338.14 : image 718 : bloc+0x20 = 0x00000100 [START ]`, et six fois en tout |
| le titre bouge-t-il ? | **non** : derniere transition a l'image 307, `CS_TITLE phase=1` jusqu'au bout |

La cause est le masque de `FUN_1801B2390` : `uVar4 = 0x1ff`, rabattu a **`8`**
quand `DAT_180C8DE1A` est non nul. `CLV_START` est le bit 8 = `0x100`, et
`0x100 & 0x8 = 0`.

**`W` n'a PAS ete essaye** : les seuls masques vus sont `0x100` (six fois),
`0x2` (une fois) et `0x0`. Jamais `0x8`.

### 15.4 LA CAUSE EST DANS NOTRE PROPRE BLOC D'INIT

Desassemblage de `module_start` a **VF5FS+0x274762**, le seul ecrivain des
quatre drapeaux :

```asm
MOV   RCX, qword ptr [R13 + 0x38]      ; le qword +0x38 de NOTRE bloc
MOV   qword ptr [0x18064b218], RCX
SHR   RAX, 0x28                        ; octet 5
TEST  AL, AL   ; SETNZ [0x180c8de18]
CMP   AL, 0x2  ; SETZ  [0x180c8de19]
SHR   RCX, 0x38                        ; octet 7
TEST  CL, 0xf  ; SETNZ [0x180c8de1a]   ; <-- LE MASQUE
TEST  CL, 0xf0 ; SETNZ [0x180c8de1b]
```

Le qword `+0x38` vaut `(flags3C << 32) | flags38`, donc son **octet 7 est
l'octet 3 de `flags3C`**. Et nous posons `blk.flags3C = 0x01000100`, dont
l'octet 3 vaut **`0x01`**. Donc `0x01 & 0x0F != 0` -> **`C8DE1A = 1`**, ce qui
concorde exactement avec la sonde : `drapeaux console[+0xC8DE18..1B]=00 00 01
00`.

**Autrement dit : c'est NOUS qui rabattons le masque du titre de `0x1FF` a
`0x8`.** Le defaut du module accepte les bits 0 a 8, START compris.

### 15.5 ET MON PROPRE COMMENTAIRE S'ARRETAIT DEUX INSTRUCTIONS TROP TOT

Le bloc du SS 310 dans l'hote transcrit ce desassemblage... et **s'arrete a
`SETZ [0x180C8DE19]`**. Les deux `SETNZ` suivants etaient dans les cinq memes
instructions. De plus, le commentaire de `flags3C` dit << octet 0 inconnu,
octet 1 a 0 >> et **ne dit rien de l'octet 3**, qui est celui qui compte.

### 15.6 CE QU'IL FAUT LIRE AVANT DE TOUCHER A CET OCTET

`DAT_180C8DE1A` a **quatre** lecteurs. Un seul est elucide :

| lecteur | role |
|---|---|
| `FUN_1801B2390` | **le masque du titre** (elucide) |
| `FUN_1800B6E70` | INCONNU |
| `FUN_18019DBF0` | INCONNU |
| `FUN_18017BBB0` | INCONNU |

**Aucun geste n'est pose.** Mettre cet octet a 0 ferait accepter START, mais
changerait aussi ce que font ces trois fonctions, et le chantier exige de
nommer la reparation avant de la poser. Il faut aussi etablir d'ou vient la
valeur `0x01000100` : si elle est transcrite de l'hote de SEGA, la changer
nous ecarte de l'oracle, et il faut d'abord relever ce que VFREVO.exe met dans
ce champ.

---

## 16. LES QUATRE LECTEURS DU DRAPEAU SONT LUS : UN SEUL BASCULEMENT
## (SS 419.18)

**Lecture seule. Aucun geste. RIEN N'A TOURNE depuis la course du SS 419.17.**

La section 15.6 laissait trois lecteurs INCONNUS et refusait d'y toucher. Ils
sont lus, et ils disent tous la meme chose.

### 16.1 La cle : `FUN_18019DB70` teste un NUMERO, pas un masque

```c
undefined8 FUN_18019db70(longlong param_1, int param_2)
{
  if ((ulonglong)(longlong)param_2 < 99) {
    uVar1 = *(ulonglong *)(param_1 + ((ulonglong)(longlong)param_2 >> 6) * 8);
    return (uVar1 >> ((byte)param_2 & 0x3f) & 1) != 0;   // le BIT n param_2
  }
  FUN_180093e60();            // hors bornes : ne revient pas
}
```

C'est un `tester_bit(ensemble_de_99_bits, numero)`. Donc les valeurs `2` et
`0x10` que deux lecteurs lui passent sont des **numeros de bouton virtuel**,
pas des masques : **bouton 2** et **bouton 16**.

Et dans l'agregateur, les valeurs sont des masques sur le meme espace :
`4 = 1<<2` et `0x10000 = 1<<16`. **Les deux memes boutons.**

### 16.2 La table complete

| lecteur | drapeau = 0 | drapeau = 1 | espace |
|---|---|---|---|
| `FUN_1801B2390` (le titre) | masque **`0x1FF`** = bits 0 a 8, **START (bit 8) COMPRIS** | bit **3** seul | boutons PHYSIQUES (`DAT_180795960`) |
| `FUN_1800B6E70` | bouton virtuel **2** | bouton virtuel **16** | virtuel, via `FUN_18019DB70` |
| `FUN_18017BBB0` | bouton virtuel **2** | bouton virtuel **16** | virtuel, via `FUN_18019DB70` |
| `FUN_18019DBF0` (agregateur) | `1<<2`, alias sur le bouton **34** | `1<<16`, alias sur le bouton **34** | virtuel |

Les deux lecteurs `2`/`0x10` ont la MEME forme en assembleur -- verifie a
`0x18017BDF9` :

```asm
MOV    EDX, 0x2
MOV    ECX, 0x10
CMP    byte ptr [0x180c8de1a], R15B     ; R15B = 0
CMOVNZ EDX, ECX                         ; non nul -> 0x10
CALL   0x18019db70
```

### 16.3 CE QUE CA ETABLIT, et ce que ca n'etablit pas

**ETABLI : `DAT_180C8DE1A` est un SELECTEUR DE DISPOSITION DE BOUTONS**, et
rien d'autre. Les quatre lecteurs choisissent un bouton, de facon coherente :
le bouton de validation est le **2** quand il est nul, le **16** quand il est
pose ; et le titre accepte tout le groupe `0x1FF` quand il est nul, le seul
bit 3 quand il est pose.

**Donc le mettre a 0 n'a PAS quatre effets de bord : il a UN effet**, un
basculement vers la disposition ou :

- le titre accepte les bits 0 a 8, donc **notre `CLV_START` (bit 8) marche** ;
- la validation est le bouton virtuel 2 au lieu du 16, partout a la fois.

**PAS ETABLI :** quel bouton virtuel notre bit physique 8 devient. La
traduction physique -> 99 bits virtuels passe par `FUN_1801B2300`, non lue.
Pour le TITRE la question ne se pose pas -- son masque porte sur les boutons
PHYSIQUES, et `0x1FF` contient le bit 8 -- mais pour les trois autres
lecteurs, si.

### 16.4 LA REPARATION, NOMMEE -- et le seul point qui reste

**Cause** : `blk.flags3C = 0x01000100` dans notre bloc d'init. Son octet 3
vaut `0x01`, et `module_start` en derive `C8DE1A = (octet & 0x0F) != 0`
(section 15.4). Notre source documente les octets 0 et 1 de ce champ et **ne
dit rien de l'octet 3**.

**Geste** : `flags3C = 0x00000100`, c'est-a-dire l'octet 3 remis a zero.
`C8DE1B` ne bouge pas (`0x01 & 0xF0` valait deja 0).

**REPONDU AU SS 419.21 (section 19), ET DANS L'AUTRE SENS : ne PAS le
changer est l'ecart.** L'oracle fait `[+0x3F] &= 0xF0`, donc il EFFACE ce
quartet et `C8DE1A` y vaut 0 ; aucun hote reel ne pose 1. Notre
transcription a oublie cet ajustement. Ancien doute, garde pour memoire :
si cette valeur etait transcrite de l'hote de SEGA, la changer nous ecarterait de
l'oracle, et il faut d'abord relever ce que `VFREVO.exe` met dans ce champ de
son propre bloc d'init. `VFREVO.exe` est analyse dans le projet Ghidra
**`revo_pc.gpr`**, qui n'est pas celui ouvert ([[ghidra-ouvrir-le-projet-revo-pc]]).

### 16.5 ET UN ESSAI GRATUIT QUI VALIDERAIT TOUTE LA LECTURE

Le bit 3 physique est, chez nous, **`W`** (`CLV_Y`, `garde = tenu('W')`).
Avec le drapeau tel qu'il est, c'est le SEUL bouton que le titre accepte.
**Presser `W` sur l'ecran-titre ne coute rien et teste la chaine entiere** :
s'il fait sortir le titre, alors le masque, la copie `bloc+0x20` ->
`+0x795960`, le front montant et la numerotation partagee sont tous confirmes
d'un coup, et il ne reste qu'un choix de bouton a corriger. S'il ne fait rien,
une de ces quatre lectures est fausse.

La course du SS 419.17 a vu `0x100` six fois et `0x2` une fois -- **jamais
`0x8`**.

---

## 17. `W` FAIT SORTIR LE TITRE : LES QUATRE LECTURES SONT CONFIRMEES
## (SS 419.19, course de 2000 images arretee a la main vers 1421)

**Course : `VF5_IMAGES=2000 VF5_JOURNAL=1 VF5_EVTS=0 VF5_CLAVIER=1`.
L'utilisateur a presse `W` seulement, puis a ferme la fenetre -- d'ou le code
`0xC0000005`, qui n'est donc PAS une faute.**

### 17.1 LA CORRELATION EST EXACTE, DIX FOIS SUR DIX

| `W` arrive (`bloc+0x20 = 0x00000008 [G ]`) | le titre sort |
|---|---|
| image 448 | **449** : CS_TITLE -> CS_SIGNIN |
| image 608 | **609** |
| image 651 | **652** |
| image 682 | **683** |
| ... | ... |

Dix appuis, dix sorties, **toujours exactement une image apres**. Et le masque
`0x00000008 [G ]` est vu 17 fois, `0x00000000` 18 fois : aucun autre bouton.

### 17.2 CE QUE CA CONFIRME, ET C'EST TOUT D'UN COUP

| lecture | section | etat |
|---|---|---|
| le masque accepte vaut `0x8`, donc le bit 3 seul | 14.2 | **CONFIRME** |
| la copie `bloc+0x20` -> `+0x795960` ne renumerote PAS | 14.4 / 16 | **CONFIRME** : notre bit 3 physique atteint le predicat |
| `+0x10` est le FRONT montant, pas l'etat tenu | 14.4 | **CONFIRME** : l'appui agit a l'image suivante, une seule fois par appui |
| `DAT_180C8DE1A = 1` est bien ce qui restreint | 15.4 / 16.2 | **CONFIRME** : le bouton accepte est bien celui que le drapeau designe |

Et par la meme mesure, **le refus d'ENTREE est entierement explique** : son bit
8 (`0x100`) n'est pas dans `0x8`. Rien d'autre n'est en cause -- ni le clavier,
ni le pont, ni le front, ni la numerotation.

### 17.3 LA REPARATION NOMMEE EN 16.4 TIENT TOUJOURS

`flags3C = 0x01000100` -> `0x00000100` ferait accepter les bits 0 a 8, donc
ENTREE. Le seul point qui reste avant de la poser est inchange : **d'ou vient
`0x01000100`**, et ce que `VFREVO.exe` met dans ce champ
([[ghidra-ouvrir-le-projet-revo-pc]], projet `revo_pc.gpr`).

L'essai de `W` ne remplace pas cette verification -- il etablit que la chaine
est saine et que seul le CHOIX du bouton est en jeu.

### 17.4 UNE QUESTION NEUVE : LE TITRE REVIENT A LUI-MEME

La sortie marche, mais elle ne mene nulle part. Le motif est stable, dix fois :

```
CS_TITLE --(appui)--> CS_SIGNIN (2 images) --> WARNING (1 image) --> CS_TITLE
   449                    451                      452
```

Les releves de sous-etat montrent `6=CS_SIGNIN phase=2` (10 fois),
`2=WARNING phase=1` et `phase=2` (10 fois chacune), et surtout
**`5=CS_TITLE phase=2` (10 fois)** -- la phase 2 du titre tourne, alors qu'elle
ne tournait jamais avant.

**Ce n'est PAS la boucle du SS 419.7** : celle-la tournait **sans aucun appui**
et 64 fois en 900 images. Ici il y a dix cycles pour dix appuis, et la course
payee du SS 419.17 en a fait **zero** sur 2000 images sans bouton valide. Le
correctif de la commande 242 tient.

**Piste a lire**, et elle est deja a demi-ecrite : `CS_TITLE` phase 2
(`FUN_1800E5A20`) fait `if (de18 && !de19 && !DAT_1807514D9)` puis
`FUN_1801AAC20`, qui demande le mode GAME (section 15 de l'ancien journal, et
[[le-point-d-entree-du-combat-est-1aac20]]). Or **`VF5_CONSOLE` met
`DAT_180C8DE18` a 0**, donc ce test echoue et la phase 2 ne demande rien : on
retombe au titre. C'est la meme famille de cause que celle du masque -- un
drapeau de NOTRE bloc d'init.

---

## 18. LA PHASE 2 DU TITRE, ET D'OU VIENT LE RETOUR AU TITRE (SS 419.20)

**Lecture seule, sur le journal de la course du SS 419.19. RIEN N'A TOURNE.**

### 18.1 `FUN_1800E5A20` : la phase 2 est un DEMONTAGE

Elle etait **deja sur le disque** (`VF5RE/code_decompile/FUN_1800e5a20.c`).

```c
if (bloc+0x1ff08 == 0) {                       // 4e site du MOTIF
    FUN_180026150(0x12e); FUN_180025920(0x12e); FUN_180195da0(0x15f);
} else {
    cmd 0x11 (17) ; FUN_1800f0a50(...) ; cmd 0x13 (19);
}
FUN_1800da490(&DAT_18074fe70, 0);              // ETEINT la tache INFORMATION
if ((DAT_180c8de18 != 0) && (DAT_180c8de19 == 0) && (DAT_1807514d9 == 0)) {
    FUN_1801aa1d0(local_res8, ...DAT_18064b218...);
    FUN_1801aac20(0, local_res8, DAT_18064b218._4_4_ & 0xff, 0);   // le COMBAT
}
return 1;                                      // INCONDITIONNEL
```

Trois choses :

1. **Son `return 1` est inconditionnel** : la phase 2 reussit toujours. Ce
   n'est pas elle qui bloque quoi que ce soit.
2. Elle **detruit** les ressources du titre (`0x12E`, `0x15F`) et **eteint la
   tache `INFORMATION`** -- donc le bandeau. C'est le quatrieme site du motif
   `bloc+0x1FF08 == 0`, apres CS_TITLE phase 0, MENU_MAIN et le bandeau.
3. Les **parametres du combat viennent de `DAT_18064B218`**, qui est le qword
   que `module_start` y recopie depuis **notre bloc d'init** (section 15.4 :
   `MOV qword ptr [0x18064b218], RCX`). `DAT_18064B218._4_4_ & 0xff` est donc
   **l'octet 0 de notre `flags3C`** -- celui que notre source appelle
   << inconnu >>. Ce champ n'est pas decoratif : il alimente l'entree du
   combat.

### 18.2 CORRECTION : `de18 == 0` N'EST PAS UNE FAUTE, C'EST NOTRE CHOIX

J'ai ecrit a la fin du SS 419.19 que la garde `de18 != 0` devant
`FUN_1801AAC20` etait << la meme famille de cause >> que le masque. **C'est
faux, et ma propre fiche le disait** : `VF5_CONSOLE` existe PRECISEMENT pour
mettre `DAT_180C8DE18` a 0 et empecher CS_TITLE de demander le mode GAME, afin
de prendre la chaine CONSOLE au lieu du combat
([[la-chaine-console-tient-a-un-octet]],
[[le-point-d-entree-du-combat-est-1aac20]]). La phase 2 ne demande donc rien,
**et c'est voulu**.

### 18.3 LES DEUX DEMANDEURS, NOMMES

Desassemblage de `FUN_1800E59C0` et `FUN_1800E59F0` :

| fonction | ce qu'elle demande |
|---|---|
| **`FUN_1800E1B00(n)`** | le **MODE** n |
| **`FUN_1800E1B20(n)`** | le **SOUS-ETAT** n |

`FUN_1800E59C0` fait `FUN_1800E1B00(5)` (mode MENU) puis `FUN_1800E1B20(0x49)`
(sous-etat **73**). `FUN_1800E59F0` fait `FUN_1800E1B20(5)` -- CS_TITLE.

**Et une hypothese refutee dans le tour meme** : j'ai cru que `FUN_1800E59F0`
etait notre coupable, parce qu'il redemande CS_TITLE et fait les memes appels
que la phase 2 du titre. Les xrefs disent qu'il est a `0x1803C8908`, soit
l'entree d'indice 8 de la table au deplacement `+0x18`, et cette entree porte
le numero **`08` = CS_DEMO** (phases `0xE5D70` / `0xE5510` / `0xE59F0`). C'est
donc la **phase 2 de CS_DEMO** : l'attract qui rend la main au titre. Parfaitement
legitime, et hors de notre cycle.

### 18.4 OU LE CYCLE SE FERME -- REFUTEE AU SS 419.24 (section 21.5)

**AVERTISSEMENT : la conclusion de cette section est FAUSSE.** La phase
de sortie de la tache est `FUN_1800E5900`, et elle ne demande AUCUNE
scene : elle delegue la commande 21 puis `return 1`, et le chemin
qu'elle remplace (`FUN_1801DEC30`) est du pur demontage. Les releves
ci-dessous restent justes ; c'est l'ELIMINATION qui etait fausse.

| releve | sous-etat demande |
|---|---|
| `2=WARNING phase=1` | **`3=CROSSPLAY_WARNING`** -- la bonne suite |
| `2=WARNING phase=2` | **`5=CS_TITLE`** -- ecrase |

Et le compte des demandes sur toute la course : `3=CROSSPLAY_WARNING` est
demande **10 fois** -- une par cycle -- et le sous-etat 3 n'est **jamais**
atteint.

Les trois phases de WARNING, lues (table entree `02`, phases `0xE6660` /
`0xE58C0` / `0xE5C00`) :

| phase | code | ce qu'elle fait |
|---|---|---|
| 0 | `FUN_1800E6660` | `if (FUN_18000BA20(...) == 0 && DAT_180C8DE18 == 0) FUN_1802CD400(DAT_180751498, "WARNING")` -- **cree la tache** |
| 1 | `FUN_1800E58C0` | `return FUN_1802CCA00(DAT_180751498) == 0` -- **attend qu'elle meure** |
| 2 | `FUN_1800E5C00` | `FUN_1802CCB60(DAT_180751498)` -- **la detruit** |

**La tache est bien creee** : `[WARNING]` parait 10 fois dans la liste des
taches vivantes de l'hote, une par cycle. Et la condition de la phase 0 est
`de18 == 0`, donc notre `VF5_CONSOLE` ne l'empeche PAS.

**Donc le seul code qui tourne entre les deux releves est la destruction de la
tache.** `FUN_1802CCB60` fait courir la phase de SORTIE de la tache (phase 3,
`vtable+0x18`, cf. `FUN_1802CD130`). **C'est la sortie de la tache
`[WARNING]` qui demande CS_TITLE**, en ecrasant le `CROSSPLAY_WARNING` pose
par la phase 1.

### 18.5 CE QUI ETAIT A LIRE -- FAIT, ET IL N'Y A PAS DE FABRIQUE

**Le nom est une ETIQUETTE recopiee a `+0x2e`, pas un selecteur de
classe : il n'y a aucune fabrique a chercher** (section 21.1). La classe
est `TaskCsWarning`, lue au desassemblage de son constructeur.

La **classe** de la tache `[WARNING]` et sa **phase de sortie**.
`FUN_1802CD400(emplacement, "WARNING")` cree par NOM, donc il y a une fabrique
qui associe ce nom a une classe ; les 399 noms RTTI sont dans
`VF5RE/CLASSES_RTTI_REVO.txt` ([[le-rtti-donne-399-noms-de-classes]]), et le
journal en nomme deja une voisine, `TaskCsOfflineWarning`.

**Degre : la conclusion de 18.4 est ETAYEE, pas CONFIRMEE.** Elle repose sur
une elimination (rien d'autre ne tourne entre les deux releves) et non sur la
lecture de l'ecrivain. Il reste aussi l'hypothese du decalage d'une image du
prologue ([[relire-juste-apres-le-geste]]) : les deux releves pourraient ne pas
encadrer ce que je crois.

---

## 19. L'ORACLE TRANCHE -- ET DANS L'AUTRE SENS (SS 419.21)

**Lecture, dans ma propre documentation. Aucun geste. RIEN N'A TOURNE.**

La section 16.4 refusait de toucher a l'octet 3 de `flags3C` tant qu'on ne
saurait pas d'ou vient `0x01000100`, << car si c'est transcrit de l'hote de
SEGA, le changer nous ecarte de l'oracle >>. **La reponse est l'inverse : ne
PAS le changer est l'ecart.**

### 19.1 Ce que l'oracle fait vraiment, deja releve

`FS GOG/analysis/HOTE_REVO.md`, le bloc d'init de `VFREVO.exe` :

| offset | contenu |
|---|---|
| +0x38 | dword **`0x2D0300DC`**, puis octet `[+0x3A] = 2` |
| +0x3C | dword `0x01000102`, puis `[+0x3C] = [rsi+0xF3]`, `[+0x3D] = 0`, **`[+0x3F] &= 0xF0`** |

**Trois ajustements** apres la constante, pas deux :

1. `[+0x3C] = [rsi+0xF3]` -- l'octet 0 vient de l'**etat d'execution**. C'est
   ce que notre commentaire << octet 0 inconnu (vient de l'hote) >> voulait
   dire, sans le savoir precisement.
2. `[+0x3D] = 0` -- l'octet 1 mis a zero. **C'est exactement ce que fait notre
   `VF5_CONSOLE`.** Il est donc FIDELE a l'oracle, et non une deviation : il
   ne devrait sans doute pas etre un interrupteur du tout.
3. **`[+0x3F] &= 0xF0`** -- le **quartet bas de l'octet 3 est EFFACE**.

### 19.2 Et le troisieme est celui qui portait la question

`module_start` calcule `C8DE1A = (octet 7 du qword) & 0x0F != 0` (section
15.4), et l'octet 7 est l'octet 3 de `flags3C`. L'oracle force ce quartet a
zero, **donc `DAT_180C8DE1A = 0` chez SEGA**, et le masque du titre vaut
`0x1FF` -- les bits 0 a 8, **START compris**.

**Et c'est vrai des DEUX hotes reels**, ce qui enleve le dernier doute :

| hote | `flags3C` | octet 3 | `& 0x0F` | `C8DE1A` | `& 0xF0` | `C8DE1B` |
|---|---|---|---|---|---|---|
| `vfes.exe` (arcade, 2021) | `0x10000102` | `0x10` | 0 | **0** | `0x10` | 1 |
| `VFREVO.exe` (Steam, 2025) | `0x01000102` puis `&= 0xF0` | **`0x00`** | 0 | **0** | 0 | 0 |
| **notre hote** | `0x01000100`, **sans le ET** | **`0x01`** | **1** | **1** | 0 | 0 |

**Aucun hote reel ne pose `C8DE1A = 1`.** La restriction du titre au seul bit 3
n'existe donc dans aucune configuration de SEGA : **c'est notre bogue, et rien
d'autre.**

### 19.3 LA CAUSE, NOMMEE : UN AJUSTEMENT OUBLIE A LA TRANSCRIPTION

Et elle est ecrite dans notre propre source. La declaration du champ dit :

```c
uint32_t    flags3C;        // +0x3C  0x01000102, octets 0 et 1 ajustes
```

**<< octets 0 et 1 ajustes >> : deux sur trois.** Le `[+0x3F] &= 0xF0` n'a
jamais ete recopie. Et la valeur posee, `0x01000100`, differe de la constante
de l'oracle `0x01000102` a l'octet 0 -- une seconde divergence, separee.

### 19.4 LE GESTE -- POSE ET COMPILE (SS 419.22)

```c
blk.flags3C &= 0xF0FFFFFFu;   // l'oracle : [+0x3F] &= 0xF0
```

Pour notre valeur, l'octet 3 passe de `0x01` a `0x00`, donc `flags3C` devient
`0x00000100`. Consequences, toutes lues :

- `C8DE1A = 0` -> le titre accepte les bits 0 a 8, **donc ENTREE** ;
- la validation redevient le bouton virtuel **2** au lieu du 16, dans les trois
  autres lecteurs, de facon coherente (section 16.2) ;
- `C8DE1B` ne bouge pas : il valait deja 0 (`0x01 & 0xF0 == 0`).

**Ce n'est pas un interrupteur et ce n'est pas un choix : c'est une ligne
manquante de notre transcription de l'oracle.**

### 19.5 LA SECONDE DIVERGENCE, A NE PAS CONFONDRE

L'octet 0 : l'oracle le prend de `[rsi+0xF3]` **a l'execution** ; nous posons
`0x00`, alors que la constante de l'oracle porte `0x02`. Et cet octet est
**passe a l'entree du combat** : `FUN_1801AAC20(0, ..., DAT_18064B218._4_4_ &
0xff, 0)` (section 18.1). C'est donc un parametre vivant, pas un drapeau --
une question ouverte, distincte, et qui demande de lire ce que `[rsi+0xF3]`
contient dans l'oracle.

### 19.6 LE GESTE EST POSE (SS 419.22) -- RIEN N'A ENCORE TOURNE

Ecrit dans `vf5fs_host.cpp`, juste apres l'affectation et **avant** le bloc
`VF5_CONSOLE`, de facon inconditionnelle -- ce n'est pas un interrupteur :

```c
{
    const uint32_t av3F = blk.flags3C;
    blk.flags3C &= 0xF0FFFFFFu;      // l'oracle : [+0x3F] &= 0xF0
    const unsigned de1A = (((blk.flags3C >> 24) & 0x0Fu) != 0) ? 1u : 0u;
    Log("  419.22 : [+0x3F] &= 0xF0 -- ajustement de l'oracle, omis"
        " jusqu'ici : flags3C 0x%08X -> 0x%08X, donc DAT_180C8DE1A = %u"
        " et le masque accepte par le titre vaut 0x%X",
        av3F, blk.flags3C, de1A, de1A ? 0x8u : 0x1FFu);
}
```

Et le journal du 310 citait `0x01000100` **en dur** : le litteral perime est
ote, il imprime desormais la valeur.

**AUTO-TEST, et il a ETE PROUVE CAPABLE D'ECHOUER.**
`scratchpad/verifier_41922.py` controle cinq choses : le ET present
exactement une fois, le litteral perime absent, l'affectation intacte, le
geste `VF5_CONSOLE` intact, et **l'ORDRE** des trois (affectation -> ET ->
`VF5_CONSOLE`). Lance d'abord sur une copie **non patchee**, il a rendu
`ECHEC -- le ET de l'oracle n'est pas present EXACTEMENT une fois (0) ; le
journal 310 cite encore 0x01000100 en dur ; ordre faux` ; sur le fichier
patche, `OK (5 controles)`. Il verifie aussi l'arithmetique sur les deux
valeurs reelles : `0x01000100 -> 0x00000100` et `0x10000102 -> 0x10000102`
(l'arcade ne bouge pas).

`build.cmd` : **OK**, l'executable est copie dans `FS REVO`.

### 19.7 CE QUE LA PROCHAINE COURSE DOIT MONTRER

**-> TOUT RENDU, section 20. Les quatre temoins sont passes.**

| temoin | attendu |
|---|---|
| ligne `419.22` dans le journal | `flags3C 0x01000100 -> 0x00000100`, `DAT_180C8DE1A = 0`, masque `0x1FF` |
| ENTREE sur l'ecran-titre | **sort du titre**, une image apres l'appui |
| `W` sur l'ecran-titre | **sort toujours** (le bit 3 est dans `0x1FF`) |
| les tirages par image | inchanges (40,7 a 60,2) : ce geste ne touche pas le rendu |

**Et ce qui n'est PAS predit** : les trois autres lecteurs passent du bouton
virtuel 16 au 2. Pour le titre la question ne se pose pas -- son masque porte
sur les boutons PHYSIQUES -- mais le menu peut reagir autrement, et
`FUN_1801B2300` (physique -> 99 bits virtuels) n'est pas lue. Si `W` cessait
de sortir du titre, une des lectures du SS 419.18 serait fausse.

Course a lancer : `VF5_IMAGES=2000 VF5_JOURNAL=1 VF5_EVTS=0 VF5_CLAVIER=1`,
par `FS REVO/host_revo/lancer_config_complete.cmd` (173 lignes).

---

## 20. ENTREE SORT DU TITRE -- LE GESTE DE L'ORACLE EST PAYE (SS 419.23)

**Deux courses, `VF5_IMAGES=2000 VF5_JOURNAL=1 VF5_EVTS=0 VF5_CLAVIER=1`.
La premiere n'a recu que `W` (l'utilisateur n'avait pas presse ENTREE) ; la
seconde a recu les deux. Les deux finissent en `0xC0000005` apres le dernier
appui -- la fenetre fermee a la main, pas une faute.**

### 20.1 LE TEMOIN, MOT POUR MOT CE QUI ETAIT PREDIT

```
419.22 : [+0x3F] &= 0xF0 -- ajustement de l'oracle, omis jusqu'ici :
flags3C 0x01000100 -> 0x00000100, donc DAT_180C8DE1A = 0
et le masque accepte par le titre vaut 0x1FF
```

### 20.2 ENTREE : TROIS SORTIES, TOUJOURS A L'IMAGE SUIVANTE

| `0x00000100 [START]` arrive | CS_TITLE **phase 2** (la sortie) |
|---|---|
| image **361** | **362** |
| image **569** | **570** |
| image **628** (lu a `PHASE 1 etape 3`) | **629** |

Le cas de 628 est le plus propre : a l'image 628 le titre est **a la phase 1**,
celle qui fait courir `FUN_1801B2390`, l'appui arrive, et la phase 2 tourne a
629. C'est exactement le mecanisme lu.

### 20.3 ET LES CINQ APPUIS QUI N'ONT RIEN FAIT SONT TOUS EXPLIQUES

Aucun appui n'est laisse sans compte -- c'etait la faiblesse a eviter :

| appui START | ou etait la chaine |
|---|---|
| 587 | **WARNING phase 2** -- pas au titre |
| 595 | CS_TITLE **etape 2 -> 3** ; la phase 1 ne tourne qu'a 596 |
| 618 | **WARNING phase 2** |
| 623 | aucune ligne de CS_TITLE a 622-624 -- hors du titre |
| 631 | 630 CS_SIGNIN phase 2, 632 WARNING phase 2 -- en plein cycle |

**Regle unique, sans exception sur 16 appuis** : un appui pris pendant que la
phase 1 de CS_TITLE est l'etape courante sort du titre a l'image suivante ;
tout appui hors de cette fenetre ne fait rien. C'est le comportement normal,
pas un defaut.

### 20.4 LE CONTROLE EST PASSE : `W` N'EST PAS CASSE

C'etait le risque nomme avant la course -- si `W` cessait de sortir, une des
quatre lectures du SS 419.18 serait fausse.

| course | appuis `W` | sorties par `W` |
|---|---|---|
| premiere (sans ENTREE) | 3 (images 479, 716, 748) | **3** (480, 717, 749) |
| seconde | 8 | **4** (481, 584, 600, 615) |

Les sorties de la seconde course se repartissent **4 par `W` + 3 par START = 7**,
et le journal compte exactement **7 CS_SIGNIN, 7 WARNING, 7 retours au titre**.
Le compte se ferme.

### 20.5 DEGRE : CONFIRME

Deux temoins independants : le journal dit que le masque vaut `0x1FF`, et le
comportement dit que le bit 8 passe. Et la cause otee est nommee et
verifiable -- un ajustement de l'oracle (`[+0x3F] &= 0xF0`) qui manquait a
notre transcription. **Ce n'est pas un interrupteur** : il est pose sans
condition.

Ce qui etait predit et s'est verifie : ENTREE sort, `W` sort toujours, le
rendu ne bouge pas. Ce qui etait annonce comme NON predit : les trois autres
lecteurs passent du bouton virtuel 16 au 2 -- **toujours non mesure**, parce
que la chaine n'atteint pas le menu.

### 20.6 LE MUR SUIVANT EST CELUI DU SS 419.20, ET IL N'A PAS BOUGE

La sortie marche maintenant par les deux boutons, mais elle ne mene toujours
nulle part : `CS_TITLE -> CS_SIGNIN -> WARNING -> CS_TITLE`, sept fois. La
phase 1 de WARNING demande `3=CROSSPLAY_WARNING`, sa phase 2 ecrase par
`5=CS_TITLE`, et le seul code entre les deux est la destruction de la tache
`[WARNING]` ([[le-cycle-du-titre-se-ferme-sur-la-tache-warning]]).

**A lire ensuite** : la CLASSE de la tache `[WARNING]` et sa phase de sortie.
`FUN_1802CD400(DAT_180751498, "WARNING")` cree par NOM ; les 399 noms RTTI
sont dans `VF5RE/CLASSES_RTTI_REVO.txt`, et le journal nomme une voisine,
`TaskCsOfflineWarning`.

---

## 21. LA TACHE WARNING, LUE -- ET LE SS 419.20 EST REFUTE (SS 419.24)

**Lecture seule, Ghidra `vf5fs_revo` port 8192. RIEN N'A TOURNE.**

### 21.1 IL N'Y A AUCUNE FABRIQUE PAR NOM

La section 18.5 annoncait : << `FUN_1802CD400(emplacement, "WARNING")` cree
par NOM, donc il y a une fabrique qui associe ce nom a une classe >>, et
envoyait chercher parmi 399 noms RTTI. **C'est faux.**

`FUN_1802CD400(p1, p2)` appelle `FUN_1802CD250(p1, *(DAT_180ea7608+0x10), p2, 2)`,
et dans `FUN_1802CD250` la chaine `param_3` est simplement **recopiee dans
l'objet a `+0x2e`**, sur 0x1f octets au plus, par `FUN_180363F50` :

```c
lVar1 = param_1 + 0x2e;
*(undefined8 *)(param_1 + 0x10) = param_2;   // le parent
*(undefined4 *)(param_1 + 8)    = param_4;   // le mode (2)
...
FUN_180363f50(lVar1, param_3, uVar10);       // le NOM, recopie
```

**Le nom est une ETIQUETTE de debogage, pas un selecteur de classe.**
`DAT_180751498` *est* l'objet-tache, et sa classe est fixee a la compilation.

### 21.2 LA CLASSE, PAR LE DESASSEMBLAGE DE SON CONSTRUCTEUR

`FUN_1800E4FC0`, le seul ecrivain de `0x180751498` :

```asm
1800e4fcb  MOV  ECX, 0x170                 ; l'objet fait 0x170 octets
1800e4fd0  CALL 0x1802ecd50                ; l'allocateur, alignement 0x10
1800e4fe5  CALL 0x1800e4d00                ; le constructeur de base
1800e4feb  LEA  RAX, [0x1803c99c8]
1800e4ff2  MOV  qword ptr [RBX], RAX       ; la VTABLE, a objet+0
1800e4ffc  CALL 0x1801de050                ; sous-objet a +0x16c
1800e5002  MOV  qword ptr [0x180751498], RBX
```

`0x1803C99C8` est **exactement** l'adresse que `CLASSES_RTTI_REVO.txt` donne
pour **`TaskCsWarning`**. Deux acquis :

1. la tache est un `TaskCsWarning` ;
2. **la colonne d'adresses du releve RTTI EST l'adresse de vtable** -- mesure
   par ce `LEA`, et non supposee. Le releve n'a pas d'en-tete, la question
   etait donc ouverte ([[un-nom-n-est-pas-du-code]]).

Et les voisines sont espacees de 0x48 : `TaskCsWarning` 0x3C99C8,
`TaskCsCrossplayWarning` 0x3C9A10, `TaskCsOfflineWarning` 0x3C9A58 -- soit
9 entrees par vtable.

### 21.3 LA VTABLE, ET LES PHASES DE LA TACHE

`FUN_1802CD130` est le pas d'une tache : la phase est a `+0x18` de l'objet, et

| phase | entree | adresse |
|---|---|---|
| 1 | vtable+0x08 | `0x1800E5C60` |
| 2 | vtable+0x10 | `0x1800E53F0` |
| **3 -- la SORTIE** | **vtable+0x18** | **`0x1800E5900`** |
| (autre) | vtable+0x20 | `0x1800E5C20` |

**A NE PAS CONFONDRE** avec les phases de la *scene* WARNING (entree `02` de
la table : `0xE6660` / `0xE58C0` / `0xE5C00`). Scene et tache sont deux
machines distinctes, chacune avec ses trois phases.

### 21.4 LA PHASE DE SORTIE EST LE CINQUIEME SITE DU MOTIF

```c
undefined8 FUN_1800e5900(longlong param_1)
{
  FUN_1801e1100(param_1 + 0x16c);
  if (*(longlong *)(DAT_180c8df28 + 0x1ff08) != 0) {
    if (*(code **)(DAT_180c8df28 + 0x1ff08) != (code *)0x0) {
      (**(code **)(DAT_180c8df28 + 0x1ff08))
          (*(undefined8 *)(DAT_180c8df28 + 0x1ff10), 0x15, 0);   // cmd 21
    }
    return 1;
  }
  uVar1 = FUN_1801dec30(param_1);
  return uVar1;
}
```

Cinq sites connus du motif `bloc+0x1FF08` : CS_TITLE phase 0 (`0xE5ED0`),
MENU_MAIN (`0x20F1E0`), le bandeau d'arcade (`0xD9ED0`), CS_TITLE phase 2
(`0xE5A20`), et **celui-ci**. Avec notre repartiteur pose, le module **delegue
la commande 21 et saute `FUN_1801DEC30`**.

### 21.5 ET LA CONCLUSION DU SS 419.20 EST REFUTEE

`FUN_1801DEC30` est **du pur demontage** : il libere six champs, coupe
`vfes_se_window_close` (en deleguant la commande 3 au passage), met des
compteurs a zero, et `return 1`. **Il ne demande AUCUNE scene.**

Donc **les deux chemins rendent 1 et aucun des deux ne demande `CS_TITLE`.**

La section 18.4 concluait : << c'est la sortie de la tache `[WARNING]` qui
demande CS_TITLE, en ecrasant le `CROSSPLAY_WARNING` pose par la phase 1 >>.
**C'etait une ELIMINATION** -- << le seul code qui tourne entre les deux
releves est la destruction de la tache >> -- **et l'elimination etait fausse.**
La section 18.5 avait pourtant nomme le risque exact : le decalage d'une image
du prologue, les deux releves pouvant ne pas encadrer ce que je croyais
([[relire-juste-apres-le-geste]], [[une-sonde-ne-commente-pas-une-valeur-non-lue]]).

### 21.6 DEUX CANDIDATS ELIMINES, ET LE CHEMIN MECANIQUE QUI RESTE

`FUN_1800E1B20` (demander un sous-etat) a **77 sites d'appel**. Je n'en lirai
pas 77 a la main. Deux sont deja ecartes :

| site | ce qu'il demande |
|---|---|
| `FUN_1800E1C20` | via `FUN_1800E2300`, qui ne rend que `0x13`, `0x14`, `0x15`, `0x16` -- **jamais 5** |
| `FUN_1800E59F0` | `(5)`, mais c'est **CS_DEMO phase 2** -- legitime (section 18.3) |

**LE BON OUTIL EST MECANIQUE, PAS UNE HYPOTHESE** : l'argument passe par ECX,
donc chaque site porte un `MOV ECX, imm` (`B9 xx 00 00 00`) juste avant le
`CALL`. Une passe de desassemblage sur les 77 sites donne la liste exacte de
ceux qui passent 5, avec un auto-test de bornes
([[un-balayage-d-octets-n-est-pas-un-decodage]]). C'est la prochaine lecture,
et elle remplace toute devinette.

### 21.7 CE QUE CA CHANGE POUR LA QUESTION DU SAUT

La question posee etait : peut-on sauter `CS_SIGNIN` (6), `WARNING` (2),
`CROSSPLAY_WARNING` (3), `OFFLINE_WARNING` (4), `CS_AUTOLOAD` (7) ?

Mecaniquement oui -- la table est cherchee par numero et demander un sous-etat
est une ecriture que l'hote peut poser
([[demander-une-scene-est-une-ecriture]]). Mais **ce tour deplace la
reponse** : la sortie de la tache WARNING nous **delegue** sa decision (commande
21), et le code que le module aurait execute ne demande rien. Donc le retour au
titre pourrait venir de NOTRE reponse, pas du code du module -- **une cause a
oter, pas un saut a forcer**. Il faut savoir qui ecrit 5 avant de choisir.

---

## 22. QUI DEMANDE CS_TITLE -- ET LA CAUSE EST UN BOUCHON DE SEGA (SS 419.25)

**Lecture seule : balayage du fichier + Ghidra. RIEN N'A TOURNE.**

### 22.1 LA METHODE, ET SON AUTO-TEST QUI A MORDU

`scratchpad/balayer_e1b20.py` : mapping VA -> offset par les **en-tetes PE lues
par pefile** (aucun offset recopie a la main,
[[jamais-d-offset-recopie-a-la-main]]), puis desassemblage **ancre a reculons**
avec capstone -- on garde le flux qui tombe exactement sur l'appel, au lieu de
deviner l'alignement ([[un-balayage-d-octets-n-est-pas-un-decodage]]).

Quatre controles, et le (a) est lance sur des adresses **deliberement
decalees** : il doit echouer, et il echoue 6 fois sur 6.

| controle | resultat |
|---|---|
| a) 6 adresses decalees | **6 rates sur 6** -- le controle mord |
| b) le compte des sites | 77 |
| c) aucun doublon | OK |
| d) les 77 vrais sites portent un `E8`/`E9` visant `0x1800E1B20` | **0 rate** |

**ET IL A ATTRAPE UNE ERREUR A MOI** : la premiere passe n'acceptait que `E8`,
et quatre sites ont echoue sur `0xE9` -- des **sauts terminaux** que Ghidra
etiquette quand meme `UNCONDITIONAL_CALL`. 73/77 validaient deja, ce qui
prouvait que le fichier, le mapping et ma transcription etaient bons : c'etait
mon hypothese qui etait trop etroite.

### 22.2 LA REPARTITION

| sous-etat demande | sites | | sous-etat | sites |
|---|---|---|---|---|
| **5** | **12** | | 60-62 | 3 / 2 / 4 |
| 8 | 1 | | 64-67 | 2 / 5 / 3 / 1 |
| 19, 21, 22 | 6 / 4 / 2 | | 69-73 | 1 / 4 / 3 / 1 / 2 |
| 23, 24 | 5 / 2 | | 41-43 | 4 / 6 / 1 |
| INDETERMINE | 3 | | | |

Les 12 qui demandent 5 : `0x1800BCEA1`, `0x1800E1B58`, **`0x1800E5716`**,
`0x1800E5A13`, `0x180208A56`, `0x180208C92`, `0x18020F922`, `0x180211983`,
`0x18021BA12`, `0x180215710`, `0x180215B94`, `0x180216174`.

**LIMITE DE LA METHODE, A NE PAS OUBLIER** : la valeur relevee est la
**derniere ecriture d'ECX avant l'appel**. Un site atteint par plusieurs
branches peut donc demander autre chose par un autre chemin -- et
`0x1800E5716` est precisement de ceux-la (22.4). Le balayage est un FILTRE qui
donne les candidats, pas la liste exhaustive des valeurs. Les 3 indetermines
(`mov ecx, eax`, `add ecx, 0x2a`, `mov ecx, edi`) restent a lire.

### 22.3 LA CHAINE CONSOLE EST ECRITE EN DONNEES

`FUN_1800E56E0` est pointe depuis `0x1803C8250` -- **une autre table que celle
des scenes** (`0x1803C87F0`). Sa forme, lue en memoire :

```
0x1803C8240 :  1800E6510  1800E56E0  1800E5B80     <- trois phases
0x1803C8260 :  00 01 08 05 06 02 03 04 07 49       <- la LISTE des sous-etats
0x1803C82A0 :  05 49 01 00                         <- entree suivante, en-tete
0x1803C82B0 :  180026620  180026620  180026620     <- ses trois phases
0x1803C82C8 :  09 0A 0B 0C 49                      <- sa LISTE
```

La liste de la premiere entree est **exactement la chaine console** :
`DATA_INITIALIZE(0)`, `SYSTEM_STARTUP(1)`, `CS_DEMO(8)`, `CS_TITLE(5)`,
`CS_SIGNIN(6)`, `WARNING(2)`, `CROSSPLAY_WARNING(3)`, `OFFLINE_WARNING(4)`,
`CS_AUTOLOAD(7)`, puis `73`. Les cinq sous-etats sur lesquels portait la
question forment donc un **segment contigu d'une liste en donnees**.

### 22.4 L'ECRIVAIN : `FUN_1800E56E0`, PHASE 1 DE CETTE ENTREE

**RETABLI AU SS 419.29 (section 26.3) : c'est bien l'ecrivain.** Le
rabattement du SS 419.26 reposait sur une lecture fausse du defaut de
`VF5_TITRE`.

**RABATTU AU SS 419.26 (section 23.3) : le titre disait << L'ECRIVAIN >>, ce qui etait TROP FORT.** C'est *un* site qui
demande 5 et qui siege dans la bonne table ; qu'il tourne ET declenche
dans notre course n'est PAS etabli. Si ses deux predicats sont faux, il
ne demande rien du tout.

Il choisit entre **5 = CS_TITLE** et **7 = CS_AUTOLOAD** :

```c
cVar1 = FUN_1801cf090();
cVar2 = FUN_1801cef40();
if (cVar1 == '\0') {
    if (cVar2 == '\0') goto SANS_DEMANDE;
    if (etat+0x1c != 2 && etat+0x1c != 7) goto SANS_DEMANDE;
    uVar3 = FUN_18000ba10();              // le port
    cVar1 = FUN_18000ba20(uVar3);
    if (cVar1 == '\0') goto LAB_1800e5711;   // -> 5 = CS_TITLE
    if (etat+0x1c != 2) goto SANS_DEMANDE;
    uVar6 = 7;                            // -> 7 = CS_AUTOLOAD
} else {
    if (etat+0x1c != 2 && etat+0x1c != 7) goto SANS_DEMANDE;
LAB_1800e5711:
    uVar6 = 5;                            // -> 5 = CS_TITLE
}
FUN_1800e1b20(uVar6);
```

### 22.5 LA CAUSE : `FUN_18000BA20` EST UN BOUCHON, DESASSEMBLE

```asm
18000ba20  32C0   XOR  AL, AL
18000ba22  C3     RET
```

**Deux octets. Zero inconditionnel, dans le binaire livre.** Verifie au
desassemblage et pas seulement a la decompilation, parce que c'est cette
fonction qui PORTE la conclusion ([[la-decompilation-ghidra-perd-des-parametres]]).
Son voisin `FUN_18000BA10` est deja connu pour etre `return 0` en dur.

**Trois consequences, toutes CONFIRMEES :**

1. dans `FUN_1800E56E0`, la branche `uVar6 = 7` est **DU CODE MORT** : le test
   `cVar1 == 0` reussit toujours, donc cette phase demande **toujours 5** ;
2. **`CS_AUTOLOAD` est inatteignable par ce chemin**, et le balayage ne trouve
   d'ailleurs **aucun** site qui demande 7 par un immediat ;
3. la phase 0 de la scene WARNING (`FUN_1800E6660`) teste le MEME predicat :
   `if (FUN_18000ba20() == 0 && de18 == 0) ... "WARNING"`. La premiere moitie
   etant toujours vraie, la tache est creee des que `de18 == 0` -- notre cas
   console. Ca colle a la mesure : 10 taches pour 10 cycles, puis 7 pour 7.

**~~Donc la boucle n'est PAS dans la reponse de notre hote.~~ NON ETABLI,
rabattu au SS 419.26 (23.3)** : la commande 212 -- NOTRE reponse -- ferme
une des deux routes de `FUN_1800E56E0`, donc l'hote participe a la
decision. Ce qui tient, c'est que la branche vers 7 est du code mort. Ce qui enterine la refutation du SS 419.24 : ni la
phase de sortie de la tache, ni notre reponse a la commande 21.

### 22.6 CE QUE CA FAIT A LA QUESTION DU SAUT

La question etait : peut-on sauter `CS_SIGNIN(6)`, `WARNING(2)`,
`CROSSPLAY_WARNING(3)`, `OFFLINE_WARNING(4)`, `CS_AUTOLOAD(7)` ?

**Elle se retourne.** Ces cinq ne sont pas un obstacle a franchir : la chaine
les PARCOURT (mesure : 6 puis 2), et c'est au moment de passer a
`CS_AUTOLOAD` qu'un bouchon de SEGA la renvoie au titre. Sauter les cinq
sauterait donc aussi `CS_AUTOLOAD` -- c'est-a-dire la seule etape que le
module veut vraiment atteindre.

**INCONNU, et a lire avant tout geste** : `FUN_1801CF090` et `FUN_1801CEF40`
(les deux autres predicats -- s'ils sont aussi des bouchons, le chemin entier
est fige), ce que vaut `etat+0x1c` chez nous (`FUN_1800E1940`), et si un autre
site demande 7 autrement que par un immediat (3 indetermines au 22.2).

---

## 23. LES DEUX PREDICATS -- ET DEUX DE MES AFFIRMATIONS A RABATTRE (SS 419.26)

**Lecture seule, Ghidra. RIEN N'A TOURNE.**

### 23.1 AUCUN DES DEUX N'EST UN BOUCHON

```c
longlong FUN_1801cf090(void)        // un drapeau a CONSOMMATION UNIQUE
{
  if (*(char *)(DAT_180796db0 + 0x11229) != '\0' &&
      *(char *)(DAT_180796db0 + 0x1122a) != '\0') {
    *(undefined1 *)(DAT_180796db0 + 0x1122a) = 0;    // il EFFACE en lisant
    return 1;
  }
  return 0;
}
```

```c
bool FUN_1801cef40(void)
{
  if (*(char *)(DAT_180796db0 + 0x11229) != '\0' &&
      FUN_1802cca00(&DAT_1807969a0) == '\0') {      // une tache est morte
    if (*(char *)(DAT_180796db0 + 0x1122c) != '\0') {
      if (thunk_FUN_1802aea80(0xffffffff, local_res8, 0, 0) == '\0') return false;
    }
    return FUN_1802cb570() != '\0';                 // la commande 212
  }
  return false;
}
```

**Les deux sont gouvernes par le MEME verrou** : `DAT_180796DB0 + 0x11229`.
S'il est nul, les deux rendent 0.

### 23.2 ET LE SECOND DEPEND DE NOTRE PROPRE REPONSE

`FUN_1802CB570`, lu :

```c
iVar1 = (**(code **)(DAT_180c8df28 + 0x1ff08))(..., 0xd4, 0);   // 212
return iVar1 == 1;
```

**Il n'accepte que 1. Notre hote repond 2** hors de STARTUP (switch de
`vf5fs_host.cpp`). Donc `FUN_1802CB570()` rend **faux**, et `FUN_1801CEF40()`
avec lui. **Dans notre course, `cVar2` vaut 0 -- par NOTRE fait.**

### 23.3 CE QUI OBLIGE A RABATTRE... ET LE RABATTEMENT ETAIT FAUX

**AVERTISSEMENT (SS 419.29, section 26) : CETTE SECTION EST ERRONEE.**
Elle repose sur << `g_modeTitre` est faux par defaut >>, qui est le
defaut du CODE ; le **lanceur** pose `VF5_TITRE=1` a sa ligne 34, et
l'en-tete de chaque journal l'imprime. Donc la 212 est servie a **1**,
`cVar2` est VRAI, et `FUN_1800E56E0` est bien l'ecrivain -- le SS 419.25
avait raison. Garde pour la lecon.

Relire `FUN_1800E56E0` avec ca en main :

```c
cVar1 = FUN_1801cf090();
cVar2 = FUN_1801cef40();        // = 0 chez nous (23.2)
if (cVar1 == '\0') {
    if (cVar2 == '\0') goto SANS_DEMANDE;   // <-- IL NE DEMANDE RIEN
    ...
}
```

| ce que j'ai ecrit au SS 419.25 | etat reel |
|---|---|
| 22.4 : << **L'ECRIVAIN** : `FUN_1800E56E0` >> | **TROP FORT.** C'est *un* site qui demande 5 et qui siege dans la bonne table. **Je n'ai jamais etabli qu'il tourne ET qu'il declenche dans notre course** -- et si les deux predicats sont faux, il ne demande RIEN. |
| 22.5 : << la boucle n'est PAS dans la reponse de notre hote : elle est dans le code livre du module >> | **NON ETABLI.** La commande 212 -- **notre** reponse -- ferme une des deux routes de cette fonction. Notre hote participe a la decision. |

C'est exactement le defaut que ma fiche
[[le-titre-d-une-fiche-porte-la-conclusion]] decrit : un titre qui affirme plus
que son corps.

### 23.4 CE QUI TIENT, ET C'EST L'ESSENTIEL

| acquis | degre |
|---|---|
| `FUN_18000BA20` = `XOR AL,AL ; RET`, desassemble | **CONFIRME** |
| donc la branche `uVar6 = 7` de `FUN_1800E56E0` est **du code mort**, et `CS_AUTOLOAD` est inatteignable PAR CETTE FONCTION | **CONFIRME** |
| la table `0x1803C8240` : trois phases + la liste ordonnee `00 01 08 05 06 02 03 04 07 49` | **CONFIRME** |
| le balayage : 77/77 cibles validees, 12 sites demandent 5 par un immediat | **CONFIRME** |
| **lequel des 12 declenche dans notre course** | **INCONNU** |
| les deux predicats ne sont pas des bouchons ; verrou commun `+0x11229` | **CONFIRME** |

### 23.5 LA PROCHAINE MESURE EST DEJA OUTILLEE, ET CE N'EST PAS 11 LECTURES

`FUN_1800E1B20` est un **point de passage unique** : une sonde a son entree
qui journalise l'**adresse de retour** nomme le site appelant en UNE course,
au lieu de decompiler les 11 autres candidats. C'est la technique deja payee
([[nommer-le-site-par-l-adresse-de-retour]], << 28 sites nommes en une
course >>), et elle repond aussi aux 3 sites indetermines du 22.2, que le
balayage statique ne peut pas trancher.

Deux garde-fous imposes par mes propres fiches : la sonde doit pouvoir
ECHOUER ([[un-invariant-sur-un-conteneur-vide-ne-verifie-rien]]), et elle ne
doit pas commenter une valeur qu'elle ne lit pas
([[une-sonde-ne-commente-pas-une-valeur-non-lue]]).

**ET UNE QUESTION QUI DEVIENT CONCRETE** : si `FUN_1801CEF40` est bien la
route attendue, alors repondre **1** a la commande 212 l'ouvrirait. Mais c'est
une reponse a changer dans l'hote, donc une CAUSE -- pas un interrupteur -- et
il faut d'abord savoir ce que SEGA repond a 212, par `cmd_oracle.py`
([[outil-cmd-oracle]]), avant d'y toucher.

---

## 24. L'ORACLE SUR 212 : NOTRE 2 N'EST PAS UNE DIVERGENCE (SS 419.27)

**Lecture seule du fichier `oracle_aout2026\VFREVO.exe`, jamais charge ni
execute. RIEN N'A TOURNE.**

Decode avec capstone, chaque gestionnaire **borne a son premier `E9`** --
sans quoi on lit le gestionnaire suivant, qui est adjacent
([[ret-1-par-defaut-repond-oui]]). L'auto-test l'affiche : 28, 79 et 10
octets sur 128 lus.

### 24.1 LA COMMANDE 212

```asm
1415CC00E  mov   rcx, [0x14342E9B0]      ; un objet global
1415CC015  call  0x142283BC0             ; un booleen dans AL
1415CC01A  movzx r14d, al
1415CC01E  xor   r14d, 1
1415CC022  inc   r14d
1415CC025  jmp   <sortie commune>        ; r14d = la reponse
```

`(al ^ 1) + 1`, donc **SEGA repond 1 si le predicat est VRAI, 2 s'il est
FAUX**. Et le module n'accepte que 1 (`FUN_1802CB570` rend `iVar1 == 1`).

### 24.2 ET LE PREDICAT EST UN APPEL VIRTUEL

```asm
142283BC0  mov rcx, [rcx + 0x30]     ; le sous-objet
142283BC4  mov rax, [rcx]            ; sa vtable
142283BC7  jmp [rax + 0x1F0]         ; VIRTUEL
```

Il depend donc de la **classe concrete installee a l'execution** : le
dos-d'oeuvre de plateforme. Irresolvable statiquement sans trouver quelle
classe est instanciee -- et inutile de le faire pour trancher (24.4).

### 24.3 LA COMMANDE 225 LIT LE MEME OBJET, ET SON DEFAUT EST 2

```asm
1415CC2EF  mov   rbx, [0x14342E9B0]       ; LE MEME objet qu'en 212
1415CC2F6  mov   r14d, 2                  ; <-- le DEFAUT est 2
           call 0x142283B80 ; test al,al ; je sortie      -> rend 2
           call 0x142283BE0
           call 0x142283B40 ; test al,al ; je sortie      -> rend 2
1415CC333  mov   r14d, 1                  ; seulement apres trois reussites
```

212 et 225 sont donc **deux interrogations d'un seul sous-systeme** (quatre
methodes groupees de `0x142283B40` a `0x142283BE0`).

### 24.4 LE VERDICT, ET IL DIFFERE DU CAS DU MATIN

**Notre 2 n'est pas une constante fausse : c'est la branche << faux >> de
SEGA**, et c'est son defaut explicite en 225. Or le predicat interroge le
dos-d'oeuvre de plateforme, et une regle du chantier est de rester **hors
ligne, sans Steam ni EOS**. Repondre 1 serait **affirmer une session de compte
que nous n'avons pas**.

Ce n'est donc **pas** le cas du `[+0x3F] &= 0xF0` du SS 419.21 : la-bas
l'oracle appliquait un ET **inconditionnel** que nous avions simplement
oublie de transcrire. Ici l'oracle est **conditionnel**, et notre constante
tombe sur la branche qui convient a un hote hors ligne.

**Donc la route par `FUN_1801CEF40` est LEGITIMEMENT fermee**, et il n'y a
rien a oter de ce cote.

### 24.5 UN CONTROLE GRATUIT, ET IL RETIRE UN DOUTE

```asm
1415CB096  call 0x1415ED1F0      ; la commande 21
1415CB09B  jmp  <sortie>         ; r14d NON touche -> la reponse par defaut
```

Le commentaire de notre hote, ecrit il y a longtemps, dit
`case 21: // SEGA : FUN_1415ED1F0 -- arrete +0x24`. **L'adresse concorde
exactement.** Donc la numerotation des commandes de notre hote EST celle que
le module emet, sans renumerotation -- ce qui etait un doute legitime
([[le-decalage-des-numeros-se-traduit-par-le-nom]]).

### 24.6 CE QUI RESTE, ET CE QU'IL NE FAUT PAS FAIRE

| candidat pour demander 5 | etat |
|---|---|
| `FUN_1801CEF40` (via cmd 212) | **FERME, et legitimement** (24.4) |
| `FUN_1801CF090` (drapeau verrouille `+0x1122A`) | possible -- les deux octets ne sont pas mesures |
| les 11 autres sites du balayage | **INCONNU** |
| les 3 sites indetermines (22.2) | **INCONNU**, hors de portee du statique |

**A NE PAS FAIRE** : repondre 1 a la commande 212 pour << ouvrir >> la route.
Ce serait feindre une session de compte, contre la regle hors ligne, et ca
enverrait sans doute la chaine dans des chemins en ligne qui ne peuvent pas
aboutir.

**LA PROCHAINE MESURE** reste celle du 23.5 : une sonde a l'entree de
`FUN_1800E1B20`, point de passage **unique**, qui journalise l'**adresse de
retour** et nomme le site en une course
([[nommer-le-site-par-l-adresse-de-retour]]). Elle tranche d'un coup les 11
candidats et les 3 indetermines, et elle doit pouvoir ECHOUER
([[un-invariant-sur-un-conteneur-vide-ne-verifie-rien]]).

---

## 25. LA SONDE DU VERROU A PARLE (SS 419.28)

**Course de 2500 images, `VF5_JOURNAL=1 VF5_EVTS=0 VF5_CLAVIER=1`, fermee a
la main. L'utilisateur a presse de quoi faire CINQ cycles.**

### 25.1 LA SONDE EST VIVANTE, ET LE CONTENEUR N'EST PAS VIDE

```
419.28 auto-test : base nulle -> non lu | base reelle -> lu
                   OK, la sonde distingue lu et non lu
```

| temoin | valeur |
|---|---|
| lectures reussies / non lues | **51 / 0** |
| sorties du titre dans la course | **5** |
| passages par `2=WARNING` | **5** |
| lignes de sonde **sur des images WARNING** | **10** |

C'est le controle qui manquait au SS 404 : une sonde qui n'imprime rien, ou
qui conclut sur zero echantillon, ne mesure rien
([[un-invariant-sur-un-conteneur-vide-ne-verifie-rien]]).

### 25.2 LE VERROU : DEUX ETATS, ET `+0x1122A` TOUJOURS NUL

Sur 51 lectures, **deux lignes distinctes seulement** :

| `+0x11229` | `+0x1122A` | `+0x1122C` | effet |
|---|---|---|---|
| 0 | 0 | 1 | `FUN_1801CF090` rend 0 ; porte de `FUN_1801CEF40` **FERMEE** |
| **1** | **0** | 1 | `FUN_1801CF090` rend 0 ; porte **OUVERTE** |

Et les **dix** lignes prises sur des images WARNING sont toutes de la seconde
forme. Donc :

- `FUN_1801CF090` exige `+0x11229` **et** `+0x1122A` non nuls : **il rend
  toujours 0**, donc `cVar1 = 0` ;
- `cVar2 = 0` aussi, par notre reponse 2 a la commande 212 (section 24).

### 25.3 DEUX CANDIDATS ELIMINES D'UN COUP

```c
if (cVar1 == '\0') { if (cVar2 == '\0') goto SANS_DEMANDE; ... }
```

**`FUN_1800E56E0` ne demande RIEN.** Mon << meilleur candidat >> du SS 419.25
tombe -- par la mesure, et c'est bien ainsi qu'il devait tomber.

**Et `FUN_1800E1B30` porte les DEUX MEMES predicats** (site `0x1800E1B58`),
donc lui non plus ne demande rien. Une seule mesure en elimine deux des douze.

### 25.4 MAIS `FUN_1800E1B30` EST LA ROUTE VERS LE MODE MENU

```c
FUN_1800b7950();
cVar1 = FUN_1801cf090();
cVar2 = FUN_1801cef40();
if (cVar1 == '\0') {
    if (cVar2 == '\0') { ... return; }     // NOTRE CAS : rien
    FUN_1800e1b00(5);                       // <-- MODE 5 = MENU
} else {
    FUN_1800e1b00(0); FUN_1800e1b20(5);     // STARTUP + CS_TITLE
}
```

`FUN_1800E1B00` demande un **MODE** (section 18.3). Donc avec `cVar2` vrai,
cette fonction demande **le mode MENU** -- exactement la progression
cherchee.

Et les conditions de `cVar2 = FUN_1801CEF40()`, une par une :

| condition | mesure |
|---|---|
| `+0x11229 != 0` | **VRAI** (=1, 25.2) |
| `FUN_1802CCA00(&DAT_1807969A0) == 0` (une tache morte) | non mesure |
| si `+0x1122C != 0` (=1), alors `thunk_FUN_1802AEA80(-1,...)` non nul | non mesure |
| **`FUN_1802CB570() != 0`, soit la commande 212 a 1** | **FAUX, par nous** |

**La seule condition que nous tenons est la derniere.**

### 25.5 ET L'INTERRUPTEUR EXISTE DEJA -- IL N'Y A RIEN A INVENTER

Notre `case 212` rend `g_modeTitre ? 1 : 2` dans STARTUP, et `g_modeTitre`
est **faux par defaut**. Son commentaire, ecrit il y a longtemps, dit :
<< 144.6 : la porte 1 de STARTUP/phase 1. Hors etat VFREVO rend 2 ; le module
exige 1. Derriere `set VF5_TITRE=1`, seule. >>

**Donc `VF5_TITRE=1` avait DEJA ete mesure necessaire a cette porte**, et le
defaut l'a perdu. Ca recoupe deux fiches : le menu a deja ete atteint
(`MENU/MENU_MAIN` des l'image 382,
[[le-menu-de-la-console-est-atteint]]), et le depot ne garde pas l'etat du
banc ([[le-depot-ne-garde-pas-l-etat-du-banc]]) -- << c'est le banc qui change
l'ecran, et aucun commit ne le dit >>. La configuration qui atteignait le menu
portait tres probablement cet interrupteur.

**La prochaine course est donc une MESURE avec `VF5_TITRE=1`**, une fois, puis
retour au defaut. Ce n'est pas un interrupteur neuf et ce n'est pas une
reparation : c'est le reglage de cette porte, remis a la valeur ou il avait
ete mesure.

### 25.6 LA LIMITE DE CETTE MESURE, A NE PAS TAIRE

La sonde lit **une fois par image, AVANT le pas du module**, et
`FUN_1801CF090` **efface `+0x1122A` quand il tire**. Un armement suivi d'une
consommation DANS LA MEME image serait donc invisible.

Ce qui attenue : la sonde voit bien changer `+0x11229` (0 -> 1), donc elle
capte les changements inter-images de ces octets.

**Degre** : << `+0x1122A` jamais vu non nul en 51 lectures couvrant 5 cycles
et 10 images WARNING >> est **CONFIRME** ; << il n'est jamais non nul >> est
**ETAYE**.

---

## 26. LA PORTE ETAIT OUVERTE : LE COMPTE SE FERME (SS 419.29)

**Aucune course. Tout vient du journal DEJA en main et du lanceur.**

### 26.1 MON ERREUR, ET ELLE EST GROSSE

J'ai ecrit au SS 419.26 : << `g_modeTitre` est FAUX par defaut, donc notre
hote repond 2 meme dans STARTUP >>. C'est le defaut du **code** (ligne 2968).
Mais le **lanceur** fait, a sa ligne 34 :

```bat
if not defined VF5_TITRE set "VF5_TITRE=1"
```

**Donc dans TOUTES les courses d'aujourd'hui `VF5_TITRE` valait 1**, et c'est
imprime dans l'en-tete de chaque journal que j'ai lu :

```
porte du titre (SS 144) : commande 0xD4 servie 1 -- OUVERTE (VF5_TITRE)
  [cmd 212] mode courant 0 -> 1   (VF5_TITRE=1, VF5_TITRE_SORTIE=1)
```

C'est exactement ce que mes deux fiches disent de faire et que je n'ai pas
fait : lire l'en-tete du journal avant de supposer
([[lire-l-en-tete-du-journal-de-l-hote]]), et se souvenir que pour onze
interrupteurs le lanceur ecrase l'initialiseur du code
([[grep-tronque-et-defaut-mort]]).

### 26.2 DONC `cVar2` EST VRAI -- ET LE JOURNAL LE DISAIT AUSSI

La ligne de mode que je lis depuis le matin :

```
mode (image 480) : 0=STARTUP phase=1 demande=5=MENU
```

**Le mode DEMANDE est 5 = MENU.** Or le seul demandeur de mode 5 dans cette
zone est `FUN_1800E1B30`, et il ne le fait que si `cVar2 != 0` :

```c
if (cVar1 == '\0') {
    if (cVar2 == '\0') { ... return; }
    FUN_1800e1b00(5);                 // <-- MODE MENU : c'est ce qu'on mesure
}
```

Donc `cVar2 = FUN_1801CEF40()` est **VRAI, CONFIRME par la mesure**, et ses
deux conditions que je n'avais pas mesurees (tache morte,
`thunk_FUN_1802AEA80`) sont satisfaites.

### 26.3 LE SS 419.25 AVAIT RAISON ; LE SS 419.26 L'A RABATTU A TORT

Tout s'emboite, et chaque maillon est maintenant mesure ou desassemble :

| maillon | etat |
|---|---|
| `cVar1 = FUN_1801CF090()` = 0 (`+0x1122A` toujours nul) | **mesure**, SS 419.28 |
| `cVar2 = FUN_1801CEF40()` = vrai (212 servie a 1) | **mesure**, 26.1-26.2 |
| `FUN_1800E1B30` demande le **mode MENU** | **mesure** (`demande=5=MENU`) |
| `FUN_1800E56E0` exige `etat+0x1c` ∈ {2,7} ; vaut **2** a l'image WARNING | **mesure** |
| `FUN_18000BA20()` = `XOR AL,AL ; RET`, donc 0 | **desassemble** |
| donc `goto LAB_1800E5711` -> **demande 5 = CS_TITLE** | **deduit, et conforme a la mesure** |

**`FUN_1800E56E0` EST BIEN L'ECRIVAIN.** Mon candidat initial etait juste ;
je l'ai rabattu au SS 419.26 sur une lecture fausse du defaut, et la sonde du
SS 419.28 n'a pas corrige l'erreur parce qu'elle ne mesurait que `cVar1`.

**Ce qui reste vrai du SS 419.28** : `cVar1` est bien toujours 0, donc la
route par le drapeau verrouille est bien morte, et `FUN_1800E1B30` passe bien
par sa branche `cVar2`. La sonde a mesure juste ; c'est mon cadre qui etait
faux.

### 26.4 LE TABLEAU COMPLET DU BLOCAGE

1. le mode **MENU est demande** et ne vient pas ;
2. parce que le changement de mode attend que la chaine des sous-etats
   atteigne sa fin (`73`, le dernier de la liste a `0x1803C8260`) ;
3. or a l'image WARNING, `FUN_1800E56E0` devrait demander **7 =
   CS_AUTOLOAD** -- le sous-etat suivant dans cette liste ;
4. et il demande **5 = CS_TITLE** a la place, **parce que
   `FUN_18000BA20` est un bouchon a zero dans le binaire livre** ;
5. donc la chaine revient au titre, indefiniment.

Et le balayage des 77 sites ne trouve **aucun** demandeur de `7` par un
immediat (degre : ETAYE -- 3 sites restent indetermines, section 22.2).

### 26.5 CE QUI RAMENE A LA QUESTION DU DEPART, MAIS GAGNEE

La question etait : peut-on sauter `CS_SIGNIN`, `WARNING`,
`CROSSPLAY_WARNING`, `OFFLINE_WARNING`, `CS_AUTOLOAD` ?

**La reponse mesuree est plus etroite et bien meilleure : il n'y a pas cinq
etats a sauter, il y a UNE transition a fournir.** La table du module dit que
`CS_AUTOLOAD` suit `WARNING` ; la seule fonction qui la demanderait a son
predicat bouchonne a zero dans le binaire livre.

**LE GESTE QUE CA NOMME** : que l'hote demande **le sous-etat 7** a l'image ou
le module est en `WARNING` et ou `FUN_1800E56E0` vient de demander 5. Ce n'est
pas un saut arbitraire : c'est fournir la transition que la liste du module
prevoit et qu'un bouchon de SEGA rend inatteignable. Demander une scene est
une ecriture que l'hote sait faire
([[demander-une-scene-est-une-ecriture]]).

**CE QU'IL FAUT ETABLIR AVANT** : que `CS_AUTOLOAD` ait de quoi tourner chez
nous -- c'est le chargement de la sauvegarde systeme, et l'hote repond deja
aux commandes 156/157 ([[le-menu-de-la-console-est-atteint]]). Et lire les
trois phases de l'entree `07` de la table des scenes avant de l'appeler.

---

## 27. CS_AUTOLOAD, LU EN ENTIER -- LA VOIE EST LIBRE (SS 419.30)

**Lecture seule, Ghidra. RIEN N'A TOURNE.**

### 27.1 LA TABLE DES SCENES, AUX ENTREES 06-08

Pas 0x20 octets, `+0x00` le numero, `+0x08`/`+0x10`/`+0x18` les trois phases :

| adresse | n° | phase 0 | phase 1 | phase 2 |
|---|---|---|---|---|
| `0x1803C88B0` | 06 CS_SIGNIN | `1800E5E50` | `1800E5570` | **`180026620`** (bouchon) |
| **`0x1803C88D0`** | **07 CS_AUTOLOAD** | **`1800E5D40`** | **`1800E54F0`** | **`1800E59C0`** |
| `0x1803C88F0` | 08 CS_DEMO | `1800E5D70` | `1800E5510` | `1800E59F0` |

**Les trois phases de `07` sont du vrai code** -- aucune n'est le bouchon
`0x180026620`, contrairement a la phase 2 de son voisin `06`.

### 27.2 LES TROIS PHASES

```c
// phase 0 -- FUN_1800E5D40 : aucun predicat, return 1 inconditionnel
*(undefined4 *)(DAT_1807514c8 + 0x5c) = 0;          // <-- ARME la sequence
FUN_1802cd240(DAT_1807514c8, 0, "TaskAutoLoad");
return 1;

// phase 1 -- FUN_1800E54F0 : attend la mort de la tache
return FUN_1802cca00(DAT_1807514c8) ^ 1;

// phase 2 -- FUN_1800E59C0 (deja desassemblee au SS 419.20) :
//   tue [0x1807514C8] ; FUN_1800E1B00(5) ; FUN_1800E1B20(0x49)
//   -> MODE MENU + SOUS-ETAT 73
```

**La phase 2 demande exactement la fin de la liste de la chaine console**
(`... 07 49`, section 22.3). Atteindre `CS_AUTOLOAD` *est* ce qui ouvre le
menu.

### 27.3 LA TACHE `TaskAutoLoad`, ET SA SORTIE EST UN << OUI >>

Constructeur `FUN_1800E4E00`, desassemble :

```asm
1800e4e0b  MOV  ECX, 0x68                   ; l'objet fait 0x68 octets
1800e4e2a  LEA  RAX, [0x1803c9af0]
1800e4e31  MOV  qword ptr [RBX], RAX        ; la vtable
1800e4e38  MOV  qword ptr [RBX + 0x5c], 0x13
1800e4e44  MOV  qword ptr [0x1807514c8], RBX
```

`0x1803C9AF0` est l'adresse que le RTTI donne pour **`TaskAutoLoad`** --
deuxieme confirmation que cette colonne est la vtable.

| entree | adresse | role |
|---|---|---|
| +0x08 | `0x1800E5C40` | phase 1 : deux champs a zero, `return 1` |
| +0x10 | `0x1800E5200` | phase 2 : la sequence (27.4) |
| **+0x18** | **`0x180026620`** | **sortie : `MOV AL,1 ; RET`** -- oui immediat |

### 27.4 LA SEQUENCE DE 19 ETAPES, ET QUI L'ARME

```c
// FUN_1800E5200
if (*(int *)(param_1 + 0x5c) < 0x13) {
    if (table[*(int *)(param_1 + 0x5c)] != 0) {
        (*table[*(int *)(param_1 + 0x5c)])();     // PTR_FUN_18063DC60
        return *(undefined1 *)(param_1 + 0x58);
    }
} else {
    *(undefined1 *)(param_1 + 0x58) = 1;          // >= 0x13 : termine
}
return *(undefined1 *)(param_1 + 0x58);
```

`+0x5c` est un compteur d'etape dans `PTR_FUN_18063DC60` (0x13 = **19**
entrees), `+0x58` le temoin de fin.

**Et l'intention se lit dans les deux ecritures de `+0x5c`** : le
constructeur pose **0x13** -- << rien a faire, termine d'emblee >> -- et **la
phase 0 de CS_AUTOLOAD le remet a 0**, ce qui ARME les 19 etapes. Le module
veut donc vraiment charger quand il entre dans ce sous-etat.

### 27.5 VERDICT, ET IL N'Y A PAS A LIRE LES 19 ETAPES

**Rien sur le chemin de `CS_AUTOLOAD` n'est bouchonne** : ses trois phases
sont du code, la sortie de sa tache rend 1 tout de suite, et sa phase 2 mene
au menu. Le seul inconnu est si les **19 etapes** aboutissent hors ligne.

| acquis | degre |
|---|---|
| les trois phases de l'entree 07, aucune bouchonnee | **CONFIRME** |
| la phase 2 demande mode MENU + sous-etat 73 | **CONFIRME** (desassemble) |
| vtable `TaskAutoLoad` = `0x1803C9AF0`, sortie = `MOV AL,1 ; RET` | **CONFIRME** |
| la phase 0 arme les 19 etapes (`+0x5c = 0`) | **CONFIRME** |
| les 19 etapes aboutissent chez nous | **INCONNU -- mais MESURABLE** |

**Et c'est la le point pratique** : inutile de decompiler les 19 etapes. Si
l'hote demande le sous-etat 7, la course tranche en quelques secondes -- soit
la chaine avance vers mode MENU et sous-etat 73, soit elle reste en
`CS_AUTOLOAD` phase 1, ce qui se VOIT dans le journal et ne casse rien.
Lire 19 fonctions pour predire ce qu'une course dit tout de suite serait
l'inverse de << epuiser la lecture >> : ici la lecture est epuisee pour la
DECISION, et le reste est du ressort de la mesure.

**LE GESTE** : que l'hote demande le sous-etat **7** quand le module est en
`WARNING` et que `FUN_1800E56E0` vient de demander 5. Demander une scene est
une ecriture ([[demander-une-scene-est-une-ecriture]]) -- un dword et deux
octets dans l'objet `VF5FS+0x7513F0`, celui que l'hote lit deja a chaque
image. Ce n'est pas un saut : c'est fournir la transition que la liste du
module prevoit et que le bouchon `FUN_18000BA20` rend inatteignable.

---

## 28. LES 19 ETAPES DE `TaskAutoLoad`, LUES (SS 419.31)

**Lecture seule : Ghidra + un balayage capstone. RIEN N'A TOURNE.**

### 28.1 LA TABLE, ET SON PROPRE CONTROLE

`PTR_FUN_18063DC60`, 19 qwords **non nuls**, et **le 20e est NUL** -- ce qui
recoupe exactement la borne `*(int *)(obj + 0x5c) < 0x13` de `FUN_1800E5200`.
Les 19 corps se suivent de `0x1800E4220` a `0x1800E4E00` (le constructeur).

**Aucune des 19 n'est le bouchon `0x180026620`.**

### 28.2 CE QUE J'AVAIS MAL NOMME, ET LA CORRECTION

J'ai d'abord lu les commandes 1/2/3 comme des entrees-sorties de fichier.
**C'est FAUX, et mon propre `vf5fs_host.cpp` le disait** : cmd 1 **ouvre une
boite de dialogue**, cmd 2 la **sonde** (<< 1 ou 2 = repondu, le module ferme ;
autre = il attend >>), cmd 3 la **ferme**. Donc `FUN_1802316E0(0x5e4b)` n'est
pas un nom de fichier : c'est un **identifiant de texte**, le message de la
boite. Cinq identifiants paraissent : `0x5e4b`, `0x5e4c`, `0x5e4d`, `0x5e4e`,
`0x5e4f`.

Encore [[agir-sur-mes-propres-notes]] : le commentaire du `case 1` portait
deja l'analyse, SS 310.

### 28.3 LES SEPT COMMANDES, PAR BALAYAGE MECANIQUE

Balayage capstone des 19 bornes (2e argument, donc `EDX`, avant chaque appel
indirect), avec quatre auto-tests dont un qui **a echoue d'abord** et m'a fait
corriger le fichier lu :

| etape | commandes | etape | commandes |
|---|---|---|---|
| 0 | (aucune) | 10 | 1 |
| 1 | **163** | 11 | 3 |
| 2 | 1 | 12 | (aucune) |
| 3 | 2, 3 | 13 | 1 |
| 4 | 1 | 14 | 2, 3 |
| 5 | 2, 3 | 15 | **421** |
| 6 | (aucune) | 16 | 1 |
| 7 | (aucune) | 17 | 3 |
| 8 | 1 | 18 | **251, 250** |
| 9 | 2, 3 | | |

**Toutes les commandes employees : 1, 2, 3, 163, 250, 251, 421.** Et le
balayage n'en ajoute AUCUNE a la lecture a la main -- l'auto-test l'exigeait.

**NI RESEAU, NI EOS, NI STEAM.** C'est le resultat qui compte : la sequence ne
depend que de nous et de deux attentes locales.

### 28.4 LE GRAPHE DES ETATS

`+0x5c` est l'etape, `+0x58` le temoin de fin, `+0x60` un compteur d'images,
`+0x64`/`+0x65` deux drapeaux. **Ce n'est pas un compteur qui s'incremente** :
chaque etape s'assigne la suivante.

| etape | ce qu'elle fait | vers |
|---|---|---|
| 0 | appelle le bouchon `0x180026620` (rend **toujours 1**) | **1** (le 18 est inatteignable) |
| 1 | **cmd 163** | 10 si != 0, sinon **2** |
| 2 | cmd 1, texte `0x5e4b`, op 2 | 3 |
| 3 | cmd 2 puis cmd 3 | 15 si `r[1]==0`, 8 sinon, **sondage** si statut ni 1 ni 2 |
| 4 | cmd 1, texte `0x5e4e`, op 2 | 5 |
| 5 | cmd 2 puis cmd 3 | 2 / 12 / 8, **sondage** |
| 6 | lance la tache de sauvegarde (aucun predicat) | 7 |
| 7 | **attend `FUN_1801CF0C0`** = la tache morte | **18** / 4 / 2, **sondage** |
| 8 | cmd 1, texte `0x5e4c` | 9 |
| 9 | cmd 2 puis cmd 3 | 8 / **18** / 2 / 10 |
| 10 | cmd 1, texte `0x5e4d`, **op 3**, et remet `+0x60` a 0 | 11 |
| 11 | **minuteur : rien avant `+0x60 > 0x3b`** (60 images) | 12 / **18** / 13 |
| 12 | attend la tache morte | 4 / **18**, **sondage** |
| 13 | cmd 1, texte `0x5e4f` | 14 |
| 14 | cmd 2 puis cmd 3 | 6 / 8, **sondage** |
| 15 | bouchon (1) puis **cmd 421** | 16 si != 0, sinon **6** |
| 16 | jumelle de 10 | 17 |
| 17 | jumelle de 11 (minuteur) | 12 / 7 / 6 |
| 18 | **cmd 251, cmd 250, puis `+0x58 = 1`** | **TERMINUS** |

Deux details qui se recoupent : les etapes 10 et 16 ecrivent **huit** octets a
`+0x5c`, ce qui **remet `+0x60` a zero** -- c'est deliberes, elles arment le
minuteur des etapes 11 et 17. Et le minuteur de 60 images est le temps
d'affichage minimum du bandeau << ne pas eteindre >>.

### 28.5 LA ROUTE AVEC NOS DEFAUTS ACTUELS

| commande | notre reponse | d'ou |
|---|---|---|
| 1, 2, 3 | **servies** ; `g_dialogue = 1` par defaut, donc cmd 2 ecrit `{1,0,0,0}` | `case 1/2/3`, SS 310 |
| 163 | **0** -- aucun `case`, le defaut n'ecrit RIEN dans `args` | balaye |
| 421 | **0** -- idem | balaye |
| 250, 251 | **0** -- idem, mais l'etape 18 ne lit pas leur reponse | balaye |

Et `g_dialogue` est pose par `getenv` dont la **valeur** est lue, donc le
defaut TIENT -- ce n'est pas un des onze defauts morts de
[[grep-tronque-et-defaut-mort]].

Donc, `local_18 = 1` et `local_14 = 0` a chaque cmd 2 :

**`0 -> 1 -> 2 -> 3 -> 15 -> 6 -> 7`**

Les sondages ne se garent pas : la cmd 2 repond 1, donc les etapes 3, 5, 9 et
14 avancent. **Mon risque annonce d'un sondage infini a l'etape 3 ne se
produit pas** -- c'est le defaut `g_dialogue = 1` qui l'evite, et je ne
l'aurais pas su sans le verifier.

### 28.6 OU TOUT SE DECIDE : DEUX OCTETS QUE MA SONDE LIT DEJA

A l'etape 7, `FUN_1801D0300` :

```c
undefined1 FUN_1801d0300(undefined4 *param_1) {
  longlong lVar1 = DAT_180796db0;
  if (param_1 != 0) *param_1 = *(undefined4 *)(DAT_180796db0 + 0x11088);
  return *(undefined1 *)(lVar1 + 0x11085);
}
```

**C'est le MEME objet `DAT_180796DB0` que ma sonde du SS 419.28 lit deja**
(elle y prend `+0x11229`, `+0x1122A`, `+0x1122C`). Donc :

| `+0x11085` | `+0x11088` | l'etape 7 va vers |
|---|---|---|
| != 0 | -- | **18 = TERMINUS, la tache meurt** |
| 0 | 1 | 4 (puis 5) |
| 0 | autre | 2 -- **et on boucle `2->3->15->6->7`** |

Et qui ecrit ces octets ? La tache que l'etape 6 lance et que l'etape 7
attend : **`TaskCsSystemSaveData`**, pilotee par les commandes **156 et 157**,
**que nous servons deja** (SS 311, commentaire du `case 156` dans
`vf5fs_host.cpp`).

### 28.7 VERDICT

| acquis | degre |
|---|---|
| 19 etapes, aucune bouchonnee, 20e qword NUL | **CONFIRME** |
| les 7 commandes employees, et aucune autre | **CONFIRME** (balayage + auto-test) |
| ni reseau, ni EOS, ni Steam dans les 19 etapes | **CONFIRME** |
| cmd 1/2/3 = boite de dialogue, pas fichier | **CONFIRME** |
| l'etape 18 pose `+0x58 = 1` et termine la tache | **CONFIRME** |
| la route `0->1->2->3->15->6->7` avec nos defauts | **ETAYE** (deduit des reponses, pas mesure) |
| ce que valent `+0x11085` et `+0x11088` a l'etape 7 | **INCONNU** |

**IL N'Y A PLUS RIEN A LIRE POUR DECIDER.** Le seul inconnu est deux octets
d'un objet que notre sonde atteint deja, et le service qui les ecrit est
implemente. Donc le geste -- demander le sous-etat **7** -- se pose avec sa
mesure dans la MEME course : deux champs de plus dans la sonde du SS 419.28,
et le journal dira si l'etape 7 part en 18 (fini), en 4, ou boucle.

---

## 29. LE GESTE POSE, ET SA MESURE (SS 419.32)

**Pose dans `vf5fs_host.cpp`, compile, copie dans le banc. LA COURSE N'A PAS
ENCORE TOURNE.**

### 29.1 CE QUI A ETE VIDE SUR LE DISQUE -- 57 FICHIERS

`VF5RE/vider_fonctions.py --liste VF5RE/a_vider.txt`, **57 videes sur 57**,
dans `VF5RE/code_decompile/`. Index verifie contre le disque :

- **les 19 etapes de `TaskAutoLoad` (`PTR_FUN_18063DC60`)** (19) : `FUN_1800e4220`, `FUN_1800e4260`, `FUN_1800e4290`, `FUN_1800e4340`, `FUN_1800e4410`, `FUN_1800e44b0`, `FUN_1800e45a0`, `FUN_1800e45e0`, `FUN_1800e4630`, `FUN_1800e46d0`, `FUN_1800e47c0`, `FUN_1800e4870`, `FUN_1800e4910`, `FUN_1800e4960`, `FUN_1800e4a00`, `FUN_1800e4ae0`, `FUN_1800e4b10`, `FUN_1800e4bb0`, `FUN_1800e4c70`
- **la tache elle-meme (vtable `0x1803C9AF0`)** (4) : `FUN_1800e4e00`, `FUN_1800e5c40`, `FUN_1800e5200`, `FUN_180026620`
- **`CS_AUTOLOAD` : les 3 phases de l'entree 07 (`0x1803C88D0`)** (3) : `FUN_1800e5d40`, `FUN_1800e54f0`, `FUN_1800e59c0`
- **les enveloppes de commandes et les portes** (5) : `FUN_1802cbd60`, `FUN_1802cb390`, `FUN_1801cf0c0`, `FUN_1801d0300`, `FUN_1802cca00`
- **les predicats de la boucle du titre** (10) : `FUN_1800e56e0`, `FUN_1800e1b30`, `FUN_1801cf090`, `FUN_1801cef40`, `FUN_1802cb570`, `FUN_18000ba20`, `FUN_18000ba10`, `FUN_1800e2300`, `FUN_1800e1b00`, `FUN_1800e1b20`
- **`WARNING` et sa phase de sortie** (2) : `FUN_1800e5900`, `FUN_1801dec30`
- **les appelees citees dans les 19 etapes** (14) : `FUN_1801cef20`, `FUN_1801cf1d0`, `FUN_1801cf1e0`, `FUN_1801cfd80`, `FUN_1801cedd0`, `FUN_1801cedc0`, `FUN_1801cfb00`, `FUN_1802316e0`, `FUN_1801dd040`, `FUN_1801dd2c0`, `FUN_1801d5970`, `FUN_1801db880`, `FUN_180228250`, `FUN_180267d70`

### 29.2 LE GESTE

**Ce n'est pas un saut d'ecrans, et ce n'est pas un interrupteur.** C'est une
transition que la table du module PRESCRIT et que son binaire livre ne peut
pas prendre.

La liste de la chaine console, dans les donnees (`0x1803C8240`) :
`00 01 08 05 06 02 03 04 07 49`. Le changement de MODE attend `73`. Sans
`CS_AUTOLOAD` (= 7), le mode MENU demande ne vient jamais.

Et la seule fonction qui demande 7 le fait **depuis l'etat 2 = WARNING** :

```c
// FUN_1800E56E0, mode 0 phase 1
if (etat+0x1c != 2 && etat+0x1c != 7) goto SANS_DEMANDE;
cVar1 = FUN_18000ba20(FUN_18000ba10());
if (cVar1 == '\0') goto LAB_1800e5711;   // -> 5 = CS_TITLE
if (etat+0x1c != 2) goto SANS_DEMANDE;
uVar6 = 7;                               // <-- CODE MORT
```

`FUN_18000BA20` est `XOR AL,AL ; RET` -- un zero dur, **desassemble**. La
branche qui demande 7 est donc inatteignable, et c'est 5 qui part.

**Ce qu'on ecrit, rien de plus.** `FUN_1800E1B20(n)`, desassemblee :

```asm
1800e1b20  MOV  dword ptr [0x180751410], ECX   ; objet d'etat +0x20
1800e1b26  MOV  byte  ptr [0x18075141c], 0x1   ; +0x2C, l'armement
```

Un dword et **UN** octet -- c'est `FUN_1800E1B00`, la demande de MODE, qui en
ecrit deux. Ne pas confondre les deux fonctions.

```c
static void FournirCsAutoload(int image, uint8_t* mo) {
    if (!mo || !PlageLisible(mo, 0x38)) return;
    if (mo[0x2C] == 0) return;                        // aucune demande armee
    if (*(const uint32_t*)(mo + 0x1C) != 2u) return;  // pas en WARNING
    if (*(const uint32_t*)(mo + 0x20) != 5u) return;  // il ne demande pas 5
    *(uint32_t*)(mo + 0x20) = 7u;
    mo[0x2C] = 1;
    ...temoin 419.32...
}
```

**On ne CHOISIT pas la cible** : 7 est lu dans la branche morte elle-meme. On
ne saute donc pas `CROSSPLAY_WARNING` ni `OFFLINE_WARNING` par preference --
c'est le module qui, depuis l'etat 2, veut aller en 7.

**AUCUN INTERRUPTEUR NEUF, actif par defaut.** L'appel est pose **hors** du
bloc etrangle `image < 3 || chg249 || image % 50` -- c'etait le piege du
SS 364, et mon propre commentaire a cet endroit le rappelait.

### 29.3 LA MESURE, DANS LA MEME COURSE

Lire `FUN_1801CFD80` (le lanceur appele par l'etape 6) a change le plan : elle
**ecrase elle-meme** `+0x11085 = 0` et `+0x11088 = 3` avant de poser la tache,
et elle a **quatre portes**. Une sonde a deux champs n'aurait rien explique.
La sonde du SS 419.28 en lit donc **cinq de plus** :

| champ | role | etat |
|---|---|---|
| `+0x1122C` | porte 1 du lanceur | **mesure = 1** (SS 419.28) |
| `+0x11080` | porte 3 : `== FUN_18000BA10()` qui rend **0** | a mesurer |
| `+0x96A8` | porte 4 : non nul (l'etape 6 passe `param_1 = 1`) | a mesurer |
| `+0x11085` | ce que `FUN_1801D0300` **rend** | a mesurer |
| `+0x11088` | ce qu'il **recopie** | a mesurer |

Et la sonde **dit la conclusion** au lieu de laisser des chiffres nus :
`l'etape 7 irait vers L'ETAPE 18 = TERMINUS` / `l'etape 4` /
`l'etape 2 -- DONC LA SEQUENCE BOUCLE`.

### 29.4 CE QUE LA COURSE PEUT DIRE, ET LES TROIS CAS

| si le journal montre | alors |
|---|---|
| aucune ligne `419.32 : image ...` | le geste n'a **pas** tourne -- rien d'autre n'est a commenter |
| `+0x11085` non nul | l'etape 7 part en **18**, la tache meurt, et la phase 2 demande **mode MENU + sous-etat 73** |
| `+0x11085 = 0` et `+0x11088 = 1` | elle part en etape 4, la sequence continue |
| `+0x11085 = 0` et `+0x11088 = 3` | **elle boucle `2->3->15->6->7`** -- et les portes 3 et 4 diront laquelle a refuse la tache |

**Controle du geste** : script separe, lance sur la copie d'AVANT -- **10
echecs sur 11** -- puis sur le fichier pose -- **11 sur 11**. Un controle qui
passe partout ne controle rien.

**Binaire** : `vf5fs_host.exe` du 8 nov 15:26, et les trois chaines-temoins
sont presentes dedans.

---

## 30. L'ETAT 40 EST ATTEINT (PAS LE MENU) -- ET LA CAUSE REELLE DE LA BOUCLE (SS 419.33, rabattu au 419.36)

**Course de 891 images, `VF5_JOURNAL=1 VF5_EVTS=0 VF5_CLAVIER=1`, fermee a la
main par l'utilisateur. ENTREE pressee vers l'image 875.**

### 30.0 RABATTEMENT, AVANT TOUT LE RESTE (SS 419.36)

**J'ai ecrit << MENU_MAIN ATTEINT >>. C'est un ETAT, pas un ecran.**
L'utilisateur n'a **rien vu**, et il a raison de refuser la phrase.

Ce qui est mesure : le mode vaut 5, le sous-etat vaut 40, et la phase 0 cree
l'objet nomme `"MAIN MENU"`. **Des variables en memoire.**

Ce qui n'est PAS mesure : qu'une interface paraisse. Et
`FUN_18020F1E0` ne batit le menu **que si `bloc+0x1FF08` est NUL** : notre
repartiteur etant pose, **le module DELEGUE le dessin et nous ne dessinons
rien**. Donc l'ecran du menu n'existe tres probablement pas.

Tout ce qui suit dans cette section porte sur la MACHINE D'ETATS, et sur rien
d'autre.

### 30.1 LA CHAINE, IMAGE PAR IMAGE

| image | sous-etat | demande |
|---|---|---|
| 875 | CS_TITLE phase 2 | 6 = CS_SIGNIN |
| 876 | CS_SIGNIN phase 2 | 2 = WARNING |
| 877 | WARNING phase 1 | **3 = CROSSPLAY_WARNING** |
| 878 | *le geste tire* | **7 = CS_AUTOLOAD** |
| 879 | CS_AUTOLOAD phase 1 | 73 |
| 880 | CS_AUTOLOAD phase 2 | mode STARTUP phase 2 |
| **881** | **40 = MENU_MAIN** (l'etat, pas l'ecran) | **mode 5 = MENU** |

**Trois images entre le geste et le menu.** Le temoin a paru **une seule
fois** -- le geste ne se repete pas, puisque la chaine quitte WARNING pour de
bon.

### 30.2 LES CINQ CHAMPS, ET POURQUOI C'ETAIT SI RAPIDE

| image | `+0x11080` | `+0x11085` | `+0x11088` | `+0x96A8` |
|---|---|---|---|---|
| 0 | **4294967295** | 0 | 3 | 1 |
| 1, 2, 307, 316 | 0 | 0 | 3 | 1 |
| **876, 877, 878** | 0 | **1** | **0** | 1 |

**Les quatre portes du lanceur PASSENT** (`+0x1122C` non nul, `+0x11080 == 0`,
`+0x96A8 != 0`).

Et le detail qui explique les deux images : **`+0x11085` valait DEJA 1 a
l'image 876**, avant le geste. La tache de sauvegarde avait donc deja tourne
et REUSSI pendant la boucle du titre -- les cycles CS_SIGNIN/WARNING appellent
`FUN_1801CFD80` eux aussi. Donc quand `CS_AUTOLOAD` est enfin entre, son
etape 7 a lu 1 tout de suite, est partie en **etape 18**, qui pose
`+0x58 = 1` : la tache meurt, la phase 1 de la scene rend 1, et la phase 2
demande mode MENU + sous-etat 73.

**La sonde lit bien de la memoire vivante** : `+0x11080` vaut `-1` a l'image 0
puis 0 a l'image 1. Un instrument qui rendrait une constante n'aurait pas
montre cette initialisation.

### 30.3 UN DEFAUT DE MA SONDE, A DIRE

Les cinq lignes des images 0 a 316 concluent **<< DONC LA SEQUENCE BOUCLE >>**
alors que la sequence **ne tournait pas du tout** a ces images. Le verdict
n'a de sens que pendant que la tache est vivante ; ma formulation l'affirme
sans cette reserve.

Ca ne m'a pas trompe ici, parce que les images sont dans la ligne. Mais c'est
le defaut que [[une-sonde-ne-commente-pas-une-valeur-non-lue]] decrit : une
sonde ne doit pas commenter un etat qu'elle n'est pas en train d'observer.
**A corriger : ne rendre le verdict que si la tache de `CS_AUTOLOAD` existe.**

### 30.4 LA CAUSE REELLE DE LA BOUCLE, PLUS FINE QUE CE QUE J'AVAIS ECRIT

J'ai ecrit, aux sections 27 a 29, que **rien** ne demandait le sous-etat
suivant. **C'est inexact, et la mesure le montre** :

- image **877** : `WARNING phase 1` demande **3 = CROSSPLAY_WARNING`** -- la
  scene demande donc bien sa suivante, et la bonne ;
- image **878** : la demande vaut **5 = CS_TITLE**.

Entre les deux, **`FUN_1800E56E0` a ECRASE la demande**. Elle tourne a CHAQUE
image (mode 0, phase 1) et, son predicat `FUN_18000BA20` rendant un zero dur,
elle repose 5 par-dessus le 3 que `WARNING` venait de demander.

**La boucle n'est donc pas une demande absente : c'est un ECRASEMENT.**

### 30.5 CE QUE CA CHANGE POUR LA SUITE, ET CE QUE MON GESTE EST VRAIMENT

Mon geste **substitue une destination** : il remplace le 5 par 7. Il marche --
`MENU_MAIN` est atteint -- mais il n'ote pas la cause, et il fait sauter
`CROSSPLAY_WARNING` et `OFFLINE_WARNING`, que la chaine voulait traverser.

**La variante fidele est maintenant identifiable** : empecher
`FUN_1800E56E0` d'ecraser la demande de la scene quand celle-ci en a deja
posee une. Alors la chaine marcherait `2 -> 3 -> 4 -> 7` d'elle-meme, par ses
propres demandes, et `CS_AUTOLOAD` serait atteint sans qu'on nomme aucune
destination. C'est << une cause otee >> au sens de la regle du chantier, la ou
mon geste est une destination fournie.

### 30.6 VERDICT

| acquis | degre |
|---|---|
| le geste tire une fois, image 878 | **CONFIRME** |
| `CS_AUTOLOAD` entre, ses deux phases tournent | **CONFIRME** |
| le mode vaut 5 et le sous-etat 40 a l'image 881 | **CONFIRME** |
| **un menu PARAIT a l'ecran** | **NON MESURE -- rien n'a ete vu, et le module delegue le dessin** |
| les 4 portes du lanceur passent ; `+0x11085 = 1` des 876 | **CONFIRME** |
| la boucle est un ECRASEMENT par `FUN_1800E56E0`, pas une demande absente | **ETAYE** (877 demande 3, 878 demande 5) |
| le menu TIENT | **NON MESURE** -- il n'a vecu que 10 images |

---

## 31. LA CAUSE OTEE, ET LA TABLE DES MODES AU COMPLET (SS 419.34)

**Pose, compile, copie dans le banc. LA COURSE N'A PAS ENCORE TOURNE.**

### 31.1 POURQUOI LA CAUSE NE PEUT PAS S'OTER DANS LE MODULE

Le predicat fautif est `FUN_18000BA20` = `XOR AL,AL ; RET`. Deux octets
(`31 C0` -> `B0 01`) suffiraient a le faire rendre 1, a longueur egale.

**Mais il a 291 references**, dont une centaine en **DATA** : c'est le
`return 0` GENERIQUE du module, pose comme entree de vtable par defaut dans
des dizaines de classes. **Un seul** de ces 291 sites est le notre
(`VF5FS+0xE57F2`, dans `FUN_1800E56E0`). Le retourner changerait le
comportement de tout le module.

C'est une mesure, pas une supposition -- d'ou le refus. Et c'est le genre de
chiffre qu'il faut compter avant d'annoncer une reparation
([[compter-avant-d-annoncer-un-nombre]]).

### 31.2 CE QU'ON FAIT A LA PLACE : REPOSER, SANS NOMMER

```c
static void RendreLaDemandeDeLaScene(int image, uint8_t* mo) {
    const uint32_t sous = *(const uint32_t*)(mo + 0x1C);
    const uint32_t dem  = *(const uint32_t*)(mo + 0x20);
    const uint8_t  arme = mo[0x2C];
    if (sous != g_sousVu) { g_sousVu = sous; g_demScene = 0xFFFFFFFFu; }
    if (sous != 2u && sous != 7u) return;     // la borne de FUN_1800E56E0
    if (!arme) return;
    if (dem != 5u) { if (dem != sous) g_demScene = dem; return; }
    if (g_demScene == 0xFFFFFFFFu) return;
    *(uint32_t*)(mo + 0x20) = g_demScene;     // on REPOSE la valeur du module
    mo[0x2C] = 1;
    ...temoin 419.34...
}
```

**On ne nomme AUCUNE destination.** La precedente version ecrivait `7` ; celle
-ci repose ce que le module avait lui-meme ecrit. La chaine marche donc
`2 -> 3 -> 4 -> 7` par ses propres demandes, et **traverse**
`CROSSPLAY_WARNING` et `OFFLINE_WARNING` au lieu de les sauter.

**La borne est LUE, pas choisie** : `FUN_1800E56E0` commence par
`if (etat+0x1c != 2 && etat+0x1c != 7) goto SANS_DEMANDE`, donc elle n'ecrase
que dans les sous-etats 2 et 7. Le `5` LEGITIME que `CS_DEMO` (8) pose a
chaque image sans y aller reste intact.

**Controle** : script separe, 1/11 sur la copie d'avant, **11/11** apres --
et deux des controles verifient que l'ANCIENNE substitution a bien **disparu**
(`FournirCsAutoload` absent, `= 7u` absent).

### 31.3 LE VERDICT DE LA SONDE, BORNE A CE QU'ELLE OBSERVE

Le defaut note en 30.3 est corrige : la sonde dit maintenant si
`TaskAutoLoad` **EXISTE**, et son verdict est au conditionnel
(<< si son etape 7 lisait maintenant >>, << ce qui BOUCLERAIT >>). Elle ne
conclut plus sur une sequence qui ne tourne pas.

### 31.4 UNE CORRECTION D'ADRESSE DANS MES PROPRES NOTES

J'ai ecrit partout que la table des modes est a **`0x1803C8240`**. **C'est
faux de 8 octets** : elle est a **`0x1803C8240`**, ce que `vf5fs_host.cpp`
ligne 19036 portait deja (`kTableMode = 0x3C8240`). Mon auto-test de decodage
a echoue dessus, ce qui l'a revele.

La disposition d'une entree, **0x68 octets** :

| offset | contenu |
|---|---|
| `+0x00` | u32 le numero de mode |
| `+0x04` | u32 (non etabli) |
| `+0x08` | phase 0 |
| **`+0x10`** | **phase 1** -- c'est la qu'est `FUN_1800E56E0` pour le mode 0 |
| `+0x18` | phase 2 |
| `+0x20`... | la liste ORDONNEE des sous-etats, terminee par 0 |
| `+0x60` | **non etabli** : vaut `{5, 73}` pour 11 entrees, `{1, 73}`, `{0, 5}` et `{10, 58}` pour les trois autres |

### 31.5 LES 14 MODES ET LEURS CHAINES

Decode depuis le FICHIER du banc, auto-test sur la phase 1 du mode 0 :

| # | mode | phases | la chaine de sous-etats |
|---|---|---|---|
| 0 | **0 STARTUP** | 3 reelles | 0 -> 1 -> 8 -> 5 -> 6 -> 2 -> 3 -> 4 -> 7 -> 73 |
| 1 | 1 | **3 bouchons** `180026620` | 9 -> 10 -> 11 -> 12 -> 73 |
| 2 | **5 MENU** | 3 reelles | **40 -> 73** |
| 3 | 2 | 3 reelles | 19 -> 20 -> 21 -> 22 -> 73 |
| 4 | 3 | 3 reelles | 23 -> 41 -> 21 -> 24 -> 22 -> 73 |
| 5 | 4 | **3 bouchons** | 25 ... 39 -> 73 (15 sous-etats) |
| 6 | 6 | 3 reelles | 41 -> 42 -> 43 -> 44 -> 73 |
| 7 | 7 | 3 reelles | 45 -> 73 |
| 8 | 8 | **3 x `18000BA20`** (= `XOR AL,AL`) | 46 ... 51 -> 73 |
| 9 | 9 | **3 bouchons** | **52 ... 57** -> 73 |
| 10 | 10 | **3 bouchons** | 58 -> 73 |
| 11 | 11 | 3 reelles | 59 -> 60 -> 61 -> 62 -> 73 |
| 12 | 12 | 3 reelles | 63 ... 67 -> 73 |
| 13 | 13 | 3 reelles | 68 ... 72 -> 73 |

**Trois lectures que cette table donne gratuitement :**

1. **Le mode MENU n'a qu'UN sous-etat : `40 = MENU_MAIN`**, puis 73. Donc
   `MENU_MAIN` **est** le repos du mode -- il n'y a rien a atteindre apres
   lui dans ce mode. Ca recoupe [[le-menu-est-atteint-la-boucle-est-un-ecrasement]].
2. **Le mode 9 porte la chaine `52 ... 57`** et ses trois phases sont des
   bouchons -- ce sont les sous-etats `APM3_*` de
   [[la-table-des-scenes-et-ses-bouchons]]. **C'est le mode du jeu en
   reseau, et il est vide.**
3. **Le mode 8 a `18000BA20` pour ses TROIS phases** -- un `return 0` dur.
   Ce mode ne peut donc jamais avancer d'une phase. Quatre autres modes
   (1, 4, 9, 10) ont le bouchon `180026620` (= `return 1`), qui au contraire
   les ferait traverser leur chaine sans rien faire.

### 31.6 CE QUI BLOQUE L'OUVERTURE DU MENU : PLUS RIEN

| etape | etat |
|---|---|
| sortir de `CS_TITLE` | **PAYE** (SS 419.22-23, ENTREE et W) |
| `CS_SIGNIN` (6) | passe, sa phase 2 est le bouchon << oui >> |
| `WARNING` (2) -> `CROSSPLAY_WARNING` (3) | **la demande etait ECRASEE** -- cause otee ici |
| `OFFLINE_WARNING` (4) -> `CS_AUTOLOAD` (7) | non mesure : la substitution les sautait |
| `CS_AUTOLOAD` (7) | **PAYE** : 19 etapes lues, terminus atteint en 2 images |
| le mode 5 et le sous-etat 40 | **ATTEINTS a l'image 881 (l'etat ; aucun ecran mesure)** |

**Ce qui reste INCONNU**, et c'est tout autre chose que << bloque >> : que le
menu **TIENNE** (10 images mesurees seulement), et ce que font ses entrees --
`FUN_18020F1E0` batit tout l'ecran SI `bloc+0x1FF08` est NUL
([[le-menu-a-deux-chemins-comme-le-titre]]), donc avec notre repartiteur pose
le module DELEGUE le menu.

---

## 32. LE POINT SUR LES 73 SOUS-ETATS (SS 419.35)

**Decode depuis le FICHIER du banc. Adresses prises de `vf5fs_host.cpp`
(lignes 19035-19037), pas d'une note :**
`kTableSous = 0x3C87F0` (0x49 x 0x20), `kTableNomsSous = 0x3C9190` (74
pointeurs de chaine), `kTableMode = 0x3C8240`.

Auto-test : l'entree 0 doit porter le numero 0, le nom 5 doit etre `CS_TITLE`
et le nom 40 `MENU_MAIN` -- sinon une des trois tables est decalee et le
releve ne vaut rien.

**Deux bouchons a reconnaitre dans les colonnes de phases :**
`oui` = `0x180026620` = `MOV AL,1 ; RET` (passe tout de suite) ;
**`non` = `0x18000BA20` = `XOR AL,AL ; RET`** (ne passe JAMAIS).

### 32.1 LE RELEVE

| n | nom | mode(s) | phase 0 | phase 1 | phase 2 | code |
|---|---|---|---|---|---|---|
| 0 | DATA_INITIALIZE | 0 | `1800E64E0` | `1800E56B0` | `1800E5B20` | **complet** |
| 1 | SYSTEM_STARTUP | 0 | `1800E6580` | `1800E58A0` | `1800E5BC0` | **complet** |
| 2 | WARNING | 0 | `1800E6660` | `1800E58C0` | `1800E5C00` | **complet** |
| 3 | CROSSPLAY_WARNING | 0 | `1800E5D20` | `1800E54D0` | `1800E59A0` | **complet** |
| 4 | OFFLINE_WARNING | 0 | `1800E64F0` | `1800E56C0` | `1800E5B60` | **complet** |
| 5 | CS_TITLE | 0 | `1800E5ED0` | `1800E55B0` | `1800E5A20` | **complet** |
| 6 | CS_SIGNIN | 0 | `1800E5E50` | `1800E5570` | `oui` | 2/3 |
| 7 | CS_AUTOLOAD | 0 | `1800E5D40` | `1800E54F0` | `1800E59C0` | **complet** |
| 8 | CS_DEMO | 0 | `1800E5D70` | `1800E5510` | `1800E59F0` | **complet** |
| 9 | LOGO | 1 | `oui` | `oui` | `oui` | **VIDE** |
| 10 | RATING | 1 | `oui` | `oui` | `oui` | **VIDE** |
| 11 | DEMO | 1 | `oui` | `oui` | `oui` | **VIDE** |
| 12 | TITLE | 1 | `oui` | `oui` | `oui` | **VIDE** |
| 13 | TITLE_TV | **aucun** | `oui` | `oui` | `oui` | **VIDE** |
| 14 | LOGO_TV | **aucun** | `oui` | `oui` | `oui` | **VIDE** |
| 15 | LOGO_TERMINAL | **aucun** | `oui` | `oui` | `oui` | **VIDE** |
| 16 | MANUAL_TERMINAL | **aucun** | `oui` | `oui` | `oui` | **VIDE** |
| 17 | TITLE_TERMINAL | **aucun** | `oui` | `oui` | `oui` | **VIDE** |
| 18 | LOOP_TERMINAL | **aucun** | `oui` | `oui` | `oui` | **VIDE** |
| 19 | SELECTOR | 2 | `1800E3F90` | `1800E2470` | `1800E2F60` | **complet** |
| 20 | MODE_SELECTOR | 2 | `1800E3F70` | `1800E2010` | `1800E2F40` | **complet** |
| 21 | VS | 2,3 | `1800E3D70` | `1800E1C20` | `1800E2CE0` | **complet** |
| 22 | GAMEOVER | 2,3 | `1800E3D40` | `1800E1BC0` | `1800E2B70` | **complet** |
| 23 | WORLD_STAGE_MAIN | 3 | `18000B830` | `18000B3D0` | `18000B4F0` | **complet** |
| 24 | WORLD_STAGE_TOURNAMENT | 3 | `18000B860` | `18000B3D0` | `18000B510` | **complet** |
| 25 | DATA_TEST_MAIN | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 26 | DATA_TEST_MISC | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 27 | DATA_TEST_OBJ | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 28 | DATA_TEST_STG | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 29 | DATA_TEST_MOT | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 30 | DATA_TEST_COLLISION | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 31 | DATA_TEST_SPR | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 32 | DATA_TEST_AET | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 33 | DATA_TEST_AUTH_3D | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 34 | DATA_TEST_CHR | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 35 | DATA_TEST_ITEM | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 36 | DATA_TEST_PERF | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 37 | DATA_TEST_TNMT | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 38 | DATA_TEST_BATTLE | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 39 | DATA_TEST_KOTSP_SS | 4 | `oui` | `oui` | `oui` | **VIDE** |
| 40 | MENU_MAIN | 5 | `1800E4210` | `non` | `1800E4130` | 2/3 |
| 41 | CS_TERM_CUSTOMIZE | 3,6 | `180211F90` | `180211A80` | `180211E90` | **complet** |
| 42 | CS_TERM_REPLAY_PLAY | 6 | `180212020` | `180211D10` | `oui` | 2/3 |
| 43 | CS_TERM_LAST_PLAY | 6 | `180211FD0` | `180211B20` | `180211EB0` | **complet** |
| 44 | CS_TERM_CLIP_PLAY | 6 | `180211F80` | `1802119C0` | `180211E40` | **complet** |
| 45 | CS_TRAINING | 7 | `180212140` | `180212070` | `1802120D0` | **complet** |
| 46 | ONLINE_STARTUP | 8 | `non` | `non` | `non` | **VIDE** |
| 47 | ONLINE_SELECTOR | 8 | `non` | `non` | `non` | **VIDE** |
| 48 | ONLINE_MENU | 8 | `non` | `non` | `non` | **VIDE** |
| 49 | ONLINE_MATCHING | 8 | `non` | `non` | `non` | **VIDE** |
| 50 | ONLINE_GAME | 8 | `non` | `non` | `non` | **VIDE** |
| 51 | ONLINE_OVER | 8 | `non` | `non` | `non` | **VIDE** |
| 52 | APM3_ENTRY | 9 | `oui` | `oui` | `oui` | **VIDE** |
| 53 | APM3_SELECTOR | 9 | `oui` | `oui` | `oui` | **VIDE** |
| 54 | APM3_GAME_VS | 9 | `oui` | `oui` | `oui` | **VIDE** |
| 55 | APM3_GAMEOVER | 9 | `oui` | `oui` | `oui` | **VIDE** |
| 56 | APM3_TRAINING | 9 | `oui` | `oui` | `oui` | **VIDE** |
| 57 | APM3_ONLINE_VS | 9 | `oui` | `oui` | `oui` | **VIDE** |
| 58 | APM3_TESTMODE_MAIN | 10 | `oui` | `oui` | `oui` | **VIDE** |
| 59 | RANK_MATCH_STARTUP | 11 | `180218720` | `180213F70` | `180215780` | **complet** |
| 60 | RANK_MATCH_MATCHING | 11 | `1802183C0` | `1802135D0` | `1802156A0` | **complet** |
| 61 | RANK_MATCH_GAME | 11 | `180218230` | `180213170` | `1802155D0` | **complet** |
| 62 | RANK_MATCH_OVER | 11 | `1802184A0` | `180213CF0` | `1802156F0` | **complet** |
| 63 | ROOM_MATCH_STARTUP | 12 | `180218720` | `180214A80` | `180215D90` | **complet** |
| 64 | ROOM_MATCH_MENU | 12 | `180218C80` | `180214760` | `oui` | 2/3 |
| 65 | ROOM_MATCH_MATCHING | 12 | `180218BA0` | `1802145F0` | `180215AC0` | **complet** |
| 66 | ROOM_MATCH_GAME | 12 | `180218980` | `1802140E0` | `180215970` | **complet** |
| 67 | ROOM_MATCH_OVER | 12 | `180218CD0` | `180214A20` | `180215B00` | **complet** |
| 68 | TOURNAMENT_STARTUP | 13 | `180218720` | `180215380` | `180215D90` | **complet** |
| 69 | TOURNAMENT_MENU | 13 | `180219230` | `1802151D0` | `oui` | 2/3 |
| 70 | TOURNAMENT_MATCHING | 13 | `180219150` | `1802150B0` | `1802160B0` | **complet** |
| 71 | TOURNAMENT_GAME | 13 | `180218F30` | `180214BE0` | `180215F80` | **complet** |
| 72 | TOURNAMENT_OVER | 13 | `180219280` | `180215320` | `1802160E0` | **complet** |

**complets : 30   partiels : 5   VIDES : 38   total : 73**

### 32.2 CE QUE LE RELEVE DIT

**1. `MENU_MAIN` est le SEUL sous-etat hors du bloc en ligne a porter un zero
dur.** Sept sous-etats ont au moins une phase a `18000BA20` : **40** et les
six du mode 8 (`46` a `51`, `ONLINE_*`). Compte mecanique, pas a l'oeil.

Et ses trois phases, verifiees sur les octets bruts de l'entree 40
(`0x1803C8CF0` : numero `0x28`, puis `1800E4210` / **`18000BA20`** /
`1800E4130`) :

| phase | adresse | ce qu'elle fait |
|---|---|---|
| 0 | `1800E4210` | `FUN_1802CD400(DAT_18079B160, "MAIN MENU")` -- **cree la tache du menu** |
| **1** | **`18000BA20`** | **`XOR AL,AL ; RET` -- rend 0 POUR TOUJOURS** |
| 2 | `1800E4130` | `FUN_180206B90()` -- la destruction |

Dans la machine a trois phases, la phase 1 doit rendre non nul pour que la
scene se termine. Donc **on ne peut JAMAIS sortir de `MENU_MAIN` par sa propre
machine.** Comparaison qui tranche : `CS_TITLE` phase 1 est du vrai code
(`1800E55B0`) et rend non nul quand START est presse. Le menu, lui, n'a pas
d'issue.

**2. Le bloc en ligne est condamne, pas seulement vide.** Les six `ONLINE_*`
ont `18000BA20` aux TROIS phases : le mode 8 ne peut pas avancer d'un cran.
C'est different du mode 9 (`APM3_*`, 52-57) qui a `180026620` partout et
traverserait sa chaine instantanement sans rien faire.

**3. Six sous-etats n'appartiennent a AUCUN mode** : `13 TITLE_TV`,
`14 LOGO_TV`, `15 LOGO_TERMINAL`, `16 MANUAL_TERMINAL`, `17 TITLE_TERMINAL`,
`18 LOOP_TERMINAL`. Aucune chaine de la table des modes ne les liste, donc ils
sont **inatteignables** par le repartiteur. Ce sont les ecrans de borne.

**4. LE CHEMIN DU COMBAT EST COMPLET.** `19 SELECTOR`, `20 MODE_SELECTOR`,
`21 VS`, `22 GAMEOVER` (mode 2), `23`/`24 WORLD_STAGE_*` (mode 3),
`45 CS_TRAINING` (mode 7) et tout le bloc `59` a `72` (classe, salon,
tournoi) ont leurs **trois phases en vrai code**. Rien n'y est bouchonne.

**5. La chaine console est complete a une phase pres** : `0` a `8` sont
complets sauf `6 CS_SIGNIN`, dont la phase 2 est `oui`.

### 32.3 DONC : CE QUI BLOQUE, EN TROIS MURS DISTINCTS

| mur | etat |
|---|---|
| **atteindre l'etat `MENU_MAIN`** | **PLUS RIEN** -- fait a l'image 881 (l'etat seul) |
| **que le menu PARAISSE** | **nous** : `FUN_18020F1E0` ne batit l'interface que si `bloc+0x1FF08` est NUL ; notre repartiteur etant pose, le module **DELEGUE** ([[le-menu-a-deux-chemins-comme-le-titre]]) |
| **SORTIR du menu vers le combat** | **`MENU_MAIN` phase 1 = `XOR AL,AL ; RET`** -- il n'y a pas d'issue dans le binaire livre |

**Le troisieme mur est le vrai, et il est nouveau.** Les deux premiers etaient
connus ; celui-la explique pourquoi atteindre le menu ne suffira jamais a
lancer un combat, alors que tout le chemin du combat (point 4) est intact
derriere.

---

## 33. << MENU_MAIN N'A PAS D'ISSUE >> EST FAUX (SS 419.37)

**L'utilisateur m'a demande si j'avais menti sur la decompilation de la phase
MENU. Je n'ai pas menti : elle etait decompilee. J'ai fait pire -- j'ai
affirme le contraire de ce que mes propres fichiers disent, sans les ouvrir.**

Les deux sources, toutes deux anterieures a cette seance :
* `VF5RE/code_decompile/FUN_18020f1e0.c`, videe le **7 nov 2026** ;
* `vf5fs_host.cpp` `case 80` (ligne 18655) et le bloc `g_menuEtat`
  (ligne 7755) : plus de 100 lignes de lecture, SS **314 / 321 / 326 / 328 /
  331 / 333**.

### 33.1 CE QUE J'AI AFFIRME A TORT A LA SECTION 32

| affirmation (section 32) | etat |
|---|---|
| << `MENU_MAIN` n'a pas d'issue : sa phase 1 est `XOR AL,AL` >> | **FAUSSE**. La phase 1 d'un **sous-etat** ne gouverne pas la sortie ; c'est la **tache** qui demande le mode suivant. |
| << le module DELEGUE le dessin du menu >> | **JUSTE, et ce fichier le disait deja** (section << Le sous-etat 40 a DEUX chemins >>, SS 419) : avec notre repartiteur, l'init prend le chemin (B), qui ne charge ni `bg_base` ni les cinq sous-menus. **Deux retouches** : le chemin (B) joue quand meme une musique (`vfes_bgm_mnu.adx`, la ou (A) joue `vf5b_tkv.adx`), et la mesure du SS 331 que j'ai citee ici -- 145 tirages/image avec l'etat 10 contre 5719 sans -- porte sur la POSE DE L'ETAT, pas sur les deux chemins. Ne pas les confondre. |

### 33.2 LA SORTIE DU MENU : HUIT SITES, MESURES

Balayage capstone des **58** appels a `FUN_1800E1B00` (demander un MODE),
croise avec les bornes de `FUN_1802079E0` (la mise a jour du menu) lues dans
`vf5fs_host.cpp` ligne 7811. Auto-test : les bornes doivent EXCLURE un site
connu hors menu (`VF5FS+0xE59DA`) -- il passe.

| site | mode demande |
|---|---|
| `VF5FS+0x208231` | 11 RANK_MATCH |
| `VF5FS+0x2082B0` | 12 ROOM_MATCH |
| `VF5FS+0x208309` | 13 TOURNAMENT |
| `VF5FS+0x2087A4` | 6 CS_TERM |
| `VF5FS+0x2088AD` | 6 CS_TERM |
| `VF5FS+0x208927` | **3 WORLD_STAGE** |
| `VF5FS+0x208A4C` | 0 STARTUP |
| `VF5FS+0x208C88` | 0 STARTUP |

Sur les 58 sites : **21 demandent le mode 5 = MENU**, 11 le mode 0, 6 le
mode 6, et 12 restent indetermines (`ECX` non immediat). Repartition
complete : mode 0 x11, 2 x1, 3 x1, **5 x21**, 6 x6, 7 x1, 8 x1, 11 x1,
12 x2, 13 x1.

### 33.3 LE VRAI MUR, ET IL EST A NOUS

`FUN_18020F1E0`, avec notre repartiteur pose, prend le chemin **riche** : 12
abonnements d'evenements, commande **216**, commande **188**,
`bloc+0x28C4 = 0x1311`, la musique `vfes_bgm_mnu.adx`, puis en **derniere
instruction** la commande **80** avec `&bloc+0x28C4`.

`+0x28C4` n'est pas un etat que le module calcule : **c'est un canal de
SORTIE de l'hote.** Recherche du scalaire `0x28c4` sur les 12 347 fonctions :
six sites, **un seul MOV** (`18020f546`, la valeur `0x1311` = 17). Les deux
aiguillages couvrent `0..0xE` puis `0..0x10` : **17 est un cran au-dela des
deux**, donc `default` a chaque image.

| ce qui manque | etat |
|---|---|
| poser `args[0]` de la commande 80 | `g_menuEtat = -1` par defaut : **on n'ecrit rien**. `VF5_MENU_ETAT=0..0x10` ; seuls 10, 11, 13 ne tuent pas la tache. |
| **servir la commande 188 (0xBC)** | **ZERO `case`** -- compte mecanique dans `vf5fs_host.cpp` |
| **servir la commande 213 (0xD5)** | **ZERO `case`** |
| **servir la commande 216 (0xD8)** | **ZERO `case`** |

Le cas 0 du menu envoie la 188 avec `args[0]=2` ; le cas 1 la 213 puis la 188
avec 3. Aucune n'est servie : elles tombent au `default`, qui journalise et
n'ecrit rien dans `args`.

**ET LE MUR DE LA CHAINE, LUI, EST AILLEURS ET DEJA ECRIT** : sections 26.4 et 27. A l'image `WARNING`, `FUN_1800E56E0` devrait demander **7 = CS_AUTOLOAD** -- le suivant de la liste `00 01 08 05 06 02 03 04 07 49` -- et il demande **5 = CS_TITLE**, parce que son predicat `FUN_18000BA20` est `XOR AL,AL ; RET` dans le binaire livre. Et c'est la phase 2 de `CS_AUTOLOAD` qui demande mode MENU + sous-etat 73. **Il n'y a pas cinq ecrans a sauter : il y a UNE transition a fournir.**

**Donc la chaine `CS_TITLE -> MENU` n'est pas cassee. Le menu est atteint,
son init reussit, sa mise a jour tourne -- et elle reste au `default` pour
toujours parce que l'hote ne lui dit jamais quelle entree est choisie, et ne
repond pas aux trois questions qu'elle pose ensuite.**

---

## 32. LA CAUSE OTEE POUR DE VRAI : SIX OCTETS A NOP (SS 419.61)

**Posee, compilee, et DEUX COURSES ONT TOURNE.**

La section 30.5 nommait la variante fidele : *<< empecher `FUN_1800E56E0`
d'ecraser la demande de la scene >>*. C'est fait, et pas par une destination
fournie : par une branche du module remise en service.

### 32.1 LE SITE, LU AU DESASSEMBLEUR

`FUN_1800E56E0`, chemin B (`FUN_1801CF090` nul, `FUN_1801CEF40` non nul) :

```
1800e57f2  E82962F2FF    CALL 0x18000ba20     ; le bouchon de SEGA
1800e57f7  84C0          TEST AL, AL
1800e57f9  0F8412FFFFFF  JZ   0x1800e5711     ; -> MOV ECX,5 ; CALL FUN_1800E1B20
1800e57ff  E83CC1FFFF    CALL 0x1800e1940
1800e5804  83781C02      CMP  [RAX+0x1c], 2   ; sous-etat == 2 (WARNING) ?
1800e5808  0F850DFFFFFF  JNZ  0x1800e571b     ; non (donc 7) -> RIEN
1800e580e  B907000000    MOV  ECX, 7
1800e5813  E9FEFEFFFF    JMP  0x1800e5716     ; demande 7 = CS_AUTOLOAD
```

et le predicat :

```
18000ba20  32C0  XOR AL, AL
18000ba22  C3    RET
```

**Les deux branches saines sont DERRIERE le `JZ`** : au sous-etat 2 elle
demande 7 elle-meme, au sous-etat 7 elle ne fait RIEN. Le bouchon les rendait
inatteignables.

### 32.2 POURQUOI PAS `FUN_18000BA20`

La section 31.1 proposait `31 C0` -> `B0 01` sur le predicat. **A ne pas
faire** : `FUN_18000BA20` a **plus de 60 sites d'appel** (releve de references
croisees). Le site qui le CONSOMME est unique. On met donc a NOP les six
octets du `JZ`, a `VF5FS+0xE57F9`, apres controle de `0F 84 12 FF FF FF` --
tout ou rien, `FlushInstructionCache`, image chargee seulement. C'est la
technique de YAMP (`Memory::Nop`, ses correctifs << Reinstate ... >>).

### 32.3 LE MECANISME COMPLET DU MEURTRE, MESURE

Le pompeur `FUN_1800E1600` :

```
1800e1793  CMP byte [0x18075141c], BL   ; mo+0x2C (arme) == 0 ?
1800e1799  JNZ 0x1800e17a3
1800e17a3  MOV ECX, 2                   ; ARME -> LA PHASE EST FORCEE A 2
1800e17a8  MOV [0x180751418], ECX       ; et ecrite dans mo+0x28
```

Donc `FUN_1800E1B20(5)` au sous-etat 7 ne demande pas seulement une scene :
il **arme**, l'armement force la phase du sous-etat a **2**, et la phase 2 de
CS_AUTOLOAD (`FUN_1800E59C0`) appelle `FUN_1802CCB60` -- elle TUE
`TaskAutoLoad`. Le chargement mourait a l'etape **2 sur 19**.

### 32.4 CE QUE LA COURSE DONNE

| acquis | degre |
|---|---|
| `[419.61]` ecrit : le controle des six octets passe | **CONFIRME** |
| `TaskAutoLoad` atteint l'etape **7/19** au lieu de 2/19 | **CONFIRME** |
| 3000 images, 36459 tirages, 3010 Clear, 0 echec de Present, **0 faute du module** | **CONFIRME** |
| `MENU_MAIN` atteint et TENU jusqu'a la fin (~2450 images) | **CONFIRME** |
| 16 taches vivantes, dont `[MAIN MENU]`, `[WORLD_STAGE_MANAGER]`, `[REPLAY_MANAGER]`, `[ROB LOAD]` | **CONFIRME** |
| **un menu PARAIT a l'ecran** | **REFUTE -- l'utilisateur voit l'ECRAN DE CHARGEMENT** |

### 32.5 L'ETAPE 7 N'EST PAS UN MUR : ELLE EST LA SORTIE NORMALE

`[7].etape 7` = `FUN_1800E45E0` :

```c
if (FUN_1801cf0c0()) {                       // = !vivante(DAT_1807969A0)
    if (FUN_1801d0300(&r)) { tache->[0x5c] = 0x12; return; }   // 18
    tache->[0x5c] = (r == 1) ? 4 : 2;
}
```

avec `FUN_1801D0300(out)` = `{ *out = [+0x11088]; return [+0x11085]; }`.

Or la section 30.2 a **CONFIRME** que `+0x11085` vaut **1 des l'image 876**.
Donc l'etape 7 lit 1, part en **etape 18**, qui pose `+0x58 = 1` : la tache
meurt **d'elle-meme**, legitimement, et la phase 2 passe au menu. Les 19
etapes ne sont PAS toutes parcourues, et elles n'ont pas a l'etre.

**Donc le correctif 419.61 a fait exactement son travail** : la tache
n'est plus assassinee a l'etape 2, elle finit par sa propre etape 18.
L'ecran de chargement n'a **jamais** ete un probleme de chargement.

### 32.6 CE QUI RESTE, ET CE QUI N'EST PAS MESURE

`[WAIT_SCREEN]` -- la tache de l'ecran d'attente -- est **encore vivante** a
l'image 632, a cote de `[MAIN MENU]`. C'est elle qui est a l'ecran.

Et la phase 1 de `MENU_MAIN` est `VF5FS+0xBA20`, un bouchon `return 0` : le
sous-etat y reste **par construction**. Ce n'est pas un blocage, c'est son
etat de repos.

| a trancher | degre |
|---|---|
| `+0x28C4` (l'etat du menu) vaut 17 = ATTENTE dans CETTE course | **NON MESURE -- la sonde etait eteinte** |
| le chemin A de `FUN_1800E56E0` (`FUN_1801CF090`) tire-t-il ? | **NON MESURE -- laisse intact a dessein** |

Les fiches qui portent la suite : [[l-ecran-d-attente-du-menu]] (`+0x28C4`
vaut 17 et le `switch` remontre l'attente a chaque image),
[[l-etat-du-menu-est-une-sortie-de-l-hote]] (le module n'ecrit JAMAIS que 17 ;
l'etat est **notre** sortie) et [[le-menu-attend-dix-sept-etats-de-l-hote]]
(les commandes **188, 213, 216** n'ont aucun gestionnaire).

Journaux : `host_log_s419_61_nop.txt` (3000 images, complete),
`host_log_s419_61_faute.txt` (1680 images, fermee par l'utilisateur -- le
code `-1073741819` vient de la fermeture, PAS d'une faute).
