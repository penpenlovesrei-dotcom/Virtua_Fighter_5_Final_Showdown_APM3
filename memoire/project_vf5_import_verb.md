---
name: project_vf5_import_verb
description: "VF5 — les décors du VF5 d'origine (ver.B) sont posés aux indices 61-81 (Dural : 4 variantes) et vus à la sonde ; empreintes de ykb réparées le 2026-09-11, eau de skb en attente d'un choix."
metadata: 
  node_type: memory
  type: project
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-11T18:42:59.269Z
---

`tools\decors_vf5.cmd` ajoute, à la suite des 19 de VF5 R (42-60) et des 4
Dural de R (82-85), les **21 entrées de ver.B** : 17 lieux (`dob bnb trb ncb
csb rvb jnb snb uib hib aeb skb ykb tkb arb brb tnb`) et **4 Dural** (`drb d2b
d3b d4b`, une géométrie `stgdur` et quatre objsets de ciel). La barre espace
fait tourner FS → R → VF5 ; la case de Dural a 13 variantes. Lot :
`tools/variantes_vf5.py` ; contrôle : `tools/controle_decors_vf5.py`.
Journal (63) à (67), `analysis/decors.md` §21 à §24.

État au 2026-09-11 soir : les empreintes dans la neige de ykb (73) sont
réparées et vues à la sonde — c'était le portage Direct3D, voir
[[reference_vf5_apm3_direct3d11]] ; Frédéric n'a pas encore jugé l'aspect.
L'eau d'Eileen (skb, 72) reste à trancher par lui : le ring de ver.B EST
l'objet `WATER_RING`, rendu blanc laiteux faute de cube d'environnement.

Les quatre ciels de ver.B : coucher de soleil, jour, orage, nuit étoilée.
Libellés provisoires « VIRTUA FIGHTER 5 - 1..4 » : c'est lui qui nomme.

**Why:** ver.B n'est pas un VF5 R de plus — voir
[[reference_vf5_verb_textures_rangs]] et [[reference_vf5_chaque_generation_ses_tables]].

**How to apply:** ne rien cloner du modèle FS qui décrit le CONTENU (objets,
textures, effets, murs, animations) : le relire dans l'ELF de ver.B. Garder du
modèle ce qui décrit le comportement (musique, anneau, rendu). Voir aussi
[[project_vf5_import_5r]], [[project_vf5_decors_dural]].
