@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LE DECOR AJOUTE DANS LE DOJO, PAR LE REPLI
rem
rem Double-cliquez, puis : MENU -^> DOJO -^> entrainement.
rem Pas besoin de seconde manette.
rem
rem CE QUI A ETE TROUVE, ET POURQUOI CE LANCEUR N EST PAS UN ESSAI DE PLUS
rem
rem   dojo_5r.cmd chargeait la Training Room (39) au lieu du decor 42. Trois
rem   hypotheses etaient tombees, et la sonde avait mesure ZERO passage sur le
rem   choix en dur du mode DOJO (0x18020AE78) : ce n etait pas ce chemin.
rem
rem   La chaine a ete lue d un bout a l autre le 2026-09-10, chaque maillon
rem   par une enumeration COMPLETE de references -- 4 references au global du
rem   mode, 2 appelants, 3 appelants de la demande :
rem
rem     0x18020AE60  [0x180754A58] = r9d       l indice du mode
rem                                            appelant : r9d = -1 EN DUR
rem     0x180209B16  ebx = [0x180754A58]
rem     0x180203F0F  mov eax, 0x27             39 = gym
rem     0x180203F1E  cmp ebp, 0x28
rem     0x180203F2E  cmova ebp, eax            au-dessus de 40 : 39
rem     0x1802035AA  call 0x18018FCF0          TaskStage::demander
rem     0x18018FD01  [TaskStage+0x60] = ecx    la demande
rem     0x18018EF8B  [TaskStage+0x5C] = ...    la recopie
rem
rem   cmova est un ECRETAGE NON SIGNE. L appelant du mode DOJO pose r9d = -1,
rem   c est-a-dire 0xFFFFFFFF : au-dessus de 40, donc ramene a 39, gym. Le
rem   decor ajoute n etait pas rejete, et pas meme demande -- l indice etait
rem   remplace deux appels avant TaskStage.
rem
rem   Aucune des six bornes levees ne pouvait l attraper : elles ont toutes ete
rem   trouvees en enumerant les LECTEURS des tables de decors, et celle-ci ne
rem   lit aucune table.
rem
rem CE QUE CE LANCEUR CHANGE, ET RIEN D AUTRE
rem
rem   Par rapport a dojo_5r.cmd, exactement trois options :
rem
rem     retiree  --dojo-decor 42        elle patchait une branche mesuree a
rem                                     zero passage
rem     ajoutee  --decor-ecretage 44    l ecretage passe de 40 a 43, sinon un
rem                                     indice de 42 ne survit pas
rem     ajoutee  --decor-repli 42       le repli n est plus gym mais le decor
rem                                     ajoute -- c est lui qu on verra quand
rem                                     le DOJO ne demande rien
rem
rem   Le TEMOIN est dojo_5r.cmd lui-meme : meme build, meme mode, et il donne
rem   la Training Room. Si celui-ci donne le dojo de 2008, la chaine est
rem   prouvee de bout en bout.
rem
rem CE QUI A CHANGE LE 2026-09-10, APRES VOTRE DEUXIEME ESSAI
rem
rem   Vous avez vu les FLAMMES et pas les BARRIERES. Les deux manques
rem   avaient ete traites la veille de la meme facon -- une entree clonee
rem   dans la table de la tache d effet -- et une seule des deux corrections
rem   pouvait marcher.
rem
rem   La table des flammes porte un pointeur vers une LISTE D UID, et rien
rem   d autre : la remplir avec NOS numeros suffisait.
rem
rem   La table des murs ne porte QUE DES POINTEURS. Tout le mur est dans les
rem   trois blocs qu ils designent, et ces blocs nomment leurs objets par
rem   (objset << 16) | rang :
rem
rem      +0x08 -> 28 morceaux : 4 poteaux aux coins (+-6, +-6) et
rem                            24 panneaux a +-1, +-3, +-5 le long des
rem                            quatre cotes -- c est LA BARRIERE DU RING
rem      +0x10 -> les uid : [1194] = STGDJO_EFF_KABE_REACT
rem      +0x18 -> la paire {FENCE, FENCE_KOWARE, 1194, 1194}
rem
rem   Objset 28. Le clone renvoyait donc au mur de djo, dont l objset n est
rem   pas charge dans un build d ajout : rien a l ecran, aucun message.
rem
rem   Le patcheur recopie maintenant les trois blocs dans .decors avec
rem   l objset 6150 et l uid 3476. Verifie dans le binaire patche, et
rem   controle_decor_neuf.py §6 le relit avant chaque vol.
rem
rem CE QU IL FAUT REGARDER
rem
rem   . le decor doit etre le dojo d Akira de VF5 R (2008) : ses textures sont
rem     deux fois plus lourdes qu en Final Showdown, ca devrait se voir ;
rem   . SES BARRIERES doivent etre la : quatre poteaux aux coins et
rem     vingt-quatre panneaux le long des quatre cotes ;
rem   . la musique doit jouer.
rem
rem   CE QUI A CHANGE LE 2026-09-10, APRES VOTRE ESSAI
rem
rem     . vous avez raison : le mode DOJO A BIEN un ecran de selection de
rem       decor. Ce qui etait ecrit ici hier etait faux, et corrige partout ;
rem     . le chargement qui ne finissait jamais est DIAGNOSTIQUE : il manquait
rem       une DIXIEME piece. Le chargeur d eclairage 0x1800D7130 compose SIX
rem       chemins, pas cinq -- le sixieme est
rem       ./rom/light_param/envmap_correct_<code>.txt (0x1800D727A), et il
rem       n existe PAS dans le dump VF5R de 2008 : c est un fichier de Final
rem       Showdown. Les 41 decors du jeu en ont un, donc il est obligatoire ;
rem     . il est desormais pris dans le .par sous le code du modele. Ce sont
rem       neuf nombres, sans nom de decor dedans : la recopie est exacte ;
rem     . un decor qui REMPLACE ne montrait pas le defaut : le code restant
rem       djo, l envmap_correct_djo.txt de l archive repondait encore. Seul
rem       l AJOUT expose le trou.
rem
rem   controle_decor_neuf.py verifie maintenant les DIX pieces : un controle
rem   qui n en voyait que neuf laissait passer la panne qu il doit attraper.
rem
rem   SI LE CHARGEMENT NE FINIT TOUJOURS PAS : depister_5r.cmd departage les
rem   sept portes de l etat 3 -- la porte la plus haute atteinte nomme la piece
rem   qui manque encore.
rem
rem   SI C EST ENCORE LA TRAINING ROOM : lancez pister_60_dojo.cmd. La sonde
rem   pose un point d arret sur l ecretage lui-meme et dit quelle valeur
rem   arrive, laquelle repart, et qui appelle.
rem
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
echo   MENU -^> DOJO -^> entrainement. Pas besoin de seconde manette.
echo   Le decor doit etre le dojo de 2008, avec SES BARRIERES de ring.
echo.
pushd "%~dp0..\runtime\media\vf5fs"
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
