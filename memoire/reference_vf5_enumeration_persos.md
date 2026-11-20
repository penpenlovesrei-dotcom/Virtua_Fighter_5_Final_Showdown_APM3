---
name: reference_vf5_enumeration_persos
description: "VF5 APM3 — l'énumération interne compte 21 personnages, bornée par `cmp ecx,0x15` ; 19 = TE2 vide, 20 = DUR."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 78a0dc37-8c59-4472-b901-32e3675904e8
  modified: 2026-09-03T00:34:05.506Z
---

Dans `vf5fs-pxd-w64-Retail_APM3.dll`, l'accesseur `0x18012CA90` traduit un indice
de personnage en données. Il borne son argument par **`cmp ecx, 0x15`** — donc
**0 à 20 sont valides** — et indexe une table de 21 entrées de 48 octets à
`0x1803E79E0` :

- 0 à 18 : les 19 combattants de la grille (AKI … TAK) ;
- **19 = `TE2`**, entrée d'essai vide ;
- **20 = `DUR` / `DURAL`**.

Deux accesseurs jumeaux (`0x18012CAB0`, `0x18012CAE0` pour le nom localisé,
identifiant `indice + 0x110`) portent la même borne.

Conséquence : **le moteur n'exclut pas Dural**, il est seulement absent de la
grille de sélection. Et le trou en 19 explique l'écart entre les 19 slots
affichés et l'indice 20 de `rob_cmn_mottbl` — ce n'est pas un décalage, c'est
une entrée morte.

`ROB+0x10` porte cet indice ([[reference_vf5_champs_rob]]) et c'est lui que le
chargeur lit pour bâtir `mot_%s.bin` (`0x180151F5E` joueur 1, `0x18015209B`
joueur 2). Détail complet dans `analysis/dural.md` ; état d'avancement dans
[[reference_reprise_vf5]].
