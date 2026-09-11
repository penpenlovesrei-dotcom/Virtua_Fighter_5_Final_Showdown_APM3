@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- BUILD D'ESSAI : LES CINQ DECORS DE DURAL, A LA PLACE DE CINQ AUTRES
rem
rem Double-cliquez. C'est le build console complet (console.cmd) plus les
rem correctifs "decors de Dural".
rem
rem 1) LE COMBAT  (--decors-dural cas)          VALIDE A L'ECRAN le 2026-09-07
rem
rem    Le decor d'un combat solo n'est pas choisi par le code : c'est le decor
rem    MAISON DE L'ADVERSAIRE, une donnee de rom/game_score.txt. Quand ce decor
rem    est celui de Dural (21 = du1), le jeu appelait 0x1800B2330 pour choisir
rem    parmi les cinq -- un BOUCHON de six octets qui rend toujours 22 (du2).
rem    Le correctif traduit cinq decors consecutifs, en place, sans caverne :
rem
rem      cas (7)  -> DU1     decor maison de LION
rem      riv (8)  -> DU2     decor maison de SHUN DI
rem      jin (9)  -> DU3     decor maison de AOI
rem      sin (10) -> DU4     decor maison de LEI-FEI
rem      djo (11) -> DU5     decor maison de AKIRA
rem
rem    Et le combat contre DURAL rend desormais DU1 au lieu du bouchon DU2.
rem
rem 2) LA GRILLE  (--decors-dural-grille)
rem
rem    La meme substitution du1 -> du2 existait a TROIS autres endroits, du
rem    cote de l'ecran : 0x180174494 (un immediat, dans TaskSelStage::update
rem    -- c'est LUI qui decidait du decor charge, et il manquait au premier
rem    jet : d'ou "DU1 = DU2" a l'essai), 0x180175320 (un jne) et 0x180175390
rem    (un cmove, chemin APM3). Les trois sont levees -- les enumerer d'un
rem    coup se fait avec tools\substitutions.py 0x15 0x16.
rem    Et quatre cases de la grille passent aux
rem    decors de Dural -- la case dur garde du1, donc les CINQ y sont, sans
rem    doublon :
rem
rem      ligne 0 :  are   nyc   slk   DU4   cas   DU2   smo
rem      ligne 1 :  tak   bar   DU5   ALEA  DU3   ter   ban
rem      ligne 2 :  hai   tan   gym   yuk   aur   umi   DU1
rem
rem 3) LES ICONES : ON NE PEUT PAS, et l'essayer casse tout
rem
rem    L'icone et le nom sous chaque case sont PEINTS par la scene AET
rem    SEL_STAGE ; ils ne sont pas dans la table. Le champ que j'avais pris
rem    pour l'icone (+0x18) est en fait l'ANCRAGE : le sprite dont le
rem    constructeur de grille (0x180173BD0) lit les x,y pour placer la case.
rem    Le repointer empile les cases au meme endroit -- le curseur n'en
rem    atteint plus qu'une, et la selection rend n'importe laquelle. Essaye
rem    le 2026-09-07, casse a l'ecran, RETIRE : le patcheur refuse l'option.
rem
rem 4) UN DEFAUT DU BUILD D'ORIGINE  (--du2-collision)
rem
rem    Observation : en ring out, le personnage se pose sur un sol qui n'existe
rem    pas, alors qu'il devrait chuter beaucoup plus bas. Le descripteur de DU2
rem    pointe sa collision sur celle de DU1 -- alors que STGDU2_COLI.000.bin
rem    existe dans le .par (3984 octets contre 5744, donc une AUTRE forme) et
rem    que la chaine "rom/STGDU2_COLI.000.bin" n'a jamais ete emise dans le
rem    binaire. DU2 partageait le sort de trm/cid/trs, les decors d'essai sans
rem    collision propre. Le correctif ecrit la chaine manquante dans le mou de
rem    fin de .rdata et repointe le descripteur.
rem    Pour comparer avant/apres : retirer --du2-collision.
rem
rem COMMENT LES VOIR
rem
rem   . DOJO / entrainement : le decor suit le personnage du PARTENAIRE.
rem     Lion -> DU1, Shun Di -> DU2, Aoi -> DU3, Lei-Fei -> DU4, Akira -> DU5.
rem     C'est le plus confortable : rien a gagner, on tourne autour du decor.
rem   . OFFLINE VERSUS : idem, en prenant l'un d'eux comme adversaire.
rem   . SINGLE PLAYER > Arcade (route A) : les cinq dans une seule partie,
rem     combats 3, 4, 6, 7 et 8.
rem   . STAGE SELECT : cinq cases, reperees dans la grille ci-dessus.
rem
rem   Pour comparer avec l'original : relancez console.cmd.
rem   Pour voir UN decor precis tout de suite : decor_perso.cmd du3
rem
rem   Touches : fleches, Entree = VALIDER, W = ANNULER, X C V = croix rond
rem             triangle, Espace = SELECT, Echap = quitter le mode.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\gen_apm_stub.py >nul
if errorlevel 1 (
  echo.
  echo La compilation du apm.dll a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso trm --decors-dural cas --decors-dural-grille --du2-collision
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   LES CINQ DECORS DE DURAL SONT EN PLACE.
echo.
echo   Le plus simple : DOJO, partenaire =
echo      Lion -^> DU1   Shun Di -^> DU2   Aoi -^> DU3   Lei-Fei -^> DU4   Akira -^> DU5
echo.
echo   A regarder : le RING OUT sur DU2, dont la VRAIE collision est chargee.
echo   Dans la grille, les cinq cases gardent l'icone du decor d'origine :
echo   c'est une limite, pas un oubli -- l'icone est peinte dans la scene 2D.
echo.
cd /d "%~dp0..\runtime\media\vf5fs"
start "" vfes.exe
endlocal
