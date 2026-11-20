---
name: project-sf3-dc-decors
description: Décors Dreamcast de SF3 Double Impact — format .pvc percé, 44 décors sortis, test tex_remix validé ; le doc qui fait foi est FORMAT-PVC.md.
metadata:
  type: project
---

Les décors de New Generation et 2nd Impact sont extraits et décodés — **44 décors**
(23 NG + 21 2I), pas 36 : plusieurs conteneurs en portent deux ou trois, et chez NG ce
sont les variantes d'heure du jour du même lieu. Le doc qui fait foi est
`C:\Users\frede\Downloads\3sx-outils\dc-decors\FORMAT-PVC.md` ; les rendus PNG sont dans
`dc-decors\rendus\`, les assets sprites dans `dc-decors\sprites\`.

**Assemblage vérifié** contre les décors nettoyés de sfgalleries.net : mêmes éléments aux mêmes places. Ces images sont en revanche inutilisables pour les palettes — agrandies, 1 % de leurs pixels seulement sur la grille 5 bits contre 74 % pour une capture Flycast. Elles confirment aussi qu'un conteneur à plusieurs .pvc porte les **rounds successifs** d'un décor (bg08/bg09 = Elena round 1 et 2).

Le test de bout en bout est **validé** : un décor de 2nd Impact posé sur la savane
d'Elena dans 3SX via `tex_remix`, aux bonnes places.

L'essentiel, non redérivable du code : un `.pvc` est une suite de 8192 tuiles de 16×16,
**chacune avec sa propre palette locale** (1 à 16 couleurs → 4 bits/pixel, au-delà →
8 bits). C'est ce détail qui rendait le fichier illisible comme image : il n'y a aucune
palette globale à trouver, et aucune largeur d'image ne peut marcher. Le tout est
entrelacé en ordre de Morton comme n'importe quelle texture PVR.

`bXX.pk` n'a pas d'en-tête : c'est la concaténation brute des parties, alignées au
secteur de 2048, le `.pvc` en premier à l'offset 0, les sprites animés `F_ETCnn` ensuite.

**Piège tex_remix :** une même bande de décor est chargée sous plusieurs **listes** de
textures — la savane d'Elena apparaît dans la liste 228 *et* dans la 132. N'en remplacer
qu'une fait clignoter l'image. Les retrouver par ressemblance d'image entre pages du
dump : la coupure est franche (écart < 0,8 contre > 6 pour les suivantes).

**Why:** trois hypothèses d'image (pixels directs, VQ, désentrelacement) avaient échoué
avant ; c'est la lecture du SH-4 qui a tranché, pas une n-ième conjecture.

**How to apply:** les **deux** exécutables se chargent à **0x8C010000** — c'est la clé
qui ouvre tout le reste (tables de noms, listes de chargement, désassemblage). Ils
portent aussi, pour chaque `.pvc`, sa taille et une somme de mots de 32 bits : toute
extraction se vérifie contre le jeu lui-même, et `outils/decoupe.py` le fait.
Voir [[reference-3sx-binaire]] et [[feedback-montrer-les-captures]].
