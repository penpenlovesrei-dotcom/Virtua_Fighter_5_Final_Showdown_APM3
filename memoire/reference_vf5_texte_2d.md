---
name: reference_vf5_texte_2d
description: "VF5 — mettre du texte au PREMIER PLAN : validé à l'écran. La profondeur est un indice borné, 4 calques x 32 rangs ; on vise le rang 127 dans son PROPRE descripteur."
metadata:
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-08T21:53:36.373Z
---

**VALIDÉ À L'ÉCRAN le 2026-09-08** — Frédéric, sur capture : « c'est bon le
texte est enfin au premier plan ». La méthode ci-dessous est celle qui marche ;
c'est la référence pour tout texte à poser par-dessus une scène AET.

**Dessiner une chaîne** : `0x18019B2E0(descripteur, drapeaux, format, …)` — la
même fonction que le « NOW LOADING » que `--sans-now-loading` neutralise.
Descripteur de 0x50 octets (`0x18019A8C0`) : `+0x08` couleur, `+0x34`…`+0x40`
les coordonnées **en pixels d'écran**, `+0x48` le STYLE (0x40 octets,
`0x18019A9D0`, mode par `0x18019B6F0`, taille par `0x18019B830`). La chaîne est
un **pointeur direct**, pas un identifiant `string_array`.

**LA PROFONDEUR EST UN INDICE DANS UN TABLEAU BORNÉ.** `0x180187C00` soumet la
commande au contexte 2D global (`0x180719900`), `0x18018CA20` l'insère :

    adresse = contexte + 16*( (desc+0x24) + 1 + ((desc+0x28 + calque) << 5) )

Le constructeur `0x18018A030` donne la taille : `new(0x838)`, puis
`0x1802FE160(ctx+0x10, 0x10, 0x80, …)` = **128 compartiments de 16 octets en
+0x10**. Le « +1 » est ce décalage. Donc

    indice = (desc+0x24) + ((desc+0x28 + calque) << 5)   dans 0..127
           = QUATRE calques de TRENTE-DEUX rangs, et rien de plus.

**LA RECETTE VALIDÉE.** La commande du texte ne pose pas `cmd+0x14` : il reste
à `-1` et l'insertion retombe sur `[contexte+0x828]`, le calque courant, celui
que l'AET a monté — d'où le texte toujours dessous. **Ne pas monter ce calque**
(global, et +8 sort du tableau : plantage du 2026-09-08). Corriger son PROPRE
descripteur, juste avant le dessin :

    desc+0x28 = 3 - calque       (le calque effectif vaut toujours 3)
    desc+0x24 = 31               (le dernier rang)
    si calque > 3 : ne pas dessiner du tout

→ indice **127**, le dernier compartiment, dessiné après tout le reste, et hors
d'atteinte du débordement. `+0x24`/`+0x28` n'ont que deux lecteurs,
`0x18019B1D0` et `0x18019B1D6` : ils sont à nous.

Le dessin part du **créneau 4 de `TaskSelStage`** (`0x180400A38`), un bouchon
`ret 0` — la phase de rendu. Liseré fait à la main : neuf passes, huit noires
décalées de 2 px, la blanche au centre.

**How to apply:** six essais à l'écran, puis un plantage, pour un problème
entièrement lisible — la taille du tableau était écrite en clair dans le
constructeur. Voir [[feedback_chercher_la_borne]] et
[[reference_vf5_greffe_section]]. Document : `analysis/texte_2d.md` §8-9-10.
