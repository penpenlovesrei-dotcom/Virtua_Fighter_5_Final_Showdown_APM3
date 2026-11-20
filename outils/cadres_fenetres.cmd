@echo off
rem ---------------------------------------------------------------------------
rem LE CATALOGUE DES CADRES DU MOTEUR.
rem
rem Toute fenetre du jeu est un RANG dans la table 0x18052E680, et chaque rang
rem nomme une composition AET deja dessinee -- cadre, fond et ancres compris.
rem Ouvrir une fenetre, c'est choisir un numero : il n'y a rien a redessiner.
rem
rem Sans argument : la table entiere (rang, planche, nom).
rem Avec des noms : leur geometrie -- le cadre, l'INTERIEUR utilisable, et la
rem composition qui sert de fond.
rem
rem   cadres_fenetres.cmd
rem   cadres_fenetres.cmd choice_win_08 cmn_win_xxl_01 term_win
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
py -3 tools\cadres_fenetres.py %*
echo.
pause
endlocal
