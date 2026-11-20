@echo off
rem Reconstruit la base Ghidra du moteur APM3 puis mesure la couverture.
rem Premiere fois : environ deux minutes. Ensuite, instantane.
setlocal
cd /d "%~dp0"
py -3 mesures/analyser.py %*
echo.
pause
