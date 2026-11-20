---
name: reference_case_vide_est_un_canal
description: "Une case de palette jamais écrite se reconnaît à ses canaux (r=b=0, g≠0), pas à la valeur 0x03E0."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-06T11:31:30.994Z
---

Le détecteur de palette fausse teste **les canaux** :

    (v & 0x7C1F) == 0 and (v & 0x03E0) != 0        rouge et bleu nuls, vert non nul

Il testait `== 0x03E0` (g = 248). L'objet `n05o19` de New Generation tombe sur `0x0280`
(g = 160) — vert lui aussi, d'une autre valeur. Le détecteur annonçait donc **zéro vert**
avec 474 pixels verts à l'écran, et la même prémisse masquait **3 207 pixels verts en 2I**
alors qu'on croyait le jeu propre.

**Une prémisse étroite ne donne pas un résultat prudent : elle donne un résultat faux, et
net.** C'est la même leçon que [[feedback_premisse_qui_borne]] — l'écrire pour pouvoir
l'attaquer.

L'index 0 reste exclu (transparent, jamais peint), et le détecteur **élimine, il ne
choisit pas**. Voir [[reference_2i_palettes_deux_jeux]].
