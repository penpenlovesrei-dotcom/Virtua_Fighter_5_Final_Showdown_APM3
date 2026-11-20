---
name: project-tex3d-hd
description: Pack de textures HD pour le moteur 3D de Supermodel — le doc qui fait foi est SupermodelSrc/Docs/Tex3DHD.md.
metadata: 
  node_type: memory
  type: project
  originSessionId: da10af44-fc5f-401d-9b3a-2c0a9d501b3b
  modified: 2026-08-15T03:45:21.812Z
---

Quatrième chantier du projet Model 3, ouvert le 2026-08-15 : un override
d'assets pour les **textures du Real3D**, pendant du pack de tuiles de
[[project_tuiles_hd]]. C'est ce qu'exigeait le vrai HD des portraits, qui ne
passent pas par le plan de tuiles. **Le document qui fait foi est
`SEGA Model 3\SupermodelSrc\Docs\Tex3DHD.md`** ; l'aiguillage est dans
[[reference_docs_projet_fv2]].

Le fait qui commande l'architecture : **il n'y a pas une texture GL par texture
du jeu**. Supermodel téléverse la texture RAM brute dans une seule texture
`R16UI`, et c'est le shader qui décode. Le HD passe donc forcément par une
modification du shader — il n'existe aucun point d'interception d'une texture
décodée.

Deux pièges déjà payés, à ne pas refaire :
- **`WriteSurfaceToBMP` rend vrai en cas d'ÉCHEC** (convention Supermodel),
  alors que `ReadImageRGBA` rend vrai en cas de succès. Un test inversé faisait
  passer 330 écritures réussies pour des erreurs.
- **Ne jamais mettre une texture unie dans un pack** : son hachage est celui de
  toute texture unie de même taille, on remplacerait n'importe quoi ailleurs à
  l'écran.

État au 2026-08-15 : chargement, appariement par hachage et pose dans l'atlas
vérifiés — 22 portraits de 512x512 posés, 0 rejeté. Générateur :
`py fv2mod\portraits_hd.py --pack 512`. Lanceur `FV2 - Portraits HD.cmd`.
Le pack **exclut** le patch VROM de `portraits.py runtime`, qui modifierait les
textures que le pack reconnaît à leur contenu d'origine.
