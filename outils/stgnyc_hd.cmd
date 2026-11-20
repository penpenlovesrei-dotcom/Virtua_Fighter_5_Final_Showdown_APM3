@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- VOIR LA TEXTURE HD DU DECOR CITY. Double-cliquez.
rem
rem La sonde force le decor 6 (nyc, le City de Jacky), mene le jeu SEUL
rem jusqu au combat et photographie. Environ deux minutes et demie, aucun
rem clavier a tenir. Les captures vont dans analysis\sonde\.
rem
rem CE QU IL FAUT REGARDER : le panneau SPORT CHANNEL et les facades. La
rem texture 315 du decor est passee de 2048x2048 a 4096x4096.
rem
rem ATTENTION, C EST UN AGRANDISSEMENT, PAS DE L ART HD : il n ajoute aucun
rem detail. Ce que cet essai prouve, c est que le jeu CHARGE et AFFICHE une
rem texture de 4096 -- pas qu elle soit plus belle. Si le decor se charge et
rem que rien n a bouge a l ecran, la chaine est bonne.
rem
rem SI LE DECOR NE CHARGE PLUS, c est la borne de taille du moteur :
rem    py -3 tools\textures_hd3d.py --retirer stgnyc
rem rend le fichier d origine ET le nom dans le .par.
rem ---------------------------------------------------------------------------
cd /d "%~dp0.."
py -3 tools\sonde_decor.py 6
echo.
pause
