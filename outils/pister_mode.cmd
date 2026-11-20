@echo off
rem ---------------------------------------------------------------------------
rem MESURE : qui pose le mode de jeu, et qui le repose.
rem
rem Double-cliquez. Le build d'essai est applique, le jeu se lance, vous jouez,
rem l'outil observe et note chaque ecriture du mode avec le site qui l'a faite.
rem
rem   deux fois Entree      -^> menu console
rem   SINGLE PLAYER, validez
rem   SCORE ATTACK, validez
rem   dans la page de reglages, validez
rem   laissez le combat demarrer, puis fermez le jeu.
rem
rem Le jeu tourne au ralenti sous le debogueur : c'est normal, ne vous en
rem inquietez pas. Moins vous appuyez, plus le releve est lisible.
rem
rem Releve au fil de l'eau : analysis\pister_mode.txt
rem Bilan                  : analysis\pister_mode_bilan.txt
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-mode --joueur2 --menu-fermer ^
    --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto ^
    --menu-exit --decor-perso trm >nul
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
py -3 tools\pister_mode.py %*
echo.
pause
endlocal
