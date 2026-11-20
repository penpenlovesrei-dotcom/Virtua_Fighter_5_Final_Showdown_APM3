@echo off
rem ---------------------------------------------------------------------------
rem Lance vfes.exe et le mene au MODE ENTRAINEMENT (DOJO).
rem
rem Le jeu n'offre pas ce mode dans son parcours de borne. On l'obtient en
rem DEVIANT sa machine a etats : au moment ou il demande le sous-etat
rem APM3_GAME_VS (50), on ecrit APM3_TRAINING (52) a la place. Le jeu emprunte
rem alors sa propre machinerie de transition.
rem
rem L'interet : le partenaire NE BOUGE PAS. Toutes les mesures d'entree avaient
rem echoue parce que l'adversaire gere par la machine agissait pendant la
rem mesure -- une seule mesure sur 48 se repetait. Ici, seul le joueur agit.
rem Le jeu affiche en prime ses propres donnees de trame.
rem
rem Compter environ une minute et demie avant que la scene s'ouvre.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
py -3 tools\tracer_etats.py --devier 50 52 --secondes 300 --a 10
echo.
pause
endlocal
