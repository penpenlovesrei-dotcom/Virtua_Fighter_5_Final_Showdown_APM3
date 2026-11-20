@echo off
rem ---------------------------------------------------------------------------
rem LES JEUX DE LA BORNE -- conversion au bon format
rem
rem Double-cliquez. Reprend chaque jaquette et chaque video de borne\jeux\ qui
rem n est pas au format, et la convertit :
rem
rem   les images  ->  jaquette.png    512x512, sans deformer (bandes noires)
rem   les videos  ->  demo.mp4        H.264 + AAC, 1280 de large, 30 images/s
rem
rem VOS ORIGINAUX SONT GARDES, renommes _source_jaquette.png et
rem _source_demo.mp4 dans le meme dossier. Rien n est efface.
rem
rem La conversion utilise ffmpeg de votre MSYS2 (C:\msys64\mingw64\bin).
rem Une video de plusieurs minutes prend une minute ou deux.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
if not exist "tools\jeux.py" (
  echo INTROUVABLE : tools\jeux.py
  pause
  exit /b 1
)
if not exist "C:\msys64\mingw64\bin\ffmpeg.exe" (
  echo INTROUVABLE : C:\msys64\mingw64\bin\ffmpeg.exe
  echo La conversion en a besoin. Le controle seul fonctionne sans lui.
  pause
  exit /b 1
)
echo Conversion en cours, cela peut prendre une minute par video...
echo.
py -3 tools\jeux.py --convertir
echo.
pause
endlocal
