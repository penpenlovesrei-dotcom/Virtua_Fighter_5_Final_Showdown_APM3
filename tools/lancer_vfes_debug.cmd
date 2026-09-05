@echo off
rem ---------------------------------------------------------------------------
rem Lance vfes.exe SOUS DEBOGUEUR et journalise :
rem   - les DLL chargees avec leur base,
rem   - chaque exception avec son type C++ demangle,
rem   - chaque appel au stub apm.dll (via OutputDebugString).
rem
rem Argument optionnel : duree en secondes (60 par defaut).
rem   lancer_vfes_debug.cmd 30
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
set DUREE=%1
if "%DUREE%"=="" set DUREE=60

echo Dossier : %CD%
echo Duree   : %DUREE% s, puis le processus est arrete.
echo.
py -3 tools\instrument.py run runtime\media\vf5fs\vfes.exe --secondes %DUREE% --silencieux
echo.
pause
endlocal
