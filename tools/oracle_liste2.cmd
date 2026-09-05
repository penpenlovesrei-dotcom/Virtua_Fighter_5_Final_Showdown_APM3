@echo off
rem ---------------------------------------------------------------------------
rem Fait arbitrer les gestionnaires de mothead par le JEU EN MARCHE.
rem
rem Pose un point d'arret a l'entree du gestionnaire et un autre sur son adresse
rem de retour, et compare 12 Ko de ROB entre les deux : les mots changes sont
rem exactement ce que le gestionnaire a ecrit, dans les conditions reelles du
rem combat. C'est ce qui fait passer un code de LIKELY a SUPPORTED.
rem
rem Le son du jeu est coupe (par processus ; le volume general n'est pas touche).
rem
rem Arguments optionnels :
rem   oracle_liste2.cmd 12,17,29          les codes a surveiller
rem   oracle_liste2.cmd 46,54 1           ... de la LISTE 1 au lieu de la liste 2
rem
rem Compter environ quatre minutes. Journal : analysis\oracle_liste2_vivant.txt
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
set CODES=%1
if "%CODES%"=="" set CODES=12,17,29,33
set LISTE=%2
if "%LISTE%"=="" set LISTE=2
py -3 tools\oracle_liste2_vivant.py --codes %CODES% --liste %LISTE% ^
   --secondes 240 --a 55 --coups 4 --scenario tools\scenarios\combat_long.txt
echo.
pause
endlocal
