---
name: feedback-pas-de-donneur
description: "Ne rien emprunter à un étage ou à un objet du jeu : partir de ressources qu'on crée. Frédéric l'a demandé une dizaine de fois."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a42b6c0d-1a36-40d8-b5ab-289a8f4629c0
  modified: 2026-08-29T21:43:12.299Z
---

**Ne pas emprunter. Créer.** Frédéric l'a redit le 29/08/2026, excédé : « on revient encore
à cette histoire de donneur : il faut partir d'un stage que l'on crée !!! C'est la énième
fois que je le dis. »

Les pages de décor l'ont déjà fait — chaque étage ajouté a sa propre archive
(`outils/archive.py`, `resources/stages/1535..1549.bin`). **Les objets animés, non** : ils
empruntent le motif d'un objet existant, en récrivant sa liste de morceaux dans la table
de trans.

**Why:** l'emprunt échoue par nature. La table de trans est partagée ; le `cg_number` du
donneur défile trame après trame, donc le motif change sous nos pieds ; ses motifs n'ont
pas tous la même longueur ni les mêmes tailles de morceaux — `CODE_16X16` ne vaut 16×16
que dans le groupe où il a été relevé. Chaque contournement a produit un gel : trois
groupes différents (`0x17`, `0xd3`, `0x2c`) tous avec « 0 emplacements occupés », des
plantages au changement d'étage, et des menus d'après-combat abîmés.

**How to apply:** quand une ressource du jeu doit porter quelque chose à nous — motif,
groupe de textures, table de trans, archive — on en **fabrique une**, comme `archive.py`
fabrique une archive de pages. On ne récrit jamais celle d'un autre, même « temporairement ».

Voir [[reference-3sx-table-trans-partagee]] et [[project-ajouter-decors-3sx]].
