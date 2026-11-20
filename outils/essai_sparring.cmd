@echo off
rem ---------------------------------------------------------------------------
rem ESSAI -- SPECIAL SPARRING lance-t-il enfin son combat ?
rem
rem Double-cliquez, rien a taper.
rem
rem C'est le build de console.cmd, plus une seule greffe : --sp-sparring.
rem Tout le reste est identique, pour que ce qui marche deja serve de temoin.
rem
rem   Deux fois Entree -> menu console -> SINGLE PLAYER
rem
rem   A ESSAYER, dans cet ordre :
rem     1. Arcade              doit toujours lancer le combat  (temoin)
rem     2. Score Attack        idem                            (temoin)
rem     3. License Challenge   idem                            (temoin)
rem     4. Special Sparring    <-- CE QUI EST EN JEU
rem
rem   Si les trois temoins marchent encore et que Special Sparring lance, la
rem   greffe est bonne. S'ils cassent, c'est la greffe qu'il faut retirer :
rem   relancez tools\console.cmd, qui ne la porte pas.
rem
rem   Touches : fleches, Entree = VALIDER, W = ANNULER, X C V = croix rond
rem             triangle, Espace = SELECT, Echap = quitter le mode.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
rem apm.dll en ASCII : les mesures reseau le construisent en UTF-16, et le jeu
rem plante alors au demarrage. Cet essai doit partir d'un build jouable.
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
    --options-sans-howto --menu-exit --decor-perso trm >nul
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   SINGLE PLAYER -^> les quatre lignes.
echo   Les trois premieres sont les temoins ; la quatrieme est l'essai.
echo.
cd /d "%~dp0..\runtime\media\vf5fs"
start "" vfes.exe
endlocal
