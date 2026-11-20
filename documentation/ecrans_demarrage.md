# LES ÉCRANS DE DÉMARRAGE — CARTE, 2026-10-09

Relevé fait sur demande de Frédéric (« sur les 4 écrans de lancement, lesquels
sont supprimables sans causer de problème ? »).

**Mise à jour du même jour** : l'écran sur l'épilepsie a été retiré par `--sans-ecran-epilepsie` (journal 161). Les trois logos restent. Le reste de cette carte décrit toujours l'état d'origine.

## 1. Ce qui passe à l'écran, mesuré

`analysis/planche_demarrage.png` : vingt vignettes, une toutes les 1,5 s,
aucune entrée envoyée.

    2,0 - 3,5 s    « Presented by SEGA »
    5,0 s          « Created by AM R&D DEPT.#2 »
    6,5 - 8,0 s    « CRIWARE »
    9,5 - 12,5 s   l'avertissement sur l'épilepsie
    15,5 s         l'attract (combat de démo, PRESS START BUTTON)
    21,5 s et +    l'écran-titre FINAL SHOWDOWN

## 2. LES QUATRE ÉCRANS SONT UNE SEULE ANIMATION

`rom/2d/aet_n_adv.bin`, scène `MAIN`, composition racine : deux calques,
`logo_jpn` (1386 trames) et `logo_usu` (1002). En export c'est `logo_usu`.

Ses **marqueurs**, lus dans le fichier (60 images/s) :

| marqueur | trame | durée | ce qu'on voit |
|---|---:|---:|---|
| `REATING_s` … `REATING_e` | 0 – 259 | 4,3 s | classification d'âge — **déjà sauté** |
| `SEGA_s` … `SEGA_e` | 260 – 399 | 2,3 s | Presented by SEGA |
| `AM2_s` … `AM2_e` | 400 – 539 | 2,3 s | Created by AM R&D DEPT.#2 |
| `CRI_s` … `CRI_e` | 540 – 679 | 2,3 s | CRIWARE |
| `INFO_st` … `INFO_end` | 680 – 1000 | 5,3 s | avertissement épilepsie |

Les sous-compositions portent les mêmes noms : `segalogo_usu`, `am2`,
`crilogo`, `info`, et les images `n_adv_sega_usu.pic`,
`n_adv_logo_new_am2.pic`, `n_adv_cri.pic`.

## 3. Où le code choisit le début et la fin

`0x18006B880`, état 1 :

    0x18006BBD1  call 0x1802447C0          la region (--langue la force a 2)
    0x18006BBDA  lea rax, "SEGA_s"         <- LE MARQUEUR DE DEBUT
    0x18006BBE3  lea rcx, "logo_jpn"   /   0x18006BBF3  lea rcx, "logo_usu"
    0x18006BC01  lea r8,  "REATING_s"      (pris seulement si region == 1)
    0x18006BC1D  lea rax, "SEGA_e"
    0x18006BC24  lea rcx, "INFO_end"       <- LA FIN, si [0x180C3B701] == 0
    0x18006BC40  call 0x180029A90          joue

On joue donc **`SEGA_s` → `INFO_end`, soit 740 trames ≈ 12,3 s**.

**Deux `lea` de quatre octets commandent tout.** Les chaînes `AM2_s`, `CRI_s`,
`INFO_st`, `AM2_e`, `CRI_e` n'existent **pas** dans le binaire — il faudrait les
poser dans la greffe, comme les textes du menu.

## 4. CE QUI EST ACCROCHÉ À L'ANIMATION

**Le jingle SEGA est calé sur une trame.** `[tache+0x68]` reçoit `263.0`
(`0x43838000`) pour `logo_usu`, et la queue commune joue
`rom/sound/voice/sega441.adx` dès que la trame courante dépasse cette valeur :

    0x18006C36E  call 0x180029780          la trame courante
    0x18006C373  vcomiss xmm0, [rbx+0x68]
    0x18006C38B  "rom/sound/voice/sega441.adx"
    0x18006C399  mov dword [rbx+0x68], -1.0

Commencer **après** SEGA ferait donc jouer la voix dès la première trame, sur
l'écran suivant. Il faudrait neutraliser ce déclenchement en même temps.

**L'avertissement épilepsie est du TEXTE, pas une image.** Le dessin de la
tâche (`0x18006C490`) demande le libellé `0x36C` au resolveur `0x1801EFD10`
dès que l'état dépasse 3. C'est ce texte que `--sans-epilepsie` supprime
(`0x18006C4B6`) — **le fond `info` resterait, 5,3 s de noir**. Pour l'écran
entier il faut finir l'animation à `CRI_e`.

## 5. CE QUI N'EST PAS SUPPRIMABLE : LA MACHINE, PAS L'IMAGE

`0x18006B880` n'est pas un diaporama, c'est **le chargeur du jeu** : douze
états, table de saut en `0x1800...6C3D4` depuis `0x18006B971`.

| état | ce qu'il fait |
|---:|---|
| 0, 1 | démarre le son, ouvre l'animation des logos |
| 2, 3 | étapes intermédiaires |
| **4** | **charge** `EFFEFFCMN`, `STGCMN`, `NAGE_VF4`, et `se_system`, `se_fd`, `se_satellite`, `se_cs`, `se_adam` (`.csb`) |
| **5** | attend que tout cela soit prêt, puis aiguille vers 6, 8 ou 10 |
| 6 – 11 | `se_tv_cmn.csb`, `se_terminal.csb`, selon le mode |

Les états 1 à 5 **s'enchaînent sans attendre l'animation** : elle couvre le
chargement, elle ne le commande pas. Raccourcir l'image ne raccourcit donc le
démarrage que **tant qu'on reste au-dessus du temps de chargement réel** — en
dessous, on verra du noir au lieu des logos. Cette durée n'est pas mesurée ;
elle se mesure en coupant et en regardant.

## 6. Verdict par écran

| écran | durée | supprimable techniquement | ce qu'il faut savoir |
|---|---:|---|---|
| SEGA | 2,3 s | oui | le jingle `sega441.adx` est calé dessus — à traiter en même temps. Marque de l'éditeur. |
| AM2 | 2,3 s | **oui, sans rien d'accroché** | aucune chaîne du binaire ne le cite. Le plus simple des quatre. |
| CRIWARE | 2,3 s | oui | le middleware CRI tourne de toute façon (il lit les `.adx`, `.csb`, `.usm`) ; c'est une **mention de licence**, en général contractuellement exigée. |
| épilepsie | 5,3 s | oui | `--sans-epilepsie` n'en retire que le **texte**. Avertissement santé réglementaire sur un support commercial ; sur une borne privée, c'est un choix. |

Gain maximal en gardant SEGA : **9,9 s sur 12,3** (fin à `SEGA_e`).
