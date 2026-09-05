@echo off
rem ---------------------------------------------------------------------------
rem Presse un ou plusieurs boutons dans le vfes.exe DEJA LANCE, et capture.
rem
rem   presser.cmd 7            appuie sur START
rem   presser.cmd 9,10         deux codes a la fois
rem   presser.cmd rien         relache tout
rem
rem Passe par apm_entrees.txt, que le stub relit toutes les 250 ms : ni
rem recompilation, ni relance du jeu.
rem
rem ATTENTION : cela REMPLACE le scenario en place par un scenario minimal.
rem Pour retrouver la sequence qui mene au combat, relancez construire_stub.cmd.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
if "%1"=="" (
  echo Usage : presser.cmd ^<codes^>     par exemple  presser.cmd 7
  pause
  exit /b 1
)
if /i "%1"=="rien" (
  py -3 tools\presser.py --relacher
) else (
  py -3 tools\presser.py %1 --duree 400 --attendre 2 --apres analysis\presser.png
)
echo.
pause
endlocal
