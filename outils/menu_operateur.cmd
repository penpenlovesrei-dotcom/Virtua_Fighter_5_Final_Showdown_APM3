@echo off
rem ---------------------------------------------------------------------------
rem Lance vfes.exe dans le MENU OPERATEUR de la borne (GAME TEST MODE).
rem
rem Le stub apm.dll rend Sequence_isTest vrai quand le scenario porte test = 1.
rem
rem Les deux boutons du menu, ETABLIS a l'ecran :
rem    code 1 = SERVICE (deplace le curseur)   code 0 = TEST (valide)
rem
rem PIEGE : les menus ont une auto-repetition. Un appui de 350 ms balaie les six
rem lignes et ramene le curseur a sa place -- on croit que rien n'a bouge. Il
rem faut des impulsions de 20 ms ; menu_test.py s'en charge et navigue en lisant
rem la position du chevron dans une capture.
rem
rem   menu_operateur.cmd                   ouvre le menu et le montre
rem   menu_operateur.cmd "GAME ASSIGNMENTS"   y va et entre dedans
rem
rem A NE PAS FAIRE : valider EXIT ou SUB SYSTEM TEST MODE, le jeu s'arrete.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
if "%~1"=="" (
  py -3 tools\menu_test.py --lancer --capture menu_operateur.png
) else (
  py -3 tools\menu_test.py --lancer --aller "%~1" test --attendre 1.5 ^
     --capture menu_operateur.png
)
echo.
echo Capture : analysis\menu_operateur.png
pause
endlocal
