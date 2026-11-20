@echo off
rem -----------------------------------------------------------------------
rem VF5 -- LA SONDE DE PLANTAGE DU COMBAT DU QUEST
rem
rem Double-cliquez. Le jeu demarre SOUS DEBOGUEUR : il est plus lent, c est
rem normal. Allez au combat du Quest et faites planter.
rem
rem   MENU > SCOREBOARDS > une salle > ENTREE > une borne > ENTREE
rem
rem CE QUE CA DONNE, ET POURQUOI C EST LA SEULE FACON HONNETE
rem
rem   Le journal du module (quest_journal.txt) dit que TOUT ce que nous
rem   posons est juste : les deux personnages, le decor, la force du CPU,
rem   le temps, les rounds, et le cas 1P/2P qui vaut enfin 0. Le sous-etat
rem   19 (VS) est atteint. Le plantage vient donc d APRES, dans le montage
rem   du combat lui-meme -- et sans adresse fautive, en parler serait
rem   deviner.
rem
rem   Cette sonde ecrit, au fil de l eau, dans quelle SECTION et a quelle
rem   ADRESSE l exception tombe : analysis\pister_plantage.txt
rem
rem   Si vous voulez continuer a essayer le reste du mode sans plantage,
rem   la touche T bascule le combat sur le SELECTEUR d arcade, la voie
rem   validee du 27/09.
rem -----------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- sonde de plantage du COMBAT DU QUEST
echo   ===================================================================
echo.
echo   MENU ^> SCOREBOARDS ^> une salle ^> ENTREE ^> une borne ^> ENTREE
echo.
py -3 tools\pister_plantage.py --secondes 600
echo.
echo   Journal : analysis\pister_plantage.txt
pause
endlocal
