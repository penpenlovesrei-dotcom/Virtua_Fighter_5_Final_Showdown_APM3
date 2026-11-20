---
name: reference_vf5_sonde_decor
description: "tools/sonde_decor.py force un décor, mène VF5 seul au combat et capture : voir un décor ajouté sans que Frédéric navigue."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-11T19:16:02.877Z
---

`py -3 tools/sonde_decor.py <indice> --toutes 4 --depuis 72 --secondes 150`
force le décor `<indice>` au seul point où le gestionnaire consomme la
demande (`0x18018EF40`, écrit dans `[rcx+0x60]`), joue un scénario de START
par l'apm.dll de substitution (Arcade, combat en rounds contre l'ordinateur),
capture dans `analysis/sonde/`. Options : `--fichiers fog_,light_param`
(CreateFileW), `--bp 0x180072BA0:nom[:adresse mémoire]` (espions, registres).
Remet le scénario manuel (`apm_entrees.txt`) après. ~2 min 30 par décor.

Pièges payés : fenêtre d'appui de 10 ms → appuis perdus sous débogueur
(20 ms) ; la navigation peut finir au DOJO (pas de rounds) si un appui
tombe mal — refaire. Le jeu doit être fermé (la sonde refuse sinon).
Windows MÉMORISE la sourdine par application : le jeu est resté muet à la
main après les sondes (« réactive le son du jeu », 2026-09-11). Depuis,
`instrument._rendre_le_son` la lève avant de fermer le jeu ; si le jeu s'est
arrêté seul, `py -3 tools/muet.py --rendre` pendant qu'il tourne.

**How to apply:** avant de conclure sur un effet visuel ou un fichier d'un
décor ajouté, le VOIR à la sonde ; les captures servent à l'analyse, c'est
Frédéric qui valide. Voir [[feedback_lire_le_code_pas_l_image]],
[[reference_vf5_cablages_numero]].
