---
name: reference_vf5_console_2007
description: "Les VF5 console de 2007 (mode Quest) : l'ISO PS3 BLUS-30020 est chiffré sans sa clé de disque ; X360_VF5 (ver.C) a ses données en clair et un xex seulement chiffré AES."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-11T19:22:40.440Z
---

Dans `C:\Users\frede\Desktop\VF5 FS DECOMP` (mesuré le 2026-09-11) :

- **`Virtua Fighter 5 (USA) (EnJaFrDeEsIt).zip`** = PS3 `BLUS-30020`, base
  ver.B (films `VF5VERBADV`). Chiffrement de DISQUE : seuls les secteurs
  0-3743 (système de fichiers, PARAM.SFO) et la mise à jour PUP sont en
  clair ; `EBOOT.BIN`, `NPC_TBL.BIN`, les menus (`AET_N_QUE`…) sont chiffrés
  par la clé propre au disque, ABSENTE du zip (le README ne nomme que le site
  d'origine). Puis `EBOOT.BIN` est un SELF, second verrou (clés PS3
  publiques). Lecture possible en flux dans le zip (ISO9660 parcouru sans
  extraire).
- **`X360_VF5/`** = Xbox 360, base ver.C (film `vf5verCadv.sfd`) : `media/`
  déjà en clair (`npc_tbl.bin` 198 768 o, `rom/rob_ai`, menus, 5 854
  textes du mode Quest) ; `default.xex` chiffré AES (clé commerciale
  publique) mais compression 1 « basique », PAS le LZX du xex de FS X360.

**How to apply:** pour le mode Quest, partir de X360_VF5 ; la PS3 ne
s'ouvre qu'avec la clé de disque (.dkey Redump ou IRD) ou un dossier déjà
extrait. Voir [[reference_xbox360_outils]].
