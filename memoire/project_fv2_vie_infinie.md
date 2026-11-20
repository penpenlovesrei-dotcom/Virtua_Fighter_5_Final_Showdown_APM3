---
name: project-fv2-vie-infinie
description: "Vie infinie FV2 — adresses de vie mesurées en combat, gel runtime livré ; la démo d'attraction ne sert à rien pour ça."
metadata: 
  node_type: memory
  type: project
  originSessionId: 8d84de2e-f177-4fa3-8104-6c97323a902a
  modified: 2026-08-15T13:21:18.029Z
---

Demandé par Frédéric le 2026-08-12 : « un patch pour avoir de la vie infinie
dans Fighting Vipers 2, ça existe ? ». **Non, ça n'existait pas** — les seuls
codes vie infinie publiés visent le premier *Fighting Vipers* sur Saturn ;
pour FV2 on ne trouve que des codes Dreamcast, et Supermodel n'a aucun moteur
de triche. Fabriqué et livré dans la foulée.

**Adresses** (bloc joueur, même pas de `0x7000` que `*1P CHARA`) :
vie courante **`0x00700566`** / **`0x00707566`**, maximum `0x?00568`, copie du
maximum `0x?0056A`. Entiers 16 bits. La table du menu de debug ne les expose
**pas** : elle ne donne que les *réglages* (`*1P ENERGY` = `0x00120540`,
`*VS ENERGY` = `0x120542`, 16 bits, borne 2000) — voir [[project_fv2_mod]].

Deux pièges qui ont orienté toute la séance :

1. **La démo d'attraction n'inflige aucun dégât** (Frédéric l'a signalé, la
   sonde l'a confirmé : 170 s sans un point perdu). Toute recherche de valeur
   de combat exige un **vrai combat**.
2. Hors combat, `0x?00566` vaut `0x2000` ou n'importe quoi — il est
   **inidentifiable** sur un écran de titre ou de sélection. Je l'avais
   d'ailleurs écarté à tort sur cette base avant de le retrouver par la mesure.

**Pas d'instruction unique à neutraliser** : le seul `sth` d'écart `0x566` de
l'image (`0x00096A04`) est en réalité de la donnée. La routine de dégâts passe
par un pointeur intermédiaire, introuvable par balayage statique sans points
d'arrêt. D'où le gel runtime, comme `roster.py`.

Livré : **`fv2mod\vie.py`** (`--deux`, `--joueur`, `--attacher`) et le
raccourci **`FV2 - Vie infinie.cmd`**. Deux garde-fous : n'écrire que si le
maximum lu est dans 1..2000, et que si la vie est **strictement positive** —
ranimer un K.O. laisserait la manche dans un état imprévu. Vérifié en combat
réel et confirmé en jeu par Frédéric le 2026-08-12.

Documenté au **§8 ter du HANDOFF.md**, qui fait foi. Adresses ajoutées à
`symbols.py`. Technique d'automatisation du combat : voir
[[reference_supermodel_memoire]].

**Porté dans l'émulateur le 2026-08-13**, sur demande de Frédéric qui voulait
une bascule au clavier : `GameFV2::HoldInfiniteLife`, touche **`Inser`**,
appelée hors du bloc du menu pour marcher aussi avec `-no-menu`. Même logique et
mêmes garde-fous que `vie.py`. Documenté au §9 bis de
`SupermodelSrc\Docs\MenuConsole.md`. **Non revérifié en combat depuis
l'émulateur** — ça demande un vrai combat.

**Option `-infinite-life` ajoutée le 2026-08-15** (réglage `InfiniteLife`,
section `Inputs`, éteint par défaut) : démarre avec la bascule déjà mise,
`Inser` la basculant toujours en jeu. Posée dans `Dump tuiles 2D.cmd` et
`Dump textures 3D.cmd` — les deux campagnes de capture doivent atteindre un
combat et **y rester**, puisque seul ce qui est réellement affiché est capturé.

Avantage décisif de la version émulateur : `vie.py` dépend du RVA statique
`0x65D098`, propre au binaire déployé, qui **ne vaut pas** pour
`SupermodelSrc\bin64\supermodel.exe`. Pour jouer avec les assets HD *et* la vie
infinie, c'est la version émulateur qu'il faut. Voir [[project_tuiles_hd]] et
[[project_fv2_menu_console]].
