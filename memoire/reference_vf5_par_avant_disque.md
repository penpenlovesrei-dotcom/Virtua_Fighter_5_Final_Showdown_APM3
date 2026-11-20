---
name: reference_vf5_par_avant_disque
description: "VF5 APM3 — ce qui est dans `vf5fs_data.par` vient du `.par` ; seul ce qui en est absent retombe sur les fichiers libres. Et ce `.par` est un lien dur vers le dump."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 22b68e08-364a-4b50-b67a-c1f1efec0229
  modified: 2026-09-10T06:36:37.875Z
---

Le moteur résout un fichier de données en consultant **d'abord l'archive
`vf5fs_data.par`** (3,99 Go, conteneur `PARC`). Ce qui s'y trouve est lu depuis
l'archive et **le disque n'est jamais interrogé**. Seul ce qui est absent de
l'index retombe sur l'arborescence libre `vf5fs_media/`.

Mesuré par point d'arrêt sur `KernelBase!CreateFileW` (`tools/tracer_fichiers.py`) :

| fichier | dans le `.par` | lu depuis |
|---|---|---|
| `stgdjo.farc`, `stghai.farc` | oui | l'archive |
| `vfes_bgm_stg_hai.adx`, `shader_pxd_w64.farc`, `se_stage_are.csb` | non | le disque |

Conséquence : **déposer un fichier dans `vf5fs_media/rom/objset/` ne fait rien**
si son nom est dans le `.par`. Pour qu'il soit lu, il faut neutraliser l'entrée
dans l'index de l'archive (la renommer suffit), ou reconstruire le `.par`.

**Piège, et il est grave** : `runtime/media/vf5fs/vf5fs_data.par` est un **lien
dur** (même inode, 2 liens) vers celui du dump en lecture seule. Écrire dedans
écrirait dans le dump, sans aucun avertissement. Casser le lien par une vraie
copie avant toute modification.

**Le corollaire, payé le 2026-09-10 : l'archive MASQUE ce qu'on a oublié de
poser.** En *remplaçant* un décor (le code reste `djo`), on ne masque que les
fichiers qu'on pose ; tous les autres continuent de venir du `.par`, donc un
oubli ne se voit pas. En *ajoutant* (code `d5r`), plus rien ne répond, et l'oubli
gèle l'écran de chargement — ici `envmap_correct_d5r.txt`, le sixième chemin
d'éclairage, absent du dump VF5R. Donc : la liste des fichiers d'un décor se lit
dans le `.par` (`par_inventaire.py --grep "(?i)<code>"` : **onze**), jamais de
mémoire, et un ajout n'hérite d'aucune tolérance qu'un remplacement avait.

Ne jamais conclure sur ce genre de question par une capture d'écran : le
sélecteur de décor est par défaut sur **Random**, donc on ne sait même pas quel
décor s'est chargé. Voir [[feedback_lire_le_code_pas_l_image]] et
`analysis/import_decors.md`.
