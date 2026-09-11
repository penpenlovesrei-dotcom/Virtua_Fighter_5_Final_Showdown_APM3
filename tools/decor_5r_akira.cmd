@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- BUILD D'ESSAI : LE DOJO D'AKIRA, VERSION VF5 R (2008)
rem
rem Double-cliquez. C'est le build console complet, PLUS le decor DJO de
rem Virtua Fighter 5 R substitue a celui de Final Showdown.
rem
rem CE QUI EST REMPLACE, ET POURQUOI C'EST TOUT
rem
rem   Le jeu complet du decor vient de VF5 R -- geometrie, collision,
rem   animation, effets et eclairage :
rem
rem     rom/objset/stgdjo.farc        19,0 Mo  (Final Showdown : 10,5 Mo)
rem     rom/STGDJO_COLI.000.bin        7 920 o (Final Showdown : 4 305 o)
rem     rom/auth_3d/STGDJO.farc
rem     rom/auth_3d/EFFSTGDJO.farc
rem     rom/ibl/djo.ibl
rem     rom/light_param/{light,fog,glow,wind}_djo.txt
rem
rem   Les huit noms sont masques dans l'index de vf5fs_data.par (un octet
rem   chacun) pour que le moteur retombe sur l'arborescence libre.
rem
rem   AUCUN OCTET DU MOTEUR N'EST TOUCHE POUR CE DECOR. La raison est une
rem   mesure : les cinq objets principaux portent les MEMES identifiants dans
rem   les deux generations -- gnd 114, reflect 115, sdw 116, sky 117, ring 118.
rem   Le descripteur du moteur (0x180403430 + 11*0xF0) demande deja
rem   114 118 117 116 115. Les 52 objets que Final Showdown a en plus sont des
rem   effets, numerotes 0 a 113 : ils ne sont pas dans le descripteur.
rem
rem   L'essai du 2026-09-03 bouclait sur l'ecran de chargement parce qu'il
rem   posait le seul objset de R a cote de l'auth_3d, des effets et de la
rem   collision de Final Showdown. Ce n'etait pas le format, c'etait le
rem   melange : un decor s'importe avec sa generation ENTIERE.
rem
rem CE QU'IL FAUT REGARDER
rem
rem   . DOJO / entrainement, partenaire = AKIRA : son decor maison est DJO.
rem   . STAGE SELECT : la case du dojo, LIGNE 1 (celle du milieu), COLONNE 2 --
rem     l'icone ne change pas, c'est le decor derriere qui change.
rem   . OFFLINE VERSUS avec Akira en face, ou Arcade route A.
rem
rem   L'ecart annonce par les fichiers : R a 40,8 Mo de textures contre 20,9 Mo
rem   en Final Showdown, et 119 objets contre 171. Les textures ont ete
rem   divisees par deux au passage a FS -- c'est ce qui devrait se voir.
rem
rem   SI LE JEU BOUCLE SUR L'ECRAN DE CHARGEMENT : lancez decor_5r_retirer.cmd,
rem   tout revient a l'etat d'origine. Puis dites-le-moi : ce sera l'eclairage
rem   (djo.ibl) ou l'auth_3d, et on les isole un par un.
rem
rem   Touches : fleches, Entree = VALIDER, W = ANNULER, X C V = croix rond
rem             triangle, Espace = SELECT, Echap = quitter le mode.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
rem ETAT DES FICHIERS : on le POSE, on ne l'herite pas.
rem Le patcheur repart de .origine ; cote fichiers, c'est cette ligne.
rem Sans elle, le dojo VF5 R pose par decor_5r_akira.cmd restait en place
rem dans tous les autres lanceurs.
py -3 tools\importer_decor.py --retirer trm >nul 2>&1
py -3 tools\importer_decor.py --retirer trs >nul 2>&1
rem Le decor AJOUTE (d5r, indice 42) est plus recent que ce lanceur : il
rem pose des fichiers libres ET ecrit obj_db DANS le .par. Sans cette ligne,
rem ce build-temoin heriterait de son etat.
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgd5r.farc" py -3 tools\decor_neuf.py --retirer d5r
rem Le decor AJOUTE (d5r, indice 42) est plus recent que ce lanceur :
rem il pose des fichiers libres ET ecrit obj_db DANS le .par. Sans cette
rem ligne, ce build-temoin heriterait de son etat.

py -3 tools\importer_decor.py --poser djo --source VF5R
if errorlevel 1 (
  echo.
  echo La pose du decor a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
py -3 tools\gen_apm_stub.py
if errorlevel 1 (
  echo.
  echo La compilation du apm.dll a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso djo --du2-collision
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
py -3 tools\pister_import.py djo --controle
if errorlevel 1 (
  echo.
  echo LE CONTROLE AVANT VOL A ECHOUE -- voir la liste ci-dessus.
  echo Rien n'a ete lance : le jeu aurait tourne en boucle sans rien dire.
  pause
  exit /b 1
)
echo.
echo   LE DOJO DE VF5 R EST EN PLACE.
echo.
echo   Le plus simple : DOJO, partenaire = AKIRA.
echo   Sinon STAGE SELECT, case du dojo : ligne du milieu, 3e colonne.
echo.
echo   SI CA BLOQUE SUR L'ECRAN DE CHARGEMENT : fermez le jeu et lancez
echo   depister_5r.cmd -- il relance sous instruments et nomme la piece
echo   fautive (objset, collision, auth_3d, eclairage ou son).
echo   Pour revenir a l'original : decor_5r_retirer.cmd
echo.
pushd "%~dp0..\runtime\media\vf5fs"
if not exist vfes.exe (
  echo INTROUVABLE : "%CD%\vfes.exe"
  pause
  popd
  exit /b 1
)
start "" "%CD%\vfes.exe"
"%SystemRoot%\System32\timeout.exe" /t 4 /nobreak >nul 2>&1
tasklist /fi "IMAGENAME eq vfes.exe" | find /i "vfes.exe" >nul
if errorlevel 1 (
  echo.
  echo LE JEU NE S'EST PAS LANCE, ou il s'est arrete aussitot.
  echo   Lancez depister_5r.cmd : il demarre le jeu sous debogueur et
  echo   ecrit ce qui se passe dans analysis\pister_import_djo.txt
  pause
) else (
  echo   Le jeu tourne.
)
popd
endlocal
