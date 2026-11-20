@echo off
rem -----------------------------------------------------------------------
rem VF5 FS -- LE MODE QUEST
rem
rem Double-cliquez. Puis, DANS LE MENU DU JEU, choisissez QUEST MODE.
rem
rem LA LIGNE QUEST MODE (mesure le 2026-10-19). Elle etait deja
rem degrisee, selectionnable et reliee -- rien n a ete ajoute :
rem
rem  . SON ETAT VAUT 0 D OFFICE. Le balayage de TOUTES les
rem    ecritures immediates dans le tableau d etats du .origine
rem    (page + 0x642 + i) rend +0x643, +0x644, +0x646, +0x648,
rem    +0x64A et +0x64B -- JAMAIS +0x645, qui est l entree 3. Ce
rem    lanceur n a pas --menu-griser, donc personne ne la grise.
rem  . LES DEUX GARDES PASSENT A L ETAT 0 : le validateur
rem    0x1801DDF54 (cmp byte [rcx+rdi+0x642],0 / je) prend la
rem    branche utile, et le creneau de curseur 0x1801E4CD8 ne
rem    refuse que les etats non nuls.
rem  . ET --quest-ecran LA CABLE DEJA. Relu dans la DLL produite :
rem        0x1801DE0B1  cmp ecx, 3
rem        0x1801DE0B4  jne 0x1801DE0C5
rem        0x1801DE0B6  mov rbx, [rsp+0x30]
rem        0x1801DE0BB  add rsp, 0x20
rem        0x1801DE0BF  pop rdi
rem        0x1801DE0C0  jmp 0x180EA2FA0   <- la greffe
rem    La queue d appel de la branche morte (ex-ACHIEVEMENTS, qui
rem    etait un jmp vers ret 0) est remplacee : cinq octets pour
rem    cinq, l epilogue a tourne, rien a ranger au retour.
rem
rem SCOREBOARDS, LUI, N OUVRE PAS LE QUEST : sa branche garde son
rem call 0x1801B0120, la page des classements. L en-tete de ce
rem lanceur disait le contraire, et il avait tort.
rem
rem   L etat employe est DATA_TEST / sous-etat 35, entierement bouchonne
rem   dans Final Showdown. ONLINE n est pas touche.
rem
rem A LA PREMIERE ENTREE : LA CREATION DE DONNEES
rem   Le Quest commence par le CHOIX D UN PERSONNAGE et la creation de ses
rem   donnees, comme en 2007 : NO-NAME, grade 10th kyu, et 50 000 G qui se
rem   versent sous vos yeux (+500 par trame, un son toutes les trois).
rem   Le message d introduction est celui du jeu, libelle 523.
rem
rem SUR LA CARTE
rem   GAUCHE / DROITE  deplacer le repere d un lieu a l autre (neuf lieux)
rem   ENTREE           entrer : la photographie du lieu
rem   W (carre)        revenir au menu
rem   En bas a gauche, la fiche du joueur : nom, grade, W, L, win ratio,
rem   argent. Le picto du grade vient de la planche de 2007.
rem
rem UN LIEU OUVERT
rem   GAUCHE / DROITE  la fenetre : le lieu, les joueurs, le statut
rem   HAUT / BAS       le curseur : la ligne du menu, ou le rival
rem   ENTREE           sur une BORNE : l ecran de RENCONTRE, puis le combat
rem   T (L1)           la voie du combat : composee (par defaut) ou par le
rem                    selecteur d arcade
rem   W (carre)        revenir a la carte
rem
rem LA BOUTIQUE, LES TOURNOIS, LES EMBLEMES
rem   La MAISON : Customize ouvre la boutique, Quest settings regle la
rem   difficulte (elle donne +0,2 ou +0,4 a la force du CPU, comme 2007).
rem   Une SALLE : sa cinquieme entree est Customize.
rem   Le DOME : sa premiere entree ouvre un TOURNOI de trois tours.
rem   Le STATUT : ENTREE y ouvre la liste des emblemes.
rem
rem   Les objets, leurs noms et leurs PRIX viennent du jeu : la colonne
rem   Point du CSV de Final Showdown, et les noms anglais de 2007.
rem
rem AVANT ET APRES LE COMBAT
rem   L ecran de RENCONTRE montre le rival, son grade et ses deux repliques
rem   (npc_tbl +0x04 et +0x08). Apres, le verdict est lu dans la session
rem   ([session+0x4E0+0x1054] : le vainqueur), le bit battu se pose, la
rem   serie monte, l argent tombe et le grade suit.
rem
rem LA MUSIQUE
rem   vf5ps3_b03map.adx, le morceau que TaskQuestMap, TaskQuestHomeMenu et
rem   TaskQuestTenpo demandent dans le code de 2007. Final Showdown ne l a
rem   pas ; tools\musique_quest.py le pose.
rem
rem LE PROFIL
rem   quest_profil.bin, a cote du jeu : les rivaux rencontres et battus
rem   (deux champs de mille bits), le temps de jeu, les combats, la
rem   carriere et les objets possedes. Il SURVIT AU REDEMARRAGE.
rem     py -3 tools\profil_quest.py --lire
rem
rem Pour tout rendre : relancez n importe quel autre lanceur.
rem -----------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- le mode QUEST (menu : SCOREBOARDS)
echo   ===================================================================
echo.
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1

echo   Bases 2D : les planches du Quest...
py -3 tools\bases_2d.py --controle
if errorlevel 1 (
  py -3 tools\bases_2d.py --ajouter que qwin tnt tnto qdan
  if errorlevel 1 (
    echo.
    echo Les bases 2D ont ECHOUE. Rien n a ete lance.
    pause
    exit /b 1
  )
)

echo   Textes du Quest ^(492 chaines, ajoutees a string_array^)...
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

echo   La musique du Quest ^(vf5ps3_b03map.adx^)...
py -3 tools\musique_quest.py --controle
if errorlevel 1 py -3 tools\musique_quest.py --ajouter

echo   La table des objets de la boutique...
py -3 tools\objets_quest.py --ecrire

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
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso djo --decors-dural cas --variantes --du2-collision --bases-2d-libres --quest-ecran --textes-quest --terminal-boutons --customize-curseur --replays-sans-gel --vignettes-costume --menu-v2 --sans-legende
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n a ete lance.
  pause
  exit /b 1
)

echo.
echo   Dans le MENU du jeu : QUEST MODE ouvre le mode Quest.
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
