---
name: reference_vf5_joueur2
description: "VF5 APM3 — le lecteur d'entrées avait été écrit pour deux joueurs puis amputé ; trois octets le rebranchent (clavier = 1P, manette = 2P)."
metadata:
  node_type: memory
  type: reference
  originSessionId: 7b8919f9-a3c9-4e11-a256-ad9c22b4c7e9
  modified: 2026-09-04T19:13:07.020Z
---

Dans le build APM3, le lecteur d'entrées `0x180243ED0` **saute toutes les
lectures pour le joueur 2** :

    0x180243F62  test ebp, ebp        ; ebp = le numéro de joueur
    0x180243F64  jne  0x1802440D6     ; joueur 2 : saute les 13 Input_isOn

Son masque de boutons vaut donc toujours zéro. C'est pour cela qu'OFFLINE
VERSUS s'affichait grisé, en réclamant en clair une seconde manette (texte
0x81).

**Mais le lecteur avait été écrit pour deux joueurs, puis amputé** : deux de
ses treize sites de code étaient restés **relatifs au joueur**
(`lea edx, [rbp + 2]`, `[rbp + 5]`). D'où un correctif de trois octets d'idée
(`--joueur2` de `tools/patch_moteur.py`) :

1. les onze `mov edx, imm32` deviennent `lea edx, [rbp + code]` + deux `nop` ;
2. les six octets du saut retiré reçoivent **`shl ebp, 4`** : `rbp` vaut 0 pour
   le joueur 1 et **16** pour le joueur 2, dont les codes deviennent 18 à 30.

Le décalage ne casse pas la boucle et **n'a rien à restaurer** : après ce point
`ebp` n'est relu qu'à `inc ebp ; cmp ebp, 2 ; jb`. Joueur 1 → 0 puis 1, on
repart ; joueur 2 → 16 puis 17, on sort.

Côté `apm.dll` (notre stub, `tools/gen_apm_stub.py`), il faut **séparer les
sources**, sinon la manette pilote les deux joueurs : codes 0-14 au **clavier
seul**, codes 18-30 à la **manette seule**.

Touches de validation, une fois en place : clavier `A` `T` `R` `Entrée`,
manette **X, LB, Y, START** (le curseur de la grille ne lit que les codes
logiques 7, 8 et 9 — voir `analysis/menu_console.md` §10).

Voir [[project_vf5_mode_console]].
