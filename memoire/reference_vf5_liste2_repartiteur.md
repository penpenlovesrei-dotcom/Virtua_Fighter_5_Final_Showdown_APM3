---
name: reference_vf5_liste2_repartiteur
description: La liste 2 de mothead a bien un répartiteur, MothRunList2 : il indexe une table de 55 gestionnaires avec le code au lieu de le comparer.
metadata:
  type: reference
---

`docs/formats/mothead.md` §3.12 affirmait que le DLL ne cherche que 7 des 44 codes de la
liste 2 et que les 37 autres ne sont jamais consultés. **Conclusion retirée le 2026-09-02.**

**`MothRunList2`** — APM3 `0x180152CE0`, R.E.V.O. `0x18015D3A0` :

- il lit un **curseur** rangé dans l'état (`+0x498` APM3, `+0x510` R.E.V.O.), remis à la base
  (`+0x4A0` / `+0x518`) par `0x180152DE0` / `0x18015D490` à chaque installation
  d'enregistrement ;
- il avance de 12 en 12 tant que la trame de l'entrée est échue, et **indexe** avec le code
  une table de 55 entrées de 32 octets — `mov r10,[table + code*32] ; call r10`. **Le code
  n'est jamais comparé** : d'où l'échec de toute recherche de `cmp code, K` ;
- la table est `0x180648840` (APM3, remplie à l'exécution par `0x180003D30`, nulle dans le
  fichier) et `0x180641350` (R.E.V.O., complète dans le fichier). **55 sur 55 pourvues** dans
  les deux ;
- la liste 2 est donc une **frise chronologique**, consommée une fois, le curseur ne revenant
  jamais en arrière. Le drapeau `+0x18` bit 0 (codes 0, 1, 8, 25, 31) = « n'agit qu'à la
  trame exacte ».

Codes établis : **0 = effet sonore daté** (charge = indice dans une table de 410 noms,
`0x180401730`) ; **9 = commutateur de bits daté** sur `état+0x4A8`, 18 cas.

Le contexte passe aux gestionnaires compte **six** cases, et ce n est pas un hasard :
`ctx = [ROB, ROB+0x440, autre, ROB, ROB+0x440, etat]`. Les trois dernieres rejouent la
convention de la liste 1, si bien qu un gestionnaire de liste 2 qui fait `add rcx, 0x18`
delegue au gestionnaire de liste 1. **Quatorze codes le font** : 36->4, 37->5, 38->6, 39->7,
40->8, 41->9, 42->10, 43->11, 44->12, 45->13, 46->14, 47->52, 48->58, 49->65. Les codes 38 a
46 reposent donc les neuf premieres fenetres temporelles a une trame donnee : les deux
verrous du chantier portent sur le meme objet.

Voir [[reference_vf5_etat_dans_rob]] et [[feedback_premisse_qui_borne]].
