---
name: reference-sf3-dc-palettes
description: Chemin des palettes de SF3 Dreamcast — banque dans l'exe, et la règle base+offset qui donne la palette d'un morceau de sprite.
metadata:
  type: reference
---

**La banque de palettes** est dans l'exécutable : 64 couleurs ARGB1555 (128 octets) par
palette. `SF3_2ND.BIN` à `0x1D9AEC` (2715 palettes), `SF3_1ST.BIN` à `0x1A8188` (2661).
Elle est **rangée par décor**, en plages contiguës et croissantes ; pour retrouver la
plage sans lire de code, compter la part des 64 couleurs présentes à l'identique dans le
`.pvc` du décor — ~100 % pour les bonnes, 8 % de moyenne. `outils/appariement.py`.

**Le chemin PowerVR.** Les tuiles de sprite sont en **PAL8** (`0x30000000`), sélecteur
`0x04000000` = banque 2, soit l'entrée 512 de la palette RAM. La palette RAM
(`0x005F9000`, 1024 entrées) se remplit par deux voies : entrées 0–511 en bloc depuis
`0x8C84FFC0` (fonction `0x8C0F607C`), entrées 512–1023 par 8 emplacements de 64
(`0x8C6D6BAC`, vidange `0x8C0F594A`). Seul l'emplacement 0 bouge en jeu, et c'est un
cyclage de couleurs. Les couleurs viennent de la palette RAM propre au jeu,
`0x8C828CD0`, converties par `0x8C0F6048`.

**CORRIGÉ le 27/08/2026 — il y a bien un index dans les données.** Le champ palette d'un
morceau de sprite (octets 2–3 du morceau de 8 octets) vaut `drapeaux << 9 | offset`, et
la palette réelle est **`base(décor, drapeaux) + offset`**. Les bases sont les sources
des transferts de la table `0x1D4DBC` de `SF3_2ND.BIN`, enregistrements de 12 octets
`{u32 destination, u32 adresse de palette, u32 taille}` — l'adresse se convertit en
numéro par `(adresse - 0x02798000) / 128`. Deux familles : le **bloc propre au décor**
(64 palettes, une entrée par décor, qui coïncide avec la plage de fond mesurée) et un
**bloc partagé** de 80 à 100 palettes (sources 1625 à 1674) où vivent les figures
humaines que plusieurs décors se prêtent. Les 15 palettes confirmées par capture
retombent toutes dessus, exactement. Table : `outils/bases.py`, démonstration
`dc-decors/ASSEMBLAGE.md`.

Ce qui reste dynamique, c'est seulement **quelle base va avec quel décor** : la
résolution passe par une table RAM de 512 octets à `0x8C6D57E0` (lue en `0x8C0F6A6E`),
remplie au chargement de l'étage par `0x8C0F5A4E`. La table qui associe un décor à ses
quatre bases n'est pas localisée ; les bases sont déduites des palettes confirmées.

**Palettes de personnage** (pour plus tard) : `0x8C0F59AA` donne l'adresse d'une palette,
`0x8C1E9AEC + offset - 0x02798000` — donc la palette N est référencée comme
`0x02798000 + N*128`. Deux tables de copie, format
`{u32 adresse, u32 destination, u32 taille}` : `0x1CB850` (3230 entrées, 112 listes, une
par personnage et couleur, nouvelle liste quand la destination repasse à 0) et
`0x1D4FD0` (~111 entrées, transferts multi-palettes). Ni l'une ni l'autre ne touche aux
décors.

**Retrouver les palettes depuis une capture** — la seule méthode qui marche, validée sur
sept décors. `outils/balayage.py` fait tout : il découpe la capture en fenêtres et, pour
chacune, ne garde que les couleurs **absentes du `.pvc` du décor** — donc appartenant à
un sprite — puis cherche la palette qui les contient exactement. L'émulateur étend les 5 bits par `(v<<3)|(v>>2)`, donc une capture **native, non
lissée** porte les valeurs exactes : les reconvertir en 5 bits et chercher la palette qui
les contient **sans tolérance**. L'écart au second est franc (7/8 contre 2/8). Les
scanlines ne gênent pas, un agrandissement bicubique est fatal. Bien isoler l'élément :
sur le feuillage de `bg0b`, toute l'image donnait 1099 (les branches du décor), les
pixels verts seuls donnent 1095. Outil : `outils/depuiscapture.py`.

**Piège majeur, mesuré sur deux cas confirmés :** la plage par décor **ne contraint pas**
les palettes de sprite. Elle se calcule sur les couleurs du `.pvc`, donc elle trouve les
palettes du **fond**, pas celles des sprites dessinés par-dessus. Les deux palettes
confirmées sont au niveau du bruit (2317 : 9,4 % de `bg10` ; 1095 : 6,2 % de `bg0b` ;
moyenne 7,7 %). Ne jamais s'en servir pour restreindre une recherche de sprite.

**Second piège :** le choix par lissage d'image ne vaut rien, il classe la bonne palette
2311e sur 2715.

**Palettes confirmées** : voir `dc-decors/PALETTES-CONFIRMEES.md`, quatorze décors.
Depuis la règle `base + offset`, connaître **une** palette d'un décor donne toutes les
autres. Urien (`bg0e`) en est sorti par **prédiction** : 1607 + 5 = **1612**, confirmé
ensuite sur capture (le grand pilier de pierre, 11 couleurs sur 12, rampe d'index 17–31).
Ken (`bg0c`) est réglé aussi — **1486, 1492, 1493** — mais par la RAM, pas par une
capture : ses sprites ne sont sur aucune capture, et le vélo, les bancs et le panneau du
ponton sont **du fond**. Un état sauvegardé Flycast porte le bloc du décor aux
emplacements 64 à 84 de la banque RAM `0x8C7AFCCC`, soit les palettes 1477 à 1497 ;
l'emplacement vaut `64 + offset du fichier`.

**Le piège des combattants s'est représenté deux fois.** Sur la capture de Ken, la
sacoche violette du vélo sort sur les palettes 211 et 24 — c'est celle de Ryu, comme le
sac de frappe du toit d'Alex. Toujours écarter les palettes < 500 avant de conclure.

**Why:** trois sessions ont buté sur « quel index va avec quel sprite » ; la question
était mal posée, et une seule capture d'écran l'a réglée.

**La RAM tranche mieux qu'une capture.** `outils/flycast.py` lit un état Flycast
(en-tête `FLYSAVE1`, vignette PNG, charge utile `#RZIPv` en tranches zlib ; la RAM se
repère par la signature de l'exécutable, chargé à 0x8C010000). `outils/etat.py` en sort
plans, objets de fond et la carte emplacement → palette. `outils/recolte.py` archive tout
dans `releves/`, les emplacements de sauvegarde étant limités à dix.

**How to apply:** partir de `outils/bases.py`. Une seule palette confirmée par décor
suffit désormais à déduire toutes les autres. Voir [[reference-sf3-dc-assemblage]],
[[reference-sf3-dc-fetc]] et [[project-sf3-dc-decors]].
