---
name: feedback_registre_pas_regle
description: "« Ne fais jamais de supposition » — une regle qui devine se remplace par un registre de ce qui a ete vu, pas par un meilleur critere."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-10T21:29:42.381Z
---

Frederic, 2026-09-10 : « ne fait jamais de supposition, il y a des eclairs dans
le decor de Goh en version R qui n'ont rien a y faire ».

**Why:** j'avais ecrit dans `patch_moteur.animations_en_plus()` une REGLE :
« ajouter toutes les animations de 2008 que le modele ne demande pas, sauf
celles qu'un autre mecanisme joue ». Je l'avais meme etiquetee « PREMISSE, pas
une mesure » — ce qui ne l'excuse pas, ca l'aggrave : je savais et j'ai livre.
La liste auth_3d d'un decor est la liste de ce qui tourne EN BOUCLE ; y verser
une animation, c'est DECIDER qu'elle est une boucle. Sur `hi5` (Broken House),
`LIHGT` et `SKY_HIKARI1` sont des coups d'une seconde : ils clignotaient sans
arret.

**How to apply:** quand une regle qui devine se fait prendre, ne pas chercher un
critere plus fin -- ce serait la meme faute mieux habillee. (Ici la duree
declaree dans le `.a3da` semblait discriminer, ARUKI 65 s contre LIHGT 1 s,
mais `DENKI_B` fait 2,7 s et le jeu le joue bien en boucle : ca ne PROUVE
rien.) Supprimer la regle, revenir au defaut sur -- le decor ajoute joue
exactement ce que son modele demande -- et ouvrir au cas par cas dans un
REGISTRE dont chaque entree porte la date et la phrase de validation.
`ANIMATIONS_VALIDEES` en est un. L'outil doit NOMMER ce qu'il n'a pas joue,
pour que rien ne se reperde.

Voir [[feedback_premisse_qui_borne]], [[feedback_lire_le_code_pas_l_image]],
[[feedback_visuel_avant_validation]], [[reference_vf5_taches_effet]].
