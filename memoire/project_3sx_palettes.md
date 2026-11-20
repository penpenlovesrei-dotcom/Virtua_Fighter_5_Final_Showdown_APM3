---
name: project_3sx_palettes
description: "Chargeur de palettes externes pour 3SX — fait et validé ; le ciel du décor d'Ibuki reste non résolu."
metadata: 
  node_type: memory
  type: project
  originSessionId: ea9a2a5c-7768-4878-b431-cd3fe872568a
  modified: 2026-08-07T21:03:40.579Z
---

**Deux briefings font autorité, les lire d'abord** :
`C:\Users\frede\Downloads\3sx-palettes-briefing.md` pour le chargeur, et
`3sx-coloredit-briefing.md` pour l'éditeur de couleurs, les pièges du rendu et les sources de
palettes — ce second est plus récent et corrige le premier sur plusieurs points. Outils préservés dans
`C:\Users\frede\Downloads\3sx-outils\palettes\` et `\mame\`.

Module `src/port/video/pal_remix.c/.h` dans `C:\Temp3sx`, calqué sur `bgm_remix`. Un jeu de
couleurs est un dossier sous `%APPDATA%\CrowdedStreet\3SX\resources\pal_remix\`, avec `char-NN.pal`
et `stage-NN.pal` en numérotation moteur. Un `.pal` est l'entrée AFS **copiée octet pour octet**.

**Livré et validé en jeu au 2026-08-06** : 24 personnages (`new-generation` 11, `2nd-impact` 13)
capturés sous MAME depuis les ROM d'arcade, et 19 décors `rethird` convertis depuis les exports
`.act` du mod re:THIRD.

**Trois conversions à ne pas confondre** — console ARGB1555 petit-boutiste rouge en haut, arcade
CPS3 **xBGR555 gros-boutiste bleu en haut** (donc inverser R et B en plus du boutisme), et `.act`
en RGB 8 bits étendu par `(v<<3)|(v>>2)`.

**COLOR EDIT MODE, commencé le 2026-08-07.** Options → Display → `COLOR EDIT` (huitième ligne
ajoutée, `ARTWORKS` conservée) → liste des 20 personnages → éditeur. Module
`src/sf33rd/Source/Game/menu/col_edit.c/.h`, écrans dans `menu.c`.

**Fait et validé en jeu :** l'aperçu vivant — un vrai combattant dessiné dans un menu, avec la
palette que `pal_remix` lui donne ; poses vérifiées à l'œil pour les 20 ; grille des 64 couleurs ;
barres R/G/B avec valeurs 0-31 ; **l'édition fonctionne** — modifier un canal se voit sur le
combattant à la frame suivante. Mise en page arrêtée le 2026-08-07.

**Reste :** garder la palette d'origine (elle sert au panneau noir de droite, encore vide, et au
DEFAULT COLOR), puis les lignes de menu et le SAVE vers un jeu `edited`. Rien n'est persistant pour
l'instant : quitter l'écran perd les modifications.

Les pièges traversés sont commentés dans `col_edit.c` — **les relire avant de toucher au dessin**,
ils sont tous du genre à échouer en silence.

**Combien de coloris par jeu** : New Generation 6 (mais Yun et Yang 3 chacun, ils partagent une
case), 2nd Impact **7** — le septième sur **HP+LK**, que la chaîne MAME n'avait jamais tapé, d'où
des fichiers arrêtés à six. **Corrigé le 2026-08-07 pour les 14** via
`palettes/complete_2i_seventh.py`, qui prend le 7e sprite du site et **vérifie les six autres
contre les captures MAME avant d'écrire**. Le mappage vient des légendes de la page, pas des noms
de fichiers : leur numérotation n'est pas dans l'ordre des boutons.

**Les sprites de Capcom Colors sont une source de palette exacte, pas seulement une référence**
(trouvé le 2026-08-07). Leurs GIF sont indexés : la table de couleurs **est** la palette du jeu,
dans l'ordre du jeu, en 8 bits par `round(v*255/31)` — donc `round(c*31/255)` retrouve les cinq
bits sans perte. Validé contre la vérité terrain : Hugo et Urien reconstruits depuis les GIF
reproduisent **exactement** leurs fichiers capturés sous MAME. Outil :
`3sx-outils/palettes/capcomcolors_to_pal.py`. **Piège** : certains GIF ont été ré-optimisés, ce qui
reconstruit la table — les couleurs restent bonnes, l'ordre est perdu. Signature : l'accord
index par index s'effondre alors que l'accord d'ensemble reste haut ; l'outil teste et refuse.
**Un ordre perdu se reconstitue** via `recover_pal_order.py` : les coloris d'un personnage sont la
même image recolorée, donc les pixels d'un sprite intact donnent l'index de palette et ceux du
sprite abîmé donnent la couleur. Aucune ressemblance devinée. Le décodeur LZW du GIF y est écrit.

**Akuma 2nd Impact est fait et complet** : coloris 2-6 depuis les GIF, et le 1 laissé sur celui de
3rd Strike parce qu'il **est le même** — prouvé par cette méthode, 49 des 50 index utilisés
identiques, le seul écart étant l'emplacement transparent qui n'est jamais dessiné. **Gill est fait** (2026-08-07), New Generation et 2nd Impact. Il n'a que **deux coloris**, et deux
banques. Le déblocage vient du fichier de triche Pugsy (`cheat.7z` dans `C:\mame`, XML extractible
au 7-Zip) : forcer les deux camps sur Gill donne un **miroir**, donc ses quatre palettes de corps
dans un seul dump — slots 0 et 8 pour le coloris 1, 16 et 24 pour le 2. Scripts
`3sx-outils/mame/gill_pick{,_2i}.lua`, montage `palettes/build_gill.py`. Adresses : NG
`2012E2F/2012C7D` et `2012E31/2012C7F` (00 puis 14) ; 2I `20142C1`/`20142C3` = 1A.
**Son coloris 1 est celui de 3rd Strike au bit près** (63/63), le 2 non (18/63) — et les fichiers
New Generation et 2nd Impact sont **identiques** : un seul jeu de couleurs pour les deux premiers
épisodes. Ni l'astuce du mode démo ni le coup unique n'ont servi.

**Problème ouvert : le ciel du décor d'Ibuki.** Le chargeur fonctionne — un fichier magenta rend
tout le décor magenta **sauf le ciel** — donc ce ciel est peint hors du bloc `ColorRAM[300]`. Sont
écartés : les couches de fond (toutes en `bgPalCodeOffset = 0x12C`), les palettes de groupe de
texture (`texgroup.c` n'en a pas), le système de transition de couleurs, et **la voie ROM** — les
patches `.ups` de re:THIRD ne changent que l'écran de sélection et l'interface, prouvé par 62
captures de palette RAM identiques entre ROM d'origine et ROM patchée. Piste suivante : instrumenter
`ppgWriteQuadUseTrans`/`bgDrawOneChip` pour journaliser l'index de palette réellement lu.

**Toujours lancer le jeu en fenêtré**, voir [[feedback_lancer_3sx_fenetre]].
Voir aussi [[project_3sx_bgm_remix]] et [[project_3sx_audio_formats]].
