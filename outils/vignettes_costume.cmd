@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LE "Costume settings" : les vignettes, puis leur CURSEUR.
rem Double-cliquez. Ne touchez pas au clavier, le jeu se conduit tout seul.
rem
rem CE QUI EST DEJA ACQUIS, ET VU A L'ECRAN :
rem   . les six vignettes s'affichent en couleur, et elles SUIVENT le
rem     personnage choisi (Taka-Arashi au cran 18 montre bien ses costumes) ;
rem   . gauche/droite font defiler le Character Select.
rem   Il a fallu DEUX temps pour les vignettes, et le premier ne suffisait
rem   pas : charger la planche AVANT de dessiner, ET l'interroger a CHAQUE
rem   trame. Une planche que personne n'attend n'arrive jamais.
rem
rem CE QUE CET ESSAI VERIFIE MAINTENANT -- et c est nouveau :
rem   LES CINQ LIGNES "---" du premier ecran. Valider le personnage donne
rem   la main a la sous-page des donnees, dont le curseur vertical ne
rem   bougeait pas : aucun compte ne lui etait pose, et son second chemin
rem   d entree (par message) est coupe lui aussi -- l octet de type de ce
rem   message n est ecrit qu une fois dans tout le binaire, pour le mettre
rem   a zero. Le scenario enchaine six BAS de t=63 a t=66,5.
rem
rem   Et le CURSEUR du "Costume settings", deja valide par Frederic : dix
rem   droites de t=88 a t=101,5, pour qu une regression se voie.
rem
rem CE QUE LA REPONSE VOUDRA DIRE :
rem   . le cadre passe de Type A a Type B, C, D... -^> repare ;
rem   . le cadre reste sur Type A                  -^> le compte ne prend pas,
rem     ou un second verrou refuse (l'accepteur de vtable, voir le dossier).
rem
rem La premiere etape, tools\vignettes_costume.py, ne lance rien : elle
rem reconstruit la table 19 x 6 d'identifiants de sprite que 0x1801CB030
rem batit SUR LA PILE et la confronte a la base de sprites. Les 114
rem identifiants existent, ce sont les SPR_T_ITM<perso>_BODY01..06.
rem
rem Pour la question voisine -- le curseur du Character Select visite-t-il
rem les crans INTERMEDIAIRES ou saute-t-il a la butee ? -- c'est
rem tools\directions_select.cmd qu'il faut lancer, pas celui-ci.
rem
rem Le scenario d'entrees manuel est SAUVE avant et REMIS apres.
rem Sorties : analysis\sonde_vignettes.txt et les PNG dans analysis\sonde\.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- les vignettes de Costume settings
echo   ===================================================================
echo.
py -3 tools\vignettes_costume.py
echo.
echo   -------------------------------------------------------------------
echo    La sonde va LANCER LE JEU et le mener seule jusqu a Customize.
echo    Ne touchez pas au clavier pendant ce temps ^(environ deux minutes^).
echo   -------------------------------------------------------------------
echo.
pause
tasklist /fi "IMAGENAME eq vfes.exe" | find /i "vfes.exe" >nul
if not errorlevel 1 (
  echo   vfes.exe TOURNE DEJA. Fermez-le d abord.
  pause
  exit /b 1
)
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
py -3 tools\sonde_vignettes.py
echo.
pause
endlocal
