@echo off
rem ---------------------------------------------------------------------------
rem MESURE : quel decor l'ecran TERMINAL charge-t-il, et par quel chemin ?
rem
rem Aucun patch n'est applique : on observe le jeu tel qu'il est.
rem
rem Le jeu se lance sous debogueur. C'EST VOUS QUI LE MENEZ :
rem    1. deux fois Entree            -> menu console
rem    2. descendre sur TERMINAL, valider
rem    3. laisser tourner quelques secondes, puis Echap
rem
rem Le resultat s'affiche a la fin, dans cette fenetre.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\pister_decor.py %*
echo.
pause
endlocal
