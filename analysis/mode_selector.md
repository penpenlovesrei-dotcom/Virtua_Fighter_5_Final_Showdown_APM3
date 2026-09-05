# MODE_SELECTOR (18) : le sous-état qui n'a pas d'écran

Désassemblé le 2026-09-05 sur `vf5fs-pxd-w64-Retail_APM3.dll.origine`, le
binaire **non patché**. Fait suite à `machine_console.md` (les deux tables),
`vs_gameover.md` (l'arbitre de fin de combat) et `carte_options.md` (le gabarit
d'une page de menu).

Recensé « vivant, jamais emprunté, jamais lu » dans `couverture_console.md`,
avec l'hypothèse « c'est probablement l'écran 1P / VS / entraînement ».

**Cette hypothèse est fausse.** `MODE_SELECTOR` n'est pas un écran : c'est un
**sas de trois gestionnaires, sans page, sans liste, sans libellé, sans
curseur, sans lecture d'entrées**, qui écrit un seul champ dans la session et
laisse la chaîne du mode l'emmener vers `VS`.

---

## 1. Le descripteur, et les bornes réelles des trois gestionnaires

Entrée 18 de la table des sous-états `0x1803A05A0`, à `0x1803A07E0` :

```
1803A07E0  12 00 00 00  01 00 00 00        ; +0x00 clé = 18, +0x04 = 1
1803A07E8  70 ca 0d 80 01 00 00 00        ; +0x08 entrée  0x1800DCA70
1803A07F0  20 ae 0d 80 01 00 00 00        ; +0x10 milieu  0x1800DAE20
1803A07F8  50 bb 0d 80 01 00 00 00        ; +0x18 sortie  0x1800DBB50
```

Nom : `MODE_SELECTOR`, chaîne `0x1803A0FF0`, pointée depuis la table des noms
`0x1803A0CE0` (56 entrées, 0 à 54 plus `MAX`), case `0x1803A0D70`.

Bornes établies au remplissage `int3` puis à la fonction suivante connue — pas
sur `.pdata`, qui chaîne les entrées :

| gestionnaire | plage | taille | valeur rendue |
|---|---|---:|---|
| entrée `0x1800DCA70` | → `0x1800DCA8C` | 28 o | toujours **vrai** |
| milieu `0x1800DAE20` | → `0x1800DB0F2` | 722 o | vrai ou faux, voir §4 |
| sortie `0x1800DBB50` | → `0x1800DBB65` | 21 o | toujours **vrai** |

Balayage linéaire de `.text` (motif `E8`/`E9` + rel32) et recherche des trois
adresses comme littéral 8 octets : **aucun appelant direct, aucune vtable**.
Les seules occurrences sont les trois cases du descripteur ci-dessus. Ces
fonctions ne tournent que par le répartiteur `0x1800DA550`.

---

## 2. Ce que l'écran est : rien

Énumération **complète** des 47 appels directs des trois gestionnaires
(balayage linéaire des trois plages, aucun tri, aucun filtre) :

* **0 appel indirect** — donc aucune vtable, donc aucune page ;
* **0 appel à `0x180245830`** — il ne démarre aucune scène AET ;
* **0 appel à `0x1801EFD10`** — il n'affiche aucun libellé ;
* **0 appel à `0x1801BBBE0`** (curseur partagé), à `0x1801A2BC0` (valider,
  code 7) ni à `0x1801A2B90` (annuler, code 8) — il ne lit aucune entrée.

Il n'y a donc **ni vtable, ni onze créneaux, ni `+0x224`, ni `+0x22C`, ni
`+0x58`/`+0x5C` de curseur, ni tableau de libellés**. Le gabarit de page décrit
au §1 et §4 de `carte_options.md` ne s'applique pas ici : ce sous-état ne
possède pas d'objet de page du tout.

### La seule scène du dossier : `DISP_JOIN`, qu'il arrête sans jamais l'ouvrir

La sortie arrête une scène AET, et le milieu l'interroge :

| fonction | corps | rôle |
|---|---|---|
| `0x1800BA0D0` | `0x1802450A0([0x1806F9C50] + 0x368)` | **arrête** la scène |
| `0x1800BCF60` | `0x180244EA0([0x1806F9C50] + 0x368)` | la scène **joue-t-elle ?** |
| `0x1800BD050` | `0x180245830([0x1806F9C50] + 0x368, "DISP_JOIN")` | **démarre** la scène |

`[0x1806F9C50]` est le gestionnaire d'affichage de combat : la même bande de
code y démarre `DISP_JUDGE`, `DISP_REPLAY`, `DISP_CONTINUE` (`+0x298`),
`DISP_GAME_OVER`, `DISP_ROUND_NO`, `DISP_WINNER`. Le créneau `+0x368` porte
**`DISP_JOIN`**, chaîne `0x18039B838`, et rien d'autre : ses deux seuls sites
de démarrage (`0x1800BD045` et `0x1800BE1AD`) passent tous deux ce créneau.

Balayage linéaire des appelants :

| fonction | appelants (balayage `.text`) |
|---|---|
| `0x1800BD050` démarrer | `0x18023BF35` — **le milieu d'`APM3_TRAINING` (52)**, et lui seul |
| `0x1800BA0D0` arrêter | `0x1800DBB54` (notre sortie), `0x18023C77E` (sortie d'`APM3_TRAINING`) |
| `0x1800BCF60` interroger | `0x1800DAF7E` (notre milieu, phase 3), `0x18023BBDB` (milieu d'`APM3_TRAINING`) |

Autrement dit : `MODE_SELECTOR` est le **jumeau console** d'une phase du mode
borne. Sur borne, `APM3_TRAINING` allume `DISP_JOIN` (l'invite « appuyez sur
START pour entrer en jeu ») puis attend sa fin en phase 2 avant de demander
`APM3_ONLINE_VS`. `MODE_SELECTOR` a le même guet et le même arrêt — mais
**personne, dans le parcours console, n'allume jamais la scène**.

---

## 3. L'entrée `0x1800DCA70` (28 o)

```
0x1800DCA70  sub  rsp, 0x28
0x1800DCA74  xor  ecx, ecx
0x1800DCA76  mov  dword [0x180644634], 1     ; la phase du milieu
0x1800DCA80  call 0x1801B7060                ; (0)
0x1800DCA85  mov  al, 1
0x1800DCA8B  ret
```

Deux choses, et c'est tout.

**`0x180644634`** (`.data`) est le compteur de phase du milieu. Balayage
linéaire de `.text` : **quatre références en tout**, toutes dans ces deux
gestionnaires — `0x1800DAE47` (lecture), `0x1800DAE7D` (= 1), `0x1800DAEEC`
(= 2), `0x1800DCA76` (= 1). Valeur initiale dans le fichier : **4**.

**`0x1801B7060(0)`** n'a rien à voir avec le son. Son corps entier :

```
0x1801B7060  mov  rax, [0x180752148]
0x1801B7067  mov  byte [rax + 0x68c1], cl
0x1801B706D  ret
```

C'est le drapeau `ctx+0x68C1` que `vs_gameover.md` §8.1 a identifié comme le
**premier verrou des deux sorties de secours** : `0x1801B6FE0` (retour au
titre) exige `+0x68C1` **et** `+0x68C2` ; `0x1801B6E40` (retour au menu) exige
`+0x68C1` puis trois autres verrous. Passer 0 **ferme les deux portes** pendant
que le sous-état tourne. 36 appelants dans le binaire, dont l'entrée de `VS`
(`0x1800DC896`) et celle de `SELECTOR` (`0x1800DCA98`).

> Correction à porter dans `vs_gameover.md` §6 : « Entrée de VS `0x1800DC890` :
> coupe le son (`0x1801B7060(0)`) » est faux. `0x1801B7060` ne touche pas au
> son ; il ferme les sorties de secours.

---

## 4. Le milieu `0x1800DAE20` (722 o) : une machine à quatre phases

### 4.1 Le préambule et l'aiguillage

```
0x1800DAE2C  call 0x1800B23A0        ; r15 = la session      = [0x1806F9C18]
0x1800DAE37  call 0x1800B23B0        ; r12 = session + 0x50  (sous-objet)
0x1800DAE42  call 0x1800B24B0        ; rsi = session + 0x4E0 (sous-objet)
0x1800DAE47  mov  edx, [0x180644634]
0x1800DAE52  mov  rdi, [rsi + 0x1090]
0x1800DAE59  sub  edx, 1 ; je 0x1800DAE87     ; phase 1
0x1800DAE5E  sub  edx, 1 ; je 0x1800DAEF6     ; phase 2
0x1800DAE67  cmp  edx, 1 ; je 0x1800DAF7E     ; phase 3
             ...                              ; défaut
```

Les trois accesseurs sont des feuilles d'une ligne :
`0x1800B23A0` → `[0x1806F9C18]`, `0x1800B23B0` → `rcx+0x50`,
`0x1800B24B0` → `rcx+0x4E0`.

| phase | corps | atteinte ? |
|---:|---|---|
| défaut (0, ≥ 4) | `0x1800DAE70` | non — l'entrée pose toujours 1 |
| 1 | `0x1800DAE87` | oui, à la première trame |
| 2 | `0x1800DAEF6` | oui, posée par `0x1800DAEEC` |
| 3 | `0x1800DAF7E` | **jamais — personne n'écrit 3** (§4.4) |

### 4.2 Phase 1 — sept gardes, dont cinq bouchonnées

Chaque garde à vrai fait sauter en `0x1800DB0E3`, qui rend `bl` = 0, donc
**faux** : « le sous-état continue ». Toutes fausses, la phase 2 est posée et
exécutée **dans la même trame**.

| site | appel | nature |
|---|---|---|
| `0x1800DAE70` | `0x180007450` | **bouchon** — rend faux (branche défaut) |
| `0x1800DAE89` | `0x180007450(0)` | **bouchon** |
| `0x1800DAE9B` | `0x180007450(1)` | **bouchon** |
| `0x1800DAEA8` | `0x180007450` | **bouchon** |
| `0x1800DAEB5` | `0x180007450` | **bouchon** |
| `0x1800DAEC2` | `0x180007450` | **bouchon** |
| `0x1800DAECF` | `0x1800B9020()` | vivant — interroge le pont borne |
| `0x1800DAEDF` | `0x1800B7850(session+0x4E0)` | vivant |
| `0x1800DAEEC` | `mov dword [0x180644634], 2` | passe en phase 2 |

`0x1800B9020()` : si le type de partie vaut 2, `0x1801D6610` / `0x1801D7910` ;
puis quatre interrogations du pont `apm.dll` (`[0x180C3B6F0]+0x1FE10`) avec les
codes `0x17`, `0x23`, `0x51`, `0x57` — rend vrai si l'une répond 2.

`0x1800B7850(x)` : si `[x+0x1090]` est non nul, saut de queue vers
`0x180167E90` ; sinon faux. `[session+0x1570]` (= `0x4E0 + 0x1090`) est le même
objet que `rdi` du préambule.

**Cinq bouchons sur sept.** C'est ici que vivait l'interaction : le corps
partagé `0x180007450` a 210 appelants dans le binaire, ce n'est jamais lui qui
a un sens, c'est le site d'appel — et cinq sites d'affilée dans la même garde
disent que la lecture de l'écran a été retirée en bloc.

### 4.3 Phase 2 — deux issues, puis la queue

```
0x1800DAEF8  call 0x180186D40(0)               ; son : arrête la voie 0
0x1800DAEFD  test rdi, rdi ; je 0x1800DAF35
0x1800DAF05  call 0x180167AC0(rdi)  -> ebx     ; [[rdi]+0xC8], si [[rdi]+0xB8]
0x1800DAF0F  call 0x180167AA0(rdi)  -> rdx     ; [[rdi]+0xC0], idem
0x1800DAF28  call 0x1800B7BA0(session, rdx, ebx, 1, -1)
0x1800DAF2F  jne 0x1800DB0E1                   ; à vrai -> rend VRAI
0x1800DAF35  call 0x1800B1D30(session, 0)      ; byte [session+0x0C]
0x1800DAF4B  call 0x1800B1D30(session, 1)      ; byte [session+0x0D]
             ; les deux non nuls :
0x1800DAF5B  call 0x18016CF70([0x180714928])   ; = [sel + 0x40C]
0x1800DAF68  call 0x1800B8D30(session, val, 0)
0x1800DAF6D  mov  bl, 1 ; ret                  ; rend VRAI
             ; sinon -> 0x1800DAFA6, la queue
```

`0x1800B1D30(s, n)` est `movzx eax, byte [n + s + 0xC]` : le drapeau « le
joueur *n* est en piste ». Son effaceur est `0x1800B27A0(s, n)`, qui remet en
plus `[s + 0x28 + n*4] = 0x15` (21 = « aucun personnage », cf.
`reference_vf5_enumeration_persos.md`) et trois `-1`.

`0x18016CF70` lit un champ du **sélecteur de combat** `[0x180714928]` — le
même objet que pilote le sous-état `SELECTOR` (17).

### 4.4 Phase 3 — le code mort

```
0x1800DAF7E  call 0x1800BCF60          ; DISP_JOIN joue-t-elle encore ?
0x1800DAF85  jne  0x1800DB0E3          ; oui -> rend faux, on attend
0x1800DAF8B  mov  ecx, 0x11
0x1800DAF90  call 0x1800DA9C0          ; demande le sous-état 17 SELECTOR
0x1800DAF95  mov  bl, 1 ; ret          ; rend vrai
```

C'est la **seule** demande de sous-état de tout `MODE_SELECTOR`, et elle est
**inatteignable** : le balayage linéaire de `.text` donne quatre références au
compteur `0x180644634`, qui n'écrivent que 1 et 2. Personne n'écrit 3.

C'est exactement le corps que le milieu d'`APM3_TRAINING` exécute en
`0x18023BBDB` — même appel à `0x1800BCF60`, même structure — à ceci près que
là-bas la phase est atteinte (`0x18023BF49 mov [rdi+0x34], 2`) et que la
demande porte sur `0x35` (`APM3_ONLINE_VS`).

### 4.5 La queue `0x1800DAFA6` : le seul travail réellement fait

```
0x1800DAFAB  call 0x180173FA0        -> ebx    ; ebx = (type_de_partie == 3)
0x1800DAFB7  call 0x1800B28B0(session+0x50, ebx)   ; [session+0x58] = ebx
0x1800DAFBE  test ebx, ebx ; je 0x1800DB086        ; 0 -> branche A
0x1800DAFC7  sub  ebx, 1   ; jne 0x1800DB0D4       ; ni 0 ni 1 -> impossible
             ; 1 -> branche B (0x1800DAFCD)
```

`0x180173FA0()` est trois instructions : `0x18019C090() == 3`. C'est le **type
de partie** de `vs_gameover.md` §2, lu dans `[0x180751010]`. La « sélection »
se réduit donc à **un test de constante** : aucune touche n'est lue, aucune
liste n'est présentée.

**Branche A — `0x1800DB086`, type ≠ 3** (notre parcours console, type 0) :

| site | appel | effet |
|---|---|---|
| `0x1800DB089` | `0x1800244D0(session)` → edi | `[session+8]` = le **joueur courant** (0 ou 1) |
| `0x1800DB099` | `0x180101820([0x18070FB10], edi)` → rbx | dossier du joueur : `base + 0x18 + edi*0x5A0` |
| `0x1800DB0A3` | `0x1800B6A70(edi)` → eax | 0, 1 ou 2 (tirage sur `0x18039B3D0` = {0,1,2}, corrigé par les drapeaux 7/8/9 du profil) |
| `0x1800DB0AD` | `0x1800B32E0(session+0x50, eax)` | `[session+0x5C] = eax` |
| `0x1800DB0B4` | `0x1800490E0(edi)` | table joueur `0x180675CE0`, 2 × 0x260 o |
| `0x1800DB0C2` | `0x180049030(edi, byte [rbx+0x117])` | idem |
| `0x1800DB0CF` | `0x180049220(edi)` | si `byte [rbx+1] != 0` |
| `0x1800DB0D7` | `0x1800B8540(session)` | validation (2026 o, jamais lue) |

Cette branche est **mot pour mot** celle du mode borne en `0x18023B853`, à un
détail près : là-bas `[session+0x58]` reçoit 0 en dur, ici il reçoit `ebx`.

**Branche B — `0x1800DAFCD`, type = 3** : même dossier de joueur, mais recopie
dans le singleton `[0x1806F9410]` (`0x180095510`, `0x180095920`, `0x180095B50`,
`0x1800958B0`) et `0x180048FF0` / `0x180049030` / `0x180049220`. Deux
arguments y sont **bouchonnés** :

| site | appel | valeur |
|---|---|---|
| `0x1800DAFFB` | `0x180007440` | **bouchon** — `xor eax, eax`, donc 0 |
| `0x1800DB002` | `0x180011950` | **rend -1** (`mov eax, 0xFFFFFFFF ; ret`, 12 appelants) |
| `0x1800DB009` | `0x180011950` | **rend -1** |

d'où `[session+0x60] = -1` (`0x1800B2F70`) et `[session+0x64] = -1`
(`0x1800B28C0`). Un cinquième corps constant à ajouter à la famille des
bouchons connus, avec un cercle d'appelants beaucoup plus étroit que les
quatre autres :

| corps | comportement | appelants (balayage linéaire) |
|---|---|---:|
| `0x180007430` | `ret 0` | 601 |
| `0x180007450` | rend faux | 210 |
| `0x180007440` | `xor eax` | 125 |
| `0x180029FB0` | rend vrai | 73 |
| `0x180011950` | rend **-1** | 12 |

---

## 5. La sortie `0x1800DBB50` (21 o)

```
0x1800DBB50  sub  rsp, 0x28
0x1800DBB54  call 0x1800BA0D0        ; arrête la scène DISP_JOIN
0x1800DBB59  call 0x180007430        ; BOUCHON (ret 0), résultat ignoré
0x1800DBB5E  mov  al, 1
0x1800DBB64  ret
```

Elle rend toujours vrai : la transition n'est jamais retenue.

---

## 6. `[session+0x58]` : le champ que tout ce sous-état sert à écrire

C'est le pivot, et il explique le nom.

`0x1800AFA70(session, dl)` est le constructeur de session : il pose la vtable
`0x18039B258` en `session+0`, la vtable `0x18039B248` en `session+0x50` (le
sous-objet est une classe à part entière), efface un tableau de 10 × 0x5C
octets, puis appelle `0x1800B4A70(session+0x50)` — dont la première écriture est :

```
0x1800B4A8C  mov qword [rcx + 8], 0xFFFFFFFFFFFFFFFF
```

**À la création d'une session, `[session+0x58] = -1`.**

Accesseurs du sous-objet `session+0x50` (feuilles d'une instruction) :

| fonction | champ | absolu |
|---|---|---|
| `0x1800244D0(x)` | lit `[x+8]` | `[session+0x58]` |
| `0x1800B28B0(x,v)` | écrit `[x+8]` | `[session+0x58]` |
| `0x1800B32E0(x,v)` | écrit `[x+0xC]` | `[session+0x5C]` |
| `0x1800B2F70(x,v)` | écrit `[x+0x10]` | `[session+0x60]` |
| `0x1800B28C0(x,v)` | écrit `[x+0x14]` | `[session+0x64]` |

Qui écrit `[session+0x58]`, balayage linéaire complet (6 sites) :

| site | valeur | contexte |
|---|---|---|
| `0x1800B7C97` | `byte [r14+0xFE]` | dans `0x1800B7BA0`, si type == 1 |
| **`0x1800DAFB7`** | `(type == 3)` | **notre queue** |
| `0x1800DB9FA` | 0 | sortie de `GAMEOVER`, branche « rejouer » |
| `0x1801C8409` | 1 | — |
| `0x1801CBDBC` | 1 | — |
| `0x18023B85D` | 0 | queue du mode borne |

Et `0x1800B4A70` le remet à **-1** depuis quatre sites, dont
`0x1800DB9CD` — la sortie de `GAMEOVER`, **avant** de décider quoi faire.

**Lecture la plus simple qui tienne : `[session+0x58]` est le mode de partie
choisi, et `-1` veut dire « pas encore choisi ».** `MODE_SELECTOR` est l'état
chargé de le remplir ; dans ce build il le remplit sans rien demander à
personne.

---

## 7. Qui demande le sous-état 18 : un seul site

Les 41 sites d'appel de `0x1800DA9C0(n)` (« demander un sous-état ») ont tous
été résolus, un à un, en lisant `ecx` en amont. **Aucun ne charge `0x12` en
dur.** Le seul producteur est l'arbitre de fin de combat `0x1800DB100`,
déjà repéré dans `vs_gameover.md` §4 :

```
0x1800DB220  mov  rcx, r14                ; r14 = session + 0x50
0x1800DB223  call 0x1800244D0             ; [session+0x58]
0x1800DB22D  cmp  eax, -1
0x1800DB235  mov  ecx, 0x12               ; MODE_SELECTOR
0x1800DB23F  cmove ebx, ecx               ; sinon ebx reste 0x13 (VS)
```

puis `0x1800DABD9 call 0x1800DA9C0` dans le milieu de `VS`.

Contre-épreuve indépendante : balayage linéaire de tout `.text` pour toute
instruction chargeant l'**immédiat `0x12`** dans un registre 32 bits (204
occurrences). Dans la bande de la machine à états `0x1800DA000`–`0x1800DE600`,
il n'y en a **qu'une seule** : `0x1800DB235`. Les autres 18 du binaire sont
ailleurs (`0x1801D0BD9` = les 18 cases de la grille, etc.).

Les six sites de `0x1800DA9C0` où `ecx` venait d'un registre ou d'un `lea` ont
été résolus aussi : `0x1800DABD9` (retour de `0x1800DB100`), `0x1801BB46E` (0x26–0x28),
`0x18023A710` (retour de `0x18023C0C0`, l'arbitre borne, borné à 0x32/0x33),
`0x18023B92F` (0x33), `0x1801DE398` (0x25–…), `0x180210F57` (0x14).

---

## 8. Comment on y arrive : la chaîne du mode — le mécanisme qui manquait

`machine_console.md` décrit la table des modes sans dire ce qu'il y a après le
champ `+0x18`. Or **chaque descripteur de mode porte, en `+0x20`, une liste
ordonnée de ses sous-états**, terminée par `0x37` (= `MAX`), et **en `+0x60`,
le mode qui lui succède par défaut**.

C'est `0x1800DA800(tête, sous-état)` qui s'en sert :

```
0x1800DA8C2  mov  dword [0x18070C50C], 0x37     ; sous-état courant
0x1800DA8CC  mov  dword [0x18070C510], 0x37     ; sous-état DEMANDÉ
...
0x1800DA921  cmp  edi, 0x37                     ; rien n'a été demandé ?
0x1800DA926  mov  eax, [rax]        -> [0x18070C50C] = chaine[0]
0x1800DA92E  mov  eax, [r8+0x24]    -> [0x18070C510] = chaine[1]
...                                             ; sinon : chercher edi
0x1800DA948  mov  ecx, [rax] ; cmp ecx, 0x37 ; je (sortie)
0x1800DA952  cmp  ecx, edi ; je 0x1800DA971     ; 15 cases au plus
0x1800DA974  mov  [0x18070C50C], edi            ; sous-état courant = edi
0x1800DA97A  mov  ecx, [r8 + rax*4 + 0x20]
0x1800DA97F  mov  [0x18070C510], ecx            ; = LE SUIVANT DE LA CHAÎNE
```

`[0x18070C510]` n'est donc pas « vide par défaut » : il est **pré-chargé avec
le successeur**. Et le bloc de transition du répartiteur, après qu'une sortie a
rendu vrai :

```
0x1800DA796  cmp  dword [0x18070C510], 0x37     ; on est le DERNIER ?
0x1800DA79D  mov  byte [0x18070C51C], 1         ; transition en attente
0x1800DA7A4  jne  0x1800DA7B7                   ; non : on ira au successeur
0x1800DA7A6  mov  byte [0x18070C500], 1         ; oui : changement de MODE
```

Et quand la tête change, `0x1800DA89F` recharge
`[0x18070C4F4] = [descripteur + 0x60]`, la tête suivante par défaut.

### La chaîne des dix modes

| mode | descripteur | chaîne `+0x20` | `+0x60` |
|---|---|---|---|
| STARTUP | `0x1803A0190` | DATA_INITIALIZE → SYSTEM_STARTUP → CS_DEMO → CS_TITLE → CS_SIGNIN → WARNING → CS_AUTOLOAD | MENU |
| ADVERTISE | `0x1803A01F8` | LOGO → RATING → DEMO → TITLE | MENU |
| MENU | `0x1803A0260` | MENU_MAIN | MENU |
| **GAME** | **`0x1803A02C8`** | **SELECTOR → MODE_SELECTOR → VS → GAMEOVER** | **MENU** |
| DATA_TEST | `0x1803A0330` | les 15 `DATA_TEST_*` | ADVERTISE |
| CS_TERM | `0x1803A0398` | CUSTOMIZE → REPLAY_PLAY → LAST_PLAY → CLIP_PLAY | MENU |
| CS_TRAINING | `0x1803A0400` | CS_TRAINING | MENU |
| ONLINE | `0x1803A0468` | les 6 `ONLINE_*` | MENU |
| APM3 | `0x1803A04D0` | ENTRY → SELECTOR → GAME_VS → GAMEOVER → TRAINING → ONLINE_VS | STARTUP |
| APM3_TESTMODE | `0x1803A0538` | APM3_TESTMODE_MAIN | APM3_TESTMODE |

La chaîne du mode `GAME` est à `0x1803A02E8` : `11 12 13 14 37`.

**`MODE_SELECTOR` est donc, par construction, l'étape entre `SELECTOR` et
`VS`.** On y arrive de deux manières :

1. **par la chaîne** : quand la sortie de `SELECTOR` rend vrai sans avoir rien
   demandé, `[0x18070C510]` vaut déjà `0x12` ;
2. **par l'arbitre** : `0x1800DB100` le demande explicitement quand
   `[session+0x58] == -1`, c'est-à-dire tant que le mode n'a pas été choisi —
   ce qui est le cas d'une session neuve.

Et lorsqu'il se termine, `[0x18070C510]` vaut `0x13` : **il mène à `VS` tout
seul, sans demander quoi que ce soit.**

---

## 9. Ce qui manquerait pour l'atteindre depuis le menu console : rien à écrire

Le milieu de `SELECTOR` (17) se termine par deux branches :

```
0x1800DB372  cmp  byte [0x180C3B701], al   ; game_mode
0x1800DB378  jne  0x1800DB438              ; != 0 : BORNE
             ; == 0 : CONSOLE
0x1800DB392  call 0x180186D40(0)
0x1800DB399  mov  ecx, 4
0x1800DB39E  call 0x1800DA9A0              ; -> mode 4 MENU
0x1800DB3A3  mov  al, 1 ; ret
             ; BORNE, 0x1800DB438 :
0x1800DB438  ... aucune demande ...
0x1800DB49A  mov  al, 1 ; ret              ; rend vrai, LA CHAÎNE FAIT LE RESTE
```

La **branche borne ne demande rien** : elle laisse la chaîne l'emmener vers
`MODE_SELECTOR`. C'est le chemin d'origine, et il est intact.

La branche console, elle, demandait le mode `MENU`. Le **maillon 2** de
`menu_console.md` §9.3 l'a remplacée par :

```
0x1800DB399  mov  ecx, 0x13
0x1800DB39E  call 0x1800DA9C0              ; -> sous-état 19 VS
```

ce qui **saute `MODE_SELECTOR`** : la demande explicite écrase le successeur de
chaîne. Le maillon a été posé parce que « le sous-état 19 `VS` n'est demandé
que par la sortie de `GAMEOVER` ; aucune première entrée » — constat exact sur
les *demandes*, mais la première entrée dans `VS` n'avait pas besoin d'une
demande : la chaîne du mode la fournissait.

**Il n'y a donc rien à fabriquer pour atteindre `MODE_SELECTOR` depuis le menu
console.** Deux options, l'une et l'autre à dix octets près :

| option | modification | effet |
|---|---|---|
| A | remplacer `0x1800DB399`–`0x1800DB3A2` par des `nop` | `SELECTOR` rend vrai sans rien demander → chaîne → `MODE_SELECTOR` → `VS` |
| B | ne rien toucher au maillon 2 | `SELECTOR` → `VS` directement, `MODE_SELECTOR` reste jamais emprunté |

Option A rétablit le parcours conçu. Coût prévisible : `MODE_SELECTOR`
n'affiche rien, ferme les sorties de secours pendant une à trois trames, écrit
`[session+0x58] = 0` et `[session+0x5C] = 0/1/2`, puis passe à `VS`. Deux
effets de bord à surveiller, dans cet ordre :

1. `[session+0x58]` cesse de valoir `-1` : l'arbitre `0x1800DB100` ne
   redemandera plus `MODE_SELECTOR` en fin de combat (c'est le comportement
   voulu, et c'est ce que fait aussi la sortie de `GAMEOVER`) ;
2. `[session+0x5C]` reçoit un tirage 0/1/2 issu de `0x1800B6A70`, que la
   branche « rejouer » de `GAMEOVER` écrit également (`0x1800DBA04`). On ne
   sait pas ce que ce champ commande — voir §11.

Avec le maillon 2 en place (option B), `MODE_SELECTOR` peut **tout de même**
tourner une fois : `[session+0x58]` vaut encore `-1` depuis la construction de
la session, et c'est exactement la condition que teste l'arbitre en
`0x1800DB22D`. Réserve : cette branche n'est atteinte que si
`0x1800244D0(session+0x4E0)` — c'est-à-dire `[session+0x4E8]` — vaut 1 (le
`cas 1` de `vs_gameover.md` §4), ce qui n'a pas été mesuré. Si c'est le cas,
`MODE_SELECTOR` tourne entre le combat et la suite sans que rien ne le montre à
l'écran ; sinon il ne tourne jamais.

---

## 10. Récapitulatif : le sous-état en une trame

| étape | ce qui se passe |
|---|---|
| entrée | `[0x180644634] = 1` ; `ctx+0x68C1 = 0` (sorties de secours fermées) ; rend vrai |
| milieu, phase 1 | 5 bouchons faux, 2 gardes vivantes ; passe en phase 2 |
| milieu, phase 2 | soit `0x1800B7BA0` (si `[session+0x15D0]` non nul), soit les deux joueurs en piste, soit la queue |
| milieu, queue | `[session+0x58] = (type == 3)` ; `[session+0x5C]`, `+0x60`, `+0x64` ; `0x1800B8540` ; rend vrai |
| sortie | arrête `DISP_JOIN` (qui n'a jamais été démarrée), un bouchon, rend vrai |
| après | `[0x18070C510]` vaut `0x13` : **`VS`** |

Aucun pixel, aucun libellé, aucune touche.

---

## 11. Ce qui n'est pas établi

* **Ce que `MODE_SELECTOR` affichait sur la version console d'origine.** Ce
  build n'en garde ni scène AET, ni libellé, ni page : le balayage des chaînes
  majuscules du binaire ne donne aucun nom de scène contenant « MODE ». On ne
  peut donc pas dire de quoi l'écran avait l'air ; on peut seulement dire ce
  qu'il n'y a plus.
* **Hypothèse, sans preuve** : les libellés `0x081` et `0x082` (« Two
  controllers are needed to play this mode. Press the START button on Player
  2's controller. ») et la scène `DISP_JOIN` que ce sous-état guette suggèrent
  un écran d'attente du deuxième joueur plutôt qu'un menu 1P/VS/entraînement.
  Rien dans le code des trois gestionnaires ne le confirme : aucun d'eux ne
  résout ces identifiants.
* **Ce que valent réellement les deux gardes vivantes de la phase 1** dans
  notre parcours (`0x1800B9020` et `0x1800B7850`). Elles dépendent du pont
  `apm.dll` et de `[session+0x1570]`, dont l'état à cet instant n'a pas été
  mesuré. Si l'une reste vraie, le sous-état s'installe au lieu de traverser.
* **`0x1800B7BA0`** (0xBF0 d'espace de pile, passe par `0x1801684F0` de la zone
  du sélecteur) et **`0x1800B8D30`** n'ont pas été lus. Ce sont les deux issues
  « riches » de la phase 2 ; on sait qu'elles rendent vrai et referment le
  sous-état, pas ce qu'elles font.
* **`0x1800B8540(session)`** (2026 o) : jamais ouverte, ici comme dans
  `couverture_console.md`.
* **Ce que commande `[session+0x5C]`** (le 0/1/2 de `0x1800B6A70`) et
  **`[session+0x60]` / `[session+0x64]`** (les deux `-1` de la branche type 3).
  Les écrivains sont recensés ; les lecteurs ne l'ont pas été.
* **Le sens exact du type de partie 3.** `vs_gameover.md` §2 propose « score
  attack / license challenge » sur la foi des sites qui le posent ; la branche
  B de la queue en dépend entièrement et n'a donc pas été validée.
* **Aucune contre-épreuve dynamique.** Rien n'a été lancé, rien n'a été patché.
  Tout ce document est de la lecture statique sur le binaire d'origine. En
  particulier, la prédiction du §9 — « `MODE_SELECTOR` tournera de toute façon
  une fois en fin de premier combat » — n'a pas été mesurée ; un compteur sur
  `0x1800DAE20` la trancherait en un essai.

Confiance : **SUPPORTED** pour tout ce qui est adressé et cité (bornes,
énumérations, chaînes de modes, sites d'écriture) — les énumérations reposent
sur un balayage linéaire de `.text`, pas sur `.pdata`. **UNKNOWN** pour tout ce
que la section ci-dessus énumère.
