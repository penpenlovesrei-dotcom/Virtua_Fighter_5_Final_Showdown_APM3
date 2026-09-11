@echo off
rem -----------------------------------------------------------------------
rem VF5 FS -- LA SONDE DE PLANTAGE
rem
rem Double-cliquez, JOUEZ NORMALEMENT, et faites planter le jeu.
rem La sonde ne touche pas au clavier : elle regarde.
rem
rem Ce qu elle ecrit, au fil de l eau, dans
rem analysis\pister_plantage.txt :
rem
rem   . chaque DECOR demande, au moment ou il est demande (le dernier
rem     avant le plantage nomme le decor fautif) ;
rem   . chaque exception : code, adresse, et DANS QUELLE SECTION elle
rem     tombe -- si c est .decors, on dit dans quelle de nos tables et a
rem     quel offset ;
rem   . l adresse lue ou ecrite, situee elle aussi ;
rem   . les registres et le code desassemble autour de RIP ;
rem   . les adresses de retour applicatives encore sur la pile.
rem
rem Le jeu se ferme seul au bout de cinq minutes. Pour plus longtemps :
rem   py -3 tools\pister_plantage.py --secondes 900
rem
rem IMPORTANT : fermez toute partie en cours AVANT de lancer -- la sonde
rem refuse de demarrer si un vfes.exe tourne deja.
rem -----------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- sonde de plantage
echo   ===================================================================
echo.
echo   Le jeu va demarrer SOUS DEBOGUEUR : il est plus lent, c est normal.
echo   Jouez, et faites planter. Tout est ecrit au fil de l eau.
echo.
py -3 tools\pister_plantage.py --secondes 300
echo.
echo   Journal : analysis\pister_plantage.txt
pause
endlocal
