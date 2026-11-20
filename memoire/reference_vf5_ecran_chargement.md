---
name: reference_vf5_ecran_chargement
description: "VF5 — l'écran d'avertissement épilepsie EST l'écran de chargement (DATA_INITIALIZE, douze phases) ; seul son texte peut partir."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7b8919f9-a3c9-4e11-a256-ad9c22b4c7e9
  modified: 2026-09-04T23:48:43.205Z
---

Dans VF5 FS, l'écran d'avertissement sur l'épilepsie au démarrage **est**
l'écran de chargement. Ce n'est pas le sous-état `WARNING` (fausse piste,
démentie à l'écran) mais le sous-état **`DATA_INITIALIZE`**.

Son objet est un singleton statique, `0x180677040`, vtable `0x18034CB90` posée
en `0x18000194A` :

    +0x10  0x18006B880   mise à jour : machine à DOUZE phases sur [obj+0x58]
    +0x20  0x18006C490   dessin : le texte 0x36C, à partir de la phase 4

Les douze phases chargent pour de vrai — `EFFEFFCMN`, `STGCMN`, `NAGE_VF4`,
`se_system.csb`, `se_tv_cmn.csb`, `se_terminal.csb`. **Sauter les phases
sauterait le chargement.** L'écran occupe le temps du chargement et en profite
pour afficher l'avertissement légal.

**Ce qui est vérifié à l'écran (2026-09-05)** : le texte seul peut être
retiré — douze octets à `0x18006C4B6`, un saut vers l'épilogue `0x18006C803`
(le prologue doit être conservé, l'épilogue restaure `rbx`, `xmm6` et 0x110
octets de pile). Il reste alors un **écran blanc** : la scène AET
`DATA_INITIALIZE`, démarrée en `0x18006C9E2`. Retirer ce fond a été essayé puis
**annulé** — rien n'établit encore ce que cet écran doit devenir.

Option `--sans-epilepsie` (texte seul), hors des lanceurs. Détail :
`analysis/menu_console.md` §18. Voir [[project_vf5_mode_console]].
