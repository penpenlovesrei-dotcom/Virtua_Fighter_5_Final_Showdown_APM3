# Le texte 2D et l'AET : deux tuyaux, une seule liste de sommets

Établi le 2026-09-08, après quatre placements ratés du nom de variante sur
l'écran de sélection des décors. Ce document dit **ce qui a été lu dans le
code**, pour qu'on cesse de tâtonner.

> **Où est la vérité.** Les sections 5 et 7 sont **périmées** : elles
> cherchaient encore le bon *moment* d'appel, qui n'a jamais été le problème.
> La section 8 donne la chaîne complète et la formule de la clef ; la
> **section 9** donne la taille du tableau — c'est elle qui explique le
> plantage — et la **section 10 est le correctif en vigueur**.

---

## 1. Le tuyau du TEXTE : un dessin immédiat

```
0x18019B2E0(descripteur, drapeaux, format, ...)   enveloppeur type printf
  -> 0x18019B330    formate dans un tampon de 0x400, convertit (0x180019D10)
    -> 0x18019AC70  mise en page : lit le STYLE en [desc+0x48], ses metriques
                    et ses echelles (+0x14, +0x18, +0x24, +0x28, +0x2C, +0x30)
      -> 0x18019B4A0  emet les QUADS de glyphes : positions en r8/r9,
                      couleur eclatee en quatre octets depuis [rbp+0x7f]
```

Le descripteur fait 0x50 octets, construit par `0x18019A8C0` :

| champ | rôle |
|---|---|
| `+0x08` | couleur, `-1` = blanc opaque |
| `+0x0C` | seconde couleur, `0xFF808080` par défaut |
| `+0x34` `+0x38` `+0x3C` `+0x40` | x1 y1 x2 y2, **en pixels d'écran** |
| `+0x48` | le STYLE (0x40 octets, `0x18019A9D0`) |

Le style porte le mode (`0x18019B6F0`) et la taille (`0x18019B830`, qui divise
par les métriques de la police). Les champs `+0x24` et `+0x2C` que j'avais pris
pour un calque et une priorité sont **des flottants du STYLE** — des échelles,
lues en `0x18019AEDB` et `0x18019B075`. Ce ne sont pas des profondeurs.

Le mot de drapeaux (`0x28` au site « NOW LOADING ») n'est pas non plus un tri :
`0x18019AC70` le manipule bit à bit (`bt edx, 9`), et le balayage de tous les
appels du moteur rend 1, 2, 4, 8, 0x20, 0x21, 0x22, 0x28, 0x800 — de petits
jeux de bits d'alignement.

## 2. Le tuyau de l'AET : des objets ENREGISTRÉS

```
0x180171E90(ctx, index, id, nom, 0xF, 0x20000)
  construit une REQUETE de 0x108 octets (0x180029000)
    [req+0x00] = id      [req+0x08] = le nom
    [req+0x28] = 0x20000     [req+0x34] = 0xF
  -> 0x180029A90  resout l'identifiant contre le gestionnaire
    -> 0x180026790  INSERE dans un arbre, clef = un compteur croissant
```

Ce ne sont pas des dessins mais des **objets vivants**, que `AetMgr` rend
chaque trame.

## 3. L'ordre de la trame, MESURÉ

`tools/pister_ordre.py`, 120 événements consécutifs, parfaitement réguliers :

```
NOTRE DESSIN -> AetMgr creneau 4 -> AetMgr creneau 6 -> AetMgr creneau 2 -> ...
```

`AetMgr` passe **toujours après** le dessin d'une tâche. Totaux sur la mesure :
notre dessin 822 passages, les créneaux 2, 4 et 6 d'`AetMgr` 2449 chacun ; les
créneaux 0, 1 et 3 ne servent qu'à l'initialisation.

## 4. Les quatre essais, et ce que chacun a prouvé

| où | résultat | ce que ça établit |
|---|---|---|
| `TaskSelStage` créneau 4 | **visible, mais dessous** | le dessin marche depuis une tâche |
| `TaskSelStage` créneau 6 | rien | ce créneau n'est pas appelé |
| détour du créneau 4 de `TaskSelector` (qui dessine le panneau) | dessous | dessiner après le parent ne suffit pas : l'AET n'est pas rendu par une tâche |
| détour du créneau 2 d'`AetMgr`, le dernier | **invisible** | le tampon de texte est **consommé AVANT** ce point |

## 5. Une conclusion TROP RAPIDE — voir la section 7

> **Cette section est dépassée.** Elle concluait à l'impossibilité en se
> fondant sur l'absence de clef de tri commune. C'était vrai, mais sans
> conséquence : l'ordre ne vient pas d'une clef, il vient de **l'ordre
> d'insertion** dans la liste de sommets. Voir la section 7, écrite après être
> descendu jusqu'aux sommets.

Les deux tuyaux n'ont **aucune clef d'ordre commune** : la constante `0x20000`
que porte toute requête AET n'apparaît **nulle part** dans le code de dessin de
texte (balayage de `0x18019A800` à `0x18019C200`).

Et l'encadrement est clos par les deux essais extrêmes : avant `AetMgr` le
texte s'affiche mais passe dessous ; après `AetMgr` il ne s'affiche plus du
tout. **Il n'existe donc aucun instant de la trame où un dessin de texte
immédiat se retrouve au-dessus de l'AET.** Ce n'est pas un problème de
placement dans le code : c'est la structure du moteur.

## 6. Ce qui reste possible

1. **Placer le texte hors des zones couvertes.** C'est ce qui marche
   aujourd'hui : la plaque « Sanctuary / Single Wall 16x16 » couvre le rendu
   jusqu'à ~420, et le texte est net en dessous de ~448 (valeur `y = 490` dans
   la greffe, en `0x180EA1814`). **Périmé** : depuis le rang 127 le texte
   passe devant la plaque, et `y` est revenu à la position validée, 460.
2. **Effacer la couche AET qui recouvre**, plutôt que de passer devant. Le
   moteur sait déjà le faire : `--sans-now-loading` supprime un dessin en
   neutralisant son appel. Si l'on supprime la ligne « Single Wall 16x16 », la
   place se libère juste sous « Sanctuary » et notre texte s'y installe sans
   rien recouvrir. **C'est la voie la moins chère et la plus sûre.**
3. **Fabriquer la mention en AET**, pour qu'elle se trie avec la plaque. C'est
   la voie propre, mais elle demande de créer une composition et son art dans
   `spr_s_selstg.farc` / `aet_*`, puis de la livrer en fichier libre. Plusieurs
   séances.

~~Ce qu'il ne faut plus tenter : chercher un autre point d'accroche.~~
**Faux** : il restait exactement un point entre les deux extrémités, l'entrée
du créneau 2. Voir la section 7.

---

## 7. Le tuyau, jusqu'aux sommets (désassemblé le 2026-09-08)

> **Dépassée elle aussi — voir la section 8.** Elle cherchait encore le bon
> *moment* d'appel. Le moment n'a jamais été le problème : c'est le CALQUE.

La section 5 concluait trop tôt. En descendant jusqu'au bout, la structure est
plus simple que je ne l'avais dit — et elle laisse une place.

### Ce que fait chaque créneau d'`AetMgr`

| créneau | ce qu'il fait, lu dans le code |
|---|---|
| **4** (`0x1800235C0`) | parcourt la liste `[mgr+0x68]` et appelle le créneau `+0x18` de chaque objet AET — la **mise à jour** |
| **6** (`0x1800251A0`) | reparcourt `[mgr+0x68]`, appelle le créneau `+0x20`, et travaille sur `[mgr+0x78]` avec la constante `0xaaaaaaaaaaaaaa9` — la division par 24, donc **un vecteur d'éléments de 0x18 octets**. C'est l'**empilement** |
| **2** (`0x180023150`) | parcourt `[mgr+0x78]` — un arbre rouge-noir (`cmp byte [rcx+0x19], 0`) — et le **consomme** |

### Ce que fait le texte

`0x18019B4A0` construit les quatre sommets d'un glyphe et les **empile par
paquets de 0x18 octets** :

```
vmovups [rdx], xmm0          ; les 16 premiers octets du sommet
vmovsd  [rdx+0x10], xmm1     ; les 8 derniers
add     qword [rcx+8], 0x18  ; on avance la fin du vecteur
... et 0x1801067C0 quand il faut agrandir
```

**Même taille d'élément que ce qu'`AetMgr` manipule au créneau 6 : 0x18.** Les
deux écrivent des sommets dans la même forme de conteneur.

### Ce que l'encadrement dit, une fois relu

Les deux essais extrêmes ne disaient pas « c'est impossible », ils bornaient :

* **avant `AetMgr`** : le texte est empilé AVANT les sprites de l'AET, donc
  dessiné dessous. C'est de l'ordre d'insertion, pas de la profondeur ;
* **après le créneau 2** : le consommateur est déjà passé, la liste est vidée
  — rien n'apparaît.

Entre les deux, il reste **un seul point** : l'**entrée du créneau 2**, après
que le 6 a tout empilé et avant que le 2 ne vide. Notre texte y est le dernier
inséré, donc dessiné par-dessus. Et rien n'est retiré de l'écran.

### Le correctif

`--variantes-texte` détourne toujours `AetMgr` créneau 2, mais **dans l'autre
sens** : notre dessin d'abord, l'original ensuite.

```
0x180EA1500  push rbx ; push rsi ; sub rsp,0x28
             mov rsi, rcx                  ; on garde l AetMgr
             mov rax, [rip -> 0x180714928] ; le singleton TaskSelector
             test rax, rax ; je passe      ; nul hors de cet ecran
             lea rbx, [rax+0x3B0]          ; -> TaskSelStage
             call 0x180EA1300              ; NOTRE TEXTE, d abord
     passe:  mov rcx, rsi
             call 0x180023150              ; PUIS l original, qui vide
             ... ; ret
```

La version precedente faisait l'inverse — original puis dessin — et donnait un
texte invisible. C'est exactement ce que produit un ajout apres le vidage.

**Ce qui reste non prouve** : que le vecteur du texte et celui de l'AET soient
le meme objet. Les elements ont la meme taille et la meme forme, le vecteur du
texte est passe en pile depuis `0x18019AC70`, et je n'ai pas remonte jusqu'a
son proprietaire. L'encadrement empirique, lui, ne laisse pas d'autre position
a essayer.

---

## 8. TROUVÉ : la profondeur existe, elle est CALCULÉE

Les sections 5 et 7 tâtonnaient encore autour du *moment* de l'appel. Le moment
n'a jamais été le problème. En descendant jusqu'à l'insertion, voici la chaîne
complète du texte :

```
0x18019AC70   remplit un vecteur TEMPORAIRE de sommets ([rsp+0x30])
0x18019B187   lea rcx, [rbp-0x80]  ;  call 0x180189880   construit la COMMANDE
              cmd+0x04 <- la police ([[desc+0x48]+8])
              cmd+0x10 <- (desc+0x30 >> 3) & 2
              cmd+0x18 <- desc+0x28        cmd+0x1C <- desc+0x24
              cmd+0x20 <- desc+0x2C        cmd+0x24 <- desc+0x2C
0x18019B203   call 0x18018E620   y attache les sommets et leur nombre
0x18019B20C   call 0x180187C00   SOUMET au contexte 2D global (0x180719900)
                -> 0x18018CA20   INSERE
```

Et l'insertion calcule une clef :

```
0x18018CA2B  r15d = cmd+0x14
0x18018CA35  si r15d == -1  ->  r15d = [contexte + 0x828]     le CALQUE COURANT
0x18018CACC  rcx  = cmd+0x18
0x18018CAD3  r14  = cmd+0x1C ; inc r14
0x18018CADD  rcx += r15                 (le calque)
0x18018CAE0  rcx <<= 5
0x18018CAE4  r14 += rcx
0x18018CAE7  r14 <<= 4
0x18018CAEB  r14 += contexte            ->  [r14] = tete de liste, [r14+8] = compte
```

soit

```
clef = (desc+0x24) + 1 + ((desc+0x28 + calque) << 5)
```

et `contexte + clef*16` désigne un **compartiment**. Le rendu parcourt les
compartiments dans l'ordre : **clef plus grande = dessiné plus tard = au-dessus.**

### Pourquoi le texte passait toujours dessous

La commande du texte **ne pose pas `cmd+0x14`**. Il reste à `-1`, et
l'insertion retombe alors sur **`[contexte+0x828]`, le calque courant** — celui
que l'AET a monté avant de dessiner ses couches. Notre texte atterrissait donc
systématiquement dans un compartiment plus bas, **quel que soit le moment de
l'appel**. C'est pour cela qu'aucun point d'accroche ne marchait : ce n'était
pas une question d'instant, mais de calque.

## 9. Le premier correctif a PLANTÉ — et le tableau a une TAILLE

Premier correctif : monter `[contexte+0x828]` de 8 autour du dessin, puis le
rendre. Frédéric, 2026-09-08 : **« le jeu crash juste avant de pouvoir
sélectionner l'icône du décor de Dural »** — c'est-à-dire à la première trame
où la garde laisse passer et où `DESSINER` travaille vraiment.

La cause ne se devine pas, elle se lit — dans le **constructeur du contexte**,
`0x18018A030` :

```
0x18018A049  mov ecx, 0x838 ; mov edx, 0x10 ; call operator new
                                        le contexte pèse 0x838 octets
0x18018A092  call 0x1802FE160(rbx+0x10, taille=0x10, compte=0x80, ctor, dtor)
                                        128 compartiments de 16 octets, en +0x10
0x18018A097  [rbx+0x818] = 0 ; [rbx+0x820] = 0
             [rbx+0x828] = le calque courant
0x18018A0A5  0x180719900 = rbx
```

Le **`+1`** de la clef est donc exactement le décalage de `0x10` du tableau, et
l'indice réel vaut :

```
indice = (desc+0x24) + ((desc+0x28 + calque) << 5)      dans 0..127
```

soit **quatre calques de trente-deux rangs, et rien de plus**. Monter le calque
de 8 réclamait l'indice `8 + 8*32 = 264`, deux kilo-octets au-delà de l'objet :
`mov r13, [r14]` y lisait un pointeur de hasard. Le montant « modeste » de la
section 8 ne l'était pas du tout — **1 suffisait à sortir du tableau dès que le
calque courant valait 3.**

## 10. Le correctif retenu : un rang BORNÉ, aucun état global — **VALIDÉ**

> **Validé à l'écran le 2026-09-08.** Frédéric, sur capture : « c'est bon le
> texte est enfin au premier plan ». C'est désormais LA méthode pour poser du
> texte par-dessus une scène AET dans ce moteur.

On ne touche plus à `[contexte+0x828]`. On corrige **notre seul descripteur**,
juste avant les neuf passes :

```
mov rax, [rip -> 0x180719900] ; test rax,rax ; jz fin
mov ecx, [rax+0x828]          ; le calque courant
mov eax, [greffe+0x08]        ; le plafond, 3
cmp ecx, eax ; jg fin         ; deja au-dessus du tableau -> on renonce
sub eax, ecx                  ; plafond - calque
mov [desc+0x28], eax          ; le calque effectif vaut TOUJOURS 3
mov eax, [greffe+0x0C]        ; l'ordre, 31
mov [desc+0x24], eax          ; le dernier rang de ce calque
```

`indice = 31 + 3*32 = 127` : le **tout dernier compartiment**, parcouru en
dernier, donc dessiné par-dessus tout — et il ne peut pas sortir du tableau,
quelle que soit la valeur du calque courant. Rien n'est à restaurer : les
quatre sorties de `DESSINER` sautent directement à `add rsp,0x38 ; ret`.

Les deux champs sont à nous : le constructeur du descripteur (`0x18019A8E6`)
pose `+0x24 = 7` et `+0x28 = 0`, et `0x18019B1D0` / `0x18019B1D6` en sont les
**seuls lecteurs** — vérifié sur toute la plage `0x18019A8C0..0x18019B2E0`.

Le dessin reste au **créneau 4 de `TaskSelStage`**, là où le texte était déjà
visible ; `AetMgr` créneau 2 est rendu à son original. Ce qui manquait n'était
pas le moment, c'était le rang.

### Le réglage

| adresse | ce que c'est | défaut |
|---|---|---|
| `0x180EA1618` | plafond de calque — **ne pas augmenter** | 3 |
| `0x180EA161C` | rang dans le calque (0..31) | 31 |
| `0x180EA1620` / `0x180EA1624` | x, y | 640, **470** |
| `0x180EA162C` | taille de police | 24 |

Vérifié sur la DLL construite : `plafond=3`, `ordre=31`, indice final **127 sur
127**, et **aucun** mot de la greffe ne ressemble à une adresse absolue.

**Confirmé à l'écran** : le compartiment 127 passe bien au-dessus de l'AET.
La réserve écrite ici — « et si l'AET dessinait lui aussi en 127 ? » — est
levée.

**Les adresses ont bougé** depuis que la greffe porte quatre anneaux : les
réglages sont maintenant en `0x180EA1618`…`0x180EA162C`, la table d'indices en
`0x180EA1790` et les noms, à pas de **32** octets, en `0x180EA1820`.
