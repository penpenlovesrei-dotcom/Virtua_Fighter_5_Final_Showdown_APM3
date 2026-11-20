---
name: project_3sx_hd_assets
description: Artworks/HUD/menus en HD dans 3SX — canvas HD et remplacement de textures faits ; reste à identifier les pages des illustrations.
metadata: 
  node_type: memory
  type: project
  originSessionId: 9cc79d80-789f-47b4-8447-3c5379a79bac
  modified: 2026-08-13T20:24:19.122Z
---

**Briefing complet et à jour** : `C:\Users\frede\Downloads\3sx-hd-briefing.md`. Le lire d'abord, il
fait autorité sur cette note.

Objectif de l'utilisateur (2026-08-07) : passer **artworks, textes de menus et HUD** en HD dans 3SX,
en gardant les persos et décors d'origine. Assets sources : les 22 illustrations Online Edition en
DDS dans `C:\Users\frede\Downloads\SF3.3 music\Assets HD` (19 combattants + Gill + la voiture et le
ballon du bonus stage ; DXT5 sauf 6 en DXT1 à alpha 1 bit, donc bords crénelés pour ceux-là).

**Fait et validé en jeu au 2026-08-07** (dans `C:\Temp3sx`, non commité) :
- `port/video/canvas.c` + option `render-scale` (1-8) : le canvas passe à N×384×224. Toute la
  géométrie arrive déjà en NDC, donc rien d'autre à toucher ; seul le blit final passe en linéaire
  au-delà de 1×. Les deux backends (SDL_GPU **et** OpenGL) sont couverts.
- `port/video/tex_remix.c` : remplacement de page de texture **par empreinte du contenu**
  (FNV-1a sur la page décompressée, crochet dans `ppgSetupTexChunk_3rd`), conteneur `.tex`
  (`3STX` + w + h + RGBA), mode `tex-remix-dump` qui écrit chaque page en PGM + manifeste,
  outil `tools/make_tex.py`. Docs dans `docs/tex_remix.md`.
- **Le pool de textures est le pool console de 10 Mo** (`system_memory_size`, foundaps2.c) : une
  seule page 1024×1024 RGBA = 4 Mo le vide et provoque `fatal_error`. Résolu en agrandissant le pool
  au démarrage de la taille des `.tex` installés (`TexRemix_ReservedBytes`).

**Point clé pour la suite** : l'illustration de l'écran de sélection n'est **pas une texture unique**.
Elle est assemblée en chips 16×16 depuis des pages de 256×256, via `_sel_pl_char_table` et
`seqsStoreChip` (mtrans.c). Les UV sont normalisées (`u/256.0f`), donc une page N× marche telle
quelle ; mais poser une illustration OE dessus demande de la **redécouper sur la grille de chips
d'origine**, pas juste de la redimensionner.

**Les PGM du dump se regardent directement** (2026-08-07) : l'agent peut lire les images, donc un
planche-contact des 102 pages suffit à voir ce que chacune contient — la boucle « couleur unie →
l'utilisateur décrit l'écran » prévue dans le briefing n'est pas nécessaire pour trier les pages.
Il faut juste étirer le contraste, les valeurs étant des index de palette et non des luminances.
Recensement du dump conservé dans `%APPDATA%\CrowdedStreet\3SX\resources\tex_remix\dump\` : pages
0-9 textes/HUD/logo, 10-35 les croquis au crayon de l'opening, **36-42 les illustrations
cel-shadées** (celles qui ont un équivalent HD), 43-85 le lettrage géant `3rd STRIKE`, 86-101 les
ciels du titre.

**Numérotation des pages faite et validée (2026-08-13)** : `TexPageOrigin { index, first, entry }`
passé à `TexRemix_Substitute`, manifeste enrichi en `page N list N entry N`. Les numéros
reproduisent exactement l'arithmétique des sources — liste 0 = `ppgScrTex` (sc_sub.c), 590-591 =
`ppgWarTex`, 600 = demo00, 601 = titre, **602-691 = `ppgOpnBgTex` (opening.c, 90 pages)**, 148-163
en liste 132 = bg.c. Compilé, installé.

**Les 102 pages dumpées sont l'opening, pas les menus** : croquis, illustrations cel-shadées et
lettrage `3rd STRIKE` vivent tous dans `ppgOpnBgTex`. Aucune page de l'écran de sélection n'y est.
Le briefing se trompe en les décrivant comme « démarrage + les menus ». Dump conservé avec ses
numéros dans `…\tex_remix\dump-opening\`.

**TRANCHÉ (2026-08-13) : le crochet de tex_remix ne peut pas atteindre les sprites en chips.**
Établi deux fois, indépendamment.

- *Mesure* : un balayage complet des 20 personnages sur l'écran de sélection n'a produit
  **aucune page nouvelle** dans le manifeste.
- *Code* : `make_texcash_work` (texcash.c:239) → `mlt_obj_trans_init` (mtrans.c:2034) →
  **`ppgSetupTexChunkSeqs`**, avec un en-tête PPG synthétique de **16×16** : le cache de
  multitextures crée des chips vides puis y fond les sprites à la demande, et
  `ppgRenewTexChunkSeqs` (PPGFile.c:891) les rafraîchit par `flLockTexture` + `memmove` brut.
  `seqsStoreChip` les adresse par `gix + (code >> 8)` où `gix = mts_base[ix].gix`.
  **`ppgSetupTexChunk_3rd` n'est jamais appelé sur ce chemin**, donc `TexRemix_Substitute` non plus.

Conséquence : tex_remix atteint ce qui est chargé en bloc — opening, titre, menus/HUD, décors — et
**jamais** l'illustration de l'écran de sélection ni les persos.

**Contournement écrit et qui tourne (2026-08-13)** : `port/video/art_remix.c/.h`, le pendant de
tex_remix pour ce qu'il ne peut pas atteindre. Un `.tex` par personnage dans
`<resources>/art_remix/`, nommé `face-NN.tex` par **numérotation moteur de `constants.h`** (déduit
du log : les faces observées vont de 1 à 19, jamais 0, et Gill est le seul non sélectionnable).
`ArtRemix_TexCode(face)` crée une vraie texture par `flCreateTextureHandle`, cache de 4 avec
éviction LRU. Outil `tools/make_art.py` (DDS → `.tex`, taille libre, l'image est étirée sur la
boîte). `Draw_Portrait_Art` dans aboutspr.c dessine un quad texturé sur la boîte de
`mlt_obj_bounds`, sur le modèle de `dispSaveLoadTitle` ; le work garde position, miroir, fondu et
tri. `ArtRemix_ReservedBytes` s'ajoute à celle de tex_remix dans foundaps2.c.

Deux pièges payés cash :
- **La réserve du pool se compte en textures résidentes, pas en fichiers installés** — plus gros
  fichier × places du cache. Compter la somme des fichiers donne `fatal_error:
  flPS2GetSystemMemoryHandle` dès la troisième face.
- **Rouge et bleu sont échangés** à l'arrivée dans le pool, malgré un téléversement annoncé en
  `R8G8B8A8`. Peau lavande, main bleue. Corrigé par un échange d'octets dans `art_remix.c`.
  **`tex_remix` déclare le même `PixelFormat` et a donc probablement le même défaut**, jamais vu
  parce que ses essais portaient sur des aplats unis.
- **`render-scale` doit être mis à 4 dans la config**, sinon le canvas reste en 384×224 et toute
  l'image HD est réduite avant affichage — le mod paraît ne servir à rien.
- **`scale-mode` décide de l'étirement** : `nearest` (et donc le `soft-linear` inexistant qui y
  retombe) passe par `fit_4_by_3_rect`, soit un allongement vertical de **9/7 = 28,6 %** sur tout
  l'écran ; `square-pixels` n'étire rien. C'est la cause des « mauvaises proportions », pas le quad.
  Le 4:3 reste le format d'origine de la borne, donc c'est un choix, pas une correction.

**Les assets OE sont exactement 10/3 des sprites d'origine** (mesuré : boîte 312×208 contre image
1040×692 pour Chun-Li, et pareil sur sept autres). Donc `mlt_obj_bounds` calcule le bon rectangle et
il n'y a pas de recadrage à inventer. Exception : **Makoto (face 16)**, 812×692 pour une boîte de
264×208, soit 3,08 en largeur contre 3,33 en hauteur — son fichier OE est recadré autrement.

**Reste ouvert** : l'utilisateur trouve les teintes délavées. Écarté par la mesure — alpha de
l'appel à 255 (`clear_level` vaut 0), fusion `SRC_ALPHA/ONE_MINUS_SRC_ALPHA` standard dans les deux
backends, et `Renderer_DrawSprite`/`DrawSprite2` passent tous deux par le même `convert_color`.
L'hypothèse restante est que l'illustration OE est simplement plus douce que le portrait CPS3.

Python utilisable ici : `C:\Users\frede\AppData\Local\Python\pythoncore-3.14-64\python.exe`
(Pillow 12.1.1, lit les DDS). Le `python` du PATH est le stub Windows et ne sort rien.

**Où vit l'illustration de sélection** : `effect/eff38.c`, dont l'en-tête dit « Large character
portraits in character select ». `effect_38_init(PL_id, dir_old, Your_Char, Play_Status, Target_BG)`
pose `my_mts = 13`, `char_index = 2`, `char_table = _sel_pl_char_table`, `my_col_code = 0x90`,
`rl_flag = PL_id ^ 1` (P1 est le miroir de P2), `position_z` 75/77. Le motif est choisi par
`set_char_move_init2(&ewk->wu, 0, char_index, dir_step + 1, 0)` où **`dir_step` = l'id du perso**
(via `ID_of_Face[Cursor_Y][Cursor_X]`). Position = `EFF38_Base_XY[id][Play_Status]` +
`EFF38_Correct_Data[id][Play_Status][dir_step]` (sel_data.c, `[2][2][22][2]`, presque tout à zéro).
`mts_base[13]` = gix 1030, p16 1, p32 6, **mode 0x2012 donc streaming**, palette ghost CP3.

Curiosité d'origine à ne pas « corriger » à l'aveugle : `dir_step` peut valoir 22 ou 23 alors que
`EFF38_Correct_Data` n'a que 22 entrées (cas Gill et `My_char == 21`).

Voir [[project_3sx_bgm_remix]] (build et install) et [[project_3sx_palettes]].
