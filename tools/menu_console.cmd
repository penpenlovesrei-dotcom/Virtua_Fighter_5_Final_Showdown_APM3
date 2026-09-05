@echo off
setlocal
set "RACINE=C:\Users\frede\Desktop\VF5RE"
set "JEU=%RACINE%\runtime\media\vf5fs"
cd /d "%RACINE%"

echo.
echo   ================================================================
echo      VF5 FS  --  MODE CONSOLE  (game_mode = 0)
echo   ================================================================
echo.
echo   Correctifs appliques :
echo      720p, anglais, logo japonais
echo      mode console
echo      menu-init    : l'attente d'initialisation (bouchon 0x180029FB0)
echo      menu-ranking : l'attente de la scene RANKING, qui ne finit jamais
echo      dural        : is_dural_unlocked -- la grille passe de 18 a 20 cases
echo.
echo   NE PAS ajouter --menu-service : mesure comme une regression,
echo   le menu redevient vide (le bloc des tics n'est plus atteint).
echo.

py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais --mode 0 --menu-init --sousmenu --dural
if errorlevel 1 goto :fin

copy /y "%RACINE%\tools\scenarios\console_start.txt" "%JEU%\apm_entrees.txt" >nul

echo.
echo   ----------------------------------------------------------------
echo    Le scenario appuie sur START tout seul a 20, 24 et 28 secondes
echo    pour franchir PRESS START BUTTON, l'ecran de sauvegarde et
echo    l'avertissement. Le clavier reste actif par-dessus.
echo.
echo    CLAVIER   fleches = directions      Entree = START
echo              W = GUARD  X = PUNCH  C = KICK
echo   ----------------------------------------------------------------
echo.

cd /d "%JEU%"
start "" "vfes.exe"
cd /d "%RACINE%"

echo   Jeu lance, a pleine vitesse (pas de debogueur).
echo.
:fin
pause
