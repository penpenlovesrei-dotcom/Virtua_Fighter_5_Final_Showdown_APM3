# Ce qu'on a lu du mode console, et ce qui reste

Ecrit le 2026-09-04, apres que le combat a demarre depuis le menu console.
Question de Frederic : « tu as desassemble tout le fonctionnement du mode
console ? tu avais omis les inputs playstation, il reste quoi d'inconnu ? »

Reponse courte : **non, et de loin.** Environ un dixieme.

## 1. Le denominateur, mesure

`tools/couverture.py` part des gestionnaires **vivants** de la machine a etats
(les trois handlers de chaque mode console et de chaque sous-etat non
bouchonne) et suit le graphe des **appels directs**.

| | |
|---|---:|
| fonctions du binaire | 13 661 (3 127 155 o) |
| surface atteinte par le parcours console | **646** (172 257 o) |
| nommees au moins une fois dans `analysis/*.md` | 67 (**10 %**) |
| nommees au moins trois fois -- c'est-a-dire travaillees | 23 (**4 %**) |

Et 646 est un **minorant** de la surface reelle : le graphe ne suit que les
`call rel32`. Tout ce qui passe par une **vtable** en est absent -- or les
pages de menu sont precisement pilotees par vtable (`0x180532AE8` et ses
soeurs). La surface vraie est plus grande, pas plus petite.

## 2. La forme de l'angle mort, et pourquoi les entrees y etaient

L'omission des entrees n'etait pas un oubli isole, c'est une **classe**.
J'ai suivi la machine a etats : modes, sous-etats, pages, scenes. Tout ce qui
est atteint par un **service partage** -- appele de partout, appartenant a
personne -- n'apparait jamais sur ce chemin-la. Les entrees en sont un cas
parfait : trois etages (`apm.dll` -> masque arcade -> codes logiques), aucun
sur le graphe des etats.

Les autres services partages, donc les autres angles morts de meme nature :

* la **sauvegarde et le profil** (`CARD SELECTOR`, `DATA SELECTOR`) ;
* le **son** et la musique (`0x180185xxx`, `0x180186xxx`) ;
* les **textes** (`string_array`, resolu seulement le 2026-09-04) ;
* le **moteur de scenes AET** lui-meme (`0x1801Bxxxx`), dont on n'utilise que
  quatre ou cinq accesseurs ;
* l'**allocation** (`0x180218410` et l'etiquette `SEL_DATA`).

## 3. Ce qui reste inconnu, par ordre de risque

**Ce qu'on vient de fabriquer, et qu'on ne comprend qu'a moitie.**
`0x1800B3620(ecx)` cree l'objet de session (0x16E0 octets) et on lui passe
`0` parce que le chemin APM3 passe `0`. On ne sait pas ce que cet argument
signifie, ni ce que l'objet contient. Le combat marche ; on ignore ce qu'on n'a
pas initialise.

**Le sous-systeme joueurs/session, `0x1800B0000`-`0x1800B9000`.** Quatre des
plus grosses fonctions jamais nommees y sont : `0x1800B0500` (3028 o),
`0x1800B5EB0` (2639 o), `0x1800B8540` (2026 o). On n'en a lu que deux feuilles.

**La suite du combat : `VS` (19) et `GAMEOVER` (20).** On y entre desormais, on
n'a pas lu leurs gestionnaires. Le « rejouer » de `0x1800DB950` demande VS ou
SELECTOR ; ce qui se passe apres un combat est donc non verifie.

**`MODE_SELECTOR` (18).** Vivant, jamais emprunte, jamais lu. C'est
probablement l'ecran « 1P / VS / entrainement » de la console.

**Les sous-menus qu'on a nommes sans les ouvrir** : CUSTOMIZE (`CUST_MAIN`,
`CUST_EQUIP`, `COSTUME MENU`, `SEL ITEM MENU`), OPTION et ses six scenes,
REPLAY, RANKING, DLC STORE, PROMOTION. Le bilan de la section 8 de
`menu_console.md` dit **ou** ils menent, pas **ce qu'ils font**.

**Le DOJO**, `0x180200000`-`0x18020B000` : une trentaine de scenes `TRN_*` et
`FREE_*`. Entierement vierge.

**`0x180227790`, 7373 octets, aucune chaine, jamais nommee.** La plus grosse
fonction de la surface console qu'on n'a jamais ouverte.

## 4. Ce qui est solide

Pour ne pas donner l'impression inverse, voici ce qui est **etabli et verifie a
l'ecran**, pas seulement lu :

* la machine a etats : deux tables, indexees par clef, 10 modes et 55
  sous-etats, avec l'inventaire des bouchons (`machine_console.md`) ;
* le bilan des liens du menu, entree par entree, et le plafond qui les borne
  (`menu_console.md` section 8) ;
* la chaine des entrees, de la touche au code logique (section 10) ;
* la grille de selection : tables de disposition, liste de cases, deplacement
  du curseur, desactivation -- et Dural jouable (`dural.md` section 14) ;
* les trois maillons de la transition vers le combat (sections 9 et 11).
