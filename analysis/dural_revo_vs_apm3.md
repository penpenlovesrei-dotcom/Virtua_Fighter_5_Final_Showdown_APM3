# DURAL : la méthode REVO contre la méthode APM3

Demande de Frédéric, 2026-11-19 : « dans le chantier REVO, le déblocage de
DURAL a été fait d'une manière "plus propre" que pour la version APM3, tu peux
regarder la note à ce sujet, comparer les 2 méthodes, et modifier si nécessaire
la version APM3. »

**Verdict : INTRANSPOSABLE, et le bouchon en est bien la raison.** Rien n'a été
modifié. Le détail et les mesures qui le portent sont ci-dessous.

Tout ce qui est marqué **MESURÉ** a été lu dans les binaires au moment d'écrire
cette note, avec `VF5RE/tools/pe_disasm.py` sur les `.origine` et sur
`FS REVO/vf5fs-pxd-w64-d3d12_SteamRetail.dll`. Aucun jeu n'a été lancé.

Sources de raisonnement : `VF5RE/MODS/DURAL/LISEZ-MOI.md`, `dural.c`, `dural.h`
(14 novembre 2026) ; `VF5RE/code_decompile/MENU.md` §419.126 à §419.129 et
§419.412 ; `analysis/dural.md` §14 ; `VF5RE/analysis/dural.md` §15 et §15.6
(absent de l'extraction figée du 1er novembre) ;
`VF5RE/analysis/comparaison_builds.md` §9.1.

---

## 1. LES DEUX MÉTHODES FACE À FACE

| | **REVO** | **APM3** |
|---|---|---|
| binaire(s) touché(s) | **aucun** | `vf5fs-pxd-w64-Retail_APM3.dll` **et** `vfes.exe` |
| ce qui est touché | la mémoire du processus, par l'hôte, à chaque image | des octets sur le disque, une fois, par le patcheur |
| prédicat visé | `FUN_1801AA370`, **45 octets, réel** — MESURÉ | `0x180007450` = `32 C0 C3` → `xor al,al ; ret`, **2 octets, bouchon** — MESURÉ |
| ce que lit le prédicat | `[base+0x795928]` (le mode) **et** `FUN_1801CEEF0` → bit 5 de `[[base+0x796DB0]+0x1108C]` — MESURÉ | **rien du tout** : il n'a aucun accès mémoire — MESURÉ |
| nombre d'appelants du prédicat | **7**, et ce sont exactement les 7 sites du sélecteur — MESURÉ | **210 appels** (212 références, dont 2 `lea`) partagés par repliement COMDAT entre prédicats distincts — MESURÉ |
| nombre de sites à forcer | **0** | **7** (3 `call` + 4 bornes) |
| octets changés sur le disque | **0** | **22** (détail au §1.2) |
| drapeau/champ réellement porteur | le **mode** `[base+0x795928]`, mis à 0 pendant le sous-état 19 | aucun : c'est le **site d'appel** qui porte le sens, jamais un drapeau |
| repérage | **par décalage depuis la base du module** | **par adresse, mais contenu vérifié avant écriture** (REFUS si les 5 octets ne sont pas le `call` attendu) |
| réversible | **oui, totalement** : rien n'est écrit sur le disque, et `DuralArreter()` rend le mode au module | **oui** : le patcheur repart toujours de `.origine`, les originaux sont conservés |

### 1.1 REVO — ce qui est écrit, et où

Deux gestes, tous deux dans l'hôte, à l'exécution. `VF5RE/MODS/DURAL/dural.c`.

| geste | cible | taille | quand |
|---|---|---|---|
| bit de sauvegarde (§419.126) | `[[base+0x796DB0]+0x1108C] \|= 0x20` | 4 octets en mémoire | chaque image |
| mode (§419.129) | `[base+0x795928] = 0`, valeur d'origine restituée en sortant | 4 octets en mémoire | **seulement** pendant le sous-état 19 (SELECTOR) |

La chaîne, relue dans le binaire REVO au moment d'écrire cette note — MESURÉ :

```
0x1801AA370  mov ebx,[0x180795928]      ; le mode
             call 0x1801CEEF0           ; la sauvegarde
             test al,al ; je .faux
             cmp ebx,4   ; je .vrai     ; VERSUS
             lea eax,[rbx-6]
             cmp eax,2   ; jbe .vrai    ; 6, 7, 8
             test ebx,ebx ; sete al     ; et 0
0x1801CEEF0  call 0x1802CB780 ; test al,al ; jne .faux
             mov rax,[0x180796DB0]
             add rax,0x1108C
             mov eax,[rax] ; shr eax,5 ; and al,1
```

Les 7 appelants, MESURÉ (`xref 0x1801AA370`) : `0x17B8E7`, `0x17C41A`,
`0x17C963`, `0x17CA04`, `0x17CAA4`, `0x17EB66`, `0x1824F8`. Ce sont, un pour
un, les sept du `LISEZ-MOI`. Le dessin et l'accessibilité s'ouvrent donc
**ensemble**.

### 1.2 APM3 — ce qui est écrit, et où

Dix sites, 22 octets, deux binaires. Tous relus dans les `.origine` au moment
d'écrire cette note — MESURÉ.

| binaire | VA | avant | après | octets | rôle |
|---|---|---|---|---|---|
| DLL | `0x18016DC69` | `E8 E2 97 E9 FF` | `B0 01 90 90 90` | 5 | compositions `_dur` (dessin) |
| DLL | `0x18016E109` | `E8 42 93 E9 FF` | `B0 01 90 90 90` | 5 | idem |
| DLL | `0x18016E20B` | `E8 40 92 E9 FF` | `B0 01 90 90 90` | 5 | la case n'est plus désactivée |
| DLL | `0x18016EB2D`+2 | `12` | `14` | 1 | borne `cmp eax,0x12 ; jg` |
| DLL | `0x18016EC37`+2 | `12` | `14` | 1 | borne `cmp eax,0x12 ; jg` |
| DLL | `0x18016EEBA`+3 | `12` | `14` | 1 | borne `cmp r15b,0x12 ; ja` |
| DLL | `0x180172391`+2 | `12` | `14` | 1 | borne `cmp ebx,0x12 ; ja` |
| DLL | `0x1806490F0` | `00` | `01` | 1 | `--wxga` : les compositions `_dur` n'existent que dans la scène WXGA |
| `vfes.exe` | `0x140002D77`, imm. +3 | `01` | `11` | 1 | `is_dural_unlocked` dans `vf5fs_game_config_t` |
| `vfes.exe` | `0x140002DE7`, imm. +0 | `F0` | `FF` | 1 | ouvre le masque du `and`, pour que le quartet survive |

Les **sept substitutions** de `analysis/dural.md` §14.6 sont les sept premières
lignes : 3 × 5 + 4 × 1 = **19 octets**. `--wxga` et `--dural` ajoutent 3 octets
dans deux binaires, pour **22**.

### 1.3 APM3 aujourd'hui : `--options-dural` a déjà dépassé le §14.6

`VF5RE/analysis/dural.md` §15 (11 octobre 2026) — absent de l'extraction figée
du 1er novembre, c'est pourquoi `FS APM3/analysis/dural.md` s'arrête à §14.8.
Les **mêmes cinq octets** des trois sites ne portent plus `mov al,1 ; nop×3`
mais `call <prédicat de la greffe>` : un `call` fait cinq octets, `mov al,1` plus
trois `nop` aussi.

Le prédicat de la greffe (`dural_zone()` dans `VF5RE/tools/patch_moteur.py`,
lignes 367-424) rend 1 ou 0 selon trois bascules réglables dans
OPTIONS > Settings > Dural. Son entrée n'est **pas** le mode de jeu : c'est
**l'entrée de menu validée**, notée par un mouchard de 8 octets à
`0x1801DDF4C` (les deux instructions d'origine recopiées dans la greffe, puis
`jmp` de retour). Les 4 bornes restent en place, inchangées.

Coût ajouté : 8 octets à `0x1801DDF4C`, plus une zone de 0xC0 octets dans
l'emplacement `DUR` (0x300 octets) de la greffe.

---

## 2. EN QUOI LA MÉTHODE REVO EST « PLUS PROPRE » — EN TERMES MESURABLES

1. **Zéro site contre sept.** REVO ne force aucun site d'appel ; APM3 en force
   sept. Et ce n'est pas une préférence de style : chez REVO un seul bit sert
   les **7** appelants d'un coup (MESURÉ), parce qu'ils appellent tous le même
   prédicat réel. Chez APM3, forcer un site ne dit rien du suivant — c'est
   justement pour cela que les deux sites de **dessin** ont dû être trouvés
   séparément, après que la case fut atteignable mais pas dessinée (§14.4).
2. **Zéro octet sur le disque contre 22.** Aucun binaire n'est modifié chez
   REVO. Rien à sauvegarder, rien à restaurer, pas de `.origine` à tenir.
3. **Elle réutilise la règle de SEGA au lieu de la réécrire.** Le prédicat
   REVO décide lui-même, avec ses deux conditions d'origine (sauvegarde + mode
   dans {0, 4, 6, 7, 8}). APM3 doit **fabriquer** une règle dans sa greffe, et
   l'alimenter avec un **mandataire** (l'entrée de menu validée) au lieu de
   l'entrée véritable (le mode de jeu) — voir §4.
4. **Elle est réversible à chaud et son témoin peut échouer.** Éteindre
   `VF5_DURAL_MODE` doit revider la case, à l'image suivante, sans repatcher
   ni relancer. Chez APM3 le témoin existe aussi (`--options-dural 0,1,0`,
   vérifié à l'écran le 11 octobre, §15.7) mais il demande un repatch.

**Ce qu'elle n'est PAS, et il faut le dire :**

* **Elle ne survit pas mieux à une mise à jour du binaire.** C'est l'inverse.
  REVO repère tout par **décalage depuis la base du module** et ne contrôle
  aucun contenu : une mise à jour Steam déplace `0x796DB0`, `0x795928`,
  `0x1108C`, et le mod écrira à côté **sans rien dire**. Le contrôle à la
  compilation de `dural.c` ne protège que l'inclusion d'une plage dans une
  autre, pas les valeurs — le `LISEZ-MOI` §7 l'écrit lui-même. Le patcheur
  APM3, lui, **relit les octets attendus et REFUSE** si le contenu a changé
  (`patch_moteur.py` lignes 2264-2273, et `GRILLE_BORNES` de même). Sur ce
  seul critère, APM3 est le plus sûr des deux. La question est d'ailleurs
  théorique pour APM3 : son binaire est figé (avril/mai 2021) et n'est jamais
  mis à jour.
* **Elle coûte du temps à chaque image.** 22 octets posés une fois contre
  deux écritures par image, plus les gardes `PlageLisible`. Le §419.412 l'a
  payé : cinq `VirtualQuery` par image, **4,88 à 5,01 ms sur une image de
  19,6**, l'avant-bride de l'hôte tombant de 9,31 à 2,83 ms/image et le banc
  passant de 51,1 à 58,5 i/s après correction. Un patch statique n'a pas ce
  problème par construction.
* **Elle n'a qu'UN geste utile sur deux, et le `LISEZ-MOI` le présente
  autrement.** `MENU.md` §419.129 mesure : « il n'a été posé **qu'une fois**
  (aucune ligne `[419.127]`), donc rien ne l'efface, et Dural restait fermé.
  Le bit était déjà bon ; **ce geste ne sert à rien**, mais il ne nuit pas. »
  Le `LISEZ-MOI` §3.1, lui, écrit « NOTRE hôte effaçait le déblocage à chaque
  événement 0x3A » et en fait l'une des « deux fois où c'était nous » — alors
  que son propre §4 constate que le bit tient. **Les deux documents divergent,
  et c'est la mesure qui tranche : ce qui a débloqué Dural dans REVO est le
  geste sur le MODE, seul.** La méthode REVO est donc encore plus courte que
  son propre résumé : **un** geste, 4 octets en mémoire, pendant un seul
  sous-état.

---

## 3. EST-ELLE TRANSPOSABLE À APM3 ? NON, ET LE BOUCHON EN EST LA RAISON

**Réponse franche : INTRANSPOSABLE.** Trois mesures la ferment, et aucune n'est
une déduction.

**MESURE 1 — le prédicat d'APM3 ne lit rien.**

```
$ pe_disasm vf5fs-pxd-w64-Retail_APM3.dll.origine func 0x180007450
0x180007450  32c0   xor al, al
0x180007452  c3     ret
```

Deux octets, aucun accès mémoire. La méthode REVO consiste à **présenter au
prédicat un état qu'il autorise**. Il n'y a ici aucun état à présenter : quoi
qu'on écrive en mémoire, dans un drapeau, dans un mode, dans la sauvegarde,
`0x180007450` rendra 0. **Le bouchon est exactement ce qui rend les sept
substitutions nécessaires.**

**MESURE 2 — le drapeau de déblocage existe, il est déjà posé, et personne
dans le sélecteur ne le lit.** `is_dural_unlocked` vit à `0x180C3B700` et
`--dural` le pose (2 octets dans `vfes.exe`, MESURÉ au §1.2). Ses références,
MESURÉ (`xref 0x180C3B700`) : **5**, dont un écrivain (`setne` à
`0x180214D69`, dans la dérivation de `module_start`) et **quatre lecteurs** —
`0x1801D081D`, `0x1801DDD4F`, `0x1801E348E`, `0x1801E490F`. **Aucun** n'est
dans le code de la grille (`0x18016Dxxx` / `0x18016Exxx`). La voie « poser un
drapeau et laisser le jeu décider », qui EST la voie REVO, est donc close par
mesure : le drapeau est posé depuis le début et la case restait fermée.

**MESURE 3 — le corps réel du prédicat n'est pas dans ce binaire.** Il est
dans le build GOG/Yakuza 6 (`0x1801A4C50`, trois appelants qui sont nos trois
sites un pour un, `comparaison_builds.md` §9.1). Chez nous le corps a disparu
dans le repliement COMDAT, et les **210 appels** restants à `0x180007450`
(MESURÉ) appartiennent à des prédicats bouchonnés **distincts** : on ne peut
donc pas réécrire le corps du bouchon, puisque 207 autres appelants le
partagent. C'est le site d'appel qui a un sens, jamais le corps.

> **Conclusion.** REVO n'a pas été « fait plus proprement » par un meilleur
> choix de méthode : il a été fait plus proprement parce que **le code de SEGA
> y est encore**. APM3 ne peut pas emprunter cette propreté, parce que ce
> qu'elle emprunte est le code lui-même.

**Rien n'a donc été modifié dans la version APM3, et il n'y a pas de poseur à
écrire.** Le point 4 de la demande est sans objet.

---

## 4. LA SEULE CHOSE QUE LA PROPRETÉ DE REVO DÉSIGNE CHEZ APM3 — ET CE QUI LA BLOQUE

Ce n'est pas la méthode REVO, c'est ce qu'elle rappelle : **lire la vraie
entrée du prédicat**.

| | ce que lit le prédicat | mesuré ? |
|---|---|---|
| REVO | `[base+0x795928]`, le mode | oui, §1.1 |
| GOG (code SEGA intact) | `[0x1805D8AF8]`, le mode de jeu | oui, `comparaison_builds.md` §9.1 |
| APM3 aujourd'hui | l'**entrée de menu validée**, un mandataire | oui, `patch_moteur.py` l. 410-419 |

Faire lire à la greffe d'APM3 le mode de jeu `0x180751010`, comme le font REVO
et SEGA, est **bloqué par une mesure déjà au dossier** : sur le chemin Arcade,
ce dword n'est jamais posé. `analysis/mode_de_jeu.md` l'écrit, et le relevé du
5 septembre 2026 montre le bloc à `mode=9` avant toute écriture — après un
Versus (mode 4), Arcade lirait encore 4 et le prédicat se tromperait de
bascule. MESURÉ ici en complément (`xref 0x180751010`) : **4 références, dont
2 écrivains seulement**, `0x18019C426` et `0x18019C4A8`, dans les accesseurs
`0x18019C420` (6 appelants) et `0x18019C4A0` (1 appelant) — et aucun n'est
atteint par l'entrée Arcade.

C'est pourquoi le mouchard du répartiteur existe : ce n'est pas un raccourci,
c'est le contournement d'un fait mesuré.

**La suite propre, si elle est voulue un jour, est déjà nommée en §15.6 pt 2 :**
étendre `--sp-mode` à Arcade en se greffant sur le `call 0x18019C420` de
`0x1801DC3A6` — comme c'est déjà fait pour Score Attack et License Challenge —
puis faire lire `0x180751010` au prédicat de la greffe. Le mouchard devient
alors inutile. **C'est un chantier à part, pas une transposition**, il touche
le lancement des combats et non Dural, et il n'a pas été entrepris ici.

---

## 5. CE QUI N'A PAS ÉTÉ VÉRIFIÉ

* **Aucun jeu n'a été lancé.** Toutes les mesures de cette note sont des
  lectures de binaires et de sources. L'état à l'écran d'APM3 est celui du
  11 octobre 2026 (§15.7, quatre captures) et celui de REVO celui du
  10 novembre 2026 (§419.129, verdict de Frédéric).
* **Le prédicat GOG `0x1801A4C50` n'a pas été relu dans son binaire** pour
  cette note : il est cité d'après `comparaison_builds.md` §9.1. Les trois
  appelants qu'il annonce correspondent à nos trois sites, mais je ne l'ai pas
  revérifié moi-même.
* **La divergence du §2 entre `LISEZ-MOI.md` §3.1 et `MENU.md` §419.129** n'est
  pas corrigée dans les fichiers : je la signale, je ne l'ai pas tranchée par
  une nouvelle course, et c'est `MENU.md` qui porte la mesure.
* **Je n'ai pas vérifié si les 4 lecteurs de `is_dural_unlocked`
  (`0x1801D081D`, `0x1801DDD4F`, `0x1801E348E`, `0x1801E490F`) commandent
  quelque chose d'utile par ailleurs.** J'ai seulement établi qu'aucun n'est
  dans le code de la grille, ce qui suffit au verdict.
