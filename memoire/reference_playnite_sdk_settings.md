---
name: reference-playnite-sdk-settings
description: "Pièges du SDK Playnite pour une page de settings (namespace d'ObservableObject, XAML dans un csproj classique)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 633fc950-d752-4e5d-9a3f-2ee9fe13d331
  modified: 2026-08-21T12:34:44.738Z
---

Trois faits vérifiés par réflexion sur `Playnite.SDK.dll` 6.16 (`C:\Users\frede\AppData\Local\Playnite\Playnite.SDK.dll`), pour toute extension avec une page de paramètres :

- **`ObservableObject` est déclaré dans le namespace `System.Collections.Generic`**, pas `Playnite.SDK`. Sans `using System.Collections.Generic;` le type est introuvable, ce qui n'a aucun rapport apparent avec la cause.
- `RelayCommand` / `RelayCommand<T>` sont dans `Playnite.SDK` ; `Serialization.GetClone<T>()` (pour le clone de `BeginEdit`) est dans `Playnite.SDK.Data`.
- **`ISettings` hérite de `IEditableObject`** : `BeginEdit` / `CancelEdit` / `EndEdit` viennent de là, avec `VerifySettings(out List<string>)` en propre.
- Sans `Properties = new GenericPluginProperties { HasSettings = true }` dans le constructeur, l'extension n'apparaît pas dans Paramètres → Extensions et `GetSettingsView` n'est jamais appelée : la page existe mais reste inatteignable.

**Où l'utilisateur trouve la page** (vérifié dans `Localization\fr_FR.xaml` de Playnite) : menu principal → **Gestionnaire d'extensions** (`LOCMenuAddons`) → section **Paramètres des extensions** (`LOCExtensionsSettings`). **Pas** dans la fenêtre Paramètres — `LOCAddonsConfigMoveInfo` dit explicitement que les réglages d'extension ont été déplacés vers le gestionnaire. Je me suis trompé là-dessus une fois et Frédéric a cherché pour rien. Un `GetMainMenuItems` avec `MenuSection = "@CartridgeShelf"` et `Action = _ => OpenSettingsView()` évite le problème en ouvrant la page d'un clic.

**XAML dans un `.csproj` classique (non SDK-style)** : rien à importer à la main. `Microsoft.WinFX.targets` est importé automatiquement par `Microsoft.NetFramework.CurrentVersion.targets` dès que `TargetFrameworkVersion != v2.0`. Il suffit d'un `<Page Include="..." >` avec `<Generator>MSBuild:Compile</Generator>` et du `.xaml.cs` en `<Compile>` avec `<DependentUpon>`. Le BAML finit embarqué dans la DLL, donc rien de plus à déployer.

Attention aussi : **`--` est interdit dans un commentaire XML** — un commentaire de `.csproj` avec un tiret double casse le chargement du projet (MSB4025), pas la compilation.

Voir [[project-cartridgeshelf-settings]], [[reference-extension-yaml-types]], [[reference-playnite-extension-load-path]], [[feedback-verifier-le-build]].
