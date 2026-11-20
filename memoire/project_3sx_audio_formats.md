---
name: project-3sx-audio-formats
description: Formats audio confirmés de SFIII 3rd Strike (arcade CPS3 vs Dreamcast) — mesurés le 2026-08-05.
metadata: 
  node_type: memory
  type: project
  originSessionId: bcdf1e34-e5cb-449b-95dd-28e10b9d06c4
  modified: 2026-08-05T21:42:52.503Z
---

Comparaison voix/bruitages entre versions de Street Fighter III: 3rd Strike.
Mesuré directement sur les fichiers présents sur cette machine (2026-08-05).

**Arcade CPS3** — la ROM son est le SIMM `30` **seul** (8 Mo), pas « 30 et 31 » :
`31` est de la donnée graphique (corrélation lag-1 ≈ 0,05 contre 0,82 pour `30`).
PCM 8 bits **signé**, mono, et les octets sont **inversés par paires** (mots 16 bits
big-endian) : lus tels quels le spectre montre une bosse parasite à 11–17 kHz.
Cadence de base 37 288 Hz → 298 kbit/s. Voix, bruitages et samples de musique
sont mélangés sans séparation ; la table des samples est dans les SIMM `10`/`20`
qui sont **chiffrés** (entropie 8,0) → pas d'extraction son par son sans
implémenter le déchiffrement CPS3.

**Dreamcast** (GDI, `track03.bin`, mode1/2352, LBA de base 45000) : les voix et
les bruitages ne sont **pas** en ADX, contrairement à l'hypothèse de départ.
- `/SOUND/*.ADX` = musique seulement (67 pistes), ADX type 3, 44100 Hz stéréo.
- `/SOUND/PLxx.OSB` = **voix**, une banque par personnage (`SOSB`), ADPCM 4 bits
  Yamaha AICA. 74 % des sons à 44100 Hz, le reste à 39255/34970/22050 Hz.
- `/SOUND/SF3_3RD.MLT` = conteneur `SMLT` : 1 `SMPB` + 1 `SMSB` + 4 `SOSB`, dont
  deux unités remplies (**bruitages**, 68 et 32 sons) et deux emplacements vides
  de 0x48000 o réservés au chargement des 2 banques de voix des combattants.
- `/DPETC/VOICE.AFS` (19 Mo) appartient à DreamPassport, **pas** au jeu.

Format d'une entrée `SOSP` (0x40 o) = recopie des registres de slot AICA :
`+04` u16 (bits 8-7 = PCMS, bits 6-0 = SA haut), `+06` SA bas, `+08` LSA,
`+0A` LEA, `+10` bits 14-11 = OCT signé / bits 10-0 = FNS
→ cadence = 44100 × 2^OCT × (1024+FNS)/1024.

**Double Impact Dreamcast** (`Downloads/SF3.3 music/Street Fighter III - Double Impact.cdi`,
lu le 2026-08-05) — **la note « impasse, musique séquencée » du briefing est fausse.**
Le disque est un ISO9660 en secteurs MODE2/2336 avec le pregap de 150 secteurs, donc
LBA fichier = LBA volume + 150 ; volume `STREET_FIGHTER3_W_IMPACT`, 316 fichiers.
Les deux jeux sont séparés : `/SFNG` (New Generation) et `/SFNG2` (2nd Impact).
Il contient **69 fichiers `.ADP`** — 32 en `M101`-`M120` pour NG, 36 en `M201`-`M229`
pour 2nd Impact — de 3 à 7 Mo chacun, sans en-tête. C'est la source manquante pour les
packs BGM de ces deux épisodes, **décodée et confirmée à l'oreille le 2026-08-05**.

Format exact : ADPCM Yamaha, **stéréo entrelacée au nibble** — nibble bas = canal
gauche, nibble haut = canal droit, dans chaque octet, **chaque canal ayant son propre
prédicteur et son propre pas**. 44100 Hz. Les décoder comme un flux unique donne bien
de la musique reconnaissable mais **écrête 4 % des échantillons** et sonne mal ; en
deux flux séparés l'écrêtage tombe à 0,08 % et la corrélation L/R monte à 0,93-0,97.
Les thèmes de décor font alors 2:30-2:40, les jingles ~13 s — des durées cohérentes.
L'algorithme lui-même est celui de `adpcm_yamaha` de ffmpeg, vérifié **bit à bit**
(0 écart sur 882 000 échantillons) : en cas de doute, emballer le `.ADP` brut dans un
en-tête WAV avec `wFormatTag = 0x0020` et laisser ffmpeg décoder sert de référence.
Le `VOICE.AFS` de 19 Mo qui avait fait conclure à l'impasse est dans `/DPETC`, donc
DreamPassport — cohérent avec ce qui est noté plus haut.

Côté graphismes, les données sont en `.PK` : `C00`-`C0E` personnages, `B00`-`B13` décors.
Attention, un `.PK` de personnage embarque une banque `SOSB` (à l'offset 0x40 dans
`C00.PK`), donc du son : chercher des palettes en scannant le fichier tombe sur ses
échantillons ADPCM et donne des faux positifs.

**Online Edition** (rip Zophar dans `Downloads/SF3.3 music`) : XMA2 (tag 0x0166),
48000 Hz stéréo, ≈140 kbit/s — donc le build Xbox 360, et musique uniquement.
Les 1662 fichiers du rip sont **tous** des segments de musique (préfixe `o` pour
les pistes d'origine, `SF3OE_` pour le remix Viklund) : aucune voix ni bruitage.
Cohérent avec le fait que l'OE émule la ROM CPS3 et ne remplace que la musique
par des flux externes → voix et bruitages a priori identiques à l'arcade.
Inféré, pas vérifié par désassemblage du build PS3.

**PS2** : aucune image du jeu ni de l'Anniversary Collection sur cette machine
(recherche faite sur C: et E:, seuls disques présents). Non mesuré.

Scripts d'analyse (extraction GDI, parseur SOSB/SMLT, décodeur ADPCM AICA,
analyse spectrale) : voir [[reference-3sx-audio-scripts]].
Tentative de faire correspondre un même échantillon entre CPS3 et DC par
corrélation d'enveloppes : **non concluante** (le témoin négatif — échantillon
inversé dans le temps — obtient le même score).

Voir aussi [[project-3sx-bgm-remix]].
