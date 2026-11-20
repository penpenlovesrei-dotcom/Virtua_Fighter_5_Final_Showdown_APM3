@echo off
rem ---------------------------------------------------------------------------
rem Coupe le son du seul vfes.exe. Le volume general de Windows n'est pas touche :
rem Windows tient un volume par session audio, et on ne met en sourdine que celle
rem dont l'identifiant de processus est celui du jeu.
rem
rem   muet.cmd            met en sourdine
rem   muet.cmd rendre     lui rend le son
rem
rem Les outils de pistage le font deja tout seuls ; ce lanceur sert quand on a
rem lance le jeu a la main.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
if /i "%1"=="rendre" (
  py -3 tools\muet.py --rendre
) else (
  py -3 tools\muet.py --surveiller 20
)
echo.
pause
endlocal
