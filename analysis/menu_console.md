# Le menu console : ce qu'on a recupere, et ce qui manque encore

Chantier ouvert le 2026-09-03. **Les donnees sont recuperees et le moteur les
lit. Le menu reste vide** -- pour une raison desormais precise.

---

## 1. Les donnees : recuperees, et au bon format

Elles n'etaient ni dans le dump APM3, ni exploitables cote Xbox 360. Elles sont
dans le **PS3**, en clair.

### La Xbox 360 est une impasse

`tools/stfs.py` (ecrit d'apres la specification Free60, aucun outil tiers
execute) lit les 2370 entrees du paquet. Valide : `ArcadeInfo.xml` ressort
intact, BOM UTF-16 compris.

Mais **chaque fichier de jeu y est enferme dans un conteneur supplementaire** :

```
magie 0F F5 12 ED, version 1, entropie du corps 7,99 bits/octet
chritm_tbl.farc : 879 800 o cote X360 contre 1 894 508 o cote APM3
bone_data.bin   :  21 658 o contre 150 480 o
```

Compresse, donc, et son decompresseur vit dans le `default.xex` -- **chiffre AES
et compresse LZX**. Hors d'atteinte sans ecrire un decodeur LZX.

### Le PS3 est en clair

`mot_DUR.farc` y commence par `FArC` tout simplement. Les planches vivent dans
`USRDIR/rom.psarc`, 63 Mo, ouvert par `tools/psarc.py` (PSARC 1.4, zlib, 326
entrees, blocs de 64 Ko).

### Et le format est le meme -- pas de gros-boutisme

C'est la crainte qui tombe :

```
PS3  aet_c_mchdur.bin : D0 0A 00 00 D0 15 00 00 ...
APM3 aet_c_mchdur.bin : D0 0A 00 00 D0 15 00 00 ...
```

Memes octets, meme taille (6704). Le format AET est petit-boutiste des deux
cotes. Aucune conversion necessaire.

### Vingt fichiers poses

Neuf planches `aet_n_*` du PSARC, onze archives `spr_n_*` du PKG (dont la police
`fnt32` et un `cmnps3` propre a la PS3), dans `vf5fs_media/rom/2d/`.

**Surprise** : leurs noms etaient **deja dans le `.par`** du runtime -- l'archive
les declare, apparemment sans donnees. Il a fallu masquer les vingt entrees
(`tools/par_masquer.py`) pour que le moteur retombe sur nos fichiers.

Mesure de confirmation, au point d'arret sur `CreateFileW` :

```
2 x  vf5fs_media/rom/2d/aet_n_adv.bin
2 x  vf5fs_media/rom/2d/aet_n_cmn.bin
2 x  vf5fs_media/rom/2d/spr_n_adv.farc
2 x  vf5fs_media/rom/2d/spr_n_cmn.farc
2 x  vf5fs_media/rom/2d/spr_n_fnt32.farc
```

Deux ouvertures chacun, **aucun reessai** : ils se chargent.

---

## 2. La planche est la bonne

`aet_n_main.bin` (119 440 o) contient exactement la scene que le code reclame :

```
p_menutxt_PS3_lt          <- la chaine referencee en 0x1801E0E7B
p_menutxt_01_lt   p_menutxt_02_rb
N_MAIN_PLA_MENU_HI20   N_MAIN_PLA_MENU_SDW50   menu_pla
```

Confiance : **CONFIRMED**.

---

## 3. Ce qui manque : le moteur ne DEMANDE pas la planche

Le traceur est formel : sur cinq fichiers `*_n_*` ouverts, **`aet_n_main` et
`spr_n_main` n'en font pas partie**. Le moteur charge `adv`, `cmn` et `fnt32` --
ce dont le parcours borne a besoin -- et jamais le menu.

Le moteur les connait pourtant tous. Il tient un **registre d'actifs** en
`.rdata`, une suite de couples `{nom, longueur}` :

```
0x18054D650  -> "2d/spr_n_adv"       (0x1E)
0x18054D680  -> "2d/spr_n_cmn"       (0x1E)
0x18054D6B0  -> "2d/spr_n_fnt32"     (0x20)
0x18054D6D0  -> "2d/spr_n_main"      (0x1F)   <- present, jamais demande
0x18054D6F0  -> "2d/spr_n_term"      (0x1F)
```

**Le build arcade a garde le code qui DESSINE le menu, mais pas celui qui
CHARGE ses ressources.** C'est cohérent avec tout le reste : les chaines
`ARCADE MENU`, `VERSUS MENU` ont bien deux references de code chacune, mais rien
ne va chercher la planche qui les contient.

## 4. La prochaine mesure

Trouver **l'identifiant** de `2d/spr_n_main` dans ce registre (son index), puis
qui demande un actif par identifiant. Deux voies :

1. remonter du registre vers son consommateur -- la fonction qui prend un indice
   et rend un actif ;
2. instrumenter le chargement d'un actif qui MARCHE (`spr_n_cmn`, charge dans
   tous les cas) et lire l'identifiant qu'on lui passe. On saura alors la forme
   de l'appel, et il n'y aura plus qu'a le refaire avec celui du menu.

La seconde est plus sure : elle part d'un cas qui fonctionne.

---

## 5. YAMP : le moteur nomme (2026-09-03)

**https://github.com/CookiePLMonster/YAMP** (MIT, lu et non execute) lance VF5FS
en autonome depuis la copie embarquee dans **Yakuza 6** -- un quatrieme build,
sur PC x86-64, dont la DLL s'appelle `vf5fs-pxd-w64-Retail Steam.dll` quand la
notre est `vf5fs-pxd-w64-Retail_APM3.dll`.

### Les vrais noms

| ce qu'on appelait | son vrai nom |
|---|---|
| `SetState(ecx, edx)` en `0x1800DA800` | **`shift_next_mode(int)`** et **`shift_next_mode_sub(int)`** |
| la regle archive-puis-disque | **`isl_file_access`**, avec `csl_file_access` et `csl_file_access_archive` |
| le point d'entree du moteur | **`module_start` / `module_stop`** -- nos SEULS deux exports |

`module_start` recoit un **`vf5fs_game_config_t`** qui porte le mode de jeu, **la
langue**, la difficulte, l'energie, les rounds et le temps. La langue est donc un
parametre de demarrage, et pas seulement l'octet `moteur+0x64D956`.

### Notre numerotation est celle de la console

```cpp
bool dest_cs_autoload()
{
    shift_next_mode(4);
    shift_next_mode_sub(48);   // MODE_SUB_MAX
}
```

`MODE_SUB_MAX = 48` cote Steam, **55** chez nous : l'ecart vaut exactement les
**sept** etats `APM3_*` de la borne. Les sous-etats **0 a 47 sont donc les memes
des deux cotes**, ce qui valide notre lecture des tables de noms et rend
transposable tout ce que YAMP sait.

Confiance : **CONFIRMED**.

### L'hypothese que cela suggere

`dest_cs_autoload` entre en mode 4 avec le sous-etat **MAX**, c'est-a-dire « ne
change pas » : il laisse le mode choisir lui-meme son sous-etat d'entree. Nos
essais forcaient directement `MENU_MAIN` (36), **court-circuitant le code
d'entree du mode** -- celui qui charge les ressources. Cela expliquerait qu'aucun
`aet_n_main` ne soit jamais demande.

Essai fait le 2026-09-03 (`--devier 49 55 --tete 4`) : la deviation s'applique,
mais **aucune transition ne suit** -- le mode `MENU` ne choisit pas de sous-etat
de lui-meme. L'hypothese n'est donc pas confirmee telle quelle ; il manque
probablement l'appel qui, dans la version console, precede `shift_next_mode`.

---

## 6. LE MENU S'AFFICHE (2026-09-03, seconde seance)

Frederic, a l'ecran : « **le menu est bien affiche** mais on ne peut pas y
naviguer ».

Le chantier est passe de « on ne sait pas pourquoi il est vide » a « il
s'affiche, et il reste sa navigation ». Voici la chaine complete, mesuree.

### 6.1 `vf5fs_game_config_t` : trouve, lu, et patchable

YAMP donne la structure (`source/V6-VF5FS.cpp`) :

```c
struct vf5fs_game_config_t {          /* 8 octets */
    uint16_t energy;                  /* +0 */
    int8_t   round;                   /* +2 */
    int8_t   time;                    /* +3 */
    int8_t   diff;                    /* +4 */
    int8_t   game_mode;               /* +5 */
    int8_t   lang;                    /* +6 */
    bool is_triangle_start : 4;       /* +7 quartet bas  */
    bool is_dural_unlocked : 4;       /* +7 quartet haut */
};
```

Elle est a **`argp+0x38`** dans les 112 octets que `module_start` recoit -- la
meme place que chez YAMP, dont la `module_params_t` fait 64 octets et recouvre
exactement nos 64 premiers (`sl_module`, `gs_module`, `ct_module`, `cri_ptr`,
`root_path`, `module_main`, puis `config`). APM3 ajoute trois champs apres.

Valeur relevee au debogueur : `DC 00 02 2D 02 01 00 00`, soit energie **220**,
rounds **2**, temps **45**, difficulte **2**, **game_mode = 1**, langue 0.

`vfes.exe` l'ecrit en **cinq instructions** :

```
0x140002D45  mov  dword [rsp+0x78], 0x2D0300DC   energy=220 round=3 time=45
0x140002D77  mov  dword [rsp+0x7C], 0x01000102   diff=2 mode=1 lang=0 fl=1
0x140002DE7  and  byte  [rsp+0x7F], 0xF0         efface is_triangle_start
0x140002E1C  mov  byte  [rsp+0x7D], 1            game_mode  (dernier mot)
0x140002E32  mov  byte  [rsp+0x7A], 2            round      (dernier mot)
```

La lecture statique predit les huit octets du debogueur **exactement**.
Confiance : **CONFIRMED**.

Cote moteur, `module_start` copie les huit octets d'un bloc dans
**`0x18064D950`** et en derive quatre drapeaux :

| global | ce qu'il vaut | references |
|---|---|---:|
| `0x180C3B700` | `is_dural_unlocked` | 5 |
| `0x180C3B701` | `game_mode != 0` -- **l'aiguillage borne/console** | **32** |
| `0x180C3B702` | `game_mode == 2` -- un TROISIEME mode existe | 12 |
| `0x180C3B703` | `is_triangle_start` | 5 |

Et `0x18064D950 + 6` est exactement l'octet de langue deja patche depuis la
veille : la coincidence ferme la demonstration.

Correctif : `py -3 tools/patch_moteur.py --mode 0` (un seul octet, a l'offset
fichier `0x002220` de `vfes.exe`).

### 6.2 Le mode console demarre vraiment

Avec `game_mode = 0`, la machine a etats prend une route jamais vue :

```
DATA_INITIALIZE -> SYSTEM_STARTUP -> CS_DEMO -> CS_TITLE
   -> CS_SIGNIN -> WARNING -> CS_AUTOLOAD -> etat [MENU], sous-etat [MAX]
```

Trois ecrans que la borne n'affiche jamais : **PRESS START BUTTON**,
l'avertissement de sauvegarde console (avec l'invite PS3 « O:Enter »), puis le
cadre du menu principal. La derniere transition -- entrer dans `MENU` avec le
sous-etat `MAX` -- **est** `dest_cs_autoload()` de YAMP,
`shift_next_mode(4)` puis `shift_next_mode_sub(MODE_SUB_MAX)`.

Confiance : **CONFIRMED**.

### 6.3 La planche est enfin demandee

Le verrou du paragraphe 3 saute des qu'on masque les vingt entrees du `.par` en
mode console. Trace sur `CreateFileW` :

```
2 x  vf5fs_media/rom/2d/aet_n_main.bin      <- jamais demande auparavant
2 x  vf5fs_media/rom/2d/spr_n_main.farc     <- idem
2 x  ... adv, cmn, fnt32, clg
```

Deux ouvertures chacun, aucun reessai.

### 6.4 Pourquoi il restait vide : deux tics manquants

La fonction qui dessine le menu est **`0x1801E0C80`** (bornes `.pdata`
`0x1801E0C80-0x1801E10DA`). Elle garde chacun de ses blocs par :

```
0x1801BDA10   cmp dword ptr [rcx], 3 ; sete al ; ret
```

Point d'arret sur la garde, mode console : **1452 passages, en-tete = 1 et
texte = 1, jamais 3.** Le menu etait donc bien dessine, et il sautait son
contenu.

L'etat d'un objet AET est avance par le tic **`0x1801BBB10`** :

```
1 -> 0x1801BE520(obj, 0) ; etat = 2
2 -> si charge : 0x1801BE520(obj, 1) ; etat = 3      <- la garde passe
3 -> pret
4 -> ... ; 5 -> ... ; 0                              (fermeture)
```

Rester a 1 ne veut donc pas dire « le chargement echoue » : **personne ne fait
tourner le tic**.

La page de menu est un objet C++ construit par **`0x1801DA550`**, qui installe
la vtable **`0x180532AE8`** et assemble cinq pages soeurs. Le **creneau 2** de
ces vtables est la mise a jour de la page. En comptant les appels au tic dans
chacune, bornes par `.pdata` :

| page | mise a jour | appels au tic |
|---|---|---:|
| sous-page 0x19A8 | `0x1801DDB40` | 2 |
| sous-page 0x1CF0 | `0x1801DD9C0` | 2 |
| sous-page 0x1FF0 | `0x1801DC510` | 2 |
| page 0x180532A28 | `0x1801DD7A0` | 2 |
| page 0x1805329C8 | `0x1801DD400` | 2 |
| **MENU** | **`0x1801DC620`** | **0** |

Cinq soeurs, deux tics chacune ; le menu, zero. **C'est la coupe du build
arcade, a l'instruction pres** -- et elle remplace la formule vague du
paragraphe 3 (« le code qui DESSINE mais pas celui qui CHARGE ») par un
mecanisme.

Pour memoire, une lecture fausse ecartee en chemin : le creneau 9, bouchonne
pour le menu et pourvu chez les cinq soeurs, semblait le coupable. Mais il
appelle `0x1801BBA20`, qui fait `3 -> 4` : c'est la **fermeture** de scene, pas
l'ouverture. Les creneaux 5 et 6 sont bouchonnes chez tout le monde : ce sont
des virtuelles inutilisees, pas des coupes.

### 6.5 Le correctif

`py -3 tools/patch_moteur.py --menu-console` pose un relais de 52 octets dans le
rembourrage de `.text` (`0x18034575C`, 164 octets libres) :

```
sub  rsp, 0x38
mov  [rsp+0x30], rcx
add  rcx, 0x240          ; l'en-tete
call 0x1801BBB10
mov  rcx, [rsp+0x30]
add  rcx, 0x298          ; le texte
call 0x1801BBB10
mov  rcx, [rsp+0x30]
add  rsp, 0x38
jmp  0x1801DC620         ; la vraie mise a jour
```

et repointe le creneau 2 de la vtable (`0x180532AF8`) dessus.

Mesure apres correctif :

```
avant :  1452 x  en-tete = 1   texte = 1
apres :  1578 x  en-tete = 3 (PRET)   texte = 3 (PRET)
           16 x  en-tete = 2          texte = 2      (la transition)
```

Et a l'ecran, verifie par Frederic : **le menu s'affiche**.

Confiance : **CONFIRMED**.

### 6.6 Ce qui reste : la navigation

Le menu ne repond pas aux directions. Ce qui est mesure :

- le moteur interroge `Input_isOn` pour **tous** les codes 2 a 14, 2640 fois
  chacun sur une passe de 55 s ;
- le stub a bien rendu VRAI pour les directions scriptees (code 2 : 25 fois,
  code 3 : 49, code 4 : 24, code 5 : 25) et pour START (code 7 : 56) ;
- `Input_isOnNow` n'est demande que pour les codes **0, 7, 8 et 15** -- jamais
  pour les directions.

Les appuis arrivent donc jusqu'au moteur, et le menu n'en fait rien.

Piste ecartee faute de preuve : les trois structures de 0x44 octets que la mise
a jour consulte 21 fois par trame (`ctx+0x4FD0`, `+0x5014`, `+0x5058`, via les
accesseurs `0x1801B89E0..0x1801B8A30` sur le global `0x180752148`) ne changent
jamais de la passe -- mais leur contenu (`02 01 01 01 01 02 ...`) ressemble a
des reglages, pas a un etat de manette vivant. **Region probablement mauvaise :
rien n'est conclu.**

Prochaine mesure, qui ne presuppose rien : **diffusion de l'objet de page**.
Echantillonner les ~0x2A10 octets de l'objet a chaque trame et relever quels
decalages changent pendant les fenetres d'appui. Si rien ne bouge, l'entree
n'atteint pas la page ; si quelque chose bouge, c'est le curseur, et on tient
le champ.

---

## 7. CORRECTION, et la vraie cause unique (2026-09-03, meme seance)

**Ce que la section 6.4 affirme est faux, et il faut le dire clairement.**

J'y ai ecrit : « la mise a jour du menu `0x1801DC620` ne contient AUCUN appel au
tic, la ou ses cinq soeurs en ont deux ». Ce comptage etait borne par **une
seule entree `.pdata`**. Or la fonction en occupe **trois** :

```
.pdata : 0x1801DC620 - 0x1801DCE9D   (2173 octets)
.pdata : 0x1801DCE9D - 0x1801DD146   ( 681 octets)
.pdata : 0x1801DD146 - 0x1801DD18C   (  70 octets)
```

`0x1801DCE9D` commence par `mov [rsp+0xd8], r12` : ce n'est pas un prologue,
c'est une continuation. Les trois blocs sont **une seule fonction**, et le
deuxieme contient bel et bien trois tics :

```
0x1801DCE96  lea  rcx, [rdi + 0x240]
0x1801DCE9D  ...
0x1801DCEA8  call 0x1801BBB10          ; +0x240
0x1801DCEAD  lea  rcx, [rdi + 0x298]
0x1801DCEB4  call 0x1801BBB10          ; +0x298
0x1801DCEB9  lea  rcx, [rdi + 0x2f0]
0x1801DCEC0  call 0x1801BBB10          ; +0x2F0
```

Le menu **a** ses tics. Ce n'est donc pas une coupe du build arcade : c'est un
bloc qu'on n'atteignait jamais. Lecon a retenir : *une entree `.pdata` n'est
pas une fonction* -- voir `analysis/PROGRAMME.md` et le piege deja note de
`pe_disasm.py`.

### La cause, cette fois mesuree jusqu'au bout

Jalons poses sur la fonction, passe de 50 s dans le menu :

| jalon | RVA | passages |
|---|---|---:|
| entree de la fonction | `0x1DC620` | 1844 |
| apres le `jne` de `0x1DC6D6` | `0x1DC6DC` | **0** |
| sortie `xor al,al` | `0x1DCE33` | 1289 |
| bloc des tics | `0x1DCE96` | **0** |

Tout sort par **`0x1801DC6D6`**, et le debut de la fonction dit pourquoi :

```
0x1801DC6C2  cmp  byte [rdi+0x29FB], 0    ; drapeau "initialisation faite"
0x1801DC6C9  jne  0x1801DC709             ; deja faite -> le corps du menu
0x1801DC6CB  lea  rcx, [rbp+0x67]
0x1801DC6CF  call 0x180029FB0             ; <- BOUCHON
0x1801DC6D4  test al, al
0x1801DC6D6  jne  0x1801DCE33             ; -> retour faux, a chaque trame
0x1801DC6E3  mov  byte [rdi+0x29FB], 1    ; JAMAIS ATTEINT
```

et **`0x180029FB0` est `mov al, 1 ; ret`** -- le troisieme bouchon de la
famille, avec `0x180007450` (`xor al,al ; ret`) et `0x180007430` (`ret 0`).
Il rend toujours « encore occupe ». Le menu attend donc une initialisation qui
ne finira jamais, ne pose jamais son drapeau, et **son corps ne tourne pas une
seule fois**.

Cela explique **les deux** symptomes d'un coup : pas de tic (menu vide) et pas
de lecture des entrees (navigation morte). Le relais de `--menu-console`
soignait le premier en aval ; il n'etait pas la bonne reponse.

### Le correctif juste

`py -3 tools/patch_moteur.py --menu-init` neutralise le `jne` de 6 octets a
`0x1801DC6D6` (offset fichier `0x1DBAD6`, `0F 85 57 07 00 00` -> six `90`).
Le bloc d'initialisation qu'on traverse alors n'appelle que des bouchons
(`0x180007430`) et ne lit pas le tampon que `0x180029FB0` aurait rempli.

Mesure apres, **sans** le relais :

| jalon | passages |
|---|---:|
| entree | 1224 |
| apres l initialisation | **1** (le drapeau se pose) |
| bloc des tics `0x1DCE96` | **155** |
| garde du menu, etat des scenes | **1207 x etat 3 (PRET)** |

Les scenes atteignent l'etat 3 **toutes seules**. `--menu-console` devient
inutile ; il reste dans l'outil, documente comme un contournement.

### Ce qui bloque encore

Le corps sort encore 1068 fois par `0x1801DCE33`, plus loin :

```
0x1801DC999  lea  rcx, [rdi + 0x2a00]
0x1801DC9A0  call 0x1801DE560       ; doit rendre VRAI
0x1801DC9A7  je   0x1801DCE33
0x1801DC9AD  call 0x1800BA090       ; doit rendre FAUX
0x1801DC9B4  jne  0x1801DCE33
0x1801DC9BA  lea  rbx, [rdi + 0x29E8]
0x1801DC9C1  movzx eax, byte [rbx]  ; l ETAT DU MENU, 0 a 10
0x1801DC9CD  cmp  eax, 0xA
0x1801DC9D0  ja   0x1801DCE3A
0x1801DC9E7  jmp  rcx               ; table de saut a 11 entrees
```

Ni `0x1801DE560` ni `0x1800BA090` n'est un bouchon : il faut mesurer laquelle
des deux gardes se ferme. C'est la prochaine passe -- jalons sur `0x1DC9AD` et
`0x1DC9BA`.

### Acquis au passage : les codes de direction ne sont plus une hypothese

`0x180243ED0` est **le** lecteur d'entrees du moteur : une boucle sur deux
joueurs, un enregistrement de 0x54 octets chacun, les boutons lus pour le seul
joueur 0. Elle assemble un masque :

| code | bit | | code | bit |
|---:|---:|---|---:|---:|
| 2 | 12 | | 7 START | 0 |
| 5 | 13 | | 8 KICK | 1 |
| 3 | 14 | | 12 PUNCH | 2 |
| 4 | 15 | | 11 GUARD | 3 |
| 6 | 9 | | 9 | 6 |
| 13 | 4 | | 10 | 7 |
| 14 | 5 | | | |

puis range, par joueur :

```
[rdi+0x08] tenu     [rdi+0x0C] tenu a la trame precedente
[rdi+0x10] front montant        [rdi+0x14] relache
[rdi+0x18] repetition, masquee par [rsi+0xA8], retard [rsi+0xAC], periode [rsi+0xAD]
```

Le moteur calcule donc ses fronts lui-meme -- d'ou le fait qu'il ne demande
jamais `Input_isOnNow` pour les directions. Mesure dans le menu :

```
masque repetition = 0x000FF0C9   retard 24   periode 3
haut   -> tenu 0x00001000   front 0x00001000
droite -> tenu 0x00002000   front 0x00002000
bas    -> tenu 0x00004000   front 0x00004000
gauche -> tenu 0x00008000   front 0x00008000
START  -> tenu 0x00000001   front 0x00000001
```

**L'etat de manette du moteur est correct**, fronts compris, et les bits 12 a 15
sont bien dans le masque de repetition. La navigation ne bloque donc pas sur
l'entree : elle bloque parce que le corps du menu ne tourne pas.

Confiance : **CONFIRMED**.

---

## 8. BILAN DES LIENS DU MENU CONSOLE (2026-09-04)

Question posee : parmi toutes les entrees du menu et des sous-menus, lesquelles
fonctionnent et lesquelles ne renvoient vers rien. Ce qui suit est etabli
**statiquement**, sans mesure, mais sans supposition : chaque ligne renvoie a
une instruction.

### 8.1 D'ou viennent les libelles

Les entrees ne sont pas des chaines du binaire : ce sont des **identifiants de
texte** passes a `0x1801EFD10`, resolus dans une table chargee en
`0x180753900` (borne `0x5A0C` = 23052 entrees). Cette table est
`string_array.farc` du `.par` (1 165 900 octets, non compresse), un FArc de
deux fichiers : `string_array_en.bin` (0x44, 0x73770 octets) et
`string_array_jp.bin`. Le fichier est **gros-boutiste** : un tableau de
pointeurs u32 BE vers des chaines UTF-8, indexe par l'identifiant.

C'est ainsi que le menu se laisse nommer sans lancer le jeu.

### 8.2 Les trois choses a regarder pour chaque entree

1. **son etat**, un octet dans le tableau `page + 0x642 + i`, lu par le dessin
   (`0x1801E0C80`) : `0` normal, `1` **grise** (l'alpha est multiplie par une
   constante), `2` **pas dessine du tout** ;
2. **sa destination**, dans le repartiteur de validation `0x1801DDF30`
   (une seule fonction, dix entrees `.pdata` chainees jusqu'a `0x1801DE1E3`) ;
3. **si cette destination atteint un mode vivant** de la machine a etats
   (voir `analysis/machine_console.md`).

Regle generale du repartiteur, premiere chose qu'il fait :

    0x1801DDF4C  movsxd rcx, dword [rdi+0x58]          ; l'entree choisie
    0x1801DDF54  cmp byte [rcx + rdi + 0x642], 0
    0x1801DDF5C  je   ...                              ; entree normale : on dispatche
    0x1801DDF5E  call 0x180007450                      ; BOUCHON -> faux
    0x1801DDF65  je   sortie                           ; **on repart sans rien faire**

Autrement dit : **toute entree grisee ou masquee ne fait rien du tout**, et ce
n'est pas un oubli, c'est le bouchon qui ferme la seule branche qui restait.

### 8.3 Le menu principal, entree par entree

`[page+0x224] = 9` (`0x1801E39D0`). **Attention : ce champ est le DERNIER
INDICE, pas un compte** -- la boucle de dessin va de 0 a lui INCLUS
(`0x1801E1079 cmp edi,[rsi+0x224]` / `jle`). Il y a donc **dix** entrees, 0 a 9,
et la dixieme (`EXIT GAME`) etait dessinee-puis-cachee par son etat, pas
exclue du compte. Cette phrase disait le contraire ; corrigee le 2026-09-05
apres l'avoir payee a l'ecran (voir section 16).

| # | libelle (id) | etat | destination | verdict |
|---:|---|---|---|---|
| 0 | SINGLE PLAYER (0x177) | normal | scene `ARCADE MENU`, page `+0x658` | le sous-menu s'ouvre |
| 1 | OFFLINE VERSUS (0x178) | normal | scene `VERSUS MENU`, page `+0x19A8` | le sous-menu s'ouvre |
| 2 | ONLINE BATTLE (0x17A) | normal | scene `MULTI MENU`, objet `0x180753820` | **mene au mode 7 ONLINE, bouchonne aux trois gestionnaires** |
| 3 | DOJO (0x17B) | normal | scene `TRAINING MENU`, page `+0x1CF0` | le sous-menu s'ouvre |
| 4 | TERMINAL (0x17C) | normal | scene `TERMINAL MENU`, page `+0x2328` | le seul qui atteint un mode vivant (5 `CS_TERM`) |
| 5 | SCOREBOARDS (0x17E) | normal | `0x1801B0120`, scene `RANKING` | s'ouvre |
| 6 | ACHIEVEMENTS (0x17F) | **2 : non dessine** | `jmp 0x180007430` (`ret 0`) | **rien, et deux fois plutot qu'une** |
| 7 | HELP & OPTIONS (0x180) | normal | `0x1801AB3A0`, scene `OPTION` | s'ouvre |
| 8 | DOWNLOAD CONTENT (0x182) | normal | scene `DLC STORE`, page `+0x2928` | s'ouvre |
| 9 | EXIT GAME (0x183) | **2 : non dessine** | scene `EXIT_CAUTION` | ~~inatteignable~~ — **ouverte le 2026-09-05, un octet**, section 16 |

Deux details que seul le code donne :

* l'entree 8 porte `UNLOCK FULL GAME` (0x181) **ou** `DOWNLOAD CONTENT` (0x182)
  selon un predicat bouchonne (`0x1801E0D3D`, `cmove`). Bouchonne a faux, c'est
  **DOWNLOAD CONTENT** qui s'affiche ;
* si le predicat de `0x1801E39FA` etait vrai, les entrees **1, 2 et 4** seraient
  grisees. Il est faux : elles restent normales. Ici le bouchon nous sert.

Deux identifiants sont **sautes** dans la liste : `0x179` *Xbox LIVE BATTLE* et
`0x17D` *LEADERBOARDS*. Ce menu est celui de la PS3, pas celui de la 360.

### 8.4 Les sous-menus, et leurs entrees

| sous-menu | scene | entrees (identifiants resolus) |
|---|---|---|
| SINGLE PLAYER | `ARCADE MENU` | Arcade (0x19E), Score Attack (0x19F), License Challenge (0x1A0) — puis une 4e branche gardee par `0x180029FB0` (bouchon **vrai**) vers `CARD SELECTOR` |
| reglages Arcade | — | Difficulty, Round count, Time limit, Max health bar:Player, Max health bar:CPU |
| OFFLINE VERSUS | `VERSUS MENU` | Round count, Time limit, Max health bar:1P, Max health bar:2P, Stage select |
| DOJO | `TRAINING MENU` | Command Training (0x218), et l'entrainement libre |
| TERMINAL | `TERMINAL MENU` | Customize (0x299), Replays (0x29A) |
| ONLINE BATTLE | `MULTI MENU` | + `MULTI_WARN`, `ONLINE_NG` |
| autres pages atteintes | `RANKING`, `OPTION MENU`/`OPTION CONTROL`/`OPTION HOWTO`/`OPTION SETTING`/`OPTION FILE`/`OPTION INFO`, `DLC STORE`, `PROMOTION`, `EXIT_CAUTION`, `UNLOCK_DURAL`, `ALL CLEAR INFO WIN`, `DIFFICULTY CHANGE WINDOW` | |

### 8.5 LE PLAFOND, et il n'est pas dans les pages

Le vrai resultat de ce bilan n'est pas dans les pages, il est au-dessus.

Le repartiteur d'etats n'a **qu'une seule** porte publique pour demander un
mode : `0x1800DA9A0`. (Les globaux `0x18070C4F0` / `0x18070C50C` / `0x18070C510`
ne sont ecrits que par `0x1800DA550`, `0x1800DA657`, `0x1800DA6E2` et
`0x1800DA800`, c'est-a-dire par le repartiteur lui-meme ; et `0x1800DA800` n'a
qu'un appelant.) On peut donc enumerer **toutes** les demandes de mode du
moteur — 27 sites, tous resolus :

| mode | nom | sites qui le demandent |
|---:|---|---:|
| 0 | STARTUP | 8 |
| 2 | **GAME** | **0** |
| 4 | MENU | 10 |
| 5 | CS_TERM | 3 |
| 6 | **CS_TRAINING** | **0** |
| 7 | ONLINE (bouchonne) | 2 |
| 8 | APM3 | 2 |
| 9 | APM3_TESTMODE (bouchonne) | 1 |

**Les modes `GAME` et `CS_TRAINING` ont leurs trois gestionnaires vivants, et
personne, nulle part dans les 3,13 Mo du moteur, ne les demande.** La
transition qui ferait passer du menu au combat n'existe pas dans ce build.

C'est le plafond du menu console, et il explique tout le reste : SINGLE PLAYER,
OFFLINE VERSUS et DOJO ouvrent bien leurs sous-menus, on peut y regler la
difficulte, les rounds, le temps, le decor — et au bout, **rien ne peut
demarrer**. Seul TERMINAL debouche sur un mode vivant (`CS_TERM`), et ONLINE sur
un mode entierement bouchonne.

**Premisse qui borne ce resultat** : que `0x1800DA9A0` soit la seule facon de
demander un mode. Elle est verifiee par l'enumeration des ecritures directes
ci-dessus. Si un jour on trouve un mode pose autrement, tout ce paragraphe est
a refaire.

### 8.6 Ce que cela veut dire pour la suite

Reparer le menu console entree par entree ne menera nulle part : les pages
fonctionnent deja mieux que ce qu'on croyait. Ce qu'il faudrait, c'est
**fabriquer la transition manquante** — un appel `0x1800DA9A0(2)` avec le
sous-etat qui va bien, pose la ou le sous-menu valide son choix. C'est un ajout
de code, pas une levee de garde : rien a debloquer, tout a ecrire.

---

## 9. LA TRANSITION VERS LE MODE GAME, FABRIQUEE (2026-09-04)

Le bilan de la section 8 disait : rien a debloquer, tout a ecrire. Voici ce qui
est ecrit. Option `--transition-game` de `tools/patch_moteur.py`.

### 9.1 Il manquait DEUX maillons, pas un

L'enumeration exhaustive des demandes de sous-etat (38 sites, tous resolus,
meme methode que pour les modes) donne le second trou :

    MENU  --(absent)-->  GAME/SELECTOR  --(absent)-->  VS

Le sous-etat 19 `VS` n'est demande que par la **sortie de `GAMEOVER`**
(`0x1800DBA16`), c'est-a-dire par le « rejouer ». Aucune premiere entree.

Et la raison du second trou se lit en clair a la fin du milieu de `SELECTOR` :

    0x1800DB372  cmp byte [0x180C3B701], al   ; game_mode != 0
    0x1800DB378  jne 0x1800DB438              ; borne : autre chemin
    0x1800DB385  call 0x18016D360(objet)      ; selection terminee ?
    0x1800DB399  mov ecx, 4
    0x1800DB39E  call 0x1800DA9A0             ; -> mode 4 MENU

**En mode console, terminer la selection ramene au menu.** Ce n'est pas casse :
c'est coherent avec un build ou le combat n'est jamais demande. La branche
console de ce selecteur ne sert qu'a choisir un personnage et repartir.

### 9.2 Maillon 1 : SINGLE PLAYER demande GAME/SELECTOR

Dans le repartiteur de validation `0x1801DDF30`, la branche de l'entree 0 fait
27 octets (0x1801DDF86 a 0x1801DDFA0). On y tient les deux demandes plus le
saut vers l'epilogue -- **pas besoin de caverne** :

    0x1801DDF86  mov  ecx, 2
    0x1801DDF8B  call 0x1800DA9A0        ; demander le mode GAME
    0x1801DDF90  mov  ecx, 0x11
    0x1801DDF95  call 0x1800DA9C0        ; demander le sous-etat 17 SELECTOR
    0x1801DDF9A  jmp  0x1801DDFDF        ; l'epilogue de la fonction
    0x1801DDF9F  nop / nop

L'hote a deja `sub rsp, 0x20` dans son prologue : l'espace d'accueil des
appelants est en place et rsp est aligne (la fonction appelle deja
`0x1801BC010` plus haut). L'epilogue vise restaure `rbx` depuis `[rsp+0x30]`,
ou il est sauve a `0x1801DDF7D`, **avant** notre code.

**Pourquoi 17 SELECTOR et pas 18 MODE_SELECTOR** : c'est le seul dont on ait la
preuve qu'il tourne (section 5 de `machine_console.md` : 1 passage sur son
entree, 1326 sur son milieu, mesures au debogueur), et son milieu pilote
l'objet `[0x180714928]` -- le selecteur de combat, celui dont on vient
d'ouvrir la case de Dural.

### 9.3 Maillon 2 : la fin du selecteur mene au combat

Dix octets, et les tailles coincident au hasard heureux : `mov ecx, imm32` fait
cinq octets dans les deux cas, et les deux fonctions de demande sont voisines,
donc le `call rel32` garde sa longueur.

    0x1800DB399  mov  ecx, 0x13          ; 19 = VS   (etait : 4 = MENU)
    0x1800DB39E  call 0x1800DA9C0        ; sous-etat (etait : 0x1800DA9A0, mode)

On reste donc dans le mode GAME et on passe au sous-etat VS.

**Portee du changement** : cette branche n'est atteignable qu'en mode console
(`game_mode == 0`) et depuis GAME -- c'est-a-dire, aujourd'hui, uniquement par
le maillon 1. Les trois autres demandeurs de `SELECTOR` (`0x1800BABEC` dans
`DISP_CONTINUE`, `0x1801E89BA` dans `PAUSE MENU`, `0x1800DABFA` dans le milieu
de `VS`) ne passent pas par la.

### 9.4 La commande

    py -3 tools/patch_moteur.py --resolution 1280 720 --langue --logo-japonais \
        --dural --wxga --dural-grille --mode 0 --menu-init --menu-ranking \
        --transition-game

`--mode 0` est indispensable : il met `game_mode` a 0, ce qui ouvre le menu
console **et** met le maillon 2 sur son chemin.

### 9.5 Ce qui reste incertain, et qu'il faut voir a l'ecran

Confiance : **LIKELY**, pas mieux. Les deux maillons sont exacts en tant que
code -- ils sont verifies au desassemblage dans le binaire patche. Ce qui n'est
pas etabli, c'est que le reste de la chaine suive :

* le mode `GAME` a ses trois gestionnaires vivants, mais il n'a jamais tourne
  dans ce build : son entree `0x1800DC7D0` peut buter sur une ressource que
  seul le mode `APM3` prepare ;
* l'entree de `VS` (`0x1800DC890`) attend que la selection ait ete **remise au
  ROB**. Sur la borne c'est le pilote `0x18023Bxxxx` du mode APM3 qui s'en
  charge ; en console, c'est peut-etre le selecteur lui-meme, peut-etre
  personne. Si le combat demarre sans combattants, c'est ce maillon-la qui
  manque, et il sera le troisieme.

Trois issues a distinguer a l'ecran : la grille de selection apparait et le
combat demarre (chaine complete) ; la grille apparait et valider ne fait rien
(le maillon 2 ne suffit pas) ; rien ne se passe en validant SINGLE PLAYER (le
mode GAME ne demarre pas, et c'est son entree qu'il faut lire).

---

## 10. LA CHAINE DES ENTREES, DE LA TOUCHE AU CODE (2026-09-04)

Frederic, apres avoir vu la grille s'afficher sans pouvoir valider : « verifie
la configuration des inputs, les boutons arcade G, P, K, start et coin ne sont
certainement pas les memes que les boutons playstation ». Voici la chaine
complete. Outil : `tools/entrees.py`.

### 10.1 Trois etages, et c'est le deuxieme qui manquait

1. **`apm.dll`** (notre stub) rend `Input_isOn(code)` pour les codes 0 a 14.
   La table touche -> code est dans `tools/gen_apm_stub.py`.
2. **`0x180243ED0`** lit ces codes et compose un **masque de boutons arcade**
   de 32 bits, range en `0x180751050 + joueur*0x54`. C'est la que G, P, K,
   start et la piece prennent leur place. Releve instruction par instruction.
3. **`0x1801A2200`** traduit ce masque en **codes logiques** (0 a 103) via une
   table de **seize paires (masque, code)** en `0x18040AEC0`, copiee au
   demarrage dans les deux fiches de peripherique par `0x1801A2AB0`. Ce sont
   ces codes-la que lisent `0x180190B80` et `0x180190BC0`.

### 10.2 La table, jusqu'a la touche

| touche (stub) | `Input_isOn` | bit du masque | code logique | role |
|---|---:|---|---:|---|
| Entree (START) | 7 | 0 | **7** | grille : VALIDER |
| A | 8 | 1 | **8** | grille : VALIDER |
| T | 12 | 2 | **7** | grille : VALIDER |
| R | 11 | 3 | **9** | grille : VALIDER |
| Y | 13 | 4 | 103 | combat |
| U | 14 | 5 | 101 | combat |
| Z | 9 | 6 | 100 | combat (P/K/G) |
| E | 10 | 7 | 102 | combat |
| Espace (piece) | 6 | 9 | 2 | lu par personne ici |
| Haut / Droite / Bas / Gauche | 2 / 5 / 3 / 4 | 12 / 13 / 14 / 15 | 3 / 6 / 4 / 5 | curseur |

Trois choses que cette table apprend :

* **les boutons de combat ne valident pas la grille.** P/K/G sortent en codes
  100 a 103 ; le curseur, lui, teste 7, 8, 9 et 11. Valider, c'est **Entree,
  T, A ou R** -- pas Z, U, E ;
* le curseur teste aussi le code **11, qu'aucun bit ne produit**. Un quatrieme
  bouton de validation existe dans le code et n'a pas de fil ;
* les bits 8, 10 et 11 du masque (codes 13 et 99) n'ont eux non plus **aucune
  touche** dans notre stub : le bouton qui ouvre `OPTION` en mode console
  (masque `0x100`) n'est cable nulle part.

### 10.3 Le menu console ne passe pas par cette couche

Balayage des sites qui lisent un code logique dans les deux zones : **le
selecteur en lit, le menu n'en lit aucun**. Les pages de menu passent
directement par `0x1801A2CA0(masque)`, c'est-a-dire par le masque arcade brut
(on l'a vu tester `8` et `0x100`). Deux couches d'entree coexistent donc, et
elles ne se recouvrent pas.

### 10.4 Ce que cela ne dit pas encore

La chaine est complete et exacte, mais elle n'explique pas a elle seule que
valider ne fasse rien : `Entree` produit bien le code 7. Deux gardes restent en
travers, et il faudra une mesure pour dire laquelle :

* `[selecteur + joueur*0x40 + 0x81]` -- « ce joueur peut-il bouger le curseur »
  --, pose a 0 ou 1 par `0x18016E390` (`0x18016ECCF` et `0x18016ED10`) ;
* la completion console elle-meme, `[selecteur + 0x62] = 1`, qui n'est atteinte
  (`0x18016CBA4`) que si `0x180170620(selecteur+0x68)` est vrai -- c'est-a-dire
  si la sous-scene `SEL_CHARA` s'est declaree finie **et** que son animation
  `+0x1D0` est terminee.

---

## 11. MAILLON 3 : L'OBJET DE SESSION (2026-09-04)

Premiere version de la transition : **le jeu plante**. Et un plantage donne une
adresse, ce qui vaut mieux qu'une heure de lecture.

### 11.1 Ce que le journal Windows donne

    Nom du module defaillant : vf5fs-pxd-w64-Retail_APM3.dll
    Exception code : 0xC0000005 (violation d'acces)
    Fault offset   : 0x00000000000B1D33   ->  VA 0x1800B1D33

En `0x1800B1D33`, une feuille de trois instructions, **sans entree `.pdata`**
(c'est pour cela que `tools/plage.py` existe) :

    0x1800B1D30  movsxd rax, edx
    0x1800B1D33  movzx  eax, byte [rax + rcx + 0xC]     <-- ici
    0x1800B1D38  ret

Un accesseur `f(objet, indice)`, qui plante parce que **`rcx` est nul**. Et
l'appelant est exactement le notre :

    0x1800DCA90  ENTREE DU SOUS-ETAT 17 SELECTOR
    0x1800DCA9D  call 0x1800B23A0     ; rend l'objet de session
    0x1800DCAAE  mov  rbx, rax        ; sans le tester
    0x1800DCAC7  call 0x1800B1D30     ; boum

### 11.2 La cause

`0x1800B23A0` rend le singleton `[0x1806F9C18]`. Il est cree par
`0x1800B3620(ecx)` (allocation de 0x16E0 octets) et **l'entree du mode GAME ne
le cree pas**. Les cinq createurs sont ailleurs : `0x1801E5010` (entree de
`CS_TERM`), `0x1801E2E80`, `0x180209DB0`, `0x18023A3C0` et `0x18023DF10` --
borne, terminal, entrainement. Sur la borne, c'est le parcours APM3 qui
fabrique l'objet avant d'arriver au selecteur. Par le menu console, personne.

Il manquait donc un **troisieme maillon, qui n'est pas une transition mais une
creation**. Correction du bilan de la section 8 : le trou n'etait pas
« deux liens », c'etait « deux liens et un objet ».

### 11.3 Le correctif

L'idiome est copie tel quel de `0x18023DFC0`, sur le chemin APM3 :

    call 0x1800B23A0 ; test rax,rax ; jne deja
    xor ecx, ecx     ; call 0x1800B3620
  deja:

Ces 46 octets ne tiennent plus dans les 27 de la branche du menu. Ils vont donc
dans la **seule caverne du binaire** : le remplissage de fin de `.text`,
`0x18034575C`, 164 octets. On se place dans sa seconde moitie (`+0x60`) pour ne
pas heurter le relais de `--menu-console`, qui occupe la premiere.

Cette caverne est **entre la taille virtuelle (`0x34475C`) et la taille brute
(`0x344800`)** de la section. Ce n'est pas un no man's land : elle est dans
`SizeOfRawData`, donc projetee depuis le fichier, et dans la derniere page
mappee. `tools/plage.py` a ete appris a la lire, `va2off` la refusant.

    0x1803457BC  sub  rsp, 0x28
    0x1803457C0  call 0x1800B23A0
    0x1803457C5  test rax, rax
    0x1803457C8  jne  0x1803457D1
    0x1803457CA  xor  ecx, ecx
    0x1803457CC  call 0x1800B3620      ; creer la session
    0x1803457D1  mov  ecx, 2
    0x1803457D6  call 0x1800DA9A0      ; mode GAME
    0x1803457DB  mov  ecx, 0x11
    0x1803457E0  call 0x1800DA9C0      ; sous-etat 17 SELECTOR
    0x1803457E5  add  rsp, 0x28
    0x1803457E9  ret

et la branche du menu se reduit a `call caverne` + `jmp epilogue`.

Alignement : au `call` depuis `0x1801DDF86`, rsp vaut 0 modulo 16 (l'hote a
`push rdi` puis `sub rsp, 0x20`) ; le `call` empile 8 ; `sub rsp, 0x28` ramene
a 0 et reserve les 32 octets d'espace d'accueil.

---

## 12. MAILLON 5 : OFFLINE VERSUS (2026-09-04)

### 12.1 La page VERSUS est la soeur exacte de celle du menu

Sa vtable est `0x1805328A8`, et elle se lit creneau par creneau en face de
celle du menu principal (`0x180532AE8`) :

| creneau | menu principal | VERSUS |
|---:|---|---|
| 1 (entree) | `0x1801E36D0` -- 9 entrees | `0x1801E4560` -- 4 entrees |
| 2 (mise a jour) | `0x1801DC620` | `0x1801DDB40` |
| 3 (validation) | `0x1801DE7B0` | `0x1801DEA60` |
| 4 (dessin) | `0x1801E0C80` | `0x1801E2190` |

Le dessin le confirme sans ambiguite : ses libelles sont `Round count`,
`Time limit`, `Max health bar:1P`, `Max health bar:2P`, `Stage select`, sous le
titre `OFFLINE VERSUS` (0x178).

**Correction d'une lecture trop rapide** : la section 8 supposait que
`0x1801DD6A0` -- seul site du moteur a poser le type de partie 1 -- etait la
page VERSUS. C'est faux. Sa vtable commence en `0x1805326C8` et son dessin est
`0x1801E17A0`, titre `TERMINAL`, entrees `Customize` / `Replays`. C'est donc la
page **TERMINAL**. Le sens du type 1 reste donc **inconnu** ; l'hypothese
« 1 = versus » de la section 8 de `vs_gameover.md` est retiree.

### 12.2 Ce qui manquait, et c'est la meme chose

`0x1801DEA60` (validation) fait exactement ceci :

    0x1801DEA66  cmp byte [rcx+0x60], 0   ; le joueur a-t-il valide ?
    0x1801DEA6D  je  0x1801DEB19          ; non -> annulation
    ...          recopie les cinq reglages de la page (+0x240 a +0x250)
                 dans le bloc courant
    0x1801DEB12  call 0x1801BA0A0         ; enregistre le bloc
    ...          referme la page et rend VRAI

**Elle enregistre les reglages et ne lance rien.** Meme forme que SINGLE
PLAYER : la page finit proprement, et personne ne demarre le combat -- puisque
rien dans le moteur ne demande le mode GAME.

### 12.3 Le correctif

On accroche **la fin du chemin valide, et lui seul** (l'annulation passe par
`0x1801DEB19`). A `0x1801DEB12`, `rcx` pointe deja le bloc de reglages ; le
relais appelle l'enregistrement avec ses arguments intacts, puis la caverne du
maillon 1 :

    0x1803457CC  sub  rsp, 0x28
    0x1803457D0  call 0x1801BA0A0        ; enregistrer les reglages
    0x1803457D5  call 0x18034579C        ; session + mode GAME + SELECTOR
    0x1803457DA  add  rsp, 0x28
    0x1803457DE  ret

La caverne du maillon 1 a ete deplacee de `MENU_CAVE + 0x60` a `+ 0x40` pour
loger les deux relais sans toucher a la premiere moitie, reservee au relais de
`--menu-console`.

Cinq octets a l'accroche, dix-neuf dans la caverne. Le reste -- selecteur,
combat, arbitre de fin, retour au menu -- est deja en place et sert les deux
entrees.

### 12.4 Ce qui reste incertain

* On passe **le meme argument `0` a `0x1800B3620`** que pour SINGLE PLAYER. Si
  cet argument est un nombre de joueurs, le versus a deux pourrait n'en avoir
  qu'un. C'est le premier endroit a regarder si l'ecran de selection ne
  propose pas deux curseurs.
* Le **type de partie reste 0** : la page VERSUS n'en pose pas, et c'est le
  menu principal qui a mis 0 (`0x1801DCC61`). Le combat se deroulera donc
  comme un solo du point de vue de la fin de partie.

### 12.5 MESURE : « ecran de reglage grise, impossible de lancer »

Et le message que la page affiche alors le dit en toutes lettres. Identifiant
de texte **0x81**, resolu par `tools/libelles.py` :

> « Two controllers are needed to play this mode.
>   Press the START button on Player 2's controller. »

Sa mise a jour `0x1801DDB40` le demande a chaque trame :

    0x1801DDC58  mov  ecx, 1
    0x1801DDC5D  call 0x1801A2330      ; le peripherique 1 a-t-il un joueur ?
    0x1801DDC64  setns cl
    0x1801DDC67  mov  byte [rdi+0x309], cl

et tant que `[page+0x309]` est nul, elle affiche 0x81 et n'accepte rien. **La
page est intacte et fait exactement son travail** : notre maillon 5 n'est pas
en cause, il n'est simplement jamais atteint.

**LE JOUEUR 2 N'EXISTE PAS DANS CE BUILD.** La cause est deux etages plus bas,
dans le lecteur d'entrees APM3 :

    0x180243F5F  mov  ebx, r14d       ; ebx = 0
    0x180243F62  test ebp, ebp        ; ebp = le numero de joueur
    0x180243F64  jne  0x1802440D6     ; JOUEUR 2 : saute TOUTES les lectures

Le masque de boutons du joueur 2 vaut donc **toujours zero** : la quinzaine
d'appels a `Input_isOn` n'est faite que pour le joueur 1. Ce build est
mono-joueur des la couche d'entree -- ce qui est coherent avec une borne a un
seul panneau.

`--versus-miroir` retire ce saut : le joueur 2 lit les **memes touches** que le
joueur 1. L'ecran se debloque et le combat peut partir, mais les deux
combattants bougent ensemble. C'est un **palliatif de mesure**, pas un vrai
deux-joueurs.

Un vrai joueur 2 demanderait deux choses : etendre notre `apm.dll` a une
seconde source (le stub a 32 creneaux de code, seuls 0 a 14 servent), et
ecrire un second bloc de lecture dans le moteur -- environ 0x16C octets, or la
caverne de `.text` n'en a plus assez. Ce serait un chantier a part entiere.

### 12.6 UN VRAI JOUEUR 2 : `--joueur2` + un stub a deux sources

Le miroir faisait bouger les deux combattants ensemble. Voici le vrai. Il tient
en deux temps, et il n'a coute que **trois octets d'idee**.

**Le constat qui rend tout facile** : sur les treize sites qui posent le code
d'entree dans `edx`, **deux le font deja relativement au joueur** --

    0x180243F71  lea edx, [rbp + 2]     ; rbp est l'index de joueur
    0x180243F84  lea edx, [rbp + 5]
    0x180243FA5  mov edx, 3             ; les onze autres sont absolus

Le lecteur avait donc ete ecrit pour deux joueurs, puis ampute.

**Temps 1.** Les onze `mov edx, imm32` (5 octets) deviennent
`lea edx, [rbp + code]` (3 octets) plus deux `nop`. Tous les codes sont alors
relatifs au joueur.

**Temps 2.** Les six octets liberes par le retrait du saut recoivent
`shl ebp, 4` : `rbp` vaut **0** pour le joueur 1 et **16** pour le joueur 2.
Les codes du joueur 2 sont donc ceux du joueur 1 plus seize -- 18 a 30, tous
dans les 32 creneaux du stub.

Et le decalage **ne casse pas la boucle**, sans rien avoir a restaurer : apres
ce point `ebp` n'est plus relu jusqu'a `inc ebp ; cmp ebp, 2 ; jb`. Joueur 1 :
0 << 4 = 0, puis 1, la boucle repart. Joueur 2 : 16 puis 17, et `cmp 17, 2`
sort. C'est exactement le comportement voulu.

**Cote stub**, `tools/gen_apm_stub.py` separe les deux sources :

| codes | joueur | source |
|---|---|---|
| 0 a 14 | 1 | **clavier seul** (fleches, Entree, A Z E R T Y U, Espace) |
| 18 a 30 | 2 | **manette seule** (croix, START, X A B Y, LB RB RT, BACK) |

Sans cette separation la manette piloterait les deux joueurs a la fois -- ce
qui etait le cas jusqu'ici.

Consequence a signaler : **la manette ne controle plus le joueur 1.** Les
scenarios d'`apm_entrees.txt`, qui nomment les codes 0 a 14, restent sur le
joueur 1 et ne changent pas.

### 12.7 MAILLON 6 : eteindre le menu en entrant en combat

Mesure a l'ecran : les deux curseurs bougent bien separement -- **le joueur 2
fonctionne** -- mais ils pilotent en meme temps le menu principal reste en
arriere-plan, et plus rien ne valide.

La sortie du mode MENU (`0x1800DCB80`) demonte pourtant bien les trois taches
du menu (0x208, 0x268, 0x269, posees par son entree `0x1800DCBF0`). Mais sous
condition :

    0x1800DCB90  call 0x1801B7010
    0x1800DCB95  test al, al
    0x1800DCB97  jne  0x1800DCB9E     ; vrai : on demonte
    0x1800DCB99  add rsp, 0x28 ; ret  ; faux : ON NE DEMONTE RIEN

et `0x1801B7010` rend « l'objet `0x180752000` n'est PAS occupe ». Quand on entre
en combat depuis la validation d'une page **encore ouverte**, il l'est : le
menu n'est jamais demonte, ses taches tournent et consomment les entrees.

Detail qui aggrave : dans ce cas la sortie rend `al = 0`, c'est-a-dire « pas
fini ». Le repartiteur la rappelle a chaque trame et la transition reste en
suspens.

`--menu-fermer` rend le demontage inconditionnel (quatre octets :
`test al,al ; jne` -> `nop nop ; jmp`). La semantique est sans ambiguite --
quitter le mode MENU doit retirer les taches du menu -- et la portee est celle
du parcours console, seul a emprunter ce mode ici.

### 12.8 Les touches, une fois le joueur 2 en place

Les codes du joueur 2 valant ceux du joueur 1 plus seize, et la table de
traduction etant la meme pour les deux peripheriques :

| | joueur 1 (clavier) | joueur 2 (manette) |
|---|---|---|
| deplacer le curseur | fleches | croix directionnelle |
| **valider** | `A`, `T`, `R`, `Entree` | **X, LB, Y, START** |
| piece | Espace | BACK |

(Les quatre touches de validation correspondent aux codes logiques 7, 8 et 9,
seuls lus par le curseur de la grille -- voir section 10.)

### 12.9 VERIFIE : OFFLINE VERSUS, A DEUX

Verdict de Frederic : **« le combat versus démarre, les deux joueurs se
contrôlent séparément »**.

Clavier pour le joueur 1, manette pour le joueur 2, sur un build dont la couche
d'entree ne lisait qu'un seul joueur. Deux entrees du menu console menent
desormais au combat :

| entree | maillons |
|---|---|
| SINGLE PLAYER | 1 (caverne), 2 (fin du selecteur), 4 (retour au menu), 6 (fermeture) |
| OFFLINE VERSUS | + 5 (accroche sur la validation de la page) + `--joueur2` |

La commande complete :

    py -3 tools/patch_moteur.py --resolution 1280 720 --langue --logo-japonais \
        --dural --wxga --dural-grille --mode 0 --menu-init --menu-ranking \
        --transition-game --joueur2 --menu-fermer

Ce que le joueur 2 apprend au passage, et qui vaut au-dela de VERSUS : **le
lecteur d'entrees avait ete ecrit pour deux joueurs, puis ampute**. Deux de ses
treize sites de code etaient restes relatifs au joueur (`lea edx, [rbp + N]`) ;
seul le saut d'entree et l'absence de seconde source manquaient. Ce n'est pas
une fonctionnalite reconstruite, c'est une fonctionnalite **rebranchee**.

---

## 13. LE DOJO — et une CORRECTION de la section 8 (2026-09-04)

### 13.1 L'enquete de la section 8 avait un angle mort

Elle affirmait : « les modes 2 `GAME` et 6 `CS_TRAINING` ont leurs trois
gestionnaires vivants, et **personne, nulle part dans les 3,13 Mo du moteur**,
ne les demande ». C'est vrai pour `GAME`. **C'est faux pour `CS_TRAINING`.**

L'erreur vient de la methode, pas du raisonnement : le balayage parcourait les
fonctions listees dans `.pdata`. Or `0x18019C3D0` est une **feuille** -- pas de
cadre de pile, sortie par saut terminal -- donc **sans entree `.pdata`**, donc
invisible. Exactement l'angle mort qui nous avait deja plantes avec
`0x1800B1D30`.

Un balayage **lineaire** de `.text` par motif d'octets (`E8`/`E9` + rel32) donne
le compte exact et definitif : **28** sites de demande de mode, **41** de
sous-etat. Un seul echappait a `.pdata` -- celui-ci :

    0x18019C3D0  mov  [0x180751010], ecx    ; le type de partie
    ...          remet les reglages a zero
    0x18019C407  test r8b, r8b
    0x18019C40A  je   0x18019C414
    0x18019C40C  lea  ecx, [rax + 6]        ; rax = 0
    0x18019C40F  jmp  0x1800DA9A0           ; DEMANDE LE MODE 6 CS_TRAINING

Lecon de methode, la troisieme fois qu'elle se paie : **`.pdata` ne liste pas
les feuilles.** Tout balayage qui s'appuie dessus est un minorant. Quand la
conclusion est « personne ne fait X », il faut le balayage lineaire.

### 13.2 Le DOJO demande deja son mode

La page DOJO est la troisieme soeur : vtable `0x180532968`, entree
`0x1801E4420` (2 entrees), mise a jour `0x1801DD9C0`, validation `0x1801A82D0`,
dessin `0x1801E1E40`. Sa mise a jour, des que le joueur valide :

    0x1801DDA45  eax = [page+0x58]          ; l'entree choisie
    0x1801DDA4C  ecx = 6                    ; entree 0
    0x1801DDA51  ecx = 7 ou 8               ; entrees 1 et 2
    0x1801DDA5C  r8b = 1 ; edx = 0
    0x1801DDA61  call 0x18019C3D0           ; type + MODE 6

**Il ne lui manque qu'une chose** : rien ne demande le **sous-etat 41
CS_TRAINING** (verifie au balayage lineaire). Sans lui, le mode changerait mais
le sous-etat resterait `MENU_MAIN`, dont le milieu est un bouchon : rien ne se
passerait.

### 13.3 Le maillon 7, le plus court

On accroche le **site d'appel** -- `0x18019C3D0` a sept appelants, les six
autres ne sont pas concernes --, on laisse la fonction poser son type et
demander son mode, et on ajoute la session et le sous-etat :

    0x18034575C  sub  rsp, 0x28
    0x180345760  call 0x18019C3D0       ; type + mode 6 (arguments intacts)
    0x180345765  call 0x1800B23A0       ; la session existe-t-elle ?
    0x18034576D  jne  0x180345776
    0x18034576F  xor  ecx, ecx
    0x180345771  call 0x1800B3620       ; sinon la creer
    0x180345776  mov  ecx, 0x29         ; 41 = CS_TRAINING
    0x18034577B  call 0x1800DA9C0
    0x180345780  add  rsp, 0x28 ; ret

Cinq octets a l'accroche, quarante et un dans la caverne. Celle-ci est
desormais pleine aux trois quarts, et `--menu-console` -- dont le relais
occupait la premiere moitie et que `--menu-init` a supplante -- est refuse
explicitement s'il est demande en meme temps.

---

## 14. MAILLON 8 : une touche pour sortir d'un mode (2026-09-04)

Constat de Frederic, DOJO en main : « il manque des touches pour sortir des
differents modes de jeu ». C'est **structurel**, et coherent avec tout le
reste : sur une borne on ne sort pas d'un mode, on joue jusqu'a la fin.

La preuve tient en un compte. Le seul arret du moteur vient de l'exterieur :
`0x1801B8C40`, qui pose le drapeau de fin `ctx+0x68C1`, n'a **qu'un appelant**,
`0x180245C51`, dans la zone des points d'entree du module. C'est l'hote qui le
commande, pas le jeu. Il n'y a donc aucun bouton de sortie a trouver : il n'en
existe pas.

### 14.1 Mais la porte est deja la, dans les deux milieux de mode

`0x1800DA9D0` (GAME) et `0x1801E4E60` (CS_TRAINING) ont la meme forme :

    bl = 0x1801B6FE0()      -> ecran-titre
    al = 0x1801B6E40()      -> mode 4 MENU
    test bl, bl ; jne ...
    test al, al ; je ... ; mov ecx, 4 ; call demander_mode

`0x1801B6E40` ne peut jamais rendre vrai -- dernier verrou bouchonne, section 8
de `vs_gameover.md`. On ne le touche pas (quatre appelants) : on remplace **les
deux sites d'appel** par un test de bouton.

### 14.2 Le bouton -- premier essai, et pourquoi il ne convenait pas

Premier choix : le masque `0x200`, c'est-a-dire la **piece** (`Espace`).
Frederic : « la touche espace est deja utilisee ».

Et il n'y a **aucun masque libre** a prendre. Les seize bits qu'alimente
`0x180243ED0` sont tous cables sur une touche qui sert (table de la section
10), et les bits 8, 10 et 11 n'ont **aucune source du tout**. Chercher un
bouton disponible dans cette couche etait donc sans issue.

### 14.3 La solution : ne pas passer par le masque

Le relais interroge directement `Input_isOn` sur un code **que le moteur ne lit
nulle part** : le **15**, libre entre les codes du joueur 1 (0 a 14) et ceux du
joueur 2 (18 a 30). Meme idiome que `0x180243ED0` : l'objet d'entrees est en
`[0x180C3B6F8]`, sa vtable est son premier champ, `Input_isOn` en est le
creneau `+0x158`. Il rend deja un booleen dans `al` -- la branche `test al, al`
qui suit n'a rien a convertir.

    0x1803457E0  sub  rsp, 0x28
    0x1803457E4  mov  rcx, [0x180C3B6F8]
    0x1803457EB  mov  rax, [rcx]
    0x1803457EE  mov  edx, 15
    0x1803457F3  call [rax + 0x158]        ; Input_isOn(15)
    0x1803457F9  add  rsp, 0x28 ; ret

Cote stub, le code 15 recoit **`Echap` au clavier et BACK a la manette**.
N'entrant pas dans la boucle par joueur, lui donner les deux sources est sans
effet de bord -- et cela donne une sortie a chacun des deux joueurs.

Trente octets dans la caverne, cinq a chacune des deux accroches. La caverne de
`.text` est pleine a 136 octets sur 164.

### 14.4 VERIFIE

« échap fonctionne, on sort bien au menu ». Et le DOJO, deux lancements plus
tot : « ça fonctionne parfaitement ».

Le parcours console compte donc quatre entrees vivantes et une sortie :

| entree du menu | etat |
|---|---|
| SINGLE PLAYER | combat solo, Dural comprise, boucle complete |
| OFFLINE VERSUS | combat a deux, clavier 1P / manette 2P |
| DOJO | entrainement, ses deux modes |
| — | **Echap / BACK** quitte n'importe lequel et rend la main au menu |

Huit maillons fabriques en tout, 136 octets de caverne sur 164.

---

## 15. L'ECRAN TERMINAL : le decor et les boutons (2026-09-04)

TERMINAL s'ouvre sans qu'aucun maillon ait ete fabrique -- la seule entree dans
ce cas : le menu contenait deja sa demande de mode ET de sous-etat
(`0x1801DCE05`), et l'entree du mode CS_TERM (`0x1801E5010`) est l'un des cinq
createurs de l'objet de session. Restent deux defauts, et ils n'ont rien a voir
l'un avec l'autre.

### 15.1 Le decor n'est pas incomplet : c'est le MAUVAIS

`0x1800D7130(index)` charge un decor par un index borne a 0x28, via la table
`0x18039F7A0` -- 41 entrees, chacune pointant un nom de trois lettres, qui se
lit en clair :

     0 tst   1 ts2   2 ts3   3 wht   4 ban   5 ter   6 nyc   7 cas   8 riv
     9 jin  10 sin  11 djo  12 umi  13 hai  14 are  15 slk  16 yuk  17 tak
    18 aur  19 bar  20 tan  21 du1 .. 25 du5  26 trm  27 cid  28 trs
    29 evo00 .. 38 evo09  39 gym  40 smo

La tache de decor de l'ecran de personnalisation (`0x1801C4D60`, celle qui
enregistre `STAGE_TASK`) demande **l'index 1**, c'est-a-dire `ts2` -- un decor
de **test**. Les tailles dans le `.par` suffisent a le montrer :

| fichier | taille | |
|---|---:|---|
| `stgts2.farc` | 505 420 o | ce qui est charge |
| **`stgtrm.farc`** | **1 289 391 o** | le decor « terminal », present et inutilise |
| `stgdjo.farc` | 10 516 296 o | un vrai decor de combat, pour l'echelle |
| `stgcas.farc` | 27 932 908 o | |

Il n'y avait donc rien a comparer avec la PS3 : **le decor complet est dans
l'archive**, le code pointait ailleurs. `--decor-terminal` remplace l'index 1
par **26 (`trm`)**. Un octet.

Portee : `0x1800D7130` n'a que **deux appelants** dans tout le moteur, celui-ci
et `0x18018F8A3` (le decor de combat, a index variable). Le changement ne
touche donc que l'ecran de personnalisation.

### 15.2 Les boutons manquants : le panneau de borne est plus petit que la manette

L'ecran de personnalisation lit ses entrees **uniquement par le masque
arcade** (26 sites, tous `0x1801A2CA0` ou `0x1801A2C10` ; jamais la couche de
pad). Les masques qu'il demande :

| masque | bits | source |
|---|---|---|
| `0x11000` / `0x22000` / `0x44000` / `0x88000` | 12-19 | les quatre directions -- **cablees** |
| `0x10`, `0x70` | 4,5,6 | Y, U, Z -- cablees |
| `0x200` | 9 | Espace (piece) -- cablee |
| **`0x100`** | 8 | **aucune source** |
| **`0x800`** | 11 | **aucune source** |
| **`0x200000`** | 21 | **aucune source** |
| **`0x400000`** | 22 | **aucune source** |

Quatre entrees que **rien ne peut produire** : `0x180243ED0` ne remplit que
seize bits (0 a 7, 9, 12 a 19), et les bits 8, 10, 11 et tout ce qui depasse 19
restent a zero. Ce ne sont pas des touches mal choisies, ce sont des boutons
que le panneau de la borne n'a pas -- l'ecran vient de la console, ou la
manette en offre davantage (L1/R1/L2/R2, SELECT).

Les leur donner demande d'**ajouter des lectures** dans `0x180243ED0`, donc de
la place : les onze couples de `nop` liberes par `--joueur2` font deux octets
chacun, non contigus, et la caverne de `.text` est deja pleine a 136 octets sur
164. C'est un chantier a part, a ouvrir avec un plan de place.

### 15.3 COMPARAISON AVEC R.E.V.O. : le decor n'est PAS en cause

> **A LIRE AVEC 15.10.** Ce qui est compare ici est l'appel d'ECLAIRAGE.
> L'appel de GEOMETRIE, cinq octets plus haut, n'avait pas ete vu. La
> conclusion « le decor n'est pas en cause » reste vraie au sens « la borne
> ne differe pas du PC », et fausse au sens « changer le decor ne sert a
> rien » -- cet essai-la n'avait jamais ete fait.

Frederic ayant redemande la comparaison, elle a ete faite avec le moteur de
R.E.V.O. -- `vf5fs-pxd-w64-d3d12_SteamRetail.dll`, 7,2 Mo, x64 lisible, dans
`Steam/steamapps/common/VFREVO/runtime/media/vf5fs/`. Resultat en quatre
points, tous negatifs :

| ce qui a ete compare | borne APM3 | R.E.V.O. |
|---|---|---|
| l'index demande par la tache de decor | **1** (`0x1801C4DCB`) | **1** (`0x1801EED9B`) |
| la table des 41 noms de decor | `tst ts2 ts3 wht ban ter ...` | **identique, entree pour entree** |
| la table etape -> cas de la tache (41 octets) | `00 01 02 07 07 ...` | **identique** |
| les huit cas de son aiguillage | offsets +0x30, +0x5E, +0x83, ... | **identiques au decalage pres** |
| les 41 `stg*.farc` du `.par` | 41 fichiers | **les memes 41** |

**HYPOTHESE PRECEDENTE RETIREE.** La section 15.1 supposait que la borne
chargeait un decor de test par erreur et que `trm` etait le bon. C'est faux :
`ts2` est le decor **voulu** pour cet ecran, dans les deux builds. L'option
`--decor-terminal` est marquee comme fausse dans `patch_moteur.py` et retiree
du lanceur.

Ce que la comparaison etablit donc : **le code et les donnees du decor sont les
memes que ceux de R.E.V.O.** La difference visuelle vient d'ailleurs.

Suspects restants, dans l'ordre :

1. **`--wxga`.** On force l'octet de variante d'affichage `[0x1806490D0+0x20]`,
   qui est lu a **54 endroits** de l'interface et decale des identifiants de
   scene. L'ecran de personnalisation est riche en interface. C'est le suspect
   numero un, et il se teste en un lancement : sans `--wxga` (Dural quitte la
   grille, mais TERMINAL se juge quand meme).
2. la resolution forcee a 1280x720, qui change les cibles de rendu ;
3. le sous-systeme de personnalisation lui-meme -- 312 fonctions, 68 Ko,
   entierement non lu (`analysis/carte_customize.md`).

### 15.4 Les directions : ce que le code dit

Le bloc de directions de `0x1801C7890` est une **rotation de camera**, et il
est garde :

    0x1801C78AF  mov  ecx, 0x40          ; bit 6 = la touche Z
    0x1801C78B4  call 0x1801A2C10        ; qui la TIENT ? (-1 si personne)
    0x1801C78B9  test eax, eax
    0x1801C78BB  jne  ...                ; on ne continue que si eax == 0
    0x1801C78BD  mov  ecx, 0x11000       ; haut
    ...          bas, gauche, droite

`0x1801A2C10` rend l'**indice du joueur** qui tient le bouton, ou -1. Le test
`eax == 0` veut donc dire « le joueur 1 tient Z ». Autrement dit, dans cet
ecran, **les directions ne font tourner le modele que si `Z` est maintenu**.

Le meme bloc lit ensuite quatre masques `0x100000`, `0x200000`, `0x400000` et
`0x800000` -- bits 20 a 23, soit le **stick analogique**. Aucun n'a de source :
`0x180243ED0` ne remplit que les bits 0 a 7, 9 et 12 a 19.

### 15.5 COMPARAISON DES DONNEES : `ts2` est identique dans les deux builds

Le code etant identique (15.3), restait la donnee. Les quatre fichiers du decor
`ts2`, sortis des deux `.par` et compares par empreinte :

| fichier | borne APM3 | R.E.V.O. | |
|---|---:|---:|---|
| `stgts2.farc` | 505 420 o | 505 420 o | **memes octets** |
| `light_ts2.txt` | 1 550 o | 1 550 o | **memes octets** |
| `fog_ts2.txt` | 224 o | 224 o | **memes octets** |
| `glow_ts2.txt` | 147 o | 147 o | **memes octets** |

Et les deux archives contiennent les **memes 41 decors**, nom pour nom.

**Conclusion : notre build affiche le meme decor, depuis les memes donnees, avec
le meme code que R.E.V.O.** Ce n'est donc pas un defaut de notre portage. La
capture PS3 montre un autre lieu parce que **la version PS3 utilise un autre
decor pour cet ecran** -- le changement date de la lignee borne/Ultimate
Showdown, pas de nous.

Ce qu'on ne peut pas verifier depuis ici : le PS3 `EBOOT.BIN` est un **SELF
chiffre** (`SCE\0`), donc illisible sans clefs, et le `rom.psarc` du dump ne
contient que l'interface (325 fichiers, aucun decor). Impossible donc de lire
l'indice que la PS3 demande.

D'ou `--decor-perso <indice|nom>` et `tools/decor_perso.cmd` : de quoi essayer
les 41 decors un par un et reconnaitre celui de la capture PS3 a l'oeil, ce
qui est la seule voie qui reste.

### 15.6 Pourquoi rien ne valide dans cet ecran

La capture de Frederic le dit elle-meme : elle affiche **« ✕ Back  ◯ Enter »**,
les boutons d'une manette PlayStation. Or les deux masques que l'ecran lit pour
ces deux actions sont `0x100` (bit 8) et `0x800` (bit 11) -- **et ces deux bits
n'ont aucune source** dans `0x180243ED0`, qui ne remplit que 0 a 7, 9 et 12 a
19. Le panneau de la borne n'a pas ces boutons.

Il faudrait donc les cabler, ce qui demande d'ajouter des lectures. La caverne
de `.text` est pleine (136 octets sur 164), mais il reste une reserve
identifiee : **la zone `0x18023xxxx`, propre au mode APM3**, que le parcours
console n'emprunte jamais. C'est la qu'il faudra prendre la place.

### 15.7 EXTRACTION DU PAQUET PS3 : le decalage de la table

Frederic : « extrait le decor de la version PS3 avec les outils a ta
disposition ». Fait -- `tools/unpack_ps3_pkg.py` sur le PKG retail de 2,05 Go
(`ZEYTrmPl...pkg`, AES-128-CTR, clef gpkg publique). L'extraction precedente
n'avait pris que `rom/2d` et `rom/rob` ; les decors sont dans `rom/objset`.

**Les decors de la PS3, vingt-sept `stg*.farc` :**

    are aur ban bar cas djo du1 du2 du3 du4 du5 gym hai jin nyc riv sin
    slk smo tak tan ter trm trs umi wht yuk

**Ceux de la borne qui n'y sont pas, quatorze :**

    tst ts2 ts3 cid evo00 .. evo09

Et **41 - 14 = 27**, exactement le nombre de decors PS3. Les comptes tombent :
la table de la borne est celle de la PS3 **plus quatorze entrees**, dont les
trois decors de test `tst ts2 ts3` inseres **en tete**.

La table PS3 est donc, dans le meme ordre :

     0 wht   1 ban   2 ter   3 nyc   4 cas   5 riv   6 jin   7 sin   8 djo
     9 umi  10 hai  11 are  12 slk  13 yuk  14 tak  15 aur  16 bar  17 tan
    18 du1 .. 22 du5  23 trm  24 trs  25 gym  26 smo

**L'ecran de personnalisation demande l'index 1.** Sur PS3 cela designait
`ban` ; depuis que la lignee borne a insere trois decors de test en tete, le
meme index designe `ts2`. **Personne n'a mis a jour l'appelant.** C'est une
vraie regression du build borne, et elle explique la capture de Frederic : la
PS3 montre un lieu, nous montrons un decor de test.

`--decor-perso 4` remet donc `ban`, l'equivalent borne de l'index 1 PS3.

**Verification supplementaire** : `stgtrm.farc` extrait du PKG PS3 est
**identique au bit pres** a celui du `.par` de la borne (SHA-1
`7757d2af106d801b`, 1 289 391 o, contenant `rm_obj.bin` + `stgtrm_tex.bin`).
Les donnees de decor sont donc les memes des deux cotes ; seul l'INDEX a
change.

### 15.8 MESURE, puis TEST : ce que le decor n'est PAS (2026-09-04)

Apres trois hypotheses fausses de suite, Frederic a mis le hola : « arrete de
patcher et de lancer le jeu quand on n'a encore rien valide ». Il avait raison,
et la suite s'est faite dans l'ordre : mesurer, puis eliminer.

**La mesure** (`tools/pister_decor.py`, un point d'arret sur le chargeur
`0x1800D7130`, lecture de `ecx` et de l'adresse de retour). Module a
`0x7FFAEE5A0000` :

| retour | offset | appelant | index |
|---|---|---|---|
| `0x7FFAEE72F8A8` | `0x18F8A8` | chargeur general | 1 (`ts2`) |
| `0x7FFAEE764DD5` | `0x1C4DD5` | **ecran de personnalisation** | **26 (`trm`)** |

et la tache va au bout : etape 1 franchie (34 passages, un seul aboutit),
etape 2 franchie (13 passages).

**Donc l'index est hors de cause, et notre patch fonctionnait.** Le decor `trm`
est demande, le chargement se termine, et l'image ne change pas : **ce qu'on
voit n'est pas le decor charge.**

**Le test** ensuite : relance sans `--wxga` (le seul de nos correctifs qui
touche massivement l'affichage -- l'octet `[0x1806490D0+0x20]` est lu a 54
endroits). Reponse de Frederic : **non**, aucun changement. `--wxga` est donc
hors de cause lui aussi.

### 15.9 Le bilan de ce fil, en negatif

Cinq choses ont ete eliminees, chacune par une verification et non par une
opinion :

| hypothese | comment elle est tombee |
|---|---|
| le decor est incomplet dans le `.par` de la borne | `stgtrm.farc` extrait du PKG PS3 : **identique au bit pres** |
| la borne charge un decor de test par erreur | R.E.V.O. charge le meme index 1, code identique |
| la table des decors differe | 41 noms identiques entre borne et R.E.V.O. |
| ~~c'est l'index qu'il faut corriger~~ | **ANNULEE le 2026-09-05, voir 15.10** : la mesure portait sur l'ECLAIRAGE, pas sur la geometrie |
| c'est `--wxga` qui abime l'ecran | test a l'ecran : aucun changement |

Ce qui reste, et c'est desormais le seul suspect : **le sous-systeme de
personnalisation lui-meme n'affiche pas le decor 3D dans ce build**. 312
fonctions, 68 Ko, jamais ouvertes (`analysis/carte_customize.md`).

Acquis au passage, et qui vaut pour la suite : la table des 41 decors, la
correspondance lieu/personnage tiree de la planche `aet_s_selstg` (section 15.7), et le fait que `trm` est **le seul vrai decor du jeu rattache a aucun
combattant** -- ce qui confirme, par une deuxieme voie, que c'est bien celui de
l'ecran TERMINAL.

### 15.10 CORRECTION : il y a DEUX index en dur, et je patchais le mauvais (2026-09-05)

Trois essais de decor n'avaient produit **aucune difference a l'ecran**. La
raison n'etait ni le decor, ni la donnee, ni `--wxga` : **l'octet que je
changeais ne commandait pas l'image**.

`0x1800D7130`, que tout ce fil appelle « le chargeur de decor », ne charge que
l'**environnement lumineux** :

    0x1800D71B5  lea r9, -> "./rom/ibl"          0x1800D71C1  lea r8, -> "%s/%s.ibl"
    0x1800D71DE  lea r9, -> "./rom/light_param"  0x1800D71EA  lea r8, -> "%s/light_%s.txt"

En changer l'index change une teinte, rien de plus -- imperceptible entre deux
decors de test. D'ou trois « je ne vois pas de difference ».

#### Le vrai demandeur

La tache `STAGE_TASK` (`0x1801C4D60`) fait **deux** demandes, chacune avec son
propre `1` en dur :

| etape | site | appel | ce que ca charge |
|---|---|---|---|
| 0 | `0x1801C4DA6` | `0x18018FCF0` | **la GEOMETRIE** -- jamais patchee jusqu'ici |
| 1 | `0x1801C4DCB` | `0x1800D7130` | l'eclairage -- le seul que je changeais |

`0x18018FCF0` est une **feuille**, donc absente de `.pdata` : il a fallu un
balayage lineaire de `.text` pour la trouver (la lecon de
`feedback_cartographier_la_zone`, payee une quatrieme fois).

    0x18018FCF0  cmp   ecx, 0x29           ; borne : 41 decors
    0x18018FCF5  mov   rax, [0x1807499D8]  ; le gestionnaire de decor
    0x18018FCFC  cmp   ecx, [rax + 0x5C]   ; deja charge ? on ne fait rien
    0x18018FD01  mov   [rax + 0x60], ecx   ; <- LA DEMANDE

#### Le gestionnaire de decor

Singleton `0x1807499D8`, construit par `0x18018EE30` (0xC0 octets), vtable
`0x180408210`. Son slot **+0x10** (`0x18018EF40`) consomme la demande a chaque
trame :

    +0x58  phase : 0 libre, 1..5 chargement en cours
    +0x5C  index CHARGE            +0x60  index DEMANDE (-1 = rien)
    +0x68  descripteur = 0x180403430 + index * 0xF0   (borne a 41)

`0x18018FE50` -- lu a l'etape 1 -- est le predicat « un decor est-il pret ? » :
faux tant que `+0x60 != -1` ou `+0x5C == -1`.

Le tableau de descripteurs `0x180403430` confirme la numerotation, en clair :

| index | +0x00 | +0x08 | +0x48 | +0x68 |
|---|---|---|---|---|
| 1 | `STGTS2` | `EFFSTGTS2` | `rom/STGTS2_COLI.000.bin` | `vfes_bgm_vf2_ban.adx` |
| 5 | `STGTER` | `EFFSTGTER` | `rom/STGTER_COLI.000.bin` | `vfes_bgm_stg_ter.adx` |
| 26 | `STGTRM` | `EFFSTGTRM` | `rom/STGDU1_COLI.000.bin` | `vfes_bgm_stg_ban.adx` |

Trois appelants seulement pour `0x18018FCF0` : `0x1801C4DAB` (ici, en dur),
`0x1800BC6AD` et `0x1802035AA` (tous deux a index variable). Le changement ne
peut donc toucher que cet ecran.

#### La tache, cartographiee en entier

41 etapes, mais **7 cas utiles** seulement -- et la sequence reelle est
0, 1, 2, puis un saut a 10, 11, 12, 40 :

| cas | etapes | ce qu'il fait |
|---|---|---|
| 0 | 0 | `"STAGE_TASK"`, puis `Decor_Demander(1)` |
| 1 | 1 | attend `Decor_Pret()`, puis `Eclairage_Charger(1)` |
| 2 | 2 | attend `0x1800D9020`, puis saute a l'etape 10 |
| 3 | 10 | `0x1801C3830`, `0x1801C3350` |
| 4 | 11 | modeles, interface, **BGM `rom/sound/bgm/vfes_bgm_cus.adx`** |
| 5 | 12 | `0x180244EA0` |
| 6 | 40 | `0x180186D40` (sortie) |
| 7 | tout le reste | sortie immediate |

Le BGM `_cus` identifie l'ecran sans ambiguite : c'est bien **CUSTOMIZE**.

#### Ce que la comparaison R.E.V.O. dit vraiment

La meme tache existe dans R.E.V.O. a `0x1801EED31`, et elle est **identique cas
par cas** : meme table etape->cas, memes 7 cas, meme `Decor_Demander(1)` suivi
de `Eclairage_Charger(1)`, meme BGM.

Ce que cela etablit : **la borne ne differe pas du PC**. Ce que cela
n'etablit pas : que `ts2` soit ce qu'il FAUT afficher. Les deux builds
afficheraient la meme chose ; si cette chose est un decor de test, elle l'est
aussi sur PC. L'essai `trm` sur la geometrie **n'avait jamais ete fait**.

#### Etat livre

`--decor-perso <index|nom>` patche desormais **les deux** octets. Verifie dans
le binaire produit :

    0x1801C4DA6  b91a000000   mov ecx, 0x1a     ; geometrie -> trm
    0x1801C4DCB  b91a000000   mov ecx, 0x1a     ; eclairage -> trm

**VALIDE A L'ECRAN LE 2026-09-05.** Frederic : « decor TRM valide pour
TERMINAL ». L'ecran affiche desormais le vrai decor du terminal. Le defaut
n'etait donc ni la donnee, ni `--wxga`, ni le sous-systeme de
personnalisation : c'etait un octet, et je changeais son voisin.

Lanceurs (double-clic, rien a taper) :

    tools\decor_TRM.cmd     le decor du terminal      <- retenu
    tools\decor_TS2.cmd     revenir a l'origine
    tools\decor_perso.cmd   demande lequel, parmi les 41

---

## 16. MAILLON 9 : EXIT GAME, la dixième entrée (2026-09-05)

Demande de Frédéric : une ligne « EXIT GAME » en bas du menu, pour revenir sous
Windows. **Elle existe déjà** — libellé `0x183`, dialogue `EXIT_CAUTION`
(`0x180532C78`), texte `0x3EE` — et, fait rare dans ce build, **son chemin
n'est pas bouchonné**.

### 16.1 Le moteur l'écrit, puis l'efface

Dans la construction du menu (`0x1801E3900`), à deux instructions d'intervalle :

    0x1801E39D0  mov dword [rbx+0x224], 9    ; on compte NEUF entrées
    0x1801E39E6  mov qword [rbx+0x642], 0    ; états 0..7 : normal
    0x1801E39F1  mov word  [rbx+0x64A], 0    ; états 8 ET 9 : normal aussi
    0x1801E3A13  mov byte  [rbx+0x64B], 2    ; ... puis on RECACHE la 9
    0x1801E3A21  mov byte  [rbx+0x648], 2    ; (et la 6, ACHIEVEMENTS)

L'état vit dans `page + 0x642 + i` : `0` normal, `1` grisé, `2` pas dessiné.
L'entrée 9 est donc mise à zéro puis remise à deux. **Un seul octet suffit** :
laisser l'état à zéro.

`[page+0x224]` ne se touche pas. Ce n'est pas un compte mais le **dernier
indice** — la boucle de dessin va de 0 à lui inclus :

    0x1801E0EFF  cmp dword [rsi+0x224], edi   ; edi = l'indice
    0x1801E0F05  jl  fin                      ; on sort quand count < i
    0x1801E1079  cmp edi, dword [rsi+0x224]
    0x1801E107F  jle boucle                   ; i va de 0 à count INCLUS

Je l'avais porté à 10 en le prenant pour un compte. Résultat à l'écran : une
**onzième** rangée, qui lit le tableau de libellés (dix entrées, `rbp-0x50` à
`rbp-0x2C`) hors bornes, tombe sur l'identifiant 0 et affiche `:Enter`.
Frédéric : « une ligne inutile "enter" est apparue juste au dessous ». Octet
retiré.

### 16.2 La validation, déjà écrite

    0x1801DE18E  scène "EXIT_CAUTION", texte 0x3EE   ; ouvre le oui/non
    0x1801DE1C5  mov byte [rdi+0x63C], 1             ; « un dialogue est ouvert »

puis, dans la mise à jour du menu :

    0x1801DCED2  cmp byte [rdi+0x63C], sil           ; dialogue ouvert ?
    0x1801DCEDB  call 0x1801BCE90                    ; la réponse
    0x1801DCEE9  js  sortie                          ; < 0 : pas encore répondu
    0x1801DCEF6  jne ailleurs                        ; != 0 : NON
    0x1801DCEF8  cmp dword [rdi+0x58], 9             ; <- l'entrée 9, en dur
    0x1801DCF09  call 0x1801DB8B0                    ; démontage des scènes
    0x1801DCF0E  mov byte [rdi+0x641], 1             ; « le menu est fini »

Le `cmp ..., 9` prouve à lui seul que **l'entrée 9 EST EXIT GAME**.

### 16.3 Ce qui manquait vraiment : le moteur ne sait pas se fermer

Sur borne, un jeu ne se ferme pas — l'hôte coupe. Le moteur n'a donc **aucune
sortie de processus** : ses seuls `ExitProcess` / `TerminateProcess` sont ceux
de la bibliothèque C. `vfes.exe` importe bien `Core_exitGame` et
`Core_isExitNeeded` de `apm.dll` (notre stub, qui les rend à 0), mais rien
depuis le menu ne les atteint.

On branche donc la dernière marche là où le moteur écrit « le menu est fini » :
entrée 9 confirmée, démontage déjà fait. Douze octets contigus sont
disponibles — l'écriture du drapeau (7) et le saut de sortie (5) — donc
**aucune caverne n'est consommée** (elle reste à 136/164) :

    c6 87 41 06 00 00 01 e9 20 02 00 00     avant
    33 c9 ff 15 02 94 16 00 90 90 90 90     après
     xor ecx,ecx ; call [ExitProcess]  ; remplissage

`ExitProcess` est déjà importée par la DLL (IAT `0x180346318`). Elle ne revient
pas ; si elle revenait, les `nop` mènent à `0x1801DCF1A`, une frontière
d'instruction valide.

### 16.4 Les deux sites

| site | avant | après |
|---|---|---|
| `0x1801E3A19` | `02` | `00` — l'entrée 9 est dessinée |
| `0x1801DCF0E` | `c68741060000 01 e920020000` | `33c9 ff15 02941600 90909090` |
| `0x1801DE182` | `488d8fc0040000 e8c2f7fdff` | `33c9 ff15 8e811600 90909090` |

(`0x1801E39D6` avait été porté de `09` à `0A` : c'était l'erreur ci-dessus, elle
est annulée.)

Option `--menu-exit`, lanceur `tools\console.cmd`. **VALIDÉ À L'ÉCRAN le
2026-09-05** : la ligne s'affiche et le OUI ferme le jeu. La réponse `0` est
bien l'affirmative.

### 16.5 Le dialogue d'avertissement, retiré (2026-09-05)

Demande de Frédéric : « supprimer le message d'avertissement sur les
sauvegardes après avoir appuyé EXIT GAME ». C'est le texte `0x3EE` —
**« All unsaved progress will be lost. Are you sure? »** — porté par la scène
`EXIT_CAUTION`. Sur borne il n'y a rien à sauver.

Le bloc qui l'ouvre n'appartient qu'à l'entrée 9, et l'autre branche est un
bouchon :

    0x1801DE152  cmp  ecx, 9
    0x1801DE155  jne  ailleurs
    0x1801DE15B  call 0x180007450        ; BOUCHON -> faux
    0x1801DE162  je   0x1801DE182        ; donc on va TOUJOURS au dialogue
    0x1801DE182  lea  rcx, [rdi+0x4C0]   ; <- la scene EXIT_CAUTION
    0x1801DE189  call 0x1801BD950

On y quitte directement, avec la même paire qu'en `0x1801DCF0E` — douze octets,
toujours sans caverne :

    33 c9              xor  ecx, ecx
    ff 15 8e 81 16 00  call qword [rip -> ExitProcess]
    90 90 90 90        remplissage jusqu'a 0x1801DE18E

**Conséquence à connaître** : `EXIT GAME` ferme désormais le jeu **sans
confirmation**. Une validation par erreur sur la dernière ligne du menu ferme
la partie. Le crochet de `0x1801DCF0E` devient du code mort — il est conservé,
il ne coûte rien et couvre l'autre route de l'entrée 9 (`0x1801DD027`).

Note : `ACHIEVEMENTS` (entrée 6) reste caché, à dessein — sa destination est un
`jmp 0x180007430`, elle ne mène nulle part.

---

## 17. LES SOUS-MENUS : le défaut venait de notre propre correctif (2026-09-05)

Constat de Frédéric : « quand je me déplace dans un sous-menu, les directions
agissent aussi sur le menu principal situé en arrière-plan ».

### 17.1 Le mécanisme voulu est écrit, et il est correct

Ouvrir un sous-menu démarre sa scène et range la sous-page dans `[menu+0x650]` :

    0x1801DDFCA  call 0x180245830          ; démarrer la scène du sous-menu
    0x1801DDFD1  je   sortie               ; échec -> on ne range rien
    0x1801DDFD3  mov  [rdi+0x650], rsi     ; succès -> la sous-page est rangée

La mise à jour du menu principal (`0x1801DC620`) se coupe alors dès sa
première instruction utile :

    0x1801DC63D  mov  rcx, [rdi + 0x650]
    0x1801DC647  je   suite                ; vide -> le menu principal continue
    0x1801DC649  call 0x180244EA0          ; la sous-page est-elle vivante ?
    0x1801DC650  jne  0x1801DCE33          ; OUI -> on rend la main sans rien lire
    0x1801DC656  ...  [rdi+0x650] = 0      ; NON -> on oublie la sous-page

Le répartiteur de validation a la même garde (`0x1801DDF36`), et R.E.V.O. a la
sienne au même endroit, **identique** (`0x1802093F6 cmp qword [rcx+0x608], 0`).
Rien ne manquait.

### 17.2 La mesure

`tools/pister_sousmenu.py` — cinq points d'arrêt, récit brut :

    OUVRE  OFFLINE VERSUS -> reussie
    GARDE  sous-page=0x2535ABEB288  vivante=1  (curseur deja bouge 320 x)
    OUBLI  la sous-page est effacee de [menu+0x650]
    OUVRE  OFFLINE VERSUS -> ECHOUEE
    OUVRE  OFFLINE VERSUS -> ECHOUEE

    curseur du menu principal deplace : 1323 fois

La sous-page est **vivante** et pourtant immédiatement oubliée. Un `jne` qui
ne saute pas alors que sa condition est vraie, cela ne s'explique que d'une
façon : **le `jne` n'était plus là**.

### 17.3 La cause : `--menu-ranking`

    MENU_RANKING = (DLL, 0x1801DC650, '0F85DD070000' -> '909090909090')

Notre propre option, posée le 2026-09-04. Sa raison était réelle : au
démarrage, une branche de la mise à jour ouvre la page RANKING et la range
comme si c'était un sous-menu —

    0x1801DCE27  call 0x1801B0120        ; ouvrir la page RANKING
    0x1801DCE2C  mov  [rdi+0x650], rax   ; <- le rangement qui figeait

— et sur une borne sans réseau cette scène n'a rien à jouer et ne se termine
jamais : le menu restait suspendu derrière elle. J'ai retiré le `jne`. Le
blocage a disparu, et **la suspension aussi, pour tous les sous-menus**.

### 17.4 Le correctif : `--sousmenu`, trois sites

| site | avant | après |
|---|---|---|
| `0x1801DCE2C` | `48898750060000` | sept `nop` — RANKING n'est plus rangée |
| `0x1801DC650` | six `nop` | **le `jne` est rendu** (on n'applique plus `--menu-ranking`) |
| `0x1801DC649` | `call 0x180244EA0` | `call 0x180244F90` |

Aucune caverne : `0x180244F90` est un prédicat du moteur, déjà utilisé sur le
**même objet** deux cents octets plus loin, pour exactement cette décision :

    0x1801DD01A  call 0x180244F90      ; la scène existe-t-elle encore ?
    0x1801DD01F  jne  sortie
    0x1801DD027  ...  [rdi+0x650] = 0  ; sinon on oublie la sous-page

#### Trois prédicats essayés, deux trop courts

| prédicat | question posée | résultat à l'écran |
|---|---|---|
| `0x180244EA0` (d'origine) | la scène **joue**-t-elle ? | faux dès la fin de l'animation d'ouverture |
| `+0x60 == 0` (caverne, essayé) | la sous-page **s'en va**-t-elle ? | ne se relâche jamais : « en sortant du sous-menu, le menu principal n'est plus navigable » |
| `0x180244F90` (retenu) | la scène **existe**-t-elle ? | vrai tant que le sous-menu est là |

Le `+0x60` de la sous-page n'est levé que le temps de la fermeture — la tâche
du menu le relit pour choisir quelle scène fermer (`0x1801E3CFB`) — puis
retombe à zéro. C'est un drapeau de transition, pas un drapeau d'état. La
caverne de 8 octets a été retirée ; elle est rendue au trou (136/164).

Le corps de `0x180244EA0` n'est pas touché — il a 96 autres appelants. Comme
toujours ici : **patcher le site d'appel, jamais le corps.**

`--sousmenu` refuse `--menu-ranking` : les deux se contredisent.

**VALIDE A L'ECRAN LE 2026-09-05.** Frederic : « ca fonctionne ». Le
sous-menu ne laisse plus passer les directions, et le menu principal
redevient navigable en sortant.

---

## 18. L'ÉCRAN D'AVERTISSEMENT SUR L'ÉPILEPSIE, sauté (2026-09-05)

Le quatrième écran du démarrage est le sous-état **`WARNING`**, clé 2 de la
table `0x1803A05A0` (nom en `0x1803A0F28`). Son texte est l'identifiant `0x36C`
de `string_array`, résolu en `0x18006C4FE` :

> A very small percentage of people may experience a seizure when exposed to
> certain visual images…

Ses trois gestionnaires :

| | | |
|---|---|---|
| entrée | `0x1800DE510` | démarre la scène AET `WARNING` |
| milieu | `0x1800DD7C0` | `call 0x180244EA0 ; sete al` — « fini quand elle ne joue plus » |
| sortie | `0x1800DDAF0` | détruit la scène |

Le moteur a **déjà** son chemin de saut, et c'est un bouchon qui le ferme :

    0x1800DE514  call 0x180007450     ; BOUCHON -> toujours faux
    0x1800DE51B  jne  0x1800DE538     ; vrai -> on sort SANS démarrer la scène
    0x1800DE525  ...  "WARNING" -> 0x180245830

On rend ce saut inconditionnel — **deux octets**, `75` → `eb`. La scène n'est
jamais démarrée ; le milieu demande alors à `0x180244EA0` si une scène absente
joue encore, obtient non, et rend « fini » dès la première trame. L'état
s'enchaîne tout seul.

Portée vérifiée : l'objet de scène `0x18070C530` n'a que **quatre** lecteurs
dans tout le moteur, dont les trois gestionnaires de `WARNING`. Aucun autre
écran ne s'en sert. Et la sortie détruit une scène absente sans broncher —
c'est le `0x1802450A0` de tout le monde.

**DEMENTI A L'ECRAN.** Frederic : « l'ecran warning est toujours present ».
Le saut du sous-etat `WARNING` fonctionne (verifie dans le binaire), mais
l'avertissement sur l'epilepsie n'est pas dessine par lui. `--sans-avertissement`
est retiree des lanceurs ; elle reste dans le patcheur, documentee comme
n'etant PAS cet ecran.

### 18.2 L'écran d'épilepsie : ce qui est ÉTABLI

Trois faits, et rien de plus.

**1. Cet écran est l'écran de chargement.** Le texte `0x36C` est dessiné par
une fonction que personne n'appelle : son adresse est le créneau **+0x20** (le
dessin) d'une vtable en `0x18034CB90`, posée en `0x18000194A` sur un singleton
statique, l'objet `0x180677040`. Cet objet est hébergé par le sous-état
`DATA_INITIALIZE`, et sa mise à jour (créneau +0x10, `0x18006B880`) est une
machine à **douze phases** sur `[obj+0x58]` qui charge pour de vrai :

| phase | ce qu'elle charge |
|---:|---|
| 4 | `EFFEFFCMN`, `STGCMN`, `NAGE_VF4`, `rom/sound/se_system.csb` |
| 8 | `rom/sound/se_tv_cmn.csb` |
| 10 | `rom/sound/se_terminal.csb` |

**À quoi sert cet écran** : il occupe l'écran pendant que le jeu charge ses
données communes, et il en profite pour afficher l'avertissement légal. Sauter
ses phases sauterait le chargement.

**2. Le texte peut être retiré.** Douze octets, vérifiés à l'écran le
2026-09-05. La garde du dessin est en tête du créneau +0x20 :

    0x18006C4B6  mov  ecx, [rcx + 0x58]   ; la phase
    0x18006C4B9  cmp  ecx, 1
    0x18006C4BC  jbe  0x18006C803         ; <- l'épilogue
    0x18006C4D7  cmp  ecx, 3
    0x18006C4DA  jle  0x18006C803
    0x18006C4FE  mov  ecx, 0x36C          ; le texte, à partir de la phase 4

On saute à l'épilogue sans condition : `e9 48 03 00 00` puis sept `nop`. Le
prologue doit être conservé — `0x18006C803` restaure `rbx`, `xmm6` et 0x110
octets de pile ; court-circuiter la fonction depuis son entrée corromprait la
pile.

**3. Il reste alors un écran blanc.** C'est la scène AET `DATA_INITIALIZE`,
démarrée en `0x18006C9E2`. Retirer ce fond a été essayé le 2026-09-05 **puis
annulé** : rien n'établit encore ce que cet écran doit devenir, et l'essai a
été arrêté avant d'être jugé. Le site est noté, il n'est pas patché.

Option `--sans-epilepsie` : elle n'enlève **que le texte**, et elle n'est dans
aucun lanceur. Le build livré garde l'écran d'origine.

### 18.3 Fausse piste, pour mémoire

Le sous-état `WARNING` (clé 2) et son saut de deux octets `0x1800DE51B`
`75` → `eb` : ils fonctionnent, mais ce n'est **pas** cet écran. Démenti à
l'écran. `--sans-avertissement` reste dans le patcheur, hors des lanceurs.

---

## 19. SINGLE PLAYER : les modes ne manquent pas, c'est NOUS qui les sautons (2026-09-05)

Demande de Frédéric : « rétablis tous les modes de jeux du mode SINGLE PLAYER ».

### 19.1 Ce que le jeu contient vraiment

| page | vtable | ce qu'elle porte |
|---|---|---|
| **les modes** | `0x180532848` | `[+0x224] = 3` → **quatre lignes** |
| réglages arcade | `0x1805328A8` | `[+0x224] = 4` → Round count, Time limit, Max health 1P/2P, Stage select |

Les quatre modes, libellés posés par le dessin `0x1801DF100` :

| # | id | libellé |
|---:|---|---|
| 0 | `0x19E` | Arcade |
| 1 | `0x19F` | Score Attack |
| 2 | `0x1A0` | License Challenge |
| 3 | `0x1A1` | Special Sparring |

Et leur validation `0x1801DDD00` est **vivante**, pas un bouchon : elle aiguille
sur `[page+0x58]` vers des sous-pages successives — l'entrée 0 ouvre la scène
`NORMAL MENU` sur `[page+0x300]`, l'entrée 1 travaille sur `[page+0x7E0]`, etc.

### 19.2 Pourquoi on ne les voit pas

**C'est notre propre correctif.** `--transition-game` remplace **27 octets** en
`0x1801DDF86` — précisément le bloc qui ouvrait le sous-menu :

    0x1801DDF86  lea  rbx, [rdi+0x658]
    0x1801DDF8D  mov  rcx, rbx
    0x1801DDF90  call 0x1801E48E0
    0x1801DDF95  lea  rdx, -> "ARCADE MENU"
    0x1801DDF9C  jmp  0x1801DE06C

Le maillon 1 le remplace par un appel à la caverne, qui crée la session et
demande GAME/SELECTOR. SINGLE PLAYER va donc droit à la grille, et toute la
branche des modes est court-circuitée. Même motif que `--menu-ranking` : un
correctif posé au premier endroit qui débloquait, et qui emporte autre chose —
voir la mémoire `feedback_garde_partagee`.

### 19.3 Le plan pour rétablir

1. **Ne plus détourner `0x1801DDF86`** : SINGLE PLAYER rouvre `ARCADE MENU`.
2. **Déplacer le maillon 1 plus bas**, à la fin de la chaîne des modes, pour que
   la session soit créée et `GAME/SELECTOR` demandé quand un mode est
   réellement choisi. Le site naturel est dans `0x1801DDD00` ou dans la page
   que le mode 0 ouvre (`NORMAL MENU`, `[page+0x300]`).
3. Vérifier que les trois autres modes aboutissent, ou les traiter un par un.

Le point à établir avant tout : **jusqu'où la chaîne native va-t-elle seule ?**
C'est ce qui décide où poser le maillon. Une mesure sur `0x1801DDD00` et sur
les demandes de mode répondra, comme pour le menu console.

### 19.4 Les modes lancent — mais tous en Arcade (2026-09-05)

`--sp-menu` rend le sous-menu, `--sp-lancer` fait lancer. Trois greffes de cinq
octets sur une seule caverne de dix-neuf, posée dans le bloc mort du cas
« How to Play » libéré par `--options-sans-howto` :

| mode | page de réglages | validateur | greffe |
|---|---|---|---|
| Arcade | `NORMAL MENU` | `0x1801DDE80` | `0x1801DDE89` |
| Score Attack | `SCOREATTACK MENU` | `0x1800A48A0` | `0x1800A48A9` |
| License Challenge | `LICENCECHALLENGE MENU` | `0x1801DDE40` | `0x1801DDE49` |

Les trois validateurs commencent par le **même** `call 0x1801BC010` (le son de
validation), d'où la caverne unique.

**Pourquoi le validateur et pas la fermeture** : mesuré. Valider et annuler sont
indiscernables une fois la page fermée — les deux gestionnaires posent
`[page+0x308] = 1` et ne diffèrent que par ce premier appel (`0x1801BC010` pour
valider, `0x1801BB9D0` pour annuler).

#### Ce qui reste faux

Frédéric, à l'écran : « Score Attack et License Challenge lancent le mode
arcade mais pas leur vrai mode », et « Special Sparring ne lance rien ».

La caverne `TRANSITION_CAVE` ne fait que ceci :

    0x1803457A0  call 0x1800B23A0     ; la session existe-t-elle ?
    0x1803457AA  xor  ecx, ecx
    0x1803457AC  call 0x1800B3620     ; la creer
    0x1803457B1  mov  ecx, 2   ; call 0x1800DA9A0   ; mode 2 = GAME
    0x1803457BB  mov  ecx, 0x11; call 0x1800DA9C0   ; sous-etat 17 = SELECTOR

Elle n'enregistre **jamais quel mode** a été choisi. Et les deux fonctions qui
en avaient l'air ne le font pas :

| fonction | ce qu'on croyait | ce qu'elle est |
|---|---|---|
| `0x1800B3620(n)` | le type de partie | `cmp ebx,1 ; jbe` — **nombre de joueurs**, 0 ou 1 |
| `0x1800B2FA0(session, n, 0, 0)` | le mode de jeu | `cmp ebx,1 ; jbe`, indexe `[rbx+rcx+0xC]` — **indice de joueur** |

**Le champ qui porte le mode de jeu n'est pas identifié.** C'est le prochain
verrou : sans lui, les quatre entrées mènent au même combat.

**Special Sparring** (mode 3) est à part : il n'a pas de page de réglages, il
passe par la fabrique `0x1801A5E90` — il n'y a donc aucun validateur à greffer.
Il faudra trouver quelle page elle rend.
