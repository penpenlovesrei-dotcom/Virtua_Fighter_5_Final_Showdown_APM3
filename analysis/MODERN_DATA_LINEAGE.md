# MODERN_DATA_LINEAGE — ce que les versions modernes ont hérité de Final Showdown

Rédigé en phase 0 parce que la preuve s'est présentée d'elle-même pendant l'inventaire.
Ce document répond à §21 pour les **données** ; la partie code reste à établir.

Rappel de §22 : *même donnée ≠ même code*. Les deux volets sont séparés ci-dessous.

---

## 1. Lignée de **code** — le moteur FS survit tel quel

Les deux binaires modernes portent un bloc de version rigoureusement identique :

| | `APM3_US` — Ultimate Showdown | `PC_REVO` — R.E.V.O. |
|---|---|---|
| Fichier | `vf5fs/vf5fs-pxd-w64-Retail_APM3.dll` | `vf5fs/vf5fs-pxd-w64-d3d12_SteamRetail.dll` |
| Chemin de build | `D:/Project/vf5/vf5fscs_source/20120711_update_1.1/vf5fs` | idem |
| Date du portage | `2016-06-30T14:58:25+09:00` | idem |
| Auteur du build | `atsu_takashi` | idem |
| Snapshot source | `2012-07-04T18:06:57+09:00` | idem |
| Titre / release | `Virtua Fighter5 Final Showdown` / `6.000` / `VERSION A` / `REVISION 1` | idem |

Lecture :

- `vf5fscs_source` = branche **console** (« cs ») de VF5FS, mise à jour 1.1 du 2012-07-11.
- Le suffixe `pxd` désigne la couche de portabilité du moteur (déclinée `w64`, `w64-d3d12`).
- Le portage date de **2016**, soit avant Ultimate Showdown (2021) et R.E.V.O. (2025) :
  les deux jeux modernes s'appuient sur **le même travail de portage**.
- Le numéro de release **6.000** est celui de notre dump `APM3_FS` (Lindbergh Rev B 6.0000).

**Conclusion : Ultimate Showdown et R.E.V.O. n'ont pas réimplémenté le moteur de combat de
Final Showdown ; ils l'embarquent, porté en x64. Confiance : CONFIRMED** pour l'identité des
blocs de version ; **SUPPORTED** pour l'affirmation que le combat est effectivement simulé par
ce DLL (le flux d'appel depuis `VFREVO.exe` / `vfes.exe` n'est pas encore tracé).

Ce résultat modifie la stratégie du projet : **`vf5fs-pxd-w64-d3d12_SteamRetail.dll` est une
pierre de Rosette**. C'est le même code que l'ELF Lindbergh, en x64 moderne, donc bien plus
lisible en décompilation — et directement comparable, fonction par fonction.

---

## 2. Lignée de **données** — mesurée au SHA-256

Comparaison intégrale de `rom/rob/` sur cinq jeux de données.
Matrice complète : `comparisons/rob_data_matrix.csv`.

| Catégorie | Rev A 2.000 → Rev B 6.000 | 6.000 → PS3 | 6.000 → REVO `rom/` | PS3 → REVO `rom/` | REVO `rom/` → `rom_200/` |
|---|---|---|---|---|---|
| `mothead_*.bin` (coups) | **0 / 21 identiques** | absent sur PS3 | **20 / 21 identiques** | absent | **0 / 21 identiques** |
| `ctrl_*.bin` (commandes) | **0 / 20 identiques** | absent sur PS3 | **19 / 20 identiques** | absent | **0 / 20 identiques** |
| `mot_*.farc` (animations) | 8 / 26 identiques | 23 / 24 | 24 / 26 | **24 / 24 identiques** | absent |
| `mot_AUTH_*.farc` | 13 / 21 identiques | 20 / 21 | 20 / 21 | **21 / 21 identiques** | absent |
| `rob_mot_tbl.bin` | différent | absent | **identique** | absent | absent |

### Ce qu'on en tire

1. **Rev A → Rev B 6.0000 est une refonte du gameplay.** Aucun `mothead_` ni `ctrl_` ne
   survit intact, et deux tiers des animations changent. Confiance : **CONFIRMED**.

2. **Les données de combat de l'arcade 6.000 survivent bit à bit dans R.E.V.O. en 2025.**
   20 `mothead_` sur 21 et 19 `ctrl_` sur 20 sont **identiques au SHA-256**, ainsi que
   `rob_mot_tbl.bin`. Quatorze ans, trois générations de matériel, deux portages — et le
   fichier n'a pas bougé d'un octet. Confiance : **CONFIRMED**.

3. **Le seul écart est Dural.** `mothead_DUR`, `ctrl_DUR`, `mot_DUR`, `mot_AUTH_DUR` diffèrent
   entre l'arcade et R.E.V.O., et sur ce point **R.E.V.O. suit la PS3, pas l'arcade** :
   `mot_AUTH_DUR` et `mot_DUR` de R.E.V.O. sont identiques à ceux de la PS3
   (341 273 o et 4 227 095 o), pas à ceux de la Lindbergh (66 788 o et 4 220 165 o).
   Cohérent avec la provenance `vf5fscs_source` (branche console) du moteur porté.
   Confiance : **CONFIRMED**.

4. **R.E.V.O. ajoute `ctrl_DUR_cpu.bin` et `mothead_DUR_cpu.bin`** : une variante CPU de Dural
   absente de toutes les versions antérieures.

5. **`rom_200/` est une troisième génération de données.** Aucun `mothead_` ni `ctrl_` de
   `rom_200/` n'est identique à son homologue `rom/` : c'est le rééquilibrage complet
   « version 2.00 » de R.E.V.O., livré à côté des données d'origine. Il contient aussi
   `training/` (20 fichiers) et `chritm_tbl.farc` (12,94 Mo contre 1,81 Mo sur Lindbergh).
   Confiance : **CONFIRMED**.

### Conséquence méthodologique

Le format de `mothead_*.bin` et `ctrl_*.bin` peut être attaqué avec **trois jeux de données
alignés sur le même format** : Rev A 2.000, arcade 6.000 (= R.E.V.O. `rom/`), et R.E.V.O.
`rom_200/`. Les tailles restent très proches d'une version à l'autre
(ex. `mothead_AKI` : 189 628 o en 6.000 contre 190 108 o en 2.00), ce qui suggère une
structure d'enregistrements de taille fixe. Diff structurel = méthode privilégiée pour la
rétro-ingénierie du format.

---

## 2 bis. Confirmation par le code

Le désassemblage du DLL de R.E.V.O. corrobore la mesure faite sur les données.

`0x180164840` est la **seule** fonction du DLL à référencer un chemin `mothead_`, et elle
référence les **deux** : `./rom/rob/mothead_` et `./rom_200/rob/mothead_`. Le choix se fait à
l'exécution, sur un booléen reçu en argument :

```
0x18016489A  test bl, bl
0x18016489C  je   0x180164d32     ; -> ./rom_200/rob/mothead_
0x1801648A2  lea  r10, [rip+…]    ; -> ./rom/rob/mothead_
```

Même schéma pour `ctrl_` (`0x18005A910`). En revanche `rob_mot_tbl.bin` (`0x1801664B0`) n'a
**qu'un seul chemin** : ce fichier est commun aux deux jeux de données.

C'est exactement ce que dit la comparaison au SHA-256 : `mothead_` et `ctrl_` sont les seuls
fichiers de `rom/rob/` qui diffèrent entre `rom/` et `rom_200/`, et `rob_mot_tbl.bin` est
identique. **Deux méthodes indépendantes, même conclusion.** Confiance : **CONFIRMED**.

Autrement dit, R.E.V.O. embarque le jeu de données d'origine de Final Showdown **et** son
rééquilibrage, et bascule de l'un à l'autre par un simple drapeau.

## 3. Ce qui n'est **pas** établi

- Rien ne prouve encore que `VFREVO.exe` ou `eve.exe` partagent du code avec FS. Ce sont des
  enveloppes probablement issues du moteur Dragon (archives `.par`, nom de code `adam`).
  Confiance : **LIKELY** pour Ultimate Showdown, **UNKNOWN** pour R.E.V.O.
- La lignée d'**algorithmes** entre l'ELF Lindbergh et le DLL x64 n'est pas vérifiée : même
  code source ne garantit pas mêmes fonctions après quatorze ans de maintenance et un
  changement d'architecture. À établir par comparaison fonction par fonction.
- Les données PS3 et X360 restent partiellement inaccessibles (`rom.psarc` non ouvert,
  conteneur STFS non ouvert).
