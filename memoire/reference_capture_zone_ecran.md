---
name: reference_capture_zone_ecran
description: Une capture « de fenêtre » par BitBlt photographie la zone d'écran, donc la fenêtre qui est devant — vérifier le premier plan.
metadata:
  type: reference
---

`tools/capture_fenetre.py` (VF5RE) capture par `BitBlt` du bureau, parce qu'un rendu Direct3D
ne se recopie pas par le DC de la fenêtre. **On photographie donc la ZONE D'ÉCRAN qu'occupe la
fenêtre, pas la fenêtre.** Si une autre fenêtre la recouvre, c'est celle-là qu'on enregistre —
c'est-à-dire l'écran de Frédéric.

Cela a déjà coûté une passe entière de mesures : dix captures « du jeu » montraient en fait une
vidéo qui tournait par-dessus, et l'outil a rendu un verdict « les dix codes déplacent le
curseur » entièrement faux.

**Toujours vérifier `GetForegroundWindow()` avant de déclencher**, ou mettre la fenêtre devant.
Et si l'utilisateur se sert de sa machine, ne pas lui voler le premier plan : préférer une
mesure en mémoire, qui ne capture rien. Les captures involontaires se suppriment.

Voir [[feedback_montrer_les_captures]].
