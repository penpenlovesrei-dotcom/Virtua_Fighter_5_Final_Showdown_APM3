@echo off
rem -----------------------------------------------------------------------
rem VF5 FS -- RETIRER les dix-neuf decors de Virtua Fighter 5 R
rem
rem Rend l etat d origine : les dix pieces de chacun, les deux bases, et
rem l entree d obj_db ecrite dans le .par.
rem -----------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
echo.
echo   Retrait des dix-neuf decors...
py -3 tools\decor_neuf.py --retirer-lot 5r
echo.
echo   Fait. Le moteur se remet au prochain lanceur : le patcheur
echo   repart toujours de .origine.
pause
endlocal
