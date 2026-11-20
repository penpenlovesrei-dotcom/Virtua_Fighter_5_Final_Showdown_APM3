@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- DURAL SELECTIONNABLE OU NON, SELON LE MODE. Double-cliquez.
rem
rem Il patche le moteur avec la SEPTIEME ligne d OPTIONS > Settings, puis
rem lance le jeu. Rien a taper.
rem
rem OU C EST :   OPTIONS > Settings > derniere ligne, " Dural ".
rem              Entree dessus ouvre une page a TROIS bascules :
rem                  Single Player   No / Yes
rem                  Offline VS      No / Yes
rem                  Online VS       No / Yes
rem              GAUCHE / DROITE changent la bascule.
rem              A (annuler) ou Entree reviennent a Settings.
rem
rem CE QU IL FAUT REGARDER, dans cet ordre :
rem
rem   1. la ligne " Dural " est bien la, en bas de Settings, et le cadre a
rem      grandi d une ligne (choice_win_08) ;
rem   2. Entree dessus ouvre la page des trois bascules. SI LE CADRE RESTE
rem      GRAND avec trois lignes dedans, ce n est pas une panne : cela veut
rem      dire que la composition de la fenetre est figee au demarrage de la
rem      scene, et qu il faudra la poser autrement ;
rem   3. mettez Single Player sur No, Offline VS sur Yes. Puis :
rem         SINGLE PLAYER > Arcade  -> la case de Dural doit avoir DISPARU
rem                                    de la grille (en bas a gauche) ;
rem         OFFLINE VERSUS          -> elle doit etre LA, et atteignable.
rem      Inversez les deux bascules et recommencez : le comportement doit
rem      s inverser.
rem
rem CE QUE CE REGLAGE NE FAIT PAS. " Online VS " n a rien a commander dans ce
rem build : l entree ONLINE VERSUS demande le mode 7, bouchonne a ses trois
rem gestionnaires. La bascule est posee et lue, aucun combat ne passe par la.
rem
rem ET IL N EST PAS GARDE D UNE SEANCE A L AUTRE : la valeur de depart est
rem celle du patch (oui / oui / oui par defaut). Pour partir autrement :
rem     py -3 tools\patch_moteur.py ... --options-dural 0,1,0
rem ---------------------------------------------------------------------------
setlocal enabledelayedexpansion
cd /d "%~dp0.."

if not exist "runtime\media\vf5fs\apm.dll" (
  echo   apm.dll manque. Lancez d abord tools\construire_stub.cmd
  pause
  exit /b 1
)

echo.
echo   Patch du moteur...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 ^
    --menu-fermer --options-raccourci --dojo-howto --dojo-cadre ^
    --options-sans-howto --options-sans-savedata ^
    --options-sans-credits --menu-exit --legende-sousmenu ^
    --attract-retour-titre --sans-now-loading --options-tips --boutons-xbox ^
    --sans-ecran-epilepsie ^
    --decor-perso trm --terminal-boutons --customize-curseur ^
    --replays-sans-gel --vignettes-costume --selitem-grille ^
    --selitem-republier --selitem-ecreter --selpart-curseur ^
    --item-basculer --sans-warning --options-resolution --options-mode ^
    --menu-v2 --sans-legende --options-dural >nul
if errorlevel 1 (
  echo.
  echo   Le patch a ECHOUE. Rien n a ete lance.
  pause
  exit /b 1
)
echo   fait.
echo.
echo   -------------------------------------------------------------------
echo    OPTIONS ^> Settings ^> derniere ligne : " Dural ".
echo    Entree dessus ouvre les trois bascules.
echo    Mettez Single Player sur No, puis SINGLE PLAYER ^> Arcade :
echo    la case de Dural doit avoir disparu de la grille.
echo   -------------------------------------------------------------------
echo.
cd /d "%~dp0..\runtime\media\vf5fs"
start "" vfes.exe
endlocal
