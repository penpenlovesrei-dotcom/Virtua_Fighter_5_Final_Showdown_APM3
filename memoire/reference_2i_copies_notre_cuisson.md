---
name: reference_2i_copies_notre_cuisson
description: "Les figures fixes derrière les objets animés viennent de notre cuisson d'éléments, pas du disque."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-04T17:21:12.921Z
---

Les « copies » que Frédéric signalait sous les sprites animés de Yun **ne sont pas dans le
disque**. Mesure : la demi-banque brute (`couches2i.demi_banque('bg03', 0, 'bas')`) montre
la scène **sans** le vieil homme ni la dame en rose ; notre page cuite les contient. 40 660
pixels de différence, colonnes 128-463, **480-575** (leurs positions exactes) et 624-783.

**C'est `poser2i` qui les cuit comme éléments statiques, alors que le code les crée comme
objets animés.** On peignait la figure, puis on posait l'objet par-dessus : deux figures dès
que l'animation s'écarte de la pose peinte.

Contrôle : notre objet ne peint jamais un pixel hors de la figure (0 sur les douze images) ;
tout l'écart est de couleur et croît avec la trame — c'est l'animation, pas un décalage.

**La règle : un script que le code pose comme objet animé ne doit pas être cuit comme
élément statique.** Les deux chemins (`poser2i` et `animer2i`) doivent se partager la liste
des scripts. Voir [[reference_2i_peint_page_assemblee]] — la recherche « est-il peint ? »
reste utile, mais elle mesure notre propre cuisson tant que ce partage n'existe pas.

2I n'a **pas** de carte de tuiles : ses fonds sont des images déjà composées. Cette piste-là
est fermée.
