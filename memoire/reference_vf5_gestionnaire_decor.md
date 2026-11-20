---
name: reference_vf5_gestionnaire_decor
description: "VF5 — charger un décor = DEUX appels (géométrie 0x18018FCF0, éclairage 0x1800D7130) ; et le descripteur est posé au gestionnaire à UNE seule instruction, 0x18018EF87."
metadata:
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-09T05:08:37.173Z
---

Dans VF5 FS, **charger un décor, c'est deux appels distincts**, chacun avec son
propre index en dur dans la tâche `STAGE_TASK` de l'écran customize
(`0x1801C4D60`) :

    0x1801C4DA6  mov ecx, 1 ; call 0x18018FCF0   <- la GEOMETRIE (l'image)
    0x1801C4DCB  mov ecx, 1 ; call 0x1800D7130   <- l'ECLAIRAGE seul

`0x1800D7130` ne compose que `%s/%s.ibl` et `%s/light_%s.txt` : **en changer
l'index ne déplace qu'une teinte.** J'ai passé une journée à le patcher en
croyant changer de décor. `--decor-perso` patche les DEUX octets.
**`trm` s'affiche : validé le 2026-09-05, REVALIDÉ le 2026-09-09** après que je
l'ai cassé en le recyclant — voir [[project_vf5_import_5r]].

`0x18018FCF0` est le vrai demandeur, et c'est une **feuille** (absente de
`.pdata`, trouvée par balayage linéaire). Elle écrit `+0x60` du gestionnaire de
décor, singleton `0x1807499D8` :

    +0x58 phase   +0x5C index chargé   +0x60 index demandé (-1 = rien)
    +0x68 descripteur = 0x180403430 + index*0xF0     (41 décors)

**LE DESCRIPTEUR EST POSÉ À UNE SEULE INSTRUCTION** — `0x18018EF40`, le créneau
`+0x10` de la vtable, qui consomme la demande :

    0x18018EF6C  cmp edx, 0x29 ; imul r8, rdx, 0xF0 ; lea rax, 0x180403430
    0x18018EF87  mov [rcx+0x68], r8      <- LE SEUL SITE
    0x18018EF8B  mov [rcx+0x5C], edx

C'est le point d'accroche naturel pour **substituer un descripteur** : une
copie prise à l'exécution du descripteur *vivant* d'un autre décor a tous ses
pointeurs déjà relogés — ce que le patch statique ne peut pas faire, faute de
relocations sur les emplacements d'essai.

**Quatre lecteurs seulement lisent la table STATIQUE par index**, et eux
échappent à cette substitution : `0x18018F560` (le code `STGxxx`),
`0x18018F590` (nom → index), `0x18018F3D0(index, variante)` (la musique — et il
**retombe sur `+0x68`** quand les neuf reprises sont nulles) et `0x18018F630`
(`+0xD4`).

**How to apply:** avant de conclure qu'un index « ne change rien », vérifier que
la fonction appelée produit bien l'image — lire ses chaînes. Une fonction
voisine, au même prototype et au même immédiat, n'est pas la même fonction. Voir
[[feedback_lire_le_code_pas_l_image]]. Documents : `analysis/decors.md` §13-14,
`analysis/menu_console.md` §15.10.
