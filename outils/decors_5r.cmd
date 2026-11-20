@echo off
rem -----------------------------------------------------------------------
rem VF5 FS -- LES DIX-NEUF DECORS DE VIRTUA FIGHTER 5 R, AJOUTES
rem
rem Double-cliquez. Puis, dans un ecran de SELECTION DE DECOR :
rem
rem     la BARRE ESPACE fait passer la case de sa version Final Showdown
rem     a sa version VF5 R -- et le nom de la generation s affiche.
rem
rem Dix-neuf cases sur vingt et une ont leur double. Les deux qui ne l ont
rem pas : la case ALEATOIRE, et du1 (VF5 R range la scene des quatre
rem decors de Dural sous un seul nom, STGDUR : la correspondance reste a
rem etablir, elle n est pas devinee).
rem
rem CE QUE C EST, ET CE QUE CE N EST PAS
rem
rem   VF5 R n apporte AUCUN decor que l APM3 n ait pas -- il a les memes,
rem   moins du5. Ce qu il apporte, ce sont des versions plus riches des
rem   memes lieux : djo +8,1 Mo, sin +8,1, smo +7,3, nyc +6,9, du3 +4,3.
rem   Les ajouter, c est mettre les DEUX generations cote a cote.
rem
rem   AUCUN emplacement du jeu n est recycle : ce sont dix-neuf entrees
rem   NEUVES, aux indices 42 a 60, et les 41 decors d origine sont
rem   intacts.
rem
rem CE QU IL FAUT REGARDER
rem
rem   . la geometrie doit etre celle de 2008 -- textures plus lourdes ;
rem   . SES BARRIERES doivent etre la, comme au dojo ;
rem   . la musique doit jouer.
rem
rem   Si un decor manque ses barrieres, c est SA table de murs ou SA liste
rem   de taches d effet : controle_decors_5r.py les relit toutes
rem   dans la DLL patchee.
rem
rem Pour tout rendre : decors_5r_retirer.cmd
rem -----------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- les dix-neuf decors de Virtua Fighter 5 R
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

if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgso5.farc" (
  echo   Les dix-neuf decors sont deja poses ; on refait les deux bases.
  rem Les bases se DEDUISENT des archives posees : les refaire coute
  rem quelques secondes et garantit qu elles decrivent bien ce qui est la.
  py -3 tools\decor_neuf.py --poser-lot 5r --bases-seules >nul
  if errorlevel 1 (
    echo.
    echo Les bases n ont pas pu etre refaites. Rien n a ete lance.
    pause
    exit /b 1
  )
) else (
  echo   Pose des dix-neuf decors ^(~400 Mo, plusieurs minutes^)...
  py -3 tools\decor_neuf.py --poser-lot 5r
  if errorlevel 1 (
    echo.
    echo La pose a ECHOUE. Rien n a ete lance.
    pause
    exit /b 1
  )
)

echo   Compilation de apm.dll...
py -3 tools\gen_apm_stub.py >nul 2>&1
echo   Patch du moteur ^(~20 s^)...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso trm --du2-collision --variantes --variantes-texte --variantes-5r --decors-table 61 --grille-table --decors-5r --decor-ecretage 61 --decor-repli 42 --obj-db-libre >nul
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
  echo LE CONTROLE AVANT VOL A ECHOUE. Rien n a ete lance.
  pause
  exit /b 1
)

echo.
echo   Dans un ecran de SELECTION DE DECOR : la BARRE ESPACE fait passer
echo   la case de Final Showdown a VF5 R.
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
