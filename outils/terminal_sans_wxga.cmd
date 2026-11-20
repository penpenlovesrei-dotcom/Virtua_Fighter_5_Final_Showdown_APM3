@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- ESSAI DU MODE TERMINAL, SANS --wxga. Double-cliquez.
rem
rem Meme chose que tools\terminal.cmd, mais SANS --wxga.
rem
rem POURQUOI : --wxga force l octet de variante d affichage [0x1806490D0+0x20],
rem qui est lu a 54 endroits de l interface et DECALE des identifiants de
rem scene. L ecran de personnalisation est l ecran le plus riche en interface
rem du build. menu_console.md S15.3 le designe comme le suspect numero un de
rem " l ecran s ouvre et n affiche que son decor ", et cet essai est le seul
rem moyen de le trancher.
rem
rem CE QUE L ON PERD SANS --wxga : Dural quitte la grille de selection. Ce
rem n est pas grave pour cet essai-la : on ne juge que le TERMINAL.
rem
rem Touches : fleches, ENTREE = valider, W = annuler, X tenu + fleches =
rem           tourner le modele, Y / U = zoom, B = recentrer la camera,
rem           N = changer de vue, Echap = quitter le mode.
rem ---------------------------------------------------------------------------
call "%~dp0_terminal_commun.cmd" "" "-- SANS --wxga"
