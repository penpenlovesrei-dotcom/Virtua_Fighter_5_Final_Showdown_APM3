---
name: reference_vf5_pxd_pierre_de_rosette
description: "Ultimate Showdown et R.E.V.O. embarquent le moteur VF5FS d'origine ; leur DLL x64 est la version lisible du même code."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3331ac98-19db-49de-a075-1d62462a23f2
  modified: 2026-09-01T04:51:01.298Z
---

`vf5fs-pxd-w64-Retail_APM3.dll` (Ultimate Showdown arcade) et
`vf5fs-pxd-w64-d3d12_SteamRetail.dll` (R.E.V.O. Steam) portent un bloc de version **identique** :

```
D:/Project/vf5/vf5fscs_source/20120711_update_1.1/vf5fs
2016-06-30T14:58:25+09:00   (portage)   atsu_takashi
2012-07-04T18:06:57+09:00   (snapshot source)
Virtua Fighter5 Final Showdown / 6.000 / VERSION A / REVISION 1
```

Ce n'est donc pas une réimplémentation : c'est **le moteur FS lui-même**, branche console
(`vf5fscs`), porté en x64 en 2016, release 6.000 — la même que le dump Lindbergh Rev B.

**Conséquence :** le DLL x64 est bien plus facile à décompiler que l'ELF32 de 2011, et c'est
le même code. Il sert de pierre de Rosette pour nommer les fonctions de l'ELF, sans attendre
PS3 ni X360.

Corollaire mesuré au SHA-256 : 20 `mothead_*.bin` sur 21 et 19 `ctrl_*.bin` sur 20 de
l'arcade 6.000 sont **identiques bit à bit** dans R.E.V.O. (2025). Seul Dural diffère, et sur
ce point R.E.V.O. suit la PS3, pas l'arcade. `rom_200/` est le rééquilibrage 2.00, livré à
côté des données d'origine.

Voir [[project_vf5_re]].
