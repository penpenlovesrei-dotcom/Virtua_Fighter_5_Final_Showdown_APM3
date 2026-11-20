@echo off
rem ---------------------------------------------------------------------------
rem RENDRE LE CLAVIER -- remet le jeu en commandes MANUELLES.
rem
rem Double-cliquez si le jeu appuie sur des touches tout seul (typiquement
rem START a l'ecran-titre).
rem
rem POURQUOI CA ARRIVAIT : vingt-deux outils du dossier ecrivent leur propre
rem scenario dans runtime\media\vf5fs\apm_entrees.txt -- deux impulsions START
rem pour traverser l'ecran-titre et aller mesurer plus loin -- et aucun ne le
rem remettait en etat. La partie suivante, jouee a la main, heritait du
rem scenario.
rem
rem C'est corrige a la source depuis le 2026-09-06 : tools\instrument.py rend
rem le clavier a la fin de chaque mesure, ET par atexit meme si la sonde plante
rem ou est interrompue. Ce lanceur ne sert donc plus que de filet.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
copy /y "tools\apm_entrees.txt" "runtime\media\vf5fs\apm_entrees.txt" >nul
if errorlevel 1 (
  echo ECHEC de la copie.
  pause
  exit /b 1
)
echo.
echo   Clavier rendu : le scenario ne contient plus que "0  rien".
echo   Le stub relit le fichier en moins de 250 ms -- inutile de relancer le jeu.
echo.
pause
endlocal
