---
name: reference_reprise_vf5
description: "VF5 : DEUX fichiers de reprise et c'est voulu — PROMPT_REPRISE.md est le briefing à coller, REPRISE.md est le journal daté. On ne les fusionne pas."
metadata:
  node_type: reference
  type: reference
  originSessionId: 3331ac98-19db-49de-a075-1d62462a23f2
  modified: 2026-09-09T05:10:32.776Z
---

Deux fichiers à la racine de `C:\Users\frede\Desktop\VF5RE\`, et **la question
« peut-on les fusionner ? » a été posée le 2026-09-09. Réponse : non, et voici
pourquoi.**

* **`PROMPT_REPRISE.md`** (~530 lignes) — le **briefing** : l'état présent, ce
  qui marche, les pièges, les outils, les chantiers ouverts. **C'est le seul à
  coller** dans une nouvelle session.
* **`REPRISE.md`** (~2 600 lignes) — le **journal** : vingt entrées datées qui
  disent *comment* on y est arrivé, et surtout *ce qui a été essayé et rejeté*.

Les fusionner ferait un premier message de 3 000 lignes — l'inverse du but — ou
perdrait l'historique des impasses, qui est précisément ce qui empêche de les
refaire (la quatrième ligne de grille, le calque 2D monté, le recyclage de
`trm`, `--decors-dural` sur `djo`).

**La règle, écrite en tête des deux fichiers :** le prompt ne raconte rien, il
renvoie au journal par date ; le journal ne résume rien, il ajoute des entrées.
Quand les deux se contredisent, **c'est le prompt qui a tort** — le journal est
écrit au moment de la mesure.

Les documents thématiques de `analysis/` font foi sur leur sujet et sont cités
par les deux : `decors.md` (le code des décors), `menu_console.md`,
`texte_2d.md`, `import_decors.md`, `ajouter_un_decor.md`, `films_usm.md`.

**How to apply:** après une séance, écrire une entrée datée dans `REPRISE.md`
et ne toucher au prompt que pour l'**état** (tableaux, pièges, chantiers).
Voir [[feedback_ne_pas_defaire_le_valide]] : une validation à l'écran s'écrit
comme une recette le jour même. Même convention que
[[reference_reprise_chantier]] pour les décors DC. Voir [[project_vf5_re]].
