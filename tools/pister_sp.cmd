@echo off
rem ---------------------------------------------------------------------------
rem MESURE : pourquoi SINGLE PLAYER ne lance rien.
rem Double-cliquez. Le jeu se lance, vous jouez, l'outil observe.
rem
rem   deux fois Entree -^> menu console
rem   SINGLE PLAYER, validez
rem   choisissez Arcade, validez
rem   dans la page de reglages, validez
rem   puis fermez le jeu.
rem
rem Bilan dans analysis\pister_sp_bilan.txt
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\pister_sp.py %*
echo.
pause
endlocal
