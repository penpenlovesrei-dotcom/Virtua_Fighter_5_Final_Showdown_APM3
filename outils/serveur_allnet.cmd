@echo off
rem ---------------------------------------------------------------------------
rem LE SERVEUR ALL.Net, et le jeu avec.
rem
rem Double-cliquez. Deux fenetres s'ouvrent :
rem   . celle-ci  : le serveur. Il journalise CHAQUE requete du jeu -- le
rem                 chemin, l'en-tete, le JSON dechiffre, et ce qu'il repond.
rem   . le jeu    : le build de console.cmd, inchange.
rem
rem Il n'y a RIEN a faire dans le jeu : le reseau part tout seul au demarrage,
rem des l'ecran d'attract. Laissez tourner une minute et regardez cette
rem fenetre-ci.
rem
rem Le serveur ne devine pas : il repond au minimum et note tout. Chaque refus
rem du jeu nommera le champ suivant a fournir.
rem
rem Pour arreter : fermez cette fenetre (le jeu se ferme avec Echap).
rem
rem Journal : analysis\serveur_allnet.txt
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
rem Le apm.dll est construit en UTF-16 : les six chaines du chemin `setupLink`
rem doivent etre larges, sinon `ImplLink::setup` refuse le `gameId` (taille 0)
rem et le reseau ne demarre pas du tout. C'est ce build-la qui plantait avant la
rem correction de `System_getGameVersion` ; il ne plante plus.
py -3 tools\gen_apm_stub.py --utf16 >nul
if errorlevel 1 (
  echo.
  echo La compilation du apm.dll a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring ^
    --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre ^
    --options-sans-howto --menu-exit --legende-sousmenu --decor-perso trm >nul
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
start "" /d "%~dp0..\runtime\media\vf5fs" vfes.exe
echo.
py -3 tools\serveur_allnet.py
pause
endlocal
