# KNOCK OUT TRIAL / KOT SPECIAL : ce qu'il en reste dans le build APM3

Établi le 2026-09-07 sur `vf5fs-pxd-w64-Retail_APM3.dll.origine` (binaire NON
patché) et sur `vf5fs_data.par`. Aucun lancement, aucune écriture dans le jeu.

---

## 1. La réponse, en une ligne

**Oui, le mode existe encore — entier côté données, presque entier côté code,
et sous un autre nom à l'écran : `Special Sparring`.**

Ce n'est pas une déduction par ressemblance : le lecteur du fichier de données
du KO Trial, la table d'adversaires, le poseur de mode et l'écran de sélection
d'équipe sont **reliés par des appels que l'on peut lire**, et le fichier de
données est **présent et peuplé** dans l'archive du jeu.

---

## 2. Les preuves, dans l'ordre où elles ont été trouvées

### 2.1 Le fichier de données est dans l'archive, et il est plein

```
py -3 tools/sllz.py lister runtime/media/vf5fs/vf5fs_data.par kotrial
  kotrial_enemy_data.txt   303 079 o  compresse 79 847  offset 0xEDA7B000
```

Extrait dans `extracted/kotrial_enemy_data.txt` (8 524 lignes, UTF-8), sa
charpente est recopiée dans `extracted/kotrial_structure.txt` :

| famille | contenu |
|---|---|
| `kot_enemy.0..170` | **171 adversaires** : nom, personnage, `fileid`, deux répliques (`pr1`/`pr2`), deux costumes + équipements, rang, titre, texte de présentation, et **une trentaine de paramètres d'IA** (`ai_type0..6`, `ai_motion_num0..4`, `ai_nagenuke1..6`, `ai_ukemi`, …) |
| `kotsp_team.0..15` | **16 équipes « KOT SPECIAL »** : libellé, nom, emblème, membres, boss, condition de boss |
| `kot_area.0..9` | 10 aires : `THE MOON`, `THE SUN`, `THE STAR`, `THE WORLD`, `STRENGTH`, `JUSTICE`, puis `THE DEVIL`, `THE DEATH`, `JUDGEMENT` et 拳豪道場 |
| `kot_zone.0..3` | 4 zones : ゾーンA, ゾーンB, ファイナルボスエリア, 弟子エリア |
| `kot_wanderer.0..27` | 28 « rôdeurs » : condition d'apparition, récompense, aire, **`stage=a,b`** (plage de décors), adversaire |
| `kot_intruder.0` | l'équipe des 19 intrus セガショールーム |
| `kot_sp_npc.0` | le PNJ spécial du 拳豪道場 |

C'est la base de données complète du mode arcade, avec sa géographie (zones →
aires → équipes) et sa progression.

### 2.2 Le lecteur de ce fichier est dans le moteur

La classe est nommée par le RTTI : **`GmKotDat`**, vtable `0x180398720`.

```
0x1800993E0   GmKotDat::charger()      demande "./rom/rob_ai/kotrial_enemy_data.txt"
0x180099450   GmKotDat::analyser()     12 158 octets — l'analyseur du fichier
0x180098B50   creation du singleton    -> [0x1806F9418]
0x18009C4A0   remise a zero
```

Les clefs que l'analyseur reconnaît sont en clair en `.rdata`,
`0x180398850`–`0x180398B24`, et elles couvrent **`kot_enemy`, `kotsp_team`,
`kot_area`, `kot_zone`, `kot_intruder`, `kot_wanderer`** — donc y compris la
partie **SPECIAL** (`kotsp_team.<n>.emblem/.member/.boss/.boss_cond`).

Le chargement est déclenché depuis un seul site, `0x18006C2C4`, dans la machine
à états d'accueil `0x18006B880`, à l'entrée de l'écran **TERMINAL** (juste avant
`rom/sound/se_terminal.csb` et le passage à l'état `0xB`).

> Nuance à noter, elle est réelle : **`kot_sp_npc` n'a pas de clef dans le
> binaire APM3**, alors que le fichier de données en contient une. Le fichier
> livré est donc d'une révision plus récente que l'analyseur, ou ce bloc est lu
> ailleurs. Ne pas conclure au-delà de ça sans l'avoir cherché.

### 2.3 Les libellés anglais du mode sont dans `string_array`

| identifiant | texte |
|---|---|
| `0x1A1` | **`Special Sparring`** |
| `0x1C8` | `Team Select` |
| `0x194` | `Return to Team Select` |
| `0x1C9` | `You defeated %s!` |
| `0x1CA` | `All teams have been defeated!` |
| `0x592B`–`0x593E` | les **noms d'équipes** : `VF Academy`, `Dreamers`, `In the Stars`, `Underworld`, `Sega Maniacs`, `Beach Bums`, `Arcade Kids`, `Frightful`, `Travel Agents`, `Creatures`, `VF Marching Band`, `Go West`, `VF.TV Camera Crew`, `Rumble Jungle`, **`KOT Trial`**, `Chefs`, `Mixed Bag`, `Grab Bag`, `Swag Bag`, `The Bosses` |
| `0x593F` | `%d Stages` |
| `~0x57xx`–`0x592A` | le **roster** : trois libellés par adversaire (nom, `pr1`, `pr2`) — ex. `Marek` / `Begin your` / `countdown to tears!` |

Les seize équipes japonaises du fichier (`＜魁！ＶＦ学園＞`, `セガマニアックス`,
`海の家「浜本」`, `ＫＯＴ同窓会`, …) ont donc **leur traduction anglaise dans le
jeu**, dans le même ordre.

### 2.4 Le mode de jeu 3 est posé par l'écran d'équipe

`analysis/mode_de_jeu.md` avait déjà établi que le mode de jeu est le dword
`0x180751010` et que la valeur **3 = Special Sparring** est posée par
`TaskMenuTeam::update` (`0x1801A4252` → setter `0x18019C420`).

Le nom de la classe est **`TaskMenuTeam`** — l'écran *Team Select*, c'est-à-dire
la sélection d'équipe du KO Trial. Elle remet aussi à zéro `0x1807513A4`
(le compteur de progression) au lancement.

### 2.5 Et le combat va chercher l'adversaire dans la table du KO Trial

`0x1800B8540` est le **constructeur de match** (il remplit une structure de
configuration puis appelle `0x1800B34D0`, qui la recopie dans les paramètres de
partie). Il appelle **deux** choses du monde KOT :

```
0x1800B87E4  call 0x1800991E0    GmKotDat : table de 5 octets en 0x180398820,
                                 indexee par le niveau CPU (0x18019C060)
0x1800B8858  call 0x1801A53A0    construit un enregistrement d'adversaire
0x1800B89D5  call 0x1801A53A0    (les deux cotes)
```

`0x1801A53A0(dst, n)` initialise un enregistrement de **0x27C octets** au format
`kot_enemy` (via `0x180098E80`, l'initialiseur de `GmKotDat`) puis le remplit
depuis une **table statique du binaire, `0x18040B650`, au pas de 0x8E octets** :
personnage, costume, équipement, rang, titre, et les paramètres d'IA. Le second
lecteur de cette même table, `0x1801A5B90`, résout des **identifiants de texte**
par `0x1801EFD10` — c'est-à-dire les libellés `0x592B…` ci-dessus.

**Conclusion de chaîne** : `Special Sparring` → `TaskMenuTeam` → mode 3 →
`0x1800B8540` → table d'adversaires au format `kot_enemy` → libellés d'équipes
du KO Trial. C'est le même mode.

---

## 3. Ce que l'arcade avait et qui n'est plus câblé

La différence n'est pas dans l'existence du mode mais dans **ce qui l'entoure**.
Sur le Lindbergh VF5 (`analysis/strings_vf5_lind.txt`, binaire ELF x86) on lit :

```
kotrial %d                       journal
kot_special_mode %d              journal — LE mode special
26TaskKoTrialDefeatStartDisp     tache d'affichage
24TaskKoTrialDefeatEndDisp
27TaskKoTrialIntrudeStartDisp
25TaskKoTrialIntrudeEndDisp
21TaskKoTrialAdviceDisp
17TaskKoTrialKoDisp
KO_TRIAL_DEFEAT_DISP / KO_TRIAL_INTRUDE_DISP / KO_TRIAL_ADVICE_DISP / KO_TRIAL_KO_DISP
KNOCKOUT TRIAL / KNOCKOUT TRIAL 1
16DwKotrialCapture / KOTRIAL CAPTURE / 26DataTestKotrialCaptureTask
p_trial_icon01_lt, p_trial_cursor01..10_lt
```

**Aucune de ces classes ni de ces chaînes n'existe dans le PXD APM3.** Les six
tâches d'affichage du KO Trial (défaite, intrusion, conseil, KO) et l'écran
titre `KNOCKOUT TRIAL` ont été retirés du build Windows ; ce qui reste, c'est le
**cœur** : la base de données, son analyseur, la table d'adversaires, le mode 3
et l'écran de sélection d'équipe.

Le R.E.V.O. Windows (`strings_pxd_revo.txt`) est dans **exactement le même
état** que l'APM3 : deux occurrences, `kotrial_enemy_data.txt` et
`sy_vf5fs_knockout`. La coupe date donc du portage PXD, pas de la borne.

*(`sy_vf5fs_knockout` est un repère sonore — l'annonce « K.O. » — pas le mode.
Il ne prouve rien et ne doit pas être compté comme une trace.)*

---

## 4. Ce que ça ouvre

1. **Les 171 adversaires du fichier ne sont pas ceux de la table statique.**
   `0x18040B650` (pas 0x8E) est une table **du binaire** ; le fichier
   `kotrial_enemy_data.txt` en est une autre, **du disque**. Savoir laquelle
   alimente réellement `Special Sparring` demande une mesure : point d'arrêt sur
   `0x1801A53A0` et sur `0x180099450`, et on lit qui passe.
2. **La géographie (zones/aires/équipes/rôdeurs) n'a pas d'écran.** Les tâches
   d'affichage sont absentes. C'est le vrai maillon manquant si l'on veut
   remonter le KO Trial complet, et c'est un chantier d'interface, pas de
   données.
3. **`kot_wanderer.<n>.stage=a,b`** est une plage d'index de décors : le mode
   choisissait son décor dans une fourchette. Voir `analysis/decors.md` §5 —
   l'index de décor du match est bien un champ des paramètres de partie, et il
   est réglable.

Confiance : **CONFIRMED** pour §2.1 à §2.4 (lecture statique complète, chaînes
d'appel vérifiées une par une, fichier extrait et lu). **SUPPORTED** pour §3
(absence prouvée par balayage ASCII *et* UTF-16 des deux binaires, mais une
absence de chaîne n'est pas une absence de code).
