@echo off
rem -----------------------------------------------------------------------
rem VF5 FS -- LE TEMOIN DE CONTROLE DU TEXTE
rem
rem Double-cliquez. C est `quest.cmd`, plus DEUX textes que le MOTEUR dessine
rem LUI-MEME. Ils ne viennent pas de nous : ce lanceur retire l option qui
rem coupe le premier et allume le second.
rem
rem   1. NOW LOADING          pendant les ecrans de chargement
rem   2. le nom de variante   sur l ecran de CHOIX DU DECOR, sous l apercu
rem      (la barre espace fait defiler VIRTUA FIGHTER 5 FS / VIRTUA
rem      FIGHTER 5 R sur la case du dojo)
rem
rem A QUOI CA SERT. Le jour ou le texte du Quest ne sort plus, ce lanceur
rem tranche en UN essai :
rem
rem   ces deux-la sortent, le Quest non   -^> c est NOTRE appel
rem   aucun des deux ne sort              -^> c est le moteur (la police, le
rem                                          contexte 2D, l ecran)
rem
rem C est ainsi que la question a ete tranchee le 2026-09-26, apres quatre
rem seances sans texte : voir REPRISE (71) et la section 9.16 de
rem analysis/mode_quest.md. La reponse fut "c est notre appel" -- il
rem manquait trois gestes que Final Showdown fait et que nous ne faisions
rem pas, a commencer par monter le calque du contexte 2D a 2 (0x180187CB0)
rem et le remettre ensuite, exactement comme la Xbox 360.
rem
rem Le Quest marche comme d habitude : dans le MENU, SCOREBOARDS.
rem Pour tout rendre : relancez n importe quel autre lanceur.
rem -----------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- le temoin de controle du texte (les deux du moteur)
echo   ===================================================================
echo.
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1

echo   Bases 2D : les quatre planches du Quest...
py -3 tools\bases_2d.py --controle
if errorlevel 1 (
  echo.
  echo   Les planches du Quest ne sont pas declarees : on les ajoute.
  py -3 tools\bases_2d.py --ajouter que qwin tnt tnto
  if errorlevel 1 (
    echo.
    echo Les bases 2D ont ECHOUE. Rien n a ete lance.
    pause
    exit /b 1
  )
)

echo   Textes du Quest ^(83 chaines, ajoutees a string_array^)...
py -3 tools\textes_quest.py --controle
if errorlevel 1 (
  py -3 tools\textes_quest.py --ajouter
  if errorlevel 1 (
    echo.
    echo Les textes du Quest ont ECHOUE. Rien n a ete lance.
    pause
    exit /b 1
  )
)

echo   Les mille rivaux ^(npc_tbl.bin, absent de Final Showdown^)...
py -3 tools\rivaux.py --controle
if errorlevel 1 (
  py -3 tools\rivaux.py --ajouter
  if errorlevel 1 (
    echo.
    echo La table des rivaux a ECHOUE. Rien n a ete lance.
    pause
    exit /b 1
  )
)

echo   Compilation de apm.dll...
py -3 tools\gen_apm_stub.py
if errorlevel 1 (
  echo.
  echo apm.dll n a pas compile. Rien n a ete lance.
  pause
  exit /b 1
)

echo   Patch du moteur ^(~30 s^)...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --options-tips --decor-perso djo --decors-dural cas --variantes --variantes-texte --du2-collision --bases-2d-libres --quest-ecran --textes-quest
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n a ete lance.
  pause
  exit /b 1
)

echo.
echo   TEMOINS DU MOTEUR : NOW LOADING au chargement, et le nom de
echo   variante sous l apercu de l ecran de choix du decor.
echo   Le Quest, lui, s ouvre par SCOREBOARDS dans le MENU.
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
