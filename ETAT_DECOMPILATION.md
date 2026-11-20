# L'état réel de la décompilation — chiffres mesurés, pas estimés

Toutes les valeurs de ce document ont été **mesurées** le 2026-11-01 par les
scripts de `mesures/`, sur les binaires de `binaires/`. Tu peux les refaire
toi-même :

    ANALYSER_ET_MESURER.cmd            le moteur (la DLL)
    ANALYSER_ET_MESURER.cmd --exe      l'exécutable

La première exécution importe le binaire dans un projet Ghidra neuf et
l'analyse (environ deux minutes), puis compte. Les suivantes sont
instantanées.

**Tolérance.** Deux analyses Ghidra du même binaire ne donnent pas toujours
le même nombre de fonctions à l'unité près : l'écart constaté entre la base
du dépôt d'origine et celle refaite par ce dossier est de **3 fonctions sur
13 856**. Ne t'inquiète pas d'un écart de cet ordre.

---

## Résumé en une phrase

L'analyse **automatique** est complète (Ghidra reconnaît 95,7 % du code du
moteur), mais le travail **humain** couvre 4 % du moteur en C archivé et
quasiment rien de l'exécutable. Les deux bases Ghidra ne contiennent aucun
renommage à la main : le savoir est dans les fichiers `.md`, pas dans Ghidra.

---

## 1. Le moteur : `vf5fs-pxd-w64-Retail_APM3.dll`

6 965 248 octets, base `0x180000000`, `.text` = 3 426 140 octets.
C'est là que vit 95 % du jeu.

| mesure | valeur | part |
|---|---|---|
| fonctions trouvées par Ghidra | **13 856** | — |
| code reconnu comme fonction | 3 279 898 o | **95,7 % du `.text`** |
| symboles posés à la main dans la base | **0** | 0 % |
| fonctions dont le C est archivé dans `code_decompile/` | **411** (408 résolues) | 2,9 % des fonctions, **4,0 % du code** |
| fonctions touchées par une adresse citée quelque part | 3 640 | 26,3 % des fonctions, 43,3 % du code |
| idem, citées par un `.md` (le savoir rédigé) | 1 971 | 14,2 % des fonctions, 27,4 % du code |

### Le piège des 3 216 fonctions « nommées »

Ghidra annonce 3 216 fonctions portant un nom autre que `FUN_xxxxxxxx`.
**Aucune n'a été nommée par un humain.** Leur classement, mesuré par
`mesures/ClasserNoms.java` :

| catégorie | nombre | ce que c'est |
|---|---|---|
| `Unwind@…` / `Catch@…` / `switchD…` | 2 089 | blocs de gestion d'exception et tables de `switch`, découpés par Ghidra |
| bibliothèque C / C++ | 404 | `memcmp`, `wcscspn`, `__acrt_*`, `std::*` |
| autres reconnus | 705 | zlib (`inflate_fast`, `deflate_stored`, `crc32`…), MFC (`CPtrList`), WinAPI |
| conflits d'identification | 18 | `FID_conflict_*` |

Autrement dit : **renommer les fonctions du moteur dans Ghidra reste
entièrement à faire.** Un repreneur qui voudrait une base annotée partirait
de `documentation/` pour y poser les noms.

### Le dénominateur utile est bien plus petit que 13 856

`outils/couverture.py` part des gestionnaires de la machine à états du mode
console et suit le graphe d'appels **directs**. Résultat mesuré :

    fonctions du binaire                            13 661 (3 127 155 o)
    atteintes depuis les gestionnaires vivants         962 (  172 257 o)
    soit 6 % du binaire

C'est un **majorant** de ce qu'il faudrait lire pour ce mode, et un
**minorant** de la surface réelle : les appels indirects (tables virtuelles,
rappels) n'y sont pas. Ce chiffre est la bonne échelle pour juger de
l'avancement — pas les 13 856.

---

## 2. L'exécutable : `vfes.exe`

1 987 072 octets, base `0x140000000`, `.text` = 1 253 075 octets.
C'est le lanceur : il charge le moteur, et il porte le son (WASAPI).

| mesure | valeur | part |
|---|---|---|
| fonctions trouvées par Ghidra | **5 548** | — |
| code reconnu comme fonction | 1 210 778 o | — |
| entrées `RUNTIME_FUNCTION` dans `.pdata` | 4 757 | — |
| symboles posés à la main | **0** | 0 % |
| fonctions dont le C est archivé | **0** | 0 % |
| fonctions touchées par une adresse citée | **34** | 0,6 % des fonctions, 0,45 % du code |
| idem, citées par un `.md` | 27 | — |

**Il n'avait jamais été importé dans un projet Ghidra** avant ce dossier.
Ce qui existe sur lui est du patch d'octets ciblé : `outils/patch_resolution.py`
force le mode de résolution, et le son a été localisé chez lui plutôt que
dans le moteur. C'est le gisement le plus inexploré de tout le projet.

---

## 3. Les deux autres DLL de la borne

| binaire | taille | fonctions | exports | état |
|---|---|---|---|---|
| `apm.reelle.dll` | 1 269 760 o | 3 040 | **106** | pas de base Ghidra, pas de décompilation. Le travail porte sur son **interface** : les 106 exports relevés, **57 réimplémentés** dans notre greffe (`donnees/apm_creneaux.json`) |
| `apmgamepad.dll` | 71 680 o | 222 | 10 | **rien** — et il n'y a rien à y faire, voir ci-dessous |
| `apm.dll.notre_greffe` | 122 880 o | 184 | 57 | notre remplaçant, produit par `outils/gen_apm_stub.py`. **C'est notre code**, mesuré — voir ci-dessous |

Le système de borne `Apmv3System` est en C# (Unity) : **13 classes**
décompilées, dans `csharp_apm3/`.

### L'`apm.dll` du banc est NOTRE code, et c'est mesuré (2026-11-04)

Attention au nom : deux fichiers différents s'appellent `apm.dll`.

| dans le banc | ce que c'est |
|---|---|
| `apm.dll`, 122 880 o, md5 `7483e1c7785a` | **notre greffe**. Source dans le dépôt : `outils/gen_apm_stub.py` (3 450 lignes), `quest_runtime.c`, `apm_tremplins.asm`, `apm_noms.inc` |
| `apm.reelle.dll`, 1 269 760 o, md5 `149c8da5bd9e` | celle de SEGA. Jamais posée dans `banc_gog` ni `banc_revo` |

**La mesure.** On découpe le `.text` des deux en fenêtres glissantes et on
compte celles de notre greffe qui se retrouvent telles quelles chez SEGA :

```
notre .text    87 552 o        SEGA .text   564 736 o

fenêtres de 16 octets communes : 3 distinctes
   432 fois   00 00 ... 00                     remplissage d'alignement
     1 fois   8b bc 24 20 01 00 00 4c 8b ...   mov edi,[rsp+0x120] ; mov r13,[rsp+0x130]
     1 fois   la même, décalée d'un octet

plus longue suite commune : 108 octets -- QUE DES ZÉROS
```

La seule coïncidence réelle fait **17 octets** : une paire de rechargements de
registres depuis un grand cadre de pile, que n'importe quel compilateur émet.
Les fenêtres de 12 octets sont du même ordre — `66 0f 1f 84 00 …`, le NOP
multi-octets d'alignement, et `48 c7 44 24 40 00 …`, la mise à zéro d'un
emplacement de pile.

Deux faits concordants : les chaînes de compilation diffèrent — la nôtre
importe `msvcrt.dll` (MinGW), celle de SEGA `MSVCP140` et `VCRUNTIME140`
(MSVC) — et 97 % du code de notre greffe est joignable depuis ses 57 exports,
donc il n'y a pas de masse étrangère embarquée.

**Ce qui vient de SEGA, et il faut le nommer :** les 57 noms d'exports,
indispensables à la liaison ; les adresses repères que la greffe va toucher
(`ROB+0x508`, `Core_execute+0xFB`, `0x18070FB10`) ; et les chaînes de
l'interface du jeu que `quest_runtime.c` cherche en mémoire (« Create new
data », « Main Costume »). Des noms, des coordonnées et des repères — aucun
octet de leur code.

**Conséquence.** Décompiler `apm.reelle.dll` n'a plus d'objet pour un modding
sans code SEGA : elle est déjà remplacée, et sa décompilation produirait du
code dérivé — l'inverse du but. Le seul usage qui reste est de l'ouvrir
ponctuellement comme **oracle** quand la greffe répond faux : par exemple le
code 6, qui rend OUI alors que l'original rend toujours faux (voir
`documentation/_journal/A FAIRE.txt`).

### `apmgamepad.dll` ne sert à rien, et c'est mesuré (2026-11-04)

Elle n'est **jamais chargée**. Une DLL ne peut l'être que de quatre façons, et
les quatre sont écartées :

1. **table d'imports** — aucun des quatre binaires du jeu ne la cite
   (`eve.exe`, `apm.dll`, `vfes.exe`, le module) ;
2. **export-renvoi** — les dix `apmGamepad*` d'`apm.dll` sont du code propre,
   aux RVA `0x1200` à `0x1550`. Zéro renvoi ;
3. **`LoadLibrary`** et 4. **import à chargement différé** — les deux exigent
   la chaîne `apmgamepad.dll` dans le binaire appelant. Elle n'est dans
   **aucun** d'eux ; `apm.dll` ne porte que les dix *noms de fonctions*, qui
   sont ses propres exports.

**Vérification par l'expérience**, la seule qui couvre aussi l'injecteur de
TeknoParrot : Frédéric a renommé le fichier dans son installation
`E:\Jeux vidéo\Jeux\Arcade\TeknoParrot\virtua fighter esport\runtime\media\`
et **le pad a continué de fonctionner**.

Pourquoi elle existe quand même : son chemin de PDB,
`src\lib\apmgamepad\amx_vc141\x64\Release`, montre que c'est une
**bibliothèque** de la chaîne de compilation de la borne (Visual Studio 2017).
Elle est liée statiquement dans `apm.dll` *et* livrée à part. Le même code, en
double.

**Conséquence appliquée :** `monter_banc.cmd`, `monter_banc_gog.cmd` et
`monter_banc_revo.cmd` ne la posent plus. Elle reste dans `SOURCES\lib` et
`binaires\`. Le commentaire de `monter_banc.cmd` qui justifiait sa pose —
« sinon le chargeur pourrait trouver la VRAIE `apm.dll` avant la nôtre » —
était un non-sens : poser *apmgamepad* ne protégeait rien contre *apm.dll*.
Ce qui protège le relais, c'est que notre `apm.dll` est **dans** le banc, et
que le dossier du programme passe avant le `PATH`.

---

## 4. Les binaires de référence (pas APM3, mais indispensables)

Le mode Quest est porté **depuis** la version Xbox 360 de 2007. Ces bases ne
sont pas dans ce dossier (ce sont d'autres images, d'autres consoles), mais
leur C décompilé y est, dans `code_decompile/` :

| binaire | fonctions | renommées à la main | ce qu'on en a tiré |
|---|---|---|---|
| VF5 Xbox 360 2007 (`vf5_x360.img`) | 18 250 | 32 | **619 fonctions PowerPC décompilées** : c'est la source du mode Quest |
| VF5 FS console X360 (`default.img`) | 20 078 | 36 | idem, pour comparer FS console et FS arcade |
| VF5R Lindbergh | 27 371 | 0 | 26 fonctions, pour les généalogies |
| VF5 « ver. B » Lindbergh | 22 965 | 0 | idem |

Les adresses PowerPC se reconnaissent à leur préfixe `0x82…`.

---

## 5. Comment lire les chiffres de couverture

Trois mesures différentes, dans l'ordre croissant de solidité :

1. **« touchée par une adresse citée »** — borne haute. Une adresse apparue
   dans un journal de sonde suffit. Dit *ce qu'on a regardé*.
2. **« citée par un `.md` »** — dit *ce qu'on a expliqué par écrit*.
3. **« C archivé »** — dit *ce qu'on a vraiment lu ligne par ligne*. C'est la
   seule des trois qui ne se gonfle pas toute seule.

Pour le moteur : 26 % / 14 % / 4 %. Garde le 4 % en tête.

---

## 6. Refaire une mesure, ou en ajouter une

- `mesures/CompterVF5.java` — le dénombrement (fonctions, sources de noms,
  commentaires, types).
- `mesures/ClasserNoms.java` — le classement des noms, qui démonte l'illusion
  des « 3 216 fonctions nommées ».
- `mesures/extraire_adresses.py` — balaye tout le dossier et sort les adresses
  de `.text` citées, en deux groupes : TOUT et DOCS (les `.md` seuls).
- `mesures/CouvVF5.java` — résout ces adresses en fonctions et somme les
  tailles.
- `mesures/DecompVF5.java` — décompile par adresse ; utilisé par
  `DECOMPILER.cmd`.
- `outils/couverture.py` — la surface par graphe d'appels, autonome
  (capstone + pefile, sans Ghidra).

Les deux scripts Java cherchent l'adresse **dans** sa fonction, pas à son
début : on cite d'ordinaire une instruction, pas une entrée.
