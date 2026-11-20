@echo off
rem ---------------------------------------------------------------------------
rem VF5 -- IMPORTER LA FINAL SHOWDOWN CONSOLE DANS GHIDRA. Double-cliquez.
rem UNE SEULE FOIS : ensuite le projet reste, et la decompilation est immediate.
rem
rem POURQUOI. Jusqu'au 2026-10-05 je n'avais que DESASSEMBLE cette version --
rem tools\x360_ppc.py, capstone sur l'image, instruction par instruction.
rem Ghidra ne portait que la console de 2007 ^(projet vf5x360_2007, celle du
rem mode Quest^) ; le dossier ghidra\vf5fs_x360 etait VIDE. Frederic : "comment
rem tu as decompile la version 360 jusqu a present sans ghidra ?" -- je ne
rem l'avais pas decompilee, et la distinction compte.
rem
rem CE QUE FAIT L'IMPORT, et aucun parametre n'est invente :
rem   . binaire BRUT a 0x82000000, PowerPC:BE:64:A2ALT-32addr. L'image sort
rem     deja chargee du decompresseur, donc la RVA vaut l'offset ;
rem   . les fonctions creees depuis .pdata AVANT l'analyse ^(PdataX360.java^) :
rem     0x8217DA00, 0x1D8F0 octets = 15 086 entrees, mesure par
rem     tools\x360_ppc.py sections ;
rem   . les routines __savegprlr_N / __restgprlr_N neutralisees par un call
rem     fixup ^(SauvegardesX360.java^). Sans lui, Ghidra en fait des fonctions
rem     qui ne reviennent pas et perd tout ce qui suit l'appel.
rem     LEURS ADRESSES NE SE RECOPIENT PAS DE 2007 : tools\x360_savegpr.py les
rem     trouve dans CETTE image ^(la plus longue suite de std rN,-M^(r1^)^), et
rem     les queues confirment -- stw r12,-8^(r1^) ; blr d'un cote, lwz r12 ;
rem     mtlr r12 ; blr de l'autre. DIX-HUIT entrees ici, r14 a r31, contre
rem     seize en 2007.
rem
rem C'EST LONG : quinze mille fonctions a analyser. Laissez la fenetre
rem tranquille ; elle dit quand c'est fini.
rem
rem ENSUITE, pour decompiler une fonction de la console :
rem     py -3 tools\decomp.py --gen fs360 0x82235068
rem ^(et --gen x360 reste la console de 2007 : une image ne se nomme pas par
rem son dossier^)
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    IMPORT DE LA FINAL SHOWDOWN CONSOLE DANS GHIDRA
echo   ===================================================================
echo.
py -3 tools\importer_x360_fs.py %*
echo.
pause
endlocal
