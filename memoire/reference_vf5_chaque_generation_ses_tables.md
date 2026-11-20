---
name: reference_vf5_chaque_generation_ses_tables
description: "Chaque génération de VF5 a SES tâches, murs, animations et dossiers d'effet ; depuis le 2026-09-11 tout est relu dans son binaire (generation.py), les 7 tâches manquantes servies par stubs."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-11T13:07:53.443Z
---

ver.B (ELF `extracted/LIND_VF5/id/disk0/vf5`) et VF5 R
(`extracted/LIND_R/id/disk0/vf5`) portent la même table que FS `0x18034D570`
(0x60 par décor : `+0x00` objsets en plus, `+0x20` tâches). R et ver.B ont 19
tâches (pas de MOVE : traduire PAR NOM). La table de R dit `hai` = WALL seul,
sans THUNDER — ce que Frédéric avait vu sur hi5 ([[feedback_registre_pas_regle]]).

**Depuis le 2026-09-11, RIEN ne vient de FS pour les entrées 42-81** (demande
explicite de Frédéric) : `tools/generation.py` est la source unique (tâches,
murs, animations, descripteur, DOWN, dossiers de TOUTES les tâches), chaque
emplacement vérifié par l'instruction qui le nomme ; `patch_moteur.Traducteur`
rend uid (par nom), textures, objets et objset à nos numéros. Journal (65),
`analysis/decors.md` §22.

Les sept tâches que FS lit en dur (LEAF, YUKA, RAIN, RINGOUT_SPLASH, SNOW_RING,
WET_CLOTH, FOG_RING) sont servies par des stubs de la greffe qui, pour un décor
de FS, relisent l'ORIGINAL (relu dans `.origine`). Ordre prouvé dans le code :
setStage (créneau 7) AVANT l'init. Les `.bss` des générations se rejouent avec
`tools/emu32.py`. Projets Ghidra `ghidra/vf5r_lind`, `ghidra/vf5verb_lind`.

**How to apply:** une donnée de décor spécial se lit dans SA génération et se
traduit ; ce qui ne se traduit pas se RETIRE. Un champ que FS a ajouté et que la
génération n'a pas (RINGOUT +0x18/+0x1C) se neutralise d'après le code de la
génération, pas au jugé. Contrôles : `controle_decors_vf5.py` / `_5r.py`
relisent en suivant le code. Rien de la troisième passe n'est vu à l'écran.
Voir [[reference_vf5r_binaire_lisible]], [[reference_vf5_taches_effet]],
[[reference_vf5_greffe_disposition]].
