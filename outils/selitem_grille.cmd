@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LE CURSEUR DE "SELECT ITEM". Double-cliquez, rien a taper.
rem
rem CE QU'IL FAUT ESSAYER, et c'est tout :
rem   MENU -^> TERMINAL -^> Customize -^> choisir un personnage -^> Customization
rem   menu -^> une ligne qui ouvre une LISTE D'OBJETS en grille.
rem   Les quatre directions doivent y deplacer le cadre, case par case, et la
rem   grille doit DEFILER quand on depasse la cinquieme ligne.
rem
rem CE QUI A CHANGE PAR RAPPORT A console.cmd : une seule option de plus,
rem --selitem-grille. Tout le reste est le build valide.
rem
rem POURQUOI CA N'AVAIT JAMAIS MARCHE. Les quatre autres pages se reparent en
rem laissant vivre le compte que le moteur leur pose. Celle-ci, non : son
rem dessin ne lit pas le curseur du repartiteur, et c'est meme l'INVERSE --
rem 0x1801C7BF4 recalcule le curseur DEPUIS la grille a chaque trame. Lui
rem poser un compte ne pouvait rien donner, la trame suivante l'effacait.
rem
rem CE QU'ON A FAIT. Rien d'invente, et meme rien de transcrit :
rem   . le CONSOMMATEUR etait deja la, vivant -- 0x1801C7B83, le
rem     "consommateur de message mort". Il prend un index absolu et en fait
rem     le couple (position, defilement), ecretage au total et pas de huit
rem     compris. Il n'avait simplement plus d'appelant ;
rem   . le PRODUCTEUR a ete lu dans la version Xbox 360 (0x82230818) : huit
rem     colonnes, fenetre de quarante cases, soit cinq lignes ;
rem   . le raccord de 186 octets donne la grille au repartiteur en
rem     (ligne, colonne), le laisse travailler, et retraduit apres lui.
rem
rem SI LE CADRE NE BOUGE TOUJOURS PAS, la question suivante est : le
rem repartiteur accepte-t-il le deplacement ? Son accepteur de creneau 7/8
rem peut etre un bouchon, comme il l'etait pour le Character Select. C'est
rem tools\sonde_vignettes.py qui le dira, pas un reglage.
rem
rem Touches : fleches, Entree = valider, W = annuler, Echap = sortir.
rem LE DEMARRAGE EST LENT. Attendez le message ci-dessous.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- le curseur de "select item"
echo   ===================================================================
echo.
tasklist /fi "IMAGENAME eq vfes.exe" 2>nul | findstr /i "vfes.exe" >nul
if not errorlevel 1 (
  echo   vfes.exe TOURNE DEJA -- apm.dll est verrouillee et le patch
  echo   echouerait en silence cote copie. Fermez le jeu d'abord.
  pause
  exit /b 1
)
echo   Compilation de apm.dll...
py -3 tools\gen_apm_stub.py >nul
if errorlevel 1 (
  echo.
  echo   La compilation du apm.dll a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo   Patch du moteur...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 ^
    --menu-fermer --options-raccourci --dojo-howto --dojo-cadre ^
    --options-sans-howto --menu-exit --legende-sousmenu ^
    --attract-retour-titre --sans-now-loading --options-tips ^
    --decor-perso trm --terminal-boutons --customize-curseur ^
    --replays-sans-gel --vignettes-costume --selitem-grille >nul
if errorlevel 1 (
  echo.
  echo   Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   MENU -^> TERMINAL -^> Customize -^> un personnage -^> une liste d'objets.
echo   Les quatre directions doivent deplacer le cadre case par case.
echo.
echo   Le jeu tourne. Le demarrage est LENT, laissez-lui le temps.
echo.
cd /d "%~dp0..\runtime\media\vf5fs"
start "" vfes.exe
endlocal
