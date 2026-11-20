@echo off
rem ---------------------------------------------------------------------------
rem Essayer N'IMPORTE LEQUEL des 41 decors dans l'ecran TERMINAL.
rem
rem Double-cliquez : la liste s'affiche et le lanceur DEMANDE le nom.
rem (Pour les deux cas courants, prenez plutot decor_TRM.cmd / decor_TS2.cmd.)
rem
rem ATTENTION -- corrige le 2026-09-05. Cet ecran demande DEUX choses, chacune
rem avec son propre index en dur : la GEOMETRIE (0x1801C4DA6, via 0x18018FCF0)
rem et l'ECLAIRAGE (0x1801C4DCB, via 0x1800D7130). Jusqu'ici seul l'eclairage
rem etait patche -- d'ou trois essais "sans aucune difference". L'option
rem change desormais les deux.
rem ---------------------------------------------------------------------------
setlocal
set "DECOR=%~1"
if not "%DECOR%"=="" goto lancer

echo.
echo   LES 41 DECORS
echo.
echo     0 tst    1 ts2    2 ts3    3 wht    4 ban    5 ter    6 nyc    7 cas
echo     8 riv    9 jin   10 sin   11 djo   12 umi   13 hai   14 are   15 slk
echo    16 yuk   17 tak   18 aur   19 bar   20 tan   21 du1   22 du2   23 du3
echo    24 du4   25 du5   26 trm   27 cid   28 trs   39 gym   40 smo
echo    29..38   evo00..evo09
echo.
echo   trm = le decor "terminal"      ts2 = ce que charge le jeu d'origine
echo.
set /p "DECOR=Quel decor ? (nom ou numero, Entree seule pour annuler) : "
if "%DECOR%"=="" (
  echo Annule.
  "%SystemRoot%\System32\timeout.exe" /t 2 >nul 2>&1
  exit /b 0
)

:lancer
call "%~dp0_decor_commun.cmd" %DECOR%
endlocal
