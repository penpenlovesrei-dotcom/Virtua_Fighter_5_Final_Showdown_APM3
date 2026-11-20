# Le repartiteur de scenes de REVO, et ou brancher le mode APM3

Mesure du 6 novembre 2026, sur
`FS REVO/vf5fs-pxd-w64-d3d12_SteamRetail.dll` (7 229 952 o, celui qu'on
execute) et `FS APM3/banc/vf5fs-pxd-w64-Retail_APM3.dll` (6 965 248 o).

Chemin suivi, sans aucun offset recopie a la main : `VF5FS+0xe2470` est le
gestionnaire de `SELECTOR` (deja etabli) -> `xrefs` rend `0x1803C8A60`, dans
`.rdata` -> la table des sous-etats -> `xrefs` sur sa base rend six sites dans
trois fonctions -> la plus grosse, **`VF5FS+0xe1600` (657 octets)**, est le
repartiteur. Il a ete decompile ; tout ce qui suit en sort.

## 1. LE REPARTITEUR : `VF5FS+0xe1600`

Appele chaque image. Il fait deux fois la meme chose, d'abord pour le MODE,
puis pour le SOUS-ETAT :

```c
// --- le MODE ---
off = 0;  i = 0;
while (*(int*)(0x1803C8240 + off) != mode_courant) {   // RECHERCHE PAR NUMERO
    i++;  off += 0x68;
    if (0x5af < off) { compteur++; return; }           // 0x5af -> 14 entrees
}
f = ((void**)0x1803C8248)[i*0xd + phase_mode];         // 0xd qwords = 0x68 o
if (f) avance = f();

// --- le SOUS-ETAT ---
p = (int*)0x1803C87F0;  j = 0;
do {
    if (*p == sousetat_courant) {                      // RECHERCHE PAR NUMERO
        if (phase_sousetat == 3) avance = 1;
        else {
            f = ((void**)0x1803C87F8)[j*4 + phase_sousetat];  // 4 qw = 0x20 o
            avance = (f == 0) || f();
        }
        ...
    }
    j++;  p += 8;                                      // 8 int = 0x20 o
} while (j < 0x49);                                    // 0x49 -> 73 entrees
```

**POINT CAPITAL : les deux tables sont parcourues en CHERCHANT le numero, pas
indexees par lui.** Le numero est a `+0x00` de l'entree, et il ne coincide pas
toujours avec la position (voir la table des modes plus bas). Un code qui
indexerait par le numero taperait a cote.

## 2. LES VARIABLES D'ETAT

```
0x1807513F0   mode courant            (cherche dans la table des modes)
0x1807513F4   mode demande
0x1807513FC   phase du mode           0, 1, 2
0x18075140C   sous-etat courant       (cherche dans la table des sous-etats)
0x180751410   sous-etat demande       0x49 = 73 = MAX = « aucun »
0x180751418   phase du sous-etat      0, 1, 2 ; 3 = fini (pas d'appel)
0x180751400   drapeau « mode en cours »
0x180751401   drapeau « mode fini »
0x18075141C   drapeau « mode engage »
0x18075141D   drapeau « transition demandee »
0x180751404   compteur d'images du repartiteur
0x180751420   compteur de passages sur le sous-etat
```

Et la fonction de demande de transition :

```
VF5FS+0xe1960 (mode, sous_etat)   <- c'est par la qu'on CHANGE de scene
```

Le veto deja connu, `FUN_1802cca60()`, est consulte en tete : s'il rend vrai,
le repartiteur sort sans rien faire. Et `0xe` (= 14 = mode `MAX`) est le mode
demande quand il n'y a plus rien a faire.

## 3. LA TABLE DES MODES

Entree de **0x68 = 104 octets** : `{ u32 numero, 4 o, 12 pointeurs }`. Seuls
les **3 premiers pointeurs** (phases 0, 1, 2) sont lus par le repartiteur ;
les 9 autres ne sont pas mesures.

La table des modes est **immediatement suivie** par celle des sous-etats :
`0x1803C8240 + 14*0x68 = 0x1803C87F0`. C'est ce qui donne sa base sans
supposition.

> **CORRECTION DU 6 NOVEMBRE 2026.** La premiere version de ces deux
> tables etiquetait chaque entree par sa POSITION. C'est faux : la table se
> lit **par le NUMERO a +0x00**, et les deux ne coincident pas aux positions
> 2 a 5. J'avais donc annonce `MENU` bouchonne : c'est `DATA_TEST`.
> Les tables ci-dessous sont etiquetees par le numero.
> Bouchonnes dans REVO : **ADVERTISE (1), DATA_TEST (4), APM3 (9), APM3_TESTMODE (10)**.
> Bouchonnes dans APM3 : **ADVERTISE (1), DATA_TEST (3), ONLINE (7)**.
> (Les entrees `APM3` et `APM3_TESTMODE` sont aux positions 9 et 10, ou
> position = numero : les 27 adresses du paragraphe 4 restent justes.)

### REVO -- 14 entrees, VA 0x1803C8240

```
pos num mode             entree        phase0       phase1       phase2       etat
0   0   STARTUP          0x1803C8240   0x1800E6510  0x1800E56E0  0x1800E5B80  reel
1   1   ADVERTISE        0x1803C82A8   0x180026620  0x180026620  0x180026620  BOUCHON
2   5   MENU             0x1803C8310   0x1800E4140  0x1800E4080  0x1800E40C0  reel   <- pos != num
3   2   GAME             0x1803C8378   0x1800E3CA0  0x1800E1B30  0x1800E2AB0  reel   <- pos != num
4   3   WORLD_STAGE      0x1803C83E0   0x18000B530  0x18000B310  0x18000B3F0  reel   <- pos != num
5   4   DATA_TEST        0x1803C8448   0x180026620  0x180026620  0x180026620  BOUCHON   <- pos != num
6   6   CS_TERM          0x1803C84B0   0x180211EF0  0x180211960  0x180211D50  reel
7   7   CS_TRAINING      0x1803C8518   0x1802120F0  0x180211960  0x180212090  reel
8   8   ONLINE           0x1803C8580   0x18000BA20  0x18000BA20  0x18000BA20  reel
9   9   APM3             0x1803C85E8   0x180026620  0x180026620  0x180026620  BOUCHON
10  10  APM3_TESTMODE    0x1803C8650   0x180026620  0x180026620  0x180026620  BOUCHON
11  11  RANK_MATCH       0x1803C86B8   0x1802180A0  0x1802130A0  0x1802154D0  reel
12  12  ROOM_MATCH       0x1803C8720   0x180218730  0x1802130A0  0x1802157B0  reel
13  13  TOURNAMENT       0x1803C8788   0x180218D00  0x1802130A0  0x180215DC0  reel
```

### APM3 -- 10 entrees, VA 0x1803A0190

```
pos num mode             entree        phase0       phase1       phase2       etat
0   0   STARTUP          0x1803A0190   0x1800DE3D0  0x1800DD700  0x1800DDA40  reel
1   1   ADVERTISE        0x1803A01F8   0x180029FB0  0x180029FB0  0x180029FB0  BOUCHON
2   4   MENU             0x1803A0260   0x1800DCBF0  0x180007450  0x1800DCB80  reel   <- pos != num
3   2   GAME             0x1803A02C8   0x1800DC7D0  0x1800DA9D0  0x1800DB890  reel   <- pos != num
4   3   DATA_TEST        0x1803A0330   0x180029FB0  0x180029FB0  0x180029FB0  BOUCHON   <- pos != num
5   5   CS_TERM          0x1803A0398   0x1801E5010  0x1801E4E60  0x1801E4F60  reel
6   6   CS_TRAINING      0x1803A0400   0x1801E5170  0x1801E4E60  0x1801E5110  reel
7   7   ONLINE           0x1803A0468   0x180029FB0  0x180029FB0  0x180029FB0  BOUCHON
8   8   APM3             0x1803A04D0   0x18023DC30  0x180007450  0x18023C2A0  reel
9   9   APM3_TESTMODE    0x1803A0538   0x180029FB0  0x180007450  0x180029FB0  reel
```

**LE RESULTAT : dans REVO, `APM3` (numero 9) et `APM3_TESTMODE` (numero 10)
ont une entree, avec le bon numero, et leurs 6 pointeurs valent tous le
bouchon `0x180026620`.** Dans APM3 les memes entrees sont reelles.

Donc la recherche par numero **trouvera** l'entree : le mode est atteignable
en structure. Il manque le code, pas l'emplacement.

## 4. LES 27 POINTEURS A ECRIRE

```
  MODE (table 0x1803C8240, pas 0x68, les 3 phases a +0x08)
    APM3                num 9    entree 0x1803C85E8   phases a 0x1803C85F0
    APM3_TESTMODE       num 10   entree 0x1803C8650   phases a 0x1803C8658

  SOUS-ETATS (table 0x1803C87F0, pas 0x20, les 3 phases a +0x08)
    APM3_ENTRY          num 52   entree 0x1803C8E70   phases a 0x1803C8E78
    APM3_SELECTOR       num 53   entree 0x1803C8E90   phases a 0x1803C8E98
    APM3_GAME_VS        num 54   entree 0x1803C8EB0   phases a 0x1803C8EB8
    APM3_GAMEOVER       num 55   entree 0x1803C8ED0   phases a 0x1803C8ED8
    APM3_TRAINING       num 56   entree 0x1803C8EF0   phases a 0x1803C8EF8
    APM3_ONLINE_VS      num 57   entree 0x1803C8F10   phases a 0x1803C8F18
    APM3_TESTMODE_MAIN  num 58   entree 0x1803C8F30   phases a 0x1803C8F38
```

Soit **27 pointeurs** : 2 modes x 3 phases + 7 sous-etats x 3 phases. Tout est
dans `.rdata`, donc `VirtualProtect` avant d'ecrire.

## 5. L'ORACLE : LES MEMES ENTREES DANS APM3

```
  MODE (table 0x1803A0190 d'APM3)
    APM3                num 8    0x18023DC30  0x180007450  0x18023C2A0
    APM3_TESTMODE       num 9    0x180029FB0  0x180007450  0x180029FB0

  SOUS-ETATS (table 0x1803A05A0 d'APM3)
    APM3_ENTRY          num 48   0x18023DDA0  0x18023A320  0x18023C380
    APM3_SELECTOR       num 49   0x18023E120  0x18023B5E0  0x1800DBB70
    APM3_GAME_VS        num 50   0x18023DE30  0x18023A5D0  0x18023C3F0
    APM3_GAMEOVER       num 51   0x18023DDC0  0x18023A530  0x18023C390
    APM3_TRAINING       num 52   0x18023E180  0x18023B8F0  0x18023C770
    APM3_ONLINE_VS      num 53   0x18023DF10  0x18023AD10  0x18023C4B0
    APM3_TESTMODE_MAIN  num 54   0x180241D80  0x180007450  0x180241D60
```

## 6. ETABLI / NON ETABLI

CONFIRME, et verifie contre le code decompile et non seulement contre un
motif : le repartiteur et son fonctionnement ; la recherche par numero ; les
deux tables, leurs bases, leurs pas et leurs longueurs (0x5af -> 14 entrees de
0x68 ; 0x49 -> 73 entrees de 0x20) ; les trois phases ; que phase 3 d'un
sous-etat ne rappelle rien ; les douze variables d'etat ; que `APM3` et
`APM3_TESTMODE` sont bouchonnes dans REVO et reels dans APM3.

NON MESURE :
1. Les **9 pointeurs restants** de chaque entree de mode (104 octets pour 3
   phases utilisees).
2. Le **drapeau a +0x04** des entrees de sous-etat (0 ou 1).
3. **Qui appelle `VF5FS+0xe1960`** pour demander le mode APM3. Dans REVO ce
   code est parti ; c'est a l'hote de faire la demande.
4. Les **27 fonctions d'APM3**, a lire une par une.
