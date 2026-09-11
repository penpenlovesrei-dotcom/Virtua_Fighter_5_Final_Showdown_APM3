@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LES VARIANTES DE DURAL, AVEC LE NOM ECRIT A L'ECRAN
rem
rem Double-cliquez, PATIENTEZ le demarrage, puis STAGE SELECT, curseur sur la
rem case SANCTUARY, BARRE ESPACE :
rem
rem     SNOW -> ECLIPSE -> SUBMERSION -> STORM -> SPACE -> SNOW ...
rem
rem   Le nom s'ecrit en blanc, centre, a x=640 y=470.
rem
rem LA CORRECTION DU DECOR TRM EST PORTEE ICI
rem
rem   `--decor-perso trm` : l'ecran TERMINAL / Customize demande DEUX fois
rem   un decor, chacun avec son propre index en dur --
rem     0x1801C4DA6  la GEOMETRIE  (via 0x18018FCF0, une FEUILLE)
rem     0x1801C4DCB  l'ECLAIRAGE   (via 0x1800D7130)
rem   Seul l'eclairage etait patche jusqu'au 2026-09-05, d'ou trois essais
rem   � aucune difference � : en changer l'index ne deplace qu'une teinte.
rem   L'option remplace les DEUX octets. Meme correction que decor_TRM.cmd.
rem   Detail : analysis\menu_console.md 15.10.
rem
rem CE LANCEUR NE TOUCHE PAS AU DOJO
rem
rem   Le dojo d'Akira en version VF5 R a son propre lanceur, VALIDE :
rem   decor_5r_akira.cmd. Il n'est ni modifie ni concerne par celui-ci.
rem   Le chantier « ajouter le 5R sans remplacer » est en attente.
rem
rem   Ce lanceur n'a PAS --decors-dural : cette option translate les indices
rem   7..11 vers du1..du5, et djo vaut 11 -- le combat au dojo chargerait du5.
rem   L'anneau des variantes n'en a pas besoin : il agit directement sur
rem   [TaskSelStage+0x5C] depuis la case `dur` de la grille.
rem
rem LE TEXTE AU PREMIER PLAN -- METHODE VALIDEE le 2026-09-08
rem
rem   La commande de dessin est soumise au contexte 2D (0x180719900) par
rem   0x180187C00, et 0x18018CA20 l'insere a une adresse CALCULEE :
rem
rem       contexte + 16 * ( (desc+0x24) + 1 + ((desc+0x28 + calque) << 5) )
rem
rem   La commande du texte ne pose PAS son champ de calque (cmd+0x14) : il
rem   reste a -1, et l'insertion retombe sur [contexte+0x828], le calque que
rem   l'AET a deja monte. Le texte passait donc dessous, quel que soit
rem   l'instant de l'appel.
rem
rem   MONTER CE CALQUE FAIT PLANTER. Le constructeur du contexte le dit :
rem
rem     0x18018A049  mov ecx, 0x838 ; call operator new     <- 0x838 octets
rem     0x18018A092  call 0x1802FE160(ctx+0x10, 0x10, 0x80) <- 128 cases de 16 o
rem
rem   Le « +1 » est ce decalage de 0x10, donc l'indice reel vaut
rem   (desc+0x24) + ((desc+0x28 + calque) << 5), BORNE A 0..127 : quatre
rem   calques de trente-deux rangs. +8 calques demandait l'indice 264.
rem
rem   Le correctif ne touche a aucun etat global. Il corrige NOTRE seul
rem   descripteur pour viser le dernier compartiment, le 127 :
rem
rem       desc+0x28 = plafond - calque   -> le calque effectif vaut 3
rem       desc+0x24 = ordre              -> le rang 31
rem
rem   Si le calque courant depassait deja 3, on ne dessine pas : pas de texte
rem   plutot qu'un acces invalide.
rem
rem   Le dessin part du CRENEAU 4 de TaskSelStage (0x180400A38), un bouchon
rem   `ret 0` -- la phase de rendu. Liseret fait a la main : neuf passes, huit
rem   noires decalees de 2 px, la blanche au centre.
rem
rem   Aucun pointeur absolu dans la greffe : la DLL est REBASEE a l'execution
rem   et la section greffee n'a pas de relocation. Les chaines sont a pas fixe
rem   de 32 octets, l'adresse se calcule en RIP-relatif.
rem
rem REGLAGES, tous des donnees de la greffe -- aucun reassemblage
rem
rem     0x180EA1618   plafond de calque                 3   (NE PAS AUGMENTER)
rem     0x180EA161C   rang dans le calque               31  (0..31)
rem     0x180EA1620   x                                 640
rem     0x180EA1624   y                                 470
rem     0x180EA162C   taille de police                  24
rem
rem   Le rendu tombe ~50 px plus haut que la valeur : -10 remonte de 10 px.
rem
rem SI QUELQUE CHOSE CLOCHE
rem
rem   variantes.cmd rend la meme build SANS le dessin -- le defilement seul,
rem   celui qui a charge DU4.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
rem Un journal, pour le cas ou la fenetre se refermerait trop vite.
if exist "analysis\variantes_texte.log" del "analysis\variantes_texte.log" >nul 2>&1
echo VF5 -- variantes_texte.cmd  %DATE% %TIME% > "analysis\variantes_texte.log"
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
rem ETAT DES FICHIERS : on le POSE, on ne l'herite pas.
rem Le patcheur repart de .origine ; cote fichiers, c'est cette ligne.
rem Sans elle, le dojo VF5 R pose par decor_5r_akira.cmd restait en place
rem dans tous les autres lanceurs.
rem Un balayage du .par coute 16 secondes. On ne le fait que s'il y a
rem vraiment quelque chose a retirer : --poser depose les fichiers ET
rem masque les noms d'un seul geste, donc le fichier libre est la preuve.
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgdjo.farc" (
  echo   Le dojo VF5 R est pose sur djo : on le retire ^(~20 s^)...
  py -3 tools\importer_decor.py --retirer djo >> "analysis\variantes_texte.log" 2>&1
)
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrm.farc" (
  echo   Un decor est pose sur trm : on le retire ^(~20 s^)...
  py -3 tools\importer_decor.py --retirer trm >> "analysis\variantes_texte.log" 2>&1
)
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrs.farc" (
  echo   Un decor est pose sur trs : on le retire ^(~20 s^)...
  py -3 tools\importer_decor.py --retirer trs >> "analysis\variantes_texte.log" 2>&1
)

echo   Compilation de apm.dll...
py -3 tools\gen_apm_stub.py >> "analysis\variantes_texte.log" 2>&1
if errorlevel 1 (
  echo.
  echo La compilation du apm.dll a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo   Patch du moteur ^(~15 s^)...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso trm --variantes --variantes-texte --du2-collision >> "analysis\variantes_texte.log" 2>&1
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   STAGE SELECT, case SANCTUARY, BARRE ESPACE.
echo   Le nom de la variante s'ecrit en blanc, au centre.
echo.
pushd "%~dp0..\runtime\media\vf5fs"
if not exist vfes.exe (
  echo INTROUVABLE : "%CD%\vfes.exe"
  pause
  popd
  exit /b 1
)
echo   Demarrage du jeu -- il met un moment a afficher.
start "" "%CD%\vfes.exe"
"%SystemRoot%\System32\timeout.exe" /t 8 /nobreak >nul 2>&1
tasklist /fi "IMAGENAME eq vfes.exe" | find /i "vfes.exe" >nul
if errorlevel 1 (
  echo.
  echo LE JEU NE S'EST PAS LANCE, ou il s'est arrete aussitot.
  pause
) else (
  echo   Le jeu tourne.
)
popd
echo.
echo   Journal complet : analysis\variantes_texte.log
echo.
pause
endlocal
