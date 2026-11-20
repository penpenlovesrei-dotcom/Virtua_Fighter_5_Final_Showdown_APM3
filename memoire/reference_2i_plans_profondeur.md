---
name: reference-2i-plans-profondeur
description: "Les plans de décor de 2nd Impact — l'ordre de dessin est celui de la liste, et la règle plan → objet est lue dans le code, pas corrélée."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 8d4f5f21-e1e1-4df4-9937-77d366b04e27
  modified: 2026-08-29T10:54:40.006Z
---

**Le champ `plan` d'un élément ne dit pas la profondeur.** Il ne choisit que le couple de
défilement `defil[plan]`. La boucle `0x8C0F693C` parcourt les éléments dans l'ordre de la
liste et dessine chacun aussitôt : **l'ordre de la liste EST l'ordre de dessin.**

Empiler par numéro de plan croissant est faux partout : sur les vingt-six relevés les deux
ordres diffèrent à chaque fois. Pour `bg00` l'ordre de la liste est **0, 1, 7, 3, 2, 4** —
le plan 7 arrive avant le plan 3, donc son petit obélisque passe *derrière* le temple.

**La règle plan → objet est dans le code**, à `0x8C0E8C6A` (poseur d'un plan à
`0x8C0E8BC6`, poseur brut à `0x8C0FF7F8`) :

    pour idx = 0 .. [0x8C6AF304+16] - 1 :
        poser(plan = idx + 1,
              x = (-objet[idx].x) & 0x3FF,
              y = (0x300 - objet[idx].y) & 0x3FF)

Les objets font **144 octets** à partir de `0x8C6AF358` (= `0x8C6AF304 + 84`), `x` en `+10`
et `y` en `+12`. `DONNEES.md` n'avait que l'horizontale, et par corrélation (35/36) ; le
code donne les deux, exactement. `0x8C0FF84E` remplit ensuite `0x8C7EFCCC` depuis la
position **précédente** de chaque plan (`plan[+6]`, `plan[+14]` du bloc de 16 octets à
`0x8C84135C`).

**Conséquence : seuls `nb_objets` plans sont pilotés par la parallaxe.** Pour `bg00` ce sont
les plans 1 et 2 ; ses plans 3 et 7 défilent (704, pas 0 comme les plans vraiment intacts)
mais **la source n'est pas localisée** — le script de Gill (`0x8C0FE2D8`, table des scripts
à `0x8C6020AC`, index = numéro de décor) n'appelle le poseur qu'avec `idx = 1`, et la table
`0x8C84135C` n'a que cinq utilisateurs, tous dans le bloc `0x8C0FF7E0..0x8C0FF85A`.

**Donc on ne sait PAS envoyer au plan lointain un plan sans objet.** `elements.py` pose un
sprite en `e.x + m.x`, ce qui n'est juste que contre le fond de SON plan. Essayé le
29/08/2026 sur `bg00` : temple et obélisques du plan 3 posés sur le fond de l'objet 0 —
ils sortaient **trop à gauche**, alors que le ciel étoilé, qui est bien l'art de l'objet 0,
tombait juste. Remis au plan proche. La profondeur reste bonne malgré tout, grâce à l'ordre
de la liste. **`PLANS_LOINTAINS` ne doit contenir qu'un plan dont l'objet est connu.**

**Un état Flycast n'est PAS nécessaire pour ça** — c'est dans le binaire. Voir
[[feedback-lire-le-code-pas-l-image]].
