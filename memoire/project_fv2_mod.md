---
name: project-fv2-mod
description: "Mod Fighting Vipers 2 (Model 3) — le programme est compressé en CROM, l'image exploitable s'extrait d'une save state Supermodel."
metadata: 
  node_type: memory
  type: project
  originSessionId: 79a4eca3-6fc5-4e04-8400-5b9ce2442882
  modified: 2026-08-07T16:57:10.831Z
---

Projet de modding Fighting Vipers 2 (Sega Model 3, Step 2.0) sous Supermodel, démarré le 2026-08-07. Brief de référence : `C:\Users\frede\Downloads\fighting-vipers-2-mod-brief.md` (5 objectifs : débloquer Del Sol/Kuhn/BM, textes+logos HD, mode Versus, mode Training, menu de sélection). Outils dans `C:\Users\frede\Documents\SEGA Model 3\fv2mod\`.

Le fait central : **la CROM ne contient pas de code lisible, le programme y est compressé (LZSS)**. Chercher des chaînes dans les ROM déinterleavées ne donne rien — ni en CROM ni en banked_crom. L'image exploitable est la **RAM principale décompressée**. C'est elle qu'il faut charger dans Ghidra, base 0, big-endian PowerPC — pas la ROM. Deux façons de l'obtenir, voir [[reference_supermodel_memoire]] : depuis une save state, ou en live sur le process via `fv2mod\mem.py`.

Repères confirmés en RAM (adresses exactes, vérifiées sur le process en cours) : menu de test factory `0x88A5C`, placeur d'objets `0x882B4`, test caméra `0x888BA` — soit très exactement les trois adresses de TCRF. Table de noms de persos à pas de 8 octets en `0xB1758` : KUMA, DELSOL, KUHN, EMI, CHARLIE, BM, MAHLER, PICKY, HONEY, JANE, SANMAN, TOKIO, RAXEL, BAHN, GRACE — les cachés ne sont pas dans une table à part, ils sont contigus aux persos de base. `CANDY` est absent du jeu. Juste après, en `0xB17D0`, deux listes d'index : `00 01 02 03 04 05 09 0A 0B` puis `00..0B` — probablement roster restreint vs roster complet, à confirmer en runtime.

**Adresses trouvées en runtime** (RAM, confirmées par diff d'images) : les deux slots de personnage sont des entiers **16 bits en `0x279668` et `0x27966C`** — espacés de 4 octets, ils portent toujours la même valeur. **`0x00580D20` est un piège, ne pas y revenir** : c'est un compteur d'écran *miroir*, décroissant, mais réécrit par le jeu en moins de 50 ms — lui écrire une grande valeur ne tient pas, et le figer bloque le jeu (écran titre comme chargement) car plusieurs routines s'en servent, l'une l'incrémentant jusqu'à 4, l'autre le décrémentant. Le vrai compteur de l'écran de sélection n'est **pas encore trouvé**. Barème des persos (ordre gauche-droite de l'écran, source vidéo HHBCFG Part 20) : Emi 0, Bahn 1, Picky 2, Jane 3 … **10 = repos**, **11 Del Sol, 12 Kuhn, 13 BM**.

**Objectif 1 terminé le 2026-08-07** : Del Sol, Kuhn et BM sont tous les trois confirmés jouables. Le mod livré est `fv2mod\play.py <delsol|kuhn|bm|normal>`, qui lance Supermodel et maintient le perso verrouillé sans rien modifier sur disque ; trois raccourcis `FV2 - *.cmd` à la racine du dossier jeu servent de cible pour Playnite. `fv2mod\unlock.py` reste l'outil d'expérimentation (s'attache à une instance déjà lancée). Deux pièges, tous deux payés cher :

1. Geler **avant** d'entrer sur l'écran de sélection, et maintenir en continu. Appliqué une fois déjà sur l'écran, le nom affiché change mais le perso chargé reste celui du curseur — la validation gagne la course. La vidéo de référence gèle puis laisse le jeu repasser par le boot.
2. **Ne jamais figer le compte à rebours.** Le jeu le réécrit à chaque frame : le figer crée un ping-pong à 10 Hz qui bloque la transition vers le combat (le jeu attend que le timer atteigne 0). C'était ça, le plantage à l'écran de chargement — pas le personnage. Les slots de perso, eux, ne sont jamais contestés par le jeu. Inutile de toucher au timer de toute façon : le perso est forcé quelle que soit la position du curseur.

Note : `epr-18022.ic2 not found` au chargement est un faux problème — ROM du drive board, région `required="false"` dans Games.xml, absente depuis toujours et sans effet.

Contrainte : le build Supermodel installé (0.3a-20251120) **n'a pas de débogueur intégré** — la seule option debug est `-dump-textures`. Pas de breakpoints : le scan mémoire se fait par diff d'images RAM.

Pour l'objectif 2 (textes/logos HD), le calque 2D n'est **pas** dans l'image RAM : c'est le Tile Generator (`F1000000-F111FFFF`), extrait à part de la save state dans `fv2mod\tile_generator.bin` (1152 Kio). Les blocs de save state s'énumèrent en cherchant les marqueurs `Src/.../*.cpp`, la chaîne `nextBlockOffset` étant inexploitable au-delà du premier bloc.

**Résultats Ghidra (2026-08-07)** — image `fv2_ram.bin` importée en `PowerPC:BE:32` base 0, projet dans le scratchpad, scripts `DecompileAt.java` / `WritersOf.java`. Corrections et trouvailles :
- Les curseurs sont **deux octets adjacents** : `0x279668` = **joueur 1**, `0x279669` = **joueur 2**. Ce que je lisais comme « un entier 16 bits » était les deux empaquetés. Trois paires existent : `668/669`, `66C/66D`, `67C/67D`. `play.py` marche parce qu'écrire 16 bits met P1=Emi et P2=le perso caché.
- **Le vrai compteur de l'écran de sélection est `0x00581408`** (l'affichage en tire ses deux chiffres via `_2_2_ >> 6`). `0x580D20` n'était qu'un miroir.
- Fonctions clés : `FUN_0005F340` déplacement du curseur, `FUN_0005FE38` affichage, `FUN_00060D34` initialisation.
- **Le déblocage existe déjà dans le jeu** : en maintenant le bouton de bit `0x200` (mot d'entrée `0x3179CC + joueur*4`) et en poussant à gauche depuis Emi (curseur 0) ou à droite depuis la case 10, le curseur saute à **11 = Del Sol**, à condition que `0x00581408 > 0x480`. Bits de direction dans `0x3179D0 + joueur*4` : `0x800` gauche, `0x400` droite. Reste à identifier quel bouton est le bit `0x200`.

**Jeu en anglais (résolu 2026-08-07)** : la ROM est la révision Japon et le TEST MENU affiche `COUNTRY` **en lecture seule** (les autres réglages, eux, s'éditent). La région est l'octet **`0x00120557`**, index dans la table de chaînes `0x2924CC` = `0:JAPAN 1:U.S.A. 2:EXPORT 3:ASIA`. L'écrire directement fonctionne, le jeu ne le réécrit pas, et les textes passent en anglais (un écran d'avertissement absent de la version JP apparaît, preuve du vrai changement de région). Le réglage est porté par `play.py --country usa` ; les lanceurs `FV2 - *.cmd` l'incluent. La NVRAM (`fvipers2.nv`) ne contient pas ce motif tel quel — patcher le fichier demanderait de décoder l'encodage de la backup RAM, non fait.

**MÉCANISME DE DÉBLOCAGE D'ORIGINE — reconstitué et vérifié en jeu le 2026-08-07.** Non documenté sur TCRF ni ailleurs.

*La manipulation* : curseur P1 sur **Emi (case 0)**, pousser **haut**, maintenir, basculer en **haut-gauche**. Second point d'entrée équivalent : depuis la **case 10**, haut puis haut-droite. Le bit `0x200` du code est donc une **direction**, pas un bouton — d'où le fait que ça ne valide aucun personnage, et que c'est infaisable au clavier avec des touches séparées : c'est un mouvement de stick. Condition : compteur `0x581408 > 0x480`, donc tôt dans le décompte.

*La progression, en trois temps* (branches de `FUN_0005F340`) :
1. état initial → la manipulation donne **Del Sol (11)** ; rangée 0-10
2. `0x0011F061` posé → Del Sol entre définitivement dans la rangée (0-11), la manipulation ne donne plus rien
3. `0x0011F06F` posé aussi → la manipulation donne **Kuhn (12)**

*Le verrou* : **`0x00279691` passe à 1 dès qu'une manipulation réussit** et neutralise tout le bloc secret (`else if (DAT_0011f060 == 0 && DAT_00279691 == 0)`). C'est ce qui empêche un second déblocage dans la même session — le remettre à 0 permet de réessayer. Vérifié : avec `0x11F061=1`, `0x11F06F=1` et `0x279691` relâché, la manipulation donne bien Kuhn.

*Del Sol devient permanent, Kuhn jamais* — observé par Frédéric et confirmé par le code : la borne de rebouclage vaut `'\n'` (10) à l'état initial puis `'\v'` (11) dans les deux branches suivantes, **elle ne monte jamais à 12**. Del Sol (11) devient donc une vraie case, atteinte en rebouclant à gauche depuis Emi ; Kuhn (12) est toujours au-delà de la borne, si bien qu'il occupe momentanément la case d'Emi et disparaît dès qu'on bouge. Il est transitoire par conception, à redéclencher à chaque fois.

*Le code Kuhn est orphelin sur la version arcade* — **`0x0011F06F` n'a aucun écrivain** dans toute la ROM (seule référence : la lecture par `FUN_0005F340`). La troisième branche existe donc mais rien ne l'active en jeu normal, ce qui explique qu'aucun code Kuhn n'ait jamais été documenté sur borne. Réserve : une écriture par pointeur calculé échapperait à l'analyse statique. En revanche `0x0011F061` est bien écrit par `FUN_0000ABC4` : à `0xAE50` quand un compteur en `0x11F298` dépasse le seuil `0x031C8240`, et à `0xB0D4` quand un compteur en `0x110B69` (incrémenté de 4) atteint 64 — mais ce second site pose aussi `0x11F060`, dont la non-nullité **désactive** tout le bloc secret.

Conditions de déblocage de la version **Dreamcast**, fournies par Frédéric et cohérentes avec `BONUS_STG_FLAG` (= `0x581461`, aussi étiqueté `*BONUS WIN`) : battre Mahler au stage 7 en moins de 5 min 50 avec au moins la moitié de sa vie, ou par Super K.O. / retrait d'armure, ce qui ouvre le stage bonus ; y battre Kuhn le débloque.

*BM n'a aucun chemin* : le code ne produit que `0xb` et `0xc`. Pour lui — et pour rendre Kuhn permanent — le patch d'instruction en `0x5F3BC`, qui porte la borne à 14, reste la seule voie.

**Pour tester confortablement** : recharger `0x00581408` à `0x1800` dès qu'il descend sous `0x1000` donne un compteur qui repart de 99 sans casser l'affichage à deux chiffres (l'affiché vaut `(halfword en 0x58140A) >> 6`, garder ≤ 99 sinon indexation hors bornes). Combiner avec une save state `F5` sur l'écran de sélection, rechargée par `F7` avant **chaque** essai — le code par la gauche exige que le curseur soit exactement sur 0.

**ROSTER COMPLET DÉBLOQUÉ (2026-08-07) — une seule instruction.** Le gestionnaire de curseur a trois modes selon `(DAT_00580f00 & 0xc0) == 0xc0` ; dans ce mode le curseur reboucle sur **14** au lieu de 10, donc Del Sol/Kuhn/BM/14 deviennent accessibles à la flèche. Or `0x580F00` n'est **pas** un drapeau de progression : c'est l'état brut du port d'entrée matériel (`0xFE040018`), rafraîchi chaque frame par `FUN_00004354` — inutile d'y écrire. Les bits `0xC0` sont les deux boutons opérateur Service+Test, inexploitables à la main puisque Test ouvre le menu.

La solution est de patcher le test : **`0x0005F3BC` : `2C 80 00 C0` (`cmpwi r0,192`) → `2C 80 00 00` (`cmpwi r0,0`)**. La condition devient vraie quand aucun bouton opérateur n'est maintenu, donc en permanence. Vérifié : le curseur parcourt 0→14. **Attention, le jeu recharge ce morceau de code** (décompression depuis la ROM), il faut donc réappliquer le patch en boucle, pas une seule fois.

Livré dans **`fv2mod\roster.py`** : réapplique le patch **uniquement quand il relit l'instruction d'origine** `2C8000C0`, et recharge le compte à rebours `0x581408` à `0x1800` quand il descend sous `0x1000`. Cette vérification n'est pas un luxe — une première version écrivait à l'aveugle et corrompait la mémoire pendant le boot, avant que le code ne soit décompressé : Supermodel partait en `unknown R32 / R16` et le jeu plantait.

Diagnostic du nom manquant de BM, pour la reprise : `FUN_00060184` traduit le curseur via une table de 15 octets en **`0xB16B8`** (`0B 01 07 05 02 08 00 04 06 03 0A 0E 0D 09 0C`), qui indexe un tableau d'**identifiants de texte 16 bits en `0xB1658`**. Ce tableau n'a que douze entrées valides (plage `0x12xx`) ; les curseurs 11 à 14 pointent au-delà, sur `0xC000`, `0x0000`, `0x0000`, `0xC020`. **BM (curseur 13) tombe sur l'entrée 9, qui vaut `0x0000`** — Sega ne lui a jamais attribué d'identifiant de texte. Le corriger suppose de trouver ou créer un id « BM » puis de l'écrire en `0xB1658 + 9*2`.

Cosmétique restant, à traiter plus tard : au-delà de l'indice 10 les noms et portraits sont faux ou absents (la routine d'affichage `FUN_0005FE38` garde `< 11` et sa table de positions n'a que 11 entrées). En particulier **l'indice 14 est un « faux Kuhn » à supprimer** — Frédéric soupçonne qu'il s'agit en réalité de Bahn mal étiqueté.

Le lanceur `play.py` utilise désormais **496×384**, la résolution native du Model 3, comme valeur par défaut de `--res`.

**Piste pour rendre les cachés réellement sélectionnables** (le mod actuel *force* un perso, il ne l'ajoute pas au menu). Frédéric rapporte que sur la **version Dreamcast** les cachés s'atteignent en poussant le curseur au-delà des extrémités de la rangée : vers la droite on obtient BM, puis Kuhn, puis Del Sol, puis retour à Emi — un **cycle circulaire**. Comme la valeur du perso *est* la position du curseur (Emi 0, Bahn 1, Picky 2…), les cachés sont simplement les cases hors champ, et l'arcade doit avoir une butée sur le déplacement. Hypothèse à tester : les deux tableaux collés en `0xB17D0` (9 entrées) et `0xB17DC` (12 entrées, le premier plus `06 07 08`) sont la séquence de positions autorisées et la séquence complète — recopier la longue sur la courte ferait cycler le curseur sur les 12. Point non élucidé : l'ordre d'affichage Dreamcast (BM, Kuhn, Del Sol) est décroissant par rapport aux valeurs 13, 12, 11.

**Modes de jeu (objectifs 3-5, entamés le 2026-08-07)** : le **mode Survival se déclenche en écrivant 1 en `0x0058145F`** (avec `0x120550 = 1`) — vérifié, « SURVIVAL MODE » s'affiche alors en haut à gauche. La manipulation P+K+G au démarrage que décrivait Frédéric n'est pas confirmée par le code et n'a jamais fonctionné ; inutile d'y revenir.

Ces adresses viennent d'une **table du menu de debug** à pas de `0x20` octets, très exploitable : `+00` = pointeur vers le libellé, `+0C` = adresse de la variable, `+1C` = type. Repères : `0x116ED4` = `*SURVIVAL KANOU` → `0x120550`, `0x116EF4` = ` SURVIVAL MODE` → `0x58145F`. Attention, quand le type vaut `0x10010F01` (au lieu de `0x00010F01`) le champ `+0C` est un **index**, pas une adresse — c'est le cas de `*PLAY KUHN` (`0x117034`, index `0x3C`) et `*PLAY DELSOL` (`0x117054`, index `0x3D`), dont la résolution reste à trouver. Cette table recense aussi `SURVIVAL FLAG`, `RANDOM_CHARA`, `BONUS_STG_FLAG`, `CPU0_flag`, `CPU1_flag`.

**La table de debug se déroule entièrement** : 61 entrées, pas de `0x20`, en se calant sur `0x116ED4` (le début n'est pas aligné sur une frontière ronde — c'est ce qui m'avait fait échouer une première fois). Adresses les plus utiles :
- **`*1P CHARA` → `0x007005B8`**, **`*2P CHARA` → `0x007075B8`** : l'identifiant réel du personnage en combat. C'est la source de vérité pour savoir qui est qui, et de quoi imposer n'importe quel perso **y compris BM**.
- `*1P COLOR` → `0x007005B9`, `*2P COLOR` → `0x007075B9`
- `*ENTRY 1P` → `0x00700000`, `*ENTRY 2P` → `0x00700100` (structures joueur, pas de `0x100`)
- `*ROUND NO` → `0x0058145C`, `*BONUS WIN` → `0x00581461`, `*GAME FRAME 1P/VS` → `0x00581418`/`0x0058141C`

**Il n'existe pas de `PLAY BM`** — seulement `*PLAY KUHN` et `*PLAY DELSOL`. Passer par `1P CHARA` est donc la voie générale, et elle couvre BM.

**Deux numérotations distinctes**, source de confusion récurrente — ne pas les mélanger :
1. *Curseur de sélection* : Emi 0, Bahn 1, Picky 2, Jane 3 … 10 = slot aléatoire, 11 Del Sol, 12 Kuhn, 13 BM, 14 « faux Kuhn ».
2. *Identifiant du personnage en combat* (`1P CHARA` en `0x7005B8`) : **mesuré Bahn = 1, Picky = 7**.

La conversion se fait par la table de 15 octets en **`0xB16B8`** (`0B 01 07 05 02 08 00 04 06 03 0A 0E 0D 09 0C`), lue par `FUN_00060184` : `identifiant = table[curseur]`. Les deux mesures la confirment. Elle donne pour les cachés — déduit, non vérifié — Del Sol **14**, Kuhn **13**, BM **9**.

**La numérotation `1P CHARA` est la liste de chaînes en `0x8C637`**, lue dans l'ordre :
`0 GRACE, 1 BAHN, 2 RAXEL, 3 TOKIO, 4 SANMAN, 5 JANE, 6 HONEY, 7 PICKY, 8 MAHLER, 9 BM, 10 CHARLIE, 11 TECHNO, 12 DURAL, 13 KUHN, 14 DELSOL, 15 KUMA.`
Bahn = 1 et Picky = 7 le confirment par la mesure. Après KUMA viennent `MOTION`, `KAMAE`, `SYAGAMI`, `WALK`… : des noms d'animations, **d'où le gel à l'identifiant 16** — la liste des combattants s'arrête à 15.

Conséquence : le « personnage inachevé » vu en forçant 15 **est KUMA**, l'ours (cf. `BONUS_STG_FLAG`). Et **TECHNO = 11**, **DURAL = 12** sont accessibles par le même biais — Dural étant le clin d'œil à Virtua Fighter dont Kuhn s'inspire.

Ne pas confondre avec la table `0xB1758` (KUMA, DELSOL, KUHN, EMI, CHARLIE, BM, MAHLER…), qui est encore un autre ordre et ne sert pas à ça.

**Réglages GAME ASSIGNMENTS** : ils occupent `0x120540`–`0x12055A`, un octet chacun. Identifiés à ce jour : **`0x120550` = SURVIVAL MODE** (1 ON / 0 OFF, mesuré par diff avant/après bascule dans le menu de test), `0x12054E` = DIFFICULTY (index de la table `0x2924B8`), `0x120557` = COUNTRY. La fonction d'affichage du menu est `FUN_0006CCA4` ; elle liste treize variables pour douze libellés, donc la correspondance ne se déduit pas de l'ordre — la mesurer par bascule est la méthode fiable.

**API de dessin (objectif 5, le menu — entamé le 2026-08-07)** : `FUN_00006B3C(element)` empile un paquet de 8 mots dans une liste d'affichage, en lisant la table d'éléments en **`0x3003CC`**. Les positions se posent avant, par `FUN_00002638(x,y,z)` et `FUN_00002610(x,y,z)` — que Ghidra décompile à vide parce qu'elles prennent leurs arguments en registres flottants ; ne pas croire qu'elles sont vides. `FUN_000081F4(id)` pose un attribut.

Point clé pour modifier l'affichage sans injecter de code : **chaque identifiant d'élément est une constante immédiate `li r3,imm`** juste avant l'appel, donc patchable en 4 octets. Écran titre = `FUN_00066068`, identifiants dans la plage `0x6xx-0x7xx` (l'écran de sélection utilise `0x12xx`). Sites repérés : `0x066140` = `li r3,0x06BE`, `0x0661D4` = `li r3,0x06BF`, `0x06626C` = `li r3,0x06BC` — les trois textes variables ; `0x706` et `0x701` reviennent dans chaque bloc (cadre commun). Les blocs sont gardés par `DAT_00581950 & 1` puis `& 2`, soit les deux joueurs.

**La liste d'affichage est lisible en RAM** — c'est l'outil qui remplace la déduction par la mesure. Pointeur en `0x580F9C` (valait `0x007D8010`), curseur en `0x580FA8`. Les paquets font **40 octets**, commencent par le mot `0x06000000`, et leur **mot 7 contient `table[element]` en boutisme inversé** ; on retrouve l'identifiant en cherchant ce pointeur dans la table `0x3003CC`. Outil : `fv2mod\displaylist.py`. Piège : le tampon **n'est pas vidé entre les images**, donc un instantané mélange la trame courante et des restes — il faut procéder par différentiel entre deux écrans, pas lire un instantané isolé.

**L'écran titre est dessiné par `FUN_00065C40` et `FUN_00066DAC`** — établi par différentiel de listes d'affichage (save state de l'écran titre contre instantané de l'intro), pas par déduction. 88 éléments lui sont propres, dont des **suites contiguës** qui trahissent des lignes de texte dessinées caractère par caractère : `0x0172-0x0188`, `0x069F-0x06B2`, `0x08D2-0x08D7`. Sites `li` correspondants : `0x69F/0x6A0/0x6A2/0x6A5` dans `FUN_00066DAC` (vers `0x066F58-0x066F88`), et `0x6A1/0x6A3/0x6A6/0x6A8` plus tout le groupe `0x8D2-0x8D7` dans `FUN_00065C40` (`0x065C80-0x065D1C`). Ce dernier groupe, six identifiants consécutifs chargés par six instructions voisines, est le meilleur candidat pour un premier essai de substitution.

Contrainte de conception relevée par Frédéric : **l'écran titre ne dure presque pas** en freeplay, et Start y mène directement à la sélection. Un menu a besoin d'un écran qui attend — soit désactiver le freeplay dans `COIN ASSIGNMENTS`, soit loger le menu entre Start et la sélection. Astuce pour l'analyser malgré sa brièveté : une save state `F5`, exploitable ensuite sans contrainte de temps.

**Objectif de Frédéric pour le menu**, formulé le 2026-08-07 : changer le comportement de Start — hors écran titre (intro, démo) Start doit amener à l'**écran titre** ; sur l'écran titre, Start doit afficher un **menu par-dessus** ; le choix mène au mode voulu. Trois briques : variable d'état d'écran, détournement de Start, affichage du menu.

**Recherche de la variable d'état : approche par les données abandonnée.** Quatre save states comparées (intro, titre, sélection, combat ; extraites en `fv2mod\dl_*.bin`) ne laissent que trois octets à quatre valeurs distinctes dans le bloc d'état — `0x580DFC` (9/15/0/5), `0x5813AF` (6/1/0/3), `0x5813D3` (6/5/0/14) — aucun ne ressemblant à une énumération dense. `0x58FDB3` avait l'air prometteur sur trois écrans (1/2/0) mais vaut 0 en combat aussi : écarté. **Reprendre par le code** : chercher le dispatcher d'écrans (switch ou table de fonctions) depuis la fonction principale, et en déduire la variable — une machine à états se reconnaît à sa structure, pas à ses valeurs.

**L'aiguillage des écrans est indirect** — deux pistes classiques écartées par la mesure, ne pas les refaire : (1) pas de **table de pointeurs de fonctions**, un balayage des 8 Mo cherchant les adresses exactes des fonctions d'écran connues ne donne que 2 occurrences isolées ; (2) **aucune référence entrante** vers `FUN_00065C40`, `FUN_00066DAC` ni `FUN_0005FE38` — Ghidra ne leur trouve pas un seul appelant. Elles sont donc atteintes par adresse calculée. Piste **non concluante** à connaître avant de la reprendre : en `0x3028A0-0x3028E0` et `0x30291C-0x30295C` s'alignent des valeurs croissantes qui ressemblent à des adresses de code (`0x65B50`, `0x65B6E`, `0x65B8C`… espacées de `0x1E`), et `FUN_00065C40` y figure. J'y ai vu une table de saut de `switch`, mais **le désassemblage ne le confirme pas** : à `0x65B50` il n'y a pas d'en-tête de switch (pas de borne suivie d'un `bctr`), plutôt une boucle et un accès indexé à une table de données en `0xB1E20`. À vérifier ou écarter avant d'aller plus loin.

Pour reprendre : suivre les branchements indirects (`bctrl`/`blrl`) depuis la boucle principale, ou capturer une adresse de retour en cours d'exécution. C'est le préalable aux trois briques du menu.

Échec instructif à ne pas refaire : j'ai d'abord parié que `FUN_00066068` dessinait l'écran titre, en me fondant sur le nombre d'appels de dessin. Le patch s'est posé proprement mais rien n'a changé à l'écran — ce n'était pas le bon écran. Toujours mesurer quelle fonction dessine, ne jamais le déduire.

Limite assumée : la substitution ne permet que de **remplacer** des éléments, pas d'en ajouter. Un vrai menu à cinq entrées demandera de l'injection de code.

**Carte de symboles — à charger en début de séance Ghidra.** `fv2mod\symbols.py` régénère `symbols.csv` (84 entrées : 56 noms venant des tables de debug de Sega, 28 de nos mesures) ; le script Ghidra `ApplySymbols.java` (dans le scratchpad) le réinjecte — renomme les fonctions, étiquette le reste. Pour enrichir, ajouter au dictionnaire `NOTRE_TRAVAIL` en tête de `symbols.py` puis relancer. Le balayage des tables est **volontairement borné** aux plages `0x116A00-0x117400` et `0x11D100-0x11D400` : sans cette contrainte le test structurel remonte 2202 faux positifs. `symbols.csv` est publiable tel quel, contrairement aux sorties du décompilateur.

Sur la question d'une **décompilation exhaustive** : techniquement possible, mais sans intérêt pratique — sortie non typée et non nommée, et surtout **non recompilable** puisque le programme est compressé en CROM. L'approche qui marche reste le ciblage adresse par adresse, capitalisé dans la carte de symboles.

**Objectif différé, décidé le 2026-08-07** : tenter plus tard un vrai patch ROM du déblocage, pour se passer du patch runtime. L'obstacle connu est identifié — le programme étant compressé en CROM, il faudra reverser le format LZSS et recompresser, ou détourner le décompresseur au vol. Le menu de debug expose un `<LZSS_INFO>`, ce qui est le point d'entrée le plus prometteur. Ne pas relancer ce chantier sans que Frédéric le demande : la route runtime a été choisie en priorité et elle est fonctionnelle.

Voisins : [[project_3sx_hd_assets]] pour l'approche remplacement de textures.

**L'amorce de FV2 est en clair, et elle est petite (mesure du 2026-08-22).** Le decompresseur LZSS vit forcement dedans : code entre **`0xFFF01560` et `0xFFF03580`** dans la CROM (offset 0x701560-0x703580 de `fv2_crom_swap16.bin`), soit ~8 Ko, 24 `blr` et 12 `mflr` — une douzaine de fonctions, lisibles en une seance. Le menu de test le nomme lui-meme : `LZSS_INFO`.

Comparaison avec l'amorce de VF3 a la meme adresse PPC 0xFFF00000 : **seulement 2,7 %** des blocs de 16 octets non triviaux sont communs. Les deux amorces ne partagent donc PAS le meme chargeur — inutile d'esperer lire celui de FV2 par calque sur [[project_vf3_model3]]. Ce que VF3 apporte, c'est la methode (crom.py, projet Ghidra avec r13 pose avant l'analyse), pas le code.

**Trois routes vers un patch ROM permanent**, par cout croissant : (1) patcher un octet LITTERAL du flux LZSS, quand l'octet vise en est un — pas de compresseur necessaire ; (2) ajouter une table de correctifs dans l'espace libre de l'amorce, appliquee APRES decompression — robuste, et c'est la route industrielle ; (3) reverser le format et recompresser — le plus cher, avec la contrainte de taille du flux.

## CORRECTION MAJEURE (2026-08-22) : FV2 n'est pas en LZSS, c'est du GZIP

Le postulat central du projet etait faux. La CROM de FV2 commence a l'offset 0 par un **fichier gzip complet** : magie `1f 8b`, methode 8 (deflate), drapeau FNAME, nom d'origine **`foo.bin`**, date de compression **1998-03-26 16:01:08 UTC**, systeme Unix. Ce qui l'a fait croire : le menu de test nomme son entree `LZSS_INFO` — l'etiquette de Sega ne decrit pas l'algorithme.

Trois preuves, toutes verifiees : les tables canoniques de DEFLATE sont dans l'amorce en 16 bits BE (`cplens` 0xFFF03604, `cplext` 0xFFF03642, `cpdist` 0xFFF03680) et le decompresseur est le `huft_build` de zlib ; `zlib.decompressobj(-15)` decompresse le flux entier et le **CRC32 du pied gzip concorde** ; les **2 701 982 octets** obtenus se posent en **RAM a l'adresse 0**, identiques a 99,9 % a un releve de RAM en cours de jeu. Un seul membre gzip dans toute la CROM.

**Consequence : plus rien n'est a reverser, et le patch ROM permanent est resolu.** Outil livre : `fv2mod/gzip_crom.py` (`extraire` / `injecter`). Le gzip d'origine fait 897 285 octets ; recompresse par Python en niveau 9 il en fait 882 022, soit **15 263 octets de marge** — un patch tient donc a la meme place. Aller-retour teste avec l'octet du patch roster : `0x0005F3BC` contient bien `2C 80 00 C0` (`cmpwi r0,192`) dans l'image decompressee, comme en RAM.

Il reste **une seule marche** : re-entrelacer la CROM sur les quatre EPROM pour produire un zip jouable (`build_crom.py` ne fait que le sens deinterleave) — exactement le meme reliquat que pour VF3, voir [[project_vf3_model3]]. Une fois franchie, tout ce que `roster.py` et le menu console maintiennent a chaud peut devenir permanent.

**Le README public du depot fv2-model3-research dit encore LZSS : a corriger.**
