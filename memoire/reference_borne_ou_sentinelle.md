---
name: reference_borne_ou_sentinelle
description: "Une comparaison à N peut BORNER une table ou TESTER la valeur N ; c'est le saut qui suit qui tranche — jae/jb bornent, je/jne testent."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 75b9ae93-ca65-4776-9a1e-32941de24687
  modified: 2026-09-09T20:42:39.989Z
---

Payé à l'écran sur VF5 APM3 le **2026-09-09**, en ajoutant un décor.

Le jeu a 41 décors, indices **0 à 40**, et `0x18018EF6C : cmp edx, 0x29 ; jae`
les borne. J'ai lu « la table s'arrête à 41 » et posé le décor ajouté à
l'indice 41. Frédéric : « le décor chargé est celui d'un décor de FS chargé au
hasard ».

**41 = 0x29 est le code « décor ALÉATOIRE ».** Sept sites le testent par
**égalité** — `0x18013391E`, `0x1801744AE`, `0x1801744AF`, `0x1801748F3`,
`0x180174930`, `0x180174A4C`, `0x18001422D` — dont la case ALEA de la grille de
sélection, qui porte 41 en `+0x08` et l'icône `stage_icon_rnd_c`.

Lever la borne a rendu 41 **adressable comme descripteur sans lui retirer son
sens de sentinelle ailleurs** : le décor s'y chargeait, et le tirage au sort
aussi.

## Comment distinguer les deux

**Le saut qui suit la comparaison, et rien d'autre :**

* `jae` / `jb` / `jge` / `jl` → une **borne** ; l'agrandir est légitime ;
* `je` / `jne` → une **valeur**, une sentinelle ; l'agrandir ne la déplace pas.

Et un indice à faire résonner : une borne `cmp x, N` sur une table de N entrées
laisse **N dehors**. Si N a l'air « juste après la table », se demander à quoi
il sert — il sert souvent à quelque chose.

Deux signes étaient sous mes yeux le jour même : la garde elle-même, et mon
propre dump de la grille qui affichait `decor 41 (?)` — le `(?)` disant qu'aucun
code à trois lettres ne correspond.

**How to apply:** avant de lever une borne pour agrandir une table, balayer les
comparaisons à la même valeur et **séparer celles que suit un saut d'égalité**.
Voir [[reference_borne_ou_taille_de_tableau]] (l'autre moitié du piège : une
borne qui est en fait une taille de tableau) et [[feedback_chercher_la_borne]].
