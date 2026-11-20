---
name: project_3sx_bgm_remix
description: "Mod 3SX ajoutant des BGM Types alternatifs — compilé et validé en jeu ; briefing complet dans C:\\Users\\frede\\Downloads\\3sx-mod-briefing.md."
metadata: 
  node_type: memory
  type: project
  originSessionId: 212b918c-b482-48f4-98ba-8a572ee9396f
  modified: 2026-08-06T22:50:15.739Z
---

**Briefings à jour, à lire d'abord, ils font autorité sur cette note :**
- `C:\Users\frede\Downloads\3sx-mod-briefing.md` — musique et structure des menus.
- `C:\Users\frede\Downloads\3sx-palettes-briefing.md` — **palettes de couleurs**, chaîne de capture
  MAME, conversion des `.act` de re:THIRD, et le **problème non résolu du ciel d'Ibuki** avec tout
  ce qui a été écarté.

**Outils préservés** dans `C:\Users\frede\Downloads\3sx-outils\` (`palettes/`, `audio/`, `mame/`) —
les scratchpads de session disparaissent, pas ça.

**Chargeur de palettes externes, fait et validé en jeu le 2026-08-06.** Module `port/video/pal_remix`,
calqué sur `bgm_remix`. Un jeu de couleurs = un dossier sous `<resources>/pal_remix/<jeu>/`, avec
`char-NN.pal` et `stage-NN.pal` indexés par la **numérotation moteur** de constants.h. Un `.pal` est
l'entrée AFS **copiée octet pour octet**, donc `init_trans_color_ram` la lit sans rien apprendre de
neuf. Branché aux cas 1 (personnages) et 2 (décors) ; le cas 2 sert aussi aux palettes d'UI, qu'on
distingue par la destination — un décor va toujours en `ColorRAM[300]` (`data == 0x12C`).
`letter_data_64_selectable()` interroge le disque : un jeu n'est proposé que si son dossier contient
quelque chose. Validé : Akuma est **ligne 0** de l'écran (alphabétique) mais personnage **14**, et le
log confirme le chargement de `char-14.pal` — donc `Custom_Row_To_Char[20]` (dans eff64.c) est juste.
Export des palettes d'origine : `export_pal.py` dans le scratchpad de session.

**Signature d'une palette 3rd Strike, mesurée sur les 40 fichiers** : bit de poids fort à 1 sur
**98,4 %** des couleurs — exactement 63/64, l'exception étant l'emplacement transparent en tête de
chaque palette — et 64,5 à 95,1 % de paires adjacentes formant une rampe. Critère très net, utile
pour reconnaître des palettes dans n'importe quel binaire.

**Le bit alpha à 98,4 % est un artefact du portage console**, ajouté pour le matériel PowerVR/GS.
Ne PAS l'utiliser pour reconnaître des palettes d'arcade. Critère indépendant du format, mesuré
lui aussi sur les 40 fichiers : rampes 64,5-95,1 % **et** 34 à 64 couleurs distinctes par palette
de 64. La condition sur les couleurs distinctes est indispensable — sans elle, un remplissage
constant passe le test des rampes à 100 %, ce qui a produit une série de faux positifs.

**ROM CPS3 fournies le 2026-08-06** (`Downloads\SF3.3 music\sfIII.zip`, `sfIII2.zip`, jeux MAME
complets). Entropie par SIMM : `sfiii-simm1` (programme New Generation) **7,96-7,99 = chiffré** ;
`sfiii2-simm1/2` (programme 2nd Impact) **2,49-5,21 = en clair** ; graphismes des deux jeux
6,33-7,53, ce sont des pixels. Cherché les palettes dans les 54 SIMM avec le critère ci-dessus,
trois dispositions 16 bits et les deux boutismes : **rien**. Les candidats trouvés dans les SIMM
programme de 2nd Impact sont des dégradés à canal unique — des suites d'octets croissants lues
comme des couleurs. Les palettes CPS3 sont donc **compressées** dans le programme.
Les savestates FBNeo ne donnent rien non plus sous aucune disposition : compressés.
**Seule voie restante : lire la palette RAM à l'exécution**, en laissant l'émulateur déchiffrer et
décompresser. **Fait le 2026-08-06, et ça marche** — voir la recette ci-dessous.

**Recette d'extraction des palettes CPS3 par MAME** (aboutie, 24 personnages sortis) :
MAME 0.289 est installé en `C:\mame` (winget `MAMEdev.MAME`, il exige `--location`). Les jeux ROM
passent sous les variantes **sans CD** : `sfiiin` et `sfiii2n` ; `sfiii`/`sfiii2` réclament un CHD
absent. Scripts Lua dans `C:\mame` : `pick_char.lua` pilote une partie et vide la palette,
`capture_pal.lua` moissonne le mode démonstration.
- Le partage mémoire à lire est **`:colourram`**, 262144 o, énumérable par
  `manager.machine.memory.shares`.
- **Piège :** `emu.add_machine_frame_notifier` renvoie un jeton d'abonnement ; s'il n'est pas gardé
  dans un global il est ramassé et **rien ne se déclenche**, sans erreur.
- Compter ~1500 trames de démarrage avant que la carte ait fini de vérifier ses SIMM.
- `-nothrottle -video none` fait tourner l'émulation ~11x le temps réel ; `-snapshot_directory`
  par run évite d'avoir à effacer (la suppression sous `C:\mame` est bloquée par une protection).
- Format des couleurs : **big-endian xBGR555**, bleu en poids fort. Le portage console est en
  petit-boutiste ARGB1555, rouge en poids fort — il faut donc **inverser R et B** en plus du
  boutisme. Symptôme quand on l'oublie : peau bleue, gi blanc (le blanc est insensible).
- Disposition : emplacement **0** = palette du corps, le seul qui suive le bouton de couleur ;
  **1-6** = effets, fixes ; **2040-2043** = le bloc de 256 couleurs que le portage range en
  `ColorRAM[502]` (vide sur la carte). L'emplacement 8 duplique le 0.
- Grille de sélection : New Generation = 5x2, curseur sur Ryu ; 2nd Impact = une rangée de 13,
  Akuma caché. New Generation donne 6 coloris par bouton, 2nd Impact 6 sur les 7 existants.
  **Yun et Yang partagent une case en New Generation** : boutons 0-2 = Yun, 3-5 = Yang.

**Résultat installé** : `pal_remix/new-generation` 11 personnages, `pal_remix/2nd-impact` 13.
Vérifié contre les sprites de https://capcomcolors.neocities.org (copies locales dans
`Downloads\SF3.3 music\Capcom Colors_*_files`, suffixes `__4SX` pour NG et `_YBxs` pour 2I) :
New Generation quasi tout exact au bit près, 2nd Impact 65/78 exacts et 67/78 au-dessus de 95 %.
Ces sprites sont une **vraie référence** — leurs couleurs tombent toutes sur la grille 5 bits.
Manquent Akuma et Gill, non sélectionnables par la voie normale.

**Disponibilité au grain de l'élément** (demandé le 2026-08-06) : un jeu de couleurs n'est proposé
à un personnage que s'il possède son fichier (`PalRemix_HasCharacter`), et une bande-son n'est
proposée sur un décor que si le pack couvre son code mix 1 (`BgmRemix_SoundtrackCoversStage`).
`letter_data_64_selectable()` prend un 3e paramètre, le sujet de la ligne, fourni par
`subject_64()` qui traduit la ligne affichée. Toujours interroger le disque ou le manifeste,
jamais une liste codée en dur : ajouter un fichier doit suffire à allumer l'entrée.

**Impasse confirmée le 2026-08-06 : pas de palettes exploitables dans Double Impact.** Les `.PK`
sont **compressés**. Cherché sérieusement, ne pas y revenir sans nouvel élément : zéro bloc à la
signature ci-dessus dans les packs personnages des deux jeux ; les quelques touches ailleurs sont
des rampes à 100 %, donc des remplissages constants, hors de la plage des vraies palettes. Quatre
dispositions 16 bits testées (ARGB1555, RGB565, ARGB4444, BGR555) sur les régions candidates :
8 à 46 % de rampes, loin du plancher de 64,5 %. Les savestates FBNeo de `sfiii`/`sfiii2` ne
contiennent pas non plus la palette RAM en clair (meilleur alpha 81 %, zéro touche).

**Thème de Gill du pack Online Edition, posé le 2026-08-05** : le rip OE n'en a pas, la source est
un remix de fan fourni par l'utilisateur (`SF3.3 music\...Psyche Out Remix...wav`). Installé en
`46_A_GIL.adx` dans `online-edition`, code 46 seul (47/48 y retombent). **Aucune boucle rendue**
dedans — 10 % d'erreur résiduelle, comme les FLAC d'OST — mais la piste rejoue la même position de
phrase 122.084 s plus loin. D'où : rogné à 211.899 s pour couper le fade final, boucle 89.815 s →
211.899 s, et un fondu de 120 ms avant la fin de boucle vers ce qui précède le point de départ, ce
qui rend le raccord continu par construction (rupture spectrale à 0.2 % d'un point pris au hasard).
**Gain laissé à l'unité** : la piste est à -10.2 LUFS, la plage du pack va de -10.7 à -6.9, donc
elle est déjà dans l'écart interne du pack ; la remonter à la médiane demanderait +1.1 dB et
écrêterait 16 fois plus d'échantillons sur un master déjà brickwallé. Rien n'a été écouté.

**Packs New Generation et 2nd Impact construits le 2026-08-05**, depuis le CDI Double Impact
(voir [[project-3sx-audio-formats]] pour le format `.ADP`). 22 pistes dans `new-generation`,
27 dans `2nd-impact`, en ADX bouclé sur le fichier entier — les thèmes de décor se terminent à
leur niveau moyen, donc ils ont été écrits pour boucler ainsi. **L'affectation piste → décor est
un placeholder** : rien sur le disque ne relie un numéro `M1xx`/`M2xx` à un décor, donc les
pistes sont posées dans l'ordre des fichiers face aux codes croissants. À corriger à l'oreille en
échangeant les noms de fichiers dans `remix.txt`. Les 20 jingles (fin en silence) sont convertis
mais non bouclés et non installés.

**Chantier ouvert au 2026-08-05, page DISPLAY** : la ligne « SCREEN ADJUST » du menu Option est
renommée « DISPLAY » et ouvre une page à 7 lignes (entrée 22 de `AT_Jmp_Tbl`, `Display_Menu` dans
menu.c). `SCREEN ADJUST` et `COLOR EDIT MODE` ouvrent une page ; `RESOLUTION`, `ARTWORKS`, `HUD`,
`BACKGROUNDS` portent une valeur. Décision de l'utilisateur : **ne pas toucher au sprite du
bandeau** — la page s'affiche donc sous le bandeau « SCREEN ADJUST ». Compilé et lancé, pas encore
validé à l'écran.

**Présentation des réglages pas encore implémentés** (choix de l'utilisateur, 2026-08-05) : une
valeur à la fois, gauche/droite fait défiler toutes les options, les indisponibles s'affichent en
grisé (`my_clear_level = 179`) et la ligne revient à la valeur disponible dès qu'on la quitte.
Retenu parce que les 5 valeurs de BACKGROUNDS font 344 px alors que la colonne n'en offre que 176.
`letter_data_64_selectable()` dans eff64.c dit combien d'entrées d'une ligne sont réellement
choisissables.

**Résolution interne réelle : 384×224** (pas 320×240), en dur dans les trois renderers.

**Écran Custom des décors** (entrée 23 de `AT_Jmp_Tbl`, `Background_Custom`) : ouvert en validant
sur `BACKGROUNDS = Custom`. **20 lignes, pas 16** — contrairement aux thèmes musicaux, les quatre
lieux qui apparaissent deux fois sont deux jeux d'assets distincts ; seul Q réutilise vraiment
ceux de Ken. A imposé `EFF04_Cursor_Data[9][16][2]` → `[10][20][2]` et un pas de 8 px au lieu de
10, ce qui met la dernière ligne à y=26 au lieu du 28 habituel.

Budget d'un libellé sur ces écrans longs : **29 caractères** (colonne de valeurs à x=+52, libellés
à x=-186, petite police à 8 px). « THE DOJO OF RINDO-KAN (MAKOTO) » en faisait 30, d'où la perte
du « THE ».

**Budgets de largeur de la page Display** (mesurés) : l'écart libellé→valeur est de **176 px** sur
toutes ses lignes, soit 12 caractères en grande police pour un libellé qui porte une valeur — d'où
« CHAR. COLOR ». Et la chose la plus large que le jeu dessine s'arrête vers **x=+190** ; c'est aussi
le seuil que le mod BGM s'était donné (`BGM_REMIX_NAME_WIDE_MAX = 9`).

**Espacement vertical par police** : petite = 8 à 10 px, grande = **18 px** (menu Direction) à 22 px
(menu Option). La bande utilisable faisant 150 px, une liste en grande police plafonne à 8-9 lignes
— c'est ce qui a imposé la pagination pour les 20 personnages (4 pages de 5, `Character_Custom`,
entrée 24 de `AT_Jmp_Tbl`).

**Les trois écrans Custom sont convertis et vérifiés au 2026-08-05** : tracklist BGM, décors,
personnages. Même modèle — 8 lignes par page, personnage en **condensé** (`effect_18`, messages),
détail entre parenthèses + points en **petite police de menu** (`effect_61`), valeur par
`effect_64`, sortie et flèches en graphismes, indicateur `PAGE n` en sprite, pas de bandeau.

**Le tri alphabétique n'est qu'un ordre d'affichage.** `Custom_Buff` reste indexé par thème, dans
l'ordre de `custom.txt` ; `Custom_Row_To_Theme[16]` traduit la ligne affichée. Vérifié en jeu :
1ʳᵉ ligne page 1 → `akuma`, 1ʳᵉ ligne page 2 → `makoto`, valeurs conservées d'une page à l'autre.
Les écrans décors et personnages ont le même décalage latent, **pas encore de table** — leur
tampon est indexé par position affichée, à corriger le jour où ces réglages agiront.

**Largeurs de `effect_18`** : `x` et `y` sont désormais des paramètres (ils étaient en dur à −143
et 199). La tracklist BGM est à −164 et non −143 comme les deux autres : sa colonne de valeurs
affiche des noms de packs, et chaque pixel gagné à gauche lui en coûte un — à −143 il ne resterait
que 11 caractères, or « Online Edition » en fait 14.

**Recette d'un écran Custom long** (référence : `Character_Custom` puis `Background_Custom` dans
menu.c) : libellés par `effect_18` → système de messages (`msgSysDirTbl`), seule voie vers la fonte
**condensée** ; les points de conduite sont écrits en dur dans la chaîne, padée à une largeur
constante (~8,2 px/caractère). Valeurs par `effect_64` avec `Order = 3` (`EFF64_SUDDENLY`, que j'ai
implémenté — il était vide) pour éviter l'entrée par la droite. Pas de bandeau : indicateur `PAGE n`
par deux `effect_66` (`char_ix 0x47` motif `0xB`, puis `0x40` motif = n° de page). Sortie et flèches
par quatre `effect_40` avec `id = 3`, qui lit `Page_Nav_Value` et descend de 44 px. Pas de curseur
`effect_04` : les lignes s'éclairent seules, sinon il ne peut pas suivre une ligne de navigation
dont l'indice bouge avec le nombre de lignes de la page. `Menu_Cursor_Move = 0` obligatoire.

**`Menu_Cursor_Move` est une barrière d'entrée, pas un compteur décoratif** : `MC_Move_Sub` ignore
toute saisie tant qu'elle est > 0, et **seul `effect_61` la décrémente** (eff61.c, un par libellé).
La poser à une valeur supérieure au nombre de libellés créés gèle définitivement l'écran — plus
aucune touche, ni curseur, ni annulation. La poser plus bas est sans danger, elle passe en négatif.

**Repère écran mesuré sur capture** (2026-08-05) : l'origine est le **centre**, l'espace utile va de
**x = −192 à +192** et de **y ≈ 8 (bas) à 232 (haut)**, y croissant vers le haut. Un glyphe de la
grande police occupe environ ±6 en y. Une liste en grande police ne doit pas démarrer au-dessus de
y ≈ 200.

**Piège des work ids, coûté une frame de debug** : `Order[]` est indexé par work id et un slot ne
peut servir **qu'un seul effet vivant**. Un bandeau tué avec `Order[x] = 4` met plusieurs frames à
mourir ; si l'écran suivant crée un autre effet sur le même id dès la frame d'après, le bandeau
ressuscite et l'autre effet disparaît. C'est ce qui a fait disparaître la seule ligne Makoto de
l'écran Custom des décors (16ᵉ ligne, valeur en `0x64 + 16 = 0x74`, l'ancien bandeau Display).
Corollaire : le bandeau d'une page doit être **hors de la plage de works de la page qu'elle
ouvre**. Le mod BGM ne s'en apercevait pas parce que Sound_Test et l'écran Custom partagent `0x72`
avec le *même* sprite de bandeau — la résurrection y est invisible.

Contraintes de menu apprises ici : les bandeaux d'`effect_57` sont des motifs de
`_sel_pl_char_table` (données binaires), pas du texte — d'où la réutilisation. `Menu_Letter_Data`
et `Slide_Pos_Data_61` sont **parallèles**, indexés par libellé : en agrandir un impose l'autre.
`Menu_Suicide[4]` et `Order[148]` sont dans l'état réseau (`game_state.h`) — ne pas les agrandir.

Mod du port natif 3SX (Street Fighter III 3rd Strike, `crowded-street/3sx`) ajoutant une
3e valeur `Remix` à l'option **Options → Sound → BGM Type**, à côté de `Arrange` et `Original`.

**Approche retenue** (choix de l'utilisateur, 2026-08-04) : pistes ADX externes, un dossier par
pack sous `<resources>/bgm_remix/`, chacun avec un manifeste `remix.txt`
(`!name` + `code | fichier | libellé`). Repli automatique sur Arrange pour tout code non couvert.
Pas de repack de `SF33RD.AFS` — le dump légal de l'utilisateur reste intact.

Un `menu.txt` optionnel fixe l'ordre et les libellés de la ligne BGM Type, `arrange` et
`original` étant des mots réservés renommables. Packs prévus, dans cet ordre : Original PS2
(= `original`), Original CPS3, Arranged (= `arrange`), Online Edition, New Generation,
2nd Impact, Random, Custom. Les 6 dossiers existent avec un manifeste vide ; aucune piste
produite à ce jour.

Une BO sans mix par round (New Generation) ne déclare qu'une piste par stage, sur le code mix1 :
les rounds 2 et 3 y retombent, et comme les 3 rounds résolvent vers le même fichier, la piste
**continue sans coupure** à travers les transitions (`bgm_remix_continues` dans sound3rd.c).

**Pourquoi ça marche sans réécrire le moteur son** : `sys_w.bgm_type` sert d'index de premier
rang dans 4 tables parallèles (`bgm_table`, `bgm_exdata`, `bgm_selector`, `Letter_Data_A8`).
Ajouter une 3e entrée pointant sur les tables Arrange suffit ; seul le chemin de lecture audio
est détourné, dans `bgm_play_request()`.

**État au 2026-08-04 : validé en jeu.** Le pack **Online Edition** (30 pistes) est construit et
fonctionne. Directives du manifeste : `!name`, `!structure arcade|console`, `!volume <dB>`.
Les types `Random` et `Custom` se résolvent en une bande-son réelle au round 1 : Random tire au
sort (RNG de SDL, **jamais** celui du jeu que le netcode rollback rejoue), Custom lit
`bgm_remix/custom.txt` selon le décor. **L'écran Custom in-game est fait** : 16 lignes
« THÈME (PERSONNAGE) » + colonne de bandes-son, ouvert en validant sur `BGM Type = Custom`,
sauvegarde dans `custom.txt`.

**Pièges de l'UI de menu, chèrement appris** : `Menu_Letter_Data` et `Letter_Data_64` sont du
texte (pas des sprites) ; `Convert_Buff` ne fait que 12 cases par ligne et est dans l'état
réseau, d'où `Custom_Buff[16]` ; `EFF04_Cursor_Data` n'avait que **7 lignes par disposition**
et toutes sont **diagonales** — d'où une 9e disposition à 16 lignes droites. Bande verticale
utilisable : y=178 (sous l'en-tête) à y=28 (bas), y croissant vers le haut.

**Point tranché le 2026-08-05** : dans 3rd Strike le thème d'un personnage *est* celui de son
décor, donc « by stage » et « by character » désignent le même réglage — la distinction
Arcade/Versus de la note d'origine décrit comment le jeu choisit le décor, pas la musique. Rien
à coder pour ça. Quatre décors sont partagés : Alex/Ken, Sean/Oro, Yun/Yang, Necro/Twelve.

**Sources analysées** (dans `C:\Users\frede\Downloads\SF3.3 music`) :
- Le rip **Online Edition en XMA** contient 3 bandes-son : sans préfixe = Arranged
  (724 segments = `bgm_exdataDC` exactement), `o` = arcade CPS3 (429/432), `SF3OE_` = les
  remixes OE (30 pistes, 15 stages A/B, **pas de Gill**). Numérotation identique aux codes BGM.
  Le rip **MP3** du même dossier contient autre chose : à ignorer.
- FLAC d'OST (New Generation, 3rd Strike) : **aucune boucle**, masters de CD avec fondu.
  Détection automatique impossible, vérifié avec un contrôle synthétique (erreur 0 sur une vraie
  boucle, 36-49 % sur ces fichiers).
- Double Impact Dreamcast : impasse, ses 383 ADX sont des voix mono 22 kHz.
- PKG PS3 : chiffré, inspectable seulement par l'en-tête (Content ID à `0x38`).

**Outils** dans `C:\Users\frede\Downloads\` : `extract-afs.ps1`, `adx-loop.ps1` (inscrit les
points de boucle dans un ADX produit par ffmpeg), `build-oe-pack.ps1`.
Un détecteur de boucle en C est dans le scratchpad de session (`find-loop.c`).

- Clone de travail : `C:\Temp3sx` (le chemin est court exprès : `git clone` échoue en
  "Filename too long" sous le scratchpad de session).
- Patch exporté : `C:\Users\frede\Downloads\3sx-bgm-remix.patch`.
- Build : `C:\Temp3sx\build\application\bin\3sx.exe`.
- Recompiler : `MSYSTEM=MINGW64`, puis `CC=clang CXX=clang++ cmake -B build
  -DCMAKE_BUILD_TYPE=Release -G Ninja && cmake --build build --parallel`.
- **Puis installer, sinon on lance un vieil exe** : `cmake --install build --prefix
  C:/Temp3sx/build/application`. `cmake --build` écrit `build\3sx.exe`, qui ne peut pas tourner seul
  (shaders et assets vivent dans la disposition d'installation) ; `build\application\bin\3sx.exe`
  reste celui du build précédent tant qu'on n'installe pas, **sans aucun avertissement**. Le préfixe
  est obligatoire : celui du cache est `C:\Program Files (x86)\3sx`, qui échoue faute de droits.
- **Ne pas tuer le jeu avec `Stop-Process -Force`** quand on veut lire ses logs : la sortie d'erreur
  est tamponnée et la fin est perdue, ce qui fait croire à tort qu'une étape ne s'est pas produite.
  `$p.CloseMainWindow()` puis attendre.

**Deux pièges découverts dans le code d'origine, à ne pas re-chercher :**
1. Le flux SDL est ouvert en dur à 48 kHz et `header->sample_rate` de l'ADX n'était jamais
   utilisé — toute piste hors 48 kHz jouait au mauvais pitch. Corrigé dans le mod.
2. Les réglages son sauvegardés (BgmType, BGM_Level, SE_Level) ne sont appliqués à l'état
   runtime *que* si on ouvre le menu Sound. Le jeu redémarre donc toujours en Arrange.
   Bug préexistant, laissé tel quel — non demandé.
