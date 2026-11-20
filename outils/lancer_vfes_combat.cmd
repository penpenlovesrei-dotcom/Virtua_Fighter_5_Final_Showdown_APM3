@echo off
rem ---------------------------------------------------------------------------
rem Lance vfes.exe et le mene TOUT SEUL jusqu'a un combat.
rem
rem Le apm.dll de substitution tient les boutons : il joue le scenario ecrit
rem dans apm_entrees.txt (deux appuis sur START, code 7). Aucun clavier n'est
rem necessaire, et le fichier peut etre modifie PENDANT que le jeu tourne :
rem le stub le relit toutes les 250 ms.
rem
rem Pour appuyer a la main pendant une partie :  presser.cmd 7
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0..\runtime\media\vf5fs"

if not exist apm.dll (
  echo ERREUR : apm.dll manquant. Lancez d'abord construire_stub.cmd
  pause
  exit /b 1
)
if not exist apm_entrees.txt (
  echo ERREUR : apm_entrees.txt manquant. Lancez d'abord construire_stub.cmd
  pause
  exit /b 1
)

echo Dossier   : %CD%
echo Scenario  : apm_entrees.txt (START a 25 s, puis a 33 s)
echo.
start "" vfes.exe
echo Attente de 60 secondes : chargement, selection, puis le vol de camera

rem ping et non timeout : timeout refuse de tourner quand l'entree

rem standard est redirigee, et rend la main aussitot sans attendre.

"%SystemRoot%\System32\ping.exe" -n 61 127.0.0.1 >nul
echo.
echo Le combat devrait avoir commence. Capture d'ecran :
cd /d "%~dp0.."
py -3 tools\capture_fenetre.py analysis\combat.png
echo.
pause
endlocal
