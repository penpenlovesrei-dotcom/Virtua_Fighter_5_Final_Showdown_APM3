---
name: project_borne_apm3
description: "La borne APM3 en C++ : VF5RE\\borne\\bin\\borne.exe du 2026-09-09 23:57 est la dernière ; coupée sur « transition vidéo + freeplay » ; paquet de reprise dans SEPTEMBRE."
metadata: 
  node_type: memory
  type: project
  originSessionId: fffdc182-c185-4b4a-9a7c-3e50d7803285
  modified: 2026-09-11T21:40:43.429Z
---

Portage C++ (Win32 + D3D11 + Media Foundation + XAudio2, g++ MSYS2, exe
statique) de l'écran de choix des jeux de l'APM3. Projet :
`C:\Users\frede\Desktop\VF5RE\borne\` ; `borne.cmd` lance, `construire.cmd`
recompile (écrit le 2026-09-11 : `borne.cmd` y renvoyait mais il manquait).

**La dernière version** est `bin\borne.exe` du **2026-09-09 23:57**
(1 119 809 octets, sha256 `71C9737D…`). Aucune autre source C++ sur la
machine. La conversation (session `3f8eb787`) s'est **coupée sur la limite
hebdomadaire** à 23:59, juste après la demande « effet de transition au
lancement de la vidéo, freeplay » : rien de cela n'est codé.

Frédéric a « perdu la fenêtre » : la retrouver par
`search_session_transcripts` ne marche pas bien, le fichier est
`3f8eb787-b241-465e-a563-2b3ce8d7c55e.jsonl` dans le dossier de projet.

**Paquet de reprise pour un autre PC** (2026-09-11) :
`C:\Users\frede\Desktop\SEPTEMBRE\VF5 borne APM3\` — `LIRE-MOI.txt`,
`REMETTRE EN PLACE.cmd` (copie sans rien écraser, testé), `PROMPT_REPRISE.md`
(porte ce qui avait été lu : `ShowMovie` → `ZoomInForMovie`/`MoveLeft`/
`MoveRight`, courbes dans les clips Animator, pas dans le code ; `Credit`
et les chaînes `CREDIT(S)` / `FREE PLAY` de `level1`).

**Reprise sur le PC OneDrive (2026-09-13)** — le chantier tourne depuis
`OneDrive\Bureau\SEPTEMBRE\VF5 borne APM3\`, sans copie sur le Bureau.
Les sept `tools\apm_*.py` calculent désormais `VF5 FS DECOMP` depuis leur
propre emplacement (plus de `Desktop` en dur). MSYS2 installé dans
`C:\msys64` (installeur 20260611, SHA-256 vérifié), `-Syuu` puis `-Suu`,
puis `mingw-w64-x86_64-gcc` 16.2.0. Essai de compilation avec les options de
`construire.cmd`, sorti dans `%TEMP%` : code 0, sans avertissement, 863 748
octets. L'exe validé fait 1 119 809 octets ; `objdump -h` montre que l'écart
vient de ses sections `.debug_*`, absentes de l'essai (`.text` 0x3f780 contre
0x3e9e0). Ni pefile, ni fsb5, ni ilspycmd sur ce PC.
**`construire.cmd` écrase `bin\borne.exe`** : garder une copie de l'exe du
09/09 avant la première recompilation.

**Clips lus (2026-09-13)** : `tools/apm_clips.py` (31 clips de
`sharedassets1.assets`, fin d'objet exacte) et `tools/apm_scene.py` (scène
`level1`). Résultats dans `interface_apm3_code.md` §10 : `ZoomInForMovie`
noircit la jaquette puis l'agrandit en (6,2 ; 3,3) ; le bouton de lecture rose
est en (720, −380) depuis le centre, sur le bord du bandeau bas, pas sur la
jaquette ; bandeaux #00B0FF / #B5E6FD. Écarts avec la borne validée **signalés,
pas corrigés**.

**Pause du 2026-09-13 (demandée par Frédéric).** Il avait dit « décode d'abord
les transitions, et corrige les écarts ». Fait : `tools/apm_controleurs.py`
(5 contrôleurs, fin exacte ; aucun fondu, attentes de 1/3 s) et la mise en
page projetée (caméra en PERSPECTIVE 60°, table §10.7). **Pas fait** : la
correction des écarts — `borne.cpp` n'a PAS été touché. Sauvegardes posées
avant : `bin\borne_valide_2026-09-09.exe` (sha256 71C9737D…) et
`src_valide_2026-09-09\`. Plan détaillé dans `PROMPT_REPRISE.md`.

**Reprise du 2026-09-13, 11 h** : les 7 points du plan sont appliqués dans
`src\borne.cpp` (projection, bandeaux #00B0FF / #B5E6FD + texte d'info,
icônes ±64 et centre relevé, titre à 64, flèches et bouton de lecture par
`AnimBouton`). Compilé sans avertissement : `bin\borne.exe` 864 441 octets.
Captures prises et envoyées ; positions mesurées sur la capture conformes au
§10.7 à l'échelle près. **EN ATTENTE DE SA VALIDATION** — rien n'est acquis
tant qu'il ne l'a pas dit. Piège de capture : en fenêtré, la zone client
(1370 × 749 sur ce PC) passe sous la barre des tâches ; capturer en F11.

**Vérifications du 13/09 après-midi (polices, icônes, lancement vidéo)**, §10.9
de `interface_apm3_code.md` : une seule police sur l'écran, SEGA_NewRodinN-B,
TrueType EMBARQUÉ, extrait dans `VF5RE\extracted\polices\` ; le logo n'est PAS
sur cet écran (scène `level0` seulement) ; les badges emoney/manette sont
d'`emoneyUI` (surimpression en jeu) ; `AnimationController` lu en CIL grâce à
un faux `pefile` posé dans `tools\pefile.py` : `dotnet.py` marche sans rien
installer.

**« applique tout » (13/09, 15 h 40)** : police SEGA, bandeaux et guides
d'origine, transition vidéo et lancement par les clips (`clips_apm3.h` généré,
`animateur.cpp`), SceneManager transcrit. `bin\borne.exe` 929 185 octets,
sans avertissement. Détail et adaptations : §10.10. **VALIDÉ par Frédéric le
13/09** (« validé mais les flèches … ont disparu ») ; sauvegarde de cet état :
`bin\borne_valide_2026-09-13.exe` et `src_valide_2026-09-13\`. Les flèches
manquaient à cause de la règle de SEGA `index ∓ 3` avec 4 jeux seulement.

**13/09 au soir** : flèches remises à sa demande (ADAPTATION : visibles dès
qu'il reste un jeu de ce côté ; retour à la règle lue écrit en commentaire).
Compilé par g++ direct (`cmd` refuse d'exécuter `construire.cmd` depuis
l'outil ; mêmes options), 929 185 octets, sans avertissement ; 3 captures
envoyées. **EN ATTENTE** de sa validation. Vérifications lues au §10.11 :
ombre = silhouette noire plus proche de la caméra, sans décalage (la borne a
un décalage inventé) ; `HorizontalMoveMessage` speed −4, largeur 1920,
défilement continu (la borne affiche fixe) ; réseau à 3 états ALL.Net,
manette allumée/éteinte seulement dans `emoneyUI`, casque sans détection ;
seul autre écran proche : le menu opérateur `level2`. Sa capture « jointe »
n'est pas arrivée.

**13/09, 20 h 50** — il a répondu : flèches = règle SEGA (rétablie) ; ombre :
« je ne comprends pas les différences » (rien changé, `BORNE_OMBRE=sega` pour
comparer, planche envoyée) ; défilement appliqué ; manette, réseau, casque
appliqués en ADAPTATIONS (`src/etat_pc.cpp`, fil COM, ajouté à
`construire.cmd`) ; `habillage/btn_volume_disable.png` DÉDUIT de la
correspondance de couleurs de SEGA. Détail §10.12. Compilé 941 090 octets,
sans avertissement. **EN ATTENTE** de sa validation. Écran opérateur : l'exe
d'origine ne l'atteint pas hors ligne, il faut le recoder — **périmètre à lui
demander**. Pendant un passage de captures, le journal a noté DROITE ×3 et
ÉCHAP que mes scripts n'ont pas envoyés (origine inconnue, peut-être lui).
Puis il a dit **« arrête avec les captures »** : ne plus lancer la borne pour
capturer tant qu'il ne le redemande pas.

**14/09** — il a signalé que le casque éteint de SEGA existe :
`extracted/apm_icones/emoneyUI__brn_volume_disable.png` (faute « brn » d'origine ;
je l'avais manqué). Il est désormais dans `habillage/btn_volume_disable.png`,
ma version déduite gardée à part. Il veut essayer l'ombre SEGA →
`borne\borne_ombre_sega.cmd`. Il a demandé « le menu principal seul » de
l'écran opérateur → `src/operateur.cpp`, `bin/operateur.exe` (683 807 octets),
`operateur.cmd`, compilé aussi par `construire.cmd` ; §10.13. Les deux
programmes démarrent et se ferment proprement (essai sans capture).

**14/09, 9 h** — sa photo d'une vraie borne a révélé une ERREUR DE MÉTHODE :
les valeurs SÉRIALISÉES de `IconListCanvas` dans `level1` n'avaient jamais été
lues (gapSize 48 et non 16, ombres −20 / −10). Et `IconShadow` est en « ombre
seulement » : les ombres sont de vraies ombres de la lumière `SubLight`
(directionnelle 30°/30°, douces) sur le fond blanc et les bandeaux. Corrigé,
avec la hauteur des textes (métriques GDI ≠ Unity : titre 23 px trop bas),
l'empilement des effets de texte, les bandeaux du film en dégradé, une version
anglaise (`borne_en.cmd`). `borne_ombre_sega.cmd` retiré. `rendu.cpp` a gagné
`decoupe` / `sans_decoupe`. Détail §10.14. `borne.exe` 955 581 octets,
`operateur.exe` 687 909, sans avertissement. Le menu en grille de sa photo n'est
PAS dans ce code (autre version d'APM3). **EN ATTENTE** de ses retours.
**Leçon** : toujours lire les champs sérialisés d'un composant avant d'utiliser
les valeurs par défaut de sa classe.

**14/09, 10 h** — il a **VALIDÉ** tout le §10.14, sauf l'ombre des bandeaux du
haut, dont il doute : incertaine (biais de normale 1,49, texel ≈ 9 px en
Ultra / 4 cascades / distance 1000, décalage de 2,6 px seulement ; la photo n'en
montre pas) — §10.15. **Il a dit « retire-les »** : ombres du bandeau du haut
et de la ligne d'info supprimées ; sauvegarde d'avant : `src_valide_2026-09-14\`
et `bin\*_valide_2026-09-14.exe`. Boutons HOME / START 3D du test des entrées extraits par
`tools/apm_boutons_3d.py` → `extracted/apm_boutons_3d/` (planche envoyée). Premier essai : l'index a semblé bouger seul (2 → 1 → 0) ;
non reproduit sur deux passages avec `BORNE_JOURNAL` (journal propre). Les
captures isolées ratent le milieu des transitions (latence 0,1 à 1 s) :
utiliser une rafale dans un seul processus.

**14/09, 10 h 20 — écran « touchscreen »** (second écran portrait 10", tactile,
résolution inconnue) : `src/touchscreen.cpp` → `bin/touchscreen.exe`
(768 999 octets), lanceurs `touchscreen.cmd`, `borne_touchscreen.cmd`,
`borne_touchscreen_en.cmd`. Grille de jaquettes + fond = DÉDUITS de sa photo
(menu absent du code v1.04 ; couleurs estimées à l'œil, anneaux reconstitués).
Panneau du volume « ヘッドホンボリューム » = LU (`HeadphoneMenu`, scène
`Headphone`, clips Open/Close) ; volume = sortie par défaut de Windows
(adaptation). Lien borne ↔ tablette par `WM_COPYDATA` (« toucher⇥id » /
« etat⇥id ») ; le toucher suit `IconListCanvas.OnTap`. `rendu` gagne
`definir_reference` / `quad_partiel` / `charger_image_reduite` ; `borne.cpp`
gagne `tactile_toucher` / `tactile_annoncer`. Tout compilé sans avertissement
(borne 959 654, operateur 689 329) ; essai journalisé : toucher → sélection →
retour en 33 ms, fermeture liée, codes 0. Sauvegarde : `src_avant_touchscreen_2026-09-14\`,
`bin\*_avant_touchscreen_2026-09-14.exe`. Détail §10.16. **EN ATTENTE** de ses
retours (pas de capture : il les a interdites).

**14/09, 13 h 30 — raccourcis sur le touchscreen** (sa demande) : tuiles YouTube
(Firefox → youtube.com/feed/playlists), Bureau (réduit tout sauf la tablette,
2ᵉ tape = rend ; pas Win+D qui cacherait la tablette), Mes documents
(explorer sur Documents OneDrive), Extinction (InitiateShutdown immédiat,
hybride, programmes FERMÉS DE FORCE, sans confirmation — voulu). Pictogrammes
dessinés par le code. Ascenseur à droite + surbrillance sous le doigt.
`touchscreen.exe` 802 243 octets. Essais UNIQUEMENT avec
`TOUCHSCREEN_RACCOURCIS_A_BLANC=1` (ne jamais lancer l'extinction pour de vrai).
Sauvegarde v1 : `src_touchscreen_v1_2026-09-14\`. §10.16 « Les raccourcis ».

**14/09, 13 h 50** — ses précisions : Extinction = APPUI LONG 2 s (jauge rose,
glisser annule) ; Bureau ne réduit que l'écran PRINCIPAL ; Mes documents sur
l'écran principal ; YouTube sur l'écran TACTILE (Firefox `-new-window`, agrandi).
Placement : indication `SEE_MASK_HMONITOR` + surveillance 15 s des nouvelles
fenêtres `CabinetWClass` / `MozillaWindowClass`, ramenées au besoin (3 fois max).
NON essayé sur deux écrans (un seul écran ici). `touchscreen.exe` 810 871 octets ;
sauvegarde v2 : `src_touchscreen_v2_2026-09-14\`.

**14/09, 14 h** — variante « 6 boutons » des guides du bandeau du bas de la
borne : `BORNE_BOUTONS=6` retire les pastilles (48, 20) et (48, −12), sans
recentrer ; lanceurs `borne_6boutons.cmd`, `borne_touchscreen_6boutons.cmd`,
et en anglais `borne_6boutons_en.cmd`, `borne_touchscreen_6boutons_en.cmd`.
Sauvegarde : `src_avant_6boutons_2026-09-14\`. §10.17.

**14/09, 18 h 45 — sons des vidéos (lu, §10.18)** : aucun bruitage au
lancement ni à la sortie des vidéos ; seule la bande son, muette en attract
seulement si `EnableAdvertizeSound` est faux — or il vaut VRAI par défaut.
L'attract coupe `cursor_lr` / `ok` (`SoundManager.Mute`). Les 4 clips ont des
NOMS : curseur.wav = cursor_lr, valider.wav = ok, retour.wav = add_credit,
demarrer.wav = add_coin. Écarts de la borne relevés, NON corrigés (attente de
sa décision).

**14/09, 19 h — sons corrigés** (« corrige-les tous, 3 = son de la pièce ») :
vidéo d'attract avec son (`BORNE_SON_ATTRACT=0` pour couper) ; lancement = ok ;
jeu sans vidéo = add_coin forcé ; cursor_lr à l'entrée d'une icône dans la zone
du centre (|x| < 192) si CanMove && IsMoving ; mute pendant l'attract. WAV
renommés aux noms SEGA, 6 voix par effet. Sauvegarde : `src_avant_sons_2026-09-14\`,
`habillage\sons\avant_2026-09-14\`. §10.18.

**2026-09-27 — l'écran tactile prend la main (EN ATTENTE de sa validation).**
Reprise sur le PC où le paquet a été copié, `Desktop\VF5 borne APM3\`.
Sauvegardes d'avant : `src_avant_options_2026-09-27\`,
`bin\borne_avant_options_2026-09-27.exe`, `bin\touchscreen_avant_options_2026-09-27.exe`.

* **`src/reglages.h`** (nouveau, entête seul — `construire.cmd` inchangé) :
  `borne\reglages.txt`, cinq lignes, lu par la borne ET l'écran tactile. Les
  variables des lanceurs restent prioritaires (`borne_en.cmd`,
  `borne_6boutons.cmd` marchent tels quels).
* **Icône OPTION** sur l'écran tactile, avec l'icône **de SEGA**
  (`extracted/apm_icones/Apmv3System__Setting.png` → `habillage/touchscreen/Setting.png`,
  sa demande ; mon dessin de trois réglettes ne sert plus que de secours).
  Panneau de 1000 × 300 unités repris de `HeadphoneMenu` (même fond, même
  en-tête #03A9F4, même bouton d'annulation), trois lignes : langue
  日本語/English, boutons 8/6, démarrage avec Windows オン/オフ.
* **Langue et boutons s'appliquent à chaud** : l'écran tactile écrit le
  fichier puis envoie `reglages` par WM_COPYDATA ; la borne relit, regrave ses
  trois textes (`poser_textes_langue`) et redessine ses guides. `six_boutons`
  n'est plus un `static const` figé au démarrage.
* **Démarrage avec Windows** : deux raccourcis `.lnk` (IShellLink) dans le
  dossier de démarrage de l'utilisateur — la borne et l'écran tactile — et
  `plein_ecran=1`, que la borne applique en appelant `basculer_plein_ecran()`.
  Rien dans la base de registre, aucun droit d'administrateur.
* **2ᵉ tape sur Bureau** : elle rend les fenêtres ET envoie `premier_plan` ;
  la borne se remet devant elle-même (un autre processus ne peut pas le faire).
* **Panneau du volume remonté** (sa demande) : `base_panneau()` =
  `max(116 × e, 30 % de la hauteur)` au lieu des 116 unités de SEGA, qui sont
  mesurées sur un écran de 1080 en paysage. Réglable :
  `volume_hauteur=` ou `TOUCHSCREEN_VOLUME_HAUTEUR`.
* **Tuile « fermer le jeu »** (sa demande), icône `Apmv3System__return.png` :
  `catalogue::lancer` rend désormais la poignée du processus
  (`SEE_MASK_NOCLOSEPROCESS`), la borne la garde, `fermer_jeu()` envoie WM_CLOSE
  aux fenêtres du jeu puis `TerminateProcess` après 2 s, et revient devant.
* Compilé sans avertissement (g++ 16.1 de ce PC) : borne 1 254 190,
  touchscreen 1 755 691, operateur 927 698 octets — plus gros que les exes du
  14/09 (autre machine, g++ 16.2) : l'écart est dans les sections `.debug_*`.
  Essai journalisé avec un `reglages.txt` d'essai : la borne lit « langue :
  anglais / guides : 6 boutons », la tablette « langue en, 6 boutons, panneau
  du volume à 476 px du bas », les deux icônes de SEGA se chargent. Fichier
  d'essai retiré ensuite. **Pas de capture : elles restent interdites depuis
  le 13/09.**

**2026-09-27, suite — la dalle n'est visible qu'en partie.** Sa mesure :
l'écran tactile fait **600 x 1024**, mais le cache n'en laisse voir que les
**717 pixels du haut**. `rendu::ancrer_en_haut()` (nouveau) colle la zone de
dessin en haut à gauche au lieu de la centrer, et `mettre_a_l_echelle` prend
`zone_utile` comme hauteur de référence : 990 x 1183 unités au lieu de
990 x 1690. Les touchers restaient justes sans rien changer (ils se
convertissent par `pixels / g_ppu`, sans décalage, depuis le même coin).
Réglage posé dans `borne
eglages.txt` : `zone_utile=717`. Pour l'essayer sur
l'écran principal : `borne	ouchscreen_tablette.cmd`
(`TOUCHSCREEN_FENETRE=600x1024` + `TOUCHSCREEN_ZONE_UTILE=717`). Capture
envoyée (il avait joint la sienne) : les 11 tuiles tiennent en 4 colonnes x 4
rangées dans la zone, noir dessous. **Les titres de la 4e colonne sont
coupés** — à lui de dire s'il préfère 3 colonnes (`TOUCHSCREEN_COLONNES=3`).

**2026-09-27 — « aucune option n'est fonctionnelle » : c'était l'AFFICHAGE.**
Sa capture montrait le panneau ouvert mais NU. Deux défauts, tous deux chez
moi : (1) `dessiner_texte` ne grave pas — une passe de `dessiner()` grave les
trois textes du volume, les miens n'y étaient pas, donc textures vides ;
(2) mes boutons étaient teintés sur `g_s_annuler`, le sprite ROUGE du bouton
Cancel, d'où le bleu nuit et le bordeaux ; ils prennent maintenant
`g_s_barre`, le sprite blanc. Le MÉCANISME, lui, marchait : essai par vrais
clics (`SendInput`, jamais `PostMessage` — les messages postés n'atteignent
pas la fenêtre), journal à l'appui : « bouton 1 → langue anglais », « bouton 4
→ APM3 borne.lnk posé ». Les étiquettes des tuiles passent à l'anglais dans la
seconde. **Leçon : un panneau qui ne réagit pas peut n'être qu'un panneau
qu'on ne sait pas lire — vérifier l'affichage avant la logique.** L'essai a
été DÉFAIT : raccourcis de démarrage supprimés, `reglages.txt` remis en
japonais / 8 boutons / sans démarrage.

**VALIDÉ par Frédéric le 2026-09-27** (« c'est validé ») : zone visible,
icône OPTION, icône « quitter le jeu », panneau du volume remonté, 2e tape sur
Bureau. Sauvegardes de cet état : `src_valide_2026-09-27\` et
`binorne_valide_2026-09-27.exe`, `bin	ouchscreen_valide_2026-09-27.exe`,
`bin\operateur_valide_2026-09-27.exe`. Puis, sa demande suivante : le bouton
des DEUX panneaux (volume et options) dit maintenant **« Close » / « 閉じる »**
au lieu de « Cancel » / « キャンセル » — écart assumé avec la scène de SEGA,
noté dans le commentaire de `HeadphoneMenu`. Vu à l'écran sur les deux
panneaux.

**Piège des essais par clics** : ils écrivent VRAIMENT dans `reglages.txt` et
posent les raccourcis de démarrage — sauvegarder le fichier avant, et remettre
l'état après. Et `PostMessage` n'atteint pas ces fenêtres : seuls de vrais
clics (`SendInput`) les touchent.

**Et l'inverse est vrai aussi** : le 27/09, j'ai vu deux fois `reglages.txt`
repasser en anglais avec le démarrage activé après mon nettoyage, et j'ai
soupçonné un défaut. **C'était Frédéric** qui se servait d'OPTION pendant que
je travaillais (« c'est moi »). Avant d'accuser le code, regarder l'HEURE du
fichier et demander : il utilise la borne en même temps que moi.

**2026-09-27, ménage (sa demande).** `borne\` passe de 632 à 343 Mo.
Supprimes : les huit sauvegardes de sources intermediaires, onze exes perimes,
les QUATRE dossiers de jeux en double (`SF3.3`, `SSFIIX`, `VF3tbo`, `VFeS`,
identiques a l'octet aux versions au nom complet — d'ou les jeux affiches en
double), les six lanceurs de langue et de boutons (leurs variables ECRASAIENT
le choix d'OPTION), et, sur sa decision, la paire du 09/09
(`src_valide_2026-09-09` + son exe) : c'etait l'etat d'AVANT la refonte des
13-14/09, 1773 lignes d'ecart dans `borne.cpp`. **Il ne reste donc qu'un seul
etat de reference : `src_valide_2026-09-27` et les trois
`bin\*_valide_2026-09-27.exe`.** Gardes aussi : `essai_video.exe` (le banc
Media Foundation, pour la lenteur des videos) et les 29 jaquettes seules de
`jeux\` (son choix ; la borne les ignore). Les mentions des lanceurs retires
ont ete corrigees dans le LISEZ-MOI et deux commentaires de sources, puis tout
a ete recompile.

**2026-09-27, les lanceurs (sa decision).** Il n'en reste que DEUX :
`borne_touchscreen.cmd` (le lancement normal : tablette puis borne, avec
`TOUCHSCREEN_SUIVRE_BORNE=1`) et `construire.cmd`. Supprimes : `borne.cmd`,
`touchscreen.cmd`, `operateur.cmd`, `touchscreen_tablette.cmd` — ils ne
faisaient que lancer un exe, ce qu'un double-clic dans `bin\` fait aussi (les
exes trouvent seuls `jeux\`, `habillage\` et `reglages.txt`). **La
documentation du toucher vivait dans l'entete de `touchscreen.cmd`** : elle a
ete recopiee dans `LISEZ-MOI.txt` (section « L ECRAN TACTILE, TUILE PAR
TUILE ») AVANT la suppression, avec les deux nouvelles tuiles. Lecon : un
lanceur de ce chantier n'est pas qu'un raccourci, c'est aussi de la doc — la
relire avant de le jeter.

**2026-09-27, fin du menage : plus une seule copie datee.** Sur sa decision,
`src_valide_2026-09-27` et les trois `bin\*_valide_2026-09-27.exe` sont
supprimes aussi. Motif : la photo ne valait plus que 18 lignes d'ecart avec
`src\`, dont 2 fonctionnelles (Cancel -> Close, qu'il a demande et vu), et les
exes « valides » allaient avec la photo, pas avec les sources -- deux
references legerement differentes, exactement la confusion qu'on venait de
supprimer pour le 09/09. **Etat unique : `src\` + les trois exes de `bin\`**
(plus `essai_video.exe`). Le dossier `borne\` fait 339 Mo, neuf entrees.
Convention pour la suite : une photo datee quand il valide quelque chose de
consequent, pas avant.

**2026-09-27 — LES VIDÉOS, RÉGLÉ ET VALIDÉ** (« c'est bon: image et son OK »).
Mesure en situation, sur sa démo de 1080p60 à 53,7 Mbit/s : **0,23 ms par
trame au lieu de 12 à 13**, sur les 16,7 ms d'une trame à 60 Hz. Le décodage
passe par la carte (`MF_SOURCE_READER_D3D_MANAGER` +
`ENABLE_ADVANCED_VIDEO_PROCESSING`), la trame reste sur la carte et se recopie
d'une texture à l'autre : le processeur ne touche plus un seul pixel.

**TROIS PIÈGES, tous muets, tous mesurés — c'est l'essentiel à retenir :**

1. **La protection multi-fils.** Media Foundation fait décoder par ses propres
   fils sur NOTRE périphérique Direct3D. Sans
   `ID3D11Multithread::SetMultithreadProtected(TRUE)`, le **premier
   `ReadSample` ne rend jamais la main** : banc témoin, blocage à plus de
   420 s ; avec elle, 8 essais sur 8 démarrent en 0,03 s
   (`bancs/banc_protege.cpp`). C'est ce blocage que j'avais pris pour un
   défaut de Media Foundation le matin même — c'était mon banc qui était
   fautif.
2. **La famille de format.** `CopySubresourceRegion` entre deux formats de
   familles différentes **ne copie rien et ne dit rien** : écran noir, son
   normal. Le décodeur de cette machine rend du **B8G8R8X8_UNORM (DXGI 88)**,
   ma texture était en B8G8R8A8 (87). La texture est maintenant créée au
   format de la source, et se refait toute seule si une autre carte en donne
   un autre. Bonus : en X8, l'alpha vaut 1 à la lecture — le forçage à 255
   pixel par pixel (1,1 ms par trame) disparaît.
3. **Le repli doit être complet.** Quand la recopie est refusée, le processeur
   reprend la trame — mais il lui faut une texture `DYNAMIC` : écrire par
   `Map` dans une texture `DEFAULT` échoue, et l'image reste noire. Le repli
   change donc AUSSI de texture.

`rendu` gagne `appareil()`, `creer_video(l, h, format)` et
`copier_texture()` (qui rend false si la copie est impossible) ; le
périphérique porte `D3D11_CREATE_DEVICE_VIDEO_SUPPORT` et la protection
multi-fils. `construire.cmd` gagne **`-ldxguid`** pour les trois programmes
(`IID_ID3D11Multithread`). Le chemin logiciel d'origine reste en secours,
intact. Les bancs sont dans **`borne\bancs\`** (il a demandé à les garder) :
`banc_video.cpp` compare les quatre chemins, `banc_ouvrir.cpp` minute chaque
étape, `banc_protege.cpp` isole la protection multi-fils.

**Avec `BORNE_JOURNAL`, la borne dit tout** : « ouverture réussie, decodage
PAR LA CARTE », puis à la fin « N trames, X ms par trame », et si la recopie
n'a pas pu se faire, le format et la taille de la texture qu'on lui tendait.

**La lenteur des vidéos, MESURÉE (rien n'est corrigé, il a dit de passer à la
suite).** Ses démos sont en 1080p à 60 i/s, l'une à 53,7 Mbit/s. Le chemin
actuel (`MF_SOURCE_READER_ENABLE_VIDEO_PROCESSING`, sortie RGB32) est
**logiciel** : 10,8 à 12,3 ms par trame, plus 1,1 ms de recopie avec l'alpha
forcé pixel par pixel — sur les 16,7 ms d'une trame à 60 Hz. Le chemin
matériel (`MF_SOURCE_READER_D3D_MANAGER` + `ADVANCED_VIDEO_PROCESSING`) donne
**1,8 à 2,5 ms**, six fois moins. MAIS il se bloque parfois au **premier
`ReadSample`** (3 essais sur 5, plus de 120 s) : la création du lecteur, elle,
prend 0,02 s. Donc le passage au matériel n'est PAS un simple changement
d'attribut : il faut décoder dans un FIL, sinon un blocage gèle la borne.
Bancs d'essai : `banc_video.cpp` et `banc_ouvrir.cpp` (bac à sable).

**Écarté à sa demande (2026-09-27)** : « le mode kiosque ne doit pas démarrer
si l'utilisateur a activé la lecture d'une vidéo » — sans objet ; au passage,
la démo automatique est déjà gelée pendant une vidéo lancée à la main
(`compter_ecoule` n'est appelé que si `peut_choisir()`).

**How to apply:** si Frédéric revient sur ce PC, le travail a pu continuer
ailleurs : comparer les dates de `SEPTEMBRE\VF5 borne APM3\VF5RE\borne\src`
avec `VF5RE\borne\src` avant de toucher à quoi que ce soit. Voir
[[reference_apm3_code_interface]] et [[reference_apm3_interface]].
