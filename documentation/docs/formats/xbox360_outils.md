# Lire le dump Xbox 360 : les outils, et ce qu'ils donnent

> **PÉRIMÉ SUR LE POINT CENTRAL (2026-10-01).** Ce fichier concluait que la
> piste X360 était « un chantier à part entière, à ne rouvrir que si la voie
> APM3 se ferme vraiment », faute de décodeur LZX. **Le décodeur existe
> désormais** : `tools/lzx.py`, écrit depuis la spécification, et
> `tools/xex.py` lit la compression 2. L'exécutable est ouvert —
> `extracted/X360_FS/sel/default.img`, 17,6 Mo de PowerPC, 264 types RTTI.
> Tout le reste de ce fichier (le format XEX2, le STFS, l'inventaire du
> paquet) reste juste et utile. **Pour l'état présent, lire
> `analysis/x360_fs.md`.**


Liens fournis par Frederic le 2026-09-03, a conserver :

- **https://github.com/emoose/xbox-reversing**

(Le second lien du message etait identique au premier.)

Mentionne dans son README, pour la version native du chargeur XEX :
**`idaxec`**, du meme auteur.

---

## Ce que le depot contient, et ce qui nous sert

| element | contenu | utile ici ? |
|---|---|---|
| **`templates/xbox-360/XEX2.bt`** et ses quatre compagnons (`XEX2Headers.bt`, `XEX2OptionalHeaders.bt`, `XEX2FlagsAndEnums.bt`, `XEX2Functions.bt`) | la specification complete du format XEX2, en gabarits 010 Editor lisibles comme du texte | **oui, decisif** : c'est la documentation qu'il fallait pour ecrire un lecteur XEX |
| **`templates/xbox-360/Xbox360Container.bt`** | le format des conteneurs Xbox 360 | **oui** : la disposition STFS, qu'on doit traverser pour extraire `default.xex` |
| **`stfschk/`** | verificateur de hachages et de signatures des paquets STFS (LIVE/PIRS/CON) | **oui, comme reference** : du code qui parcourt reellement un paquet, dont les tables de hachage qu'il faut savoir sauter |
| **`xbox360.py`** + **`x360_imports.py`** | chargeur XEX pour IDA 7.0+, en Python | **oui, comme source** : la logique d'en-tete, de sections et d'imports est directement lisible |
| `templates/xbox-360/XDBF.bt`, `XboxGDFImage.bt`, `Xbox360KeyVault.bt`, `recctrl.bt` | tableau de bord, images de disque, coffre a cles | non |
| `templates/xbox`, `templates/xbox-one` | autres generations | non |

Licence BSD-3-Clause.

---

## La limite a connaitre avant de s'engager

Le chargeur `xbox360.py` annonce lui-meme : *« should support loading almost all
**(uncompressed)** XEX formats »*. **Il ne gere pas les XEX compresses.**

Or XEX2 a trois modes :

1. **aucun** -- lisible directement ;
2. **« basic »** -- une suite de blocs (taille de donnees, taille de zeros) : la
   « decompression » se reduit a recopier et a remplir de zeros. Trivial ;
3. **« normal »** -- LZX. C'est le morceau cher.

**Beaucoup de titres de detail sont en mode 1 ou 2.** La premiere chose a faire
n'est donc pas d'ecrire un decompresseur, mais de **lire l'en-tete de notre
`default.xex` et de regarder dans quel mode il est**. Les gabarits `XEX2*.bt`
donnent exactement ou lire.

---

## Ou en est notre dump

`extracted/X360_FS/.../7D2DF36BD11FB8394C3D652339E6FE1DA1337B1058`, 2,05 Go,
paquet STFS `LIVE`.

Deja verifie sans aucun outil : **les blocs de donnees sont en clair**. On lit
directement dans le paquet `default.xex` (0xC380), l'en-tete `XEX2` (0xD7A000),
`stgdjo.farc`, `mothead_DUR`, `ctrl_DUR`, `chritm_tbl`, `spr_t_itmaki`.

En revanche `UNLOCK_DURAL`, `ARCADE MENU` et `mot_%s.bin` n'y apparaissent pas :
ils sont dans l'executable, qui est donc bien chiffre ou compresse.

## MESURE : notre XEX est dans le cas cher

En-tete lu le 2026-09-03, directement dans le paquet (`FILE_FORMAT_INFO` a
`0xD7A000 + 0x1B70`) :

```
magic XEX2, 15 en-tetes optionnels
ImageBase 0x82000000, point d'entree 0x823DEE78, image 16,8 Mo
chiffrement : 1  -> AES (cle de detail publique)
compression : 2  -> NORMAL, c'est-a-dire LZX, fenetre 0x8000
```

**C'est le mode 3, le plus couteux.** Ni « aucun » ni « basic » : il faut un
decodeur LZX complet (arbres de Huffman, deltas, deplacements alignes), et c'est
exactement ce que le chargeur `xbox360.py` d'emoose annonce ne pas gerer.

Le depot reste utile pour la **specification** (les gabarits `XEX2*.bt` ont
permis de lire cet en-tete en dix minutes) mais il ne donne pas le decodeur.

**Consequence sur le cout** : la piste X360 n'est plus « un detour », c'est un
chantier a part entiere. A ne rouvrir que si la voie APM3 se ferme vraiment.

## L'ordre des operations, le jour ou l'on s'y met

1. lire `XEX2.bt` et `XEX2Headers.bt`, puis l'en-tete a `0xD7A000` : **quel mode
   de compression, quel chiffrement** ;
2. si le mode est « aucun » ou « basic », ecrire le lecteur -- c'est court ;
3. traverser le STFS pour extraire proprement `default.xex` (sauter les tables
   de hachage, tous les 0xAA blocs) -- `Xbox360Container.bt` et `stfschk/` disent
   comment ;
4. desassembler du PowerPC gros-boutiste et chercher la table de la grille de
   selection, celle qui manque dans APM3.

Rappel : **aucun code ne se transporte** de la 360 vers APM3 (PowerPC contre
x86-64). Ce qu'on irait chercher, c'est la **logique lue comme une donnee**,
dans un build ou Dural fonctionne.
