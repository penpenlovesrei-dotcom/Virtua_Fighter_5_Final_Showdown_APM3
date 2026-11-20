---
name: reference_vf5_machine_etats
description: La machine à états de vfes.exe, et comment entrer en mode entraînement en la déviant.
metadata:
  type: reference
---

`SetState` = **`0x1800DA800`** dans le build APM3 : `SetState(ecx = état de tête,
edx = sous-état)`. État de tête courant en `0x18070C4F0`, sous-état en `0x18070C50C`.

**Deux** tables de noms, et non une : `0x1803A0C80` (11 états de tête, `STARTUP`…`MAX`) et
`0x1803A0CE0` (56 sous-états, `DATA_INITIALIZE`…`MAX`). Le découpage se prouve par le
sentinelle `0x37 = 55` que la fonction écrit, qui est le `MAX` de la seconde.

Le parcours réel, de l'écran-titre au combat, tient en **trois transitions** :
`APM3_ENTRY` → `APM3_SELECTOR` → `APM3_GAME_VS`.

**Le mode entraînement s'obtient par déviation.** `APM3_TRAINING` (sous-état 52) est le frère
de `APM3_GAME_VS` (50) : écrire 52 dans `rdx` au moment où le jeu demande 50 le fait entrer en
DOJO, en empruntant sa propre machinerie de transition. `tools/dojo.cmd`. Le partenaire y est
**inerte** — vérifié : son `ROB` ne change jamais, alors qu'en combat les deux bougent. C'est
la seule scène où une mesure d'entrée peut converger.

Voir [[reference_vf5_stub_entrees]] et [[reference_vf5_champs_rob]].
