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
