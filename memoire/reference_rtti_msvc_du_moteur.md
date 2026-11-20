---
name: reference_rtti_msvc_du_moteur
description: "Les noms de classes du moteur VF5 se lisent par tools/rtti.py (RTTI MSVC) — extract_rtti.py ne sait lire que l'ELF PS3, et le « AV » d'un nom est du mangling, pas un préfixe."
metadata: 
  node_type: memory
  type: reference
  originSessionId: c8041ead-a983-4a60-bc8a-6955e23922a8
  modified: 2026-09-05T16:18:18.948Z
---

Le moteur APM3 (`vf5fs-pxd-w64-Retail_APM3.dll`) est un PE MSVC x64 à **RTTI
complet** : 534 vtables nommées, dont tout le sous-système réseau et toutes les
pages de menu. C'est la source de noms la plus fiable du chantier.

**`tools/extract_rtti.py` ne sert à rien ici** : il lit l'ABI Itanium, donc le
build **PS3 (ELF)**, pas le PE. Le bon outil est **`tools/rtti.py`**, écrit le
2026-09-05 :

    py -3 tools/rtti.py --out analysis/rtti_apm3.txt
    py -3 tools/rtti.py --grep Link

La chaîne qu'il suit : `TypeDescriptor` (nom `.?AVMaClasse@@`, la structure
commence 0x10 octets AVANT la chaîne) → `CompleteObjectLocator` (24 octets,
signature 1, et un champ `rva(self)` qui rend la reconnaissance sûre) → la
vtable, dont le qword **qui précède** pointe sur le COL.

**Le piège qui a fait écrire un document entier avec de faux noms** : dans
`.?AVFoo@@`, le **`V` est la lettre de classe du mangling** (V = class,
U = struct), et le `A` le précède. Une lecture naïve de la chaîne brute donne
`AVFoo` et on croit à un préfixe de nom. C'est ainsi que `am::abaas::LinkMain*`
a été noté « AVLinkMain* » pendant toute une séance — voir
[[reference_vf5_reseau]].

**How to apply:** avant d'affirmer un nom de classe du moteur, le lire dans
`analysis/rtti_apm3.txt`, et se rappeler que les vtables voisines se touchent —
lire quatre qwords à une adresse donne parfois la fin de la table précédente.
`tools/vtable.py` détecte les frontières et le type de chaque créneau.

Voir [[reference_tables_indexees_par_personnage]],
[[reference_coherence_nest_pas_role]].
