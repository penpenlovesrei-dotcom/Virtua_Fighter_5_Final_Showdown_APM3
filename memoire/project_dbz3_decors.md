---
name: project-dbz3-decors
description: "Échange des décors Butouden 3 ↔ Butouden 2 — démarré le 2026-08-03, bloqué sur la localisation du décompresseur."
metadata: 
  node_type: memory
  type: project
  originSessionId: 0e0f32dc-aa23-4cf3-b0a5-3c95b3aa9946
  modified: 2026-08-03T21:07:09.409Z
---

Projet démarré le 2026-08-03 : remplacer des décors de *DBZ Super Butouden 3* (SNES)
par ceux de *Super Butouden 2*. Distinct du projet MSU-1 ([[project-dbz3-msu1]]),
mêmes ROMs.

Tout le détail technique est dans
`C:\Users\frede\Documents\Super Famicom\Roms\Dragon Ball Z - Super Butouden 3 (J) [!]\decors-project\NOTES.md`
(carte des banques, outils, impasses documentées). Ne pas le redocumenter ici.

Ce qui n'est pas dans le repo :

- **État au 2026-08-03** : étape 1 sur 3 (localiser le décompresseur), **non terminée**.
  L'analyse statique a plafonné. L'utilisateur a choisi d'installer **Mesen2** pour
  tracer l'exécution ; la procédure est dans `decors-project/TRACE-MESEN.md`. En
  attente qu'il renvoie l'adresse du tampon WRAM `$7E`.
- Le plan convenu est en trois jalons avec point d'arrêt à chaque fois : (1) décompresseur
  + extraction des décors en PNG, (2) preuve de concept sur **un seul** décor testé dans
  l'émulateur, (3) généralisation seulement si (2) passe. Ne pas sauter de jalon.
- `decors-project/tools/trace_vram.lua` est **non testé** — écrit sans Mesen installé.
- **Leçon de méthode** : j'ai cherché le décompresseur en filtrant les blocs identiques
  BT2/BT3 par une « signature LZ » (présence de certains opcodes dans une fenêtre).
  Les 7 candidats étaient tous faux — six blocs de données, un de padding `$FF`. Des
  opcodes isolés ne distinguent pas code et données, et le décompresseur n'est de toute
  façon pas byte-identique entre les deux jeux (relogé). **Ne pas refaire cette passe.**
- Contrairement au driver sonore (2 % d'octets communs), le moteur *graphique* est
  largement partagé : `$08:8000` est identique à la même adresse dans les deux jeux.
  C'est ce qui rend le projet plausible — le codec est probablement commun.
