---
name: reference_vf5_index_decor_game_score
description: "VF5 — le décor d'un combat vient de rom/game_score.txt (décor maison de l'adversaire), pas du code ; 0x29 = aléatoire, résolu dans l'écran de sélection."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-07T05:15:22.064Z
---

L'index de décor d'un match vit dans les **paramètres de partie, `+0x4C`**
(accesseur feuille `0x1800B48D0`). Sa valeur de repos, posée par la remise à
zéro `0x1800B56C0`, est **`0x29` = 41 = « aléatoire / non choisi »** — hors des
41 décors 0..40, donc `0x18018FCF0` la refuse et aucun décor n'est demandé.

**En solo, le décor est celui de l'adversaire**, et ce n'est pas une constante
du code : `0x1800AF400(personnage)` interroge le singleton `GameScoreSetting`
(`0x1806F9C10`), qui analyse **`rom/game_score.txt`** — un fichier en clair du
`.par` :

    score.chara.8.name=LIO    score.chara.8.stage=STGCAS
    score.route.0.enemy0.name=BRA ...        (les trois routes A/B/C)

Le nom `STGCAS` est converti en index par `0x18018F590` (strcmp sur les 41
descripteurs). **Changer les décors des routes ne demande donc aucun patch de
code** — seulement d'éditer ce fichier, par la voie `tools/par_masquer.py`.

Le `0x29` « Random » est résolu **dans l'écran** `TaskSelStage` avant d'être
posé (`0x18017474E : si curseur == 0x29, prendre [obj+0x60]`). Il n'atteint
jamais [[reference_vf5_gestionnaire_decor]].

**Why:** j'ai cherché longtemps un tirage au sort dans le moteur ; il n'y en a
pas à cet endroit, et la « sélection » est pour l'essentiel une donnée de
fichier.

**How to apply:** pour forcer un décor, viser `[params+0x4C]` ou
`0x18018FCF0` — un seul point. Pour changer l'association décor↔personnage,
éditer `game_score.txt`. Détail complet dans `VF5RE/analysis/decors.md`.
