@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- ESSAI DU MODE TERMINAL. Double-cliquez, rien a taper.
rem
rem C est le build console habituel, plus deux choses :
rem   . --decor-perso trm : le decor de la borne pour l ecran TERMINAL ;
rem   . --terminal-boutons : les DEUX boutons de camera de cet ecran, qui
rem     lisaient des bits du masque arcade que RIEN ne remplit, passent sur
rem     les codes 16 et 17 du stub -- les touches B et N.
rem
rem CE QUE LA MESURE A ETABLI, ET QU IL FAUT SAVOIR AVANT DE JUGER :
rem   VALIDER et ANNULER de cet ecran ne passent PAS par le masque arcade.
rem   Ils passent par Input_isOnNow(7) = ENTREE et Input_isOnNow(8) = W, qui
rem   ont tous deux une source depuis toujours. Si rien ne repond, ce n est
rem   donc pas une touche qui manque : c est que l interface de l ecran ne se
rem   dessine pas. Cet essai est la pour trancher entre les deux.
rem
rem Cette version garde --wxga (comme console.cmd).
rem Pour l essai SANS --wxga -- le suspect numero un de menu_console.md
rem S15.3 -- lancez tools\terminal_sans_wxga.cmd.
rem
rem Touches : fleches, ENTREE = valider, W = annuler, X tenu + fleches =
rem           tourner le modele, Y / U = zoom, B = recentrer la camera,
rem           N = changer de vue, Echap = quitter le mode.
rem ---------------------------------------------------------------------------
call "%~dp0_terminal_commun.cmd" "--wxga" "-- avec --wxga"
