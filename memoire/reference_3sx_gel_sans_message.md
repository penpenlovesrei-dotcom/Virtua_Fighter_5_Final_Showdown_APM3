---
name: reference-3sx-gel-sans-message
description: "Localiser un gel muet dans 3SX — l'absence de fatal.log écarte tout mtrans, et la méthode des jalons réécrits par trame."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7f4afaf5-d8a3-4dd5-9905-114b9a59832e
  modified: 2026-09-01T04:54:13.746Z
---

Dans 3SX, un gel **sans message** se localise sans débogueur (aucun n'est installé sur cette
machine, et un `pacman` sur ce MSYS2 est risqué — voir [[reference-msys2-ca-bundle-vide]]).

**Le tri qui coûte zéro essai.** Tous les `while (1) {}` de `mtrans.c` — la panne d'Ibuki —
sont précédés d'un `flLogOut`, et `flLogOut` (`foundaps2.c`) écrit `fatal.log` avec `fclose`
**puis TUE le jeu** (`__dead2` → `fatal_error`). Donc :

* **pas de `fatal.log` + le jeu tourne en rond = ce n'est AUCUN puits de `mtrans`.**

Ne pas repartir sur `get_mltbuf16_ext` sans avoir regardé `fatal.log` d'abord.
`njWaitVSync_with_N` (`sys_sub.c`) est un `while (1)` pur mais n'est appelé nulle part.

**Deux battements valent mieux qu'un.** Un battement posé dans `DecorObjets_Avancer` ne dit
rien quand il se tait : figé, ou bien `eff05` ne l'atteint pas. Le battement qui tranche est
dans `SDL_AppIterate` (`sdl_app.c`) — il compte les tours de la boucle de trame et ne dépend
de rien.

**Les jalons réécrits par trame** (`port/video/jalon.c`) : le journal ne contient jamais
qu'UNE trame, et alterne entre `jalons-a.log` et `jalons-b.log`. Au gel, l'un porte la trame
morte — son dernier jalon est le dernier point atteint — et l'autre une trame saine comme
témoin. Armé seulement à partir d'un étage ≥ 22, donc les menus ne ralentissent pas. C'est ce
dispositif qui a mené du « ça gèle » à la fonction exacte en trois essais.

Voir [[reference-reprise-chantier]] et [[feedback-verifier-le-build]].
