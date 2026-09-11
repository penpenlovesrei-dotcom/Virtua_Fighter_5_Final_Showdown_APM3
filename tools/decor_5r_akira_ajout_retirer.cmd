@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- RETIRE LE DOJO VF5 R AJOUTE SUR trs, ET REND L'ETAT D'ORIGINE
rem
rem Rend les huit noms dans l'index de vf5fs_data.par et efface les fichiers
rem libres poses dans vf5fs_media/rom/ sous le code `trs`. L'emplacement
rem redevient le decor d'essai vide qu'il etait.
rem
rem Le binaire n'est pas concerne : patch_moteur.py repart toujours de
rem vf5fs-pxd-w64-Retail_APM3.dll.origine, donc le clone de descripteur
rem disparait des le prochain lanceur.
rem
rem Le dojo de Final Showdown n'a jamais bouge : ce lanceur ne le touche pas.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
echo   Retrait du decor pose sur trs ^(~20 s, un balayage du .par^)...
py -3 tools\importer_decor.py --retirer trs
echo.
echo   Etat d'origine retabli. Relancez console.cmd, variantes_texte.cmd ou
echo   n'importe quel autre lanceur : chacun repose son propre etat.
echo.
pause
endlocal
