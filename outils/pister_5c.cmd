@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- QUI REMET LE DECOR A DU1 ?
rem
rem Double-cliquez, PATIENTEZ le demarrage, puis :
rem   STAGE SELECT, curseur sur la case de DURAL,
rem   pressez la BARRE ESPACE deux ou trois fois, puis quittez le jeu.
rem   Le bilan s'affiche.
rem
rem CE QUE LA MESURE PRECEDENTE A DIT
rem
rem   Le detour de --variantes fait TOUT ce qu'il doit : il est joue (300
rem   passages), la barre espace repond (al = 1), et l'index EST ecrit a 22
rem   (du2). Puis quelque chose le remet a du1 dans la foulee :
rem
rem     t=49.0  etat 2  decor du2     <- notre ecriture a pris
rem     t=49.0  etat 2  decor du1     <- et elle est defaite aussitot
rem
rem   Ce n'est donc ni l'entree, ni la garde, ni l'anneau. C'est un AUTRE
rem   ecrivain du champ.
rem
rem CE QUE CELLE-CI FAIT
rem
rem   Le balayage donne huit candidats qui ecrivent TaskSelStage+0x5C dans la
rem   seule zone 0x180170000-0x180180000. Plutot que de les departager a la
rem   lecture, on pose un point d'arret MATERIEL en ecriture sur le champ :
rem   le processeur nomme lui-meme l'instruction fautive, et on voit la valeur
rem   qu'elle pose.
rem
rem   Le champ est en [0x180714928] + 0x3B0 + 0x5C.
rem
rem   Attention : le registre de debogage se declenche APRES l'ecriture --
rem   l'adresse montree est l'instruction SUIVANTE, l'ecrivain est juste avant.
rem
rem   Journal complet : analysis\pister_5c.txt
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\pister_5c.py --secondes 300
echo.
pause
endlocal
