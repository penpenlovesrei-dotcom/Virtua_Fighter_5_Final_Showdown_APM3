@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- OU EXACTEMENT "select part" PLANTE. Double-cliquez.
rem
rem POURQUOI CE LANCEUR EXISTE, et c'est dit franchement : j'ai propose DEUX
rem fois un correctif pour cet ecran en raisonnant sur le desassemblage, et
rem deux fois il a plante. Le desassemblage ne dit pas quelle instruction
rem faute : `+0x58` sert a une dizaine de structures differentes dans cette
rem zone -- 179 acces releves entre 0x1801C0000 et 0x1801D1000 -- et aucun
rem releve statique ne tranche. Il faut l'adresse de la faute.
rem
rem CE LANCEUR NE SERT QU'A CA. Il porte --selpart-curseur (l'option qui
rem plante) et la sonde de plantage, SANS aucun point d'arret : le jeu tourne
rem a sa vitesse normale, parce que les 25 images par seconde des autres
rem sondes viennent des `0xCC`, pas du debogueur. Seules les exceptions sont
rem regardees, et Windows les envoie de lui-meme.
rem
rem CE QU'IL FAUT FAIRE :
rem   TERMINAL -^> Customize -^> un personnage -^> "select part", HAUT/BAS
rem   pour descendre dans un bloc, puis VALIDEZ -- c'est la que ca plante.
rem
rem PASSE 3 : LE FILET. La cause est trouvee et corrigee (--selitem-ecreter) ;
rem ce lanceur ne sert plus qu'a reprendre la mesure si quelque chose plante
rem ENCORE. Il porte donc le correctif, lui aussi.
rem
rem CE QUE LES DEUX PREMIERES PASSES ONT DONNE.
rem   La premiere passe a donne la faute : 0x1801C7589,
rem     cmp byte ptr [rcx + 0x240], 0     avec rcx = 0x0000F00DD458BAAD
rem   c'est-a-dire `TaskSelItemMenu::update` qui dereference la globale
rem   [0x180752610] -- SANS test -- alors qu'elle porte du remplissage de
rem   tas ^(la famille BAADF00D^). Cette globale est en BSS, donc nulle au
rem   chargement, et ses seuls ecrivains y mettent soit une allocation
rem   valide ^(0x1801C6AD0^) soit zero ^(0x1801C6BE0^). Elle a donc ete
rem   ecrite PAR AILLEURS.
rem
rem   Cette passe arme donc DEUX choses de plus :
rem     . un point d'arret MATERIEL en ecriture sur 0x180752610, qui NOMME
rem       l'instruction qui y ecrit ^(et ne coute rien : pas de 0xCC, aucune
rem       exception tant que personne n'ecrit^) ;
rem     . quatre espions sur le valideur 0x1801C8280, qui relevent la
rem       categorie, l'index de sous-partie, le compte du bloc, les ids des
rem       entrees et l'ID qui devient une adresse en 0x1801C834B. Ils ne
rem       frappent que sur une VALIDATION.
rem
rem   Si l'index sort du compte, ou si l'ID depasse 24, c'est MON relais qui
rem   donne au jeu une sous-partie dont l'entree n'a jamais ete remplie --
rem   et la sonde l'ecrira en clair, avec des asterisques.
rem
rem CE QU'ON OBTIENT, et c'est tout ce qui me manque :
rem
rem   EXCEPTION ACCESS_VIOLATION (2e chance)  a 0x...
rem     ou      : ...dll!.greffe+0x3380 (VA preferee 0x180EA3380)
rem               ^^^^^^^ LA SECTION : .greffe = NOTRE relais
rem                                    .text   = le code du jeu
rem     acces   : ECRITURE de 0x0000000000000000
rem     --- code autour de RIP ---
rem     ^>^>^> 0x...  mov dword ptr [rdi + 0x58], r11d
rem     retour  -^> 0x1801C7D6A
rem
rem La section suffit a repartir la faute entre mon code et le sien, et le
rem desassemblage autour de RIP donne l'instruction exacte. Une passe, et on
rem sait -- au lieu d'une troisieme hypothese.
rem
rem UNE EXCEPTION DE "2e chance" EST CELLE QUI TUE LE PROCESSUS : c'est
rem celle-la qu'il faut lire. Les "1re chance" sont souvent normales ^(le
rem moteur en rattrape^).
rem
rem Le journal s'ecrit AU FIL DE L'EAU dans analysis\pister_plantage.txt :
rem meme si le jeu meurt, ce qui a ete vu est sur le disque.
rem
rem Vos reglages de manette sont CONSERVES ^(--garder-scenario^) : le plantage
rem se provoque a la manette, et les perdre changerait ce qu'on mesure.
rem
rem Clavier : fleches, Entree = valider, W = annuler, Echap = sortir du mode.
rem LE DEMARRAGE EST LENT. Laissez-lui le temps.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- OU "select part" PLANTE, exactement
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
echo   Patch du moteur, AVEC --selpart-curseur ^(l'option qui plante^)...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 ^
    --menu-fermer --options-raccourci --dojo-howto --dojo-cadre ^
    --options-sans-howto --menu-exit --legende-sousmenu ^
    --attract-retour-titre --sans-now-loading --options-tips ^
    --decor-perso trm --terminal-boutons --customize-curseur ^
    --replays-sans-gel --vignettes-costume --selitem-grille ^
    --selitem-republier --selitem-ecreter --selpart-curseur --item-basculer --sans-warning >nul
if errorlevel 1 (
  echo.
  echo   Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   -------------------------------------------------------------------
echo    ALLEZ FAIRE PLANTER LE JEU.
echo    TERMINAL ^> Customize ^> un personnage ^> "select part".
echo    GAUCHE/DROITE change de bloc, HAUT/BAS parcourt le bloc.
echo.
echo    HAUT/BAS pour descendre dans un bloc, puis VALIDEZ.
echo.
echo    La sonde ne pose AUCUN point d'arret : pleine vitesse.
echo    Journal : analysis\pister_plantage.txt
echo   -------------------------------------------------------------------
echo.
py -3 tools\pister_plantage.py --sans-jalons --garder-scenario ^
    --selpart --surveiller 0x180752610:8 --secondes 600
echo.
echo   ===================================================================
echo    CE QUI A FAUTE
echo   ===================================================================
if exist "analysis\pister_plantage.txt" (
  findstr /n /c:"EXCEPTION" /c:"ou      :" /c:"acces   :" /c:"cible   :" ^
      /c:"retour" /c:">>>" /c:"qui ecrit" /c:"DR0" /c:"DR1" /c:"***" ^
      /c:"VALIDATION" /c:"l ID" /c:"ids des" /c:"curseurs" ^
      "analysis\pister_plantage.txt"
) else (
  echo   AUCUN JOURNAL. La sonde n'a rien ecrit.
)
echo.
echo   Journal complet : analysis\pister_plantage.txt
echo.
pause
endlocal
