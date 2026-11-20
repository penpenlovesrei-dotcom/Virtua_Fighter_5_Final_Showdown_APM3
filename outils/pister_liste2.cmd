@echo off
rem ---------------------------------------------------------------------------
rem Prend le repartiteur de la liste 2 de mothead sur le fait, dans un combat.
rem
rem Lance le jeu sous debogueur, le mene au combat par le scenario d'entrees,
rem puis pose des points d'arret sur MothRunList2 et sur les gestionnaires des
rem codes demandes. A chaque passage il decode l'entree (code, trame) et la
rem charge utile.
rem
rem Argument optionnel : les codes de liste 2 a surveiller (defaut 0,9).
rem   pister_liste2.cmd 0,9
rem   pister_liste2.cmd 26,34
rem
rem Compter environ deux minutes. Journal complet dans
rem analysis\pistage_liste2.txt.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
set CODES=%1
if "%CODES%"=="" set CODES=0,9
py -3 tools\pister_liste2.py --secondes 110 --a 55 --bp-max 4 --codes %CODES%
echo.
pause
endlocal
