@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LE CURSEUR DU "Character Select" DEFILE-T-IL VRAIMENT ?
rem Double-cliquez. Ne touchez pas au clavier, le jeu se conduit tout seul.
rem
rem LA QUESTION QUI RESTE. Le curseur BOUGE, c'est acquis et vu a l'ecran :
rem Akira au cran 0, T-Arashi au cran 18. Mais le martelage qui l'a montre
rem ALTERNAIT gauche et droite, et les deux rebouclent sur l'autre butee : le
rem curseur n'a donc jamais visite un seul cran intermediaire. "Il decremente
rem avec rebouclage" et "il saute a la butee" produisent EXACTEMENT la meme
rem trace. Cet essai separe les deux, et lui seul.
rem
rem CE QU'IL FAIT AUTREMENT. Plus aucun appui "start" apres l'ouverture, donc
rem rien qui puisse quitter l'ecran ; et une DROITE TOUTES LES 0,3 SECONDE de
rem t=38 a t=100, soit plus de deux cents. Une droite ne valide rien et ne
rem ferme rien : la marteler partout ne coute que du temps, et un ecran qui ne
rem vivrait qu'une seconde en recoit quand meme trois.
rem
rem POURQUOI PAS UN INSTANT PRECIS. Les deux horloges ne sont pas la meme :
rem apm.dll date ses appuis depuis le premier appel d'Input_isOn, la sonde
rem depuis la creation du processus, et l'ecart varie de plusieurs secondes
rem d'un lancement a l'autre. Deux essais au scenario IDENTIQUE ont donne au
rem Character Select 2065 trames, puis 75.
rem
rem CE QUE LA REPONSE VOUDRA DIRE :
rem   . les crans se suivent 0,1,2,3...  -^> il DEFILE, tout est bon ;
rem   . il n'y a que 0 et 18             -^> il SAUTE A LA BUTEE, a reparer ;
rem   . COMPTE=5 au lieu de 18           -^> on est tombe dans Costume settings,
rem                                         l'ecran a ete quitte trop tot.
rem
rem Pour l'essai ordinaire -- les vignettes, et le curseur des costumes --
rem c'est tools\vignettes_costume.cmd qu'il faut lancer, pas celui-ci.
rem
rem Le scenario d'entrees manuel est SAUVE avant et REMIS apres.
rem Sorties : analysis\sonde_vignettes.txt, analysis\sonde\directions_t*.png
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- le curseur du Character Select defile-t-il ?
echo   ===================================================================
echo.
tasklist /fi "IMAGENAME eq vfes.exe" | find /i "vfes.exe" >nul
if not errorlevel 1 (
  echo   vfes.exe TOURNE DEJA. Fermez-le d abord.
  pause
  exit /b 1
)
echo   La sonde va LANCER LE JEU, le mener seule jusqu a Customize, puis
echo   marteler la direction DROITE pendant une minute.
echo   Ne touchez pas au clavier ^(environ deux minutes^).
echo.
pause
echo   Compilation de apm.dll et patch du moteur ^(~30 s^)...
py -3 tools\gen_apm_stub.py >nul
if errorlevel 1 ( echo   apm.dll n a pas compile. & pause & exit /b 1 )
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 ^
    --menu-fermer --options-raccourci --dojo-howto --dojo-cadre ^
    --options-sans-howto --menu-exit --legende-sousmenu ^
    --attract-retour-titre --sans-now-loading --options-tips ^
    --decor-perso trm --terminal-boutons --customize-curseur ^
    --replays-sans-gel --vignettes-costume --muet >nul
if errorlevel 1 ( echo   Le patch a ECHOUE. & pause & exit /b 1 )
py -3 tools\sonde_vignettes.py --directions
echo.
pause
endlocal
