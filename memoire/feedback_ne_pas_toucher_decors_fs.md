---
name: feedback_ne_pas_toucher_decors_fs
description: Interdiction — ne rien modifier dans les décors de Final Showdown ; le chantier 5R ajoute à côté.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-10T21:49:56.274Z
---

Frederic, 2026-09-10 : « on ne touche pas aux decors de FS, je t'interdis d'y
modifier quoique ce soit ».

**Why:** les 41 decors d'origine sont la reference. Le chantier VF5 R AJOUTE
dix-neuf entrees aux indices 42-60 ; il ne repeint rien. Un correctif applique
« pour que ca corresponde » a un decor d'origine detruit le temoin qui permet de
comparer les deux generations -- et c'est le temoin qui a resolu la moitie des
defauts de ce chantier.

**How to apply:** avant de proposer une retouche d'asset, dire EXPLICITEMENT
quel fichier -- `STGHI5_*` (a nous) ou `STGHAI_*` (a eux). J'ai ecrit « je
retire l'eclairage de nos deux fichiers pour qu'ils correspondent a FS » et il a
compris que j'allais toucher a FS. L'ambiguite seule suffit a alarmer.

Deux exceptions existantes, toutes deux demandees par lui et validees a
l'ecran : les 3 octets de `--du2-collision` (descripteur de `du2`, +0x48..+0x4A)
et `--decor-repli`. Rien d'autre.

Verification : `.decors` recopie les 41 entrees a l'identique ; comparer la DLL
patchee a `.origine` table par table (script d'audit du 2026-09-10) le prouve en
quelques secondes. Le faire plutot que de l'affirmer.

Voir [[feedback_ajouter_jamais_remplacer]], [[feedback_ne_pas_defaire_le_valide]],
[[project_vf5_import_5r]].
