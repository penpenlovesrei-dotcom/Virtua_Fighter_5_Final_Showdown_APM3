---
name: project_tuiles_hd
description: "Assets 2D HD du Tile Generator Model 3 dans Supermodel — le document qui fait foi est SupermodelSrc/Docs/TuilesHD.md."
metadata: 
  node_type: memory
  type: project
  originSessionId: 26deb3cf-f191-4f11-ad3c-f28efd6ac92f
  modified: 2026-08-15T08:51:26.274Z
---

**Le document qui fait foi est `SupermodelSrc\Docs\TuilesHD.md`**, versionné avec
le code — le lire en premier, il est plus complet et plus à jour que cette note.
Ce qui suit n'en est qu'un résumé de contexte.

Projet ouvert le 2026-08-11 : remplacer les graphismes 2D du Tile Generator
Model 3 par des assets HD, en override façon texture pack, dans
`C:\Users\frede\Documents\SEGA Model 3\SupermodelSrc` (dépôt git propre,
build MinGW par `build_dbg.sh`, à lancer depuis un bash MSYS2 `MSYSTEM=MINGW64`
— cf. [[reference_msys2_ca_bundle_vide]]).

**Le fait qui change tout, et qui contredit la doc historique** : dans cet arbre
`Render2D` ne décode plus aucune tuile. `AttachVRAM`, `AttachPalette`,
`AttachRegisters`, `WriteVRAM` sont des **stubs vides**. Tout le rendu 2D est un
**rastériseur CPU scanline** dans `TileGen.cpp` : `DrawLine(i)` est appelée
ligne par ligne depuis `Model3.cpp` entre deux tranches d'exécution PPC, compose
les 4 couches dans deux surfaces 512x384 RGBA (bas/haut selon `Above3D`), et
`Render2D` ne fait plus que téléverser ces deux surfaces en textures 496x384.
Donc : le point d'interception unique est `Draw4BitTilePair` / `Draw8BitTilePair`,
en C++, sans shader à toucher. Et la résolution n'est verrouillée qu'à trois
endroits : `TileGenBuffer.h`, `Render2D::Init`, `Render2D::PreRenderFrame`.

Autre point structurant : `WriteRAM32` est **l'entonnoir unique** de toute
écriture VRAM (les variantes 8/16 bits et `LoadState` y passent), donc un seul
hook y suffit pour invalider un cache.

**Identité d'une tuile** : jamais l'index de motif (simple offset VRAM, mobile),
mais le couple **(hash du contenu, index de palette)** — en 4 bpp la palette
vient de l'entrée de name table et un même motif sert en plusieurs couleurs.

**Étape 0 livrée et vérifiée en jeu** (mode dump) : `Src/Model3/TileDump.{h,cpp}`,
options `-tilegen-dump` et `-tilegen-dump-nogfx`, sortie dans
`Analysis/TileDump/<jeu>/`, lanceur `Dump tuiles 2D.cmd` à la racine du dossier
de jeu. **Entièrement passif** — c'est la convention des dumps d'émulateur, et
Frédéric a eu raison de la rappeler : une première version exigeait Alt+S ou une
période, elle a été remplacée. On joue, et tout ce qui apparaît est capturé une
fois, dédupliqué par hachage de contenu : un BMP 8x8 par tuile + `tiles.csv`,
une tilemap 512x512 + grille 64x64 + légende par disposition distincte de name
table, plus `layers/index.csv`. Deux filtres indispensables, trouvés à la
mesure : ne capturer une disposition qu'après **deux images identiques**
(sinon on collectionne les états intermédiaires pendant que le jeu construit
l'écran : 91 dispositions au lieu de 39 sur le même trajet), et ne rien écrire
si la couche est vide. Plafond de 256 dispositions par couche. Coût mesuré :
43 Mo pour 75 s de mode attract, dominé par les tilemaps.

**Découverte à confronter au HANDOFF** : sur l'écran de staff roll de FV2, le
texte `PRESS START BUTTON` et `CREDIT(S) 3/3` est **composé de tuiles 8x8 dans
la couche 0**, donc remplaçable tuile par tuile. Le §9 du HANDOFF supposait, à
partir de la version Dreamcast, que ces phrases étaient des images pré-rendues.
Vrai peut-être sur l'écran titre proprement dit, faux sur celui-là.
Cf. [[project_fv2_inventaire_2d]], dont la conclusion « motifs introuvables en
clair » reste exacte côté ROM : ils n'existent qu'après décompression, en VRAM,
ce que le mode dump capture précisément.

**Étape 1 livrée** (surface HD) : `TileGenScale` / `-tilegen-scale=<n>`, 1 à 8,
défaut 1. `TileGenBuffer` est alloué sur le tas avec `scale/stride/visibleWidth/
height` ; `TileGen::ScaleFromConfig` dans `TileGenBuffer.h` est la **source
unique** interrogée par `CTileGen` et `CRender2D`, qui dimensionnent
indépendamment — sans ça un désaccord ferait lire hors bornes au téléversement.
`GetLine` prend toujours un numéro de ligne **native**. Seuls les deux
`lineBuffer[x] = colour32` deviennent `WritePixel(lineBuffer + x*m_scale, ...)`,
qui écrit un bloc scale×scale ; à l'échelle 1 il dégénère en l'instruction
d'origine, donc l'échelle 1 est inchangée par construction. `Render2D` prend ses
dimensions du tampon lui-même. Mémoire : 600 Mo à l'échelle 8, ~50 Mo à 4.

**Ce qui n'a pas pu être vérifié, et pourquoi** : aucun A/B au pixel près entre
échelle 1 et 4. La capture d'écran du bureau (`CopyFromScreen`) rend des
résultats non fiables sur la fenêtre OpenGL, les save states de `Saves/` sont
incompatibles avec le binaire recompilé, et la fenêtre SDL n'accepte pas les
touches synthétiques — donc pas d'image déterministe atteignable depuis un
script. Vérifié en revanche : l'échelle est bien appliquée (ligne de journal
« Tile generator rendering at 4x »), et 22 captures montrent le rendu 2D correct
par-dessus la 3D sur des écrans variés.

**Étape 2 livrée et prouvée à l'écran** (override par tuile) :
`Src/Model3/TilePack.{h,cpp}` + `Src/Util/ImageRead.{h,cpp}`. **Pas de
manifeste** : le nom de fichier est la clé, donc on reprend un fichier écrit par
le dump, on le redessine plus grand, on le remet sous le même nom dans
`Assets/TilePacks/<jeu>/tiles/`. Taille imposée : 8 × TileGenScale, carré.
Option `TilePack` (défaut vrai) et `-no-tile-pack` pour comparer.
Lecteur d'images maison — **zlib est déjà lié** (`-lz` dans Makefile.Win32),
donc PNG 8 bits RGB/RGBA non entrelacé décodé à la main, plus BMP 24/32 bits.
Palette : `_pXXXX` vise une palette précise, `_pANY` ou l'absence de `_p` sert
de repli. Les **offsets de couleur** (registres 0x40/0x44) sont réappliqués aux
pixels HD, sinon l'art resterait allumé pendant les fondus ; d'où le paramètre
`palPair` ajouté à `Draw4/8BitTilePair`. L'alpha partiel est composité, ce que
le matériel ne sait pas faire, pour les bords antialiasés.

Preuve : pack de test de 1701 tuiles (le logo FV2, canaux rouge et bleu
échangés) généré depuis le dump — chargé « 1701 tiles, 0 rejected », logo affiché
aux couleurs échangées, géométrie identique. Les quelques tuiles absentes du pack
gardent leurs couleurs d'origine, ce qui confirme la granularité par tuile.
Ce pack est conservé sous `Assets/TilePacks/fvipers2.demo-couleurs-inversees/`
(renommé pour ne pas être chargé).

**Étape 3 livrée** (override de couche entière) : fichier
`Assets/TilePacks/<jeu>/layers/L<n>_<hash>.png`, même convention de nom que le
dump, **512 × TileGenScale carré** — la tilemap entière, pas la fenêtre visible,
pour que le défilement continue de marcher. Clé = hachage de la name table de la
couche, calculé une fois par image dans `CTileGen::ResolveLayerOverrides`
(appelé depuis `BeginVBlank` **et** `LoadState`). Le span remplacé consomme
exactement la même largeur qu'une paire de tuiles, donc le masque stencil
continue de fonctionner ; la source est `((x+scrollX)&511, (line+scrollY)&511)`.
Transparent = rien dessiné : l'image **est** la couche. Le hachage est sorti
dans `Src/Model3/TileHash.h`, partagé par le dump et le pack — leur divergence
serait un bug indébogable.

**Non implémenté, et c'est un choix** : zones de signature et trous. Sur FV2 le
contenu dynamique (noms de persos, texte clignotant) est sur la **couche 0** et
l'art fixe sur la **couche 2** — la séparation par couche suffit, la machinerie
serait inutilisée. À ajouter seulement si un jeu mélange les deux sur une couche.

Trace utile ajoutée : `Tile pack: layer N replaced by L<n>_<hash>` au premier
déclenchement, sinon un pack keyé par contenu ne dit jamais s'il a matché.

**Confirmé à l'écran par Frédéric le 2026-08-12** avec ses propres images HD du
logo SEGA (`L2_008a1e4c8b68b68c`) et de l'écran titre (`L2_ab8fdb84f0886f07`),
tous deux sur la couche 2, sans défilement. Le chargeur accepte deux tailles de
couche : `512×scale` carré (tilemap entière, pour ce qui défile) ou
`496×scale × 384×scale` (écran visible, posé à l'origine) — c'est la seconde
qui sert en pratique. Lanceur `Tester HD.cmd` à la racine du dossier de jeu.

**Étape 4 livrée le 2026-08-15, pas encore jugée à l'écran** (16/9) :
`TileGenWidth` / `-tilegen-width=<496..1024>`, 682 étant le 16/9 des 384 lignes.
**Le fait à ne pas re-déduire** : le matériel remplit 496 colonnes et pas une de
plus (pas de 512 dont 16 d'overscan, name table écrite sur 62 colonnes), donc
aucun réglage d'affichage ne peut montrer plus du plan de tuiles — contrairement
à la 3D, dont `-wide-screen` élargit vraiment le tronc de cône. Une première
tentative de **placement** (modes pillar/stretch/anchor, le dernier coupant le
plan en trois bandes ancrées aux bords) a été essayée puis **retirée** : Frédéric
l'a vue déchirer en trois la bannière de l'écran de round. Ce qu'il voulait est
l'inverse : agrandir la toile et **dessiner** des images de layer 16/9.
Donc surface allouée à `width × 384`, image du matériel centrée par une marge
égale, décalage ajouté une fois pour toutes dans `TileGenBuffer::GetLine` — le
rastériseur ignore l'élargissement, exactement comme il ignore `TileGenScale`.
Troisième taille acceptée pour un layer : `width×échelle × 384×échelle`
(2728×1536 à 682/4), qui est une **image d'écran et non une tuilemap** :
`HDLayer::wide`, ne défile pas, ne se replie pas, atteint les marges. Les marges
échappent au masque stencil (hors grille matériel) et sont posées par
`DrawHDLayerMargins` avant la boucle de spans. Outil : `fv2mod/layer_16_9.py`.
Lanceur `FV2 - 16-9.cmd`.

**Leçon d'outillage** : ne pas vérifier par capture d'écran du bureau. C'est déjà
peu fiable sur une fenêtre OpenGL, et `SetForegroundWindow` en boucle **vole le
focus pendant que Frédéric travaille** — une série de captures a attrapé son GIMP.
Vérifier par le journal, ou lui laisser le contrôle visuel.

Étape suivante : 4) motifs de cellules pour les éléments mobiles.
