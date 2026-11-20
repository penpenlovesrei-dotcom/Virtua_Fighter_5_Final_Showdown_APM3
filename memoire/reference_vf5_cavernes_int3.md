---
name: reference_vf5_cavernes_int3
description: "Les bourrages int3 donnent de la place à volonté dans le moteur VF5, et deux correctifs peuvent se disputer une caverne en silence."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 61cff823-927b-4eea-81b1-5063c9d15cce
  modified: 2026-09-07T04:49:50.377Z
---

Le moteur APM3 n'a pas « quatre cavernes pleines » : MSVC aligne ses fonctions
à 16 octets et remplit l'écart avec `0xCC`. Il y a **1431 plages d'au moins 14
octets**, dont plusieurs de 21. Une plage se prouve libre en vérifiant qu'elle
ne tombe dans aucune des 13 661 entrées de `.pdata` et qu'elle finit sur une
frontière à 16. Une chaîne de caractères peut y vivre aussi : `.text` est
lisible.

**Le piège qui a coûté License Challenge** : `patch_moteur.py` vérifie les
octets attendus dans `.origine`, **jamais dans le fichier en cours
d'écriture**. Deux options peuvent donc écrire à la même adresse sans qu'aucune
ne proteste — c'est arrivé entre `--sp-lancer` et `--legende-sousmenu`, tous
deux logés en `0x1801A71D8` ; la seconde écrasait la première, et le mode était
cassé sans un seul message. Le garde-fou est désormais `_poser()`, un journal
des octets écrits qui refuse toute collision ; une reprise volontaire de site se
déclare avec `reprise=True`.

Voir [[reference_reprise_vf5]] et [[feedback_verifier_le_build]].
