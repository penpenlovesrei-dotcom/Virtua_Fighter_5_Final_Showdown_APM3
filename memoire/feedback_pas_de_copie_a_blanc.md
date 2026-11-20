---
name: feedback-pas-de-copie-a-blanc
description: "Ne jamais « tester à blanc » un script destructeur en le réécrivant par substitution puis en l'exécutant ; il supprime pour de vrai si un motif rate."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 09665412-af58-4b1f-b0e7-e8036bd15ccf
  modified: 2026-09-11T13:22:52.461Z
---

Le 11/09/2026, pour vérifier la syntaxe d'un `.cmd` de suppression, j'en ai fait une copie
où `sed` devait remplacer chaque commande destructrice par un `echo`, puis je l'ai lancée
DANS LA MÊME commande. Le motif `git -C "C:\\Temp3sx" worktree remove` n'a pas matché (échappement
des antislashs), et `rmdir "C:\stage..."` non plus : trois worktrees (3sx-p, 3sx-r, 3sx-t)
et seize dossiers vides ont été supprimés alors que Frédéric n'avait demandé qu'une LISTE.
Rattrapé parce que le patch de 3sx-t existait déjà : sources remises à l'identique,
build/ et third_party/ perdus.

**Why:** ma propre sortie affichait les lignes non neutralisées juste avant l'exécution ; enchaîner
contrôle et exécution a rendu le contrôle inutile.

**How to apply:** un script destructeur ne s'exécute jamais, même « à blanc ». Si on veut vérifier
sa syntaxe, écrire un script de test DISTINCT qui n'appelle que `echo`, ou relire. Et si une
transformation doit neutraliser, vérifier son résultat dans un appel séparé, avant tout lancement.
Voir aussi [[feedback-demander-confirmation]].
