---
name: reference_clavier_frederic
description: "Le clavier de Frédéric : AZERTY compact, sans Début ni Fin — et les noms de touches que Supermodel accepte."
metadata:
  type: reference
---

Trois contraintes à vérifier **avant** de lier une touche dans Supermodel. Elles
ont coûté cher plusieurs fois, la dernière le 2026-08-16.

**1. Le clavier est compact : ni `Début` ni `Fin`.** Il a `Inser` et `Suppr`.
Le commentaire de `Src/Inputs/Inputs.cpp` a longtemps tenu `Inser` et `Fin` pour
« déjà en service et éprouvées » — c'était vrai d'`Inser` seulement : une touche
liée et jamais pressée n'a rien prouvé. `UICycleStage` est donc passé de `Fin` à
`Alt+F9`.

**2. Il est AZERTY, et DirectInput lit des positions physiques.** `KEY_M`
désigne la place du M en QWERTY, soit la touche `,` en AZERTY. Sur la rangée
QSDFGHJKLM contre ASDFGHJKL;, seules les extrémités diffèrent : **G J K L** sont
au même endroit sur les deux. La rangée des chiffres et les touches de fonction
aussi.

**3. Un nom de touche inconnu est accepté en silence.** `KEY_DELETE` n'existe
pas ; le nom est **`KEY_DEL`**. Une séance entière en a conclu à tort que
Supermodel n'avait pas Suppr. Relire `s_validKeyNames` dans
`Src/Inputs/InputSystem.cpp` avant de lier, jamais deviner.

Et une touche doit aussi être libre **côté jeu** : une combinaison Alt ne la
retire pas au jeu. Voir le long commentaire en tête de `Inputs.cpp`, qui tient le
compte des essais ratés.

Concerne [[project_fv2_menu_console]], [[project_tex3d_hd]], [[project_tuiles_hd]].

**Les bascules ajoutées, état au 2026-08-16** — les touches uniques sont
épuisées, il ne reste que des combinaisons Alt :

| | |
|---|---|
| `Inser` | vie infinie joueur 1 |
| `Suppr` | **les deux captures**, 2D et 3D, en marche / en veille |
| `Alt+F9` | choix du décor (était sur `Fin`, injoignable) |

Une touche pour les deux dumps, pas deux : les lanceurs sont séparés et
n'activent qu'une capture chacun. J'avais d'abord pris `Alt+L` pour le 2D, en
traitant les deux dumps comme indépendants — Frédéric a relevé que ça n'avait
aucun sens, et ça gaspillait la dernière lettre sûre de son clavier.

Règle des veilles : elles suspendent l'**enregistrement**, jamais l'objet. Le
détruire viderait l'inventaire, et couper le pointeur priverait le cache des
invalidations d'écriture VRAM — il rendrait des hachages périmés au réveil.
