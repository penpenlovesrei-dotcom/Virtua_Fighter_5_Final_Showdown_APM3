@echo off
rem ---------------------------------------------------------------------------
rem VITRINE APM3 -- un lanceur habille comme une borne ALL.Net P-ras Multi
rem
rem Double-cliquez. Le navigateur s'ouvre sur la vitrine ; cette fenetre reste
rem ouverte tant qu'elle tourne. Echap dans la vitrine, ou Ctrl+C ici, arrete.
rem
rem AJOUTER UN JEU -- un dossier par jeu dans vitrine\jeux\ :
rem
rem     vitrine\jeux\<le nom que vous voulez>\
rem         jaquette.png     votre jaquette   (ou .jpg)
rem         demo.mp4         votre video      (ou .webm)
rem         jeu.json         facultatif :
rem                          {"titre":"...", "exe":"C:\\...\\jeu.exe",
rem                           "args":[], "editeur":"...", "annee":1993}
rem
rem Sans jeu.json, le nom du dossier sert de titre et le premier .exe ou .cmd
rem trouve dedans est lance. N'importe quel executable convient.
rem Un dossier ajoute apparait tout seul : la vitrine relit toutes les 5 s.
rem
rem TOUCHES
rem     fleches / manette      naviguer
rem     Entree, Espace, bouton A   lancer
rem     Echap, bouton B        quitter
rem     F5                     relire le catalogue tout de suite
rem
rem IL N'Y A RIEN QUI SORTE, ET CE N'EST PAS DU RESEAU NEUTRALISE
rem
rem   . le serveur ecoute sur 127.0.0.1 UNIQUEMENT -- injoignable meme depuis
rem     le reseau local ;
rem   . la page ne charge aucune ressource distante : ni police, ni script, ni
rem     image. Tout est dans vitrine\media\ ;
rem   . le seul role du serveur est de lancer l'executable que la page lui
rem     demande -- un navigateur ne peut pas le faire lui-meme, et c'est tant
rem     mieux.
rem
rem L'HABILLAGE vient du systeme APM3 lui-meme : les badges de coin, les
rem fleches, le cercle barre, le logo ALL.Net P-ras MULTI et les jingles sont
rem ceux extraits par tools\apm_icones.py et tools\apm_sons.py.
rem Detail : analysis\interface_apm3.md.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
if not exist "vitrine\vitrine.py" (
  echo INTROUVABLE : vitrine\vitrine.py
  pause
  exit /b 1
)
py -3 vitrine\vitrine.py
echo.
pause
endlocal
