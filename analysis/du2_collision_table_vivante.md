# `--du2-collision` écrivait dans une table morte

**2026-11-20.** Trouvé en passant par le sous-agent des doublons de Dural,
mesuré puis réparé ici. Rien n'a été lancé : aucune course, et le jeu n'a pas
démarré une seule fois.

---

## 1. Ce qui s'était passé

`--du2-collision` repointe le descripteur de `du2` sur sa propre collision.
C'est le correctif du « en ring out, le personnage est sur un sol qui n'existe
pas » : le build d'origine fait pointer `du2` sur `rom/STGDU1_COLI.000.bin`,
celle de `du1`. Frédéric l'a demandé, et validé **à l'écran** en septembre
2026 — « la modification du decor de dural est OK ».

Puis `--decors-table N` est arrivé. Il **recopie** la table des 41
descripteurs dans la section `.decors` et repointe les sites du moteur vers
la copie. La table d'origine devient morte. Et `--du2-collision` continuait
d'écrire dedans.

Le correctif ne s'est pas mis à échouer : il s'est mis à **ne rien faire**,
sans un mot, en rendant toujours 0.

## 2. La mesure, avant de toucher à quoi que ce soit

`tools/refs_plage.py` sur la plage des 41 descripteurs
(`0x180403430`–`0x180405AA0`, 9 840 octets) :

| binaire | références RIP-relatives vers `0x180403430` | vers `.decors` |
|---|---|---|
| `.origine` | **6** | — (la section n'existe pas) |
| DLL patchée | **0** | **6**, toutes vers `0x180EB1000` |

Les six sites sont les mêmes de part et d'autre (`0x18018EF79`,
`0x18018F3DD`, `0x18018F407`, `0x18018F569`, `0x18018F599`, `0x18018F640`) ;
celui de `+0x70` vise l'entrée 0 décalée dans les deux cas. **Le sous-agent en
annonçait cinq : il y en a six.**

Et le champ lui-même, entrée 22, `+0x48` :

| | table `0x180403430` | table `.decors` |
|---|---|---|
| `.origine` | `rom/STGDU1_COLI.000.bin` | — |
| DLL patchée (19 oct.) | `rom/STGDU2_COLI.000.bin` **(juste)** | `rom/STGDU1_COLI.000.bin` **(faux)** |

La table juste était celle que personne ne lit.

**Dix-sept lanceurs passent les deux options**, pas trois :
`decor_ajoute`, `decors_44`, `decors_5r`, `decors_grille`, `decors_table`,
`decors_vf5`, `depister_5r_ajoute`, `dojo_5r`, `dojo_5r_repli`,
`dojo_5r_temoin`, `item_porte`, `objset_pret`, `pister_5c_dojo`,
`pister_60_dojo`, `pister_decor_ajoute`, `pister_dojo_5r`, `questV2`.
Vingt-cinq passent `--du2-collision` en tout.

**L'ordre des options n'y est pour rien**, et c'est mesuré : les dix-sept
passent déjà `--du2-collision` **avant** `--decors-table`. Le socle applique
ses chantiers dans son ordre à lui, et recopie la table depuis l'état
d'origine quoi qu'on lui donne. Il n'y avait donc rien à corriger dans les
lanceurs.

## 3. Où la réparation est posée, et pourquoi là

Dans `VF5RE/tools/patch_moteur.py` — le pilote en source clair — et non dans
le socle, qui est du bytecode (`socle_20261008.pyc`) et où `--du2-collision`
vit hors d'atteinte. La fonction `_du2_collision_vivante()` tourne **après**
le socle, pour tout lanceur qui demande `--du2-collision`.

Trois choix, chacun pour une raison :

- **Aucun mot nouveau dans les lanceurs.** Une option neuve aurait réparé les
  lanceurs qu'on aurait pensé à modifier, et laissé les autres cassés. Les
  vingt-cinq sont réparés par l'option qu'ils passent déjà.
- **Aucune adresse de table en dur.** La fonction lit le déplacement du `lea`
  du moteur (`0x18018EF78`, celui dont `--eau-refraction` se sert déjà) **dans
  la DLL produite**, et suit donc la table vivante qu'elle ait bougé ou non.
  Sans `--decors-table`, la table vivante est l'originale, le champ porte déjà
  la bonne valeur, et la pose ne fait rien.
- **La chaîne est retrouvée par son contenu**, jamais par son adresse : le
  socle la pose dans le mou de `.rdata`, dont la place dépend des options.

Et quatre refus, qui préfèrent arrêter la construction à la laisser mentir :
la chaîne absente (le socle n'a pas posé l'option du tout), la chaîne présente
deux fois, un champ qui porte autre chose que la collision de `du1`, et
**l'absence de relocation** sur le champ visé — un pointeur absolu sans
relocation ne se voit pas au format, il se voit au premier rebasage, sous la
forme d'un plantage. (Elle est bien là : type DIR64, bloc `0x180EB2000`.)

## 4. Le contrôle, et ses deux sens vérifiés

`VF5RE/tools/controle_du2_collision.py`. Il ne connaît aucune adresse de
table : il suit le `lea`, lit le champ, lit la chaîne au bout, et montre les
**deux** tables côte à côte.

Il distingue **trois** états, parce qu'un silence ne les distingue pas : la
chaîne absente (l'option n'a pas été demandée — il le dit et rend 0), la table
vivante sur `du1` (la régression — il rend 1), la table vivante sur `du2`
(correct — il rend 0).

Les deux sens sont vérifiés sur de **vrais binaires**, pas sur une idée :

| binaire | verdict | code |
|---|---|---|
| DLL du banc d'avant (`.avant_du2_vivante`) | ÉCHEC, « la table vivante porte encore la collision de du1 » | **1** |
| DLL reconstruite | OK | **0** |
| `.origine` | troisième état, et la table vivante y est en `0x180403430` — la preuve qu'il suit le `lea` | 0 |

Le contrôle n'est câblé dans aucun lanceur : la réparation est automatique et
refuse bruyamment. Il est là pour le jour où la table déménagera encore.

## 5. La reconstruction, et ce qu'elle prouve

**Je me suis d'abord trompé de lanceur.** J'ai reconstruit avec la ligne de
`decors_vf5.cmd` : **6 106 octets** de différence avec le banc installé. Ce
n'était pas ce lanceur. J'ai restauré le banc depuis la copie prise avant
(empreinte revenue à `a9d02d13…`), puis trouvé la réponse là où elle était
écrite — `runtime/media/vf5fs/ram/patch_empreinte.json`, qui garde la **ligne
d'options entière** et le sha256 de la DLL produite. Le banc venait de
`questV2.cmd`, en **1920 × 1080**.

Reconstruit avec cette ligne-là :

```
octets differents : 3
  offset 0x6B5CE8 : 20 -> 60
  offset 0x6B5CE9 : 79 -> 1B
  offset 0x6B5CEA : 40 -> 64
```

**Trois octets, et rien d'autre.** 0x180407920 → 0x180641B60 ; les cinq
octets de poids fort du pointeur sont identiques. C'est exactement la forme du
correctif d'origine — « entree 22 (du2) : +0x48 +0x49 +0x4A » — posée cette
fois dans la table que le moteur lit.

Que le reste soit identique à l'octet prouve deux choses d'un coup : le patch
est déterministe, et j'ai bien reproduit la construction du banc.

| | empreinte |
|---|---|
| avant | `a9d02d136f78360f5e225bfb993c4101a6753ff7c0e85755250e251895a6d7ac` |
| après | `a0377dbf548868fbcc677600387f4918abab0b49845dd71d4e73836d3b6ced88` |

`vfes.exe` ne tournait pas (`tasklist` avant). Les deux contrôles de décors
déjà en place passent : `controle_decors_5r.py` « RIEN A REDIRE — les 23
entrées de VF5 R sont conformes à SON binaire », `controle_decors_vf5.py`
idem pour les 21 de ver.B. Le cache `patch_empreinte.json` porte la nouvelle
empreinte et la nouvelle taille du pilote.

## 6. Ce qui n'est PAS vérifié

- **L'écran.** Rien de ceci n'a été vu en jeu. Le ring out de `du2` est
  mesuré juste **dans le binaire** ; c'est Frédéric qui mesure l'écran.
  Ce qu'il faudrait regarder : un ring out sur le décor **du2** de Dural, et
  voir si le personnage tombe sur un sol à la forme de `du2` (3 984 octets de
  collision) au lieu de celle de `du1` (5 744).
- **Les douze autres tables indexées par le décor.** Je n'ai mesuré que celle
  des descripteurs. Si `--decors-table` en a déplacé d'autres, un autre
  correctif peut écrire dans une copie morte de la même façon. Ce n'est pas
  mesuré, et c'est la question qui ressemble le plus à celle-ci.
- **Les autres entrées de la table vivante.** La réparation ne touche que
  l'entrée 22. Si une autre entrée avait été corrigée par une autre option
  après la recopie, elle serait muette pour la même raison — non cherché.
- **Les seize lanceurs autres que `questV2.cmd`** n'ont pas été reconstruits.
  La réparation est dans le pilote, donc elle les couvre par construction,
  mais aucun n'a été exécuté.

## 7. Un contrôle qui passait sur un fichier cassé

`tools/verifier_decors_table.py` compare la copie de `.decors` à la table de
`.origine` et exige l'identité. Il est **câblé dans quatre lanceurs**
(`decor_ajoute`, `decors_44`, `decors_grille`, `decors_table`) et y rend 1.

Avant la réparation, la copie était identique à la source à l'octet, et ce
contrôle annonçait **AUCUNE FAUTE** — il confirmait fidèlement que la copie
portait fidèlement le défaut. Après la réparation, il a annoncé une faute qui
n'en était pas.

Il sait maintenant que cet écart-là est **voulu**, et seulement celui-là :
huit octets, à l'emplacement de `du2 +0x48`, et il faut en plus que la valeur
y soit l'adresse de `rom/STGDU2_COLI.000.bin`, retrouvée par son contenu. Un
autre octet reste une faute ; et l'inverse en est une aussi — la chaîne dans
la DLL et la copie qui ne pointe pas dessus, c'est la régression même.

Il est donc devenu un **second détecteur indépendant** de ce défaut, dans
quatre lanceurs, là où il était auparavant aveugle. Les deux sens sont
vérifiés en échangeant les binaires :

| DLL servie | verdict | code |
|---|---|---|
| réparée | « le seul ecart est VOULU : du2 +0x14E8 (sa collision) » / AUCUNE FAUTE | **0** |
| celle d'avant | « du2 +0x14E8 : la collision de du2 n est PAS posee » / 1 FAUTE | **1** |

### Deux fautes de ma part, attrapées par les contrôles et non par une course

- Mon poseur a écrit des ancres en **LF** dans un fichier en **CRLF pur** :
  zéro occurrence trouvée, rien écrit. (`patch_moteur.py` est en LF seul,
  `verifier_decors_table.py` en CRLF — les deux cohabitent dans `tools/`.)
- Mon premier tri des écarts classait « non posé » tout octet permis qui ne
  **diffère** pas de la source. Or les cinq octets de poids fort du pointeur
  sont identiques dans les deux tables : seuls trois changent. Le bon test ne
  regarde pas l'écart, il regarde **la valeur**.

## 8. Les fichiers touchés

| fichier | ce qui change |
|---|---|
| `VF5RE/tools/patch_moteur.py` | `_du2_collision_vivante()` et ses trois aides, appelées pour tout lanceur qui passe `--du2-collision` — avant le retour anticipé `if not demandes`, sinon `decors_table.cmd` et `decors_grille.cmd` n'en verraient rien |
| `VF5RE/tools/controle_du2_collision.py` | **neuf** — le contrôle dédié, trois états |
| `VF5RE/tools/verifier_decors_table.py` | l'écart voulu, borné et vérifié sur la valeur |
| `VF5RE/runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll` | reconstruit, trois octets |
| `…dll.avant_du2_vivante` | la copie prise avant, gardée |
| `…/ram/patch_empreinte.json` | mis à jour par `patch_si_besoin.py` |

Rien n'est commité.
