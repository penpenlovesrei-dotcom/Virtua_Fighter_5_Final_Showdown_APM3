---
name: feedback-son-observation-prime
description: "Quand Frédéric dit avoir vu une chose fonctionner, ma théorie est fausse — pas son observation."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 61cff823-927b-4eea-81b1-5063c9d15cce
  modified: 2026-09-06T12:41:50.806Z
---

Quand Frédéric affirme avoir **vu** quelque chose marcher, c'est un fait acquis.
Si ma mesure ou ma déduction dit le contraire, **c'est moi qui me trompe**, et je
dois repartir de son observation — pas construire une théorie qui l'écarte.

**Why :** le 2026-09-06, j'avais conclu que l'attract de VF5 était impossible à
réparer, preuve à l'appui : CRI Mana répondait « No available decoder is attached
for the video stream », et le binaire ne contenait que des greffons de codec
audio. Raisonnement juste, conclusion fausse. Il a dit « cet attract fonctionne
en mode arcade, et je ne suis pas sûr que ce soit une vidéo ». Il avait raison
sur les deux points : c'est du **temps réel**, et le moteur choisit simplement
entre deux animations (`logo_vf5` en borne, `logo_vf5_short` en console). Quatre
octets ont suffi. J'avais passé une demi-journée sur une piste morte parce que
j'ai préféré ma mesure à ce qu'il voyait à l'écran.

Même travers le même jour : j'ai conclu d'un nom de dossier (`APM3_US`) que tout
le chantier portait sur un autre jeu, et j'ai réécrit le document d'amorçage. Il
a tranché en une phrase.

**How to apply :** dès qu'il décrit un comportement observé, en faire le point de
départ et chercher **pourquoi ma mesure ne le voit pas** — mauvais mode, mauvais
moment, mauvais site. Ne jamais répondre « c'est impossible » à quelque chose
qu'il a vu. Et devant deux explications, préférer celle qui est cohérente avec
son observation, même si elle est moins élégante. Voir aussi
[[feedback_observation_puis_code]] et [[feedback_premisse_qui_borne]].
