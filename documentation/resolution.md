# Choisir la resolution de rendu

Chantier n° 1 du programme du 2026-09-03. **Fait.** 1280x720 verifie a l'ecran
par Frederic : « c'est bon, plus de zoom et fluide ».

Le correctif tient en **quatre valeurs** dans deux binaires, sans debogueur.

---

## 1. Le correctif

`tools/patch_resolution.py`, lanceur `lancer_resolution.cmd`.

| binaire | adresse | instruction d'origine |
|---|---|---|
| `vfes.exe` | `0x140002FD6` | `mov dword ptr [rbp-0x50], 0x780`  (1920) |
| `vfes.exe` | `0x140002FDD` | `mov dword ptr [rbp-0x4c], 0x438`  (1080) |
| moteur | `0x1800E74A6` | `mov dword ptr [rsi+0xa4], 0x780`  (1920) |
| moteur | `0x1800E74B0` | `mov dword ptr [rsi+0xa8], 0x438`  (1080) |

Dans `vfes.exe` c'est un bloc d'initialisation de la configuration d'affichage :
`[rbp-0x48] = 0x3c` (60 Hz) est juste au-dessus des deux dimensions.

**Il faut les deux binaires.** Corriger `vfes.exe` seul fait suivre la fenetre,
la chaine d'echange et la vue -- mais le moteur continue a creer ses cibles de
rendu et sa propre vue en 1920x1080.

Les originaux sont conserves en `.origine` ; `--rendre` les remet.

---

## 2. Comment on y est arrive, et les impasses

### La fausse table de modes

J'avais annonce une table de modes d'affichage en `.rdata` vers `0x1803FEB80`,
parce qu'on y lit a la suite 1024x768, 1280x720, 1920x1080, 2560x1440 et
3840x2160 au pas regulier de 28 octets. **C'est un pool de constantes
flottantes** : les references a cette zone sont des `vmulss` et des `vsubss`.
Une suite reguliere n'est pas une table.

### Trois couches, decouvertes une par une

| ce qu'on forcait | resultat |
|---|---|
| la chaine d'echange seule | image rognee : l'ATS coupe a droite |
| + la fenetre | ATS correct, **vue 3D zoomee** |
| + trois globaux (`vfes.exe+0x1E43A8`, moteur `+0x6490DC`, `+0x649104`) | toujours zoomee |
| + chaque cible de rendu a sa creation | toujours zoomee |
| **+ la vue posee par `vfes.exe+0x3DA0F`** | **plus de zoom** |

La vue etait la cause : `RSSetViewports` recevait toujours 1920x1080 alors que
toutes les cibles etaient en 720p, donc le dessin se faisait 1,5 fois trop grand
et l'on n'en voyait que le coin.

### Pourquoi le forcage a l'execution ne pouvait pas marcher

`RSSetViewports` est appelee **a chaque passe de chaque trame**. S'y arreter,
c'est des centaines d'evenements de debogage par image : le jeu devenait
inutilisable, ecran noir et lenteur. C'est ce qui a impose le patch statique --
lequel a rendu tous les forcages inutiles d'un coup, puisqu'ils descendent tous
de la meme paire de valeurs.

---

## 3. Ce que l'instrumentation a appris au passage

Le point d'arret sur `ID3D11Device::CreateTexture2D` (indice 5 de la vtable)
donne la chaine de rendu complete. En 1920x1080 d'origine :

```
1920x1080  profondeur D24S8        par vfes.exe+0x34EC4
1920x1080  rendu, format 90        par moteur+0x26EEBD
1920x1080  profondeur, ech 8       par moteur+0x26F4AA
1920x1080  rendu, ech 8            par moteur+0x26EEBD
640x360 -> 320x180 -> 160x90 -> 80x45 -> 40x23   (chaine de flou)
1024x1024, 512x512, 256x256 ...                  (ombres, reflets)
```

**Le jeu applique un anticrenelage 8x** sur ses cibles internes, alors que la
chaine d'echange annonce un seul echantillon. Invisible autrement.

Chaine d'echange d'origine : 1920x1080, 60 Hz, `B8G8R8A8_UNORM`, 1 echantillon,
3 tampons, en fenetre.

Les vtables utilisees : `ID3D11Device::CreateTexture2D` = indice 5,
`ID3D11DeviceContext::RSSetViewports` = indice 44. Et les arguments de
`D3D11CreateDeviceAndSwapChain` a l'entree : `pSwapChainDesc` en `[rsp+0x40]`,
`ppSwapChain` `+0x48`, `ppDevice` `+0x50`, `ppImmediateContext` `+0x60` -- je me
suis trompe deux fois sur ce decompte, chaque erreur coutant une passe blanche.

---

## 4. Ce qui reste ouvert

- **Seul le 720p est verifie.** Les autres modes du lanceur sont proposes mais
  non essayes : rien ne garantit que l'interface, dessinee pour du 16:9, suive
  en 4:3 ou en 21:9, ni que le moteur accepte de monter en definition -- les
  cibles intermediaires (1024x1024, 512x512) restent fixes, elles.
- **L'anticrenelage** est deja a 8x sur les cibles internes. Le monter serait le
  gain d'image suivant.

---

## 5. Regle de travail sur ce chantier

**Les captures sont soumises, pas jugees.** Posee par Frederic apres trois
verdicts visuels errones de ma part sur ce seul chantier.

Ce qui se dit : le reglage applique, et ce qui est **mesure**. Ce qui ne se dit
pas : « ca marche », « le cadrage est bon ».

La raison est concrete : sur un jeu de combat le cadrage change a chaque
instant, et deux captures prises au meme temps dans deux executions ne sont pas
comparables -- mesure faite, **correlation 0,05** entre deux passes du meme
scenario. L'oeil ne peut pas trancher a partir de la ; l'instrument, si.
`CreateTexture2D` puis `RSSetViewports` ont repondu en deux passes a ce que six
captures avaient laisse ouvert.
