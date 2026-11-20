@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- L'ESSAI DE LA GREFFE RELOGEABLE
rem
rem Double-cliquez. Il n'y a RIEN A VOIR A L'ECRAN : cet essai ne change pas
rem une image du jeu. Ce qu'il montre, c'est que le chargeur de Windows
rem accepte une table de relocations que NOUS avons reconstruite -- et donc
rem qu'une section greffee peut desormais porter des pointeurs absolus.
rem
rem POURQUOI CA COMPTE
rem
rem   La DLL est rebasee a chaque lancement (une adresse differente a chaque
rem   fois). Une section ajoutee apres coup n'apparait dans aucun bloc de
rem   relocation : une adresse ecrite dedans reste a la base preferee
rem   0x180000000 et ne designe plus rien. C'est cette limite qui interdisait
rem   un descripteur de decor COMPLET -- la table des murs (+0xC0), les neuf
rem   musiques, les noms d'auth_3d sont tous des pointeurs.
rem
rem CE QUE LE LANCEUR FAIT
rem
rem   1. construit le build console habituel ;
rem   2. lui greffe une section `.decors` et y ecrit, EN ABSOLU, l'adresse de
rem      la table des descripteurs (0x180403430) ;
rem   3. reconstruit la table de relocations entiere -- les 209 blocs
rem      d'origine PLUS le notre -- dans une section `.reloc2`, et repointe le
rem      repertoire de donnees n 5 ;
rem   4. lance le jeu, attend qu'il charge, et LIT LA MEMOIRE DU PROCESSUS.
rem
rem CE QU'IL FAUT LIRE
rem
rem   Sans relocation, le temoin vaudrait encore 0x180403430.
rem   Avec, il doit valoir  base_reelle + 0x403430.
rem   Le verdict est ecrit en toutes lettres a la fin.
rem
rem   Pour revenir a un build normal : n'importe quel autre lanceur. Le
rem   patcheur repart toujours de .origine, la greffe disparait d'elle-meme.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1

echo   [1/4] Auto-controle du format, sur une copie de .origine...
echo.
py -3 tools\pe_sections.py --essai
if errorlevel 1 (
  echo.
  echo L'AUTO-CONTROLE A ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)

echo.
echo   [2/4] Construction du build console ^(~15 s^)...
py -3 tools\gen_apm_stub.py >nul 2>&1
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso trm --variantes --variantes-texte --du2-collision >nul
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)

echo.
echo   [3/4] Greffe de .decors et reconstruction des relocations...
echo.
py -3 tools\pister_relocations.py --poser
if errorlevel 1 (
  echo.
  echo LA GREFFE A ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)

echo.
echo   [4/4] Lancement du jeu, puis lecture de sa memoire.
echo         Le demarrage est LENT : on attend 35 secondes.
echo.
pushd "%~dp0..\runtime\media\vf5fs"
start "" "%CD%\vfes.exe"
popd
"%SystemRoot%\System32\timeout.exe" /t 35 /nobreak >nul 2>&1
tasklist /fi "IMAGENAME eq vfes.exe" | find /i "vfes.exe" >nul
if errorlevel 1 (
  echo.
  echo LE JEU S'EST ARRETE AUSSITOT -- c'est deja un resultat : le chargeur
  echo a refuse l'image. Dites-le-moi.
  pause
  exit /b 1
)
echo.
py -3 tools\pister_relocations.py --lire
set "VERDICT=%ERRORLEVEL%"
echo.
if "%VERDICT%"=="0" (
  echo   Le jeu tourne encore : fermez-le avec Echap, ou laissez-le.
) else (
  echo   L'essai a ECHOUE. Le detail est au-dessus.
)
echo.
pause
endlocal
