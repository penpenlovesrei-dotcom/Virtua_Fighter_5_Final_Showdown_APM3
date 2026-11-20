@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- QUI ECRIT LA SAUVEGARDE, ET QUI L'EFFACE. Double-cliquez.
rem
rem POURQUOI CE LANCEUR. J'ai propose trois correctifs de suite sur la
rem sauvegarde du personnage, en lisant du desassemblage par fragments, et les
rem trois ont rate. Frederic a demande une sonde qui regarde le jeu FAIRE.
rem La voici, et elle ne devine rien.
rem
rem CE QU'ELLE SURVEILLE. Des points d'arret MATERIELS en ecriture :
rem   . l'EMPLACEMENT du pointeur de la table des personnages ^(0x180752148^)
rem   . l'EMPLACEMENT du pointeur de l'enregistrement ^(0x18070FB10^)
rem puis, des que le moteur y range son objet et a l'instruction qui SUIT :
rem   . la TETE DE LA TABLE DES PERSONNAGES  ^(pointeur + 0x28^)
rem   . la PREMIERE PARTIE EQUIPEE           ^(pointeur + 0x18 + 0x262^)
rem
rem POURQUOI EN DEUX TEMPS. La premiere redaction attendait que les pointeurs
rem soient non nuls en sondant toutes les 100 ms. Un effacement qui suit
rem l'allocation de quelques microsecondes -- exactement ce qu'on soupconne --
rem passait entre deux sondages. En surveillant d'abord l'emplacement du
rem pointeur, la couverture est complete et sans trou ; le registre du
rem pointeur est rendu aussitot apres.
rem
rem NOTRE PROPRE SAUVEGARDE EST COUPEE pour cette passe. Le apm.dll de
rem substitution restaure la table au demarrage : ses ecritures tombent aux
rem memes adresses que celles du moteur, et les deux releves se melangeaient.
rem On ne mesure pas un moteur en gardant la main dessus. La sonde remet le
rem reglage comme elle l'a trouve en sortant.
rem   --avec-notre-sauvegarde  garde notre bloc actif ^(passe SUIVANTE : celle
rem                            qui dira si notre restauration est defaite^)
rem
rem UN POINT D'ARRET MATERIEL NE COUTE RIEN : aucun 0xCC, aucune exception
rem tant que personne n'ecrit a l'adresse. Le jeu tourne a PLEINE VITESSE --
rem ce qui compte, puisqu'il faut naviguer jusqu'a Customize a la main.
rem
rem CE QU'IL FAUT FAIRE, et c'est tout :
rem   1. TERMINAL -^> Customize
rem   2. habillez un personnage
rem   3. ENREGISTREZ-LE ^(c'est le geste qu'on veut voir^)
rem   4. fermez le jeu
rem
rem CE QUE LA SONDE ECRIRA, pour chaque ecriture :
rem   ECRITURE sur la TABLE DES PERSONNAGES ^(acces 3^)
rem     qui ecrit : ...dll!.text+0x1D0B21 ^(VA preferee 0x1801D0B21^)
rem     entrees occupees : 0 -^> 1
rem     --- code a partir de RIP ---
rem
rem Le compte d'entrees occupees dit si l'ecriture GARNIT ou EFFACE, et
rem l'adresse a la base preferee est la seule qui se retrouve dans un
rem desassemblage. C'est tout ce qui manquait pour arreter de parier.
rem
rem Journal au fil de l'eau : analysis\pister_sauvegarde.txt -- meme si le jeu
rem meurt, ce qui a ete vu est sur le disque. La passe precedente est archivee.
rem
rem LE DEMARRAGE EST LENT. Laissez-lui le temps.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- QUI ECRIT LA SAUVEGARDE, ET QUI L'EFFACE
echo   ===================================================================
echo.
tasklist /fi "IMAGENAME eq vfes.exe" 2>nul | findstr /i "vfes.exe" >nul
if not errorlevel 1 (
  echo   vfes.exe TOURNE DEJA -- apm.dll est verrouillee et le patch
  echo   echouerait en silence cote copie. Fermez le jeu d'abord.
  pause
  exit /b 1
)
echo   Compilation de apm.dll...
py -3 tools\gen_apm_stub.py >nul
if errorlevel 1 (
  echo.
  echo   La compilation du apm.dll a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo   Patch du moteur...
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 ^
    --menu-fermer --options-raccourci --dojo-howto --dojo-cadre ^
    --options-sans-howto --menu-exit --legende-sousmenu ^
    --attract-retour-titre --sans-now-loading --options-tips ^
    --decor-perso trm --terminal-boutons --customize-curseur ^
    --replays-sans-gel --vignettes-costume --selitem-grille ^
    --selitem-republier --selitem-ecreter --selpart-curseur ^
    --item-basculer --sans-warning >nul
if errorlevel 1 (
  echo.
  echo   Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
if not exist "runtime\media\vf5fs\ram" mkdir "runtime\media\vf5fs\ram"
echo.
echo   -------------------------------------------------------------------
echo    CE QU'IL FAUT FAIRE :
echo      1. TERMINAL ^> Customize
echo      2. habillez un personnage
echo      3. ENREGISTREZ-LE
echo      4. fermez le jeu
echo.
echo    NOTRE sauvegarde est COUPEE : on regarde le moteur SEUL.
echo    La sonde ne conduit rien, elle regarde. Pleine vitesse.
echo    Journal : analysis\pister_sauvegarde.txt
echo   -------------------------------------------------------------------
echo.
py -3 tools\pister_sauvegarde.py --secondes 900 %*
echo.
echo   ===================================================================
echo    CE QUI A ECRIT
echo   ===================================================================
if exist "analysis\pister_sauvegarde.txt" (
  findstr /n /c:"ECRITURE" /c:"qui ecrit" /c:"entrees occupees" /c:">>>" ^
      /c:"LE POINTEUR" /c:"par :" /c:"notre bloc" /c:"DR" ^
      "analysis\pister_sauvegarde.txt"
) else (
  echo   AUCUN JOURNAL. La sonde n'a rien ecrit.
)
echo.
echo   Journal complet : analysis\pister_sauvegarde.txt
echo.
pause
endlocal
