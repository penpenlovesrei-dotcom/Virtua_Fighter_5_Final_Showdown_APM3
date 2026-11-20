@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LE MODE QUEST, SUR LA BUILD COMPLETE. Double-cliquez.
rem
rem   Dans le MENU du jeu : QUEST MODE, la ligne 3.
rem
rem POURQUOI CE LANCEUR, ET PAS tools\quest.cmd (2026-10-19)
rem
rem   quest.cmd est une REGRESSION : 37 options la ou celui-ci en porte
rem   65. Il lui manque tout le travail des trois dernieres semaines --
rem   OPTIONS refondu, la manette du joueur 2, VF.TERMINAL, le Movie
rem   Theater, les quatre-vingt-six decors, la grille select item, les
rem   variantes, le nom de donnees... vingt-neuf options en tout.
rem
rem   Celui-ci part donc de item_porte.cmd et n AJOUTE que ce que le
rem   mode Quest demande :
rem
rem     --bases-2d-libres  le moteur lit ./rom/2d/, ou les planches du
rem                        Quest sont declarees (tools/bases_2d.py)
rem     --quest-ecran      la greffe de l ecran, posee sur la branche
rem                        morte de la ligne 3 (0x1801DE0C0)
rem     --textes-quest     les 492 chaines du mode, resolvables
rem     --quest-degriser   item_porte grise QUEST MODE avec ONLINE
rem                        VERSUS en UNE instruction ; cette option
rem                        passe l immediat de 0x1801E3A0A de 0x0101 a
rem                        0x0001, et rend la ligne 3 a l etat 0
rem
rem   Tout le reste est celui de item_porte.cmd, mot pour mot.
rem
rem IL TOURNE A PLEINE VITESSE : plus de debogueur. La sonde faisait tomber le
rem jeu a 25 images par seconde, et on ne juge pas une manette a 25 images par
rem seconde. Ce qu'il fallait mesurer, le apm.dll l'ecrit maintenant tout seul
rem dans un fichier (voir plus bas).
rem
rem TROIS CHOSES A ESSAYER, et elles sont independantes.
rem
rem  1. LA MANETTE. Elle double le clavier sur le JOUEUR 1.
rem        croix / stick gauche  les directions
rem        START **ou A**        valider
rem        X     **ou B**        annuler
rem     C'ETAIT LA LE DEFAUT : dans les menus le moteur ne lit QUE deux codes,
rem     le 7 (valider) et le 8 (annuler). START portait le 7, X le 8, et le
rem     bouton A -- celui que tout le monde presse -- ne portait aucun des
rem     deux. "seul le bouton start fonctionne" etait donc exact, et par
rem     construction. A et B sont desormais des DOUBLES, pas des accords : un
rem     masque a deux bits voulait dire "les deux tenus ensemble", d'ou un
rem     second masque par code.
rem
rem  2. L'ECRAN WARNING, entre le titre et le menu. Le premier correctif etait
rem     un FAUX : il changeait `je` en `jmp` vers LA MEME cible, et cette
rem     branche etait deja prise a chaque trame. Il ne faisait rien, et c'est
rem     pour ca que l'ecran etait toujours la. `TaskCsWarning::update` rend
rem     maintenant "termine" des la premiere trame.
rem
rem  3. L'ECRAN "select part" -- navigation a DEUX ETAGES, et cette fois
rem     la cause du plantage est MESUREE de bout en bout.
rem        GAUCHE / DROITE  change de bloc  (head, face, arms, upper, lower)
rem        HAUT   / BAS     parcourt les sous-parties DU bloc
rem
rem     LE PLANTAGE N'ETAIT PAS LE RELAIS. La sonde a montre, au moment de
rem     valider : categorie=0, sous-partie=1, compte du bloc=3, ids 0 1 2
rem     puis les sentinelles -1, ID retenu = 1. Tout etait juste.
rem
rem     LA FAUTE EST UN DEBORDEMENT DE TABLEAU DU MOTEUR. Un point d'arret
rem     materiel sur la globale 0x180752610 a nomme ses auteurs : la boucle
rem     de remplissage des cases de "select item" (0x1801CC260) a marche
rem     jusqu'a la case 207 d'un tableau qui n'en porte que 128, et a mange
rem     le pointeur du composite de personnalisation. 0x1801C7589 le
rem     dereference ensuite SANS test : c'est la que ca plantait.
rem
rem     128 n'est pas un nombre choisi : la structure est a adresse fixe,
rem     son tableau commence en +0x74, son compte est en +0x274, donc
rem     (0x274-0x74)/4 = 128 cases. Le moteur y posait le nombre d'objets
rem     de la liste SANS ecretage. --selitem-ecreter l'ecrete.
rem
rem     ET LA NAVIGATION DESARMEE LE CACHAIT : sans elle on n'atteignait
rem     que la premiere sous-partie de chaque bloc, qui porte moins de 128
rem     objets. Le defaut etait la depuis toujours.
rem
rem     ET ON A MAINTENANT TOUS LES OBJETS. La structure est REPUBLIEE dans
rem     la greffe (--selitem-republier) : son tableau passe de 128 a 512
rem     cases. 512 n'est pas un nombre choisi -- chritm_tbl porte 14 444
rem     objets sur 20 personnages, et comptes par (Category, Position) le
rem     pire cas est Kage, ATAM/KAMI (les cheveux), avec 227 objets. Puis
rem     Aki 193, Jacky 188, Shun 185. 512 fait plus du double du pire cas.
rem
rem     Dix-sept deplacements corriges SUR PLACE, sans un seul relais : la
rem     queue de la structure porte deja des disp32. L'ecretage reste, en
rem     filet et non en limite.
rem
rem CE QUI EST DEJA VALIDE A L'ECRAN, et qu'on ne defait pas :
rem   . --selitem-grille   la grille "select item"
rem   . --item-basculer    le modele 3D de l'objet sur le personnage
rem
rem ===========================================================================
rem LE JOURNAL DE LA MANETTE, sans debogueur et sans ralentissement.
rem
rem   runtime\media\vf5fs\apm_journal.txt
rem
rem Trois sortes de lignes, et RIEN quand rien ne change :
rem
rem   PAD    0x1000  A              l'etat BRUT de la manette a change
rem   MASQUE 0x000280  codes 7 9    ce que le stub en a tire
rem   LU     Input_isOn(7) = OUI    ce que le MOTEUR a demande et obtenu
rem
rem Les trois separent les trois pannes possibles :
rem   pas de ligne PAD du tout     -^> la manette n'arrive pas au stub
rem   PAD oui, MASQUE sans le code -^> elle arrive sur le mauvais code
rem   MASQUE oui, pas de LU        -^> l'ecran courant ne lit pas ce code
rem Ce lanceur l'affiche a la fin.
rem ===========================================================================
rem
rem ===========================================================================
rem LA RESOLUTION SE CHOISIT MAINTENANT DANS LE JEU.
rem
rem   OPTIONS ^> Settings ^> cinquieme ligne, "Resolution"
rem   GAUCHE / DROITE  1280x720, 1600x900, 1920x1080, 2560x1440, 3840x2160
rem   puis VALIDEZ     le jeu se ferme et CE LANCEUR LE ROUVRE aussitot
rem
rem POURQUOI IL SE FERME, et ce n'est pas un defaut : la chaine d'echange de
rem vfes.exe et les cibles de rendu du moteur sont creees UNE FOIS au
rem demarrage, depuis quatre immediats statiques. Rien dans ce jeu ne sait
rem changer de resolution a chaud -- et le releve de ce chantier note qu'y
rem toucher a l'execution l'avait rendu injouable. On relance donc, ce qui
rem prend le temps d'un demarrage.
rem
rem Le choix vit dans runtime\media\vf5fs\ram\resolution.txt, en clair. Si ce
rem fichier n'existe pas, on demarre en 1280x720 -- la resolution validee a
rem l'ecran.
rem ===========================================================================
rem
rem Clavier : fleches, Entree = valider, W = annuler, Echap = sortir du mode.
rem LE DEMARRAGE EST LENT. Laissez-lui le temps.
rem ---------------------------------------------------------------------------
setlocal enabledelayedexpansion
cd /d "%~dp0.."
set "RESFIC=runtime\media\vf5fs\ram\resolution.txt"
set "MODFIC=runtime\media\vf5fs\ram\mode.txt"
set "BTNFIC=runtime\media\vf5fs\ram\boutons.txt"
echo.
echo   ===================================================================
echo    VF5 -- la resolution se choisit dans OPTIONS ^> Settings
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
py -3 tools\gen_apm_stub.py
if errorlevel 1 (
  echo.
  echo   La compilation du apm.dll a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
if exist "runtime\media\vf5fs\apm_journal.txt" del "runtime\media\vf5fs\apm_journal.txt"
rem LE DOSSIER DE SAUVEGARDE. Le moteur construit le chemin "ram/BackupRam"
rem SANS CONDITION au demarrage, mais il n'importe que CreateFileW -- AUCUN
rem CreateDirectory. Il peut donc creer le FICHIER et pas le DOSSIER.
if not exist "runtime\media\vf5fs\ram" mkdir "runtime\media\vf5fs\ram"

rem --- LES 86 DECORS, ET CE QUE 86 VEUT DIRE (2026-10-13) ------------
rem Ce n est PAS 86 cases de grille : la grille garde ses vingt et une
rem cases. 86 est la taille de la TABLE DES DESCRIPTEURS du moteur, et
rem ce que le lot ajoute est UN ANNEAU PAR CASE -- la barre espace fait
rem tourner la meme case entre ses generations :
rem
rem     Final Showdown (0 a 28) -> VF5 R (42 a 60) -> VF5 ver.B (61 a 81)
rem
rem Dix-neuf cases ont leur double VF5 R, vingt et une leur version
rem ver.B, et la case de DURAL passe de cinq variantes a treize.
rem Sans ces options, le seul anneau pose est celui de Dural (du1..du5)
rem -- constat de Frederic le 2026-10-12 : "seuls quelques variants du
rem decor de dural sont selectionnables".
echo   Les decors de VF5 R et de VF5 ver.B...
set "POSES=1"
if not exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgso5.farc" set "POSES=0"
if not exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgd4b.farc" set "POSES=0"
if not exist "runtime\media\vf5fs\vf5fs_media\rom\objset\stgd45.farc" set "POSES=0"
if "%POSES%"=="1" (
  echo     deja poses ; on refait les deux bases.
  py -3 tools\decor_neuf.py --poser-lot 5r+vf5 --bases-seules >nul
) else (
  echo     pose ^(plusieurs centaines de Mo, plusieurs minutes^)...
  py -3 tools\decor_neuf.py --poser-lot 5r+vf5
)
if errorlevel 1 (
  echo.
  echo   La pose des decors a ECHOUE. Rien n a ete lance.
  pause
  exit /b 1
)
py -3 tools\shader_empreintes.py >nul

:relancer
rem --- la resolution a appliquer : celle que le jeu a retenue, sinon 1280x720
set "RL=1280"
set "RH=720"
if exist "%RESFIC%" for /f "usebackq tokens=1,2" %%a in ("%RESFIC%") do (
  set "RL=%%a"
  set "RH=%%b"
)
rem --- le MODE a appliquer : celui que le jeu a retenu, sinon console
set "MD=console"
if exist "%MODFIC%" for /f "usebackq tokens=1" %%a in ("%MODFIC%") do set "MD=%%a"
rem --- LE STYLE DES PASTILLES DE BOUTONS, retenu de la meme facon.
rem LA PLANCHE spr_n_fnt32 EST RESIDENTE -- mesure du 2026-10-11 : la
rem changer en cours de partie ne touche pas l ecran. Le choix fait en
rem jeu ne peut donc s appliquer qu ICI, avant le lancement.
rem boutons_style.py pose la planche ET la table de chaines, et ne
rem refait rien si le style est deja en place.
set "BT=ps3"
if exist "%BTNFIC%" for /f "usebackq tokens=1" %%a in ("%BTNFIC%") do set "BT=%%a"
echo.
echo   Style des boutons : !BT!
py -3 tools\boutons_style.py --poser !BT!
if errorlevel 1 echo   Style !BT! non pose ; on garde ce qui est la.
echo.
rem --- --terminal-ordre, QUATRIEME VERSION (2026-10-13) ------------
rem VF.TERMINAL suit enfin la sequence de la console, et elle a ete
rem LUE dans le code Xbox 360, pas deduite :
rem
rem   VF.TERMINAL  ->  le selecteur de carte, PAR-DESSUS le menu
rem                ->  le menu Customize items / Edit data name
rem                ->  le chargement, puis le decor du terminal
rem
rem LES TROIS VERSIONS PRECEDENTES ONT ECHOUE POUR LA MEME RAISON :
rem elles corrigeaient 0x1801DE38D, l entree 0 du validateur du
rem sous-menu TELLE QUE LE .origine LA PORTE. Mais --menu-v2 a deja
rem reecrit ce validateur : dans la DLL PATCHEE, 0x1801DE38D n est
rem plus qu un `nop` au milieu de trente-huit, jamais atteint. On
rem ecrivait donc un correctif juste dans du code mort.
rem
rem LE SEUL SITE QUI COMPTE est l entree du MENU PRINCIPAL
rem (0x1801DE056), que --menu-v2 faisait sauter sur une greffe
rem demandant le mode 5 tout de suite -- on quittait le mode MENU,
rem les trois taches du menu etaient demontees, et le Character
rem Select flottait sur du gris. Le relais y construit maintenant le
rem TaskMenuTerminal et lui pose AUSSITOT sa sous-page, le CARD
rem SELECTOR, exactement comme la ligne 3 du meme validateur sur
rem Xbox 360 (0x822B407C). Tout le reste etait deja ecrit dans la
rem DLL de la borne et n attendait que ce maillon.

rem --- LES VARIANTES DE DECOR Y SONT DEPUIS LE 2026-10-12 -----------
rem Constat de Frederic : " les variantes des decors ne sont plus
rem accessibles ". Elles n y avaient JAMAIS ete : la DLL de reference
rem du 12 porte encore son bouchon `ret 0` au creneau 4 de TaskSelStage,
rem donc ce lanceur n a jamais pose --variantes. Elles vivaient dans
rem variantes_texte.cmd et les lanceurs de decors, qui eux n ont PAS la
rem refonte du menu console. Les deux tiennent ensemble : la ligne
rem complete passe, et le creneau 4 porte desormais la greffe.
rem   ECRAN DE SELECTION DES DECORS : BARRE ESPACE sur une case a
rem   variantes fait defiler, et le nom s ecrit en blanc sous l apercu.
rem
rem --- LA LIGNE QUEST MODE EST OUVERTE ICI (2026-10-19) ---------
rem --menu-griser grise ONLINE VERSUS et QUEST MODE en UNE
rem instruction, un mov word dont l immediat porte les deux octets
rem d etat : [page+0x644] et [page+0x645]. --quest-degriser passe
rem cet immediat de 0x0101 a 0x0001 : ONLINE VERSUS reste grise,
rem QUEST MODE revient a 0. UN SEUL OCTET.
rem
rem Les deux gardes sont alors satisfaites, relues dans la DLL
rem PRODUITE : le validateur 0x1801DDF54 (cmp byte [..+0x642],0 / je)
rem prend la branche utile, et le creneau de curseur 0x1801E4CD8 ne
rem refuse plus que les etats non nuls.
rem
rem Et --quest-ecran a deja cable la ligne : il remplace la queue
rem d appel de la branche morte de la ligne 3 (0x1801DE0C0,
rem ex-ACHIEVEMENTS, un jmp vers ret 0) par un saut vers sa greffe.
rem
rem --- POURQUOI --boutons-xbox N EST PLUS DANS LA LIGNE (2026-10-12) --
rem Il changeait quatre octets de la TABLE D ECHAPPEMENTS du moteur
rem (ESC_BTN_*_PS3 -> les cases Xbox). Or `pictos_xbox.py` a mesure le
rem 2026-10-10 qu AUCUN LIBELLE ne cite un `ESC_BTN_*` : cette table
rem n est lue par personne. Le vrai levier est le TEXTE lui-meme, dans
rem string_array.farc, et c est `boutons_style.py` qui le pose selon le
rem style choisi -- un octet par occurrence. L option etait donc sans
rem effet, et la laisser dans la ligne laissait croire le contraire.
echo   Patch du moteur -- resolution !RL! x !RH!, mode !MD!...
if /i "!MD!"=="arcade" goto patch_arcade
py -3 tools\patch_si_besoin.py --resolution !RL! !RH! --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 ^
    --menu-fermer --options-raccourci --dojo-howto --dojo-cadre ^
    --options-v2 --menu-exit --legende-sousmenu ^
    --attract-retour-titre --sans-now-loading --options-tips ^
    --sans-ecran-epilepsie ^
    --decor-perso trm --terminal-boutons --customize-curseur ^
    --replays-sans-gel --vignettes-costume --selitem-grille ^
    --selitem-republier --selitem-ecreter --selpart-curseur ^
    --item-basculer --sans-warning --options-resolution --options-mode ^
    --menu-v2 --menu-griser --quest-degriser ^
    --bases-2d-libres --quest-ecran --textes-quest ^
    --versus-joueur2 --sans-legende --options-dural ^
    --versus-manette --terminal-ordre --film-cadres --nom-donnees --films-theatre ^
    --du2-collision --variantes --variantes-texte ^
    --variantes-5r --variantes-vf5 --decors-5r --decors-vf5 ^
    --decors-5r-dural --decors-table 86 --grille-table ^
    --decor-ecretage 86 --decor-repli 42 --obj-db-libre >nul
goto patch_fait

:patch_arcade
rem L ARCADE D ORIGINE, et rien de plus. Aucun correctif du menu console
rem n a de sens ici -- et ce n est pas qu une question de proprete :
rem --options-resolution posait les SIX relais de TaskOptionSetting, une
rem page qui n existe pas en arcade, et un appui les atteignait. Le jeu
rem se fermait alors tout seul (code de sortie 0, aucune exception : ce
rem n etait pas un plantage mais NOTRE ExitProcess, au bout de NOTRE
rem chaine -- ram\resolution.txt ressortait a 2560 1440). C est le
rem "F1 fait crasher le jeu en mode arcade" du 2026-10-07.
rem --options-mode se suffit a lui-meme : il pose la zone que apm.dll
rem surveille et LA PORTE DU RETOUR, la septieme ligne du menu TEST.
py -3 tools\patch_si_besoin.py --resolution !RL! !RH! --langue ^
    --mode 1 --options-mode >nul

:patch_fait
if errorlevel 1 (
  echo.
  echo   Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   -------------------------------------------------------------------
echo    A ESSAYER :
echo.
echo    1. OPTIONS a QUATRE sous-menus :
echo         Controls : Settings (remappage) . Buttons style
echo         Display  : Tips . Resolution
echo         Sound    : Volume BGM . Volume SE . BGM Type
echo         Game     : DURAL . Game Mode
echo       Resolution : GAUCHE/DROITE puis VALIDEZ -- le jeu se ferme
echo       et se rouvre tout seul dans la nouvelle resolution.
echo    2. TERMINAL ^> Customize : le personnage enregistre doit revenir.
echo    3. OPTIONS ^> Game ^> Game Mode : Console ou Arcade. VALIDEZ :
echo       le jeu se ferme et se rouvre dans le mode choisi.
echo       POUR REVENIR DE L ARCADE, l ecran Settings n existe plus.
echo       Le MENU TEST a une SEPTIEME ligne "CONSOLE MODE", et le
echo       curseur y est deja. Ce menu s ouvre par "test = 1" dans
echo       apm_entrees.txt -- tools\mode_console.cmd le fait pour vous.
echo.
echo    Le plantage du 2026-10-06 est corrige : 0x1801A6E0D citait bien
echo    0x180410D88, mais comme BORNE DE FIN d'un balayage, pas comme
echo    table. Son deplacement est rendu. Si ca replante :
echo    tools\settings_plantage.cmd donne l'adresse.
echo.
echo    Le jeu tourne a PLEINE VITESSE. Fermez-le quand vous avez vu.
echo   -------------------------------------------------------------------
echo.
pushd runtime\media\vf5fs
start /wait "" vfes.exe
popd
rem --- le jeu a-t-il demande une AUTRE resolution ? Alors on relance.
set "NL="
set "NH="
if exist "%RESFIC%" for /f "usebackq tokens=1,2" %%a in ("%RESFIC%") do (
  set "NL=%%a"
  set "NH=%%b"
)
if not "!NL!"=="" if not "!NL! !NH!"=="!RL! !RH!" (
  echo.
  echo   ===================================================================
  echo    NOUVELLE RESOLUTION DEMANDEE : !NL! x !NH! -- on relance
  echo   ===================================================================
  goto relancer
)
rem --- le jeu a-t-il demande un AUTRE style de boutons ?
set "NB="
if exist "%BTNFIC%" for /f "usebackq tokens=1" %%a in ("%BTNFIC%") do set "NB=%%a"
if not "!NB!"=="" if not "!NB!"=="!BT!" (
  echo.
  echo   ===================================================================
  echo    NOUVEAU STYLE DE BOUTONS : !NB! -- on relance
  echo   ===================================================================
  goto relancer
)
rem --- le jeu a-t-il demande un AUTRE mode ? Alors on relance aussi.
set "NM="
if exist "%MODFIC%" for /f "usebackq tokens=1" %%a in ("%MODFIC%") do set "NM=%%a"
if not "!NM!"=="" if not "!NM!"=="!MD!" (
  echo.
  echo   ===================================================================
  echo    NOUVEAU MODE DEMANDE : !NM! -- on relance
  echo   ===================================================================
  goto relancer
)
echo.
echo   ===================================================================
echo    LA SAUVEGARDE
echo   ===================================================================
dir /b "runtime\media\vf5fs\ram" 2>nul | findstr /r "." >nul
if errorlevel 1 (
  echo   Le dossier ram\ est VIDE. Si vous avez personnalise un
  echo   personnage, regardez les lignes SAUVE du journal ci-dessous.
) else (
  dir "runtime\media\vf5fs\ram"
  echo   customize.bin est la sauvegarde que LE STUB tient : le moteur,
  echo   lui, n'ecrit rien ^(sa tache TaskCsSystemSaveData existe mais tous
  echo   ses appels de service sont des bouchons replies^).
)
echo.
echo   ===================================================================
echo    JOURNAL DE LA MANETTE ET DE LA SAUVEGARDE
echo   ===================================================================
if exist "runtime\media\vf5fs\apm_journal.txt" (
  type "runtime\media\vf5fs\apm_journal.txt"
) else (
  echo   AUCUN JOURNAL. Le stub n'a rien ecrit : verifiez que
  echo   tools\apm_entrees.txt porte bien "journal_fichier = 1".
)
echo.
echo   Fichier : runtime\media\vf5fs\apm_journal.txt
echo.
pause
endlocal
