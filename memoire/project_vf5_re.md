---
name: project_vf5_re
description: Rétro-ingénierie de Virtua Fighter 5 Final Showdown ; espace de travail et étiquettes de sources corrigées.
metadata: 
  node_type: memory
  type: project
  originSessionId: 3331ac98-19db-49de-a075-1d62462a23f2
  modified: 2026-09-01T04:50:48.854Z
---

Chantier ouvert le 2026-09-01. Espace de travail : `C:\Users\frede\Desktop\VF5RE\`
(dumps en lecture seule dans `Desktop\VF5 FS DECOMP\`, extractions dans `VF5RE\extracted\`).

**Deux dossiers de dump portent un nom trompeur :**

- `APM3_FS` n'est **pas** un dump APM3 : c'est du **Lindbergh, Rev B ver 6.0000**
  (release 6.000, build 2011-10-17, CRC32 loader `0x034C0D02`). ELF32 x86, `libsegaapi.so`,
  toolchain MontaVista.
- `LIND_FS` est la **Rev A** (release 2.000, build 2010-06-28, CRC32 `0xBAE2BE62`),
  sous forme de deux images ext3 dans un 7z.

On a donc bien deux révisions arcade distinctes, malgré l'absence des dossiers
`ARCADE_FS_REVA` / `REVB` annoncés.

Phase 0/1 terminée : voir `VF5RE\analysis\INITIAL_REPORT.md`, qui indexe tous les autres
livrables. L'entité combattante s'appelle `Rob` dans le moteur ; les données de coups sont
`rom/rob/mothead_<CHR>.bin`, les commandes `ctrl_<CHR>.bin`.

Voir [[reference_vf5_pxd_pierre_de_rosette]] et [[reference_python_stub_windows]].
