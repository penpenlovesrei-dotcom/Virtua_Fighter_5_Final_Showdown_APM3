---
name: reference_vf5_eclairage_decor
description: "VF5 — l'éclairage d'un décor n'est pas dans son descripteur : table de 41 codes en 0x18039F7A0, lue par 0x1800D7130."
metadata:
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-08T21:55:08.804Z
---

**Où l'éclairage est indexé.** Pas dans le descripteur de décor (qui ne porte
que le code auth_3d, l'objset, la collision et les BGM) mais dans une **table à
part de 41 chaînes minuscules** en `0x18039F7A0`, lue par `0x1800D7130` :

    cmp ecx, 0x28 ; ja ret            <- 41 decors, borne dure
    mov rdx, [0x18039F7A0 + idx*8]    <- "djo", "trm", "du1", ...
    -> 0x1800D7150 compose  ibl/%s.ibl
                            light_param/{light,fog,glow,wind}_%s.txt
                            light_param/envmap_correct_%s.txt

Deux appelants : le combat (`0x18018F8A3`, index = `[gestionnaire+0x5C]`,
l'index CHARGÉ) et l'écran customize (`0x1801C4DD0`). Voir
[[reference_vf5_gestionnaire_decor]] : géométrie et éclairage sont deux appels.

**Ce n'est PAS la cause d'une image ratée sur un emplacement recyclé.** Je l'ai
cru le 2026-09-08 — les réglages de VF5 R (glow `exposure` 2.8 contre 2.0)
sortiraient surexposés dans le rendu de 2010. Faux : Frédéric a reposé le même
décor avec les mêmes fichiers sur `djo`, couleurs correctes. La cause était le
**descripteur** de l'emplacement, dont douze champs de rendu étaient restés
ceux d'un décor d'essai — voir [[feedback_recopier_tout_l_enregistrement]].

`importer_decor.py --eclairage <source>` existe (prendre les cinq pièces
d'éclairage chez une autre génération que la géométrie) mais n'est pas utilisé :
l'éclairage de VF5 R est le bon.

**How to apply:** deux fausses pistes ont été écartées **sans essai à
l'écran** — l'`auth_3d` (les `.a3da` du dojo 5R ne portent que des caméras :
zéro `light`, `fog`, `ambient`) et le masquage du `.par`. Chercher d'abord ce
que le fichier CONTIENT avant d'accuser le chemin qui l'apporte. Voir
[[project_vf5_import_5r]] et `analysis/decors.md` §13.
