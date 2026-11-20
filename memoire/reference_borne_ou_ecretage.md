---
name: reference-borne-ou-ecretage
description: "Une borne peut être un `cmov` avec valeur de repli, invisible pour qui énumère les lecteurs d'une table ; et `cmova` est non signé, donc -1 y est « trop grand »."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4a9d6ee7-5058-40ad-8b84-68b1840c1e36
  modified: 2026-09-10T06:17:35.375Z
---

Troisième forme de la famille, après [[reference_borne_ou_sentinelle]] (`jae`
borne, `je` teste une valeur) et [[reference_borne_ou_taille_de_tableau]] : une
borne peut être un **écrêtage sans branchement**.

VF5 APM3, `0x180203F1E` : `cmp ebp, 0x28` puis `0x180203F2E cmova ebp, eax`
avec `eax = 39` — tout indice de décor au-dessus de 40 devient `gym`,
silencieusement, **deux appels avant** que `TaskStage` en entende parler. Les
six bornes déjà levées avaient été trouvées en énumérant les *lecteurs des
tables de décors* ; celle-ci ne lit aucune table, donc aucune énumération de ce
type ne pouvait la rendre.

Deux pièges dans un :

* **la forme.** Chercher `jae`/`jb` devant une lecture de table ne trouve pas un
  `cmp`+`cmov`. Balayer aussi cette forme (quinze sites dans ce binaire, un seul
  pertinent) ;
* **le signe.** `cmova` est **non signé** : `-1` (« aucun choix ») y vaut
  `0xFFFFFFFF`, donc « au-dessus de 40 », donc remplacé par le repli. Un
  écrêtage a donc DEUX correctifs distincts — la borne, et la valeur de repli.

**Pourquoi :** un indice qui ne survit pas au trajet n'est pas forcément rejeté
par un test ; il peut avoir été remplacé par un `cmov`, sans saut, sans message.

**Comment l'appliquer :** quand une valeur arrive fausse au bout d'une chaîne,
suivre la chaîne par énumérations complètes de références (un global n'a souvent
que quatre ou vingt références, là où l'offset générique en a deux cents), et se
demander à chaque maillon ce que devient `-1`.
