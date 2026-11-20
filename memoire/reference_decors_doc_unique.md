---
name: reference-decors-doc-unique
description: Le document qui fait foi pour le chantier des décors est dc-decors/DECORS.md ; les autres sont des journaux.
metadata: 
  node_type: memory
  type: reference
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-03T08:07:19.991Z
---

Pour le chantier des décors 2I/NG vers 3SX, le fichier qui fait foi est
`C:\Users\frede\Downloads\3sx-outils\dc-decors\DECORS.md` (écrit le 02/09/2026), avec
`DONNEES-2I.json` pour les données machine.

`REPRISE.md`, `BILAN.md`, `SANS-ETAT.md` et `NEW-GENERATION.md` restent des **journaux de
session** : chronologiques, avec des corrections empilées sur des affirmations dépassées —
`SANS-ETAT.md` contient même une section marquée FAUX à lire comme un raisonnement raté.

**Pourquoi :** Frédéric a demandé un document unique parce que l'information était
dispersée sur onze fichiers qui se recoupaient et se contredisaient. Le but final est
d'automatiser l'extraction complète sans aucune action de l'utilisateur, et `DECORS.md`
est organisé autour de ça — il porte une liste explicite de ce qui demande encore une main
humaine.

**Comment l'appliquer :** lire `DECORS.md` en premier ; n'ouvrir les journaux que pour le
détail d'un désassemblage ou pour vérifier qu'une piste a déjà été fermée. Y reporter tout
nouvel acquis au lieu de l'ajouter à un journal. Voir [[reference-reprise-chantier]].
