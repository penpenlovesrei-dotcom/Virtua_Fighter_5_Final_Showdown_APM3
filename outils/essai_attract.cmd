@echo off
rem ---------------------------------------------------------------------------
rem ESSAI -- l'animation de titre LONGUE, en mode console.
rem
rem Double-cliquez, rien a taper, et NE TOUCHEZ A RIEN au demarrage.
rem
rem C'est le build de console.cmd, plus une seule greffe : --attract-long.
rem
rem CE QU'ON ATTEND, apres les logos SEGA et CRIWARE :
rem   Akira qui enchaine des mouvements, le titre en 3D derriere, un mouvement
rem   de camera qui finit sur l'ecran-titre classique.
rem   C'est ce que le mode BORNE joue deja ; le mode console prenait la version
rem   courte (logo_vf5_short) au lieu de la longue (logo_vf5).
rem
rem SI CA NE CHANGE RIEN : dites-le, le choix d'animation n'est alors pas le
rem seul aiguillage, et il faudra regarder la phase 2 du titre (0x1800DD930).
rem
rem SI CA CASSE : tools\console.cmd ne porte pas cette greffe.
rem
rem   Touches : Entree = VALIDER, W = ANNULER, Echap = quitter le mode.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\gen_apm_stub.py >nul
if errorlevel 1 (
  echo.
  echo La compilation du apm.dll a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring ^
    --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre ^
    --options-sans-howto --menu-exit --legende-sousmenu --attract-long ^
    --decor-perso trm >nul
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   Laissez tourner apres les logos : la sequence doit se jouer seule.
echo.
cd /d "%~dp0..\runtime\media\vf5fs"
start "" vfes.exe
endlocal
