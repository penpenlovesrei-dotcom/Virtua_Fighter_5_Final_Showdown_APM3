---
name: reference-fenetre-fixe-attribution
description: "Une fenêtre fixe autour d'une routine donne de fausses attributions — le symptôme qui la trahit est un site d'appel attribué à deux décors."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7f4afaf5-d8a3-4dd5-9905-114b9a59832e
  modified: 2026-09-01T16:26:35.186Z
---

Les outils d'attribution de blocs (`chargeurs2i.py`, `chargeursng.py`) balayaient une
**fenêtre fixe** autour d'une routine (`0x200` octets) pour trouver ses appels. Les scripts
d'étage se suivent en mémoire — 340 à 1672 octets en 2nd Impact — donc la fenêtre mord sur la
routine suivante et lui vole ses appels.

**Le symptôme qui trahit le défaut, et qu'il faut chercher en premier : un même site d'appel
attribué à deux décors.** Un site n'est que dans une routine. Si la sortie en montre un
partagé, l'attribution est fausse — c'est ce qui a démasqué le défaut le 01/09/2026
(`0x8C0DEB7A` donné aux décors 12 et 13).

**Les deux gardes qui le corrigent**, joints :

1. borner la fenêtre au premier `rts` (`0x000B` en SH-4) plus son delay slot ;
2. refuser tout site qui tombe dans la routine d'un *autre* décor, quelle que soit la
   fenêtre qui l'a ramassé.

Attention : corriger ce défaut ne suffit pas. Il masquait un second, plus profond — l'index
de la table des scripts est la **bande**, pas le décor (voir
[[reference-2i-index-est-la-bande]]). C'est ce second défaut qui donnait le bloc de Sean à
Urien. Les deux se cumulaient.

C'est le même piège que [[reference-coherence-nest-pas-role]] sous une autre forme : la
sortie était parfaitement cohérente d'aspect. Voir [[reference-2i-variantes-aire]].
