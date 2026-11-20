# LA BRUME D'ANNEAU D'AOI (`jin` / `jn5`) — CE QUI MANQUE, MESURÉ

Relevé le 2026-10-15. Tout est lu au désassembleur, rien n'est supposé.

## 1. Ce n'est pas le fichier de brouillard

`fog_jn5.txt` **est** lu et appliqué : forcé en rouge, la bande couvre l'étang,
le pont et le pied de la pagode. Final Showdown met ce même groupe à densité 0
dans `fog_jin.txt`, et quatre décors de FS s'en servent encore. La brume qui
manque est celle qui passe **devant les combattants** : c'est la tâche
`FOG_RING`, la seule autre que `jn5` demande.

## 2. Le défaut : une table à un seul enregistrement

    TaskEffectFogRing::pre_init     0x180072B60
        rbx = this + 0x58
        call 0x180072130(rbx, indice_decor)
        [0x180677B10] = rbx

    0x180072130(bloc, indice)
        [bloc]      = 1
        [bloc+0x04] = 1.0f      [bloc+0x08] = 1
        [bloc+0x58] = 0         [bloc+0x2B8] = 0
        cmp edx, [0x1806431C8]      <-- L'UNIQUE enregistrement
        jne 0x180072565             <-- tout autre decor : ON SORT
        ... les quinze parametres de la brume

La table `0x1806431C8` est dans `.data`, **statique, un seul enregistrement de
`0x3C` octets**, et il porte l'indice **22** — `du2`, l'arène de Dural. Pour
`jn5` (48) la fonction sort tout de suite : la tâche tourne avec cinq valeurs
par défaut et **aucun paramètre**. Rien n'est dessiné.

## 3. VF5 R en a DEUX, et le second est `jin`

Chez VF5 R la table est en **`.bss`** (`0x8BE4DE0`) : elle n'est pas dans le
fichier, elle est **écrite par un constructeur statique**, `0x84CCDE4`, qui
entre avec `edi = -0.12f`, `esi = 0`, `ebx = 1.0f` et pose les deux
enregistrements en clair (`0x84CCE99`..`0x84CCF9E`). La boucle de lecture, elle,
est en `0x84CBD4A` : `cmp [edx+0x8BE4DE0], esi / add edx,0x3C / sub ecx,1 / jns`
avec `ecx = 1` — **deux tours**.

L'ordre natif des décors de R donne l'indice **9 = `jin`** et **22 = `du2`**.

| champ | rôle lisible | `jin` (R, 9) | `du2` (R, 22) | APM3 (22) |
|---|---|---|---|---|
| +0x00 | indice du décor | **9** | 22 | 22 |
| +0x04 | actif (octet) | 1 | 1 | 1 |
| +0x08 | compte (va en +0x34 ET +0x38 du bloc) | 2000 | 2000 | 2000 |
| +0x0C | flottant | 16,0 | 16,0 | 16,0 |
| +0x10 | flottant | 0,4 | 0,4 | 0,4 |
| +0x14 | flottant | 0,0 | 0,0 | 0,0 |
| +0x18 | flottant | −0,12 | −0,12 | −0,12 |
| +0x1C | **identifiant de texture** | **15460** | 15650 | 15650 |
| +0x20…+0x2C | quatre flottants (RGBA ?) | 1 1 1 1 | 1 1 1 1 | 1 1 1 1 |
| +0x30 | flottant | 18,0 | 18,0 | 18,0 |
| +0x34 | flottant | 1,0 | 1,0 | 1,0 |
| +0x38 | flottant | **0,3** | 0,1 | 0,1 |

**L'enregistrement `du2` d'APM3 est celui de VF5 R, octet pour octet.** Celui
de `jin` a été retiré, et il ne diffère que par **trois champs** : l'indice,
`+0x1C` (15460 au lieu de 15650) et `+0x38` (0,3 au lieu de 0,1).

## 3 bis. Le champ `+0x1C` est l'identifiant de la TEXTURE de brume

La chaîne, lue bout à bout :

    0x180072100   si [this+0x58] != 0 :
                      0x1800ec7c0(rappel = 0x180072BA0, bloc, id_effet = 0x16)

    0x180072BA0   le rappel. Il monte l'effet, puis :
    0x180072C37       mov ecx, [rbx+0x1C]          ; rbx = le bloc
    0x180072C3A       call 0x1801957A0             ; -> rax
    0x180072C42       test rax, rax / je ...       ; absent -> on saute le reste

    0x1801957A0   recherche dans l'arbre rouge-noir de `[0x18074ADB8]` :
                  clé `uint32` en `+0x20`, valeur rendue en `nœud+0x28`, 0 si
                  absent. Le module qui tient cette carte est celui des
                  objsets (`'./rom/objset/'`, `'tex_db.bin'`, `'TXHD'`), et la
                  fonction voisine `0x180195800` lit `[valeur+0xC]` et
                  `[valeur+0xE]` en `word` avec décalage de mipmap : **ce sont
                  des textures**.

Résolus dans le `tex_db` d'APM3 — par l'IDENTIFIANT, pas par l'offset de pot,
ce qui m'avait d'abord donné des noms glissés :

| id | nom |
|---|---|
| 15459 | `F_VF5E_JIN00_MU_TUBU1` |
| **15460** | **`F_VF5E_JIN00_MU_TUBU2`** — la brume de `jin` |
| 15649 | `F_VF5E_DU2_MU_TUBU1` |
| **15650** | **`F_VF5E_DU2_MU_TUBU2`** — celle de `du2`, la seule servie |

`MU` est le préfixe des effets du décor, `TUBU` (粒) le grain de particule.

**Et la texture de `jin` est déjà chargée chez nous** : `stgjn5_obj.bin` (447
objets, 605 textures) porte **15459 et 15460**. Rien ne manque dans les
données — ni la texture, ni l'objset, ni le `tex_db`. Il ne manque que
l'enregistrement de la table.

## 4. RENVERSEMENT : le travail était DÉJÀ FAIT, et ce n'est pas la cause

**Le socle du 2026-10-08 pose déjà cet enregistrement.** Sa ligne, que j'avais
sous les yeux sans la lire :

> FOG_RING : l'appel 0x180072B80 → 0x180072130 passe par le stub 0x180EA55D0,
> qui recopie dans 0x1806431C8 (0x3C octets) le dossier de 48, sinon
> l'original de FS

Sa table, en `0x180EA5640`, porte **deux** dossiers de `0x3C`, et le premier
est, au bit près, ce que je venais de remesurer chez VF5 R :

| | dossier 0 | dossier 1 |
|---|---|---|
| +0x00 | **0x30 = 48** (`jn5`) | 0x16 = 22 (`du2`) |
| +0x1C | **15460** `F_VF5E_JIN00_MU_TUBU2` | 15650 `F_VF5E_DU2_MU_TUBU2` |
| +0x38 | **0,3** | 0,1 |

J'avais donc écrit un détour qui refaisait, moins bien, un travail en place
depuis une semaine. Il a été **retiré**, et la DLL repatchée depuis le socle
seul : `0x18007215C` est intact et `0x180072B80` appelle bien le stub.

### Ce que la sonde a mesuré, décor 48 forcé

* **le stub écrit** : point d'arrêt **matériel** sur `0x1806431C8`, un accès,
  valeur `0x30` = 48 ;
* **la texture est cherchée** : `0x180072C3A`, **1779 passages**, `ecx` =
  `0x3C64` = 15460 à chaque fois ;
* **et elle est TROUVÉE** : `0x180072C3F`, **4330 passages**, `rax` non nul
  (`0x159137F49F8`) ;
* donc `[bloc+0x58]` est non nul — sans quoi le rappel sortirait dès
  `0x180072BAD` — et le dessin est émis à chaque trame.

**Rien ne manque dans la chaîne des paramètres, et la brume n'apparaît pas à
l'écran.** La cause est ailleurs : dans le rendu lui-même, ou dans la position
des éléments.

## 5. FAUSSE PISTE, corrigée : `0x180072DC0` n'est pas FOG_RING

J'avais pris `0x180072DC0` pour la mise à jour de FOG_RING et lu, dedans, une
naissance de particules sur le déplacement des combattants, gardée par des
compteurs en `+0x8C` et `+0xA4`. **C'est faux.** Le RTTI MSVC le tranche :

    0x18034F6A0   TaskEffectFogRing
    0x18034EA40   TaskEffectHit      <- 0x180072DC0 est SON créneau 2

Les deux classes sont **entrelacées** dans le binaire — `0x180072100`,
`0x180072130`, `0x180072580`, `0x180072B60`…`0x180072D90` sont FogRing, et
`0x180072DC0`, `0x180072F80`, `0x180073080` sont Hit. D'où la confusion, et
d'où l'incohérence que j'avais relevée sans la comprendre : un pas de `0x18`
d'un côté, de `0x14` de l'autre, parce que ce sont deux objets différents.

**`+0x8C` et `+0xA4` n'existent pas dans FOG_RING. Il n'y a personne à
chercher.**

## 5 bis. La vraie forme de TaskEffectFogRing

    créneau  2   0x180071F50   init
    créneau  3   0x180072080   dest -- libère [this+0xA0] et [this+0xA8],
                               éteint la passe 4, remet [0x180677B10] à 0
    créneau  4   0x180072100   disp -- ne dessine que si [bloc+0x00] != 0
    créneau  7   0x180072B60   pre_init -- charge les paramètres
    créneau 11   0x180072D90
    créneau 13   0x180072D40   remise à zéro (le jumeau de 0x180072CF0,
                               l'un prend le `this`, l'autre le bloc)
    les créneaux 5, 6, 8, 9, 12, 14, 15 sont le bouchon `ret 0` 0x180007430

La **mise à jour** est `0x1800725A0` (hors vtable), gardée par
`cmp [bloc+0x38], 0 / jle` — et `bloc+0x38` reçoit `table+0x08` = **2000**,
donc la garde passe.

Le bloc porte **deux allocations**, faites par le chargeur lui-même :

    0x180072242  movsxd rdi, [bloc+0x34]      ; 2000, de table+0x08
    0x180072246  mov eax, 0x2C ; mul rdi      ; 2000 x 0x2C = 88 000 octets
    0x18007225C  call 0x180218930             ; l'allocateur

`bloc+0x48` est le tableau d'éléments, `bloc+0x50` celui des sommets que le
dessin lie en `0x180072C5C`. Les deux sont libérés par le destructeur.

Autrement dit : **la tâche est complète et alimentée**. Ce qui reste à lire,
c'est `0x1800725A0` jusqu'au bout — où les éléments sont placés, et avec
quelle taille — car c'est là que se joue la visibilité.

## 6. Ce qu'il faudra décider avant de poser quoi que ce soit

Ajouter un second enregistrement demande de toucher au **code**, pas seulement
aux données : le `cmp edx, [0x1806431C8] / jne` d'APM3 est une comparaison
**déroulée**, il n'y a pas de boucle à rallonger. Deux voies, aucune essayée :

* greffer une boucle à la place du `cmp/jne` (6 + 6 octets au site, la table
  recopiée dans `.decors` avec deux enregistrements) ;
* ou dérouter `0x18007215C` vers la greffe, qui rend l'enregistrement de `jn5`
  quand `edx == 48` et retombe sur le chemin d'origine sinon.

Mais tout cela est **caduc** : le socle pose déjà l'enregistrement, et la
mesure dit que les paramètres arrivent. Ce qui reste à chercher, c'est
pourquoi un dessin émis à chaque trame, avec la bonne texture, ne produit
rien à l'écran — en commençant par `0x18014452B`, le seul appelant de
l'accesseur du bloc.


---

# LE DÉCOR D'AOI, TEL QU'IL EST FAIT

Lecture du 2026-10-15, sans aucune mesure à l'exécution.

## A. Il y a DEUX brumes, et elles n'ont rien à voir

### 1. La brume d'arrière-plan — `fog_jn5.txt`

Trois groupes, et le fichier est **intact** : `diff` avec
`extracted/decors/VF5R/light_param/fog_jin.txt` ne sort rien, octet pour
octet. (Le test rouge du début de session portait sur le groupe 1 ; il a été
défait. Le `color 4.41 1.0 1.0 0.0` du groupe 2, qui a l'air d'un rouge
oublié, est d'origine : FS Lindbergh le porte aussi.)

| groupe | densité | linéaire | couleur |
|---|---|---|---|
| 0 | 0,6 | 0 → 100 | 0,70 0,90 1,00 |
| 1 | 1,0 | −2,5 → 1 | 0,70 0,90 1,00 |
| 2 | 1,0 | −100 → 16 | **4,41** 1,00 1,00 (alpha 0) |

Final Showdown met le groupe 1 à **densité 0** dans son `fog_jin.txt` ; VF5 R
le laisse à 1. C'est ce groupe qu'on voit à l'écran sur l'étang, le pont et le
pied de la pagode — vérifié en le forçant en rouge, puis défait.

### 2. La brume VOLUMÉTRIQUE — `MOYA` (靄)

Ce n'est pas du brouillard de distance : c'est un **objet 3D**.

    STGJN5_EFF_MOYA.a3da   (2821 octets, daté du 31/01/2008)
        object.0.name      = STGJIN_EFF_MOYA_000
        object.0.morph     = MOYA          <- morph, pas une texture animée
        curve.0.name       = MOYA          27 clés, oscillant 0 → 1 → 0
        object.0.rot.y     0 → 6,28319     une rotation COMPLÈTE
        play_control.size  = 7788 trames à 60 i/s, soit 2 min 10

Une nappe qui tourne lentement sur elle-même en se déformant. Ses deux poses
de morph sont dans l'objset : **`stgjin_eff_moya_000` (rang 444)** et
**`stgjin_eff_moya_001` (rang 445)**, sur 447 objets.

## B. Tout ce que MOYA demande est en place

| pièce | état |
|---|---|
| l'objet, deux poses | `stgjn5_obj.bin`, rangs 444 et 445 |
| l'animation | `EFFSTGJN5.farc`, `STGJN5_EFF_MOYA.a3da`, 2821 o — la taille de l'original |
| l'uid | **3532**, catégorie `EFFSTGJN5`, dans la base que le jeu lit |
| la liste d'animations du décor | table greffée, entrée 48 : `ARUKI_A, ARUKI_B, ARUKI_C, TALK, MOYA, -1` |

## C. Et Final Showdown joue DÉJÀ cette brume

Dans la table d'origine, l'entrée du décor `jin` (**indice 9**, celui du jeu,
pas notre variante) porte :

    1942  STGJIN_EFF_MOYA
    3348  STGJIN_EFF_TOUYAMA        (les montagnes lointaines)

L'uid 1942 n'apparaît **qu'une fois** dans tout le binaire. Donc la brume
volumétrique d'Aoi n'a pas été supprimée par le portage : elle est jouée sur
le décor d'Aoi de Final Showdown.

Deux écarts avec le nôtre, relevés sans verdict :

1. `jn5` demande **MOYA mais pas TOUYAMA** ;
2. les listes de **tâches** diffèrent complètement —

        9 jin : WALL, WET_CLOTH, RINGOUT_SPLASH, LEAF     (Final Showdown)
       48 jn5 : WALL, FOG_RING                            (VF5 R)

   `jn5` est fidèle à VF5 R, qui ne demandait que `WALL` et `FOG_RING`.

## D. Où en est `FOG_RING`, l'autre piste

C'est le système de **particules** de VF5 R, sans rapport avec MOYA. Sa chaîne
a été suivie de bout en bout et **elle fonctionne** : dossier de paramètres
posé par le socle, 2000 éléments alloués et semés dans un cube de 16, sources
de perturbation posées par les combattants, mise à jour, sommets, rendu dans
la cible 5, composition vers la cible 2, et la texture **liée au shader du
décor** dans la passe 7 (slot `0x22B`, 3698 passages mesurés).

Ce qui n'a pas été vérifié : que le **programme de fragments** du décor
échantillonne ce slot. C'est le même genre de verrou que pour l'eau d'Eileen.

## E. Les adresses greffées BOUGENT d'un patch à l'autre

Piège rencontré aujourd'hui : la table des tâches était en `0x180EB65F0`
avant un repatch, en **`0x180EB4DC0`** après. On ne note donc jamais ces
adresses — on les retrouve, et on vérifie le contenu (`slk` doit donner
`WALL, WATER_RING, RIPPLE, SPLASH`).


## F. LE BROUILLARD DE HAUTEUR EST UNE PERMUTATION DE SHADER, ET ELLE N'EST PAS CHARGÉE

### Ce que le shader fait

Dans les programmes ARB de Lindbergh FS (le même code que l'APM3), chaque
programme de fragments déclare **deux** couleurs de brouillard :

    PARAM p_fog_color        = program.env[4];
    PARAM p_height_fog_color = program.env[11];

et n'en emploie qu'**une**, selon la permutation :

    stage_blinn.00000000.fp :  LRP o_color.rgb, a_fogcoord.xxxy, p_fog_color, tmp;
    stage_blinn.00000020.fp :  LRP o_color.rgb, a_fogcoord.xxxy, p_height_fog_color, tmp;

C'est le **chiffre en avant-dernière position** de la clé qui décide, et le
seuil n'est pas le même partout :

| shader | chiffres | avant-dernier = brouillard de hauteur |
|---|---|---|
| `stage_blinn` | 8 | **2 ou 3** (0 et 1 = brouillard de distance) |
| `skin_default` | 8 | **1** |
| `cloth_default` | 9 (ARB) | **1** |

Exactement la moitié des permutations de chaque famille l'emploie : 96 sur 192
pour `stage_blinn`, 48 sur 96 pour `skin_default`, 96 sur 192 pour
`cloth_default` et `hair_default`, 64 sur 128 pour `item_blinn`.

### La table de présence, et ce qu'elle charge

Le chargeur `0x180175BF0` ne monte un programme que si une table d'octets le
dit. Le sous-shader fait `0x40` octets :

    +0x18  nb de programmes de SOMMETS   +0x1C  nb de FRAGMENTS
    +0x20  noms (vp)                     +0x28  noms (fp)
    +0x30  présence (vp)                 +0x38  présence (fp)

    0x180175D27  mov rax, [rbx+0x30]
    0x180175D2B  cmp byte ptr [rax+rbp], 0
    0x180175D2F  je  <suivante>              <- absente : on ne charge pas

Relevé dans la DLL produite :

| shader | fragments | chargés | **avec brouillard de hauteur** |
|---|---|---|---|
| BLINN (sous-shader 0) | 192 | 16 | **0** |
| BLINN (sous-shader 1) | 384 | 3 | **0** |
| ITEM | 128 | 29 | **0** |
| **STAGE** | 192 | 8 | **0** |
| **SKIN** | 96 | 24 | **0** |
| HAIR | 384 + 32 | 29 + 6 | **0** |
| CLOTH | 192 | 34 | **0** |

Les huit permutations de décor chargées sont `00100010`, `00110010`,
`00101010`, `00111010`, et les mêmes en `…11` : **l'avant-dernier chiffre vaut
1 partout**, jamais 2 ni 3. Pour `SKIN`, il vaut **0** sur les vingt-quatre.

**Aucun objet, décor ou personnage, ne peut donc recevoir le brouillard de
hauteur.** Les programmes existent dans l'archive ; c'est la table de présence
du binaire qui les écarte — le même verrou que pour l'eau d'Eileen.

### Ce que cela n'explique pas, et qu'il ne faut pas confondre

La bande bleutée visible sur `jn5` et absente de `jin` vient donc du
brouillard **de distance** (`p_fog_color`), pas de la nappe de hauteur : les
deux décors ne diffèrent que par la densité du groupe 1, et l'effet se voit.
Comment le moteur répartit ses trois groupes entre `env[4]` et `env[11]`
reste à lire.

Réserve : les noms de permutations d'APM3 et ceux des ARB de Lindbergh n'ont
pas toujours le même nombre de chiffres (`cloth_default` : 10 contre 9). La
transposition n'est sûre que pour `stage_blinn` et `skin_default`, où les deux
côtés en ont huit.


## G. MOYA : LA CHAÎNE DE DONNÉES EST ENTIÈRE, VÉRIFIÉE MAILLON PAR MAILLON

`--fog-hauteur` a été **retiré** (la DLL est repatchée sans lui) : le
brouillard de hauteur teinte les objets, il ne peut pas passer **devant** eux.
Ce qui passe devant est un objet, et c'est MOYA.

### La géométrie : une nappe qui couvre toute l'arène

Lue sur les **sommets**, pas sur la sphère englobante :

| maille | x | y | z |
|---|---|---|---|
| 0 | −1,0 → 17,9 | −0,6 → 4,1 | −16,0 → 3,3 |
| 1 | −17,7 → 3,3 | −0,5 → 5,1 | −18,0 → 1,0 |
| 2 | −17,7 → 1,0 | −0,0 → 5,9 | −3,4 → 15,8 |
| 3 | −0,9 → 17,9 | −0,3 → 6,3 | −1,0 → 17,9 |

Quatre quadrants, **36 × 36 unités**, montant à **6,3** — bien au-dessus de la
tête d'un combattant. Matériau `BLINN`, une texture : **16160 =
`F_VF5E_JIN00_IK_KUMO1`** (*kumo*, 雲, le nuage), présente dans l'objset.

### Les six maillons, tous vérifiés

| maillon | état |
|---|---|
| l'animation | `STGJN5_EFF_MOYA.a3da`, 2821 o, dans `EFFSTGJN5.farc` |
| l'uid | **3532**, catégorie `EFFSTGJN5`, dans la base que le jeu lit |
| la table d'animations du décor | entrée `{48, → liste}` en `0x180EB6660`, liste `ARUKI_A, ARUKI_B, ARUKI_C, TALK, MOYA, -1` |
| l'ordre | **celui de VF5 R**, relu dans son ELF : MOYA y est aussi le cinquième |
| la capacité | pas en cause : le décor 19 en a **7**, le 12 en a **6** |
| la résolution de l'objet | `STGJN5_EFF_MOYA_000` → objset **6156** (= `STGJN5`), id interne **449** ; l'objset porte cet id au rang 444 |

Le lecteur est `0x1800706B0` : il balaie la table par pas de `0x10` jusqu'au
terminateur `-1` (donc les entrées ajoutées sont bien vues), puis inscrit
chaque uid dans la liste de la tâche. Au passage, il porte les deux cas
particuliers que le socle a étendus : `cmp edx, 8` → `[this+0xB1]` et
`cmp edx, 0x28` → `[this+0xB0]`.

**Piège écarté** : les objets de l'objset de `jn5` s'appellent tous
`stgjin_*` (447 sur 447) alors que les animations demandent `STGJN5_*`. Ce
n'est **pas** un défaut : la résolution passe par `obj_db`, qui déclare les
447 noms `STGJN5_*` et les fait pointer sur les bons identifiants internes.
Le nom écrit dans le fichier objset n'est jamais consulté.

### Et pourtant

Rien à l'écran — et **pas davantage sur le décor d'Aoi d'origine** (`jin`,
indice 9), dont la liste est `MOYA, TOUYAMA` et qui n'est touché par aucun de
nos chantiers. Sa capture le montre : ciel clair, eau verte, aucune nappe.

Le défaut n'est donc ni dans notre import, ni dans les données : **ces objets
d'effet ne sont pas rendus dans APM3**. Même constat que pour `FOG_RING`,
dont la chaîne entière fonctionne jusqu'à la liaison de sa texture au shader
du décor.

## H. LA FILE TRANSLUCIDE : VÉRIFIÉE, ET ÉCARTÉE

MOYA **est** translucide, c'est établi par son matériau :

    +0x3D4 = 0x00000A81    bit 0 = 1 (mélange), bit 2 (veto) = 0,
                           bit 28 (opaque) = 0 ; source 4, destination 5
    nom du matériau : « CZ_kumo_mawari » -- le tour du nuage

Le répartiteur `0x1800EB71B` l'envoie donc du côté translucide. Mais la borne
de 40 **ne le concerne pas**, et le détail compte :

    0x1800EB759  test ecx, 0x7E00000   ; les bits 21..26 du mot de mélange
    0x1800EB75F  jbe 0x1800EB7F0       ; aucun posé -> AUTRE chemin
    0x1800EB765  r9 = le compte courant
    0x1800EB76A  cmp r9, 0x28          ; 40
    0x1800EB76E  jge <on jette>
    0x1800EB774  rax = r9 * 0x1A0      ; l'enregistrement, sur la PILE

Les bits 21 à 26 de `0x00000A81` sont **nuls**. MOYA prend donc toujours
`0x1800EB7F0`, et la file de 40 enregistrements de `0x1A0` ne le voit jamais.
**La piste est fausse.**

### Le chemin qu'il prend réellement

    0x1800EB7F0  test byte [r11+0x78], 4   / jne  -> liste
    0x1800EB7F7  bt r9d, 0xc               / jb   -> liste
    0x1800EB7FE  sinon : call 0x1800EAB60(1, rbx)   -- dessin direct
    0x1800EB810  liste : rdi = rdx+0x70
                 call [rax+8]              -- alloue un maillon
                 si rax == 0 -> ON SAUTE, sans un mot
                 chaînage, puis inc [rdi+0x28]

### Le pool de maillons : pas de borne dure

L'allocateur appelé en `0x1800EB81D` est virtuel (`call [rax+8]`). Le seul
allocateur à pool du RTTI est **`pxd::csl_allocator_with_pool`**
(vtable `0x1805B0428`, créneau 1 = `0x1802871C0`), et il se lit ainsi :

    0x1802871D8  cmp rdx, [rcx+0x18]   ; la taille demandée vs celle des blocs
    0x1802871DC  ja  <repli>           ; trop grand : on passe au repli
    0x1802871DE  rcx = [rcx+0x10]      ; le pool
    0x1802871E2  call 0x1802873C0      ; prendre un bloc
    0x1802871E7  test rax, rax / jne   ; obtenu : on rend
    0x1802871EC  rcx = [rdi+8]         ; L'ALLOCATEUR DE REPLI
    0x1802871F9  call [rax+8]          ; et on lui demande

Le pool lui-même (`0x1802873C0`) est une **liste libre** à pointeur taggé
(compteur ABA sur les seize bits de poids fort) : `[rcx]` la taille de bloc,
`[rcx+8]` la tête ; tête nulle, il rend 0.

**Donc l'épuisement du pool ne jette rien** : il y a un repli, et l'objet
n'est perdu que si les DEUX allocateurs échouent. La capacité du pool n'est
pas une borne dure, et elle n'est pas lisible en statique -- elle est fixée à
la construction, dont le seul site est `0x180287154`.

**Réserve honnête** : je n'ai pas pu confirmer, sans exécuter, que
l'allocateur de `0x1800EB81D` est bien celui-là. Ce qui est sûr : MOYA ne
passe pas par la file de 40, et son chemin n'a pas de borne fixe.

Ce qui trancherait en une passe : un point d'arrêt sur `0x1800EB820`
(`test rax, rax / je`). S'il est atteint avec `rax` nul, l'objet est jeté
faute de maillon ; sinon il est bien mis en liste, et le défaut est en aval.


## I. LE CODE DE LINDBERGH, ET UNE PISTE QUE J'AI CRUE BONNE

### Le chemin complet, comparé

| | VF5 R (Lindbergh) | APM3 |
|---|---|---|
| lecteur de la table d'animations | `0x84B8D66`, pas **8** | `0x1800706B0`, pas **0x10** |
| cas particuliers | décors **8** et **0x27** (39) | décors **8** et **0x28** (40) |
| garde de capacité | `cmp [edi+0x50], ebx` | `cmp [rbx+0x58], rax` |
| création d'instance | `0x829A0E4` | `0x18003C370` |
| test de validité | `0x8294494` | `0x180041A80` |
| **borne d'instances auth_3d** | `cmp edx, 0x40` → **64** | `cmp rax, 0x60` → **96** |
| taille d'une instance | `0x1A0` | `0x2C8` |

Le code est **le même**, et sur le seul point où les deux diffèrent, APM3 est
**plus large** que VF5 R. Aucune amputation sur ce chemin.

Ce qu'on en retient quand même : la création d'instance exige que la
description soit chargée —

    0x18003C3BE  cmp dword ptr [rax+4], 0 / je -> ECHEC

— et si elle échoue, `0x180041A80` rend « faux » et l'animation est **sautée
sans un mot**. Encore un échec muet.

### La table des 93 archives : une fausse piste, et pourquoi

Le binaire porte en **`0x18054E180`** une table de **93 enregistrements de
`0x10`** : `{pointeur vers "auth_3d/<nom>", un nombre}` (238 pour
`effstgjin`, 648 pour `effstghai`). Elle liste les décors d'origine —
`effstgjin`, `stgjin`, et vingt autres — et **aucun** des dix-neuf ajoutés.
Le socle ne la touche jamais : il déclare nos archives dans la BASE
(catégorie `EFFSTG<CODE>`), pas dans le binaire.

J'en ai conclu que nos archives n'étaient jamais chargées. **C'était faux**,
et deux signes auraient dû m'arrêter avant :

* la table n'a **aucune référence RIP ni aucun pointeur** dans tout le
  binaire -- je ne savais même pas qui la lisait ;
* il existe un chargement **dynamique** : `0x180038661` concatène
  `"rom/auth_3d/"` et le nom pris en `[rdi+0xE0]`.

La sonde a tranché en deux minutes :

    fichier : .../rom/auth_3d/EFFSTGJN5.farc
    fichier : .../rom/auth_3d/STGJN5.farc

**Les deux archives de `jn5` sont bien ouvertes.** La table des 93 ne commande
pas le chargement ; son rôle reste inconnu. Ne pas y revenir sans savoir qui
la lit.

### Donc, à ce stade

Cinq pistes examinées, cinq écartées : la file translucide de 40, la capacité
de la liste d'animations, le pool de maillons, la borne d'instances, et le
chargement de l'archive. Les données sont entières, l'archive est lue, et le
code de référence est identique.

Le maillon suivant, et il se mesure en une passe : l'animation est-elle
**inscrite** ? Un point d'arrêt sur `0x180070740` (`test al, al`, juste après
l'appel au test de validité) le dit — `al` à 0 signifie que l'instance n'a pas
été créée.


## J. CE N'EST PAS MOYA, C'EST LE BROUILLARD DE HAUTEUR

### Ce que montrent les captures de la borne

Frédéric a fourni deux captures de la version Lindbergh. La brume n'y passe
pas **devant** les combattants : c'est une **nappe qui noie tout l'espace
jusqu'à une altitude donnée**. Les troncs disparaissent par le bas, les
piliers de la pagode sont mangés à mi-hauteur, l'eau n'existe plus, et le
plancher du ring **émerge** juste au-dessus. Signature d'un brouillard de
hauteur, pas d'une géométrie — et le fichier le disait :

    group_start 1 / density 1.0 / linear -2.5 1.0

La nappe monte jusqu'à `y = 1`, le plancher est juste au-dessus. FS met ce
groupe à densité 0, VF5 R à 1.

**MOYA n'est donc pas la cible.** La section G reste vraie (ses données sont
entières, il est inscrit, instances 3 à 7) mais c'est un autre sujet.

### Le vertex shader change de formule, pas seulement le fragment

C'est la pièce que j'avais manquée, et elle explique l'essai raté :

    stage_blinn.00000010.vp :
      SUB _tmp0.w, pos_c.z, state.fog.params.y     <- la PROFONDEUR (z caméra)
      MUL_SAT _tmp0.w, _tmp0.w, state.fog.params.w
      MUL o_fog.x, _tmp0.w, state.fog.params.x

    stage_blinn.00000020.vp :
      SUB _tmp0.w, -pos_w.y, program.env[14].y     <- la HAUTEUR (y monde)
      MUL_SAT _tmp0.w, _tmp0.w, program.env[14].w
      MUL tmp.y, _tmp0.w, program.env[14].x

Le chiffre de permutation commande donc **quatre** modes, et on les lit :
`0` sans brouillard, `1` distance (`state.fog.params`), `2` hauteur
(`env[14]`), `3` sans doute les deux.

### L'essai du 2026-10-16, et pourquoi il a effacé la brume

Les deux moitiés posées (8 permutations **fragment** chargées, état 22 à 2
aux deux sites `0x1800F2FB4` et `0x1800F278A`), la DLL relue au
désassembleur : **la brume a disparu au lieu d'apparaître**.

Cause, et le symptôme y collait exactement : le **fragment** basculait sur
`p_height_fog_color` (`env[11]`) pendant que le **vertex** continuait à
calculer la profondeur, et que ni `env[11]` ni `env[14]` n'étaient alimentés.
Une couleur nulle appliquée à une coordonnée valide : plus de brume du tout.

Essai **annulé**, état 22 revenu à 1.

### Le code du brouillard de hauteur est ENTIER dans APM3

    env[11] -- la couleur :
    0x1800F290E  lea ecx, [rdx+7] ; call 0x1802475B0   ; on pose le paramètre
    0x1800F2916  mov ecx, 0xB     ; call 0x180247430   ; on marque env[11]

    env[14] -- les paramètres de la nappe :
    0x1800F29FB  lea ecx, [rdx+0xB] ; call 0x1802475B0
    0x1800F2A03  mov eax, [rdi+0x1C]    ; les drapeaux
    0x1800F2A0A  test al, 0x20          ; LE BIT 5
    0x1800F2A0C  je  <on saute>         ; à 0 : env[14] n'est jamais marqué
    0x1800F2A0E  mov ecx, 0xE  ; call 0x180247430

`0x180247430(i)` marque l'entrée `i` d'un tableau d'env
(`[contexte + i*0x20 + 0x757E8] = 1`). Ses appelants emploient les index
1, 3, 5, 6, 7, 8, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF — l'énumération des `env`.

**Rien n'a été amputé.** Il manque que deux conditions soient réunies, toutes
deux dans le même champ `[rdi+0x1C]` :

* **bit 5 (`0x20`)** autorise `env[14]` ;
* **bit 8 (`0x100`)** fait écrire l'état 22 — mais avec la valeur **1**.

### Ce champ `[rdi+0x1C]`

`rdi = [rcx+8]`, et `rcx` est un contexte de dessin : les cinq appelants de
`0x1800F2470` sont des dessins (`0x180085696` est dans
`TaskEffectWaterRing`, `0x1800F129B` et `0x1800F19E1` dans le module de
rendu). Ce n'est **pas** le matériau : sur les 467 matériaux de `jn5`, seuls
84 portent le bit 8, tous des `WATER02`, et ni le sol ni le ciel ne l'ont.

La fonction jumelle `0x1800F2B30` lit le même champ en `[rsi+0x1C]`.


## K. LES QUATRE POINTS SONT POSES ET ILS MARCHENT

`--fog-hauteur` est **en place** dans `tools/patch_moteur.py`, avec son
lanceur `tools/brume_aoi.cmd`. Quatre points :

| | site | avant | apres |
|---|---|---|---|
| le saut qui prive `env[14]` de sa validation | `0x1800F2A0C` | `74 51` | `90 90` |
| l'etat 22, constante | `0x1800F2FB4` | `…01000000` | `…02000000` |
| l'etat 22, via `r12d` | `0x1800F278A` | `41 BC 01…` | `41 BC 02…` |
| les permutations | table de presence | 2 vp, 8 fp | **4 vp, 16 fp** |

**Et ils fonctionnent** : le decor emprunte bien la permutation 2. La preuve
est dans la comparaison des deux essais --

* avec l'etat a 2 **sans** les programmes de sommets : la brume DISPARAIT
  (le fragment lisait une couleur vide pendant que le sommet calculait la
  profondeur) ;
* avec les quatre points : **le brouillard revient**.

Ce qui reste est donc la seule **valeur** d'`env[14]` : avec les parametres
du groupe 0 (`0 -> 100`) on obtient ce qu'on voit, un brouillard lointain ;
avec ceux du groupe 1 (`-2,5 -> 1`) on aurait la nappe au ras du sol.

### Le descripteur d'`env`, decode

Le contexte de rendu est un pointeur global en **`0x180C414F8`**
(`0x180253C90` : `mov rax, [rip+…] ; ret`). Les descripteurs d'`env`
commencent a **`contexte + 0x757E0`**, par pas de **`0x20`** :

| champ | role | lu a l'execution (env[14]) |
|---|---|---|
| `+0x00` | taille | `0x18` |
| `+0x08` | le marquage, pose par `0x180247430` | 0 puis 1 |
| **`+0x10`** | **l'offset de la donnee** | `0x10` puis **`0x20`** |
| **`+0x14`** | **le nombre de composantes** | 4 puis **2** |
| `+0x18` | le type | **`0x161`** = flottant (cf. `cmp r8d, 0x161 / mov esi, 4` en `0x180246B30`) |

Les deux derniers recoupent le code au mot pres : l'appelant d'`env[14]`
passe `edx = 2` (`lea edx, [r9+2]`, `0x1800F29F7`), et on lit bien 2.

### Ce qui reste a trouver : le buffer

Deux fausses pistes, ecrites pour ne pas les refaire :

* **`[descripteur+0x20]` n'est pas un pointeur.** J'avais lu
  `mov qword [r15+0x20], rax` (`0x180246BD3`) comme tel ; `rax` y est
  l'argument d'**offset**. La sonde l'a dit en une passe : « le descripteur
  ne porte aucun pointeur », puis « 0x40 illisible » (0x20 + 0x20).
* **`contexte + 0xD7B50` n'est pas le buffer.** On y lit `1 0 0 0` puis
  `0 0 1 0` a `+0x20` : les lignes d'une matrice identite.

### L'outil ajoute : la lecture indirecte

`tools/sonde_decor.py` accepte desormais, en troisieme champ de `--bp` :

    0x180715498                direct, une adresse de la DLL
    *0x180C414F8+0x759A0       INDIRECT : [A] + B
    **0x180C414F8+0x759C0+0x20 DOUBLE   : [[A]+B] + C

et rend quatre mots en hexa ET en flottant -- c'est le flottant qui
distingue `-2,5 -> 1` de `0 -> 100`. Sans lui, toutes les structures du
moteur restaient hors de portee : elles vivent au bout d'un pointeur global,
jamais a une adresse fixe. Sauvegarde : `sonde_decor.py.avant_indirect`.


## L. LA GREFFE REMPLIT LES DEUX REGISTRES -- ET L ECRAN NE CHANGE PAS

`--fog-hauteur` porte desormais, en plus des quatre points, un relais greffe
(`FGH_*`, zone `CPL_FGH`, 131 octets) pose sur `0x1800F2A0E` (`mov ecx, 0xE`,
cinq octets) et rendant la main en `0x1800F2A13`. Il ecrit les deux registres
et pose les bits de renvoi :

    contexte = [0x180C414F8]
    env[11] <- contexte + 0xD8AB0 : 0,70  0,90  1,00  1,00
    env[14] <- contexte + 0xD8AE0 : 1,00  -1,00  0  0,285714
    [[contexte]+0x38] + 0x420 |= 0x4800        (bits 11 et 14)

L adresse d un `env` est `contexte + 0xD7B50 + (index + 0xEB) * 0x10`, lue en
`0x1802512F2` (`lea rax, [rsi+0xEB] ; shl rax, 4 ; add rax, rdi`).

**Les deux ecritures sont VERIFIEES a l execution** -- premier passage a zero
(la greffe n a pas encore tourne), puis stables :

    env14 : 3F800000 BF800000 00000000 3E924925  =  1  -1  0  0,285714
    env11 : 3F333333 3F666666 3F800000 3F800000  =  0,7  0,9  1  1

**Et Frederic ne voit aucune nappe.** Les valeurs sont donc justes en memoire
et n arrivent pas au GPU : il manque le TELEVERSEMENT. Le bit pose reproduit
pourtant `0x1802512C0` a l identique. Deux explications a departager :

* le moteur remet `[rdx+0x420]` a zero avant d en tenir compte ;
* le renvoi effectif se fait plus loin, apres `0x180251329` (`test cl, cl /
  je`), partie non lue -- c est la que `cl` vaut 1 quand la boucle de copie a
  change un mot, donc c est le candidat le plus probable.

### Ce qui reste vrai et acquis

* les quatre points marchent (le decor emprunte la permutation 2) ;
* les deux registres sont remplis, aux bonnes adresses, avec les bonnes
  valeurs ;
* il ne manque donc QUE l envoi au GPU.

### L ecart 13/14, leve

Le moteur MARQUE d abord, POSE ensuite, et chaque registre a sa paire :

    0x1800F29BA  mov ecx, 0xD           marque env[13]
    0x1800F29FE  lea ecx, [rdx+0xB]=13  pose   env[13]
    0x1800F2A0E  mov ecx, 0xE           marque env[14]
    0x1800F2A53  lea ecx, [rdx+0xC]=14  pose   env[14]

J avais apparie la pose d env[13] avec le marquage d env[14]. Les adresses
calculees etaient bonnes malgre cette erreur.


## M. LA CHAINE DE RENDU EST EN DEUX BINAIRES

`--fog-hauteur` a ete **entierement annule** (patcheur restaure, DLL
repatchee, lanceur supprime) : `0x1800F2A0C` porte de nouveau son `je`, et
l etat 22 vaut 1.

### Le temoin qui a tout retourne

`env[4]` est `p_fog_color`, la couleur du brouillard de DISTANCE -- celui
qu on voit a l ecran. Lu a l execution dans le tampon que j avais trouve :

    env[4]  : 00000000 00000000 00000000 00000000
    env[12] : 00000000 00000000 00000000 00000000

**Zero.** Un registre qui FONCTIONNE est vide dans ce tampon : ce n est donc
pas celui que le GPU lit, et la greffe ecrivait dans une zone inerte (elle
ecrivait juste, aux adresses visees, avec les bonnes valeurs -- verifie --
mais au mauvais endroit).

### Pourquoi : il y a DEUX binaires

| binaire | role |
|---|---|
| `vf5fs-pxd-w64-Retail_APM3.dll` (7,2 Mo) | la logique du jeu et une API de rendu ABSTRAITE : les descripteurs d `env` (offset, compte, type), les shaders, les permutations |
| **`vfes.exe`** (2,0 Mo) | la couche **Direct3D 11** |

Preuve : la DLL n a **aucune** chaine `d3d11`/`dxgi` et un seul import
graphique (`D3DReflect` de `d3dcompiler_47`), tandis que `vfes.exe` importe
**`d3d11.dll`, `dxgi.dll` et `d3dcompiler_47.dll`**.

La DLL ne tient donc que la DESCRIPTION des constantes ; les valeurs vivent
dans un constant buffer que `vfes.exe` remplit. C est pour cela que
`contexte + 0xD7B50 + (i + 0xEB) * 0x10` est inerte.

### Ou reprendre

Dans **`vfes.exe`** : la fonction qui lit les descripteurs d `env` de la DLL
et remplit le constant buffer D3D11. Elle existe forcement, puisque le
brouillard de distance arrive a l ecran. Tout notre outillage vise la DLL --
`vfes.exe` est quasiment vierge pour nous.

Et ce qui reste acquis, a ne pas refaire : les quatre points (permutations
chargees + etat 22 a 2) donnent bien au decor la permutation « brouillard de
hauteur ». Il ne manque que l alimentation de `env[11]` et `env[14]`.


## N. LA FONCTION QUI REMPLIT LE CONSTANT BUFFER : `vfes.exe` 0x14002F430

`vfes.exe` : x64, base `0x140000000`, `.text` de 0x131ED3. Ses seuls imports
graphiques : `D3D11CreateDeviceAndSwapChain`, `CreateDXGIFactory1`,
`D3DReflect` -- ce dernier dit qu il REFLECHIT les DXBC pour retrouver leurs
constantes.

Aucun `UpdateSubresource` : le moteur remplit ses tampons par `Map`/`Unmap`
(12 et 8 sites). Un seul bloc reunit Unmap, VSSetConstantBuffers et
PSSetConstantBuffers -- c est la fonction, `0x14002F430` (1014 octets) :

    0x14002F460  rax = [rdi+0x38]
    0x14002F464  r13 = [rax+rdx+8]           ; LE MASQUE des registres « sales »
    0x14002F4A0  bsr rax, r13                ; le bit le plus haut
    0x14002F4BC  btr r13, rcx                ; on l efface
    0x14002F4C0  ecx = r8 + rdx              ; l index du registre
    0x14002F4C4  rbp = [rax + rcx*8 + 0x18]  ; son descripteur, un QWORD EMPAQUETE
    0x14002F4D0  esi = bpl                   ; champ de 8 bits
    0x14002F4DD  r14 = (rbp >> 16) & 0xFFF   ; champ de 12 bits
    0x14002F4E4  r15 = rbp >> 24
    0x14002F4EF  call 0x140036E20            ; -> le slot
    0x14002F53E  call [ctx+0x70]             ; Map
    0x14002F5E0  vmovdqu xmm0,[rcx]          ; la COPIE, 16 octets a la fois
    0x14002F5F2  vmovntdq [rdx],xmm0
    0x14002F60E  call [ctx+0x78]             ; Unmap
    0x14002F611  mfence
    0x14002F65D  call [ctx+0x38]             ; VSSetConstantBuffers
    0x14002F69F  call [ctx+0x80]             ; PSSetConstantBuffers

**C est le pendant exact du bit que la DLL pose** (`[rdx+0x420] |= 1 << i`,
`0x1802512C0`). La methode « ecrire la valeur, puis marquer » etait donc la
bonne ; c est l adresse d ecriture qui etait fausse.

### D OU VIENNENT LES OCTETS COPIES

    0x14002F557  r8 = [rdi+0x38]        ; la structure d etat du rendu
    0x14002F560  r14d <<= 4             ; champ 12 bits x 16 = la TAILLE en octets
    0x14002F564  r15 &= 0xFFFFFFF0      ; champ >>24, aligne 16 = l OFFSET
    0x14002F567  r8 += 0x420            ; <<< LE BUFFER commence a +0x420
    0x14002F571  r8 += r15              ; + l offset propre au registre
    0x14002F574  r9 = taille / 16       ; le nombre de lignes de 16 octets

**La source est `[rdi+0x38] + 0x420 + offset`**, l offset et la taille venant
du descripteur empaquete du registre (`[rdi+0x38] + 0x18 + index*8`).

### La chaine entiere, nommee

    la DLL   decrit   : index, count, type        -> un descripteur
    la DLL   marque   : un bit « ce registre a change »
    vfes.exe parcourt : le masque de bits
    vfes.exe lit      : [etat+0x420 + offset], `taille` octets
    vfes.exe copie    : vers le constant buffer mappe, Unmap, Set*ConstantBuffers

### LE PIEGE QUI M A FAIT TOURNER EN ROND

L offset **0x420 est le meme des deux cotes**, mais pas sur le meme objet :
dans la DLL (`0x1802512C0`) c est un CHAMP DE BITS, dans `vfes.exe`
(`0x14002F567`) c est le DEBUT DES DONNEES. Deux structures distinctes, un
offset identique. Ne plus confondre.

### Pour ecrire nos valeurs

1. localiser la structure `[rdi+0x38]` de `vfes.exe` ;
2. lire les descripteurs d `env[11]` et `env[14]` pour en extraire leurs
   offsets (bits 24+, alignes 16) et leurs tailles (bits 16-27, x16) ;
3. ecrire les flottants a `+0x420 + offset` ;
4. marquer les bits.

Plus aucune inconnue de structure.


## O. LA STRUCTURE EST LOCALISEE -- ET LES DEUX LECTURES SE REJOIGNENT

La sonde sait desormais armer dans **`vfes.exe`** : elle reconnait le module a
la base preferee de l adresse (0x140000000 l exe, 0x180000000 la DLL) et
choisit toute seule, sans syntaxe de plus. Elle affiche aussi `rdi`, `rsi` et
`r8`. Sauvegarde : `sonde_decor.py.avant_exe`.

Point d arret sur `0x14002F55B`, juste apres `mov r8, [rdi+0x38]` :

    rdi = 0x1F96EF48E40   CONSTANT      -> l objet renderer de vfes.exe
    r8  = 0x1F974B3CF40   CONSTANT      -> [rdi+0x38], la structure d etat
    rsi = 5, 6, 9, 0xC, 0xD, 0x1D, ...  -> les index des registres pousses

### Les deux lectures decrivaient la MEME zone

La DLL calcule `rdx = [[contexte]+0x38]` (`0x1802512B1`) et `vfes.exe`
calcule `r8 = [rdi+0x38]` (`0x14002F557`) : **c est le meme objet**. Donc :

    [etat + 0x420]           le MASQUE de bits      (ecrit par la DLL, 0x1802512D4)
    [etat + 0x420 + offset]  les DONNEES du registre (lu par vfes.exe, 0x14002F571)

L offset est aligne a 16 (`r15 &= 0xFFFFFFF0`) donc toujours >= 0x10 : les
premiers octets portent le masque, les donnees suivent. Ce que je prenais
pour deux structures contradictoires est une seule zone vue des deux cotes.

**La greffe posait donc le bit au bon endroit depuis le debut.** C est
l ecriture des valeurs qui tombait a cote : `contexte + 0xD8AB0` au lieu de
`[[contexte]+0x38] + 0x420 + offset`.

### Tout ce qu il faut pour ecrire, en un endroit

| quoi | ou |
|---|---|
| le contexte | `[0x180C414F8]` |
| l etat | `[[contexte] + 0x38]` |
| le descripteur du registre `i` | `[etat + 0x18 + i*8]`, un qword empaquete |
| son offset | `(descripteur >> 24) & 0xFFFFFFF0` |
| sa taille | `((descripteur >> 16) & 0xFFF) * 16` |
| ses donnees | `etat + 0x420 + offset` |
| le masque | `etat + 0x420`, bit `i` |


## P. OU EN EST LE CHANTIER (il n est PAS clos)

> Le 2026-10-18 j avais intitule cette section « le chantier s arrete ici ».
> **Frederic ne l a jamais demande**, et ce n est pas a moi d en decider. Il
> avait dit « ensuite on passe sur le chantier du mode quest » -- passer a
> autre chose, pas abandonner. J avais aussi annule la greffe de ma propre
> initiative. Corrige.

La greffe corrigee ecrit a `[[contexte]+0x38] + 0x420 + offset`, l offset
relu dans le descripteur du registre. Le relais a ete **relu au
desassembleur** : adresses bonnes, sorties bonnes, registres sauves et
rendus. **Frederic : aucun changement a l ecran.**

### Un defaut attrape par la relecture, et qui valait la regle

La premiere version du relais portait trois `je` COURTS vers une sortie
situee a 174 octets. Un saut court ne porte que 127 : le deplacement passait
NEGATIF et les trois sauts partaient **en arriere, dans du code quelconque**.
Jamais lance -- la relecture au desassembleur l a vu avant. Corrige en
`0f84` + disp32.

### Ce qui est etabli, et qui ne sera pas a refaire

* la brume d Aoi est un brouillard de **HAUTEUR**, pas un objet (captures de
  la borne) ;
* son chiffre de permutation change les **deux** programmes : le sommet
  mesure `-pos_w.y` et lit `env[14]`, le fragment emploie `env[11]` ;
* les **quatre points** donnent bien au decor cette permutation -- demontre
  par la difference entre les deux essais (sans les programmes de sommets la
  brume DISPARAIT, avec eux elle revient) ;
* `env[11]` et `env[14]` sont a **zero**, et `env[4]` -- le brouillard de
  distance, qui MARCHE -- l est aussi dans ce tampon ;
* la chaine de rendu est en **deux binaires** : la DLL decrit, `vfes.exe`
  televerse (lui seul importe d3d11.dll) ;
* `[etat + 0x420]` est le masque, `[etat + 0x420 + offset]` les donnees, et
  l etat est `[[contexte]+0x38]` des deux cotes.

### Ce qui manque, et c est la seule chose (le chantier REPREND la)

Ecrire a cette adresse ne suffit pas : il reste un maillon entre le tampon et
le GPU. Pistes non explorees, dans l ordre ou je les prendrais :

1. **le moment** : le relais ecrit pendant la preparation d un objet ; le
   televersement de `vfes.exe` a peut-etre deja eu lieu pour cette trame.
   Un point d arret sur `0x14002F590` (la boucle de copie) avec lecture de la
   source dirait ce que l exe lit VRAIMENT a ce moment ;
2. **l offset** : verifier par la mesure que le descripteur d `env[14]` porte
   bien un offset non nul -- s il vaut 0, le relais ecrit sur le masque ;
3. **le masque** : `0x420` sert de masque ET de base des donnees ; si
   l offset est petit, le `or` du relais ecrase les premiers flottants.

Le point 3 est le plus probable, et il se verifie sans rien patcher.

### L etat du patch

`--fog-hauteur` a ete **retire** de `tools/patch_moteur.py` et la DLL
repatchee sans lui. Le chantier se remet en une commande : le code du relais
et des quatre points est integralement decrit ci-dessus et dans les sections
J a O.

### Six fausses pistes, closes

MOYA (ses donnees sont entieres, il est inscrit, instances 3 a 7), la file
translucide de 40, le pool de maillons, la borne d instances auth_3d, le
chargement de l archive, la table des 93 archives. Toutes ecrites comme
fausses dans les sections precedentes.
