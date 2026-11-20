---
name: reference_vf5_relocation_pointeur_nul
description: Une relocation sur un champ NUL fabrique un pointeur non nul ; le delta de rebasage se reconnait a vue.
metadata: 
  node_type: memory
  type: reference
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-10T21:07:55.877Z
---

Un champ mis a ZERO qui porte encore une RELOCATION n'est pas nul a
l'execution : le chargeur y ajoute le delta de rebasage. La garde
`if (ptr != 0)` du moteur laisse alors passer un pointeur mort.

**Le delta se reconnait a vue** : `base du module - base preferee`. Sur le
plantage d'aurora du 2026-09-10, `rbp = 0x00007FF8892E0000` et
`0x7FFA092E0000 - 0x180000000 = 0x7FF8892E0000`. Egalite exacte = le champ
valait zero dans le fichier.

Cas de figure : on clone un enregistrement AVEC ses relocations, puis on remet
un de ses pointeurs a zero pour dire « ce champ n'existe pas ». La relocation
survit au zero.

`patch_moteur.decors_table()` retire desormais de `a_reloger` toute relocation
qui vise un quadruple mot nul, et le DIT. Voir [[reference_vf5_greffe_section]]
et [[reference_vf5_clone_pointe]].
