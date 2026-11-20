---
name: reference_2i_peint_page_assemblee
description: "Un objet peint se cherche dans la page assemblée, et par BALAYAGE — l'ancre ment."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-04T15:36:35.030Z
---

Dans 2I, un personnage animé est souvent **aussi peint dans le décor**, à l'arrêt : l'objet
est censé le recouvrir. C'est une référence de position qui ne dépend ni de la caméra ni
d'une capture — mais elle se prend avec deux précautions.

**1. Chercher dans la PAGE ASSEMBLÉE (`poser2i.lire_liste`), pas dans la banque du disque
(`couches2i.demi_banque`)** : dans la banque, la figure est éclatée en tuiles et n'apparaît
nulle part d'un seul tenant. Le zéro qu'on y trouve est un artefact. Ce faux zéro a fait
conclure « aucun objet de Ryu / de Yun n'est peint » — faux les deux fois.

**2. Mesurer par BALAYAGE, jamais par l'ancre.** `situer_animes.chercher` s'appuie sur le
pixel le plus rare de l'image : ça n'a de sens que si la figure est peinte à l'identique.
Pour la femme en rose de Yun, l'ancre disait 512 et le balayage 496 — j'ai déplacé l'objet
sur la foi de l'ancre et Frédéric a répondu « c'est pire ». **En dessous de ~90 % d'accord,
la figure peinte n'est pas la nôtre et ne dit rien de sa place.**

`rendu_fiches.py` rend l'objet depuis les **tuiles compilées** : c'est lui qu'il faut
utiliser pour ces mesures, pas les sprites du disque. Voir [[reference_3sx_objets_decor_animes]]
et [[feedback_lire_le_code_pas_l_image]].
