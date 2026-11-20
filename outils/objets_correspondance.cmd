@echo off
rem -----------------------------------------------------------------------
rem VF5 -- LA TABLE DE CORRESPONDANCE DES OBJETS : VF5 (2007) -> Final Showdown
rem
rem Double-cliquez. Rien n est modifie dans le jeu : cet outil LIT les deux
rem tables d objets et ecrit une table de traduction.
rem
rem POURQUOI. Chaque rival du mode Quest porte son costume dans npc_tbl :
rem deux listes de 24 identifiants d objets. Final Showdown a RENUMEROTE ses
rem objets (Akira : 401 en 2007, 1 004 dans FS). Poser le costume d un rival
rem sans traduire ses numeros l habillerait n importe comment.
rem
rem CE QUI SERT DE CLEF : le libelle interne du modele (ATAMA_01, OUTER_03),
rem qui n a pas bouge entre les deux jeux, controle par la categorie et la
rem variante de couleur.
rem
rem SORTIE : analysis\quest\objets_2007_vers_fs.json
rem
rem Pour regarder un personnage objet par objet :
rem   py -3 tools\objets_correspondance.py --detail aki
rem -----------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
set PYTHONIOENCODING=utf-8
echo.
echo   ===================================================================
echo    VF5 -- objets : la table 2007 -^> Final Showdown
echo   ===================================================================
echo.
py -3 tools\objets_correspondance.py
if errorlevel 1 (
  echo.
  echo La table n a pas ete construite.
)
echo.
pause
endlocal
