---
name: project-fv2-freeplay-dabord
description: "FV2 est fait pour le freeplay uniquement ; le mode crédit n'est qu'un bonus s'il marche."
metadata: 
  node_type: memory
  type: project
  originSessionId: cbe532ed-e4e8-44b3-be45-6eb2a7e27c18
  modified: 2026-08-16T12:04:20.972Z
---

Frédéric construit le menu console de Fighting Vipers 2 **avec le freeplay en
vue, et lui seul**. Le mode à crédits est un bonus : bienvenu s'il fonctionne,
jamais une raison de renoncer à quelque chose.

**Why:** dit explicitement le 2026-08-16, alors qu'on pesait un menu posé sur le
vrai écran titre du jeu et que le crédit était donné comme l'un des deux points
délicats. La moitié de cette objection tombe.

**How to apply:** quand un arbitrage oppose le freeplay au mode crédits, le
freeplay gagne. Ne pas présenter une gêne pour le mode crédits comme un obstacle
— la signaler, et continuer. Ce qui reste vrai en revanche, c'est la mécanique :
un mode se lance en injectant un **vrai Start dans un jeu qui tourne**, donc tout
ce qui gèle le jeu doit dégeler avant d'injecter. C'est indépendant des crédits.

Et la règle qui ne bouge pas : **ne jamais toucher au compteur de crédits** —
c'est ce qui fait marcher le freeplay sans son octet.

Voir [[project_fv2_menu_console]].
