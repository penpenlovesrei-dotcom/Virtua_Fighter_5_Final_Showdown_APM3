---
name: reference-ecran-250-pourcent
description: "L'ecran de cette machine est a 250 % d'echelle : GetWindowRect rend du logique, les captures d'ecran du physique."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6a3a967f-1144-49b5-9b3c-9300693489a1
  modified: 2026-08-22T17:45:28.683Z
---

L'affichage de cette machine est mis a l'echelle **250 %**, et le bureau fait **2304 x 1296 pixels physiques**. Deux consequences qui ont deja cause une mauvaise mesure :

- **`GetWindowRect` depuis un processus non DPI-aware rend des coordonnees LOGIQUES.** Une fenetre annoncee `40,60 578x457` occupe en realite `100,150 1445x1143` physiques. Multiplier par **2,5**, pas par 1,5.
- **`Graphics.CopyFromScreen` travaille en pixels PHYSIQUES**, et seulement si le processus a appele `SetProcessDPIAware()` au prealable — sinon Windows virtualise et l'image est floue ou tronquee.

Symptome typique quand on se trompe : la capture semble **zoomee** et ne montre que le coin superieur gauche de la fenetre. C'est ce qui a fait croire, le 2026-08-22, qu'un pack de tuiles ne s'appliquait pas alors que la zone modifiee etait simplement hors du cadre — voir [[project_vf3_model3]].

Recette qui marche, en PowerShell :

```
Add-Type -TypeDefinition 'using System.Runtime.InteropServices; public class D { [DllImport("user32.dll")] public static extern bool SetProcessDPIAware(); }'
[void][D]::SetProcessDPIAware()
$g.CopyFromScreen(100, 150, 0, 0, (New-Object System.Drawing.Size 1450, 1150))
```

Le plus sur reste de **capturer tout le bureau** (2304 x 1296) et de recadrer ensuite : aucune conversion a se tromper.
