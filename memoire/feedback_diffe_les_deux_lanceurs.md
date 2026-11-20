---
name: feedback_diffe_les_deux_lanceurs
description: "Quand un build marche et l'autre pas, commencer par DIFFER LES DEUX INVOCATIONS — avant les fichiers, avant le désassemblage."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-08T22:12:42.996Z
---

2026-09-08, VF5. `decor_5r_akira.cmd` montrait le dojo de VF5 R correctement.
Mon `variantes_texte.cmd` montrait autre chose. Frédéric a dû me dire **deux
fois** : « regarde comment `decor_5r_akira.cmd` fonctionne, lui est bon ».

La différence était **une option de ligne de commande**. `--decors-dural cas`
réécrit une translation `cmp eax,7 ; jl ; cmp eax,11 ; jg ; add eax,14` —
`cas riv jin sin djo -> du1..du5`. **`djo` vaut 11 : il est dans la plage.**
Tout combat au dojo chargeait `du5`. Ce n'était pas le dojo mal éclairé, ce
n'était pas le dojo.

Avant de trouver ça j'avais accusé, dans l'ordre : les réglages d'éclairage de
VF5 R (réfutés par sa propre capture), puis le descripteur incomplet de
l'emplacement (réel, mais secondaire). Deux détours, plusieurs désassemblages,
alors qu'un `diff` des deux lignes de commande donnait la réponse en dix
secondes.

**Why:** deux builds qui ne different que par leur invocation forment une
expérience déjà faite. La comparer coûte une commande ; la reconstruire par
l'analyse coûte des heures et se trompe. Et quand il dit « celui-là est bon »,
il désigne le témoin — pas une opinion à contourner.

**How to apply:** dès qu'un build marche et l'autre non, **differ d'abord les
deux invocations**, ensuite les fichiers posés, ensuite seulement le binaire.
Et faire refuser au patcheur les combinaisons d'options qui se contredisent :
`--variantes-djo` avec un `--decors-dural` qui avale l'indice 11 est
maintenant une erreur explicite. Voir [[feedback_son_observation_prime]],
[[feedback_recopier_tout_l_enregistrement]] et `analysis/decors.md` §13.
