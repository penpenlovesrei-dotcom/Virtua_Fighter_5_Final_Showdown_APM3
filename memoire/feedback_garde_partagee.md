---
name: feedback_garde_partagee
description: "Neutraliser un saut de garde débloque un cas et casse tous les autres : soigner la cause qui remplit la variable, pas la garde qui la lit."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7b8919f9-a3c9-4e11-a256-ad9c22b4c7e9
  modified: 2026-09-04T23:26:07.407Z
---

Quand un écran reste figé sur une attente, **ne pas neutraliser le saut de
garde**. La garde est presque toujours partagée : la débrancher pour un cas la
débranche pour tous. Il faut remonter à ce qui **remplit** la variable testée.

**Why:** le 2026-09-04 sur VF5, le menu console restait suspendu derrière la
scène RANKING, qui sur une borne sans réseau ne se termine jamais. J'ai
remplacé le `jne` de `0x1801DC650` par six `nop` (`--menu-ranking`). Le blocage
a disparu — et avec lui la suspension du menu principal pour **tous les
sous-menus**. Le lendemain, Frédéric : « quand je me déplace dans un sous-menu,
les directions agissent aussi sur le menu principal en arrière-plan ». J'ai
alors cherché le défaut dans le moteur, comparé avec R.E.V.O. (identique),
écrit une sonde — pour découvrir que la cause était mon propre correctif.

Le signe qui aurait dû me sauter aux yeux dans la mesure : la sonde disait
`vivante=1` puis, la ligne suivante, « sous-page effacée ». **Un `jne` qui ne
saute pas alors que sa condition est vraie n'existe pas** : le saut n'était
plus là.

**How to apply:**

- avant de neutraliser une garde, compter ses autres bénéficiaires — ici, la
  même instruction protégeait cinq sous-menus ;
- soigner la cause : c'était le rangement `0x1801DCE2C mov [rdi+0x650], rax`,
  sept octets, qui inscrivait RANKING comme si c'était un sous-menu ;
- si le prédicat lui-même est mauvais, le remplacer **au site d'appel** —
  jamais toucher le corps (96 autres appelants) : voir
  [[reference_vf5_verrou_bouchonne]]. Et chercher le bon prédicat **dans le
  moteur** avant d'en écrire un : ici les trois candidats étaient « la scène
  joue-t-elle ? » (trop court), « la sous-page s'en va-t-elle ? » (drapeau de
  transition, jamais relâché — le menu restait bloqué au retour) et « la scène
  existe-t-elle ? », qui était déjà utilisée sur le même objet deux cents
  octets plus loin. C'est celle-là qui marche ;
- et quand un défaut apparaît après une session de correctifs, **relire ses
  propres patchs avant de désassembler le moteur**.

Voir [[project_vf5_mode_console]], [[feedback_cartographier_la_zone]].
