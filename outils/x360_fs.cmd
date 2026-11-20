@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- OUVRIR L'EXECUTABLE XBOX 360. Double-cliquez.
rem
rem POURQUOI. La borne APM3 a des ECRANS DESARMES qu'aucune mesure interne ne
rem peut reparer sans inventer : le curseur de "select part" et de "select
rem item" tient sa position dans sa propre grille, et le seul code qui la
rem deplacait -- un consommateur de messages -- n'a plus de producteur. La
rem version Xbox 360 de Final Showdown porte la MEME interface : les noms de
rem planches "part_win", "p_part_plt_lt" et "p_yaji_left_c" y sont, et la
rem classe "TaskCsMenu" -- le repartiteur de curseur de la borne -- aussi.
rem Transposer une implementation qui marche n'est pas inventer.
rem
rem CE QUE CE LANCEUR FAIT, en deux temps :
rem   1. tools\stfs.py   sort default.xex du conteneur LIVE (2 Go) ;
rem   2. tools\xex.py    le dechiffre (AES, cle de detail) et le DECOMPRESSE,
rem                      puis imprime les sections de l'image PowerPC.
rem
rem LE VERROU QUI A SAUTE LE 2026-10-01. Ce XEX est en compression 2, dite
rem "normale", c'est-a-dire LZX -- et le depot n'avait pas de decodeur ; le
rem dossier docs\formats\xbox360_outils.md disait que c'etait "le morceau
rem cher" et que la piste console etait "un chantier a part entiere".
rem tools\lzx.py est ce decodeur, ecrit depuis la specification.
rem
rem CE QUI SE VERIFIE TOUT SEUL, et qui prouve que la sortie est juste :
rem   . l'empreinte SHA-1 du premier bloc, donnee par l'en-tete du XEX ;
rem   . l'image commence par "MZ" et porte un PE PowerPC gros-boutiste ;
rem   . les chaines UNLOCK_DURAL et ARCADE MENU, que le dossier signalait
rem     ABSENTES du paquet brut, apparaissent -- elles etaient compressees.
rem
rem Sortie : extracted\X360_FS\sel\default.xex et default.img (17,6 Mo).
rem Comptez deux a trois minutes : le decodeur LZX est en Python pur.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 FS -- ouvrir l executable Xbox 360
echo   ===================================================================
echo.
py -3 tools\lzx.py --essai
if errorlevel 1 ( echo   Le decodeur LZX echoue a son propre essai. & pause & exit /b 1 )
set PAQUET=extracted\X360_FS\Virtua Fighter 5 Final Showdown + TU1\584111FE\000D0000\7D2DF36BD11FB8394C3D652339E6FE1DA1337B1058
if not exist "%PAQUET%" (
  echo   Le conteneur LIVE est introuvable :
  echo     %PAQUET%
  echo   Il sort de l archive RAR de "VF5 FS DECOMP\X360_FS".
  pause
  exit /b 1
)
if not exist extracted\X360_FS\sel mkdir extracted\X360_FS\sel
echo   1/2  extraction de default.xex du conteneur...
py -3 tools\stfs.py extraire "%PAQUET%" extracted\X360_FS\sel --motif default.xex
if errorlevel 1 ( echo   L extraction a ECHOUE. & pause & exit /b 1 )
echo.
echo   2/2  dechiffrement et decompression LZX ^(deux a trois minutes^)...
py -3 tools\xex.py extracted\X360_FS\sel\default.xex extracted\X360_FS\sel\default.img
if errorlevel 1 ( echo   L ouverture a ECHOUE. & pause & exit /b 1 )
echo.
pause
endlocal
