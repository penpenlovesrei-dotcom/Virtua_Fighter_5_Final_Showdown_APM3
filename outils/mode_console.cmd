@echo off
rem -------------------------------------------------------------------
rem VF5 FS -- LE MODE DE JEU hors du jeu. Double-cliquez.
rem
rem Le mode se choisit normalement DANS le jeu :
rem   . aller en arcade  : OPTIONS ^> Settings, ligne "Game Mode"
rem   . revenir en console : le MENU TEST, derniere ligne "CONSOLE MODE"
rem
rem CE QUI OUVRE LE MENU TEST, et c etait la question du 2026-10-07 :
rem `Sequence_isTest()`, un export de NOTRE apm.dll. Le moteur l appelle
rem par vtable[0x1A0] d un objet que vfes.exe fournit, et s il rend vrai
rem 0x1800DDA80 demande la tete 9 = APM3_TESTMODE. Il est pilote par
rem "test = 1" dans runtime\media\vf5fs\apm_entrees.txt, relu A CHAUD.
rem Aucun correctif binaire la-dedans : la porte etait chez nous.
rem
rem Ce lanceur fait les deux gestes sans editer de fichier a la main.
rem -------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
set "MODFIC=runtime\media\vf5fs\ram\mode.txt"
set "ENTFIC=runtime\media\vf5fs\apm_entrees.txt"
echo.
echo   ===================================================================
echo    VF5 -- mode de jeu et menu TEST
echo   ===================================================================
echo.
tasklist /fi "IMAGENAME eq vfes.exe" 2>nul | findstr /i "vfes.exe" >nul
if not errorlevel 1 (
  echo   vfes.exe TOURNE. Fermez le jeu d abord : le mode est lu au
  echo   demarrage, et le changer pendant qu il tourne ne ferait rien.
  pause
  exit /b 1
)
if not exist "runtime\media\vf5fs\ram" mkdir "runtime\media\vf5fs\ram"
if exist "%MODFIC%" (
  for /f "usebackq tokens=1" %%a in ("%MODFIC%") do echo   mode en place : %%a
) else (
  echo   mode en place : console ^(aucun fichier^)
)
echo.
echo   1 = repasser en MODE CONSOLE
echo   2 = demarrer dans le MENU TEST ^(test = 1^)
echo   3 = ne plus demarrer dans le menu TEST ^(test = 0^)
echo.
set "REP="
set /p "REP=  Votre choix (1/2/3, Entree pour annuler) : "
if "%REP%"=="1" goto console
if "%REP%"=="2" goto test_on
if "%REP%"=="3" goto test_off
echo   rien fait.
goto fin

:console
echo console> "%MODFIC%"
echo.
echo   mode.txt porte desormais : console
echo   Relancez tools\item_porte.cmd : il relira ce fichier.
goto fin

:test_on
py -3 -c "import io,sys; p=sys.argv[1]; s=io.open(p,encoding='latin-1').read(); io.open(p,'w',encoding='latin-1',newline='').write(s.replace('test    = 0','test    = 1',1))" "%ENTFIC%"
echo.
echo   test = 1 : le jeu demarrera dans le MENU TEST.
echo   Sa derniere ligne est "CONSOLE MODE" -- le curseur y est deja,
echo   parce que le menu s ouvre sur sa DERNIERE ligne. Validez avec
echo   la touche TEST ^(F1^).
goto fin

:test_off
py -3 -c "import io,sys; p=sys.argv[1]; s=io.open(p,encoding='latin-1').read(); io.open(p,'w',encoding='latin-1',newline='').write(s.replace('test    = 1','test    = 0',1))" "%ENTFIC%"
echo.
echo   test = 0 : demarrage normal.
goto fin

:fin
echo.
pause
endlocal
