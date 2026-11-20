---
name: reference_vf5_resolution
description: "VF5 APM3 — la résolution se change par quatre immédiats dans DEUX binaires ; forcer à l'exécution rend le jeu injouable."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 22b68e08-364a-4b50-b67a-c1f1efec0229
  modified: 2026-09-03T07:51:32.915Z
---

La résolution de rendu de VF5 FS (APM3) se change **statiquement**, par quatre
immédiats — et il faut **les deux binaires** :

| binaire | adresse de l'immédiat | instruction |
|---|---|---|
| `vfes.exe` | `0x140002FD6` | `mov [rbp-0x50], 0x780` (1920) |
| `vfes.exe` | `0x140002FDD` | `mov [rbp-0x4c], 0x438` (1080) |
| moteur | `0x1800E74A6` | `mov [rsi+0xa4], 0x780` |
| moteur | `0x1800E74B0` | `mov [rsi+0xa8], 0x438` |

Outil : `tools/patch_resolution.py`, lanceur `lancer_resolution.cmd`.
**1280×720 vérifié à l'écran** (« plus de zoom et fluide », 2026-09-03).

**Corriger `vfes.exe` seul ne suffit pas** : la fenêtre, la chaîne d'échange et
la vue suivent, mais le moteur continue à créer ses cibles de rendu **et sa
propre vue** en 1920×1080.

**Ne jamais forcer à l'exécution.** `RSSetViewports` est appelée à chaque passe
de chaque trame ; s'y arrêter fait des centaines d'événements de débogage par
image, et le jeu devient injouable — écran noir et lenteur. C'est ce qui a coûté
plusieurs allers-retours avant de passer au patch statique.

Au passage, mesuré par point d'arrêt sur `CreateTexture2D` : **le jeu applique
un anticrénelage 8×** sur ses cibles internes, alors que la chaîne d'échange
annonce un seul échantillon.

Indices de vtable utiles : `ID3D11Device::CreateTexture2D` = **5**,
`ID3D11DeviceContext::RSSetViewports` = **44**. Arguments de
`D3D11CreateDeviceAndSwapChain` à l'entrée : `pSwapChainDesc` `[rsp+0x40]`,
`ppSwapChain` `+0x48`, `ppDevice` `+0x50`, `ppImmediateContext` `+0x60`.

Détail complet dans `analysis/resolution.md`. Voir aussi
[[feedback_soumettre_les_images]] : sur ce chantier, les captures se soumettent,
elles ne se jugent pas.
