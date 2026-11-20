---
name: reference-coherence-nest-pas-role
description: "Une table parfaitement reguliere n'est pas une table identifiee : la coherence interne prouve le decoupage, jamais la fonction."
metadata: 
  node_type: memory
  type: reference
  originSessionId: d8d62c33-dc93-4caa-8109-4cbb89f7f7af
  modified: 2026-08-31T21:47:58.051Z
---

**Une cohérence interne prouve qu'on a bien decoupe une table. Elle ne dit RIEN de son
role.** C'est l'erreur qui a coute le plus cher sur ce chantier, et elle s'est repetee trois
fois en une session.

* **`0x8C1D54E0` (2nd Impact)** — douze octets par etage, et sa seconde paire vaut la
  premiere retrecie de **56 pixels de chaque cote, sur les dix-sept etages**. J'en ai conclu
  « ce sont les limites de camera ». Posee sur Ibuki, elle rend le niveau **plus etroit que
  sur Dreamcast**. Les vraies limites sont ailleurs (`0x8C0D9C26`, deux valeurs globales).
* **`0x8C1A2534` (New Generation)** — dix-huit entrees, forme identique a la table des
  scripts, dispatcher jumeau, `memcpy` coherent. Ce n'est pas la table des decors.
* **« le rang d'une routine par adresse donne le numero de decor »** — faux, la table
  `0x8C18A804` dit le contraire.

**Why :** un binaire de jeu est plein de tables regulieres. La regularite vient de la
generation automatique des donnees, pas de la fonction. Se contenter d'une cohérence
interne, c'est confondre « j'ai trouve une structure » et « j'ai trouve CETTE structure ».

**How to apply :** ne conclure le role d'une table qu'avec une mesure **independante** —
l'appelant qui la lit, un raccord avec l'autre jeu, ou une capture Dreamcast. Deux exemples
de ce qui vaut preuve sur ce chantier : les neuf index de palette passes en dur qui tombent
tous sur la bande de meme numero (huit sur huit), et les 383 de course de camera qui tombent
exactement sur le defaut `{0x140, 0x2c0}` de 3rd Strike. Voir
[[feedback-lire-le-code-pas-l-image]].
