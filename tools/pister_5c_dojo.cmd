@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- QUI ECRIT L INDICE DE DECOR ? (point d arret MATERIEL)
rem
rem Double-cliquez, puis : MENU -> DOJO -> entrainement. Le decor charge doit
rem etre le dojo d'Akira de VIRTUA FIGHTER 5 R (2008), a l'indice 42 -- une
rem entree qui n'existe pas dans le jeu.
rem
rem AUCUNE SECONDE MANETTE N'EST NECESSAIRE.
rem
rem POURQUOI CE LANCEUR EXISTE
rem
rem   La sonde du 2026-09-09 n'a montre qu'UNE demande de decor pendant un
rem   combat : « index 39 (gym) ». Jamais 42. Le decor ajoute n'etait donc pas
rem   rejete -- il n'etait pas DEMANDE.
rem
rem   La raison est lisible en cinq instructions (0x18020AE50) : le mode DOJO
rem   A BIEN un ecran de selection de decor -- tranche par Frederic le
rem   2026-09-10, contre ce qui etait ecrit ici. Ce bloc-ci pose en dur --
rem   39 (gym, la Training Room) ou 11 (djo, le dojo d'Akira) selon un
rem   drapeau. C'est ce qu'on voyait a l'ecran.
rem
rem   `--dojo-decor 42` remplace le 11 par notre indice. C'est le seul chemin
rem   qui rende un decor ajoute visible sans passer par OFFLINE VERSUS.
rem
rem CE QUE CETTE MESURE CHERCHE
rem
rem   dojo_5r.cmd charge la Training Room (39) au lieu du decor 42, alors que
rem   le temoin (--dojo-decor 11) charge bien le dojo de Final Showdown. Le
rem   patch EST pose : `mov ecx, 42` est dans le binaire, verifie.
rem
rem   L'indice 42 est donc PRODUIT puis remplace quelque part. Trois points
rem   d'arret le disent en une seule partie :
rem
rem     0x18020AE78   le choix en dur du mode 1   -> eax, 42 ou 39 ?
rem     0x1800BC6AD   la demande du combat        -> ecx, l'indice demande
rem     0x1800D7130   le chargeur                 -> l'indice charge
rem
rem   . si le CHOIX donne 42 et la DEMANDE 39, le remplacement est entre les
rem     deux, et c'est la que je chercherai ;
rem   . si le CHOIX donne deja 39, c'est que ce n'est pas ce site-la qui
rem     decide, et le temoin nous a trompes tous les deux.
rem
rem   Le journal s'ecrit AU FIL DE L'EAU dans analysis\pister_decor.txt.
rem   Envoyez-moi les lignes « CHARGEMENT » et « choix / demande ».
rem
rem CE QU'IL FAUT REGARDER
rem
rem   . le decor doit etre le dojo de 2008 : ses textures sont deux fois plus
rem     lourdes qu'en Final Showdown (40,8 Mo contre 20,9), ca devrait se voir ;
rem   . SES MURS doivent etre la -- un ring out dans un dojo n'existe pas. Si
rem     le personnage passe au travers, c'est +0xC0 qui n'est pas suivi ;
rem   . la musique doit jouer.
rem
rem   SI LE JEU BOUCLE SUR L'ECRAN DE CHARGEMENT : fermez-le et dites-le-moi.
rem   Le decor est alors demande mais une piece manque, et il y a sept portes
rem   a departager -- c'est un tout autre resultat que « rien ne se passe ».
rem
rem   Pour comparer : dojo_5r_temoin.cmd rend le meme build avec --dojo-decor
rem   11, c'est-a-dire le dojo d'origine. Le meme mode, le meme chemin, un
rem   seul chiffre de difference.
rem
rem   Pour tout rendre : decor_ajoute_retirer.cmd
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- qui ecrit l indice de decor ? (DR en ecriture)
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
echo   MENU -^> DOJO -^> entrainement. Pas besoin de seconde manette.
echo   Le decor doit etre le dojo de 2008, avec SES MURS.
echo.
echo   Le jeu demarre SOUS DEBOGUEUR. Le clavier est a vous.
echo   MENU -^> DOJO -^> entrainement, puis fermez le jeu.
echo.
py -3 tools\pister_5c_stage.py --secondes 300
echo.
echo   Le journal : analysis\pister_5c_stage.txt
echo.
pause
endlocal
