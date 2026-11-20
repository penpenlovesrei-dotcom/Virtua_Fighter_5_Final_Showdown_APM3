@echo off
rem -----------------------------------------------------------------------
rem VF5 FS -- LE MOTEUR LIT-IL NOS FICHIERS D ECLAIRAGE ?
rem
rem Double-cliquez, puis CHARGEZ LE DECOR D AOI en version R (le
rem sanctuaire, barre espace sur sa case). Vous avez 180 secondes.
rem
rem La sonde met un point d arret sur CreateFileW/A et journalise TOUT
rem chemin contenant light_param, fog_ ou .ibl. Elle ne touche pas au
rem clavier : elle regarde.
rem
rem CE QU ON CHERCHE, ET POURQUOI
rem
rem   Le brouillard d un decor vient de rom/light_param/fog_CODE.txt.
rem   Celui de 2008 allume son GROUPE 1 (la bande de tout proche,
rem   linear -2.5 a 1.0) ; Final Showdown l a eteint sur le sanctuaire.
rem   Quatre decors du jeu s en servent quand meme (du2, du3, du5, slk),
rem   donc le moteur sait le faire.
rem
rem   Il reste UNE question, et une seule : le moteur ouvre-t-il
rem   fog_jn5.txt ? Nos fichiers sont poses LIBRES, leur nom n est pas
rem   dans vf5fs_data.par -- et tous les chargeurs ne retombent pas sur
rem   le disque (obj_db.bin ne le faisait pas, cf REPRISE (42)).
rem
rem   Si fog_jn5.txt apparait dans le journal, la cause est ailleurs.
rem   S il n apparait pas, elle est la.
rem
rem Journal : analysis	racer_eclairage.txt
rem -----------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- le moteur lit-il nos fichiers d eclairage ?
echo   ===================================================================
echo.
echo   Chargez le decor d AOI en version R. 180 secondes.
echo.
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32	imeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools	racer_fichiers.py --secondes 180 --filtre light_param,fog_,.ibl
echo.
echo   Journal : analysis	racer_eclairage.txt
pause
endlocal
