---
name: project_vf5_knockout_trial
description: "VF5 APM3 — le KNOCK OUT TRIAL de la borne est toujours là, renommé Special Sparring ; données et analyseur intacts, seul l'habillage a été coupé."
metadata: 
  node_type: memory
  type: project
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-07T05:15:40.013Z
---

Constaté le 2026-09-07, sur demande de Frédéric. Le mode arcade
**KNOCK OUT TRIAL / KOT SPECIAL n'a pas été supprimé** du build APM3 : il y est
sous le nom **`Special Sparring`** (mode de jeu **3**).

Ce qui est intact :

* **`kotrial_enemy_data.txt`**, dans le `.par`, 303 079 o, peuplé : 171
  adversaires avec leur IA, **16 équipes `kotsp_team`** (c'est le « SPECIAL »),
  10 aires, 4 zones, 28 rôdeurs, les intrus, le PNJ du dojo ;
* son analyseur : classe **`GmKotDat`** (RTTI), chargeur `0x1800993E0`,
  analyseur `0x180099450`, déclenché à l'entrée du TERMINAL (`0x18006C2C4`) ;
* les libellés anglais dans `string_array` : `Special Sparring` (0x1A1),
  `Team Select` (0x1C8), les vingt noms d'équipes 0x592B–0x593E dont
  `KOT Trial`, et le roster (nom + deux répliques par adversaire) ;
* l'écran **`TaskMenuTeam`** (pose le mode 3 en `0x1801A4252`) et la table
  d'adversaires **`0x18040B650`** (pas 0x8E), lue par `0x1801A53A0` depuis le
  constructeur de match `0x1800B8540`.

Ce qui a été coupé **au portage PXD** (absent aussi de R.E.V.O., donc pas une
coupe de la borne) : les six tâches d'affichage du Lindbergh
(`TaskKoTrialDefeatDisp`, `IntrudeDisp`, `AdviceDisp`, `KoDisp`…), l'écran
titre `KNOCKOUT TRIAL`, les curseurs `p_trial_cursor01..10_lt`, le journal
`kot_special_mode %d`. **Le cœur reste, l'habillage est parti.**

Deux questions ouvertes, à mesurer et non à supposer : laquelle des deux
sources d'adversaires alimente vraiment le mode (le fichier ou la table
statique `0x18040B650`), et le fait que la clef **`kot_sp_npc` n'existe pas**
dans l'analyseur APM3 alors qu'elle est dans le fichier.

**Why:** l'attente naturelle était « mode arcade retiré du portage » ; c'est
faux, et le nom console masque la parenté.

**How to apply:** le document qui fait foi est
`VF5RE/analysis/knockout_trial.md`. Le maillon manquant pour remonter le mode
complet est de l'**interface**, pas de la donnée. Voir
[[project_vf5_mode_console]].
