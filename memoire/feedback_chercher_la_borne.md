---
name: feedback_chercher_la_borne
description: "Ne pas régler une valeur « raisonnable » : chercher la BORNE dans le code. Un indice a une taille de tableau, et elle est écrite en clair."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-08T21:22:27.535Z
---

Frédéric, 2026-09-08 : **« Ne tâtonne pas, désassemble tout ce qui est
nécessaire »**, et **« ne me fais plus tester pour rien, on perd notre
temps »**. Il compte les essais à l'écran et les limite lui-même (« fait, et
c'est la dernière fois »).

Le cas qui l'a déclenché : pour faire passer un texte au premier plan, j'ai
monté un calque de **8** en écrivant dans le commentaire « le montant est
volontairement modeste ». Le jeu a planté. La valeur n'était pas modeste ou
excessive — **elle était hors bornes**, et la borne était écrite en clair, une
ligne au-dessus dans le code : `mov ecx, 0x838 ; call operator new`, puis un
constructeur de tableau à **128 éléments**. Même `1` aurait pu sortir.

**Why:** un « réglage raisonnable » est un aveu qu'on n'a pas lu la structure.
Quand une valeur sert d'**indice**, la question n'est jamais « combien mettre »
mais « jusqu'où va le tableau » — et un allocateur, un constructeur de tableau
ou une comparaison de garde le disent en une instruction.

**How to apply:** avant de proposer une valeur à régler, trouver son domaine :
`new(taille)`, le compte passé au constructeur de tableau, le `cmp` de la garde.
Si le domaine ne se trouve pas, dire qu'il n'est pas trouvé plutôt que de
livrer un essai. Voir [[feedback_lire_le_code_pas_l_image]],
[[feedback_premisse_qui_borne]] et [[reference_vf5_texte_2d]].
