---
name: feedback-chercher-avant-de-retroconcevoir
description: "Avant de retro-concevoir un format, chercher si une implementation publique existe deja -- souvent l'outil est deja dans le projet."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7b8919f9-a3c9-4e11-a256-ad9c22b4c7e9
  modified: 2026-09-04T12:01:19.145Z
---

Avant de reconstruire un format de fichier a la main, **chercher sur le web s'il est deja documente ou implemente**. Et regarder d'abord les outils tiers deja presents dans le projet : leur auteur publie souvent le code.

**Why:** le 2026-09-04, sur VF5, j'ai passe une heure a retro-concevoir la compression `SLLZ` des archives PAR — 32 variantes balayees, une reconstruction du codage a partir d'une sortie connue, deux fausses pistes. Frederic a demande : « tu as regarde sur internet si un decompresseur SLLZ n'existe pas deja ? ». Il existait : `ParLibrary/Sllz/Decompressor.cs` de **ParManager** (Kaplas80, MIT). Et `ParTool.exe`, qui est la partie visible de ce meme projet, etait dans `tools/` depuis le debut du chantier. Le code de reference donnait en trente lignes les deux details que je n'avais pas devines (bits de poids fort d'abord ; le drapeau se decale AVANT la lecture des octets de l'element).

**How to apply:** des qu'un format resiste a deux essais raisonnes, s'arreter et chercher — le nom du format, plus « source », « decompressor », « format ». Regarder aussi qui a ecrit les outils tiers deja utilises. Le travail de retro-ingenierie garde toute sa valeur pour ce qui est **specifique au jeu** ([[reference_vf5_pxd_pierre_de_rosette]] : YAMP a donne le `vf5fs_game_config_t`) ; il n'en a aucune pour un format d'archive partage par toute une serie.
