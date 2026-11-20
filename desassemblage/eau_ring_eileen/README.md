# L'eau du ring d'Eileen — les désassemblages

Déposés le 2026-11-19 pour [`analysis/eau_ring_eileen.md`](../../analysis/eau_ring_eileen.md).

Ce sous-dossier n'est **pas** géré par `tools/deposer_disasm.py` : il a été
écrit à part pour ne pas toucher à l'existant. Tout y est relu du binaire,
jamais recopié d'une note.

Les adresses Xbox 360 sont celles de **`extracted/X360_VF5/vf5_x360.img`** —
Virtua Fighter 5, Xbox 360, 2007, base `0x82000000`. Ce n'est pas
`extracted/X360_FS/`, qui est Final Showdown et répondrait autre chose sans la
moindre erreur. Les adresses APM3 sont celles de
`binaires/vf5fs-pxd-w64-Retail_APM3.dll.origine`, base `0x180000000`.

| fichier | ce qu'il porte |
|---|---|
| [`x360_rappel_anneau_eau.txt`](x360_rappel_anneau_eau.txt) | `TaskEffectWaterRing` côté console : la vtable `0x82005D0C`, le créneau 4 `0x821C9370` qui accroche le rappel sur `STGSLK_WATER_RING`, et **le rappel `0x821C9238`, qui lie les deux cibles de rendu sur les unités 3 et 4** avant de tracer. Plus les primitives `0x8224CAC8` / `0x8224CB28` / `0x82359788`. |
| [`apm3_rappel_anneau_eau.txt`](apm3_rappel_anneau_eau.txt) | le même objet dans la borne : vtable `0x18034F330`, créneau 4 `0x180085620`, rappel `0x180085680` — **le rappel console moins ses quatre liaisons de texture**, les six mêmes champs passés au tracé. |
| [`x360_chargeur_decor.txt`](x360_chargeur_decor.txt) | `0x822C3E38` cas 1 : ce qui lit `[descripteur+0x58]` (reflet) et `[descripteur+0x5C]` (réfraction), et `0x8224B590`, le lieur de scène (unités 15 et 14). |
| [`apm3_chargeur_decor.txt`](apm3_chargeur_decor.txt) | `0x18018FA20`, son jumeau : `[descripteur+0xC0]` et `[descripteur+0xC8]`. |
| [`tables_decors_reflet_refraction.txt`](tables_decors_reflet_refraction.txt) | les deux tables de descripteurs en entier — 37 décors côté X360, 41 côté APM3 — avec leurs blocs de reflet et de réfraction. |
| [`shaders_water_ring.txt`](shaders_water_ring.txt) | les 20 programmes `water_ring` de la Xbox 360 (lus dans leur CTAB) et les 8 d'APM3 (lus dans les déclarations du DXBC). |
| [`donnees_anneau_eau.txt`](donnees_anneau_eau.txt) | les matériaux et les textures du disque du ring dans les quatre jeux de données, et l'éclairage réellement posé. |
