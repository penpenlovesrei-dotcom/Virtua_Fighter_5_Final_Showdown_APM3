@echo off
rem ---------------------------------------------------------------------------
rem Controle de conformite de mothead_<CHR>.bin sur tout le corpus :
rem les quatre jeux de donnees, 104 fichiers.
rem Doit afficher "104 fichier(s) : 104 conforme(s), 0 non conforme(s)",
rem puis "9140 identifiant(s) : 9140 dans le jeu du personnage, 0 hors du jeu".
rem
rem Le second controle apparie mothead_XXX.bin au jeu d'animations NOMME XXX.
rem Ne pas se servir du champ set_index de l en-tete : il ne designe pas ce jeu
rem (881 identifiants sur 9140 seulement).
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
py -3 tools\mothead.py check ^
  "C:\Users\frede\Desktop\VF5 FS DECOMP\APM3_FS\rom\rob" ^
  extracted\LIND_FS\tree\disk1\rom\rob ^
  extracted\PC_REVO_farc\rom\rob ^
  extracted\PC_REVO_farc\rom\resident ^
  extracted\PC_REVO_farc\rom_200\resident
echo.
echo --- les identifiants d'animation appartiennent-ils au bon personnage ? ---
py -3 tools\mothead.py ids extracted\APM3_FS_farc\rob\mot_db\mot_db.bin ^
  "C:\Users\frede\Desktop\VF5 FS DECOMP\APM3_FS\rom\rob"
echo.
pause
endlocal
