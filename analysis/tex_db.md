# `tex_db.bin` — la dernière des trois, et la plus simple

Établi le 2026-09-09. Outil : **`tools/tex_db.py`**.
Ferme la liste de `analysis/ajouter_un_decor.md` §2 : les six bases du moteur
sont désormais toutes lues pour ce qui concerne les décors.

---

## 1. La carte

```
0x00000   u32 nombre de textures   25 992
0x00004   u32 offset de la table   0x9ABF0
0x00008   deux u32 à zéro
0x00010   POT : les noms, terminés par zéro           633 824 o
0x9ABF0   TABLE   25 992 × 8   {identifiant, offset du nom}
0xCD830   fin du fichier, à l'octet près
```

```
[    0] id 0x0000  F_VF5C_DUMMY
[    1] id 0x0001  F_VF5C_AKI01_FJ_DOUGI
[25991] id 0x7E02  F_VF5C_VAN749_KAMI_T
```

Les préfixes disent la provenance : **VF5C** 19 525 (personnages), **VF5E**
4 921 (décors), **VF5S** 1 364, **VF5IT** 169.

## 2. Ce qui la distingue de `obj_db.bin`

* **la table est TRIÉE par identifiant** — vérifié sur les 25 992 entrées. On
  n'ajoute donc pas à la fin : on **insère** à sa place. `obj_db`, lui, n'est
  trié ni par jeu ni par objet, et s'ajoute à la fin. C'est la seule différence
  de méthode entre les deux outils, et elle n'est pas cosmétique : rien ne dit
  que le moteur ne fasse pas une dichotomie ;
* **l'espace des identifiants est troué** : 25 992 textures pour des
  identifiants allant jusqu'à 32 258, soit **910 plages libres**. La plus grande
  au-delà du dernier identifiant en offre 400, et il existe des trous internes
  de 303, 151, 150… — largement de quoi loger un décor entier ;
* un seul pot de chaînes, pas deux.

## 3. Un décor importé n'a RIEN à y ajouter

Le dojo porte **271 textures**, `F_VF5E_DJO00_*`, identifiants `0x19C7` et
suivants. Une archive importée puis renommée garde ses noms **et** ses
identifiants de texture internes : ils sont déjà dans cette base, sous leurs
noms d'origine. Seule une texture **vraiment neuve** demande une entrée.

C'est la réponse à la réserve écrite le 2026-09-08 dans
`analysis/decors.md` §14.8 — « le risque qui reste, et il est réel :
`tex_db.bin` ». **Le risque n'existait pas** : l'objset importé déclare des
identifiants de texture qui sont ceux de sa génération d'origine, et ils sont
présents. Ce qui manquait au décor posé sur `trs` était ailleurs — les noms
d'auth_3d du descripteur, et la table des murs.

Pour l'anecdote qui situe l'échelle : l'emplacement `trs` ne porte que **deux**
textures à son nom (`F_VF5S_TRS00_MU_BLUE` et une autre). Il n'en avait pas
besoin de plus, puisqu'il chargeait celles du dojo.

## 4. Usage

```
py -3 tools/tex_db.py --essai
py -3 tools/tex_db.py --montrer DJO00
py -3 tools/tex_db.py --libres
py -3 tools/tex_db.py --ajouter F_VF5E_XXX00_IK_MUR --id 26672 --sortie <f>
```

L'aller-retour rend le fichier **identique à l'octet près**, et un identifiant
déjà pris est refusé en nommant son occupant :

```
REFUS : l identifiant 6599 est deja pris (F_VF5E_DJO00_IK_FENCE)
```
