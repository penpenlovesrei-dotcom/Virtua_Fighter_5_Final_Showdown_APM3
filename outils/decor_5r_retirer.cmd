@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- RETIRE LE DECOR IMPORTE DE VF5 R ET REMET LE JEU D'ORIGINE
rem
rem Rend les huit noms dans l'index de vf5fs_data.par et efface les fichiers
rem libres poses dans vf5fs_media/rom/. Le moteur reprend le decor DJO de Final
rem Showdown, celui de l'archive.
rem
rem Le binaire n'est pas concerne : l'import ne le touchait pas.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\importer_decor.py --retirer djo
echo.
echo   Etat d'origine retabli. Relancez console.cmd ou decors_dural.cmd.
echo.
pause
endlocal
