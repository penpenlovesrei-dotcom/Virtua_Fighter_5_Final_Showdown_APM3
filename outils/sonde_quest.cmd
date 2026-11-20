@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LA SONDE DU MODE QUEST. Double-cliquez.
rem
rem Elle mene le jeu TOUTE SEULE jusqu a l ecran voulu, sans que personne
rem touche au clavier, et fait des captures a heures fixes. Le scenario est
rem joue par apm.dll, qui relit apm_entrees.txt toutes les 250 ms.
rem
rem Le scenario manuel est SAUVE avant et REMIS apres.
rem
rem Sans argument : la liste des dix scenarios.
rem   tools\sonde_quest.cmd carte
rem   tools\sonde_quest.cmd combat
rem
rem IMPORTANT : la sonde REFUSE de lancer le jeu tant que le fichier temoin
rem   runtime\media\vf5fs\AUTORISATION_LANCEMENT.txt
rem n existe pas. C est l interdiction de Frederic, et seule sa main la leve.
rem Sans ce fichier, la sonde se contente d ECRIRE les scenarios dans
rem tools\scenarios\quest_*.txt, ou on peut les relire et les corriger.
rem
rem Sorties : analysis\sonde_quest.txt et les PNG dans analysis\sonde\.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- sonde du mode QUEST
echo   ===================================================================
echo.
if "%~1"=="" (
  py -3 tools\sonde_quest.py --liste
  echo.
  echo   Relancez avec un nom de scenario, par exemple :
  echo       tools\sonde_quest.cmd carte
  echo.
  pause
  exit /b 0
)
py -3 tools\sonde_quest.py %*
set RC=%ERRORLEVEL%
echo.
if "%RC%"=="3" (
  echo   Le jeu n a PAS ete lance : l interdiction tient. Les scenarios sont
  echo   ecrits dans tools\scenarios\.
)
pause
endlocal
exit /b %RC%
