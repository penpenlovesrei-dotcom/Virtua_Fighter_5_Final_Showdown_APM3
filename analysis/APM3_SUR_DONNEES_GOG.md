# LE CODE D'APM3 TOURNE SUR LES DONNEES DU GOG

Mesure du 4 novembre 2026. Banc : `FS APM3\banc_gog`, monte par
`outils\monter_banc_gog.cmd`. Captures dans le banc.

## 1. La question

> « peut-on mettre le vfes.exe et le vf5fs-pxd-w64-Retail_APM3.dll de
> `SOURCES\APM3_US\runtime\media\vf5fs` dans le dossier
> `SOURCES\Yakuza_6_FS_GOG\Yakuza 6 - vf5fs` et lancer le jeu ? »

Personne ne l'avait jamais essaye, dans aucun sens. C'etait la seule case
franchement vide du dossier : tout ce qui concernait APM3 et le GOG avait ete
*compare*, jamais *execute* ensemble.

## 2. LA REPONSE EST OUI, ET SANS RIEN EMPRUNTER

Le jeu demarre, affiche, et atteint l'ECRAN-TITRE en 140 s, sur les donnees
du GOG, avec le code d'APM3 **vierge** -- les octets de `SOURCES`, aucun de
nos correctifs. Aucun fichier n'a ete emprunte au `vf5fs_media` d'APM3.

```
 PID lance, fenetre « V », 1920x1080
   12s   moyenne 373,9/765   max 765   non-noirs  99,94 %   film d'intro
   30s   moyenne 317,4/765   max 765   non-noirs  98,74 %   film d'intro
   55s   moyenne 122,1/765   max 562   non-noirs  99,78 %   DEMO EN MOTEUR
   80s   moyenne 236,1/765   max 765   non-noirs 100,00 %
  110s   moyenne 441,7/765   max 765   non-noirs 100,00 %
  140s   moyenne 540,7/765   max 765   non-noirs  99,87 %   ECRAN-TITRE
```

| moment | capture | ce qu'on voit |
|---|---|---|
| 12 s | `capture_gog_12s.png` | le film d'attraction, Aoi, plein cadre |
| 55 s | `capture_gog_55s.png` | **Lei-Fei dans un decor 3D : ce n'est plus un film, c'est le moteur** |
| 110 s | `capture_gog_110s.png` | suite du cycle d'attraction |
| 140 s | `capture_gog_140s.png` | **le logo FINAL SHOWDOWN** |

La capture de 55 s est la plus importante des quatre : un film se lit avec
trois textures et un quad, et c'est tout ce que prouve un film a l'ecran. Un
personnage anime dans un decor eclaire prouve que le moteur de rendu complet
tourne sur ces donnees -- maillages, squelettes, matieres, ombres.

Le processus a ete arrete par nous a chaque fois, jamais par une erreur.
`SOURCES` verifiee intacte apres coup (taille et date du `.par` inchangees),
bien qu'il soit monte en lien dur.

## 3. CE QUI TOMBE

**Le mur `apm.dll` n'en etait pas un.** Il est reel -- `apm.dll` est un import
obligatoire de `vfes.exe`, 57 fonctions, et elle n'est pas dans le dossier
`vf5fs` (elle est un niveau au-dessus, dans `runtime\media`). Mais nous avons
le bouchon depuis septembre (`outils\gen_apm_stub.py`), et il fait le travail
ici comme ailleurs : `quest_journal.txt` montre qu'il s'est charge et qu'il a
trouve le moteur. Nomme comme obstacle le 4 novembre a 17h35, il etait deja
franchi.

**Le mur `shader_vf5_w64.farc` n'a pas eu lieu.** Je l'avais predit par ecrit
avant le lancement : le `vf5fs_media\w64` d'APM3 porte deux archives de
nuanceurs, le GOG une seule. Le jeu tourne sans la seconde. La prediction
etait fausse, et c'est une bonne nouvelle -- `shader_pxd_w64.farc`, identique
a l'octet pres des deux cotes, suffit. L'autre archive sert sans doute un
chemin que l'ecran d'attraction n'emprunte pas.

**Et la comparaison des imports expliquait deja pourquoi ca pouvait marcher.**
`vfes.exe` n'importe que `apm.dll`, `KERNEL32`, `USER32`, `ole32`, `DINPUT8`,
`SHLWAPI`, `d2d1`, `d3d11`, `dxgi`, `D3DCOMPILER_47` -- tout le reste est
systeme. Et les deux modules exportent `module_start`/`module_stop` et posent
leur pointeur par `mov rax,[rdx+0x30] ; mov [rax], <ptr>` : meme ABI d'hote,
memes offsets (`VF5RE\analysis\comparaison_builds.md` S9). Ce qui etait ecrit
« rien n'interdit *a priori* » se lit maintenant « rien ne l'interdit ».

## 4. CE QUE CELA NE DIT PAS

Il faut etre net sur la portee, parce que trois affirmations voisines sont
fausses.

1. **Ce n'est pas « le GOG tourne ».** C'est le JEU D'APM3 qui tourne sur les
   DONNEES du GOG. Le module `vf5fs-pxd-w64-Retail_GOG.dll` n'a pas ete
   charge une seule fois ; il est pose dans le banc en temoin de l'essai
   reciproque, qui reste a faire.
2. **Rien n'a ete joue.** Attraction et ecran-titre seulement. Entrees,
   selection de personnage, combat, son : non mesures.
3. **Les 20 fichiers manquants n'ont pas encore mordu.** La liste de noms du
   `.par` GOG est un sous-ensemble strict de celle d'APM3, moins 19
   `*itm_patch.farc` et `se_adam.acb` ; et le GOG porte 2 `.usm` contre 17.
   L'attraction n'y touche visiblement pas. Un mode qui y touche cassera.

## 5. CE QUE CELA OUVRE

Le `.par` du GOG fait 1,92 Go contre 3,99 Go pour celui d'APM3, et le jeu
tourne pareil. C'est donc une **deuxieme source de donnees interchangeable**
sous le meme code -- un levier que nous n'avions pas :

- un banc deux fois plus leger pour les essais qui ne dependent pas des
  donnees ;
- un **differentiel** : tout comportement qui change entre les deux `.par`
  designe un fichier, et la liste des ecarts ne compte que 20 noms ;
- et, dans l'autre sens, la confirmation que le probleme du GOG n'a jamais ete
  ses donnees. `YAMP_GOG.md` disait deja que le jeu GOG tourne sous YAMP ;
  on sait maintenant que ses donnees tournent aussi sous `vfes.exe`.

## 6. REFAIRE LA MESURE

```
outils\monter_banc_gog.cmd                     monte le banc (liens durs)
outils\monter_banc_gog.cmd emprunt             + shader_vf5_w64.farc d'APM3
outils\capturer_banc_gog.ps1 -Moments 12,30,55,80,110,140 -Suffixe _gog
```

`capturer_banc_gog.ps1` lance, photographie la zone client a chaque moment,
imprime moyenne/max/taux de non-noirs, et arrete le processus. L'histogramme
est la parce qu'une fenetre noire et une fenetre qui affiche ne se distinguent
pas sur une vignette, mais se distinguent sur les octets.

---

## 7. TROIS OBSERVATIONS DE L'UTILISATEUR, ET LEURS CAUSES

Frederic a relance le banc lui-meme et a rapporte trois faits. Ils ne sont
pas trois bogues : ce sont trois mecanismes differents, et deux etaient deja
mesures ailleurs dans le dossier sans qu'on en ait tire la consequence.

### 7.1 « Le film d'introduction a le son » -- attendu, et instructif

Un `.usm` Sofdec porte son propre flux audio. Il ne passe pas par le systeme
de musique du jeu. Que le film sonne ne dit donc rien de la BGM, et que la
BGM soit muette ne dit rien du decodeur video. Les deux chemins sont
disjoints, et l'observation les separe proprement.

### 7.2 « Pas de son sur l'animation avant l'ecran-titre » -- LES NOMS

C'est la BGM, et la cause se lit dans les noms de fichiers.

```
rom\sound\bgm     GOG 165 fichiers     APM3 285 fichiers
```

Les deux jeux de noms sont **disjoints** :

| APM3 demande | le GOG fournit |
|---|---|
| `vfes_bgm_vf5fs_are.adx` | `vf5fs_bgm_are.adx` |
| `vfes_bgm_vf5r_dur.adx`  | `vf5r_dur.adx` |
| `vfes_bgm_vf1_aur.adx`   | `h_aur_vf1.adx` |
| `vfes_bgm_vf4ev_cas.adx` | `h_cas_vf4ev.adx` |
| `vfes_bgm_mnu/sel/con/end/rom/tor/aim/cus.adx` | **rien** |
| `vfes_jng_win/lod/los/ovr.adx` | **rien** |
| `vfes_se_logo_sega.adx` | **rien** |

**Pas un seul fichier `vfes_bgm_*` dans le GOG.** Et le S9 de
`VF5RE\analysis\comparaison_builds.md` avait deja compte la chaine
`vfes_bgm_*` **221 fois** dans le module APM3 contre **0** dans le module
GOG. Le fait etait mesure depuis le 11 octobre ; il manquait de le relier a
un silence.

> La BGM est muette **par les noms**, pas par le format.

Et ce ne sont PAS les memes octets -- verifie, pas suppose :

```
vfes_bgm_vf5fs_are  6 475 776 o  48000 Hz        vf5fs_bgm_are  5 937 152 o  44100 Hz
vfes_bgm_vf5r_dur   6 934 528 o  48000 Hz        vf5r_dur       1 984 512 o  22050 Hz
vfes_bgm_vf1_aur    5 859 328 o  48000 Hz        h_aur_vf1      2 648 064 o  22050 Hz
```

Empreintes differentes des deux cotes. Ce sont d'autres encodages, plus
courts et moins fins cote GOG -- ce qui se comprend pour un mini-jeu inclus
dans Yakuza 6.

**Un renommage est donc plausible, et non verifie.** Plausible parce que les
en-tetes se lisent et concordent : magie `80 00`, version `03 12 04 02`,
**stereo des deux cotes**, et la frequence est portee PAR LE FICHIER -- le
decodeur CRI la lit, il n'a pas a la supposer. Non verifie parce que personne
ne l'a essaye. La musique jouerait alors en 22 kHz avec des boucles plus
courtes que celles de la borne.

Les huit musiques de menu, les quatre jingles et le son du logo SEGA, eux,
n'ont **aucun equivalent** dans le GOG : le VF5FS de Yakuza 6 n'a pas de
menus d'arcade. Ceux-la resteront muets quoi qu'on fasse, sauf a les prendre
chez APM3 -- ce qui serait un emprunt, a compter comme tel.

### 7.3 « Ni manette ni clavier » -- UN FICHIER MANQUAIT

Ce n'etait pas le GOG, et ce n'etait pas le jeu. Notre `apm.dll` lit sa
configuration dans **`apm_entrees.txt`**, pose a cote d'elle, et ce fichier
porte entre autres :

```
clavier = 1
manette = 1
manette_joueur = 2
```

Sans ce fichier, le bouchon ne repond qu'au scenario scripte -- et un
scenario vide ne presse jamais rien. Le jeu tournait donc, et n'obeissait a
personne.

`apm_entrees.txt` est desormais pose dans le banc, et
`monter_banc_gog.cmd` l'y recopie a chaque montage. C'est corrige a la
source, pas seulement dans le dossier.

> Le bouchon n'est pas qu'un bouchon : il porte le clavier, la manette, un
> scenario rejoue, une sauvegarde et un menu operateur. Il faut le configurer
> comme on configure une borne.

## 8. L'ETAT, APRES CES TROIS POINTS

| | etat |
|---|---|
| demarrage, fenetre, rendu | **mesure : va jusqu'a l'ecran-titre** |
| moteur 3D sur donnees GOG | **mesure : demo en moteur a 55 s** |
| son du film d'introduction | **mesure : present** |
| musique de fond | muette -- **cause nommee : les noms**, correction proposee non essayee |
| musiques de menu, jingles, logo SEGA | absents du GOG, sans equivalent |
| clavier et manette | **corrige : `apm_entrees.txt` pose, a re-essayer** |
| selection, combat, son de combat | non mesures |

---

## 9. LE MODULE APPREND LES NOMS DU GOG (patch de chaines)

Demande de Frederic : ne pas fabriquer d'alias dans les donnees du GOG, mais
repeindre **ce que le module demande**. C'est le bon sens -- le dossier de
donnees reste celui du GOG, lisible et intact, et c'est le module qui
s'adapte a son hote.

### 9.1 LE MODULE PORTE DEJA LES DEUX TABLES

Decouverte en relevant les chaines : le module ne porte pas une famille de
noms, il en porte **deux**, et elles se touchent dans le binaire.

```
003961d0  rom/sound/bgm/vfes_jng_ovr.adx
003961f0  rom/sound/bgm/vf5fs_jng_ovr.adx      (+32)
0039a4e0  vfes_jng_win.adx
0039a4f8  vf5fs_jng_win.adx                    (+24)
0039a540  rom/sound/bgm/vfes_bgm_con.adx
0039a560  rom/sound/bgm/vf5fs_lp_cnt.adx       (+32)
003fdc60  rom/sound/bgm/vf5fs_bgm_sel.adx
003fdc80  rom/sound/bgm/vfes_bgm_sel.adx       (+32)
```

`vfes_*` est la table ARCADE, `vf5fs_*` la table CONSOLE. Le code d'origine
choisissait entre elles selon la cible, et le binaire d'APM3 a garde les deux.

**Et le GOG livre exactement celle de la table console** : `vf5fs_bgm_sel.adx`,
`vf5fs_jng_ovr.adx`, `vf5fs_jng_los.adx`, `vf5fs_jng_win.adx`,
`vf5fs_lp_cnt.adx`, `vf5fs_lp_nam.adx`, `vf5fs_jng_cha.adx` sont tous la. La
correspondance n'est donc pas une regle que j'invente : **c'est le binaire qui
l'etablit**, et le dossier qui la confirme.

### 9.2 POURQUOI LE PATCH EST SUR

Les noms sont stockes en chemins complets, chacun dans son emplacement, a pas
de 40 octets pour la table des decors. Les cibles sont plus COURTES :

```
rom/sound/bgm/vfes_bgm_vf5fs_ban.adx  36 -> rom/sound/bgm/vf5fs_bgm_ban.adx  31
rom/sound/bgm/vfes_bgm_vf5r_ban.adx   35 -> rom/sound/bgm/vf5r_ban.adx       26
rom/sound/bgm/vfes_bgm_vf1_ban.adx    34 -> rom/sound/bgm/h_ban_vf1.adx      27
```

On ecrit a la meme adresse, on complete par des zeros : aucun pointeur ne
bouge, aucune relocalisation, aucune section a agrandir, taille du fichier
inchangee.

**Quatre cibles font un caractere de PLUS** (`vf5fs_jng_ovr` contre
`vfes_jng_ovr`). Mon garde-fou les a refusees -- et il avait raison de le
faire. Plutot que de forcer, l'outil compte maintenant les octets NULS qui
suivent reellement la chaine (l'alignement sur 8 en laisse) et n'ecrit jamais
au-dela de ce qu'il a verifie nul. Les quatre tiennent dans ce bourrage.

### 9.3 LA MESURE

`outils\patcher_bgm_gog.py` (a vide par defaut, `--ecrire` pour agir) :

```
133 chaines repeintes      vers h_* 68,  vers vf5fs_* 45,  vers vf5r_* 20
 72 laissees telles quelles -- le GOG n'a ni les vfk_* ni la plupart des vf4ev_*
  5 hors regle              vfes_bgm_mnu / cus / aim, vfes_jng_lod,
                            vfes_se_logo_sega : aucun jumeau console dans le
                            module, et aucune correspondance etablie. On ne
                            devine pas : elles restent muettes, et nommees.
```

Verifie apres coup : `SOURCES` identique au `.origine` (le lien dur avait
**3 liens** ; l'outil le casse et prend une vraie copie AVANT d'ecrire),
module patche different, 2 544 octets changes, 6 965 248 octets des deux
cotes. Reversible par le `.origine`.

### 9.4 CE QUI RESTE A ENTENDRE

Je n'ai pas d'oreilles : le patch est verifie *structurellement*, pas
*acoustiquement*. C'est a l'ecoute de trancher.

## 10. L'ECRAN NOIR APRES L'ECRAN-TITRE

Frederic : « le bouton start fonctionne mais apres l'ecran titre, c'est un
ecran noir ». Le premier point confirme le S7.3 -- `apm_entrees.txt` rend la
manette et le clavier. Le second a un suspect nomme, et mesure.

### 10.1 DIX-NEUF FICHIERS, ET PRESQUE TOUTE LA DIFFERENCE

```
objset/akiitm_patch   objset/aoiitm_patch   objset/braitm_patch
objset/gohitm_patch   objset/jakitm_patch   objset/jefitm_patch
objset/kagitm_patch   objset/krtitm_patch   objset/lauitm_patch
objset/leiitm_patch   objset/lioitm_patch   objset/monitm_patch
objset/mskitm_patch   objset/paiitm_patch   objset/saritm_patch
objset/shuitm_patch   objset/takitm_patch   objset/vanitm_patch
objset/wolitm_patch
```

Dix-neuf chaines dans le module, une par personnage. Et dans les archives :

```
.par du GOG    19 dossiers, 1842 fichiers, 1.79 Go  ->  0 fichier itm_patch
.par d APM3    19 dossiers, 1862 fichiers, 3.71 Go  -> 19 fichiers, 2,06 Go
```

**3,71 - 1,79 = 1,92 Go.** Les dix-neuf archives d'items sont a elles seules
presque toute la difference entre les deux `.par`. Le GOG, c'est l'archive
d'APM3 moins la personnalisation -- ce qui se comprend : le mini-jeu de
Yakuza 6 n'a pas de carte Aime, donc pas d'items a acheter.

`VF5RE\analysis\disasm\chargeur_archive.txt` avait deja identifie le
demandeur : `0x180038600`, 640 octets, site d'appel **`0x180038803`**, qui
reclame `objset/<perso>itm` **et** `objset/<perso>itm_patch`. Le nom est bati
dans un `std::string` sur la pile, ce qui explique qu'aucun format
`objset/%s` ne figure dans le binaire.

> **Hypothese de tete, pas encore prouvee :** l'ecran de selection charge les
> personnages, reclame `<perso>itm_patch`, ne trouve rien, et reste noir.
> Trois faits la soutiennent -- le chargeur les demande, le GOG n'en a aucun,
> et l'ecran noir arrive juste la. Aucun ne la prouve.

### 10.2 DEUX ROUTES, ET UNE MECANIQUE DEJA MESUREE

`outils\par_masquer.py` porte une mesure qui decide de tout, prise au point
d'arret sur `CreateFileW` (`analysis\import_decors.md`) :

> le moteur consulte **d'abord** l'archive PARC ; ce qui s'y trouve est lu
> depuis l'archive et le disque n'est jamais interroge.

Donc, a l'inverse : **un nom ABSENT de l'index fait retomber le moteur sur
l'arborescence libre de `vf5fs_media\`.** Les dix-neuf noms n'etant pas dans
l'index du GOG, le moteur les cherche deja sur le disque -- et ne les trouve
pas.

| route | ce qu'elle coute | ce qu'elle laisse |
|---|---|---|
| **A. deposer les 19 fichiers libres** dans `banc_gog\vf5fs_media\rom\objset\` | ~2 Go empruntes a APM3, aucune reconstruction d'archive | prouve ou refute l'hypothese en un lancement, et se defait en effacant |
| **B. patcher le chargeur** a `0x180038803` pour qu'il ne reclame pas le `_patch` | du desassemblage | aucun emprunt : les donnees du GOG suffisent, ce qui est le sens du projet |

La route A est aussi l'experience qui tranche. La route B est la reparation.
