@echo off
rem Decompile une ou plusieurs fonctions du moteur, par adresse.
rem Exemple : DECOMPILER.cmd 0x180171F40
setlocal
cd /d "%~dp0"
if "%~1"=="" goto demande
py -3 mesures/analyser.py --decompile %*
goto fin
:demande
set /p ADR=Adresse (ex. 0x180171F40) :
if "%ADR%"=="" goto fin
py -3 mesures/analyser.py --decompile %ADR%
:fin
echo.
pause
