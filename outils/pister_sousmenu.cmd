@echo off
rem ---------------------------------------------------------------------------
rem MESURE : pourquoi le menu principal repond-il encore dans un sous-menu ?
rem Double-cliquez. Le jeu se lance, vous jouez, l'outil observe.
rem
rem   deux fois Entree -^> menu console
rem   descendez sur OFFLINE VERSUS, validez
rem   dans le sous-menu, HAUT et BAS plusieurs fois
rem   Echap pour revenir
rem
rem Le bilan s'affiche a la fermeture ET est ecrit dans
rem analysis\pister_sousmenu_bilan.txt
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\pister_sousmenu.py %*
echo.
pause
endlocal
