@echo off
rem ---------------------------------------------------------------------------
rem MESURE : pourquoi les sous-sous-menus d'options refusent-ils de s'ouvrir ?
rem Double-cliquez. Le jeu se lance, vous jouez, l'outil observe.
rem
rem   deux fois Entree -^> menu console
rem   descendez sur HELP ^& OPTIONS, validez
rem   essayez CHAQUE ligne, une par une :
rem      How to Play, Controls, Settings, Save Data, Credits
rem   puis fermez le jeu.
rem
rem Le bilan s'affiche a la fermeture ET est ecrit dans
rem analysis\pister_scene_bilan.txt
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\pister_scene.py %*
echo.
pause
endlocal
