---
name: feedback_verifier_le_build
description: "Ne jamais prendre le silence d'une sortie filtrée ou tronquée pour un succès — vérifier par le code de sortie."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c242bf71-58d0-4715-8a79-c53741fe7284
  modified: 2026-08-13T22:22:54.622Z
---

Sur 3SX, plusieurs tests ont été menés à l'aveugle par ma faute, chaque fois pour la même raison :
avoir traité une sortie réduite comme une preuve.

- `cmake --build ... | grep -Ei 'error'` ne sortant rien : j'en ai conclu au succès. Le build avait
  échoué, `cmake --install` a réinstallé l'ancien exe, et l'utilisateur a testé trois fois le même
  binaire en cherchant des changements absents.
- Puis `... | tail -3 && echo BUILD_OK` : `BUILD_OK` s'est affiché sur un build en échec, le code de
  sortie testé étant celui de `tail`.
- `Select-Object -First 4` sur un script de conversion : PowerShell tue la commande en amont, quatre
  images converties sur vingt, et un état bâtard testé en jeu.
- Durée d'un processus déduite de l'horodatage de son log : le jeu ne journalise qu'au démarrage,
  j'ai annoncé 4 secondes et « personne ne l'a piloté » pour un run de 48 secondes entièrement joué.

**Why:** une sortie vide, tronquée ou indirecte est indistinguable d'un succès, et les étapes
suivantes réussissent quand même sur des données périmées. L'erreur ne se voit alors qu'à l'écran,
plusieurs allers-retours plus tard.

**How to apply:** rediriger vers un fichier et lire le `$?` de la commande elle-même
(`cmake --build build > /tmp/b.log 2>&1; b=$?`), vérifier l'horodatage du binaire installé avant de
lancer, ne jamais tronquer la sortie d'une commande **qui agit** — seulement celle qui raconte. Et
mesurer ce qu'on prétend mesurer : la fin d'un processus, pas la dernière ligne qu'il a écrite.

Voir [[project_3sx_hd_assets]].
