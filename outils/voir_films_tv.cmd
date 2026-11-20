@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- REGARDER LES ONZE FILMS DE VF.TV, AVEC LE SON. Double-cliquez.
rem
rem Ils viennent du dossier /tv/movie de l image de VF5 R, et ils n ont pas
rem encore de titre : c est en les regardant qu on les nommera.
rem
rem CE QUE CE LANCEUR FAIT. Il ecrit dans MOVIES\A_REGARDER un vrai .mpg
rem par film : l image est RECOPIEE TELLE QUELLE (un .sfd Sofdec1 EST un
rem flux MPEG-1), et le son -- de l ADX, le format de CRI, que CRI range
rem dans le flux 0xC0 sous l etiquette « audio MPEG » -- est decode puis
rem reencode en MP2, le seul son qu un conteneur MPEG sache porter.
rem
rem LES ANCIENS .mpg ETAIENT DES LIENS DURS vers les .sfd : muets, et le
rem meme fichier sous deux noms. Ils sont remplaces, sans que les .sfd
rem soient touches.
rem
rem Double-cliquez un .mpg, ou glissez tout le dossier dans VLC.
rem ---------------------------------------------------------------------------
cd /d "%~dp0.."
py -3 tools\films_mpg.py %*
if errorlevel 2 (
  echo.
  echo   Rien n a ete produit. Lisez le message ci-dessus.
  pause
  exit /b 1
)
echo.
start "" "%CD%\MOVIES\A_REGARDER"
echo   Le dossier est ouvert. Double-cliquez un film.
echo.
pause
