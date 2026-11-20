---
name: reference_3sx_objets_decor_animes
description: 3SX anime déjà les objets de décor (eff05) ; trois maillons manquaient à un étage ajouté.
metadata: 
  node_type: memory
  type: reference
  originSessionId: d8349b3e-1653-4777-8c03-2b86bf71ea1e
  modified: 2026-08-28T18:36:01.972Z
---

3SX sait animer un objet de décor **dans un étage ajouté** — mesuré le 28/08/2026 sur
l'étage 23 : 29 images distinctes, une par trame après un maintien initial de 50.

La mécanique existe : `eff05.c`, « Stage background objects ». Un objet tient en huit
`s16` — `{ dead_f, plan, palette, x, y, z, index d'animation, sync }` — via
`scr_obj_num[bg_index]`, `scr_obj_data[bg_index]`, `char_add[bg_index]`.

**Les trois maillons qui manquaient à un étage au-delà des 22 d'origine :**

1. `effect_05_init()` n'était pas appelé depuis le script d'étage (`bg220.c`).
2. Le groupe de graphiques n'était pas chargé — un étage ajouté emprunte la liste de
   chargement d'un autre. `mtrans.c` **boucle à l'infini** dans ce cas (le « plantage au
   chargement »). `load_any_texture_patnum(cg_number, 2, 0)` avant le dessin le règle.
3. `char_move()` n'était pas appelé : `eff05` et `eff06` ne l'appellent jamais, leurs
   objets sont **fixes par conception**. C'est `eff07` qui anime.

**Deux pièges qui ont coûté trois parties :** `cg_ctr` est un compte à rebours de
maintien, pas un numéro d'image ; et une fenêtre de trace de 40 trames est trop courte
quand le maintien de la première image en fait 50. **Journaliser un changement, pas un
compteur.**

**Comment un objet obtient ses pixels** — et pourquoi `tex_remix` ne peut rien pour eux :
une page de groupe fait 256×256, découpée en 16×16 chips de 16×16
(`seqsStoreChip`, `mtrans.c` : `u = (code & 0xF) * 16`, `v = code & 0xF0`,
`page = gix + (code >> 8)`, `gix = mts_base[7].gix` = 80). Mais ces pages **ne viennent
pas de l'archive** : elles sont remplies à l'exécution, chip par chip, dans `mtrans.c`
vers la ligne 560 — `lz_ext_p6_fx()` décompresse 256 octets dans `mt->mltbuf`, puis
`njReLoadTexturePartNumG()` téléverse. Elles ne passent donc jamais par
`ppgSetupTexChunk_3rd`, où `tex_remix` est branché.

**Le point d'injection est là** : un chip 16×16 = 256 octets d'index 8 bits, le format
exact de nos tuiles. Recopier les nôtres dans `mltbuf` juste après `lz_ext_p6_fx`.

Le port n'a aucun journal ; `fatal_error()` écrit sur stderr avec une trace de pile.

Lié à [[reference_sf3_dc_pool_tuiles]], [[project_ajouter_decors_3sx]],
[[feedback_verifier_le_build]].
