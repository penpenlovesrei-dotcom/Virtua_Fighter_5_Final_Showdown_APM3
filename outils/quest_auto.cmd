@echo off
rem ---------------------------------------------------------------
rem VF5 FS -- LE MODE QUEST, VERIFIE TOUT SEUL. Double-cliquez.
rem
rem   Il lance questV2.cmd, puis pilote le jeu jusqu a l ecran du
rem   Quest et le photographie dans analysis\_quest_auto.png.
rem
rem   La sequence est celle que Frederic a dictee : 10 s d attente,
rem   START, 2 s, START, 2 s, BAS, 1 s, START, capture.
rem
rem   LES APPUIS NE SONT PAS DU CLAVIER SIMULE : le apm.dll relit
rem   apm_entrees.txt toutes les 250 ms, donc ecrire ce fichier
rem   revient a presser le bouton. Aucun focus n est vole.
rem ---------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo   Le pilote attend que vfes.exe demarre...
start "pilote du Quest" /min py -3 tools\quest_auto.py
call "%~dp0questV2.cmd"
endlocal
