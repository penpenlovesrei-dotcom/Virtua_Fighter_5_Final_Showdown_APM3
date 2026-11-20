---
name: reference_vf5_depot_public
description: "Le dépôt GitHub public du chantier VF5 et sa règle : clone VF5RE-public, seulement .md/.py/.cmd, jamais de C décompilé ni reseau_allnet.md (clé AES)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-11T19:13:21.600Z
---

`https://github.com/penpenlovesrei-dotcom/Virtua_Fighter_5_Final_Showdown_APM3`,
clone local `C:\Users\frede\Desktop\VF5RE-public` (VF5RE lui-même n'est PAS
un dépôt git). On y COPIE depuis VF5RE ; `gh` y est connecté.

Règle de ce qui entre (celle des premiers commits, tenue le 2026-09-11) :
`.md` d'analyse, `.py` et `.cmd` d'outils, le `.java` de Ghidra, les deux
journaux. Jamais : C décompilé (`analysis/*.c`), captures, données de jeu
(le `.gitignore` bloque déjà `.bin .farc .dll .png`…), ni
`reseau_allnet.md` qui porte la clé AES du réseau. Avant de copier : clôture
des imports des outils publiés, et balayage clés/hex longs/courriels.

Décors publiés le 2026-09-11 : branche `decors-vf5r-et-vf5`, PR #1 (non
fusionnée à la date). Les deux premiers commits allaient directement sur
`master`.

**How to apply:** « publie sur GitHub » = ce dépôt ; vérifier l'état de
PR #1 avant d'en ouvrir une autre. Voir [[reference_reprise_vf5]].
