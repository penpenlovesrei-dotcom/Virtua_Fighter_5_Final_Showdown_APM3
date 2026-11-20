@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LA CARTE DE L'IMAGE XBOX 360. Double-cliquez. Ne lance rien.
rem
rem Imprime, de l'image PowerPC ouverte par tools\x360_fs.cmd :
rem   . les neuf sections et l'adresse de base ;
rem   . LA TABLE DE CORRESPONDANCE des champs de curseur entre la borne APM3
rem     et la Xbox 360 -- la piece maitresse ;
rem   . le nombre de types RTTI et de vtables retrouvees.
rem
rem D'OU VIENT LA TABLE, et pourquoi elle ne suppose rien. La fonction
rem TaskCsMenu::update existe dans les DEUX builds et fait la meme chose dans
rem le meme ordre : 0x1801BBBE0 cote borne, 0x82217B30 cote Xbox 360. Lues
rem cote a cote, instruction par instruction, les champs se nomment d'eux
rem memes. L'ecart d'offsets vient de la taille des pointeurs -- 64 bits
rem contre 32 -- mais l'ORDRE et le ROLE sont identiques.
rem
rem CE QUE LA CARTE SERT A FAIRE. Les ecrans "select part" et "select item"
rem de la borne sont desarmes : leur curseur de grille n'a plus de code pour
rem bouger. Cote console la meme interface marche. Avec la table, une
rem fonction console se relit directement dans le vocabulaire de la borne.
rem
rem Les autres commandes de l'outil, en ligne :
rem   py -3 tools\x360_ppc.py sections
rem   py -3 tools\x360_ppc.py chaines part_win
rem   py -3 tools\x360_ppc.py xref 0x82010CAC      qui construit cette adresse
rem   py -3 tools\x360_ppc.py rtti Cs              classes et vtables
rem   py -3 tools\x360_ppc.py vtable 0x82011628
rem   py -3 tools\x360_ppc.py func 0x82217B30 --max 70
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 FS -- la carte de l image Xbox 360
echo   ===================================================================
echo.
if not exist extracted\X360_FS\sel\default.img (
  echo   L image est absente. Lancez d abord tools\x360_fs.cmd.
  pause
  exit /b 1
)
py -3 tools\x360_ppc.py carte
echo.
pause
endlocal
