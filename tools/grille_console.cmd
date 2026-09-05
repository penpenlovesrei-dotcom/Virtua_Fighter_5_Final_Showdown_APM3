@echo off
setlocal
set "RACINE=C:\Users\frede\Desktop\VF5RE"
cd /d "%RACINE%"

echo.
echo   ================================================================
echo      VF5 FS  --  GRILLE DE SELECTION CONSOLE, EN DIRECT
echo   ================================================================
echo.
echo   Le menu principal n'est PAS emprunte : sa machine a etats est du
echo   code mort dans ce build (le drapeau [menu+0x2A09] qui l'ouvre
echo   n'est ecrit nulle part -- deux lecteurs, zero ecrivain). Valider
echo   une entree ne peut donc rien declencher.
echo.
echo   On devie donc la transition qui mene a CS_AUTOLOAD vers
echo   SELECTOR sous la tete GAME, AVANT que la page de menu existe.
echo.
echo   is_dural_unlocked est pose : la grille doit compter 20 cases au
echo   lieu de 18 (0x1801D0BD5 : test r8b,4 -> 0x14 au lieu de 0x12).
echo   REGARDER S'IL Y A UNE VINGTIEME CASE.
echo.

py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais --mode 0 --menu-init --sousmenu --dural
if errorlevel 1 goto :fin

echo.
echo   ----------------------------------------------------------------
echo    Le jeu tourne sous debogueur (necessaire pour devier), donc au
echo    ralenti : environ 25 images par seconde au lieu de 60. Normal.
echo.
echo    Le scenario appuie sur START a 20, 24 et 28 secondes. Ensuite
echo    le clavier est actif : fleches, Entree.
echo   ----------------------------------------------------------------
echo.

py -3 tools\tracer_etats.py --devier 5 17 --tete 2 --secondes 600 --scenario tools\scenarios\console_start.txt --son

:fin
pause
