---
name: feedback_cartographier_la_zone
description: "Désassembler une zone ENTIÈRE d'un coup plutôt qu'une fonction à la demande — et vérifier que la prémisse d'un balayage est aussi systématique que le balayage."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7b8919f9-a3c9-4e11-a256-ad9c22b4c7e9
  modified: 2026-09-04T13:01:36.249Z
---

Sur un binaire, quand une question résiste : **cartographier la zone entière**
au lieu de désassembler une fonction à la demande. Coût, une minute ; ça
remplace vingt questions.

**Why:** le 2026-09-04, sur VF5, j'ai passé une journée à lire une fonction par
question — quatre fausses pistes sur l'écran de sélection, trois correctifs
bâtis sur des lectures locales et démentis à l'écran. Frédéric : « je ne
comprends pas pourquoi toutes les fonctions de l'écran de sélection ne sont pas
encore désassemblées ». Il avait raison : `tools/carte_zone.py` a sorti les 411
fonctions du sélecteur d'un coup et la garde cherchée est apparue en une
minute. C'est ce qui a rendu Dural jouable ([[project_vf5_dural]]).

**How to apply:**

- écrire l'outil de carte une fois (bornes, appelants, appelés, chaînes
  référencées, globaux connus, immédiats remarquables, bouchons) et le relancer
  sur chaque zone ;
- **un balayage ne vaut que ce que vaut sa prémisse** : le premier balayage
  « systématique » cherchait les appels au bouchon *autour des chaînes `_dur`*
  et en trouvait deux ; en énumérant les appelants dans toute la zone, seize.
  Écrire la prémisse pour pouvoir l'attaquer — voir [[feedback_premisse_qui_borne]] ;
- **une fonction n'est pas une entrée `.pdata`** : elle en couvre souvent
  plusieurs chaînées. Prendre la première pour la fonction entière fait conclure
  faux (déjà arrivé sur le menu console). D'où `tools/plage.py`, qui désassemble
  une plage sans s'arrêter au premier `ret` ;
- **et `.pdata` ne liste pas les FEUILLES** — pas de cadre de pile, pas d'entrée
  de déroulement. Ce trou s'est payé trois fois sur VF5 : une feuille qui
  plantait et n'apparaissait sur aucune carte, puis une conclusion fausse
  (« personne ne demande ce mode ») parce que le demandeur était une feuille à
  saut terminal. **Quand la conclusion est « personne ne fait X », il faut un
  balayage LINÉAIRE de `.text` par motif d'octets**, jamais une itération sur
  `.pdata` — celle-ci ne donne qu'un minorant.

Complète [[feedback_lire_le_code_pas_l_image]] : là où celle-ci dit *où* est la
donnée, celle-ci dit *combien* en lire d'un coup.
