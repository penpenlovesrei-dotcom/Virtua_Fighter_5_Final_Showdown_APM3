---
name: feedback-lire-le-code-pas-l-image
description: "Frédéric refuse qu'on règle à la vue ou qu'on mesure sur une de ses références quand la donnée est dans le binaire."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8d4f5f21-e1e1-4df4-9937-77d366b04e27
  modified: 2026-08-30T22:56:52.135Z
---

Quand Frédéric signale un défaut de placement, **il n'attend pas un réglage à l'œil, ni
une mesure prise sur la capture de référence qu'il vient d'envoyer.** Il l'a dit deux fois
de suite : « pourquoi on doit régler comme ça à la vue alors qu'on a toutes les données ? »
puis « normalement tu n'as rien à mesurer par rapport à ma référence si tu as toutes les
données en main ».

**Why :** sur ce chantier tout se lit — le format, les palettes, l'assemblage, les
cadences, les positions ont tous été percés en désassemblant, et les sessions perdues l'ont
été à empiler des hypothèses sur une image. Une valeur calée sur une capture est calée sur
une position de caméra et un instant ; elle ne se transporte pas. Sa référence sert à
**valider**, pas à **mesurer** — il précise lui-même quand le ratio n'est pas bon.

**How to apply :** devant un défaut de placement, chercher la fonction qui produit la
valeur avant de toucher à un paramètre. Trois fois sur trois dans la session du 29/08/2026
c'était payant : l'ancrage vertical se déduisait du mappage des pages (exact au pixel, là
où une mesure de l'art donnait 80 lignes de trop), l'ordre de dessin était l'ordre de la
liste d'affichage, et la règle plan → objet est écrite en `0x8C0E8C6A`.

Corollaire : **ne pas réclamer un relevé Flycast avant d'avoir vérifié que le binaire ne
répond pas déjà.** Je lui avais annoncé quatre savestates comme nécessaires — elles ne
l'étaient pas. Voir [[reference-2i-plans-profondeur]] et [[feedback-demander-confirmation]].

**La capture Dreamcast par décor, accordée le 31/08/2026 — ORIENTER, PAS MESURER.** Il a
accepté d'en fournir une par décor, à une condition qu'il a posée d'emblée : « uniquement
pour t'orienter et tu cherches ensuite dans le code de 2I ». La capture répond donc à
« qu'est-ce qui existe, et à peu près où », jamais à « quelle valeur ». Elle dit quelle
hypothèse tester ; le binaire fournit le chiffre.

**Why :** ce qui a coûté la session du 30-31/08, ce n'est pas le manque de données, c'est
d'avoir pris une **cohérence interne pour une identification**. La table `0x8C1D54E0` a
une régularité qui tient sur dix-sept étages (la seconde paire = la première rétrécie de
56 px) — ça prouvait le découpage, et j'en ai conclu le rôle : les limites de caméra.
Appliquée, elle rendait le niveau plus étroit que sur Dreamcast. Une capture m'aurait dit
tout de suite que la piste était mauvaise, sans que j'aille y lire un seul nombre.

**How to apply :** demander la capture AVANT de modifier, s'en servir pour choisir quoi
chercher dans le binaire, puis livrer la valeur lue — jamais la valeur vue. Et ne pas
livrer un changement dont je ne sais pas prédire l'effet à l'écran : deux fois de suite le
31/08 j'ai fait valider des modifications invisibles ou fausses. Voir
[[feedback-verifier-le-build]].

**Le sens inverse, sur VF5 le 03/09/2026 : ne pas CONCLURE d'une capture.** Trois fois de
suite dans la même session, j'ai lu un succès sur une image et Frédéric a corrigé :

1. un décor « importé » jugé sur une capture — alors que **le sélecteur de décor est par
   défaut sur Random** : je ne savais même pas lequel s'était chargé ;
2. le 720p déclaré bon parce que l'ATS était bien mis en page — « le mode 720p est zoomé
   sur toutes tes captures » : l'interface est en espace écran et se remet à l'échelle
   seule, la vue 3D restait cadrée pour 1920 ;
3. le menu console déclaré affiché — « c'est un écran de loading ».

**Why :** une capture prouve qu'il s'est passé *quelque chose*, jamais *quoi*. Elle ne
dit pas quelle donnée a été lue, ni d'où elle vient.

**How to apply :** avant de regarder l'écran, se demander quelle mesure trancherait — et
la faire. Dans les trois cas elle existait et était courte : forcer le décor au lieu de
subir Random, comparer le champ de vision et pas l'ATS, chercher les ressources du menu
dans l'inventaire. Le point d'arrêt sur `CreateFileW` a répondu en une passe à une
question que quatre captures avaient laissée ouverte. Voir
[[reference_vf5_par_avant_disque]].
