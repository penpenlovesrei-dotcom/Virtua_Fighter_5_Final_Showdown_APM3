@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LE BUILD CONSOLE COMPLET. Double-cliquez, rien a taper.
rem
rem Ce qu'il contient, tout valide a l'ecran sauf la derniere ligne :
rem   . Dural jouable dans la grille
rem   . SINGLE PLAYER  : les QUATRE lignes lancent le combat -- Arcade, Score
rem                      Attack, License Challenge et Special Sparring
rem   . OFFLINE VERSUS : a deux -- clavier = joueur 1, manette = joueur 2
rem   . DOJO           : entrainement
rem   . TERMINAL       : avec son vrai decor (trm)
rem   . Echap          : sortir d'un mode et revenir au menu
rem   . EXIT GAME      : dixieme ligne du menu, ferme le jeu (sans confirmation)
rem   . DOJO           : une 4e ligne, How to Play  <- A ESSAYER
rem   . la legende du bas ne se superpose plus quand un sous-menu est ouvert
rem   . l'attract joue LA VIDEO de la borne, remise au format USM
rem     (rom/movie/vf5adv.usm ; l'original codec 5, illisible ici, est
rem      sauvegarde a cote sous vf5adv.usm.ecarte)
rem     Pour revenir a l'animation d'Akira : ajouter --attract-long a la
rem     ligne de patch, et remettre le vf5adv.usm d'origine.
rem   . le texte "NOW LOADING" est retire des ecrans de chargement
rem   . OPTIONS > Settings : la quatrieme ligne est "Tips" Off/On, et elle
rem     commande le conseil affiche pendant les chargements. Elle remplace
rem     "Autosave", qui n'a aucun lecteur sur borne. Defaut : On.
rem   . CORRIGE le 2026-09-06 : la legende du bas et License Challenge
rem     logeaient leur caverne a la MEME adresse (0x1801A71D8) ; la legende
rem     ecrasait le lancement. License Challenge etait casse. La legende a sa
rem     caverne a part, et patch_moteur.py refuse desormais toute collision.
rem   . couper l'attract par START ramene au TITRE. Sans le correctif, la
rem     coupure basculait en mode BORNE (APM3_ENTRY, ecran noir, quatre
rem     appuis de plus, puis la selection de personnages arcade).
rem
rem   Le TITRE, lui, transparait toujours sous celui du sous-menu (� MAIN MENU �
rem   sous � SINGLE PLAYER �) : c'est l'AFFICHAGE NORMAL, tranche par Frederic
rem   le 2026-09-06. Ne pas le � corriger �.
rem
rem   Touches : fleches, Entree = VALIDER, W = ANNULER, X C V = croix rond triangle,
rem             Espace = SELECT, Echap = quitter le mode, F1/F2 = TEST/SERVICE.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
rem Le apm.dll est remis en ASCII : les mesures reseau (pister_link.cmd) le
rem construisent en UTF-16, et le jeu plante alors au demarrage. Ce lanceur doit
rem rendre un build jouable, quoi qu'ait laisse la mesure precedente.
py -3 tools\gen_apm_stub.py >nul
if errorlevel 1 (
  echo.
  echo La compilation du apm.dll a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso trm
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   Deux fois Entree  -^> menu console
echo   EXIT GAME est la DIXIEME ligne, tout en bas de la liste.
echo   Elle ferme le jeu tout de suite, sans confirmation.
echo.
cd /d "%~dp0..\runtime\media\vf5fs"
start "" vfes.exe
endlocal
