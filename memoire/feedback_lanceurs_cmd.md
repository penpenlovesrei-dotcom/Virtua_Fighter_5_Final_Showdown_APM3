---
name: feedback-lanceurs-cmd
description: "Toujours livrer un lanceur .cmd à double-cliquer, jamais une ligne de commande à recopier."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7d3168ca-275c-4d30-8e06-abc13121b915
  modified: 2026-08-12T18:08:05.161Z
---

Frédéric ne veut **jamais** de ligne de commande à recopier. Chaque manipulation
qu'il doit lancer se livre sous forme d'un fichier `.cmd` à double-cliquer, à la
racine du dossier de jeu (`C:\Users\frede\Documents\SEGA Model 3\`).

**Why:** demandé explicitement — « jamais de ligne de commande ». Les lignes
qu'on lui a données ont d'ailleurs échoué en pratique : lancée depuis le mauvais
dossier, Supermodel ne trouve ni `Config\` ni `ROMs\` et ouvre SuperSetup.

**How to apply:** un `.cmd` par manipulation, sur le modèle de ceux qui existent
(`Tester HD.cmd`, `FV2 - Journal entrees.cmd`, `FV2 - Menu console.cmd`). Il
commence par `cd /d "%~dp0"`, vérifie que le binaire et la ROM existent, affiche
les touches et **ce qu'il faut observer**, puis lance. Voir
[[reference_supermodel_binaire]].

**Ne jamais editer un `.cmd` pendant qu'il tourne.** `cmd.exe` relit le fichier
au fur et a mesure en retenant un **offset en octets** : si le fichier grossit
pendant que le batch est bloque sur la ligne du jeu, l'offset ne tombe plus au
meme endroit et la fin du fichier est rejouee — le jeu **se relance tout seul**
des qu'on le ferme. Vu le 2026-08-22 sur `VF3 - Dural jouable.cmd` (lanceur
demarre a 12:50, edite a 12:52, jeu ferme a 12:55, relance immediate par le
meme `cmd.exe`). Attendre la fermeture du jeu pour modifier son lanceur.
