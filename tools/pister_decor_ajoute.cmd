@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- QUEL DECOR LE COMBAT DEMANDE-T-IL VRAIMENT ?
rem
rem Double-cliquez. C'est le build du decor ajoute, mais lance SOUS
rem DEBOGUEUR : un point d'arret sur 0x1800D7130, l'UNIQUE chargeur de decor,
rem dit pour chaque chargement l'INDICE demande et QUI le demande.
rem
rem POURQUOI CETTE MESURE
rem
rem   A l'ecran, le combat charge « Training Room » -- et STGGYM est le decor
rem   MAISON de KRT (Jean Kujo), d'apres rom/game_score.txt. Deux lectures
rem   possibles, et elles demandent des correctifs opposes :
rem
rem     A. le combat n'utilise PAS le choix de STAGE SELECT dans ce mode : il
rem        prend le decor maison de l'adversaire. Notre indice 42 ne serait
rem        alors jamais demande -- le journal ne le montrerait pas.
rem     B. l'indice 42 EST demande, mais quelque chose le rejette ou le
rem        traduit en route. Le journal le montrerait, suivi d'un autre.
rem
rem   Je ne veux pas trancher au jugé : le balayage des immediats ne dit pas a
rem   quel domaine chaque comparaison appartient, et j'ai deja paye une fois
rem   pour avoir suppose au lieu de mesurer.
rem
rem CE QU'IL FAUT FAIRE
rem
rem   1. laissez le jeu demarrer (le clavier reste a VOUS, rien n'est force) ;
rem   2. allez jusqu'au combat comme d'habitude -- STAGE SELECT, case du DOJO,
rem      BARRE ESPACE pour passer sur VIRTUA FIGHTER 5 R, puis validez ;
rem   3. quand le decor est charge, fermez le jeu (Echap puis EXIT, ou la
rem      croix). La mesure s'arrete d'elle-meme au bout de quatre minutes.
rem
rem   Le journal est ecrit AU FIL DE L'EAU dans analysis\pister_decor.txt :
rem   meme si le debogueur se bloque, ce qui a ete vu est ecrit.
rem
rem   Envoyez-moi les lignes « CHARGEMENT : index ... ».
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- quel decor le combat demande-t-il ? (mesure sous debogueur)
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
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso trm --variantes --variantes-texte --du2-collision --decors-table 44 --grille-table --decor-neuf d5r --objset 6150 --auth3d STGD5R --variantes-neuf 42 >nul
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)

echo.
echo   Le jeu demarre SOUS DEBOGUEUR. Le clavier est a vous.
echo   Allez au combat : STAGE SELECT, case du DOJO, BARRE ESPACE, validez.
echo   Puis fermez le jeu -- ou laissez la mesure finir (4 minutes).
echo.
py -3 tools\pister_decor.py --secondes 240
echo.
echo   Le journal : analysis\pister_decor.txt
echo.
pause
endlocal
