@echo off
rem ---------------------------------------------------------------------------
rem Fait arbitrer les decodages par le moteur lui-meme : la DLL du build APM3
rem n'a que des imports systeme, elle se charge dans un processus Python.
rem
rem   1. rob_cmn_mottbl.bin  -> doit donner 14157/14157 identiques
rem   2. les 84 gestionnaires de codes de mothead sur un faux combattant
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo === 1. rob_cmn_mottbl.bin ===
py -3 tools\oracle_mottbl.py
echo.
echo === 2. les 84 gestionnaires de codes ===
py -3 tools\oracle_handlers.py
echo.
pause
endlocal
