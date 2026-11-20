# LA BRUME DU DÉCOR D'AOI (`jin` / `jn5`) — LUE DANS LA LINDBERGH VF5 R

Relevé le 2026-11-19. **Aucune course, aucun lancement.** Tout ce qui suit est
lu dans des fichiers : l'ELF Lindbergh de VF5 R, les trois archives de
nuanceurs, la DLL du moteur et les `light_param/*.txt`.

Désassemblages déposés dans
`FS APM3/desassemblage/brume_aoi_lindbergh_r/` (voir son `README.md`).

Cette note **continue** `documentation/brume_anneau_aoi.md`, qui s'arrêtait à
sa section P : « les deux registres sont remplis, aux bonnes adresses, avec les
bonnes valeurs, et Frédéric ne voit aucune nappe ». **La raison est trouvée, et
elle n'est pas dans le moteur : elle est dans le nuanceur.**

---

## 1. Comment la brume est décrite dans les données — et ce que notre build en fait

### Le fichier, et le champ

`rom/light_param/fog_<code>.txt`, en texte clair, **trois groupes**
(`group_start 0/1/2`), chacun avec `type`, `density`, `linear` (deux valeurs) et
`color` (quatre). Lu dans la fonction VF5 R `0x0811715E` (§2), un groupe est en
mémoire un enregistrement de **0x24 octets**, neuf champs — huit viennent du
fichier :

| offset | champ | accesseur VF5 R | sert à |
|---|---|---|---|
| +0x00 | `type` (entier) | `0x081170D0` | **0 ⇒ `glDisable(GL_FOG)` et on sort** ; sinon `glFogi(GL_FOG_MODE, …)` : 1 → `GL_LINEAR` (0x2601), 2 → `GL_EXP` (0x800), 3 → `GL_EXP2` (0x801) |
| +0x04 | `density` | `0x081170DA` | `glFogf(GL_FOG_DENSITY)` |
| +0x08 | `linear` début | `0x081170E6` | `glFogf(GL_FOG_START)` |
| +0x0C | `linear` fin | `0x081170F2` | `glFogf(GL_FOG_END)` |
| +0x10 | entier | `0x081170FE` | `glFogi(GL_FOG_INDEX, …)` — champ absent du fichier texte |
| +0x14…+0x20 | `color` R G B A | `0x0811710A` (quatre pointeurs de sortie) | `glFogfv(GL_FOG_COLOR, couleur × 0,125)` |

Le test `type == 0 ⇒ glDisable(GL_FOG)` est fait **avant** l'aiguillage de
groupe, donc pour les trois ; tous les autres appels GL de la colonne de droite
ne concernent que le **groupe 0**, et pour les groupes 1 et 2 le `type` n'est
testé que « non nul ». *(Les trois groupes de `fog_jn5.txt` ont `type 1`.)*
Les talons PLT
ont été résolus par `.rel.plt` : `glFogi 0x080532F8`, `glFogf 0x08051D08`,
`glFogfv 0x08051C58`, `glEnable 0x08053768`, `glDisable 0x080525E8`,
`glProgramEnvParameter4fARB 0x08053A98`.

Table des trois groupes : `0x08A9C400` en `.bss`, pas de 0x24. Valeurs par
défaut posées par `0x081174A8` : `type=0, density=0, 20.0, 1000.0, …`.

### Et le groupe 1 EST le brouillard de hauteur

C'est le fait neuf, et il tranche : **ce n'est pas une déduction, c'est le
`cmp ebx, 1 / je` de `0x08117189`.**

| groupe | ce que VF5 R en fait |
|---|---|
| **0** | brouillard de **distance** : `glFogi(GL_FOG_MODE)`, `glFogf(GL_FOG_DENSITY/START/END)`, `glFogi(GL_FOG_INDEX)`, `env[4]` fragment = la couleur brute, puis `glFogfv(GL_FOG_COLOR, couleur × 0,125)` (`[0x08775A18] = 0,125`) et `glEnable(GL_FOG)` |
| **1** | brouillard de **HAUTEUR** : `env[14]` sommet = `(density, début, fin, 1/(fin−début))`, `env[11]` fragment = la couleur RGBA |
| **2** | troisième registre : `env[19]` sommet, même quadruplet |

### Les valeurs du décor d'Aoi

`FS APM3/banc_revo/vf5fs_media/rom/light_param/fog_jn5.txt` est **octet pour
octet** le `fog_jin.txt` de VF5 R (`diff` muet). Son groupe 1 :

    density 1.00000
    linear  -2.50000 1.00000
    color   0.700000 0.900000 1.00000 1.00000

donc `env[14] = (1,0 ; −2,5 ; 1,0 ; 0,285714)` — car `1/(1 − (−2,5)) = 1/3,5`.
La constante `1,0` du numérateur est lue en `0x08764570`.

*(Note au passage : la greffe du 2026-10-18 écrivait `env[14] = (1, −1, 0,
0,285714)`. Le `w` était juste, le `y` pas — il vaut **−2,5**, pas −1 — et le
`z` vaut 1,0. Le `z` n'est de toute façon pas lu par le nuanceur.)*

### Quels décors ont une brume de hauteur, des deux côtés

| | décors avec groupe 1 actif |
|---|---|
| **VF5 R** | `du2`, `du3`, **`jin`**, `slk` |
| **Final Showdown** (APM3 et Lindbergh) | `du2`, `du3`, `du5`, `slk` — **`jin` a été mis à densité 0** |

Final Showdown n'a donc pas supprimé le mécanisme : il a éteint la brume
d'Aoi **dans la donnée**, et en a ajouté une à `du5`. Notre `jn5` porte la
donnée de R, intacte. Détail dans
`desassemblage/brume_aoi_lindbergh_r/donnees_groupe1_densite.txt`.

### Ce que notre build en fait aujourd'hui : rien, et c'est mesuré en trois temps

1. le fichier est lu et le groupe 1 est bien celui de R (ci-dessus) ;
2. la DLL sait décrire `env[11]` et `env[14]` (`0x1800F2470`, §3) ;
3. **mais le programme de sommets qui devrait les lire met la sortie de
   brouillard à zéro en dur** (§4), et **aucune permutation « hauteur » n'est
   chargée** pour les familles du décor (§5).

---

## 2. Comment la Lindbergh VF5 R le rend — les fonctions, nommées

ELF `VF5RE/extracted/LIND_R/id/disk0/vf5`, x86-32, pas de `.symtab` ; les noms
donnés ci-dessous sont **descriptifs**, pas d'origine. Les classes RTTI
existent en clair et confirment la fenêtre de mise au point `5FogDw` avec ses
`GroupListBox`, `TypeListBox`, `DensitySlider`, `LinearSlider`, `ColorSlider` —
c'est-à-dire exactement les champs du §1.

| adresse | ce qu'elle fait |
|---|---|
| `0x0811715E` | **appliquer_groupe(indice)** — l'unique aiguillage. `lea edi, [eax*4 + 0x8A9C400]` avec `eax = indice*9` : le pas est 0x24 |
| `0x081170D0` / `DA` / `E6` / `F2` / `FE` | lire `type` / `density` / `début` / `fin` / l'index de brouillard |
| `0x0811710A` | lire la couleur RGBA dans quatre pointeurs |
| `0x08117496` | `&table[indice]` |
| `0x081174A8` et `0x081174E6` | remise aux valeurs par défaut |
| `0x08117482` | `glDisable(GL_FOG)` |
| `0x08142304` / `0x08142310` / `0x0814231C` | la **passe de décor** : `appliquer_groupe(0)`, `(1)`, `(2)`, à chaque trame, sans condition |
| `0x08053A98` / `0x080540C8` | les talons PLT de `glProgramEnvParameter4fARB` / `4fvARB` |

Le chemin du groupe 1, lu instruction par instruction
(`vf5r_appliquer_groupe_0811715E.txt`, 0x081171F2 → 0x081172DA) :

    0x081171F2  density        -> argument x
    0x08117201  début          -> argument y
    0x08117212  fin            -> argument z
    0x0811724B  xmm1 = fin − début
    0x0811724F  xmm2 = 1,0 / (fin − début)      [0x08764570] = 1,0
    0x08117266  [esp+4] = 0x0E                  l'index 14
    0x0811726E  [esp]   = 0x8620                GL_VERTEX_PROGRAM_ARB
    0x08117275  call glProgramEnvParameter4fARB

    0x08117299  0x0811710A(groupe, &r, &g, &b, &a)
    0x081172B6  [esp+4] = 0x0B                  l'index 11
    0x081172BE  [esp]   = 0x8804                GL_FRAGMENT_PROGRAM_ARB
    0x081172C9  call glProgramEnvParameter4fARB

### Le nuanceur, côté VF5 R

Archive `/shader.farc`, **sortie pour cette analyse** de l'image ext2
`vf5r_rom.bin` (`tools/ext2.py sortir`, puis `tools/farc.py extract`) :
4 067 programmes ARB. **VF5 R n'a aucune famille `stage_blinn`** — c'est une
famille que Final Showdown a introduite. Ses décors sont rendus par
`blinn_per_vert` / `blinn_per_frag` / `lambert`, et le chiffre de brouillard
de la clé de permutation commande quatre modes :

| mode | sommet | fragment |
|---|---|---|
| 0 | rien | — |
| 1 | `MUL o_fog.x, …, state.fog.params.x` (distance) | `LRP o_color.xyz, a_fogcoord.xxxy, p_fog_color` = `env[4]` |
| **2** | `MUL tmp.x, …` (distance) **puis** `MUL tmp.y, …, env[14].x` (hauteur) **puis `MAX o_fog.x, tmp.x, tmp.y`** | `LRP o_color, a_fogcoord.xxxy, p_height_fog_color` = `env[11]` |
| 3 | `TEX … texture[14]` sur le monde XZ, `−pos_w.y − (−0,6)`, `×2` saturé → `o_fog.x` | `env[11]` |

Le mode 2 **combine les deux brumes par un `MAX`** et c'est ce `MAX` qui porte
le résultat à la sortie. Retenir : la brume de hauteur n'est pas un
remplacement du brouillard de distance, c'est un maximum avec lui.

### L'appariement avec APM3

| | VF5 R (Lindbergh) | APM3 (Windows) |
|---|---|---|
| appliquer un groupe | `0x0811715E` | partie de `0x1800F2470` |
| appel de la passe de décor | `0x08142304/10/1C` | les **quatre** appelants de `0x1800F2470` : `0x18007E625`, `0x180085696` (`TaskEffectWaterRing`), `0x1800F129B`, `0x1800F19E1` |
| poser la valeur d'un `env` | `glProgramEnvParameter4fARB` (PLT `0x08053A98`) | `0x1802475B0` (décrit) + `0x180247430` (marque) |
| téléverser au GPU | le pilote OpenGL | `vfes.exe` `0x14002F430` (Map/Unmap/Set\*ConstantBuffers) |
| `env[14]` sommet | index 14, cible `0x8620` | `0x1800F2A0E` (`mov ecx, 0xE`) et `0x1800F2A53` (la pose) |
| `env[11]` fragment | index 11, cible `0x8804` | `0x1800F2916` (`mov ecx, 0xB`) |

**La chaîne est la même des deux côtés.** La différence n'est pas là.

---

## 3. Le masque `[rdi+0x1C]` : l'énigme de la section J, résolue

`0x1800F2470` déclare les registres `env` un par un, et **chaque registre est
gardé par un bit du champ `[rdi+0x1C]`**, où `rdi = [rcx+8]` :

    0x1800F2A03  mov eax, [rdi+0x1C]
    0x1800F2A0A  test al, 0x20          <-- bit 5
    0x1800F2A0C  je  <on saute>         <-- a 0 : env[14] n'est jamais marque

Ce masque n'est pas un réglage de décor : **tout dit que c'est la liste des
registres que le programme compilé LIT.** Les deux faits qui le soutiennent :
`blinn_per_vert` mode 2 lit `cb[0][14]` et a besoin du bit 5 ; `stage_blinn`
mode 2 ne le lit pas. **Mais je n'ai pas lu le code qui calcule
`[rdi+0x1C]`** — c'est une déduction, pas une mesure (§7).

Si elle est juste, forcer le bit 5 (`74 51` → `90 90`, essai du 2026-10-18)
téléverse `env[14]` **vers un nuanceur qui ne le lit pas**.

C'est pourquoi les sections L, M, O et P n'ont rien donné : les valeurs
arrivaient, l'adresse était bonne, le masque était bon — et le consommateur
était absent. **Le chantier ne butait pas sur le moteur.**

---

## 4. CE QUI MANQUE, CAUSE MESURÉE : le programme de sommets du décor met la brume à ZÉRO

### Côté ARB (documentation du défaut)

Dans `rom/shader.farc` de **Final Showdown Lindbergh** *et* d'**APM3**, la
famille `stage_blinn` — celle que FS a créée pour les décors — a un mode 2
amputé :

    blinn_per_vert, mode 2  (VF5 R ET Final Showdown) :
      MUL tmp.x, _tmp0.w, state.fog.params.x
      MUL tmp.y, _tmp0.w, program.env[14].x
      MAX o_fog.x, tmp.x, tmp.y                  <-- la sortie est ecrite

    stage_blinn, mode 2  (Final Showdown seulement) :
      MUL tmp.y, _tmp0.w, program.env[14].x      <-- tmp.y est MORT
                                                 <-- pas de MAX, pas de o_fog

Recensement des deux archives (identique dans les deux) :

| | programmes de sommets mode 2 avec le `MAX` | sans |
|---|---|---|
| `blinn_per_vert` | 32 | 0 |
| `lambert` | 32 | 0 |
| `constant` | 16 | 0 |
| **`stage_blinn`** | **0** | **8** |

`o_fog` n'est écrit **nulle part** dans ces huit programmes. Le fragment
interpole donc une coordonnée jamais produite, et le `LRP` avec un facteur nul
rend la couleur non embrumée.

### Côté DXBC — c'est la seule archive que notre build charge

La DLL ne nomme qu'une archive de nuanceurs : `w64/shader_pxd_w64.farc`
(chaîne en `0x3FF9D0`). Ni elle ni `vfes.exe` ne portent `rom/shader` ou
`shader.farc`. **Les `.vp`/`.fp` ARB ne sont pas lus par le build Windows** —
ils ne servent ici que de source lisible du même générateur.

Le même défaut est dans le DXBC, et il s'y lit en une ligne :

| permutation | dernière écriture de la sortie de brouillard `o1.w` |
|---|---|
| `stage_blinn.*10.vp` (distance) — 8 sur 8 | `mul o1.w, r0.x, cb[3][5].x` |
| **`stage_blinn.*20.vp` (hauteur) — 8 sur 8** | **`mov o1.w, l(0)`** |

Vérifié sur les dwords bruts : `05000036 00102082 00000001 00004001 00000000`
= `mov o1.w, l(0.0)`, à l'index de dword **386** (offset fichier `0x9A0`) —
exactement là où le mode 1 commence son `dp4 r0.x, cb[2][22], v0`.
Le mode 2 déclare en outre `cb[3]` avec **3** vec4 au lieu de 6 : le tampon de
brouillard n'est même plus lié.

Et les témoins **intacts du même build** existent, ce qui écarte un
malentendu sur le format :

    blinn_per_vert.00000200000.vp :
      70  dp4     r0.w, cb[2][29], v0        ; -pos_w.y
      71  add     r0.w, r0.w, cb[0][14].y    ; - debut
      72  mul_sat r0.w, r0.w, cb[0][14].w    ; * 1/(fin-debut)
      73  mul     r0.w, r0.w, cb[0][14].x    ; * densite
      74  dp4     r1.x, cb[2][22], v0        ; z camera
      75  add     r1.y, r1.x, cb[3][5].y
      77  mul_sat r1.x, r1.y, cb[3][5].w
      78  mul     r1.x, r1.x, cb[3][5].x
      79  max     o2.x, r0.w, r1.x           ; LE MAX, present

Même formule que l'ARB de VF5 R, au mot près. Idem dans `blinn_per_frag` et
`lambert`. **Seule `stage_blinn` est cassée** (8 blobs sur 3 950).

Le **fragment**, lui, est correct des deux côtés : chaque
`stage_blinn.*20.fp` ne diffère de son jumeau `*10.fp` que par **UN dword**,
l'index du registre `env` : `0x04` → `0x0B`, soit `p_fog_color` →
`p_height_fog_color`. Même longueur, 8 paires sur 8.

### Et un second verrou, indépendant : la table de présence

`apm3_presence_nuanceurs.txt` donne les 50 sous-nuanceurs de la DLL et, pour
chacun, les permutations réellement montées (chargeur `0x180175BF0`,
`0x180175D2B : cmp byte ptr [rax+rbp], 0 / je`). Descripteur de `stage_blinn` :
`0x180556430`, présence vp en `0x180556140` (32 octets), présence fp en
`0x180556060` (192 octets). Identique dans `.origine` et `.PATCHEE`.

| famille | vp existants | vp chargés | lesquels |
|---|---|---|---|
| `stage_blinn` | 32 | **2** | `00000010`, `00001010` — chiffre de brouillard **1** |
| `blinn_per_vert` | 128 | 5 | tous en `…1…` |
| `blinn_per_frag` | 64 | 2 | tous en `…1…` |
| `lambert` | 256 | 38 | **deux en `2`** : `00200000`, `00200100` |
| `skin_default` | 16 | 2 | `10000001`, `10010001` |

Les 8 fragments chargés de `stage_blinn` sont `00100010`, `00110010`,
`00101010`, `00111010` et les mêmes en `…11` : **chiffre de brouillard 1
partout**. Aucun programme « hauteur » n'est monté pour les familles du décor.

### Quelle famille, et le nom qui manque

Le moteur porte **40 noms de nuanceurs** (`SHADER_FFP, BLINN, ITEM, SKIN,
HAIR, CLOTH, SKY, EYEBALL, EYELENS, MEMBRAN, GLASS, SIMPLE, LAMBERT,
CONSTANT, PEEL, TONEMAP, REDUCE, MAGNIFY, GAUSS, SUN, FADE, WATER01,
WATER02, WATRING, W_PTCL, SNOW_PT, SNORING, SN_TSL, SN_NRM, FLOOR, PUDDLE,
RAIN, VOLLIT, RIPPLE, FOGPTCL, PARTICL, SHOWVEC, FONT, DEFAULT, CORRECT`,
à partir de `0x1805729D0`) pour **50 descripteurs de sous-nuanceurs**. La
correspondance n'est donc pas un pour un — `hair_default` en a deux à lui
seul — et surtout **il n'y a pas de nom `STAGE` dans la liste** : `stage_blinn`
ne figure pas parmi les noms, pas plus que `shadowmap`, `silhouette`,
`simple_reflect`, `simple_refract`, `ripple_emit`, `fence_alpha` et `movie`.
**Aucun matériau ne peut donc demander `stage_blinn` par son nom.**
Les 384 matériaux de `stgjn5_obj.bin` disent tous `BLINN` (zéro `STAGE`), et le
choix entre
`blinn_per_vert` / `blinn_per_frag` / `stage_blinn` est donc fait par le
moteur — code que je n'ai pas lu (§7).

Et cela change le coût selon la réponse :

| si le décor passe par… | ce qu'il faut |
|---|---|
| **`stage_blinn`** | réparer 8 blobs DXBC **et** allumer la présence |
| **`blinn_per_vert` / `blinn_per_frag`** | **allumer la présence, rien d'autre** |

Car les jumeaux mode 2 des sept permutations BLINN chargées existent tous et
sont tous **intacts** (`cb[0][14]` lu) :

    blinn_per_vert.00000100000 -> .00000200000     intact
    blinn_per_vert.01000100000 -> .01000200000     intact
    blinn_per_vert.00000100010 -> .00000200010     intact
    blinn_per_vert.00000100001 -> .00000200001     intact
    blinn_per_vert.01000100001 -> .01000200001     intact
    blinn_per_frag.00000100000 -> .00000200000     intact
    blinn_per_frag.00000100001 -> .00000200001     intact

### Résumé de la cause

**Deux verrous, tous deux dans la donnée de nuanceurs, aucun dans le moteur :**

1. la table de présence ne monte, pour `stage_blinn`, `blinn_per_vert` et
   `blinn_per_frag`, que des permutations « brouillard de distance » ;
2. et la permutation « hauteur » de `stage_blinn` est **inutilisable telle
   quelle** : son programme de sommets pose `o1.w = 0`.

Le premier explique l'absence de brume avant l'essai du 2026-10-16 ; le second
explique pourquoi l'essai du 2026-10-18, qui avait levé le premier, n'a rien
donné non plus.

---

## 5. En prime : les COMBATTANTS ne peuvent pas être embrumés non plus

Les captures de la borne montrent les jambes des combattants noyées dans la
nappe. Mesuré, et c'est un sujet à part entière :

| | programme de sommets de la peau |
|---|---|
| **VF5 R** `skin_default.0000001.vp` — **l'unique variante avec brouillard** | mode **3** : `TEX texture[14]` sur le monde XZ, `−pos_w.y − (−0,6)`, `×2` saturé → `o_fog.x`, et son fragment emploie `p_height_fog_color` |
| **Final Showdown / APM3** `skin_default.00000001.vp` — l'unique variante | mode **1** : `dp4 cb[2][22]` (z caméra) + `cb[3][5]` → brouillard de **distance** |

Les 16 programmes de sommets de `skin_default` du build Windows **ne lisent
jamais** de paramètre de hauteur (aucun `cb[0][14]`). 48 de ses 96 fragments
emploient `env[11]`, mais **aucun des 24 chargés** : tous les chargés sont en
chiffre 0, donc `env[4]`.

Autrement dit : Final Showdown a **changé le modèle de brume de la peau**, de
la nappe texturée de R au brouillard de distance. Refaire la brume du décor
ne remettra pas les combattants dedans.

---

## 6. Ce qu'il faudrait faire — coût et blocages

### Voie 0, à faire AVANT tout : lire le sélecteur de famille

Si les objets du décor passent par `blinn_per_vert`/`blinn_per_frag`, **il n'y
a rien à réparer dans les nuanceurs** : les sept jumeaux mode 2 sont intacts, et
le seul geste est d'allumer **sept octets de présence vp** et les octets fp
correspondants, plus les deux points « état 22 = 2 ». Coût : quelques octets
dans la DLL, aucune reconstruction d'archive.

Cette question se tranche **sans course**, en lisant qui choisit le
sous-nuanceur pour un matériau `BLINN` (le descripteur de `stage_blinn` est en
`0x180556430`, celui de `blinn_per_vert` en `0x180556370` : il suffit de
remonter leurs lecteurs). **C'est la mesure à faire en premier**, parce qu'elle
départage un geste de quelques octets et une chirurgie de huit blobs DXBC.

### Voie A, fidèle : réparer les 8 programmes de sommets `stage_blinn.*20.vp`

Remplacer, dans chacun, le `mov o1.w, l(0)` (5 dwords, offset `0x9A0` pour
`00000020.vp`) par le bloc que porte déjà `blinn_per_vert` :

    dp4     r0.x, cb[2][29], v0        ; -pos_w.y
    add     r0.x, r0.x, cb[0][14].y
    mul_sat r0.x, r0.x, cb[0][14].w
    mul     o1.w, r0.x, cb[0][14].x

`cb[2][29]` est **le bon registre dans `stage_blinn` aussi** : son mode 3
(`stage_blinn.00000030.vp`, dword 72) fait précisément
`dp4 r0.y, cb[2][29], v0` puis `add r0.y, r0.y, l(-0.6)` — c'est donc bien la
ligne qui rend `−pos_w.y`. Ce point est **mesuré**, pas supposé.

Puis : allumer les 2 octets de présence vp (indices 16 et 20 de
`0x180556140`) et les 8 octets fp correspondants, et remettre les deux points
« état 22 = 2 » (`0x1800F2FB4`, `0x1800F278A`) déjà décrits en §K de
`brume_anneau_aoi.md`.

**Coût** : ~32 dwords en remplacement de 5 par blob, donc +108 octets ; il faut
reprendre la taille du chunk `SHEX`, la taille totale du DXBC et la table
d'offsets de chunks, élargir `dcl_constantbuffer cb[0]` de 4 ou 14 à **15**, et
reconstruire `shader_pxd_w64.farc` — `tools/farc.py` sait écrire
(`ecrire_farc`, `comme`).

**Avantage décisif** : aucune régression ailleurs. Seuls **quatre** décors ont
un groupe 1 actif dans Final Showdown (`du2`, `du3`, `du5`, `slk`) — et ils
sont censés l'avoir. Tous les autres ont `density 0` : la permutation 2 leur
serait neutre.

**Blocages** : (a) l'empreinte de 16 octets de l'en-tête DXBC devient fausse —
le runtime D3D11 ne la vérifie pas en pratique, mais ce n'est pas vérifié ici ;
(b) le moteur appelle `D3DReflect`, et ces blobs n'ont **pas** de chunk `RDEF` :
la correspondance `env[14]` ↔ `cb[0][14]` est donc une **convention**, lue dans
`blinn_per_vert` et non confirmée pour `stage_blinn` ; (c) la pression de
registres (`dcl_temps`) est à revérifier blob par blob.

### Voie B, bon marché : détourner le mode 1, qui marche déjà

Un seul dword par blob, taille inchangée, aucune reconstruction de chunk :

1. écrire dans `stage_blinn.*20.vp` **les octets de `stage_blinn.*10.vp`**, en
   changeant `cb[2][22]` → `cb[2][29]` dans le `dp4` du brouillard
   (dword 386+4/+5) ;
2. remettre le dword de registre du fragment `0x0B` → `0x04`, pour que la
   couleur vienne d'`env[4]` comme aujourd'hui ;
3. présence + « état 22 = 2 » comme en voie A ;
4. recopier les valeurs du **groupe 1** dans le **groupe 0** de `fog_jn5.txt`.

**Coût** : deux dwords par paire, et rien d'autre. Toute la plomberie employée
est celle qui fonctionne aujourd'hui (le brouillard de distance arrive à
l'écran).

**Blocage, et il est sérieux** : les paramètres viendraient alors du groupe 0,
qui est actif sur **tous** les décors. Chacun verrait ses nombres de distance
réinterprétés comme des hauteurs — régression globale. La voie B ne vaut que
comme **essai d'une seule course**, pour voir la nappe une fois et confirmer
que le reste de la chaîne est juste. Elle ne peut pas être livrée.

### Ce que je ne recommande pas

Reprendre `env[14]` côté moteur (sections J à P de `brume_anneau_aoi.md`).
Ce n'est pas le moteur qui manque : **le `mov o1.w, l(0)` du §4 est une
lecture directe du bytecode**, et tant que le programme de sommets pose zéro,
aucun patch de la DLL ou de `vfes.exe` ne peut produire quoi que ce soit —
qu'on ait raison ou non sur l'origine du masque `[rdi+0x1C]`.

Et ne pas toucher à `MOYA` : la §J de `brume_anneau_aoi.md` l'avait déjà
écarté, et rien ici ne le ramène.

---

## 7. CE QUI N'A **PAS** ÉTÉ VÉRIFIÉ

* **Rien n'a été exécuté.** Aucune course, aucun `vfes.exe`, aucune mesure à
  l'écran. **C'est l'écran qui tranche**, et il n'a pas été consulté.
* **Quelle famille les objets du décor d'Aoi lient réellement.** Les 384
  matériaux de `stgjn5_obj.bin` portent le nom `BLINN` (0 `STAGE`), et
  `stage_blinn` **ne figure pas dans la liste des 40 noms de nuanceurs** du
  moteur : le choix est donc fait par du code que je n'ai **pas lu**. Le nom
  « stage_blinn », le fait que 2 vp et 8 fp en soient chargés, et la §F de
  `brume_anneau_aoi.md` (qui en parlait comme d'un nuanceur « STAGE ») font
  pencher pour `stage_blinn` — **ce n'est pas une mesure**. C'est la voie 0
  du §6, et elle divise ou multiplie le coût par dix.
* **La correspondance `env[i]` ↔ `cb[0][i]`** : établie en lisant
  `blinn_per_vert` (où `cb[0][14]` porte bien `(densité, début, fin,
  1/(fin−début))`), **non confirmée** pour `stage_blinn`, dont `cb[0]` ne fait
  que 4 ou 14 vec4 et sert visiblement à autre chose (les permutations
  `01…`/`10…`/`11…` y lisent `cb[0][14]` hors de tout brouillard).
* **L'origine du masque `[rdi+0x1C]`** (§3) : je n'ai **pas lu** le code qui le
  calcule. Que ce soit la liste des registres lus par le programme compilé est
  une déduction appuyée sur deux cas concordants, pas une mesure. Elle est
  centrale au raisonnement du §3 : si elle est fausse, le §3 tombe — mais le §4,
  qui est une lecture directe du bytecode, tient quand même.
* **Le registre de `env[19]`** (groupe 2) côté APM3 : non cherché.
* **La signification exacte de chaque chiffre** des clés de permutation, hormis
  celui du brouillard. Les clés n'ont pas le même nombre de chiffres entre VF5 R
  et FS (`skin_default` : 7 contre 8, `blinn_per_vert` : 12 contre 11) ; seule
  la position du chiffre de brouillard a été recoupée, par le contenu des
  programmes.
* **Si le runtime D3D11 valide l'empreinte du DXBC**, et si le moteur valide
  une empreinte de `shader_pxd_w64.farc`.
* **Si `tools/farc.py:ecrire_farc` reproduit l'archive à l'identique** quand on
  ne change aucun membre (le contrôle évident avant tout patch ; non fait).
* **Le choix du mode de brouillard** : est-il par matériau, par objet, ou
  global ? §J/§K de `brume_anneau_aoi.md` le traitait comme un **état global**
  (`état 22`, deux sites de constante). Je n'ai pas vérifié qu'un matériau
  puisse le demander seul — c'est ce qui décide si la voie A peut être
  restreinte au décor d'Aoi.
* **`MOYA`** : rien de neuf. La section G de `brume_anneau_aoi.md` reste vraie,
  et la section J reste vraie aussi : ce n'est pas la cible.

---

## 8. VOIE 0 FAITE : la famille du decor est **BLINN**, pas `stage_blinn`

Releve le 2026-11-19, apres le §7. **Aucune course, aucun lancement.** Tout
est lu dans `vf5fs-pxd-w64-Retail_APM3.dll.origine` et dans les fichiers de
donnees. Outil depose : `VF5RE/tools/cle_permutation.py`.

### La table maitresse des groupes de nuanceurs

`0x180554378`, **48 enregistrements de 0x28 octets** (le dernier finit a
`0x180554AF8`, ou commence la reserve des tables de chiffres) :

| offset | champ |
|---|---|
| +0x00 | pointeur sur le **nom** du groupe (`BLINN`, `ITEM`, `STAGE`, ...) |
| +0x08 | indice **1-base** (1..48) |
| +0x0C | **nombre de sous-nuanceurs** consecutifs (0x40 chacun) |
| +0x10 | premier **descripteur** de sous-nuanceur |
| +0x18 | **nombre de chiffres** de la cle de permutation |
| +0x20 | table des **ETATS**, un entier par chiffre |

Le groupe 1 est `BLINN` et il porte **deux** sous-nuanceurs :
`blinn_per_vert` (`0x180556370`) **et** `blinn_per_frag` (`0x1805563B0`).
Le groupe 3 est `STAGE` et porte `stage_blinn` (`0x180556430`).

### Le nom `STAGE` existe -- et personne ne le demande

Le §4 disait « il n'y a pas de nom `STAGE` dans la liste ». **A corriger** :
le nom existe, son pointeur est dans l'enregistrement 3 de la table
maitresse ; sa chaine vit juste ailleurs (`0x18039B858`, mise en commun par
l'editeur de liens avec le nom d'ensemble d'objets de la tache). Idem pour
`SHDMAP`, `SIL`, `S_REFL`, `S_REFR`, `RIPEMIT`, `SN_FOOT`, `FENCE`, `MOVIE`.

Mais le **selecteur** tranche, et il n'y en a qu'un :

| site | ce qu'il fait |
|---|---|
| `0x180176410` | **nom -> indice de groupe** : `strcmp` sur les 48 noms, pas de 0x30 sur le tableau vivant `0x180714B00 + indice*0x30`, rendu **1-base**, **0x31 = introuvable** |
| `0x1800F7760`, boucle `0x1800F77A0` | la **fixation des materiaux** : pour chaque materiau, `0x180176410(nom)` puis **l'indice est ecrit EN PLACE** sur les huit octets du nom, avec la sentinelle `0xDEADFF` juste apres |
| `0x180175870` | le meme `strcmp`, suivi de la liaison ; ses **deux** appelants passent un nom **litteral** : `"RIPEMIT"` (`0x18007B523`) et `"SN_FOOT"` (`0x18007E438`) |

La sentinelle `0xDEADFF` n'apparait qu'a **deux** adresses de tout `.text`
(`0x1800F77A3` le test, `0x1800F77B6` la pose) : **il n'existe qu'un seul
site de resolution dans le moteur**, et son unique entree est le nom du
materiau.

### Et aucun materiau ne dit `STAGE`

Compte des chaines sur les **48** fichiers d'objets de decor extraits
(`VF5RE/extracted/_controle_*/stg*_obj.bin`) :

    STAGE = 0 partout.   BLINN = 1 a 1011 selon le decor.
    stgjn5_obj.bin : BLINN 384, STAGE 0, WATER01 1.

**Conclusion, mesuree : les objets du decor d'Aoi lient `blinn_per_vert` /
`blinn_per_frag`.** `stage_blinn` est inatteignable depuis la donnee -- ses
2 vp et 8 fp montes sont du lest de construction.

**Ce que cela ferme :** la **voie A** (chirurgie des huit blobs DXBC
`stage_blinn.*20.vp`) et la **voie B** (detournement du mode 1) **ne
concernent pas le decor d'Aoi**. Le `mov o1.w, l(0)` du §4 est bien reel,
mais il est dans une famille que le decor n'emprunte pas.

---

## 9. LE CHIFFRE DE BROUILLARD EST L'**ETAT 15** -- pas l'etat 22

### Le constructeur de la cle, lu instruction par instruction

`0x180175680`, boucle `0x180175740` (`rbp` = l'enregistrement de groupe,
`rsi` = le sous-nuanceur) :

    rax = [p_etats + 4*k]              ; l'ETAT du chiffre k (champ +0x20)
    ecx = [0x180715440 + rax*4]        ; sa VALEUR VIVANTE
    edx = [max_vp + 4*k]               ; le MAXIMUM du chiffre (descripteur +0x08)
    eax = min(ecx, edx)                ; cmovle -- on BORNE
    indice_vp += eax * poids ; poids *= (edx + 1)

Donc : **base mixte, chiffre 0 le moins significatif**, et le nom du
programme s'ecrit **chiffre 0 en premier**. Les maxima sont statiques, en
`.rdata` : descripteur **+0x08** pour les sommets, **+0x10** pour les
fragments. Le produit des `(max+1)` vaut exactement le nombre de programmes
(`+0x18` / `+0x1C`) pour les 50 sous-nuanceurs.

**Controle** (`tools/cle_permutation.py --controle`) : les **4 206** jeux de
chiffres des 50 sous-nuanceurs sont recalcules a l'identique, 4 206 sur
4 206. Et il peut echouer : `--essai-faux`, qui inverse l'ordre des
chiffres, n'en retrouve que **297 sur 4 206**.

### L'etat 15, et le fait qu'il va jusqu'a 3

| famille | rang du chiffre | etat | max vp | max fp | valeurs **montees** |
|---|---|---|---|---|---|
| `blinn_per_vert` | 5 / 11 | **15** | **3** | **3** | 1 |
| `blinn_per_frag` | 5 / 11 | **15** | **3** | **3** | 1 |
| `stage_blinn` | 6 / 8 | **15** | 3 | 3 | 1 |
| `lambert` | 2 / 8 | 15 | 3 | 3 | 0, 1, **2** |
| `constant` | 1 / 6 | 15 | 3 | 3 | 0, 1 |
| `fence_alpha` | 1 / 2 | 15 | 3 | 3 | 0, 1, **2**, **3** |
| `skin_default` | 7 / 8 | 15 | **1** | **0** | 1 |
| `hair_default`, `cloth_default`, `eye_ball`, `item_blinn`, `water01`, `floor` | | 15 | **1** ou 0 | 0 ou 1 | 0, 1 |
| 36 autres familles (`sky_default`, `shadowmap`, `simple`, `water_ring`, ...) | | **absent** | | | |

Deux consequences, toutes deux mesurees :

1. **Rien a reparer dans les nuanceurs du decor.** `blinn_per_vert` et
   `blinn_per_frag` acceptent deja la valeur 2 (`max = 3`) et leurs jumeaux
   mode 2 sont intacts (§4). Le seul geste est d'allumer leurs octets de
   presence.
2. **Les combattants ne peuvent pas suivre, meme si l'etat est force** :
   `skin_default`, `hair_default`, `cloth_default` ont **max 1** sur ce
   chiffre, et le `cmovle` borne. Cela recoupe le §5 par un autre chemin.

### La correction du §K de `brume_anneau_aoi.md`

L'« etat 22 » de son §K **n'est pas le chiffre de brouillard**. L'adresse
qu'il patchait, `0x180715498`, est bien l'etat 22 (`0x180715440 + 22*4`),
mais l'etat 22 est le chiffre **7** de `BLINN` et le chiffre **1** de
`stage_blinn`, de maximum **1** en sommet et **0** en fragment. L'essai du
2026-10-18 reglait donc un autre chiffre que celui du brouillard.
*(`--fog-hauteur` a depuis ete retire du patcheur : il n'y a rien de vivant
a defaire, c'est l'explication de l'echec, pas une regression en place.)*

---

## 10. QUI DECIDE LA VALEUR DE L'ETAT 15 : `0x1800F3060`

Un seul site la pose a 2 ou 3, et c'est une lecture directe :

    0x1800F30F8  mov r15d, 1                     ; la valeur par defaut
    0x1800F348B  mov eax, [r14+0x3d4]            ; les drapeaux de la scene
    0x1800F3492  bt eax, 0x14 ; jb  0x1800F34DA  ; bit 20 -> on ne touche a rien
    0x1800F3498  cmp byte [rsp+0x108], 0 ; jne   ; idem
    0x1800F34A2  bt eax, 0x1b ; jae 0x1800F34BC  ; BIT 27 A ZERO -> etat 15 = 1
    0x1800F34A8  and eax, 0x20000000             ; on ne garde que le bit 29
    0x1800F34AD  bts eax, 0x1e                   ; on force le bit 30
    0x1800F34B1  shr eax, 0x1d                   ; -> 2, ou 3 si le bit 29 etait la
    0x1800F34B4  mov [0x18071547C], eax          ; l'etat 15
    0x1800F34BC  mov [0x18071547C], r15d         ; = 1

Autrement dit : **bit 27 absent -> brouillard de DISTANCE (1)** -- c'est
l'etat du jeu aujourd'hui, et il explique a lui seul que les sept
permutations BLINN montees soient toutes en chiffre 1. **Bit 27 present ->
2** (la nappe), **ou 3 si le bit 29 est la** (la nappe texturee, mode que FS
n'alimente pas).

**NON TROUVE : qui met le bit 27.** Aucun `or`/`bts` sur le deplacement
`+0x3D4` avec `0x08000000` dans tout `.text` (releve par motif d'octets sur
les quatre formes, et par `tools/champ_x64.py 0x3d4 --ecritures`, 27 acces
confirmes dont 11 ecritures) ; les seules ecritures du champ sont des
initialisations (`0x1800EE8F4`, `0x18024FB7A`) et une recopie champ par
champ (`0x18015F304`). Le bit passe donc par une base deja decalee, ou par
la donnee -- et ce n'est **pas mesure**.

---

## 11. CE QU'IL RESTE A POSER, ET LES OCTETS EXACTS

### Point 1 -- les 26 octets de presence (indispensable, et sans risque)

Les 26 jumeaux « chiffre de brouillard = 2 » des 26 permutations BLINN
montees. **Les 26 existent dans `w64/shader_pxd_w64.farc`** (verifie nom par
nom contre les 3 950 membres : zero manquant) -- **aucune reconstruction
d'archive**.

| famille | presence | octets a passer de 0 a 1 (offset fichier) |
|---|---|---|
| `blinn_per_vert` vp | `0x180555110` | `0x553D14`, `0x553D15`, `0x553D34`, `0x553D54`, `0x553D55` |
| `blinn_per_vert` fp | `0x180555020` | `0x553C50`, `0x553C51`, `0x553C54`, `0x553C57`, `0x553C58`, `0x553C5A`, `0x553C5D`, `0x553C63`, `0x553CB0`, `0x553CB1`, `0x553CB4`, `0x553CB7`, `0x553CB8`, `0x553CBA`, `0x553CBD`, `0x553CC3` |
| `blinn_per_frag` vp | `0x180554FB0` | `0x553BB4`, `0x553BD4` |
| `blinn_per_frag` fp | `0x180554E00` | `0x553A73`, `0x553B27`, `0x553B33` |

Ces offsets **ne doivent pas etre ecrits en dur** : ils se recalculent par
contenu (§13).

### Point 2 -- l'etat 15 a 2 (18 octets pour 18, longueur inchangee)

Ancre, **unique dans tout le fichier**, en `0x1800F34A2` :

    avant : 0F BA E0 1B 73 14 25 00 00 00 20 0F BA E8 1E C1 E8 1D
    apres : B8 02 00 00 00 90 90 90 90 90 90 90 90 90 90 90 90 90
            ( mov eax, 2  puis treize nop -- on tombe sur le
              `mov [0x18071547C], eax` de 0x1800F34B4, eax valant 2 )

Pas de saut, pas de drapeau lu : on ne depend plus ni du bit 27 ni du
bit 29, et la valeur 3 devient inatteignable par ce chemin.

### Point 3 -- le marquage d'`env[14]` (a tenir en reserve)

Ancre, **unique**, en `0x1800F2A0A` : `A8 20 74 51 B9 0E 00 00 00` ->
`A8 20 90 90 B9 0E 00 00 00`.

**A ne poser que si le point 2 ne donne rien a l'ecran.** Raison : si la
deduction du §3 est juste -- `[rdi+0x1C]` est la liste des registres que le
programme compile LIT -- alors le bit 5 s'allumera **tout seul** des que le
decor passera par `blinn_per_vert` mode 2, qui lit `cb[0][14]`. Le forcer
serait inutile. Si la deduction est fausse, `env[14]` restera non televerse
et la nappe manquera : c'est alors ce point qui la rend. **Les deux
hypotheses sont departagees par l'ecran, pas par le fichier.**

### Pourquoi le point 2, qui est global, ne doit rien casser ailleurs

C'est un **raisonnement**, pas une mesure d'ecran, et il tient a trois
faits mesures :

1. les familles des combattants et des objets ont **max 1** sur le
   chiffre 15 (§9) : le `cmovle` les laisse en 1 ;
2. le mode 2 intact de `blinn_per_vert` finit par
   `max o2.x, r0.w, r1.x` (§4) -- un **maximum** du terme de hauteur et du
   brouillard de distance. Avec `density = 0`, le terme de hauteur vaut 0 et
   le mode 2 **degenere exactement en mode 1** ;
3. dans la donnee de **notre** build (`banc_revo/.../rom/light_param`),
   **38 des 45** `fog_*.txt` ont un groupe 1 a `density 0.00000`, et
   **aucun** n'a `fin == debut` -- le plus serre est `fog_sn5` a 0,01.
   Pas de division par zero, donc pas de NaN a passer dans le `max`.

Les sept decors a groupe 1 non nul de notre build, a nommer parce qu'ils
**changeront** d'aspect et que c'est a l'ecran qu'on le verra :

| decor | density | linear |
|---|---|---|
| **`jn5`** (Aoi, VF5 R) | 1,00 | -2,50 -> 1,00 |
| `jnb` (Aoi, VF5 d'origine) | 0,29 | 1,00 -> 4,00 |
| `d25` | 1,00 | -1,00 -> 1,50 |
| `d35` | 1,00 | 0,00 -> 1,00 |
| `sk5`, `skb` | 1,00 | -0,14 -> -0,03 |
| `snb` | 0,60 | -0,60 -> -0,01 |

*(Le §1 n'en nommait que quatre, pour la donnee de FS ; notre build porte
celle de R pour les decors `*5`, d'ou `jn5` et `jnb` en plus.)*
`lambert` et `fence_alpha`, qui ont deja des permutations en chiffre 2
montees, passeront aussi en 2 : leurs modes 2 portent le meme `max` (32 et
16 programmes recenses au §4 pour `lambert` et `constant`) ; **`fence_alpha`
n'a pas ete relu**.

---

## 12. LE BLOC A AJOUTER A `tools/patch_moteur.py`

Repere **par contenu**, jamais par adresse -- la chaine d'ancre est le nom
d'un programme, pas une VA.

    # -----------------------------------------------------------------
    # `--brume-aoi` -- LA NAPPE DU DECOR D'AOI (analysis/brume_decor_aoi.md,
    # sections 8 a 12). Deux points, et aucune adresse en dur.
    #
    # 1. L'ETAT 15 A 2. `0x1800F3060` ne pose 2 que si le bit 27 de
    #    `[scene+0x3D4]` est la, et personne ne l'y met (section 10).
    #    Dix-huit octets pour dix-huit : `mov eax, 2` puis treize `nop`,
    #    et on tombe sur le `mov [etat15], eax` qui suivait.
    # 2. LES 26 OCTETS DE PRESENCE des jumeaux « chiffre 2 » des 26
    #    permutations BLINN montees. Ils se CALCULENT : on part du nom
    #    `blinn_per_vert.00000100000.vp` dans `.rdata`, on remonte au
    #    tableau de noms, de la au descripteur, et on lit maxima, noms et
    #    presence. Rien d'adresse.
    # -----------------------------------------------------------------
    BRUME_ETAT15 = (
        0x1800F34A2,
        bytes.fromhex('0fbae01b73142500000020 0fbae81ec1e81d'
                      .replace(' ', '')),
        bytes.fromhex('b802000000' + '90' * 13),
    )
    BRUME_ANCRE_NOM = b'blinn_per_vert.00000100000.vp\x00'
    BRUME_CHIFFRE_MAX = 3     # le chiffre de brouillard est le SEUL a 3
    BRUME_VALEUR = 2

et, dans `main`, apres les options de decor :

    if '--brume-aoi' in demandes:
        if not _poser_points(chemin, origine, [BRUME_ETAT15]):
            return 2
        ok, msg = _brume_presence(chemin)     # la fonction ci-dessous
        if not ok:
            print('REFUS : %s' % msg)
            return 2
        faits.append('brume : l etat 15 (le chiffre de brouillard de la cle '
                     'de permutation) est pose a 2 en 0x1800F34A2 au lieu de '
                     'suivre le bit 27 de [scene+0x3D4], et %s. Le decor '
                     'd Aoi passe par blinn_per_vert/blinn_per_frag '
                     '(mesure : ses 384 materiaux disent BLINN, zero STAGE) '
                     'dont les jumeaux mode 2 sont intacts. Les combattants '
                     'ne suivent pas : skin_default a max 1 sur ce chiffre.'
                     % msg)

La fonction, dans l'esprit de `_eau_refraction` (elle relit la DLL
**produite** et rend `(vrai, message)` ou `(faux, raison)`) :

    def _brume_presence(chemin):
        '''Allume les jumeaux « chiffre de brouillard = 2 » de BLINN.

        Tout par contenu : on cherche la CHAINE du nom d'un programme deja
        monte, on remonte au tableau de noms (un qword qui pointe dessus),
        puis au descripteur (un qword qui pointe sur ce tableau, a +0x20).
        '''
        # 1. la chaine -> sa VA ; 2. le qword qui la designe -> noms_vp[i],
        #    donc noms_vp = cette VA - i*8 ; 3. le qword qui designe
        #    noms_vp -> descripteur + 0x20.
        # 4. du descripteur : max_vp = [+0x08], max_fp = [+0x10],
        #    nvp = [+0x18], nfp = [+0x1C], noms_fp = [+0x28],
        #    presence_vp = [+0x30], presence_fp = [+0x38].
        # 5. le rang du chiffre de brouillard = le SEUL k ou max_vp[k] == 3.
        #    S'il n'est pas unique -> REFUS.
        # 6. pour chaque octet de presence non nul : on remplace le chiffre
        #    k par 2 dans les chiffres de son indice (base mixte, chiffre 0
        #    le moins significatif), on recalcule l'indice du jumeau, et ON
        #    VERIFIE que le nom a cet indice est bien le nom attendu
        #    (meme chaine, le chiffre k mis a 2). Sinon -> REFUS.
        # 7. on ecrit 1 sur l'octet de presence du jumeau, et on refuse si
        #    cet octet ne valait pas 0.
        # Rendre : (True, '26 permutations BLINN de plus (5+16 per_vert, '
        #                 '2+3 per_frag)')

`VF5RE/tools/cle_permutation.py` fait deja les etapes 4 a 6 et porte le
controle (4 206 noms recalcules, et `--essai-faux` qui echoue) : le bloc du
patcheur peut l'importer plutot que de les refaire.

---

## 13. CE QUI N'A **PAS** ETE VERIFIE (suite du §7)

* **Rien n'a ete execute.** Aucune course. **C'est l'ecran qui tranche**, et
  il n'a pas ete consulte : ni la nappe sur `jn5`, ni l'absence de
  regression sur les 38 decors a densite nulle, ni l'aspect des six autres
  decors a groupe 1 non nul.
* **Qui met le bit 27 de `[scene+0x3D4]`** (§10). C'est la seule voie qui
  permettrait de restreindre la brume au decor d'Aoi au lieu de la forcer
  partout ; elle n'est pas trouvee.
* **Lequel des deux sous-nuanceurs de BLINN** le decor utilise reellement,
  `blinn_per_vert` ou `blinn_per_frag`. Les deux ont leurs jumeaux mode 2
  intacts et les deux sont traites par le point 1, donc la question ne
  bloque pas -- mais elle n'est pas tranchee. Le choix passe par le champ
  `[sous_nuanceur+0x00]` cherche par `0x180175680`
  (« Cannot find SubShaderName %d »).
* **`fence_alpha` mode 2** n'a pas ete relu dans le DXBC ; il passera en 2
  comme les autres familles a max 3.
* **La correspondance `env[i]` <-> `cb[0][i]`** reste ce que disait le §7 :
  etablie sur `blinn_per_vert`, ou `cb[0][14]` porte bien le quadruplet.
  C'est maintenant la famille qui nous concerne -- la convention est donc
  verifiee **la ou elle sert**, ce qui n'etait pas le cas au §7.
* **L'origine du masque `[rdi+0x1C]`** (§3) : toujours une deduction. Elle
  decide si le point 3 du §11 est necessaire ou inutile.
---

## 14. POSEE DANS `patch_moteur.py` (2026-11-19)

Option neuve `--brume-aoi`, qui fait les **deux** points de la section 11 --
le point 3, le marquage d'`env[14]`, reste **en reserve** comme la note le
demande, et son adresse n'apparait que dans un commentaire.

**Les 26 offsets ne sont pas ecrits en dur.** `_brume_presence` part de la
chaine `blinn_per_vert.00000100000.vp`, remonte au tableau de noms, de la au
descripteur, et lit maxima, noms et presence. Elle retombe sur les
**4 adresses de presence et les 26 offsets** releves a la main dans la
section 11, et sur le rang **5** pour le chiffre de brouillard.

**Le piege, paye au premier essai.** La remontee du tableau de noms sur le
seul prefixe de famille traverse le tableau VOISIN : les fragments de la meme
famille portent le meme prefixe (`blinn_per_vert.xxxxxxxxxxx.fp`) et sont
ranges juste a cote. Le rang trouve pour l'ancre etait **194** dans un
tableau de **192** permutations -- c'est le controle
`produit des bases == nombre de permutations` qui l'a dit. La remontee exige
donc aussi le **suffixe**.

**Mesure de la pose** : 18 octets a l'etat 15, 26 octets de presence
(3 `blinn_per_frag` fp, 2 `blinn_per_frag` vp, 16 `blinn_per_vert` fp,
5 `blinn_per_vert` vp), et le `mov [0x18071547C], eax` qui suit les
dix-huit est intact. DLL `022b3d66...` -> `9b87f161...`, taille inchangee.

**Les refus sont nommes, et verifies par des fautes volontaires** : ancre
bidon (« la chaine ... apparait 0 fois »), max faux (« 0 chiffres a max 7 »),
frere inexistant (« le sous-nuanceur voisin nomme blinn_per_frag au lieu
de ... »). Un second passage rend `deja pose (26 jumeaux montes)` et n'ecrit
rien.

**Rien n'a ete lance.** La section 13 reste entiere : c'est l'ecran qui dit
si la nappe apparait sur `jn5`, si les 38 decors a densite nulle sont
intacts, et ce que deviennent les six autres.
---

## 15. L'ÉCRAN A TUÉ UNE HYPOTHÈSE : LE POINT 3 EST POSÉ (2026-11-19)

Course `20261119_2259`, verdict de Frédéric : **« pas de brouillard pour
aoi »**. Issue **D2**, nommée d'avance.

### Ce que cette issue tranche

Le contrôle d'avant-course a établi que l'état 15 valait bien 2 et que les
26 jumeaux étaient montés. Le chiffre de brouillard change donc, et l'écran
ne montre rien. **La première des deux hypothèses du §3 tombe** : si
`[rdi+0x1C]` était la liste des registres que le programme compilé *lit*, le
bit 5 se serait allumé tout seul dès que le décor est passé par
`blinn_per_vert` mode 2, qui lit `cb[0][14]`. Il ne s'est rien passé. La
constante de hauteur n'est **jamais téléversée**, et le mode 2 calcule son
terme de hauteur avec zéro -- ce qui le fait dégénérer exactement en mode 1,
d'où l'absence de différence à l'écran.

C'est le cas pour lequel le §11 gardait le point 3 en réserve, avec sa
condition écrite d'avance : « À ne poser que si le point 2 ne donne rien à
l'écran. »

### Ce qui est posé

Option **`--brume-env14`**, séparée de `--brume-aoi` pour qu'on puisse la
retirer seule. Elle **refuse** si `--brume-aoi` n'est pas là : marquer
`env[14]` comme téléversé sans que le mode 2 soit atteint ne peut rien
donner, et on l'aurait appris par une course.

    0x1800F2A0A   A8 20 74 51  ->  A8 20 90 90

Mesure : **exactement deux octets** changent dans la DLL par rapport à celle
de la course, et ce sont les deux du `je`. Rien d'autre n'a bougé.

### Ce qui n'est toujours pas vérifié

* **Que le décor regardé était bien `jn5`.** Le journal ne dit pas quel décor
  a été chargé, et la capture ne permet pas de distinguer `jn5` de la version
  Final Showdown. Si la barre ESPACE n'a pas été passée, `fog_jn` n'a pas le
  même groupe 1 et la mesure de D2 ne vaut rien. **À confirmer à la prochaine
  course.**
* **L'issue D4 n'a pas été testée** : aucune des deux captures n'est un décor
  banal. On ne peut donc pas dire que `--brume-aoi` est sans effet ailleurs,
  seulement que rien n'a planté et que le journal ne porte aucune exception.
* **Si le point 3 ne donne rien non plus**, alors la seconde hypothèse du §3
  tombe aussi et il faudra chercher qui met le bit 27 de `[scene+0x3D4]` --
  la voie que le §10 n'a pas trouvée.
---

## 16. UNE PORTE FERMÉE PROPREMENT : LA BRUME D'AOI N'EST PAS UNE TÂCHE D'EFFET (2026-11-19)

Décompilation à REA + Ghidra 12.1.2 sur `analysis/vf5fs_apm3_origine.dll`,
après la deuxième course blanche. **Il fallait vérifier que la brume qu'on
cherche n'était pas, depuis le début, un objet tout autre que le nuanceur.**
Elle ne l'est pas, et voici comment on le sait.

### 16.1 Le moteur a deux tâches de brume

Le tableau des 23 noms de tâches d'effet, `0x18034E4D0` :

    0 HIT  1 AUTH3D  2 WALL  3 LEAF  4 WATA  5 SNOW  6 YUKA  7 RIPPLE
    8 RAIN  9 THUNDER  10 DOWN  11 MOVE  12 RINGOUT_SPLASH  13 WATER_RING
    14 SPLASH  15 SNOW_RING  16 FOG_ANIM  17 WET_CLOTH  18 FOG_RING
    19 BREATH  20 PARTICLE  21 POISON  22 ELE_BOARD

`FUN_180071AF0` est `TaskEffectFogAnim::pre_init()` (sa propre trace le dit),
et sa garde a **exactement la même forme déroulée** que celle de `RIPPLE` :

```c
puVar2 = &DAT_180643130;                     // id 14  -> `are`
if (param_2 != DAT_180643130) puVar2 = 0;
if (param_2 == DAT_180643164)                // id 13
     puVar2 = &DAT_180643164;
else if (puVar2 == 0) goto LAB_180071b91;    // rien : le drapeau reste à 0
...
*_DAT_180677b08 = 1;                         // l'autorisation, jamais donnée
```

### 16.2 Et `jin` ne demande AUCUNE des deux

La liste de tâches de ver.B pour `jin`, relue dans son ELF et traduite en
numérotation FS, est

    [2, 12, 17]  =  WALL, RINGOUT_SPLASH, WET_CLOTH

Ni 16 (`FOG_ANIM`), ni 18 (`FOG_RING`). **Le décor d'Aoi ne porte pas de tâche
de brume, ni chez ver.B, ni chez VF5 R.** La nappe qu'on cherche est donc bien
celle du **nuanceur** — `blinn_per_vert` mode 2 et `cb[0][14]` — et la voie
suivie depuis le début est la seule qui existe. Ce n'est plus une hypothèse.

### 16.3 Un décor PERD bien sa brume à cause de cette garde, mais ce n'est pas celui d'Aoi

`are` (14) demande `FOG_ANIM`, et ses variantes ajoutées sont **`ae5` = 52** et
**`aeb` = 71**. Aucune des deux n'est 13 ou 14 : **leur brume est éteinte par
la même garde à deux identifiants que l'eau d'Eileen.** Même cause, même
remède, autre décor — à noter pour plus tard, pas à poser ce soir.

### 16.4 Ce qui n'est toujours pas trouvé

**Qui écrit la VALEUR de `env[14]`.** Le bloc de `0x1800F2A0A` ne fait que le
*déclarer* (`mov ecx, 0xE` puis `call 0x180247430` = marque ; `lea ecx,[rdx+0xc]`
= 14 puis `call 0x1802475B0` = décrit). Le point 3 force ce marquage ; la
course du 19 novembre dira s'il suffit. Si non, c'est l'écriture de la valeur
qu'il faudra trouver, et le bit 27 de `[scene+0x3D4]` avec elle.
---

## 17. CORRECTION DE LA SECTION 16 : LES DEUX PORTES QUE J'AVAIS FERMÉES SONT OUVERTES (2026-11-20)

Même faute que pour l'eau, et au même endroit : **la section 16 lit la garde
dans `.origine` et conclut sur la DLL qui tourne.** Voir
`eau_ring_eileen.md` §10.2 pour la faute elle-même.

### 17.1 `FOG_ANIM` n'est plus gardée par deux identifiants

Dans la DLL en place, `0x180071B3E` porte un **balayage** sur une table de
`0x180EC2130`, pas `0x34`, et cette table sert **quatre décors : 14, 13, 52,
71** — `are`, le treizième, **`ae5`** et **`aeb`**.

**La section 16.3 tombe en entier** : `ae5` et `aeb` ont leur brume animée,
elle leur a été rendue par les options de décors.

### 17.2 Et surtout : `jn5` DEMANDE BIEN UNE TÂCHE DE BRUME

La section 16.2 dit que `jin` n'en demande aucune. Elle lit la liste de
**ver.B**, qui est celle de `jnb` (67) : `WALL, RINGOUT_SPLASH, WET_CLOTH`.
Mais la liste de **VF5 R**, celle de `jn5` (48), est tout autre — le patcheur
l'imprime :

    48<-jin(EFFECT_WALL EFFECT_FOG_RING)
    jn5[VF5 R](DOWN=DOWNKEMU FOG_RING)

**`jn5` demande `EFFECT_FOG_RING` (18).** Et `decors.md` §24 la porte comme
posée : « FOG_RING 18 | `0x180072130`, appelée du setStage `0x180072B80` | UN
dossier `0x1806431C8` (0x3C), texture en `+0x1C` | `call` → stub de recopie →
`jmp 0x180072130` », avec la liste des décors servis : **`jn5` `snb`**.

Donc la phrase « la nappe qu'on cherche est celle du nuanceur, et c'est la
seule voie qui existe » est **fausse**. Il y a deux voies pour la brume d'Aoi,
et la seconde est déjà câblée :

1. le **nuanceur** — `blinn_per_vert` mode 2, `cb[0][14]`, l'état 15 : les
   trois pièces sont posées et jamais vues à l'écran ;
2. **`TaskEffectFogRing`** — la tâche que `jn5` demande, servie depuis le
   chantier des décors, et dont on n'a **rien mesuré ce soir**.

### 17.3 Ce qui tient

Que `jnb` (ver.B) ne demande aucune tâche de brume : sa liste est bien
`[2, 12, 17]`. Que les deux tâches `FOG_ANIM` et `FOG_RING` existent et sont
les n° 16 et 18 du tableau de `0x18034E4D0`. Que les trois pièces du nuanceur
sont en place. Rien d'autre.

### 17.4 Ce qu'il faut mesurer avant de reparler de la brume

* ce que `TaskEffectFogRing` rend aujourd'hui sur `jn5` — son init, son
  dossier de `0x1806431C8`, et si son dessin est atteint ;
* si la nappe qu'on attend est la sienne ou celle du nuanceur, **avant** de
  dépenser une course de plus sur l'état 15.
---

## 18. MESURE DE `TaskEffectFogRing` SUR `jn5` : LA CHAÎNE EST ENTIÈRE, ET AUCUNE COURSE NE L'A JAMAIS VUE (2026-11-20)

Frédéric : « Oui, mesure ». Rien lancé, rien posé. Dix lectures : les deux
binaires, les archives d'objets des décors, `tex_db.bin`, l'archive de
nuanceurs, `vf5fs_host.cpp`, et les **486** journaux archivés.

### 18.1 Dans le FS de série, PERSONNE ne demande `EFFECT_FOG_RING`

La table des tâches d'effet par décor de `.origine` est en **`0x18034D570`**
— 41 enregistrements de `0x60`, la liste en `+0x20`, terminée par `-1`. Elle
se lit dans `FUN_18006F620` (`lea rax, [rip+0x2DDEF7]` ; l'indice y est
multiplié par 3 puis décalé de 5, donc le pas est `0x60`).

Les 41 listes, relues une à une : **aucune ne porte 18.**

`TaskEffectFogRing` est donc du **code mort dans l'APM3 de série**. La tâche
existe entière — RTTI, quatre fonctions de table virtuelle, son dossier, sa
physique, son rappel de dessin — et aucun décor ne la réclame. Son unique
dossier, en `0x1806431C8`, porte l'identifiant **22**, qui est **`du2`** ; et
`du2` ne demande que `WALL`.

*(L'identifiant 22 se lit dans la table de pointeurs de noms `0x18039F7A0` :
`tak` y occupe un emplacement hors séquence, et c'est pourquoi le tableau de
chaînes brutes de `0x18039FC40`, lu au pas de 4, décale tout après `tak` — il
donne `du3` au lieu de `du2`. C'est la table de POINTEURS qui fait foi.)*

Ce que `decors.md` §24 relevait de VF5 R l'explique : là-bas FOG_RING a **deux**
dossiers, `jin` et `du2` ; chez ver.B, c'est `sin` qui la porte. Final Showdown
a gardé le code et jeté les demandes.

### 18.2 Dans la DLL qui tourne, trois décors la demandent

La même table est repointée en **`0x180EB65F0`** (même pas de `0x60`, même
`+0x20`), et elle couvre les 86 décors :

| décor | la liste de tâches, dans la DLL en place |
|---|---|
| 48 **`jn5`** | **`WALL FOG_RING`** |
| 68 `snb` | `WALL FOG_RING` |
| 83 `d25` | `WALL FOG_RING` |
| 67 `jnb` | `WALL RINGOUT_SPLASH WET_CLOTH` — aucune brume, comme §17.3 le disait |
| 9 `jin` | `WALL WET_CLOTH RINGOUT_SPLASH LEAF` |
| 22 `du2` | `WALL` |
| 13 `hai` / 14 `are` / 52 `ae5` / 71 `aeb` | `FOG_ANIM` pour les quatre |
| 15 `slk` / 53 `sk5` / 72 `skb` | `WALL WATER_RING RIPPLE SPLASH` (+ `WET_CLOTH` pour 72) |

**`jn5` demande bien `EFFECT_FOG_RING`, et c'est la seule des trois
générations de `jin` à le faire.**

### 18.3 Le « stub de recopie », décodé

Le `call` de `0x180072B80` ne va plus à `0x180072130` : il va à
**`0x180EA6C50`, dans `.greffe`** (aucun `call`/`jmp` de `.text` ne vise plus
`0x180072130` — vérifié par balayage de tous les `E8`/`E9` des deux binaires).

    180EA6C50  lea  rax, [rip+0x69]        ; -> 0x180EA6CC0, la table
    180EA6C57  mov  r9d, 3                 ; trois dossiers
    180EA6C5D  test r9d, r9d / je          ; epuise ?
    180EA6C62  cmp  edx, [rax] / je        ; l identifiant du decor
    180EA6C66  add  rax, 0x3c / dec r9d / jmp
    180EA6C6F  lea  r8, [rip-0x863aae]     ; -> 0x1806431C8, le dossier vif
               sept `mov` de 8 octets + un de 4 = 0x3C recopies
    180EA6CB6  jmp  0x180072130

**La voie « pas trouvé » n'est pas un trou.** Les 0x3C octets qui suivent
immédiatement la table, en `0x180EA6D74`, sont **le dossier d'origine de `du2`
octet pour octet** : un décor non servi fait recopier le dossier de série, et
l'égalité unique `param_2 == [0x1806431C8]` échoue alors proprement.

### 18.4 Le dossier de `jn5` n'est pas un clone

| champ | `du2` 22 (série) | **`jn5` 48** | `snb` 68 | `d25` 83 |
|---|---|---|---|---|
| `+0x00` identifiant | 22 | **48** | 68 | 83 |
| `+0x08` | 2 000 | 2 000 | 2 000 | 2 000 |
| `+0x0C` | 16 | 16 | 12 | 16 |
| `+0x10` | 0,4 | 0,4 | 0,52 | 0,4 |
| `+0x18` | −0,12 | −0,12 | −0,28 | −0,12 |
| `+0x1C` **texture** | 15 650 | **15 460** | 8 647 | 15 650 |
| `+0x34` | 1 | 1 | 0,9 | 1 |
| `+0x38` | 0,1 | **0,3** | 0,05 | 0,1 |

`d25` est le clone exact de `du2`, l'identifiant près — conforme à ce que
`decors.md` notait (« du2 = FS octet pour octet »). `jn5` et `snb`, non : ils
portent leurs propres valeurs, prises dans leur binaire d'origine. **Celle de
`jn5` est trois fois plus dense que celle de `du2`** (`+0x38` : 0,3 contre 0,1).

### 18.5 La texture existe, et c'est celle de `jin`

| identifiant | nom dans `tex_db.bin` | dans l'objset du décor servi |
|---|---|---|
| 15 460 | `F_VF5E_JIN00_MU_TUBU2` | **oui**, `stgjn5_obj.bin`, 605 textures |
| 15 650 | `F_VF5E_DU2_MU_TUBU2` | oui, `stgd25_obj.bin`, 108 textures |
| 8 647 | `F_VF5E_SIN00_IK_TUBU1` | oui, `stgsnb_obj.bin`, 115 textures |

`stgjn5` porte **15 459 `JIN00_MU_TUBU1` et 15 460 `JIN00_MU_TUBU2`**. Et
`stgjnb` — le `jin` de ver.B — n'a **ni l'une ni l'autre**, seulement
`7664 JIN00_IK_TUBU2`. La paire `MU_` est donc bien l'apport de VF5 R, et elle
est arrivée avec le décor.

### 18.6 Le nuanceur est monté, lui

Groupe **`FOGPTCL`**, indice 42, **zéro chiffre de clé** — donc une seule
permutation, rien à choisir :

    fog_ptcl  (descripteur 0x180556E30, id 44)
      vp : 1 programme, 1 monte   (presence 0x180554DFF)
      fp : 1 programme, 1 monte   (presence 0x180554DFE)

Les deux octets de présence valent `01` **dans les deux binaires**, et
`fog_ptcl..vp` / `fog_ptcl..fp` sont tous deux dans
`shader_pxd_w64.farc` (3 950 membres). **Ce n'est pas le défaut de
`water01` :** ici il n'y a rien à monter.

### 18.7 La physique et le dessin sont réels, pas des bouchons

* `FUN_1800725A0` intègre chaque particule avec sa traînée
  (`DAT_1806431A8`, `DAT_1806431BC`, `DAT_1806431C0`) ;
* `FUN_180071BC0` lit les **deux combattants** (`FUN_1801509B0`,
  `FUN_180150920`, `FUN_1801508A0`, `FUN_1801509C0`), **cinq os chacun** par
  `FUN_1800E0280`, et allume jusqu'à **dix** émetteurs en `+0x124` (pas `0x28`
  depuis `+0x128`) quand un os passe sous la hauteur `DAT_1806431B8`. C'est
  une **nappe qui réagit aux pieds**, pas un décor peint ;
* `FUN_1800729C0`, le rappel de dessin, fait plus de 400 octets
  (`push rbp ; sub rsp,0x50 ; … call 0x18010BEF0 ; call 0x18010CCA0`). Rien
  d'un `return 1` comme `TaskEffectEleBoard`.

### 18.8 ET VOICI LE FAIT QUI TRANCHE : AUCUNE COURSE N'A JAMAIS CHARGÉ UN DÉCOR DU CHANTIER

Les **486** journaux archivés, grepés tous, sur la ligne que l'hôte imprime
lui-même (`[419.185] … decor [+0x5C]=`). Voici **tous** les décors qui ont
jamais été chargés, et leur compte :

    -1 : 44     0 : 202     4 : 24     7 : 56      9 : 20
    11 : 38    13 : 10     16 : 20    19 : 3491   20 : 22

**C'est tout.** Jamais 48 (`jn5`), jamais 67 (`jnb`), jamais 52 ni 71
(`ae5`, `aeb`), jamais 15, 53 ni 72 (`slk`, `sk5`, `skb`). Et aucun journal
ne contient le mot `jn5`, `JIN00`, `FOG_RING`, ni « decor = 48 ».

Donc : **les deux courses blanches sur la brume n'ont pas mesuré la brume
d'Aoi.** Elles ont tourné sur le décor 19 (`tan`), comme 3 491 lignes sur
3 923. Le nuanceur, l'état 15 et `env[14]` n'ont jamais été regardés sur le
décor pour lequel on les a posés. Ce ne sont pas deux mesures négatives :
ce sont deux mesures **hors sujet**, et la mienne, pas celle de Frédéric.

### 18.9 CE QUI BLOQUE UNE COURSE SUR `jn5`, et c'est UNE CONSTANTE

L'hôte sait déjà imposer le décor — `ImposerLeDecor`, SS 419.254 : il remplace
les quatorze octets de `VF5FS+0xBD96C` par `MOV ECX, <n>` + neuf `NOP`, en
vérifiant le site par contenu. Mais :

```c
if (g_decorImpose >= 0x29) {
    Log("  [419.254] REFUS : VF5_DECOR_IMPOSE=%ld hors des bornes du"
        " module lui-meme (0 a 0x28). Rien n'est ecrit.", g_decorImpose);
    return false;
}
```

**`VF5_DECOR_IMPOSE=48` serait REFUSÉ**, et le journal le dirait. La borne
`0x29` était vraie du module de série — 41 décors. Elle ne l'est plus : la DLL
en place en porte **86** (indices 0 à 85). C'est **une constante à relever**,
plus la consigne de pilotage à écrire d'avance, et rien d'autre.

Et l'interrupteur est **fermé** dans le lanceur (`set "VF5_DECOR_IMPOSE=-1"`,
ligne 161) : trois états, pas deux — fermé, refusé, armé.

### 18.10 Ce qui n'est PAS mesuré

* **Qu'une nappe paraisse à l'écran.** Jamais vu, et §18.8 dit pourquoi :
  le décor n'a jamais été chargé. C'est l'écran qui tranchera.
* Que la **passe 4** (`FUN_18010CA20(4,1)`, prise par l'init) soit consommée
  pour ce décor. Le rappel est enregistré ; personne n'a prouvé qu'il est
  appelé.
* Que `Combat_MachineAEtats`, qui lit `[vue+0x4C]` quatre fois et continuera
  de lire le décor que le module a choisi, ne fasse pas un écart entre la
  musique ou les fiches et la scène chargée — le commentaire de l'hôte le dit
  déjà de 19, et ça vaudra autant de 48.
* Si `jn5` **tient** 650 images : le décor 13 faisait fauter le module à
  `VF5FS+0x30b2cf`, 4 courses sur 4. Un décor ajouté n'a jamais été imposé.
---

## 19. CORRECTION DE LA SECTION 18.8 : JE ME SUIS GREPÉ LE MAUVAIS CHANTIER (2026-11-20)

Frédéric : « j'ai bien chargé et vu le décor de Aoi en version VF5 R ».

**Il a raison, et la section 18.8 est fausse.**

### 19.1 Les 486 journaux ne sont pas ceux de ce build

    485 journaux  host_log*.txt  sous  FS REVO/
      1 journal   host_log*.txt  sous  FS GOG/

`host_log.txt` est le journal de **`vf5fs_host.cpp`**, l'hôte du chantier
REVO — un autre module, un autre binaire, une autre histoire. Les décors qu'il
nomme (0, 4, 7, 9, 11, 13, 16, 19, 20, et 19 à 3 491 lignes sur 3 923) sont
ceux du module de REVO, qui n'a **aucun** décor ajouté : c'est précisément
pourquoi aucune valeur n'y dépasse 20. J'aurais dû le voir là.

**Aucun de ces journaux ne dit quoi que ce soit de l'APM3.**

### 19.2 Et les journaux de l'APM3 ne nomment pas le décor

Ils sont ailleurs : `apm_journal*.txt` et `quest_journal*.txt`, 25 fichiers
dans `runtime/media/vf5fs/courses/`. Les seules lignes « decor N » qu'ils
portent sont les compositions de combat du mode quest :

    [quest] combat compose : perso 0 contre 7 ; decor 5 ; force 12 ; ...

soit les décors 5, 7 et 11, et ce sont des choix du mode quest, pas ceux de
Frédéric en versus. **Le décor chargé ne se lit dans aucun journal de ce
build.** Il se lit à l'écran. C'est la règle §3 de `CLAUDE.md`, mot pour mot :
« c'est l'écran qui tranche, pas le journal ».

### 19.3 Ce que ça change, et c'est beaucoup

Le stub de `FogRing`, avec ses trois dossiers 48, 68, 83, est présent dans
**les deux sauvegardes du 19 novembre** :

| binaire | horodatage | le `call` de `0x180072B80` |
|---|---|---|
| `…dll.avant_du2_vivante` | 2026-11-19 20:59 | → `0x180EA6C50`, dossiers 48, 68, 83 |
| `…dll.avant_decors_19nov` | 2026-11-19 22:53 | → `0x180EA6C50`, dossiers 48, 68, 83 |
| `…dll` en place | 2026-11-20 14:39 | → `0x180EA6C50`, dossiers 48, 68, 83 |
| `…dll.origine` | 2021-05-19 | → `0x180072130` |

Donc quand Frédéric a chargé `jn5`, **`TaskEffectFogRing` était déjà
câblée** : la tâche demandée (§18.2), le dossier recopié (§18.3), la texture
`JIN00_MU_TUBU2` présente (§18.5), le nuanceur `fog_ptcl` monté (§18.6).

### 19.4 Ce qui tient du §18, ce qui tombe

**Tient** : 18.1 à 18.7 et 18.9 — tout ce qui est lu dans les binaires, les
objsets, `tex_db.bin`, l'archive de nuanceurs et le source de l'hôte.

**Tombe** : 18.8 en entier. Les deux courses blanches ne sont **pas** « hors
sujet » : si Frédéric était sur `jn5`, ce sont de vraies mesures négatives sur
un `FogRing` câblé. Et 18.9 n'est plus un **préalable** : la borne `0x29` reste
un fait exact, mais Frédéric atteint `jn5` à la main ; elle ne sert qu'à qui
voudrait imposer un décor sans le choisir.

### 19.5 La vraie question, que je n'ai pas posée

**Sur `jn5`, qu'est-ce qui paraît ?** Rien du tout, ou quelque chose de trop
faible pour s'appeler une nappe ? Les deux réponses n'envoient pas au même
endroit :

* **rien** → le défaut est en aval de l'init : la passe 4
  (`FUN_18010CA20(4,1)`) n'est pas consommée, ou le rappel `0x1800729C0` n'est
  jamais appelé ;
* **quelque chose de faible** → c'est l'émission : la hauteur
  `DAT_1806431B8` que les os doivent franchir, ou le `+0x38` du dossier
  (0,3 pour `jn5` contre 0,1 pour `du2`).

Et dans les deux cas, ça se mesure **avant** de reparler de l'état 15 du
nuanceur, qui est l'autre voie.
---

## 20. UNE TROISIÈME VOIE, TROUVÉE JUSTE AVANT L'ARRÊT : `STGJN5_EFF_MOYA` (2026-11-20)

Frédéric, sur `jn5` : « brume en arrière plan OK mais pas au premier plan ;
a priori ce doit être un cylindre de brume qui recouvre en partie les
combattants ». Alors on a cherché l'objet, et il existe.

### 20.1 Ce que `jn5` porte et que `jnb` n'a pas

Les trois objsets de `jin` comparés par leurs noms d'objets : **jn5 (447) est
un SOUS-ENSEMBLE strict du `jin` de FS Lindbergh (643)** — zéro objet que FS
n'ait déjà. Ce que jn5 a et que **`jnb` (ver.B, 443) n'a pas** :

    stgjin_eff_moya_000     stgjin_eff_kemutubu_bmz
    stgjin_eff_moya_001     stgjin_eff_kemutubu2_bmz
    stgjin_eff_saku         stgjin_ring

**もや = brume, 煙 = fumée.** Et `jnb` est précisément la génération qui ne
demande aucune tâche de brume (§18.2).

### 20.2 Et une scène auth_3d les anime

| archive | membres | la scène de brume |
|---|---|---|
| `EFFSTGJN5.farc` | **11** | **`STGJN5_EFF_MOYA.a3da`** |
| `EFFSTGJNB.farc` | 10 | **aucune** |

Les dix autres membres sont les mêmes de part et d'autre (ARUKI_A/B/C,
DOWNKEMU, IKE, KABE_REACT, SPLASH_DOBON, SPLASH_DOBON_S, TALK). **`MOYA` est
exactement le onzième**, et c'est celui que ver.B n'a pas.

Et `EFFECT_AUTH3D` est **toujours créée** (`decors.md` §… : liste
`0x18034D510`), donc rien à demander de ce côté.

### 20.3 Il y a donc TROIS voies, pas deux

| voie | état |
|---|---|
| le nuanceur — `blinn_per_vert` mode 2, `cb[0][14]`, état 15 | posée, jamais vue |
| **`TaskEffectFogRing`** — 2 000 particules aux pieds, texture `JIN00_MU_TUBU2` | **câblée** (§18), vue sans effet |
| **`STGJN5_EFF_MOYA.a3da`** sur `stgjin_eff_moya_000/001` | **rien mesuré** |

Et c'est la troisième qui ressemble le plus à ce que Frédéric décrit : un
**maillage**, pas une pluie de particules. Un cylindre de brume est un objet.

### 20.4 LA PROCHAINE MESURE, et elle ne coûte pas de course

**`STGJN5_EFF_MOYA` est-elle déclarée dans la catégorie `auth_3d` de `jn5`
dans la base d'objets ?** C'est exactement la pièce que l'import de décor doit
fabriquer (`decor_neuf.py`, la catégorie `STG<code>` et ses uid), et c'est le
genre de pièce qui manque sans rien dire : l'archive est sur le disque, la
scène est dedans, et personne ne la demande.

À lire ensuite, dans cet ordre :

1. la catégorie `auth_3d` de `jn5` dans `obj_db` / la base des scènes — la
   liste des uid que le décor réclame, et si `STGJN5_EFF_MOYA` y est ;
2. ce que `decor_neuf.py` a posé pour les onze membres de `EFFSTGJN5.farc`,
   et s'il en a posé dix ;
3. seulement après, le dessin de `TaskEffectFogRing` (passe 4, rappel
   `0x1800729C0`).

**Rien n'est posé, rien n'est lancé.** Arrêt demandé par Frédéric à ce point.
---

## 21. LA VOIE `MOYA` EST DÉCLARÉE PARTOUT : LE DÉFAUT N'EST PAS DANS LES DONNÉES (2026-11-20)

La mesure que §20.4 demandait, faite. **Elle répond non à ma propre
hypothèse :** rien ne manque dans les bases.

### 21.1 La scène est déclarée, et son objet aussi

| pièce | état |
|---|---|
| `auth_3d_db.bin` | catégorie `EFFSTGJN5` = `category.41.value`, **dix uid** (3528 à 3537) |
| dont | **`uid.3532.value=A STGJN5_EFF_MOYA`** |
| l'archive | `EFFSTGJN5.farc` porte `STGJN5_EFF_MOYA.a3da`, 2 821 o, daté du 31 janvier 2008 |
| la scène nomme | `STGJN5_EFF_MOYA_000` (`object_list`, `play_control`, `visibility`) |
| `obj_db.bin` | déclare **`STGJN5_EFF_MOYA_000` et `_001`** en `0x107EC0` — renommés par l'import |
| l'objset `stgjn5` | porte les objets **449 `stgjin_eff_moya_000`** et **450 `stgjin_eff_moya_001`** |

Les bases sont en majuscules (`STGJN5_EFF_MOYA_000`) et les objsets en
minuscules (`stgjin_eff_moya_000`) **partout, y compris pour le `jin` de
série** : ce n'est pas un écart de l'import, c'est la convention du moteur.

### 21.2 La liste du descripteur est la GÉOMÉTRIE, pas les animations

Le descripteur de décor (`0x180EB1000 + idx*0xF0`) porte en `+0x14`..`+0x24`
**cinq identifiants `(objset << 16) | id d'objet`**, terminés par `-1`. Pour
`jin` (35) ils valent

    438 stgjin_gnd   451 stgjin_ring   442 stgjin_sky   441 stgjin_sdw
    439 stgjin_reflect

et pour `jn5` (6156) les quatre premiers, **puis `-1`**. Ce n'est **pas** un
oubli : l'objset de `jin` de VF5 R, relu dans `extracted/decors/VF5R/`, fait
447 objets, id max 451, et **l'objet 439 `stgjin_reflect` n'y existe pas**.
La liste est juste. (Contrôle croisé : `sk5` reçoit les **cinq** de `slk`,
`ae5` les trois de `are`, `bn5` les trois de `ban` — chaque fois exactement ce
que la source contient.)

Donc `moya` (449/450) n'a jamais eu à être dans cette liste : c'est un objet
d'effet, pas du décor, et c'est la scène qui le montre.

### 21.3 La traduction d'uid de `TaskEffectAuth3D`, et pourquoi MOYA s'en passe

`TaskEffectAuth3D::setStage` (`0x180070340`) parcourt les scènes de la tâche
(`[tâche+0x68]`, `[tâche+0x58]` entrées) et lit l'uid de chacune par un
**appel grefé**, `0x180EA80C0` : il appelle l'accesseur d'origine
`0x180041440`, puis traduit l'uid par une table de paires à `0x180EA80F0` —

    3519 -> 1256   STGRV5_EFF_IDOU  -> STGRIV_EFF_IDOU
    3520 -> 1257   STGRV5_EFF_KAWA  -> STGRIV_EFF_KAWA
    3703 -> 2036   STGSO5_EFF_FLASH -> STGSMO_EFF_FLASH
    3774 -> 1256   STGRVB_EFF_IDOU  -> STGRIV_EFF_IDOU
    3775 -> 1257   STGRVB_EFF_KAWA  -> STGRIV_EFF_KAWA

**`3532` (MOYA) n'y est pas.** Et ce n'est pas un manque, parce que la suite
n'est pas une table indexée : ce sont **des cas particuliers nommés un par
un** —

    lea ecx, [rax-0x4E8] ; cmp ecx,1 ; jbe ...    ; uid 1256 et 1257
    cmp eax, 0x7F4                                ; uid 2036
    puis, sur l uid traduit : 1159, 1160, 1249, 1256, 2029

`STGJIN_EFF_MOYA` est l'uid **1942** (`auth_3d_db`, ligne 2766). Il n'est
dans aucun de ces cas. **Un uid non traduit prend le chemin ORDINAIRE**, celui
de `0x1800703FF`, qui configure et joue la scène. La table du socle ne mappe
donc que ce qui en a besoin, et MOYA n'en a pas besoin.

### 21.4 Bilan : les trois voies sont ouvertes dans les données

| voie | dans les données |
|---|---|
| le nuanceur, état 15 + `env[14]` | posé |
| `TaskEffectFogRing` | câblé de bout en bout (§18) |
| `STGJN5_EFF_MOYA` + objets 449/450 | **déclaré de bout en bout** |

**Le défaut n'est pas une déclaration qui manque.** Il est à l'exécution, et
c'est là qu'il faut aller.

### 21.5 Ce qu'il reste à mesurer, et rien de tout ça n'exige une course

1. **Qui remplit `[tâche+0x68]`** — la liste de scènes que la tâche parcourt.
   Si la scène n'est jamais CRÉÉE depuis la catégorie, le `setStage` ne la
   voit pas et ne dit rien. C'est le seul endroit où un décor ajouté peut
   encore perdre sa scène sans bruit.
2. **La passe 4** de `FogRing` (`FUN_18010CA20(4,1)`) : est-elle consommée ?
3. Et seulement après : l'état 15.
---

## 22. FRÉDÉRIC A VU LE MÊME DÉFAUT SUR LE DÉCOR DE LEI FEI — ET ÇA TUE LA VOIE `MOYA` COMME CAUSE (2026-11-20)

**La mesure d'écran**, rapportée pendant la séance : « le décor de Lei Fei de
VF5 présente le même problème de brume que celui d'Aoi VF5 R ».

### 22.1 Lei Fei, c'est `sin`, et sa version VF5 ver.B est l'indice 68

`decors.md` : « `cas riv jin sin djo` → les décors maison de Lion, Shun Di,
Aoi, Lei-Fei et … ». Donc l'anneau de Lei Fei est **10 `sin` | 49 `sn5` |
68 `snb`**, et « son décor de VF5 » est **`snb`, l'indice 68**.

### 22.2 Il y a EXACTEMENT trois décors qui demandent `FOG_RING`, et ce sont eux

Relu dans la sortie de la reconstruction du jour, et dans `tools/generation.py` :

| le nôtre | copié de | lu dans | `MOYA` ? |
|---|---|---|---|
| **48** `jn5` (Aoi, VF5 R) | `jin` 9 | l'ELF **VF5 R**, deux dossiers (`jin`, `du2`) | **oui** |
| **68** `snb` (Lei Fei, VF5) | `sin` 10 | l'ELF **ver.B**, un seul dossier (`sin`) | **non** |
| **83** `d25` (Dural, VF5 R) | `du2` 22 | l'ELF **VF5 R** | **non** |

Et le stub de recopie de `FOG_RING` (`0x180EA6C50` → `0x1806431C8`, 0x3C
octets) recopie le dossier « de 48 68 83, sinon l'original de FS ». **Les
trois décors qui demandent la brume en anneau sont exactement les trois qui
reçoivent un dossier.** Frédéric en a vu deux, et ils se comportent pareil.

Ce n'est **pas** une permutation `jin`/`sin` mal posée : côté VF5 R le dossier
de brume est bien celui de `jin`, côté ver.B c'est bien celui de `sin`. Chaque
génération a été lue dans son propre binaire.

### 22.3 Ce que ça tue, et c'est net

Les listes d'animations d'effet, relues dans la reconstruction :

```
l entree 48 (jn5) : ARUKI_A ARUKI_B ARUKI_C TALK MOYA
l entree 68 (snb) : KUMO1 BIRD
```

`MOYA` n'existe que pour `jn5`. Les seules occurrences du nom dans tout le
dépôt sont `STGJN5_*` et `STGJIN_*` — rien pour `sin` ni `snb`. Donc **68 n'a
qu'une seule voie de brume : `TaskEffectFogRing`.** Et il montre le même
défaut que 48.

**La voie 3 du §20 (`STGJN5_EFF_MOYA`) ne peut donc pas être LA cause.** Elle
reste peut-être une seconde pièce manquante sur 48, mais elle n'explique pas
68, qui ne l'a pas. Le défaut commun est dans `TaskEffectFogRing`, **à
l'exécution** — exactement ce que concluait le §21.4, et ça le resserre :

* ce n'est pas une donnée propre à `jn5` : 68 vient d'un autre modèle, d'un
  autre dossier, lu dans un autre binaire ;
* ce n'est pas le nuanceur du décor non plus, sinon le défaut dépendrait du
  décor.

**Et ça donne une épreuve** : une réparation de `TaskEffectFogRing` doit faire
apparaître la brume sur **48 ET 68** d'un coup. Si elle n'en répare qu'un, la
cause n'était pas celle-là.

### 22.4 Un troisième point de mesure, et il est gratuit

**83 = `d25`**, la deuxième variante VF5 R de Dural, atteignable à la barre
espace sur la case de Dural. Elle demande `FOG_RING`, elle n'a **pas** `MOYA`.
Si elle n'a pas de brume non plus, c'est trois sur trois, par la même voie.
**Non mesuré.**

### 22.5 Où ça rejoint l'eau d'Eileen

`eau_ring_eileen.md` §13 : `sk5` ne montre toujours pas d'eau, alors que
`TaskEffectRipple` s'initialise dessus. Même forme de défaut, et la §13 le
disait déjà : **une tâche qui s'initialise, prend sa passe, enregistre son
dessin — et ne paraît pas.** L'observation de Lei Fei ne change pas cette
question, elle la rend plus sûre : le défaut est dans la machinerie partagée
des tâches d'effet, pas dans un décor.

La prochaine mesure reste celle du §21.5, et elle n'exige **aucune course** :
qui remplit `[tâche+0x68]`, et la passe 4 est-elle consommée.
---

## 23. LE JEU D'ORIGINE CONFIRME : LA BRUME EST UNE COUCHE AU SOL (2026-11-20)

### 23.1 Les deux images

Frédéric a montré deux captures du décor de la famille SANCTUARY :

| | ce qu'on y voit |
|---|---|
| **notre build** | de la brume **au fond**, aucune au premier plan. Le sol est net jusqu'aux pieds |
| **le jeu d'origine** (Akira contre Dural, HUD d'arcade, `BONUS STAGE`) | une **couche de brume au sol**, devant la grille, à hauteur de jambes |

Sa phrase : « je te confirme, il y a bien de la brume au 1er plan dans le jeu
d'origine ». **C'est l'écran qui tranche, et il a tranché.**

### 23.2 Ça recoupe exactement ce que le code disait

Le §18.6 et le §18.7 décrivaient déjà cette brume-là, sans qu'on l'ait vue :

* groupe de nuanceurs **`FOGPTCL`** — *fog particle* ;
* texture `F_VF5E_DU2_MU_TUBU2` — **`TUBU` = 粒**, grain ;
* `FUN_180071BC0` lit **les deux combattants**, **cinq os chacun**, et allume
  jusqu'à **dix** émetteurs quand un os passe sous la hauteur
  `DAT_1806431B8` : « une nappe qui réagit aux pieds, pas un décor peint ».

La brume de fond que notre build montre est un **autre** mécanisme : le
brouillard de hauteur du nuanceur du décor (§4, états 15 / `env[14]`). Il
marche. `FOG_RING`, non. **Les deux ne se confondent plus.**

### 23.3 Ce que ça change pour la recherche

L'hypothèse la plus proche du symptôme devient **la hauteur de déclenchement**.
`DAT_1806431B8` est **hors** des 0x3C octets que le stub recopie par décor (le
dossier commence en `0x1806431C8`) : c'est une **globale**. Si elle est réglée
pour la géométrie d'un décor donné, un décor dont le sol est ailleurs
n'allumerait **jamais** un émetteur — tout tourne, rien ne sort au sol, et
c'est exactement l'image.

Elle était déjà nommée comme non mesurée au §18.10. Elle devient la première à
lire, **avant** la passe 4, parce qu'elle explique à elle seule l'écart entre
les deux captures. Et elle se lit **sans course**.

### 23.4 CE QUI N'EST PAS MESURÉ, ET QUI COMPTE

**De quel jeu vient la vidéo d'origine : VF5 R ou VF5 FS ?** Je ne sais pas le
lire sur l'image, et l'écart est décisif :

* si c'est **VF5 R** — tout est cohérent avec le §18.1 : côté 5R, `du2` 22 est
  bien l'un des deux dossiers `FOG_RING`, et notre `d25` (83) en est la copie ;
* si c'est **VF5 FS** — alors le §18.1, « dans le FS de série, PERSONNE ne
  demande `EFFECT_FOG_RING` », est **faux**, et il y a dans le MÊME binaire une
  référence qui marche, à comparer octet par octet avec la nôtre. Ce serait la
  meilleure nouvelle du chantier.

Et il reste à confirmer **quel décor** notre capture montrait — six appuis sur
la case de Dural donnent `d25` (83), mais ça n'a pas été lu à l'écran.
---

## 24. `TaskEffectFogRing` LUE EN ENTIER : MA PROPRE HYPOTHÈSE DU §23.3 TOMBE (2026-11-20)

Lecture de `0x180072130` (init), `0x180071BC0` (les émetteurs) et
`0x1800725A0` (l'intégration) dans la DLL en place. Aucune course.

### 24.1 D'abord, la correction : le §23.3 est FAUX

J'avais proposé que la hauteur globale `DAT_1806431B8` explique l'absence de
brume au sol. **Elle ne l'explique pas.**

Ce qui est vrai, et mesuré : `DAT_1806431B8` vaut **0,2**, elle a **une seule
référence dans toute la DLL** (`0x180071D81`), et c'est une **lecture**.
Personne ne l'écrit — ni le stub, ni l'init. Elle n'est pas par décor.

Mais elle ne garde que les **émetteurs de pas** :

```c
if (*piVar9 == 0) {                              // l'os 0
  if ((y < DAT_1806431b8) && (DAT_1806431b8 <= y_precedent) && (n < 10))
      ... allumer un emetteur ...                // un FRANCHISSEMENT vers le bas
} else if (DAT_180643198 <= vitesse) { ... }     // les quatre autres : a la vitesse
```

Et l'intégration `0x1800725A0` **fait avancer les 2 000 particules à chaque
image, qu'il y ait un émetteur ou non** : les émetteurs n'entrent que dans un
`if (0 < [tache+0x124])` qui les pousse. Hors de ce `if`, chaque particule
intègre sa vitesse, sa traînée (`DAT_1806431A8`), sa gravité
(`DAT_1806431BC`, `DAT_1806431C0`) et se fait **borner à ±9** — `±([+0x0C] ×
0,5 + 1)`, soit ±9 pour `[+0x0C] = 16`.

**La nappe ne dépend donc pas des pieds.** Les pieds la remuent ; ils ne la
créent pas. Une nappe absente n'est pas une affaire de hauteur de
déclenchement.

### 24.2 Ce que l'init fait, et ce qu'elle ne fait pas

`0x180072130(tache, indice_du_decor)` est **entièrement gardée** par :

```c
if (param_2 == (int)DAT_1806431c8) { ... }   // l'indice doit valoir celui du dossier vif
```

Le dossier vif, lu aujourd'hui en `0x1806431C8`, porte les valeurs de série de
`du2` : identifiant **22**, `+0x08` = 2 000, `+0x0C` = 16, `+0x10` = 0,4,
`+0x18` = −0,12, `+0x1C` = **15 650**. Conforme au §18.4. Le stub
(`0x180EA6C50`) y recopie le dossier du décor servi **avant** de sauter ici,
donc pour 48, 68 et 83 **l'égalité tient et l'init tourne**.

Et à l'intérieur, en toute fin :

```c
FUN_18010ca20(4,1);                       // passe 4 ALLUMEE
FUN_18010bdc0(0,FUN_1800729c0,param_1);   // rappel de dessin, ETIQUETTE 0
```

**Donc : le dossier est bon, l'init tourne, les 2 000 particules sont placées
et intégrées, la passe est allumée, le dessin est enregistré.** Tout ce qui
précède le dessin est en place.

### 24.3 Le défaut est au DESSIN, et `passes_rendu.md` l'a déjà nommé

Il ne reste qu'une condition, et elle est entière (`passes_rendu.md` §3) :

> le rappel est appelé **si et seulement si** `*(char*)(g_pRenderPassMgr + 4)`
> vaut autre chose que 0 à cette image.

Et cet octet (§0 de la même note) :

* n'a **aucun compteur de références** ;
* est écrit par **trois tâches sœurs** — `FogRing`, `Ripple`, `SnowRing` ;
* est remis à **0 par le destructeur** de `FogRing` et de `Ripple`, **sans
  aucune garde** « avais-je démarré ? » ;
* et le désenregistrement se fait **par étiquette**, étiquette qui vaut **0
  pour les trois** : il retire **le premier** rappel de la liste, pas
  forcément le sien.

C'est exactement la forme du symptôme, et c'est **le même octet pour la brume
d'Aoi et pour l'eau d'Eileen**. Un seul défaut, pas deux — ce que la §13 de
`eau_ring_eileen.md` pressentait.

### 24.4 LA PROCHAINE MESURE, et elle n'exige toujours aucune course

1. **L'ordre** : au chargement d'un décor, le destructeur d'une tâche sœur
   passe-t-il **après** l'init de `FogRing` ? Si oui, la passe 4 retombe à 0 et
   tous les rappels deviennent muets d'un coup.
2. **`[tache+8]`** : l'init le met à **1** (`param_1[8] = 1`, avant même la
   garde), et `0x180071BC0` n'allume ses émetteurs que si
   `*(char*)(tache+8) == 0`. Qui le remet à 0 ? Si personne, les pas ne
   remueront jamais la nappe — un second défaut, indépendant du premier.
3. Et seulement après, l'état 15.

### 24.5 CE QUI N'EST PAS MESURÉ

* **Que la tâche `TaskEffectFogRing` soit réellement CRÉÉE** pour 48, 68 et 83.
  Tout ce qui précède décrit ce qui se passe **si** elle l'est ; la création
  elle-même n'a pas été lue dans cette séance.
* **La valeur de la passe 4 pendant un combat.** Elle ne se lit pas
  statiquement : c'est une déduction d'ordre d'appels, pas une mesure.
* **Ce que `0x1800729C0` dessine réellement.** Il fait plus de 400 octets et
  appelle `0x18010BEF0` / `0x18010CCA0` (§18.7), mais il n'a pas été ouvert.
* **Le champ `+0x10` d'une particule**, mis à 0 par l'init : s'il s'agit d'une
  durée de vie ou d'une opacité, il pourrait rendre la nappe invisible sans
  émetteur. L'intégration ne le touche pas ; le dessin, lui, n'a pas été lu.
---

## 25. LA VTABLE DE `TaskEffectFogRing`, LUE : UN CANDIDAT FERMÉ, ET LE DERNIER MAILLON NOMMÉ (2026-11-20)

Toujours sans course. La tâche **se nomme elle-même** : `FUN_180072080`
appelle `FUN_180040270("TaskEffectFogRing::dest()\n")`. Plus de doute
d'identification.

### 25.1 La vtable, en `0x18034F6A0`

| créneau | adresse | ce que c'est |
|---|---|---|
| +0x00 | `0x18006E890` | hérité |
| +0x08 | `0x180072580` | |
| +0x10 | `0x180071F50` | **la mise à jour** |
| +0x18 | **`0x180072080`** | **le destructeur** |
| +0x20 | `0x180072100` | |
| +0x28, +0x30 | `0x180007430` | le bouchon `ret 0` |
| +0x38 | **`0x180072B60`** | **l'init** |
| +0x40, +0x48 | `0x180007430` | le bouchon |
| +0x50 | `0x18006FA40` | |
| +0x58 | `0x180072D90` | |

L'autre référence au destructeur, `0x180E6A8C8`, est une entrée **`.pdata`**
(`BeginAddress 0x00072080`), pas une copie de vtable. Rien à en tirer.

### 25.2 Le destructeur, sans la moindre garde

```c
if ([tache+0xa0]) { liberer ; [tache+0xa0] = 0 }
if ([tache+0xa8]) { liberer ; [tache+0xa8] = 0 }
FUN_18010ca20(4, 0);      // LA PASSE 4 S ETEINT
FUN_18010be60(0);         // desenregistre PAR ETIQUETTE 0
FUN_1800f0ba0(0);
DAT_180677b10 = 0;
```

Aucun `si j'ai demarre`. Il éteint la passe **même si l'init n'a rien fait**.
Confirme `passes_rendu.md` §0 mot pour mot, et cette fois sur la tâche nommée.

### 25.3 LE CANDIDAT `[tâche+8]` EST FERMÉ : ce n'est pas un défaut

Le §24.4 point 2 demandait qui remet `[tâche+8]` à 0. **La mise à jour le
fait**, à chaque image, en dernière ligne :

```c
longlong FUN_180071f50(tache) {
  dt = (**(code **)(**(longlong **)(tache + 0x318) + 8))() * 0.016666668;
  if (1e-06 < |dt|) {
    FUN_180071bc0(tache + 0x58, dt);   // les emetteurs
    FUN_1800725a0(tache + 0x58, dt);   // l integration
  }
  ... recopie [sous+0x38] particules de [sous+0x48] vers [sous+0x50] ...
  *(uint *)(tache + 0xb0) = n;         // LE COMPTE A DESSINER
  *(undefined1 *)(tache + 0x60) = 0;   // = [sous+8], puisque le sous-objet est en +0x58
  return ...;
}
```

Le `1` posé par l'init est donc un **drapeau de première image** : il empêche
d'émettre tant qu'il n'y a pas de position précédente valide, et il tombe au
bout de la première mise à jour. **Normal. Ce n'est pas la cause.**

### 25.4 Et le compte à dessiner vient de l'init

La boucle de recopie est gardée par `[sous+0x38]`, que **seule l'init
renseigne** (à 2 000, depuis `+0x08` du dossier). Si l'init n'a rien fait,
`[sous+0x38]` vaut 0, la recopie est sautée, `[tâche+0xb0]` reste **0**, et le
rappel de dessin — s'il est seulement appelé — n'a **rien** à dessiner.
Silence parfait, sans une ligne de journal.

### 25.5 LE DERNIER MAILLON, ET IL EST NOMMÉ

L'init de la vtable passe l'indice **tel quel**, lu au désassembleur :

```asm
180072b6d  MOV EDI, EDX          ; l indice du decor, pris a l appelant
180072b77  ADD RBX, 0x58         ; le sous-objet
180072b7b  MOV EDX, EDI
180072b80  CALL 0x180ea6c50      ; le stub -> recopie le dossier -> 0x180072130
180072b85  MOV [0x180677b10], RBX
```

**Tout tient à cet indice.** La chaîne entière est conditionnelle à
`indice == [0x1806431C8]`, et c'est le stub qui rend cette égalité vraie — à
condition d'avoir reçu le **vrai** indice.

**L'HYPOTHÈSE, et elle explique les trois décors d'un coup** : si l'init est
appelée avec l'indice de **BASE de l'anneau** au lieu du vrai, alors

* pour `jn5` 48 la base est **9**, pour `snb` 68 c'est **10**, pour `d25` 83
  c'est **21** ;
* le stub ne trouve aucun de ces trois dans sa table, recopie donc le dossier
  de série (`du2`, identifiant **22**) ;
* `FUN_180072130(sous, 9|10|21)` compare à 22 → **faux** → **l'init ne fait
  rien** ;
* `[sous+0x38]` reste 0, le compte à dessiner reste 0 ;
* et le destructeur éteint quand même la passe 4.

**Rien dans les données ne serait fautif** — ce qui est exactement ce que les
§18 à §24 ont constaté, chacun de leur côté. Et c'est le **même piège** que
celui des aperçus : l'entrée B du socle (`0x180EA10C0`) met l'indice de BASE
dans `[rbx+0x5c]` et range le **vrai** en `0x180EA1614`.

### 25.6 CE QUI N'EST PAS MESURÉ

* **Qui appelle le créneau +0x38 de la vtable, et avec quel indice.** C'est la
  seule chose qui manque, et elle décide de tout. Elle se lit sans course.
* Que la tâche soit **créée** pour 48, 68 et 83 — toujours pas vérifié.
* Ce que `0x1800729C0` dessine, et le champ `+0x10` d'une particule (§24.5).
* La valeur de la passe 4 pendant un combat : elle ne se lit pas
  statiquement.
---

## 26. LA CHAINE DE RÉPARTITION, LUE EN ENTIER : L'HYPOTHÈSE DU §25.5 EST MORTE, ET CELLE DU §24.3 AUSSI (2026-11-20)

Toujours sans course. Tout ce qui suit est lu dans la DLL en place.

### 26.1 Il n'y a qu'UN conteneur, et les 23 tâches sont ses membres

`FUN_18006EDC0` alloue **0x3978 octets** et appelle `FUN_18006DB10`, qui pose
les 23 vtables **d'affilée** dans ce même objet. `TaskEffectFogRing::vftable`
va en `param_1[0x612]`, soit l'offset **`+0x3090`**. Puis 23 pointeurs
globaux sont écrits, de `0x180677270` à `0x180677320` — un **tableau**, pas
23 variables : `FUN_18006EF40` l'efface d'un seul `memset` de **0xB8 = 23 × 8**
octets.

`(0x300 − 0x270) / 8 = 18`. **`FogRing` est l'indice 18**, et la table de noms
`0x18034E4D0` le confirme mot pour mot :

| 0 `HIT` | 1 `AUTH3D` | 2 `WALL` | 3 `LEAF` | 4 `WATA` | 5 `SNOW` |
| 6 `YUKA` | 7 `RIPPLE` | 8 `RAIN` | 9 `THUNDER` | 10 `DOWN` | 11 `MOVE` |
| 12 `RINGOUT_SPLASH` | 13 `WATER_RING` | 14 `SPLASH` | 15 `SNOW_RING` |
| 16 `FOG_ANIM` | 17 `WET_CLOTH` | **18 `FOG_RING`** | 19 `BREATH` |
| 20 `PARTICLE` | 21 `POISON` | 22 `ELE_BOARD` | |

**La tâche est donc TOUJOURS construite**, pour tout décor. Le §24.5 point 1
(« que la tâche soit réellement créée ») est **tranché : oui**.

### 26.2 Qui appelle le créneau +0x38, et avec quel indice — la question du §25.6

`xrefs` sur l'init `0x180072B60` ne rend que **deux** références : le créneau
de vtable `0x18034F6A0 + 0x38` et une entrée `.pdata`. Elle n'est donc
**jamais appelée directement**. Le seul appelant est la machine d'états
`FUN_18006F380`, par dispatch :

```c
iVar6 = *piVar12;                                    // l indice de TACHE 0..22
lVar2 = *(longlong *)(&DAT_180677270 + iVar6 * 8);   // le pointeur de la tache
puVar3 = (&PTR_s_EFFECT_HIT_18034e4d0)[iVar6];       // son nom
FUN_180245830(*plVar11, puVar3);
(**(code **)(**plVar11 + 0x38))(*plVar11, *param_1); // <<< L INIT
(**(code **)(**plVar11 + 0x50))(*plVar11, ...);
FUN_180245a10(*plVar11, 1);                          // activer
```

`param_1` est le global `DAT_180642FE0`, et c'est `FUN_18006F620` qui le
remplit :

```c
piVar3 = &DAT_180eb65f0 + param_1 * 0x60;   // la fiche du decor, 0x60 octets
_DAT_180642fe0 = param_1;                   // >>> L INDICE DU DECOR, TEL QUEL
DAT_180642fe8 = piVar3;
DAT_1806430b8 = 1;                          // demarre la machine
```

**L'indice passé à l'init est le vrai indice du décor.** Pas l'indice de base
de l'anneau. **L'HYPOTHÈSE DU §25.5 EST FAUSSE, et il faut la tenir pour
morte.** Elle était séduisante parce qu'elle expliquait trois décors d'un
coup, et parce que le même piège avait déjà mordu sur les aperçus. Elle ne
tient pas à la lecture.

### 26.3 La fiche par décor, et les listes qui comptent

La table `0x180EB65F0` est **dans la zone greffée**. Pas de **0x60** par
décor, deux listes terminées par `-1` :

| offset | ce que c'est | consommé par |
|---|---|---|
| `+0x00` .. `+0x1F` | 8 identifiants d'**archives** à charger | `FUN_1800F9C60` / `FUN_1800FB7E0` |
| `+0x20` .. `+0x3F` | 8 indices de **tâches** (0..22) | le dispatch ci-dessus |

Et `tables_generation.py` lit **exactement** `table(0x18006F675) + indice *
0x60 + 0x20` : l'adresse a été retrouvée deux fois, par deux chemins
indépendants.

Les huit fiches lues aujourd'hui :

| décor | liste de tâches en `+0x20` | demande 18 ? |
|---|---|---|
| 9 `jin` (Aoi, FS) | 2 `WALL`, 17 `WET_CLOTH`, 12 `RINGOUT_SPLASH`, 3 `LEAF` | non |
| 10 `sin` (Lei Fei, FS) | 2, 17, 12 | non |
| 21 `du1` (Dural SNOW) | 2 `WALL`, 5 `SNOW`, 19 `BREATH`, 17 `WET_CLOTH` | non |
| 22 `du2` (Dural, FS) | 2 `WALL` | non |
| **48 `jn5`** | **2 `WALL`, 18 `FOG_RING`** | **oui** |
| **68 `snb`** | **2 `WALL`, 18 `FOG_RING`** | **oui** |
| 82 | 2, 5, 19, 17 — la liste de 21 | non |
| **83 `d25`** | **2 `WALL`, 18 `FOG_RING`** | **oui** |

Le §18.1 est donc confirmé par la donnée elle-même : **aucun décor de série ne
demande `EFFECT_FOG_RING`**, et les trois qui le demandent sont bien 48, 68 et
83. Le §22.4 n'est plus un point de mesure à faire : **83 la demande**.

### 26.4 Le stub et sa table sont justes

```c
iVar2 = 3;
for (piVar1 = &DAT_180ea6cc0; iVar2 != 0 && param_2 != *piVar1; piVar1 += 0xf)
    iVar2--;                       // 3 cles, puis la 4e case = le repli
... recopie 0x3C octets vers 0x1806431C8 ...
FUN_180072130();                   // l init
```

Les quatre entrées, lues en `0x180EA6CC0` :

| clé | particules | texture | nom de la texture, résolu dans `tex_db.bin` |
|---|---|---|---|
| **48** | 2 000 | 15460 | `F_VF5E_JIN00_MU_TUBU2` |
| **68** | 2 000 | 8647 | `F_VF5E_SIN00_IK_TUBU1` |
| **83** | 2 000 | 15650 | `F_VF5E_DU2_MU_TUBU2` |
| 22 (repli) | 2 000 | 15650 | idem |

Le premier int de chaque entrée **est la clé**, et c'est lui qui devient
`DAT_1806431C8`. Donc pour 48, 68 et 83 la garde de l'init,
`param_2 == (int)DAT_1806431C8`, **est vraie**. L'init tourne.

### 26.5 L'HYPOTHÈSE DU §24.3 TOMBE AUSSI : il n'y a aucune tâche sœur chargée

La liste **commune**, en `0x18034D530` : `{1 AUTH3D, 10 DOWN, 11 MOVE,
20 PARTICLE, 21 POISON}`. Les ressources communes, en `0x18034D510` : `{21}`.

Pour 48, 68 et 83, l'ensemble complet des tâches est donc
`{1, 10, 11, 20, 21}` + `{2, 18}` = **sept tâches, et `FogRing` est la seule
qui écrive la passe 4**. Ni `RIPPLE` (7) ni `SNOW_RING` (15) n'est chargée.

**Le §24.3 — « une tâche sœur éteint la passe 4 sans garde » — n'a donc aucune
sœur à accuser sur ces trois décors.** Le défaut d'étiquette 0 et l'absence de
compteur de références restent vrais dans l'absolu, mais ils ne peuvent pas
produire CE symptôme ici.

### 26.6 CE QUI RESTE, ET IL N'Y A PLUS QUE LE DESSIN

Tout ce qui précède le dessin est **lu et correct** : la tâche existe, le décor
la demande, l'init est appelée avec le bon indice, le dossier recopié a la
bonne texture, la garde passe, 2 000 particules sont placées, la passe 4 est
allumée, le rappel est enregistré, la tâche est activée. Et rien à l'écran.

Il ne reste donc que **deux** choses, et aucune n'exige de course :

1. **Les pixels de la texture sont-ils livrés ?** `tex_db.bin` n'est qu'un
   **annuaire de noms** — sa propre documentation le dit : « Un decor importe
   n'a donc rien a ajouter ici », les noms et identifiants voyagent **dans
   l'archive**. Que les trois noms y soient ne prouve **pas** que les pixels
   soient dans une archive que notre build charge pour 48, 68 et 83. Et la
   liste `+0x00` de ces trois fiches est **vide** (`-1` d'emblée) : aucune
   archive d'effet propre au décor n'est demandée. C'est la première à lire.
2. **`FUN_1800729C0`**, le rappel de dessin, toujours jamais ouvert (§24.5).

### 26.7 LE CONTRÔLE QUI EXISTE DÉJÀ, ET CE QU'IL NE COUVRE PAS

`VF5RE/tools/tables_generation.py` compare **la DLL patchée** aux listes de la
génération et rend `taches_manquent` / `taches_en_trop`. Lancé aujourd'hui sur
le lot VF5 R : **`jn5` (jin, 48) — manquent `-`, en trop `-`**. Tout concorde.

Mais son lot **s'arrête au décor 60**. Les doublons de Dural (78 à 85), `d25`
compris, **ne sont couverts par aucun contrôle existant**. C'est à étendre.

### 26.8 MES DEUX FAUTES DE CETTE SÉANCE, NOMMÉES

1. **Un décalage d'adresse d'un cran.** J'ai calculé `83 × 0x60 = 0x1EC0` —
   c'est `0x1F20`. J'ai donc lu la fiche du décor **82** en croyant lire celle
   de 83, et j'ai annoncé que 83 ne demandait pas `FOG_RING`. **C'était faux.**
   Relu à `0x180EB8510`, 83 la demande. La coïncidence rendait l'erreur
   crédible : 82 porte bien la liste de 21.
2. **Une absence prise pour un fait.** `tex_db.py --montrer TUBU` filtré et
   tronqué n'a pas affiché `JIN00_MU_TUBU2` ni `DU2_MU_TUBU2`, et j'en ai
   conclu qu'elles manquaient. Résolues par **numéro**, les trois existent.
   C'est la règle du `CLAUDE.md` — un refus, une troncature et une absence font
   **trois** états — et je l'ai enfreinte sur une sortie que j'avais moi-même
   coupée à 20 lignes.
### 26.9 LE SONDAGE DES ARCHIVES LIVRÉES, ET OÙ IL EST AVEUGLE

Relevé dans `runtime/media/vf5fs/vf5fs_media/rom/auth_3d/`. **Le témoin
d'abord**, parce que sans lui un négatif ne vaut rien :

| archive | noms `F_VF5E_` en clair | `TUBU` en clair |
|---|---|---|
| `EFFSTGJN5.farc` | **12** | **oui** |
| `EFFSTGSNB.farc` | **2** | non |
| `EFFSTGD25.farc` | **2** | non |
| `EFFSTGD5R.farc` | **24** | non |
| `STGJN5.farc` / `STGSNB.farc` / `STGD5R.farc` | **0** | non |

Ce que ça permet de dire, et rien de plus :

* les `EFFSTG*.farc` exposent leurs noms **en clair** — le grep y voit, donc un
  négatif y compte. `TUBU` est présent dans `JN5` et absent de `SNB` et `D25` ;
* **les `STG*.farc` n'exposent AUCUN nom** : pour eux le grep est **aveugle**.
  Les pixels d'une texture de décor vivent là. **La présence de
  `F_VF5E_DU2_MU_TUBU2` dans les données livrées n'est donc PAS tranchée**, ni
  dans un sens ni dans l'autre. Trois états, pas deux.
* aucune des quatre archives ne porte le nom **complet** `F_VF5E_*TUBU*` : la
  tâche prend sa texture par **identifiant global**, pas par un nom de scène
  `auth_3d`. Cohérent avec le §26.4.

Et un fait de voisinage, à vérifier avant d'en tirer quoi que ce soit :
`EFFSTGD15.farc` et `EFFSTGD35.farc` portent `TUBU`, **`EFFSTGD25.farc` non**.
Il n'existe par ailleurs **pas de `STGD25.farc`** : les variantes VF5 R de
Dural ont une archive d'effets mais pas de jeu d'objets propre.

**Ce qu'il faut pour trancher** : ouvrir un `STG*.farc` (décompresser), et y
chercher l'identifiant 15650. C'est la prochaine lecture, et elle n'exige
aucune course.
---

## 27. LE RAPPEL DE DESSIN ET LES ARCHIVES, LUS : TOUTE LA CHAÎNE STATIQUE EST JUSTE (2026-11-20)

Les deux dernières portes du §26.6, ouvertes. Toujours sans course.

### 27.1 `FUN_1800729C0` ne dessine AUCUNE particule

```c
void FUN_1800729c0(char *sous) {          // sous = tache + 0x58
  FUN_1800f0ba0(0);
  if (*sous != '\0') {                    // LA GARDE, UN SEUL OCTET
    FUN_1800f0ba0(1);
    cible = FUN_18010bef0(5);             // la CIBLE DE RENDU 5
    FUN_18010cca0(cible, 0); FUN_180248bc0(0x800);
    FUN_18024f500(0, 0, hauteur, largeur);
    c = *(undefined4 *)(sous + 0x40);
    FUN_18024e3c0(c, c, c, 1.0);          // la couleur d effacement : r=g=b=c
    FUN_1802541d0(0x4100);                // EFFACER
    if (FUN_1800ec090(0x16) != 0)
        FUN_1800ea4c0(0x16, 0, 0);        // dessiner la CATEGORIE 0x16
    FUN_180248ba0(); FUN_18010d190(cible);
    ... FUN_1800d1f30(FUN_18010bef0(2), 0, cible, 0, {0.8,0.8,0.8,1.0});  // composer dans la cible 2
  }
}
```

C'est une **passe de composition**, pas un dessin de particules : elle lie la
cible 5, l'efface au gris `[sous+0x40]`, fait dessiner la **catégorie 0x16**,
puis compose la cible 5 dans la cible 2 à 0,8.

Et `FUN_1800EA4C0(categorie)` est le **dessinateur par catégorie** :
`DAT_18070F6A0 + categorie * 0x30` porte le **compte** en `+0x38` (c'est tout
`FUN_1800EC090`) et la **tête de liste chaînée** en `+0x30`. Les éléments ont
un type en `+0x00` : 0 = maillage, 2 = **rappel**, 3 = tableau de maillages.

### 27.2 LA SOUMISSION, c'est le créneau +0x20 — et il porte la même garde

```c
void FUN_180072100(longlong tache) {                      // vtable +0x20
  if (*(char *)(tache + 0x58) != '\0')
      FUN_1800ec7c0(FUN_180072ba0, tache + 0x58, 0x16);   // >>> CATEGORIE 0x16
}
```

La boucle est donc fermée et cohérente : la soumission inscrit un rappel dans
la catégorie 0x16, et la passe 4 dessine cette catégorie dans la cible 5.
**Il n'y a pas de maillon manquant.**

La vtable se complète :

| créneau | adresse | ce que c'est |
|---|---|---|
| +0x08 | `0x180072580` | **journalise `"TaskEffectFogRing::init()\n"`** et rend 1 |
| +0x10 | `0x180071F50` | la mise à jour |
| +0x18 | `0x180072080` | le destructeur |
| **+0x20** | **`0x180072100`** | **la soumission → catégorie 0x16** |
| +0x38 | `0x180072B60` | l'init |
| **+0x50** | **`0x18006FA40`** | **`[tache+0x58] = param`** — la garde, écrasée |
| +0x58 | `0x180072D90` | pose l'horloge en `[tache+0x318]` |

### 27.3 LA GARDE VIENT DU DOSSIER, PUIS LE CHARGEUR L'ÉCRASE

L'init pose la garde **depuis la donnée** :

```c
*param_1 = 1;                                  // par defaut
*(undefined4 *)(param_1 + 0x58) = 0;           // le compte a dessiner
param_1[8] = 1;                                // le drapeau de 1re image
if (param_2 == (int)DAT_1806431c8) {
    *param_1 = DAT_1806431c8._4_1_;            // <<< [sous+0] = l octet +4 DU DOSSIER
    *(undefined4 *)(param_1 + 0x34) = ...;     // le nombre de particules
    *(undefined4 *)(param_1 + 0x1c) = ...;     // la TEXTURE
    *(undefined4 *)(param_1 + 0x40) = DAT_180643200;   // la couleur = dossier +0x38
```

Puis `FUN_18006F380` appelle **+0x50 juste après** l'init, ce qui **écrase**
cette garde avec `*(char *)(machine + 0xDC)` = **`0x1806430BC`**.

La carte du dossier, enfin complète, et **validée** : le dossier statique de
série en `0x1806431C8` est **identique octet pour octet** à la 4e entrée de
repli de notre stub. Le format produit par le générateur est donc juste.

| offset | champ | 22 (repli) | 48 `jn5` | 68 `snb` | 83 `d25` |
|---|---|---|---|---|---|
| +0x00 | l'identifiant = **la clé** | 22 | 48 | 68 | 83 |
| **+0x04** | **la garde du dessin** → `[sous+0]` | **1** | **1** | **1** | **1** |
| +0x08 | particules → `[sous+0x34]` et `[+0x38]` | 2 000 | 2 000 | 2 000 | 2 000 |
| +0x0C | → `[sous+0x0C]` | 16,0 | 16,0 | 12,0 | 16,0 |
| +0x10 | → `[sous+0x10]` | 0,4 | 0,4 | 0,52 | 0,4 |
| +0x18 | → `[sous+0x18]` | −0,12 | −0,12 | −0,28 | −0,12 |
| +0x1C | **la texture** → `[sous+0x1C]` | 15 650 | 15 460 | 8 647 | 15 650 |
| +0x30 | → `[sous+0x30]` | 18,0 | 18,0 | 18,0 | 18,0 |
| +0x34 | → `[sous+0x3C]` | 1,0 | 1,0 | 0,9 | 1,0 |
| **+0x38** | **la couleur** → `[sous+0x40]` | **0,1** | **0,3** | **0,05** | **0,1** |

**La garde vaut 1 dans les quatre entrées.** Rien à corriger là.

### 27.4 LE COMMUTATEUR GLOBAL, ET IL N'EST PAS INDEXÉ PAR DÉCOR

```c
void FUN_18006f9c0(char visible) {        // le commutateur « effets visibles »
  if (DAT_1806430bc != visible && (DAT_1806430bc = visible, DAT_1806430b8 == 4))
      for (chaque tache chargee)  (**(code **)(*tache + 0x50))(tache, visible);
}
```

`DAT_1806430BC` vaut **1 en statique** (lu : `0x1806430B8` = 0, `0x1806430BC` =
1). Son unique appelant est `FUN_18018F680`, **la machine d'états du chargeur
de scène**, dont l'état 3 fait, à la suite :

```c
FUN_18006f620(*(undefined4 *)(requete + 0x5c));   // l indice du decor
FUN_18006f9c0(*(undefined1 *)(requete + 0x70));   // la visibilite des effets
*(undefined4 *)(requete + 0x58) = 4;              // etat = charge
```

**Les deux sont des champs de la MÊME requête de scène.** La visibilité n'est
donc **pas** lue dans une table indexée par le décor : nos indices neufs (48,
68, 83) ne sont pas désavantagés par cette garde. Le §4 de
`ajouter_un_decor.md` n'a rien à y lever.

Au passage, dans la même fonction, une comparaison d'indice **en dur** —
l'entrée `0x18018FAC6` du tableau de ce §4, retrouvée dans son contexte :

```c
if ((requete[0x5c] == 0x28 || requete[0x5c] == 0x10) && scene != 0)
    *(undefined1 *)(scene + 0x334) = 0;
```

### 27.5 LES ARCHIVES : LES TROIS TEXTURES SONT SERVIES

Le §26.9 laissait la question ouverte parce que le grep était aveugle. Elle est
tranchée, et l'aveuglement est **expliqué** :

* `rom/auth_3d/STG*.farc` sont des **FArc NON compressés**, et ils ne portent
  pas de textures : `STGD5R.farc` contient trois scènes `.a3da`
  (`S010A010_DJO_STG_01.a3da`…). D'où zéro nom `F_VF5E_` : ce ne sont pas des
  fichiers de texture ;
* `rom/objset/stg{jn5,snb,d25}.farc` sont des **FArC COMPRESSÉS**, deux membres
  chacun : `*_obj.bin` et `*_tex.bin`. **Voilà pourquoi le grep ne voyait
  rien** — c'était la compression, pas une absence.

Membre `*_obj.bin` lu **en mémoire** (sans extraction), identifiant cherché
comme mot de 32 bits. **Le contrôle d'abord** : on cherche *tous* les
identifiants du même préfixe, pour savoir si le fichier en porte.

| décor | archive | textures du préfixe présentes | la texture du dossier |
|---|---|---|---|
| 48 `jn5` | `stgjn5_obj.bin` | **413 sur 481** | 15 460 → **SERVIE** |
| 68 `snb` | `stgsnb_obj.bin` | **155 sur 460** | 8 647 → **SERVIE** |
| 83 `d25` | `stgd25_obj.bin` | **2 sur 2** | 15 650 → **SERVIE** |

Et `stgd25_obj.bin` nomme les objets correspondants :
`STGDU2_EFF_KUMUTUBU_BMZ` et `STGDU2_EFF_KUMUTUBU2_BMZ` — 雲粒, « grain de
nuage ».

`*_tex.bin` ne porte **aucun** identifiant global (0 sur 2) : on ne peut rien
en conclure, ni dans un sens ni dans l'autre. Trois états.

**LE CANDIDAT TEXTURE EST FERMÉ.**

### 27.6 CE QUI RESTE : PLUS RIEN DE STATIQUE

Bilan des §24 à §27. Tout ce qui se lit sans lancer le jeu est **juste** :

* la tâche est toujours construite (§26.1) ;
* les trois décors demandent la tâche 18 (§26.3) ;
* l'init reçoit le vrai indice du décor (§26.2) ;
* le stub trouve sa clé et recopie un dossier au bon format (§26.4, §27.3) ;
* la garde du dossier vaut 1, le commutateur global vaut 1 (§27.3, §27.4) ;
* 2 000 particules sont placées, intégrées, recopiées, comptées (§24, §25) ;
* la soumission inscrit dans la catégorie 0x16 et la passe 4 la dessine
  (§27.1, §27.2) ;
* la texture est livrée et référencée (§27.5).

**Il n'y a plus de candidat lisible statiquement.** Les trois qui restent sont
des faits d'exécution, et aucun ne se lit dans le binaire :

1. **`[requête de scène + 0x70]` au chargement.** Qui remplit ce champ, et
   avec quoi, dans le mode de jeu où Frédéric regarde.
2. **La cible de rendu 5.** `FUN_18010BEF0(5)` — notre moteur est rustiné en
   1920 × 1080 alors que le journal annonce 1 280 × 720 (§11.1 de
   `apercus_decors_par_version.md`). Si la cible 5 n'est pas allouée, la
   composition n'écrit nulle part. **C'est le candidat le plus sérieux, et il
   est propre à notre build.**
3. **Le compte réellement soumis** : `FUN_1800EC090(0x16)` et `[tache+0xb0]`
   pendant un combat.

### 27.7 LA SONDE EST MAINTENANT PRÉCISE, ET ELLE TIENT EN QUATRE LIGNES

Pour la prochaine course — **et il en faut une**, il n'y a plus d'autre voie.
Quatre faits, journalisés **à l'instant où ils arrivent**, une ligne chacun,
sans période et sans plafond (`CLAUDE.md` §4.3 et §4.5) :

| quoi | où | ce que ça tranche |
|---|---|---|
| `[tache+0x58]` après l'appel de +0x50 | fin de l'état 3 du chargeur | la garde a-t-elle survécu |
| `FUN_18010BEF0(5)` rendu non nul | entrée de `FUN_1800729C0` | la cible 5 existe-t-elle |
| `FUN_1800EC090(0x16)` | dans `FUN_1800729C0` | la soumission est-elle arrivée |
| `[tache+0xb0]` | après la mise à jour | combien de particules à dessiner |

Et il y a **déjà une ligne de journal dans le jeu** : le créneau +0x08
(`0x180072580`) appelle
`FUN_180040270("TaskEffectFogRing::init()\n")`. Avant d'ajouter une sonde,
**grepper les 442 journaux archivés pour cette chaîne** (`CLAUDE.md` §4.1) :
si elle y est, elle dit déjà si la tâche est initialisée, et sur quel décor.
**Non fait.**
### 27.8 LE GREP DES JOURNAUX EST FAIT, ET IL NE DIT RIEN — MAIS IL OUVRE UNE PORTE

`CLAUDE.md` §4.1 appliqué sur-le-champ, puisque c'était gratuit.

**486 journaux** `host_log*.txt` sur le disque. Grep de « FogRing » : **aucun**.
Et **le témoin** — grep de « TaskEffect », qui couvre les 23 tâches et leurs
lignes `init()` / `dest()` : **aucun non plus**.

Le témoin échoue, donc **le silence ne mesure rien**. Et la raison se lit :

```c
undefined8 FUN_180040270(void) { return 0; }
```

**Le journaliseur interne du moteur est neutralisé** dans le build retail. Les
23 chaînes `"TaskEffect*::init()\n"` et `"::dest()\n"` sont bien dans le
binaire ; **personne ne les imprime**. Le §27.7 affirmait qu'il y avait « déjà
une ligne de journal dans le jeu » : c'est **faux**, et c'est corrigé ici.

**Ce que ça ouvre, et c'est mieux que la sonde prévue** : `FUN_180040270` est
un bouchon d'une instruction, appelé par **tout** le moteur avec une chaîne de
format. Le rustiner pour router vers notre journal allumerait d'un coup
l'ensemble des traces d'origine — les 23 tâches d'effet, leurs init et leurs
dest, dans l'ordre réel — **sans écrire une sonde par site**. C'est exactement
ce que les §24.4 et §26.5 voulaient mesurer (l'ordre des appels), et ça
répondrait aussi au chantier de l'eau d'Eileen.

**Non fait, non mesuré, et à peser avant de le faire** : le volume. Un
journaliseur d'origine appelé à chaque image noierait le journal, et
`CLAUDE.md` §4.3 rappelle qu'il y a six plafonds de vingt lignes dans
`vf5fs_host.cpp` qui font taire sans rien dire. Un filtre sur le préfixe de la
chaîne est donc obligatoire, pas optionnel.
## 28. FOG_RING EST DU CODE MORT DANS TOUS LES BUILDS LIVRÉS

Tout le chantier, du §24 au §27, posait que FOG_RING est un effet qui marche
et qu'on avait mal recâblé. **C'est faux, et ça se lit sans course.**

### 28.1 LA MÉTHODE, ET LE SITE REPÉRÉ PAR CONTENU

La table des fiches par décor n'est pas notée : elle est **dérivée du code**.
Le site est la suite d'octets qui calcule `indice * 0x60` puis charge la
table — jamais une adresse, puisque les builds n'en partagent aucune :

```
48 8D 34 6D 00 00 00 00   LEA RSI,[RBP*2]
48 03 F5                  ADD RSI,RBP
48 8D 05 ?? ?? ?? ??      LEA RAX,[rip+disp]      <-- LA TABLE
48 C1 E6 05               SHL RSI,5               <-- *0x20, donc le pas = 0x60
48 03 F0                  ADD RSI,RAX
```

**Les témoins** : la signature doit sortir **une seule fois** (zéro = autre
build, plusieurs = signature trop faible), et le `SHL 5` doit suivre, sinon
le pas n'est pas 0x60. Les huit fichiers lus passent les deux.

**La disposition de la fiche est établie par le code qui la CONSOMME**,
`FUN_18006F380`, pas par une note :

```c
iVar6 = *(int *)(fiche + 0x20 + k * 4);   if (iVar6 == -1) break;   k < 16
while (*(int *)(fiche + j) != -1) { ... } j += 4, j <= 0x1F
```

Archives en `+0x00..0x1F`, indices de tâche en `+0x20`, les deux terminés par
`-1`, seize tâches au plus.

### 28.2 LE RELEVÉ

| build | table | fiches | décors demandant 18 = FOG_RING |
|---|---|---|---|
| APM3 rustinée (la nôtre) | `0x180EB65F0` | **86** | **48, 68, 83** |
| APM3 origine | `0x18034D570` | 41 | **aucun** |
| APM3 sources (`SOURCES/APM3_US`) | `0x18034D570` | 41 | **aucun** |
| REVO Steam | `0x1803775B0` | 41 | **aucun** |
| REVO janvier 2025 | `0x180330830` | 41 | **aucun** |
| LJ d3d12 | `0x1802A9210` | 41 | **aucun** |
| GOG Steam | `0x180241D00` | 41 | **aucun** |
| GOG Yakuza 6 | `0x180241D00` | 41 | **aucun** |

Et la fiche du **décor 22 (`du2`)** — le seul indice que la table
d'acceptation de FOG_RING contient, site `0x18007215C`, table `0x1806431C8`,
**un seul enregistrement** d'après `tools/effets_tables_fs.py` — ne demande
que `{2 = WALL}`, dans les trois variantes APM3.

**Donc : la tâche FOG_RING n'est attachée à aucun décor, dans aucun build
livré que nous détenons.** Sa vtable est construite, son pointeur global
`0x180677300` est écrit au démarrage, sa table d'acceptation nomme le décor
22 — et aucune fiche ne demande la tâche 18, donc `FUN_18006F380` ne
l'attache jamais, ne l'initialise jamais, ne l'appelle jamais. **Elle n'a
jamais dessiné une seule image.** SEGA l'a laissée compilée et débranchée.

**Ce que ça change** : nos greffes sur 48, 68 et 83 sont la **première
exécution de ce code**. On ne répare pas un câblage : on **met en service du
code mort**. Rien dans ses paramètres, son placement, sa liaison de texture
n'a jamais été éprouvé par personne. Et **il n'existe aucun témoin à
l'écran** : forcer le décor 22 ne montrerait rien, puisque 22 ne demande pas
la tâche. Les §25.5, §24.3 et §26.6 cherchaient la cause d'une régression qui
n'existe pas.

### 28.3 MA FAUTE, DITE SUR-LE-CHAMP

J'ai annoncé ce résultat **une fois de trop tôt**, sur un balayage de 90
fiches. Il n'y en a que 41 : au-delà, je lisais ce qui suit la table — des
**pointeurs**, dont la moitié basse (`0x8033E2C8`) sort en entier signé
négatif. Mon premier témoin (« WALL dans au moins 40 fiches sur 90 ») recalait
du coup la table d'origine, dont je savais qu'elle était la bonne. Je n'ai pas
monté le seuil pour le faire passer : j'ai **changé de témoin** — une table
vraie ne contient que des indices légaux `0..22`, et le balayage s'arrête donc
**tout seul** à la première fiche illégale. Les 41 tombent alors
identiquement sur **six fichiers indépendants**, ce qui est le vrai témoin de
la borne.

### 28.4 LA COURSE, ÉCRITE AVANT

Pas de sonde à poser dans la DLL : `tools/sonde_decor.py` force un décor,
mène le jeu au combat **toute seule** (scénario de substitution dans
`apm.dll`, START à 20, 24, 28, 32, 38, 44, 52, 58, 64, 70 s), et accepte des
points d'arrêt. On n'ajoute **aucune ligne** au binaire.

**Décor 48 (`jn5`, le brouillard d'Aoi)**, et pas 83 : sa texture est la
mieux attestée des trois — `413` identifiants `F_VF5E_JIN00_*` sur `481`
présents dans `stgjn5_obj.bin` (§27), et `TUBU` en clair dans
`EFFSTGJN5.farc` (§26.9). Si le chemin échoue là, ce n'est pas faute de
données.

**Les six points de mesure, lus instruction par instruction** — chaque valeur
décisive tombe dans un **registre**, à une adresse connue, donc aucun modèle
de structure n'est supposé :

| adresse | registre | ce que ça dit |
|---|---|---|
| `0x1800729D0` | `Rbp` | le rappel de composition tourne ; `Rbp` = l'objet. Juste avant `CMP byte ptr [RBP],0` + `JZ` : **la garde** |
| `0x180072A00` | `Rax` | **la cible de rendu 5**, après la garde — `MOV RCX,RAX` qui suit `CALL FUN_18010BEF0(5)` |
| `0x180072A7C` | `Rax` | **le compte de la catégorie 0x16**, sur le `TEST EAX,EAX` + `JZ` qui suit `FUN_1800EC090(0x16)` |
| `0x180072C3A` | `Rcx` | **l'identifiant de texture** chargé depuis `[RBX+0x1C]` — doit valoir **15460** pour `jn5` |
| `0x180072C42` | `Rax` | **la texture résolue** par `FUN_1801957A0` — zéro et ça dessine sans texture |
| `0x180072CC6` | `R8` | **le compte de particules** passé à l'appel de dessin — 2 000 attendus |

La commande, à lancer **jeu fermé** :

```
cd "C:\Users\frede\Documents\RECOMP\Virtua Fighter 5 FS\VF5RE"
py -3 tools/sonde_decor.py 48 --secondes 160 --histo 0x1800729D0:rappel:Rbp,0x180072A00:cible5:Rax,0x180072A7C:cat16:Rax,0x180072C3A:texid:Rcx,0x180072C42:texok:Rax,0x180072CC6:dessine:R8 --toutes 12 --depuis 82
```

**Et tout de suite après, avant toute analyse**, copier le journal de côté :
`VF5RE/analysis/sonde_decor.txt` est écrit **en dur**, sans option de nom, et
la course suivante l'écrasera.

Pourquoi `--histo` et pas `--bp` : `--bp` **plafonne en silence**. Son
gestionnaire ne journalise que les passages `n <= 6` puis 50, 500 et 5 000, et
le `finally` n'écrit **que les histos** — le compte total d'un espion ne
ressort **jamais**. C'est le piège de `CLAUDE.md` §4.3, présent dans cet
outil-là. `--histo` n'a pas de plafond et son total est écrit à la fin.
*(Limite à nommer : `--histo` masque à 32 bits, donc `cible5` ne donne que la
moitié basse du pointeur — assez pour distinguer nul de non nul et deux cibles
l'une de l'autre, pas pour lire l'adresse entière.)*

### 28.5 LES ISSUES, NOMMÉES D'AVANCE

| ce que le journal rend | ce que ça prouve | ce qu'on fait ensuite |
|---|---|---|
| `rappel` à **0 coup** | le rappel de composition n'est pas enregistré : la passe 4 ne nous appelle pas | remonter à qui enregistre le rappel, et pourquoi pas nous |
| `rappel` > 0 et `cible5` à **0 coup** | **la garde `[objet+0] == 0` est fermée** : le dossier copié par notre greffe ne l'a pas mise à 1, ou l'init n'a pas tourné | relire `FUN_180072130` et l'octet que la greffe copie |
| `cible5` > 0, valeur **0** | la cible de rendu 5 n'existe pas à ce moment | lire comment `DAT_18070FC68+0x15C+5*4` est renseigné |
| `cat16` > 0 et **toutes ses valeurs à 0** | la tâche ne **soumet rien** : `FUN_180072100` ne s'exécute pas ou n'enregistre pas | remonter à la soumission, vtable `+0x20` |
| `cat16` **non nul** et `dessine` à **0 coup** | la catégorie 0x16 contient autre chose que nous | lire ce que `FUN_1800EA4C0(0x16)` appelle réellement |
| `dessine` > 0 avec `R8` = **2000** | **les particules sont dessinées** : le défaut est en aval — mélange, profondeur, ou la composition de la cible 5 dans l'image | passer aux états de mélange de `FUN_180072BA0` |
| `texid` ≠ **15460** | notre greffe a copié **le mauvais dossier** | relire la table `0x180EA6CC0` et la boucle de clés |
| `texok` à **0** | la texture n'est pas chargée en mémoire : ça dessine transparent | revenir au §27 et à l'archive d'objets |
| **tout à 0 coup** et les captures montrent un menu | **le combat n'a pas démarré** — course perdue, pas un résultat | relancer avec moins de points d'arrêt, ou `--appuis` ajusté |

**Le risque principal de cette course** : les points d'arrêt logiciels coûtent
une exception par passage. Six sites à une image chacun font environ 29 000
exceptions sur les 80 s de combat. Les appuis du scénario sont sur une horloge
**murale** : si le jeu rame, ils tombent dans le mauvais menu et le combat ne
démarre pas. Ce qui limite le risque, et c'est lisible dans les adresses : en
dehors du combat, **seul `rappel` peut se déclencher** — les cinq autres sont
après la garde ou dans le dessin des particules. Les menus tournent donc à
vitesse à peu près normale, et les dix appuis tombent avant le ralentissement.
**Non mesuré**, nommé comme pari.

**Et c'est l'écran qui tranche** : les sept captures (`82 s` à `154 s`, pas de
12 s, dans `VF5RE/analysis/sonde/`) sont à **regarder**, pas à mesurer en
pourcentage de pixels non noirs (§7).

### 28.6 LA LISTE DE CONTRÔLE AVANT-POSE, FRANCHIE

1. **La sonde parle-t-elle déjà ?** Les 37 journaux `apm_journal*` /
   `sonde*.txt` du disque grepés, avec **témoin** : 9 d'entre eux répondent à
   une chaîne certaine, donc le grep y voit. Aucun ne porte `fogring`,
   `72ba0`, `729c0` ni `cible`. **Aucune course n'a jamais posé ces points
   d'arrêt.** Le silence compte.
2. **Les gardes englobantes, jusqu'au sommet.** `FUN_1800729C0` n'a qu'une
   garde, `CMP byte ptr [RBP],0` à `0x1800729D0`, et c'est précisément ce
   qu'on mesure par différence entre `rappel` et `cible5`. `FUN_180072BA0` n'a
   que `CMP dword ptr [RCX+0x58],0` à `0x180072BA6`, mesurée de même par
   `dessine`. Aucun interrupteur de lanceur en jeu : la sonde ne lit pas
   `host_log`, elle pilote `vfes.exe` directement.
3. **Un plafond de lignes ?** Oui, et c'est pour ça qu'on n'utilise pas
   `--bp` — voir §28.4. `--histo` n'en a pas.
4. **Le déclenchement est-il un fait du jeu ?** Oui : aucun `image + N`.
   Chaque point d'arrêt est une **instruction**, et chaque valeur est lue au
   moment où le jeu la calcule.
5. **Le bilan sort-il sans sortie propre ?** Oui. La sonde se termine
   **elle-même** après `--secondes` ; Frédéric n'a pas à fermer le jeu, et le
   bloc `finally` écrit les histos même sur exception. Les histos comptent
   **chaque** passage, sans période et sans plafond.
6. **Mes contrôles visent-ils l'état, ou les mots ?** L'état : six registres
   lus dans le processus, et la garde mesurée par un **écart** entre deux
   comptes, jamais par une chaîne cherchée dans un fichier.

**À faire avant de lancer** : le jeu doit être **fermé**, et Windows retient
la mise en sourdine par application — lancer `py -3 tools/muet.py --rendre`
pendant que la course tourne.
## 29. LA CHAÎNE EST LUE EN ENTIER — ET ELLE RÉDUIT LA COURSE À DEUX ISSUES

Demandé : lire l'init et la soumission avant de dépenser une course. Fait, et
ça a entraîné quatre lectures de plus, toutes gratuites. **Le §28.4 est
périmé : sa course mesurerait six choses dont cinq sont maintenant tranchées
par la lecture.**

### 29.1 L'OBJET, ENFIN NOMMÉ SANS SUPPOSITION

`FUN_180072B60` (créneau `+0x38` de la vtable) fait
`FUN_180EA6C50(param_1 + 0xb, indice)` — sur un `longlong*`, donc **+0x58**.
L'objet que toute la chaîne manipule est donc **`S = tâche + 0x58`**, et
`FUN_180072B60` en garde un pointeur direct dans **`DAT_180677B10`**. Plus
besoin de passer par `0x180677300` et son décalage : une seule indirection
suffit.

Tout recoupe : `FUN_1800729C0` teste `[S+0]` (la garde) et lit `[S+0x40]` en
flottant (la couleur) ; `FUN_180072100` teste `[S+0]` et inscrit le dessin
avec **S** ; `FUN_180072BA0` teste `[S+0x58]`, lit la texture en `[S+0x1C]`
et les sommets en `[S+0x50]`.

### 29.2 L'INIT, ET LA SEULE GARDE QUI COMPTE

```c
*param_1 = 1;                           // la garde a 1, AVANT le test
*(undefined4 *)(param_1 + 0x58) = 0;    // le compte de dessin a ZERO
...
if (param_2 == (int)DAT_1806431c8) {    // la cle du dossier que la greffe a copie
    *param_1 = DAT_1806431c8._4_1_;     // la garde reprend l octet +4 du dossier
    ... 2000 particules placees, deux tableaux alloues ...
    FUN_18010ca20(4, 1);
    FUN_18010bdc0(0, FUN_1800729c0, param_1);   // le rappel est enregistre ICI
}
```

**Tout est sous la clé.** Si la greffe ne trouve pas l'indice, elle retombe sur
l'entrée de repli (clé 22), `DAT_1806431C8` vaut alors 22, le test échoue pour
48 — et **rien** ne se produit : ni placement, ni rappel. C'est un tout ou
rien, pas une dégradation.

### 29.3 LE COMPTE DE DESSIN NE DÉPEND PAS DE L'INTÉGRATION

`FUN_180071F50` (l'update, créneau `+0x10`), chaque image :

```c
if (1e-06 < |dt|) { FUN_180071bc0(S, dt); FUN_1800725a0(S, dt); }
uVar1 = *(uint *)(param_1 + 0x90);       // = S[0x38], le compte SOURCE
... copie uVar1 particules de S[0x48] (pas 0x2C) vers S[0x50] (pas 0x20) ...
*(uint *)(param_1 + 0xb0) = uVar1;       // = S[0x58], LE COMPTE DE DESSIN
```

Et `S[0x38]` est écrit une seule fois, par l'init, depuis le **dossier
`+0x08`**. Donc : **si l'init a tourné, le compte de dessin vaut 2000 à chaque
image, inconditionnellement.** L'intégration ne peut pas le changer — elle ne
peut que déplacer des particules.

### 29.4 L'ÉTIQUETTE 0 EST NORMALE — LA PISTE EST MORTE

`FUN_18010BDC0(0, rappel, données)` empile un triplet dans une **liste** à
`DAT_18070FC68+0x400` ; le `0` est une **étiquette**, pas un rang. Et
`FUN_18010CA20(4,1)` n'est pas une passe : c'est `[DAT_18070FC68+4] = 1`.

Elle n'a que **trois** appelants : notre init `0x180072130`, et `0x18007AE10`
et `0x18007D820` — les inits de deux effets acceptés par de **vrais** décors
(`{4, 15}` et `{16}` d'après `tools/effets_tables_fs.py`), donc deux effets
qui tournent. Les deux font, à l'instruction près :

```
MOV ECX, 0x4   /  CALL 0x18010CA20      ; le meme octet d autorisation
XOR ECX, ECX   /  CALL 0x18010BDC0      ; la meme etiquette ZERO
```

**Notre enregistrement est structurellement identique à deux effets qui
dessinent.** L'hypothèse « enregistré sur la mauvaise passe » est morte.

*(Au passage : `0x18007AE10` lit sa table d'acceptation en `0x180EC2D30`,
dans la zone ajoutée, par une boucle terminée par `-1` — nous avions donc
déjà greffé cet effet-là, et dans un style **différent** de
`FUN_180EA6C50`, qui compte trois clés en dur avec un repli. Les deux
marchent, mais ce n'est pas la même main.)*

### 29.5 LES QUATRE DOSSIERS, DÉCODÉS

Relevé à `0x180EA6CC0`, pas de 0x3C, et interprété **comme l'init les lit** :

| | clé | garde `+04` | particules `+08` | `+0C` | `+10` | `+18` | texture `+1C` | `+30` | `+34` | gris `+38` |
|---|---|---|---|---|---|---|---|---|---|---|
| entrée 0 | **48** `jn5` | 1 | 2000 | 16.0 | 0.4 | -0.12 | **15460** | 18.0 | 1.0 | 0.3 |
| entrée 1 | **68** `snb` | 1 | 2000 | 12.0 | 0.52 | -0.28 | **8647** | 18.0 | 0.9 | 0.05 |
| entrée 2 | **83** `d25` | 1 | 2000 | 16.0 | 0.4 | -0.12 | **15650** | 18.0 | 1.0 | 0.1 |
| entrée 3 (repli) | **22** `du2` | 1 | 2000 | 16.0 | 0.4 | -0.12 | 15650 | 18.0 | 1.0 | 0.1 |

**L'entrée 2 est octet pour octet l'entrée 3**, la clé exceptée — donc le
dossier de `d25` est le dossier d'origine de SEGA pour DU2, ce qui est
cohérent : `d25` est un doublon de DU2 et réemploie sa texture 15650.

Aucune valeur absurde : garde à 1 partout, 2000 particules partout, les bonnes
textures, un gris non nul. Et le placement de l'init répartit les 2000
particules sur **±8 unités en X et en Z** autour de l'origine (`0.5 * 16.0`),
Y vers 0.4 ± 0.5 — une nappe au sol parfaitement sensée.

### 29.6 CE QUI RESTE, ET CE QUE ÇA FAIT DE LA COURSE

**La chaîne statique est correcte de bout en bout**, de la fiche du décor
jusqu'à l'appel de dessin, avec des paramètres sains, et identique en
structure à deux effets qui dessinent. Il n'y a **plus de maillon non lu**.

Il ne reste donc que **deux** issues, pas neuf :

1. **l'init n'a pas tourné** — tout ou rien, §29.2 ;
2. **les 2000 particules sont dessinées et invisibles.**

Et pour la deuxième, un candidat que la lecture ne peut pas écarter et que
**aucune** des neuf issues du §28.5 n'aurait vu : `FUN_180071BC0` et
`FUN_1800725A0` intègrent les particules, et c'est du **code jamais exécuté**
(§28). S'ils lisent un champ non initialisé et produisent des positions
**NaN**, le matériel rejette chaque triangle, rien n'apparaît — et le compte
reste 2000, la texture se résout, la garde est ouverte, la catégorie est
peuplée. **Tous les compteurs seraient sains et l'écran noir.** C'est
exactement le mode de défaillance d'un effet jamais mis en service.

**Donc la course ne doit pas compter : elle doit lire les COORDONNÉES.**

### 29.7 LA COURSE RÉVISÉE — DEUX POINTS D'ARRÊT

```
cd "C:\Users\frede\Documents\RECOMP\Virtua Fighter 5 FS\VF5RE"
py -3 tools/sonde_decor.py 48 --secondes 160 --bp 0x180072CC6:dessine:**0x180677B10+0x50+0x0,0x180072C42:texture:*0x180677B10+0x1c --toutes 12 --depuis 82
```

* `0x180072CC6` — `R8` porte le **compte** passé à l'appel de dessin (2000
  attendus), et la mémoire est la **double indirection** vers le premier
  sommet : `[[S]+0x50]` est le tableau de sommets, et le journal rend ses
  quatre premiers mots **en hexa et en flottant**. Une position `NaN` sort en
  `7FC00000` / `nan`, un zéro en `0`. **C'est le mot qui tranche.**
* `0x180072C42` — `RAX` porte la **texture résolue** (zéro = pas chargée), et
  la mémoire donne l'identifiant demandé, 15460 attendu.

Ici le plafond de `--bp` (passages 1 à 6, puis 50, 500, 5000) est **sans
conséquence** : ces valeurs sont constantes ou le deviennent, et six passages
suffisent à les lire. C'est pour **compter** que `--bp` est inutilisable, pas
pour lire.

| ce que le journal rend | ce que ça prouve |
|---|---|
| `dessine` à **0 coup** | l'init n'a pas tourné : la greffe n'a pas trouvé la clé 48 — issue 1 |
| `R8` = 2000 et les sommets **`nan`** | **la cause est trouvée** : l'intégration produit des positions invalides |
| `R8` = 2000 et les sommets **tous à 0** | les particules sont toutes à l'origine, donc dégénérées |
| `R8` = 2000, sommets sensés (±1 après le ×0.125), `texture` non nul | tout est correct jusqu'au matériel : le défaut est dans le **mélange**, la **profondeur**, ou la composition de la cible 5 |
| `texture` à **0** | la texture 15460 n'est pas en mémoire : ça dessine transparent |
| tout à 0 coup **et** les captures montrent un menu | le combat n'a pas démarré — course perdue, pas un résultat |

Deux points d'arrêt au lieu de six : le risque de désynchronisation des dix
appuis, nommé au §28.5, tombe d'autant.

**Et c'est toujours l'écran qui tranche** : les sept captures de
`VF5RE/analysis/sonde/` sont à **regarder**.

### 29.8 CE QUI N'EST TOUJOURS PAS MESURÉ

* `FUN_180071BC0` et `FUN_1800725A0` ne sont **pas lus** — c'est délibéré : la
  course va dire en un coup si leur résultat est valide, ce qu'une lecture de
  plus ne garantirait pas.
* la queue de `FUN_1800729C0` — `FUN_18010BEF0(2)` puis `FUN_1800D1F30` —
  compose la cible 5 dans la cible 2. **Non lue.** Si le mélange y est nul,
  rien ne sort même avec des particules parfaites. C'est la lecture à faire
  **si** la course rend « tout correct ».
* la texture 15460 est **servie** par `stgjn5_obj.bin` (§27) ; que ses pixels
  ne soient pas uniformément transparents n'a **jamais** été vérifié.
## 30. LA COMPOSITION EST LUE — ET LA CIBLE DE RENDU 5 EST ÉCARTÉE

Dernière lecture gratuite du §29.8 : la queue de `FUN_1800729C0`, qui compose
la cible 5 dans la cible 2.

### 30.1 CE QUE C'EST

`FUN_1800D1F30` n'est qu'une **enveloppe** :

```c
void FUN_1800d1f30(longlong dest, undefined4 p2, longlong src, undefined4 p4,
                   undefined8 couleur)
{
  FUN_18010cca0();            // lie la destination (RCX = dest a l entree)
  FUN_1800d1fa0(*(u32 *)(*(longlong *)(dest + 8) + 0x10), p2,
                *(u32 *)(*(longlong *)(src  + 8) + 0x10), p4, couleur);
  FUN_18010d190(dest);
}
```

Et `FUN_1800D1FA0` est le **noyau de composition** — précisément la fonction
que l'effet qui marche (`0x18007D820`) appelle **directement**, sans
l'enveloppe. Même machinerie, pas une voie à nous.

Les constantes, relevées :

| | valeur |
|---|---|
| `0x18034B3EC` — la couleur de composition de FOG_RING | **0,8** (donc `{0.8, 0.8, 0.8, 1.0}`) |
| `0x180348BB0` — celle de l'effet qui marche | `{1.0, 1.0, 1.0, 1.0}` |
| `0x180346D3C` — l'alpha, `XMM6` | **1,0** |
| `0x180346D38` | 0,5 |

Non nulles, et voisines. **La composition ne multiplie pas par zéro.**

### 30.2 L'ARGUMENT QUI ÉCARTE LA CIBLE 5, ET IL TIENT À UNE ABSENCE DE PLANTAGE

`FUN_1800D1FA0` s'ouvre sur :

```c
if (((int)param_1 != 0) && ((int)param_3 != 0)) { ... }
```

`param_3` est l'identifiant de surface de la **source**, c'est-à-dire la cible
5, obtenu en **déréférençant** `[cible5 + 8]` puis en lisant `+0x10`. Si la
cible 5 n'avait pas de surface, `[cible5 + 8]` vaudrait 0 et cette ligne
lirait l'adresse `0x10` : **violation d'accès**. Pas un silence — un plantage.

Or le jeu ne plante pas sur ces décors : Frédéric voit le ring, il ne voit
pas le brouillard. Donc :

* **soit la composition tourne**, et alors la cible 5 **a une surface
  valide** — elle n'est pas la cause ;
* **soit la composition ne tourne pas du tout**, et c'est que la garde
  `[S+0] == 0` a fait sortir `FUN_1800729C0` à son `JZ 0x180072B4F` — ce qui
  est **l'issue 1** (l'init n'a pas tourné), pas un problème de cible.

**Dans les deux cas, « la cible de rendu 5 n'est pas allouée » n'explique pas
un brouillard absent sans plantage.** L'hypothèse de départ du §27.6, et la
question qui a nommé la course, sont closes — tranchées par une **absence de
plantage**, sans dépenser une image.

*(Et `FUN_18010BEF0` ne rend jamais nul, §27 : son arithmétique n'a pas de
chemin vers zéro. Les deux lectures se recoupent.)*

### 30.3 UN DÉTAIL QUI N'EN EST PAS UN

`FUN_1800729C0` fait la composition **après** le `JZ` qui saute le dessin de
la catégorie 0x16 quand elle est vide (`0x180072A7E`). Donc la composition a
lieu **même si rien n'a été dessiné** : la cible 5 est alors composée vide, ce
qui ne produit rien de visible et ne plante pas. C'est cohérent avec ce qu'on
observe, et ça veut dire que **voir la composition tourner ne prouve rien sur
le dessin**. Seul le compte de la catégorie, ou les sommets, le disent.

### 30.4 CE QU'IL RESTE, APRÈS TOUTES LES LECTURES

La chaîne est lue de la fiche du décor jusqu'au mélange final. Il ne reste
**que quatre candidats**, et aucun n'est accessible à la lecture statique :

1. **la garde est fermée** — l'init n'a pas tourné, tout ou rien (§29.2) ;
2. **des positions `NaN` ou dégénérées** sorties de `FUN_180071BC0` /
   `FUN_1800725A0`, du code jamais exécuté (§29.6) ;
3. **les pixels de la texture 15460** sont vides ou entièrement
   transparents — la texture est *servie* (§27), ses pixels n'ont **jamais**
   été regardés ;
4. **l'état de mélange** posé dans `FUN_180072BA0` — `FUN_180248BC0(0xffffffff)`
   puis `FUN_18024A6A0(2)` — avec un fond de cible 5 inconnu.

Les candidats 1 et 2 sont exactement ce que lit la course révisée du §29.7, en
deux points d'arrêt.

Le candidat **3 est gratuit et ne demande aucune course** : `tools/bc.py` et
`tools/bc_rapide.py` décodent déjà le BC/DXT, et `tools/textures_hd.py` sait
manipuler ces jeux de textures. Il reste à situer les pixels de 15460 dans
`stgjn5_obj.bin` / `stgjn5_tex.bin`, dont le **format conteneur n'a pas été
lu**. Et le §7 de `CLAUDE.md` impose la suite : convertir en PNG et
**regarder** — pas compter des pixels non noirs.

Le candidat 4 demande de connaître ce que vaut la cible 5 avant le dessin :
ça ne se lit pas, ça se mesure.
## 31. LA TEXTURE EST REGARDÉE — ELLE EST BONNE, LE CANDIDAT 3 TOMBE

Le candidat 3 du §30.4 : les pixels de 15460 sont-ils vides ? **Non.** Fait
sans course, et **en regardant**, pas en comptant (`CLAUDE.md` §7).

### 31.1 AUCUN OUTIL NEUF — LA RÈGLE §6 A PAYÉ TROIS FOIS

Tout existait, et j'ai failli écrire un parseur pour rien :

* `tools/farc.py` ouvre le `FArC` compressé ;
* `tools/objset.py` **lit l'en-tête du jeu d'objets** — c'est la pièce qui
  manquait, et l'index des notes la donnait (`reference_vf5_objset_lecture.md`,
  « un objset se LIT ») ;
* `tools/txp.py` rend les pixels, et pose même un **damier** sous l'alpha ;
* `tools/tex_db.py` donne le nom d'un identifiant.

L'en-tête du jeu d'objets, déjà documenté dans `objset.py` :
`+0x1C` l'offset de la table des identifiants de texture, `+0x20` leur
**nombre**.

### 31.2 LA FAUSSE PISTE, ET POURQUOI LE TÉMOIN L'A ARRÊTÉE

Premier essai : chercher 15460 comme mot aligné dans `stgjn5_obj.bin` et
prendre la plage d'identifiants légaux autour. Elle a rendu **495**, puis
**589 sur 605** en élargissant. Le témoin exigeait l'égalité avec les 605
textures du jeu TXP : il a **refusé**, et il avait raison — les mots qui
précédaient étaient une suite continue `7267, 7268, 7269…`, donc la table
commençait ailleurs et le rang trouvé aurait été faux. **Une image sortie sous
un nom non justifié aurait été pire que pas d'image.**

L'en-tête tranche sans heuristique :

| | |
|---|---|
| jeu d'objets `stgjn5_obj.bin` | 447 objets, id max 451, **605 textures**, table à `0x11AEF40` |
| jeu TXP de `stgjn5_tex.bin` | **605 textures** |

**605 = 605** : les deux tables sont parallèles, et **15460 est au rang 435**.

### 31.3 CE QU'ON VOIT

Planche dans `analysis/brume_texture_jn5_15460.png` — pixels sur damier,
alpha seul, couleur seule.

| rang | identifiant | nom | format | ce qu'on voit |
|---|---|---|---|---|
| **435** | **15460** | `F_VF5E_JIN00_MU_TUBU2` | 64×64 DXT5 | **une bouffée de fumée blanche**, couleur blanc pur, alpha en dégradé doux jusqu'à 160 |
| 434 | 15459 | `F_VF5E_JIN00_MU_TUBU1` | 64×64 DXT5 | la même chose, une autre bouffée — la paire |
| 433 | 7664 | `F_VF5E_JIN00_IK_TUBU2` | 16×16 DXT5 | un bruit bleu-gris, autre chose |
| 436 | 7665 | `F_VF5S_AOI00_TK_FENCE` | 256×512 DXT1 | une structure éclairée orange, opaque |

**Le témoin de décodage passe** : `TK_FENCE` ressemble à ce que son nom
annonce, donc la chaîne `farc → objset → TXP → DDS → pixels` est juste. Et la
cible est **exactement** ce qu'une texture de particule de brouillard doit
être.

À noter : la couleur est **blanc pur**. Toute la teinte vient donc de
`FUN_18024E3C0` dans `FUN_1800729C0`, qui reçoit le gris du dossier — 0,3 pour
`jn5`. Cohérent, et ça veut dire qu'un gris trop faible assombrirait le
brouillard sans jamais le faire disparaître.

### 31.4 OÙ ON EN EST

Des quatre candidats du §30.4, **le 3 est mort**. Il reste :

1. **la garde est fermée** — l'init n'a pas tourné (§29.2) ;
2. **des positions `NaN` ou dégénérées** sorties de `FUN_180071BC0` /
   `FUN_1800725A0` (§29.6) ;
4. **l'état de mélange** de `FUN_180072BA0`, sur un fond de cible 5 inconnu
   (§30.4).

Les trois se mesurent, aucun ne se lit. **La lecture statique est finie.** Les
1 et 2 sont exactement ce que rend la course révisée du §29.7, en deux points
d'arrêt ; le 4 ne se décidera qu'à l'écran, sur les captures.
## 32. LA COURSE EST COURUE — LA CHAÎNE VA JUSQU'AU MATÉRIEL, L'ÉCRAN EST VIDE

Course du 20 novembre 2026, 20 h 00, décor 48 `jn5`, deux points d'arrêt.
Journal archivé : `courses/sonde_brume_jn5_20261120_2000.txt`.

### 32.1 LE JOURNAL A CHANGÉ — LA PREUVE, PAS LE CODE DE SORTIE

| | avant | après |
|---|---|---|
| taille | 974 o | **5 597 o** |
| SHA-256 | `0650758826386A3E…` | **`1406605AE95DE0BD…`** |

Le code de sortie était 0 dans les deux cas et n'a rien prouvé (`CLAUDE.md` §3).

### 32.2 CE QUE LA SONDE A RENDU

Décor : `decor demande 13 -> force a 48`. Comptes : **4 903** passages sur la
demande de décor, **4 617** sur `dessine`, **4 617** sur `texture` — égaux, donc
chaque soumission porte sa texture.

| point | ce qui est lu | valeur |
|---|---|---|
| `0x180072C42` `texture` | `RAX` = texture résolue | **non nul** à chaque passage (`0x12548D27D28`) |
| `0x180072C42` `texture` | `[S+0x1C]` = l'identifiant demandé | `0x00003C64` = **15460** ✔ |
| `0x180072CC6` `dessine` | `R8` = particules passées au dessin | **`0x7D0` = 2 000** à chaque passage |
| `0x180072CC6` `dessine` | `[[S+0x50]]`, quatre flottants | voir ci-dessous |

Les quatre flottants, images 1 à 6 puis 50 puis 500 :

```
#1    3F8C9481 3D800000 3ED3265A 3F800000  =   1.09828  0.0625  0.412402  1
#2    3F8CB8EB 3D800000 3ED36441 3F800000  =   1.09939  0.0625  0.412874  1
#3    3F8CDD55 3D800000 3ED3A228 3F800000  =   1.10050  0.0625  0.413347  1
#6    3F8D4A93 3D800000 3ED45BDD 3F800000  =   1.10384  0.0625  0.414763  1
#50   BF8C9610 3D800000 3EDEFF91 3F800000  =  -1.09833  0.0625  0.435544  1
#500  BF192778 3D800000 3F25E86C 3F800000  =  -0.598258 0.0625  0.648078  1
```

**Aucun `NaN`, aucun zéro, et ça bouge** — monotone d'une image à l'autre, et
borné dans ±1,1. L'intégration tourne.

### 32.3 L'ISSUE EST LA QUATRIÈME

Des six issues nommées d'avance au §29.7, c'est celle-ci :

> `R8` = 2000, sommets sensés, `texture` non nul → **tout est correct jusqu'au
> matériel : le défaut est dans le mélange, la profondeur, ou la composition de
> la cible 5.**

Et les trois candidats survivants du §31.4 se réduisent à **un seul** :

| candidat | sort |
|---|---|
| 1 — la garde est fermée, l'init n'a pas tourné | **mort** : `R8` = 2 000, donc l'init a tourné et la clé 48 a été trouvée |
| 2 — positions `NaN` ou dégénérées | **mort** : les valeurs sont finies, variées et vivantes |
| 4 — le mélange, la profondeur, la composition | **seul debout** |

### 32.4 L'ÉCRAN — REGARDÉ, PAS COMPTÉ

Capture `analysis/sonde/d48_t130.png`, 2 592 × 1 518, à t = 130 s : écran
**YOU LOSE** sur `jn5`, Akira en gros plan, plancher de bois et tatamis au bas
du cadre. Agrandie à pleine résolution sur trois zones — le fond lointain, le
sol à gauche, le sol à droite :

* le voile bleu pâle qui couvre l'image est **uniforme** : c'est le fondu de
  fin de round, pas des bouffées ;
* le **grain du bois est net**, les motifs des tatamis sont nets, les bords des
  lames sont francs ;
* **aucune bouffée, aucune granulation, aucun halo au ras du sol.**

**Rien n'est dessiné**, alors que 2 000 particules sont soumises avec leur
texture résolue, 4 617 fois.

### 32.5 LES CAPTURES — UN REFUS N'EST PAS UNE ABSENCE

Sept captures étaient prévues (82 à 154 s) ; **une seule** a été écrite. Et la
sonde dit pourquoi, ligne par ligne :

* 82, 94, 106, 118 s : **`capture REFUSEE` — la fenêtre du jeu est recouverte
  par une autre.** Elle a refusé d'enregistrer le bureau plutôt que de rendre
  une image qui ne mesure rien ;
* 130 s : écrite ;
* 142 et 154 s : jamais atteintes, le processus était sorti.

Aucune anomalie : les quatre manquantes sont des **refus annoncés**, pas des
silences.

### 32.6 CE QUI N'EST PAS PROUVÉ, ET QU'IL NE FAUT PAS COMPTER COMME ACQUIS

* **Que `[[S+0x50]]` soit le tampon de sommets** — c'est ma lecture, pas une
  preuve. Ce qui est établi, c'est que cette mémoire est finie et vivante, pas
  ce qu'elle représente. Le deuxième flottant, **`0,0625` constant de l'image 1
  à la 500**, ne ressemble pas à une coordonnée qui s'intègre ; si c'était une
  **taille**, 1/16 d'unité sur un décor de rayon 16 serait un point invisible.
  À vérifier avant d'y bâtir quoi que ce soit.
  > **CORRIGÉ au §33.2 :** c'en est bien le tampon de sommets, et `0,0625` est
  > bien la coordonnée **Y**. Le pas de sommet vaut `0x20` et le premier
  > attribut fait 12 octets — lu dans l'appel, pas supposé. L'hypothèse
  > « taille » est morte.
* **Une seule image, en fin de round, caméra en gros plan.** Elle montre le sol
  de près et il est net — mais ce n'est pas une mesure sur toute la durée du
  combat.
* **L'état de mélange de `FUN_180072BA0` n'est toujours pas lu**, ni la
  profondeur, ni ce que contient la cible 5 au moment de la composition.

### 32.7 OÙ VA LA SUITE

Un seul candidat debout, et il **se lit sans course** : l'état de mélange et de
profondeur posé par `FUN_180072BA0`, comparé à celui des deux effets qui, eux,
dessinent (`0x18007AE10`, `0x18007D820`). C'est une lecture statique, gratuite,
et elle n'a jamais été faite.
## 33. L'ÉTAT DE RENDU EST LU — IL EST NORMAL, ET DEUX DE MES PISTES TOMBENT

Lecture statique seule, **zéro course**, sur la demande de Frédéric. Elle
répond au candidat 4 du §32.3, et la réponse est **négative** : il n'y a pas
d'anomalie d'état de mélange.

### 33.1 LA RÈGLE §6 A PAYÉ UNE QUATRIÈME FOIS

`FUN_180072ba0`, `FUN_18007ae10` et `FUN_18007d820` étaient **déjà décompilés**
dans `code_decompile/` (`fogring_dessin_fs.c`, `effets_ripple.c`,
`effets_snowring_fs.c`). Un grep avant, et trois décompilations évitées.

### 33.2 UN FAIT ACQUIS AU PASSAGE — LE TAMPON DE SOMMETS EST IDENTIFIÉ

```c
FUN_180247600(3,   0x161, 0x20, [S+0x50]);        // canal 0 = POSITION
FUN_1802470a0(4,   0x161, 0x20, [S+0x50]+0x0c);   // canal 3
FUN_1802475b0(0xe, 1, 0x161, 0, 0x20, [S+0x50]+0x1c);
```

`FUN_180247600` et `FUN_1802470a0` sont deux enveloppes de `FUN_180246b30`,
qui ne diffèrent que par leur dernier argument : **0** pour la première, **3**
pour la seconde. Le canal 0 est la position.

**Le pas est `0x20` et le premier attribut tient sur 12 octets** (le suivant
est à `+0x0C`). Donc les quatre flottants lus pendant la course du §32 étaient
`x, y, z` **suivis du premier mot du canal 3**. `0,0625` est bien **Y**, pas
une taille. Le §32.6 est corrigé en conséquence.

### 33.3 LE JUMEAU GÉOMÉTRIQUE — `FUN_1800819B0`

Parmi les quinze tireurs qui passent par `FUN_180247230`, un est l'exact
homologue de FogRing : **même pas `0x20`, mêmes décalages `+0`, `+0x0C`,
`+0x1C`, même format `0x161`, même mode de tirage `2`**. C'est le témoin de
comparaison qui manquait depuis le début.

### 33.4 LA COMPARAISON, ÉTAT PAR ÉTAT

| | FogRing | SnowRing (dessine) | Ripple (dessine) | jumeau `0x1800819B0` |
|---|---|---|---|---|
| nettoyage `248BC0` | `0xffffffff` | — | — | `0xffffffff` |
| empilage `24A6A0` | 2 | 2 | 2 | `0xffffffff` |
| sommets `247100` | 300 | 300 | 300 | 300 |
| pixels `2473B0` | `0x12D` | `0x12D` | `0x12D` | — |
| programme | `975970(0x2A)` | `975870("SN_FOOT")` | `975870("RIPEMIT")` | `975970(0x1B)` |
| **états allumés** | **`0xAC`, `0x318`, `0x2CD`** | **`0x318`, `0xAC`, `0x2CD`** | `0x318` | `0x318`, `0x2CD` |
| `2573A0` | `(0x318,0x319,1)` | `(0x318,0x319,1)` | — | `(0x318,0x319,1)` |
| `24F2A0` | `0x311` | `0x311` | `0x311` | `0x311` |
| texture sur `0x21D` | oui | oui | — | oui |

**FogRing allume exactement le même jeu d'états que SnowRing, qui dessine.**
Rien ne manque, rien n'est en trop, rien n'est aberrant. **Le candidat 4 ne
tient pas par la lecture.**

### 33.5 DEUX FAUSSES PISTES, LES MIENNES, MORTES EN COURS DE LECTURE

**(a) `FUN_18024F2D0(18.0)`.** J'ai cru tenir l'anomalie : FogRing lui passe
`[S+0x30]` = **18,0** là où Ripple et SnowRing passent une valeur voisine de 1
et **restaurent à `0x3F800000` = 1,0**. C'est faux. La fonction écrit un
scalaire global unique (`contexte+0xD9598`) que ces deux effets alimentent de
la même façon avec leur propre valeur ; **18,0 est une taille de point
parfaitement plausible**, et c'est la valeur d'origine de SEGA — elle est
identique dans les **quatre** dossiers, DU2 compris.

**(b) « la sélection du programme par indice est fragile ».** FogRing demande
son programme par **indice** (`FUN_180175970(0x2A)`), sans repli, tandis que
les deux effets qui dessinent le demandent par **nom**
(`FUN_180175870`), avec un repli à `0x31` et une indirection. L'argument
paraissait fort. **Le témoin l'a tué** :

| voie | appelants |
|---|---|
| `FUN_180175970` — par **indice** | **22** |
| `FUN_180175870` — par **nom** | **2** |

L'indice est **la norme**, le nom l'exception. L'hypothèse tombe.

*(Et la table de programmes `DAT_180714B00`, pas `0x30`, est en `.bss` : 384
octets lus à l'entrée 42 et ses voisines rendent **zéro**. Elle est remplie à
l'exécution, donc elle ne se lit pas statiquement — ce n'est pas une absence,
c'est une illisibilité.)*

### 33.6 CE QUI RESTE DEBOUT, ET QUI NE SE LIT PAS

**Le masque d'écriture de couleur, `FUN_18024E5A0`.** FogRing **ne l'appelle
jamais** — il hérite donc de ce que le dessin précédent a laissé. Ripple le
pose à `(0,0,0,1)` et SnowRing à `(1,0,0,0)`, et **tous deux le restaurent à
`(1,1,1)` — trois arguments sur quatre**, le quatrième restant la valeur
résiduelle du registre. Si l'effet qui tourne juste avant FogRing laisse le
masque fermé, FogRing tire 2 000 particules dans le vide sans rien écrire.

C'est la seule hypothèse encore debout, et **elle dépend de l'ordre
d'exécution** : elle se mesure, elle ne se lit pas. Le jumeau
`FUN_1800819B0` ne l'appelle pas davantage — mais **je n'ai pas établi qu'il
dessine réellement à l'écran**, donc il ne lave FogRing de rien.

### 33.7 LE BILAN, SANS L'ARRONDIR

La lecture demandée est **faite** et elle est **négative**. Elle n'a pas trouvé
la cause ; elle a fermé le candidat 4 tel qu'il était posé, tué deux de mes
propres pistes, et rendu un fait acquis (§33.2) plus un témoin de comparaison
(§33.3). Il ne reste rien de lisible sur ce chemin : la suite est une mesure.
## 34. LA COURSE SUR LE MASQUE — CONSIGNE ÉCRITE AVANT, ISSUES NOMMÉES D'AVANCE

**Rien n'est lancé.** Cette section est posée *avant* la course, comme l'exige
`CLAUDE.md` §3, et elle se relira ensuite avec son compte.

### 34.1 LE FAIT QUI REND LA COURSE POSSIBLE

`FUN_180253C90()` rend `DAT_180C414F8` : **le contexte est un global**, donc
adressable depuis l'extérieur. Et `FUN_18024DD20` livre le sens des clés — ce
que le §33 ne faisait que constater :

| clé | ce qu'elle fait réellement |
|---|---|
| **`0xAC`** | **LE MÉLANGE.** Allumé : écrit `0xE` dans les bits bas de l'octet `objet+0x50`, et recopie **six** facteurs depuis `états+0x5C..0x61` vers `objet+0x51..0x56`. Éteint : remet l'octet à `& 0xF0`. |
| `0x318` | écrit `états+0x9E4`, lève `0x2002` |
| `0x8D` | écrit `états+0x70`, touche la profondeur (`objet+0x58..0x60`) |
| `0x7A` | écrit `états+0xA0C`, touche `objet+0x40..0x4C` |

Et `FUN_18024E5A0(a,b,c,d)` écrit les bits **hauts** (`0x10`/`0x20`/`0x40`/
`0x80`) du **même octet `objet+0x50`**.

> **UN SEUL OCTET PORTE LES DEUX RÉPONSES.**
>
> | `[[0x180C414F8]] + 0x50` | |
> |---|---|
> | bits bas `0x0F` | **mélange** : `0xE` = allumé, `0x0` = éteint |
> | bits hauts `0xF0` | **masque d'écriture** des quatre canaux |
>
> Chaîne exacte : `contexte = [0x180C414F8]`, `objet = [contexte+0]`,
> octet à `objet+0x50`. C'est la forme `**A+B+C` que la sonde sait lire.

### 34.2 LA VALEUR ATTENDUE, ET POURQUOI ELLE SE PASSE DE TÉMOIN EXTERNE

Au point `0x180072CC6`, FogRing a **déjà** appelé `FUN_18024E900(0xAC)`
quelques instructions plus haut. Donc, si sa pose d'état atteint le matériel :

* bits bas = **`0xE`** (le mélange qu'il vient d'allumer) ;
* bits hauts = **`0xF0`** (les quatre canaux ouverts) ;
* **l'octet doit valoir `0xFE`.**

Toute autre valeur est la cause. Le contrôle peut donc **échouer sur une faute
réelle et réussir sur une pose juste**, sans avoir besoin d'un effet témoin qui
tournerait sur `jn5` — ce qu'on ne sait pas garantir.

### 34.3 LA LIGNE, ET POURQUOI DEUX SONDES ET PAS UNE

```
py -3 "C:\Users\frede\Documents\RECOMP\Virtua Fighter 5 FS\VF5RE\tools\sonde_decor.py" 48 ^
  --secondes 160 ^
  --bp "0x180072CC6:melange_au_tirage:**0x180C414F8+0x0+0x50" ^
  --histo "0x18024E5A0:masque_pose:Rcx+Rdx+R8+R9" ^
  --toutes 12 --depuis 82
```

Les deux plafonds de l'outil sont **vérifiés dans le source**, pas supposés :

| sonde | plafond réel | angle mort | ce qui le couvre |
|---|---|---|---|
| `--bp` | **8 relevés** (`n <= 6 or n in (50,500,5000)`), **silencieux** | un masque qui ne se fermerait qu'à certaines images | l'histogramme, qui n'a pas de plafond |
| `--histo` | aucun, et il rend les totaux | **il ne sait pas lire la mémoire** (`regs.split('+')` : registres seuls) | les 8 relevés de `--bp`, qui lisent l'octet effectif |

Chacune couvre l'angle mort de l'autre. **Aucun outil neuf n'est écrit.**

### 34.4 LES ISSUES, NOMMÉES D'AVANCE

| ce que le journal rend | ce que ça prouve |
|---|---|
| octet = **`0xFE`** | mélange allumé et quatre canaux ouverts : **le masque est innocent**, la piste du §33.6 tombe et il ne reste plus rien de nommé |
| bits hauts = **`0x00`** | **la cause est trouvée** : FogRing tire dans un masque fermé, hérité du dessin précédent |
| bits hauts ≠ `0xF0` mais ≠ `0` | un ou deux canaux fermés — cause partielle, à relire facteur par facteur |
| bits bas = **`0x0`** | le mélange n'est **pas** allumé au matériel bien que `0xAC` ait été posé : la pose n'arrive pas jusqu'à l'objet, et c'est un résultat plus grave que le masque |
| `[mem] pointeur 0x… = 0` | la sonde **refuse** la lecture : le contexte n'existe pas à cet instant. **Un refus, pas une absence** — course à refaire plus tard dans le combat |
| `masque_pose` ne contient que `(1,1,1,·)` | personne ne ferme jamais rien : le masque est hors de cause avant même de lire l'octet |
| le 4ᵉ registre de `masque_pose` est **du bruit** | `FUN_18024E5A0(1,1,1)` n'a que **trois** arguments : le canal alpha est alors posé au hasard par Ripple et SnowRing, et c'est une piste neuve |
| aucun passage sur `melange_au_tirage` | le combat n'a pas démarré sur 48 — **course perdue, pas un résultat** |

### 34.5 CE QUE FRÉDÉRIC DOIT FAIRE, ET CE QUI A COÛTÉ LA DERNIÈRE FOIS

* **Garder la fenêtre du jeu au premier plan.** À la course du §32, **quatre
  captures sur sept ont été refusées** parce qu'une autre fenêtre la
  recouvrait. La sonde a eu raison de refuser, mais l'écran n'a été mesuré
  qu'une fois.
* **Aller au combat sur le décor 48** et y rester ; la sonde s'arrête seule à
  160 s.
* Le jeu doit être **fermé avant** le lancement.

*(Réserve honnête : `--toutes 12 --depuis 82` est un déclenchement au **temps**,
pas un fait du jeu — `CLAUDE.md` §4.4. C'est acceptable ici parce que le temps
ne commande que les **captures** ; le fait qui tranche, lui, est relevé sur un
point d'arrêt, donc à l'instant exact du tirage.)*
## 35. LA COURSE SUR LE MASQUE EST COURUE — LE MÉLANGE EST SAIN

Course du 20 novembre 2026, 20 h 22. Journal archivé :
`courses/sonde_masque_jn5_20261120_2022.txt`. Les issues du §34.4 se relisent
ici avec leur compte.

### 35.1 LE JOURNAL A CHANGÉ

| | avant | après |
|---|---|---|
| taille | 5 597 o | **5 756 o** |
| SHA-256 | `1406605AE95DE0BD…` | **`1F25476B5ADBE23F…`** |

### 35.2 L'OCTET VAUT `0xFE` — L'ISSUE 1

Mot relevé à `[[0x180C414F8]]+0x50`, **identique aux 8 relevés** :

```
[mem 0x10EC1A17E50] 050101FE 08020206 00FFFF20 81118111
```

En petit-boutien, l'octet de `+0x50` est le poids faible du premier mot :
**`0xFE`**.

* bits bas **`0xE`** → le mélange est **ALLUMÉ** ;
* bits hauts **`0xF0`** → les **quatre canaux** sont ouverts.

> **C'est exactement la valeur annoncée au §34.2. Le masque d'écriture est
> innocent, et le mélange est bien actif. La piste du §33.6 est morte.**

### 35.3 LES SIX FACTEURS, LUS ET NON DEVINÉS

La course a rendu plus que demandé : les octets `+0x51..+0x56`, qui sont la
recopie des facteurs `[états+0x5C..0x61]`. Leur sens vient de
`FUN_18024C760` et `FUN_18024C870`, **lus** :

`FUN_18024C760(états, opCouleur, opAlpha)` écrit `0x5C` et `0x5D` par une
table explicite — `0x3CE`→**1**, `0x3CF`→4, `0x3D0`→5, `0x3D1`→2,
`0x3D2`→3, **défaut → 1**. `FUN_18024C870(états, src, dst, srcA, dstA)` écrit
`0x5E..0x61`.

| octet | rôle | valeur relevée |
|---|---|---|
| `0x5C` | opération couleur | **1** |
| `0x5D` | opération alpha | **1** |
| `0x5E` | facteur source couleur | **5** |
| `0x5F` | facteur destination couleur | **6** |
| `0x60` | facteur source alpha | **2** |
| `0x61` | facteur destination alpha | **2** |

**Aucun facteur nul, source et destination distinctes, opération à la valeur de
repos** — celle que SnowRing restaure en sortie (`FUN_18024E300(0x3CE)`). Dans
la convention habituelle, 5 et 6 sont `SRC_ALPHA` et `INV_SRC_ALPHA` : le
mélange translucide classique, exactement ce qu'il faut pour du brouillard.

*(Réserve : `FUN_18024C1A0` fait la conversion finale et n'a pas été lue. Mais
la conclusion n'en dépend pas — ce qui compte est qu'il n'y a **ni `ZERO`/`ZERO`
ni facteur manquant**.)*

### 35.4 L'HISTOGRAMME — ET UNE ISSUE DU §34.4 QUI TIRE

27 543 appels à `FUN_18024E5A0`, 3 727 valeurs distinctes :

| masque posé | coups |
|---|---|
| `(1, 1, 1, 1)` | **10 964** |
| `(0, 0, 0, 0)` | **10 962** |
| `(1, 1, 1, <bruit>)` | 3 725 valeurs, 4 à 8 coups chacune |

Deux faits :

1. **Quelqu'un ferme les quatre canaux près de 11 000 fois**, presque autant
   qu'il les ouvre. Ce n'est pas au moment où FogRing tire — les 8 relevés
   disent `0xF0` — mais c'est un comportement à connaître.
2. **L'issue « le 4ᵉ registre est du bruit » a tiré.** 3 725 valeurs distinctes
   pour `R9` : `FUN_18024E5A0(1,1,1)` n'a bien que **trois** arguments, et le
   canal alpha est posé au hasard par Ripple et SnowRing en sortie. Ghidra
   avait raison. Cela ne touche pas FogRing, qui ne l'appelle jamais.

### 35.5 L'ÉCRAN — UN VRAI COMBAT, CETTE FOIS

Deux captures écrites, et la troisième **refusée** et dite (`aucune fenêtre
"Virtua Fighter" à t=106 s`) — un refus, pas un silence.

* `d48_t082.png` : **Akira contre Goh en plein combat**, barres de vie, `16`
  au chrono, `1st STAGE`. Le dojo d'Aoi au-dessus de l'eau.
* `d48_t094.png` : le même décor en `REPLAY`.

Agrandies à pleine résolution — sol devant les pieds, sol à droite, base des
rochers : **le plancher est lisse, les lames de bois sont franches, aucune
bouffée, aucune granulation, aucun halo au ras du sol.** Le voile bleu pâle est
le brouillard atmosphérique du décor, uniforme et lointain, pas des particules.

**3 860 tirages de 2 000 particules, état de mélange sain, texture résolue —
et rien à l'écran.**

### 35.6 LA LIMITE, NOMMÉE D'AVANCE ET TOUJOURS VRAIE

**8 relevés sur 3 860.** Le plafond de `--bp` était annoncé au §34.3 ; il tient
toujours. Les 8 sont identiques au bit près, et l'histogramme couvre ce que les
8 ne voient pas côté masque — mais il reste strictement vrai qu'**un état qui
se dégraderait sur une poignée d'images précises passerait inaperçu**.

### 35.7 OÙ ON EN EST — PLUS AUCUNE HYPOTHÈSE NOMMÉE N'EST DEBOUT

Toutes les causes nommées depuis le §30 sont tombées, chacune par une mesure ou
une lecture :

| | sort |
|---|---|
| la garde fermée, l'init n'a pas tourné | mort (§32) — `R8` = 2 000 |
| positions `NaN` ou dégénérées | mort (§32) — finies et vivantes |
| les pixels de la texture | mort (§31) — bouffée blanche nette |
| la cible de rendu 5 | mort (§30) — absence de plantage |
| l'état de mélange | mort (§33) — mêmes états que SnowRing |
| le masque d'écriture de couleur | **mort (§35)** — `0xF0` |
| les facteurs de mélange | **mort (§35)** — `1/1/5/6/2/2` |

**Il ne reste rien de nommé.** Ce qui n'a jamais été lu, en revanche, est connu
et court :

* **le programme 42 lui-même.** `FUN_180175970(0x2A)` indexe `DAT_180714B00`,
  pas `0x30`, **en `.bss`** : illisible statiquement (§33.5), mais
  `_DAT_180715638` reçoit l'indice et l'entrée est lisible **en marche**. C'est
  la seule pièce de la chaîne dont on n'a jamais vu le contenu.
* `FUN_180071BC0` et `FUN_1800725A0`, délibérément jamais lus ;
* la profondeur, et ce que contient la cible 5 au moment de la composition.
## 36. LA PRÉPARATION A TUÉ LA COURSE — DEUX HYPOTHÈSES MORTES, ZÉRO COURSE

Frédéric a dit « prépare » pour une course sur le programme 42. **La
préparation a répondu à la question sans la course**, et en a tué une seconde
au passage. Voilà pourquoi la liste de contrôle du §4 existe.

### 36.1 LA RÈGLE §6 A PAYÉ DEUX FOIS DANS LE MÊME MOUVEMENT

**(a) `VF5RE/tools/shader_empreintes.py`**, écrit le 11 septembre 2026, porte
en en-tête un diagnostic qui change tout :

> le moteur APM3 tourne sur Direct3D 11, où un point fait **TOUJOURS un
> pixel**. Le portage a donc donné un **geometry shader** aux cinq programmes
> de points (conteneurs `GSFX` : `fog_ptcl`, `particle.1`,
> `snow_particle.0/1`, `water_particle`) — et PAS à `snow_footprint..vp`.

Or **FogRing tire en mode 2 = POINTLIST**, 2 000 points, avec
`FUN_18024F2D0([dossier+0x30])` = **18,0** comme taille de point — une taille
que D3D11 **ignore** sans geometry shader. 2 000 points d'un pixel à alpha
faible : rigoureusement invisibles. C'était le symptôme exact.

**(b) Ma propre note, §8**, posée le 19 novembre, documentait déjà la table :

> `0x180176410` : **nom → indice de groupe**, `strcmp` sur les 48 noms, pas de
> 0x30 sur le **tableau vivant `0x180714B00 + indice*0x30`**

Le §33.5 la déclarait « illisible statiquement, en `.bss` ». **C'est vrai du
tableau vivant, et faux de la question** : sa contrepartie statique est la
table maîtresse `0x180554378`, 48 enregistrements de 0x28, **noms lisibles**.
Et l'outil qui la lit existait déjà : `VF5RE/tools/cle_permutation.py`.

### 36.2 L'INDICE 42 EST `FOGPTCL` — LE BON PROGRAMME

`cle_permutation.py` rend les 48 groupes, et son propre contrôle passe
(**4 206 jeux de chiffres sur 4 206 recalculés à l'identique**) :

| indice | nom | |
|---|---|---|
| 26 | `WATRING` | |
| 27 | `W_PTCL` | celui du jumeau `FUN_1800819B0` |
| 30 | `SN_FOOT` | le nom littéral de SnowRing |
| 37 | `RIPEMIT` | le nom littéral de Ripple |
| **42** | **`FOGPTCL`** | **celui que FogRing demande par `FUN_180175970(0x2A)`** |

**FogRing demande exactement le bon programme.** L'hypothèse du §33.5 — déjà
affaiblie par le témoin 22-contre-2 — est définitivement morte, et cette
fois **sans dépenser une course**.

### 36.3 ET `FOG_PTCL` A BIEN SON GEOMETRY SHADER

Lecture de `shader_pxd_w64.farc` (3 950 membres) par `farc.py`, aucun outil
neuf. Un conteneur `GSVS` ne porte qu'un programme de sommets ; un `GSFX`
porte GSVS + GSPS + **GSGS**.

| membre | tête | |
|---|---|---|
| **`fog_ptcl..vp`** | **`GSFX`** | **porte un geometry shader** |
| `particle.1.vp` | `GSFX` | |
| `snow_particle.0.vp` | `GSFX` | |
| `snow_particle.1.vp` | `GSFX` | |
| `water_particle..vp` | `GSFX` | |
| `snow_footprint..vp` | `GSVS` | le défaut connu, toujours là |

**Le témoin passe sur les cinq** : `snow_footprint` ressort bien en `GSVS` et
les quatre autres en `GSFX`, exactement comme le prédisait la note de
septembre. La lecture des quatre octets de tête est donc juste.

*(Le témoin a d'abord **échoué**, et il avait raison de m'arrêter : j'avais
inclus les membres `.fp`, qui sont des **pixel** shaders et n'ont jamais eu à
être des `GSFX`. La faute était dans mon périmètre, pas dans le seuil — je l'ai
borné aux `.vp`, je n'ai pas assoupli le contrôle.)*

### 36.4 LE BILAN : NEUF CAUSES MORTES

| | sort |
|---|---|
| la garde fermée, l'init n'a pas tourné | mort (§32) |
| positions `NaN` ou dégénérées | mort (§32) |
| les pixels de la texture | mort (§31) |
| la cible de rendu 5 | mort (§30) |
| l'état de mélange | mort (§33) |
| le masque d'écriture de couleur | mort (§35) |
| les facteurs de mélange | mort (§35) |
| **le mauvais programme** | **mort (§36) — c'est `FOGPTCL`** |
| **le geometry shader manquant** | **mort (§36) — `fog_ptcl..vp` est un `GSFX`** |

### 36.5 LA PISTE NEUVE, ET ELLE EST PRÉCISE

`shader_empreintes.py` livre un dernier fait, dans son propre contrôle de
fabrication :

```python
if 'gs_5_0' not in t_gs or 'cb12[28]' not in t_gs:
    raise Refus('le geometry shader compile ne lit pas cb12[28]')
```

**La taille de point vient de `cb12[28]`**, lue par le geometry shader. Et
`FUN_18024F2D0(v)` écrit son scalaire à `contexte+0xD9598`. **Le pont entre les
deux n'a jamais été lu.** Si `cb12[28]` ne reçoit pas les 18,0 — parce que le
tampon n'est pas lié au geometry shader, ou pas mis à jour sur ce chemin — les
quadrilatères sont **dégénérés** et rien ne se voit, exactement comme
maintenant.

Cela se lit **sans course** : `shader_empreintes.py` porte déjà
`sous_blocs()`, `dxbc_de()` et `desassembler()`. Il suffit de désassembler le
GSGS de `fog_ptcl..vp` et celui de `water_particle..vp` — qui, lui, dessine —
et de comparer ce qu'ils font de `cb12[28]`.
## 37. LE GEOMETRY SHADER EST DÉSASSEMBLÉ — CONFORME, ET LA CHAÎNE SE FERME

Lecture seule, **zéro course**. Outils : `farc.py` et les fonctions
`sous_blocs()`, `dxbc_de()`, `desassembler()` de `shader_empreintes.py`, qui a
une garde `__main__` — l'importer ne fait rien. **Aucun outil neuf.**

### 37.1 LES QUATRE GS LISENT `cb12[28]` — LA PISTE DU §36.5 TOMBE

| membre | `cb12[28]` | la ligne de taille |
|---|---|---|
| **`fog_ptcl..vp`** | **1×** | `mul r1.xy, cb12[28].xyxx, v[0][0].yyyy` |
| `snow_particle.0.vp` | 1× | `mul r1.xy, cb12[28].xyxx, v[0][0].yyyy` |
| `water_particle..vp` | 1× | `mul r1.xy, cb12[28].xyxx, v[0][1].xxxx` |
| `particle.1.vp` | 1× | `mul r1.xy, cb12[28].xyxx, v[0][1].xxxx` |

Les trois témoins la lisent, donc la constante est la bonne ; et la cible la
lit aussi. **`fog_ptcl` est identique à `snow_particle.0`, qui dessine.**

*(Contrôle du contrôle : une constante inventée, `cb99[123]`, se trouve 0 fois.)*

### 37.2 LA SIGNATURE CORRIGE MA LECTURE DU REGISTRE

Un numéro de registre ne dit rien seul. La signature d'entrée de `fog_ptcl` :

```
// Name            Index  Mask  Register  SysValue
// TEXCOORD            8  x            0      NONE
// COLOR               1   y           0      NONE
// SV_POSITION         0  xyzw         1       POS
```

Donc `v[0][0].y` = **`COLOR1`**, pas la position. J'avais cru un instant lire
« la taille vient de `position.y` » : **c'est faux**, et la signature le dit.

Le calcul complet du demi-quadrilatère :

```
mul r1.xy, cb12[28].xyxx, v[0][0].yyyy    // × COLOR1    (la taille)
mul r1.xy, r1.xyxx, v[0][1].wwww          // × position.w (la perspective)
mul r1.xy, r1.xyxx, l(0.5, 0.5, 0, 0)
```

puis quatre `emit_stream` : un `trianglestrip` de 4 sommets, `dcl_maxout 4`.
**Le point est bien étendu en quadrilatère.**

### 37.3 D'OÙ VIENT `COLOR1` — LA CHAÎNE SE FERME

`shader_empreintes.py` le nommait déjà : `COLOR1.x` est **l'attribut 14**. Et
FogRing pose exactement cela : `FUN_1802475B0(0xE, 1, 0x161, 0, 0x20,
[S+0x50]+0x1C)` — attribut 14, **un** composant, à **`+0x1C`** du sommet.

`FUN_180071F50` remplit le tampon, et tout s'aligne enfin :

```c
pfVar3[0..2] = pfVar4[0..2] * 0.125;   // +0x00  position / 8
pfVar3[3..5] = <depuis S+0x78 / S+0x80>;// +0x0C  canal 3
pfVar3[6]    = fVar2 * pfVar4[10];     // +0x18  alpha   (fVar2 = S+0x3C)
pfVar3[7]    = pfVar4[9];              // +0x1C  TAILLE
```

Le `× 0.125` explique les **±1,1** relevés au §32 pour des particules placées
à ±8, et `0,0625` = 0,5 × 0,125 : **le §33.2 tenait**.

Et la taille, posée une fois par l'init (`FUN_180072130`) :

```c
fVar1 = *(float *)(param_1 + 0x30);                     // = 18.0
*(float *)(particule + 0x24) = ((fVar22 + fVar22) - fVar25) + fVar1;
```

soit **un aléa centré sur 18,0** — le même champ `S+0x30` que FogRing passe à
`FUN_18024F2D0`. L'octet `0x24` est bien l'indice **9** d'une particule de
`0x2C` (11 flottants), et `FUN_180071F50` copie `pfVar4[9]` en `+0x1C`. **La
chaîne taille → COLOR1 → geometry shader est complète et cohérente.**

### 37.4 DEUX AUTRES PISTES MORTES AU PASSAGE

* **Le débordement de tampon.** Le tampon de sommets est alloué pour
  `[S+0x34]` et rempli sur `[S+0x38]` — deux champs distincts. Mais l'init
  écrit `uVar7 = DAT_1806431D0; [S+0x38] = uVar7; [S+0x34] = uVar7;` :
  **les deux reçoivent la même valeur**. Pas de débordement.
* **L'intégration n'écrase pas la taille.** `FUN_1800725A0` touche les indices
  0, 2, 6, 7, 8 et 10 de la particule — **jamais le 9**. La taille survit à
  toutes les images.

### 37.5 DIX CAUSES MORTES, ET DEUX CASES JAMAIS OUVERTES

À la liste du §36.4 s'ajoute **le geometry shader non conforme** : mort. Dix.

Mais la lecture a isolé **les deux seules cases du sommet qui n'ont jamais été
mesurées** — le §32 lisait quatre mots depuis `+0x00`, donc `+0x00` à `+0x0C` :

| | ce qu'elle porte | ce qui la rend nulle |
|---|---|---|
| **`+0x18`** | **l'alpha** = `[S+0x3C] × particule[10]` | `S+0x3C` à 0, ou la durée de vie tombée à 0 |
| **`+0x1C`** | **la taille** = `particule[9]` ≈ 18,0 | une copie manquée par la greffe |

L'une ou l'autre à zéro donne **exactement** le symptôme : 2 000 quadrilatères
soumis, état sain, et rien à l'écran — transparents, ou dégénérés.

**Et les deux se lisent d'un seul relevé.** Quatre mots depuis `+0x18`
rendent l'alpha, la taille, **et** les `x, y` du sommet suivant — un témoin
d'alignement interne, qui doit retomber dans les ±1,1 déjà connus :

```
--bp "0x180072CC6:alpha_et_taille:**0x180677B10+0x50+0x18"
```

C'est la dernière case de la chaîne, et elle ne se lit pas autrement : ces
valeurs n'existent qu'en marche.
## 38. LA COURSE SUR L'ALPHA ET LA TAILLE — LA CONSIGNE, ÉCRITE AVANT

Les deux dernières cases du sommet, nommées au §37.5. **Aucun outil neuf**, et
la ligne est celle du §32 avec **deux offsets changés** : rien d'autre.

### 38.1 LA LISTE DU §4, FAITE AVANT

**§4.1 — la sonde parle-t-elle déjà ?** **Non.** Les 498 journaux grepés, par
les **noms d'espion**, pas par des mots : il n'en existe que quatre dans toute
l'histoire du disque — `espion:dessine`, `espion:melange_au_tirage`,
`espion:texture`, `histo:masque_pose`. Aucun n'a jamais porté sur `+0x18` ni
`+0x1C`.

*(Mon premier grep a cherché la **spécification** `0x50+0x0` dans les journaux
et n'a rien trouvé — normal : un journal ne garde que le **nom** de la sonde et
l'adresse résolue, jamais sa spécification. C'était une faute §4.6 — viser les
mots qui parlent de l'état au lieu de l'état — la **deuxième** de cette
session. Refait par les noms, avec un témoin qui matche.)*

**§4.2 — les gardes englobantes.** Les deux adresses visées vivent dans
`FUN_180072BA0`, dont le corps entier n'a **qu'une** garde, au sommet :

```
0x180072BA6  CMP dword ptr [RCX+0x58], 0
0x180072BAD  JZ  0x180072CE9          <- saute toute la fonction
```

`0x180072BE0`, `0x180072C42` et `0x180072CC6` sont **après** elle, et le seul
autre branchement (`0x180072C45: JZ 0x180072C5C`, la texture) reconverge avant
`0x180072CC6`. Les deux adresses sont donc atteintes **exactement aussi
souvent** — et le §32 les a comptées : **4 617 passages chacune**. Il n'y a
aucun interrupteur à vérifier : cette sonde ne touche pas l'hôte REVO.

**§4.3 — un plafond de lignes ?** Les six `static long nJ = 0; if (++nJ <= 20)`
sont dans `vf5fs_host.cpp`, et **cette course n'y passe pas** : `sonde_decor.py`
pilote `vfes.exe` au débogueur, sans une ligne d'hôte. Le plafond équivalent de
cet outil est ailleurs, et il est lu en source au §38.4.

**§4.4 — le déclenchement est-il un fait du jeu ?** Oui : un point d'arrêt sur
l'instruction. Pas `image + N`. Le temps ne commande que les captures.

**§4.5 — le fait qui tranche se journalise-t-il à l'instant où il arrive ?**
Oui : si la taille est nulle, **le relevé n°1 le dit**, à la première image où
le décor se dessine. Rien n'est attendu.

**§4.6 — mes contrôles visent-ils l'état ?** Oui, et deux fois : chaque fenêtre
porte sa propre valeur témoin, **lue et non supposée** (§38.3).

### 38.2 OÙ SONT LES DEUX VALEURS, LU DANS L'ASSEMBLEUR

`FUN_180071F50` remplit le tampon. Son `param_1` est la **base**, et le dossier
est `base + 0x58` — c'est pour cela qu'elle appelle l'intégration par
`LEA RCX, [RBX+0x58]`. D'où toute la correspondance :

| dans la base | dans le dossier | ce que c'est |
|---|---|---|
| `0x180071FC0  MOV EAX, [RBX+0x90]` | `+0x38` | le nombre de particules |
| `0x180071FD7  VMOVSS XMM7, [RBX+0x94]` | **`+0x3C`** | **le facteur d'alpha** |
| `0x180071FC9  MOV RDX, [RBX+0xA0]` | `+0x48` | les particules |
| `0x180071FD0  MOV RCX, [RBX+0xA8]` | `+0x50` | les sommets |
| `0x180072060  MOV [RBX+0xB0], EAX` | `+0x58` | **le compte que le tirage lit** |

Cette dernière ligne ferme une boucle : **le remplissage écrit dans `+0x58` le
compte que le tirage relit**, et le §32 y a mesuré `r8 = 0x7D0`. Les 2 000
sommets ont donc bien été écrits.

Et la boucle de remplissage, sommet par sommet :

```
0x18007202E  VMULSS XMM0, XMM7, [RDX+0x28]   // alpha  = facteur x particule[10]
0x180072033  VMOVSS [RCX+0x18], XMM0         //        -> sommet +0x18
0x180072038  MOV    EAX, [RDX+0x24]          // taille = particule[9]
0x18007203E  MOV    [RCX+0x1C], EAX          //        -> sommet +0x1C
0x180072041  LEA    RCX, [RCX+0x20]          // pas du sommet  : 0x20
0x18007204B  LEA    RDX, [RDX+0x2C]          // pas de particule : 0x2C
```

### 38.3 LA LIGNE, ET POURQUOI CES DEUX FENÊTRES

```
py -3 "C:\Users\frede\Documents\RECOMP\Virtua Fighter 5 FS\VF5RE\tools\sonde_decor.py" 48 ^
  --secondes 160 ^
  --bp "0x180072CC6:sommet:**0x180677B10+0x50+0x18,0x180072C42:dossier:*0x180677B10+0x34" ^
  --toutes 12 --depuis 82
```

C'est **mot pour mot** la ligne du §32, aux deux offsets près (`+0x0` → `+0x18`,
`+0x1c` → `+0x34`) et aux noms près. Mêmes adresses, mêmes deux formes
d'indirection, même durée. Le risque de la course est celui d'une course déjà
courue deux fois.

`DAT_180677B10` n'est pas deviné : la note le tient de l'assembleur,
`180072B85  MOV [0x180677b10], RBX`, et le journal du §32 le **confirme par
l'arithmétique** — la sonde `texture` y lisait `0x12526AADD44` avec
`rbx = 0x12526AADD28`, soit exactement `rbx + 0x1C`.

Chaque fenêtre rend **quatre mots**, en hexa et en flottant, et chacune porte
**son propre témoin** :

| fenêtre | mot 1 | mot 2 | mot 3 | mot 4 |
|---|---|---|---|---|
| `sommet` = sommet[0]+0x18 | **l'alpha** | **la taille** | sommet[1].x *(témoin)* | sommet[1].y *(témoin)* |
| `dossier` = dossier+0x34 | compte alloué *(témoin)* | compte *(témoin)* | **le facteur d'alpha** | inconnu |

**Les témoins ne sont pas décoratifs.** Les mots 1 et 2 de `dossier` doivent
rendre `0x000007D0`, parce que le §32 a mesuré 2 000 au tirage ; s'ils ne le
rendent pas, c'est que `dossier = base + 0x58` est faux et **le facteur relevé
ne vaut rien**. Les mots 3 et 4 de `sommet` doivent retomber dans les **±1,1**
du §32 ; s'ils rendent 18,0, la fenêtre est décalée et **tout le relevé est à
rejeter**. Chaque fenêtre peut donc **échouer sur une faute réelle et réussir
sur une pose juste**, sans dépendre de l'autre.

### 38.4 LE HISTOGRAMME EST ÉCARTÉ, ET VOICI POURQUOI

`--histo` n'a **aucun plafond**, là où `--bp` s'arrête à **8 relevés**
(`if n <= 6 or n in (50, 500, 5000)`, lu en source). Il était donc tentant. Il
est écarté pour deux raisons mesurées, pas supposées :

* **son chemin xmm n'a jamais tourné.** Le seul histogramme de toute
  l'histoire du disque, `histo:masque_pose`, portait sur des registres
  **entiers** (`Rcx+Rdx+R8+R9`, valeurs brutes du genre `3314891521`). La
  branche `ctx.FltSave.XmmRegisters[...]` de `valeur()` est du code **jamais
  exécuté** — on ne mesure pas une inconnue avec une inconnue.
* **il arrondit.** `return round(f * 20) / 20` : un alpha de 0,02 y sort à
  **0,0**, indiscernable d'un vrai zéro. Or c'est précisément la question.

La forme mémoire de `--bp`, elle, rend l'**hexadécimal exact** et a déjà tourné
aux §32 et §35. Le plafond de 8 est acceptable ici, et pour une raison lue :
**la taille est statique** — le §37.4 a établi que `FUN_1800725A0` touche les
indices 0, 2, 6, 7, 8 et 10 d'une particule, **jamais le 9**. Un seul relevé
suffit donc pour elle. L'alpha, lui, décroît, et c'est pour cela que les
relevés **n°50 et n°500** comptent plus que les six premiers.

*(Et `--bp` distingue bien **trois** états, pas deux : `_lire_memoire` rend
« pointeur = 0 », « le descripteur ne porte aucun pointeur », ou « illisible »
— un refus n'est pas une absence.)*

### 38.5 LES ISSUES, NOMMÉES D'AVANCE

| ce que le journal rend | ce que ça prouve |
|---|---|
| taille = **`0x00000000`** | **LA CAUSE EST TROUVÉE** : 2 000 points de taille nulle, quadrilatères dégénérés, rien à l'écran |
| taille ≈ **`0x419…`** (18,0) | la taille arrive jusqu'au sommet : cette piste tombe |
| alpha = `0` **et** facteur = `0` | **LA CAUSE EST TROUVÉE** en amont : `dossier+0x3C` est nul, tout est multiplié par zéro |
| alpha = `0` **mais** facteur ≠ `0` | c'est `particule[10]` — la durée de vie — qui est nulle : l'intégration tue les particules à la naissance. Cause trouvée, mais ailleurs |
| alpha non nul et **minuscule** (sous `0x3C800000` ≈ 0,0156) | brume présente mais sous le seuil visible : c'est un réglage, pas une greffe manquée |
| alpha ≠ 0 **et** taille ≠ 0 aux 8 relevés | **les deux dernières cases de la chaîne sont saines.** Douze causes mortes, et plus rien de nommé du côté des données : il faudra le pixel shader, ou la cible de rendu 5 à la composition |
| mots 1-2 de `dossier` ≠ `0x7D0` | mon arithmétique est fausse : **le facteur ne vaut rien**, seule la fenêtre `sommet` compte |
| mots 3-4 de `sommet` hors ±1,1 | la fenêtre est décalée : **tout le relevé est à rejeter**, et le pas de 0x20 est à relire |
| `[mem] pointeur 0x… = 0` | **refus, pas absence** : `FUN_180072B60` n'a pas tourné à cet instant. Course à refaire plus tard dans le combat |
| `[mem] le descripteur … ne porte aucun pointeur` | `dossier+0x50` est nul : le tampon de sommets n'est pas alloué. Cause trouvée, et en amont de tout |
| aucun passage sur `sommet` | le combat n'a pas démarré sur 48 : **course perdue, pas un résultat** |

### 38.6 CE QUE FRÉDÉRIC DOIT FAIRE

* **Fermer le jeu avant** le lancement.
* **Garder la fenêtre du jeu au premier plan.** Au §32, **quatre captures sur
  sept** ont été refusées parce qu'une autre fenêtre la recouvrait.
* **Aller au combat sur le décor 48** et y rester ; la sonde s'arrête seule à
  160 s.
* Si le jeu reste muet après : `py -3 tools/muet.py --rendre`, jeu lancé.

### 38.7 CE QUE CETTE COURSE NE MESURERA PAS

* **Un seul sommet sur 2 000.** La fenêtre lit le sommet[0]. Un zéro isolé
  parmi 2 000 ne se verrait pas — mais le symptôme est une absence *totale*,
  donc le sommet[0] est représentatif. Ce n'est pas une preuve, c'est un pari
  nommé.
* **8 images sur ~4 600** (1 à 6, puis 50 et 500).
* **`--toutes 12 --depuis 82` est un déclenchement au temps**, pas un fait du
  jeu (`CLAUDE.md` §4.4). Acceptable parce que le temps ne commande que les
  **captures** ; le fait qui tranche est relevé sur un point d'arrêt.
* **Et c'est l'écran qui tranche, pas le journal.** Même si la taille et
  l'alpha sortent sains, la brume reste invisible jusqu'à ce que Frédéric la
  voie.
## 39. LA COURSE EST COURUE — ALPHA ET TAILLE SONT SAINS, ET RIEN N'A CHANGÉ

Course lancée sur le « oui, lance » du 20 novembre 2026, selon la consigne du
§38, **sans en changer une lettre**.

### 39.1 LE JOURNAL A CHANGÉ — PROUVÉ, PAS SUPPOSÉ

Copié de côté **avant toute analyse**, comme `CLAUDE.md` §3 l'exige :
`VF5RE/runtime/media/vf5fs/courses/sonde_alphataille_jn5_20261120_2110.txt`.

| | taille | empreinte SHA-256 |
|---|---|---|
| avant (le §35) | 5 756 o | `1F25476B5ADBE23F41C0CBA1A0DF993634867BB4FB609C89234D1CDA0FD4597B` |
| après | **5 200 o** | **`C7FEDBFB99328D20D8B98527EB765187A859BDE22BD25698025A9D23B55FB119`** |

Le code de sortie était 0, et **ça ne prouve rien** ; c'est l'écart d'empreinte
qui prouve. `decor demande 19 -> force a 48`, **4 409 passages** sur chacune des
deux sondes.

### 39.2 LES QUATRE TÉMOINS PASSENT — LE RELEVÉ COMPTE

Lus **avant** les valeurs, comme annoncé au §38.3 :

| témoin | attendu d'avance | rendu |
|---|---|---|
| `dossier` mot 1 (`+0x34`) | `0x7D0` | **`000007D0`** |
| `dossier` mot 2 (`+0x38`) | `0x7D0` | **`000007D0`** |
| `sommet` mot 3 (sommet[1].x) | dans les ±1,1 du §32 | 0,352 → 0,438 → **−1,029** |
| `sommet` mot 4 (sommet[1].y) | dans les ±1,1 | **0,0625** |

Donc `dossier = base + 0x58` tient, et la fenêtre n'est pas décalée. Les deux
issues « relevé à rejeter » du §38.5 sont écartées.

### 39.3 LES VALEURS — AUCUNE N'EST NULLE

```
dossier  [mem 0x1E1872BA70C] 000007D0 000007D0 3F800000 3E99999A = 2000 2000 1.0 0.3
sommet   [mem 0x1E1A9958638] 3F800000 417064C3 3EB4799E 3D800000 = 1.0 15.0246 0.352 0.0625
```

| case | valeur | aux 8 relevés |
|---|---|---|
| sommet `+0x18` — **l'alpha** | **1,0** | constant |
| sommet `+0x1C` — **la taille** | **15,0246** | **constant** |
| dossier `+0x3C` — **le facteur d'alpha** | **1,0** | constant |
| dossier `+0x34` / `+0x38` — les comptes | **2 000** | constants |

La taille constante aux huit relevés **confirme le §37.4** par la mesure :
`FUN_1800725A0` ne touche jamais l'indice 9. Et 15,02 est bien un aléa centré
sur les 18,0 de `S+0x30`, comme l'init le prescrit.

C'est **l'issue 5 du §38.5**, celle qui ne donne pas de cause.

### 39.4 L'ÉCRAN, QUI EST LE SEUL À TRANCHER

Trois captures ont abouti (t = 82, 94, 106 s), **aucune refusée** — la consigne
du §38.6 a tenu.

**Frédéric les a lues, et son relevé est : il n'y a pas de brume au PREMIER
PLAN.** Le voile visible au fond est le brouillard de **distance**, celui du
groupe 0 du §1 — pas la nappe de `FOG_RING`.

*(J'avais lu « il y a de la brume » dans la capture. C'était faux, et ce
n'était pas à moi de le lire : `CLAUDE.md` §3 dit que **Frédéric mesure
l'écran**. Consigné pour que la faute ne se refasse pas : une brume de
distance et une nappe au sol ne se distinguent pas depuis le journal, et je
n'ai pas à trancher une image.)*

### 39.5 DOUZE CAUSES MORTES, ET LE CONSTAT QUI EN SORT

| | sort |
|---|---|
| la garde fermée, l'init n'a pas tourné | mort (§32) |
| positions `NaN` ou dégénérées | mort (§32) |
| les pixels de la texture | mort (§31) |
| la cible de rendu 5 | mort (§30) |
| l'état de mélange | mort (§33) |
| le masque d'écriture de couleur | mort (§35) |
| les facteurs de mélange | mort (§35) |
| le mauvais programme | mort (§36) |
| le geometry shader manquant | mort (§36) |
| le geometry shader non conforme | mort (§37) |
| le débordement de tampon / l'indice 9 écrasé | mort (§37.4) |
| **l'alpha ou la taille à zéro** | **mort (§39) — 1,0 et 15,02** |

**Tout ce que le jeu remet à D3D11 est correct**, de l'allocation des 2 000
particules jusqu'à la dernière case du sommet. La faute est donc **en aval de
la donnée de sommet**, et plus rien de ce qui a été nommé ne tient.

### 39.6 CE QUI RESTE, ET QUI N'A JAMAIS ÉTÉ LU

Trois choses, nommées sans être mesurées. **La première est la plus forte, et
c'est la piste du §36.5 qui n'est toujours pas morte :**

1. **La VALEUR de `cb12[28]`.** Le §37 a prouvé que le geometry shader la
   **lit**, comme les trois témoins qui dessinent. Il n'a **pas** prouvé
   qu'elle **contient** quelque chose. Or toute la taille en dépend :
   `cb12[28].xy × COLOR1 × position.w × 0,5`. Si ce registre est à zéro, les
   2 000 quadrilatères sont dégénérés **malgré** une taille de 15,02 au sommet
   — exactement le symptôme. Le pont entre `FUN_18024F2D0(v)`, qui écrit son
   scalaire en `contexte+0xD9598`, et le tampon de constantes du geometry
   shader **n'a jamais été lu**, et il se lit **sans course**.
2. **L'état de profondeur.** Jamais lu. Une nappe au niveau du sol
   (`y = 0,0625 × 8 = 0,5`) est le cas où un test de profondeur la rejette
   derrière le plancher sans rien dire.
3. **`FUN_180071BC0`**, toujours pas décompilée.
## 40. LES TROIS LECTURES RESTANTES — `cb12[28]` N'EST JAMAIS LIÉ

Trois lectures menées en parallèle sur demande de Frédéric, **zéro course**,
`rea`/Ghidra sur
`VF5RE/runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll`.

### 40.1 `FUN_180071BC0` N'EST PAS L'ÉMETTEUR — TREIZIÈME CAUSE MORTE

C'est le **constructeur des sources de vent**. Elle échantillonne 5 os × 2
combattants, en déduit leur vitesse depuis l'image précédente, et reconstruit
la liste (10 au maximum, pas `0x28`, compte en `dossier+0x124`) des champs de
force que `FUN_1800725A0` consomme ensuite — producteur → consommateur.

Deux branches, lues :

* **un pied qui se pose** (os d'indice 0 passant sous `DAT_1806431B8` = 0,2) :
  rayon 2,0, direction (0, 1, 0), force 2,2 ;
* **un membre rapide** (vitesse > `DAT_180643198` = 10,0) : rayon 0,5,
  direction = la vitesse normalisée, force = `min(v, 100) × 0,01`.

**Elle ne déréférence jamais `dossier+0x48` ni `dossier+0x50`** : elle n'atteint
aucune particule et aucun sommet. Les offsets `0x1C`, `0x30`, `0x34`, `0x38`,
`0x3C`, `0x48`, `0x50`, `0x58` sont **absents de ses 911 octets**. La seule mise
à zéro de tout son corps est son propre compte de sources, qu'elle reconstruit
dans le même appel. **Elle ne peut rien annuler de ce dont l'affichage dépend.**

### 40.2 LA PROFONDEUR NE DISTINGUE PAS FOG_RING DES TÉMOINS

La clé de profondeur est **`0x8D`**, et la chaîne est établie maillon par
maillon, pas devinée :

| maillon | ce qu'il fait |
|---|---|
| `FUN_18024E900(0x8D)` | → `FUN_18024DD20(contexte+0xD8BD0, 0x8D, 1)` |
| cas `0x8D`, `0x18024DE6E` | lève le bit de saleté, écrit `[états+0x70]`, puis `objet+0x58` (clé packée) |
| `FUN_18025CEB0` | `if (sale & 0xC)` → vidange |
| `FUN_18026FB60` | dépaquette `objet+0x58` en `D3D11_DEPTH_STENCIL_DESC` exact |
| vtable `+0x120` | **indice 36 = `OMSetDepthStencilState`** |

*(J'avais annoncé l'indice 53 dans la consigne. **C'est 36** ; l'agent l'a
trouvé seul et corrigé. `OMSetBlendState` est à `+0x118` = 35 et `RSSetState`
à `+0x158` = 43, ce qui recoupe les trois bits de saleté.)*

Et le résultat, qui est un vrai résultat :

> **FOG_RING, Ripple et SnowRing font exactement la même chose sur la
> profondeur : rien.** Les trois héritent de l'état du dessin précédent.

L'absence a été cherchée par **deux voies** : les trois corps décompilés en
entier, **et** un balayage binaire de tout `mov r32, 0x8D` — 25 sites, aucun
dans `FUN_180072BA0`, `FUN_18007B4A0` ni `FUN_18007E420`. Et il n'existe pas
d'autre poseur : le bit de saleté `or qword [r],4` n'a que **6 occurrences**
dans tout le binaire, et `or qword [r],8` **zéro**.

Mieux : FOG_RING est la **mieux élevée** des trois. Elle seule enveloppe par
`FUN_180248BC0(0xFFFFFFFF)`, qui sauvegarde le bloc d'états complet, profondeur
comprise (`+0x70`, `+0x71`, `+0x72`, `+0x78`, `+0x80`), et le dépilage rejoue la
clé `0x8D`. Ripple et SnowRing ne restaurent rien : **ce sont eux qui fuient.**

**La profondeur n'est donc pas écartée, mais elle n'explique pas l'écart.** Pour
qu'elle tienne, il faudrait que l'état *hérité* diffère entre FOG_RING et les
témoins — un fait d'exécution que la lecture ne peut pas rendre.

*(L'agent nommait aussi le masque d'écriture de couleur comme « second état
hérité, non mesuré ». **Il l'est** : le §35 a lu l'octet `[[0x180C414F8]]+0x50`
à `0xFE` aux huit relevés, soit `0xF0` = quatre canaux ouverts — le même octet.
L'agent n'avait pas ce contexte.)*

### 40.3 `cb12[28]` N'EST JAMAIS LIÉ — ET C'EST LA CAUSE

**La piste du §36.5, restée ouverte depuis, est tranchée.**

**(a) Où va vraiment la taille de point.** L'immédiat `0xD9598` n'a que **deux**
occurrences dans les 15,5 Mo : l'écrivain `FUN_18024F2D0` (`0x18024F2EE`) et un
**unique** lecteur, `FUN_180251390` (`0x180251555`). Ce lecteur la range en :

```c
auVar4 = vinsertps_avx(ZEXT416(*(uint *)(contexte + 0xd9598)), ...);
*(undefined1 (*) [16])(param_1 + 0xe30) = auVar4;    // registre 1, .x
FUN_18025BEE0(uVar2, 6, 2);                          // slot 6, 2 registres
(**(code **)(... + 0x38))(..., 6, 1, ...);           // vtable 0x38
```

L'identité de la vtable est **prouvée** : dans `FUN_18025BEE0`, le même objet
est appelé en `0x70` avec `MapType = 4` (`WRITE_DISCARD`) et en `0x78` —
`Map` (14) et `Unmap` (15). Donc l'objet est l'`ID3D11DeviceContext` et
**`0x38` = indice 7 = `VSSetConstantBuffers`**.

> La taille de point atterrit dans **`b6` du nuanceur de SOMMETS, registre 1,
> composante `.x`**, soit l'octet `0x10` de son tampon. **Pas `0x1C0`, pas le
> slot 12, pas le geometry shader.**

**(b) Ce que le geometry shader reçoit réellement.** L'initialiseur
`FUN_18025FD90` enregistre toute la table des tampons avec des **immédiats
littéraux** (`0x18025FE83`–`0x18025FF6D`) :

| idx | descripteur | slot | étage | registres |
|---|---|---|---|---|
| 13 | `0x1010D` | 13 | VS | 1 |
| 29 | `0x1001021D` | 13 | PS | 1 |
| **45** | **`0x2001042D`** | **13** | **GS** | **1** |
| 6 | `0x32F0030306` | 6 | VS+PS | 3 |

Et la fonction fait, juste à côté, `MOV dword [RCX+0x420], 0` … `[RCX+0x470], 0`
— **tous les offsets prédits par le décodage, à l'octet près.**

> **Le geometry shader reçoit exactement un tampon : `b13`, UN seul registre
> float4.** Le slot 12 n'est lié à **aucun** étage — aucun descripteur ne porte
> 12 en octet 0. Et même `b13` n'a que le registre `[0]` : **le registre 28
> n'existe pas.**

`FUN_18025C190` lie bien un geometry shader réel (`0xB8` = `GSSetShader`) et ses
échantillonneurs (`0x100` = `GSSetSamplers`), mais **aucun tampon de
constantes**. Le cache des tampons GS (`device+0x1088` et son miroir `+0x1328`),
balayé en disp32 sur tout `.text`, n'est touché que par **deux** fonctions : la
vidange `FUN_18025DE00` et la remise à zéro `FUN_18025F440` — qui appelle
`GSSetConstantBuffers(0, 14, {NULL × 14})`.

**Donc `mul r1.xy, cb12[28].xyxx, v[0][0].yyyy` lit un slot non lié. Sous D3D11,
cela rend des zéros. Taille × 0 = 0 : les 2 000 quadrilatères sont dégénérés.**

C'est la seule explication trouvée qui soit **compatible avec tout le reste** :
la donnée de sommet saine, l'état sain, le bon programme, le geometry shader
présent et conforme — et rien à l'écran.

*(Le contrôle de l'agent a d'abord échoué, et il l'a dit : sa recherche de
descripteur GS ne rendait rien, **mais son témoin positif non plus**, alors que
l'instruction existe. Il avait mal sérialisé la valeur sur 6 octets au lieu de
5. Corrigé, le témoin rend 1 occurrence. **Sans ce témoin il concluait une
absence sur un échec de recherche** — exactement la faute que `CLAUDE.md` §4.1
nomme.)*

### 40.4 LA TENSION QUE CE RÉSULTAT CRÉE, ET QU'IL NE FAUT PAS ENTERRER

Le §37 a établi que **les quatre** programmes de points à geometry shader lisent
`cb12[28]` : `fog_ptcl`, `snow_particle.0`, `water_particle`, `particle.1`. Si
le slot 12 n'est lié nulle part, **tous les quatre sont dégénérés**, pas
seulement FogRing.

Or le §37 appelait ces trois-là « les témoins qui dessinent ». **Cette
affirmation n'a jamais été mesurée** — elle était une supposition de ma part.

Les deux témoins dont le dessin est réellement constaté, Ripple et SnowRing, ne
sont **pas** des programmes de points à geometry shader : SnowRing demande
`SN_FOOT` = `snow_footprint..vp`, qui est un **`GSVS`** sans geometry shader
(§36.3), et Ripple demande `RIPEMIT`, absent de la liste des cinq `GSFX`. **Ni
l'un ni l'autre ne passe par `cb12[28]`.** Il n'y a donc pas de contradiction —
mais il y a une **prédiction**, et elle se vérifie à l'écran :

> **Si `cb12[28]` est bien la cause, alors les particules de neige, les
> particules d'eau et les particules génériques sont AUSSI invisibles dans ce
> build.**

C'est Frédéric qui mesure l'écran. Tant qu'il ne l'a pas regardé, la cause
est **lue, pas prouvée**.

### 40.5 CE QUI N'EST PAS VÉRIFIÉ

* **La valeur de `cb12[28]` en marche n'a pas été mesurée.** Tout le §40.3 est
  une lecture statique. Elle est serrée — deux occurrences de l'immédiat, la
  table en immédiats littéraux, le cache GS fermé par l'autre bout — mais ce
  n'est pas une mesure.
* **La prédiction du §40.4 n'est pas regardée.**
* `FUN_180251390` lie son slot 6 directement, en doublon du descripteur idx 6
  de l'initialiseur ; lequel gagne à l'instant du tracé n'est pas déterminé.
  Cela ne change rien à la réponse sur le GS.
* Il n'est pas prouvé exhaustivement qu'aucun code ne construise un descripteur
  GS **à l'exécution** avec un slot calculé ; c'est la sonde sur `+0x1088` /
  `+0x1328` qui ferme la question, par l'autre bout.
* L'état de profondeur **hérité** reste non mesuré (§40.2).
* Les valeurs `DAT_18064319x` du §40.1 sont celles de l'image sur le disque ;
  un chargement de paramètres pourrait les réécrire.
* Piste neuve, non identifiée : `objet+0x1DC8 & 0x170000`, une capacité dont la
  branche force la profondeur à désactivée — pour tout le monde, pas seulement
  FogRing.
## 41. LE §40.3 EST FAUX — `cb12[28]` EST BIEN LIÉ AU GEOMETRY SHADER

**Écrit dans l'heure qui suit le §40, avant toute réparation.** Le §40.3
concluait que le slot 12 n'était lié à aucun étage. **C'est faux.** J'ai failli
réparer sur ce diagnostic.

### 41.1 CE QUI A DÉCLENCHÉ LA VÉRIFICATION

En cherchant quels effets utilisent les quatre programmes de points, j'ai
rouvert `VF5RE/tools/shader_empreintes.py`, dont l'en-tête du 11 septembre 2026
porte ceci :

> `cb12[28].xy` valant **(2/L, −2/H) du viewport COURANT** (`0x18025E830`,
> recalculé à chaque viewport par `0x180261840`)

et `REPRISE.md` est encore plus précis :

> écrit par `0x18025E830` (descripteur **`0x601F270C`** : emplacement **12**,
> registre **28**)

Deux notes du projet, écrites deux mois avant, disaient le contraire de
l'agent. **Un compte rendu d'agent n'est pas une preuve.**

### 41.2 LA LECTURE QUI TRANCHE, FAITE PAR MOI

`FUN_18025E830`, décompilée :

```c
lVar1 = *(longlong *)(param_1 + 0x38);
...
*(float *)(lVar1 + 0x640) = auVar2._0_4_ *  2.0 + 0.0 + ...;   // 2/L
*(float *)(lVar1 + 0x644) = auVar2._4_4_ * -2.0 + 0.0 + ...;   // -2/H
*(float *)(lVar1 + 0x648) = ... + -1.0 + ...;
*(float *)(lVar1 + 0x64c) = ... +  1.0 + ...;
*(ulonglong *)(lVar1 + 8) = *(ulonglong *)(lVar1 + 8) | 0x8000000000000;
*(undefined8 *)(lVar1 + 0x78) = 0x601f270c;
```

Quatre faits, et ils s'emboîtent :

1. **Le bit de saleté est `0x8000000000000`**, soit le bit **51**. Avec la règle
   `idx = 63 − bit` que l'agent a lui-même établie : **idx 12**.
2. **Le descripteur est écrit en `lVar1 + 0x78`**, et la table est en
   `état+0x18 + idx*8` : `0x18 + 12×8` = **`0x78`**. L'idx 12 confirmé par
   l'adresse d'écriture, indépendamment du bit.
3. **Le descripteur `0x601F270C` se décode** avec le format de l'agent :
   octet 0 = `0x0C` → **slot 12** ; masque d'étage = bits 8-13 = `0x27` =
   `VS|PS|GS|DS` — **le GS en est** ; nombre de registres = bits 16-27 =
   `0x01F` = **31**, donc les registres 0 à 30 : **le 28 existe**.
4. **L'arithmétique ferme la question toute seule.** Offset = bits 24+ =
   `0x60` ; les données sont donc en `état + 0x420 + 0x60` = **`0x480`**. Le
   registre 28 est à `0x480 + 28×16` = `0x480 + 0x1C0` = **`0x640`** —
   **exactement l'octet que cette fonction écrit.** Les quatre composantes
   `0x640/0x644/0x648/0x64C` sont `(2/L, −2/H, −1, 1)`, la transformation
   viewport → repère normalisé.

> **`cb12[28]` est lié au geometry shader, il contient le facteur d'échelle du
> viewport, et il est réécrit à chaque changement de viewport.** La chaîne de
> taille du §37 est entière.

### 41.3 POURQUOI L'AGENT S'EST TROMPÉ — ET IL L'AVAIT NOMMÉ

Il n'a lu que les **immédiats littéraux de l'initialiseur** `FUN_18025FD90`.
Un descripteur écrit **à l'exécution** par une autre fonction lui échappait par
construction. Sa propre réserve le disait :

> « Je n'ai pas non plus prouvé exhaustivement qu'aucun code ne construit un
> descripteur GS à l'exécution avec un slot calculé. »

**C'est exactement le trou, et c'est par là que le fait est passé.** Sa sonde
sur le cache `device+0x1088` ne fermait rien : elle prouvait seulement que deux
fonctions **appellent** `GSSetConstantBuffers`, pas que la table qu'elles lisent
soit vide — or la vidange `FUN_18025DE00` lit précisément la table que
`FUN_18025E830` vient de remplir.

La leçon, et elle est à moi, pas à lui : **j'ai consigné sa conclusion comme un
résultat au §40.3 au lieu de vérifier son maillon le plus fort.** Sa réserve
était écrite noir sur blanc dans son compte rendu.

### 41.4 CE QUE CELA CHANGE AU BILAN

| | sort |
|---|---|
| `cb12[28]` non lié | **MORT (§41) — il est lié, et vivant** |

Le §40.3 est **retiré** comme cause. Le §40.4, qui en tirait la prédiction que
les particules de neige, d'eau et génériques seraient aussi invisibles, **tombe
avec lui** : il n'y a plus de raison de l'attendre, et cette prédiction ne doit
pas être présentée à Frédéric comme un test.

Restent valides, et sans changement : le §40.1 (`FUN_180071BC0` n'est pas
l'émetteur) et le §40.2 (la profondeur ne distingue pas FogRing des témoins).

**Et la cause n'est donc pas trouvée.** Quatorze causes mortes, la chaîne de
taille entière de bout en bout, et toujours rien à l'écran.

### 41.5 CE QUI N'EST TOUJOURS PAS MESURÉ

* **La valeur de `cb12[28]` en marche.** Le §41.2 prouve qu'il est *écrit* et
  *lié* ; il ne prouve pas ce qu'il **vaut** à l'instant où FogRing tire. Si le
  viewport courant à ce moment n'est pas celui de l'écran, l'échelle est
  fausse. Cela se mesure, et une seule lecture suffit : les quatre flottants en
  `[état+0x640]` au point d'arrêt `0x180072CC6`.
* L'état de profondeur **hérité** (§40.2).
* `objet+0x1DC8 & 0x170000`, la capacité qui forcerait la profondeur à
  désactivée.
* Quels effets utilisent les quatre programmes de points : **pas encore
  cherché**, c'est ce que je faisais quand la contradiction est apparue.
## 42. QUI DEMANDE LES QUATRE PROGRAMMES DE POINTS — RÉSULTAT PARTIEL, ET DIT

Cherché après le §41, **sans course**. Le but initial — tester la prédiction du
§40.4 — est mort avec elle ; ce qui reste utile est de savoir s'il existe un
**autre** effet sur `FOGPTCL`, qui servirait de témoin visible.

### 42.1 LA MÉTHODE, ET SON TROU

`FUN_180175970(indice)` a **36 sites d'appel** (`xrefs`). J'ai cherché par
octets le motif `MOV ECX, imm32` **immédiatement suivi** d'un `E8`, pour les
quatre indices : `0x1B` = `W_PTCL`, `0x1C` = `SNOW_PT`, `0x2A` = `FOGPTCL`,
`0x2B` = `PARTICL`. Puis j'ai gardé les seuls sites dont l'adresse + 5 tombe
**exactement** sur un des 36 appels.

**Ce filtre était indispensable.** Sur les **17** sites `MOV ECX, 0x2A` du
binaire, **un seul** est suivi d'un appel à `FUN_180175970` : les seize autres
chargent 42 pour autre chose. Un filtre « la fonction contenante est dans la
liste des appelants » en aurait laissé passer **cinq** — `FUN_1800F0D80`,
`FUN_1800F14C0`, `FUN_1800F3060`, `FUN_180104A80` — tous faux.

### 42.2 CE QUE ÇA REND

| programme | sites trouvés | qui |
|---|---|---|
| **`FOGPTCL` (42)** | **1** | `FUN_180072BA0` — **FogRing, et personne d'autre** |
| **`W_PTCL` (27)** | **1** | `FUN_1800819B0` — le jumeau géométrique du §33.3 |
| `SNOW_PT` (28) | 0 | — |
| `PARTICL` (43) | 0 | — |

### 42.3 CE QUE ÇA NE PROUVE PAS

**Le motif ne couvre que 2 des 36 sites d'appel.** Les 34 autres chargent leur
indice autrement — par registre, par `LEA`, ou depuis la mémoire ;
`FUN_180072BA0` elle-même en donne l'exemple deux lignes plus loin avec
`LEA ECX, [RDX + -0x1]`. **Les zéros du tableau ci-dessus sont donc des échecs
de recherche, pas des absences**, et les deux « 1 » sont des minorants.

Conséquence pratique : **aucun autre effet sur `FOGPTCL` n'a été trouvé**, donc
il n'y a pas de témoin visible tout fait à comparer à FogRing. Pour en être sûr
il faudrait résoudre l'indice des 34 autres sites, ce qui n'est pas fait.
