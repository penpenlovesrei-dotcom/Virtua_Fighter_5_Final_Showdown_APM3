@echo off
rem ---------------------------------------------------------------------------
rem MESURE UN ECRAN DE MENU TOUT SEUL : lance, navigue, photographie, et dit
rem si l ecran est noir. Double-cliquez, ne touchez a rien.
rem
rem   essai_menu.cmd            SINGLE PLAYER
rem   essai_menu.cmd dojo       le DOJO
rem   essai_menu.cmd cran 6     la septieme ligne, quelle qu elle soit
rem
rem Captures dans analysis\essai_<nom>_tNN.png
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
if "%~1"=="" (py -3 tools\essai_menu.py sp) else (py -3 tools\essai_menu.py %*)
echo.
pause
endlocal
