@echo off
rem ---------------------------------------------------------------------------
rem CHRONOMETRER LE LANCEUR, etape par etape.
rem
rem Repond a " le jeu met du temps a demarrer " pour la partie qui va du
rem DOUBLE-CLIC au lancement de vfes.exe. Le profil BOOT du journal, lui, ne
rem mesure que ce qui vient apres : son horloge part au chargement de apm.dll.
rem
rem Avant de lancer le jeu, item_porte.cmd fait cinq choses -- recompiler
rem apm.dll, refaire les bases de decors, les empreintes de shaders, le style
rem de boutons, et une cinquantaine de chantiers sur le moteur. On les relance
rem ici une par une, exactement comme lui, et on les chronometre.
rem
rem NE RIEN LANCER PENDANT QUE LE JEU TOURNE : ce script recompile apm.dll et
rem repatche le moteur. Fermez vfes.exe d'abord.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
tasklist /nh | find /i "vfes.exe" >nul
if not errorlevel 1 (
  echo.
  echo   vfes.exe TOURNE. Fermez le jeu avant de chronometrer.
  echo.
  pause
  exit /b 1
)
echo.
echo   Chronometrage du lanceur -- memes commandes, meme ordre.
echo.
py -3 tools\chrono_lanceur.py
echo.
pause
endlocal
