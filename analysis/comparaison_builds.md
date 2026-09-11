# APM3 contre Yakuza 6 : deux builds du même moteur PXD

Établi le 2026-09-09. Sources :

| | APM3 (le nôtre) | Yakuza 6 |
|---|---|---|
| binaire | `vf5fs-pxd-w64-Retail_APM3.dll` | `vf5fs-pxd-w64-Retail_GOG.dll` |
| chemin | `runtime/media/vf5fs/` | `…\VF5 FS DECOMP\Yakuza_6_FS\Yakuza 6 - vf5fs\` |
| taille | 6 965 248 o | 5 390 336 o |
| sha256 | `045c0696…` | `a10c731b…` |
| horodatage PE | **2021-05-19** | **2022-12-02** |
| éditeur de liens | MSVC 14.16 | MSVC 14.16 |
| base préférée | `0x180000000` | `0x180000000` |
| `.text` | 3 426 140 o | 2 332 296 o |
| fonctions `.pdata` | **13 661** (3,13 Mo) | **9 770** (2,11 Mo) |
| archive `.par` | 3,71 Go, 1 862 fichiers | 1,79 Go, 1 842 fichiers |

**Le build Yakuza 6 est plus RÉCENT de dix-huit mois** et pourtant plus petit
d'un tiers. Ce n'est pas une version antérieure : c'est le même moteur amputé
de sa couche arcade.

Outils écrits pour cette comparaison : `tools/comparer_builds.py` (structures)
et `tools/par_inventaire.py` (archives).

---

## 1. Les données sont les MÊMES

`par_inventaire.py --contre` : **1 822 fichiers communs** sur 1 862 / 1 842.

Les seuls écarts réels :

* **APM3 a en plus** les dix-neuf `<perso>itm_patch.farc` (les correctifs
  d'objets de personnalisation) et `se_adam.acb` ;
* **Yakuza 6 n'a rien que l'APM3 n'ait pas.** Les vingt noms qui ressortaient
  « seulement dans B » sont nos propres masques (`aet_n_*.bi_`,
  `spr_n_*.far_`) posés par un chantier antérieur ;
* **76 fichiers de même nom, de taille différente** : uniquement des `.acb`
  CRI, à quelques centaines d'octets près — sauf `se_system.acb`, plus GROS
  chez Yakuza 6 (1 535 904 contre 1 317 952).

Les 41 décors sont là des deux côtés, aux mêmes tailles à l'octet près
(`stgdjo.farc` 10 516 296 o, `stgdu1.farc` 27 229 016 o…).

**Le décor perdu de Dural n'est pas là non plus.** Ni `stgdur.farc` dans
l'archive, ni la chaîne dans le binaire : les deux builds ne connaissent que
`auth_3d/stgdur` et `auth_3d/effstgdur`, l'animation sans la géométrie. La
conclusion de `reference_vf5_stgdur_verb` tient : il n'existe que dans
VF5 ver.B.

---

## 2. Les 41 descripteurs de décor : UN seul champ diffère

La table se retrouve par sa structure, pas par son adresse :

| | APM3 | Yakuza 6 |
|---|---|---|
| table des décors | `0x180403430` | `0x1802F5B40` |
| **pas d'une entrée** | **0xF0** | **0xD8** |
| table d'éclairage (41 codes) | `0x18039F7A0` | `0x180293860` |

**Les 24 octets d'écart sont le bloc BGM, et rien d'autre.** Aligné champ par
champ sur `djo` :

```
+0x00 .. +0x68   IDENTIQUES : code, effets, objset, les cinq objets,
                 +0x2C..+0x34, la collision
+0x68            la musique principale
   APM3   +0x70 .. +0xB0   NEUF reprises  (vf1 vf2 vfk vf3 vf4 vf4ev vf5 vf5r vf5fs)
   YAK6   +0x70 .. +0x98   SEPT reprises  (vfp vf1 vf2 vf3 vf4 vf5r)
puis tout se réaligne, décalé de 0x18 :
   APM3 +0xB8 = YAK6 +0xA0   le compte de murs
   APM3 +0xC0 = YAK6 +0xA8   le tableau de murs
   APM3 +0xD0 = YAK6 +0xB8   l'aiguillage de rendu
   APM3 +0xD4 = YAK6 +0xBC   l'index du saut à dix constantes
   APM3 +0xE4 = YAK6 +0xCC   la taille de l'aire
```

Les schémas de nommage de la musique diffèrent : APM3 dit
`rom/sound/bgm/vfes_bgm_stg_djo.adx`, Yakuza 6 dit `vf5fs_bgm_djo.adx` et
`h_djo_vfN.adx`.

### Le seul écart de contenu : la collision de DU2

```
22  du2   coli  APM3 'rom/STGDU1_COLI.000.bin'  /  YAK6 'rom/STGDU2_COLI.000.bin'
```

**C'est la confirmation indépendante de `--du2-collision`.** Le défaut relevé
par Frédéric à l'écran — « en ring out, le personnage se pose sur un sol qui
n'existe pas » — est une **régression propre au build APM3** : le build console
pointe la bonne collision. Notre correctif ne fait que remettre ce que Yakuza 6
a toujours eu.

Les quarante autres descripteurs sont identiques champ pour champ.

---

## 3. Le bouchonnage n'est PAS une amputation de l'arcade

C'est la mesure qui corrige une hypothèse de travail. Les **quatre mêmes
familles de bouchons** existent des deux côtés, dans des proportions
comparables :

| bouchon | APM3 | Yakuza 6 |
|---|---|---|
| `ret 0` | `0x180007430` — **577** appelants | `0x180004080` — **429** |
| `xor al,al ; ret` | `0x180007450` — **210** | `0x1800283A0` — **241** |
| `xor eax,eax ; ret` | `0x180007440` — **117** | `0x180028390` — **128** |
| `mov al,1 ; ret` | `0x180029FB0` — **71** | `0x1800457A0` — **44** |
| part des appels | 1,8 % | 2,3 % |

`xor al,al ; ret` a même **plus** d'appelants chez Yakuza 6. Ces bouchons ne
sont donc pas des maillons retirés pour la borne : ce sont des fonctions vides
que l'éditeur de liens fusionne (ICF) — virtuelles par défaut, journalisation
compilée à vide. `reference_vf5_verrou_bouchonne` doit se lire ainsi : *patcher
le site d'appel, jamais le corps* reste vrai et vital, mais « un maillon
bouchonné » n'est pas en soi la preuve d'une amputation.

---

## 4. Ce que chaque build a en propre : le RTTI

`rtti.py` : APM3 **534** vtables nommées, Yakuza 6 **314**.

Sur les **noms de base** (l'espace de noms anonyme `?A0x…` diffère d'un build à
l'autre et fait croire à des classes absentes) : 311 communes, 118 propres à
APM3, **3** propres à Yakuza 6.

**Propres à Yakuza 6** — et c'est tout :

    TaskMultiMenu   TaskMultiMenuRule   TaskMultiResult

le menu de partie **locale à plusieurs**, que l'APM3 remplace par
`MenuGameAssign` / `MenuGameAssignRule` / `MenuGameAssignRuleLocal`.

**Propres à APM3** (118) — la couche arcade, sans exception notable :

* le **réseau de bornes liées** : `AbaasManager`, les onze `LinkMainState*`,
  `LinkReceiveThread`, `LinkSend`, `PacketGate`, `StunChecker`, les dix
  `Turn*`, `ConnectivityChecker`, `LineQualityChecker`, `Udp`, `RemoteAddress` ;
* la **cryptographie et le transport** : `Aes`, `Bcrypt`, `CNG`, `CryptKey`,
  `Curl`, `HttpData`, `Zlib` ;
* les **tâches de borne** : `TaskApm3Entry`, `TaskApm3TestMode`,
  `TaskApmResult`, `TaskTitleAdam`, `TaskSession`, `TaskRanking`,
  `TaskRankingList`, `TaskAutoLoad`, `TaskCsSystemSaveData`, `TaskTimer` ;
* le **menu opérateur** : `MenuTop`, `MenuPageBase`, `MenuBookkeep`,
  `MenuGameAssign*`, `MenuSoundSetting`, `MenuBackupClear` ;
* le reste est du STL et des exceptions (`ios_base`, `runtime_error`…).

**Les classes de personnalisation existent des deux côtés.** Ma première
comparaison, faite sur les noms complets, annonçait `TaskCustomizeMenu`,
`TaskCostumeMenu`, `TaskSelItemMenu`, `TaskSelPartMenu`, `TaskMenuCustomize`
comme propres à Yakuza 6 : c'était le hachage d'espace de noms anonyme qui
changeait. **Comparer les noms de base.**

---

## 5. Les chaînes témoins

| chaîne | APM3 | YAK6 | ce que ça dit |
|---|---|---|---|
| `am::abaas` | oui | **non** | le netcode de bornes liées est arcade seul |
| `APM3_ENTRY` | oui | **non** | l'écran noir de la borne aussi |
| `vfes_bgm_cus` | oui | **non** | la musique de Customize a un autre nom |
| `EXIT_CAUTION` | oui | oui | la confirmation de EXIT GAME |
| `TERMINAL MENU` | oui | oui | la page TERMINAL |
| `NOW LOADING` | oui | oui | |
| `rom/game_score.txt` | oui | oui | le décor maison de l'adversaire |
| `obj_db.bin` | oui | oui | |
| `%s/envmap_correct_%s.txt` | oui | oui | |

Le mode console de l'APM3 n'est donc pas un vestige : ses chaînes sont **les
mêmes** que celles du build console, à l'identique.

---

## 6. Ce que Yakuza 6 apporte au chantier

1. **Une pierre de touche pour les données.** Tout écart de descripteur entre
   les deux builds est un défaut d'un côté ou de l'autre. Le premier trouvé —
   la collision de DU2 — valide un correctif que nous avions déduit seuls.
   `comparer_builds.py` permet de refaire ce test sur n'importe quelle table.
2. **Un build console de référence, plus récent que le nôtre.** Pour toute
   question « comment ce menu se comporte-t-il quand la borne n'est pas là »,
   c'est la meilleure réponse disponible — meilleure que R.E.V.O., qui est un
   portage.
3. **`TaskMultiMenu` / `TaskMultiMenuRule` / `TaskMultiResult`** : trois
   classes que nous n'avons pas, pour la partie locale à plusieurs. À lire si
   le VERSUS local demande un jour plus que ce que `MenuGameAssign` donne.
4. **Ce qu'il n'apporte pas** : aucun décor de plus, aucun fichier de données
   que nous n'ayons, et pas le `stgdur` perdu.

---

## 7. Deux pièges payés en écrivant cette comparaison

* **Le pas d'une table se déduit, il ne se suppose pas.** Figé à `0xF0`, le
  chercheur de table répondait « introuvable » sur Yakuza 6, dont le pas vaut
  `0xD8`. Une structure se reconnaît par sa **forme** — ici : « l'entrée 1
  pointe sur `STGTS2` et l'entrée 11 sur `STGDJO` », quel que soit le pas.
* **Chercher une chaîne en exigeant le NUL juste après** faisait répondre
  « absent » pour `am::abaas` (qui préfixe des noms plus longs) et pour
  `STGDUR` (qui vit dans `rom/auth_3d/STGDUR.farc`). Sous-chaîne d'abord,
  mot entier seulement si on sait pourquoi.


---

## 8. Le balayage des autres tables (2026-09-09)

Toutes les tables liées aux décors ont été croisées. **Une seule chose diffère
en plus de la collision de DU2** — et elle est délibérée.

| table | APM3 | Yakuza 6 | verdict |
|---|---|---|---|
| les 41 codes d'éclairage | `0x18039F7A0` | `0x180293860` | **identiques**, 0 écart |
| les blocs de murs (`+0xC0`) | 5 blocs, 12 décors | 5 blocs, 12 décors | **identiques**, contenus compris |
| la grille de sélection (21 cases) | `0x180400210` | `0x1802F2B70` | **identique**, case par case |
| la liste d'aperçus | `0x180174BF0`, 26 entrées | `0x18017E4xx`, 26 entrées | **identique** : 4..25, 39, 40, 41, `-1` |
| les 41 descripteurs | | | **1 écart** : la collision de DU2 |
| le forçage « du1 → du2 » | **4 sites** | **1 site** | **3 sites propres à l'APM3** |

### Le forçage de Dural : un bouchon PARTAGÉ, trois verrous ARCADE

C'est la nuance que la comparaison apporte, et elle corrige notre lecture.

**Le bouchon du combat est dans les DEUX builds** — même code, même valeur :

```
APM3  0x1800B2330   b8 16 00 00 00   mov eax, 0x16 ; ret
YAK6  0x1800C6040   b8 16 00 00 00   mov eax, 0x16 ; ret
```

et il est appelé depuis un site rigoureusement identique — `cmp eax,0x15 ;
jne ; call ; test rax,rax ; je ; mov rcx,rax ; call ; mov rcx,rax ; call` —
en `0x1800B8B02` chez nous, `0x1800CC794` chez Yakuza 6. Les deux voisins sont
de vrais accesseurs des deux côtés (`mov rax,[rip+…]` et `lea rax,[rcx+0x50]`).

**Choisir toujours DU2 pour un combat n'est donc pas une amputation de la
borne : c'est ce que SEGA a livré partout.**

En revanche, les **trois sites d'écran sont propres à l'APM3**. Balayage
exhaustif de tous les `cmp <reg32>, 0x15` suivis d'un `0x16` dans les seize
octets :

```
APM3   0x18017448F   cmp eax,0x15 ; jne ; mov r8d,0x16 ; mov [rbx+0x5C],r8d
       0x180175338   cmp eax,0x15 ; jne ; mov [rbx+0x60],0x16   (+ [rbx+0x5C])
       0x1801753A0   cmp eax,0x15 ; mov ecx,0x16 ; cmove eax,ecx
       -> 3 sites
YAK6   -> 0 site
```

Ce sont donc **trois verrous ajoutés pour la borne**, qui bloquent la case de
Dural sur DU2 dans l'écran de sélection. `--decors-dural-grille` les lève, et
`--variantes` fait de même pour poser son anneau : les deux correctifs
remettent l'écran dans l'état du build console.

### Ce que ça change dans notre lecture

`project_vf5_decors_dural` parlait d'un « forçage QUADRUPLE ». C'est exact au
sens des sites, mais il faut le lire ainsi :

* **1 bouchon partagé** avec le build console — le choix du décor de combat ;
* **3 verrous propres à l'APM3** — le blocage de l'écran de sélection.

Et la collision de DU2 reste la seule **régression** de données trouvée dans
tout le domaine des décors.
