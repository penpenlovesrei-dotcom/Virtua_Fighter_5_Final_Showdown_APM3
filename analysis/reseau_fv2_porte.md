# Le jeu en ligne de fv2-recomp, porté dans VF5FS APM3

Frédéric, 19 novembre 2026 : « **intègre le mode de jeu en ligne que je t'ai
pointé, celui de SEGA n'est pas adapté** ».

La note `en_ligne_vf3_transposable.md` avait conclu « inutile et impossible tel
quel ». Frédéric a tranché contre ce verdict, et **deux mesures faites ce
soir lui donnent raison sur le fond** — mais une troisième déplace le mur, et
il faut la dire tout de suite.

---

## 1. Ce qui est fait, et prouvé

**Le réseau de `fv2-recomp` est dans `apm.dll`.** La bibliothèque a été
construite, liée, et la DLL charge toujours ses 57 fonctions.

| | avant | après |
|---|---|---|
| `apm.dll` | 130 048 o | **547 840 o** |
| empreinte MD5 | `8DE630D3…` | `5996C8DF…` |
| entrées de la table d'export | 58 | **58** |

Les onze fichiers de `fv2-recomp/src/net` sont copiés **octet pour octet**
dans `VF5RE/tools/reseau` (MD5 vérifié, fichier par fichier). Ils
**compilent sans une erreur ni un avertissement** avec le gcc de la greffe —
du premier coup, parce qu'ils ne dépendent de rien d'autre que du contrat
`Game` et portent déjà leurs branches Windows (`winsock2.h`, `winhttp.h`).

La construction passe désormais par **deux langages** : les `.cpp` par `g++`,
le `.c` par `gcc`, et la liaison par `g++` (sinon `libstdc++` ne viendrait
pas), avec `-static-libstdc++` pour la même raison que `-static-libgcc` était
déjà là.

---

## 2. Les deux mesures qui ont changé le verdict

### 2.1 Le contrat ne fait que quatre méthodes

```cpp
struct Game {
    virtual bool begin(const std::vector<uint8_t> &blob) = 0;
    virtual void save(std::vector<uint8_t> &state) = 0;
    virtual bool load(const std::vector<uint8_t> &state) = 0;
    virtual void advance(const uint16_t input[2], bool resim) = 0;
};
```

`Session`, `Link`, `RoomLink`, `stun`, `http` **ne savent rien du jeu**. Le
seul lien avec le reste de `fv2-recomp` dans tout `src/net` est un appel à
`game.hash_skip()`.

### 2.2 L'entrée à deux joueurs était déjà résolue

La note disait « un masque global de 12 bits **sans indice de joueur** ».
C'était vrai de l'API brute d'`apm.dll`, et **ce n'est plus l'état du
projet** : le correctif `--joueur2` de `patch_moteur.py` insère `shl ebp, 4`
dans le lecteur d'entrées du moteur (`0x180243ED0`), si bien que le joueur 2
demande le code du joueur 1 **plus seize**. Codes 2 à 14 au joueur 1, 18 à 30
au joueur 2, et `g_masque` — que la greffe compose elle-même — porte les deux.

**`advance` était donc résolu avant ce portage.** C'est ce qui le rend
possible.

---

## 3. Le mur, mesuré : le rollback demande une photo, et il n'y en a pas

`vf3_netplay.h` montre comment VF3 sauvegarde son état :

```cpp
size_t hash_skip() const override { return m3::Model3::STATE_HEADER; }
```

**`m3::Model3` est un émulateur.** La machine entière tient dans un bloc
d'octets plat, et `save` en est une copie. C'est pour cela que le rollback y
est trivial.

**VF5FS APM3 est un binaire x64 natif.** Il n'y a pas de bloc plat : l'état de
la simulation est dispersé dans le tas, en pointeurs, avec des ressources
D3D12 accrochées dessus. Rien ne se photographie en une copie.

> **Ce n'est pas la règle du dossier sur les savestates.** Celle-là interdit
> de lire la mémoire du **processus REVO depuis l'extérieur**, ce que Windows
> a refusé par l'erreur 5. Ici nous sommes **dedans** notre propre processus,
> et personne ne nous refuse rien. La difficulté est **la forme de l'état**,
> pas le droit d'y toucher.

---

## 4. D'où l'étage posé : le pas verrouillé

`Session::set_lockstep(true)` lui fait **attendre** les entrées d'en face au
lieu de les deviner. Aucune image n'est rejouée, donc `load` n'est jamais
appelé, donc l'absence de photo ne coûte rien — **sauf deux choses, et il faut
les nommer** :

1. **Le retard ne peut pas être caché.** Avec le rollback on joue à deux
   images de retard quel que soit le ping ; ici **le retard est le ping**.
2. **La détection de désynchronisation ne vaut rien.** `save` rend un état
   **vide** : les deux côtés hachent la même chose, et `checksum_every` ne
   peut rien attraper. Un état inventé serait pire — la somme de contrôle le
   prendrait pour la vérité. Un état vide ne trompe personne.

`cfg.max_rollback` est borné à `[1, 30]` par `Session` : on ne peut pas le
mettre à zéro. Il reste à 1, et le pas verrouillé fait que rien ne le
déclenche.

### Comment l'image est retenue

`vf5net_image()` est appelé depuis **la composition des entrées de
`Core_execute`** — une fois par image, au seul endroit où `g_masque` se forme.
Tant qu'il rend 0, on attend sur place, et comme `Core_execute` *est* le
battement de la carte, attendre là retient l'image entière. **C'est l'engin
qui fait tourner la frame, pas nous** : c'est ce qui permet de ne pas toucher
à la boucle principale de `vfes.exe`.

**Un plafond de dix secondes**, pour une raison nommée : sans lui, un
adversaire qui disparaît fige le jeu sans retour et il faudrait tuer le
processus.

Les bits gardés en local : **0 et 1** (TEST, SERVICE), **15** (quitter le
mode), **16 et 17** (caméra du terminal), **31** (notre menu). Aucun
n'appartient au combat.

---

## 5. Ce qu'il n'y a PAS encore

* **Aucun moyen de démarrer une session.** `vf5net_demarrer()` existe et est
  liée, mais **rien ne l'appelle** : la ligne « Jouer en ligne » du menu
  ÉCHAPPE est toujours éteinte. Tant que personne n'appelle,
  `vf5net_etat()` rend 0 et **le crochet ne fait rien du tout** — le jeu se
  comporte exactement comme avant.
* **Pas de salon, pas de code à six lettres.** Ils vivent dans
  `src/host/online.cpp` (99 Ko) avec toute l'interface RmlUi de fv2-recomp,
  qui n'est pas portable telle quelle. `RoomLink` — STUN, TURN, perçage de
  trous — **est là et compile** ; ce qui manque est le client HTTP du worker
  Cloudflare qui échange un code contre les adresses d'en face. Cet étage-ci
  relie **deux adresses données à la main**, par `UdpLink`.
* **Aucune course.** Rien de tout ceci n'a été vu à l'écran.

---

## 6. Ce qui n'est pas vérifié

* **Que la simulation de VF5FS soit déterministe d'une machine à l'autre.**
  Le jeu sait rejouer un combat depuis des entrées enregistrées
  (`AVTaskGameVsReplay`, `ROB_SHORT_REPLAY_REC`), ce qui l'étaye fortement —
  mais rejouer chez soi et **concorder avec une autre machine** ne sont pas la
  même chose. Et sans somme de contrôle utile (§4), on ne le saura pas en
  jouant.
* **Qu'attendre dans `Core_execute` retienne l'image sans rien casser
  ailleurs** — le son, le rendu, les minuteries du moteur.
* **Que deux instances se soient jamais parlé.** Zéro.
* Que les deux côtés soient au même écran quand la session commence : c'est
  aujourd'hui à l'humain de le faire.

---

## 7. Les fichiers

| fichier | ce que c'est |
|---|---|
| `VF5RE/tools/reseau/*.cpp`, `*.h` | les onze de `fv2-recomp/src/net`, **copie octet pour octet** |
| `VF5RE/tools/reseau/vf5_reseau.cpp` | **la couture**, et le seul qui nous appartient |
| `VF5RE/tools/poser_reseau.py` | le poseur, rejouable ; `--controler` contrôle sans écrire |
| `VF5RE/tools/gen_apm_stub.py.avant_reseau` | la copie d'avant |
| `VF5RE/tools/obj/` | les objets de la construction |

Contrôles du poseur : trois témoins ×1, l'encodage inchangé (6 signes
non-ASCII avant et après), et **un contrôle négatif** — l'ancienne ligne de
liaison en un seul `gcc` compte ×0, ce qui échouerait si la pose n'avait rien
fait.


---

## 8. Le salon à code — posé le 19 novembre 2026 au soir

Frédéric : « **Le salon d'abord** ».

`apm.dll` : **547 840 → 635 904 octets**, empreinte `5996C8DF…` → `A7A8F783…`,
**58 exports** inchangés.

### 8.1 Les routes, telles que le worker les déclare

Lues dans `fv2-recomp/tools/lobby/src/index.js`, pas devinées :

| route | corps | réponse |
|---|---|---|
| `POST /v1/turn` | `{game, version, content}` | `{servers:[{host,port,username,credential}], country}` |
| `POST /v1/host` | `{game, version, content, name, cands, relay}` | `{code, key, token}` |
| `POST /v1/wait` | `{code, key}` — attend jusqu'à 20 s | `{guest: null \| {name, cands, relay}}` |
| `POST /v1/join` | `{code, game, version, content, name, cands, relay}` | `{name, cands, relay, token}` |

Quatre témoins ×1 dans `apm.dll`, **×0** dans la sauvegarde d'avant.

**Aucun trafic de jeu n'y passe** : les deux parties se relient directement, et
ne passent par le relais TURN que lorsqu'elles ne peuvent pas.

### 8.2 Ce qui tourne sur quel fil

`vfnet::http::request` et `RoomLink::resolve` **bloquent** : ils tournent sur un
fil à eux. **Tout le reste de `RoomLink`** — `tick`, `set_peer`, `candidates` —
reste sur le fil principal, parce que rien ne dit qu'il supporte deux fils et
qu'il n'y a aucune raison de le parier.

### 8.3 L'empreinte des données : une garde faible, et c'est dit

`content` empêche deux joueurs aux fichiers différents d'être appariés.
fv2-recomp hache ses fichiers ; ici on prend les **tailles** du module et de
`vf5fs_data.par` (FNV-1a 64 bits). Lire quatre gigaoctets au démarrage
coûterait des secondes pour une garantie à peine meilleure. **Deux archives
différentes de même taille passeraient** — la garde attrape le cas qui arrive,
une version de module qui n'est pas la même, pas un adversaire malveillant.

---

## 9. Deux fautes de la soirée, dites parce qu'elles coûtent

### 9.1 `libwinpthread-1.dll` — attrapée avant toute course

La première liaison a rendu une `apm.dll` qui **importait
`libwinpthread-1.dll`**, la bibliothèque de fils de mingw que `std::mutex`
tire. Cette DLL **n'est pas à côté de `vfes.exe`**. La DLL ne se serait pas
chargée, et le jeu serait mort au démarrage sans rien dire d'utile.
`-static-libgcc -static-libstdc++` ne suffisaient pas ; **`-static`** prend
tout.

Le poseur a été **corrigé à la source** — `gen_apm_stub.py` restauré depuis sa
sauvegarde et reposé — plutôt que rustiné, et la construction porte désormais
**un contrôle des dépendances** : toute DLL importée hors d'une liste blanche
de DLL système arrête la construction. Il aurait attrapé la faute.

### 9.2 Deux contrôles qui visaient les mots, pas l'état

Le dossier le nomme au §4.6 de `CLAUDE.md`, et je suis tombé dedans **deux
fois dans la même heure** :

* un contrôle comptait `-static-libstdc++` dans **tout** le fichier et criait à
  la faute en trouvant **deux de mes propres commentaires**. Corrigé : le
  compte est borné au corps, lignes `#` exclues, et doublé d'un contrôle
  **positif** (`'-static'` ×1).
* un contrôle cherchait les octets `stun.cloudflare.com` dans `apm.dll` et
  rendait **0**. J'ai d'abord annoncé une chaîne tronquée — **c'était faux**.
  Un essai isolé imprime `stun.cloudflare.com:3478` correctement : avec `-O2`,
  gcc **découpe le littéral** en un bloc de 16 octets et un second, parce qu'il
  incorpore la copie. Le binaire est juste ; le contrôle ne l'était pas.

---

## 10. Ce qu'il reste, exactement

1. **Rien n'appelle encore `vf5net_salon_demarrer`.** Il faut la page du menu :
   héberger / rejoindre, la saisie des six lettres, l'affichage du code et de
   l'état. Tant que personne n'appelle, `vf5net_etat()` rend 0 et **le crochet
   de `Core_execute` ne fait rien du tout**.
2. **L'adresse du worker n'est pas configurable.** Elle doit venir
   d'`apm_entrees.txt`, qui est relu à chaud toutes les 500 ms — c'est la
   convention du projet.
3. **Le worker n'est pas déployé.** `wrangler deploy` depuis
   `fv2-recomp/tools/lobby`, plus une clé TURN Cloudflare. C'est le geste de
   Frédéric, pas le mien : il engage un compte et un abonnement.
4. **Aucune course.** Rien de tout ceci n'a été vu à l'écran, et deux instances
   ne se sont jamais parlé.


---

## 11. La page « Jouer en ligne » — posée le 19 novembre 2026

`apm.dll` : **635 904 → 641 536 octets**, empreinte `A7A8F783…` → `828FADAF…`,
**58 exports** inchangés, et toujours **aucune DLL hors système** importée.

La ligne « Jouer en ligne » du menu ÉCHAPPE n'est plus grisée : elle ouvre une
**seconde page**.

| ligne | ce qu'elle fait |
|---|---|
| Héberger un salon | `/v1/host` ; le code à six lettres s'affiche en grand |
| Rejoindre `______` | les six cases se remplissent au clavier (A–Z), Retour arrière efface |
| Arrêter | coupe la session et le salon |
| Retour | revient à la racine |

Sous les lignes : l'**état en toutes lettres** (préparation, recherche de nos
adresses, en attente d'un joueur, relié, échec), le code quand il y en a un, et
les messages du salon et de la session. **C'est la seule chose qui dise ce qui
se passe** : tout le reste est sur un fil, et muet.

### 11.1 Trois décisions, et pourquoi

* **ÉCHAP remonte avant de fermer.** Fermer tout d'un coup depuis la page
  ferait perdre le code à l'écran sans que rien ne le redise. Un second ÉCHAP
  ferme.
* **L'ouverture choisit la première ligne UTILISABLE.** Sans adresse de salon,
  « Héberger » et « Rejoindre » sont grisées et le curseur tombe sur
  « Retour » — la règle de fv2-recomp : une ligne sans rien à faire est
  dessinée, grisée et sautée.
* **Les fronts des 26 lettres se consomment même sur une autre ligne.** Sans
  cela, une lettre tenue pendant qu'on change de ligne s'écrirait d'un coup en
  arrivant sur la ligne du code.

### 11.2 L'adresse du worker : `apm_salon.txt`

Un fichier à côté de `vfes.exe`, première ligne non vide et non commentée.
**Pas `apm_entrees.txt`**, bien que ce soit la convention du projet et qu'il se
relise à chaud : son lecteur est dans le C de `gen_apm_stub.py`, que j'ai déjà
remué deux fois ce soir. Un fichier à part, lu par le C++ qui s'en sert, ne
touche à rien. Lu **une fois** : changer l'adresse demande de relancer, et le
fichier le dit lui-même.

### 11.3 Les contrôles

| contrôle | résultat |
|---|---|
| `JOUER EN LIGNE`, `Heberger un salon`, `TON CODE :`, `A-Z taper le code` | ×1 dans le produit, **×0** dans la sauvegarde |
| `apm_salon.txt` | ×2 (le `fopen` et le message à l'écran) |
| entrées de la table d'export | **58**, inchangées |
| DLL importées | KERNEL32, USER32, WINHTTP, WS2_32, msvcrt — **que du système** |
| **contrôle négatif** : l'ancienne raison grisée du réseau (`il n'est expose nulle part`) | **×0** |

Ce dernier peut échouer sur une faute réelle : les raisons des lignes grisées
sont lues **dans l'ordre où elles paraissent**, et en laisser une de trop aurait
collé le texte du réseau sous « Disposition des touches » sans qu'aucun
compilateur ne dise rien.

### 11.4 Ce qui reste, et c'est court

1. **Déployer le worker** — `npx wrangler deploy` depuis
   `fv2-recomp/tools/lobby`, plus une clé TURN Cloudflare, puis l'adresse dans
   `apm_salon.txt`. **C'est le geste de Frédéric** : il engage un compte et un
   abonnement.
2. **La course.** Les consignes et les issues **O à T** sont écrites d'avance
   dans `VF5RE/tools/course_menu_echappe.cmd`. Sans worker, la course mesure la
   page elle-même (issues O à T) ; elle ne peut pas mesurer une partie.
3. **Deux instances ne se sont toujours jamais parlé.**
