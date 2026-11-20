---
name: reference-sh4-fin-de-fonction
description: "Le premier rts d'une fonction SH-4 n'est pas sa fin — c'est souvent une sortie d'échec enjambée par un branchement."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-03T08:25:46.014Z
---

Pour borner une fonction SH-4, ni la fenêtre fixe ni le premier `rts` ne conviennent :

* une **fenêtre fixe** déborde sur la fonction suivante et lui vole ses appels (symptôme :
  un même site d'appel attribué à deux décors) ;
* le **premier `rts` est souvent une sortie d'échec**. Le spawner `0x8C0323F0` de SF3 2nd
  Impact teste son allocation et rend `-1` vingt octets avant le corps qui lit son bloc.
  S'y arrêter fait conclure « cette fonction ne lit rien ».

La règle qui tient les deux bouts : suivre les branchements (`bra`/`bsr` disp12,
`bt`/`bf`/`bt.s`/`bf.s` disp8), retenir la cible la plus lointaine, et n'accepter un `rts`
que s'il n'est **pas enjambé**.

**Pourquoi :** les deux erreurs ont chacune produit une fausse conclusion sur ce projet, et
elles se compensent en apparence — l'une trouve trop, l'autre pas assez.

**Comment l'appliquer :** `outils/spawners2i.fin_de_fonction` porte la version juste ;
`chargeurs2i.fin_de_fonction` a encore la règle du premier `rts`. Voir
[[reference-fenetre-fixe-attribution]] et [[reference-decors-doc-unique]].
