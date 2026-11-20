@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LES BOUTONS XBOX DANS OPTIONS ^> CONTROLS. Double-cliquez.
rem
rem L'ecran Controls montre un SCHEMA DE MANETTE -- rom/2d/spr_n_cmnps3, une
rem DualShock 3 en 512x512 RGBA8. C'est LUI qui portait les ronds et les croix,
rem pas le texte : les libelles citaient deja les glyphes Xbox (0x32F a 0x332 =
rem U+E002 Y, U+E000 B, U+E001 A, U+E003 X), dans les deux tables.
rem
rem Les quatre boutons sont DECOUPES dans la planche du jeu (spr_n_fnt32,
rem rangee 56, colonnes 50 a 53) : on ne dessine rien. La correspondance tombe
rem case pour case -- triangle=Y, carre=X, rond=B, croix=A -- donc les traits
rem de legende rouges designent toujours le bon bouton. Ils sont dans la
rem texture, et ils sont preserves pixel par pixel.
rem
rem   1  apercu (n'ecrit rien dans le jeu)  -^> analysis\schema_manette_xbox.png
rem   2  poser    (l'origine est gardee a cote, en .farc.origine)
rem   3  retirer  (remet l'origine)
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   1 = apercu     2 = poser     3 = retirer
echo.
set "C="
set /p "C=Votre choix (1, 2 ou 3) : "
if "%C%"=="2" goto poser
if "%C%"=="3" goto retirer
py -3 tools\schema_manette_xbox.py --apercu
goto fin
:poser
py -3 tools\schema_manette_xbox.py --poser
goto fin
:retirer
py -3 tools\schema_manette_xbox.py --retirer
:fin
echo.
pause
endlocal
