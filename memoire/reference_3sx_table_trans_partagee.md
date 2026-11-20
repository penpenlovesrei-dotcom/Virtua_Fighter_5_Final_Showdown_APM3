---
name: reference-3sx-table-trans-partagee
description: "La table de trans de 3SX est en RAM et PARTAGÉE : y écrire sa propre grille gèle le moteur dès qu'un autre travail dessine le même motif."
metadata: 
  node_type: memory
  type: reference
  originSessionId: a42b6c0d-1a36-40d8-b5ab-289a8f4629c0
  modified: 2026-08-29T21:19:01.505Z
---

Mesuré le 29/08/2026, sur le gel de fin de round des étages 2I ajoutés.

`DecorObjets_Motif` récrit la liste de morceaux d'un motif **dans la table de trans**.
Cette table est en RAM et modifiable — le moteur y écrit lui-même dans `search_trsptr` —
mais elle est **partagée** : le motif appartient au groupe donneur, et d'autres travaux
le dessinent aussi. Ils lisent alors la grille étrangère, mettent leur motif en cache
**sans ses morceaux de 32×32**, et `get_mltbuf32_ext` — qui ne fait que *chercher* —
journalise puis part en `while (1) {}`. Un gel, pas un plantage.

La trace qui l'a dit :

    GEL 32x32 : code 0x00170022 (groupe 0x17), 0 emplacements occupes

groupe 23, morceau 34 — soit exactement le `CODE_16X16` posé partout — et un cache 32
entièrement vide.

**Correction : garder une copie de l'entrée d'origine et la RENDRE** dès qu'un autre
travail vient dessiner ce motif (`DecorObjets_Motif` est appelé pour tous les travaux),
et en quittant l'étage.

**Et la fausse piste, écartée par la même trace** : `effd3`, l'effet d'aube, n'est appelé
que si `Round_Result & 0x980`. Sur un K.O. ordinaire ce bit est nul — il n'a jamais
tourné. Instrumenter avant d'accuser.

Voir [[feedback-lire-le-code-pas-l-image]] et [[project-ajouter-decors-3sx]].
