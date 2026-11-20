---
name: reference-sf3-dc-fetc
description: Les deux décompresseurs des sprites F_ETCnn de SF3 Dreamcast — 3772 blocs sur 3772, sortie 4096 octets à rebours.
metadata:
  type: reference
---

Les blocs graphiques des assets `F_ETCnn` (sprites animés de décor) se décompressent par
**deux schémas** trouvés dans `SF3_2ND.BIN`. Les deux rendent **4096 octets écrits à
rebours** depuis la fin du tampon — le code fait `mov.b rX,@-r5`, c'est le point qui
rend le format incompréhensible tant qu'on le lit à l'endroit.

- **Schéma A, `0x8C0F6548`** — octets de commande avec table circulaire de 16 valeurs
  récentes initialisée à `1..16`, et `dernier` initialisé à **17**.
- **Schéma B, `0x8C0F663C`** — RLE à drapeaux, 512 tours de 8 sorties.

Rien dans les données ne dit lequel s'applique : on essaie les deux, et la double
contrainte (consommer tout le bloc **et** remplir exactement 4096) tranche. Sur les
3772 blocs des deux jeux : 3688 en A, 84 en B, aucun échec. Les 84 sont tous dans
`ng-b02-F_ETC35`.

Les 4096 octets sont **16 tuiles de 16×16 en 8 bits, lues ligne par ligne** — pas
d'entrelacement, contrairement aux pages `.pvc` du même jeu. Mesuré sur 4456 tuiles.

**Why:** trois pistes ont été perdues avant d'y arriver — les stores voisins de la
table, une routine de cache, une routine de nettoyage.

**La banque de palettes** est dans l'exécutable : 64 couleurs ARGB1555 par palette
(128 octets), `SF3_2ND.BIN` à `0x1D9AEC` (2715 palettes), `SF3_1ST.BIN` à `0x1A8188`
(2661). Trouvée en remontant depuis `0x005F9000`, la palette RAM du PowerVR.
La banque est **rangée par décor**, en plages contiguës et croissantes. Pour la
retrouver sans lire de code : compter, pour chaque palette, la part de ses 64 couleurs
présentes **à l'identique** dans le `.pvc` du décor — ~100 % pour les bonnes, 8 % de
moyenne. `outils/appariement.py` fait le tableau.

Ce qui manque encore : **laquelle de ces palettes va avec quel sprite**. L'index n'est
ni dans le conteneur (champs 0, 3 et 5 des animations nuls sur 16320 enregistrements),
ni référencé par adresse (les deux tables de copie `0x1CB850` et `0x1D4FD0` ne servent
qu'aux personnages). Il est calculé dans le code. La déduction directe est exclue :
aucune tuile de sprite n'apparaît dans le décor de son étage.

**How to apply:** ce qui a marché est une recherche mécanique : balayer tous les
`mov.l Rm,@(8,Rn)` du code et ne garder que ceux dont la source vient d'un pool
contenant une adresse de code. 29 candidats, dont le bon. Pour la palette, même
principe en partant de l'adresse matérielle. Voir [[project-sf3-dc-decors]] et
`dc-decors/FORMAT-PVC.md`.
