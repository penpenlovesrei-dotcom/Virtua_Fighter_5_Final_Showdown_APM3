@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LES REGLAGES D'OPTIONS TIENNENT-ILS ? Double-cliquez, rien a taper.
rem
rem Ce lecteur ne lance rien et ne modifie rien. Il montre ce que apm.dll a
rem enregistre dans runtime\media\vf5fs\ram\options.bin, et les lignes OPT du
rem journal.
rem
rem L'ESSAI, dans l'ordre :
rem   1. lancez le jeu par tools\item_porte.cmd (il recompile apm.dll)
rem   2. OPTIONS ^> Settings : changez un volume, et Tips
rem   3. quittez par EXIT GAME
rem   4. double-cliquez CE fichier : les valeurs changees doivent y etre
rem   5. relancez le jeu : OPTIONS ^> Settings doit les retrouver, et le
rem      journal porter " OPT    reglages relus de ... "
rem
rem Ce qui est enregistre, et pourquoi exactement cela : voir le long
rem commentaire " LES REGLAGES D OPTIONS, QUI NE TENAIENT PAS " dans
rem tools\gen_apm_stub.py. Le moteur designe lui-meme le bloc, par son
rem predicat " c'est sale " en 0x1801B7AC0.
rem
rem Se coupe par " sauvegarde = 0 " dans apm_entrees.txt, comme la
rem personnalisation.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
py -3 tools\options_bin.py
echo.
pause
endlocal
