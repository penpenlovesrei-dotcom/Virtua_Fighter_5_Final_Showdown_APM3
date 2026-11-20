---
name: reference-release-tag-scheme
description: "Un tag de release regroupe plusieurs plugins, dont les versions diffèrent — le numéro du tag n'est pas celui du plugin."
metadata: 
  node_type: memory
  type: reference
  originSessionId: b6a2c382-c062-4077-bc27-75a9d70650ca
  modified: 2026-08-03T02:31:51.181Z
---

Dépôt `penpenlovesrei-dotcom/Playnite-physical-cartridge-disc` : un tag GitHub désigne un **lot de publication**, pas la version d'un plugin. Les trois plugins avancent à leur propre rythme et se retrouvent sous le tag du lot.

- `v0.1` — CartridgeShelf 0.1, DigitalShelf 0.1, **DiscShelf 0.2**
- `v0.2` — CartridgeShelf 0.2, DigitalShelf 0.2
- `v0.3` — DiscShelf 0.3
- `v0.4` — CartridgeShelf 0.3, DiscShelf 0.4
- `v0.5` — DigitalShelf 0.3

D'où des `PackageUrl` qui paraissent incohérents dans `manifests/*.yaml` (`download/v0.1/DiscShelf-v0.2.pext`) alors qu'ils sont corrects. Vérifier avant de « corriger » une URL.

Les `.pext` se construisent avec `_release\build-release.ps1`, qui lit la version dans `extension.yaml` de chaque dossier de staging — voir [[reference-playnite-extension-load-path]] pour la source des binaires empaquetés.

**Publié dans l'annuaire officiel.** La PR `JosefNemec/PlayniteAddonDatabase#619` a été fusionnée le 13 août 2026 : les trois plugins figurent désormais au catalogue Playnite. Deux rejets l'avaient précédée, tous deux dus au manifeste d'annuaire et non au code — un fichier commité vide, et `GenericPlugin` au lieu de `Generic`.

**Conséquence pour la suite : plus aucune PR à soumettre.** L'entrée d'annuaire pointe vers `InstallerManifestUrl`, que Playnite relit tout seul. Publier une nouvelle version se résume donc à trois gestes dans le dépôt personnel : incrémenter `extension.yaml` et `AssemblyInfo.cs`, ajouter l'entrée dans `manifests/<Nom>.yaml`, puis créer la release GitHub portant le `.pext`.

**Toujours créer la release avant de toucher au manifeste** : `Toolbox verify` teste l'accessibilité HTTP du `PackageUrl`, et un manifeste par ailleurs correct échoue tant que le paquet n'est pas en ligne.
