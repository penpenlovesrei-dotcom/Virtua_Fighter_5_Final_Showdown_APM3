---
name: reference_vf5_build_yakuza6
description: "VF5 — le moteur embarqué dans Yakuza 6 est une pierre de touche : mêmes données, un seul descripteur différent (la collision de DU2), et il prouve que le bouchonnage n'est pas une amputation arcade."
metadata:
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-09T16:32:02.449Z
---

`…\VF5 FS DECOMP\Yakuza_6_FS\Yakuza 6 - vf5fs\` — `vf5fs-pxd-w64-Retail_GOG.dll`
(5,39 Mo) et son `.par` (1,79 Go). **Bâti le 2022-12-02, dix-huit mois APRÈS
l'APM3** (2021-05-19) et pourtant plus petit d'un tiers : 9 770 fonctions
contre 13 661. Même moteur, sans la couche arcade.

**Les données sont les mêmes.** 1 822 fichiers communs ; les 41 décors aux
mêmes tailles à l'octet près. APM3 a en plus les dix-neuf
`<perso>itm_patch.farc` et `se_adam.acb`. Le `stgdur` perdu n'y est pas non
plus — voir [[reference_vf5_stgdur_verb]].

**LE RÉSULTAT QUI SERT : sur les 41 descripteurs de décor, un seul champ
diffère**, et c'est la **collision de DU2** (APM3 `STGDU1_COLI`, Yakuza 6
`STGDU2_COLI`). Le défaut vu à l'écran par Frédéric est une régression propre à
l'APM3, et `--du2-collision` est validé par un build indépendant.

Le pas d'une entrée vaut **0xF0 chez APM3 et 0xD8 chez Yakuza 6** : les
24 octets sont le bloc BGM, dix pointeurs contre sept. Tout le reste se
réaligne — `+0xB8`→`+0xA0`, `+0xD0`→`+0xB8`, `+0xE4`→`+0xCC`.

**LE BOUCHONNAGE N'EST PAS UNE AMPUTATION.** Les quatre mêmes familles
existent des deux côtés — `ret 0` 577/429 appelants, `xor al,al ; ret`
210/**241**, `xor eax,eax ; ret` 117/128, `mov al,1 ; ret` 71/44. Ce sont des
fonctions vides fusionnées par l'éditeur de liens. Corrige la lecture de
[[reference_vf5_verrou_bouchonne]] : « patcher le site d'appel, jamais le
corps » reste vrai, « c'est bouchonné donc amputé » est faux.

**RTTI** : 534 vtables contre 314 ; sur les noms de BASE, 118 propres à APM3
(réseau `Abaas`/`Link*`/`Turn*`, crypto, `TaskApm3*`, menu opérateur `Menu*`)
et **trois** propres à Yakuza 6 : `TaskMultiMenu`, `TaskMultiMenuRule`,
`TaskMultiResult` — la partie locale à plusieurs.

**How to apply:** `tools/comparer_builds.py <a.dll> <b.dll>` compare les
structures (table des décors, pas déduit, 41 descripteurs, chaînes témoins) et
`tools/par_inventaire.py <a.par> --contre <b.par>` les archives. Deux pièges
payés : **le pas d'une table se déduit** (figé à 0xF0 → « table introuvable »),
et chercher une chaîne en exigeant son NUL fait manquer `am::abaas` et
`STGDUR`. Document : `analysis/comparaison_builds.md`. Voir
[[reference_vf5_pxd_pierre_de_rosette]].
