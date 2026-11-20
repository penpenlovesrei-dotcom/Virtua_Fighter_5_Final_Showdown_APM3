# L'EAU DU DÉCOR D'EILEEN (`slk`) — CE QUE LA CONSOLE FAIT ET QUE LE PORTAGE A PERDU

Mesuré le 2026-10-15 sur l'image PowerPC de **Virtua Fighter 5 Xbox 360**
(`VF5 FS DECOMP\X360_VF5\default.xex`, déchiffré par `tools/xex.py`, clé
commerciale, base `0x82000000`, image de 15 663 104 octets commençant par `MZ`).
C'est la génération console de 2007 — celle des captures de référence.

Le `EBOOT.BIN` PS3 a ses segments **chiffrés** (aucune chaîne en clair,
`TaskEffectWaterRing` introuvable) : il n'est pas mesurable ici.

---

## 1. La tâche est la même partout

`TaskEffectWaterRing::init`, Xbox 360, `0x821C92D0` :

    call [vtbl+0x24](this, 1)      ; -> 0x821B7B38 : [this+0x50] = 1
    call [vtbl+0x28](this, 0)      ; -> 0x821C0DA8 : [this+0x54] = 0
    r3 = 0 ; bl 0x8224B088         ; -> stb r3, 0x5D(0x8284C79C)
    trace("TaskEffectWaterRing::init()")

Même forme chez Lindbergh ver.B (`0x839596A` → `0x80FB9A0` → `[0x8800331]`) et
chez APM3 (`0x180085640` → `[0x180677330 + 0x330]`). **La tâche n'a jamais rien
dessiné, dans aucune version** : elle pose un drapeau, et c'est tout.

## 2. Mais côté console, le drapeau EST LU

Balayage de toute la section exécutable pour `lbz rT, 0x5d(rA)` : **trois**
lectures, `0x8224B674`, `0x8234CEE4`, `0x8234CF30`. Celle de `0x8224B674` :

    8224B668  lbz   r11, 3(r31)       ; un premier drapeau
    8224B670  beq   -> tout sauter
    8224B674  lbz   r11, 0x5d(r31)    ; LE DRAPEAU WATER_RING
    8224B67C  beq   -> tout sauter
    8224B680  lwz   r11, 0xfc(r31)    ; l indice pose par la mise en place
    8224B688  addi  r10, r31, 0x11c   ; la table des anneaux d eau
    8224B694  lwzx  r11, r11, r9      ; redirection par [r29+0xC + indice*4]
    8224B698  r11 *= 0x24             ; des enregistrements de 36 octets
    8224B6A4  r27 = r31+0x11C + r11*0x24
    8224B6AC  bl 0x8224CAC8           ; ET IL DESSINE
    8224B6BC  stw   r11, 0x9c(r30)    ; il note que c est fait

`0x8224CAC8` encadre l'appel de deux marqueurs GPU (`0x82359788` avec `0x84C0`)
et soumet le tracé par `0x82359830` → `0x82357DC0`.

**Chez APM3, ce champ (`[gestionnaire + 0x330]`) n'est lu NULLE PART.** Établi
deux fois : au désassembleur sur tout le `.text` (86 instructions touchent un
déplacement `0x330` ; les seules lectures d'un mot sont deux variables de pile
dans une fonction sans rapport), puis **au point d'arrêt matériel** (DR0, 4 o,
lecture ou écriture) posé sur `0x180677660` pendant 115 s de combat sur le
décor 72 : **un seul accès, l'écriture de la tâche elle-même**.

## 3. La console a, PAR DÉCOR, un bloc d'anneau d'eau

Le câblage n'est pas dans la tâche, il est dans la mise en place du décor,
`0x822C3EF8` :

    r11 = [r31+0x58]        ; le descripteur du decor
    r30 = [r11+0x5C]        ; LE BLOC WATER_RING DU DECOR
    si r30 == 0 -> on saute tout          ; pas de bloc = pas d eau
    r3 = [r30+0] ; bl 0x8224B048          ; [gestionnaire+0xFC] = cet indice
    r3 = 1       ; bl 0x8224B088          ; [gestionnaire+0x5D] = 1

Descripteur console d'Eileen : **`0x82081B68`**, pas **`0x70`** (le suivant est
`STGYUK`). Champs utiles :

    +0x00  -> "STGSLK"                 +0x04  -> "EFFSTGSLK"
    +0x40  -> "rom/STGSLK_COLI.000.bin"
    +0x4C  -> "rom/sound/bgm/vf5b_slk.adx"
    +0x58  -> 0x820814A8   (un bloc de sept 1)
    +0x5C  -> 0x820814CC   LE BLOC WATER_RING, NON NUL

et le bloc lui-même fait douze octets : `{1, 0, 0}`. L'indice d'anneau d'eau
d'Eileen vaut donc **1**.

## 4. Et les shaders console sont plus riches

    water_ring   Lindbergh / APM3 : 3 bits de permutation,  8 programmes
                 Xbox 360         : 5 bits,                16 programmes .fp
    water01      Lindbergh / APM3 : 10 bits
                 Xbox 360         : 11 bits, 608 chaines

Le `water_ring` de Lindbergh (source ARB lisible) est **purement diffus** :

    TEX col, texture[1] ; TEX normal, texture[2] ; TXL lc, texture[6]
    TXL diff, normal, texture[9], CUBE      ; cube d IRRADIANCE, par la NORMALE
    MUL o_color, diff, col                  ; aucune alpha en sortie

Aucune de ses quatre permutations n'a de transparence, de reflet ni de
spéculaire. Le cube y est un cube d'ambiance, pas un miroir.

Les reflets, la réfraction et le vrai cube mapping sont dans **`water01`**, le
shader du grand plan `eff_water` :

    TEX cube_map,    reflect_vec,    texture[5],  CUBE   ; cube par le REFLET
    TEX reflect_map, screen_uv,      texture[15], 2D     ; reflet espace ecran
    TEX refract_map, screen_uv.zwww, texture[14], 2D     ; REFRACTION
    DP3/SUB_SAT/POW p_fresnel                            ; FRESNEL
    MOV o_color.a, color_map                             ; et il ECRIT l alpha

## 5. Conclusion

Sur le moteur APM3, l'anneau d'eau d'Eileen **ne peut pas être rendu comme sur
console** : le drapeau existe, la tâche le pose, et le consommateur a disparu
du portage. C'est le même défaut que celui relevé le 2026-09-11 pour
`SNOW_RING` (« aucun décor de FS ne crée SNOW_RING »), mais mesuré jusqu'au
bout cette fois.

---

## 6. LE SHADER DE L'ANNEAU D'EAU A ÉTÉ AMPUTÉ (mesure du 2026-10-15)

**Correction d'une prémisse** : `extracted\APM3_FS_farc\shader\` n'est PAS
l'archive d'APM3 — c'est l'extraction de celle de Lindbergh FS, octet pour
octet (`water_ring.000.fp` y commence par `!!ARBfp1.0`). La vraie archive
d'APM3 est `VF5 FS DECOMP\APM3_US\runtime\media\vf5fs\vf5fs_media\w64\
shader_pxd_w64.farc`, 10 530 083 o, 3950 entrées, corps DXBC `ps_5_0`.

### Les quatre formats

    LIND FS   FArC gzip   2724 entrees   ARB texte
    APM3      FArc brut   3950 entrees   GSPS/GSVS/GSFX -> DXBC a +0x80
    PS3       FArC gzip   4531 entrees   CgBinaryProgram gros-boutiste, ucode RSX
    X360      FArc brut   4744 entrees   en-tete 0x28 + CTAB D3D9 gros-boutiste

Aucun chiffrement : `tools/farc.py` ouvre les quatre.

### Les unités de texture de `water_ring`, par plateforme

| | LIND FS / APM3 | PS3 / X360 |
|---|---|---|
| textures | `1`, `2`, `6`, [`7`], **`9` CUBE** | `0,1,2,3,`**`4`** toujours ; + [**`5` CUBE**], [`6`], [`7`] |
| varyings | tex_color0, tex_normal0, tex_shadow0 | idem **+ a_color0, a_color1, a_eye, a_position** |
| constantes | `env[12]`, `env[13]`, `light[1].diffuse` | **`env[0]`, `local[1]`, `local[2]`, `local[4]`, `material.specular`** |
| instructions | 13 ARB / 16 DXBC | **31 a 48** |

Rôles des unités, établis par l'inventaire des 2724 programmes ARB :
`4` = la **carte de transparence** (`a_tex_parency`), `5` = le cube
d'environnement par le **vecteur de reflet**, `9` = le cube d'**irradiance**
par la normale, `14`/`15` = refraction/reflet en espace ecran.
`local[1]` = `p_intensity`, `local[2]` = `p_reflect_refract_uv_scale`,
`local[4]` = `p_fresnel`, `env[0]` = `p_fb_isize`.

Donc la console a, sur l'anneau d'eau : **la transparence** (unite 4), **le
reflet** (cube unite 5 par le vecteur de reflet) et **le Fresnel**
(`local[4]` + `a_eye`). Final Showdown n'a rien de tout cela — son cube de
l'unite 9 est de l'ambiance diffuse, pas un miroir.

### La preuve la plus propre : le programme de SOMMETS est resté intact

`water_ring.000.vp` (LIND FS) et `water_ring.00000.vp` (PS3) ont **la meme
signature**, y compris :

    TEX displace, a_tex0, texture[14], 2D      ; une CARTE DE HAUTEUR qui
                                               ; deplace le maillage
    sorties : o_eye, o_color_f1 (hauteur de vague + speculaire)

**Final Showdown calcule toujours ces sorties, et son fragment shader ne les
emploie plus.** L'anneau d'eau de FS est un fragment shader ampute derriere un
vertex shader intact. Et APM3 est le portage exact de ce fragment shader
ampute, instruction par instruction (seul ajout : l'inversion du X de la
normale).

### `water01`, lui, n'a pas bouge

Les 96 jeux d'unites distincts de `water01` sont **exactement les memes** sur
LIND, PS3 et X360. C'est `water_ring` qui a ete reduit, pas le reste.

---

## 7. LA CHAÎNE COMPLÈTE, LUE DANS LE MOTEUR LINDBERGH ver.B

Et elle **corrige** le §2 : chez ver.B le drapeau EST lu. Il n'était pas
trouvable en absolu parce qu'il est lu en `[ebx+0x51]`, `ebx = 0x88002E0`.

### Ce que `TaskEffectWaterRing` fait vraiment

Vtable `0x86045C8`. Créneau 2 `init`, 3 `ctrl`, 4 `dest`, **5 `disp`**, 7
`pre_init`. `init` ne fait qu'une remise à zéro du drapeau (`0x8395A5E` perd
son 2e argument et saute sur `0x80FB9A0(0)`) ; c'est le CHARGEUR de décor qui
le met à 1 ensuite.

**`disp` (`0x8395A0E`) est tout le rendu** : il appelle `0x8395A7A`, qui
enregistre un **rappel de dessin par objet** sur `0x170005` =
objset 0x17 (`STGSLK`) rang 5 = **`STGSLK_WATER_RING`**, le vrai maillage.
`WaterRing` est la seule tâche d'effet à se greffer sur un maillage de décor ;
`Leaf`, `Ripple` et `SnowRing` se greffent sur des objets `DUMMY`.

Le rappel `0x8395AA0` :

    0x80FB42C(0) -> cible « reflet »       -> 0x80FD6F4(.,3) = GL_TEXTURE3
    0x80FB42C(1) -> cible « refraction »   -> 0x80FD6F4(.,4) = GL_TEXTURE4
    0x80DFCC2 / 0x80E100C / 0x80E0408      -> le trace du maillage

### Le descripteur de décor porte le bloc

Table `0x852F220`, pas `0x70`, **28 décors**. `slk` = indice 15 = `0x852F8B0`.

    +0x58  descripteur « reflet »       slk -> 0x852FEB4 = {1,1,1}
    +0x5C  descripteur « REFRACTION »   slk -> 0x852FED8 = {1,0,0}

**Seuls `jin` et `slk` ont un bloc de refraction ; les 26 autres ont 0.**

Le chargeur `0x80C7BFC`, en fin de chargement :

    si [desc+0x5C] != 0  ET  cumul VRAM < 20.0 Mo  (seuil 0x852F160) :
        0x80FB4A0(3, 1)          autoriser la passe 3
        0x80FB812(*[desc+0x5C])  0x88003F0 = le numero de variante
        0x80FB9A0(1)             byte[0x8800331] = 1

### Les cibles de rendu, tailles mesurées

Table `0x8657800`, 13 enregistrements de 0x18 :

    slot 0  reflet       512 x 256  RGBA8 + DEPTH24
    slot 1  REFRACTION   512 x 256  RGBA8 + DEPTH24      <- slk et jin
    slots 4,5,6          256 x 256  RGBA32F, sans profondeur

Passe 2 = technique `"S_REFL"`, **passe 3 = `"S_REFR"`** (`0x80FC0B0` :
bind FBO, `glViewport`, `glClear`, listes 0x10/0x12/0x11).

### Le lecteur du drapeau

`0x80FC488` (passe 7), seul lecteur, `0x80FC538` :

    if (passe 3 autorisee) {
        [0x8800C04] = 1
        if (byte[ebx+0x51])  ->  lier la cible de refraction sur GL_TEXTURE14
                                 [0x8800C00] = 1          <- un bit de VARIANTE
    }

`0x8800BFC/C00/C04` composent les bits qui choisissent parmi les **32**
`water_ring.*.fp` de ver.B.

### L'animation des vagues appartient à `Ripple`, pas à `WaterRing`

`TaskEffectRipple` est **autonome** : il s'autorise la passe 4, s'y inscrit, et
son rappel `0x8393254` fait un ping-pong sur **trois cibles 256x256 RGBA32F**
(`glScissor` à 1 px pour que l'onde ne reboucle pas), puis publie sa texture
dans `0x88005CC`. `WaterRing` ne produit rien : il **consomme** deux cibles
remplies par d'autres passes.

### ET LA RÉGRESSION N'EST PAS DANS LE PORTAGE PC — ELLE EST DANS VF5 R

Chez VF5 R, le descripteur fait `0x8C` octets (table `0x87738A0`, 40 décors) et
le chargeur `0x8108CF8` lit `[desc+0x6C]` pour le reflet et **`[desc+0x70]`
pour la refraction**. Le reflet reste renseigné pour neuf décors.
**`+0x70` vaut 0 pour les quarante.** Le seul site qui met le drapeau à 1
(`0x8109132`) est dans ce bloc gardé : il ne s'exécute jamais.

Et le programme `water_ring` passe de **32 variantes `fp` à 4**.

Donc : **l'anneau d'eau est mort dès VF5 R**, une génération avant le portage
PC. Final Showdown hérite de R, et APM3 hérite de FS. La seule génération qui
l'ait jamais eu est ver.B — c'est-à-dire les consoles, c'est-à-dire exactement
la capture de reference.

---

## 8. LE MOTEUR APM3 : LE SYSTÈME DE PERMUTATIONS, DÉCODÉ

### Les tables

    0x180554350   49 shaders de materiau, 0x28 chacun
                  +0x00 nom  +0x18 nb de chiffres  +0x20 indices d etat
    WATER01 @ 0x180554710 : id 24, 10 chiffres = etats [23,22,37,41,43,44,38,47,49,15]
    WATRING @ 0x180554760 : id 26,  3 chiffres = etats [49,46,24]
    0x180715440   la table d etat, 50 mots
    0x180175680   le constructeur de cle : un nombre a BASE MIXTE,
                  chiffre de poids faible en tete

### Ce que chaque chiffre de `water01` allume (verifie sur les sources ARB)

| chiffre | etat | ce qu il allume |
|---|---|---|
| 2 | 37 | `texture[0]`, puis `[1]` |
| 3 | 41 | `texture[2]`, la normale |
| **4** | **43** | **`texture[15]`, le REFLET en espace ecran** |
| **5** | **44** | **`texture[14]`, la REFRACTION** |
| **6** | **38** | **`texture[5]`, le CUBE par le vecteur de reflet** |
| 7 | 47 | `texture[3]`, le speculaire |
| 9 | 15 | terme d alpha / Fresnel |

Les etats 43 et 44 ne sont ecrits qu en `0x18010B294` et `0x18010B2EE` --
exactement les deux sites qui lient les unites 15 et 14.

### Le seul bit qui separe ver.B de FS

`materiau+0x04` bit **15** (`0x8000`) -> etat 38 -> chiffre 6 -> **le CUBE**.
Avec `0x0101` (ver.B) le cube ne peut PAS apparaitre.

### ET LE COUP DE MASSUE : 4 PROGRAMMES DE FRAGMENTS SUR 192 SONT CHARGES

L init `0x180175BF0` ne charge un programme que si une **table de presence**
(`sousShader+0x38`) porte 1 pour cette permutation. Sinon l identifiant reste
a 0 et rien n est lie. Pour `WATER01`, quatre seulement :

    rang 105  water01.0001100001.fp   normale + REFLET
    rang 123  water01.0001001001.fp   normale + CUBE
    rang 129  water01.0001101001.fp   normale + REFLET + CUBE
    rang 130  water01.0011101001.fp   tex0 + normale + REFLET + CUBE

1. **Aucune n a le chiffre 5** : la refraction en espace ecran n existe pas
   dans ce build, quoi qu on fasse.
2. Les deux rangs atteignables avec `0x0101` (100 et 106) sont **ABSENTS** :
   le materiau de ver.B ne peut aboutir a AUCUN programme de fragments.
3. Le rang 124 (`0x8529` SANS reflet) est **absent** ; le rang **130**
   (`0x8529` AVEC reflet) est **present**. Le build de FS n a garde la
   permutation que pour un decor ou le reflet est ALLUME.

Les 3950 programmes sont pourtant **tous dans l archive sur le disque**
(`w64/shader_pxd_w64.farc`, meme ensemble de noms que la table `0x18064E4E0`).
C est la table de presence du `.dll` qui les ecarte, pas l archive.

### Les passes de reflet et de refraction EXISTENT dans APM3

Repartiteur `0x18010C330`, un octet d autorisation par passe.
Passe **2** = reflet (`0x18010B570`, technique `"S_REFL"`), passe **3** =
refraction (`0x18010B940`, `"S_REFR"`). Onze cibles de rendu allouees sans
condition (`0x1803A4FD0`) : les cibles 0 et 1 font **512 x 256**.

Elles sont allumees a l activation du decor, `0x18018FA59` :

    rbx = [[tacheDecor+0x68] + 0xC0]
    si rbx == 0 -> RIEN
    0x18010CA20(2,1) ; [gest+0x15C] = indice ; 0x18010C9E0(1)   ; REFLET
    puis, si le budget 20.0f passe : passe 3 + 0x18010C9F1(1)    ; REFRACTION

**Et `TaskEffectWaterRing::init` ETEINT la refraction** : `0x18008564C`,
`xor ecx,ecx ; call 0x18010C9F0`.

### Le volume de code, les trois taches au banc

| classe | fonctions | octets |
|---|---|---|
| `TaskEffectRipple` | 25 | **6 421** |
| `TaskEffectSplash` | 27 | **6 563** |
| **`TaskEffectWaterRing`** | **3** | **186** |

Un rapport de 1 a 35. Son `disp` ne fait que redessiner l objet `0x27006E`,
le meme disque que la liste d affichage du decor dessine deja.

### CE QUI RESTE A MESURER, ET C EST LE SEUL VERROU

`[donneesDecor + 0xC0]` est-il non nul pour `slk` / `skb` ? C est lui qui
allume la passe de reflet. S il l est, le materiau `0x8529` choisit le **rang
130**, qui porte le reflet ET le cube. Sinon le rang 124, qui n est pas
charge, et rien ne s affiche.
