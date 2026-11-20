# LA TABLE DE CORRESPONDANCE : NOS BOUCHONS, LEUR HOMOLOGUE REVO

2026-10-09. Demande de Frédéric : « pour chaque site bouchonné chez nous, le
site homologue dans REVO ».

**Le résultat dément l'attente de départ, et c'est le principal apport de ce
relevé** : le build arcade n'est pas un gruyère de coupes. Sur tout ce qui a pu
être apparié, **sept sites** seulement diffèrent — et la moitié d'entre eux sont
bouchonnés à juste titre.

## 1. Méthode

On ne compare pas des adresses. Deux passes :

**a. Par les vtables.** Les 353 classes communes, créneau par créneau, un
créneau étant « bouchonné » si sa cible est un corps de trois octets rendant une
constante (`xor al,al ; ret`, `ret 0`, `mov al,1 ; ret`, `xor eax,eax ; ret`).

**b. Par les fonctions, appariées sur une chaîne-ancre** — une chaîne citée par
**une seule** fonction et présente **une seule fois** dans le binaire, des deux
côtés. 1201 ancres communes, **375 paires de fonctions**.

Les bouchons se cherchent **par motif** dans `.text`, pas parmi les fonctions
`.pdata` : une fonction de trois octets n'a pas d'entrée `.pdata`, et le premier
jet en trouvait deux au lieu de treize.

## 2. PREMIER RÉSULTAT : LES VTABLES NE PORTENT AUCUNE COUPE

**Zéro** créneau bouchonné chez nous et pourvu dans REVO, sur 353 classes.

Les créneaux 5 et 6 des tâches sont bouchonnés **des deux côtés** — ce sont des
virtuelles inutilisées, comme `menu_console.md` 6.4 le disait déjà. Les vtables
de REVO ont simplement **un créneau de plus** (12 au lieu de 11, 8 au lieu de 7),
inséré en 2026, ce qui décale la suite :

    TaskOptionSetting   APM3 11 creneaux, bouchons [5, 6, 9]
                        REVO 12 creneaux, bouchons [5, 6, 10]

## 3. DEUXIÈME RÉSULTAT : LES VOLUMES SONT COMPARABLES

| | APM3 | REVO |
|---|---:|---:|
| bouchons distincts | 13 | 103 |
| fonctions en appelant un | 438 | 491 |
| sites d'appel | **988** | **1060** |

`xor al,al ; ret` : 210 appels chez nous, 189 chez REVO. **Ce n'est pas une
cicatrice d'arcade, c'est un idiome du moteur.**

## 4. LA TABLE — les sept sites

Fonctions appariées où **nous** appelons un bouchon et **REVO non** :

| ancre | APM3 | site | bouchon | REVO | verdict |
|---|---|---|---|---|---|
| `CLIP_CAUTION` | `0x1801AEA80` | `0x1801AEB09` | `0x180007450` FAUX | `0x1801BF3F0` → `call 0x1802C5110` | **prédicat réseau — correct** |
| `ONLINE_NG` | `0x1801DD190` | 3 sites | — | `0x180208EE0` → `0x1802C5110` ×2 | **prédicat réseau — correct** |
| `sync_io_buf` | `0x1801B23B0` | `0x1801B2462` | `0x180007450` FAUX | `0x1801C8950` → `call 0x1801C5390` | à lire (synchro d'E/S) |
| `TaskCsSystemSaveData(LOAD)` | `0x1801B7640` | `0x1801B7692`, `0x1801B769B` | `0x180007440` → 0, `0x180007450` FAUX | `0x1801D5FB0` | **le test a DISPARU — réparable** |
| `TaskCsSystemSaveData(SAVE)` | `0x1801B7960` | `0x1801B79A9`, `0x1801B79B2`, `0x1801B79F6` | idem + `0x180007430` | `0x1801D62A0` | **idem** |
| `ERASE_CONFIRM` | `0x1801CEEF0` | `0x1801CF23D` | `0x180029FB0` VRAI | `0x1801FA770` | forme réécrite |
| `CHAR SELECT / DATA SELECT` | `0x1801D02B0` | `0x1801D0576`… | `0x180029FB0` VRAI | `0x1801FBC20` | forme réécrite |

### CLIP_CAUTION — identique à l'instruction près

    APM3  0x1801AEB00  mov word [rbx+0x268], 0
          0x1801AEB09  call 0x180007450      <- xor al,al ; ret
          0x1801AEB0E  test al, al
          0x1801AEB10  mov ecx, 0x438
          0x1801AEB15  mov edx, 0x42D
          0x1801AEB1A  cmovne ecx, edx

    REVO  0x1801BF485  call 0x1802C5110      <- UNE VRAIE FONCTION
          0x1801BF48A  test al, al
          0x1801BF48C  mov ecx, 0x448
          0x1801BF491  mov edx, 0x43D
          0x1801BF496  cmovne ecx, edx

Les identifiants de texte ont glissé de 0x10, le reste est le même. Et
`0x1802C5110` de REVO lit l'objet de session `0x180EA6DF8`, interroge
`0x180C8DF28` et finit par `cmp al, 3 ; sete al` : **c'est « la session est-elle
établie ? »**. Sur une borne hors ligne, FAUX est la bonne réponse. Rien à
réparer.

### TaskCsSystemSaveData — REVO a supprimé le test

    APM3  0x1801B768E  test ebx, ebx
          0x1801B7690  jns 0x1801B7699
          0x1801B7692  call 0x180007440     <- rend 0  : « l utilisateur courant »
          0x1801B7697  mov ebx, eax
          0x1801B7699  mov ecx, ebx
          0x1801B769B  call 0x180007450     <- rend FAUX : « ce slot est-il monte ? »
          0x1801B76A0  test al, al
          0x1801B76A2  je 0x1801B7731       <- SORTIE : la tache n est jamais lancee
          0x1801B76A8  mov rcx, [0x180752148]
          0x1801B76AF  cmp ebx, [rcx+0x6718]
          0x1801B76B5  jne 0x1801B7731

    REVO  0x1801D5FD2  call 0x1802CCAB0     <- « cette tache tourne-t-elle deja ? »
          0x1801D5FD7  test al, al
          0x1801D5FD9  jne sortie
          ... puis l initialisation et le demarrage, SANS garde de peripherique

REVO n'a pas de « slot utilisateur monté » à vérifier : il écrit par
`user_storage::UserStorage`. **La garde a été retirée, pas réimplémentée** —
donc le correctif de notre côté serait de la court-circuiter, pas d'écrire une
fonction.

## 5. Ce que la table ne couvre pas

* **63 fonctions** appelant un bouchon chez nous n'ont pas d'ancre utilisable
  (aucune chaîne unique citée) : elles ne sont pas appariées.
* `ERASE_CONFIRM` et `CHAR SELECT` : REVO a réécrit la fonction, le squelette
  d'instructions ne se retrouve pas. Il faudrait les lire une à une.
* Les coupes qui ne sont **pas** des bouchons — comme le **tic absent** de la
  page de MENU (`0x1801DC620`, zéro appel à `0x1801BBB10`) — échappent par
  construction à ce relevé : il n'y a aucun `call` à chercher.

## 6. Ce qu'il faut en retenir

Trois cas de figure, et un seul mérite du travail :

1. **Prédicat réseau** (CLIP_CAUTION, ONLINE_NG, sans doute sync_io_buf) : le
   bouchon dit « pas de session », ce qui est **vrai** sur une borne hors ligne.
   Rien à faire.
2. **Garde de périphérique** (les deux `TaskCsSystemSaveData`) : REVO a retiré
   le test. C'est le seul endroit où la table dit quoi faire — court-circuiter.
3. **Fonction réécrite** : la comparaison ligne à ligne ne s'applique plus.

**Et la vraie leçon est ailleurs** : sur 988 sites, sept. Le mode console
d'APM3 n'est pas une ruine à reconstruire — c'est du code entier dont quelques
prédicats d'environnement rendent faux.
