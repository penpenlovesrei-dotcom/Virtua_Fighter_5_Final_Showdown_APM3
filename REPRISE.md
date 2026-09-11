# REPRISE — état du chantier VF5

**Ce fichier fait foi sur l'état courant.** Dernière mise à jour : 2026-09-02
(sessions « section 1 de mothead », « exécution instrumentée », « le combat tourne »,
puis « les deux verrous »).

Projet : rétro-ingénierie de la famille Virtua Fighter 5, cible principale
**Final Showdown arcade**. Espace de travail : `C:\Users\frede\Desktop\VF5RE\`.

---

## 1. Règles du chantier

- **Les dumps sont en lecture seule.** Rien n'est jamais écrit dans
  `C:\Users\frede\Desktop\VF5 FS DECOMP\` ni dans le dossier Steam. Toute extraction va dans
  `VF5RE\extracted\`.
- **Niveaux de confiance obligatoires** sur chaque conclusion :
  `UNKNOWN` / `SPECULATIVE` / `LIKELY` / `SUPPORTED` / `CONFIRMED`.
  Ne jamais promouvoir une hypothèse en fait sans preuve.
- **Ne pas mélanger les versions.** Toute affirmation précise de quelle source elle vient.
- Sur cette machine, **`python` est un stub inerte du Microsoft Store** : il se lance, ne
  produit rien, et ne signale aucune erreur. Toujours écrire **`py -3`**.
- Pour afficher du japonais depuis un script : `PYTHONIOENCODING=utf-8`.
- Les scripts n'écrivent que dans `VF5RE\`.
- **Copie de travail exécutable** : `VF5RE\runtime\media\` contient de quoi lancer
  `vfes.exe` sans toucher au dump — les petits fichiers sont copiés, `vf5fs_data.par` est un
  **lien dur** et `vf5fs_media` une **jonction** vers `APM3_US`. Rien n'y est écrit.

---

## 2. Les six sources, et deux étiquettes trompeuses

| ID | Ce que c'est réellement | Chemin |
|---|---|---|
| `LIND_FS` | VF5FS **Rev A**, release 2.000, 2010-06-28, Lindbergh | `Desktop\VF5 FS DECOMP\LIND_FS\vf5fs.7z` |
| `APM3_FS` | VF5FS **Rev B ver 6.0000**, release 6.000, 2011-10-17, **Lindbergh** | `Desktop\VF5 FS DECOMP\APM3_FS\` |
| `PS3_FS` | VF5FS PS3 `NPEB00913` v01.00 (EU) | `Desktop\VF5 FS DECOMP\PS3_FS\*.pkg` |
| `X360_FS` | VF5FS X360 `584111FE` + TU1 | `Desktop\VF5 FS DECOMP\X360_FS\*.rar` |
| `APM3_US` | ALLS/APM3 **Windows x64** — deux jeux : VF5 eSports + Ultimate Showdown | `Desktop\VF5 FS DECOMP\APM3_US\` |
| `PC_REVO` | R.E.V.O. World Stage 1.0.0.0 | `Program Files (x86)\Steam\steamapps\common\VFREVO\` |

**Deux pièges à ne pas refaire :**

1. **`APM3_FS` n'est pas un dump APM3 — c'est du Lindbergh** (partition `/home/disk1`).
   ELF32 x86, `libsegaapi.so`, GLUT/GLX, toolchain MontaVista, `tools/lindbergh/`.
2. **`APM3_US` contient deux jeux distincts** : `eve.exe` (moteur Dragon) et
   `vf5fs/vfes.exe` (moteur FS porté).

Identification des révisions arcade : double signal concordant — bloc de version interne du
binaire, et CRC32 du loader calculé sur `fichier[0x0A…0x400A]`
(`0xBAE2BE62` = Rev A, `0x034C0D02` = Rev B 6.0000). Détail dans `analysis/VERSIONS.md`.

---

## 3. Le résultat structurant du projet

**Ultimate Showdown et R.E.V.O. embarquent le moteur VF5FS d'origine**, pas une
réimplémentation. Leurs DLL `vf5fs-pxd-w64-*` portent un bloc de version **identique** :

```
D:/Project/vf5/vf5fscs_source/20120711_update_1.1/vf5fs
2016-06-30T14:58:25+09:00   portage        atsu_takashi
2012-07-04T18:06:57+09:00   snapshot source
Virtua Fighter5 Final Showdown / 6.000 / VERSION A / REVISION 1
```

Conséquences pratiques :

- `vf5fs-pxd-w64-d3d12_SteamRetail.dll` (7,2 Mo, x64, **14 178 fonctions bornées par
  `.pdata`**) est **la pierre de Rosette** : même code que l'ELF de 2011, bien plus lisible.
  **Commencer par lui, toujours.**
- 20 `mothead_*.bin` sur 21 et 19 `ctrl_*.bin` sur 20 de l'arcade 6.000 sont **identiques au
  SHA-256** dans R.E.V.O. (2025). Seul Dural diffère, et sur ce point R.E.V.O. suit la PS3.
- R.E.V.O. livre **deux jeux de données** : `rom/` (Final Showdown d'origine) et `rom_200/`
  (rééquilibrage 2.00), et bascule de l'un à l'autre **par un booléen à l'exécution**.

---

## 4. Formats décodés

### `FARC` — CONFIRMED, `docs/formats/farc.md`, `tools/farc.py`

Conteneur de toutes les données du jeu, de 2010 à 2025. Gros-boutiste.
Trois modes de stockage, dont un piège : dans une archive `FArC`, une entrée dont
**`usize == 0`** est stockée en clair (et non pas quand les deux tailles sont égales).
Les entrées compressées sont du **gzip**, pas du deflate brut.

Validé : `mothead_AKI.bin` extrait de `resident.farc` est identique au SHA-256 au fichier
libre de `rom_200/rob/`.

### `mot_db.bin` + `rob_mot_tbl.bin` — CONFIRMED, `docs/formats/mot_tables.md`, `tools/motdb.py`

- `mot_db.bin` : 45 jeux d'animation, **11 026 animations nommées, zéro doublon**, 149 os.
- `rob_mot_tbl.bin` est une **archive FARC** contenant `rob_cmn_mottbl.bin` et `yarare.bin`.
- `rob_cmn_mottbl.bin` : 21 entrées = 21 personnages, chacune avec N postures ; chaque bloc
  est un tableau de **363 rôles logiques → identifiant d'animation**.
  Postures : **LEI 7, SHU 6, KAG 3, VAN 3, SAR 2, LAU 2, DUR 2**, tous les autres 1.
- Lexique moteur tiré des noms : `KAMAE` garde, `GU` guard, `TA`/`SY` les deux appuis,
  `ST`/`EN` début/fin, `YA` yarare (encaissement), `KABE` mur, `DMY` doublure.

**Tout identifiant d'animation croisé ailleurs peut désormais être nommé.**

### `mothead_<CHR>.bin` — structure entière décodée, `docs/formats/mothead.md`, `tools/mothead.py`

En-tête de fichier et bloc `CCD` **CONFIRMED**. La **section 1** — les mouvements — est
maintenant décodée elle aussi, et vérifiée à la fois sur les données et sur le code du moteur.

```
section 1 = en-tete 32 o + enregistrements + table de recherche
  en-tete  : index du jeu d'animation, id_min, id_max, offset de la table
  table    : (id_max - id_min + 1) u32, bourree a 32 o
             table[id - id_min] = offset de l'enregistrement (0 = absent)
  enregis. : 32 o -> six mots de drapeaux + trois offsets de liste
             liste 1 : (code, charge)          entrees de 8 o
             liste 2 : (code, trame, charge)   entrees de 12 o, trames croissantes
             liste 3 : tableau d'offsets, charges de 16 o
```

Ce n'est pas un tableau d'enregistrements fixes : c'est un **pool à charges utiles partagées**,
adressé par une table indexée sur l'identifiant d'animation. Tous les offsets stockés sont
relatifs à la base de la section 1 ; le chargeur les relocalise en offsets relatifs au champ
porteur.

Conformité : **84 fichiers, 36 135 enregistrements, 100 % sur tous les contrôles**
(offsets de liste, décroissance des charges, croissance des trames). Les 21 fichiers de
l'arcade 6.000 donnent **le résultat décisif** : chacune des 9 140 entrées non nulles de la
table tombe sur un identifiant qui existe dans `mot_db.bin` **et appartient au jeu du
personnage** — 9 140 sur 9 140.

Le code le confirme : `0x180164400` fait exactement `table[id - id_min]`, et `0x1801633C0`
répartit la liste 1 sur une table de **84 gestionnaires** en `0x1804210D0` — même borne que le
code maximal observé dans les données (83).

**Les 84 gestionnaires de la table `0x1804210D0` ont été lus** (81 distincts,
`analysis/disasm_mothead_handlers.txt`). Un code = un champ, ou un groupe de champs, de
l'état de mouvement (`ROB+0x798`) ; les offsets croissent avec le numéro de code. 33 des 84
codes ne sont jamais employés dans les données.

Sens établis, avec leur niveau de confiance :

- **code 3 = l'attaque** (841/986 des `KI`, 730/890 des `PU`), dix sous-champs dont
  **les dégâts** (0–100, mis à l'échelle par `0x180177CF0` = ×(1+mod/125), nuls sur toutes
  les animations `_MISS`), **le niveau** (1 haut / 2 milieu / 3 bas), **un angle binaire
  16 bits** nié en miroir, **un code directionnel** remappé par une table gauche/droite de
  63 entrées, et **l'indice de réaction dans `yarare.bin`** — 3 363/3 363 dans [0, 106], la
  borne du code étant 107 pour 108 enregistrements. CONFIRMED.
- **codes 6 à 42 = une table de 32 fenêtres temporelles** de 12 octets à `état+0x154`, six
  codes en écrivant trois ou six d'un coup. Structure CONFIRMED, rôle de chaque fenêtre
  UNKNOWN.
- **code 45 = la prise** (identifiant du partenaire + dégâts + repères de trame),
  **code 46 = le même, côté victime**. **code 0 = un tirage aléatoire pondéré** (poses
  d'intro de round, gardes). **code 54 = l'orientation**, **code 60 = un drapeau *sabaki***,
  **code 73 = un masque de parties du corps** appliqué au bloc *yarare*.
- Liste 2 : **codes 5, 6, 30, 31 = jalons de trame purs** ; **code 18 = bifurcation datée**
  vers une autre animation ; **code 32 = esquive latérale** ; **codes 14 et 27 = les
  mouvements de boisson de Shun** ; **codes 17, 30, 31 = collision murale**.

**L'état de mouvement est incorporé dans `ROB` à l'offset `0x798`** — `0x180178A50`, seul
appelant de `MothApplyRecord`, commence par `lea rdi,[rcx+0x798]`. Vingt fonctions du DLL
calculent ce pointeur ; plusieurs consommateurs en sont sortis :

- **`0x1801423B0`** applique le coup : il lit `état+0x8E` (les dégâts), ou `état+0x90` quand
  la victime porte l'un des bits 10, 11 ou 23 de `ROB+0x7B4`, passe la valeur à
  `0x1801788D0` qui l'écrit chez la victime, et calcule une secousse proportionnelle à la
  racine carrée des dégâts. **Les dégâts passent de SUPPORTED à CONFIRMED**, et le code 50
  est nommé : c'est la valeur de rechange.
- **`0x180133010`** fait un `switch` à six modes sur `état+0x54`, le champ que le code 0
  écrit ; toutes les branches appellent `0x180178A50`. **Ce que le code 0 tire au sort est la
  transition de fin d'animation**, et ses six champs sont nommés (mode, deux identifiants,
  deux options, un seuil d'attente, un poids).
- **`0x180166240`** referme la boucle : les modes 2, 3 et 5 résolvent un **numéro de rôle**
  sur `rob_cmn_mottbl.bin` — même global, mêmes bornes 21 et 363 que
  `docs/formats/mot_tables.md`. `mothead` → rôle → table des rôles → identifiant →
  `0x180178A50` → enregistrement `mothead` suivant.
- **`0x180163170`** et **`0x180162B90`** remettent l'état à zéro et donnent les **valeurs par
  défaut** de chaque champ ; la seconde initialise les 32 fenêtres à `(0.0, -1.0, -1.0)`, ce
  qui **établit l'ordre de leurs trois champs**.

Une fois l'adresse de l'état connue, chercher **qui lit** le champ que chaque gestionnaire
écrit a débloqué sept codes de plus (relevé complet dans
`analysis/mothead_state_readers.csv`, 1 274 accès sur 210 offsets) :

- **codes 52 et 53** = deux **masques de 64 bits**, l'un porté par l'attaquant, l'autre par la
  cible ; `0x18013FF80` les croise et teste chez la cible le bit que la table `0x18063D060`
  associe au **niveau d'attaque**. Cette table ne rend que quatre bits pour quinze niveaux, et
  le regroupement retrouve exactement la partition haut / milieu / bas obtenue par les noms :
  **le niveau d'attaque passe de SUPPORTED à CONFIRMED**.
- **code 59** = un **décalage d'angle**, ajouté par `0x1801651D0` à la fois à l'angle du coup
  (`état+0x98`) et à l'orientation (`état+0x374`).
- **code 4** = deux coefficients flottants (défauts 1.2 et 1.0) ; **code 72** = un vecteur 3D
  soustrait à une position ; **code 69** = un masque de bits ; **code 82** = deux `u16`
  additifs.

Les dix codes `UNKNOWN` qui écrivaient encore un champ ont été repris de la même façon, et
sept se sont laissés qualifier :

- **codes 55 et 83** = deux nouveaux **identifiants d'animation**. Le 55 relie une animation
  de chancellement à sa sortie (`CMN_K_LFLG_YORO` → `CMN_K_LFLG_KAI`, 40/40 valides) ; le 83
  désigne l'**animation de référence d'un groupe directionnel** (`X_B`, `X_L`, `X_R`, `X_F`
  pointent tous vers `X_F`, 36/36 valides), `-1` signifiant « garder l'animation courante ».
- **code 68** = un **troisième masque de 64 bits** de la famille des codes 52 et 53, lu par
  `0x1801405D0` avec exactement le même motif, suivi de sept paramètres dont un pourcentage
  de défaut 100 et un coefficient de défaut 1.0.
- **code 70** = retranche 1 à 3 du compteur `ROB+0x588` (`0x180177C20`, valeur niée).
- **code 66** = une valeur qui **écrase un défaut** pris en `ROB+0x4E6`.
- **code 51** = des **paramètres de trajectoire**, relus en flottants par `0x18014FAD0`.
- **code 81** = une **requête de caméra** : le gestionnaire saute dans `0x180141CA0`, qui
  dépose les six champs dans le singleton `0x1806B84C0` et pose son drapeau ; le module
  propriétaire porte la chaîne `NAGE_VF4`.

Enfin, les trois entrées nulles de la table de répartition (**codes 43, 44 et 71**)
s'expliquent : **il n'existe pas de second répartiteur**. Ces codes sont réclamés à la demande,
soit par une boucle écrite en ligne dans la fonction consommatrice, soit par
**`0x180164720`** — qui n'est pas, comme d'abord lu, un chercheur de liste 2, mais un
**chercheur générique des deux listes** (son 2ᵉ argument choisit le pas, 8 ou 12) qui **rend la
charge utile et non l'entrée**. Ses 38 sites d'appel passent le code en immédiat : 0, 1, 2, 3,
18, 43, 45, 46, 47, 51, 55, 68 et 71.

- **code 43** = l'angle et l'ampleur de la projection : `0x180143490` en lit un `u16` dont les
  13 valeurs sont **toutes multiples de 256** (des angles binaires) et un `f32` d'amplitude, à
  côté de `ROB+0x434` que `RobApplyHit` remplit avec la racine carrée des dégâts ; à défaut il
  retombe sur les champs des codes 82 et 83. `FUTTOBI` 27/34, `KIRIMOMI` 10/14.
- **code 44** = un coefficient du même domaine (`f32` −1.0 ou 0.5 à 0.9, plus des bits).
- **code 71** = un marqueur : deux consommateurs, dont un qui incrémente deux compteurs de
  `ROB`. Sa charge vaut 0 dans les 649 emplois, donc rien de plus n'est déductible.

La **liste 2** a été reprise de la même façon. Elle n'a pas non plus de table de répartition :
`analysis/mothead_list2_consumers.csv` relève **69 sites** couvrant 17 codes, dont 10 des 32
qui étaient `UNKNOWN`. Faute de consommateur pour la majorité, **le format de la charge des
44 codes a été typé sur les données** et figure désormais dans `mothead_opcodes.csv`.

- **code 26 = le numéro de posture** : `0x180178FC0` l'écrit dans `ROB+0x554`, l'argument que
  `0x180147680` passe à `GetMotionForRole`. Preuve sur les données : les **474 valeurs sont
  exactement dans `[0, nposture−1]`** du personnage tel que `rob_cmn_mottbl.bin` le donne —
  LEI 0–6 (7 postures), SHU 0–5 (6), KAG et VAN 0–2 (3), DUR/LAU/SAR 0–1 (2), les autres 0.
  Sans exception. **CONFIRMED**, et troisième point de jonction entre `mothead` et
  `rob_cmn_mottbl`.
- **code 2 = l'angle de rotation daté** : ses 114 valeurs sont des angles binaires 16 bits
  (0xC000, 0x4000, 0x8000…), `TURN` 601/606 — le pendant animé du code 54 de la liste 1.
- **code 4 = un sélecteur temporel** : `0x180146E30` compare le champ trame de chaque entrée à
  la trame courante, ce qui confirme aussi ce champ côté code. **code 7** = un angle plus deux
  flottants, `UK` (*ukemi*) 21/22.
- Régularités notables sans consommateur : les **codes 21, 22, 24 et 52 n'apparaissent qu'à la
  trame 0** (propriétés statiques rangées dans la liste datée) ; les codes 15 et 16 n'utilisent
  que leur `u16` haut (1, 2 ou 3) ; le code 33 porte un `1.0f` dans 2 848 cas sur 2 900.

**Les codes 0 et 9 de la liste 2 n'ont pas de consommateur dans le DLL**, et cinq voies ont
été épuisées pour les chercher (détail en §3.11 de la doc) : `MothFindPayload` avec code en
immédiat — les 38 sites sont tous résolus et aucun ne les demande ; l'idiome exact de recherche
en ligne, **y compris la variante `test r,r` qu'exigerait le code 0**, qui ne rend que sept
codes ; les lecteurs du pointeur de liste 2 rangé en `état+0x518`, tous des sérialiseurs ; un
parcours complet avec table de saut, qui **n'existe pas** (aucun saut indirect sur un pas de
12 dans tout le DLL) ; et les fonctions du module `mothead` lues une à une. Or ces deux codes
sont **vivants dans les quatre jeux de données**, y compris le rééquilibrage 2.00 de 2025 où
leur nombre change encore. Trancher demande une exécution instrumentée.

La recherche a livré un résultat de côté : **`0x18017382C` est le consommateur du tableau du
code 65** (liste 1). Il fait `lea rdx,[rbx+0xB68]` — soit `0x798 + 0x3D0` — balaie les dix
cases, saute les libres et répartit sur le type en `+0x08` par une table de six cas ; les
données confirment la borne, ce champ ne valant que 0, 1 ou 5. Le code 65 devient **une
condition de branchement parmi dix**.

**Verdict sur la liste 2, obtenu en renversant la question** — au lieu de chercher chaque
code, énumérer les fonctions qui accèdent à la liste. Toute lecture passe par le champ `+0x18`
de l'enregistrement, obtenu par `MothGetRecord` : **exactement douze fonctions** le font, et
entre elles **elles ne cherchent que sept codes : 3, 4, 6, 11, 18, 26 et 34**. De plus,
`MothFindPayload` **n'est jamais appelé en mode liste 2** (ses 38 sites passent tous `edx=0`),
et il n'existe aucun répartiteur par table de saut sur un pas de 12 dans tout le DLL.

**Les 37 autres codes — 93 141 entrées sur 119 173, soit 78 % de la liste 2 — ne sont jamais
consultés par leur code.** Ils sont marqués comme tels dans `mothead_opcodes.csv`. Ce qui est
établi : aucune recherche par code n'existe pour eux, les trois voies d'accès ayant été
énumérées exhaustivement (SUPPORTED). Ce qui ne l'est pas : qu'ils soient inertes — une
consommation qui ne compare pas le code y échapperait.

Pour le modding, la conséquence est directe : **seuls les codes 3, 4, 6, 11, 18, 26 et 34 de
la liste 2 ont un effet démontrable** sur ce build.

**45 codes de liste 1 sur 51 employés et 16 de liste 2 sur 44 sont qualifiés.** Restent six
`UNKNOWN` en liste 1 (61, 62, 67 sans champ d'état ; 74, 75, 80 typés mais sans lecteur). Les
deux verrous durs — **le rôle des 32 fenêtres** et **les 37 codes de liste 2 jamais cherchés**
— relèvent désormais d'une **exécution instrumentée**, pas d'une recherche statique.

### Exécution instrumentée — `analysis/INSTRUMENTATION.md`

**Le moteur peut servir d'oracle hors du jeu.** `vf5fs-pxd-w64-Retail_APM3.dll` (build
Ultimate Showdown du dump `APM3_US`) n'a **que des imports système** : elle se charge dans un
processus Python ordinaire, sans jeu, sans démon, sans matériel. On y appelle ses fonctions sur
de vraies données et on fait arbitrer le décodage par le code d'origine.

Trois décodages sont ainsi passés de « lu dans le désassemblage » à **vérifié dynamiquement** :

- **la formule de dégâts** : `ScaleDamageByPower` appelée sur 72 couples (dégâts, modificateur),
  **72/72** concordent avec `v*(mod+125)*8/1000` ;
- **`rob_cmn_mottbl.bin` de bout en bout** : un fichier relocalisé installé dans le global du
  moteur, puis `GetMotionForRole(perso, posture, rôle)` appelé sur toutes les combinaisons —
  **14 157 valeurs sur 14 157** identiques à `tools/motdb.py`. Cela valide aussi la **règle de
  relocation** (`valeur stockée = offset absolu − position du champ`) et met au jour un piège :
  deux entrées peuvent **partager** la même table de postures, qu'il ne faut donc relocaliser
  qu'une fois ;
- **les 84 gestionnaires de codes de `mothead`** : `tools/oracle_handlers.py` fabrique un faux
  combattant à zéro, appelle chaque gestionnaire avec une charge marquée et relève les champs
  écrits, chaque code dans un sous-processus. **77 des 81 gestionnaires ont été exécutés et
  tous écrivent où la lecture statique le prévoyait.** Les quatre qui n'écrivent rien sont
  gardés par un bit de drapeau nul dans un état vierge ; les quatre plantages déréférencent des
  globaux que le faux `ROB` laisse nuls. Le répartiteur APM3 (`0x180158B51`, table
  `0x1803F95B0`) a **84 entrées avec des trous aux mêmes codes 43, 44 et 71** : la numérotation
  est identique sur les deux builds.

**Découverte au passage : l'état de mouvement n'a pas la même disposition dans les deux
builds.** Le portage a remplacé deux `std::vector` par des tableaux de taille fixe — le
conteneur du code 47 en `état+0x310` (24 o → 40 o) et celui du code 65 en `état+0x3B8`
(24 o → 120 o, et il rangeait le *pointeur* de charge là où le build 2025 copie 12 octets).
D'où deux paliers d'écart, `0x18` puis `0x78`. **Les offsets d'état de `mothead.md` valent donc
pour le build R.E.V.O.** ; pour la famille arcade, retrancher `0x18` à partir de `état+0x310`
et `0x78` à partir de `état+0x3D0`.

**Le jeu démarre.** R.E.V.O. est protégé (`start_protected_game.exe`) : ce n'est pas une cible
de débogage, et l'y attacher ferait courir un risque au compte Steam. `vfes.exe` du dump, lui,
se laisse déboguer. Il mourait sur une exception C++ non gérée **`amdaemon::Exception`** — le
démon ALL.Net des bornes SEGA — mais il ne parle pas au démon directement : il passe par
`apm.dll`, dont il importe **57 fonctions**.

**`tools/gen_apm_stub.py` génère et compile un `apm.dll` de substitution** qui répond « borne
saine, partie gratuite » (`Credit_isFreePlay` vrai, `AllnetAuth_isGood` vrai, `Sequence_isTest`
faux, pas de lecteur Aime…) et annonce chaque appel par `OutputDebugStringA`, que le débogueur
journalise. Résultat : plus d'exception, le processus passe de 11,8 Mo bloqués à **577 Mo,
57 threads**, et ouvre une fenêtre **1920×1080** intitulée `Virtua Fighter 5 FS (PXD/64bit)`
qui affiche **l'écran-titre** (`analysis/vfes_ecran_titre.png`). Sur 18 s : 12 666 appels au
stub, 22 fonctions distinctes, aucun plantage.

Deux détails à ne pas redécouvrir : `apm.dll` doit être **à côté** de l'exécutable (dans le
dump il est un niveau au-dessus), et le `gcc` de MSYS2 n'est utilisable que si
`C:\msys64\mingw64\bin` est dans le `PATH`. La vraie `apm.dll` est conservée sous
`apm.reelle.dll` dans la copie de travail.

**Ce que cela ouvre** : `Input_isOn` est appelé 4 680 fois en 18 s — **c'est le stub qui tient
les boutons**. En lui faisant rendre « départ appuyé » au bon moment, on peut mener le jeu
jusqu'à un combat sans toucher au clavier, et poser enfin des points d'arrêt matériels en
lecture sur `état+0x154` pour trancher la question des 32 fenêtres.

### Le combat tourne, et les fenêtres ont parlé — `analysis/fenetres_temporelles.md`

**`vfes.exe` va tout seul jusqu'à `ROUND 1`.** Le stub `apm.dll` tient la manette :
`Input_isOn` et `Input_isOnNow` prennent **un seul argument, le code du bouton**, et le stub
joue un scénario lu dans `apm_entrees.txt`, **relu à chaud** — on règle une séquence pendant
que le jeu tourne, sans recompiler. **Le code 7 est START** (CONFIRMED, à l'écran) : deux
appuis mènent d'un démarrage à froid au combat. Le sens des douze autres codes reste UNKNOWN.
Format et relevé complet : `docs/formats/apm_input.md`.

**Le premier verrou dur est ouvert.** Il tenait à une erreur d'adresse : dans le build APM3,
**l'état de mouvement est à `ROB+0x8A0`**, pas à `ROB+0x798` comme dans R.E.V.O. — écart
constant `0x108`, `ctx[1]` passant de `ROB+0x338` à `ROB+0x440`. Lu dans `MothApplyRecord`
(APM3 **`0x180158B40`**, unique appelant `0x18015A350`) et vérifié à l'exécution. Or les
consommateurs des fenêtres tiennent le **ROB** et les adressent en ROB-relatif (`[rdi+0x9F8]`)
— d'où la stérilité des recherches précédentes.

Une fois la base corrigée, une seule passe rend **115 accès flottants, 15 fonctions, les 32 fenêtres
touchées** (`analysis/mothead_fenetres_sites.csv`). Le premier relevé annonçait 547 accès sur
101 fonctions : il comptait des accès sur `rip` et sur la pile, et tous les objets qui ont par
hasard un champ au même déplacement. Un champ de fenêtre est un flottant ; en l'exigeant, il
reste quatre balayeuses (copieurs, réinitialiseurs) et **onze fonctions spécifiques**, où se
trouve le sens. Acquis complémentaires : **les fenêtres sont datées en trames**, en flottants ; la fin
d'une fenêtre est **bornée à la durée de l'animation** (`état+0x004 − 1.0f`) ; une valeur
négative dans la charge signifie « garder la valeur courante » ; et `0x18013329F` montre à quoi
sert une fenêtre — une **borne de trame choisie par des drapeaux**, rangée dans `état+0x074`.

**Et une fenêtre, finalement, n'est pas nommée : elle est choisie.** Deux fonctions jumelles,
`0x18013329F` et `0x1801345F9`, sont des **sélecteurs** : un arbre de tests à deux étages sur
les mots de drapeaux du combattant désigne un **groupe**, trois bits de modificateur
(`dl & 0x40`, `al & 0x10`, `dl & 2`) désignent la variante, et la fenêtre qui en résulte fournit
ses bornes. La première rend le **champ +4**, la seconde le **champ +8**, dans le même ordre de
fenêtres. Deux autres fonctions, `0x180133EA0` et `0x1801394F0`, reprennent chacune **un groupe
de cet arbre** et lisent le **champ +0**, comparé à la trame courante.

| champ | qui le lit | ce qu'il est |
|---|---|---|
| +0 | les consommateurs de groupe | **le début** de la fenêtre |
| +4 | `0x18013329F` ; borné à `état+0x004 − 1.0f` par le poseur | **la borne haute** |
| +8 | `0x1801345F9`, même arbre | une **troisième borne** |

Cinq fenêtres — **2, 10, 15, 20 et 27** — ne sont sélectionnées nulle part et n'ont aucun
lecteur scalaire : elles occupent les cases que l'arbre laisse vides.

**Et l'arbre teste le masque de commande du combattant.** `0x18013329F` et `0x1801345F9` ne
sont que des fragments ; les vraies entrées sont `0x180133280` et `0x1801345E0`, toutes deux
`f(rcx = ROB)`, et toutes deux commencent par `mov ebx, [rcx+0x518] ; test ebx,ebx ; je`. Or
`ROB+0x518` reçoit **la même valeur que `ROB+0x508`** — les fonctions qui les écrivent le font
par paire, à l'instruction suivante — et `ROB+0x508` est le masque d'entrée, **mesuré** à
l'exécution.

**Une fenêtre temporelle est donc un créneau d'entrée** : la commande en cours désigne un
groupe, trois bits de modificateur désignent la variante, et la fenêtre dit entre quelles
trames cette commande est recevable dans l'animation. C'est ce qu'un jeu de combat appelle une
fenêtre de *cancel*, d'enchaînement ou de *sabaki*. `SUPPORTED` — la chaîne est complète, mais
l'attribution nominale de chaque bit du masque reste ouverte.

**Et l'on sait désormais quel code pose quelle fenêtre.** Le même filtre strict appliqué aux 84
gestionnaires de la liste 1 rend la correspondance entière : **32 codes pour 32 fenêtres, un
pour un** — 6→0, 7→1, 8→2, 9→3, 10→4, 12→5, 13→6, 14→7, 15→8, 16→9, 17→10, 18→11, 19→12,
21→13, 22→14, 23→15, 24→16, 25→17, 27→18, 28→19, 29→20, 30→21, 31→22, 33→23, 34→24, 35→25,
36→26, 37→27, 38→28, 39→29, 41→30, 42→31 — et les **six codes que cette liste saute** (5, 11,
20, 26, 32, 40) sont exactement ceux qui écrivent **plusieurs fenêtres d'un coup**. La plage
5 à 42 est couverte sans trou. `CONFIRMED`.

Pour modifier une fenêtre dans les données, on sait donc quel code de liste 1 écrire — et la
liste 2 offre les mêmes pour les neuf premières, à une trame donnée.

### La liste 2 a un répartiteur — `analysis/liste2_repartiteur.md`

**Le second verrou tombe le même jour, et une conclusion est retirée.** `mothead.md` §3.12
affirmait, en `SUPPORTED`, que le DLL ne cherche que sept des 44 codes de liste 2 et que les
37 autres — 78 % des entrées — ne sont jamais consultés. **C'est faux.**

Il existe un répartiteur : **`MothRunList2`**, APM3 `0x180152CE0`, R.E.V.O. `0x18015D3A0`. Il
lit un **curseur** rangé dans l'état (`+0x498` sur APM3, `+0x510` sur R.E.V.O.), avance de 12
en 12 tant que la trame de l'entrée est échue, et **indexe** avec le code une table de 55
entrées de 32 octets — `mov r10, [table + code*32] ; call r10`. Le code n'est **jamais
comparé** : c'est pour cela qu'aucune recherche de `cmp code, K` ne pouvait aboutir. La liste 2
est une **frise chronologique**, consommée une fois dans l'ordre des trames, le curseur ne
revenant jamais en arrière ; le drapeau `+0x18` bit 0 (codes 0, 1, 8, 25, 31) signifie
« n'agit qu'à la trame exacte ».

Le fil a été une fonction de trois instructions, `0x180152DE0`, qui recopie la base
`état+0x4A0` dans le curseur `état+0x498`. La recherche précédente n'avait examiné que le
champ de base — dont personne ne se sert pour parcourir. **Le lecteur était le champ d'à
côté.**

**Les 55 codes ont un gestionnaire, dans les deux builds**, avec le même profil de drapeaux
(`analysis/mothead_liste2_gestionnaires.csv`). Sur les 104 fichiers, le code de liste 2 le
plus grand rencontré est **54**, exactement la borne du répartiteur.

- **Code 0 = un effet sonore daté.** CONFIRMED. La charge `u32` indexe une table de **410 noms
  de sons** (`fd_gard00`, `fd_punch_00`, `fd_kick_01st`, `fd_jump_00`…). 16 089 charges sur le
  corpus, 71 valeurs, toutes dans `[1, 391]`.
- **Code 9 = un commutateur de bits daté.** CONFIRMED. La charge `u16` choisit l'un de **18
  cas** qui posent ou effacent un bit du masque `état+0x4A8`. 28 224 charges et **exactement
  18 valeurs distinctes, 0 à 17** — la borne du commutateur. C'était le code le plus employé
  du format.

Les deux ont été **vus s'exécuter dans un combat** (`tools/pister_liste2.cmd`), et l'écart
`état − ROB` y vaut `0x8A0`, ce qui reconfirme la disposition du build APM3.

**Les 55 gestionnaires ont été lus**, un à un : rôle, champ écrit et forme de la charge dans
`analysis/mothead_liste2_roles.md`. Plus aucun code `UNKNOWN` en liste 2.

**Puis douze `LIKELY` sont passés à `SUPPORTED` par l'exécution.**
`tools/oracle_liste2_vivant.py` pose un point d'arrêt à l'entrée du gestionnaire **et un autre
sur son adresse de retour**, et diffe 12 Ko de `ROB` entre les deux : les mots changés sont
exactement ce que le gestionnaire a écrit, dans les conditions réelles du combat. Six
campagnes de quatre minutes ont couvert dix-sept codes. Bilan des 44 codes employés :
**16 `CONFIRMED`, 21 `SUPPORTED`, 7 `LIKELY`**.

Ce que ces campagnes ont ajouté, au-delà des promotions :

- **Six codes ouvrent une fenêtre de trames.** Pour les codes **17, 29, 33, 51, 52 et 53**, le
  premier `u16` de la charge est un **numéro de trame**, converti en flottant et rangé dans
  l'état. Vérifié sur les données : ce `u16` est supérieur à la trame de sa propre entrée dans
  **394/394**, **498/498**, **242/242**, **44/44** et 1 425/1 430 des cas. Le code 12 échoue au
  même test (106 cas inférieurs) — c'est le bon contre-exemple : sa charge est un masque.
- **Le code 33 a été pris sur le fait** : `état+0x78C` reçoit la trame de l'entrée (48.0 puis
  64.0) et `état+0x790` la charge (54.0 puis 70.0).
- **Une hypothèse a été testée et rejetée** : `état+0x784`, que le code 18 écrit, n'est pas un
  identifiant d'animation. Sur 532 entrées, 8 seulement seraient valides, et les valeurs
  fréquentes sont des puissances de deux — ce sont des masques.
- **Sept codes restent `LIKELY`**, et pour de bonnes raisons, toutes vérifiées :
  le **21** n'existe que dans le rééquilibrage 2.00 (5 entrées, absent de tout jeu arcade) et
  n'est donc **pas observable** ; les **22, 27 et 54** ne vivent que chez Brad, Jeffry, Shun et
  El Blaze — et `ROB+0x10`, désormais lu à chaque passe, dit quels personnages étaient en
  scène ; le **19** n'est pas passé **même dans un combat contre Brad**, alors que 24 de ses 40
  entrées sont chez lui : il vit dans des animations que l'adversaire n'a pas jouées ; les
  **13** et **25** s'exécutent mais ne franchissent pas leur garde — celle du 13 est lue :
  il faut que le bit 1 de `ROB+0x7B8` soit à zéro **chez les deux combattants**.

Le résultat structurant de cette lecture : **quatorze codes de la liste 2 sont des codes de la
liste 1 datés.** Leur gestionnaire fait `add rcx, 0x18` et saute dans celui de la liste 1 — et
c'est pour cela que le contexte compte six cases : les trois dernières rejouent la convention
de la liste 1.

| liste 2 | 36 | 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| liste 1 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 52 | 58 | 65 |

Les codes 38 à 46 visent **les neuf premières fenêtres temporelles** : la liste 1 les pose à
l'installation de l'animation, la liste 2 les repose à une trame donnée. Les deux verrous du
chantier se rejoignent donc sur le même objet.

Autres acquis de la lecture : les codes **3 et 4** posent et effacent un bit d'un tableau de
drapeaux basé en `état+0x1C` ; le code **26** écrit le numéro de posture en `ROB+0x65C`, soit
`ROB+0x554` de R.E.V.O. **au décalage `0x108` près — ce qui recoupe la correction d'adresse
par un troisième chemin** ; les codes **14, 15 et 16** ajoutent un octet signé à `ROB+0x690`,
le compteur que le code 70 de la liste 1 décrémente : **le compteur de boisson de Shun** ; les
codes **17, 28 et 30** partagent le bloc `état+0x4B0`, l'un posant un déplacement, l'autre une
rampe, le troisième les annulant ; les codes **0, 8 et 31** aboutissent tous les trois au même
émetteur de son.

### Le menu opérateur et le mode entraînement — `analysis/machine_etats.md`

**Deux codes d'entrée sont nommés, et le jeu a un mode entraînement.**

`Sequence_isTest` est désormais piloté par le scénario (`test = 1`), sans recompilation : le
jeu démarre alors dans `GAME TEST MODE`, dont le pied de page dit « SELECT WITH SERVICE BUTTON
AND PRESS TEST BUTTON ». En mode test, `Input_isOnNow` est interrogé pour **0, 1, 7 et 8** — et
le code **1 n'apparaît nulle part ailleurs**. Vérifié à l'écran : **code 1 = SERVICE**
(déplace le curseur), **code 0 = TEST** (valide). `CONFIRMED`.

**Piège de mesure, qui m'a d'abord fait conclure à tort** : les menus ont une
**auto-répétition**. Un appui de 350 ms balaie les six lignes et ramène le curseur à sa place
— on croit que rien n'a bougé. 80 ms ⇒ trois lignes, 40 ms ⇒ deux, **20 ms ⇒ une seule**. Le
stub relit donc son scénario toutes les **30 ms** au lieu de 250, sans quoi aucune impulsion
assez brève n'était possible.

**L'écran de test d'entrées est hors d'atteinte** : `SUB SYSTEM TEST MODE` rend la main au menu
*système* de la borne, servi par la vraie `apm.dll` via `Core_execute` ; le menu du jeu n'en a
pas. La voie visée est donc fermée — mais elle a mené ailleurs.

**La machine à états.** `0x1800DA800` est `SetState(ecx = état de tête, edx = sous-état)`, avec
**deux** tables de noms — `0x1803A0C80` (11 états de tête) et `0x1803A0CE0` (56 sous-états) ;
le découpage se prouve par le sentinelle `0x37 = 55`, qui est le `MAX` de la seconde. Le
parcours réel, relevé de l'écran-titre au combat, tient en **trois transitions** :

```
[STARTUP] -> [APM3]   sous-etat [CS_TITLE]      -> [MAX]
[APM3]    -> [MAX]    sous-etat [APM3_ENTRY]    -> [APM3_SELECTOR]
[APM3]    -> [MAX]    sous-etat [APM3_SELECTOR] -> [APM3_GAME_VS]
```

Or **`APM3_TRAINING` (52) est le frère de `APM3_GAME_VS` (50)**. En écrivant 52 dans `rdx` au
moment où le jeu demande 50, il emprunte sa propre machinerie de transition et **entre en mode
entraînement** : partenaire immobile, affichage des données de trame (`tools/dojo.cmd`,
captures `analysis/training_01.png` et `training_02.png`). `CONFIRMED`.

C'est ce qui manquait à toutes les mesures d'entrée : une scène où **seul le joueur agit**.

### Tables CSV — `analysis/CHARACTERS.md`

Roster confirmé par les données du jeu (`Sasikae-Soutyaku_Sheet1.csv`) :
`MSK`=EL BLAZE, `MON`=EILEEN, `KRT`=KARATE, `TAK`=TAKAARASHI. Les CSV sont en **CP932**.

---

## 5. Où j'en suis exactement

### Quelle part du moteur est décodée

Mesuré le 2026-09-02 sur `vf5fs-pxd-w64-Retail_APM3.dll` — **13 661 fonctions bornées par
`.pdata`, 3,13 Mo de code** :

| | fonctions | part | octets | part |
|---|---:|---:|---:|---:|
| rôle établi | **159** | **1,2 %** | 23 382 | 0,7 % |

Le chiffre est bas, et il doit l'être : **le moteur entier n'a jamais été la cible**. Les 98 %
restants sont le rendu, l'audio, le réseau, l'interface, la physique — rien de tout cela n'a
été ouvert, ni ne le sera sans raison. Ce qui est visé, ce sont les **formats de données de
combat**, et là la couverture est d'une autre nature :

- `mothead` : structure entière décodée, **104 fichiers sur 104 conformes**, et
  **9 140 identifiants d'animation sur 9 140** dans le jeu de leur personnage ;
- **les 84 gestionnaires de codes de la liste 1** lus, **77 exécutés** hors du jeu par
  l'oracle et **7 des 8 restants dans le combat** — seul le code 62 n'est jamais passé ;
- **les 55 gestionnaires de codes de la liste 2** lus, aucun `UNKNOWN`, et
  **quatorze vus s'exécuter** dans un combat ;
- **les 32 fenêtres temporelles** : quel code les pose, qui les lit, et ce qu'elles sont ;
- `mot_db` + `rob_cmn_mottbl` : **14 157 valeurs sur 14 157** arbitrées par le moteur ;
- `FARC` : identité au SHA-256 vérifiée.

Autrement dit : **1 % du binaire, et à peu près tout ce qu'on est venu y chercher.**


| Sujet | État |
|---|---|
| Inventaire, hashes, versions des 6 sources | **fait** |
| Matrice API → loader → matériel (Lindbergh) | **fait** |
| Classification du code par RTTI (168 types, ~160 `Task*`) | **fait** |
| Format FARC | **fait** |
| Base d'animations (`mot_db`, `rob_cmn_mottbl`) | **fait** |
| `mothead` : en-tête + CCD | **fait** |
| `mothead` : section 1 (structure) | **fait** |
| `mothead` : les 84 gestionnaires de codes lus | **fait** |
| `mothead` : consommateurs de l'état (`ROB+0x798`) | **localisés** |
| `mothead` : lecteurs des champs, code par code | **relevés** |
| Exécution instrumentée : outil, cible, blocage | **fait** |
| Moteur comme oracle hors du jeu | **opérationnel**, trois décodages validés |
| Les 84 gestionnaires exécutés par le moteur | **fait**, 77/81 hors du jeu, 7 des 8 restants dans le combat |
| Deux dispositions d'état selon le build | **établi** (écarts 0x18 et 0x78) |
| `vfes.exe` démarre (stub `apm.dll`) | **fait** : écran-titre en 1920×1080 |
| Entrées scriptées par le stub | **fait** : `apm_entrees.txt`, relu à chaud ; code 7 = START |
| Combat qui tourne | **fait** : Akira contre Lion, `analysis/etape4_combat.png` |
| Points d'arrêt logiciels et matériels | **faits** : `instrument.py`, DR0-DR3 sur 57 threads |
| Disposition de l'état dans le ROB, build APM3 | **corrigée** : `ROB+0x8A0`, pas `0x798` |
| `mothead` : les 32 fenêtres temporelles | **verrou ouvert** : 115 accès flottants, 15 fonctions, 32 fenêtres |
| `mothead` : nommer chaque fenêtre | **ouvert**, mais devenu ordinaire |
| `mothead` : les 37 codes de liste 2 « jamais lus » | **verrou ouvert** : répartiteur trouvé, 55/55 codes pourvus |
| `mothead` : codes 0 et 9 de la liste 2 | **faits** : son daté, commutateur de bits daté |
| `mothead` : lire les 55 gestionnaires de liste 2 | **fait** : 15 CONFIRMED, 7 SUPPORTED, 22 LIKELY, 0 UNKNOWN |
| `mothead` : sens des codes restants et des drapeaux | **ouvert** |
| `yarare.bin` : en-tête | fait ; contenu des enregistrements **ouvert** |
| Chargeurs de données dans le DLL R.E.V.O. | **carte établie**, 11 fonctions |
| Consommateur de `mothead` | **localisé** : `0x180164400`, `0x1801633C0`, `0x180164720`, `0x1801651D0` |
| Boucle principale | **non cherchée** |
| PS3 `EBOOT.BIN` | **verrouillé** (SELF NPDRM chiffré) |
| X360 conteneur STFS | **non ouvert** |
| Ghidra | **non installé** sur la machine |

`analysis/functions.csv` : 96 fonctions, chacune avec sa preuve et son niveau de confiance.
`analysis/mothead_list2_consumers.csv` : les douze fonctions qui consultent la liste 2 **hors frise**, et les sept codes qu'elles cherchent ; la frise, elle, passe par `MothRunList2`.

---

## 6. Verrous restants

| Verrou | Ce qu'il faudrait | Outil signalé |
|---|---|---|
| `USRDIR/EBOOT.BIN` (PS3) est un SELF NPDRM chiffré (`SCE`+NUL, clé rév. `0x0019`) | déchiffreur SCE + klicensee (le `.rap` fourni la contient) | **scetool**, build sorvigolova — `psx-place.com/resources/scetool-sorvigolova.256/` |
| Conteneur STFS `LIVE` (X360) | extracteur STFS, puis décodeur XEX2 | **XeXTool** — `github.com/SleepTheGod/XeXTool` ; et **`extract_xex_direct.py`** — `github.com/sp00nznet/360tools/blob/main/tools/extract_xex_direct.py` |
| `USRDIR/rom.psarc` (PS3) | dépaqueteur PSARC | — |
| Section `PSFD00` de l'ELF (62 Ko, hors convention, dans le segment exécutable) | désassemblage | — |

Référence générale sur l'outillage PS3 : `psdevwiki.com/ps3/Dev_Tools`.

**Ces outils sont signalés, pas encore récupérés ni testés.** `scetool` et `XeXTool` sont des
exécutables tiers : à examiner avant de les lancer. `extract_xex_direct.py` est du Python
source, donc lisible avant emploi — c'est par lui qu'il faut commencer côté X360.

---


## 7. Trois pistes pour la suite, par rendement décroissant

1. **Nommer les 32 fenêtres** en lisant les 96 fonctions spécifiques de
   `analysis/mothead_fenetres_sites.csv`. Plus de chance ni d'exécution : de la lecture.
2. **Les dix derniers `LIKELY` de la liste 2.** Six demandent un personnage précis (Brad,
   Shun, El Blaze) : il faut donc savoir déplacer le curseur à l'écran de sélection, ce qui
   revient à identifier les codes d'entrée — `tools/identifier_entrees.py` est écrit pour ça.
   Quatre autres (13, 20, 24, 25, 31) demandent de franchir une garde que le seul martèlement
   des boutons n'atteint pas.
3. **Identifier les douze autres codes d'entrée.** Le plus propre est l'écran de sélection de
   personnage, où le curseur bouge sans ambiguïté, ou le menu opérateur (`Sequence_isTest`
   rendu vrai) dont l'écran de test d'entrées nomme chaque signal.
4. **Ouvrir les verrous PS3 et X360** avec les outils signalés en §6 (`scetool`, `XeXTool`,
   `extract_xex_direct.py`). Le script Python du 360 est lisible avant emploi : c'est par lui
   qu'il faut commencer.
5. **Installer Ghidra** et importer les binaires dans des bases séparées
   (`ghidra/vf5fs_lind`, `vf5fs_apm3`, `revo_pc`), amorcées par `analysis/functions.csv`.

## 8. Outillage

### Lanceurs `.cmd` — `tools/`

Rien ne se lance à la ligne de commande : chaque outil a son `.cmd`, à double-cliquer.

| Lanceur | Ce qu'il fait |
|---|---|
| `lancer_vfes.cmd` | lance le jeu (écran-titre en 1920×1080) |
| `lancer_vfes_debug.cmd [secondes]` | le lance sous débogueur : DLL, exceptions, appels au stub |
| `construire_stub.cmd` | régénère et recompile le `apm.dll` de substitution |
| `verifier_formats.cmd` | contrôle de conformité `mothead` — doit dire 104/104 |
| `oracles.cmd` | fait arbitrer les décodages par le moteur — doit dire 14157/14157 |
| `lancer_vfes_combat.cmd` | lance le jeu et le laisse aller **seul jusqu'au combat**, puis capture |
| `presser.cmd <codes>` | appuie sur des boutons dans le jeu **déjà lancé**, et capture |
| `pister_fenetres.cmd [offsets]` | qui lit telle fenêtre : combat, ROB, points d'arrêt matériels |
| `pister_liste2.cmd [codes]` | prend le répartiteur de liste 2 et ses gestionnaires sur le fait |
| `menu_operateur.cmd [ligne]` | ouvre le menu opérateur de la borne et y navigue |
| `dojo.cmd` | mène le jeu au **mode entraînement**, où le partenaire ne bouge pas |

Dans un `.cmd`, écrire les **chemins système complets** (`%SystemRoot%\System32\timeout.exe`) :
sinon `timeout`, `find` et consorts sont captés par les outils Unix de Git Bash quand le
script est lancé depuis un shell bash.

### Écrit pour ce projet — `tools/`

| Script | Rôle |
|---|---|
| `inventory_sources.py` | inventaire + typage par signature + SHA-256 |
| `scan_elf.py` | lecteur ELF 32/64, LE/BE |
| `dump_section.py` | extraction de section ELF |
| `extract_strings.py` | chaînes avec offset **et adresse virtuelle** |
| `extract_rtti.py` | noms de types Itanium C++ ABI |
| `find_ptr_table.py` | tables de pointeurs vers chaînes |
| `api_matrix.py` | imports → bibliothèque fournisseur |
| `summarize_inventory.py` | résumés d'inventaire |
| `compare_assets.py` | comparaison de deux inventaires |
| `compare_dirs.py` | comparaison de N répertoires au SHA-256 |
| `unpack_ps3_pkg.py` | dépaqueteur PKG PS3 retail (AES-128-CTR, clé publique) |
| **`farc.py`** | lecteur d'archives FARC |
| `convert_csv.py` | CP932 → UTF-8 |
| **`pe_disasm.py`** | désassemblage PE x64 (pefile + capstone, bornes par `.pdata`) |
| **`motdb.py`** | base d'animations : `mot_db` + `rob_cmn_mottbl` |
| **`mothead.py`** | `mothead_<CHR>.bin` : section 1 entiere, controle de conformite, inventaire des codes |
| **`instrument.py`** | débogueur Win32 : lancement sous débogage, journal des DLL, exceptions avec type C++ démangé |
| **`oracle_mottbl.py`** | fait arbitrer le décodage de `rob_cmn_mottbl.bin` par le moteur lui-même |
| **`oracle_handlers.py`** | exécute les 84 gestionnaires de codes sur un faux combattant et relève ce qu'ils écrivent |
| **`gen_apm_stub.py`** | génère et compile le `apm.dll` de substitution qui fait démarrer `vfes.exe` |
| **`presser.py`** | appuie sur des boutons dans le jeu déjà lancé, via le scénario relu à chaud |
| **`capture_fenetre.py`** | capture une fenêtre à l'écran en PNG (DPI par moniteur) |
| **`pister_etat.py`** | mène au combat, trouve le ROB, arme les points d'arrêt matériels |
| **`pister_liste2.py`** | points d'arrêt sur `MothRunList2` et sur les gestionnaires de liste 2 |
| **`lire_gestionnaires_liste2.py`** | résume les 55 gestionnaires : champs touchés, charge lue, appels |
| **`oracle_liste2_vivant.py`** | diffe le `ROB` avant et après chaque gestionnaire, dans le combat |
| `identifier_entrees.py` | identifie les codes d'entrée à l'écran de sélection, par diff d'image |
| **`tracer_etats.py`** | trace la machine à états, et sait la dévier (`--devier 50 52`) |
| **`menu_test.py`** | pilote le menu opérateur par impulsions de 20 ms, curseur lu à l'image |
| `muet.py` | coupe le son du seul `vfes.exe`, sans toucher au volume général |
| `poser_roles_liste2.py` | consigne les rôles lus dans le CSV des codes et dans la doc |
| `apm_entrees.txt` | le scénario d'entrées joué par le stub |
| `scenarios/combat_martelage.txt` | mène au combat puis martèle les boutons |
| `lancer_vfes.cmd` | lanceur de `vfes.exe` depuis la copie de travail |

Dépendances installées : `capstone`, `pefile`, `pycryptodome`.

### Outils tiers — `tools/`

| Outil | État |
|---|---|
| `PARtool v1.3.windows-x64/ParTool.exe` | fonctionne, archives `.par` |
| `FFmpeg-based-ADX-converter/` | fonctionne, audio ADX |
| `loaders/lindbergh-loader/` | clone de référence, lecture seule |
| `PSN.PKG.Decryptor...` | redondant ; **ne déchiffre pas les SELF** |
| `PARC.Archive.Importer.exe` | interface graphique, non scriptable |
| `FARC-v0.1.0-alpha2-.exe` | **échoue** sur les archives du jeu — utiliser `farc.py` |
| `PS4 PKG Tool` | sans objet, aucune source PS4 |

### Piège de `pe_disasm.py`

Le balayage linéaire de `.text` s'arrête au premier octet invalide et ne trouve rien.
**Toujours passer par `.pdata`** (`runtime_functions()`), qui donne les bornes exactes des
14 178 fonctions.

---

## 9. Carte des documents

| Fichier | Fait foi sur |
|---|---|
| **`REPRISE.md`** | **l'état courant** |
| `analysis/INITIAL_REPORT.md` | l'inventaire et l'identification des versions (phases 0/1) |
| `analysis/SOURCES.md` | le référentiel des six sources et les extractions |
| `analysis/VERSIONS.md` | l'identification des versions, avec preuves |
| `analysis/MANIFEST.md` | les SHA-256 |
| `analysis/SOURCE_INVENTORY.md` | le contenu détaillé de chaque source |
| `analysis/CHARACTERS.md` | le roster, les codes, le vocabulaire du corps |
| `analysis/CODE_CLASSIFICATION.md` | GAME / MOTEUR / LINDBERGH / TIERS |
| `analysis/API_MATRIX.md` | jeu → API → loader → matériel |
| `analysis/LOADER_ARCHAEOLOGY.md` | l'apport des loaders, avec validation croisée |
| `analysis/MODERN_DATA_LINEAGE.md` | ce que US et R.E.V.O. ont hérité |
| `analysis/functions.csv` | la base de fonctions |
| `docs/formats/farc.md` | le format FARC |
| `docs/formats/mothead.md` | le format `mothead_<CHR>.bin`, sections 1 et 2 |
| `analysis/mothead_opcodes.csv` | les codes de `mothead` : emplois, taille de charge, gestionnaire |
| `analysis/disasm_mothead_section1.txt` | les quatre fonctions du moteur qui lisent la section 1 |
| `analysis/disasm_mothead_handlers.txt` | les 84 gestionnaires de codes de la liste 1 |
| `analysis/disasm_mothead_consumers.txt` | les consommateurs de l'état de mouvement |
| `analysis/disasm_mothead_readers.txt` | les lecteurs des champs, code par code |
| `analysis/disasm_mothead_readers2.txt` | les dix derniers codes qui écrivent un champ |
| `analysis/disasm_mothead_ondemand.txt` | les codes réclamés à la demande (43, 44, 71) |
| `analysis/disasm_mothead_list2.txt` | les consommateurs de la liste 2 |
| `analysis/mothead_list2_consumers.csv` | tous les sites de consommation de la liste 2 |
| `analysis/INSTRUMENTATION.md` | l'exécution instrumentée : cible, outil, blocage, oracle, dispositions d'état |
| `analysis/fenetres_temporelles.md` | **les 32 fenêtres** : le verrou ouvert, et comment |
| `analysis/liste2_repartiteur.md` | **la liste 2** : le répartiteur, et la conclusion retirée |
| `analysis/machine_etats.md` | la machine à états, le menu opérateur, et le mode entraînement |
| `analysis/mothead_liste2_gestionnaires.csv` | les 55 gestionnaires de liste 2, dans les deux builds |
| `analysis/mothead_liste2_roles.md` | **le rôle de chacun des 55**, lu gestionnaire par gestionnaire |
| `analysis/pistage_liste2.txt` | le relevé brut des points d'arrêt sur la liste 2 |
| `docs/formats/apm_input.md` | l'interface d'entrée d'`apm.dll` et le scénario du stub |
| `analysis/mothead_fenetres_sites.csv` | les accès flottants aux fenêtres, fenêtre par fenêtre |
| `analysis/pistage_fenetres.txt` | le relevé brut des points d'arrêt matériels |
| `analysis/etape4_combat.png` | la preuve que le combat tourne |
| `analysis/oracle_handlers_sortie.txt` | la sortie de la passe sur les 84 gestionnaires |
| `analysis/vfes_ecran_titre.png` | la preuve que `vfes.exe` démarre |
| `analysis/mothead_state_readers.csv` | tous les accès aux champs de l'état, offset par offset |
| `docs/formats/mot_tables.md` | `mot_db.bin` et `rob_mot_tbl.bin` |
| `comparisons/rob_data_matrix.csv` | l'identité des données de combat sur 5 versions |

## Dural (2026-09-03)

Etat : voir `analysis/dural.md`.

- **Acquis, CONFIRMED** : l'enumeration interne des personnages compte **21**
  entrees ; `0x18012CA90` (indice -> donnees) borne par `cmp ecx, 0x15`, donc
  **0 a 20 valides**, et l'entree 20 est `DUR` / `DURAL`. L'entree 19 est `TE2`,
  vide. Le moteur n'exclut pas Dural.
- **Acquis** : `ROB+0x10` est l'indice de personnage, et c'est lui que le
  chargeur lit pour batir `mot_%s.bin` (`0x180151F5E` joueur 1,
  `0x18015209B` joueur 2).
- **Non fait** : la substitution a l'execution. `tools/forcer_dural.py` pose le
  point d'arret trop tard (0 passage). A reprendre en le posant des le
  chargement du moteur, sur les quatre sites de `mot_%s.bin`.
- **Impasses documentees** : point d'arret materiel en ecriture sur `ROB+0x10`
  (0 acces en 245 s) ; balayage memoire du choix de personnage en zone d'image
  (0 adresse -- le choix est sur le tas).

## Parente console (2026-09-03)

Voir `analysis/parente_console.md`. Le build APM3 **est** le build console :
48 des 56 sous-etats sont ceux de la PS3 (dont quinze `DATA_TEST_*`), et le code
des menus console est compile dedans (2 references par chaine de menu). Rien a
rapatriser : le PS3 est du PowerPC, et de toute facon tout est deja la. Le
travail est une question d'**atteignabilite**, comme la deviation qui a ouvert
le DOJO. Piste la plus prometteuse : `DATA_TEST_CHR` / `DATA_TEST_MOT`
(sous-etats 30 et 25), qui montreraient Dural sans passer par la grille.

================================================================================
## SESSION DU 2026-09-03 -- ce qui a change

Journee dense. Quatre chantiers avances, dont deux **livres et verifies a
l'ecran par Frederic**, un ouvert avec un blocage precis, un ferme.

### LIVRE ET VERIFIE : resolution, langue, logo, ecran noir, entrees

Un patcheur unique, `tools/patch_moteur.py`, qui repart **toujours** des
`.origine` -- les correctifs ne s'empilent plus.

```
py -3 tools/patch_moteur.py --resolution 1280 720 --langue --logo-japonais
py -3 tools/patch_moteur.py --lire      /  --rendre
```

| correctif | ou | verifie |
|---|---|---|
| **resolution** | `vfes.exe` 0x140002FD6 / 0x140002FDD, moteur 0x1800E74A6 / 0x1800E74B0 | « plus de zoom et fluide » |
| **langue** | moteur 0x1802447B0 **et** 0x1802447C0 -- les DEUX getters | « plus de caractere japonais » |
| **logo japonais** | moteur 0x18006BBD1, `call` -> `xor eax,eax` | -- |
| **ecran noir** | traverse par impulsion START (`--passer-entry`) | « c'est parfait » |
| **clavier/manette** | stub `apm.dll` : W=GUARD X=PUNCH C=KICK | joue |

Lanceur du Bureau : `Virtua Fighter 5 FS.cmd`, option 1 = jouer sans ecran noir.

### OUVERT : Dural se charge mais se fige

**La source de la selection est trouvee** apres deux impasses :

```
moteur+0x14F5B3   mov ecx, [rbx-0x10c]    ; l'indice de personnage
moteur+0x14F5C5   call CodeDuPersonnage
```

Ce site passe **deux fois**, une par joueur, au chargement. `rbx-0x10C` est hors
des ROB : c'est la structure de selection, en amont. `tools/pister_perso.py
--forcer 20 --depuis 0 --rob` y ecrit l'indice de Dural.

**Resultat** : Dural se charge (modele a l'ecran) mais **se fige sur l'etat de
mouvement 0x510B** -- 2 changements contre 14 pour un personnage normal force
par la meme methode (temoin TAK). Ce n'est donc **ni la methode, ni les
donnees** : tout est dans le `.par`, et les quatre sites de `CodeDuPersonnage`
recoivent bien 20.

### FERME : DATA_TEST, et le court-circuit de APM3_ENTRY

- Les quinze ecrans `DATA_TEST_*` sont **compiles hors du build** : chaque nom
  n'apparait qu'une fois, dans la table de noms, et aucune chaine de menu de
  debogage n'existe. Quatre captures identiques a l'octet pres en martelant les
  treize codes. La voie courte vers Dural n'existe pas.
- **Sauter `APM3_ENTRY` plante** : violation d'acces a `moteur+0xB1D33`. Il
  prepare ce que la selection lit. On le traverse, on ne le saute pas.

### LE MENU CONSOLE : donnees recuperees, chargement manquant

Voir `analysis/menu_console.md`. En resume :

- la Xbox 360 est une impasse (chaque fichier dans un conteneur `0F F5 12 ED`,
  decompresseur dans un XEX chiffre + LZX) ;
- **le PS3 est en clair** : `tools/psarc.py` ouvre `USRDIR/rom.psarc` ;
- **le format est identique**, pas de gros-boutisme :
  `aet_c_mchdur.bin` a les memes octets des deux cotes ;
- 20 fichiers `aet_n_*` / `spr_n_*` poses, et le moteur les lit ;
- **mais il ne demande jamais `aet_n_main`** : le build arcade a garde le code
  qui DESSINE le menu, pas celui qui CHARGE ses ressources.

### YAMP : le moteur enfin nomme

https://github.com/CookiePLMonster/YAMP (MIT, lu et non execute).

| notre nom | le vrai |
|---|---|
| `SetState` 0x1800DA800 | **`shift_next_mode`** / **`shift_next_mode_sub`** |
| regle archive-puis-disque | **`isl_file_access`** : `csl_file_access` et `csl_file_access_archive` |
| point d'entree | **`module_start` / `module_stop`** -- nos SEULS exports |

`MODE_SUB_MAX = 48` cote Steam contre **55** chez nous : l'ecart vaut exactement
les sept etats `APM3_*`. **Nos sous-etats 0 a 47 sont ceux de la console.**

`module_start(size_t args, const void* argp)` recoit `args = 0x70` et une
structure de 112 octets faite de pointeurs (contextes son, graphique, entrees,
plus un chemin de jeu en `vfes.exe+0x6E3C40`). **C'est la que YAMP passe le mode
de jeu et la langue.** La piste n'est pas epuisee : il reste a identifier lequel
de ces pointeurs porte le `vf5fs_game_config_t`.

### Outils nouveaux

`stfs.py` (conteneurs Xbox 360), `psarc.py` (archives PS3), `patch_moteur.py`,
`par_masquer.py`, `pister_perso.py`, `tracer_fichiers.py`, `config_module.py`,
`langue.py`, `resolution.py`, `patch_resolution.py`.

### Etat laisse

Jeu ferme. Les 20 entrees du `.par` **rendues**. Patches resolution + langue +
logo **en place**. Les fichiers PS3 restent dans `vf5fs_media/rom/2d/` mais sont
ignores (l'archive reprend la main).

================================================================================
## SESSION DU 2026-09-03 (soir) -- LE MENU CONSOLE S'AFFICHE

Chantier 2 debloque. Detail complet dans `analysis/menu_console.md`, section 6.

### Le fil, en trois maillons

1. **`vf5fs_game_config_t` trouve.** YAMP en donne les champs ; il est a
   `argp+0x38` dans les 112 octets de `module_start`, et `vfes.exe` l'ecrit en
   cinq instructions (`0x140002D45`, `D77`, `DE7`, `E1C`, `E32`). La lecture
   statique predit **exactement** les huit octets releves au debogueur :
   `DC 00 02 2D 02 01 00 00`. Le moteur les recopie dans `0x18064D950` -- dont
   l'octet +6 est celui de la langue deja patche la veille -- et en derive
   quatre drapeaux, dont **`0x180C3B701` = `game_mode != 0`, l'aiguillage
   borne/console, consulte a 32 endroits**. CONFIRMED.

2. **`game_mode = 0` demarre le mode console.** Parcours mesure :
   `DATA_INITIALIZE -> SYSTEM_STARTUP -> CS_DEMO -> CS_TITLE -> CS_SIGNIN ->
   WARNING -> CS_AUTOLOAD -> etat MENU`. La derniere transition **est**
   `dest_cs_autoload()` de YAMP. Trois ecrans que la borne n'affiche jamais.
   Et, les vingt entrees du `.par` masquees, `aet_n_main.bin` et
   `spr_n_main.farc` sont **enfin demandes** -- le verrou du 2026-09-03 matin
   saute. CONFIRMED.

3. **Le menu restait vide parce que deux tics manquaient.** La fonction de
   dessin `0x1801E0C80` garde chaque bloc par `cmp dword [rcx], 3`. Mesure :
   **1452 passages, les deux objets AET a l'etat 1, jamais 3.** Le tic
   `0x1801BBB10` fait 1->2->3 ; personne ne le faisait tourner. La page de menu
   est construite par `0x1801DA550` avec cinq pages soeurs ; le creneau 2 de
   leurs vtables est la mise a jour, et en comptant les appels au tic :
   **cinq soeurs a 2, le menu a 0**. C'est la coupe, a l'instruction pres.

### Le correctif, permanent

```
py -3 tools/patch_moteur.py --resolution 1280 720 --langue --logo-japonais --mode 0 --menu-console
```

`--mode 0` : un octet de `vfes.exe` (offset fichier `0x002220`).
`--menu-console` : un relais de 52 octets dans le rembourrage de `.text`
(`0x18034575C`) qui fait les deux tics manquants puis saute dans
`0x1801DC620`, et le creneau 2 de la vtable (`0x180532AF8`) repointe dessus.

Mesure apres : `1578 x en-tete = 3 (PRET), texte = 3 (PRET)`.
**A l'ecran, verifie par Frederic : le menu s'affiche.**

`tools/patch_moteur.py` sait aussi regler energie, rounds, temps, difficulte, et
poser `is_dural_unlocked` / `is_triangle_start` (`--dural`, `--triangle`) --
ces deux derniers sont exposes parce qu'ils sont dans les memes huit octets,
pas parce qu'ils ont ete essayes.

### Ce qui reste ouvert : la navigation

Le menu ne repond pas aux directions. Mesure au journal du stub, sur 55 s :
le moteur interroge `Input_isOn` pour tous les codes 2 a 14 (2640 appels
chacun) et le stub a bien rendu VRAI pour les directions scriptees et START ;
`Input_isOnNow` n'est demande que pour les codes 0, 7, 8, 15. **Les appuis
atteignent le moteur ; le menu n'en fait rien.**

Une piste a ete ecartee faute de preuve : les trois structures de 0x44 octets
lues 21 fois par trame par la mise a jour (`ctx+0x4FD0`, `+0x5014`, `+0x5058`
sur le global `0x180752148`) ne bougent pas de la passe, mais leur contenu
ressemble a des reglages, pas a un etat de manette. Rien n'est conclu.

**Prochaine mesure, sans presupposer** : echantillonner l'objet de page entier
a chaque trame et relever les decalages qui changent pendant les fenetres
d'appui. Rien qui bouge = l'entree n'atteint pas la page ; quelque chose qui
bouge = c'est le curseur.

### Outils

- `tools/pister_menu.py` (neuf) : lit la garde du menu, sait la forcer,
  depouille le journal d'entrees du stub, observe les structures de manette.
- `tools/patch_moteur.py` : + `--mode`, `--energie`, `--rounds`, `--temps`,
  `--difficulte`, `--dural`, `--triangle`, `--menu-console`.
- `tools/scenarios/console_start.txt`, `console_journal.txt` (neufs).

### Piege confirme deux fois de plus

Les captures prises par le debogueur **et** par `capture_fenetre.py` ont
photographie la fenetre de Claude, pas le jeu : le premier plan ne se vole pas
sous Windows. Consigne de Frederic : « arrete avec les captures, je te dis ce
que je vois. » Son oeil fait foi.

### CORRECTION, meme seance : la vraie cause, et une erreur de methode

Ce que j'ai ecrit plus haut -- « la mise a jour du menu n'a AUCUN tic la ou ses
cinq soeurs en ont deux » -- **est faux**. Le comptage etait borne par une seule
entree `.pdata`, alors que la fonction en occupe trois (`0x1801DC620`,
`0x1801DCE9D`, `0x1801DD146`) : `0x1801DCE9D` commence par
`mov [rsp+0xd8], r12`, ce n'est pas un prologue. **Une entree `.pdata` n'est pas
une fonction.** Le menu a bien ses trois tics, dans un bloc qu'on n'atteignait
jamais.

La vraie cause, mesuree par jalons : tout sort par **`0x1801DC6D6`**.

```
0x1801DC6C2  cmp  byte [rdi+0x29FB], 0   ; drapeau "initialisation faite"
0x1801DC6C9  jne  0x1801DC709            ; deja faite -> le corps du menu
0x1801DC6CF  call 0x180029FB0            ; <- BOUCHON : `mov al,1 ; ret`
0x1801DC6D6  jne  0x1801DCE33            ; -> retour faux, a chaque trame
0x1801DC6E3  mov  byte [rdi+0x29FB], 1   ; JAMAIS ATTEINT
```

`0x180029FB0` est le troisieme bouchon de la famille, avec `0x180007450` et
`0x180007430`. Le menu attend une initialisation qui ne finira jamais. Cela
explique **les deux** symptomes : menu vide ET navigation morte.

Correctif juste : `--menu-init` (six `90` a l'offset `0x1DBAD6` du moteur).
Mesure apres, **sans** le relais : l'initialisation se fait une fois, le bloc
des tics tourne 155 fois, et les scenes atteignent l'etat 3 toutes seules.
`--menu-console` devient un contournement inutile ; il reste documente comme
tel.

Ligne de commande a jour :

```
py -3 tools/patch_moteur.py --resolution 1280 720 --langue --logo-japonais --mode 0 --menu-init
```

**Ce qui bloque encore** : le corps sort 1068 fois plus loin, sur l'une des deux
gardes de `0x1801DC999` (`0x1801DE560` doit rendre vrai, `0x1800BA090` doit
rendre faux) -- aucune des deux n'est un bouchon. Prochaine passe : jalons sur
`0x1DC9AD` et `0x1DC9BA` pour savoir laquelle se ferme. Juste derriere se trouve
la machine a etats propre du menu : `[rdi+0x29E8]`, 0 a 10, table de saut a
11 entrees en `0x1801DC9E7`.

**Acquis ferme au passage** : les codes de direction ne sont plus une hypothese.
`0x180243ED0` est le lecteur d'entrees ; codes 2/5/3/4 -> bits 12/13/14/15,
START 0, KICK 1, PUNCH 2, GUARD 3. Il calcule ses propres fronts (d'ou l'absence
d'`Input_isOnNow` sur les directions), et l'etat de manette mesure dans le menu
est **correct**. Cela raye une des trois pistes du paragraphe 7.

================================================================================
## SESSION DU 2026-09-04 -- Dural : deux negatifs qui valent cher

Courte reprise apres la seance du menu console.

- **`is_dural_unlocked` ne dege le rien.** Le drapeau trouve la veille dans le
  `vf5fs_game_config_t` a ete pose (`--dural`) puis mesure : Dural reste sur
  `0x510B`, deux changements, exactement comme sans lui. Coherent avec la
  lecture statique -- les cinq sites qui lisent `0x180C3B700` sont tous dans le
  code d'interface console. Le drapeau ouvrira la grille, pas le combat.

- **`0x510B` est le REPOS de Dural**, pas un etat casse : `DUR_L_IDLE_TA`,
  role 0 posture 0 de l'entree 20. Calcule **sans lancer le jeu**, l'oracle
  ayant deja prouve que `motdb.py` rend ce que rend le moteur. Dural est meme
  mieux pourvue que TAK : 356 roles resolus sur 363 contre 349.

- **La machinerie de roles tourne pour elle**, a la meme cadence que pour le
  temoin (voir `analysis/dural.md` section 12).

La question a donc change de forme : **pourquoi Dural ne quitte-t-elle jamais
son repos**, alors que tout ce qui precede l'installation de l'animation
fonctionne ? Le blocage est en aval de `GetMotionForRole`.

### La piste pour demain : se servir vraiment de la pierre de Rosette

YAMP nous a deja donne le `vf5fs_game_config_t`, et c'est lui qui a ouvert le
mode console. Mais on ne s'en sert que comme d'une documentation. Deux emplois
bien plus forts restent inexploites :

1. **Le diff des deux moteurs.** On a les DEUX binaires sur cette machine :

   ```
   APM3  runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll
   REVO  C:\Program Files (x86)\Steam\steamapps\common\VFREVO\runtime\media\
         vf5fs\vf5fs-pxd-w64-d3d12_SteamRetail.dll
   ```

   Le build arcade a bouchonne au moins trois predicats : `0x180029FB0`
   (`mov al,1 ; ret`), `0x180007450` (`xor al,al ; ret`) et `0x180007430`
   (`ret 0`). **Dans R.E.V.O., ces fonctions existent pour de vrai.** Les lire
   la-bas dit ce que le menu attendait -- et la meme methode s'applique a tout
   autre bouchon qu'on rencontrera, Dural comprise. C'est exactement l'emploi
   d'une pierre de Rosette, et on ne l'a jamais fait.

2. **Le source de YAMP nomme le code console.** `source/Y6/cs_game.cpp` porte
   les `dest_cs_*` -- c'est-a-dire la suite `CS_TITLE / CS_SIGNIN / WARNING /
   CS_AUTOLOAD` qu'on vient de parcourir a l'aveugle. Le lire donnerait les
   noms et l'ordre attendu de ce qu'on instrumente.

Ce que YAMP ne peut PAS faire tel quel : heberger notre DLL. Il construit une
`module_params_t` de 64 octets pour le build Steam ; la notre en fait 112, avec
trois champs APM3 en plus (`+0x40`, `+0x60`, `+0x68`) -- et `+0x68` porte
justement l'interface de rappel que la mise a jour du menu appelle. Le lancer
sur `Retail_APM3.dll` laisserait ce pointeur nul.

================================================================================
## OUTILLAGE AJOUTE LE 2026-09-04

Rappel de la regle : **chaque outil a son lanceur `.cmd`**, et rien ne se tape
a la ligne de commande. Les lanceurs neufs sont `menu_console.cmd` et
`grille_console.cmd`.

### Ecrit pour le projet

| outil | role |
|---|---|
| **`sllz.py`** | lecteur d'index **PARC** + decompresseur **SLLZ v1**. Donne acces a n'importe lequel des 1862 fichiers de `vf5fs_data.par` **sans extraire les 4 Go** -- ce que `ParTool.exe` ne sait pas faire. Manquait au projet depuis le debut. |
| **`aet.py`** | lecteur de planches **AET** : scenes, compositions, calques. C'est lui qui a tranche la question de Dural. |
| **`bouchons.py`** | inventaire des fonctions bouchonnees du build : 20 bouchons, 1086 sites d'appel. Passe par les **cibles d'appel** et non par `.pdata`, car un bouchon est une feuille sans entree de deroulement. |
| **`pister_menu.py`** | la garde du menu, son forcage, le journal d'entrees du stub, l'etat de manette, le diff d'objet, les jalons, la deviation d'etat et le **forcage direct des globaux** du repartiteur. |
| **`pister_grille.py`** | lit en memoire le tableau de cases du selecteur (20 cases, la 19e est Dural). |
| **`pister_scenes.py`** | releve les scenes nommees que le jeu reclame, avec leur site d'appel. A donne `SEL_COMMON` / `SEL_CHARA` / `SEL_CURSOR` en une passe. |
| **`pister_vga.py`** | dit si le selecteur charge la variante **VGA** ou **WXGA**. |
| **`carte_zone.py`** | cartographie une ZONE entiere : toutes les fonctions, leurs bornes, appelants, appeles, chaines, globaux connus, immediats remarquables, bouchons. 411 fonctions du selecteur en une minute. C'est lui qui a trouve la garde de Dural. |
| **`plage.py`** | desassemble une PLAGE d'adresses **sans s'arreter au premier `ret`**. Une vraie fonction couvre souvent plusieurs entrees `.pdata` chainees ; la prendre pour la fonction entiere fait conclure faux. |
| **`libelles.py`** | resout un identifiant de texte en libelle, via `string_array.farc` du `.par` (FArc, **gros-boutiste**). C'est lui qui a nomme les neuf entrees du menu console. |

Ajouts a `patch_moteur.py` : `--mode`, `--energie`, `--rounds`, `--temps`,
`--difficulte`, `--dural`, `--triangle`, `--menu-init`, `--menu-ranking`,
`--menu-service`, `--menu-console`, `--wxga`, `--dural-grille`.

Ajouts a `pister_perso.py` : `--moth` (les roles demandes a `GetMotionForRole`)
et `--surveiller` (point d'arret materiel sur l'etat de mouvement du ROB).

### Scenarios neufs

| fichier | role |
|---|---|
| `scenarios/console_start.txt` | franchit titre, sauvegarde et avertissement en mode console |
| `scenarios/console_journal.txt` | le meme, avec `journal = 1` et des directions scriptees |
| `scenarios/rester_grille.txt` | **parque le jeu sur `APM3_SELECTOR` et l'y laisse** -- indispensable, la borne ne donne que quinze secondes sur cet ecran |

### Sources tierces telechargees et LUES (aucune executee)

| source | licence | ce qu'elle a donne |
|---|---|---|
| **YAMP** (CookiePLMonster) `source/V6-VF5FS.cpp` | MIT | le `vf5fs_game_config_t` : c'est lui qui a ouvert le mode console |
| **ParManager** (Kaplas80) `ParLibrary/Sllz/Decompressor.cs` | MIT | l'algorithme SLLZ v1 -- `ParTool.exe`, deja dans `tools/`, en est la partie visible |
| **AetPlugin** (samyuu) `src/comfy/file_format_aet_set.cpp` | -- | la structure des planches AET, format partage avec Project DIVA |

Les fichiers telechargés sont dans le repertoire temporaire de la session, pas
dans le depot : ce sont des references de lecture, pas des dependances.

---

# SESSION DU 2026-09-04 (soir) — **DURAL EST JOUABLE**

Verdict à l'écran, mot pour mot : « dural selectionnable, aucun defaut
perceptible pendant les combats, Dural est jouable. »

Le but ouvert le 2026-09-02 est atteint, et par la voie propre : **patch
statique uniquement**, pas de débogueur en fonctionnement, pas de forçage à
l'exécution. Le jeu se lance normalement.

    py -3 tools/patch_moteur.py --resolution 1280 720 --langue \
        --logo-japonais --dural --wxga --dural-grille

## Ce qui bloquait, et qui n'était pas ce qu'on croyait

La grille de la borne ne « manquait » pas de Dural. Sa case existe dans la
table de disposition `0x1803FF0B0` — sept colonnes, trois lignes, 21 cases,
Dural en bas à gauche (colonne 0, ligne 2, personnage 20). Le jeu la construit,
la dessine — puis la **désactive explicitement** :

    0x18016E20B  call 0x180007450   ; prédicat bouchonné -> 0
    0x18016E212  jne ...            ; jamais pris
    0x18016E214  mov edx, 0x14      ; 20 = DURAL
    0x18016E21C  call 0x180173F50   ; pose 1 en +0x14 de sa case

et le déplacement du curseur (`0x180173110`) saute toute case marquée
(`cmp byte [rax+0x14], 0 ; jne suivante`). Détail complet, avec les deux tables
de disposition et le constructeur de liste : **`analysis/dural.md` section 14**,
qui fait foi.

## Trois leçons de méthode, qui valent au-delà de Dural

1. **Cartographier une zone entière coûte une minute et remplace vingt
   questions.** Toute la journée avait été passée à désassembler à la demande —
   une fonction, une question — ce qui donne l'illusion d'avancer : quatre
   fausses pistes, trois correctifs bâtis sur des lectures locales et démentis à
   l'écran. `tools/carte_zone.py` a sorti les 411 fonctions du sélecteur d'un
   coup, et la garde est apparue en une minute.

2. **Un balayage n'est systématique que si sa prémisse l'est.** Le premier
   « balayage systématique » cherchait les appels au bouchon *autour des chaînes
   `_dur`* : deux résultats. En énumérant les appelants dans toute la zone :
   **seize**. Deux dessinent la case, un troisième la rend atteignable.

3. **Une fonction n'est pas une entrée `.pdata`.** Le déplacement du curseur
   couvre sept entrées chaînées (0x180173110 → 0x1801735C5, 1205 octets). D'où
   `tools/plage.py`, qui désassemble une plage sans s'arrêter au premier `ret`.

## Une erreur de numérotation corrigée

Les notes affirmaient « dur = 19, rnd = 20 » dans une numérotation d'affichage
distincte. **Faux** : la case 19 de la table porte le personnage **20**, et la
grille de la borne n'a aucune case aléatoire. Les quatre bornes `cmp .., 0x12`
devaient passer à **0x14**, pas 0x13 — à 0x13 on n'ouvrait que TE2. C'est
pourquoi `--dural-grille` seule n'avait rien changé au premier essai.

## Ce qui reste ouvert

Le **menu console** — demandé explicitement pour plus tard. État connu, dans
`analysis/menu_console.md` : il s'affiche, le curseur bouge, mais la logique
vit dans l'objet de page et non dans le sous-état ; le verrou est
`[menu+0x2A09]`, **deux lecteurs, zéro écrivain**. R.E.V.O. ne sert pas de
greffon (disposition d'objet différente : sa page utilise +0x3024/+0x27C0, la
nôtre +0x29FB/+0x2A09 ; 70 sous-états contre 55).

---

# SESSION DU 2026-09-04 (nuit) — **LE PARCOURS CONSOLE BOUCLE**

Vérifié à l'écran, dans l'ordre : Dural jouable, puis le menu console mène au
combat, puis le combat ramène au menu, puis on peut relancer un combat.

    MENU_MAIN
      -> SINGLE PLAYER       maillon 1 : session créée, mode GAME, SELECTOR
      -> SELECTOR            la grille, Dural comprise
      -> VS                  maillon 2 : la fin du sélecteur mène au combat
      -> GAMEOVER/SELECTOR   arbitre 0x1800DB100 — déjà en place
      -> MENU_MAIN           maillon 4 : retour au menu, non au titre

Une seule commande, un seul lanceur : `tools/console_combat.cmd`.

    py -3 tools/patch_moteur.py --resolution 1280 720 --langue --logo-japonais \
        --dural --wxga --dural-grille --mode 0 --menu-init --menu-ranking \
        --transition-game

## Ce que ça établit

**Le cœur du mode console est intact dans ce build.** Le mode GAME, ses quatre
sous-états (SELECTOR, MODE_SELECTOR, VS, GAMEOVER) et l'arbitre de fin de
combat n'ont pas été retirés. Ce qui manquait tenait en **quatre maillons** —
deux transitions, une création d'objet, une branche — et en **quatre prédicats
bouchonnés**.

## Le motif, qui s'est répété quatre fois

Un chemin complet, et un **dernier verrou bouchonné** juste avant l'arrivée :

| verrou | ce qu'il ferme |
|---|---|
| `0x18016E20B` | la case de Dural dans la grille |
| `0x18016DC69` / `0x18016E109` | les compositions `_dur` du dessin |
| `0x1801DE0ED` | l'entrée `DLC STORE` |
| `0x1801B6E8E` | le retour au menu après le combat |

Tous appellent le **même corps**, `0x180007450` (`xor al,al ; ret`), qui a 210
appelants : c'est un repliement COMDAT entre plusieurs prédicats distincts.
**On patche le site d'appel, jamais le corps** — et quand la branche a une
portée nulle (le mode GAME n'a aucun autre demandeur), on corrige la branche
plutôt que le prédicat, qui lui en a quatre.

## Documents

- `analysis/menu_console.md` — bilan des liens (§8), transition (§9, §11), entrées (§10)
- `analysis/vs_gameover.md` — VS et GAMEOVER, le type de partie, le maillon 4
- `analysis/couverture_console.md` — **ce qui reste** : 10 % de la surface lue
- `analysis/dural.md` §14 — Dural jouable

---

# SESSION DU 2026-09-04 (nuit, suite) — **VERSUS À DEUX JOUEURS**

Deux entrées du menu console mènent au combat, et le versus se joue vraiment à
deux : **clavier = joueur 1, manette = joueur 2**.

    py -3 tools/patch_moteur.py --resolution 1280 720 --langue --logo-japonais \
        --dural --wxga --dural-grille --mode 0 --menu-init --menu-ranking \
        --transition-game --joueur2 --menu-fermer

Lanceur : `tools/console_combat.cmd`.

## Le joueur 2 n'existait pas — au sens propre

    0x180243F5F  mov  ebx, r14d       ; ebx = 0
    0x180243F62  test ebp, ebp        ; ebp = le numéro de joueur
    0x180243F64  jne  0x1802440D6     ; JOUEUR 2 : saute TOUTES les lectures

Le masque de boutons du joueur 2 valait **toujours zéro**. D'où l'écran de
réglages d'OFFLINE VERSUS grisé, qui réclame en clair une seconde manette
(texte 0x81, résolu par `tools/libelles.py`).

**Mais le lecteur avait été écrit pour deux joueurs, puis amputé** : deux de ses
treize sites de code étaient restés relatifs au joueur (`lea edx, [rbp + N]`).
D'où un correctif de trois octets d'idée :

1. les onze `mov edx, imm32` deviennent `lea edx, [rbp + code]` + deux `nop` ;
2. les six octets du saut retiré reçoivent **`shl ebp, 4`** — `rbp` vaut 0 pour
   le joueur 1, **16** pour le joueur 2, dont les codes deviennent 18 à 30.

Et le décalage ne casse pas la boucle sans rien restaurer : après ce point
`ebp` n'est relu qu'à `inc ebp ; cmp ebp, 2 ; jb`. Joueur 1 → 0 puis 1, on
repart. Joueur 2 → 16 puis 17, on sort. Exactement le comportement voulu.

Côté `apm.dll` (notre stub), les deux sources sont séparées : codes 0-14 au
**clavier seul**, codes 18-30 à la **manette seule**. Sans quoi la manette
pilotait les deux joueurs.

## Maillon 6 : éteindre le menu

Le menu restait allumé sous le combat et consommait les entrées. Sa sortie
(`0x1800DCB80`) ne démonte ses trois tâches que si `0x1801B7010` — « l'objet
`0x180752000` n'est pas occupé » — et il l'est quand on entre en combat depuis
une page encore ouverte. Pire, elle rend alors `al = 0` (« pas fini ») et la
transition reste en suspens. `--menu-fermer` rend le démontage inconditionnel.

## Les touches

| | joueur 1 (clavier) | joueur 2 (manette) |
|---|---|---|
| curseur | flèches | croix directionnelle |
| valider | `A`, `T`, `R`, `Entrée` | **X, LB, Y, START** |
| pièce | Espace | BACK |

---

# SESSION DU 2026-09-04 (nuit, fin) — **LE MODE CONSOLE EST JOUABLE**

Quatre entrées du menu mènent quelque part, et on peut en ressortir.

| entrée | état |
|---|---|
| SINGLE PLAYER | combat solo, Dural comprise, boucle complète |
| OFFLINE VERSUS | combat à deux, **clavier 1P / manette 2P** |
| DOJO | entraînement, ses deux modes |
| — | **Échap** (clavier) ou **BACK** (manette) quitte un mode et revient au menu |

```
py -3 tools/patch_moteur.py --resolution 1280 720 --langue --logo-japonais \
    --dural --wxga --dural-grille --mode 0 --menu-init --menu-ranking \
    --transition-game --joueur2 --menu-fermer
```

Lanceur unique : `tools/console_combat.cmd`.

## Les huit maillons

| # | ce qui manquait | où |
|---|---|---|
| 1 | le menu ne demandait jamais le mode GAME | `0x1801DDF86` → caverne |
| 2 | la fin du sélecteur ramenait au menu | `0x1800DB399` |
| 3 | **l'objet de session n'était créé par personne** | caverne |
| 4 | après le combat, on partait au titre | `0x1800DA9EC` |
| 5 | OFFLINE VERSUS n'enregistrait que ses réglages | `0x1801DEB12` |
| 6 | le menu restait allumé sous le combat | `0x1800DCB95` |
| 7 | DOJO demandait son mode mais pas son sous-état | `0x1801DDA61` |
| 8 | aucune touche pour sortir d'un mode | `0x1800DA9E3`, `0x1801E4E6E` |

Plus `--joueur2` : le lecteur d'entrées ne lisait qu'un joueur.

## La leçon de méthode qui s'est payée trois fois

**`.pdata` ne liste pas les fonctions feuilles.** Trois fois ce trou a coûté :

1. une fonction prise pour une entrée `.pdata` alors qu'elle en couvre plusieurs
   chaînées (le menu, la première fois) ;
2. la feuille `0x1800B1D30` qui plantait, invisible aux cartes ;
3. l'affirmation « personne ne demande le mode CS_TRAINING », fausse : le
   demandeur `0x18019C3D0` est une feuille à saut terminal.

Quand la conclusion est « personne ne fait X », il faut le **balayage linéaire**
de `.text` par motif d'octets, jamais l'itération sur `.pdata`. Compte exact
ainsi obtenu : 28 sites de demande de mode, 41 de sous-état.

## Ce qui reste

TERMINAL, OPTION, SCOREBOARDS, DLC : pages identifiées, jamais ouvertes.
ONLINE est mort (mode 7 bouchonné aux trois gestionnaires). Et **90 % de la
surface console reste non lue** — `analysis/couverture_console.md`.

La caverne de `.text` est pleine à 136 octets sur 164 : le prochain maillon
devra trouver de la place ailleurs.

## 2026-09-05 — le décor TERMINAL : deux index, pas un

Le décor de l'écran customize se demande **deux fois**, avec deux immédiats
distincts dans `STAGE_TASK` (`0x1801C4D60`) :

    0x1801C4DA6  mov ecx,1 ; call 0x18018FCF0   la GEOMETRIE  (jamais patchée avant)
    0x1801C4DCB  mov ecx,1 ; call 0x1800D7130   l'ÉCLAIRAGE   (le seul patché jusqu'ici)

`0x1800D7130` ne charge que `./rom/ibl` + `./rom/light_param` : les trois essais
« sans différence » ne mesuraient donc rien. `0x18018FCF0` est une feuille,
trouvée par balayage linéaire ; elle écrit `+0x60` du gestionnaire de décor
(singleton `0x1807499D8`, descripteurs `0x180403430 + i*0xF0`, 41 entrées,
index 26 = `STGTRM`).

R.E.V.O. a la même tâche, identique cas par cas — la borne ne diverge pas du
PC ; mais l'essai `trm` sur la géométrie reste à faire.

`--decor-perso` patche désormais les **deux** octets. Vérifié statiquement :
les deux sites portent `b9 1a 00 00 00`.

    tools\decor_perso.cmd trm      pour essayer
    tools\decor_perso.cmd ts2      pour revenir

Détail complet : `analysis/menu_console.md` §15.10.

## 2026-09-05 — EXIT GAME dans le menu

L'entrée existait : libellé `0x183`, dialogue `EXIT_CAUTION`, chemin de
validation intact (`0x1801DCEF8 cmp dword [rdi+0x58], 9`). Le moteur la met à
l'état « normal » puis la **recache** deux instructions plus loin, et ne compte
que neuf entrées.

Deux sites, sans toucher à la caverne (toujours 136/164) :

    0x1801E3A19   02 -> 00                     l entree 9 est dessinee
    0x1801DCF0E   drapeau+saut -> ExitProcess  la sortie du processus

**Piège** : `[page+0x224]` n'est pas un compte mais le **dernier indice** — la
boucle de dessin va de 0 à lui INCLUS (`0x1801E1079 cmp edi,[rsi+0x224]` /
`jle`). Le porter de 9 à 10 ajoute une onzième rangée qui lit le tableau de
libellés hors bornes et affiche `Enter`. Ne pas y toucher.

Le moteur n'a aucune sortie native (sur borne, l'hôte coupe) ; on appelle
`ExitProcess`, déjà importée (IAT `0x180346318`).

Option `--menu-exit`. Lanceur : `tools\console.cmd` (build complet).
Détail : `analysis/menu_console.md` §16.

## 2026-09-05 — sous-menus : le défaut était notre propre patch

`--menu-ranking` (2026-09-04) neutralisait le `jne` de `0x1801DC650`, qui est
**la garde partagée** par tous les sous-menus du menu console. Résultat : le
menu principal lisait les directions sous chaque sous-menu.

`--sousmenu` le remplace, en trois sites :

    0x1801DCE2C   le rangement de la page RANKING -> sept nop   (la vraie cause)
    0x1801DC650   le `jne` est RENDU (on n applique plus --menu-ranking)
    0x1801DC649   call 0x180244EA0 -> call 0x180244F90

Aucune caverne (toujours 136/164). Trois prédicats essayés : « la scène
joue-t-elle ? » (d'origine, trop court), « la sous-page s'en va-t-elle ? »
(`+0x60`, jamais relâché — le menu restait bloqué au retour), et « la scène
existe-t-elle ? » — celui du moteur, déjà utilisé sur le même objet en
`0x1801DD01A`.

**Valide a l'ecran le 2026-09-05.**

Mesure : `tools/pister_sousmenu.cmd`, bilan dans
`analysis/pister_sousmenu_bilan.txt`. Détail : `analysis/menu_console.md` §17.

## 2026-09-05 — l'écran épilepsie : constats, rien n'est livré

L'écran d'avertissement **est l'écran de chargement**, sous-état
`DATA_INITIALIZE` (et non `WARNING`, fausse piste démentie à l'écran).
Singleton `0x180677040`, vtable `0x18034CB90` :

    +0x10  0x18006B880   douze phases sur [obj+0x58] -- vrai chargement
    +0x20  0x18006C490   dessin du texte 0x36C, a partir de la phase 4

Vérifié à l'écran : **le texte seul peut partir** — douze octets à
`0x18006C4B6`, saut vers l'épilogue `0x18006C803` (garder le prologue, il
restaure `rbx`, `xmm6`, 0x110 octets de pile). Il reste alors un écran blanc,
la scène AET démarrée en `0x18006C9E2` ; retirer ce fond a été essayé puis
**annulé**, rien n'établit ce que l'écran doit devenir.

`--sans-epilepsie` (texte seul) et `--sans-avertissement` (le sous-état
WARNING) existent dans le patcheur mais **ne sont dans aucun lanceur**. Le
build livré garde l'écran d'origine. Détail : `analysis/menu_console.md` §18.

## 2026-09-05 — le réseau : le netcode de bornes liées est intact

Question de Frédéric, à partir de YAMPnet puis de R.E.V.O. Relevé statique :

- **R.E.V.O.** porte un rollback (`AVTaskRobRollback`, `AVIoRollbackCtrl`,
  `AVRollbackTraceUnit`) et un appariement EOS. **Rien de tout ça dans APM3** :
  zéro `Rollback`, zéro `EOS_`, zéro `SteamAPI`, ni dans le moteur ni dans
  `vfes.exe`. Absent, pas bouchonné.
- **APM3 porte le netcode de bornes liées, entier** : 23 classes `AVLink*` et
  `AV*Packet*`, du démarrage (`Startup`) à la fin de partie (`PlayEnd`,
  `CleanupMatch`) en passant par l'appariement complet et la phase de combat
  (`Playing`), avec un fil de réception et un médiateur de paquets.
- **Le transport est câblé** : le moteur importe quatorze fonctions de
  `ws2_32`. `vfes.exe` n'en importe aucune.
- **Le déterminisme est prouvé par le jeu** : il sait rejouer un combat
  (`AVTaskGameVsReplay`, `AVTaskRobShortReplay_Rec`, `TERM_REPLAY_BUF`).

Conclusion : la piste n'est ni de transplanter R.E.V.O. (pas de plan de coupe,
et du code de SEGA à recopier), ni d'écrire un lockstep de zéro, mais de
**réveiller ce qui est déjà là**. C'est aussi ce que fait YAMPnet pour les jeux
conçus comme deux cabinets reliés : il tunnelise leur protocole natif.

Détail et ordre de travail : `analysis/reseau.md`.


## 2026-09-07 — KNOCK OUT TRIAL : il est là, sous le nom de Special Sparring

Question de Frédéric : le mode arcade `KNOCK OUT TRIAL SPECIAL` existe-t-il
encore dans le code ?

**Oui.** La chaîne complète a été lue, appel par appel :

- `kotrial_enemy_data.txt` est **dans le `.par`** (303 079 o) et **peuplé** :
  171 adversaires avec leur IA, **16 équipes `kotsp_team`** (le « SPECIAL »),
  10 aires, 4 zones, 28 rôdeurs, les intrus, le PNJ du dojo ;
- son analyseur est dans le moteur : classe **`GmKotDat`** (RTTI), chargeur
  `0x1800993E0`, analyseur `0x180099450` (12 158 o), déclenché à l'entrée du
  **TERMINAL** (`0x18006C2C4`) ;
- les libellés anglais sont dans `string_array` : `Special Sparring` (0x1A1),
  `Team Select` (0x1C8), `All teams have been defeated!` (0x1CA), les vingt
  noms d'équipes 0x592B–0x593E dont **`KOT Trial`**, et le roster complet
  (nom + deux répliques par adversaire) ;
- l'écran **`TaskMenuTeam`** pose le mode de jeu **3** (`0x1801A4252`) ;
- et le constructeur de match `0x1800B8540` va chercher son adversaire dans la
  table `0x18040B650` (pas 0x8E) via `0x1801A53A0`, au format `kot_enemy`.

Ce qui a été **retiré du portage PXD** (absent aussi de R.E.V.O., donc coupé au
portage, pas sur la borne) : les six tâches d'affichage du Lindbergh
(`TaskKoTrialDefeatDisp`, `IntrudeDisp`, `AdviceDisp`, `KoDisp`…), l'écran
titre `KNOCKOUT TRIAL`, les curseurs `p_trial_cursor01..10_lt`, et le journal
`kot_special_mode %d`. Le cœur reste, l'habillage est parti.

Détail : **`analysis/knockout_trial.md`**. Données extraites :
`extracted/kotrial_enemy_data.txt`, `extracted/kotrial_structure.txt`.

## 2026-09-07 — les décors : sélection et chargement, désassemblés en entier

**Le piège d'abord** : `0x1800D7130` n'est pas « le chargeur de décor », c'est
le poseur d'**éclairage** (`ibl` + `light_param`), sur la table de codes à trois
lettres `0x18039F7A0`. La **géométrie** passe par une autre table,
`0x180403430`, **41 descripteurs de 0xF0 octets**. Deux index, deux chemins.

- **`TaskStage`** (RTTI, vtable `0x180408210`, singleton `0x1807499D8`) :
  `+0x58` l'état (0 → 5), `+0x5C` le décor courant, `+0x60` le décor demandé,
  `+0x68` le descripteur. Update `0x18018EF40`, chargeur `0x18018F680`,
  déchargeur `0x18018F230`.
- **Le descripteur** est entièrement cartographié : objset (`+0x10`), collision
  (`+0x48`), `auth_3d` (`+0x00`, `+0x08`), les **neuf variantes de musique**
  (`+0x70`…`+0xB0`, c'est le `Stage BGM Type` du menu), caméra et sons.
  Mis à plat dans `analysis/table_decors.csv` (`tools/table_decors.py`).
- **`0x18018FCF0(index)` est le SEUL demandeur de décor**, et il n'a que
  **trois** appelants : le combat (`0x1800BC5E0`), l'écran Customize
  (`0x1801C4D60`, index en dur) et la démo (`0x180203550`).
- **L'index vit dans les paramètres de partie, `+0x4C`** ; sa valeur de repos
  est **`0x29` = 41 = aléatoire** (`0x1800B56C0`), refusée par `0x18018FCF0`.
- **En solo, le décor est celui de l'adversaire** : `0x1800AF400(perso)` lit
  une table *(personnage, décor)* que **`rom/game_score.txt`** fournit en clair
  (`score.chara.<n>.stage=STGDJO`, 21 entrées), plus les trois routes.
  Extrait dans `extracted/game_score.txt`. **Éditable sans patcher le code.**
- **`TaskSelStage`** (vtable `0x180400A18`) construit une liste de 27 entrées :
  index 4→0x14, 0x15→0x19 (les cinq Dural sous un seul calque), 0x27, 0x28, et
  `0x29` = *Random*, résolu **dans l'écran** (`0x18017474E`) avant d'atteindre
  la tâche. Les 17 décors d'essai sont dans la table mais pas dans la liste.
- L'autorisation « Stage select » est le **bit 1 du dword `0x18066B8E8`**
  (`Wrap_allow_stage_select`, `0x180046960` / `0x180046970`).

Détail : **`analysis/decors.md`** (le document qui fait foi pour le code des
décors ; `decors_vf5r.md` et `import_decors.md` restent ceux des fichiers).
Désassemblages bruts : `analysis/disasm_decors_{A,B,C,D}.txt`,
`disasm_selstage.txt`, `disasm_match_setup.txt`.

Outils ajoutés : `tools/refs_multi.py` (toutes les références de N cibles en un
seul balayage), `tools/ecrit_champ.py` (qui écrit dans `objet+N`),
`tools/immediat.py`, `tools/bornes.py`, `tools/hexva.py`,
`tools/zone_chaines.py`, `tools/chercher_motif.py`, `tools/table_decors.py`.

## 2026-09-07 (2) — les cinq décors de Dural : le choix était un bouchon

Le décor d'un combat solo est le **décor maison de l'adversaire**
(`rom/game_score.txt`), demandé par `0x1800AF400(personnage)` — qui n'a **qu'un
seul appelant**, `0x1800B8AFA`, dans le constructeur de match. Et juste après :

    0x1800B8B02  cmp  eax, 0x15        ; 21 = du1, le decor de Dural
    ...
    0x1800B8B1C  call 0x1800B2330      ; le choix parmi les cinq
    0x1800B8B21  mov  r12d, eax

`0x1800B2330` fait six octets : `mov eax, 0x16 ; ret` — **toujours DU2**. Un
bouchon de plus, un seul appelant, argument ignoré. Les cinq décors de Dural
sont dans le jeu, entiers, chargés par le chemin ordinaire ; **un seul était
atteignable**.

**`--decors-dural [premier]`** (lanceur **`tools\decors_dural.cmd`**) réécrit le
bloc `0x1800B8B02`–`0x1800B8B20` en place, 31 octets, **sans caverne** :

    cmp eax, lo ; jl fin ; cmp eax, lo+4 ; jg fin ; add eax, 21-lo ; fin: jmp

Par défaut `lo = 7` : **cas riv jin sin djo → du1 du2 du3 du4 du5**, soit les
décors maison de Lion, Shun Di, Aoi, Lei-Fei et Akira. En OFFLINE VERSUS, un
combat par décor ; en Arcade route A, les cinq dans une seule partie
(combats 3, 4, 6, 7 et 8 — le combat contre Dural rend désormais DU1, le
bouchon n'étant plus appelé).

Deux précautions qui ne sautent pas aux yeux, et qui sont dans le commentaire du
patcheur : `0x1800B8B21` (`mov r12d, eax`) est **préservé** parce que la voie
License Challenge y saute depuis `0x1800B8A2D` — l'écraser aurait cassé ce mode
en silence, exactement la collision du 2026-09-06 ; et la traduction agit
**avant** que l'index ne devienne le décor courant, donc les cas particuliers
indexés (8 et 9, 16 et 40) ne se déclenchent pas sur les décors traduits.

Vérifié statiquement : le bloc se redésassemble exactement comme prévu, et la
ligne de patch complète du build console passe sans collision.

## 2026-09-07 (3) — ajouter un décor : l'identifiant est une DONNÉE

Le verrou supposé — « l'identifiant d'objset est câblé dans le moteur » — est
faux, et c'est mesuré. `0x1800F9450` cherche l'identifiant par **dichotomie**
dans un vecteur construit au démarrage par `0x18006B7E0`, à partir de :

    0x1800F9803  "./rom/objset/"
    0x1800F981A  "obj_db.bin"

`rom/objset/obj_db.bin` (1,1 Mo, extrait dans `extracted/obj_db.bin`) : en-tête
de 0x20 octets, pot commun de chaînes, puis une table de **0x24 octets par jeu
d'objets** — `{offset du nom, IDENTIFIANT, obj.bin, tex.bin, .farc}`.

Les 43 entrées `STG*` recoupent le descripteur du moteur **une par une**, y
compris les trois qui cassent la suite : `STGDU5 = 5529`, `STGGYM = 2847`,
`STGSMO = 2848`, et l'identifiant 29 n'est attribué à personne. **L'identifiant
n'est pas la position, l'espace est troué, il accepte des valeurs hautes.** Ces
trois décors ont été ajoutés après coup exactement comme on voudrait le faire.

Cinq autres bases suivent la même logique (`tex_db`, `spr_db`, `aet_db`,
`auth_3d_db`, `mot_db`).

Et l'inventaire des tables indexées par le décor a été fait : **onze sites,
tous bornés**. Contrairement au chantier 3SX, passer de 41 à 42 décors demande
de lever des bornes identifiées, pas de deviner où ça plantera. La voie courte
reste de **recycler l'un des 17 emplacements d'essai** (`tst ts2 ts3 wht trm cid
trs evo00..evo09`) : aucune borne à toucher.

Recette complète : **`analysis/ajouter_un_decor.md`**.

Réserve honnête : `TaskSelStage` (l'écran de sélection de décor) est construit
au démarrage par la même fabrique que la page `CHAR SELECTOR` — laquelle est
construite et **jamais affichée**. Rien ne prouve encore que celui-ci soit
piloté ; c'est pourquoi le build d'essai ne repose pas sur lui.

Outils ajoutés : `tools/cavernes.py` (bourrages `int3` prouvés libres, avec la
condition de frontière à 16 qui manquait).

## 2026-09-07 (4) — TaskSelStage EST piloté : la réserve est levée

La séance précédente laissait une réserve : *« rien ne prouve que `TaskSelStage`
soit piloté, il est construit par la même fabrique que `CHAR SELECTOR` qui,
elle, n'est jamais affichée »*. **Elle est levée, et elle était fausse.**

`TaskSelStage` n'est pas un singleton : il est **membre**, à `+0x3B0`, de
**`TaskSelector`** (RTTI, vtable `0x1803FEFD8`, singleton `[0x180714928]`) —
c'est-à-dire l'objet que `machine_console.md` §5 avait déjà mesuré vivant
(1326 passages sur son gestionnaire de milieu).

Et il est **enregistré comme tâche**, exactement comme `TaskStage` :

    0x18016CC6C  lea  rcx, [rbx + 0x3b0]      ; le TaskSelStage embarque
    0x18016CC73  lea  rdx, "SEL_STAGE"
    0x18016CC7A  call 0x180245830             ; Task::Append(nom)

`0x180245830` est le même appel que `0x18018FB20("STAGE")` fait pour
`TaskStage` (183 sites dans le binaire). Le site d'enregistrement, `0x18016CC30`,
est appelé depuis `0x18016C8CE` — **à l'intérieur de `TaskSelector::update`**,
donc sur le chemin vivant. Une fois la tâche inscrite, le gestionnaire l'anime
par sa vtable, donc **`0x180174250` tourne** : la navigation du curseur, la
grille d'icônes et les deux tables `0x180400210` / `0x1804004B0` sont vivantes.

Méthode : balayage de toutes les prises d'adresse `lea r?, [r? + 0x3B0]`
(19 sites, tous dans la famille `0x18016Cxxx`) plus `refs_multi --plage` sur
tout `TaskSelStage`. Confiance : **CONFIRMED**.

### Et un DEUXIÈME bouchon Dural, du côté de l'écran

`TaskSelector::update` appelle chaque trame `0x180175320(TaskSelStage*)` :

    0x180175330  call 0x1801749F0        ; le decor choisi
    0x180175335  mov  [rbx+0x60], eax
    0x180175338  cmp  eax, 0x15          ; 21 = du1
    0x18017533B  jne  suite
    0x18017533D  mov  dword [rbx+0x60], 0x16   ; 22 = DU2, EN DUR
    0x180175344  mov  dword [rbx+0x5c], 0x16   ; 22 = DU2, EN DUR

Même substitution que `0x1800B2330`, mais sur l'écran de sélection. **Deux
verrous indépendants forçaient DU2** ; `--decors-dural` ne touche que le
premier. Le second reste à traiter si l'on veut choisir DU1..DU5 dans la
grille.

## 2026-09-07 (5) — les décors des trois générations Lindbergh, extraits

Extraction complète dans **`extracted/decors/`**, table dans
**`analysis/decors_lindbergh.csv`**, outil **`tools/inventaire_decors.py`**,
document **`analysis/decors_lindbergh.md`**.

| dossier | jeu | identification |
|---|---|---|
| `VF5_VERB` | **VF5 ver.B** | `gameid=SBLM`, build `overseas_edition/20070530`, chaînes `vf5verB_jng*` |
| `VF5R` | VF5 R | 2008-06-16 |
| `VF5FS_LIND` | Final Showdown Rev A | release 2.000, 2010-06-28 |

420,6 / 519,6 / 539,9 Mo, rangés à l'identique
(`objset/ auth_3d/ coli/ ibl/ light_param/`).

**`Virtua Fighter 5.7z` n'était pas inventorié** — `SOURCES.md` donnait
`VF5_ARCADE` pour absent. C'est bien un dump Lindbergh de VF5 vanilla ver.B.

**La découverte : `stgdur.farc`, 35,7 Mo, dans ver.B uniquement.** Le plus gros
objset de tout le corpus, et il n'existe dans aucune version ultérieure. En
ver.B, **un seul** décor de Dural entier, et `du1`…`du4` réservés mais vides
(225–486 Ko) ; en R, `dur` disparaît et les quatre se remplissent ; en FS un
cinquième s'ajoute. **Le décor de Dural a été découpé en quatre puis en cinq.**
C'est le seul contenu réellement absent d'APM3 — la cible naturelle d'un import.

`decors_vf5r.md` concluait *« le décor DUR n'est pas un décor, c'est un jeu
d'effets »* : juste pour R et FS, faux en général. Deux autres corrections :

* `import_decors.md` §5 affirmait les 41 objsets identiques entre FS Lindbergh
  et APM3. **Quarante sur quarante et une** : `stgjin.farc` fait 21 886 056 o
  côté Lindbergh et 21 871 895 o côté APM3, **14 161 octets d'écart**.
* `import_decors.md` §7 affirmait que VF5 R n'a pas d'`auth_3d/STGDJO.farc`.
  Il l'a : 37 811 octets.

Et le conteneur ne bouge pas de 2007 à 2011 — mesuré sur les quatre
générations : `FArC`, en-tête `0x3A`, `<nom>_obj.bin` + `<nom>_tex.bin`.

Piège de disposition : un décor est à cheval sur DEUX images, et pas dans le
même sens selon le jeu. R : géométrie sur `vf5r.bin`, reste sur `vf5r_rom.bin`.
FS : géométrie sur `vf5fs_ext.bin`, reste sur `vf5fs.bin` (`disk0` n'est qu'un
arbre de liens symboliques).

## 2026-09-07 (6) — les décors de Dural marchent, et le bouchon était TRIPLE

**Frédéric, à l'écran : « les décors de Dural fonctionnent ».** `--decors-dural`
est validé.

En allant patcher le second verrou, il s'est avéré qu'il y en avait **trois**,
pas deux. La substitution « du1 → du2 » est une **politique**, appliquée à trois
endroits indépendants :

| site | contexte | forme |
|---|---|---|
| `0x1800B2330` | le combat | bouchon `mov eax, 0x16 ; ret` |
| `0x18017533D` / `0x180175344` | l'écran (`0x180175320`) | deux `mov` immédiats |
| `0x1801753A8` | le chemin APM3 (`0x180175390`) | un `cmove eax, ecx` |

Les deux derniers encadrent le même tirage : **`0x1801749F0` est le tireur
aléatoire de décor**. Il parcourt exactement la grille d'icônes
(`0x180400218`, pas `0x20`, borne `0x2A0` = 21 cases), saute la case ALÉATOIRE
(`0x29`), saute ce que désigne la table d'exclusion `0x180400770` — **qui vaut
`-1`, donc n'exclut rien** — et saute ce qui a déjà été tiré (marqueurs dans un
tableau de 0x29 octets, remis à zéro quand le sac est vide). Autrement dit :
**du1 est bien dans le tirage, et les deux sites le remplacent après coup.**

L'hypothèse « du2 est forcé parce que du1 ne marcherait pas » est écartée : le
premier correctif fait passer le combat contre Dural par du1, et Frédéric l'a
vu tourner.

**`--decors-dural-grille`**, ajouté au lanceur `tools\decors_dural.cmd` :

* `0x18017533B` : le `jne` devient un `jmp` — **un octet** ; le bloc de
  substitution devient inatteignable et `[+0x5C] = eax` s'applique toujours ;
* `0x1801753A8` : le `cmove` devient trois `nop` ;
* quatre cases de la grille passent de riv/jin/sin/djo à du2/du3/du4/du5 ; la
  case `dur` garde du1, donc **les cinq y sont, sans doublon** :

      ligne 0 :  are   nyc   slk   DU4   cas   DU2   smo
      ligne 1 :  tak   bar   DU5   ALEA  DU3   ter   ban
      ligne 2 :  hai   tan   gym   yuk   aur   umi   DU1

Les **icônes** des quatre cases ne changent pas (`stage_icon_sin_c`,
`_riv_c`, `_djo_c`, `_jin_c`) : c'est voulu, c'est ce qui permet de dire quelle
case on a prise. L'aperçu, lui, montre l'habillage `dur` pour les cinq — la
liste de `0x180174BF0` associe déjà `dur`/`dur_stay` aux indices `0x15`–`0x19`,
il n'y avait rien à ajouter de ce côté.

Tout est en place, aucune caverne, aucune collision. Vérifié au
désassemblage ; **la grille elle-même n'a pas encore été vue à l'écran**.

## 2026-09-07 (7) — la grille s'affiche, et l'essai trouve un défaut d'origine

**La grille s'affiche.** Capture de Frédéric : l'écran `STAGE SELECT`, trois
lignes de sept cases, aperçu en haut, grille en bas. La réserve sur
`TaskSelStage` est définitivement close — la tâche est inscrite **et** dessinée.

Ses trois observations, et ce que chacune a donné.

### « DU1 est identique à DU2 »

**Sur l'écran de sélection, c'est normal et inévitable** : l'aperçu ne vient pas
du décor mais de la liste de `0x180174BF0`, qui associe la même planche AET
`dur`/`dur_stay` aux indices `0x15` à `0x19`. La légende « Sanctuary / Single
Wall 16x16 » est **peinte dans cette planche** — elle n'est pas un libellé
(recherche dans `string_array` : aucun résultat pour « Sanctuary », « Deep
Mountain », « Single Wall »). Les cinq décors de Dural partagent donc un seul
aperçu, par construction.

**En combat, ils ne devraient pas l'être** : `objset` 30 contre 31,
`stgdu1.farc` 27 229 016 octets contre `stgdu2.farc` 24 144 242. Reste à voir.

### « en ring out, le personnage est sur un sol qui n'existe pas »

C'est un **défaut du build d'origine**, pas de nos correctifs. Le descripteur de
du2 (`0x1804048D0`) pointe sa collision sur **`rom/STGDU1_COLI.000.bin`** —
celle de du1. Trois faits le qualifient :

* `STGDU2_COLI.000.bin` **existe dans le `.par`** : 3 984 octets, contre 5 744
  pour celle de du1. Deux tailles, donc deux formes de sol ;
* la chaîne `rom/STGDU2_COLI.000.bin` **n'existe nulle part dans le binaire** —
  elle n'a jamais été émise à la compilation ;
* du2 est dans le même sac que `trm`, `cid` et `trs`, les trois décors d'essai
  qui prennent la collision de du1 faute d'en avoir une.

**`--du2-collision`** écrit la chaîne manquante dans le **mou de fin de
`.rdata`** (`0x180641B56`–`0x180641C00`, 170 octets à zéro, compris dans
`SizeOfRawData` donc projeté en mémoire — même mécanique que la caverne de fin
de `.text` déjà employée en `0x18034575C`), puis repointe `desc+0x48`. Aucune
caverne `int3` ne convenait : la plus grande fait 21 octets, il en fallait 24.

### « l'icône du bas est toujours celle du stage d'origine »

Exact, et c'était mon choix — il permettait de repérer la case prise. Mais
puisque l'aperçu du haut est **le même pour les cinq**, l'icône d'origine ne
distinguait rien de plus que la position : elle ne faisait que contredire
l'aperçu. **`--decors-dural-icones`** met les quatre cases sur
`stage_icon_dur_c`. Les cinq ne se distinguent plus que par leur position.

Les deux options sont dans `tools\decors_dural.cmd`, chacune retirable seule
pour comparer. Vérifiées sur le binaire patché ; **pas encore vues à l'écran**.

## 2026-09-07 (8) — `--decors-dural-icones` : une erreur, trois symptômes

Frédéric, après essai : « très mauvais patch : les icônes sont toujours les
mêmes, seul DU1 est sélectionnable, le curseur saute toutes les autres versions
de décor de Dural, et DU1 est remplacé par DU4 ou 5 ».

**Les trois symptômes viennent d'une seule ligne, et j'avais mal lu un champ.**

J'avais pris le champ `+0x18` d'une case de grille pour « le nom de l'icône à
dessiner » et je l'avais fait pointer, sur quatre cases, vers
`stage_icon_dur_c`. Ce n'est pas une icône : c'est **le sprite d'ANCRAGE qui
donne à la case sa position à l'écran**. Le constructeur de grille
`0x180173BD0` le lit ainsi (`rsi = table + 4`, donc `[rsi+0x14]` = case+0x18) :

    cmp  qword [rsi+0x14], 0            ; pas d'ancre -> position INTERPOLEE
    je   0x180173DAC
    call 0x1800298B0(buf, [rsi+0x14])   ; resout le sprite par son NOM
    vmovsd xmm0, [rax+0x40]             ; -> x, y REELS du sprite
    vmovsd [r14+rdi+8], xmm0            ; la position de la case

Quatre cases pointant sur le même sprite reçoivent donc **les mêmes x et y** :
cinq entrées empilées au même endroit. Le curseur n'en atteint qu'une (« seul
DU1 est sélectionnable »), les autres sont injoignables (« le curseur saute »),
et la sélection de cette position rend n'importe laquelle des cinq (« DU1 est
remplacé par DU4 ou 5 »). Quant aux icônes, elles n'avaient aucune raison de
changer : **elles sont peintes par la scène AET `SEL_STAGE`**, pas par cette
table.

L'option est **retirée**, et `patch_moteur.py` la **refuse explicitement** —
elle traîne encore dans les vieux lanceurs, un abandon silencieux serait pire.

Ce qui reste, et qui n'a rien à voir : `--decors-dural-grille` ne touche que
`+0x08`, l'indice de décor, que le constructeur de grille ne lit pas du tout
(il ne lit que `+0x00` colonne, `+0x04` ligne, `+0x18` ancre). Vérification sur
le binaire reconstruit, décor/ancrage case par case :

    ligne 0 : are/are  nyc/nyc  slk/slk  du4/sin  cas/cas  du2/riv  smo/smo
    ligne 1 : tak/tak  bar/bar  du5/djo  ALEA/rnd du3/jin  ter/ter  ban/ban
    ligne 2 : hai/hai  tan/tan  gym/gym  yuk/yuk  aur/oro  umi/umi  du1/dur

Le décor change, l'ancrage ne bouge pas. **Conséquence à assumer : les cinq
cases de Dural garderont l'icône et le nom du décor d'origine.** Les changer
demande de toucher aux données 2D du `.par` (`spr_db`, `aet_db` et la planche
de sprites) — un autre chantier.

**La leçon, et elle est générale** : un champ qui *ressemble* à un nom de
ressource peut être une **position**. Le nom ne dit pas le rôle ; seul son
consommateur le dit. Je n'avais pas lu `0x180173BD0` avant de patcher — c'est
exactement le défaut que `reference_coherence_nest_pas_role` décrit.

## 2026-09-07 (9) — le QUATRIÈME site : « DU1 = DU2 » enfin expliqué

Frédéric, après le correctif de la grille : le curseur atteint bien les cinq
cases, le ring out sur DU2 charge bien sa vraie collision, **mais DU1 = DU2**,
et « il manque le décor de Dural qui se déroule de nuit ».

D'abord la vérification qui écarte la fausse piste : les deux décors ont bien
des données d'éclairage distinctes. `light_du1.txt` et `light_du2.txt` sont
tous deux dans le `.par`, et ils diffèrent sur **huit lignes sur cinquante-neuf**
— positions de lumières, `diffuse 0.5` contre `1.0`, `ambient` différent. Deux
décors qui chargent ça ne peuvent pas se ressembler. Le problème n'était donc
pas dans les données.

**Il restait un quatrième site de substitution, et c'était le décisif** :

    0x18017448A  mov r8d, [rbx+0x5c]     ; le decor selectionne
    0x18017448E  cmp r8d, 0x15           ; 21 = du1
    0x180174492  jne suite
    0x180174494  mov r8d, 0x16           ; 22 = du2
    0x18017449A  mov [rbx+0x5c], r8d     ; ... et on l'ECRIT

Il est dans **`TaskSelStage::update` elle-même** (`0x18017425E`), et c'est lui
qui décidait du décor réellement chargé. Les trois autres agissaient en amont
ou sur des chemins annexes ; celui-là écrasait le résultat.

Correction : on ne détourne pas le saut, on change **l'immédiat**, `0x16` →
`0x15`. Le bloc s'exécute à l'identique et rend du1 à du1 — aucun flot modifié,
aucune instruction morte, **un octet**. C'était la forme la plus sûre, et
c'est celle qu'il aurait fallu prendre pour les trois autres.

### La leçon, et l'outil qui en sort

J'ai cherché ces sites **un par un**, au fil des symptômes : trois trouvés, un
manqué, et il a fallu un essai de Frédéric pour le révéler. Une substitution
« du1 → du2 » a une forme reconnaissable : une comparaison à la source suivie,
quelques instructions plus loin, d'un immédiat égal à la cible.

**`tools/substitutions.py <source> <cible>`** énumère ces sites d'un coup. Sur
le binaire d'origine, `0x15 0x16` en rend **quatre** (plus un faux positif, une
borne de boucle `cmp rax, 0x16`). Les quatre d'un seul coup, là où trois
séances de lecture ciblée en avaient laissé un.

C'est la même leçon que `feedback_cartographier_la_zone` : la zone entière d'un
coup, pas le site que le symptôme désigne.

## 2026-09-07 (10) — les cinq Dural identifiés, par leurs NOMS D'OBJETS

J'ai d'abord voulu identifier les cinq décors de Dural par leur **éclairage**
(`light_param/*.txt`, en clair). J'ai conclu « du5 = la nuit » : brouillard
noir, diffuse `0.07 0.08 0.16`. **Faux.** Frédéric : « du5 se passe dans
l'espace, rien à voir ». Un ciel noir bleuté, c'est l'espace autant que la
nuit — la couleur ne distingue pas les deux.

Ce qui les distingue, ce sont les **objets**. Les `stgdu*_obj.bin` portent leurs
noms en clair ; il suffit de les extraire (`tools/farc.py extract`) et de
chercher `hosi` (星), `kumo` (雲), `star`, `sky`, `mars` :

| décor | case de la grille | objets qui le nomment |
|---|---|---|
| du1 | Sanctuary (l.3 c.7) | `sky10` … `sky23` — beaucoup de couches de ciel, **aucune étoile** |
| **du2** | **River (l.1 c.6)** | **`R4S1CGZ_hosi`, `stgdu2_eff_hosi_000/001`, `CGZ_kumo`, `stgdu2_eff_kumo_000/001`** → **NUIT ÉTOILÉE** |
| du3 | Shrine (l.2 c.5) | `CGZ_sky`, `stgdu3_sky` — ciel simple |
| du4 | Deep Mountain (l.1 c.4) | `sky3_cloudy_weather2/3`, `stgdu4_eff_sky_dome` — nuageux |
| du5 | Statues (l.2 c.3) | `mars_CGZ_sky`, `CGZ_star1/2/3`, `star_all_00` → **ESPACE / Mars** |

Et le `stgdur.farc` de VF5 ver.B **n'a aucun objet de ciel** — ce n'était donc
pas une version de nuit non plus.

**L'ironie** : le décor de nuit étoilée est `du2`, c'est-à-dire exactement celui
que les quatre bouchons forçaient partout. Frédéric le voyait donc *toujours*
avant les correctifs ; maintenant que les cinq sont distincts, il est sur une
case qui ne l'annonce pas (« River »).

**Et on sait enfin POURQUOI le moteur forçait du2.** R.E.V.O. range ses décors
en `.par` nommés : `st_vf5_sanctuary1.par` … `sanctuary5.par`. Seul
**`sanctuary2` fait 40 Mo ; les quatre autres sont des souches de 190 Ko.**
Les cinq Dural s'appellent donc « Sanctuary 1 à 5 », et dans les portages
modernes un seul est réellement livré — le deuxième. La substitution
« du1 → du2 » n'était pas un bouchon oublié : c'est la trace d'une décision de
portage, appliquée à quatre endroits. **APM3, lui, a les cinq en entier**
(24 à 28 Mo chacun) — c'est ce qui rend le correctif possible.

Leçon d'outillage : `tools/ambiances.py` classe tous les décors par ambiance
lumineuse (utile, mais il ne distingue pas nuit et espace), et c'est le
balayage des **noms d'objets** qui a tranché. Une couleur se déduit ; un nom se
lit.

## 2026-09-07 (11) — les cinq Dural, identifiés pour de bon

Deux identifications fausses avant celle-ci : « du5 = la nuit » (déduite du
brouillard noir — c'était Mars), puis « du2 = la nuit étoilée » (déduite des
objets `hosi`/`kumo` — c'est le décor en ÉRUPTION, qui a aussi des étoiles).
Frédéric a corrigé les deux à l'écran. La leçon tient en une ligne : **un décor
ne s'identifie ni par sa couleur ni par un mot-clé isolé, mais par l'inventaire
de ses objets.**

Empreinte complète, lue dans les `stgdu*_obj.bin` et les `EFFSTGDU*.farc` :

| décor | case | objets qui le caractérisent |
|---|---|---|
| du1 | Sanctuary | `MZ_saidan` (autel), `MZ_iseki` (ruines), `BMZ_mizu` (eau), et **24 objets de ciel : `sky`, `sky10` … `sky32`** |
| du2 | River | `CGZ_gouka1` (豪火), `R4S1CGZ_funka_a/b` (噴火, éruption), `MZ_inseki` (隕石, météore), `MZ_hi` (feu), `STGDU2_EFF_FIRE`, `STGDU2_EFF_KEMURI` (fumée), plus `hosi` et `kumo` → **le décor en éruption** |
| du3 | Shrine | `CGZ_hamon` (ondes), `CZ_sky_ref`, effets `DOBON` (chute dans l'eau) |
| du4 | Deep Mountain | `sky3_cloudy_weather2/3`, `stgdu4_eff_sky_dome`, `DOWNKEMU` (fumée) |
| du5 | Statues | `mars_CGZ_sky`, `CGZ_star1/2/3`, `CGZ_monn` (lune), `MZ_b_hikari` → **l'espace, ciel de Mars** |

**Aucun n'est une nuit étoilée simple**, et ce n'est pas un défaut de notre
build : c'est vrai des trois générations arcade.

* VF5 ver.B : `stgdur.farc` (35,7 Mo) n'a **aucun objet de ciel**.
* VF5 R : du1 a les **mêmes 24 ciels** qu'en FS ; du2 n'a que
  `CGZ_sky2`/`CGZ_sky3` — **ni feu, ni météore, ni étoile**. L'éruption a donc
  été **ajoutée en Final Showdown**.
* FS / APM3 : les cinq ci-dessus.

**La piste qui reste** : les **24 objets de ciel de du1**, numérotés `sky10` à
`sky32`, identiques en R et en FS. Une série numérotée de cette taille est la
signature d'un ciel qui **change** — cycle jour/nuit au fil du combat, ou jeu
de ciels sélectionnable. Le descripteur ne joue que trois auth_3d
(`0x001E0001`, `0x001E017E`, `0x001E0000` = objset 30, objets 1, 382 et 0) :
si un ciel de nuit est dans le lot, il est atteint autrement.

Sources non ouvertes qui pourraient trancher : `PS3_FS` et `X360_FS` (les
versions console de Final Showdown), dépaquetées mais dont les décors n'ont
jamais été inventoriés.

## 2026-09-07 (12) — un lecteur d'objsets, et deux inventaires à jeter

L'inventaire « par mots-clés » des décors de Dural était faux **dans sa
méthode** : je balayais l'ASCII des `stgdu*_obj.bin` et je prenais tout ce qui
ressemblait à un nom. Sur `stgdur_obj.bin` cela rendait 19 298 « noms », dont
l'immense majorité était du bruit binaire. Les tableaux du 2026-09-07 (10) et
(11) sont à jeter, y compris la « piste des 24 ciels ».

**`tools/objset.py`** lit maintenant la table, au lieu de deviner. L'en-tête
d'un jeu d'objets fait 0x40 octets :

    +0x00 magie 0x05062500   +0x04 NOMBRE d'objets   +0x08 plus grand id
    +0x0C table des objets   +0x14 TABLE DES NOMS    +0x18 table des ids
    +0x1C ids de texture     +0x20 nombre de textures

Et la vérité est beaucoup plus simple que l'inventaire bruyant :

| décor | objets réels (hors effets) |
|---|---|
| du1 | `stgdu1_gnd` 1, `stgdu1_ring` 382, `stgdu1_sky` **0** |
| du2 | `stgdu2_gnd` 4, `stgdu2_ring` 181, `stgdu2_sky` 3 |
| du3 | `stgdu3_gnd` 1, `stgdu3_reflect` 3, `stgdu3_sky` 0, `stgdu3_ring` 415 |
| du4 | `stgdu4_gnd` 1, `stgdu4_sky` 0, `stgdu4_ring` 189 |
| du5 | `stgdu5_gnd` 0, `stgdu5_ring` 1, `stgdu5_sky` 2 |

**Un décor a UN seul objet de ciel.** Il n'y a pas de série de 24 ciels, donc
pas de cycle jour/nuit caché. Le reste des noms — `hosi`, `kumo`, `mars` — sont
des noms internes de maillages ou de textures, pas des objets du moteur.

### Le champ `+0x14`…`+0x34` du descripteur est décodé

Vérification croisée sur les 41 décors : le mot HAUT est l'**identifiant
d'objset**, le mot BAS l'**identifiant d'objet dans cet objset**. Les cases
sont, dans l'ordre : `gnd`, `ring`, `sky`, `sdw`, `reflect`, —, puis trois
objets de l'objset **0** (les effets communs) pour sept décors.

    du1  objset 30   30:1  30:382  30:0
    djo  objset 28   28:114 28:118 28:117 28:116 28:115
    du5  objset 5529 5529:0 5529:1 5529:2  … 0:28600 0:28601 0:28602

C'est ce décodage qui rend l'import d'un décor étranger calculable.

---

## 2026-09-07 (13) — le décor de nuit de Dural : ce que dit l'image

Frédéric a donné sa source : une capture GameSpot **datée du 18 janvier 2007**,
donc **VF5 vanilla** (Xbox 360 / PS3), pas Final Showdown. Elle est enregistrée
en `analysis/vf5_2007_dural_nuit.jpg`.

`tools/textures_decor.py` sort les textures d'un décor en planche contact. Le
résultat, en trois images (`analysis/dural_nuit_le_point.png`) :

1. la capture 2007 : une rotonde à arches, sol de dalles polies, **ciel de nuit
   étoilé** dans les arches ;
2. l'écran de chargement de VF5 vanilla, extrait de `spr_s_loaddur.farc` du
   dump `X360_VF5` : **« Dural — SANCTUARY »**, et la vignette montre la même
   architecture **de jour**, herbe et colonnes ;
3. la texture du seul objet ciel de `du1` en Final Showdown : **un ciel de jour
   nuageux**.

Les planches de textures de `stgdur` (ver.B, 77 textures) et de `stgdu1` (FS,
139) montrent **les mêmes atlas** : colonnes, arches, remplages gothiques,
dallage, mur de pierre. `du1` **est** le SANCTUARY de 2007, réédité.

Conclusion, et elle est nette : le décor de nuit n'est **pas un sixième décor
manquant**. C'est le SANCTUARY, dont le ciel a changé entre 2007 et Final
Showdown. Les cinq `du1`..`du5` sont cinq variantes du même lieu — ce que
confirme le nommage de R.E.V.O., `st_vf5_sanctuary1..5.par`.

Deux façons de le retrouver, et la deuxième est celle qu'on sait déjà faire :

* remplacer la texture de `stgdu1_sky` par un ciel étoilé — cosmétique, mais
  l'éclairage resterait diurne ;
* **importer le `stgdur` de VF5 ver.B / X360 en entier** (35,7 Mo, un objset
  `stgdur_gnd` unique, sa collision, ses `light_param`) sur un emplacement
  d'essai. C'est exactement la manœuvre décrite ci-dessous.

Ce qui reste à vérifier : la capture 2007 est peut-être un état **scénarisé**
du combat final (nuit) et non le décor tel qu'il se charge. Le `stgdur` de
ver.B n'a **aucun objet de ciel** — le ciel y vient d'ailleurs.

---

## 2026-09-07 (14) — importer un décor de VF5 R : le dojo d'Akira

Demande de Frédéric : intégrer un décor de VF5 R pour l'essayer, celui d'Akira.
Le décor maison d'Akira est **`STGDJO`** (`rom/game_score.txt`,
`score.chara.0.stage=STGDJO`), index 11 — et c'est justement celui qui avait
échoué le 2026-09-03 en bouclant sur l'écran de chargement.

### La mesure qui explique l'échec, et qui rend l'import gratuit

Les cinq objets principaux de `djo` portent les **mêmes identifiants dans les
deux générations** :

    VF5 R (119 objets)          Final Showdown (171 objets)
      114 stgdjo_gnd              114 stgdjo_gnd
      115 stgdjo_reflect          115 stgdjo_reflect
      116 stgdjo_sdw              116 stgdjo_sdw
      117 stgdjo_sky              117 stgdjo_sky
      118 stgdjo_ring             118 stgdjo_ring

Et le descripteur du moteur demande déjà `28:114 28:118 28:117 28:116 28:115`.
**Il n'y a donc RIEN à patcher dans le binaire.** Les 52 objets que Final
Showdown a en plus sont des effets, numérotés 0 à 113 : aucun n'est nommé dans
le descripteur.

L'échec de septembre n'était donc ni le format ni les identifiants : c'était le
**mélange**. On avait posé l'objset de R à côté de l'`auth_3d`, des effets et de
la collision de Final Showdown. Corollaire à retenir : **un décor s'importe
avec sa génération entière**, et la note d'`import_decors.md` §7 (« VF5 R n'a
pas de `auth_3d/STGDJO.farc` ») était fausse — il fait 37 811 octets.

### L'outil

**`tools/importer_decor.py`** pose ou retire le jeu complet :

    py -3 tools/importer_decor.py --etat djo
    py -3 tools/importer_decor.py --poser djo --source VF5R
    py -3 tools/importer_decor.py --retirer djo

Huit fichiers, huit noms masqués dans l'index du `.par` : `stgdjo.farc`,
`STGDJO_COLI.000.bin`, `STGDJO.farc`, `EFFSTGDJO.farc`, `djo.ibl`, et les
quatre `light_param`. L'outil **refuse** de poser un jeu incomplet, en
nommant ce qui manque : c'est la garde contre la faute de septembre.

`envmap_correct_djo.txt` n'existe pas en 2008 ; il n'est pas masqué, donc celui
de Final Showdown est conservé.

### Un défaut de `par_masquer.py`, corrigé au passage

L'outil masquait **toutes** les occurrences d'un nom dans les 4 Go. Or
`STGDJO_COLI.000.bin` en a trois, dont deux vers `0xEDD000` — à 15 Mo, donc au
cœur des données archivées. Les écraser aurait corrompu un fichier au lieu de
cacher un nom. La borne est maintenant lue dans l'en-tête PARC : les noms
vivent entre `0x20` et la première des deux tables (`+0x14`, `+0x1C`), soit
`0x1D660` ici. Rien au-delà n'est touché.

### Le lanceur

**`tools/decor_5r_akira.cmd`** — build console complet + le décor importé.
**Sans `--decors-dural`** : cette option traduit les index 7 à 11 vers du1..du5,
donc elle enverrait `djo` (11) sur `du5` et cacherait précisément ce qu'on veut
voir. `--decor-perso djo` met le décor importé sur l'écran de personnalisation,
pour le voir sans lancer un combat.

**`tools/decor_5r_retirer.cmd`** rend les huit noms et efface les fichiers
libres. Le binaire n'est pas concerné.

Où regarder : DOJO avec **Akira** en partenaire ; ou STAGE SELECT, case du
dojo, **ligne du milieu, 3e colonne** (grille hors-ligne `0x180400210`,
ligne 1 colonne 2, ancre `stage_icon_djo_c`).

Ce qui devrait se voir : VF5 R a **40,8 Mo de textures contre 20,9 Mo** en
Final Showdown pour ce décor. Les textures ont été divisées par deux au
passage ; la géométrie, elle, a grossi.

Non vérifié à l'écran : personne n'a encore lancé cette build.

## 2026-09-07 (15) — l'import est instrumenté

Frédéric : « tu as instrumenté `decor_5r_akira.cmd` pour dépister rapidement les
erreurs ou plantages ? » Non — le lanceur se contentait de lancer le jeu. Fait.

Un décor importé peut échouer de trois façons qui donnent **le même écran de
chargement qui tourne** : le fichier n'est pas lu, le fichier est lu mais refusé,
ou une pièce annexe manque. **`tools/pister_import.py`** sépare les trois.

**Contrôle avant vol** (0,2 s, sans lancer le jeu) : les neuf fichiers posés,
leur taille et leur magie ; les neuf noms masqués dans l'index du `.par` ; le
descripteur du moteur ; et la question qui compte — *les objets que le
descripteur DEMANDE existent-ils dans l'objset qu'on a posé ?* Le lanceur
l'exécute et **refuse de lancer le jeu** si une faute sort.

**Mesure** (jeu lancé, clavier rendu) : points d'arrêt sur `CreateFileW/A`
filtrés sur nos neuf noms ; relevé continu de `TaskStage` (`[0x1807499D8]+0x58`)
avec un journal des changements d'état ; et surtout **les sept portes de la
barrière de l'état 3**.

C'est le point qui rend le dépistage rapide : `0x18018F74A` évalue sept
conditions **à la suite** et ressort à la première qui échoue. Il suffit donc de
poser un point d'arrêt au point d'arrivée de chacune — la porte la plus haute
atteinte désigne exactement la pièce fautive :

| porte | adresse atteinte si elle passe | pièce mise en cause |
|---|---|---|
| 1 | `0x18018F760` | l'objset (`stgdjo.farc`) |
| 2 | `0x18018F76D` | l'éclairage (`djo.ibl`, `light_param`) |
| 3 | `0x18018F77A` | la collision (`STGDJO_COLI.000.bin`) |
| 4 | `0x18018F78E` | l'auth_3d du décor (`STGDJO.farc`) |
| 5 | `0x18018F7A2` | le drapeau de scène |
| 6 | `0x18018F7B7` | l'auth_3d des effets (`EFFSTGDJO.farc`) |
| 7 | `0x18018F7C4` | les sons d'ambiance |

Jalons d'état : `0x18018FAF5` (→2), `0x18018F952` (→3), `0x18018F821` (→4),
`0x18018F73E` (**→5, en place**).

Lanceur : **`tools/depister_5r.cmd`**. Journal :
`analysis/pister_import_djo.txt`.

Essai à blanc de 35 s : l'outil tourne de bout en bout, mais personne n'ayant
mené le jeu jusqu'à un combat, la tâche est restée à l'état 0. Le verdict le
dit maintenant au lieu d'accuser le masquage — un outil qui conclut sur une
mesure vide est un outil qui ment.

Contrôle avant vol sur l'état actuel : **aucune faute**. Les neuf fichiers sont
posés, les neuf noms masqués, et l'objset de VF5 R contient bien `stgdjo_gnd`
114, `stgdjo_ring` 118, `stgdjo_sky` 117, `stgdjo_sdw` 116, `stgdjo_reflect`
115 — les cinq que le descripteur demande. Les trois derniers champs
(`0:28389`, `0:28390`, `0:28391`) viennent de l'objset commun et ne dépendent
pas de l'import.

## 2026-09-08 (16) — la grille passe de 21 à 25 cases : on AJOUTE

`--decors-dural-grille` détournait quatre cases : `riv`, `jin`, `sin` et `djo`
disparaissaient de l'écran. **`--grille-ajout`** les garde et ajoute une
**quatrième ligne**.

```
  are    nyc    slk    sin    cas    riv    smo
  tak    bar    djo    ALEA   jin    ter    ban
  hai    tan    gym    yuk    aur    umi    du1
  du2*   du3*   du4*   du5*                        (* = sans ancre)
```

Les 24 vrais décors du jeu sont désormais tous dans la grille, sans doublon.

**La place** : les deux tables de cases se suivent — `0x180400210` (21 cases,
hors ligne) puis `0x1804004B0` (22 cases, bornes liées), et la liste
d'exclusion ne commence qu'en `0x180400770`. Soit **0x560 d'affilée = 43
cases**. La table des bornes liées n'est lue que si `[0x180C3B6F0]+0x1FE10` est
non nul ; en console il est nul (`0x180174B6D : cmp …, r8=0 ; je` → branche hors
ligne), et la capture du 2026-09-07 le confirme : 3 × 7, la grille hors ligne.

**La position, et c'est le point** : lu dans `0x180173BD0`, une case **n'a pas
besoin d'ancre**. Le constructeur retient la dernière case ancrée (`+0x60`
colonne, `+0x64` ligne), calcule deux gradients (`xmm11` par colonne, `xmm10`
par ligne) et **extrapole** toute case dont `+0x18` est nul. Les quatre neuves
se placent donc au pas de la grille. C'est l'exact inverse de l'erreur du
2026-09-07 : repointer `+0x18` sur une ancre **déjà utilisée** empilait les
cases.

**Quatre compteurs**, et quatre seulement — les autres `0x15` du voisinage sont
des identifiants de calques AET (`0x18017481B`, `0x180174FBC`, `0x180175056`,
`0x180175129`) ou l'index du décor `du1` (`0x180174E13`) :

```
0x1801746D2  mov r8d, 0x15    -> 25   le compte donne au constructeur
0x18017493C  cmp rbx, 0x15    -> 25   la boucle qui cherche la case ALEA
0x180174BBE  cmp rax, 0x15    -> 25   la boucle index de decor -> case
0x180174AA0  cmp rsi, 0x2A0   -> 800  la borne du tirage au sort
```

Vérifié dans le binaire patché : les 25 cases sont là, les quatre compteurs
valent 25 (800 pour la borne en octets).

Lanceur : **`tools/decors_ajoutes.cmd`**. Il refuse `--grille-ajout` avec
`--decors-dural-grille` (les deux mettraient du2..du5 deux fois).

**Les deux inconnues, qui ne se tranchent qu'à l'image** :

1. la 4e ligne tombe-t-elle **dans le cadre** ? La grille occupe le tiers bas ;
   rien dans le code ne dit où s'arrête la zone dessinée ;
2. les cases neuves **n'ont pas d'aperçu**. La liste des aperçus n'est pas une
   table mais du **code**, construit instruction par instruction vers
   `0x180174BF0` (`mov [rbp+0xD0], 0x14 ; lea rax, "tan" ; …`, 0x18 octets par
   entrée). Lui ajouter une entrée demande une caverne.

## 2026-09-08 (17) — le multiplexeur USM, et les films de la Xbox 360

Chantier annoncé « ouvert, rien d'écrit » dans `PROMPT_REPRISE.md`. Il est
livré. Document : `analysis/films_usm.md`.

**La prémisse s'est vérifiée** : le flux vidéo d'un `.usm` du jeu est du
**MPEG-1 standard** — pas une seule extension MPEG-2 (`00 00 01 B5`) dans
`vf5adv.usm`. Donc `mpeg_codec = 1` (« Sofdec.Prime ») est exactement ce qu'un
`.sfd` transporte déjà, et `audio_codec = 2` est de l'ADX. **Il n'y a rien à
convertir : on remballe.** C'est la différence avec `medianoche.exe` du dossier
« MP4 to USM », qui décode et réencode en H.264.

Les trois inconnues annoncées ont été levées **par la mesure sur les films du
jeu**, pas par supposition :

* **une image par morceau `@SFV`** — 7304 morceaux de donnée pour
  `total_frames = 7304`, compté ;
* **50 blocs ADX = 1600 échantillons** par morceau `@SFA` (1800 octets en
  stéréo) ; le premier ne porte que l'en-tête ADX (288 octets) ;
* `VIDEO_SEEKINFO.ofs_byte` est l'**offset absolu dans le fichier**, une ligne
  par début de GOP — vérifié en comparant la table aux positions réelles des
  morceaux.

Restent `max_picture_size` et `metadata_size`, dont le message d'échec est
connu (`E2010122901M: Playback work memory…`) : il n'est jamais apparu, mais
**rien n'a encore été joué dans le jeu**.

### La preuve de non-perte

Les flux ressortis du `.usm` produit ont le **même MD5** que ceux du `.sfd`
d'origine, vidéo et audio, sur des films de 54 à 232 Mo :

```
vf5moe      video  52 209 294 o   4d9bef4b0a77b70c7cef10e5cdbed4bf   IDENTIQUE
            audio     976 698 o   f02d829d80f6224176f26cc35e219f9f   IDENTIQUE
vf5verBadv  video 206 916 206 o                                      IDENTIQUE
            audio voie 0..3, quatre flux                             IDENTIQUES
```

### Le multipiste : l'AIX déplié

Frédéric : « le convertisseur doit gérer le multipiste audio ». Un `.sfd` peut
porter un conteneur **AIX** — le multipiste de CRI. Format relevé sur la piste
`0xC2` de `vf5verBadv.sfd` : un en-tête `AIXF` (nombre de flux en `+0x40`,
offset des données en `+0x20`), puis des morceaux **`AIXP`** entrelacés,
chacun étiqueté du **numéro de son flux** en `+0x08`, avec sa longueur **utile**
en `+0x0A` — la charge est bourrée, `+0x04` compte le bourrage.

Les trois premiers `AIXP` portent chacun l'en-tête ADX de leur flux, les
suivants leurs blocs. Recoller flux par flux les charges utiles rend donc trois
ADX complets, sans rien décoder. Chacun devient une **voie `@SFA`**, qui est
précisément le mécanisme multipiste de Sofdec2. `vf5verBadv` sort en **quatre
voies**, et les trois flux AIX ont des empreintes **différentes** : le
désentrelacement route bien chaque morceau.

### Les films de la Xbox 360, extraits

Les deux dumps ne se ressemblent pas : VF5 vanilla a cinq `.sfd` en fichiers
libres ; Final Showdown est un **paquet STFS** de 2,05 Go (magie `LIVE`, 2370
entrées, ouvert par `tools/stfs.py`) qui ne contient **qu'un seul film**,
`vf5end.sfd`, et **aucun `.usm`**. Les six sont réunis dans
`extracted/sfd_x360/`.

```
film                                octets  image       cadence  son
fs_vf5end.sfd                    145311744  1280x720    60.000/s ADX 44100 Hz, 82,0 s
vanilla_vf5adv.sfd               232202240  1280x720    60.000/s ADX 48000 Hz, 90,0 s + AIX
vanilla_vf5end.sfd               191207424  1280x720    60.000/s ADX 44100 Hz, 74,0 s
vanilla_vf5moe.sfd                53989376   640x480    30.000/s ADX 48000 Hz, 18,1 s
vanilla_vf5verBadv.sfd           227686400  1280x720    60.000/s ADX 48000 Hz, 80,7 s + AIX
vanilla_vf5verCadv.sfd           209416192  1280x720    60.000/s ADX 44100 Hz, 80,1 s + AIX
```

Cinq des six sont en **1280×720 à 60 images/s**, la définition exacte des films
d'APM3. À noter : le `vf5end.sfd` de la Xbox 360 Final Showdown (145 311 744 o)
n'est **pas** celui du Lindbergh Final Showdown (145 477 632 o) — deux masters.

### La seule réserve qui tient encore

Le champ `date` des morceaux vidéo avance, chez CRI, à **moitié** du temps réel
(60,8 s pour un film de 121,7 s) alors que l'audio est juste — et les cinq
films du jeu ont tous ce décalage. C'est donc une convention de leur outil, et
le lecteur se cadence sur `framerate_n / framerate_d`. On reproduit la
convention observée ; `--dates justes` écrit l'autre.

### Outils écrits

`tools/sfd.py` (lecteur Sofdec1), `tools/usm.py` (lecteur Sofdec2 : morceaux,
tables `@UTF`, démultiplexage), `tools/usm_mux.py` (le multiplexeur, avec
écriture des tables `@UTF`), `tools/sfd_inventaire.py`, lanceur
`tools/sfd_vers_usm.cmd` (glisser-déposer ou double-clic).

## 2026-09-08 (18) — le nom de variante au premier plan : le tuyau 2D, désassemblé

> **PARTIELLEMENT PÉRIMÉ — lire la section 19.** Ce qui suit reste juste sur la
> chaîne du texte et sur `AetMgr`, mais sa **conclusion est fausse** : l'ordre à
> l'écran n'est pas l'ordre d'insertion, et le détour du créneau 2 d'`AetMgr`
> n'a rien donné. La profondeur existe, elle est calculée, et `desc+0x24` /
> `desc+0x28` ne sont pas des flottants de style : ce sont les deux champs qui
> la fixent.

Frédéric, après quatre placements ratés : « ne me fais plus tester pour rien,
on perd notre temps. Désassemble ce qui est nécessaire, arrête de tâtonner. »
Il avait raison. Document : `analysis/texte_2d.md`.

### Ce qui était acquis avant, et qui bornait le problème

| où le dessin est posé | résultat | ce que ça établit |
|---|---|---|
| `TaskSelStage` créneau 4 | visible, **dessous** | le dessin marche depuis une tâche |
| `TaskSelStage` créneau 6 | rien | ce créneau n'est pas appelé |
| détour du créneau 4 de `TaskSelector` | dessous | dessiner après le parent ne suffit pas |
| détour du créneau 2 d'`AetMgr`, **original puis dessin** | **invisible** | la liste est déjà vidée à ce moment |

### Ce que la lecture a apporté

**Le texte** : `0x18019B2E0` → `0x18019B330` (formatage) → `0x18019AC70` (mise
en page) → **`0x18019B4A0`**, qui construit les quatre sommets d'un glyphe et
les empile :

```
vmovups [rdx], xmm0 ; vmovsd [rdx+0x10], xmm1 ; add qword [rcx+8], 0x18
```

soit des **sommets de 0x18 octets**, avec `0x1801067C0` pour agrandir le
vecteur.

**`AetMgr`**, les trois créneaux qui tournent :

| créneau | rôle |
|---|---|
| 4 (`0x1800235C0`) | parcourt `[mgr+0x68]`, appelle `+0x18` de chaque objet — la mise à jour |
| 6 (`0x1800251A0`) | reparcourt, appelle `+0x20`, travaille sur `[mgr+0x78]` avec `0xaaaaaaaaaaaaaa9` (division par 24) — **l'empilement de sommets de 0x18 octets** |
| 2 (`0x180023150`) | parcourt `[mgr+0x78]` et le **consomme** |

**Même taille d'élément des deux côtés.** L'ordre à l'écran n'est donc pas une
profondeur : c'est **l'ordre d'insertion**.

### Deux fausses pistes, écartées par la lecture

* les champs `+0x24` et `+0x2C` du descripteur, que je prenais pour un calque
  et une priorité, sont des **flottants du STYLE** — des échelles, lues en
  `0x18019AEDB` et `0x18019B075` ;
* le mot `0x28` n'est pas un tri mais un jeu de bits d'alignement
  (`bt edx, 9`) : le balayage de tous les appels de dessin de texte du moteur
  rend 1, 2, 4, 8, 0x20, 0x21, 0x22, 0x28, 0x800.

### Le correctif

Il restait **un seul point** entre les deux bornes : l'**entrée** du créneau 2,
après que le 6 a tout empilé et avant que le 2 ne vide. Le détour y est donc
inversé — **notre dessin d'abord, l'original ensuite** — et notre texte est le
dernier sommet inséré, donc dessiné par-dessus. **Rien n'est retiré de
l'écran**, ce qui était la contrainte posée.

Non vérifié à l'écran au moment d'écrire. Ce qui n'est pas prouvé : que le
vecteur du texte et celui de l'AET soient le même objet — les éléments ont la
même taille et la même forme, mais le vecteur du texte est passé en pile depuis
`0x18019AC70` et je n'ai pas remonté jusqu'à son propriétaire.

### La leçon, et elle a coûté cher

Six essais à l'écran pour un problème qui se lisait. À chaque fois j'ai raisonné
par analogie — « le créneau 5 existe donc il est appelé », « le parent dessine
après donc il suffit de passer après lui » — au lieu de descendre dans le code.
La seule mesure qui a fait avancer, `tools/pister_ordre.py`, a donné l'ordre de
la trame en une fois. Et la seule lecture qui a débloqué, celle des sommets,
tenait en trois fonctions.

## 2026-09-08 (19) — la profondeur 2D : un tableau de 4 × 32, et la taille se lit

Suite directe de la section 18, dont la conclusion était fausse. Trois faits,
tous **lus**, aucun deviné. Document : `analysis/texte_2d.md` §8-9-10.

### 1. La profondeur existe et elle est CALCULÉE

`0x180187C00` soumet la commande au contexte 2D global (`0x180719900`) et
`0x18018CA20` l'insère à une adresse calculée :

```
0x18018CA2B  r15d = cmd+0x14
0x18018CA35  si r15d == -1  ->  r15d = [contexte+0x828]     le CALQUE COURANT
0x18018CACC  rcx = cmd+0x18 ; r14 = cmd+0x1C ; inc r14
0x18018CADD  rcx += r15 ; rcx <<= 5 ; r14 += rcx ; r14 <<= 4 ; r14 += contexte
```

et `0x18019B1D0` / `0x18019B1D6` alimentent ces deux champs depuis le
**descripteur** : `cmd+0x1C ← desc+0x24`, `cmd+0x18 ← desc+0x28`. `cmd+0x14`,
lui, n'est **jamais** posé sur le chemin du texte : il reste à `-1` (le
constructeur `0x18018993E`), et l'insertion retombe donc sur le calque courant,
celui que l'AET a monté. Voilà pourquoi aucun point d'accroche ne marchait :
ce n'était pas une question d'instant.

### 2. Monter le calque a PLANTÉ, et la raison est une taille

Frédéric : « le jeu crash juste avant de pouvoir sélectionner l'icône du décor
de Dural » — la première trame où la garde laisse passer. Le **constructeur du
contexte** donne la faute :

```
0x18018A049  mov ecx, 0x838 ; call operator new                 0x838 octets
0x18018A092  call 0x1802FE160(ctx+0x10, 0x10, 0x80, ctor, dtor) 128 x 16 o
0x18018A097  [ctx+0x818], [ctx+0x820], puis [ctx+0x828] le calque courant
```

Le `+1` de la formule est exactement le décalage de `0x10` du tableau, donc

```
indice = (desc+0x24) + ((desc+0x28 + calque) << 5)      dans 0..127
```

soit **quatre calques de trente-deux rangs**. Monter le calque de 8 demandait
l'indice 264, deux kilo-octets au-delà de l'objet. Ce n'était pas un « montant
trop grand » : **1 suffisait déjà à sortir** dès que le calque courant valait 3.

### 3. Le correctif : borné par construction, et sans état global

`DESSINER` ne touche plus à `[contexte+0x828]`. Il corrige **son propre
descripteur** avant les neuf passes :

```
desc+0x28 = plafond - calque      (le calque effectif vaut toujours 3)
desc+0x24 = ordre                 (31)
si calque > plafond               on ne dessine pas du tout
```

`indice = 31 + 3*32 = 127`, le dernier compartiment : parcouru en dernier, donc
au-dessus de tout, et hors d'atteinte du débordement. Rien n'est à restaurer,
les quatre sorties sautent droit sur `add rsp,0x38 ; ret`.

Vérifié sur la DLL construite : `plafond=3`, `ordre=31`, `desc+0x28` écrit en
`0x180EA1848`, `desc+0x24` en `0x180EA1844`, indice **127 / 127**, et **zéro**
mot de la greffe ne ressemble à une adresse absolue.

### Réglages, tous des données de la greffe

| adresse | rôle | défaut |
|---|---|---|
| `0x180EA1808` | plafond de calque — **ne pas augmenter** | 3 |
| `0x180EA180C` | rang dans le calque (0..31) | 31 |
| `0x180EA1810` / `0x180EA1814` | x, y | 640, **460** (position validée) |
| `0x180EA181C` | taille de police | 24 |

Lanceur : **`tools\variantes_texte.cmd`**. Le repli sans dessin, celui qui a
chargé DU4, reste **`tools\variantes.cmd`**.

### Ce qui n'est pas prouvé

Que le compartiment 127 soit bien au-dessus de celui de l'AET. Il l'est par
construction — c'est le dernier — **sauf** si l'AET dessine lui aussi en 127 :
l'ordre serait alors celui de l'insertion, et il faudrait avancer notre dessin
dans la trame. À trancher sur une image.

### La leçon, chère

Six essais à l'écran puis un plantage, pour un problème entièrement lisible —
la taille du tableau était écrite en clair, `mov ecx, 0x838`, dans le
constructeur. Et l'erreur de méthode a été la même à chaque fois : régler une
valeur « modeste » au lieu de chercher la **borne**.


## 2026-09-09 (20) — une séance de casse, et ce qu'elle a appris

Séance à porter au passif. En voulant **ajouter** le dojo de VF5 R au lieu de
le remplacer, j'ai cassé quatre choses qui marchaient. Tout est rendu, et le
rétablissement de `trm` est **validé à l'écran par Frédéric**.

### Les quatre casses, et leur cause

| ce qui a cassé | la cause |
|---|---|
| le dojo chargeait `du5` | `--decors-dural cas` translate 7..11 → du1..du5, et **djo vaut 11**. `decor_5r_akira.cmd` n'a jamais eu cette option : c'était la seule différence entre les deux lanceurs |
| `trm` / TERMINAL ne chargeait plus rien | j'ai recyclé un emplacement **déjà réparé** (validé le 2026-09-05), écrasé son descripteur, et laissé ses neuf noms masqués dans le `.par` sans les fichiers |
| `djo` restait en VF5 R dans **tous** les lanceurs | l'état des fichiers était **hérité** : `patch_moteur.py` repart de `.origine`, `importer_decor.py --poser` ne repart de rien |
| `variantes_texte.cmd` ne démarrait plus | je l'avais réécrit en **fins de ligne UNIX** ; `cmd.exe` casse dessus sans un mot |
| puis : une fenêtre noire | j'avais redirigé toute la sortie vers un journal, et appelé `--retirer` sans condition : **16 s de balayage du `.par`**, deux fois, en silence |

### Ce qui est rendu et vérifié, sur les octets

* `trm` : neuf noms rendus dans le `.par`, zéro fichier libre, descripteur
  `0x180404C90` **identique à `.origine`**. `--decor-perso trm` remet ses deux
  octets (`0x1801C4DA6+1` et `0x1801C4DCB+1` = `0x1A`) — **validé à l'écran** ;
* `djo` : `decor_5r_akira.cmd` intact, contrôle avant vol passé ;
* les 47 lanceurs : `tools/verifier_lanceurs.py` les passe tous.

### Les garde-fous posés

* **chaque lanceur POSE son état de fichiers**, il ne l'hérite plus — et
  seulement si un fichier libre est là, pour ne pas payer 16 s pour rien ;
* **`tools/verifier_lanceurs.py`** : fins de ligne, fichiers cités, et la
  ligne de patch réellement exécutée. 47 lanceurs, aucun défaut ;
* `variantes_texte.cmd` : un `pause` final systématique, un journal dans
  `analysis/variantes_texte.log`, une ligne d'état avant chaque étape ;
* `--decor-perso trm` porté dans `variantes_texte.cmd`, comme
  `decor_TRM.cmd`.

### Ce qui a quand même été appris, et qui sert

Le désassemblage de la séance vaut, lui, et il est rangé dans
`analysis/decors.md` §13 (les mesures) et §14 (la proposition) :

* **le descripteur de décor a QUINZE champs utiles**, pas trois — dont
  `+0xD0` qui aiguille un rendu (`0x18018F440`, comparé à 0 et à 4) et `+0xD4`
  qui indexe un **saut sur dix constantes** (`0x18018F630` → `0x180204863`) ;
* `+0xB8` / `+0xC0` sont un **compte et un tableau de murs** : douze décors
  seulement en ont, ceux qui ont des murs, `djo` compris ;
* le descripteur est posé au gestionnaire à **une seule instruction**,
  `0x18018EF87 mov [rcx+0x68], r8` — c'est le point d'accroche naturel pour
  substituer un descripteur sans se heurter aux relocations ;
* seuls **quatre** lecteurs lisent la table statique par index : le code
  `STGxxx`, le balayage inverse, la musique (`0x18018F3D0`, qui **retombe sur
  `+0x68`** quand les neuf reprises sont nulles) et `+0xD4` ;
* la **liste d'aperçus** ne connaît que 26 indices (4..25, 39, 40, 41) et
  **efface** les couches AET quand elle ne trouve pas ; le curseur, lui,
  retombe sur la case `rnd` — mais dans une branche qui s'exécute avant notre
  accroche, donc sans effet ;
* l'**éclairage** n'est pas dans le descripteur : table de 41 codes en
  `0x18039F7A0`, lue par `0x1800D7130`.

### La leçon, et elle est de méthode

Deux lanceurs, un qui marche et un qui rate, **et je n'ai pas commencé par les
comparer**. Frédéric a dû le demander deux fois. Avant de désassembler quoi que
ce soit : *diffe les deux invocations*. Et une validation à l'écran s'écrit
comme une **recette reproductible** le jour même, sinon elle est perdue —
`project_vf5_import_5r` la porte désormais.


## 2026-09-09 (21) — le build de Yakuza 6 : une pierre de touche

Comparaison du moteur APM3 avec celui embarqué dans **Yakuza 6**
(`vf5fs-pxd-w64-Retail_GOG.dll`). Document complet :
`analysis/comparaison_builds.md`. Outils écrits pour l'occasion :
`tools/comparer_builds.py` et `tools/par_inventaire.py`.

Le build Yakuza 6 est **plus récent de dix-huit mois** (2022-12-02 contre
2021-05-19) et pourtant plus petit d'un tiers : 9 770 fonctions contre 13 661.
C'est le même moteur, amputé de sa couche arcade.

### Trois résultats qui servent

1. **Les données sont les mêmes.** 1 822 fichiers communs sur ~1 850 ; les 41
   décors aux mêmes tailles à l'octet près. APM3 a en plus les dix-neuf
   `<perso>itm_patch.farc` et `se_adam.acb` ; Yakuza 6 n'a rien de plus. Et le
   `stgdur` perdu n'y est pas non plus — les deux binaires ne connaissent que
   `auth_3d/stgdur`, l'animation sans la géométrie.

2. **Sur les 41 descripteurs de décor, UN SEUL champ diffère** — et c'est la
   **collision de DU2** : APM3 pointe `STGDU1_COLI.000.bin`, Yakuza 6 pointe
   `STGDU2_COLI.000.bin`. Le défaut que Frédéric avait vu à l'écran est donc
   une **régression propre à l'APM3**, et `--du2-collision` est validé par un
   build indépendant. Les quarante autres sont identiques champ pour champ.

   Le pas d'une entrée vaut **0xF0 chez APM3 et 0xD8 chez Yakuza 6** : les
   24 octets d'écart sont exactement le bloc BGM — dix pointeurs contre sept.
   Tout le reste se réaligne (`+0xB8`→`+0xA0`, `+0xD0`→`+0xB8`, `+0xE4`→`+0xCC`).

3. **Le bouchonnage n'est PAS une amputation de l'arcade.** Les quatre mêmes
   familles existent des deux côtés, dans des proportions comparables :

   | bouchon | APM3 | YAK6 |
   |---|---|---|
   | `ret 0` | 577 appelants | 429 |
   | `xor al,al ; ret` | 210 | **241** |
   | `xor eax,eax ; ret` | 117 | 128 |
   | `mov al,1 ; ret` | 71 | 44 |

   Ce sont des fonctions vides fusionnées par l'éditeur de liens, pas des
   maillons retirés. « Patcher le site d'appel, jamais le corps » reste vrai ;
   « c'est bouchonné donc on l'a amputé » ne l'est pas.

### Le balayage des autres tables

Toutes les tables liées aux décors ont été croisées ensuite. **Identiques** :
les 41 codes d'éclairage, les cinq blocs de murs (`+0xC0`, mêmes douze décors),
la grille de sélection case par case, et la liste d'aperçus (4..25, 39, 40, 41).

**Le forçage « du1 → du2 » se scinde en deux, et c'est la nuance qui compte :**

* le **bouchon du combat** — `mov eax,0x16 ; ret` — est dans les **DEUX**
  builds (`0x1800B2330` chez nous, `0x1800C6040` chez Yakuza 6), appelé depuis
  un site rigoureusement identique. Choisir toujours DU2 pour un combat n'est
  donc **pas** une amputation de la borne ;
* les **trois sites d'écran** (`0x18017448F`, `0x180175338`, `0x1801753A0`)
  sont **propres à l'APM3**. Balayage exhaustif de tous les `cmp <reg32>,0x15`
  suivis d'un `0x16` : **3 sites chez nous, 0 chez Yakuza 6**. Ce sont des
  verrous ajoutés pour la borne, que `--decors-dural-grille` et `--variantes`
  lèvent — ils remettent l'écran dans l'état du build console.

`project_vf5_decors_dural` parlait d'un « forçage quadruple » : c'est exact,
mais il faut lire **1 bouchon partagé + 3 verrous arcade**.

### Le RTTI

534 vtables nommées chez APM3, 314 chez Yakuza 6. Sur les **noms de base** :
311 communes, 118 propres à APM3 (le réseau `Abaas`/`Link*`/`Turn*`, la crypto,
les `TaskApm3*`, le menu opérateur `Menu*`), et **trois** propres à Yakuza 6 —
`TaskMultiMenu`, `TaskMultiMenuRule`, `TaskMultiResult`, la partie locale à
plusieurs.

**Piège** : comparées sur les noms COMPLETS, cinq classes de personnalisation
semblaient propres à Yakuza 6. C'était le hachage d'espace de noms anonyme
(`?A0x…`) qui change d'un build à l'autre. Comparer les noms de base.

### Deux pièges d'outillage, payés sur place

* **le pas d'une table se déduit** : figé à `0xF0`, le chercheur répondait
  « table introuvable » sur un binaire où elle vaut `0xD8` ;
* **chercher une chaîne avec son NUL** faisait répondre « absent » pour
  `am::abaas` et `STGDUR`, qui sont des sous-chaînes.


## 2026-09-09 (22) — l'interface APM3, cartographiée

Parti d'une capture : six badges grisés et barrés aux quatre coins de
l'écran-titre. Le jeu n'y était pour rien. Document qui fait foi :
**`analysis/interface_apm3.md`**. Outils : `tools/apm_icones.py`,
`tools/apm_sons.py`, `tools/apm_lancer.py` + `tools/apm_hors_ligne.cmd`.

### Le réseau : un seul binaire sort, et SEGA le dit

`amdaemon.exe` porte les sept domaines ALL.Net (`aime.naominet.jp`,
`naominet.jp`, `at.sys-all.net`, `amlog.sys-all.net`…) et les API `connect` /
`WinHttpOpen` / `getaddrinfo` / `send`. **`Apmv3System.exe` et `emoneyUI.exe`
n'ont aucune API réseau.** Et `firewall.cfg` du système ne contient qu'une
ligne : `x:\amdaemon.exe`.

D'où l'essai hors ligne, sans démon, en bac à sable, sous mesure :

```
emoneyUI      arrete tout seul apres  8 s (code 0)   0 connexion
Apmv3System   arrete tout seul apres 17 s (code 0)   0 connexion
```

### Ce que le dossier contient vraiment

* **109 textures** Unity (96 extraites, 13 en BC7 non décodé) et **78 PNG** en
  clair dont **13 distincts** — les logos e-money : nanaco, 楽天Edy, iD,
  交通系, WAON, PASELI, SAPICA ;
* **114 `.wav`** dont **19 distincts** : des jingles de paiement de 0,22 s à
  3,59 s. **Aucune musique**, aucun `AudioClip` Unity ;
* **aucune vidéo** — le lecteur AVPro et la machinerie `Advertize` sont là,
  les films arrivent par le réseau ;
* **233 messages d'erreur** en trois langues (`am_resources/*.dll`), avec
  numéro, reset et domaine : 949 `Keychip Not Found`, 6401 `I/O board is not
  connected`, 5501 `Touch Panel Not Found`, 703 `Available application not
  found`…
* **ni fond d'écran, ni jaquette** : c'est un système d'exploitation, pas un
  jeu.

### Deux choses qui servent au chantier VF5

* **`lib/apm.dll` est le vrai `apm.dll`** que `vfes.exe` importe — identique à
  notre `apm.reelle.dll` au SHA-256 près (`a91ca49bbe728413b873`), tout comme
  `apmgamepad.dll` (`92fe8f90b508d1a90e74`) ;
* **`game.bat` ne doit JAMAIS être lancé** : il efface `Y:\`, écrit dans
  `HKLM\System\SEGA\…` et **flashe** les micrologiciels de la carte USB IO,
  de la carte LED (COM2, 115200) et de la dalle tactile.

### Les deux fautes d'outillage, payées ici

* **`brn_volume_disable`** — SEGA a écrit `brn_` au lieu de `btn_`. Trois
  recherches ciblées l'ont manqué : je cherchais le nom que je supposais. Seul
  le balayage complet de la table des textures l'a rendu. **Énumérer d'abord,
  filtrer après.**
* Ma signature de « décor d'essai » figeait les rangs d'objets à 0 et 1 ; `ts2`
  et `ts3` (rangs 1 et 2) en sont sortis « vrais décors ». Même faute que le
  pas de table figé à `0xF0` dans `comparer_builds.py` : **tester la FORME,
  jamais des valeurs devinées.**

## 2026-09-09 (23) — le dojo de VF5 R **ajouté**, et une option qui n'avait jamais marché

Frédéric, ce matin : le nom de variante **s'affiche** — le correctif du rang 127
du 2026-09-08 est validé à l'écran, `variantes_texte.cmd` fait ce qu'il annonce.
Puis : « maintenant je veux ajouter proprement le décor VF5R d'Akira. Fais-le
sur une build spécifique, on pourra revenir en arrière si ça se passe mal. »

Livré : **`tools/decor_5r_akira_ajout.cmd`** et
**`tools/decor_5r_akira_ajout_retirer.cmd`**. Document :
`analysis/import_decors.md` §10.

### Ce que j'ai trouvé en ouvrant `--variantes-djo`

L'option existait déjà — écrite le 2026-09-08, jamais relancée depuis. Elle
était cassée **en deux endroits qui se contredisaient** :

* `VARIANTES_ANNEAU_DJO = ([11, 26], …)` : 26, c'est `trm`. La barre espace
  aurait fait défiler vers le décor TERMINAL ;
* `VARIANTES_TRM_INDEX = 29` : le clonage visait `evo00` — **cinq lettres**,
  alors que `importer_decor.py --vers` renomme les entrées internes de
  l'archive par substitution **en place**. La pose des fichiers n'aurait pas pu
  aboutir.

Le correctif posait donc le décor à un endroit et faisait défiler vers un autre.
Deux constantes pour une seule donnée : elles ont divergé au premier changement.
L'emplacement est désormais **un argument** (`--variantes-djo <code>`) et tout
en est dérivé — indice, objset, chaîne de collision, anneau.

### Le garde-fou qui se mordait la queue

`emplacements.py` déclare pris tout code qu'un de nos `.cmd` nomme. C'est la
preuve 4, celle qui manquait le jour où `trm` a été cassé, et elle est juste.
Mais dès que le lanceur qui **pose** le décor écrit `--vers trs`, `trs` devient
« utilisé par decor_5r_akira_ajout.cmd » — et `importer_decor.py` le refuse à ce
lanceur-là. Un lanceur ne pouvait pas poser son propre décor deux fois.

Levé sans affaiblir la garde : `emplacements.py --pourquoi <code>` étiquette ses
raisons (`descripteur` / `grille` / `apercu` = le moteur s'en sert ; `lanceur
<nom>` = une réservation), et `importer_decor.py --pour <lanceur.cmd>` ne lève
que les réservations, et seulement celles du lanceur qui demande.

### Le choix de `trs` s'est mesuré

Quinze emplacements libres ; deux critères en laissent cinq puis un :

* **trois lettres** — la substitution en place dans l'en-tête du `FArC` ;
* la **forme** du descripteur (deux objets du bon objset, trois `-1`).

Mesure faite au passage, et elle sert : les six emplacements candidats (`tst
ts3 wht cid trs evo00`) portent **exactement les mêmes sept relocations** —
`0x00 0x08 0x48 0x50 0x58 0x60 0x68` — là où `djo` en a dix-sept. La liste des
dix pointeurs à remettre à zéro n'était donc pas propre à `trm`.

### Vérifié, et jusqu'où

* le patch passe, descripteur `0x180404E70` (trs, objset 44), collision écrite
  en `0x180641B80` sans collision avec `--du2-collision` ;
* l'anneau de la greffe porte bien `[11, 28]` et les deux libellés
  `VIRTUA FIGHTER 5 FS` / `VIRTUA FIGHTER 5 R` ;
* les quatre refus se déclenchent : `trm`, `djo`, un code à cinq lettres, un
  code inconnu ;
* `pister_import.py trs --controle` : **rien à redire** — neuf fichiers posés,
  noms masqués, et les cinq objets demandés présents dans l'objset posé ;
* `verifier_lanceurs.py` : 49 lanceurs, aucun défaut ;
* le jeu **démarre et atteint l'écran-titre** (`analysis/ajout_5r_titre.png`).

**Pas encore vu à l'écran** : la bascule. C'est l'essai à faire.

## 2026-09-09 (24) — une section greffée peut enfin porter des pointeurs

Frédéric a tranché la direction, et il a raison : recycler les emplacements
d'essai **n'est pas un ajout**, c'est un remplacement de décors inutilisés, et
ils ne sont pas assez nombreux pour les décors de VF5 R **et** du VF5 d'origine.
« Il faut donc faire un VÉRITABLE ajout de décor au jeu. »

Document : `analysis/greffe_relocations.md`. Outil : `tools/pe_sections.py`.

### D'abord, pourquoi le décor posé sur `trs` sortait partiel

Deux causes, mesurées au diff du descripteur champ par champ, et toutes deux
**structurelles au recyclage** :

* `+0x00` = `STGDJO` et `+0x08` = `EFFSTGDJO` — le clone garde les noms
  d'auth_3d du dojo. L'emplacement emprunte donc l'animation de **Final
  Showdown**, et notre `auth_3d/STGTRS.farc` posé ne peut **jamais** être lu :
  `auth_3d_db.bin` porte 308 noms `STG*`, et aucun emplacement d'essai n'y
  figure. Le contrôle avant vol ne pouvait pas le voir — il vérifie les
  fichiers posés, pas ce que le descripteur NOMME ;
* `+0xB8` = 2 murs avec `+0xC0` = NULL. L'emplacement n'a pas de relocation
  là ; un clone statique ne peut pas porter la table des murs.

Un emplacement d'essai n'a ni entrée de base de données, ni relocations. Ça ne
se répare pas.

### La clé de voûte : la table de relocations est un COUPLE, pas une section

Le chargeur ne cherche pas `.reloc`. Il lit le **répertoire de données n° 5**,
`(RVA, taille)`, à `optional_header + 152`. On peut donc lire les 209 blocs
d'origine (29 643 entrées), y ajouter les nôtres, écrire le tout dans une
section neuve et repointer le répertoire.

`tools/pe_sections.py` le fait, et se contrôle en relisant **avec `pefile`** :
un outil qui se relit lui-même ne prouve rien. Trois témoins, dont un en
`0xFF8` — le cas limite, huit octets qui finissent pile sur la fin de page.

    origine : 6 sections, 29643 relocations utiles
    apres   : 8 sections, 29646 relocations utiles
    rebasage simule : 3 pointeurs corriges dans .decors
    AUCUNE FAUTE.

### Et le contrôle qui compte : Windows accepte-t-il la table ?

Le format bien écrit ne prouve pas que le chargeur l'accepte. On a donc greffé
`.decors` sur la DLL **déjà patchée** du build console, écrit `0x180403430` en
dur dedans, reconstruit la table, lancé le jeu, et lu la mémoire du processus
vivant :

    vfes.exe pid 19648 ; moteur charge en 0x7FFC81C70000
    delta de rebasage : 0x7FFB01C70000
      temoin en 0x7FFC82B12000 : 0x7FFC82073430
      attendu                  : 0x7FFC82073430
    RELOCATION APPLIQUEE.

**Le jeu démarre avec neuf sections et une table de relocations reconstruite.**
La règle « aucun pointeur absolu dans la greffe » tombe : elle valait pour une
section sans relocations, et nos sections en ont maintenant.

### Ce que la mesure a donné au passage

* **184 octets libres** dans l'en-tête = quatre en-têtes de section. Trois sont
  prévues (`.greffe`, `.decors`, `.reloc2`), une reste. **L'ordre compte** :
  `.greffe` doit être posée en premier pour garder `0x180EA1000`, ses réglages
  étant documentés à des adresses fixes ;
* le mou de `.reloc` existe — 328 octets — et ne sert à rien : 128 descripteurs
  demandent plus de deux mille entrées ;
* **`auth_3d_db.bin` est du TEXTE.** `#A3DA`, puis `category.74.value=STGDJO`
  et `uid.703.value=A S010A010_DJO_STG_01`. Déclarer l'animation d'un décor
  neuf est une édition de texte, pas un format à rétro-concevoir ;
* les huit bornes indexées par le décor sont relevées, toutes des `cmp` sur un
  immédiat (`0x28`, `0x29`) plus `cmp r9, 0x2670` = 41 × 0xF0.

### Une capture ratée, et pourquoi

Les deux captures de la séance ont photographié le **navigateur de Frédéric** :
`SetForegroundWindow` est refusé à un processus d'arrière-plan, et on
photographie la zone d'écran, pas la fenêtre. Le piège est déjà écrit
(`reference_capture_zone_ecran`) ; il se represente dès que la machine est
utilisée pendant la mesure. La preuve du chargement, elle, ne dépend d'aucune
image : c'est la lecture mémoire.

### La suite

`.decors` est greffée et relogeable, mais **vide**. L'ordre :

1. y déplacer les deux tables de 41 entrées (descripteurs, codes à trois
   lettres), repointer les `lea`, lever les huit bornes — et vérifier que le
   jeu tourne encore **à 41 décors**, avant d'en ajouter un seul ;
2. les trois bases de données : `auth_3d_db` (texte), `obj_db`, `tex_db` ;
3. seulement ensuite, le premier décor VÉRITABLEMENT ajouté.

## 2026-09-09 (25) — les deux tables de décors déplacées, à 41 décors

Suite directe de l'entrée 24. La greffe sait porter ses relocations ; on s'en
sert. Document : `analysis/ajouter_un_decor.md` §7. Lanceur :
**`tools/decors_table.cmd`**.

### Ce qui est fait

`--decors-table [N]` copie les **deux** tables indexées par le décor dans la
section `.decors` — 41 descripteurs de `0xF0` en +0, 41 pointeurs de code à
trois lettres en `+0x2670` — repointe les huit sites qui les chargent, et
reconstruit la table de relocations pour les **556 pointeurs** déplacés.

**À `N = 41`, aucune borne n'est levée.** C'est délibéré : on veut pouvoir
séparer « le déplacement est faux » de « la borne est fausse ». Le jeu doit se
comporter exactement comme avant.

### Deux outils écrits pour l'occasion

* **`tools/refs_plage.py`** — les références à une **plage**, en un seul
  balayage. `refs_lineaires.py` cherche une adresse ; une table ne se référence
  pas qu'à son premier octet, et c'est ainsi qu'on a trouvé `0x18018F409`, qui
  entre par `+0x70` pour la base des neuf reprises de musique. Il rapporte le
  **champ `disp32`**, pas l'adresse d'instruction : capstone, parti d'un octet
  mal aligné, lit parfois `lea eax` là où il y a `lea rax`, et l'adresse est
  alors décalée d'un octet — le `disp32`, lui, ne bouge pas.
* **`tools/verifier_decors_table.py`** — octets identiques, huit sites,
  relocations une par une, rebasage simulé.

### La règle qui a guidé la copie

**On ne devine aucun décalage : une relocation est recopiée là où `.origine`
en a une.** C'est exactement l'inverse de la faute des deux séances
précédentes, où l'on croyait qu'un descripteur « disait trois champs » puis
« quinze ». Il en dit ce que la table de relocations en dit, et elle est
lisible.

La mesure au passage : 515 pointeurs dans les descripteurs, à dix-sept
décalages ; 17 décors en portent 7 (les emplacements d'essai), 12 en portent 16
et 12 en portent 17. Le bloc des **murs** (`0x1804033E0`) n'est pas relogé —
ce sont des triplets 0/1/2, des données — donc il ne bouge pas et `+0xC0` le
vise toujours.

### Vérifié, et jusqu'où

Sans lancer le jeu : 9840 + 328 octets identiques, huit sites repointés, 556
relocations posées (ni une de moins, ni une de trop), aucune relocation
d'origine perdue, rebasage simulé qui corrige les 515 pointeurs.

Dans le **processus vivant**, le descripteur du dojo relu à sa nouvelle
adresse :

    moteur en 0x7FFC62390000  (delta 0x7FFAE2390000)
       +0x00 STGDJO   +0x08 EFFSTGDJO   +0x48 rom/STGDJO_COLI.000.bin
       +0x68 rom/sound/bgm/vfes_bgm_stg_djo.adx   +0xC0 les murs
       code du decor 11 : 'djo'   code du decor 28 : 'trs'

**Pas encore vu à l'écran** — c'est l'essai à faire, et il consiste à ne RIEN
voir changer.

### Un défaut attrapé par l'outillage, et il vaut d'être noté

`verifier_lanceurs.py` a refusé `decors_table.cmd` : il rejoue la ligne de
patch d'un `.cmd` sans retirer la redirection `>nul`, et `--decors-table`
consommait aveuglément le mot suivant. Corrigé en ne consommant le mot que
s'il est un **nombre**. Le contrôle des lanceurs a trouvé un défaut que le
lanceur seul n'aurait montré qu'à l'exécution.

### La fenêtre noire, et la faute refaite le même jour

Frédéric : « `decors_table.cmd` ne lance rien d'autre que sa propre fenêtre, un
écran noir qui n'affiche aucun message. »

Cause, mesurée en lisant mon propre lanceur : **trois `--retirer`
inconditionnels et muets**, chacun un balayage de 16 s des 4 Go du `.par`. Soit
cinquante secondes de fenêtre noire avant le premier `echo`. C'est **exactement**
la faute de l'entrée 20 de ce journal — « j'avais redirigé toute la sortie vers
un journal, et appelé `--retirer` sans condition » — refaite le même jour, dans
un lanceur neuf, alors que les quatre autres portent déjà la garde `if exist`.

Corrigé : bannière dès la première ligne, `--retirer` seulement si le fichier
libre est là, et chaque étape annoncée.

### Et l'antislash mangé, qui a failli passer

La première réparation est passée par un **heredoc `bash`**. Il a mangé les
antislashs, Python a interprété `\v` et `\r`, et
`runtime\media\vf5fs\vf5fs_media\rom\objset` est devenu `runtime\media` +
tabulation verticale + `f5fs` + retour chariot + `om\objset`. Le lanceur restait
syntaxiquement valide, `cmd.exe` n'aurait rien dit — il aurait simplement
cherché un chemin qui n'existe pas — et **`verifier_lanceurs.py` l'a déclaré
sain** : il contrôlait les fins de ligne et les fichiers cités, pas les octets
de contrôle à l'intérieur des chemins.

Le piège « les heredocs bash mangent les antislashs » est écrit depuis
longtemps. Ce qui manquait, c'est un contrôle qui le VOIE. Ajouté :
`verifier_lanceurs.py` refuse désormais tout octet < 0x20 autre que TAB, CR et
LF, et nomme la cause. Éprouvé sur un témoin sali exprès, puis effacé.

**La leçon est de méthode, et elle est la même deux fois** : un piège écrit dans
la documentation ne protège de rien tant qu'un outil ne le détecte pas. Les
deux fautes de cette séance étaient toutes les deux déjà écrites.

### VALIDÉ À L'ÉCRAN

Frédéric, 2026-09-09 : **« rien n'a changé à l'écran, tout fonctionne »**.

C'était l'énoncé exact de l'essai. Les deux tables indexées par le décor vivent
désormais dans une section à nous, avec leurs 556 relocations, et le jeu ne s'en
aperçoit pas. **La recette, à reproduire telle quelle** :

    py -3 tools\patch_moteur.py <options du build console> --decors-table
    py -3 tools\verifier_decors_table.py        (contrôle sans lancer le jeu)

Lanceur : `tools\decors_table.cmd`.

### La septième borne : elle ne se lève pas, et ce n'est pas une prudence

`ajouter_un_decor.md` §4 la notait « `0x1801B5F7F`, compteurs de parties, 41
entrées de 0x10 o, `cmp r8d, 0x29` — protégé ». Deux corrections, l'une de
forme, l'autre de fond.

**De forme** : `0x1801B5F7F` est un **début de fonction** relevé dans `.pdata`,
pas une comparaison. Les vraies sont `0x1801B648D` et `0x1801B6507`, plus
`0x1801B6483` (`cmp r8d, 0x22`), la version déroulée par huit — soit `N - 7`.
C'est le piège déjà écrit : *une entrée `.pdata` est souvent un FRAGMENT*, et
celle-ci commence au milieu d'un calcul de ratio.

**De fond, et c'est ce qui compte** : cette boucle n'indexe aucune table de
`.rdata`. Elle recopie des compteurs d'un objet vers un autre —

    source       [r14 + 0x11FC + i*8]      deux dwords : parties, victoires
    destination  [rdi + 0x1A2EC + i*0x10]  trois dwords et un ratio flottant

— et **les deux tableaux sont exactement dimensionnés à 41**. La preuve tient
en deux instructions, celles qui suivent la boucle : `lea rsi, [rdi + 0x1A580]`
alors que `0x1A2EC + 41*0x10 = 0x1A57C`, et `lea rbx, [r14 + 0x1348]` alors que
`0x11FC + 41*8 = 0x1344`. Le champ suivant commence **juste après**.

Lever cette borne ne donnerait donc pas des statistiques aux décors ajoutés :
cela écrirait dans le champ d'à côté. Elle reste à 41, définitivement, et le
patcheur le **dit** dans son compte rendu — pour que personne ne cherche un jour
pourquoi un décor ajouté n'a pas de compteur de parties.

**La leçon vaut plus que la borne** : toutes les bornes à 41 ne sont pas des
bornes de TABLE. Certaines sont des **tailles de tableau dans une structure**.
Avant d'en lever une, regarder ce qui suit le tableau — ici, une seule
instruction le disait.

Les six autres se lèvent, elles : `--decors-table 48` passe.

## 2026-09-09 (26) — `auth_3d_db.bin` ouvert, et il était en clair

Document : **`analysis/auth_3d_db.md`**. Outil : **`tools/a3d_db.py`**.

`ajouter_un_decor.md` §5 la listait parmi « ce qui reste ouvert », avec
`tex_db.bin`, depuis le 2026-09-07. Il n'y avait rien à ouvrir : **223 565
octets, 8 172 lignes, zéro octet non imprimable.** Un dictionnaire `clé=valeur`
précédé de `#A3DA`.

### La seule règle qui compte

**Les clés sont triées comme des CHAÎNES.** `category.10.value` avant
`category.2.value`, `category.length` après `category.9.value` — « l » passe
après les chiffres. `a3d_db.py` ne garde donc pas les lignes, il garde les
paires et les réécrit triées ; et l'**aller-retour rend le fichier identique à
l'octet près**. C'est le contrôle qui dit qu'on a compris le format, et il tient
en une commande : `py -3 tools/a3d_db.py --essai`.

### Ce que la base dit

| | |
|---|---|
| catégorie | le nom d'une archive : `STGDJO` → `auth_3d/STGDJO.farc` (`auth_3d/%s.farc`, `0x1803F9438`) |
| uid | un `.a3da` de cette archive ; `A ` en tête est un marqueur de type |
| chargée depuis | `rom/auth_3d/auth_3d_db.bin` (`0x180348C30`) |

92 catégories, 3 469 uids, dont **1 166 sans catégorie ni taille**. Le dojo :
`STGDJO` 3 uids (`S010A010_DJO_STG_01/02/03`), `EFFSTGDJO` 6.

### Ajouter, et les deux décisions qui vont avec

`--ajouter STGTRS --depuis STGDJO` : la catégorie est insérée **dans l'ordre
alphabétique avec renumérotation** — les 92 d'origine sont classées, et rien ne
dit que le moteur ne fasse pas une dichotomie dessus — tandis que les uids sont
ajoutés **à la fin sans renuméroter**, leur numéro étant un identifiant et non
un rang (ceux de `STGDJO` sont 703-705, au milieu des autres). Dix-sept lignes
changent, et le résultat se relit à l'octet près.

**Les noms de `.a3da` sont recopiés VERBATIM**, et c'est le bon défaut :
`importer_decor.py --vers` renomme les deux entrées de l'objset dans l'en-tête
du `FArC`, **pas** les `.a3da`. Une archive importée puis renommée porte
toujours `S010A010_DJO_STG_01`. Substituer le code donnerait des noms qui
n'existent nulle part, et le décor se chargerait **sans son animation, en
silence** — exactement le défaut qu'on cherchait à corriger. `--renommer`
existe, explicite, pour le jour où l'archive sera réécrite aussi.

### Une trouvaille en chemin, et une question ouverte

En cherchant comment le moteur nomme les archives, un **second registre** est
apparu : `0x18054E180`, **249 entrées de 16 octets**, `{const char* chemin;
size_t}` — les 93 `auth_3d/…`, puis `objset/…`, `rob/mot_…`, `string_array`. La
seconde valeur n'est pas un nombre d'uids (`adv` : 400 ici, 12 uids dans la
base) : une taille, ou un budget.

**Un balayage linéaire de toute la plage — `.text` et données — ne trouve
AUCUNE référence.** C'est le genre d'affirmation qui exige précisément ce
balayage, et c'en est un ; mais tant qu'on n'a pas trouvé *comment* elle est
atteinte, on ne peut pas conclure qu'elle est morte. Si elle l'est, un décor
ajouté n'a rien à y faire. Sinon, c'est la prochaine table à étendre.

`size` n'est pas expliqué non plus. Recopié du modèle, il est exact par
construction pour un décor importé ; il faudra le comprendre pour une animation
neuve.

## 2026-09-09 (27) — `obj_db.bin` : la « zone inexpliquée » était un pot de chaînes

Document : **`analysis/obj_db.md`**. Outil : **`tools/obj_db.py`**.

`ajouter_un_decor.md` §5 portait depuis le 2026-09-07 : « la zone
`0x77890`–`0x0F3F80` n'est pas expliquée ; écrire un reconstructeur demande de
la comprendre ». Elle est expliquée, et ce n'était pas une structure : **c'est le
second pot de chaînes**, celui des noms d'objets. Il commence exactement où
finit la table des jeux — `0x77950`, l'adresse notée était approchée d'une
centaine d'octets, ce qui suffisait à ne pas voir que les deux se touchent.

    0x000000   en-tete, huit u32
    0x000020   POT A : les chaines de la table des jeux      272 192 o
    0x042760   table des JEUX      6044 x 0x24               217 584 o
    0x077950   POT B : les noms d'objets                     509 488 o
    0x0F3F80   table des OBJETS    17744 x 8                 141 952 o
    0x116A00   fin, a l'octet pres

Un objet vaut `(objset << 16) | rang` **suivi de l'offset de son nom** — le même
empaquetage que le descripteur de décor. `djo` demande `0x1C0072 0x1C0076
0x1C0075 0x1C0074 0x1C0073` : objset 28, rangs 114 118 117 116 115, soit
`STGDJO_GND _RING _SKY _SDW _REFLECT`. L'objset en porte **171** ; le
descripteur n'en nomme que cinq, les 166 autres sont des effets.

### La réécriture, et le contrôle qui la valide

Les deux pots sont gardés en octets et on n'y ajoute qu'à la fin : les offsets
du pot A ne bougent jamais, ceux du pot B se décalent d'une quantité connue.
Sans ajout, le décalage est nul et **l'aller-retour rend le fichier identique à
l'octet près** — 1 141 248 octets, 6044 jeux, 17 744 objets.

Un décor complet ajouté coûte **5 769 octets**, et le fichier produit se relit
lui aussi à l'octet près.

### Deux choses qui ne se devinaient pas

* **Zéro est une valeur.** 191 jeux sur 6044 n'ont ni fichier d'objets, ni
  fichier de textures, ni archive : ce sont les objsets d'**items**
  (`AKIITM012`…), qui vivent dans l'archive d'un autre. Refuser le zéro faisait
  échouer la lecture dès le rang 70 — le premier essai s'est arrêté là.
* **Aucune des deux tables n'est triée.** On ajoute donc à la fin sans rien
  réordonner : le moteur construit son index trié au démarrage.

### Le garde-fou a servi dès le premier essai

`--ajouter STGTRS` est **refusé** : `STGTRS` existe déjà, identifiant 44. Les
41 emplacements de décor ont tous leur entrée dans `obj_db` — et c'est
exactement pour cela que `importer_decor.py --vers trs` marchait côté fichiers
sans toucher à cette base. Un décor **vraiment** ajouté a besoin d'un nom neuf ;
l'essai est passé sur `STG5RD`, identifiant 6150.

Les identifiants sont **troués et non bornés** : 66 plages libres, la plus
confortable commençant à 6150. Le studio a fait pareil — `du5`, `gym` et `smo`
portent 5529, 2847 et 2848, pris ailleurs.

### Reste

`tex_db.bin`, la dernière des trois : même famille, 841 776 octets, en-tête
`0x6588` entrées à `0x9ABF0`.

## 2026-09-09 (28) — `tex_db.bin`, et le risque qui n'existait pas

Document : **`analysis/tex_db.md`**. Outil : **`tools/tex_db.py`**.
Les trois bases que le vrai ajout de décors demandait sont faites.

La carte tient en cinq lignes — c'est la plus simple des trois :

    0x00000   u32 nombre de textures   25 992
    0x00004   u32 offset de la table   0x9ABF0
    0x00010   POT : les noms                              633 824 o
    0x9ABF0   TABLE  25 992 x 8   {identifiant, offset du nom}
    0xCD830   fin, a l'octet pres

### La différence de méthode avec `obj_db`, et elle compte

**La table est TRIÉE par identifiant**, vérifié sur les 25 992 entrées. On
n'ajoute donc pas à la fin : on **insère**. `obj_db`, lui, n'est trié ni par jeu
ni par objet, et s'ajoute à la fin. Rien ne dit que le moteur ne fasse pas une
dichotomie sur l'une ; on ne casse pas un tri par commodité.

L'espace est troué : 25 992 textures pour des identifiants allant à 32 258,
soit **910 plages libres** — 400 au-delà du dernier, et des trous internes de
303, 151, 150. De quoi loger un décor entier n'importe où.

### Le risque annoncé n'existait pas

`analysis/decors.md` §14.8 portait, depuis le 2026-09-08 : « le risque qui
reste, et il est réel : `tex_db.bin`. L'objset importé déclare des identifiants
de texture ; rien ne prouve encore qu'ils se résolvent sous un autre objset ».

**Rien à prouver : ils sont déjà dans la base.** Le dojo porte 271 textures
`F_VF5E_DJO00_*`, identifiants `0x19C7` et suivants. Une archive importée puis
renommée garde ses noms **et** ses identifiants de texture ; ils sont présents
sous leurs noms d'origine. Un décor importé n'a donc **rien** à ajouter ici —
seule une texture vraiment neuve en demande une.

Ce qui manquait au décor posé sur `trs` était donc bien ailleurs, et c'est
mesuré : les noms d'auth_3d du descripteur (`+0x00` = `STGDJO`) et la table des
murs (`+0xC0` à zéro). Pour situer l'échelle : `trs` ne porte que **deux**
textures à son nom. Il n'en avait pas besoin de plus, puisqu'il chargeait celles
du dojo.

### L'état de la voie B

| pièce | état |
|---|---|
| section greffée avec ses relocations | fait, prouvé dans le processus vivant |
| les deux tables de 41 déplacées | fait, **validé à l'écran** |
| les six bornes levables | levées ; `--decors-table 48` passe |
| la septième | reste à 41 : c'est une taille de tableau, pas une borne de table |
| `auth_3d_db.bin` | fait, aller-retour à l'octet près |
| `obj_db.bin` | fait, aller-retour à l'octet près |
| `tex_db.bin` | fait, aller-retour à l'octet près |
| la grille et les aperçus | **à faire** |
| le premier décor vraiment ajouté | **à faire** |

## 2026-09-09 (29) — la grille déménagée, et l'aperçu enfin mesuré

Lanceur : **`tools/decors_grille.cmd`**. Option : `--grille-table`, qui exige
`--decors-table` — les deux tables partagent la section `.decors` et la même
reconstruction des relocations, qui doit se faire **une** fois, en dernier.

### Une erreur de la documentation, corrigée

`ajouter_un_decor.md` §6.2 annonçait, depuis le 2026-09-07 : « les deux tables
de cases sont adjacentes, suivies de la liste d'exclusion — soit **0x560 octets
d'affilée = 43 cases** ».

**C'est faux, et dangereusement.** Ce qui suit la seconde table, ce sont **deux
qwords** (`-1`, `0`) puis, immédiatement, **les chaînes `stage_icon_*_c` que la
grille elle-même pointe** : `0x180400778` porte `stage_icon_are_c`, et la case 0
y pointe. Écrire 43 cases là aurait détruit les noms d'icônes que ces cases
utilisent. La « place libre » était le contenu de la table.

On ne s'entasse donc plus : **la grille déménage**, comme les deux autres.

### Ce qui bouge

| | |
|---|---|
| `0x180400210` | 21 cases de `0x20` → `.decors` + `0x27C0` |
| ses 21 pointeurs d'icône | une relocation chacun |
| cinq sites `lea` | dont **deux qui visent `+0x8`**, le champ d'index, sur lequel deux boucles balaient |

La table des **bornes liées** (`0x1804004B0`, 22 cases) ne bouge pas : elle n'a
aucun pointeur — pas d'icône — et ce build n'utilise pas ce mode.

La case, mesurée : `+0x00` colonne, `+0x04` ligne, `+0x08` **index du décor**,
`+0x0C` 332, `+0x10` 331, `+0x18` le pointeur d'icône.

### Aucun des quatre comptes n'est touché, et c'est délibéré

    0x1801746D4   mov r8d, 21        le compte passe au constructeur
    0x18017493F   cmp rbx, 21        recherche de la case ALEA
    0x180174BC1   cmp rax, 21        index de decor -> case
    0x180174AA3   cmp rsi, 21*0x20   le tirage au sort

Le déménagement doit se prouver seul, comme celui des descripteurs l'a été.
**Et une case vide serait dangereuse** : son index de décor irait à
`0x18018FCF0`, dont la garde est `cmp ecx, 0x29 ; jge ret` — elle arrête les
index trop **grands**, pas les négatifs, et un `-1` multiplié par `0xF0` lit
**avant** la table. On n'ajoutera donc de case que quand il y aura un décor à y
mettre.

**Ce qui n'est PAS un compte**, relevé au passage : `0x180174C00` et
`0x18017507B` portent `0x2C0`, qui vaut pourtant 22 × 0x20 — mais ce sont
`sub rsp, 0x2C0` et `add rsp, 0x2C0`, la taille de pile du constructeur
d'aperçus. Une valeur qui ressemble à un compte n'en est pas un.

### L'aperçu : mesuré, et la voie pour l'étendre est trouvée

La liste est bien construite **sur la pile**, `0x18` octets par entrée
`{i32 index, ptr "xxx", ptr "xxx_stay"}` — on la voit s'assembler `lea rax,
"ter"` / `mov [rsp+0x70], rax` / `lea rax, "ter_stay"` / `mov [rsp+0x78], rax`.

Le lecteur, lui, est court et clair (`0x180175010`) :

    mov edx, [rcx]           l'index de l'entree
    cmp edx, -1  ; je        le TERMINATEUR -> on efface
    cmp edx, [rbx+0x5C]      l'index du decor courant -> trouve
    add rcx, 0x18            le pas
    cmp rax, 0x1a  ; jb      la borne : 26 entrees

et le chemin « pas trouvé » (`0x18017502D`) appelle **trois fois**
`0x1801721D0(scene, 0x13 / 0x14 / 0x15)` : ce sont les trois couches AET
effacées, exactement ce que `decors.md` §13 annonçait.

**La voie pour l'étendre ne demande pas de réécrire le constructeur.** Il suffit
de détourner le lecteur vers une table statique de `.decors` : `lea rcx,
[rsp+0x50]` en `0x180175005` fait **cinq** octets — assez pour un `jmp rel32`
vers une caverne qui pose `lea rcx, [rip+d]` et revient. La construction sur la
pile devient alors morte, sans gêner personne. Reste à changer la borne
`0x1a` en `0x18017502A`.

Ce n'est pas fait : il n'y a pas encore de décor ajouté dont il faudrait
l'aperçu.

### Vérifié

`verifier_decors_table.py` couvre désormais la grille : octets identiques,
cinq sites repointés, 21 pointeurs d'icône relogés, **et les quatre comptes
contrôlés intacts**. Aucune faute. **Pas encore vu à l'écran** — et là encore,
l'essai consiste à ne rien voir changer, icônes comprises.

### VALIDÉ À L'ÉCRAN

Frédéric, 2026-09-09 : **« rien n'a changé à l'écran, tout fonctionne »** — le
même énoncé que pour les descripteurs, et c'était le même essai.

**La recette, à reproduire telle quelle :**

    py -3 tools\patch_moteur.py <options du build console> --decors-table --grille-table
    py -3 tools\verifier_decors_table.py

Lanceur : `tools\decors_grille.cmd`. `--grille-table` **exige**
`--decors-table` : les deux partagent la section `.decors` et la reconstruction
des relocations, qui doit se faire une seule fois, en dernier.

**Les trois tables du chantier décors vivent désormais dans une section à
nous**, avec leurs 577 relocations, et le jeu ne s'en aperçoit pas :

| table | où | relocations |
|---|---|---|
| 41 descripteurs de `0xF0` | `.decors` + 0 | 515 |
| 41 pointeurs de code | `.decors` + `0x2670` | 41 |
| 21 cases de grille | `.decors` + `0x27C0` | 21 |

## 2026-09-09 (30) — quarante-quatre décors, et une mine désamorcée avant de sauter

Lanceur : **`tools/decors_44.cmd`**. C'est la première fois que la table de
décors du jeu est plus grande que la sienne.

### La mine, trouvée en relisant le lecteur plutôt qu'en levant la borne

Lever les six bornes donne une table de N entrées — mais **une entrée laissée à
zéro n'est pas neutre**. `0x18018F590` balaie les N descripteurs pour résoudre
un nom en index, et il **déréférence `+0x00`** :

    0x18018F5B0  mov   r8, [r9+rbx]        le pointeur du nom
    0x18018F5C3  movzx ecx, [rax+r8]       ... et on lit dedans, octet par octet

Un pointeur nul y lit à une adresse absurde. **Lever une borne sans remplir ce
qu'elle ouvre, c'est armer un plantage** — et il ne se serait pas vu tout de
suite, ce chemin n'étant emprunté que par la résolution d'un nom de décor
(`game_score.txt`).

Toute entrée au-delà de 41 est donc un **clone complet** du dojo — 17 pointeurs
relogés chacun, **la table des murs (`+0xC0`) et les neuf reprises de musique
comprises** — avec son propre code à trois lettres, `x00`, `x01`, `x02`, écrit
dans `.decors` et relogé lui aussi.

C'est le premier endroit où l'on voit ce que la greffe relogeable a débloqué :
le clone de septembre, sur un emplacement d'essai, ne pouvait porter que **7**
pointeurs sur 17. Celui-ci les porte tous.

### Ce que le build fait

| | |
|---|---|
| table des descripteurs | **44** entrées, les 41 d'origine puis trois clones |
| table des codes | 44, avec trois codes neufs dans `.decors` |
| six bornes | levées à 44 |
| la septième | reste à 41 — tableau dans une structure, pas une table |
| grille | 21 cases, déménagée, comptes intacts |
| ce qui sélectionne les trois neufs | **rien** : ni grille, ni anneau, ni `game_score.txt` |

L'essai est donc, encore une fois, de **ne rien voir changer**. Le contrôle
statique passe : `verifier_decors_table.py --n 44`, aucune faute, et chacune des
trois entrées neuves porte ses 17 relocations et un code valide.

### Ce qui manque encore à un décor VRAIMENT ajouté

Les trois entrées neuves sont des clones du dojo : elles chargent ses fichiers.
Pour qu'une d'elles devienne un décor à part entière, il reste à lui donner

1. **son objset** — `obj_db.py --ajouter`, identifiant neuf (6150 est libre) ;
2. **son animation** — `a3d_db.py --ajouter`, catégories `STGxxx`/`EFFSTGxxx` ;
3. **ses chaînes propres** dans `.decors` : `+0x00`, `+0x08`, `+0x48` — elles
   sont relogeables désormais, donc rien ne s'y oppose ;
4. **ses fichiers**, posés sous le code neuf : ils n'existent pas dans le
   `.par`, donc **aucun nom à masquer** — c'est le cas facile, celui que
   `ajouter_un_decor.md` §3.1 décrivait ;
5. **de quoi le sélectionner** : l'anneau de la barre espace, `--variantes-djo`,
   sur la case du dojo. Pas une case de grille — une case reste une case, c'est
   tranché.

Rien là-dedans n'est ouvert : les cinq outils existent.

### VALIDÉ À L'ÉCRAN

Frédéric, 2026-09-09 : **« rien n'a changé à l'écran, tout fonctionne »** — la
troisième fois de la journée, et le troisième essai dont l'énoncé était de ne
rien voir changer.

**Le jeu tourne donc avec 44 décors.** La recette :

    py -3 tools\patch_moteur.py <options console> --decors-table 44 --grille-table
    py -3 toolserifier_decors_table.py --n 44

Lanceur : `tools\decors_44.cmd`. La voie B est ouverte : il ne reste plus qu'à
remplir une entrée.

## 2026-09-09 (31) — le descripteur d'un décor VRAIMENT ajouté

`--decor-neuf <code> --objset <id> --auth3d <NOM>` remplit la première entrée
neuve (indice 41) avec ce qui la rend distincte du modèle. Le résultat, relu
dans le binaire produit :

    DESCRIPTEUR 41 -- le decor AJOUTE
       +0x00 nom auth_3d  'STGD5R'
       +0x08 eff auth_3d  'EFFSTGD5R'
       +0x48 collision    'rom/STGD5R_COLI.000.bin'
       +0x68 musique      'rom/sound/bgm/vfes_bgm_stg_djo.adx'
       +0x70 reprise VF1  'rom/sound/bgm/vfes_bgm_vf1_djo.adx'
       +0xC0 MURS         0x1804033E0
       +0x10 objset       6150
       +0x14 objets       0x18060072 0x18060076 0x18060075 0x18060074 0x18060073
       +0xB8 murs         2        +0xE4 aire  12 x 12
       code[41] = 'd5r'

**Les dix-sept pointeurs sont valides.** C'est exactement ce que l'emplacement
d'essai ne pouvait pas porter : le clone du 2026-09-08 sur `trs` en perdait dix
sur dix-sept — les neuf reprises de musique et la table des murs.

Trois chaînes neuves vivent dans `.decors` et sont relogées avec le reste. Les
longueurs se correspondent, ce qui n'est pas un hasard mais une contrainte :
`djo` (3) → `d5r` (3), `stgdjo` (6) → `stgd5r` (6), `EFFSTGDJO` (9) →
`EFFSTGD5R` (9). C'est ce qui permettra à `importer_decor.py` de renommer les
archives **en place**.

`--variantes-neuf 41` pose l'anneau de la barre espace entre le dojo de Final
Showdown et celui-ci — sans recycler aucun emplacement du jeu.

### Une faute d'ancrage, et comment elle s'est vue

Le premier essai a rendu un descripteur 41 **inchangé**, cloné du dojo, sans un
message. Cause : j'avais inséré le bloc avant le *second* `if grille:` — celui
du compte rendu — et non avant le premier, qui précède
`fp.write(bytes(contenu))`. Le code écrivait donc dans un tampon déjà versé sur
le disque.

Ça ne s'est vu que parce qu'on **relit le binaire produit** au lieu de croire le
compte rendu du patcheur, qui annonçait pourtant fièrement l'entrée 41. Un
compte rendu dit ce que le code croit avoir fait ; seule la relecture dit ce
qu'il a fait.

### Ce qui reste, et c'est du fichier

1. `obj_db.bin` : l'entrée `STGD5R`, identifiant 6150, et ses 171 objets ;
2. `auth_3d_db.bin` : les catégories `STGD5R` et `EFFSTGD5R` ;
3. les deux bases posées en fichiers libres, leurs noms masqués dans le `.par` ;
4. les pièces du décor posées sous le code `d5r` — **aucun nom à masquer**,
   elles n'existent pas dans le `.par`.

Les outils des trois premiers points existent et se contrôlent seuls.

## 2026-09-09 (32) — les fichiers et les deux bases : le décor ajouté est complet

Lanceurs : **`tools/decor_ajoute.cmd`** et `tools/decor_ajoute_retirer.cmd`.
Outils : **`tools/decor_neuf.py`** (pose et retire) et
**`tools/controle_decor_neuf.py`** (contrôle avant vol).

### Ce qui est posé, et ce qui est masqué

| | |
|---|---|
| les neuf pièces, sous le code `d5r` | **aucun nom à masquer** — `stgd5r.farc`, `d5r.ibl`, `STGD5R_COLI.000.bin` n'existent dans le `.par` d'aucune façon |
| `obj_db.bin` | `STGD5R`, identifiant **6150**, 171 objets recopiés de `STGDJO` |
| `auth_3d_db.bin` | `STGD5R` (3 uids) et `EFFSTGD5R` (6 uids) |
| l'index du `.par` | **deux noms masqués, et deux seulement** : `obj_db.bin`, `auth_3d_db.bin` |

C'est la première fois qu'on est dans le **cas facile** que
`ajouter_un_decor.md` §3.1 décrivait depuis le 2026-09-07 : « un décor nouveau
se dépose librement, sans toucher au `.par` ». Jusqu'ici on recyclait, donc on
masquait neuf noms ; ici on ajoute, donc on n'en masque que deux — et ces deux-là
sont des bases, pas le décor.

### Les longueurs se correspondent, et c'est une contrainte, pas un hasard

`importer_decor.renommer_farc` substitue les noms **en place** dans l'en-tête du
`FArC`. Le code a donc été choisi pour que tout tienne :

    djo (3) -> d5r (3)   stgdjo (6) -> stgd5r (6)   EFFSTGDJO (9) -> EFFSTGD5R (9)

`decor_neuf.py` le **vérifie** avant de copier quoi que ce soit, et refuse en
nommant le champ fautif.

### Ce qui est recopié verbatim, et pourquoi il le faut

Les noms d'**objets** (`STGDJO_GND`) et de **`.a3da`**
(`S010A010_DJO_STG_01`) ne sont pas substitués. L'archive posée est celle du
modèle, renommée : elle porte toujours ces noms à l'intérieur. Les deux bases
doivent donc les déclarer tels quels — sinon le décor charge sans sa géométrie
ou sans son animation, **en silence**. C'est exactement le défaut qui rendait
partiel le décor posé sur `trs`.

### Le contrôle avant vol, et la question qui compte

`controle_decor_neuf.py` pose cinq questions, mais une seule décide : **les cinq
objets que le descripteur demande existent-ils dans l'archive posée, sous
l'identifiant d'objset posé ?**

    1. LE DESCRIPTEUR
       objset demande        6150
       objets demandes       6150:114 6150:118 6150:117 6150:116 6150:115
       auth_3d               'STGD5R' / 'EFFSTGD5R'
       collision             'rom/STGD5R_COLI.000.bin'
    3. LA BASE obj_db POSEE
       STGD5R : identifiant 6150, stgd5r_obj.bin / stgd5r_tex.bin / stgd5r.farc
    4. LES OBJETS DEMANDES EXISTENT-ILS DANS L ARCHIVE POSEE ?
       stgd5r_obj.bin : 119 objets, id max 118
         6150:114   stgdjo_gnd     6150:118   stgdjo_ring
         6150:117   stgdjo_sky     6150:116   stgdjo_sdw
         6150:115   stgdjo_reflect
    5. LA BASE auth_3d_db POSEE
       STGD5R      3 uid(s)   EFFSTGD5R   6 uid(s)
    RIEN A REDIRE.

**Un écart assumé, et il faut le dire** : `obj_db` déclare 171 objets pour cet
objset (recopiés de la version 2010) alors que l'archive de 2008 n'en porte que
119. Les 52 en trop sont des effets que personne ne demande — ce sont des noms
dans une base, rien ne les charge. À corriger le jour où l'on voudra une base
exacte, pas avant.

### L'anneau, vérifié dans la greffe

    comptes des anneaux : (5, 2, 0, 0)
      anneau 0 : [21, 22, 23, 24, 25]      les cinq Dural
      anneau 1 : [11, 41]                  le dojo, et le decor AJOUTE
      rang 8 : 'VIRTUA FIGHTER 5 FS'
      rang 9 : 'VIRTUA FIGHTER 5 R'

`--variantes-neuf 41` ne clone rien et ne garde rien : le descripteur est déjà
rempli, et l'indice n'existe pas dans `.origine` — la garde « emplacement
d'essai intact » n'y aurait aucun sens. C'est une option à part, et le patcheur
refuse un indice inférieur à 41.

### L'état

Tout est construit et contrôlé sans lancer le jeu. **Rien n'a encore été vu à
l'écran** — et cette fois, contrairement aux trois essais précédents, l'essai
n'est pas de ne rien voir changer : c'est de voir un décor **de plus**.

## 2026-09-09 (33) — l'indice 41 est le code « aléatoire », et ça se voyait

Frédéric, à l'écran : **« le décor chargé est celui d'un décor de FS chargé au
hasard »**.

Sa phrase nomme la cause. Le décor ajouté avait été posé à l'indice **41** — le
premier libre après les décors du jeu, indices 0 à 40. Or **41 = 0x29 est le
code « décor aléatoire »**.

Sept sites le testent **par égalité**, et non comme une borne :

    0x18013391E   un balayage de liste cherchant la valeur 41
    0x1801744AE   0x1801744AF   0x1801748F3   0x180174930   0x180174A4C
                  TaskSelStage : la case ALEA, dont l'icone est
                  `stage_icon_rnd_c` et dont le champ +0x08 vaut 41
    0x18001422D   idem, ailleurs

### Ce qui aurait dû me le dire, et que j'avais sous les yeux

Deux choses, l'une et l'autre déjà écrites dans ce journal :

* **la garde du gestionnaire.** `0x18018EF6C : cmp edx, 0x29 ; jae` accepte
  0 à 40 — les 41 décors — et laisse 41 **dehors**. Une borne à `0x29` sur une
  table de 41 entrées ne dit pas « la table s'arrête là », elle dit « 41 n'est
  pas un décor » ;
* **le dump de la grille**, fait le jour même : la case [10] portait
  `decor 41 (?)` avec l'icône `stage_icon_rnd_c`. Le `(?)` était mon propre
  outil disant qu'aucun code à trois lettres ne correspond — et je l'ai lu sans
  le voir.

Lever la borne a rendu 41 **adressable comme descripteur** sans lui retirer son
sens de sentinelle ailleurs. Le décor s'y chargeait donc bel et bien, et le
tirage au sort aussi — d'où un décor de Final Showdown pris au hasard.

C'est la même faute de forme que la borne des compteurs de parties, dans
l'autre sens : là, une valeur qui ressemblait à un compte n'en était pas un ;
ici, une valeur qui ressemblait à une borne était **une valeur**.

### Le correctif

**Les décors ajoutés commencent à 42.** `DECORS_PREMIER_NEUF = 42`, et le
patcheur refuse `--variantes-neuf 41` en expliquant pourquoi, avec les sept
adresses. L'entrée 41 reste ce qu'elle était : un place-tenant que rien
n'atteint.

Vérifié dans le binaire produit :

    anneau 1 (le dojo) : [11, 42]
    code[41] = 'x00'   code[42] = 'd5r'   code[43] = 'x02'
    descripteur 42 : objset 6150, auth_3d 'STGD5R'
    descripteur 41 : objset 28, auth_3d 'STGDJO'   (place-tenant)

Et le contrôle avant vol passe à l'indice 42 : `RIEN A REDIRE`.

**La leçon** : une borne et une sentinelle se ressemblent, et le seul moyen de
les distinguer est de regarder le **saut** qui suit la comparaison. `jae`/`jb`
bornent ; `je`/`jne` testent une valeur. `tools/refs_plage.py` ne le dit pas —
il faudrait un balayage qui sépare les deux, et il tient en une expression
régulière.

## 2026-09-09 (34) — « il charge uniquement Training Room » : ce que ça dit, et ce que ça ne dit pas

Frédéric, à l'écran : **« il charge uniquement training room (décor de Jean
Kujo) »**.

Le fait qui compte est dans `rom/game_score.txt` : **`score.chara.17.name=KRT`,
`score.chara.17.stage=STGGYM`**. Training Room est le décor **maison** de Jean
Kujo. Ce n'est donc pas un décor au hasard — c'est celui de l'adversaire.

### Ce que j'ai vérifié, et ce que ça n'a pas donné

Balayage de tout `.text` pour les comparaisons à 41, en séparant les bornes des
sentinelles par **le saut qui suit** : 29 sites, dont 7 par égalité et 19 par
borne. Neuf bornes ne sont pas dans notre liste — le groupe `0x1800A2xxx` et
`0x180200748`.

Mais elles comparent à `0x29` **puis à `0x2D`** et rendent 2, 3 ou 4 : c'est un
classificateur sur une plage 41..45, pas la borne d'une table de décors. Et le
balayage des immédiats **ne dit pas à quel domaine appartient chaque
comparaison** : 42, 43, 45 ont aussi des tests d'égalité un peu partout, qui
peuvent porter sur des identifiants de personnage, d'état, de n'importe quoi.

**Je m'arrête donc là plutôt que de deviner.** C'est la limite d'un balayage, et
elle est déjà écrite : une énumération ne vaut que sa prémisse.

### Les deux lectures, et elles demandent des correctifs opposés

| | |
|---|---|
| **A** | le combat n'utilise pas le choix de STAGE SELECT dans ce mode : il prend le décor maison de l'adversaire. L'indice 42 ne serait alors **jamais demandé** |
| **B** | l'indice 42 **est** demandé, mais quelque chose le rejette ou le traduit en route |

### La mesure qui tranche, et elle tient en un point d'arrêt

`0x1800D7130` est **l'unique chargeur de décor** — mesuré le 2026-09-05, deux
appelants seulement. Un point d'arrêt dessus donne, pour chaque chargement,
l'**indice demandé** (`ecx`) et l'**appelant** (l'adresse de retour).

`tools/pister_decor.py` le fait déjà ; il nomme désormais les indices ajoutés
(`ALEA(41)`, `ajoute-42`…). Lanceur : **`tools/pister_decor_ajoute.cmd`** — le
build du décor ajouté, lancé sous débogueur, clavier libre, journal écrit **au
fil de l'eau** dans `analysis/pister_decor.txt`.

Si le journal ne montre jamais `index 42`, c'est A. S'il le montre suivi d'un
autre chargement, c'est B, et l'adresse de l'appelant dira où.

## 2026-09-09 (35) — la mesure : `index 39 (gym)`, et 42 jamais demande

Le journal, apres un combat Akira contre Jacky :

    points d'arret poses a t=8 s
    CHARGEMENT : index 39 (gym)  <- appelant inconnu 0x7FFC8184F8A8

**Une seule demande, et l'indice 42 n'apparait jamais.** C'est la lecture A :
le choix de STAGE SELECT n'arrive pas jusqu'au combat.

### Deux corrections de lecture, dont une de mon outil

**L'« appelant inconnu » etait parfaitement connu.** `0x7FFC8184F8A8 - 0x18F8A8
= 0x7FFC816C0000` : c'est le **chargeur general** `0x18018F8A8`, celui qui lit
l'indice dans `[rsi+0x5C]`. `pister_decor.py` comparait l'adresse de retour a
`0x18018F8A8` **en adresse d'image**, alors que le module est rebase a chaque
lancement. Corrige : on compare des RVA. Un outil qui dit « inconnu » pour ce
qu'il connait fait perdre plus de temps qu'il n'en gagne.

**Et ce n'est pas le decor maison de l'adversaire.** Akira contre Jacky :
`game_score.txt` donne `AKI -> STGDJO` et `JAK -> STGNYC`. Ni l'un ni l'autre.
Ma premiere lecture de « Training Room » etait fausse.

### D'ou vient 39, lu dans le code

Le combat demande `session+0x4C` (`0x1800B48D0`, un getter d'une instruction),
via `0x1800BC6AD`. Et il existe un endroit qui pose l'indice **en dur** :

    0x18020AE50   mov [0x180754A28], ecx      le mode
                  cmp ecx, 1                  ... si c'est le mode 1
                  test dl, dl
                  mov eax, 0x27               39 = gym
                  mov ecx, 0x0B               11 = djo
                  cmovne eax, ecx             dl != 0 -> djo, sinon -> gym

**Le mode 1 choisit gym ou djo, en dur, sans jamais consulter STAGE SELECT.**
C'est le chemin de l'entrainement, et c'est tres exactement ce qu'on a vu :
Training Room.

Il y a un second site du meme genre en `0x180203F0F`.

### Ce que ça change pour le decor ajoute

**Rien ne dit encore qu'il est faux.** On ne l'a jamais demande : le mode
emprunte ne consulte pas le choix de decor. La question devient « quel chemin
transporte le choix de STAGE SELECT jusqu'a `session+0x4C` », et non « pourquoi
notre indice est-il rejete ».

`pister_decor.py` pose maintenant trois points d'arret de plus, qui repondent en
une seule mesure :

    0x1800BC6AD   la demande du combat      ecx = session+0x4C
    0x18020AE78   le choix EN DUR du mode 1 eax = 39 ou 11
    0x1800B8AFF   le decor maison           eax, avant la substitution Dural

Si `choix EN DUR du mode 1 = 39` s'affiche, tout est dit.

## 2026-09-09 (36) — le DOJO ne consulte jamais STAGE SELECT : `--dojo-decor`

Frédéric : **« je teste uniquement avec le mode dojo, la manette 2 est très mal
gérée, je n'arrive plus à lancer le mode versus »**.

Ça referme la question d'un coup. Le mode DOJO ne demande **jamais** le décor
choisi : il pose l'indice en dur, en cinq instructions —

    0x18020AE50   cmp ecx, 1        le mode 1
                  test dl, dl
    0x18020AE6E   mov eax, 0x27     39 = gym, la Training Room
    0x18020AE73   mov ecx, 0x0B     11 = djo, le dojo d'Akira
    0x18020AE78   cmovne eax, ecx

Le décor ajouté n'était donc **ni rejeté ni faux : il n'était pas demandé**. La
sonde le disait déjà — une seule demande, `index 39 (gym)`, et jamais 42.

### Le correctif, et il est d'une ligne

`--dojo-decor <indice>` remplace l'immédiat « djo » par celui qu'on veut. C'est
le seul chemin qui rende un décor ajouté visible **sans seconde manette**.

Deux lanceurs, et c'est volontairement une paire :

| | |
|---|---|
| `tools/dojo_5r.cmd` | `--dojo-decor 42` — le dojo de VF5 R, ajouté |
| `tools/dojo_5r_temoin.cmd` | `--dojo-decor 11` — le dojo d'origine |

**Le même build, le même chemin, un seul chiffre de différence.** C'est la leçon
du 2026-09-09 sur les deux lanceurs : quand l'un marche et l'autre pas, il faut
pouvoir comparer les invocations — autant les fabriquer comparables d'avance.

### Ce qu'il faut regarder, et ce que chaque symptôme dira

* le décor de 2008 a **40,8 Mo de textures** contre 20,9 en Final Showdown ;
* **ses murs** : un ring out dans un dojo n'existe pas. Si le personnage passe
  au travers, c'est `+0xC0` qui n'est pas suivi ;
* si le jeu **boucle sur l'écran de chargement**, le décor est demandé mais une
  pièce manque — un tout autre résultat que « rien ne se passe », et il y a sept
  portes à départager (`pister_import.py`).

### Ce qui reste ouvert, et qui n'est pas un détail

**La manette 2 est mal gérée, au point de bloquer OFFLINE VERSUS.** Ce mode
était validé le 2026-09-05 (clavier joueur 1, manette joueur 2, `--joueur2`,
`analysis/...` sur le lecteur d'entrées amputé). C'est donc soit une régression
de la journée, soit un défaut qui n'avait pas été vu. À reprendre, et à
mesurer — pas à supposer.

## 2026-09-09 (37) — 42 est PRODUIT puis remplace par 39

Frédéric : « `dojo_5r.cmd` lance training room, `dojo_5r_temoin.cmd` lance dojo
de FS, aucune trace de 5R ».

C'est un résultat **différent** du précédent, et meilleur : avant, l'indice 42
n'était jamais demandé. Maintenant il est **produit**, puis remplacé.

### Ce qui est vérifié

Le patch est bien posé — relu dans le binaire produit :

    apres --dojo-decor 42 : mov eax, 39 ; mov ecx, 42 ; cmovne eax, ecx

(Ma première relecture disait `mov ecx, 11` : elle portait sur le build
**témoin**, le dernier construit. Relire le bon fichier fait partie de la
mesure.)

### Ce que le témoin prouve, et ce qu'il ne prouve PAS

Il prouve que le mode DOJO charge bien `djo` quand rien n'est touché. Il **ne
prouve pas** que `0x18020AE50` est le site qui décide : un build non modifié
donne `djo` par n'importe quel chemin.

Mais changer la **valeur** de `ecx` a fait basculer le résultat sur `eax` (39),
et un `cmovne` ne regarde pas la valeur qu'il déplace. Donc soit le site est
bien celui-là et **42 est rejeté plus loin**, soit ce n'est pas lui et la
coïncidence est troublante. Les deux se départagent par la mesure, pas par le
raisonnement.

### Ce qui a été éliminé

Les deux seuls lecteurs de `0x180754A58` (`0x18020AA10`, `0x180209AF0`) ne font
que rendre la valeur, ou `-1` si un test échoue. **Aucun repli vers 39 chez
eux.**

### La mesure

`tools/pister_dojo_5r.cmd` : le build `dojo_5r`, sous débogueur, trois points
d'arrêt —

    0x18020AE78   le choix en dur du mode 1   -> eax, 42 ou 39 ?
    0x1800BC6AD   la demande du combat        -> ecx
    0x1800D7130   le chargeur                 -> l'indice charge

* CHOIX 42 et DEMANDE 39 → le remplacement est entre les deux ;
* CHOIX déjà 39 → ce n'est pas ce site-là qui décide, et le témoin nous a
  trompés.

### Au passage : un contrôle qui accusait à tort

`verifier_lanceurs.py` a annoncé « 25 LANCEUR(S) A REPARER » avec vingt-cinq
tracebacks. Aucun n'était cassé : **`vfes.exe` tournait** et tenait la DLL, donc
`patch_moteur.py` ne pouvait pas la réécrire. Un contrôle qui accuse à tort est
pire qu'un contrôle absent — il envoie chercher un défaut qui n'existe pas. Il
détecte désormais le jeu en cours d'exécution, le dit, et saute cette partie.

## 2026-09-09 (38) — la sonde tue ma piste : `0x18020AE78` ne s'exécute JAMAIS

Le journal de `pister_dojo_5r.cmd`, sur le build `--dojo-decor 42` :

    CHARGEMENT : index 39 (gym)  <- CHARGEUR GENERAL (index variable)
    BP Chargeur                            : 1 passage(s)
    BP Choix : demande du combat  ecx      : 0 passage(s)
    BP Choix : choix EN DUR du mode 1  eax : 0 passage(s)
    BP Choix : decor maison       eax      : 0 passage(s)
    BP Etape1 / Etape2                     : 0 passage(s)

**Les trois sites que je soupçonnais ne s'exécutent pas.** Un seul chargement,
par le chargeur général, qui lit son indice dans `[rsi+0x5C]`.

Le correctif de l'appelant, lui, marche : le journal dit maintenant
« CHARGEUR GENERAL » là où il disait « appelant inconnu ».

### Ce que je croyais, et ce que ça valait

J'ai bâti trois hypothèses successives sur des lectures de code, et les trois
sont tombées :

1. « le décor de l'adversaire » — faux, ni `AKI→STGDJO` ni `JAK→STGNYC` ;
2. « le mode DOJO pose l'indice en dur en `0x18020AE50` » — le site ne tourne
   pas ;
3. « le témoin prouve que c'est ce chemin » — il ne prouvait que « un build non
   modifié charge `djo` », ce que n'importe quel chemin donne. Je l'avais écrit
   en le construisant, et je m'y suis quand même appuyé.

**Les deux lanceurs sont bien identiques à un chiffre près** — diff fait, une
seule ligne, `--dojo-decor 42` contre `11`. Ce n'est donc pas une différence
d'invocation.

### La mesure suivante, et c'est la bonne famille

Le chargeur lit `[TaskStage+0x5C]`, soit `[0x1807499D8] + 0x5C`. Toute la
question est « qui a mis 39 dedans ». Chercher le prochain candidat par la
lecture serait refaire la même erreur une quatrième fois.

**`tools/pister_5c_stage.py`** (lanceur `tools/pister_5c_dojo.cmd`) pose un
point d'arrêt **MATÉRIEL en écriture** sur ce champ et laisse le processeur
nommer l'écrivain — exactement ce qui avait tranché l'affaire du1 le
2026-09-08, quand huit candidats se valaient à la lecture.

Le journal donne, avec des **temps** : chaque écriture, sa RVA, la valeur
écrite, puis le chargement. La dernière écriture avant le chargement est celle
qui décide. Les temps séparent le démarrage (l'attract) de ce qui se passe
quand on entre dans le mode — et il n'est pas exclu que le seul chargement vu
soit celui de l'attract, ce que la sonde précédente ne pouvait pas dire.

## 2026-09-10 (39) — le 39 était un ÉCRÊTAGE, deux appels avant `TaskStage`

Reprise avec le seul journal de la veille. La sonde `pister_5c_dojo.cmd` avait
bien tourné, à 23h24, et son résultat n'avait pas été lu :

    DR arme sur 0x20F6DBBCE5C (t=2.7 s) -- valeur actuelle tst
    t=  50.5 s  ecriture depuis 0x7FFD2F000B82 (rva 0x879F0B82) -> 4277075694
    ... cinq fois

Trois choses s'y lisent, et aucune n'est celle qu'on cherchait :

* `4277075694` = `0xFEEEFEEE`, le remplissage de tas d'un bloc **libéré**, et
  l'écrivain est `ntdll` : l'objet surveillé avait été **détruit** ;
* « valeur actuelle tst » était un champ à **zéro** — `tst` est l'indice 0. Un
  affichage qui nomme sans donner le nombre transforme un champ vide en
  résultat ;
* aucun `CHARGEMENT` dans le journal : la partie n'avait pas atteint le combat.

### Le champ surveillé ne pouvait rien dire

`+0x5C` n'est écrit que par **UNE** instruction dans tout le binaire. Le
validateur `0x18018EF40`, appelé à chaque trame :

    0x18018EF44  movsxd rdx, [rcx+0x60]      la DEMANDE
    0x18018EF48  cmp edx, -1 ; je            rien a faire
    0x18018EF65  mov [rcx+0x58], 1           etat 1 : chargement
    0x18018EF6C  cmp edx, 0x29 ; jae         la borne des 41 decors
    0x18018EF71  imul r8, rdx, 0xF0          le descripteur
    0x18018EF87  mov [rcx+0x68], r8
    0x18018EF8B  mov [rcx+0x5C], edx         la RECOPIE
    0x18018EF8E  mov [rcx+0x60], -1          demande consommee

Surveiller `+0x5C` ne pouvait donc nommer que cette recopie. Et `TaskStage` est
**créé et détruit** en cours de partie — `0x18018EE30` publie le pointeur en
`0x1807499D8`, `0x18018EEA0` le remet à zéro — donc un DR armé une fois sur
`objet+0x5C` finit forcément sur un bloc rendu au tas.

### La chaîne, lue d'un bout à l'autre par des énumérations complètes

Le décideur est celui qui écrit `+0x60`. Un balayage linéaire compte **233**
écritures de 32 bits en `[reg+0x60]` : hors de portée par la lecture. Mais le
singleton, lui, n'a que **21 références**, toutes dans le même bloc
`0x18018EE30`–`0x18018FE51`, et l'unique écrivain de `+0x60` est
`0x18018FD01`, dans la feuille `0x18018FCF0` — `TaskStage::demander(ecx)`.
Cette feuille a **trois** appelants. Le troisième, `0x1802035AA`, passe
`[params+0xD0]`. Et le global des paramètres n'a que **14** références.

De là, tout se déroule sans un seul candidat choisi à la lecture :

    0x18020AE60  mov [0x180754A58], r9d       l'indice du mode
                                              2 appelants : r9d = -1 EN DUR
                                              (0x1801E51FB), ou [0x180C406FC]
    0x180209B16  cmovne ebx, [0x180754A58]    si le mode console est actif
    0x180209B31  call 0x180203E40 (ecx=ebx)   les parametres du combat
    0x180203F0F  mov eax, 0x27                39 = gym
    0x180203F1E  cmp ebp, 0x28
    0x180203F2E  cmova ebp, eax               >>> au-dessus de 40 : 39 <<<
    0x180203F34  mov [params+0xD0], ebp
    0x1802035A4  mov ecx, [params+0xD0]
    0x1802035AA  call 0x18018FCF0             TaskStage::demander
    0x18018FD01  mov [TaskStage+0x60], ecx    la demande
    0x18018EF8B  mov [TaskStage+0x5C], edx    la recopie
    0x18018F8A3  -> le chargeur, index = [+0x5C]

**`cmova` est un écrêtage NON SIGNÉ.** L'appelant `0x1801E51FB` pose
`r9d = -1`, soit `0xFFFFFFFF` : au-dessus de 40, donc remplacé par **39, gym**.
Le décor ajouté n'était ni rejeté ni même demandé — son indice était remplacé
**deux appels avant** que `TaskStage` en entende parler. Et cela explique tout
d'un coup : le seul chargement `index 39 (gym)`, l'insensibilité à
`--dojo-decor`, et les zéro passages mesurés sur `0x18020AE78` (le bloc 39/11
est dans la branche `mode == 1`, que le DOJO ne prend pas).

### Pourquoi aucune des six bornes ne l'avait attrapé

Les six ont été trouvées en énumérant les **lecteurs des deux tables de
décors**. Celle-ci ne lit aucune table : elle assainit un indice avant de le
ranger dans les paramètres du combat. Une borne n'est donc pas forcément un
`jae` devant une table (cf. `reference_borne_ou_sentinelle`) ni une sentinelle
`je` sur une valeur : **elle peut être un `cmov` avec valeur de repli**, et
cette forme-là est invisible pour qui cherche les lecteurs d'une table.

Balayage de tout `.text` pour la forme « `cmp reg, 40/41` … `cmov` » : quinze
sites. Neuf sont le groupe `0x1800A2xxx`, le classificateur déjà écarté le
2026-09-09 ; `0x1801750AF` est un `cmove` sur 41, le code aléatoire ;
`0x180203F1E` est **le seul** qui écrête un indice de décor. La prémisse de ce
balayage, écrite pour pouvoir être attaquée : il ne voit que la forme
`cmp`+`cmov`. Un écrêtage écrit en branchement (`cmp` / `jbe` / `mov`) lui
échapperait.

### Ce qui est livré

| | |
|---|---|
| `--decor-ecretage <N>` | porte la borne de 40 à N-1, comme `--decors-table` pour les six autres |
| `--decor-repli <i>` | remplace le repli `gym` par l'indice `i` — le seul geste qui donne un décor quand l'appelant ne demande **rien** |
| `tools\dojo_5r_repli.cmd` | le décor ajouté vu du DOJO. Trois options d'écart avec `dojo_5r.cmd`, énoncées dans son en-tête, et `dojo_5r.cmd` sert de témoin : lui donne la Training Room |
| `tools\pister_60_dojo.cmd` | la sonde refaite : DR sur le **pointeur** (donc réarmée à chaque création de tâche), DR sur `+0x60` et `+0x5C`, et quatre points d'arrêt logiciels le long de la chaîne, dont l'écrêtage lui-même |

La sonde relit la **borne vivante** et le **repli vivant** dans le processus
plutôt que de les supposer : elle reste juste sur un build patché, et elle dit
`ECRETE` ou `passe` au lieu de laisser déduire.

`pister_5c_dojo.cmd` et `pister_5c_stage.py` restent en place : leur journal est
la mesure qui a tué la piste `+0x5C`, et le nom dit lequel est lequel.

### Ce que ça ne dit pas encore

Le lanceur n'a **pas encore été lancé** — personne n'a vu le décor ajouté à
l'écran. Deux résultats possibles, et ils se départagent seuls :

* le dojo de 2008 s'affiche : la chaîne est prouvée de bout en bout ;
* c'est encore la Training Room : alors `[0x180754A58]` ne vient pas de
  l'appelant à `-1`, et la sonde le dit en une partie.

## 2026-09-10 (40) — il manquait une DIXIÈME pièce, et le DOJO a bien un écran de sélection

Deux retours de Frédéric sur `dojo_5r_repli.cmd`, et les deux comptent :

1. **« une fois le décor akira 5R sélectionné, le chargement ne finit jamais »** ;
2. **« une erreur que tu as commise hier : le mode dojo propose bien un écran de
   sélection des décors »**.

### La correction d'abord, parce qu'elle était écrite partout

« Le mode DOJO ne consulte JAMAIS STAGE SELECT » était **faux**. C'était écrit
dans `PROMPT_REPRISE.md`, dans quatre lanceurs et deux fois dans
`patch_moteur.py` — corrigé aux sept endroits, avec la date et le fait qu'elle a
été tranchée, pour qu'on ne la réécrive pas.

Ce qui reste vrai, et qui est mesuré : le bloc `0x18020AE50` (39 `gym` / 11
`djo` selon un drapeau) est dans la branche `mode == 1`, **zéro passage**, donc
`--dojo-decor` patche un immédiat qui ne s'exécute pas ; et quand rien n'est
demandé (`r9d = -1`), l'écrêtage `0x180203F2E` en fait 39. Les deux constats de
la veille tiennent ; c'est la conclusion qu'on en tirait qui était trop large.
**L'écrêtage était bien le verrou** : le décor sélectionné à l'écran arrive
maintenant jusqu'au chargeur — le chargement commence, ce qu'il ne faisait pas.

### Le chargement qui ne finit jamais : SIX chemins d'éclairage, pas cinq

`0x1800D7130` compose, pour le code à trois lettres du décor :

    ./rom/ibl/<code>.ibl                          0x1800D71C1
    ./rom/light_param/light_<code>.txt            0x1800D71EA
    ./rom/light_param/fog_<code>.txt              0x1800D720E
    ./rom/light_param/glow_<code>.txt             0x1800D7232
    ./rom/light_param/wind_<code>.txt             0x1800D7256
    ./rom/light_param/envmap_correct_<code>.txt   0x1800D727A   <- absent

`decor_neuf.py` posait **neuf** pièces ; il en fallait dix. Et le contrôle avant
vol vérifiait les mêmes neuf : il annonçait « RIEN À REDIRE » sur un jeu
incomplet — un contrôle qui ne voit pas la panne qu'il est censé attraper.

**Pourquoi `envmap_correct_*` manquait** : il **n'existe pas dans le dump VF5R**
de 2008. C'est un fichier de Final Showdown. Les 41 décors du jeu en ont un
(41 fichiers dans le `.par`), donc il n'est pas optionnel. On le prend dans le
`.par` sous le code du modèle : ce sont neuf nombres,
`1\n1\n1\n0\n0\n0\n0.15\n-0.75\n0.4\n` pour `djo`, sans aucun nom de décor —
la recopie est exacte.

**Et pourquoi le décor qui REMPLACE ne montrait rien** : en remplacement le code
reste `djo`, et seuls les neuf noms posés sont masqués dans le `.par` —
`envmap_correct_djo.txt` de l'archive continuait de répondre. Seul l'AJOUT
expose le trou. C'est la même leçon que « le `.par` avant le disque », prise par
l'autre bout : ce que l'archive fournit encore masque ce qu'on a oublié.

### Ce qu'un décor demande, en entier

Onze fichiers portent le code d'un décor dans le `.par` (`par_inventaire.py
--grep "(?i)djo"`), et non neuf :

| | |
|---|---|
| `stg<code>.farc` | l'objset |
| `STG<CODE>_COLI.000.bin` | la collision |
| `STG<CODE>.farc`, `EFFSTG<CODE>.farc` | les deux auth_3d |
| `<code>.ibl` | l'éclairage |
| `light_ fog_ glow_ wind_ envmap_correct_<code>.txt` | les **cinq** light_param |
| `se_stage_<code>.acb` | l'ambiance sonore — **pas** à poser, voir plus bas |

### Le son d'ambiance ne bloque pas, et c'est mesuré, pas supposé

`rom/sound/se_stage_<code>.csb` n'est ni composé ni dans le descripteur — le
descripteur de `djo` porte ses deux noms d'auth_3d, sa collision et ses **dix**
`.adx` de musique, rien d'autre. Le chemin vient d'une **liste d'association**
en `0x180408850` : 24 entrées `{indice, pointeur}`, parcourues linéairement par
`0x1801903F3`, terminée par un pointeur nul.

**Un indice absent n'échoue pas** : `rdx` garde la valeur posée par défaut en
`0x1801903DC`, le jeu de sons de `are`. Le décor ajouté a donc l'ambiance de
`are`, et rien ne bloque. Pour lui donner celle de `djo` il faudrait ajouter
`{42, 0x1804084C0}` — mais la liste est suivie **immédiatement** de ses chaînes
(`0x1804089E0` porte `rom/sound/se_stage_are.csb`), donc il faudrait la
déplacer, comme les trois autres tables. Pas fait, pas urgent, et écrit ici pour
que ça ne se redécouvre pas.

C'est la troisième forme de table rencontrée sur ce chantier : table indexée
(descripteurs, codes), tableau dans une structure (compteurs de parties), et
maintenant **liste d'association avec valeur par défaut**. Celle-ci est la seule
qui pardonne un indice inconnu.

### Livré

* `decor_neuf.py` pose **dix** pièces, la dixième extraite du `.par` sous le code
  du modèle (`extraire_du_par`, qui refuse un fichier comprimé plutôt que de
  rendre des octets faux) ; `--retirer` et `--etat` suivent ;
* `controle_decor_neuf.py` vérifie les dix ;
* le décor `d5r` a été retiré et reposé : dix pièces présentes, contrôle « RIEN
  À REDIRE » ;
* `dojo_5r_repli.cmd` inchangé côté build ; son en-tête dit ce qui a changé.

Personne n'a encore vu le décor à l'écran.

## 2026-09-10 (41) — la dixième pièce ne suffit pas ; et une adresse en dur lisait le mauvais décor

« Temps de chargement infini » de nouveau, avec `envmap_correct_d5r.txt` posé.
Donc ce n'était pas ça, ou pas seulement ça. Ce qui est acquis quand même : le
décor est **demandé** et le chargement **démarre** — l'écrêtage était bien le
verrou de la demande.

### Ce que la lecture élimine, avant de mesurer

Le descripteur 42 du binaire patché, relu champ par champ :

    +0x00  STGD5R                          +0x48  rom/STGD5R_COLI.000.bin
    +0x08  EFFSTGD5R                       +0x68..+0xB0  les dix .adx de djo

Les dix musiques pointent celles de `djo`, qui existent — donc rien à poser de ce
côté, et le descripteur n'est pas en cause. Le contrôle avant vol de
`pister_import.py` est propre : dix fichiers posés, aucun nom resté visible dans
le `.par`, et les cinq objets demandés (`6150:114..118`) présents dans l'objset
posé. Trois objets viennent de l'objset **commun** (`0:28389..28391`), non
vérifiables sans le charger.

Il reste donc la barrière de l'état 3, et c'est exactement ce que la sonde des
sept portes sait nommer.

### LE PIÈGE : `TABLE_RVA = 0x403430` en dur, alors que la table a DÉMÉNAGÉ

`pister_import.py` lisait le descripteur à `0x180403430 + indice*0xF0`. Or
`--decors-table 44` **déménage** la table dans `.decors` : dans le build du jour
elle est à `0x180EA2000`. À l'ancienne adresse, l'indice 42 rendait le
descripteur de… `du5` — `STGDU5`, `rom/STGDU5_COLI.000.bin`, les musiques de
`dur`. Aucun message : des octets plausibles, tous les champs au bon endroit,
un décor qui n'a rien à voir.

C'est la variante « adresse en dur » de la leçon des tables déplacées, et elle
est sournoise parce que le résultat **ressemble** à un descripteur. La table se
lit maintenant comme le moteur la lit : le `disp32` du `lea` de `0x18018EF78`
(`table_des_descripteurs`). Une adresse de table en dur dans un outil, sur ce
chantier, est désormais un défaut par construction.

### Livré

* `pister_import.py` : la table est **lue**, pas supposée ; `--indice <n>` pour
  un décor ajouté (il n'est pas dans la liste des 41) ; `morceaux()` compte la
  dixième pièce ;
* `tools\depister_5r_ajoute.cmd` : le build de `dojo_5r_repli.cmd`, puis les
  sept portes. C'est la mesure qui nomme la pièce qui manque encore.

La porte 7 (sons d'ambiance) ne peut pas bloquer — liste d'association avec
valeur par défaut, voir l'entrée (40). Restent six candidates, et le journal en
retiendra une.

## 2026-09-10 (42) — le moteur ne lit PAS notre `obj_db.bin` : il prend celui du `.par`, masqué ou pas

La sonde des sept portes a rendu le verdict, et ce n'était aucune des sept :

    t=  84.8 s  etat 1, 2, 3   decor courant AJOUTE-42
    ... les NEUF autres pieces sont ouvertes ...
    t=  85.3 s  etat 4 (derniere attente)      -- et jamais l'etat 5

`stgd5r.farc` **n'est jamais ouvert**, alors qu'en remplacement `stgdjo.farc`
s'ouvrait dès l'état 2. La géométrie n'est donc pas refusée : elle n'est pas
demandée. L'état 4 attend un objset qui n'a jamais été réclamé.

### Le vecteur d'objsets du moteur ne contient pas le nôtre

`0x1800F9450` est un **lower_bound** sur un vecteur d'enregistrements de 0x200
octets, clé en tête, atteint par `[[0x18070FA90]]` (deux indirections — la
première lecture, à une seule, rendait 94 098 entrées et des clés absurdes ; une
indirection oubliée ne se signale pas, elle rend des octets).

`tools/pister_objset.py` le lit dans le processus vivant, **sans aucune
navigation** :

    vecteur : 6044 entrees de 0x200 octets, cles TRIEES, min 0, max 6149
    notre objset 6150 : ABSENT
    la dichotomie du moteur tombe au rang 6044 -> RATE

6044, c'est le compte de l'`obj_db.bin` **d'origine**. Le nôtre en a 6045.

### Trois mesures qui semblaient impossibles ensemble

* `obj_db.bin` est **masqué** dans l'index du `.par` — vérifié, et essayé des
  deux façons : dernier caractère (`obj_db.bi_`) puis premier (`Xbj_db.bin`) ;
* `tracer_fichiers.py --tout` ne montre **aucune** ouverture d'un chemin
  `rom/objset/…` sur le disque — seul le `.par` est ouvert. `auth_3d_db.bin`,
  lui, **est** ouvert sur le disque (deux fois) : le masquage marche pour lui ;
* retirer notre fichier posé ne change rien : toujours 6044.

Les entrées du `.par` ne portent aucun hachage de nom (huit dwords :
drapeaux, taille, taille comprimée, offset, trois zéros, un horodatage 2011),
donc le masquage aurait dû suffire.

### Ce que la mesure a tranché

`tools/pister_objdb.py` pose trois points d'arrêt dans le chargeur
`0x1800F97E0` :

    CHARGEUR obj_db appele : +0x90 (deja charge) = 0
    chemin compose : './rom/objset/obj_db.bin'
    octets rendus a 0x7FF46DA8A9F0 : 9c170000 05180000 60270400 50450000 803f0f00
    --> nombre de jeux = 6044  (6044 = L ORIGINE)

Le chargeur compose bien le bon chemin, et il reçoit les octets **d'origine**,
à une adresse qui n'est dans aucun module — une vue de fichier projetée, c'est-à-dire
le `.par`. **Le résolveur de ce loader consulte l'archive et n'y voit pas notre
masquage**, là où celui d'`auth_3d_db` tombe sur le disque. Deux fichiers, deux
ordres de résolution : ce n'est pas le masquage qui est en cause, c'est le
loader.

### La suite, et ce qu'elle coûte

Deux voies, et une seule est sûre :

1. **écrire notre `obj_db` DANS le `.par`** — remplacer les octets du membre.
   Il est comprimé en SLLZ (drapeaux `0x80000000`, 0x116A00 → 0x59D23) et le
   nôtre est plus gros de 5 769 octets, donc pas de remplacement en place : il
   faut le poser **non comprimé en fin d'archive** et réécrire son entrée
   d'index (drapeaux, taille, taille comprimée, offset). L'offset est un dword
   et la fin d'archive est à 3 987 499 008 < 2^32, donc ça tient ;
2. patcher le loader pour qu'il préfère le disque. Moins cher en octets, mais
   il faudrait d'abord lire son résolveur, et le `.par` restera la source pour
   tous les autres fichiers du même chemin.

La voie 1 ne demande aucune analyse supplémentaire : elle utilise ce que
`par_masquer.py` sait déjà faire de l'index.

### Combien de lancements, et pourquoi

Huit dans la séance, tous **sans navigation** (le vecteur et le chargeur sont
lus au démarrage) sauf celui des sept portes, qui était le seul à demander
d'aller au DOJO. Frédéric l'a fait remarquer : une sonde qui se pilote seule
reste un lancement de jeu sur sa machine. À grouper : une seule sonde qui pose
tous les points d'arrêt d'une question, pas une par hypothèse.

## 2026-09-10 (43) — les 50 secondes d'attente : une borne vérifiée APRÈS le balayage

Frédéric : « `decor_5r_akira.cmd` fonctionne mais il met énormément de temps à
démarrer. » Chronométrage de chaque étape, avant de toucher à quoi que ce soit :

    17,0 s   importer_decor.py --retirer trm      (et il n'y a RIEN a retirer)
    16,0 s   importer_decor.py --retirer trs      (idem)
    17,0 s   importer_decor.py --poser djo
     1,0 s   gen_apm_stub.py
     3,0 s   patch_moteur.py
     0,3 s   pister_import.py djo --controle
    -------
     ~54 s   avant que le jeu ne demarre

Trente-trois secondes sur cinquante-quatre étaient dépensées par deux étapes
**qui n'avaient rien à faire**.

### La cause

`par_masquer.positions()` cherchait un nom dans le `.par` **entier**, puis
sortait de la boucle une fois passé la borne du pot de noms :

    out, i = [], m.find(nom.encode())
    while i >= 0:
        if i >= borne:
            break

La borne était donc vérifiée **après** coup. Or `find` sans borne lit jusqu'à
trouver, ou jusqu'à la fin : une fois la dernière occurrence du pot dépassée, le
`find` suivant balayait les **3,99 Go** pour conclure « plus rien ». Deux
recherches par nom (le clair et le masqué), neuf noms par décor : ~16 s par
appel, et le lanceur en fait trois.

    i = m.find(cible, i + 1, borne)      # la borne DANS l'appel

C'est aussi plus juste : la recherche ne regarde plus jamais dans les données,
où `STGDJO_COLI.000.bin` a deux occurrences vers `0xEDD000`.

### Après

     0,24 s   --retirer trm
     0,23 s   --retirer trs
     0,26 s   --poser djo
     1,03 s   gen_apm_stub
     3,40 s   patch_moteur
     0,28 s   --controle
    -------
     ~5,4 s   au lieu de 54

Le contrôle avant vol passe toujours (« Rien à redire », les neuf noms masqués,
`envmap_correct_djo.txt` visible exprès). Ce qui reste est le démarrage du
moteur lui-même, qui n'est pas de notre ressort.

**La leçon, et elle vaut pour tous les outils du chantier** : une borne
vérifiée *après* un balayage ne borne rien — elle borne le résultat, pas le
travail. Quand on cherche dans un fichier de plusieurs gigaoctets, la borne se
passe à la fonction de recherche.

### Au passage, deux corrections de ma part

* j'avais cassé ce lanceur en rendant obligatoire, dans `pister_import.py`, la
  dixième pièce (`envmap_correct_<code>.txt`) : pour un décor qui REMPLACE, elle
  vient du `.par` et n'a pas à être posée. Le contrôle comptait deux fautes
  imaginaires et le lanceur s'arrêtait sans rien lancer ;
* j'avais aussi écrit `obj_db` dans le `.par` (entrée (42)) : annulé, entrée
  d'index rendue et archive retronquée à sa taille exacte. Vérifié : l'index ne
  diffère plus du dump que par les 29 noms qui doivent être masqués — les neuf
  du dojo posés par le lanceur, et les vingt fichiers d'interface de `rom/2d`.

Et une erreur de mesure à ne pas refaire : j'ai cru pendant une heure que le jeu
« démarrait puis mourait ». Il ne mourait pas — je lançais le `.cmd` depuis mon
propre shell, et la fin de mon appel emportait le processus. Lancé **détaché**,
comme le fait un double-clic, il reste debout. Le journal d'événements Windows
ne montrait d'ailleurs aucun plantage : c'est ce qui aurait dû me mettre la puce
à l'oreille tout de suite.

## 2026-09-10 (44) — les bases sont EMBARQUÉES dans le binaire, et c'est pour ça qu'`obj_db` n'était jamais lu

Trois mesures se contredisaient depuis l'entrée (42) :

* masquer `obj_db.bin` dans l'index du `.par` — des deux façons, dernier
  caractère puis premier — ne changeait rien ;
* `tracer_fichiers.py --tout` ne montrait **aucune** ouverture de
  `rom/objset/…` sur le disque ; seul le `.par` était ouvert ;
* écrire nos octets **dans** le `.par` (entrée d'index repointée, membre non
  comprimé en fin d'archive) ne changeait rien non plus.

La réponse était dans le binaire, et elle se lit en clair. Le moteur porte une
**archive `FArC` embarquée** en `0x1804137F0` :

    mot_db.bin        offset 0x00000136  comprime  83693   taille  290208
    obj_db.bin        offset 0x00014823  comprime 262037   taille 1141248
    tex_db.bin        offset 0x000547B8  comprime 184594   taille  841776
    spr_db.bin        offset 0x000818CA  comprime 418011   taille 1524752
    aet_db.bin        offset 0x000E79A5  comprime  15540   taille   45520
    rob_mot_tbl.bin   offset 0x000EB659  comprime  10188   taille   79808
    tst.ibl, light_tst, fog_tst, glow_tst, wind_tst, envmap_correct_tst

`obj_db.bin` y fait **1 141 248 octets** : l'original à l'octet près. Le
chargeur `0x1800F97E0` compose bien `./rom/objset/obj_db.bin`, mais le
résolveur consulte cette archive **d'abord**, décompresse le membre dans le tas
et rend un pointeur qui n'est dans aucun module — ce que la sonde montrait
depuis le début sans qu'on sache le lire.

**La preuve croisée est nette** : `auth_3d_db.bin` n'est **pas** dans cette
archive, et c'est justement la seule base dont le masquage du `.par` marchait
(`tracer_fichiers.py` la voyait s'ouvrir sur le disque). Les fichiers qui
ignoraient nos masquages sont exactement ceux qui sont embarqués.

### Le correctif : un octet

Le même geste que le masquage du `.par`, mais dans le binaire —
`--obj-db-libre` remplace le `n` de `obj_db.bin` par `_` en `0x18041381C`. Le
membre devient introuvable sous ce nom, le résolveur passe à la suite, et il
trouve notre copie. Le patcheur repartant toujours de `.origine`, retirer
l'option rend l'archive embarquée intacte. On ne touche qu'à `obj_db` : les
quatre autres bases embarquées n'ont aucune raison d'être libérées.

### Mesuré, et c'est le verrou qui saute

`tools/pister_objset.py`, sans aucune navigation :

    avant :  6044 entrees, max 6149, notre objset 6150 ABSENT   -> dichotomie RATE
    apres :  6045 entrees, max 6150, PRESENT au rang 6044       -> dichotomie TROUVE

Le moteur connaît enfin le jeu d'objets du décor ajouté. C'est ce qui manquait
pour qu'il demande `stgd5r.farc` — la géométrie n'était pas refusée, elle
n'était pas demandée (entrée (42)).

### État posé

`decor_neuf.py --poser d5r` écrit désormais `obj_db` **dans le `.par`**
(`par_ecrire.py`) au lieu de le masquer, `auth_3d_db` reste masqué et posé en
fichier libre, et `dojo_5r_repli.cmd` / `depister_5r_ajoute.cmd` passent
`--obj-db-libre`. Contrôle avant vol : « RIEN À REDIRE ».

### Au passage : ce que fait `--decor-perso`

Frédéric : « le décor d'Akira est correctement chargé mais attention il remplace
le décor TRM ». C'est l'option `--decor-perso djo` de `decor_5r_akira.cmd` :
elle fixe le décor de l'**écran de personnalisation / TERMINAL** (deux octets,
`0x1801C4DA7` et `0x1801C4DCC`, le troisième appelant de `0x18018FCF0`). Ce
build le met sur `djo`, donc sur le dojo de VF5 R. Ce n'est pas un effet de
bord du décor importé : c'est cette option-là, et `--decor-perso trm` la remet
sur le décor terminal.

## 2026-09-10 (45) — la QUATRIÈME table indexée par l'étage, trouvée en décompilant

Frédéric : « au lieu de faire des sondes à tout va, pourquoi tu ne décompiles
pas ? » Réponse honnête : parce que je croyais Ghidra absent, pour avoir cherché
dans `Program Files` et dans les dossiers vides de `VF5RE\ghidra`. **Il est
installé** — `C:\Users\frede\Desktop\Nouveau dossier\ghidra_12.1.2_PUBLIC_…`,
avec Java 21 dans le PATH. L'analyse complète de la DLL prend **107 secondes**.

Quatre tours de sondes n'avaient pas trouvé la cause. Le C de deux fonctions l'a
donnée en vingt minutes.

### La cause

Le passage de l'état 3 à l'état 4 appelle, avec l'indice du décor :

```c
void FUN_18006F620(int indice)                      // 0x18006F620
{
    for (p = &DAT_18034D510; *p != -1; p++)  charger_objset(*p, 1);
    FUN_18003C200("EFFEFFCMN");
    liste = &DAT_18034D570 + indice * 0x60;         // <<<< 41 ENTREES
    for (p = liste; *p != -1; p++)  charger_objset(*p, 1);
    DAT_180642FE0 = indice;  DAT_180642FE8 = liste;
}
```

et l'état 4 attend que **toute cette liste** soit chargée :

```c
else if (etat == 4 && FUN_18006FA60() == 0) {   // FUN_18006FA60 interroge la liste
    FUN_1800F8A40(descripteur[0x10]);           // notification, resultat IGNORE
    etat = 5;
}
```

À l'indice 42, la lecture sort de la table et tombe sur ce qui suit dans
`.rdata` — **des moitiés de pointeurs**, prises pour des identifiants
d'objset :

    [ 0..40]  premier entier = -1        (liste vide)
    [41]      -2144011768, 1, -2144011752, 1, …
    [42]      -2144011576, 1, -2144011552, 1, …

Le moteur demande ces objsets, ils n'existeront jamais, il les attend pour
toujours. Aucun message, et l'écran de chargement tourne.

### Ce que ça corrige de mes propres conclusions

* « l'objset ajouté n'est pas prêt » était **faux**. L'état 4 ne teste pas la
  disponibilité de l'objset : `FUN_1800F8A40` y est appelée pour **notifier**,
  et son résultat est ignoré. J'avais lu la fin d'une fonction voisine et bâti
  une théorie dessus ;
* les trois « drapeaux » `+0x90`, `+0x128`, `+0x138` sont bien réels, mais ils
  ne gardent pas cette porte-là. `+0x90` et `+0x128` sont **deux fois le même**
  drapeau : l'enregistrement d'objset embarque deux objets de chargement
  identiques, celui du `_obj.bin` en `+0x00` et celui du `_tex.bin` en `+0x98`
  (0x98 + 0x90 = 0x128).

### Le correctif

La table rejoint le déménagement de `--decors-table`, comme les trois autres.
Deux choses la rendent plus simple :

* **les 41 entrées réelles sont toutes vides.** Cette liste sert aux décors qui
  demandent des objsets *en plus* du leur, et aucun n'en demande. Une entrée
  neuve est donc un clone de l'entrée 0 — on ne fabrique pas un `-1` à la main ;
* **aucun pointeur dedans**, donc aucune relocation. Le correctif le vérifie
  quand même : il refuse si `.origine` porte la moindre relocation dans la
  plage. Et `refs_plage.py` ne trouve qu'**un seul** site à repointer, le
  `disp32` en `0x18006F675`.

Vérifié dans le binaire patché : les 41 entrées sont identiques à l'octet près,
les entrées 41, 42 et 43 commencent par `-1`, et le site vise `0x180EA3D40`,
dans `.decors`.

### Outils

* `tools/ghidra/DecompVF5.java` — le script headless qui sort le C d'une liste
  d'adresses (chacune cherchée **dans** sa fonction, pas à son début) ;
* `tools/decomp.py` — l'enveloppe : `py -3 tools/decomp.py 0x1800F9C60` ;
* projet `ghidra/vf5fs_apm3` (78 Mo), analyse faite. À refaire seulement si le
  binaire d'origine change.
* sorties de la séance : `analysis/decomp_objset.c`, `decomp_resolveur.c`,
  `decomp_chargement.c`, `decomp_poll.c`, `decomp_barriere.c`,
  `decomp_porte_etat4.c`.

**La leçon de méthode, et c'est Frédéric qui l'a posée** : une sonde dit quelle
branche s'exécute et quelle valeur vit dans un champ. Elle ne dit pas ce que le
code *fait*. Pour ça, on lit — et depuis aujourd'hui, on lit en C.

## 2026-09-10 (46) — le décor ajouté S'AFFICHE ; puis les flammes et le mur, deux tables de plus

**Le décor 42 se charge et s'affiche.** Frédéric : « le decor 5R est chargé ».
C'est le premier décor **vraiment ajouté** de ce chantier, et il aura fallu
lever quatre verrous pour qu'il apparaisse — l'écrêtage (39), la dixième pièce
(40), l'archive embarquée (44), la quatrième table indexée par l'étage (45).

Restaient deux manques, signalés dans l'ordre : **pas de flammes**, puis **pas
de mur**. Ils ont la même forme, et deux causes distinctes qu'il a fallu prendre
l'une après l'autre.

### 1. L'index des noms d'objets est GLOBAL, trié, lu par dichotomie

L'animation des flammes dit :

    object.0.uid_name       = STGDJO_EFF_FIRE_BMZ        un objet, par NOM
    object.0.tex_pat.0.name = F_VF5E_DJO00_IK_FIRE_000   une texture, par nom

et `FUN_1800F8B50` résout ce nom dans un **index global** `{nom, valeur}` de
16 octets, `[gestionnaire+0xC8..+0xD0]`, **trié par nom**, parcouru par
dichotomie — bâti depuis `obj_db`.

`decor_neuf.py` déclarait notre objset 6150 avec les **171 noms du modèle**.
L'index en contenait donc deux exemplaires, et la dichotomie rend le
**premier** : celui de l'objset 28, `STGDJO`, qui n'est pas chargé dans un build
d'ajout. L'effet se liait à un objet d'un objset absent — rien à l'écran, aucun
message. La géométrie, elle, marchait : le descripteur ne demande pas ses objets
par nom mais par **identifiant empaqueté** (`6150:114`..`118`).

**Ceci corrige une règle qu'on avait écrite de travers** : « les noms d'objets se
recopient VERBATIM ». C'est vrai **dans l'archive** — elle est celle du modèle,
elle porte ses noms. C'est faux **dans `obj_db`**, où le doublon casse tout ce
qui se lie par nom.

`renommer()` substitue donc `STGDJO_` → `STGD5R_` (même longueur, en place)
dans trois endroits qui doivent rester d'accord :

| | |
|---|---|
| `obj_db` | les 171 objets déclarés |
| `auth_3d_db` | les uid de `EFFSTG<CODE>` |
| les `.a3da` eux-mêmes | membres de l'archive **et** contenu |

Les **textures ne sont pas touchées** : elles s'appellent `F_VF5E_DJO00_…`, sans
`STGDJO_`, et `tex_db` les déclare globalement sous ces noms-là.

Pour réécrire les archives d'animation, `farc.py` sait désormais **écrire** un
`FArc` brut — aller-retour prouvé à l'octet près sur les cinq membres. Le moteur
lit les deux variantes ; recomprimer aurait demandé de retrouver le gzip exact
de SEGA pour ne gagner que de la place.

### 2. Chaque tâche d'effet a SA table, indexée par le décor

Le renommage était nécessaire mais pas suffisant : les flammes ne sont pas
jouées par nom, elles sont **listées par numéro d'uid**, par décor, dans une
table propre à chaque tâche d'effet. À l'état 3, `0x18006F380` donne l'indice du
décor à chacune (`obj->vtable[7](obj, indice)`), et chacune y cherche son
entrée :

    TaskEffectAuth3D::setStage  0x1800706B0  -> table 0x18034FD20
        22 entrees {indice, pointeur vers une liste d'uid}, fin {-1, 0}
        djo (11) -> [1193, 1191, 1192] = HATA, FIRE, FIRE_REFLECT

    TaskEffectWall::setStage    0x1800843A0  -> table 0x180355C30
        32 entrees de 0x40 {indice, trois pointeurs, quatre qwords a zero}
        djo (11) -> {11, 0x180352060, 0x180352560, 0x180352568}

Ce sont des **listes d'association** : un indice inconnu ne plante pas, il ne
fait **rien**. D'où deux absences en silence, sur un décor par ailleurs complet.

Les deux tables sont pleines — après le terminateur de la table Auth3D viennent
des flottants — donc elles **déménagent dans `.decors`** avec les quatre autres,
et elles portent des pointeurs, donc avec leurs relocations.

**Les numéros d'uid ne sont pas écrits en dur.** `uids_correspondants()` lit
l'`auth_3d_db` **posé**, retrouve chaque animation du modèle par sa valeur
renommée, et garde l'**ordre du modèle** — c'est lui qui dit dans quel ordre le
jeu les joue. Si une correspondance manque, le patcheur **refuse** : cela
voudrait dire que `decor_neuf.py` et `patch_moteur.py` ne parlent pas du même
décor.

Vérifié dans le binaire patché :

    table Auth3D -> 0x180EA4DC0   les 22 entrees d origine IDENTIQUES
       [22] indice 42 -> [3475, 3473, 3474]   nos HATA, FIRE, FIRE_REFLECT
       [23] terminateur recopie
    table Wall   -> 0x180EA4F60   les 32 entrees d origine IDENTIQUES
       [32..34] indices 41, 42, 43 : clones complets de l entree de djo

744 pointeurs relogés (631 avant), six tables déplacées, dix sites repointés.

### Ce qu'un décor ajouté demande, à ce jour

| | |
|---|---|
| **dix** fichiers | les neuf de la génération source + `envmap_correct_` pris dans le `.par` |
| `obj_db` | une entrée d'objset, ses objets **renommés**, et le fichier **écrit dans le `.par`** (le masquage ne suffit pas : l'archive est embarquée dans le binaire) |
| `--obj-db-libre` | un octet dans le `FArC` embarqué, sinon le moteur ignore notre base |
| `auth_3d_db` | deux catégories, uid renommés, posé en fichier libre + nom masqué |
| les `.a3da` | membres et contenu renommés, réécrits en `FArc` brut |
| **six** tables déplacées | descripteurs, codes, grille, objsets en plus, effets a3d, effets mur |
| trois bornes | `--decors-table`, `--decor-ecretage`, et le repli si on veut le forcer |

### Ce qui reste

* **le voir avec ses flammes et son mur** : le build est posé, l'essai n'a pas
  encore été fait ;
* le décor ajouté a l'**ambiance sonore de `are`** (liste d'association
  `0x180408850`, valeur par défaut) — pas bloquant, écrit dans l'entrée (40) ;
* les décors ajoutés n'ont **pas de compteur de parties** (septième borne, un
  tableau dans une structure).

## 2026-09-10 (47) — les flammes brûlent, les barrières manquaient : un clone n'est pas un clone

Frédéric, après l'essai : « les flammes sont bien présentes sur la dernière
build, mais il n'y a toujours pas les barrières du ring ». Les deux manques
avaient été traités le même jour, de la même façon — une entrée clonée dans la
table de la tâche d'effet — et **une seule des deux corrections pouvait
marcher**.

### Ce que la table des murs porte réellement

`TaskEffectAuth3D` (les flammes) porte un pointeur vers une **liste de numéros
d'uid**, et rien d'autre. On l'avait reconstruite avec nos numéros : correct,
et c'est pour ça que les flammes sont là.

`TaskEffectWall` porte **trois pointeurs**, et tout le mur est dans ce qu'ils
désignent. Lus dans `.origine` pour `djo` :

    +0x08 -> 0x180352060   28 morceaux de 0x2C : {objet, 10 flottants}, fin -1
    +0x10 -> 0x180352560   les uid, fin -1 : [1194]
    +0x18 -> 0x180352568   les paires de 0x10 : {intact, casse, uid, uid}

Les 28 morceaux **sont** la barrière, et c'est un plan lisible à l'œil nu :

    4 poteaux   objset 28 rang 113  STGDJO_EFF_POLE    aux quatre coins
                                                       (+-6, +-6), -45/45/135/225
   24 panneaux  objset 28 rang  47  STGDJO_EFF_FENCE   a +-1, +-3, +-5 le long
                                                       des quatre cotes

et la paire dit ce qui les remplace quand elles cassent :
`{28:47 FENCE, 28:48 FENCE_KOWARE, 1194, 1194}`, avec
`uid.1194.value = A STGDJO_EFF_KABE_REACT`.

**Objset 28. Uid 1194.** Le clone de l'entrée renvoyait donc au mur de `djo` :
un objset qui n'est pas chargé dans un build d'ajout, et un uid d'une autre
catégorie. `TaskEffectWall` ne trouvait rien à poser — **pas de barrière, et
pas un message.** C'est le défaut des flammes, un cran plus bas.

### Le correctif

`patch_moteur.mur_charge_modele()` lit les trois blocs du modèle **avant** de
dimensionner `.decors` (leur taille entre dans le calcul), et la boucle des
entrées neuves les y recopie en substituant :

| | |
|---|---|
| l'objset | 28 → 6150, **le rang ne bouge pas** (l'archive de 2008 a bien 47, 48 et 113) |
| les uid | 1194 → **3476**, retrouvé par sa valeur renommée `STGD5R_EFF_KABE_REACT` dans la base **posée** |
| `+0x08`/`+0x10`/`+0x18` | repointés sur les copies |

Trois refus, plutôt que trois suppositions : si le modèle porte des champs
`+0x20..+0x38` non nuls (non décodés), si ses trois pointeurs n'ont pas déjà
leurs **relocations** (une adresse écrite là ne survivrait pas au rebasage), ou
si un bloc nomme un objset autre que celui du modèle.

Vérifié dans le binaire patché :

    [33] indice 42 -> 0x180EA68F0  0x180EA6DF0  0x180EA6E00
         relocations en +0x08, +0x10, +0x18 : OUI
         28 morceaux : objset 6150 rang 47 x24, rang 113 x4
         uid [3476]
         paire 6150:47 -> 6150:48, uid 3476

### Le contrôle qui manquait, et son contrôle négatif

`controle_decor_neuf.py` a un **§6** : il lit les deux tables d'effets dans la
DLL **patchée**, suit les trois blocs du mur, et vérifie que chaque objet nomme
*notre* objset avec un rang présent dans l'archive posée, et que chaque uid est
de la catégorie `EFFSTG<CODE>`.

Le contrôle négatif est gratuit : les entrées 41 et 43 du même build sont des
clones de `djo` **non corrigés**, laissés exprès. Le contrôle lancé sur
l'indice 43 rend **36 fautes** — les 28 morceaux de mur, la liste d'uid, les
quatre champs de la paire. C'est mot pour mot ce que l'entrée 42 disait la
veille, sans que rien ne le regarde.

### La leçon, et c'est la troisième fois qu'elle se paie

Une table indexée par le décor a **deux** façons de mentir : ne pas avoir
d'entrée, ou en avoir une **qui désigne les données du modèle**. Un clone n'est
un clone que si ce qu'il pointe l'est aussi. Avant de cloner une entrée, lire
**ce qu'elle pointe**, et se demander ce qui, là-dedans, nomme le décor.

### Ce qui reste

* **le voir** : `tools\dojo_5r_repli.cmd`, MENU → DOJO ;
* les autres tâches d'effet (`Snow`, `Rain`, `Leaf`, `Ripple`…) ne sont
  toujours pas ouvertes — le dojo n'en utilise aucune, mais si l'une d'elles a
  la même forme que le mur, elle aura le même piège ;
* l'ambiance sonore reste celle de `are` ; pas de compteur de parties.

## 2026-09-10 (48) — la tâche n'existait pas : `EFFECT_WALL` n'était jamais créée

Frédéric, après le correctif (47) : « les barrières sont toujours invisibles
(mais la collision avec les barrières est bien gérée) ». Puis, à la demande,
deux témoins à l'écran qui ont tout tranché :

| | barrières |
|---|---|
| le dojo **d'origine** (indice 11), dans le build du décor ajouté | **oui** |
| le décor **ajouté** (indice 42), même build | non |
| l'archive de 2008 **à la place** de `djo` (`decor_5r_akira.cmd`) | **oui** |

Même binaire, même géométrie de 2008 : ni la table des murs, ni les objets, ni
les textures. **C'est l'indice.**

### La septième table, et elle était sous le nez

`0x18034D570`, 41 entrées de `0x60`, celle que ce chantier appelait « la table
des objsets en plus » et dont `patch_moteur.py` disait : *« les 41 entrées
réelles sont TOUTES VIDES »*. Cette mesure avait été faite sur les **quatre
premiers octets**. Une entrée en fait **96** :

    +0x00   8 identifiants d'objset a charger EN PLUS, fin -1   (toutes vides)
    +0x20  16 indices de TACHES D'EFFET a creer,       fin -1   (PAS vides)

Le `+0x20` est lu par `0x18006F380`, le créateur des tâches d'effet, et les noms
sont en clair dans `0x18034E4D0` : `EFFECT_HIT`, `EFFECT_AUTH3D`,
**`EFFECT_WALL`**, `EFFECT_LEAF`, `EFFECT_SNOW`, `EFFECT_RIPPLE`,
`EFFECT_THUNDER`, `EFFECT_RINGOUT_SPLASH`, `EFFECT_FOG_ANIM`,
`EFFECT_WET_CLOTH`, `EFFECT_BREATH`, `EFFECT_ELE_BOARD`…

Toujours créées (`0x18034D530`) : HIT, AUTH3D, DOWN, MOVE, PARTICLE, POISON.
**WALL n'en est pas.** `djo` demande `[2]` ; 32 décors sur 41 demandent 2.

Nos entrées neuves clonaient **l'entrée 0**, qui ne demande rien. Donc :
`TaskEffectWall` **n'était jamais instanciée** pour le décor 42, sa table
indexée par le décor — pourtant corrigée la veille — n'était jamais consultée,
et les 28 morceaux du mur restaient lettre morte.

**Et tout le symptôme s'explique, exactement** :

* les **flammes** marchaient : `EFFECT_AUTH3D` est toujours créée ;
* la **collision** marchait : elle ne vient pas de la tâche mais du descripteur
  `+0xB8`/`+0xC0`, posée par `0x18010CA20`…`0x18010CA60` dans le chargeur de
  décor. D'où « un mur qu'on ne voit pas et contre lequel on bute », qui était
  l'indice le plus utile de la séance ;
* rien dans le binaire ne lisait `gestionnaire+0x3B0` : je cherchais le lecteur
  d'un tableau publié par une tâche **qui n'existait pas**.

### Ce qui a été fait

* les entrées neuves de `0x18034D570` sont un **clone complet de l'entrée du
  modèle**, comme le descripteur et comme l'entrée de mur. Le patcheur refuse si
  la liste du modèle n'a pas de terminateur, ou si elle est vide ;
* le commentaire de `OBJSETS_TABLE_VA` est réécrit : il portait l'erreur ;
* `controle_decor_neuf.py` §7 lit la liste dans la DLL patchée et la compare à
  celle du modèle. Vérifié : `etage 42 : taches 2=EFFECT_WALL`, identique à 11 ;
* le correctif (47) sur la table des murs **reste nécessaire** : sans lui la
  tâche existerait et pointerait sur l'objset du modèle. Les deux vont ensemble.

### Effet de bord : la question du §17.1 est répondue

« Les autres tâches d'effet (`Snow`, `Rain`, `Leaf`, `Ripple`…) n'ont pas été
ouvertes » — elles n'ont **aucune borne à lever**. Il suffit que l'entrée du
décor les demande, et la table dit lesquelles chaque décor demande. Le jour où
on ajoutera un décor pluvieux, la ligne est écrite d'avance.

### La leçon

Une entrée se compare **en entier** à celle du modèle, ou pas du tout.
« Toutes les entrées sont vides » était une mesure faite sur 4 octets d'un
enregistrement de 96 — et elle a coûté deux essais à l'écran. Corollaire du
(47) : un clone n'est un clone que si ce qu'il pointe l'est aussi **et** si
l'enregistrement entier l'est.

## 2026-09-10 (49) — les barrières sont là, et les dix-neuf décors de VF5 R sont posés

Frédéric : « les barrières sont là ». Le premier décor **vraiment ajouté** du
chantier est donc complet — géométrie de 2008, flammes, barrières de ring — et
la recette tient. Suite immédiate, demandée dans le même message : ajouter tous
les décors de VF5 R.

### L'inventaire, croisé et non supposé

Les 41 descripteurs du binaire contre `extracted/decors/VF5R/` :

| | |
|---|---|
| **19 complets** | ban ter nyc cas riv jin sin djo umi hai are slk yuk tak aur bar tan gym smo |
| `du1`..`du4` | pas de `auth_3d/STGDU<n>.farc` — VF5 R range la scène des quatre décors de Dural sous **un seul** nom, `STGDUR.farc`. À établir, pas à deviner |
| `du5` | n'existe pas dans VF5 R |
| les 17 emplacements d'essai | 0 à 1,2 Mo, sans animation |

Indices **42 à 60**, objsets **6150 à 6168**, codes `<1re><3e>5` (`bn5`, `tr5`,
`nc5`…) sauf `djo` qui garde `d5r` — on ne renomme pas un build validé.

### Ce qu'il a fallu généraliser, et ce que ça a appris

**Un lot n'est pas N fois un.** `decor_neuf.poser` repartait de
`extracted/obj_db.bin` à chaque appel : dix-neuf appels auraient laissé le
dernier décor seul, en silence. Les fichiers se posent un par un, les **bases
une seule fois** (`poser_lot`).

**Chaque décor clone SON modèle**, pas `djo` — dans les cinq tables où il
apparaît. Le descripteur porte la musique et la configuration de l'anneau ;
la liste de tâches d'effet dit s'il y a de la pluie, de la neige, du
brouillard ; la table des murs et celle des animations sont indexées par le
décor.

**Quatre champs de mur de plus, décodés** (le dojo n'en utilisait aucun) :

    +0x20  un SECOND tableau de morceaux, meme forme que +0x08     nyc
    +0x28  EXACTEMENT DEUX uid : EFF_SAKU_UP / _DOWN (柵)          yuk, gym
    +0x30  {objet, uid, ., .} de 0x10, fin -1 : les cassables      umi hai aur tan
    +0x38  un uid par enregistrement de +0x30                      umi hai aur tan

Trois surprises, toutes mesurées :

* **`-1` est une valeur légitime** dans un champ d'objet — `ban` dit ainsi
  qu'un panneau n'a pas de version cassée. Le premier jet refusait ;
* **tous les uid d'un mur ne sont pas dans la liste `+0x10`** : `umi` cite 3361
  (`STGUMI_EFF_SAKU_BROKEN`) dans `+0x30`. On relève donc tous les uid du mur
  d'abord, puis on traduit en un seul appel ;
* **`tan` désigne un objet de `hai`** : son `+0x30` porte `34:545` avec ses
  propres uid. L'enregistrement de `hai` a été recopié chez SEGA et seul l'uid
  a changé ; l'objset n'étant pas chargé, l'objet ne fait rien — **déjà dans le
  jeu d'origine**. Le clone le recopie tel quel, et le patcheur le dit plutôt
  que de « corriger » ce qui n'est pas à nous.

**Un modèle sans mur n'en donne pas.** `riv` et `smo` n'ont aucune entrée dans
la table des murs. Le premier jet leur en fabriquait une, clonée de `djo` :
`controle_decors_5r.py` l'a vue tout de suite — 14 fautes, « 28 morceaux de mur
d'un autre objset ». C'est le défaut du (47) qui essayait de revenir.

### L'accès : dix-neuf anneaux

`--variantes-5r` pose un anneau par case de grille : la barre espace fait
passer la case de Final Showdown à VF5 R, avec le nom de la génération. Dix-neuf
des vingt et une cases ont leur double.

`VARIANTES_MAX_ANNEAUX` passe de 4 à 20, et trois choses ont dû suivre :

* les offsets des trois tableaux de la greffe étaient **en dur** (0x780 / 0x790
  / 0x820) ; ils sont dérivés maintenant, sinon ils se recouvraient ;
* la borne `cmp ecx, 160` ne tient plus dans un **imm8 signé** : imm32 au-delà
  de 127 ;
* `GREFFE_TAILLE` : `0x1000` → `0x3000` (le tableau des noms fait 5120 octets).

### L'état

* 19 décors posés, 382 Mo, `obj_db` écrit dans le `.par` (1 397 593 octets),
  `auth_3d_db` posé et masqué ;
* patch complet passé, `controle_decors_5r.py` : **RIEN A REDIRE** sur les 19 ;
* lanceurs `tools\decors_5r.cmd` et `tools\decors_5r_retirer.cmd` ;
* **personne n'a encore regardé l'écran.**

### Ce qui reste

* `du1`..`du4` : établir la correspondance avec `STGDUR.farc` ;
* les **noms** à l'écran sont ceux de la génération (`VIRTUA FIGHTER 5 R`), pas
  ceux du décor ;
* l'ambiance sonore d'un décor ajouté reste celle de `are` ;
* pas de compteur de parties pour les décors ajoutés.

## 2026-09-10 (50) — « nombreux plantages » : la sonde, et ce que le statique a déjà éliminé

Frédéric, après le build des dix-neuf : « nombreux plantages, instrumente pour
en déterminer la cause ».

### La sonde : `tools\plantage_5r.cmd`

`tools/pister_plantage.py` lance le jeu sous débogueur **sans toucher au
clavier** — c'est lui qui joue, elle regarde — et écrit **au fil de l'eau** dans
`analysis/pister_plantage.txt` :

| | |
|---|---|
| chaque **décor demandé** | point d'arrêt sur `0x18018EF87`, le seul site qui pose le descripteur. Le nom est résolu : « 47 (rv5, la version VF5 R de riv) » |
| les **sept portes de l'état 3** | un seul coup chacune, sinon le jeu rampe. La plus haute atteinte dit où le chargement s'arrête |
| chaque **exception** | code, adresse, **et dans quelle SECTION elle tombe** — si c'est `.decors`, dans quelle de nos tables et à quel offset |
| l'adresse **lue ou écrite** | située elle aussi |
| les **registres** et le **désassemblage autour de RIP** | pour lire l'instruction fautive au lieu de la deviner |
| les adresses de **retour applicatives** sur la pile | déjà fournies par `instrument.violation` |

Essai à vide, 90 s : le jeu atteint le titre et **ne plante pas tout seul**. La
seule exception est un `_com_error` de première chance dans `KernelBase`, que
`instrument.py` rapporte depuis toujours sur tous les builds. Le plantage
demande donc une navigation — la sienne.

### Ce que le statique a déjà éliminé

Avant de lui faire relancer quoi que ce soit, quatre contrôles :

* **les anneaux de la greffe** : 20 anneaux, comptes et indices exacts,
  `VAR_FIN = 0x1E50` bien à l'intérieur des `0x3000` de `.greffe` ;
* **la table des relocations** : 30 753 entrées de type 10 (29 643 à l'origine),
  **aucune hors section** ;
* **les descripteurs des dix-neuf modèles** : tous ont leurs relocations en
  `+0x00`, `+0x08` et `+0x48`, les trois champs que le patcheur réécrit. Une
  seule manquante aurait donné un pointeur à la base préférée — et des
  plantages partout ;
* **`verifier_decors_table.py`** : aucune faute.

### UN CONTRÔLE QUI MENT EST PIRE QUE PAS DE CONTRÔLE

`verifier_decors_table.py` annonçait **onze fautes**. Aucune n'était réelle : il
prenait `n = DECORS_TABLE_N` (41) **en dur** et cherchait la table des codes à
`+0x2670`, alors qu'à 61 décors elle est à `+0x3930`. Il lisait donc l'entrée 41
comme si c'étaient des codes, et déclarait vingt relocations manquantes.

Le nombre se **lit** maintenant dans le binaire : le `lea` des codes donne
l'adresse de la table, et `0xF0` étant multiple de 16, `n = (cible - base) /
0xF0` exactement. Il retombe sur 41 si le compte n'est pas crédible, et le dit.

### Ce qui reste

Le journal de la sonde, une fois qu'il aura fait planter le jeu. La question
qu'elle répond en une ligne : **quel décor était demandé**, et **où** ça tombe.

## 2026-09-10 (51) — le plantage : `VAR_NUM` avait quatre cases pour vingt anneaux

Frédéric a joué sous la sonde et fait planter le jeu. Le journal
(`analysis/pister_plantage.txt`) donne la réponse en trois lignes :

    EXCEPTION ACCESS_VIOLATION  a ...+0xEA11E7
      ou      : .greffe+0x1E7 (VA preferee 0x180EA11E7)
      acces   : LECTURE de 0x00007FFB06E718F0
      >>> 0x180EA11E7  mov eax, dword ptr [rdx + rcx*4]
          rcx=0000000043EB0048  rdx=00007FF9F73B17D0
      AUCUN decor demande avant ce plantage.

**C'est notre greffe**, et pas le moteur. `rdx` pointe `VAR_IDX` ; `rcx` vaut
`0x43EB0048` — un rang de tableau astronomique, là où on attend 0 à 159.

### D'où venait ce rang

Le sous-programme APPLIQUER fait :

```
mov ecx, eax          ; le rang rendu par TROUVER (anneau*8 + position)
shr ecx, 3            ; -> l anneau
lea rdx, VAR_NUM
mov edx, [rdx+rcx*4]  ; le NUMERO courant de cet anneau
shl ecx, 3
add ecx, edx          ; -> le rang final
lea rdx, VAR_IDX
mov eax, [rdx+rcx*4]  ; <<< ici
```

`VAR_NUM` était déclaré `0x600 # 4 u32 : le numero courant par anneau` — **en
dur, quatre entrées**. Le 2026-09-10 les anneaux sont passés de 4 à 20 pour les
dix-neuf décors de VF5 R, et j'ai dérivé `VAR_COMPTES`, `VAR_IDX` et
`VAR_TEXTES`… **en oubliant `VAR_NUM`**.

Au cinquième anneau et au-delà, `VAR_NUM[anneau]` lit `VAR_RANG` (0x610), puis
`VAR_APPLIQUE`, `VAR_PLAFOND`, `VAR_X`, `VAR_Y`, et enfin **`VAR_DESC`** — le
descripteur de texte, plein de flottants. `0x43EB0048` est l'un d'eux.

Et le pire n'est pas la lecture : l'entrée A **ECRIT** au même endroit
(`mov [rdx+rcx*4], eax`, le numéro incrémenté). Une pression sur la barre espace
sur n'importe quelle case au-delà de la quatrième écrasait donc le rang courant,
le descripteur de texte et son style. D'où « **nombreux** plantages », et d'où
le fait qu'ils tombent un peu partout et pas toujours au même endroit.

### Le correctif, et le contrôle qui manquait

`VAR_NUM` est **dérivé** comme les trois autres et posé après `VAR_TEXTES`, à
`0x1E50` — là où il y a de la place. La frontière code/données devient
`VAR_DONNEES = 0x600` (le bornage du créneau de vtable s'appuyait sur `VAR_NUM`).

Surtout, `verifier_disposition()` contrôle désormais que **aucune zone de la
greffe n'en recouvre une autre** et que tout tient dans la section, et
`variantes_greffe` l'appelle avant d'assembler quoi que ce soit. Contrôle
négatif : en remettant `VAR_NUM = 0x600`, il rend

    greffe : NUM (0x600..0x650) recouvre RANG (0x610)

C'est exactement le défaut, nommé.

### La leçon

Un tableau dimensionné **en dur** dans une greffe ne dit rien quand il déborde :
il écrit chez le voisin, et le jeu tombe ailleurs, plus tard, « souvent ». Le
journal (49) disait déjà « les trois tableaux étaient à des offsets en dur ;
ils sont dérivés maintenant, sinon ils se recouvraient en silence » — il y en
avait **quatre**, et le quatrième a coûté la séance. Une disposition se
**vérifie**, elle ne se relit pas.

## 2026-09-10 (52) — les cinq objets d'un décor ne sont pas aux mêmes rangs

Frédéric : « soit des plantages, des loadings infinis ou des décors qui se
chargent mais ils sont très incomplets. Je commence par aurora qui plante. »

Trois symptômes, **une seule cause**, et elle est dans le patcheur.

### `DECOR_NEUF_RANGS`, écrit en dur sur les rangs de `djo`

Le descripteur d'un décor demande cinq objets par `(objset << 16) | rang` :
gnd, ring, sky, sdw, reflect. `patch_moteur` écrivait
`DECOR_NEUF_RANGS = (114, 118, 117, 116, 115)` pour **tous** les décors
ajoutés. C'est juste pour `djo`, le premier — et faux pour les dix-huit autres :

    djo  114 118 117 116 115        aur  413 598 414  -1  -1
    ban  817 941 818  -1 942        gym    0 158   1  -1 151
    cas  151 181  -1 153 152        smo    0 308   1  -1  -1

Écrire les rangs de `djo` chez `aur` demande donc les objets 114 à 118 de
l'objset d'`aur` — des morceaux d'effet pris au hasard — et rate le sol, le
ring et le ciel. Selon ce que le rang visé contient, ça plante, ça charge sans
fin, ou ça affiche un décor très incomplet. **Les trois symptômes de la même
faute.**

Autre chose que ces relevés montrent : **onze descripteurs du jeu portent des
emplacements VIDES** (`0xFFFFFFFF`). `aur` n'a ni `sdw` ni `reflect`. « Pas
d'objet » est une valeur normale, pas une anomalie.

Les cinq champs se recopient donc du **modèle**, objset substitué et rang
inchangé, `0xFFFFFFFF` passé tel quel.

### Et le rang doit EXISTER dans l'archive de 2008

Le contrôle ajouté au passage — « les cinq rangs sont-ils dans l'archive
posée ? » — a immédiatement trouvé trois cas de plus :

    bn5 : rang 942 absent      jn5 : rang 439 absent      ae5 : rang 385 absent

C'est le même dans les trois : **`reflect`**. Le reflet est une addition de
Final Showdown ; la géométrie de 2008 ne l'a pas. L'emplacement est donc mis à
« pas d'objet », comme le jeu le fait lui-même ailleurs — et le patcheur le
**dit** au lieu de demander un objet qui n'existe pas.

`variantes_5r.ids_archive()` lit les identifiants de l'archive posée, avec un
cache : le patcheur et le contrôle s'en servent tous les deux.

### La leçon, et c'est la troisième fois de la journée

Une constante écrite en dur pour le PREMIER cas devient fausse au deuxième :

* (49) `VAR_COMPTES`, `VAR_IDX`, `VAR_TEXTES` — offsets en dur, corrigés ;
* (51) `VAR_NUM` — le quatrième, oublié, quatre cases pour vingt anneaux ;
* (52) `DECOR_NEUF_RANGS` — les rangs de `djo` pour dix-neuf décors.

À chaque fois la même forme : ça marchait sur le cas d'origine, et le lot l'a
cassé en silence. Et à chaque fois, le contrôle ne le voyait pas **parce qu'il
répétait l'hypothèse de l'outil qu'il contrôlait** — `controle_decors_5r.py`
comparait lui aussi aux rangs de `djo`. Un contrôle doit **remesurer**, pas
recopier.

### L'état

Les dix-neuf repassent le contrôle : `RIEN A REDIRE`. `ar5` (aurora) demande
maintenant `6164:413 6164:598 6164:414 - -`, exactement les objets de son
modèle. **Pas encore vu à l'écran.**

## 2026-09-10 (53) — l'analyse des dix-neuf : `obj_db` décrivait la MAUVAISE archive

Frédéric : « analyse tous les décors et leurs besoins spécifiques, sinon on ne
s'en sortira jamais ». Il a raison, et l'analyse systématique donne **deux
défauts de fond** que la chasse au plantage un par un n'aurait jamais rendus.

### 1. `obj_db` décrivait l'archive Final Showdown, on pose celle de 2008

`decor_neuf` déclarait dans `obj_db` **les objets du modèle FS**. Or l'archive
posée est celle de **2008**. Mesure sur les dix-neuf :

| | déclarés | archive 2008 | déclarés mais ABSENTS | présents mais NON déclarés |
|---|---:|---:|---:|---:|
| d5r | 171 | 119 | 52 | 0 |
| bn5 | 905 | 833 | 119 | **47** |
| jn5 | 643 | 447 | 196 | 0 |
| br5 | 364 | 328 | 94 | **58** |
| ae5 | 415 | 353 | 103 | **41** |

Les deux sens font mal :

* **déclaré mais absent** : un rang qu'on demande et que l'archive n'a pas — le
  chargement ne finit pas, ou l'objet manque ;
* **présent mais non déclaré** : les objets que 2008 a et que FS n'a plus. Ce
  sont exactement ceux que les `.a3da` **de 2008** nomment
  (`STGBN5_EFF_DOWNKEMU_BMZ_000`, `STGAE5_EFF_NEON1_MZ_000`…). Le nom est
  introuvable dans l'index global, l'effet ne se lie à rien, en silence.

**`obj_db` décrit l'archive qu'on POSE.** Les objets s'y déclarent en la
lisant : `variantes_5r.objets_archive()`.

### 2. `auth_3d_db` déclarait des uid sans leur `.a3da`

Même cause : on recopiait la liste d'uid du modèle FS. La génération de 2008 n'a
pas les mêmes animations — tous les décors manquent `EFF_DASH`, et surtout
**`aur`, `umi`, `hai` et `tan` n'ont ni `EFF_SAKU_BROKEN` ni leurs
`BROKEN_SHADOW`**.

Or c'est exactement ce que le `+0x30`/`+0x38` de leur entrée de mur référence —
les objets cassables. Et `TaskEffectWall`, créneau 1, **boucle sur
`FUN_180044640` jusqu'à ce que ses animations soient prêtes**. Un uid déclaré
sans son `.a3da`, c'est une promesse que le moteur attend : **chargement infini
ou plantage.** Ce sont les quatre décors à objets cassables — et `aur`
(aurora) en fait partie.

`decor_neuf` ne déclare donc que les uid dont le `.a3da` est **dans l'archive
posée**, et `patch_moteur` **tronque** ce que ces animations servaient plutôt
que de pointer sur un uid absent :

    ui5 hi5 ar5 tn5 : 0 objet(s) cassable(s) sur 1 -- 2008 n a pas l animation
    bn5 jn5         : animation d effet retiree de la liste

### L'analyse est maintenant dans le contrôle

`controle_decors_5r.py` vérifie **dix** choses par décor, dont les trois
nouvelles :

  8. `obj_db` décrit l'archive posée, **ni plus ni moins** ;
  9. chaque uid déclaré a son `.a3da` **dans** l'archive posée ;
 10. chaque objet nommé par un `.a3da` est déclaré dans `obj_db`.

Les dix-neuf passent : `RIEN A REDIRE`.

### Ce que l'analyse a aussi établi, et qui ne bloque pas

* les **tâches d'effet autres que WALL et AUTH3D** ont bien chacune leur table,
  et `TaskEffectBreath::setStage` est **trois comparaisons explicites** contre
  trois constantes, avec `return` si aucune ne correspond : un indice inconnu
  **ne fait rien**. Nos décors n'auront donc ni souffle, ni neige, ni brouillard
  — mais ça ne plante pas ;
* trois décors (`ban`, `jin`, `are`) n'ont **pas d'objet `reflect`** en 2008 :
  l'emplacement passe à « pas d'objet », comme onze descripteurs du jeu ;
* `riv` et `smo` n'ont **pas d'entrée de mur** du tout, et n'en reçoivent pas.

### La leçon

Chercher la cause d'un plantage à la fois aurait pris la semaine. L'analyse
systématique — *que demande chaque décor, et l'avons-nous ?* — l'a donnée en une
passe, et elle en a donné **deux** au lieu d'une. C'est Frédéric qui l'a
imposée.

## 2026-09-10 (54) — aurora : une tâche d'effet CRÉÉE SANS DONNÉES

Frédéric : « aurora plante encore, tes analyses sont médiocres, il y a encore
d'autres éléments que tu n'as que partiellement analysé ? ». Oui — et voici
celui qui faisait tomber aurora.

### `EFFECT_BREATH` ne connaît que trois décors

Le `+0x20` de `0x18034D570` dit quelles tâches d'effet créer. `aur` demande
**WALL et BREATH**. Or `TaskEffectBreath::setStage` n'est pas une table : ce
sont **trois comparaisons explicites**, et un `return` si aucune ne colle.

    0x1806430C0 -> 16 (yuk)    0x1806430D4 -> 18 (aur)    0x1806430E8 -> 21 (du1)

Notre indice 56 n'y est pas. La tâche est donc **créée**, `setStage` ne lui
donne **rien**, et sa mise à jour tourne quand même sur un état vierge.

C'est la même forme pour les autres : `FOG_ANIM` ne connaît que `are`, `SNOW`
que `yuk`, et ainsi de suite. **Dix des dix-neuf décors** demandaient au moins
une tâche que rien ne servait :

    43 RIPPLE SPLASH WET_CLOTH   51 THUNDER FOG_ANIM      54 SNOW BREATH
    44 LEAF                      52 FOG_ANIM ELE_BOARD    56 BREATH
    47 WET_CLOTH RINGOUT_SPLASH SPLASH                    53 WATER_RING RIPPLE SPLASH
    48 WET_CLOTH RINGOUT_SPLASH LEAF   49 WET_CLOTH RINGOUT_SPLASH

### Le correctif : ne demander que ce qu'on sait servir

`EFFETS_SERVIS = (2,)` — `EFFECT_WALL`, la seule dont on **pose** l'entrée
(avec `AUTH3D`, qui ne passe pas par cette liste). Toute autre tâche est retirée
de la liste du décor ajouté, et le patcheur le **dit**, décor par décor.

Le décor perd l'effet ; il ne perd rien d'autre. Chacune se rouvrira le jour où
on déplacera sa table, exactement comme on l'a fait pour WALL et AUTH3D.

### CE QUI RESTE PARTIELLEMENT ANALYSÉ — la liste, sans rien cacher

C'est la question qu'il a posée, et elle mérite une réponse entière.

| | état |
|---|---|
| les **30 champs du descripteur** | traités : `+0x00`, `+0x08`, `+0x10`, `+0x14..+0x24`, `+0x48`. **Clonés sans être compris** : `+0x28..+0x40`, `+0x50`/`+0x58`/`+0x60` (trois blocs `.data`, rôle non identifié), `+0xC8..+0xE8` (propriétés de rendu, aire) |
| la **musique** (`+0x68`, `+0x70..+0xB0`) | clonée du modèle : un décor de VF5 R joue la musique de **Final Showdown**, alors que les pistes `vf5r_*` sont dans le jeu |
| les **sept autres tables d'effet** | localisées (`BREATH` 0x1806430C0, `FOG_ANIM` 0x180643130, `SNOW` 0x180643340, `SPLASH` 0x180351B18, `THUNDER` 0x180351BB8, `MOVE` 0x180350820, `DOWN` 0x18034FF20) mais **non déplacées** : les effets correspondants sont retirés |
| `tex_db` | de **4 à 127 identifiants** de texture de 2008 sont inconnus de `tex_db` selon le décor. `d5r` en a 50 et il marche, donc **ce n'est pas fatal** — mais ce n'est pas expliqué, et une collision de nom n'a **pas** été mesurée |
| l'**aperçu** de la case (`0x180174BF0`) | 26 entrées seulement ; efface les trois couches AET pour nos indices |
| le **son d'ambiance** | liste d'association `0x180408850` à valeur par défaut : tous nos décors ont l'ambiance de `are` |
| les **compteurs de parties** | bornés à 41, les décors ajoutés n'en ont pas |
| `du1`..`du4` | pas ajoutés (VF5 R range leur scène sous `STGDUR`) |

### La leçon

Trois séances à traiter un symptôme à la fois. La question qui trouve, c'est :
**qu'est-ce que ce décor DEMANDE, et l'avons-nous ?** Pour les tâches d'effet,
la réponse n'était pas « la table n'a pas d'entrée, donc rien ne se passe » —
c'était « la tâche est créée quand même ». Une liste d'association pardonne ;
une tâche vivante sans données, non.

## 2026-09-10 (55) — aurora se charge : les barrières, et les personnages animés

Frédéric : « aurora se lance, il manque les barrières du ring comme pour le
décor d'Akira avant que tu ne le corriges, il manque les personnages en 3D
animés dans le décor ». Deux causes distinctes, toutes deux mesurées.

### 1. Un bloc de mur qu'on ne sait pas servir se met à ZÉRO, il ne se tronque pas

C'était ma faute, et elle est instructive. Les objets cassables (`+0x30`) et
leurs uid (`+0x38`) d'`aur` demandaient `EFF_SAKU_BROKEN`, que 2008 n'a pas.
J'avais **tronqué** le bloc en y posant un terminateur `-1`.

Or `FUN_1800848C0` **ne compte pas** les enregistrements de `+0x30` :

```c
if (param_6 != 0) {
    iVar8 = *(param_1 + 0x210);            // le nombre de MORCEAUX, lu dans +0x08
    if (4 < iVar8) iVar8 = 4;
    for (...)  puVar19[-1] = *(int *)(lVar13 + 4);   // l'uid, sans terminateur
```

Il en lit `min(morceaux, 4)` — quatre pour `aur` — et lit le champ `+4` de
chacun, **terminateur compris**, puis déborde sur ce qui suit dans `.decors`.
Le terminateur ne l'arrête pas : **la seule garde est `param_6 != 0`**.

Les deux pointeurs partent donc à zéro, et le décor perd ses objets cassables
au lieu de faire lire n'importe quoi. Quatre décors sont dans ce cas : `ui5`,
`hi5`, `ar5`, `tn5` — les quatre à objets cassables.

### 2. Les personnages animés : 2008 en a que Final Showdown n'a plus

La liste d'animations d'effet d'`aur` (table `0x18034FD20`) est `[JYOUKI,
RORA]` — de la vapeur et un rouleau. L'archive de 2008, elle, porte AUSSI :

    STGAR5_EFF_ARUKI    STGAR5_EFF_ARUKI_B    STGAR5_EFF_ARUKI_C
    STGAR5_EFF_KANKYAKU STGAR5_EFF_TOIKI

`aruki` = la marche, `kankyaku` = les spectateurs. **Final Showdown les a
coupées**, donc la liste du modèle ne les demande pas — et le décor de 2008
restait désert.

`animations_en_plus()` ajoute donc à la liste toutes les animations de la
catégorie posée que le modèle ne demandait pas, **sauf** celles qu'un autre
mécanisme joue (`KABE_REACT`, `SAKU*`, `BROKEN*` → le mur ; `DOWNKEMU` →
`EFFECT_DOWN` ; `DASH` → `EFFECT_MOVE`). Onze décors en profitent :

    ar5  ARUKI ARUKI_B ARUKI_C KANKYAKU TOIKI     bn5  KANKYAKU KANKYAKU4 …
    hi5  HATA KAMINARI1..4 SKY_DOME_H/L/M …       br5  KABE_KOWARE PERA WALK_DB

**C'est une PRÉMISSE, pas une mesure** : rien ne prouve que ces animations
soient faites pour tourner en boucle. Elle est écrite dans le code pour pouvoir
être attaquée — si l'une se voit de travers, elle se retire de la liste.
`EFFETS_UIDS_MAX` passe de 12 à 40 pour les loger.

### Aurora, dans le binaire

    mur 56        : morceaux, uid, paires ; +0x30 et +0x38 a ZERO
    animations 56 : [JYOUKI, RORA, ARUKI, ARUKI_B, ARUKI_C, KANKYAKU, TOIKI]

---

## (56) 2026-09-10 — les sept tables d'effet, et la mine sous DOWN/MOVE

Demande : « finir d'analyser les sept autres tables d'effet (BREATH, FOG_ANIM,
SNOW, SPLASH, THUNDER, MOVE, DOWN) et les sons d'ambiance pour les rétablir dans
les décors ». **Fait** — voir `analysis/decors.md` §19, qui fait foi.

Le journal de `plantage_5r.cmd` a d'abord donné la cause du dernier plantage
d'aurora en une ligne : `rbp = 0x7FF8892E0000` **est** le delta de rebasage,
donc un champ nul portant encore une relocation. C'est le `+0x30`/`+0x38` du mur
qu'on met à zéro. Garde-fou général posé (§19.6) : huit relocations retirées, sur
`ui5`, `hi5`, `ar5` et `tn5`.

Puis les sept tables. Trois formes (§19.1) :

  * `DOWN` et `MOVE` sont des **tableaux denses sans borne ni terminateur**, et
    ces deux tâches sont **toujours créées** : les dix-neuf décors ajoutés y
    lisaient du texte de `.rdata` pris pour un uid, depuis le début. Étendus à
    61 entrées, uid traduits (§19.2) ;
  * `SNOW` est une liste à terminateur : elle déménage ;
  * `BREATH`, `FOG_ANIM`, `SPLASH` et `THUNDER` ont leur **chaîne de comparaisons
    déroulée** remplacée sur place par un balayage — le nombre d'entrées quitte
    le code pour les données (§19.3).

`EFFETS_SERVIS` : `(2,)` → `(2, 5, 9, 14, 16, 19)`. Et `KAMINARI`, `SKY_DOME`,
`TOIKI` sortent de la liste auth_3d : elles appartiennent à `THUNDER` et
`BREATH`, elles y auraient tourné en boucle (§19.5).

Le contrôle lit maintenant `EFFETS_SERVIS` **chez le patcheur** et vérifie que
chaque tâche demandée a son dossier (§19.7). `RIEN A REDIRE` sur les dix-neuf.

**À voir à l'écran** : `tools\decors_5r.cmd`. Aurora ne devrait plus tomber ;
`hi5` (Haiku) devrait avoir ses éclairs, `yk5` (Yuki) sa neige et son souffle,
`bn5`/`rv5`/`sk5` leurs éclaboussures, et les dix-neuf la poussière de chute.

---

## (57) 2026-09-10 — les sept tâches d'effet qui restaient, analysées

Demande : « analyse aussi les sept autres tâches pendant que je teste
`decors_5r.cmd` ». Rien touché au binaire — lecture sur `.origine` et sur la
copie Ghidra. Résultat complet dans `analysis/decors.md` §20, qui fait foi.

La prémisse de départ était fausse : `FUN_180076B00`, que ce journal donnait
comme un obstacle (« LEAF, RIPPLE, WATER_RING et SNOW_RING partagent ce
setStage »), est un **simple setter**. C'est la mise à jour qui lit la table.
Les vtables se lisent d'un coup : `py -3 tools/rtti.py --grep TaskEffect`.

Verdict par tâche :

  * `WET_CLOTH` (17) : **aucune table** — un scalaire choisi par `index == 19`,
    et aucun des quatre décors concernés n'est le 19. Se rouvre telle quelle.
  * `ELE_BOARD` (22) : **bouchonnée** (init = `return 1;`). `are` ne l'a pas non
    plus. Rien à restaurer.
  * `RIPPLE` (7) : chaîne déroulée ×2, clone pur. Un balayage suffit.
  * `LEAF` (3) et `SNOW_RING` (15) : chaîne déroulée, et elles nomment des
    objets `(objset << 16) | rang` — la convention du mur. `tr5` et `yk5` ont
    les rangs dans leur archive de 2008 ; **`jn5` ne les a pas**.
  * `RINGOUT_SPLASH` (12) : quatrième forme de borne du chantier — une
    **adresse de fin littérale** (`while (p < 0x180350C90)`). Deux uid
    (`SPLASH_DOBON` / `_S`, présents en 2008 pour les trois décors) et un
    **pointeur** de chaîne à reloger.
  * `WATER_RING` (13) : pas de table du tout, un **littéral** `0x27006E`
    (l'objet 39:110 = `stgslk_water_ring`) dans le code. Le seul des sept qui
    demande une greffe plutôt qu'un balayage.

Piège déjà connu qui reviendra : `SPLASH_DOBON` est aujourd'hui dans la liste
`auth_3d` de `jn5` et `sn5` via `animations_en_plus()`. Le jour où
`RINGOUT_SPLASH` sera servie, elle devra rejoindre `EFFETS_AUTRES_MECANISMES` —
exactement comme `KAMINARI` et `TOIKI` (§19.5).

Rien n'a été implémenté : on attend le verdict du test en cours avant de
rebâtir.

**Leçon de forme, la troisième fois qu'elle coûte :** ne jamais passer un texte
à `py -3 -c` depuis une chaîne bash entre guillemets doubles — les accents
graves y sont des substitutions de commande, et le texte arrive vidé de tous ses
`...`. Écrire le script avec l'outil Write, puis le lancer.

---

## (58) 2026-09-10 — aurora validé ; la règle qui devinait devient un registre

Frédéric : « aurora ne plante plus, les personnages en 3D du decors sont bien
presents, et la barriere du ring aussi, ce decor est validé. » **`ar5` est
validé à l'écran.**

Puis : « ne fait jamais de supposition, il y a des eclairs dans le decor de Goh
en version R qui n'ont rien à y faire » — `hi5`, Broken House / Abandoned Dojo.

La faute était dans `animations_en_plus()`, et je l'avais moi-même étiquetée
« PRÉMISSE, pas une mesure » : ce qui ne l'excuse pas, ce qui l'aggrave. La
liste `auth_3d` d'un décor est la liste de ce qui tourne **en boucle** ; y
verser une animation de 2008, c'est **décider** qu'elle en est une. Sur `hi5`,
`LIHGT` et `SKY_HIKARI1` sont des coups d'**une seconde** — la durée exacte de
`KAMINARI1` — et ils clignotaient sans arrêt.

Un meilleur critère aurait été la même faute mieux habillée. La durée déclarée
dans le `.a3da` (`play_control.size / fps`) semblait discriminer :

    ar5  ARUKI 65 s   ARUKI_B 117 s   ARUKI_C 99 s   KANKYAKU 4 s
    hi5  LIHGT 1,0 s  SKY_HIKARI1 1,0 s  HATA 1,0 s  (KAMINARI1 1,0 s)

mais `DENKI_B` fait 2,7 s et Final Showdown le joue bien en boucle : **ça ne
prouve rien.**

La règle est donc supprimée. Par défaut un décor ajouté joue exactement ce que
son modèle demande. `ANIMATIONS_VALIDEES` est un **registre** : une animation
de 2008 ne s'y ouvre qu'après avoir été vue, et son entrée porte la date et la
phrase de validation. Seul `ar5` y figure (les quatre marcheurs et spectateurs).
Le patcheur **nomme** celles qu'il ne joue pas, décor par décor, pour qu'elles
ne se reperdent pas :

    bn5 3   nc5 3   jn5 2   sn5 3   ui5 1   hi5 3   sk5 2   br5 3   tn5 1

`hi5` a maintenant exactement la liste de `hai` : `DENKI_B`, `KUMO`. Contrôle
avant vol vert sur les dix-neuf.

---

## (59) 2026-09-10 — audit « a-t-on touché aux décors de FS ? », et le tonnerre de `hi5`

Frédéric : « on ne touche pas aux decors de FS, je t'interdis d'y modifier
quoique ce soit. L'as tu fait jusqu'a present ? » — question posée après que
j'ai écrit, ambigument, « je retire l'éclairage de nos deux fichiers pour qu'ils
correspondent à FS ». Je parlais de `STGHI5_*`. L'ambiguïté seule suffisait.

**L'audit, mesuré et non affirmé** (comparaison de la DLL patchée à `.origine`,
table par table). Les treize tables indexées par le décor, **à leur adresse
d'origine** : identiques octet pour octet. Une seule exception :

    entree 22 (du2) : +0x48 +0x49 +0x4A     = --du2-collision

soit trois octets, le correctif qu'il avait demandé et validé à l'écran. Il a
confirmé : « la modification du decor de dural est OK ».

Ce qui change quand même, et qu'il fallait nommer :

  * **deux mots dans NOTRE copie** (`.decors`) : les dossiers `TaskEffectThunder`
    de 13 et 24 portent leur indice dans le mot de bourrage `+0x1C`, parce que
    le balayage a besoin d'un champ là où le code d'origine avait des littéraux.
    L'original à `0x180351B98` est intact ;
  * **quatre préambules du moteur** réécrits (BREATH, FOG_ANIM, SPLASH,
    THUNDER) — code partagé, équivalent par construction ;
  * les deux **bases partagées**, ajouts seulement : `auth_3d_db` 0 disparu /
    0 modifié / 194 ajoutés ; `obj_db` 0 / 0 / 19. Le `.par` de l'atelier porte
    nos octets d'`obj_db` ; il n'est plus un lien dur, le dump est intact ;
  * `--decor-repli 42`.

Aucun `.farc` de FS modifié, aucun nom masqué dans le `.par`.

**Le tonnerre.** « dans sa version FS, il y a des eclairs et c'est normal, n'y
touche pas. Par contre dans sa version R, on voit des effets de l'eclair, avec
des changements tres rapides de l'eclairage, et ca n'a rien a faire dans ce
variant. »

Cause mesurée : les `SKY_DOME_H/M/L` n'animent pas des objets, ils animent la
**lumière de scène** et le **`camera_auxiliary`** (exposition, saturation de
l'image entière). Et les deux générations n'en font pas la même chose :

    animation      FS light/cam_aux   VF5 R light/cam_aux
    SKY_DOME_H     86 / 48            86 / 48
    SKY_DOME_M      0 / 0            102 / 28
    SKY_DOME_L      0 / 0             90 / 18

Final Showdown a **vidé** l'éclairage de `_M` et `_L` ; VF5 R le garde sur les
trois. D'où le clignotement, quel que soit le niveau de qualité choisi.

Correctif : nouveau registre **`EFFETS_RETIRES`**, le pendant d'
`ANIMATIONS_VALIDEES` — ce qu'un variant ne doit PAS avoir, sur constat à
l'écran. `hi5` ne demande plus `EFFECT_THUNDER`, et son dossier n'est plus posé
dans la table (qui revient à 13, 24, terminateur). `hai` n'est pas touché.

Le contrôle lit `EFFETS_RETIRES` **chez le patcheur** — il avait crié une fausse
faute le temps d'une commande, faute d'être au courant. Troisième rappel de la
même leçon.

---

## (60) 2026-09-10 — l'eau du ring d'Eileen

Frédéric : « occupe toi de WATER_RING pour le decor de Eileen ». Eileen, c'est
`MON` dans `game_score.txt` → `STGSLK`, indice 15, dont notre variant est `sk5`
(53). Son modèle demande quatre tâches ; il n'en recevait que deux.

`TaskEffectWaterRing` n'a **aucune table indexée par le décor** — c'est le seul
cas du jeu. Son créneau 4 nomme son objet par un **littéral** :

    0x180085630  mov ecx, 0x27006E        = (39 << 16) | 110 = STGSLK_WATER_RING

Le moteur est câblé sur le décor de Final Showdown ; `sk5` est l'objset 6161,
donc rien ne s'affichait.

**Le remède.** `rcx` porte encore la tâche en `0x180085630` (rien ne l'a touché
depuis l'entrée) et `setStage` a rangé l'indice du décor en `+0x58`. Les cinq
octets du `mov ecx, imm32` deviennent donc un `call` vers un stub de 38 octets
posé dans `.greffe` (`0x180EA2EA0`, la seule section exécutable qui soit à
nous), qui balaie une table `{indice, objet}` :

    decor 53 -> objet 6161:110
    terminateur

et rend **le littéral d'origine** quand l'indice n'y est pas. `slk` retombe donc
sur `mov ecx, 0x27006E` : le décor du jeu ne change pas d'un octet, et l'audit
le confirme.

Trois mesures avant de poser la substitution, aucune supposition : le modèle
demande-t-il vraiment la tâche, son objset est-il bien celui du littéral, et le
rang 110 existe-t-il dans l'archive de 2008 (`STGSK5_WATER_RING`, oui, au même
rang). Sinon le patcheur le dit et ne pose rien.

`EFFETS_SERVIS` gagne 13. Les zones `EAU` et `EAU_TABLE` entrent dans
`_disposition()`, donc sous la garde de `verifier_disposition()`.

Le contrôle suit l'appel depuis `0x180085631`, puis le `lea` du stub, et lit sa
table : il vérifie que l'objet posé est bien `<notre objset>:110`. Il ne recopie
aucune adresse — il les déduit du binaire patché.

**Reste sur `sk5`** : `RIPPLE` (les rides à la surface), qui est un balayage
identique aux quatre d'hier — table `0x1806432E0`, 2 dossiers de `0x2C`, aucun
uid, clone pur.

---

## (61) 2026-09-11 — RIPPLE, les marcheurs d'Aoi, et le brouillard de premier plan

**RIPPLE (7).** Même forme que les quatre chaînes d'hier, à un détail près : elle
n'est pas dans `setStage` (un simple setter) mais dans `FUN_18007AE10`, appelée
depuis l'init. 46 octets de chaîne déroulée, index dans `edx`, résultat dans
`rcx`, et un `mov r15d, edx` pris dans la zone qu'il faut remettre en tête. Deux
dossiers de plus : `bn5` et `sk5`. `EFFETS_SERVIS` gagne 7.

**Les personnages 3D d'Aoi — un vrai défaut, et il n'était pas où je le
cherchais.** `decor_neuf.py` ne déclarait dans `auth_3d_db` que **ce que le
modèle de Final Showdown déclarait** :

    EFFSTGJIN (FS)   7 animations
    EFFSTGJN5.farc   10 fichiers      -> 5 declares, 5 invisibles

`EFF_ARUKI_A`, `_B`, `_C`, `EFF_TALK` et `EFF_IKE` étaient dans l'archive posée
et **n'entraient jamais dans la base** : aucun mécanisme ne pouvait les
atteindre, et `animations_en_plus()` ne les voyait même pas. Une base doit
décrire ce qui est **posé**, pas la liste du modèle. Corrigé : tout membre
`.a3da` de l'archive est déclaré. Déclarer n'est pas jouer — c'est
`ANIMATIONS_VALIDEES` qui décide.

Le champ `size` d'un uid n'est pas la taille du fichier : c'est **exactement le
`play_control.size` du `.a3da`** — mesuré sur les douze uid d'`EFFSTGAR5`
(ARUKI 3901, ARUKI_B 7021, KANKYAKU 241, TOIKI 30). On le lit, on ne l'invente
pas. Onze décors gagnent des déclarations (`hi5` +26, `tn5` +10, `jn5` +5…).

**Le brouillard de premier plan.** C'est le **groupe 1** du fichier
`rom/light_param/fog_<code>.txt` — la bande de tout proche.

    FS   jin : density 0.00000   linear -2.50  1.00      SEGA l'a ETEINT
    2008 jn5 : density 1.00000   linear -2.50  1.00      allume
    FS   slk : density 1.00000   linear -0.14 -0.03      SEGA l'a GARDE
    2008 sk5 : density 1.00000   linear -0.14 -0.03      identique

Ce qui est établi par décompilation, et qui écarte trois pistes :

  * le parseur (`FUN_1800D72A0`) stocke le groupe N via
    `FUN_180088160(n) = &DAT_1806F86D0 + n*0x24`, **sans aucune borne** —
    le groupe 1 est donc bien lu ;
  * **aucun champ du descripteur** ne sépare les quatre décors à groupe 1
    actif (`slk`, `du2`, `du3`, `du5`) des 37 autres — rien ne le conditionne ;
  * le mécanisme n'est pas bouchonné : quatre décors du jeu s'en servent.

Reste **une** inconnue : le moteur ouvre-t-il nos `fog_<code>.txt` ? Ils sont
posés en fichiers LIBRES et leur nom n'est pas dans le `.par` — et tous les
chargeurs ne retombent pas sur le disque (`obj_db.bin` ne le faisait pas, cf.
(42)). La chaîne statique s'arrête sur un appel indirect : `FUN_1800D7150`
(bâtisseur des six chemins) n'a qu'un appelant direct, l'amorçage
`FUN_1800D6130`, qui lui passe `codes[0]`. Le chemin par décor passe par une
enveloppe (`0x1800D7140`) atteinte **par vtable**.

**Le témoin est gratuit** : `slk` et `sk5` ont un groupe 1 **identique**. Si la
version R d'Eileen montre la même brume rasante que la version FS, les fichiers
sont lus et la cause d'Aoi est ailleurs. Sinon, elle est là. À regarder en même
temps que l'anneau d'eau.

Sinon, `tools\tracer_eclairage.cmd` met un point d'arrêt sur `CreateFileW` et
journalise tout chemin contenant `light_param` : c'est la réponse directe.

---

## (62) 2026-09-11 — le binaire de VF5 R est lisible, et il tranche

`extracted/LIND_R/vf5r.bin` (2,4 Go, image Lindbergh) porte **les tables du
moteur de VF5 R**. Elles se retrouvent par leurs valeurs, sans symboles :
chercher le motif flottant d'un enregistrement connu de Final Showdown suffit.
C'est un outil de comparaison qu'on n'avait pas utilisé jusqu'ici.

**Ce qu'il donne pour le décor d'Eileen (`slk` 15 / `sk5` 53) :**

    RIPPLE   R 0x4915C6CC  idx=15  0.4 0.8 | 0.10 0.1905 0.505 1.0 | id 9207
             FS 0x18064330C idx=15  0.4 0.8 | 0.10 0.1905 0.505 1.0 | id 9207
    SPLASH   R 0x4915C798  idx=15  id 8712 | 0.20 0.15 0.11 | 100 100 100
             FS 0x1806434C8 idx=15  id 8712 | 0.20 0.15 0.11 | 100 100 100
    TACHES   R 0x48FEF4A0  [2, 12, 7, 13] = WALL WATER_RING RIPPLE SPLASH
             FS            [2, 13, 7, 14] = les MEMES

**Octet pour octet, les deux générations sont identiques sur ce décor.** Notre
entrée 53 est un clone exact : RIPPLE `0.10 0.19 0.51` (bleu), SPLASH
`0.20 0.15 0.11` (sable). Il n'y a donc pas de « bonne couleur » à retrouver
dans le code de R : **le bleu de RIPPLE est celui de VF5 R**.

La seule variable qui reste est l'ARTWORK derrière l'identifiant de particule
9207 — un asset global de l'ensemble d'effets, que l'import n'a jamais touché
(on ne porte que les archives de décor). Et `tex_db` montre que Final Showdown
a AJOUTE le sable sur ce décor : toutes les textures `SAND` y portent le
préfixe `F_VF5S_`, tandis que les grains d'eau portent `F_VF5E_`
(`SLK00_IK_MIZU_TUBU01..04`, tubu = grain, mizu = eau). Le binaire de R ne
nomme **aucune** texture `SAND` pour ce décor.

**La numérotation des tâches d'effet diffère entre les deux moteurs**, et c'est
une trouvaille réutilisable : R en a **19**, Final Showdown **23**. FS a inséré
`EFFECT_MOVE` en 11 (d'où le décalage de 1 au-delà), puis ajouté `PARTICLE`,
`POISON` et `ELE_BOARD` à la fin. C'est cohérent avec `EFF_DASH`, absent de
toutes les archives de 2008 : la tâche MOVE n'existait pas.

    R  : 0 HIT 1 AUTH3D 2 WALL 3 LEAF 4 WATA 5 SNOW 6 YUKA 7 RIPPLE 8 RAIN
         9 THUNDER 10 DOWN 11 RINGOUT_SPLASH 12 WATER_RING 13 SPLASH
         14 SNOW_RING 15 FOG_ANIM 16 WET_CLOTH 17 FOG_RING 18 BREATH

**Aoi n'est PAS validé** : seules ses animations le sont (« personnages en 3D
dans le decor OK »), le brouillard de premier plan manque toujours. Le registre
le dit désormais explicitement.

---

## (63) 2026-09-11 — les décors du VF5 d'origine (ver.B), ajoutés, Dural compris

**Lanceur : `tools\decors_vf5.cmd`** (retrait : `decors_vf5_retirer.cmd`). La
barre espace fait tourner chaque case sur ses TROIS générations : Final
Showdown → VF5 R → VIRTUA FIGHTER 5. **Posé, patché, contrôlé — pas vu à
l'écran.**

    21 entrées neuves, indices 61..81, objsets 6169..6190, codes <1re><3e>b
    dob bnb trb ncb csb rvb jnb snb uib hib aeb skb ykb tkb arb brb tnb
    drb d2b d3b d4b      <- les QUATRE Dural de ver.B

    controle_decors_5r.py   RIEN A REDIRE -- les 19 decors
    controle_decors_vf5.py  RIEN A REDIRE -- les 21 entrees de ver.B

Table du lot : `tools/variantes_vf5.py`. Et **tout ce qui vient de ver.B y est
LU dans son ELF** (`extracted/LIND_VF5/id/disk0/vf5`, x86-32, déjà extrait) :
aucune valeur n'est recopiée à la main.

### Ce qui n'était pas comme VF5 R — trois découvertes, toutes mesurées

**1. Les identifiants de TEXTURE de ver.B ne sont pas ceux de FS.** VF5 R
numérote comme FS (sur les dix-neuf objsets posés, chaque identifiant connu de
la `tex_db` de FS désigne une texture du même décor). ver.B, non : **3 277
identifiants sur 3 975** désignent autre chose chez FS —
`F_VF5E_DJO00_IK_DOWNKEM_000` porte le numéro de `F_VF5E_BAR00_HR_PERA_102`,
`stgdur` celui des lunettes de Wolf. Posés tels quels, deux textures pour un
numéro. `variantes_vf5.ecrire_objset` **renumérote** dans NOTRE archive : un
nom que FS connaît prend le numéro de FS, les 1 381 autres un numéro libre (trous
de la `tex_db` de FS, hors de ceux de VF5 R). Les identifiants sont en deux
endroits et deux seulement — la liste de l'en-tête (`+0x1C`/`+0x20`) et les huit
emplacements de chaque matériau (`+0x14 + t*0x78 + 4`) : vérifié, **aucun**
emplacement non vide ne sort de la liste. Seul `_obj.bin` est recomprimé ; le
`_tex.bin` est recopié octet pour octet.

**2. Les RANGS d'objets de ver.B ne sont pas ceux de FS** (`STGDJO_GND` : 114 chez
FS, 0 chez ver.B). Les cinq objets viennent du **descripteur de ver.B**, relu
dans l'ELF (table en `0x852F220`, 28 × 0x70) :

    ver.B  +0x08 objset  +0x0C 2e objset  +0x10 GND  +0x14 SKY  +0x18 SDW
           +0x20 REFLECT +0x24 REFRACT (jin)  +0x28..0x30 reflets d'objectif
    FS     +0x10 objset  +0x14 GND  +0x18 RING  +0x1C SKY  +0x20 SDW
           +0x24 REFLECT +0x2C..0x34 reflets d'objectif (TEXTURES, pas des uid)

ver.B n'a pas d'objet RING (le sol le porte) : `-1`, valeur que FS écrit lui-même.

**3. Chaque génération a SES tables d'effets.** ver.B a la même table que
`0x18034D570` (en `0x85FF520`), sa table de murs (`0x8600480`, 14 × 0x14) et sa
liste d'animations (`0x86001E0`). On les prend TELLES QUELLES :

  * **les tâches** : celles de ver.B, traduites par NOM (19 tâches, pas de MOVE,
    comme R), et seulement celles qu'on sait servir ;
  * **les murs** : ceux de ver.B, convertis au format FS — un morceau fait 0x28
    chez ver.B, 0x2C chez FS (FS a inséré un ENTIER à +4 : 0 sur 293 morceaux,
    1 sur 15 ; on met 0). 12 décors ont leurs barrières, dont les **24 grillages
    cassables de Goh** ;
  * **les animations** : celles de ver.B (les marcheurs d'Aoi, les spectateurs
    de Lau, le feu de Goh…). Plus besoin de registre ici : le binaire dit ce qui
    était joué.

**Et la table de VF5 R, relue de la même façon dans `vf5r.bin`, donne `hai` =
WALL seul — sans THUNDER.** C'est exactement ce que Frédéric a vu sur hi5 et
qu'on avait retiré à la main (`EFFETS_RETIRES`). Le binaire le confirme.

### Dural : QUATRE variantes, et elles répondent à « il en manque trois »

ver.B a quatre descripteurs de Dural sur UNE géométrie (`stgdur`, 35,7 Mo) :
son `+0x0C` nomme un second objset — le CIEL (`stgdu1`..`stgdu4`, qui ne sont pas
des décors). FS a le même mécanisme, complet et jamais servi : la liste
`+0x00` de `0x18034D570` — demandée par `0x18006F620`, attendue par la porte de
l'état 4 (`0x18006F380`, état 1), rendue par `0x18006FA70`. Décompilé, pas
supposé. Les quatre planches (`analysis/ciel_verb_du1..4.png`) :

    du1  un COUCHER DE SOLEIL panoramique      -> drb
    du2  un ciel de JOUR, nuages + reflet       -> d2b
    du3  un ciel d'ORAGE, gris-vert             -> d3b
    du4  une NUIT ETOILEE, voie lactee          -> d4b

Frédéric avait noté qu'il manquait NIGHT, DAY et SUNSET. Libellés provisoires
« VIRTUA FIGHTER 5 - 1..4 » : le nom est à lui.

La case de Dural passe à **neuf** variantes : la greffe les découpe par
décalage et masque, donc 16 par anneau (puissance de deux), greffe à 0x4000.
**Seulement dans le build ver.B** : `decors_5r.cmd` garde sa greffe de 0x3000 à
l'octet près (la ligne de commande est lue à l'import).

### Deux corrections en passant

* un décor ajouté **sans mur** perdait AUSSI son entrée d'animations d'effet
  (un `continue` trop tôt) : `rv5` et `so5` n'avaient pas les leurs, que `riv`
  et `smo` ont. Corrigé pour les deux lots ;
* `controle_decors_vf5.py` lit la liste `+0x00` comme le moteur, jusqu'au
  premier `-1` : les entrées de FS portent `-1, 0, 0…`.

### Ce qui reste

* **voir** : `decors_vf5.cmd` ;
* les tâches que ver.B avait et qu'on ne sert pas (pas de dossier chez le
  modèle FS) : YUKA (ban), RAIN/RIPPLE/SPLASH (nyc), SNOW_RING (yuk),
  FOG_RING, WET_CLOTH, RINGOUT_SPLASH — le contrôle les nomme décor par décor ;
* les champs inconnus du descripteur (`+0x3C` de FS…) viennent du modèle FS ;
* la même lecture de la table de VF5 R dit que `bn5` et `rv5` ont RIPPLE/SPLASH
  que R n'avait pas — **pas touché**, à trancher.

---

## (64) 2026-09-11 — les tables de VF5 R relues dans SON exécutable : le lot 5R vient de FS

Question de Frédéric : « les effets, les murs et les animations de VF5R ne
proviennent pas de FS ? ». **Si, ils en viennent**, et c'est maintenant mesuré.
Pour le lot VF5 R, les listes de tâches, les entrées de mur et les listes
d'animations sont des CLONES DU MODÈLE FS (uid traduits vers nos catégories) ;
de R ne viennent que la géométrie, les textures, la collision, l'éclairage et
les fichiers `.a3da`. Pour ver.B, les trois listes sont les siennes (63).

`tools/tables_generation.py r|verb` : l'exécutable de R est extrait
(`extracted/LIND_R/id/disk0/vf5`, avec `obj_db`/`tex_db`/`auth_3d_db` dans
`extracted/decors/VF5R/_db`), et ses tables sont RETROUVÉES par valeur, sans
adresse en dur — la même découverte rend exactement les adresses de ver.B déjà
connues (contre-épreuve). R : descripteurs `0x87738A0` (pas 0x8C), tâches
`0x8833EE0`, animations `0x88351C0`, murs `0x8835460` (pas 0x20, morceau 0x28
comme ver.B : c'est FS qui a inséré l'entier).

**VF5 R contre ce que la DLL applique (entrées 42-60)** :

    taches   manquent  bn5 YUKA  tr5 LEAF  rv5 WET_CLOTH RINGOUT_SPLASH
                       jn5 FOG_RING  sn5 WET_CLOTH RINGOUT_SPLASH
                       br5 RAIN WET_CLOTH SPLASH  tn5 THUNDER
             en trop   bn5 RIPPLE SPLASH  rv5 SPLASH  hi5 FOG_ANIM
    anims    manquent  bn5 KANKYAKU KANKYAKU4 (spectateurs)
                       hi5 HATA FIRE KUSA DORA
             en trop   ar5 RORA  br5 KANKYAKU WALK_A WALK_B WALK_AB WALK_C
                       tn5 SKY_DOME_M
    murs     17 identiques a R (objets ET positions), so5/rv5 sans mur des deux cotes
             nc5 : 2 des 4 panneaux designent FENCE_B / FENCE_C de FS
                   (rangs 393/394) -- ABSENTS de l'archive de R. R a 4 FENCE.

**ver.B contre ce que la DLL applique (entrées 61-81)** : murs et animations
identiques ; seules manquent les tâches qu'on ne sait pas servir (YUKA, LEAF,
RIPPLE/RAIN/SPLASH de nyc, RINGOUT_SPLASH, WET_CLOTH, FOG_RING, SNOW_RING).

Pour les DEUX lots, les DOSSIERS des tâches servies (paramètres de neige, de
souffle, de tonnerre, d'ondes, d'éclaboussures, de brume animée, l'anneau
d'eau) sont ceux du modèle FS — seul celui de `slk` a été comparé à R (identique,
(62)).

Rien n'est corrigé : `ar5` et `hi5` sont validés à l'écran, et deux « en trop »
sont chez eux (RORA, FOG_ANIM). À trancher par Frédéric.

## (65) 2026-09-11 — chaque génération a SES effets : listes, murs, dossiers, et les sept tâches qui manquaient

Frédéric : « applique à VF5 R ses propres listes, rien ne doit venir de FS,
applique les effets VF5 à VF5, décompile les effets dont on ne sait pas se
servir si c'est nécessaire ».

**1. Tout ce qu'une entrée spéciale (R 42-60, ver.B 61-81) contient vient de
son binaire**, lu par `tools/generation.py` (source unique) et traduit par
`patch_moteur.Traducteur` : uid par NOM (`STGRIV_` → `STGRV5_`, catégorie posée
`EFFSTG<eff>`), textures (R : même numéro ; ver.B : par nom), objets
`(objset << 16) | rang` (l'objset de la génération devient le nôtre ; le rang doit
exister dans l'archive posée). Liste des tâches, entrée de mur (morceaux, uid,
paires, grillage, cassables), animations, descripteur, poussière de chute, et
les DOSSIERS de SNOW / BREATH / SPLASH / RIPPLE / FOG_ANIM / THUNDER /
WATER_RING. Conséquences visibles : `hi5` perd THUNDER et FOG_ANIM et gagne HATA
FIRE KUSA DORA ; `bn5` retrouve ses spectateurs ; `nc5` a les quatre vrais FENCE
de R ; `ar5` perd RORA.

**2. Les sept tâches que FS ne savait pas servir à un décor ajouté** sont
décompilées (FS : `analysis/effets_fogring_data.c`,
`effets_yuka_rain_fogring.c`, `effets_yuka_ringout_fs.c`, `effets_wetcloth*.c` ;
R : `effets_ringout_r*.c` ; ver.B : `effets_ringout_verb.c` — projets Ghidra
`ghidra/vf5r_lind` et `ghidra/vf5verb_lind`, importés pour l'occasion) et
servies avec les données de LA génération :

| tâche | ce que FS lit | remède | qui |
|---|---|---|---|
| LEAF (3) | 2 `cmp` déroulés, `{indice, objet, objet}` | la chaîne devient un balayage (CHAINES) ; R/ver.B nomment leurs deux objets par des LITTÉRAUX du dessin | tr5 trb |
| YUKA (6) | CINQ littéraux câblés sur `ban` : objset `0x18`, table `0x180356620` (144 dalles × 3 couches), uid `0x496`, objet `0x180000` ; le setStage ignore l'indice | le créneau 7 choisit notre config ou celle de FS et l'écrit dans une variable de la greffe ; les cinq sites la relisent | bn5 bnb |
| RAIN (8) | UN bloc `0x180643280` recopié par l'init ; setStage = `ret 0` | le créneau 7 recopie le bloc du décor (sinon celui de FS, relu dans `.origine`) avant l'init | br5 ncb |
| RINGOUT_SPLASH (12) | tableau `0x180350C10` borné par une adresse de FIN littérale | déménage dans `.decors`, les deux `lea` repointés, chaîne recopiée ; R/ver.B n'ont ni le décalage y ni la « poussée » de FS : 0,0 et un NaN que le stub du `call 0x18006F350` lit comme « ne pas pousser » | rv5 sn5 rvb jnb |
| SNOW_RING (15) | UN dossier `0x180643450`, lu par `0x18007D820` seule | stub avant l'appel : recopie le nôtre, sinon celui de FS | ykb |
| WET_CLOTH (17) | un scalaire : 0,4 si indice == 19, sinon 0,001 | `mov eax, 0x13` → stub qui rend l'indice s'il doit valoir 0,4 | br5 = 0,4 (règle de R) ; tous les autres 0,001 (ver.B n'a pas de règle) |
| FOG_RING (18) | UN dossier `0x1806431C8`, lu par `0x180072130` seule | stub avant l'appel, comme SNOW_RING | jn5 snb |

Ordre établi dans le code, pas supposé : l'état 3 de `0x18006F380` appelle
`vtable[7](tâche, indice)` juste après l'inscription (`0x180245830` n'appelle
aucune méthode) ; l'init tourne à la première trame — c'est pour cela que l'init
de WetCloth lit déjà l'indice.

Les deux « constructeurs statiques » (`.bss` de R et ver.B) se rejouent avec
`tools/emu32.py` (qui sait maintenant `movss`) : le du2 de R, rejoué, est
IDENTIQUE octet pour octet à celui de FS — contre-épreuve.

Greffe : GRE_GEN, derrière la table de l'anneau d'eau ; lanceur VF5 passé à
0x5000 (utilisé jusqu'à 0x4800), lanceur 5R inchangé à 0x3000 (0x2950).
Contrôles : `controle_decors_vf5.py` / `controle_decors_5r.py` relisent chaque
nouveau dossier EN SUIVANT LE CODE (appel → stub → `lea` → table) et
comparent : « RIEN À REDIRE » pour les 21 + 19 entrées, et plus aucune tâche
« que la génération avait aussi ». `verifier_lanceurs.py --sans-patch` : aucun
défaut. Rien n'a été VU à l'écran.

`EFFETS_RETIRES` et `ANIMATIONS_VALIDEES` ne servent plus aux entrées
spéciales (leurs listes viennent de la génération) ; ils restent pour un clone
de FS.

## (66) 2026-09-11 — les comportements câblés sur un numéro, les Dural de VF5 R, et une sonde qui voit

Retour de Frédéric sur la construction de 15 h 11 (le lanceur a bien tourné à
cette heure : `obj_db.bin` et `auth_3d_db.bin` datent de 15:11:56) : l'eau
d'Eileen (ver.B), les empreintes de Wolf (ver.B), les grillages invisibles de
Jean et Wolf (R), le brouillard d'Aoi et la brume de Lei-Fei (R), les flashs
de Taka-Arashi (R), les décors de Dural (R).

**1. Une sonde qui voit — `tools/sonde_decor.py <indice>`.** Elle force un
décor au seul point où le gestionnaire consomme la demande (`0x18018EF40`,
`[rcx+0x60]`), mène le jeu seul jusqu'au combat en Arcade (apm.dll de
substitution : appuis sur START, fenêtre de 20 ms — 10 ms en perdait sous
débogueur), journalise les fichiers ouverts (`--fichiers`), pose des espions
(`--bp adresse:nom[:mémoire]`) et fait des captures (`--captures`,
`--toutes`). Le scénario manuel est sauvé avant et REMIS après. Captures dans
`analysis/sonde/`. Environ deux minutes et demie par décor.

**2. FS câble des comportements sur des NUMÉROS de décor et d'uid.** Nos
entrées ne les déclenchaient jamais. Relevé exhaustif : les 18 appelants de
l'accesseur `0x18018F580`, les 137 méthodes des tâches d'effet décompilées
(`analysis/taches_effet_toutes_fs.c`), puis vérification dans le code de R
(accesseur `0x8108718`, 10 appelants) et de ver.B. Un comportement n'est
rendu à une entrée QUE si sa génération l'a (`generation.CABLAGES`, vérifié
instruction par instruction : l'immédiat comparé doit être l'indice du décor
dans CETTE génération — smo vaut 0x27 chez R, 0x28 chez FS).

| comportement | test FS | R | ver.B | rendu à |
|---|---|---|---|---|
| grillage alterné | `== 16 ‖ == 39` (0x18008474A, 0x180084D7F) | 0x84B9536 | — | yk5, gm5 |
| reflet du grillage | `== 39` + objet `0xB1F009D` | 0x84BB7FA | — | gm5 (son objet) |
| plan de coupe de S_REFL | `== 10` (0x18010B6CB) | 0x81427CB | — | sn5 |
| paramètres de bar | `== 0x13` (0x180105636) | 0x813EB6A | — | br5 |
| Auth3D : balancement riv | `== 8` → +0xB1 | 0x84B8DA4 | 0x838C88D | rv5, rvb |
| Auth3D : flashs de fin de round | `== 0x28` → +0xB0 | `== 0x27` | — | so5 |
| uid IDOU/KAWA, FLASH | 0x4E8/0x4E9, 0x7F4 | mêmes numéros | 0x364/0x365 | rv5, rvb, so5 |

Ce que FS teste et qu'AUCUNE génération ne teste n'est pas rendu : plan d'eau
riv/jin (`0x18018FBC0`), particules de yuk/hai, jin du ring-out
(`0x1800795FB`), drapeau gym (`0x1801F4272`), public/néons/voitures d'Auth3D.
La caméra par décor (`0x180053EEB`, décors 4 à 25) existe chez R avec SA
table (4 à 38) : non rendue, à faire si Frédéric le demande.

Mécanique (greffe) : aux appels de l'accesseur, un stub rend l'indice FS du
même lieu pour nos entrées ; le setStage d'Auth3D (créneau 7) est enveloppé
pour poser les drapeaux ; l'accesseur d'uid `0x180041440` est enveloppé à ses
quatre appels d'Auth3D. Vu à la sonde : **gm5 et yk5 alternent cage / ring
ouvert d'un round à l'autre** (RING OUT au round sans grillage), **les flashs
de so5 ne partent qu'au RING OUT, à la défaite et sur CONTINUE**.

**3. Les quatre Dural de VF5 R, indices 82-85** (`d15 d25 d35 d45`, objsets
6191-6194). Le « manque » de `STGDU<n>.farc` n'en est pas un : leurs
catégories de scène sont VIDES dans la base de R, comme `STGDU1` chez FS
(`variantes_5r.SANS_SCENE`, vérifié par `controler()`). Posés, contrôlés,
vus à la sonde (d15 : château sous la neige ; d45 : ciel d'orage). La case de
Dural a 13 variantes : FS 5, R 4 (« SNOW - VF5 R »…), ver.B 4. Lanceur :
`--decors-table 86 --decors-5r-dural --decor-ecretage 86`. Une collision
d'identifiant de texture (6925 : feu de hib ver.B / Dural de R) est sans
effet, les deux objsets ne se chargeant jamais ensemble.

**4. Ce qui est établi sans être corrigé.**

* **Brouillard d'Aoi (jn5)** : `fog_jn5.txt` EST lu (sonde, CreateFileW) ; la
  brume dense sur l'étang est le groupe 1 de R (hauteur -2,5 à 1,0) ;
  FOG_RING s'initialise sur notre dossier, dessine à chaque image et trouve
  sa texture (espions). Rien ne manque côté code : il faut savoir ce que
  Frédéric voit chez R.
* **Brume de Lei-Fei (sn5)** : son fichier de R n'a qu'une brume de distance
  légère (groupe 0, densité 0,1), le groupe 1 est éteint ; le plan de coupe
  de sin (§2) est désormais rendu. Même question.
* **Eau d'Eileen (skb)** : chez ver.B le ring EST l'objet `WATER_RING`
  (textures `KA_NIGORI`, eau trouble) ; le moteur FS le rend blanc laiteux —
  chez FS et R il est posé sur un vrai ring de sable/roche. Le grand plan
  `EFF_WATER` (shader `WATER01`) n'a chez ver.B ni cube d'environnement ni
  drapeau `environment` ; l'essai du seul drapeau (0x101 → 0x501) ne change
  presque rien. Rendre de l'eau demande un choix (matériau de R, cube de R) :
  à trancher par Frédéric. Au passage : **sk5 (R) est entièrement bleuté**
  (captures `d53_*`), c'est la « couleur du sable » d'Eileen signalée plus
  tôt.
* **Empreintes de Wolf (ykb)** : SNOW_RING tourne entièrement (chargement
  sur notre dossier, dessin, passe `SN_FOOT` 1 816 fois) ; la table des 16
  os (0, 10, 72, 101…) et les paramètres sont IDENTIQUES chez FS, R et
  ver.B. La neige se creuse jusqu'à la grille sous un corps, jamais sous un
  pas : c'est le rendu (shaders `snow_ring`/`snow_footprint` de FS, chargés
  depuis les données) qui diffère. Chantier à part.

## (67) 2026-09-11 — les empreintes dans la neige de Wolf : un point Direct3D fait un pixel

Frédéric : « les empreintes de pas dans la neige ne fonctionnent toujours
pas », puis « dans la version FS du stage de Wolf, il n'y a pas de neige sur
le sol du ring ». C'est la clé : **aucun décor de FS ne crée SNOW_RING**
(tâches de `yuk` chez FS : pas de SNOW_RING ; chez ver.B : WALL SPLASH
SNOW_RING WET_CLOTH BREATH ; chez R, ni `yuk` ni `slk` ne l'ont — les traces
dans le sable d'Eileen de R viennent de WATER_RING). Le code de SNOW_RING
est dans le moteur APM3, mais personne ne l'a jamais fait tourner sur PC.

**Ce qui a été écarté, par la mesure :**

* la table des 16 os (`0x180350FF0`) : lue dans `bone_data.bin` (format
  DIVA, 21 squelettes, 149 os d'objet), elle nomme `n_hara_cp`, `j_kao_wj`,
  coudes, mains, cuisses, jupes, genoux, `kl_asi_*_wj_co` (chevilles),
  `kl_toe_*_wj` — et les os d'objet sont IDENTIQUES chez ver.B et FS (celui
  de FS Lindbergh est même égal à l'octet à celui de R) ;
* la logique : sonde `--histo 0x18007E322:empreinte:Rbp+xmm6` sur ykb —
  16 928 empreintes ajoutées en un combat, surtout par les os 12-15
  (chevilles à y ≈ 0,1, orteils à y ≈ 0,0) ;
* les shaders ARB : ceux de ver.B et de FS ne diffèrent que par l'en-tête
  commun à tous (`TEMP t_normal` / `p_max_alpha`).

**La cause.** Chaque empreinte est un POINT : `glPointSize(6)` (la valeur
+0x10 du dossier, la même chez ver.B et FS), mode 2 → `D3D11_PRIMITIVE_
TOPOLOGY_POINTLIST` (`0x180245EA0`), dans une cible de 512 × 512 (sonde,
viewport posé en `0x18007E035`) qui couvre l'anneau de 12 m : 6 pixels =
14 cm, un pied. Mais le moteur APM3 est une couche OpenGL → **Direct3D 11**
(`VSSetConstantBuffers`, `IASetPrimitiveTopology`… en vtable), et en D3D11
un point fait toujours UN pixel. Les shaders ne sont pas les `.fp/.vp` ARB
mais du **DXBC précompilé** dans `w64/shader_pxd_w64.farc` ; le portage a
donné un geometry shader (conteneur `GSFX`) aux cinq programmes de points
— `fog_ptcl`, `particle.1`, `snow_particle.0/1`, `water_particle` — et PAS à
`snow_footprint..vp`, resté un `GSVS` alors que son shader de sommets sort
déjà la taille (COLOR1.x, lue en TEXCOORD6 : l'attribut 14 que pose
`0x18007E420`). Empreintes de 2,3 cm : un corps qui glisse traîne 16 os et
creuse un sillon, un pas ne laisse rien.

**Le format, lu dans le chargeur.** `0x180250DA0` : un programme de
sommets (0x447) qui commence par `GSFX` va à `0x180269490`. GSFX : 'GSFX',
0x20, 0x00050001, taille ; +0x10 u16 somme des lettres du nom puis le nom
(clé du cache, `0x180269BD0` — 0x57A = « snow_particle ») ; +0x30 trois
(décalage, taille) : GSVS, GSPS, GSGS ; +0x48 la taille, +0x4C 0. GSGS
(`0x1802716A0`) : +0x10 0x10000000, +0x18 0x80 et taille du DXBC, +0x20
vingt octets qui ne sont qu'une CLÉ de cache. Le geometry shader des flocons
étire un point de `taille` pixels avec `cb12[28].xy` = (2/L, −2/H) du
viewport COURANT — écrit par `0x18025E830` (descripteur `0x601F270C` :
emplacement 12, registre 28), appelé à chaque viewport par `0x180261840`.

**Le remède.**

* `tools/shader_empreintes.py` compile (d3dcompiler_47) le geometry shader
  des empreintes — celui des flocons à l'instruction près, avec la signature
  du shader d'empreintes en entrée ET en sortie —, l'emballe en `GSFX` (GSVS
  de FS tel quel, GSPS nul du portage tel quel, GSGS neuf) et pose
  `w64/shader_vf5_w64.farc`, qui ne contient QUE `snow_footprint..vp`.
  L'archive de FS n'est pas touchée. `--controle` relit tout.
* `patch_moteur.SHADER_EMPREINTES_SITE` : le `lea rdx, [chemin]` de
  `0x180176829` (le lecteur de shaders par nom, `0x1801767D0`) devient
  `call stub ; nop2` ; le stub rend le chemin de FS, sauf pour
  « snow_footprint..vp ». Posé seulement si une entrée reçoit SNOW_RING, et
  refusé si l'archive n'est pas conforme.
* `tools\decors_vf5.cmd` fabrique l'archive avant le patch ;
  `controle_decors_vf5.py` (point 11) relit le site, les trois `lea` du stub
  et leurs cibles, puis l'archive.

**Vu à la sonde** (`analysis/sonde/planche_d73_empreintes.png`,
`avant_apres_d73.png`, `d73_sol_apres.png`) : notre archive est ouverte
juste après celle de FS ; la neige se creuse sous chaque pied, le ring se
couvre de trous au fil du combat. C'est Frédéric qui juge si c'est l'aspect
de la borne.

Contrôles : ver.B « RIEN A REDIRE » (shader des empreintes conforme), R
« RIEN A REDIRE », `verifier_lanceurs --sans-patch` « AUCUN DÉFAUT ».
