---
name: feedback-piloter-supermodel-clavier
description: "Piloter Supermodel au clavier depuis un script : scancodes obligatoires, et verifier le premier plan avant d'envoyer quoi que ce soit."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 44c4ed34-7690-4b13-bc86-36da84c8eb64
  modified: 2026-08-21T12:30:58.534Z
---

Pour mesurer une valeur qui n'existe qu'en jeu, il faut envoyer des touches a Supermodel depuis un script. Deux regles, apprises en les enfreignant le 2026-08-21.

**Toujours des scancodes.** `SendInput` avec `KEYEVENTF_SCANCODE` (fleches en plus `KEYEVENTF_EXTENDEDKEY`). `SendKeys` du WScript.Shell et `keybd_event` en codes virtuels **n'arrivent pas** jusqu'a Supermodel, qui raisonne en positions physiques — c'est deja note dans [[reference_supermodel_memoire]], et je ne l'ai pas applique.

**Toujours verifier le premier plan avant d'envoyer.** Windows refuse `SetForegroundWindow` a un processus qui n'a pas deja le premier plan : `AppActivate` peut renvoyer vrai sans que la fenetre soit devant. Les touches partent alors **dans la fenetre active de Frederic** — l'application Claude, un explorateur — sans le moindre message. Un appui sur ALT plus un `AttachThreadInput` levent le verrou, mais pas toujours.

**Why:** une sequence perdue ne se voit pas dans les donnees ; elle produit des candidats qui ressemblent a des trouvailles. Une valeur relevee 3, puis 5, puis 7 a des intervalles egaux n'etait qu'un compteur libre, prise pour un compteur de credits.

**How to apply:** verifier `GetForegroundWindow()` et **s'arreter** si ce n'est pas la fenetre du jeu, plutot que d'envoyer a l'aveugle (c'est ce que fait `chasse.py` dans `vf3-model3-research`). Et pour toute chasse a la variable, relever deux fois sans rien faire d'abord (masque de bruit), puis avancer par pas irreguliers. Voir [[project_vf3_model3]].

**Les boutons de combat, verifies dans INPUT TEST le 2026-08-22.** Un seul scancode repond : **0x1E, la position physique du A d'un QWERTY** -> PUNCH. Les positions R (0x13), T (0x14) et Q (0x10, la touche marquee A sur un clavier AZERTY) ne produisent RIEN. C'est conforme a `Config/Supermodel.ini` : `InputPunch = KEY_A`, `InputKick = KEY_S`, `InputGuard = KEY_D`, ou les noms `KEY_x` designent des positions QWERTY. Sur le clavier AZERTY de Frederic, les trois boutons sont donc les touches marquees **Q, S, D**. `chasse.touche("a")` envoie bien PUNCH — les mesures passees tiennent.

Si Frederic parle d'un mapping R = GUARD, T = PUNCH, A = KICK, ce n'est PAS celui que Supermodel voit : demander d'ou il vient (manette, JoyToKey, ou souhait de remappage) avant d'adapter l'outillage.
