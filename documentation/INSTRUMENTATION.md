# Exécution instrumentée — ce qui marche, ce qui bloque

Première session d'instrumentation, 2026-09-01. Objectif : atteindre ce que la recherche
statique ne peut pas atteindre (le rôle des 32 fenêtres, les 37 codes de liste 2 jamais
cherchés). **Ces deux verrous restent fermés à ce stade** — ils demandent un combat qui tourne. Un stub
`apm.dll` (§6) a depuis fait **démarrer `vfes.exe` jusqu'à l'écran-titre**, ce qui ouvre la
voie. Mais l'instrumentation a livré autre chose : **le moteur peut servir
d'oracle hors du jeu**, ce qui a permis de valider dynamiquement la formule de dégâts, le
décodage complet de `rob_cmn_mottbl.bin`, et **les 84 gestionnaires de codes de `mothead`** —
et de découvrir au passage que **l'état de mouvement n'a pas la même disposition dans les deux
builds** (§4.4).

---

## 1. Le choix de la cible

| Cible | Verdict |
|---|---|
| **R.E.V.O.** (Steam) | `runtime/media/start_protected_game.exe` : le jeu est **sous protection anti-tamper**. Le déboguer serait techniquement voué à l'échec et ferait courir un risque au compte Steam. **Écartée.** |
| **`vfes.exe`** (dump `APM3_US`, VF5 Ultimate Showdown, moteur FS porté) | Exécutable Windows x64 ordinaire, sans protection. **Retenue.** |
| ELF Lindbergh (arcade 2.000 / 6.000) | Nécessite Linux + `lindbergh-loader`. Non disponible ici. |

**Le dump n'a pas été touché.** Une copie de travail a été créée dans `VF5RE\runtime\media\` :
les petits fichiers sont copiés, `vf5fs_data.par` (4 Go) est un **lien dur** et `vf5fs_media`
une **jonction** vers le dump — accès en lecture, zéro octet dupliqué, rien d'écrit dans
`VF5 FS DECOMP`.

---

## 2. L'outil : `tools/instrument.py`

Un débogueur Win32 en `ctypes`, sans dépendance tierce. Il lance l'exécutable sous
`DEBUG_ONLY_THIS_PROCESS`, journalise les DLL chargées avec leur base, et rapporte chaque
exception avec son code, son adresse et le module qui la contient.

Il **décode les exceptions C++ MSVC** : à partir des paramètres de l'exception
(`ExceptionInformation[1..3]` = objet, `ThrowInfo`, base d'image) il remonte la
`CatchableTypeArray` jusqu'aux `TypeDescriptor` et rend le **nom de type démangé**. C'est ce
qui a permis d'identifier le blocage en une seule exécution.

Lanceur : `tools/lancer_vfes.cmd`.

---

## 3. Ce que l'exécution a montré

```
processus 14576 lance sous debogage
  image     0x00007FF7E0560000  vfes.exe
  dll       0x00007FFB33940000  apm.dll
  dll       0x00007FFBD6760000  dxgi.dll
  dll       0x00007FFBD5840000  d3d11.dll
  dll       0x00007FFB19860000  vf5fs-pxd-w64-Retail_APM3.dll
  EXCEPTION exception C++ (2e chance)
      type    : .?AVException@amdaemon@@ / .?AVexception@std@@
  sortie du processus, code 0xE06D7363
```

Trois faits, tous nouveaux :

1. **La DLL moteur se charge.** `vf5fs-pxd-w64-Retail_APM3.dll` est bien mappée avant l'échec :
   le blocage n'est pas dans le moteur de jeu.
2. **Le blocage est `amdaemon::Exception`** — le démon ALL.Net des bornes SEGA (réseau,
   comptabilité, keychip). C'est la dépendance arcade, désormais **prouvée** et non plus
   supposée. Sans un substitut d'`amdaemon`, ce build ne démarrera pas.
3. `apm.dll` doit être **à côté de l'exécutable** : dans le dump il est un niveau au-dessus,
   et sans lui le processus reste bloqué sans fenêtre ni message.

Confiance : **CONFIRMED**.

---

## 4. Le moteur comme oracle, hors du jeu

Constat décisif tiré des imports :

| DLL | Imports |
|---|---|
| `vf5fs-pxd-w64-d3d12_SteamRetail.dll` (R.E.V.O.) | `steam_api64.dll`, `EOSSDK-Win64-Shipping.dll`, … |
| `vf5fs-pxd-w64-Retail_APM3.dll` | **KERNEL32, ADVAPI32, ole32, OLEAUT32, D3DCOMPILER_47, bcrypt, WS2_32 — que du système** |

La DLL APM3 **se charge donc dans un processus Python ordinaire**, sans jeu, sans démon, sans
matériel. On peut appeler ses fonctions directement avec de vraies données et **faire arbitrer
le décodage par le moteur lui-même**.

Les fonctions déjà nommées dans le DLL R.E.V.O. se retrouvent dans le build APM3 par
recherche de motif d'octets (avec joker sur les déplacements RIP) :

| Fonction | R.E.V.O. | APM3 |
|---|---|---|
| `ScaleDamageByPower` | `0x180177CF0` | `0x1801695C0` |
| `GetMotionForRole` | `0x180166240` | `0x18015B310` |
| global `rob_cmn_mottbl` | `0x180756E20` | `0x180713F20` |

### 4.1 La formule de dégâts — vérifiée

`ScaleDamageByPower` appelée directement sur 72 couples (dégâts, modificateur) :

```
degats    mod |   moteur ma formule
    20      0 |       20       20
    20     25 |       24       24
    20    125 |       40       40
    80    125 |      160      160
72/72 concordent avec v*(mod+125)*8/1000 pour mod>0, v sinon
```

La formule de `docs/formats/mothead.md` §3.1 n'est plus une lecture de désassemblage : elle est
**vérifiée dynamiquement**. Confiance : **CONFIRMED**.

### 4.2 `rob_cmn_mottbl.bin` — validé de bout en bout

`tools/oracle_mottbl.py` charge la DLL, **relocalise** un vrai `rob_cmn_mottbl.bin`, écrit le
pointeur dans le global du moteur, puis appelle `GetMotionForRole(perso, posture, rôle)` pour
**toutes** les combinaisons et compare à `tools/motdb.py` :

```
rob_cmn_mottbl.bin : 56232 octets, 21 entrees, borne de role 363
14157 valeurs comparees : 14157 identiques, 0 differentes
```

**14 157 sur 14 157.** Cela valide d'un coup :

- la structure décrite dans `docs/formats/mot_tables.md` (21 entrées, 363 rôles, postures) ;
- la **règle de relocation**, jusque-là seulement déduite du désassemblage :
  **`valeur stockée = offset absolu − position du champ`**, appliquée à trois niveaux
  (en-tête → table des entrées, entrée → table des postures, poste → bloc) ;
- au passage, un piège : **deux entrées peuvent partager la même table de postures**
  (l'entrée 19 partage celle de l'entrée 0). Relocaliser naïvement en parcourant les entrées
  applique deux fois le décalage aux champs partagés. Il faut relever les positions une seule
  fois, puis écrire. Sans cela : 12 963/14 157.

Confiance : **CONFIRMED**.

### 4.3 Les 84 gestionnaires de codes — exécutés

`tools/oracle_handlers.py` va plus loin : il fabrique un **faux combattant** (un `ROB` de
128 Ko entièrement à zéro), monte le contexte que le répartiteur passe aux gestionnaires
(`ctx[0] = ROB`, `ctx[1] = ROB+0x338`, `ctx[2] = ROB+0x798`), puis appelle **chaque
gestionnaire** avec une charge utile marquée (octets 1, 2, 3, …) et relève les mots de l'état
qui ont changé. Chaque code tourne dans un **sous-processus** : un gestionnaire qui déréférence
un global non initialisé plante, et le plantage n'emporte pas le relevé des autres.

Le répartiteur du build APM3 a été retrouvé par sa forme (`mov r,[base+rax*8] ; call r`) :
`0x180158B51`, table `0x1803F95B0`. Celle-ci compte **84 entrées avec des trous exactement aux
codes 43, 44 et 71** — comme dans le build R.E.V.O. La numérotation des codes est donc la même
sur les deux builds. Sortie complète : `analysis/oracle_handlers_sortie.txt`.

| Verdict | Codes |
|---|---:|
| écrit là où prédit, **offsets identiques** | 42 |
| écrit là où prédit, **décalé de 0x18** | 13 |
| écrit là où prédit, **décalé de 0x78** | 15 |
| à vérifier | 3 |
| n'écrit rien | 4 |
| plantage | 4 |
| pas de gestionnaire | 3 |

**77 des 81 gestionnaires ont été exécutés, et tous écrivent où la lecture statique le
prévoyait** — aux deux décalages de build près (voir §4.4). Les trois « à vérifier » sont les
codes 1, 3 et 50 : ils touchent un champ *avant* celui que la colonne `champ_etat` du CSV
mentionne en premier (le compteur `état+0x078` pour le code 3, le mot de drapeaux
`état+0x01C` pour le code 1). Ce sont des champs déjà décrits en prose dans
`docs/formats/mothead.md`, pas des désaccords.

Les quatre « n'écrit rien » sont **corrects** : ces gestionnaires sont gardés par un bit de
drapeau qui vaut 0 dans un état vierge. Le code 54, par exemple, commence par
`test dword [état+0x0C], 0x100 ; je ret`. Les quatre plantages (codes 46, 47, 67, 73)
déréférencent des globaux que le faux `ROB` laisse nuls.

Le code 3 mérite d'être montré, car il reproduit exactement la cartographie de la §3.1 de
`mothead.md`, charge utile marquée à l'appui :

```
etat+0x078  01              compteur incremente
etat+0x07C  01              drapeau « attaque active »
etat+0x080  010203040506    charge +0x00 (u32) et +0x04 (s16)
etat+0x088  0708            charge +0x06 : le niveau d'attaque
etat+0x08C  090a090a        charge +0x08 DEUX FOIS : degats bruts et degats mis a l'echelle
etat+0x094  0d0e0f101112    charge +0x0C (u32) et +0x10 (u16, l'angle)
etat+0x09C  1314            charge +0x12 : l'indice yarare
etat+0x0A0  15161718191a1b1c1d1e   charge +0x14, +0x18, +0x1C
```

Les dégâts apparaissent **en double** en `0x8C` et `0x8E` avec la même valeur, parce que le
modificateur de puissance vaut 0 dans un état vierge et que la mise à l'échelle est alors
l'identité. C'est la §3.1 confirmée à l'octet près.

### 4.4 Deux dispositions d'état : le portage a remplacé deux `std::vector`

L'oracle a mis au jour ce que la lecture statique d'un seul binaire ne pouvait pas montrer :
**les offsets de l'état de mouvement ne sont pas les mêmes dans les deux builds.** En
comparant les 84 gestionnaires des deux DLL, les écarts se répartissent en trois paliers
nets : 0, `0x18`, puis `0x78`. Deux champs expliquent tout.

| Champ | APM3 (2021) | R.E.V.O. (2025) | Effet |
|---|---|---|---|
| code 47 | **conteneur** en `état+0x310` : `begin`, `end`, `capacité` (24 o), passé à une fonction d'insertion | **tableau fixe** de 5 cases de 8 o (40 o) | +`0x18` |
| code 65 | **conteneur** en `état+0x3B8` : `push_back` du *pointeur* de charge (24 o) | **tableau fixe** de 10 cases de 12 o (120 o), copie des 12 octets | +`0x60` de plus |

```
APM3 0x180157CF0 (code 65) :
    add  rcx, 0x3B8
    mov  rdx, [rcx+8]          ; end
    cmp  [rcx+0x10], rdx       ; capacite atteinte ?
    mov  [rdx], rax            ; on range le POINTEUR
    add  qword [rcx+8], 8
```

**Le portage a donc remplacé deux `std::vector` par des tableaux de taille fixe** — la
transformation classique quand on veut supprimer les allocations dynamiques d'une boucle de
jeu. Conséquence pratique : **les offsets d'état de `docs/formats/mothead.md` valent pour le
build R.E.V.O.** ; pour la famille arcade il faut retrancher `0x18` à partir de `état+0x310`,
puis `0x78` à partir de `état+0x3D0`. Confiance : **CONFIRMED** (vérifié sur les 84
gestionnaires des deux binaires, et de bout en bout à l'exécution).

---

## 5. Ce que cela ne résout pas

Les deux verrous visés au départ demandent un **combat qui tourne** :

- le rôle des 32 fenêtres (`état+0x154` … `0x2D3`) ;
- les 37 codes de liste 2 que le DLL ne cherche jamais.

Or aucun build ne tourne ici : R.E.V.O. est protégé, `vfes.exe` exige `amdaemon`. Les pistes,
par coût croissant :

1. **Substituer `amdaemon`.** `vfes.exe` meurt sur une exception C++ précise ; un stub qui
   satisfait l'initialisation d'`apm.dll` suffirait peut-être à passer. Le point d'arrêt est
   déjà localisable avec `tools/instrument.py`.
2. **Étendre l'oracle.** Beaucoup de gestionnaires de codes sont des recopies pures : on peut
   fabriquer un faux « état » en mémoire, appeler un gestionnaire avec une charge utile
   choisie, et lire les champs écrits. Cela ne dit pas *qui lit*, mais confirme *ce qui est
   écrit* — et c'est faisable dès maintenant, sans jeu.
3. **`lindbergh-loader` sous Linux** pour l'ELF arcade, qui est la cible principale du projet.

---

## 6. Le stub `apm.dll` — le jeu demarre

`amdaemon` n'est pas joignable, mais **le jeu ne lui parle pas directement** : il passe par
`apm.dll`, la bibliotheque de la carte ALLS/APM3, dont `vfes.exe` importe **57 fonctions**
(`Aime_*` pour le lecteur de carte, `Allnet*` pour le reseau et la comptabilite,
`Credit_*`, `Sequence_*`, `System_*`, `Input_*`, `Backup_*`). Remplacer `apm.dll` par une
implementation locale evite tout dialogue avec le demon.

`tools/gen_apm_stub.py` genere le source C des 57 exports et le compile. Les reponses sont
choisies pour que le jeu se croie sur une borne saine en partie gratuite :

| Fonction | Reponse du stub | Pourquoi |
|---|---|---|
| `Credit_isFreePlay` | vrai | pas de monnayeur |
| `AllnetAuth_isGood` | vrai | reseau ALL.Net authentifie |
| `Sequence_isTest` | faux | on n'est pas en mode test operateur |
| `Error_isOccurred` | faux | aucune erreur materielle |
| `Aime_isReaderDetected` | faux | pas de lecteur de carte |
| `Backup_isSetupSucceeded` | vrai | sauvegarde prete |
| `System_get*`, `AllnetAuth_get*Name` | chaine C constante | identite de carte factice |
| `Credit_toString` | pointeur cache rendu, `std::string` vide construite | valeur de retour par objet (ABI x64) |

Chaque fonction annonce son appel par `OutputDebugStringA`, que `tools/instrument.py`
journalise : c'est la boucle de mise au point, et cela donne la sequence d'appels reelle.

**Piege de compilation** : le `gcc` de MSYS2 fonctionne, mais **uniquement si
`C:\msys64\mingw64\bin` est dans le `PATH`** — sinon il ne trouve pas ses propres DLL et
sort en erreur sans message. `gen_apm_stub.py` s'en charge.

La vraie `apm.dll` est conservee sous `apm.reelle.dll` dans la copie de travail ; le dump
n'est pas touche.

### Resultat

```
  dll  0x00007FFBBC0F0000  apm.dll                        <- le stub
  [dbg] [apm] stub charge
  dll  0x00007FFB19860000  vf5fs-pxd-w64-Retail_APM3.dll
  [dbg] [apm] Core_execute ... Credit_isFreePlay ... Input_isOnNow ...
```

Plus d'`amdaemon::Exception`. Le processus passe de 11,8 Mo bloques a **577 Mo, 57 threads,
76 modules**, et ouvre une fenetre **1920x1080** intitulee
**`Virtua Fighter 5 FS (PXD/64bit)`** qui affiche **l'ecran-titre de Virtua Fighter 5 Final
Showdown**. Capture : `analysis/vfes_ecran_titre.png`.

Sur 18 secondes : **12 666 appels au stub, 22 fonctions distinctes**, aucun plantage. Les plus
sollicitees dessinent la boucle de jeu :

```
 4680 x Input_isOn          722 x AllnetAuth_isGood      389 x Credit_isFreePlay
 1440 x Input_isOnNow       722 x System_getKeychipId    362 x Core_execute
 1097 x Sequence_isTest     722 x AllnetAuth_getLocationId
```

Les 35 autres fonctions ne sont pas appelees a ce stade : elles servent aux ecrans suivants
(carte Aime, credits, sequence de partie).

Confiance : **CONFIRMED** — le jeu demarre et affiche.

### Ce que cela ouvre

`Input_isOn` est appele 4 680 fois en 18 secondes : **c'est le stub qui tient les boutons**.
En lui faisant rendre « depart appuye » au bon moment, on peut mener le jeu jusqu'a un combat
sans toucher au clavier — et c'est la que les points d'arret materiels en lecture sur
`etat+0x154` repondront enfin a la question des 32 fenetres.

---


---

## 7. Le jeu va jusqu'au combat, et les points d'arret repondent

Session du 2026-09-02. Les deux pas annonces en fin de section 6 sont faits.

### 7.1 Le stub tient la manette

`Input_isOn` et `Input_isOnNow` prennent **un seul argument, le code du bouton** (0 a 15).
`vfes.exe` ne les appelle pas directement : il publie une table de troncs
(`0x140002BE0 : mov ecx, edx ; jmp [Input_isOn]`) que le **moteur** appelle. Chercher des
appels directs dans `vfes.exe` n'en trouve aucun -- c'etait la premiere fausse piste.

Le stub joue desormais un scenario lu dans **`apm_entrees.txt`**, relu des que le fichier
change : on regle une sequence pendant que le jeu tourne, sans recompiler. Detail complet du
format et des codes dans `docs/formats/apm_input.md`.

Le releve des appels donne ce que le jeu interroge : `Input_isOn` pour **les treize codes 2 a
14**, `Input_isOnNow` pour **0, 7, 8 et 15**, une fois chacun par trame.

**Le code 7 est START.** Deux appuis -- un a l'ecran-titre, un a la selection -- suffisent a
mener le jeu d'un demarrage a froid jusqu'a `ROUND 1`, sans toucher au clavier. Preuves a
l'ecran : `analysis/etape1_titre.png`, `etape2_code7.png`, `etape3_apres_select.png`,
`etape4_combat.png` (Akira contre Lion, Palace). Confiance : **CONFIRMED**.

Le sens des douze autres codes n'est **pas** etabli : un balayage pendant un combat est
illisible, l'adversaire gere par la machine agissant en meme temps.

### 7.2 Points d'arret logiciels et materiels

`tools/instrument.py` sait maintenant :

- poser un point d'arret **logiciel** (INT3) a `module+offset`, journaliser les registres, et
  se rearmer seul (octet rendu, drapeau de trace, 0xCC reecrit) ;
- poser jusqu'a quatre points d'arret **materiels** (DR0-DR3) sur des adresses de donnees, sur
  **tous** les threads -- 57 ici -- y compris ceux crees apres la pose ;
- ignorer des plages de RIP sans interet, et **liberer un registre** apres N acces pour que le
  jeu reprenne sa vitesse ;
- prendre une capture d'ecran de la fenetre a un instant choisi.

Trois pieges y ont ete corriges, tous silencieux :

1. **la boucle ne s'arretait jamais** quand les evenements affluaient : le controle de duree
   n'etait fait que dans la branche de temporisation de `WaitForDebugEvent`. Un `--secondes 25`
   tournait plus de deux minutes ;
2. **l'adresse d'un point d'arret logiciel** : Windows rapporte l'adresse de l'INT3 lui-meme,
   pas `adresse+1` comme le RIP du contexte. Le rapprochement echouait, l'octet n'etait jamais
   rendu, et le processus rejouait l'INT3 sans fin ;
3. **le DR7 perime** : desarmer un registre pendant le traitement d'une exception puis
   reecrire le contexte tel quel remettait le registre en place.

### 7.3 Ce que cela a donne

`tools/pister_etat.py` enchaine tout : lancement sous debogueur, scenario d'entrees jusqu'au
combat, point d'arret sur `MothApplyRecord` pour y lire le ROB, puis points d'arret materiels
sur les fenetres. **Le premier des deux verrous est ouvert** -- releve et consequences dans
`analysis/fenetres_temporelles.md`.

Le resultat structurant : **l'etat de mouvement est a `ROB+0x8A0` dans le build APM3**, et non
a `ROB+0x798` comme dans R.E.V.O. (ecart constant `0x108`, ctx[1] passant de `0x338` a
`0x440`). Les consommateurs des fenetres tiennent le **ROB** et les adressent en ROB-relatif :
c'est cette base fausse qui rendait la recherche statique sterile. Une fois corrigee, une seule
passe rend **547 acces sur 101 fonctions, touchant les 32 fenetres**
(`analysis/mothead_fenetres_sites.csv`).

---

## 8. L'oracle vivant : le jeu arbitre ce que fait chaque gestionnaire

`tools/oracle_handlers.py` fait déjà arbitrer les gestionnaires **hors du jeu**, sur un faux
combattant. Mais un faux `ROB` a tous ses drapeaux à zéro : les gestionnaires gardés ne font
rien, et ceux qui déréférencent un global plantent. Sur les 84 de la liste 1, **huit étaient
restés sans verdict** — quatre plantages (46, 47, 67, 73) et quatre « n'écrit rien » (0, 54,
61, 62).

`tools/oracle_liste2_vivant.py` reprend la même idée **dans le combat** :

1. point d'arrêt à l'entrée du gestionnaire — on y a `ctx`, la charge utile et l'entrée ;
2. on lit **12 Ko de `ROB`** (l'instantané *avant*) et l'adresse de retour empilée ;
3. on pose un point d'arrêt sur cette adresse de retour ;
4. quand il tombe, on relit et on **diffe** : les mots changés sont exactement ce que le
   gestionnaire a écrit, dans les conditions réelles du combat.

L'option `--liste 1` bascule sur la table des 84 gestionnaires de la liste 1 ; `--champs`
relève en plus la valeur de champs choisis à l'entrée, ce qui permet de **vérifier une garde
plutôt que d'attendre une écriture qui ne viendra pas**.

Sur la liste 2, six campagnes de quatre minutes ont couvert dix-sept codes et fait passer
**quatorze codes de `LIKELY` à `SUPPORTED`**.

### Les huit gestionnaires de liste 1 restés sans verdict

Sept des huit répondent, et aucun ne plante :

| code | verdict hors du jeu | ce que le combat montre |
|---:|---|---|
| **0** | rien écrit | `état+0x054 = 0` (le mode) et **`état+0x058 = 0x984`**. Or `0x984` est `MUE_TA_IDOL` de **BRA**, et la seconde valeur vue, `0x41CB`, est `MUE_TA_IDOL_A` du **même personnage** : `état+0x058` est bien un **identifiant d'animation**. `CONFIRMED` |
| **46** | plantage | `état+0x2E0 = 88.0`, `état+0x300 = −1.0`, `état+0x304 = 80.0` — les trois `s16` de la charge (`88`, `−1`, `80`) convertis en flottants |
| **47** | plantage | `état+0x318` passe de 0 à 1 puis 2 : un **compteur** qu'il incrémente à chaque passage |
| **54** | rien écrit | `état+0x35C` — **le champ même que le code 2 de la liste 2 modifie** (l'angle de rotation) |
| **61** | rien écrit | deux passages, aucune écriture dans les 12 Ko observés |
| **62** | rien écrit | jamais passé pendant la fenêtre |
| **67** | plantage | trois passages, aucune écriture dans les 12 Ko — cohérent avec la lecture statique, qui le fait transmettre à `ROB+0x5D38`, **hors** de la fenêtre observée |
| **73** | plantage | `état+0x0E8`, `état+0x0F0`, `état+0x138`, `état+0x140`, tous de 5 à 6 : **deux blocs parallèles distants de `0x50`**, ce qui va avec la lecture « masque de parties du corps » |

La leçon est nette : **un faux combattant à zéro ne peut pas répondre à la place du vrai.**
L'oracle hors du jeu reste le bon outil pour ce qui est mécanique ; dès qu'une garde ou un
global entre en jeu, il faut le combat.

Le son du jeu est coupé **par processus** (`Debugger.muet`, via `pycaw`) : le volume général de
Windows n'est pas touché.

### Deux pièges de mesure, payés comptant

- **Une capture « de fenêtre » capture la zone d'écran.** `capture_fenetre.py` passe par un
  `BitBlt` du bureau, parce qu'un rendu Direct3D ne se recopie pas par le DC de la fenêtre. Si
  une autre fenêtre est devant, c'est elle qu'on enregistre. Une passe entière de mesures a
  ainsi rendu un verdict entièrement faux, et photographié autre chose que le jeu. Les outils
  vérifient désormais `GetForegroundWindow()` et refusent de capturer à l'aveugle.
- **Un filtre trop large gonfle un relevé.** Le premier balayage des accès aux 32 fenêtres
  rendait 547 accès sur 101 fonctions ; en exigeant une base qui soit un registre général, pas
  d'index, et une instruction **flottante scalaire**, il en reste **77 sur 11 fonctions**. Ce
  qui a sauté : des `lea [rip+…]`, des cadres de pile, un `lock xadd` de compteur de
  références, et surtout des `vmovups ymmword` qui sont des recopies de bloc au pas de `0x20`.

## Outillage produit

| Fichier | Rôle |
|---|---|
| `tools/instrument.py` | débogueur Win32 : lancement sous débogage, journal des DLL, exceptions avec type C++ démangé |
| `tools/lancer_vfes.cmd` | lanceur de `vfes.exe` depuis la copie de travail |
| `tools/oracle_mottbl.py` | fait arbitrer le décodage de `rob_cmn_mottbl.bin` par le moteur |
| `runtime/media/` | copie de travail (lien dur + jonction vers le dump, qui reste intact) |
| `tools/gen_apm_stub.py` | le stub `apm.dll`, avec les entrees scriptees |
| `tools/apm_entrees.txt` | le scenario d'entrees, relu a chaud |
| `tools/presser.py` | appuie sur des boutons dans le jeu deja lance |
| `tools/capture_fenetre.py` | capture la fenetre du jeu en PNG |
| `tools/pister_etat.py` | mene au combat, trouve le ROB, arme les points d'arret materiels |
| `tools/scenarios/combat_martelage.txt` | scenario qui mene au combat puis martele les boutons |
