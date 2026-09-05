@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LE BUILD CONSOLE COMPLET. Double-cliquez, rien a taper.
rem
rem Ce qu'il contient, tout valide a l'ecran sauf la derniere ligne :
rem   . Dural jouable dans la grille
rem   . SINGLE PLAYER  : combat solo, retour au menu, on peut relancer
rem   . OFFLINE VERSUS : a deux -- clavier = joueur 1, manette = joueur 2
rem   . DOJO           : entrainement
rem   . TERMINAL       : avec son vrai decor (trm)
rem   . Echap          : sortir d'un mode et revenir au menu
rem   . EXIT GAME      : dixieme ligne du menu, ferme le jeu (sans confirmation)
rem   . DOJO           : une 4e ligne, How to Play  <- A ESSAYER
rem
rem   Touches : fleches, Entree = VALIDER, W = ANNULER, X C V = croix rond triangle,
rem             Espace = SELECT, Echap = quitter le mode, F1/F2 = TEST/SERVICE.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --decor-perso trm
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   Deux fois Entree  -^> menu console
echo   EXIT GAME est la DIXIEME ligne, tout en bas de la liste.
echo   Elle ferme le jeu tout de suite, sans confirmation.
echo.
cd /d "%~dp0..\runtime\media\vf5fs"
start "" vfes.exe
endlocal
