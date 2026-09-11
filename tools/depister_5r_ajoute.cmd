@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- OU BLOQUE LE CHARGEMENT DU DECOR AJOUTE ? (les sept portes)
rem
rem Double-cliquez. MENU -^> DOJO -^> selectionnez le dojo d Akira de VF5 R.
rem Laissez le chargement tourner une dizaine de secondes, puis FERMEZ le jeu.
rem Le journal s ecrit AU FIL DE L EAU dans analysis\pister_import_d5r.txt.
rem
rem POURQUOI CE LANCEUR, APRES DEUX CORRECTIFS QUI N ONT PAS SUFFI
rem
rem   L ecretage leve, le decor est bien DEMANDE et le chargement DEMARRE.
rem   La dixieme piece posee (envmap_correct_d5r.txt), il ne finit toujours
rem   pas. Trois pannes donnent le meme ecran qui tourne, et une seule mesure
rem   les separe :
rem
rem     1. le fichier n est PAS LU        -> un nom non masque dans le .par
rem     2. le fichier est lu mais REFUSE  -> un objet demande manque dedans
rem     3. une PIECE ANNEXE manque        -> la barriere de l etat 3 ne passe
rem                                          jamais
rem
rem   L etat 3 du chargeur evalue SEPT conditions a la suite et ressort a la
rem   premiere qui echoue. La porte la plus haute atteinte nomme donc
rem   exactement la piece qui manque :
rem
rem     porte 1  l objset            stgd5r.farc
rem     porte 2  l eclairage         d5r.ibl + les cinq light_param
rem     porte 3  la collision        STGD5R_COLI.000.bin
rem     porte 4  l auth_3d du decor  STGD5R.farc
rem     porte 5  le drapeau de scene
rem     porte 6  l auth_3d des effets EFFSTGD5R.farc
rem     porte 7  les sons d ambiance  (ne peut PAS bloquer : liste avec defaut)
rem
rem   La sonde releve aussi les fichiers reellement OUVERTS sur le disque
rem   (point d arret sur CreateFileW/A) et l etat de TaskStage en continu. Un
rem   fichier pose mais jamais ouvert et un fichier ouvert puis refuse ne se
rem   ressemblent pas dans le journal.
rem
rem CE QU IL FAUT M ENVOYER : les lignes  porte  et  etat , et la liste des
rem fichiers ouverts. Le verdict est ecrit a la fin du journal.
rem
rem   Le build est celui de dojo_5r_repli.cmd, a l identique.
rem   Pour tout rendre : decor_ajoute_retirer.cmd
rem ---------------------------------------------------------------------------

setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- le dojo de VF5 R par le REPLI (ecretage leve)
echo   ===================================================================
echo.
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1

set "ETAT=0"
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgdjo.farc" set "ETAT=1"
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrm.farc" set "ETAT=1"
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrs.farc" set "ETAT=1"
if "%ETAT%"=="1" (
  echo   Un decor importe sur un emplacement du jeu est en place : on le
  echo   retire ^(~20 s chacun^).
  if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgdjo.farc" py -3 tools\importer_decor.py --retirer djo >nul 2>&1
  if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrm.farc" py -3 tools\importer_decor.py --retirer trm >nul 2>&1
  if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrs.farc" py -3 tools\importer_decor.py --retirer trs >nul 2>&1
)

if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgd5r.farc" (
  echo   Le decor d5r est deja pose.
) else (
  echo   Pose du decor ajoute ^(~20 s^)...
  py -3 tools\decor_neuf.py --poser d5r --depuis djo --source VF5R --objset 6150
  if errorlevel 1 (
    echo.
    echo La pose a ECHOUE. Rien n'a ete lance.
    pause
    exit /b 1
  )
)

echo   Compilation de apm.dll...
py -3 tools\gen_apm_stub.py >nul 2>&1
echo   Patch du moteur ^(~20 s^)...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso trm --variantes --variantes-texte --du2-collision --decors-table 44 --grille-table --decor-neuf d5r --objset 6150 --auth3d STGD5R --variantes-neuf 42 --decor-ecretage 44 --decor-repli 42 --obj-db-libre >nul
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)

echo.
py -3 tools\controle_decor_neuf.py --code d5r --indice 42 --objset 6150
if errorlevel 1 (
  echo.
  echo LE CONTROLE AVANT VOL A ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)

echo.
echo   MENU -^> DOJO -^> selectionnez le dojo d Akira de VF5 R.
echo   Laissez le chargement tourner ^(dix secondes suffisent^), puis
echo   FERMEZ le jeu. Le journal est deja ecrit.
echo.
py -3 tools\pister_import.py d5r --indice 42 --secondes 300
echo.
echo   Le journal : analysis\pister_import_d5r.txt
echo.
pause
endlocal
