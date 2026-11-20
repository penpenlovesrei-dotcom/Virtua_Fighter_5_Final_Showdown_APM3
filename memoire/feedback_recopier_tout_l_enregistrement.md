---
name: feedback_recopier_tout_l_enregistrement
description: "Recycler un emplacement, c'est cloner TOUT son enregistrement, pas les champs qu'un document nomme. Et un diff champ par champ coûte une commande."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-08T22:03:41.450Z
---

2026-09-08. En posant le dojo de VF5 R sur l'emplacement libre `trm` (VF5 FS),
j'ai recopié **les trois champs que la doc nommait** — objets, collision,
musique — et supposé le reste inerte. L'image est sortie fausse. Les douze
autres champs étaient ceux d'un décor d'ESSAI : `+0xD0` aiguille un rendu,
`+0xD4` indexe un saut sur dix constantes, `+0x2C..+0x34` sont des identifiants
que seuls huit décors portent, `+0xE4/+0xE8` sont l'aire.

**Puis j'ai accusé la mauvaise cause** : les réglages d'éclairage de VF5 R.
Frédéric a tranché en relançant `decor_5r_akira.cmd` — le même décor, les mêmes
fichiers, sur `djo` : correct. Sa capture disculpait les fichiers **avant** que
je ne cherche.

Sa remarque : « comment tu peux faire cette erreur sur TRM quand on a déjà
travaillé dessus et identifié tous les noms des décors ? » Elle porte : `trm`
était identifié depuis le 2026-09-05.

**Why:** connaître le NOM d'un enregistrement ne dit rien de sa FORME. Un
document qui cite trois champs cite ce dont il avait besoin ce jour-là, pas
l'inventaire. Et comparer deux enregistrements champ par champ coûte une
commande — moins cher que n'importe quelle hypothèse.

**How to apply:** avant de recycler un emplacement, **differ son enregistrement
avec celui du modèle**, et cloner tout ce qui n'est pas propre à
l'emplacement. Deux réserves lues dans le code, pas devinées : les pointeurs ne
se recopient que là où une **relocation** les suit (PE rebasé), et un champ
qu'on remet à zéro doit être un champ qu'on sait facultatif. Voir
[[feedback_cartographier_la_zone]], [[reference_vf5_greffe_section]] et
[[feedback_son_observation_prime]]. Document : `analysis/decors.md` §13.
