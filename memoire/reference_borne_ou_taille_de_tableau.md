---
name: reference_borne_ou_taille_de_tableau
description: "Une borne à N n'est pas forcément une borne de TABLE : ça peut être la taille d'un tableau DANS une structure, et la lever écrit dans le champ d'à côté."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 75b9ae93-ca65-4776-9a1e-32941de24687
  modified: 2026-09-10T06:36:45.613Z
---

Mesuré sur VF5 APM3 le **2026-09-09**, en levant les bornes des 41 décors.

Six des sept `cmp` à 41 bornaient bien une **table** de `.rdata` : les lever
suffit. La septième, celle des **compteurs de parties**, n'indexait aucune
table — elle recopiait des compteurs d'un objet vers un autre :

```
source       [r14 + 0x11FC + i*8]      parties, victoires
destination  [rdi + 0x1A2EC + i*0x10]  trois dwords et un ratio
```

**Les deux tableaux font exactement 41 entrées, et deux instructions qui suivent
la boucle le prouvent** : `lea rsi, [rdi + 0x1A580]` alors que
`0x1A2EC + 41*0x10 = 0x1A57C`, et `lea rbx, [r14 + 0x1348]` alors que
`0x11FC + 41*8 = 0x1344`. Le champ suivant commence juste après. Lever la borne
n'aurait pas donné de statistiques aux décors ajoutés : cela aurait écrit dans
le champ d'à côté.

**Comment distinguer les deux, et c'est la seule façon :** regarder ce qui SUIT
le tableau. Un `lea` sur l'adresse immédiatement suivante dit que la taille est
figée dans la structure. Une table de `.rdata`, elle, est suivie d'autre chose
sans rapport.

Deuxième piège, payé le même jour : l'adresse notée pour cette borne
(`0x1801B5F7F`) était un **début de fonction relevé dans `.pdata`**, pas une
comparaison — les vraies étaient `0x1801B648D`, `0x1801B6507` et `0x1801B6483`
(la version déroulée par huit, bornée à `N - 7`). Une entrée `.pdata` est
souvent un simple FRAGMENT.

**Troisième forme, trouvée le 2026-09-10 : la LISTE D'ASSOCIATION avec valeur
par défaut.** Les sons d'ambiance de VF5 (`0x180408850`) sont 24 entrées
`{indice, pointeur}` parcourues linéairement, terminées par un pointeur nul ; un
indice inconnu ne casse rien, le code garde le défaut posé juste avant la
boucle. C'est la seule des trois formes qui pardonne — donc avant d'ajouter une
entrée ou de lever une borne, savoir dans laquelle on est. Et la régularité ne
dit rien de la forme : cette table est parfaitement régulière et n'est pas
indexée (cf. [[reference_coherence_nest_pas_role]]).

**How to apply:** avant de lever une borne pour agrandir quoi que ce soit,
désassembler la boucle ENTIÈRE et lire l'instruction qui suit. Et ne jamais
lever une borne dont l'adresse vient d'une note : la relire. Voir
[[reference_tables_indexees_par_etage]], [[feedback_chercher_la_borne]] et
[[reference_vf5_greffe_section]].
