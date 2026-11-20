@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LES PICTOS DE OPTIONS ^> CONTROLS : LA SONDE. Double-cliquez.
rem
rem ELLE SE MESURE TOUTE SEULE : le jeu est lance, navigue jusqu a
rem OPTIONS ^> Controls et photographie l ecran. Aucun clavier a tenir.
rem Comptez environ soixante-dix secondes.
rem
rem CE QU ELLE DEMANDE AU JEU. Les quatre lignes de l ecran portent quatre
rem codepoints DIFFERENTS, et la capture dit ce que chacun dessine :
rem
rem    ligne 1   U+E000   SEGA l appelle CIRCLE -- la planche y met le B
rem    ligne 2   U+E003   SEGA l appelle SQUARE -- la planche y met le X
rem    ligne 3   U+E015   le rond PlayStation lui-meme
rem    ligne 4   U+E01A   le P rouge, TEMOIN hors de la plage des boutons
rem
rem Le temoin evite qu un releve vide passe pour une reponse.
rem
rem LA TABLE DES LIBELLES EST RENDUE A LA FIN, meme si l essai s interrompt.
rem
rem La capture : analysis\essai_controls_t58.png
rem ---------------------------------------------------------------------------
cd /d "%~dp0.."
py -3 tools\pictos_essai.py
echo.
pause
