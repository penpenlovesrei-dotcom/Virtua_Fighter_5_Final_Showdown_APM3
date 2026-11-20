@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LES DEUX TABLES DE DECORS DEPLACEES, A 41 DECORS
rem
rem Double-cliquez. C'est le build console habituel, a une chose pres : les
rem DEUX tables indexees par le decor ne sont plus dans .rdata, elles sont
rem dans une section a nous, avec leurs 556 relocations.
rem
rem CE QU'IL FAUT VERIFIER, ET C'EST TOUT L'INTERET
rem
rem   RIEN NE DOIT AVOIR CHANGE. Il y a toujours 41 decors, avec les memes
rem   descripteurs, aux memes index. Si quelque chose bouge, c'est le
rem   deplacement qui est faux -- et on veut le savoir MAINTENANT, avant
rem   d'ajouter un seul decor.
rem
rem   . STAGE SELECT : les 21 cases, les memes apercus, le meme curseur ;
rem   . un combat : le decor charge, son sol, ses murs, sa musique ;
rem   . la case SANCTUARY + BARRE ESPACE : les cinq decors de Dural defilent,
rem     et leur nom s'ecrit -- c'est le test le plus dur, il traverse les deux
rem     tables ;
rem   . TERMINAL : son decor `trm` ;
rem   . DOJO / entrainement : le dojo d'Akira, avec ses murs.
rem
rem CE QUI A CHANGE SOUS LE CAPOT
rem
rem   0x180403430   41 descripteurs de 0xF0 octets   -> section .decors +0
rem   0x18039F7A0   41 pointeurs de code 3 lettres   -> section .decors +0x2670
rem
rem   556 pointeurs suivent, chacun avec SA relocation, recopiee la ou
rem   .origine en a une. C'est ce que la greffe ne savait pas faire avant
rem   aujourd'hui, et c'est pour cela que le descripteur d'un decor ajoute
rem   restait ampute de ses murs et de ses neuf musiques.
rem
rem   AUCUNE borne n'est levee : on reste a 41. Le jour ou on passera a plus,
rem   ce sera `--decors-table <N>`, et on saura que le deplacement, lui, est
rem   deja bon.
rem
rem   Pour revenir a un build normal : n'importe quel autre lanceur. Le
rem   patcheur repart toujours de .origine.
rem
rem   Touches : fleches, Entree = VALIDER, W = ANNULER, Espace = SELECT,
rem             Echap = quitter le mode.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- LES DEUX TABLES DE DECORS DEPLACEES, A 41 DECORS
echo   ===================================================================
echo.
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1

rem ETAT DES FICHIERS : on le POSE, on ne l'herite pas -- MAIS on ne paie le
rem balayage du .par (16 s, muet) que s'il y a vraiment quelque chose a
rem retirer, et on DIT ce qu'on fait. Le fichier libre est la preuve qu'un
rem --poser est passe.
rem Sans cette garde, le lanceur restait CINQUANTE SECONDES sur une fenetre
rem noire sans un mot : la faute du journal 20, refaite le meme jour.
set "ETAT=0"
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgdjo.farc" set "ETAT=1"
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrm.farc" set "ETAT=1"
if exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgtrs.farc" set "ETAT=1"
if "%ETAT%"=="1" (
  echo   Un decor importe est en place : on le retire.
  echo   Chaque retrait balaie les 4 Go du .par -- comptez ~20 s chacun.
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
  echo   Etat des fichiers pose.
) else (
  echo   Aucun decor importe en place : rien a retirer.
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

echo   Patch du moteur, tables deplacees ^(~20 s^)...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso trm --variantes --variantes-texte --du2-collision --decors-table >nul
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  echo Relancez sans le ^>nul pour voir le refus :
  echo   py -3 tools\patch_moteur.py ... --decors-table
  pause
  exit /b 1
)

echo.
echo   Controle du deplacement, sans lancer le jeu :
echo.
py -3 tools\verifier_decors_table.py
if errorlevel 1 (
  echo.
  echo LE CONTROLE A ECHOUE -- voir la liste ci-dessus.
  echo Rien n'a ete lance.
  pause
  exit /b 1
)

echo.
echo   RIEN NE DOIT AVOIR CHANGE A L'ECRAN. Ce qu'il faut regarder :
echo     . STAGE SELECT : les 21 cases et leurs apercus ;
echo     . un combat : sol, murs, musique ;
echo     . SANCTUARY + BARRE ESPACE : les cinq Dural et leur nom ;
echo     . TERMINAL et le DOJO.
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
  echo LE JEU NE S'EST PAS LANCE, ou il s'est arrete aussitot -- c'est deja
  echo un resultat : le chargeur a refuse l'image, ou une table est fausse.
  pause
) else (
  echo   Le jeu tourne.
)
popd
pause
endlocal
