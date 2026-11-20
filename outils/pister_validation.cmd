@echo off
rem ---------------------------------------------------------------------------
rem MESURE : d'ou vient la double validation d'Entree.
rem Double-cliquez. Le jeu se lance, vous jouez, l'outil observe.
rem
rem   deux fois Entree -^> menu console
rem   descendez sur OPTIONS, validez UNE SEULE FOIS
rem   puis fermez le jeu tout de suite.
rem
rem Moins vous appuyez, plus le releve est lisible.
rem Bilan dans analysis\pister_validation_bilan.txt
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\pister_validation.py %*
echo.
pause
endlocal
