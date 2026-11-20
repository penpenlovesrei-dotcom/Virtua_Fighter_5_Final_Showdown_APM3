---
name: project-shin-akuma-build
description: "La build a part de Shin Akuma : worktree C:\\Temp3sx-shin, branche shin-akuma, personnage 20, ca demarre mais personne ne l'a encore vu."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1b6a7297-36d0-4db2-9df6-56a319b1221c
  modified: 2026-09-01T20:36:36.323Z
---

Ouvert le 01/09/2026, apres l'arbitrage de Frederic : **Shin Akuma prend le numero 20**
(en fin de liste, pas sa place d'arcade 15), et **sur une build a part**.

* arbre de travail `C:\Temp3sx-shin` (git worktree, branche `shin-akuma`) — `C:\Temp3sx`
  et son exe ne sont pas touches ;
* jeu dans `C:\Temp3sx-shin\jeu\`, lanceur `SHIN AKUMA - premier essai.cmd` ;
* les deux builds partagent `resources\`, ou une seule chose a ete **ajoutee** :
  `sfiii3nr1.zip` (la build habituelle ne la lit pas, `arcade-balance` etant faux).

**Why :** ses donnees de personnage n'existent que dans la ROM d'arcade, donc le portage
doit la lire ; et une centaine de tableaux indexes par le personnage ont du passer a 21
entrees, la 21e recopiee d'Akuma — sauf `pl_nr_piyo_tbl` (2978, pas 2849).

**How to apply :** l'etat complet, ce qui est fait et ce qui reste, est dans
`Downloads\3sx-outils\shin-akuma\BUILD.md`. **Personne ne l'a encore vu a l'ecran** : le
premier essai est le prochain pas, cf. [[feedback-visuel-avant-validation]]. Rien n'est
commite. Voir [[project-shin-akuma]] pour la demonstration, et
[[reference-tables-indexees-par-etage]] : le meme motif s'applique aux tables indexees
par le personnage, certaines plantent SANS message.
