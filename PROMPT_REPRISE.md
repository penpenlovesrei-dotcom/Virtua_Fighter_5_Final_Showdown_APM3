# Reprise — Virtua Fighter 5 Final Showdown, build arcade APM3

*À jour du 2026-09-05. Colle ce fichier entier comme premier message.*

---

Tu reprends un chantier de rétro-ingénierie sur **Virtua Fighter 5 Final
Showdown, build arcade APM3** (carte SEGA ALLS). Atelier :
`C:\Users\frede\Desktop\VF5RE`. Écris en français.

Le moteur est `runtime/media/vf5fs/vf5fs-pxd-w64-Retail_APM3.dll` (3,4 Mo, base
`0x180000000`), lancé par `vfes.exe`. **Ne lis jamais le binaire patché pour
analyser** : lis `vf5fs-pxd-w64-Retail_APM3.dll.origine`, et passe `--origine`
aux outils. Le patcheur repart toujours de l'origine, donc un correctif retiré
de la ligne de commande disparaît vraiment.

Le but du chantier : ce build arcade contient tout le **mode console** (dix
modes, 55 sous-états, l'arbitre de fin de combat) mais des maillons en ont été
retirés ou bouchonnés. On les refabrique, un par un, et on rend jouable ce qui
ne l'est plus.

---

## 1. Ce qui marche, validé à l'écran

Lanceur unique, double-cliquable : **`tools\console.cmd`**.

| | état |
|---|---|
| **Dural** | jouable dans la grille |
| **SINGLE PLAYER** | quatre modes affichés ; Arcade, Score Attack et License Challenge lancent le combat |
| **OFFLINE VERSUS** | à deux — clavier joueur 1, manette joueur 2 |
| **DOJO** | quatre lignes, `How to Play` ajoutée (déplacée depuis OPTIONS) |
| **TERMINAL** | avec son vrai décor `trm` |
| **OPTIONS** | quatre lignes, renommé depuis `HELP & OPTIONS` |
| **EXIT GAME** | dixième ligne du menu, ferme le jeu sans confirmation |
| **Échap** | quitte le mode courant |

Touches (joueur 1, clavier) : flèches, **Entrée = valider**, **W = annuler**,
X/C/V = croix/rond/triangle, Espace = SELECT, T/Y/U = L1/R1/R2, F1/F2 =
TEST/SERVICE, Échap = sortir.

---

## 2. LA TÂCHE EN COURS

**Score Attack et License Challenge lancent le mode Arcade, pas le leur.**

Le mode de jeu est le dword global **`0x180751010`** — vérifié : huit
références dans tout `.text`, balayage linéaire. Valeurs : `0` Arcade,
`1` Score Attack, `2` License Challenge, `3` Special Sparring, `4` Versus. Le
binaire le confirme lui-même (`0x1800B8B9F cmp eax,3 ; ja` : au-dessus de 3, il
ne lit plus les réglages solo).

**Le piège, payé à l'écran** : il y a deux poseurs voisins.

    0x18019C490  mov [0x180751010], ecx ; ret     <- le mode SEUL
    0x18019C4A0  mov [0x180751010], ecx           <- le mode ET le bloc entier
                 mov [0x180751014], 0
                 mov [0x180751018], 0
                 mov [0x18075101A], 0
                 mov [0x18075101E], 0
                 puis recopie les reglages depuis [rdx]

`0x180751010` est la **première case d'un bloc de seize octets** qui porte aussi
la santé, le temps, les rounds et le niveau CPU. Poser le mode seul laisse le
reste tel que l'Arcade l'avait rempli : le combat démarre sur des réglages
incohérents et **plante**. C'est ce qui a été essayé et retiré.

Le chemin natif appelle `0x18019C4A0` avec une structure construite juste avant,
dans la mise à jour de la page du mode. Pour Score Attack, c'est
**`0x1801DD73E`**, gardé par le `je` de `0x1801DD700`.

**La direction** : ne pas poser le mode nous-mêmes. Laisser la page faire son
travail, et lancer **après** — donc se greffer dans la mise à jour, une fois le
`call 0x18019C4A0` natif passé. Commence par lire la garde de `0x1801DD700` et
la mise à jour `0x1801DD6A0` en entier.

**Un défaut connu, non corrigé** : `0x1800A48A0`, le validateur de Score Attack
où notre maillon est greffé, est cité par **trois** vtables (`0x18039A160`,
`0x1805326C8`, `0x180532728`). La greffe s'y déclenche pour les trois. Si un
combat se lance depuis un écran inattendu, c'est de là.

**Special Sparring** ne lance rien : il n'a pas de page de réglages, il passe
par la fabrique `0x1801A5E90`. Son point d'ancrage existe pourtant —
`TaskMenuTeam::validate` `0x1801A4390`, dont le premier appel est à
`0x1801A4399`, même forme que les trois autres.

---

## 2 bis. La piste qui vaut le détour : le réseau

Découvert le 2026-09-05, pas encore entamé. **Le netcode de bornes liées est
entier dans le binaire.** Vingt-trois classes RTTI, du démarrage à la fin de
partie :

    AVLinkMainStateStartup / Setup / Standby / Unavailable
    AVLinkMainStateMatchingAllocate / ChannelBind / ConnectivityCheck
                                    / Match / QualityCheck / WaitReady
    AVLinkMainStatePlaying / PlayEnd / CleanupMatch
    AVLinkReceiveThread  AVLinkSend  AVPacketGate  AVPacketMediator
    AVSendPacket  AVReceivePacket  AVTaskSession

Et le transport est câblé : le moteur importe **quatorze fonctions de
`ws2_32`** (`socket`, `connect`, `sendto`, `recvfrom`, `WSAIoctl`…). `vfes.exe`
n'en importe aucune : le réseau est dans le moteur, pas dans l'hôte.

Le déterminisme est établi **par le jeu lui-même** : il sait rejouer un combat
(`AVTaskGameVsReplay`, `AVTaskRobShortReplay_Rec`, scènes `REPLAY_VS`,
`ROB_SHORT_REPLAY_REC`). Un rejeu suppose une simulation déterministe pilotée
par des entrées enregistrées.

À l'inverse, le rollback de R.E.V.O. est **absent** d'APM3 (0 occurrence de
`Rollback`, `EOS_`, `SteamAPI`), et le transplanter n'a pas de plan de coupe :
les deux DLL sont des frères aux dispositions différentes, et ce serait recopier
du code de SEGA.

**L'ordre de travail** : cartographier `AVLinkMain*` et `AVTaskSession`, voir où
la machine s'arrête et ce qu'elle attend d'ALL.Net, puis faire répondre notre
`apm.dll` — c'est le rôle qu'elle tient déjà pour les entrées et les pièces.
Tout est dans `analysis/reseau.md`.

---

## 3. Les pièges de ce binaire, tous payés au moins une fois

- **Patcher le site d'appel, jamais le corps.** Les prédicats bouchonnés sont
  partagés par des centaines d'appelants : `0x180007450` (rend faux) en a 210,
  `0x180007430` (`ret 0`), `0x180007440`, `0x180029FB0` (rend vrai). Le sens est
  dans l'appel.
- **`.pdata` ne liste pas les FEUILLES**, et une fonction couvre souvent
  plusieurs entrées chaînées. Toute affirmation « personne n'appelle X » exige
  un **balayage LINÉAIRE de `.text`** par motif d'octets. Une itération sur
  `.pdata` ne donne qu'un minorant, et a produit plusieurs conclusions fausses.
- **`+0x224` d'une page est le DERNIER INDICE, pas un compte** : la boucle de
  dessin va de 0 à lui INCLUS. Le porter de 9 à 10 a ajouté une rangée qui
  lisait les libellés hors bornes.
- **Les tables de modes et de sous-états sont indexées par leur champ `+0x00`**,
  pas par leur position.
- **Ne pas neutraliser une garde partagée.** `--menu-ranking` avait débranché le
  `jne` de `0x1801DC650` pour lever une attente : ça a débranché la suspension
  du menu pour les cinq sous-menus. Soigner ce qui remplit la variable, pas la
  garde qui la lit.
- **Une fonction voisine n'est pas la même fonction.** Deux fois cette
  session : `0x1800D7130` (éclairage) pris pour le chargeur de décor
  (`0x18018FCF0`), et `0x18019C490` pris pour `0x18019C4A0`.
- **Mesurer avant de corriger.** Chaque cause supposée plutôt que mesurée s'est
  révélée fausse à l'écran. Les sondes `tools/pister_*.py` existent pour ça, et
  elles écrivent leur relevé **au fil de l'eau** — le débogueur se bloque
  parfois en fin de session et un bilan écrit à la fin serait perdu.
- **Les heredocs `bash` mangent les antislashs.** Écrire du Python contenant
  `\n` ou `\x00` par heredoc corrompt le fichier. Utiliser l'outil Write, ou
  `os.linesep` / `bytes(4)`.
- **`python` est un stub inerte** sur cette machine : lancer `py -3`.

---

## 4. Les outils

Tous dans `tools/`, Python 3, dépendances `capstone` et `pefile`.

| outil | rôle |
|---|---|
| `patch_moteur.py` | **le** patcheur. Chaque correctif est une option ; il repart toujours de `.origine` et REFUSE si les octets attendus ne sont pas là |
| `plage.py` | désassemble une **plage**, sans s'arrêter au premier `ret`. `--origine` obligatoire pour analyser |
| `carte_zone.py` | cartographie une zone entière : appelants, appelés, chaînes, bouchons |
| `libelles.py` | résout un identifiant de texte (`0x2F1`) ou cherche par texte |
| `renommer_libelle.py` | réécrit un libellé **sur place** dans le `.par` ; refuse si le `.par` a plus d'un lien dur |
| `sllz.py` | index PARC et décompression SLLZ ; `sllz.Par(chemin).entrees()` |
| `instrument.py` | le débogueur : points d'arrêt logiciels, contexte, lecture mémoire |
| `pister_*.py` | une sonde par question. Modèle à copier pour la suivante |
| `gen_apm_stub.py` | génère `apm.dll`, la bibliothèque de substitution de la carte arcade (entrées comprises) |

**Après `construire_stub.cmd`, remettre `apm_entrees.txt` en jeu manuel** : le
modèle redéploie un scénario qui presse START tout seul à 25 s et 33 s. Et
`front = 10` — la fenêtre de `Input_isOnNow` doit rester **plus courte qu'une
trame** (16,7 ms), sinon chaque appui valide deux fois.

---

## 5. Les cavernes, et ce qu'il en reste

Il n'y a pas de section libre : on greffe dans du code mort.

| caverne | taille | état |
|---|---:|---|
| `.text` fin de section `0x18034575C`–`0x180345800` | 164 o | ~150 utilisés (dojo, transition, versus, sortie, libellé) |
| raccourci désactivé `0x1801A7C89`–`0x1801A7CDB` | 82 o | 65 utilisés (relais How to Play du Dojo) |
| cas « How to Play » mort `0x1801A703D`–`0x1801A707D` | 65 o | 2 cavernes de lancement |
| cas « Credits » mort `0x1801A71D8`–`0x1801A71FC` | 37 o | 1 caverne de lancement |

Les deux derniers ne sont morts **que si `--options-sans-howto` est appliqué**,
et le second **que si `--options-raccourci` l'est** aussi. Les options qui s'en
servent le vérifient et refusent sinon.

---

## 6. Où lire

| document | sujet |
|---|---|
| `REPRISE.md` | le journal du chantier, séance par séance |
| `analysis/machine_console.md` | les deux tables : dix modes, 55 sous-états |
| `analysis/menu_console.md` | le menu console, entrée par entrée, et les neuf maillons (§19 = SINGLE PLAYER) |
| `analysis/mode_de_jeu.md` | le champ du mode de jeu et ses lecteurs |
| `analysis/mode_selector.md` | `MODE_SELECTOR`, et le **chaînage des modes** (`+0x20` liste, `+0x60` successeur) |
| `analysis/carte_options.md` | l'écran d'options, son curseur, la disposition des touches |
| `analysis/dural.md` | la grille et le déblocage de Dural |
| `analysis/couverture_console.md` | ce qui est lu, et ce qui ne l'est pas (~10 % des 8 541 fonctions) |
| `analysis/reseau.md` | **le netcode de bornes liées, intact dans le binaire** |

Publié : **https://github.com/penpenlovesrei-dotcom/Virtua_Fighter_5_Final_Showdown_APM3**
(analyse et outils seulement, aucune donnée de jeu). Le dépôt local est
`C:\Users\frede\Desktop\VF5RE-public` — y recopier les documents et commiter
pour publier la suite.

---

## 7. Comment travailler avec Frédéric

- Il juge **sur l'image**. Livrer une capture ou un lanceur, pas un verdict.
- **Toujours un lanceur `.cmd`**, double-cliquable, jamais une ligne de commande
  à recopier.
- Ne pas proposer d'arrêter, ni demander « on continue ? ». Rendre la main
  seulement pour une vraie question ou un essai à faire.
- Une observation de sa part est un **point de départ d'analyse**, pas une
  valeur à régler à la vue.
- Quand il signale un défaut après une séance de correctifs, **relire ses
  propres patchs avant de désassembler le moteur**. C'est arrivé deux fois.
