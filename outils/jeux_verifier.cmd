@echo off
rem ---------------------------------------------------------------------------
rem LES JEUX DE LA BORNE -- controle
rem
rem Double-cliquez. Dit, pour chaque jeu de borne\jeux\, si la jaquette et la
rem video sont au bon format, et si l executable est trouve. NE MODIFIE RIEN.
rem
rem Les formats attendus, et pourquoi :
rem
rem   jaquette.png   CARREE, 512x512 conseille, 384 minimum. Le code de l APM3
rem                  pose ses icones sur un carre de 256 px, et agrandit de
rem                  moitie celle du centre : 256 x 1,5 = 384 px a l ecran.
rem
rem   demo.mp4       H.264 + AAC, 16:9, 1280x720 suffit. C est ce que le
rem                  lecteur video de Windows lit sans rien installer. Le
rem                  H.265 est refuse : son codec est PAYANT sur Windows 11.
rem
rem   jeu.json       facultatif : titre, chemin de l executable, editeur, annee.
rem                  Sans lui, le nom du dossier sert de titre et le premier
rem                  executable du dossier est lance.
rem
rem Pour remettre au format ce qui ne l est pas : tools\jeux_convertir.cmd
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
if not exist "tools\jeux.py" (
  echo INTROUVABLE : tools\jeux.py
  pause
  exit /b 1
)
py -3 tools\jeux.py
echo.
pause
endlocal
