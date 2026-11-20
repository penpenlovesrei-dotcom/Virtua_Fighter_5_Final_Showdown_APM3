---
name: feedback_lancer_3sx_fenetre
description: "Lancer 3SX toujours en fenêtré, et avec musique et bruitages à -4."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ea9a2a5c-7768-4878-b431-cd3fe872568a
  modified: 2026-08-06T21:17:10.644Z
---

Deux consignes permanentes quand je lance 3SX pour un test.

**Toujours en fenêtré.** Demandé explicitement le 2026-08-06, après plusieurs lancements en plein
écran. Le réglage est `fullscreen = false` dans `%APPDATA%\CrowdedStreet\3SX\config`. Le vérifier
avant chaque lancement, il peut avoir été remis à `true`. La taille de fenêtre est réglée par
`window-width` / `window-height` dans le même fichier (640×480 actuellement).

**Musique et bruitages à -4.** Demandé le 2026-08-06 aussi.

**Pourquoi :** ces lancements servent à vérifier un changement et s'enchaînent souvent plusieurs
fois de suite. En fenêtré et à volume réduit, l'utilisateur garde la main sur le reste de sa
machine, et il peut faire une capture d'écran facilement — c'est le principal moyen qu'il a de me
montrer ce qu'il voit, puisque je ne vois jamais le rendu.

**Piège sur le volume :** il n'y a **pas** de clé de config pour le son. `bgm_level` et `se_level`
sont des globales de `src/sf33rd/Source/Game/sound/sound3rd.c`, initialisées à 15 (« Standard ») à
chaque démarrage, et la seule chose qui les change est l'écran Options → Sound. C'est le même quirk
d'origine que pour BgmType, décrit dans [[project_3sx_bgm_remix]] : les réglages son sauvegardés ne
sont appliqués qu'en ouvrant ce menu. Sur l'échelle du menu, **-4 vaut l'indice 11** (0 = Silence,
1 = -14, … 14 = -1, 15 = Standard). Donc pour honorer la consigne il faut agir sur ces valeurs
initiales, pas sur le fichier de config.

Voir [[project_3sx_bgm_remix]] et [[project_3sx_palettes]] pour les projets eux-mêmes.
