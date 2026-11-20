@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- SORTIR LES IMAGES 2D DU JEU EN PNG. Double-cliquez.
rem
rem Il ecrit les 171 textures 2D dans HD_TEXTURES\EXTRACTED\2D, une par
rem PNG, a l endroit, puis ouvre le dossier.
rem
rem LE NOM DE CHAQUE PNG EST SON ADRESSE :   <archive>__texNN.png
rem C est ce nom qu il faut redonner a une version HD pour qu elle retrouve sa
rem place -- on repose avec tools\textures_hd.cmd.
rem
rem Relancer est sans danger : les PNG sont simplement reecrits. Rien dans le
rem jeu n est touche par cet outil, il ne fait que LIRE.
rem ---------------------------------------------------------------------------
cd /d "%~dp0.."
py -3 tools\textures_hd.py --sortir
echo.
start "" "%CD%\HD_TEXTURES\EXTRACTED\2D"
echo   Le dossier est ouvert.
echo.
pause
