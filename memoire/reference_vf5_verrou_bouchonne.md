---
name: reference_vf5_verrou_bouchonne
description: "VF5 APM3 — le motif dominant du build : un chemin complet fermé par un dernier prédicat bouchonné ; patcher le site d'appel, jamais le corps."
metadata:
  node_type: memory
  type: reference
  originSessionId: 7b8919f9-a3c9-4e11-a256-ad9c22b4c7e9
  modified: 2026-09-04T18:39:43.135Z
---

Dans le build APM3 de VF5, le motif dominant n'est pas « la fonctionnalité a
été retirée » mais **« le chemin est complet et un dernier verrou le ferme »**.
Il s'est présenté quatre fois le 2026-09-04 :

| site d'appel | ce qu'il ferme |
|---|---|
| `0x18016E20B` | la case de Dural dans la grille (elle est dessinée, puis désactivée) |
| `0x18016DC69` / `0x18016E109` | les compositions `_dur` du dessin |
| `0x1801DE0ED` | l'entrée `DLC STORE` du menu |
| `0x1801B6E8E` | le retour au menu après un combat |

**Tous appellent le même corps**, `0x180007450` (`xor al,al ; ret`), qui a
**210 appelants** : c'est un repliement COMDAT entre plusieurs prédicats
distincts. Le corps n'a donc aucun sens ; c'est **le site d'appel** qui en a
un. Trois autres bouchons partagés existent : `0x180007430` (`ret 0`),
`0x180007440` (`xor eax`), `0x180029FB0` (`mov al,1` — celui-là rend VRAI).

**Comment faire :**

- remplacer le `call` par `mov al, 1` + trois `nop` (5 octets pour 5) ;
- **jamais** patcher le corps : on casserait les 209 autres ;
- et quand le prédicat a plusieurs appelants mais que la **branche** qui le
  consomme a une portée nulle, corriger la branche. Exemple : `0x1801B6E40` a
  quatre appelants, mais `0x1800DA9D0` (le milieu du mode GAME) ne tourne que
  sur notre parcours, puisque le mode 2 n'a aucun autre demandeur.

Corollaire de méthode : quand quelque chose « ne fait rien » dans ce build,
chercher d'abord un `call 0x1800074xx` sur le chemin, avant de supposer que le
code manque. Voir [[project_vf5_mode_console]] et [[project_vf5_dural]].
