@echo off
rem ---------------------------------------------------------------------------
rem Regenere et recompile le apm.dll de substitution (57 exports).
rem
rem gcc vient de MSYS2. PIEGE : il n'est utilisable que si C:\msys64\mingw64\bin
rem est dans le PATH, sinon il ne trouve pas ses propres DLL et sort en erreur
rem SANS message. gen_apm_stub.py s'en charge lui-meme.
rem
rem La vraie apm.dll est conservee sous apm.reelle.dll.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
py -3 tools\gen_apm_stub.py
echo.
pause
endlocal
