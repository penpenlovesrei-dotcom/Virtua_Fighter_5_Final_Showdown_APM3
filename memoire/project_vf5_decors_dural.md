---
name: project_vf5_decors_dural
description: "VF5 — les cinq décors de Dural existent tous ; le choix parmi eux était un bouchon rendant toujours DU2. Corrigé par --decors-dural, jamais vu à l'écran."
metadata: 
  node_type: memory
  type: project
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-08T21:22:13.504Z
---

**Les cinq se choisissent au SELECT depuis le 2026-09-08** (lanceur
`tools\variantes.cmd`, option `--variantes`) : le curseur reste sur UNE case et
la barre espace fait défiler l'anneau. Frédéric a chargé DU4 — validé.
Nommage : du1 SNOW, du2 ECLIPSE/METEOR, du3 SUBMERSION, du4 STORM, du5 SPACE ;
**il manque NIGHT, DAY, SUNSET**. La 4e ligne de cases essayée avant a été
REFUSÉE ; voir [[reference_vf5_greffe_section]].

**Le NOM de la variante à l'écran** (`--variantes-texte`,
`tools\variantes_texte.cmd`) est écrit par le créneau 4 de `TaskSelStage`, en
neuf passes pour le liseré. Il a coûté six essais et deux plantages — pointeurs
absolus dans une greffe rebasée, puis montée du calque 2D hors du tableau de
compartiments. Corrigé, **pas encore vu à l'écran** ; voir
[[reference_vf5_texte_2d]]. Reste ensuite la ligne de génération
`Virtua Fighter 5 / 5R / Final Showdown` sous la mention de taille.

Livré le 2026-09-07, lanceur **`tools\decors_dural.cmd`**.
**Frédéric a vu les décors de Dural fonctionner** — `--decors-dural` est validé
à l'écran. `--decors-dural-grille` (la grille de sélection) est en place mais
**n'a pas encore été vu**.

**Croisé avec le build Yakuza 6 le 2026-09-09** — voir
[[reference_vf5_build_yakuza6]]. Le forçage se scinde en deux, et la nuance
compte : le **bouchon du combat** (`mov eax,0x16 ; ret`) est dans les **DEUX**
builds, donc « toujours DU2 en combat » n'est pas une amputation de la borne ;
les **trois sites d'écran sont propres à l'APM3** (balayage exhaustif : 3 chez
nous, 0 chez Yakuza 6). Et la **collision de DU2** est la seule vraie
régression de données : Yakuza 6 pointe `STGDU2_COLI.000.bin`, nous
`STGDU1_COLI.000.bin` — `--du2-collision` est donc validé par un build
indépendant, et le fichier lui-même est identique au SHA-256 près.

Le forçage « du1 → du2 » était **QUADRUPLE** : `0x1800B2330` (le combat, un
bouchon `mov eax,0x16 ; ret`), **`0x180174494`** (l'immédiat dans
`TaskSelStage::update` — **c'est lui qui décide du décor réellement chargé**),
`0x18017533D`/`0x180175344` (l'écran) et `0x1801753A8` (le chemin APM3, un
`cmove`). J'en ai trouvé trois en cherchant site par site ; le quatrième n'est
sorti qu'après un essai de Frédéric (« DU1 = DU2 »).

**`tools/substitutions.py <source> <cible>` les énumère d'un coup** — écrit
pour ça. `0x15 0x16` en rend quatre, plus un faux positif (`cmp rax, 0x16`, une
borne de boucle). Chercher au symptôme en avait laissé un ; voir
[[feedback_cartographier_la_zone]].

La forme la plus sûre est de changer **l'immédiat** (`0x16` → `0x15`) et non de
détourner le saut : le bloc s'exécute à l'identique, aucun flot modifié, un
octet.

Le décor d'un combat solo est le **décor maison de l'adversaire**
(`rom/game_score.txt`, voir [[reference_vf5_index_decor_game_score]]). Quand ce
décor est celui de Dural (21 = du1), le jeu appelle `0x1800B2330` pour choisir
parmi les cinq — et `0x1800B2330` fait six octets : `mov eax, 0x16 ; ret`,
**toujours DU2**. Un seul appelant, argument ignoré. Les cinq décors sont dans
le jeu, entiers ; un seul était atteignable.

Le correctif réécrit `0x1800B8B02`–`0x1800B8B20` **en place**, 31 octets, sans
caverne : `cmp eax,lo ; jl fin ; cmp eax,lo+4 ; jg fin ; add eax,21-lo ; fin:`.
Par défaut `lo = 7` → **cas riv jin sin djo → du1..du5**, soit les décors de
Lion, Shun Di, Aoi, Lei-Fei, Akira.

Deux pièges évités, à ne pas réintroduire :

* `0x1800B8B21` (`mov r12d, eax`) doit rester : la voie License Challenge y
  saute depuis `0x1800B8A2D`. L'écraser aurait cassé ce mode **sans un seul
  message** — voir [[feedback_garde_partagee]].
* la translation agit **avant** que l'index ne devienne le décor courant, donc
  les cas particuliers indexés du chargeur (8 et 9 dans `0x18018F030`, 16 et 40
  dans `0x18018FAC6`) ne se déclenchent pas sur les décors traduits.

`--decors-dural-grille` lève les deux forçages de l'écran (`0x18017533B` : le
`jne` devient un `jmp`, **un octet** ; `0x1801753A8` : le `cmove` devient trois
`nop`) et convertit quatre cases de la grille (riv jin sin djo → du2 du3 du4
du5), la case `dur` gardant du1 — les cinq y sont sans doublon. Les **icônes**
des quatre cases ne changent pas, exprès : c'est ce qui permet de dire quelle
case on a prise.

**Les cinq sont cinq variantes du MÊME lieu** — le SANCTUARY de VF5 vanilla
(2007). R.E.V.O. les nomme d'ailleurs `st_vf5_sanctuary1..5.par`. Les planches
de textures le montrent : `stgdu1` et le `stgdur` de ver.B portent les mêmes
atlas (colonnes, arches, remplages, dallage). Voir
[[reference_vf5_objset_lecture]] pour l'outil, et
`analysis/dural_nuit_le_point.png` pour l'image.

**Le décor de nuit étoilée que cherche Frédéric n'est pas un sixième décor** :
c'est ce même SANCTUARY, dont le CIEL a changé. Chaque décor n'a qu'**un seul**
objet de ciel (`stgduN_sky`), et celui de du1 en FS porte une texture de ciel
de JOUR nuageux. Deux inventaires antérieurs, faits au balayage d'ASCII
(« du2 = la nuit étoilée », « 24 objets de ciel `sky10`…`sky32` »), étaient du
BRUIT : voir [[feedback_lire_le_code_pas_l_image]] — un nom se lit dans sa
table, pas dans le tas d'octets.

**Pourquoi le moteur forçait du2** : R.E.V.O. nomme ses décors
`st_vf5_sanctuary1..5.par`, et **seul `sanctuary2` fait 40 Mo, les quatre
autres sont des souches de 190 Ko**. Les cinq Dural sont « Sanctuary 1 à 5 »,
et les portages modernes n'en livrent qu'un. APM3 les a **tous les cinq** en
entier (24–28 Mo) : c'est ce qui rend le correctif possible.

**L'écran de sélection s'affiche** (capture du 2026-09-07) : `STAGE SELECT`,
3 × 7 cases. Deux choses à savoir avant de s'en étonner :

* **les cinq décors de Dural ont le MÊME aperçu**, par construction : la liste
  de `0x180174BF0` leur associe la même planche AET `dur`/`dur_stay`, et la
  légende « Sanctuary / Single Wall 16x16 » y est **peinte** (aucun libellé
  correspondant dans `string_array`). Ce n'est pas un bug ;
* **du2 embarquait la collision de du1** — défaut du build d'origine :
  `STGDU2_COLI.000.bin` existe dans le `.par` (3 984 o contre 5 744) mais la
  chaîne `rom/STGDU2_COLI.000.bin` n'a jamais été émise. Symptôme relevé par
  Frédéric : en ring out, le personnage se pose sur un sol inexistant.
  `--du2-collision` écrit la chaîne dans le **mou de fin de `.rdata`**
  (`0x180641B56`, 170 o à zéro, projeté en mémoire) — aucune caverne `int3` ne
  faisait 24 octets, la plus grande en fait 21.

**How to apply:** pour voir les cinq — le DOJO est le plus commode, le décor
suit le personnage du **partenaire** (Lion / Shun Di / Aoi / Lei-Fei / Akira) ;
sinon Arcade route A, combats 3, 4, 6, 7 et 8. Le combat contre Dural rend
désormais DU1. Documents : `analysis/decors.md` §8 bis,
`analysis/ajouter_un_decor.md`.
