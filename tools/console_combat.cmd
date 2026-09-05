@echo off
rem ---------------------------------------------------------------------------
rem MODE CONSOLE + TRANSITION VERS LE COMBAT.
rem
rem Applique le jeu de correctifs complet (toujours a partir des .origine) puis
rem lance le jeu :
rem
rem   --mode 0            demarre en mode console (le menu, pas la borne)
rem   --menu-init         leve l'attente d'initialisation du menu
rem   --sousmenu      leve l'attente du classement
rem   --transition-game --sp-menu --sp-lancer   SINGLE PLAYER demande GAME/SELECTOR,
rem                       et la fin du selecteur demande VS au lieu du menu
rem   --dural --wxga --dural-grille   Dural dans la grille
rem   --resolution 1280 720 --langue --logo-japonais
rem
rem CE QU'IL FAUT ESSAYER, dans l'ordre (voir analysis/menu_console.md 10) :
rem   fleches                 deplacer le curseur
rem   sur la grille : A, puis T, puis R, puis Entree
rem     -> ce sont les QUATRE touches qui produisent un code de validation
rem        (codes logiques 8, 7, 9 et 7). Z, U, E sont les boutons de COMBAT
rem        (codes 100 a 103) et ne valident pas la grille.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."

echo Application des correctifs...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto
if errorlevel 1 (
  echo.
  echo ERREUR : le patcheur a refuse. Rien n'a ete lance.
  pause
  exit /b 1
)

echo.
cd /d "%~dp0..\runtime\media\vf5fs"
if not exist apm.dll (
  echo ERREUR : apm.dll manquant. Lancez d'abord construire_stub.cmd
  pause
  exit /b 1
)

echo Lancement... fenetre "Virtua Fighter 5 FS (PXD/64bit)".
echo.
echo   1. deux fois Entree pour arriver au menu console
echo   2. SINGLE PLAYER (premiere entree), valider
echo   3. sur la grille : valider avec A, T, R ou Entree
echo   4. MENER LE COMBAT JUSQU'AU BOUT : on doit revenir au MENU
echo      (et non a l'ecran-titre -- c'est le maillon 4)
echo   5. RELANCER UN COMBAT depuis le menu (la boucle est fermee)
echo   6. DOJO (quatrieme entree) : doit mener a l'entrainement
echo   -- POUR SORTIR D'UN MODE : ECHAP au clavier, ou BACK a la manette.
echo      Ramene au menu console.
echo   7. OFFLINE VERSUS : CLAVIER = joueur 1, MANETTE = joueur 2.
echo      Appuyer sur START DE LA MANETTE pour que le 2e joueur entre,
echo      puis regler et lancer. Les deux doivent bouger separement.
echo.
start "" vfes.exe
"%SystemRoot%\System32\timeout.exe" /t 6 /nobreak >nul 2>&1
"%SystemRoot%\System32\tasklist.exe" /fi "imagename eq vfes.exe" /nh | "%SystemRoot%\System32\findstr.exe" /i vfes >nul
if errorlevel 1 (
  echo Le jeu s'est arrete. Relancez avec lancer_vfes_debug.cmd pour voir pourquoi.
) else (
  echo Le jeu tourne.
)
echo.
pause
endlocal
