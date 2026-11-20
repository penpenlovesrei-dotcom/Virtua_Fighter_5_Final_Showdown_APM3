# LE CODE D'APM3 SUR LES DONNEES DE R.E.V.O.

Mesure du 4 novembre 2026. Banc : `FS APM3\banc_revo`, monte par
`outils\monter_banc_revo.cmd`. Meme protocole que
[APM3_SUR_DONNEES_GOG.md](APM3_SUR_DONNEES_GOG.md).

## 1. La question

> « la DLL et l'exe d'APM3 peuvent-ils demarrer avec les fichiers de REVO ? »

## 2. LA REPONSE EST OUI, ET ELLE VA JUSQU'AU COMBAT

Avec **un seul fichier emprunte**, `vfes.exe` et le module APM3 vierges
atteignent un vrai combat sur les donnees de R.E.V.O. : Akira dans la
cathedrale, barres de vie, compteur de manches 2/5, ATH complet
(`capture_revo_emprunt_140s.png`).

C'est beaucoup plus loin que le GOG, qui s'arretait a l'ecran noir d'apres le
titre. La raison est nommee au S4.

```
sans emprunt   MORT a 3 s, code 0xC0000005 (violation d'acces)
avec emprunt   12s  moyenne  79,1/765     30s  noir (chargement)
               55s  noir                  80s  moyenne 153,3/765
              110s  moyenne 157,7/765    140s  COMBAT, moyenne 245,8/765
```

## 3. LA DECOUVERTE PRINCIPALE : R.E.V.O. EMBARQUE L'ARCHIVE DE LA BORNE

Elle ne se cherchait pas, et elle vaut plus que l'experience elle-meme.

```
.par de REVO    19 dossiers, 1862 fichiers, 3 987 499 008 o
.par d'APM3     19 dossiers, 1862 fichiers, 3 987 499 008 o

communs 1862    seulement dans REVO 0    seulement dans APM3 0
communs mais de TAILLE DIFFERENTE : 1
    mot_db.farc    REVO 83 726 o    APM3 83 728 o    ecart -2
```

**Memes noms, memes tailles, a DEUX octets pres dans un seul fichier.**
R.E.V.O. ship l'archive de donnees de la borne, pratiquement telle quelle.

Consequences immediates, chacune mesuree :

| | GOG | REVO |
|---|---|---|
| `<perso>itm_patch.farc` | **0** | **19**, tailles identiques a APM3 |
| noms de BGM | `vf5fs_bgm_*`, `h_*`, `vf5r_*` | **268 `vfes_bgm_*`** -- la nomenclature ARCADE |
| `vfes_se_logo_sega.adx` | absent | **present** |
| fichiers de `vf5fs_data.par` | 1842 | **1862**, comme APM3 |

> **Le patch de chaines du S9 de `APM3_SUR_DONNEES_GOG.md` serait ici
> NUISIBLE.** Il repeint `vfes_bgm_*` vers `vf5fs_bgm_*` ; les donnees de
> REVO portent precisement les premiers. Le banc `banc_revo` pose donc le
> module **VIERGE**, et `monter_banc_revo.cmd` le lie depuis `SOURCES`, pas
> depuis `banc_gog`.

Et les dix-neuf archives d'items qui manquaient au GOG -- cause probable de
son ecran noir d'apres-titre -- sont ici. C'est coherent avec le fait que ce
banc-ci, lui, atteint le combat.

## 4. LE SEUL MUR, ET IL ETAIT PREDIT

```
vf5fs_media\w64\              REVO            APM3            GOG
  shader_pxd_w64.farc          9 026 o    10 530 083 o    10 530 083 o
  shader_pxd_w64_d3d12.farc   53 778 o          --              --
  shader_vf5_w64.farc             --         3 303 o           --
```

**R.E.V.O. a vide l'archive de nuanceurs D3D11** -- 9 Ko la ou la borne en a
10,5 Mo -- et a mis les siens dans une archive D3D12. Le module d'APM3 est
D3D11 (il importe `D3DCOMPILER_47`) : il va chercher 10,5 Mo et en trouve 9 Ko.

Sans emprunt : **violation d'acces a 3 secondes**. Avec l'archive D3D11
d'APM3 a la place : le jeu va au combat. **Un fichier, et un seul**, separe
le plantage du combat.

C'est aussi ce qui explique, a posteriori, pourquoi le GOG avait affiche du
premier coup : son `shader_pxd_w64.farc` est identique a celui d'APM3 **a
l'octet pres**. Le GOG est un portage D3D11 ; R.E.V.O. est un portage D3D12.
Le partage des donnees suit l'API graphique, pas la date.

L'emprunt est ici un **REMPLACEMENT**, pas un ajout : le fichier existe des
deux cotes sous le meme nom. `monter_banc_revo.cmd emprunt` met celui d'APM3
a la place et le dit ; sans l'argument il remet celui de REVO.

## 5. CE QUE R.E.V.O. A EN PLUS, ET QUE LE MODULE APM3 IGNORE

```
ws_rob_data.par          3 229 696 o
ws_sound.par             4 759 552 o
vf5fs_media\rom_200\     chritm_tbl.farc, resident.farc (+ .r2421, .r2427),
                         string_array.farc, rob\, training\
bgm                      337 fichiers contre 285 -- dont vf5revo_bgm_btl_final,
                         vf5revo_bgm_map, vf5revo_bgm_tor_final
```

La couche `rom_200\` n'existe ni chez APM3 ni au GOG, et `resident.farc`
y porte deux revisions numerotees (`.r2421`, `.r2427`). C'est le materiel
propre a World Stage. Poses dans le banc, ils n'ont rien casse ; rien ne dit
que le module d'APM3 les lise.

## 6. CE QUE CELA CHANGE POUR LE PROJET

C'est le point qui depasse l'experience.

`analysis\BASE_LEGALE.md` pose que **la version APM3 n'est pas censee etre
disponible aux particuliers** et que rien d'elle ne part dans un paquet. Or
on vient de mesurer que **les donnees de la borne sont deja dans R.E.V.O.**,
que l'utilisateur possede legitimement. La matiere du jeu n'a donc pas besoin
de venir d'APM3.

Ce qui manque pour faire tourner le jeu d'arcade sur les donnees de R.E.V.O.
se reduit, a cette mesure, a **une seule archive** : les nuanceurs D3D11.
Et elle ne manque que parce qu'on fait tourner le module D3D11. Le module de
R.E.V.O., lui, est D3D12 et a les siens.

> La question « que faut-il emprunter a APM3 ? » a donc une reponse courte,
> et elle tient en un nom de fichier.

## 7. CE QUE CELA NE DIT PAS

1. **Rien n'a ete joue par une main.** Les captures viennent du scenario
   d'`apm_entrees.txt`. Jouabilite, duree d'une partie, stabilite au-dela de
   140 s : non mesurees.
2. **Le son n'a pas ete ecoute.** Les noms sont pourtant les bons ici, ce qui
   laisse attendre mieux qu'au GOG -- mais c'est une attente, pas une mesure.
3. **`mot_db.farc` differe de 2 octets** et personne n'a regarde en quoi.
4. **L'essai reciproque reste entier** : le module D3D12 de R.E.V.O. sous
   `vfes.exe` n'a pas plus ete tente que celui du GOG. Il est pose dans le
   banc en temoin.

## 8. REFAIRE LA MESURE

```
outils\monter_banc_revo.cmd              donnees REVO pures  -> plantage a 3 s
outils\monter_banc_revo.cmd emprunt      + nuanceurs D3D11   -> combat
outils\capturer_banc_gog.ps1 -Banc banc_revo -Moments 12,30,55,80,110,140 -Suffixe _revo
```

Le script de capture refuse desormais de mesurer si un `vfes.exe` tourne
deja : le 4 novembre, des relevés ont ete rendus incoherents parce que deux
instances se recouvraient a l'ecran. Un instrument qui peut etre trompe doit
dire quand il l'est.
