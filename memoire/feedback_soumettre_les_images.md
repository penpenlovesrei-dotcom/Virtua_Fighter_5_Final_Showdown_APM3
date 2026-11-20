---
name: feedback_soumettre_les_images
description: "Frédéric tranche lui-même sur les captures — je les soumets sans verdict, je ne conclus pas à sa place."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 22b68e08-364a-4b50-b67a-c1f1efec0229
  modified: 2026-09-03T07:33:04.834Z
---

**« tu vas arrêter de juger les images, tu me les soumets avant »** — dit le
2026-09-03 pour le chantier résolution de VF5, après que je me sois trompé
**trois fois de suite** en lisant un succès sur une capture :

1. un décor « importé » jugé bon — alors que le sélecteur de décor est par défaut
   sur **Random** et que j'ignorais lequel s'était chargé ;
2. le 720p déclaré correct parce que l'ATS était bien mis en page — « le mode
   720p est zoomé sur toutes tes captures », puis une seconde fois « tes
   conclusions sur les images sont fausses, le jeu est toujours zoomé » ;
3. le menu console déclaré affiché — « c'est un écran de loading ».

**Why :** une capture prouve qu'il s'est passé *quelque chose*, jamais *quoi*.
Et sur un jeu de combat, le cadrage change à chaque instant : deux captures
prises au même temps dans deux exécutions ne sont pas comparables (mesuré :
corrélation 0,05 entre deux passes du même scénario). Mon jugement visuel a
coûté trois allers-retours ; le sien tranche en une phrase.

**How to apply :**

- **Livrer la capture, décrire le réglage, et s'arrêter là.** Pas de « ça
  marche », pas de « le cadrage est correct », pas de « ça a l'air bon ».
- Dire ce qui est **mesuré** — « aucune cible de rendu ne reste en 1920×1080 »
  — et laisser l'image parler pour le reste.
- Si un doute visuel se pose, chercher l'instrument : ici c'était le point
  d'arrêt sur `CreateTexture2D`, qui donne la taille réelle de chaque cible et
  qui a révélé en une passe ce que six captures avaient laissé ouvert.

Voir [[feedback_lire_le_code_pas_l_image]] et [[feedback_montrer_les_captures]] :
toute capture se montre, même ratée — et désormais, sans conclusion attachée.
