@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LA BARRE ESPACE FAIT DEFILER LES VARIANTES DU DECOR
rem
rem Double-cliquez, et PATIENTEZ : le demarrage est long. Le script dit
rem "Le jeu tourne" quand c'est parti.
rem
rem CE QU'IL FAUT ESSAYER
rem
rem   STAGE SELECT, curseur sur la case de DURAL (ligne du bas, 7e colonne).
rem   Pressez la BARRE ESPACE : le decor charge passe a la variante suivante,
rem   sans quitter l'ecran et sans bouger le curseur.
rem
rem     du1 SNOW  ->  du2 ECLIPSE/METEOR  ->  du3 SUBMERSION
rem           ->  du4 STORM  ->  du5 SPACE  ->  du1 ...
rem
rem   Validez pour lancer le combat sur la variante affichee.
rem   Sur toute autre case, la barre espace ne fait rien : c'est voulu, seul
rem   l'anneau de Dural est defini pour l'instant.
rem
rem LE NOM DE LA VARIANTE EST MAINTENANT ECRIT A L'ECRAN
rem
rem   SNOW, ECLIPSE, SUBMERSION, STORM ou SPACE s'affiche en blanc, centre,
rem   a x=640 y=460. L'apercu, lui, ne change pas : les cinq decors de Dural
rem   partagent la meme planche AET (dur / dur_stay), et c'est de l'art peint.
rem
rem   DEUX CHOSES A REGARDER, que je ne peux pas verifier d'ici :
rem     . le texte apparait-il ? Ce dessin n'a JAMAIS tourne. S'il fait
rem       planter, c'est la premiere piste ;
rem     . est-il AU BON ENDROIT ? y=460 est une supposition -- je ne sais pas
rem       ou tombe exactement la mention de la taille du decor. La position
rem       est deux flottants dans la greffe (0x180EA1810 et 0x180EA1814) :
rem       dites-moi le decalage et je la corrige.
rem
rem   Le texte se dessine par 0x18019B2E0(descripteur, 0x28, chaine) -- la
rem   MEME fonction que le NOW LOADING que --sans-now-loading neutralise.
rem   Elle n'a rien a voir avec string_array : c'est un pointeur direct, donc
rem   les trois noms de generation tiendront dans la greffe sans probleme.
rem
rem COMMENT C'EST FAIT
rem
rem   . la barre espace est le code brut 6, un canal LIBRE : la vraie apm.dll
rem     ne l'affirme jamais. Deux sites du moteur l'interrogent deja
rem     (0x18023B269, 0x18023BA48) ;
rem   . DEUX accroches, et c'est la seconde qui compte. La premiere version
rem     ecrivait [rbx+0x5C] en 0x180174710 : elle marchait -- 300 passages,
rem     al = 1 a chaque appui, index ecrit a 22 -- et pourtant seul du1 se
rem     chargeait. Un point d'arret MATERIEL en ecriture sur le champ a nomme
rem     le coupable : 0x180174781, la recomputation depuis la case du curseur,
rem     qui defaisait notre ecriture dans la meme trame.
rem     Donc maintenant : 0x180174710 lit le bouton et fait tourner un NUMERO
rem     DE VARIANTE garde dans la greffe -- plus dans [rbx+0x5C], qui ne nous
rem     appartient pas -- et 0x1801747C0, APRES la recomputation et juste
rem     avant le rafraichissement, l'applique. Elle a le dernier mot.
rem
rem   LA PLACE : les cavernes int3 font 20 octets au mieux et le detour en fait
rem   76. On ajoute donc une SECTION au fichier -- l'en-tete avait 184 octets
rem   libres pour un en-tete de plus, et le fichier se termine exactement sur
rem   une frontiere d'alignement. Aucun octet existant n'est deplace.
rem   Verifie : le jeu se lance avec la section greffee.
rem
rem   Pour revenir en arriere : decors_dural.cmd (les cinq decors sur quatre
rem   cases detournees, l'ancienne facon).
rem
rem   Touches : fleches, Entree = VALIDER, W = ANNULER, ESPACE = variante,
rem             Echap = quitter le mode.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
rem ETAT DES FICHIERS : on le POSE, on ne l'herite pas.
rem Le patcheur repart de .origine ; cote fichiers, c'est cette ligne.
rem Sans elle, le dojo VF5 R pose par decor_5r_akira.cmd restait en place
rem dans tous les autres lanceurs.
py -3 tools\importer_decor.py --retirer djo >nul 2>&1
py -3 tools\importer_decor.py --retirer trm >nul 2>&1
py -3 tools\importer_decor.py --retirer trs >nul 2>&1

py -3 tools\gen_apm_stub.py
if errorlevel 1 (
  echo.
  echo La compilation du apm.dll a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
py -3 tools\patch_moteur.py --resolution 1280 720 --langue --logo-japonais ^
    --dural --wxga --dural-grille --mode 0 --menu-init --sousmenu ^
    --transition-game --sp-menu --sp-lancer --sp-sparring --joueur2 --menu-fermer --options-raccourci --dojo-howto --dojo-cadre --options-sans-howto --menu-exit --legende-sousmenu --attract-retour-titre --sans-now-loading --options-tips --decor-perso djo --decors-dural cas --variantes --du2-collision
if errorlevel 1 (
  echo.
  echo Le patch a ECHOUE. Rien n'a ete lance.
  pause
  exit /b 1
)
echo.
echo   STAGE SELECT, case de DURAL (ligne du bas, 7e colonne).
echo   BARRE ESPACE = variante suivante : SNOW, ECLIPSE, SUBMERSION,
echo   STORM, SPACE, puis on recommence.
echo.
echo   L'apercu ne changera PAS : les cinq partagent la meme planche.
echo   Comptez vos appuis, et regardez le decor charge.
echo.
pushd "%~dp0..\runtime\media\vf5fs"
if not exist vfes.exe (
  echo INTROUVABLE : "%CD%\vfes.exe"
  pause
  popd
  exit /b 1
)
start "" "%CD%\vfes.exe"
"%SystemRoot%\System32\timeout.exe" /t 8 /nobreak >nul 2>&1
tasklist /fi "IMAGENAME eq vfes.exe" | find /i "vfes.exe" >nul
if errorlevel 1 (
  echo.
  echo LE JEU NE S'EST PAS LANCE, ou il s'est arrete aussitot.
  echo   Si c'est la section greffee, decors_dural.cmd remet un binaire
  echo   sans greffe : le patcheur repart toujours de .origine.
  pause
) else (
  echo   Le jeu tourne.
)
popd
endlocal
