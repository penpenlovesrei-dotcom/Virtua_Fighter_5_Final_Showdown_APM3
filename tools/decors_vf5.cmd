@echo off
rem -----------------------------------------------------------------------
rem VF5 FS -- LES DECORS DU VIRTUA FIGHTER 5 D ORIGINE (ver.B), AJOUTES
rem           a la suite de ceux de VF5 R
rem
rem Double-cliquez. Puis, dans un ecran de SELECTION DE DECOR :
rem
rem     la BARRE ESPACE fait tourner la case entre ses TROIS generations :
rem     Final Showdown -> VF5 R -> VIRTUA FIGHTER 5 -> Final Showdown
rem
rem     La case de DURAL tourne sur NEUF variantes : les cinq de Final
rem     Showdown, puis les QUATRE de VF5 ver.B -- la meme architecture
rem     (stgdur, 35,7 Mo, que plus aucune version ne contient) sous
rem     quatre ciels et quatre eclairages. Libelles provisoires
rem     "VIRTUA FIGHTER 5 - 1 .. 4" : leur nom est a donner a l ecran.
rem
rem CE QUI N ETAIT PAS COMME VF5 R, ET QUI EST CORRIGE A LA POSE
rem
rem   . les textures de ver.B ne sont pas numerotees comme celles de FS
rem     (3 277 numeros sur 3 975 designaient une autre texture) : elles
rem     sont RENUMEROTEES dans nos archives, jamais dans celles du jeu ;
rem   . ses objets n ont pas les memes rangs : le sol, le ciel, l ombre et
rem     le reflet sont relus dans le descripteur de ver.B lui-meme ;
rem   . ses effets sont les SIENS (sa table, relue dans son binaire) :
rem     pas d effet que ver.B n avait pas ;
rem   . depuis le 2026-09-11, VF5 R comme ver.B : listes, murs,
rem     animations ET dossiers d effet viennent de LEUR binaire, et
rem     sept effets de plus sont servis -- sol qui se casse (bn5 bnb),
rem     petales (tr5 trb), pluie (br5 ncb), eclaboussure de ring-out
rem     (rv5 sn5 rvb jnb), anneau de neige (ykb), vetements mouilles,
rem     anneau de brume (jn5 snb). Pas encore vus a l ecran ;
rem   . les grillages cassables sont des ajouts de VF5 R : seuls djo, slk,
rem     yuk et bar gardent leurs barrieres en ver.B.
rem
rem AUCUN decor de Final Showdown n est touche : ce sont des entrees
rem NEUVES, indices 61 a 81, a cote des 42 a 60 de VF5 R.
rem
rem Pour tout rendre : decors_vf5_retirer.cmd
rem -----------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- les decors de VF5 R et du VIRTUA FIGHTER 5 d origine
echo   ===================================================================
echo.
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1

rem ETAT DES FICHIERS : on le POSE, on ne l herite pas.
set "ETAT=0"
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgdjo.farc" set "ETAT=1"
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrm.farc" set "ETAT=1"
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrs.farc" set "ETAT=1"
if "%ETAT%"=="1" (
  echo   Un decor importe sur un emplacement du jeu est en place : on le retire.
  if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgdjo.farc" py -3 tools\importer_decor.py --retirer djo >nul 2>&1
  if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrm.farc" py -3 tools\importer_decor.py --retirer trm >nul 2>&1
  if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrs.farc" py -3 tools\importer_decor.py --retirer trs >nul 2>&1
)

set "POSES=1"
if not exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgso5.farc" set "POSES=0"
if not exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgd4b.farc" set "POSES=0"
if not exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgd45.farc" set "POSES=0"
if "%POSES%"=="1" (
  echo   Les decors sont deja poses ; on refait les deux bases.
  py -3 tools\decor_neuf.py --poser-lot 5r+vf5 --bases-seules >nul
  if errorlevel 1 (
    echo.
    echo Les bases n ont pas pu etre refaites. Rien n a ete lance.
    pause
    exit /b 1
  )
) else (
  echo   Pose des decors ^(plusieurs centaines de Mo, plusieurs minutes^)...
  py -3 tools\decor_neuf.py --poser-lot 5r+vf5
  if errorlevel 1 (
    echo.
    echo La pose a ECHOUE. Rien n a ete lance.
    pause
    exit /b 1
  )
)

echo   Shader des empreintes dans la neige ^(ykb^)...
py -3 tools\shader_empreintes.py >nul
if errorlevel 1 (
  echo.
  echo Le shader des empreintes n a pas pu etre pose. Rien n a ete lance.
  pause
  exit /b 1
)

echo   Compilation de apm.dll...
py -3 tools\gen_apm_stub.py >nul 2>&1
echo   Patch du moteur ^(~30 s^)...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso trm --du2-collision --variantes --variantes-texte --variantes-5r --variantes-vf5 --decors-table 86 --grille-table --decors-5r --decors-vf5 --decors-5r-dural --decor-ecretage 86 --decor-repli 42 --obj-db-libre >nul
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n a ete lance.
  pause
  exit /b 1
)

echo.
py -3 tools\controle_decors_5r.py
if errorlevel 1 (
  echo.
  echo LE CONTROLE AVANT VOL DE VF5 R A ECHOUE. Rien n a ete lance.
  pause
  exit /b 1
)
echo.
py -3 tools\controle_decors_vf5.py
if errorlevel 1 (
  echo.
  echo LE CONTROLE AVANT VOL DE ver.B A ECHOUE. Rien n a ete lance.
  pause
  exit /b 1
)

echo.
echo   Dans un ecran de SELECTION DE DECOR : la BARRE ESPACE fait tourner
echo   la case : Final Showdown, VF5 R, VIRTUA FIGHTER 5.
echo.
pushd "%~dp0..\runtime\media\vf5fs"
echo   Demarrage du jeu -- il met un moment a afficher.
start "" "%CD%\vfes.exe"
"%SystemRoot%\System32\timeout.exe" /t 8 /nobreak >nul 2>&1
tasklist /fi "IMAGENAME eq vfes.exe" | find /i "vfes.exe" >nul
if errorlevel 1 (
  echo.
  echo LE JEU NE S EST PAS LANCE, ou il s est arrete aussitot.
  pause
) else (
  echo   Le jeu tourne.
)
popd
pause
endlocal
