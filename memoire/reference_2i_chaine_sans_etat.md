---
name: reference-2i-chaine-sans-etat
description: "La chaîne complète qui produit un sprite de décor de 2nd Impact sans aucun savestate Flycast — validée à l'écran."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 8d4f5f21-e1e1-4df4-9937-77d366b04e27
  modified: 2026-08-29T19:41:44.741Z
---

Validée à l'écran le 29/08/2026 sur le petit obélisque de `bg00` (étage 22, plan 4) :
placement **et** couleurs justes, sans ouvrir un seul `.state`.

    table des elements   0x8C17B980 +      enregistrements de 16 octets
        +0 plan   +2 drapeaux   +4 x (signe)   +6 y   +8 palette   +10 script
              |
    table maitresse des scripts   0x8C5F9B38 + aire*4  ->  [pointeurs]
        script -> enregistrements de 8 octets, u16 +6 = index global
              |
    asset F_ETCnn : anims[index global - span], span = `index_global[0]`
        champ 1,2 = l'ANCRE     champ 4 = offset dans la table des sprites
        le RANG de cet offset parmi les offsets distincts = le numero de sprite
              |
    assemblage.charger(asset) -> (asset, tuiles) ; assemblage.poser(sprite, tuiles)

**La palette** : `base(decor, drapeaux) + offset`, avec `champ palette du MORCEAU`
(`drapeaux = champ >> 9`, `offset = champ & 0x1FF`), bases dans `outils/bases.py`.
Couleurs lues dans la **banque du binaire, offset `0x1D9AEC`**, 2715 palettes de 64
couleurs RGB555 (`palettes.lire`). Adresse confirmee par `0x8C0F59AA` :
`r4 + 0x8C1E9AEC - 0x02798000`.

* Prendre la palette de l'ELEMENT au lieu du morceau donne un emplacement faux (913 au
  lieu de 839 pour l'obelisque) : un degrade plat.
* Une palette peut avoir ses premieres entrees en **magenta `0xFC1F`** sans etre fausse —
  ce sont des emplacements que le sprite n'emploie pas. Verifier quels index le sprite
  utilise avant de conclure.
* Base verifiee : l'acolyte de `bg00`, offset 44, donne **871**, la valeur de
  `PALETTES-CONFIRMEES.md`.

**Position** : l'ancre du script ne suffit pas. `assemblage.poser` rend
`(image, masque, x0, y0)` et `(x0, y0)` est le coin de la boite **dans le repère du
sprite** : l'ancre mène à l'origine du sprite, `(x0, y0)` de cette origine au coin de
l'image. Les deux s'ajoutent.

    x = (element.x + ancre_x + x0) & 0x3FF
    y = (sol - element.y + ancre_y + y0) & 0x3FF     sol = 1023 pour treize decors

`x0` vaut zéro sur les neuf éléments de `bg00`, d'où un `x` juste même en l'oubliant ;
`y0` non (-32 temple, -16 obélisques et acolyte), et c'est de ces valeurs-là qu'ils
étaient trop bas. Outil : `outils/poser22.py`.

**L'objet animé, lui, n'est pas dans le repère de la banque.** `bg.c` capture
`BgMATRIX` avant son `njTranslate(0,0,1024)` + `njScale(0,1,-1,1)`, donc une page posée
en `bank_y` se voit en `1024 - bank_y` ; et la grille du motif met la rangée d'image
`lig` en `(ligs-1-lig)*16` (`y_moteur`). D'où
`position_x = bank_x`, `position_y = 1024 - bank_y - (ligs-1)*16`. Le terme
`(ligs-1)*16` manquait — 80 px pour l'acolyte.

**Ce qui manque encore** : comment chaque decor atteint SON bloc dans la table des
elements. Les blocs ne sont vises par aucun pointeur -- `0x8C0FCE3C` les atteint par
`base + offsets[index]`, la base venant de `0x8C0FCCC8`.

Voir [[reference-2i-coefficients-binaire]] et [[feedback-lire-le-code-pas-l-image]].
