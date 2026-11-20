@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- DEPISTE LE DECOR IMPORTE : OU CA BLOQUE, ET POURQUOI
rem
rem Double-cliquez APRES un essai qui a mal tourne. Le jeu se relance sous
rem instruments -- le clavier reste a vous, allez au DOJO avec Akira, ou
rem prenez la case du dojo dans STAGE SELECT.
rem
rem CE QUI EST MESURE
rem
rem 1. AVANT DE LANCER, sans le jeu : les neuf fichiers poses (taille et
rem    magie), les neuf noms masques dans l'index du .par, le descripteur du
rem    moteur, et surtout -- les objets que le descripteur DEMANDE existent-ils
rem    dans l'objset qu'on a pose ? S'il manque quelque chose, le jeu n'est
rem    meme pas lance.
rem
rem 2. PENDANT LA PARTIE : quels fichiers du decor sont reellement OUVERTS sur
rem    le disque (point d'arret sur CreateFileW/A) ; l'etat de TaskStage releve
rem    en continu ; et les SEPT PORTES de la barriere de l'etat 3, une par une.
rem
rem POURQUOI LES SEPT PORTES. L'etat 3 du chargeur (0x18018F74A) evalue sept
rem conditions A LA SUITE et ressort a la premiere qui echoue. La porte la plus
rem haute atteinte designe donc exactement la piece qui manque :
rem
rem    porte 1  l'objset            (stgdjo.farc)
rem    porte 2  l'eclairage         (djo.ibl + light_param)
rem    porte 3  la collision        (STGDJO_COLI.000.bin)
rem    porte 4  l'auth_3d du decor  (STGDJO.farc)
rem    porte 5  le drapeau de scene
rem    porte 6  l'auth_3d des effets(EFFSTGDJO.farc)
rem    porte 7  les sons d'ambiance
rem
rem Trois pannes se ressemblent a l'ecran -- fichier jamais lu, fichier lu mais
rem refuse, piece annexe manquante -- et donnent le meme ecran de chargement
rem qui tourne. Ces trois mesures les separent.
rem
rem Le journal complet est ecrit dans analysis\pister_import_djo.txt.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\pister_import.py djo --secondes 300
echo.
pause
endlocal
