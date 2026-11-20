---
name: reference_2i_profondeur_palette
description: "La profondeur d'un objet de décor 2I est en +556, et elle vaut son numéro de palette."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-04T17:08:45.034Z
---

**`+556` est `my_priority`, et il reçoit le NUMÉRO DE PALETTE.** Lu dans le code sur deux
chargeurs : `+88` et `+556` sont alimentés par le même registre, en écritures consécutives
(`8C02936E` : `+556 <- r1`, `+88 <- r1` ; `8C02356A` : `+88 <- r3`, `+556 <- r3`).

L'ancre qui nomme les champs : les spawners écrivent `0x4200` en `+552`, exactement ce que
`eff05.c` pose dans `my_col_mode`. D'où `+554 = my_col_code`, `+556 = my_priority`,
`+558 = my_family` (notre « plan »). `charid.c` confirme : il pose ces quatre champs dans
cet ordre.

**L'échelle** : `char_init_data2` donne aux combattants un `my_pr` de **28 à 56** ; les
plans de fond sont à 84, 90, 94 ; le modèle du port à 80. Un `z` plus grand est plus loin.
Un objet à 23 passe donc devant les combattants.

J'avais affirmé le contraire — « aucun chargeur n'écrit la profondeur » — en cherchant
`position_z` à `+76`, offset calculé dans une structure du port de 140 octets sans rapport
avec l'objet 2I. Voir [[feedback_analogie_nest_pas_lecture]] et
[[reference_2i_inventaire_chargeurs]].

Autre correction du même jour : **la bande n'est pas le décor**, et `bande_vers_decor` n'a
aucun trou — la bande 11 est le décor 10. Voir [[reference_tables_indexees_par_etage]].
