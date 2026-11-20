---
name: feedback-visuel-avant-validation
description: "Le mode d'inspection dans le port a ete construit puis REJETE : il ne faisait que refaire ce que Frederic fait en jouant."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d8d62c33-dc93-4caa-8109-4cbb89f7f7af
  modified: 2026-08-30T23:13:41.878Z
---

**Ne pas reproposer un « mode d'inspection » dans le port.** Il a ete construit le
31/08/2026 — forcage d'etage par `SF3_INSPECTION`, capture du canevas en BMP, greffe sur
la demo d'attraction pour qu'il tourne sans piloter les menus — puis retire entierement le
jour meme, a sa demande : « on arrete je vois pas l'interet de cet outil, les couleurs sont
fausses, c'est exactement la meme chose que quand je teste par moi meme ».

Il avait pourtant dit « OK » quelques messages plus tot, avec une condition : « je veux un
visuel avant que tu valides quoi que ce soit ». C'est cette condition qui reste vraie ; pas
l'outil.

**Why :** l'outil ne lui epargnait rien. Il devait toujours accepter une compilation et
lancer le jeu ; la seule chose gagnee etait que JE pouvais regarder les images — ce qui
n'est pas ce qu'il voulait, puisque c'est lui qui tranche. Et il a produit 386 Mo de BMP
sur son disque, avec le rouge et le bleu inverses dans mon ecriture du BMP. Un outil qui
double le travail existant en le rendant faux ne se defend pas.

**How to apply :**

* **La regle qui survit :** avant d'annoncer qu'une chose marche, montrer une image et
  laisser Frederic trancher. Ne jamais ecrire « c'est bon » sur mes seules verifications —
  relire les tuiles depuis le C compile prouve que la donnee est bien posee, pas qu'elle
  est a la bonne place. Voir [[feedback-montrer-les-captures]].
* **Ce qu'il accepte pour m'orienter**, et qui suffit : une capture Dreamcast par decor,
  cf. [[feedback-lire-le-code-pas-l-image]]. Elle dit ou chercher ; le binaire donne la
  valeur.
* **Attention a l'echange rouge/bleu**, qui m'a eu deux fois : les `.tex` du port et le
  canevas OpenGL ne rangent pas les composantes comme je le suppose. Un ciel cyan qui sort
  jaune, c'est ca et rien d'autre.
