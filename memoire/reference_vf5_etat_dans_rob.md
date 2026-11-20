---
name: reference_vf5_etat_dans_rob
description: Dans le build APM3 de VF5FS l'état de mouvement est à ROB+0x8A0, pas ROB+0x798 ; les consommateurs adressent en ROB-relatif.
metadata:
  type: reference
---

L'état de mouvement de `mothead` est à **`ROB+0x798` dans le build R.E.V.O.** mais à
**`ROB+0x8A0` dans le build APM3** (celui de `vfes.exe`, le seul qui se laisse déboguer).
`ctx[1]` passe de `ROB+0x338` à `ROB+0x440` : écart constant de `0x108`. Lu dans
`MothApplyRecord` APM3 = **`0x180158B40`** (et non `0x180158B51`, qui n'en est que le
fragment `.pdata` portant la boucle de liste 1), unique appelant `0x18015A350`.

**Pourquoi c'est le piège central** : les consommateurs des champs de l'état ne tiennent pas
un pointeur sur l'état, ils tiennent le **ROB**, et adressent en ROB-relatif — `[rdi+0x9F8]`
pour la fenêtre 0, pas `[rdi+0x158]`. Toute recherche statique menée sur les offsets d'état,
ou sur `0x798`, ne trouve rien et fait conclure à tort qu'il n'y a pas de consommateur.
C'est exactement ce qui avait bloqué le verrou des 32 fenêtres.

Corollaire : la constante `ST = 0x798` de `tools/oracle_handlers.py` ne fausse pas ses
relevés (il fabrique lui-même le contexte), mais elle ne décrit pas APM3.

Voir [[reference_reprise_vf5]] et [[project_vf5_re]].
