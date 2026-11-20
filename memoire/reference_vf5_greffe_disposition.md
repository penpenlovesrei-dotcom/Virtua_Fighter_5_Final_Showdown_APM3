---
name: reference_vf5_greffe_disposition
description: VF5 — un tableau de la greffe dimensionné en dur déborde chez le voisin en silence ; verifier_disposition() le refuse.
metadata:
  type: reference
---

La greffe de `--variantes` range son code et ses données à des offsets fixes.
Quand un tableau y est dimensionné **en dur**, l'agrandir ailleurs ne suffit
pas : il déborde sur son voisin, et il l'ECRIT.

Le cas du 2026-09-10 : `VAR_NUM` (« le numéro courant par anneau ») était
déclaré `0x600, 4 u32` pendant que `VARIANTES_MAX_ANNEAUX` passait de 4 à 20
pour les dix-neuf décors de VF5 R. Au cinquième anneau, `VAR_NUM[anneau]`
lisait `VAR_RANG`, puis `VAR_APPLIQUE`, `VAR_X`, `VAR_Y`, et enfin `VAR_DESC` —
le descripteur de texte. L'entrée A y écrivait aussi. Résultat : « nombreux
plantages », jamais au même endroit.

La sonde `tools/pister_plantage.py` l'a nommé en une passe :

    ACCESS_VIOLATION en .greffe+0x1E7
    mov eax, [rdx + rcx*4]   rdx = VAR_IDX, rcx = 0x43EB0048  (un flottant)

**How to apply:** tout tableau de la greffe se **dérive** de
`VARIANTES_MAX_ANNEAUX` / `_MAX_VARIANTES`, et `patch_moteur.verifier_disposition()`
— appelée par `variantes_greffe` avant d'assembler — refuse tout recouvrement.
Contrôle négatif : remettre `VAR_NUM = 0x600` rend « NUM (0x600..0x650)
recouvre RANG (0x610) ». Voir [[feedback_controle_qui_ment]],
[[reference_vf5_greffe_section]], [[feedback_chercher_la_borne]].
