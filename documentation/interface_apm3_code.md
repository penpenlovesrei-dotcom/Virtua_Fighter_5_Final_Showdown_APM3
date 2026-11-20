# Le CODE de l'interface APM3 — désassemblage du CIL

Ouvert le 2026-09-09, à la demande de Frédéric : **comprendre le
fonctionnement de l'interface**, puis la **recoder en C++**. Les autres
fonctions de la borne (comptabilité, réseau, carte Aime, micrologiciels) ne
sont pas dans le périmètre.

Complète `analysis/interface_apm3.md`, qui décrit les **données** (images,
sons, messages). Celui-ci décrit le **code**.

---

## 0. Le fait qui change l'outillage

**L'interface n'est pas du x86.** `Apmv3System.exe` est une application
**Unity 2017.3.0f3** : l'exécutable n'est que le lanceur Unity, et toute la
logique est du **C# compilé en CIL**, dans
`Apmv3System_Data/Managed/Assembly-CSharp.dll`. `capstone` n'y voit rien.

D'où **`tools/dotnet.py`**, écrit pour ce chantier : un lecteur de métadonnées
ECMA-335 et un désassembleur CIL, sans dépendance autre que `pefile`.

    py -3 tools/dotnet.py <assembly.dll> --types
    py -3 tools/dotnet.py <assembly.dll> --type <Classe>
    py -3 tools/dotnet.py <assembly.dll> --methode <Classe.Methode>
    py -3 tools/dotnet.py <assembly.dll> --cherche <motif>

Le format, pour qui reprendra : le répertoire de données **14** du PE donne
l'en-tête CLI ; son `+8` donne les métadonnées, signées `BSJB` ; celles-ci
portent des flux nommés — `#~` les tables, `#Strings` les noms, `#US` les
chaînes littérales, `#Blob` les signatures. **Le piège du format** : la taille
d'une ligne de table dépend du nombre de lignes des tables qu'elle référence,
donc il faut compter *toutes* les tables avant de pouvoir en lire *une*.

> **Piège payé sur place** : dans la table `TypeDef`, le **nom précède
> l'espace de noms**. Les avoir intervertis affichait
> « Main / Apm.System.AbaasGs » au lieu de « Apm.System.AbaasGs / Main ».

---

## 1. La carte : 499 types, et seulement deux familles nous concernent

| espace de noms | types | ce que c'est |
|---|---|---|
| `(global)` | 224 | interop, énumérations, classes générées |
| `RenderHeads.Media.AVProVideo` | 40 | le lecteur vidéo (greffon) |
| **`Picker`** | **31** | **le carrousel générique** |
| `Apm.System.Setting.Volatile` | 26 | réglages en RAM |
| **`Apm.System.GameSelect`** | **24** | **l'écran de choix des jeux** |
| `Apm.System.Setting.NonVolatile` | 19 | réglages persistants |
| `Apm.System.Util.Image` | 16 | les *images* d'application (les jeux) |
| `Apm.System.Daemon` | 15 | le pont vers `amdaemon` |
| `Apm.System.SubSystemTest.*` | ~40 | le **menu opérateur** — hors périmètre |
| `Apm.System.Error`, `Warning` | 6 | les écrans d'erreur |

**Le périmètre utile est donc `Apm.System.GameSelect` + `Picker`** : 55 types.
Tout le reste — comptabilité, Aime, ALL.Net, tests d'entrées, mise à jour de
micrologiciel — est écarté.

---

## 2. Un décompilateur, et tout change

`ilspycmd` 11.0 installé le 2026-09-09 (`dotnet tool install -g ilspycmd`,
autorisé par Frédéric). Il rend du **C# lisible** là où mon `dotnet.py` ne
donnait que du CIL. Les deux servent : `dotnet.py` pour cartographier
(499 types en une commande), `ilspycmd` pour lire.

    ilspycmd -t Apm.System.GameSelect.IconListCanvas <Assembly-CSharp.dll>

Sources décompilées : **`analysis/apm3_source/`** — `SceneManager.cs` (437 l.),
`IconListCanvas.cs` (638), `Icon.cs`, `IconCanvas.cs`, `WheelEffect3D.cs`,
`MoviePlayer.cs`, `TitleAnimation.cs`.

> **Correction de ma première lecture.** J'avais pris les six champs de
> `Design` pour une maquette. Ce sont des **`Material`** — l'apparence des
> panneaux, pas leur géométrie. `panelThickness` est le seul nombre.

---

## 3. Le carrousel, en entier

`Apm.System.GameSelect.IconListCanvas`. **Les valeurs par défaut sont dans le
code**, pas seulement dans la scène :

```csharp
accel               = new Vector2(-1f, 0f)   // la deceleration, par trame
rangeOfMovement     = 0.5f                   // en fraction d'icone
iconSize            = 256f
gapSize             = 16f
selectedIconRatio   = 1.5f                   // l'agrandissement du centre
selectedIconShadowZ = -24f
iconShadowZ         = -16f
```

### 3.1 Le placement — une simple règle d'écart

```csharp
private void AlignmentIcon(int selectedIndex, float offset = 0f)
{
    float pas = gapSize + iconSize;              // 272
    for (int i = 0; i < iconsOrder.Count; i++)
        iconsOrder[i].anchoredPosition =
            new Vector2(-pas * (selectedIndex - i) + offset, 0f);
    speed = Vector2.zero;
}
```

Les icônes sont sur **une ligne**, espacées de `iconSize + gapSize` = 272, et
l'icône sélectionnée est à `x = 0`. Il n'y a **pas** de roue 3D dans cet
écran : `WheelEffect3D` appartient à la bibliothèque `Picker`, que le menu
opérateur utilise ailleurs. *Ma supposition du §5 précédent était fausse.*

### 3.2 L'agrandissement — une rampe linéaire, pas une courbe

`IconCanvas`, lignes 116-124 :

```
demi   = Size * MaxRatio / 2                    // 256 * 1.5 / 2 = 192
echelle = |x| >= demi ? 1
                      : (1 - MaxRatio)/demi * |x| + MaxRatio
ombreZ  = MinShadowZ - ( |x| >= demi ? 0
                       : (MaxShadowZ-MinShadowZ)/demi * |x|
                         - (MaxShadowZ-MinShadowZ) )
```

L'icône vaut **×1,5 au centre**, décroît **linéairement** jusqu'à ×1 à 192 px,
et reste à ×1 au-delà. L'ombre suit la même rampe, de `-16` à `-24` en Z.

### 3.3 Le mouvement — balistique, pas interpolé

C'est le point qui donne son ressenti à la borne. `Select(cible)` **résout la
vitesse initiale** pour que l'icône s'arrête pile au centre :

```csharp
float pas = |accel.x|;          // 1
float parcouru = 0f;
while (parcouru < |cible.x|) { parcouru += pas; pas += |accel.x|; }
speed = ±pas;
```

C'est la somme triangulaire : on cherche le plus petit *n* tel que
1+2+…+*n* ≥ distance, et on part à la vitesse *n*. Ensuite, chaque trame :

```csharp
private void IntertialMove()
{
    foreach (icon) icon.anchoredPosition += new Vector2(speed.x, 0f);
    float v = |speed.x| - |accel.x|;
    speed = (v < 0f) ? Vector2.zero : ±v;          // decroit de 1 par trame

    if (|speed.x| >= |conditionSpeed.x|) {
        // encore lance : on borne aux extremites
        if (premiere.x >=  iconSize*rangeOfMovement) { Alignment(0, +128); Select(premiere); }
        if (derniere.x <= -iconSize*rangeOfMovement) { Alignment(n-1, -128); Select(derniere); }
        return;
    }
    if (isInertiaMove) { Select(GetNextSelectIcon()); isInertiaMove = false; }

    // arrivee : le centre a ete franchi, ou la vitesse est nulle
    if (changementDeSigne || (speed == 0 && selectionnee.x != 0)) {
        AlignmentIcon(index);
        IsMoving = false;
    }
}
```

Décélération **constante de 1 pixel par trame par trame**, arrêt exact,
recalage sec à l'arrivée. `rangeOfMovement * iconSize` = **128 px** : c'est la
butée au-delà de laquelle la liste se raccroche à son extrémité.

### 3.4 La profondeur — un tri par distance au centre

```csharp
list.Sort((a, b) => (int)(|b.Position.x| - |a.Position.x|));
// puis DisplayOrderIndex croissant, boutons par-dessus, fond en premier
```

**Les icônes les plus éloignées du centre sont dessinées en premier**, donc
derrière. Avec l'agrandissement et l'ombre, cela suffit à donner le relief :
aucune 3D n'est utilisée.

### 3.5 Les entrées

Une seule voie, tactile à l'origine :

```
OnTouchDown(nom, pos)      OnMove(nom, delta)      OnMoveEnd(nom, vitesse)
OnTap(nom, pos)            OnEnter()
MoveLeft()  MoveRight()  MoveNext()  OnPageButtonTap(isLeft)
```

Le clavier et la manette ne font qu'appeler `MoveLeft` / `MoveRight` /
`OnEnter`. **Un portage n'a donc qu'à alimenter `speed`.**

### 3.6 Par trame

```csharp
private void Update()
{
    leftButton.Show  = !IsMoving && IsEnableLeftButton;
    rightButton.Show = !IsMoving && IsEnableRightButton;
    if (!IsAnimating) { if (speed != zero) IntertialMove(); Sort(); }
    if (CanSelect) { title.Title = centre.Info.Icon.TitleName; title.Show(); }
    else title.Hide();
}
```

Les flèches ne s'affichent **que** à l'arrêt, et le titre n'apparaît que
lorsque la sélection est stable.

### 3.7 Les quatre transitions

`AnimationType { StartGame, CancelStartGame, ShowMovie, EndMovie }`, jouées
par `StartAnimation(type, onEnd, onInvalidCondition)`.

---

## 4. L'apparence : `GameSelect.Design`

Six champs. **Cinq sont des `Material`** — l'apparence des panneaux, pas leur
géométrie :

```
backPanel  hedderPanel  messagePanel  bottomPanel  movieButton   des Material
panelThickness                                                   le seul nombre
```

L'orthographe est celle de SEGA : « hedder ». La disposition, elle, est dans
la scène Unity, pas dans le code. **Cela suffit à savoir de quoi l'écran est
fait** : un fond, un bandeau haut, un bandeau bas, une ligne de message, un
bouton vidéo — mais pas où ils sont.

> Correction : j'avais d'abord lu ces six champs comme une maquette. Ils
> portent des matériaux.

---

## 5. La machine à états : `GameSelect.SceneManager`

Lue en entier. Elle tient en trois choses.

### 5.1 Deux conditions dérivées

```csharp
bool IsAdvertize => advertizeTime <= elapsedTime;
bool IsEnd => isMountEnd && isStartGameEnd
              && !mainCanvas.IsAnimating && !iconListCanvas.IsBusy;
```

### 5.2 Le compteur d'attract

`UpdateElapsedTime()` ajoute `Time.deltaTime` et détecte le **franchissement**
du seuil : `onStartAdvertize` part une seule fois, puis la coroutine
`Advertize` démarre. `ResetElapsedTime()` fait l'inverse — `onEndAdvertize`,
arrêt de la coroutine, compteur à zéro. **Toute entrée appelle
`ResetElapsedTime`.**

### 5.3 La démonstration, six états qui bouclent

```
StartMovie ──> WaitMovieStartAnimation ──> WaitMovie ──>
WaitMovieEndAnimation ──> WaitCanMove ──> WaitMove ──> StartMovie ...
```

À `WaitCanMove` elle appelle `MoveNext()` : **la borne fait défiler ses jeux
toute seule, en jouant la vidéo de chacun**. En attract, le son est coupé si
`EnableAdvertizeSound` est faux. C'est exactement la vitrine que Frédéric
décrit.

### 5.4 Les entrées, quatre points

```csharp
OnLeftLeverOn()   -> iconListCanvas.MoveLeft()
OnRightLeverOn()  -> iconListCanvas.MoveRight()
OnPush01OnNow()   -> si CanSelect : GameStart(...)  sinon : annule la video
OnPush02OnNow()   -> si CanSelect : PlayMovie()     sinon : annule la video
OnPushOtherOnNow(), OnChangeCredit(), Update() (le tactile)
```

**Le motif est constant** : si la sélection n'est pas stable, l'entrée ne fait
qu'**annuler la démonstration en cours**. Et `CancelPlayMovie()` gère la
course : si la fenêtre vidéo n'est pas encore ouverte, il pose un drapeau que
`OnStartMovieAnimationEnd` relira. Un portage doit reprendre ce drapeau, sinon
une touche pressée pendant l'ouverture est perdue.

### 5.5 Le lancement

```csharp
GameStart(subGameId, version, info) {
    isStartingGame = true;
    if (!bootApplication) { isMountEnd = isStartGameEnd = true; }   // mode debug
    else { AppMounter.Mount(id, OnMountEnd); daemonMain.StartGame(id, OnStartGameEnd); }
    iconListCanvas.StartAnimation(StartGame, ...);
    mainCanvas.StartAnimation(HideAllPanel, ...);
}
```

Puis, à chaque trame, quand `IsEnd` devient vrai : `systemSequenceManager.Exit(
NextProcess.Game, launchSubGameId, launchVersion)` — c'est la **sortie de la
scène** qui lance le jeu.

> **`bootApplication` est le cadeau du chantier.** `Start()` le lit dans
> `GeneralSetting.GameSelectDebugSetting` : à faux, l'interface **joue toute
> l'animation de lancement puis revient** (`CancelStartGame` + `ShowNewIcon`)
> sans rien monter ni démarrer. SEGA a laissé dans le code le mode qui sert
> exactement à une vitrine.

Il y a une **seule branche vers le jeu**, une seule vers le test opérateur
(`BeginTest`), une seule vers l'erreur. C'est un port simple.

---

## 6. Le carrousel générique : `Picker`

31 types : `Picker`3 -> MassivePicker`3`, les `ScrollRect`, les `LayoutGroup`,
les `PickerItem` / `ZoomPickerItem`, `EffectBase -> EffectComponent ->
WheelEffect3D, ZoomItemEffect`, plus `ObjectPool`1` / `ListPool`1`.

> **Correction.** J'avais annoncé que les icônes étaient sur une roue 3D.
> **C'est faux pour cet écran** : `IconListCanvas` place ses icônes sur une
> ligne (§3.1) et n'utilise rien de `Picker`. Cette bibliothèque sert
> **ailleurs** — le menu opérateur et ses longues listes, qui recyclent leurs
> éléments par `ObjectPool`. **Hors périmètre.**

---

## 7. Ce qui reste à mesurer

Une seule chose, et elle est facultative : **les valeurs sérialisées de la
scène** (`Apmv3System_Data/level1`, `level2`). Les champs `[SerializeField]`
d'une instance y écrasent les valeurs par défaut du code. Un build de sortie
n'a pas de *type tree*, mais les champs d'un `MonoBehaviour` sont écrits
**dans l'ordre de déclaration**, que les métadonnées donnent.

Mais **le code porte déjà des valeurs par défaut cohérentes** (§3), et
`advertizeTime` vient d'un réglage, pas de la scène. On peut écrire le portage
sans cette mesure, et l'affiner ensuite si le ressenti ne colle pas.

**Le désassemblage de l'interface est donc terminé.** Périmètre couvert :
`SceneManager`, `IconListCanvas`, `IconCanvas`, `Icon`, `MoviePlayer`,
`TitleAnimation`, `Design`. Écartés en connaissance de cause : `Picker`,
`SubSystemTest`, `Daemon`, `AbaasGs`, `Setting`.

---

## 8. Le portage C++ : la spécification

**Les données** — un dossier par jeu, là où l'original interroge le démon :

```
identifiant, titre, version, jaquette, video, executable + arguments,
disponible ou non
```

**Le rendu** — l'écran est **plat**. Il faut : un quadrilatère texturé avec
échelle et translation, un tri par profondeur, de la vidéo, du son. Ni 3D, ni
canvas Unity. `Direct3D 11` + `Media Foundation` + `XAudio2` couvrent tout
sans une seule bibliothèque à installer.

**La boucle** — à 60 Hz, dans cet ordre, celui de l'original :

```
1. entrees             -> MoveLeft / MoveRight / Enter, et ResetElapsedTime
2. si vitesse != 0     -> IntertialMove()          (§3.3)
3. tri par |x|         -> Sort()                   (§3.4)
4. echelle et ombre    -> par icone                (§3.2)
5. elapsedTime         -> franchissement de advertizeTime -> attract (§5.3)
6. dessin
```

**Les constantes**, telles quelles :

| | |
|---|---|
| taille d'icône | 256 |
| écart | 16 |
| pas | 272 |
| agrandissement du centre | ×1,5 |
| rampe d'agrandissement | 192 px |
| décélération | 1 px/trame² |
| butée d'extrémité | 128 px |
| ombre Z | −16 à −24 |

**À ne pas reprendre** : `amdaemon`, ALL.Net, la carte Aime, la comptabilité,
les tests de sous-systèmes, les micrologiciels, `Picker`.

**La base de rendu est tranchée : Win32 + Direct3D 11 + Media Foundation +
XAudio2.** Mesuré le 2026-09-09, pas supposé : le MinGW-w64 de son MSYS2
(g++ 16.1) porte déjà `d3d11.h`, `mfapi.h` et `xaudio2.h`, et un programme
d'essai qui inclut les trois **compile et se lie**. Donc :

* rien à installer, `cl.exe` absent de son Visual Studio ne bloque rien ;
* **aucune DLL à livrer** — tout vient de Windows ;
* SDL2 (2.32) et ffmpeg (libavcodec 62) sont là aussi, mais ils imposeraient
  des DLL à côté de l'exécutable pour une écran plat qui n'en a pas besoin.

    g++ -std=c++17 ... -ld3d11 -ldxgi -lmfplat -lmf -lmfreadwrite -lmfuuid -lole32

---

## 9. Les jeux : où ils vont, et sous quel format

`borne\jeux\<un dossier par jeu>\` — voir `borne\LISEZ-MOI.txt`.

| fichier | format | pourquoi ce chiffre |
|---|---|---|
| `jaquette.png` | carrée, 512×512 (384 mini) | `iconSize` 256 × `selectedIconRatio` 1,5 = 384 px à l'écran |
| `demo.mp4` | H.264 + AAC, 16:9, 1280×720 | Media Foundation le lit sans codec ; le HEVC est payant sur Windows 11 |
| `jeu.json` | facultatif | titre, `exe`, `args`, éditeur, année |

Deux outils, écrits et **essayés de bout en bout** sur une jaquette 300×420
en JPEG et une vidéo VP9 en WebM :

* `tools\jeux_verifier.cmd` — dit ce qui va et ce qui ne va pas. Ne touche à rien.
* `tools\jeux_convertir.cmd` — remet au format par ffmpeg, en gardant les
  originaux sous `_source_*`.

Le dossier est **indépendant du programme** : Frédéric peut le remplir dès
maintenant, le portage viendra le lire tel quel.
