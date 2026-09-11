@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- QUI DEMANDE LE DECOR ? (point d arret MATERIEL sur +0x60)
rem
rem Double-cliquez, puis : MENU -^> DOJO -^> entrainement, et fermez le jeu.
rem Le journal s ecrit AU FIL DE L EAU dans analysis\pister_60_stage.txt.
rem
rem CE LANCEUR REMPLACE pister_5c_dojo.cmd, ET VOICI POURQUOI
rem
rem   La mesure de la veille surveillait TaskStage+0x5C. Son journal n a rendu
rem   que cinq ecritures venues de ntdll, valeur FEEEFEEE : le remplissage de
rem   tas d un bloc LIBERE. Deux defauts, et les deux sont dans le binaire,
rem   pas dans une hypothese :
rem
rem     . +0x5C n est ecrit que par UNE instruction dans tout le moteur,
rem       0x18018EF8B, qui RECOPIE +0x60. Surveiller +0x5C ne pouvait donc
rem       nommer que cette recopie. Le decideur est celui qui ecrit +0x60 ;
rem
rem     . la tache TaskStage est creee ET DETRUITE en cours de partie
rem       (0x18018EE30 publie le pointeur, 0x18018EEA0 le remet a zero). Un
rem       point d arret arme une fois sur objet+0x5C finit par regarder un
rem       bloc rendu au tas. C est mot pour mot ce que le journal disait.
rem
rem   Un balayage lineaire compte 233 ecritures de 32 bits en [reg+0x60] dans
rem   .text : les departager par la lecture est hors de portee. Le processeur,
rem   lui, nomme l ecrivain.
rem
rem CE QUE LA SONDE POSE
rem
rem     DR sur le POINTEUR 0x1807499D8   creation / destruction de la tache,
rem                                      et REARMEMENT sur le nouvel objet
rem     DR sur tache+0x60                la DEMANDE : valeur, instruction,
rem                                      et la chaine d appel sur la pile
rem     DR sur tache+0x5C                la recopie : elle doit venir de la
rem                                      rva 0x18EF8E, sinon mon modele est faux
rem     BP sur 0x18020AE60               l indice que le mode pose (r9d)
rem     BP sur 0x180203F2E               l ECRETAGE a 40 vers gym : la
rem                                      valeur qui arrive, la borne et le
rem                                      repli relus VIVANTS
rem     BP sur 0x18018FCF0               la demande
rem     BP sur 0x1800D7130               l indice reellement charge
rem
rem   A chaque tic, les deux champs sont relus : une valeur qui change sans
rem   qu un DR l ait vue est DITE, au lieu de passer inapercue.
rem
rem CE QU IL FAUT M ENVOYER
rem
rem   Les lignes " DEMANDE ^<- " et les " retour ... rva " qui les suivent :
rem   c est la chaine qui mene au 39. Et la ligne " CHARGEMENT ".
rem
rem   Le build est celui de dojo_5r.cmd, a l identique : decor ajoute d5r a
rem   l indice 42, --dojo-decor 42. On ne change pas le build pendant qu on
rem   mesure.
rem
rem   Pour tout rendre : decor_ajoute_retirer.cmd
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- qui DEMANDE le decor ? (DR sur TaskStage+0x60)
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
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso trm --variantes --variantes-texte --du2-collision --decors-table 44 --grille-table --decor-neuf d5r --objset 6150 --auth3d STGD5R --variantes-neuf 42 --dojo-decor 42 >nul
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
echo   Le jeu demarre SOUS DEBOGUEUR, et il demarre LENTEMENT.
echo   Le clavier est a vous : MENU -^> DOJO -^> entrainement, puis fermez
echo   le jeu. Pas besoin de seconde manette.
echo.
py -3 tools\pister_60_stage.py --secondes 420
echo.
echo   Le journal : analysis\pister_60_stage.txt
echo.
pause
endlocal
