---
name: reference-extension-yaml-types
description: "Les valeurs Type d'un extension.yaml Playnite sont celles de l'enum ExtensionType, pas les noms de classes du SDK"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3ec89142-c1a6-4182-bf26-f5b6db650905
  modified: 2026-08-03T02:47:10.607Z
---

Dans `extension.yaml`, le champ `Type` attend une valeur de l'énumération `ExtensionType` de Playnite (dans `Playnite.dll`, **pas** dans `Playnite.SDK.dll`) : `GenericPlugin`, `GameLibrary`, `MetadataProvider`, `Script`.

Piège : pour un plugin de bibliothèque, la classe C# s'appelle `LibraryPlugin` mais la valeur YAML est **`GameLibrary`**. Écrire `Type: LibraryPlugin` fait échouer silencieusement le chargement — l'extension n'apparaît nulle part dans Playnite, et la seule trace est dans `%AppData%\Playnite\playnite.log` :

```
ERROR|ExtensionFactory:Failed to parse plugin description: ...\extension.yaml
YamlDotNet.Core.YamlException: ... La valeur demandée 'LibraryPlugin' est introuvable.
```

**How to apply:** quand une extension semble totalement ignorée par Playnite (aucune entrée dans `extensions.log`), chercher d'abord `Failed to parse plugin description` dans `playnite.log` — `extensions.log` ne contient que les journaux des plugins déjà chargés, donc il est vide dans ce cas. Voir [[project-digital-library-tile]].

Deuxième vocabulaire, à ne pas confondre : les manifestes soumis à `PlayniteAddonDatabase` n'acceptent que `Generic`, `GameLibrary`, `MetadataProvider`, `ThemeDesktop`, `ThemeFullscreen`. Donc **`Generic`** côté annuaire là où `extension.yaml` écrit `GenericPlugin`. Recopier la valeur d'`extension.yaml` fait rejeter la PR.

Avant toute soumission, valider avec `%LocalAppData%\Playnite\Toolbox.exe verify Addon <fichier>` : la commande vérifie aussi le manifeste d'installation distant, mais elle le lit via `raw.githubusercontent.com`, qui sert du cache pendant environ cinq minutes après un push. Voir [[reference-release-tag-scheme]].
