@echo off
rem ---------------------------------------------------------------------------
rem MESURE : le reseau des bornes liees demarre-t-il ?
rem
rem Double-cliquez. Le apm.dll de substitution est reconstruit (il porte
rem desormais une vraie identite de borne), le build console est applique, le
rem jeu se lance et l'outil observe.
rem
rem   Laissez simplement tourner une minute sur l'ecran d'attract, puis fermez.
rem   AUCUNE TOUCHE n'est necessaire : le reseau se met en route tout seul,
rem   des le demarrage du moteur, sans qu'on entre dans un menu.
rem
rem Le jeu tourne au ralenti sous le debogueur : c'est normal.
rem
rem Releve au fil de l'eau : analysis\pister_link.txt
rem Bilan                  : analysis\pister_link_bilan.txt
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
echo Reconstruction du apm.dll de substitution (chaines en UTF-16)...
py -3 tools\gen_apm_stub.py --utf16
if errorlevel 1 (
  echo.
  echo La compilation du stub a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo Application du build console...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-mode --joueur2 --menu-fermer ^
    --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto ^
    --menu-exit --decor-perso trm >nul
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
py -3 tools\pister_link.py %*
echo.
pause
endlocal
