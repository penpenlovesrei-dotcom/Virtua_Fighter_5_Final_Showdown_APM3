---
name: reference-supermodel-memoire
description: "Comment lire la RAM Model 3 de Supermodel — format save state, pointeur statique, entrée ArtMoney."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 79a4eca3-6fc5-4e04-8400-5b9ce2442882
  modified: 2026-08-12T16:17:46.626Z
---

**Réglage `InputSystem` sur cette machine : `xinput`.** Les trois valeurs ont été essayées : `rawinput` (celle d'origine) confisque clavier et souris au niveau système via `RIDEV_NOLEGACY`, Alt+Tab compris — on se retrouve enfermé dans la fenêtre ; `dinput` libère le clavier mais **ne voit pas la manette** ; `xinput` fait les deux. La manette est **JOY1**, alors que la config d'origine mettait JOY2 sur le joueur 1 — d'où le fait que Frédéric se retrouvait joueur 2. Sauvegardes de l'ini en `Supermodel.ini.bak` et `.bak2`.

Deux accès à la RAM principale Model 3 (8 Mo) sous Supermodel. Dans les deux cas elle est stockée **mots 32 bits inversés** : il faut un byte-swap 32 pour relire du PowerPC big-endian.

**Save state** (`.st0`). Format CBlockFile : par bloc, trois `uint32` little-endian — `nextBlockOffset`, `nameLength`, `commentLength` — puis le nom, le commentaire, puis les données jusqu'à `nextBlockOffset`. Le bloc utile est `"Model 3"`, et **la RAM commence à l'offset `0x10` du bloc**, pas à 0 (16 octets d'état divers avant). Avec ce décalage, offset fichier == adresse PPC.

**Process en cours**. Le build `0.3a-20251120-git-3e94dd0` x64 (md5 `f2dfe94e9038c1dc51d6a7530db83e3d`, installé dans `Documents\SEGA Model 3`) garde un pointeur statique vers la base RAM en **`Supermodel.exe+0x65D098`** (.bss). Une seule déréférence, stable d'un lancement à l'autre. Attention au piège : la région `VirtualQueryEx` commence 0x40 octets *avant* la base réelle — c'est l'en-tête de bloc heap Windows, pas des données.

**Piège si on s'attache au démarrage** : Supermodel **réalloue son pool mémoire après le chargement des ROM**. Un outil qui lit le pointeur une seule fois juste après le lancement obtient une base périmée et écrit ensuite dans le vide, sans la moindre erreur — `WriteProcessMemory` renvoie succès. Il faut **relire le pointeur à chaque passe** de la boucle. Symptôme : lectures correctes, écritures sans effet. Deuxième piège du même ordre : juste après `CreateProcess`, `EnumProcessModulesEx` réussit mais la liste est vide et `mods[0]` vaut NULL, que ctypes rend en `None` — tester le module, pas seulement le handle.

Ce pointeur donne l'entrée à ajouter dans `C:\Games\ArtMoney\am820.emul`, section `*Sega Model 3` (déjà fait, sauvegarde en `am820.emul.bak`) :
```
Supermodel 0.3a-20251120 x64;Supermodel.exe;N;f2dfe94e9038c1dc51d6a7530db83e3d
;RAM 8MB;0;Supermodel.exe+P0065D098;800000
```
Conséquence du word-swap dans ArtMoney : une valeur **4 octets** se lit correctement en little-endian à l'adresse PPC telle quelle, mais un octet isolé à l'adresse PPC `A` s'affiche à **`A xor 3`** (et un mot de 16 bits à `A xor 2`).

**Piloter le jeu au clavier depuis un script** (indispensable pour mesurer une
valeur qui n'existe qu'en combat) : `SendInput` avec `KEYEVENTF_SCANCODE`
fonctionne, y compris avec `InputSystem = dinput`. Envoyer des **scancodes**,
pas des codes virtuels : Supermodel raisonne en positions physiques. Scancodes
utiles — `1` = `0x02` (Start), `3` = `0x04` (crédit), `A` = `0x1E` (Punch,
touche Q en AZERTY). Séquence qui amène à un combat : focus fenêtre, crédit ×3,
Start, puis Punch répété pour valider le perso. Compter ~18 s de boot.
Fermer par `WM_CLOSE` posté à la fenêtre, **jamais** par `terminate()` : la
NVRAM n'est écrite qu'à la sortie propre.

Utilisé par [[project_fv2_mod]] et [[project_fv2_vie_infinie]].
