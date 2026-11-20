---
name: reference_vf5_greffe_section
description: "VF5 — on AJOUTE des sections au PE (4 en-têtes libres), et depuis le 2026-09-09 on peut aussi leur donner des RELOCATIONS : le répertoire n° 5 se repointe."
metadata:
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-09T19:08:42.695Z
---

**La place.** Les bourrages `int3` rendent 20 octets au mieux. Le fichier, lui,
a de la place aux deux endroits qu'il faut : la table des sections finit en
`0x348` alors que `SizeOfHeaders` vaut `0x400` (**184 octets libres, quatre
en-têtes de plus**), et le fichier s'arrête exactement où finit `.reloc`, sur
une frontière de `FileAlignment`. **Aucun octet existant n'est déplacé.**

**Trois sections prévues, et L'ORDRE COMPTE :** `.greffe` d'abord (elle doit
garder `0x180EA1000`, ses réglages sont documentés à des adresses fixes), puis
`.decors`, puis `.reloc2` en dernier puisqu'elle décrit les deux autres. Une
quatrième reste libre.

## La règle « aucun pointeur absolu » est LEVÉE (2026-09-09)

Elle valait parce qu'une section ajoutée n'apparaît dans aucun bloc de
relocation, et que la DLL est rebasée (`0x7FFC81C70000`, `0x7FFDB0620000`… —
une adresse différente à chaque mesure).

**Le chargeur ne cherche pas `.reloc` : il lit le répertoire de données n° 5,
un couple (RVA, taille) à `optional_header + 152`.** Donc :

1. lire les 209 blocs d'origine (29 643 entrées) ;
2. y ajouter les siennes, groupées par page de 4 Ko, type **10 (`DIR64`)** ;
3. écrire le tout dans une section neuve ;
4. repointer le répertoire.

`tools/pe_sections.py` le fait (`--essai` = auto-contrôle relu par `pefile`, et
un rebasage simulé). **Deux détails du format qui ne pardonnent pas** : la
taille d'un bloc doit être multiple de quatre — bourrer avec une entrée
`ABSOLUTE` si le nombre d'entrées est impair — et les pages doivent croître.

Le mou de `.reloc` (328 octets) existe et ne sert à rien : une table de décors
demande des milliers d'entrées.

**Prouvé dans le processus vivant**, pas seulement au format : pointeur
`0x180403430` écrit en dur dans `.decors`, jeu lancé, lecture mémoire →
`base + 0x403430`. Détail : `analysis/greffe_relocations.md`.

## L'ordre d'écriture compte plus que le code

Le détour `--variantes` écrivait `TaskSelStage+0x5C` en `0x180174710` : tout
marchait et pourtant seul du1 se chargeait. Un point d'arrêt **MATÉRIEL** en
écriture (`tools/pister_5c.py`) a nommé les concurrents — la recomputation
depuis la case du curseur (`0x180174781`) passait après nous. D'où la forme en
**deux accroches**.

**How to apply:** avant de contorsionner du code en RIP-relatif dans une
greffe, se demander si la donnée ne devrait pas simplement être **relogée** —
c'est possible depuis le 2026-09-09. Et quand un champ partagé « ne garde pas »
ce qu'on y écrit, ne pas relire le code : armer un DR en écriture dessus. Voir
[[reference_debogueur_win32_pieges]] et [[project_vf5_decors_dural]].
