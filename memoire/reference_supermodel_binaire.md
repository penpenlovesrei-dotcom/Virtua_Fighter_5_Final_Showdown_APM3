---
name: reference-supermodel-binaire
description: "Le Supermodel à lancer est celui de bin64, et depuis le dossier de jeu — pas celui de la racine."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7d3168ca-275c-4d30-8e06-abc13121b915
  modified: 2026-08-12T18:08:15.265Z
---

Deux exécutables coexistent, et un seul connaît les options du projet :

- `SEGA Model 3\Supermodel.exe` — **ancien binaire**, ignore `-tilegen-scale`,
  `-input-log`, `-menu-eat-start`, `-midi-log` ;
- `SEGA Model 3\SupermodelSrc\bin64\supermodel.exe` — **celui qu'on compile**.

Supermodel cherche `Config\`, `ROMs\`, `NVRAM\` et `Assets\` **dans le dossier
courant**, pas à côté de son `.exe`. Lancé depuis `bin64\`, il n'en trouve aucun
et ouvre SuperSetup. D'où le `cd /d "%~dp0"` en tête de chaque lanceur —
voir [[feedback_lanceurs_cmd]].

Compilation, depuis un shell MSYS2 **MinGW64** :
`MSYSTEM=MINGW64 /c/msys64/usr/bin/bash.exe -lc "cd '…/SupermodelSrc' && ./build_dbg.sh"`

L'édition de liens échoue avec `Permission denied` si une instance du jeu tourne
encore : la fermer d'abord. Vérifier ensuite l'horodatage de
`NVRAM\fvipers2.nv`, c'est lui qui dit si la fermeture a été propre.
