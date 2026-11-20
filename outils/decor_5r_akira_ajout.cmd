@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- BUILD A PART : LE DOJO D'AKIRA VF5 R **AJOUTE**, PAS SUBSTITUE
rem
rem Double-cliquez. C'est le build console complet, PLUS le dojo d'Akira de
rem Virtua Fighter 5 R (2008) pose sur un emplacement LIBRE. Le dojo de Final
rem Showdown reste entier, a sa place : aucun decor n'est perdu.
rem
rem CE QUI CHANGE PAR RAPPORT A decor_5r_akira.cmd
rem
rem   decor_5r_akira.cmd  REMPLACE le dojo : les fichiers de VF5 R sont poses
rem                       sous le nom `djo`, et celui de Final Showdown
rem                       disparait tant que le lanceur est en place.
rem   CE LANCEUR          AJOUTE : les fichiers sont poses sous le code `trs`,
rem                       un emplacement d'essai que RIEN n'utilise -- mesure
rem                       par tools\emplacements.py sur quatre preuves. Les
rem                       deux generations coexistent.
rem
rem COMMENT LE VOIR, ET C'EST LE POINT
rem
rem   STAGE SELECT, case du DOJO (ligne du milieu, 3e colonne), puis
rem   **BARRE ESPACE** : le decor sous le curseur bascule entre les deux
rem   generations, et le nom s'ecrit a l'ecran --
rem
rem       VIRTUA FIGHTER 5 FS   le dojo de 2010, celui du jeu
rem       VIRTUA FIGHTER 5 R    le dojo de 2008, importe entier
rem
rem   C'est le meme mecanisme que les cinq decors de Dural : une case reste
rem   UNE case, la barre espace fait defiler ses variantes.
rem
rem CE QUI EST TOUCHE, ET C'EST TOUT
rem
rem   Cote FICHIERS -- les huit pieces de VF5 R posees sous le code `trs` dans
rem   vf5fs_media/rom/, et les huit noms correspondants masques dans l'index de
rem   vf5fs_data.par (un octet chacun). Les deux noms internes de l'archive
rem   sont reecrits dans son en-tete (stgdjo_obj.bin -> stgtrs_obj.bin).
rem
rem   Cote MOTEUR -- le descripteur de `trs` (0x180404E70) recoit un CLONE
rem   complet de celui de djo : il faut les quinze champs, pas trois. Restent
rem   en propre l'objset (44), les cinq objets et la collision, ecrite dans le
rem   mou de .rdata. Le binaire repart TOUJOURS de .origine : il n'y a rien a
rem   defaire de ce cote-la.
rem
rem POUR REVENIR EN ARRIERE
rem
rem   decor_5r_akira_ajout_retirer.cmd  rend les huit noms au .par, efface les
rem                                     fichiers libres. Puis n'importe quel
rem                                     autre lanceur repose son propre etat.
rem
rem   Le binaire, lui, revient tout seul : le prochain lanceur le refabrique
rem   depuis vf5fs-pxd-w64-Retail_APM3.dll.origine.
rem
rem   Touches : fleches, Entree = VALIDER, W = ANNULER, X C V = croix rond
rem             triangle, Espace = SELECT/variante, Echap = quitter.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
if exist "analysis\decor_5r_ajout.log" del "analysis\decor_5r_ajout.log" >nul 2>&1
echo VF5 -- decor_5r_akira_ajout.cmd  %DATE% %TIME% > "analysis\decor_5r_ajout.log"
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1

rem ETAT DES FICHIERS : on le POSE, on ne l'herite pas. Un balayage du .par
rem coute 16 secondes, donc on ne retire que ce qui est vraiment la -- le
rem fichier libre est la preuve qu'un --poser est passe.
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgdjo.farc" (
  echo   Un decor est pose sur djo : on le retire ^(~20 s^)...
  py -3 tools\importer_decor.py --retirer djo >> "analysis\decor_5r_ajout.log" 2>&1
)
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrm.farc" (
  echo   Un decor est pose sur trm : on le retire ^(~20 s^)...
  py -3 tools\importer_decor.py --retirer trm >> "analysis\decor_5r_ajout.log" 2>&1
)

if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrs.farc" (
  echo   Le dojo VF5 R est deja pose sur trs -- on ne repaie pas les 20 s.
) else (
  echo   Pose du dojo VF5 R sur l'emplacement libre trs ^(~20 s^)...
  py -3 tools\importer_decor.py --poser djo --source VF5R --vers trs --pour decor_5r_akira_ajout.cmd
  if errorlevel 1 (
    echo.
    echo La pose du decor a ECHOUE. Rien n'a ete lance.
    pause
    exit /b 1
  )
)

echo   Compilation de apm.dll...
py -3 tools\gen_apm_stub.py >> "analysis\decor_5r_ajout.log" 2>&1
if errorlevel 1 (
  echo.
  echo La compilation du apm.dll a ECHOUE. Rien n'a ete lance.
  echo Voir analysis\decor_5r_ajout.log
  pause
  exit /b 1
)

echo   Patch du moteur ^(~15 s^)...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso trm --variantes --variantes-texte --variantes-djo trs --du2-collision
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)

echo.
echo   Controle avant vol...
py -3 tools\pister_import.py trs --controle
if errorlevel 1 (
  echo.
  echo LE CONTROLE AVANT VOL A ECHOUE -- voir la liste ci-dessus.
  echo Rien n'a ete lance : le jeu aurait tourne en boucle sans rien dire.
  echo Pour repartir propre : decor_5r_akira_ajout_retirer.cmd
  pause
  exit /b 1
)

echo.
echo   LE DOJO DE VF5 R EST **AJOUTE**. Celui de Final Showdown est intact.
echo.
echo   STAGE SELECT, case du DOJO ^(ligne du milieu, 3e colonne^), puis
echo   BARRE ESPACE : le decor bascule, et son nom s'ecrit a l'ecran.
echo.
echo   SI CA BLOQUE SUR L'ECRAN DE CHARGEMENT : fermez le jeu et lancez
echo   depister_5r.cmd -- il nomme la piece fautive parmi les sept portes.
echo   Pour tout rendre : decor_5r_akira_ajout_retirer.cmd
echo.
pushd "%~dp0..\runtime\media\vf5fs"
if not exist vfes.exe (
  echo INTROUVABLE : "%CD%\vfes.exe"
  pause
  popd
  exit /b 1
)
echo   Demarrage du jeu -- il met un moment a afficher.
start "" "%CD%\vfes.exe"
"%SystemRoot%\System32\timeout.exe" /t 6 /nobreak >nul 2>&1
tasklist /fi "IMAGENAME eq vfes.exe" | find /i "vfes.exe" >nul
if errorlevel 1 (
  echo.
  echo LE JEU NE S'EST PAS LANCE, ou il s'est arrete aussitot.
  echo   Lancez depister_5r.cmd : il demarre le jeu sous debogueur.
  pause
) else (
  echo   Le jeu tourne.
)
popd
pause
endlocal
