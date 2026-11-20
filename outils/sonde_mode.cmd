@echo off
rem -----------------------------------------------------------------------
rem VF5 FS -- LA SONDE DES MODES
rem
rem POURQUOI (2026-10-13). « Exit without saving » ne rend pas le menu :
rem il retombe sur l ecran « Select Part ». Trois correctifs poses a trois
rem endroits differents n y ont rien change. On arrete de deviner.
rem
rem CE QU ELLE REGARDE, et c est tout :
rem
rem   0x1800DA9A0   « je demande ce MODE »        -> ecx = le mode
rem   0x1800DA9C0   « je demande ce SOUS-ETAT »   -> ecx = le sous-etat
rem
rem Chaque passage est journalise avec ses registres. La suite des demandes,
rem lue dans l ordre, dit QUI ecrase notre demande de mode 4 et avec quoi.
rem
rem CE QU IL FAUT FAIRE :
rem   1. fermez toute partie en cours (la sonde refuse de demarrer sinon) ;
rem   2. double-cliquez ici ;
rem   3. dans le jeu : VF.TERMINAL, puis Customize, puis choisissez une
rem      donnee, puis « exit without saving » ;
rem   4. fermez le jeu.
rem
rem Le jeu tourne SOUS DEBOGUEUR : il est plus lent, c est normal.
rem Journal : analysis\sonde_mode.txt
rem -----------------------------------------------------------------------
setlocal
cd /d "%~dp0.."

tasklist /fi "IMAGENAME eq vfes.exe" | find /i "vfes.exe" >nul
if not errorlevel 1 (
  echo.
  echo   Un vfes.exe tourne deja. Fermez-le, puis relancez.
  pause
  exit /b 1
)

if not exist "analysis" mkdir "analysis"

echo.
echo   ===================================================================
echo    VF5 -- sonde des modes et des sous-etats
echo   ===================================================================
echo.
echo   Dans le jeu : VF.TERMINAL ^> Customize ^> une donnee ^> exit without
echo   saving. Puis fermez le jeu.
echo.
py -3 tools\instrument.py run "runtime\media\vf5fs\vfes.exe" ^
    --cwd "runtime\media\vf5fs" ^
    --secondes 600 ^
    --journal "analysis\sonde_mode.txt" ^
    --bp vf5fs-pxd-w64-Retail_APM3.dll+0xDA9A0 ^
    --bp vf5fs-pxd-w64-Retail_APM3.dll+0xDA9C0 ^
    --bp-max 4000
echo.
echo   Journal : analysis\sonde_mode.txt
pause
endlocal
