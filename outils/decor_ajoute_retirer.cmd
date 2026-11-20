@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- RETIRE LE DECOR AJOUTE d5r ET REND L'ETAT D'ORIGINE
rem
rem Efface les neuf pieces posees sous le code d5r, les deux bases reecrites,
rem et rend au .par les deux noms masques (obj_db.bin et auth_3d_db.bin).
rem
rem Le binaire n'est pas concerne : patch_moteur.py repart toujours de
rem vf5fs-pxd-w64-Retail_APM3.dll.origine, donc la table redevient 41 decors
rem des le prochain lanceur.
rem
rem Aucun decor du jeu n'a ete touche : il n'y a rien d'autre a rendre.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
echo   Retrait du decor ajoute ^(~20 s, un balayage du .par^)...
py -3 tools\decor_neuf.py --retirer d5r
echo.
echo   Etat d'origine retabli. N'importe quel autre lanceur repose le sien.
echo.
pause
endlocal
