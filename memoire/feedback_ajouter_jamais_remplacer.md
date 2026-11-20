---
name: feedback_ajouter_jamais_remplacer
description: "VF5 — la règle du chantier : on AJOUTE des décors, on n'en remplace aucun, sauf les décors d'essai encore inutilisés. Et « d'essai » se MESURE."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-09T05:29:20.312Z
---

Frédéric, 2026-09-09 : **« on est d'accord que tu ajoutes des décors, mais que
tu ne remplaces rien (évite l'erreur TRM), sauf éventuellement les décors
tests. »**

**Et « d'essai » ne se suppose pas, ça se mesure.** `trm` en avait l'air — un
décor d'essai de 1,2 Mo dans une liste de dix-sept. C'était le décor
**TERMINAL**, réparé et validé à l'écran le 2026-09-05, et **treize** de nos
lanceurs le nomment. Le recycler l'a cassé.

`tools/emplacements.py` tranche sur **quatre preuves indépendantes** :

1. la forme du descripteur (`0x180403430 + i*0xF0`) : un décor d'essai n'a que
   **deux** objets, `+0x18`/`+0x20`/`+0x24` à −1, tous deux de son propre
   objset ;
2. la grille de sélection (`0x180400210`, 21 cases, indice en `+0x08`) ;
3. la liste d'aperçus de `0x180174BF0` — 26 indices en dur : 4..25, 39, 40, 41 ;
4. **nos propres lanceurs** : tout code cité dans `tools/*.cmd` hors commentaire.

C'est la preuve 4 qui manquait. Résultat mesuré : **15 libres** — `tst ts3 wht
cid trs evo00…evo09` — et `trm` / `ts2` pris.

Piège de méthode rencontré en écrivant l'outil : ma première signature figeait
les rangs d'objets à 0 et 1, et `ts2` (rangs 1 et 2) ressortait « vrai décor ».
Tester la **forme**, jamais des valeurs devinées — voir
[[feedback_premisse_qui_borne]].

**How to apply:** `importer_decor.py --vers <code>` consulte cette liste et
**refuse** un emplacement pris (`--forcer` passe outre en le disant) — c'est un
garde-fou contre MA faute, pas un mur pour lui : il fait ses contrôles
lui-même. Voir [[feedback_ne_pas_defaire_le_valide]] et
[[project_vf5_import_5r]] ; plan complet dans `analysis/decors.md` §14.
