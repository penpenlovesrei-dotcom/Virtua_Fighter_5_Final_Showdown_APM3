@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- OU PLANTE L'ECRAN SETTINGS. Double-cliquez.
rem
rem POURQUOI CE LANCEUR. La cinquieme ligne "Resolution" fait planter
rem l'ouverture d'OPTIONS ^> Settings. J'ai onze sites dans le moteur et six
rem relais : en designer un au juge serait exactement l'erreur deja commise sur
rem "select part", ou le relais etait INNOCENT et la faute dans un debordement
rem de tableau du moteur. On mesure donc l'adresse AVANT de l'expliquer.
rem
rem CE LANCEUR N'EST PAS CELUI AVEC LEQUEL VOUS JOUEZ : item_porte.cmd n'a plus
rem --options-resolution, il marche. Celui-ci la remet, expres, sous debogueur.
rem
rem CE QU'IL FAIT : il n'arme AUCUN point d'arret ^(--sans-jalons^). Le jeu
rem tourne a pleine vitesse ; le debogueur ne sert qu'a recevoir l'exception
rem que Windows envoie au moment du plantage.
rem
rem CE QU'IL FAUT FAIRE, et c'est tout :
rem   1. laissez arriver le menu
rem   2. OPTIONS ^> Settings
rem   3. le jeu plante -- c'est voulu, la sonde ecrit ce qu'il faut
rem
rem CE QUE LA SONDE ECRIRA :
rem   EXCEPTION ACCESS_VIOLATION
rem     ou      : ...dll!.text+0x1AA4xx ^(VA preferee 0x1801AA4xx^)
rem     acces   : lecture de 0x0000000000000000
rem     cible   : ...
rem     --- code autour de RIP ---
rem
rem L'adresse a la base PREFEREE est la seule qui se retrouve dans un
rem desassemblage. Si elle tombe dans la greffe ^(0x180EA4xxx^) la faute est
rem dans un de mes relais ; si elle tombe dans .text, c'est le moteur qui
rem deborde, et il faudra savoir sur quoi.
rem
rem Journal au fil de l'eau : analysis\pister_plantage.txt
rem
rem LE DEMARRAGE EST LENT. Laissez-lui le temps.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- OU PLANTE L'OUVERTURE DE SETTINGS
echo   ===================================================================
echo.
tasklist /fi "IMAGENAME eq vfes.exe" 2>nul | findstr /i "vfes.exe" >nul
if not errorlevel 1 (
  echo   vfes.exe TOURNE DEJA -- apm.dll est verrouillee et le patch
  echo   echouerait en silence cote copie. Fermez le jeu d'abord.
  pause
  exit /b 1
)
echo   Compilation de apm.dll...
py -3 tools\gen_apm_stub.py >nul
if errorlevel 1 (
  echo.
  echo   La compilation du apm.dll a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo   Patch du moteur, AVEC la ligne Resolution...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 ^
    --menu-fermer --options-raccourci --dojo-howto --dojo-cadre ^
    --options-sans-howto --menu-exit --legende-sousmenu ^
    --attract-retour-titre --sans-now-loading --options-tips ^
    --decor-perso trm --terminal-boutons --customize-curseur ^
    --replays-sans-gel --vignettes-costume --selitem-grille ^
    --selitem-republier --selitem-ecreter --selpart-curseur ^
    --item-basculer --sans-warning --options-resolution >nul
if errorlevel 1 (
  echo.
  echo   Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
if not exist "runtime\media\vf5fs\ram" mkdir "runtime\media\vf5fs\ram"
echo.
echo   -------------------------------------------------------------------
echo    CE QU'IL FAUT FAIRE :
echo      1. laissez arriver le menu
echo      2. OPTIONS ^> Settings
echo      3. le jeu plante -- c'est VOULU, la sonde note l'adresse
echo.
echo    Aucun point d'arret n'est arme : pleine vitesse.
echo    Journal : analysis\pister_plantage.txt
echo   -------------------------------------------------------------------
echo.
py -3 tools\pister_plantage.py --sans-jalons --garder-scenario --secondes 600
echo.
echo   ===================================================================
echo    OU CA A PLANTE
echo   ===================================================================
if exist "analysis\pister_plantage.txt" (
  findstr /n /c:"EXCEPTION" /c:"ou      :" /c:"acces   :" /c:"cible   :" ^
      /c:">>>" "analysis\pister_plantage.txt"
) else (
  echo   AUCUN JOURNAL. La sonde n'a rien ecrit.
)
echo.
echo   Journal complet : analysis\pister_plantage.txt
echo.
pause
endlocal
