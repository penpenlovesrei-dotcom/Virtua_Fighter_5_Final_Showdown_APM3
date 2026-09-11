@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LE PREMIER DECOR VRAIMENT AJOUTE AU JEU
rem
rem Double-cliquez. Le dojo d'Akira de Virtua Fighter 5 R (2008) n'occupe la
rem place de RIEN : il vit a l'indice 41, une entree qui n'existait pas dans le
rem jeu. Les 41 decors d'origine sont tous intacts, celui de Final Showdown
rem compris.
rem
rem COMMENT LE VOIR
rem
rem   STAGE SELECT, case du DOJO (ligne du milieu, 3e colonne), BARRE ESPACE :
rem
rem       VIRTUA FIGHTER 5 FS   le dojo de 2010, indice 11, celui du jeu
rem       VIRTUA FIGHTER 5 R    le dojo de 2008, indice 42, AJOUTE
rem
rem POURQUOI L'INDICE 42 ET PAS 41
rem
rem   41 = 0x29 est le code « DECOR ALEATOIRE ». Sept sites du moteur le
rem   testent par EGALITE, pas comme une borne -- la case ALEA de la grille
rem   porte 41 en +0x08, et son icone est stage_icon_rnd_c. Un decor pose la
rem   se fait tirer au sort : c'est ce que le premier essai a montre a
rem   l'ecran, « le decor charge est celui d'un decor de FS charge au hasard ».
rem   La garde du gestionnaire le disait deja : `cmp edx, 0x29 ; jae` accepte
rem   0 a 40. Les decors ajoutes commencent donc a 42.
rem
rem CE QUI LE REND DIFFERENT DE decor_5r_akira_ajout.cmd
rem
rem   Ce lanceur-la posait le decor sur `trs`, un emplacement d'ESSAI du jeu.
rem   Il en restait un decor PARTIEL, et pour deux raisons de fond :
rem     . son descripteur nommait encore l'auth_3d du dojo de 2010 ;
rem     . un emplacement d'essai n'a que SEPT pointeurs relogés sur dix-sept,
rem       donc pas de table de murs et pas les neuf reprises de musique.
rem
rem   Ici l'entree est NEUVE, dans une section a nous qui porte ses propres
rem   relocations : ses DIX-SEPT pointeurs sont valides.
rem
rem CE QUE LE BUILD POSE
rem
rem   binaire   table de 44 decors (six bornes levees), l'entree 42 avec son
rem             objset 6150, son auth_3d STGD5R / EFFSTGD5R, sa collision
rem             rom/STGD5R_COLI.000.bin, et son code a trois lettres « d5r »
rem   fichiers  les neuf pieces sous le code d5r -- AUCUN nom a masquer, elles
rem             n'existent dans le .par d'aucune facon
rem   bases     obj_db.bin (+STGD5R, identifiant 6150, 171 objets) et
rem             auth_3d_db.bin (+STGD5R, +EFFSTGD5R) poses en fichiers libres,
rem             et CES DEUX NOMS-LA masques dans le .par
rem
rem POUR REVENIR EN ARRIERE
rem
rem   decor_ajoute_retirer.cmd rend les deux noms au .par et efface les
rem   fichiers. Le binaire, lui, revient tout seul : le patcheur repart
rem   toujours de .origine.
rem
rem   Touches : fleches, Entree = VALIDER, W = ANNULER, Espace = SELECT,
rem             Echap = quitter le mode.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- LE PREMIER DECOR VRAIMENT AJOUTE : le dojo d'Akira, VF5 R
echo   ===================================================================
echo.
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1

rem ETAT DES FICHIERS : on le POSE, on ne l'herite pas -- et on ne paie le
rem balayage du .par (16 s, muet) que s'il y a quelque chose a retirer.
set "ETAT=0"
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgdjo.farc" set "ETAT=1"
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrm.farc" set "ETAT=1"
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrs.farc" set "ETAT=1"
if "%ETAT%"=="1" (
  echo   Un decor importe sur un emplacement du jeu est en place : on le
  echo   retire. Chaque retrait balaie les 4 Go du .par -- ~20 s chacun.
  if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgdjo.farc" (
    echo     - djo...
    py -3 tools\importer_decor.py --retirer djo >nul 2>&1
  )
  if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrm.farc" (
    echo     - trm...
    py -3 tools\importer_decor.py --retirer trm >nul 2>&1
  )
  if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrs.farc" (
    echo     - trs...
    py -3 tools\importer_decor.py --retirer trs >nul 2>&1
  )
)
echo.

if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgd5r.farc" (
  echo   Le decor d5r est deja pose -- on ne repaie pas le balayage.
) else (
  echo   Pose du decor ajoute : neuf pieces, deux bases, deux noms masques.
  echo   Comptez ~20 s.
  py -3 tools\decor_neuf.py --poser d5r --depuis djo --source VF5R --objset 6150
  if errorlevel 1 (
    echo.
    echo La pose a ECHOUE. Rien n'a ete lance.
    pause
    exit /b 1
  )
)
echo.

echo   Compilation de apm.dll...
py -3 tools\gen_apm_stub.py >nul 2>&1
if errorlevel 1 (
  echo.
  echo La compilation du apm.dll a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)

echo   Patch du moteur, 44 decors ^(~20 s^)...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso trm --variantes --variantes-texte --du2-collision --decors-table 44 --grille-table --decor-neuf d5r --objset 6150 --auth3d STGD5R --variantes-neuf 42 >nul
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)

echo.
echo   Controle du deplacement des tables :
echo.
py -3 tools\verifier_decors_table.py --n 44
if errorlevel 1 (
  echo.
  echo LE CONTROLE DES TABLES A ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   Controle avant vol du decor ajoute :
echo.
py -3 tools\controle_decor_neuf.py --code d5r --indice 42 --objset 6150
if errorlevel 1 (
  echo.
  echo LE CONTROLE AVANT VOL A ECHOUE -- voir la liste ci-dessus.
  echo Rien n'a ete lance : le jeu aurait tourne en boucle sans rien dire.
  echo Pour repartir propre : decor_ajoute_retirer.cmd
  pause
  exit /b 1
)

echo.
echo   STAGE SELECT, case du DOJO, BARRE ESPACE.
echo     VIRTUA FIGHTER 5 FS  = indice 11, le dojo du jeu
echo     VIRTUA FIGHTER 5 R   = indice 42, AJOUTE
echo.
echo   Si le decor ne charge pas, le jeu boucle sur l'ecran de chargement :
echo   fermez-le et dites-le-moi, il y a sept portes a departager.
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
"%SystemRoot%\System32\timeout.exe" /t 8 /nobreak >nul 2>&1
tasklist /fi "IMAGENAME eq vfes.exe" | find /i "vfes.exe" >nul
if errorlevel 1 (
  echo.
  echo LE JEU NE S'EST PAS LANCE, ou il s'est arrete aussitot.
  pause
) else (
  echo   Le jeu tourne.
)
popd
pause
endlocal
