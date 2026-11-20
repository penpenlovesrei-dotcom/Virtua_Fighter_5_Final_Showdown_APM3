@echo off
rem ---------------------------------------------------------------------------
rem ESSAI -- Score Attack et License Challenge lancent LEUR mode.
rem
rem C'est le build complet de `console.cmd`, plus une seule chose : ces deux
rem modes ne sont plus lances par leur validateur, mais par leur propre mise a
rem jour, juste apres que le jeu y a pose le mode de jeu et les reglages.
rem
rem CE QU'IL FAUT REGARDER
rem
rem   SINGLE PLAYER -> Score Attack -> valider
rem     . le combat part-il ?
rem     . est-ce bien Score Attack -- SEPT combats d'affilee, pas de remise a
rem       zero du combattant entre deux, et pas de film de fin ?
rem
rem   SINGLE PLAYER -> License Challenge -> valider
rem     . le combat part-il ?
rem     . l'ecran de resultat de licence apparait-il a la fin ?
rem
rem   Arcade et OFFLINE VERSUS ne sont pas touches : ils doivent marcher comme
rem   avant. S'ils ont change, c'est un defaut a signaler.
rem
rem SI RIEN NE SE LANCE sur ces deux modes, c'est le risque connu et assume :
rem l'animation de sortie de la page ne retombe pas dans ce build, donc la mise
rem a jour n'atteint jamais le site de la greffe. Ce n'est pas une regression du
rem reste -- `tools\console.cmd` reste le build de reference, intact.
rem
rem   Touches : fleches, Entree = VALIDER, W = ANNULER, X C V = croix rond
rem             triangle, Espace = SELECT, Echap = quitter le mode.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-mode --joueur2 --menu-fermer ^
    --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto ^
    --menu-exit --decor-perso trm
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   Deux fois Entree -^> menu console -^> SINGLE PLAYER
echo   Essayez Score Attack, puis License Challenge.
echo.
cd /d "%~dp0..\runtime\media\vf5fs"
start "" vfes.exe
endlocal
