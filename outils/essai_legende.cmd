@echo off
rem ---------------------------------------------------------------------------
rem ESSAI -- la legende du bas ne se superpose plus.
rem
rem Double-cliquez, rien a taper.
rem
rem C'est le build de console.cmd, plus une seule greffe : --legende-sousmenu.
rem
rem LE DEFAUT N'ETAIT PAS DE NOTRE FAIT : un build temoin sans --sousmenu
rem montrait la meme superposition. Il est natif a ce build d'arcade.
rem
rem   Deux fois Entree -> menu console
rem
rem   A ESSAYER :
rem     1. Sur MAIN MENU, promenez le curseur : la legende du bas doit suivre
rem        l'entree choisie, comme avant.
rem     2. Entree sur SINGLE PLAYER : le bandeau ne doit plus porter QUE la
rem        legende du sous-menu -- plus de texte du menu principal dessous.
rem     3. W pour revenir : la legende du menu principal doit revenir.
rem     4. Meme chose sur OFFLINE VERSUS, DOJO, TERMINAL, OPTIONS.
rem
rem   CE QUI RESTE : le TITRE se superpose encore -- " MAIN MENU " transparait
rem   sous " SINGLE PLAYER ". C'est un second defaut, distinct, sur la scene
rem   d'en-tete (garde 0x1801E0DA5, scene [page+0x240]). Non traite ici.
rem
rem   Si quelque chose casse : tools\console.cmd ne porte pas cette greffe.
rem
rem   Touches : fleches, Entree = VALIDER, W = ANNULER, Echap = quitter le mode.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
rem apm.dll en ASCII : les mesures reseau le construisent en UTF-16, et le jeu
rem plante alors au demarrage.
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
    --options-sans-howto --menu-exit --legende-sousmenu --decor-perso trm >nul
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   Ouvrez un sous-menu : le bandeau du bas ne doit plus porter qu'un texte.
echo   W pour revenir : la legende du menu principal doit revenir.
echo.
cd /d "%~dp0..\runtime\media\vf5fs"
start "" vfes.exe
endlocal
