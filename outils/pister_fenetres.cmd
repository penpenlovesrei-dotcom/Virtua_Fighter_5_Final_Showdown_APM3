@echo off
rem ---------------------------------------------------------------------------
rem Repond a "qui lit les 32 fenetres temporelles de l'etat de mouvement".
rem
rem Lance le jeu sous debogueur, le mene au combat par le scenario d'entrees,
rem pose un point d'arret sur MothApplyRecord pour y lire le ROB, puis arme des
rem points d'arret MATERIELS sur les fenetres et releve chaque acces.
rem
rem Argument optionnel : les offsets a surveiller (defaut : la fenetre 0).
rem   pister_fenetres.cmd 0x154,0x158,0x15C
rem   pister_fenetres.cmd 0x1C0,0x1C4,0x1C8      (fenetre 9)
rem
rem Compter environ deux minutes et demie. Journal complet dans
rem analysis\pistage_fenetres.txt.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
set OFFSETS=%1
if "%OFFSETS%"=="" set OFFSETS=0x154,0x158,0x15C
py -3 tools\pister_etat.py --scenario tools\scenarios\combat_martelage.txt ^
   --secondes 135 --a 55 --dr-max 40 --offsets %OFFSETS%
echo.
pause
endlocal
