---
name: reference_apm3_code_interface
description: "L'interface APM3 est du C# Unity, lue avec ilspycmd ; le carrousel est plat et balistique, pas une roue 3D."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-09T17:58:23.244Z
---

`Apmv3System.exe` est un lanceur Unity 2017.3 : toute l'interface est du C#
dans `Apmv3System_Data/Managed/Assembly-CSharp.dll`. `capstone` n'y voit rien.

**Deux outils, deux usages** : `tools/dotnet.py` (écrit ici) cartographie les
499 types en une commande ; **`ilspycmd`** (installé le 2026-09-09,
`dotnet tool install -g ilspycmd`, dans `~/.dotnet/tools`) rend du C# lisible.

    ilspycmd -t Apm.System.GameSelect.IconListCanvas <Assembly-CSharp.dll>

Sources dans `analysis/apm3_source/`, analyse dans
`analysis/interface_apm3_code.md`. Le désassemblage est **terminé**.

**Trois erreurs que j'ai faites en lisant les noms au lieu du code** :

1. `Design` porte des **`Material`**, pas une maquette.
2. `WheelEffect3D` n'est **pas** utilisé par cet écran : il appartient à
   `Picker`, la bibliothèque du menu opérateur. Le carrousel est **plat**,
   icônes sur une ligne espacées de 272 px.
3. Le défilement n'est pas interpolé mais **balistique** : `Select()` résout
   la vitesse initiale par somme triangulaire, puis on décélère de 1 px par
   trame par trame jusqu'à l'arrêt exact au centre.

**Le cadeau du code** : `bootApplication` à faux joue toute l'animation de
lancement puis revient sans rien démarrer. SEGA a laissé le mode qui sert
exactement à une vitrine.

**Why:** Frédéric a rejeté la vitrine HTML et demande un portage C++ ; toute
supposition sur le ressenti serait un tâtonnement, or il exige qu'on
désassemble. Voir [[feedback_lire_le_code_pas_l_image]] et
[[feedback_analogie_nest_pas_lecture]].

**How to apply:** avant d'écrire une ligne de C++, relire le §8 de
`interface_apm3_code.md` : il porte la boucle dans l'ordre de l'original et
les huit constantes. Ne rien inventer qui n'y soit pas.
Voir [[reference_apm3_interface]] pour les **données** (images, sons).
