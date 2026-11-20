---
name: reference_vf5_yamp
description: "YAMP (CookiePLMonster) donne les vrais noms du moteur PXD de VF5FS — shift_next_mode, module_start, isl_file_access — et confirme notre numérotation d'états."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 22b68e08-364a-4b50-b67a-c1f1efec0229
  modified: 2026-09-03T18:26:56.616Z
---

**https://github.com/CookiePLMonster/YAMP** — « Yakuza Arcade Machine Player ».
Lance VF5FS en autonome à partir de la copie embarquée dans **Yakuza 6**. C'est
donc un **quatrième build**, sur PC x86-64, très proche du nôtre : sa DLL
s'appelle `vf5fs-pxd-w64-Retail Steam.dll` quand la nôtre est
`vf5fs-pxd-w64-Retail_APM3.dll`.

Sous licence MIT. Lu, pas exécuté.

## Les vrais noms

Notre `SetState` (`0x1800DA800`) s'appelle en réalité :

```cpp
void shift_next_mode(int mode);        // l'etat de tete
void shift_next_mode_sub(int modeSub); // le sous-etat
```

Le moteur expose **`module_start`, `module_stop`** — et notre DLL APM3 exporte
**exactement ces deux symboles**, rien d'autre. La signature est
`int(*)(size_t args, const void* argp)`, avec un `vf5fs_game_config_t` qui porte
**le mode de jeu, la langue, la difficulté, l'énergie, les rounds et le temps**.
La langue est donc un **paramètre de démarrage**, pas seulement l'octet
[[reference_vf5_langue]].

## Notre numérotation est celle de la console

`cs_game.cpp` contient :

```cpp
shift_next_mode(4);
shift_next_mode_sub(48);   // MODE_SUB_MAX
```

`MODE_SUB_MAX = 48` côté Steam ; chez nous **55**. L'écart est exactement de
**sept** — les sept états `APM3_*` ajoutés par la borne. Donc les sous-états
**0 à 47 sont rigoureusement identiques des deux côtés**, et tout ce que YAMP
sait se transporte.

## L'accès aux fichiers a un nom

Interface `isl_file_access`, avec deux implémentations : **`csl_file_access`**
(disque) et **`csl_file_access_archive`** (le `.par`). C'est la règle
archive-puis-disque mesurée dans [[reference_vf5_par_avant_disque]]. YAMP
**substitue l'objet d'accès** — bien plus propre que masquer des noms dans
l'index, et c'est la voie à prendre si l'on doit servir beaucoup de fichiers.

Autres fichiers utiles du dépôt : `pxd_types.h` (primitives du moteur,
`ARCHIVE_FIND_RESULT`), `Y6/gs.h`, `Y6/sl.h`, `Y6/file_access.h`,
`Y6/sys_util.h`, `RenderWindow.cpp` (résolution).

Limites annoncées par YAMP, qui recoupent nos propres chantiers : pas de son,
pas d'en-ligne, **rendu fixe en 720p étiré**, clavier en dur.
