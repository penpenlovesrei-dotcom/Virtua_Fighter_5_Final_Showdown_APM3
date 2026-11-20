---
name: reference-disques-xbox-illisibles
description: Le lecteur de Frédéric ne voit aucun disque Xbox ni Xbox 360 — la détection XDVDFS est impossible sur ce matériel.
metadata: 
  node_type: memory
  type: reference
  originSessionId: b6a2c382-c062-4077-bc27-75a9d70650ca
  modified: 2026-08-25T17:03:25.330Z
---

Testé le 25 août 2026 sur le lecteur **HL-DT-ST BDDVDRW CH10LS28 (USB)**, avec une sonde d'accès brut (`\\.\D:`, recherche de la signature `MICROSOFT*XBOX*MEDIA` aux bases XGD1, XGD2 et XGD3) :

- CD audio → **reconnu** (l'instrument et le lecteur fonctionnent, le témoin est valide) ;
- disque **Xbox 360** → `MediaLoaded=False`, taille exposée 0 Go, « Le périphérique n'est pas prêt » ;
- disque **Xbox originale** → même résultat.

Le lecteur ne voit donc même pas la partition vidéo, encore moins la partition de jeu XDVDFS. C'est le comportement attendu : les disques Xbox sont pressés avec une structure non standard que la plupart des lecteurs PC signalent comme vierge. Y accéder exige un firmware modifié sur des modèles de lecteurs précis.

**Conséquence pour DiscShelf : pas de support Xbox ni Xbox 360.** Une proposition de détecteurs `XboxDetector` / `Xbox360Detector` avec lecteur XDVDFS maison a été écartée pour cette raison — le code était correct dans son principe (les parseurs XBE et XEX avaient les bons décalages) mais reposait sur une prémisse fausse. Ne pas relancer ce chantier sans changer de lecteur, et même alors le pari reste mauvais.

Trois défauts relevés dans cette proposition, à connaître si le sujet revient un jour : lecture du descripteur au LBA 32 **absolu** (faux pour XGD2/XGD3, dont le volume commence à un offset de partition) ; arrêt du parcours de répertoire au premier `0xFFFF`, qui est le rembourrage de fin de secteur et non la fin des entrées ; `FileStream` tamponné à 4096 octets sur un handle de volume brut.

À noter tout de même : un `default.xbe` porte le **nom du jeu en clair** (certificat +0x0C, 40 caractères UTF-16). Pour la Xbox originale, aucune base Title ID → nom ne serait nécessaire — seule la 360 en aurait besoin. Voir [[reference-release-tag-scheme]] pour le dépôt concerné.
