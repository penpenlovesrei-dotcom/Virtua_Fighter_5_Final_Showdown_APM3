@echo off
rem ---------------------------------------------------------------------------
rem LES DEUX APPLICATIONS UNITY DU SYSTEME APM, HORS LIGNE
rem
rem Double-cliquez. Le lanceur prepare un BAC A SABLE (une copie de
rem APM_V1.04_internal_0 dans runtime\apm_bac, 241 Mo, une seule fois), puis
rem lance emoneyUI.exe et Apmv3System.exe SANS le daemon, en relevant leurs
rem connexions TCP a chaque seconde.
rem
rem POURQUOI C'EST HORS LIGNE PAR CONSTRUCTION
rem
rem   amdaemon.exe est le SEUL binaire du systeme qui parle a ALL.Net : sept
rem   noms de domaine (aime.naominet.jp, naominet.jp, at.sys-all.net,
rem   amlog.sys-all.net, d-amlog.sys-all.net...) et les API connect,
rem   WinHttpOpen, getaddrinfo, send.
rem
rem   Apmv3System.exe et emoneyUI.exe n'ont AUCUNE API reseau. Leurs seuls
rem   noms de domaine sont les schemas XML de leur manifeste Windows. Ils
rem   parlent au daemon par AMDaemon.NET.dll, en local.
rem
rem   On ne lance pas le daemon. Les deux applications n'ont alors aucun
rem   chemin vers l'exterieur. Et la configuration du BAC est desamorcee par
rem   surcroit : allnet_auth, allnet_accounting, network, aime, usb_io, apm
rem   passent tous a false -- dans la COPIE, jamais dans l'original.
rem
rem LE RISQUE QUI RESTE, ET IL EST DIT
rem
rem   UnityPlayer.dll embarque le rapport de plantage Unity
rem   (perf-events.cloud.unity3d.com) et WSAStartup / getaddrinfo. Il ne se
rem   declenche qu'en cas de plantage, mais je ne peux pas le prouver inerte.
rem   D'ou la mesure : chaque connexion TCP est relevee et ecrite dans
rem   analysis\apm_lancement.log. Si vous voulez une garantie dure, coupez le
rem   Wi-Fi ou debranchez le cable avant de cliquer -- c'est votre geste, pas
rem   le mien.
rem
rem CE QUE CE LANCEUR NE FAIT JAMAIS
rem
rem   . il ne lance PAS game.bat. Ce script d'arcade efface Y:\, ecrit dans
rem     HKLM\System\SEGA\... et FLASHE les micrologiciels de la carte USB IO,
rem     de la carte LED (COM2, 115200) et de la dalle tactile. Sur un PC
rem     ordinaire, c'est destructeur ;
rem   . il ne touche ni au pare-feu, ni au fichier hosts, ni a la base de
rem     registre ;
rem   . il ne travaille jamais sur le dossier d'origine.
rem
rem CE QU'IL FAUT EN ATTENDRE
rem
rem   Les deux applications sont ecrites pour une borne : lecteur Aime sur le
rem   port 3, carte USB IO, carte LED, dalle tactile, et les lecteurs X: Y: W:.
rem   Sans daemon elles afficheront au mieux leur ecran d'erreur. Le but n'est
rem   pas de les faire fonctionner, c'est de VOIR leurs badges de coin --
rem   ceux de la capture. Le journal Unity dira ou elles se sont arretees.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   Preparation du bac a sable (copie, une seule fois)...
py -3 tools\apm_lancer.py --preparer
if errorlevel 1 (
  echo.
  echo La preparation a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   Lancement HORS LIGNE, 20 s chacune, connexions relevees...
echo.
py -3 tools\apm_lancer.py emoneyUI Apmv3System --secondes 20
echo.
echo   Journal : analysis\apm_lancement.log
echo   Journaux Unity : analysis\unity_emoneyUI.log, analysis\unity_Apmv3System.log
echo.
pause
endlocal
