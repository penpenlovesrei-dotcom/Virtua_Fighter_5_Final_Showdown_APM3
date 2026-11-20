---
name: feedback_controle_qui_ment
description: Un contrôle qui porte une constante en dur ment dès que le build change — pire que pas de contrôle.
metadata:
  type: feedback
---

Un outil de vérification qui garde une constante **en dur** finit par annoncer
des fautes qui n'existent pas, et il le fait au pire moment : quand on cherche
une vraie panne.

Le cas du 2026-09-10 (VF5) : `verifier_decors_table.py` prenait le nombre de
décors à 41, en dur. Sur un build à 61, il cherchait la table des codes à
`+0x2670` au lieu de `+0x3930`, lisait une entrée de descripteur comme si
c'étaient des codes, et rendait **onze fautes** dont vingt relocations
« manquantes ». J'étais en train de chercher la cause de plantages : ce faux
positif m'a fait perdre du temps sur une piste inventée.

**Why:** un contrôle sert à trancher. S'il peut se tromper sans le dire, il ne
tranche plus rien, et il oriente vers une fausse cause.

**How to apply:** un contrôle **lit** ce qu'il vérifie dans l'artefact — ici le
`lea` du binaire patché donne l'adresse de la table, donc le compte. Quand il
retombe sur une valeur par défaut, il le **dit**. Et quand un contrôle annonce
une faute, vérifier d'abord qu'il parle bien du build qu'on lui donne. Voir
[[feedback_premisse_qui_borne]], [[feedback_cartographier_la_zone]].
