---
name: reference-3sx-binaire
description: Quel 3sx.exe lancer — celui de build\application\bin, jamais celui de build\.
metadata:
  type: reference
---

Le dépôt 3SX produit **deux copies identiques** de `3sx.exe` :

- `build\3sx.exe` — sortie brute du compilateur, **ne démarre pas** : il lui manque
  `zlib1.dll`, `SDL3.dll`, `libiconv-2.dll` et le dossier `shaders\`. Windows affiche
  « Impossible d'exécuter le code, car zlib1.dll est introuvable ».
- `build\application\bin\3sx.exe` — la copie installée, avec ses DLL, ses shaders et
  ses assets à côté. **C'est celle-là qu'il faut lancer**, et c'est là que doivent
  vivre les lanceurs `.cmd`.

Même taille, même horodatage : rien ne les distingue à l'œil, seul le voisinage compte.
`build\install_manifest.txt` liste ce que la copie installée embarque.

**Why:** un aller-retour perdu le 27/08/2026 en pointant un lanceur sur `build\3sx.exe`.

**How to apply:** vérifier `zlib1.dll` à côté du binaire avant de livrer un lanceur.
Voir [[feedback-lanceurs-cmd]] et [[feedback-lancer-3sx-fenetre]].
