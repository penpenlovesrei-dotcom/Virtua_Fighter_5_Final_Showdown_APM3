---
name: reference_vf5_champs_rob
description: Champs du ROB établis dans le build APM3 de VF5FS — personnage, posture, masques d'entrée, tampon.
metadata:
  type: reference
---

Champs du combattant (`ROB`) établis sur le build APM3, tous vérifiés autrement que par
déduction :

- **`ROB+0x10` = l'indice du personnage** (0 à 20, l'entrée dans `rob_cmn_mottbl`) et
  **`ROB+0x65C` = la posture**. Les **71** sites d'appel de `GetMotionForRole` (APM3
  `0x18015B310`) présentent tous le même motif : `mov ecx,[ROB+0x10]` et
  `movzx edx, byte [ROB+0x65C]`. `ROB+0x65C` est aussi ce que le code 26 de la liste 2 écrit,
  et l'équivalent de `ROB+0x554` de R.E.V.O. au décalage `0x108` près.
- **`ROB+0x508` = masque d'entrée courant, `ROB+0x510` = masque tamponné,
  `ROB+0x90C` = trames restantes du tampon (un flottant, 15 à 19), `ROB+0x91C` = tampon
  actif.** Relevés à l'exécution à l'entrée des gestionnaires 20 à 24 de la liste 2. C'est un
  tampon d'entrée de jeu de combat.
- `ROB+0x690` = **le compteur de boisson de Shun** (`ROB+0x588` dans R.E.V.O.).
- `ROB+0x8A0` = l'état de mouvement — voir [[reference_vf5_etat_dans_rob]].

Lire `ROB+0x10` permet de savoir **quel personnage est en jeu sans aucune capture d'écran**.
