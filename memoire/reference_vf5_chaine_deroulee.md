---
name: reference_vf5_chaine_deroulee
description: "Une chaine de comparaisons deroulee occupe plus de place qu'un balayage : on la remplace SUR PLACE."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-10T21:08:06.973Z
---

Quand le nombre d'entrees d'une table est petit, le compilateur DEROULE la
boucle de recherche en autant de `cmp` qu'il y a d'entrees. Le nombre d'entrees
vit alors dans le CODE, et deplacer la table ne sert a rien.

**Mais une chaine deroulee coute plus d'octets qu'un balayage.** Mesure du
2026-09-10 sur les quatre taches d'effet de VF5 : la chaine occupe 26 a 63
octets, le balayage en demande 24 a 33. On la remplace donc SUR PLACE, sans
caverne :

    lea CUR,[rip+table] / L: cmp [CUR+d],-1 / je AUCUN / cmp IDX,[CUR+d]
    je TROUVE / add CUR,pas / jmp L / AUCUN: jmp <sortie> / TROUVE: ... nop

Il faut relever, pour chaque fonction : le registre d'INDEX, le registre de
RESULTAT, l'adresse de reprise, la sortie d'echec, et le prologue pris dans la
zone (BREATH y avait un `mov r14, rcx`). Le patcheur REFUSE si ca ne tient pas.

Piege paye : `mov r14, rcx` est `4C 8B F1`, pas `49 8B F1` (= `mov rsi, r9`).
Toujours RELIRE le code pose au desassembleur.

Voir `patch_moteur.CHAINES` / `balayage_chaine()` et
[[reference_vf5_taches_effet]].
