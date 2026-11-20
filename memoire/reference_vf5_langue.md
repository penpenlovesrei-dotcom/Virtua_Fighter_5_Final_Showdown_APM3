---
name: reference_vf5_langue
description: "VF5 APM3 — un seul octet (moteur+0x64D956) bascule tout le jeu du japonais à l'anglais ; vérifié à l'écran."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 22b68e08-364a-4b50-b67a-c1f1efec0229
  modified: 2026-09-03T17:34:23.418Z
---

**Un octet suffit.** `moteur+0x64D956`, dans `.data` : **0 = Japon**, non nul =
export. Vérifié à l'écran le 2026-09-03 : « ça fonctionne, plus de caractère
japonais à l'écran ».

Le sélecteur est minuscule et se lit d'un coup :

```
0x1802447C0  movzx eax, byte ptr [0x18064D956]
0x1802447C7  neg   al
0x1802447C9  sbb   eax, eax
0x1802447CB  and   eax, 2          ; rend 0 (Japon) ou 2 (export)
0x1802447CE  ret
```

L'octet vaut 0 au démarrage et **le moteur le réécrit une fois vers t = 3 s** :
le forcer deux fois suffit à le faire tenir. `tools/langue.py --export` le fait
à chaud, `--japon` le défait.

Quatre appelants, dont un par élément visible :

| appelant | choisit |
|---|---|
| `0x18006BBD1` | **le logo** : `logo_jpn` ou `logo_usu` |
| `0x1801AAF4F` | écrit `[rdi+0x240] = 0 ou 2`, puis appelle avec `edx = 0x19` |
| `0x1801BB077` | libellé de victoire `" W "` |
| `0x1801BB090` | libellé de défaite `" L "` |

**J'avais sous-estimé sa portée** : j'annonçais que le japonais peint dans les
planches 2D (`格闘スタイル`, les données de trame du DOJO) resterait. Faux — la
bascule a tout emporté. Le site `0x1801AAF4F`, qui écrit un champ de config,
propage sans doute bien plus loin que les trois autres.

Ce que le drapeau ne peut pas toucher en revanche : les **noms d'articles**, qui
sont en japonais **dans les données** (`dur_itm.csv` porte 鏡面反射体（銀）,
ガラス, 石膏). Il faudrait réécrire les CSV.

Détail dans `analysis/langue.md`. Nos binaires viennent du dump **`APM3_US`**,
pas de `APM3_FS` — on tourne déjà sur le build export, et pourtant le drapeau
est à 0. Voir [[reference_vf5_resolution]] pour l'autre patch du même moteur :
les deux se marchent dessus si l'on empile les sauvegardes `.origine`.
