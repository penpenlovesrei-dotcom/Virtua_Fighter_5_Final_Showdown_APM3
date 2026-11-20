@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- POURQUOI LA BARRE ESPACE NE FAIT RIEN
rem
rem Double-cliquez, PATIENTEZ le demarrage, puis :
rem   allez a STAGE SELECT, curseur sur la case de DURAL,
rem   et pressez la BARRE ESPACE plusieurs fois, LENTEMENT.
rem   Ensuite fermez le jeu (Echap puis quittez), le bilan s'affiche.
rem
rem Le detour peut echouer a quatre endroits, et ils ne se ressemblent pas.
rem Trois points d'arret poses DANS la greffe les separent :
rem
rem   0x180EA1000  entree du detour           -> est-il seulement joue ?
rem   0x180EA1015  apres la requete d'entree  -> al vaut-il jamais autre chose
rem                                              que zero ?
rem   0x180EA1036  l'ecriture de l'index      -> la rotation a-t-elle lieu ?
rem
rem plus un releve continu de l'etat et du decor de TaskSelStage.
rem
rem   . detour jamais joue        -> le point d'accroche est mauvais ;
rem   . al toujours zero          -> la barre espace n'arrive pas sur le code 6,
rem                                  ou [rax+0x160] n'est pas ce qu'on croit ;
rem   . aucune ecriture           -> une garde ferme (etat, ou hors anneau) ;
rem   . ecritures MAIS du1 charge -> quelqu'un remet l'index en aval.
rem
rem Le binaire n'est pas retouche : c'est celui que variantes.cmd a produit.
rem Journal complet : analysis\pister_variantes.txt
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\pister_variantes.py --secondes 300
echo.
pause
endlocal
