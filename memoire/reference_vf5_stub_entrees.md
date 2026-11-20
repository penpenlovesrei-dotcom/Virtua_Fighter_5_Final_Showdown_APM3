---
name: reference_vf5_stub_entrees
description: Le stub apm.dll tient la manette de VF5FS ; Input_isOn(code) à un seul argument, code 7 = START, scénario relu à chaud.
metadata:
  type: reference
---

`vfes.exe` n'a aucune source de boutons hors du stub `apm.dll` : c'est lui qui joue.

- **`char Input_isOn(int code)` — un seul argument.** `vfes.exe` publie des troncs
  (`0x140002BE0 : mov ecx, edx ; jmp [Input_isOn]`) appelés par le **moteur** via une table
  de pointeurs. Chercher des appels directs dans `vfes.exe` n'en trouve **aucun** : ce n'est
  pas la preuve d'une absence, c'est le signe qu'on cherche du mauvais côté.
- Codes 2 à 14 = bits 0 à 11 d'un masque unique (le **code 6 n'a pas de bit**) ; 0 et 15 sont
  deux cas particuliers. Le jeu interroge `isOn` pour 2 à 14 et `isOnNow` pour 0, 7, 8, 15.
- **Code 0 = TEST et code 1 = SERVICE**, les deux boutons de la borne. Vérifiés dans le menu
  opérateur, qu'on ouvre avec `test = 1` dans le scénario (`Sequence_isTest` rendu vrai).
  Le code 1 n'est interrogé **que** là.
- **Piège des menus : l'auto-répétition.** Un appui de 350 ms balaie toute la liste et ramène
  le curseur à sa place — on croit que rien n'a bougé. 80 ms = trois lignes, 40 ms = deux,
  **20 ms = une**. C'est pour cela que le stub relit son scénario toutes les **30 ms** et non
  250 : sinon aucune impulsion assez brève n'est possible.
- **Le code 7 est START** : deux appuis mènent d'un démarrage à froid jusqu'à `ROUND 1`.
  Le sens des douze autres n'est pas établi ; les balayer pendant un combat est illisible,
  l'adversaire machine agissant en même temps.
- Le scénario est dans **`apm_entrees.txt`, à côté de la DLL, relu toutes les 250 ms** : on
  presse un bouton en réécrivant le fichier, sans recompiler ni relancer (`presser.cmd`).
- **`journal = 1` fait tomber le jeu de 60 à 25 images par seconde sous débogueur** (900
  messages `OutputDebugString` par seconde). Le mettre à 0 dès qu'on ne compte plus les appels.

Voir [[reference_vf5_etat_dans_rob]] et [[reference_reprise_vf5]].
