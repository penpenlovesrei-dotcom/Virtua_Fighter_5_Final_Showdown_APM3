@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- POURQUOI L OBJSET AJOUTE NE SE DECLARE-T-IL PAS PRET ?
rem
rem Double-cliquez. MENU -^> DOJO -^> choisissez le dojo de VF5 R, et LAISSEZ
rem le chargement tourner : la mesure se prend PENDANT qu il tourne. Fermez
rem le jeu ensuite. Journal : analysis\pister_objset_pret.txt
rem
rem CE QUE LA MESURE PRECEDENTE A ETABLI
rem
rem   t=42,0 s  etat 2  OUVERT : rom/objset/stgd5r.farc   la geometrie EST
rem                                                       demandee, enfin
rem   t=42,7 s  etat 3  les neuf autres pieces sont ouvertes
rem   t=43,1 s  etat 4 (derniere attente)  ... et jamais l etat 5
rem
rem   Et les sept portes de l etat 3 passent EXACTEMENT comme dans le build
rem   qui marche : 24 24 9 5 5 5 5 1 des deux cotes. Aucune piece ne manque,
rem   aucune porte ne refuse.
rem
rem   Le mur est l etat 4. Il appelle 0x1800F8A40(objset), qui demande au
rem   gestionnaire d objsets si celui-ci est PRET, en testant trois octets de
rem   son enregistrement : +0x90, +0x128 et +0x1F4.
rem
rem CE QUE CETTE SONDE FAIT, ET POURQUOI PAR COMPARAISON
rem
rem   Le gestionnaire garde UN ENREGISTREMENT DE 0x200 OCTETS PAR OBJSET,
rem   dans un vecteur trie par identifiant. Quand l etat 4 dure plus de deux
rem   secondes, la sonde ecrit :
rem
rem     . l enregistrement de NOTRE objset 6150, 128 dwords ;
rem     . celui d un objset TEMOIN qui est pret -- STGGYM (2847), le decor
rem       de la Training Room ; a defaut, le premier qu elle trouve pret ;
rem     . le DIFF des deux, offset par offset ;
rem     . les trois drapeaux nommes, cote a cote.
rem
rem   Deviner lequel des sous-systemes -- geometrie, textures, animation --
rem   n a pas fini serait repartir dans les hypotheses. Deux objets de meme
rem   forme, un qui marche et un qui ne marche pas : c est le champ qui
rem   differe qui nomme le coupable.
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
echo   MENU -^> DOJO -^> choisissez le dojo de VF5 R.
echo   LAISSEZ le chargement tourner : la comparaison se prend PENDANT
echo   qu il tourne. Fermez le jeu ensuite.
echo.
py -3 tools\pister_objset_pret.py --objset 6150 --temoin 2847 --secondes 300
echo.
echo   Le journal : analysis\pister_objset_pret.txt
echo.
pause
endlocal
