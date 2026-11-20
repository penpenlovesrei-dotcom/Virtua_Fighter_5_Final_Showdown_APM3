---
name: feedback_premisse_qui_borne
description: Une énumération exhaustive ne vaut que ce que vaut la prémisse qui la borne — écrire la prémisse noir sur blanc pour pouvoir l'attaquer.
metadata:
  type: feedback
---

Deux verrous du chantier VF5, tenus pour définitifs après des recherches menées
*exhaustivement*, sont tombés le même jour. Dans les deux cas l'exhaustivité était réelle et
portait sur le mauvais objet :

- les 32 fenêtres : cherchées sur les offsets d'état, alors que les consommateurs tiennent le
  **ROB** et adressent en ROB-relatif ;
- les 37 codes de liste 2 : cherchés comme des valeurs **comparées**, alors que le code
  **indexe** une table ; et le parcours lit un **curseur voisin** du pointeur examiné.

**Why:** « les trois voies d'accès possibles ont été énumérées exhaustivement » est une
affirmation sur une liste de voies, pas sur le binaire. Quand un décompte est complet et que
le résultat reste nul, le défaut est presque toujours dans la borne, pas dans la recherche.

**How to apply:** devant une conclusion négative « il n'existe pas de X », retrouver la
prémisse qui définit où X pouvait être, et l'attaquer d'abord. Écrire cette prémisse
explicitement dans la doc : c'est parce que §3.12 énonçait la sienne — « toute lecture passe
par `MothGetRecord` » — qu'elle a pu être réfutée en une heure. Et se méfier des deux formes
de dérive : la base décalée (mauvais point de départ) et le champ voisin (bon objet, mauvais
membre).

Voir [[reference_vf5_liste2_repartiteur]] et [[feedback_lire_le_code_pas_l_image]].
