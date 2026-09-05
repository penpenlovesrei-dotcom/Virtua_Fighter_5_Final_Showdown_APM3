# Mettre le jeu en anglais plutot qu'en japonais

Question du 2026-09-03. Il y a bien un **drapeau de region** dans le moteur, et
il vaut **0 = Japon** par defaut. Reste a savoir jusqu'ou il porte.

---

## 1. Ce qu'on ne trouve pas

Aucun fichier d'actif suffixe par langue dans le dump : pas de `*_jpn.*`,
`*_usa.*`, `*_eng.*`, ni de `msg`, `text`, `lang` ou `str`. Il n'y a donc **pas
deux jeux de ressources** entre lesquels basculer.

A noter aussi : nos binaires (`vfes.exe`, le moteur) viennent du dump
**`APM3_US`**, pas de `APM3_FS` -- empreintes identiques. On tourne deja sur le
build export, et pourtant une partie de l'interface est en japonais.

## 2. Le selecteur, et il est minuscule

En remontant le choix `logo_jpn` / `logo_usu` :

```
0x1802447C0  movzx eax, byte ptr [0x18064D956]
0x1802447C7  neg   al
0x1802447C9  sbb   eax, eax
0x1802447CB  and   eax, 2          ; rend 0 (Japon) ou 2 (export)
0x1802447CE  ret
```

L'idiome classique « booleen -> 0 ou 2 ». **Tout depend d'un seul octet**, en
`.data`, a `moteur+0x64D956`.

Mesure a l'execution : il vaut **0** au demarrage, et le moteur le reecrit une
fois vers t = 3 s. Le forcer a 1 deux fois suffit a le faire tenir.

## 3. Quatre appelants, et pas seulement le logo

| appelant | ce qu'il choisit |
|---|---|
| `0x18006BBD1` | `logo_jpn` ou `logo_usu` |
| `0x1801AAF4F` | ecrit `[rdi+0x240] = 0 ou 2`, puis appelle avec `edx = 0x19` |
| `0x1801BB077` | le libelle de victoire : `" W "` ou son equivalent |
| `0x1801BB090` | le libelle de defaite : `" L "` ou son equivalent |

C'est donc **un drapeau de langue**, pas un simple choix d'ecusson. Mais quatre
sites, c'est peu : il ne peut pas couvrir a lui seul tout ce qui est en japonais
a l'ecran.

## 4. Ce qui restera probablement en japonais

Le texte japonais visible ne vient pas tout de ce drapeau :

- **`格闘スタイル`** (style de combat) sur l'ecran de chargement, et les noms de
  style : dessines dans les planches 2D `aet_*` / `spr_*`, pas dans le binaire ;
- **`攻撃発生`, `硬化差`** (donnees de trame du mode DOJO) : idem ;
- les **noms d'articles** : ils sont en japonais **dans les donnees** --
  `dur_itm.csv` porte 鏡面反射体（銀）, ガラス, 石膏. Aucun drapeau ne les
  traduira ; il faudrait reecrire les CSV.

Autrement dit : le drapeau bascule ce que le **code** choisit ; il ne touche pas
ce qui est **peint dans une image** ni **ecrit dans une donnee**.

## 5. Outils

- `tools/langue.py --export` bascule le drapeau a l'execution (`--japon` le
  remet). Reversible, sans rien modifier sur le disque.
- Pour un correctif permanent, la voie propre est le **patch statique** du
  getter : remplacer `0x1802447C0` par `mov eax, 2 ; ret` (six octets :
  `B8 02 00 00 00 C3`). Attention : la DLL porte deja le patch de resolution et
  son `.origine` -- il faudra unifier les deux patcheurs plutot que d'empiler
  des sauvegardes.
