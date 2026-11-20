---
name: project-dbz3-msu1
description: "Patch MSU-1 pour DBZ Super Butouden 3 (SNES) — fonctionne, confirmé à l'oreille dans Snes9x 1.63."
metadata: 
  node_type: memory
  type: project
  originSessionId: d10f67b3-d2e8-4876-a8c5-aec896d7c12e
  modified: 2026-08-03T17:55:22.280Z
---

Projet démarré le 2026-08-03 : patchs MSU-1 (musiques qualité CD) pour
`Dragon Ball Z - Super Butouden 3 (J) [!]` **et** `Super Butouden 2 (J) (V1.1)`.
Les deux fonctionnent. Chacun a son dossier `msu1-project/` avec son README.

**Ne jamais supposer qu'un jeu de la même série partage son driver** : BT2 et
BT3 n'ont que 2 % d'octets communs dans la zone du driver sonore. BT2 a été
recartographié de zéro, et cette approche a permis de le réussir du premier
coup là où BT3 avait demandé sept allers-retours.

Tout est dans
`C:\Users\frede\Documents\Super Famicom\Roms\Dragon Ball Z - Super Butouden 3 (J) [!]\msu1-project\`
— voir son `README.md` pour les détails techniques (point d'accroche, table
des IDs, carte du driver sonore). Ne pas les redocumenter ici.

Ce qui n'est pas dans le repo et qu'il faut savoir :

- **Butouden 3 est PUBLIE** (2026-08-03) :
  <https://github.com/penpenlovesrei-dotcom/DBZ3-MSU1-patch>, release v1.0.
  Sources du paquet dans `C:\Users\frede\Documents\Super Famicom\MSU1-patches\`
  (qui est le dépôt git). `ZELDIX-POST.txt` contient le message forum en BBCode,
  prêt à poster mais **pas encore publié sur Zeldix**.
- **Butouden 2 n'est PAS publié** — l'utilisateur l'a explicitement retiré du
  paquet : pas testé avec de vraies musiques, et sa limite connue le rend
  prématuré. Ne pas le rajouter sans son accord.
- Rien de copyrighté dans la distribution : ni ROM ni audio, uniquement le
  patch IPS, la doc et les scripts.
- **Toujours vérifier un patch IPS avec un applicateur écrit séparément** du
  générateur : un bug symétrique entre écriture et lecture serait invisible
  autrement. `tools/apply_ips.py` sert à ça.
- Piège résolu en fin de parcours : faire *sélectionner* et *lancer* la piste
  au même endroit provoquait un redémarrage audible quand le jeu repassait par
  la routine. Séparer les deux (sélection en `$ADE6`, lecture à la commande
  `$01`) et ne pas relancer si `AUDIO_PLAYING` est déjà levé règle ça sans
  avoir à réserver un octet de RAM dans le jeu.
- Il reste à confirmer si le jeu numérote ses morceaux à partir de 0 ou de 1,
  et quel numéro correspond à quel écran. À faire quand l'utilisateur aura
  10 morceaux **distincts** (il n'avait que le même mp3 copié 10 fois).
- **Piège de méthode qui a coûté très cher ici** : j'ai supposé que tout le son
  passait par un seul port et j'ai construit trois hypothèses successives
  dessus, chacune validée par un test utilisateur. Le driver utilisait deux
  ports, et le numéro du morceau n'était sur aucun des deux — il fallait
  remonter à la routine qui téléverse les données du morceau. **Leçon** : avant
  de bâtir sur une hypothèse d'architecture, vérifier qu'elle est complète —
  chercher tous les points d'écriture vers le matériel, pas seulement le
  premier trouvé.
- **Second piège, plus subtil** : j'avais une table qui repliait *toute* valeur
  sur un domaine valide (modulo N). Le patch semblait fonctionner alors que je
  lisais le mauvais octet — la table masquait l'erreur. Elle n'est apparue
  qu'en passant à des pistes distinctes. **Pour valider une hypothèse, utiliser
  une table qui ÉCHOUE si l'hypothèse est fausse**, pas une qui rattrape tout.
- Normalisation audio : `wav2msu.py` mesure la sonie ITU-R BS.1770 (pondération
  K + double gating), pas la crête. Pour doser musique vs bruitages, ne pas
  toucher aux fichiers — utiliser le registre de volume MSU-1 (`--volume`),
  car les bruitages viennent du SPC et ignorent le gain des `.pcm`.
- **Leçon de méthode** : j'ai tenté de détecter la piste MSU-1 active en
  testant le verrou des fichiers `.pcm` (ouverture exclusive). **Peu fiable** —
  Windows Defender scanne les fichiers et produit des faux positifs. Pire, le
  sondage lui-même ouvre les fichiers en exclusif et peut perturber la lecture
  de Snes9x. Ne pas réutiliser cette technique ; demander à l'utilisateur ce
  qu'il entend est plus rapide et plus sûr.
- **Autre leçon** : j'ai tué et relancé Snes9x plusieurs fois pendant que
  l'utilisateur testait, en détruisant sa session et sans lui laisser le temps
  de rapporter ce qu'il entendait. Quand il teste, ne pas toucher à
  l'émulateur — demander d'abord.
- Cible : **Snes9x**, ROM japonaise brute (pas la traduction anglaise).
- `ffmpeg` n'est pas installé sur cette machine — `wav2msu.py` ne gère donc
  que le `.wav` pour l'instant. `winget install Gyan.FFmpeg` pour le reste.
- Aucun patch MSU-1 n'existe pour aucun jeu Dragon Ball SNES (vérifié sur la
  liste Zeldix et romhacking.net) — c'est du travail original, pas un portage.

Voir aussi [[reference-snes-msu1-format]].
