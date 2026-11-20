---
name: reference_vf5_ecran_noir
description: "VF5 APM3 — l'écran noir entre le titre et la sélection est APM3_ENTRY ; le sauter fait planter, il faut le traverser par une impulsion START."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 22b68e08-364a-4b50-b67a-c1f1efec0229
  modified: 2026-09-03T18:04:11.849Z
---

L'écran noir entre l'écran-titre et la sélection des personnages est
**`APM3_ENTRY`** (sous-état 48), l'attente de la borne. Il ne dessine rien parce
que son contenu dépend du lecteur de carte et de l'afficheur de crédits que
notre `apm.dll` ne fournit pas. **Ce n'est pas le menu PS3** : l'état de tête
reste `APM3`, il ne devient jamais `MENU`.

Mesuré en direct pendant que Frédéric y était :

```
1  [t= 12,4 s]  STARTUP -> APM3     CS_TITLE   -> MAX
2  [t= 72,5 s]  APM3 -> STARTUP     APM3_ENTRY -> CS_TITLE   <- repart seul apres ~60 s
4  [t=113,5 s]  APM3 -> MAX         APM3_ENTRY -> APM3_SELECTOR
```

**Le sauter fait planter.** `--sauter-entry` (forcer le sous-état à
`APM3_SELECTOR` en entrant dans `APM3`) provoque une **violation d'accès
immédiate à `moteur+0xB1D33`**, en première puis en seconde chance, et le
processus meurt. `APM3_ENTRY` prépare donc quelque chose dont la sélection a
besoin — et `moteur+0xB1D33` nomme l'endroit exact où ça manque.

**La solution qui marche : le traverser.** `tools/tracer_etats.py --passer-entry`
écrit une directive dans le fichier d'entrées dès que le jeu entre dans `APM3` ;
le stub appuie sur START. Un seul appui humain au lieu de deux, plus d'écran
noir, plus de retour au titre. Vérifié à l'écran : « c'est parfait ».

Cela a demandé une nouveauté dans le stub, l'**impulsion à usage unique** :

```
impulsion = start
duree = 150
```

Elle presse les codes pendant N ms **à partir du moment où la ligne est lue**.
C'est le déclencheur qui manquait : les pas d'un scénario sont datés depuis le
premier sondage d'entrée, instant qu'un outil extérieur ne connaît pas. Ici
c'est la **date du fichier** qui déclenche — l'écrire suffit.

Réserve : cela passe par le débogueur, un seul point d'arrêt sur `SetState`
(pas dans une boucle chaude, donc sans ralentissement). Pour un patch statique
il faudrait comprendre ce qu'`APM3_ENTRY` initialise. Voir
[[reference_vf5_machine_etats]].
