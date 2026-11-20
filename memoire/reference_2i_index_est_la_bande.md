---
name: reference-2i-index-est-la-bande
description: "L'index de 0x8C1D3FB4 est la BANDE, pas le décor — c'est la cause du « décalage d'index à partir de l'étage 10 »."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7f4afaf5-d8a3-4dd5-9905-114b9a59832e
  modified: 2026-09-01T16:26:18.561Z
---

**`0x8C1D3FB4`, la table des scripts d'étage de 2nd Impact, est indexée par la BANDE, pas par
le décor.** Tout l'outillage appelait « décor » cet index, d'où un cran d'écart sur la moitié
des décors — le fameux « décalage d'index à partir de l'étage 10 » que la doc constatait sans
l'expliquer.

La table `0x8C1D591C` donne `(décor*3 + aire) -> bande` et dit que **le décor 8 porte les
bandes 8, 9 et 9**. Au-delà, `bande = décor + 1`.

**La mesure qui tranche** (les deux lectures en concurrence sur les dix-sept blocs — combien
résolvent 100 % de leurs images dans l'asset du décor supposé) :

    lecture « index = decor »  ->  14 / 17
    lecture « index = bande »  ->  16 / 17

Elle ne gagne pas aux points, elle redresse les deux échecs : l'index 13 passe de **0/19**
(lu Urien) à **46/46** (lu Sean), l'index 11 de 0/0 (Ken) à 8/8 et 4/4 (Yang). Et l'index 10
passe de 4/4 à **16/16 et 82/82** — le critère « beaucoup d'images » d'`accorder2i.py`.

Ça confirme par le calcul ce que Frédéric avait tranché à l'écran : `0x8C17E918` est bien le
bloc d'Oro, appelé depuis la **bande 10**.

Conséquences sur les attributions : **Ken (décor 11) et Urien (décor 13) n'ont AUCUN bloc** ;
leurs objets supposés venaient du décalage. Sean (décor 12, bande 13) a le bloc
`0x8C17E9A6`, deux enregistrements — dont le singe.

Voir [[reference-fenetre-fixe-attribution]], qui est un défaut distinct du même outil, et
[[reference-coherence-nest-pas-role]].
