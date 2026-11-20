---
name: reference_2i_protocole_transfert
description: "`transfert2i.py` passe un décor à douze portes ; rien ne passe sans être lu dans le code."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-04T20:47:25.332Z
---

`outils/transfert2i.py` est **une barrière, pas un assistant**. Il passe un décor à douze
portes et rend un code de sortie : 0 si toutes passent, 1 sinon. Chaque porte ferme une
faute qui a réellement coûté une régression visible, et son commentaire la nomme.

1. le décor est identifié (**la bande n'est pas le décor**) ; 2. asset et bases de palette ;
3. tous les chargeurs rendent une carte de champs (bloc **et** constantes) ; 4. chaque objet
porte `+102/+106` — un chargeur qui ne les écrit pas ne dit rien de sa place ; 5. la
profondeur `+556` est lisible ; 6. les variantes `z` sont relevées ; 7. chaque script se
résout dans l'asset ; 8. aucune palette verte hors index 0 ; 9. les bornes du moteur ;
10. les scripts animés sont écartés de la cuisson ; 11. **sous le sprite d'un objet animé,
la page rend la banque du disque** ; 12. les objets à plusieurs scripts et ceux qui suivent
les combattants sont signalés.

**L'empreinte est l'union des pixels opaques du sprite, jamais sa boîte.** Effacer la boîte
avait vidé le décor de Yun — « il manque tous les sprites ». Et on n'efface pas l'empreinte
d'un *élément* écarté : l'élément et l'objet ne sont pas au même endroit (la charrette est
élément en 303, objet en 536).

**L'échelle des profondeurs de 2I n'est pas celle de 3SX** : reporter `my_priority` tel quel
(90, 91) place l'objet derrière nos plans, qui sont à 84/90/94 — il disparaît. Tant que la
correspondance n'est pas établie, garder `z = 0`. Voir [[reference_2i_profondeur_palette]],
[[reference_2i_copies_notre_cuisson]] et [[feedback_observation_puis_code]].
