---
name: project-digital-library-tile
description: Plugin DigitalShelf — 3e jaquette basculant vers les bibliothèques numériques ; en place et fonctionnel depuis le 2026-08-02
metadata: 
  node_type: memory
  type: project
  originSessionId: 3ec89142-c1a6-4182-bf26-f5b6db650905
  modified: 2026-08-02T11:51:26.039Z
---

Plugin **DigitalShelf** dans `C:\Users\frede\AppData\Local\Playnite\Extensions\DigitalShelf` (`LibraryPlugin`, Id `f7ba5ce6-190b-47ed-ba0c-59928375d2a1`). Il ajoute une jaquette qui bascule entre une vue « console » (jaquettes cartouche + CD) et une vue « bibliothèques numériques » (Steam, Epic, GOG…), via deux préréglages de filtre que le plugin crée lui-même.

Ordre des jaquettes, imposé par `SortingName` : `!!` DigitalShelf (gauche), `!0` DiscShelf (milieu), `!1` CartridgeShelf (droite). **La tuile est en première position volontairement** : Playnite sélectionne le premier élément après un changement de filtre, et c'est le seul moyen fiable pour qu'elle soit sélectionnée au retour de la vue Steam.

Compilation : `msbuild <plugin>.csproj /t:Rebuild /p:Configuration=Debug` avec le MSBuild de Visual Studio 18 Community. `OutputPath = .\` : le DLL atterrit directement là où Playnite l'attend.

**Pièges rencontrés, à ne pas réessayer :**

- `IMainViewAPI.SelectGame` ne déplace **pas** le focus visible du mode Fullscreen (il ne change que la sélection logique ; `SelectedGames` confirme pourtant le succès). Aucune API du SDK ne permet de déplacer ce focus.
- `InvokeOnStarted()` sur un `PlayController` déclenche la minimisation automatique de Playnite (`MinimizeAfterGameStartup`), d'où un aller-retour par le bureau Windows. N'invoquer que `InvokeOnStopped`.
- Un thème Fullscreen ne peut ni animer l'opacité des jaquettes (Playnite la pilote lui-même quand `AsyncImageLoading` est actif), ni produire de pixelisation (pas de code-behind ni de shader). D'où la fenêtre superposée du plugin pour l'effet mosaïque.
- Ne jamais poser `ScrollViewer.CanContentScroll="False"` ni surcharger `ItemsPanel` sur `PART_ListGameItems` : le panneau natif `FullscreenTilePanel` est alors mesuré en largeur infinie et Playnite plante au démarrage.
- Ne pas lier la hauteur d'une image à l'`ActualHeight` de sa case parente dans `ListGameItemTemplate.xaml` : dépendance circulaire, les jaquettes s'effondrent à une hauteur nulle.

Voir [[reference-extension-yaml-types]].
