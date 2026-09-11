@echo off
rem -----------------------------------------------------------------------
rem VF5 FS -- RETIRER les decors du VIRTUA FIGHTER 5 d origine (ver.B)
rem
rem Retire les pieces de ver.B et les deux bases. Les decors de VF5 R
rem restent poses : decors_5r.cmd refait ses bases lui-meme. Pour tout
rem rendre, VF5 R compris : decors_5r_retirer.cmd ensuite.
rem -----------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
echo.
echo   Retrait des decors de ver.B...
py -3 tools\decor_neuf.py --retirer-lot vf5
echo.
echo   Fait. Le moteur se remet au prochain lanceur : le patcheur
echo   repart toujours de .origine.
pause
endlocal
