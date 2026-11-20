@echo off
rem ---------------------------------------------------------------------------
rem Mesure, code par code, quel bit du masque du combattant chaque code allume.
rem
rem Ne capture RIEN a l'ecran : tout se lit en memoire (ROB+0x508 et ROB+0x510).
rem Deux combattants sont mesures, parce qu'on ne sait pas d'avance lequel est le
rem joueur, et plusieurs passes sont faites, parce que l'adversaire bouge aussi.
rem
rem ATTENTION : sur le jeu contre la machine, cette mesure NE CONVERGE PAS --
rem une seule mesure sur 48 s'est repetee. Voir docs/formats/apm_input.md.
rem La carte code -> bit de l'INTERFACE, elle, est etablie statiquement.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
py -3 tools\carte_entrees.py --passes 4 --pause 0.9 --secondes 400
echo.
pause
endlocal
