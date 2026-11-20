@echo off
rem ---------------------------------------------------------------------------
rem Le corps commun des deux essais du mode TERMINAL. NE PAS double-cliquer :
rem utilisez tools\terminal.cmd ou tools\terminal_sans_wxga.cmd.
rem
rem   %1 = les options supplementaires passees au patcheur (entre guillemets)
rem   %2 = le libelle affiche a l'ecran
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- ESSAI DU MODE TERMINAL   %~2
echo   ===================================================================
echo.
tasklist /fi "IMAGENAME eq vfes.exe" | find /i "vfes.exe" >nul
if not errorlevel 1 (
  echo   vfes.exe TOURNE DEJA. Fermez-le d abord : on ne patche jamais un
  echo   moteur en cours d execution.
  pause
  exit /b 1
)

echo   Compilation de apm.dll...
py -3 tools\gen_apm_stub.py
if errorlevel 1 (
  echo.
  echo   apm.dll n a pas compile. Rien n a ete lance.
  pause
  exit /b 1
)

echo   Patch du moteur ^(~30 s^)...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 ^
    --menu-fermer --options-raccourci --dojo-howto --dojo-cadre ^
    --options-sans-howto --menu-exit --legende-sousmenu ^
    --attract-retour-titre --sans-now-loading --options-tips ^
    --decor-perso trm --terminal-boutons --customize-curseur --replays-sans-gel --vignettes-costume %~1
if errorlevel 1 (
  echo.
  echo   Le patch a ECHOUE. Rien n a ete lance.
  pause
  exit /b 1
)

echo.
echo   -------------------------------------------------------------------
echo    CE QUI A CHANGE DEPUIS VOTRE DERNIER ESSAI
echo   -------------------------------------------------------------------
echo    Vous aviez dit : "ENTREE valide, W annule, mais les fleches ne font
echo    bouger aucun curseur", et c etait pareil avec et sans --wxga.
echo.
echo    La cause est trouvee, et elle est mesuree. Le repartiteur des pages
echo    de menu ne deplace un curseur que si le COMPTEUR de la page est
echo    superieur a zero. Trois pages posent leur compte... puis l effacent
echo    quelques instructions plus loin, sur le meme chemin :
echo.
echo       TaskDataSelector   19 crans   le choix du personnage
echo       TaskCustomizeMenu   7 lignes  le Customization menu
echo       TaskExclWarning     2 lignes
echo.
echo    --customize-curseur neutralise ces trois effacements, et rien
echo    d autre. Aucune valeur inventee : 19, 7 et 2 sont les comptes que le
echo    moteur se donne lui-meme.
echo   -------------------------------------------------------------------
echo    CE QU IL FAUT REGARDER
echo   -------------------------------------------------------------------
echo    Deux fois ENTREE, puis TERMINAL, ENTREE.
echo.
echo    SUR "Customize" :
echo      1. Character Select : GAUCHE / DROITE doivent maintenant faire
echo         defiler les dix-neuf personnages, Akira, Pai, Lau...
echo      2. Espace ouvre le Customization menu : HAUT / BAS doivent y
echo         parcourir les SEPT lignes, de "Return to customization" a
echo         "Save and Exit".
echo      3. Dans "Costume settings", les six vignettes : --vignettes-costume
echo         charge la planche spr_t_itm du personnage avant de dessiner,
echo         et l interroge a chaque trame. Les images EXISTENT -- elles
echo         s affichent deja quand on rouvre l ecran plus tard.
echo      4. B recentre la camera, N change de vue, X tenu + fleches
echo         tournent le modele -- deja valide par vous.
echo.
echo    SUR "Replays" :
echo      "Your data" ne doit PLUS figer le jeu : la page se referme et on
echo      revient au menu TERMINAL. Le lecteur de reprises lui-meme reste
echo      mort -- son chargement est un bouchon dans ce build, et il n y a
echo      aucune reprise a lire. C est un REPLI, pas une reparation.
echo   -------------------------------------------------------------------
echo.
pushd "%~dp0..\runtime\media\vf5fs"
echo   Demarrage du jeu -- il met un moment a afficher.
start "" "%CD%\vfes.exe"
"%SystemRoot%\System32\timeout.exe" /t 8 /nobreak >nul 2>&1
tasklist /fi "IMAGENAME eq vfes.exe" | find /i "vfes.exe" >nul
if errorlevel 1 (
  echo.
  echo   LE JEU NE S EST PAS LANCE, ou il s est arrete aussitot.
) else (
  echo   Le jeu tourne.
)
popd
pause
endlocal
