---
name: reference_vf5_apm3_direct3d11
description: "Le moteur APM3 dessine en Direct3D 11 (couche GL->D3D11) : shaders DXBC dans w64/shader_pxd_w64.farc, pas l'ARB ; un point y fait 1 pixel sans geometry shader."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-11T18:42:37.762Z
---

Les `.fp/.vp` ARB des archives Lindbergh ne sont PAS ce que lit APM3 : le
moteur lit chaque shader par son nom (`0x1801767D0`) dans
`vf5fs_media/w64/shader_pxd_w64.farc`, du DXBC en conteneurs `GSVS` /
`GSPS` / `GSFX` (= VS + PS + `GSGS`). Désassembler : `D3DDisassemble` de
d3dcompiler_47 par ctypes (script `dxbc_dis` recopié dans
`tools/shader_empreintes.py`).

Piège payé le 2026-09-11 : les empreintes de SNOW_RING (ykb) sont des points
`glPointSize(6)` ; en D3D11 un point fait 1 pixel, et le portage n'a donné un
geometry shader qu'aux 5 programmes de points que FS utilise. Un code d'effet
que FS ne fait jamais tourner (SNOW_RING n'est dans aucun décor FS) peut
donc être muet à cause du PORTAGE, pas des données. `cb12[28]` = (2/L, −2/H)
du viewport courant (`0x18025E830`). Remède et format : REPRISE (67).

**How to apply:** un effet de décor ajouté qui « tourne » (espions, sonde)
mais ne se voit pas → regarder son shader DXBC et les états GL sans
équivalent D3D11 avant de soupçonner les données. Ne jamais modifier
l'archive de FS : poser à côté et rediriger par nom. Voir
[[reference_vf5_sonde_decor]], [[feedback_ne_pas_toucher_decors_fs]].
