@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LE MOVIE THEATER : QUELLE LIGNE LANCE UN FILM ? Double-cliquez.
rem
rem Frederic : " seule la 1ere ligne lance une video ". Cette sonde le mesure
rem sans personne devant l ecran. DEUX passes, environ trois minutes en tout :
rem
rem   1. LIGNE 0  -- le temoin. Elle est la seule a passer par le relais
rem      d ENTREE (0x1801DE369).
rem   2. LIGNE 11 -- " Ending movie VF5 Final Showdown ", celle qui joue
rem      vf5end.usm. Elle passe par le relais de VALIDATION (0x1801DE39F).
rem
rem Le validateur se coupe en deux a 0x1801DE367 : ligne 0 d un cote, toutes
rem les autres de l autre. Les deux captures cote a cote disent donc LEQUEL
rem des deux relais ne part pas -- c est ce qui manquait pour le savoir.
rem
rem Les captures :
rem   analysis\essai_film0_tNN.png     la ligne 0
rem   analysis\essai_film11_tNN.png    la ligne 11
rem ---------------------------------------------------------------------------
cd /d "%~dp0.."
echo.
echo   PASSE 1 sur 2 -- la ligne 0, le temoin
echo.
py -3 tools\essai_menu.py film0
echo.
echo   PASSE 2 sur 2 -- la ligne 11, celle de vf5end.usm
echo.
py -3 tools\essai_menu.py film11
echo.
pause
