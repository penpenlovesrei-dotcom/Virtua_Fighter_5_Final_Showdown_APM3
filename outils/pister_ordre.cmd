@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- QUI DESSINE APRES NOUS ?
rem
rem Double-cliquez, PATIENTEZ le demarrage, allez a STAGE SELECT avec le
rem curseur sur la case de DURAL, et laissez l'ecran tranquille deux secondes.
rem Le releve se fait tout seul. Fermez ensuite le jeu, le bilan s'affiche.
rem
rem POURQUOI CETTE MESURE
rem
rem   Le texte s'affiche mais passe SOUS les couches AET. Trois placements ont
rem   echoue, tous fondes sur un raisonnement et non sur une mesure :
rem
rem     . creneau 4 de TaskSelStage  -> dessine, mais dessous ;
rem     . creneau 6 de TaskSelStage  -> jamais appele ;
rem     . detour du creneau 4 de TaskSelector, celui qui dessine le panneau
rem       -> toujours dessous.
rem
rem   Le dernier point est le plus instructif : si dessiner APRES le parent ne
rem   suffit pas, l'AET n'est pas rendu par une tache. Reste a savoir par quoi.
rem
rem CE QUE LA SONDE FAIT
rem
rem   Elle enregistre la suite des appels entre DEUX passages de notre dessin
rem   -- soit exactement une trame. Ce qui apparait dedans, apres nous, est ce
rem   qui nous recouvre. Sont instrumentes notre dessin et les sept creneaux
rem   d'AetMgr, la classe que le RTTI nomme (vtable 0x1803487A8).
rem
rem   Si rien d'instrumente ne passe apres nous, c'est deja une reponse : le
rem   coupable n'est pas AetMgr, et on elargira le filet.
rem
rem   Journal complet : analysis\pister_ordre.txt
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\pister_ordre.py --secondes 300
echo.
pause
endlocal
