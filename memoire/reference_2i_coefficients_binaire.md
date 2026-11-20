---
name: reference-2i-coefficients-binaire
description: "Où lire les coefficients de parallaxe de 2nd Impact dans le binaire, sans passer par un état Flycast."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 8d4f5f21-e1e1-4df4-9937-77d366b04e27
  modified: 2026-08-29T14:42:58.010Z
---

Les coefficients de parallaxe se lisent **dans `SF3_2ND.BIN`**, pas seulement en RAM — ce
qui est indispensable pour New Generation, qui n'a aucun état Flycast.

**Plans lointain et proche — une table.** `0x8C1D4F48`, **pas de `0x20`**, indexée par le
numéro de décor. La première paire (u32 16.16) est `(coef_x, coef_y)` de l'objet 0, la
deuxième celle de l'objet 1 (toujours 1,00 / 1,00). **Treize décors sur treize** concordent
avec la RAM, et la table couvre aussi `bg07`, `bg08` et `bg0f`, que les états ne couvrent
pas. Les deux paires suivantes de la rangée ne sont pas les objets 2 et 3.

**Plan supplémentaire — écrit en dur par le script d'étage.** Motif :

    mov.l  Rm,@(16,Rn)    objet[+16] = coef_x
    mov.l  Rm,@(20,Rn)    objet[+20] = coef_y

Le balayage général de ce couple donne onze sites et quatre valeurs réelles :

| coef_x / coef_y | sites | décor |
|---|---|---|
| 0,8125 / 0,875 | `0x8C0DC0BA`, `0x8C0DF650` | `bg01` |
| 0,75 / 0,75 | `0x8C0DDF90`, `0x8C0DE3D0`, `0x8C0E0464`, `0x8C0E0664` | `bg09` |
| 0,75 / 0,875 | `0x8C0DEE30`, `0x8C0E0C96` | `bg0e` |
| 0,875 / 1 | `0x8C0DD9DA`, `0x8C0E0234` | non attribué |

**`bg00` n'en écrit aucun** — il n'y a pas un seul littéral `0xE000` dans son script
(`0x8C0FE2D8`). Sa valeur, **0,875 / 0,875, est donc le DÉFAUT**, et c'est cohérent : les
objets 4 et 6 portent `0,875 / 1` et `0,625 / 0,875` **à l'identique dans les vingt et un
états**, donc ce sont des valeurs initialisées, pas des restes. Le 0,875 de `bg00` est
validé à l'écran.

**Règle pour l'automatisation** : coefficient du plan supplémentaire = l'écrasement du
script s'il existe, sinon le défaut 0,875 / 0,875.

Voir [[reference-2i-plans-profondeur]] et [[feedback-lire-le-code-pas-l-image]].
