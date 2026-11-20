---
name: project-oro-menagerie
description: La ménagerie d'Oro n'a aucun bloc — ses bêtes ont leurs champs en immédiats dans le spawner.
metadata:
  type: project
---

Le chat, le chien et le perroquet d'Oro (SF3 2nd Impact) **n'ont aucun bloc
d'enregistrements**. On en a cherché un pendant des semaines, et trois enregistrements
avaient été essayés au jugé puis rejetés à l'écran.

Leur spawner écrit `x`, `y`, `palette`, `plan` et la table de scripts en **immédiats**, et
le numéro de script est posé par la **routine** de l'objet, pas par une donnée. La routine
d'étage d'Oro `0x8C0DE548` les appelle en clair : id 55 le perroquet (`0x8C030546`),
id 72 le gros chat (`0x8C0338E8`), id 71 le chien (`0x8C03369E`), id 74 les chauves-souris
(`0x8C033FC2`, qui, lui, a un bloc).

Et les **chatons** (id 73) ne sont pas créés par la routine d'étage : c'est le spawner du
**chat** qui les crée en dernier geste (`jsr 0x8C033ACC`). La mère fait ses chatons, et ils
sont posés à côté d'elle. Toute la ménagerie est donc placée -- posée le 02/09/2026,
jamais vue à l'écran.

**Pourquoi :** deux leçons dépassent Oro — *un objet n'a pas forcément de bloc*, et *un
objet peut être créé par un autre objet* plutôt que par la routine d'étage. Une remontée
qui ne vise que les routines d'étage déclare « aucun chemin » alors qu'il passe par un
frère.

**Comment l'appliquer :** chercher qui charge la table de scripts du décor
(`0x8C12AB8C` pour Oro) — les fonctions qui la portent **sans lire de bloc** sont les
spawners à immédiats. Voir [[reference-remonter-graphe-appels]] et
[[reference-decors-doc-unique]].
