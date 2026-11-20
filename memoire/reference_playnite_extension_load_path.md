---
name: reference-playnite-extension-load-path
description: "Playnite charge les extensions depuis Roaming\\Playnite\\Extensions\\<Id>, pas depuis le dossier de compilation — désynchronisation silencieuse"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3ec89142-c1a6-4182-bf26-f5b6db650905
  modified: 2026-08-03T21:31:28.545Z
---

Emplacements en jeu :

- **sources** : le dépôt `Documents\GitHub\Playnite-physical-cartridge-disc\<Nom>\`, où MSBuild écrit aussi la DLL (`OutputPath = .\`) ;
- **dossier réellement chargé** : `%AppData%\Playnite\Extensions\<Id-du-plugin>\`, nommé d'après le `Id` de `extension.yaml` ;
- **dossier programme** : `%LocalAppData%\Playnite\Extensions\<Nom>\` — Playnite **le scanne aussi**, puis déduplique par `Id` et retient la copie Roaming. Un doublon y vit donc masqué, sans jamais s'exécuter, mais prêt à reprendre la main si le dossier Roaming disparaît.

Le 3 août 2026, cinq copies de chaque plugin coexistaient. Tout ce qui n'était ni le dépôt ni la copie Roaming a été archivé dans `%LocalAppData%\PlayniteDoublons_20260803_232541` : les trois dossiers du dossier programme, et `C:\Dev` (vérifié sans contenu unique). **Il ne doit rester que deux copies : le dépôt, source, et Roaming, exécution.**

`C:\Dev` était l'ancêtre de la cascade : le projet y vivait, chargé via le réglage « extension de développement » de `config.json` (`DevelExtenions`, avec la faute de frappe de Playnite), qui se réinitialise seul à chaque fermeture. Si un doublon réapparaît un jour, vérifier ce champ en premier.

**Playnite charge la copie Roaming**, et **aucune erreur ne signale** qu'elle est périmée : le plugin se charge, journalise normalement, mais exécute du vieux code.

Corollaire moins évident, qui a coûté une soirée : la cible de copie ne recopiait que l'assembly. Tout fichier omis reste figé à sa version du jour de l'installation — `extension.yaml` annonçait encore `0.1` pendant que la DLL exécutée était celle de `0.2`. **Redéployer l'extension entière**, en excluant l'état de l'utilisateur (clés d'API, `mosaic_enabled.txt`, `UserLibrary.csv`) qu'une compilation ne doit jamais rétablir.

**How to apply:** devant un comportement qui ignore une modification pourtant compilée, lire d'abord la version annoncée au démarrage dans `%AppData%\Playnite\playnite.log` :

```
ExtensionFactory:Loaded plugin: CartridgeShelf, version 0.1
```

Si elle ne correspond pas à `extension.yaml` du dépôt, le problème est un déploiement incomplet, pas le code. Comparer ensuite les dates — pas les tailles, deux DLL distantes de 19 h faisaient exactement 46 080 octets.

Ids : DiscShelf `7c3e2d1a-9f61-4c7d-8b4e-123456789abc`, CartridgeShelf `a1312fcb-7107-4168-95ba-181dd6069299`, DigitalShelf `f7ba5ce6-190b-47ed-ba0c-59928375d2a1`.

Piège annexe rencontré en cherchant une chaîne dans un DLL : décoder tout le fichier en UTF-16 depuis l'octet 0 désaligne une chaîne sur deux et produit de faux « absent ». Chercher sur les **octets** (`Encoding.Unicode.GetBytes(motif)`), ou mieux, extraire les `ldstr` du corps de la méthode par réflexion. Voir [[reference-extension-yaml-types]].
