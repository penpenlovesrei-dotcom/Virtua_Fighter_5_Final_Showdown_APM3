# Prompt de reprise — VF5RE, session du 2026-10-18

Colle ce texte au début d'une nouvelle session.

---

## Le contexte

Rétro-ingénierie de **Virtua Fighter 5 Final Showdown, build arcade APM3**
(SEGA ALLS), dans `C:\Users\frede\Desktop\VF5RE`. **Réponds en français.**

Le moteur est `runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll` (base
`0x180000000`), chargé par `vfes.exe` (base `0x140000000`). On **analyse
toujours le `.origine`**, on **patche toujours par `tools/patch_moteur.py`**,
et on lance par un double-clic sur un `.cmd`.

`patch_moteur.py` est un **pilote** : il charge `tools/socle_20261008.pyc` et
porte en source claire tous les chantiers postérieurs. Les noms d'options
qu'il ne connaît pas sont **ignorés en silence**.

**LA CHAÎNE DE RENDU EST EN DEUX BINAIRES.** Découvert le 2026-10-18 : la DLL
porte la logique et une API de rendu abstraite ; **`vfes.exe` porte la couche
Direct3D 11** — lui seul importe `d3d11.dll`, `dxgi.dll` et
`d3dcompiler_47.dll`. Tout l'outillage visait la DLL ; l'exe est presque
vierge. Toute question de rendu peut exiger d'ouvrir les deux.

## Les règles de travail, non négociables

- **Aucune supposition.** On lit le code, on mesure. Les observations de
  Frédéric à l'écran priment sur toute déduction.
- **Le code dit ce qui PEUT arriver, la mesure dit lequel est arrivé.**
- **Pas de sous-agents.** Tout doit être double-cliquable (`.cmd`).
- **Ne jamais patcher pendant que `vfes.exe` tourne** (`tasklist` avant).
- **Ne jamais lancer `tools/verifier_lanceurs.py` pendant une session.**
- **Ne jamais écrire directement un fichier du dépôt** : écrire à côté, puis
  `os.replace`.
- **Après chaque patch, relire les sites ET les relais dans la DLL PRODUITE,
  au désassembleur.** Jamais dans le script qui les écrit.
- **Montrer toutes les captures, sans verdict.** C'est Frédéric qui tranche.
- **Ne rien clore, ne rien annuler de sa propre initiative.** « On passe à
  autre chose » ne veut pas dire « on abandonne ». (Faute commise le 18/10.)
- Réponses courtes. Dire ce qui est **mesuré** et ce qui ne l'est pas.

## Les pièges qui ont coûté cette session

1. **Les heredocs bash mangent les échappements.** `b'\x00'` dans un
   `py -3 - <<'FIN'` devient un **octet nul réel** dans le fichier écrit, et
   Python refuse ensuite de le lire. Écrire les scripts avec l'outil Write,
   jamais en heredoc dès qu'il y a un `\x`.
2. **Un `je` court ne porte que 127 octets.** Un relais de 189 octets avec des
   sauts courts vers sa fin produit des déplacements **négatifs** : les sauts
   partent en arrière, dans du code quelconque. Utiliser `0f84 + disp32`. Vu
   au désassembleur avant tout essai — la règle de relecture a payé.
3. **Les adresses greffées bougent d'un patch à l'autre.** La table des tâches
   était en `0x180EB65F0`, puis `0x180EB4DC0`. On ne les note jamais : on les
   **retrouve**, et on vérifie le contenu (`slk` doit donner
   `WALL, WATER_RING, RIPPLE, SPLASH`).
4. **`0x420` est le même offset des deux côtés, sur deux objets différents** :
   champ de bits dans la DLL (`0x1802512D4`), début des données dans
   `vfes.exe` (`0x14002F567`). De quoi tourner en rond une après-midi.
5. **Une généralisation à partir d'un seul cas est une faute.** « Créneau 4
   vide = ne dessine pas » : faux, 11 tâches sur 23 sont dans ce cas, dont
   SNOW et THUNDER qui fonctionnent à l'écran.
6. **Les captures sont refusées si une fenêtre recouvre le jeu.** Ne rien
   lancer pendant une sonde avec captures.

## Les outils gagnés cette session

`tools/sonde_decor.py` sait désormais :

- **lire à travers un pointeur** : `--bp adr:nom:*0x180C414F8+0x759A0`
  (`[A]+B`) et `**0x180C414F8+0x759C0+0x20` (`[[A]+B]+C`). Rend quatre mots en
  hexa **et** en flottant — c'est le flottant qui parle ;
- **armer dans `vfes.exe`** : elle reconnaît le module à la base préférée de
  l'adresse (`0x140…` l'exe, `0x180…` la DLL) et choisit seule ;
- afficher `rdi`, `rsi` et `r8` en plus de `rax/rcx/rdx/rbx`.

Sauvegardes : `sonde_decor.py.avant_indirect`, `.avant_exe`.

---

# CHANTIER 1 — LA BRUME D'AOI (**ouvert**, non clos)

Tout est dans **`analysis/brume_anneau_aoi.md`** (963 lignes, sections A à P).

**Ce que c'est** : sur la borne Lindbergh, la brume d'Aoi est une **nappe au
ras du sol** qui noie tout jusqu'à une altitude donnée — les troncs
disparaissent par le bas, le plancher du ring **émerge**. C'est un brouillard
de **HAUTEUR**, pas un objet. Le fichier le dit : `fog_jn5.txt`, groupe 1,
`density 1.0`, `linear -2.5 1.0`. Final Showdown met ce groupe à **0**.

**Acquis, à ne pas refaire :**

- le chiffre de permutation change **les deux** programmes : le sommet mesure
  `-pos_w.y` au lieu de `pos_c.z` et lit `env[14]`, le fragment emploie
  `env[11]` ;
- **les quatre points donnent bien au décor cette permutation** — démontré :
  sans les programmes de sommets la brume **disparaît**, avec eux elle
  **revient** ;
- `env[11]` et `env[14]` sont à **zéro** ; `env[4]` (le brouillard de
  distance, qui **marche**) l'est aussi dans ce tampon ;
- `[état + 0x420]` est le masque, `[état + 0x420 + offset]` les données, et
  l'état est `[[contexte]+0x38]` des deux côtés (contexte = `[0x180C414F8]`) ;
- l'offset vient du descripteur `[état + 0x18 + i*8]` (bits 24+, aligné 16),
  la taille des bits 16–27 ×16, le type `0x161` = flottant.

**Le patch** (`--fog-hauteur`) a été retiré du patcheur et la DLL repatchée
sans lui — **de ma propre initiative, ce qui était une faute**. Tout son code
est décrit sections J à O : les quatre points avec leurs octets, le relais
avec ses adresses, les valeurs (`env[11]` = `0,70 0,90 1,00 1,00` ;
`env[14]` = `1 / -1 / 0 / 0,285714`), les sauts longs.

**La piste la plus probable, et elle se vérifie SANS patcher** : `0x420` sert
de masque **et** de base des données. Si l'offset d'`env[14]` est petit, le
`or dword [rax+0x420], 0x4800` du relais **écrase les flottants qu'il vient
d'écrire**. Une sonde sur le descripteur donne l'offset réel.

Les deux autres pistes : le **moment** de l'écriture (le téléversement de
`vfes.exe` a peut-être déjà eu lieu pour la trame), et l'offset nul.

**Six fausses pistes closes**, toutes écrites comme telles : MOYA (ses données
sont entières, il est inscrit, instances 3 à 7), la file translucide de 40, le
pool de maillons, la borne d'instances auth_3d, le chargement de l'archive, la
table des 93 archives.

---

# CHANTIER 2 — LE MODE QUEST

Tout est dans **`analysis/mode_quest.md`** (2033 lignes). 323/323 fonctions
décompilées ; ce qui manque est **la carrière** (création de données, argent,
grade, W/L).

**Avancée du 2026-10-18 (§12)** : le point 2 du §4.3 demandait que
l'adversaire soit le **rival**, avec son **nom** et son **costume**.

- `0x1800B3470` range **deux** structures : le dossier de `0x5A0` à
  `objet + 0x68 + j*0x5A0`, **et** une table jusqu'ici inconnue de **`0x240`
  octets par joueur** à `objet + 0xBA8` ;
- **le nom affiché est `dossier + 0x05`, 21 octets** (20 caractères + nul) ;
- deux autres chaînes : `+0x1A` (11) et `+0x3C` (5) ;
- l'indice du joueur courant est en `objet + 0x48`.

**Ce qui reste** : la **tenue portée**. Soit parmi les scalaires du dossier
(`+0x25`, `+0x26`, `+0x28`, `+0x30`, `+0x38`, `+0x41`, `+0x48`,
`+0x50`…`+0x56`), soit dans la table de `0x240` — jamais lue. Le plus rapide
est de recouper avec **`ram/customize.bin`** (22 Ko), que `apm.dll` sauve
déjà : un dossier écrit sur disque dit ses champs mieux qu'un copieur de
3028 octets.

---

## Les autres chantiers en attente

- **Taka Arashi `so5` (60)** : les flashs d'appareil photo pendant le replay
  mais pas pendant « continue? ». `STGSO5_EFF_FLASH` est dans sa liste
  `auth_3d` ; aucune tâche d'effet sur ce décor.
- **L'eau d'Eileen `skb` (72)** : `analysis/eau_slk_console.md` et
  `eau_slk_donnees.md`. Le dernier verrou est la table de présence des
  permutations. `--eau-refraction` existe dans le patcheur, **inerte**.
- La planche de logos de l'écran-titre ; les pictogrammes PS3 dans
  OPTIONS/CONTROLS.
