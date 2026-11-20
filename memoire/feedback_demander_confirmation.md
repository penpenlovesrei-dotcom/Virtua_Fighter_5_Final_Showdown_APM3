---
name: feedback-demander-confirmation
description: "Une observation ou une question de Frédéric ouvre un dialogue : demander confirmation, ne pas enchaîner sur une modification."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: da10af44-fc5f-401d-9b3a-2c0a9d501b3b
  modified: 2026-08-15T10:14:53.499Z
---

**LA REGLE, EN UNE LIGNE : ne rien compiler tant qu'il n'a pas dit de le faire.**
Repondre d'abord. C'est la formulation qu'il a exigee lui-meme le 2026-08-18,
apres que la version longue ci-dessous eut echoue trois fois.

Quand Frédéric rapporte une observation nouvelle, **lui demander confirmation et
précision avant d'en tirer quoi que ce soit**. Ne pas transformer son
observation en explication, ne pas enchaîner sur une mesure ou une
modification dans la foulée.

**Une question est une invitation à discuter, pas un ordre de travail.** S'il
demande « pourquoi ne pas faire X ? », il ouvre un échange sur X — il ne demande
pas que X soit écrit, compilé et livré avant sa phrase suivante. Répondre à la
question, dire ce que ça impliquerait, et **attendre**.

**Pourquoi :** dans la séance du 2026-08-15, j'ai avancé cinq explications
successives d'un même symptôme — le slot de choix aléatoire, le cache du pack
de textures, « aucun effet », le rechargement du compte à rebours, une formule
miroir — dont quatre se sont révélées fausses. À chaque fois je les ai
présentées comme des résultats, et à chaque fois c'est Frédéric qui a dû me
reprendre. La dernière reposait sur **un seul point de données** (`10 − 6 = 4`)
et un « donc ». C'est le travers que le §10 du HANDOFF appelle « raisonner au
lieu de mesurer », et il use la patience autant qu'il fait perdre du temps.

Le même jour, il a proposé un déclencheur par détection du sprite GAME OVER.
J'ai écrit le relevé, compilé et livré dans la même réponse. Sa remarque : cela
**lui coupe la parole**. Il n'avait pas fini de poser le problème, et une
réponse qui arrive sous forme de binaire compilé ferme la discussion au lieu de
l'ouvrir.

**Le cas qui me fait deraper le plus souvent, ajoute le 2026-08-18 :** quand
Frederic signale un defaut dans ce que je viens de livrer, je le traite comme un
ordre de corriger, et j'enchaine correctif + compilation + nouvelle version dans
la meme reponse. **Ce n'est pas un ordre de coder.** C'est un constat, et il
ouvre un echange sur la cause. Le 2026-08-18, cinq allers-retours de suite sur
le menu de l'ecran titre ont ete traites comme ca : a chaque fois j'ai livre une
version avant qu'il ait fini d'expliquer, et trois de ces versions etaient
fausses. Il me l'a redemande a plusieurs reprises dans la meme seance.

**Repondre, dire ce que je crois avoir compris, proposer -- et attendre.** Une
nouvelle version pendant qu'il ecrit lui coupe la parole, exactement comme le
binaire compile du 2026-08-15.

**La variante du 2026-08-20, et elle est pire que les autres : UNE DESCRIPTION
N'EST PAS UNE PLAINTE.** Sur le mode training, Frederic ecrit « sur l'ecran de
selection, le joueur 1 selectionne son personnage puis selectionne son
adversaire ». C'etait la description de ce qui MARCHAIT. Je l'ai lue comme un
defaut a corriger, j'ai defait le Start P2 injecte -- et le CPU a repris la
place du mannequin, cassant la fonctionnalite. Il a fallu deux essais pour
revenir, et la vraie question n'etait ni « qui joue » ni « qui a raison » mais
« qui tient le curseur ».

Avant de DEFAIRE quelque chose qui fonctionne, verifier que la phrase est bien
une plainte. Une phrase sans verbe de jugement -- pas de « trop », pas de « ne
marche pas », pas de « il faudrait » -- est probablement un constat neutre.
Demander « c'est un defaut ou c'est ce qu'il faut ? » coute une ligne ; defaire
a coute deux essais et une regression.

**Comment l'appliquer :**
- une observation rapportée est une **donnée**, pas une conclusion : la
  reformuler pour vérifier que je l'ai comprise, demander ce qui manque
  (à quel moment, dans quelles conditions, qu'est-ce qui a changé exactement),
  et attendre la réponse ;
- une question se répond, elle ne se code pas. Proposer ce que ça donnerait,
  chiffrer si possible, et laisser le prochain tour décider ;
- ne jamais écrire « donc » sur un seul point de données ;
- dire explicitement « hypothèse » quand c'en est une, et ne rien construire
  dessus avant de l'avoir mise à l'épreuve ;
- **ne pas défaire l'état d'une expérience pendant qu'il écrit.** Une
  restauration automatique après N secondes efface justement ce qu'il est en
  train de décrire. Laisser l'état en place et n'y toucher que sur sa demande.

Voisins : [[feedback_ne_pas_suggerer_arret]], [[feedback_verifier_le_build]].
