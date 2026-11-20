---
name: project_vf5_mode_console
description: "VF5 APM3 — le mode console est jouable : SINGLE PLAYER, VERSUS à deux, DOJO, et Échap pour sortir ; huit maillons fabriqués."
metadata:
  node_type: memory
  type: project
  originSessionId: 7b8919f9-a3c9-4e11-a256-ad9c22b4c7e9
  modified: 2026-09-04T19:13:28.520Z
---

**Le mode console de VF5 FS (build arcade APM3) fonctionne en boucle**, vérifié
à l'écran le 2026-09-04 : menu → sélection de personnage → combat → fin de
combat → retour au menu → on relance un combat.

    py -3 tools/patch_moteur.py --resolution 1280 720 --langue --logo-japonais \
        --dural --wxga --dural-grille --mode 0 --menu-init --menu-ranking \
        --transition-game

Lanceur : `tools/console_combat.cmd`. Détail : `analysis/menu_console.md`
(§8 bilan, §9 et §11 transition, §10 entrées) et `analysis/vs_gameover.md`.

## Ce qui manquait, et ce qui ne manquait pas

**Le cœur était intact.** Le mode GAME, ses quatre sous-états (SELECTOR,
MODE_SELECTOR, VS, GAMEOVER) et l'arbitre de fin de combat `0x1800DB100`
n'avaient pas été retirés. Il manquait **six maillons** :

1. le menu ne demandait jamais le mode GAME (aucun site du moteur ne le
   demandait — enquête exhaustive sur les 27 demandes de mode) ;
2. la fin du sélecteur ramenait au menu au lieu de mener au combat ;
3. **l'objet de session n'était créé par personne** sur ce chemin — c'est ce
   qui faisait planter (`0x1800B23A0` rendait NULL) ;
4. après le combat, la branche prise menait à l'écran-titre, le retour au menu
   étant fermé par un prédicat bouchonné ;
5. OFFLINE VERSUS enregistrait ses réglages sans rien lancer (même forme que
   SINGLE PLAYER) — et le joueur 2 n'existait pas, voir [[reference_vf5_joueur2]] ;
6. le menu restait allumé sous le combat et consommait les entrées : sa sortie
   ne démonte ses tâches que sous une condition jamais vraie dans ce cas ;
7. DOJO demandait déjà son mode (par un saut terminal dans une **feuille**,
   invisible aux balayages `.pdata`) mais personne ne demandait son sous-état ;
8. **EXIT GAME existait mais était recachée** : le moteur met son état à
   « normal » (`0x1801E39F1`) puis le repasse à 2 (`0x1801E3A13`). **Un octet**
   la rend visible. Sa validation est intacte — mais le moteur n'a aucune sortie
   de processus (sur borne, l'hôte coupe), d'où l'appel greffé à `ExitProcess`,
   déjà importée. Piège payé à l'écran : `[page+0x224]` n'est **pas un compte
   mais le dernier indice** (boucle `jle`), y toucher ajoute une rangée qui lit
   les libellés hors bornes et affiche « Enter » ;
9. **aucune touche ne permettait de sortir d'un mode** — c'est structurel : sur
   borne l'arrêt vient de l'hôte. `Échap` (clavier) et BACK (manette) sont
   câblés sur le code libre 15, que le moteur ne lit nulle part ailleurs.

## Ce qui reste

Quatre entrées sont parcourues de bout en bout : SINGLE PLAYER, OFFLINE VERSUS
(à deux joueurs), DOJO et TERMINAL — ce dernier avec son vrai décor `trm`,
validé le 2026-09-05, voir [[reference_vf5_gestionnaire_decor]]. `EXIT GAME`
ferme le jeu, et les sous-menus sont redevenus modaux (`--sousmenu`) : tout
cela validé à l'écran le 2026-09-05. Les autres (TERMINAL, OPTION, SCOREBOARDS, DLC)
mènent à des pages identifiées mais jamais ouvertes. `ONLINE BATTLE` est mort : mode 7 bouchonné
aux trois gestionnaires. Et **10 % seulement de la surface console est lue** —
voir `analysis/couverture_console.md`, qui donne le compte et la liste des
angles morts.

Voir [[project_vf5_dural]], [[reference_vf5_verrou_bouchonne]],
[[reference_reprise_vf5]].
