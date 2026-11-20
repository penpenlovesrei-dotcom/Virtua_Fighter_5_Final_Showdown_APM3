# L'EAU DU RING D'EILEEN — POURQUOI C'EST DU SABLE, ET CE QUE FAIT LA XBOX 360

Mesuré le 2026-11-19. Tout ce qui suit est relu dans les binaires et les
archives ; les désassemblages sont déposés dans
[`desassemblage/eau_ring_eileen/`](../desassemblage/eau_ring_eileen/).
Ce qui vient d'une séance antérieure est signalé comme tel, et ce qui n'a pas
été vérifié est en dernière section.

---

## 0. La réponse en quatre lignes

Le disque du ring d'Eileen **est** l'objet `stgslk_water_ring`, et il est
rendu **opaque et purement diffus**. La Xbox 360 en fait de l'eau par **quatre
instructions de liaison de texture** dans son rappel de dessin
(`FUN_821C9238`) : elle y accroche la cible de **reflet** et la cible de
**réfraction** sur les unités 3 et 4. **Le rappel de la borne APM3
(`FUN_180085680`) est le même, moins ces quatre liaisons** — et ses quatre
programmes `water_ring` ne déclarent même pas ces deux unités. Le sable n'est
pas une texture de sable : c'est un disque opaque, aux cartes froides de
ver.B, éclairé par le jour chaud de ver.B.

---

## 1. Où est le problème

### 1.1 Le décor, le fichier, et ce qui y est réellement posé

| | |
|---|---|
| décor | **`skb`** — Eileen, version du **VF5 d'origine** (Lindbergh ver.B), posé à l'indice **72** de notre grille (voir [[project_vf5_import_verb]]) |
| archive | `runtime/media/vf5fs/vf5fs_media/rom/objset/stgskb.farc`, **23 468 425 o, datée du 2026-09-11** |
| objets | `stgslk_water_ring` (rang 103) et `stgslk_eff_water` (rang 99) — le préfixe reste `slk`, l'archive seule est renommée |
| éclairage | `rom/light_param/*_skb.txt` + `rom/ibl/skb.ibl` |

**Rien du chantier d'octobre n'est en place.** Aucun fichier `.avant_eau` ni
`.avant_hauteur` n'existe sur le disque ; `fog_skb.txt` porte bien
`density 0.600000` et `color 1.30000 1.20000 1.00000`, c'est-à-dire le jour
chaud de ver.B et non le bleu de `sk5`. Ni `tools/eau_eileen.py` ni
`tools/eau_sur_le_ring.py` n'ont laissé de trace. Ce qu'on regarde est donc
**l'import brut de ver.B**.

### 1.2 Le disque du ring ne porte pas de texture de sable — mesuré, et regardé

Converties en PNG et **regardées**, pas seulement comptées :

| texture | taille | moyenne RGB | aspect |
|---|---|---|---|
| **12674** (empl. 0) | 512² | (70, 71, 84) | gris-bleu sombre nuageux — le fond trouble |
| **12675** (empl. 1) | 512² | (184, 197, 218) | **blanc bleuté froid**, quadrillage d'ombres |
| 9207 (empl. 2) | 256² | (0, 0, 255) | bleu pur — la « normale » |
| 9261 (`MU_RINGOUTMIZU`) | 512² | (188, 179, 158) | **sable beige** — mais c'est le sol de `eff_water`, pas l'anneau |

Les deux cartes de l'anneau sont **froides**. Ce sont celles de ver.B (11800
et 11801 là-bas) : mêmes rangs dans la planche, mêmes tailles, mêmes moyennes
— notre import renumérote les identifiants, pas les images. *(Comparées par
rang et par moyenne, pas par empreinte.)*

### 1.3 Les trois verrous, et ils sont tous mesurés

**(a) Le bloc de réfraction du décor est nul, pour les quarante et un décors.**

La table des descripteurs d'APM3 est `0x180403430`, 41 entrées de `0xF0`.
`FUN_18018FA20` y lit `[desc+0xC0]` (reflet) et `[desc+0xC8]` (réfraction).
Relevé en entier :

    STGSLK (15)   +0xC0 -> 0x1804033E0 = {0,1,1}     reflet ARMÉ
                  +0xC8 -> 0                         réfraction ABSENTE
    les 41        +0xC8 -> 0                         sans exception

Et quand bien même il serait renseigné : `TaskEffectWaterRing::init`
(`0x180085640`) rappelle `FUN_18010C9F0(0)` en `0x18008564C` et **éteint le
drapeau** juste après.

**(b) Le rappel de dessin de l'anneau a perdu ses quatre liaisons.**

C'est le cœur. Les deux rappels, côte à côte :

| Xbox 360 `0x821C9238` | APM3 `0x180085680` |
|---|---|
| `r31 = FUN_82226538()` | `rbx = FUN_1800F06C0()` |
| `r30 = FUN_8224AF58(0)` — cible **reflet** | **absent** |
| `r29 = FUN_8224AF58(1)` — cible **réfraction** | **absent** |
| `FUN_8224CAC8(r30, 3)` — lier sur l'unité **3** | **absent** |
| `FUN_8224CAC8(r29, 4)` — lier sur l'unité **4** | **absent** |
| `FUN_82225568(r31)` | `FUN_1800F2470(rbx)` |
| `FUN_82226448(+2C,+34,+54,+56,+30,+58)` — le tracé | `FUN_1800F0CB0(+2C,+34,+54,+56,+30,+58)` |
| `FUN_82225BB8(r31)` | `FUN_1800F2060(rbx)` |
| `FUN_8224CB28(r30)` ; `FUN_8224CB28(r29)` — délier | **absent** |

**Les six mêmes champs sont passés au tracé, dans le même ordre.** Il ne
manque que les liaisons.

**(c) Le programme `water_ring` ne sait plus lire ces deux unités.**

Relevé directement dans les archives, pas d'après une note :

| | Xbox 360 (`shader_hlsl_88.farc`) | APM3 (`shader_pxd_w64.farc`) |
|---|---|---|
| fragments | **16** (5 chiffres de permutation) | **4** (3 chiffres) |
| unités, toujours | **u0 u1 u2 u3 u4** | **t1 t2 t6 t9** |
| unités, au choix | u5 (cube par le vecteur de reflet), u6, u7 | t7 |
| constantes | `program_env`, `program_local`, `state_material_specular` (nommées dans la CTAB) | *illisibles* — les DXBC de l'archive sont dépouillés, aucun chunk `RDEF` |
| sommets | 4 programmes, tous sur **u14** (carte de hauteur) | 4 programmes, tous sur **t0** |

Les seize fragments de la console déclarent **u3 et u4 sans condition** : ce
sont exactement les deux cibles que le rappel y lie. **Aucun des quatre
fragments d'APM3 ne déclare t3 ni t4.** Même si le rappel reliait les deux
cibles, le programme ne les échantillonnerait pas.

### 1.4 Donc, d'où vient le sable

Le disque est tracé dans la **file opaque** — le champ `+0x3D4` du matériau
vaut `0x10000A80` dans les quatre générations, et le bit 28 court-circuite le
mélange au répartiteur. Il reste donc un disque plein, de couleur
`texture × irradiance`. Sa carte visible est froide ; l'ambiance de ver.B est
chaude (brouillard `1.30 / 1.20 / 1.00`, densité 0,60, ambiante 0,70). Le
produit des deux donne un beige crème — et c'est ce que l'œil appelle du
sable.

Cette dernière liaison (c'est l'éclairage qui achève de le faire lire comme
du sable) **n'est pas de moi : elle a été mesurée à l'écran le 2026-10-15**,
par élimination — avec le matériau et les textures de VF5 R le ring restait du
sable ; avec les six fichiers d'éclairage de `sk5` il est devenu de l'eau
sombre qui ondule. C'est écrit dans l'en-tête de `tools/eau_eileen.py`. Je ne
l'ai pas revue à l'écran.

---

## 2. Comment la Xbox 360 le fait

Tout lu dans **`extracted/X360_VF5/vf5_x360.img`** (VF5, Xbox 360, 2007,
15 663 104 o, base `0x82000000`). Fonctions nommées, dans l'ordre de la
chaîne.

### 2.1 Le décor déclare qu'il a de l'eau

`FUN_822C3E38` est la mise en place du décor : machine à quatre états sur
`[this+0x4C]`, table de sauts en `0x822C3E78`. **Le cas 1** (`0x822C3E88`) lit
le descripteur `[this+0x58]` et y trouve deux blocs :

    [desc+0x58]  bloc « reflet »       -> FUN_8224AFF8(2, 1)   autoriser la passe 2
                                          FUN_8224B038(bloc[0])  [mgr+0xF8]
                                          FUN_8224AFE0(bloc[1], bloc[2])
                                          FUN_8224B078(1)       [mgr+0x5C] = 1
    [desc+0x5C]  bloc « RÉFRACTION »   -> FUN_8224AFF8(3, 1)   autoriser la passe 3
                                          FUN_8224B048(bloc[0])  [mgr+0xFC]
                                          FUN_8224B088(1)       [mgr+0x5D] = 1

Le gestionnaire global est **`0x8284C79C`** : ses octets `+0x00..+0x0F` sont
les autorisations de passe, `+0x5C` et `+0x5D` les deux drapeaux, `+0x11C` un
tableau d'enregistrements de cible de 36 octets.

**La table des décors est `0x820814D8`, 37 entrées de `0x70`.** Relevée en
entier : **seuls `STGJIN` (9) et `STGSLK` (15) portent un bloc de réfraction**,
`{1,0,0}` tous les deux. Eileen est bien l'un des deux décors d'eau du jeu.

### 2.2 Les cibles sont liées pour la scène

`FUN_8224B590` est le lieur de scène. Sous **double garde** — l'autorisation
de passe (`[mgr+2]`, `[mgr+3]`) **et** le drapeau (`[mgr+0x5C]`, `[mgr+0x5D]`) :

    0x8224B624   li r4, 0xF   -> FUN_8224CAC8(cible, 15)   le REFLET sur GL_TEXTURE15
    0x8224B690   li r4, 0xE   -> FUN_8224CAC8(cible, 14)   la RÉFRACTION sur GL_TEXTURE14

Ce sont les unités que lit `water01`, le grand plan.

### 2.3 Et sur l'anneau, c'est la tâche qui les lie

`TaskEffectWaterRing`, vtable **`0x82005D0C`** (par la RTTI). Son **créneau 4**
(`0x821C9370`) est le `disp` :

    lbz  r11, 0x50(r3)      ; si le drapeau de la tâche est nul, rien
    beqlr
    r3 = 0x00170005         ; objset 0x17 = STGSLK, rang 5 = STGSLK_WATER_RING
    r4 = 0x821C9238         ; LE RAPPEL DE DESSIN
    b  0x822216D0           ; l'enregistrer

`0x00170005` : c'est **le disque du ring**, le même objet que chez nous.

Et le rappel **`FUN_821C9238`** fait les quatre liaisons :

    r30 = FUN_8224AF58(0)   ; la cible « reflet »
    r29 = FUN_8224AF58(1)   ; la cible « réfraction »
    FUN_8224CAC8(r30, 3)    ; GL_TEXTURE3
    FUN_8224CAC8(r29, 4)    ; GL_TEXTURE4
    ... le tracé ...
    FUN_8224CB28(r30) ; FUN_8224CB28(r29)

`FUN_8224AF58(k)` rend l'enregistrement de cible : il passe par la variante
`[mgr+0xF8+4k]`, la redirige par la table `0x82651448[variante + 3k]`, puis
indexe `mgr+0x11C` par 36. Pour `slk` : reflet → enregistrement 0,
réfraction → enregistrement 1.

### 2.4 Les deux primitives, et pourquoi on sait ce qu'elles font

    FUN_82359788(e)        [0x82AD5500+0x1DA438] = e - 0x84C0   -> glActiveTexture
    FUN_82359830(c, id)                                         -> glBindTexture
    FUN_8224CAC8(cible, n)  [cible+0xC] = n
                            FUN_82359788(n + 0x84C0)
                            FUN_82359830([[cible+4]+0x14], [[cible+4]+0x10])
    FUN_8224CB28(cible)     la même chose avec id = 0           -> délier

**`0x84C0` est `GL_TEXTURE0`**, et `FUN_82359788` le retranche de son argument
avant de le ranger (`addis r10, r3, -1 ; addi r10, r10, 0x7B40`). Le moteur a
donc gardé sa forme OpenGL jusque sur la Xbox 360, et `FUN_8224CAC8` n'est pas
un tracé : **c'est une liaison de texture.**

### 2.5 Le programme de fragments, côté console

Les 16 `water_ring.*.fp` sont du `ps_3_0` précédé d'un en-tête SEGA de `0x28`
octets et d'une **CTAB D3DX gros-boutiste**, qui nomme les paramètres. Tous
déclarent `u0 u1 u2 u3 u4`, plus, selon les chiffres de permutation, `u5` (le
cube par le vecteur de reflet), `u6`, `u7` et `program_env` (`p_fb_isize`).
`state_material_specular` est là dans les seize.

Le sens des unités est celui que l'inventaire des sources ARB de Lindbergh
avait établi le 2026-10-15 : `4` = la carte de transparence, `5` = le cube par
le vecteur de reflet, `14`/`15` = réfraction et reflet en espace écran.

**Donc, sur l'anneau, la console a : la transparence, le reflet, la réfraction
et le Fresnel. La borne n'a qu'un cube d'irradiance diffus.**

---

## 3. Ce qu'il faudrait faire dans APM3

Trois pièces manquent, et elles ne se remplacent pas au même prix.

### 3.1 La pièce bon marché : l'éclairage

Poser les six fichiers de `sk5` (`tools/eau_eileen.cmd --eclairage-r`). Coût :
nul, réversible, aucun octet de moteur. **Résultat déjà vu à l'écran le
2026-10-15** : le ring devient de l'eau sombre qui ondule. Mais ce n'est pas
l'eau de la console — c'est la nuit bleue de VF5 R posée sur le jour de ver.B,
et tout le reste du décor change de couleur avec. **C'est un choix d'aspect, et
il revient à Frédéric** ; c'est exactement ce que la fiche
[[project_vf5_import_verb]] laisse en attente depuis le 2026-09-11.

### 3.2 La pièce moyenne : rendre les quatre liaisons au rappel

Greffer dans `FUN_180085680`, avant l'appel du tracé `0x1800F0CB0`, l'équivalent
des quatre instructions de la console, et les deux déliaisons après. Le dépôt
sait déjà faire ce genre de greffe (relais en section ajoutée, site d'appel
dévié, jamais le corps). Il faut pour cela :

1. les deux accesseurs de cible côté APM3 — les jumeaux de `FUN_8224AF58` ;
2. le lieur — le jumeau de `FUN_8224CAC8`. **`0x18010CE60` est un candidat
   mesuré** : `FUN_18010B1F0` l'appelle avec `edx = 0xF` en `0x18010B28F`,
   c'est-à-dire la liaison d'une cible sur l'unité 15 ;
3. que la passe 2 soit bien allumée pour `skb` — elle l'est,
   `[STGSLK+0xC0] = {0,1,1}`, donc la cible de reflet existe. **La passe 3 ne
   l'est pas**, donc la cible de réfraction est vide ou absente.

Coût : une séance de greffe, pas davantage. **Mais à elle seule elle ne change
rien à l'écran** — voir 3.3.

### 3.3 La pièce qui coûte : le programme de fragments

C'est le verrou. Les quatre `water_ring.*.fp` d'APM3 ne déclarent pas `t3` ni
`t4` ; ils ne peuvent pas lire les cibles même liées. Il faut **écrire** un
programme de fragments qui les lise, avec transparence et Fresnel — ou porter
celui de la console, dont le microcode Xenos n'est pas transposable tel quel en
DXBC.

Le dépôt a **déjà le mécanisme de livraison**, et il est éprouvé :
`tools/shader_empreintes.py` fabrique une archive à côté,
`w64/shader_vf5_w64.farc`, et dévie l'ouverture du moteur pour **un seul nom de
shader**. Le même site servirait pour `water_ring`. Il reste à savoir **laquelle
des quatre permutations** le matériau `0x010D` demande — ça se lit dans le
constructeur de clé `0x180175680` et la table d'états `0x180715440`, ou se
mesure en une passe de `tools/tracer_fichiers.py`.

**Et il faut écrire le DXBC à la main**, comme l'a été le geometry shader des
empreintes dans la neige : il n'y a pas de compilateur HLSL dans la chaîne, et
le shader doit être compatible des entrées que le programme de sommets d'APM3
produit (`TEXCOORD8 TEXCOORD0 TEXCOORD7 TEXCOORD2`) et des registres de
constantes que le moteur remplit. C'est le gros du travail.

### 3.4 Ce qui bloque, nommément

| blocage | mesuré | contournable ? |
|---|---|---|
| `[STGSLK+0xC8] = 0`, les 41 | oui, dans le `.dll` | oui — patch de donnée, mais `init` rééteint le drapeau derrière |
| `init` éteint la réfraction (`0x18008564C`) | oui | oui — deux octets |
| le rappel ne lie rien | oui, désassemblé | oui — greffe |
| **le fragment shader ne déclare pas `t3`/`t4`** | **oui, dans l'archive** | **non sans écrire un DXBC neuf** |
| la cible de réfraction n'est remplie par personne tant que la passe 3 n'est pas permise | oui (`[desc+0xC8] = 0`) | lié au premier |
| allumer la réfraction décale la permutation de `WATER01` de douze rangs et fait tomber `eff_water` sur un programme non chargé | **non, pas par moi** — c'est le relevé du 2026-10-15 | inconnu |

**Mon avis, et c'est un avis :** 3.1 est gratuit et visible tout de suite ;
3.2 et 3.3 ne se tiennent qu'ensemble, et 3.3 est une séance entière d'écriture
de DXBC avec un seul moyen de vérifier — l'écran.

---

## 4. Deux corrections à des notes existantes

1. **`analysis/eau_slk_console.md` §2** dit de `0x8224B674` : « …
   `bl 0x8224CAC8` **ET IL DESSINE** ». Non : `FUN_8224CAC8` est une liaison de
   texture (`glActiveTexture` + `glBindTexture`), et l'argument `0xE` est le
   numéro d'unité, pas un compteur. La même section donne `0x8234CEE4` et
   `0x8234CF30` comme « lectures du drapeau `water_ring` » : ces deux-là lisent
   le `+0x5D` d'un **autre** objet (un bloc d'état de matériau, qui a aussi un
   `+0x9`, un `+0xA` et un `+0x5E`), pas le gestionnaire `0x8284C79C`. Le seul
   lecteur du drapeau est `0x8224B674`.
2. **`analysis/decors.md`** nomme les champs `+0xC0` et `+0xC8` du descripteur
   APM3 « descripteur sonore principal » et « de repli ». Ce sont le **bloc de
   reflet** et le **bloc de réfraction** : `FUN_18018FA20` et le
   `FUN_822C3E38` cas 1 de la Xbox 360 appellent les mêmes cinq accesseurs,
   dans le même ordre, avec les mêmes arguments.

---

## 5. Ce qui n'a PAS été vérifié

- **Rien n'a été lancé. Aucune course.** Tout est statique : binaires, archives,
  images.
- **Je n'ai pas vu l'écran.** « Le ring paraît en sable » est la mesure de
  Frédéric ; « avec l'éclairage de `sk5` il devient de l'eau sombre » est la
  mesure de la séance du 2026-10-15, lue dans l'en-tête de `tools/eau_eileen.py`.
  Je n'ai revu ni l'une ni l'autre.
- **Je n'ai pas établi quelle surface Frédéric appelle « le sable ».** Le disque
  du ring (`stgslk_water_ring`) est ma lecture, parce que c'est lui qui occupe
  l'aire de combat et que l'essai au magenta du 2026-10-15 l'avait identifié.
  Le grand plan `stgslk_eff_water` est un autre candidat, et son emplacement 0
  est bel et bien une image de sable (`MU_RINGOUTMIZU`, 9261).
- **Le microcode Xenos des seize `water_ring.*.fp` n'a pas été désassemblé.**
  Je n'ai lu que leur CTAB : ce que chaque programme **déclare** lire, pas ce
  qu'il **calcule**. C'est suffisant pour comparer les unités de texture ; ce
  n'est pas une lecture du calcul, et je ne peux pas dire à quoi ressemble
  exactement le Fresnel de la console.
- **Le DXBC d'APM3 n'a pas été désassemblé non plus**, seulement ses
  déclarations (`dcl_resource`) et le compte de ses opcodes. Les DXBC de
  l'archive sont dépouillés : aucun chunk `RDEF`, donc aucun nom de ressource.
- **La permutation réellement demandée** parmi `water_ring.000/001/010/011`
  n'est pas déterminée. Les quatre sont amputées de la même façon, donc la
  conclusion ne dépend pas de la réponse — mais une greffe, elle, en dépendra.
- **Le bit 28 de `+0x3D4` qui envoie le tracé dans la file opaque** est repris
  de la lecture du moteur faite le 2026-10-15 (`0x1800EB71B : bt ecx, 0x1C ;
  jb`). J'ai vérifié que le champ vaut bien `0x10000A80` dans les quatre
  générations, pas que le moteur le lit ainsi.
- **Le décalage de douze rangs de `WATER01`** quand on allume la réfraction, la
  table de présence `sousShader+0x38` et les rangs 100 / 106 / 130 / 142 sont
  **repris du relevé du 2026-10-15**. Je ne les ai pas relus dans le binaire.
- **`0x18010CE60` comme jumeau de `FUN_8224CAC8`** est une **piste**, pas une
  mesure : je l'ai vu appelé avec `edx = 0xF` depuis `FUN_18010B1F0`, et rien
  de plus. Sa signature n'a pas été lue.
- **Les cibles de rendu d'APM3** (combien, quelle taille, laquelle est la
  réfraction) n'ont pas été relevées par moi.
- **L'indice 72 de `skb`** vient de [[project_vf5_import_verb]] ; je ne l'ai pas
  revérifié dans `tools/decors_vf5.cmd`.
- **La PS3** n'est pas mesurable : ses segments sont chiffrés. Ce n'est pas une
  absence, c'est un refus de lecture.

---

## 6. Deuxieme seance du 2026-11-19 : la cle de permutation, et WATRING

Mesure par deux outils neufs, qui se relancent :
`tools/eau_nuanceurs_apm3.py` (la presence lue dans la DLL, les liaisons
lues dans le DXBC) et `tools/eau_presence_watring.py` (le controle et la
pose des deux octets du 6.5). DLL lue :
`binaires/vf5fs-pxd-w64-Retail_APM3.dll.origine`, base `0x180000000`.
Archive lue : `runtime/media/vf5fs/vf5fs_media/w64/shader_pxd_w64.farc`.

### 6.1 La numerotation `t<N>` d'APM3 EST celle des unites du moteur

Le doute du 5 est leve. Les quatre `water01.*.fp` montes declarent :

    water01.0001100001.fp   t2 t15
    water01.0001001001.fp   t2 t5
    water01.0001101001.fp   t2 t5 t15
    water01.0011101001.fp   t0 t2 t5 t15

`t15` est exactement l'unite que le lieur de scene accroche : `0x18010B28F`
appelle `0x18010CE60` avec `edx = 0xF`. La numerotation du DXBC est donc
celle du moteur, et comparer les `t3`/`t4` d'APM3 aux `u3`/`u4` de la console
a un sens. **Aucun des quatre ne declare `t14`** : la refraction est morte
dans tout le build, pas seulement sur l'anneau.

Au passage, les trois mots d'etat du lieur, releves dans son corps :

    0x18010B294   etat 43 = 1   le REFLET est lie sur l'unite 15
    0x18010B2BA   etat 45 = 1   la passe 3 est permise
    0x18010B2EE   etat 44 = 1   la REFRACTION est liee sur l'unite 14

`0x180715440` est donc le tableau d'etats lui-meme, celui que le
constructeur de cle indexe.

### 6.2 La cle de permutation, et elle est verifiee

Lue dans `0x1801756F9`..`0x180175770` :

    chiffre_i = min(radice_i, ETATS[indice_i])
    cle       = somme chiffre_i * place_i
    place_0 = 1 ; place_i = place_{i-1} * (radice_{i-1} + 1)

Les deux radices -- sommets et fragments -- sont dans le meme
enregistrement de 0x30 octets : `[+8]` les sommets, `[+0x10]` les fragments.

    WATER01  etats [23,22,37,41,43,44,38,47,49,15]
             radices vp [1,1,0,1,0,0,0,0,1,1]  ->  32
             radices fp [0,0,2,1,1,1,1,1,0,1]  -> 192

**Le controle :** le modele rend le rang **105** pour
`water01.0001100001.fp` et le rang **130** pour `water01.0011101001.fp` --
les deux rangs releves independamment le 2026-10-15. Il passe.

### 6.3 WATRING n'a aucun chiffre pour le reflet, la refraction, le cube ni le Fresnel

    WATRING  etats [49, 46, 24]
             radices vp [1, 1, 0]  -> 4
             radices fp [0, 1, 1]  -> 4

Ni 43 (reflet), ni 44 (refraction), ni 38 (cube par le vecteur de reflet),
ni 15 (alpha / Fresnel) ne figurent dans sa cle. **Aucune permutation de
WATRING, dans ce build, ne peut les lire** : ce n'est pas que les quatre `fp`
ne declarent pas `t3`/`t4`, c'est que le nuanceur n'a pas de chiffre pour
eux. C'est dans les tables de la DLL, pas dans une archive.

### 6.4 Et WATRING n'a aucun programme de sommets atteignable

Le chiffre 1 des sommets vaut `min(1, ETATS[49])`.

**Toutes les ecritures du mot d'etat 49 (`0x180715504`) rangent zero** :
sept sites, tous le meme bloc de remise a zero de fin de trace
(`0x1800F089E`, `0x1800F0A8B`, `0x1800F1127`, `0x1800F1454`, `0x1800F1585`,
`0x1800F17D7`, `0x1800F1C71`), plus la remise a zero en bloc de
`0x1801764A0`. Et le traducteur materiau -> etats `0x1800F3060` ecrit les
etats 15, 41, 46 et 47 : **jamais le 49**.

*Le controle, celui qui pourrait echouer :* les etats 15, 22, 23, 37, 41,
44, 46 et 47 ont, eux, des ecrivains qui ne sont pas le bloc de remise a
zero -- par exemple `0x1800F2FB4 : mov dword ptr [etat 22], 1`. La lecture
sait donc faire la difference entre « remis a zero » et « jamais pose ».

La presence des quatre `vp` vaut `[0, 1, 0, 1]`, et l'indice est
`d1 + 2*d2` :

    idx 0  water_ring.000.vp   presence 0   <- la cle tombe ici
    idx 1  water_ring.100.vp   presence 1
    idx 2  water_ring.010.vp   presence 0   <- la cle tombe ici
    idx 3  water_ring.110.vp   presence 1

Les deux montes sont exactement ceux qui exigent `d1 = 1`. Le chargeur
`0x180175BF0` ne monte un programme que si son octet de presence est non nul
(`0x180175D2B`). **La cle ne peut atteindre que des indices non montes.**

**La contradiction, nommee :** les deux `water01.*.vp` montes portent tous
deux le chiffre 9 -- l'etat 49 -- a **0**, ce qui s'accorde avec un etat 49
toujours nul. C'est la table de presence de WATRING qui est l'intruse. Et
**ce que fait le moteur quand aucun programme de sommets n'est monte n'est
pas mesure** : identifiant a zero, programme precedent laisse en place, ou
trace abandonne -- trois etats, aucun verifie.

### 6.5 Deux octets, et ils sont sans risque

Dans l'archive, `water_ring.000.vp` est **octet pour octet**
`water_ring.100.vp` (md5 `d73e2f231f7000a2cd689eb34ed89344`), et
`water_ring.010.vp` est `water_ring.110.vp`
(`6967b588071e0b78de9a61829dd8f1bf`). Memes signatures des deux cotes :
5 entrees, 5 sorties dont `SV_POSITION` au registre 4. Le chiffre 1 ne
change donc **rien** au programme emis : monter les indices 0 et 2 rend
exactement le programme que SEGA a monte pour l'autre chiffre.

    VA 0x18055636C   offset fichier 0x554F6C
    00 01 00 01  ->  01 01 01 01

Pose et controlee **sur une copie** de `.origine`, pas sur le depot :
md5 `3214e19696deed80e9da8e54f5e6afe8` -> `eabb10d6a10e73d3003b9e134d8e6397`,
`--rendre` revient a `3214e196...` a l'empreinte pres, un deuxieme `--poser`
dit « deja pose » sans ecrire, et une copie dont la presence est
`00 00 00 01` est **refusee** sans une seule ecriture.

Le bloc pour `tools/patch_moteur.py` est dans le rapport de seance : un
triplet a ajouter a `EAU_INIT`, que `_poser_points` verifie deja.

### 6.6 Trois corrections

1. **`tools/patch_moteur.py`, l'en-tete de `--eau-refraction`** dit : « le
   seul programme qui [anime la surface] est `water_ring.000.vp` : `TEX
   displace, a_tex0, texture[14], 2D` [...] L'unite 14 n'est liee qu'en
   `0x18010B2E9` ». C'est la source ARB de Lindbergh. **Dans le DXBC
   d'APM3, `water_ring.*.vp` echantillonne `t0`, pas `t14`** : le
   deplacement vient de l'**emplacement 0 du materiau** (12674 sur le `skb`
   pose). Allumer la passe 3 ne peut donc pas nourrir le deplacement de
   sommets d'APM3. Lu en entier, lignes 22 a 25 de `water_ring.100.vp` :
   `r0.xy = v3.xy*(1,-1)+(0,1)` ; `sample_l t0` ; `r0.x *= 0.5` ;
   `r0.xyz = normale*r0.x + position`. Et le programme que l'en-tete nomme,
   `water_ring.000.vp`, est justement celui dont la presence est nulle.
2. **Le 1.3 (c) de cette note** concluait juste, mais sur une premisse non
   etablie (que `t3`/`t4` d'APM3 soient les `u3`/`u4` de la console). Elle
   l'est maintenant (6.1), et la vraie raison est plus forte (6.3).
3. **`desassemblage/eau_ring_eileen/shaders_water_ring.txt`** compte 17
   instructions pour `water_ring.000.fp` ; en comptant les `dcl_*` il y en a
   31. Ce n'est pas une erreur, ce sont deux comptes -- note pour qu'ils
   n'aient pas l'air de se contredire.

### 6.7 Ce que calcule reellement le fragment du disque, lu en entier

`water_ring.000.fp`, 31 opcodes : `t2` (la normale) depliee `*2-1`,
normalisee, `x` inversee ; `t9` (le cube d'IRRADIANCE) echantillonne au
niveau 0 selon cette normale ; `t6` echantillonne en `TEXCOORD7.xy` au
niveau `TEXCOORD7.w` -- et **le programme de sommets ecrit `TEXCOORD7`
constant a zero** (`o2 = (0,0,0,0)`), donc `t6` est lu en (0,0) ; `mad` avec
`cb0[13]`/`cb0[12]` ; `* cb4[2]` ; `* t1` (l'emplacement 1, le 12675 froid) ;
`* 4` -> `o0`, avec `alpha = t1.a * 4`. Opaque et purement diffus, confirme
instruction par instruction. **L'alpha EST calcule** : c'est la file opaque
qui l'ignore.

### 6.8 Et la piste que ca rouvre

`tools/eau_eileen.py` a refuse, le 2026-10-15, de poser le materiau de
WATER01 sur le disque du ring, pour garder le deplacement : « les deux
s'excluent, et c'est la deformation qui a ete choisie ». Si le 6.4 tient,
**il n'y a pas de deformation a garder** : WATRING n'a aucun programme de
sommets atteignable. L'arbitrage tombe, et `COPIES =
{'stgslk_water_ring': 'stgslk_eff_water'}` redevient la route la moins
chere vers de l'eau sur le disque -- le rang 130 de WATER01 est monte et lit
`t15`.

**Non verifie, et ca decide de tout :** le maillage du disque porte-t-il
`TANGENT0` ? Le programme de sommets de WATER01 le declare, celui de
WATRING non. Tant que ce n'est pas lu dans l'objset, c'est une piste, pas un
plan.

### 6.9 Ce qui n'a PAS ete verifie dans cette seance

- **Rien n'a ete lance. Aucune course.** `vfes.exe` tournait au debut de la
  seance (une course de menu, lancee par Frederic) ; rien n'a ete ecrit sous
  `runtime/media`. Il etait absent a la fin, et rien n'y a ete pose non plus.
- **Quelle surface Frederic appelle « le sable » n'est toujours pas
  etablie.** Element neuf : l'objset `slk` de ver.B **n'a pas** d'objet
  `stgslk_ring` (id 259), alors que ceux de FS et de VF5 R l'ont. Chez ver.B
  le disque d'eau EST donc le plancher du ring ; chez FS c'est un film
  au-dessus d'un vrai plancher.
- **Deux des sept sites d'ecriture de l'etat 49** (`0x1800F1454` et
  `0x1800F17D7`) : le registre (ebp, r13) n'a pas ete remonte jusqu'a un
  zero dans la fenetre lue. Les cinq autres le sont (`xor`), et le bloc est
  identique aux sept.
- **Qu'un autre module (`vfes.exe`) puisse ecrire l'etat 49** par une
  fonction exportee n'a pas ete verifie.
- **Ce que fait le moteur sans programme de sommets monte.**
- **Le contenu des `cb0`..`cb5`** : les DXBC sont depouilles, aucun `RDEF`.
- **Le format de sommets du maillage du disque** (`TANGENT0`).
- **L'eclairage (3.1) n'a pas ete touche** : `fog_skb.txt` porte toujours le
  jour chaud de ver.B.
---

## 7. POSEE DANS `patch_moteur.py` -- ET SOUS SON PROPRE MOT (2026-11-19)

### La correction a la section 6 : `EAU_INIT` aurait dormi

La section 6 demande d'ajouter le triplet a `EAU_INIT`, c'est-a-dire a
l'option `--eau-refraction`. Mesure faite avant de poser :

    grep -rl "eau-refraction" --include=*.cmd .   ->   AUCUN LANCEUR

`--eau-refraction` n'existe que dans le patcheur et dans les notes. Le
correctif y aurait dormi : la course aurait montre du sable, et on aurait
cherche la faute dans les octets au lieu de la chercher dans la ligne
d'options. **Et on ne peut pas ajouter `--eau-refraction` aux lanceurs pour
autant** : ses deux points reposent sur la premisse que la section 6 vient
de demontrer fausse pour APM3 (`water_ring.*.vp` echantillonne `t0`, pas
`t14`), et les poser allume une passe de refraction en faisant pointer un
bloc **global** sur la cible 1 -- un risque reel pour un gain nul.

D'ou : la presence de `WATRING` a pris **son propre mot**, `--eau-presence`,
avec sa propre liste `EAU_PRESENCE`. Deux octets, une cause mesuree, aucun
effet de bord connu.

### Ce que la pose a mesure

Patcheur relance avec la ligne d'options exacte de la DLL installee (relue
dans `ram/patch_empreinte.json`, resolution 1920 x 1080, 60 chantiers) plus
`--eau-presence --brume-aoi` :

| | |
|---|---|
| DLL avant | `022b3d667a72851485e62383f6d3d2ebd04be9fb` |
| DLL apres | `9b87f161f8b3a65d2773eb3089fb798d2fadb4d6` |
| taille | 7 181 824, inchangee |
| octets differents | **46, et le jeu des offsets est EXACTEMENT celui attendu** |

Les 46 se decomposent en 18 (l'etat 15 de la brume) + **2** (la presence de
`WATRING` : `00 01 00 01` -> `01 01 01 01`, deux octets sur quatre changent)
+ 26 (la presence des jumeaux BLINN). Rien d'autre n'a bouge : le controle
compare le JEU des offsets, pas leur nombre.

La DLL d'avant est gardee sous
`runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll.avant_decors_19nov`.

### Ce qui n'est toujours pas tranche

**L'ecran.** Rien n'a ete lance. Les quatre points de la section 6 restent
ouverts, le premier en tete : si le moteur ne montait rien, l'anneau recoit
son programme de sommets ; si quelque chose etait deja monte par un chemin
non trouve, les deux octets ne font rien.
---

## 8. L'ÉCRAN A RÉPONDU : LE SABLE N'EST PAS `stgslk_water_ring` (2026-11-19)

Course `20261119_2259`, verdict de Frédéric : **« pas d'eau pour eileen »**.
Issue **D6**, nommée d'avance, qui laissait deux causes possibles. La
question « quelle surface est le sable » traînait depuis octobre (§6.2 du
rapport, point 2 des restes). **Elle est tranchée, et sans course.**

### Comment, en regardant les images

Les deux surfaces candidates du `skb` monté dans notre build :

| objet | nuanceur | emplacement 0 | rang dans `stgskb_tex.bin` |
|---|---|---|---|
| `stgslk_water_ring` | `WATRING` | id **12674** | 520 |
| `stgslk_eff_water` | `WATER01` | id **9261** | 573 |

Converties en PNG et **regardées**, 512 × 512 DXT1 toutes les deux :

* **rang 520**, l'emplacement 0 du disque `water_ring` : une nappe **bleu-gris
  sombre**, nuageuse. De l'eau.
* **rang 573**, l'emplacement 0 du grand plan `eff_water` : un **beige pâle**,
  granuleux, uniforme. **Du sable.**

La surface de la capture est beige pâle. **C'est `stgslk_eff_water` qu'on
voit, pas le disque.** Une texture DXT1 bleu-gris sombre ne devient pas beige
pâle sous un éclairage.

### Ce que ça fait tomber, et ce que ça ouvre

Les deux octets de `--eau-presence` sont **justes et inutiles** : ils montent
bien les programmes de sommets que la clé de `WATRING` peut atteindre --
l'outil de l'agent le confirme, `POSE` contre `AVANT` sur le `.origine` --
mais `WATRING` n'habille pas la surface qu'on voit. **On a réparé le bon
défaut sur le mauvais objet.** L'option reste, elle ne coûte rien et elle est
mesurée ; elle ne sera simplement pas ce qui rend l'eau.

**Et le sable est dans la donnée d'origine, pas dans notre chaîne.** Les deux
textures sont **identiques octet pour octet** entre l'objset ver.B extrait et
celui que notre build monte (sha1 `1957f28ccbe4` et `6738522b661f`), et elles
occupent les **mêmes rangs** 573 et 520. `--decors-vf5` n'a rien abîmé.

Donc : chez ver.B aussi, l'emplacement 0 d'`eff_water` est une image de
sable. **C'est le nuanceur `WATER01` qui en fait de l'eau** -- reflet,
réfraction, cube, Fresnel. Et le §6.1 a mesuré que dans tout notre build
**aucun des quatre `water01.*.fp` ne déclare `t14`** : la réfraction est
morte partout.

### La suite, et elle change de cible

Ce n'est plus `WATRING` qu'il faut regarder, c'est **`WATER01` sur
`stgslk_eff_water`** : quelle permutation est montée pour ce matériau, ce
qu'elle lit, et ce qui manque pour que le reflet (état 43, unité 15, qui lui
est **vivant** -- §6.1) habille la surface. `cle_permutation.py WATER01` fait
déjà la moitié du chemin.

**Pas mesuré** : ce que `WATER01` rend aujourd'hui sur ce matériau, ni si le
reflet seul suffit à sortir du sable.
---

## 9. LA PHYSIQUE DE L'EAU EXISTE DANS CE BUILD, ET ELLE EST COUPÉE POUR NOS DÉCORS (2026-11-19)

Frédéric : « l'eau NE PEUT PAS ÊTRE UNE SIMPLE TEXTURE : elle a une physique
différente du sable ». **C'est juste, et la cause est maintenant mesurée dans
le binaire.** Décompilation à REA + Ghidra 12.1.2 sur
`analysis/vf5fs_apm3_origine.dll`.

### 9.1 `TaskEffectRipple` est là, entière, nuanceurs montés

| ce qu'on trouve | où |
|---|---|
| RTTI `.?AVTaskEffectRipple@@` | `0x180663178` |
| `EFFECT_RIPPLE`, **tâche n° 7** du tableau des 23 noms | `0x18034FA78`, tableau en `0x18034E4D0` |
| traces `TaskEffectRipple::init()` / `::dest()` | `0x180350E9F` / `0x180350EC0` |
| nuanceurs | `ripple.0.vp`, `ripple.0.fp`, `ripple.1.fp`, `ripple_emit.{00,10,01,11}.fp`, `ripple_emit.00.vp` |

`cle_permutation.py RIPPLE` : groupe **41**, un sous-nuanceur, descripteur
`0x180556DF0` (id 43) — **vp 1 programme / 1 monté, fp 2 programmes / 2
montés**. Contrôle de la base mixte : 4206 jeux de chiffres sur 4206
recalculés à l'identique.

**Rien ne manque côté nuanceurs.** Ce n'est pas un problème de présence,
contrairement à `water01`.

### 9.2 Le vrai init, et sa garde : DEUX identifiants en dur

`FUN_18007AE10`, appelé par l'init `0x18007B030`
(`FUN_18007ae10(DAT_1806f2160, (int)param_1[0xb])`) :

```c
puVar6 = &DAT_1806432e0;                       // entrée 0
if (param_2 != DAT_1806432e0) puVar6 = 0;      // son id : 4
if (param_2 == DAT_18064330c)                  // entrée 1, son id : 15
     puVar6 = &DAT_18064330c;
else if (puVar6 == 0) return;                  // <<< SORTIE SÈCHE
```

Ensuite seulement : les trois tampons (`FUN_180218930`), la passe 4
(`FUN_18010CA20(4,1)`), le rappel de dessin `LAB_18007B470`, les deux chaînes
de 14 éléments de `0x14` octets remplies depuis `DAT_180350E30` et
`DAT_180350E68`, et pour finir

```c
*(undefined4 *)(gestionnaire + 0x328) = 1;
*(uint *)(gestionnaire + 0x32c) = (uint)(param_2 == 4);
```

**Ce n'est pas une boucle sur une table : c'est un test déroulé sur deux
identifiants**, et le `return` ne laisse aucune trace. Pas de tampon, pas de
passe 4, `+0x328` reste à zéro.

### 9.3 Les deux identifiants, lus dans les octets

    0x1806432E0  id = 4    -> `ban`
    0x18064330C  id = 15   -> `slk`   (le décor d'Eileen d'ORIGINE)

Pas `0x2C` entre les deux, conforme à `decors.md` §20.1.

**Et nos décors d'Eileen sont ailleurs :** `sk5` = **53**, `skb` = **72**
(`variantes_5r.py`, `variantes_vf5.py`). Ni 4, ni 15.

**`skb` demande pourtant bien la tâche 7.** La liste de ver.B pour `slk`,
relue dans son ELF et traduite en numérotation FS, est

    [2, 13, 7, 14, 17]  =  WALL, WATER_RING, RIPPLE, SPLASH, WET_CLOTH

Donc : la tâche est créée, son init s'exécute, et **il sort avant la première
allocation**. La surface n'a aucune onde — jamais, dans aucune image.

### 9.4 Rien n'a jamais été posé là

Les deux identifiants sont **identiques dans `.origine` et dans la DLL en
place** (relus côte à côte). Et `analysis/decors.md` §20.1 le portait déjà
comme un reste, écrit le 2026-09-10 :

> | 7 | `RIPPLE` | `0x1806432E0`, via `FUN_18007AE10` depuis l'init | chaîne
> déroulée ×2, pas `0x2C` | flottants + 1 id de sprite | `bn5`, `sk5` |
> balayage ; **clone pur** |

Ce « clone pur » n'a pas été fait. **C'est le reste le plus cher du chantier
de l'eau, et il était écrit.**

### 9.5 Ce que ça change pour les deux octets de ce soir

`--eau-water01` (les rangs 100 et 106 du grand plan) rend au matériau un
programme de fragments — **le nuanceur**. `--eau-presence` rend à `WATRING`
ses permutations. **Ni l'un ni l'autre ne rend la SIMULATION** : celle-ci est
`TaskEffectRipple`, et elle est coupée par l'identifiant de décor. Les trois
sont indépendantes et aucune ne remplace les autres.

### 9.6 Le choix qui reste, et il n'est pas à moi

La garde étant **déroulée**, on ne peut pas ajouter un troisième décor sans
toucher au code. Trois poses possibles, et chacune coûte :

| pose | ce qu'on gagne | ce qu'on perd |
|---|---|---|
| `15 -> 72` | l'eau de `skb` | l'eau du `slk` d'origine |
| `4 -> 53` **et** `15 -> 72` | `sk5` **et** `skb` | `ban` et `slk` d'origine |
| détour sur la garde | tous | du code neuf dans un chemin chaud |

### 9.7 Ce qui n'est PAS mesuré

* **Que `gestionnaire+0x328` soit lu quelque part.** Le balayage
  `champ_x64.py 0x328` sort 40 accès, mais le déplacement `0x328` appartient à
  des dizaines d'objets différents et **aucun appelant de `FUN_18006F350` (le
  getter du gestionnaire, 40 appelants) ne le lit**. Ce n'est pas une preuve :
  un consommateur peut garder le pointeur. `+0x330`, lui, a été prouvé non lu
  par point d'arrêt matériel (cf. `VF5RE/analysis/eau_slk_console.md`).
* **Que restaurer la tâche fasse paraître de l'eau.** C'est l'écran qui
  tranchera.
---

## 10. CORRECTION DE LA SECTION 9 : LA TÂCHE DES ONDES TOURNE DÉJÀ SUR `skb` (2026-11-20)

**La section 9 conclut faux sur son point central.** Elle dit que la garde de
`TaskEffectRipple` ne connaît que les décors 4 et 15, donc que l'init sort à
sec sur `skb` (72) et que la simulation ne tourne jamais. C'est vrai de
**`.origine`**. Ce n'est pas vrai de **la DLL qui tourne**.

### 10.1 Ce que porte la DLL en place

Le socle remplace cette garde. Il l'écrit lui-même, dans la sortie du tour de
patch que j'avais sous la main :

> « effets : la chaîne de comparaisons DÉROULÉE de `TaskEffectRipple`
> (`0x18007AE1F`, 46 octets) devient un **balayage de 30 octets sur une table
> à terminateur** — le nombre d'entrées quitte le CODE pour les DONNÉES. »

Mesuré dans la DLL en place : `0x18007AE1F` porte

    mov    r15d, edx
    lea    rdx, [rip+...]      -> 0x180EC2D30, dans `.decors`
    cmp    dword [rdx], -1 / je  ; cmp eax,[rdx] / je ; add rdx,0x2C ; jmp

et la table de `0x180EC2D30`, pas `0x2C`, porte **cinq décors : 4, 15, 53, 64,
72** — `ban`, `slk`, **`sk5`**, `ncb`, **`skb`**. C'est `--decors-vf5` et
`--decors-5r` qui la posent, et `decors.md` §20.1 le portait comme un reste
parce qu'il a été **fait depuis**.

**Donc `TaskEffectRipple` s'initialise bien sur `skb`.** Ses trois tampons
sont alloués, la passe 4 est prise, `gestionnaire+0x328` est posé à 1.

### 10.2 Ma faute, et elle était trouvable sans rien lancer

J'ai lu l'**oracle** (`.origine`) et conclu sur le **binaire qui tourne**.
C'est le paragraphe 4.1 de `CLAUDE.md`, mot pour mot : « la sonde parle-t-elle
déjà ? » — et ici la réponse était dans la sortie du patcheur, du tour que je
venais de faire, en clair, avec l'adresse exacte du site.

Le contrôle qui manquait existait aussi : je n'ai jamais comparé les 46 octets
du site **entre `.origine` et la DLL produite**. Je n'ai comparé que les deux
identifiants de la table de `.data` — identiques dans les deux, forcément,
puisque le socle n'y touche pas : il change le CODE et met sa table ailleurs.

### 10.3 Ce que j'ai posé, et qui est défait

`--eau-ondes` : une garde refaite dans `.greffe`, 46 octets au même site. Elle
**écrasait celle du socle**, et en pire — quatre entrées au lieu de cinq, le
décor 64 (`ncb`) perdu.

Défait, et vérifié par empreinte :

| fichier | état rendu |
|---|---|
| `tools/patch_moteur.py` | 161 887 octets, sha256 `9ee7e0561ee4d78d…` — identique à la sauvegarde d'avant |
| la DLL en place | sha256 `339429e1892cb80b…` — exactement l'empreinte que `ram/patch_empreinte.json` enregistre |

Il ne reste rien de `--eau-ondes` : ni le mot, ni la zone, ni la branche.

### 10.4 Ce qui tient de la section 9, et ce qui tombe

**Tient** — mesuré, et indépendant de la garde :

* `TaskEffectRipple` est entière dans ce build, RTTI compris ;
* **tous ses nuanceurs sont montés** : `ripple.0.vp` 1/1, `ripple.0.fp` +
  `ripple.1.fp` 2/2, contrôle de la base mixte 4206/4206 ;
* l'enregistrement de `slk` porte en `+0x20` la texture **9207**, que §1.2
  avait convertie en PNG et regardée : 256² de **bleu pur**, la normale
  **plate**. C'est bien la tâche des ondes qui fabrique le relief, et une
  normale plate éclairée comme du sable donne du sable.

**Tombe** : que la tâche ne s'initialise pas, que la garde soit un obstacle,
et toute la section 9.6 (le choix entre repointer un dword et greffer) — il
n'y a rien à choisir, c'est déjà fait.

### 10.5 Le contrôle qui aurait trouvé la faute, et il est posé

`tools/controle_decors_poses.py` porte maintenant l'inverse de ce que je
croyais : il part du **site**, suit le `lea`, parcourt la table et exige que
**53 et 72** y soient.

    DLL en place : EN PLACE -- balayage sur la table de 0x180EC2D30,
                   5 decors : 4, 15, 53, 64, 72
    .origine     : PAS DE BALAYAGE -- 0x18007AE1F porte encore les deux cmp
                   deroules du .origine

Il échoue sur une faute réelle (une ligne d'options qui perdrait
`--decors-vf5`) et réussit sur l'état juste. Les deux sont vérifiés.

### 10.6 Où en est l'eau, vraiment

| pièce | état |
|---|---|
| la simulation `TaskEffectRipple` | **déjà servie** sur 53 et 72, depuis les options de décors |
| le nuanceur `water01` (rangs 100/106) | posé le 2026-11-19, **jamais vu à l'écran** |
| `WATRING` présence | posé, mauvais objet, inoffensif |

Il reste donc **une course**, et une seule question ouverte : est-ce que
`gestionnaire+0x328`, le drapeau que la tâche pose, est **lu** quelque part ?
Son voisin `+0x330` (WATER_RING) a été prouvé non lu par point d'arrêt
matériel. Ce n'est pas mesuré pour `+0x328`.
---

## 11. LE MÊME FAIT, POUR L'EAU : LE DÉCOR D'EILEEN N'A JAMAIS ÉTÉ CHARGÉ (2026-11-20)

Mesuré en même temps que `brume_decor_aoi.md` §18.8, et ça vaut mot pour mot
ici. Les **486** journaux archivés, grepés tous sur la ligne de l'hôte
`[419.185] … decor [+0x5C]=`, donnent **tous** les décors jamais chargés :

    -1 : 44     0 : 202     4 : 24     7 : 56      9 : 20
    11 : 38    13 : 10     16 : 20    19 : 3491   20 : 22

**Ni 15 (`slk`), ni 53 (`sk5`), ni 72 (`skb`).** Le `ban` (4) y est 24 fois —
et c'est le seul décor à ondes qui ait jamais tourné.

Donc le balayage des ondes du §10.1, les deux nuanceurs de `--eau-water01` et
la présence `WATRING` n'ont **jamais** été regardés sur un décor d'Eileen. La
question ouverte du §10.6 — `gestionnaire+0x328` est-il lu ? — ne se mesure
pas avant d'avoir chargé 53 ou 72.

Et le même verrou : `ImposerLeDecor` (SS 419.254) refuse tout numéro
`>= 0x29`, donc 53 et 72 autant que 48. **Une constante dans
`vf5fs_host.cpp`, la même pour les deux chantiers.**
---

## 12. CORRECTION DE LA SECTION 11 : LE MÊME GREP, LA MÊME FAUTE (2026-11-20)

La section 11 conclut de 486 journaux que `slk`, `sk5` et `skb` n'ont jamais
été chargés. **C'est faux, et pour la raison exposée dans
`brume_decor_aoi.md` §19 :** 485 de ces journaux sont sous `FS REVO/`, ils
viennent de l'hôte REVO et d'un module sans aucun décor ajouté — d'où le fait
qu'aucune valeur n'y dépasse 20. Les journaux de l'APM3 (`apm_journal*.txt`,
`quest_journal*.txt`) **ne nomment pas** le décor choisi en versus.

**Donc on ne sait pas, par le journal, quels décors d'Eileen ont tourné.**
Seul l'écran le dit, et c'est Frédéric qui le mesure.

Ce qui tient du §11 : rien, sauf le fait que `ImposerLeDecor` refuse tout
numéro `>= 0x29` — vrai, mais ce n'est pas un préalable puisque le décor se
choisit à la main.

Ce qui reste donc ouvert pour l'eau, exactement comme avant le §11 : le
balayage des ondes est en place sur 53 et 72 (§10.1), `--eau-water01` est posé,
et **il faut demander à Frédéric ce que la surface donne sur `sk5` et `skb`**
avant d'en déduire quoi que ce soit.
---

## 13. FRÉDÉRIC : TOUJOURS PAS D'EAU DANS LE NIVEAU VF5 D'EILEEN (2026-11-20)

Mesure d'écran, rapportée pendant la séance : **`sk5` ne montre toujours pas
d'eau.** C'est la seule mesure qui tranche (`CLAUDE.md` §3), et elle est
négative.

Ce qui était en place quand il a regardé — tout vérifié par empreinte le même
jour (§10, §12) :

| pièce | état |
|---|---|
| le balayage des ondes de `TaskEffectRipple` | en place, table de `0x180EC2D30`, cinq décors dont **53** et **72** |
| les nuanceurs de `ripple` | vp 1/1, fp 2/2 |
| `--eau-water01` (rangs 100 et 106) | posé |
| `--eau-presence` (WATRING) | posé |

**Donc la tâche des ondes s'initialise sur `sk5` et il n'y a rien à l'écran.**
Les trois pièces posées ne suffisent pas, et la question du §10.6 devient la
question centrale : **`gestionnaire+0x328`, le drapeau que l'init pose, est-il
LU quelque part ?** Son voisin `+0x330` (WATER_RING) a été prouvé non lu par
point d'arrêt matériel ; `+0x328` ne l'est pas.

À mesurer avant de reposer un octet, et dans cet ordre :

1. si `+0x328` est lu — et le même doute vaut pour la **passe 4**
   (`FUN_18010CA20(4,1)`) que l'init réclame, exactement comme pour
   `TaskEffectFogRing` (`brume_decor_aoi.md` §21.5) ;
2. si le rappel de dessin de l'init (`LAB_18007B470`) est appelé.

**Les deux chantiers butent maintenant sur la même question** : une tâche qui
s'initialise, prend sa passe, enregistre son dessin — et ne paraît pas.
C'est un seul défaut à chercher, pas deux.
