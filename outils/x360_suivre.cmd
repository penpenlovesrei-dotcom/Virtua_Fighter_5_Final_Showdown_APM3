@echo off
rem ---------------------------------------------------------------------------
rem VF5 -- LES CHAMPS D'UNE STRUCTURE RENDUE PAR UN ACCESSEUR, cote Xbox 360.
rem Double-cliquez. Le releve par defaut est LE PROFIL DU QUEST DE 2007,
rem c'est-a-dire la valeur rendue par FUN_8230B5B8.
rem
rem L'IMAGE LUE EST CELLE DE VF5 2007 (extracted\X360_VF5\vf5_x360.img) et
rem PAS celle de Final Showdown : les deux ont la meme base 0x82000000, et
rem une adresse de 2007 repond autre chose dans l'autre SANS erreur.
rem
rem DEUX PARCOURS, et les deux sont montres :
rem   . en LIGNE DROITE  un seul chemin, celui qui ne prend aucun branchement
rem   . sur GRAPHE       les deux cotes de chaque conditionnel, borne a la
rem                      fonction appelante par .pdata
rem Le second rend cinq champs de plus, dont les quatre u32 du bas de l'ecran
rem de statut. Les deux restent des MINORANTS : ce qu'ils montrent est vrai,
rem ce qu'ils ne montrent pas n'est pas prouve absent.
rem
rem Lecture seule. Rien n'est patche, le jeu n'est pas lance.
rem ---------------------------------------------------------------------------
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    LE PROFIL DU QUEST DE 2007 -- en ligne droite
echo   ===================================================================
echo.
py -3 tools\x360_suivre.py 0x8230B5B8
if errorlevel 1 (
  echo.
  echo   Le releve a ECHOUE. Verifiez que extracted\X360_VF5\vf5_x360.img
  echo   existe -- il sort de tools\xex.py.
  pause
  exit /b 1
)
echo.
echo   ===================================================================
echo    LE MEME, sur le GRAPHE DE FLOT -- cinq champs de plus
echo   ===================================================================
echo.
py -3 tools\x360_suivre.py 0x8230B5B8 --graphe
echo.
echo   ===================================================================
echo    LE SOCLE -- FUN_822DAC40, dont le profil est +0xC0
echo   ===================================================================
echo.
py -3 tools\x360_suivre.py 0x822DAC40 --graphe
echo.
echo   Les quatre u32 du statut (profil +0x17C a +0x188) sont LUS par
echo   l'ecran de statut et ECRITS par personne qui passe par l'un ou
echo   l'autre accesseur. Detail au paragraphe 14.9 de
echo   analysis\mode_quest.md.
echo.
pause
