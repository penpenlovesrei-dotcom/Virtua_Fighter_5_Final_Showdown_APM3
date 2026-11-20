---
name: project_vf5_dural
description: "VF5 APM3 — Dural est JOUABLE depuis le 2026-09-04, par patch statique seul ; sa case de grille était désactivée, pas absente."
metadata:
  node_type: memory
  type: project
  originSessionId: 7b8919f9-a3c9-4e11-a256-ad9c22b4c7e9
  modified: 2026-09-04T13:01:21.339Z
---

**Dural est jouable sur le build arcade APM3.** Vérifié à l'écran le
2026-09-04 : sélectionnable dans la grille, aucun défaut perceptible en combat.
Détail complet dans `analysis/dural.md` **section 14**, qui fait foi.

Livré **par patch statique seul** — pas de débogueur en fonctionnement, pas de
forçage d'indice à l'exécution :

    py -3 tools/patch_moteur.py --resolution 1280 720 --langue \
        --logo-japonais --dural --wxga --dural-grille

## Ce qui bloquait

Sa case n'était pas absente : elle est dans la table de disposition de la borne
(`0x1803FF0B0`, sept colonnes, trois lignes, 21 cases, Dural **en bas à
gauche**). Le jeu la construit, la dessine, puis la **désactive** —
`0x18016E20B` appelle un prédicat bouchonné, et sur son faux `0x180173F50`
marque la case du personnage 20. Le déplacement du curseur saute toute case
marquée. Trois substitutions d'appel plus quatre bornes portées à `0x14`
suffisent.

`--wxga` est nécessaire : les compositions `_dur` n'existent que dans la scène
WXGA.

## Ce que cela invalide dans les notes anciennes

- « Dural se fige sur `0x510B` » : faux. C'est son repos, `DUR_L_IDLE_TA`
  (section 11). Elle ne s'est jamais figée.
- « il manque un drapeau de profil » : bonne intuition, mauvaise cible. Le
  drapeau est le prédicat bouchonné `0x180007450` — mais il fallait le forcer
  **aux bons sites d'appel**. Ce corps est partagé par repliement COMDAT entre
  plusieurs prédicats distincts : c'est le site d'appel qui a un sens, jamais le
  corps. Il a 210 appelants ; seize dans le sélecteur.

Voir [[reference_vf5_enumeration_persos]], [[reference_vf5_yamp]],
[[feedback_cartographier_la_zone]] et [[reference_reprise_vf5]].
